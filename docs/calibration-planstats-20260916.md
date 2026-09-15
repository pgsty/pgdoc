PG10—PG20 规划器统计信息校准记录（2026-09-16）

从 PG18 的七块完整正文和外层框架开始，实际阅读十一版 planstats.sgml、七种完整英文变体和全部中文候选。随后完整阅读 147 个相关段落、目录／视图行、命令说明和标题，及一段非渲染发行说明注释。范围涉及 71 个文件、158 个正文范围，含 449 叶段、159 父段、399 原始块；其中 release-10.sgml 仅核对源文注释，不代表通读其整份发行说明。

本批修复八类问题，并按十一版本逐项核准：

- PS001：将普通 n-distinct 统计概念沿用性能指南和 PG10—13 的“非重复值”译法；覆盖计数、估计、统计信息、系数和命令说明，保留实际 ndistinct、n_distinct、pg_ndistinct 等标识符。
- PS002：十一版将 except 译作“除非”，把可观察到的次优计划误说成条件。改为“除了计划可能不够理想之外，对此没有直接反馈”。相关 ICU 无直接反馈段是另一语境，六版完整核准后保留。
- PS003：PG14—16 缺少本版“输出取自 8.3，其他版本行为可能不同”的提示，恢复两句；PG17 起英文移除，依本版保留差异。
- PS004：PG14—16 的连接估计说明混入新版按行数说明和字段标签，恢复本版按非重复值数量估计的完整段落及 structfield 标记；PG17 起的新说明保留。
- PS005：PG14—16 混入新版公式、BUFFERS OFF 和小数形式的 actual rows。31 个原始块恢复为对应版完整英文内容，其余 368 个原始块不变。
- PS006：PG14—17 混入 PG18 才有的 psql \do+ 检查 LEAKPROOF 提示。删除本版英文不存在的整句和两处链接；PG18—20 原文有该提示，完整保留。
- PS007：按既有词表统一“多元统计信息”和“高频值／高频值频率”，校正 PG10—13 正文中残留的“多变量”和“最常见值”译法。
- PS008：十一版性能指南将自动计算所有多元统计信息的 impractical 说成“不可能”，恢复“不切实际”，保留其应由统计信息对象指定列组的说明。

另对相同英文的直方图／MCV 计算、独立条件、函数依赖、分组计数、MCV 列表和邮政编码示例说明复用审定译文。跨原始块和行内标记分组后，58 个正文组无未决冲突；常规 79 叶段组、17 父段组、28 其他组也均已核准，保留一组既有本地标题锚点例外。最终 66 新文本组的完整正文实际复读，重复原始块由完整版本阅读与逐字节证明绑定，并以 34 个复读框架无遗漏地对应全部新单元。

共修订 50 个正文文件和 3 个规范文件。新增第 648 条 n-distinct → 非重复值，记录普通说明的计数／估计／统计信息／系数用法，明确区别 non-distinct，保留标识符、锚点和代码；九项用户回退保持。修订后 71 个涉及文件中的普通 n-distinct 残留为零，唯一文字命中是保留的非渲染源文注释。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-matrix.md)共 22 组、242 格：61 修复／复用、134 核准、40 不适用、7 例外。十一版中英文 8,523 个 SGML 文件中的 352 处相关命中全部归位：350 处绑定完整已读正文范围，2 处为同一段英文／中文发行说明注释。补充扫描处理紧邻中文的 N-distinct，保留首轮扫描证据。

完整核准行数与 relpages 缩放、等频直方图及桶内线性估计、MCV 内外的选择率、NULL 比例、直方图与 MCV 总体不重叠、独立谓词乘积、位图堆访问代价、连接选择率先于具体计划估计、函数依赖的列级局限、多列非重复值计数、MCV 实际值与兼容组合、范围条件、统计信息的 SELECT／LEAKPROOF 权限、安全屏障视图和第三方估算函数约束。源码路径、数字、逻辑连接词和全部结果逐版保留，未运行任何示例。

版本边界核准：多元 MCV 列表从 PG12 起；stxndistinct 到 stxdndistinct 及 pg_statistic_ext_data 的变化、PG14 起表达式统计信息、PG19 起虚拟生成列命令形式和 JSON 格式示例按本版处理。PG16 起第一处频率公式使用 mcv_freqs，PG17 起连接说明使用行数，PG18 起 EXPLAIN 使用 BUFFERS OFF 和小数行数，PG19 起本章示例 JOIN／ON 大写；旧版自身的 mvf／mvfs、数字和原始结构保留。9 处既有原始块行尾空格差异逐行列明，其余字节与自身英文一致。3 个既有本地锚点和 rules.sgml 三版的额外 LEAKPROOF literal 包装已核准保留。

新快照 checkpoint-planstats-ready：十一版 1,279 配对节点，6 处范围内提示全部精确绑定并归类，零未决、零漂移、零子节点差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文；规范文件等于审定追加内容。此项是解析核验，并非 HTML／PDF 构建。

前一 pageinspect 阶段已提交 39f647f6，未推送。本批准备阶段提交，继续本地化与字符集章节。历史原 2,466 待追溯单元上次核准 221、余 2,245，仍需在最终内容上重新对账；全书逐句校准、此前批次跨代码与行内标记的同源正文复核、独立追溯和十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建 0/33。

证据：[完整范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-changes.json)、[全部命中](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-all-occurrences-closure.json)、[跨标记分组](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-cross-markup-prose-groups.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-reread-proof.json)、[复读绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-new-text-bundle-binding-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-raw-proof.json)、[行尾空格](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-raw-trailing-space-proof.json)、[受保护值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-protected-proof.json)、[删除链接](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-attribute-change-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-version-boundary-proof.json)、[术语复查](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-post-apply-term-check.json)、[规范](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-norm-changes.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-native-validation.json)、[锚点提示绑定](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-native-anchor-classification-proof.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/planstats-full-reviewed-certificate.json)。
