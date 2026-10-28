"""CPU neural dialogue with licensed presets, ASR checks and no fallback voice."""
import hashlib, json, re, time
from difflib import SequenceMatcher
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly

SR = 24000
VOICES = {'Luna': 'alba', 'Max': 'marius', 'Zig': 'javert'}
ENGINE = 'pocket-tts-3.3.0-v4'

from alignment import normal, merge_asr_words, expand_asr_numbers

class VoicePipeline:
    def __init__(self):
        import torch
        from pocket_tts import TTSModel
        from faster_whisper import WhisperModel
        torch.set_num_threads(2)
        self.tts = TTSModel.load_model(language='english')
        self.states = {who: self.tts.get_state_for_audio_prompt(v) for who, v in VOICES.items()}
        self.asr = WhisperModel('base.en', device='cpu', compute_type='int8', cpu_threads=2)
        self.records = []
        self.precise_asr = None

    def generate(self, line, who, seed):
        import torch
        torch.manual_seed(seed)
        # Keep the wording. Mixed case avoids spelling out an all-caps shouted hook.
        spoken = line if not line.isupper() else line.capitalize().replace('Max!', 'Max!')
        a = self.tts.generate_audio(self.states[who], spoken).detach().cpu().numpy().astype(np.float32)
        if self.tts.sample_rate != SR:
            from math import gcd
            g = gcd(SR, self.tts.sample_rate)
            a = resample_poly(a, SR//g, self.tts.sample_rate//g).astype(np.float32)
        if not np.isfinite(a).all() or not .4 < len(a)/SR < 25:
            raise ValueError('Invalid speech samples or duration')
        peak = float(np.max(np.abs(a)))
        if peak < .015 or np.mean(np.abs(a) >= .999) > .001:
            raise ValueError('Silent or clipped source speech')
        # Retain intra-line dynamics; conservative gain, no pitch shift or speed-up.
        a *= min(1.5, .66/peak)
        padded = np.pad(resample_poly(a, 2, 3), (8000, 8000))
        words = line.split()
        ref = [normal(w) for w in words]
        for asr_pass in range(2):
            if asr_pass:
                from faster_whisper import WhisperModel
                if self.precise_asr is None:
                    self.precise_asr = WhisperModel('small.en',device='cpu',compute_type='int8',cpu_threads=2)
                asr = self.precise_asr
            else:
                asr = self.asr
            segments, _ = asr.transcribe(padded, language='en', beam_size=5,
                word_timestamps=True, condition_on_previous_text=False, temperature=0)
            heard = [w for segment in segments for w in segment.words or [] if normal(w.word)]
            heard = merge_asr_words(expand_asr_numbers(heard, words), words)
            hyp = [normal(w.word) for w in heard]
            matcher = SequenceMatcher(None, ref, hyp, autojunk=False)
            matches = sum(b.size for b in matcher.get_matching_blocks())
            coverage = matches/max(len(ref), len(hyp), 1)
            if coverage >= .95 and heard:break
        if coverage < .95 or not heard:
            raise ValueError(f'Transcript mismatch ({coverage:.2f}): {" ".join(w.word for w in heard)}')
        # Preserve original captions. Exact matching words anchor timing; minor ASR
        # spelling differences interpolate only inside the neighboring word interval.
        tokens = [None]*len(words)
        for tag, i, j, k, l in matcher.get_opcodes():
            if tag == 'equal':
                for x, y in zip(range(i,j), range(k,l)):
                    tokens[x] = {'text': words[x], 'phonemes': words[x].lower(),
                                 'start': max(0.,heard[y].start-.5), 'end': min(len(a)/SR,max(0.,heard[y].end-.5))}
            elif j > i:
                start = max(0.,(heard[k].start if k < len(heard) else heard[-1].end)-.5)
                end = min(len(a)/SR,max(start,(heard[l-1].end if l > k else (heard[k].start if k < len(heard) else len(a)/SR+.5))-.5))
                for x in range(i,j):
                    tokens[x] = {'text':words[x], 'phonemes':words[x].lower(),
                        'start':start+(end-start)*(x-i)/(j-i), 'end':start+(end-start)*(x-i+1)/(j-i)}
        assert all(t is not None and 0 <= t['start'] <= t['end'] <= len(a)/SR+.1 for t in tokens)
        return a, tokens, {'speaker':who, 'voice':VOICES[who], 'script':line,
            'transcript':' '.join(w.word.strip() for w in heard), 'word_match':round(coverage,3),
            'duration':len(a)/SR, 'source_peak':peak, 'seed':seed,
            'asr_model':'small.en' if asr_pass else 'base.en', 'automated_validation':'PASS', 'naturalness_listening':'NOT_AUDITIONED'}

def speech(pipeline, line, who, cache):
    import soundfile as sf
    key = hashlib.sha256(f'{ENGINE}|{line}|{VOICES[who]}'.encode()).hexdigest()[:20]
    wav = cache/f'{key}.wav'; meta = cache/f'{key}.json'
    if wav.exists() and meta.exists():
        payload = json.loads(meta.read_text()); a, sr = sf.read(wav, dtype='float32')
        assert sr == SR
    else:
        errors = []
        for attempt in range(5):
            try:
                a, tokens, report = pipeline.generate(line, who, int(hashlib.sha256(f'pocket-tts-3.3.0-v1|{line}|{VOICES[who]}'.encode()).hexdigest()[:7],16)+attempt)
                payload = {'tokens':tokens, 'report':report}
                sf.write(wav, a, SR, subtype='PCM_16'); meta.write_text(json.dumps(payload,indent=2))
                break
            except Exception as e:
                errors.append(str(e)); print(f'Voice retry {who} {attempt+1}/5: {e}', flush=True)
                if attempt == 4: raise RuntimeError(f'No acceptable speech; no fallback: {errors}') from e
                time.sleep(1)
    pipeline.records.append(payload['report'])
    # Keep dry dialogue for independent review, without music masking it.
    return a, payload['tokens']
