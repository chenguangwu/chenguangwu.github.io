# CSV 解析：非法字段引号被静默接受

- 受影响工具路径：`tools/it/csv-to-json.html`、`tools/it/markdown-table-generator.html`

## 问题描述

两个工具都未检查引号闭合后必须是分隔符或行尾，也接受未引用字段内部的引号。源码显示，CSV 转 JSON 输入 `name,value` 换行后接 `"a"b,c` 会把首字段静默解析为 `ab`；Markdown 表格工具已有单独任务记录相同问题。两处均需浏览器复核。

## 解决方案

按字段跟踪引号状态，指出非法位置及行列；覆盖闭合后多余字符、未引用字段中的引号、合法双引号转义和跨行字段。与既有 Markdown 表格任务协同处理。
