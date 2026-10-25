# 医疗 · 专科计算类（ent/dermatology/obstetrics/pediatrics/ophthalmology/urology 等 ~120 页）

## 已知问题
### S1. 已修：wisdom-tooth 方向分、easi 儿童权重、wells、GAGS 归 B1 待裁断、wheelchair 压强单位、M-CHAT。
### S2. 遗留小项：kupperman（G01-A8）、vanderbilt（G01-A8）。

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
