"""Original AI HOUSE vector-style art, drawn at output resolution; no external assets."""
import math
from landlord_art import KINDS, stage
from finale_art import KINDS as FINALE, stage as finale_stage
from earnings_art import KINDS as EARNINGS, stage as earnings_stage
from v2_art import stage as v2_stage
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont
INK='#232438'; CREAM='#fff4df'; COLORS={'Luna':'#8ce5d4','Max':'#ffbb8b','Zig':'#dfb7ff'}
@lru_cache(maxsize=64)
def font(size): return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',size)
class Canvas:
    def __init__(self,im): self.d=ImageDraw.Draw(im); self.k=im.width/540
    def xy(self,p): return tuple(round(x*self.k) for x in p)
    def shape(self,name,p,fill,outline=None,width=2,**kw):
        kw={k:round(v*self.k) if k=='radius' else v for k,v in kw.items()}
        getattr(self.d,name)(self.xy(p),fill=fill,outline=outline,width=max(1,round(width*self.k)),**kw)
    def box(self,p,c,r=0,outline=None,w=2): self.shape('rounded_rectangle',p,c,outline,w,radius=r)
    def oval(self,p,c,outline=None,w=2): self.shape('ellipse',p,c,outline,w)
    def poly(self,p,c): self.d.polygon([self.xy(q) for q in p],fill=c)
    def line(self,p,c,w=2): self.d.line([self.xy(q) for q in p],fill=c,width=max(1,round(w*self.k)),joint='curve')
    def text(self,s,x,y,size=20,c=INK,anchor='mm'):
        self.d.text(self.xy((x,y)),s,font=font(round(size*self.k)),fill=c,anchor=anchor)
@lru_cache(maxsize=4)
def room(width):
    im=Image.new('RGB',(width,round(width*16/9)),CREAM);d=Canvas(im)
    d.box((0,0,540,640),'#e8c9b5');d.box((0,0,540,200),'#f2d8be')
    d.box((0,620,540,960),'#bc8c83');d.line([(0,621),(540,621)],'#9c6e6f',5)
    for y in (680,760,865):d.line([(0,y),(540,y)],'#aa7d7c',2)
    d.box((302,178,498,452),INK,18);d.box((314,190,486,440),'#33445d',10)
    d.oval((402,211,451,260),'#ffe8b4')
    for i in range(15):
        x=324+(i*47)%149;y=205+(i*31)%210;d.oval((x,y,x+2,y+2),'#b5c5d4')
    for x,h in [(320,80),(350,60),(387,110),(430,70),(461,130)]:
        d.box((x,440-h,x+23,440),'#24344c',2)
        for yy in range(450-h,429,18):d.box((x+6,yy,x+10,yy+6),'#e7b275')
    d.line([(399,190),(399,440)],INK,6);d.line([(314,316),(486,316)],INK,6)
    d.box((57,204,202,355),'#a87061',7);d.box((66,213,193,346),CREAM,2)
    d.oval((91,229,170,308),'#ed9976');d.poly([(75,334),(123,263),(179,334)],'#667d75')
    d.line([(30,492),(171,492)],'#81584f',9)
    for x,h,c in [(47,42,'#d47c6b'),(66,54,'#687d83'),(88,36,'#e4b564')]:d.box((x,488-h,x+13,487),c,2)
    d.box((113,456,144,488),'#edbe89',5);d.oval((112,420,130,466),'#607c66');d.oval((130,414,149,461),'#738d71')
    d.box((60,533,482,686),'#374c58',28,INK,3);d.box((74,550,266,648),'#4d6870',18);d.box((276,550,467,648),'#4d6870',18)
    d.box((46,617,492,706),'#4c6470',18,INK,3);d.box((38,578,90,702),'#597681',15,INK,3);d.box((454,578,505,702),'#597681',15,INK,3)
    d.line([(84,707),(80,726)],INK,9);d.line([(463,707),(470,726)],INK,9)
    d.oval((35,706,513,783),'#d9aaa0');d.oval((75,717,481,767),'#e8bbae')
    return im

def actor(d,who,x,y,t,mouth='rest',energy=0,scale=1,emotion='neutral',gesture=False):
    # Local coordinates make the same character reusable in all shots.
    bob=math.sin(t*2.8)*2; y+=bob
    def p(a):return (x+a[0]*scale,y+a[1]*scale)
    def box(a,c,r=0,o=INK,w=2):d.box((*p(a[:2]),*p(a[2:])),c,r*scale,o,w*scale)
    def oval(a,c,o=None,w=2):d.oval((*p(a[:2]),*p(a[2:])),c,o,w*scale)
    def poly(a,c):d.poly([p(q) for q in a],c)
    def line(a,c=INK,w=2):d.line([p(q) for q in a],c,w*scale)
    skin=COLORS[who]; blink=(t+{'Max':0,'Luna':1.1,'Zig':2.3}[who])%3.8<.13
    oval((-76,188,76,210),'#987d81')
    if who=='Zig':
        line([(-26,141),(-30,181)],INK,15);line([(26,141),(30,181)],INK,15)
        box((-50,177,-12,194),'#77728e',8);box((12,177,50,194),'#77728e',8)
        box((-59,44,59,151),skin,19);box((-42,62,42,130),'#b999d4',10)
        oval((-14,81,14,109),'#f2e3ff',INK);d.text('Z',*p((0,95)),size=15*scale)
        line([(-55,68),(-78,97),(-71,126)],'#a68abd',12);oval((-83,115,-60,140),skin,INK)
        hand=(90,123-84*gesture);line([(55,69),(78,90),hand],'#a68abd',12);oval((hand[0]-11,hand[1]-10,hand[0]+11,hand[1]+11),skin,INK)
        box((-70,-93,70,40),skin,23);box((-59,-80,59,24),INK,18)
        line([(0,-93),(0,-118)],INK,4);oval((-9,-132,9,-114),'#ffce74',INK)
        box((-83,-47,-69,-8),'#a78bbb',5);box((69,-47,83,-8),'#a78bbb',5)
        for ex in (-28,28):
            if blink:line([(ex-12,-27),(ex+12,-27)],'#8ce5d4',4)
            else:box((ex-12,-44,ex+12,-18),'#8ce5d4',7,None)
    else:
        trouser='#273447' if who=='Max' else '#303d4d';shirt='#ed865a' if who=='Max' else '#486276'
        box((-46,126,-7,182),trouser,9);box((7,126,46,182),trouser,9)
        box((-55,174,-6,195),CREAM,9);box((7,174,56,195),CREAM,9)
        box((-60,34,60,139),shirt,23)
        line([(-51,55),(-77,91),(-62,126)],shirt,24);oval((-73,115,-48,139),skin,INK)
        hand=(91,112-97*gesture);line([(51,55),(78,76),hand],shirt,24);oval((hand[0]-12,hand[1]-12,hand[0]+12,hand[1]+12),skin,INK)
        if who=='Max':
            line([(-30,43),(0,61),(30,43)],'#f5b18c',6);line([(-12,54),(-14,86)],CREAM,2);line([(12,54),(14,86)],CREAM,2)
            box((-31,96,31,122),'#d6714d',8,None)
        else:
            poly([(-43,38),(0,75),(42,38)],'#d7e8e2');oval((-7,64,7,78),'#ffc76e',INK)
        box((-17,13,17,47),skin,9)
        if who=='Luna':
            oval((-67,-113,67,41),'#303342',INK);poly([(-53,-40),(-94,-66),(-71,-8),(-49,3)],skin);poly([(53,-40),(94,-66),(71,-8),(49,3)],skin)
        else:
            oval((-72,-44,-47,-5),skin,INK);oval((47,-44,72,-5),skin,INK)
        oval((-58,-98,58,35),skin,INK,3)
        if who=='Max':
            poly([(-59,-36),(-66,-87),(-47,-113),(-14,-108),(3,-126),(26,-105),(50,-107),(67,-73),(53,-42),(39,-76),(1,-67),(-29,-84),(-43,-49)],'#513c40')
            line([(-37,-95),(-16,-89),(5,-105)],'#735047',4)
        else:
            poly([(-57,-42),(-65,-91),(-35,-118),(8,-125),(47,-107),(61,-71),(24,-93),(-20,-72),(-47,-73)],'#3e405a')
            line([(-39,-97),(-8,-109),(23,-105)],'#74708f',5)
        for ex in (-25,25):
            if blink:line([(ex-13,-30),(ex+13,-30)],INK,3)
            else:
                oval((ex-13,-46,ex+13,-19),CREAM,INK,1);oval((ex-4,-40,ex+6,-21),INK);oval((ex-2,-37,ex+1,-33),'white')
            tilt=5 if emotion=='worried' else (-4 if who=='Luna' else 0)
            line([(ex-14,-53+(tilt if ex<0 else -tilt)),(ex+13,-55)],INK,3)
        line([(-2,-21),(-5,-10),(3,-8)],'#bc8e8a',2)
        oval((-47,-14,-27,-3),'#e99d91');oval((27,-14,47,-3),'#e99d91')
    my=7 if who!='Zig' else 2
    if mouth=='rest':line([(-12,my),(0,my+3),(13,my-1)],INK if who!='Zig' else '#8ce5d4',3)
    elif mouth=='closed':line([(-13,my),(13,my)],INK if who!='Zig' else '#8ce5d4',4)
    else:
        mw=8 if mouth=='round' else 19;mh=5+min(12,energy*17)
        oval((-mw,my-4,mw,my+mh),INK if who!='Zig' else '#8ce5d4')
        if who!='Zig':
            if mouth!='round':box((-mw+3,my-3,mw-3,my+1),CREAM,1,None)
            oval((-7,my+mh-5,8,my+mh-1),'#e68590')

def egg(d,x,y,t,cracked=False):
    sway=math.sin(t*18)*3 if cracked else math.sin(t*3)*2
    d.oval((x-54+sway,y-81,x+54+sway,y+53),'#9ee6c8',INK,3)
    d.oval((x-35+sway,y-62,x-15+sway,y-28),'#e2f8dd')
    for a,b in [(20,-39),(-22,3),(23,22)]:d.oval((x+a-8,y+b-9,x+a+8,y+b+9),'#65b7a2')
    if cracked:d.line([(x-29,y-50),(x+3,y-24),(x-13,y-8),(x+19,y+15),(x-2,y+38)],INK,4)
def dinosaur(d,x,y,t,fire=False):
    y+=math.sin(t*6)*4
    d.poly([(x+25,y+20),(x+91,y+32),(x+58,y-9)],'#71bb99')
    d.oval((x-33,y-9,x+39,y+64),'#7ac5a0',INK,3);d.oval((x-16,y+8,x+22,y+58),'#e6ecc4')
    for a in (-19,21):d.oval((x+a-15,y+48,x+a+13,y+67),'#79b58e',INK)
    d.oval((x-49,y-70,x+34,y+7),'#8ed3a8',INK,3);d.oval((x-61,y-39,x+8,y+5),'#a3dfb4',INK,2)
    for a in (0,18,33):d.poly([(x+a,y-65),(x+a+4,y-87),(x+a+15,y-63)],'#edb775')
    d.oval((x-20,y-54,x-4,y-32),INK);d.oval((x-18,y-51,x-13,y-45),CREAM)
    d.oval((x-48,y-23,x-43,y-18),INK)
    d.line([(x-53,y-8),(x-32,y-4),(x-13,y-10)],INK,2)
    if fire:
        flick=math.sin(t*40)*8
        d.poly([(x-53,y-14),(x-113,y-50+flick),(x-101,y-22),(x-174,y-16),(x-115,y+5),(x-130,y+26+flick),(x-53,y+2)],'#ef7953')
        d.poly([(x-54,y-12),(x-110,y-22),(x-94,y-8),(x-144,y-4),(x-99,y+9),(x-54,y+1)],'#ffcf72')

def render(scene,index,t,duration,who,mouth,energy,caption,episode=1,width=1080):
    im=room(width).copy();d=Canvas(im);kind=scene.get('visual',['rent','egg','scan','hatch','fire','vote'][min(index,5)])
    # Story action and staging change between shots, not just camera movement.
    burned=kind not in KINDS|EARNINGS|FINALE|{'couch_rent','v2'} and (episode>1 or (episode==1 and index>=5) or (kind=='fire' and t>1.7))
    if burned:
        d.box((35,530,508,620),'#e8c9b5');d.box((35,620,508,727),'#bc8c83')
        d.line([(35,621),(508,621)],'#9c6e6f',5)
        d.oval((62,660,482,723),'#665c68')
        d.line([(91,687),(211,665),(330,701),(443,681)],'#4f4959',7)
        if kind=='fire' and t>1.7:
            for j in range(5):
                yy=640-(t*22+j*33)%140;xx=110+j*65;d.oval((xx,yy,xx+21,yy+28),'#a89498')
    hero_x=185 if kind in ('egg','scan','hatch','fire') else 270
    if kind=='v2':
        v2_stage(d,scene,t,duration,who,mouth,energy,actor,dinosaur,egg,INK,CREAM)
    elif kind in FINALE:
        finale_stage(d,scene,t,duration,who,mouth,energy,actor,dinosaur,INK,CREAM)
    elif kind in EARNINGS:
        earnings_stage(d,scene,t,duration,who,mouth,energy,actor,dinosaur,egg,INK,CREAM)
    elif kind in KINDS:
        stage(d,scene,t,duration,who,mouth,energy,actor,dinosaur,INK,CREAM)
    elif kind=='couch_rent':
        phase=scene.get('phase','invoice')
        if phase=='eviction' and t>1.1:
            # Move the existing couch artwork away, preserving its approved design.
            k=width/540;crop=room(width).crop(tuple(round(v*k) for v in (35,530,510,727)))
            d.box((35,530,510,620),'#e8c9b5');d.box((35,620,510,727),'#bc8c83')
            d.line([(35,621),(510,621)],'#9c6e6f',5)
            im.paste(crop,(round((35+min(550,(t-1.1)*370))*k),round(530*k)))
            d=Canvas(im)
        for person,x in [('Luna',105),('Max',240),('Zig',370)]:
            actor(d,person,x,505,t,mouth if person==who else 'rest',energy if person==who else 0,.76,'worried',person==who)
        dinosaur(d,426,655,t,False)
        sign='RENT DUE: $900' if phase in ('invoice','owner') else 'NO EATING THE ASSETS' if phase=='warning' else 'COUCH: EVICTED!'
        d.box((42,185,478,243),INK,12);d.text(sign,260,214,21,'#ffe078')
        if phase=='owner':
            d.box((355,565,484,600),CREAM,6,INK);d.text('LANDLORD',419,582,13)
        if phase=='eviction':
            d.box((350,565,485,605),CREAM,6,INK);d.text('EVICTED',417,585,17,'#bf5c4d')
    else:
        actor(d,who,hero_x,430,t,mouth,energy,1.4,'worried' if kind=='rent' else 'neutral',(.5+.5*math.sin(t*2)) if kind in ('egg','vote') else 0)
    if kind=='rent':
        d.box((318,551,432,615),CREAM,5,INK);d.line([(320,554),(375,589),(430,554)],'#b6a79a',2);d.text('RENT',375,602,12)
        d.box((73,235,267,291),INK,12);d.text('BALANCE: $0',170,263,19,'#ffd080')
    elif kind=='egg':egg(d,382,612,t)
    elif kind=='scan':
        
        if episode==1:egg(d,390,619,t)
        else:dinosaur(d,390,619,t)
        scan=565+(t*65)%105;d.line([(330,scan),(450,scan)],'#72e5db',3)
        d.box((261,249,498,302),INK,12);d.text(scene.get('scan_label','HEARTBEAT DETECTED'),380,276,15,'#96edd3')
    elif kind=='hatch':
        if t<1.2:egg(d,386,612,t,True)
        else:
            dinosaur(d,386,605,t)
            d.poly([(333,659),(345,640),(359,651),(373,637),(383,666)],'#c5f1db')
            d.poly([(407,667),(413,640),(428,652),(443,638),(445,670)],'#c5f1db')
    elif kind in ('fire','dino'):dinosaur(d,392,608,t,kind=='fire' and .65<t<1.8)
    elif kind=='vote':
        d.box((46,168,474,205),INK,12);d.text(scene.get('choice_a','A  KEEP HIM'),260,187,19,'#a2ead3')
        d.box((46,213,474,250),INK,12);d.text(scene.get('choice_b','B  SELL HIM'),260,232,19,'#ffc59a')
    elif kind in ('meeting','chomp'):
        d.box((266,405,519,683),'#273047',13,INK,3)
        d.box((278,428,507,647),'#b2e3f0',8)
        d.box((286,440,388,533),'#f8d6b3',6);d.text('MAX',338,454,12)
        d.box((397,440,500,533),'#e7b7c7',6);d.text('HR',448,454,12)
        d.box((286,543,500,632),'#c7edc7',6);d.text('DINO - MANAGER',393,555,12)
        dinosaur(d,390,615,t,False)
        if kind=='chomp':
            d.box((397,440,500,533),'#343446',6);d.text('SIGNAL LOST',449,485,10,'#ffffff')
            for j in range(5):d.line([(400,465+j*12),(498,460+j*12)],'#f3a5b5',2)
    elif kind=='bill':
        d.box((321,522,454,651),CREAM,8,INK);d.text(scene.get('prop_title','REPAIR BILL'),388,550,14);d.text(scene.get('prop_value','$900'),388,591,25,'#bf5c4d')
    if kind=='v2':
        zoom=1+.022*min(1,t/max(duration,.1))
        nw,nh=round(im.width*zoom),round(im.height*zoom)
        im=im.resize((nw,nh),Image.Resampling.BICUBIC).crop(((nw-width)//2,(nh-round(width*16/9))//2,(nw+width)//2,(nh+round(width*16/9))//2))
        d=Canvas(im)
    # Clean brand safe area; captions avoid Shorts bottom and right-hand UI.
    d.box((28,43,172,78),INK,11);d.text('AI HOUSE',100,61,20,CREAM)
    d.text(f'{episode:02d} / YOU DECIDE',474,61,11,INK,'rm')
    d.box((33,114,507,153),'#f7e5d2',10);d.text(scene.get('beat',kind.upper()),270,134,17)
    if caption:
        words=caption.split();lines=[];line=''
        for word in words:
            test=(line+' '+word).strip()
            if font(46).getlength(test)>800 and line:lines.append(line);line=word
            else:line=test
        if line:lines.append(line)
        lines=lines[:2];top=720
        d.box((36,top-12,472,top+len(lines)*29+12),INK,12)
        for j,line in enumerate(lines):
            d.text(line,254,top+14+j*29,23,'#fff4df')
            if kind=='v2':
                words=line.split();selected=next((w for w in words if any(c.isdigit() for c in w) or w.lower().strip('.,!?') in ('million','dinosaur','billion','earth','nobody','rent','fired','expired','delete','simulation')),None)
                if selected:
                    total=font(46).getlength(line)/2
                    before=line[:line.index(selected)]
                    center=254-total/2+font(46).getlength(before)/2+font(46).getlength(selected)/4
                    d.text(selected,center,top+14+j*29,23,'#ffe078')
    return im
