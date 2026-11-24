# 表格单元格显示 HTML 标签：健康类

## 问题描述

公共 `ToolBox.createTable()` 会转义文本；下列工具将包含 `<span>` 的状态字符串放进表格行，因此标记会作为文字显示，颜色状态不会按预期渲染。调用与公共函数已逐项对照源码，仍需浏览器核验；这些状态不应只靠颜色区分。

- `tools/elderly/assessor-risk-1.html`、`tools/elderly/assessor-36.html`、`tools/elderly/assessor-37.html`：检查或介入状态。
- `tools/fitness/detector-15.html`、`tools/fitness/assessor-63.html`：测试与质量状态。
- `tools/gastroenterology/detector-7.html`：药敏状态；需优先核对显示是否可能造成误读。
- `tools/nutrition/rater-33.html`、`tools/nutrition/self-assess-5.html`：饮食项及评分状态。

## 解决方案及验收

状态以纯文本传入表格，采用受控样式类或安全 DOM 节点提供辅助视觉提示，同时保留公共转义以保护用户输入。分别检查各种状态、读屏、深浅主题、中英文和窄屏；涉及健康判断的含义和来源由专业人员核对。
