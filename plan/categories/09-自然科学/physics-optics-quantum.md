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
