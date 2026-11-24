# Base64 转图片：部分 Data URL 的下载扩展名错误

受影响工具：`tools/design/base64-to-image.html`

## 问题描述
Data URL 允许无 `;base64` 的图片，如百分号编码的 SVG；下载扩展名却用整个 `lastURL.split(';')[0]` 提取。没有分号时结果包含逗号和数据内容，文件名不再是 `.svg`。`image/vnd.microsoft.icon` 等 MIME 子类型直接作为扩展名也不符合常见文件扩展名。

## 解决方案
复用已解析 MIME，通过明确映射选择安全文件扩展名，并处理无分号、附带 charset 和 MIME 别名；验证 SVG、JPEG、ICO、PNG 的实际下载文件名及内容。
