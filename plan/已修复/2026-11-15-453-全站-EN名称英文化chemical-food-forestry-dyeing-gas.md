# 453 · 全站 EN 名称英文化（chemical / food / forestry / dyeing / gas 40 页）

## 问题
`chemical` 8、`food` 8、`forestry` 8、`dyeing` 8、`gas` 8 页 `en` 仍为中文名，英文态 SEO 与卡片标题退化（G05）。

## 处理
只改源 `i18n/tools/_en_override.json`，共 40 条。

- chemical：`Tank Capacity & Liquid Level Converter`、`Crude Oil API Gravity & Density Converter`、
  `Chemical Purity, Moisture & Impurity Checker`、`Chemical Purity Titration Calculator`。
- food：`Syrup Brix & Baume Converter`、`Wine Alcohol by Gravity Calculator`、
  `Seasoning Recipe Batch Scaler`、`Scoville Heat Unit Converter`、`Menu Gross Margin Analyzer`。
- forestry：`Forest Stock Volume Estimator`、`Wildlife Population Line Transect Estimator`、
  `Stand Density Index Calculator`、`Afforestation Density Optimizer`。
- dyeing：`Dye Dosage Calculator`、`Dye Liquor Ratio Calculator`、`AATCC 100 Antibacterial Test Calculator`、
  `CMC Color Difference Evaluator`。
- gas：`Residential Gas Load Calculator`、`Gas Regulator Sizing Calculator`、
  `Gas Leak Explosion Risk Checker`、`Cathodic Protection Current Calculator`。

## 验证
- 五行业 `en` 含中文 **40 → 0**；全站 **428 → 352**。
- 全站 `en` 重名组 **0**；`audit_en_meta_degenerate.py --check` 无新增退化。
- `python3 _build.py` 通过。

## 后续
nutrition 7 → data 7 → fun 7 → electronics 7 → medical 7 → transport 7 → ophthalmology 7 → logistics 7。
按老板要求暂不推送、不跑全量门禁。
