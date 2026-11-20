# 02 九宫格展开与相框掉落

分类：opener；状态：used；规格：2688×1512 / 30fps / 7.333秒。

来源：联发集团最终修订版。preview.mp4为项目已有示例；index.html为浏览器入口。Python条目的index.html仅播放预览，真正的可编辑渲染工程是render.py。

需要的新素材：封面照片和标题；9路格子视频；5路整画面片段。

可替换字段：cover, cover_crop, title, title_position, center_title, clips, audio, grid_lines。

## 调用

读取根目录catalog.json，找到编号02，先复制实例，保留本条目原件：

```bash
python motion.py new 02 新视频-02
python motion.py validate instances/新视频-02
python motion.py render instances/新视频-02
```

编辑实例config.json并把新素材放入assets。请随新口播替换旧音频、字幕和产品名称，勿沿用示例中的结论。默认宽高比例与节奏保留；换画幅须重新排版并检查裁切。

本版为2688×1512原生版，grid_lines=false；不加九宫格白色分割线，相框自身白边保留。中文字体优先系统仿宋，可在font中指定字体路径；跨系统使用仓库开源Noto替代。
