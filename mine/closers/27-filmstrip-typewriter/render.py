from pathlib import Path
import json,os,shutil
P=Path(__file__).parent;cfg=json.loads((P/'config.json').read_text(encoding='utf-8'));W,H=cfg['width'],cfg['height'];S=W/1920
FF=os.environ.get('FFMPEG') or shutil.which('ffmpeg') or 'ffmpeg'
FONT=cfg.get('font') or str(next(p/'shared/fonts/NotoSerifCJKsc-Bold.otf' for p in [Path(os.environ.get('MOTION_REPO_ROOT',P)),*P.parents] if (p/'shared/fonts/NotoSerifCJKsc-Bold.otf').exists()))

from PIL import Image,ImageOps,ImageDraw,ImageFont
import subprocess
def sc(x):return round(x*S)
names=cfg['photos']
imgs=[ImageOps.fit(ImageOps.exif_transpose(Image.open(P/n)).convert('RGB'),(sc(606),sc(350)),method=Image.Resampling.LANCZOS) for n in names]
font=ImageFont.truetype(FONT,sc(48));small=ImageFont.truetype(FONT,sc(15));lines=cfg['lines']
enc=subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','14','-pix_fmt','yuv420p','-video_track_timescale','30000',str(P/'rendered-picture.mp4')],stdin=subprocess.PIPE)
for f in range(cfg['duration_frames']):
 t=f/30;im=Image.new('RGB',(W,H),'black');d=ImageDraw.Draw(im);remaining=int(max(0,t-.15)*22)
 for j,line in enumerate(lines):
  shown=line[:max(0,remaining)];remaining-=len(line);x=sc(245);y=sc([430,570][j])
  for ch in shown:d.text((x,y),ch,font=font,fill=(245,242,232));x+=d.textlength(ch,font=font)+sc(6.7)
 stripx=sc(1130);d.rectangle((stripx,0,sc(1830),H),fill=(31,27,22));offset=t*sc(420)
 for k in range(-1,6):
  idx=int(offset//sc(420))+k;y=int(k*sc(420)-offset%sc(420));im.paste(imgs[idx%len(names)],(stripx+sc(47),y+sc(36)));d.text((stripx+sc(48),y+sc(8)),cfg['film_top']+f'     {idx%len(names)+1:02d}',font=small,fill=(208,166,80));d.text((stripx+sc(48),y+sc(393)),cfg['film_bottom'],font=small,fill=(208,166,80))
 for y in range(-sc(40),H+sc(40),sc(42)):
  yy=y-int(offset%sc(42))
  for x in (stripx+sc(10),stripx+sc(675)):d.rounded_rectangle((x,yy,x+sc(15),yy+sc(24)),radius=sc(3),fill=(225,221,210))
 if t>3.2:im=Image.blend(Image.new('RGB',(W,H)),im,max(0,1-(t-3.2)/.4))
 enc.stdin.write(im.tobytes())
enc.stdin.close();assert enc.wait()==0
print('Native ending ready',flush=True)

subprocess.run([FF,'-y','-v','error','-i',str(P/'rendered-picture.mp4'),'-i',str(P/cfg['audio']),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(cfg['duration_frames']/cfg['fps']),'-movflags','+faststart',str(P/'rendered.mp4')],check=True)
