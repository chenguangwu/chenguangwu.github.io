# 494 · nephrology / neurology 英文态清零（23 页 35 条）

## 问题
- nephrology：8 页共 16 处下拉框「请选择…」未译。
- neurology：11 页「恢复为未评估状态」、ncs-emg 9 处「未选择」、qmg/rater-21/twstrs 三页量表说明与算例。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 35 条：
`请选择…` → `Select…`，`恢复为未评估状态` → `Reset to unassessed`，`未选择` → `Not selected`。

## 验证
- nephrology / neurology 两行业 `--check` 全部 **残留 0**（48 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
