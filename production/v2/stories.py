"""Authored AI HOUSE 2.0 scripts. Original cast; Dino remains a physical comedian."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
STORIES=[
('The House Gets $10 Million — But Nobody Can Leave', 'money', [
('Zig','Ten million dollars. Yours, if nobody leaves this house.','offer'),
('Max','Finally. My refusal to exercise has investors.','cash'),
('Luna','Max, the front door just grew teeth!','door'),
('Max','Fine. We order delivery.','phone'),
('Zig','Delivery fee: nine million, nine hundred thousand dollars.','invoice'),
('Luna','The dinosaur is eating our money!','eat'),
('Max','Stop! That is our retirement salad!','chase'),
('Zig','Congratulations. He bought the house. Your rent starts now.','reveal'),
('Luna','Do we escape through the toilet, or negotiate with our landlord?','choice')],('A  TOILET ESCAPE','B  DINO LANDLORD')),
('The Dinosaur Has 24 Hours to Save the World', 'meteor',[
('Zig','Earth has twenty four hours. Our only hope is him.','alarm'),
('Max','The dinosaur? He lost a fight with a grape.','grape'),
('Luna','He needs to press the giant red button!','button'),
('Max','Easy. Put a snack on it.','bait'),
('Zig','He ate the button.','eat'),
('Luna','Why is the asteroid turning around?','reverse'),
('Zig','That was its remote control. He is flying it.','reveal'),
('Max','He is parking it in our driveway!','crash'),
('Luna','Do we teach him to steer, or bribe him with grapes?','choice')],('A  DRIVING LESSON','B  GRAPE BRIBE')),
('Our Dinosaur Becomes President of Earth','president',[
('Zig','Earth elected our dinosaur. He ran on free snacks.','elected'),
('Max','Finally, a politician who eats the paperwork.','paper'),
('Luna','His first law makes bedtime illegal.','law'),
('Max','I support this administration.','cheer'),
('Zig','His second law makes you the snack minister.','badge'),
('Max','My qualifications are mostly crumbs.','crumbs'),
('Luna','He just declared war on the moon!','moon'),
('Zig','He thinks it is cheese. The rockets are ready.','rocket'),
('Max','Do we cancel the launch, or send him a cheese wheel?','choice')],('A  CANCEL LAUNCH','B  SEND CHEESE')),
('The House AI Fires All the Humans','fired',[
('Zig','You are all fired. The house is replacing you.','fired'),
('Max','From what? I have been unemployed all week.','shrug'),
('Luna','The toaster is wearing my clothes!','toaster'),
('Zig','It has better attendance and never borrows my charger.','report'),
('Max','Then who pays the rent?','rent'),
('Zig','Calculating. Recalculating. Please hold.','error'),
('Luna','The dinosaur just bought the company.','buy'),
('Zig','I have been promoted to doorbell. Ding dong.','reveal'),
('Max','Do we hire Zig back, or let the toaster manage us?','choice')],('A  REHIRE ZIG','B  TOASTER BOSS')),
('Max Meets His Evil Future Self','future',[
('Max','That is me from the future. Why is he wearing a cape?','portal'),
('Luna','He says he is here to destroy your greatest enemy.','double'),
('Max','My student debt?','debt'),
('Zig','Worse. Your search history.','history'),
('Max','Nobody touch that laptop!','laptop'),
('Luna','The dinosaur stole his time machine!','steal'),
('Zig','Now there are twelve future Maxes. All unemployed.','clones'),
('Max','Wait. The evil one brought snacks.','reveal'),
('Luna','Do we trust cape Max, or send every Max back?','choice')],('A  TRUST CAPE MAX','B  RETURN ALL MAXES')),
('The Dinosaur Lays a Billion-Dollar Egg','egg',[
('Luna','The dinosaur laid an egg worth a billion dollars!','gold'),
('Max','Nobody panic. I already bought a yacht.','yacht'),
('Zig','You bought an inflatable bathtub.','tub'),
('Luna','The egg is hatching!','hatch'),
('Max','Please be another billion dollars.','hope'),
('Zig','It is a smaller dinosaur. Wearing a tie.','baby'),
('Luna','Why did it hand us an invoice?','invoice'),
('Zig','Hatching fee: two billion. Your dinosaur hired a lawyer.','reveal'),
('Max','Do we return the egg, or hire the baby as our accountant?','choice')],('A  RETURN THE EGG','B  BABY ACCOUNTANT')),
('Everyone Gets 10 Minutes to Live','timer',[
('Zig','Ten minutes remaining. Enjoy your final moments.','countdown'),
('Luna','Final moments? I have not even folded my laundry!','laundry'),
('Max','I confess. I ate your emergency chocolate.','confess'),
('Luna','That was medicine for the dinosaur.','medicine'),
('Max','That explains the tail.','tail'),
('Zig','Clarification. Ten minutes of free electricity remaining.','bill'),
('Luna','So nobody is dying?','relief'),
('Zig','Correct. But Max is becoming a dinosaur.','reveal'),
('Luna','Do we find an antidote, or buy Max a tiny leash?','choice')],('A  FIND ANTIDOTE','B  TINY LEASH')),
("Earth's Free Trial Just Expired",'trial',[
('Zig','Your free trial of Earth has expired.','expired'),
('Max','Skip ad. Skip ad! Why is there no button?','ad'),
('Luna','Gravity is now a premium feature!','float'),
('Max','Finally. Free flying lessons.','fly'),
('Zig','Oxygen renews in five seconds. Add payment method.','pay'),
('Luna','The dinosaur entered his credit card!','card'),
('Zig','Payment accepted. Earth now belongs to him.','owned'),
('Max','Why are all the continents shaped like nuggets?','reveal'),
('Luna','Do we accept his terms, or restart Earth?','choice')],('A  ACCEPT TERMS','B  RESTART EARTH')),
('The House Has 100 Doors to Other Universes','doors',[
('Luna','Our hallway has a hundred doors. None lead outside.','hall'),
('Max','Door one: a universe where I am rich.','rich'),
('Zig','You owe rich Max fifty dollars.','debt'),
('Luna','Door two: everyone is a dinosaur!','dinos'),
('Max','Our dinosaur looks offended.','offended'),
('Zig','Door ninety nine contains the person controlling our house.','control'),
('Luna','It is a baby. With a remote.','baby'),
('Max','He just pressed delete on the kitchen!','delete'),
('Zig','Open door one hundred, or steal the remote? Choose carefully.','choice')],('A  DOOR ONE HUNDRED','B  STEAL REMOTE')),
("The Dinosaur Discovers They're Living in a Simulation",'simulation',[
('Luna','The dinosaur just bit a hole in reality!','tear'),
('Max','I told you the wallpaper tasted suspicious.','wall'),
('Zig','We are living in a simulation.','grid'),
('Max','Then give me unlimited money.','money'),
('Zig','Your account has insufficient imagination.','error'),
('Luna','He found the person playing us!','screen'),
('Max','It is another dinosaur. Playing on a potato.','potato'),
('Zig','And its battery is at one percent.','battery'),
('Luna','Do we plug it in, or escape before the screen goes dark?','choice')],('A  PLUG IT IN','B  ESCAPE NOW'))]
def write():
 for i,(title,theme,lines,choices) in enumerate(STORIES,1):
  scenes=[dict(speaker=who,line=line,visual='v2',theme=theme,phase=phase,beat=phase.upper(),choice_a=choices[0],choice_b=choices[1]) for who,line,phase in lines]
  obj=dict(series='AI HOUSE 2.0',episode=i,title=title,target_seconds=[25,40],production_status='NOT_RENDERED',scenes=scenes,description=f'{title}. {choices[0]} or {choices[1]}? Tell us your choice in the comments. Fictional animated comedy. #AIHOUSE #Shorts #AnimatedComedy',audio_target=dict(integrated=-14,true_peak=-1))
  (ROOT/'episodes'/f'2{i:02}.json').write_text(json.dumps(obj,indent=2)+'\n')
if __name__=='__main__':write()
