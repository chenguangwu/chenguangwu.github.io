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
