"""Write episode-specific upload text based on the actual rendered episode script."""
import csv,json,sys
from pathlib import Path
ep=sys.argv[1];out=Path(sys.argv[2]);src=json.loads((Path('episodes')/(ep+'.json')).read_text())
rows=list(csv.DictReader(open('production/AI_HOUSE_30_DAY_UPLOAD_METADATA.csv',newline='')))
row=next(r for r in rows if r['episode']==ep)
choice=src['scenes'][-1]['line']
title=src['title']
desc=f"{title} 🦖😂\n\nMax, Luna, Zig and Dino are back in AI HOUSE! {choice}\n\nWatch the whole episode and comment A or B to decide what happens next. Episode {int(ep)} of 30.\n\n#AIHOUSE #AnimatedComedy #Dinosaur #Shorts"
row.update(youtube_title=(title+f" 🦖 | AI HOUSE Ep {int(ep)} #Shorts")[:100],youtube_description=desc,instagram_caption=f"{title} 😂🦖\n{choice} Comment A or B! Episode {int(ep)}/30. #AIHOUSE #AnimatedComedy #Reels",facebook_caption=f"{title} | AI HOUSE Episode {int(ep)}. {choice} #AIHOUSE #Reels #AnimatedComedy")
with (out/f'episode_{ep}_upload.txt').open('w') as f:
    for k in ['youtube_title','youtube_description','youtube_tags','instagram_caption','facebook_caption']:
        f.write(k.upper().replace('_',' ')+':\n'+row[k]+'\n\n')
print('Episode-specific metadata written')
