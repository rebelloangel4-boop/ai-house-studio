"""AI HOUSE 2.0 acting and story props, using the established character drawings."""
import math
from PIL import Image, ImageDraw

def stage(d,s,t,duration,who,mouth,energy,actor,dinosaur,egg,ink,cream):
 theme=s['theme'];phase=s['phase'];progress=min(1,t/max(.1,duration));W=d.k
 def sign(text,y=270,size=22,color='#ffe18b'):
  if close and y>=350:y=270
  if phase in ('float','fly'):y=180
  d.box((40,y-25,500,y+25),ink,12);d.text(text,270,y,size,color)
 def cash(x,y,gold=False):
  d.box((x-27,y-12,x+27,y+12),'#ffd46f' if gold else '#95e7b5',3,ink);d.text('$',x,y,15)
 def door(x,y,label='EXIT',open=False):
  d.box((x-47,y-100,x+47,y+90),ink,8);d.box((x-39,y-91,x+39,y+82),'#292b52' if open else '#bb7d68',5)
  d.text(label,x,y-68,13,cream);d.oval((x+25,y-8,x+32,y-1),'#ffd46f')
 def globe(x,y,r=63):
  d.oval((x-r,y-r,x+r,y+r),'#66bedf',ink,3)
  d.poly([(x-45,y-28),(x-9,y-48),(x+7,y-23),(x-8,y),(x+10,y+30),(x-5,y+48),(x-27,y+9)],'#89d09b')
  d.poly([(x+23,y-38),(x+50,y-15),(x+31,y+8),(x+14,y-9)],'#89d09b')
 def screen(label,value,color='#94ead1'):
  d.box((90,185,450,365),ink,18);d.box((103,199,437,349),'#263b50',10)
  d.text(label,270,235,17,cream);d.text(value,270,290,29,color)
 def button(x=270,y=405):
  d.oval((x-48,y-16,x+48,y+24),ink);d.oval((x-42,y-22,x+42,y+13),'#ff6c69',ink,3)
 def phone(x,y):
  d.box((x-32,y-52,x+32,y+52),ink,9);d.box((x-25,y-42,x+25,y+37),'#9cdfd2',4);d.text('$',x,y,26)
 def rocket(x,y):
  d.poly([(x-16,y+35),(x,y-48),(x+16,y+35)],cream);d.oval((x-8,y-12,x+8,y+5),'#77cbda',ink)
  d.poly([(x-12,y+33),(x,y+65+math.sin(t*30)*8),(x+12,y+33)],'#ffb866')
 # Cast blocking alternates wide ensemble, reaction, and close shots.
 close=phase in ('cash','phone','chase','shrug','confess','hope','relief','offended','wall','debt','history')
 if close:
  actor(d,who,180,470,t,mouth,energy,1.24,'worried' if phase in ('chase','debt','confess') else 'neutral',.5+.5*math.sin(t*4))
 else:
  for person,x in [('Luna',100),('Max',255),('Zig',410)]:
   speaking=person==who
   x+=math.sin(t*2.1+(0 if speaking else 2))* (4 if speaking else 1)
   yy=505
   if theme=='trial' and phase in ('float','fly'): yy-=70+math.sin(t*2+x)*32
   actor(d,person,x,yy,t+(0 if speaking else .7),mouth if speaking else 'rest',energy if speaking else 0,.78,'worried' if phase in ('door','alarm','error','countdown') else 'neutral',(.55+.4*math.sin(t*3)) if speaking else 0)
 dx=410;dy=650
 if phase=='choice':
  dinosaur(d,dx,dy,t)
  d.box((35,181,505,246),ink,12);d.text(s['choice_a'],270,213,19,'#a2ead3')
  d.box((35,260,505,325),ink,12);d.text(s['choice_b'],270,292,19,'#ffc59a')
  d.text('COMMENT YOUR CHOICE',270,382,18,ink)
  return
 if theme=='money':
  if phase in ('offer','cash'):
   screen('TRANSFER COMPLETE','$10,000,000')
   for j in range(11): cash(45+(j*73)%470,315+(t*105+j*53)%390)
  elif phase=='door':
   door(270,288)
   for j in range(6):d.poly([(232+j*13,301),(238+j*13,316+math.sin(t*8)*4),(245+j*13,301)],cream)
   sign('EXIT: LOCKED',397,21,'#ffad99')
  elif phase=='phone':phone(395,390);sign('DELIVERY ORDERED',253)
  elif phase=='invoice':screen('DELIVERY FEE','$9,900,000','#ffb99d')
  elif phase in ('eat','chase'):
   dx=310+math.sin(t*3)*60
   for j in range(5):cash(dx-110+((t*70+j*25)%90),dy-35)
   sign('RETIREMENT SALAD',258)
  elif phase=='reveal':
   screen('NEW OWNER','DINO');d.box((340,640,470,671),cream,6,ink);d.text('RENT: $10M',405,656,14)
 elif theme=='meteor':
  if phase=='alarm':screen('TIME UNTIL IMPACT','23:59:59','#ffb99d')
  elif phase=='grape':d.oval((375,340,412,377),'#bd85ce',ink,3)
  elif phase in ('button','bait','eat'):
   if phase!='eat':button(270,300)
   else:sign('REMOTE: SWALLOWED',270)
   if phase=='bait':d.oval((262,271,279,288),'#b67ad2',ink)
  else:
   globe(150,295)
   x=360-70*math.sin(t*1.5) if phase=='reverse' else 370
   d.oval((x-37,260,x+37,334),'#9d8c8f',ink,3)
   d.line([(x+30,277),(x+75,250)],'#ffb76b',12)
   sign('DRIVEWAY RESERVED' if phase=='crash' else 'PILOT: DINO',403)
 elif theme=='president':
  if phase in ('elected','law','badge'):screen('PRESIDENT OF EARTH',{'elected':'DINO WINS!','law':'NO BEDTIME','badge':'SNACK MINISTER'}[phase])
  elif phase in ('moon','rocket'):
   d.oval((215,210,325,320),'#ffe195',ink);rocket(370,350-(t*80)%120);sign('MOON = CHEESE?',400)
  else:
   for j in range(7):d.box((60+j*65,230+math.sin(t*3+j)*30,85+j*65,265+math.sin(t*3+j)*30),cream,2,ink)
 elif theme=='fired':
  if phase in ('fired','rent','report','error'):screen('HOUSE MANAGEMENT',{'fired':'YOU ARE FIRED','rent':'RENT DUE','report':'TOASTER: 100%','error':'RECALCULATING...'}[phase], '#ffb69c')
  elif phase=='reveal':screen('ZIG: NEW POSITION','DOORBELL');button(270,393)
  elif phase=='buy':screen('OWNER UPDATED','DINO, CEO')
  else:
   d.box((210,240,340,330),'#aeb8cf',20,ink,4);d.box((231,223,318,245),ink,6);d.poly([(228,330),(270,370),(320,330)],'#486276');d.text('LUNA?',275,285,18)
 elif theme=='future':
  if phase in ('portal','double','reveal'):
   for r in range(90,55,-8):d.oval((270-r,282-r,270+r,282+r),'#7d67a1' if r%2 else '#83d8d6')
   d.poly([(243,270),(202,405),(340,405),(290,270)],'#53345f')
   actor(d,'Max',270,290,t,'rest',0,.45)
  elif phase=='clones':
   for j in range(12):actor(d,'Max',65+(j%6)*81,235+(j//6)*100,t+j*.2,'rest',0,.27)
  else:
   screen('MAX / PRIVATE',{'debt':'BALANCE: -$50','history':'SEARCH HISTORY','laptop':'DO NOT OPEN','steal':'TIME MACHINE'} .get(phase,'ACCESS DENIED'))
 elif theme=='egg':
  if phase in ('gold','hatch','hope'):
   egg(d,270,300,t,phase=='hatch');sign('VALUATION: $1 BILLION',405,18)
   for j in range(6):d.text('+',180+j*34,190+math.sin(t*3+j)*20,23,'#ffce71')
  elif phase in ('baby','reveal'):
   dinosaur(d,270,300,t);d.poly([(265,315),(260,345),(270,351),(277,339),(271,315)],'#694780');sign('LEGAL COUNSEL',405)
  elif phase=='invoice':screen('HATCHING FEE','$2,000,000,000','#ffad99')
  else:d.oval((180,270,370,350),'#a2dce5',ink,3);d.text('LUXURY YACHT',275,310,16)
 elif theme=='timer':
  if phase=='countdown':screen('TIME REMAINING',f'09:{59-int(t):02}', '#ffb89a')
  elif phase=='laundry':
   for j in range(4):d.box((180+j*12,250+j*21,350+j*12,280+j*21),['#96d5c7','#f2b092'][j%2],10,ink)
  elif phase in ('medicine','confess'):screen('DINO MEDICINE','DO NOT EAT', '#ffb89a')
  elif phase in ('tail','reveal'):
   d.poly([(280,603),(364,587+math.sin(t*6)*8),(335,636),(283,631)],'#88c9a3');sign('MAX: UPDATING...',275)
  else:screen('FREE ELECTRICITY','TRIAL ENDING')
 elif theme=='trial':
  if phase in ('expired','ad','pay'):screen('EARTH PREMIUM',{'expired':'TRIAL EXPIRED','ad':'SKIP: UNAVAILABLE','pay':'ADD PAYMENT'}[phase], '#ffb69c')
  elif phase=='card':phone(270,290);sign('PAYMENT ACCEPTED',405)
  else:globe(270,280,81);sign('OWNER: DINO' if phase in ('owned','reveal') else 'GRAVITY: OFF',405)
 elif theme=='doors':
  if phase in ('hall','rich','control','delete'):
   for j in range(4):door(77+j*129,290,str(1+j if phase in ('hall','rich') else 96+j),True)
   if phase=='delete':d.box((310,240,500,380),'#25233d');d.text('DELETED',405,307,22,'#ffb7b0')
  elif phase in ('dinos','offended'):
   for j in range(3):dinosaur(d,110+j*157,280,t+j)
  elif phase=='baby':dinosaur(d,270,280,t);phone(370,310)
  else:screen('MULTIVERSE DEBT','$50')
 elif theme=='simulation':
  if phase in ('tear','wall','grid','error'):
   d.poly([(200,190),(350,215),(320,270),(370,330),(210,370),(241,290)],'#172b3c')
   for j in range(6):d.line([(210,220+j*22),(335,220+j*22)],'#5ce8b4',1)
   if phase=='error':sign('IMAGINATION: INSUFFICIENT',407,17)
  elif phase in ('screen','potato','battery'):
   screen('SIMULATION HOST','BATTERY: 1%' if phase=='battery' else '')
   if phase!='battery':d.oval((224,270,316,320),'#b18b61',ink,3);dinosaur(d,406,320,t)
  else:cash(270,285,True);sign('MONEY CHEAT DENIED',405)
 dinosaur(d,dx,dy,t)
 if phase=='choice':
  # Keep ending choices separated from subtitles and player controls.
  d.box((35,181,505,246),ink,12);d.text(s['choice_a'],270,213,19,'#a2ead3')
  d.box((35,260,505,325),ink,12);d.text(s['choice_b'],270,292,19,'#ffc59a')
  d.text('COMMENT YOUR CHOICE',270,382,18,ink)
