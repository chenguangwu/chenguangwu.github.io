# 全站 `|| 默认值` 吞掉合法 0 · 只读扫描（2026-11-05）

> 范围 `tools/**/*.html`，共 4916 个页面文件。**只读**：未改任何页面 / `i18n` / 构建产物，未跑 `_build.py`，未 push。
> 机器可读清单：`scripts/out/number-fallback.json`（摘要版，含全量 T1/T1r/T3、T2 按目录聚合、10 页真机结论）。

## 0. 结论速览

| 项 | 值 |
|---|---|
| 扫描文件 | 4916 |
| 命中 `expr \|\| N`（N≠0） | **1802 处 / 928 页** |
| **T1 真缺陷（直接计算路径）** | **42 处 / 23 页** |
| **T1r 真缺陷（历史/预设回填路径）** | **6 处 / 5 页** |
| T2 语义正确（参数必须 >0） | 1751 处 |
| T3 无影响（`\|\|` 作用在字符串上） | 3 处 / 3 页 |
| 真机抽验 | 10 页，**10/10 复现预判**（准确率 100%） |

已确证四例复核：`agriculture/crop-water-requirement` 的 `days || 1` **仍存在**（仅「复制结果」路径，见 §3.1）；`agriculture/straw-return`（`targetCN || 25`）、`livestock/calving-interval`（`gestation || 283`）、`livestock/poultry-light-program`（日龄 `|| 1`）**已不再命中** —— 对应线已改为空串/`<=0` 显式校验。

## 1. 扫描口径与分档

### 1.1 正则（宽变体，按整段左表达式抓取）

```python
NUM = r'-?\d+(?:\.\d+)?'
pat = re.compile(r'(?P<left>[^;{}\n]{0,180}?)\s*\|\|\s*(?P<dflt>%s)(?![0-9.eE])' % NUM)
```

- 覆盖 `parseFloat(x)||N`、`parseInt(x)||N`、`Number(x)||N`、`num('id')||N`、`getVal(...)||N`、`$('#x').value||N`、`+x||N`、`x = x||N`、`document.getElementById('x').value||N` 及字典/历史记录取值 `d.age||N`。
- 按左侧是否含数值强转（`parseFloat|parseInt|Number|parseNum|toNum` 或一元 `+`）与是否含 `.value` 分 `numeric / string / bare` 三型，再叠加业务语义判档。
- **`|| 0` 一律不命中（有意为之）**：`0 || 0 === 0`、`NaN || 0 === 0`，`||0` 不可能吞掉合法 0，只把非法/空输入回退成 0，属正常兜底。
- **`??` 不在范围内**：`??` 只对 `null/undefined` 生效，不会吞 0，语义本就正确。
- 已知盲区：跨行拼接的表达式、默认值写成变量/常量（`|| DEFAULT`）、模板字符串内嵌表达式、`a?.[k] || N` 以外的动态键。这些量级很小，未纳入统计。

### 1.2 三档定义（含新增的 T1r）

| 档 | 定义 | 处置 |
|---|---|---|
| **T1** | 该参数业务上 **0 是合法值**（天数/次数/面积/用量/比例/评分/单价/0°C/0 岁/0 月龄/零向量/零标量/零荷载），被 `\|\| N` 改成 N，直接改变计算结果、跳过校验或评错级 | 必须修 |
| **T1r** | 同上，但触发点是**历史记录恢复 / 预设回填 / 本地存储读取**：存进去的 0 被读成 N，且随后立即 `calculate()`，结果同 T1 | 建议同批修（改 `??` 或空串判定） |
| **T2** | 该参数业务上**必须 >0**（生成条数、画布边长、分母、样本量、周期、库存数量下限外的尺寸…），兜底只是把空/非法输入当默认示例值 | 不改，登记备查；可补「请输入大于 0 的值」提示 |
| **T3** | `\|\|` 确实作用在**字符串**上（`input.value`），空串才回退，`"0"` 为 truthy 不受影响；页面后续另有数值校验 | 不改 |

> 复核中把预判的 `science/probability-calculator.html:752`（`sigma||1`）**从 T1 降为 T2**：标准差 0 业务上不合法，兜底 1 属「无效输入当默认」，但页面应显式提示而非静默画图。

## 2. 真机抽验（10 页 / 10 命中）

方法：`python3 -m http.server 8137` + puppeteer-core（Chrome 绝对路径），注入 0（或对照非 0 值），读取 `#result`/`.result-box`/`#resultTable` 等真实结果容器。

| # | 页面 | 注入 | 观测 | 预判 |
|---|---|---|---|---|
| 1 | `it/random` | min=-10, max=0, count=3 | 输出 `-0.949595, 54.504079, -8.727387`（出现 >0） | T1 ✅ |
| 2 | `it/vector-magnitude` | 三元全 0 | 同页输出「零向量无单位向量」却又给 α=β=γ=90° | T1 ✅ |
| 3 | `it/random-string` | cnt=0 | `rows=5`（页面自身钳制应得 1） | T1 ✅ |
| 4 | `pediatrics/pediatric-asthma` | age=0 | 渲染 7 题（`age<4` 分支被绕过）；age=3 反为空白 | T1 ✅ |
| 5 | `pediatrics/developmental-milestones` | age=0 | 显示「当前月龄参考标准：18月」 | T1 ✅ |
| 6 | `health/smoking-cost-calculator` | years=0 vs 1 | 两值输出完全相同（¥9,125） | T1 ✅ |
| 7 | `hr/gross-up-calculator` | threshold=0 vs 5000 | 两值输出完全相同（10451.61） | T1 ✅ |
| 8 | `food/dough-fermentation-time` | temp=0 | 显示 25°C「最佳温度区间」 | T1 ✅ |
| 9 | `science/matrix-calculator` | scalar=0 | 输出「k·A = 1·A」，步骤「k = 1」 | T1 ✅ |
| 10 | `sales/conversion-funnel` | 首阶段 0、次阶段 3 | 表格出现「加购→下单 3300.00%」「下单 40000.00%」 | T1 ✅ |

> `agriculture/crop-water-requirement` 未进真机（其 `days||1` 只在 `copyResult()`；主 `calc()` 在 `:289/:294` 已显式拒绝 0 天），按源码路径判定，见 §3.1。

## 3. T1 真缺陷全表（42 处 / 23 页）

### 3.1 直接计算路径（42 处）

| 页面 | 行 | 参数 | 模式 | 证据片段 | 建议处置 |
|---|---|---|---|---|---|
| `agriculture/crop-water-requirement` | 333 | days | `+value\|\|1` | `var days=+document.getElementById('days').value\|\|1;` | **仅复制路径**：`copyResult()` 复用主 `calc()` 的 `days<=0` 拒绝，0 天时提示并中断复制 |
| `construction/pipe-flow` | 303 | temperature | `parseFloat\|\|20` | `var temp = parseFloat(…'temperature'.value) \|\| 20;` | 0°C 合法；改为空串判定，仅空/NaN 回退 20 |
| `food/dough-fermentation-time` | 304 | temp | `parseFloat\|\|25` | `var temp = parseFloat(…'temp'.value) \|\| 25;` | 0°C（冷藏发酵）合法；同上 |
| `health/smoking-cost-calculator` | 428 | years | `parseInt\|\|1` | `const y = parseInt(…'years'.value)\|\|1;` | 0 年合法（戒烟/当年）；空值才用 1 |
| `health/water-intake-calculator` | 411 | age | `parseInt\|\|30` | `const age = parseInt(…'age'.value)\|\|30;` | 0 岁（新生儿）合法；空值才用 30 |
| `hr/gross-up-calculator` | 273 | threshold | `parseFloat\|\|5000` | `const threshold = parseFloat(…'threshold'.value) \|\| 5000;` | 起征点 0 合法；空值才用 5000 |
| `hr/recruitment-funnel` | 320 / 364 | 首阶段 count | `x\|\|1` | `var maxCount = stages[0].count \|\| 1;` | 全 0 阶段时柱宽基准应为 0/不出图，不要用 1 冒充真实值 |
| `hr/recruitment-funnel` | 324 / 368 | 上一阶段 count（分母） | `x\|\|1` | `pct = i===0?100:(stages[i].count/(stages[i-1].count\|\|1)*100);` | 分母 0 时输出「—」/未定义，不可改 1（否则百分比 ×100 爆炸） |
| `it/random-string` | 234 | cnt | 双段 `parseInt(value\|\|'5')\|\|5` | `…if(cnt>50)cnt=50; if(cnt<1)cnt=1;` | **与自身钳制矛盾**：0 应钳到 1，现得 5；去掉第一段 `\|\|5`，空串单独处理 |
| `it/random` | 352 | max | `parseFloat\|\|100` | `const max = parseFloat(…'max'.value) \|\| 100;` | max=0 合法（恒生成 0）；真机已复现变 100 |
| `it/vector-magnitude` | 292 / 293 / 294 | 方向余弦分母 | `m\|\|1` | `Math.acos(v[0]/(m\|\|1))*180/Math.PI` 等 | 零向量模长 0 应判「方向余弦未定义」，不能给 90° |
| `it/vector-magnitude` | 295 ×3 | 方向余弦分母 | `m\|\|1` | `cos α = '+fmt(v[0]/(m\|\|1))+', cos β …` | 同上（与结果区措辞自相矛盾） |
| `legal/personal-injury` | 398 | age（历史回填） | `d.age\|\|35` | `document.getElementById('age').value=d.age\|\|35` | 改 `?? 35`（仅 null/undefined 回退）；0 岁合法 |
| `math/factorial-calc` | 243 | n（几何平均指数） | `n\|\|1` | `[(Math.pow(f,1/(n\|\|1))).toFixed(4), '几何平均…']` | n=0 时 1/0 未定义，应输出「—」并提示，而不是悄悄用 1 |
| `math/function-plotter` | 268 / 269 / 270 / 271 / 272 | 系数 a | `v('p_a')\|\|1` | `a:v('p_a')\|\|1`（linear/quadratic/trig/exp/log 五处） | **系数 a=0 合法**（水平线/零幅/常数项）；改 `Number.isFinite` 判定 |
| `optical/photochromic-lens` | 331 | temp | `parseFloat\|\|25` | `var temp = parseFloat(…'temp'.value) \|\| 25;` | 0°C 合法 |
| `pediatrics/developmental-milestones` | 277 / 307 | age（月龄） | `parseFloat\|\|18` | `var age=parseFloat(…'age'.value)\|\|18;` | 0 月龄（新生儿）合法 |
| `pediatrics/hfmd-course` | 281 | day | `parseFloat\|\|1` | `var day=parseFloat(…'day'.value)\|\|1;` | 发病当天 day=0 合法 |
| `pediatrics/pediatric-asthma` | 268 / 317 | age（岁） | `parseFloat\|\|8` | `var age=parseFloat(…'age'.value)\|\|8;` | 0 岁婴儿合法；已真机复现 0 岁走成人分支 |
| `pediatrics/vanderbilt-adhd` | 298 / 359 | age（岁） | `parseFloat\|\|8` | `var age=parseFloat(…'age'.value)\|\|8;` | 0 岁合法 |
| `rental/calc-commission-1` | 230 | amount（比率分母） | `amount\|\|1` | `fmt(total/(amount\|\|1)*100,2)+'%'` | amount=0 时综合费率应 0/「—」，现被算成 total×100% |
| `sales/conversion-funnel` | 276 | 首阶段 count | `count\|\|1` | `var maxCount = stages[0].count \|\| 1;` | 同 recruitment-funnel |
| `sales/conversion-funnel` | 279 | 上一阶段 count（分母） | `count\|\|1` | `var pct = i===0?100:(stages[i].count/(stages[i-1].count\|\|1)*100);` | 同 recruitment-funnel；真机复现 3300%/40000% |
| `science/matrix-calculator` | 498 / 541 | scalar / p（幂次） | `parseFloat\|\|1` / `parseInt\|\|1` | `const k = parseFloat(…'scalar'.value)\|\|1;`、`const p = parseInt(…'scalar'.value)\|\|1;` | 零标量（零矩阵）、0 次幂（单位矩阵）均合法 |
| `science/vector-calculator` | 377 / 500 | scalar | `parseFloat\|\|1` | `const k = parseFloat(…'scalar'.value)\|\|1;` | 零标量合法 |
| `structural/bearing-pressure` | 291 / 313 | N（单位荷载分母） | `N\|\|1` | `(A/(N\|\|1)).toFixed(4)` | N=0 时单位面积应 ∞/「—」，不能按 1 kN 算 |

### 3.2 历史 / 预设回填路径 T1r（6 处 / 5 页）

| 页面 | 行 | 参数 | 模式 | 证据片段 | 建议处置 |
|---|---|---|---|---|---|
| `legal/ipr-damages` | 419 | punitiveMultiplier | `d.multiplier\|\|1` | `…punitiveMultiplier').value=d.multiplier\|\|1` | 惩罚倍数 0 合法；改 `?? 1` |
| `legal/traffic-accident-compensation` | 458 | age | `d.age\|\|35` | `…'age').value=d.age\|\|35` | 0 岁合法；改 `?? 35` |
| `legal/work-injury-compensation` | 407 | monthlySalary | `d.salary\|\|8000` | `…'monthlySalary').value=d.salary\|\|8000` | 0 工资合法（无业/家庭照护）；改 `?? 8000` |
| `legal/work-injury-compensation` | 407 | avgSalary | `d.avgSalary\|\|8000` | `…'avgSalary').value=d.avgSalary\|\|8000` | 同上 |
| `medical2/drug-expiry` | 383 | fQty（库存数量） | `it.qty\|\|1` | `document.getElementById('fQty').value = it.qty\|\|1;` | 库存 0 合法（已用完），改 `?? 1` |
| `project/manager-cost` | 276 | bac（总预算） | `d.bac\|\|100000` | `document.getElementById('bac').value = d.bac \|\| 100000;` | BAC=0 合法；改 `?? 100000`（注意 `totalDays\|\|90` 属 T2，0 工期非法） |

## 4. T2 语义正确（1751 处，按目录聚合）

命中量最大的 20 个目录（完整 172 个目录的计数与代表行见 JSON `T2_by_dir`）：

| 目录 | 命中 | 页数 | 典型语义 |
|---|---|---|---|
| finance | 88 | 31 | 期数/年限/金额下限、利率分母 |
| design | 80 | 51 | 生成条数、画布边长、动画时长（`min≥1` 或 `Math.max` 已兜底） |
| it | 70 | 38 | 生成数量 / ID 长度 / 周期，step=0 会除零 |
| health | 48 | 16 | 年龄下限、每日次数、剂量分母 |
| sports | 41 | 28 | 回合/组数/人数 |
| edu | 34 | 15 | 题目数量/样本量 |
| music | 32 | 11 | BPM/音符数量/声道数 |
| electromagnetism | 32 | 8 | 电感/电阻作分母，≤0 无定义 |
| biz | 31 | 15 | 生成条数、文字尺寸 |
| science | 31 | 13 | 样本量、标准差、自由度 |
| realestate | 30 | 22 | 面积/年限/套数 |
| fitness | 30 | 10 | 体重/心率/次数 |
| accounting | 28 | 8 | 期数/年限 |
| agriculture | 24 | 12 | 面积/株数（已修的 `targetCN`/`gestation` 三例不再命中） |
| tax | 24 | 10 | 税率分母/年数 |
| dance | 24 | 6 | 拍数/人数 |
| legal | 24 | 15 | 年限/赔偿基数 |
| restaurant | 23 | 8 | 份数/人数 |
| tcm-chemistry | 23 | 10 | 剂量/配比 |
| securities | 22 | 9 | 期数/本金 |
| 其余 152 目录 | 1012 | — | 单页 1–10 处，语义同族（尺寸/数量/分母） |

> T2 不改，但同类可考虑统一提示：空值/非法值走默认时应在结果区标注「已按默认值 N 计算」，避免用户误以为输入被采纳。

## 5. T3 无影响（字符串口径，3 处 / 3 页）

| 页面 | 行 | 参数 | 证据片段 | 说明 |
|---|---|---|---|---|
| `design/stripe-pattern` | 262 | angle | `const angle = document.getElementById('angle').value \|\| 45;` | `"0"` 为 truthy，角度 0° 正常生效；仅空串回退 45 |
| `sales/commission-calculator` | 551 | 区间上限 | `lastCap.value = lastCap.value \|\| 100000;` | 输入框字符串，`"0"` 不回退；0 上限会由后续校验处理 |
| `video/video-speed` | 416 | fps | `…/(document.getElementById('fps').value\|\|30)*1000` | 下拉框取值，无 0 选项；仅空值回退 |

> 另有一批「字典取值 / 音频参数」被初版分到 T3，复核后归回 T2：`MARKER_REF[m]\|\|5.0`、`VENTURI_FLOW[valve]\|\|4`、`defaults[pair]\|\|1.1`（forex 两页）、`o.frequency.value = freq\|\|1000`、`state.targetHours\|\|500`、`w:v('p_w')\|\|1`（function-plotter 三角函数频率）——这些键值/参数本身不允许为 0，属语义正确兜底。

## 6. 修法模板（供各线套用）

```js
// ❌ 吞 0
const days = +document.getElementById('days').value || 1;

// ✅ 只对空/NaN 回退，0 原样保留
const raw = document.getElementById('days').value;
const days = raw.trim() === '' ? 1 : Number(raw);

// ✅ 历史/预设回填：?? 只回退 null/undefined
document.getElementById('age').value = d.age ?? 35;

// ✅ 分母场景：不要造 1，显式说明未定义
const pct = prev > 0 ? (cur / prev * 100) : null;   // 渲染为「—」
```

## 7. 局限与后续

- 静态正则，不做 AST 求值；判定依赖人工业务语义，T2 的 1751 条只做了**目录级语义归纳 + 抽样**，未逐条读函数体。
- 真机只抽 10 页（覆盖 it/pediatrics/health/hr/food/science/sales 七类业务），准确率 10/10；T1r 6 条全为源码路径判定，**未做真机点击验证**（需先产生一条 0 值历史记录再恢复）。
- 建议下一轮：① 按 §3 表逐条修（T1r 与 T1 同批）；② 修完跑一次 `scripts/verify_*_calc.js` 补 0 输入用例；③ 若要重扫，复用 §1 正则 + `scripts/out/number-fallback.json` 的目录聚合做 diff。
