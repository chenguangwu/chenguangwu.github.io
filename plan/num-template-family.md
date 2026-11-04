# num() 空态模板族台账

> 生成日期：2026-11-05　|　静态扫描 + 真机探针交叉；真机证据来自 `/tmp/probe/out/interaction-invalid.jsonl`。

## 扫描口径

三条同时成立记为 **M1（高风险族）**：

1. 主计算函数（`calcTool()` 或 `calc()`）内用 `num()` 或 `parseFloat(...)||0` 取输入；
2. 该函数体内没有任何存在性守卫（无 `请填写` / `__tbInputGuard` / `value===''` / `!isFinite` / `isNaN(parseFloat(...))`）；
3. 同文件存在 `__<slug>Num(id)` 形式的 `isFinite` 助手，但只被同页辅助函数（`__<slug>Raw` / `Restore` / `Extras` / `resetForm`）调用，**主路径从不调用**。

## 三种模板形态

| 形态 | 特征 | 静态页数 | 说明 |
|---|---|---|---|
| M1 `num()` + 未接线 `__*Num()` | 守卫写对了但只服务 Extras | 232 | 本台账主体；62 页已由探针实测 `empty_bogus` |
| M2 `num()` 裸用，无助手 | 全文件没有 `isFinite` 版本可复用 | 242 | 同症状的兄弟变体，需逐页判断 0 是否合法 |
| M3 内联 `parseFloat(...)||0` | 无 `num()`、无助手 | 611 | 大量生成器/演示页混入，不可批量加守卫；必须先探针实测 |

## M1 清单（按目录分组，★ = 探针实测 `empty_bogus`）

| 目录 | 页数 | 探针确认 | slug |
|---|---|---|---|
| `tax` | 21 | 16 | ★ad-valorem-duty, ★break-even-taxable, capital-gains-effective, ★capital-gains-tax, corporate-income-tax, ★customs-duty, ★excise-tax, ★foreign-tax-credit, ★gift-tax, ★interest-income-tax, ★payroll-tax, ★property-tax, reverse-charge, ★sales-tax-addon, ★social-security-tax, ★specific-duty, stamp-duty, tax-credit, ★tax-on-discount, ★vat-from-exclusive, ★withholding-tax |
| `geometry` | 15 | 0 | angle-between-vectors, cone-frustum-volume, cone-volume, cube-properties, cylinder-volume, dot-product-2d, ellipsoid-volume, parabola-vertex, point-line-distance, pyramid-volume, pythagorean, rectangular-prism-volume, regular-polygon-area, sphere-surface-area, trapezoid-area |
| `robotics` | 14 | 12 | ★belt-linear-speed, ★cable-tension-pulley, ★centripetal-speed-limit, ★dc-motor-back-emf, end-effector-reach, ★forward-kinematics-2r, ★gear-ratio-torque, gravity-comp-torque, ★lead-screw-speed, ★lifting-torque, ★linear-accel-force, ★motor-power, ★motor-torque-current, ★rotational-inertia-torque |
| `civil` | 13 | 0 | carbonation-depth, cft-capacity, concrete-volume, concrete-wb-ratio, isolated-footing, masonry-bearing, one-way-slab, rc-beam-rebar, rebar-anchorage, rebar-weight, slope-stability-fos, two-way-slab, wind-load |
| `economics` | 10 | 7 | ★balance-of-trade, ★compound-amount, fisher-equation, ★fv-annuity, ★labor-force, ★okuns-law, ★pv-annuity, ★real-gdp, spending-multiplier, tax-multiplier |
| `energy` | 9 | 0 | daily-irradiation, energy-consumption, energy-cost, energy-from-power, fuel-heat-value, joule-heating, solar-panel-power, three-phase-power, wind-power-physics |
| `aerospace` | 7 | 5 | bank-angle-load, ★descent-rate, ★drag-force, ★lift-equation, ★lift-force, load-factor, ★thrust-required |
| `banking` | 7 | 5 | ★amortization-first-interest, ★continuous-compounding, daily-interest, ★effective-annual-rate, fisher-real-rate, ★net-worth, ★tax-equivalent-yield |
| `materials` | 7 | 4 | ★linear-thermal-expansion, mass-from-density, ★rule-of-mixtures, specific-heat-capacity, specific-weight, ★tensile-force-area, ★volumetric-strain |
| `mechanical` | 7 | 3 | beam-point-load, centrifugal-force, flywheel-energy, ★gear-ratio, ★lever-advantage, spring-rate, ★torque-power |
| `engineering` | 6 | 0 | axial-stress, bending-stress, cantilever-deflection, poisson-strain, pressure-vessel, section-inertia |
| `metrology` | 6 | 0 | calibration-uncertainty, gauge-repeatability, gauge-reproducibility, guard-band-95, least-count-error, resolution-uncertainty |
| `nuclear` | 6 | 0 | decay-fraction, effective-halflife, gamma-attenuation, mean-life-from-halflife, reaction-rate, survival-probability |
| `electromagnetism` | 5 | 0 | capacitors-parallel, capacitors-series, electric-power, force-wire-field, inductors-series |
| `insurance` | 5 | 1 | annuity-nsp, expected-claim-loss, ★ibnr-estimate, surrender-value, uw-margin |
| `investment` | 5 | 1 | portfolio-beta, present-value-inv, retention-ratio, sustainable-growth, ★yield-spread |
| `kinematics` | 5 | 0 | freq-from-omega, height-fall-distance, relative-velocity-1d, tangential-accel, uniform-displacement |
| `math` | 5 | 0 | exponent-solve, log-base, quadratic-discriminant, root-calc, slope-line |
| `securities` | 5 | 4 | annualized-vol, ★enterprise-value, ★market-cap, ★market-risk-premium, ★option-breakeven-put |
| `acoustics` | 4 | 0 | acoustic-impedance, combine-two-spl, sound-speed-air, spl-add |
| `astronomy` | 4 | 0 | apparent-magnitude-distance, moon-illumination, schwarzschild-radius, solar-declination |
| `meteorology` | 4 | 0 | isa-temperature, precipitation-rate, saturation-vapor-pressure, wind-direction |
| `parenting` | 4 | 0 | diaper-usage, feeding-amount-baby, formula-mixing, pumping-plan |
| `quantum` | 4 | 0 | angular-momentum-quant, mass-energy-equivalence, photon-flux, spin-magnetic-moment |
| `signal` | 4 | 2 | ★carrier-freq, cascade-gain-db, first-order-rise, ★pll-lock-range |
| `statistics` | 4 | 0 | correlation-r-squared, p, percentile-rank, probability-complement |
| `chemistry` | 3 | 0 | boiling-point-elevation, ph-to-h, solubility-product |
| `finance` | 3 | 0 | credit-card-grace-period, points-redemption-value, portfolio-return |
| `fluid` | 3 | 0 | chezy-velocity, hydrostatic-pressure, volume-flow-rate |
| `health` | 3 | 0 | milk-tea-calories, pregnancy-weight-gain, safe-period-calculator |
| `it` | 3 | 0 | phone-screen-sizes, regex-common, video-bitrate |
| `process` | 3 | 2 | measurement-uncertainty, ★tolerance-rss, ★tolerance-worst-case |
| `structural` | 3 | 0 | section-modulus-circle, thermal-strain, torsion-polar-j |
| `dynamics` | 2 | 0 | hooke-force, static-friction-max |
| `machinery` | 2 | 0 | bolt-preload, shaft-torsion |
| `optics` | 2 | 0 | focal-length-mirror, thin-film-min |
| `restaurant` | 2 | 0 | bbq-portion, hotpot-portion |
| `science` | 2 | 0 | hookes-law, newtons-second |
| `thermodynamics` | 2 | 0 | convective-heat-rate, humid-air-enthalpy |
| `construction` | 1 | 0 | cement-mortar-ratio |
| `decor` | 1 | 0 | ceiling-panel-quantity |
| `electrical` | 1 | 0 | home-load-estimate |
| `fun` | 1 | 0 | meditation-timer |
| `gardening` | 1 | 0 | balcony-sunlight |
| `healthcare` | 1 | 0 | bmr-calculator |
| `home` | 1 | 0 | washer-capacity |
| `hr` | 1 | 0 | annual-leave-prorate |
| `life` | 1 | 0 | drinking-water-plan |
| `metallurgy` | 1 | 0 | steel-profile-weight |
| `optical` | 1 | 0 | optical-path-length |
| `wedding` | 1 | 0 | wedding-banquet |
| `woodwork` | 1 | 0 | desk-dimensions |

## 已获真机证据的页（`empty_bogus`）

| # | 页面 | 清空后仍输出的伪结果（截断） |
|---|---|---|
| 1 | `aerospace/descent-rate` | 0.0下降率 (m/min)0.00下降率 (m/s)0.00水平速度 (m/s)0.000下降梯度 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 2 | `aerospace/drag-force` | 0.00阻力 D (N)0.0动压 q = ½ρv² (Pa)0.00阻力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 3 | `aerospace/lift-equation` | 0.00升力 L (N)0.0动压 q = ½ρv² (Pa)0.00升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 4 | `aerospace/lift-force` | 0.00升力 L (kN)0.0升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 5 | `aerospace/thrust-required` | 0.000所需推力 (kN)0.0动压 q = ½ρv² (Pa)0.00等效推力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 6 | `banking/amortization-first-interest` | 0.00首月利息 I₁0.00首月还本金0.000年利率 (%)0.0000首月利息占本金比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 7 | `banking/continuous-compounding` | 0.00连续复利终值 A0.00利息总额0.0000年实际收益率 (%)0.0000较年复利增益 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 8 | `banking/effective-annual-rate` | 0.000有效年利率 EAR (%)0.00000EAR (小数)0.0000EAR 高于名义利率 (百分点)0.0000与连续复利之差 (百分点) ⏐ 📋 复制结果⬇️ 导出 T |
| 9 | `banking/net-worth` | 0净资产 NW (元)0.00负债率 (%)0.000资产覆盖倍数0.00净资产占资产 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 10 | `banking/tax-equivalent-yield` | 0.000税后等效收益率 TEY (%)0.000应税需高出的百分点0.0边际税率 (%)0.0000免税溢价系数减一 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 11 | `economics/balance-of-trade` | 0贸易差额 BoT0.00差额占出口比 (%)0.000出口进口比0进出口总额 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 12 | `economics/compound-amount` | 0.00复利终值 F0.00利息总额 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 13 | `economics/fv-annuity` | 0.00年金终值 FV0.00利息总额 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 14 | `economics/labor-force` | 0劳动力 LF0.00失业率 (%)0.00就业率 (%)0.0000就业与失业人数比 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 15 | `economics/okuns-law` | 0.00失业率变化 Δu (百分点)0.00增长缺口0.00失业率变化幅值 (百分点)0.000相对增长缺口 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 16 | `economics/pv-annuity` | 0.00年金现值 PV0.00贴现总额 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 17 | `economics/real-gdp` | 0.00实际 GDP0.00价格扭曲部分0.00实际占名义比重 (%)0.00价格扭曲占比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 18 | `insurance/ibnr-estimate` | 0.00IBNR 准备金 (元)0.00已付赔款比例 (%)0.00已付赔款 (元)0.00最终赔款 (元) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 19 | `investment/yield-spread` | 0利差 Spread (bps)0.0000利差 (%)0.000基准收益率 (%)0.000对比收益率 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 20 | `materials/linear-thermal-expansion` | 0.000伸长量 ΔL (mm)0.0000热应变 (微应变)0.000000膨胀后长度 (m) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 21 | `materials/rule-of-mixtures` | 0.00复合模量 E_c (GPa)0.000e+0E_c (Pa) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 22 | `materials/tensile-force-area` | 0.0拉力 F (N)0.00F (kN)0.0000应力复算 (Pa)0.000应力 (MPa) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 23 | `materials/volumetric-strain` | 0.00000体积应变 ε_v0.0000体积变化率 (%)0.000000平均正应变 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 24 | `mechanical/gear-ratio` | 齿数须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 25 | `mechanical/lever-advantage` | 臂长须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 26 | `mechanical/torque-power` | 转速须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 27 | `process/tolerance-rss` | 0.000总公差 (RSS)0.000线性叠加总公差0.00RSS 占线性叠加比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 28 | `process/tolerance-worst-case` | 0.000总公差 (最差)0.000统计公差 (RSS)0.000平均单项公差 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 29 | `robotics/belt-linear-speed` | 0.0000带速 v (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 30 | `robotics/cable-tension-pulley` | 0.00绳张力 T (N)0.000机械效益 F/T0.00三绳组单绳张力 (N) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 31 | `robotics/centripetal-speed-limit` | 0.000最大速度 v_max (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 32 | `robotics/dc-motor-back-emf` | 0.00反电动势 E (V)0.0转速 (r/min) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 33 | `robotics/forward-kinematics-2r` | 0.0000末端 x (m)0.0000末端 y (m) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 34 | `robotics/gear-ratio-torque` | 0.00输出扭矩 τ_out (N·m) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 35 | `robotics/lead-screw-speed` | 0.00000线速度 v (m/s)0.00v (mm/s) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 36 | `robotics/lifting-torque` | 0.000关节转矩 τ (N·m) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 37 | `robotics/linear-accel-force` | 0.00驱动力 F (N)0.000驱动力 (kgf)0.0000驱动力 (kN) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 38 | `robotics/motor-power` | 0.00机械功率 P (W)0.0转速 (r/min)0.0000机械功率 (hp) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 39 | `robotics/motor-torque-current` | 0.0000转矩 τ (N·m)0.0τ (mN·m) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 40 | `robotics/rotational-inertia-torque` | 0.00所需扭矩 τ (N·m)0.00角加速度 (°/s²)0.0000所需扭矩 (kgf·m) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 41 | `securities/enterprise-value` | 0.00企业价值 EV (万元)0.00净市值（市值 − 现金）0.0000债务/市值 比 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 42 | `securities/market-cap` | 0.00总市值 (亿元)0总市值 (元)0总市值 (万元)0.0000股数 (亿股)0.000000总市值 (万亿元) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 43 | `securities/market-risk-premium` | 0.00市场风险溢价 (%)0.00市场收益率 (%)0.00无风险利率 (%)0.00溢价与无风险利率之比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 44 | `securities/option-breakeven-put` | 0.00盈亏平衡价 BE (元)0.0000执行价与盈亏平衡价之比0.000权利金占执行价 (%)0.00执行价与权利金之和 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 45 | `signal/carrier-freq` | 0.000载波频率 f_c (kHz)0.000带宽 B (kHz)0.0000上边频与载波比0.000几何中心频率 (kHz) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 46 | `signal/pll-lock-range` | 0锁定范围 Δf (Hz)0.000Δf (MHz)0.0000e+0锁定范围 (rad/s)0半锁定范围 (Hz) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 47 | `tax/ad-valorem-duty` | 0.00从价税 T (元)0.00完税价格合计 (元)0.00从价税率 (%)0.00货值与税额之差 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 48 | `tax/break-even-taxable` | 0.00所需应税所得0.00应纳税额 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 49 | `tax/capital-gains-tax` | 0.00资本利得0.00资本利得税0.00税后到手 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 50 | `tax/customs-duty` | 0.00进口关税0.00含税成本0.00关税税率 (%)0.000税额占含税成本比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 51 | `tax/excise-tax` | 0.00消费税 T (元)0.000计税金额 (元)0.000综合税率 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 52 | `tax/foreign-tax-credit` | 0.00可抵扣额 (元)0.00抵免限额 (元)0.00境外已纳税额 (元)0.00超出限额部分 (元) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 53 | `tax/gift-tax` | 0.00赠与税 T (元)0.00应税金额 (元)0.000有效税率 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 54 | `tax/interest-income-tax` | 0.00利息所得税0.00税后利息0.00利息税率 (%)0.0000利息/税额 倍数 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 55 | `tax/payroll-tax` | 0.00工薪税 T (元)0.0000合计税率0.00税后实得 (元) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 56 | `tax/property-tax` | 0.00年房产税额0.00月均房产税 (元)0.000000税率小数形式0.00五年累计税额 (元)0.000000房产原值 (百万元) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 57 | `tax/sales-tax-addon` | 0.00消费税额0.00含税价0.00税率 (%)0.000税额占含税价比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 58 | `tax/social-security-tax` | 0.00社保费 T (元)0.00用工总成本 (元)0.00社保费率 (%)0.00基数与社保费之差 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 59 | `tax/specific-duty` | 0.00从量税 T (元)0.000000税额 (万元)0.00月均税额 (元)0.00年化税额 (元)0.000000单位税额与数量之比 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 60 | `tax/tax-on-discount` | 0.00折后价0.00税额0.00优惠金额0.00含税总价 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 61 | `tax/vat-from-exclusive` | 0.00增值税额0.00含税金额0.00税率 (%)0.000税额占不含税价比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 62 | `tax/withholding-tax` | 0.00预提税额0.00实际支付净额0.00预提税率 (%)0.0000支付额/税额 倍数 ⏐ 📋 复制结果⬇️ 导出 TXT |

## 使用约束

- **不得按 M3 全量加守卫**：611 页里大量是生成器/演示页（默认值即有效输入，空态本就可运行）。
- **修前必须全量探针复测**：M1 中仅 62 页有 live 证据，其余 170 页需实测后才可判定“真缺陷 / 合法 0”。
- 合法 0 的典型：`debt=0`、`r=0`、`t=0`、`paid=0`、`paid=1`；守卫只判“是否填写（空串 / parseFloat=NaN）”，不判“是否非 0”。
