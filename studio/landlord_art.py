"""Shot-specific Week 2 props; uses the established room and character drawings."""
import math

KINDS={'thermostat','deposit','pets','meter','inspection','ceiling'}

def stage(d,scene,t,duration,who,mouth,energy,actor,dinosaur,INK,CREAM):
    kind=scene['visual'];phase=scene.get('phase','shock');payoff=phase=='payoff'
    for person,x in [('Luna',100),('Max',237),('Zig',375)]:
        actor(d,person,x,525,t,mouth if person==who else 'rest',energy if person==who else 0,.68,'worried',person==who)
    dinosaur(d,423,647,t)
    # The action stage is above the cast, keeping props and subtitles away from faces.
    d.box((42,178,488,400),'#f7e5d2',16,INK,2)
    if kind=='thermostat':
        d.box((75,210,212,362),CREAM,14,INK,3)
        d.box((90,228,197,285),INK,7);d.text('16 C',144,256,26,'#8ce5d4')
        d.box((106,301,180,341),'#53677b',5);d.line([(117,312),(170,312)],INK,5)
        d.text('TAP TO HEAT',144,380,12)
        if phase in ('escalate','payoff'):
            d.oval((325,218,402,295),'#ffd16f',INK,2)
            for j in range(8):
                a=j*math.pi/4;d.line([(363+47*math.cos(a),257+47*math.sin(a)),(363+58*math.cos(a),257+58*math.sin(a))],'#e9aa48',4)
        else:
            for j in range(3):
                x=296+j*51;y=260+math.sin(t*5+j)*9
                d.line([(x-12,y),(x+12,y)],'#80bcd0',3);d.line([(x,y-12),(x,y+12)],'#80bcd0',3)
        if payoff:
            d.box((277,316,466,383),CREAM,5,INK);d.text('SUN: OVERDUE',371,338,15,'#bf5c4d');d.text('$900',371,365,22)
        else:d.text('WARMTH: EXTRA',353,360,16)
    elif kind=='deposit':
        d.box((75,270,250,370),'#9fc6bc',12,INK);d.text('DEPOSIT',162,343,18)
        for j in range(8):
            x=95+(j%4)*38;y=245+(j//4)*24
            d.oval((x,y,x+29,y+29),'#f0c66f',INK);d.text('$',x+14,y+14,15)
        d.text('LAUNDRY FUND',162,207,15)
        if phase in ('escalate','payoff'):
            d.oval((331,242,417,328),'#f0c66f',INK,3);d.text('$',373,284,37)
            for j in range(3):d.oval((393+j*4,246+j*19,424+j*4,272+j*19),'#f7e5d2')
            d.text('RECEIPT' if payoff else 'QUALITY CHECK',375,365,17)
        else:
            d.text('ALL OUR',365,265,21);d.text('SAVINGS',365,301,21)
    elif kind=='pets':
        if phase=='shock':
            d.text('NO PETS ALLOWED',265,250,27,'#bf5c4d');d.text('SIGNED: DINO',265,310,18)
        else:
            for i,name in enumerate(('LUNA','MAX','ZIG')):
                x=95+i*145;d.oval((x-24,220,x+65,278),'#d9887e',INK,3)
                d.box((x-11,269,x+54,301),'#f0c66f',6,INK);d.text(name,x+21,285,14)
            d.text('REGISTERED HOUSE PETS',265,335,20)
            if payoff:d.text('DINO: SUPPORT LANDLORD',265,376,17,'#bf5c4d')
    elif kind=='meter':
        d.line([(89,202),(196,202),(196,260)],'#617887',16)
        fixed=phase!='shock';d.box((173,238,219,257),'#e1b569' if fixed else '#617887',4)
        for j in range(3):
            if fixed and not payoff:continue
            y=272+(t*80+j*31)%72;d.oval((188,y,202,y+17),'#a2d7ea' if not payoff else '#ddd1bc')
        d.box((116,350,276,380),'#c88d75',15,INK);d.text('SNACKS',196,367,14)
        if phase in ('escalate','payoff'):
            d.box((300,222,457,362),INK,14);d.text('WATER METER',378,245,14,CREAM)
            d.text('$'+str(10+int(t*4)),378,288,32,'#8ce5d4');d.text('DROPS SAVED' if payoff else 'PREMIUM',378,334,14,CREAM)
        else:d.text('REPAIRED' if fixed else 'LEAK!',367,292,24,'#bf5c4d')
    elif kind=='inspection':
        d.box((79,201,256,382),'#b88668',8,INK,3)
        d.box((92,216,241,366),'#544959',5)
        for j in range(12):
            x=99+(j*29)%117;y=242+(j*23)%108
            d.box((x,y,x+31,y+18),['#dfb7ff','#edb775','#8ce5d4'][j%3],5,INK,1)
        if phase in ('explain','escalate'):d.line([(250,217),(270+math.sin(t*8)*5,360)],'#c49b78',12)
        if phase=='escalate':
            d.line([(290,206),(290,382)],'#edb775',7)
            for j in range(9):d.line([(285,217+j*18),(300,217+j*18)],INK,2)
        d.text('STUDIO' if payoff else 'INSPECTION',374,251,22)
        d.text('TO LET' if payoff else 'TODAY',374,290,22)
        if payoff:d.text('DEPOSIT: $900',374,347,17,'#bf5c4d')
    elif kind=='ceiling':
        d.line([(72,218),(462,218)],'#81584f',9)
        for x in (110,245,380):
            d.line([(x,219),(x,283)],INK,7);d.line([(x+53,219),(x+53,283)],INK,7)
            d.box((x-12,278,x+65,302),'#597681',8,INK);d.line([(x-8,301),(x-8,337)],INK,6)
        if payoff:
            d.oval((387,245,417,273),'#8ed3a8',INK);d.oval((385,235,417,251),'#a3dfb4',INK)
            d.oval((394,239,398,243),INK);d.text('DINO: GRAVITY INCLUDED',265,374,17)
        else:d.text('FREE SEATS / GRAVITY EXTRA',265,374,16,'#bf5c4d')
