# PR20 Visual Learning Workflow / PR20 科学视觉学习流程

## 中文版

### 1. 核心定位

PR20 是一个**由用户人工筛选、面向科学绘图生成的视觉学习与参考系统**。

它的目的不是自动判断哪些论文图“好看”，也不是优先寻找与当前课题关键词最接近的图片。进入 PR20 的参考图已经由用户手动选择并认可，因此都属于有效的视觉学习样本。

PR20 的核心职责是：

> **把用户认可的真实科学图片转化为可理解、可检索、可组合、可迁移的视觉知识，并根据具体科学绘图任务，为新图确定最合适的视觉表达方式。**

核心分工：

> **用户决定 PR20 学哪些图。**  
> **用户与 ChatGPT 讨论决定新图要表达什么。**  
> **PR20 决定这些科学内容应该如何被视觉化。**

### 2. 科学逻辑先于视觉检索

PR20 不负责决定科学机制本身。

对于 Bath–RP、Bath–Bio-Se、GAC/DIET、EET/EEU、环境梯度、组学结果整合等任务，首先通过用户与 ChatGPT 的讨论确定：

- 科学问题与核心结论；
- 图中需要出现的模块；
- established / candidate / unresolved 路径；
- 证据边界；
- 信息层级和阅读顺序；
- 哪些信息应突出、哪些应弱化。

科学内容确定后，PR20 再回答：

> 这个逻辑应该用什么 layout、cell rendering、material rendering、arrow grammar、palette、typography、density、depth 和 visual hierarchy 呈现？

### 3. 用户人工筛选是视觉 ground truth

标准入口为：

```text
Real published scientific figures
        ↓
User manual selection / approval
        ↓
Approved PR20 reference corpus
```

用户负责决定哪些真实 published figures 值得进入图库。

**只要图片被用户保留，就代表它值得 PR20 学习。** PR20 不再设置第二层自动“审美批准”机制。

### 4. PR20 学习 visual grammar，而不是整图模板

PR20 应逐张拆解参考图，而不是把某篇论文的整张 Figure 当作模板复制。

主要学习维度包括：

- composition / overall spatial organization；
- layout；
- visual hierarchy；
- cell rendering；
- membrane / intracellular rendering；
- material / mineral / GAC / electrode / nanoparticle rendering；
- metabolite / molecule / gas / electron representation；
- arrow and connector grammar；
- palette and accent strategy；
- typography and label placement；
- whitespace；
- information density；
- panel organization；
- dimensionality；
- perspective / camera angle；
- lighting / shadow；
- transparency / translucency；
- evidence-to-mechanism integration；
- reusable motifs。

最终学习对象是：

> **visual components + visual rules**

而不是：

> **copy one published figure style**

### 5. 不限制 2D：2D / 2.5D / 3D / hybrid 都是有效样本

PR20 不预设“正确科研风格必须是 2D”。

用户认可的参考图可以是：

```text
2D
2.5D
3D
Hybrid 2D–3D
```

对于 3D reference，PR20 还应学习：

- object geometry；
- perspective；
- camera angle；
- depth hierarchy；
- lighting and shadow；
- surface/material treatment；
- transparency / translucency；
- foreground/background separation；
- cells/materials/molecules 之间的空间关系。

学习 3D 不意味着最终必须生成 full 3D。PR20 可以进行跨维度迁移，例如：

```text
3D reference
↓
learn volume + depth + surface + spatial contact
↓
translate into restrained 2.5D scientific schematic
```

当任务本身适合空间表现时，也可以直接采用 full 3D 或 hybrid 2D–3D。

### 6. 视觉适配优先于主题相似

PR20 的核心检索问题不是：

> 哪张图和当前研究主题最相似？

而是：

> 哪些用户认可的参考图为当前展示问题提供了最好的视觉解决方案？

科学相关性主要作为兼容性约束，而不是主排序指标。

例如一个 Bath–RP 图可能需要分别寻找：

- overall layout reference；
- Bath / microbial cell rendering reference；
- RP / partner cell rendering reference；
- extracellular exchange reference；
- arrow grammar reference；
- palette reference；
- density / whitespace reference。

### 7. 默认使用多参考图综合

一张新图不应该机械模仿单一 reference。

推荐模式：

```text
Reference A → overall composition
Reference B → cell rendering
Reference C → material / molecule representation
Reference D → arrow grammar
Reference E → palette
Reference F → typography / whitespace
Reference G → information-density control
```

PR20 将这些互补视觉方案综合为新的、任务特异的视觉系统。

### 8. Style Recipe 是核心中间产物

正式生成科学图之前，PR20 应输出结构化 Style Recipe，通常包括：

```text
scientific task
layout / composition
visual hierarchy
cell rendering
material rendering
molecular representation
arrow / connector grammar
palette
accent strategy
typography
whitespace
information density
dimensionality
perspective / lighting when relevant
reusable motifs
elements to avoid
```

Style Recipe 是参考图库与新图生成之间的桥梁，不应只是一次性自然语言 prompt。

### 9. 长期目标：用户自己的多套 scientific visual languages

随着用户不断添加认可的参考图，PR20 应逐渐归纳稳定的审美规律，但不应收敛成一种固定风格。

更理想的结果是：

> **在统一的用户审美方向下，建立多个 task-specific scientific visual languages。**

例如：

- microbial interaction；
- membrane EET / EEU；
- material–microbe interface；
- environmental gradient；
- perturbation comparison；
- experimental workflow；
- evidence-to-mechanism summary；
- graphical abstract。

### 10. 完整 Workflow

```text
STEP 0
Real published scientific figures
        ↓

STEP 1 — USER
Manual visual selection / approval
        ↓
Approved PR20 reference corpus
        ↓

STEP 2 — PR20
Visual decomposition
        ↓
composition
layout
hierarchy
cell rendering
material rendering
arrow grammar
palette
typography
whitespace
density
depth
lighting
reusable motifs
        ↓

STEP 3 — PR20
Visual grammar annotation
        ↓

STEP 4 — PR20
Reusable visual knowledge library
        ↓

STEP 5 — USER + CHATGPT
Define scientific logic of the new figure
        ↓

STEP 6 — PR20
Identify required visual roles
        ↓

STEP 7 — PR20
Retrieve complementary approved references
        ↓

STEP 8 — PR20
Multi-reference visual synthesis
        ↓

STEP 9 — PR20
Structured task-specific Style Recipe
        ↓

STEP 10
Scientific figure generation
        ↓

STEP 11 — USER
Review generated figure
        ↓

STEP 12 — PR20
Refinement / feedback accumulation
```

### 11. PR20 不负责什么

PR20 不应：

- 自动决定哪些 published figures 值得用户喜欢；
- 决定科学机制是否成立；
- 以主题关键词相似度主导审美 reference ranking；
- 强制所有输出采用 flat 2D；
- 整体复制某一篇论文图；
- 把图库规模作为首要成功指标。

### 12. 成功标准

PR20 是否成功，主要看它能否稳定回答：

1. **用户认可的图库里，具体有哪些视觉原则值得学习？**
2. **当前科研图应该借哪些 reference 的哪些部分？**
3. **如何把这些视觉原则重新组合成一张科学正确、原创且审美成熟的新图？**

一句话总结：

> **你决定 PR20 学什么图；我们决定图要说什么；PR20 决定它应该长什么样。**

---

# English Version

## 1. Core positioning

PR20 is a **human-curated visual learning and reference system for scientific figure generation**.

Its purpose is not to automatically decide which published figures are aesthetically good, nor to retrieve references mainly because they share scientific keywords with the current project. Every figure that enters the curated PR20 corpus has already been manually selected and approved by the user and is therefore considered a valid visual-learning source.

The core responsibility of PR20 is:

> **To transform user-approved published scientific figures into interpretable, searchable, reusable, combinable, and transferable visual knowledge, and to use that knowledge to determine the most appropriate visual expression for each new scientific figure.**

The division of responsibility is:

> **The user decides what PR20 learns from.**  
> **The user and ChatGPT decide what the new figure needs to communicate.**  
> **PR20 decides how that scientific content should look.**

## 2. Scientific logic comes before visual retrieval

PR20 does not determine the scientific mechanism itself.

For each new task, the user and ChatGPT first define the scientific question, figure content, evidence boundaries, established versus candidate relationships, information hierarchy, and intended reading order.

Once the logic is fixed, PR20 addresses the complementary visual question:

> **How should that logic be represented through layout, rendering, connectors, palette, typography, density, dimensionality, and hierarchy?**

## 3. Human curation is the visual ground truth

The canonical entry path is:

```text
Real published scientific figures
        ↓
User manual selection / approval
        ↓
Approved PR20 reference corpus
```

Once the user retains a reference, PR20 treats it as worth learning from. It does not require a second automatic aesthetic approval layer.

## 4. Learn visual grammar, not complete figures

PR20 should decompose each approved reference into transferable visual components and rules rather than treating a published figure as a template to copy.

Key learning dimensions include composition, layout, hierarchy, cell rendering, membrane/interior rendering, material representation, molecular representation, arrow grammar, palette, typography, whitespace, density, dimensionality, perspective, lighting, transparency, panel organization, evidence integration, and reusable motifs.

The system learns:

> **visual components + visual rules**

rather than:

> **one complete published figure style to imitate**

## 5. 2D, 2.5D, 3D, and hybrid references are all valid

PR20 should not enforce a flat-2D aesthetic.

The approved corpus may contain 2D, restrained 2.5D, full 3D, and hybrid 2D–3D scientific illustrations.

For user-approved 3D references, PR20 should additionally analyze geometry, perspective, camera angle, depth hierarchy, lighting, shadow treatment, surface properties, translucency, foreground/background separation, and spatial relationships.

Learning from a 3D figure does not require reproducing it as full 3D. Transfer across dimensionality is allowed when appropriate.

## 6. Visual suitability outranks topical similarity

The central retrieval question is not:

> Which figure is scientifically most similar to the current topic?

It is:

> **Which approved references provide the strongest visual solutions for the current presentation problem?**

Scientific relevance acts mainly as a compatibility constraint.

## 7. Multi-reference synthesis is the default

A new scientific figure should normally combine complementary visual solutions from several approved references.

For example:

```text
Reference A → overall composition
Reference B → cell rendering
Reference C → material / molecule representation
Reference D → arrow grammar
Reference E → palette
Reference F → typography / whitespace
Reference G → information-density control
```

The goal is a new task-specific visual system, not imitation of one published figure.

## 8. The Style Recipe is the key intermediate output

Before generation, PR20 should produce a structured Style Recipe specifying the task, layout, hierarchy, rendering choices, connector grammar, palette, typography, whitespace, information density, dimensionality, perspective/lighting where relevant, reusable motifs, and elements to avoid.

The Style Recipe is the bridge between the approved reference corpus and figure generation.

## 9. Long-term goal: multiple user-specific scientific visual languages

As the user adds more approved references, PR20 should identify recurring aesthetic preferences and transferable design patterns. It should not collapse them into one universal house style.

The target is:

> **multiple task-specific scientific visual languages under a coherent user-curated aesthetic direction.**

## 10. Full workflow

```text
REAL PUBLISHED FIGURES
        ↓
USER MANUAL SELECTION / APPROVAL
        ↓
APPROVED PR20 REFERENCE CORPUS
        ↓
VISUAL DECOMPOSITION
        ↓
VISUAL GRAMMAR ANNOTATION
        ↓
REUSABLE VISUAL KNOWLEDGE
        ↓

NEW SCIENTIFIC FIGURE TASK
        ↓
USER + CHATGPT DEFINE SCIENTIFIC LOGIC
        ↓
PR20 IDENTIFIES REQUIRED VISUAL ROLES
        ↓
TASK-SPECIFIC REFERENCE RETRIEVAL
        ↓
MULTI-REFERENCE VISUAL SYNTHESIS
        ↓
STRUCTURED STYLE RECIPE
        ↓
SCIENTIFIC FIGURE GENERATION
        ↓
USER REVIEW
        ↓
REFINEMENT / FEEDBACK ACCUMULATION
```

## 11. What PR20 should not do

PR20 should not automatically decide which published figures the user should like, define the scientific mechanism, rank references mainly by topical keyword similarity, force all output into flat 2D, imitate one published figure wholesale, or optimize primarily for corpus size.

## 12. Success criteria

PR20 succeeds when it can reliably answer:

1. **What visual principles should be learned from the approved corpus?**
2. **Which approved references best solve the current presentation problem, and which visual role should each one serve?**
3. **How should those visual principles be recombined into a scientifically correct, original, and aesthetically mature new figure?**

Final principle:

> **You decide what PR20 learns from. We decide what the figure needs to say. PR20 decides how it should look.**
