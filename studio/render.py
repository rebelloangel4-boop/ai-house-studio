"""AI HOUSE production renderer. Generates review files only; never uploads to YouTube."""
import argparse, hashlib, json, math, os, re, subprocess, wave
from pathlib import Path
import numpy as np
from art import render
ROOT=Path(__file__).resolve().parents[1]; SR=24000; FPS=30
from voices import VoicePipeline, speech, VOICES
def ff(*args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
def wavwrite(path,data):
    with wave.open(str(path),'wb') as f:
        f.setnchannels(1 if data.ndim==1 else data.shape[1]);f.setsampwidth(2);f.setframerate(SR);f.writeframes((np.clip(data,-.98,.98)*32767).astype('<i2').tobytes())
def wavread(path):
    with wave.open(str(path),'rb') as f:
        assert f.getframerate()==SR
        return np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(np.float32)/32768

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
    for i in range(0,len(tokens),4):
        chunk=tokens[i:i+4]
        end=min(chunk[-1]['end']+.12,tokens[i+4]['start']) if i+4<len(tokens) else chunk[-1]['end']+.12
        if chunk[0]['start']-.05<=t<end:return caption_text(chunk)
    return ''

def polish_dialogue(data,tokens,who):
    """Trim quiet edges, retain breaths, and modestly quicken delivery without pitch shifts."""
    block=240
    rms=np.array([np.sqrt(np.mean(data[i:i+block]**2)) for i in range(0,len(data),block)])
    active=np.flatnonzero(rms>max(.0015,float(rms.max())*.025))
    if not len(active):raise ValueError('Silent dialogue')
    start=max(0,int(active[0]*block-.06*SR))
    end=min(len(data),int((active[-1]+1)*block+.09*SR))
    # Preserve any quiet phonemes that the existing alignment identified.
    start=min(start,max(0,int((tokens[0]['start']-.04)*SR)))
    end=max(end,min(len(data),int((tokens[-1]['end']+.06)*SR)))
    cropped=data[start:end]
    rate={'Luna':1.04,'Max':1.06,'Zig':1.08}[who]
    result=subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(SR),'-ac','1','-i','pipe:0',
        '-af',f'highpass=f=65,atempo={rate}', '-f','f32le','-ar',str(SR),'-ac','1','pipe:1'],
        input=cropped.astype('<f4').tobytes(),capture_output=True,check=True)
    audio=np.frombuffer(result.stdout,dtype='<f4').copy()
    scale=len(audio)/len(cropped);limit=len(audio)/SR
    aligned=[dict(q,start=max(0,min(limit,(q['start']-start/SR)*scale)),
        end=max(0,min(limit,(q['end']-start/SR)*scale))) for q in tokens]
    return audio,aligned,{'tempo':rate,'trimmed_seconds':round((len(data)-len(cropped))/SR,3)}

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
        a=int(start*SR);b=min(n,a+int(length*SR))
        if b<=a:return
        u=np.arange(b-a)/SR
        sfx[a:b]+=amp*np.sin(2*np.pi*(freq*u+sweep*u*u))*np.sin(np.pi*np.minimum(1,u/length))**2
    if kind=='rent':tone(.05,.45,110,.11,-55)
    if kind in ('egg','scan'):
        for i in range(4):tone(.2+i*.12,.17,660+i*170,.045)
    if kind in ('hatch','meeting'):
        a=int(1.1*SR);b=min(n,a+int(.17*SR));sfx[a:b]+=.08*rng.standard_normal(b-a)*np.exp(-np.arange(b-a)/(SR*.035));tone(1.38,.25,900,.07,1300)
    if kind in ('fire','chomp'):
        a=int(.65*SR);b=min(n,int(1.75*SR));noise=rng.standard_normal(b-a);noise=np.convolve(noise,np.ones(25)/25,mode='same')
        sfx[a:b]+=.19*noise*np.sin(np.linspace(0,np.pi,b-a))**2;tone(1.75,.22,95,.12,-120)
    if kind in ('thermostat','deposit','pets','meter','inspection','ceiling','daycare','translator','pizza','influencer','snacks','clone','accountant','audit','ban','campaign','promise','debate','ballots','recount','house_vote','couch_boss'):
        tone(.08,.12,740,.025);tone(max(.25,duration-.22),.12,370,.025)
    speechtrack=np.zeros(n);a=int(lead*SR);b=min(n,a+len(audio));speechtrack[a:b]=audio[:b-a]
    duck=np.ones(n);duck[max(0,a-int(.12*SR)):min(n,b+int(.15*SR))]=.28
    music*=duck;fade=np.minimum(1,t/.025)*np.minimum(1,(duration-t)/.12)
    stereo=np.stack((speechtrack+music+sfx,speechtrack+np.roll(music,100)+sfx*.92),axis=1)*fade[:,None]
    assert np.max(np.abs(stereo))<1,'Audio clipping before mastering'
    return stereo

def srt_time(t):
    ms=round(t*1000);s,ms=divmod(ms,1000);m,s=divmod(s,60);h,m=divmod(m,60);return f'{h:02}:{m:02}:{s:02},{ms:03}'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--episode',default='001');ap.add_argument('--preview',action='store_true')
    ap.add_argument('--dialogue-source',type=Path,help='Reuse verified original dry voices and alignments without new inference')
    args=ap.parse_args()
    story=json.loads((ROOT/'episodes'/f'{args.episode}.json').read_text());out=ROOT/'output'/args.episode;out.mkdir(parents=True,exist_ok=True)
    cache=ROOT/'.voice-cache';cache.mkdir(exist_ok=True)
    if args.preview:
        for i,s in enumerate(story['scenes']):render(s,i,2,5,s['speaker'],'wide',.4,s['line'],story['episode']).save(out/f'shot_{i}.jpg')
        return
    pipeline=None;records=[]
    if args.dialogue_source:
        source_qa=json.loads((args.dialogue_source/'voice_qa.json').read_text())
        source_timeline=json.loads((args.dialogue_source/'timeline.json').read_text())
        assert len(source_qa['segments'])==len(story['scenes'])==len(source_timeline)
    else:pipeline=VoicePipeline()
    timeline=[];subtitle=[];offset=0;clips=[]
    for i,s in enumerate(story['scenes']):
        if args.dialogue_source:
            record=source_qa['segments'][i]
            assert record['script']==s['line'] and record['voice']==VOICES[s['speaker']]
            assert record['automated_validation']=='PASS'
            assert 'post_processing' not in record,'Reuse original dry dialogue, not an already tempo-adjusted export'
            data=wavread(args.dialogue_source/f'dialogue_{i:02}_{s["speaker"]}.wav')
            tokens=source_timeline[i]['tokens'];records.append(dict(record))
        else:
            data,tokens=speech(pipeline,s['line'],s['speaker'],cache);records.append(dict(pipeline.records[-1]))
        original=out/'original_dialogue';original.mkdir(exist_ok=True)
        wavwrite(original/f'dialogue_{i:02}_{s["speaker"]}.wav',data)
        (original/f'scene_{i}.json').write_text(json.dumps({'tokens':tokens,'report':records[-1]},indent=2))
        data,tokens,polish=polish_dialogue(data,tokens,s['speaker'])
        records[-1].update(post_processing=polish,duration=len(data)/SR)
        lead=.04 if i==0 else .06
        tail=.45 if s.get('visual')=='vote' else .14
        action_min={'hatch':1.65,'fire':2.05,'chomp':2.05}.get(s.get('visual'),1.25)
        duration=max(action_min,len(data)/SR+lead+tail)
        if 'seconds' in s:
            duration=float(s['seconds'])
            if lead+len(data)/SR+.08>duration:
                raise ValueError(f'Scene {i}: natural dialogue needs {lead+len(data)/SR+.08:.2f}s, slot is {duration:.2f}s; rewrite rather than truncate')
        wavwrite(out/f'dialogue_{i:02}_{s["speaker"]}.wav',data)
        count=math.ceil(duration*FPS);duration=count/FPS
        kind=s.get('visual',['rent','egg','scan','hatch','fire','vote'][min(i,5)])
        sound=out/f'scene_{i}.wav';wavwrite(sound,mix(data,duration,kind,lead));clip=out/f'scene_{i}.mp4'
        command=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-r',str(FPS),'-i','pipe:0','-i',str(sound),'-map','0:v','-map','1:a','-c:v','libx264','-threads','2','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-t',str(duration),str(clip)]
        checkpoint=out/f'scene_{i}.checkpoint.json'
        signature=hashlib.sha256(data.tobytes()+json.dumps([s,tokens,duration],sort_keys=True).encode()+(ROOT/'studio/art.py').read_bytes()+(ROOT/'studio/landlord_art.py').read_bytes()+(ROOT/'studio/earnings_art.py').read_bytes()+(ROOT/'studio/finale_art.py').read_bytes()+(ROOT/'studio/render.py').read_bytes()).hexdigest()
        reusable=False
        if clip.exists() and checkpoint.exists() and json.loads(checkpoint.read_text()).get('signature')==signature:
            check=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(clip),'-f','null','-'],capture_output=True)
            reusable=check.returncode==0
        if not reusable:
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
            checkpoint.write_text(json.dumps({'signature':signature,'frames':count}))
        clips.append(clip)
        for j in range(0,len(tokens),4):
            chunk=tokens[j:j+4];subtitle.append((offset+lead+chunk[0]['start'],offset+lead+chunk[-1]['end'],caption_text(chunk)))
        timeline.append({'scene':i,'start':offset,'duration':duration,'lead':lead,'speech_seconds':len(data)/SR,'speaker':s['speaker'],'voice':VOICES[s['speaker']],'tokens':tokens,'visual':kind})
        offset+=duration
        print(f'Scene {i+1}/{len(story["scenes"])} complete: {duration:.2f}s',flush=True)
    print(f'Dialogue-led edit duration: {offset:.2f}s',flush=True)
    playlist=out/'concat.txt';playlist.write_text(''.join(f"file '{c.name}'\n" for c in clips))
    raw=out/'assembled.mp4';final=out/f'episode_{args.episode}.mp4'
    ff('-f','concat','-safe','0','-i',playlist,'-c','copy',raw)
    # Loudness normalization with a conservative true-peak ceiling; stereo stays stereo.
    video_args=['-c:v','copy']
    if story.get('exact_seconds'):
        # Drop accumulated AAC packet padding from the video time base; never drop frames.
        video_args=['-vf','setpts=N/(30*TB)','-c:v','libx264','-preset','veryfast','-crf','19','-threads','2','-t',str(story['exact_seconds'])]
    ff('-i',raw,*video_args,'-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000','-ac','2','-c:a','aac','-b:a','192k','-movflags','+faststart',final)
    (out/'voice_qa.json').write_text(json.dumps({'voices':VOICES,'segments':records,'listening_approval':'PENDING'},indent=2))
    (out/'captions.srt').write_text('\n\n'.join(f'{i+1}\n{srt_time(a)} --> {srt_time(b)}\n{text}' for i,(a,b,text) in enumerate(subtitle))+'\n')
    (out/'timeline.json').write_text(json.dumps(timeline,indent=2))
    (out/'metadata.json').write_text(json.dumps({'title':story['title'],'description':story.get('description','Three roommates. One terrible decision. Choose A or B in the comments. #AIHOUSE #AnimatedComedy #Shorts'),'tags':['AI HOUSE','animated comedy','interactive story'],'publishing_approved':False,'alignment':'Whisper word timestamps mapped to original script; mouth shapes approximate', 'voice_engine':'pocket-tts-3.3.0', 'listening_approval':'PENDING','duration':offset},indent=2))
    for p in [raw,playlist]:p.unlink()
    print(f'RENDERED FOR REVIEW: {final}',flush=True)
if __name__=='__main__':main()
