# Properties 序列化键名未转义空格及注释符

- 受影响工具：`tools/it/properties-parser.html`
- 问题：美化或 JSON 转 Properties 时，`escapeKey` 仅转义反斜杠、等号和冒号；键包含空格时会被重新解析为另一个键，键以 `#` 或 `!` 开头时输出可能成为注释。源码分析，需用 Java Properties 验证往返结果。
- 解决方案：完整转义键中的空白、控制字符和会影响行解析的注释符，正确处理值的前导空格；验证 JSON→Properties→解析的键值一致性。
