# curl 解析：合法请求文本触发无效数值错误

- 受影响工具：`tools/it/curl-parser.html`
- 问题：解析后的 URL、请求头和正文组成 HTML 后，代码对整段内容检查 `Infinity` 或独立的 `NaN`。例如 `curl https://example.com/Infinity` 是合法请求，但会显示数值无效错误，无法查看解析结果。源码分析，待浏览器复核。
- 解决方案：移除对请求文本的数值关键字扫描，保留输出转义；用 URL、请求头和请求体分别包含 `NaN`、`Infinity` 的请求验证结构化结果与原始内容一致。
