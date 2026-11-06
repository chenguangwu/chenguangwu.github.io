## `tools/investment/`（5 页）

- `tools/investment/bond-price.html` — 空态：`0.00债券价格 P折价状态`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/investment/discounted-payback.html` — 空态：`0.00 年折现回收期`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/investment/npv-calc.html` — 空态：`0.00净现值 NPV`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/investment/payback-period.html` — 空态：`0.00 年静态回收期`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/investment/yield-spread.html` — 空态：`0利差 Spread (bps)0.0000利差 (%)0.000基准收益率 (%)0.000对比收益率 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/kinematics/`（8 页）

- `tools/kinematics/angular-displacement.html` — 空态：`0.000角位移 θ (rad)0.000末角速度 (rad/s)0.000平均角速度 (rad/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/kinematics/angular-final-velocity.html` — 空态：`0.000末角速度 ω (rad/s)0.000角位移 (rad)0.000平均角速度 (rad/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/kinematics/final-velocity-accel.html` — 空态：`0.000末速度 v (m/s)0.000v (km/h)0.000位移 s (m)0.000速度增量 (m/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/kinematics/projectile-velocity-components.html` — 空态：`0.000水平分量 vₓ (m/s)0.000竖直分量 vᵧ (m/s)0.00合矢量方向 (°)0.0000水平/竖直分量比 vx/vy`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/kinematics/relativistic-velocity-add.html` — 空态：`0.000000合成速度 u (c)0.000e+0u (m/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/kinematics/rpm-to-radps.html` — 空态：`0.000角速度 ω (rad/s)0.0000转速 (转/秒)0.000角速度 (rad/min)0.0000频率 f (Hz)0.0000角速度平方 (rad²/s²)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/kinematics/tangential-velocity.html` — 空态：`0.000切向速度 v (m/s)0.000切向速度 (km/h)0.0000转速 (转/秒)0.0000角速度复核 (rad/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/kinematics/velocity-squared.html` — 空态：`0.000末速度 v (m/s)0.000速度平方增量 v²−v₀²0.000速度增量 Δv (m/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/language/`（2 页）

- `tools/language/language-toolkit.html` — 空态：`0总字符数 0汉字数 0英文字母 0数字数 0标点符号 0空格数 0英文单词数 0句子数`；根因：空值未拦截，按 0 参与计算，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/language/stats-2.html` — 空态：`总字符数（含空格）：0不含空格字符数：0汉字数：0英文字母数：0英文单词数：0数字字符数：0标点数：0（中文 0 / 西文 0）空白符：0行数：0`；根因：空串经 `Number('')` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/life/`（1 页）

- `tools/life/countdown.html` — 空态：`⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行 Ctrl/⌘ + Enter 快速运行`；根因：空值未拦截，按 0 参与计算，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/livestock/`（1 页）

- `tools/livestock/milk-yield-scc.html` — 空态：`0.0平均产奶量(kg)0平均SCC(万/ml)0.0最高产奶量(kg)优秀最新SCC等级`；根因：空值经 `|| 0` 兜底变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。

## `tools/logistics/`（2 页）

- `tools/logistics/express-freight-calc.html` — 空态：`计费重量：0.00 kg超首重：0.00 kg（进位计费 0 kg）预计运费：0.00 元`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/logistics/package-volume-calc.html` — 空态：`尺寸体积：0.0 cm³体积（m³）：0.0000材积重：0.00 kg`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/materials/`（4 页）

- `tools/materials/linear-thermal-expansion.html` — 空态：`0.000伸长量 ΔL (mm)0.0000热应变 (微应变)0.000000膨胀后长度 (m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/materials/rule-of-mixtures.html` — 空态：`0.00复合模量 E_c (GPa)0.000e+0E_c (Pa)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/materials/tensile-force-area.html` — 空态：`0.0拉力 F (N)0.00F (kN)0.0000应力复算 (Pa)0.000应力 (MPa)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/materials/volumetric-strain.html` — 空态：`0.00000体积应变 ε_v0.0000体积变化率 (%)0.000000平均正应变`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/mechanical/`（3 页）

- `tools/mechanical/gear-ratio.html` — 空态：`齿数须>0。`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/mechanical/lever-advantage.html` — 空态：`臂长须>0。`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/mechanical/torque-power.html` — 空态：`转速须>0。`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/metalwork/`（1 页）

- `tools/metalwork/detector-mold.html` — 空态：`测量点：各轴偏差：X轴：+0.000 mm ✓ 合格Y轴：+0.000 mm ✓ 合格Z轴：+0.000 mm ✓ 合格空间偏差：0.0000 mm公差要求：±0.000 mm综合判定：合格该测量点三…`；根因：空值未拦截，按 0 参与计算，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。

## `tools/meteorology/`（4 页）

- `tools/meteorology/beaufort-scale.html` — 空态：`0 级蒲福风级无风风力名称`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/meteorology/dafengyingxiangpinggu.html` — 空态：`阵风风力等级0级无风风力较小，无大风影响0.0平均风速 (m/s)0.0阵风风速 (m/s)0.00阵风系数 G0.0阵风差 (m/s)项目风速 (m/s)蒲福等级名称平均风0.00级无风阵风0.00…`；根因：空值未拦截，按 0 参与计算，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/meteorology/jiaotongqixianganquantishi.html` — 空态：`交通气象综合预警等级特级预警(黑)气象条件极端，立即封闭道路，禁止通行。风险项当前值等级说明能见度0 m特级预警强浓雾(特级)，能见度极低，严禁通行。路面结冰0.0°C黄色预警路面接近冰点(黄色)，注…`；根因：空值未拦截，按 0 参与计算，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/meteorology/strength-3.html` — 空态：`0%冰雹概率 PH0.0VIL 近似 (kg/m²)0.0降水强度 (mm/h)0水量通量 (m³/s)弱对流/层状云回波顶高：0.0 km（低顶(浅对流)）冰雹概率对流较弱，降水以稳定性为主。`；根因：空值未拦截，按 0 参与计算，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/metrology/`（6 页）

- `tools/metrology/bias-absolute.html` — 空态：`0.000绝对偏倚 Bias0.000相对偏倚 (%)0.00000测量与参考比0.000偏倚绝对值`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/metrology/dimensional-tolerance.html` — 空态：`0.000公差 (mm)0.000最大极限尺寸 (mm)0.000最小极限尺寸 (mm)0.000公差带中心偏差 (mm)0.000公差带中值尺寸 (mm)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/metrology/flatness-deviation.html` — 空态：`0.000平面度误差 (mm)0.0平面度误差 (μm)0.000中位高度 (mm)0.00相对平面度 (ppm)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/metrology/roundness-deviation.html` — 空态：`0.000圆度误差 (mm)0.0圆度误差 (μm)0.000平均半径 (mm)0.00相对圆度 (ppm)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/metrology/tolerance-stackup-worst.html` — 空态：`0.000总公差 (最坏) (mm)0.000平均单环 (mm)0.000统计平方根（RSS）总公差 (mm)0.000极端法与统计法之差 (mm)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/metrology/uncertainty-propagation-sum.html` — 空态：`0.0000合成标准不确定度 u_c`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/nuclear/`（8 页）

- `tools/nuclear/activity-decay.html` — 空态：`0.000活度 A (Bq)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/nuclear/activity.html` — 空态：`0.000e+0活度 A (Bq)0.000e+0A (Ci)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/nuclear/binding-energy.html` — 空态：`0.000e+0结合能 BE (J)0.000BE (MeV)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/nuclear/dose-equivalent.html` — 空态：`0.00剂量当量 H (Sv)0.00吸收剂量 (rad 拉德)0.0剂量当量 (mSv 毫希沃特)0.0剂量当量 (rem 雷姆)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/nuclear/fission-energy-yield.html` — 空态：`0.000e+0总能量 E (J)0.000E (kWh)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/nuclear/mass-defect.html` — 空态：`0.00000质量亏损 Δm (u)0.000对应能量 (MeV)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/nuclear/nuclear-radius.html` — 空态：`0.000核半径 R (fm)0.000核直径 (fm)0.000核体积近似 (fm³)0.000000核子数密度 (个/fm³)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/nuclear/q-value.html` — 空态：`0.0000Q 值 (MeV)吸能反应类型`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/nutrition/`（2 页）

- `tools/nutrition/estimate-2.html` — 空态：`0.0g 控盐优秀 钠摄入约 0 mg · 相当于食盐 0.0 g 继续保持低盐饮食，对血压和心血管有益。`；根因：空值经 `|| 0` 兜底变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/nutrition/nutrition-1.html` — 空态：`0% of 0 = 0.00`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/obstetrics/`（1 页）

- `tools/obstetrics/afi-normal.html` — 空态：`0.0羊水指数AFI(cm)羊水过少评估结果`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/optical/`（1 页）

- `tools/optical/numerical-aperture.html` — 空态：`0.000数值孔径 NA = n·sinθ0.000由 NA 反推半角 (°)0.00000NA 平方0.0000n 与 NA 之比`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/pr/`（1 页）

- `tools/pr/risk-assessment.html` 【Top50仍存在】 — 空态：`0风险总数0低风险0中风险0高/极高`；根因：空值未拦截，按 0 参与计算，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。

## `tools/process/`（2 页）

- `tools/process/tolerance-rss.html` — 空态：`0.000总公差 (RSS)0.000线性叠加总公差0.00RSS 占线性叠加比 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/process/tolerance-worst-case.html` — 空态：`0.000总公差 (最差)0.000统计公差 (RSS)0.000平均单项公差`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/property/`（2 页）

- `tools/property/elevator-energy.html` — 空态：`0.00 kWh单台日能耗`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/property/shared-area.html` — 空态：`0.00 ㎡套内总面积`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/pulmonology/`（1 页）

- `tools/pulmonology/light-criteria.html` — 空态：`0.00蛋白比值0.00LDH比值0胸水LDH(U/L)漏出液积液性质`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/quantum/`（2 页）

- `tools/quantum/bohr-orbit-radius.html` — 空态：`0.0000轨道半径 r_n (Å)0.0000r_n (nm)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/quantum/quantum-oscillator-energy.html` — 空态：`0.0000能量 E (eV)0.0000e+0角频率 omega (rad/s)0.0000零点能 (eV)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/realestate/`（2 页）

- `tools/realestate/calc-2.html` — 空态：`年租金收入：0.00 元（月租 0.00 元）毛租金回报率：0.00%净租金回报率：0.00%`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/realestate/convert-area-shared.html` — 空态：`公摊面积 = 0.00 ㎡ 建筑面积 = 0.00 ㎡ 得房率 = NaN % 参考：多层住宅得房率一般 85% 以上，高层 75% 左右，超高层 70% 左右`；根因：空值直接参与运算，结果出现 NaN/Infinity（空值经 `+input.value || 0` 变成 0）。

## `tools/reproductive-medicine/`（1 页）

- `tools/reproductive-medicine/baifenbijisuanqi.html` — 空态：`0% of 0 = 0.00`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/restaurant/`（1 页）

- `tools/restaurant/menu-pricing.html` — 空态：`成本合计：0.00 元建议售价：0.00 元建议毛利：0.00 元`；根因：空值经 `|| 0` 兜底变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。

## `tools/robotics/`（11 页）

- `tools/robotics/belt-linear-speed.html` — 空态：`0.0000带速 v (m/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/cable-tension-pulley.html` — 空态：`0.00绳张力 T (N)0.000机械效益 F/T0.00三绳组单绳张力 (N)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/centripetal-speed-limit.html` — 空态：`0.000最大速度 v_max (m/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/dc-motor-back-emf.html` — 空态：`0.00反电动势 E (V)0.0转速 (r/min)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/gear-ratio-torque.html` — 空态：`0.00输出扭矩 τ_out (N·m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/lead-screw-speed.html` — 空态：`0.00000线速度 v (m/s)0.00v (mm/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/lifting-torque.html` — 空态：`0.000关节转矩 τ (N·m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/linear-accel-force.html` — 空态：`0.00驱动力 F (N)0.000驱动力 (kgf)0.0000驱动力 (kN)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/motor-power.html` — 空态：`0.00机械功率 P (W)0.0转速 (r/min)0.0000机械功率 (hp)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/motor-torque-current.html` — 空态：`0.0000转矩 τ (N·m)0.0τ (mN·m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/robotics/rotational-inertia-torque.html` — 空态：`0.00所需扭矩 τ (N·m)0.00角加速度 (°/s²)0.0000所需扭矩 (kgf·m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/science/`（4 页）

- `tools/science/gravitational-potential.html` — 空态：`0.0 J重力势能 E_p = mgh0.0000重力势能 (MJ)0.000高度复算 (m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/science/kinetic-energy.html` — 空态：`0.0 J动能 E_k = ½mv²0.0000速度平方 v² (m²/s²)0.000000动能 (kJ)0.000质量与动能之积`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/science/mechanical-power.html` — 空态：`0 W功率 P = F·v0.000000功率 (kW)0.000000功率 (hp 英制马力)0.0000功率 (kgf·m/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/science/work-done.html` — 空态：`0.0 J功 W = F·d·cosθ0.000沿位移分力 (N)0.000垂直分力 (N)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/securities/`（5 页）

- `tools/securities/calc-1.html` — 空态：`净盈亏：+0.00 元收益率：0.00%买入总成本：0.00 元（金额 0.00 + 佣金 0.00 + 过户费 0.00）卖出净收入：0.00 元（金额 0.00 - 佣金 0.00 - 印花税 0…`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/securities/enterprise-value.html` — 空态：`0.00企业价值 EV (万元)0.00净市值（市值 − 现金）0.0000债务/市值 比`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/securities/market-cap.html` — 空态：`0.00总市值 (亿元)0总市值 (元)0总市值 (万元)0.0000股数 (亿股)0.000000总市值 (万亿元)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/securities/market-risk-premium.html` — 空态：`0.00市场风险溢价 (%)0.00市场收益率 (%)0.00无风险利率 (%)0.00溢价与无风险利率之比 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/securities/option-breakeven-put.html` — 空态：`0.00盈亏平衡价 BE (元)0.0000执行价与盈亏平衡价之比0.000权利金占执行价 (%)0.00执行价与权利金之和`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/service/`（1 页）

- `tools/service/complaint-analysis.html` — 空态：`暂无数据`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/shipping/`（1 页）

- `tools/shipping/convert-time-speed.html` — 空态：`航程 = 0.00 海里 (≈ 0.00 km)`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/signal/`（3 页）

- `tools/signal/carrier-freq.html` — 空态：`0.000载波频率 f_c (kHz)0.000带宽 B (kHz)0.0000上边频与载波比0.000几何中心频率 (kHz)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/signal/energy-discrete.html` — 空态：`0.000信号能量 E0采样点数 N0.0000平均功率 (E/N)0.0000均方根值 RMS`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/signal/pll-lock-range.html` — 空态：`0锁定范围 Δf (Hz)0.000Δf (MHz)0.0000e+0锁定范围 (rad/s)0半锁定范围 (Hz)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/sports/`（2 页）

- `tools/sports/calc-angle-slope.html` — 空态：`0% of 0 = 0.00`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/sports/convert-29.html` — 空态：`柔韧指数 = NaN 踢腿点距头顶 = 0.0 cm 测量规范：支撑腿伸直，量地面至踢腿最高点的垂直距离 双腿差异超过 10% 提示不对称，需针对性平衡训练 本指数与坐位体前屈、纵跳共同构成下肢柔韧评…`；根因：空值直接参与运算，结果出现 NaN/Infinity（空值经 `+input.value || 0` 变成 0）。

## `tools/startup/`（1 页）

- `tools/startup/calc-1.html` — 空态：`建议启动资金：0.00 元其中一次性投入 0.00 元，运营资金 0.00 元，应急储备 0.00 元月运营成本：0.00 元，按此标准资金可支撑约 0.0 个月`；根因：空值经 `|| 0` 兜底变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。

## `tools/statistics/`（5 页）

- `tools/statistics/iqr.html` — 空态：`IQR：0.0000 异常值下限：0.0000 异常值上限：0.0000 中位数：0.0000`；根因：空值经 `+input.value || 0` 变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/statistics/pooled-variance.html` — 空态：`0.000合并方差 s_p²`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/statistics/statistics-12.html` — 空态：`均值：0.0000 中位数：0.0000 极差：0.0000 总和：0.0000`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/statistics/statistics-16.html` — 空态：`斜率 a：0.0000 截距 b：0.0000 预测 y：0.0000`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/statistics/variance-list.html` — 空态：`0.0000样本方差 s²`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

