# 491 · mechanical / manufacturing 英文态清零（17 页 50 条）

## 问题
- mechanical：轴承寿命、带传动、螺栓扭矩、切削速度、齿轮参数、转矩-功率等 12 页公式与 placeholder。
- manufacturing：班产能、DPMO 西格玛、库存、OEE、CPK 等 5 页公式与 placeholder。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 50 条。齿轮/轴承公式符号原样保留。

## 验证
- mechanical / manufacturing 两行业 `--check` 全部 **残留 0**（18 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
