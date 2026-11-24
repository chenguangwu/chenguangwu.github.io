# YAML 格式化：常见序列解析失败

- 受影响工具：`tools/it/yaml-formatter.html`
- 问题：解析 `items:\n  - one\n  - two` 时抛出 `arr.push is not a function`，格式化、压缩及 YAML 转 JSON 无法处理常见的嵌套列表；`a: [one, two]` 则被当作字符串而不是数组。
- 解决方案：使用支持 YAML 语法的纯前端解析器，明确版本及支持范围；覆盖根序列、嵌套序列、对象数组和流式集合，确保转换结果保留类型及顺序。
