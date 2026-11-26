# 文本编码工具：UTF-8 解码丢失开头字符

- 受影响工具：`tools/it/base64-converter.html`、`tools/it/base32-encode.html`、`tools/it/base58-encode.html`、`tools/it/octal-encode.html`、`tools/it/uuencode.html`、`tools/it/xxencode.html`
- 问题：文本解码使用默认 BOM 处理的 `TextDecoder`，会移除开头的 U+FEFF。文本 `\uFEFFabc` 编码后再解码得到 `abc`，不能无损往返；Base32 和 Base85 共用该解码器。源码及解码行为已核实，待浏览器复核。
- 解决方案：明确 BOM 作为文本字符的处理方式，提供无损解码或可选剥除；验证各编码及适用的批量模式及字符串首尾的 U+FEFF。
