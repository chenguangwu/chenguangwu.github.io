# CSV 多行单元格破坏 Markdown 表格

## 问题

CSV 解析支持引号内换行，但生成 Markdown 时直接将换行插入表格行。例如 `name,note` 后的一行 `A,"first` 换行 `second"` 会被拆成多个物理行，预览及转回 CSV 无法保留单元格结构。

## 解决方案

为单元格换行定义可逆的安全表示，或在无法无损转换时明确提示；预览与导出使用一致规则，覆盖 LF、CRLF、空行和混合引号。

## 受影响工具路径

- `tools/data/csv-to-markdown.html`
