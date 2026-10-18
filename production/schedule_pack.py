import argparse,datetime,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def select(pack,today):
    start=datetime.date.fromisoformat(pack['launch_date']);index=(today-start).days
    if index<0 or index>6:return []
    return [pack['episodes'][index]]+([pack['bridges']] if index==6 else [])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--batch',action='store_true');p.add_argument('--pack',default='week-001');a=p.parse_args()
    pack=json.loads((ROOT/'packs'/f'{a.pack}.json').read_text());today=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).date()
    episodes=pack['episodes']+[pack['bridges']] if a.batch else select(pack,today)
    print('episodes='+json.dumps(episodes,separators=(',',':')))
    print('active='+str(bool(episodes)).lower())
    print('compile='+str(a.batch or (pack['bridges'] in episodes)).lower())
