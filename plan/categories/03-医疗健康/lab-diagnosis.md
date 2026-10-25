# 医疗 · 检验与诊断类（clinical-lab/cardiology 检验/血气等 ~80 页）

## 已知问题
### L1. 血气/电解质换算已全量核验通过（✅ 本仓 16 批审计）。
### L2. convert-glucose 系数方向已修（✅）；mic-breakpoint 判定图已注入（✅）。
### L3. 遗留：hp-dob 14C 阈值待裁断（G01-A7）。

## 功能缺陷
- 检验页缺「参考范围性别/年龄分列」（部分页有，未统一）。
- 血气页缺「酸碱失衡四步判读流程图」交互。

## 优化点
- S3 阈值标尺：所有检验值结果画正常区间条+落点（G06-S3 医疗首选）。
- 「报告单批量解读」：贴多行化验数据一次判读（文本解析纯前端可行，竞品稀缺）。

## 受影响范围
- tools/clinical-lab/（血气/生化/免疫 17 页）、tools/cardiology/ 检验类（心肌标志物等）、tools/nephrology/（eGFR/电解质）、tools/gastroenterology/（hp-dob/saag）、tools/medical/convert-glucose（~80 页合计）

## 进度
- 🔴 待开发
