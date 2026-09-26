---
name: pgdoc-terminology
description: PostgreSQL 中文文档术语校准——词表定稿后跨版本统一正文译法（词族×版本矩阵、两层台账、五步审计、豁免分类）。涉及 glossary 词条调整、术语回退、跨版本译名统一时使用。流程见 ref/terminology.md。
---

执行 pgdoc 术语校准任务。

1. 完整读取并遵循 `ref/terminology.md` 的流程、判断顺序、豁免分类与语境边界判例。
2. 判断顺序：该版英文语义 → 字面保护（exclude.tsv/保护区）→ 词条与逐条规则（glossary.tsv + glossary.rules.tsv 配套）→ 译风最小语法调整。
3. 核心约束：按词族覆盖全部适用版本，不按版本各自定译法；高歧义词从英文反向定位；词头勘误不授权改写代码；每个候选最终有明确处置（修改/已规范/带证据的豁免/未决）。
4. 词表与规则变更登记到 `docs/change.md`；交付含跨版本台账、豁免清单、各版构建验收。不提交/推送/发布。
