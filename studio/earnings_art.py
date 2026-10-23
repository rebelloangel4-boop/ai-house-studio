"""Original Week 3 action props, drawn with the established AI HOUSE palette."""
import math
KINDS={'daycare','translator','pizza','influencer','snacks','clone','accountant'}

def stage(d,scene,t,duration,who,mouth,energy,actor,dinosaur,egg,INK,CREAM):
    kind=scene['visual'];phase=scene.get('phase','shock');end=phase=='payoff'
    for person,x in [('Luna',100),('Max',237),('Zig',375)]:
        actor(d,person,x,525,t,mouth if person==who else 'rest',energy if person==who else 0,.68,'worried',person==who)
    dinosaur(d,423,647,t)
    d.box((42,178,488,400),'#f7e5d2',16,INK,2)
    def label(s,y=375,size=16):d.text(s,265,y,size)
    def mini_egg(x,y,cracked=False):
        sway=math.sin(t*7+x)*2
        d.oval((x-21+sway,y-31,x+21+sway,y+28),'#9ee6c8',INK,2)
        d.oval((x-12,y-18,x-5,y-7),'#e2f8dd')
        if cracked:d.line([(x-14,y-20),(x+6,y-5),(x-5,y+6),(x+10,y+20)],INK,2)
    def tiny_dino(x,y):
        d.oval((x-21,y-18,x+23,y+24),'#8ed3a8',INK,2)
        d.oval((x-29,y-13,x+10,y+8),'#a3dfb4',INK,2)
        d.oval((x-9,y-11,x-4,y-5),INK)
        d.poly([(x+15,y+13),(x+39,y+23),(x+23,y)],'#71bb99')
    if kind=='daycare':
        d.box((80,277,446,346),'#597681',14,INK,3)
        if phase in ('shock','explain'):
            for x in (145,265,385):mini_egg(x,270,phase=='explain')
            label('DINO DAYCARE / OPEN')
        else:
            for j,x in enumerate((135,265,395)):
                tiny_dino(x,244+math.sin(t*7+j)*5)
            d.box((163,299,365,336),'#dfb7ff',12,INK);d.text('MAX',265,316,19)
            if end:
                for j in range(3):d.text('Z',330+j*18,290-j*18-(t*10)%15,16,'#735b8a')
            label('NAP TIME: THE ADULT')
    elif kind=='translator':
        d.box((82,215,247,348),'#53677b',15,INK,3)
        d.box((97,232,231,298),INK,7);d.text('BURP' if phase=='explain' else 'ROAR',165,263,24,'#8ce5d4')
        d.oval((132,315,153,336),'#edb775');d.oval((174,315,195,336),'#edb775')
        d.line([(253,275),(284,275)],INK,5)
        d.poly([(283,263),(301,275),(283,287)],INK)
        y=217+min(t*15,25) if end else 235
        d.box((315,y,453,345),CREAM,4,INK,2)
        d.text('INVOICE' if end else 'PAYMENT',384,y+24,17,'#bf5c4d')
        d.text('EXPLANATION' if end else 'DINO FEE',384,y+52,12)
        d.text('$900',384,y+81,23)
        label('TRANSLATION: EXTRA')
    elif kind=='pizza':
        d.box((79,213,453,352),'#c79a72',8,INK,3)
        if phase in ('shock','explain'):
            for j in range(4):
                x=103+j*85;d.poly([(x,263),(x+64,263),(x+33,337)],'#f4c875')
                d.line([(x,263),(x+64,263)],'#bd7951',8)
                d.oval((x+23,281,x+38,296),'#bf5c4d')
                d.poly([(x+16,241),(x+16,218),(x+30,229),(x+40,216),(x+51,229),(x+59,218),(x+59,241)],'#edb775')
            label('A ROYALTY ON EVERY BITE')
        else:
            d.line([(102,300),(136,306),(159,298)],'#bd7951',8)
            if end:
                d.box((306,247,425,330),CREAM,4,INK);d.text('LUXURY',365,267,15);d.text('HOME',365,291,17);d.text('$900',365,314,16,'#bf5c4d')
            label('BOX RENTAL NOW AVAILABLE' if end else 'PROFIT: CRUST')
    elif kind=='influencer':
        d.box((116,258,348,333),'#597681',14,INK,3)
        d.box((131,243,333,299),'#4d6870',13,INK)
        if phase=='shock':
            d.box((139,257,221,298),'#8ba1a0',8);d.box((240,257,323,298),'#8ba1a0',8)
        d.oval((372,216,455,299),CREAM,INK,3);d.oval((382,226,445,289),'#f7e5d2',INK,2)
        d.line([(415,299),(415,352)],INK,5);d.line([(384,352),(446,352)],INK,5)
        d.box((398,241,430,283),'#53677b',5,INK)
        if end:
            d.box((149,262,318,310),CREAM,6,INK);d.text('FAMILY: FIRED',234,287,17,'#bf5c4d')
        label('SPONSORED SKINCARE' if phase=='explain' else 'THE COUCH HAS AN AGENT')
    elif kind=='snacks':
        d.box((72,207,243,351),'#617887',12,INK,3);d.box((86,223,229,335),CREAM,6)
        d.line([(93,263),(221,263)],'#617887',4);d.line([(93,301),(221,301)],'#617887',4)
        d.text('EMPTY',157,281,20,'#bf5c4d')
        if phase in ('shock','explain'):
            d.box((323,242,420,307),INK,8);d.oval((350,252,399,298),'#8ce5d4',INK,2)
            d.line([(370,308),(370,347)],INK,5)
        else:
            d.box((296,218,460,333),INK,9);d.text('SIGNAL LOST',378,274,17,CREAM)
        if end:
            d.box((284,344,466,386),'#edb775',5,INK);d.text('CRIME TOUR: $9',375,365,17)
        else:label('EMERGENCY SNACK SECURITY')
    elif kind=='clone':
        d.box((126,211,232,293),'#dfb7ff',15,INK,3);d.box((137,225,221,277),INK,9)
        for x in (151,191):d.box((x,241,x+18,256),'#8ce5d4',4)
        d.box((137,298,222,350),'#b999d4',10,INK)
        if phase in ('explain','escalate'):
            d.box((149,313,211,336),'#edb775',3,INK);d.text('BOSS',180,325,13)
        if end:
            d.box((301,222,451,334),'#c79a72',5,INK,3);d.text('MANAGER',376,253,18);d.text('CARDBOARD',376,290,15)
            d.line([(293,281),(250,281)],INK,4)
        else:
            d.text('CHORE',368,258,22);d.text('COMMISSION',368,293,18)
        label('PLEASE REPORT TO THE BADGE' if end else 'HELP HAS ARRIVED')
    elif kind=='accountant':
        if phase in ('shock','explain'):
            mini_egg(165,274,phase=='explain')
            d.box((252,225,437,337),CREAM,6,INK);d.text('INTERVIEW',345,253,21);d.text('CRACK!',345,296,25,'#bf5c4d')
        else:
            tiny_dino(159,269);d.poly([(157,289),(146,316),(168,316)],'#bf5c4d')
            d.box((279,220,449,347),CREAM,5,INK)
            d.text('DIGESTION' if end else 'LEDGER',364,249,18)
            d.text('FEE: $900' if end else 'EATEN',364,290,21,'#bf5c4d')
            d.text('PAY NOW',364,326,13)
        label('OUR NEW ACCOUNTANT')
