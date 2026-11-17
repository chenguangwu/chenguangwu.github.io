# 自然科学 · 基础计算（math/science/statistics/geometry/encode 数学系，~230 页）

## 功能缺陷
- 统计页缺「数据粘贴→自动识别分布推荐」（描述统计后给分布拟合建议）。
- 排列组合页缺「大数模式说明」（已转科学计数，补「精度提示」文案）。

## 优化点
- S3 分步：概率/分布页加查表过程可视化（z→Φ 的面积图）。
- S6 智能输入：单位换算页（general/convert 系）标杆试点（G06-S6）。

## 受影响范围
- tools/math/（41 页）、tools/statistics/（51 页）、tools/science/ 计算类（93 页中 ~60 计算页）、tools/geometry/、tools/general/convert 系、tools/encode 数学系（~230 页合计）

## 进度
- 🔴 待开发

## 2026-11-06 科学工具静态续审（清单 606–613）

- `tools/science/physics-constants.html:236-260,276-281,328-340`：SMS-129（exp 数量级写 0，含 c/F/R∞/atm/H₀ 五项）与 SMS-130（玻尔兹曼常数(摩尔) R/Nₐ 重复行）已于 2026-11-17 真机销账——exp 改 8/4/7/5/1 与卡片科学计数一致、重复行删除；搜索、分类、复制及筛选导出路径存在。SMS-128（分类维度错置）属产品语义裁断，保留待决。
- `tools/science/quadratic-equation.html:366-367,293`：旧 SMS-136 已改为相对阈值 `epsD=1e-12×max(b²,|4ac|,1e-300)` + 小数 `toExponential(6)`，第 962 批真机确认（`scripts/_verify_printing_travel_regress_962.mjs`）：x²−5x+6 两根 2/3、判「两不等实根」。SMS-137 负 a 共轭根符号已于 972 批修正（im 取绝对值，a=−1 得 ±i），结果趋势仍解析以 `Δ` 开头的文本（SMS-151 共用模板问题）。

## 2026-11-06 数学工具静态续审

- `tools/math/complex-number.html:297-317`：输入实时变化仅重算极坐标和图，先点运算后再改输入，运算输出仍为旧结果；清空实部或虚部被当作 0，单目运算亦会给结论。
- `tools/math/formula-calculator.html:310-340,345-393,411-418`：搜索、分类、卡片复制和筛选 CSV 的代码路径存在；表格随 `renderList` 包装刷新。仅静态阅读，未验证公式专业正确性、交互执行或导出文件。

## 2026-11-03 审计补充

### 留存优化：压力换算口径对照（低，建议）
- 证据：同页 `:447-464,467-484` 已并列单位结果及海拔压力参考曲线。
- 影响：同页；方案：提供常见轮胎表压与绝压示例，并明确大气压力假设，防止用户误把参考值视为实测。

## 2026-11-03 续查（并行批 F）

### 留存优化
- 统计检验页（t/F/卡方/ANOVA）把「样本量、方差、自由度」的前置条件做成可见校验清单，结果区同步给出 p 与效应量（η²、Cohen's d），减少「只给统计量、不给结论」的往返。
- 卡方与比值比页补「结果可带走」的标准化段落：χ²/df/p、OR/95%CI/校正标记，避免用户再手工查表。
- SI 换算页增加常用组合（1 fm→m、1 nm→m、1 μg→g）与「极小值不归零」的显示策略说明。
- 有效数字页给出「半值修约规则」与末尾 0 保留选项，示例覆盖 1.005、1.015。

### 续查覆盖
- `tools/statistics/one-sample-t-test.html`
- `tools/statistics/f-test-variance.html`
- `tools/science/si-unit-converter.html`
- `tools/statistics/chi-square-test.html`
- `tools/statistics/odds-ratio.html`
- `tools/science/significant-figures.html`
- 本轮共 8 页；仅阅读源码并用 node 内存复算，未做浏览器、EN 态、移动端与门禁验证。

## T 批 自然科学覆盖（2026-11-04）

- 同轮复核：SMS-19 非数字静默丢弃已修，`5,7,9 / 6,bad,8 / 7,9,11` 报第 2 组第 2 项无效；SMS-20 每组仅一个观测及组内平方和为零已分别报错，不再给出 p 值或显著性结论。

### 覆盖清单（T 批 自然科学 · 8 页，初次审计历史快照；当前状态以本清单修订说明为准）

- `tools/science/equation-balancer.html`：SMS-21/22 已修——前导系数剥离后重算并提示，欠定方程输出一组系数且明确标注「非唯一解」，公式说明同步；核心为真 RREF 求解（非硬编码示例），KMnO4+HCl、Cu+HNO3、Ca(OH)2+H3PO4、Fe2(SO4)3+NaOH、CuSO4·5H2O 分解等经典式均配平正确。括号不配对、离子电荷（`H+`、`Fe3+`）不支持，`H+ + OH- = H2O` 直接报「无法识别字符」。
- `tools/science/ph-calculator.html`：SMS-11/12/13 已修——无效输入先清旧报告再 toast，`pH=−log10[H+]`、`pOH=14−pH`、HH 方程实现无误，空值与 pH=0 区分、酸碱分级阈值与磷酸缓冲 pKa 标签一致。无温度/Kw 输入，公式说明已声明按 25 ℃。
- `tools/science/molar-mass-calculator.html`：SMS-9/10 已修——括号类型栈匹配、结晶水多段系数独立、正整数下标校验；元素表覆盖 Mn/Cr/Ni 等 118 种，`KMnO4`/`K2Cr2O7`/`NiSO4` 分别约 158.032/294.181/154.749 g/mol。
- `tools/science/p-value-calculator.html`：1 条（SMS-14 中）。`normalCDF`/`betaI`/`tCDF`/`gammp` 数值与参考值一致（t=2.5,df=20 双侧 0.021234；χ²=9.49,df=4 上尾 0.050002；Z=1.96 双侧 0.049996）；问题仅为 df 截断。df>200 改走正态近似（t=2.5,df=201 得 0.012419，t 分布精确值约 0.0132，约 6% 偏差），属常见近似，未单列条目。
- `tools/science/effect-size-calculator.html`：SMS-15 已修——双样本 n 严格整数校验（拒绝小数/空值），小数停算提示；SD≤0 单独提示；公式框口径跨 3 源同步。
- `tools/science/sample-size-calculator.html`：SMS-16 已修——总体 N 非空即要求正整数，N=50.5/N=0 停算提示，不再静默截断或当无限总体。
- `tools/science/wire-gauge-converter.html`：SMS-158 已修——铜电阻 `ρ=0.0172 Ω·mm²/m` 按 `R=ρ×1000/A` 修正（Ω/km），主结果/明细/参考表/导出 CSV 同源 ×1000；派生 Ω/1000ft 与 100m 压降联动正确。AWG24=84.01 Ω/km、AWG20=33.23 Ω/km、AWG0=0.32 Ω/km。
- `tools/science/torque-converter.html`：SMS-155 已修——导出 CSV 八行数值后缀按各自单位符号（N·m/kN·m/lb·ft/lb·in/kgf·m/gf·cm/ozf·in/dyn·m），表头改为通用 Value，不再全部标 N·m。
- `tools/science/work-done.html`：SMS-160 已修——预设倍率与结果自洽（默认 F=50,d=10→500 J；「2×」改 F=100,d=10→1000 J；「0.5×」改 F=25,d=10→250 J）。
- `tools/science/tide-height-estimator.html`：SMS-152/153/154 已修——太阳引潮项 `abs(sin)` 修正相位（春分/秋分 0%、夏至/冬至 46%）；默认日期改本地时区 `__tideLocalDate()` 消除东八区凌晨错位；纬度越界/空值停算提示。verify 潮差 expect 同批由 0.86 更新为 1.08 m。
- `tools/science/xianxingfangchengzuqiujie-2yuan-3yuan.html`：SMS-161/162 已修——历史按索引读 `vals` 真恢复（三元签名显示实际系数）、保存改 600ms 防抖+去重；预设带 `__xhMode` 在 after 调 `setMode` 真正切元数，「默认参数」补全 12 项。
- `tools/science/chi-square-calculator.html`：SMS-17/18 已修——零观测值与非法项过滤（`10,0`→χ²=10、`bad` 报第 3 项错误）、自由度按行列数计算（2×2 得 df=1）、2×2 独立性预设期望由误填的均分 25,25,25,25 改为边际值 22.5,27.5,22.5,27.5（χ² 由 10 修正为 9.09）。χ²=Σ(O−E)²/E 与上尾 CDF 正确（默认 30,25,20,15,10 → χ²=12.5、df=4、p=0.013996）。
- `tools/science/anova-calculator.html`：2 条（SMS-19 中、SMS-20 中）。SSB/SSW、dfB=k−1、dfW=N−k、F 与上尾 p 正确（默认数据 F(2,12)=25.554、p=4.73e-5）；问题为非数值静默丢弃与 dfW=0 未拦。注：SMS-7 的同名问题在 `tools/statistics/one-way-anova.html`，与本页实现不同（本页直接由原始观测算 SSW，无 `(n−1)s²` 负值缺陷）。

- 声明：本轮仅通读源码并用 node 在 `/tmp` 复刻各页 `calc()` 实算（未开浏览器、未跑 `_test_static`/`run_gates`、未做线上或英文态/CDN 验证），未修改任何工具页、构建产物或仓库文件。新增 14 条：高 1（SMS-9），中 13（SMS-10～SMS-22）。

## U 批 · 统计计算余量（2026-11-04）

- 同轮复核：SMS-25 已修，百分位 `50,150,-5` 明确提示 150 越界并中止。

### SMS-26 T 分数页公式框承诺「单样本 t 统计量与 df=n−1」，但页面无 n 输入、只做 T=50+10Z 换算（中，承诺未实现）
- 问题：公式框首条列 `t=(x̄−μ₀)/(s/√n)（单样本）`，引据表也列 `df=n−1` 作为「t 统计量/自由度」；但页面只有 X、M、SD 三个输入，没有配对数 n，主算只输出 `Z=(X−M)/SD` 与 `T=50+10Z`，从不输出 t 统计量或 df。按首条公式理解的使用者会把 X/M/SD 当作 t 检验输入，实际拿到的是 T 分数。
- 证据：`tools/science/t-score-calculator.html:161`（公式框并列两个定义）、`:242-247`（引据表 t 统计量、df=n−1）、`:165-167`（仅 X/M/SD 输入，无 n）、`:295-307`（实际只算 Z 与 T）。
- 复现：X=85、M=70、SD=10 → 实际 `Z=1.5`、`T=65`；若按首条公式当作单样本 t 检验，缺少 n 无法计算。期望页面只声明 T 分数定义，或补 n 输入并单独输出 t 与 df。
- 影响：`tools/science/t-score-calculator.html`；公式说明与实现口径不一致，统计检验场景会误读输出。
- 方案：公式框只保留 `T=50+10Z`，把单样本 t 统计量移入说明并注明「本页不计算」；或新增 n 输入并分别输出 t/df 与 T 分数。
- 假工具：否（T 分数换算正确）。

- 同轮复核：SMS-29 常量序列已明确提示方差为 0、Pearson r 无定义；SMS-30 的非法项已拒绝，X=`1,2,3,4`、Y=`2,4,bad,6,8` 提示 Y 第 3 项错误。

### 覆盖清单（U 批 统计计算余量 · 10 页，初次审计历史快照；当前状态以复核记录为准）

- `tools/science/mode-calculator.html`：SMS-23 已修——逐项严格解析（整 token 正则），非法项指出第几项并停算；旧「过滤非法项」承诺跨 5 源同步为停算口径。SMS-24 千分位与极小值口径保持。
- `tools/science/median-calculator.html`：0 条。奇偶中位数正确（`1,2,3,4` → 2.5、`5` → 5、`3,1` → 2）；仅共享 `parseData` 静默过滤非法项，但公式说明已声明「无法解析的项按无效值过滤」，不单列。
- `tools/science/quartile-calculator.html`：0 条。R-7 `pos=(n−1)p` 线性插值、IQR 与 1.5×IQR 栅栏正确（`1,2,3,4` → Q1=1.75/Q2=2.5/Q3=3.25、IQR=1.5；`1,2,3,4,100` 检出 100）。
- `tools/science/percentile-calculator.html`：1 条（SMS-25 中）。R-7 分位数与 `i/(n−1)` 排名口径一致（`1..10` 的 P50=5.5）；`n=1` 排名分母为 0 已在公式说明中声明，不计缺陷。
- `tools/science/t-score-calculator.html`：1 条（SMS-26 中）。`T=50+10Z`、`Φ(Z)` 百分位与分档判断正确（X=85/M=70/SD=10 → T=65、前 6.7%）。
- `tools/science/variance-calculator.html`：SMS-27 已修——严格解析拒绝非法项；替代公式按相对误差检测浮点消减，大数样例不再误标「与上方一致」，改提示「请以主结果为准」。SMS-28 极小值口径保持。
- `tools/science/correlation-calculator.html`：2 条（SMS-29 中、SMS-30 中）。Pearson r 与 r² 正常数据正确（`1,2,3,4` vs `2,4,6,9` → r=0.9944）。
- `tools/statistics/cramers-v.html`：SMS-32 已修——列联表四格要求非负整数，小数/负值/行列合计为 0 停算并清空；面板从 `#result` 分离，避免 setResult 删除图表。
- `tools/statistics/relative-risk.html`：SMS-33 已修——非负整数校验；移除 c 误判分母守卫，区分 a=0 且 c=0 报 0/0 未定义、仅 c=0 报无穷大；__rrChart 与判读层同步停绘清空。

- 声明：本轮仅逐页读源码并用 node 在 `/tmp` 复刻各页 `calc()` 实算（未开浏览器、未跑 `_build.py`/`_test_static`/`run_gates`、未做线上与英文态验证），未修改任何工具页、构建产物或仓库文件。新增 11 条：高 2（SMS-23、SMS-31），中 9（SMS-24～SMS-30、SMS-32、SMS-33）；中位数、四分位两页未发现计算类缺陷。

## V 批 · 物理/工程计算（2026-11-04）

- 同轮复核：SMS-36/37 已全部修（含正向求 Vout 的 `||0` 兜底，第 1003 批清账）。`tools/science/voltage-divider-calculator.html` 对目标电压越界/为 0、正向 Vin/R1/R2 空值或非正均提示并清空结果。

- 同轮复核：SMS-42 已修，`tools/science/coulomb-force.html:267-274` 对力和场强取绝对值并标明吸引或排斥；实跑 q₁=1 μC、q₂=−1 μC、r=0.1 m，力大小为 0.8988 N、方向为相互吸引。

### 覆盖清单（V 批 物理/工程 · 8 页，初次审计历史快照；当前状态以复核记录为准）

- `tools/science/coulomb-force.html`：1 条（SMS-42 中）。`F=kq₁q₂/r²`、`E=kq₁/r²`、`U=kq₁q₂/r` 的量纲与数值正确（默认 1/1/0.1 → 0.8988 N、898800 N/C、0.0899 J）；`r=0` 由守卫拦截，异号电荷负号问题除外。
- `tools/science/fraction-calculator.html`：2 条（SMS-34 高、SMS-35 中）。正常整数四则与约分正确（`1/2+1/3=5/6`、`4/8→1/2`、`1/2÷1/3=3/2`）；带分数 `-5/3 → -1 2/3` 正确。
- `tools/science/logic-gate-simulator.html`：2 条（SMS-43 中、SMS-44 中）。8 个门的真值表与 `fn` 全部正确（AND/OR/NOT/NAND/NOR/XOR/XNOR/BUFFER）；真值表高亮按 `data-row` 匹配正确；问题在组合链预设文案与开关 UI 同步。
- `tools/science/pcb-trace-width.html`：2 条（SMS-39 中、SMS-40 中）。公式、单位（`oz→1.378 mil`、`mil→0.0254 mm`、`oz→0.035 mm`）与截面积一致（默认 2 A/10°C/1 oz 外层 → 30.76 mil / 0.781 mm / 0.0273 mm²）；问题为参考表数值与零值早退。
- `tools/science/hookes-law.html`：0 条。`F=kx`、`U=0.5kx²`、`kx²=2U` 正确（100 N/m · 0.2 m → 20.0 N、2.0000 J、4.0000 J）；`k=0` 时「劲度系数倒数」显示 1e9 m/N 系公式框自述的 `1÷max(k,10⁻⁹)` 口径，空值按 0 兜底亦已在公式框声明，故不计缺陷。

- 声明：本轮仅逐页读源码并用 node 在 `/tmp` 复刻各页主算（含组合链语义与单位换算），未开浏览器、未跑 `_build.py`/`_test_static`/`run_gates`、未做线上与英文态验证，未修改任何工具页、构建产物或仓库文件。新增 11 条：高 2（SMS-34、SMS-36），中 9（SMS-35、SMS-37～SMS-44）；8 页中胡克定律页未发现计算类缺陷。

## W 批 · 统计计算 II（2026-11-04）

### 覆盖清单（W 批 统计计算 II · 8 页，原审计快照）

> 以下为历史覆盖情况，并非当前缺陷状态；SMS-45/46 与本批其余已修项不再适用，SMS-51 的已修和残留部分以上方 2026-11-06 复核为准。

- `tools/statistics/sample-variance.html`：0 条（SMS-45 已修）。`s²=Σ(x−x̄)²/(n−1)` 正确（默认 `2,4,4,4,5,5,7,9` → 均值 5.0000、s²=4.5714、s=2.1381）；空格/换行输入主算与附加层解析不一致一项已修（统一 `__svList()` 严格解析、n<2 停算清空）；另发现并修复四面板嵌在 `#result` 内被主算覆写删除的同类假功能。本页与 `variance-list.html` 功能高度重复（同为「样本方差计算器」），属内容重复，未按计算缺陷单列。
- `tools/statistics/variance-list.html`：本页已合并为指向 `sample-variance.html` 的重定向存根（仅 998 字节、含 `TOOLBOX-REDIRECT`），SMS-46 及其复核结论均已过时、不再适用。
- `tools/statistics/range-stat.html`：1 条（SMS-47 中）。默认 `2,4,4,4,5,5,7,9` → R=7.00、N=8、均值 5.0000 正确；全部相同 → R=0.00 正确；问题为换行/分号切分与非法项计入 N。
- `tools/statistics/z-score-calc.html`：1 条（SMS-48 中）。`z=(x−μ)/σ`、偏离量、`μ+1.96σ` 与 `Φ(z)` 百分位正确（115/100/15 → z=1.000、129.400；z 基准表 -3～3 百分位单调）；问题为负 σ 与早退留旧图表。
- `tools/statistics/standard-error.html`：1 条（SMS-49 中）。`SE=σ/√n` 与 1.96/2.576 半宽正确（15/36 → 2.5000、4.9000、6.4400）；「SE 减半所需 n = 4n」正确；问题为负 σ、σ=0 的 SE/σ=NaN 与早退留旧表。
- `tools/statistics/statistics-16.html`：0 条（SMS-50/51/52 已修）。最小二乘斜率/截距/预测在正常 5 对数据上正确（默认 → a=2.0600、b=-0.0600、ŷ=12.3000；`a` 与引据 `Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²` 等价）；原 x 全同、缺值残留、r/R² 未展示三项已修。另：本页 deep-dive 标题与正文为「统计功效与效应」，与线性回归主题不符（内容错配，属文案层面，未单列缺陷）。
- `tools/statistics/statistics-7.html`：0 条（SMS-53 负值守卫、SMS-54 恒定数据判定卡均已修）。总体中心矩 `g₁=m₃/m₂^1.5`、超额峰度 `m₄/m₂²−3` 正确（默认 10 值 → 偏度 1.3127、峰度 1.0559；均匀 1～10 → 偏度 0、峰度 -1.2242）；负数据被通用守卫拒绝一项已修（SMS-53：清空负值受限集合），恒定数据判定卡错误一项已修（SMS-54：方差为 0 停答并清空面板）。另：本页 deep-dive 同样为「统计功效与效应」，与偏度峰度主题不符（内容错配，未单列）。
- `tools/statistics/percentile-rank.html`：0 条（SMS-55 已修）。`PR=(L+0.5E)/N×100` 正确（默认 8 值、70 → 43.75%；最高 90 → 93.75%；目标 100/40 → 100.00%/0.00% 边界正确）；空格输入主算取首值与明细表矛盾一项已修（主算/明细/曲线同源解析）。

- 声明：本轮仅逐页读源码并用 node 在 `/tmp` 复刻各页主算（含 `split`/`parseList` 解析差异、`toFixed` 输出与守卫早退路径），未开浏览器、未跑 `_build.py`/`_test_static`/`run_gates`、未做线上与英文态验证，未修改任何工具页、构建产物或仓库文件。新增 11 条：高 0，中 11（SMS-45～SMS-55），承诺未实现 1 条（SMS-52），安全 0 条，假工具 0 条；8 页均完成覆盖。

## X 批 · 统计相关/检验（2026-11-04）

### 覆盖清单（X 批 统计相关/检验 · 8 页，原审计快照）

> 以下为历史覆盖情况，并非当前缺陷状态；SMS-45/46/56/57/58/59/60/61/62/64 等已修项不再适用，统计页剩余条目以上方复核为准。

- `tools/statistics/iqr.html`：0 条（SMS-57/58 已修）。默认 25/40/60 → IQR 35.0000、下限 -27.5000、上限 112.5000、中位数 40.0000 正确；四个预设（薪资/分数/对称/右偏）与其摘要值一致；Q3<Q1 输出负 IQR 与反向边界一项已修（SMS-57：五数顺序链校验 + 四面板清空）；描述承诺与五数摘要不符一项已修（SMS-58：中文描述、英文 intro、EN map、guides、分类页与生成器全源收窄为「五数概括」）。
- `tools/statistics/statistics-11.html`：0 条（SMS-56 已修）。默认 80/90/70、权重 0.5/0.3/0.2 → 加权平均 83.0000、权重和 1.0000 正确；三个预设（成绩/价格/等权）公式无误；四个辅助面板被 `#result` 覆盖而失效一项已修（SMS-56：面板移出结果容器、wmDiff 纳入页签、Σw=0 停算清空）。
- `tools/statistics/binomial-pmf.html`：0 条（SMS-59 已修）。主算对数域正确（默认 10/3/0.5 → 0.11719；n=20,k=2,p=0.1 → 0.28518；p=0/p=1 边界正确）；附加层 `q^n` 下溢导致历史 pk=0 一项已修（SMS-59：对数域增量递推 + pk 与主算同源 + 图表窗口围绕 k）。
- `tools/statistics/independent-t-test.html`：0 条（SMS-60/61 已修）。默认 → t=1.8974、df=38、p=0.0654 正确；前提卡的方差比阈值、Welch t 与 dfw 计算正确；表格 t 口径混用与 n/s 校验缺失两项已修（附加层共用 sp² 与合并标准误；主算强制 n₁,n₂ 为 ≥2 整数且 s₁,s₂>0；`__itChart()` 与主算前提同源，停算清空曲线）。
- `tools/statistics/correlation-coefficient.html`：0 条（SMS-62 已修）。默认 X=1..5、Y=2,4,5,4,5 → r=0.7746、r²=0.6000、t=2.1213 正确；四个预设（正/负/强相关）正确；常量数据下强度结论与「—」矛盾一项已修（dx/dy≤0 或 r 非有限时停答提示并清空图表/明细/差异/历史）。
- `tools/statistics/correlation-r-squared.html`：0 条（SMS-63 已修）。默认 r=0.8 → R²=0.6400、未解释 0.360000、决定优势比 1.777778、VIF 2.777778 正确；r=0.1～0.95 查表矩阵计算正确；主算越界不校验且与明细表截断值矛盾一项已修（严格解析 −1≤r≤1、越界停答清空五面板、主算与明细/参考曲线同源）。
- `tools/statistics/pooled-variance.html`：0 条（SMS-64 已修）。默认 10/2、12/3 → 6.750 正确；note 中 (9·4+11·9)/20=6.75 与 deep-dive 例 100/117.8 复算一致；n≤1、空值、负 sd 守卫已存在；残留的「只清 pvTable、图表与差异面板保留旧结果」已修（三处共用 `__pvClear()`）。
- `tools/statistics/sample-size-mean.html`：0 条。σ=10、e=2、z=1.96 → n=97（96.04 向上取整）、中间量 9.8000、95% 参考 96.0 正确；e=1 → 385 正确；守卫覆盖必填、非数值与 e=0，附加层表格按固定 90/95/99 阈值计算正确；未发现算错/崩溃/假功能。极限输入（负 σ/负 e 平方后与正值同值、z=0 → n=0）属无效参数且不产生错误量级，未单列。

- 声明：本轮仅逐页读源码并用 node 在 `/tmp` 复刻各页主算与边界分支（对数域/下溢、合并与未合并 t、守卫早退路径、`toFixed` 输出），未开浏览器、未跑 `_build.py`/`_test_static`/`run_gates`、未做线上与英文态验证，未修改任何工具页、构建产物或仓库文件。新增 9 条：高 1（SMS-56），中 8（SMS-57～SMS-64），其中承诺未实现 1 条（SMS-58），安全 0 条，假工具 0 条；8 页均完成覆盖（sample-size-mean 0 条）。

## Y 批 · 自然科学·天文/地理/计算（2026-11-04）

- `tools/science/astro-geo-calculator.html`：0 条 —— 地震能量、TNT 当量、地平线、湿度与气压正确；SMS-65/66/67 已于第 1027 批修复（日出日落时区改 `+8−lon/15` 北京 04:49、蒲福表按 min 下界命中消灭 0.1 空隙、位置行按符号输出 N/S/E/W）；SMS-68 已于第 1031 批修复（遮挡卡改按观察者几何地平线扣减后求目标可见最低高度，h=2m 得 0.0/1.9/17.5m）；SMS-69 为旧审计快照，2026-11-08 F-N189 全站护栏已把趋势图数据源改为 `__tbScore`，第 1032 批探针实测图表绘制 `[1,1]`、表格 2 行，条目销账。
- `tools/science/astronomy-toolkit.html`：0 条 —— 撞击坑 CMM 标度律（默认 50 m/20 km/s → 1.14 km 瞬态坑、约 9.4 Mt）、UTM 正反算、观测评分主体正确；SMS-73（经度无校验/61 带）已修——正向经度限 -180~180、带号钳制 1~60，反向加 E/N 物理范围与结果域守卫；SMS-71 第 1030 批、SMS-74 第 1033 批、SMS-70 第 1034 批、SMS-72 第 1035 批修复（66.5°~66.56° 早退文案改为「几何口径不足严格阈值＋视直径/折射可致短暂无落日或无日出」，明确否定全年极昼极夜，并加英文分支）；Y 批本页销账。
- `tools/science/barcode-pharmacode.html`：0 条 —— 非固定映射假工具；走共享 `js/barcode-lib.js` 的 `pharmacodeEncode`（`num+1` 二进制去最高位、1→宽条、条间 1 模块空白），3→两窄条、131070→16 宽条，取值 3～131070 有守卫，画布渲染与自动生成正常。
- `tools/science/calc-cycle.html`：0 条 —— 元素量、括号嵌套与未知元素报错正确；SMS-75/76 已于第 1028 批修复（多余右括号先拦截再 pop 不再抛 TypeError、段首系数 5H2O 乘算 CuSO4.5H2O=249.68 与文档一致），Y 批本页销账。
- `tools/science/calc-distance.html`：2 条（SMS-79/80）—— Haversine 距离、英里/海里、初始方位角、中点纬度均正确（默认北京→上海 1067.310 km、方位 153.07°）；SMS-77 已于第 1029 批修复（切度分秒时四坐标输入 type 同步改 text、值不再被清空）；剩余中点经度越界与快捷键说明不符两处中等（飞行时间 60 分进位 973 批销账）。

| 页面 | 问题（含 tools/&lt;dir&gt;/&lt;slug&gt;.html:NN） | 编号 |
|---|---|---|
| tools/science/calc-distance.html | 中点经度 `lon1+atan2(By,cosφ1+Bx)` 未归一化到 ±180：(-30,178)→(-20,-170) 输出「184.24568」（node 复刻）。:249、:265 | SMS-79 |
| tools/science/calc-distance.html | 使用说明写「Ctrl/Cmd + Enter 复制结果」，键盘处理只匹配 Ctrl/Cmd+C（且需无选中文本），按说明操作无反应。:174 对 :367 | SMS-80 |

- 统计：5 页 / 3 条（高 0 / 中 3）/ 安全 0 条 / 假工具 0 个 / 编号区间 SMS-65～SMS-80（SMS-65/66/67 第 1027 批、SMS-75/76 第 1028 批、SMS-77 第 1029 批、SMS-71 第 1030 批、SMS-68 第 1031 批、SMS-74 第 1033 批、SMS-70 第 1034 批、SMS-72 第 1035 批修复；SMS-69 第 1032 批按 F-N189 现状销账；SMS-78 飞行时间进位 973 批销账）。

## Y 批 · 自然科学·统计/物理/化学（2026-11-04）

- `tools/science/centripetal-force.html`：0 条。默认 2 kg / 10 m·s⁻¹ / 5 m → F=40.0 N、4.0789 kgf、a=20.0000 m/s²、T=3.1416 s 正确；预设、图表、历史与差异均按 F 正常记录；v=0 因周期 T 发散被守卫拦截属合理，未发现算错/崩溃/假功能。
- `tools/science/chemistry-calculator.html`：SMS-83～85 已于第 1015 批真机销账——分子式严格解析（未知元素/括号失配/零下标报错、段首系数与结晶水多段独立），稀释恰好留空一个值双向求解（C₁/V₁ 必填正值），理想气体非求解字段正数校验（T=-10 K 报错）。H2O/Ca(OH)₂/Fe₂(SO₄)₃/KMnO₄ 摩尔质量、浓度/pH/气体主算均正确；原分子式 XSS 第 953 批已修。本批 Y 批已全部销账。

- 声明：本轮为历史审计快照；SMS-81（969 批）、SMS-83～85（第 1015 批）、SMS-86～91（早前批次及第 1014 批）均已真机销账，Y 批无剩余未修项；安全 0 条（原 SMS-82 XSS 已修复，第 953 批真机复核）；假工具 0 个。
- 统计：8 页 / 0 条（Y 批全部销账）/ 安全 1 条（tools/science/chemistry-calculator.html:588、:596、:822）/ 假工具 0 个 / 编号区间 SMS-81～SMS-91（历史快照，均已销账）。

## Z 批 · 自然科学·数学/地学/热学（2026-11-04）

- `tools/science/gcd-calculator.html`：SMS-94/95 已于第 1006 批改严格整数解析（Number + isInteger + 拒绝超 2^53），factorize 卡死路径随之被堵；默认 48,36,24 → GCD 12 不变。仍共用 SMS-106 附加历史模板问题（未修）。
- `tools/science/lcm-calculator.html`：SMS-94 同族严格解析已修；SMS-96 改为先除后乘 `a/g*b` 缓解 gcd>1 时的中间积溢出，但互质大数（如 1000000007×1000000009）结果超 2^53 仍需 BigInt 重构，保留待专业裁断。
- `tools/science/geo-distance-calculator.html`：SMS-97 已修——Haversine、初始方位角与英里/海里换算正确（北京 39.9042,116.4074 → 上海 31.2304,121.4737 = 1067.310 km）；同组错误按字段保存后聚合渲染，lat1 越界不会被随后合法的 lon1 抹掉。仍共用 SMS-106。
- `tools/science/heat-transfer-calculator.html`：1 条（SMS-100 承诺未实现）。默认铜 401 W/m·K / 10 cm² / 10 mm / ΔT 75 → 3007.50 W、热流密度 3,007,500.00 W/m² 正确；SMS-98/99 已修——非正/非有限参数清结果并拒绝，历史记录回填 17 个输入字段；比热容 Q=mcΔT 的主结果、卡、历史与导出按热量 J/kJ/kWh/kcal 显示。热辐射仍只有公式没有计算。
- `tools/science/latlon-utm-converter.html`：SMS-101 已修——北京 39.9042,116.4074 → 50N 449345.061E 4417292.495N（收敛角 −0.2916°、比例因子 0.999632），正反算往返准确；经度 +180° 钳制到第 60 带（中央经线 177.0°），反算增加 E (0~1e6)/N (0~1e7) 范围与结果域校验，带号与 E/N 不匹配时明确拒绝而非输出荒谬经纬度。
- `tools/science/led-resistor-calculator.html`：1 条（SMS-104 中）。串联 5 V/20 mA/2.2 V → R 140 Ω、P 56.0 mW 正确，标准电阻与实际电流亦正确；SMS-102/103 已修——并联功耗改按总电流 (n·If)²·R（12 V/2.2 V/20 mA/2 只由 196.0 mW 更正为 392.0 mW）、精度下拉按 tol 选 E96/E24/E12/E6 标准数列（R=500 时分别 499/510/470 Ω）。残留为「取最近标准值」是否改为「向上取以保证不超额定」的产品口径（页面明确承诺"最接近值"），保留待工程裁断。
- `tools/science/log-calculator.html`：SMS-105 已修——极小值示例与 `fmt()` 普通分支均使用科学计数（阈值 ≤1e-3），`1e-5` 不再被 `toLocaleString()` 默认 3 位小数显示为 0。

| 页面 | 问题（含 tools/science/&lt;slug&gt;.html:NN） | 编号 |
|---|---|---|
| tools/science/lcm-calculator.html | 第 1006 批已把 `lcm2` 改为先除后乘 `abs(a/gcd*b)` 并同步步骤行，缓解 gcd>1 时中间积溢出；但互质大数 lcm(1000000007,1000000009) 真值 1,000,000,016,000,000,063 超 2^53，Number 无法精确表示，仍需 BigInt 重构（未自判）。:234 | SMS-96 |
| tools/science/heat-transfer-calculator.html | 承诺未实现：英文 intro「conductive, convective and radiative … Stefan-Boltzmann」、公式列表、公式框「☀️ 热辐射公式」、FAQ「传导、对流与辐射的热量传递」均承诺辐射计算，但页面仅 conduction/specific/convection 三模式，无 ε、辐射面积、T₁⁴/T₂⁴ 输入，Q=εσA(T₁⁴−T₂⁴) 无法计算。:179、:362、:395、:904 对 :198-201、:620-683 | SMS-100 |
| tools/science/led-resistor-calculator.html | `nearestStdR` 取绝对差最近值而非「不小于」：R=140 Ω（5 V/20 mA/2.2 V）选 130 Ω，实际电流 21.54 mA 超设定 20 mA（+7.7%）；取 150 Ω 则为 20.53 mA。:482-492、:565、:577 | SMS-104 |
| tools/science/gcd-calculator.html | 附加历史模板把 `.result-box` 文本截 80 字存入「结果」列，趋势图再 `parseFloat` 该文本：gcd/lcm 以「输入：」开头、log 以「x = 」开头、geo 以「📊 计算详情」开头 → 恒 NaN，图永不绘制且结果列显示输入串；factorial「10! = …」得 10，图表画的是输入 n 而非 n!。:326-332、:368（同模板 lcm:307/349、log:308/350、geo:1027/1069、factorial:343/385） | SMS-106 |

- 声明：本轮仅逐页通读 8 页源码（HTML + 内联 JS），用 node 在 `/tmp` 复刻主算与边界（BigInt 阶乘位数、斯特林溢出、parseInt 精度、√n 枚举、双精度乘积、UTM 正反算、LED 并联功率/标准电阻、对数 fmt），未开浏览器、未跑 `_build.py`/`run_gates`、未做线上与英文态验证，未修改任何工具页、构建产物或仓库文件。
- 原审统计（历史快照）：8 页 / 15 条（高 4 / 中 11，其中承诺未实现 1 条 SMS-100）/ 安全 0 条 / 假工具 0 个 / 编号区间 SMS-92～SMS-106；SMS-93 与 SMS-105 已分别于 2026-11-06、第 1012 批复核清理。

## Z 批 · 自然科学·矩阵/统计/电学（2026-11-04）

- `tools/science/matrix-calculator.html`：SMS-107/108/109 已修——2×2/3×3 乘、行列式、逆、秩主算复核正确（[[4,7],[2,6]] det=10、A⁻¹=[[0.6,-0.7],[-0.2,0.4]]）；幂次改 Number + 整数校验，0 标量/0 次幂保留；奇异与秩判据改相对元素级容差，逆矩阵 check 输出最大偏差。
- `tools/science/mean-calculator.html`：SMS-110 几何平均连乘溢出/下溢已于第 1005 批改对数域 exp(Σln/n) 修复。SMS-111（千分位逗号被当分隔符）属页面「逗号或空格分隔」口径未定义，保留待产品裁断。
- `tools/science/mechanical-power.html`：SMS-117 已修——P=F·v 与 kW/hp/kgf·m/s 系数（745.6999、9.80665）换算正确（100 N×5 m/s=500 W）；主结果改有效数字格式，0.2 W 不再显示 0 W、0.5 W 不再进位成 1 W，数据表同步。
- `tools/science/meteor-crater-estimator.html`：1 条（SMS-121 中）。CMM 标度律与能量/破坏半径自洽（50 m/13 km/s 铁陨石 → 1.2 km、10 km/20 km/s → 119.6 km）；SMS-119/120 已修——地表类型切换才套默认密度，同类型手改值保留；质量单位档改为 1e6 kg=千吨、1e9 kg=百万吨。保留通古斯按钮与预设参数矛盾待口径裁断。
- `tools/science/nato-phonetic.html`：SMS-112/113 已修——NATO 表 Alfa/Juliett 与数字读法（Three/Tree、Nine/Niner）正确，ANSI 老表 Y/Z 改为 YOKE/ZEBRA，历史记录写入 `__natoMode` 并在点击时恢复原模式，不再强制 ANSI。
- `tools/science/newtons-second.html`：SMS-118 已修——F=ma、kN、a×3.6（km/h/s）、kgf 换算正确（10 kg/3 m/s² → 30.0 N、0.030000 kN、10.8000、3.0591）；主结果与 kN 档按量级保留有效位/科学计数，0.0001 N 与 1e-7 kN 不再归零，数据表同步。
- `tools/science/nth-root-calculator.html`：SMS-114/115/116 已修——∛27=3、⁴√16=2、x>0 全部复数根（27 的立方根 −1.5±2.598i）正确；负奇整数根用 `Math.abs(n)%2` 识别，0 的负次根明确报错，≤1e-3 走科学计数不再把非零小值回显为 0。

| 页面 | 问题（tools/science/&lt;slug&gt;.html:NN） | 编号 |
|---|---|---|
| tools/science/mean-calculator.html | `parseData` 以 `[,\s\n;]+` 切分后静默丢弃非数值 token：「1,000, 2,000」被切成 1/0/2/0 → n=4、AM=0.75（真值 1500），数据列表与 n 均随之改变，无任何提示。:242、:246-248 | SMS-111 |
| tools/science/meteor-crater-estimator.html | 「通古斯事件」按钮与自带预设冲突：按钮用石质 3000 kg·m⁻³ / 27 km·s⁻¹ / 沉积岩，预设「通古斯 60m 彗星」用 1500 kg·m⁻³ / 15 km·s⁻¹ / 冰盖，同一事件两套参数（撞击能量相差约 6.5 倍）。:587-593 对 :851 | SMS-121 |

- 声明：本轮仅逐页通读 8 页源码（HTML + 内联 JS）并用 node 在 `/tmp` 复刻主算与边界（矩阵求逆/奇异阈值、连乘几何平均溢出、千分位解析、负整数指数开方、负指数零次根、小数取整、CMM 坑径标度律、欧姆定律增益/单位档），未开浏览器、未跑 `_build.py`/`run_gates`、未做线上与英文态验证，未修改任何工具页、构建产物或仓库文件。`nato-phonetic` 的 `else html += c` 曾按注入排查：字母字符都会被 `ALPHA[c]` 替换成 `<span>`，未转义的只剩标点/非 ASCII，无法拼出可执行标签，故不计安全条。
- 统计：8 页 / 17 条（高 3 / 中 14，其中承诺未实现 0 条（SMS-109 已于 632 批修复））/ 安全 0 条（无 eval、无 allow-same-origin、无明文存密、无第三方外传）/ 假工具 0 个 / 编号区间 SMS-107～SMS-123。

## 2026-11-06 科学工具静态续审（清单 598–605）

- 以下历史结论对应旧源码，当前不应继续计为已确认：SMS-9/10 摩尔质量解析已支持括号、水合物并扩充至 118 元素（`molar-mass-calculator.html:233-273`）；SMS-21/22 配平已剥离前导系数并明确提示欠定非唯一（`equation-balancer.html:389-407`、`:547-570`、`:718-719`）；SMS-34/35 分数输入已有整数检查与除零提示（`fraction-calculator.html:357-393`）；SMS-40 PCB 输入无效时清结果、图表和缓存（`pcb-trace-width.html:406-422`）。上述为代码状态变化，不代表实际回归通过。
- LED SMS-102（并联功耗按 (n·If)²·R）与 SMS-103（精度档按 tol 选 E96/E24/E12/E6）已于第 1020 批修复；仅 SMS-104（取最近值 vs 向上取整的产品口径）仍在，页面承诺「最接近标准值」，改口径需工程/产品裁断，不自判。原举例中 150 Ω 电流应为 18.67 mA（2.8 V/150 Ω），不是 20.53 mA。
- PCB 的参考表 SMS-39 仍需按当前资料复核，导出路径另仅用真值校验，负输入可能输出 NaN（`pcb-trace-width.html:473-485`）。
- 本批仅静态读代码及算式复核，未运行浏览器，不能计双跑。

## AA 批 · 自然科学·物理/数论/元素（2026-11-04）

- `tools/science/pendulum-period.html`：SMS-124 已修——默认/重置/历史预设三处 g 由 9.81 统一为 9.80665（与同页引据及 physics-constants 一致），输入 step 改 any 使默认值合步长；英文 JSON placeholder 同步。L=1、g=9.80665 → T=2.006 s、f=0.4985 Hz、ω=3.1321 rad/s，量纲自洽。
- `tools/science/periodic-table.html`：SMS-125 已修——118 元素及 H/Cr/Cu/Pd/La–Lu 电子排布抽样正确；镧系与锕系首格均加 `grid-column:1` 强制各起新行，锕系不再续排在镧系行右侧。
- `tools/science/permutation-calculator.html`：SMS-126/127 已于第 1007 批改严格整数解析 + n≤2000 上限守卫，并删除未使用的 O(n) 数组；P(7,3)=210 等常规结果不变。
- `tools/science/physics-constants.html`：3 条（SMS-128～130 中）。c、G、h、e、mₑ、Nₐ、k_B、R、α、a₀ 等数值抽查全部正确；问题在分类维度错置、柱图 exp 元数据与数值不符、重复行符号/数值自相矛盾。
- `tools/science/pi-digits.html`：0 条。1000 位串长度、前缀与第 100/1000 位复核无误（…3421170679 / …2164201989），第 N 位与搜索位置 +1 口径无偏差。
- `tools/science/polar-day-night.html`：1 条（SMS-131 中）。70°N 极昼 5/21–7/23 共 64 天、极夜 11/19–1/21 共 64 天，与深挖算例一致；问题在 66.56° 预设返回 0 天及参考卡天数与引擎冲突。
- `tools/science/power-calculator.html`：SMS-132/133 已修——Math.pow 主算正确（2^10=1024、2^-10=9.765625e-4），引据表为指数律，极小数与普通小数（|x|<1e-3）均走科学计数，2^-10 显示 9.7656250000e-4 而非 0.001。
- `tools/science/prime-number.html`：SMS-134/135 已修——单值判定/区间筛/质因数分解主算正确（97 素数、91=7×13）；`parsePositiveInt` 用 Number+Number.isSafeInteger 严格解析（拒绝 97.9 截断、1e3→1），区间终点上限 1e7、单值试除至 √n 有界，verify 4 条覆盖。

| 页面 | 问题（tools/science/&lt;slug&gt;.html:NN） | 编号 |
|---|---|---|
| tools/science/physics-constants.html | 分类维度错置：`universal` 的标签写作「宇宙学」（英文 Cosmology），却装入 c/μ₀/ε₀/G/h/ℏ 等普适与电磁常数；「引力加速度(标准) g」归入「天文」，页面也无电磁类别——按分类查 μ₀/ε₀ 找不到对应维度。:236-244、:269、:277 | SMS-128 |
| tools/science/polar-day-night.html | 66.56° 预设使极昼/极夜天数均为 0，输出「该纬度无极昼现象 / 无极夜现象」，与参考卡「66.56° 极圈：极昼/极夜各约 1 天」及深挖「约 1 天」直接冲突（阈值 90−23.44=66.56，而正弦近似峰值仅 23.4398，全年无一日满足）；参考卡 70/75/80° 的 65/60、105/95、135/125 也与引擎 64/64、102/102、131/131 不符（按本公式同纬度极昼/极夜必然等长）。:145、:185-187、:222、:267 | SMS-131 |

- 声明：本轮仅逐页通读 8 页源码（HTML + 内联 JS），在 `/tmp` 用 node 复刻主算与边界（单摆 T/f/ω 与 g 双值对比、极昼逐日布尔与跨年连续区间、幂 fmt 的 `toLocaleString` 默认位数、π 1000 位串头尾与第 100/1000 位、parseInt 截断、BigInt 排列的量级、sieve 内存/试除复杂度、常量 exp 分桶），未开浏览器、未跑 `_build.py`/`run_gates`、未做线上与英文态验证，未修改任何工具页、构建产物或仓库文件。默认单位复核：单摆 L(m)/g(m·s⁻²) 量纲自洽，极昼工具纬度统一按度、无角度/弧度混用。
- 安全注记：本批 8 页无 `eval`/`new Function`/`allow-same-origin`/`document.write`、无明文存密、无页面自有网络外传；本批数值页的用户输入均经 `parseFloat`/`parseInt` 或固定数字正则后才参与运算与拼接，未形成可控 HTML 注入。公共模板统一注入的 `lf1-cdn-tos.bytegoofy.com/ttzz/push.js` 属全站既有项（前批按「非本批页面特有、不重复登记」口径处理），故未计入条数。
- 原审统计（历史快照）：8 页 / 12 条（高 2 / 中 10）/ 安全 0 条 / 假工具 0 个 / 编号区间 SMS-124～SMS-135；SMS-124（972 批）、SMS-125（第 1021 批镧锕系定位）、SMS-129/130、SMS-132（第 1014 批）、SMS-133、SMS-134/135 均已真机销账，本批仅剩 SMS-131（66.56° 极昼 0 天，涉天文常数口径待裁断）。

## AA 批 · 自然科学·方程/统计/RC/星等（2026-11-04）

- `tools/science/quadratic-equation.html`：2026-11-06 复核判别式改相对阈值，小系数原例算出 ±1，SMS-136 清理；a<0 共轭根负虚部（SMS-137）已于 972 批修正。
- `tools/science/range-calculator.html`：2 条（SMS-138 高、SMS-139 中）。默认 [12,25,8,17,33,21,6] → min 6 / max 33 / 极差 27 / 中程 19.5 正确；问题为千分位逗号被当分隔符、说明承诺的均值/中位数/标准差未实现。
- `tools/science/rc-time-constant.html`：3 条（SMS-140 高、SMS-141～142 中）。预设「滤波 1 kΩ×100 nF → 100 μs」复核正确；问题为默认 10000(kΩ)+0.000001(μF)=10 MΩ/1 pF 使 τ=10 μs（与数值字面本意 10 ms 差 1000 倍）、简介承诺的截止频率缺失、0 V 被替换为 5 V。
- `tools/science/star-magnitude-compare.html`：2 条（SMS-146～147 中）。−1.46 vs 0 → Δm=1.46、3.84 倍；太阳/满月 Δm=14 → 3.98×10⁵，倍率落在常识区间；问题为 0.77 等重复行反查取错星名、天津四与老人星二的距离/绝对星等不自洽。
- `tools/science/statistics-calculator.html`：2 条（SMS-148 高、SMS-150 中）。默认 n=15 → 均值 10.8、中位数 9、样本 sd 7.485、偏度 0.672、超额峰度 −0.918，全部正确；问题为千分位被切分、末组区间标 `[a,b)` 却含最大值。SMS-149（NaN 偏度/峰度误判对称/正态）本批已修。
- `tools/science/{quadratic-equation,range-calculator,star-magnitude-compare,statistics-calculator}.html`：1 条（SMS-151 中，共用模板）。`__*Extras` 对中文结果文本做 `parseFloat` 恒得 NaN → 「结果趋势」图永不渲染（rc 页为 canvas 曲线，不受影响）。

| 页面 | 问题（tools/science/&lt;slug&gt;.html:NN） | 编号 |
|---|---|---|
| tools/science/range-calculator.html | `parseData` 以 `[,\s\n;]+` 切分，千分位逗号被当分隔符：输入「1,000, 2,000」→ [1,0,2,0]，极差由 1000 变成 2；单值「1,000」→ [1,0] 极差 1，页面无任何提示。:232 | SMS-138 |
| tools/science/range-calculator.html | 公式说明承诺「同时输出均值、中位数与标准差便于对照」，但 `calculate` 只渲染最小值/最大值/极差/中程数与步骤，全页无均值、中位数、标准差计算（承诺未实现）。:154、:240-254 | SMS-139 |
| tools/science/rc-time-constant.html | 默认值与默认单位错配：阻值 10000 配 `kΩ`（=10 MΩ）、容值 0.000001 配 `μF`（=1 pF），τ=10⁷×10⁻¹²=10 μs；两个数值显然按 Ω/F 基单位填写（10000 Ω × 1 μF 应为 10 ms），默认 τ 与字面本意差 1000 倍，10 MΩ 电阻与 1 pF 电容也非典型默认。:134、:137、:145、:151 | SMS-140 |
| tools/science/rc-time-constant.html | 工具简介承诺计算「各时间点充放电电压与截止频率」，但全页无 f_c=1/(2πRC) 输出、无任何频率字段（默认 τ=10 μs 对应截止频率 15.9 kHz），承诺未实现。:463 | SMS-141 |
| tools/science/rc-time-constant.html | `var vs = +voltage.value &#124;&#124; 5` 把合法的 0 V 静默替换成 5 V：输入 0 V 后表格仍按 5 V 显示充电/放电电压（τ 不变，但电压列与曲线全错），导出路径同源。:269、:315 | SMS-142 |
| tools/science/star-magnitude-compare.html | 按星等值反查星名取错行：`STARS.find(s => Math.abs(s.vmag - m1) < 0.01)` 取首个匹配，而表内 0.77 等有牛郎星（:293）与十字架二（:294）两行；点选十字架二后结果卡标注为「牛郎星」，两星张冠李戴。:335-336 | SMS-146 |
| tools/science/star-magnitude-compare.html | 表内距离/绝对星等不自洽：天津四 vmag 1.25、amag −6.95、dist 2615 ly，按距离反推 amag≈−8.27（差 1.3 等）；老人星二 vmag 1.69、amag −0.9 反推距离仅 107 ly（实际约 111 ly），表中 dist 却写 381 ly（约 3.5 倍）。:300、:304 | SMS-147 |
| tools/science/statistics-calculator.html | 同一千分位缺陷：`parseData` 用 `[,\s\n;]+` 切分，「1,000, 2,000」→ [1,0,2,0]，n=4 而非 2，均值/方差/偏度全部按错误数据计算，页面无提示。:270 | SMS-148 |
| tools/science/statistics-calculator.html | 频数表末组区间标成左闭右开 `[20.4, 25.00)`，却把最大值 25 计入该组（`idx` 夹到最后一桶），末行区间与频数自相矛盾；默认数据即可复现。:411 | SMS-150 |
| tools/science/&#123;quadratic-equation,range-calculator,star-magnitude-compare,statistics-calculator&#125;.html | 共用模板「结果趋势」图恒为空：`__*Extras` 用 `parseFloat(arr[j].d[rk])` 解析中文结果文本（「Δ = 1」「极差 Range = 27」「星等差 Δm = 1.46」「样本均值 = 10.8」），恒为 NaN，`nums.length>=2` 永不成立，图一次都不渲染（rc 页为 canvas 曲线不受影响）。quadratic:514、range:335、star:598、statistics:612 | SMS-151 |

- 声明：本轮仅逐页通读 6 页源码（HTML + 内联 JS），在 `/tmp` 用 node 复刻主算与边界（RC 默认 τ=10 μs 与 Ω/F 基单位对照、二次方程小系数判别式与 a<0 复根、极差/统计的千分位切分、频数表分箱边界、星表 23 行 m–M–距离反推、流量单位换算与 Re），未开浏览器、未跑 `_build.py`/`run_gates`、未做线上与英文态验证，未修改任何工具页、构建产物或仓库文件。默认单位复核：流量 `mm`+`m/s`、星等无量纲、二次方程无量纲均自洽；RC 的默认单位组合不自洽（见 SMS-140）。星等倍率复核：天狼星/0 等 3.84 倍、太阳/满月 3.98×10⁵、南北极星对比 23.7 倍，均在常识区间。
- 安全注记：本批 6 页无 `eval`/`new Function`/`allow-same-origin`/`document.write`、无明文存密、无页面自有网络外传；输入均经 `parseFloat`/`parseInt` 后才参与运算，HTML 拼接值来自数值或内部常量。flow 历史项虽把 `modeName`/`Q_str` 写入 `innerHTML`，但这些字符串只由页面自身生成（localStorage 被篡改属同源自注入，不计）。公共模板 `lf1-cdn-tos.bytegoofy.com/ttzz/push.js` 为全站既有项，按前批口径不重复登记。
- 原审统计（历史快照）：6 页 / 16 条（高 4 / 中 12）/ 安全 0 条 / 假工具 1 个 / 承诺未实现 2 处 / 编号区间 SMS-136～SMS-151；SMS-136 已于 2026-11-06 复核清理。

## AB 批 · 自然科学·潮汐/换算/方程（2026-11-04）

> 页面名后的「（死键 N）」= 该页第三层英文词典（`i18n/tools/en/<ind>/<slug>.json`）高优先死键数（来源 `plan/i18n-dead-keys.md`）；各线改本页时顺手清理，本批不修英文。

**族矩阵（7 页）**

| 页面 | 类型 | 输入 | 主算 / 输出 | 默认态复算 |
|---|---|---|---|---|
| tools/science/tide-height-estimator.html（死键 2） | 潮汐估算 | 日期、纬度、海岸类型、月相(自动/手动) | 月球+太阳半日潮正弦模型 | 2026-11-04、30°N、开阔海岸、自动 → 残月 0.7、太阳 0.327、高潮 0.48 m、低潮 −0.29 m、潮差 0.77 m |
| tools/science/torque-converter.html（死键 0） | 纯单位换算 | 数值 + 8 种扭矩单位 | `baseNm/f` 全单位展开 + 功率-转速表 | 10 N·m → 7.375621 lb·ft、88.50746 lb·in、1.019716 kgf·m、101,971.6 gf·cm、1,416.119 ozf·in、1e+6 dyn·m |
| tools/science/trigonometry-calculator.html（死键 1） | 三角/反三角 | 角度或弧度、三角/反三角、反函数种类 | sin/cos/tan、csc/sec/cot、asin/acos/atan、象限 | 30° → 0.5 / 0.866 / 0.577；asin 0.5 = 30°、acos 0.5 = 60°、atan 1 = 45° |
| tools/science/wavelength-to-rgb.html（死键 0） | 光谱派生换算 | 380–780 nm | `wlToRgb` + f=c/λ + E=1240/λ | 550 nm → #A3FF00、545.45 THz、2.25 eV |
| tools/science/wire-gauge-converter.html（死键 0） | 纯单位换算 | AWG 0–40 或直径 mm | 92 指数公式 + 面积/电阻/载流/压降 | 24 AWG → 0.511 mm、0.205 mm²、载流 1.02 A；页面电阻 0.08「Ω/km」（真值 84.01，差 1000 倍） |
| tools/science/work-done.html（死键 0） | 物理量计算 | 力 F、位移 d、夹角 θ | `W = F·d·cosθ` + 分解与图表 | 50×10×cos0 = 500 J |
| tools/science/xianxingfangchengzuqiujie-2yuan-3yuan.html（死键 0） | 代数求解 | 2/3 元系数 | Cramer 法则 + 行列式判定 | 2 元 x=1,y=2；3 元 x=1,y=2,z=3 |

族矩阵结论：真正的纯换算只有扭矩与线规两页；波长是光谱派生量，潮汐/功/三角/方程是计算器；7 页同用 TBKit 标签页、历史与导出外壳，历史与预设实现同源，故同类缺陷可跨页复现。

**逐页结论（未修项）**

- `tools/science/torque-converter.html`：8 个单位系数与功率-转速表全部正确（9549/ rpm），默认 10 N·m 展开正确；仅导出 CSV 把每一行都追加「 N·m」，非 N·m 行的单位标签全错。
- `tools/science/wire-gauge-converter.html`：AWG↔mm、面积与载流公式正确，默认 24 AWG 的 0.511 mm、0.205 mm²、1.02 A 一致；但铜电阻把 `ρ/A`（Ω/m）直接标成 Ω/km，整表与压降/每千英尺派生值全部小 1000 倍（AWG 24 显示 0.08 Ω/km，真值 84.01）。
- `tools/science/work-done.html`：`W=Fd cosθ` 与默认 500 J 正确；两个预设同时翻倍/减半 F 与 d，实际倍率为 4×/0.25×，与「2×/0.5×」标签不符。

**问题条目**

| 页面 | 问题（含 tools/science/&lt;slug&gt;.html:NN） | 编号 |
|---|---|---|
| tools/science/torque-converter.html | 【中】导出 CSV 单位后缀写死：`__torqueExport` 对全部 8 行都追加「 N·m」，lb·ft、lb·in、kgf·m、gf·cm、ozf·in、dyn·m 行均被标成 N·m（数值本身正确）。:488-490 | SMS-155 |
| tools/science/wire-gauge-converter.html | 【高】铜电阻量纲错 1000 倍：`res_km=rho/area_mm2` 实为 Ω/m，却标成「Ω/km」（:403、:409），AWG 24 显示 0.08 Ω/km（真值 84.01）、AWG 20 显示 0.03（真值 33.23）、AWG 0 因 `toFixed(2)` 直接成 0.00；由它派生的「Ω/1000ft」（`res_km×0.3048`，:419）与「100m 压降」（`res_km/1000×100`，:421）同样小 1000 倍（AWG 24 显示 0.0084 V，应 8.40 V）。:403、:409、:418-421、:436 | SMS-158 |
| tools/science/work-done.html | 【中】预设倍率标签与结果不符：「示例 2×」把 F 50→100、d 10→20，做功 500→2000 J（4×）；「示例 0.5×」把 F→25、d→5，做功→125 J（0.25×），标签的 2×/0.5× 均未实现。:258-261 | SMS-160 |

**统计（未修项）**
- 条数：3（高 1 / 中 2 / 假 0 / 安全 0）；编号 SMS-155、SMS-158、SMS-160。
- 高优编号：SMS-158（铜电阻 Ω/m 当 Ω/km）。
- 假工具：0；承诺未实现：0；冒用标准：0。
- 安全：0 条；上述 3 页无 `eval`/`new Function`/`allow-same-origin`/`document.write`/明文存密/Cookie/页面自有网络外传；拼接值来自数值或内部常量。公共模板 ttzz 脚本不单列。
- 复算：node 内存复算 AWG 24 电阻 0.0840 vs 84.01 Ω/km、100m 压降 0.0084 vs 8.40 V；功预设 2000/125 J vs 500 J；扭矩 8 系数与 9549/rpm 表；未落盘仓库；仅源码阅读，未开浏览器、未跑 `_build.py`/`run_gates.py`、未改 `tools/**` 与构建产物。
- 去重说明：SMS-158 的 Ω/m 与 Ω/km 量纲混用与既有「单位错配」同类但本页还连带压降与每千英尺两项派生值，按页单列。

## AC 批 · 矩阵/向量运算族（2026-11-04）

### 族矩阵

| 页面 | 实现方式 | 可逆或可验证 | 结论 |
|---|---|---|---|
| `tools/science/matrix-calculator` | 自写 det（Laplace）、mul、inverse（高斯-若当）、rank、矩阵快速幂 | 可验证 | A=[[4,7],[2,6]] det=10、A·A⁻¹≈I、A⁻²≈inv(A)² 均正确；2026-11-06 复核 SMS-107 的 0 输入已修 ｜ **631 批已修**：相对容差统一（SMS-108 的 2e-7·I 不再误判奇异）、幂次小数不再截断（改整数校验） ｜ **632 批已修**：`check` 改为实输出乘积矩阵 + 与单位矩阵最大偏差（2.22e-16 判在容差内），不再只打印定义句；同时 9 个分支标签全部走 isEn 分流（EN 态零 CJK）。 |
| `tools/math/determinant-2x2` | 自写闭式 det=ad−bc | 可验证 | 默认 −2 正确；显示精度与奇异判定自相矛盾 |
| `tools/science/vector-calculator` | 自写 dot/cross/mag/proj/angle/scale | 可验证 | 2026-11-06 复核：k=0 和零向量夹角的原例已修；极小非零向量会被绝对阈值误认为零向量 |
| `tools/design/data-matrix` | 伪实现：32 位哈希→LCG 随机格 + 外观边框，无 ECC200 编码/纠错（`:258-294`） | 不可验证（自述不可扫码） | 装饰图案，非 Data Matrix |

### 独立实现 vs 共享实现

- **4 页全部独立实现，族内共享 0**：det/mul/inverse 只在 matrix-calculator，向量算子只在 vector-calculator，determinant 只有一元闭式，data-matrix 只有哈希/PRNG。
- 族外重复：matrix-calculator 的 det/mul/inverse 与 `tools/math/matrix-transpose` 等页同套公式，改动需跨页同步（不计入本族同源）。

### 逐页结论

- **data-matrix**：默认 text=Data Matrix、size=14，输出确定性伪随机格 + 左/下实线、上/右交替边框（`:276-281`），与「装饰图案」自述一致；无 ECC200 编码。

### 问题清单（新增）

| 编号 | 页面:行 | 级别 | 问题与期望值 |
|---|---|---|---|
| SMS-163 | `tools/math/determinant-2x2.html:241,243,264-266` | 高 | 展示用 `det.toFixed(2)`、判定用 `det===0`：[[0.1,0.3],[0.3,0.9]]（ad=bc，数学奇异）node 复算 det=1.38e-17 → 页面「行列式 0.00」+「非奇异（可逆）」自相矛盾。期望以 `Math.abs(det)<eps`（如 1e-12）判定并与显示精度统一 ｜ **630 批已修**：新增 `__det2x2Judge`，判据 |det| ≤ 1e-12·max(|ad|,|bc|)；残差非零时展示 toExponential(2)（1.39e-17）并标注「ad 与 bc 在双精度下仅差…」，卡片/明细表/公式框三源同源且 EN 态同步。 |
| SMS-166 | `tools/science/vector-calculator.html:352-365` | 中 | 2026-11-06 复核：零向量夹角已提示「零向量无法计算夹角」，Node 执行实际 `calculate()` 确认原例已修。残留：判断采用绝对阈值 `mA<1e-12 &#124;&#124; mB<1e-12`，A=(1e-13,0)、B=(1,0) 等非零向量仍被误判为零，投影分支对 B 同样适用该阈值。 ｜ **630 批已修**：新增 `__isZeroVec(v)`（|v| ≤ max|分量|·1e-12 或最大分量恰为 0 才算零向量），夹角/投影/单位向量/绘图四处判定 + fmt 展示统一，1e-13 级非零向量不再误判，非零极小值改科学计数。 |
| SMS-167 | `tools/science/matrix-calculator.html:430` | 中 | rank 主元阈值同为绝对 1e-12：[[1e-13,0],[0,1e-13]] 可逆却 rank=0（应 2）；与既有 SMS-108 同根，修复时并入该条 ｜ **631 批已修**：新增 __matScale/__matEps，det/inverse/rank 三处判定统一用 max|元素|·1e-12 相对容差，det 提示文案同源；[[1e-13,0],[0,1e-13]] rank=2、2e-7·I 可逆（5e6·I）；幂次改 Number+isInteger 严格整数。 |

### 统计

- 页数 **4**；独立实现 **4** / 共享实现 **0**。
- 原审新增 **6** 条（高 **2** / 中 **4** / 假 **0** / 安全 **0**）；编号 SMS-163–SMS-168。2026-11-06 复核清理 SMS-164/165：向量数乘与绘图均保留 0；矩阵极小数采用科学计数，公共 CSV 导出对含逗号单元格加引号。SMS-166 原例已修；SMS-163/166 于 630 批、SMS-167/108 于 631 批、SMS-168 于 632 批全部修复或收紧。
- 复核既有：SMS-107/108/109（matrix-calculator 幂次整数校验、相对容差、求逆验证实输出）已于 631/632 批修复，源码核对确认（`:583 Number.isInteger`、`:352` 相对容差、`:555-567` check 实输出）；D-N137（data-matrix 无 ECC200）核心仍成立，但「定位边方向与 ISO 相反」已失效（当前 :277-280 符合标准），属条码标准口径待专业确认，不自判。
- 复算方式：`/tmp` node 复刻页面函数（det/mul/inverse/rank/向量算子）；未开浏览器、未跑 `_build.py`/门禁、未改仓库文件。
