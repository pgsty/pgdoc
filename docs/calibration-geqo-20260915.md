PG10—PG20 GEQO 校准记录（2026-09-15）

从 PG18 开始完整读取十一版 geqo.sgml，七个主块通过完整中英文件阅读覆盖；三种完整英文变体和全部中文候选实际核对。另读十一版完整 GEQO 配置节、两个完整引用书目，33 相关范围，共 33 文件、44 范围。22 正文修订：十一版 geqo.sgml 与 config.sgml。规范仍为 647 条，九项用户回退保留。

四项问题均水平核对并修复十一版：

- GQ001：将 more fit、least fit、more-fit 的“更适合／最不适合”统一为“适应度更高／适应度最低”，与本章 fitness 定义一致。
- GQ002：“任何时刻找到的最佳序列都会被用来生成最终计划”没有准确表达单个最佳序列。改为“使用整个搜索过程中找到的最佳序列生成最终计划”。
- GQ003：geqo_pool_size 中的“池尺寸”与相邻参数“池大小”不一致，统一为池大小，即种群中的个体数。
- GQ004：geqo_seed 中的“找到的最优路径”改为搜索中找到的最佳路径，并明确不同种子可能找到更好或更差的结果，避免暗示非穷举搜索保证全局最优。

PG15 的非随机结果段复用实际读过的 PG18 译文。四组最终全文实际复读；37 叶段组、4 父段组、50 其他组核准，一组既有 GA／TSP 缩略词包装保留，无未决同源冲突。共核准 374 叶段、44 父段、14 原始代码块。代码均满足固定英文＝修改前中文＝审定中文，未执行示例。

全章核准包括连接数量与搜索复杂性、System R 算法和实现历史；种群、个体、适应度、染色体、基因和进化操作；旅行商问题的整数串与 4-1-3-2 连接树；稳态、边重组交叉、不采用独立变异操作符的说明；标准规划器对候选的代价估计、淘汰和重组、迭代停止条件；固定 geqo_seed 和其他规划器输入的重现条件；内存与重复子连接代价估计，以及 TSP 子串独立性的局限。

187 个术语节点按含义逐个绑定；population／individuals 在中文中的先后顺序因语法交换，不机械按序号配对。77 个完整参数条目核准类型、默认值、范围和联动，包括 geqo 默认启用、threshold 默认 12、effort 的 1—10 和默认 5、pool／generations 的零值自动选择、selection_bias 范围与 seed 范围；此前架构阶段修订的 threshold 内容保持。22 个完整书目保留正式作者、题名、版次、出版社、ISBN 和链接；PG10 的 ELMA04／FONG 大写目标按自身源文核准。

图形版本逐版核准：PG10—12 保留完整 ASCII 算法图和 P(t)／P''(t) 说明；PG13 起使用自身 SVG。十六个现存 SVG／Graphviz 资产及六个旧版缺席格均检查；SVG 与同版英文逐字节一致，伪代码、节点和边定义实际阅读。PG14—17 的 Graphviz 文件仅多一行既有的正确布局注释，执行定义和 SVG 均与原文一致，保留该注释。PG14—20 在普通 GA／TSP 文本上保留三处合法缩略词包装。资产最终渲染视检仍属于后续最终构建验收。

记录一类原文历史用词疑义，涉及十一版：原文先说不使用 mutation 操作符，后文又用带引号的 mutation 描述候选变化，并将 crossover 称为 mutation procedure。保留自身原文、引号及重组／变异区分，未擅改算法或声称运行验证。

十一版中英文 8,523 个 SGML 文件水平扫描，99 处问题命中全部绑定到已读完整范围；11 条实体声明、主文档包含和目标文件链核准。[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-matrix.md)共 16 组、176 格：45 修复／复用、109 核准、4 不适用、7 格式例外、11 原文疑点。这些不是缺陷总数或全书完成率。

新快照 checkpoint-geqo-ready：十一版 1,718 配对节点、24 条范围内提示全部核准，包括 22 个正式书目标题和两个既有本地 ID；零未决、零漂移、零子节点差异。PG10 多行书目标题的原生结束行定位差异，使用唯一完整标题和原文范围核准。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。全书原始审计退出码保留。

前一阶段内部架构提交 e00e3085 已核验，24 路径、未推送。本批准备阶段提交，JIT 完整章节及相关参数继续。历史原 2,466 待追溯单元累计核准 221、余 2,245；全书逐句语义校准、独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-reread-proof.json)、[代码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-version-boundary-proof.json)、[完整参数与书目](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-parameter-and-bibliography-proof.json)、[术语](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-firstterm-semantic-proof.json)、[算法资产](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-algorithm-asset-proof.json)、[缩略词](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-existing-acronym-wrapper-proof.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-source-inclusion-proof.json)、[全部命中](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-all-occurrences-closure.json)、[本地 ID](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-existing-local-ids-proof.json)、[原文疑义](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-source-questions.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-matrix.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/geqo-full-reviewed-certificate.json)。
