# 表格单元格显示 HTML 标签：业务与安全类

## 问题描述

公共 `ToolBox.createTable()` 会对每个单元格转义；以下页面却把 `<strong>` 或 `<span>` 字符串放进传给该函数的行数据，标签因此会显示为普通文字，而不是预期的强调或状态颜色。以下调用与公共函数已逐项对照源码，仍需用浏览器核对页面运行时是否另有处理。

- `tools/sales/commission-calc.html`：佣金合计行。
- `tools/sales/target-breakdown.html`：目标合计行；另见分类任务。
- `tools/hr/social-insurance.html`：个人、单位及总计行。
- `tools/marketing/market-share.html`：市场份额合计行。
- `tools/printing/estimate-ink.html`：墨量与成本合计行。
- `tools/hotel/checker-assessor.html`、`tools/hotel/assessor-62.html`：检查状态。
- `tools/exhibition/assessor-61.html`：评估状态。
- `tools/fire/detector-178.html`、`tools/fire/detector-176.html`：消防检查状态。

## 解决方案及验收

表格数据保持纯文本，通过明确受控的样式类或安全 DOM 构造表达合计和状态；不得为了渲染标记而关闭对用户输入的转义。逐页检查合计与状态标签、中英文、深浅主题、窄屏及读屏，并验证结果数值和导出未变化。
