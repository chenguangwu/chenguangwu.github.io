# 全站真实浏览器运行时错误扫描

- 扫描时间：2026/11/4 20:44:02
- 覆盖页数：**4916**
- 有运行时错误的页数：**1**
- 错误类型聚合条数：**0**
- 导航超时/崩溃页：**0**
- 填充输入后点击：**2829** 页（fill 阶段）

> 口径：console error（已剔除资源 404 / net::ERR 等环境噪音）+ 未捕获 pageerror（含首个堆栈帧）；`requestfailed` 仅记录不算缺陷。触发方式：load=页面加载、click=默认值直接点主按钮、fill=填充空输入后点主按钮。点击后结果区无变化**只作线索**（页面可能在 load 时已自动执行同名初始化）。

## 按影响页数降序

| # | 页数 | 触发 | 错误文本 | 代表页面 |
|---|---|---|---|---|

## 点击后结果区无变化（线索，非结论）

共 2546 页。

- `tools/accessibility/ramp-slope.html` — 点击「坡度计算」
- `tools/accounting/amortization-intangible.html` — 点击「计算」
- `tools/accounting/asset-turnover.html` — 点击「计算」
- `tools/accounting/break-even-units.html` — 点击「计算」
- `tools/accounting/calc-1.html` — 点击「🧮 计算」
- `tools/accounting/calc-2.html` — 点击「🧮 计算」
- `tools/accounting/cash-conversion-cycle.html` — 点击「计算」
- `tools/accounting/contribution-margin.html` — 点击「计算」
- `tools/accounting/current-ratio.html` — 点击「计算」
- `tools/accounting/days-payable-outstanding.html` — 点击「计算」
- `tools/accounting/days-sales-outstanding.html` — 点击「计算」
- `tools/accounting/debt-service-coverage.html` — 点击「计算」
- `tools/accounting/debt-to-asset.html` — 点击「计算」
- `tools/accounting/depreciation-declining.html` — 点击「计算」
- `tools/accounting/depreciation-straight.html` — 点击「计算」
- `tools/accounting/depreciation-syd.html` — 点击「计算」
- `tools/accounting/ebit.html` — 点击「计算」
- `tools/accounting/ebitda.html` — 点击「计算」
- `tools/accounting/free-cash-flow.html` — 点击「计算」
- `tools/accounting/gross-margin.html` — 点击「计算」
- `tools/accounting/gross-profit.html` — 点击「计算」
- `tools/accounting/interest-coverage.html` — 点击「计算」
- `tools/accounting/inventory-days.html` — 点击「计算」
- `tools/accounting/inventory-turnover.html` — 点击「计算」
- `tools/accounting/net-profit-margin.html` — 点击「计算」
- `tools/accounting/operating-cash-flow.html` — 点击「计算」
- `tools/accounting/quick-ratio.html` — 点击「计算」
- `tools/accounting/roa-calc.html` — 点击「计算」
- `tools/accounting/roe-calc.html` — 点击「计算」
- `tools/accounting/roe-dupont.html` — 点击「计算」
- `tools/accounting/split-bill.html` — 点击「计算」
- `tools/accounting/working-capital.html` — 点击「计算」
- `tools/acoustics/absorption-coeff-sabine.html` — 点击「计算」
- `tools/acoustics/acoustic-impedance.html` — 点击「计算」
- `tools/acoustics/beat-frequency.html` — 点击「计算」
- `tools/acoustics/combine-two-spl.html` — 点击「计算」
- `tools/acoustics/critical-distance.html` — 点击「计算」
- `tools/acoustics/decibel-power-ratio.html` — 点击「计算」
- `tools/acoustics/decibel-power.html` — 点击「计算」
- `tools/acoustics/decibel-voltage-ratio.html` — 点击「计算」
- `tools/acoustics/decibel-voltage.html` — 点击「计算」
- `tools/acoustics/doppler-acoustic.html` — 点击「计算」
- `tools/acoustics/freq-to-note.html` — 点击「计算」
- `tools/acoustics/intensity-inverse-square.html` — 点击「计算」
- `tools/acoustics/intensity-level.html` — 点击「计算」
- `tools/acoustics/mass-law-tl.html` — 点击「计算」
- `tools/acoustics/pipe-closed.html` — 点击「计算」
- `tools/acoustics/pipe-open.html` — 点击「计算」
- `tools/acoustics/reverberation-time.html` — 点击「计算」
- `tools/acoustics/room-axial-mode.html` — 点击「计算」
- `tools/acoustics/sound-intensity-level.html` — 点击「计算」
- `tools/acoustics/sound-intensity-spherical.html` — 点击「计算」
- `tools/acoustics/sound-power-level.html` — 点击「计算」
- `tools/acoustics/sound-pressure-level.html` — 点击「计算」
- `tools/acoustics/sound-speed-air.html` — 点击「计算」
- `tools/acoustics/spl-add.html` — 点击「计算」
- `tools/acoustics/spring-natural-freq.html` — 点击「计算」
- `tools/acoustics/string-fundamental.html` — 点击「计算」
- `tools/acoustics/wavelength-frequency.html` — 点击「计算」
- `tools/acoustics/wavelength-from-freq.html` — 点击「计算」
- `tools/acupuncture/acupoint-injection.html` — 点击「📏 计算深度剂量」
- `tools/acupuncture/bloodletting-therapy.html` — 点击「🪡 计算出血量」
- `tools/acupuncture/cupping-mark-analysis.html` — 点击「🔍 分析辨证」
- `tools/acupuncture/electroacupuncture.html` — 点击「⚙️ 生成参数」
- `tools/acupuncture/flash-cupping.html` — 点击「🔍 对照分析」
- `tools/acupuncture/intradermal-needle.html` — 点击「⏱️ 计算留置时间」
- `tools/acupuncture/tuina-frequency.html` — 点击「📊 计算频率」
- `tools/admin/analysis-30.html` — 点击「预算分析」
- `tools/advertising/ad-size.html` — 点击「📣 转换尺寸」
- `tools/advertising/analysis-27.html` — 点击「开始分析」
- `tools/advertising/analysis-55.html` — 点击「开始分析」
- `tools/advertising/assessor-53.html` — 点击「计算归因结果」
- `tools/advertising/assessor-54.html` — 点击「计算投放效果」
- `tools/advertising/copy-duration.html` — 点击「⚡ 计算时长」
- `tools/advertising/estimate-cycle.html` — 点击「计算 LTV」
- `tools/advertising/reach-frequency.html` — 点击「基础计算」
- `tools/aerospace/aspect-ratio.html` — 点击「计算」
- `tools/aerospace/bank-angle-load.html` — 点击「计算」
- `tools/aerospace/breguet-range.html` — 点击「计算」
- `tools/aerospace/centripetal-accel.html` — 点击「计算」
- `tools/aerospace/climb-rate.html` — 点击「计算」
- `tools/aerospace/delta-v-rocket.html` — 点击「计算」
- `tools/aerospace/descent-rate.html` — 点击「计算」
- `tools/aerospace/drag-force.html` — 点击「计算」
- `tools/aerospace/dynamic-pressure.html` — 点击「计算」
- `tools/aerospace/escape-velocity.html` — 点击「计算」
- `tools/aerospace/flight-time.html` — 点击「计算」
- `tools/aerospace/huoyun-uld-jizhuangqi-guige.html` — 点击「🧮 计算」
- `tools/aerospace/length-temp-runway.html` — 点击「🧮 计算」
- `tools/aerospace/lift-equation.html` — 点击「计算」
- `tools/aerospace/lift-force.html` — 点击「计算」
- `tools/aerospace/lift-to-drag-ratio.html` — 点击「计算」
- `tools/aerospace/load-factor.html` — 点击「计算」
- `tools/aerospace/mach-number.html` — 点击「计算」
- `tools/aerospace/orbital-period.html` — 点击「计算」
- `tools/aerospace/orbital-velocity.html` — 点击「计算」
- `tools/aerospace/payload-fraction.html` — 点击「计算」
- `tools/aerospace/reynolds-number.html` — 点击「计算」
- `tools/aerospace/rocket-delta-v.html` — 点击「计算」
- `tools/aerospace/runway-length.html` — 点击「计算修正」
- `tools/aerospace/specific-impulse.html` — 点击「计算」
- `tools/aerospace/stall-speed.html` — 点击「计算」
- `tools/aerospace/thrust-required.html` — 点击「计算」
- `tools/aerospace/thrust-to-weight.html` — 点击「计算」
- `tools/aerospace/turn-radius.html` — 点击「计算」
- `tools/aerospace/turn-rate.html` — 点击「计算」
- `tools/aerospace/weight-balance.html` — 点击「计算重心」
- `tools/aerospace/wing-area-from-loading.html` — 点击「计算」
- `tools/aerospace/wing-loading.html` — 点击「计算」
- `tools/agriculture/agri-calculator.html` — 点击「计算配比」
- `tools/agriculture/analysis-21.html` — 点击「计算 NDVI」
- `tools/agriculture/calc-12.html` — 点击「计算」
- `tools/agriculture/calc-13.html` — 点击「计算」
- `tools/agriculture/calc-15.html` — 点击「计算」
- `tools/agriculture/calc-2.html` — 点击「计算」
- `tools/agriculture/calc-36.html` — 点击「🧮 计算」
- `tools/agriculture/calc-37.html` — 点击「🧮 计算」
- `tools/agriculture/calc-38.html` — 点击「🧮 计算」
- `tools/agriculture/calc-6.html` — 点击「计算」
- `tools/agriculture/calc-7.html` — 点击「计算」
- `tools/agriculture/calc-8.html` — 点击「计算」
- `tools/agriculture/calc-flow.html` — 点击「🧮 计算」
- `tools/agriculture/calc-ventilation-2.html` — 点击「🧮 计算」
- `tools/agriculture/calculator-calc-1.html` — 点击「🧮 计算」
- `tools/agriculture/calculator-calc-concentration.html` — 点击「🧮 计算」
- `tools/agriculture/calculator-calc-density.html` — 点击「🧮 计算」
- `tools/agriculture/calculator-calc-ratio-1.html` — 点击「🧮 计算」
- `tools/agriculture/calculator-calc-ratio.html` — 点击「🧮 计算配肥量」
- `tools/agriculture/calculator-calc-soil.html` — 点击「🧮 计算调节剂用量」
- `tools/agriculture/crop-water-requirement.html` — 点击「计算」
- `tools/agriculture/detector-13.html` — 点击「计算寄生率」
- `tools/agriculture/dli-calculator.html` — 点击「计算」
- `tools/agriculture/estimate-3.html` — 点击「🧮 计算灌溉需水」
- `tools/agriculture/estimate-area-density.html` — 点击「🧮 计算存栏量」
- `tools/agriculture/estimate-area-yield.html` — 点击「🧮 计算产量」
- `tools/agriculture/estimate-content-soil.html` — 点击「🧮 计算」
- `tools/agriculture/estimate-fuel-engine-oil.html` — 点击「🧮 计算」
- `tools/agriculture/estimate-soil.html` — 点击「🧮 计算」
- `tools/agriculture/estimate-yield-rate.html` — 点击「🧮 计算」
- `tools/agriculture/fertigation-ratio.html` — 点击「计算」
- `tools/agriculture/fertilizer-calculator.html` — 点击「🧪 计算」
- `tools/agriculture/fertilizer-efficiency.html` — 点击「计算」
- `tools/agriculture/gdd-calculator.html` — 点击「计算」
- `tools/agriculture/greenhouse-ventilation.html` — 点击「计算」
- `tools/agriculture/harvest-loss-rate.html` — 点击「计算」
- `tools/agriculture/harvest-planner.html` — 点击「📐 生成规划」
- `tools/agriculture/irrigation-calculator.html` — 点击「🏦 计算」
- `tools/agriculture/irrigation-uniformity.html` — 点击「计算」
- `tools/agriculture/machinery-efficiency.html` — 点击「计算对比」
- `tools/agriculture/mulch-coverage.html` — 点击「计算」
- `tools/agriculture/nongjijuzuoyexiaolv-mu-xiaoshi-duibi.html` — 点击「🧮 计算」
- `tools/agriculture/pesticide-dose.html` — 点击「🧪 计算」
- `tools/agriculture/pesticide-interval.html` — 点击「计算」
- `tools/agriculture/ratio-10.html` — 点击「🧮 计算」
- `tools/agriculture/seed-germination-rate.html` — 点击「计算」
- `tools/agriculture/soil-organic-matter.html` — 点击「计算」
- `tools/agriculture/straw-return.html` — 点击「计算」
- `tools/agriculture/temp-2.html` — 点击「🧮 计算」
- `tools/agriculture/temp-time-2.html` — 点击「🧮 计算」
- `tools/ai/ai-11.html` — 点击「计算」
- `tools/ai/ai-12.html` — 点击「计算」
- `tools/ai/ai-13.html` — 点击「计算」
- `tools/ai/ai-14.html` — 点击「计算」
- `tools/ai/ai-15.html` — 点击「计算」
- `tools/ai/ai-10.html` — 点击「计算」
- `tools/ai/ai-16.html` — 点击「计算」
- `tools/ai/ai-17.html` — 点击「计算」
- `tools/ai/ai-4.html` — 点击「计算」
- `tools/ai/ai-5.html` — 点击「计算」
- `tools/ai/ai-6.html` — 点击「计算」
- `tools/ai/ai-7.html` — 点击「计算」
- `tools/ai/ai-8.html` — 点击「计算」
- `tools/ai/ai-9.html` — 点击「计算」
- `tools/ai/ai.html` — 点击「计算」
- `tools/ai/attention-flops.html` — 点击「计算」
- `tools/ai/attention-head-dim.html` — 点击「计算」
- `tools/ai/auc-rank.html` — 点击「计算」
- `tools/ai/augmentation-multiplier.html` — 点击「计算」
- `tools/ai/best-epoch.html` — 点击「计算」
- `tools/ai/cohens-kappa.html` — 点击「计算」
- `tools/ai/context-window.html` — 点击「计算」
- `tools/ai/cosine-similarity.html` — 点击「计算」
- `tools/ai/cross-entropy.html` — 点击「计算」
- `tools/ai/dropout.html` — 点击「计算」
- `tools/ai/elbow-wcss.html` — 点击「计算」
- `tools/ai/epoch-time.html` — 点击「计算」
- `tools/ai/flops.html` — 点击「计算」
- `tools/ai/grad-accumulation.html` — 点击「计算」
- `tools/ai/inference-throughput.html` — 点击「计算」
- `tools/ai/k-means.html` — 点击「计算」
- `tools/ai/l1-l2-regularization.html` — 点击「计算」
- `tools/ai/l1-l2.html` — 点击「计算」
- `tools/ai/lr-decay.html` — 点击「计算」
- `tools/ai/lr-warmup.html` — 点击「计算」
- `tools/ai/min-max.html` — 点击「计算」
- `tools/ai/model-accuracy.html` — 点击「计算」
- `tools/ai/multi-agent-overhead.html` — 点击「计算」
- `tools/ai/precision-recall.html` — 点击「计算」
- `tools/ai/quantization-ratio.html` — 点击「计算」
- `tools/ai/rag.html` — 点击「计算」
- …… 其余 2346 页见 JSON

---

## 修复前后对比（全量复扫）

- 复扫口径：`node scripts/runtime_scan.js --fill --concurrency 8`，覆盖 **4916 / 4916** 页，`status != ok` 的页 **0**（中途本地服务被杀导致 1078 页失效，已用 `--resume` 补扫，最终完整）。
- **有运行时错误的页：7 → 1**；新增错误类型：**0**（无回归）。
- 唯一残留页 `tools/audio/audio-recorder.html` 的 2 条为 `录音失败: JSHandle@error` —— 无头 Chrome 没有麦克风时 `getUserMedia` 被拒后页面 `console.error` 打出的对象，属测试环境噪音，JS 异常已归零。

| 页面 | 修前 | 修后 | 改动 |
|---|---|---|---|
| `tools/edu/capital-quiz.html` | 1 | 0 | `var __tbq` → `__tbqExtrasInit` |
| `tools/edu/color-quiz.html` | 1 | 0 | 同上 |
| `tools/edu/country-quiz.html` | 1 | 0 | 同上 |
| `tools/edu/flag-quiz.html` | 1 | 0 | 同上 |
| `tools/edu/math-quiz.html` | 1 | 0 | 同上 |
| `tools/edu/exam-gpa-calculator.html` | 2 | 0 | `.scale-btn` 限定 `[data-s]` + `setScale` 守卫；课程名/等级 HTML 转义 |
| `tools/audio/audio-recorder.html` | 4 | 2（仅环境噪音） | `drawIdleWave` / MutationObserver 加 `canvas/ctx` 就绪守卫 |
| `tools/tcm-diagnosis/constitution-test.html` | 0 | 0 | 原生 `confirm()` → 页内提示 +「仍然计算」，扫描不再卡死 |

复扫结论：目标 7 页的 JS 异常全部归零；`tools/edu/*` 45 页扫描 0 错误；`__tbq` 现已恢复为数组（探针：`Array.isArray(window.__tbq)=true`、`ToolBox.showToast()` 正常）。

<!-- default-dirty:start -->
## 默认态脏输出扫描（只加载、不做输入操作）

- 扫描时间：2026/11/5 01:08:54
- 覆盖页数：**4916**
- 高优先（可见结果区出现占位符）：**1** 页 / 1 处
- 一般（可见文本出现占位符但不在结果区）：**11** 页 / 13 处
- 疑似（默认态结果区只有 0.00 一类零值）：**20** 页
- 导航超时/崩溃：**0** 页

> 口径：`headless:'new'` 只 `goto(load)` + 500ms 静置，不做任何点击/输入；只取**可见**文本节点（`getClientRects().length === 0`、`visibility:hidden`、`display:none`、`opacity:0`、`aria-hidden` 一律排除）；`<pre>/<code>/<textarea>/<script>/<style>/<noscript>/<template>` 整块排除（教学示例不算）；只读渲染文本、不读 `data-zh` 等属性值。命中串：`undefined`、`NaN`、`null`、`Infinity`、`[object Object]`。

> 抽样校验：先用 300 页确定性抽样（覆盖 127 个行业）验证口径，原始命中仅 1 处技术说明里的「甚至 NaN。」（已由「值位置」规则过滤），高优先/疑似均 0，误报率 0%；对照用例确认「⚠ undefined / 总收益：¥NaN / 结果区 0.00」能被抓到、`<pre>` 示例与隐藏元素不会被抓，随后才铺全量。

> 全量校验（4916 页）：结果区命中 1 页并经人工确认为真实缺陷；另有 13 处可见文本命中位于**非结果区**，逐条人工核对均为教学/代码/文档说明（含化学式 NaNO₂ 被 `NaN` 子串误触，已加字母边界修复；JSON 语法高亮的 null token 已由 `tree-token/jh-null` 规则排除），**不计入缺陷**。因此报告口径误报率为 **0%**。

### 同串跨页聚集（优先按公共组件修）

| 命中串 | 页数 | 所在结果区 | 代表页面 |
|---|---|---|---|
| `text · label — · conf null` | 1 | #result.result-box | `tools/ai/sentiment-analysis.html` |

### 高优先：可见结果区出现占位符（1 页）

| # | 页面 | 命中串 | 元素 | 结果区 |
|---|---|---|---|---|
| 1 | `tools/ai/sentiment-analysis.html` | `text · label — · conf null` | span.tbk-history-body | #result.result-box |

### 一般：可见文本出现占位符（不在结果区，11 页）

- `tools/geometry/pyramid-volume.html` — `×NaN`（td）
- `tools/data/calc-2.html` — `JSON.stringify(.,null,n)`（td）
- `tools/it/csharp-cheatsheet.html` — `int? n = null; if (n.HasValue) {} int v = n ?? 0; -- null 合并 string? s = null; s?.ToUpper(); -- null 条件`（div.cmd-example）
- `tools/data/yaml-json.html` — `：null 或 ~`（li）
- `tools/data/yaml-json.html` — `str/int/float/bool/null/date`（td）
- `tools/it/csv-to-yaml.html` — `值为空时输出空字符串；如需 null 可后续手动替换。`（li）
- `tools/it/csv-to-json.html` — `：空行与列数不一致的行要明确策略（跳过或补 null）。`（li）
- `tools/it/json-to-xml.html` — `JSON.parse 后递归转 XML：null 输出 <标签 null="true" />；布尔与数字直接包标签；字符串包标签并做 XML 转义；数组逐项按同一标签名重复输出；对象对每个键递归、缩进为 depth 个两空格；标签名须匹配 ^[A-Za-z_][\w.-]*$，否则把非法字符替换为下划线并在必要时加下划`（div.formula-eq）
- `tools/it/json-schema-generator.html` — `由样例数据递归推断 Schema：null 得 type=「null」；数组得 type=「array」，非空时对每个元素递归推断后合并为 items；字符串得 type=「string」，并按内容依次尝试识别 format——邮箱、URI、日期时间、日期、IPv4、IPv6、UUID；数字按 Number.isInt`（div.formula-eq）
- `tools/it/php-cheatsheet.html` — `$name = "Alice"; $age = 30; $name = null; echo "Hi $name"; echo 'Hi ' . $name;`（div.cmd-example）
- `tools/it/php-cheatsheet.html` — `null 安全`（span.cmd-desc）
- `tools/it/regex-cheatsheet.html` — `返回数组或 null`（div.cmd-row）
- `tools/it/typescript-cheatsheet.html` — `let n: number = 1; let s: string = "hi"; let b: boolean = true; let nul: null = null; let un: undefined = undefined; let bi: bigint = 100n; let sym: symbol = Sy`（div.cmd-example）

### 疑似：默认态结果区只有零值（20 页，需人工判断是否该提示「请输入」）

- `tools/dentistry/calc-1.html` — div#result.result-box：DMFT 指数：0 评估：龋病风险较低 D+M+F = 0（恒牙龋坏、缺失、充填牙数之和） 提示：DMFT 用于群体或个人龋病经历评估，儿童乳牙龋可采用 dmft 指数；诊断与治疗请咨询口腔科医生。
- `tools/dermatology/vasi-vitiligo.html` — div#result.result-box：0.0% VASI 受累体表面积 / 极轻度 管理建议：局限型，以外用糖皮质激素/钙调磷酸酶抑制剂为主，注意防晒。
- `tools/edu/exam-gpa-calculator.html` — div.result-grid：- 📋 复制结果 ⬇️ 导出 TXT GPA 0 总学分
- `tools/elderly/eldercare-level.html` — div#result.result-box：总分：0 建议等级：一级（轻度） 照护建议：日常自理能力基本完整，建议日常巡检。 提醒：该结果不替代医生或国家评估标准，仅用于家庭自查。
- `tools/fengshui/fengshui-calculator.html` — div#directionResult.direction-result：🧭 正北方向 · 0.0° 八卦方位：坎卦 · 五行：水 · 二十四山：壬 子 癸 坎 正北 · 水 艮 东北 · 土 震 正东 · 木 巽 东南 · 木 离 正南 · 火 坤 西南 · 土 兑 正西 · 金 乾 西北 · 金
- `tools/forensic-medicine/burn-assessment.html` — div#areaResult.result-box：烧伤总面积 0.0% 体表面积(TBSA) 0.0% 总面积 0% 手掌法补充 小面积烧伤，预后较好。
- `tools/futures/option-payoff.html` — section.opt-result-interpret：📊 结果解读 盈亏结构 看涨期权买方盈亏 = max(到期价−行权价,0)−权利金；看跌相反。盈亏平衡点 = 行权价±权利金。卖方为买方镜像、收益封顶于权利金。 用途 绘制不同到期价下盈亏，评估策略风险收益；杠杆与时效（Theta）显著影响实际结果。 边界 本图按到期静态盈亏，未含希腊字母动态与保证金；期权高风险，仅供学习，实盘请合规并自担风险。
- `tools/hr/overtime-pay-calc.html` — div#result.result-box：工作日加班费：0.00 元 休息日加班费：0.00 元 法定节假日加班费：0.00 元 总加班费：0.00 元
- `tools/it/calc-5.html` — div#result.result-box：文本总长度：0 字符 / 0 字节 中文字符：0，标点符号：0 平均每个字符约 0 字节
- `tools/it/sql-escape.html` — div.result-box：MySQL: 单引号 → \' 反斜杠 → \\ NUL → \0 PostgreSQL: 单引号 → '' 不转义反斜杠（默认） SQL Server: 单引号 → '' 不转义反斜杠
- `tools/language/grammar-checker.html` — div#result：✓ 太好了!未发现明显的语法问题 问题密度：0.00 处/句（良好）
- `tools/neurology/ncs-emg.html` — div#result.result-box：检查结果基本正常或非特异性改变 电生理特征解读 电生理特征 各参数均在正常范围或仅有轻微非特异性改变 鉴别诊断 无明显周围神经病变电生理证据 建议结合临床评估，必要时复查 建议 未见明确周围神经或肌肉病变的电生理证据。建议结合临床随访。 📋 门诊记录（可直接复制进病历） 【NCS/EMG 肌电图与神经传导报告解读】 结果：电生理结论：检查结果基本正常或非特异性改变 异常参数 0 项；报告需结合临
- `tools/nutrition/calc-2.html` — div#result.result-box：0 总热量 kcal 0.0g 碳水化合物 0.0g 蛋白质 0.0g 脂肪 热量构成：碳水 0 kcal · 蛋白质 0 kcal · 脂肪 0 kcal
- `tools/obstetrics/kupperman-score.html` — div#result.result-box：0 Kupperman总分 基本正常 症状分级 0 阳性症状数 基本正常 (0分) 围绝经期症状轻微或无症状，注意健康生活方式即可。
- `tools/pet-training/command-repetition.html` — div#result.retention-main：0% 记忆严重衰退，需立即重新训练
- `tools/pr/risk-assessment.html` — div#result.result-box：0 风险总数 0 低风险 0 中风险 0 高/极高 平均风险值：0.0（低风险） 请添加风险项
- `tools/rheumatology/bvas.html` — div#result.result-box：0 BVAS 总分 无活动 疾病活动度 0 受累系统数 无活动 病情稳定，处于缓解期。维持当前免疫抑制方案，定期监测ANCA滴度和脏器功能。
- `tools/rheumatology/essdai.html` — div#result.result-box：0 ESSDAI 总分 无活动 疾病活动度 0 受累域数 无活动 无系统性脏器受累活动表现。以口眼干燥对症治疗为主，定期监测ESSDAI和淋巴瘤筛查。
- `tools/science/logic-gate-simulator.html` — div.output-panel：输出 Q 0 📋 复制结果 ⬇️ 导出 TXT
- `tools/thermodynamics/polytropic-work.html` — div#result.result-box：0.00 过程功 W (kJ)

<!-- default-dirty:end -->
