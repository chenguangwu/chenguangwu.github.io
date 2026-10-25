# 医疗 · 药物剂量类（health/medical/clinical-nursing 剂量页 ~40 页）

## 已知问题
### D1. 待裁断：dosage-calculator 阿莫西林按次剂量偏高（G01-A5）。
### D2. 已修：child-medication-dose 包/袋规格解析、gfr-calculator 种族系数、parkland 图（口径本身见 G01-A1）。

## 功能缺陷
- 儿童剂量页均无「年龄→体重默认填充」（WHO 中位体重表，静态可行）。
- 无「肝肾功能调整提示」（剂量页联动 eGFR 结果给出减量建议文案）。

## 优化点
- S8 空态教育化最适合本类：每个输入框 placeholder 给「典型值+范围」。
- 药品库数据集中 json 化（当前散在页内 JS），便于审校与后续扩充。

## 受影响范围
- tools/health/（child-medication-dose/weight-dosage 等 40 页）、tools/medical/dosage-calculator 系、tools/healthcare/（parkland/ibw 等）、tools/clinical-nursing/ 输液类（~40 页合计）

## 进度
- 🔴 待开发
