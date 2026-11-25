# JSON Schema 生成：合法键名触发数值错误

- 受影响工具：`tools/it/json-schema-generator.html`
- 问题：生成的 schema 高亮结果被当作数值文本扫描 `Infinity` 和独立的 `NaN`。例如合法输入 `{"Infinity":1}`，schema 属性名包含 `Infinity`，生成后显示数值无效错误；代码在检查前已更新 `lastSchema`，结果与操作状态可能不一致。源码分析，待浏览器复核。
- 解决方案：只校验 JSON 解析和实际数值，不扫描 schema 的文本内容；统一更新输出、树视图和可复制数据的状态。验证上述键名及启用示例时包含这类字符串的值。
