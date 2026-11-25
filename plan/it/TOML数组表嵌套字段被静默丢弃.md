# TOML 数组表的嵌套字段被静默丢弃

## 问题

解析嵌套表头时未进入数组表的当前元素。例如 `[[products]]` 下定义 `name = "A"`，随后用 `[products.details]` 定义 `color = "red"`，details 被挂在 JavaScript 数组的非索引属性上，JSON 序列化时消失。

## 解决方案

采用符合规范的本地 TOML 解析器，或正确定位数组表的当前元素；验证多个数组元素、嵌套表及嵌套数组表，确保结果完整且非法语法有明确提示。

## 受影响工具路径

- `tools/it/toml-to-json.html`
