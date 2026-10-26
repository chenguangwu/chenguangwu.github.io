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
- 🟢 批次 03-67（2026-10-26 · 报告单批量解读模块）：`clinical-lab/blood-routine-reference` 加 textarea「报告单批量解读」（贴多行「指标名 值」）→ `__brBatch()` 文本解析：逐行抽首个数字 + 指标名 token 匹配（按命中 token 长度取最优，「血红蛋白」不误配「平均红细胞血红蛋白」）→ 逐项定位参考区间（偏低/偏高/正常 + 偏离%）+ 异常统计 + 未识别行回显；EN 态 __BR_NAME_EN/__BR_GROUP_EN 全英文（harness probe 验证零 CJK）。reportText 默认空 ⇒ 卡不渲染零交集；clicks 直调 __brBatch 强用例（WBC 3.2/HGB 105/PLT 450 → 三异常）。verify 77/77、判别器 7794/0、门禁 218/218。
- 🟢 批次 03-68（2026-10-26 · S3 标尺铺开第八批 · pcr-ct）：`clinical-lab/pcr-ct-interpretation`：
  #pcr_ctRefBar（Ct 值四带：阳性高拷贝<30/低拷贝 30–38/灰区 38–cutoff/阴性≥cutoff，带边界随判定阈值 cutoff 动态构建；cutoff≤30 病态值跳过标尺）；ref-card「样本Ct N → 落在 X带」文本定位。
  **顺带修存量 EN 泄漏**：interpretQual 全部动态串（判读结果/四态 status/质控 3 条/ΔCt 行/拷贝数行）补 `__T`，qualResult 容器 EN 态零 CJK（jsdom 实测，stash 复核确认泄漏为存量非本批引入）。
  verify +2 新用例（灰区 ct=39、阴性 ct=42）+ 既有 ct=32 用例补锚 → 79/79；判别器 7824/0；门禁 218/218。
- 🟢 批次 03-69（2026-10-26 · S3 标尺铺开第九批 · 生化比值多标尺）：`clinical-lab/biochemistry-ratio`：
  三标尺 #bio_ratioDeRitisBar（De Ritis 四带 0.7/1/2）、#bio_ratioBunCrBar（BUN/Cr 三带 10/20）、#bio_ratioRBar（R 因子 DILI 三带 2/5）；ref-card 三行文本定位。
  **顺带修存量 EN 泄漏**：calc() 全部动态串（结果标题/三段比值标签+描述/换算行/UA-ALB）补 `__T`（顺带修「GGG/ALT」笔误→GGT/ALT）；result 容器 EN 零 CJK。
  **新坑（__EN 时序）**：`var __EN` 赋值若放在首段 `var html` 之后，hoisting 只提升声明不提升赋值 → h3 走 zh 泄漏；必须把 __EN 定义移到函数最前。
  **判别器抓 1 逃生**：用例 bun=5.0/cr=80 恰等于页面默认值 → B 态 BUN/Cr 同值 15.5 → 锚改 bun=6.0/cr=70 → 21.2 升高带。
  verify +1 用例 → 80/80；判别器 0 逃生；门禁 218/218。
- 🟢 批次 03-70（2026-10-26 · S3 标尺铺开第十批 · 电泳五分段三标尺）：`clinical-lab/electrophoresis-analysis`：
  #ep_albBar/#ep_a2Bar/#ep_gBar 三标尺（偏低/正常/偏高，带界取 REF lo/hi 57–68/5–11/10–20，max 100%）+ ref-card 三行；a1/b 暂不铺（b 与 β-M峰特判耦合）。
  **顺带修存量 EN 泄漏**：analyze() 全部动态串（合计行/findings 13 条/正常行/白蛋白对比行）补 `__T`；默认态+注入异常态 EN 均零 CJK（jsdom 实测）。
  verify 既有用例补 3 锚（白蛋白50→偏低/α2 13→偏高/γ 23→偏高）→ 80/80；判别器 0 逃生；门禁待跑。
- 🟢 批次 03-71（2026-10-26 · S3 标尺铺开第十一批 · 甲状腺轴）：`clinical-lab/thyroid-function-model`：
  #thy_tshBar/#thy_ft3Bar/#thy_ft4Bar 三标尺（偏低/正常/偏高，带界取 REF 0.27–4.2/3.1–6.8/12–22，max 10/12/40）+ ref-card「TSH 0.02 mIU/L → 落在 偏低」式三行。
  锚纪律：tsh=2.0/ft3=5.0/ft4=16 是页面默认 → 同值用例只取非默认指标锚（低T3 用例仅 FT3 锚、亚临床甲减用 TSH+FT4 锚）。
  ref-card 走 __T（EN 零 CJK）；页面其余动态串（8 种 pattern/desc/mechanism/表格）存量中文未治理 → 记入待续（页面级 i18n 大工程单独批）。
  verify 80/80（4 用例补 6 锚）；判别器 0 逃生；门禁待跑。
- 🟢 批次 03-72（2026-10-26 · S3 标尺铺开第十二批 · 免疫比值 + S3/S8 收口）：`clinical-lab/flow-cytometry-ratio`：
  #flow_ratioBar（CD4/CD8 比值三带 0.71/2.78，max4）+ #flow_cd4Bar（CD4 绝对值四带 <200 重度抑制 AIDS/200–414 偏低/414–500 边缘/≥500 正常，max1600）双标尺 + ref-card 双行；cd8=0 无效态不渲染。
  **顺带修存量 EN 泄漏**：calc() 动态串（stat-grid 六卡片标签/flags 7 条/HIV 分期/正常行）补 `__T`；result 容器 EN 零 CJK。
  verify 80→82（既有倒置用例补 2 锚 + 升高带、边缘带 2 新用例）；判别器 0 逃生；门禁 218/218。
  **S3 标尺铺开就此收口**：clinical-lab 剩余 14 页均为 0 输入参考表/查表型（parasite-egg-id/urine-sediment-atlas/autoantibody/mic-breakpoint/analysis-8/9 等）或多时点曲线型（cardiac-marker-curve）、单行文本换算（convert-glucose-1），不适配单值带标尺。
  **S8 placeholder 收口**：最后一处缺 placeholder 输入框（medical/calculator-calc-2 的 age）已补「如 6（选填，0–18）」；placeholder-only 改动零 verify 影响（medical 17/17）。
- 🔴 待续：批量解读可向生化/免疫面板推广（需各页自有参考表）；
  thyroid-function-model 页面级 EN i18n（8 pattern 全串）单独批治理。
