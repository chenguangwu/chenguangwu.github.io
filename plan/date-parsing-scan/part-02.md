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

