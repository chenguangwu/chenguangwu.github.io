# 450 · 全站 EN 名称英文化（ecommerce 13 + life 12 + eco 12）

## 问题
`ecommerce` 13 页、`life` 12 页、`eco` 12 页 `en` 仍为中文名，英文态 SEO / 卡片标题退化（G05）。

## 处理
只改源 `i18n/tools/_en_override.json`，共 37 条。

- ecommerce：`Sales Growth Rate Calculator`、`Repeat Purchase Cycle Predictor`、
  `E-Commerce Conversion Funnel Analyzer`、`Inventory Reorder Point Calculator`、
  `Platform Commission Calculator`、`Logistics Fulfillment Lead Time Calculator`、`Competitor Monitoring Report Tool`。
- life：`Random Number Generator`、`Anniversary Countdown Tool`、`Stopwatch & Countdown Timer`、
  `Password Strength Checker`、`Store Site Selection Scoring Model`、`Phone Number Carrier & Region Lookup`。
- eco：`Solar PV Emission Reduction Estimator`、`Solid Waste Generation Estimator`、
  `Wastewater Treatment Load Calculator`、`Building Energy Use Intensity Calculator`、
  `Afforestation Carbon Sink Estimator`、`Recyclability Assessment Tool`。

## 验证
- 三行业 `en` 含中文 **37 → 0**；全站 **549 → 512**。
- 全站 `en` 重名组 **0**；`audit_en_meta_degenerate.py --check` 无新增退化。
- `python3 _build.py` 通过。

## 后续
property 12 → geology 11 → meteorology 11 → finance 11 → metallurgy 10 → photo 10 → welding 10。
按老板要求暂不推送、不跑全量门禁。
