# 视频与声音波形展示

适合：AI视频展示、音画同步说明、生成效果演示、带声音的视频案例。
风格：黑金、清晰演示、简洁。节奏：随素材。

分类：middle；状态：used；规格：1080×1920 / 30fps / 9.467秒。

来源：工具榜单HappyHorse段。preview.mp4为项目已有示例；index.html为浏览器入口。Python条目的index.html仅播放预览，真正的可编辑渲染工程是render.py。

需要的新素材：带声音的视频片段；标题和来源文字。

可替换字段：video, audio, wave_audio, title, source_label, background, accent。

## 调用

读取根目录catalog.json，按名称或视频需求选择“视频与声音波形展示”，先复制实例，保留本条目原件：

```bash
python motion.py new "视频与声音波形展示" 新视频-17
python motion.py validate instances/新视频-17
python motion.py render instances/新视频-17
```

编辑实例config.json并把新素材放入assets。请随新口播替换旧音频、字幕和产品名称，勿沿用示例中的结论。默认宽高比例与节奏保留；换画幅须重新排版并检查裁切。