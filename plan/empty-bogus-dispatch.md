# empty_bogus 未领取 230 页分派清单

- 生成时间：2026-11-05
- 数据源：`plan/interaction-invalid-top100.json` 的 `recheck.emptyBogus.pendingDispatch`（230 页）+ 隔离复扫记录 `/tmp/probe/out/interaction-invalid.jsonl`（每页空态实际渲染文本）
- 口径：清空全部输入后点主按钮；结果区输出 0/NaN/伪结论即命中。**修复要求：空输入不得给出合格/优秀/推荐类结论，应提示「请填写…」或清空结果区。**
- 分派粒度：按 `tools/<行业>/` 整组派工；每组页数见下表。`【Top50仍存在】` 为 Top 50 定向复扫仍命中的页；`【已领取未修好】` 的 10 页不在本 230 清单内，单列于文末。

## 分组总览

| 目录 | 页数 | 其中 Top50 仍存在 |
|---|---|---|
| `tools/aerospace/` | 5 | 5 |
| `tools/astronomy/` | 2 | 2 |
| `tools/baking/` | 1 | 1 |
| `tools/banking/` | 5 | 5 |
| `tools/chemistry/` | 4 | 3 |
| `tools/chinese-cook/` | 1 | 0 |
| `tools/dynamics/` | 12 | 0 |
| `tools/eco/` | 18 | 0 |
| `tools/economics/` | 7 | 0 |
| `tools/electromagnetism/` | 4 | 0 |
| `tools/encode/` | 3 | 0 |
| `tools/energy/` | 3 | 0 |
| `tools/ent/` | 1 | 0 |
| `tools/film/` | 1 | 0 |
| `tools/fire/` | 1 | 0 |
| `tools/fishery/` | 1 | 0 |
| `tools/fluid/` | 3 | 0 |
| `tools/food-processing/` | 2 | 0 |
| `tools/food/` | 1 | 0 |
| `tools/general/` | 1 | 0 |
| `tools/geometry/` | 11 | 0 |
| `tools/healthcare/` | 5 | 0 |
| `tools/hematology/` | 1 | 0 |
| `tools/home/` | 2 | 0 |
| `tools/insurance/` | 4 | 0 |
| `tools/investment/` | 5 | 0 |
| `tools/kinematics/` | 8 | 0 |
| `tools/language/` | 2 | 0 |
| `tools/life/` | 1 | 0 |
| `tools/livestock/` | 1 | 0 |
| `tools/logistics/` | 2 | 0 |
| `tools/materials/` | 4 | 0 |
| `tools/mechanical/` | 3 | 0 |
| `tools/metalwork/` | 1 | 0 |
| `tools/meteorology/` | 4 | 0 |
| `tools/metrology/` | 6 | 0 |
| `tools/nuclear/` | 8 | 0 |
| `tools/nutrition/` | 2 | 0 |
| `tools/obstetrics/` | 1 | 0 |
| `tools/optical/` | 1 | 0 |
| `tools/pr/` | 1 | 1 |
| `tools/process/` | 2 | 0 |
| `tools/property/` | 2 | 0 |
| `tools/pulmonology/` | 1 | 0 |
| `tools/quantum/` | 2 | 0 |
| `tools/realestate/` | 2 | 0 |
| `tools/reproductive-medicine/` | 1 | 0 |
| `tools/restaurant/` | 1 | 0 |
| `tools/robotics/` | 11 | 0 |
| `tools/science/` | 4 | 0 |
| `tools/securities/` | 5 | 0 |
| `tools/service/` | 1 | 0 |
| `tools/shipping/` | 1 | 0 |
| `tools/signal/` | 3 | 0 |
| `tools/sports/` | 2 | 0 |
| `tools/startup/` | 1 | 0 |
| `tools/statistics/` | 5 | 0 |
| `tools/surveying/` | 13 | 0 |
| `tools/tax/` | 16 | 0 |
| `tools/text/` | 1 | 0 |
| `tools/thermodynamics/` | 5 | 0 |
| `tools/usedcar/` | 1 | 0 |
| `tools/wedding/` | 1 | 0 |
| **合计** | **230** | **17** |

> 根因三型计数：全 0 数值 **209** 页 / 0 值伪结论 **19** 页 / NaN 泄漏 **2** 页。

## `tools/aerospace/`（5 页）

- `tools/aerospace/descent-rate.html` 【Top50仍存在】 — 空态：`0.0下降率 (m/min)0.00下降率 (m/s)0.00水平速度 (m/s)0.000下降梯度 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/aerospace/drag-force.html` 【Top50仍存在】 — 空态：`0.00阻力 D (N)0.0动压 q = ½ρv² (Pa)0.00阻力 (kgf)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/aerospace/lift-equation.html` 【Top50仍存在】 — 空态：`0.00升力 L (N)0.0动压 q = ½ρv² (Pa)0.00升力 (kgf)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/aerospace/lift-force.html` 【Top50仍存在】 — 空态：`0.00升力 L (kN)0.0升力 (kgf)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/aerospace/thrust-required.html` 【Top50仍存在】 — 空态：`0.000所需推力 (kN)0.0动压 q = ½ρv² (Pa)0.00等效推力 (kgf)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/astronomy/`（2 页）

- `tools/astronomy/kepler-equation.html` 【Top50仍存在】 — 空态：`0.000偏近点角 E (°)0.00000E (rad)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/astronomy/light-travel-time.html` 【Top50仍存在】 — 空态：`0.000传播时间 t (min)0.0t (s)0.0000距离 (天文单位 AU)0.0000传播时间 (h)0.000e+0距离 (光年)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/baking/`（1 页）

- `tools/baking/recipe-scaler.html` 【Top50仍存在】 — 空态：`缩放后配方（×0）`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/banking/`（5 页）

- `tools/banking/amortization-first-interest.html` 【Top50仍存在】 — 空态：`0.00首月利息 I₁0.00首月还本金0.000年利率 (%)0.0000首月利息占本金比 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/banking/continuous-compounding.html` 【Top50仍存在】 — 空态：`0.00连续复利终值 A0.00利息总额0.0000年实际收益率 (%)0.0000较年复利增益 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/banking/effective-annual-rate.html` 【Top50仍存在】 — 空态：`0.000有效年利率 EAR (%)0.00000EAR (小数)0.0000EAR 高于名义利率 (百分点)0.0000与连续复利之差 (百分点)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/banking/net-worth.html` 【Top50仍存在】 — 空态：`0净资产 NW (元)0.00负债率 (%)0.000资产覆盖倍数0.00净资产占资产 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/banking/tax-equivalent-yield.html` 【Top50仍存在】 — 空态：`0.000税后等效收益率 TEY (%)0.000应税需高出的百分点0.0边际税率 (%)0.0000免税溢价系数减一`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/chemistry/`（4 页）

- `tools/chemistry/gibbs-free-energy.html` 【Top50仍存在】 — 空态：`0.000ΔG (kJ/mol)平衡反应方向`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/chemistry/kp-kc.html` 【Top50仍存在】 — 空态：`0.000e+0压力平衡常数 Kp0.0RT (L·atm/(mol·K))`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/chemistry/mole-fraction.html` 【Top50仍存在】 — 空态：`0.0000总物质的量 (mol)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/chemistry/partial-pressure.html` — 空态：`0.00分压 Pᵢ (kPa)0.00其余组分分压 (kPa)0.000摩尔分数 (%)0.000其余组分占比 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/chinese-cook/`（1 页）

- `tools/chinese-cook/estimate-16.html` — 空态：`0% of 0 = 0.00`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/dynamics/`（12 页）

- `tools/dynamics/angular-momentum.html` — 空态：`0.000角动量 L (kg·m²/s)0.000两倍角动量0.0000由 L 反推角速度0.000转动动能 (J)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/impulse.html` — 空态：`0.00冲量 J (N·s)0.0冲量 (N·ms 牛毫秒)0.0000冲量 (kgf·s 千克力秒)0.0000力与作用时间之比 (N/s)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/inclined-plane-accel.html` — 空态：`0.000加速度 a (m/s²)静止/需外力状态`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/kinetic-friction.html` — 空态：`0.00动摩擦力 F_k (N)0.0000正压力与摩擦系数之比0.0000摩擦力 (kgf 千克力)0.0000摩擦系数平方`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/momentum.html` — 空态：`0.0动量 p (kg·m/s)0.0动能 Ek (J)0.0动量乘速度 (kg·m²/s²)0.0000质量与速度之比 (kg·s/m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/power-force.html` — 空态：`0.0功率 P (W)0.00P (kW)0.000功率 (公制马力 PS)0.000功率 (英制马力 hp)0.000每小时做功 (kJ/h)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/power-rotational.html` — 空态：`0.00旋转功率 P (W)0.0000旋转功率 (hp)0.0000旋转功率 (kW)0.0000旋转功率 (PS)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/rotational-kinetic-energy.html` — 空态：`0.000转动动能 E (J)0.000两倍转动动能（I 乘 ω²）0.0000角动量 L0.0000转速 (转/秒)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/spring-potential.html` — 空态：`0.000弹性势能 U (J)0.000对应弹力 F (N)0.0000劲度与位移平方之积 (J)0.0000弹性势能 (mJ 毫焦)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/torque-force.html` — 空态：`0.00力矩 τ (N·m)0.0000有效力臂 (m)0.000径向分量 (N)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/weight-force.html` — 空态：`0.00重力 W (N)0.00W (kgf)0.00月球表面重力 (N)0.00火星表面重力 (N)0.000重力 W (kgf 标准重力)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/dynamics/work-energy-theorem.html` — 空态：`0.00合外力功 W (J)0.00末动能 (J)0.00初动能 (J)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/eco/`（18 页）

- `tools/eco/battery-storage.html` — 空态：`可用电量：0.00 kWh总能量：0.00 kWh`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/convert-air-aqi.html` — 空态：`0等级 优 ｜ 输入浓度 0 µg/m³ ｜ 建议 可正常户外活动`；根因：空值经 `+input.value || 0` 变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/eco/eco-10.html` — 空态：`年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效植树：0 棵`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/eco-11.html` — 空态：`单次额外燃油：0.00 L年额外燃油：0.00 L年额外碳排：0.00 吨`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/eco-16.html` — 空态：`年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效减少汽车：0 辆`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/eco-4.html` — 空态：`日产生量：0.00 吨/天年产生量：0.00 吨/年累计吨天数：0 kg·天`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/eco-7.html` — 空态：`总标准煤：0.00 kgce总 kWh：0.00 kWh总 MJ：0.00 MJ`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/eco-8.html` — 空态：`总株数：0 株年碳汇量：0.00 吨/年累计碳汇：0.00 吨`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/eco.html` — 空态：`电力碳排：0.00 kg燃煤碳排：0.00 kg天然气碳排：0.00 kg汽油碳排：0.00 kg总碳排：0.00 kg`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/ecological-footprint.html` — 空态：`生态足迹：0.000 gha`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/electricity-carbon.html` — 空态：`CO₂ 排放：0.00 kg等效树木吸收天数：0.0 天`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/env-impact-score.html` — 空态：`综合评分：0.0 分最高项：0 分`；根因：空值经 `+input.value || 0` 变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/eco/landfill-methane.html` — 空态：`CH₄ 产量：0.0 kg/年CO₂ 当量：0.0 kgCO₂e`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/rainwater-harvest.html` — 空态：`收集量：0 L折合吨：0.00 吨`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/solar-output.html` — 空态：`发电量：0.0 kWh等效减排：0.00 kgCO₂`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/water-footprint.html` — 空态：`总耗水：0 L折合 m³：0.00 m³`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/water-saving.html` — 空态：`节约水量：0.0 L折合吨：0.00 吨`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/eco/wind-power.html` — 空态：`功率：0.00 kW`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/economics/`（7 页）

- `tools/economics/balance-of-trade.html` — 空态：`0贸易差额 BoT0.00差额占出口比 (%)0.000出口进口比0进出口总额`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/economics/compound-amount.html` — 空态：`0.00复利终值 F0.00利息总额`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/economics/fv-annuity.html` — 空态：`0.00年金终值 FV0.00利息总额`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/economics/labor-force.html` — 空态：`0劳动力 LF0.00失业率 (%)0.00就业率 (%)0.0000就业与失业人数比`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/economics/okuns-law.html` — 空态：`0.00失业率变化 Δu (百分点)0.00增长缺口0.00失业率变化幅值 (百分点)0.000相对增长缺口 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/economics/pv-annuity.html` — 空态：`0.00年金现值 PV0.00贴现总额`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/economics/real-gdp.html` — 空态：`0.00实际 GDP0.00价格扭曲部分0.00实际占名义比重 (%)0.00价格扭曲占比 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/electromagnetism/`（4 页）

- `tools/electromagnetism/coil-torque.html` — 空态：`0.0000磁力矩 τ (N·m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/electromagnetism/energy-capacitor.html` — 空态：`0.000储能 E (µJ)0.000e+0储能 E (J)0.000电荷量 (mC)0.0000e+0电荷量 Q = CV (C)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/electromagnetism/magnetic-flux.html` — 空态：`0.000e+0磁通 Φ (Wb)0.00Φ (µWb)0.0000磁通 (mWb)0.0000磁感应强度复算 (T)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/electromagnetism/solenoid-field.html` — 空态：`0.000e+0磁感应强度 B (T)0.000B (mT)0.0000e+0单位电流磁场 (T/A)0.000磁感应强度 B (Gauss)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/encode/`（3 页）

- `tools/encode/encode-2.html` — 空态：`估算差异比特数：0 位采样差异：0 位汉明距离：0 位`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/encode/shannon-entropy.html` — 空态：`信息熵 H：0.0000 bit/符号`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/encode/url-encoded-length.html` — 空态：`编码后长度：0 字符膨胀率：0.0 %`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/energy/`（3 页）

- `tools/energy/carbon-footprint.html` — 空态：`年度总排放`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/energy/energy-calculator.html` — 空态：`0.0月用电碳排放 kg`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/energy/power-consumption.html` — 空态：`总耗电`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/ent/`（1 页）

- `tools/ent/caloric-test.html` — 空态：`0%单侧减弱 UW0%方向优势 DP0.0右耳总和(°/s)0.0左耳总和(°/s)`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/film/`（1 页）

- `tools/film/convert-time-1.html` — 空态：`帧率需>0`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/fire/`（1 页）

- `tools/fire/calc-water-pressure-hydrant.html` — 空态：`满足压力校核0.000 MPa所需入口压力0.000 MPa可用入口压力+0.000 MPa安全余量高程折算 0.000 MPa = 栓口 0.000 MPa + 管损 0.000 MPa。`；根因：空值经 `|| 0` 兜底变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。

## `tools/fishery/`（1 页）

- `tools/fishery/calc-39.html` — 空态：`0% of 0 = 0.00`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/fluid/`（3 页）

- `tools/fluid/bernoulli-pressure.html` — 空态：`0.0压力 P₂ (Pa)0.00压差 (kPa)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/fluid/buoyancy-force.html` — 空态：`0.00浮力 F_b (N)0.0000排开液体质量 (kg)0.00排开液体质量 (g)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/fluid/stagnation-pressure.html` — 空态：`0.0驻点压力 p₀ (Pa)0.0动压 q (Pa)0.0000驻点压比 p0/p`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/food-processing/`（2 页）

- `tools/food-processing/material-balance.html` — 空态：`0.00总投入0.00总产出0.00损耗0.0%得率`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/food-processing/recipe-cost-calculator.html` — 空态：`¥0.00总成本0g配方总用量0g实际耗用-每kg成本`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/food/`（1 页）

- `tools/food/calc-concentration.html` — 空态：`0% of 0 = 0.00`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/general/`（1 页）

- `tools/general/wurenjixuantingwuchajisuan.html` — 空态：`0.00水平误差 (m)0.00垂直误差 (m)0.00三维综合误差 (m)0.00开环飘移量 (m)高精度悬停悬停精度评定`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/geometry/`（11 页）

- `tools/geometry/arc-length.html` — 空态：`0.0000弧长 L (m)0.0000圆心角 (rad)0.000占整圆比例 (%)0.0000对应扇形面积 (m²)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/chord-length.html` — 空态：`0.0000弦长 c (m)0.0000半弦长 (m)0.0000对应弧长 (m)0.0000矢高 (m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/circle-area.html` — 空态：`0.0000圆面积 A (m²)0.0000圆周长 (m)0.0000球体积 (m³)0.0000直径 (m)0.0000半圆面积 (m²)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/circle-circumference.html` — 空态：`0.0000圆周长 C (m)0.0000直径 (m)0.0000圆面积 (m²)0.0000球体积 (m³)0.0000内接正方形面积 (m²)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/distance-3d.html` — 空态：`0.000三维距离 d`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/ellipse-area.html` — 空态：`0.000椭圆面积 A (m²)0.000000长短半轴之比0.000椭圆周长近似 (m)0.000等面积圆面积 π√(ab)（半径=√(ab)）`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/midpoint-2d.html` — 空态：`0.000中点 x_M0.000中点 y_M`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/sector-area.html` — 空态：`0.0000扇形面积 A (m²)0.000占整圆比例 (%)0.0000弧长 L = r·θ (m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/sphere-volume.html` — 空态：`0.000球体体积 V (m³)0.000球表面积 (m²)0.000大圆周长 (m)0.000球体积 (L 升)0.000球体积 (cm³)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/torus-volume.html` — 空态：`0.000环体体积 V (m³)0.000环体表面积 (m²)0.000中心圆周长 (m)0.0000体积与环半径之比`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/geometry/triangle-heron.html` — 空态：`这三条边不能构成三角形：需满足任意两边之和大于第三边（当前 0、0、0）。`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。

## `tools/healthcare/`（5 页）

- `tools/healthcare/apgar.html` — 空态：`Apgar 总分：0 分临床意义：重度窒息`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/healthcare/chads-vasc.html` — 空态：`评分：0 分风险分层：低危`；根因：空值经 `+input.value || 0` 变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/healthcare/healthcare-5.html` — 空态：`维持需求：0.0 g目标需求：0.0 g每餐建议：0.0 g`；根因：空值经 `+input.value || 0` 变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/healthcare/morse.html` — 空态：`总分：0 分风险等级：低风险`；根因：空值经 `+input.value || 0` 变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/healthcare/wells.html` — 空态：`评分：0 分临床概率：低度`；根因：空值经 `+input.value || 0` 变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。

## `tools/hematology/`（1 页）

- `tools/hematology/detector-5.html` — 空态：`0.0%PNH总克隆（粒细胞）未检测到 PNH 克隆诊断评估无显著溶血风险溶血风险0 U/LLDH 水平`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/home/`（2 页）

- `tools/home/lighting-calculator.html` — 空态：`0 所需总光通量 (lm)`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/home/room-calculator.html` — 空态：`0.00 面积 (m²)`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/insurance/`（4 页）

- `tools/insurance/complete-life-expectancy.html` — 空态：`0.000完全期望寿命 e_x0生命表项数 N0.0000平均预期余命`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/insurance/ibnr-estimate.html` — 空态：`0.00IBNR 准备金 (元)0.00已付赔款比例 (%)0.00已付赔款 (元)0.00最终赔款 (元)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/insurance/ibnr-reserve.html` — 空态：`0.00IBNR 准备金 (元)0.00最终赔款估计 (元)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/insurance/life-cover-need.html` — 空态：`0.00建议保额 (元)0.00收入替代部分 (元)0.00保额下限 (元)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。

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

## `tools/surveying/`（13 页）

- `tools/surveying/area-coordinates.html` — 空态：`0.00面积 (m²)0.0000面积 (亩)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/bearing-to-offset.html` — 空态：`0.000北向增量 ΔN (米)0.000东向增量 ΔE (米)0.000反算方位角 (度)0.000增量平方和`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/chord-length-curve.html` — 空态：`0.000弦长 C (米)0.000曲线长 L (米)0.000外距 E (米)0.0000圆心角 (°)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/circular-curve.html` — 空态：`0.000切线长 T (m)0.000曲线长 L (m)0.000外距 E (m)0.000中点弦距 M (m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/coordinate-distance-2d.html` — 空态：`0.000水平距离 D (米)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/coordinate-distance-3d.html` — 空态：`0.000空间距离 (m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/coordinate-rotation.html` — 空态：`0.000旋转后 X (m)0.000旋转后 Y (m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/elevation-diff.html` — 空态：`0.000总高差 (m)0.0000平均站差 (m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/horizontal-distance.html` — 空态：`0.000水平距离 (m)0.000高差 (m)0.000坡度 (%)0.000斜距与水平距离差 (m)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/middle-ordinate-curve.html` — 空态：`0.000中点垂距 M (米)0.000曲线长 L (米)0.000外距 E (米)0.0000圆心角 (°)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/prismoidal-volume.html` — 空态：`0.00棱台体积 V (米³)0.00平均断面法体积（对比）(米³)0.000中断面与端面均值之差 (米²)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/reduced-level-bsfs.html` — 空态：`0.000待定点高程 RL (米)0.000视线高 HI (米)0.000高差 = BS-FS (米)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/surveying/tangent-length-curve.html` — 空态：`0.000切线长 T (米)0.000曲线长 L (米)0.000外距 E (米)0.0000圆心角 (°)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/tax/`（16 页）

- `tools/tax/ad-valorem-duty.html` — 空态：`0.00从价税 T (元)0.00完税价格合计 (元)0.00从价税率 (%)0.00货值与税额之差`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/break-even-taxable.html` — 空态：`0.00所需应税所得0.00应纳税额`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/capital-gains-tax.html` — 空态：`0.00资本利得0.00资本利得税0.00税后到手`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/customs-duty.html` — 空态：`0.00进口关税0.00含税成本0.00关税税率 (%)0.000税额占含税成本比 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/excise-tax.html` — 空态：`0.00消费税 T (元)0.000计税金额 (元)0.000综合税率 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/foreign-tax-credit.html` — 空态：`0.00可抵扣额 (元)0.00抵免限额 (元)0.00境外已纳税额 (元)0.00超出限额部分 (元)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/gift-tax.html` — 空态：`0.00赠与税 T (元)0.00应税金额 (元)0.000有效税率 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/interest-income-tax.html` — 空态：`0.00利息所得税0.00税后利息0.00利息税率 (%)0.0000利息/税额 倍数`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/payroll-tax.html` — 空态：`0.00工薪税 T (元)0.0000合计税率0.00税后实得 (元)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/property-tax.html` — 空态：`0.00年房产税额0.00月均房产税 (元)0.000000税率小数形式0.00五年累计税额 (元)0.000000房产原值 (百万元)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/sales-tax-addon.html` — 空态：`0.00消费税额0.00含税价0.00税率 (%)0.000税额占含税价比 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/social-security-tax.html` — 空态：`0.00社保费 T (元)0.00用工总成本 (元)0.00社保费率 (%)0.00基数与社保费之差`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/specific-duty.html` — 空态：`0.00从量税 T (元)0.000000税额 (万元)0.00月均税额 (元)0.00年化税额 (元)0.000000单位税额与数量之比`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/tax-on-discount.html` — 空态：`0.00折后价0.00税额0.00优惠金额0.00含税总价`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/vat-from-exclusive.html` — 空态：`0.00增值税额0.00含税金额0.00税率 (%)0.000税额占不含税价比 (%)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/tax/withholding-tax.html` — 空态：`0.00预提税额0.00实际支付净额0.00预提税率 (%)0.0000支付额/税额 倍数`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/text/`（1 页）

- `tools/text/stats-1.html` — 空态：`总字符数（含空白）：0总字符数（不含空白）：0中文字符数：0英文单词数：0数字组数：0行数：0非空行数：0`；根因：空值未拦截，按 0 参与计算，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/thermodynamics/`（5 页）

- `tools/thermodynamics/entropy-generation.html` — 空态：`0.000熵产 S_gen (J/K)满足第二定律 (S_gen≥0)判定0.000系统熵变 ΔS_sys (J/K)0.000环境熵变 ΔS_surr (J/K)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，0 值落入最低风险/最优档，仍输出「优秀/低危/满足」类结论。
- `tools/thermodynamics/latent-heat.html` — 空态：`0相变热量 Q (J)0.000热量 (MJ)0比潜热复算 (J/kg)0.0热量 (kJ)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/thermodynamics/linear-expansion.html` — 空态：`0.0000伸长量 ΔL (mm)0.000末长 (mm)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/thermodynamics/polytropic-work.html` — 空态：`0.00过程功 W (kJ)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。
- `tools/thermodynamics/specific-heat-q.html` — 空态：`0.0热量 Q (J)0.000热量 (kJ)`；根因：空值经页面 `num()`（`parseFloat` 后 `isNaN → 0`）变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/usedcar/`（1 页）

- `tools/usedcar/car-purchase-cost.html` — 空态：`购置税：0.00 元保险费：0.00 元上牌费：0.00 元落地总价：0.00 元`；根因：空值经 `|| 0` 兜底变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## `tools/wedding/`（1 页）

- `tools/wedding/wedding-budget-planner.html` — 空态：`¥0总预算¥0已分配¥0剩余`；根因：空值经 `+input.value || 0` 变成 0，结果区照常渲染全 0 数值，无「请填写」提示。

## 附：已领取未修好（10 页，不在 230 待分派清单）

| 页面 | 复扫空态文案 | 状态 |
|---|---|---|
| `tools/agriculture/agri-calculator.html` | `氮 (N)0.00kg磷 (P₂O₅)0.00kg钾 (K₂O)0.00kg配方比例：0-0-0施肥面积：0 亩每亩用量：0 kg/亩肥料总量：0.0 kg` | 待修 |
| `tools/astronomy/hubble-redshift-distance.html` | `0.00距离 d (Mpc)0.00d (百万光年)0.00退行速度 v = cz (km/s)0.0000d (十亿光年)` | **本批已修**：空输入改为「请输入有效红移 z（≥ 0）后再计算。」 |
| `tools/design/px-to-rem.html` | `转换结果` | 待修（空态无提示） |
| `tools/encode/base32.html` | `编码长度：0 字符无填充长度：0 字符` | 待修 |
| `tools/fishery/salinity-calculator.html` | `⚠️ 四项均需填写有效数值：现有水量须 >0，三个盐度须 ≥0。…` | **扫描误判**：已是提示语，文案含 `>0 / ≥0` 的数字被空态规则误命中，无需修 |
| `tools/hr/overtime-pay-calc.html` | `工作日加班费：0.00 元休息日加班费：0.00 元法定节假日加班费：0.00 元总加班费：0.00 元` | 待修 |
| `tools/mining/convert-grade-ore.html` | `品位需填写 ≥0 的数值（g/t）；矿石量需填写 ≥0 的数值（t）；金属价格需填写 ≥0 的数值（元/g）` | **扫描误判**：已是提示语，数字 `≥0` 被误命中，无需修 |
| `tools/museum/audio-guide-timer.html` | `0秒讲解总时长` | 待修 |
| `tools/robotics/forward-kinematics-2r.html` | `0.0000末端 x (m)0.0000末端 y (m)` | 待修 |
| `tools/surveying/bearing-from-coordinates.html` | `0.00方位角 α (°)0.000两点距离 (同坐标单位)第一象限坐标增量象限` | 待修 |

> 结论：10 页中 **2 页为扫描器数字误判**（提示语含 `>0 / ≥0`）、**1 页本批已修**，实际待修 **7 页**。

## 附：Top 50 形态变化（2 页）

- `tools/it/matrix-multiplier.html`：`empty_bogus` 已消失，`click_error`（`Cannot read properties of null (reading 'value')`）**为扫描时差**——复扫跑在 `4d120b9e9a`（01:55）修复提交之前的版本；当前版本已含「行列数须为 1–6 整数」「缺单元格先构建」校验，真机复验空态输出「请输入矩阵 A 与 B 的行列数」且无异常，**无需再改**。
- `tools/astronomy/hubble-redshift-distance.html`：`interact_error` 消失，`empty_bogus` 仍在（空态继续输出 0）→ **本批已修**，真机空态输出「请输入有效红移 z（≥ 0）后再计算。」。
