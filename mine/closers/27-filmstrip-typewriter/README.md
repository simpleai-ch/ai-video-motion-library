# 27 黑底打字文案与照片胶片条

分类：closer；状态：used；规格：2688×1512 / 30fps / 3.600秒。

来源：联发集团原生高清结尾。preview.mp4为项目已有示例；index.html为浏览器入口。Python条目的index.html仅播放预览，真正的可编辑渲染工程是render.py。

需要的新素材：两行收尾文案；照片列表。

可替换字段：lines, photos, film_top, film_bottom, font, audio。

## 调用

读取根目录catalog.json，找到编号27，先复制实例，保留本条目原件：

```bash
python motion.py new 27 新视频-27
python motion.py validate instances/新视频-27
python motion.py render instances/新视频-27
```

编辑实例config.json并把新素材放入assets。请随新口播替换旧音频、字幕和产品名称，勿沿用示例中的结论。默认宽高比例与节奏保留；换画幅须重新排版并检查裁切。

示例视频使用原项目字体；默认可编辑工程使用仓库Noto字体，可通过font换为已授权字体。胶片标签也可换成自己的项目名，照片按列表循环滚动。
