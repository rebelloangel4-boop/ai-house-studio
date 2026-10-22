"""One sequential production batch. Keep successes; do not auto-retry failed episodes."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args):subprocess.run([sys.executable,*args],cwd=ROOT,check=True)
results=[]
for ep in ('010','011','012','013','014','015','032'):
    folder=ROOT/'output'/ep;folder.mkdir(parents=True,exist_ok=True)
    signature=hashlib.sha256(b''.join((ROOT/p).read_bytes() for p in [f'episodes/{ep}.json','studio/render.py','studio/art.py','studio/landlord_art.py','studio/voices.py','studio/verify.py'])).hexdigest()
    stamp=folder/'final.checkpoint.json'
    try:
        if not (stamp.exists() and json.loads(stamp.read_text())['signature']==signature and (folder/f'episode_{ep}.mp4').exists()):
            if ep!='032':(folder/f'AI_HOUSE_SHORT_{int(ep)-1:03}.mp4').unlink(missing_ok=True)
            (folder/'qa.json').unlink(missing_ok=True)
            run('studio/render.py','--episode',ep)
        run('studio/verify.py',str(folder))
        stamp.write_text(json.dumps({'signature':signature}))
        if ep!='032':
            import shutil
            shutil.copy2(folder/f'episode_{ep}.mp4',folder/f'AI_HOUSE_SHORT_{int(ep)-1:03}.mp4')
        results.append({'asset_id':ep,'status':'technical_pass_review_pending'})
    except subprocess.CalledProcessError as exc:
        results.append({'asset_id':ep,'status':'failed','exit_code':exc.returncode})
    (ROOT/'output/week2-batch.json').write_text(json.dumps(results,indent=2))
if any(r['status']=='failed' for r in results):raise SystemExit('Failed assets retained for targeted repair; compilation skipped')
run('production/compile_week.py','--pack','week-002')
