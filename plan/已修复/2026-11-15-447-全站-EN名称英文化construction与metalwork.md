# 447 · 全站 EN 名称英文化（construction 17 + metalwork 17）

## 问题
`construction` 与 `metalwork` 各 17 页 `en` 仍为中文名，英文态 SEO 与卡片标题退化（G05）。

## 处理
只改源 `i18n/tools/_en_override.json`，共 34 条。

construction 示例：`Room Area & Gross Floor Area Calculator`、`Formwork Support Spacing Calculator`、
`Scaffold Safety Verification Calculator`、`Construction Cost Index Calculator`、
`Construction VAT & Surcharge Calculator`、`Concrete Mix Proportion Calculator`、
`Pipe Insulation Thickness Calculator`、`Insulation Thermal & Flame Test Checker`。

metalwork 示例：`Injection Molding Flow Simulation Estimator`、`Carburizing Depth & Time Process Designer`、
`Metallographic Grain Size Analyzer`、`Gear Machining Parameter Calculator`、
`NDT Flaw Detection Compliance Checker`、`Salt Spray Test Grade Assessor`、`Heat Treatment Process Recorder`。

命名遵循 `<对象> <功能> Calculator / Estimator / Analyzer / Checker / Tool`，无尾部括号，与既有英文名不重复。

## 验证
- 两行业 `en` 含中文 **34 → 0**；全站 **642 → 608**。
- 全站 `en` 重名组 **0**；`audit_en_meta_degenerate.py --check` 无新增退化。
- `python3 _build.py` 通过。

## 后续
agriculture 15 → fitness 15 → hydraulic 15 → materials 14 → ecommerce 13 → life 12 → eco 12。
按老板要求暂不推送、不跑全量门禁。
