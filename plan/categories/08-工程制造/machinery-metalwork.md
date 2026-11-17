# 机械/金属加工 · tools/{machinery,metalwork,welding,manufacturing}（~160 页）

## 2026-11-06 木工角度静态续审（清单 651）

- `tools/woodworking/angle-cut.html:287-307,328-367`：接头角、段数清空分别按 90、2 计算；复合角空值按 0；锥切宽度空值按 0，非法长度只更新文字不清原指标卡。等宽合法输入使 `len/diff` 为 Infinity，结果区域被整块数值守卫替换为错误；图形只用段数绘制正多边形，不反映传入角度。几何与实际锯台设定须专业复核，未运行页面。

## 2026-11-06 印刷工具静态续审

- `tools/printing/analysis-7.html:204-228`：非法及负数测点被静默丢弃，`parseFloat` 还会接受数字前缀；全零时均匀度无分母却输出 0、判定「暗斑明显」。输入无效时参考标尺未清除。
- `tools/printing/box-area.html:274-320`：长宽高之外，粘口和出血空值按 0，负数未经校验可导致面积偏低；纸板尺寸和含出血面积口径应结合具体盒型复核。
- `tools/printing/carton-design.html:282-288,291-341,364`：板厚未限制小于各外尺寸的一半，可生成负内尺寸和容积；反算比例空或 0 静默按 1。初始仅调用尺寸计算，切到容积反算时未调用 `calcVol()`，结果待输入变化才生成。
- `tools/printing/convert-gsm.html:203-232`：原紧度 0 静默替换问题关键代码已变，现有范围校验；但 A4 按 1/16 m² 计算，实际 210×297 mm 是 0.06237 m²，结果略有偏差。
- `tools/printing/estimate-ink.html:255-265,277-295,306-327,351-355`：无单价分支和 CMYK 的「单张墨量(毫克)」用 kg/张乘 1000，实际应乘 1000000，数值小 1000 倍；印数 `parseInt` 会截断小数。历史公式、四色范围及损耗标签问题关键代码已有变化，详见长尾旧条目。
- `tools/printing/ink-coverage.html:290-308`：只校验宽、长和张数；覆盖率、上墨量、单价、损耗空值变 0，色数空或 0 变 1，负数及覆盖率超 100% 可参与计算。`tools/printing/sheet-calc.html:270-287` 已用 `Math.ceil` 取整每册张数，历史问题关键代码已变；损耗仍可为负且空值按 0。均为静态分析，未运行浏览器，工艺模型须复核。

## 2026-11-06 塑料工具静态续审

- `tools/plastic/blow-molding.html:270-320`：只校验部分分母，制品直径、型坯壁厚、屈服强度空值按 0；例如清空制品直径仍输出吹胀比 0 和「偏小」，清空强度仍输出推荐压力 0；负数也可进入计算。应校验输入并清空结论。
- `tools/plastic/injection-cycle.html:263-301,304-316`：各工序空值按 0、型腔数空或 0 按 1；只校验总周期，负工序、良率超 100%、日运行时间超 24 小时仍参与计算。总周期无效时仅覆盖结果，旧阶段图仍留存，复制路径也不复用守卫。
- `tools/plastic/material-select.html:124-145,248-275`：筛选条件按材料特点过滤，搜索覆盖名称和应用；提示写「点击性能特点标签可快速筛选」，但表格单元格只输出纯文本，没有点击处理，提示与实现不符。
- `tools/plastic/shrinkage-calc.html:249-280,283-295`：制品尺寸空值按 0 得 100% 收缩率；反算收缩率空值按 0，100% 得除零并显示破折号，超过 100% 或负数仍给出负尺寸或放大量。复制路径另行计算，可复制 Infinity；应验证输入及复用有效结果。
- `tools/plastic/extrusion-rate.html:253-302` 输入触发计算并校验参数，历史千倍量纲问题现已除以 1000，详见长尾行业旧条目；以上均为静态分析，未运行页面或验证工艺模型。

## 2026-11-06 金工工具静态续审

- `tools/metalwork/thread-spec.html:250-283,453-460`：筛选和分类生成规格表，当前导出指向该规格表，历史导出历史表的关键代码已变；规格数据及实际导出未做专业或浏览器验证。

## 功能缺陷
- metalwork 7 个「双段通用对比页」功能单薄（carbon-8/diandonggongju-xifen/laxue-ladao/tangxue/wushua/yuanlingongju-xifen/zhineng-duogongneng）：生效 calc 仍是 A/B 两值通用比值-差值输出，非领域公式（carbon-8 第二段有 850-950℃ 渗碳拟合为例外）；建议按主题补真实领域计算（渗碳层深-时间、拉削力-齿升、镗杆刚度等）。
- 折弯页缺「回弹补偿」输入项。

## 优化点
- S3 分步：齿轮/皮带选型链路图（已注入部分 chart，推广 S3 明细）。

## 受影响范围
- tools/machinery/（78）、tools/metalwork/（42）、tools/welding/、tools/manufacturing/

## 进度
- 🔴 待开发

## 2026-11-03 审计补充

### 留存优化：材料温度变化对照（低，建议）
- 证据：同页 `:223-230,246-251,264-267` 已提供线膨胀公式、明细和数值预设。
- 影响：同页；方案：预设可标注材料来源与适用温度，并并排展示用户选择的两种材料伸长量；注明线性系数为近似。

### 覆盖
- 本轮人工及只读子代理核查 `tools/engineering/thermal-expansion.html`、`tools/machinery/pidaizhangjinjisuan.html`、`tools/metalwork/welding-heat.html` 共 3 页；仅源码和算术推导，未做浏览器验证，其余未逐页覆盖。三条已全部修复销账。

## 2026-11-03 续查（并行批 H）

> 编号说明：文件原有历史编号 `M3` 保留不动；本批按并行批约定新增 `MM-H` 系列，不与其重号。以下结论均为源码阅读 + node 内存复算，未做真实浏览器、英文态、移动端、门禁或线上验证。

### MM-H8 不良率页把「不良品数」当「缺陷数」，d>t 直接拦截多缺陷场景（中，确认）
- 描述：页面输入名是「不良数」，但 DPMO 按 `d/t/p` 计算；当一件产品存在多个缺陷（DPMO 的标准口径）时，缺陷数可大于投入件数，页面却在 `d>t` 时直接 toast 拦截，导致该口径无法录入。
- 证据：`tools/manufacturing/defect-rate.html:174-182`（三个输入）、`:297-304`（`if(d>t)` 拦截与 `dpmo=(d/t)*1e6/p`）、`:220`（深度解析以「不良 250 件/2 工序」举例，未区分缺陷与不良品）。node 复算 total=1000、defects=1200 → 被 `d>t` 拦截；若按缺陷数口径，DPMO=（1200/1000）×10⁶/2=`600000`。
- 影响：`tools/manufacturing/defect-rate.html`。多缺陷工序的真实 DPMO 无法计算，用户只能把缺陷数压成不良品数，结果系统性偏低。
- 方案：拆成「不良品数」与「缺陷数」两个输入（PPM 用不良品数、DPMO 用缺陷数），或在单一输入上加「计数口径」切换并同步结果卡标签。

### 留存优化
- `tools/metalwork/sheet-bend.html`：增加 R/T–K 因子联动提示表与「回弹补偿角」输入（现有功能缺陷已记缺回弹项），并在结果区并列显示「含回弹修正的展开长」。
- `tools/metalwork/forging-ratio.html`：增加各火次锻造比与累计锻造比（连乘）小表，直接对应标准引据里的「总锻造比」条款。
- `tools/manufacturing/capacity-planning.html`：结果区并列展示「加班次 / 加设备 / 外包」三种补缺口方案的件数与成本，替代当前只给「新增 N 台」。
- `tools/manufacturing/defect-rate.html`：把 DPMO→σ→CPK 的换算阶梯画成一条标尺并标出当前值，同时区分「不良品率 / 缺陷率」两种口径。
- `tools/welding/weld-strength.html`：内置 Q235/Q345/304 的角焊缝强度设计值小表与利用率条，让「够不够」一眼可见。
- `tools/machinery/bearing-1.html`：补 a₁/aISO 修正系数输入与「L₁₀ vs 修正寿命」对照；历史摘要补轴承类型（当前 `historySummary()` 只写 C/P/n，不同类型记录看起来相同）。
- `tools/machinery/tanhuangsheji.html`：并列展示质量、固有频率推导与端部型式（并紧/磨平）对压实长度的影响；修正频率后可加「工作频率→频率比」提示。
- `tools/metalwork/calc-stretch.html`：按 GB/T 228.1 增加「标距类型（5d/10d）」与原始直径联动，自动校验 L0 与截面积是否自洽。

### 续查覆盖
- 已覆盖 8 页：`tools/metalwork/sheet-bend.html`、`tools/metalwork/forging-ratio.html`、`tools/manufacturing/capacity-planning.html`、`tools/manufacturing/defect-rate.html`、`tools/welding/weld-strength.html`、`tools/machinery/bearing-1.html`、`tools/machinery/tanhuangsheji.html`、`tools/metalwork/calc-stretch.html`。
- 已排除前批已覆盖页：`tools/machinery/pidaizhangjinjisuan.html`、`tools/metalwork/welding-heat.html`、`tools/engineering/thermal-expansion.html`（后者不在本文件四个目录内，仅作去重说明）。
- 未覆盖：machinery/metalwork/welding/manufacturing 其余页面（含 `carbon-8`、`laxue-ladao` 等双段对比页）本批未逐页审计。
- 编号：本批编号 `MM-H1`–`MM-H13`，现存待办 `MM-H8`（不良品/缺陷计数口径需产品裁断）。
- 验证声明：仅源码阅读 + node 内存复算；未做真实浏览器、英文态（`?lang=en-US`）、移动端、门禁、线上或导出文件实测。涉及 TBKit 渲染、toast、CSV 输出的运行时表现未实测，相关条目仅确认到源码路径层面。

## V 批 · 机械/金属/焊接/制造（2026-11-04）

> 范围：`tools/machinery/` 4 页（低噪音寿命、涂装用量、润滑系统、输送带选型）+ `tools/metalwork/` 1 页（螺纹规格）+ `tools/welding/` 2 页（保护气体配比、安全通风）+ `tools/manufacturing/` 1 页（CPK）。方法：逐页源码阅读 + node 内存复算（脚本 `/tmp/v_batch.js`）；未开浏览器、未跑 `_build.py` / `run_gates.py`、未做英文态/移动端/线上验证。编号续接 `MM-H37`，从 `MM-H38` 起。

### 覆盖清单
- `tools/machinery/lifespan-18.html`：深度解析第二算例载荷因子已改为 0.858，与公式一致（2026-11-16 第 663 批销账）。
- `tools/machinery/area-dosage-1.html`：未发现中/高缺陷；`10·VS/DFT` 涂布率、`A/(理论×TE)` 实际用量、1.3 kg/L 质量估算与 0~100 区间校验均正确，未记缺陷。
- 编号：本批新增 `MM-H38`–`MM-H47`（2 高 / 8 中），续接 `MM-H37`，不重号；H38–H47 已全部修复销账。
- 验证声明：仅源码阅读 + node 内存复算；未开浏览器、未跑 `run_gates.py` / `_build.py`、未做英文态/移动端/线上验证。本批未修改任何工具页、js/css/json 或构建产物。

## W 批 · 机械扭矩/压力/寿命（2026-11-04）

> 范围：`tools/machinery/` 6 页（低油雾寿命、花键规格、扭矩补偿、联轴器选型、皮带传动、刚度/载荷/疲劳检测）+ `tools/metalwork/` 2 页（无损探伤分级、试模问题统计）。方法：逐页源码阅读 + node 内存复算（脚本 `/tmp/w_batch.js`）；未开浏览器、未跑 `_build.py` / `run_gates.py`、未做英文态/移动端/线上验证。编号续接 `MM-H47`，从 `MM-H48` 起。

### 覆盖清单
- `tools/machinery/lifespan-23.html`：换油间隔与伪油雾生成量已修（MM-H54、MM-H55）。
- `tools/machinery/pressure-4.html`：内/外花键标签与深解挤压表述已修（MM-H48、MM-H49）。
- `tools/machinery/torque-3.html`：历史已补存动载/工况（MM-H50）。
- `tools/machinery/torque-2.html`：历史已补存负载特性（MM-H51）。
- `tools/machinery/power-16.html`：带速/超系列提示与「无根数校核」声明已修（MM-H52、MM-H53）。
- `tools/machinery/detector-159.html`：国标/验收表述与 S-N 承诺已核实清除（MM-H56、MM-H57）。
- `tools/metalwork/detector-24.html`：输入校验与尺寸阈值降级已完成（MM-H58、MM-H59）。
- `tools/metalwork/analysis-35.html`：正数/严重度校验、字段切分与转义已完成（MM-H60、MM-H61、MM-H62）。
- 编号：本批新增 `MM-H48`–`MM-H62`（2 高 / 13 中），续接 `MM-H47`，不重号；假工具 1（MM-H56）／安全 1（MM-H62）。
- 验证声明：原审计为源码阅读 + node 内存复算（`/tmp/w_batch.js`）；H48–H62 已在 2026-11-16 第 663–669 批逐条修复，均跑对应小门禁、`_build.py`、`_test_static.py` 与 selfcheck（归档见 `plan/已修复/2026-11-16-663…669`）。

## X 批 · 机械检测/寿命（2026-11-04）

> 范围：`tools/machinery/` 8 页（智能/无人/高效对比、设备寿命分析、螺纹传动、电机选型、橡胶三项检测、紧固件三项检测、轴承三项检测、阀门选型）。方法：逐页源码阅读 + node 内存复算（脚本 `/tmp/x_batch.js`）；未开浏览器、未跑 `_build.py` / `run_gates.py`、未做英文态/移动端/线上验证。编号续接 `MM-H62`，从 `MM-H63` 起。

### 覆盖清单
- `tools/machinery/zhineng-wurenyugaoxiaoduibijisuanqi.html`：0 问题（补无人化评分成三路线、深解改评分方法与 0–100 校验，MM-H70、MM-H71）。
- `tools/machinery/analysis-lifespan.html`：0 问题（维修时间 0~rt、故障次数正整数、深解改为 MTBF/可用度，MM-H67–H69）。
- `tools/machinery/thread-drive.html`：0 问题（下放力矩含轴承摩擦、非自锁文案与 guard 分子提示已修正，MM-H72）。
- `tools/machinery/calc-200.html`：0 问题（超 630 kW 只提示超系列、效率 >100% 拦截，MM-H65、MM-H66）。
- `tools/machinery/detector-134.html`：国标/验收表述已清除、负值拦截已补（MM-H63、MM-H64）。
- `tools/machinery/detector-hardness-torque.html`：国标/验收表述已清除、负值拦截已补（MM-H63、MM-H64）。
- `tools/machinery/detector-155.html`：国标/验收表述已清除、负值拦截已补（MM-H63、MM-H64）。
- `tools/machinery/pressure-flow-5.html`：0 问题（Cv/Kv、DN 选档、流速与深度解析算例均复算一致；历史 `lines[10]` 取「估算流速」行正确）。
- 编号：本批新增 `MM-H63`–`MM-H72`（1 高 / 9 中），续接 `MM-H62`，不重号；假工具 1（MM-H63，另 MM-H70 为部分）；安全 0；承诺未实现 1（MM-H68）。
- 验证声明：原审计为源码阅读 + node 内存复算（`/tmp/x_batch.js`）；H63/H64 已在 2026-11-16 第 670 批修复（三页国标表述退场、负值拦截补齐）、H65/H66 已在第 671 批修复（超系列告警、效率上限拦截）、H67–H69 已在第 672 批修复（维修时间 0~rt、故障次数正整数、深解改 MTBF/可用度）、H70/H71 已在第 673 批修复（补无人化评分与 0–100 校验、深解改评分方法）、H72 已在第 674 批修复（下放力矩含轴承摩擦、非自锁文案、分子提示），均跑对应小门禁与构建，归档见 `plan/已修复/2026-11-16-670…` 至 `674…`。X 批条目已全部销账。

## Y 批 · 机械·铸造/齿轮/检测（2026-11-04）

**逐页结论（8 页）**
- `tools/machinery/analysis-casting.html`：重量、模数与 Chvorinov 凝固时间公式及默认算例（7200 g / 2.5 cm / 12.5 s）一致；标题/引据仍是「箱体焊接/刚度」。
- `tools/machinery/calc-89.html`：平均半径 (D+d)/4、T=μFRmz、p=F/A 正确，默认 80 N·m / 0.099 MPa 复算一致；深度解析整节跑题到法兰接合面。
- `tools/machinery/calc-gear.html`：直齿 d/db/da/df/p/pb 与默认算例正确；斜齿根切最少齿数少乘 cos²β，判定偏松，齿顶厚未实现。
- `tools/machinery/detector-194.html`：决策只剩「年限>8 更换」，设备类型与运行模式是死输入，检查清单只按故障套模板，阀门/换热器也列旋转机械拆检项。
- `tools/machinery/detector-stretch.html`：三项阈值全是写死常量却宣称依据 GB/T 1689、GB/T 528、GB/T 1688 判定合格，空值/负值还可判合格，属假工具。
- `tools/machinery/energy-2.html`：制动能耗/扭矩/功率公式正确，默认 30.84 kJ、130.90 N·m、10.28 kW 复算一致；深度解析讲电机效率与年电费，与制动无关。
- `tools/machinery/estimate-gravity.html`：六种体积公式与形心取值正确，默认板 50 cm³ / 392.5 g 一致；负尺寸/负密度不拦，组合重心缺逐件全局偏移输入。
- `tools/machinery/flow-14.html`：水力/轴功率/电机功率与两个算例复算一致（4.09/5.45/6.27 kW，nq 48.7）；电机 400 kW 上限、η/K 校验、公式框与固定 1450 r/min 均有缺陷。

**问题条目**

| 页面 | 问题（含 tools/machinery/<slug>.html:NN） | 编号 |
|---|---|---|
| tools/machinery/analysis-casting.html | 【中】名不副实：`<title>`/meta 为「箱体（焊接/铸造/刚度）分析」并承诺刚度与变形，页面实际只算浇注重量/模数/凝固时间；标准引据表列尺寸公差/拔模斜度/刚度，均无对应输入输出（:10-11,183-195） | MM-H74 |
| tools/machinery/calc-89.html | 【中】深度解析整节写法兰接合面压力（W/A、螺栓预紧），与离合器无关；算例 D=100/d=60、W=10 kN 无法用页面输入复现（:433-442） | MM-H75 |
| tools/machinery/calc-gear.html | 【高】斜齿根切最少齿数用 2ha*·cos³β/sin²αt，按端面条件应为 2ha*·cosβ/sin²αt；β=20° 得 12.7（应 14.4），β=30° 得 8.7（应 11.5），13 齿斜齿轮会被判「不根切」（:322,325；:178 亦写 17·cos³β） | MM-H77 |
| tools/machinery/calc-gear.html | 【中】深度解析称「校核根切与齿顶厚」，页面只输出 da/df，无齿顶厚 sa 计算（:511） | MM-H79 |
| tools/machinery/detector-194.html | 【高】设备类型 v1 与运行状态 v4 为死输入：calc 只用 years>8 判更换，v1/v4 仅回显名称；检查清单只按故障 v2 分支，阀门/换热器也输出「轴承磨损/联轴器对中/地脚螺栓/动平衡」；简介仍称「考虑运行模式的影响」（:213-222,227-231,288） | MM-H80 |
| tools/machinery/detector-stretch.html | 【高】阈值 0.08 g、20 MPa、1×10⁶ 次为写死常量，却宣称依据 GB/T 1689、GB/T 528、GB/T 1688 判定合格；三者均为试验方法标准，不规定该合格线，页面还称「检测报告可用于质量验收」（:10,213,232；:125 仍为「合法性校验」模板） | MM-H81 |
| tools/machinery/detector-stretch.html | 【中】空值/负值兜底为 0 后直接判定：清空磨耗量 → 0 g 显示「合格」，磨耗 -0.5 g 也判「合格」，漏检项目被当作合格项（:219-226） | MM-H82 |
| tools/machinery/energy-2.html | 【中】深度解析「设备能耗/能效」讲电机效率、年电费与传动效率连乘，页面只算制动能耗，5 kW / η=90% / 4000 h 算例无对应输入；引据表列「温升核算」但页面无质量/比热/散热输入（:426-434,159-161） | MM-H83 |
| tools/machinery/estimate-gravity.html | 【中】val() 只把 NaN 归 0，尺寸与自定义密度无正值校验：板长 -100 mm → V=-50 cm³、m=-392.5 g；密度 -5 g/cm³（默认板 50 cm³）→ m=-250 g（:306,331-366） | MM-H84 |
| tools/machinery/estimate-gravity.html | 【中】组合重心无逐件全局位置输入：addToAssembly 只存局部 cx/cy/cz，renderAssembly 直接 Σm·c/Σm 并标「组合重心」；两件无法分别放到 x=0 与 x=200，页面注文自认「需考虑各零件在全局坐标系中的位置偏移」，且提示称原点为几何中心而代码输出 L/2（:200,398-403,421-427,442） | MM-H85 |
| tools/machinery/flow-14.html | 【中】pickMotor 在 Pm>400 kW 时静默返回 400，仍标「推荐电机」：Pm=500 → 推荐 400 kW、负载率 125%，无「超范围」提示（:194-197,210,224,230） | MM-H86 |
| tools/machinery/flow-14.html | 【中】效率 η 与安全系数 K 只判非负/非零，未按 1–100、1–2 校验：η=120% → Psh=3.41 kW 小于水力功率 4.09 kW；K=0.5 → Pm=2.73 kW（:136-137,198,203） | MM-H87 |
| tools/machinery/flow-14.html | 【中】公式框写 P_s=ρgQH/(η·1000)，Q 按页面 m³/h 计漏掉 /3600（且 η 未注明百分数/小数），按该式手算至少大 3600 倍；下方信息框才是 /(3600×1000)（:128,145） | MM-H88 |
| tools/machinery/flow-14.html | 【中】比转速固定按 1450 r/min 计算，页面无转速输入：2900 r/min 时 nq 翻倍（默认 48.7→97.4），泵型从「旋涡泵/部分流泵」跨到「离心泵（中比转速）」；简介仍称「依据比转速推荐泵型」（:212-219,228-229） | MM-H89 |

**统计**
- 条数：14（高 3 / 中 11）；编号区间：MM-H73–MM-H89，续接 MM-H72，不重号不跳号。
- 高优编号：MM-H77（齿轮根切判据算错）、MM-H80（检测页死输入）、MM-H81（检测页写死阈值冒充国标）。
- 假工具：1（`tools/machinery/detector-stretch.html`）。安全条目：0（无 XSS、eval、allow-same-origin、明文存密、第三方外传）。
- 复算：node 内存复算关键值（根切 zmin、负体积/负密度、泵功率与 nq、制动能耗、离合器扭矩/压力），未落盘仓库；仅源码阅读，未开浏览器、未跑构建/门禁、未改工具页。
- 去重说明：`detector-stretch` 与既有 MM-H63 同为「写死阈值冒充国标」模式，但页面不同，按逐页口径单列。

## Z 批 · 机械·选型/寿命/传动（2026-11-04）

**逐页结论（8 页）**
- `tools/machinery/flow-itinerary.html`：推力/拉力/容积/流量公式与默认算例复算一致，预设条单位已与输入（MPa）一致。
- `tools/machinery/frequency-17.html`：k/m 固有频率、阻尼透射率、隔振效率与静变形公式及深度解析算例均复算一致，0 问题。
- `tools/machinery/jingmishebeixuanxing.html`：导轨 6 倍载荷、导程按 3000 rpm 的选择逻辑成立；但「导程精度」按导程写死 ±3/±5/±8 μm 与 C3/C5/C7 无关，超表上限静默取下限，历史漏存速度。
- `tools/machinery/lifespan-20.html`：L10 与其两个算例复算一致；但精度/润滑因子无 ISO 281 依据却冠以 ISO 281，dn 值固定按内径 25 mm 估算，两项核心结论失真。
- `tools/machinery/lifespan-7.html`：Arrhenius Q10 与四因子连乘复算一致；PV 固定 50 mm 轴径、限值 0.3，默认工况即报超限；超温段固定 0.05、低温无材料下限。
- `tools/machinery/lifespan-bearing-1.html`：p、v、pV、L10 与所需 C 复算一致；pV 合格线固定 10 忽略材料许用 6–30，且 pV>20 仍推荐滑动轴承，与「超限」自相矛盾。
- `tools/machinery/power-voltage.html`：P=Tn/9550、额定电流与两个算例一致；极数按阈值下取导致 1100/2000/2400 rpm 出现 −10%~−60% 负转差率，>400 kW 静默封顶。
- `tools/machinery/speed-26.html`：节距/链速/链节数公式与默认算例一致；链号「额定功率」实为与转速无关的单值常量，非峰值转速下普遍高估许用功率，超表上限静默取 24A。

**问题条目**

| 页面 | 问题（含 tools/machinery/<slug>.html:NN） | 编号 |
|---|---|---|
| tools/machinery/jingmishebeixuanxing.html | 【高】「导程精度」由导程写死（5→±3、10→±5、其余±8 μm/300mm），与所选 C3/C5/C7 无关：acc=50 判 C7（标准 ±50 μm/300mm），默认导程 5 却显示 ±3μm/300mm；acc=5 判 C3、导程 40 又显示 ±8μm/300mm，精度等级与精度值自相矛盾（:217, :220, :232） | MM-H91 |
| tools/machinery/jingmishebeixuanxing.html | 【高】导轨/导程超表静默取末项：负载 2000 kg→需 117.6 kN，仍推荐 HGR65（动额定仅 101 kN）；速度 200 m/min→导程 40mm 时转速 5000 rpm，超过页面自称 3000 rpm 上限，均无超范围提示（:200-202, :205-208, :216, :230） | MM-H92 |
| tools/machinery/jingmishebeixuanxing.html | 【中】历史记录 `saveHistory` 未存 vSpeed，`restoreHistory` 也不恢复速度；恢复后按当前速度重算，同一记录的导程/转速/扭矩与保存时不一致（:239, :241, :216） | MM-H93 |
| tools/machinery/lifespan-20.html | 【高】精度因子 p0..p2=1.0/1.05/1.1/1.2/1.5、润滑因子 grease..jet=0.8/1.0/1.3/1.5 均无 ISO 281 依据；`precisionLife=L10h*cf*lf` 把润滑影响二次计入（L10 本身已受润滑影响），P2+喷油可把「精度保持寿命」放大至疲劳寿命 2.25 倍，与注文「精度保持寿命通常低于疲劳寿命」矛盾；meta/简介仍称「基于 ISO 281…结合精度等级因子」（:10, :209-210, :232） | MM-H95 |
| tools/machinery/lifespan-20.html | 【高】dn 值按 `n*25` 写死内径 25mm，页面无内径输入；5000 rpm 下实际 100mm 内径 dn=500000（已到高速润滑警戒线），页面显示 125000 并判「工况良好」，dn 结论随真实轴承内径完全失真（:235-236, :243） | MM-H96 |
| tools/machinery/lifespan-7.html | 【高】PV 校核固定轴径 0.05m（无轴径输入），限值 PTFE 0.5、其余 0.3 MPa·m/s；默认 5MPa/1500rpm→PV=19.64 即「超限」，PTFE 预设 2MPa/500rpm→2.62 也「超限」却同时判寿命「优」，油润滑 O 形圈被系统性误判为干摩擦超限（:246, :249-250） | MM-H97 |
| tools/machinery/lifespan-7.html | 【中】温度因子超材料上限一律取 0.05：NBR 在 300℃ 仍与 130℃ 同为 231h；低温侧不按材料下限校验（NBR 可输入 -50℃），Q10 因子 2^13=8192，寿命放大到 3781 万小时（:221, :233-235, :243-244） | MM-H98 |
| tools/machinery/lifespan-bearing-1.html | 【中】滑动 pV 合格线固定 10 MPa·m/s，忽略注文给出的材料许用（巴氏合金 6–10、铝青铜 20–30）；pV=25 时既标「超限」，又因 `pV>20` 推荐「滑动轴承（高速或重载）」，结论自相矛盾（:175, :223, :226） | MM-H99 |
| tools/machinery/power-voltage.html | 【高】极数按转速阈值下取（≥2500→2、≥1200→4、≥800→6），不校验实际转速是否高于同步转速：1100rpm→6极(n1=1000, s=−10%)、2000rpm→4极(n1=1500, s=−33.3%)、2400rpm→4极(s=−60%)，页面直接输出负转差率，物理上不可能（:198-205, :237） | MM-H100 |
| tools/machinery/power-voltage.html | 【中】Pm>400kW 时 `pickMotor` 静默返回 400，仍标「推荐电机功率」并据此算极数/电流；K=1、Pm=500 → 推荐 400kW、负载率 125%，无超范围提示（:194-196, :225, :238） | MM-H101 |
| tools/machinery/speed-26.html | 【高】链号表每档只有单一 maxKw/maxRpm（06B 3kW/9000rpm … 24A 250kW/1300rpm），与转速、齿数、排数无关，却称「查 06B~24A 额定功率/转速表」；任意转速都直接套用同一峰值额定值，非峰值转速下普遍高估许用功率（5.5kW@960rpm 选 08A、30kW@1450rpm 选 12A），且无工况系数/齿数/排数修正（:206-214, :218-219, :465-466） | MM-H102 |
| tools/machinery/speed-26.html | 【中】无链号满足时 `sel` 保持末项 24A 并照常出结果：1000kW 时修正功率 1000kW 仍推荐 24A（maxKw 250）；n=10000rpm 仍推荐 24A（maxRpm 1300），无「超出选型范围」提示（:217-220, :228-233） | MM-H103 |

**统计**
- 条数：12（高 7 / 中 5）；编号区间：MM-H90–MM-H103，其中 MM-H90、MM-H94 已修销账，续接 MM-H89，不重号不跳号。
- 高优编号：MM-H91（丝杠精度等级与导程精度脱钩）、MM-H92（导轨/导程超限静默取下限）、MM-H95（无依据因子冒充 ISO 281）、MM-H96（dn 内径写死 25mm）、MM-H97（PV 轴径写死 50mm）、MM-H100（极数推断产生负转差）、MM-H102（链号额定功率表与转速无关）。
- 假工具：2（`tools/machinery/lifespan-20.html` 的核心精度/润滑因子无标准来源；`tools/machinery/speed-26.html` 的「额定功率/转速表」名不副实）。承诺未实现：0。
- 安全：0（8 页均无 XSS、eval、allow-same-origin、明文存密或业务数据第三方外传，无 path:line 可列；全站模板 ttzz 脚本不单列）。
- 复算：node 内存复算关键值（2000kg 导轨需求 117.6kN、200m/min 导程 40→5000rpm、PV 19.635 与 2.618、-50℃ NBR 3781 万小时、dn 500000、1100/2000/2400rpm 负转差、30kW@1450rpm 链速 9.67m/s），未落盘仓库；仅源码阅读，未开浏览器、未跑 `_build.py`/`run_gates.py`、未改 `tools/**` 与构建产物，未触碰 `plan/interaction-validity.md`。
- 去重说明：`lifespan-20` 与既有寿命类工具同属「L10 正确但附加因子无依据」模式，但本页新增 dn 写死内径，按逐页口径单列；`power-voltage` 的 400kW 封顶与 MM-H86（flow-14）同模式但页面不同，不合并。

## Z 批 · 机械·强度/扭矩/定位（2026-11-04）

**逐页结论（8 页）**
- `tools/machinery/strength-15.html`：实为「链条设计」（URL 名不符实，按 §7 不改名）；链速、圆周力、传动比、中心距、链节数复算正确，但节距/链号只按小链轮转速查表、功率 P 不参与，且无 meta 承诺的静/疲劳强度校核（高）。
- `tools/machinery/strength-7.html`：剪切/挤压/撕裂三式与默认算例复算一致，铆缝效率口径成立；但 n 同时充当铆钉数与单剪面积、净截面按全部铆钉同排扣除，缺剪切面数/排数输入，双剪与多排工况失真（中）。
- `tools/machinery/temp-hardness.html`：流程可跑，但回火软化斜率、介质系数、截面折减均为无来源写死常量，45 钢 500/600°C 硬度高估约 10–16 HRC（高）。
- `tools/machinery/torque-motion.html`：推力档位、速度、功率与默认算例一致；仅深度解析两个算例的效率用了页面不存在的 0.9 与错配的 0.6/0.7，历史不存执行器类型（中）。
- `tools/machinery/torque-response.html`: ω/α/T/峰值功率与两个算例一致；制动能量未乘负载系数（默认高 25%、反向负载低 23%），「默认参数」预设 vLoad 与页面默认不符（中）。
- `tools/machinery/xiao-dingwei-lianjie-chicun.html`：主算 d=√(4F/πτ) 正确；「双销并联直径=2×d」已于 972 批修正为 d/√2（真机 9/9 通过）。残留：⇄ 互换按钮错位量纲，挤压/销长/配合未实现（中）。
- `tools/metalwork/analysis-36.html`：计数/加权/缺陷率与算例（212、19.20%）一致；仅是统计器，可见英文副标题与简介承诺的成因/对策、标准差、控制界限、位置溯源均未实现（假 + 中；原未转义注入项已修复，第 952 批真机复核）。
- `tools/metalwork/analysis-cost-price-5.html`：均值/样本标准差/CV/极差/首末涨跌幅/最大回撤与算例一致；标题与引据表承诺材料成本构成但无任何成本输入，价格 0/负值未校验（假 + 中；原未转义注入项已修复，第 952 批真机复核）。

**问题条目**

| 页面 | 问题（含 tools/<dir>/<slug>.html:NN） | 编号 |
|---|---|---|
| tools/machinery/strength-15.html | 【高】选型只按小链轮转速查节距表，功率 P 完全不参与：5.5 kW 与 500 kW @960 r/min 都推荐 p=25.4 mm / 16A（v=7.722 m/s，F 分别 712 / 64753 N），无额定功率、抗拉、疲劳任何校核；meta 与 JSON-LD 仍称「并校核滚子链静强度与疲劳强度」，引据表列 ISO 606 / GB/T 1243 / ISO 10823 的强度与磨损三项，页面一项未算（:10, :154-166, :205-215, :223, :230） | MM-H104 |
| tools/machinery/strength-7.html | 【中】铆钉数 n 同时被当作剪切面数与同一排铆钉数：As=n·πd²/4 按单剪、A_net=(W−n·d)·t 把全部铆钉在同一净截面扣除，页面无剪切面数/排数输入，双剪或多排铆缝的剪切与撕裂承载力系统性失真；深度解析「双剪 n=2」实际按 2 个铆钉单剪计算（:277-282, :519） | MM-H105 |
| tools/machinery/temp-hardness.html | 【高】回火软化按固定斜率 k×(T−150)/100（k=1.0–4.0）线性外推，45 钢水淬：500°C 页面 42.6 HRC（手册回火曲线约 30–33）、600°C 页面 39.7 HRC（约 22–26），高估约 10–16 HRC；介质系数 1.0/0.85/0.6 与截面折减 1−0.15·ln(D/d)、0.5 下限同为无来源写死常量，却在引据表列 ISO 6507/642/4885（三者均为试验/术语标准，不给出硬度预测式）（:125, :206-218, :340-358） | MM-H106 |
| tools/machinery/torque-motion.html | 【中】深度解析两个算例的效率与页面档位不符：算例一称「蜗轮丝杠 η=0.7」（页面蜗轮丝杠为 0.6），算例二用 η=0.9（页面无此档）；默认工况按页面档位实算功率 0.15 kW（0.6）而非 0.13 kW，6000N/500mm/5s 实算 1.06 kW（0.85）而非 1.00 kW（:136-138, :386） | MM-H107 |
| tools/machinery/torque-motion.html | 【中】历史只存 F/S/t/SF，不存执行器类型（η），恢复记录后按当前档位重算，同一记录的电机功率与保存时不一致（:235, :237） | MM-H108 |
| tools/machinery/torque-response.html | 【中】制动能量 0.5·J·ω²/1000 未乘负载系数，而制动力矩/峰值功率已乘：默认 0.8（阻力辅助）页面 28.82 kJ 应为 23.06（高 25%）；提升反向 1.3 时页面仍 28.82，应为 37.47（低 23%），制动器热容量校核偏差（:208, :210-212） | MM-H109 |
| tools/machinery/torque-response.html | 【中】预设「默认参数」vLoad=1.0（纯惯性），页面默认选中 0.8（有阻力辅助）；点该预设后制动力矩由 101.23 变 126.54 N·m、选型力矩 151.84→189.81，与初始结果不一致（:137, :337） | MM-H110 |
| tools/machinery/xiao-dingwei-lianjie-chicun.html | 【中】「⇄ 互换 A/B」沿用通用两参模板，交换 F(kN) 与 τ(MPa) 后仍按 d=√(4F/πτ) 计算：20/120 互换后成 120 kN / 20 MPa，d=87.4 mm、截面积 5999 mm²，无单位/量纲提示（:131, :493-498, :562） | MM-H112 |
| tools/machinery/xiao-dingwei-lianjie-chicun.html | 【中】深度解析称「圆柱销/圆锥销的直径 d 与长度 L 按剪力与挤压选定」并给出 σc=F/(d·t)，页面无板厚 t、销长 L 与配合输入，只输出直径/截面积，「尺寸」与挤压校核未实现（:720-724, :563-566） | MM-H113 |
| tools/metalwork/analysis-36.html | 【假】只做「数量×权重」统计；可见英文副标题承诺 "Diagnose common casting defects … assess likely causes and remedies"，简介功能承诺均值/标准差/极差、控制界限判定批次合格性、按浇道/型腔定位高发位置，代码全部未实现，无任何成因/对策输出（:117, :286-292, :209-239） | MM-H114 |
| tools/metalwork/analysis-36.html | 【中】数量与权重不校验：cnt 可为负或 0（缺陷总数/缺陷率变负），权重不限 1–3（输 100 使加权指数虚高约 30 倍），页脚仍写「权重按严重度取 1~3」（:217-219, :237） | MM-H115 |
| tools/metalwork/analysis-cost-price-5.html | 【假】标题含「成本」、引据表列「材料成本=体积×密度×单价（铜 8.96 g/cm³）」与「总成本=材料+加工+损耗+废品率」，页面只有价格序列统计，无体积/密度/加工费/废品率任何输入，成本分析未实现（:125, :191-203, :220-256） | MM-H117 |
| tools/metalwork/analysis-cost-price-5.html | 【中】负价仍参与均值/标准差/回撤：输入 −10 等负值仍照常统计，缺少「价格应为非负」的业务校验（前一期为 0 与均值为 0 的除零假合规已于 973 批修复销账） | MM-H118 |

**统计**
- 条数：13（高 2 / 中 9 / 假 2）；编号区间：MM-H104–MM-H119，续接 MM-H103，安全两条 MM-H116/H119 已修复销账、MM-H111 双销量纲于 972 批销账，其余不重号不跳号。
- 高优编号：MM-H104（链条选型不看功率、无强度校核）、MM-H106（回火线性模型高估 10–16 HRC）；MM-H111（双销并联直径 2d）已于 972 批修正为 d/√2。
- 假工具：2（`tools/metalwork/analysis-36.html`、`tools/metalwork/analysis-cost-price-5.html`，均核心统计可用但宣称的分析/诊断/成本能力未实现）。承诺未实现另有：MM-H104（meta 称校核静/疲劳强度）、MM-H113（挤压与销长）。
- 安全：0 条（原 MM-H116/H119 的用户输入未转义均已由 `escXss` 修复，第 952 批真机复核零注入）；其余 8 页无 XSS、eval、allow-same-origin、明文存密或业务数据外传；全站模板 ttzz 脚本不单列。
- 复算：node 复算 45 钢 500/600°C 42.6/39.7 HRC、链速 7.722 m/s 与 F 712/12951/64753 N、双销 10.301/29.135 mm、制动能量 23.06/28.82/37.47 kJ、缺陷指数 212 与 19.20%、CV 4.41%/SD 2446.38，未落盘仓库；仅源码阅读，未开浏览器、未跑 `_build.py`/`run_gates.py`、未改 `tools/**` 与构建产物，未触碰 `plan/interaction-validity.md`。
- 去重说明：`strength-15`「按转速查表不看载荷」与 MM-H102（speed-26 额定功率表）同属选型表缺载荷维度但页面与机制不同；`temp-hardness` 的写死系数与 MM-H81（detector-stretch 写死阈值）同模式但页面不同，均按逐页口径单列。

## AA 批 · 金属·检测/硬度/模具（2026-11-04）

**逐页结论（8 页）**
- `tools/metalwork/analysis-simulator.html`：充填时间、Ballman 冷却时间可跑；但「流程/壁厚比」cm 与 mm 混算且用投影面积当流程长度，默认值小 10 倍（阈值 150 几乎不触发），模具温度是死输入，冷却时间可为负。
- `tools/metalwork/calc-feed.html`：n/Vf/f 公式正确，默认算例 1909.9 rpm、763.9 mm/min 复算一致；材料去除率 Q 算了不渲染，且公式缺切宽/切深、量纲是 mm²/min。
- `tools/metalwork/calc-gear-2.html`：直齿 d/da/df/db 正确；滚刀转速把工件分度圆当刀具直径（φ100 滚刀时高 2.1 倍），斜齿承诺未实现。
- `tools/metalwork/detector-21.html`：按材料/缺陷/厚度打分选法可跑；材料 6 档只分铁磁/非铁磁，strict 与 critical 同分，深度解析跑到探测器参数。
- `tools/metalwork/detector-23.html`：偏差与合格判定正确；IT 等级只按公差带绝对值、无视公称尺寸（0.039 mm @Ø50 判 IT4，实为 IT8），却注「按 GB/T 1800.1」。
- `tools/metalwork/detector-55.html`：18 项加权评分与 ★ 一票否决可跑；参考标尺把 <60% 的「不合格」划进「合格」带，引据表与深度解析均跑题。
- `tools/metalwork/detector-hardness.html`：三维加权可跑；厚度允许偏差基本失效、胶带法无输入恒判合格、各涂层合格线为写死常量却称依据国标，默认组合即判不合格。
- `tools/metalwork/detector-mold.html`：三轴偏差与空间偏差计算正确；ptName 存在 DOM XSS，「记录此点」是假功能，公式承诺的空间偏差判据未实现。

**问题条目**

| 页面 | 问题（含 tools/metalwork/<slug>.html:NN） | 编号 |
|---|---|---|
| tools/metalwork/analysis-simulator.html | 【高】流程/壁厚比量纲混算：`slender=(V/A)/h` 中 V 为 cm³、A 为 cm²、h 为 mm，默认 (200/100)/3=0.667；统一按 mm 为 (200000/10000)/3=6.67，偏小 10 倍。且 V/A 是平均厚度而非流程长度（公式框同时写「表面积」与「投影面积」），阈值 150 几乎永不触发（:111,115,230,234,240） | MM-H120 |
| tools/metalwork/analysis-simulator.html | 【高】模具温度 tmold 是死输入：被 parseFloat 并参与 isFinite 校验，但 Tmo 之后从未进入任何公式或输出；改 40/60/80 结果完全不变（:124,221-244） | MM-H121 |
| tools/metalwork/analysis-simulator.html | 【中】温度关系与正值未校验：Te>Tw+1.273(Tm−Tw) 时 ln 项为负，如 Tm=240/Tw=30/Te=300 → tCool≈−0.02 s；α=0 得 Infinity 显示「—」，V/A/h 为负也照算（:227-230） | MM-H122 |
| tools/metalwork/calc-feed.html | 【高】材料去除率 Q 算了不渲染：`var Q = vf*dia*0.02` 从未进入结果/导出/历史，公式框仍承诺「材料去除率 Q ≈ Vf×D×0.02」；该式缺切宽/切深、量纲为 mm²/min，与引据表 MRR=切宽×切深×进给 自相矛盾（:127,180,216,220-226） | MM-H123 |
| tools/metalwork/calc-gear-2.html | 【高】滚刀转速把工件分度圆当刀具直径：`n=1000*Vc/(π*d)` 中 d=m*z；m2/z24/Vc40 → 265.3 rpm，按 φ100 滚刀应约 127 rpm（高 2.1 倍）；若按工件转速理解，则「滚刀转速」标签又错。插齿同样用 d 算「转速」，与冲程数概念混淆（:176,228,238,248） | MM-H124 |
| tools/metalwork/calc-gear-2.html | 【假】英文副标题承诺 "for spur and helical gears"，但无螺旋角 β 输入，da=m(z+2)、df=m(z−2.5)、db=mzcos20° 全按直齿，斜齿几何未实现（:127,224-227） | MM-H125 |
| tools/metalwork/detector-21.html | 【高】材料 6 选项只分铁磁/非铁磁：铸件/锻件/管材/焊接件落入同一 isFerro 分支，打分与建议完全相同；检测等级 strict 与 critical 都只 +1 RT/+1 UT，两档无差异（:216,223-226,238-239） | MM-H126 |
| tools/metalwork/detector-21.html | 【中】深度解析整节为「焊接/探伤探测器参数对比」（灵敏度 0.5/1.0 mm、信噪比 20 dB、设备比对），与本页按材料/缺陷/厚度选检测方法无关，页面也无对应输入（:312-320） | MM-H127 |
| tools/metalwork/detector-23.html | 【高】IT 等级只按公差带绝对值查表、完全不看公称尺寸：0.039 mm 在 Ø50 按 GB/T 1800.1 为 IT8（30–50 mm IT8=39 μm），页面判 IT4；阈值 0.004/0.006/0.010… 不对应任何尺寸段的 IT01/IT0/IT1，属冒用国标验收（:214,236-247） | MM-H128 |
| tools/metalwork/detector-23.html | 【中】检测方式不影响判定：measureMethod 只改方法名与「不确定度 ±0.005/0.002/0.010 mm」文本，pass 仍只看 dev∈[lt,ut]；注文称不确定度应小于公差带 1/3~1/10，激光 ±0.010 对 0.010 公差带仍判合格（:215,233,248,258-259） | MM-H129 |
| tools/metalwork/detector-23.html | 【中】空值/负公差无校验：nominal/actual 空值经 `||0` 变 0；上偏差 −0.05、下偏差 +0.05 时 tolRange=−0.1 仍归为 IT01，pass 恒 false 并输出「尺寸偏大/偏小」建议，无参数错误提示（:224-247,260-268） | MM-H130 |
| tools/metalwork/detector-55.html | 【中】参考区间标尺把 <75% 全部标「合格」：bands 第三段 lo:null、hi:75、label 合格，覆盖了页面实际判「不合格」的 <60% 区间（:295-298,313） | MM-H131 |
| tools/metalwork/detector-55.html | 【中】引据表与深度解析均跑题：引据列 OEE/Weibull/MTBF，深度解析讲无损检测探测器「检出率/3σ 阈值/设备一致性」，本页是维修流程 18 项自查，无对应输入或输出（:160-172,349-362） | MM-H132 |
| tools/metalwork/detector-hardness.html | 【高】「厚度允许偏差 ±μm」基本失效：ratio≥1.0 一律 thickScore=100/thickPass=true，实测 52 vs 标准 40、容差 ±5（差 12 μm）仍输出「✓ 通过」；ratio>1.6（70 vs 40）也 pass；仅 0.85–1.0 段才用容差（:322-335,410） | MM-H133 |
| tools/metalwork/detector-hardness.html | 【高】胶带法（ASTM D3359）无对应等级输入：选 tape 时 crosscutRow 与 pulloffRow 都 display:none，代码仍读隐藏的 crosscutGrade（默认 0 级）→ 恒 100 分/合格，方法选择等于死选项（:137-150,289-315） | MM-H134 |
| tools/metalwork/detector-hardness.html | 【高】各涂层合格线是写死常量却称依据国标：reqPencil paint=HB、anode=2H、pvd=6H，reqHV paint=100…pvd=800，reqNano paint=1…pvd=20，均无标准来源；GB/T 9286/6739/4957 是划格/铅笔/测厚方法标准，不规定合格线，简介仍称「依据…综合判定合格性」（:124,349,357,364,525） | MM-H135 |
| tools/metalwork/detector-hardness.html | 【中】默认组合自相矛盾：pencilGrade 默认 6B（最软）、coatingType 默认 paint（要求 HB 指数 6），加载即显示「涂层质量良好（未达标）/不合格」，默认参数无法演示合格路径（:183,206,343,349-350） | MM-H136 |
| tools/metalwork/detector-mold.html | 【高】「记录此点」是假功能：addPoint 只把 `{name,dx}` push 进 pointList，该数组从不渲染、也不导出；CSV 导出的是 TBKit 历史表（输入+结果摘要），不是多点测量报告（:243-250,414-416） | MM-H138 |
| tools/metalwork/detector-mold.html | 【中】公式框与判定逻辑不符：说明称「各轴偏差均不超公差且空间偏差不超公差」才 PASS，代码 allPass=passX&&passY&&passZ，未判 dist；三轴各 0.019 mm、tol=0.020 → 空间偏差 0.0329 mm 仍判「合格」（:120,227-239） | MM-H139 |
| tools/metalwork/detector-mold.html | 【中】空值/零公差无校验：坐标用 `+value` 读取，清空理论/实测坐标得 0 仍参与计算；清空公差得 ±0.000 mm，任意偏差全判超差并给出刀具补偿建议，无「请输入」提示（:222-224,238-264） | MM-H140 |

**统计**
- 条数：20（高 10 / 中 9 / 假 1）；编号区间：MM-H120–MM-H140，续接 MM-H119，安全一条 MM-H137 已修复销账，其余不重号不跳号。
- 高优编号：MM-H120（流程比单位混算）、MM-H121（模具温度死输入）、MM-H123（Q 算了不渲染）、MM-H124（滚刀转速用分度圆）、MM-H126（材料/等级死选项）、MM-H128（IT 等级无视公称尺寸）、MM-H133（厚度容差失效）、MM-H134（胶带法恒合格）、MM-H135（写死涂层合格线冒充国标）、MM-H138（记录点假功能）。
- 假工具：0（核心直齿/评分/偏差计算均可用）；承诺未实现：1（MM-H125 斜齿）；冒用国标：2（MM-H128、MM-H135）。
- 安全：0 条（原 MM-H137 已于第 952 批改走 `ToolBox.escHtml` 并真机回放验证）；其余 8 页无 XSS、eval、allow-same-origin、明文存密或业务数据外传；全站模板 ttzz 脚本不单列。
- 复算：node 内存复算关键值（流程比 0.667 vs 6.67、铣削 1909.9 rpm / 763.9 mm/min / Q 305.6 mm²/min、滚齿 265.3 vs 127.3 rpm、IT8(30–50 mm)=39 μm、模腔空间偏差 0.0329 mm），未落盘仓库；仅源码阅读，未开浏览器、未跑 `_build.py`/`run_gates.py`、未改 `tools/**` 与构建产物，未触碰 `plan/interaction-validity.md`、`plan/units-factors.md`。
- 去重说明：`detector-hardness` 的写死涂层合格线与 MM-H81（detector-stretch 写死阈值）同属「冒充国标验收」模式但页面不同；`detector-23` 的 IT 表与 MM-H91（丝杠精度等级与导程脱钩）同为「查表值不随输入维度变化」但字段不同。

## AA 批 · 金属·锻造/压铸/糖度（2026-11-04）

**逐页结论（8 页）**
- `tools/metalwork/lifespan-1.html`：续航/Wh/DoD 公式正确，默认 10W/5000mAh/3.7V 复算 1.26h；铅酸选项自动写入单格 2V，12V 电池续航被低估 6 倍。
- `tools/metalwork/pinpaijiazhipinggujisuan.html`：乘数模型可跑，默认 4500 万元；年限系数可为负仍出负估值，引据 ISO 10668 却无折现，科技预设 13 亿 = 6.5 倍营收。
- `tools/metalwork/pressure-casting.html`：五法过滤可跑；批量档漏判，压铸/低压在中批量仍入选，首选恒为砂型，承诺的浇注/冷却工艺参数与压射比压未实现。
- `tools/metalwork/recorder-9.html`：钢种温度表与 t=k·δ+20 可跑；渗碳无渗层深度输入，保温时间只输出固定文案，核心卖点未实现。
- `tools/metalwork/resistance-2.html`：六法评分可跑；接头形式是死输入，板厚关系与厚度可互相矛盾，默认 3mm 低碳钢对接竟首选激光焊。
- `tools/metalwork/speed-itinerary.html`：行程/走刀/时间可跑；每刀往复数把工件长度当横向宽度，200×100 板时间偏大一倍，材料去除量算了不渲染。
- `tools/metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi.html`：第二段覆盖后 IT 可算（D50/IT7=0.0273 mm）；用实际 D 而非尺寸段几何均值偏高 9%，形位公差取 IT/2 无依据，⇄ 互换即报错。
- `tools/metalwork/temp-forging.html`：查表温度正确；10kg/φ50 钢件加热仅 8 min、保温 2 min，低约一个数量级，温度条满量程恒按 1300℃。

**问题条目**

| 页面 | 问题（含 tools/metalwork/<slug>.html:NN） | 编号 |
|---|---|---|
| tools/metalwork/lifespan-1.html | 【中】铅酸电池选项自动把电压写成 2 V（`BAT_VOLT.lead=2`），但选项标签是「铅酸电池(12V/单格2V)」；12V/100Ah 电池续航 81.6h 被算成 13.6h，低估 6 倍，用户需手工改回 12V（:156,220,239-242） | MM-H141 |
| tools/metalwork/pinpaijiazhipinggujisuan.html | 【中】年限系数只校验 >0（HTML `min=0.5` 仅约束步进器），键盘输 −1 得负品牌价值且仍标「初创品牌」；利润率控件 `max=80` 但校验放行到 100（:137,145,232,236,238,242-249） | MM-H142 |
| tools/metalwork/pinpaijiazhipinggujisuan.html | 【假】引据表称 ISO 10668「收益法/特许权使用费节省法」，实算却是「利润×乘数×年限×份额」自定义模型、全程无折现；科技预设 2 亿营收×20%×10×1.3×2.5 = 13 亿（6.5 倍营收，合计 32.5 倍利润），冒用国标口径（:127,186-199,241-242,436） | MM-H143 |
| tools/metalwork/pressure-casting.html | 【高】批量维度漏判：压铸/低压铸造 `batch:'mass'`，代码只排除 `batch==='single'`，选「中批量」时两者仍进入可选列表并被推荐，与页面「压铸适合薄壁大批量、小批不适合」自相矛盾（:167,222-223,238-239,491） | MM-H144 |
| tools/metalwork/pressure-casting.html | 【中】首选恒为砂型：`Object.keys(METHODS)` 顺序把 sand 放首位，凡铁/钢/铝/铜命中即取 `matched[0]`；铝合金 5kg/5mm/中批的首选仍是砂型而非压铸/金属型，排序未按精度/批量/成本评分（:233,240,248） | MM-H145 |
| tools/metalwork/pressure-casting.html | 【假】简介与 FAQ 承诺输出「浇注、冷却等工艺参数」，引据表列压射比压、Chvorinov 凝固时间、浇注系统比，页面均未计算；且 ISO 8062-3（铸件尺寸公差）被标为压射比压与浇注系统比的出处（:127,130,182-195,550） | MM-H146 |
| tools/metalwork/recorder-9.html | 【高】渗碳工艺无渗层深度输入：`calcSoaking` 对渗碳分支恒返回字符串「按渗层深度估算（约 0.12~0.15 mm/h）」，从不按深度计算分钟数，新建作业的保温时间也没有数值；公式框却写「保温时间随渗层深度确定」（:127-128,401-405,443） | MM-H147 |
| tools/metalwork/recorder-9.html | 【中】目标温度与记录温度均无范围校验：目标可输 0/负数/远超材料区间仍进入曲线与统计，`createJob` 只拦 ≤0；记录温度任意值均接受（:152,411,450-453） | MM-H148 |
| tools/metalwork/resistance-2.html | 【高】接头形式 `joint` 完全不参与过滤与评分：唯一使用处是一个空 `if` 块（无任何语句/赋值），对接/搭接/T形/角接结果与首选方法完全相同，属死输入（:147-152,231,239-241,279-291） | MM-H149 |
| tools/metalwork/resistance-2.html | 【高】默认 3mm 低碳钢对接评分：激光 50+20+15=85 > TIG 80 > 电阻 75，首选激光焊，与页面「薄板≤3mm 优先 TIG/电阻焊」及成本「低」优先的口径相反；成本「高」在评分中完全不扣分（:274,279-290） | MM-H150 |
| tools/metalwork/resistance-2.html | 【中】板厚关系 `plateType` 与厚度 t 独立输入：t=3 可选「厚板」、t=50 可选「薄板」，过滤按 t、评分按 plateType，同一 t 可得不同首选；`resetAll` 又把 plateType 设为 medium，而页面初始/预设为 sheet（:156-161,284-286,454） | MM-H151 |
| tools/metalwork/resistance-2.html | 【假】简介承诺推荐「工艺参数」，结果只有方法/保护气体/质量/成本，无电流、电压、气流量；引据表的热输入 Q、碳当量 CE、预热温度三项均未实现（:128,183-197） | MM-H152 |
| tools/metalwork/speed-itinerary.html | 【高】每刀进给往复数用 `ceil(L/f)`，把工件长度 L 当作横向宽度；进给量是 mm/往复行程的横向步距，正确应为 `ceil(宽度/f)`。200×100 板应为 400 往复，页面算 800（时间 6.4 vs 3.2 min），长度/宽度比越大偏差越大（:245-247,259） | MM-H153 |
| tools/metalwork/speed-itinerary.html | 【高】材料去除量 `materialRemoval` 算了不渲染、不进导出，公式框仍承诺；且 `L×余量×切深×0.001` 量纲错误（缺宽度，正确体积为 L×宽×余量）（:127,248） | MM-H154 |
| tools/metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi.html | 【中】IT 用实际直径 D 而非尺寸段几何均值：D50 算 IT7=0.0273 mm、IT8=0.0427 mm，GB/T 1800.1 的 30–50 段为 0.025/0.039 mm，偏高约 9%；公式框仅写「≈」，未提示应按段均值（:126,564-566） | MM-H155 |
| tools/metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi.html | 【中】圆度/同轴度建议直接取 `IT/2`：两项形位公差本属独立公差项目、同一数值无标准依据，页面却作为「建议」输出（:567） | MM-H156 |
| tools/metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi.html | 【中】⇄ 互换按钮把孔径 D 与 IT 等级互换（50↔7），第二段校验随即判「IT 等级需为 5–10 的整数」，常规输入一按即报错；重置按钮已被第二段覆盖为 50/7，但互换未同步（:131,495-501,575） | MM-H157 |
| tools/metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi.html | 【中】孔径 D 无正值校验：只判 `isFinite`，输 −50 仍按 cbrt 得负标准公差 −0.0273 mm 并正常渲染（:559,562-566） | MM-H158 |
| tools/metalwork/temp-forging.html | 【高】加热/保温时间量级错误：`ceil(0.5W+0.05d)` 把 kg 与 mm 直接相加，10kg/φ50 钢件仅 8 min；保温 `ceil(0.2W)` 仅 2 min。φ50 钢件常规加热约 30–60 min、保温 ≥30 min，页面低约一个数量级，且与截面/装炉条件脱钩（:127,226-227,243-244） | MM-H159 |
| tools/metalwork/temp-forging.html | 【中】温度条满量程恒取 `Math.max(maxHeat,1300)`，而所有 maxHeat≤1300 故恒为 1300：铝合金 490℃ 的「最高加热」条只占 38%、470℃ 始锻占 36%，视觉上远低于满量程，图表失去材料相对意义（:247-254） | MM-H160 |

**统计**
- 条数：20（高 7 / 中 10 / 假 3 / 安全 0）；编号区间：MM-H141–MM-H160，续接 MM-H140，不重号不跳号。
- 高优编号：MM-H144（压铸/低压批量档漏判）、MM-H147（渗碳保温时间假功能）、MM-H149（接头形式死输入）、MM-H150（默认首选激光焊）、MM-H153（长度当横向宽度）、MM-H154（材料去除量算了不渲染）、MM-H159（加热/保温时间低一个数量级）。
- 假工具：0（8 页核心查表/公式均可用）；承诺未实现：3（MM-H146 铸造工艺参数、MM-H152 焊接工艺参数、MM-H147 渗碳深度估算）；冒用国标：2（MM-H143 ISO 10668、MM-H146 ISO 8062-3）。
- 安全：0 条；8 页均未发现 XSS、eval、allow-same-origin、明文存密或业务数据外传；`recorder-9` 备注经 `escHtml` 转义，`tangxue` 历史恢复仅接数值参数，全站模板 ttzz 脚本不单列。
- 复算：node 内存复算 IT7/IT8(D50)=0.0273/0.0427 mm vs 段均值 0.025/0.039 mm、刨削 800 vs 400 往复与 6.4/3.2 min、锻造加热 8 min/保温 2 min、品牌默认 4500 万与科技预设 13 亿、铅酸 2V 13.6h vs 12V 81.6h，未落盘仓库；仅源码阅读，未开浏览器、未跑 `_build.py`/`run_gates.py`、未改 `tools/**` 与构建产物，未触碰 `plan/interaction-validity.md`、`plan/units-factors.md`。
- 去重说明：`speed-itinerary` 的长度/宽度维度混用与 MM-H120（流程/壁厚单位混算）同为维度错配但页面与字段不同；`temp-forging` 的固定 1300 满量程与 MM-H131（detector-55 标尺区间错位）同为图表刻度失真但页面不同；`tangxue` 的 IT 近似与 MM-H128（detector-23 IT 表无视公称尺寸）同为 IT 查表口径问题但机制不同，均按逐页口径单列。

## AB 批 · 金属·对比计算器族（2026-11-04）

> 页面名后的「（死键 N）」= 该页第三层英文词典（`i18n/tools/en/<ind>/<slug>.json`）高优先死键数（来源 `plan/i18n-dead-keys.md`）；各线改本页时顺手清理，本批不修英文。

**族矩阵（4 页）**

| 页面 | 输入 | 主算 / 输出 | 默认态复算 | 族内定位 |
|---|---|---|---|---|
| tools/metalwork/tester-19.html（死键 1） | 电缆类型、绝缘电阻(MΩ·km)、测试温度、导体电阻(Ω/km)、标称截面、U₀、长度 | 绝缘/导体/耐压三项验收报告 | PVC 70mm²、500 MΩ·km、20℃、0.268 Ω/km、0.6kV、100m → IR 500≥0.5、导体 0.268≤0.2948、耐压 3.5kV/15min → 综合合格 | 独立检测计算器（共用 TBKit 外壳，非 A/B 对比） |
| tools/metalwork/thread.html（死键 1） | 螺纹类型、直径、螺距、材料、内外、批量 | 中径/小径/底孔 + 工艺方案表 | M10×1.5 碳钢外螺纹单件 → d2 9.026、d3 8.160、n 1910 rpm，单件档仅车削一项且为首选 | 独立工艺推荐器 |
| tools/metalwork/wushua-zhinengyuqingliangduibijisuanqi.html（死键 0） | 无刷评分、轻量评分 | 综合差距、推荐侧重、权重比 | 90/72 → 差距 18.0、无刷路线优先、55.6% | A/B 双评分模板 |
| tools/metalwork/zhineng-duogongnengyunaiyongduibijisuanqi.html（死键 0） | 智能评分、耐用评分 | 同上 | 85/78 → 差距 7.0、智能路线优先、52.1% | 与 wushua 页同源，仅换变量与文案 |

族矩阵结论：4 页并非同一业务族，后两页才是「智能对比计算器」；前两页只是同用 TBKit 双列表单外壳的独立计算器。后两页除名词替换外 DOM、函数、历史逻辑完全同构，故同类缺陷按页各记。

**逐页结论**

- `tools/metalwork/tester-19.html`：默认态可跑并判「综合合格」；电缆长度是死输入、导体电阻未按温度折算，两项涉及输入口径待产品裁断。
- `tools/metalwork/thread.html`：默认 M10×1.5 的几何、转速与方案表可跑；螺纹类型只改规格文案，梯形/管/统一螺纹仍套公制 60° 系数；首选方案恒为车削，与「大批量优先滚压」自相矛盾。
- `tools/metalwork/wushua-zhinengyuqingliangduibijisuanqi.html`：`abs(A−B)`、`A/(A+B)`、A 大则推荐无刷三项均真实实现，默认 90/72 正确。
- `tools/metalwork/zhineng-duogongnengyunaiyongduibijisuanqi.html`：与 wushua 页完全同构，默认 85/78 正确。

**问题条目**

| 页面 | 问题（含 tools/metalwork/&lt;slug&gt;.html:NN） | 编号 |
|---|---|---|
| tools/metalwork/tester-19.html | 【中】电缆长度是死输入：:346 读取 `len` 后，报告与判定均未再使用（:366-367 只列 IR/cr），绝缘电阻直接按输入的 MΩ·km 与限值比较，100 m 与 300 m 结果完全相同；若输入是整根电缆实测 MΩ，应按 `R×L(km)` 归一后再比。:346、:351、:366 | MM-H162 |
| tools/metalwork/tester-19.html | 【中】导体电阻未做温度折算：报告表头写「导体电阻(20°C)」，但 :354 直接用实测 `cr` 对 20℃ 限值，`temp` 只用于绝缘电阻分支；35℃ 实测 4.85 Ω/km 与 20℃ 的 4.61 会被当成同一口径。:342、:354、:367 | MM-H163 |
| tools/metalwork/thread.html | 【高】螺纹类型不参与几何计算：`threadType` 只在 :262 拼规格字符串，:250-251 恒用公制 60° 系数；Tr40×7 得 d2 35.453 mm（正确 36.5）、d3 31.412 mm（正确 33.0），统一/管螺纹同样错配，还会输出 `10"-1.5UNC`、`G10/1.5` 这类无意义规格。:221、:250-251、:262、:455 | MM-H165 |
| tools/metalwork/thread.html | 【中】首选方案恒为车削：`methods` 固定先推车削（:234），仅大批量追加滚压（:236），:248 取 `methods[0]`；选「Tr40×7 大批量」仍推荐车削，与页内「外螺纹大批量优先滚压/搓丝」相反；内螺纹大直径同理仍首选攻丝。:234-248、:455 | MM-H166 |

**统计**
- 条数：4（高 1 / 中 3 / 假 0 / 安全 0）；编号区间 MM-H161–MM-H170，续接 MM-H160，不重号不跳号。
- 高优编号：MM-H165（螺纹类型不改几何）。
- 假工具：0（4 页主算均可跑）；承诺未实现：0；冒用国标：0（tester-19 引 GB/T 3048 与判定表一致，问题在修正公式而非冒用）。
- 安全：0 条；4 页无 `eval`/`new Function`/`allow-same-origin`/`document.write`/明文存密/页面自有网络外传；历史值仅接数值或 `escHtml` 后的时间串，未形成可控 HTML 注入；公共模板 ttzz 脚本不单列。
- 复算：node 内存复算温度因子 35℃ 0.3536 vs 2.8284、5℃ 2.8284 vs 0.3536，Tr40×7 的 d2/d3 35.453/31.412 vs 36.5/33.0，M10×1.5 的 d2 9.026/d3 8.160/n 1910 rpm，对比页 90/72→18.0/55.6%、85/78→7.0/52.1%，未落盘仓库；仅源码阅读，未开浏览器、未跑 `_build.py`/`run_gates.py`、未改 `tools/**` 与构建产物，未触碰 `plan/interaction-validity.md`、`plan/units-factors.md`、`plan/input-parse-dup.md`。
- 去重说明：tester-19 的温度修正方向错误与既有「查表值不随输入变化」类不同，属公式符号错误，单列；thread 的类型死选项与 MM-H126（材料/等级死选项）同属「下拉只改文案」，但本页还叠加几何错算，按页面单列；两个对比页为同一模板缺陷，按逐页口径各记一条。
