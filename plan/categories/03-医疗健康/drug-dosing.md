# 医疗 · 药物剂量类（health/medical/clinical-nursing 剂量页 ~40 页）

## 已知问题
## 功能缺陷
- 儿童剂量页均无「年龄→体重默认填充」（WHO 中位体重表，静态可行）。
- 无「肝肾功能调整提示」（剂量页联动 eGFR 结果给出减量建议文案）。

## 优化点
- S8 空态教育化最适合本类：每个输入框 placeholder 给「典型值+范围」。
- 药品库数据集中 json 化（当前散在页内 JS），便于审校与后续扩充。

## 受影响范围
- tools/health/（child-medication-dose/weight-dosage 等 40 页）、tools/medical/dosage-calculator 系、tools/healthcare/（parkland/ibw 等）、tools/clinical-nursing/ 输液类（~40 页合计）

## 进度
- 🟡 进行中（2026-10-26 批次 03-2）：两条功能缺陷已在 2 个代表页落地
  - `health/child-medication-dose`：新增「同年龄参考体重（WHO 生长标准 P50，0–18 岁男/女）」+ 输入值与中位体重偏差百分比；
    新增「肝肾功能减量提示」（两 select：肾功能 Ccr 四级 / 肝功能 Child-Pugh 四级），8 种药标注主要清除途径（肝/肾/局部肠道），
    药物参考表新增「主要清除途径」列。
  - `medical/dosage-calculator`：同样两套能力接入；儿童（≤18 岁）显示参考体重核对并**偏差 >40% 时红字提示核对单位（kg/斤）**；
    15 种药按清除途径给出肝/肾分级减量建议（阿莫西林/头孢氨苄/万古霉素→肾，对乙酰氨基酚/布洛芬/苯妥英钠等→肝，头孢曲松/环磷酰胺→肝+肾）。
  - 数据源：WHO weight-for-age P50（0–18 岁）；清除途径按各药说明书主要消除途径归类，提示文案统一附「以说明书与药师核定为准」。
- 🔴 待续：剩余剂量页（clinical-nursing 输液类 ~40 页、health/insulin-dose 等）按同一模板铺开；
  「药品库 json 化（散在页内 JS → 集中 json 便于审校）」未做。
