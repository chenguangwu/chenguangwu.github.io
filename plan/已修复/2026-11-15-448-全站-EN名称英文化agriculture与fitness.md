# 448 · 全站 EN 名称英文化（agriculture 15 + fitness 15）

## 问题
`agriculture` 与 `fitness` 各 15 页 `en` 仍为中文名，英文态 SEO / 卡片标题退化（G05）。

## 处理
只改源 `i18n/tools/_en_override.json`，共 30 条。

agriculture 示例：`Crop Moisture & Dry Matter Converter`、`Greenhouse Film Rolling Time Advisor`、
`Stored Grain Pest Outbreak Temperature Alert`、`Fertigation EC & pH Dosing Calculator`、
`N-P-K Fertilizer Blending Calculator`、`Pesticide Dilution Concentration Calculator`、`NDVI Vegetation Index Analyzer`。

fitness 示例：`Running Pace Converter`、`Body Fat Percentage Estimator`、`Navy Method Body Fat Calculator`、
`Skinfold Body Fat Calculator`、`VO2max Cooper Test Estimator`、`Core Stability Assessor`。

### 重名冲突处置（未合并页面）
- `calculator-calc-soil` 与 `calc-8` 同为土壤 pH 调节，输入不同（前者按调节深度、后者按土壤缓冲能力），
  分别命名 `Lime & Sulfur Soil pH Correction Calculator` / 既有 `Soil pH Adjustment Calculator`。
- `estimate-3` 与 `calc-12` 同为灌溉用水量，输入不同（前者 Kc+ET₀+降雨、后者面积+深度+效率），
  分别命名 `Crop Evapotranspiration Irrigation Estimator` / 既有 `Irrigation Water Requirement Estimator`。
- 两组页面功能侧近重复，留待后续合并批次评估，本批仅消除英文重名。

## 验证
- 两行业 `en` 含中文 **30 → 0**；全站 **608 → 578**。
- 全站 `en` 重名组 **0**；`audit_en_meta_degenerate.py --check` 无新增退化。
- `python3 _build.py` 通过。

## 后续
hydraulic 15 → materials 14 → ecommerce 13 → life 12 → eco 12 → property 12。
按老板要求暂不推送、不跑全量门禁。
