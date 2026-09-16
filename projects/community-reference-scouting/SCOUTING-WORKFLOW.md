# 可复用 scouting 工作流程

1. **接收 brief**：图的任务、对象、目标期刊尺寸、参考角色；先区分首图、GA、机制图、材料/细胞界面和纯结果图。
2. **识别缺口**：先判断当前缺的是 layout、cell/material rendering、arrow grammar、palette、2.5D depth、3D geometry/lighting 还是其他 visual role；不要只按科学关键词搜相似论文。
3. **分阶段检索**：先看标题、来源、摘要或教程目录；每个平台先筛最相关少数项。选定后读对应段落，图像细节才进入直接视觉检查。
4. **追溯原始来源**：转贴中的论文图追溯 DOI、原始 figure 和许可。保留 discovery chain，防止多个转贴被误当多个独立来源。
5. **分级**：rights_primary / expert_tutorial / expert_vendor / practitioner / community_anecdote / discovery_only。证据角色不同，不按点赞、期刊名或视觉精致度混排。
6. **提炼候选 insight**：一条记录写清做什么、何时用、何时不用、依据定位、如何验证。分开源作者建议、可见观察和本项目综合。所有规则保持 candidate，不升级为 PR20 硬规范。
7. **检验冲突**：例如阴影提升体积 vs 阴影造成噪声；按图的任务给出有条件的处理，不机械投票。若与用户已认可的 PR20 reference 冲突，只记录冲突，不覆盖 PR20。
8. **逐资产权利检查**：允许公开镜像才保存；否则 URL + image locator + rights pending。截图本身不会消除图内资产版权。
9. **视觉检查**：记录具体看到的结构与缺点；caption-only / text-only 不可改为 visual_inspected。记录 agent inspection 与 user selection 的区别。
10. **验证并提案**：运行校验器，生成 CRP 候选包；`recommended_visual_roles` 只是 proposal metadata，不代表排序；不得给本模块参考分配 PR20 M 编号。
11. **用户选择**：只有用户明确选择后，才将该 reference / rule 标为 `user_selected`。
12. **handoff 到 PR20**：用户选中的 reference 直接进入 PR20 visual decomposition / visual grammar 流程；不再设置第二轮自动审美审批。失败案例和未选候选保留原因，下一次检索复用已查记录。

## 选择标准

优先有原作者、可定位例子、清晰 before/after 或操作解释、与目标 visual role 相关的帖子。降权纯软件清单、无出处拼图、购买导流、泛称“顶刊风格”的营销内容。

优先按**构图 / 对象 / 箭头 / 材料 / 深度 / 光照 / typography / density**等不同角色找少量互补来源；不凑同一来源大量相似图。

科学主题相关性用于保证兼容性，但不是主要审美排序依据。

## 2D / 2.5D / 3D scouting

PR22 不预设 2D 或 2.5D 一定优于 3D。根据任务需要，可以分别搜索：

- **2D**：layout、hierarchy、arrow grammar、labeling、whitespace；
- **2.5D**：cutaway、occlusion、depth cues、controlled gradients；
- **3D**：geometry、camera angle、perspective、lighting、shadow、surface/material rendering、transparency；
- **hybrid**：2D logic + 3D spatial asset / material interface 的组合方式。

3D reference 被用户选中后，可由 PR20 直接学习 3D visual language，也可跨维度转译成 restrained 2.5D。不要因为“3D”标签本身自动降权。

## Authority hierarchy

```text
Scientific evidence / science lock
        ↓
User-selected PR20 references
        ↓
PR20 visual grammar + Style Recipe
        ↓
PR22 external scouting insights
```

PR22 是 scouting advisor，不是 visual authority。

## 停止与升级条件

遇到登录、403、CAPTCHA 或不可读图片，记录覆盖限制；不绕过访问控制。只在缺失内容会改变结论时继续另一条合法来源。

当已经能形成少量可审查、角色互补、来源清楚的候选 insight / reference 后停止扩展。**不以规则数量、reference 数量或来源数量作为成功指标。** 后续真实绘图暴露缺口时再定向补查。

## 正反触发

- 正：找材料–细菌机制图的 2.5D/3D 界面表现方法、比较 GA 布局、收集首图叙事经验、寻找高质量科学 3D 的 geometry / lighting / surface-rendering 教程。
- 反：计算 isotope 原始数据、分析 PCA/火山图、判断 Bath EEU 是否成立、自动修改 PR20、自动决定用户审美、批量抓取付费素材。

未来接入 skill/router 需要另行验证；本 PR 是可执行校验的研究参考项目，不假装已经安装或自动运行。
