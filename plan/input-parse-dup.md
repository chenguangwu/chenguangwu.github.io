# 数字输入解析重复清单（设计与生活线）

> 用途：统一抽取公共输入解析函数前的收编清单。**本批不改 `js/common.js`**，仅登记现状。
> 统计范围：`tools/design/**`、`tools/life/**`、`tools/fun/**`、`tools/library/**`、`tools/art/**`（不含 `tools/image/**` 等其它分类）。
> 统计口径：页面内联脚本直接读取表单值并转数字的写法（`parseFloat(document.getElementById(...))`、`+document.getElementById(...).value`）。

## 结论

- **共 58 页**直接 `parseFloat(document.getElementById(...))`，未做任何归一化（design 23 / life 31 / fun 2 / library 2 / art 0）。
- 另有 **16 页**使用一元 `+document.getElementById(...).value`（design 11 / life 2 / fun 3），部分与上面重叠。
- **已自带归一化实现、应优先替换为公共函数的 4 页**：`analysis-cost-10`、`percentage-calculator`、`timestamp`、`px-to-rem`（写法各不相同，见下表 A）。
- 统一后建议函数：`ToolBox.parseNumber(raw, {stripUnits, allowComma, fullWidth})`，返回 `{value, error}`；解析失败要把原文回显，禁止静默变 0。

## A 组：已有归一化实现（4 页，抽公共函数的首批替换点）

| 页面 | 现有写法 | 说明 |
|---|---|---|
| `tools/life/analysis-cost-10.html` | `norm()`：全角数字→半角、`．`→`.`、`，`→`,`、去 `￥¥`、去「元/块」、循环去千分位逗号 | 整行解析，失败行收集后回显原文 |
| `tools/life/percentage-calculator.html` | `numVal()`：全角数字→半角、去 `，,`、去 `％%`、去 `￥¥` | 每个输入独立解析 |
| `tools/life/timestamp.html` | `parseTimestamp()`：全角数字→半角、去 `，,`、去空白/全角空格、`parseFloat`、按数量级判断秒/毫秒 | 负数与小数秒按 magnitude 判断，不再按字符串长度 |
| `tools/design/px-to-rem.html` | `num()`：全角数字→半角、`．`→`.`、去 `，,`、去 `px/rem` 后缀 | 根字号 ≤0 时按 16px 计算并明示 |

## B 组：`parseFloat(document.getElementById(...))` 直读（58 页）

### design（23 页）

`analysis-64.html`、`breakpoint-queries.html`、`card-generator.html`、`color-shade-generator.html`、`css-animation-generator.html`、`css-grid-generator.html`、`exposure-triangle-calculator.html`、`flexbox-generator.html`、`generator-33.html`、`generator-34.html`、`image-rotator.html`、`loading-dots.html`、`particle-effect-generator.html`、`photo-print-size.html`、`pixel-art-generator.html`、`rem-to-px.html`、`ripple-effect.html`、`shutter-speed-calculator.html`、`spacing-scale.html`、`spinner-generator.html`、`tester-assessor.html`、`typography-scale.html`、`waveform-visualizer.html`

### life（31 页）

`analysis-23.html`、`analysis-cost-9.html`、`angle-converter.html`、`area-converter.html`、`candle-burn-time.html`、`concentration-converter.html`、`cycle-4.html`、`daily-calorie-needs.html`、`data-rate-converter.html`、`data-unit-converter.html`、`date-add-subtract.html`、`density-converter.html`、`drinking-water-plan.html`、`energy-converter.html`、`flow-rate-converter.html`、`frequency-converter.html`、`generator-random-1.html`、`length-converter.html`、`magnet-converter.html`、`parking-fee.html`、`power-converter.html`、`pressure-converter.html`、`radiation-converter.html`、`report-profit.html`、`shoe-size-converter.html`、`speed-converter.html`、`temperature-converter.html`、`time-converter.html`、`unit-converter.html`、`volume-converter.html`、`weight-converter.html`

### fun（2 页）

`meditation-timer.html`、`random-name-gen.html`

### library（2 页）

`overdue-fine.html`、`shelf-capacity.html`

### art（0 页）

## C 组：仅做分隔符归一（未处理全角数字/单位后缀）

| 页面 | 写法 | 待补齐 |
|---|---|---|
| `tools/life/stats-13.html` | 姓名/份数支持半角与全角逗号、顿号、分号、制表符、空格 | 全角数字（１２３）仍会解析失败，建议并入公共函数 |
| `tools/life/analysis-cost-9.html` | 逗号/空白分隔行 | 同上 |

## 备注

- 上表页面均未改动，仅登记；后续统一抽函数时按 A→B→C 顺序替换，并在各分类 verify 用例中补「全角/千分位/单位后缀」注入断言。
- 有 16 页使用一元 `+`（design 11 / life 2 / fun 3），替换时注意 `+'' === 0` 的静默零值陷阱，公共函数应返回显式错误。
