# AI动效库调用约定

先读取catalog.json，按number、aliases、category、source、status筛选，再读对应README.md及meta.json。
用户可直接说“调用01”“调用26”或提供仓库链接与编号。不需要安装Skill；勿把旧演示文案与字幕照搬到新片。
用motion.py new创建instances内副本；替换config.json和assets后validate、render。保留mine及references原件，输出位于实例rendered.mp4。
used=已在项目成片出现；recreated=已制作但未确认用于成片；idea=只有参考，需先复刻预览，不能称作可直接渲染模板。
01/02/05开头，17/32中间，26/27结尾。编号保持稳定。跨画幅需适配构图；按实际口播调整时长并检查字幕、声音和素材匹配。
新效果入库后更新meta.json、catalog.json和预览。只有实际用到用户成片后才登记used_in；参考作者/链接未知时保持待补，不编造来源。
