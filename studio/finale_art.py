"""Week 4 household-comedy actions using the established artwork and palette."""
import math
KINDS={'audit','ban','campaign','promise','debate','ballots','recount','house_vote','couch_boss'}

def stage(d,scene,t,duration,who,mouth,energy,actor,dinosaur,INK,CREAM):
    kind=scene['visual'];phase=scene.get('phase','shock');end=phase=='payoff'
    for person,x in [('Luna',100),('Max',237),('Zig',375)]:
        actor(d,person,x,525,t,mouth if person==who else 'rest',energy if person==who else 0,.68,'worried',person==who)
    dinosaur(d,423,647,t)
    d.box((42,178,488,400),'#f7e5d2',16,INK,2)
    def label(s):d.text(s,265,376,16)
    def invoice(x,y,title,amount):
        d.box((x,y,x+148,y+115),CREAM,5,INK,2);d.text(title,x+74,y+29,15);d.text(amount,x+74,y+75,23,'#bf5c4d')
    def couch(x,y,s=1):
        d.box((x,y,x+180*s,y+60*s),'#4d6870',12*s,INK,2)
        d.box((x-7*s,y+30*s,x+187*s,y+77*s),'#597681',10*s,INK,2)
        for xx in (x+15*s,x+160*s):d.line([(xx,y+77*s),(xx,y+89*s)],INK,5*s)
    def biscuit(x,y):
        d.oval((x-24,y-20,x+24,y+20),'#e9bd76',INK,2)
        for dx,dy in [(-9,-6),(9,-6),(0,8)]:d.oval((x+dx-2,y+dy-2,x+dx+2,y+dy+2),'#a8784a')
    def pizza(x,y):
        d.poly([(x-35,y-24),(x+35,y-24),(x,y+42)],'#f4c875');d.line([(x-35,y-24),(x+35,y-24)],'#bd7951',7)
        d.oval((x-12,y-5,x+4,y+11),'#bf5c4d')
    if kind=='audit':
        if end:
            for j in range(7):biscuit(95+j*19,300+math.sin(j)*10)
            d.text('EVIDENCE: EATEN',178,230,17)
        else:
            d.box((105,224,236,298),'#edb775',12,INK,3);d.box((96,281,245,325),'#d2a04d',10,INK)
            d.poly([(110,226),(110,202),(137,220),(170,197),(203,220),(234,202),(234,226)],'#edb775')
        invoice(300,220,'SNACK BUDGET','$900');label('REPLACEMENT REQUIRED' if end else 'ONE VERY LARGE BISCUIT')
    elif kind=='ban':
        d.box((82,222,240,333),'#8cbccb',12,INK,3);d.text('ACCOUNT',161,253,20);d.text('FROZEN',161,297,23,CREAM)
        d.box((295,266,449,340),'#b999d4',14,INK,3);d.line([(319,279),(426,279)],INK,5)
        y=235-abs(math.sin(t*4))*12 if end else 245
        d.box((329,y,414,y+51),'#e9bd76',10,INK);d.text('RENT' if end else 'BREAD',372,y+27,17)
        label('TOAST ACCEPTED' if end else 'THE MONEY PRINTER')
    elif kind=='campaign':
        d.box((82,208,247,347),CREAM,6,INK,2);d.text('LUNA',165,239,27,'#438d82');d.text('FAIRNESS',165,284,19)
        if phase in ('escalate','payoff'):
            d.box((284,208,451,347),'#b8ddbf',6,INK,2);d.text('DINO',368,239,27);d.text('LUNCH',368,284,24)
        if end:
            for j in range(5):d.oval((209+j*4,217+j*23,258+j*4,254+j*23),'#f7e5d2')
        label('POLICIES: ABSORBED' if end else 'THE HOUSE CAMPAIGN')
    elif kind=='promise':
        for x in (113,203):pizza(x,274)
        d.text('FREE!',160,217,27,'#bf5c4d')
        invoice(297,222,'READING FEE' if end else 'SMALL PRINT','$9' if end else 'BRING PIZZA')
        label('READING COSTS EXTRA' if end else 'THE PIZZA PROMISE')
    elif kind=='debate':
        for x in (86,309):d.box((x,270,x+131,347),'#617887',8,INK,2)
        if phase in ('shock','explain'):
            d.line([(265,337),(265,245)],INK,5);d.oval((250,219,280,265),'#b999d4',INK,2)
            d.text('WHERE IS DINNER?',265,195,16)
        else:
            d.oval((221,221,308,312),'#a3dfb4',INK,3)
            for j in range(3):
                x=317+j*14+math.sin(t*8)*3;d.line([(x,239-j*4),(x+8,264),(x,289+j*4)],'#bf5c4d',3)
            d.text('SNACKS!',265,331,23,'#bf5c4d')
        label('THE STOMACH HAS THE FLOOR')
    elif kind=='ballots':
        d.box((116,240,410,347),'#c79a72',10,INK,3);d.line([(175,251),(352,251)],INK,5)
        d.text('HOUSE BALLOTS',265,318,19)
        if phase in ('shock','explain'):
            for j in range(3):
                y=202+(t*27+j*13)%36;d.box((184+j*39,y,212+j*39,y+25),CREAM,2,INK);d.text('X',198+j*39,y+12,15)
        else:
            d.poly([(192,284),(329,284),(258,225)],'#e9bd76');d.line([(201,282),(319,282)],'#8eb783',6)
        label('INDEPENDENT: SANDWICH' if end else 'KEEP LUNCH SEPARATE')
    elif kind=='recount':
        if phase in ('shock','explain'):
            for j in range(5):
                x=100+j*73;d.poly([(x-22,309),(x-10,269),(x+16,257),(x+30,298),(x+9,320)],'#9297a1')
        else:
            for x in (130,230,330):biscuit(x,287)
            if end:
                d.box((390,235,450,330),CREAM,6,INK);d.text('MILK',420,282,13)
        label('BISCUITS + MILK' if end else 'EMERGENCY RECOUNT')
    elif kind=='house_vote':
        couch(174,249,1)
        for j,name in enumerate(('LUNA','MAX','ZIG','DINO')):
            x=100+j*109;d.text(name,x,210,14)
            if phase!='shock':d.line([(x,225),(265,252)],'#bf5c4d',3)
        label('OUR HOUSEHOLD CHOICE' if end else 'POINT AT A LEADER')
    elif kind=='couch_boss':
        couch(99,242,1.1)
        d.poly([(150,236),(150,205),(179,225),(200,201),(223,225),(248,205),(248,236)],'#edb775')
        if phase in ('escalate','payoff'):
            if end:
                couch(341,287,.5);d.text('LANDLORD',389,255,14)
            else:invoice(317,218,'SITTING RENT','$900')
        else:d.text('PRESIDENT',369,284,19)
        label('EVEN COUCHES PAY RENT' if end else 'THE COUCH TAKES OFFICE')
