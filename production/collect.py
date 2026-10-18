"""Fetch exact week's successful daily artifacts; fail on missing or stale sources."""
import hashlib,json,os,urllib.request,zipfile,io
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];pack=json.loads((ROOT/'packs/week-001.json').read_text());repo=os.environ['GITHUB_REPOSITORY'];token=os.environ['GH_TOKEN']
class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        redirected=super().redirect_request(req,fp,code,msg,headers,newurl)
        if redirected is not None: redirected.remove_header('Authorization')
        return redirected
opener=urllib.request.build_opener(SafeRedirect)
def request(url):
    req=urllib.request.Request(url,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json'})
    return opener.open(req,timeout=90).read()
artifacts=json.loads(request(f'https://api.github.com/repos/{repo}/actions/artifacts?per_page=100'))['artifacts']
for ep in pack['episodes']+[pack['bridges']]:
    wanted=f'ai-house-{pack["id"]}-{ep}';matches=[a for a in artifacts if a['name']==wanted and not a['expired']]
    if not matches:raise RuntimeError(f'Missing daily artifact: {wanted}')
    match=max(matches,key=lambda a:a['created_at']);dest=ROOT/'output'/ep;dest.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(request(match['archive_download_url']))) as z:
        for n in z.namelist():
            p=(dest/n).resolve()
            if not p.is_relative_to(dest.resolve()):raise ValueError('Unsafe archive path')
        z.extractall(dest)
    manifest=json.loads((dest/'source.json').read_text());expected=hashlib.sha256((ROOT/'episodes'/f'{ep}.json').read_bytes()).hexdigest()
    assert manifest['script_sha256']==expected,f'Stale episode {ep}: rerender before compilation'
print('Collected and verified all eight source artifacts')
