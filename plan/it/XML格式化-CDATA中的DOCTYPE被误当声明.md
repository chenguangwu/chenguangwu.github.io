# XML 格式化：CDATA 中的 DOCTYPE 被误当声明

- 受影响工具路径：`tools/it/xml-formatter.html`

## 问题描述

提取 DOCTYPE 时对全文搜索首次出现的 `<!DOCTYPE`，不区分实际声明与 CDATA 或注释中的文本。源码分析表明，合法输入 `<root><![CDATA[<!DOCTYPE other>]]></root>` 会被额外加上 `<!DOCTYPE other>`，改变原文档结构。既有任务处理真实声明的内部子集，不覆盖此情况。

## 解决方案

仅当解析结果存在文档类型时定位并保留顶层真实声明，识别过程中跳过注释、CDATA 和处理指令；验证声明前注释、无声明和内部子集等输入及美化、压缩输出。
