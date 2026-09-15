PG10—PG20 前言与安装引导校准记录（2026-09-15）

从 PG18 开始读完 intro、notation、info、legal、install-binaries、sourcerepo，覆盖 62 个完整源文件；PG10—13 无独立二进制安装章。另读 34 个关联范围，合计 80 文件、96 范围。实际阅读包括 6 个主分块、17 个完整英文变体及全部中文候选、7 组关联内容和各版安装开篇的完整变体。intro 的框架不代表其中引用的 history、problems 等章节正文已读。本批 10 个正文文件修订；规范保持 647 条，九项用户回退保持。

两类确认问题已逐版核对：

- FM001：PG14—16 的特性列表混入本版英文没有的 12 个链接，共 36 个。恢复本版不带链接的结构，保留全部 12 项特性和扩展能力；PG17—20 保留其英文已有的链接，PG10—13 核准。
- FM002：PG14—20 二进制安装章的 installation／binaries 索引词未翻译，统一为“安装／二进制软件包”。十一版主安装章和适用版 Windows 安装章的索引也核准；25 个完整索引条目全部水平对照。

[逐版矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-matrix.md)共 20 组、220 格：10 修复、157 核准、46 不适用、7 格式例外。两个最终译文组实际复读，51 个叶段同源组、6 个父段组、21 个其他组没有未决冲突。这些是列明范围的核验结果，不是全书完成率。

前言核准文档七部分、预期读者、POSTGRES 4.2 与 Berkeley 背景、对象关系型特性及扩展方式。约定核准方括号、花括号、竖线、省略号、字面符号和 SQL／shell 提示符，以及管理员与用户的广义称谓。信息来源核准 Wiki、FAQ、TODO、网站、邮件列表与参与渠道。

法律声明按本版保留年份和版权主体：PG10 为 2022，PG11 为 2023，PG12 为 2024，PG13 为 2025，PG14—20 为 2026。核准免费使用、复制、修改与分发的通知保留条件，责任和担保排除、按现状提供及不承担支持义务；PG10—12 五段旧结构与 PG13 起六段结构各自保留。

安装说明核准优先使用二进制软件包、开发工作使用源代码，以及本版下载地址。PG10—13 没有独立二进制安装文件、实体声明或包含，但原安装开篇的“阅读打包者提供的说明”完整保留；四个版本分别留下迁移边界证据。Windows 指引按版本保留 MinGW／Cygwin 与 MSVC 入口，不把后来调整回填旧版。

源码仓库说明核准 Git 镜像、克隆、分支、离线浏览和 fetch 的含义；PG10—12 的 git:// 地址、PG10—16 的 Bison／Flex／Perl 构建说明，以及 PG19 起 Git 索引结构均按自身英文保留。文中的同步时效是固定英文陈述，本批未核验远端同步状态，也未运行示例命令。

378 个叶段、47 个父段及 25 个原始块核准；全部原始块与自身英文逐字节一致且未修改。保护标记、行内值、链接和源码注释逐范围验证。七个二进制安装文件在英文普通文字 PostgreSQL 处已有额外 productname 标签，文字出现次数相同，完整段落未改动，逐处保留并单列例外。

62 条实体声明、包含和完整目标链已核准，二进制安装使用实际别名 installbin，不能按文件名猜测。新快照 checkpoint-front-matter-ready：十一版 1,310 节点精确绑定，11 条范围内 anonymous_alignment 提示全部闭合；零未决、零漂移、零子节点数量差异。当前中文＝审定稿＝新快照，固定英文＝本次解包英文。全书原始审计退出码保留，本批结论仅覆盖列明范围。

上一批 sepgsql 提交 c08d8751 已核验。本批准备阶段提交；历史、问题报告与参考书目已开始完整逐版对照。全书余项、历史 2,466 条绑定独立对账，以及十一版 HTML／A4 PDF／US PDF 共 33 个最终构建仍未完成，最终构建 0/33。

证据：[范围](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-scope-proof.json)、[修订](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-changes.json)、[复读](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-reread-proof.json)、[原始块](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-raw-proof.json)、[保护标记](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-protected-proof.json)、[行内值](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-inline-literal-proof.json)、[版本边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-version-boundary-proof.json)、[实体](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-source-inclusion-proof.json)、[安装索引](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-horizontal-installation-index-proof.json)、[旧版边界](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-absence-migration-proof.json)、[矩阵](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-matrix.json)、[新解析](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-native-validation.json)、[提示分类](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-native-classification.json)、[证书](/Users/vonng/pgsty/pgdoc/outputs/pg10-20-calibration-20260911-134417/zcode-followup/front-matter-full-reviewed-certificate.json)。
