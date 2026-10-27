import base64, datetime, importlib.util, json, threading, unittest, urllib.request, urllib.error
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'production'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
server=module('studio_server');job=module('studio_job')
class StudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler);cls.url='http://127.0.0.1:'+str(cls.http.server_port)
        cls.thread=threading.Thread(target=cls.http.serve_forever,daemon=True);cls.thread.start()
    @classmethod
    def tearDownClass(cls):cls.http.shutdown();cls.http.server_close()
    def request(self,path,token=False,body=None):
        return urllib.request.urlopen(urllib.request.Request(self.url+path,headers={'Authorization':'Bearer example-test-token'} if token else {},data=None if body is None else json.dumps(body).encode()))
    def test_health_and_shell(self):
        for path in ['/healthz',*server.STATIC]:
            with self.request(path) as r:self.assertEqual(r.status,200);self.assertIn("frame-ancestors 'none'",r.headers['Content-Security-Policy'])
    def test_private_api_requires_token(self):
        for path in ['/api/catalog','/api/runs','/api/videos','/api/media/123']:
            with self.assertRaises(urllib.error.HTTPError) as ctx:self.request(path)
            self.assertEqual(ctx.exception.code,401)
    @patch.object(server,'github',return_value={'permissions':{'push':False}})
    def test_read_only_user_cannot_control(self,g):
        with self.assertRaises(urllib.error.HTTPError) as ctx:self.request('/api/catalog',True)
        self.assertEqual(ctx.exception.code,401)
    @patch.object(server,'github')
    def test_dispatch_has_fixed_repo_ref_and_valid_episode(self,g):
        g.side_effect=[{'permissions':{'push':True}},{}]
        with self.request('/api/render',True,{'episode':'001'}) as r:self.assertEqual(r.status,202)
        self.assertEqual(g.call_args.args,('/actions/workflows/studio-production.yml/dispatches','example-test-token',{'ref':'main','inputs':{'episode':'001'}}))
    @patch.object(server,'github',return_value={'permissions':{'push':True}})
    def test_path_injection_rejected(self,g):
        with self.assertRaises(urllib.error.HTTPError) as ctx:self.request('/api/render',True,{'episode':'../../secret'})
        self.assertEqual(ctx.exception.code,400);self.assertEqual(g.call_count,1)
    def test_catalog_has_30_distinct_shorts(self):
        c=server.catalog();eps=c['schedule']['episodes'];self.assertEqual(len(eps),30);self.assertEqual(len(set(eps)),30)
        self.assertNotIn('008',eps)
        for ep in eps:self.assertTrue((ROOT/'episodes'/f'{ep}.json').exists())
    def test_calendar_disabled(self):self.assertIsNone(job.select_episode('',datetime.date(2026,10,29)))
    def test_explicit_episode(self):
        self.assertEqual(job.select_episode('001'),'001')
        for ep in ['../','999','1','001;whoami']:
            with self.assertRaises(ValueError):job.select_episode(ep)
    @patch.object(server,'github')
    def test_download_binary_and_safe_filename(self,g):
        g.side_effect=[{'permissions':{'push':True}},{'name':'episode_001.mp4','size':12},b'examplebytes']
        with self.request('/api/media/123',True) as r:
            self.assertEqual(r.headers['Content-Type'],'video/mp4');self.assertEqual(r.read(),b'examplebytes')
    @patch.object(server,'github')
    def test_non_video_asset_rejected(self,g):
        g.side_effect=[{'permissions':{'push':True}},{'name':'secrets.txt','size':12}]
        with self.assertRaises(urllib.error.HTTPError) as ctx:self.request('/api/media/123',True)
        self.assertEqual(ctx.exception.code,400)
    @patch.object(server,'github')
    def test_schedule_persisted_with_sha_and_put(self,g):
        config=server.catalog()['schedule']
        g.side_effect=[{'permissions':{'push':True}},{'sha':'old-sha','content':base64.b64encode(json.dumps(config).encode()).decode()},{}]
        with self.request('/api/schedule',True,{'enabled':True,'start_date':'2026-11-01'}) as r:self.assertEqual(r.status,200)
        self.assertEqual(g.call_args.kwargs,{'method':'PUT'})
        self.assertEqual(g.call_args.args[2]['sha'],'old-sha')
        saved=json.loads(base64.b64decode(g.call_args.args[2]['content']))
        self.assertTrue(saved['enabled']);self.assertEqual(saved['episodes'],config['episodes'])
    @patch.object(server,'github')
    def test_compile_uses_existing_workflow(self,g):
        g.side_effect=[{'permissions':{'push':True}},{}]
        with self.request('/api/compile',True,{'week':'week-001'}) as r:self.assertEqual(r.status,202)
        self.assertEqual(g.call_args.args[2],{'ref':'main','inputs':{'episodes':'all'}})
    @patch.object(server,'github',return_value={'permissions':{'push':True}})
    def test_invalid_date_rejected(self,g):
        with self.assertRaises(urllib.error.HTTPError) as ctx:self.request('/api/schedule',True,{'enabled':True,'start_date':'tomorrow'})
        self.assertEqual(ctx.exception.code,400)

if __name__=='__main__':unittest.main()
