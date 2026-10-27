"""Bounded rendering retries, durable review assets, and explicit failure records."""
import argparse, datetime, json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def select_episode(request, today=None):
    if request:
        if len(request)!=3 or not request.isdigit() or not (ROOT/'episodes'/f'{request}.json').is_file(): raise ValueError('Unknown episode')
        return request
    config=json.loads((ROOT/'production/studio_schedule.json').read_text())
    if not config['enabled']: return None
    from zoneinfo import ZoneInfo
    day=today or datetime.datetime.now(ZoneInfo(config['timezone'])).date()
    index=(day-datetime.date.fromisoformat(config['start_date'])).days
    return config['episodes'][index] if 0<=index<len(config['episodes']) else None

def produce(ep, runner=subprocess.run):
    out=ROOT/'output'/ep;out.mkdir(parents=True,exist_ok=True)
    report={'episode':ep,'status':'running','attempts':[],'listening_approval':'PENDING'}
    for attempt in range(1,3):
        (out/'qa.json').unlink(missing_ok=True)
        try:
            for command in [['studio/render.py','--episode',ep],['studio/verify.py',str(out)]]:
                runner([sys.executable,*command],cwd=ROOT,check=True,timeout=2400)
            if json.loads((out/'qa.json').read_text())['technical_gate']!='PASS': raise ValueError('Verification did not pass')
            report['status']='technical_pass_review_pending';report['attempts'].append({'attempt':attempt,'result':'PASS'});break
        except (subprocess.SubprocessError,ValueError,OSError) as exc:
            report['attempts'].append({'attempt':attempt,'result':'FAIL','error':str(exc)[:1000]})
            report['status']='failed'
        finally: (out/'job_report.json').write_text(json.dumps(report,indent=2))
    if report['status']=='failed': raise RuntimeError('Production failed after two attempts; see job_report.json')
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--episode',default='');p.add_argument('--select-only',action='store_true');a=p.parse_args()
    ep=select_episode(a.episode)
    if a.select_only:
        with open(os.environ['GITHUB_OUTPUT'],'a') as f:f.write('episode='+str(ep or '')+'\n')
        return
    if ep: produce(ep)
if __name__=='__main__':main()
