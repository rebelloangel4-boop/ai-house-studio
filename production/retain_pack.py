"""Draft review assets only; never publish to YouTube or Drive."""
import os,subprocess,sys
from pathlib import Path
assert len(sys.argv)==2 and sys.argv[1] in ('week-003','week-004')
pack=sys.argv[1];week=int(pack.rsplit('-',1)[1])
files=list(Path('output').glob('*/AI_HOUSE_SHORT_*.mp4'))+list(Path('output').glob(f'{pack}/AI_HOUSE_WEEK_{week:02}_FULL.mp4'))
if files:
    tag=f'week{week}-review-'+os.environ['GITHUB_RUN_ID']
    subprocess.run(['gh','release','create',tag,'--draft','--target',os.environ['GITHUB_SHA'],'--title',f'AI HOUSE Week {week} review MP4s','--notes','Individual technically verified videos. Creative and listening review pending. No public publishing.'],check=True)
    subprocess.run(['gh','release','upload',tag,*map(str,files)],check=True)
