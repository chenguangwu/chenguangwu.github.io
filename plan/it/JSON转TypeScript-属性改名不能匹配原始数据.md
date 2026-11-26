# JSON 转 TypeScript：属性改名不能匹配原始数据

- 受影响工具：`tools/it/json-to-code.html`
- 问题：TypeScript 属性名转换为 camelCase，原键仅保留在注释中。例如 `user-name` 生成 `userName`，接口无法准确描述原始 JSON 对象，直接使用时类型和运行时字段不一致。依据源码推导，待浏览器复核。
- 解决方案：接口属性保留原始 JSON 键，必要时使用引号属性名；验证特殊字符、大小写以及可能的名称碰撞。
