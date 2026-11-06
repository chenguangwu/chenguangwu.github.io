# 全站日期解析模板排查（2026-11-05）

## 1. 扫描口径

- 范围：`tools/**/*.html` 全量 **4916 页**（只读扫描，未改动）。
- 模式：① `new Date('...')` 字符串字面量；② 日期控件值直接 `new Date(变量/.value)`；③ `toISOString()` 取「今天」/默认值/展示；④ `Date.parse('YYYY-MM-DD')`；⑤ `getUTC*` 与 `get*` 混用。
- 判定锚：同一输入在 UTC+8 与 UTC−5 下输出不同且只有一个正确，或历史日期在 UTC/本地之间不存在（2/29、月末、跨年）。
- 纯 UTC 语义页面（时间戳换算、时区换算、ICS 导出、农历/节气算法的 UTC 中间量）判「安全」，**不改**。

## 2. 三档计数

| 判定 | 计数 | 说明 |
|---|---|---|
| 真缺陷（我的目录，已修） | 1 页 | `tools/life/date-difference-calculator.html`：日期控件 UTC 解析 + `toISOString` 默认值 |
| 真缺陷（其它目录，待派工） | 153 条 / 76 页 | 见 §4，按目录分组；每行可直接派工 |
| 安全（纯 UTC 语义） | 约 30 页 | `timestamp`、`timezone-converter*`、`calendar-qr`(ICS)、`lunar-calendar`/节气 UTC 中间量等，保持 UTC；示例见 §5 |
| 正常（克隆/排序/文件名时间戳） | 约 20 页 | `new Date(t)` 历史时间戳、排序比较、导出文件名与 `exportDate`；示例见 §5 |

> 计数口径：§4 的「条」＝命中行（同一页面可能多条），已剔除纯文件名/导出元数据行；「页」＝去重文件数。

> 说明：日期控件值 `new Date(v + 'T00:00:00')`（datetime-local / 补 `T00:00:00`）按本地解析，属安全，未计入清单；仅裸 `YYYY-MM-DD` 计入。

## 3. 已修（`design/`、`life/`、`home/`）

- `life/date-difference-calculator.html`：新增 `parseLocalDate(y,m-1,d)` 与 `fmtLocalDate()`；`calcDiff/calcAddSub/saveHistory` 全部改用本地解析；`setToday()` 与首屏默认 `startDate/endDate/baseDate` 改用本地格式化，月末（1/31 → 2 月末）按 `daysInMonth` 夹取。
- `life/date-add-subtract.html`：默认 `baseTime` 由「偏移后 `toISOString().slice(0,16)`」改为本地字段拼接（原写法结果正确但属模板习惯，统一收口）。
- `design/`、`home/`：无日期控件解析；`toISOString` 仅用于导出元数据/文件名，判安全，未改。
- 同批 verify：`scripts/verify_life_calc.js` 新增闰日跨年用例（2024-02-29 → 2025-03-01 = 367 天、1年1月）。

### aerospace（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `aerospace/flight-time.html` | 478 | `	var todayStr = today.toISOString().split('T')[0];` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### agriculture（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `agriculture/calculator-calc-1.html` | 190 | `function getDate(id){var v=document.getElementById(id).value;return v?new Date(v):null;}` | 变量 v 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |

### archaeology（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `archaeology/artifact-measurement.html` | 261 | `	var dt=document.getElementById('dt').value\|\|new Date().toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### automotive（6 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `automotive/auto-beauty-calc-1.html` | 288 | `const lastDate = new Date(last);` | 变量 last 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `automotive/countdown-engine-oil.html` | 331 | `	ts:new Date().toISOString().slice(0,10)` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `automotive/cycle-13.html` | 335 | `	document.getElementById('wDate').value=new Date().toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `automotive/cycle-13.html` | 359 | `	const date=document.getElementById('wDate').value\|\|new Date().toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `automotive/cycle-belt.html` | 434 | `	const rec={id:uid(),...c,savedAt:new Date().toISOString().slice(0,10)};` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `automotive/fuel-anomaly.html` | 264 | `	records.push({date:new Date().toISOString().split('T')[0],mileage:newMileage,liters:40,price:7.8});` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### beauty（4 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `beauty/aging-calculator.html` | 558 | `	date:new Date().toISOString().split('T')[0],` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `beauty/hair-color.html` | 543 | `	date:new Date().toISOString().split('T')[0],` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `beauty/makeup-shade.html` | 549 | `	date:new Date().toISOString().split('T')[0],` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `beauty/skincare-routine.html` | 807 | `	date:new Date().toISOString().split('T')[0],` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### cleaning（3 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `cleaning/appliance-cycle.html` | 285 | `	var today = new Date().toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `cleaning/appliance-cycle.html` | 313 | `	document.getElementById('checkDate').value = new Date().toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `cleaning/appliance-cycle.html` | 369 | `new Date(lastClean + 'T00:00:00'	var nextDate = lastClean ? new Date(new Date(lastClean + 'T00:00:00').getTime` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### clinical-lab（2 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `clinical-lab/tumor-marker-doubling.html` | 406 | `	document.getElementById('d2').value = today.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `clinical-lab/tumor-marker-doubling.html` | 407 | `	document.getElementById('d1').value = past.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### clinical-nursing（3 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `clinical-nursing/cycle-7.html` | 374 | `var startTs = startVal ? new Date(startVal).getTime() : Date.now();` | 变量 startVal 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `clinical-nursing/ostomy-bag-timing.html` | 371 | `var last = new Date(lastChangeStr);` | 变量 lastChangeStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `clinical-nursing/ostomy-bag-timing.html` | 473 | `	document.getElementById('lastChange').value = now.toISOString().slice(0,16);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### cosmetic-derm（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `cosmetic-derm/post-procedure-recovery.html` | 304 | `var baseDate = dateStr ? new Date(dateStr) : new Date();` | 变量 dateStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |

### ecommerce（4 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `ecommerce/cycle-15.html` | 361 | `	purchases: [{ date: new Date().toISOString().slice(0, 10), amount: 100, note: '首次购买' }]` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `ecommerce/cycle-15.html` | 412 | `	var lastDate = cust.purchases.length ? cust.purchases[cust.purchases.length - 1].date : new Date().toISOStrin` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `ecommerce/cycle-15.html` | 413 | `new Date(lastDate	var nextDate = new Date(new Date(lastDate).getTime() + 30 * 24 * 3600 * 1000).toISOString().` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `ecommerce/cycle-15.html` | 598 | `	var nextDate = a.nextPurchaseDate ? a.nextPurchaseDate.toISOString().slice(0, 10) : '';` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### edu（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `edu/ebbinghaus-curve.html` | 367 | `const date=new Date(start);date.setDate(date.getDate()+it);` | 变量 start 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |

### elderly（4 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `elderly/medication-schedule.html` | 291 | `	const start = document.getElementById('startDate').value \|\| new Date().toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `elderly/medication-schedule.html` | 295 | `const date = new Date(start);` | 变量 start 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `elderly/medication-schedule.html` | 297 | `	const label = date.toISOString().slice(0, 10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `elderly/reminder-time.html` | 619 | `	var today = new Date().toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### endocrinology（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `endocrinology/metabolic-syndrome.html` | -1 | `Date.parse(__cd) 后 new Date(...) 取本地年月日生成随访日期` | date-only 按 UTC 解析，负时区基线回退一天，三次随访日期整体错位。 | 改 new Date(y, m-1, d) 本地构造。 |

### fengshui（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `fengshui/birthday-analysis.html` | 352 | `const d = new Date(dateStr);` | 变量 dateStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |

### funeral（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `funeral/memorial-date.html` | 559 | `	document.getElementById('memDay').value = d.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### general（8 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `general/calc-13.html` | 228 | `	var today=new Date();var tstr=today.toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `general/calc-13.html` | 230 | `	document.getElementById('v0').value=past.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `general/calc-13.html` | 277 | `	var today=new Date();var tstr=today.toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `general/calc-13.html` | 279 | `	document.getElementById('v0').value=past.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `general/calc-14.html` | 261 | `	document.getElementById('v1').value=today.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `general/calc-14.html` | 263 | `	document.getElementById('v0').value=b.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `general/calc-14.html` | 310 | `	document.getElementById('v1').value=today.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `general/calc-14.html` | 312 | `	document.getElementById('v0').value=b.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### health（20 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `health/body-fat-calculator.html` | 686 | `	date:new Date().toISOString().split('T')[0],` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `health/calorie-needs.html` | 779 | `	date:new Date().toISOString().split('T')[0],` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `health/ovulation-calculator.html` | 371 | `const ovDay = new Date(lmp);` | 变量 lmp 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/ovulation-calculator.html` | 380 | `const nextPeriod = new Date(lmp);` | 变量 lmp 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/ovulation-calculator.html` | 383 | `const periodEnd = new Date(lmp);` | 变量 lmp 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/ovulation-calculator.html` | 416 | `const ovDay = new Date(lmp);` | 变量 lmp 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/ovulation-calculator.html` | 423 | `const periodEnd = new Date(lmp);` | 变量 lmp 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/ovulation-calculator.html` | 425 | `const nextPeriod = new Date(lmp);` | 变量 lmp 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/ovulation-calculator.html` | 431 | `const viewDate = new Date(lmp);` | 变量 lmp 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/pregnancy-due-date.html` | 404 | `dueDate = new Date(lmpDate);` | 变量 lmpDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/pregnancy-due-date.html` | 409 | `lmpDate = new Date(ovDate);` | 变量 ovDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/pregnancy-due-date.html` | 411 | `dueDate = new Date(ovDate);` | 变量 ovDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/pregnancy-due-date.html` | 419 | `lmpDate = new Date(usDate);` | 变量 usDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/pregnancy-due-date.html` | 427 | `lmpDate = new Date(ivfDate);` | 变量 ivfDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/pregnancy-due-date.html` | 429 | `dueDate = new Date(ivfDate);` | 变量 ivfDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/premature-age-calculator.html` | 405 | `var birthDate = new Date(birthStr);` | 变量 birthStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/premature-age-calculator.html` | 406 | `var todayDate = new Date(todayStr);` | 变量 todayStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/premature-age-calculator.html` | 421 | `eddDate = new Date(eddStr);` | 变量 eddStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/safe-period-calculator.html` | 262 | `const lmp=new Date(lmpRaw);` | 变量 lmpRaw 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `health/safe-period-calculator.html` | 315 | `var lmp=new Date(lmpRaw);` | 变量 lmpRaw 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |

### healthcare（2 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `healthcare/bmi-calculator.html` | 650 | `	date:new Date().toISOString().split('T')[0],` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `healthcare/tdee-calculator.html` | 778 | `	date:new Date().toISOString().split('T')[0],` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

