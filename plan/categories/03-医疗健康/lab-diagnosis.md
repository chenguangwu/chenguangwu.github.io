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

## 2026-11-03 第一轮抽样补充

### 血常规报告单位、序号被误读（高，确认）
- `tools/clinical-lab/blood-routine-reference.html:307-342` 取每行首个数字，匹配项目后直接按项目默认单位判读：`HGB 13.5 g/dL` 被当作 13.5 g/L，`1 WBC 8.0` 的序号 1 被当检验值。原函数在内存桩中复现；浏览器未验证。
- 方案：对单位转换及数值位置做明确解析；未知单位或多数字歧义行提示用户确认，不能静默判读。页面 `:358-364` 切换人群只刷新参考表而不刷新批量结果，应同步重算或清除旧结果。保留原文、识别值、单位和人群供核对并可一键清除。

### 未识别行注入 HTML（高，确认源码路径；浏览器触发待验证）
- `tools/clinical-lab/blood-routine-reference.html:312-319,344-348` 将未识别原文拼入 `innerHTML`，原函数执行后 `<img src=x onerror=alert(1)>` 原样进入输出 HTML；该路径需要用户主动输入或粘贴，未证明远程投递链与真实浏览器执行。
- 方案：未识别原文使用文本节点或完整转义；补恶意标签与普通字符回归用例。

### 倍增时间零间隔和倒序判读（高，确认）
- `tools/clinical-lab/tumor-marker-doubling.html:280-300,320-362` 日期差取绝对值且不拒绝相同日期；同一天数值 10→20 算出 0 天并显示「倍增极快」，倒序日期也会产生正间隔；相等数值进入下降半衰期分支。无效或下降分支未清独立标尺。
- 方案：分别处理日期顺序、非零间隔及两次值相等；同步清理旧标尺，明确正数天数优先于日期的规则。医学阈值本轮未核验，不作临床结论。
- 覆盖：本轮仅抽查以上检验 2 页，未覆盖其他检验工具、真实浏览器和门禁。

## 2026-11-03 续查：血气、便潜血、MIC 折点与 INR

### L-N1 血气把单纯高碳酸或单纯低氧都判成呼吸衰竭（高，确认源码缺陷）
- 证据：`tools/clinical-lab/blood-gas-analysis.html:338-342` 的 `o2Status` 先判 `pao2<60` 即「I型呼吸衰竭」，再判 `paco2>=50` 即「II型呼吸衰竭」，未要求两者同时满足。PaO2 70、PaCO2 55 得「II型呼吸衰竭」；PaO2 55、PaCO2 60 得「I型」。
- 影响：`tools/clinical-lab/blood-gas-analysis.html`；氧合结论与实际血气不符，属临床判读错误。
- 方案：I 型要求 PaO2<60 且 PaCO2 正常/偏低，II 型要求 PaO2<60 且 PaCO2≥50；高碳酸但氧合正常时应单列「高碳酸血症」；补三组边界用例。

### L-N2 呼酸慢性代偿示例与程序结论相反（高，确认内部矛盾）
- 证据：`tools/clinical-lab/blood-gas-analysis.html:195` 示例为 pH 7.33、PaCO2 60、HCO3 34，声称「符合慢性代偿」；`:309-320` 慢性预期 HCO3=31，`|34-31|<3` 为严格判断不成立，随后 `else` 直接输出「HCO3 低于预期，合并代谢性酸中毒」。实际 HCO3 高于预期，且慢性代偿窗口被边界值排除。
- 影响：`tools/clinical-lab/blood-gas-analysis.html`；官方示例跑出相反结论，用户无法信任代偿判断。
- 方案：代偿带用闭合区间（≤±3），并在高于/低于预期两分支之前先判定落在急性/慢性窗口；示例与代码用同一组阈值做回归。

### L-N3 血气清空输入后保留旧判读（中，确认源码路径）
- 证据：`tools/clinical-lab/blood-gas-analysis.html:251-253` 当 pH/PaCO2/HCO3 任一为 0 或空时直接 `return`，未清空历史渲染的 `#result`。与 G10 同类，按页记录。
- 影响：`tools/clinical-lab/blood-gas-analysis.html`；用户会以为旧结论对应新样本，复制导出也可能带走旧判读。
- 方案：失败分支明确提示缺项并清空或置灰结果与复制按钮；保留最近一次成功判读时须标注输入摘要。

### L-N4 MIC 折点示例与本页 CLSI 数据不一致（高，确认源码缺陷）
- 证据：`tools/clinical-lab/mic-breakpoint.html:191` 大肠杆菌左氧氟沙星示例称 EUCAST 折点「≤1 敏感、≥2 耐药」；`:256` 实际数据为 `{s:0.5, r:4}`（页面标题称 CLSI M100）。按本页数据，MIC 1 判 I 而非 S，MIC 2 判 I 而非 R。`:131,161` 同时声称「CLSI/EUCAST」但只有一套数据。
- 影响：`tools/clinical-lab/mic-breakpoint.html`；示例与判读互相矛盾，用户拿示例核对会得到不同结论。
- 方案：只保留与本页数据同一标准（CLSI M100 版本年份）的示例；若要做标准对照，另建 EUCAST 数据表并在标题、CSV 中标注标准与版本，不得混用两套折点。

### L-N5 MIC 未校验取值合法性（中，确认源码缺陷）
- 证据：`tools/clinical-lab/mic-breakpoint.html:321,326-329,373-383` 仅 `parseFloat`，未校验正数与 2 倍稀释序列；输入 `-1` 或 `0` 均落到 `mic<=d.s` 被判「S 敏感」。
- 影响：`tools/clinical-lab/mic-breakpoint.html`；非法 MIC 得到「敏感」这一最危险的错误方向。
- 方案：要求 MIC>0，提示按实际稀释梯度（0.125/0.25/0.5…）录入；非法值不输出 S/I/R，并给出示例输入；导出 CSV 带标准与版本列。

### L-N6 便潜血免疫法年龄空值被静默当作 50 岁（中，确认源码缺陷）
- 证据：`tools/clinical-lab/stool-occult-blood.html:307,313,317` 的 `parseInt(age.value,10)||50` 使空值、非数字与 0 岁统一变成 50；阴性分支因此输出「年龄≥50 建议每年复查 FIT」，弱阳性分支触发「≥45 直接预约肠镜」。
- 影响：`tools/clinical-lab/stool-occult-blood.html`；年龄未知者被套用老年筛查建议，建议与真实人群不符。
- 方案：年龄为空时显示通用建议并提示补充年龄，不要用默认值代替；校验 0–120 整数，结果区标注所用年龄段。

### L-N7 化学法阳性叠加红肉干扰后无结论块（中，确认源码路径）
- 证据：`tools/clinical-lab/stool-occult-blood.html:344-357` 红肉阳性时 `realPos=false`，而唯一的结论分支是 `else if(!interfer.length)`，因此只渲染红色「阳性」大字与干扰提示，没有「不可判读/需复查」结论框。
- 影响：`tools/clinical-lab/stool-occult-blood.html`；用户只看到阳性结论却读不到处理建议，易自行判断为出血。
- 方案：增加「受干扰不可判读」结论分支（禁食 3 天复查或改 FIT），并不再把大号「阳性」作为主结论展示。

### L-N8 INR 低于 0.8 时 PT 比值被替换成「延长」（中，确认源码缺陷）
- 证据：`tools/clinical-lab/coagulation-inr.html:291` `inr<0.8?'延长':(pt/ptN).toFixed(2)`；INR 低于参考意味着 PT 缩短，页面却写「延长」且隐藏真实比值（如 0.7）。
- 影响：`tools/clinical-lab/coagulation-inr.html`；与临床含义相反，用户无法核对 PT 比值。
- 方案：始终显示数值比值，方向说明改为「缩短/正常/延长」三态；补低 INR 用例。

### L-N9 INR 页 PTA 公式未标注口径（中，疑似待验证）
- 证据：`tools/clinical-lab/coagulation-inr.html:280` `pta=ptN/(ptN+0.6*(pt-ptN))*100` 为线性近似式，页面无公式来源；临床常见的另一种 PTA 口径（由 PT 比值/ISI 反推）在同一 PT 下结果明显不同（如 PT 24 s、对照 12 s、ISI 1 时两种口径约 62.5% 与 50%）。
- 影响：`tools/clinical-lab/coagulation-inr.html`；不同实验室口径混用会导致活动度读数误读。
- 方案：先确认目标人群采用的口径并在页面标明公式与来源，或并列输出两种口径并注明差异；本条需医学专业确认后再定，不做单方判定。

### 留存与可核对优化（按页落点，非确认缺陷）
- `tools/clinical-lab/blood-gas-analysis.html`：缺少「四步判读流程」分步展示（原氧合/原发/代偿/AG 或混合），用户看不到推导顺序就难以核对；建议把现有分支结果改成可展开的 4 步卡片，并支持粘贴血气单文本自动填三项。
- `tools/clinical-lab/mic-breakpoint.html`：只能单菌种单 MIC 逐次查，建议支持粘贴「药名 MIC」多行做批量判读并导出，是检验科最直接的复用场景。
- `tools/clinical-lab/coagulation-inr.html`：剂量调整只给文字建议，无历史曲线；建议保存多次 INR 形成趋势与用药调整记录，便于复诊对比。
- `tools/clinical-lab/stool-occult-blood.html`：无复查日期记录；建议生成「3 天后复查」提醒卡片与本次结果摘要复制。

### 续查覆盖
- 新抽查 `tools/clinical-lab/blood-gas-analysis.html`、`tools/clinical-lab/stool-occult-blood.html`、`tools/clinical-lab/mic-breakpoint.html`、`tools/clinical-lab/coagulation-inr.html` 共 4 页，新增 9 条（3 条高优），另 4 条按页留存建议；均为源码与数值推导，未做浏览器、线上或门禁验证，医学阈值未做独立文献核验。

## 2026-11-03 续查：尿常规判读

### L-N10 尿比重/酸碱度留空时被判为「正常」（高，确认源码缺陷）
- 证据：`tools/clinical-lab/urinalysis-interpretation.html:259-262` 中 `parseFloat('')` 得 NaN，`n<1.003` 与 `n>1.025` 均为假，函数落到 `return {t:'正常'}`；`interpret()`（`:269-273`）随即把「正常」写入对应指标栏。清空比重或 pH 后仍显示绿色正常。
- 影响：`tools/clinical-lab/urinalysis-interpretation.html`；未测项目被当成正常结果，属误导性判读。
- 方案：区分「未填写/未检测」与数值正常，空值显示「未填写」且不参与综合结论；提交时提示缺项，或用显式「未检测」选项。

### L-N11 比重与 pH 参考区间偏窄且未标注来源（中，疑似待验证）
- 证据：`tools/clinical-lab/urinalysis-interpretation.html:261-262,302-307,320-325` 尿比重正常区间取 1.003–1.025、pH 取 5.5–7.5；同一阈值在 `classify`、`notes`、标尺三处重复硬编码。常见检验报告比重上限多为 1.030、尿液 pH 参考范围常见 4.6–8.0（不同实验室与标本状态有差异），按本页口径 1.028 被判「偏高」、pH 7.6 被判「偏碱」。
- 影响：`tools/clinical-lab/urinalysis-interpretation.html`；与用户手上的检验单对不上，降低可信度。
- 方案：由医学专业确认目标人群与标本口径后统一阈值并注明来源/实验室区间；把阈值抽成单处常量，`classify`、提示与标尺共用，避免三处漂移。

### 留存优化（按页落点，非确认缺陷）
- `tools/clinical-lab/urinalysis-interpretation.html`：结果只有逐项提示，不能一键复制成「报告式摘要」交给医生。建议按「项目—结果—参考—判读」四列生成可复制的报告块与 CSV，并保留检验单原始排序。
- 同页：无示例数据入口，新用户面对十余个下拉框不知如何试。建议加「典型尿路感染」「糖尿病酮症」等示例一键填充，并在结果顶部标注「示例」避免误当自测。
- 同页：异常提示全用醒目红色，轻度的尿胆原增多与血尿同色。建议按临床优先级分级（危急/需复查/轻度），避免所有异常同权。

### 续查覆盖
- 新抽查 `tools/clinical-lab/urinalysis-interpretation.html` 1 页，新增 2 条（1 条高优、1 条待验证）与 3 条留存建议；未做浏览器、线上或门禁验证，阈值口径需专业复核。

## 2026-11-03 修复收口（L-N1 / L-N2 / L-N4）
- **L-N1 已修**：`blood-gas-analysis.html` 氧合判型改为「II 型 = PaO2<60 且 PaCO2≥50；I 型 = PaO2<60 且 PaCO2<50；PaCO2≥50 而 PaO2≥60 仅判高碳酸血症」，并在公式区补呼衰判据。新增 3 条 verify（II 型 / I 型 / 单纯高碳酸）。
- **L-N2 已修**：慢性代偿改为闭合区间 ±3 且先判上下越界，HCO3 34（慢性预期 31.0）现在判「慢性呼酸代偿」，不再误报合并代酸；深解示例补预期值与区间说明。新增 3 条 verify（边界 34 / 上越界 36 / 下越界 24），并同步更新既有 2 条代偿断言。
- **L-N4 已修**：`mic-breakpoint.html` 示例改为本页 CLSI M100 口径（S≤0.5、R≥4，MIC 8 判 R），`CLSI/EUCAST` 混用文案与 FAQ/JSON-LD 统一为 CLSI M100（2023）。
- 中文/英文 i18n 字典同步更新；`_build.py` 通过（SW 戳 `6898340262`），`run_gates.py` 218/218，`verify_clinical-lab_calc.js` 88/88。
- 提交：`15892e31c7`；L-N3（缺项清空）与 L-N5（MIC 合法性校验）仍待处理。

## 2026-11-03 续查（并行批 F）

### L-N12 白带清洁度 Ⅰ 度分支不可达，完全正常报告被判Ⅱ度（高，确认源码缺陷）
- 问题：分级先用「Ⅱ度」条件拦下，Ⅰ度条件是其真子集且排在后面，导致 Ⅰ度永远不会输出；默认的「杆菌 ++++、球菌 −、上皮 ++++、WBC 0-5」这一最正常组合被判为Ⅱ度。
- 证据：`tools/clinical-lab/vaginal-discharge-grading.html:275-281`，Ⅱ度判定 `:279` 为 `bac>=2 && coc<=0 && epi>=2 && wbc<=1`，Ⅰ度 `:281` 为 `bac>=4 && coc===0 && epi>=4 && wbc===0`，前者先命中；四个下拉默认首选项为 4/0/4/0（`:139-171`）。node 内存复算 `grade(4,0,4,0)` → `2`，而页面表格 `:184` 与公式 `:131` 都把该组合定为 Ⅰ度。
- 影响：`tools/clinical-lab/vaginal-discharge-grading.html`；完全正常的镜检报告只能得到「Ⅱ度(正常)」，Ⅰ度结果无法复现，用户无法与检验单分级核对。
- 方案：把 Ⅰ 度判定移到 Ⅱ 度之前，或改为按 `:184-187` 表格四行阈值逐项匹配的单一表驱动函数；补 Ⅰ/Ⅱ/Ⅲ/Ⅳ 四条边界用例（`4/0/4/0`、`2/0/2/1`、`0/2/1/2`、`0/4/0/3`）。

### L-N13 脑脊液完全正常的默认值被判「病毒性脑膜炎 100%」（高，确认）
- 问题：评分只累计化脓/结核/病毒三类，没有「正常/无异常」类别；清亮外观与「糖正常」两条规则都只给病毒加分，于是正常脑脊液必然落到病毒项并获得 100% 匹配度。
- 证据：`tools/clinical-lab/csf-analysis.html:280-306` 评分结构，`:282` 清亮→viral+2、`:301` 糖比值正常→viral+2；默认输入 appearance=clear、pressure=150、wbc=10、poly=50、protein=0.4、glu=3.0、bg=5.5、cl=120（`:138-161`），`:377` 页面加载即调用 `analyze()`。node 内存复算 scores={bacterial:0,tb:0,viral:4}、total=4，`:311` pct=100 → `:315-316` 输出「最可能：病毒性脑膜炎／匹配度 100%」。
- 影响：`tools/clinical-lab/csf-analysis.html`；一份各项均在参考范围内的脑脊液被直接判成病毒性脑膜炎，属误导性结论，且用户打开页面即见该结论。
- 方案：增加「无异常／正常」类别与「异常项 ≥2 或总分过阈」才出倾向的门槛；正常项只做参考说明，不参与分母；补一条全正常用例断言结果不含「病毒性脑膜炎」。

### L-N14 HbA1c→血糖换算空值/负值输出负血糖并判「正常糖耐量」（高，确认）
- 问题：HbA1c 取值用 `+value||0`，空值与 0 都变成 0 代入 ADAG 公式，得到负的平均血糖；判读只按 `mg<140` 落入「正常糖耐量」分支，负值反被判成正常。
- 证据：`tools/clinical-lab/convert-glucose-1.html:203-204`，`const a1c=+document.getElementById("a1c").value||0; const mg=28.7*a1c-46.7`。node 内存复算：空值 → a1c=0、mg=-46.7 mg/dL、-2.59 mmol/L，判读「eAG 低于 140 mg/dL，一般属正常糖耐量范围」；输入 `-1` → -75.4 mg/dL、-4.19 mmol/L 仍判正常。
- 影响：`tools/clinical-lab/convert-glucose-1.html`；清空输入框或误填负值会显示负血糖并标注正常，结果区可直接被复制导出。
- 方案：先判空值/NaN/非正数（建议 HbA1c 3–20%），失败时提示「请输入有效 HbA1c」并清空结果，不把 0 代入公式；整数与一位小数边界补回归用例。

### L-N15 心肌标志物页参考上限不随标志物切换，负上限输出负倍数（高，确认）
- 问题：切换标志物类型只重算，不调整 99th 参考上限；默认上限固定为 cTnI 的 0.04，切到 CK-MB/MYO 后同一数值被按 cTnI 口径放大。上限输入也未校验正值，负值会让「峰值/上限」变成负数且判读分支恒真。
- 证据：`tools/clinical-lab/cardiac-marker-curve.html:140-145` 的 `onchange="analyze()"` 只重算，`:147` 的 upper 默认 `0.04` 不联动；`:289` `parseFloat(value)||0.04` 不拒绝负值。node 内存复算：示例序列 0.02/0.5/3.2/8.5/5.1（`:241-247`、`:280-285`）切为 CK-MB 后 peak/upper = 3.2/0.04 = 80×，`:356` 输出「典型急性心肌梗死(AMI)…峰值达参考上限 80 倍」；upper=-0.04 时 `:302` 显示 `-80.0×`、`:357` 恒走「轻度升高」分支。
- 影响：`tools/clinical-lab/cardiac-marker-curve.html`；非 cTnI 标志物被系统性误判为 AMI，负上限使所有输入都得到异常结论。
- 方案：为每种标志物配置默认上限与单位（cTnI/cTnT ng/L、CK-MB ng/mL、MYO ng/mL），切换类型时同步示例值与上限；校验 upper>0，非法值不输出判读并提示单位。

### L-N16 自身抗体 SLE「标志抗体」恒列四项，含实际阴性项（高，确认）
- 问题：SLE 关联的 `abs` 字段用恒真 filter，无论实际阳性项是哪几个，都输出「抗Sm/抗dsDNA/抗Rib-P/抗PCNA」四项，等于把阴性抗体写成标志抗体。
- 证据：`tools/clinical-lab/autoantibody-interpretation.html:348`，`abs:['抗Sm','抗dsDNA','抗Rib-P','抗PCNA'].filter(function(a,s){return true;}).join('/')` 条件恒真。最小触发：ANA 均质型（`:347` +1）、抗组蛋白阳性（`:346` +1）、抗Rib-P 阳性（`:344` +1）合计 3 分，`dsdna`/`sm` 均为阴性 → 输出「系统性红斑狼疮(SLE)…标志抗体：抗Sm/抗dsDNA/抗Rib-P/抗PCNA」。
- 影响：`tools/clinical-lab/autoantibody-interpretation.html`；结论区把未检出的高度特异抗体列为依据，用户与检验单逐条核对时会产生矛盾。
- 方案：按实际阳性项动态拼接 (`dsdna==='pos'` 才加抗dsDNA、`smPos` 才加抗Sm、`rib`/`pcna` 同理)，无特异抗体时改为「未检出 SLE 高度特异抗体，请结合临床与 dsDNA」。

### L-N17 HbA1c 换算器 0%/负值判「正常」（中，确认）
- 问题：仅拦截 NaN，0 与负数照常参与换算与分级；反向输入低血糖值也会得到偏低 HbA1c 并标「正常」。
- 证据：`tools/clinical-lab/hba1c-converter.html:274-287` 只判 `isNaN(v)`，`:290-295` 分级按 `<5.7` 判正常。node 内存复算：HbA1c 0% → eAG -2.6 mmol/L、等级「正常」；-1% → -4.2 mmol/L 仍「正常」；反算输入 2 mmol/L → HbA1c 2.9% 判「正常」。
- 影响：`tools/clinical-lab/hba1c-converter.html`；负平均血糖被标为血糖控制良好，与 L-N14 同一类缺项/非法值问题。
- 方案：校验 HbA1c 与血糖均为正（HbA1c 建议 3–20%，血糖建议 1–35 mmol/L），非法时提示缺项并清空结果区。

### L-N18 蛋白电泳缺项补 0，β/α1 降低无判读可出「各区带均在参考范围内」（中，确认）
- 问题：数值读取空值即 0，导致缺项被当作「该区带显著降低」；同时 β 区带完全没有任何判读（`REF.b` 定义后从未使用），α1 只判升高不判降低，可把超上限的 β 与偏低 α1 报成全部正常。
- 证据：`tools/clinical-lab/electrophoresis-analysis.html:252` `num()` 空值→0，`:293` `vals.alb<REF.alb.lo` 无缺项判断（清空白蛋白即输出「白蛋白降低 0%（0.0 g/L）」）；`:250` 定义 `REF.b`，全页仅 `:297,320` 用到 `REF.a1`，无 β 分支；`:281-283` 标尺只铺白蛋白/α2/γ。node 内存复算：alb 60、a1 4、a2 8、β 18、γ 10（合计 100）→ findings 为空，`:329` 输出「各区带均在参考范围内」，而 β 18% 已高于参考上限 13%。
- 影响：`tools/clinical-lab/electrophoresis-analysis.html`；缺项与 β 异常都得不到任何提示，结论与页面自带参考表 `:165-169` 相悖。
- 方案：区分未填与 0（空值不参与判读并列缺失项）；补齐 α1/β 双向下限阈值与 findings，β 用 `vals.b>REF.b.hi`、`vals.b<REF.b.lo` 判读，并给 β/α1 加标尺或文字定位。

### L-N19 心肌标志物迟达峰的高值被判「曲线变化不显著」（中，确认）
- 问题：曲线判读把「峰值 ≥5× 上限」与「达峰 ≤24h」绑在同一个分支；达峰晚于 24h 的高值既不满足 AMI 分支，也不满足 NSTEMI 分支（后者上限为 5×），最终落到「曲线变化不显著」。
- 证据：`tools/clinical-lab/cardiac-marker-curve.html:352-363` 分支顺序，`:355` 要求 `hasPeak && peak.t<=24`，`:357` 要求 `peak.v<=upper*5`，`:359` 其余靠 `riseEarly`。node 内存复算：30h 1.0、48h 0.5、72h 0.3，upper 0.04 → peak=25×、hasPeak=true、peak.t=30>24、riseEarly=false → 走 `:361-362` else，输出「曲线变化不显著／整体在参考范围内，不支持急性心肌梗死」。
- 影响：`tools/clinical-lab/cardiac-marker-curve.html`；峰值 25 倍上限的序列被判成无显著变化，判读方向完全相反。
- 方案：先按峰值倍数分档（≥5× 高、>1–5× 轻中度），达峰时间只作为补充描述不再决定主结论；补迟达峰高值用例，`riseEarly` 分支改为独立的「早期上升」提示而非兜底条件。

### L-N20 脑脊液空值按 0 计分、缺项静默保留旧结果（中，确认）
- 问题：所有参数读取空值即 0，缺项被当成极端病理值参与评分；只有 WBC 与蛋白同时为空才 early return，且 return 前不清空结果区。
- 证据：`tools/clinical-lab/csf-analysis.html:270` `num()` 空值→0，`:275` `if(!wbc && !protein) return;`。清空血糖 → `:297` `bg>0?glu/bg:1` 兜底比值 1 → `:301` viral+2、`:336` 输出「糖正常…倾向病毒性」；清空氯化物 → `:303` `cl<110` 给结核 +2；清空多核比例 → `:292` 判「淋巴为主」。
- 影响：`tools/clinical-lab/csf-analysis.html`；缺测项目被读成病理性结论，且早退时旧判读仍留在 `#result`，用户会以为对应新样本。
- 方案：缺项标记为「未填写/未检测」并不参与该类评分，结果区列出缺失项；早退分支清空或置灰结果并禁用复制导出。

### L-N21 脑脊液糖比值 0.4 / 0.4 / 0.55 三套口径并存（中，确认内部矛盾）
- 问题：评分用 `<0.4` 判结核、提示语用 `>0.4` 即「糖正常倾向病毒」、参考卡又写「糖比值 ≥0.55」，同一比值在三条路径得到三种解释。
- 证据：`tools/clinical-lab/csf-analysis.html:300` 评分 `gluRatio<0.4` 才给结核 +1，`:336` `else if(gluRatio>0.4)` 输出「糖正常…倾向病毒性」，`:363` 参考卡 `糖比值 ≥0.55`。node 内存复算：glu 2.6、bg 6.0（比值 0.43）→ 评分走病毒 +2、提示写「糖正常」，参考卡同期标注 0.43 低于 0.55。
- 影响：`tools/clinical-lab/csf-analysis.html`；患者拿着 0.43 的比值会同时看到「正常」与「低于 0.55」两种说法。
- 方案：抽成单常量（按实验室口径取 0.55 或 0.5），评分、findings、参考卡共用；0.4–0.55 灰区单独写「比值轻降，需结合糖绝对值」。

### L-N22 INR 换算页深度解析与简介是「39 类检验单位换算 + 胆固醇」模板（中，确认文案错配）
- 问题：页面功能只做 PT/对照/ISI → INR，但场景、示例、FAQ、简介全部来自通用「检验单位换算」模板，示例讲胆固醇 mg/dL→mmol/L，与凝血无关。
- 证据：`tools/clinical-lab/convert-39.html:195-208`（深解），`:198-200` 场景「外文文献数值（mg/dL）换算为本地产报告（mmol/L）」「不同仪器单位（IU/L↔ng/mL）」，`:202` 示例「总胆固醇 200 mg/dL ÷ 38.67 ≈ 5.17 mmol/L」，`:205-207` FAQ 讲「每种物质分子量」；`:248` 简介「约 39 类检验单位换算工具」。而输入与公式见 `:120-126`（PT / 正常对照 PT / ISI）。
- 影响：`tools/clinical-lab/convert-39.html`；正文与工具功能无关，用户按正文找不到换算入口，且与 `coagulation-inr.html` 功能重复，形成同质化内容。
- 方案：把 deep-dive/FAQ/intro 改写为 INR 内容（ISI 含义、INR 与 PT 比值关系、抗凝目标区间、Vitamin K 拮抗剂监测），删除胆固醇/分子量模板；保留纯换算定位并在页面注明与 coagulation-inr 的差异，或合并入口。

### L-N23 自身抗体 PM-Scl / Ma-2 阳性无任何关联和提示（中，确认）
- 问题：ENA 表定义了抗 PM-Scl 与抗 Ma-2，但 `interpret()` 没有任何规则引用，勾选阳性只回显「(+) — 说明」，疾病关联区不出现，ANA 阳性时还会额外提示「未发现疾病特异性抗体组合」。
- 证据：`tools/clinical-lab/autoantibody-interpretation.html:282-283` 定义两项，`:338-368` 全部疾病规则只涉及 sm/rnp/ssa/ssb/scl70/jo1/rib/pcna/histone/centromere；`:381-385` 仅回显阳性条目，`:377-378` 无 dx 且 ANA 阳性时输出「ANA阳性但未发现疾病特异性抗体组合」。
- 影响：`tools/clinical-lab/autoantibody-interpretation.html`；两种明确有临床指向的抗体（SSc-肌炎重叠、副肿瘤神经综合征）被判为「无特异性组合」，与条目自身说明 `:282-283` 矛盾。
- 方案：补 SSc-肌炎重叠综合征（抗 PM-Scl）与副肿瘤神经综合征（抗 Ma-2）关联规则；若暂不判读，则在条目上直接标注「本页仅列条目，不参与关联判读」。

### L-N24 HbA1c 页宣称 NGSP↔IFCC 换算但无该功能（低，确认文案）
- 问题：简介与深解示例都讲 NGSP% 与 IFCC mmol/mol 互换，但页面输入只有 HbA1c(%) 与平均血糖(mmol/L)，没有 mmol/mol 字段或模式。
- 证据：`tools/clinical-lab/hba1c-converter.html:413` 简介「HbA1c NGSP%↔IFCC mmol/mol 换算工具」，`:204-208` 示例「NGSP 7.0% → IFCC (7.0−2.15)×10.93 ≈ 53 mmol/mol」，输入区 `:143-150` 与切换 `:136-139` 只有两种模式。
- 影响：`tools/clinical-lab/hba1c-converter.html`；用户按正文示例找不到 mmol/mol 换算入口，正文承诺的功能实际缺失。
- 方案：增加 NGSP↔IFCC 第三模式（`IFCC = (NGSP−2.15)×10.93` 及反算），或删掉该宣称并同步深解示例。

### L-N25 HbA1c↔血糖换算页简介宣称 mg/dL↔mmol/L 双向换算，实际无该入口（低，确认）
- 问题：简介与 FAQ 讲 mg/dL 与 mmol/L 互换（如 126 mg/dL ÷ 18），但页面只接受 HbA1c 一个输入，血糖换算仅作为 eAG 的附属显示，不能由血糖反推、也不接受 mg/dL 输入。
- 证据：`tools/clinical-lab/convert-glucose-1.html:250` 简介「血糖 mg/dL↔mmol/L 换算工具…纯换算」，`:156` 深解示例「126 mg/dL ÷ 18 = 7.0 mmol/L」，而输入区 `:124` 只有一个 `a1c` 输入框，计算 `:203` 只把 HbA1c 换算为 eAG。
- 影响：`tools/clinical-lab/convert-glucose-1.html`；与同目录 `hba1c-converter.html` 功能近乎重复，正文承诺的双向换算无法执行，用户可能误以为可以输入 mg/dL。
- 方案：补齐 mg/dL↔mmol/L 双输入（或明确合并到 hba1c-converter），把简介改为「HbA1c→平均血糖」；如保留纯换算定位，需在正文标注「本页不做血糖单位互换」。

### L-N26 白带清洁度 BV 提示条件与「白细胞少」的典型特征相悖（低，待验证）
- 问题：只要球菌 ≥++ 且白细胞 ≥5-15 就提示「可能为细菌性阴道病(BV)」，而 BV 的典型镜下特征是白细胞不多；该条件更容易落在需鉴别的炎症场景。
- 证据：`tools/clinical-lab/vaginal-discharge-grading.html:305` `if(coc>=2 && wbc>=2) clues.push('可能为细菌性阴道病(BV)，建议做胺试验和线索细胞检查')`；同页 `:190-192` 判读原则与 `:191` 提 BV 需 pH/胺试验/线索细胞。该提示的临床阈值需专业确认。
- 影响：`tools/clinical-lab/vaginal-discharge-grading.html`；可能把非 BV 的炎症（滴虫/需氧菌）引导到 BV 检查路径。
- 方案：由妇科/检验口径确认后再改判据；建议提示改为「球菌增多伴白细胞增多：需鉴别 BV/滴虫/需氧菌性阴道炎，结合 pH、胺试验、线索细胞与湿片」，并单列 BV 典型特征（白细胞少、线索细胞阳性）。

### 留存优化
- `tools/clinical-lab/convert-glucose-1.html`：结果只有一段长文本，建议按「HbA1c—eAG(mg/dL)—eAG(mmol/L)—判读—建议」拆成表格，并加控制目标对照（7.0% ≈ 154 mg/dL）与一键复制报告块。
- `tools/clinical-lab/convert-39.html`：缺少与 `coagulation-inr.html` 的差异说明与病史入口（是否服抗凝药）；建议加「是否在用华法林／目标区间（2.0–3.0 或 2.5–3.5）」选项，避免所有人被套同一治疗区间。
- `tools/clinical-lab/hba1c-converter.html`：复查提醒只在填日期时出现，建议补「本次 HbA1c 与上次对比」与趋势记录；日期推算用 `setMonth` 存在 1/31 + 3 月滚动到 5/1 的边界，可改为按日历月末修正。
- `tools/clinical-lab/cardiac-marker-curve.html`：时间点可重复、可负值，`dt=0` 时速率显示 0 且无提示；建议去重/校验时间单调递增，并允许粘贴「时间 值」多行批量录入。
- `tools/clinical-lab/autoantibody-interpretation.html`：`updateRow` 只改颜色不重算，用户改选项后须再点「解释结果」；建议改为变更即重算，并在结果区标注所用的 ANA 滴度/核型。
- `tools/clinical-lab/csf-analysis.html`：压力/蛋白已有标尺，糖与氯化物仍只有文字；建议补糖、氯化物标尺与「缺失项清单」，并把三类得分以可展开的计分明细展示，便于核对。
- `tools/clinical-lab/electrophoresis-analysis.html`：`formula-box` 内 `formula-title` 被放在 `formula-eq` 之后（`electrophoresis-analysis.html:134`），标题与内容顺序颠倒；建议调整顺序并补「总蛋白未填时不显示 0.0 g/L」的占位提示。
- `tools/clinical-lab/vaginal-discharge-grading.html`：结果只有等级与一段说明，建议并列显示「本次镜检四项取值—对应表格行—等级」以便核对，并允许保存多次结果比较。

### 续查覆盖
- 新抽查 8 页：`tools/clinical-lab/convert-glucose-1.html`、`tools/clinical-lab/convert-39.html`、`tools/clinical-lab/hba1c-converter.html`、`tools/clinical-lab/cardiac-marker-curve.html`、`tools/clinical-lab/autoantibody-interpretation.html`、`tools/clinical-lab/csf-analysis.html`、`tools/clinical-lab/electrophoresis-analysis.html`、`tools/clinical-lab/vaginal-discharge-grading.html`。
- 新增 15 条（L-N12–L-N26），其中高优 5 条（L-N12–L-N16）、中优 7 条、低优 3 条（含 1 条待验证）；另 8 条按页留存建议。证据均为源码行号 + node 内存复算；未做浏览器、英文态、移动端、线上或门禁验证，医学阈值未做独立文献核验。

## 追加审计：流式 CD4/CD8、寄生虫虫卵（2026-11-04）

### L-N27 流式页清空 CD8 即输出「比值 0.00 / 降低(倒置)」，且无参考区间卡（高，确认缺陷）
- 问题：CD8 留空被 `num()` 转成 0，`ratio` 仍照公式算出 0；随后无条件按 `<0.71` 判「比值降低」并把「CD4/CD8倒置」加入异常提示。参考区间卡与标尺又只在 `cd8>0` 时渲染，页面出现「0.00 + 倒置」却没有任何区间说明，用户无法判断这是缺失值还是真实倒置。
- 证据：`tools/clinical-lab/flow-cytometry-ratio.html:256`（`num()` 把 NaN 归 0）、`:260`（读取 cd8）、`:267`（`ratio = cd8>0 ? cd4/cd8 : 0`）、`:280`（`ratio<0.71` 判降低）、`:284`（显示 `ratio.toFixed(2)` + 状态）、`:290`（参考区间卡 `if(cd8>0)`）、`:320`（倒置提示）。
- 复现：CD8 留空，其余默认（WBC 6.0、淋巴 35%、CD4 40%）→ 页面显示 `0.00`「CD4/CD8 比值 — 比值降低」，同时提示「CD4/CD8倒置」；期望输出「CD8 缺失，无法计算比值」并隐藏比值判读。node 复算：`ratio = 40/0 → 0`（代码分支），参考区间卡条件 `cd8>0 = false`。
- 影响：`tools/clinical-lab/flow-cytometry-ratio.html`；缺失值被当成真实病理性倒置，且与参考区间卡缺失形成自相矛盾的报告。
- 方案：`cd8<=0` 时比值显示 `—`、状态置「无法计算」，不推入倒置 flag，也不渲染比值标尺；给 CD8/CD4/WBC/淋巴百分比加 >0 必填守卫。

### L-N28 流式页清空 WBC/淋巴百分比/CD4 任一值即提示「CD4<200，AIDS 分期」（高，确认缺陷）
- 问题：绝对计数由 WBC、淋巴百分比、CD4% 连乘得到，三者任一留空都会被 `num()` 归 0，`cd4Abs=0` 命中 `<200`，直接输出「重度免疫抑制，AIDS分期」并推入「CD4 绝对值降低」。若 CD8 仍有值，同一屏还会显示正常的 CD4/CD8 比值，结论互相打架。
- 证据：`tools/clinical-lab/flow-cytometry-ratio.html:259-267`（`||` 缺省式取 0、绝对计数连乘）、`:317-318`（`cd4Abs<414` / `<200` 两个 flag，无 `>0` 守卫）、`:284`（比值仍可正常显示）。
- 复现：WBC 留空（其余默认）→ node 复算 `absLymph=0`、`cd4Abs=0`、`cd8Abs=0`、`ratio=1.60`；页面提示 `CD4绝对值降低` + `CD4<200/μL(重度免疫抑制，AIDS分期)`。期望：输入不全时清空结果并提示补全。
- 影响：`tools/clinical-lab/flow-cytometry-ratio.html`；未录入白细胞或 CD4% 即给出艾滋病期提示，属于高风险的假阳性结论。
- 方案：`absLymph<=0` 时整块结果只显示「请补全 WBC/淋巴百分比/CD4%」；AIDS 分期提示额外要求 CD4% 与绝对计数均 >0，并区分「HIV 阳性」开关后再输出分期。

### L-N29 流式页 Treg 输入完全不参与计算；NK 42/μL、CD4 60% 仍报「各项指标正常」（中，确认缺陷）
- 问题：Treg 只在 `calc()` 里读入一次，之后没有任何绝对计数、参考区间或判读引用；同时异常 flag 只覆盖 CD4 低值、比值、总 T 低、B 低，未覆盖 CD4% 高值、CD8 高低、NK 与 B 的上限。因此 NK 明显降低或 CD4% 超上限时仍可输出「各项指标在参考范围内」。
- 证据：`tools/clinical-lab/flow-cytometry-ratio.html:260`（读取 `treg`，全文无第二次引用）、`:302`（NK 仅显示数值）、`:317-323`（flag 仅 CD4/比值/总T/B 低值）、`:330`（无 flag 即输出「各项指标在参考范围内」）、参考区间表 `:168-172`（含 NK 95–640、CD4 27–51%）。
- 复现：默认参数仅把 NK 改为 2% → node 复算 NK 绝对值 `42 /μL`（低于 95），flags 为空 → 页面显示「各项指标在参考范围内」。再把 CD4 改为 60% → `cd4Abs=1260`（在 414–1611 内）、`ratio=2.40`，flags 仍为空 → 仍报全部正常，尽管 CD4% 60 已高于参考上限 51%。
- 影响：`tools/clinical-lab/flow-cytometry-ratio.html`；低 NK 与高 CD4% 被绿色「全部正常」掩盖，Treg 输入给用户「已纳入分析」的错觉。
- 方案：删除 Treg 输入或在结果区补 Treg 百分比/绝对值与区间；为 CD4%、CD8%、NK、B 增加上下限双向 flag，并让 `:330` 的「全部正常」只在全部亚群均有值且全部在区间内时出现。

### L-N30 流式页 CD4 参考区间三套口径并存（≥500 / 414–1611 / <500 免疫抑制）（中，确认缺陷）
- 问题：参考区间表给 CD4 绝对值 414–1611/μL，绝对计数标尺把 414–500 标为「边缘」、≥500 才算正常，而异常 flag 又把 414–499 一律写「CD4<500 免疫抑制」。同一数值（如 450）在三个位置得到「正常下限内」「边缘」「免疫抑制」三种说法。
- 证据：`tools/clinical-lab/flow-cytometry-ratio.html:168`（表：414–1611）、`:299`（低于 414 才标红）、`:306-308`（标尺 <200 重度、200–414 偏低、414–500 边缘）、`:317-319`（`<414` 降低、`<500` 免疫抑制）。
- 复现：CD4 绝对值 450/μL（如 WBC 6、淋巴 35%、CD4 21.4%）→ 表内属 414–1611、标尺属「边缘(414–500)」、flag 输出「CD4<500/μL(免疫抑制)」。期望三处同源，只保留一套「正常/边缘/抑制」阈值。
- 影响：`tools/clinical-lab/flow-cytometry-ratio.html`；检验人员按不同区块核对会得到不同结论，报告一致性受损（阈值口径需检验科/医师复核）。
- 方案：把表、标尺 bands、flag 阈值抽成同一常量（建议以所用实验室参考区间为准，页面注明来源），并统一 414–500 的措辞（「低于参考下限/边缘」而非「免疫抑制」）。

### L-N31 流式页简介宣称可输入「绝对计数」，实际只有百分比输入（中，确认文案与功能不符）
- 问题：简介写「输入各亚群百分比或绝对计数」，但页面 6 个亚群全部是 `%` 输入，没有绝对计数（/μL）输入或百分比/绝对计数切换；绝对计数只能由 WBC×淋巴%×亚群% 反算。
- 证据：`tools/clinical-lab/flow-cytometry-ratio.html:400`（简介「输入各亚群百分比或绝对计数」）、`:139-154`（输入项均为「(%)」）、`:402`（功能点「亚群百分比与绝对计数对照」）。
- 复现：按简介寻找「CD4 绝对计数 800/μL」输入入口 → 页面无此字段；只能输入 CD4% 后由 `:262` 反算。期望简介与输入一致，或提供「按绝对计数录入」模式。
- 影响：`tools/clinical-lab/flow-cytometry-ratio.html`；检验科报告常直接给绝对计数，用户按简介无法录入，需手工反推百分比。
- 方案：增加「百分比 / 绝对计数」二选一模式（绝对计数模式下由 CD4abs 反推百分比并保留比值），或把简介改为「输入百分比，自动换算绝对计数」。

### L-N32 流式页「结果趋势」图因 parseFloat 读到中文首段永不渲染（中，确认缺陷）
- 问题：历史记录把整段结果文本存入 `结果` 字段，趋势图再对该字段 `parseFloat`。结果 HTML 首段是「计算结果」标题，`parseFloat('计算结果 ...')` 为 NaN，所有记录都被 `isFinite` 过滤，`nums.length` 永远达不到 2，折线图不出现。
- 证据：`tools/clinical-lab/flow-cytometry-ratio.html:276`（结果首段 `<h3>计算结果</h3>`）、`:493`（`rk = en ? 'Result' : '结果'`）、`:433-436`（`textContent` 去空白后整段入库）、`:473-479`（`parseFloat(arr[j].d[rk])` + `isFinite` + `nums.length>=2` 才画线）。
- 复现：连续计算两组默认参数（比值 1.60 与 1.40）→ node 复算 `parseFloat('计算结果 0.50 CD4/CD8') = NaN`；历史表有两行，但折线图仍为空。期望趋势图按比值/绝对计数画线。
- 影响：`tools/clinical-lab/flow-cytometry-ratio.html`；图表 tab 形同虚设，多次随访无法看趋势。
- 方案：历史记录单独存数值字段（`ratio`、`cd4Abs`、`cd8Abs`），趋势图读数值而非结果文本；或从结果 DOM 按已知结构取 `.ratio-big .v` 的数值。

### L-N33 流式页「相关工具」把血气分析卡片重复渲染两次（低，确认缺陷）
- 问题：同一 `blood-gas-analysis.html` 在相关工具网格中出现两次，卡片标题不同，用户会以为是两个不同工具。
- 证据：`tools/clinical-lab/flow-cytometry-ratio.html:383` 与 `:387`（同一个 href、同一目录）。
- 复现：滚动到页面底部「相关工具」→ 可见两张指向 `blood-gas-analysis.html` 的卡片。
- 影响：`tools/clinical-lab/flow-cytometry-ratio.html`；重复入口降低内链质量，也浪费一个推荐位。
- 方案：删除其中一张，替换为真正相关的 `coagulation-inr.html`/`biochemistry-ratio.html` 之外的互补工具（如免疫球蛋白/补体页）。

**留存建议（tools/clinical-lab/flow-cytometry-ratio.html）**
- 支持按检验报告批量录入多个时间点（粘贴「日期 WBC 淋巴% CD4% CD8% …」多行），一次生成 CD4 绝对值与比值趋势，并导出 CSV/报告块。
- 结果区补 Treg、NK、B 的绝对值与上下限箭头，并把「参考区间表—标尺—flag」改为同源配置，输出可直接贴进检验报告的「输入+判读+区间」摘要。
- 增加「HIV 阳性/非 HIV/未标注」开关，非 HIV 的 CD4 低值只提示「细胞免疫抑制，需查因」，不直接输出 AIDS 分期。

### L-N34 寄生虫页短膜壳绦虫卵大小写成「47-37 μm」，区间上下限颠倒（中，确认数据错误）
- 问题：尺寸字段为 `47-37 μm`，上限小于下限；同页其他虫卵均按「小-大」书写。该错误会让按大小筛查时把 37–47 μm 误读为 47 μm 起。
- 证据：`tools/clinical-lab/parasite-egg-id.html:246`（`size:'47-37 μm'`，短膜壳绦虫卵）。
- 复现：页面展开「短膜壳绦虫卵」→ 大小显示 `47-37 μm`；期望 `37-47 μm`（常见资料约 30–47 μm，具体以科室图谱为准）。node 复算：按 `-` 切分 `'47-37'.split('-')` 得 `[47,37]`，首值为上限、末值为下限，任何直接取首值作排序键的实现都会把该卵排在 47 μm 以上。
- 影响：`tools/clinical-lab/parasite-egg-id.html`；形态对照的尺寸是最常用的初筛字段，反序会误导镜检测量。
- 方案：改为 `37-47 μm`，并把 `size` 拆成 `min/max` 数值字段，供筛选与排序使用。

### L-N35 寄生虫页名为「形态识别器」，但搜索只匹配名称+描述，大小/形状/卵壳/卵盖等结构化字段不参与（中，确认缺陷）
- 问题：筛选条件只有 `name` 与 `desc` 两个字符串，用户按「厚壳」「有卵盖」「腰鼓形」「70-106」等形态特征搜索时，只有恰好写进 `desc` 的词才命中；`size/shape/shell/operculum/content` 字段完全不被检索。搜索框标签又写「搜索虫卵名称」，与页面「形态识别」定位不一致。
- 证据：`tools/clinical-lab/parasite-egg-id.html:139`（标签「搜索虫卵名称」）、`:264-270`（只 `e.name` 与 `e.desc` 做 `indexOf`）、`:277-283`（大小/形状/颜色/卵壳/卵盖/内容物是独立字段）、`:418`（简介定位「形态要点对照/易混淆项提示/图谱复习」）。
- 复现：输入「70-106」→ 0 条（该串只在日本血吸虫卵的 `size` 字段）；输入「卵盖」→ 只命中 `desc` 里写了「卵盖」的条目，肝吸虫的 `operculum:'有(明显)'` 不命中（其 `desc` 只写「有盖」）。期望按字段匹配并高亮命中字段。
- 影响：`tools/clinical-lab/parasite-egg-id.html`；镜检时最常见的「按大小/有无卵盖/壳厚薄」检索路径不可用。
- 方案：把 `name/desc/size/shape/color/shell/operculum/content` 统一拼接为检索文本（大小另做数值区间匹配），搜索框改为「搜索名称或形态特征（如：卵盖、70-106、腰鼓）」并显示命中字段。

### L-N36 寄生虫页「图谱复习」无任何虫卵图；图表只是类别计数且不随筛选变化（低，确认缺陷）
- 问题：简介与功能点宣称「图谱复习」，但页面没有任何虫卵插图或示意图；CSS 里定义了 `.egg-svg` 却从未使用。默认打开的「图表」只把 12 个条目按「线虫/吸虫/绦虫」计数（5/5/2），既不体现形态，也不随搜索/分类筛选更新。
- 证据：`tools/clinical-lab/parasite-egg-id.html:30`（`.egg-svg` 仅有样式、无使用）、`:148`（图表 tab 默认 active）、`:305-306`（`EGGS.forEach` 全量计数）、`:318`（第二处全量计数）、`:418`（「图谱复习」）、`:355-357`（tab 切换只隐藏/显示，不重算）。
- 复现：筛选「吸虫」后切到图表 → 饼图仍是全部 12 项的 5/5/2 分布；展开任一虫卵卡片 → 只有文字字段，没有图。期望图表按当前筛选结果更新，或直接改为形态示意图。
- 影响：`tools/clinical-lab/parasite-egg-id.html`；「图谱复习」承诺落空，图表对鉴别诊断没有信息量。
- 方案：为每个虫卵补 SVG/示意图（复用 `.egg-svg` 容器）并标比例尺；图表改为当前筛选集合的类别分布，或在筛选时同步重算；若不打算做图，删掉「图谱复习」表述并把图表 tab 换成「易混淆对比表」。

**留存建议（tools/clinical-lab/parasite-egg-id.html）**
- 增加多字段形态筛选（大小区间、形状、卵壳厚薄、有无卵盖、内容物、颜色），并按尺寸排序/并排对比易混淆对（肝吸虫 vs 姜片虫、蛔虫受精 vs 未受精）。
- 每个虫卵配一张带比例尺的 SVG 示意图（已有 `.egg-svg` 样式可直接复用），支持点击放大。
- 「导出」改为导出当前筛选结果，并加「镜检记录」模板（样本号、视野、测量尺寸、所见、结论），便于检验科留档。

### 承诺 vs 实际（Q 批专项）

- `tools/clinical-lab/flow-cytometry-ratio.html`：简介「输入各亚群百分比或绝对计数」（`:400`）vs 实际 6 个输入全为百分比（`:139-154`）——**未实现绝对计数录入**，判定：文案承诺 > 功能。
- `tools/clinical-lab/flow-cytometry-ratio.html`：功能点「亚群百分比与绝对计数对照」（`:402`）vs Treg 输入读后即弃（`:260`）、NK/B 无上下限判读（`:317-323`）——**「对照」只覆盖部分亚群**，判定：部分实现。
- `tools/clinical-lab/parasite-egg-id.html`：简介「图谱复习」（`:418`）vs 页面无图、`.egg-svg` 空置（`:30`）——**图谱未实现**，判定：承诺未实现。
- `tools/clinical-lab/parasite-egg-id.html`：页面命名/简介的「形态识别」vs 搜索仅名称+描述（`:264-270`）——**按形态识别未实现**，判定：承诺 > 功能。
- 复制/导出：两页均有导出入口（`flow-cytometry-ratio.html:158` + `:512`、`parasite-egg-id.html:145` + `:333-340`），流式页另有复制结果（`:159` + `:351`），寄生虫页无复制结果按钮；未发现「宣称复制/导出但按钮缺失」；但流式页的趋势图因结果文本解析失败不渲染（见 L-N32），属「有图表入口无有效输出」。
- 本批 2 页未发现「限时、核验、ROI、难度分级」类营销宣称；「自动识别」仅寄生虫页以名称搜索的形式出现，已并入 L-N35。

### 覆盖

- 实读 2 页：`tools/clinical-lab/flow-cytometry-ratio.html`、`tools/clinical-lab/parasite-egg-id.html`。
- 新增 10 条（L-N27–L-N36）：高 2、中 6、低 2；另每页 3 条留存建议。
- 未覆盖：`clinical-lab` 其余页、`zh-tw/` 繁体产物、英文态运行时字典；未做浏览器、移动端、门禁与线上验证，未做文献级阈值核验（L-N30/L-N34 的参考区间与虫卵尺寸需检验科复核）。

### L-N37 尿沉渣页搜索只匹配名称/临床意义/形态，大小、颜色、参考区间不参与，「7-8」「无色」「0/HP」均查不到（中，确认缺陷）
- 问题：`filterItems()` 只用 `name/sig/morph` 三字段做 `indexOf`；`size/bg/mean` 是独立字段但不可检索。镜检最常用的检索入口恰是「7-8 μm 的红细胞」「无色透明管型」「0/HP 病理性结晶」，这些词都落在未检索字段；公式框却把三字段规则写成既定设计。
- 证据：`tools/clinical-lab/urine-sediment-atlas.html:280`（三字段 `indexOf`）、`:249-251`（红细胞 size 7-8 μm、白细胞 10-14 μm）、`:239-247`（结晶 mean 0/HP / 少量/HP）、`:230-259`（bg 无色/黄褐色…）、`:138`（公式框写明只查名称+临床意义+形态）、`:144`（搜索框占位「管型、结晶、红细胞」）。
- 复现：node 按页面同款过滤：输入「7-8」→ 0 条，而字段库中有 1 条（红细胞均一型）；输入「无色」→ 仅 1 条（透明管型），实际 `bg` 含「无色」的有 13 条；输入「0/HP」→ 0 条，实际 `mean` 含「0/HP」的有 8 条。期望：输入「7-8」命中红细胞、「0/HP」命中病理性结晶。
- 影响：`tools/clinical-lab/urine-sediment-atlas.html`；按尺寸/颜色/参考区间检索全部失效，图谱查询退化为名称检索。
- 方案：把 `name/sig/morph/size/bg/mean` 合并为检索文本（size 另做数值区间匹配），搜索框提示改为「名称/大小/颜色/参考区间（如：7-8、无色、0/HP）」并高亮命中字段。

### L-N38 尿沉渣页名为「图谱」却无任何图像；「图表」tab 因结果文本恒为条目名列表而永不渲染（中，确认缺陷）
- 问题：全文没有 `<img>`/`<svg>`，只有文字「形态」描述；页面注入的 tab 默认打开「图表」，但 `nums` 来自 `parseFloat(结果文本)`，而结果文本是 `itemList` 的前 80 个字（「透明管型管型颗粒管型…」）→ 恒为 NaN，`nums.length>=2` 永不成立，图表永久空白。
- 证据：`tools/clinical-lab/urine-sediment-atlas.html:130`（图表 tab 首位）、`:500`（默认 `show(btns[0])`）、`:385-392`（`__urine_sediment_atlasResText` 取 itemList 文本前 80 字）、`:427-431`（`parseFloat` + `nums.length>=2` 才画）、`:139`（「图谱式对照」）、`:174`/`:352`（深度解析与简介均称「图谱」）。
- 复现：用搜索词「管型」与「结晶」各产生一条历史 → 打开「图表」仍空白；node `parseFloat('透明管型管型颗粒管型管型红细胞管型')` = `NaN`。期望：图表按当前筛选集合做类别统计，且每个条目有可对照的形态示意图。
- 影响：`tools/clinical-lab/urine-sediment-atlas.html`；「图谱」承诺落空，「图表」成为永久空面板，用户会误以为功能故障。
- 方案：图表改为当前筛选集合的分类计数（或在筛选时重算）；为条目补带比例尺的 SVG 示意图；若不打算做图，删除「图谱」表述并把图表 tab 换成「易混淆对比表」。

**留存建议（tools/clinical-lab/urine-sediment-atlas.html）**
- 检索扩展到 `size/bg/mean`，支持数值区间（如 7-8 命中 7–8 μm）与命中字段高亮。
- 为 27 个条目配带比例尺的示意图，并做易混淆并排对比（红细胞均一/非均一、透明/颗粒/蜡样管型、草酸钙/尿酸结晶）。
- 增加「镜检记录」模式：样本号、视野计数、所见条目、结论，导出当前筛选结果而非空历史表。

### L-N39 精液页清空浓度即判「无精子症」，PR+NP 可 >100% 仍判「生育力良好」（高，确认缺陷）
- 问题：`num()` 对空值返回 0，空值直接进入诊断；`conc===0` 被当作无精子症。同时 PR/NP/形态/存活率无 0–100 校验，总活力可超过 100%。
- 证据：`tools/clinical-lab/semen-analysis.html:253`（`num()` 空值返 0）、`:261-264`（取值与 `totalMot=pr+np`）、`:278`/`:282`（少精子症与 `conc===0` 无精子症）、`:288`（总活力显示）、`:294-296`（TMSC 分档）。
- 复现：清空「精子浓度」→ node 复算 `total=0`、`TMSC=0`，诊断「少精子症、无精子症」、判「生育力受损」；期望提示「请填写浓度」而非无精子症。输入 PR 150、NP 10 → 总活力 160%、TMSC 192×10⁶，仍判「生育力良好」；期望 0–100 范围校验并拒绝计算。
- 影响：`tools/clinical-lab/semen-analysis.html`；空白/误填会直接产出「无精子症」这一重大诊断，属于高风险误读。
- 方案：空值走「待填」分支并跳过相关判定；PR/NP/IM、形态、存活率加 0–100 校验，并对 PR+NP+IM≤100 给出提示（阈值需男科/生殖医师复核）。

### L-N40 精液页 IM（不动精子%）输入不参与任何计算，且恒显示「✓ 正常」（中，确认缺陷）
- 问题：`im` 读入后从未参与 `totalMot/TMSC` 或诊断，`setInterp('im', true)` 无条件标「✓ 正常」。用户填 IM 100% 仍显示正常，输入形同装饰。
- 证据：`tools/clinical-lab/semen-analysis.html:261`（`im=num('im')` 后再未引用）、`:270`（`setInterp('im', true, '', '')`）、`:263`（`totalMot=pr+np`）。
- 复现：node 固定其余输入，`im=0` 与 `im=100` 得到总活力均为 55%、TMSC 66×10⁶，结果区无任何 IM 字段。期望：IM 参与「PR+NP+IM 是否合计 100%」的一致性提示，并按 WHO 的存活率口径给出判读。
- 影响：`tools/clinical-lab/semen-analysis.html`；一个可见输入对结论零影响，易让用户误以为已纳入评估。
- 方案：让 IM 参与合计校验与「不动精子比例」提示；若暂不实现，删除该输入或明确标注「不参与本工具判读」。

### L-N41 精液页引据行「WHO 6th ed. (2010)」与正文 WHO 5th(2010) 冲突，且 2010 年版是第 5 版（低，确认错误）
- 问题：同一页参考下限表头写「WHO 第5版(2010)」，引据表却写「WHO 6th ed. (2010)」；WHO 第 6 版为 2021 年，2010 年对应第 5 版。
- 证据：`tools/clinical-lab/semen-analysis.html:224`（「WHO 6th ed. (2010) semen ref」）、`:160`（「WHO 第5版参考下限(第5百分位)」）、`:208`（FAQ「WHO 第 5 版（2010）」）、`:305`/`:315`（标尺与参考卡均写 WHO 5th）。
- 复现：查看「引据标准」表 → 版次与年份自相矛盾；2010 年版实为第 5 版。期望：全页统一为「WHO 第5版(2010)」。
- 影响：`tools/clinical-lab/semen-analysis.html`；引据可信度受损，用户按第 6 版核对会得到不同下限。
- 方案：统一为 WHO 第5版(2010)；若要支持第 6 版，整表换数值并加版次切换（阈值需生殖医学复核）。

### L-N42 甲状腺页单侧激素升高/缺项被当作「正常」：FT3 10 pmol/L 仍输出「各项指标在参考范围内」（高，确认缺陷）
- 问题：分型只用 `hormoneHigh/hormoneLow` 的总布尔，`else` 兜底一律「甲状腺功能正常」；FT3 高但 TSH 正常既不是甲亢也不进任何分支，直接落到 else。未填项为 `null` 被当作「不低不高」，仅填 TSH 8 即判「亚临床甲减」。
- 证据：`tools/clinical-lab/thyroid-function-model.html:284-288`（布尔聚合）、`:291-319`（六分支 + else）、`:315-318`（else 文案「各项指标在参考范围内」）、`:258`（`num()` 空值为 `null`）、`:248`（参考区间）。
- 复现：node：TSH 2.0 + FT3 10（>6.8）+ FT4 16 → 「甲状腺功能正常 / 各项指标在参考范围内」；TSH 2.0 + FT4 30 → 同样「正常」；TSH 8 + FT4 留空 → 「亚临床甲减」。期望：单侧升高输出「FT3/T4 升高待查」，缺 FT4 时不得判亚临床甲减。
- 影响：`tools/clinical-lab/thyroid-function-model.html`；T3 型甲亢/单侧升高被漏报，仅 TSH 升高被过度诊断，均属高风险。
- 方案：新增 `hormoneHigh && TSH 正常` 的「T3/T4 升高待查」分支；对缺失 FT3/FT4 返回「请补充」；TSH 0 也应按「测不出」提示而非亚临床甲亢（阈值需内分泌医师复核）。

### L-N43 甲状腺页清空 TSH 直接 return，结果区保留上一次结论且无「待填」提示（中，确认缺陷）
- 问题：`if(tsh==null) return;` 只中止本次渲染，不清理 `#result`，上一次的分型与标尺残留在页面上。
- 证据：`tools/clinical-lab/thyroid-function-model.html:269`（`if(tsh==null) return;`）、`:276`（结果 HTML 从「结果分析」开始重建）。
- 复现：先输入 TSH 0.05 → 「亚临床甲亢」；再清空 TSH 输入框 → 结果区仍是「亚临床甲亢」（仅参考标尺消失）。期望：清空后显示「请填写 TSH」或把结果置灰失效。
- 影响：`tools/clinical-lab/thyroid-function-model.html`；用户改参数后看到的是旧结论，容易误读。
- 方案：空值时清空结果并提示「TSH 为必填」，或保留结果但加「已失效，请重新分析」遮罩。

### L-N44 甲状腺页公式框把 `formula-eq` 放在 `formula-title` 之前，标题显示在公式下方（低，确认缺陷）
- 问题：`formula-box` 内先输出公式正文、后输出「📐 工作原理与说明」标题，与同批其他页的「标题在上」结构相反。
- 证据：`tools/clinical-lab/thyroid-function-model.html:132`（同一行 `formula-eq` 在前、`formula-title` 在后）；对照 `tools/clinical-lab/semen-analysis.html:138`（title 在前）。
- 复现：打开「工作原理与说明」区块 → 公式正文在上、标题在下。期望：标题在公式上方。
- 影响：`tools/clinical-lab/thyroid-function-model.html`；版式一致性。
- 方案：把 `formula-title` 移到 `formula-eq` 之前，构建后复查。

**留存建议（tools/clinical-lab/semen-analysis.html）**
- 空值与越界校验（0–100、PR+NP+IM≤100），结果中区分「未填」与「0」。
- 让 IM 参与总活力一致性提示或删除该输入；补精子总数/浓度单位换算与复查次数提示。
- 明确标注 WHO 版次与参考下限来源，支持第5/6版切换并注明报告须写版次。

**留存建议（tools/clinical-lab/thyroid-function-model.html）**
- 补「单侧激素升高」与「缺项」分支（T3 型甲亢、仅 TSH 升高需复查 FT4），并处理 TSH=0。
- TPO 阈值抽为常量并注明检测平台差异；提供妊娠/老年参考区间切换（需医师复核）。
- 修正公式框标题顺序；示例按钮点击后自动切回「结果」tab，避免结果被隐藏。

### 承诺 vs 实际（R 批专项）

- `tools/clinical-lab/urine-sediment-atlas.html`：标题/meta/简介「图谱查询器/图谱式对照」（`:10`、`:16`、`:139`、`:352`）vs 全文无 `img/svg`，只有文字形态 + 永久空白的图表 tab（`:130-132`、`:427-431`）——**图谱未实现**，判定：承诺 > 功能。
- `tools/clinical-lab/urine-sediment-atlas.html`：「导出明细 CSV」（`:148`、`:466`）vs 首次打开历史表尚未渲染，`exportTable` 遇空表直接 `return false`（`js/tool-kit.js:226`），页面 `try/catch` 吞掉——**有入口无输出**，判定：功能缺失（8 页共性）。
- `tools/clinical-lab/semen-analysis.html`：引据行「WHO 6th ed. (2010)」（`:224`）vs 正文 WHO 5th（2010）（`:160`、`:208`）——**版次错配**，判定：文案错误（见 L-N41）。
- `tools/clinical-lab/semen-analysis.html`：TMSC「≥20×10⁶ 生育力良好、5–20 临界、<5 受损」（`:138`、`:294-296`）为研究性阈值且未给出来源——判定：待验证（需生殖医学复核）。
- `tools/clinical-lab/thyroid-function-model.html`：「以 TSH 为核心、结合 FT3/FT4 分型」（`:132`）vs 单侧升高落 else「正常」、缺 FT4 仍判亚临床（`:291-319`）——**分型不完整**，判定：承诺 > 功能（见 L-N42）。
- 复制/导出：尿沉渣页仅导出（`:148`/`:466`，无复制）；精液页导出+复制（`:154-155`、`:334`、`:497`）；甲状腺页仅导出（`:150`/`:514`，无复制）；三页导出均指向历史表，首次点击无输出。
- 本批 3 页未发现「限时、核验、ROI、难度分级」类宣称；「识别」仅尿沉渣 meta 的「辅助显微镜检识别」，实为人工文字对照，无自动识别。

### 覆盖

- 实读 3 页：`tools/clinical-lab/urine-sediment-atlas.html`、`tools/clinical-lab/semen-analysis.html`、`tools/clinical-lab/thyroid-function-model.html`。
- 新增 8 条（L-N37–L-N44）：高 2、中 4、低 2；另每页 3 条留存建议。
- 未覆盖：`clinical-lab` 其余页、`zh-tw/` 繁体产物、英文态运行时字典；未做浏览器、移动端、门禁与线上验证。
- 阈值核验：尿沉渣参考区间、精液 WHO 版次与 TMSC 分档、甲状腺参考区间与 TPO 阈值（34 IU/mL）均需检验科/男科/内分泌医师复核。

## T 批 消化内科 覆盖（2026-11-04）

### L-N45 Child-Pugh 空值被当 0：清空胆红素/PT 反而「改善」分级，清空白蛋白重取 3 分，且两个下拉默认就是最差档（高，确认缺陷）
- 问题：`parseFloat(...)||0` 把空值一律变 0；胆红素 0→1 分、PT 0→1 分、INR 0→1 分（均当作正常），而白蛋白 0→`<28`→3 分（当作最差）。腹水/脑病下拉预选 `2`（中-大量、III-IV 级），首屏默认即 10 分 C 级。
- 证据：`tools/gastroenterology/child-pugh.html:264-267`（空值转 0）、`:275-282`（胆红素/白蛋白分档）、`:286-293`（PT/INR 分档）、`:139`/`:147`（两个 `selected` 均为 2）、`:313-328`（分级分支）。
- 复现：node 复算：默认 35/30/4/1.7/2/2 → 10 分 C 级；仅清空胆红素 → 9 分 B 级（清空反而「升级」）；仅清空白蛋白 → 11 分 C 级；白蛋白 40 + 其余全空 + 腹水无/脑病无 → 3 分 A 级（低于 5 分下限）。期望：缺项提示「请填写」，不参与计分。
- 影响：漏填任一项即得到错误分级，且默认 C 级会让未编辑用户误以为示例已失代偿。阈值/分界需临床复核。
- 方案：空值走「待填」分支并阻止出分；必填项加校验；下拉改为中性「请选择」或默认「无」。

### L-N46 Child-Pugh 注释给出 PBC 胆红素调整，但无任何入口（中，确认缺陷）
- 问题：页面注明原发性胆汁性胆管炎用 `<68 / 68-170 / >170` 分档，calc 却固定用 `<34 / 34-51 / >51`，输入区无「是否 PBC」开关，PBC 患者胆红素项被系统性高估。
- 证据：`tools/gastroenterology/child-pugh.html:173`（PBC 注释）vs `:275-277`（固定阈值）；`:124-150`（输入区无该开关）。
- 复现：node：PBC 患者 TBIL 60 → 页面 2 分（应 1 分）；TBIL 100 → 3 分（按页内 68-170 应为 2 分）。
- 影响：PBC 患者总分与分级偏高，可能影响手术风险判断。阈值需肝病科复核。
- 方案：新增「是否 PBC」并按注释切换胆红素阈值；否则删除该注释，避免用户误以为已支持。

### L-N47 Glasgow 清空钙/白蛋白/PaO₂ 各得 1 分，轻症被直接判成重症（高，确认缺陷）
- 问题：三项均为「低于阈值得分」，空值→0 天然满足 `<2.0`、`<32`、`<60`，各 +1；其余「高于阈值得分」项空值则为 0 分，空值方向不一致。
- 证据：`tools/gastroenterology/glasgow-pancreatitis.html:266-274`（空值 0）、`:294`（钙）、`:297`（白蛋白）、`:303`（PaO₂）、`:312-316`（≥3 判重症）。
- 复现：默认 55/15/10/350/200/2.0/32/8/65 → 0 分「轻症」；清空钙+白蛋白+PaO₂ → 3 分「重症急性胰腺炎，入住 ICU」。期望：缺项提示「待填」。
- 影响：漏填三项即被建议 ICU；漏填一项也会 +1，可能把 2 分轻症推成 3 分重症。阈值需临床复核。
- 方案：空值不参与计分并阻止出结论，结果区标注缺项清单。

### L-N48 Glasgow 参考标尺把 0–6 分整段标成「重症」，轻症被视觉误标（中，确认缺陷）
- 问题：refBar 只有两带，`0–6` 全标「重症」、`≥6` 标「极危重」，没有 `<3` 轻症带；0–2 分患者的读数落在「重症」带，与文字结论相反。
- 证据：`tools/gastroenterology/glasgow-pancreatitis.html:337`（bands `{lo:null,hi:6,label 重症}` / `{lo:6,label 极危重}`）vs `:307-321`（<3 轻症、3-5 重症）。
- 复现：默认输入（0 分）→ 结果文字「轻症可能性大」，标尺色带显示「重症」。期望三带 `<3 / 3-5 / ≥6`。
- 影响：同一页图表与结论矛盾，轻症被标成重症。阈值需临床复核。
- 方案：按 3、6 两个切点重建三带并补「轻症」label。

### L-N49 Glasgow 引据表写「8 项」且漏列 AST，与实际 9 项评分表矛盾（中，确认缺陷）
- 问题：实际计分 9 项，引据表只列 8 项（Age/WBC/glucose/urea/PO₂/calcium/albumin/LDH，缺 AST），且文字写「8 项指标」；用户按引据表准备数据会漏掉 AST。
- 证据：`tools/gastroenterology/glasgow-pancreatitis.html:236`（"8 项指标在 48 h 内评估"）、`:246`（8 项枚举）vs `:161-174`（9 行评分表含 AST）、`:291`（AST 计分）。
- 复现：node：AST 210 且其余不达标 → 1 分；只按引据表核对会漏掉这 1 分，3 分重症被算成 2 分轻症。
- 影响：漏项导致系统性低估 1 分，跨越 3 分分界时分级错误。分界需临床复核。
- 方案：引据表改为 9 项并补 AST，与正文评分表同步。

### L-N50 CDAI 清空 Hct 被当 0，凭空 +222 分，直接推入中度活动（高，确认缺陷）
- 问题：`hct||0` 后 `hctStd-hct` 达 37，×6 = 222 分，任何患者的 CDAI 都会被抬高；Hct 未做 20–60% 范围校验。
- 证据：`tools/gastroenterology/cdai.html:272`（空值 0）、`:281-282`（标准值减实测值）、`:284`（加权求和）、`:301-313`（分级）。
- 复现：node：默认女性 14/10/7/1/0/0/35/-5 → 154「轻度活动」；仅清空 Hct → 364「中度活动」（`<=450`）。期望：提示 Hct 必填。
- 影响：漏填一项即误判中重度，页面随即建议激素/生物制剂。阈值需消化科复核。
- 方案：Hct 空值拦截并提示；加 20–60% 合法性校验，越界报错。

### L-N51 CDAI 的 Hct 标准值 42/37 与 Best 1976 通行 47/42 不符，恒定少 30 分（高，需临床复核）
- 问题：页面表格、deep-dive、代码统一用「男 42−Hct、女 37−Hct」，通行 CDAI 公式为「男 47−Hct、女 42−Hct，×6」；两者恒差 5 个百分点 Hct → 30 分 CDAI，足以跨越 150 缓解分界。
- 证据：`tools/gastroenterology/cdai.html:169`（表「男:42-Hct, 女:37-Hct」）、`:217`（deep-dive 同值）、`:281`（`gender==='male'?42:37`）。
- 复现：node：女、Hct 34、体重 −3、14/10/5/0/0/0 → 页面 128 分「缓解」；按 47/42 口径 → 158 分「轻度」。默认女性案例页面 154 vs 47/42 口径 184。
- 影响：缓解/轻度被系统性错分 30 分，可能漏判活动期。**口径与分界需消化科医师复核**。
- 方案：核对本院采用口径后改为 47/42 并注明出处；若确用 42/37，须在页面标注来源与适用人群。

### L-N52 SAAG 空值/负梯度直接判「非门脉高压性腹水」，并给出结核/恶性检查建议（高，确认缺陷）
- 问题：两值 `||0`；血清空白、腹水 12 → SAAG −12，仍进入 `<11` 分支，输出「非门脉高压性腹水」及细胞学/ADA/淀粉酶建议；无 0–60 g/L 校验，也无负值报错。
- 证据：`tools/gastroenterology/saag-ascites.html:262-265`（空值 0 与差值）、`:274-292`（二分支）、`:126`（公式框自述「两值缺省按 0，无强校验」）。
- 复现：node：0/12 → −12.0 → 非门脉高压性；0/0 → 0.0 → 非门脉高压性；仅填腹水 12 亦然。期望：缺项提示，负值报「输入有误」。
- 影响：空白或误填会否定门脉高压，把病因方向引向结核/恶性。11 g/L 阈值需消化科复核。
- 方案：任一为空即不出结论；`saag<0` 报错；校验 0–60 g/L 与「腹水≤血清」合理性。

### L-N53 肝性脑病页把「四项全正常」判为 0 级=MHE 并建议乳果糖（高，确认缺陷）
- 问题：0 级被直接等同于 MHE，代码四项全 0 → grade 0 → 输出「轻微型肝性脑病（MHE）」并建议乳果糖；但页面没有任何 NCT-A/B、符号数字测试等 MHE 确诊输入，正常人也必然落入该分支。另「取四项最高」使意识清醒 + 扑翼样震颤选「4 消失(深昏迷)」时直接判 Ⅳ 级。
- 证据：`tools/gastroenterology/hepatic-encephalopathy.html:298`（取最高）、`:300-307`（0 级=MHE 描述）、`:310-313`（grade 0 输出 MHE + 乳果糖）、`:196`（MHE 需心理/神经生理检查确诊）。
- 复现：node：四项全选「正常/无」→「0级（MHE）…建议乳果糖口服」；期望「无肝性脑病（未达 MHE 诊断）」。意识 0/行为 0/认知 0/扑翼 4 → 「Ⅳ级（昏迷）」。
- 影响：完全正常者被贴 MHE 标签并接受不必要用药；单项极端选项可伪造 Ⅳ 级。分级与阈值需肝病科复核。
- 方案：拆分「无 HE（0 级）」与「MHE（需测试阳性）」；未提供测试结果时不得输出 MHE；对「扑翼样震颤消失」需与意识等级一致性校验。

### L-N54 胆红素页空值判「正常范围」，仅填 TBIL 判「溶血/Gilbert」并建议 Coombs/UGT1A1（高，确认缺陷）
- 问题：两值 `||0`，且 `tbil<=ref` 分支优先，0 直接判正常；仅填 TBIL 85、DBIL 空 → 比值 0.0% → 走 `<20` 分支，判「间接胆红素升高为主（溶血性/Gilbert）」。
- 证据：`tools/gastroenterology/bilirubin-ratio.html:262-263`（空值 0）、`:269`（比值）、`:279-289`（正常与间接升高分支）、`:333`（标尺同口径）。
- 复现：node：0/0 → ratio 0.0%「正常范围/无明显黄疸」；85/空 → ratio 0.0%「溶血/Gilbert」，并建议 LDH、网织红、Coombs、UGT1A1。期望：任一为空即提示「请填写」。
- 影响：空表得到「正常」或直接指向溶血检查，两个方向都错。分界（20/35/60%）需检验科复核。
- 方案：两值均必填，缺项不出结论；补充「仅填一项」时的明确提示。

### L-N55 胆红素页展示 DBIL 参考上限 6.8/8.0，但代码从不校验 DBIL（中，确认缺陷）
- 问题：ref 下拉文案含「DBIL≤6.8 / ≤8.0」，但 `refVal` 只作为一个 TBIL 阈值使用，DBIL 上限完全未参与判断；TBIL 21、DBIL 15 仍判「正常范围」。
- 证据：`tools/gastroenterology/bilirubin-ratio.html:133-136`（选项文案）、`:264`（只取单个 `refVal`）、`:279-282`（仅比较 `tbil<=refVal`）。
- 复现：node：TBIL 21 / DBIL 15 → ratio 71.4%，类型仍「正常范围」；期望提示「直接胆红素升高（>6.8）」并考虑 Dubin-Johnson/Rotor。
- 影响：孤立直接胆红素升高被漏报为正常。参考上限需检验科复核。
- 方案：把参考拆成 `tbilMax` / `dbilMax` 两值，分别判定并给出单项升高提示。

### L-N56 胆红素页 DBIL>TBIL 时静默封顶，掩盖录入错误仍出「梗阻性黄疸」（中，确认缺陷）
- 问题：`if(dbil>tbil){dbil=tbil;}` 把不可能输入改成 100% 比值，无任何提示，继续输出高置信度分类。
- 证据：`tools/gastroenterology/bilirubin-ratio.html:266`（静默封顶）、`:269`（比值）、`:296-311`（>60% 梗阻分支）。
- 复现：node：85/100 → DBIL 被改为 85 → ratio 100.0%「梗阻性黄疸」，建议超声/MRCP；期望报「DBIL 不应大于 TBIL」。
- 影响：录入错误被包装成明确结论，可能触发不必要的影像检查。分界需临床复核。
- 方案：改为显式报错并停止计算，保留原值供用户核对。

### L-N57 Mayo 仅凭总分 ≤2 判「缓解期」，与页内「且单项 ≤1」自相矛盾（中，确认缺陷）
- 问题：代码只判 `score<=2`；页内 FAQ 与通行临床缓解定义要求便血 0 且便次 ≤1。便次 2 分、其余 0 分 → 总分 2 → 判「缓解期」。
- 证据：`tools/gastroenterology/mayo-score.html:307`（`if(score<=2)`）、`:243`（FAQ「≤2 且单项 ≤1」）、`:136-144`（便次选项）。
- 复现：node：2/0/0/0 → 总分 2、部分 Mayo 2 → 「缓解期，继续维持治疗」；期望「未达缓解/轻度活动」。阈值需消化科复核。
- 影响：未达缓解者被判缓解，可能延误升级治疗。方案：缓解判定加 `stool<=1 && bleeding===0`（或按部分 Mayo ≤1），并在结果中显示单项条件。

### L-N58 HP 耐药页「青霉素过敏」分支屏蔽全部药敏与治疗史，仍推荐已知耐药抗生素（高，确认缺陷）
- 问题：`if(penicillin)` 最先命中，分支内完全不读 `clarithro/metronidazole/levo/history`；铋剂可用时「替代方案」含克拉霉素（即使克拉霉素耐药），无铋剂时两条方案都含克拉霉素、其中一条还含左氧（即使左氧耐药）；既往失败≥2 次也拿不到难治方案。非过敏分支中 `clarithro==='unknown'` 亦按「非耐药」处理，等同未检测即敏感。
- 证据：`tools/gastroenterology/hp-resistance.html:303-313`（青霉素分支与两条方案）、`:284-289`（这些输入在该分支未被引用）、`:314-348`（其他分支才使用）、`:317`（仅 `resistant` 才避开克拉霉素）。
- 复现：node：青霉素过敏+铋剂+克拉耐药+甲硝唑耐药+左氧耐药 → 方案2 仍「PPI+铋+克拉霉素+甲硝唑」；青霉素过敏+无铋剂+克拉耐药+左氧耐药 → 两条方案均含克拉霉素（第二条含左氧）。期望：按耐药结果过滤每条方案。
- 影响：直接推荐已知耐药抗生素，根除失败风险升高；治疗史被忽略使难治病例拿到初治方案。方案与阈值需消化科/感染科复核。
- 方案：先统一计算「禁用药物集」（青霉素过敏→禁阿莫西林；克拉/左氧/甲硝唑耐药→剔除或降级），再按 history 选层级；每条候选方案做禁用集校验后才输出。

### 覆盖清单（T 批 · 8 页）

- `tools/gastroenterology/child-pugh.html`：2 条（L-N45 高、L-N46 中）。PT/INR 取高分、A/B/C 分界与正文表一致；问题集中在空值与 PBC 分支缺失。
- `tools/gastroenterology/glasgow-pancreatitis.html`：3 条（L-N47 高、L-N48 中、L-N49 中）。9 项阈值方向（>55/>15/>10/>600/>200/<2.0/<32/>16/<60）与正文表逐项一致；问题为 `<` 类指标空值误计分、标尺色带缺失轻症、引据表漏 AST。
- `tools/gastroenterology/cdai.html`：2 条（L-N50 高、L-N51 高）。8 项均被读取、加分方向正确；问题为 Hct 空值与 Hct 标准值口径。
- `tools/gastroenterology/mayo-score.html`：1 条（L-N57 中）。4 项子评分与 0–12 总分、3/6/11 分界与正文表一致；问题仅为「总分≤2 即缓解」与页内单项条件矛盾。
- `tools/gastroenterology/saag-ascites.html`：1 条（L-N52 高）。11 g/L 阈值方向与表一致；问题为空值/负梯度无拦截。
- `tools/gastroenterology/hepatic-encephalopathy.html`：1 条（L-N53 高）。四档选项与正文表基本对应；问题为 0 级=MHE 的误判与「取最高」一致性。
- `tools/gastroenterology/bilirubin-ratio.html`：3 条（L-N54 高、L-N55 中、L-N56 中）。20/35/60% 分界方向与表一致；问题为空值、DBIL 上限死参数、DBIL>TBIL 静默封顶。
- `tools/gastroenterology/hp-resistance.html`：1 条（L-N58 高）。非过敏分支的分层逻辑大体可用；问题为青霉素分支覆盖一切且不做耐药过滤。

- 本批共实读 8 页，新增 14 条（L-N45–L-N58）：高 8、中 6。
- 方法声明：仅源码通读 + 在 `/tmp` 用 node 复刻 `calc()` 实算边界输入；**未开浏览器、未跑 `_build.py` / 门禁、未做线上验证、未核对 `zh-tw/` 与英文态字典**。
- 阈值声明：Child-Pugh 分档与 PBC 标准、Glasgow 9 项阈值与 3/6 分界、CDAI Hct 常数 42/37 与 47/42 两口径、SAAG 11 g/L、West Haven 分级、胆红素 20/35/60% 与 DBIL 6.8/8.0、Mayo 缓解定义、HP 各方案与耐药阈值——**均需相应专科临床复核**。
