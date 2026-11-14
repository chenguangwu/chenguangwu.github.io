# 481 · hematology / nuclear / obstetrics / fishery 英文态清零（23 页 31 条）

## 问题
- hematology：5 个评分页的重置按钮文案「恢复为未评估状态」。
- nuclear：活度、衰变分数、当量剂量、质量亏损、核半径、Q 值六页代码口径说明与比活度问答。
- obstetrics：5 个下拉框「请选择…」、内膜厚度算例（含拆开的「着床窗」）。
- fishery：放养密度、休药期温度模型、饲料蛋脂比、清淤、承载密度五页算例。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 31 条。
核物理页保留科学计数法与常量数值不变；`请选择…` 统一译为 `Select…`。

## 验证
- 4 个行业 `--check` 全部 **残留 0**（23 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
