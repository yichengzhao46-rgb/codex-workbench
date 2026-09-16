# PR20 接口：只递交候选，不直接写入主库

## 已验证快照

- PR：[PR-FIG: human-curated scientific visual learning system](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)
- 读取时间：2026-09-15；状态 Draft / Open / unmerged。
- head：`c4dea1b31db6b022e73e29967a0f02c959e39bcb`；branch：`feat/figure-style-corpus-v0.1`。
- base：`main`，`e3d30727c56520fcbecc952d4b425895e59448f2`。新分支从该 main 建立，不叠在 PR20 上。
- 当时 PR 正文报告主库 22 项 M001–M022；这属于 PR20 的自述状态，本批未重做其 22 张图审核。

## 职责表

| 对象 | 本模块 | PR20 |
| --- | --- | --- |
| 公开社区/教程检索 | 负责 | 可消费候选 |
| 来源可靠度、版权记录 | 负责候选记录 | 入库前复核 |
| 设计建议与反例 | 输出候选、条件和冲突 | 结合精选图决定采用 |
| M 编号、主库选择 | 不分配，不改写 | 用户选择后分配 |
| 视觉语法与 Style Recipe | 只建议映射字段 | 保持最终权威 |
| 科学主张与箭头事实 | 不提供科学证据 | 由用户与科学证据锁定 |
| anti-AI-look 终稿审核 | 提供上游检查理由 | 既有生产层负责 |

## 稳定的提案字段

示例：[CRP001.json](handoff/CRP001.json)。必需字段：`proposal_id`、`status`、`target_pr`、`target_snapshot_sha`、`source_ids`、`asset_ids`、`rule_ids`、`recommended_visual_roles`、`style_recipe_field_map`、`rights_summary`、`limitations`、`user_selection_required`。所有引用保持本模块 S/R/E 编号。

| 社区候选 | PR20 Style Recipe 段落 |
| --- | --- |
| 阅读方向、首图职能、焦点 | B Reference roles / C Visual architecture |
| 轮廓、材料、低强度 2.5D | D Rendering rules |
| 颜色、标签、碳/电子流 | E Semantic visual grammar |
| 资产生成、文字和箭头重建 | F Generation strategy / H Reconstruction |
| 装饰扣除、风格一致性 | G Anti-AI-look / I QA |

## 晋级过程

1. `discovered`：记录出处与访问状态；blocked 只作线索。
2. `reviewed_candidate`：有具体学习点、使用限制和权利记录；图像细节必须来自直接观察。
3. `proposed`：形成候选包，明确使用角色和预期改善。
4. `user_selected`：用户选择该参考或规则，保留选择记录。
5. `accepted_in_pr20`：由 PR20 完成视觉分解、版权复核、M 编号/映射及真实任务 QA。

拒绝或推迟均记录原因，避免重复抓取。禁止以下载成功或论坛高赞替代晋级。这里的选择门槛属于 PR20 已核实的 user-curated 职责；不阻止本次已经授权的独立 PR 创建。

本批只到 `proposed`，不发送 PR20 评论、不修改主库、不自动合并、不自动推广到 codex-playbook。若将来 PR20 模板改变，先比较固定快照与新模板，再修订映射。
