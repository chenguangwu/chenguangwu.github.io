# 医疗 · 检验与诊断类（clinical-lab/cardiology 检验/血气等 ~80 页）

## 已知问题
## 功能缺陷
- 检验页缺「参考范围性别/年龄分列」（部分页有，未统一）。
- 血气页缺「酸碱失衡四步判读流程图」交互。

## 优化点
- S3 阈值标尺：所有检验值结果画正常区间条+落点（G06-S3 医疗首选）。
- 「报告单批量解读」：贴多行化验数据一次判读（文本解析纯前端可行，竞品稀缺）。

## 受影响范围
- tools/clinical-lab/（血气/生化/免疫 17 页）、tools/cardiology/ 检验类（心肌标志物等）、tools/nephrology/（eGFR/电解质）、tools/gastroenterology/（hp-dob/saag）、tools/medical/convert-glucose（~80 页合计）

## 进度
- 🟡 进行中（2026-10-26 批次 03-1 · S3 参考区间标尺）
  - 通用组件：新增 `TBKit.chart.refBar(host,{value,unit,min,max,bands,log,ticks})`（`js/tool-kit.js`，纯 SVG 自绘、支持对数刻度、英文态 label 自动切换）。
  - 已落地 6 页：nephrology/ckd-staging（eGFR G1–G5 带）、nephrology/creatinine-clearance（Ccr 五级带）、cardiology/nt-probnp（排除/灰区/纳入，对数刻度）、clinical-lab/coagulation-inr（目标区间随适应症联动）、clinical-lab/hba1c-converter（正常/前期/糖尿病 六级带）、clinical-lab/blood-gas-analysis（pH 三带）。
  - 形态纪律：SVG 标尺只做增强，**必须同时输出一段「参考区间定位」文本到 `#result`**（门禁可断言 + 无障碍），且文本走 `__T(en,zh)` 双语 helper。
- 🔴 待续：其余检验页（thyroid-function-model / urinalysis / csf / semen / electrolyte 等）按同一模板铺开；「报告单批量解读」模块待开发。
