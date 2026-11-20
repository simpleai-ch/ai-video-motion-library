# AI 视频动效库 ai-video-motion-library

AI 剪辑用的动效模板：开头 / 中间 / 结尾。每个动效一个文件夹，浏览器打开 `index.html` 就能播放，文字、颜色、时长可以在顶部的 CONFIG 里改。

## 目录结构
```
mine/              自己视频里做过、用过的动效
  openers/         开头
  middles/         中间
  closers/         结尾
references/        参考别人视频的动效（已复刻或待复刻）
  openers/
  middles/
  closers/
catalog.json       总目录：所有动效的位置、来源、状态、风格标签
```

每个动效文件夹包含：
- `index.html`：动效本体（可替换内容在顶部的 CONFIG 里）
- `meta.json`：风格总结、适用场景、可编辑字段
- `preview.gif` / `cover.png`：预览
- `README.md`：镜头顺序和时间点
- `assets/`：参考图、IP 素材等

## 状态字段
`catalog.json` 和 `meta.json` 里的 `status`：
- `idea`：只存了参考素材，还没做
- `recreated`：已复刻，可以用
- `used`：已在自己视频里用过（同时在 `used_in` 记下视频名）

参考动效用进自己的视频后，复制一份到 `mine/` 对应分类下，作为自己的版本。

## 新增一个动效
1. 先判断是自己的（`mine/`）还是参考的（`references/`），再选开头 / 中间 / 结尾
2. 新建文件夹，放入 `index.html`、`meta.json`、预览图
3. 在 `catalog.json` 里加一条

## 调用方式
在对话里说“从动效库里找一个暗黑科技风的开头”，Claude 读取 `catalog.json` 按标签筛选，取出动效，按新视频内容改 CONFIG，再导出视频。


## 已加入的编号动效（2026-11-20）

不需要安装Skill。下次把本仓库链接和编号交给AI即可；AI先读catalog.json及AGENTS.md，再复制模板替换内容。

|编号|动效|分类|状态|预览与工程|
|---|---|---|---|---|
|01|工具榜单快闪与卡片归位|opener|used|[查看](mine/openers/01-ranking-flash)|
|02|九宫格展开与相框掉落|opener|used|[查看](mine/openers/02-grid-reveal)|
|05|梯形卡片由上到下展开铺屏|opener|recreated|[查看](references/openers/05-trapezoid-popups)|
|17|上方视频与下方动态音频波形|middle|used|[查看](mine/middles/17-video-waveform)|
|26|封面墙与头像上升点击关注|closer|used|[查看](mine/closers/26-follow-wall)|
|27|黑底打字文案与照片胶片条|closer|used|[查看](mine/closers/27-filmstrip-typewriter)|
|32|标题逐字从大且模糊收缩清晰|middle|idea|[查看](references/middles/32-title-focus)|

### 下次直接这样说

> 从 https://github.com/simpleai-ch/ai-video-motion-library 调用01做开头、17做中间展示、26做结尾。新文案是……，素材路径是……，输出9:16，先给动态预览。

> 按仓库32的参考效果复刻标题“……”，先出预览。

### 本机运行

安装Git LFS后克隆（视频及开源字体使用LFS存储），再安装运行依赖：

```bash
git clone https://github.com/simpleai-ch/ai-video-motion-library.git
cd ai-video-motion-library
git lfs pull
python -m pip install -r requirements.txt
npm install
npx playwright install chromium
python motion.py list
python motion.py new 01 我的新视频
python motion.py validate instances/我的新视频
python motion.py render instances/我的新视频
```

FFmpeg需在PATH中，或设置FFMPEG环境变量为可执行文件路径。可用CHROME_EXECUTABLE指定已安装的Chrome。用`python -m http.server 8000`后打开http://localhost:8000/index.html浏览目录；浏览器条目可通过各自index.html播放，修改config.json后执行渲染会同步配置。

Python条目02/27的index.html是预览播放器，可编辑渲染程序为render.py；01/05/17/26为HTML/Canvas模板。32仅为参考，不提供假定已完成的复刻工程。新实例保存在instances，默认不提交到仓库。

媒体与模板代码分开维护；示例素材不等于授权用于任意商业发布。Noto字体许可证见shared/fonts/OFL.txt；Windows系统字体不随仓库分发。
