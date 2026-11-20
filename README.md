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
