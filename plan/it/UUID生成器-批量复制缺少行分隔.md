# UUID 生成器：批量复制时结果粘连

- 受影响工具：`tools/it/uuid-v4-generator.html`、`tools/it/uuid-v5-generator.html`
- 问题：生成结果以多个相邻 `div.code-row` 呈现，复制时直接使用容器 `textContent`，相邻元素之间不会自动插入换行，多个 UUID 或“名称 → UUID”记录粘成一串，无法按行使用。
- 解决方案：从结构化结果数组按换行符序列化，明确复制 UUID 还是名称与 UUID，并在复制失败时提示用户。
- 验证建议：各生成器输出多条后粘贴到纯文本框，核对行数、顺序及每条内容。
