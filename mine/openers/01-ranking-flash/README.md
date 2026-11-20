# 快闪榜单开场

适合：工具盘点、产品榜单、多个功能介绍、快速吸引注意力。
风格：黑金、科技感、信息密集、快节奏。节奏：快。

分类：opener；状态：used；规格：1080×1920 / 30fps / 5.200秒。

来源：工具榜单v10。preview.mp4为项目已有示例；index.html为浏览器入口。Python条目的index.html仅播放预览，真正的可编辑渲染工程是render.py。

需要的新素材：10张图片和对应名称/编号；可选人物视频；新口播音频与字幕。

可替换字段：items, heading, subheading, captions, presenter, show_presenter, audio, timing。

## 调用

读取根目录catalog.json，按名称或视频需求选择“快闪榜单开场”，先复制实例，保留本条目原件：

```bash
python motion.py new "快闪榜单开场" 新视频-01
python motion.py validate instances/新视频-01
python motion.py render instances/新视频-01
```

编辑实例config.json并把新素材放入assets。请随新口播替换旧音频、字幕和产品名称，勿沿用示例中的结论。默认宽高比例与节奏保留；换画幅须重新排版并检查裁切。