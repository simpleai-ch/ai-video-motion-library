# 梯形弹窗铺屏

适合：评论展示、观点集中出现、需求很多、消息刷屏、信息爆发。
风格：浅色、层叠、社交信息流、快节奏。节奏：快。

分类：opener；状态：recreated；规格：1080×1920 / 30fps / 4.000秒。

来源：项目试做；未确认进入成片。preview.mp4为项目已有示例；index.html为浏览器入口。Python条目的index.html仅播放预览，真正的可编辑渲染工程是render.py。

需要的新素材：每张卡片的文案与姓名。

可替换字段：lines, names, pos, starts, colors。

## 调用

读取根目录catalog.json，按名称或视频需求选择“梯形弹窗铺屏”，先复制实例，保留本条目原件：

```bash
python motion.py new "梯形弹窗铺屏" 新视频-05
python motion.py validate instances/新视频-05
python motion.py render instances/新视频-05
```

编辑实例config.json并把新素材放入assets。请随新口播替换旧音频、字幕和产品名称，勿沿用示例中的结论。默认宽高比例与节奏保留；换画幅须重新排版并检查裁切。