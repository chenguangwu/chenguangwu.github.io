# 医疗 · 专科计算类（ent/dermatology/obstetrics/pediatrics/ophthalmology/urology 等 ~120 页）

## 已知问题
## 已知问题（批19 部分审读新增）
### C1. cosmetic-derm/concentration 游离酸比例公式颠倒
- 描述：`freeRatio = 10^(pH-pka)/(1+10^(pH-pKa))` 算出的是**解离型 A⁻ 占比**，页面却标注「游离酸比例」并以 `freeAcid = conc×freeRatio` 输出「游离酸浓度」——方向颠倒（pH 越高游离酸反而越大）。同站 chemical-peel.html 用 `1/(1+10^(pH-pKa))`（HA 占比）口径正确，两页互相矛盾。
- 方案：改为 `freeRatio = 1/(1+Math.pow(10, ph-pka))`，与 chemical-peel 对齐；深度解读同步（G03 数据源）。
- 受影响：tools/cosmetic-derm/concentration.html
- 置信度：高

## 功能缺陷
- 产科预产期页缺「孕周时间轴可视化」（周数条+当前周胎儿大小描述）。
- 眼科视力页缺 LogMAR/Snellen 分数互转表（部分有，未统一）。

## 优化点
- S2 场景：「孕 12 周建档日历」「宝宝 6 月龄辅食量」。
- 专科「随访计划」生成器：输入诊断日期→输出复查时间表（纯前端、高粘性）。

## 受影响范围
- tools/ent/、tools/dermatology/、tools/obstetrics/、tools/ophthalmology/、tools/urology/、tools/pulmonology/、tools/rheumatology/、tools/cosmetic-derm/、tools/forensic-medicine/（~120 页合计）

## 进度
- 🔴 待开发
