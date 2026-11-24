# JSON 转 TOML：DEL 控制字符产生无效结果

受影响工具：`tools/it/json-to-toml.html`

`tomlVal()` 对普通字符串直接使用 `JSON.stringify()`，但该方法不会转义 DEL 字符 U+007F。实测把包含 U+007F 的字符串作为 JSON 值，页面原转换函数生成的 TOML 含原始 DEL，Python `tomllib` 报非法字符，页面转换逻辑却未发现错误。JSON 字符串可以通过 `\u007f` 表达此类输入。

解决方案：按 TOML 基本字符串规则对不允许的控制字符进行 Unicode 转义，或清晰拒绝无法保留的输入；键名和嵌套值都需覆盖。用独立 TOML 解析器验证 U+0000–U+001F、U+007F、换行、反斜杠、引号和 Unicode，并核验解析后的字符串与输入一致。
