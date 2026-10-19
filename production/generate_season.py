"""Create 30 connected, review-only comedy scripts with consistent Episode-2 pacing.
Run locally or in GitHub Actions. Existing hand-edited episodes 001–003 are preserved.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Story beats: visual setup, escalating ridiculous consequence, end vote.
BEATS=[
("Zig Trains a Dinosaur","DINO! DROP THE COUCH!","He thinks it's a chew toy.","That's a thousand-dollar chew toy.","I taught him to sit!","On the landlord.","Our security deposit just screamed.","Vote A: train Dino! B: train Max!"),
("Luna's House Rules Explode","WHO ATE THE RULEBOOK?!","Dino said it looked delicious.","That was our only copy.","Fine. Rule one: no fire!","He just invented rule two: more fire.","I'm moving to the moon.","Vote A: ban fire! B: ban Max!"),
("Dino Has a Secret Admirer","WHO SENT DINO FLOWERS?!","He's got more dates than me.","The flowers are carnivorous.","Aw. True love bites.","So does the bouquet.","The vase just proposed.","Vote A: open it! B: run away!"),
("The Landlord Meets Dino","WHY IS THE LANDLORD SCREAMING?!","He met our new roommate.","The roommate ate his clipboard.","That's a good first impression!","He's charging us pet rent.","Dino's charging HIM entry.","Vote A: negotiate! B: hide Dino!"),
("Pet Deposit Disaster","THE DEPOSIT IS TEN THOUSAND?!","Dino is technically a goldfish.","That goldfish breathes fire.","He's a very passionate fish.","The landlord wants proof.","Dino just cooked the aquarium.","Vote A: pay! B: disguise Dino!"),
("Max Opens Dino Daycare","WHY ARE THERE SIX DINOSAURS?!","I started a babysitting business.","You're being babysat by reptiles.","They love me!","They ate the customer.","Five-star service. No refunds.","Vote A: close it! B: expand!"),
("Zig Builds a Dino Translator","HE JUST CALLED ME WHAT?!","The collar translates dinosaur.","It says Max is the pet.","That is NOT accurate.","It also says pay your rent.","Even dinosaurs have standards.","Vote A: translate more! B: unplug!"),
("Dino Says His First Word","DINO JUST SAID MAMA?!","Obviously he means me.","He said pizza, Max.","That's basically my name.","Now he's ordering fifty.","He has better credit than you.","Vote A: deliver! B: cancel!"),
("Max Sells Dino Selfies","WHY IS DINO FAMOUS?!","I sold his selfies online.","You sold his baby pictures.","For excellent profit!","He wants royalties.","He's suing you in crayon.","Vote A: pay Dino! B: lawyer up!"),
("A Rival Influencer Arrives","SOMEONE STOLE DINO'S FANS!","It's a dancing toaster.","It has better choreography.","I can dance!","Please don't demonstrate.","The toaster just blocked you.","Vote A: dance battle! B: prank!"),
("Dino Goes Missing","WHERE IS OUR DINOSAUR?!","He left a goodbye note.","It says 'need snacks'.","He can't write!","Then who forged the note?","Your handwriting is worse.","Vote A: search! B: follow crumbs!"),
("Dino Brings a Friend","WHY ARE THERE TWO OF THEM?!","Dino made a friend.","His friend is twice as hungry.","Maybe they're twins?","One of them is the landlord.","That explains the tie.","Vote A: welcome! B: investigate!"),
("Two Dinos One Apartment","THE FLOOR IS MOVING!","They're playing hide and seek.","Under the building.","At least they're bonding.","With the plumbing.","Our bathroom is now a volcano.","Vote A: evacuate! B: film it!"),
("Zig Makes a Clone","WHY ARE THERE TWO ZIGS?!","I upgraded myself.","The clone is actually nice.","Delete him immediately.","He made everyone breakfast.","I am experiencing jealousy.","Vote A: keep clone! B: delete!"),
("Luna Finds a Dino Map","WHY IS THE MAP GLOWING?!","Dino drew a treasure map.","That's our electricity bill.","Wait. It leads downstairs.","We don't have downstairs.","We do now.","Vote A: explore! B: seal it!"),
("Max Hunts for Treasure","I FOUND A GOLDEN KEY!","That's the bathroom key.","Why is it glowing?","Because you microwaved it.","Then why is it opening walls?","I withdraw my diagnosis.","Vote A: enter! B: run!"),
("The Secret Couch Door","OUR COUCH HAS A BASEMENT?!","Best furniture investment ever.","You bought it from a wizard.","It came with free delivery.","And a screaming portal.","Five stars. Great legroom.","Vote A: jump! B: lock it!"),
("Underground Dino Arcade","WHY IS DINO WINNING EVERYTHING?!","He has tiny lucky hands.","He has the cheat codes.","He can't read!","Neither can Max.","Stop attacking me personally.","Vote A: compete! B: cash out!"),
("Dino Wins a Mystery Prize","HE WON A GIANT EGG?!","It's his trophy.","The trophy is breathing.","Maybe it's a lamp.","Your lamp just growled.","I want a refund.","Vote A: hatch! B: return!"),
("Zig Detects a Conspiracy","THE EGG IS SPYING ON US!","It's just blinking.","Those are security cameras.","Who installed them?","The egg did.","I respect its work ethic.","Vote A: expose! B: pretend!"),
("The Tiny Genius Hatches","THE BABY JUST DID MATH?!","He calculated our rent.","He found three errors.","That's impossible!","He also found your lies.","I don't like this baby.","Vote A: hire him! B: hide!"),
("Baby Dino Runs Accounting","WE HAVE A NEW ACCOUNTANT?!","He's four minutes old.","And already more qualified.","Can he do my taxes?","He just audited your snacks.","I plead hungry.","Vote A: promote! B: fire!"),
("Max Is Banned From Decisions","WHY AM I ON PROBATION?!","You bought a second volcano.","It was on sale!","No more financial decisions.","What about emotional ones?","Also banned.","Vote A: forgive! B: extend!"),
("Luna Runs for President","I'M RUNNING THIS HOUSE!","You already do.","Now it's official.","What is your policy?","No fires. No debt. No Max.","That feels targeted.","Vote A: vote Luna! B: rebel!"),
("Dino Runs Against Luna","THE DINOSAUR IS RUNNING?!","His slogan is free pizza.","That's bribery!","It's working.","He just won the couch.","I demand a recount.","Vote A: Luna! B: Dino!"),
("Election Night Chaos","WHO STOLE THE BALLOT BOX?!","Dino thinks it's a lunchbox.","That's election interference.","It's also empty.","Because Max forgot the ballots.","Democracy is having a moment.","Vote A: recount! B: revote!"),
("Finale: Who Rules AI House?","WE HAVE A NEW PRESIDENT?!","The results are unbelievable.","Nobody voted for Max.","I voted for myself!","That was your pizza receipt.","The house just voted back.","Vote A: new rules! B: chaos!")
]
def make(i,beat):
    title,*lines=beat
    visuals=['fire','dino','scan','hatch','meeting','chomp','vote']
    speakers=['Luna','Max','Zig','Max','Luna','Zig','Luna']
    scenes=[]
    for j,(speaker,line,visual) in enumerate(zip(speakers,lines,visuals)):
        scene={'speaker':speaker,'line':line,'visual':visual,'beat':(['WHAT JUST HAPPENED?!','MAX HAS A PLAN','ZIG DISAPPROVES','IT GETS WORSE','LUNA PANICS','ABSOLUTE CHAOS','YOU DECIDE!'][j]),'min_seconds':(4.1 if j==6 else 3.4 if j%2==0 else 3.2),'lead':0.05}
        if j==6:
            import re
            options=re.search(r'Vote A:\s*(.*?)!\s*B:\s*(.*?)!',line,re.I)
            if options:
                scene.update(choice_a='A  '+options.group(1).upper(),choice_b='B  '+options.group(2).upper())
            else:
                scene.update(choice_a='A  OPTION ONE',choice_b='B  OPTION TWO')
        scenes.append(scene)
    return {'series':'AI HOUSE — You Decide','episode':i,'title':title,'target_seconds':25,'production_status':'generated review draft; creative approval pending','scenes':scenes}
def main():
    # Episode 3 already authored; generate 4–30 using story ideas.
    assert len(BEATS)==27,len(BEATS)
    for i,beat in enumerate(BEATS,4):
        p=ROOT/'episodes'/f'{i:03}.json'
        if p.exists():continue
        p.write_text(json.dumps(make(i,beat),indent=2)+'\n')
    print('Season scripts created (existing episodes preserved)')
if __name__=='__main__':main()
