# Community / Reference Scouting for Scientific Figures

科研绘图公开社区参考检索与规则提炼，v0.1。它是 PR20 的**上游 external visual-design scouting / evidence layer**：负责发现和记录外部视觉设计知识，但**不决定 PR20 应该学习什么，也不作为最终 visual authority**。

> **PR22 discovers and documents external visual-design knowledge; it does not determine what PR20 should learn.**

## 先看什么

- [研究总结与适用场景](RESEARCH-SYNTHESIS.md)：结论、冲突建议、Bath/MOB 使用边界。
- [图像参考画廊](GALLERY.md)：4 张可重分发的原图、6 条链接参考及具体学习点。
- [20 条候选设计规则](DESIGN-RULES.md)：适用条件、反例和验收方法；这些规则是 external design hypotheses，不是 PR20 的硬规范。
- [anti-AI-look 候选检查](ANTI-AI-LOOK.md)：与 PR20 现有生产层对齐。
- [PR20 接口](PR20-INTERFACE.md)：候选提案如何交给用户选择，再 handoff 到 PR20。
- [来源记录](evidence/source-notes.md)、[检索范围](evidence/search-log.md)、[版权核查](evidence/rights-review.md)、[视觉检查](evidence/visual-review.md)。

## 本批结果

18 条来源记录：17 条外部来源 + 1 条 PR20 合约记录。外部来源包含专家/厂商教程、研究者博客、3 个 Reddit 讨论、中文入口及权利原文；不是 17 条都完成了全文或图片审核。

10 条图像证据记录：4 张 CC BY 4.0 原图已保存并逐图检查；1 条 BioRender 配图在浏览器中检查但仅存链接；其余 5 条保留 text-only / uninspected / blocked 状态。20 条规则全部为候选，0 条自动晋级 PR20，0 张宣称用户已批准。

## 职责边界

本模块负责：

- 公开社区、教程、研究者博客和公开设计资料的 scouting；
- 来源分级、出处追踪、版权状态与访问限制记录；
- 候选设计原则、反例、冲突建议和适用条件；
- 候选 reference 入口及其可能提供的 visual roles；
- 当任务需要时，定向搜索 2D、2.5D、3D 或 hybrid scientific-visualization 方法与案例。

本模块**不负责**：

- 判断哪些图片最终值得 PR20 学习；
- 给候选参考分配 M 编号；
- 覆盖用户已经认可的 PR20 reference；
- 定义科学机制或证据边界；
- 把社区经验直接变成 Style Recipe 的强制规则；
- 把 2D / 2.5D 作为默认优于 3D 的审美等级。

PR20 继续负责用户精选机制图的视觉分解、visual grammar、multi-reference synthesis、Style Recipe 和最终生产审核。**当 PR22 建议与用户已认可的 PR20 reference 冲突时，以用户选择和 PR20 visual grammar 为准。** PR21 继续承担纯组学结果图。

新模块不安装 skill、不改变任何全局路由、不修改 PR20/PR21 文件，也不自动产生定时抓取。

## 3D / hybrid scouting

PR22 可以主动检索高质量 3D scientific rendering 的公开教程和设计经验，尤其关注：

- geometry / morphology
- perspective / camera angle
- depth hierarchy
- lighting / shadow
- material and surface rendering
- transparency / translucency
- spatial contact and foreground/background separation

这些结果只作为候选设计知识。PR20 可将其中的视觉原则直接用于 3D，也可跨维度转译为 restrained 2.5D；PR22 不自动把 3D 降权，也不要求最终输出必须是 3D。

## 重复使用

按 [scouting 工作流程](SCOUTING-WORKFLOW.md) 提交下一批；数据字段见 [manifest contract](schemas/manifest-contract.md)。仅明确许可的资产放在 `assets/public/`，其余只记录链接。

在仓库根目录运行（仅 Python 标准库，无网络、无写入 PR20）：

```sh
python projects/community-reference-scouting/scripts/validate.py
python projects/community-reference-scouting/scripts/validate.py --self-test
```

检查结果与限制见 [validation report](validation/REPORT.md)。本批研究于 2026-09-15 开始，2026-09-16 完成交付。
