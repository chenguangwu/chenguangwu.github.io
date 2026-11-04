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

