PG10—PG20 JIT 校准记录（2026-09-15）

从 PG18 开始完整读取 PG11—20 的 jit.sgml，实际核对五种完整英文变体及所有中文候选；十一块 PG18 主块通过完整文件阅读覆盖。另读 110 个完整相关条目：十项 JIT 参数和 LLVM 编译选项各十版。共 30 文件、120 范围，20 正文文件修订。PG10 的文件、实体声明、主文档包含、JIT 参数及 LLVM 选项均确认缺席，不回填未来功能。规范仍为 647 条，九项用户回退保留。

五类问题均扫描十一版并按自身英文处理：

- JI001：PG11—20 普通概念索引 Just-In-Time compilation 译为“即时编译”；受保护缩略词 JIT 保留。
- JI002：PG11—20 的“不如生成”将可行方式改成建议，修为可以生成专用于表达式、由 CPU 原生执行的函数，以取代通用求值代码。
- JI003：PG14—16 的六个完整 EXPLAIN 输出误用了未来版本。逐版恢复自己的原文输出，核准估计行数格式、Buffers 行、Deform 时间和结果行数提示。
- JI004：PG14—20 的“很可能会大于潜在节省”未准确表达本例编译开销会超过节省时间。修为“JIT 的开销会超过可能节省的时间”；PG11—13 原有比较正确，在保留自身原始输出的前提下复用相同英文的审定译文。
- JI005：PG11—20 的优化阈值说明将 unlikely 弱化为“也未必有益”，且加入“更能够”的比较。修为“也不太可能有益”和“但可以提高执行速度”。

LLVM 支持条件和关闭 JIT 的说明复用相同英文下已经读过的 PG13 译文，保留原有代码、链接和属性。九组最终新文本实际完整复读，包括四组带完整输出的示例变体。共核准 350 叶段、30 父段；48 同源叶段组、5 父段组和 36 其他组无未决译文冲突。空 ulink 的长短标记仅在只读比较器内归一，正文属性不变。

完整章节核准包括表达式求值和元组变形；内联、轻量与昂贵优化；总估计代价和计划时决策；通用预备计划读取 PREPARE 时参数；扩展 bitcode 的 PGXS 支持、目录和索引文件；替代提供者的初始化入口和三个回调。代码、标识符、路径及链接均按自身版本核准。

40 个原始块修改后均与同版固定英文逐字节相同，其中六个错误输出恢复，其余 34 个修改前后均等于原文。PG11—17 的 rows=1／356、PG18 起的小数格式和 Buffers 行分别保留；Deform 时间仅 PG17 起存在，结果行数提示保留至 PG17。PG11—12 与 PG13 起的零宽空格实体差异保留。未执行 SQL、C 代码、配置命令或任何示例。

参数按自身版本核准：jit 默认在 PG11、19、20 为 off，PG12—18 为 on；LLVM 最低版本在 PG11—16 为 3.9、PG17 为 10、PG18—20 为 14。调试和性能分析支持在 PG11—13 只能于服务器启动时设置，PG14 起改为会话开始时，PG15 起允许相应 SET 权限。提供者仍仅服务器启动时设置。代价默认值 100000／500000、-1 禁用、阈值关系、profiling 路径变化、LLVM_CONFIG／CLANG／CXX 及旧版 llvm-config-$major-$minor 查找方式均核准。

十一版中英文 8,523 个 SGML 文件水平扫描，117 处问题命中均绑定到已读完整范围。实体核准包括十个实际包含链和 PG10 的缺席证据；两个既有本地 ID 保留。[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-matrix.md)共 19 组、209 格：50 修复／复用、140 核准、19 不适用。这些不是缺陷总数或全书完成率。

新快照 checkpoint-jit-ready：十一版解析检查完成，范围内 1,240 配对节点、2 条提示全部核准；提示均为既有本地 ID。零未决、零漂移、零子节点差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。全书原始审计退出码保留；此次解析并非 HTML／PDF 构建。

前一 GEQO 阶段提交 8c771380 已核验、未推送。本批准备阶段提交，继续并行查询。历史原 2,466 待追溯单元累计核准 221、余 2,245；全书逐句语义校准、独立对账及十一版 HTML／A4 PDF／US PDF 共 33 项最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-reread-proof.json)、[代码](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-protected-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-version-boundary-proof.json)、[完整参数](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-complete-parameter-proof.json)、[实体及缺席](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-source-inclusion-proof.json)、[全部命中](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-all-occurrences-closure.json)、[本地 ID](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-existing-local-ids-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-matrix.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/jit-full-reviewed-certificate.json)。
