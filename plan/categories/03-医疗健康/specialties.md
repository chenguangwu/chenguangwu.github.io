# 医疗 · 专科计算类（ent/dermatology/obstetrics/pediatrics/ophthalmology/urology 等 ~120 页）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

## 2026-11-06 结石成分静态续审（清单 649）

- `tools/urology/stone-composition.html:243-252,286-320`：成分筛选、搜索及选择卡片均有代码路径；Brushite 条目列“酸性尿”成因和“碱化尿液”预防，与磷酸钙结石管理可能冲突，须泌尿科专业人员依据现行指南核验，不据此自行改变尿液 pH 或用药。未运行页面，其他药物和阈值未做专业核验。

## 2026-11-06 中药工具静态续审（清单 630–633）

- `tools/tcm-pharmacy/formula-song.html`：缺必填项时只 toast、保留上次生成结果——第1328批已修（generateSong 两处缺必填分支均清 result.innerHTML，源码形态强锚 `FSONGCLR` 已落 tcm-pharmacy verify；旧版段内引用 before=2/fixed=4，旧版无 ⇒ BAD）。原药材输入未转义注入路径已于第 951 批修复并真机验证。余项：方歌生成质量与方剂内容未做专业核验。
- `tools/tcm-pharmacy/four-qi-nature.html:358-372,383-425,440-443`：畏寒对应 `qi:'热'`，计分只处理寒、温两种，单选畏寒时总分为 0，算法误判“寒热不显”且评分百分比为 NaN。症状到药性推荐和代表药须临床专业复核。
- `tools/tcm-pharmacy/herb-quality.html`：切标签只切 class、内联 display 未解除致两区同显——第1327批已修（switchTab 同步设 tab-standard/tab-score 的内联 display，源码形态强锚 `HQTAB` 已落 tcm-pharmacy verify；旧版无 ⇒ BAD）。余项：滑块变化也不清理已生成评分；评分阈值与“符合药典标准、可入药使用”须专业复核。
- `tools/tcm-pharmacy/tcm-pharmacoeconomics.html`：按最低日费用给出“最经济方案”和“性价比”，没有疗效或等效性数据，且不同疗程时最低日费未必对应最低总费用。费用/药物比较须临床专业复核，未运行页面。（原 CSV 隐藏表未转义注入路径已于第 951 批修复并真机验证，从待办删除。）

## 2026-11-06 中医问诊工具静态续审（清单 626–629）

- `tools/tcm-diagnosis/disease-tracking.html`：未填写症状也可保存总分 0 并标「无症状」；不同记录填写的症状集合不同时仍直接比较总分给出好转/加重判断。（原症状/舌象/脉象/日期未经转义拼入时间线、趋势、汇总和导出 HTML 的注入路径已于第 951 批修复并真机验证，从待办删除。）
- `tools/tcm-diagnosis/formula-matching.html`：天麻钩藤饮 `用法` 字段错配致详情用法为空——第1320批已修（数据对象 `用法`→`usage`，强锚 `FMUSAGE` 源码哨兵已落 tcm-diagnosis verify；旧版无该 `usage` ⇒ BAD）。余项：方剂内容及禁忌未做专业核验。
- `tools/tcm-diagnosis/ten-questions.html`：重置未重置性别下拉——第1321批已修（resetForm 显式设 pGender='男'，源码形态强锚 `TQRESET` 已落 tcm-diagnosis verify；旧版无该重置 ⇒ BAD）。余项：改动输入后 300ms 静默生成完整记录；重置只改 DOM，不代表清除了通用输入持久化，隐私状态待验证。
- `tools/tcm-diagnosis/treatment-principle.html:371-437,474-490`：选择项触发建议，全部未选则隐藏并拒绝导出；参考方药与治则映射可直接呈现具体治疗建议，须临床专业核验，不能据静态检查判医疗正确。四页均未运行浏览器。

## 2026-11-06 儿童疫苗排程静态续审

- `tools/pediatrics/vaccine-schedule.html`：清空出生日期只更新清单、主结果保留旧年龄——第1329批已修（!birthDate 分支补清 #result，源码形态强锚 `VACCLR` 已落 pediatrics verify；旧版分支段 getElementById( 引用 2/fixed 3，旧版无 ⇒ BAD）。余项：已接种至 0 月龄被 `||-1` 当成未填写；"逾期/当前应接种"月龄口径与页面说明不一致、导出不含接种状态、未来出生日期未拒绝——均涉疫苗排期与月龄口径须临床复核。
- `:266-272,371-372`：固定排程及“缺几针补几针”建议未本次核对最新免疫规划、适龄范围或补种个体条件；应由预防接种专业人员核验，不以静态检查替代医学判断。

## 2026-11-06 视光工具静态续审（第四批）

> 六页仅静态分析，未运行页面或验证视光标准；专业建议须复核。

- `tools/optical/photochromic-lens.html`：温度无下界致 `tempFactorDark` 为负、变深时间出现负秒——第1320批已修（因子非正即双语提示并中止，不做武断的下限钳制，真机负温用例已落 optical verify；旧版输出负时间 ⇒ BAD）。余项：清空温度仍按 25°C 输出结论；经验模型与适用温度范围须专业复核。
- `tools/optical/polarized-axis.html`：球镜/柱镜/前倾角/面弯空值静默按 0——第1317批已修（四处原始判空+非有限数与角度范围守卫，强锚 `PAGUARD` 已落 optical verify；旧版无 `__sphRaw` ⇒ BAD）。余项：模型与处方补偿方法须专业复核（原轴位已按「仅对照显示」处理，不参与诱导柱镜合成）。
- `tools/optical/polarized-stress.html:314-327,361-369`：表格色序数组相对 `COLORS` 索引错位：一级红（索引 4）标一级、二级紫（索引 5）也标一级，二级红（索引 9）标二级但三级紫（索引 10）标二级；末项高级粉白被标三级。等级及合格判断须专业复核。
- `tools/optical/prism-decentration.html:126-153,316-322,325-366`：切换“已知移心”后下拉仍标“基底方向”，代码却把该值当移心方向，再对负镜取反作为基底；同一选项语义随模式变化，易误填。棱镜量或移心量清空当作 0，仍输出结果；0 镜度被一律拒绝，包含只求诱导量模式。方向与临床适用性须复核。
- `tools/optical/progressive-corridor.html`：下加光/镜圈高度/瞳高空值静默代入——第1316批已修（三处原始判空+下加光非负、镜圈高度与瞳高正数守卫，强锚 `PCGUARD` 已落 optical verify；旧版无 `__addRaw` ⇒ BAD）。余项：图示中 `nearY-fitY` 为负，连接线使用负 CSS 高度，绘制效果待验证；通道策略与图示须视光师复核。
- `tools/optical/tinted-lens.html`：基础透光率清空/0 回退 92%、未约束 0–100——第1314批已修（原始串判空+范围校验，无效清 tintGrid，强锚 `TINTVLT` 已落 optical verify）。余项：颜色系数及对夜间/驾驶使用的结论须按适用标准复核。

## 2026-11-06 视光工具静态续审（第三批）

> 八页仅源码推演，未运行浏览器或核验验光、光学标准；涉及专业结论须复核。

- `tools/optical/convergence-near-point.html`：瞳距空值按 0 计算——第1315批已修（原始串判空+正数守卫，强锚 `CNPGUARD` 已落 optical verify）。距离/瞳距无效未清参考表——第1328批已修（pd<=0 与 dist<=0 两守卫均清 #distTable tbody，源码形态强锚 `CNPTBL` 已落 optical verify；旧版 calc 段引用 before=1/fixed=3，旧版无 ⇒ BAD）。余项：PD=62mm/40cm 的每眼需求与双眼总量口径冲突须视光师复核。
- `tools/optical/frame-pupillary.html`：A/DBL/PD 清空按 0 出匹配建议——第1315批已修（三处原始判空+正数守卫，强锚 `FPGUARD` 已落 optical verify；ED 为 0 回退 A 属选填默认，保留）。余项：移心过大时一律建议更大 DBL 与自身公式方向冲突，须视光师复核。
- `tools/optical/frame-tilt.html`：倾角/瞳距/瞳高清空按 0——第1315批已修（原始串判空，pd 与瞳高正数守卫，倾角 0 仍合法，强锚 `FTGUARD` 已落 optical verify）。`shiftCm` 未展示英文简介所述棱镜效应且无镜度输入——第 131 批已补选填镜度并按 Prentice 输出 `|c×D|`，留空不改变原输出（用例已落 optical verify）。前倾光心移动与瞳高方向仍须专业复核。
- `tools/optical/lens-refractive-index.html`：度数/直径/中心厚度空值静默代入——第1316批已修（三处原始判空+直径与中心厚度正数守卫，强锚 `LRGUARD` 已落 optical verify；旧版无 `__pRaw` ⇒ BAD）。余项：正负镜均对度数取绝对值并用明确标注“负镜”的边厚公式，正镜也显示中心加差的边厚。厚度模型适用范围须专业复核。
- `tools/optical/peripheral-defocus.html`：中心/周边/偏心角空值静默按 0 或 20——第1317批已修（三处原始判空+偏心角正数守卫+无效时清 `vis` 示意图，强锚 `PDGUARD` 已落 optical verify；旧版无 `__centralRaw` ⇒ BAD）。RPD=0 主提示说信号微弱，方向卡和示意图却称远视性、促进眼轴增长——第 137 批已统一 ±0.5D 中性带（方向/图色/效能同口径，用例已落 optical verify）。离焦量和镜型直接映射具体防控百分比的临床有效性仍须专业复核。

## 2026-11-06 眼科与视光工具静态续审（第二批）

> 七页仅分析源码，未运行页面或做医学核验；医疗和验光解释须专业复核。

- `tools/ophthalmology/strabismus-angle.html`：历史恢复无参调用 `switchTab()` 抛错且不重算——第1334批已修（switchTab 无参分支安全重算 conv/hirsch/combine 并 return，源码形态强锚 `STRASHIST` 已落 ophthalmology verify；旧版无 ⇒ BAD）。页面称 1Δ 在 1 米偏移 1cm，但转换网格算 `pd*0.5`（20Δ 显示 10cm）；`pd2` 未参与；Hirschberg 说明 15Δ/mm 而运行用 7°/mm——第 133 批已修（偏移改为 `pd`、Hirschberg 改 `mm*15` 后经 PD 换算、`pd2` 补充偏移占比；强锚 `STRAMATH` 已落 ophthalmology verify）。医学换算和适用性仍须复核。
- `tools/ophthalmology/refraction-error.html`：单片或双镜任一数字清空即直接返回、旧处方仍显示——第1323批已修（calcSingle/calcCombine 空值分支清对应结果容器，源码形态强锚 `REFCLR` 已落 ophthalmology verify；旧版无 ⇒ BAD）。散光分类仅看轴位而不看柱镜正负，互为转置的处方可能被标成不同类别——第 135 批已修（正柱镜先转 90° 得到负柱镜轴再分类，并注明判定轴；用例已落 ophthalmology verify）。页内 180° 示例的 J0 算式与负号结果是否自洽仍须专业复核。
- `tools/ophthalmology/tear-breakup-time.html`：清空首次值未清参考标尺 `resultRefBar`——第1323批已修（清空分支同步清 `resultRefBar`，源码形态强锚 `TBUTCLR` 已落 ophthalmology verify；旧版无 ⇒ BAD）。10 秒在代码中为正常而表格/FAQ/图例写 >10 正常——第 130 批已统一为 ≥10（强锚 `TB10` 已落 ophthalmology verify）。干眼分级、用药建议和阈值仍须临床复核。
- `tools/ophthalmology/vision-screening-21.html`：清空历史不清趋势容器、旧图留存——第1326批已修（__vsClearHist 同步清 `#__vsTrend`，源码形态强锚 `VSCLR` 已落 ophthalmology verify；旧版无 ⇒ BAD）。所有未答题默认“从不”、可连点生成完整结论——第 128 批已修（频率下拉增加空占位，`recordCurrent` 未选齐左右眼即拦截并提示；运行时用例 `VSUNANS` 已落 ophthalmology verify）。问卷到近视度数、置信带与散光轴位的医学有效性无本次证据，须专业复核。
- `tools/ophthalmology/visual-field-analysis.html`：仅检查 NaN，VFI 越界/PSD 负值仍进分级——第1325批已修（要求 PSD≥0、VFI∈[0,100]，MD 负值按习惯保留，源码形态强锚 `VFIDOM` 已落 ophthalmology verify；旧版无 ⇒ BAD）。HAP 等医学分期及界限须专业复核。
- `tools/optical/accommodation-amplitude.html`：年龄清空经 `||0` 当成 0 岁继续出结果——第1318批已修（原始串判空+年龄正数守卫，强锚 `AAGUARD` 已落 optical verify；旧版无 `__ageRaw` ⇒ BAD）。非正参考调节幅度对应近点被写成固定 999cm——第 136 批已将负幅度夹到 0、近点显示 ∞（用例已落 optical verify）。深解的 30 岁数值及引据表公式与实际公式不一致，医学适用性仍须验光专业复核。实测调节值为选填，未动。
- `tools/optical/anti-fatigue-design.html`：基础模式空年龄默认 0、空或 0 工作距离默认 40cm——第1318批已修（年龄/距离/远用度数三处原始判空+年龄与距离正数守卫，远用度数允许 0 与负值，强锚 `AFGUARD` 已落 optical verify；旧版无 `__ageRaw` ⇒ BAD）。基础 ADD 先封顶 1D 使渐进片建议不可达——第 132 批已修（保留封顶前原始需求，`>1.00D` 提示改用渐进片；用例已落 optical verify）。余项：基础远用度数 `rx` 读取后未使用，进阶近距隐斜只展示不参与建议。所述验配方法、隐斜处理和建议须专业复核。

## 2026-11-06 眼科工具静态续审

> 八页仅源码分析；未进行浏览器、图形、下载或医学标准核验，医疗问题均需临床复核。

- 同页 `:717-729,698-706`：用户填写的 `ecRow` 原样存入记录，随后拼入 `innerHTML`，存在本地存储型 HTML/脚本注入路径；未实际执行载荷。
- `tools/ophthalmology/astigmatism-chart.html`：切换射线数后旧标记按索引错位——第1334批已修（标记存的是射线索引、角度=索引×(360/条数)，24↔36 切换后同索引角度全变；修复后切条数即清两眼 marked 并同步读数，源码形态强锚 `ASLINES` 已落 ophthalmology verify；旧版无 ⇒ BAD）。高亮扇区镜像与分步切眼不重绘——第 127 批已修（新增 `sectorCenterAngle` 统一射线角与 canvas 弧角，`goStep` 内补重绘；强锚 `ASANGLE`/`ASSTEP` 已落 ophthalmology verify）。余项：向量直接平均 180° 相反射线时会相互抵消仍输出数值轴位，视觉意义及轴位解释须临床核验。
- `tools/ophthalmology/amsler-grid-test.html`：切换眼别未清 `S.drawing` 致未完成绘制串眼——第1334批已修（amEye change 与 goStep 两处切眼别均补清 S.drawing/S.cursor，源码形态强锚 `AMDRAW` 已落 ophthalmology verify；旧版两处皆无 ⇒ BAD）。余项：提示可点“完成”闭合但工具栏未见完成按钮，实际只绑定双击或 Enter；保存只含已闭合标记，正在绘制的区域不入快照；触屏事件表现未实测。
- `tools/ophthalmology/axial-length.html`：仅检查 NaN，眼轴/声速为负或零仍参与运算（零声速致除零）——第1324批已修（calcCorr/calcSeg 两分支要求长度与声速均为正，源码形态强锚 `ALNEG` 已落 ophthalmology verify；旧版无 ⇒ BAD）。余项：接触压平校正从测量长度减 0.15 mm，与压平造成测值缩短的方向可能矛盾，IOL 输出符号与深解“下调”描述亦需核对。专业假设及公式须临床核验。
- `tools/ophthalmology/cd-ratio.html`：越界输入被静默夹到 0–1 而继续给分级；0.5 分级与综合风险口径矛盾——第 126 批已统一为 `<=0.5` 临界、`>0.5` 疑似，阈值表同步改 `> 0.5 ~ 0.7`（强锚用例已落 ophthalmology verify）。ISNT 解释及阈值仍须临床核验。
- `tools/ophthalmology/iop-correction.html`：清空必填时网格与公式区残留旧值——第1322批已修（`__tbInputGuard` 空值分支与越界分支一致，同步清 `grid`/`formulaList`，源码形态强锚 `IOPCLR` 已落 ophthalmology verify；旧版无 ⇒ BAD）。余项：各公式及临床适用性未核验。
- `tools/ophthalmology/oct-rnfl.html`：只拦 NaN，负厚度或负年龄也产生分级——第1324批已修（年龄与各项厚度须为正，源码形态强锚 `OCTNEG` 已落 ophthalmology verify；旧版无 ⇒ BAD）。界面写 `S>I>N>T`，实际判定为 `s>i-5 && i>n && n>t`——第 134 批已把可见文案统一为 `S>I−5 且 I>N>T` 并注明容差（用例已落 ophthalmology verify）。年龄模型与分级仍须专业核验。

## 2026-11-06 子宫内膜记录静态续审

- `tools/obstetrics/cycle-8.html`：“最新厚度”与临床解读先按周期天数取最大、图表跨周期混在一条曲线——第 129 批已修（最新按测量日期降序取，跨周期省略趋势线并提示，强锚 `CHLATEST` 已落 obstetrics verify）。仅源码推演，**需临床复核**。
- `tools/obstetrics/cycle-8.html:345-350,414-427,489-493`：仅凭固定周期日推定月经/增殖/排卵/分泌期并生成“正常范围”“警惕病变”解读，图表对所有日期统一显示 7–14mm；周期长度、实际排卵与临床背景未参与。是否适用及参考阈值须专业核验，不将静态模型视为医学结论。

## 功能缺陷
- 产科预产期页缺「孕周时间轴可视化」（周数条+当前周胎儿大小描述）。
- 眼科视力页缺 LogMAR/Snellen 分数互转表（部分有，未统一）。

## 优化点
- S2 场景：「孕 12 周建档日历」「宝宝 6 月龄辅食量」。
- 专科「随访计划」生成器：输入诊断日期→输出复查时间表（纯前端、高粘性）。

## 受影响范围
- tools/ent/、tools/dermatology/、tools/obstetrics/、tools/ophthalmology/、tools/urology/、tools/pulmonology/、tools/rheumatology/、tools/cosmetic-derm/、tools/forensic-medicine/（~120 页合计）

## 进度
- 🟢 长期增强（2026-11-21 复核：无缺陷项，转后续批次）：「宝宝 6 月龄辅食量」等其余 S2 场景；随访铺开候选余量视批次续接。

## 2026-11-06 健康工具静态复核

> 范围：`tools/health/{pregnancy-due-date,ovulation-calculator,gfr-calculator,blood-pressure-classifier}.html` 的输入事件、计算及结果路径；仅静态阅读和 Node 算式复算，未运行页面、检查浏览器或验证临床标准；医疗解释须专业人员复核。

### 清空输入仍保留旧医疗结果（高 · 部分修复余项）
- 已修：`gfr-calculator`（第1310批新增 `clearGfr()`，年龄/肌酐无效及 Cockcroft 缺体重均清 gfrVal/gfrStage/marker/statsGrid/wtInfo，强锚 `GFCLR` 已落 health verify）；`blood-pressure-classifier` 第1304批已补必填与舒>收校验并清空结果。
- 余项：`ovulation-calculator` 清空周期/经期仍保留旧结果；`pregnancy-due-date` 切换预产期方式且目标日期为空仍保留前一方式结果。两页涉周期预测/临床口径，需专业裁断后同步清理与提示，未擅改。
- 影响：当前输入不完整或方式已改变时仍可见旧结论。应同步清空结果、图示及相关导出，并给必填提示；代码审计不证明浏览器实际呈现，需后续交互验证。


## 2026-11-06 健康工具静态复核续批

> 实读 `health/{child-bmi-calculator,child-height-predictor,body-surface-area,cholesterol-ratio,calorie-needs}` 的主要计算与输入路径，仅源码和算式复算，未做浏览器或临床标准核验。

### 体表面积英制下的场景预设未换算（中，第1305批余项）
- `tools/health/body-surface-area.html`：切换时换算已有输入值已于第1305批修复（setUnit 按 2.54/0.453592 换算）；但场景预设注入固定公制值（如「成年男性」175cm/75kg），在英制模式下点击会当 175 in/75 lb 使用，仍错位。
- 建议让预设值按当前 unit 换算注入或预设按单位分组；明确显示单位与校验异常身高体重，涉及剂量计算需临床复核。

### 儿童身高预测选填项未参与结果（低，代码确认）
- `tools/health/child-height-predictor.html:195-202,483-506,521-543` 读取孩子年龄和当前身高，但主预测和百分位只使用父母身高、性别；两项仅供 CSV 导出。更改这两个字段不会影响显示的预测值，预设含这两项易让人误以为参与估算。
- 建议明确标为记录用途或删除无计算作用的输入；若要引入生长预测，先经专业审查。

## 2026-11-06 健康工具静态复核第三批

> 实读 `health/{alcohol-units,blood-sugar-converter,caffeine-limit,fracture-healing,ibw-calculator,protein-needs}` 的主要输入、计算和结果路径；仅静态分析，未运行页面或核验临床标准，医疗结论须专业人员复核。

### 血糖和理想体重清空后保留旧结果（中 · 部分修复余项）
- 已修（第1309批）：`blood-sugar-converter.html` 新增 `clearGlucose()`，fromMmol/fromMgdl 空/非法输入同步清对方输入与状态、刻度、统计卡；假「换算系数」已于第1305批改恒为 18.02；强锚 `BSCLR` 已落 health verify。
- 余项：`blood-sugar-converter` 负数仍进入低血糖分类（涉临床适用范围，待专业裁断）；`ibw-calculator.html` 清空身高直接返回、理想体重与实际体重比较仍是前次值，极小正身高可产生负理想体重，临床公式适用范围需专业核对，未擅改。

### 蛋白质计算输入含义及边界需复核（中，代码确认）
- `tools/health/protein-needs.html:169-173,202-207,373-407`：读取性别但不参与计算；来源系数可使推荐量超过页面标示的「安全上限」，例如 65 kg、竞技运动员 2.2 g/kg、纯植物系数 0.7 时推荐约 **204 g/天**，而上限约 **163 g/天**。这只是实现和标签之间的矛盾，不判断该上限的临床有效性。建议解释输入用途，核对来源系数、推荐范围及健康人群适用条件。
- `health/fracture-healing` 的筛选、年龄对照、预设和图表代码已阅读；未发现上述同类确定性问题不等于交互或临床内容经验证。

## 2026-11-06 健康生活工具静态复核

> 实读 `health/{sleep-cycle-calculator,smoking-cost-calculator,waist-hip-ratio,water-intake-calculator}` 的主要输入及结果路径，仅静态阅读和算式复算；未运行页面，医学适用性须复核。

### 腰臀比与饮水计算清空后的结果未同步（中 · 部分修复余项）
- 已修（第1309批）：`waist-hip-ratio.html` 无效输入在既有主卡清理基础上补清 waistVal/hipVal/whtrVal/bmiVal/riskContent，强锚 `WHCLR` 已落 health verify。
- 余项：`water-intake-calculator.html` 清空体重或填 0 仍按 65 kg 计算，年龄无效时只更换主结果而杯数、范围、时间表保留旧值；页面接受 0 岁并生成成人式饮水时间表，使用场景与安全性须儿科专业复核，区分空值与 0、限制不适用人群涉及专业口径，未擅改。

## 2026-11-06 康复与呼吸计时器静态复核

> 阅读 `health/{rehab-timer,breath-timer}` 的选择、计时及历史路径，以下为代码推断，未操作页面或验证真实计时。

- `tools/health/rehab-timer.html`：删除当前或前面的项目后未同步重设 `itemId`，可能指向另一项目或不存在的项，后者开始时读取 `undefined.duration`——第1311批已修（splice 后重映射 itemId 并同步 remaining，强锚 `RHDEL` 已落 health verify）。余项：运行中更改下拉框不会切换当前计时项目，但下拉框仍可显示新选择；涉及运行中切换语义，待裁断。
- 同页 `:542-558,590-597` 在开始和暂停后继续时立即调用 `tick()`，随后才设置每秒定时器，因此每次开始或恢复都立刻扣减 1 秒。建议维护稳定项目标识、删除时停止或重选、运行中锁定选择，并避免额外的立即扣秒。

## 2026-11-03 第一轮抽样补充

### 无效眼轴仍显示推荐晶体度数（历史结论，源码已变待回归）
- `tools/ophthalmology/iol-power.html:408-414` 当前 `calc()` 已新增眼轴 15–36、K 30–60、A 常数 100–130 的有限值与范围检查，并清除次级输出；旧版 0 眼轴的结论不再适用于当前源码，未做运行回归。旧记录中的页面示例与函数算值差异、SRK/T 公式权威性及极值边界仍需独立核验。
- 方案：实际计算入口检查适用输入及分母、清除所有旧结果；算例按实现重算并核对。当前未验证 SRK/T 公式的权威性或临床适用性，需领域专家核对，不将软件结果作为临床依据。保留输入快照、模型名称和校验状态以便复核。

## 2026-11-03 续查（并行批 G）

> 本批覆盖 8 页：`cardiology/{chads2-vasc,has-bled,grace-score,timi-score,nt-probnp,ckd-epi,statin-dose}`、`clinical-lab/blood-gas-analysis`。均为源码阅读 + node 内存复算，未做真实浏览器、英文态、移动端、权威标准或门禁验证。

### 留存优化
- 心内数值页统一接入同一套输入守卫：`ckd-epi` 已有 `__tbInputGuard`，而 `grace-score`、`timi-score`、`nt-probnp`、`statin-dose` 仍是 `||0` 裸解析，建议抽成共享脚本后逐页替换，避免同类空值缺陷反复出现。
- 把静态表格/公式说明中的分档阈值改为与 `calc()` 常量同源（如 HAS-BLED 3 分、TIMI `/14`、CHA₂DS₂-VASc 女性 1 分），防止「说明一套、计算一套」。
- 血气分析建议补一张「pH 正常时的四象限（PaCO2↑/↓ × HCO3↑/↓）」判定表，并在结果中显式输出 AG/代偿方向，减少单向标签误判。

### 续查覆盖
- 本批逐页阅读并内存复算 8 页：`cardiology/chads2-vasc`、`cardiology/has-bled`、`cardiology/grace-score`、`cardiology/timi-score`、`cardiology/nt-probnp`、`cardiology/ckd-epi`、`cardiology/statin-dose`、`clinical-lab/blood-gas-analysis`。
- 未覆盖：`cardiology` 其余页（如 `statin` 之外的血脂/抗凝页、`ckd-epi` 同目录页）、`nephrology` 其余页、`endocrinology` 其余页；`homa-ir` 仅初读未成条。未做浏览器、英文态、移动端、真实设备与门禁验证，结论均为静态源码 + node 复算口径。

## 追加审计：心内 3 页 + 呼吸 3 页（2026-11-04）

### 承诺 vs 实际（Q 批专项）

- `tools/pulmonology/pneumothorax.html`：meta/副标题/信息框宣称「Rhea 法」（`:10`、`:118`、`:168`）vs 引据表描述另一算法且无 Rhea 出处（`:219-221`）——**Rhea 方法学未落实**，判定：待验证。
- 复制/导出：6 页均有「导出明细 CSV」（calc-3 `:160`/`:416-419`、ambulatory `:150`/`:504`、coronary `:144`/`:527`、tb-resistance `:165`/`:493`、pulmonary-function `:147`/`:485`、pneumothorax `:150`/`:461`）；除 calc-3 外 5 页另有「复制结果」（ambulatory `:151`/`:344`、coronary `:145`/`:367`、tb-resistance `:166`/`:321`、pulmonary-function `:148`/`:312`、pneumothorax `:151`/`:289`）。未发现「宣称复制/导出但按钮缺失」；导出的是历史表，若历史为空则为空表，属可用性提示缺失而非功能缺失。
- 难度分级/限时/ROI/核验：本批 6 页未发现此类营销宣称；页面均为「仅供临床参考」。

### 覆盖

- 实读 6 页：`tools/cardiology/calc-3.html`、`tools/cardiology/ambulatory-bp.html`、`tools/cardiology/coronary-calcium.html`、`tools/pulmonology/tb-resistance.html`、`tools/pulmonology/pulmonary-function.html`、`tools/pulmonology/pneumothorax.html`。
- 新增 39 条（03-84–03-122）：高 11、中 21、低 7（含 2 条待验证）；另每页 3 条留存建议。
- 未覆盖：同目录其余心内/呼吸页、`zh-tw/` 繁体产物、英文态运行时字典；未做浏览器、移动端、真实设备、门禁与线上验证。
- 医学阈值/方案（TIMI 分层、ABPM 晨峰、CACS 百分位与停药、TB 耐药分型与方案、GOLD、气胸分型）均未做独立文献核验，落地前需医师/药师复核。

### 覆盖

- 实读 5 页：`tools/cardiology/hypertension-jnc.html`、`tools/cardiology/cardiac-rehab-mets.html`、`tools/cardiology/aspirin-prevention.html`、`tools/cardiology/echo-report.html`、`tools/cardiology/nyha-classification.html`。
- 新增 15 条（03-123–03-137）：高 5、中 8、低 2；另每页 3 条留存建议。
- 未覆盖：同目录其余心内页、`zh-tw/` 繁体产物、英文态运行时字典；未做浏览器、移动端、真实设备、门禁与线上验证。
- 医学阈值/方案（血压分级与风险矩阵、METs 能耗换算、USPSTF 年龄与出血阈值、LVEF 分类与 ICD 指征、6MWT 分档）均未做独立文献核验，落地前需心血管医师/药师复核。

### 覆盖

- 实读 8 页：`tools/cardiology/cpet-analysis.html`、`tools/cardiology/antiarrhythmic-class.html`、`tools/cardiology/myocardial-bridge.html`、`tools/cardiology/calc-1.html`、`tools/cardiology/rater-risk-3.html`、`tools/pulmonology/self-assess-3.html`、`tools/pulmonology/rater-13.html`、`tools/pulmonology/pulmonary-rehab.html`。
- 新增 20 条（03-138–03-157）：高 6、中 11、低 3；每页 1–3 条留存建议。
- 数值均 node 实算（复现脚本 `/tmp/audit_calc.mjs`）；HTML 结构用 python3 `html.parser` 验证（`input` 标签吞 `</div>`）。
- 未覆盖：浏览器真机/移动端、英文态运行时字典、`zh-tw/` 繁体产物、门禁与线上验证。
- 临床阈值（CPET 移植指征、JNC 7 风险矩阵、GRACE 分段与死亡率表、FTND 分档、Wells 三/二分类、MIP/MEP 参考下限与 RMT 强度）未做独立文献核验，落地前需心血管/呼吸科医师与临床药师复核。

### V 批覆盖清单（2 页）
- `tools/gastroenterology/ibd-nutrition.html`：4 条中 03-195 已于第1331批修复（BMI/白蛋白空值不计分，强锚 `IBD195`）、03-197 标尺已修（IBD197）、03-198 cat 已修（IBD198CAT）；仅 03-196 并发症档位与公式/选项顺序颠倒未动（评分表口径须临床复核）。BMI/体重下降/摄入的正向分档与总分相加逻辑本身正确。
- `tools/gastroenterology/capsule-endoscopy.html`：3 条中 03-199/200/201 已于第1330批修复（跨日归一化+00:00判空+标尺三段同源，强锚 `CAPFIX`）；同日、顺序正确时 GTT/SBTT 与 60/90、180/360/480 分级实算一致。余项：同日倒序硬报错须临床口径裁定。
- **本批合计 7 条：高 2（03-195、03-199）/ 中 5。假工具 0 个。全部阈值与建议均需临床复核。**
- 说明：本轮为**只读**审计，逐行读源码 + `node` 在 `/tmp` 复刻 `calc()` 实算（脚本 `/tmp/v_gi.js`、`/tmp/v_capsule.js`）；**未开浏览器**、**未运行 `_build.py` / `run_gates.py`**、**未做线上验证**，除本文件外未修改任何仓库文件。

### 828 批核销记录（2026-11-16）

- 核销 03-91、03-97、03-112、03-117、03-132、03-138、03-152、03-158 共 8 条（高 8）。
- 前六项为「空值按 0 出结论」类缺陷，页面均已改为空值拦截/未检测提示；FTND 已有 `__scaleDirty` 默认态守卫；Wells 三分类已改 `<2` 低危，本批仅补移除 `hr` 默认勾选。
- 门禁：`verify_cardiology_calc.js` 44/44、`verify_pulmonology_calc.js` 47/47（各新增 4 例）；`_build.py` + `_test_static.py` 4685/4685/0。
