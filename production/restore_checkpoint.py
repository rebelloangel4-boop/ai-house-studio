"""Restore the latest bounded, path-checked pilot checkpoint for a fresh runner."""
import io,json,os,subprocess,zipfile
from pathlib import Path
repo=os.environ['GITHUB_REPOSITORY']
name='ai-house-short008-pilot-checkpoint'
artifacts=json.loads(subprocess.check_output(['gh','api',f'repos/{repo}/actions/artifacts?per_page=100']))['artifacts']
for item in artifacts:
    if item['name']!=name or item['expired']:continue
    raw=subprocess.check_output(['gh','api',f'repos/{repo}/actions/artifacts/{item["id"]}/zip'])
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        assert sum(i.file_size for i in z.infolist())<80_000_000,'Checkpoint exceeds budget'
        root=Path.cwd().resolve()
        for n in z.namelist():
            dest=(root/n).resolve()
            assert dest.is_relative_to(root),'Unsafe path'
            assert n.startswith(('output/009/','.voice-cache/')),'Unexpected checkpoint contents'
        z.extractall(root)
    print(f'Restored checkpoint {item["id"]}; renderer fingerprints validate scene reuse')
    break
else:print('No previous checkpoint; starting fresh')
