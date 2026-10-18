"""Original first-week scripts. Editorial drafts; no audience votes are fabricated."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=[
(2,'The Dinosaur Ate My Job Interview',[
('Max','My interview starts in thirty seconds.','dino','ONE JOB. ONE DINOSAUR.'),
('Luna','Then why is your resume smoking?','fire','A WARM INTRODUCTION'),
('Max','He added a personal touch.','bill','EXPERIENCE: FIRE'),
('Zig','Your strongest skill is now combustion.','scan','SCANNING QUALIFICATIONS'),
('Luna','Tell them you work well under pressure.','dino','CAREER ADVICE'),
('Max','Should I introduce him as my assistant, or blame the printer?','vote','HELP MAX GET HIRED')],('A  MY ASSISTANT','B  THE PRINTER')),
(3,'Our Robot Charged the Dinosaur Rent',[
('Zig','I have calculated the new tenant fee.','bill','EVERYONE PAYS RENT'),
('Max','He is literally two days old.','dino','A VERY SMALL TENANT'),
('Zig','Then he owes two days of rent.','bill','NO FREE TRIAL'),
('Luna','Can he pay in warmth?','fire','UTILITIES INCLUDED?'),
('Max','Great. Our heating bill is now our roommate.','dino','A HOT NEW DEAL'),
('Luna','What is his job: tiny heater, or security guard?','vote','HIRE THE DINOSAUR')],('A  TINY HEATER','B  SECURITY GUARD')),
(4,'We Gave a Dinosaur a Performance Review',[
('Luna','Your first performance review. Please do not eat it.','bill','EMPLOYEE OF THE WEEK'),
('Zig','Attendance: perfect. Furniture: missing.','scan','THE NUMBERS ARE IN'),
('Max','He is a creative problem solver.','dino','A STRONG REFERENCE'),
('Luna','The problem was a cushion.','fire','ONE SMALL INCIDENT'),
('Zig','And he solved it permanently.','dino','NO REPEAT PROBLEMS'),
('Max','Does he deserve a promotion, or a very tiny warning?','vote','YOU ARE THE MANAGER')],('A  PROMOTE HIM','B  TINY WARNING')),
(5,'The Dinosaur Found Our Emergency Fund',[
('Max','Good news. I found our emergency fund.','rent','FINALLY, SOME MONEY'),
('Luna','That is an empty envelope.','rent','PLEASE LOOK INSIDE'),
('Max','Exactly. No money, no money problems.','bill','MAX DOES FINANCE'),
('Zig','I am downloading a longer sigh.','scan','PROCESSING THAT LOGIC'),
('Luna','The dinosaur has better financial instincts. He eats the bills.','dino','DEBT MANAGEMENT'),
('Zig','Who should control the budget: Luna, or a locked box?','vote','CHOOSE OUR TREASURER')],('A  LUNA','B  LOCKED BOX')),
(6,'Our Dinosaur Failed the Quiet Test',[
('Luna','One minute of silence. That is all I ask.','dino','THE QUIET CHALLENGE'),
('Max','He has been practicing all morning.','dino','FULLY PREPARED'),
('Zig','The smoke alarm disagrees.','fire','A SMALL INTERRUPTION'),
('Max','That was a silent sneeze.','dino','TECHNICALLY CORRECT'),
('Luna','The ceiling was very loud about it.','bill','THE REPAIR ESTIMATE'),
('Max','What should we try next: bedtime stories, or dinosaur yoga?','vote','HELP US GET SOME SLEEP')],('A  BEDTIME STORY','B  DINOSAUR YOGA')),
(7,'One Week With the Worlds Worst Roommate',[
('Luna','One week. Two cushions. Zero rent.','bill','THE FIRST WEEK REPORT'),
('Zig','And one surprisingly warm apartment.','fire','LOOK ON THE BRIGHT SIDE'),
('Max','Admit it. You would miss him.','dino','THE FINAL ARGUMENT'),
('Luna','I would miss the sofa more.','dino','SOMEONE HAD TO SAY IT'),
('Zig','The sofa never ate the bills.','bill','ONE POINT TO DINOSAUR'),
('Luna','Final vote. Keep our tiny disaster, or find him a new home?','vote','YOU DECIDE WHAT IS NEXT')],('A  KEEP HIM','B  NEW HOME'))]
for number,title,scenes,choices in DATA:
    story={'series':'AI HOUSE — You Decide','episode':number,'title':title,'production_status':'editorial draft; no viewer votes counted','scenes':[]}
    for i,(speaker,line,visual,beat) in enumerate(scenes):
        s={'speaker':speaker,'line':line,'visual':visual,'beat':beat,'min_seconds':4 if i<5 else 6}
        if visual=='fire':s['lead']=1.9
        if visual=='vote':s.update(choice_a=choices[0],choice_b=choices[1])
        story['scenes'].append(s)
    (ROOT/'episodes'/f'{number:03}.json').write_text(json.dumps(story,indent=2)+'\n')
bridges=[
('Luna','Welcome to our first week with a dinosaur. The rent money did not survive.','rent','AI HOUSE / WEEK ONE'),
('Zig','Next, Max tried to get a job. We needed the income.','bill','DAY TWO / JOB INTERVIEW'),
('Luna','With the job situation unclear, Zig tried collecting rent.','bill','DAY THREE / THE TENANT FEE'),
('Zig','A performance review followed. Results were mixed.','scan','DAY FOUR / PERFORMANCE REVIEW'),
('Luna','Then Max discovered accounting. We are still recovering.','rent','DAY FIVE / THE BUDGET'),
('Zig','By day six, everyone needed some quiet.','dino','DAY SIX / THE QUIET TEST'),
('Luna','Finally, we added up the damage. And the benefits.','bill','DAY SEVEN / THE VERDICT'),
('Luna','That was our first week. Tell us: keep the dinosaur, or find him a new home? Your decision can shape the next chapter.','vote','THE NEXT CHAPTER IS YOURS')]
story={'series':'AI HOUSE','episode':8,'title':'A Dinosaur Ate Our Rent: The Complete First Week','production_status':'compilation connective scenes','scenes':[{'speaker':sp,'line':line,'visual':v,'beat':b,'min_seconds':4} for sp,line,v,b in bridges]}
(ROOT/'episodes/008.json').write_text(json.dumps(story,indent=2)+'\n')
(ROOT/'packs/week-001.json').write_text(json.dumps({'id':'week-001','launch_date':'2026-10-19','episodes':[f'{i:03}' for i in range(1,8)],'bridges':'008','editorial_status':'draft, awaiting pilot review','votes_counted':False,'publishing_enabled':False},indent=2)+'\n')

# Props carry each scene's meaning rather than reusing the pilot's labels.
prop_map={
 2:{2:('RESUME','MAX')},
 3:{0:('TENANT FEE','$2 / DAY'),2:('RENT DUE','$4')},
 4:{0:('REVIEW','WEEK 1')},
 5:{2:('BUDGET','$0')},
 6:{4:('REPAIR BILL','$900')},
 7:{0:('WEEK 1','-$900'),4:('UNPAID','BILLS')},
 8:{1:('RESUME','MAX'),2:('TENANT FEE','$2 / DAY'),6:('WEEK 1','-$900')}
}
scans={4:{1:'ATTENDANCE: 100%'},5:{3:'SIGH: DOWNLOADING'},8:{3:'REVIEW COMPLETE'}}
for number in range(2,9):
 path=ROOT/'episodes'/f'{number:03}.json';story=json.loads(path.read_text())
 for index,(title,value) in prop_map.get(number,{}).items():
  story['scenes'][index].update(prop_title=title,prop_value=value)
 for index,label in scans.get(number,{}).items():story['scenes'][index]['scan_label']=label
 path.write_text(json.dumps(story,indent=2)+'\n')
