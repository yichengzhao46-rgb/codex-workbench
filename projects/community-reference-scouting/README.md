# Community / Reference Scouting for Scientific Figures

科研绘图公开社区参考检索与规则提炼，v0.1。它是 PR20 的上游候选输入层，独立分支、独立目录、独立审核。

## 先看什么

- [研究总结与适用场景](RESEARCH-SYNTHESIS.md)：结论、冲突建议、Bath/MOB 使用边界。
- [图像参考画廊](GALLERY.md)：4 张可重分发的原图、6 条链接参考及具体学习点。
- [20 条可复用设计规则](DESIGN-RULES.md)：适用条件、反例和验收方法。
- [anti-AI-look 候选检查](ANTI-AI-LOOK.md)：与 PR20 现有生产层对齐。
- [PR20 接口](PR20-INTERFACE.md)：候选提案如何送审，谁决定晋级。
- [来源记录](evidence/source-notes.md)、[检索范围](evidence/search-log.md)、[版权核查](evidence/rights-review.md)、[视觉检查](evidence/visual-review.md)。

## 本批结果

18 条来源记录：17 条外部来源 + 1 条 PR20 合约记录。外部来源包含专家/厂商教程、研究者博客、3 个 Reddit 讨论、中文入口及权利原文；不是 17 条都完成了全文或图片审核。

10 条图像证据记录：4 张 CC BY 4.0 原图已保存并逐图检查；1 条 BioRender 配图在浏览器中检查但仅存链接；其余 5 条保留 text-only / uninspected / blocked 状态。20 条规则全部为候选，0 条自动晋级 PR20，0 张宣称用户已批准。

## 职责边界

本模块负责检索、来源分级、版权、候选规则、反例与适用场景。PR20 继续负责用户精选机制图、视觉分解、视觉语法、Style Recipe 和最终生产审核。PR21 继续承担纯组学结果图。新模块不安装 skill、不改变任何全局路由、不修改 PR20/PR21 文件，也不自动产生定时抓取。

## 重复使用

按 [scouting 工作流程](SCOUTING-WORKFLOW.md) 提交下一批；数据字段见 [manifest contract](schemas/manifest-contract.md)。仅明确许可的资产放在 `assets/public/`，其余只记录链接。

在仓库根目录运行（仅 Python 标准库，无网络、无写入 PR20）：

```sh
python projects/community-reference-scouting/scripts/validate.py
python projects/community-reference-scouting/scripts/validate.py --self-test
```

检查结果与限制见 [validation report](validation/REPORT.md)。本批研究于 2026-09-15 开始，2026-09-16 完成交付。
