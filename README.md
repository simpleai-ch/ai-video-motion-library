# 动效库 motion-library

视频用的开头 / 中间 / 结尾动效。每个动效一个文件夹，打开 `index.html` 就能播放。

## 目录结构
```
openers/   开头动效
middles/   中间动效
closers/   结尾动效
catalog.json   总目录（所有动效的类型、来源、状态、风格标签）
```

每个动效文件夹包含：
- `index.html`：动效本体（可替换内容都在顶部的 CONFIG 里）
- `meta.json`：风格总结、适用场景、可编辑字段
- `preview.gif` / `cover.png`：预览
- `README.md`：镜头顺序和时间点
- `assets/`：参考图、IP 素材等

## “自己的” vs “参考的”
不按文件夹分，而是在 `meta.json` 和 `catalog.json` 里用两个字段区分：

| 字段 | 取值 |
|---|---|
| `source` | `own` 自己做过的 · `reference` 参考别人的 |
| `status` | `idea` 只存了参考素材，还没做 · `recreated` 已复刻、可以用 · `used` 已在自己视频里用过 |

参考动效做出来、用进自己的视频后，只需要把 `status` 改成 `used`，并在 `used_in` 里记下用在哪条视频，不用挪文件夹。

## 新增一个动效
1. 在对应分类下新建文件夹，比如 `openers/neon-title/`
2. 放入 `index.html`、`meta.json`、预览图
3. 在 `catalog.json` 里加一条

## 调用方式
在对话里说“从动效库里找一个暗黑科技风的开头”，Claude 会读取 `catalog.json` 按标签筛选，取出对应的动效，按新视频的内容修改 CONFIG，然后导出视频。
