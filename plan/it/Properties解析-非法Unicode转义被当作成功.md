# Properties 解析静默接受非法 Unicode 转义

- 受影响工具：`tools/it/properties-parser.html`
- 问题：`__ppUni()` 遇到不完整或含非十六进制字符的 `\u` 转义时丢掉反斜杠并继续解析。例如 `a=\u12G4` 被当作普通文本并显示成功，不能反映 Java Properties 的非法转义错误。源码已核实，待与 Java 实现及浏览器复核。
- 解决方案：对格式错误的 Unicode 转义报告行号及位置，停止生成成功结果；覆盖键和值、合法四位转义、字面双反斜杠、截断及非法字符。
