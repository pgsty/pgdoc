# 最终 r4 HTML 视觉证据验收

四版最终 HTML 构建及源清单核验通过。对 r2、归档 r3、最终 r4 的全部 4181 个文件分别重算 SHA256，三棵产物树完全相同，其中 HTML 为 4172 页。

最终源清单 SHA256：`dd2c53ebf07c9d39d407d11c7439d1c2e21da5273bbe6da24b1d9160001ab401`。四版现存源文件与清单一致，每版 r3→r4 仅 PDF 样式变化。

据此精确复用已完成的 26 个真实浏览页面、30 张实际看过的截图和 16 次真实点击记录；52 张捕获截图与全部观察记录哈希再次验证。没有新增浏览或点击，也不把全树字节比较称为逐页视觉检查。

| 版本 | HTML 页 | 全部文件 | 已浏览页 | 实看截图 | 真实点击 |
|---|---:|---:|---:|---:|---:|
| 13.23 | 1060 | 1064 | 7 | 8 | 4 |
| 12.22 | 1054 | 1057 | 7 | 8 | 4 |
| 11.22 | 1048 | 1049 | 6 | 7 | 4 |
| 10.23 | 1010 | 1011 | 6 | 7 | 4 |

原检查覆盖版本首页与目录、索引/POSIX 锚点、history 无显式 ID 小节跳转、历史 recovery.conf 或 pg_standby、COPY 版本差异、函数匹配表与 PG12/13 XMLTABLE 空格示例。最终 HTML 的原点击 href 及 fragment 再次静态核验存在。

原 r2/r3 报告、观察记录和截图字节均保留；新 JSON 记录所有最终结果 SHA、完整产物树 SHA、截图 SHA，以及 r3 构建记录迁移到 attempt-03 的精确映射。

原有英文生成界面词、源内容未变的英语索引标签与官方远程 CSS/字体依赖仍按原报告披露。本次没有重新下载外部样式资源。

- [最终 JSON 与逐页证据](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/html/HTML-VISUAL-QA-r4.json)
- [原始实际视觉报告](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/html/HTML-VISUAL-QA.md)
- [r3 中间绑定报告](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/visual-qa/html/HTML-VISUAL-QA-r3.md)

PDF 最终产物和全站链接扫描使用独立验收证据。

- [archive_build 独立 r3/r4 字节比较](/Users/vonng/pgsty/pgdoc/outputs/pg10-13-from-14-20260909-150220/html-r3-r4-byte-equivalence.json)
