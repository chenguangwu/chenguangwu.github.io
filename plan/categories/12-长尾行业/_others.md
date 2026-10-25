# 长尾行业汇总（<20 页的 190+ 行业）

> 本文件只收录**已知具体问题**（来自 16 批审计备案）；长尾行业共性问题（留存/性能/EN）统一走 plan/G 系列，不在此重复。

## 已收录问题
### O1. dyeing/tester-9 输入 C 未参与计算（GB/T 20944.2 对照口径）
- 方案：`(C−B)/C` 与 `logC−logB` 分支接入；受影响：tools/dyeing/tester-9.html
## 受影响范围
- tools/ 其余 190+ 长尾行业目录

## 进度
- 🟡 按需增量（新问题随批次追加于此）

### O6. food-testing/heavy-metal-migration 食品中含量虚高 1000 倍（批19 实锤）
- 描述：输入标签实测——浓度 mg/L、浸泡液体积 mL、食品模拟液体积 mL（对应 1kg 食品）。量纲推演：conc(mg/L)×volume(mL)÷1000 = mg；除以 foodVol(mL)÷1000 = kg ⇒ **conc×volume÷foodVol 已直接是 mg/kg**，代码再 `×1000` 结果虚高 1000 倍。默认 Pb 0.05mg/L×100mL/1000mL 显示 5 mg/kg（正确 0.005），对照 SML 0.01 mg/kg 必然误判「超标不合格」。
- 方案：删除 `×1000`，`migrationKg=(conc*volume)/foodVol`；迁移量 mg/dm² 卡同样核对（其链为 conc×vol/1000÷area，conc mg/L×mL/1000=mg、mg/dm² ✓ 无误）；同步修 SML 对比与判级。
- 受影响：tools/food-testing/heavy-metal-migration.html
- 置信度：高

## 长尾行业通用优化指引
- 留存/分享/场景预设等共性优化统一执行 `plan/G06-留存与竞争力升级.md`（S1 首屏即答案、S2 场景预设、S4 分享卡按流量数据择优覆盖长尾）。
- 文案类改动一律先查数据源（`plan/G03`）。
