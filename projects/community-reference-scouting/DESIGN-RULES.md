# 候选设计规则

所有条目均为 `candidate`。来源支持、视觉观察、项目约束与设计综合分别标注；本表由 `manifests/rules.json` 整理。编号用于接口，不能作为 PR20 的 M 编号。

## R01 · 一句主信息先于美化

先写一句可证实的主信息，再画信息模块；缩略图中应先看到核心对象和结果方向。

- 适用：graphical_abstract, first_figure
- 不可机械迁移：不能把图形摘要当作全文所有实验的缩小拼图。
- 证据类型：`source_supported`；来源：[S001](https://www.biorender.com/blog/top-4-tips-for-designing-a-graphical-abstract), [S002](https://www.simplifiedsciencepublishing.com/resources/best-graphical-abstract-examples-with-free-templates)；定位：Starting your graphical abstract; Design Summary
- 验收：让未参与绘图的人复述第一眼看到的信息。

## R02 · 图 1 与图形摘要分工

首图优先回答研究对象、条件和体系组织；GA 优先传达主要发现。首图是否以概念图开场由论文叙事决定。

- 适用：first_figure, graphical_abstract
- 不可机械迁移：不存在已证实的“Nature 大子刊首图必须是示意图”通则。
- 证据类型：`curator_synthesis`；来源：[S002](https://www.simplifiedsciencepublishing.com/resources/best-graphical-abstract-examples-with-free-templates), [S009](https://esurf.copernicus.org/articles/6/687/2018/)；定位：Layout recommendations; Figure 1 model overview
- 验收：分别写出两个交付物的读者问题，避免同一内容机械复用。

## R03 · 按逻辑选择布局

顺序用线性，对照用平行，尺度变化用嵌套，只有真实闭环才用环形。

- 适用：mechanism_schematic, graphical_abstract
- 不可机械迁移：不能为画面平衡把单向交换闭合为循环。
- 证据类型：`source_supported`；来源：[S002](https://www.simplifiedsciencepublishing.com/resources/best-graphical-abstract-examples-with-free-templates), [S008](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011789)；定位：Circular and Unique Designs; Rule 5 / Fig 5
- 验收：遮去箭头后仍能判断入口和阅读方向。

## R04 · 层级由信息重要性决定

设一个主视觉焦点；辅助对象缩小、降饱和或减少细节。

- 适用：first_figure, mechanism_schematic, 2d_2_5d
- 不可机械迁移：不要把每个颗粒、细胞和仪器都画成同等醒目的主体。
- 证据类型：`curator_synthesis`；来源：[S001](https://www.biorender.com/blog/top-4-tips-for-designing-a-graphical-abstract), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Color and contrast; PR20 visual architecture
- 验收：缩小后能指出第一、第二、第三阅读层级。

## R05 · 颜色表达稳定语义

同一实体跨 panel 使用同色；以少量语义色配中性色和必要强调色。

- 适用：mechanism_schematic, graphical_abstract
- 不可机械迁移：2–3 色是起点，不是所有机制图的硬上限；不强行套医学“暖色坏、冷色好”。
- 证据类型：`source_supported`；来源：[S001](https://www.biorender.com/blog/top-4-tips-for-designing-a-graphical-abstract), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Color and contrast; palette discipline
- 验收：用对象—颜色映射检查所有 panel；额外颜色需说明功能。

## R06 · 对比与可访问性

灰度缩小检查关键边界；用标签或线型补充颜色。

- 适用：all_schematics
- 不可机械迁移：不能只看彩色大屏是否漂亮，也不能让淡色文字融入背景。
- 证据类型：`source_supported`；来源：[S001](https://www.biorender.com/blog/top-4-tips-for-designing-a-graphical-abstract), [S008](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011789)；定位：Color and contrast; Rule 8
- 验收：最终使用尺寸下检查灰度和关键标签；必要时模拟色觉差异。

## R07 · 箭头有语义而非只指方向

分别定义碳流、电子流、物质交换和叙事转场；不确定关系要有明确图例。

- 适用：mechanism_schematic
- 不可机械迁移：虚线没有跨论文统一含义；不能靠箭头美化把假设画成事实。
- 证据类型：`curator_synthesis`；来源：[S008](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011789), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Rule 6 / Fig 6; semantic visual grammar
- 验收：逐条核对起点、终点、方向、标签、证据状态。

## R08 · 对齐和留白形成分组

同级模块对齐，模块间距离大于模块内部距离；移除无作用的框。

- 适用：all_schematics
- 不可机械迁移：留白不是规定比例，不能以装饰分隔线取代逻辑分组。
- 证据类型：`source_supported`；来源：[S001](https://www.biorender.com/blog/top-4-tips-for-designing-a-graphical-abstract), [S008](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011789)；定位：Alignment; Rule 6 grouping
- 验收：检查横纵基线、标签间距和线条相撞。

## R09 · 先决定使用尺寸

在期刊要求的画幅和实际排版尺寸上设计；社交媒体与论文版分别排版。

- 适用：first_figure, graphical_abstract
- 不可机械迁移：不是所有期刊 GA 都必须是正方形；不要从大海报直接缩小。
- 证据类型：`source_supported`；来源：[S001](https://www.biorender.com/blog/top-4-tips-for-designing-a-graphical-abstract), [S002](https://www.simplifiedsciencepublishing.com/resources/best-graphical-abstract-examples-with-free-templates), [S008](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011789)；定位：Plan ahead; social media formatting; Rule 4 / Fig 4
- 验收：最终宽度下检查文字及最细线条，确认目标期刊要求。

## R10 · 统一素材外观

来自不同素材库的对象统一线宽、细节量、透视和视觉重量。

- 适用：mechanism_schematic, 2d_2_5d
- 不可机械迁移：不能用软件品牌或图标数量代替视觉一致性。
- 证据类型：`curator_synthesis`；来源：[S005](https://www.reddit.com/r/labrats/comments/1duy1nq/how_does_nature_reviews_design_their_diagrams/), [S006](https://www.reddit.com/r/labrats/comments/1vup1ss/any_suggestion_for_graphical_abstracts/), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Editorial redraw anecdotes; template discussion; rendering rules
- 验收：并排检查重复对象，纠正无语义的样式变化。

## R11 · 2.5D 为结构服务

优先用轮廓、剖面和遮挡说明空间；轻微渐变仅在改善体积辨识时加入。

- 适用：2d_2_5d, material_interface
- 不可机械迁移：不是禁止 3D；不要把封面级光效带入所有论文机制图。
- 证据类型：`curator_synthesis`；来源：[S003](https://www.animateyour.science/post/how-to-draw-in-illustrator-a-step-by-step-tutorial-for-researchers), [S004](https://www.joriseekhout.com/blog/3d-illustrations-for-scientific-articles/), [S007](https://www.reddit.com/r/labrats/comments/1v2du8e/how_are_figures_like_this_created/), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Dimension and Shading; low-poly paragraph; dimensionality discussion
- 验收：与平面版本比较：深度是否新增了有用信息，是否遮挡标签。

## R12 · 平面与空间 panel 可按任务混合

用 2D 剖面讲通量，用空间视图讲位置；通过重复对象和标号连接。

- 适用：first_figure, environmental_context
- 不可机械迁移：同一场景内部不能出现无法解释的透视变化。
- 证据类型：`visual_observation`；来源：[S009](https://esurf.copernicus.org/articles/6/687/2018/)；定位：Figure 1 panels a–c
- 验收：每种视角写出一个信息目的；删除仅为炫技的角度。

## R13 · 形态和机制不得由教程推断

先冻结物种、材料形态和已知结构；通用细菌教程只借用制作方法。

- 适用：microbial_schematic, material_interface
- 不可机械迁移：不可把教程中的杆状轮廓、表面丝状物或蛋白装饰直接套到研究对象。
- 证据类型：`project_guardrail`；来源：[S003](https://www.animateyour.science/post/how-to-draw-in-illustrator-a-step-by-step-tutorial-for-researchers), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：H. pylori tutorial; PR20 science lock
- 验收：形态和结构回到当前任务的显微证据或可靠物种资料确认。

## R14 · 限制装饰性渲染

默认哑光、低纹理、白色或近白背景；去掉没有信息功能的辉光、浮游颗粒和强反射。

- 适用：2d_2_5d, mechanism_schematic
- 不可机械迁移：合理的光照、材料界面或空间信息可有例外，但必须写明理由。
- 证据类型：`project_guardrail`；来源：[S001](https://www.biorender.com/blog/top-4-tips-for-designing-a-graphical-abstract), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Common mistakes; anti-AI-look pass
- 验收：逐项解释光效或纹理编码的信息；无法解释则删除。

## R15 · 重建文字和证据连接线

AI 可辅助资产草稿；最终标签、化学式、panel 字母与箭头由可控工具排版并核对。

- 适用：ai_assisted_schematic
- 不可机械迁移：不能把生成模型输出的科学标签或连接关系当成可靠内容。
- 证据类型：`project_guardrail`；来源：[S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Asset-first generation; reconstruction
- 验收：检查文字可编辑性、箭头语义和 science lock 的一一对应。

## R16 · 消除模板感靠内容特异性

用研究问题决定构图和视觉角色；参考按不同功能组合，并保留有意义的物种或材料差异。

- 适用：graphical_abstract, mechanism_schematic
- 不可机械迁移：不添加随机粗糙、不规则噪声或伪手绘以伪装“人类风格”。
- 证据类型：`curator_synthesis`；来源：[S006](https://www.reddit.com/r/labrats/comments/1vup1ss/any_suggestion_for_graphical_abstracts/), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Template fatigue; intentional consistency
- 验收：若删去标题仍与无关论文完全通用，应检查缺失的研究特异信息。

## R17 · 区分设计经验和科研证据

论坛评价用于发现困扰和候选方法；不得据此确认 EET、EEU、DIET 或物种特异碳固定。

- 适用：all_schematics
- 不可机械迁移：流行度、点赞、发表期刊和视觉精致度都不能确定科学机制。
- 证据类型：`project_guardrail`；来源：[S005](https://www.reddit.com/r/labrats/comments/1duy1nq/how_does_nature_reviews_design_their_diagrams/), [S007](https://www.reddit.com/r/labrats/comments/1v2du8e/how_are_figures_like_this_created/), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Community anecdotes; science lock
- 验收：每条机制连接必须另有科学证据记录，参考库只提供视觉依据。

## R18 · 取得单资产权限再入库

分别核查阅读、保存、公开重分发、改编和模型输入权限；不明确则只留链接。

- 适用：reference_scouting
- 不可机械迁移：CC 网页、开放文章、免费账号和公开截图均不是所有内含素材的统一许可。
- 证据类型：`rights_policy`；来源：[S010](https://help.biorender.com/hc/en-gb/articles/17605463719709-Publication-license-Terms-of-use), [S011](https://smart.servier.com/terms-of-use/), [S018](https://help.biorender.com/hc/en-gb/articles/17605449206045-Publication-license-guidelines-Editing-your-figure-outside-of-BioRender)；定位：Rights pages in source catalog
- 验收：本地资产必须有许可依据、署名、变更说明和 SHA256。

## R19 · 独立参考按角色晋级

社区来源先形成候选包；用户选择和 PR20 直接视觉审核之后才分配 M 编号或加入 Style Recipe。

- 适用：reference_scouting
- 不可机械迁移：不能因规则听起来合理而自动添加进 PR20 主库。
- 证据类型：`interface_contract`；来源：[S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：PR20 design rule; reference roles
- 验收：检查 proposed 状态和空的 canonical_id；禁止直接写 PR20 目录。

## R20 · 用小样验证而非审美分数代替验收

比较读图顺序、标签可读性、证据含义和编辑能力；记录失败与修订。

- 适用：all_schematics
- 不可机械迁移：anti-AI-look 清单不能检测作者身份，也不能保证期刊接收。
- 证据类型：`curator_synthesis`；来源：[S005](https://www.reddit.com/r/labrats/comments/1duy1nq/how_does_nature_reviews_design_their_diagrams/), [S017](https://github.com/yichengzhao46-rgb/codex-workbench/pull/20)；定位：Editorial normalization anecdotes; QA
- 验收：下一步真实绘图任务再做盲读测试；本 PR 不宣称用户验证已完成。
