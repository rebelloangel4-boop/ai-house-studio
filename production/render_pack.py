"""One sequential production batch. Keep successes; do not auto-retry failed episodes."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args):subprocess.run([sys.executable,*args],cwd=ROOT,check=True)
ap=argparse.ArgumentParser();ap.add_argument('--pack',required=True);args=ap.parse_args()
assert args.pack in ('week-003','week-004')
pack=json.loads((ROOT/'packs'/f'{args.pack}.json').read_text())
results=[]
for ep in [*pack['episodes'],pack['bridges']]:
    folder=ROOT/'output'/ep;folder.mkdir(parents=True,exist_ok=True)
    signature=hashlib.sha256(b''.join((ROOT/p).read_bytes() for p in [f'episodes/{ep}.json','studio/render.py','studio/art.py','studio/landlord_art.py','studio/earnings_art.py','studio/finale_art.py','studio/voices.py','studio/verify.py'])).hexdigest()
    stamp=folder/'final.checkpoint.json'
    try:
        if not (stamp.exists() and json.loads(stamp.read_text())['signature']==signature and (folder/f'episode_{ep}.mp4').exists()):
            if ep!=pack['bridges']:(folder/f'AI_HOUSE_SHORT_{int(ep)-1:03}.mp4').unlink(missing_ok=True)
            (folder/'qa.json').unlink(missing_ok=True)
            run('studio/render.py','--episode',ep)
        run('studio/verify.py',str(folder))
        stamp.write_text(json.dumps({'signature':signature}))
        if ep!=pack['bridges']:
            import shutil
            shutil.copy2(folder/f'episode_{ep}.mp4',folder/f'AI_HOUSE_SHORT_{int(ep)-1:03}.mp4')
        results.append({'asset_id':ep,'status':'technical_pass_review_pending'})
    except subprocess.CalledProcessError as exc:
        results.append({'asset_id':ep,'status':'failed','exit_code':exc.returncode})
    (ROOT/'output'/f'{args.pack}-batch.json').write_text(json.dumps(results,indent=2))
if any(r['status']=='failed' for r in results):raise SystemExit('Failed assets retained for targeted repair; compilation skipped')
run('production/compile_week.py','--pack',args.pack)
