# 473 · packaging / paper / parenting 英文态清零（24 页 77 条）

## 问题
- 包装：McKee 堆码抗压公式块、纸箱强度链（环压→边压→BCT）整段未译；placeholder「如 300」等 5 个。
- 造纸：克重换算、浆浓调配、水分/绝干率、纸浆得率、纸卷长度、瓦楞箱强度六页公式说明整段未译。
- 育儿：尿布用量、奶量估算、喂养时间表、生长百分位评估（含 WHO 参考句与百分位分级）未译。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 77 条；公式符号（⌊⌋、⌈⌉、√、π、≈、≥）原样保留。
`paper/strength-1` 的「周长 P = …」在 EN 态被 `_prefix` 半译为 `Perimeter P = …`，按 zh 源文作键。
placeholder 统一译为 `e.g. N` 形式。

## 验证
- packaging / paper / parenting 三行业 `--check` 全部 **残留 0**（24 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
