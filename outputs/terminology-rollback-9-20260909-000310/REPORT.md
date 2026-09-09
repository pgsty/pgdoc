# PG14—19 九项术语回退验收

已完成用户指定的九项回退及必要关联规则。最终在中文源文中应用 1,895 个定点原子修改，涉及 321 个文件；其中 1,626 个撤回此前校准，269 个补齐对应概念、索引或简介。当前可确定的回退未决项为 0。

本次保留现场既有人工修改和其他术语。开工核对时，中文源文件与上一交付一致；现用九项规则已经由此前本地规则回退更新，本轮保留并验证该工作，没有整体安装复审候选。原始词表、冻结 refs、复审材料、旧备份、旧执行台账及两次旧交付均保持完整。

| 序号 / 术语 | 回退前 → 回退后 | 正文原子数 | 涉及版本与文件 | 六版核对结果 | 验证 | 未决 |
|---|---|---:|---|---|---|---:|
| 27 B-tree | B 树（词表）；B-tree / B-Tree / 概念性 btree（正文） → **B-树** | 1,691 | PG14—19；277 文件；indices、btree、操作符类、发布说明等；包含关联索引及简介 | 六版概念统一；真实方法名与缩写等逐项保留 | 规则、范围与六版验收通过 | 0 |
| 127 default B-tree operator class | 默认 B-tree 操作符类 → **默认 B-树操作符类** | 66 | PG14—19；30 文件；func、gin、queries、ref/create_type、xindex | 六版各 11 处；计入第 27 项，不重复累计 | 规则、范围与六版验收通过 | 0 |
| 179 first-committer-win | first-committer-wins / 先提交者胜出 → **first-committer-win / 以先提交者为准** | 0 | PG14—19；现用词表、规则、别名及开工材料 | 六版未发现该词条的历史正文修改；相关 MVCC 语境已核查 | 规则、范围与六版验收通过 | 0 |
| 180 first-updater-win | first-updater-wins / 先更新者胜出 → **first-updater-win / 以先更新者为准** | 0 | PG14—19；现用词表、规则、别名及开工材料 | 六版未发现该词条的历史正文修改；相关 MVCC 语境已核查 | 规则、范围与六版验收通过 | 0 |
| 199 full-page image | 整页映像及同对象页面映像/映像 → **整页镜像及同对象页面镜像/镜像** | 156 | PG14—19；47 文件；config、wal、monitoring、generic-wal、pgstatstatements、EXPLAIN、pg_waldump、发布说明 | 六版已核；含存储的镜像等明确回指，其他 image 对象保留 | 规则、范围与六版验收通过 | 0 |
| 213 header data | 头部数据 → **首部数据** | 0 | PG14—19；现用词表、规则、别名及开工材料 | 六版无历史正文动作；48 处相关类型标识符已核并保持原样 | 规则、范围与六版验收通过 | 0 |
| 267 Join Types and Methods | 连接类型与方法 → **连接类型和方式** | 0 | PG14—19；现用词表、规则及开工材料 | 六版无该组合标题的历史修改；独立 Join Types 等按原文保留 | 规则、范围与六版验收通过 | 0 |
| 385 percentiles | 百分位数 → **百分位点** | 48 | PG14—19；18 文件；func（PG19 为 func/func-aggregate）、syntax、xaggr | 六版各 8 处；独立 discrete percentile 的离散百分位数保持原样 | 规则、范围与六版验收通过 | 0 |
| 600 Value Insertion | 值插入 → **插入值** | 0 | PG14—19；现用词表、规则、别名及开工材料 | 六版未发现该标题的历史正文修改；句中插入值表达按实际句法保留 | 规则、范围与六版验收通过 | 0 |

原子修改是可定位的文本片段，不等同于独立语义位置；一句简介可包含两个片段。所有实际文件与当前行号见 [FILES.md](FILES.md)、[POSITIONS.tsv](POSITIONS.tsv)。完整英文依据、前后文本和六版处置见 [逐位置台账](ledgers/applied-edits.current.jsonl) 与 [六版核对索引](ledgers/position-six-version-links.jsonl)。

第 179、180 项英文词头恢复单数 `win`，`wins` 保留为检索别名，文献和代码的实际拼写不改。已撤销说明性正文 B-tree 必须保留英文的规定。当前词表和逐条规则均为 631 条，别名表 25 条，字面保护说明 48 条；除指定九项外，仅同步第 36 项 backup block 对整页镜像的关联规则。译风和排除表保持原样。

跨版总账包含 299 个语义单元、1,794 个版本格及 54 个术语/版本格。旧台账中标记九项的 1,644 个片段已全部给出唯一处置：1,626 个撤回，18 个实际属于‘连续’限定词或独立离散百分位词条的片段保留。另有 4,778 个非目标历史片段完整保留，其中包括 12 个第 137 项修改。

B-tree 保留清单的 512 个位置也已闭合：214 个普通概念统一，六个定义位置补入中文并保留 acronym，34 个实际访问方法名、24 个扩展名和 234 个代码/输出/引用位置保留。逐条依据见 [保留审计](ledgers/btree-retention-final-dispositions.jsonl)。首次审查中过窄的范围分类在新记录中明确撤回，原审查文件保留。

| 版本 / 固定英文 | HTML | A4 PDF | US PDF |
|---|---|---|---|
| PG14 / 14.24 | [通过，1,080 页](builds/14/html/html/index.html) | [通过，2,895 页](builds/14/A4/postgresql-14-zh-A4.pdf) | [通过，3,056 页](builds/14/US/postgresql-14-zh-US.pdf) |
| PG15 / 15.19 | [通过，1,072 页](builds/15/html/html/index.html) | [通过，2,908 页](builds/15/A4/postgresql-15-zh-A4.pdf) | [通过，3,077 页](builds/15/US/postgresql-15-zh-US.pdf) |
| PG16 / 16.15 | [通过，1,145 页](builds/16/html/html/index.html) | [通过，2,918 页](builds/16/A4/postgresql-16-zh-A4.pdf) | [通过，3,078 页](builds/16/US/postgresql-16-zh-US.pdf) |
| PG17 / 17.11 | [通过，1,143 页](builds/17/html/html/index.html) | [通过，2,898 页](builds/17/A4/postgresql-17-zh-A4.pdf) | [通过，3,061 页](builds/17/US/postgresql-17-zh-US.pdf) |
| PG18 / 18.6 | [通过，1,148 页](builds/18/html/html/index.html) | [通过，2,934 页](builds/18/A4/postgresql-18-zh-A4.pdf) | [通过，3,099 页](builds/18/US/postgresql-18-zh-US.pdf) |
| PG19 / 19beta3 | [通过，1,176 页](builds/19/html/html/index.html) | [通过，3,010 页](builds/19/A4/postgresql-19-zh-A4.pdf) | [通过，3,179 页](builds/19/US/postgresql-19-zh-US.pdf) |

上表 18 个目标均为最终源码重新实际构建，命令退出码全部为 0，构建前后及验收时源码哈希一致。A4 尺寸为 595.275 × 841.889 pt，US 为 612 × 792 pt。命令、时间、日志和产物 SHA-256 见 [构建验收](audit/build-validation.json)。初轮 builds 及中止的 builds-r2 不计入最终验收，交付链接只指向 builds-r3。

源码验收覆盖 2,637 个中文文件、2,353 个英文文件与 3,172 个历史材料；3,366 个唯一证据对象校验通过。全部差异可由授权片段精确重建，SGML 标记、属性、ID、链接、实体、注释、代码及字面标识符保持不变，git diff --check 通过。构建器使用 loaddtd，本报告证明实际解析、渲染及结构不变量，不宣称另行做过严格 DTD 验证。

最终 HTML、PDF 代表页的实际目视记录，以及索引 see/seealso 的六版检查，见 [最终验收汇总](audit/final-acceptance.json)。视检范围是记录中的代表页，不是逐页人工审阅整套手册。

最终 12 份 PDF 的 532 条 FOP 警告与旧基线逐条一致，其中 484 条溢出的对象和数值均未变化；没有新增错误或溢出。既有 FDW 长标识符裁切附新旧实页证据保留。PG14、PG17 A4 比旧交付各减少一页，其余 PDF 页数不变。详见 [构建诊断](reviews/build_diagnostics/FINAL-README.md)。六版索引也未新增悬空引用，旧基线 PG14/15 各六项、PG16—19 各五项保持原样。

既有技术内容或链接观察去重后共 39 条，详见 [BASELINE-OBSERVATIONS.md](BASELINE-OBSERVATIONS.md)。这些是位置观察，不是 39 个独立新增缺陷。已知名词回退照常完成，技术缺位未借同版的其他术语出现冒充功能依据，也未混入功能修订。

当前生效开工材料已同步至 [ACTIVE.md](../../plans/terminology-14-19/ACTIVE.md)、[ROLLBACK-9.md](../../plans/terminology-14-19/ROLLBACK-9.md)、PROMPT、USAGE、README、PLAN 及 families。词表、逐条规则、别名和字面保护说明的最终快照见 [快照说明](SNAPSHOTS.md)，本轮修订追加在 tmp/ref/change.md。

本地修改和验证已完成；未提交、推送或发布。
