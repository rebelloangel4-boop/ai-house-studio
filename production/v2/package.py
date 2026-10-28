"""Prepare individual MP4 exports and original thumbnails; retain honest review flags."""
import json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'studio'))
from PIL import Image
from art import Canvas,actor,dinosaur
CAPTIONS=['$10 MILLION TRAP','DINO SAVES EARTH?','PRESIDENT DINO','HUMANS: FIRED','EVIL FUTURE MAX','THE BILLION $ EGG','10 MINUTES LEFT','EARTH: EXPIRED','100 SECRET DOORS','REALITY IS FAKE']
ATTRIBUTION='Synthetic voices: Pocket TTS by Kyutai (CC BY 4.0), Manu Orsini, Simon Rouard, Gabriel De Marmiesse, Václav Volhejn, Neil Zeghidour and Alexandre Défossez. Luna uses Alba MacKenna / Kyutai casual voice (CC BY 4.0); Max and Zig use donated CC0 presets. Voices transformed into synthetic character dialogue. https://huggingface.co/kyutai/pocket-tts | https://huggingface.co/kyutai/tts-voices | https://creativecommons.org/licenses/by/4.0/ . Original AI HOUSE artwork, scripts, synthesized music and effects.'
def pack(n):
 ep=f'2{n:02}';out=ROOT/'output'/ep;dst=ROOT/'output'/'deliverables';dst.mkdir(exist_ok=True)
 story=json.loads((ROOT/'episodes'/f'{ep}.json').read_text())
 meta=dict(title=story['title'],description=story['description']+'\n\n'+ATTRIBUTION,tags=['AI HOUSE','animated comedy','dinosaur','Max','Luna','Zig','interactive story','cartoon shorts',story['scenes'][0]['theme']],review_status='Technical checks passed only when matching qa.json says PASS; listening/creative review pending',publishing_approved=False)
 (dst/f'AI_HOUSE_EP{n:02}_UPLOAD.txt').write_text('TITLE\n'+meta['title']+'\n\nDESCRIPTION\n'+meta['description']+'\n\nTAGS\n'+', '.join(meta['tags'])+'\n')
 (dst/f'AI_HOUSE_EP{n:02}_METADATA.json').write_text(json.dumps(meta,indent=2))
 im=Image.new('RGB',(1280,720),'#24354c');d=Canvas(im)
 d.oval((285,-100,625,350),'#39516b');d.box((20,20,180,49),'#ffe080',8);d.text('AI HOUSE 2.0',100,35,18)
 d.text(CAPTIONS[n-1],25,90,30,'#fff4df',anchor='lm')
 actor(d,'Max',110,188,1,'round',.8,.53,'worried',True)
 actor(d,'Luna',220,195,1,'wide',.8,.48,'worried',True)
 dinosaur(d,385,225,1)
 d.box((325,35,510,72),'#ffe080',9);d.text(f'EPISODE {n:02}',417,54,19)
 im.save(dst/f'AI_HOUSE_EP{n:02}_THUMBNAIL.png')
 src=out/f'episode_{ep}.mp4'
 if src.exists():
  qa=json.loads((out/'qa.json').read_text());assert qa.get('extended_technical_gate')=='PASS'
  shutil.copy2(src,dst/f'AI_HOUSE_EP{n:02}_FINAL.mp4')
  shutil.copy2(out/'qa.json',dst/f'AI_HOUSE_EP{n:02}_QA.json')
  shutil.copy2(out/'captions.srt',dst/f'AI_HOUSE_EP{n:02}_CAPTIONS.srt')
if __name__=='__main__':
 for n in range(1,11):pack(n)
