# PostgreSQL 官方文档样式固定副本

此目录固定 `https://www.postgresql.org/media/css/docs-complete.css` 在 2026-09-26 的完整资源依赖，供 HTML 构建离线使用。它保留现有官方主题；各版本自己的 `stylesheet.css` 和覆盖规则仍按原顺序加载。构建不下载任何资源。

`manifest.json` 记录每个资源的原始 URL、下载字节 SHA-256、本地字节 SHA-256 和大小。CSS 仅将资源 URL 改成相对路径；Font Awesome 中三个原站返回 404、pgweb 仓库也不存在的 SVG 字体末尾备选已删除，仍保留 eot、woff2、woff、ttf 四种原有格式。没有改动其他 CSS 规则。图片和字体逐字节保存。

来源及许可：

- PostgreSQL 网站代码及资源：PostgreSQL License，见 `licenses/postgresql-LICENSE.txt`。官方仓库说明：<https://github.com/postgres/pgweb>，查验时提交 `f6b76f3c9e76a301c6a33e6fd790e60217303bfc`；下载资产以 manifest 的实际网络字节哈希为准。
- Bootstrap 4.4.1：MIT，见 `licenses/bootstrap-MIT.txt`。
- normalize.css 7.0.0：MIT，见 `licenses/normalize-MIT.txt`。
- Font Awesome Free 5.0.6：CSS 为 MIT，字体为 SIL OFL 1.1；保留 CSS、字体嵌入版权信息和 `licenses/fontawesome-LICENSE.txt`。
- Open Sans：Copyright 2020 The Open Sans Project Authors；字体内嵌许可为 SIL OFL。完整许可文本见 `licenses/open-sans-OFL.txt`（上游当前项目版权声明亦保留）。

`bin/prepare_html_resources.py` 校验固定副本 SHA 后复制到产物 `_static/pgweb/`，仅重写对上述精确官方入口的样式引用。普通正文外链不变。
