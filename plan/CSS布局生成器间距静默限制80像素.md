# CSS 布局生成：间距静默限制 80 像素

- 受影响工具：`tools/design/flexbox-generator.html`、`tools/design/css-grid-generator.html`
- 问题：生成时将 gap 钳制到 0–80 并回写输入框，界面未说明上限；输入 100px 会变为 80px，Flexbox 页面参考表还称允许任意长度。依据源码确认，待浏览器复核。
- 解决方案：允许合理的非负间距，或明确限制及提示；避免在逐字输入时静默改写，覆盖 0、80、100 和空值。
