# Markdown 表格：非普通空格边界被删除

- 受影响工具路径：`tools/it/markdown-table-generator.html`

## 问题描述

生成 Markdown 时只统计边缘普通空格，再用 `trim()` 删除所有边缘空白。依据源码，CSV 引号字段中的前后制表符或不换行空格会在 Markdown 输出中丢失，但 CSV 数据模型仍保留；与已有纯普通空格数量翻倍问题不同，需浏览器复核。

## 解决方案

明确支持的空白字符，按字符保留边缘内容；对 Markdown 无法无损表达的情况提供编码或提示，并对照 Markdown 渲染与 CSV 导出。
