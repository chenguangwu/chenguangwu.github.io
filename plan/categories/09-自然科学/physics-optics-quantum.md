# 物理/光学/量子 · tools/{physics 类目录,astronomy,optics,quantum,kinematics,dynamics,thermodynamics,acoustics,fluid}（~250 页）

## 已知问题
## 功能缺陷
- ~~天文页缺「当前位置可见行星」（静态星历表月度数据模块）。~~ ✅ 2026-10-26 已落地（observation-conditions 新增「🪐 当日行星可见性」：JPL 近似轨道要素算水金火木土距角/晨昏方位/黄道位置/观测评价）

## 优化点
- S7 引据：CODATA 常数出处标注。→ 已落地 60 页（2026-10-26 十三批）：第一批 astronomy 5 页（gravitational-force / schwarzschild-radius / light-travel-time / stellar-parallax / hubble-redshift-distance），第二批 quantum 4 + fluid 1（photon-energy / boltzmann-population / bohr-orbit-radius / compton-wavelength / hydrostatic-pressure），第三批 thermo 1 + kinematics 2 + optics 1（ideal-gas-pressure / free-fall-time / projectile-max-height / refractive-index-speed），第四批 nuclear 2 + quantum 2 + chemistry 1（mass-defect / binding-energy / stefan-boltzmann-power / wien-displacement / mass-to-moles），第五批 dynamics 3 + acoustics 1（weight-force / static-friction-max / kinetic-friction / sound-speed-air），第六批 electrical 1 + materials 1 + thermo 3（wire-resistance / linear-thermal-expansion / charles-law / entropy-change / adiabatic-tv），第七批 astronomy 1 + quantum 4（kepler-third-period / de-broglie-wavelength / heisenberg-uncertainty / hydrogen-energy-level / cyclotron-frequency），第八批 nuclear 4（carbon-dating-age / radioactive-decay / half-life-from-lambda / activity，¹⁴C 剑桥 5730±40a 与利比约定 5568a、ln2、N_A、居里 3.7e10 Bq）；各页加「📐 物理常数/核数据引据」表（数值+单位+出处，CODATA 2018 / 新 SI 定义值 / IAU 2015 B3 / IAU 2012 B2 / ISO / IAPWS / AME2020 / CIPM / NASA / IEC 60028 / ASM / ASTM / NIST / ITS-90 / IAEA / ICRU），第九批 astronomy 1 + fluid 3（apparent-magnitude-distance / buoyancy-force / kinematic-viscosity / capillary-rise，含 IAU 2015 B2 秒差距与 M_bol,☉=4.74、L_0=3.0128e28 W、IAPWS-95 水密度与粘度、IAPWS 1994 表面张力、UNESCO 海水 1025、ISO 2533 空气密度），第十批 optics 3 + thermo 2（rayleigh-criterion / resolving-power / doppler-optical / heat-conduction / boyles-law，含瑞利系数 1.21967 = j₁,₁/π 精确数学常数、CIE 1924 明视觉峰值 555 nm、SI c、ASM/CRC 导热系数、ISO 2533 atm 与 R），第十一批 thermo 5（humid-air-enthalpy / convective-heat-rate / cp-cv-ratio / gay-lussac-law / diesel-efficiency，含 ASHRAE 湿空气 c_p,a=1.006 与 c_p,v=1.86、IAPWS-IF97 0 ℃ 汽化潜热 2501 kJ/kg、R_a=287.042、ASHRAE 对流换热系数区间、Mayer 关系式 c_p−c_v=R、γ 理论值 5/3 与 7/5），第十二批 chemistry 5（poh-to-ph / boiling-point-elevation / arrhenius / gibbs-free-energy / gas-density，含水的离子积 K_w=1.0e-14 与 pK_w 精确值 13.997（CODATA 2018/IUPAC）、pK_w 随温度变化（0 ℃≈14.94、100 ℃≈12.26）、CRC 依数性常数 K_b/K_f（水 0.512/1.86、苯 2.53/5.12、乙醇 1.22/1.99）、R、IUPAC 标准态 p°=100 kPa 与 c°=1 mol/L、干空气 M=28.96546e-3、理想气体摩尔体积 22.41396954 L/mol），第十三批 electrical 4（voltage-drop / wire-gauge-selector / calc-1 / voltage-9，含 IEC 60028 铜 0.017241 与铝 0.028264 及 α₂₀、IEC 60364-5-52 载流量与 30 ℃ 基准、敷设降容系数；**并明确压降限值与降容为工程经验值，不得冒称标准规定值**）。其余物理/天文/化学/电气页待续批。
- ~~S3 分步：透镜/成像光路图（SVG 动态）。~~ ✅ 2026-10-26 已落地（thin-lens-equation 新增「🔍 成像性质与光路示意」：成像性质文字 + SVG 三条特殊光线光路图）

## 受影响范围
- tools/optics/（40）、tools/quantum/（28）、tools/astronomy/、tools/kinematics/、tools/dynamics/、tools/thermodynamics/、tools/acoustics/（56）、tools/fluid/、tools/optical/（40）（~250 页）

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 折射明细固定显示全反射（高，确认源码缺陷）
- 证据：`tools/optics/snells-law.html:266-276,286-306` 默认 n₁=1、n₂=1.5、入射角 30°，主结果约 19.471°，附属表却固定写「发生全反射」，CSV 导出读取该表。
- 影响：`tools/optics/snells-law.html`；TBKit 渲染时正常折射被记录成全反射。
- 方案：结果与导出共用求解状态；覆盖正常折射、临界角和全反射，并提供可核对的角度明细。

### 棱镜空输入产生伪结果并保留旧表（高，确认源码缺陷）
- 证据：`tools/optics/prism-deviation.html:207-217,224-248` 默认 n=1.5、A=10° 计算后清空 n，主计算按 0 处理并显示 -10°；附属表因空值返回，保留上次数据。
- 影响：`tools/optics/prism-deviation.html`，主结果、旧明细和导出可能互相矛盾。
- 方案：区分空值和数值 0，非法输入清除结果及禁用导出；给出小顶角近似条件与可核对算例。

### 里德伯量子数先校验后取整产生零能级（中，确认源码缺陷）
- 证据：`tools/quantum/rydberg-wavelength.html:237-257,279-288` 输入低能级 0.4、高能级 2 通过正数检查后被四舍五入为 0；相等能级也使波数为零。
- 影响：`tools/quantum/rydberg-wavelength.html`，无效能级被接受，计算出现非有限值。
- 方案：计算前要求正整数且能级不同，直接提示而不静默取整；提供常见跃迁预设和系列归属。

### 低于阈值时负能量差被称作最大动能（中，确认源码缺陷）
- 证据：`tools/quantum/photoelectric-effect.html:213-220,232-245` 频率 1e14 Hz、功函数 2 eV 时页面判定无法逸出，却显示约 -1.586 eV「最大动能」；该负值是 hf−φ 能量差，不是已逸出电子动能。
- 影响：`tools/quantum/photoelectric-effect.html`，解释与结果/明细产生物理概念误导。
- 方案：低于阈值明确显示「无光电子，最大动能不适用」，若展示有符号能量差须另命名，统一导出并补阈值算例。

### 覆盖
- 本轮抽查上述光学及量子 4 页；仅源码和数值推导，未进行浏览器实测、线上验证，其余页面未逐页覆盖。

## 2026-11-03 续查（并行批 I）

### PQ-01 负光强被当成有效值，吸收占比爆到万亿级（中，确认）
- 描述：入射光强无任何上下限校验，负值照常代入马吕斯定律，占比分母又被 `Math.max(I0, 1e-9)` 钳到 1e-9，两处叠加后输出量纲上荒谬的百分比。
- 证据：`tools/optics/malus-law.html:207`（`num()` 把非法值兜底为 0，无守卫）、`:211`（I = I0·cos²θ）、`:214-215`（被吸收光强与占比）、`:237`（明细表同式）。node 复算：`I0=-100, θ=60` → I=-25.00、被吸收 -75.000、占比 **-7500000000000.00 %**（正常区间应为 0–100 %）。
- 同页次生：`I0` 留空 → 主结果卡片显示「透射光强 0.00 / 占比 0.00」，而 `:230` 的明细表因 `isFinite` 失败提前 return，保留上一次的 25.00 —— 主结果与明细/CSV 互相矛盾。
- 影响：`tools/optics/malus-law.html`，用户误填负号或清空输入即得到自相矛盾、不可解释的结果，且无任何提示。
- 方案：要求 I₀ ≥ 0 且为有限值，非法输入清空结果并禁用导出；占比统一按 `I0>0` 才计算，去掉 `max(1e-9)` 兜底改为显式提示；空值走与明细同一状态分支。

### PQ-02 入射侧折射率取 0 时静默伪造折射率比（中，确认）
- 描述：`n₁=0` 未被拦截，`n₂/n₁` 先按 Infinity 求角（得 90°），随后比值又用 `n2/(n1||1)` 静默替换成 `n₂/1`，页面上出现一个根本不存在的 1.5000。
- 证据：`tools/optics/brewster-angle.html:267`（`Math.atan(n2/n1)`）、`:270`（`(n2/(n1||1))`）、`:234`（守卫 `var __D={};` 为空对象 ⇒ 分母检测恒不触发）、`:265`（守卫只拦空值/non-number）。node 复算：`n1=0, n2=1.5` → θ_B=90.000°、折射率比 **1.5000**、互补角 0.000°；`n1=-1, n2=1.5` → θ_B=-56.310°、比值 -1.5000 亦被接受。
- 影响：`tools/optics/brewster-angle.html`，物理上不存在 n₁=0，页面却给出看似正常的比值并写入明细表与 CSV；负折射率同样无提示。
- 方案：把 n₁、n₂ 纳入 `__D` 分母/正值校验（n₁≠0 且两者 > 0）；非法时不渲染比值，明确提示「入射侧折射率为 0 时无定义」，并复核 `n1||1` 这类兜底写法。

### PQ-03 三个预设给出完全相同的布儒斯特角（中，确认）
- 描述：「示例 2×」「示例 0.5×」只按比例同步放大 n₁ 与 n₂，比值恒为 1.5，导致三个预设输出逐位一致，标签语义失效。
- 证据：`tools/optics/brewster-angle.html:306-310`（默认 1.0/1.5、2× 为 2/3、0.5× 为 0.5/0.75）。node 复算三者均 → **56.3099°**。
- 影响：`tools/optics/brewster-angle.html`，预设按钮看起来可用但点击后结果不变，用户会误判工具未响应。
- 方案：预设改为改变比值（如空气→玻璃 1.5、空气→水 1.33、玻璃→水 1.33/1.5），或在标签中直接标注目标介质而不是「2×/0.5×」。

### PQ-04 输入守卫把分子误标成「分母不能为 0」（低，确认）
- 描述：`__D` 把三个输入全列为分母，但条纹间距公式中 λ 与 L 都在分子，只有缝距 d 是分母，报错文案与实际公式相反。
- 证据：`tools/optics/young-fringe.html:236`（`__D={"lam":…,"L":…,"d":…}`）、`:212`（文案「是本计算的分母，不能为 0」）、`:269`（`dy=lam*L/d*1000`）。复现：`lam=0` 或 `L=0` → 输出「⚠「波长 λ (纳米)」是本计算的分母，不能为 0。」
- 影响：`tools/optics/young-fringe.html`，用户被指向错误的物理原因（λ=0 时问题是「无条纹」而非除零）。
- 方案：`__D` 只保留 `d`；λ=0、L=0 用各自专属提示（「波长为 0 无干涉条纹」「屏距为 0 无视场」），并核对同批模板页的 `__D` 是否也过度收录。

### PQ-05 康普顿散射角未限幅，270° 与 90° 同值且空值静默为 0（中，确认）
- 描述：散射角只在三角函数里使用，未限制到 0–180°，超出范围与负角一律按余弦周期折叠；空值又被 `num()` 兜底为 0，主结果直接显示 0.0000 pm。
- 证据：`tools/quantum/compton-shift.html:211-212`（θ 直接 ×π/180 代入 `1−cosθ`）、`:229`（明细表遇非有限值提前 return）。node 复算：θ=270° → **2.4263 pm**（与 90° 完全相同）、θ=315° → 0.7106 pm（与 45° 相同）、θ=0/空 → 0.0000 pm。
- 同页次生：`:120` 公式框只写「λ_C ≈ 2.43 pm、90° Δλ ≈ 2.43 pm」，未给出 Δλ 完整表达式与角度定义域。
- 影响：`tools/quantum/compton-shift.html`，越界角被当成合法散射角；空输入时主结果为 0 而明细保留旧值。
- 方案：限定 0° ≤ θ ≤ 180° 并提示越界；空值与其他页统一走「请填写」分支；公式框补 Δλ=(h/m_ec)(1−cosθ) 及定义域。

### PQ-06 量子数被静默取整，且预设把质量/阱宽置 0 导致明细 Infinity（高，确认）
- 描述：`n` 用 `Math.round()` 处理，0.4 变 0、1.5 变 2、-2 与 2 同值；更严重的是两个预设把参与分母的 `m`、`L` 直接写成 0，主结果被守卫拦下，明细表却照常渲染出 Infinity。
- 证据：`tools/quantum/infinite-well-energy.html:273`（`Math.round(num('n'))`）、`:274`（E = n²h²/(8mL²)）、`:240`（`__D` 仅含 m、L）、`:293`（明细守卫只判 `isFinite`，0 是有限值故放行）、`:295-300`（`toExponential/toFixed` 对 Infinity 输出字符串 `Infinity`）、`:315-316`（预设 `{n:'2', m:'0', L:'0'}` 与 `{n:'0.5', m:'0', L:'0'}`）。node 复算：n=0.4 → n=0 → **0.000e+0 J / 0.0000 eV**；n=-2 → 1.5040 eV（与 n=2 相同）；n=1.5 → 1.5040 eV；预设场景 E=Infinity。
- 影响：`tools/quantum/infinite-well-energy.html`，与本页引据表「E₁≠0」自相矛盾；点「示例 2×/0.5×」得到「主结果报错 + 明细/CSV 为 Infinity」的分裂状态。
- 方案：n 必须为正整数，直接提示而非取整；m、L 要求 >0 且有限；明细渲染前复用同一校验状态，杜绝 Infinity 落表；修正两个预设为真实可算值。

### PQ-07 级次 0 被当作暗纹，两个预设把波长置 0 得到全零角度（高，确认）
- 描述：`m` 取整后未排除 0（0 级是中央亮纹而非暗纹），而「示例 2×/0.5×」预设把 `λ` 写成 0，于是 `sinθ=mλ/a=0`，暗纹角与第一暗纹角全部输出 0.0000°，且无任何提示。
- 证据：`tools/optics/single-slit-diffraction.html:268-270`（`m=Math.round(num('m'))`、`s=m*lam/a`、`th=Math.asin(s)`）、`:236`（`__D` 只含 `a`，λ=0 放行）、`:271-274`（三项输出）、`:313-314`（预设 `{a:'0.0002', lam:'0', m:'2'}`、`{a:'0.0001', lam:'0', m:'0.5'}`）。node 复算：m=0 → **θ=0.0000°、sinθ=0.00000**；m=0.4 → 同样 m=0；点「示例 2×」→ λ=0 → θ=0.0000°、θ₁=0.0000°。
- 影响：`tools/optics/single-slit-diffraction.html`，用户点预设即得到物理上不存在的「0° 暗纹」，且明细与 CSV 同样错误。
- 方案：m 限定为非零整数（0 与负数提示「暗纹级次从 ±1 起」）；λ 纳入正值校验；修正预设波长并补一组可手算算例。

### PQ-08 塞曼分裂空值输出 0 且明细保留旧值，玻尔磁子被当成结果卡（低，确认）
- 描述：`B` 无守卫，留空即按 0 算，四项输出全为 0；明细表因非有限值提前 return 而保留上一次数值；同时把常量 μ_B 单独列成一张「结果」卡。
- 证据：`tools/quantum/zeeman-splitting.html:210-218`（`B=num('B')`、`dE=muB*B`）、`:216`（`(muB).toExponential(4)` 作为「玻尔磁子 (J/T)」结果项）、`:231`（明细遇 NaN return）。node 复算：B=0 → ΔE **0.000e+0 eV / 0.000e+0 meV**；B=1 → 5.788e-05 eV（与说明一致）。
- 影响：`tools/quantum/zeeman-splitting.html`，空输入时主区显示 0 能级分裂（看似「无分裂」）而明细保留旧场强的数据；常量被包装成随输入变化的「结果」易被误读。
- 方案：B 留空/非正值提示而非 0 兜底；主结果与明细共用校验；μ_B 移到引据/常量表，不作为结果卡。

### PQ-09 电子对阈值页假输入、空预设与失效的 history/diff（低，确认）
- 描述：唯一输入 `dummy` 不参与任何计算；三个预设的 `values` 均为空对象；历史记录只写常量 `H`，页面无 `H` 元素，恢复必然无效；diff 也只监视常量。
- 证据：`tools/quantum/pair-production-threshold.html:126-131`（`id="dummy"` 标「（常量计算）」）、`:211-219`（`calcTool` 只读常量，不读 dummy）、`:241`（`TBKit.history.record({H:H})`）、`:244`（`diffBox(...,['H'])`）、`:252-256`（三个 `values:{}`）。node 复算：阈值 1.0220 MeV / 1.0220e+6 eV / λ=1.2132e-12 m，与 `dummy` 取值无关。
- 影响：`tools/quantum/pair-production-threshold.html`，输入框与预设、历史、差异四个控件均无实际作用，用户反复输入无反馈。
- 方案：要么去掉假输入改成纯常量卡片，要么改为真实输入（入射光子能量 MeV）并判断是否越过阈值、给出超出阈值时的动能；预设改为 1.022/2/10 MeV；history 只记录真实字段。

### PQ-10 电子质量常数与引据标称版本不一致（低，待验证）
- 描述：多个量子页使用 `ME=9.10938356e-31`（CODATA 2014），而引据表标称 CODATA 2018（2018 值为 9.1093837015e-31），属引据一致性问题；因显示位数有限，当前输出看不出差异。
- 证据：`tools/quantum/compton-shift.html:210`、`tools/quantum/infinite-well-energy.html:272`、`tools/quantum/pair-production-threshold.html:212`（均 `ME=9.10938356e-31`）；`tools/quantum/compton-shift.html:156` 引据行写「CODATA 2018」。node 复算：λ_C = 2.426310 pm（2014 与 2018 在 6 位小数处相同，相对差异 1.55e-6 %）；阈值 1.0220 MeV（4 位小数相同）。
- 影响：`tools/quantum/compton-shift.html`、`infinite-well-energy.html`、`pair-production-threshold.html`，当前显示值不受影响，但引据与实现版本不符，后续提高精度或换位数时会暴露。
- 方案：统一把电子质量换成 CODATA 2018 值并在引据表注明取值年份；或把引据表改标 CODATA 2014，二者取其一，避免「标称 2018、实算 2014」。

### 留存优化
- 本批 8 页均存在「主结果与明细表各自为政」的共性结构：`calcTool()` 只做空值兜底，`__…Extras()` 用 `isFinite` 独自判空并提前 return，两者状态不同步。建议后续统一成一个 `readInputs()` + 一套校验结果，主区与明细/CSV 共用，避免「主区 0、明细旧值」。
- 预设生成器是全站模板产物，出现了把关键量写成 0（`infinite-well-energy` 的 m/L、`single-slit-diffraction` 的 λ）和等比缩放导致输出不变（`brewster-angle`）两类问题；建议对 optics/quantum 全量扫一遍 `values` 里含 `'0'` 或三项同比例缩放的预设。
- `__tbInputGuard` 的 `__D` 由「真浏览器逐项置零探测」生成，本批已见过度收录（`young-fringe` 把分子当分母）与完全为空（`brewster-angle`）两种失真；建议改为人工按公式分母维护并加注释。
- 常量与引据：本批 4 个量子页重复声明同一组常量（H/C/ME/EV/A0/RY/B_WIEN），其中 A0、RY、B_WIEN 多数页未使用；可收敛为共享常量表，同时统一到 CODATA 2018。

### 续查覆盖
- 本批实查 8 页：`tools/optics/malus-law.html`、`brewster-angle.html`、`young-fringe.html`、`single-slit-diffraction.html`、`tools/quantum/compton-shift.html`、`infinite-well-energy.html`、`zeeman-splitting.html`、`pair-production-threshold.html`。
- 前批已覆盖（本批未重复）：`tools/optics/snells-law.html`、`prism-deviation.html`、`tools/quantum/rydberg-wavelength.html`、`photoelectric-effect.html`。
- 方法：仅静态阅读源码 + node 内存复算（输入→输出逐条记录如上）；**未**开浏览器、未做英文态/繁体态、未做移动端、未跑 `_build.py`/`run_gates.py` 或任何门禁，也未验证线上表现。
- 未覆盖：`tools/optics` 余 15 页、`tools/quantum` 余 21 页、`tools/optical`(41)、`tools/astronomy`(24) 及 `tools/kinematics|dynamics|thermodynamics|acoustics|fluid`，留待后续批次。

## X 批 · 物理/光学（2026-11-04）

### PQ-11 多普勒页把有符号速度约定封死，远离场景无法计算（高，确认）
- 描述：两个速度输入按标签是「朝向为正」的有符号量，但输入守卫把 vo、vs 列入「不能为负值」，导致观察者后退、声源后退等页面自己承诺的场景根本无法输入；「声源远离」卡片另用 `(v+vs)` 替代，与用户输入的实际符号语义脱节。
- 证据：`tools/science/doppler-effect.html:130-137`（标签「观察者速度 v₀（朝向源为正）」「波源速度 v_s（朝向观察者为正）」）、`:254`（`__N` 把 f/v/vo/vs 全部登记为不能为负）、`:287`（主式 `f*(v+vo)/(v-vs)`）、`:289`/`:312`（「声源远离」固定用 `(v+vs)`）。静态推导：vo=-10 被守卫直接拦下并中止计算。
- 影响：`tools/science/doppler-effect.html`，页面标称的双向（接近/远离）能力实际只剩「接近」一半，用户按标签填负值得到「观察者速度不能为负值」。
- 方案：仅 f、v 限非负，vo、vs 允许负值；主式统一按 `f′ = f(v+vo)/(v−vs)` 计算一次，并据结果给出「接近/远离」文字判定，不要用替换分母的卡片冒充远离分支。

### PQ-12 球面镜页明示「凸面镜 f 为负」却拒绝负焦距（高，确认）
- 描述：公式框、输入标签和深挖算例都写明凸面镜取 f<0，但输入守卫把 f 登记为「不能为负值」，凸面镜（后视镜）这一半功能被直接屏蔽，页面自带算例也无法复现。
- 证据：`tools/optics/mirror-equation.html:121`（「凹面镜 f 为正、凸面镜 f 为负」）、`:128`（标签「焦距 f（凹正凸负）」）、`:247-256`（`__N` 含 f，返回「焦距 f（凹正凸负） (m)」不能为负）、`:365`（算例 f=−0.2、d_o=0.5 → d_i=−0.1429 m）。
- 影响：`tools/optics/mirror-equation.html`，明确承诺的凸面镜成像无法计算，与页面文案、FAQ、算例自相矛盾。
- 方案：f 允许负值，仅拦截 f=0 与非有限值；补凸面镜算例（f=−0.2/d_o=0.5 → d_i=−0.1429 m、虚像缩小正立）回归。

### PQ-13 光子能量页两个预设把波长写成 0，点击即报错（高，确认）
- 描述：「示例 2×」「示例 0.5×」两个预设的 `lam` 均为 `'0'`，而 λ 又被守卫列为分母，点预设后不再计算，而是显示「波长 λ (m) 是本计算的分母，不能为 0」。
- 证据：`tools/quantum/photon-energy.html:342-343`（两条 `values:{lam:'0'}`）、`:269`（`__D` 含 lam）、`:275-277`（分母报错文案）。
- 影响：`tools/quantum/photon-energy.html`，两个预设按钮形同虚设，用户点「示例」得到的不是示例结果而是错误提示。
- 方案：预设改为真实波长（如 250e-9 / 1000e-9），并按 2×/0.5× 语义给出可核对算例。

### PQ-14 重力势能页空值静默为 0，主区与明细/CSV 分裂（中，确认）
- 描述：`num()` 把空值兜底为 0，主结果直接按 `mgh=0` 渲染「0.0 J」；明细侧另用独立校验，遇空值提前 return，保留上一轮的有效数据，形成主区 0、明细旧值的分裂。另「高度复算」= U/(m·g) 恒等于输入 h，作为独立指标与图表系列具有误导性。
- 证据：`tools/science/gravitational-potential.html:215`（`num` 空值→0）、`:217-223`（U=mgh 与三张卡）、`:237`（`__gravitational_potentialNum` 遇空值 NaN 提前 return）、`:239-246`（明细/CSV 沿用旧值）、`:222`/`:244`（「高度复算」）。node 复算：默认 m=10、g=9.81、h=5 → 490.5 J；清空 h 后主区 0.0 J、明细仍 490.5。
- 影响：`tools/science/gravitational-potential.html`，空输入被当成「势能为 0」的正常结果，且导出与页面正文不一致。
- 方案：加「必填且有限」守卫，空值不渲染结果并禁用导出；明细复用同一校验状态；「高度复算」若保留须标为校验项，否则与图表同删。

### PQ-15 磁通量反解忽略夹角，B/S 结果偏大 cosθ 倍（中，确认）
- 描述：`Φ = BS cosθ` 正解含 cosθ，但反解 B 和 S 时直接 `phi/S`、`phi/B`，完全不读用户填写的夹角；θ≠0 时结果系统性偏差。
- 证据：`tools/science/physics-calculator.html:401-404`（`phi_bs` 分支：`:402` 正解含 cosθ，`:403` B=phi/S，`:404` S=phi/B）。node 复算：φ=1 Wb、S=2 m²、θ=60° → 页面 B=0.5000 T，正确值 1.0000 T。
- 影响：`tools/science/physics-calculator.html`，单页计算器的磁通量反解给出错误数值且无提示。
- 方案：反解并入 cosθ（B=φ/(S·cosθ)、S=φ/(B·cosθ)），cosθ=0 时提示「磁通量与面积垂直时无解」。

### PQ-16 折射定律入射角未限幅，100°/负角被当合法（中，确认）
- 描述：θ₁ 不经任何范围校验就投入 `sin`，大于 90° 或负值按三角函数周期继续计算，输出看似正常的折射角。
- 证据：`tools/science/physics-calculator.html:449-457`（`:451` 直接 `Math.sin(theta1.v*π/180)`，`:457` 反解 θ₁ 亦无校验）。node 复算：n₁=1、n₂=1.5、θ₁=100° → θ₂=41.036°；θ₁=−30° → θ₂=−19.471°。
- 影响：`tools/science/physics-calculator.html`，物理上不存在的入射角被接受，折射角与临界角判断随之失真。
- 方案：限定 0°≤θ₁≤90°（含 90° 边界），越界明确提示；θ₂ 同理限定 0–90°。

### PQ-17 光电效应低于阈值仍显示负的「最大初动能」（中，确认）
- 描述：`Eₖₘₐₓ = hf − W₀` 不做阈值判断，hf<W₀ 时把负值照常标成最大初动能。
- 证据：`tools/science/physics-calculator.html:496-500`（`:498` 直接 `hval*f.v-W0.v`）。node 复算：f=1e14 Hz、W₀=2 eV（3.204e-19 J）→ −2.542e-19 J，页面仍显示为「最大初动能」。
- 影响：`tools/science/physics-calculator.html`，低于阈频时给出负动能，概念误导（与前一页 photoelectric-effect 同类缺陷）。
- 方案：hf<W₀ 时显示「无光电子逸出，最大初动能不适用」，若展示 hf−W₀ 须另命名并注明为有符号能量差。

### PQ-18 薄透镜在 d_o=f 时输出「—/-—」与 Infinity 明细（中，确认）
- 描述：守卫只拦截 f=0、d_o=0，未处理 d_o=f；此时像距发散，主区字符串被 `/Infinity/` 替换成「—-」，明细/CSV 保留原始 `Infinity`，SVG 坐标被钳到边界但仍按无穷放大率绘制。
- 证据：`tools/optics/thin-lens-equation.html:239`（`__D` 仅判等于 0）、`:284`（`di=1/(1/f-1/do)`）、`:302`（`calcRay` 同式）、`:319-320`（`xI=xL+di*scale` 后钳位）。node 复算：f=0.1、d_o=0.1 → d_i=Infinity、m=−Infinity，`toFixed(4)` 得到字符串 `Infinity`。
- 影响：`tools/optics/thin-lens-equation.html`，物距等于焦距（成像于无穷远，物理上合法）时出现「像距 —、放大率 -—、像性质 实像」的分裂显示，光路图失真。
- 方案：|d_o−f| 小于阈值时判「成像在无穷远」，清空像距/放大率/光路图并提示；明细与 CSV 走同一状态分支。

### PQ-19 折射率页允许介质光速超过真空光速，n<1 与 3×10¹⁷ 联动值（中，确认）
- 描述：只拦截 v=0，不校验 v≤c；v>c 时 n<1、v 为负时 n 为负，「速度差与光速之比倒数」又用 `max(c−v,1e-9)` 兜底，输出天文数字。
- 证据：`tools/optics/refractive-index-speed.html:268`（`__D` 只含 v）、`:301-306`（n=c/v 与 `c/Math.max(c-v,1e-9)`）、`:386`（FAQ 自己承认 n<1 说明输入有误）。node 复算：v=4e8、c=3e8 → n=0.7500、末项 3e17。
- 影响：`tools/optics/refractive-index-speed.html`，狭义相对论上不可能的输入被当作正常值，主卡与明细同时给出错误物理量。
- 方案：要求 c>0 且 0<v≤c，越界提示「介质光速不可能超过真空光速」；删除「速度差与光速之比倒数」这类无物理意义卡片，或改成 n−1。

### PQ-20 球面镜焦距为 0 未拦截，得到「像距 0、放大率 0」伪结果（中，确认）
- 描述：守卫的 `__D` 只列 d_o，f=0 放行；`1/f` 为无穷，`di=1/(∞−1/do)` 收敛成 0，页面据此判「虚像、放大率 0」。
- 证据：`tools/optics/mirror-equation.html:235`（`__D` 仅 `do`）、`:280`（di 计算）、`:282-283`（输出卡）。node 复算：f=0、d_o=0.5 → d_i=0.0000、|m|=0.0000。
- 影响：`tools/optics/mirror-equation.html`，无意义的焦距被包装成一组正常数值。
- 方案：f 与 d_o 均须非零且有限，f=0 单独提示「焦距不能为 0」；主区、明细、CSV 共用该状态。

### PQ-21 多普勒在 v_s=v 时主区「—」、明细/CSV 为 Infinity（中，确认）
- 描述：分母 `v−vs` 为 0 时没有任何守卫（`__D` 为空对象），主区字符串被替换成「—」，明细表与导出却保留字符串 `Infinity`，Δf 同样失效。
- 证据：`tools/science/doppler-effect.html:242`（`var __D={}`）、`:287-290`（fp 与 Δf）、`:311-313`（明细同式）。node 复算：f=1000、v=343、vo=0、vs=343 → fp=Infinity。
- 影响：`tools/science/doppler-effect.html`，波源速度达到波速时页面既无物理解释，又出现主区与明细互相矛盾的输出。
- 方案：vs≥v 时提示「波源速度不能达到或超过波速」并停算；明细/导出与主区共用同一校验结果。

### PQ-22 光子能量接受负波长得负能量，差异框只监视常量 H（中，确认）
- 描述：λ 无符号校验，负值照算得负能量与负 eV；同页历史记录写入常量 H，`diffBox` 也只监视 `H`，差异面板永远没有差异。
- 证据：`tools/quantum/photon-energy.html:301-303`（H/C/EV 与 `E=H*C/lam`）、`:325-326`（明细表同式）、`:329`（`record({lam,H})`）、`:332`（`diffBox(...,['H'])`）。node 复算：λ=−500e-9 → E=−3.973e-19 J、−2.480 eV。
- 影响：`tools/quantum/photon-energy.html`，负波长被当作有效输入；差异对照功能形同虚设（假功能），无法反映波长变化。
- 方案：λ 须 >0 且有限，非法输入停算并禁用导出；diffBox 改监视 `lam`，历史记录不再写入常量 H。

### 覆盖
- 本批实查 8 页：`tools/science/physics-calculator.html`、`gravitational-potential.html`、`spring-oscillation-period.html`、`doppler-effect.html`、`tools/quantum/photon-energy.html`、`tools/optics/thin-lens-equation.html`、`mirror-equation.html`、`refractive-index-speed.html`。
- 页面名替换说明：`tools/physics/` 目录不存在，8 页实际分布在 `tools/science`（4）、`tools/quantum`（1）、`tools/optics`（3）；清单中的 `lens-equation`、`ray-optics`、`refraction-angle` 在仓库中无同名页，按「同目录顺延未审计页」分别取 `thin-lens-equation`、`mirror-equation`、`refractive-index-speed`（`snells-law` 已在前批覆盖，故未重复）。
- `spring-oscillation-period.html` 本批未发现符合入账口径的缺陷（仅 `__D` 把分子 m 误标为「分母」的文案问题，属低危，未计入编号）。
- 方法：仅静态读源码 + node 内存复算（关键输入→输出已逐条记录）；**未**开浏览器、未做英文态/繁体态与移动端、未跑 `_build.py`/`run_gates.py` 或任何门禁，也未验证线上表现。
