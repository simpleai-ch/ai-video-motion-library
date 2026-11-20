# 26 封面墙与头像上升点击关注

分类：closer；状态：used；规格：1080×1920 / 30fps / 4.467秒。

来源：工具榜单v10、LibTV结尾。preview.mp4为项目已有示例；index.html为浏览器入口。Python条目的index.html仅播放预览，真正的可编辑渲染工程是render.py。

需要的新素材：封面图片；可选新头像；可选新点击前景序列与音效。

可替换字段：wall_images, wall_opacity, avatar, foreground_frames, rise_frames, audio。

## 调用

读取根目录catalog.json，找到编号26，先复制实例，保留本条目原件：

```bash
python motion.py new 26 新视频-26
python motion.py validate instances/新视频-26
python motion.py render instances/新视频-26
```

编辑实例config.json并把新素材放入assets。请随新口播替换旧音频、字幕和产品名称，勿沿用示例中的结论。默认宽高比例与节奏保留；换画幅须重新排版并检查裁切。

avatar=null时保留示例原头像；设置图片路径后替换圆形头像，手指/红勾保留原片动作。foreground_frames若替换为另一段，须适配paint10蒙版，不能只换路径。wall_opacity默认0.24，rise_frames默认16。

点击动作以透明WebP帧序列保存，确保浏览器和导出逐帧一致。替换foreground_frames时保持画幅420×650及头像/贴纸位置。
