# 统计检验极小 p 值显示为零

- 受影响工具路径：`tools/statistics/one-sample-t-test.html`、`tools/statistics/paired-t-test.html`、`tools/statistics/independent-t-test.html`、`tools/statistics/one-sample-z-test.html`
- 问题：主结果统一用四位小数显示双侧 p 值，非零且小于显示精度的概率会显示为 `0.0000`，容易被理解为概率严格为零；部分明细也固定六位。源码静态分析，极端参数下的数值下溢和页面表现待核验。
- 解决方案：对小概率使用科学计数法或明确的上限表达（如小于显示阈值），将数值下溢与数学上的零区分；显著性判断使用未格式化数值。核对主结果、明细、历史和导出，验证普通值、极小值和阈值附近。
