# 526 canvas 文案英文态：agriculture 3 页 + finance 10 页清零

- 日期：2026-11-15
- 背景：525 批验收只覆盖 DOM 文本节点与 `placeholder/title/aria-label/alt` 属性；
  `<canvas>` 内 `ctx.fillText()` 绘制的文字不参与 DOM i18n，`--check` 扫不到，属于未覆盖缺陷。
- 工具：新建 `scripts/_en_canvas_probe.mjs`（puppeteer-core + 本机 Chrome，重写
  `CanvasRenderingContext2D.prototype.fillText` 记录绘制串）。三帧判定：
  `?lang=en-US` → `I18n.set('zh-CN')` → `I18n.set('en-US')`，英文帧不得含汉字、中文帧须含汉字。
  新增 `PASS-noredraw` 状态：第三帧为空而首帧非空时不判 PASS，避免「未挂重绘」的假通过。

## 修复清单

| 行业 | 页面 | 主要改动 |
| --- | --- | --- |
| agriculture | fertilizer-calculator | 图表标题与 N/P/K 图例三元化，挂 `__tbRedraw` |
| agriculture | irrigation-calculator | 面板标题、净灌溉/输水损失、`m³/亩`→`m³/mu`，挂重绘 |
| agriculture | pesticide-dose | 用药量/用水量、亩/总用药量图例三元化，挂重绘 |
| finance | break-even-calculator | 盈亏平衡点/销量/金额轴、敏感性图两轴；`formatMoney` 英文口 k/M；重绘走 `calc()` |
| finance | compound-interest | `fmtShort` 英文口 k/M/B；年份轴、总资产/累计投入图例；挂重绘 |
| finance | depreciation-calculator | 期初/第 i 年轴、四种方法图例；重绘走 `calc()` |
| finance | investment-roi | 三张图年份轴、成本标注、总价值/投入本金、方案 A/B；按当前 tab 重绘 |
| finance | irr-calculator | `fmtShort` 英文口 k/M/B；流入/流出图例；挂重绘 |
| finance | lease-payment-calculator | 第 N 期轴；`formatShort` 英文口 k/M/B；重绘走 `calc()` |
| finance | loan-amortization | 饼图本金/利息及标题、折线图万→k/M 轴、还款曲线/剩余本金/累计利息；重绘走 `calc()` |
| finance | npv-calculator | 初始/第 N 期轴、投资流出/流入/累计现金流图例；重绘走 `calc()` |
| finance | retirement-calculator | 亿/万→k/M/B 轴、退休线、资产增长曲线图例、年龄轴；重绘走 `calc()` |
| finance | profit-margin-calculator | `formatMoney` 英文口 k/M/B；总成本环图、瀑布图八个条目；重绘走 `calc()` |

统一约定：绘制函数首行 `var en = /^en/i.test(document.documentElement.lang || '')`，
末尾注册 `window.__tbRedraw` + `toolbox:langchange` 监听（`js/i18n.js` 的 `set()` 会派发该事件）。

## 探针本身的两处修正

1. `triggerCalc` 前先清空 `window.__fillLog`：部分页面靠 `canvas.width = ...` 重置画布而非
   `clearRect`，历史中文帧会污染首帧判定（retirement 首轮即因此误报）。
2. `triggerCalc` 从固定函数名列表改为枚举 `window` 上所有 `calc*/draw*/render*/compute*/update*/refresh*`
   无参函数；原先 investment-roi（`calcSimple/calcRegular/calcCompare`）等页面完全不触发，只能 SKIP。
   改动后立刻暴露出 profit-margin-calculator 的真实残留。

## 验收

- `node scripts/_en_canvas_probe.mjs finance` → 115 页，FAIL/ERR **0**。
- `node scripts/_en_canvas_probe.mjs agriculture` → 64 页，FAIL/ERR **0**。
- `node scripts/_en_i18n_probe.mjs --check finance` → 113 页，有残留 **0** 页（DOM 层无回归）。
- `python3 _build.py` 通过；`python3 _test_static.py` 4685/4685。
- 说明：本批只改页面内联 `<script>` 的绘制文案与数字缩写，不动结构化文案，`_build.py` 不覆盖这些改动。

## 剩余（见 `plan/i18n-canvas-todo.md`）

- P1：science、astronomy、maritime 等行业的 canvas 页；
- P2：fun 画布、image 模板、ophthalmology。
