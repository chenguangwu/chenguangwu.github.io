# Sitemap 生成器：字段说明与输出不符

- 受影响工具：`tools/it/sitemap-generator.html`
- 问题：页面说明称每个 URL 含 loc、lastmod、changefreq、priority；实际只输出 loc 和用户填写时的 lastmod，界面没有后两项设置。依据源码确认，待浏览器复核。
- 解决方案：准确说明现有输出和可选字段，并同步中英文与 SEO；如后续增加字段设置，说明搜索引擎对字段的实际支持并覆盖空日期。
