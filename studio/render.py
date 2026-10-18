"""AI HOUSE proof-of-concept. Not approved for automatic YouTube upload."""
import json, math, os, subprocess, tempfile, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from kokoro import KPipeline
ROOT=Path(__file__).resolve().parents[1]
story=json.loads((ROOT/'episodes/001.json').read_text())
OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
W,H=1080,1920
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def ff(*args):
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
def label(draw,txt,xy,size=56,color='white',heavy=True):
    draw.text(xy,txt,font=ImageFont.truetype(bold if heavy else font,size),fill=color,stroke_width=2,stroke_fill='#182032')
def character(draw,who,x,y,openmouth=False,blink=False):
    colors={'Max':'#f0ac6c','Zig':'#82d9ec','Luna':'#bb8de8'}
    c=colors[who]
    draw.rounded_rectangle((x-125,y+185,x+125,y+550),radius=80,fill=c)
    if who=='Zig':
        draw.rounded_rectangle((x-140,y-90,x+140,y+235),radius=75,fill=c,outline='#263750',width=12)
        draw.ellipse((x-75,y+15,x-30,y+65),fill='#192b3c')
        draw.ellipse((x+30,y+15,x+75,y+65),fill='#192b3c')
        draw.line((x,y-90,x,y-165),fill=c,width=12)
        draw.ellipse((x-18,y-185,x+18,y-149),fill='#fff1a0')
    else:
        draw.ellipse((x-135,y-95,x+135,y+235),fill=c,outline='#493b59',width=9)
        if who=='Luna':
            draw.ellipse((x-130,y-185,x-75,y-35),fill=c)
            draw.ellipse((x+75,y-185,x+130,y-35),fill=c)
        if not blink:
            draw.ellipse((x-75,y+15,x-25,y+73),fill='white')
            draw.ellipse((x+25,y+15,x+75,y+73),fill='white')
            draw.ellipse((x-55,y+30,x-36,y+60),fill='#18283d')
            draw.ellipse((x+45,y+30,x+64,y+60),fill='#18283d')
        else:
            draw.line((x-75,y+48,x-25,y+48),fill='#192b3c',width=7)
            draw.line((x+25,y+48,x+75,y+48),fill='#192b3c',width=7)
    draw.ellipse((x-24,y+118,x+24,y+(175 if openmouth else 130)),fill='#41283b')
def frame(scene,t,spoken=False):
    im=Image.new('RGB',(W,H),'#18233a');d=ImageDraw.Draw(im)
    d.rectangle((0,0,W,1100),fill='#283d5d')
    d.rectangle((0,1080,W,H),fill='#735b77')
    d.rectangle((70,190,490,700),fill='#27334f',outline='#e0a9a1',width=18)
    d.ellipse((160,260,400,510),fill='#f4ca84')
    d.rounded_rectangle((80,1120,1000,1530),radius=38,fill='#b88a8b')
    d.rectangle((80,1530,1000,1580),fill='#5c405c')
    i=scene
    if i==0:
        character(d,'Luna',540,650,spoken)
        label(d,'RENT: $0', (320,1500),74,'#ffe3a2')
    elif i==1:
        character(d,'Max',530,650,spoken)
        d.ellipse((350,1430,720,1770),fill='#76e6be',outline='#e2fff4',width=22)
    elif i==2:
        character(d,'Zig',520,640,spoken)
        label(d,'UNKNOWN SPECIES', (175,1520),55,'#f8c7a8')
    elif i==3:
        character(d,'Max',310,650,spoken)
        d.ellipse((570,1310,920,1690),fill='#84e8b5')
        d.polygon([(580,1440),(660,1300),(700,1440)],fill='#71bb8d')
        label(d,'CRACK!',(580,1180),76,'#fff1a1')
    elif i==4:
        character(d,'Zig',350,670,spoken)
        d.ellipse((710,1410,960,1620),fill='#e98542')
        d.polygon([(710,1470),(850,1120),(960,1470)],fill='#f5b55b')
    else:
        character(d,'Luna',540,660,spoken)
        d.rounded_rectangle((120,1450,960,1760),radius=45,fill='#17293d')
        label(d,'A: KEEP HIM', (215,1500),67,'#a3f0d2')
        label(d,'B: SELL HIM', (215,1620),67,'#ffd5a6')
    label(d,'AI HOUSE', (345,55),70,'#fff0c5')
    label(d,'EPISODE 01', (380,1800),48,'#fff0c5')
    return im
def speech(pipeline,line,voice,out):
    pieces=[]
    for _,_,audio in pipeline(line,voice=voice,speed=1.06):
        pieces.append(np.asarray(audio,dtype=np.float32))
    if not pieces: raise RuntimeError('TTS returned no audio')
    data=np.concatenate(pieces)
    import soundfile as sf
    sf.write(out,data,24000)
    return len(data)/24000
def main():
    pipeline=KPipeline(lang_code='a')
    voices={'Luna':'af_heart','Max':'am_michael','Zig':'am_fenrir'}
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        clips=[]
        for i,s in enumerate(story['scenes']):
            line=s['line'];speaker=s['speaker']
            audio=tmp/f'{i}.wav'
            speech(pipeline,line,voices[speaker],audio)
            # Allocate scene at least enough time for its full spoken line.
            import soundfile as sf
            snd,sr=sf.read(audio)
            duration=max(5.0,len(snd)/sr+1.1)
            image=tmp/f'{i}.png'
            frame(i,0,True).save(image)
            vid=tmp/f'{i}.mp4'
            # Subtle zoom; audio begins at 0.4s. Retain every spoken line.
            vf=f"scale=1160:2060,crop=1080:1920:x='40+12*sin(t/2)':y='70+10*sin(t/3)',format=yuv420p"
            ff('-loop','1','-framerate','30','-i',image,'-i',audio,
               '-filter_complex',f'[0:v]{vf}[v];[1:a]adelay=400|400,apad,volume=1.5[a]',
               '-map','[v]','-map','[a]','-t',duration,
               '-c:v','libx264','-preset','veryfast','-crf','21','-r','30',
               '-c:a','aac','-b:a','192k','-ar','48000',vid)
            clips.append(vid)
        concat=tmp/'concat.txt'
        concat.write_text(''.join("file '"+str(clip)+"'"+chr(10) for clip in clips))
        if len(clips)!=len(story['scenes']) or any(not clip.exists() or clip.stat().st_size==0 for clip in clips):
            raise RuntimeError('Missing or empty rendered scene before assembly')
        ff('-f','concat','-safe','0','-i',concat,'-c','copy',OUT/'episode_001.mp4')
    print('Rendered',OUT/'episode_001.mp4')
if __name__=='__main__':main()
