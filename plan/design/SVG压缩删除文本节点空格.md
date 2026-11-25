# SVG 压缩可能删除有意义的文本空格

## 问题

压缩仅保护自身标记 `xml:space="preserve"` 的 text 元素，随后全局删除标签之间的空白。例如 `<text><tspan>Hello</tspan> <tspan>world</tspan></text>` 会丢失词间空格，改变显示内容；全局空白折叠也可能影响文本及样式内容。

## 解决方案

按 XML 结构区分可压缩区域，保留 text、tspan、继承的空白保留规则和样式内容；验证压缩前后的文本、渲染及 XML 可解析性。

## 受影响工具路径

- `tools/design/svg-minifier.html`
