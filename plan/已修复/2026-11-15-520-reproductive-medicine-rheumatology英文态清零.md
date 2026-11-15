# 520 批：reproductive-medicine / rheumatology 英文态清零

- 日期：2026-11-15
- 范围：`reproductive-medicine` 25 页中 15 页、`rheumatology` 25 页中 16 页，合计 112 条键。
- 手段：只改 `i18n/tools/en/<industry>/*.json` 的 `map`；
  IVF/精液参数判读、自身抗体滴度分级、疾病活动度评分与分类标准整句英译。
- 备注：`rheumatology` 多页为「阈值分档 + 评分条目」列表，逐条按文本节点作键；
  `ANCA 分型`等被 `<strong>` 拆开的片段分别作键，英文值中括号保持闭合。
- 验收：两行业 `--check` 均残留 0；`_build.py` 通过；`_test_static.py` 4685/4685。
