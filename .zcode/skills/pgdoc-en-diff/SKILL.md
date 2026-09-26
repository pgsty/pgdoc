---
name: pgdoc-en-diff
description: PostgreSQL 英文文档两版本差异工作区：文件级（增删改更名清单+逐文件统计）与内容级（完整 unified diff）+ 溯源。小版本增量同步前固定英文差异、或需要审阅两版英文变化时使用。脚本 bin/diff_en_docs.py。
---

执行 pgdoc 英文文档版本差异制作任务。

1. 标准流程：`python3 bin/diff_en_docs.py <旧版> <新版>`，输出到 `en/diff/<旧版>-vs-<新版>/`：`README.md`（概览+统计+来源校验表）、`files-added.txt` / `files-removed.txt` / `files-changed.txt` / `files-renamed.tsv`（文件级）、`stats.tsv`（逐文件 ± 行数，非文本标记 `binary`）、`full.diff`（内容级完整差异，路径标 `a/<旧版>/…` `b/<新版>/…`）、`SOURCE.json`（两侧清单 SHA256 与归档校验和溯源）。
2. 小版本增量同步（如 16.14→16.15）：先用 pgdoc-en-fetch 获取新版，再制作本差异；`files-*` 清单与 `stats.tsv` 共同界定增量翻译范围，只改差异涉及的内容，同一变更在适用版本复用译文。
3. 更名按内容 SHA256 相同识别（不计内容变化）；`binary` 行为图片等非文本，不进入翻译范围。
4. 核验：`unchanged + changed + removed = FROM 侧文件数`、`unchanged + changed + added = TO 侧文件数`，两侧文件数与 SOURCES.json 登记或目录实数对照；不符即停查。
5. 纪律：差异工作区由脚本随时可再生，勿手工编辑 `full.diff`/`stats.tsv`；重生成时先删旧目录或用 `--out` 换位置；生成参数与两侧溯源以 `SOURCE.json` 为准。
