"""Choose seven season episodes per India-local calendar day, with manual retry."""
import datetime,json,os
today=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5,minutes=30))).date()
batches={datetime.date(2026,10,20):range(9,16),datetime.date(2026,10,21):range(16,23),datetime.date(2026,10,22):range(23,30),datetime.date(2026,10,23):range(30,31)}
day=os.environ.get('BATCH_DATE','').strip()
if day:today=datetime.date.fromisoformat(day)
episodes=[f'{n:03}' for n in batches.get(today,[])]
with open(os.environ['GITHUB_OUTPUT'],'a') as f:
    f.write('episodes='+json.dumps(episodes)+'\n')
    f.write('active='+str(bool(episodes)).lower()+'\n')
print(f'Batch date {today}: {episodes}')
