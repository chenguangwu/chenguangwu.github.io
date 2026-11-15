# 527 canvas 文案英文态（二）：finance 补漏 + science + 自动图表标签

- 日期：2026-11-15
- 线索：526 批建立的 canvas 探针在修正两处假阴性后，暴露出一批此前「PASS/SKIP」的页面其实仍有中文。

## 探针三处修正（假阴性来源）

1. 改走本地 HTTP 静态服务（`http://127.0.0.1:<随机端口>`）：`file://` 下 `js/toolbox.js` 路径解析失败、
   i18n 字典 `fetch` 被 CORS 拦截，导致 `ToolBox is not defined`、页面根本没画图。
2. 去掉 `clearRect` 重置日志：多画布页面后画的图会调用 `clearRect` 把先前 `fillText` 记录一并清空，
   使含中文的画布「看起来干净」；改为每次触发前显式清空 `__fillLog`。
3. `triggerCalc` 先调用页面的 `__*Presets` 填示例值，再枚举 `calc*/draw*/render*/compute*/update*/refresh*`
   无参函数；否则输入守卫直接 `return`，页面永远 SKIP。另改为复用单一标签页，避免上百页规模下
   `Target.createTarget` 会话崩溃。

## 页面修复

| 页面 | 改动 |
| --- | --- |
| `science/rc-time-constant` | 图例 充电/放电 → Charging/Discharging；挂重绘 |
| `finance/dca-calculator` | `formatShort` 亿/万→k/M/B；`第N年`→`Year N`；挂重绘 |
| `finance/inflation-calculator` | 同上 |
| `finance/mutual-fund-calculator` | 同上 |
| `finance/bond-yield-calculator` | 复用页面已有 `__bondEn()`：年份/现金流（元）/`第N年`/空态提示；挂重绘 |
| `finance/position-size-calculator` | 胜率/仓位比例/价格/盈亏/加仓层级/累计投入 四组轴标题、满凯利/实际仓位/止损图例；挂重绘 |
| `finance/break-even-calculator` | 敏感性图图例 售价/变动成本/固定成本 → Price/Variable cost/Fixed cost |
| `finance/option-profit-calculator` | 盈亏平衡/标的价格/每股盈亏；挂重绘 |
| `finance/credit-card-interest` | 标签来自共享自动图表 `data-labels` 属性，见下 |

## 共享层：`data-labels` 不再漏译

`js/common.js` 的 `initResultViz()` 直接读中文 `data-labels` 画图，该属性不参与 DOM i18n。

- `js/tool-i18n.js`：暴露 `window.__tbEnLookup = pickEn`（与 DOM 同一套 per-tool/通用层/正文短语表），
  字典异步加载完成后派发 `toolbox:dictready`。
- `js/common.js`：英文态用 `__tbEnLookup` 逐条翻译 `data-labels`（无键保留原文）；
  监听 `toolbox:langchange` / `toolbox:dictready` 重跑 `initResultViz()`。
- 字典补键：`finance/credit-card-interest.json` 加 本金/利息/应还总额；
  `agriculture/crop-water-requirement.json` 加 需水量/作物系数。

## 验收

- `_en_canvas_probe.mjs finance` → 115 页 FAIL/ERR **0**（SKIP 0）。
- `_en_canvas_probe.mjs agriculture` → 64 页 FAIL/ERR **0**。
- `_en_canvas_probe.mjs science` → 92 页 FAIL/ERR **0**（`range-calculator` 无 canvas，SKIP）。
- `--check finance / agriculture / science` → 113 / 63 / 90 页，残留均 **0**。
- `python3 _build.py` 通过；`python3 _test_static.py` 4685/4685（含 `js/common.js`、`js/tool-i18n.js` 改动）。

## 剩余（`plan/i18n-canvas-todo.md`）

- P1 收尾：astronomy（earth-curvature/solar-elevation/tide-estimator）、maritime（tide-window）。
- P1 其他：aerospace、marketing、procurement/eoq、health、healthcare、hematology、medical、sales、admin。
- P2：fun 游戏画布、image 模板、ophthalmology 视标、cognition/psychology 结果图。
