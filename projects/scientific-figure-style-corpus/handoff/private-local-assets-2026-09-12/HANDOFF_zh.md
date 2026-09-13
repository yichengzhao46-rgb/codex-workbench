# Zotero 图像入库交接 — 2026-09-12

用户最新决定：本地停止继续改进，先打包，余下工作交给 GitHub。不要 merge，保持 Draft PR。

## 包的使用

- `github-handoff.zip`：可交给 GitHub 的代码、元数据及交接说明，没有出版社图片、PDF、数据库、凭据或虚拟环境。
- `private-local-assets.zip`：139 张实际 PNG 与本地复查材料，仅供本机私人研究，**不要上传公开 GitHub**。
- GitHub 包的 `overlay/` 是待应用文件，保持仓库相对路径；`reference/` 仅是本地旧基线说明供阅读，不能用来覆盖最新远端版本。
- `local-changes.patch` 仅包含已跟踪文件的差异；新增文件都在 overlay 中。不要将 patch 与 overlay 重复应用。

## 当前状态（真实文件核验）

扫描 203 个本地 PDF attachment，186 个 Zotero 父条目；先前按标准化标题核对为 177 篇（存在重复条目）。
160 个父条目满足元数据、期刊/主题阈值；此数字未进一步按文章去重，不能直接称作160篇独立文章。
最后一轮输出139张、104篇不同文章，每篇最多2张，250 dpi，139个独立SHA256均已重新验证。
Public实际可镜像图片为0；现有public manifest的100行都是planned占位。Combined实际文件为139，达到本次私人raw corpus数量目标。
这不代表项目原有“100张可公开镜像且完成QA”的Stage 0门槛通过；保持元素库/Router门禁不变。

## QA 状态和必须接续的工作

1. 33张已与原PDF对照检查并按精确PNG SHA256记为complete；包括当时随机10、最高相关10、每核心期刊至少3张及5张修复复查。106张仍为pending_manual_qa。
2. 最后一轮从140变139：原Science of The Total Environment条目 `6LD6WCLF` graphical abstract未被新检测逻辑重新识别，因此已从现行manifest消失。需要诊断该格式，或明确记录为排除；不要凑数补普通数据图。
3. 最后一次改动修复了两类问题：把靠近页顶的菌名误当页眉，以及Elsevier将Highlights/Graphical abstract合并成同一文本块。9项回归测试通过，但**最新输出尚未完成视觉复查**。
4. 优先复查当前sample id对应下列条目：`2UXJZ9V5` Fig3（此前顶部裁断）；`LBY4FZWM`、`I9HQ7Q29`、`TDHGXHG7` graphical abstract（此前混入Highlights/Abstract文字）；`CP39QAM5` graphical abstract（此前包含Highlights和页脚）。按item key查manifest，不要依赖旧contact sheet数字索引。
5. 已复查的 `76D7M9IR` Fig1方程面板完整，`ZEMR5578` graphical abstract已修复完整；`H6FIEJJA` Fig2和`66J4LWIV` Fig3跨栏完整；`ECS7K5X9` Fig6原稿水印保留。`ZN7J262M` Fig1仍保留轻微running-header条，已在QA备注说明。
6. 私有目录存在之前渲染但已排除的遗留PNG。当前包只收录现行manifest的139张；不要对整个旧目录计数。可后续将未引用的本次生成ZOT文件安全隔离，禁止删除Zotero原文件。
7. `manifests/zotero-visual-qa.json`记录前一轮140张时的抽样，sample_id与SHA256是权威标识，旧index仅诊断用途。最新QA helper重跑可能抽取不同随机行；补查新增样本，或明确保留原抽样队列。
8. 7张caption触发第三方adapted/reproduced风险标记。未触发不等于版权清除。全部private_local、redistribution_allowed=false。
9. 私有PNG不在GitHub包中。GitHub云端可改代码/审阅metadata和运行合成测试，但不能声称完成本地图片视觉QA。需要本机运行后回填结果。

## 运行环境及命令

从仓库根目录运行，先读AGENTS.md及项目RAW_CORPUS_POLICY.md、ZOTERO_INGEST.md。
本机虚拟环境 `.venv` 使用 `--without-pip --system-site-packages` 创建，复用已有PyMuPDF 1.27.2和Pillow 12.2.0，未修改系统环境。云端请另建venv并安装scripts/requirements.txt。

```powershell
.\.venv\Scripts\python.exe -X utf8 projects/scientific-figure-style-corpus/scripts/scan_zotero_corpus.py
.\.venv\Scripts\python.exe -X utf8 projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py --allow-other-journals --curated-only --overwrite --dpi 250
.\.venv\Scripts\python.exe projects/scientific-figure-style-corpus/scripts/test_zotero_ingest.py
.\.venv\Scripts\python.exe projects/scientific-figure-style-corpus/scripts/qa_zotero_corpus.py
.\.venv\Scripts\python.exe projects/scientific-figure-style-corpus/scripts/qa_source_pages.py
.\.venv\Scripts\python.exe -X utf8 projects/scientific-figure-style-corpus/scripts/verify_zotero_corpus.py
```

Zotero位于 `C:/Users/25019609r/Zotero`，私有PNG位于 `C:/Users/25019609r/scientific-figure-corpus-private/zotero`。
读取数据库用mode=ro内存backup；若独占锁阻碍，复制DB/WAL到临时区、验证源大小/mtime稳定和quick_check、读取内存只读快照。未写Zotero数据库或PDF。
MuPDF报告若干structure/page tree警告，但现行139张PNG可打开、尺寸和hash验证通过；警告不应静默等同于所有PDF页结构正常。

## 代码及文档待收尾

- 旧入口重复build/figure_candidates/write_manifest死代码已移除，入口委托zotero_pipeline。
- 清理和统一CLI、代码风格、摘要/排除日志：--min-required已使用；--overwrite目前仅兼容参数，每次确定性重渲染。
- 补全独立文章去重：当前输出按DOI/item限制且标准化标题验证每篇<=2；可加强跨重复条目的DOI/标题归一逻辑。
- 更新ZOTERO_INGEST.md（旧示例仍写max-per-article 3；实际CLI允许1/2）和README当前统计，不改RAW_CORPUS_POLICY标准。
- 补最终13项报告、检查所有新文件差异、确认没有私有binary被跟踪，再提交/推送现有分支。不要merge、不要改codex-playbook、不要拆元素库或训练Router。

## Git交接

分支：`feat/figure-style-corpus-v0.1`。
所有本轮修改尚未commit或push。已有PR #20： https://github.com/yichengzhao46-rgb/codex-workbench/pull/20
此前读取到open、draft=true、merged=false；打包时未重新联网刷新。
本地基线落后已fetch远端4个提交，远端改动涉及公共采集workflow、build_raw_corpus.py和新run_raw_corpus_scoped.py。
应基于最新远端应用overlay；不要用旧仓库快照回滚远端，不需要force push。保持原Draft PR。

本地基线commit：`73c7e24be3cc5c93b53ce4c66cfcb138336c6d71`
已获取的远端commit（可能已变化）：`f68fc164061f27999308ff45c9f7ac96692b7bbc`

## 期刊、用途和主题分布

### 期刊

| 类别 | 张数 |
|---|---:|
| Environmental Science & Technology | 23 |
| Nature Communications | 15 |
| Bioresource Technology | 11 |
| Chemical Engineering Journal | 8 |
| Water Research | 8 |
| Angewandte Chemie International Edition | 7 |
| The ISME Journal | 6 |
| Science Advances | 5 |
| Chemical Reviews | 4 |
| Trends in Microbiology | 4 |
| Frontiers in Microbiology | 3 |
| Nature | 3 |
| ACS Central Science | 2 |
| ACS Sustainable Chemistry & Engineering | 2 |
| Advanced Science | 2 |
| Applied and Environmental Microbiology | 2 |
| Biotechnology Advances | 2 |
| Chemosphere | 2 |
| Electrochemistry | 2 |
| Environmental Microbiology Reports | 2 |
| ISME Communications | 2 |
| Journal of the American Chemical Society | 2 |
| Small | 2 |
| Applied Microbiology and Biotechnology | 1 |
| Biochemical Engineering Journal | 1 |
| Engineering | 1 |
| Environmental Microbiome | 1 |
| FEMS Microbiology Ecology | 1 |
| Journal of Water Process Engineering | 1 |
| Microbiome | 1 |
| Molecular Systems Biology | 1 |
| Nano Today | 1 |
| Nature Biotechnology | 1 |
| Nature Catalysis | 1 |
| Nature Reviews Microbiology | 1 |
| Nature Sustainability | 1 |
| Nature Water | 1 |
| PLOS Computational Biology | 1 |
| PLoS Biology | 1 |
| Proceedings of the National Academy of Sciences | 1 |
| RSC Advances | 1 |
| Scientific Reports | 1 |
| iScience | 1 |

### Figure purpose

| 类别 | 张数 |
|---|---:|
| electron_transfer | 27 |
| metabolic_pathway | 27 |
| microbial_interaction | 17 |
| integrated_mechanism | 14 |
| graphical_abstract | 13 |
| comparative_perturbation | 10 |
| experimental_design | 8 |
| conceptual_overview | 7 |
| environmental_process | 6 |
| material_microbe_interface | 6 |
| multiscale_schematic | 4 |

### 主题（多标签，不相加为总数）

| 类别 | 张数 |
|---|---:|
| methane_methanotrophy | 82 |
| electron_transfer | 58 |
| soluble_donors_mediators | 50 |
| oxygen_redox_interfaces | 47 |
| environmental_microbiology_engineering | 42 |
| material_microbe_interfaces | 30 |
| microbial_cross_feeding | 24 |
| RP_carbon_fixation | 17 |

## 本轮新增或修改文件

- `.gitignore`
- `projects/scientific-figure-style-corpus/manifests/zotero-exclusions.csv`
- `projects/scientific-figure-style-corpus/manifests/zotero-file-verification.json`
- `projects/scientific-figure-style-corpus/manifests/zotero-ingest-summary.json`
- `projects/scientific-figure-style-corpus/manifests/zotero-private-manifest.csv`
- `projects/scientific-figure-style-corpus/manifests/zotero-qa-decisions.csv`
- `projects/scientific-figure-style-corpus/manifests/zotero-visual-qa.json`
- `projects/scientific-figure-style-corpus/scripts/ingest_zotero_figures.py`
- `projects/scientific-figure-style-corpus/scripts/qa_source_pages.py`
- `projects/scientific-figure-style-corpus/scripts/qa_zotero_corpus.py`
- `projects/scientific-figure-style-corpus/scripts/requirements.txt`
- `projects/scientific-figure-style-corpus/scripts/scan_zotero_corpus.py`
- `projects/scientific-figure-style-corpus/scripts/test_zotero_ingest.py`
- `projects/scientific-figure-style-corpus/scripts/verify_zotero_corpus.py`
- `projects/scientific-figure-style-corpus/scripts/zotero_layout.py`
- `projects/scientific-figure-style-corpus/scripts/zotero_pipeline.py`
