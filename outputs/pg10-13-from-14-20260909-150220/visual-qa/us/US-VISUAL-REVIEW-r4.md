# PostgreSQL 10—13 正式 r4 US PDF 视觉验收

四份正式 US PDF 共实际查看 **53 页**，全部通过。已查看页面未发现裁切、重叠、缺字或表格越界。结论仅覆盖以下实际查看范围，不代表全书逐页审阅。

最终源清单 SHA256：`dd2c53ebf07c9d39d407d11c7439d1c2e21da5273bbe6da24b1d9160001ab401`。

| 版本 | 实际查看物理页 | 页数 | 结果 |
|---|---|---:|---|
| 13.23 | 1, 3, 35, 46, 190, 457, 732, 748, 787, 2260, 2740, 2741, 2742, 2780 | 14 | PASS |
| 12.22 | 1, 3, 34, 45, 190, 198, 475, 783, 1926, 1927, 2719, 2720, 2721, 2747 | 14 | PASS |
| 11.22 | 1, 3, 34, 45, 184, 451, 1889, 1890, 2660, 2661, 2662, 2687 | 12 | PASS |
| 10.23 | 1, 3, 33, 43, 44, 171, 425, 1775, 1776, 2512, 2513, 2514, 2542 | 13 | PASS |

PG10物理43页的version()结果在44页延续，已查看两页；长预格式行按显示断点续行。标签/值表在相邻页延续，原始单元格内容由FO守恒审计独立核对。

Table of Contents、Synopsis、Note、Table、Section、Index及冻结底稿既有英文短索引词保留，单独记录为继承行为。

逐页检查主题、PNG/PDF/构建记录SHA与未查看截图列表见 [机器可核验记录](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/US-VISUAL-REVIEW-r4.json)。

**PostgreSQL 13.23**

[正式PDF](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/13-US/postgresql-13.23-zh-US.pdf)；SHA256 `b7d82a8ec0ae7c74b2d0d95a03adeab182e42367ee328b4bf01d60adbc466f57`。

- [物理页 1](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-0001.png)：封面13.23，通过。
- [物理页 3](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-0003.png)：目录，通过。
- [物理页 35](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-0035.png)：历史正文与Postgres95，通过。
- [物理页 46](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-0046.png)：version()长代码输出，通过。
- [物理页 190](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-0190.png)：日期时间边界值表，通过。
- [物理页 457](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-0457.png)：全文搜索长函数签名及代码，通过。
- [物理页 732](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-0732.png)：高可用矩阵Londiste/Slony/pglogical，通过。
- [物理页 748](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-0748.png)：热备历史正文，通过。
- [物理页 787](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-0787.png)：探针表InvalidBackendId，通过。
- [物理页 2260](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-2260.png)：遗传查询优化器SVG图与箭头，通过。
- [物理页 2740](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-2740.png)：pg_standby标题与历史正文，通过。
- [物理页 2741](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-2741.png)：pg_standby选项和连续分页，通过。
- [物理页 2742](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-2742.png)：pg_standby Linux/Windows命令换行，通过。
- [物理页 2780](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/13/page-2780.png)：双栏索引与BGWORKER长常量，通过。

**PostgreSQL 12.22**

[正式PDF](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/12-US/postgresql-12.22-zh-US.pdf)；SHA256 `e5cf74c3f6e2762e7bd4da2782a4c504fe0bda61d54614dc6c5312f3447ab406`。

- [物理页 1](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-0001.png)：封面12.22，通过。
- [物理页 3](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-0003.png)：目录，通过。
- [物理页 34](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-0034.png)：历史正文，通过。
- [物理页 45](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-0045.png)：version()长代码输出，通过。
- [物理页 190](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-0190.png)：日期时间边界值表，通过。
- [物理页 198](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-0198.png)：间隔输出ISO格式与布尔表，通过。
- [物理页 475](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-0475.png)：全文搜索长函数签名及代码，通过。
- [物理页 783](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-0783.png)：pg_stat_database_conflicts表与自动交叉引用，通过。
- [物理页 1926](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-1926.png)：pgbench长整数与浮点数，通过。
- [物理页 1927](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-1927.png)：pgbench连续分页和标签/值表，通过。
- [物理页 2719](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-2719.png)：pg_standby标题与历史正文，通过。
- [物理页 2720](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-2720.png)：pg_standby选项和连续分页，通过。
- [物理页 2721](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-2721.png)：pg_standby Linux/Windows命令换行，通过。
- [物理页 2747](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/12/page-2747.png)：双栏索引与BGWORKER长常量，通过。

**PostgreSQL 11.22**

[正式PDF](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/11-US/postgresql-11.22-zh-US.pdf)；SHA256 `3888eee78c5da3e58a5a172553f1c8a848df0528f1e21ec50ea64e5b28fb0386`。

- [物理页 1](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-0001.png)：封面11.22，通过。
- [物理页 3](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-0003.png)：目录，通过。
- [物理页 34](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-0034.png)：历史正文，通过。
- [物理页 45](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-0045.png)：version()长代码输出，通过。
- [物理页 184](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-0184.png)：日期时间边界值及旧时间类型表，通过。
- [物理页 451](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-0451.png)：全文搜索长函数签名及代码，通过。
- [物理页 1889](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-1889.png)：pgbench标签/值表与长数值，通过。
- [物理页 1890](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-1890.png)：pgbench续页、负整数及浮点输出，通过。
- [物理页 2660](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-2660.png)：pg_standby标题及recovery.conf历史配置，通过。
- [物理页 2661](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-2661.png)：pg_standby选项和连续分页，通过。
- [物理页 2662](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-2662.png)：pg_standby Linux/Windows命令换行，通过。
- [物理页 2687](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/11/page-2687.png)：双栏索引与BGWORKER长常量，通过。

**PostgreSQL 10.23**

[正式PDF](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/10-US/postgresql-10.23-zh-US.pdf)；SHA256 `c406e7152616967ecd9bcfb9cb6cf8563931d4695a1954ab49f4f537e937d76b`。

- [物理页 1](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-0001.png)：封面10.23，通过。
- [物理页 3](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-0003.png)：目录，通过。
- [物理页 33](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-0033.png)：历史正文保留二十多年版本措辞，通过。
- [物理页 43](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-0043.png)：version()查询与跨页表头，通过。
- [物理页 44](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-0044.png)：version()输出连续页与psql命令，通过。
- [物理页 171](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-0171.png)：日期时间边界值与bytea转义表，通过。
- [物理页 425](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-0425.png)：全文搜索长签名及EXECUTE PROCEDURE代码，通过。
- [物理页 1775](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-1775.png)：pgbench历史函数表，通过。
- [物理页 1776](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-1776.png)：pgbench续页、数值及分布公式，通过。
- [物理页 2512](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-2512.png)：pg_standby标题及recovery.conf历史配置，通过。
- [物理页 2513](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-2513.png)：pg_standby选项和连续分页，通过。
- [物理页 2514](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-2514.png)：pg_standby Linux/Windows命令换行，通过。
- [物理页 2542](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/us/10/page-2542.png)：双栏索引与BGWORKER长常量，通过。
