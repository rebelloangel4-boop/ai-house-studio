"""Original music and synchronized synthesized effects; no external samples."""
import math
import numpy as np
SR=24000

def mix(audio,duration,scene,lead):
 n=math.ceil(duration*SR);music=np.zeros((n,2));fx=np.zeros((n,2));voice=np.zeros(n)
 rng=np.random.default_rng(sum(map(ord,scene['phase'])))
 def put(target,start,wave,level=.1,pan=0):
  at=max(0,int(start*SR));count=min(len(wave),n-at)
  if count>0:target[at:at+count]+=wave[:count,None]*np.array([1-pan*.35,1+pan*.35])[None,:]*level
 def note(freq,length=.3):
  u=np.arange(int(length*SR))/SR
  return (np.sin(2*np.pi*freq*u)+.22*np.sin(4*np.pi*freq*u))*np.exp(-u*10)*np.minimum(1,u/.006)
 # Bouncy minor jazz harmony, bass and brushed rhythm. Musical attacks are softened.
 for j,start in enumerate(np.arange(0,duration,.46)):
  root=[146.83,174.61,130.81,164.81][(j//4)%4]
  put(music,start,note(root,.42),.026,-.3)
  if j%2==0:
   for interval in (1,1.1892,1.4983,1.7818):put(music,start+.04,note(root*2*interval,.38),.008,.45)
  u=np.arange(int(.12*SR))/SR
  hat=rng.standard_normal(len(u))*np.exp(-u*55)
  put(music,start+.23,hat,.006,.4)
  kick=np.sin(2*np.pi*(65*u-100*u*u))*np.exp(-u*35)
  put(music,start,kick,.035)
 def impact(start=0):
  u=np.arange(int(.35*SR))/SR
  put(fx,start,np.sin(2*np.pi*(90*u-75*u*u))*np.exp(-u*12),.15)
 def chime(start=0):
  for j,f in enumerate((880,1108.73,1318.51)):put(fx,start+j*.07,note(f,.32),.055,.3)
 def whoosh(start=0):
  u=np.arange(int(.22*SR))/SR;noise=rng.standard_normal(len(u))
  noise=np.convolve(noise,np.ones(9)/9,'same')*np.sin(np.pi*u/.22)**2
  put(fx,start,noise,.09,-.3)
 phase=scene['phase'];theme=scene['theme']
 cues=[]
 whoosh(0);cues.append({'effect':'transition_whoosh','time':0})
 if phase in ('offer','cash','buy','card','elected','gold','reveal','owned'):
  chime(.1);cues.append({'effect':'cash_or_reveal_chime','time':.1})
 if phase in ('door','alarm','crash','fired','error','expired','delete','tear'):
  impact(.05);cues.append({'effect':'cinematic_impact','time':.05})
 if phase in ('phone','invoice','pay','report','badge'):
  chime(.12);cues.append({'effect':'notification','time':.12})
 if phase in ('eat','chase','paper','crumbs'):
  for at in np.arange(.25,duration-.15,.4):
   u=np.arange(int(.09*SR))/SR
   put(fx,at,rng.standard_normal(len(u))*np.exp(-u*50),.028)
   cues.append({'effect':'cartoon_crunch','time':round(float(at),3)})
 if phase in ('countdown','battery','alarm'):
  for at in np.arange(.1,duration,.5):
   put(fx,at,note(1400,.065),.03);cues.append({'effect':'timer_tick','time':round(float(at),3)})
 if theme in ('simulation','future'):
  for at in (.05,.18):put(fx,at,note(95,.08),.05)
 if phase=='choice':
  # Silence music for the opening of the question, then a gentle unresolved cadence.
  music[:min(n,int(.28*SR))]*=0
 a=int(lead*SR);b=min(n,a+len(audio));voice[a:b]=audio[:b-a]
 # Signal-driven ducking with smooth attack/release prevents abrupt volume jumps.
 rms=np.sqrt(np.convolve(voice*voice,np.ones(960)/960,'same'))
 target=np.where(rms>.009,.22,1.0);gain=np.ones(n);g=1.
 for i,v in enumerate(target):
  coef=.004 if v<g else .00016;g+=coef*(v-g);gain[i]=g
 music*=gain[:,None]
 fade=np.minimum(1,np.arange(n)/(SR*.008))*np.minimum(1,(n-np.arange(n))/(SR*.035))
 result=(voice[:,None]+music+fx)*fade[:,None]
 if np.max(np.abs(result))>=.99:raise ValueError('Unmastered mix clips')
 return result,cues
