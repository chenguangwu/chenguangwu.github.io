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
### C2. forensic-medicine/bone-age-estimation 胎儿支路胎龄公式斜率严重失真（批20）
- 描述：`ageByFemur = 6.752 + 0.2127×FL(mm)`（默认 FL=50mm 真实胎龄约 26 周，公式给 17.4 周）；`ageByCRL = 0.017×CRL + 4.5`（默认 CRL=120mm 真实约 15.5 周，公式给 6.5 周，斜率小约 6 倍）。代码注释还写着第三个公式 `(CRL+6.5×1.037)/0.88`，三处互相矛盾；formula-box 把错误公式原样展示。
- 方案：FL 改产科线性近似 GA(w)≈0.43×FL+8.5（或分段查表）；CRL 改 Robinson 简化 GA(w)≈0.1×CRL+6.5（限 6–14 周内有效并注明）；formula-box / 深度解读同步（G03 数据源）。
- 受影响：tools/forensic-medicine/bone-age-estimation.html
- 置信度：高（默认值代入即可复现失真）
