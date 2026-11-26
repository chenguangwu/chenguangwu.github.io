# CSS 处理：格式化和压缩改变选择器语义

- 受影响工具：`tools/it/css-formatter.html`、`tools/it/css-minify.html`
- 问题：格式化器不区分伪类与声明冒号，`a:hover` 可能变为无效的 `a: hover`；压缩器删除冒号前空格，`.parent :hover` 变成 `.parent:hover`，改变匹配对象。依据源码推导，待浏览器复核。
- 解决方案：使用理解 CSS 语法的解析或词法处理，仅在安全上下文调整空白；比较处理前后的伪类、伪元素、后代选择器和声明解析结果。
