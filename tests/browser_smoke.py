"""Browser layout/auth-shell checks; authenticated UI uses explicit fixtures, not live credentials."""
import json, subprocess, sys, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
process=subprocess.Popen([sys.executable,'production/studio_server.py'],cwd=ROOT,env={**__import__('os').environ,'PORT':'8765'})
try:
    for _ in range(50):
        try:urllib.request.urlopen('http://127.0.0.1:8765/healthz');break
        except OSError:time.sleep(.1)
    with sync_playwright() as p:
        browser=p.chromium.launch()
        for width,height in [(390,844),(1280,800)]:
            page=browser.new_page(viewport={'width':width,'height':height})
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto('http://127.0.0.1:8765');page.get_by_role('heading',name='Open your studio').wait_for()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert page.request.get('http://127.0.0.1:8765/api/catalog').status==401
            page.locator('#token').fill('example-fixture-token')
            manifest=json.loads((ROOT/'production/manifest.json').read_text())
            fixtures={'catalog':{'manifest':manifest,'episodes':[json.loads((ROOT/'episodes/001.json').read_text())],'schedule':json.loads((ROOT/'production/studio_schedule.json').read_text())},'runs':[],'videos':[]}
            page.route('**/api/*',lambda route:route.fulfill(json=fixtures.get(route.request.url.rsplit('/',1)[-1],{})))
            page.get_by_role('button',name='Connect securely').click()
            page.get_by_role('button',name='Render for review').wait_for()
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert page.evaluate('localStorage.length === 0 && sessionStorage.length === 0')
            page.get_by_role('button',name='Schedule',exact=True).click();page.get_by_role('heading',name='Day 30',exact=True).wait_for()
            Path('test-results').mkdir(exist_ok=True);page.screenshot(path=f'test-results/studio-{width}.png',full_page=True)
            page.get_by_role('button',name='Sign out').click();assert page.locator('#desk').is_hidden()
            assert not errors,errors
            page.close()
        browser.close()
    print('PASS: mobile/desktop layout, real unauthenticated API rejection, fixture UI navigation/logout. Live authenticated flows NOT tested.')
finally:process.terminate();process.wait(timeout=10)
