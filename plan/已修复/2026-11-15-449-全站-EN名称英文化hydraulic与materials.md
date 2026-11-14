# 449 · 全站 EN 名称英文化（hydraulic 15 + materials 14）

## 问题
`hydraulic` 15 页、`materials` 14 页 `en` 仍为中文名，英文态 SEO / 卡片标题退化（G05）。

## 处理
只改源 `i18n/tools/_en_override.json`，共 29 条。

hydraulic 示例：`Spillway Discharge Calculator`、`Ecological Minimum Flow Calculator`、
`Vacuum Generator Flow Calculator`、`Hydraulic Pump Selection Tool`、`Hydraulic Valve Selection Tool`、
`Pipe Flow & Pressure Drop Calculator`、`Design Flood Frequency Analyzer`、`Hydraulic Oil Cleanliness ISO 4406 Checker`。

materials 示例：`Abrasive Hardness Selection Tool`、`Archard Wear Resistance Calculator`、
`Thermal Fatigue Life Calculator`、`Material Fatigue Life Calculator`、`Arrhenius Material Life Calculator`、
`High-Temperature Creep Life Calculator`、`Coating VOC & Hazardous Substance Compliance Checker`、
`Stone Color Difference & Strength Checker`。

## 验证
- 两行业 `en` 含中文 **29 → 0**；全站 **578 → 549**。
- 全站 `en` 重名组 **0**；`audit_en_meta_degenerate.py --check` 无新增退化。
- `python3 _build.py` 通过。

## 后续
ecommerce 13 → life 12 → eco 12 → property 12 → geology 11 → meteorology 11。
按老板要求暂不推送、不跑全量门禁。
