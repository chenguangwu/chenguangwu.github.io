# 524 批：science 英文态清零（四）quartile / root —— science 收口

- 日期：2026-11-15
- 范围：`quartile-calculator`（27 条）、`root-calculator`（25 条），共 52 条键。
- 手段：只改 `i18n/tools/en/science/*.json` 的 `map`；分位位置约定、IQR/1.5 倍界、根式化简与复数分支整段英译。
- 备注：`quartile` 的「Q₂ 即中位数」「IQR=Q₃−Q₁」、`root` 的「直角三角形的斜边」「标准差 σ」均被行内元素拆开，
  按片段作键（片段本身以 `。`、`=Q₃−Q₁；` 开头，英文片段保留对应标点）。
- 验收：`--check science` **90 页残留 0**；`_build.py` 通过；`_test_static.py` 4685/4685。
- 结论：science 全部 11 页清零，本轮全站「英文态内容区零中文」行业清单已全部消化。
