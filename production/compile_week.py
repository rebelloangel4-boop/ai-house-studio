"""Re-edit seven Shorts with original connective scenes and one closing vote."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def ff(*args):subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pack',default='week-001');a=ap.parse_args()
    pack=json.loads((ROOT/'packs'/f'{a.pack}.json').read_text());out=ROOT/'output';target=out/a.pack;target.mkdir(exist_ok=True)
    bridge=out/pack['bridges'];bt=json.loads((bridge/'timeline.json').read_text());assert len(bt)==len(pack['episodes'])+1
    pieces=[];chapters=[];offset=0
    def cut(source,start,duration):
        nonlocal offset
        p=target/f'part_{len(pieces):02}.mp4'
        ff('-ss',start,'-i',source,'-t',duration,'-vf','split=2[bg][fg];[bg]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=40:2[back];[fg]scale=608:1080[front];[back][front]overlay=(W-w)/2:(H-h)/2,format=yuv420p','-c:v','libx264','-threads','2','-preset','veryfast','-crf','20','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',p)
        pieces.append(p);offset+=duration
    for i,ep in enumerate(pack['episodes']):
        folder=out/ep;qa=json.loads((folder/'qa.json').read_text());assert qa['technical_gate']=='PASS'
        timeline=json.loads((folder/'timeline.json').read_text());story=json.loads((ROOT/'episodes'/f'{ep}.json').read_text())
        has_vote=timeline[-1]['visual']=='vote'
        chapters.append({'start':round(offset,3),'title':story['title']})
        cut(bridge/f'episode_{pack["bridges"]}.mp4',bt[i]['start'],bt[i]['duration'])
        # Remove repeated CTAs, preserving each story and its punchline.
        cut(folder/f'episode_{ep}.mp4',0,timeline[-1]['start'] if has_vote else sum(s['duration'] for s in timeline))
    cut(bridge/f'episode_{pack["bridges"]}.mp4',bt[-1]['start'],bt[-1]['duration'])
    playlist=target/'concat.txt';playlist.write_text(''.join(f"file '{p.name}'\n" for p in pieces));raw=target/'raw.mp4';final=target/f'AI_HOUSE_WEEK_{int(a.pack.rsplit("-",1)[1]):02}_FULL.mp4'
    ff('-f','concat','-safe','0','-i',playlist,'-c','copy',raw)
    ff('-i',raw,'-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000','-ac','2','-c:a','aac','-b:a','160k','-movflags','+faststart',final)
    ff('-xerror','-i',final,'-f','null','-')
    duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(final)]))
    assert abs(duration-offset)<1 and 20<duration<600
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','json',str(final)]))
    assert (probe['streams'][0]['width'],probe['streams'][0]['height'])==(1920,1080), 'Landscape 1080p required'
    assert final.stat().st_size<80_000_000,'Storage budget exceeded'
    (target/'metadata.json').write_text(json.dumps({'title':pack.get('title','A Dinosaur Ate Our Rent | AI HOUSE: The Complete First Week'),'chapters':chapters,'duration':duration,'publishing_approved':False,'votes_counted':False},indent=2))
    (target/'qa.json').write_text(json.dumps({'technical_gate':'PASS','creative_approval':'PENDING','source_episodes':pack['episodes'],'connective_scenes':len(bt),'repeated_vote_scenes_removed':sum(json.loads((out/e/'timeline.json').read_text())[-1]['visual']=='vote' for e in pack['episodes']),'duration':duration,'resolution':'1920x1080','landscape_edit':'centered vertical composition with blurred extended background','publishing_enabled':False},indent=2))
    for p in pieces+[raw,playlist]:p.unlink()
    print(f'Compilation ready for review: {final}')
if __name__=='__main__':main()
