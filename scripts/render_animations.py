from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, os
from functools import lru_cache
OUT=Path(__file__).resolve().parents[1]/'assets'; W,H=1080,330; S=2
BG='#101013'; FG='#eee4d9'; RED='#cf817b'; HOT='#f2b2a1'; DIM='#a99b96'; MUT='#79504f'; LINE='#493335'; PANEL='#1d1519'; GOLD='#bca17c'
@lru_cache(None)
def F(n,k):return ImageFont.truetype({'m':'/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf','b':'/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf','r':'/usr/share/fonts/opentype/inter/Inter-Regular.otf'}[k],n*S)
def p(pt):return tuple(round(v*S) for v in pt)
def txt(d,x,y,s,n=16,c=FG,k='m',a=None):d.text(p((x,y)),s,font=F(n,k),fill=c,anchor=a)
def ln(d,pts,c=LINE,w=1):d.line([p(a) for a in pts],fill=c,width=max(1,round(w*S)),joint='curve')
def el(d,b,fill=None,outline=None,w=1):d.ellipse(p(b),fill=fill,outline=outline,width=max(1,round(w*S)))
def circle(d,x,y,r,fill=None,outline=None,w=1):el(d,(x-r,y-r,x+r,y+r),fill,outline,w)
def poly(d,pts,fill=None,outline=None,w=1):
 if fill:d.polygon([p(a) for a in pts],fill=fill)
 if outline:ln(d,pts+[pts[0]],outline,w)
def rect(d,b,fill=None,outline=None,w=1,r=0):d.rounded_rectangle(p(b),radius=r*S,fill=fill,outline=outline,width=max(1,round(w*S)))
def arc(d,b,a,z,c,w=1):d.arc(p(b),a,z,fill=c,width=max(1,round(w*S)))
def pol(x,y,r,a):return x+r*math.cos(a),y+r*math.sin(a)
def mix(a,b,t):return '#'+''.join(f'{round(int(a[i:i+2],16)*(1-t)+int(b[i:i+2],16)*t):02x}' for i in (1,3,5))
def icon(d,kind,t):
 x,y=148,162; a=t*math.tau*2-math.pi/2
 if kind=='sentinel':
  pts=[(148,69),(223,99),(223,164),(215,191),(192,214),(148,239),(104,214),(81,191),(73,164),(73,99)]
  poly(d,pts,PANEL,RED,1.8);poly(d,[(148+(xx-148)*.84,162+(yy-162)*.84) for xx,yy in pts],None,MUT,1)
  for r in (20,40,58):circle(d,x,y,r,None,MUT,1.1)
  ln(d,[(x-65,y),(x+65,y)],MUT);ln(d,[(x,y-65),(x,y+65)],MUT)
  for k in range(20):ln(d,[(x,y),pol(x,y,58,a-k*.033)],mix(PANEL,RED,(1-k/20)*.42),1.2)
  ln(d,[(x,y),pol(x,y,58,a)],HOT,1.6);circle(d,x,y,3,HOT)
  for bx,by in [(177,130),(119,179),(180,189)]:
   age=((a-math.atan2(by-y,bx-x))%math.tau)/math.tau; v=math.exp(-age*4);circle(d,bx,by,3,mix(MUT,HOT,v));circle(d,bx,by,6+3*v,None,mix(PANEL,RED,v),1)
 elif kind=='arquivini':
  # stack of three embossed cylindrical data vaults
  for j in range(2,-1,-1):
   yy=97+j*39;rect(d,(84,yy,212,yy+39),PANEL,RED,1.5);el(d,(84,yy+21,212,yy+57),PANEL,RED,1.5);el(d,(84,yy-18,212,yy+18),PANEL,RED,1.5);arc(d,(93,yy-13,203,yy+13),10,170,MUT)
   for k in range(3):ln(d,[(98+k*7,yy+21),(98+k*7,yy+26)],MUT)
   circle(d,201,yy+21,3,mix(MUT,HOT,.5+.5*math.cos(math.tau*(t*2-j/3))))
  circle(d,*pol(x,97,1,0),1,RED);circle(d,148+62*math.cos(a),97+17*math.sin(a),3,HOT)
  rect(d,(126,179,170,222),BG,RED,1.7,4);arc(d,(133,162,163,194),180,360,RED,2);ln(d,[(133,177),(133,179)],RED,2);ln(d,[(163,177),(163,179)],RED,2);circle(d,148,196,4,HOT);ln(d,[(148,199),(148,207)],HOT,1.6)
 elif kind=='boot':
  for i in range(16):
   b=i*math.tau/16;poly(d,[pol(x,y,80,b-.075),pol(x,y,91,b-.075),pol(x,y,91,b+.075),pol(x,y,80,b+.075)],PANEL,MUT)
  circle(d,x,y,80,None,RED,1.4);circle(d,x,y,72,None,MUT)
  poly(d,[pol(x,y,66,math.pi/6+i*math.tau/6) for i in range(6)],PANEL,RED,1.2)
  # symmetrical drop with cubic curves
  def bez(a,b,c,e):return [((1-u)**3*a[0]+3*(1-u)**2*u*b[0]+3*(1-u)*u*u*c[0]+u**3*e[0],(1-u)**3*a[1]+3*(1-u)**2*u*b[1]+3*(1-u)*u*u*c[1]+u**3*e[1]) for u in [i/30 for i in range(31)]]
  pts=bez((148,105),(134,129),(111,148),(111,175))+bez((111,175),(111,221),(185,221),(185,175))+bez((185,175),(185,148),(162,129),(148,105));poly(d,pts,mix('#402125','#783b3d',(.5+.5*math.sin(t*math.tau*2))*.65),RED,1.7);txt(d,148,174,'B+',30,FG,'b','mm');arc(d,(53,67,243,257),math.degrees(a),math.degrees(a)+42,HOT,2)
 else:
  rect(d,(84,85,212,238),PANEL,RED,1.6,6);rect(d,(92,93,204,230),None,MUT,1,3);circle(d,148,132,22,None,RED,1.5);arc(d,(109,156,187,221),180,360,RED,1.5);ln(d,[(109,188),(109,198),(187,198),(187,188)],RED,1.5)
  for i in range(3):ln(d,[(103,208+i*6),(194-(i%2)*12,208+i*6)],MUT)
  yy=100+122*(.5-.5*math.cos(t*math.tau));ln(d,[(94,yy),(202,yy)],HOT,1.4);circle(d,202,yy,3,HOT)

def render(kind,title,tag,serial,sub,quote,steps):
 im=Image.new('RGB',(W*S,H*S),BG);d=ImageDraw.Draw(im);rect(d,(1,1,W-2,H-2),None,LINE,1,8)
 for x,y,sx,sy in [(13,13,1,1),(W-14,13,-1,1),(13,H-14,1,-1),(W-14,H-14,-1,-1)]:ln(d,[(x,y+sy*13),(x,y),(x+sx*13,y)],RED)
 ln(d,[(295,26),(295,305)],LINE);ln(d,[(316,59),(1046,59)],LINE);txt(d,317,24,tag,13,RED);txt(d,1046,24,serial,13,GOLD,a='ra');txt(d,315,73,title,42,FG,'b');txt(d,317,127,sub,18,DIM,'r');ln(d,[(317,159),(1046,159)],LINE)
 xs=[334+i*692/(len(steps)-1) for i in range(len(steps))];ln(d,[(xs[0],196),(xs[-1],196)],MUT)
 for i,(x,(a,b)) in enumerate(zip(xs,steps)):
  circle(d,x,196,7,BG,MUT,1.4);txt(d,x,177,f'{i+1:02}',12,DIM,a='mm');anchor='la' if i==0 else 'ra' if i==len(xs)-1 else 'ma';txt(d,x,214,a,17,FG,'b',anchor);txt(d,x,239,b,13,DIM,'m',anchor)
 ln(d,[(317,268),(1046,268)],LINE);txt(d,317,283,quote,17,RED,'r');txt(d,1046,308,'ILLUSTRATIVE / B+',10,MUT,a='ra');txt(d,148,25,'NOOSPHERIC ARCHIVE',11,MUT,a='ma');txt(d,148,293,'B.POSITIVE  //  '+serial.split('/')[-1].strip(),11,RED,a='ma')
 for i in range(48):
  a=i*math.tau/48;ln(d,[pol(148,162,108 if i%4==0 else 112,a),pol(148,162,115,a)],MUT if i%4==0 else LINE)
 circle(d,148,162,103,None,LINE);circle(d,148,162,98,None,'#2c2326')
 for a in (0,math.pi/2,math.pi,math.pi*1.5):ln(d,[pol(148,162,107,a),pol(148,162,120,a)],RED)
 # 120 evenly spaced frames: 6 seconds, 20 fps; fixed typography, no slide changes.
 frames=[];N=120
 for j in range(N):
  t=j/N;f=im.copy();d=ImageDraw.Draw(f);icon(d,kind,t);u=t*(len(xs)-1);x=xs[0]+(xs[-1]-xs[0])*t;fade=min(1,t*12,(1-t)*12)
  for k in range(10,0,-1):
   xx=max(xs[0],x-k*4);ln(d,[(xx,196),(min(x,xx+4),196)],mix(MUT,HOT,fade*(1-k/11)*.85),2)
  if fade>0:circle(d,x,196,3.7,mix(MUT,HOT,fade))
  for i,xx in enumerate(xs):
   q=math.exp(-((u-i)/.22)**2)*fade
   if q>.03:circle(d,xx,196,7,BG,mix(MUT,HOT,q),1.6);circle(d,xx,196,2.4,mix(MUT,HOT,q))
  frames.append(f.resize((W,H),Image.Resampling.LANCZOS))
 atlas=Image.new('RGB',(W,H*5))
 for i in range(5):atlas.paste(frames[i*N//5],(0,i*H))
 pal=atlas.quantize(colors=256);q=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in frames];q[0].save(OUT/(kind+'.gif'),save_all=True,append_images=q[1:],duration=50,loop=0,optimize=True,disposal=1);frames[40].save(OUT/(kind+'-preview.png'));print(kind,(OUT/(kind+'.gif')).stat().st_size,flush=True)
if __name__=='__main__':
 render('sentinel','SentinelForge','STC-001  /  DETECTION ENGINEERING','STC / 001','Event-driven telemetry and threat detection','Detect the heresy. Preserve the evidence.',[('Ingest','FastAPI'),('Raw event','DB → Kafka'),('Normalize','DB → Kafka'),('Detect','Alerts + evidence')])
 render('arquivini','ArquiVini','STC-002  /  DATA INTEGRITY','STC / 002','Spring Boot contact API and relational integrity','The sacred constraints shall not be violated.',[('Request','REST API'),('Validate','Jakarta'),('Service','Transaction'),('Persist','PostgreSQL')])
 render('boot','Rite of initialization','B.POSITIVE  /  PERSONAL TERMINAL','B+ / 000','Backend engineering · Distributed systems · Security','Praise the Omnissiah. Run the tests.',[('Runtime','Python / Java'),('Data','PostgreSQL'),('Events','Kafka'),('Observe','Metrics')])
 render('identity','Identity & Access','STC-003  /  SECURITY RESEARCH','STC / 003','Academic research · IAM and IT governance','Trust is earned. Access is audited.',[('Assess','Current access'),('Identify','Risks'),('Evaluate','IAM controls'),('Recommend','Improvement')])
