from pathlib import Path
import json,os,shutil
P=Path(__file__).parent
cfg=json.loads((P/'config.json').read_text(encoding='utf-8'))
FF=os.environ.get('FFMPEG') or shutil.which('ffmpeg') or 'ffmpeg'
W,H=cfg['width'],cfg['height'];S=W/1920
files={k:str(P/v['file']) for k,v in cfg['clips'].items()}

from PIL import Image,ImageDraw,ImageFont,ImageEnhance,ImageOps
import subprocess,io
C,R=W//3,H//3
def size(n):return round(n*S)
def font(n):return ImageFont.truetype(cfg.get('font') or ('C:/Windows/Fonts/simfang.ttf' if Path('C:/Windows/Fonts/simfang.ttf').exists() else str(next(p/'shared/fonts/NotoSerifCJKsc-Bold.otf' for p in [Path(os.environ.get('MOTION_REPO_ROOT',P)),*P.parents] if (p/'shared/fonts/NotoSerifCJKsc-Bold.otf').exists()))),size(n))
def serif(n):return ImageFont.truetype('C:/Windows/Fonts/times.ttf' if Path('C:/Windows/Fonts/times.ttf').exists() else str(next(p/'shared/fonts/NotoSerifCJKsc-Bold.otf' for p in [Path(os.environ.get('MOTION_REPO_ROOT',P)),*P.parents] if (p/'shared/fonts/NotoSerifCJKsc-Bold.otf').exists())),size(n))
def ease(t):t=max(0,min(1,t));return t*t*(3-2*t)
class Reader:
 def __init__(self,id,start,w,h,count):self.id=id;self.start=start;self.w=w;self.h=h;self.count=count;self.proc=None;self.last=-1;self.im=None
 def get(self,n):
  n=min(self.count-1,max(0,n))
  if n==self.last:return self.im.copy()
  if self.proc is None or n<self.last:
   if self.proc:self.proc.stdout.close();self.proc.terminate();self.proc.wait()
   self.proc=subprocess.Popen([FF,'-v','error','-threads','1','-ss',str(self.start+n/30),'-stream_loop','-1','-i',files[self.id],'-map','0:v:0','-vf',f'fps=30,scale={self.w}:{self.h}:flags=lanczos:force_original_aspect_ratio=increase,crop={self.w}:{self.h}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
   self.last=n-1
  while self.last<n:
   data=self.proc.stdout.read(self.w*self.h*3);assert len(data)==self.w*self.h*3,(self.id,n);self.im=Image.frombytes('RGB',(self.w,self.h),data);self.last+=1
  return self.im.copy()
 def close(self):
  if self.proc:self.proc.stdout.close();self.proc.terminate();self.proc.wait()
ids=[f'g{i}' for i in range(9)]
g=[Reader(id,cfg['clips'][id]['start'],C,R,cfg['clips'][id]['count']) for id in ids]
readers={k:Reader(k,v['start'],W,H,v['count']) for k,v in cfg['clips'].items() if not k.startswith('g')}

def frame(k,n):return readers[k].get(n)
first={4:134,3:145,5:145,2:148,6:148,1:150,7:150,0:153,8:153};second={4:174,3:179,0:181,1:184,2:186,5:189,8:191,7:193,6:195}
photo=ImageOps.exif_transpose(Image.open(P/cfg['cover'])).convert('RGB').crop(tuple(cfg['cover_crop'])).resize((W,H),Image.Resampling.LANCZOS)
def title(im):
 d=ImageDraw.Draw(im)
 for x,y,tx,fs in [(cfg['title_position'][0],cfg['title_position'][1],cfg['title'][0],74),(cfg['title_position'][0],cfg['title_position'][1]+92,cfg['title'][1],57),(cfg['title_position'][0]+2,cfg['title_position'][1]+171,cfg['title'][2],22)]:d.text((size(x),size(y)),tx,font=font(fs),fill='white')
 return im
def reveal(im,tile,j,p):
 tw=max(1,int(C*p));th=max(1,int(R*p));ox=C-tw if j%3==0 else 0 if j%3==2 else (C-tw)//2;oy=R-th if j//3==0 else 0 if j//3==2 else (R-th)//2
 z=1+.09*(1-p);big=tile.resize((int(C*z),int(R*z)),Image.Resampling.LANCZOS);tile=big.crop(((big.width-C)//2,(big.height-R)//2,(big.width+C)//2,(big.height+R)//2));im.paste(tile.crop((ox,oy,ox+tw,oy+th)),(j%3*C+ox,j//3*R+oy))
def grid(im):
 layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer)
 for x in (C,C*2):d.line((x,0,x,H),fill=(255,255,255,100),width=2)
 for y in (R,R*2):d.line((0,y,W,y),fill=(255,255,255,100),width=2)
 return Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')
photos=[]
for j in [0,1,2,5,6,8,7,3]:
 # Build large photo cards from the original full-resolution frame, never from a grid tile.
 raw=subprocess.check_output([FF,'-v','error','-ss',str(cfg['clips'][ids[j]]['start']+35/30),'-i',files[ids[j]],'-map','0:v:0','-frames:v','1','-vf',f'scale={size(1094)}:{size(684)}:flags=lanczos:force_original_aspect_ratio=increase,crop={size(1094)}:{size(684)}','-f','image2pipe','-c:v','png','-'])
 ph=Image.new('RGB',(size(1150),size(790)),'white');ph.paste(Image.open(io.BytesIO(raw)),(size(28),size(28)));photos.append(ph)
enc=subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','14','-pix_fmt','yuv420p','-video_track_timescale','30000',str(P/'rendered-picture.mp4')],stdin=subprocess.PIPE)
for idx,f in enumerate(list(range(cfg['cover_hold_frames']))+list(range(cfg['source_transition_start'],cfg['source_end_frame']))):
 if f<174:
  im=title(photo.copy())
  for j,t in first.items():
   if f>=t:
    tile=g[j].get(f-t)
    if j==4:
     tile=ImageEnhance.Brightness(tile).enhance(.4);d=ImageDraw.Draw(tile)
     for x,y,tx,ft in [(28,32,cfg['center_title'][0],serif(62)),(28,112,cfg['center_title'][1],font(54)),(30,202,cfg['center_title'][2],font(32))]:d.text((size(x),size(y)),tx,font=ft,fill='white')
    reveal(im,tile,j,ease((f-t+1)/5))
 elif f<222:
  im=Image.new('RGB',(W,H))
  for j in range(9):im.paste(g[j].get(f-first[j]),(j%3*C,j//3*R))
  src=frame('whole',f-174)
  for j,t in second.items():
   if f>=t:
    x=j%3*C;y=j//3*R;reveal(im,src.crop((x,y,x+C,y+R)),j,ease((f-t+1)/3))
 elif f<247:
  im=frame('walk',f-222)
  if f<228:im=Image.blend(frame('whole',f-174),im,(f-221)/6)
 elif f<297:
  im=frame('walk',f-222);src=frame('next',f-247);ww=int(C+(W-C)*ease((f-247)/10));x=(W-ww)//2;im.paste(src.crop((x,R,x+ww,R*2)),(x,R))
  for j,t in {6:264,8:267,7:270,1:273,0:279,2:282}.items():
   p=ease((f-t)/3)
   if p>0:
    x=j%3*C;y=j//3*R;hh=int(R*p);im.paste(src.crop((x,y,x+C,y+hh)),(x,y))
 else:
  im=frame('next',f-247)
  for j,t in {4:297,5:300,3:302}.items():
   if f>=t:im.paste(g[j].get(f-t),(j%3*C,R))
  if f>=305:
   ww=int(W*ease((f-304)/7));x=(W-ww)//2;im.paste(frame('lead',f-305).crop((x,0,x+ww,R)),(x,0));im.paste(frame('whole',f-305).crop((x,R*2,x+ww,H)),(x,R*2))
 if cfg.get('grid_lines',False):im=grid(im)
 if f>=321:
  if f>=337:im=frame('base',75+f-337)
  layer=im.convert('RGBA');poses=[(-100,70,-17),(850,-70,11),(1820,40,20),(-120,850,13),(900,1050,-10),(1860,920,-17),(500,550,15),(1390,570,-15)]
  for k,(cx,cy,angle) in enumerate(poses):
   p=ease((f-320-k*.14)/4);fall=max(0,(f-336-k*.25)/12);dx=(cx-960)*1.4*(1-p);dy=(-1250 if cy<400 else 1300)*(1-p)+2100*fall*fall;ph=photos[k].convert('RGBA').rotate(angle+(1-p)*12+fall*6,resample=Image.Resampling.BICUBIC,expand=True);layer.alpha_composite(ph,(int(size(cx+dx)-ph.width/2),int(size(cy+dy)-ph.height/2)))
  im=layer.convert('RGB')
 if f in [0,153,195,328,344]:im.save(P/f'opening-{f}-native.png')
 enc.stdin.write(im.tobytes())
 if idx%40==0:print('Native opening',idx,flush=True)
enc.stdin.close();assert enc.wait()==0
for r in list(readers.values())+g:r.close()
print('Native opening ready',flush=True)

N=cfg['cover_hold_frames']+cfg['source_end_frame']-cfg['source_transition_start']
subprocess.run([FF,'-y','-v','error','-i',str(P/'rendered-picture.mp4'),'-i',str(P/cfg['audio']),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(N/30),'-movflags','+faststart',str(P/'rendered.mp4')],check=True)
