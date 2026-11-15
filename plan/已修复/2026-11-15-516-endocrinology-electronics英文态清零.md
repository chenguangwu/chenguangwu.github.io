# 516 批：endocrinology / electronics 英文态清零

- 日期：2026-11-15
- 范围：`endocrinology` 22 页中 20 页、`electronics` 21 页中 16 页，合计 181 条键。
- 手段：只改 `i18n/tools/en/<industry>/*.json` 的 `map`；
  内分泌判读阈值与诊断框架、电子公式与工程经验说明整句英译，`请选择…` → `Select…`，
  `如 22（14–40）` → `e.g. 22 (14-40)`。
- 备注：多处「本工具自建经验规则/非指南原文」免责句按页保留原意，明确标注 non-guideline。
- 验收：两行业 `--check` 均残留 0；`_build.py` 通过；`_test_static.py` 4685/4685。
