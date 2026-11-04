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

## T 批 机械/制造覆盖（2026-11-04）

> 本批只读审计 `tools/machinery/` 下 8 个此前未覆盖页面；编号续接 `MM-H13`，从 `MM-H14` 起。

### MM-H14 检测页「孔径偏差」按单向 ≤0.1 判定，负偏差与空值被判合格（高，确认缺陷）
- 问题：输入是带符号的孔径偏差，页面标准栏写「≤±0.1mm」，但判定用 `val <= 0.1` 单向比较；同时 `parseFloat(...)||0` 把空值当 0。孔实际偏小（负偏差）或未填时都会判「合格」，并可给出「综合判定：合格」与「可用于质量验收」。
- 证据：`tools/machinery/detector-strength-lifespan.html:128`（标准栏 ±0.1）、`:213`（`op:"<=", threshold:0.1`）、`:219`（空值→0）、`:221-224`（单向判定与 allPass）、`:229-232`（合格结论）。
- 复现：node 复刻 → v1=-0.5、v2=650、v3=5500：孔径偏差 -0.5mm 判「合格」，综合「✅ 合格」；期望「不合格」。v1 留空、v2=650、v3=5500：表格显示「0 mm 合格」，综合「✅ 合格」；期望提示未填并判不合格。
- 影响：`tools/machinery/detector-strength-lifespan.html`。孔径偏小是常见实测结果，会被直接放行；空值也会被当成合格测量值，检测报告结论失真。
- 方案：`v1` 增加非空/数值校验，判定改为 `Math.abs(val) <= 0.1`（或 range [-0.1,0.1]）；任一字段为空/非法时置 `allPass=false` 并单独标红，不输出合格结论。

### MM-H15 压力扭矩检测页泄漏率空值/负值当 0，仍可综合合格（中，确认缺陷）
- 问题：`parseFloat(...)||0` 把空值当 0，而泄漏率判定为 `val <= 0.1`；清空或输入负泄漏率都会判「合格」。其余两项填合法值时综合结论直接「合格」。
- 证据：`tools/machinery/detector-pressure-torque.html:128-130`（三个输入）、`:213`（泄漏率 `<=0.1`）、`:219`（空值→0）、`:221-232`（判定与综合结论）。
- 复现：v1=""、v2=16、v3=150 → 表格「0 % 合格」，综合「✅ 合格」；v1=-1 → 同样「合格」。期望：未填/负值应标红并判不合格。
- 影响：`tools/machinery/detector-pressure-torque.html`。负泄漏率是不可能测量值，空值则是未检测；两者都被当成「0% 泄漏」放行。
- 方案：泄漏率增加 `val>=0` 与空值校验；空值单独提示「未填」而不是 0；负值判非法。

### MM-H16 螺纹中径 d₂ 多乘 cos(α/2)，60° 螺纹中径系统性偏大（高，确认缺陷）
- 问题：公式写成 `d₂ = d − 0.75·H·cos(α/2)`，其中 `H=P/(2tan(α/2))` 已含牙型角几何；60° 时正确基本中径为 `d − 0.64952P`，代码实际为 `d − 0.5625P`，中径偏大 `0.087P`。
- 证据：`tools/machinery/thread-recognize.html:125`（公式）、`:390-391`（`H` 与 `d2`）。55° 时 `0.75·H·cos27.5°≈0.639P` 与惠氏 `0.6403P` 接近，所以错误只在 60° 暴露。
- 复现：M10×1.5 → 代码 d₂=9.156mm，正确 9.026mm（+0.130mm）；M20×2.5 → 18.594 vs 18.376（+0.218mm）。期望按牙型角分支：60° `d−0.64952P`、55° `d−0.6403P`。
- 影响：`tools/machinery/thread-recognize.html`。中径是螺纹检验的核心尺寸，M10 的 6g 中径公差带仅约 0.15mm，0.13mm 误差接近整个公差带，会误导通止规判断。
- 方案：按牙型角分支计算中径（60° `d−0.64952P`、55° `d−0.6403P`），删除公式中的 `cos(α/2)`；公式行同步改为分段说明，并为 M10/M20 加回归算例。

### MM-H17 G1/2 预设与 30° 牙型角无数据库支撑，返回错误「最接近规格」（中，确认缺陷）
- 问题：`THREADS` 只有公制/UNC/UNF/BSW/BSF，没有 G（BSPP）管螺纹；「G1/2」预设 20.955/1.814/55° 必然无精确匹配，落到「最接近」分支后给出 3/4-12 BSF。选「30°（梯形/管螺纹）」时所有库项都加 100 分惩罚，仍返回一个 60° 螺纹，且不提示该角度无数据。
- 证据：`tools/machinery/thread-recognize.html:143-146`（角度选项含 30°）、`:528`（G1/2 预设）、`:338-347`（匹配与角度过滤）、`:356-373`（无匹配时的 closest 选择，`:363` 仅 +100 不排除）。
- 复现：G1/2（20.955/1.814/55）→ 无精确匹配，最接近「3/4-12 BSF」（标准外径 19.050、螺距 2.117）；期望识别为 G1/2 或明确提示「库中无 G 系列」。M10×1.5 选 30° → 返回「M10，60°」，期望提示无 30° 数据。
- 影响：`tools/machinery/thread-recognize.html`。预设是用户最常点的入口，G1/2 会被误认成 BSF；30° 选项则是死分支。
- 方案：补 G1/8–G2 的 BSPP 数据（或删除 G1/2 预设）；30° 选项在无数据时禁用/提示；closest 仅在角度一致时展示，否则只显示「无同角度标准螺纹」。

### MM-H18 平行度/位置度/跳动用圆度表派生，比 GB/T 1184 表值偏紧 2–3.6 倍（高，确认缺陷）
- 问题：页面只内置直线度/平面度（B1）与圆度/圆柱度（B2）两张表；平行度用 `B1×1.25`，位置度用 `圆度(g−1)×2`，跳动用 `圆度(g−1)×1.4`，并非 GB/T 1184 附录 B 的 B3/B4 表值（位置度更是独立数系，不按 D 查表）。结果系统性偏严，但页面仍宣称「内置 GB/T 1184 附录B 标准数据表」。
- 证据：`tools/machinery/tolerance-1.html:128`（自述「位置度=2t圆度，跳动=1.4t圆度」）、`:271-275`（三个派生系数）、`:227-235`（仅 B1/B2 两张表）、`:542`（宣称标准数据表）。对照 GB/T 1184-1996：B3 平行度 40–63mm/7 级=30μm，B4 同轴度/对称度/圆跳动/全跳动 30–50mm/7 级=20μm、50–120mm/7 级=25μm。
- 复现：平行度 L=50、7 级 → 代码 15μm，标准 30μm（低 50%）；位置度 D=80、7 级 → 12μm，标准 25μm（低 52%）；跳动 D=50、7 级 → 5.6μm，标准 20μm（低 72%）。
- 影响：`tools/machinery/tolerance-1.html`。用户按页面标注的形位公差会比标准严 2–3.6 倍，直接抬高加工/检测成本，且与「依据 GB/T 1184 附录B」的承诺不符。
- 方案：内置 B3/B4 实际表值（B4 同轴度/对称度/圆跳动/全跳动为同一张表）；位置度改为独立的「位置度数系」选择器，不再按 D 派生；删除 1.25/2/1.4 三个系数。

### MM-H19 形位公差超表尺寸静默夹取末段，且「查表范围」显示错段（中，确认缺陷）
- 问题：`findIndex` 超出最大分段时直接返回最后一档，`lookupRound`/`lookupStraight` 照常取值，不提示超表；`rangeLabel` 又用 `D_breaks` 的索引去取 `L_breaks`，直线度/平行度的显示范围与实际查表分段不一致。
- 证据：`tools/machinery/tolerance-1.html:227-235`（两个 lookup 的 `findIndex` 末档行为）、`:278`（`L_breaks[findIndex(D_breaks,D)]`）、`:291`（回显「查表范围 ≤…」）。
- 复现：圆度 D=1000、7 级 → 返回 20μm（实为 400–500 档），卡片仍写「≤500mm」；直线度 L=20000、7 级 → 返回 150μm（实为 ≤10000 档），但显示「≤2500mm」；直线度 L=25、7 级 → 值取自 ≤25 档，却显示「≤63mm」。
- 影响：`tools/machinery/tolerance-1.html`。大尺寸/超表零件得到一个「看似有依据」的公差值；范围文字也误导用户以为取的是另一档。
- 方案：超表时返回空值并提示「超出 GB/T 1184 表范围（≤500 / ≤10000mm）」；`rangeLabel` 改用与 lookup 相同的断点数组与同一 `idx`。

### MM-H20 带传动包角缺下限截断，D₁>D₂ 时算出 191° 仍判「满足」，极端值 NaN 也判「满足」（中，确认缺陷）
- 问题：`alpha1 = π − 2asin(min(1,(D2−D1)/(2a)))` 只有上限 `min(1,·)`，没有 `max(−1,·)`，也没有 D1≤D2 校验。D1>D2 时 asin 为负，α1 超过 180°；几何无解时 asin 参数 <−1 得 NaN，但判定链 `α1<120 / <150 / else` 对 NaN 全部落到 else 的成功分支。
- 证据：`tools/machinery/calc-lifespan-belt.html:256-259`（只校验 D1/D2/a >0）、`:275-277`（包角与 alpha2）、`:332-337`（成功分支）。
- 复现：D1=200、D2=100、a=500 → α1=191.48°、α2=168.52°（大轮包角反而小于小轮），提示「✓ 满足要求（≥150°）」；D1=300、D2=100、a=50 → α1=NaN，显示「小轮包角 —°」但仍提示「✓ 满足要求（≥150°）」。
- 影响：`tools/machinery/calc-lifespan-belt.html`。互换大小轮是常见输入错误，页面不但不报错，还给出不可能的角度和合格结论，F1/F2/Fq 也按错误包角计算。
- 方案：校验 `D1<=D2`（或自动交换并提示）；`asin` 参数加 `Math.max(-1, Math.min(1, ·))`，截断发生时直接判几何无解并中止；NaN 不得进入成功分支。

### MM-H21 带传动 n₁/P 未校验，0 转速输出 0 张力；P=0 且 v=0 仍提示「带速在合理范围」（中，确认缺陷）
- 问题：只校验 D1/D2/a，`n1` 与 `P` 未校验。n1=0/负值时 `v<=0`，`Fe` 被强制为 0，F1/F2/F0/Fq 全 0；P=0 且 n1=0 时还命中「✓ 带速 … 在合理范围（5~25 m/s）」的成功文案（0 不在 5~25）。
- 证据：`tools/machinery/calc-lifespan-belt.html:251-259`（读取 n1/P、仅三项校验）、`:289`（`Fe = v>0 ? P/v : 0`）、`:339-346`（带速判定与成功文案）。
- 复现：D1=100、D2=300、a=500、n1=0、P=5.5 → v=0.00、Fe=0、F1/F2/F0/Fq 全 0，仅提示带速偏低；n1=0、P=0 → v=0.00，提示「✓ 带速 0.00 m/s 在合理范围（5~25）」。
- 影响：`tools/machinery/calc-lifespan-belt.html`。5.5kW 传动在 0 转速下显示 0 张力，结果可被复制；P=0 的成功提示与判定阈值自相矛盾。
- 方案：`n1>0`、`P>0` 纳入校验并逐项标红；`Fe` 仅在 `v>0 && P>0` 时计算，否则中止；带速成功分支增加 `v>=5 && v<=25` 条件。

### MM-H22 齿轮页斜齿/锥齿的压力角是死输入；db 与锥齿 df₁ 公式错误但未渲染（中，确认缺陷）
- 问题：`αn` 只参与 `db`，而斜齿结果卡不显示 db；锥齿完全不使用 αn。斜齿/锥齿下改压力角输出一字不变。另有 `db` 用 `tan²β`（正确应为 `1/cos²β` 即 `1+tan²β`），锥齿 `df1` 用 `sinδ`（正确为 `cosδ`），两者当前均未渲染。
- 证据：`tools/machinery/calc-gear-3.html:222-226`（读取/校验 αn）、`:258-265`（αn 仅进 db，`:264`）、`:271-274`（斜齿只输出 mt/d/da/df/zv/p）、`:287-300`（锥齿只输出 da1/dm1，`:288` 的 df1 未输出）。
- 复现：斜齿 mn=2、z=20、β=15：αn=20 与 αn=45 输出均为 d=41.411、da=45.411、df=36.411、mt=2.070、zv=22.19、p=6.283。db 代码 41.216mm，正确 38.755mm（高 6.3%）；锥齿 m=4、z1=20、z2=40：df1 代码 75.707mm，正确 71.414mm（高 6.0%）。
- 影响：`tools/machinery/calc-gear-3.html`。压力角输入在两种模式下是死输入，用户会以为已参与计算；两处错误公式一旦恢复展示即产生错误尺寸。
- 方案：斜齿/锥齿隐藏 αn 或改为显示端面压力角/基圆直径；db 改为 `d·cosβ/sqrt(cos²β+tan²αn)`；df1 改为 `d−2hf·cosδ`；若暂不展示则删除未用变量。

### MM-H23 压缩机页进气温度只查 NaN，−273.1℃ 时质量流量 7 万 kg/min（中，确认缺陷）
- 问题：温度输入 HTML 限 −20~60℃，但 JS 只 `isNaN(t)`，不校验上下限；`tempK=t+273.15`、`tempFactor=293.15/tempK` 在 t→−273.15 时趋于 Infinity，t=−300 时为负，质量流量随之为 Infinity/负值，页面无报错。
- 证据：`tools/machinery/pressure-flow-4.html:135`（min/max）、`:195-202`（只查 isNaN）、`:221-223`（温度系数与质量流量）、`:238-239`（显示）。
- 复现：默认 q=10、p=0.7，t=−273.1 → tempK=0.05、温度修正系数 5863、质量流量 70,356 kg/min（正常 20℃ 为 12.00）；t=−300 → 系数 −10.918、质量流量 −131.02 kg/min；t=−273.15 → Infinity，卡片被替换为「—」但仍无提示。
- 影响：`tools/machinery/pressure-flow-4.html`。温度是唯一影响质量流量的输入，越界时输出荒谬值或「—」，用户无法判断是输入错误还是模型限制。
- 方案：校验 `t>=-20 && t<=60`，越界标红并中止；`tempK<=0` 时单独提示「低于绝对零度」；温度系数只在合法区间显示。

### 覆盖清单
- `tools/machinery/detector-strength-lifespan.html`：1 高（MM-H14）。
- `tools/machinery/detector-pressure-torque.html`：1 中（MM-H15）。
- `tools/machinery/thread-recognize.html`：1 高 + 1 中（MM-H16、MM-H17）。
- `tools/machinery/tolerance-1.html`：1 高 + 1 中（MM-H18、MM-H19）。
- `tools/machinery/calc-lifespan-belt.html`：2 中（MM-H20、MM-H21）。
- `tools/machinery/calc-gear-3.html`：1 中（MM-H22）。
- `tools/machinery/pressure-flow-4.html`：1 中（MM-H23）。
- `tools/machinery/torque-1.html`：未发现中/高缺陷；9550 系数、`T2=T1·i·η`、`n2=n1/i` 与四项正数校验均正确，档位效率仅作保守取值，不记缺陷。
- 编号：本批新增 `MM-H14`–`MM-H23`（3 高 / 7 中），续接 `MM-H13`，不重号。
- 验证声明：仅源码阅读 + node 内存复算（形位公差另对照 GB/T 1184-1996 公开表值核对系数）；未开浏览器、未跑 `run_gates.py` / `_build.py`、未做英文态/移动端/线上验证。本批未修改任何工具页或构建产物。
