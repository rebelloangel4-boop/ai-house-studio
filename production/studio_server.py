"""Small authenticated GitHub-backed control plane; no credentials or media persisted."""
import json, os, re, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'rebelloangel4-boop/ai-house-studio'
API = 'https://api.github.com/repos/' + REPO
STATIC = {'/': ('index.html','text/html'), '/app.js': ('app.js','text/javascript'), '/style.css': ('style.css','text/css'), '/manifest.webmanifest': ('manifest.webmanifest','application/manifest+json'), '/sw.js': ('sw.js','text/javascript'), '/icon.svg': ('icon.svg','image/svg+xml')}

def github(path, token, data=None, binary=False):
    headers={'Authorization':'Bearer '+token, 'Accept':'application/octet-stream' if binary else 'application/vnd.github+json', 'X-GitHub-Api-Version':'2022-11-28', 'User-Agent':'AI-HOUSE-Studio'}
    if data is not None: headers['Content-Type']='application/json'
    req=urllib.request.Request(API+path, data=None if data is None else json.dumps(data).encode(), headers=headers)
    # Prevent a GitHub storage redirect from forwarding the API credential.
    class SafeRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            result=super().redirect_request(req,fp,code,msg,headers,newurl)
            if result: result.remove_header('Authorization')
            return result
    with urllib.request.build_opener(SafeRedirect).open(req,timeout=60) as res:
        body=res.read(85_000_001)
        if len(body)>85_000_000: raise ValueError('Response exceeds media limit')
        return body if binary else (json.loads(body) if body else {})

def catalog():
    manifest=json.loads((ROOT/'production/manifest.json').read_text())
    return {'manifest':manifest,'episodes':[json.loads(p.read_text()) for p in sorted((ROOT/'episodes').glob('*.json'))], 'schedule':json.loads((ROOT/'production/studio_schedule.json').read_text())}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Do not log request headers, credentials or query strings.
    def reply(self,status,body,typ='application/json',extra=None):
        if not isinstance(body,bytes): body=json.dumps(body).encode()
        self.send_response(status)
        self.send_header('Content-Type',typ)
        self.send_header('Content-Length',str(len(body)))
        self.send_header('Cache-Control','no-store')
        self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; media-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
        for k,v in (extra or {}).items(): self.send_header(k,v)
        self.end_headers(); self.wfile.write(body)
    def authorized(self):
        auth=self.headers.get('Authorization','')
        if not auth.startswith('Bearer ') or len(auth)<16: raise PermissionError('Sign in with a repository-scoped GitHub token')
        token=auth[7:]
        repo=github('',token)
        if not repo.get('permissions',{}).get('push'): raise PermissionError('Repository write access is required')
        return token
    def do_GET(self): self.handle_request(False)
    def do_POST(self): self.handle_request(True)
    def handle_request(self,post):
        try:
            if self.path=='/healthz' and not post: return self.reply(200,{'status':'ok'})
            if self.path in STATIC and not post:
                name,typ=STATIC[self.path];return self.reply(200,(ROOT/'web'/name).read_bytes(),typ)
            if not self.path.startswith('/api/'): return self.reply(404,{'error':'Not found'})
            token=self.authorized()
            if not post:
                if self.path=='/api/catalog': return self.reply(200,catalog())
                if self.path=='/api/runs':
                    runs=github('/actions/runs?per_page=40',token)['workflow_runs']
                    return self.reply(200,[{k:r[k] for k in ('id','name','status','conclusion','html_url','created_at','head_sha')} for r in runs])
                if self.path=='/api/videos':
                    releases=[]
                    for page in range(1,6):
                        batch=github(f'/releases?per_page=100&page={page}',token);releases+=batch
                        if len(batch)<100: break
                    return self.reply(200,[{'id':a['id'],'name':a['name'],'bytes':a['size'],'release':r['name'],'draft':r['draft'],'created_at':a['created_at']} for r in releases for a in r['assets'] if a['name'].endswith('.mp4')])
                m=re.fullmatch(r'/api/media/(\d+)',self.path)
                if m:
                    asset=github('/releases/assets/'+m[1],token)
                    if not asset['name'].endswith('.mp4') or asset['size']>80_000_000: raise ValueError('Not an allowed MP4')
                    body=github('/releases/assets/'+m[1],token,binary=True)
                    return self.reply(200,body,'video/mp4',{'Content-Disposition':'attachment; filename="'+re.sub(r'[^a-zA-Z0-9_.-]','_',asset['name'])+'"'})
            else:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<4096: raise ValueError('Invalid request size')
                payload=json.loads(self.rfile.read(length))
                if self.path=='/api/render':
                    ep=str(payload.get('episode',''))
                    if not re.fullmatch(r'\d{3}',ep) or not (ROOT/'episodes'/f'{ep}.json').is_file(): raise ValueError('Unknown episode')
                    github('/actions/workflows/studio-production.yml/dispatches',token,{'ref':'main','inputs':{'episode':ep}})
                    return self.reply(202,{'status':'requested','message':'GitHub accepted dispatch; refresh history to confirm start.'})
            return self.reply(404,{'error':'Not found'})
        except PermissionError as exc: self.reply(401,{'error':str(exc)})
        except urllib.error.HTTPError as exc: self.reply(502,{'error':f'GitHub returned HTTP {exc.code}; check token permissions, expiry and Actions availability.'})
        except (ValueError,KeyError,json.JSONDecodeError): self.reply(400,{'error':'Invalid input or unexpected upstream response'})
        except Exception: self.reply(502,{'error':'Service request failed; retry or inspect deployment logs.'})

if __name__=='__main__': ThreadingHTTPServer(('0.0.0.0',int(os.environ.get('PORT','8000'))),Handler).serve_forever()
