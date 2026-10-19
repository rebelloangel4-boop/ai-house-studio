"""AI HOUSE production renderer. Generates review files only; never uploads to YouTube."""
import argparse, hashlib, json, math, os, re, subprocess, wave
from pathlib import Path
import numpy as np
from art import render
ROOT=Path(__file__).resolve().parents[1]; SR=24000; FPS=30
VOICES={'Luna':('af_heart',0.97),'Max':('am_michael',1.00),'Zig':('am_fenrir',0.96)}
def ff(*args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
def wavwrite(path,data):
    with wave.open(str(path),'wb') as f:
        f.setnchannels(1 if data.ndim==1 else data.shape[1]);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(data,-.98,.98)*32767).astype('<i2').tobytes())
def wavread(path):
    with wave.open(str(path),'rb') as f:
        assert f.getframerate()==SR
        return np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)/32768

def speech(pipeline,line,who,cache):
    voice,speed=VOICES[who];key=hashlib.sha256(f'v3-natural|{line}|{voice}|{speed}'.encode()).hexdigest()[:20]
    wav=cache/f'{key}.wav';meta=cache/f'{key}.json'
    if wav.exists() and meta.exists():return wavread(wav),json.loads(meta.read_text())
    parts=[];tokens=[];offset=0
    for result in pipeline(line,voice=voice,speed=speed,split_pattern=r'(?<=[.!?])\\s+') :
        a=np.asarray(result.audio,dtype=np.float32);parts.append(a)
        for token in result.tokens or []:
            start=getattr(token,'start_ts',None);end=getattr(token,'end_ts',None)
            if start is not None and end is not None:
                tokens.append({'text':token.text,'phonemes':token.phonemes or '', 'start':offset+float(start),'end':offset+float(end)})
        offset+=len(a)/SR
    if not parts or not tokens:raise RuntimeError('Speech or word alignment missing; refusing unsynchronised render')
    audio=np.concatenate(parts)
    peak=float(np.max(np.abs(audio)))
    if peak<.001:raise RuntimeError('Silent speech')
    audio=audio*(.66/peak);wavwrite(wav,audio);meta.write_text(json.dumps(tokens))
    return audio,tokens

def viseme(audio,tokens,t):
    n=int(t*SR)
    if n<0 or n>=len(audio):return 'rest',0.
    samples=audio[max(0,n-240):min(len(audio),n+480)];rms=float(np.sqrt(np.mean(samples*samples)))
    if rms<.012:return 'rest',0.
    tk=next((tk for tk in tokens if tk['start']<=t<=tk['end']),None)
    if not tk:return 'rest',0.
    # Kokoro provides word alignment; phonemes within each word are interpolated.
    ps=tk['phonemes'];ratio=(t-tk['start'])/max(.001,tk['end']-tk['start']);ch=ps[min(len(ps)-1,int(ratio*len(ps)))] if ps else 'a'
    return ('closed' if ch in 'pbm' else 'round' if ch in 'uʊoɔw' else 'wide'),min(1,rms*9)

def caption_text(chunk):
    return re.sub(r'\s+([,.!?;:])', r'\1', ' '.join(q['text'] for q in chunk))

def caption_at(tokens,t):
    for i in range(0,len(tokens),5):
        chunk=tokens[i:i+5]
        end=tokens[i+5]['start'] if i+5<len(tokens) else chunk[-1]['end']+.2
        if chunk[0]['start']-.05<=t<end:return caption_text(chunk)
    return ''

def mix(audio,duration,kind,lead):
    n=math.ceil(duration*SR);t=np.arange(n)/SR;music=np.zeros(n);sfx=np.zeros(n)
    # Original, deterministic pizzicato score; no recordings or copyrighted samples.
    notes=[146.83,220,293.66,349.23,293.66,220,164.81,220]
    for i,start in enumerate(np.arange(0,duration,.48)):
        u=t-start;mask=(u>=0)&(u<.65);v=u[mask]
        music[mask]+=.013*np.sin(2*np.pi*notes[i%8]*v)*np.exp(-v*9)
        music[mask]+=.005*np.sin(2*np.pi*notes[i%8]*2*v)*np.exp(-v*13)
    rng=np.random.default_rng(76)
    def tone(start,length,freq,amp=.09,sweep=0):
        a=int(start*SR);b=min(n,a+int(length*SR));u=np.arange(b-a)/SR
        sfx[a:b]+=amp*np.sin(2*np.pi*(freq*u+sweep*u*u))*np.sin(np.pi*np.minimum(1,u/length))**2
    if kind=='rent':tone(.05,.45,110,.11,-55)
    if kind in ('egg','scan'):
        for i in range(4):tone(.2+i*.12,.17,660+i*170,.045)
    if kind in ('hatch','meeting'):
        a=int(1.1*SR);b=min(n,a+int(.17*SR));sfx[a:b]+=.08*rng.standard_normal(b-a)*np.exp(-np.arange(b-a)/(SR*.035));tone(1.38,.25,900,.07,1300)
    if kind in ('fire','chomp'):
        a=int(.65*SR);b=min(n,int(1.75*SR));noise=rng.standard_normal(b-a);noise=np.convolve(noise,np.ones(25)/25,mode='same')
        sfx[a:b]+=.19*noise*np.sin(np.linspace(0,np.pi,b-a))**2;tone(1.75,.22,95,.12,-120)
    speechtrack=np.zeros(n);a=int(lead*SR);b=min(n,a+len(audio));speechtrack[a:b]=audio[:b-a]
    duck=np.ones(n);duck[max(0,a-int(.12*SR)):min(n,b+int(.15*SR))]=.28
    music*=duck;fade=np.minimum(1,t/.025)*np.minimum(1,(duration-t)/.12)
    stereo=np.stack((speechtrack+music+sfx,speechtrack+np.roll(music,100)+sfx*.92),axis=1)*fade[:,None]
    assert np.max(np.abs(stereo))<1,'Audio clipping before mastering'
    return stereo

def srt_time(t):
    ms=round(t*1000);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60);return f'{h:02}:{m:02}:{s:02},{ms:03}'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--episode',default='001');ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    story=json.loads((ROOT/'episodes'/f'{args.episode}.json').read_text());out=ROOT/'output'/args.episode;out.mkdir(parents=True,exist_ok=True)
    cache=ROOT/'.voice-cache';cache.mkdir(exist_ok=True)
    if args.preview:
        for i,s in enumerate(story['scenes']):render(s,i,2,5,s['speaker'],'wide',.4,s['line'],story['episode']).save(out/f'shot_{i}.jpg')
        return
    from kokoro import KPipeline
    import torch
    torch.set_num_threads(2)
    pipeline=KPipeline(lang_code='a',repo_id='hexgrad/Kokoro-82M',device='cpu')
    timeline=[];subtitle=[];offset=0;clips=[]
    for i,s in enumerate(story['scenes']):
        data,tokens=speech(pipeline,s['line'],s['speaker'],cache);lead=float(s.get('lead',.3));duration=max(float(s.get('min_seconds',4)),len(data)/SR+lead+.10)
        count=math.ceil(duration*FPS);duration=count/FPS
        kind=s.get('visual',['rent','egg','scan','hatch','fire','vote'][min(i,5)])
        sound=out/f'scene_{i}.wav';wavwrite(sound,mix(data,duration,kind,lead));clip=out/f'scene_{i}.mp4'
        command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(FPS),'-i','pipe:0','-i',str(sound),'-map','0:v','-map','1:a','-c:v','libx264','-threads','2','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-t',str(duration),str(clip)]
        process=subprocess.Popen(command,stdin=subprocess.PIPE)
        try:
            for frame_no in range(count):
                t=frame_no/FPS;mouth,energy=viseme(data,tokens,t-lead);caption=caption_at(tokens,t-lead)
                im=render(s,i,t,duration,s['speaker'],mouth,energy,caption,story['episode'])
                if frame_no==min(count-1,60):im.save(out/f'shot_{i}.jpg',quality=92)
                process.stdin.write(im.tobytes())
            process.stdin.close()
            if process.wait()!=0:raise RuntimeError(f'Encoder failed on scene {i}')
        finally:
            if process.poll() is None:process.kill();process.wait()
        clips.append(clip)
        for j in range(0,len(tokens),5):
            chunk=tokens[j:j+5];subtitle.append((offset+lead+chunk[0]['start'],offset+lead+chunk[-1]['end'],caption_text(chunk)))
        timeline.append({'scene':i,'start':offset,'duration':duration,'lead':lead,'speech_seconds':len(data)/SR,'speaker':s['speaker'],'tokens':tokens,'visual':kind})
        offset+=duration
        print(f'Scene {i+1}/{len(story["scenes"])} complete: {duration:.2f}s',flush=True)
    if story.get('target_seconds') and not 24 <= offset <= 26: print(f'WARNING: Target 24–26s, actual {offset:.2f}s',flush=True)
    playlist=out/'concat.txt';playlist.write_text(''.join(f"file '{c.name}'\n" for c in clips))
    raw=out/'assembled.mp4';final=out/f'episode_{args.episode}.mp4'
    ff('-f','concat','-safe','0','-i',playlist,'-c','copy',raw)
    # Loudness normalization with a conservative true-peak ceiling; stereo stays stereo.
    ff('-i',raw,'-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000','-ac','2','-c:a','aac','-b:a','192k','-movflags','+faststart',final)
    (out/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt_time(a)} --> {srt_time(b)}\n{text}' for i,(a,b,text) in enumerate(subtitle))+'\n')
    (out/'timeline.json').write_text(json.dumps(timeline,indent=2))
    (out/'metadata.json').write_text(json.dumps({'title':story['title'],'description':story.get('description','Three roommates. One terrible decision. Choose A or B in the comments. #AIHOUSE #AnimatedComedy #Shorts'),'tags':['AI HOUSE','animated comedy','interactive story'],'publishing_approved':False,'alignment':'Kokoro word timestamps; within-word visemes are approximate','duration':offset},indent=2))
    for p in clips+[out/f'scene_{i}.wav' for i in range(len(clips))]+[raw,playlist]:p.unlink()
    print(f'RENDERED FOR REVIEW: {final}',flush=True)
if __name__=='__main__':main()
