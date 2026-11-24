# Excel 公式速查：正文宣传与实际清单不一致

受影响工具：`tools/office/excel-formula-reference.html`

## 问题描述
正文建议对比 XLOOKUP 和 VLOOKUP、确认动态数组函数支持情况，公式说明还提到 COUNTIF；实际 `DATA` 只有 12 项，没有 XLOOKUP、COUNTIF 或动态数组函数，搜索这些名称无法检索到对应条目。正文称搜索会高亮，渲染逻辑只筛选而不高亮。

## 解决方案
补充页面承诺的函数和版本兼容说明，或者调整文案使其准确反映现有功能；实现或移除高亮承诺。覆盖 XLOOKUP、COUNTIF 与无匹配搜索。
