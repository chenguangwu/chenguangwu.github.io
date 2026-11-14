# 483 · quality / museum 英文态清零（10 页 55 条）

## 问题
- quality：Cp/Cpk/Pp/Ppk 公式、X̄ 控制图、DPMO 与西格玛水平换算、PPM 定义等 33 条。
- museum：展陈视角-距离模型 11 条、展陈照度计算 14 条、展柜温湿度判定说明 2 条。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 55 条。
`quality/calc-cpk` 的「评级：」被 `_prefix` 半译为 `Rating:`（无空格），按 zh 源文作键；
`museum/lighting-lux` 的「平均照度」被半译为 `Average illuminance`，同样按 zh 源文作键。
Φ、Φ⁻¹、σ、⌊⌋、√、Ω 等符号原样保留。

## 验证
- quality / museum 两行业 `--check` 全部 **残留 0**（10 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
