# SVG 压缩：误删 CDATA 内的文本

- 受影响工具：`tools/design/svg-minifier.html`
- 问题：移除注释选项在原始字符串上匹配 `<!--...-->`，不能区分 XML 注释与 CDATA 内的普通文本。例如 `<svg xmlns="http://www.w3.org/2000/svg"><text><![CDATA[a<!--b-->c]]></text></svg>` 会丢失文本中的 `<!--b-->`。依据源码推导，待浏览器复核。
- 解决方案：按 XML 节点类型仅移除真实注释，保留 CDATA 和文本；验证默认选项下压缩前后的文本及渲染。
