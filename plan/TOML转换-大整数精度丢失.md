# TOML 转换：大整数被静默舍入

受影响工具：`tools/it/toml-to-json.html`、`tools/it/toml-to-yaml.html`、`tools/it/toml-to-xml.html`

问题：解析整数时使用 JavaScript `parseInt` 并存入 Number，超过安全整数范围的合法 TOML 整数会丢失精度，例如 `9007199254740993` 可能变为 `9007199254740992`，转换结果与原配置不一致。

解决方案：解析时保留整数原始精度，按目标格式准确序列化；对无法无损表达的目标明确提示或提供可选表示方式，不得静默改值。验证正负边界、大整数及进制写法。
