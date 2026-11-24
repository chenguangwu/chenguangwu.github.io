# Base64 转图片：纯 Base64 格式识别范围与支持列表不一致

受影响工具：`tools/design/base64-to-image.html`

## 问题描述
Data URL MIME 白名单包含 BMP、AVIF、ICO 等，但 `sniffMime()` 只识别 PNG、JPEG、GIF、WEBP 和部分 SVG。有效的 BMP、ICO 等纯 Base64 会显示“无效的 Base64 数据”，即使浏览器能解码加上正确 MIME 的同一图片。SVG 识别也只查看前 48 字节，带较长 XML 声明或注释的有效 SVG 可能被拒绝。

## 解决方案
扩展可靠的文件签名识别，并允许用户手动选择未知格式；区别编码错误、格式未识别和浏览器不支持。明确支持范围，用带和不带 Data URL 前缀的多格式样本验证。
