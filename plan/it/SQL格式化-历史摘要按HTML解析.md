# SQL 格式化：历史摘要按 HTML 解析

受影响工具：`tools/it/sql-formatter.html`

## 问题描述
历史摘要来自 SQL 输入，`renderHistory()` 未转义即将其拼入 `innerHTML`。包含 HTML 标签的 SQL 字符串会产生意外页面节点，并存在脚本注入风险；实际触发条件需浏览器复核。

## 解决方案
通过节点 `textContent` 渲染摘要和其他动态字段，不把用户输入拼入 HTML；使用无害标记、引号和既有历史验证显示为原文。
