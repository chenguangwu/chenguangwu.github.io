# 518 批：metallurgy / procurement / property / forensic-medicine 英文态清零

- 日期：2026-11-15
- 范围：`metallurgy` 14 页、`procurement` 8 页、`property` 16 页、`forensic-medicine` 7 页，合计 168 条键。
- 手段：只改 `i18n/tools/en/<industry>/*.json` 的 `map`；
  冶炼收得率/硬度反解/扩散脱碳、供应商评分与准入、物业费分摊与绩效评级、法医推断模型整句英译。
- 备注：`forensic-medicine` 多处为列表式标签（弹道/创角/着地姿势），逐条按文本节点作键；
  单位（kJ、m²/s、MPa、℃）与规范编号保留原文。
- 验收：四行业 `--check` 均残留 0；`_build.py` 通过；`_test_static.py` 4685/4685。
