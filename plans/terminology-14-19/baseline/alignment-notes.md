# 版本对应关系的准备阶段发现

以下是只读检查得到的已存在情况；本准备工作未修改相关文件。它们影响术语校准时如何取得同版英文证据，不应被当作本次术语修改产生的缺陷。

## PG16 的三个额外参考页

`zh/16/ref/pg_combinebackup.sgml`、`zh/16/ref/pg_createsubscriber.sgml`、`zh/16/ref/pg_walsummary.sgml` 存在，但 `en/16.15/ref/` 没有这三个文件。在 PG16 中文 [reference.sgml:239](/Users/vonng/pgsty/pgdoc/zh/16/reference.sgml:239)、[reference.sgml:269](/Users/vonng/pgsty/pgdoc/zh/16/reference.sgml:269)、[reference.sgml:277](/Users/vonng/pgsty/pgdoc/zh/16/reference.sgml:277) 中可以看到对应实体引用，不能简单当作“目录里未使用的多余文件”。

对照 `en/16.15/reference.sgml` 与 `en/16.15/ref/allfiles.sgml`，没有这些对应实体；`en/17.11` 中则存在同名参考页及引用。这足以说明当前 PG16 中英文目录存在基线对应差异，但还不足以确定项目引入这些参考页的意图。不得自行删除文件、删除引用，或把 PG17 英文当作 PG16 官方对应内容。

本次字面扫描在 `zh/16/ref/pg_createsubscriber.sgml:346` 找到词条 620（walsender）的旧中文候选“WAL 发送器”。其是否可校准必须先判断此文件的来源与适用范围，不能仅凭新译很明确就掩盖版本归属问题。具体目标行在正式执行时应重新定位。

正式执行应检查现有版本适用说明与源文件来源；若有可靠的项目约定，按该约定明确标注范围后处理。否则记录为 `BLOCKED_EVIDENCE`，保留该处并继续其他能够与同版英文匹配的工作。最终报告要区分已完成的术语迁移与这项已有基线问题，不能把未决项算作完成。

## PG14、PG15 的目录差异

PG14 另有 `ref/merge.sgml` 及上述三个参考页；PG15 另有上述三个参考页。`ref/allfiles.sgml` 中可见实体声明，但准备时未在这两版 `reference.sgml` 中看到这几个额外页的引用。声明不等于实际包含，正式执行仍需核对从 `postgres.sgml` 出发的包含关系，再决定是否属于 `ORPHAN_NOT_INCLUDED`。

PG14、PG15 的英文存在 `ref/postmaster.sgml`，对应中文目录没有同名文件；本任务不顺带补译或改造参考页结构。若它影响某个词条的对应定位，记录路径/结构差异并查找既有中文等价位置。

## 构建入口检查

六版 `make -C zh/<大版本> check-deps` 均返回 0，完整结果在 [build-readiness.json](build-readiness.json)。这只证明 Makefile 检查的命令可找到，未执行 HTML 或 PDF 构建，也未证明 DocBook catalog、XSL、Java 运行环境、FOP 或字体渲染正确。正式构建与渲染验收仍是正文校准完成后的必做步骤。
