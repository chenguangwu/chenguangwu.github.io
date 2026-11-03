# 机械/金属加工 · tools/{machinery,metalwork,welding,manufacturing}（~160 页）

## 已知问题### M3. gongyeshebeigonglvpipei 死代码与误导注释
- ✅ 死变量清理（2026-10-26）：torque/loadTorque 两行死变量与注释已删，grep 确认无引用；顺带修该页 #res EN 存量泄漏（calc 动态串 10 处全 __T 化 + location fallback，NO_MODULE 是容器名 #res 非默认所致，--container=res 后 OK_EN）。

## 功能缺陷
- metalwork 7 个「双段通用对比页」功能单薄（carbon-8/diandonggongju-xifen/laxue-ladao/tangxue/wushua/yuanlingongju-xifen/zhineng-duogongneng）：生效 calc 仍是 A/B 两值通用比值-差值输出，非领域公式（carbon-8 第二段有 850-950℃ 渗碳拟合为例外）；建议按主题补真实领域计算（渗碳层深-时间、拉削力-齿升、镗杆刚度等）。
- ✅ 切削页「材料-刀具匹配表」已具备（2026-10-30 复核）：`mechanical/cutting-speed.html` 的 `#refList` 已渲染 碳钢/合金钢/铸铁/铝合金/不锈钢 × 高速钢/硬质合金 的速度区间矩阵，deep-dive 亦列同口径推荐区间；该项销案（`machinery/speed-cutting-feed` 为跳转存根）。
- 折弯页缺「回弹补偿」输入项。

## 优化点
- S7 引据：GB/ISO 标准号徽标（本类可信度关键）。→ 已落地 12 页（2026-10-27 批31）：machinery/bearing-1 + estimate-lifespan-bearing + bearing-load + bolt-preload + calc-gear-1 + calc-64 + calc-strength + drive-2、welding/weld-strength + calc-weld + temp-time-6 + detector-25（ISO 281/GB/T 6391、GB/T 3098.1/VDI 2230、GB/T 1357、GB/T 1800.1/ISO 286-1、GB 50017、IIW 碳当量、NB/T 47013）；累计 24 页（批31+32）：批32 加 shaft-torsion/tolerance(-1)/thread-4/torque/strength-34/strength-6/tanhuangsheji + metalwork/surface-finish + assessor-34 + analysis-39 + calc-pressure-mold；两目录其余页待续批。
- S3 分步：齿轮/皮带选型链路图（已注入部分 chart，推广 S3 明细）。

## 受影响范围
- tools/machinery/（78）、tools/metalwork/（42）、tools/welding/、tools/manufacturing/

## 进度
- 🔴 待开发

## 2026-11-03 审计补充

### 线膨胀计算错误时明细/图表可能保留旧值（高，确认源码缺陷）
- 问题：清空原长后主结果显示错误，但附属数据表、图表计算分支提前退出不清理旧图表或明细，CSV 仍指向原表。
- 证据：`tools/engineering/thermal-expansion.html:220-224,238-251,258-261,270-274,316-319`；主函数错误退出后包装函数继续运行，extras 对空值直接 return，导出读取 `#thermal_expansionTable`。仅静态核查，图表初次绘制及点击导出需浏览器复验。
- 影响：`tools/engineering/thermal-expansion.html`；错误输入下旧工程数据可能被误认为当前输出。
- 方案：统一校验并同时清空/禁用结果、明细、图表及导出，恢复合法值时一并更新；增加合法→清空→导出测试。

### 留存优化：材料温度变化对照（低，建议）
- 证据：同页 `:223-230,246-251,264-267` 已提供线膨胀公式、明细和数值预设。
- 影响：同页；方案：预设可标注材料来源与适用温度，并并排展示用户选择的两种材料伸长量；注明线性系数为近似。

### 皮带历史恢复遗漏带轮直径（高，确认源码缺陷）
- 问题与证据：`tools/machinery/pidaizhangjinjisuan.html:212-225,245-252` 用直径计算带速及张力，但历史保存、恢复和复制摘要均缺直径。B 型、500 mm、1450 rpm、5.5 kW、125 mm 时单根约 289.8 N；保存后改为 250 mm 再恢复，仍使用 250 mm，计算约 144.9 N。
- 影响：`tools/machinery/pidaizhangjinjisuan.html`，历史工况无法准确复现，复制结果缺关键输入。
- 方案：保存、恢复并显示节径；旧记录缺字段时提示，增加保存—更改直径—恢复的回归测试。

### 焊接热输入超限及单位示例错误（高，确认源码缺陷）
- 问题与证据：`tools/metalwork/welding-heat.html:132-148,195,245-256` 输入控件标明效率最大 1，但计算只拒绝非正数；180 A、24 V、25 cm/min、η=2 输出 2.074 kJ/mm。页面示例将 4320 J/cm 写成 43.2 kJ/m，正确换算为 432 kJ/m。
- 影响：`tools/metalwork/welding-heat.html`，非法效率仍出具热输入，示例单位错误影响核对。
- 方案：计算时校验 0<η≤1，修正示例并补边界和跨单位测试；保留工艺预设并展示换算明细。

### 覆盖
- 本轮人工及只读子代理核查 `tools/engineering/thermal-expansion.html`、`tools/machinery/pidaizhangjinjisuan.html`、`tools/metalwork/welding-heat.html` 共 3 页；仅源码和算术推导，未做浏览器验证，其余未逐页覆盖。

## 2026-11-03 续查（并行批 H）

> 编号说明：文件原有历史编号 `M3` 保留不动；本批按并行批约定新增 `MM-H` 系列，不与其重号。以下结论均为源码阅读 + node 内存复算，未做真实浏览器、英文态、移动端、门禁或线上验证。

### MM-H1 折弯角 180° 时外延量爆炸，展开长出 −1.14×10¹⁷ mm（高，确认）
- 描述：角度输入上限为 `max=180`，校验只拒绝 `A>180`；`A=180` 时 `tan(A/2)=tan 90°` 在 JS 得 1.633×10¹⁶，OSSB/BD 随之爆炸，展开长变成巨大负数，结果卡仍按普通数值格式化输出且无任何提示。
- 证据：`tools/metalwork/sheet-bend.html:130`（`max="180"`）、`:235`（仅 `A<=0||A>180` 拦截）、`:240-242`（`OSSB=tan(rad/2)*(R+T)`、`BD=2*OSSB-BA`）、`:243,258`（`toFixed(3)` 输出，`replace(/Infinity|NaN/g,'—')` 兜不住有限大数）。node 复算 T=2、R=1.5、A=180、K=0.46、L1=50、L2=40 → BA `7.603`、OSSB `57159337736183792.000`、BD `114318675472367584.000`、展开长 `-114318675472367488.000 mm`。
- 影响：`tools/metalwork/sheet-bend.html`。180° 对折本是常见工况，用户得到量级荒谬的下料尺寸，且页面无「不适用」提示，存在按错误尺寸下料的风险。
- 方案：输入上限改为 179°（或 <180），或对 A=180 单独提示「BD 法在 A→180 时 OSSB→∞，请改用折线/对折展开算法」；增加 A=179/180 边界用例并断言输出有限。

### MM-H2 折弯半径与两法兰长度允许负值，可算出负展开长（中，确认）
- 描述：校验只覆盖 T、A 与「六参数非数」，未校验 `R>=0`、`L1/L2>=0`；负 R 使 BA 为负、负法兰长度直接进入 `L=L1+L2-BD`。
- 证据：`tools/metalwork/sheet-bend.html:128-130`（`min` 只是 HTML 属性，键盘可输入负值）、`:235`（校验集合）、`:239-242`。node 复算 A=90、K=0.46、T=2：R=-1 → BA `-0.126`、OSSB `1.000`、BD `2.126`、展开长 `87.874 mm`；L1=-50、L2=-40 → 展开长 `-93.199 mm`。
- 影响：`tools/metalwork/sheet-bend.html`。负下料尺寸可直接被复制/导出，且 R=-1 这种不存在的几何仍显示「可算」。
- 方案：补 `R>=0`（建议 `R>0` 并提示最小弯曲半径）、`L1>0 && L2>0`；越界标红并中止，不进入明细/历史。

### MM-H3 深度解析算例 BA/BD/展开长三处与公式不符（中，确认）
- 描述：算例写「BA≈4.93、BD=5.07、L=94.93」，按同页 `:239-242` 公式复算应为 `BA=5.655、BD=4.345、L=95.655`。
- 证据：`tools/metalwork/sheet-bend.html:189`（算例文本）、`:239-242`（实际公式）。node 复算 T=2、R=3、A=90、K=0.3、L1=L2=50 → BA `5.655`、OSSB `5.000`、BD `4.345`、展开长 `95.655 mm`。
- 影响：`tools/metalwork/sheet-bend.html` 深度解析区。用户用该算例手算核对时必然与页面结果对不上，削弱可信度。
- 方案：按公式重算算例三值（建议在页面注明 `K=0.3` 为示例取值），并加一条与默认参数一致的算例。

### MM-H4 锻造比在「锻后截面大于原始」时给出负变形，仍提示「建议增大变形」（中，确认）
- 描述：拔长/镦粗均未校验终锻尺寸方向，K<1（甚至 0.34）时 `ε=(A₀−A₁)/A₀` 为负，页面仍走「未达到目标锻造比，建议增大变形」分支；目标锻造比也只要求 `>0`，可填 0.5 让零变形判合格。
- 证据：`tools/metalwork/forging-ratio.html:270-272`（仅 `target<=0` 拦截，`min=1` 只是 HTML 属性）、`:277-279`、`:283-286`、`:290-292`（无方向校验）、`:300`（显示 `deform.toFixed(1)`）、`:303,308`（固定文案）。node 复算拔长圆 d0=70、d1=120、target=3 → K `0.340`、ε `-193.9%`；镦粗 H0=80、H1=200 → K `0.400`、ε `-150.0%`。
- 影响：`tools/metalwork/forging-ratio.html`。输入方向填反时输出负变形率与「建议增大变形」自相矛盾，易被误读为工艺不足。
- 方案：拔长要求 `A₁<A₀`、镦粗要求 `H₁<H₀`，否则提示「锻后尺寸大于原始，变形方向相反」并停止；`target` 要求 `>=1`；负变形不得进入结论。

### MM-H5 产能页「单台日产能」再乘班次，2 班时产能翻倍（高，确认）
- 描述：输入标签是「单台日产能(件)」，计算却统一乘 `shifts`；只有把 200 理解成「单台班产能」才自洽。用户按标签填日产能时，2 班配置会得到 2 倍理论产能、利用率减半、所需设备数减半。
- 证据：`tools/manufacturing/capacity-planning.html:172`（标签）、`:176-180`（班次下拉，默认 2 班）、`:294-298`（注释「单台日产能已按班次计算」但 `monthlyCap=m*cap*wd*sh` 仍再乘一次）、`:226`（深度解析同样按 200×22×2 举例）。node 复算 5 台/200/2 班/22 天/需求 20000：按页面口径 → 月产能 `44000`、利用率 `45.5%`、需 `3` 台；若 200 为真实日产能 → 月产能 `22000`、利用率 `90.9%`、需 `5` 台。
- 影响：`tools/manufacturing/capacity-planning.html`。扩产/排班结论可能差一倍，直接影响设备投资与交期判断。
- 方案：标签改为「单台班产能(件/班)」，或删除 `*sh` 并让日产能含全部班次；在结果区回显「按 X 班计，单台月产能 = …」；补一组「日产能口径」回归用例。

### MM-H6 利用率被截断在 200%，工作日 0 静默按 22 天（中，确认）
- 描述：`utilRate=Math.min(d/monthlyCap,2)` 把超载工况压到 200%，进度条按 `utilRate*50` 封顶 100%；`workDays` 用 `|| 22`，输入 0 或空值会被悄悄替换成 22。
- 证据：`tools/manufacturing/capacity-planning.html:188`（`min=1 max=31`）、`:291`（`wd=...||22`）、`:297`（`Math.min(...,2)`）、`:322-323`（`${(utilRate*100).toFixed(1)}%` 与 `width:${Math.min(utilRate*50,100)}%`）、`:333`（缺口文案另用真实 `overHours`）。node 复算默认参数、需求 100000 → 实际 `227.27%`，页面显示 `200.0%`；工作日填 0 → 按 22 天计算。
- 影响：`tools/manufacturing/capacity-planning.html`。严重超载时利用率与缺口口径不一致（百分比封顶、缺口却继续增大），工作日被替换后用户无法察觉。
- 方案：取消 200% 封顶（或超 100% 单独标红并显示真实值）；`workDays` 为 0/空时提示而非兜底 22；结果区注明采用的工作日。

### MM-H7 不良率页工序数为负时 DPMO 变负，直接判 6σ「卓越」（高，确认）
- 描述：`processes` 只做 `||1` 兜底，负数原样进入 `dpmo=(d/t)*1e6/p`，得负 DPMO；`dpmoToSigma` 首个分支 `dpmo<=0.002` 命中，返回 6.0σ，CPK 也被抬到 2.00、等级「卓越」。
- 证据：`tools/manufacturing/defect-rate.html:294-298`（`p=...||1`，无 `p>=1` 校验）、`:303`（`dpmo=.../p`）、`:280-291`（`dpmoToSigma` 阶梯）、`:305-313`（sigma/cpk/level）、`:341-352`（结果卡）。node 复算 total=10000、defects=50、processes=-2 → DPMO `-2500`、sigma `6.0`、CPK `2.00`、等级 `卓越`。
- 影响：`tools/manufacturing/defect-rate.html`。一个明显非法的工序数会产出「世界级质量」结论，可能被直接用于质量汇报。
- 方案：`processes` 校验为 `>=1` 的整数，越界报错并停止；`dpmo<=0` 时单独处理（0 缺陷时才允许 0 DPMO→6σ），负值不得进入换算。

### MM-H8 不良率页把「不良品数」当「缺陷数」，d>t 直接拦截多缺陷场景（中，确认）
- 描述：页面输入名是「不良数」，但 DPMO 按 `d/t/p` 计算；当一件产品存在多个缺陷（DPMO 的标准口径）时，缺陷数可大于投入件数，页面却在 `d>t` 时直接 toast 拦截，导致该口径无法录入。
- 证据：`tools/manufacturing/defect-rate.html:174-182`（三个输入）、`:297-304`（`if(d>t)` 拦截与 `dpmo=(d/t)*1e6/p`）、`:220`（深度解析以「不良 250 件/2 工序」举例，未区分缺陷与不良品）。node 复算 total=1000、defects=1200 → 被 `d>t` 拦截；若按缺陷数口径，DPMO=（1200/1000）×10⁶/2=`600000`。
- 影响：`tools/manufacturing/defect-rate.html`。多缺陷工序的真实 DPMO 无法计算，用户只能把缺陷数压成不良品数，结果系统性偏低。
- 方案：拆成「不良品数」与「缺陷数」两个输入（PPM 用不良品数、DPMO 用缺陷数），或在单一输入上加「计数口径」切换并同步结果卡标签。

### MM-H9 角焊缝 extras 绕过校验，焊脚 0 时写入 0 截面与 Infinity 应力（中，确认）
- 描述：主计算对 `F/hf/lw<=0` 会报错并 return，但包装后的 extras 只判断三个原始值是否 `isFinite`，0 属于有限值；于是 `hf=0` 时仍生成 `A=0`、`tau=Infinity` 的明细表并写入历史，导出直接读该表。
- 证据：`tools/welding/weld-strength.html:219-228`（主计算校验与输出）、`:236-251`（extras 仅 `isFinite` 检查、`A=0.7*hf*lw`、`tau=F/A`、`history.record`）、`:256-258`（导出读 `#weld_strengthTable`）。node 复算 F=50 kN、hf=0、lw=200 → A `0`、τ `Infinity`（`toFixed(2)` 得字符串 `Infinity`）。
- 影响：`tools/welding/weld-strength.html`。无效参数下主结果提示错误，但明细/历史/CSV 仍出现 0 mm² 与无限应力，形成两套互相矛盾的输出。
- 方案：extras 复用主计算的合法性判定（`F>0 && hf>0 && lw>0`），非法时清空表格/跳过历史；导出前再校验一次。

### MM-H10 角焊缝未扣起灭弧长度、也未做许用应力判定（中，确认）
- 描述：页面注意事项写明「l_w 应扣除起灭弧缺陷（通常减 2h_f）」「τ 应 ≤ 角焊缝强度设计值」，但计算把输入 `lw` 直接当有效长度，且没有强度设计值输入与通过/不通过判定。
- 证据：`tools/welding/weld-strength.html:133-135`（lw 输入）、`:177-179`（两条说明）、`:219-227`（`A=0.7*hf*lw`、仅输出 A/τ）。node 复算默认 F=50 kN、hf=6、lw=200 → A `840`、τ `59.52 MPa`；按 2h_f 扣减后 A `789.6`、τ `63.32 MPa`（低估 6.4%）。
- 影响：`tools/welding/weld-strength.html`。用户按页面说明自行扣减时结果对不上；不做许用值判定则无法回答「这条焊缝够不够」。
- 方案：增加「是否扣减 2h_f」开关（默认扣减）并回显有效长度；增加角焊缝强度设计值输入（或按母材/焊条推荐），输出利用率与通过/不通过。

### MM-H11 轴承页 C=0 通过校验，输出 0 转/0 小时/0 年（中，确认）
- 描述：提示文案要求「C、P、n 均需大于 0」，实际守卫只拦 `P===0||n===0`；C=0 时 `ratio=0`、`L10=0`，三项寿命全 0 且无任何错误提示。
- 证据：`tools/machinery/bearing-1.html:178`（`num` 允许 0）、`:184-187`（守卫不含 `C===0`）、`:188-192`（`ratio=C/P`、`Math.pow(ratio,p)`）、`:195-206`（结果卡）。node 复算 C=0、P=5、n=1500 → C/P `0.00`、L₁₀ `0.0` 百万转、L₁₀h `0.0`、L₁₀y `0.00` 年。
- 影响：`tools/machinery/bearing-1.html`。额定动载荷为 0 是明显的非法输入，却得到完整「寿命 0」结果，且可被复制/记入历史。
- 方案：守卫补 `C<=0`，与提示文案一致；三输入均要求正数并按字段分别标红。

### MM-H12 弹簧固有频率质量换算差 1000 倍，频率低估约 31.6 倍（高，确认）
- 描述：密度单位是 g/cm³、体积按 mm³ 计算，换算成 kg 的系数应为 `1e-6`，代码用了 `1e-3`，质量放大 1000 倍；`fn=(1/2π)·sqrt(k/m×1000)` 随之低估 31.6 倍。
- 证据：`tools/machinery/tanhuangsheji.html:190`（材料密度表 `rho:7.85` 等）、`:235`（`m=1e-3*rho*πd²/4*πDn`）、`:236`（`fn`）、`:251`（显示 `固有频率 (Hz)`）、`:178-179`（注意事项要求固有频率为工作频率 10 倍以上）。node 复算 d=3、D=20、n=8、碳素钢丝 G=79300、ρ=7.85：k `12.5455 N/mm`、体积 `3553.06 mm³`；代码质量 `27.8915 kg` → fn `3.375 Hz`（显示 `3.4`），正确质量 `0.0278915 kg` → fn `106.74 Hz`。
- 影响：`tools/machinery/tanhuangsheji.html`。固有频率校核整体失真，按页面值会误判「远离共振」，实际频率约高 31.6 倍。
- 方案：质量系数改为 `1e-6`（或先把体积换算为 cm³ 再乘密度）；补一条独立算例（如 d=3/D=20/n=8 期望 ≈106.7 Hz）作为回归基线。

### MM-H13 拉伸试验页每次键入都写历史，8 条上限被输入中间态占满（中，确认）
- 描述：四个输入均为 `oninput="calc()"`，而 `calc()` 末尾无条件 `saveHistory(...)`；编辑任一项的每个合法中间值都会立刻落库，历史很快只剩中间态。
- 证据：`tools/metalwork/calc-stretch.html:133-145`（四个 `oninput="calc()"`）、`:189-228`（`calc` 内计算）、`:227`（`saveHistory('δ=...')`）、`:242-249`（`unshift` 且截断到 8 条）。node 复算把 L0 改为 10（L1=125）→ δ `1150.00%`，该中间态会作为一条正常记录写入。
- 影响：`tools/metalwork/calc-stretch.html`。历史/「最近计算」无法反映用户最终工况，恢复记录会跳回中间输入。
- 方案：仅在「计算」按钮、Enter 或 blur 时保存；或对 `calc` 加 500–800 ms debounce，并在保存前按输入快照去重。

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
- 编号：本批新增 `MM-H1`–`MM-H13`，与文件原有 `M3` 不重号。
- 验证声明：仅源码阅读 + node 内存复算；未做真实浏览器、英文态（`?lang=en-US`）、移动端、门禁、线上或导出文件实测。涉及 TBKit 渲染、toast、CSV 输出的运行时表现未实测，相关条目仅确认到源码路径层面。
