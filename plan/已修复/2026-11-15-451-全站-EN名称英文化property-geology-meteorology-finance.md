# 451 · 全站 EN 名称英文化（property 12 + geology 11 + meteorology 11 + finance 11）

## 问题
四个行业共 45 页 `en` 仍为中文名，英文态 SEO / 卡片标题退化（G05）。

## 处理
只改源 `i18n/tools/_en_override.json`，共 45 条。

- property：`Property Benchmarking Gap Analyzer`、`Property Budget & Profit Planner`、
  `Utility Energy Cost Allocation Calculator`、`PDCA Property Service Quality Assessor`、
  `Fire Drill & Facility Inspection Recorder`、`Inspection Route & Schedule Planner`。
- geology：`Geological Column & Section Generator`、`Cross-Section Reserve Estimator`、
  `Trench & Channel Sampling Designer`、`Ore Grade & Cut-Off Grade Screener`、
  `Exploration Grid Spacing Planner`、`Rock Mechanics & Physical Property Tester`。
- meteorology：`Fog Visibility Condition Estimator`、`Tidal Harmonic Analysis Tool`、
  `Dew Point & Comfort Calculator`、`Radar Reflectivity Precipitation Estimator`、
  `Drought Index Assessor`、`UV Index Protection Advisor`。
- finance：`Housing Provident Fund Loan Calculator`、`Fixed Asset Register & Depreciation Tool`、
  `Liquidity & Solvency Ratio Analyzer`、`Equipment Lease Rate Calculator`、
  `Credit Assessment & Limit Manager`、`UK Sort Code Validator`。

论文式「XX 域」套话名一并改为具体对象名（如 `Word Search Puzzle Game`）。

## 验证
- 四行业 `en` 含中文 **45 → 0**；全站 **512 → 467**。
- 全站 `en` 重名组 **0**；`audit_en_meta_degenerate.py --check` 无新增退化。
- `python3 _build.py` 通过。

## 后续
metallurgy 10 → photo 10 → welding 10 → design 9 → advertising 9 → leather 9 → textile 9。
按老板要求暂不推送、不跑全量门禁。
