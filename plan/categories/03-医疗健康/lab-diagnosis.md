# 医疗 · 检验与诊断类（clinical-lab/cardiology 检验/血气等 ~80 页）

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
  - 形态纪律：SVG 标尺只做增强，**必须同时输出一段「参考区间定位」文本到 `#result`**（门禁可断言 + 无障碍），且文本走 `__T(en,zh)` 双语 helper。
- 🔴 待续：批量解读可向生化/免疫面板推广（需各页自有参考表）；
  thyroid-function-model 页面级 EN i18n（8 pattern 全串）单独批治理。

## 2026-11-03 续查：血气、便潜血、MIC 折点与 INR

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
- **L-N4 未完全修复（2026-11-06 复核，重新待处理）**：先前修复记录称示例和数据均为 S≤0.5、R≥4；当前 `mic-breakpoint.html:191` 仍如此写，但 `:256` 的革兰阴性菌左氧氟沙星实际是 S≤0.5、R≥2，MIC 2 会判 R，示例折点与数据再次冲突。此外示例 MIC 0.06 被 `:319-325` 的二倍稀释系列校验拒绝，无法按示例判 S。需由专业人员核实标准版本及折点后统一数据、示例和输入校验，勿仅凭历史记录改临床阈值。
- 中文/英文 i18n 字典同步更新；`_build.py` 通过（SW 戳 `6898340262`），`run_gates.py` 218/218，`verify_clinical-lab_calc.js` 88/88。
- 提交：`15892e31c7`；本段门禁数字及后续待办状态均为当时记录。2026-11-06 本轮运行 `node scripts/verify_clinical-lab_calc.js` 148/148，通过的是 Node 桩用例，未验证真实浏览器或线上；L-N4 仍待处理，其他条目不在本轮复核范围。

## 2026-11-03 续查（并行批 F）

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

### 829 批核销记录（2026-11-16）

- 核销 L-N27–L-N30（流式细胞术 CD4/CD8 比值）共 4 条：页面已改为「未填写指标不参与判读」。
- L-N27：`ratioValid = cd4>0 && cd8>0`，无效时比值显示「—」并提示补全，不再推入倒置 flag。
- L-N28：WBC/淋巴百分比缺失时整块拦截，AIDS 分期提示改为「仅 HIV 阳性者」条件表述。
- L-N29：Treg 已参与计算（绝对计数 + 占 CD4%），NK/CD4%/CD8% 增加双向 flag；「全部在参考范围内」仅在全部亚群均填写时出现。
- L-N30：CD4 450/μL 统一为「参考下限内(414–500)」，不再另判「免疫抑制」。
- 门禁新增 4 例，`node scripts/verify_clinical-lab_calc.js` 161/161。

### 830 批核销记录（2026-11-16）

- 核销 L-N31（文案承诺）、L-N32（趋势图）、L-N33（重复相关工具）、L-N34（虫卵尺寸反序）共 4 条。
- L-N31：简介已改为「输入白细胞、淋巴细胞百分比与各亚群百分比，自动换算绝对计数」，不再宣称可直接录入绝对计数。
- L-N32：趋势图改读历史记录的 `cd4`/`cd8` 反算比值，不再 `parseFloat` 结果文本；门禁注入两条历史断言折线 `[1.5,0.5]`。
- L-N33：相关工具中 `blood-gas-analysis.html` 仅剩一张卡片。
- L-N34：短膜壳绦虫卵尺寸改为 `37-47 μm`，门禁断言 `EGGS` 数据。
- 门禁：`node scripts/verify_clinical-lab_calc.js` 163/163（新增 2 例）。

### 831 批核销记录（2026-11-16）

- 核销 L-N35：搜索已覆盖 `name/desc/shape/color/shell/operculum/content` 并对 `size` 做数值区间匹配（`parseSizeRange` + `matchSizeQuery`，支持 `70-106`、单值、μm/um/微米后缀）；卡片显示「命中：…」字段。
- 门禁：输入 `70-106` 命中日本血吸虫卵（仅 size 字段可匹配）、输入「卵盖」命中卵盖字段条目 ⇒ `PGE size=Y operc=Y`。
- `node scripts/verify_clinical-lab_calc.js`：164/164。

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

### 832 批核销记录（2026-11-16）

- 核销 L-N36–L-N41 共 6 条；其中 L-N40 为代码修复（`setInterp` 支持 highText），其余为复核核销。
- L-N36：图表已改用 `currentList`，筛选后饼图同步；页面与深解已移除「图谱复习」等含图承诺，`.egg-svg` 死样式不再被引用。
- L-N37：尿沉渣 `filterItems` 覆盖 name/sig/morph/size/bg/mean 六字段；尺寸查询「7-8」命中 1 项。
- L-N38：首屏由 `tabify()` 直接调用 `__urineDrawChart()`，数据源 `__urineList` 初始化为全量 ITEMS，不再空白等待二次输入。
- L-N39：精液八项空值/越界整块拦截，不再按 0 判「少精症 + 弱精症」。
- L-N40：`setInterp(id,ok,lowText,highText)` 原实现丢弃 `highText`，IM 偏高显示反方向「↓ 偏低」；改为 `lowText||highText||'↓ 偏低'`，总活力 35%/IM 65% 现显示「↑ 不动精子比例偏高(总活力不足40%)」。
- L-N41：精液页公式与引据表统一为 WHO 第 5 版（2010），并注明第 6 版（2021）数值差异。
- 门禁新增 3 例（尿沉渣尺寸检索、精液空值、IM 偏高提示），`node scripts/verify_clinical-lab_calc.js` 167/167。

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

### 833 批核销记录（2026-11-16）

- 核销 L-N42、L-N43 并修复 L-N44。
- L-N42：空态守卫（`tsh==null||ft3==null||ft4==null` → 提示补全核心三项并清空标尺）已在分型前拦截；单侧升高已有「甲状腺激素升高（需鉴别）」分支。门禁新增两例：TSH 8 + FT3/FT4 空 ⇒ 补全提示；TSH 2.0 + FT3 10 ⇒ 需鉴别。
- L-N43：同一守卫在缺项时重写 `#result` 并清空 `thy_*Bar`，不再保留上一次结论。
- L-N44：公式框内 `formula-title` 移至 `formula-eq` 之前，与同批页面版式一致（本批代码修复）。
- 门禁：`node scripts/verify_clinical-lab_calc.js` 169/169。

## T 批 消化内科 覆盖（2026-11-04）

### 827 批核销记录（2026-11-16）

- 核销 L-N45–L-N58 共 14 条：本轮逐页复核 `tools/gastroenterology/` 下 8 页，均已在页面内修复，本次仅补门禁并核销状态。
- Child-Pugh（L-N45/L-N46）：空值走 `missing` 分支停止评分；腹水/脑病下拉改「请选择…」空值默认；新增 PBC 复选框切换 68/170 胆红素分档。
- Glasgow（L-N47/L-N48/L-N49）：九项空值统一「未填 → 不计分」并列出缺项；refBar 改 `<3 轻症 / 3–6 重症 / ≥6 危重` 三带；引据表与正文统一为 9 项含 AST。
- CDAI（L-N50/L-N51）：Hct 空值拦截、20–60% 校验；Hct 标准值改为 Best 1976 的男 47/女 42。
- SAAG（L-N52）：任一空值不出结论；0–60 g/L 与「腹水 ≤ 血清」校验，异常显式报错。
- 肝性脑病（L-N53）：拆分「无临床 HE」与「MHE 需专项测试阳性」，新增 `mheTest` 下拉；扑翼样震颤「消失」与意识等级不一致时剔除该项。
- 胆红素（L-N54/L-N55/L-N56）：两值必填、DBIL 上限参与判断、DBIL>TBIL 显式报错停止计算。
- Mayo（L-N57）：临床缓解改为「总分 ≤2 且便次 ≤1 且无便血」，总分达标但单项活动输出「未达临床缓解（单项活动）」。
- HP 耐药（L-N58）：统一 `blocked` 禁用集（青霉素过敏→阿莫西林；耐药→对应药物），方案池逐条过滤，无可用方案时明确提示。
- 门禁（827 批新增 15 例）：`node scripts/verify_gastroenterology_calc.js` 53/53。

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
