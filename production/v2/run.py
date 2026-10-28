"""Resumable render -> technical QA. Never claim creative approval automatically."""
import argparse,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def run(ep):
 for attempt in range(2):
  try:
   subprocess.run([sys.executable,'studio/render.py','--episode',ep],cwd=ROOT,check=True)
   subprocess.run([sys.executable,'production/v2/verify.py',ep],cwd=ROOT,check=True)
   return
  except subprocess.CalledProcessError:
   if attempt:raise
   time.sleep(2)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--episode',required=True,choices=[f'2{i:02}' for i in range(1,11)]);args=ap.parse_args();run(args.episode)
