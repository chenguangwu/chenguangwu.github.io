# 475 · pr / printing / project / railway / rehabilitation / rental / road 英文态清零（23 页 90 条）

## 问题
- 公关：赞助 ROI、关键词密度、效果综合评分、风险矩阵评估整段未译。
- 印刷：亮度/照度均匀度统计、盒型展开面积、由容积反算尺寸。
- 项目：干系人象限判据、挣值分析（PV/EV/AC、CPI/SPI/EAC/ETC/VAC）。
- 康复：FIM 分级、量表构成、效能/效率解读。
- 租赁：中介费分摊、阶梯水电结算、市场比较法租金评估。
- 铁路/道路：5 页共 23 个中文 placeholder。

## 处理
只改源 `i18n/tools/en/<ind>/<slug>.json` 的 `map`，共 90 条。
`pr/analysis-density-1`（`英文单词数`→`English words`）、`rehabilitation/fim-scale`（`合计`→`Total`）、
`rental/cycle-11`（`用量`→`Dosage`）、`rental/rent-2`（`单价`→`Unit price`）均被 `_prefix` 半译，按 zh 源文作键。

## 验证
- 7 个行业 `--check` 全部 **残留 0**（23 页）。
- `python3 _build.py` 通过；`_test_static.py` **4685/4685**。
