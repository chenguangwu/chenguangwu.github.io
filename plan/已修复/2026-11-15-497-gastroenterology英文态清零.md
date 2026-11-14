# 497 · gastroenterology 英文态清零（13 页 32 条）

## 问题
- 13 页共 30 处下拉框「请选择…」未译；
- `stool-occult-quant` 的 FIT/粪钙卫蛋白联合判读算法与两组算例未译。

## 处理
只改源 `i18n/tools/en/gastroenterology/<slug>.json` 的 `map`，共 32 条。
`请选择…` 统一译为 `Select…`。

## 验证
- gastroenterology 行业 `--check` **残留 0**（22 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
