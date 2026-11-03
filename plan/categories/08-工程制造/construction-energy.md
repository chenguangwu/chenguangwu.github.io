# 土木/能源 · tools/{civil,construction,structural,energy,fire-rescue,safety,urban,bridge,road,tunnel,architecture}（~200 页）

## 已知问题
## 功能缺陷
- 混凝土配比页缺「强度等级↔水灰比对照」联动表。
- 消防页缺「疏散宽度计算」（商店/观众厅指标）高频项。

## 优化点
- S7 引据：GB 50010/50016 标准徽标。→ civil 24 页全量收口（批34/62），structural 13 页（批35），energy 14 页（批57），construction 38 页全量收口（批66/67/68，GB 50010/JGJ 55/GB 50500-2013/JGJ 130-2011/GB 50009-2012 等）。本文件 S7 全部收口。
- S3 分步：土压力/承载力分步图解。

## 受影响范围
- tools/civil/、tools/construction/、tools/structural/、tools/energy/（41）、tools/fire-rescue/、tools/safety/、tools/urban/、tools/bridge/、tools/road/、tools/tunnel/（~200 页）

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 地基承载力校验与旧复制结果不一致（高，确认源码缺陷）
- 问题与证据：`tools/civil/dijichengzailijisuan.html:159-179,192-195` 对负黏聚力和负摩擦角标红，但主退出条件不含二者，仍继续计算。有效参数 c=15、φ=0、γ=18、B=2、Df=1.5、K=2 得 52.05 kPa；随后清空 B，主结果提示错误但 `lastResult` 未清空，复制仍使用旧值。
- 影响：`tools/civil/dijichengzailijisuan.html`，非法工况仍出结果、错误状态可能复制旧设计数据。
- 方案：统一校验条件并同步清空或禁用旧复制结果；提供工况历史并排对比时明确模型和适用条件。

### 风电功率的零 Cp 被默认为 0.4（高，确认源码缺陷）
- 问题与证据：`tools/energy/wind-power-estimator.html:269-281,295-307` 使用 `parseFloat(...) || 0.4`，用户输入 Cp=0 被代入 0.4；风速 12 m/s、半径 40 m、密度 1.225 kg/m³ 时页面按约 2.128 MW 输出，而公式按 Cp=0 应为 0。
- 影响：`tools/energy/wind-power-estimator.html`，结果与输入不符。
- 方案：区分零、空值与非法输入，显示实际采用的参数；年发电量明确容量系数与功率基准假设，可允许用户设置容量系数并对照工况。

### 覆盖
- 本轮抽查上述 2 页，仅源码及算术推导，未进行真实浏览器、专业标准及线上验证；其余页面未逐页覆盖。

## 2026-11-03 续查（并行批 F）

本批覆盖 8 页：`tools/civil/active-earth-rankine.html`、`tools/civil/pile-capacity.html`、`tools/civil/beam-udl.html`、`tools/energy/heat-pump-cop.html`、`tools/energy/power-factor-calc.html`、`tools/energy/three-phase-power.html`、`tools/energy/energy-payback.html`、`tools/energy/lcoe.html`。本文件此前无编号前缀，本批起统一使用 CE-N 前缀（CE-N1…CE-N10），与既有无编号条目区分、不重号。下列结论均来自源码阅读 + node 内存复算（复刻页内公式），未在浏览器执行。

### CE-N1 朗金主动土压力漏掉黏聚力平方项（高，确认）
- 描述：公式框与 `calcTool()` 均用 `E_a = ½γH²K_a − 2cH√K_a`，缺少从临界深度起算的 `+2c²/γ` 项；仅当 `z0≥H` 时整体归零。
- 证据：`tools/civil/active-earth-rankine.html:116,224-226`。复现 γ=18、H=5、φ=30°、c=10 → 页面输出 E_a=17.26 kN/m（Ka=0.333、z0=1.92 m）；同一压力沿深度积分到墙底应为 28.38 kN/m（½γH²Ka−2cH√Ka+2c²/γ），偏低约 39%。
- 影响：黏性填土挡墙主动土压力被系统性低估，用于抗滑/抗倾验算偏不安全。
- 方案：补 `+2c²/γ`；`z0<H` 时自临界深度起算，`z0≥H` 时输出 0 并提示全高开裂；同步更新公式框、tool-notes 与深度解析示例。

### CE-N2 朗金 φ 只校验大于 0，预设直接给 φ=60（中，确认）
- 描述：输入框标注 0–45 且 `max=45`，但 `calcTool()` 仅判 `phi<=0`；预设「示例 2×」写死 `phi:'60'`，点击即越界计算。
- 证据：`tools/civil/active-earth-rankine.html:131,219,278`。复现点「示例 2×」→ φ=60、Ka=0.0718、E_a=129.23 kN/m（页面照常输出）；手动输入 φ=120 → Ka 同为 0.0718，与 60° 结果无法区分。
- 影响：越界/超限输入给出貌似合法结果，无任何提示。
- 方案：JS 校验 `0<φ≤45`，越界标红停止；预设改为几何相似工况（只缩放 γ、H，保持 φ、c 不变）。

### CE-N3 单桩承载力接受负侧阻/负端阻并输出负 Ra（中，确认）
- 描述：`min=0` 只约束步进器，`calcTool()` 仅校验 d、L、K>0，qs、qp 可为负。
- 证据：`tools/civil/pile-capacity.html:131,137,224,227`。复现 d=0.6、L=15、qs=−40、qp=2000、K=2 → 总侧阻 −1131 kN、端阻 565 kN、Ra=−283 kN。
- 影响：负承载力被当作有效特征值展示并写入历史/CSV，布桩方向会反。
- 方案：qs、qp ≥0、K ≥1 纳入 JS 校验；Ra<0 时提示参数矛盾。

### CE-N4 简支梁挠度的 I 与 b×h 默认/预设不是同一截面（高，确认）
- 描述：挠度用独立输入 I（cm⁴），应力用 b、h 算 `W=bh²/6`，但默认与三组预设中 I 均与 b×h 的实际惯性矩严重不符。
- 证据：`tools/civil/beam-udl.html:137,141,145,230-232,283-285`。默认 b=200、h=400 真实 I=106,667 cm⁴，页面取 8000 cm⁴ → 输出 δ=140.62 mm，按真实 I 应为 10.55 mm（放大 13.3×）；预设「示例 2×」b=400、h=800 真实 I=1,706,667 cm⁴、页面取 16000 cm⁴ → δ=1125.00 mm（真实 10.55 mm，放大 106.7×）。
- 影响：12 m 跨梁显示 1.1 m 挠度，与同页 σ=16.88 MPa 自相矛盾；按默认值抄结果会误判变形与配筋。
- 方案：由 b、h 自动算 `I=bh³/12`（cm⁴）并只读展示，或移除 I 输入改用 b、h；至少把默认与三组预设的 I 改成与 b×h 匹配值，并在切预设时联动重算。

### CE-N5 热泵输入功率 0 被兜底成 0.1 kW，电价 0 被兜底成 0.58（中，确认）
- 描述：`parseFloat(...) || 0.1`、`|| 0.58` 把零值、空值与非法值混同。
- 证据：`tools/energy/heat-pump-cop.html:302,313,331-333`。复现 制热量 12、输入功率 0、运行 1800 h、电价 0.58 → COP 显示 120.00、年耗电 180 kWh；复现 输入功率 3.5、电价 0 → 年电费 ¥3654（按 0.58 计），而非 0。
- 影响：零输入/零电价得到貌似精确的错误结果，与已记录的 `wind-power` Cp=0 同类。
- 方案：区分空值、零、非法值；输入功率 ≤0 提示并停止；电价 0 视为合法并按 0 计费，同时回显实际采用值。

### CE-N6 热泵制冷模式仍用制冷量对比锅炉制热，运行 0 h 时条形宽度 NaN（中，确认）
- 描述：`buildCompare(...)` 在 EER 模式下仍以 `output*hours` 当作年制热量，与电锅炉/燃气锅炉 COP 比较；且 `maxCost=0` 时宽度为 NaN。
- 证据：`tools/energy/heat-pump-cop.html:351,357-364,366,371`。复现切到「❄️ 制冷 EER」、制冷量 10、输入 3.0、1800 h → 对比区显示「热泵 COP=3.33 vs 电锅炉 COP=0.95」，基准为 18000 kWh 制冷量；复现 运行时长 0 → `maxCost=0`，HTML 出现 `width:NaN%`。
- 影响：制冷工况的节能结论口径错误；0 h 时费用条渲染异常。
- 方案：EER 模式隐藏该对比或改为同冷量电制冷对比；`maxCost<=0` 时按 0% 宽度且不渲染费用条。

### CE-N7 功率因数页 P>S 时 acos 越界，两张卡片塌成「—」（中，确认）
- 描述：只校验分母 S≠0，未校验 `0<P≤S`，pf>1 后 `Math.acos` 得 NaN。
- 证据：`tools/energy/power-factor-calc.html:246,279-284`。复现 P=800、S=500 → PF 显示 1.600，相位角与无功功率经 `NaN→—` 兜底显示「—」；PF=0.8 正常时 φ=36.87°、Q=600.000 kvar。
- 影响：物理不可能输入（有功大于视在）仍出一半结果，用户易误读为「无功为 0」。
- 方案：校验 `0≤P≤S` 且 S>0，越界标红停止；Q 改用 `√(S²−P²)` 直接算，避开 acos 定义域。

### CE-N8 三相功率预设 pf=1.8，P 大于 S 且 Q 被吞成 0（中，确认）
- 描述：无任何校验，预设「示例 2×」把功率因数设为 1.8；Q 用 `max(0,1−pf²)` 掩盖负值。
- 证据：`tools/energy/three-phase-power.html:215-221,258`。复现点「示例 2×」（U=760、I=200、pf=1.8）→ 有功 473.89 kW、视在 263.27 kVA、无功 0.00 kvar（P/S=1.80）。
- 影响：越界 pf 输出「有功大于视在」且无功为 0，与功率三角形矛盾。
- 方案：JS 校验 `0≤pf≤1` 与 U、I>0；预设改为同 pf 只缩放 U、I；Q 计算前先判 pf 越界并提示。

### CE-N9 回收期接受负年节约，且 save=0 被守卫拦下与公式说明矛盾（中，确认）
- 描述：未做非负校验；同时输入守卫把 inv、save 都当分母，save=0 直接报「不能为 0」，公式框承诺的 Infinity→「—」兜底永远走不到。
- 证据：`tools/energy/energy-payback.html:120,247,279-284`。复现 初投资 30000、年节约 −6000 → 回收期 −5.00 年、年回报率 −20.0%、10 年净收益 −90000 元；复现 年节约 0 → 提示「年节约 (元/年) 是本计算的分母，不能为 0」。
- 影响：负节约产出负回收期，项目评估结论反向；0 节约本应表达「无法回收」而非输入错误。
- 方案：inv、save 均要求 ≥0；save=0 单独分支输出「无法回收（∞）」并保留其余三项，删除与实现不符的说明。

### CE-N10 LCOE 拒绝折现率 r=0，缺极限分支（中，确认）
- 描述：守卫把 r 列入「不能为 0」分母集合，但 r→0 的 CRF 极限为 1/n，是合法工况。
- 证据：`tools/energy/lcoe.html:123,251,296`。复现 CAPEX=5,000,000、n=20、r=0、O&M=100,000、E=1,200,000 → 被拦为「折现率 r 是本计算的分母，不能为 0」；按极限 CRF=1/20=0.0500，LCOE 应为 0.292 元/kWh。
- 影响：想算不计折现（或近似零折现）的 LCOE 无法得到结果，与「CRF 随折现率升高而增大」的说明不闭环。
- 方案：r=0 走 `CRF=1/n` 分支，只在 n=0 时报错；公式框补充 r=0 极限说明。

### 留存优化
- 朗金页：补土压力沿深度折线图（标注 z0）与 φ/c 敏感性表；先修 φ 上限与预设再扩展。
- 简支梁页：增加「按 b×h 反算 I」或截面库选择；补充「自重是否已计入 q」的提示。
- 热泵页：补 SCOP/SEER 与部分负荷说明；对比区按模式切换基准；运行时长 0 的边界提示。
- 三相/功率因数：两页互加「线电压/相电压」「pf 上限」提示，避免同源输入口径混用。
- 回收期/LCOE：可把动态回收期、NPV/IRR 与折现敏感性作为可选扩展，不改变现有主结果。

### 续查覆盖
- 已覆盖 8 页：`tools/civil/active-earth-rankine.html`、`tools/civil/pile-capacity.html`、`tools/civil/beam-udl.html`、`tools/energy/heat-pump-cop.html`、`tools/energy/power-factor-calc.html`、`tools/energy/three-phase-power.html`、`tools/energy/energy-payback.html`、`tools/energy/lcoe.html`。
- 未覆盖：civil/energy 其余页面，以及 construction/structural/fire-rescue 等目录本批未逐页审计。
- 验证声明：仅源码阅读 + node 内存复算，未做真实浏览器、英文态（`?lang=en-US`）、移动端、门禁或线上验证；专业标准取值亦未逐条核对。
