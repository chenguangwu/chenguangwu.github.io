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

