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

## 4. 其它目录清单（按目录归属，待分派）

共 **153 条 / 76 页**，目录分布：`legal` 39、`health` 20、`general` 8、`travel` 7、`automotive` 6、`obstetrics` 6、`rental` 5、`beauty` 4、`ecommerce` 4、`elderly` 4、`science` 4、`cleaning` 3、`clinical-nursing` 3、`library` 3、`livestock` 3、`textile` 3、`video` 3、`clinical-lab` 2、`healthcare` 2、`medical` 2、`pet` 2、`property` 2、`usedcar` 2、`aerospace` 1、`agriculture` 1、`archaeology` 1、`cosmetic-derm` 1、`edu` 1、`endocrinology` 1、`fengshui` 1、`funeral` 1、`medical2` 1、`museum` 1、`nephrology` 1、`pediatrics` 1、`restaurant` 1、`sports` 1、`urban` 1、`wedding` 1。


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

### legal（39 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `legal/debt-statute-limitations.html` | 309 | `startDate = new Date(dueDate);` | 变量 dueDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/debt-statute-limitations.html` | 314 | `startDate = new Date(lastDemand);` | 变量 lastDemand 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/debt-statute-limitations.html` | 327 | `if(lastPromise && new Date(lastPromise) > effectiveStart){` | 变量 lastPromise 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/debt-statute-limitations.html` | 328 | `effectiveStart = new Date(lastPromise);` | 变量 lastPromise 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/debt-statute-limitations.html` | 331 | `if(lastDemand && new Date(lastDemand) > effectiveStart){` | 变量 lastDemand 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/debt-statute-limitations.html` | 332 | `effectiveStart = new Date(lastDemand);` | 变量 lastDemand 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/debt-statute-limitations.html` | 366 | `	html += `<p>${dbL('时效起算日：','Period starts on: ')}<strong>${effectiveStart.toISOString().split('T')[0]}</stron` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/debt-statute-limitations.html` | 367 | `	html += `<p>${dbL('时效届满日：','Period expires on: ')}<strong>${actualEnd.toISOString().split('T')[0]}</strong></` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/double-wage-no-contract.html` | 288 | `const hire = new Date(hireDate);` | 变量 hireDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/double-wage-no-contract.html` | 289 | `const end = new Date(endDate);` | 变量 endDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/double-wage-no-contract.html` | 314 | `	__dwD = {hireDate: hireDate, endDate: endDate, salary: salary, months: months, total: total, startStr: startO` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/double-wage-no-contract.html` | 316 | `	<p>${dwL('双倍工资起算：','Double wage starts from: ')}<strong>${startOfDouble.toISOString().split('T')[0]}</strong>` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/double-wage-no-contract.html` | 317 | `	<p>${dwL('计算截止日期：','Calculation end date: ')}<strong>${actualEnd.toISOString().split('T')[0]}</strong></p>` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/labor-compensation.html` | 365 | `const hireD = new Date(hire);` | 变量 hire 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/labor-compensation.html` | 366 | `const leaveD = new Date(leave);` | 变量 leave 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/late-payment-interest.html` | 306 | `	const today = new Date().toISOString().split('T')[0];` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/legal-age.html` | 301 | `const birth = new Date(birthDate);` | 变量 birthDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/legal-age.html` | 372 | `	items.push({date: new Date().toISOString().split('T')[0], label: laL('今天','Today')+' '+D.years+laL('岁','y'), ` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/legal-age.html` | 376 | `	items.push({date: dd.toISOString().split('T')[0], label: pend[i].age+laL('岁','y')+' '+laL(pend[i].name, msEn[` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/legal-reference.html` | 600 | `var applyDate = new Date(dateStr);` | 变量 dateStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/legal-reference.html` | 638 | `	html += '<p style="margin:8px 0;font-size:13px;"><strong>到期日期：</strong>' + ToolBox.escHtml(expireDate.toISOSt` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/legal-reference.html` | 775 | `	var today = new Date().toISOString().split('T')[0];` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/loan-statute-limitations.html` | 356 | `startDate = new Date(dueDate);` | 变量 dueDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/loan-statute-limitations.html` | 359 | `startDate = new Date(lastInstallmentDate);` | 变量 lastInstallmentDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/loan-statute-limitations.html` | 362 | `startDate = new Date(claimDate);` | 变量 claimDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/loan-statute-limitations.html` | 372 | `if(lastDemandDate) interruptDates.push({date: new Date(lastDemandDate), reason: lsL('催款（提出履行请求）','Demand for p` | 变量 lastDemandDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/loan-statute-limitations.html` | 373 | `if(lastPaymentDate) interruptDates.push({date: new Date(lastPaymentDate), reason: lsL('部分还款（义务人同意履行）','Partial` | 变量 lastPaymentDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/loan-statute-limitations.html` | 374 | `if(promiseDate) interruptDates.push({date: new Date(promiseDate), reason: lsL('承诺还款（义务人同意履行）','Promise to repa` | 变量 promiseDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/loan-statute-limitations.html` | 379 | `	interruptReason = lsL(`最后一次时效中断事由：${interruptDates[0].reason}（${interruptDates[0].date.toISOString().split('T` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/loan-statute-limitations.html` | 408 | `	html += `<p style="margin-top:8px;">${lsL('时效起算日：','Period starts on: ')}<strong>${actualStartDate.toISOStrin` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/loan-statute-limitations.html` | 409 | `	html += `<p>${lsL('诉讼时效届满日：','Limitation period expires on: ')}<strong style="font-size:16px;">${expirationDa` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/patent-term-calculator.html` | 333 | `var applyDate = new Date(applyStr);` | 变量 applyStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/patent-term-calculator.html` | 341 | `new Date('2021-06-01') 作为专利期限起算分界` | 字面量日期按 UTC 解析，负时区回退一天，起算分界偏移。 | 改为 new Date(2021, 5, 1) 或 new Date(Date.UTC(2021,5,1)) 并统一取 UTC 分量。 |
| `legal/patent-term-calculator.html` | 372 | `	__ptD = {type: type, years: actualYears, apply: applyStr, grant: grantStr, expire: expireDate.toISOString().s` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/statute-limitations.html` | 306 | `let start = new Date(startDate);` | 变量 startDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/statute-limitations.html` | 311 | `const interrupt = new Date(interruptionDate);` | 变量 interruptionDate 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `legal/statute-limitations.html` | 342 | `	__slD = {start: startDate, limitType: limitType, interrupt: interruptionDate, effective: effectiveStart.toISO` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/statute-limitations.html` | 347 | `	<p>${slL('届满日期：','Expiry date: ')}<strong style="color:var(--primary);">${actualEnd.toISOString().split('T')[` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `legal/will-template-generator.html` | 421 | `var d = new Date(dateStr);` | 变量 dateStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |

### library（3 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `library/overdue-fine.html` | 357 | `	document.getElementById('returnDate').value = new Date().toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `library/overdue-fine.html` | 365 | `	document.getElementById('borrowDate').value = b.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `library/overdue-fine.html` | 366 | `	document.getElementById('dueDate').value = d.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### livestock（3 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `livestock/castration-timing.html` | 304 | `	dateStr = today.toISOString().split('T')[0];` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `livestock/fattening-pig-timeline.html` | 275 | `	dateInput.value = today.toISOString().split('T')[0];` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `livestock/fattening-pig-timeline.html` | 295 | `var startDate = new Date(startStr);` | 变量 startStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |

### medical（2 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `medical/reminder-2.html` | 400 | `var exp = new Date(expiry);` | 变量 expiry 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `medical/reminder-2.html` | 566 | `	var today = new Date().toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### medical2（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `medical2/drug-expiry.html` | 370 | `	document.getElementById('fExpiry').value = d.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### museum（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `museum/historical-calendar.html` | 499 | `	document.getElementById('date-input').value = today.toISOString().slice(0, 10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### nephrology（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `nephrology/manager-1.html` | 638 | `	date: new Date().toISOString().slice(0,10)` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### obstetrics（6 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `obstetrics/cycle-8.html` | 597 | `	var today = new Date().toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `obstetrics/due-date.html` | 259 | `edd=new Date(eddStr);` | 变量 eddStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `obstetrics/due-date.html` | 262 | `lmp=new Date(lmpStr);` | 变量 lmpStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `obstetrics/gestational-age.html` | 296 | `var lmp=new Date(lmpStr);` | 变量 lmpStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `obstetrics/gestational-age.html` | 361 | `var usDate=new Date(usStr);` | 变量 usStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `obstetrics/gestational-age.html` | 373 | `var lmp=new Date(lmpStr);` | 变量 lmpStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |

### pediatrics（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `pediatrics/vaccine-schedule.html` | 252 | `	return d.toISOString().split('T')[0];` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### pet（2 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `pet/pet-medicine.html` | 515 | `	const record={date:new Date().toISOString().split('T')[0],time:new Date().toTimeString().slice(0,5),...r};` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `pet/training-planner.html` | 517 | `	const record={date:new Date().toISOString().split('T')[0],time:new Date().toTimeString().slice(0,5),...p};` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### property（2 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `property/irrigation-schedule.html` | 335 | `var start = startStr ? new Date(startStr) : new Date();` | 变量 startStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `property/irrigation-schedule.html` | 395 | `	document.getElementById('startDate').value = new Date().toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### rental（5 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `rental/cycle-11.html` | 356 | `	readings.push({ date: new Date().toISOString().slice(0, 10), value: 0, note: '初始读数' });` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `rental/cycle-11.html` | 379 | `	readings.push({ date: new Date().toISOString().slice(0, 10), value: lastVal, note: '' });` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `rental/cycle-11.html` | 422 | `	var settlementRecord = { date: new Date().toISOString().slice(0, 10), items: [] };` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `rental/reminder-4.html` | 483 | `	var defaultStart = today.toISOString().slice(0, 10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `rental/reminder-4.html` | 484 | `	var defaultEnd = new Date(today.getTime() + 365 * 24 * 3600 * 1000).toISOString().slice(0, 10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### restaurant（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `restaurant/taste-preference.html` | 341 | `	const key=d.toISOString().split('T')[0];` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### science（4 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `science/astro-geo-calculator.html` | 483 | `	document.getElementById('sun-date').value = today.toISOString().split('T')[0];` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `science/astro-geo-calculator.html` | 870 | `	document.getElementById('sun-date').value = today.toISOString().split('T')[0];` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `science/tide-height-estimator.html` | 288 | `	const dateStr = today.toISOString().split('T')[0];` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `science/tide-height-estimator.html` | 296 | `	document.getElementById('inputDate').value = today.toISOString().split('T')[0];` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### sports（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `sports/sports-stats.html` | 311 | `	const date = document.getElementById('aDate').value \|\| new Date().toISOString().slice(0, 10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### textile（3 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `textile/cost-calculator.html` | 402 | `	function saveRecord(){if(!window._lastCalc)return;const r={date:new Date().toISOString().split('T')[0],time:n` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `textile/dye-mixer.html` | 346 | `	function saveRecord(){if(!window._lastCalc\|\|Object.keys(selected).length===0)return;const r={date:new Date().` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `textile/pattern-calculator.html` | 343 | `	function saveRecord(){if(!window._lastCalc)return;const r={date:new Date().toISOString().split('T')[0],time:n` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### travel（7 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `travel/timezone-converter-advanced.html` | 320 | `	document.getElementById('fromTime').value = local.toISOString().slice(0, 16);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `travel/travel-days-counter.html` | 246 | `	function setStartToday(){const d=new Date().toISOString().slice(0,10);document.getElementById('start').value=` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `travel/travel-days-counter.html` | 247 | `function setEndWeek(){const s=document.getElementById('start').value;if(s){const d=new Date(s);d.setDate(d.get` | 变量 s 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `travel/travel-days-counter.html` | 252 | `const start=new Date(s),end=new Date(e),now=new Date();` | 变量 s 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |
| `travel/travel-days-counter.html` | 274 | `	document.getElementById('start').value=new Date(Date.now()+7*86400000).toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `travel/travel-days-counter.html` | 275 | `	document.getElementById('end').value=new Date(Date.now()+14*86400000).toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |
| `travel/world-timezone-converter.html` | 357 | `	document.getElementById('localDate').value=now.toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### urban（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `urban/calc-spacing.html` | 254 | `var dateLabel=new Date(dateStr).toLocaleDateString('zh-CN',{month:'long',day:'numeric'});` | 变量 dateStr 作为日期串（控件值或今日串）；date-only 按 UTC 解析，负时区回退一天；配合本地 getMonth/getDate 时月末/闰日/跨年边界偏移。 | 改用 new Date(y, m-1, d) 按本地年月日构造；若为纯 UTC 语义则统一用 Date.UTC + getUTC*。 |

### usedcar（2 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `usedcar/recorder-maintenance.html` | 353 | `	const date=document.getElementById('rDate').value\|\|new Date().toISOString().slice(0,10);` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `usedcar/recorder-maintenance.html` | 490 | `	document.getElementById('rDate').value=new Date().toISOString().slice(0,10);` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

### video（3 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `video/video-compressor.html` | 357 | `	function saveRecord(){if(!window._lastCalc)return;const r={date:new Date().toISOString().split('T')[0],time:n` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `video/video-converter.html` | 366 | `	const r={date:new Date().toISOString().split('T')[0],time:new Date().toTimeString().slice(0,5),...window._las` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |
| `video/video-speed.html` | 472 | `	const r={date:new Date().toISOString().split('T')[0],time:new Date().toTimeString().slice(0,5),..._lastCalc};` | 展示/保存的日期取自 UTC，可能与本地日期差一天（需要 UTC 语义的时间戳除外）。 | 展示与按日分组改本地格式化；仅时间戳/ICS 明确保留 UTC。 |

### wedding（1 条）

| 页面 | 行 | 用法 | 后果 | 建议改法 |
|---|---|---|---|---|
| `wedding/countdown-timeline.html` | 360 | `	document.getElementById('weddingDate').value=defaultDate.toISOString().split('T')[0];` | 默认值/输入框「今天」取自 UTC 日期，负时区全天、UTC+8 的 0–8 点会差一天。 | 改用本地 getFullYear/getMonth/getDate 拼 YYYY-MM-DD（或 getTimezoneOffset 校正后再 toISOString）。 |

## 5. 安全 / 正常（示例，勿改）

- `life/timestamp.html`、`edu/timezone-converter.html`、`travel/timezone-converter-advanced.html`（偏移校正后 toISOString，结果=本地墙上时间）、`legal/calendar-qr.html`（本地解析→UTC 生成 ICS）、`chinese/lunar-calendar.html`/`funeral/reminder-3.html`（UTC 仅作算法中间量，输出重建本地日期）。
- `life/date-add-subtract.html` 的 `new Date('YYYY-MM-DDTHH:MM')` 与 `life/countdown.html` 的 `new Date(d+'T'+t+':00')`：datetime 形式按本地解析。
- `legal2/*`、`library/overdue-fine.html`、`library/overdue-fine` 的 `new Date(parseDate(...))`：已是 Date 对象克隆。
- `sports/sports-schedule.html` 的 `valueAsDate || new Date()`：已是 Date 对象。
- 各页 `new Date(t)` / `new Date(h.t)`：历史记录为 epoch 毫秒；`ugs` 排序比较与导出文件名时间戳不影响日期正确性。

## 6. 2026-11-05 收口：travel / automotive / life 本批处置

| 页面 | 行 | 处置 |
|---|---|---|
| `travel/travel-days-counter.html` | 246/247/252/274/275 | ✅ 已修：新增 `parseLocalDate`/`fmtDate`，默认值与 +7/+14 天改本地格式化；`calc()` 改本地解析 + `Date.UTC` 零点差，避开 DST 的 23/25 小时日。 |
| `travel/world-timezone-converter.html` | 357 | ✅ 已修：默认日期改 `fmtLocalDate(now)`；同页删除死代码 `isDST()`，改 IANA `zoneOffset()` 实时偏移（卡片/图表/导出表统一），并修 `setHours` 原地改写导致的「所有城市恒 00:00」。 |
| `travel/timezone-converter-advanced.html` | 320 | ☑️ 判安全，不改：`new Date(now.getTime() - getTimezoneOffset()*60000)` 偏移校正后 `toISOString()` 恰为本地墙上时间。 |
| `automotive/auto-beauty-calc-1.html` | 288 | ✅ 已修：新增 `parseLocalDate`；同页 `addMonths` 由裸 `setMonth` 改「目标月首日 + 日夹取」（1/31 +1 月 → 2/28，闰年 2/29）。 |
| `automotive/countdown-engine-oil.html` | 331 | ✅ 已修：新增 `todayStr()`，本地拼 YYYY-MM-DD。 |
| `automotive/cycle-13.html` | 335/359 | ✅ 已修：`wDate` 默认与保存回退均改 `todayStr()`。 |
| `automotive/cycle-belt.html` | 434 | ✅ 已修：`savedAt` 改 `todayStr()`。 |
| `automotive/fuel-anomaly.html` | 264 | ✅ 已修：记录日期改 `todayStr()`。 |
| `life/date-difference-calculator.html` | 加减月 | ✅ 已修：`addMonthsClamped()` 月末夹取（本批补闰年/平年用例）。 |
| `life/temperature-converter.html` | 单位换算 | ✅ 已修：新增绝对零度下界（−273.15℃ / 0K / −459.67℉），低于即拒绝并提示；K/°F/°R 输入同校验。 |
| `life/workday-calculator.html`、`life/age-in-days.html`、`life/date-diff.html`、`life/countdown.html`、`life/reminder-cycle.html`、`life/cycle-pruning-lawn.html` | — | ☑️ 判安全：本地年月日构造 / Date 克隆 / epoch 毫秒 / datetime 本地解析。 |
| `design/farnsworth-d15-test.html`、`design/palette-cvd-checker.html`、`design/signature-pad.html` | — | ☑️ 判安全：仅导出元数据时间戳 / 文件名时间戳，不参与日期计算。 |
