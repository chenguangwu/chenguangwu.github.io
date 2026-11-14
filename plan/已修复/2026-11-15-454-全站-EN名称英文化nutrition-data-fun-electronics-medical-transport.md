# 454 · 全站 EN 名称英文化（nutrition / data / fun / electronics / medical / transport 42 页）

## 问题
六个行业共 42 页 `en` 仍为中文名或中英混排（如 `CSV  Markdown 表格`、`mmol/L  mg/dL`），
英文态 SEO 与卡片标题退化（G05）。

## 处理
只改源 `i18n/tools/_en_override.json`，共 42 条。

- nutrition：`Vitamin C & Zinc Intake Recommender`、`Nutrient Reference Value Percentage Calculator`、
  `Mediterranean Diet Adherence Scorer`、`Chinese Balanced Diet Guideline Self-Assessment`。
- data：`Random Chinese Name Generator`、`CSV to Markdown Table Converter`、`CSV to JSON Array Converter`、
  `YAML JSON Converter`（避开与 `it/csv-to-json` 的既有 `CSV JSON Converter` 重名）。
- fun：`24 Game Puzzle Generator` / `24 Game Puzzle Solver`（生成与求解分列）、`Sudoku Generator & Solver`、
  `Maze Generator & Solver`、`Laugh Sound Effect Synthesizer`、`Harbor Container FPS Demo Game`。
- electronics：`RC Time Constant Calculator`、`Amplifier Power & Distortion Calculator`、
  `Antenna Length & Gain Calculator`、`LDO vs DC-DC Power Efficiency Calculator`。
- medical：`Blood Glucose Unit Converter`、`IV Drip Rate Calculator`、`Weight-Based Drug Dosage Calculator`、
  `Urinary Stone Risk Assessor`、`Medication Expiry Alert Tool`。
- transport：`Freight Volumetric Weight Calculator`、`Tire Size Upgrade Calculator`、
  `Container Loading Quantity Estimator`、`Fuel Cost per Trip Calculator`
  （避开与 `automotive/fuel-cost-calculator` 重名）、`Vehicle Depreciation Calculator`。

## 验证
- 六行业 `en` 含中文 **42 → 0**；全站 **352 → 310**。
- 全站 `en` 重名组 **0**；`audit_en_meta_degenerate.py --check` 无新增退化。
- `python3 _build.py` 通过。

## 后续
ophthalmology 7 → logistics 7 → fire-rescue 7 → it 6 → rental 6 → surveying 6 → woodwork 6。
按老板要求暂不推送、不跑全量门禁。
