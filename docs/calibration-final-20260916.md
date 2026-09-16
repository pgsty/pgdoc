# PG18.6 主线校准与 PG10—PG20 最终验收

2026-09-16。**按最新范围，PG18.6 待续正文已完成，发现的问题已横向核验 PG10—PG20；十一版 HTML、A4 PDF、US PDF 共 33 个目标全部通过最终验收。当前无待续正文或构建验收项。**

## 已完成的正文范围

按用户最后确定的原则，以 `en/18.6/` 当前文档为入口，按顺序核对中文；发现问题后，逐版读取 PG10—PG20 各自固定英文并修复适用位置。没有扫描 Git 历史，也没有继续校对旧小版本发行说明。

原有 131 个待续文件中，130 个的正文剩余范围已经补齐；`release-18.sgml` 按用户纠偏排除。该数字表示续作清单完成情况，不表示对其余十版分别重新通读整书。累计修复 422 个不同中文 SGML 文件、41 个生成相关文件；最后一批补完 SQL 特性表、代码约定、NLS、文档指南与 131 条术语表词条。

计数已纠正：此前 423 的清单误留了 `zh/16/release-16.sgml` 一个发行说明文件，现从正文数量中剔除，为 422。

主要问题及版本边界见 [阶段记录](/Users/vonng/pgsty/pgdoc/docs/calibration-sequential-20260916.md)。原 F-001—F-026 的逐版处理见 [前期问题总结](/Users/vonng/pgsty/pgdoc/docs/calibration-20260914-status.md)。最新工作入口见 [交接文档](/Users/vonng/pgsty/pgdoc/docs/calibration-handoff-20260916.md)。

## 本轮验收补修

PDF 实际页面检查发现连续函数名列表超出页边、窄表格中的长数值或名称溢出，以及中文参数名使用西文字体度量导致错位。共享 PDF 构建入口增加打印布局处理，保留原有断行机会，在合适位置补充断行，修正中文行内字体度量，并调整窄表格中长标量值的字号。该修复对十一版、A4 与 US 两种纸张统一执行。

这部分只处理生成的 XSL-FO：SGML、HTML、标识符、链接目标和代码示例原文不变。三个保护性回归测试通过；PG18／19 整书 FO 再次处理的文字、节点顺序、非字体属性及幂等性检查通过。对应三个文件为 `bin/build_standalone_pdfsrc.sh`、`bin/prepare_chinese_pdf.py`、`tests/test_prepare_chinese_pdf.py`，单独统计，不计入正文校对文件数。

HTML 完整引用检查还发现 PG19 将 `%S`、`%s` 的两个原始 ID 同时转换为大写，造成锚点冲突。逐版核验后，仅 PG19 需要补齐已有的 PG20 保护：保留 `%S` 原始 ID，同时保持 `%s` 的旧链接。PG10—18 无这组冲突。两个目标已在实际浏览器中分别定位确认。该样式文件单独统计。

## 验收证据

- 原生整书解析：十一版全部通过。PG10 使用 OpenSP，PG11—20 使用 DocBook DTD，退出码与诊断均为 0。
- 生成内容：42 个表的结构与受保护标识符检查通过；输入哈希、匹配次数、输出哈希三类错误均在写入前被拒绝。
- 构建：以每版同一份固定文档快照生成 HTML、A4 PDF、US PDF。每次构建核对实际消费的正文、生成表和固定上游来源。
- HTML：检查全部本地页面引用、资源与锚点；浏览器检查实际中文表格和术语跳转。
- PDF：检查整书文字页边界、FOP 日志，并对每版两种纸张渲染抽页；对 PG18 发现问题的页面另做复验。抽页验收不等同于逐页人工检查所有 PDF 页面。

结果、日志、输入与产物集中在 [最终验收目录](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/)。汇总脚本 `finalize_checks.py` 同时核对当前正文、固定快照、原生解析、构建消费记录及产物哈希，避免用旧构建冒充当前结果。

## 最终构建矩阵

下面均为本轮固定输入实际生成的最终产物。总计 **12,135 个 HTML 页面、62,573 页 PDF**；检查 **333,943 条本地页面／资源引用**，缺失目标、缺失锚点及重复 ID 均为 0。

| 固定版本 | HTML 页数／产物 | A4 PDF 页数／产物 | US PDF 页数／产物 | 验收 |
| --- | ---: | ---: | ---: | --- |
| 10.23 | [1,010](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/10/html/index.html) | [2,422](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/10/postgresql-10-zh-A4.pdf) | [2,542](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/10/postgresql-10-zh-US.pdf) | 通过 |
| 11.22 | [1,048](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/11/html/index.html) | [2,547](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/11/postgresql-11-zh-A4.pdf) | [2,687](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/11/postgresql-11-zh-US.pdf) | 通过 |
| 12.22 | [1,055](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/12/html/index.html) | [2,617](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/12/postgresql-12-zh-A4.pdf) | [2,754](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/12/postgresql-12-zh-US.pdf) | 通过 |
| 13.23 | [1,061](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/13/html/index.html) | [2,631](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/13/postgresql-13-zh-A4.pdf) | [2,782](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/13/postgresql-13-zh-US.pdf) | 通过 |
| 14.24 | [1,080](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/14/html/index.html) | [2,781](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/14/postgresql-14-zh-A4.pdf) | [2,935](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/14/postgresql-14-zh-US.pdf) | 通过 |
| 15.19 | [1,088](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/15/html/index.html) | [2,826](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/15/postgresql-15-zh-A4.pdf) | [2,979](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/15/postgresql-15-zh-US.pdf) | 通过 |
| 16.15 | [1,169](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/16/html/index.html) | [2,865](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/16/postgresql-16-zh-A4.pdf) | [3,033](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/16/postgresql-16-zh-US.pdf) | 通过 |
| 17.11 | [1,143](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/17/html/index.html) | [2,903](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/17/postgresql-17-zh-A4.pdf) | [3,066](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/17/postgresql-17-zh-US.pdf) | 通过 |
| 18.6 | [1,148](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/18/html/index.html) | [2,951](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/18/postgresql-18-zh-A4.pdf) | [3,122](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/18/postgresql-18-zh-US.pdf) | 通过 |
| 19beta3 | [1,176](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/19/html/index.html) | [3,026](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/19/postgresql-19-zh-A4.pdf) | [3,197](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/19/postgresql-19-zh-US.pdf) | 通过 |
| 20 | [1,157](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/20/html/index.html) | [2,864](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/20/postgresql-20-zh-A4.pdf) | [3,043](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/artifacts/20/postgresql-20-zh-US.pdf) | 通过 |

22 本 PDF 的整书页边界检查通过，FOP 没有溢出、缺字或错误诊断；每本保留 4 条已核验的非阻断提示：Symbol／ZapfDingbats 粗体回退、缺少中文连字符词典、span 继承提示。实际查看 22 张逐版本／纸型特性表页面，并追加 PG18 复制矩阵、术语表、聚合函数表和 PG19 类型表、oid2name 示例共 10 张页面。**这是 32 张实际抽页检查，不声称逐页人工查看全部 PDF。**

最终汇总：[acceptance.json](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/acceptance.json)。页面与产物哈希核验：[visual-review.json](/Users/vonng/pgsty/pgdoc/outputs/pg18-sequential-20260916/final/visual-review.json)。构建命令、固定英文来源、输入／消费／产物哈希及全量日志在同目录对应文件中。

## 提交与保留边界

此前阶段提交为 `3f4eb05be99543d929403f79c26d5e014826e630` 和 `7af7818ed83b703c8279a72849c63731e06a4c19`；最后 30 个正文／生成映射文件已核实进入 `8fb47319d0504aef8b137c49c390aa75eeaf2c5c`。共享工作区另一任务同时提交，因此该提交还含它的一个 PG9.3 文件；这里记录实际情况，不重写共享提交。构建修复已独立提交 `28ffbb399accfd2715c74a6bd1db5e8f36ac039d`，只包含 PDF 构建入口、打印处理器、三个回归测试及 PG19 HTML 样式四个文件。本报告及交接文件单独提交；最终文档提交号保存在本机 `final/completion.json`。

早先误做的 `zh/10/release-10.sgml` 至 `zh/18/release-18.sgml` 修改仍单独保留，不纳入本轮正文提交，也不计为校对进度。构建对应保存下来的当前工作区快照，包含这些保留内容；它不是仅凭某一个提交即可重现的纯提交树。固定输入和哈希已随验收证据保留。本任务没有推送或发布。

固定英文自身的疑点按既定边界保留；例如 GID 长度、动态探针参数编号、逻辑解码示例输出等，不能擅自改写原文含义。HTML 的 `rev="made"` 作者邮箱元数据与十一版各自英文一致，单列记录，不计为正文导航链接。

已清理本轮 127.5 MiB 的失效排版中间文件；保留最终产物、约 117 MiB 的十一版正文快照、小型日志、检查记录及抽页图片。构建临时源树自动清理，不恢复此前已清除的大型历史缓存。
