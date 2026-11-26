# 文字与表情图标预览把输入当 HTML 解析

## 问题
文字和表情输入框允许普通文本，生成画布时按文本绘制，但三档预览使用模板字符串直接插入 `innerHTML`。例如输入 `<b>` 时，画布将其视为字符，预览区却将其解析为标签，导致预览与实际 PNG 不一致；用户输入不应被当作页面标记。

## 解决方案
用 `textContent` 写入预览文字，或在拼接前正确转义；验证尖括号、引号、普通字符和表情输入，确保三档预览与下载图显示一致。

## 受影响工具路径
- `tools/design/favicon-from-emoji.html`
- `tools/design/favicon-from-text.html`
