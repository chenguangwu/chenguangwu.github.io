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
  - 已落地 8 页：nephrology/ca-p-product（钙磷乘积 达标/轻度/显著三段）、nephrology/microalbuminuria（正常/微量/大量，随 UACR·浓度·24h 三模式换阈值）+ 以下 6 页：nephrology/ckd-staging（eGFR G1–G5 带）、nephrology/creatinine-clearance（Ccr 五级带）、cardiology/nt-probnp（排除/灰区/纳入，对数刻度）、clinical-lab/coagulation-inr（目标区间随适应症联动）、clinical-lab/hba1c-converter（正常/前期/糖尿病 六级带）、clinical-lab/blood-gas-analysis（pH 三带）。
  - 形态纪律：SVG 标尺只做增强，**必须同时输出一段「参考区间定位」文本到 `#result`**（门禁可断言 + 无障碍），且文本走 `__T(en,zh)` 双语 helper。
- 🟢 收口（2026-10-26 批次 03-40 · S3 标尺跨分类铺开首批）：在「单主值 + 参考区间带」型页加 refBar + 守卫式调用（harness 不加载外链 tool-kit.js，靠 `typeof TBKit!=='undefined'` 守卫避免报错），三页：
  - `cardiology/coronary-calcium`：CACS 积分 → bands 无/轻/中/广/重（max1500）；verify 弱用例 `93岁`(输入回显) 先改 `中度钙化` 仍逃生（页面默认 cacs=280 同为中钙），终锚 `50–75百分位`（随 age=93 注入变化，默认 62 岁=≥75百分位，零交集）。
  - `nephrology/dialysis-ktv`：spKt/V → bands 不足/临界/达标/理想（max2.5）；verify 派生公式片段改 `透析充分（理想）`。
  - `gastroenterology/child-pugh`：评分 → bands A/B/C 级（max15）；原用例已强（评分明细+分级），保留。
  - 三分类 verify 全过（cardiology 23/23、nephrology 23/23、gastroenterology 22/22）；全量门禁待跑。
- 🟢 批次 03-41（2026-10-26 · S3 标尺铺开第二批 · 内分泌）：同模板再铺 2 页：
  - `endocrinology/homa-ir`：#homa_irRefBar（高敏感/正常/临界/IR/严重IR 五带，max8，临界带上界随人群切点 cutoff 联动）；文本定位含 IR 切点 + HOMA-β 状态（`__betaEn` 映射保 EN 零 CJK）。
  - `endocrinology/glycated-albumin`：#glycated_albuminRefBar（达标/尚可/偏高/显著升高，max30）；文本定位含 GA 带 + eAG 双单位换算。
  - 两页现有 verify 用例已强（2.93/120、20.5/33.3 派生值锚），零改动；EN 态经 harness 内联 probe（clicks 覆盖 TBKit + fire input）验证 ref-card 零 CJK。
- 🟢 批次 03-42（2026-10-26 · S3 标尺铺开第三批）：再铺 2 页：
  - `endocrinology/ogtt-interpretation`：#ogtt_fpgBar（正常/IFG/糖尿病，max15）+ #ogtt_h2Bar（正常/IGT/糖尿病，max20）双标尺；ref-card 文本定位含空腹与 2h 双锚。
  - `medical/convert-glucose`：#convert_glucoseRefBar（低血糖/正常/IFG/糖尿病/显著升高，max25，mg/dL 结果自动折算 mmol/L 当量）；文本定位注明「空腹口径，随机血糖标准不同」。
  - 两页现有 verify 用例已强，零改动；注入态与 EN 零 CJK 经 harness 内联 probe 验证通过。
- 🟢 批次 03-43（2026-10-26 · S3 标尺铺开第四批）：`clinical-lab/tumor-marker-doubling`：
  #tumor_doublingRefBar（DT 极快/较快/中等/缓慢四带，max360，末带 `hi:null` 开区间）；ref-card 只在上升分支（DT）渲染，下降分支（t½，阈值随标志物生理半衰期浮动）不适配固定带，暂不铺。注入态/EN 零 CJK probe 通过；clinical-lab verify 72/72。
- 🟢 批次 03-44（2026-10-26 · S3 标尺铺开第五批 · 多指标页首例）：`clinical-lab/urinalysis-interpretation`：
  #ua_sgBar（偏低/正常/偏高，max1.04）+ #ua_phBar（偏酸/正常/偏碱，max9）双标尺；ref-card 随 interpret() 渲染。
  **新坑**：该页 select 全部无 onchange（interpret 仅按钮/启动触发）⇒ inputs 注入不重渲染；且兜底循环会先跑 buildForm() 重置默认值 ⇒ inputs 注入被吞。解法：**clicks 在页面作用域直调 `interpret()`**（本页函数是顶层声明、非 IIFE，pageEval 可达），新增强用例 expect「尿比重 1.030 → 落在 偏高」「pH 8.0 → 落在 偏碱」。verify 73/73、判别器 7783 检/0 逃生。
- 🟢 批次 03-45（2026-10-26 · S3 标尺铺开第六批）：`clinical-lab/csf-analysis`：
  #csf_presBar（压力 偏低/正常/轻度升高/升高，max400）+ #csf_proBar（蛋白 偏低/正常/增高/显著增高，max5）双标尺；ref-card 四 li（压力/蛋白/糖+糖比值/氯化物）。糖比值、氯化物结核提示做进文本 li（无固定单带，不做 SVG）。EN 零 CJK probe 通过；verify 73/73。
- 🟢 批次 03-46（2026-10-26 · S3 标尺铺开第七批）：`clinical-lab/semen-analysis`：
  #semen_concBar（精子浓度 少精/参考内，max300）+ #semen_prBar（PR 弱精/参考内，max100）双标尺；ref-card 六 li（量/浓度/PR/形态/存活率/pH，WHO 5th 参考下限 + 达标/未达）。EN 零 CJK probe 通过；verify 73/73、门禁 218/218。
- 🔴 待续：其余检验/单值带型页按同一模板铺开（thyroid-function-model / electrolyte / blood-routine-reference 等多值/查表型页 refBar 适配性弱，需做「多指标多标尺」变体或逐页评估）；「报告单批量解读」模块待开发。
