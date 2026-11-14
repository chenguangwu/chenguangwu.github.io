# 472 · forex / futures / glass / hotel 英文态清零（22 页 174 条）

## 问题
- 金融公式块：杠杆/爆仓、点值、点差成本、持有成本定价、对冲比率、保证金、Black-Scholes 希腊字母、期权损益。
- 玻璃工艺：退火曲线、切割排版、斯涅尔折射/全反射、热弯参数。
- 酒店换算：双向换汇、行程分配、入住率/RevPAR。
- placeholder 中文共 60+ 个。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json`，共 174 条；公式与符号（e^、N(d1)、σ、ρ、⌊⌋、⌈⌉）原样保留。
`_prefix` 半译形态（`Contract value =`、`Remaining capital =`、`Deviation =`、`Fee =`、`Rotate 90°`）按 zh 源文作键。

## 验证
- 4 个行业整行业 `--check` 全部 **残留 0**（22 页）。
- `python3 _build.py` 通过。
