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
| `life/date-difference-calculator.html` | 加减月 | ✅ 已修：`addMonthsClamped()` 月末夹取（本批补闰年/平年用例）。 |
| `life/temperature-converter.html` | 单位换算 | ✅ 已修：新增绝对零度下界（−273.15℃ / 0K / −459.67℉），低于即拒绝并提示；K/°F/°R 输入同校验。 |
| `life/workday-calculator.html`、`life/age-in-days.html`、`life/date-diff.html`、`life/countdown.html`、`life/reminder-cycle.html`、`life/cycle-pruning-lawn.html` | — | ☑️ 判安全：本地年月日构造 / Date 克隆 / epoch 毫秒 / datetime 本地解析。 |
| `design/farnsworth-d15-test.html`、`design/palette-cvd-checker.html`、`design/signature-pad.html` | — | ☑️ 判安全：仅导出元数据时间戳 / 文件名时间戳，不参与日期计算。 |

