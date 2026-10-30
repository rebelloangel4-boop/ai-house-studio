"""Additional AI HOUSE 2.0 quality gates. Creative/listening status is never inferred."""
import json,re,subprocess,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'studio'))
from importlib.util import spec_from_file_location, module_from_spec
spec=spec_from_file_location("baseline_verify",ROOT/"studio"/"verify.py");module=module_from_spec(spec);spec.loader.exec_module(module);verify=module.verify

def check(ep):
 folder=ROOT/'output'/ep;verify(folder);movie=folder/f'episode_{ep}.mp4'
 scan=subprocess.run(['ffmpeg','-hide_banner','-i',str(movie),'-vf','blackdetect=d=0.08:pix_th=0.10,freezedetect=n=-55dB:d=1','-af','loudnorm=I=-14:TP=-1:LRA=9:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
 log=scan.stderr;(folder/'full_scan.log').write_text(log)
 loud=json.loads(log[log.rfind('{'):]);black=re.findall(r'black_start:(\S+).*?black_end:(\S+)',log);frozen=re.findall(r'freeze_start: (\S+)',log)
 qa=json.loads((folder/'qa.json').read_text());qa.update(black_intervals=black,frozen_sections=frozen,integrated_lufs=float(loud['input_i']),true_peak_dbtp=float(loud['input_tp']),sha256=hashlib.sha256(movie.read_bytes()).hexdigest())
 assert not black,black
 assert not frozen,frozen
 assert -15<=qa['integrated_lufs']<=-13,qa
 assert qa['true_peak_dbtp']<=-1,qa
 # Dialogue-driven Shorts may finish slightly below 25 seconds; never pad pauses.
 assert 23<=qa['duration_seconds']<=45,qa
 voice=json.loads((folder/'voice_qa.json').read_text());assert all(s['automated_validation']=='PASS' for s in voice['segments'])
 assert all((folder/f'sound_cues_{i}.json').exists() for i in range(9))
 qa['extended_technical_gate']='PASS';qa['listening_approval']='PENDING';qa['creative_approval']='PENDING'
 (folder/'qa.json').write_text(json.dumps(qa,indent=2))
 print(json.dumps(qa,indent=2))
if __name__=='__main__':check(sys.argv[1])

