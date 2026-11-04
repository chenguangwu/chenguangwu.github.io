# 交互有效性扫描（第二轮：点了到底有没有用）

- 扫描时间：2026/11/5 01:47:07
- 覆盖工具页：**4916**
- 有输入控件的页：**4512**
- 无输入控件（纯展示/参考卡，跳过）：**404**
- 有输入但无主按钮（实时计算/表单提交，不计缺陷）：**588**
- 命中至少一类问题：**328**（复扫后重算）

> 计数口径（2026-11-05 复扫后）：空态两类按本文件「修效验证」节更新——`empty_bogus` 240（复扫仍命中）、`empty_conclusion` 7（对照法确认）；表中其余类型沿用上一轮全量扫描值。全站命中至少一类问题约 **328** 页（按复扫结果去重估算）。
>
> 口径：① 有效性＝先填值→记录快照→**改一个输入为明显不同的合法值**→再点主按钮→比较前后快照（排除「加载时已自动算过一次」的假阴性）；② 空态＝清空所有输入后点主按钮，结果区给出 NaN/Infinity/undefined/null/0/空串或结论即为缺陷；③ 死控件＝控件 id 在全部 `<script>` 中从未出现（且页面无 `querySelectorAll('input')` / `FormData` 这类泛化读取，内联 oninput 绑定的不计）。快照优先取 `#result/#output/.result*` 等结果容器，无则回退整页正文（剔除控件内的当前值）。

## 修效验证（2026-11-05 定向复扫）

> 复扫对象：`empty_bogus` 296 页 + `empty_conclusion` 56 页，共 **352** 页；全部读取**当前工作区**页面（本地 `http.server`，未 push）。
> 并发说明：共享 `scripts/out/interaction-invalid.jsonl` 被其他修复线的扫描并发覆盖（丢 291 条记录），本轮改用隔离输出复扫，不写共享中间文件。
> 探针：`empty_bogus` 走 `runtime_scan.js --interact` 空态流程；`empty_conclusion` 走对照法（空输入 / 默认值 / 边界值三组）。

### 结论三数字

| 指标 | empty_bogus | empty_conclusion | 合计 |
|---|---|---|---|
| 基线 | 296 | 56 | 352 |
| 已修（复扫不再命中） | 54 | 4 | **58** |
| 仍存在（复扫确认） | 240 | 7 | **247** |
| 待分派（仍存在且未被任何修复线领取） | 230 | 7 | **237** |
| 形态变化（原问题消失但出现新问题） | 2 | 0 | 2 |

- `empty_bogus` 的 240 页仍存在中，**10 页已被修复线改动但仍未通过**（已领取未修好），其余 **230 页未被领取** → 待分派 230。
- `empty_conclusion` 的 52 页仍被扫描器命中，但对照法只有 **7 页**「空输入结论 = 默认输入结论」；另 **25 页**空输入结论与默认不同（结论随输入变化，按对照口径不计命中），**20 页**根本不是结论（数值/推荐列表/静态参考文案，属词表误报）。

### Top 50 定向复扫

| 分档 | 页数 | 结论 |
|---|---|---|
| 已消失 | **30** | 空输入不再是 0/NaN/伪结论（多为补「请填写…」提示） |
| 仍存在 | **18** | 空输入仍直接输出 0/NaN/伪结论 |
| 形态变化 | **2** | 原问题消失但出现新问题（见下） |

**仍存在（18 页）**


- `tools/pr/risk-assessment.html`
- `tools/aerospace/descent-rate.html`
- `tools/aerospace/drag-force.html`
- `tools/aerospace/lift-equation.html`
- `tools/aerospace/lift-force.html`
- `tools/aerospace/thrust-required.html`
- `tools/agriculture/agri-calculator.html`
- `tools/astronomy/kepler-equation.html`
- `tools/astronomy/light-travel-time.html`
- `tools/baking/recipe-scaler.html`
- `tools/banking/amortization-first-interest.html`
- `tools/banking/continuous-compounding.html`
- `tools/banking/effective-annual-rate.html`
- `tools/banking/net-worth.html`
- `tools/banking/tax-equivalent-yield.html`
- `tools/chemistry/gibbs-free-energy.html`
- `tools/chemistry/kp-kc.html`
- `tools/chemistry/mole-fraction.html`

**形态变化（2 页）**

- `tools/it/matrix-multiplier.html`：`empty_bogus` 已消失（空态改为「请输入矩阵 A 与 B 的行列数」），但新增 `click_error`（点主按钮抛 `Cannot read properties of null (reading 'value')`）。
- `tools/astronomy/hubble-redshift-distance.html`：`interact_error` 已消失，`empty_bogus` 仍在（空态继续输出 0）。

### empty_conclusion 对照法分派清单（52 页，按目录）

> 「同结论」列只认**空输入结论 vs 默认输入结论**，不认整段快照：`同` = 命中；`不同` = 结论随输入变化，不计命中；`—` = 结果区没有结论（数值/推荐列表/静态参考文案）。
> 已修 4 页：`accounting/assessor-risk-11`、`hvac/supply-air`、`life/generator-price`、`safety/generator-hazard`（空态已改为「请填写…」或复扫不再命中）。

| 目录 | 页面 | 空输入结论 | 默认输入结论 | 同结论 | 归类 |
|---|---|---|---|---|---|
| `aerospace/` | `tools/aerospace/weight-balance.html` | 平衡状态：重心在安全范围内；重量状态：未超重 | 平衡状态：重心在安全范围内；重量状态：未超重 | **同** | 真命中 |
| `agriculture/` | `tools/agriculture/detector-nutrition.html` | 综合等级：不合格 | 综合等级：一级 | **不同** | 不同结论 |
| `agriculture/` | `tools/agriculture/irrigation-uniformity.html` | 均匀度评价：均匀性差 | 均匀度评价：优秀 | **不同** | 不同结论 |
| `automotive/` | `tools/automotive/voltage-1.html` | 无（负载率 0.0%，仅“安全线”静态文案） | 无 | **—** | 非结论 |
| `beauty/` | `tools/beauty/recommender-face-shape.html` | 无（推荐列表） | 无（推荐列表，条目不同） | **—** | 非结论 |
| `biz/` | `tools/biz/checker-8.html` | 质量不合格 | 质量良好 | **不同** | 不同结论 |
| `biz/` | `tools/biz/presentation-timer.html` | 进度正常 | 进度正常 | **同** | 真命中 |
| `clinical-lab/` | `tools/clinical-lab/thyroid-function-model.html` | 甲状腺功能正常 | 甲状腺功能正常 | **同** | 真命中 |
| `decor/` | `tools/decor/detector-18.html` | 综合判定：达标 / 合格 | 综合判定：不达标 | **不同** | 不同结论 |
| `eco/` | `tools/eco/aqi.html` | 健康等级：1 级 | 健康等级：2 级 | **不同** | 不同结论 |
| `eco/` | `tools/eco/noise-superposition.html` | 限值对照全 ✓（达标） | 限值对照全 ✗（超标） | **不同** | 不同结论 |
| `edu/` | `tools/edu/assessor-27.html` | 成熟度等级：1级-初始级 | 成熟度等级：3级-规范级 | **不同** | 不同结论 |
| `electronics/` | `tools/electronics/bandwidth.html` | 推荐运放：LM358 / NE5532 | 推荐运放：NE5532 / TL072 | **不同** | 不同结论 |
| `electronics/` | `tools/electronics/capacitance.html` | 推荐标准值：8 pF | 推荐标准值：27 pF | **不同** | 不同结论 |
| `encode/` | `tools/encode/encode-7.html` | 无（安全阈值 n=1） | 无（n≈2.6e19） | **—** | 非结论 |
| `endocrinology/` | `tools/endocrinology/detector-metabolism.html` | 风险评估：低风险 | 风险评估：中风险 | **不同** | 不同结论 |
| `energy/` | `tools/energy/air-purifier-area.html` | 无（0 m²） | 无（28/40/48 m²） | **—** | 非结论 |
| `energy/` | `tools/energy/water-tds-evaluator.html` | 直饮水级｜水质极优 | 自来水级｜水质良好 | **不同** | 不同结论 |
| `ent/` | `tools/ent/ahi-severity.html` | 100% 正常 | 82% 中度低氧 | **不同** | 不同结论 |
| `ent/` | `tools/ent/hearing-loss-classification.html` | 无（0 值 + 静态标尺“正常”） | 无 | **—** | 非结论 |
| `ent/` | `tools/ent/laryngeal-nerve.html` | F0 异常 / Jitter 正常 | F0 正常 / Jitter 异常 | **不同** | 不同结论 |
| `fitness/` | `tools/fitness/ratio-19.html` | 等级：优秀（100.0 分） | 等级：优秀（99.2 分） | **同** | 真命中 |
| `fitness/` | `tools/fitness/weight-capacity-training.html` | 强度区间：低强度 | 强度区间：肌肥大 | **不同** | 不同结论 |
| `gardening/` | `tools/gardening/recommender.html` | 无（推荐列表） | 无（推荐列表，条目不同） | **—** | 非结论 |
| `general/` | `tools/general/recommender-24.html` | 无（推荐列表） | 无（推荐列表，条目不同） | **—** | 非结论 |
| `healthcare/` | `tools/healthcare/checker-manager.html` | 多项判定：需整改 | 多数判定：合规 | **不同** | 不同结论 |
| `healthcare/` | `tools/healthcare/water-intake.html` | 无（推荐饮水 0 mL） | 无（2730 mL） | **—** | 非结论 |
| `hr/` | `tools/hr/assessor-training-hr.html` | 评估等级：需改进 | 评估等级：卓越 | **不同** | 不同结论 |
| `hr/` | `tools/hr/attendance-stats.html` | 出勤率评级：优秀 | 出勤率评级：良好 | **不同** | 不同结论 |
| `hydraulic/` | `tools/hydraulic/dam-stability.html` | Ks 0.975 不满足；Ko 2.813 满足 | Ks 0.975 不满足；Ko 2.813 满足 | **同** | 真命中 |
| `insurance/` | `tools/insurance/pure-premium.html` | 无（0.00 元） | 无（3,600 元） | **—** | 非结论 |
| `leather/` | `tools/leather/temp-9.html` | 热稳定性：优秀 | 热稳定性：较差 | **不同** | 不同结论 |
| `leather/` | `tools/leather/time-34.html` | 操作建议：温度偏低 | 操作建议：温度适宜 | **不同** | 不同结论 |
| `leather/` | `tools/leather/yield-rate-1.html` | 处理效果：较差 | 处理效果：良好 | **不同** | 不同结论 |
| `leather/` | `tools/leather/yield-rate.html` | 利用率：较差 | 利用率：优秀 | **不同** | 不同结论 |
| `life/` | `tools/life/recommender-8.html` | 无（推荐列表） | 无（推荐列表，条目不同） | **—** | 非结论 |
| `manufacturing/` | `tools/manufacturing/production-efficiency.html` | 无（OEE 87.5/59.5/95.0，与默认完全相同） | 无（同值） | **—** | 非结论 |
| `meteorology/` | `tools/meteorology/risk-14.html` | 综合风险：中高风险（71） | 综合风险：低风险（25） | **不同** | 不同结论 |
| `mining/` | `tools/mining/checker-training-hr.html` | 安全等级：不达标（停产整顿） | 安全等级：安全生产标准化一级 | **不同** | 不同结论 |
| `museum/` | `tools/museum/exhibit-spacing.html` | 无（559.8 / 0.0 / 48.0 cm） | 无（205.3 / 76.8 / 176.0 cm） | **—** | 非结论 |
| `nephrology/` | `tools/nephrology/vascular-calcification.html` | 无钙化｜风险低 | 重度钙化｜风险高 | **不同** | 不同结论 |
| `optical/` | `tools/optical/recommender-1.html` | 无（推荐列表，与默认完全相同） | 无（同列表） | **—** | 非结论 |
| `optical/` | `tools/optical/recommender-11.html` | 无（推荐列表，与默认完全相同） | 无（同列表） | **—** | 非结论 |
| `rental/` | `tools/rental/recommender-5.html` | 无（推荐列表） | 无（推荐列表，条目不同） | **—** | 非结论 |
| `reproductive-medicine/` | `tools/reproductive-medicine/sperm-dfi.html` | 分级：优秀（DFI 0%） | 分级：优秀（DFI 12%） | **同** | 真命中 |
| `safety/` | `tools/safety/generator-21.html` | 无（清单） | 无（清单，条目不同） | **—** | 非结论 |
| `safety/` | `tools/safety/random-13.html` | 无（知识卡片） | 无（知识卡片，条目不同） | **—** | 非结论 |
| `seismology/` | `tools/seismology/generator-drill.html` | 无（预案列表） | 无（预案列表，条目不同） | **—** | 非结论 |
| `tax/` | `tools/tax/calc-8.html` | 推荐方案：单独计税（省税 ¥0） | 推荐方案：单独计税（省税 ¥2,520） | **同** | 真命中 |
| `textile/` | `tools/textile/strength-color-diff.html` | 合格判定（阈值 0） | 不合格判定（阈值 1.5） | **不同** | 不同结论 |
| `travel/` | `tools/travel/recommender-10.html` | 无（推荐列表） | 无（推荐列表，条目不同） | **—** | 非结论 |
| `travel/` | `tools/travel/recommender-9.html` | 无（推荐列表） | 无（推荐列表，条目不同） | **—** | 非结论 |

**真命中 7 页（建议优先分派）**

| 页面 | 根因 |
|---|---|
| `tools/aerospace/weight-balance.html` | 全 0 载荷仍判「重心在安全范围内 / 未超重」；无空态拦截。 |
| `tools/biz/presentation-timer.html` | 空态点「开始演讲」仍显示「进度正常」；状态文案与输入无关（低危）。 |
| `tools/clinical-lab/thyroid-function-model.html` | 清空 TSH 后 `analyze()` 直接 return，结果区沿用上一次默认值并显示「甲状腺功能正常」。 |
| `tools/fitness/ratio-19.html` | 左右尺寸全 0 → 差异 0 → 对称分 100 → 优秀；无正数/非空校验。 |
| `tools/hydraulic/dam-stability.html` | `calc()` 在 H/B 为空时 return，结果区保留默认值的「满足/不满足」结论。 |
| `tools/reproductive-medicine/sperm-dfi.html` | DFI/HDS 空值按 0 参与分级 → 优秀。 |
| `tools/tax/calc-8.html` | 工资与年终奖全 0 仍给出「推荐方案：单独计税」。 |

> 口径冲突说明：`plan/empty-conclusion-dispatch.md` 的 34 页清单按旧口径（空输入只要给出结论就算）整理；按本轮的对照法，只有上表 7 页符合「空输入与默认输入同结论」。该文件保留作历史记录，分派以本节为准。

## 总览（按类型）

| 类型 | 页数 | 严重度 |
|---|---|---|
| 空输入直接给出 NaN/Infinity/undefined/null/0 | **240** | 高 |
| 改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验） | **48** | 低 |
| 空输入直接给出结论（同空/默认结论，对照法确认） | **7** | 中 |
| 重置按钮未改变任何输入 | **31** | 低 |
| 点击主按钮抛异常（含 console 报错） | **2** | 高 |
| 导出/下载按钮 onclick 目标函数不存在（必死） | **1** | 中 |
| 死控件（静态） | **1** 页 / 2 个控件 | 低-中 |

> **置信度分层**：高/中置信度缺陷页 **250** 页（点击抛异常、空态坏值/结论、死按钮、死控件）；`no_effect` 基线 **53** 页，已改用「0.8× 相对量级变异」主探针并在无变化时追加「5× 放大探针」；复扫后 **5** 页退出、剩余 **48** 页，三档为真无效 **4** / 阈值掩蔽 **3** / 探针失真 **41**（显示精度掩蔽不计缺陷）。逐页结论见 `plan/no-effect-recheck.md`。

### 精度/阈值掩蔽：探针被结果区小数位抹平（8 页，不计缺陷）

> 判定：主探针 0.8× 默认值后结果区无变化，但同一控件放大到 5× 后结果变化。说明页面计算链路正常，只是 20% 量级差在 `toFixed(2)`/整数输出下不可见。

- `tools/advertising/assessor-52.html` — 主探针 budget [number] "50000" → "40000"｜结果最大小数位 2｜放大探针 budget [number] "40000" → "200037"; venueCost [number] "15000" → "7503…
- `tools/advertising/assessor-55.html` — 主探针 targetPop [number] "500" → "400"｜结果最大小数位 1｜放大探针 targetPop [number] "400" → "2037"; spots [number] "60" → "337"; rating…
- `tools/healthcare/apgar.html` — 主探针 appearance [number] "2" → "1.6"｜结果最大小数位 0｜放大探针 appearance [number] "1.6" → "45"; pulse [number] "2" → "47"; grimace […
- `tools/hematology/detector-5.html` — 主探针 granCD59 [number] "35" → "28"｜结果最大小数位 1｜放大探针 granCD59 [number] "28" → "177"; granCD55 [number] "32" → "197"; rbcCD5…
- `tools/hr/overtime-pay-calc.html` — 主探针 hourly [number] "25" → "20"｜结果最大小数位 2｜放大探针 hourly [number] "20" → "137"; weekday [number] "0" → "49"; weekend [nu…
- `tools/it/crc-calculator.html` — 主探针 cw [number] "40" → "32"｜结果最大小数位 1｜放大探针 cw [number] "32" → "64"; input [textarea] "48656c6c6f" → "48656c6c6f21…
- `tools/it/keyword-density.html` — 主探针 minLen [number] "10.5" → "8.4"｜结果最大小数位 2｜放大探针 minLen [number] "8.4" → "20"; inputText [textarea] "abc 123" → "probe-…
- `tools/it/random-string.html` — 主探针 len [number] "16" → "12.8"｜结果最大小数位 0｜放大探针 len [number] "12.8" → "101"; cnt [number] "5" → "62"

## 按行业分布（便于分派修复线）

| 类型 | 集中行业（页数） |
|---|---|
| 空输入直接给出 NaN/Infinity/undefined/null/0 | tools/eco/ 18、tools/dynamics/ 12、tools/geometry/ 11、tools/kinematics/ 8、tools/economics/ 7、tools/aerospace/ 5、tools/banking/ 5、tools/healthcare/ 5 |
| 改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验） | tools/it/ 14、tools/design/ 2、tools/food-processing/ 2、tools/forensic-medicine/ 2、tools/hematology/ 2、tools/image/ 2、tools/life/ 2、tools/music/ 2 |
| 空输入直接给出结论（同空/默认结论，对照法确认） | tools/aerospace/ 1、tools/biz/ 1、tools/clinical-lab/ 1、tools/fitness/ 1、tools/hydraulic/ 1、tools/reproductive-medicine/ 1、tools/tax/ 1 |
| 重置按钮未改变任何输入 | tools/rheumatology/ 4、tools/rehabilitation/ 3、tools/it/ 3、tools/elderly/ 2、tools/general/ 2、tools/hematology/ 2、tools/audio/ 1、tools/biz/ 1 |
| 点击主按钮抛异常（含 console 报错） | tools/it/ 1 |
| 导出/下载按钮 onclick 目标函数不存在（必死） | tools/it/ 1 |

## Top 50 高影响页面（按严重度加权）

| # | 页面 | 得分 | 类型 | 证据 |
|---|---|---|---|---|
| 1 | `tools/it/matrix-multiplier.html` | 3 | click_error | 按钮「计算乘法」｜click: Cannot read properties of null (reading 'value') @ getM (/tools/it/matrix-multiplier… |
| 2 | `tools/aerospace/descent-rate.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.0下降率 (m/min)0.00下降率 (m/s)0.00水平速度 (m/s)0.000下降梯度 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 3 | `tools/aerospace/drag-force.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00阻力 D (N)0.0动压 q = ½ρv² (Pa)0.00阻力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 4 | `tools/aerospace/lift-equation.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00升力 L (N)0.0动压 q = ½ρv² (Pa)0.00升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 5 | `tools/aerospace/lift-force.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00升力 L (kN)0.0升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 6 | `tools/aerospace/thrust-required.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000所需推力 (kN)0.0动压 q = ½ρv² (Pa)0.00等效推力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 7 | `tools/agriculture/agri-calculator.html` | 2.6 | empty_bogus | 空输入点「计算配比」→ 结果区 氮 (N)0.00kg磷 (P₂O₅)0.00kg钾 (K₂O)0.00kg配方比例：0-0-0施肥面积：0 亩每亩用量：0 kg/亩肥料总量：0.0 kg ⏐ 📋 … |
| 8 | `tools/astronomy/hubble-redshift-distance.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00距离 d (Mpc)0.00d (百万光年)0.00退行速度 v = cz (km/s)0.0000d (十亿光年) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 9 | `tools/astronomy/kepler-equation.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000偏近点角 E (°)0.00000E (rad) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 10 | `tools/astronomy/light-travel-time.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000传播时间 t (min)0.0t (s)0.0000距离 (天文单位 AU)0.0000传播时间 (h)0.000e+0距离 (光年) ⏐ 📋 复制结果⬇️ 导… |
| 11 | `tools/baking/recipe-scaler.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 缩放后配方（×0） ⏐ 📋 复制结果⬇️ 导出 TXT |
| 12 | `tools/banking/amortization-first-interest.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00首月利息 I₁0.00首月还本金0.000年利率 (%)0.0000首月利息占本金比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 13 | `tools/banking/continuous-compounding.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00连续复利终值 A0.00利息总额0.0000年实际收益率 (%)0.0000较年复利增益 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 14 | `tools/banking/effective-annual-rate.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000有效年利率 EAR (%)0.00000EAR (小数)0.0000EAR 高于名义利率 (百分点)0.0000与连续复利之差 (百分点) ⏐ 📋 复制结果⬇️… |
| 15 | `tools/banking/net-worth.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0净资产 NW (元)0.00负债率 (%)0.000资产覆盖倍数0.00净资产占资产 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 16 | `tools/banking/tax-equivalent-yield.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000税后等效收益率 TEY (%)0.000应税需高出的百分点0.0边际税率 (%)0.0000免税溢价系数减一 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 17 | `tools/chemistry/gibbs-free-energy.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000ΔG (kJ/mol)平衡反应方向 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 18 | `tools/chemistry/kp-kc.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000e+0压力平衡常数 Kp0.0RT (L·atm/(mol·K)) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 19 | `tools/chemistry/mole-fraction.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.0000总物质的量 (mol) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 20 | `tools/chemistry/partial-pressure.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00分压 Pᵢ (kPa)0.00其余组分分压 (kPa)0.000摩尔分数 (%)0.000其余组分占比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 21 | `tools/chinese-cook/estimate-16.html` | 2.6 | empty_bogus | 空输入点「🧮 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 22 | `tools/design/px-to-rem.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 转换结果 ⏐ 0px = 0.0000rem ⏐ 📋 复制结果⬇️ 导出 TXT |
| 23 | `tools/dynamics/angular-momentum.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000角动量 L (kg·m²/s)0.000两倍角动量0.0000由 L 反推角速度0.000转动动能 (J) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 24 | `tools/dynamics/impulse.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00冲量 J (N·s)0.0冲量 (N·ms 牛毫秒)0.0000冲量 (kgf·s 千克力秒)0.0000力与作用时间之比 (N/s) ⏐ 📋 复制结果⬇️ 导出… |
| 25 | `tools/dynamics/inclined-plane-accel.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000加速度 a (m/s²)静止/需外力状态 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 26 | `tools/dynamics/kinetic-friction.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00动摩擦力 F_k (N)0.0000正压力与摩擦系数之比0.0000摩擦力 (kgf 千克力)0.0000摩擦系数平方 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 27 | `tools/dynamics/momentum.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.0动量 p (kg·m/s)0.0动能 Ek (J)0.0动量乘速度 (kg·m²/s²)0.0000质量与速度之比 (kg·s/m) ⏐ 📋 复制结果⬇️ 导出 T… |
| 28 | `tools/dynamics/power-force.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.0功率 P (W)0.00P (kW)0.000功率 (公制马力 PS)0.000功率 (英制马力 hp)0.000每小时做功 (kJ/h) ⏐ 📋 复制结果⬇️ 导… |
| 29 | `tools/dynamics/power-rotational.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00旋转功率 P (W)0.0000旋转功率 (hp)0.0000旋转功率 (kW)0.0000旋转功率 (PS) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 30 | `tools/dynamics/rotational-kinetic-energy.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000转动动能 E (J)0.000两倍转动动能（I 乘 ω²）0.0000角动量 L0.0000转速 (转/秒) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 31 | `tools/dynamics/spring-potential.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000弹性势能 U (J)0.000对应弹力 F (N)0.0000劲度与位移平方之积 (J)0.0000弹性势能 (mJ 毫焦) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 32 | `tools/dynamics/torque-force.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00力矩 τ (N·m)0.0000有效力臂 (m)0.000径向分量 (N) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 33 | `tools/dynamics/weight-force.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00重力 W (N)0.00W (kgf)0.00月球表面重力 (N)0.00火星表面重力 (N)0.000重力 W (kgf 标准重力) ⏐ 📋 复制结果⬇️ 导出… |
| 34 | `tools/dynamics/work-energy-theorem.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00合外力功 W (J)0.00末动能 (J)0.00初动能 (J) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 35 | `tools/eco/battery-storage.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 可用电量：0.00 kWh总能量：0.00 kWh ⏐ 📋 复制结果⬇️ 导出 TXT |
| 36 | `tools/eco/convert-air-aqi.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0等级 优 ｜ 输入浓度 0 µg/m³ ｜ 建议 可正常户外活动 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 37 | `tools/eco/eco-10.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效植树：0 棵 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 38 | `tools/eco/eco-11.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 单次额外燃油：0.00 L年额外燃油：0.00 L年额外碳排：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 39 | `tools/eco/eco-16.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效减少汽车：0 辆 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 40 | `tools/eco/eco-4.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 日产生量：0.00 吨/天年产生量：0.00 吨/年累计吨天数：0 kg·天 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 41 | `tools/eco/eco-7.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 总标准煤：0.00 kgce总 kWh：0.00 kWh总 MJ：0.00 MJ ⏐ 📋 复制结果⬇️ 导出 TXT |
| 42 | `tools/eco/eco-8.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 总株数：0 株年碳汇量：0.00 吨/年累计碳汇：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 43 | `tools/eco/eco.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 电力碳排：0.00 kg燃煤碳排：0.00 kg天然气碳排：0.00 kg汽油碳排：0.00 kg总碳排：0.00 kg ⏐ 📋 复制结果⬇️ 导出 TXT |
| 44 | `tools/eco/ecological-footprint.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 生态足迹：0.000 gha ⏐ 📋 复制结果⬇️ 导出 TXT |
| 45 | `tools/eco/electricity-carbon.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 CO₂ 排放：0.00 kg等效树木吸收天数：0.0 天 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 46 | `tools/eco/env-impact-score.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 综合评分：0.0 分最高项：0 分 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 47 | `tools/eco/landfill-methane.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 CH₄ 产量：0.0 kg/年CO₂ 当量：0.0 kgCO₂e ⏐ 📋 复制结果⬇️ 导出 TXT |
| 48 | `tools/eco/rainwater-harvest.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 收集量：0 L折合吨：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 49 | `tools/eco/solar-output.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 发电量：0.0 kWh等效减排：0.00 kgCO₂ ⏐ 📋 复制结果⬇️ 导出 TXT |
| 50 | `tools/eco/water-footprint.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 总耗水：0 L折合 m³：0.00 m³ ⏐ 📋 复制结果⬇️ 导出 TXT |

## 一、按钮有效性（点了没反应 / 点了报错）

### 点击主按钮抛异常（含 console 报错）（2 页）

- `tools/it/matrix-multiplier.html` — 按钮「计算乘法」｜click: Cannot read properties of null (reading 'value') @ getM (/tools/it/matrix-multiplier.html:283:68)
- `tools/marketing/ad-roi.html` — 空态点「计算 ROI」｜click: Cannot read properties of null (reading 'value')（2026-11-05 复扫新增）

## 二、空态（没填也敢给结论）

### 空输入直接给出 NaN/Infinity/undefined/null/0（上轮 121 页；复扫后 240 页，以「修效验证」节为准）

- `tools/aerospace/descent-rate.html` — 空输入点「计算」→ 结果区 0.0下降率 (m/min)0.00下降率 (m/s)0.00水平速度 (m/s)0.000下降梯度 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/aerospace/drag-force.html` — 空输入点「计算」→ 结果区 0.00阻力 D (N)0.0动压 q = ½ρv² (Pa)0.00阻力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/aerospace/lift-equation.html` — 空输入点「计算」→ 结果区 0.00升力 L (N)0.0动压 q = ½ρv² (Pa)0.00升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/aerospace/lift-force.html` — 空输入点「计算」→ 结果区 0.00升力 L (kN)0.0升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/aerospace/thrust-required.html` — 空输入点「计算」→ 结果区 0.000所需推力 (kN)0.0动压 q = ½ρv² (Pa)0.00等效推力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/agriculture/agri-calculator.html` — 空输入点「计算配比」→ 结果区 氮 (N)0.00kg磷 (P₂O₅)0.00kg钾 (K₂O)0.00kg配方比例：0-0-0施肥面积：0 亩每亩用量：0 kg/亩肥料总量：0.0 kg ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/astronomy/hubble-redshift-distance.html` — 空输入点「计算」→ 结果区 0.00距离 d (Mpc)0.00d (百万光年)0.00退行速度 v = cz (km/s)0.0000d (十亿光年) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/astronomy/kepler-equation.html` — 空输入点「计算」→ 结果区 0.000偏近点角 E (°)0.00000E (rad) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/astronomy/light-travel-time.html` — 空输入点「计算」→ 结果区 0.000传播时间 t (min)0.0t (s)0.0000距离 (天文单位 AU)0.0000传播时间 (h)0.000e+0距离 (光年) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/baking/recipe-scaler.html` — 空输入点「计算」→ 结果区 缩放后配方（×0） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/amortization-first-interest.html` — 空输入点「计算」→ 结果区 0.00首月利息 I₁0.00首月还本金0.000年利率 (%)0.0000首月利息占本金比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/continuous-compounding.html` — 空输入点「计算」→ 结果区 0.00连续复利终值 A0.00利息总额0.0000年实际收益率 (%)0.0000较年复利增益 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/effective-annual-rate.html` — 空输入点「计算」→ 结果区 0.000有效年利率 EAR (%)0.00000EAR (小数)0.0000EAR 高于名义利率 (百分点)0.0000与连续复利之差 (百分点) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/net-worth.html` — 空输入点「计算」→ 结果区 0净资产 NW (元)0.00负债率 (%)0.000资产覆盖倍数0.00净资产占资产 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/tax-equivalent-yield.html` — 空输入点「计算」→ 结果区 0.000税后等效收益率 TEY (%)0.000应税需高出的百分点0.0边际税率 (%)0.0000免税溢价系数减一 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chemistry/gibbs-free-energy.html` — 空输入点「计算」→ 结果区 0.000ΔG (kJ/mol)平衡反应方向 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chemistry/kp-kc.html` — 空输入点「计算」→ 结果区 0.000e+0压力平衡常数 Kp0.0RT (L·atm/(mol·K)) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chemistry/mole-fraction.html` — 空输入点「计算」→ 结果区 0.0000总物质的量 (mol) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chemistry/partial-pressure.html` — 空输入点「计算」→ 结果区 0.00分压 Pᵢ (kPa)0.00其余组分分压 (kPa)0.000摩尔分数 (%)0.000其余组分占比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chinese-cook/estimate-16.html` — 空输入点「🧮 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/design/px-to-rem.html` — 空输入点「计算」→ 结果区 转换结果 ⏐ 0px = 0.0000rem ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/angular-momentum.html` — 空输入点「计算」→ 结果区 0.000角动量 L (kg·m²/s)0.000两倍角动量0.0000由 L 反推角速度0.000转动动能 (J) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/impulse.html` — 空输入点「计算」→ 结果区 0.00冲量 J (N·s)0.0冲量 (N·ms 牛毫秒)0.0000冲量 (kgf·s 千克力秒)0.0000力与作用时间之比 (N/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/inclined-plane-accel.html` — 空输入点「计算」→ 结果区 0.000加速度 a (m/s²)静止/需外力状态 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/kinetic-friction.html` — 空输入点「计算」→ 结果区 0.00动摩擦力 F_k (N)0.0000正压力与摩擦系数之比0.0000摩擦力 (kgf 千克力)0.0000摩擦系数平方 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/momentum.html` — 空输入点「计算」→ 结果区 0.0动量 p (kg·m/s)0.0动能 Ek (J)0.0动量乘速度 (kg·m²/s²)0.0000质量与速度之比 (kg·s/m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/power-force.html` — 空输入点「计算」→ 结果区 0.0功率 P (W)0.00P (kW)0.000功率 (公制马力 PS)0.000功率 (英制马力 hp)0.000每小时做功 (kJ/h) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/power-rotational.html` — 空输入点「计算」→ 结果区 0.00旋转功率 P (W)0.0000旋转功率 (hp)0.0000旋转功率 (kW)0.0000旋转功率 (PS) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/rotational-kinetic-energy.html` — 空输入点「计算」→ 结果区 0.000转动动能 E (J)0.000两倍转动动能（I 乘 ω²）0.0000角动量 L0.0000转速 (转/秒) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/spring-potential.html` — 空输入点「计算」→ 结果区 0.000弹性势能 U (J)0.000对应弹力 F (N)0.0000劲度与位移平方之积 (J)0.0000弹性势能 (mJ 毫焦) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/torque-force.html` — 空输入点「计算」→ 结果区 0.00力矩 τ (N·m)0.0000有效力臂 (m)0.000径向分量 (N) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/weight-force.html` — 空输入点「计算」→ 结果区 0.00重力 W (N)0.00W (kgf)0.00月球表面重力 (N)0.00火星表面重力 (N)0.000重力 W (kgf 标准重力) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/work-energy-theorem.html` — 空输入点「计算」→ 结果区 0.00合外力功 W (J)0.00末动能 (J)0.00初动能 (J) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/battery-storage.html` — 空输入点「计算」→ 结果区 可用电量：0.00 kWh总能量：0.00 kWh ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/convert-air-aqi.html` — 空输入点「计算」→ 结果区 0等级 优 ｜ 输入浓度 0 µg/m³ ｜ 建议 可正常户外活动 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-10.html` — 空输入点「计算」→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效植树：0 棵 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-11.html` — 空输入点「计算」→ 结果区 单次额外燃油：0.00 L年额外燃油：0.00 L年额外碳排：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-16.html` — 空输入点「计算」→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效减少汽车：0 辆 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-4.html` — 空输入点「计算」→ 结果区 日产生量：0.00 吨/天年产生量：0.00 吨/年累计吨天数：0 kg·天 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-7.html` — 空输入点「计算」→ 结果区 总标准煤：0.00 kgce总 kWh：0.00 kWh总 MJ：0.00 MJ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-8.html` — 空输入点「计算」→ 结果区 总株数：0 株年碳汇量：0.00 吨/年累计碳汇：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco.html` — 空输入点「计算」→ 结果区 电力碳排：0.00 kg燃煤碳排：0.00 kg天然气碳排：0.00 kg汽油碳排：0.00 kg总碳排：0.00 kg ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/ecological-footprint.html` — 空输入点「计算」→ 结果区 生态足迹：0.000 gha ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/electricity-carbon.html` — 空输入点「计算」→ 结果区 CO₂ 排放：0.00 kg等效树木吸收天数：0.0 天 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/env-impact-score.html` — 空输入点「计算」→ 结果区 综合评分：0.0 分最高项：0 分 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/landfill-methane.html` — 空输入点「计算」→ 结果区 CH₄ 产量：0.0 kg/年CO₂ 当量：0.0 kgCO₂e ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/rainwater-harvest.html` — 空输入点「计算」→ 结果区 收集量：0 L折合吨：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/solar-output.html` — 空输入点「计算」→ 结果区 发电量：0.0 kWh等效减排：0.00 kgCO₂ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/water-footprint.html` — 空输入点「计算」→ 结果区 总耗水：0 L折合 m³：0.00 m³ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/water-saving.html` — 空输入点「计算」→ 结果区 节约水量：0.0 L折合吨：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/wind-power.html` — 空输入点「计算」→ 结果区 功率：0.00 kW ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/balance-of-trade.html` — 空输入点「计算」→ 结果区 0贸易差额 BoT0.00差额占出口比 (%)0.000出口进口比0进出口总额 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/compound-amount.html` — 空输入点「计算」→ 结果区 0.00复利终值 F0.00利息总额 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/fv-annuity.html` — 空输入点「计算」→ 结果区 0.00年金终值 FV0.00利息总额 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/labor-force.html` — 空输入点「计算」→ 结果区 0劳动力 LF0.00失业率 (%)0.00就业率 (%)0.0000就业与失业人数比 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/okuns-law.html` — 空输入点「计算」→ 结果区 0.00失业率变化 Δu (百分点)0.00增长缺口0.00失业率变化幅值 (百分点)0.000相对增长缺口 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/pv-annuity.html` — 空输入点「计算」→ 结果区 0.00年金现值 PV0.00贴现总额 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/real-gdp.html` — 空输入点「计算」→ 结果区 0.00实际 GDP0.00价格扭曲部分0.00实际占名义比重 (%)0.00价格扭曲占比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electromagnetism/coil-torque.html` — 空输入点「计算」→ 结果区 0.0000磁力矩 τ (N·m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electromagnetism/energy-capacitor.html` — 空输入点「计算」→ 结果区 0.000储能 E (µJ)0.000e+0储能 E (J)0.000电荷量 (mC)0.0000e+0电荷量 Q = CV (C) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electromagnetism/magnetic-flux.html` — 空输入点「计算」→ 结果区 0.000e+0磁通 Φ (Wb)0.00Φ (µWb)0.0000磁通 (mWb)0.0000磁感应强度复算 (T) ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 结果含义磁通量 Φ=B…
- `tools/electromagnetism/solenoid-field.html` — 空输入点「计算」→ 结果区 0.000e+0磁感应强度 B (T)0.000B (mT)0.0000e+0单位电流磁场 (T/A)0.000磁感应强度 B (Gauss) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/encode/base32.html` — 空输入点「计算」→ 结果区 编码长度：0 字符无填充长度：0 字符 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/encode/encode-2.html` — 空输入点「计算」→ 结果区 估算差异比特数：0 位采样差异：0 位汉明距离：0 位 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/encode/shannon-entropy.html` — 空输入点「计算」→ 结果区 信息熵 H：0.0000 bit/符号 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/encode/url-encoded-length.html` — 空输入点「计算」→ 结果区 编码后长度：0 字符膨胀率：0.0 % ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/energy/carbon-footprint.html` — 空输入点「♻️ 计算」→ 结果区 年度总排放 ⏐ 0 kg CO₂e ⏐ 约合 ⏐ 0.00 吨 ⏐ 对比中国人均 ⏐ 0% ⏐ 对比全球人均 ⏐ 0% ⏐ 🌳 抵消需种树 ⏐ 0 棵 / 年 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/energy/energy-calculator.html` — 空输入点「计算碳排放」→ 结果区 0.0月用电碳排放 kg ⏐ 0.0月用气碳排放 kg ⏐ 0.0月驾车碳排放 kg ⏐ 0年总碳排放 kg CO₂ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/energy/power-consumption.html` — 空输入点「🧮 计算」→ 结果区 总耗电 ⏐ 0.0 kWh ⏐ 总电费 ⏐ ¥ 0.00 ⏐ 日均电费 ⏐ ¥ 0.00 ⏐ 日均耗电 ⏐ 0.0 kWh ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ent/caloric-test.html` — 空输入点「计算分析」→ 结果区 0%单侧减弱 UW0%方向优势 DP0.0右耳总和(°/s)0.0左耳总和(°/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/film/convert-time-1.html` — 空输入点「计算」→ 结果区 帧率需>0 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fire/calc-water-pressure-hydrant.html` — 空输入点「🧮 计算所需压力」→ 结果区 满足压力校核0.000 MPa所需入口压力0.000 MPa可用入口压力+0.000 MPa安全余量高程折算 0.000 MPa = 栓口 0.000 MPa + 管损 0.000 MPa。 ⏐ 📋…
- `tools/fishery/calc-39.html` — 空输入点「🧮 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fishery/salinity-calculator.html` — 空输入点「🐟 计算」→ 结果区 ⚠️ 四项均需填写有效数值：现有水量须 >0，三个盐度须 ≥0。未测盐度请勿留空（淡水请明确输入 0） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fluid/bernoulli-pressure.html` — 空输入点「计算」→ 结果区 0.0压力 P₂ (Pa)0.00压差 (kPa) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fluid/buoyancy-force.html` — 空输入点「计算」→ 结果区 0.00浮力 F_b (N)0.0000排开液体质量 (kg)0.00排开液体质量 (g) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fluid/stagnation-pressure.html` — 空输入点「计算」→ 结果区 0.0驻点压力 p₀ (Pa)0.0动压 q (Pa)0.0000驻点压比 p0/p ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food-processing/material-balance.html` — 空输入点「核算」→ 结果区 0.00总投入0.00总产出0.00损耗0.0%得率 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food-processing/recipe-cost-calculator.html` — 空输入点「核算成本」→ 结果区 ¥0.00总成本0g配方总用量0g实际耗用-每kg成本 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food/calc-concentration.html` — 空输入点「🐟 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/general/wurenjixuantingwuchajisuan.html` — 空输入点「🧮 计算」→ 结果区 0.00水平误差 (m)0.00垂直误差 (m)0.00三维综合误差 (m)0.00开环飘移量 (m)高精度悬停悬停精度评定 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/arc-length.html` — 空输入点「计算」→ 结果区 0.0000弧长 L (m)0.0000圆心角 (rad)0.000占整圆比例 (%)0.0000对应扇形面积 (m²) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/chord-length.html` — 空输入点「计算」→ 结果区 0.0000弦长 c (m)0.0000半弦长 (m)0.0000对应弧长 (m)0.0000矢高 (m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/circle-area.html` — 空输入点「计算」→ 结果区 0.0000圆面积 A (m²)0.0000圆周长 (m)0.0000球体积 (m³)0.0000直径 (m)0.0000半圆面积 (m²) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/circle-circumference.html` — 空输入点「计算」→ 结果区 0.0000圆周长 C (m)0.0000直径 (m)0.0000圆面积 (m²)0.0000球体积 (m³)0.0000内接正方形面积 (m²) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/distance-3d.html` — 空输入点「计算」→ 结果区 0.000三维距离 d ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/ellipse-area.html` — 空输入点「计算」→ 结果区 0.000椭圆面积 A (m²)0.000000长短半轴之比0.000椭圆周长近似 (m)0.000等面积圆面积 π√(ab)（半径=√(ab)） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/midpoint-2d.html` — 空输入点「计算」→ 结果区 0.000中点 x_M0.000中点 y_M ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/sector-area.html` — 空输入点「计算」→ 结果区 0.0000扇形面积 A (m²)0.000占整圆比例 (%)0.0000弧长 L = r·θ (m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/sphere-volume.html` — 空输入点「计算」→ 结果区 0.000球体体积 V (m³)0.000球表面积 (m²)0.000大圆周长 (m)0.000球体积 (L 升)0.000球体积 (cm³) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/torus-volume.html` — 空输入点「计算」→ 结果区 0.000环体体积 V (m³)0.000环体表面积 (m²)0.000中心圆周长 (m)0.0000体积与环半径之比 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/triangle-heron.html` — 空输入点「计算」→ 结果区 这三条边不能构成三角形：需满足任意两边之和大于第三边（当前 0、0、0）。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/apgar.html` — 空输入点「计算」→ 结果区 Apgar 总分：0 分临床意义：重度窒息 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/chads-vasc.html` — 空输入点「计算」→ 结果区 评分：0 分风险分层：低危 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/healthcare-5.html` — 空输入点「计算」→ 结果区 维持需求：0.0 g目标需求：0.0 g每餐建议：0.0 g ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/morse.html` — 空输入点「计算」→ 结果区 总分：0 分风险等级：低风险 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/wells.html` — 空输入点「计算」→ 结果区 评分：0 分临床概率：低度 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/hematology/detector-5.html` — 空输入点「解读检测结果」→ 结果区 0.0%PNH总克隆（粒细胞）未检测到 PNH 克隆诊断评估无显著溶血风险溶血风险0 U/LLDH 水平 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/home/lighting-calculator.html` — 空输入点「💡 计算」→ 结果区 0 所需总光通量 (lm)
- `tools/home/room-calculator.html` — 空输入点「🧮 计算」→ 结果区 0.00 面积 (m²)
- `tools/hr/overtime-pay-calc.html` — 空输入点「计算加班费」→ 结果区 工作日加班费：0.00 元休息日加班费：0.00 元法定节假日加班费：0.00 元总加班费：0.00 元 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/complete-life-expectancy.html` — 空输入点「计算」→ 结果区 0.000完全期望寿命 e_x0生命表项数 N0.0000平均预期余命 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/ibnr-estimate.html` — 空输入点「计算」→ 结果区 0.00IBNR 准备金 (元)0.00已付赔款比例 (%)0.00已付赔款 (元)0.00最终赔款 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/ibnr-reserve.html` — 空输入点「计算」→ 结果区 0.00IBNR 准备金 (元)0.00最终赔款估计 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/life-cover-need.html` — 空输入点「计算」→ 结果区 0.00建议保额 (元)0.00收入替代部分 (元)0.00保额下限 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/bond-price.html` — 空输入点「计算」→ 结果区 0.00债券价格 P折价状态 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/discounted-payback.html` — 空输入点「计算」→ 结果区 0.00 年折现回收期 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/npv-calc.html` — 空输入点「计算」→ 结果区 0.00净现值 NPV ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/payback-period.html` — 空输入点「计算」→ 结果区 0.00 年静态回收期 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/yield-spread.html` — 空输入点「计算」→ 结果区 0利差 Spread (bps)0.0000利差 (%)0.000基准收益率 (%)0.000对比收益率 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/angular-displacement.html` — 空输入点「计算」→ 结果区 0.000角位移 θ (rad)0.000末角速度 (rad/s)0.000平均角速度 (rad/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/angular-final-velocity.html` — 空输入点「计算」→ 结果区 0.000末角速度 ω (rad/s)0.000角位移 (rad)0.000平均角速度 (rad/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/final-velocity-accel.html` — 空输入点「计算」→ 结果区 0.000末速度 v (m/s)0.000v (km/h)0.000位移 s (m)0.000速度增量 (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/projectile-velocity-components.html` — 空输入点「计算」→ 结果区 0.000水平分量 vₓ (m/s)0.000竖直分量 vᵧ (m/s)0.00合矢量方向 (°)0.0000水平/竖直分量比 vx/vy ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/relativistic-velocity-add.html` — 空输入点「计算」→ 结果区 0.000000合成速度 u (c)0.000e+0u (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/rpm-to-radps.html` — 空输入点「计算」→ 结果区 0.000角速度 ω (rad/s)0.0000转速 (转/秒)0.000角速度 (rad/min)0.0000频率 f (Hz)0.0000角速度平方 (rad²/s²) ⏐ 📋 复制结果⬇️ 导…
- `tools/kinematics/tangential-velocity.html` — 空输入点「计算」→ 结果区 0.000切向速度 v (m/s)0.000切向速度 (km/h)0.0000转速 (转/秒)0.0000角速度复核 (rad/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/velocity-squared.html` — 空输入点「计算」→ 结果区 0.000末速度 v (m/s)0.000速度平方增量 v²−v₀²0.000速度增量 Δv (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/language/language-toolkit.html` — 空输入点「🔢 字符统计」→ 结果区 0总字符数 0汉字数 0英文字母 0数字数 0标点符号 0空格数 0英文单词数 0句子数
- `tools/language/stats-2.html` — 空输入点「统计字符」→ 结果区 总字符数（含空格）：0不含空格字符数：0汉字数：0英文字母数：0英文单词数：0数字字符数：0标点数：0（中文 0 / 西文 0）空白符：0行数：0 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/life/countdown.html` — 空输入点「开始倒计时」→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行 Ctrl/⌘ + Enter 快速运行 ⏐ 📋 复制结果⬇️ 导出 TXT

### 空输入直接给出结论（上轮 34 页；对照法复扫后 7 页，以「修效验证」节为准）

- `tools/aerospace/weight-balance.html` — 空输入点「计算重心」→ 结果区 载荷项重量 (kg)力臂 (m)力矩 (kg·m)使用空机00.000未命名00.000未命名00.000未命名00.000未命名00.000未命名00.000 0 总重量 (kg) 0 总力矩 (k…
- `tools/agriculture/detector-nutrition.html` — 空输入点「判读品质」→ 结果区 综合等级：不合格 优质 2 / 合格 2 / 共 6 项发酵度评价：发酵不足（乳酸 0%）指标实测判读蛋白质0%偏低脂肪0%偏低还原糖0%偏低水分0%优质灰分0%优质乳酸(发酵度)0%偏低品质解读：多…
- `tools/agriculture/irrigation-uniformity.html` — 空输入点「计算」→ 结果区 0.0%克里斯琴森系数CU0.0%分布均匀度DU0.00平均灌水量(mm)0.0%变异系数CV均匀度评价：均匀性差CU参考标准：>90%优秀 \| 80-90%良好 \| 70-80%一般 \| <70%差…
- `tools/automotive/voltage-1.html` — 空输入点「🧮 计算」→ 结果区 38.0用电总电流 (A)38.0含充电总电流 (A)0负载率 (%)-38.0剩余电流 (A)0.55用电功率 (kW)0.00发电机功率 (kW)负载充足平衡评估负载率: 0.0%（安全线 80%…
- `tools/beauty/recommender-face-shape.html` — 空输入点「生成」→ 结果区 生成结果： 1. 心形脸 推荐发型：下巴长度波波头、空气刘海、微卷发尾 妆容建议：眉尾略收，唇妆突出，平衡宽额头 注意：避免过厚刘海和顶部过高 2. 长形脸 推荐发型：法式刘海、齐肩发、横向蓬松卷发 …
- `tools/biz/checker-8.html` — 空输入点「质量评估」→ 结果区 8服务质量总分服务质量不合格质量等级评估维度权重得分明细状态人员标准25%0持证0%/培训0%/着装0%/出勤0%差服务流程30%25巡逻0%/门禁0%/响应0分钟/记录0%差装备设施20%0监控0%…
- `tools/biz/presentation-timer.html` — 空输入点「开始演讲」→ 结果区 进度正常
- `tools/clinical-lab/thyroid-function-model.html` — 空输入点「分析」→ 结果区 结果分析参考区间定位TSH 2 mIU/L → 落在 正常（0.27–4.2 mIU/L 正常）FT3 5 pmol/L → 落在 正常（3.1–6.8 pmol/L 正常）FT4 16 pmol/L…
- `tools/decor/detector-18.html` — 空输入点「检测判定」→ 结果区 室内空气质量检测结果（GB/T 18883-2022）污染物实测值限值判定甲醛0 mg/m³≤0.08✓ 达标 (0%)TVOC0 mg/m³≤0.6✓ 达标 (0%)苯0 mg/m³≤0.03✓ 达…
- `tools/eco/aqi.html` — 空输入点「计算」→ 结果区 健康等级：1 级建议活动时长：0.0 小时PM2.5 估算：0.0 µg/m³ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/noise-superposition.html` — 空输入点「计算叠加」→ 结果区 叠加后总声压级3.0 dB安静声源数量2最大声源0.0 dB能量平均0.0 dB较最大声源增加+3.0 dB距离衰减参考（点声源，距最大声源）：1m0.0 dB5m-14.0 dB10m-20.0 d…
- `tools/edu/assessor-27.html` — 空输入点「知识评估」→ 结果区 知识管理成熟度评估知识捕获：0/10 ✗知识共享：0/10 ✗知识应用：0/10 ✗知识创新：0/10 ✗知识存储：0/10 ✗知识安全：0/10 ✗综合评分：0.00/10成熟度等级：1级-初始级知…
- `tools/electronics/bandwidth.html` — 空输入点「🧮 计算」→ 结果区 0.00e+0所需 GBP (Hz)0.00e+0建议 GBP (Hz)0.00e+0-3dB带宽 (Hz)推荐运放：LM358 / NE5532 (1~10MHz)。建议选型裕量≥2倍，高频应用还需…
- `tools/electronics/capacitance.html` — 空输入点「🧮 计算」→ 结果区 0.00匹配电容 (pF)8推荐标准值 (pF)0.0晶振CL (pF)0.0杂散电容 (pF)C1=C2=C=2×(CL−Cs)。推荐就近选取标准容值8pF，C1与C2各接一个。 ⏐ 匹配电容26.…
- `tools/encode/encode-7.html` — 空输入点「计算」→ 结果区 空间大小：1 近似碰撞概率：0.000000 %安全阈值 n：1 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/endocrinology/detector-metabolism.html` — 空输入点「分析判读」→ 结果区 儿茶酚胺及代谢产物检测结果项目实测参考范围判定24h尿VMA0 mg/24h1-7↓ 偏低24h尿HVA0 mg/24h1-4↓ 偏低血去甲肾上腺素0 pg/mL80-520↓ 偏低血肾上腺素0 pg…
- `tools/energy/air-purifier-area.html` — 空输入点「计算」→ 结果区 0最小面积 m²0推荐面积 m²0最大面积 m²0.0换气次数/小时 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 估算口径适用面积常按 CADR（洁净空气量）× 系数估算：卧室约 CAD…
- `tools/energy/water-tds-evaluator.html` — 空输入点「评估」→ 结果区 直饮水级🎯 适用场景直饮无需处理高端饮用纯净水实验室超纯水稀释💡 健康提示水质极优，口感清冽。TDS极低可能意味着缺乏有益矿物质，长期饮用纯净水建议适当补充矿物质。🌍 WHO标准对比完全符合WH…
- `tools/ent/ahi-severity.html` — 空输入点「计算评估」→ 结果区 0AHI(次/h)0AI暂停指数0HI低通气指数0ODI氧减指数0微觉醒指数100%正常 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺正常00.20.40.60.810
- `tools/ent/hearing-loss-classification.html` — 空输入点「计算分析」→ 结果区 0PTA气导(dB)0PTA骨导(dB)0气骨导差(dB)0高频平均(dB) ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺正常00.20.40.60.810
- `tools/ent/laryngeal-nerve.html` — 空输入点「分析评估」→ 结果区 F0 基频0 Hz异常 ⏐ Jitter 微扰0%正常 ⏐ Shimmer 振幅微扰0%正常 ⏐ NHR 噪谐比0正常 ⏐ HNR 谐噪比0 dB异常 ⏐ MPT 最长发声0 秒异常 ⏐ 📋 复制结…
- `tools/fitness/ratio-19.html` — 空输入点「🧮 计算」→ 结果区 100.0综合对称评分优秀对称等级0差异>10%部位数部位左 (cm)右 (cm)差异差异%对称分上臂0.00.00.0 cm 0.00%100.0大腿0.00.00.0 cm 0.00%100.0小…
- `tools/fitness/weight-capacity-training.html` — 空输入点「🧮 计算」→ 结果区 0.0 kg训练总容量0.0 kg估算 1RM0.0%强度百分比0总次数强度区间：低强度 （推荐次数 25+）极低强度，适合热身与康复。相对 1RM 强度 0.0%（相对容量系数 -）1RM 百分比建…
- `tools/gardening/recommender.html` — 空输入点「生成」→ 结果区 浇水频次推荐：1. 兰花 \| 春季·阴雨·保水性强 → 建议每10-14天1次，忌积水，植料偏干后再浇2. 吊兰 \| 夏季·晴天·排水快 → 建议每2-3天1次，保持土壤微润，避免积水3. 薄荷 \| …
- `tools/general/recommender-24.html` — 空输入点「生成」→ 结果区 替代产品/方案推荐：1. VS Code → 替代：VSCodium、Fleet、Sublime Text2. Premiere Pro → 替代：DaVinci Resolve、Shotcut、Kd…
- `tools/healthcare/checker-manager.html` — 空输入点「执行GSP检查」→ 结果区 📋 GSP质量管理检查报告检查维度评分判定说明质量管理体系与文件0/10需整改质量管理制度、操作规程、记录文件、内审人员与培训管理0/10需整改执业药师配备、岗前培训、年度继续教育设施与设备管理0/…
- `tools/healthcare/water-intake.html` — 空输入点「计算」→ 结果区 推荐饮水量：0 mL折合杯数(250mL)：0.0 杯 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/hr/assessor-training-hr.html` — 空输入点「评估培训效果」→ 结果区 培训效果评估（柯氏前两层）培训主题：参训：0人 \| 时长：0小时能力提升：0→0（+0.0，提升0.0%）L1反应层（满意度）：0/100L2学习层-知识（测试通过率）：0/100L2学习层-技能（能…
- `tools/hr/attendance-stats.html` — 空输入点「📊 统计」→ 结果区 4员工数0 次迟到合计0 次早退合计0 天旷工合计0 天请假合计0 小时加班合计0 元扣款合计4 人全勤人数0 元全勤奖合计0 元加班费合计 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 姓名迟到早退旷工…
- `tools/hydraulic/dam-stability.html` — 空输入点「🧮 计算」→ 结果区 坝体自重 W：21189.60 kN水平水压力 P：11301.12 kN（作用点 h/3=16.00 m）扬压力 U：4237.92 kN（折减系数 α=0.5）抗滑稳定安全系数 Ks：0.975 …
- `tools/insurance/pure-premium.html` — 空输入点「计算」→ 结果区 0.00纯保费 (元/单位)0.00含10%安全边际 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/leather/temp-9.html` — 空输入点「🧮 计算」→ 结果区 0.00%收缩率0.0收缩温度 (℃)优秀热稳定性评估：收缩率＜3%，热稳定性优异。收缩温度偏低，需加强鞣制。 ⏐ 收缩率10.00% → 较差 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/leather/time-34.html` — 空输入点「🧮 计算」→ 结果区 0推荐软化时间 (min)0基准时间 (min)2.92温度系数1.00活力系数操作建议：温度偏低，酶活性不足，建议升温至37~40℃。软化过度会损伤皮纤维，须密切监控。 ⏐ 软化时间31min ⏐ …
- `tools/leather/yield-rate-1.html` — 空输入点「🧮 计算」→ 结果区 0.00%铬回收率0.000回收铬量 (kg)较差处理效果回收率 = (废液浓度−回收后浓度) ÷ 废液浓度 × 100%。回收铬量 = 浓度差 × 处理量 ÷ 10⁶ (kg)。 ⏐ 回收率85.0…

## 三、死控件与辅助按钮

### 改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验）（50 页）

- `tools/agriculture/countdown-4.html` — 按钮「开始孵化」｜构造值 batchName [text] "abc 123" → "abc 123x"｜改前 📖 查看「鸡蛋孵化倒计时（21天）使用指南」 📅 鸡蛋孵化倒计时（21天） ⚠️ 专业工具免责声明 本工具结果为本页… → 点击后 📖 查看「鸡蛋孵化倒计时（21天）使用指南」 📅 鸡蛋孵化倒计时（21天） ⚠️ 专业工具免责声明 本工具结果为本页…
- `tools/cardiology/calc-1.html` — 按钮「评估分级」｜构造值 sbp [number] "175" → "140"｜改前 血压分级：2级高血压 收缩压 ≥160 或 舒张压 ≥100 mmHg 心血管风险分层：中危 2级高血压且无其他危险因素… → 点击后 血压分级：2级高血压 收缩压 ≥160 或 舒张压 ≥100 mmHg 心血管风险分层：中危 2级高血压且无其他危险因素…
- `tools/data/pivot-table.html` — 按钮「📊 生成」｜构造值 inputData [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 🔄 透视表 (sum) 地区 \ 产品 AB 合计 华北 210150 360 华东 200340 540 华南 12… → 点击后 🔄 透视表 (sum) 地区 \ 产品 AB 合计 华北 210150 360 华东 200340 540 华南 12…
- `tools/dermatology/leprosy-grading.html` — 按钮「生成分级报告」｜构造值 leprosyType [select] "TT" → "BT"｜改前 G0D0级残疾无感觉丧失和可见畸形 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 G0D0级残疾无感觉丧失和可见畸形 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/design/flexbox-generator.html` — 按钮「计算」｜构造值 gap [number] "12" → "9.600000000000001"｜改前 生成的 CSS ⏐ 实时预览（3 个项目） ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 生成的 CSS ⏐ 实时预览（3 个项目） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/design/mesh-gradient.html` — 按钮「生成」｜构造值 overlay [text] "abc 123" → "abc 123x"｜改前 background-color: #000000; background-image: radial-gradient… → 点击后 background-color: #000000; background-image: radial-gradient…
- `tools/electromagnetism/free-space-impedance.html` — 按钮「计算」｜构造值 x [number] "0" → "1"｜改前 376.73波阻抗 Z₀ (Ω)2.997925真空光速 (×10⁸ m/s)1.256637真空磁导率 μ₀ (μH/… → 点击后 376.73波阻抗 Z₀ (Ω)2.997925真空光速 (×10⁸ m/s)1.256637真空磁导率 μ₀ (μH/…
- `tools/endocrinology/pcos-diagnosis.html` — 按钮「诊断评估」｜构造值 cycle [number] "45" → "36"｜改前 满足① 排卵障碍满足② 高雄激素满足③ 多囊形态 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 满足① 排卵障碍满足② 高雄激素满足③ 多囊形态 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food-processing/fermentation-brix.html` — 按钮「计算」｜构造值 vol [number] "100" → "80"｜改前 0g糖消耗量0.00%酒精度 ABV0g酒精生成量0gCO₂生成量 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 0g糖消耗量0.00%酒精度 ABV0g酒精生成量0gCO₂生成量 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food-processing/ph-adjustment.html` — 按钮「计算」｜构造值 vol [number] "0.001" → "0.001"｜改前 0.00mL需加溶液量0.000g纯物质量0.0000mol物质的量pH 无变化调节方向 ⏐ 📋 复制结果⬇️ 导出 … → 点击后 0.00mL需加溶液量0.000g纯物质量0.0000mol物质的量pH 无变化调节方向 ⏐ 📋 复制结果⬇️ 导出 …
- `tools/forensic-medicine/electrocution-injury.html` — 按钮「分析电击伤」｜构造值 currentType [select] "ac" → "dc"｜改前 0阳性特征数0%特征符合度 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 0阳性特征数0%特征符合度 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/forensic-medicine/rigor-mortis.html` — 按钮「评估死后时间」｜构造值 envTemp [select] "low" → "normal"｜改前 2.0平均僵硬度2.0上部关节2.0下部关节 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 2.0平均僵硬度2.0上部关节2.0下部关节 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/funeral/memorial-date.html` — 按钮「计算」｜构造值 memTitle [text] "abc 123" → "abc 123x"｜改前 • 头七：逝后第 7 天 • 三七 / 五七：逝后第 21 / 35 天 • 百日：逝后第 100 天 • 周年：逝后满… → 点击后 • 头七：逝后第 7 天 • 三七 / 五七：逝后第 21 / 35 天 • 百日：逝后第 100 天 • 周年：逝后满…
- `tools/gardening/plant-calendar.html` — 按钮「📅 月份视图」｜构造值 search [text] "abc 123" → "abc 123x"｜改前 📖 查看「蔬菜种植时间历使用指南」 📅 蔬菜种植日历 按月份/季节/类别查看蔬菜种植时间，含播种、移栽、收获、生长期… → 点击后 📖 查看「蔬菜种植时间历使用指南」 📅 蔬菜种植日历 按月份/季节/类别查看蔬菜种植时间，含播种、移栽、收获、生长期…
- `tools/hematology/itp-risk-score.html` — 按钮「评分」｜构造值 drug [select] "heparin" → "quinine"｜改前 9总分 (满分8)确定 (Definite)因果关系等级 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺不太可能… → 点击后 9总分 (满分8)确定 (Definite)因果关系等级 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺不太可能…
- `tools/hematology/mm-staging.html` — 按钮「分期」｜构造值 albumin [number] "35" → "28"｜改前 R-ISS III分期ISS 3ISS分期43个月中位OS ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 R-ISS III分期ISS 3ISS分期43个月中位OS ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/image/image-compress.html` — 按钮「压缩质量80·输出格式webp·最大尺寸（等比缩放）1920」｜构造值 fmt [select] "webp" → "jpeg"｜改前 ⚡ 效率工具栏 ✓ 本地处理 1 个文件入口 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ⚡ 效率工具栏 ✓ 本地处理 1 个文件入口 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/image/wechat-cover-maker.html` — 按钮「生成」｜构造值 title [text] "abc 123" → "abc 123x"｜改前 ✨ 公众号封面生成器 纯前端生成 900×383 封面图：标题 + 副标题 + 背景渐变 + 下载。 标题 副标题 背景… → 点击后 ✨ 公众号封面生成器 纯前端生成 900×383 封面图：标题 + 副标题 + 背景渐变 + 下载。 标题 副标题 背景…
- `tools/it/ast-viewer.html` — 按钮「解析 AST」｜构造值 codeInput [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 ⬇️ 导出统计 CSV ⏐ 0 ⏐ 0 ⏐ 0 ⏐ 0 → 点击后 ⬇️ 导出统计 CSV ⏐ 0 ⏐ 0 ⏐ 0 ⏐ 0
- `tools/it/calc-7.html` — 按钮「格式化对象」｜构造值 jsonInput [textarea] "{\"a\":1,\"b\":2}" → "{\"a\":2}"｜改前 对象中不存在键 user。 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 对象中不存在键 user。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/docker-run-converter.html` — 按钮「计算」｜构造值 cmd [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 docker-compose.yml ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 docker-compose.yml ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/dockerfile-generator.html` — 按钮「计算」｜构造值 port [number] "3000" → "2400"｜改前 Dockerfile ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 Dockerfile ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/hill-cipher.html` — 按钮「加密 ↑」｜构造值 key [text] "abc 123" → "abc 123x"｜改前 密钥矩阵3325行列式9 mod 26行列式逆元3逆矩阵1517209 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 密钥矩阵3325行列式9 mod 26行列式逆元3逆矩阵1517209 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/html-nesting-checker.html` — 按钮「检查」｜构造值 html [textarea] "<div><p>hi</p></div>" → "<div><span>x</span…｜改前 ✅ HTML 嵌套结构合法（无未闭合/错误嵌套标签） ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 结果含义… → 点击后 ✅ HTML 嵌套结构合法（无未闭合/错误嵌套标签） ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 结果含义…
- `tools/it/json-to-tsv.html` — 按钮「转换 →」｜构造值 jsonInput [textarea] "{\"a\":1}" → "{\"a\":2}"｜改前 name age city 张三 30 上海 李四 25 北京 → 点击后 name age city 张三 30 上海 李四 25 北京
- `tools/it/mac-lookup.html` — 按钮「查询」｜构造值 macInput [text] "abc 123" → "abc 123x"｜改前 ❌ 长度错误：当前 6 个十六进制字符，应为 12 位 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ❌ 长度错误：当前 6 个十六进制字符，应为 12 位 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/password-generator.html` — 按钮「🎲 生成」｜构造值 length [number] "66" → "52.800000000000004"｜改前 16+ 推荐长度 4种 字符类型 90天 更换周期 2FA 双重验证 ⏐ ⚡ 效率工具栏 ✓ 本地处理 13 个参数 C… → 点击后 16+ 推荐长度 4种 字符类型 90天 更换周期 2FA 双重验证 ⏐ ⚡ 效率工具栏 ✓ 本地处理 13 个参数 C…
- `tools/it/plist-parser.html` — 按钮「压缩」｜构造值 input [textarea] "<root><item>1</item>" → "<root><item>3</it…｜改前 { "name": "Alice", "age": 30, "active": true, "tags": [ "adm… → 点击后 { "name": "Alice", "age": 30, "active": true, "tags": [ "adm…
- `tools/it/protobuf-parser.html` — 按钮「解析」｜构造值 input [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 { "syntax": "", "package": "", "imports": [], "options": [],… → 点击后 { "syntax": "", "package": "", "imports": [], "options": [],…
- `tools/it/sitemap-generator.html` — 按钮「计算」｜构造值 urls [textarea] "https://example.com/" → "https://example.co…｜改前 sitemap.xml ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 sitemap.xml ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/toml-formatter.html` — 按钮「格式化」｜构造值 input [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 title = "toolbox" port = 8080 replicas = 3 ⏐ 📋 复制结果⬇️ 导出 TX… → 点击后 title = "toolbox" port = 8080 replicas = 3 ⏐ 📋 复制结果⬇️ 导出 TX…
- `tools/it/uuid-v5-generator.html` — 按钮「生成」｜构造值 ns [text] "abc 123" → "abc 123x"｜改前 example.com → cfbff0d1-9375-5685-968c-48ce8b15ae17example.or… → 点击后 example.com → cfbff0d1-9375-5685-968c-48ce8b15ae17example.or…
- `tools/life/chinese-number.html` — 按钮「转换」｜构造值 inputVal [text] "abc 123" → "abc 123x"｜改前 无法识别输入 ⏐ 简体：〇 一 二 三 四 五 六 七 八 九 十 百 千 万 亿 大写：零 壹 贰 叁 肆 伍 陆 柒… → 点击后 无法识别输入 ⏐ 简体：〇 一 二 三 四 五 六 七 八 九 十 百 千 万 亿 大写：零 壹 贰 叁 肆 伍 陆 柒…
- `tools/life/unit-converter.html` — 按钮「▶ 运行」｜构造值 fromValue [number] "1" → "0.8"｜改前 • 选择分类后，在左侧输入数值即可实时换算到右侧单位 • 点击中间 ⇅ 按钮可交换两个单位 • 常用换算速查可一键填入常… → 点击后 • 选择分类后，在左侧输入数值即可实时换算到右侧单位 • 点击中间 ⇅ 按钮可交换两个单位 • 常用换算速查可一键填入常…
- `tools/metallurgy/alloy-ratio.html` — 按钮「计算加入量」｜构造值 steelW [number] "0.01" → "0.01"｜改前 总原料加入量 0.000 t ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 总原料加入量 0.000 t ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/music/chord-notes.html` — 按钮「🔍 分析和弦」｜构造值 chordInput [text] "abc 123" → "abc 123x"｜改前 和弦类型标记示例音程（半音）结构 大三和弦C0, 4, 7根-大三-纯五 小三和弦Am0, 3, 7根-小三-纯五 增三… → 点击后 和弦类型标记示例音程（半音）结构 大三和弦C0, 4, 7根-大三-纯五 小三和弦Am0, 3, 7根-小三-纯五 增三…
- `tools/music/music-analysis.html` — 按钮「🎤 开始分析」｜构造值 sample-rate [number] "12" → "9.600000000000001"｜改前 码率: 1411 kbps 每秒: 172.27 KB/s 60秒总大小: 10.09 MB 每小时: 605.62 M… → 点击后 码率: 1411 kbps 每秒: 172.27 KB/s 60秒总大小: 10.09 MB 每小时: 605.62 M…
- `tools/nuclear/pair-annihilation.html` — 按钮「计算」｜构造值 dummy [number] "1" → "0.8"｜改前 511.0每个光子能量 (keV)1022.0总能量 (keV)0.5110每个光子能量 (MeV)1.0220总能量 … → 点击后 511.0每个光子能量 (keV)1022.0总能量 (keV)0.5110每个光子能量 (MeV)1.0220总能量 …
- `tools/pet/fish-tank-volume.html` — 按钮「计算水量」｜构造值 length [number] "2" → "1.6"｜改前 • 过滤器：流量建议为水量的3-5倍/小时 • 加热棒：每升水约需1-2W加热功率 • 增氧泵：小型缸2-5W，大型缸5… → 点击后 • 过滤器：流量建议为水量的3-5倍/小时 • 加热棒：每升水约需1-2W加热功率 • 增氧泵：小型缸2-5W，大型缸5…
- `tools/rental/cycle-11.html` — 按钮「计算结算」｜构造值 number [number] "260" → "208"｜改前 ⏱️ 水电（读数/周期）结算 记录电表、水表、燃气表读数，自动计算用量与费用，支持阶梯电价，生成结算报告。 📐 工作原… → 点击后 ⏱️ 水电（读数/周期）结算 记录电表、水表、燃气表读数，自动计算用量与费用，支持阶梯电价，生成结算报告。 📐 工作原…
- `tools/rheumatology/sapho-syndrome.html` — 按钮「评估诊断」｜构造值 duration [number] "3" → "2.4000000000000004"｜改前 高度提示SAPHO综合征诊断评估中等活动疾病活动度7诊断评分 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 高度提示SAPHO综合征诊断评估中等活动疾病活动度7诊断评分 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/safety/haxijisuan.html` — 按钮「🔐 计算」｜构造值 input [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 ❌ Failed to execute 'digest' on 'SubtleCrypto': Algorithm: U… → 点击后 ❌ Failed to execute 'digest' on 'SubtleCrypto': Algorithm: U…
- `tools/sales/moving-average.html` — 按钮「🔮 预测」｜构造值 window [number] "11" → "8.8"｜改前 📋 复制结果⬇️ 导出 TXT ⏐ 期数实际值移动平均/预测第3期128128第4期142135第5期150140第6… → 点击后 📋 复制结果⬇️ 导出 TXT ⏐ 期数实际值移动平均/预测第3期128128第4期142135第5期150140第6…
- `tools/science/periodic-table.html` — 按钮「搜索 Fe」｜构造值 search [text] "Fe" → "Fex"｜改前 H氢 Hydrogen原子序数 1 · 第1周期 · 第1族 · 非金属原子量1.008电子排布1s¹密度0.0899 … → 点击后 H氢 Hydrogen原子序数 1 · 第1周期 · 第1族 · 非金属原子量1.008电子排布1s¹密度0.0899 …
- `tools/sports/sports-stats.html` — 按钮「跑步周」｜构造值 aMinutes [number] "2" → "1.6"｜改前 2总记录数 ⏐ 720总消耗 kcal ⏐ 70总时长 分钟 ⏐ 12.0总距离 km ⏐ 日期类型时长(min)距离(… → 点击后 2总记录数 ⏐ 720总消耗 kcal ⏐ 70总时长 分钟 ⏐ 12.0总距离 km ⏐ 日期类型时长(min)距离(…
- `tools/stats/regression-analysis.html` — 按钮「🧮 计算」｜构造值 pred-x [number] "11" → "8.8"｜改前 样本数 n10斜率 b1.9867截距 a0.0733相关系数 r0.9994决定系数 R²0.9989剩余标准差 s0… → 点击后 样本数 n10斜率 b1.9867截距 a0.0733相关系数 r0.9994决定系数 R²0.9989剩余标准差 s0…
- `tools/stats/statistical-tests.html` — 按钮「🧮 检验」｜构造值 one-mu [number] "20" → "16"｜改前 样本数 n10样本均值 x̄25.5000样本标准差 s8.6699标准误 SE2.7417假设均值 μ₀20t 统计量… → 点击后 样本数 n10样本均值 x̄25.5000样本标准差 s8.6699标准误 SE2.7417假设均值 μ₀20t 统计量…
- `tools/tcm-chemistry/fingerprint-similarity.html` — 按钮「📋 计算相似度」｜构造值 refData [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 0.9981平均相关系数0.9995平均夹角余弦0.9985最大相关系数0.9974最小相关系数 ⏐ 📋 复制结果⬇️… → 点击后 0.9981平均相关系数0.9995平均夹角余弦0.9985最大相关系数0.9974最小相关系数 ⏐ 📋 复制结果⬇️…
- `tools/tcm-chemistry/structure-identification.html` — 按钮「📊 解析IR数据」｜构造值 irInput [text] "abc 123" → "abc 123x"｜改前 IR数据解析结果输入1个吸收峰，识别出0个特征基团📊 特征峰归属结构特征推断：未识别到明显特征基团解析提示：IR主要用… → 点击后 IR数据解析结果输入1个吸收峰，识别出0个特征基团📊 特征峰归属结构特征推断：未识别到明显特征基团解析提示：IR主要用…
- `tools/text/text-to-ascii-art.html` — 按钮「计算」｜构造值 src [text] "abc 123" → "abc 123x"｜改前 ASCII 艺术字 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ASCII 艺术字 ⏐ 📋 复制结果⬇️ 导出 TXT

### 重置按钮未改变任何输入（31 页）

- `tools/audio/audio-recorder.html` — 「清空全部」｜点击后所有输入值未变化
- `tools/biz/lorem-ipsum-advanced.html` — 「清空」｜点击后所有输入值未变化
- `tools/cleaning/appliance-cycle.html` — 「重置所有记录」｜点击后所有输入值未变化
- `tools/dentistry/sialography.html` — 「清空」｜点击后所有输入值未变化
- `tools/design/image-to-ascii.html` — 「清空」｜点击后所有输入值未变化
- `tools/edu2/wrong-book.html` — 「清空全部」｜点击后所有输入值未变化
- `tools/elderly/fall-risk.html` — 「重置」｜点击后所有输入值未变化
- `tools/elderly/reminder-time.html` — 「🗑️ 清空全部」｜点击后所有输入值未变化
- `tools/finance/password-generator-advanced.html` — 「清空」｜点击后所有输入值未变化
- `tools/food/nutrition-calculator.html` — 「清空本餐」｜点击后所有输入值未变化
- `tools/funeral/ceremony-timeline.html` — 「清空」｜点击后所有输入值未变化
- `tools/general/calc-13.html` — 「🗑️ 重置」｜点击后所有输入值未变化
- `tools/general/calc-14.html` — 「🗑️ 重置」｜点击后所有输入值未变化
- `tools/hematology/aps-diagnosis.html` — 「重置」｜点击后所有输入值未变化
- `tools/hematology/rater-risk-1.html` — 「重置」｜点击后所有输入值未变化
- `tools/home/furniture-layout.html` — 「🧹 清空布局」｜点击后所有输入值未变化
- `tools/hydraulic/cycle-19.html` — 「清空」｜点击后所有输入值未变化
- `tools/it/nanoid-generator.html` — 「清空」｜点击后所有输入值未变化
- `tools/it/random.html` — 「清空」｜点击后所有输入值未变化
- `tools/it/uuid-v7-generator.html` — 「清空」｜点击后所有输入值未变化
- `tools/property/cycle-10.html` — 「清空」｜点击后所有输入值未变化
- `tools/rehabilitation/berg-balance-scale.html` — 「重置」｜点击后所有输入值未变化
- `tools/rehabilitation/flacc-scale.html` — 「重置」｜点击后所有输入值未变化
- `tools/rehabilitation/mmse-scoring.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/bvas.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/rater-16.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/rater-17.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/sledai.html` — 「重置」｜点击后所有输入值未变化
- `tools/safety/reminder-cycle-protection.html` — 「清空全部」｜点击后所有输入值未变化
- `tools/tcm-diagnosis/tongue-diagnosis.html` — 「重置」｜点击后所有输入值未变化
- `tools/transport/calc-4.html` — 「🗑️ 清空选择」｜点击后所有输入值未变化

### 导出/下载按钮 onclick 目标函数不存在（必死）（1 页）

- `tools/it/typescript-compiler.html` — 「⬇ 下载 JS」｜onclick 调用 downloadJs() 但该函数不存在（typeof=false）

### 死控件（静态检测，1 页）

> 仅列「控件 id 在整页脚本中零引用、且页面没有泛化读取控件」的页；如需与运行时交叉验证，见 JSON 的 `deadControlPages`。

- `tools/legal/legal-calculator.html` — lit-type-labor(input/radio)、lit-type-ip(input/radio)

### 低置信度线索：导出/下载未观察到触发（350 页）

> 这些页的导出按钮 onclick 函数存在、点击也不报错，但没观察到带 download 的 `a.click()`；多为结果为空时静默 return，需人工复核，不计入缺陷数。

- `tools/accounting/report-2.html` —「导出明细 CSV」（__report_2Export）
- `tools/acupuncture/acupoint-combination.html` —「导出明细 CSV」（__acupoint_combinationExport）
- `tools/admin/analysis-30.html` —「导出明细 CSV」（__analysis_30Export）
- `tools/admin/detector-time.html` —「⬇️ 导出日程 CSV」
- `tools/admin/version-control.html` —「📤 导出JSON」（exportData）
- `tools/advertising/analysis-27.html` —「导出明细 CSV」（__analysis_27Export）
- `tools/advertising/analysis-55.html` —「导出明细 CSV」（__analysis_55Export）
- `tools/advertising/storyboard-timeline.html` —「导出脚本」（exportScript）
- `tools/agriculture/countdown-cycle.html` —「导出明细 CSV」（__countdown_cycleExport）
- `tools/agriculture/cycle-honey.html` —「📥 导出记录」（exportExtr）
- `tools/ai/ai-10.html` —「导出 CSV」（__b1Export）
- `tools/ai/ai-15.html` —「导出 CSV」（__adExport）
- `tools/ai/ai-16.html` —「导出 CSV」（__aeExport）
- `tools/ai/ai-17.html` —「导出 CSV」（__afExport）
- `tools/ai/ai-5.html` —「导出 CSV」（__a5Export）
- `tools/ai/ai-8.html` —「导出 CSV」（__a8Export）
- `tools/ai/ai-7.html` —「导出 CSV」（__a7Export）
- `tools/ai/ai-9.html` —「导出 CSV」（__a9Export）
- `tools/ai/ai-code-review.html` —「导出 CSV」（__crExport）
- `tools/ai/ai-prompt-generator.html` —「导出 CSV」（__pgExport）
- `tools/ai/ai.html` —「导出 CSV」（__b4Export）
- `tools/ai/attention-head-dim.html` —「导出 CSV」（__ahExport）
- `tools/ai/auc-rank.html` —「导出 CSV」（__arExport）
- `tools/ai/cohens-kappa.html` —「导出 CSV」（__ckExport）
- `tools/ai/context-window.html` —「导出 CSV」（__cwExport）
- `tools/ai/best-epoch.html` —「导出 CSV」（__beExport）
- `tools/ai/cosine-similarity.html` —「导出 CSV」（__csExport）
- `tools/ai/cross-entropy.html` —「导出 CSV」（__ceExport）
- `tools/ai/dropout.html` —「导出 CSV」（__dpExport）
- `tools/ai/elbow-wcss.html` —「导出 CSV」（__ewExport）
- `tools/ai/epoch-time.html` —「导出 CSV」（__etExport）
- `tools/ai/grad-accumulation.html` —「导出 CSV」（__gaExport）
- `tools/ai/inference-throughput.html` —「导出 CSV」（__itExport）
- `tools/ai/k-means.html` —「导出 CSV」（__kmExport）
- `tools/ai/l1-l2-regularization.html` —「导出 CSV」（__l1Export）
- `tools/ai/l1-l2.html` —「导出 CSV」（__l2Export）
- `tools/ai/min-max.html` —「导出 CSV」（__mxExport）
- `tools/ai/model-accuracy.html` —「导出 CSV」（__maExport）
- `tools/ai/precision-recall.html` —「导出 CSV」（__prExport）
- `tools/ai/quantization-ratio.html` —「导出 CSV」（__qrExport）
- `tools/ai/rag.html` —「导出 CSV」（__rgExport）
- `tools/ai/rmse.html` —「导出 CSV」（__rmExport）
- `tools/ai/roc-auc.html` —「导出 CSV」（__raExport）
- `tools/ai/sigmoid.html` —「导出 CSV」（__sgExport）
- `tools/ai/softmax.html` —「导出 CSV」（__smExport）
- `tools/ai/softmax-2.html` —「导出 CSV」（__s2Export）
- `tools/ai/specificity.html` —「导出 CSV」（__spExport）
- `tools/ai/temperature-scaling.html` —「导出 CSV」（__tsExport）
- `tools/ai/steps-per-epoch.html` —「导出 CSV」（__seExport）
- `tools/ai/training-flops.html` —「导出 CSV」（__tfExport）
- `tools/astronomy/convert-17.html` —「导出明细 CSV」（__convert_17Export）
- `tools/audio/audio-cut.html` —「⬇
导出 WAV」（exportSelection）
- `tools/audio/audio-echo.html` —「💾 导出 WAV」（exportWav）
- `tools/audio/audio-recorder.html` —「导出音频」（exportAudio）
- `tools/automotive/fuel-anomaly.html` —「💾 下载结果」
- `tools/beauty/aging-calculator.html` —「⬇️ 导出 TXT」
- `tools/biz/lorem-ipsum-advanced.html` —「导出明细 CSV」（__lorem_ipsum_advancedExport）
- `tools/biz/summary-rater-csat.html` —「导出明细 CSV」（__summary_rater_csatExport）
- `tools/biz/team-roster-generator.html` —「导出明细 CSV」（__team_roster_generatorExport）
- `tools/biz/text-compare.html` —「导出明细 CSV」（__text_compareExport）
- `tools/biz/text-extract-dates.html` —「导出明细 CSV」（__text_extract_datesExport）
- `tools/biz/text-extract-ips.html` —「导出明细 CSV」（__text_extract_ipsExport）
- `tools/cardiology/has-bled.html` —「导出明细 CSV」（__has_bledExport）
- `tools/ceramics/glaze-temp.html` —「⬇️ 导出测温锥对照 CSV」
- `tools/chess/bridge-scoring.html` —「导出明细 CSV」（__bridge_scoringExport）
- `tools/chess/gomoku-forbidden.html` —「导出明细 CSV」（__gomoku_forbiddenExport）
- `tools/cleaning/appliance-cycle.html` —「导出明细 CSV」（__appliance_cycleExport）
- `tools/cleaning/cycle-20.html` —「⬇️ 导出养护排期 CSV」
- `tools/cleaning/staff-schedule.html` —「导出明细 CSV」（__staff_scheduleExport）
- `tools/clinical-lab/hba1c-converter.html` —「导出明细 CSV」（__hba1c_converterExport）
- `tools/clinical-lab/urinalysis-interpretation.html` —「⬇️ 导出 TXT」
- `tools/clinical-nursing/cycle-7.html` —「📥 导出记录」（exportData）
- `tools/clinical-nursing/pressure-injury-description.html` —「导出明细 CSV」（__pressure_injury_descriptionExport）
- `tools/clinical-nursing/reminder-time-1.html` —「📥 导出记录」（exportData）
- `tools/clinical-nursing/suction-pressure.html` —「导出明细 CSV」（__suction_pressureExport）
- `tools/cognition/cognitive-assessment.html` —「⬇️ 导出 TXT」
- `tools/cognition/schulte-table.html` —「⬇️ 导出训练记录 CSV」
- `tools/data/calc-2.html` —「导出明细 CSV」（__calc_2Export）
- `tools/data/csv-analyzer.html` —「制表符导出数据分析」
- `tools/data/csv-json.html` —「导出明细 CSV」（__csv_jsonExport）
- `tools/data/data-cleaner.html` —「导出明细 CSV」（__data_cleanerExport）
- `tools/data/yaml-json.html` —「导出明细 CSV」（__yaml_jsonExport）
- `tools/dentistry/sialography.html` —「导出明细 CSV」（__sialographyExport）
- `tools/dermatology/chilblain-grading.html` —「导出明细 CSV」（__chilblain_gradingExport）
- `tools/dermatology/hdss-hyperhidrosis.html` —「导出明细 CSV」（__hdss_hyperhidrosisExport）
- `tools/dermatology/pityriasis-rosea.html` —「导出明细 CSV」（__pityriasis_roseaExport）
- `tools/design/blueprint-grid.html` —「导出明细 CSV」（__blueprint_gridExport）
- `tools/design/checkerboard-generator.html` —「导出明细 CSV」（__checkerboard_generatorExport）
- `tools/design/dot-pattern.html` —「导出明细 CSV」（__dot_patternExport）
- `tools/design/gradient-from-color.html` —「导出明细 CSV」（__gradient_from_colorExport）
- `tools/design/grid-pattern.html` —「导出明细 CSV」（__grid_patternExport）
- `tools/design/image-cropper.html` —「导出明细 CSV」（__image_cropperExport）
- `tools/design/image-rounded-corners.html` —「⬇ 下载 PNG」（downloadResult）
- `tools/design/image-to-ascii.html` —「下载 .txt」（downloadResult）
- `tools/design/iso-noise-reference.html` —「导出明细 CSV」（__iso_noise_referenceExport）
- `tools/design/loading-dots.html` —「导出明细 CSV」（__loading_dotsExport）
- `tools/design/isometric-grid.html` —「导出明细 CSV」（__isometric_gridExport）
- `tools/design/music-scale-reference.html` —「⬇️ 导出音阶 CSV」（msExportCsv）
- `tools/design/pattern-generator.html` —「导出明细 CSV」（__pattern_generatorExport）
- `tools/design/qr-code-styled.html` —「下载」（downloadImg）
- `tools/design/signature-pad.html` —「⬇ 导出 PNG」（exportPNG）
- `tools/design/spectrum-visualizer.html` —「导出明细 CSV」（__spectrum_visualizerExport）
- `tools/design/spinner-generator.html` —「导出明细 CSV」（__spinner_generatorExport）
- `tools/design/stripe-pattern.html` —「导出明细 CSV」（__stripe_patternExport）
- `tools/design/svg-to-png.html` —「下载 PNG」（downloadPNG）
- `tools/design/tailwind-colors.html` —「⬇️ 导出色板清单 CSV」（__twExport）
- `tools/design/waveform-visualizer.html` —「导出明细 CSV」（__waveform_visualizerExport）
- `tools/ecommerce/cycle-15.html` —「导出数据」（exportData）
- `tools/ecommerce/report.html` —「导出明细 CSV」（__reportExport）
- `tools/edu/24-point-solver.html` —「导出明细 CSV」（__24_point_solverExport）
- `tools/edu/chinese-stroke-counter.html` —「导出明细 CSV」（__chinese_stroke_counterExport）
- `tools/edu/convert-1.html` —「导出明细 CSV」（__convert_1Export）
- `tools/edu/convert-3.html` —「导出明细 CSV」（__convert_3Export）
- `tools/edu/ebbinghaus-curve.html` —「导出明细 CSV」（__ebbinghaus_curveExport）
- `tools/edu/edu-unit-converter.html` —「导出明细 CSV」（__edu_unit_converterExport）
- `tools/edu/exam-gpa-calculator.html` —「⬇️ 导出成绩单 CSV」
- `tools/edu/exam-study-planner.html` —「📤 导出」（exportTasks）
- `tools/edu/pinyin-converter.html` —「导出明细 CSV」（__pinyin_converterExport）
- `tools/edu/reading-speed-calculator.html` —「导出明细 CSV」（__reading_speed_calculatorExport）
- `tools/edu2/wrong-book.html` —「导出明细 CSV」（__wrong_bookExport）
- `tools/elderly/bp-trend.html` —「导出明细 CSV」（__bp_trendExport）
- `tools/elderly/fall-risk.html` —「⬇️ 导出 TXT」
- `tools/elderly/reminder-time.html` —「📥 导出CSV」（exportSchedule）
- `tools/electrical/power-factor-compensation.html` —「导出明细 CSV」（__power_factor_compensationExport）
- `tools/encode/calc-1.html` —「导出明细 CSV」（__calc_1Export）
- `tools/encode/calc-2.html` —「导出明细 CSV」（__calc_2Export）
- `tools/encode/image-to-base64.html` —「下载图片」（downloadImg）
- `tools/endocrinology/cycle-hormone.html` —「⬇️ 导出 TXT」
- `tools/energy/stats-energy.html` —「导出明细 CSV」（__stats_energyExport）
- `tools/ent/adenoid-grading.html` —「导出明细 CSV」（__adenoid_gradingExport）
- `tools/ent/tonsil-grading.html` —「导出明细 CSV」（__tonsil_gradingExport）
- `tools/fengshui/fengshui-calculator.html` —「导出明细 CSV」（__fengshui_calculatorExport）
- `tools/finance/dns-record-info.html` —「⬇️ 导出DNS记录 CSV」
- `tools/finance/gold-price-calculator.html` —「导出明细 CSV」（__gold_price_calculatorExport）
- `tools/finance/housing-fund-loan.html` —「导出明细 CSV」（__housing_fund_loanExport）
- `tools/finance/mortgage-calculator.html` —「↓ 导出结果」
- `tools/finance/number-to-words-chinese.html` —「导出明细 CSV」（__number_to_words_chineseExport）
- `tools/finance/number-to-words.html` —「导出明细 CSV」（__number_to_wordsExport）
- `tools/finance/register-depreciation.html` —「导出数据」（exportAssets）
- `tools/finance/sharpe-ratio.html` —「导出明细 CSV」（__sharpe_ratioExport）
- `tools/finance/tax-calculator.html` —「↓ 导出结果」
- `tools/finance/word-counter.html` —「↓ 导出结果」
- `tools/fishery/cycle-6.html` —「⬇️ 导出清淤计划 CSV」
- `tools/fitness/cycle-5.html` —「⬇️ 导出课程表 CSV」
- `tools/fitness/training-volume.html` —「导出明细 CSV」（__training_volumeExport）
- `tools/food/cooking-converter.html` —「导出明细 CSV」（__cooking_converterExport）
- `tools/food/food-pairing.html` —「导出明细 CSV」（__food_pairingExport）
- `tools/food/nutrition-calculator.html` —「⬇️ 导出营养明细 CSV」（__nutriExport）
- `tools/food/stats-ingredient.html` —「导出明细 CSV」（__stats_ingredientExport）
- `tools/food/stats-simulator-flavor.html` —「导出明细 CSV」（__stats_simulator_flavorExport）
- `tools/fun/1a2b-guess.html` —「⬇️ 导出 TXT」
- `tools/fun/keyboard-heatmap.html` —「导出明细 CSV」（__keyboard_heatmapExport）
- `tools/fun/word-scramble.html` —「导出明细 CSV」（__word_scrambleExport）
- `tools/fun/typing-rhythm.html` —「导出明细 CSV」（__typing_rhythmExport）
- `tools/funeral/funeral-budget-planner.html` —「导出明细 CSV」（__funeral_budget_plannerExport）
- `tools/funeral/reminder-3.html` —「导出明细 CSV」（__reminder_3Export）
- `tools/gardening/pest-identifier.html` —「导出明细 CSV」（__pest_identifierExport）
- `tools/gardening/reminder-cycle-succulent.html` —「导出明细 CSV」（__reminder_cycle_succulentExport）
- `tools/general/convert-21.html` —「导出明细 CSV」（__convert_21Export）
- `tools/geology/analysis-33.html` —「导出明细 CSV」（__analysis_33Export）
- `tools/health/calorie-needs.html` —「导出明细 CSV」（__calorie_needsExport）
- `tools/health/milk-tea-calories.html` —「导出明细 CSV」（__milk_tea_caloriesExport）
- `tools/health/rehab-timer.html` —「导出明细 CSV」（__rehab_timerExport）
- `tools/health/symptom-checker.html` —「导出明细 CSV」（__symptom_checkerExport）
- `tools/hematology/leukemia-classification.html` —「导出明细 CSV」（__leukemia_classificationExport）
- `tools/home/furniture-layout.html` —「📥 导出」（exportLayout）
- `tools/home/renovation-budget.html` —「📥 导出」（exportBudget）
- `tools/hydraulic/cycle-19.html` —「⬇️ 导出维护排程 CSV」
- `tools/image/image-collage.html` —「↓ 导出结果」
- `tools/kids/mirror-letter.html` —「导出明细 CSV」（__mirror_letterExport）
- `tools/kids/multiplication-practice.html` —「导出明细 CSV」（__multiplication_practiceExport）
- `tools/legal/calendar.html` —「导出明细 CSV」（__calendarExport）
- `tools/legal/contract-templates.html` —「⬇️ 导出模板清单 CSV」
- `tools/legal/social-security-base.html` —「⬇️ 导出 TXT」
- `tools/legal/will-template-generator.html` —「下载文本」（downloadWill）
- `tools/legal2/keyword-extract.html` —「导出明细 CSV」（__keyword_extractExport）
- `tools/life/analysis-80.html` —「导出明细 CSV」（__analysis_80Export）
- `tools/life/analysis-cost-9.html` —「导出明细 CSV」（__analysis_cost_9Export）
- `tools/life/color-name-finder.html` —「导出明细 CSV」（__color_name_finderExport）
- `tools/life/countdown-2.html` —「导出明细 CSV」（__countdown_2Export）
- `tools/life/cycle-4.html` —「⬇️ 导出用品清单 CSV」（__supplyExport）
- `tools/life/cycle-pruning-lawn.html` —「⬇️ 导出养护排期 CSV」
- `tools/life/data-unit-converter.html` —「导出明细 CSV」（__data_unit_converterExport）
- `tools/life/drinking-water-plan.html` —「导出明细 CSV」（__drinking_water_planExport）
- `tools/life/timestamp.html` —「导出明细 CSV」（__timestampExport）
- `tools/logistics/analysis-report.html` —「导出明细 CSV」（__analysis_reportExport）
- `tools/logistics/load-calculator.html` —「导出明细 CSV」（__load_calculatorExport）
- `tools/manufacturing/defect-rate.html` —「导出明细 CSV」（__defect_rateExport）
- `tools/marketing/social-media-image-sizes.html` —「📥 导出尺寸表」（exportSizes）
- `tools/math/complex-number.html` —「导出明细 CSV」（__complex_numberExport）
- `tools/medical/reminder-2.html` —「📥 导出CSV」（exportData）
- `tools/medical2/drug-expiry.html` —「导出」（exportData）
- `tools/metalwork/thread-spec.html` —「导出明细 CSV」（__thread_specExport）
- `tools/mining/analysis-cost-3.html` —「⬇️ 导出 TXT」
- `tools/museum/era-comparator.html` —「导出明细 CSV」（__era_comparatorExport）
- `tools/music/music-player.html` —「导出 CSV」
- `tools/music/piano-keyboard.html` —「导出 CSV」
- `tools/nephrology/manager-1.html` —「⬇️ 导出 eGFR 评估 CSV」
- `tools/nutrition/rater-33.html` —「导出明细 CSV」（__rater_33Export）
- `tools/obstetrics/cycle-8.html` —「📥 导出CSV」（exportData）
- …… 其余 150 页见 JSON


## 定向复扫用法

```bash
# 单页复扫
node scripts/runtime_scan.js --interact --only tools/it/whitespace.html --timeout 10000
# 单分类/目录复扫（尾部斜杠=整个目录）
node scripts/runtime_scan.js --interact --only tools/accounting/ --timeout 10000 --concurrency 8
# 通配符 / 多个目标（逗号分隔）
node scripts/runtime_scan.js --interact --only "tools/it/*.html,tools/ai/ai-1*.html"
# 按清单复扫（每行一个相对路径）
node scripts/runtime_scan.js --interact --files /tmp/pages.txt --timeout 10000
```

> 定向复扫会强制重扫命中页，其余记录原样保留，并在结束时自动重算本报告与 JSON；不要与 `--resume` 混用。
> 全量原始数据：`scripts/out/interaction-invalid.jsonl`（逐行、4916 条）与 `scripts/out/interaction-invalid.json`（8 MB），均被 `.gitignore` 忽略，只留本地。
> 精简摘要（401 个高/中置信页）：`plan/interaction-invalid-top100.json`。

### 扫描误报判据（2026-11-05 补充）

空态扫描用「结果区是否含 0 / NaN / 关键词」判定，会把**正常提示语**误判为坏值：提示语里的 `>0`、`≥0`、`≤`、`<` 等符号后紧跟数字 `0` 时，数字规则会命中 `0`，从而误报 `empty_bogus`。本轮已确认 **2 例**：

- `tools/fishery/salinity-calculator.html` — 提示语「现有水量须 >0，三个盐度须 ≥0。未测盐度请勿留空（淡水请明确输入 0）」。
- `tools/mining/convert-grade-ore.html` — 提示语「品位需填写 ≥0 的数值（g/t）；矿石量需填写 ≥0 的数值（t）…」。

补充判据：结果区文本若以 `⚠️` / `请` / `需` / `须` / `请填写` 开头，且**没有独立数值结果**（只有提示语与不等式约束），应先归为「提示语」而非结果；含 `>`、`≥`、`≤`、`<` 的数字不计入 0/NaN 坏值。上述 2 页人工复核后从 `empty_bogus` 待修清单移除。
