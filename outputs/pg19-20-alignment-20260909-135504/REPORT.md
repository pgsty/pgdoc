PG19beta3 / PG20devel 增量译文对齐验收报告
============================================

本轮已完成相对于 PG18.6 的增量范围内的审阅、译文对齐、构建和验收。共同英文的译法按准确性选定并统一；英文确有差异的部分保留各版含义、标识符、结构和链接。修改已写入 `zh/19/` 和 `zh/20/`。本轮没有提交、推送或发布。

英文依据是启动时冻结的 `en/18.6`、`en/19beta3`、`en/20`。PG20 对应提交 `86f7c82cf1023e3599f40f939727791a7090cd44`；本报告不把持续变化的上游 master 当作验收输入。术语遵循不翻译词表、术语表、译风规范和既有译文的优先级。

| 审阅范围 | 数量 / 处理 |
| --- | --- |
| 英文审阅记录 | 3,261 条，全部有结论，无待处理映射 |
| 两版英文相同的记录 | 2,206 条，其中原始同文异译候选 465 条已逐项核对 |
| 两版英文不同的候选 | 122 条，逐项保留共同部分并体现实际差异 |
| 原始单侧记录 | PG19 781 条、PG20 152 条；另识别出 WAIT FOR 重命名/重组的 7 对记录 |
| 旧中文残留候选 | 118 条，全部有修正或保留依据 |
| 共同生成表和资源 | 核对 SQL 特性、关键字、Meson 目标、等待事件及两份时态隔离图源文件 |

原始文件差异覆盖 PG19 的 177 个修改文件、58 个新增文件和 2 个删除文件，以及 PG20 的 179 个修改文件、55 个新增文件和 2 个删除文件。段落与表格条目比较结合删除、移动、重组和生成输入核对，避免仅比较当前中文文本而遗漏两版共同漏译。

最终修改 PG19 的 **69 个文件**（64 个 SGML 文件、5 个资源/本地化文件），PG20 的 **23 个文件**（22 个 SGML 文件、1 个 SVG）。记录了 471 项内容或结构修改，另有 25 处本轮新增行尾空白、SVG 字体声明修正。原有未涉及英文增量的段落和各版格式予以保留。

在可以直接选取共同译文的 365 项中，350 项采用 PG20，15 项采用更准确的 PG19；需要补译、定位纠正或拆分合并的项目另有明确记录。没有把某一版整篇覆盖到另一版。

本轮的主要修正包括：

- 统一插入清理、复制源、WAL、后台工作进程、校验和及应用时间相关增量术语和描述。
- 用 PG19 的准确说明补回 PG20 遗漏的源 WAL 发送进程、`max_files_per_process` 排除项，修正 GiST `stratnum` 的旧标识符和 `debug_print_raw_parse` 的重复段落。
- 补齐 PG19 的 `slotsync_skip_reason`、JSON 路径字符串方法、`pg_buffercache` 标脏说明、区域设置注意事项和配置进程清单；对齐正则分割示例及相关段落结构。
- 补齐 PG20 的 `jsonb_populate_record_valid`、strict JSON 对象聚合说明、整数与 `bytea` 转换、`COLLATION FOR` 示例等共同增量；补齐两版共同缺失的 JSON 宽松模式自动展开示例。
- 删除 PG19 中两版英文已经删除的 `escape_string_warning` 说明、旧正则字符串注意事项和旧逻辑复制协议说明。
- 对齐时态隔离图的中文标签，修正会触发 PDF SVG 渲染错误的字体声明；两版生成表本地化均经过构建验证。

实际版本差异已保留。例如：PG19 的属性图、分区合并拆分和 beta 协议协商说明；PG20 的 PQfn/refint 移除、ICU 最低版本、JSON_TABLE PLAN、UUID 支持范围、WAL 压缩选择和部分旧服务器兼容范围。`max`/`min` 的共同类型说明一致，PG20 的额外 UUID 支持单独保留。

| 最终构建 | 结果 | 规模 |
| --- | --- | --- |
| PG19beta3 HTML | 通过 | 1,176 个 HTML 页面 |
| PG19beta3 A4 PDF | 通过 | 3,014 页 |
| PG19beta3 US Letter PDF | 通过 | 3,184 页 |
| PG20devel HTML | 通过 | 1,157 个 HTML 页面 |
| PG20devel A4 PDF | 通过 | 2,853 页 |
| PG20devel US Letter PDF | 通过 | 3,036 页 |

最终六次构建完成于 2026-09-09 15:02–15:04（北京时间）。每次构建的中文覆盖文件均与最终输入清单逐文件匹配；两版共 971 个源文件可由启动快照和审阅修改逐字重建。英文输入及 8 份规则文件的哈希保持不变。校对前的 Git HEAD 为 `8ff9e69bff64a8f8f1bc025dc6a1faf10ad4e137`，验收时未改变。

验收证据包括：

- 六份展开后的 DocBook XML 全部通过 DTD 校验；`git diff --check` 通过；没有引入重复 ID。删除的 8 个 ID 对应已删除的旧配置说明和旧协议条目。
- 365 项统一译文在两版实际最终位置上的 730 次检查全部通过；282 项新增受保护文本检查和 112 个涉及修改的代码块检查均无未解决项。代码块比较保留既有代码或核对冻结英文，允许已审阅的注释翻译。
- 六次构建的 21 份生成表输出哈希全部匹配源目录中的本地化清单；在实际展开 XML 中核对了 26 个共同生成表条目及 19 个等待事件译文。
- 全量 HTML 内部链接及图片引用检查：除下述原有页脚邮件链接外，两版均为 0 个错误。浏览器检查 24 个页面，响应、锚点、图片均正常，未出现横向溢出。
- 渲染并目视检查 56 张 PDF 页面，包括两种纸型的封面、索引、时态图、正则示例、JSON 表、配置、libpq 和复制槽说明；中文图中文字和字体正常，抽查页面无新增裁切或重叠。

基线问题与本轮范围分开记录：四份 PDF 分别保留 PG19 A4 52 条、PG19 US 44 条、PG20 A4 20 条、PG20 US 16 条长行/行内溢出警告。已用未修改的 PG19 快照重建基线，并与原 PG20 构建逐项比对；忽略 FO 源码位置后，警告内容和溢出幅度完全相同，没有新增警告。最终四份 PDF 的严重错误及缺字警告均为 0，PG20 原有 Arial 回退警告也已消除。上游和基线的紧凑列名/类型排版、表格跨页方式保持原样。

HTML 页脚原有的 `pgsql-docs@lists.postgresql.org` 链接缺少 `mailto:`，在每页重复出现（PG19 1,176 次，PG20 1,157 次）；本轮未改动页脚模板。PG18.6 继承而来、英文未变化的译文差异和残留英文不在本轮批量修改范围内。因此本结论是增量对齐验收通过，不是全书基线零缺陷声明。

两份构建脚本在本轮构建完成后的 15:11 又出现固定归档输入和生成目标处理方面的更新。本轮没有覆盖这些更新。`patches/build-scripts.patch` 仅包含本轮引入的本地化触发条件及注释调整；校对前脚本、构建时脚本和后来观测到的差异分别保存在审计包中。六份交付产物仍对应上述已验证的最终文档源文件。

交付内容：

- [PG19 A4 PDF](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/postgresql-19beta3-zh-A4.pdf)、[PG19 US Letter PDF](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/postgresql-19beta3-zh-US.pdf)
- [PG20 A4 PDF](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/postgresql-20devel-zh-A4.pdf)、[PG20 US Letter PDF](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/postgresql-20devel-zh-US.pdf)
- [PG19 HTML 包](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/postgresql-19beta3-zh-html.tar.gz)、[PG20 HTML 包](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/postgresql-20devel-zh-html.tar.gz)
- [两版最终中文源码](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/pg19-pg20-zh-source.tar.gz)
- [PG19 补丁](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/patches/zh19.patch)、[PG20 补丁](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/patches/zh20.patch)、[本轮构建脚本补丁](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/patches/build-scripts.patch)
- [完整审计包](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/audit.tar.gz)、[交付清单](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/MANIFEST.json)、[SHA256SUMS](/Users/vonng/pgsty/pgdoc/outputs/pg19-20-alignment-20260909-135504/SHA256SUMS)

审计包内的 `checks/README.md` 指明最终验收入口。`reviews/` 保存英文比较及逐项决策，`ledgers/` 保存带源位置和前后哈希的编辑记录，`raw-diffs/` 保存原始英文差异，`visual-qa/` 保存渲染证据；历史失败候选已单独标明，不作为最终验收结果。补丁均相对于本轮启动时的中文快照生成，适用于审阅本轮变化，不应覆盖后来新增的其他工作。

完整工作记录目录：`/Users/vonng/pgsty/pgdoc/tmp/pg19-20-alignment/20260909-135504`。
