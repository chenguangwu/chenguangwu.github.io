# URL 编解码：encodeURI 保留方括号的说明错误

- 受影响工具：`tools/it/url-encode.html`
- 问题：页面说明称 `encodeURI` 保留 `[` 和 `]`，但 JavaScript 实际会把它们分别编码为 `%5B` 和 `%5D`。例如 `encodeURI('https://x.test/a[b]')` 在 Node.js 结果为 `https://x.test/a%5Bb%5D`。可能误导用户理解编码结果。
- 解决方案：依据实际 JavaScript 标准函数修正文案及示例，单独说明完整 URL 的解析和组件编码不同；核对中英文、FAQ 和 SEO 描述，验证方括号和 IPv6 地址等场景。
