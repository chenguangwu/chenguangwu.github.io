# 全站「NaN 比较恒 false 导致校验被绕过」排查

- 排查时间：2026-11-05
- 范围：`tools/**/*.html` 全部 **4916** 页（内联 `<script>` 静态扫描）+ 40 页真机抽验
- 性质：只读排查，未改任何工具页、未跑 `_build.py`、未 push

## 一、结论先看

| 口径 | 页数 |
|---|---|
| 含「互斥边界判断对」（`x<min \|\| x>max` / `x>=min && x<=max` 等，同一变量） | **375** |
| 其中已有变量级 `isFinite/isNaN/Number.isInteger` 守卫 | **187**（已防护） |
| 其中走 `parseFloat(...) \|\| 0` / `?? 0` 兜底（NaN 在比较前已被转成 0） | **117** |
| 其中**无守卫、无兜底**的真候选（本次定义的「NaN 可绕过」） | **81** |

真机抽验 40 页（34 页取得有效结果）：**真缺陷 8 / 无后果 9 / 已防护 13 / 其余 10 页探针未定位或无有效证据**。

**关键结论：经典「`NaN < min` 恒 false 放行」在 81 个静态候选里实际只命中 1 页（约 7%），而 117 页的 `|| 0` 静默兜底桶才是真风险——抽验 17 页中 7 页给出可观察的错误结论（41%）。**

原因：大量页面在变量级没有 `isFinite`，但下游函数里有自己的空值/范围提示（`请输入有效数值`、`请填写…`），静态规则看不到。真正危险的是 `parseFloat(v) || 0`：非法输入被静默改写成 0，随后所有范围校验都「合法通过」，页面照常输出结论。

## 二、静态判定口径

1. **成对边界**：同一变量同时出现在上下界两侧，如 `if(x<2 || x>len)`、`if(x>=0 && x<=100)`。
2. **变量来源**：`parseFloat / parseInt / Number / 一元 + / .value` 直取。
3. **已防护**：同一脚本内存在 `isFinite(x)` / `Number.isFinite(x)` / `isNaN(x)` / `Number.isInteger(x)` 等以该变量为参数的守卫。
4. **兜底桶**：赋值右侧出现 `||` 或 `??`（`parseFloat(x) || 0`、`+v || 0`），NaN 在进入比较前已变 0，不属经典绕过，但属「静默 0」风险。
5. **整数索引**：额外检测 `new Array(v)` / `Array(v)` / `v.repeat(`，全站命中均为 0（未发现 `Array(NaN)` 类崩溃）。

## 三、真机抽验设计

- 逐页独立启动 Chrome（避免 session closed），注入 `abc`（主）/ 空串（辅），派发 `input` + `change`，点击主按钮，比较结果区前后文本。
- 判定信号：`pageerror` / console error / `alert`；结果区出现 `NaN`、`—`、`0.00`、`Array(NaN)`、`Invalid array length`；或**结论未变但输入已被清空/改写**。
- 探针失败页（静态推断的输入框 id 与实际不符）单列为 `probe_failed`，不计入准确率分母。

## 四、三档明细（40 页）

### 4.1 真缺陷（8 页，可观察后果）

| # | 页面 | 变量来源 / 模式 | 注入 | 真机现象 | 建议 |
|---|---|---|---|---|---|
| 1 | `tools/finance/car-loan-calculator.html` | `downPct = parseFloat(...) \|\| 0`；`if(downPct<0 \|\| downPct>100)` | `abc` | 首付金额 45,000.00 → **0.00 元**，购置税/保险/月供照常给出，无任何提示 | 在 `\|\| 0` 前先判 `isFinite`，非法值给「请输入 0–100 的首付比例」并清空结果 |
| 2 | `tools/agriculture/dli-calculator.html` | `lightPPFD = +value \|\| 0`；`lightPPFD<0` 校验 | `abc` | 补光 DLI 由数值变 **0.0**，总 DLI 仍 17.3，页面继续给「光照达标」类结论 | 同上；补光参与判定时必须区分「未填」与「填错」 |
| 3 | `tools/ent/tympanometry.html` | `tpp = +value \|\| 0`；`tpp>=-100 && tpp<=100` 分支 | `abc` | 峰压显示 **0 dPa**，仍判 **A 型正常型**，并给临床建议 | 峰压为空/非法时应要求填写，不得默认 0（0 dPa 是正常值） |
| 4 | `tools/agriculture/dry-matter-conversion.html` | `moisture = +value \|\| 0` | `abc` | 干物质 25.00 → **100.00 kg**、含水率 75% → **0.0%**，无提示 | 含水率缺失时拒绝计算（100% 干物质是边界伪结果） |
| 5 | `tools/ai/ai-15.html` | `prior = +value \|\| 0`；`prior>0 && prior<1` | `abc` | P(B) 0.059 → **0.050**，后验概率 16.1017% → **0.0000%**，阳性预测值 0.00%，仍给完整结论 | 先验非法时提示并停止输出 |
| 6 | `tools/energy/water-tds-evaluator.html` | `tds = parseFloat(...) \|\| 0` | `abc` | 水质判定从「城市自来水（合格）」变为 **「直饮水级 / 无需处理」** | TDS 缺失时不得套用 0（0 会落到最高等级） |
| 7 | `tools/electrical/calc-2.html` | `pf = parseFloat(...) \|\| 0`；`pf<0 \|\| pf>1` | `abc` | 有功功率 27.973 → **0.000 kW**，无功/视在功率不变，结果自相矛盾 | 同上 |
| 8 | `tools/chemistry/lifespan-24.html` | `conc = parseFloat(...)`，无兜底、无 `isFinite` | `abc` | 抛 `TypeError: Cannot read properties of undefined (reading 'text')`，结果区**沿用旧结论**（127 天、低风险），用户看不到出错 | 加输入校验 + try/catch，异常时清空结果而非保留旧值 |

> 第 8 条属「异常未处理」，与前 7 条「静默 0」成因不同，但同属本次注入可触发的真实缺陷。

### 4.2 无后果（9 页，NaN 被后续兜底或变量未参与判定）

| 页面 | 现象 |
|---|---|
`tools/film/editing-timecode.html` | `fps` 非数值 → 总帧数/秒/毫秒全部显示 `—`（有统一 NaN→`—` 兜底），仅缺显式提示
`tools/data/xml-html-css-geshihua-yiyou-kebuchong.html` | 缩进输入非法 → 输出完全不变（`parseInt` 后另有默认值）
`tools/endocrinology/short-stature-prediction.html` | `boneAge=abc` → 输出逐字不变
`tools/fengshui/zodiac-lookup.html` | `birthYear=abc` → 输出逐字不变
`tools/endocrinology/frax-score.html` | `age=abc` → 骨折概率/风险分级结论不变
`tools/electronics/smt-stencil.html` | 注入后结果区无变化（变量未进入主计算）
`tools/chemical/reaction-yield.html` | 结果区逐字不变
`tools/agriculture/assessor-1.html` | 结果区逐字不变
`tools/design/css-grid-generator.html` | 非数值控件，注入无影响

### 4.3 已防护（13 页，有显式校验/提示/alert）

| 页面 | 防护表现 |
|---|---|
`tools/accessibility/ramp-slope.html` | 「请输入有效数值」
`tools/chess/bridge-scoring.html` | 「请检查输入：定约级别需为 1–7 的整数…」
`tools/clinical-lab/convert-glucose-1.html` | 「⚠️ 请输入有效 HbA1c（3–20%）…结果已清空」
`tools/cosmetic-derm/rf-tightening.html` | 「请填写「真皮层目标温度 (°C)」后再计算」
`tools/edu/calc-4.html` | 「请输入有效的成绩、权重和考核项数」
`tools/electrical/power-factor-compensation.html` | 「请输入有效参数（功率因数 0~1）」
`tools/electrical/voltage-drop.html` | 「请输入有效参数」
`tools/agriculture/irrigation-calculator.html` | 「土壤适宜含水量下限须在 30–100% 之间」
`tools/agriculture/harvest-loss-rate.html` | 「实际产量必须大于0」
`tools/cardiology/echo-report.html` | 参数非法时显示「未检测」并降级分级，不硬套结论
`tools/finance/tax-bracket.html` | 「请输入正数」
`tools/it/rail-fence-cipher.html` | alert「深度必须在 2 到文本长度之间」（本次问题的原始实证页，已防护）
`tools/ai/cross-entropy.html` | 「⚠ 部分结果无定义（分母为 0 或输入为空），请检查输入」

### 4.4 探针未定位 / 无有效证据（10 页）

`tools/biz/text-extract-ips.html`、`tools/construction/detector-131.html`、`tools/agriculture/machinery-efficiency.html`、`tools/chemical/detector-composition.html`（未定位输入框）；
`tools/dyeing/color-diff.html`、`tools/ecommerce/analysis-70.html`（静态映射到的控件不是参与校验的那个 `pu`/`ref`）；
`tools/agriculture/cycle-honey.html`、`tools/beauty/aging-calculator.html`、`tools/edu/number-memory.html`、`tools/finance/loan-amortization.html`（结果区为空或未渲染，无法判定）。

## 五、静态规则精度评估

| 桶 | 抽验有效页 | 真缺陷 | 命中率 |
|---|---|---|---|
| 真候选（无守卫无兜底，81 页） | 15 | 1（lifespan-24） | **6.7%** |
| `\|\| 0` 兜底桶（117 页） | 17 | 7（car-loan、dli、tympanometry、dry-matter、ai-15、water-tds、calc-2） | **41%** |

结论：
- 「无 `isFinite` + 成对边界」这个静态判据**召回尚可、精度很低**——大量页面下游有自己的空值提示，静态规则看不到；按这个清单逐页改 JS 性价比低。
- 应优先按**兜底桶**修：`parseFloat/parseInt/+value || 0` 共 117 页，属于「非法输入被静默改成合法的 0」，且抽验近半有可观察后果。
- 81 个候选里，真缺陷通常伴随「0 恰好在合法域内」的语义（如峰压 0 dPa、TDS 0、含水率 0%），可按「默认值是否落在正常区间」二次排序，进一步收窄。

## 六、修复建议（按优先级）

1. **P0 兜底桶**：117 页中凡「输入值 0 落在合法区间且代表正常/最优」的变量（峰压、TDS、含水率、先验概率、功率因数、首付比例），去掉 `|| 0`，改为显式 `isFinite` 校验 + 提示 + 清空结果。
2. **P1 异常兜底**：`chemistry/lifespan-24.html` 类，页面抛异常后仍保留旧结论，需 catch 后清空并提示。
3. **P2 候选桶**：81 页按「0 是否落在正常区间」人工过一遍，只改语义敏感的；其余仅补 `isFinite` 即可，不必重排逻辑。
4. **通用写法**（可直接复用到各修复线）：

```js
const raw = el.value.trim();
const v = Number(raw);
if (raw === '' || !Number.isFinite(v) || v < MIN || v > MAX) {
  setResult('请输入有效的 …（范围 MIN–MAX）');
  return;
}
```

> 注意：`parseFloat(...) || 0` 的错误写法不能靠「再加一个 `v < MIN || v > MAX`」修好——`NaN || 0` 已经变成 0，范围判断永远通过。必须先判断原始字符串/`isFinite`。

## 七、复现与产物

- 静态扫描（临时脚本，逻辑未入库）：`node /tmp/nan_scan.js` → `/tmp/nan-static.json`
- 真机抽验：`node /tmp/nan-auto2.js`（候选桶 18 页）、`node /tmp/nan-auto3.js`（兜底桶 12 页）；需先起本地服务 `python3 -m http.server 8137 --directory <项目根>`
- 全量摘要（含 81 候选 / 117 兜底 / 40 页三档明细）：本地 `scripts/out/nan-bypass.json`（被 `.gitignore` 忽略，不进 git）
- 精简摘要（入库）：`plan/nan-bypass-summary.json`

## 八、局限

- 抽验只覆盖 40/4916 页，且以「结果区文本变化」为主要信号，canvas 绘图类页面的 NaN 不可见。
- 静态脚本按「第一个赋值语句」推断变量来源，无法处理跨函数传参（如 `calc(x)` 内部再解析），因此 `probe_failed` 的 6 页不代表页面无缺陷。
- 工作区有其它修复线的未提交改动，抽验反映的是**当前工作区**状态；线上版本可能已有差异。
