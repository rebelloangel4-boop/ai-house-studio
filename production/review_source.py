"""Reuse only verified outputs matching this exact visual, script and voice pipeline."""
import hashlib, io, json, os, subprocess, sys, urllib.request, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fingerprint(ep):
    files=[ROOT/'episodes'/f'{ep}.json',*sorted((ROOT/'studio').glob('*.py')),ROOT/'production/voice-requirements.txt']
    return hashlib.sha256(b''.join(p.relative_to(ROOT).as_posix().encode()+p.read_bytes() for p in files)).hexdigest()
def main():
    ep=sys.argv[2]; folder=ROOT/'output'/ep
    if sys.argv[1]=='stamp':
        (folder/'source.json').write_text(json.dumps({'fingerprint':fingerprint(ep),'commit':os.environ['GITHUB_SHA'],'listening_approval':'PENDING'}));return
    repo=os.environ['GITHUB_REPOSITORY']; name=f'ai-house-voice-v1-{ep}'
    artifacts=json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/actions/artifacts?per_page=100']))['artifacts']
    for artifact in artifacts:
        if artifact['name']!=name or artifact['expired']:continue
        # gh handles authenticated redirects; no tokens are printed or stored in artifacts.
        try:
            data=subprocess.check_output(['gh','api',f'repos/{repo}/actions/artifacts/{artifact["id"]}/zip'])
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                manifest=json.loads(z.read('source.json'))
                if manifest.get('fingerprint')!=fingerprint(ep):continue
                if json.loads(z.read('qa.json'))['technical_gate']!='PASS':continue
                if any(not (folder/p).resolve().is_relative_to(folder.resolve()) for p in z.namelist()):raise ValueError('Unsafe artifact')
                folder.mkdir(parents=True,exist_ok=True);z.extractall(folder)
            print(f'Reusing verified {ep} from artifact {artifact["id"]}')
            with open(os.environ['GITHUB_OUTPUT'],'a') as f:f.write('reused=true\n')
            return
        except (subprocess.CalledProcessError,ValueError,KeyError,zipfile.BadZipFile) as e:
            print(f'Cannot reuse artifact {artifact["id"]}: {type(e).__name__}')
    with open(os.environ['GITHUB_OUTPUT'],'a') as f:f.write('reused=false\n')
if __name__=='__main__':main()
