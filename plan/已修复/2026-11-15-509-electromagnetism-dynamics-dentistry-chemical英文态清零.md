# 509 · electromagnetism / dynamics / dentistry / chemical 英文态清零（22 页 43 条）

## 问题
- `electromagnetism` 3 页、`dynamics` 7 页：物理公式「校验 + 判据」说明整段中文；
- `dentistry` 5 页：`请选择…` 与 `恢复为未评估状态` 未译；
- `chemical` 7 页：摩尔质量、溶液浓度、滴定/重量法纯度、混配稀释、储罐容积、苗木验收与占位未译。

## 处理
只改源 `i18n/tools/en/<industry>/<slug>.json` 的 `map`，共 43 条。
物理说明统一复用同一句校验口径英文；`请选择…` → `Select…`；`恢复为未评估状态` → `Reset to unassessed`。

## 验证
- 四行业 `--check` 均 **残留 0**（26 / 21 / 23 / 14 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
