# 496 · ophthalmology 英文态清零（15 页 60 条）

## 问题
- 眼轴/角膜曲率/角膜内皮/屈光/视野等 10 页共 37 个中文 placeholder；
- 视力记录对照表（8 条等级标签）、SRK II / SRK/T 公式、眼压角膜厚度四式校正、OSDI 计分、
  21 题视力筛查评分、视力换算枢纽 logMAR 说明。

## 处理
只改源 `i18n/tools/en/ophthalmology/<slug>.json` 的 `map`，共 60 条。
`iop-correction` 与 `iol-power` 的长句被 `<code>`/`<strong>` 拆成多个文本节点，按运行时片段分别作键。

## 验证
- ophthalmology 行业 `--check` **残留 0**（31 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
