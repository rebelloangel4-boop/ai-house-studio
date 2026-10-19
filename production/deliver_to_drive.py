"""Copy approved GitHub Actions MP4 artifacts into a private Google Drive folder.
Requires GDRIVE_CLIENT_ID, GDRIVE_CLIENT_SECRET, GDRIVE_REFRESH_TOKEN,
GDRIVE_FOLDER_ID, GH_TOKEN, GITHUB_REPOSITORY. Never publishes to social media.
"""
import io,json,os,urllib.request,urllib.parse,zipfile
from pathlib import Path
def req(url,data=None,headers=None,method=None):
    q=urllib.request.Request(url,data=data,headers=headers or {},method=method)
    with urllib.request.urlopen(q,timeout=120) as r:return r.read()
def token():
    fields={k:os.environ[v] for k,v in [('client_id','GDRIVE_CLIENT_ID'),('client_secret','GDRIVE_CLIENT_SECRET'),('refresh_token','GDRIVE_REFRESH_TOKEN')]}
    fields['grant_type']='refresh_token'
    return json.loads(req('https://oauth2.googleapis.com/token',urllib.parse.urlencode(fields).encode(),{'Content-Type':'application/x-www-form-urlencoded'}))['access_token']
def gh(url):
    # Authorization must not be forwarded to the signed artifact download host.
    q=urllib.request.Request(url,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(q,timeout=120) as r:
        final=r.geturl()
        if final.startswith('https://api.github.com/'):return r.read()
        if r.headers.get('Content-Type','').startswith('application/json'):return r.read()
        return r.read()
def main():
    access=token();auth={'Authorization':'Bearer '+access};folder=os.environ['GDRIVE_FOLDER_ID']
    repo=os.environ['GITHUB_REPOSITORY'];run=os.environ.get('SOURCE_RUN_ID')
    if not run:raise RuntimeError('SOURCE_RUN_ID required')
    runs=json.loads(gh(f'https://api.github.com/repos/{repo}/actions/runs/{run}'))
    if runs.get('conclusion')!='success':raise RuntimeError('Source run not successful')
    artifacts=json.loads(gh(f'https://api.github.com/repos/{repo}/actions/runs/{run}/artifacts?per_page=100'))['artifacts']
    copied=[];skipped=[]
    for art in artifacts:
        if art.get('expired'):continue
        if not (art['name'].startswith('ai-house-week-') or art['name'].startswith('ai-house-season-review-')):continue
        archive=gh(art['archive_download_url'])
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            qa_names=[n for n in z.namelist() if n.endswith('qa.json')]
            if not qa_names:continue
            qa=json.loads(z.read(qa_names[0]))
            if qa.get('technical_gate')!='PASS':continue
            for n in z.namelist():
                if not n.endswith('.mp4'):continue
                # A scene render may contain temporary scene_*.mp4; only copy finished deliverables.
                if not (Path(n).name.startswith('episode_') or Path(n).name.startswith('AI_HOUSE_')):continue
                filename=Path(n).name
                query=urllib.parse.urlencode({'q':f"name = '{filename}' and '{folder}' in parents and trashed = false",'fields':'files(id,name)','page_size':100})
                existing=json.loads(req('https://www.googleapis.com/drive/v3/files?'+query,headers=auth))
                if existing.get('files'):skipped.append(filename);continue
                data=z.read(n)
                metadata=json.dumps({'name':filename,'parents':[folder],'description':f'AI HOUSE review only; source GitHub Actions run {run}; publishing not approved'}).encode()
                boundary='ai_house_upload_boundary'
                body=(f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n').encode()+metadata+(f'\r\n--{boundary}\r\nContent-Type: video/mp4\r\n\r\n').encode()+data+(f'\r\n--{boundary}--\r\n').encode()
                result=json.loads(req('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name',body,{**auth,'Content-Type':f'multipart/related; boundary={boundary}'}))
                copied.append(result['name'])
    # Deliver the 30-day ready-to-copy publishing metadata alongside the videos.
    sheet=Path('production/AI_HOUSE_30_DAY_UPLOAD_METADATA.csv')
    if sheet.exists():
        filename='AI_HOUSE_30_DAY_UPLOAD_METADATA.csv'
        query=urllib.parse.urlencode({'q':f"name = '{filename}' and '{folder}' in parents and trashed = false",'fields':'files(id,name)'})
        if not json.loads(req('https://www.googleapis.com/drive/v3/files?'+query,headers=auth)).get('files'):
            boundary='ai_house_csv_boundary'
            meta=json.dumps({'name':filename,'parents':[folder],'mimeType':'text/csv'}).encode()
            body=(f'--{boundary}\\r\\nContent-Type: application/json; charset=UTF-8\\r\\n\\r\\n').encode()+meta+(f'\\r\\n--{boundary}\\r\\nContent-Type: text/csv\\r\\n\\r\\n').encode()+sheet.read_bytes()+(f'\\r\\n--{boundary}--\\r\\n').encode()
            req('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',body,{**auth,'Content-Type':f'multipart/related; boundary={boundary}'})
            copied.append(filename)
    print(json.dumps({'source_run':run,'uploaded':copied,'already_present':skipped,'publishing_enabled':False},indent=2))
if __name__=='__main__':main()
