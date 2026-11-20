# AI 视频动效库

直接描述你的视频和想要的感觉，让AI从仓库选择动效。**不需要记编号，也不需要安装Skill。**

## 以后这样说

> 去 https://github.com/simpleai-ch/ai-video-motion-library 选合适的动效，帮我剪这条视频。内容是企业培训活动回顾，整体有纪实感，开头利落，结尾简洁温暖。文案和素材在……，先给动态预览。

> 给这条AI工具盘点选一个节奏快、有科技感的开头，中间重点展示视频与声音效果，结尾引导关注。

> 从库里找一个高级一点的照片回顾结尾，不要关注贴纸。

AI会按内容用途、风格、使用位置、节奏和素材需求筛选，读取具体工程，再替换为新内容。库里没有合适效果时，会说明差距，不强行套用。

## 已有的效果

|效果名称|适合什么内容|位置|状态|
|---|---|---|---|
|[暗黑科技关系网络](references/middles/ai-editor-network)|多工具协作、AI功能解释、关系说明|中间|已制作待用|
|[快闪榜单开场](mine/openers/01-ranking-flash)|工具盘点、产品榜单、多个功能介绍|开头|已用过|
|[九宫格纪实开场](mine/openers/02-grid-reveal)|培训活动、企业活动、入企服务|开头|已用过|
|[梯形弹窗铺屏](references/openers/05-trapezoid-popups)|评论展示、观点集中出现、需求很多|开头|已制作待用|
|[视频与声音波形展示](mine/middles/17-video-waveform)|AI视频展示、音画同步说明、生成效果演示|中间|已用过|
|[照片墙关注结尾](mine/closers/26-follow-wall)|引导关注、账号收尾、个人IP|结尾|已用过|
|[胶片照片谢幕](mine/closers/27-filmstrip-typewriter)|活动总结、企业培训回顾、纪录片收尾|结尾|已用过|
|[逐字聚焦标题](references/middles/32-title-focus)|短标题强调、章节标题、关键词强调|中间|参考待复刻|

## 仓库结构

- mine/openers、middles、closers：自己视频中用过的开头、中间、结尾。
- references/openers、middles、closers：参考或待用效果。
- catalog.json：AI检索目录，含风格、适合内容、素材需求、状态和路径。
- index.html：可按文字、风格、用途和位置筛选的本地预览目录。
- AGENTS.md：供AI阅读的选择与复用规则。

每项的README.md和meta.json说明如何换内容；config.json为新项目配置。Python条目的index.html只播放示例，可编辑渲染工程是render.py；浏览器条目可编辑HTML/Canvas。逐字聚焦标题目前只有参考，选用前需复刻。

## 本机运行（可交给AI执行）

视频与开源字体使用Git LFS；安装Git LFS后执行：

```bash
git clone https://github.com/simpleai-ch/ai-video-motion-library.git
cd ai-video-motion-library
git lfs pull
python -m pip install -r requirements.txt
npm install
npx playwright install chromium
python motion.py search "培训活动回顾的纪实开头"
python motion.py new "九宫格纪实开场" 新培训视频
python motion.py validate instances/新培训视频
python motion.py render instances/新培训视频
```

FFmpeg需在PATH中，或用FFMPEG环境变量指定。可用CHROME_EXECUTABLE指定已安装Chrome。运行`python -m http.server 8000`后访问http://localhost:8000/index.html浏览预览。

原模板保留，新项目位于instances，默认不提交。默认画幅不同，换画幅时需重新排版。旧编号仅用于内部兼容，旧调用仍有效。

Noto字体许可证见shared/fonts/OFL.txt，Windows系统字体不随仓库分发。示例素材不等于授权用于任意商业发布。
