# Baudot 编码前大写转换改变非 ASCII 字符

- 受影响工具：`tools/it/baudot-code.html`
- 问题：编码前对整个输入执行 Unicode `toUpperCase()`；例如不支持的 `ß` 会变成 `SS` 并被编码，绕过不支持字符提示，结果与原输入含义不同。源码推断，待浏览器复核。
- 解决方案：逐原始字符仅将 ASCII 小写字母转为大写，其余字符按 Baudot 字符表判断支持性并明确列出；测试 ASCII 小写、ß、带变音符号字母与中文。
