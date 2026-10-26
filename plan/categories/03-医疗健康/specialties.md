# 医疗 · 专科计算类（ent/dermatology/obstetrics/pediatrics/ophthalmology/urology 等 ~120 页）

## 已知问题
## 功能缺陷
- 产科预产期页缺「孕周时间轴可视化」（周数条+当前周胎儿大小描述）。
- 眼科视力页缺 LogMAR/Snellen 分数互转表（部分有，未统一）。

## 优化点
- S2 场景：「孕 12 周建档日历」「宝宝 6 月龄辅食量」。
- 专科「随访计划」生成器：输入诊断日期→输出复查时间表（纯前端、高粘性）。

## 受影响范围
- tools/ent/、tools/dermatology/、tools/obstetrics/、tools/ophthalmology/、tools/urology/、tools/pulmonology/、tools/rheumatology/、tools/cosmetic-derm/、tools/forensic-medicine/（~120 页合计）

## 进度
- 🟢 批次 03-50（2026-10-26 · 产科预产期页时间轴可视化）：`obstetrics/due-date`：
  ① 孕周时间轴进度条（0–42 周，0/12/28/37/42 刻度，颜色随孕期分期）；② ref-card 增「胎儿发育估计（孕 N 周）：身长/体重 + 水果粗略类比」九段静态表（个体差异大以超声为准）+「孕程进度 X%」。
  harness 冻结 now=2024-06-15 ⇒ 日期/孕周内容门禁内确定；现有 EDD 强用例（cycle=30 → 2024-11-18）零改动仍判别。verify 46/46、判别器 0 逃生、门禁 218/218。
- 🟢 批次 03-51（2026-10-26 · 眼科对照表统一）：`ophthalmology/vision-screening-21` 补「视力记录对照表」静态卡（小数/5 分记录/LogMAR/Snellen 20ft 五列七行 + LogMAR=5−5分 换算关系），与 visual-acuity-converter 口径统一。静态区块不改 calc ⇒ verify 28/28、门禁 218/218。
- 🔴 待开发：专科「随访计划」生成器；S2 场景（孕 12 周建档日历等）。
