"""Write evidence-based per-episode state; never infer creative completion."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def update():
 episodes=[]
 receipts=json.loads((ROOT/'production/v2/delivery_receipts.json').read_text()) if (ROOT/'production/v2/delivery_receipts.json').exists() else {}
 for n in range(1,11):
  source=f'2{n:02}';story=json.loads((ROOT/'episodes'/f'{source}.json').read_text());out=ROOT/'output'/source
  qa=json.loads((out/'qa.json').read_text()) if (out/'qa.json').exists() else {}
  scenes=len(list(out.glob('scene_*.checkpoint.json')))
  stages=dict(Script='complete',Graphics='implemented; visual review pending',Animation=f'{scenes}/9 scenes rendered',Voices='generated' if (out/'voice_qa.json').exists() else 'pending',Sound='mixed' if len(list(out.glob('sound_cues_*.json')))==9 else 'pending',Editing='rendered' if (out/f'episode_{source}.mp4').exists() else 'pending',Rendering='complete' if (out/f'episode_{source}.mp4').exists() else 'pending',QA=qa.get('extended_technical_gate','pending'),Complete=False)
  episodes.append(dict(episode=n,source=source,title=story['title'],requested_filename=f'AI_HOUSE_EP{n:02}_FINAL.mp4',stages=stages,qa=qa,listening_review='blocked: session does not support audio input',download_url=('https://chatgpt.com/library?file_id='+receipts[source]['video']+'&account_id=personal') if source in receipts else None))
 manifest=dict(schema=2,project='AI HOUSE 2.0',complete=False,episodes=episodes,zero_budget=True,paid_services_used=False,original_repository_baseline='ad49ab3872164036e39680158b207b0cb02874dc',resume_command='python production/v2/run.py --episode 201',notes='Local scene checkpoints and voice caches are reused. Technical checks do not certify cinematic quality or natural voices.')
 (ROOT/'PRODUCTION_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 return manifest
if __name__=='__main__':update()
