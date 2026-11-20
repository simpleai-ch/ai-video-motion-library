from pathlib import Path
import argparse,json,shutil,subprocess,sys,os,re,math,array
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description='从动效库复制实例并渲染');s=p.add_subparsers(dest='cmd',required=True)
s.add_parser('list')
a=s.add_parser('search');a.add_argument('query');a.add_argument('--stage',choices=['opener','middle','closer']);a.add_argument('--limit',type=int,default=3)
a=s.add_parser('new');a.add_argument('effect');a.add_argument('name')
for name in ['validate','render']:
 a=s.add_parser(name);a.add_argument('project')
args=p.parse_args();cat=json.loads((ROOT/'catalog.json').read_text(encoding='utf-8'))['effects']
if args.cmd=='list':
 for t in cat:print(t['name'],t['category'],t['status'])
 sys.exit(0)
if args.cmd=='search':
 from tools.search_effects import search_effects
 found=search_effects(cat,args.query,args.stage,args.limit)
 if not found:print('没有明确匹配；请查看catalog.json，由AI根据内容选择或说明缺口。')
 for e,score,matched in found:print(json.dumps({'name':e['name'],'path':e['path'],'status':e['status'],'matched':matched,'use_cases':e['use_cases']},ensure_ascii=False))
 sys.exit(0)
if args.cmd=='new':
 key=args.effect.upper().lstrip('M');key=key.zfill(2) if key.isdigit() else args.effect
 t=next((x for x in cat if key==x.get('number') or args.effect in [x['id'],x['name'],*x.get('aliases',[])]),None)
 if not t:raise SystemExit('找不到该编号/名称')
 if not re.fullmatch(r'[\w\-\u4e00-\u9fff ]+',args.name):raise SystemExit('实例名只允许中文、字母、数字、空格和横线')
 dst=ROOT/'instances'/args.name
 if dst.exists():raise SystemExit('实例已存在，不覆盖')
 shutil.copytree(ROOT/t['path'],dst,ignore=shutil.ignore_patterns('reference','check-*','rendered*.mp4','preview.mp4','__pycache__'))
 print(dst)
 if t['status']=='idea':print('该条目只有参考，需要先复刻，不能直接当成已完成模板渲染')
 sys.exit(0)
d=Path(args.project).resolve()
if not d.is_relative_to(ROOT):raise SystemExit('实例需位于仓库内')
cfg=json.loads((d/'config.json').read_text(encoding='utf-8'));engine=cfg['engine'];files=[]
if engine=='reference':raise SystemExit('该标题效果为参考条目，尚无可替换文案的渲染工程；请先按README复刻。')
for k in ['audio','presenter','video','foreground_video','avatar','cover']:
 if cfg.get(k) and (k!='presenter' or cfg.get('show_presenter')):files.append(cfg[k])
files += [i['image'] for i in cfg.get('items',[])]+cfg.get('wall_images',[])+cfg.get('foreground_frames',[])+cfg.get('photos',[])+[v['file'] for v in cfg.get('clips',{}).values()]
missing=[x for x in files if not (d/x).exists()]
if missing:raise SystemExit('缺少素材：'+str(missing))
if cfg.get('motion_id')=='01' and len(cfg['items'])!=10:raise SystemExit('01当前为10个槽位，改数量需适配布局')
if args.cmd=='validate':print('素材路径与配置检查通过');sys.exit(0)
ff=os.environ.get('FFMPEG') or shutil.which('ffmpeg')
if not ff:raise SystemExit('请安装FFmpeg或设置FFMPEG环境变量')
env=os.environ.copy();env['FFMPEG']=ff;env['MOTION_REPO_ROOT']=str(ROOT)
if cfg.get('motion_id')=='17':
 raw=subprocess.check_output([ff,'-v','error','-i',str(d/cfg.get('wave_audio',cfg['video'])),'-ar','8000','-ac','1','-f','f32le','-']);a=array.array('f');a.frombytes(raw)
 if sys.byteorder!='little':a.byteswap()
 n=600;values=[]
 for i in range(n):
  part=a[len(a)*i//n:len(a)*(i+1)//n];values.append(math.sqrt(sum(x*x for x in part)/max(1,len(part))))
 (d/'wave.js').write_text('window.WAVE='+json.dumps(values)+';',encoding='utf-8')
if engine=='browser':
 node=shutil.which('node')
 if not node:raise SystemExit('请安装Node.js并运行npm install')
 subprocess.run([node,str(ROOT/'tools/render-browser.cjs'),str(d)],env=env,check=True)
else:subprocess.run([sys.executable,str(d/'render.py')],cwd=d,env=env,check=True)
