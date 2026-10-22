"""Draft review assets only; never publish to YouTube or Drive."""
import os,subprocess
from pathlib import Path
files=list(Path('output').glob('*/AI_HOUSE_SHORT_*.mp4'))+list(Path('output').glob('week-002/AI_HOUSE_WEEK_02_FULL.mp4'))
if files:
    tag='week2-review-'+os.environ['GITHUB_RUN_ID']
    subprocess.run(['gh','release','create',tag,'--draft','--target',os.environ['GITHUB_SHA'],'--title','AI HOUSE Week 2 review MP4s','--notes','Individual technically verified videos. Creative and listening review pending. No public publishing.'],check=True)
    subprocess.run(['gh','release','upload',tag,*map(str,files)],check=True)
