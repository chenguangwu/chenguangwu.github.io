# 医疗 · 药物剂量类（health/medical/clinical-nursing 剂量页 ~40 页）

## 2026-11-06 医疗工具静态续审

- `tools/medical/clinical-tools.html:461-475`：65–74 岁与 ≥75 岁可同时勾选并相加，评分与建议可能失真；历史 MELD 旧系数及肌酐无上限的关键代码已变，现为 `:508-523` 公式、上下限及血钠修正，临床准确性需专业回归。
- `tools/medical/drug-info.html:389-400,477-484`：搜索仍受当前分类约束，点击其他分类后再点降压预设不会重置分类；匹配字段仍不含禁忌。内置药物信息本轮未做权威核验。
- `tools/medical/reminder-2.html:396-425,442-450,489-513`：历史“安全筛选含关注、无效日期误判”相关代码已变，现分开过滤并设置无效状态。`new Date('YYYY-MM-DD')` 按 UTC 解析后归零到本地日期，UTC 负时区会提前一天；DST 切换日再以固定 24 小时相除也可能出现日期差一日。仅源码分析，未进行时区或浏览器验证。

## 2026-11-06 药效期与排程静态续审

- `tools/medical2/drug-expiry.html:315-317,405-418,442-453`：空阈值或 0 回退 180/30，阈值大小关系无校验；数量空或 0 被存为 1，负数可保存。清理过期操作直接过滤并持久化，无确认或撤销，与「清空全部」不同；自定义阈值后剩余天数颜色仍按固定 30/180 天着色（`:364`）。
- `tools/medical2/surgery-duration.html:362-383`：打开准备时间后清空任意时长按 0 求和，负数也可参与计算；隐藏该区间则不计额外时间。排程结果仅为代码口径，具体时长和临床适用性未核验；未运行页面。

## 功能缺陷
- 儿童剂量页均无「年龄→体重默认填充」（WHO 中位体重表，静态可行）。
- 无「肝肾功能调整提示」（剂量页联动 eGFR 结果给出减量建议文案）。

## 优化点
- S8 空态教育化最适合本类：每个输入框 placeholder 给「典型值+范围」。
- 药品库数据集中 json 化（当前散在页内 JS），便于审校与后续扩充。

## 受影响范围
- tools/health/（child-medication-dose/weight-dosage 等 40 页）、tools/medical/dosage-calculator 系、tools/healthcare/（parkland/ibw 等）、tools/clinical-nursing/ 输液类（~40 页合计）

## 进度
- 🟡 进行中（2026-10-26 批次 03-2）：其余代表页待铺开
  - `health/child-medication-dose`：新增「同年龄参考体重（WHO 生长标准 P50，0–18 岁男/女）」+ 输入值与中位体重偏差百分比；
    新增「肝肾功能减量提示」（两 select：肾功能 Ccr 四级 / 肝功能 Child-Pugh 四级），8 种药标注主要清除途径（肝/肾/局部肠道），
    药物参考表新增「主要清除途径」列。
  - `medical/dosage-calculator`：同样两套能力接入；儿童（≤18 岁）显示参考体重核对并**偏差 >40% 时红字提示核对单位（kg/斤）**；
    15 种药按清除途径给出肝/肾分级减量建议（阿莫西林/头孢氨苄/万古霉素→肾，对乙酰氨基酚/布洛芬/苯妥英钠等→肝，头孢曲松/环磷酰胺→肝+肾）。
  - 数据源：WHO weight-for-age P50（0–18 岁）；清除途径按各药说明书主要消除途径归类，提示文案统一附「以说明书与药师核定为准」。
- 🔴 待续：剩余剂量页（clinical-nursing 输液类等）按同一模板铺开——已扫：clinical-nursing 输液类页无年龄输入（评分/操作型为主），
  health/healthcare/medical/pediatrics 含「年龄+剂量」且未铺 WHO 中位体重的页仅剩 `health/body-surface-area`（非剂量页），
  「同年龄参考体重」模板可铺页已全部铺完（03-2/47/48 三批）；
  「药品库 json 化（散在页内 JS → 集中 json）」涉及 40 页大重构且 fetch json 在 verify harness 不可达，暂缓待裁。

## 2026-11-03 审计补充

### 覆盖
- 本轮人工阅读 1 页 `tools/health/insulin-dose.html`；医疗其他页面未逐页审计，未运行页面与门禁。

## 2026-11-03 续查（并行批 J）

> 范围：本轮人工阅读 8 个用药/剂量类页面（`tools/medical` 5 页、`tools/healthcare` 2 页、`tools/clinical-nursing` 1 页）。全部结论来自源码静态阅读 + node 内存复算，未开浏览器、未验证英文态/移动端/门禁。涉及临床剂量的条目均需药师/医师复核。

### 留存优化
- 统一“无效输入→清空结果/标记过期”的交互模式：D-N1 等问题建议使用一致的输入检查。
- `tools/medical/dosage-calculator.html:533-554` 的复制结果未包含肝/肾功能减量提示，复制进病历会丢失关键警示；建议复制全文或附警示行。
- `tools/medical/calculator-calc-2.html:352-383` 历史记录只存 name/weight，回放不恢复 age/tier/freq，记录摘要与实际重算可能不一致；建议存全量参数。
- `tools/medical/calculator-calc-infusion.html:368-373` 历史不存 conc/体重，回放结果可能与记录摘要不同；建议存 conc/w。
- `tools/medical/drug-info.html:454` 药物明细用原字符串拼 innerHTML，未转义；当前静态数据无风险，数据外置/用户可编辑时需 `escapeHtml`。
- 药品剂量数据仍散在各页 JS（承接上文 03-2 待裁）；若集中 json，需保留内联兜底以适配 verify harness 不可 fetch 的限制。

### 续查覆盖
- 已读 8 页：`tools/medical/dosage-calculator.html`、`tools/medical/calculator-calc-2.html`、`tools/medical/calculator-calc-infusion.html`、`tools/medical/convert-time-infusion.html`、`tools/medical/drug-info.html`、`tools/healthcare/healthcare.html`、`tools/healthcare/parkland.html`、`tools/clinical-nursing/iv-drip-rate.html`。
- 取证方式：源码逐行阅读 + node 内存复算（复刻页面公式与 `toFixed` 口径），未运行浏览器、未验证英文态/移动端/门禁，未做线上核对。
- 未覆盖：`tools/healthcare/healthcare-2.html`（输液滴速）等同类页未读；药品剂量数值本身的医学正确性未逐条核对，D-N2/D-N5/D-N7/D-N9 的阈值与口径需药师/医师复核。
- 与既有条目关系：D-N1（结果过期）、03-2（剂量数据 json 化）仍有效；本轮新增均为不同页面/不同成因，未与 D-N1 重号。

## 2026-11-04 续查（并行批 L）

> 范围：本轮人工阅读 8 个用药/剂量/给药类页面（`tools/healthcare` 4 页、`tools/clinical-nursing` 3 页、`tools/medical` 1 页）：`tools/healthcare/bsa-calculator.html`、`tools/healthcare/egfr-calculator.html`、`tools/healthcare/egfr.html`、`tools/healthcare/ibw.html`、`tools/clinical-nursing/cvc-maintenance.html`、`tools/clinical-nursing/bag-valve-mask.html`、`tools/clinical-nursing/gastric-tube-depth.html`、`tools/medical/convert-glucose.html`。仅源码逐行阅读 + node 内存复算（复刻页面表达式与 `toFixed`/`Math.round` 口径），未开浏览器、未验证英文态/移动端/门禁。临床剂量与阈值条目均需药师/医师复核。

### 留存优化
- D-N25 与 D-N31 同属「公式版本/引据与实现不一致」：建议在结果区固定输出「所用公式 + 版本 + 单位」，避免同站多页各写一套出处。
- D-N28/D-N30 同属「输入校验或公式适用范围」问题：建议统一输入守卫模式（范围 + 单位 + 越界红字），与 D-N1/D-N24 的「无效输入清空结果」一并抽公共逻辑。
- D-N27 的 EMR 文案（`cvc-maintenance.html:381`）是硬编码的透析 1000 U/mL，与实际计算脱钩；建议 EMR 只引用计算结果对象，禁止再写静态浓度。
- 本轮未核对药典/指南数值本身的医学正确性（如 BVM 频率、胃管公式、透析封管浓度），D-N26/D-N27 的具体阈值需药师/医师复核。

- 本轮实读 8 页：`tools/healthcare/bsa-calculator.html`、`tools/healthcare/egfr-calculator.html`、`tools/healthcare/egfr.html`、`tools/healthcare/ibw.html`、`tools/clinical-nursing/cvc-maintenance.html`、`tools/clinical-nursing/bag-valve-mask.html`、`tools/clinical-nursing/gastric-tube-depth.html`、`tools/medical/convert-glucose.html`。
- 新增 8 条（高 3、中 4、低 1）：D-N25~D-N32。最高优为 D-N25（race=0 → eGFR 0/CKD 5）、D-N26（胃管身高法 77 cm/34 cm）、D-N27（透析导管生理盐水封管、肝素 0）。
- 未覆盖：`tools/healthcare` 的 `healthcare-4` / `healthcare-5` / `map` / `qtc` 与 `tools/clinical-nursing` 的 `suction-pressure` / `chest-compression-depth` / `cvc-maintenance` 之外的管路页未读；英文态、移动端、verify 与门禁未验证。
- 与既有条目关系：D-N1/D-N24 的「无效输入沿用旧值」与本轮 D-N28/D-N32 的无守卫同类但页面不同，未重号。

## 2026-11-04 续查（并行批 M）

> 范围：本轮人工阅读 8 个用药/剂量/给药/监护类页面（`tools/healthcare` 4 页、`tools/clinical-nursing` 3 页、`tools/medical` 1 页）：`tools/healthcare/qtc.html`、`tools/healthcare/map.html`、`tools/healthcare/ideal-weight.html`、`tools/healthcare/healthcare-5.html`、`tools/clinical-nursing/suction-pressure.html`、`tools/clinical-nursing/chest-compression-depth.html`、`tools/clinical-nursing/restraint-duration.html`、`tools/medical/clinical-tools.html`。仅源码逐行阅读 + node 内存复算（复刻页面表达式与 `toFixed`/`Math.round`/`parseInt` 口径），未开浏览器、未验证英文态/移动端/门禁。临床剂量与阈值条目均需药师/医师复核。

### 留存优化
- D-N40 涉及「实现与页内引据/简介不一致」：建议结果区固定输出「所用公式 + 版本 + 单位 + 是否已按指南限幅」，避免同一页自相矛盾。
- D-N34/D-N36/D-N37 同属「无输入守卫 + 0/越界值仍出一等结果」：与 D-N1/D-N24/D-N28 同源；建议抽公共 guard（范围 + 必填 + 越界红字 + 无效清空），一次性覆盖本类页面。
- D-N39 与 D-N38 的排程/示意问题属「派生量未单一来源」：建议时间点只由公式派生、示意图只由最终数值派生，避免中间量二次叠加。
- 本轮未核对指南数值本身的医学正确性（吸痰负压、按压深度、约束松解周期、MELD 阈值），D-N37/D-N38/D-N39/D-N40/D-N41 的具体阈值需药师/医师复核。

- 本轮实读 8 页：`tools/healthcare/qtc.html`、`tools/healthcare/map.html`、`tools/healthcare/ideal-weight.html`、`tools/healthcare/healthcare-5.html`、`tools/clinical-nursing/suction-pressure.html`、`tools/clinical-nursing/chest-compression-depth.html`、`tools/clinical-nursing/restraint-duration.html`、`tools/medical/clinical-tools.html`。
- 新增 9 条（高 2、中 7、低 0）：D-N33~D-N41。最高优为 D-N37（成人吸痰 150–200 与引据 80–120 矛盾、默认 150 判安全）、D-N40（MELD 系数错位 + 6 分下限 + MELD-Na 查表偏差）。
- 未覆盖：`tools/healthcare` 的 `healthcare-4`（NYHA）、`chads-vasc`、`nrs2002`、`wells`、`resp-rate`、`water-intake`、`bac-calculator` 与 `tools/clinical-nursing` 的 `tracheostomy-dressing`、`ostomy-bag-timing`、`restraint-check`、`fall-emergency-flow`、`surgical-position-risk`、`assessor-*` 未读；英文态、移动端、verify 与门禁未验证。
- 与既有条目关系：D-N28（`ibw.html`）与本轮 D-N35 同为理想体重/无守卫，页面不同、D-N35 另含性别回退与年龄死字段；D-N31（eGFR 公式/引据不一致）与本轮 D-N40 同源模式、页面不同；D-N1/D-N24/D-N28 的「无效输入仍出结果」与本轮 D-N34/D-N36 同类但页面不同。未与 D-N1~D-N32 重号。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 个用药/剂量/给药/监护类页面（`tools/healthcare` 3 页、`tools/clinical-nursing` 4 页、`tools/medical` 1 页）：`tools/medical/reminder-2.html`、`tools/healthcare/nrs2002.html`、`tools/clinical-nursing/tracheostomy-dressing.html`、`tools/clinical-nursing/ostomy-bag-timing.html`、`tools/healthcare/resp-rate.html`、`tools/healthcare/blood-pressure-grade.html`、`tools/clinical-nursing/generator-pressure.html`、`tools/healthcare/healthcare-4.html`。仅源码逐行阅读 + node 内存复算（复刻页面表达式与 `toFixed`/`Math.round`/`parseInt` 口径），未开浏览器、未验证英文态/移动端/门禁。临床剂量与阈值条目均需药师/医师复核。

### 留存优化
- D-N42/D-N48 同属「展示档位与代码分档不一致」：建议把档位名称、阈值、统计口径集中到单一配置，页面文案、图例、筛选与统计全部由该配置派生。
- D-N44/D-N45/D-N47/D-N50 同属「无效或自相矛盾的输入仍输出一等结果」：与 D-N1/D-N24/D-N28/D-N34/D-N36 同源；建议抽公共 guard（必填 + 范围 + 互斥校验 + 无效清空），一次覆盖本类评估页。
- D-N43/D-N44 是同一页的量表语义与输入口径问题：若短期不改结构，至少先把三个营养条目改成 0–3 下拉并在 label 写明「分值」，可同时消除「相加」和「填实测值」两类误用。
- D-N45/D-N46 同属「同一页多套时间/间隔表」：建议间隔、次数、预警点只保留一个数据源，公式框、信息框、深度解析与代码全部引用它，避免再次漂移。
- 本轮未核对量表/指南数值本身的医学正确性（NRS2002 条目阈值、气切换药频次、造口更换周期、年龄分段呼吸频率、血压分级阈值、NYHA 定义），D-N43/D-N45/D-N46/D-N47/D-N48/D-N50 的具体阈值需药师/医师复核。

- 本轮实读 8 页：`tools/medical/reminder-2.html`、`tools/healthcare/nrs2002.html`、`tools/clinical-nursing/tracheostomy-dressing.html`、`tools/clinical-nursing/ostomy-bag-timing.html`、`tools/healthcare/resp-rate.html`、`tools/healthcare/blood-pressure-grade.html`、`tools/clinical-nursing/generator-pressure.html`、`tools/healthcare/healthcare-4.html`。
- 新增 9 条（高 2、中 7、低 0）：D-N42~D-N50。最高优为 D-N43（NRS2002 三项相加、满分 13 与量表 7 分不符）、D-N48（默认 120/80 判「3 等级」、五档与三级制整体错位）。
- 未覆盖：`tools/healthcare` 的 `wells`、`chads-vasc`、`water-intake`、`bac-calculator` 等其余评分/生活页，`tools/clinical-nursing` 的 `restraint-check`、`fall-emergency-flow`、`surgical-position-risk`、`assessor-*`、`cold-compress-timer`、`reminder-time-1` 未读；英文态、移动端、verify 与门禁未验证。
- 与既有条目关系：`convert-flow-concentration.html` 已在 D-N18 覆盖（反推无上限、装置宣称未实现），本轮不重复；D-N34（`map.html`）与本轮 D-N48 都出现「负脉压」，但页面不同、D-N48 另含五档编号与图例错位；D-N1/D-N24/D-N28/D-N34/D-N36 的「无效输入仍出结果」与本轮 D-N44/D-N47/D-N50 同类但页面不同。未与 D-N1~D-N41 重号。

## 2026-11-04 续查（并行批 O）

> 范围：本轮人工阅读 8 个监护/护理流程与医疗计算页（`tools/clinical-nursing` 5 页、`tools/medical` 3 页）：`fall-emergency-flow.html`、`restraint-check.html`、`surgical-position-risk.html`、`assessor-pressure-risk.html`、`cold-compress-timer.html`、`calc-34.html`、`estimate-metabolism.html`、`calculator-calc-due-date.html`。仅源码逐行阅读 + `node -e` 内存复算（复刻页面表达式、`Math.round`/`toFixed`/`parseInt` 与本地时区日期口径），未开浏览器、未验证英文态/移动端/门禁。医学阈值与剂量条目只判断实现与页内文案是否一致，具体数值需药师/医师复核。

### 留存/优势（按页）
- 跌倒应急流程：8 步闭环 + 场景预设 + 计时 + 历史/CSV/EMR，适合作为科室演练与交接模板；建议把「完成步骤索引 + 每步时间戳」纳入历史与导出，形成可复盘的时间轴。
- 约束带检查：按约束部位拆分清单、带 EMR 与历史，结构清晰；建议把检查项改为真实 checkbox 并把勾选数组纳入历史，同时让「复制结果」列出未确认项。
- 手术体位压力点：固定的体位-压力点-措施库 + 矩阵/CSV/复制，适合术前体位核对；建议补时长输入与 >4h 上调，或删掉未实现的时长宣称，并为英文态补数据层。
- 术中压力性损伤评估：体位基础分 + 时长/BMI/年龄/合并症加权 + 预设，方向正确；建议加输入守卫、输出分项构成表，并与手术体位页共用同一风险算法。
- 冷敷计时器：部位×敏感度系数 + 计时 + 预设 + EMR，临床场景贴合；建议改为时间戳倒计时、历史记录部位+敏感度+计时状态，并把皮肤观察做成可勾选日志。
- 每日热量需求（RER）：BMR/TDEE/BMI/三大营养素与历史一屏呈现，计算路径清楚；建议补人类文献引据、缺口上限校验，并把历史保存改为防抖/失焦触发。
- 静息代谢率：三公式并列 + 条形对比 + 预设，便于方法学对照；建议修正百分比、校验体脂率、动态标注参与公式，并显示各公式权重。
- 预产期：LMP/受孕/IVF 三模式 + 里程碑 + 预设，覆盖常见临床路径；建议周期校正只用于 LMP、统一本地日期解析、补未来日期校验与里程碑排序。

- 本轮实读 8 页：`tools/clinical-nursing/fall-emergency-flow.html`、`restraint-check.html`、`surgical-position-risk.html`、`assessor-pressure-risk.html`、`cold-compress-timer.html`、`tools/medical/calc-34.html`、`estimate-metabolism.html`、`calculator-calc-due-date.html`。
- 新增 30 条（高 5、中 15、低 10）：D-N51~D-N80。高优为 D-N54（约束带 EMR 未确认项错位）、D-N68（人体热量页嵌兽医引据）、D-N69（500 kcal 缺口上限未实现）、D-N72（kcal 差值当百分比）、D-N76（受孕/IVF 误用周期校正）。
- 未覆盖：本批 8 页之外的 `tools/clinical-nursing` 其余流程页、`tools/medical` 其余计算页未读；英文态、移动端、verify 脚本与门禁均未验证；D-N60/D-N65/D-N80 分别标注「待验证/待临床复核」。
- 与既有条目关系：D-N51/D-N52 属跌倒流程页，未与 D-N31~D-N50 的急诊/监护条目重号；D-N62 的「无守卫仍出结果」与 D-N1/D-N24/D-N28/D-N34/D-N36/D-N44 同源但页面不同；D-N68/D-N72/D-N76 为新增计算/日期类页面，未与 D-N25~D-N41 的公式/引据条目重复。

## 2026-11-04 续查（并行批 P）

- 范围：只读实读 8 页（clinical-lab 2、cardiology 3、pulmonology 3），完整阅读 HTML、内联 JS、公式框、深度解析与 FAQ。本轮未改代码、未跑构建、未做 git 写、未在仓库建临时文件、未开浏览器。
- 口径：医学阈值仅核对「页面声明 vs 代码实现」是否一致，不裁决临床正确性；凡涉及分型/分级/阈值均需临床复核。
- 编号：接续 D-N80，从 D-N81 起；落盘前已确认文件当前最大号为 D-N80。

### 留存/优势（按页）
- 生化比值：AST/ALT、BUN/Cr、GGT/ALT、R 因子、UA/ALB 五项各有独立结果卡与参考标尺，结构清楚；建议先让简介/深析与这五项对齐，再决定是否新增 AG/A/G 工具。
- PCR Ct 判读：定性/定量/质控/标准曲线四块齐全，预设与 CSV 导出完整；建议按「阴性→不出定量值」门控输出，并让历史保存定量结论与标准点。
- 主动脉夹层：范围单选 + 风险因素 + 策略卡，急诊分型路径清楚；建议给 radio 补 id 并入历史，并统一 DeBakey 映射。
- Holter：Lown 分级 + 负荷 + 预设 + 图表，覆盖较完整；建议用总数/实际总心搏共同判频发，并补总心搏输入。
- 心包积液：五档分级 + 填塞征象 + 处理建议，临床路径完整；建议统一五档口径并修正预设深度。
- GINA/ACT：GINA 四问 + ACT 五题双量表，结构好；建议统一 ACT 三档判读并把 ACT 纳入历史/导出。
- Lung-RADS：类型×大小×生长/恶性/新发 + 随访建议，框架完整；建议补实性成分输入，修正 15mm/6mm 边界与元数据分类。
- STOP-BANG：8 项 + 分层 + 标尺 + 历史/CSV，简洁易用；建议性别改为显式必选，并补预设或移除空预设页签。

- 本轮实读 8 页：`tools/clinical-lab/biochemistry-ratio.html`、`tools/clinical-lab/pcr-ct-interpretation.html`、`tools/cardiology/aortic-dissection.html`、`tools/cardiology/holter-grading.html`、`tools/cardiology/pericardial-effusion.html`、`tools/pulmonology/gina-asthma.html`、`tools/pulmonology/lung-rads.html`、`tools/pulmonology/stop-bang.html`。
- 新增 34 条（高 2、中 23、低 9）：D-N81~D-N114。高优为 D-N85（PCR Ct=0 阴性仍输出 1.10e+12 拷贝/ΔCt）、D-N107（Lung-RADS 部分实性 ≥15mm 永不 4B）。
- 未覆盖：本批 8 页之外的 clinical-lab/cardiology/pulmonology 其余页面未读；英文态、移动端、浏览器实机、verify 脚本与全部门禁均未验证；医学阈值只做「页面声明 vs 实现」一致性核对，D-N81/D-N91/D-N98/D-N99/D-N101/D-N104/D-N105/D-N107/D-N108/D-N109/D-N110/D-N113 等涉及分型/分级/阈值处均需临床复核。

## T 批 clinical-nursing 覆盖（2026-11-04）
- 本轮审计 8 页：`tools/clinical-nursing/morse-score.html`、`braden-score.html`、`barthel-index.html`、`pain-nrs.html`、`calc-rater-risk.html`、`assessor-rater-risk.html`、`pressure-injury-description.html`、`reminder-time-1.html`。
- 新增 11 条（高 10 / 中 1），编号 D-N115–D-N125，沿用本文件 D-N 前缀；假工具候选 0 页（8 页均有真实评分/生成/计时实现）。
- 未做浏览器/门禁/线上验证；医学阈值仅做「页面声明 vs 实现」一致性核对，分级界值需临床复核。
