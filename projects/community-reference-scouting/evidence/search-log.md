# 检索与覆盖日志

检索窗口：2026-09-15 至 2026-09-16。目的性探索，非穷尽或系统检索；不报告无法审计的命中总数。

| 检索词或入口 | 处理结果 |
| --- | --- |
| `site.biorender.com blog graphical abstract design mistakes` | S001；官方许可单独核查 S010/S018；.dev 镜像与 .com 视作同一来源 |
| `site.reddit.com scientific figures graphical abstract design` | 找到模板同质化、制作方法讨论；保留 S005–S007，排除纯推广服务帖 |
| `site.simplifiedsciencepublishing.com graphical abstract design tips` | S002；读布局段落，不采用接收率提升等无充分证据营销断言 |
| `scientific illustration blog flat 3D gradients figures` | S003/S004；排除泛 AI 生成器广告、无关计算机视觉论文 |
| `site.zhuanlan.zhihu.com 科研绘图 配色` / `科研作图配色避雷指南 千张` | 经 S012 找到 S013；正文 403，未产生规则 |
| `site.xiaohongshu.com Nature大子刊的第一张图` / 用户原链接 | S014；规范 URL 与分享 URL 均未能读取；分享令牌不写入仓库 |
| 中文 PPT 科研示意图配色结果 | S015，仅元数据；未用作已验证设计证据 |
| `Ten simple rules for designing graphical abstracts PLOS` | S008；核查许可并只保存 Fig 4/5/6 |
| S004 博客的 DOI 链接 | S009；从 publisher 下载 Fig 1，而非复制博客图片 |
| `site.help.biorender.com icons redistribution license publication` | S010/S018；厂商当前许可说明优先于论坛说法 |
| Reddit 提到 SMART | S011 权利核查；未采集 SMART 图库 |
| S005 链接 Nature art-editor profile | S016 只读到公开开头，其余受访问限制 |
| GitHub PR20 | 仅读取角色、模板、anti-AI-look 快照；未重新收集其图像库 |

## 排除与偏差

- 删除搜索结果中的无关 CSS 艺术、3D 重建算法、售卖服务和无来源图片拼贴。
- 不用论坛流行度给设计原则赋予科学证据强度。
- 社区转贴和出版原文记为 discovery chain，不能算作独立重复验证。
- 英文教程覆盖强于中文 app；不能声称已总结“小红书四图”或完整知乎意见。
- 原始出版图用于验证社区经验和合法视觉示例；本项目主体仍是 community/reference scouting，而不是复制 PR20 的文献图像库。
