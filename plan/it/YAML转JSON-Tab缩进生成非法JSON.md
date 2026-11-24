# YAML 转 JSON 的 Tab 缩进产生非法 JSON

- 受影响工具：`tools/it/yaml-to-json.html`
- 问题：选择 Tab 缩进时，`JSON.stringify` 的缩进参数是两个可见字符反斜杠和 t，而不是真正的制表符；非空对象输出每行前出现 `\t` 文本，作为 JSON 空白位置时无法被 JSON 解析器接受。源码推断，待浏览器复核。
- 解决方案：使用真正的制表符作为缩进参数，验证对象、数组和空结构输出均可由独立 `JSON.parse` 解析且与原数据一致。
