# HTML 压缩：行内元素间距被删除

- 受影响工具：`tools/it/html-minifier.html`
- 问题：安全模式把 canvas、video、audio、iframe 等标签当作块级边界删除相邻空格；这些元素可以参与行内排版，例如 `<span>A</span> <canvas></canvas> <span>B</span>` 的间距会丢失。CSS 也可以改变其他标签的 display。依据源码推导，待浏览器复核。
- 解决方案：默认保守保留可能影响行内排版的空格，不仅凭标签名推断布局；验证替换元素、CSS 指定 inline 和常见块级元素的压缩结果。
