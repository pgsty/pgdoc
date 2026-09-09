# PG10—13 分版本提交验收

2026-09-09，按用户“每个版本一组提交，分批提交这些修改”的后续指令完成本地分组提交。此前执行提示词和最终报告中的“未提交”描述其封存时点；本文件记录后续明确授权。未推送或发布。

公共构建适配单独提交；四版中文各自成笔。共享计划、任务表、来源清单和验收摘要归入最后一批。

| 分组 | 提交 | 文件数 |
|---|---|---:|
| build | `4e03c6ce2d2f2ced60fe629c3fab8c4a68aa6a7b` | 3 |
| 13 | `1b464aa6fb222af3d18d05082a484485ba8df483` | 418 |
| 12 | `521a680c50a5a2e49f409c53ca579e4f72accd43` | 412 |
| 11 | `0e8d09aebabdb6b5122d29e53f2d53fa4ee50ca4` | 388 |
| 10 | `1eaa45704f394b5abeaf544b0ce3ce42181e4a95` | 380 |

四版共1598个源文件与最终验收清单 `dd2c53ebf07c9d39d407d11c7439d1c2e21da5273bbe6da24b1d9160001ab401` 逐文件SHA256相同；提交前又读取Git暂存区blob核对内容。公共构建脚本与12项实际构建使用的脚本哈希一致。本轮只整理Git提交，没有改变已验收译文或构建输入，因此复用已有HTML/A4/US构建及视觉验收。

首次加入Git的整树包含既有空白，差异检查按原样纳入的文件报告PG13 149处、PG12 146处、PG11 136处、PG10 137处，共568处。每处均属于逐字节一致的已验收源文件，保留原格式和SQL输出字面内容；不以修改空白制造新的源码版本。公共构建适配的差异检查通过。详细位置及暂存区验证见COMMIT-VALIDATION.json。共享材料另有25781处已分类诊断：TASKS.tsv的25752处与TERMS-NEW.tsv的14处均为原有CRLF记录行尾；build-compatibility.patch的15处为空白上下文行所需的单个空格。均与原交付文件逐字节一致并保留，未分类诊断为0。

[正式交付报告](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/FINAL-REPORT.md) · [源码及产物入口](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/README.md) · [源文件哈希清单](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/final-source-manifest.json) · [提交核验记录](/Users/vonng/pgsty/pgdoc/plans/pg10-13-from-14/COMMIT-VALIDATION.json)

Git收录源码、正式计划、构建记录、验收摘要与产物校验值。完整原始diff、逐块台账、截图、HTML、PDF和审计压缩包继续保留在本地运行及交付目录；报告中的这些链接表示本地交付位置。PG14—20、AGENTS.md和其他任务的输出保持原状。
