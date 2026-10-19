"""Upload finished MP4 and matching text directly, not ZIP, to private Drive."""
import json,os,sys,urllib.parse,urllib.request
from pathlib import Path
def call(url,data=None,headers=None):
    with urllib.request.urlopen(urllib.request.Request(url,data=data,headers=headers or {}),timeout=180) as r:return json.loads(r.read())
def main():
    folder=Path(sys.argv[1]);fields={k:os.environ[v] for k,v in [('client_id','GDRIVE_CLIENT_ID'),('client_secret','GDRIVE_CLIENT_SECRET'),('refresh_token','GDRIVE_REFRESH_TOKEN')]}
    fields['grant_type']='refresh_token'
    token=call('https://oauth2.googleapis.com/token',urllib.parse.urlencode(fields).encode(),{'Content-Type':'application/x-www-form-urlencoded'})['access_token']
    auth={'Authorization':'Bearer '+token};parent=os.environ['GDRIVE_FOLDER_ID']
    for path in sorted(folder.iterdir()):
        if not (path.name.startswith('episode_') and path.suffix in ('.mp4','.txt')):continue
        name=path.name
        query=urllib.parse.urlencode({'q':f"name = '{name}' and '{parent}' in parents and trashed = false",'fields':'files(id,name)'})
        existing=call('https://www.googleapis.com/drive/v3/files?'+query,headers=auth)
        if existing.get('files'):print('Already delivered:',name);continue
        boundary='ai_house_direct_upload'
        typ='video/mp4' if path.suffix=='.mp4' else 'text/plain'
        metadata=json.dumps({'name':name,'parents':[parent],'description':'AI HOUSE review only; publishing approval pending'}).encode()
        body=(f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n').encode()+metadata+(f'\r\n--{boundary}\r\nContent-Type: {typ}\r\n\r\n').encode()+path.read_bytes()+(f'\r\n--{boundary}--\r\n').encode()
        result=call('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name',body,{**auth,'Content-Type':f'multipart/related; boundary={boundary}'})
        print('Delivered:',result['name'])
if __name__=='__main__':main()
