# 中文 SEO 描述混入英文名称和通用操作模板

## 问题描述

以下三个页面的中文 `description` 在功能描述后追加“先阅读 [英文工具名] 的输入说明，使用一组可复现的示例参数运行一次并记录结果”。该句没有补充工具能力或适用范围，英文名称混入中文描述，与自然搜索摘要不匹配；相同文案也出现在社交元数据和部分结构化数据中。

- `tools/finance/credit-card-grace-period.html`
- `tools/finance/points-redemption-value.html`
- `tools/finance/installment-real-rate.html`

## 解决方案及验收

逐页核对真实输入、结果、重要假设与限制，编写准确简洁的中文描述并适当说明适用范围；同步核对英文、繁体、Open Graph、Twitter 和 JSON-LD。不要仅为长度添加套话。构建后检查搜索摘要字段及运行时语言状态。
