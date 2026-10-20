"""Technical quality gate; human creative approval is separately required."""
import json, subprocess, sys
from pathlib import Path
import numpy as np

def verify(folder):
    folder=Path(folder);files=list(folder.glob('episode_*.mp4'));assert len(files)==1,files
    p=files[0];probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
    v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
    assert (v['width'],v['height'])==(1080,1920)
    assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and v['r_frame_rate']=='30/1'
    assert a['codec_name']=='aac' and a['channels']==2 and a['sample_rate']=='48000'
    duration=float(probe['format']['duration']);assert 10<duration<65
    # Dialogue-led cuts can be shorter than 15s; require every scripted word instead of padding.
    timeline=json.loads((folder/'timeline.json').read_text());assert abs(sum(s['duration'] for s in timeline)-duration)<.15
    story=json.loads((Path(__file__).resolve().parents[1]/'episodes'/f'{folder.name}.json').read_text())
    assert len(timeline)==len(story['scenes']),'Missing scene'
    for scene,shot in zip(story['scenes'],timeline):
        assert [t['text'] for t in shot['tokens']]==scene['line'].split(),'Missing or changed dialogue'
        assert shot['speaker']==scene['speaker']
    for s in timeline:
        assert s['lead']+s['speech_seconds']<=s['duration']+.04, 'Speech truncated or scene timing inconsistent'
        assert s['tokens'] and all(0<=t['start']<=t['end']<=s['speech_seconds']+.3 for t in s['tokens'])
    samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vn','-f','f32le','-ac','2','-ar','24000','pipe:1']),dtype='<f4')
    peak=float(np.max(np.abs(samples)));rms=float(np.sqrt(np.mean(samples*samples)));assert .02<rms<.4;assert peak<.99
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True)
    # Confirm actual pixel changes within the first shot, not just different shot files.
    def frame(t):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=270:480','-f','rawvideo','-pix_fmt','rgb24','pipe:1']),dtype=np.uint8).astype(float)
    motion=float(np.mean(np.abs(frame(.6)-frame(1.4))));assert motion>.05
    assert (folder/'captions.srt').stat().st_size>50
    report={'technical_gate':'PASS','creative_approval':'PENDING','duration_seconds':duration,'resolution':'1080x1920','fps':30,'stereo':True,'sample_peak_dbfs':round(20*np.log10(peak),2),'rms_dbfs':round(20*np.log10(rms),2),'motion_difference':round(motion,3),'size_mb':round(p.stat().st_size/1e6,2),'publishing_enabled':False,'listening_approval':'PENDING','voice_identities':sorted(set(s['voice'] for s in timeline))}
    (folder/'qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':verify(sys.argv[1])
