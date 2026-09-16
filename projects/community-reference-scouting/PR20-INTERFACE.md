# PR20 接口：只递交候选，不直接写入主库

## 已验证快照

- PR：[PR-FIG: human-curated scientific visual learning system](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)
- 读取时间：2026-09-15；状态 Draft / Open / unmerged。
- head：`c4dea1b31db6b022e73e29967a0f02c959e39bcb`；branch：`feat/figure-style-corpus-v0.1`。
- base：`main`，`e3d30727c56520fcbecc952d4b425895e59448f2`。新分支从该 main 建立，不叠在 PR20 上。
- 当时 PR 正文报告主库 22 项 M001–M022；这属于 PR20 的自述状态，本批未重做其 22 张图审核。

## 核心接口原则

> **PR22 discovers and documents external visual-design knowledge; it does not determine what PR20 should learn.**

PR22 输出的是候选设计知识和候选 reference 入口，不是 visual authority。用户决定哪些 reference 值得进入 PR20；一旦用户选中，PR20 直接把它视为有效 visual-learning input，并进入 visual decomposition / visual grammar 流程，而不是再做第二轮审美审批。

## 职责表

| 对象 | PR22 / 本模块 | PR20 |
| --- | --- | --- |
| 公开社区/教程检索 | 负责 | 可消费候选 |
| 来源可靠度、版权记录 | 负责候选记录 | 入库/使用时复核 |
| 设计建议与反例 | 输出 candidate insights、条件和冲突 | 结合用户精选 reference 决定是否采用 |
| 候选视觉角色 | 可建议，不代表优先级 | 由 visual decomposition / Style Recipe 最终决定 |
| 用户参考选择 | 不替代用户决定 | 用户选择是 source of truth |
| M 编号、主库映射 | 不分配、不改写 | 用户选择后处理 |
| visual grammar / Style Recipe | 只建议字段映射 | 保持最终权威 |
| 科学主张与箭头事实 | 不提供科学证据 | 由用户 + ChatGPT + 科学证据锁定 |
| anti-AI-look 终稿审核 | 提供上游候选检查理由 | 既有生产层负责 |
| 2D / 2.5D / 3D / hybrid | 均可 scouting | 根据任务和用户-approved corpus 决定最终使用方式 |

## Authority hierarchy

当外部建议发生冲突时，采用以下优先级：

```text
Scientific evidence / science lock
        ↓
User-selected PR20 references
        ↓
PR20 visual grammar + task-specific Style Recipe
        ↓
PR22 external design insights / community advice
```

因此，PR22 的规则不能覆盖用户已经认可的视觉语言。例如，社区教程若建议减少阴影，但用户选入 PR20 的高质量 3D reference 正是通过柔和光照和体积关系实现清晰表达，则 PR22 只能记录这种冲突和适用条件，不能自动降权该 reference。

## 稳定的提案字段

示例：[CRP001.json](handoff/CRP001.json)。必需字段：`proposal_id`、`status`、`target_pr`、`target_snapshot_sha`、`source_ids`、`asset_ids`、`rule_ids`、`recommended_visual_roles`、`style_recipe_field_map`、`rights_summary`、`limitations`、`user_selection_required`。

其中：

- `recommended_visual_roles` = proposal metadata，不是排序结果；
- `style_recipe_field_map` = 可能影响哪些 PR20 字段，不代表必须采用；
- 所有引用保持本模块 S/R/E 编号，用户选择前不分配 M 编号。

| 社区候选 | PR20 Style Recipe 段落 |
| --- | --- |
| 阅读方向、首图职能、焦点 | B Reference roles / C Visual architecture |
| 轮廓、材料、2D/2.5D/3D 深度处理 | D Rendering rules |
| 颜色、标签、碳/电子流 | E Semantic visual grammar |
| 资产生成、文字和箭头重建 | F Generation strategy / H Reconstruction |
| 装饰扣除、风格一致性 | G Anti-AI-look / I QA |

## Handoff 流程

1. `discovered`：记录出处与访问状态；blocked 只作线索。
2. `reviewed_candidate`：有具体学习点、使用限制和权利记录；图像细节必须来自直接观察。
3. `proposed`：形成候选包，明确可能的 visual roles 和预期改善；仍不代表推荐优先级。
4. `user_selected`：用户明确选择该参考或规则，保留选择记录。
5. `handoff_to_pr20`：交给 PR20 进入 visual decomposition、visual grammar、M 编号/映射和真实任务 QA。

`handoff_to_pr20` 不代表 PR20 再进行第二轮“这张图够不够好看”的审批；用户选择本身已经定义了该 reference 值得学习。

拒绝或推迟均记录原因，避免重复抓取。禁止以下载成功、论坛高赞、厂商品牌或发表期刊替代用户选择。

## 3D / hybrid reference

PR22 可以针对 3D / hybrid scientific visualization 定向 scouting，包括 geometry、perspective、camera angle、depth hierarchy、lighting、shadow、surface/material rendering 和 transparency。

这些原则既可以由 PR20 直接用于 3D，也可以跨维度转译成 restrained 2.5D。PR22 不把 3D 自动视为低优先级，也不把“2.5D 更学术”设为硬规则。

本批只到 `proposed`，不发送 PR20 评论、不修改主库、不自动合并、不自动推广到 codex-playbook。若将来 PR20 模板改变，先比较固定快照与新模板，再修订映射。
