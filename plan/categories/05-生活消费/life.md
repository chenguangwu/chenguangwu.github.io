# 生活综合 · tools/life（70 页）

## 功能缺陷
- age 系页无「法定年龄事件」联动（投票/驾车/退休倒计时）。

## 优化点
- S2 场景：「宝宝 100 天纪念」「结婚 10 周年」；S4 分享卡：生日/年龄卡。

## 受影响范围
- tools/life/（70 页）

## 进度
- 🔴 待开发

## 2026-11-06 交互静态续审（清单 412–417，生活部分）

仅源码分析，未运行页面或浏览器。

### 金额输出依赖数字读法选项并截断厘位（中，源码确认）
- `tools/life/number-to-chinese.html:183-186,372-374,402-403,492-508`：标为「大写金额」的输出复用当前选中的数字及单位，默认简体小写时 `12.34` 会按小写生成「十二元三角四分」，并非大写；小数只读取前两位，示例 `0.005` 会显示「零元整」，没有告知厘位被舍弃。涉及金额录入、复制，应单独明确金额精度与大写口径，不能静默舍弃。

### 罗马数字清空后旧拆解仍保留（中，源码确认）
- `tools/life/roman-numeral.html:170-175,333-338`：罗马输入有效后清空，仅把 `numResult` 设置为 `--`，未清空 `numBreak`，旧数字拆解继续留在结果区。需在空态同步清除拆解。

### 历史结论变化
- `phone-lookup` 使用号段表推断运营商，号段表时效未核验，且携号转网后可能变化。
- `holiday-calendar` 月工作日仍以总天数减周末和节日，重复扣除路径仍在（`:819-820,860-861`）；非已覆盖年份的数据完整性未运行验证。

### 清洁及草坪提醒跨夏令时时天数偏多（中，Node 复现）
- `tools/life/reminder-cycle.html:236-238` 与 `tools/life/cycle-pruning-lawn.html:298-300` 以本地午夜的毫秒差除以 24 小时后向上取整。`TZ=America/Los_Angeles` 下，从 2026-10-31 到 2026-11-07 相隔 7 个日历日，但跨越夏令时回拨共 169 小时，页面计算为 8 天。两页的下次日期已用本地日历日期加天数；剩余问题是倒计时天数和紧急程度可能偏大。

## 2026-11-06 交互静态续审（清单 406–411）

仅源码分析，未运行页面、浏览器或安全载荷；下述为源码可达性及推导，需回归验证。`cycle-4` 用品单位/日志字段未转义拼 HTML 的注入点已于第 953 批全部经 `ToolBox.escHtml` 修复，真机回放证明判别有效，从待办删除。

### 其他路径与旧结论
- `cycle-4` 的场景预设仍直接覆盖现有用品（`:477-495`，既有 LF-N85）；`data-unit-converter` 历史恢复仍无参调用 `setMode()`（`:329-334,473-485`，既有 LF-N36）。
- `event-countdown` 的节日日期、清明固定日期和年度范围与既有记录对应；刷新及定时重算为源码路径，未验证实际显示。
- `cycle-pruning-lawn` 使用本地日期构造；`color-name-finder` 增加十六进制格式校验；`bill-splitter` 简单 AA 对负数、余数和姓名转义的旧路径已改变。详见原条目标注，不据此宣称回归通过。

## 2026-11-03 审计补充

### 密码生成失败后仍可复制旧密码（高，确认缺陷）
- 问题：取消全部字符类型后再生成，页面提示选择类型，但强度条未重置，复制仍读取上次生成的密码。
- 证据：`tools/life/generator-strength.html:373-393,414-421,430`：空字符池只更新提示与列表后 return，未清空 `allPwds`、强度条；默认加载时执行 `gen()`。浏览器行为未实测。
- 影响：`tools/life/generator-strength.html`；复制所得内容与当前失败状态不一致。
- 方案：失败分支清空密码数组和强度状态，禁用复制直到成功生成；补有效→全部取消→复制测试。

### 留存优化：可解释的强度与配置（低，建议）
- 证据：同页 `:375-393` 展示长度与字符种类及强度；支持批量生成（`:375-376,395-401`）。
- 影响：同页；方案：解释随机字符池与熵估算假设，并提供易读字符排除选项；不得将密码写入历史或分享卡。

### 月末加月与页面承诺不一致（高，确认函数缺陷）
- 问题与证据：`tools/life/date-add-subtract.html:145-149,291-314` 说明月末应取目标月末，代码直接 `setMonth()`；原函数内存执行 2023-01-31 12:00 加 1 月得到 2023-03-03 12:00，而非 2 月末。
- 影响：`tools/life/date-add-subtract.html`，续期和纪念日计算可能错月。
- 方案：先确定目标年月，再将日夹到该月末，测试闰年、负月数和加年；明确日历日与固定 24 小时的语义。

### 覆盖
- 本轮人工核查 2 页：`tools/life/generator-strength.html` 与 `tools/life/date-add-subtract.html`；后者使用内存 DOM 桩，真实浏览器与其他页面未逐页覆盖。

## 2026-11-03 续查：年龄、日期差与 AA 分摊

### 留存优化（按页落点，非确认缺陷）
- `tools/life/age-calculator.html`：结果只有本地展示，无「年龄摘要复制」与里程碑倒数（18/30/60 岁、万天）。建议加一键复制/分享卡与下一里程碑倒计时，这是生日类页面的主要回流点。
- `tools/life/bill-splitter.html`：分摊结果不能直接转发，缺「每人一句催款文案」或多人群分享。建议生成按人分段的可复制文本（姓名 + 金额 + 合计），并允许选择余数承担者。
- `tools/life/date-diff.html`：工作日口径只排除周末，未处理法定节假日/调休。建议提供节假日库开关或自定义非工作日，并支持导出 `.ics`/复制区间说明。
- `tools/life/percentage-calculator.html`：四个子计算各自独立，无常用场景预设（折扣、涨幅、完成率）。建议加场景预设并在结果旁固定展示「计算式」，便于截图核对。

### 续查覆盖
- 新抽查 `tools/life/age-calculator.html`、`tools/life/percentage-calculator.html`、`tools/life/date-diff.html`、`tools/life/bill-splitter.html` 共 4 页，新增 6 条（0 条高优，4 条中优）与 4 条留存建议；为源码与数值推导，未做浏览器、移动端、线上或门禁验证。

## 2026-11-03 续查（并行批 F）

### 留存优化
- `tools/life/workday-calculator.html`：结果旁同时给出「含首尾/不含结束」两种口径并允许切换；内置 2026 国务院节假日与调休预设、导出 `.ics` 工期，减少手工维护日期。
- `tools/life/parking-fee.html`：按自然日明细表 + 「首时免费/半小时进位/夜间封顶」等规则预设，并在结果标明封顶是否生效，便于离场前截图核对。
- `tools/life/drinking-water-plan.html`：杯容量可选（200/250/300 ml）、计划一键复制与导出提醒，分段合计明确标注「与目标一致」，提升日常复用。
- `tools/life/zodiac-calculator.html`：同时展示农历日期与春节分界，提供「按春节/按立春」口径切换及生日分享卡，作为社交类查询的回流点。
- `tools/life/shoe-size-converter.html`：增加 Nike/Adidas 等品牌尺码预设与「脚长→国内码」常用对照表，结果保留半码并附「建议预留 5–10 mm」提示。
- `tools/life/world-clock.html`：城市搜索改为全量可搜、会议时段支持导出与各城市本地时间对照，修复无效时区后可作为会议排期入口。
- `tools/life/timestamp.html`：批量区支持逐行单位标注与「复制全部」、常用时间戳预设（今天/本周一/本月一号已在下方，可与批量联动），方便日志排查复盘。

### 续查覆盖
- 本轮新抽查 `tools/life/workday-calculator.html`、`tools/life/parking-fee.html`、`tools/life/drinking-water-plan.html`、`tools/life/zodiac-calculator.html`、`tools/life/shoe-size-converter.html`、`tools/life/world-clock.html`、`tools/life/timestamp.html` 共 7 页，新增 11 条（3 条高优、5 条中优、3 条低优）与 7 条留存建议。
- 证据均为源码阅读 + node 内存复算（含 `TZ=America/Los_Angeles` 时区快照与 `Intl.DateTimeFormat` 时区有效性校验）；未做浏览器、移动端、英文态、线上或门禁验证，涉及浏览器行为的结论均为源码推导。

## 2026-11-03 续查（并行批 I）

### 留存优化
- `tools/life/chinese-number.html`：结果区增加「简体 / 大写 / 人民币」逐项复制与交叉校验（三段结果必须对应同一数值），并提供小数、负数开关，避免用户误把截断结果当完整转换。
- `tools/life/roman-numeral.html`：拆解式改为与减法规则一致的「IV=4」形式，并附 1–3999 常用对照表与一键复制，提升教学/核对场景的复用率。
- `tools/life/birthday-paradox.html`：按当前总天数动态给出「达到 50%/90%/99% 所需人数」表与曲线，并提供分享文案（人数、概率、假设），这是该页主要传播点。
- `tools/life/daily-calorie-needs.html`：体脂率卡改为带公式与置信区间的估算（或直接移除），并在 TDEE 面板显式展示所用的 BMR 公式，避免跨面板口径不一致。
- `tools/life/ring-size-converter.html`：增加「周长→港码/美码/欧码」对照表、可打印指圈尺与「建议预留 0.5 码」提示；同时输出日本码/中国码，覆盖国内主流标注。
- `tools/life/bra-size-converter.html`：补姐妹码（如 75C↔80B）与「底围偏紧/罩杯偏满」的选码说明，并给出测量步骤图示，提升实际选购价值。
- `tools/life/candle-burn-time.html`：直径要么参与燃速模型、要么标注为「仅提示不影响估算」；增加按「每天 2/4/6 小时」的天数对照表与燃烧日历。
- `tools/life/clothing-size-converter.html`：增加品牌/版型预设与「净尺寸→最近码」推荐，结果区固定展示所用净尺寸与余量，减少跨境退换。

### 续查覆盖
- 本轮新抽查 `tools/life/chinese-number.html`、`tools/life/roman-numeral.html`、`tools/life/birthday-paradox.html`、`tools/life/daily-calorie-needs.html`、`tools/life/ring-size-converter.html`、`tools/life/bra-size-converter.html`、`tools/life/candle-burn-time.html`、`tools/life/clothing-size-converter.html` 共 8 页，新增 12 条（6 条高优、5 条中优、1 条低优）与 8 条留存建议。
- 证据均为源码阅读 + node 内存复算（复制页面纯函数与对照表在内存中执行，含边界/负数/超范围输入）；未做浏览器、移动端、英文态、线上或门禁验证，DOM 交互类结论（如清空后旧文案残留）为源码路径推导。

## 2026-11-03 续查（并行批 K）

> 范围：本轮实读 `tools/life/unit-converter.html`、`temperature-converter.html`、`data-unit-converter.html`、`base-convert.html`、`leap-year-checker.html`、`music-practice-timer.html`、`countdown-1.html`、`phone-lookup.html` 共 8 页。仅源码静态阅读 + node 内存复算，未开浏览器，未做英文态/移动端/门禁验证。

### LF-N30 油耗分类声明 reciprocal 却按乘法换算，整类双向结果错位（高，确认缺陷）
- 描述：fuel 表中 km/L、mpg(US)、mpg(UK) 标了 `reciprocal: true`（与 L/100km 成反比），但 `convertFrom` 两个分支都只做 `val × fromFactor ÷ toFactor`，从未读取该标记。反比单位必须以 `factor ÷ value` 折算到基准，因此整类换算与同页速查文案、参考值全部矛盾；gal/100mi 属比例型，混在同一张表里更易掩盖问题。
- 证据：`tools/life/unit-converter.html:675-679`（reciprocal 声明与比例型混排）、`:682-684`（速查文案）、`:774-777`、`:790-793`（只用 factor 乘除）。
- 复现：8 L/100km → mpg(US) 实际 `0.034011`（期望 `29.40`）；10 L/100km → km/L 实际 `0.1`（期望 `10`）；1 mpg(US) → km/L 实际 `2.35215`（期望 `0.425`）；29.4 mpg(US) → L/100km 实际 `6915.32`（期望 `8.0`）。
- 影响：`tools/life/unit-converter.html`；油耗是换算器最常用分类之一，除「值为 1」的巧合外所有结果错 1–3 个数量级，速查项「8 L/100km ≈ 29.4 mpg」点下去得到 0.034。
- 方案：按单位语义分组——反比单位先算 `base = factor / value`，比例型保持 `value × factor`；输出端反比单位用 `factor / base`；补 8 L/100km ↔ 29.4 mpg、10 L/100km ↔ 10 km/L 往返用例。

### LF-N31 功率分类 dBm 声明 special 但无换算实现，选中后结果静默清空（中，确认缺陷）
- 描述：power 的 `dbm` 只有 `special: 'dbm'`、没有 factor；`convertFrom` 仅对 `cat.special && currentCategory === 'temperature'` 走特殊路径，dBm 仍按 factor 乘除，得到 `undefined` 参与运算的 NaN，`formatNumber` 对非有限值返回空串，结果栏被清空且无任何提示。
- 证据：`tools/life/unit-converter.html:590`（dBm 声明）、`:771-777`（仅 temperature 特判）、`:799-800`（NaN → 空串）。
- 复现：功率分类 1 W → dBm 实际空白（期望 `30`）；1 dBm → W 实际空白（期望约 `1.259`）；导出/历史会记录空值。
- 影响：`tools/life/unit-converter.html`；射频、音响场景常用 dBm，用户只能看到空结果，无法判断是输入错误还是工具不支持。
- 方案：实现 `dBm → W: 10^((x−30)/10)`、`W → dBm: 30 + 10·log10(x)`；`x <= 0` 时提示「dBm 只对正功率有定义」；其它功率单位仍走 factor。

### LF-N32 能量速查引用不存在的 megajoule，点击抛 TypeError 且结果栏停留旧值（中，确认缺陷）
- 描述：能量速查「1 度电 = 3.6 MJ」的 `to: 'megajoule'` 不在 units 表中；`applyQuick` 不做存在性校验，直接把值写进 `<select>`，无效值使 `select.value` 变为空串，随后 `cat.units[''].factor` 抛 TypeError。此时 fromValue/fromUnit 已被改成 1 千瓦时，结果栏仍保留上一个分类的数值。
- 证据：`tools/life/unit-converter.html:569`（无效 to 单位）、`:555-566`（单位表无 megajoule）、`:730-736`（无校验写入 select）、`:774-775`。
- 复现：切到「能量」→ 点该速查项 → 控制台 `TypeError: Cannot read properties of undefined (reading 'factor')`，输入区显示 1 千瓦时，结果栏显示上一次（如长度分类）的旧数字。
- 影响：`tools/life/unit-converter.html`；速查是页面主推的一键换算入口，首次点击即报错，且界面呈现跨分类错行数据。
- 方案：改目标为 `kilojoule`（1 kWh = 3600 kJ）或补 megajoule 单位；`applyQuick` 先校验 `cat.units[q.from] && cat.units[q.to]`，缺失时提示并中止写入。

### LF-N33 数据分类 KB/KiB 并存且系数完全相同，同站两页口径不一（低，确认缺陷）
- 描述：data 分类同时定义 `kilobyte` 与 `kibibyte`，factor 均为 1024（MB/MiB、GB/GiB、TB/TiB 同样重复），下拉出现两个结果完全一致的选项，等于把 KB 当 KiB 用且无十进制模式；同站 `life/data-unit-converter` 默认 1024 但可切到 1000，两页对「1 KB」给出两个答案。
- 证据：`tools/life/unit-converter.html:507-508`、`:513`（重复系数）、`:518-521`（速查全部按 1024）；`tools/life/data-unit-converter.html:327`（默认 1024）、`:211`（参考表定义 KB 十进制 1000）。
- 复现：data 分类 1 MB → 选 KB 与选 KiB 都输出 `1,024`（期望 KiB 为 `976.56`，或明确声明 KB=1024 并删掉重复项）。
- 影响：`tools/life/unit-converter.html`；存储容量是最易产生纠纷的换算，用户无法从界面判断本页采用哪种口径。
- 方案：KB/MB 按 1000、KiB/MiB 按 1024；若坚持二进制口径，删除 KiB 系列并在分类说明中写明「本页 KB 采用 1024」。

### LF-N34 清空任一温标输入框会被立即回填默认值，无法留空重输（中，确认缺陷）
- 描述：五个 `fromXxx()` 都用 `parseFloat(...) || 默认值`（0 / 32 / 273.15 / 491.67 / 0），而 `updateAll` 又把五个输入框全部 `toFixed(2)` 回写。用户删除字段内容后，input 事件立刻按默认值计算并回填，字段永远无法为空；误清空还会静默得出 0°C 的全套结果。
- 证据：`tools/life/temperature-converter.html:442`、`:446`、`:451`、`:456`、`:462`（|| 默认值）、`:427-436`（updateAll 回写五框）。
- 复现：清空「华氏度」→ 该框立刻变回 `32.00`，摄氏度 `0.00`、开尔文 `273.15`（期望空值时不计算、保持空框并提示）。
- 影响：`tools/life/temperature-converter.html`；改数时常先全选删除，此时字段自己弹回默认值，用户以为输入被吞掉，且结果区短暂显示错误温度。
- 方案：解析前判空（`input.value.trim()===''` 时清空其余结果并 return），去掉 `||` 兜底；回写仅更新「非当前编辑框」或在 `change` 时统一格式化。

### LF-N35 低于绝对零度照常换算，页面自述的下限未校验（低，确认缺陷）
- 描述：页面说明写明「开尔文存在理论下限 0K（−273.15°C）」，但 K 输入 −10 仍照常输出 −283.15°C、−477.67°F、负兰氏与负列氏，无任何越界提示。
- 证据：`tools/life/temperature-converter.html:174-175`（说明）、`:450-454`（无校验）。
- 复现：开尔文输入 `-10` → 实际 `-283.15 °C / -477.67 °F`（期望提示「低于绝对零度」并拒绝换算）。
- 影响：`tools/life/temperature-converter.html`；物理上不可能的值被当成正常结果显示并允许复制/存档，教学场景会误导。
- 方案：在 `updateAll` 入口判 `k < 0`（即 `c < -273.15`），显示错误态并禁用复制；其余温标同步置空。

### LF-N36 从历史恢复时无参调用 setMode，换算卡全部变 ∞、模式按钮失焦（中，确认缺陷）
- 描述：历史恢复回调回填输入后调用 `setMode()` 不带参数，wrapper 把 `mode=undefined`；随后 `Math.pow(undefined, idx)` 全为 NaN，`formatNumber` 把 NaN 显示为 ∞，两个模式标签的 `toggle('active', m===…)` 也都不成立，页面呈现「无模式 + 全 ∞」。
- 证据：`tools/life/data-unit-converter.html:473-487`（回调，`:484` 为 `setMode();`）、`:329-334`（无参即写 undefined）、`:341`、`:346`（NaN → ∞）、`:379`。
- 复现：二进制模式输入 1 TB 换算一次生成历史 → 点该历史恢复 → 所有单位卡显示 `∞`、两个模式标签均无高亮（期望按记录时的模式恢复，且历史里也未保存 mode）。
- 影响：`tools/life/data-unit-converter.html`；历史恢复是页面核心功能之一，恢复后整页数据不可用，只能手动再点一次模式。
- 方案：`setMode(rec.mode || 1024)` 并把 mode 写入历史记录；`setMode` 入口兜底 `m = (m===1000||m===1024) ? m : 1024`。

### LF-N38 自定义进制允许 2–62，但 JS toString 只支持 2–36，超限直接抛 RangeError（中，确认缺陷）
- 描述：输入框 `min=2 max=62`、占位文写「2–62」，实现却直接 `Number.prototype.toString(customBase)`，规范只支持 2–36；37–62 抛 RangeError，且抛错时二/八/十/十六进制已写入、ASCII/Unicode 与自定义栏尚未更新，页面停在半更新状态。导出路径有同样缺陷。
- 证据：`tools/life/base-convert.html:198`（max=62）、`:329-330`（直接 toString）、`:333-350`（抛错后未执行的文本区）、`:383-384`（导出路径）。
- 复现：输入 255、自定义进制填 40 → 控制台 `RangeError: toString() radix argument must be between 2 and 36`；bin/oct/dec/hex 为 `11111111/377/255/FF`，自定义栏仍是上次的 `73`。
- 影响：`tools/life/base-convert.html`；UI 明确宣称支持到 62，用户按提示输入 40 就触发异常，且界面数据不同步。
- 方案：要么把上限改为 36 并在文案中说明，要么自行实现 2–62 的数字/字母映射（0-9a-zA-Z）再输出；解析与导出共用同一实现。

### LF-N39 parseInt 静默截断非法字符，非法的「部分合法」输入照常出数（中，确认缺陷）
- 描述：四种前缀解析都用 `parseInt`，只有整串完全无法解析才会 `isNaN` 置「错误」；带非法尾巴或中间夹非法字符时会被截断后正常换算，与页面「解析失败时各栏置『错误』」的承诺不符。
- 证据：`tools/life/base-convert.html:309-321`（parseInt 与 isNaN 判定）。
- 复现：`0b1012` → 实际 dec `5`、bin `101`（期望「错误」，末位 2 不属于二进制）；`12a` → 实际 `12`；`0x1G` → 实际 `1`。
- 影响：`tools/life/base-convert.html`；用户粘贴带空格/注释的代码常量时会得到少一位的错误结果，且无任何警示。
- 方案：按前缀选定合法字符集后整串正则校验（`^[01]+$` 等），不匹配直接置「错误」；再用 `Number()`/显式逐位累加替代 `parseInt`。

### LF-N40 查询范围允许负数/0/小数，倒序区间照常渲染（低，确认缺陷）
- 描述：范围用 `parseInt(...) || 10`，负数、0、空值都被静默兜底或透传；负数会得到 `start > end` 的倒序区间，标题仍是「2024 - 2019 年附近的闰年：无」；0 被当成 10。年份同样走 parseInt，`2024.5` 静默按 2024。
- 证据：`tools/life/leap-year-checker.html:264-265`（parseInt 与 `||10`）、`:279-284`（start=y、end=y+range−1、for 循环）。
- 复现：范围填 `-5` → 实际「2024 - 2019 年附近的闰年：无」（期望提示「范围须为正整数」）；范围填 `0` → 实际按 10 年；年份 `2024.5` → 实际按 2024。
- 影响：`tools/life/leap-year-checker.html`；错误输入得到看似正常的空结果，用户会以为该区间真的没有闰年。
- 方案：年份与范围统一 `Number()` + `Number.isInteger` 校验（范围 1–500），非法时清空结果并字段级提示；标题改为「从 y 起 N 年」以匹配实现。

### LF-N41 练习计时用 setInterval 递减，后台标签页会明显走慢（中，确认缺陷）
- 描述：计时靠 `setInterval(...,1000)` 每次 `remaining--`，不读墙钟；后台标签页/系统休眠时定时器被节流，剩余秒数只按回调次数减少，5 分钟阶段可能走十几分钟，阶段切换与完成提示同步延后。
- 证据：`tools/life/music-practice-timer.html:285-293`（setInterval 递减与阶段切换）、`:271-278`（显示直接取 remaining）。
- 复现：设 5 分钟阶段 → 开始 → 切到其它标签 5 分钟再回来：实际剩余仍接近 `05:00`（仅少量回调），期望接近 `00:00` 或已完成（源码推演，未开浏览器）。
- 影响：`tools/life/music-practice-timer.html`；练琴时常把页面放后台听节拍/看谱，计时失真会让阶段时长与总练习量全部不准。
- 方案：记录 `endTs = Date.now() + remaining*1000`，每 tick 用 `remaining = Math.ceil((endTs-Date.now())/1000)` 重算；或用递归 setTimeout + 墙钟校正。

### LF-N42 新增阶段接受负时长，列表显示「-05:00」并在一秒内被跳过（低，确认缺陷）
- 描述：`addSegment` 用 `parseInt(prompt) || 5`，负数非 falsy 直接透传；负时长阶段在列表显示「-05:00」，开始后首次 tick 即因 `remaining <= 0` 被判为阶段结束，立刻跳段并播提示音。
- 证据：`tools/life/music-practice-timer.html:265-268`（parseInt 与 push）、`:270`（fmt 负数）、`:287-290`（<=0 跳段）。
- 复现：新增阶段时长 `-5` → 列表 `-05:00`；点开始约 1 秒内跳到下一阶段并响提示音（期望拒绝负值并提示）。
- 影响：`tools/life/music-practice-timer.html`；手滑输入负号会得到无法执行的阶段，且提示音被误触发。
- 方案：`const mins = Number(prompt(...)); if(!Number.isInteger(mins) || mins<=0) return showToast('时长须为正整数')`；`fmt` 对负数兜底。

### LF-N43 历史在加载预设/重置时就写记录，英文标签仍是中文（低，确认缺陷）
- 描述：`__tbn` 在每次 `loadTemplate` 后被调用并记录一次「练习计划总时长(秒)」，因此点预设、点重置都会写入历史，即使从未开始练习；历史标题「练习成绩历史（练习计划总时长(秒)）」把「成绩」与「计划时长」混为一谈。英文态 `LBL` 两个分支字符串完全相同，仍显示中文。
- 证据：`tools/life/music-practice-timer.html:298-313`（`:303` 双语同串、`:313` 记录）、`:328`（loadTemplate wrapper）、`:296`（reset 也调 loadTemplate）。
- 复现：依次点 3 个预设再点重置 → 历史新增 4 条计划时长，实际练习 0 次；`?lang=en-US` 时该标签仍为中文。
- 影响：`tools/life/music-practice-timer.html`；历史被配置操作污染，无法反映真实练习量，跨语言用户看到混排文案。
- 方案：仅在练习真正开始/结束（或阶段完成）时 `record`，记录「实际练习秒数」而非计划总时长；`LBL` 英文分支改为 `Practice plan total (s)` 或直接记录实际时长。

### LF-N44 倒计时到点判定挂在 rAF 上，标签页隐藏时不响铃且延迟触发（中，确认缺陷）
- 描述：到点判断只在 `tick()` 内做，而 tick 由 `requestAnimationFrame` 续排；标签页隐藏时 rAF 停止，`elapsed >= target` 永远不会被检查，`onFinish()`（提示音与完成态）要等用户切回标签才补触发。显示值本身用墙钟 `curElapsed()`，切回不会算错，但提醒会迟到。
- 证据：`tools/life/countdown-1.html:261-268`（`:265-266` 到点分支、`:268` rAF 续排）、`:263`（墙钟取值）。
- 复现：设 5 分钟 → 开始 → 切到其它标签 5 分钟：到点时无任何提示音/文案；切回后才弹完成态并响铃（期望按时提醒）。
- 影响：`tools/life/countdown-1.html`；倒计时的典型用法就是「开始后切走做别的事」，此时提醒失效，工具的核心价值丢失。
- 方案：到点提醒用独立 `setTimeout(target - elapsed)`（配合 Audio 解锁）触发，rAF 只负责渲染；并在 `visibilitychange`/`pagehide` 时用墙钟补判一次。

### LF-N45 目标为 0 秒时点开始立即「完成」并响铃，1e3 分钟被截成 1 分钟（低，确认缺陷）
- 描述：`applyTarget` 用 `parseInt` 只做 clamp 不写回：分钟 0/秒 0 → target=0，点开始后 tick 首次即 `0 >= 0` 判定完成，立刻响铃；`1e3` 被 parseInt 成 1 分钟；秒填 60 被 clamp 成 59 但输入框仍显示 60。0 秒目标还会随 `save()` 持久化，刷新后仍是完成态。
- 证据：`tools/life/countdown-1.html:232-239`（parseInt + clamp 无回写）、`:246-248`、`:265-266`、`:202-204`（load 时按 target 恢复完成态）。
- 复现：0 分 0 秒 → 点开始实际立即 `00:00.00` 完成并响铃（期望提示至少 1 秒）；分钟填 `1e3` → 实际 1 分钟；秒填 `60` → 实际按 59 秒计时。
- 影响：`tools/life/countdown-1.html`；空目标被当成一次「完成」并播放提示音，容易误判；数字输入被静默改写，界面值与实际目标不一致。
- 方案：`Number()` 解析 + 整数校验，最小值 1 秒；clamp 后把规范值写回输入框，避免显示值与 target 不一致。

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 10 页（`tools/life/length-converter.html`、`weight-converter.html`、`volume-converter.html`、`area-converter.html`、`speed-converter.html`、`time-converter.html`、`event-countdown.html`、`holiday-calendar.html`、`age-in-days.html`、`date-difference-calculator.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### LF-N51 精确年龄借位不足，显示负数天数（中，确认缺陷）
- 描述：`d < 0` 时只向上一月借一次天数，且借的是「上一自然月天数」；当出生日大于上月天数（29/30/31 日生日跨越 2 月或 4 月）时借完仍为负，且无后续修正。
- 证据：`tools/life/age-in-days.html:279-290`（y/m/d 分解）、`:301`（输出「精确年龄」）
- 复现：出生 2000-01-31，把系统日期设为 2026-03-01 → 实际 `26 岁 1 月 -2 天`（期望 `26 岁 1 月 1 天` 或 0 月 28 天口径）；出生 2001-01-31 同日同样得 `-2 天`。
- 影响：`tools/life/age-in-days.html`；每月头几天、生日为 29/30/31 的用户会看到负数天数，而「精确年龄」是本页主结果。
- 方案：借位后 `while(d < 0){ m--; d += new Date(nowY, nowM-1, 0).getDate(); }`，或改为「从出生日逐月推进直到不超过今天」的算法；补 31 日生日、闰年 2/29 用例。

### LF-N52 生日当天把「下一个生日」算成 365/366 天后（中，确认缺陷）
- 描述：`if(next < now)` 用含时分秒的 `now` 比较「今年生日 00:00」，生日当天该条件必然成立，直接跳到明年；再用 `Math.ceil` 取整得到 365（闰年后 366）。
- 证据：`tools/life/age-in-days.html:292-294`
- 复现：生日 11-04、当天 2026-11-04 10:00 → 实际「距离下一个生日：365 天」（期望「今天生日」或 0 天）。与 LF-N5（age-calculator 生日当天 `nextAge+1`）同源，但页面与文案不同。
- 影响：`tools/life/age-in-days.html`；生日当天正是查询高峰，结果与事实相反。
- 方案：与「今日 00:00」比较（`if(next <= todayMidnight) next.setFullYear(+1)`），相等时走「今天生日」分支；补当天/前一天/闰日用例。

### LF-N53 月度「工作日」重复扣减周末假期且忽略调休（中，确认缺陷）
- 描述：月度信息卡用 `workdays = totalDays - weekends - holidays`，把落在周六/日的节假日又扣了一遍；也没有任何调休补班（周末上班）数据，工作日系统性偏少。
- 证据：`tools/life/holiday-calendar.html:860-865`（公式）、`:819-821`（holidays/weekends 仅按标记累加）
- 复现：2026 年 2 月 → 实际 `28-8-7 = 13` 天（期望 15 天：20 个工作日 − 2/16-2/20 五个工作日假期）；2025 年 10 月 → 实际 15 天（期望 17 天：23 个工作日 − 10/1-10/3、10/6-10/8 六个工作日假期）。
- 影响：`tools/life/holiday-calendar.html`；日历顶部统计是排期/请假常用信息，每月少 1-3 天。
- 方案：逐日遍历当月，节假日不计、否则按 `isWeekend` 判定；另建补班日集合把对应周末强制计入工作日。

### LF-N54 2027 年春节整体提前一天，与站内倒计时页冲突（中，确认数据缺陷）
- 描述：`holidayData` 把 2027 年春节假期从 2 月 5 日开始，而 2027 年正月初一为 2 月 6 日（2/5 是除夕）；同站 `event-countdown` 的 `lunarDates[2027].spring` 也是 `[2,6]`。
- 证据：`tools/life/holiday-calendar.html:579-585`；对照 `tools/life/event-countdown.html:283`
- 复现：翻到 2027 年 2 月 → 2 月 5 日与 2 月 6 日都标「春节」（期望 2/6 起为春节，2/5 标除夕或不标）。
- 影响：`tools/life/holiday-calendar.html`；跨年请假/返乡日期错一天，且与站内另一页自相矛盾。
- 方案：2027 春节数据改为 2/6 起并按国务院安排补足天数；除夕单列 `type:'other'`。

### LF-N55 年初农历栏整段空白（低，确认缺陷）
- 描述：`getLunarDate` 找不到「≤ 当日」的农历月时回退取上一年数组的最后一项（腊月），但该腊月起始日落在当年 1 月、晚于被查日期，`diffDays < 0` 直接返回空串；真正的上一农历月（冬月）从未被使用。
- 证据：`tools/life/holiday-calendar.html:690-720`（`:703-712` 回退、`:716` 越界返回）
- 复现：2026-01-05 → 农历栏空白（期望「冬月十七」）；2027-01-03 → 空白（期望「冬月廿五」）；2024-01-10 → 空白（`lunarInfo` 无 2023 年数据）。
- 影响：`tools/life/holiday-calendar.html`；每年元月前 1-3 周日历农历列留白，用户会以为数据缺失。
- 方案：回退时取上一年倒数第二项并按跨年天数计算；无覆盖年份显示「农历数据未覆盖」而非空白。

### LF-N56 清明固定为 4 月 5 日，多年倒数多一天（中，确认缺陷）
- 描述：清明节写死 `new Date(y,3,5)`，但清明是节气，公历日期逐年为 4/4 或 4/5；本页说明也写「4 月 4-5 日」。
- 证据：`tools/life/event-countdown.html:309`（写死）、`:180`（说明）；对照 `tools/life/holiday-calendar.html:613`、`:620`（2024/2025 为 4/4）、`:627`、`:634`（2026/2027 为 4/5）
- 复现：2025-03-20 查看列表 → 实际「清明节 2025年4月5日」（期望 4 月 4 日，倒数少 1 天）；2024 年同理。
- 影响：`tools/life/event-countdown.html`；约一半年份清明倒数差 1 天，且与站内日历页数据冲突。
- 方案：内置逐年清明日期表（2024-2030）或复用节气数据；查不到年份时隐藏该条或标注「按 4/5 估算」。

### LF-N57 「包含周末」勾选语义与说明相反，取消勾选后周末天数归 0（中，确认缺陷）
- 描述：`workdays = includeWeekends ? countWorkdays(start,end) : days`，与公式说明「勾选『包含周末』时按自然日计数，否则扣减落在周六周日的天数」正好相反；默认勾选时输出扣周末的工作日，取消勾选后「工作日」变成总天数、「周末天数」变成 0。
- 证据：`tools/life/date-difference-calculator.html:457-458`、`:190`（说明）、`:204`（默认 `checked`）
- 复现：2026-01-01 → 2026-01-31，取消勾选「包含周末」→ 实际「工作日 31 / 周末 0」（期望 工作日 22 / 周末 9）；勾选时得到 22/9。与 LF-N1（date-diff.html）同型的「周末天数恒 0」，但此处还叠加了说明与实现的反转。
- 影响：`tools/life/date-difference-calculator.html`；统计加班/请假时口径被反转且无任何提示。
- 方案：工作日恒按排除周末的口径计算，周末恒为 `days - workdays`；若保留「包含周末」开关，应只影响总天数统计并同步改说明。

### LF-N58 「设为今天」/默认生日用 toISOString，早 8 点前得到昨天（低，确认缺陷）
- 描述：两页都用 `new Date().toISOString().split('T')[0]` 取「今天」，`toISOString` 走 UTC；东八区 00:00-07:59 时 UTC 仍是前一天，写入的是昨天。
- 证据：`tools/life/date-difference-calculator.html:409-413`、`tools/life/age-in-days.html:251-254`
- 复现：中国时区 2026-11-04 07:00 点「开始设为今天」→ 填入 `2026-11-03`（期望 `2026-11-04`）；age-in-days 打开时的默认生日同样早一天。
- 影响：`tools/life/date-difference-calculator.html`、`tools/life/age-in-days.html`；早晨使用时「今天」按钮给出错误日期，并直接带入日期差/生日计算（与 LF-N8 的 UTC 解析同源，但此处发生在当前日期而非输入解析）。
- 方案：改用本地日期拼装（`getFullYear/getMonth/getDate` + 补零），两页共用同一 helper。

### LF-N60 「月」系数与页面参照说明相差约一天（低，确认缺陷）
- 描述：实现与公式区均为 `month: 2629800`（30.4375 天 = 365.25/12），但页面底部仿实物参照的 FACTS 写「『月』取平均朔望月 29.53 天」，两种口径差 0.9 天。
- 证据：`tools/life/time-converter.html:279`、`:149`、`:530`
- 复现：1 月 → 实际 30.4375 天；同页 FACTS 声称 29.53 天（对应 2551392 s，而非 2629800 s）。
- 影响：`tools/life/time-converter.html`；用户按参照说明复核会得出与结果不一致的结论，月子/产假类场景按 29.53 天理解会少算约 1 天。
- 方案：FACTS 改为「月按 365.25/12 = 30.4375 天」，或增加「农历月（29.53 天）」切换并同步系数。

### LF-N61 深度解析「1 杯≈240 mL」与换算系数 236.59 mL 不一致（低，确认缺陷）
- 描述：换算系数 `cup: 236.5882365`（美制杯），深度解析示例却写「1 杯≈240 mL」，且页面没有「美制杯 / 公制杯」切换。
- 证据：`tools/life/volume-converter.html:281`（系数）、`:223`（示例）
- 复现：2 杯 → 实际 `473.176 mL`；按示例 240 mL/杯应约 480 mL（差约 7 mL）。
- 影响：`tools/life/volume-converter.html`；烘焙按示例估算会偏少，多杯累计误差扩大，用户无法判断本页采用哪种杯。
- 方案：统一按 236.588 mL 并标注「美制杯（US cup）」，或提供 240/250 mL 量杯选项。

- 本轮实读 10 页：`tools/life/length-converter.html`、`weight-converter.html`、`volume-converter.html`、`area-converter.html`、`speed-converter.html`、`time-converter.html`、`event-countdown.html`、`holiday-calendar.html`、`age-in-days.html`、`date-difference-calculator.html`；新增 13 条（高 1 / 中 7 / 低 5）；其中 `weight-converter.html`、`area-converter.html` 通读换算核心后未发现确认缺陷。未覆盖：`date-add-subtract.html`（已有条目）、`countdown-2/timer/countdown.html`、`analysis-23/74/80`、`analysis-cost-*`、`assessor-target`、`color-name-finder`、`cycle-*`、`detector-checker-strength`、`generator-price`、`generator-random-1`、`number-to-chinese`、`recommender-8`、`reminder-cycle`、`report-profit`、`stats-13`、`concentration/energy/frequency/magnet/pressure/radiation/data-rate/flow-rate/density-converter` 等。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（`tools/life/number-to-chinese.html`、`tools/life/data-rate-converter.html`、`tools/life/report-profit.html`、`tools/life/frequency-converter.html`、`tools/life/energy-converter.html`、`tools/life/power-converter.html`、`tools/life/flow-rate-converter.html`、`tools/life/concentration-converter.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### LF-N64 未限制整数位数，17 位起输出字面「undefined」（中，确认缺陷）
- 描述：页面标注「最大支持 16 位整数 + 小数」，但输入正则不限长度，`BIG_UNITS_*` 只有 `['','万','亿','万亿']` 四级；17 位整数分成 5 组时索引 `bigUnits[4]` 为 `undefined`，直接拼进结果。
- 证据：`tools/life/number-to-chinese.html:180`（16 位声明）、`:343-344`（四级单位）、`:423-429`（按组数取单位）、`:350`（无长度校验）
- 复现：10000000000000000（17 位）→ 实际「一undefined」（期望提示「超出 16 位」或正确读作「一亿亿」）；100000000000000000（18 位）→ 实际「十undefined」。
- 影响：`tools/life/number-to-chinese.html`；超范围输入不拦截，结果区出现英文 `undefined`，与「最大支持 16 位」的承诺矛盾。
- 方案：转换前校验整数部分长度 ≤16，超限给出明确提示；或把单位表扩展到「亿亿」并同步文档。

### LF-N65 示例区写「10 → 一十」，实现输出「十」，同页对照表又写「十」（低，确认文案矛盾）
- 描述：`convertInt` 在结果以「一十」开头时无条件删掉「一」，因此 10 输出「十」；但页面「转换示例」第一条写「10 → 一十」，而下方数字对照表写「10 → 十」，同一页给出两种读法。
- 证据：`tools/life/number-to-chinese.html:230`（示例「一十」）、`:255`（对照表「十」）、`:431-434`（删除前导「一十」）
- 复现：输入 10 → 实际「十」（按示例区期望「一十」，按对照表则正确）。
- 影响：`tools/life/number-to-chinese.html`；不影响数值，但示例与对照表自相矛盾，用户无法判断哪种是规范读法。
- 方案：统一采用「十」并改示例为「10 → 十」，或保留「一十」并删除 `:431-434` 的截断逻辑；同步检查大写/繁体模式。

### LF-N66 「对应下载速度」按 1024² 折算，与页面 12.5 MB/s 基准相差 4.6%（中，确认缺陷）
- 描述：结果区下载速度用 `base / 8 / 1024 / 1024`，把 MB 当 MiB；而页面公式说明与深度解析均以十进制 100 Mbps = 12.5 MB/s 为基准（`base / 8 / 1e6`）。同一页对「MB/s」两套口径，且输出标签仍写 MB/s。
- 证据：`tools/life/data-rate-converter.html:304`（1024² 折算）、`:193`（「100 Mbps 理论下载速度 ≈ 12.5 MB/s」）、`:220`（示例「100 Mbps = 12.5 MB/s」）、`:20`（标题「区分十进制与二进制单位」）
- 复现：选 100 Mbps → 实际「对应下载速度：11.92092896 MB/s」（期望 12.5 MB/s）；1000 Mbps → 实际 119.2092896（期望 125）；8000 kbps → 实际 0.9536743164（期望 1）。
- 影响：`tools/life/data-rate-converter.html`；宽带测速对照时结果系统性偏低约 4.6%，用户会误判带宽不达标，且与页面自带基准直接冲突。
- 方案：统一用 `base / 8 / 1e6` 并标注 MB/s；若要保留二进制口径，则改用 `MiB/s` 标签并同步改写页面全部 12.5 MB/s 示例。

### LF-N67 回款率只写 `max=100` 不校验，150% 时出现「未回款 -92500 元」（中，确认缺陷）
- 描述：`recv` 输入框仅靠 HTML `max="100"`，JS 计算不做范围校验；`inflow = rev * recv / 100`、`arrear = rev - inflow` 直接使用越界值。手输 150 或负数都照常出报表，现金流入甚至会超过营业收入。
- 证据：`tools/life/report-profit.html:152`（`min="0" max="100"` 仅声明）、`:253-256`（无校验直接乘除）、`:243`（`num` 把空/非数静默当 0）
- 复现：营业收入 185000、进货 96000、人工 38000、房租 15000、杂费 7000、回款率 150%、期初 50000 → 实际「现金流入 277500 元、未回款 -92500 元、期末现金 171500 元」（期望回款率限制在 0–100% 或提示「回款率不能超过 100%」）。负数回款率同理得到负流入。
- 影响：`tools/life/report-profit.html`；财务工具出现负「未回款」和高于营收的现金流入，结论完全失真，且无任何越界提示。
- 方案：`calc()` 内校验 `0 <= recv <= 100`，越界时在结果区提示并停止计算；`num` 对空值区分「未填」而非静默 0。

### LF-N68 公式与 FAQ 承诺周期 T=1/f，结果区没有任何周期输出（低，确认缺陷）
- 描述：公式区写明「周期与频率互为倒数 T = 1 ÷ f」并给出「3000 rpm = 50 Hz，对应周期 20 ms」，FAQ 也重复该关系；但结果只遍历 `factors` 输出 Hz/kHz/MHz/GHz/rpm，没有 T 或毫秒字段。
- 证据：`tools/life/frequency-converter.html:157`（公式与 20 ms 示例）、`:224-225`（FAQ 重复）、`:298-305`（结果仅单位换算）
- 复现：选 3000 rpm → 实际只显示「基准 3000 rpm = 50 Hz」及各频率单位（期望另显示「周期 20 ms」）；50 Hz 同理应显示 20 ms。
- 影响：`tools/life/frequency-converter.html`；页面把周期作为核心卖点写进公式和 FAQ，用户按示例核对时找不到对应结果。
- 方案：在结果区增加一行 `周期：fmt(1000 / base) ms`（base 为 Hz），零/负值时提示无效；或从公式与 FAQ 中删除周期承诺。

### LF-N69 meta 与英文简介宣称「电子伏特」，单位表实际没有 eV（低，确认缺陷）
- 描述：页面 description/og/twitter 与英文简介都写支持 electronvolt，但下拉只有 J/kJ/cal/kcal/Wh/kWh/BTU 七项，`factors` 也没有 eV 键，用户无法进行 eV 换算。
- 证据：`tools/life/energy-converter.html:10`（meta「电子伏特」）、`:159`（英文简介 `electronvolt`）、`:168-176`（下拉无 eV）、`:276-284`（系数表无 eV）
- 复现：输入 1 kWh → 实际只得到 3.6e6 J 等七项，无法选 eV；期望至少能得 1 eV = 1.602176634e-19 J 或页面不宣称支持。
- 影响：`tools/life/energy-converter.html`；物理习题/半导体场景的用户按搜索词进入后找不到所需单位，属文案与功能不符。
- 方案：增加 `eV: 1.602176634e-19` 与对应选项（并补 keV/MeV），或删除 meta/英文简介中的 electronvolt。

### LF-N70 英文简介宣称「BTU per hour」，实际只有 BTU 没有 BTU/h（低，确认缺陷）
- 描述：英文简介写 `BTU per hour`，但下拉与系数只有功率单位 W/kW/MW/PS/hp，BTU/h 未实现；中文简介与公式也未提 BTU/h。
- 证据：`tools/life/power-converter.html:159`（英文简介 BTU per hour）、`:168-175`（下拉五项）、`:273-279`（系数表）
- 复现：选 1 kW → 实际得到 1000 W、1.3596 PS 等，无法得到 3412.142 BTU/h（期望提供该项或删除宣称）。
- 影响：`tools/life/power-converter.html`；空调/制冷场景常用 BTU/h，英文用户会误以为可直接换算。
- 方案：增加 `BTUh: 0.293072222` 与选项（1 BTU/h ≈ 0.293 W），或删除英文简介中的 BTU per hour。

### LF-N71 英文简介与引据表宣称质量流量 kg/s，实际只有体积流量且无密度输入（低，确认缺陷）
- 描述：英文简介写 `volumetric and mass flow rates ... kg/s`，公式引据表也写「质量流量 = 体积流量 × 密度」，但下拉只有 L/s、L/min、m³/h、m³/s、gpm、cfm 六个体积单位，页面没有密度输入，无法计算 kg/s。
- 证据：`tools/life/flow-rate-converter.html:159`（英文简介 kg/s）、`:250`（引据表质量流量公式）、`:168-175`（下拉六项体积单位）、`:274-281`（系数表）
- 复现：默认 1 L/min → 实际只输出 0.01666666667 L/s 等体积单位（期望若宣称质量流量，应能输入密度并输出 kg/s，例如水 1 kg/L 时 1 L/min = 0.01667 kg/s）。
- 影响：`tools/life/flow-rate-converter.html`；需要质量流量的用户无法完成换算，且引据表公式与界面能力不一致。
- 方案：删除 mass flow/kg/s 表述，或增加「介质密度」输入并按 `kg/s = L/s × kg/L` 输出一行质量流量。

### LF-N72 meta 与正文宣称 mol/L、g/L 及按密度换算，实际只有 ppm 质量比（低，确认缺陷）
- 描述：meta description 写「在 ppm、mg/L、百分比与摩尔浓度间换算，依据溶液密度处理水溶液情形」，英文简介与深度解析也列 mol/L、g/L；但下拉只有 ppm/ppb/ppt/%/mg/L/μg/L，没有摩尔浓度或 g/L，也没有密度/摩尔质量输入。
- 证据：`tools/life/concentration-converter.html:10`（meta 摩尔浓度/密度）、`:162`（英文简介 mol/L、g/L）、`:508`（深度解析 mol/L、g/L 需密度或摩尔质量）、`:171-178`（下拉六项）、`:277-284`（系数表）
- 复现：输入 1% → 实际得 10000 ppm、10000 mg/L 等质量比（期望若支持 mol/L，应能按溶质摩尔质量换算，如 1 mol/L NaCl ≈ 58.44 g/L）；界面无 mol/L、g/L 选项，也无密度输入。
- 影响：`tools/life/concentration-converter.html`；实验配比/水质检测用户按 meta 搜索进入后无法做摩尔浓度换算，文案承诺超出实现。
- 方案：删除 mol/L、g/L 与「按密度」表述，明确「稀水溶液质量浓度近似」；或增加摩尔质量/密度输入并实现 mol/L、g/L 两项。

- 本轮实读 8 页：`tools/life/number-to-chinese.html`、`data-rate-converter.html`、`report-profit.html`、`frequency-converter.html`、`energy-converter.html`、`power-converter.html`、`flow-rate-converter.html`、`concentration-converter.html`；新增 11 条（高 1 / 中 4 / 低 6）。另抽读 `pressure-converter.html`、`angle-converter.html`、`density-converter.html` 做同类换算模板比对，未计入本轮条目。未覆盖：`analysis-23/74/80`、`analysis-cost-9/10`、`angle-converter`、`assessor-target`、`countdown`、`countdown-2`、`countdown-timer`、`cycle-4`、`cycle-pruning-lawn`、`density-converter`、`detector-checker-strength`、`generator-price`、`generator-random-1`、`magnet-converter`、`pressure-converter`、`radiation-converter`、`recommender-8`、`reminder-cycle`、`stats-13` 等。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 页（`tools/life/detector-checker-strength.html`、`countdown-timer.html`、`countdown-2.html`、`color-name-finder.html`、`generator-random-1.html`、`cycle-4.html`、`reminder-cycle.html`、`cycle-pruning-lawn.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### LF-N79 自定义事件用 `Math.ceil` 判天数，当天与已过事件均误报（中，确认缺陷）
- 描述：`days = Math.ceil(diff / 86400000)` 以「剩余毫秒」向上取整，导致同一天内剩余数小时被算成「还有 1 天」；已过不足 24 小时得 `-0`，`days === 0` 分支命中，显示「就是今天！🎉」。
- 证据：`tools/life/countdown-timer.html:486-493`（`const days = Math.ceil(...)`、`days > 0 / === 0 / else` 三分支）
- 复现：现在 00:05、事件今天 23:59 → 实际「还有 1 天」（期望「就是今天」）；现在 15:00、事件今天 13:00（已过 2 小时）→ 实际「就是今天！🎉」（期望「已过」）。
- 影响：`tools/life/countdown-timer.html` 自定义事件区；当天提醒与刚过期事件的状态互相颠倒。
- 方案：先按本地日历日比较判断「今天/未来/过去」，需要精确到小时时单独显示时分；对 `-0` 与负数统一走「已过」。

### LF-N80 每年纪念日「第 N 个周年」按当前年份算，目标已滚到明年时少 1（中，确认缺陷）
- 描述：`calcTarget` 对每年重复项会把已过的今年日期滚到明年并返回 `years = now.getFullYear() - 起始年`；但 `render` 里的「第 N 个周年」又用同一个「当前年份」差，没有用滚动后的目标年，跨过纪念日之后显示的就是「下一年的周年数」。
- 证据：`tools/life/countdown-2.html:204-214`（`calcTarget`，`:210` 的 `years` 用 `now.getFullYear()`）、`:283-284`（`yr=now.getFullYear()-…` 后拼「第 N 个周年」）
- 复现：添加 `2000-05-20` 每年提醒，今天 2026-11-04 → 实际目标 `2027-05-20`，副标题「第 26 个周年」；期望 2027 年是第 27 个周年。
- 影响：`tools/life/countdown-2.html`；纪念日/生日跨过当年日期后，周年序号整整少 1，且一年内长期显示错误。
- 方案：`yr = target.getFullYear() - base.getFullYear()`（或按已到达的周年计数），并在 `calcTarget` 里直接返回该值供渲染使用。

### LF-N81 2 月 29 日的每年纪念日被滚成 3 月 1 日（低，确认缺陷）
- 描述：每年重复用 `new Date(year, base.getMonth(), base.getDate())`，非闰年 2 月 29 日自动溢出到 3 月 1 日，页面照此展示并倒计时，未做闰年分支或提示。
- 证据：`tools/life/countdown-2.html:208-209`（构造与滚动均用 `base.getDate()`）、`:280`（`fmtDate(c.target)`）、`:291`（日期写入卡片）
- 复现：添加 `2000-02-29` 且勾选每年，今天 2026-11-04 → 实际「2027年3月1日」（2027 非闰年）；期望 2 月末（2/28 或明确提示「平年按 3/1 计」）。
- 影响：`tools/life/countdown-2.html`；闰日生日/纪念日在平年被推后一天，且日期与用户记忆不符。
- 方案：先判 `isLeapYear(year)`，平年取 2/28（或 3/1）并在副标题注明口径。

### LF-N84 meta/标题承诺「整数或小数」「是否允许重复」，实现只有整数且可重复（中，确认缺陷）
- 描述：meta description 与 `<title>` 都写「批量生成整数或小数」「支持自定义范围、数量与是否允许重复」，但界面只有 min/max/数量三个输入，`gen()` 用 `parseInt` 读范围并只调用 `randInt`（整数），也没有任何去重逻辑或「允许重复」开关。
- 证据：`tools/life/generator-random-1.html:10`（meta 小数/是否允许重复）、`:11`、`:13`（title/og:title）、`:208`（`randInt` 整数）、`:209-211`（`parseInt` 读 min/max）、`:125-127`（仅 3 个输入）
- 复现：min=0.5、max=1.5、数量=5 → 实际只出现 0 或 1（`parseInt` 截断），期望 0.5–1.5 的小数；连续生成 5 个 1–2 的整数可出现重复，界面无「不重复」选项（期望按 meta 承诺可控）。
- 影响：`tools/life/generator-random-1.html`；抽奖/抽样用户按「不重复」「小数」搜索进入后发现无法实现，属文案与实现不一致。
- 方案：增加「整数/小数」与「允许重复」两个开关；小数用 `parseFloat` + 精度控制，不重复用部分 Fisher-Yates 抽样并在数量超过范围时提示。

### LF-N85 三个场景预设直接整体替换用品列表，无确认导致已有记录丢失（中，确认缺陷）
- 描述：`applySupplyPreset` 对 `home/office/cafe` 都用 `supplies = sc.map(...)` 整体覆盖，既不询问也不合并；用户手工录入的用品与库存被静默清空（消耗日志仍保留，形成「有日志无用品」的孤儿记录）。
- 证据：`tools/life/cycle-4.html:477-496`（`:494` 的整表覆盖，函数内无 `confirm`）、`:182-184`（三个预设按钮直接 `onclick="applySupplyPreset(...)"`）
- 复现：先手动添加「洗洁精 3 瓶」「抽纸 6 提」→ 点「办公室」→ 实际原有两条消失，只剩洗手液/垃圾袋/消毒湿巾；期望提示「将覆盖当前列表，是否继续」或追加预设。
- 影响：`tools/life/cycle-4.html`；误点一次即丢失全部手工库存，且日志列表继续显示已删用品的名称。
- 方案：覆盖前 `confirm`，或改为「追加预设（同名跳过）」；删除用品时同步提供「仅删除用品/连日志一起删」选择。

## 2026-11-04 续查（并行批 O）

> 范围：`tools/life/analysis-23 / 74 / 80`、`analysis-cost-9 / 10`、`angle / density / magnet / pressure / radiation-converter` 共 10 页逐页通读；编号接续 LF-N88。仅静态源码审计，未做浏览器、英文态、移动端与门禁验证。

### LF-N88 日照间距页预设把「判定标准」标成低/中/高波动，0.5/3.0 直接推向全达标/全不达标（中，确认缺陷）
- 问题：预设文案与参数语义完全不符。三个预设实际写入的是「判定标准（日照间距系数）」`std`，却命名为「低波动 / 中波动 / 高波动」；0.5 明显低于住宅项目常见的 1.0 以上量级，3.0 又远高于任何实际标准。
- 证据：`tools/life/analysis-23.html:416-419`（预设 `std` 0.5/1.2/3.0）；`:213-214`（`std` 读取与兜底）；`:227`（`o.k>=std` 达标判定）；`:233-237`（结果展示）。
- 复现：示例 A 36m/30m=1.2000、B 50/45=1.1111、C 78/60=1.3000、D 27/24=1.1250。点「低波动」→ 达标 4 栋、100.00%；点「高波动」→ 达标 0 栋、0.00%、评价「间距普遍偏窄」。期望预设表达规范严格度（如 1.5/1.2/1.0），而非波动。
- 影响：`tools/life/analysis-23.html`；一键把结论推到两个极端，用户容易误以为 0.5/3.0 是规范限值。
- 方案：改为「严格 1.5 / 常规 1.2 / 宽松 1.0」，label 同步改「严格/常规/宽松」，并在预设旁注明依据（当地日照规划技术规定）。

### LF-N89 日照间距页不校验负间距，负系数仍进入均值/极差/达标统计（中，确认缺陷）
- 问题：只过滤 `h<=0`，间距 `d` 为 0 或负数时照样计算 `k=d/h`，负系数被当作有效样本参与全部统计与评价。
- 证据：`tools/life/analysis-23.html:219-221`（仅 `isNaN` 与 `h<=0`）；`:230-236`（均值、最高/最低、极差、达标率）。
- 复现：输入 `1栋,18,-22` → 实际「间距系数 -1.2222」「平均 -1.2222」「极差 0.0000」「达标 0 栋」「间距普遍偏窄」；期望拒绝该行并提示「间距需为正数」。
- 影响：`tools/life/analysis-23.html`；多栋混合时负值会显著拉低均值、放大极差，达标率失真。
- 方案：`d<=0` 与 `h<=0` 同过滤；对被跳过的行给出行号与原因；`p.length<3` 也提示「列数不足」。

**留存/优势（tools/life/analysis-23.html）**
- 保留批量粘贴（每行一栋）与 4 位小数的系数/极差输出，适合规划前期快速筛查。
- 把预设升级为「住宅/学校/旧城」常用规范阈值，并增加「一键导出判定表 CSV」。
- 已有历史快照可扩展为「本次 vs 上次达标率」对比，直接看方案调整效果。

### LF-N90 竞品分析页份额/价格/增速无范围校验，份额合计 150% 仍判「覆盖主要竞争面」（中，确认缺陷）
- 问题：只做 `isNaN` 校验，未限制份额 0–100%、价格/增速合理区间；份额合计任意值都进入 `ss>=80` 判定。
- 证据：`tools/life/analysis-74.html:214-215`（仅 isNaN）；`:228`（`ss>=80` 判「样本覆盖主要竞争面」）；`:231`（展示 `ss`）。
- 复现：输入 `A,10,150,5` → 实际「份额合计 150.00%」「样本说明：样本覆盖主要竞争面」；期望提示份额超过 100% 并拒绝该判定。
- 影响：`tools/life/analysis-74.html`；错误份额被解读为「市场覆盖完整」，竞品结论可信度失真。
- 方案：`sh` 限制 0–100、`ss` 设 95–105 容差；超限行标红并给「请核对份额」提示；价格与增速同样加区间校验。

### LF-N92 竞品分析页预设页签恒为空，且首屏自动写入一条历史（低，确认缺陷）
- 问题：`__analysis_74Presets` 为空实现，但工具栏仍渲染「预设」页签；同时 `calc()` 被包装后由 Boot 在加载时调用，默认示例被静默记入历史。
- 证据：`tools/life/analysis-74.html:395-397`（空预设）；`:398-402`（包装后 Boot 调 `calc()`）；`:362-388`（`__analysis_74Extras` 在无 `last` 时直接 `record`，初始 `skip=false` 见 `:299`）。
- 复现：首次打开页面 → 历史已有 1 条默认示例；点「预设」→ 空白面板。
- 影响：`tools/life/analysis-74.html`；历史被无关默认值污染，预设成为死入口。
- 方案：删除空预设页签或补 3 组行业示例；Boot 首次计算设 `skip` 标志，仅在用户输入/点击后记录。

**留存/优势（tools/life/analysis-74.html）**
- 保留「价格/份额/增速」四列批量粘贴与最低价、最高份额、最快增速三个即时结论。
- 增加份额合计校验与超限标红，避免把 150% 当成有效市场。
- 可补「竞品对比表导出」与「3C/餐饮/快消」示例预设，降低首次使用门槛。

### LF-N93 损耗分析页承诺「均值与波动」，实现没有任何标准差/波动输出（中，确认缺陷）
- 问题：meta、英文说明与深度解析均承诺统计「均值与波动 / mean and fluctuation」，但结果区只有加权平均损耗率、合计与高发环节，无标准差、无变异系数，图表也无数据源。
- 证据：`tools/life/analysis-80.html:10`（meta「统计损耗率、均值与波动」）；`:123`（英文「loss rate, mean and fluctuation」）；`:227-231`（仅合计/平均率/高发环节/明细表）；`:233`（渲染）。
- 复现：默认输入 `进货,5,100 / 货架,10,200 / 报损,3,50` → 实际「损耗合计 18.00｜平均损耗率 5.14%｜高发环节 货架」+ 明细表；无波动/标准差。
- 影响：`tools/life/analysis-80.html`；页面承诺的核心指标缺失，与深度解析「两车间标准差对比」无法对应。
- 方案：补总体/样本标准差（或变异系数）并按环节输出，明确公式分母；图表页签复用该序列。

### LF-N94 损耗分析页 FAQ 让用户「先换算为损耗率再贴入」，与「损耗量,应售量」入参口径冲突（中，确认缺陷）
- 问题：FAQ 称「页面统计的是你输入的数值本身；建议先把各项统一换算为损耗率再贴入」，但实现把第二列当损耗量、第三列当应售量，自动计算率；同时建议「在备注中说明」，页面却没有备注字段。
- 证据：`tools/life/analysis-80.html:166`（统计输入数值本身）、`:167`（备注）、`:221-224`（`rate=loss/base*100`）。
- 复现：按 FAQ 贴入 `进货,5%`（仅两列/率）→ 该行被跳过；贴入 `进货,5,100` 则输出 5.00%，证明第二列被当损耗量而非率。
- 影响：`tools/life/analysis-80.html`；用户按说明操作会得到空结果或错误口径。
- 方案：FAQ 改写为「每行填损耗量与应售量，工具自动换算率」；删除「备注」或新增备注列并写入导出。

**留存/优势（tools/life/analysis-80.html）**
- 保留「环节,损耗量,应售量」三列批量录入与高发环节定位，贴合门店盘点场景。
- 增加损耗率排序与高发环节高亮，先看最值得改的环节。
- 补齐标准差/环比并配 3 组零售、仓储示例预设，才能兑现「波动分析」定位。

### LF-N96 成本结构页简介承诺固定/变动拆解与降本优先级，实现仅合计/均值/极差/占比（中，确认缺陷）
- 问题：公式说明称「按固定/变动与单位/总口径拆解成本结构，输出可控项与降本优先级」，功能介绍列「成本结构拆解 / 降本优先级排序 / 预算偏差归因」，但代码只算合计、项均、最大/最小、极差、占比，没有分类字段、没有排序、没有预算数据入口。
- 证据：`tools/life/analysis-cost-9.html:126`（公式说明）；`:277-279`（简介与功能特点）；`:219-234`（calc 全部输出）。
- 复现：输入 `原料,42 / 人工,31 / 租金,15 / 水电,9` → 实际「合计 97.00｜项均 24.25｜最大项 原料(42.00)」、占比表、极差 33.00；无固定/变动标签、无优先级排序。
- 影响：`tools/life/analysis-cost-9.html`；用户找不到承诺的分类与排序，属明显名实不符。
- 方案：二选一——实现「固定/变动」字段并按占比降序输出「优先优化项」；或将文案改为「成本汇总与占比/极差分析」。

### LF-N97 成本结构页不校验负金额，合计为 0/负数时占比显示「—%」或负值（低，确认缺陷）
- 问题：金额只校验 `isNaN`，负成本被当有效项；`r.v/total*100` 在 total=0 时产生 `Infinity/NaN`，由字符串替换成「—%」，正负混合时出现负占比。
- 证据：`tools/life/analysis-cost-9.html:222-224`（仅 isNaN）；`:232`（`r.v/total*100`）；`:235`（`replace(/Infinity|NaN/g,'—')`）。
- 复现：`原料,100 / 退货,-50` → 合计 50.00，退货占比 `-100.00%`；`原料,10 / 人工,-10` → 合计 0.00，两行占比分别显示「—%」与「-—%」（`Infinity`/`-Infinity` 被全局替换），但页面仍显示「最大项 原料(10.00)」。
- 影响：`tools/life/analysis-cost-9.html`；负占比与破折号占比会被误读为正常结果，掩盖录入错误。
- 方案：金额限制 `>=0`（或把负数标为「冲减项」并单列口径）；合计 `<=0` 时直接提示「合计需为正数」，不渲染占比表。

**留存/优势（tools/life/analysis-cost-9.html）**
- 保留「成本项,金额」逐行粘贴与占比表，适合门店快速看成本结构。
- 增加「占比降序 + 固定/变动标签」，直接产出降本优先级。
- 已支持复制/导出，可再补「导出含占比与极差」的完整 CSV。

### LF-N98 预算偏差页 meta/简介承诺占比、均值、离散度与毛利/盈亏平衡/方案对比，实现只有预算差异（中，确认缺陷）
- 问题：meta 称「统计占比、均值与离散度」，工具简介称「计算总成本与毛利结构、测算盈亏平衡点，对比优化方案」，功能特点列「毛利结构拆解 / 盈亏平衡测算 / 方案对比模拟」，使用场景列「减租排班优化评估 / 低动销汰换测算」；实际页面只做预算 vs 实际的合计、总差异、执行率、最大超支项与逐项差异率。
- 证据：`tools/life/analysis-cost-10.html:10`（meta）；`:278-291`（简介/功能特点/场景）；`:217-237`（calc 全部输出）。
- 复现：输入 `进货,8000,7400 / 人工,5000,5600 / 租金,3000,2900` → 输出合计、差异 -100、执行率 99.38%、超支项人工；无占比、均值、离散度、毛利、盈亏平衡、方案对比。
- 影响：`tools/life/analysis-cost-10.html`；承诺功能大面积缺失，SEO 描述与实际页面不符。
- 方案：meta/简介改为「预算与实际差异分析」；若要保留承诺，需新增售价/成本字段算毛利、固定成本/毛利率算盈亏平衡，并提供两方案对比模块。

### LF-N100 角度换算页深度解析承诺「弧度换度分秒」，页面只有十进制度（中，确认缺陷）
- 问题：常见使用场景称「工程制图把程序输出的弧度换成度分秒，核对与图纸标注是否一致」，但页面仅输出 deg/rad/grad/rev 四种十进制度量，没有度分秒输入或输出。
- 证据：`tools/life/angle-converter.html:209`（场景文案）；`:277-293`（convert 仅遍历四种单位）；`:263-268`（`factors` 无 DMS）。
- 复现：输入 `1`、单位 rad → 实际输出 `57.29577951 °`（十进制度），没有 `57°17′44.8″`。
- 影响：`tools/life/angle-converter.html`；工程制图场景无法在本页完成，需另找工具。
- 方案：补 DMS 输出行（度/分/秒）与 DMS 输入解析（支持 `57°17′44.8″`），并与十进制度做双向校验。

### LF-N101 角度换算页「尺度感知」按绝对值匹配，-90° 仍显示「≈ 直角（90°）」（低，确认缺陷）
- 问题：参照物匹配用 `Math.abs(base)`，忽略符号；展示时输入带负号、参照却是正向，方向信息丢失。
- 证据：`tools/life/angle-converter.html:532-538`（`Math.abs(base)` 参与 log 距离）；`:545-547`（带符号输入 + 正参照展示）。
- 复现：输入 `-90`、单位「度」→ 实际「你的输入 ≈ -90 度」「💡 ≈ 直角 (90 度)」；期望「≈ -直角」或注明「按量值比较」。
- 影响：`tools/life/angle-converter.html`；旋转方向、坡度正负等场景会读到相反方向的参照，易误解。
- 方案：`base<0` 时参照文案加「反向」，或对角度类输入直接提示「负值表示反向」；参照匹配仍可按量值但显式标注。

**留存/优势（tools/life/angle-converter.html）**
- 保留「输入一个值、同时给出其余三种单位」的单屏批量输出，换算闭合（90°→100 grad、1 rad→57.29577951° 均正确）。
- 增加常用角度预设（30/45/60/90/180/360）与「度分秒」双向模式，直接覆盖制图场景。
- 补「复制全部结果」与有效数字位选择，便于写进图纸说明。

### LF-N102 密度/磁场换算页标题从句中截断，单位列表缺失（低，确认缺陷）
- 问题：`<title>` 与 `og:title` 以残缺的单位开头或直接省略列表，浏览器标签与搜索结果标题不通顺。
- 证据：`tools/life/density-converter.html:14`、`:20`（「密度换算器 - L 等常用密度单位间互相换算」）；`tools/life/magnet-converter.html:14`、`:20`（「磁场强度换算器 - 等磁学单位间互相换算」）。
- 复现：打开密度页 → 标签页显示「密度换算器 - L 等常用密度单位间互相换算」；期望「密度换算器 - kg/m³、g/cm³、lb/ft³ 等常用密度单位换算」。
- 影响：`tools/life/density-converter.html`、`tools/life/magnet-converter.html`；标题首词悬空、列表缺失，降低 SERP 点击率与可信度。
- 方案：两页标题改为完整单位枚举（密度 kg/m³、g/cm³、lb/ft³；磁场 A/m、Oe、T、G），并同步 og/twitter 标题。

### LF-N103 密度换算页接受负密度并原样输出（低，确认缺陷）
- 问题：只校验 `isNaN`，物理上不存在的负密度照样换算，结果区全是负值且无提示。
- 证据：`tools/life/density-converter.html:303-307`（仅 `isNaN`）；`:308-313`（基准与各单位的输出）。
- 复现：输入 `-1`、单位 g/cm³ → 实际「基准：-1 g/cm³ = -1000 kg/m³」，其余单位同为负；期望提示「密度需为正数」。
- 影响：`tools/life/density-converter.html`；负密度可被复制/导出进入下游计算，造成隐蔽错误。
- 方案：`v<=0` 拒绝（0 可提示「真空/无质量」），错误文案改为「请输入正数密度值」。

**留存/优势（tools/life/density-converter.html）**
- 保留 kg/m³ 基准 + 四种常用单位一次给全，1 g/cm³=1000 kg/m³、1 lb/ft³=16.018463 kg/m³ 复算闭合。
- 增加「水/空气/铝/铁」常用密度预设与目标单位选择（减少全量输出）。
- 补有效数字位选择与「复制全部」，方便实验记录。

**留存/优势（tools/life/magnet-converter.html）**
- 保留 H/B 两类单位一屏换算 + 真空下 B 对应值，物理实验场景实用。
- 增加「地磁/MRI/NdFeB」预设（页面已有雏形）与「H/B 分类切换」减少混读。
- 补「复制全部结果」与有效数字位选择。

**留存/优势（tools/life/pressure-converter.html）**
- 保留 Pa 基准 + kPa/MPa/bar/psi/atm/mmHg 七单位一屏输出，psi 与 bar 复算闭合（1 psi=6.894757293 kPa、2.4 bar=34.8094 psi）。
- 增加「表压/绝压」切换（轮胎 2.4 bar、血压 120 mmHg 都是表压），避免单位制混淆。
- 页面已有血压/轮胎/水深/地心等参照，可升级为一键预设并补「复制结果」。

### LF-N108 辐射换算页把「辐射权重因子」写成「组织权重因子」，且 Gy↔Sv 无条件并列（中，确认缺陷）
- 问题：深度解析与结果解读多处把 Sv 的换算写成「乘组织权重」，实际应为辐射权重因子 w_R；组织权重 w_T 用于有效剂量。另 Gy 与 Sv 在同一因子表内 1:1 互换，结果表对任意源单位都同时给出另一类量，未限定射线类型。
- 证据：`tools/life/radiation-converter.html:227`（「组织权重 1 时≈1 Sv」）、`:230-231`（「乘组织权重」「组织权重为 1」）、`:540`（「Sv = Gy×组织权重因子」）、`:279-291`（Gy/Sv 同表同值）、`:311-314`（全单位输出）、`:542`（仅文末一句「不同射线权重因子不同」）。
- 复现：输入 `2`、单位 Gy → 结果区仍直接并列 `2 Sv`；若按 α 粒子 w_R=20，应为 40 Sv。页面仅在文末免责声明提到「不同射线权重因子不同」，结果区无任何提示或射线类型选择。
- 影响：`tools/life/radiation-converter.html`；辐射防护核心概念错位（把 w_R 说成组织权重 w_T），用户可能把 Gy 与 Sv 当成可无条件 1:1 互换。
- 方案：改为「辐射权重因子 w_R」；Gy→Sv 增加射线类型选择（X/γ/β w_R=1、α=20、中子按能谱），或在结果显著位置提示「本页仅按 w_R=1 换算」。

**留存/优势（tools/life/radiation-converter.html）**
- 保留 Gy/rad/mGy 与 Sv/mSv/uSv/rem 两类七单位一屏换算，1 Gy=100 rad、1 rem=10 mSv 复算闭合。
- 增加「射线类型」选择后再给 Sv，真正区分吸收剂量与当量剂量。
- 预设胸片/CT/年本底/职业限值，并给「吸收剂量 / 当量剂量」不同配色，减少单位混读。

### LF-N109 密度/磁场/辐射三页 FAQ 宣称「支持复制」，工具栏实际没有复制按钮（低，确认缺陷）
- 问题：FAQ 与可见 opt-faq 写「结果会在结果区实时显示，支持复制与导出」，但工具栏只有「换算 / 导出明细 CSV / 清空」，无复制按钮，也无 `copyRes` 实现；FAQ 场景回答仍是通用套话「日常生活中的实用计算与小工具」。
- 证据：`tools/life/density-converter.html:106`、`:183`、`:503`；`tools/life/magnet-converter.html:106`、`:182`、`:506`；`tools/life/radiation-converter.html:106`、`:184`、`:531`。
- 复现：换算后查看工具栏 → 无「复制」；FAQ 却承诺支持复制。
- 影响：三页；承诺功能缺失，用户需手选结果文本；通用 FAQ 降低页面可信度。
- 方案：三页补「复制结果」按钮（`ToolBox.copyText(resultBox.innerText)`）或删掉「支持复制」；FAQ 场景回答改为密度/磁场/辐射的具体用途。

### LF-N110 本批 10 页「图表」页签恒空白：结果文本 parseFloat 永远 NaN（中，确认缺陷）
- 问题：历史记录把整段中文结果写进 `结果` 字段，图表渲染时对 `arr[j].d[rk]` 直接 `parseFloat`，因字符串以「基准：/楼栋数：/竞品数：/损耗合计：…」开头而恒为 `NaN`，`nums.length` 永远达不到 2，`TBKit.chart.line` 从不执行。
- 证据：`tools/life/analysis-23.html:373`、`analysis-74.html:354`、`analysis-80.html:360`、`analysis-cost-9.html:352`、`analysis-cost-10.html:363`、`angle-converter.html:366`、`density-converter.html:387-394`、`magnet-converter.html:392`、`pressure-converter.html:387`、`radiation-converter.html:390`（均为 `parseFloat(arr[j].d[rk])`，其中 density 还显式 `if(isFinite(v))` 过滤）。
- 复现：连续换算两次（如 1 Oe、2 Oe）后点「图表」→ 空白；node `parseFloat("基准：1 Oe = 79.5774715 A/m")` → `NaN`；`parseFloat("楼栋数：3 判定标准…")` 同样 `NaN`。期望画出两次结果趋势。
- 影响：10 页；整块图表功能形同虚设，历史记录也无法可视化。
- 方案：记录历史时另存结构化数值（如 `rec.__v = mean/base/avg`），图表读数值字段；或从结果文本用正则提取首个数值并做空态提示。

**留存/优势（tools/life/angle / density / magnet / pressure / radiation-converter）**
- 五个换算器均支持一次输入、全单位并列输出，便于批量比对；其中 90°→100 grad、1 g/cm³→1000 kg/m³、1 Gy→100 rad 等双向换算复算闭合。
- 页面已有常用预设（地磁/MRI、血压/轮胎、放疗剂量等），可补齐「一键预设 + 复制全部结果」。
- 图表页签修复后可升级为「多次换算趋势」，但换算类更建议做「单位对照表导出」而非趋势图。

- 本批实读 10 页：`tools/life/analysis-23.html`、`analysis-74.html`、`analysis-80.html`、`analysis-cost-9.html`、`analysis-cost-10.html`、`angle-converter.html`、`density-converter.html`、`magnet-converter.html`、`pressure-converter.html`、`radiation-converter.html`；新增 23 条（高 2 / 中 10 / 低 11）。未覆盖：`stats-13`、`assessor-target`、`generator-price`、`recommender-8`、`countdown` 及 life 下其余未列页面。未做浏览器交互、英文态 `?lang=en-US`、移动端与 `run_gates.py` 门禁验证；图表类结论基于源码与 node 复算。

## 2026-11-04 续查（并行批 P）

范围：仅实读下列 7 页源码（含内联 JS、公式框、deep-dive、FAQ），只读审计；未开浏览器、未做 `?lang=en-US`、移动端与 `run_gates.py` 门禁验证，换算类数值用 `node -e` 复算（含双向闭合）。编号自 LF-N111 起，接续 LF-N110。

### LF-N111 公式框称「同名买家合并计数」，FAQ 与代码却按行重复计（中，确认缺陷）
- 问题：同一页对「同名」给出互相矛盾的两种口径，结果区按行计数，公式框承诺的去重并不存在。
- 证据：`tools/life/stats-13.html:120`（「同名买家按同一人合并计数」）与 `:167`（FAQ「不能…同一姓名出现两次会算作两个条目」）；代码 `:221-239` 仅 `rows.push` 后 `people=rows.length`。
- 复现：名单 `张丽,2` + `张丽,3` → 实际「接龙人数 2 人 / 合计 5 份 / 340.00 元」；若按公式框合并应 1 人 5 份（人均 340 元）。
- 影响：`tools/life/stats-13.html`；接龙对账时人数与人均金额双口径，用户无法判断该信哪一条。
- 方案：二选一并同步三处文案——要么按姓名 `Map` 合并份数并保留「合并 N 条」提示，要么删掉公式框的去重承诺；补同名/同名不同份用例。

### LF-N112 描述承诺「占比、分档结果」，结果区与 SEO 简介承诺的漏斗/时段峰值均未实现（中，确认缺陷）
- 问题：meta、公式框标题级承诺的产出多于实际，结果区只有人数、份数、最多/最少、金额、人均；没有单项占比、没有分档金额，也没有 SEO 简介里的付款聚合、转化漏斗、时段峰值。
- 证据：`tools/life/stats-13.html:10`（「统计人数、占比与分档结果」）、`:120`（「分档金额 = 单价 × 数量；占比 = 单项数量 ÷ 总数量 × 100%」）、`:291-295`（「报名付款聚合 / 转化漏斗分层 / 时段峰值识别」）、`:245-251`（实际输出）。
- 复现：默认名单统计 → 结果区逐行只有 7 个指标，无任何「占比 %」或分档行。
- 影响：`tools/life/stats-13.html`；标题与摘要描述的卖点缺失，用户按 description 搜索进来后功能对不上。
- 方案：补逐人占比（份数/总份数）与分档金额两行（或分档表）；删除 SEO 简介中未实现的付款、漏斗、时段峰值措辞；同步 deep-dive。

### LF-N113 带单位写法被整体当成姓名、份数静默按 1 计；小数份数照收（低，确认缺陷）
- 问题：`张丽,2 箱` 这类从群接龙直接复制的写法，最后一个 token 不是数字，整行被当姓名且份数回落为 1；`1.5` 份也会原样进入合计。
- 证据：`tools/life/stats-13.html:222-234`（末位 `parseFloat` 失败即 `name=parts.join(' ')`；`qty<=0` 才回落 1；未限制整数）。
- 复现：`node` 复算 `张丽,2 箱` → 1 人 / 1 份 / 68.00 元（期望 2 份 / 136.00 元）；`张丽,1.5` → 合计 1.5 份。
- 影响：`tools/life/stats-13.html`；份数与金额少算且无任何提示，是接龙结算的高频输入形态。
- 方案：解析时剥离末位单位（箱/份/个/件）后再取数；份数限正整数并对小数、无法解析的尾项给出逐行提示；deep-dive 已有「多分隔符」口径需一并更新。

**留存建议（tools/life/stats-13.html）**
- 已支持全角逗号、顿号、分号、制表符与「只写姓名按 1 份」的容错，保持这套宽松解析并补逐行提示即可，不建议改严格模式。
- 建议把「下单最多/最少」升级为份数排行前 3 + 占比，正好补齐 LF-N112 的缺口，无需新增输入。
- 单价≤0 已有统一提示；可再补「合计已对齐」一行（份数×单价与逐人金额求和比对），提升对账可信度。

### LF-N114 可见性、人流、人口、竞争店数均无上下限夹取，可见性填 50 得 139.0/100（高，确认缺陷）
- 问题：输入框声明 `min=1 max=10`，但 `calc()` 只做 `+value||0`，未夹取也未校验；可见性 50 使该维度得 500 分，总分突破 100；负人流量得负分，总分可低于 0。
- 证据：`tools/life/assessor-target.html:137`（`min="1" max="10"`）、`:224-232`（`vs*10`、`Math.min(100,tr/100)` 对人流只封上限不封下限、总分直接加权）。
- 复现（node -e 复算同公式）：可见性 50 → `vis=500`、`total=139.0`，页面显示「139.0/100 优秀（强烈推荐）」；人流 -8000 → `ts=-80`、`total=28.0`；竞争 -2 → `comp=130`。
- 影响：`tools/life/assessor-target.html`；评分越界后评级仍按 ≥75 判「优秀」，选址结论完全失真，且用户看不出异常。
- 方案：统一 `clamp`——可见性夹到 1–10（或校验后提示）、人流/人口/竞争店数/租金限 ≥0 且设合理上限；总分再夹 0–100；补越界与空白用例（空白当前按 0 分静默参与）。

### LF-N115 「店铺面积」输入对评分毫无作用，与「六项打分」自述不符（中，确认缺陷）
- 问题：`shopArea` 被读取进变量后从未参与任何维度；改面积不改变任何分值。且页内自述互不一致：公式说明写「五维加权 / 等级 A/B/C」（`:129`），deep-dive 与 description 又写「六项（含面积）」；实现为五项四档（优秀/良好/一般/不佳）。
- 证据：`tools/life/assessor-target.html:136`（输入）、`:226`（`sa=` 赋值后无引用）、`:232`（总分仅五项权重）、`:129`（「五维加权…等级（A/B/C）」）、`:164`（「按人流、竞争、人口、租金、面积与可见性六项打分」）、`:10`（description 列入面积）、`:233`（四档评级）。
- 复现：面积 80 → 总分 76.0；改为 2000 → 仍 76.0（同输入其余项不变）。
- 影响：`tools/life/assessor-target.html`；用户填了面积却得不到任何反馈，误以为模型已考虑坪效。
- 方案：要么把面积纳入评分（如人均面积/坪效档位，权重从现有五项中重分配并同步公式框与 FAQ），要么删掉该输入及所有「六项」措辞，二选一。

### LF-N116 人口维度 5000 人即封顶、租金档位缺「>300 元」档，公式框均未披露（中，确认缺陷）
- 问题：`popScore=min(100, po/50)`，人口 5000 及以上一律满分，2 万与 5 千得分完全相同；租金 `>300` 实为 20 分，但公式框只写到「≤300 计 40 分」，未说明超档结果。
- 证据：`tools/life/assessor-target.html:229`、`:230`、`:128`（公式框分档描述止于「≤300」）；注意事项 `:215` 反称「≥3000 人可支撑一家便利店」。
- 复现（node）：人口 5000 与 20000 均 `pop=100`、总分同为 76.0/76.0；租金 301 与 3000 均 `rentScore=20`，而公式框读者会以为最少 40。
- 影响：`tools/life/assessor-target.html`；商圈规模差异被抹平，大面积/高租金铺位被同一档处理，模型区分度失真。
- 方案：人口改用分段或对数刻度（如 3000/5000/10000/30000 对应 60/80/90/100），租金补「>300 → 20」并在公式框写明；deep-dive 的候选铺位算例随之重算。

### LF-N117 deep-dive 候选铺位 B 示例分数与实现不符（低，确认缺陷）
- 问题：正文写 B 铺「约 48 分（一般）」，同参数代入实现得 50.5 分。
- 证据：`tools/life/assessor-target.html:168`；算法 `:227-233`。
- 复现（node）：人流 3000、竞争 5、人口 1 万、租金 200、可见性 5 → 9+5+20+9+7.5 = 50.5，非 48。
- 影响：`tools/life/assessor-target.html`；算例与结果不一致，用户按示例手算会对不上。
- 方案：算例改为「约 50.5 分」或改参数使结果落在 48；deep-dive 数字统一用 node 实跑结果。

### LF-N118 可见的 opt-guide/opt-faq 通用套话块与 deep-dive FAQ 重复（中，确认缺陷）
- 问题：页面底部同时存在 deep-dive 的 FAQ 与 `opt-faq` 通用问答，后者答案为「在对应的输入框或选项中填写…」「计算结果准确吗」等模板句；`opt-guide` 也只写「点击计算或生成按钮」；FAQPage JSON-LD 与 opt-faq 同源。
- 证据：`tools/life/assessor-target.html:427`（`section.opt-guide` + `section.opt-faq`）、`:77`（FAQPage LD）、`:171-175`（deep-dive FAQ）。
- 复现：页面滑到底部 → 出现两段「常见问题」，通用问答与上方深度解析重复且无选址信息。
- 影响：`tools/life/assessor-target.html`；正文可信度与 SEO 质量双降（生活类其余 8 页已有同类残留，见 `length-converter`/`unit-converter` 等）。
- 方案：按 `scripts/opt_cleanup_opt_blocks.py --cat life` 清掉可见块，`opt_faq_ld_sync.py` 同步 LD；保留 deep-dive 中的选址专属问答。

### LF-N119 三页面包屑行业名与 tools/life 首页不一致（低，确认缺陷）
- 问题：同一行业目录下，`assessor-target` 面包屑写「便利店务」，`generator-price`/`recommender-8` 写「家政服务」，而 `tools/life/index.html` 的行业名是「日常生活」。
- 证据：`tools/life/assessor-target.html:108`、`tools/life/generator-price.html:99`、`tools/life/recommender-8.html:99`；对照 `tools/life/index.html:71`（「🏠 日常生活工具」）。
- 复现：对比三页面包屑第二级文字与首页 h1 → 三个名字互不相同。
- 影响：三页；面包屑误导站点结构，且属「只写一次」字段（构建不会刷新，改名需同步页面与 i18n）。
- 方案：三页面包屑统一改为「🏠 日常生活」并同步 BreadcrumbList LD；若确为细分场景，应在 life 首页新增对应分类而非借用错名。

**留存建议（tools/life/assessor-target.html）**
- 五维加权 + 四档评级 + 两段候选铺位对比示例的结构清晰，补面积维度（LF-N115）后即成完整六维模型。
- 已内置 4 组预设（社区店/旗舰店/街边小铺），建议再加「空白重置」与「两铺并排对比卡」，比趋势图更贴合选址决策。
- 公式框已披露权重与分档，保持这一透明度；把人口/面积/超档租金补进同一框即可，无需新增页面。

### LF-N120 deep-dive 与 FAQ 称「随机组合」，实现却是固定顺序循环（中，确认缺陷）
- 问题：服务项按 `services[i % services.length]` 顺序取用，生成 5 条必为「网站开发→UI设计→品牌策划→法律咨询→翻译服务」；`randItem` 定义了却从未调用。
- 证据：`tools/life/generator-price.html:239`（固定索引）、`:211-213`（`randItem` 无引用）、`:155`（「随机组合」）、`:161`（FAQ「当前为随机组合生成」）。
- 复现：连续点两次「生成」或把数量设为 5 → 服务项名称与顺序完全一致，仅金额/编号变化。
- 影响：`tools/life/generator-price.html`；用户按「随机」预期做多版本比选时拿到同质结果，多次生成价值下降。
- 方案：改 `randItem(services)`（可加「不重复前缀」抽样）或保留顺序但把文案改成「按内置清单依次生成」；二选一后同步 deep-dive/FAQ。

### LF-N121 公式框的单价×数量×税率×折扣与引据表成本加成，页面无对应输入；「中文大写」实为小写数字（中，确认缺陷）
- 问题：页面唯一输入是「生成数量」，金额为 1000–50000 随机整数；公式框却描述 `单价 × 数量 ×（1 + 税率）− 折扣额`，引据表讲成本加成/目标毛利/心理定价，均无输入可落地。deep-dive 称生成「中文大写」金额，`numberToChinese` 输出的是「一万二千三百四十五」这类小写中文数字，而非财务大写（壹贰叁肆）。
- 证据：`tools/life/generator-price.html:120`（公式）、`:124`（仅 `cnt`）、`:214-233`（`units/nums` 用「一二三…」）、`:155`（「中文大写报价条目」）、`:178-192`（成本加成等引据）。
- 复现：生成 5 条 → 金额均为随机值，改数量只改条数；任取一条金额 12345 → 显示「一万二千三百四十五元整」，不是「壹万贰仟叁佰肆拾伍元整」。
- 影响：`tools/life/generator-price.html`；公式框与引据表对用户零参考价值，且「大写」不符合同/财务常识，正式抄用易出错。
- 方案：要么增加单价、税率、折扣三个可选输入并按公式计算，要么把公式框改为「随机草案生成规则」；金额大写改用财务大写映射（壹贰叁肆伍陆柒捌玖拾佰仟万），并同步引据表。

### LF-N122 「导出明细 CSV」导出的只是历史表，结果被截断到 80 字（低，确认缺陷）
- 问题：导出读取 `#generator_priceTable`（历史记录表），其中「结果」列由 `res.slice(0,80)` 生成；合同的第二至第八条不会出现在 CSV 里。
- 证据：`tools/life/generator-price.html:362`（`slice(0,80)`）、`:369-379`（历史表渲染）、`:437`（`exportTable('#generator_priceTable')`）。
- 复现：生成 1 条合同 → 导出 CSV → 只有「时间/生成数量/结果」，结果列止于「合同编号…第一条 服务内容」附近，条款缺失。
- 影响：`tools/life/generator-price.html`（`recommender-8` 与 `stats-13`/`assessor-target` 同模板同现象）；导出物无法作为草稿留档。
- 方案：把当前 `#res` 全文按条目拆行导出（或导出 `#res` 的 textContent），历史表另设「导出历史」按钮。

**留存建议（tools/life/generator-price.html）**
- 八条合同骨架（服务内容/金额/付款/期限/知识产权/保密/违约/争议）覆盖面好，适合作为初稿；保留并加「复制单条」比整体复制更实用。
- 金额 30% 预付 + 尾款 = 总额的拆分逻辑闭合，可在结果区显式写「预付+尾款=总额」增强可核对性。
- 编号 `HT-xxxx-xxxx` 可改为「日期+序号」并去重，避免同批草案编号碰撞。

### LF-N123 公式框以年收入/负债/工资总额测算保额与保费，页面没有这些输入，数值全为随机（中，确认缺陷）
- 问题：`保额按需求法估算：寿险 = 年收入×5~10 + 负债 − 已有储蓄…；雇主责任险保费 = 员工年工资总额 × 行业费率`，但页面仅有「生成数量」，保额取自场景区间随机数、保费为 `randInt(保额×2, 保额×30)` 元，与任何收入/费率无关。
- 证据：`tools/life/recommender-8.html:120`（公式）、`:124`（唯一输入）、`:228-231`（`randInt` 生成 amount/premium）、`:236`（输出「建议保额…年保费参考」）。
- 复现：数量设 1 连点三次 → 同一场景保额与保费每次不同（如 5–50 万间跳变、保费 10–1500 元随机），且改不出任何收入参数。
- 影响：`tools/life/recommender-8.html`；用户会误以为「年保费参考」与保额有精算关系，实际仅 0.02%–0.3% 的固定随机带。
- 方案：增加年收入/负债/已有保额/员工人数四个可选输入并按公式实算；若坚持纯示例，则把公式框改为「常见保额区间示例」并删除保费数字或标注「随机示例，非报价」。

### LF-N124 数量上限 50 但只有 8 个场景，第 9 条起场景名重复；承诺的「保额区间」输出为单值（低，确认缺陷）
- 问题：`n` 最大 50，`scenarios[i % 8]` 使每 8 条循环一次，第 9 条与第 1 条场景名完全相同；deep-dive 称「输出每类对应的险种名称与常见保额区间」，实际每条只给一个随机保额数字。
- 证据：`tools/life/recommender-8.html:215`（上限 50）、`:216-225`（8 个场景）、`:228`（`i % scenarios.length`）、`:236`（单值 `amount`）、`:155`（「常见保额区间」）。
- 复现：数量 9 → 第 9 条「家庭财产 场景」与第 1 条同名；输出行形如「建议保额：137 万元」，无区间。
- 影响：`tools/life/recommender-8.html`；批量清单出现重复场景，用户误以为覆盖了 50 类风险。
- 方案：数量上限收到 8 或扩充场景库；按场景给「区间」文案（如「50–300 万元」），随机值仅作示例并标注。

**留存建议（tools/life/recommender-8.html）**
- 8 类场景（家财/意外/雇主/公众/旅行/宠物/租房/小微）覆盖面实用，建议保留并补「已有保障」勾选项做缺口提示。
- 「选购要点」四条轮换（免赔额/法律援助/地域/等待期）比泛化文案有用，可固定为每场景专属两条。
- 保持纯前端与「不构成报价」免责声明；若加输入，务必仍不上传、不落盘。

### LF-N125 页面渲染出两个「🔗 相关工具」区块（中，确认缺陷）
- 问题：同一页连续出现两个 `data-related-tools="1"` 容器，标题、卡片列表重复，且第一个混入殡葬/婚礼工具。
- 证据：`tools/life/countdown.html:451`（第一个区块，含 `../funeral/grave-design.html`、`../wedding/seating-chart.html`）、`:478`（第二个区块）。
- 复现：打开页面 → 「相关工具」标题出现两次，网格上下叠放 5 + 6 张卡片。
- 影响：`tools/life/countdown.html`；移动端首屏被重复模块拉长，权重分散；两套推荐口径互相冲突。
- 方案：删除手工追加的重复区块（保留构建注入的一套），并核对 `related-tools` 注入是否因二次写入产生重复；补静态断言（每页 `data-related-tools="1"` 只出现一次）。

### LF-N126 带已存目标刷新时「已过/剩余小时」图表不渲染（低，确认源码缺陷，静态分析）
- 问题：内联脚本在解析期即执行 `load()`→`showResult()`→`__cdExtras()`，此时 `tool-kit.js`（defer）尚未执行，`typeof TBKit==='undefined'` 直接 return；之后无任何时机补渲染，图表区保持空白。
- 证据：`tools/life/countdown.html:110`（`tool-kit.js` 为 defer）、`:184-195`（内联脚本与 `load()`）、`:289-298`（`__cdExtras` 的 TBKit 守卫）、`:376-377`（包装后立即 `load()`）。
- 复现：设定目标并刷新页面 → 结果区正常倒计时，但「已过(小时)/剩余(小时)」柱状图空白；点一次「开始倒计时」后才出现。
- 影响：`tools/life/countdown.html`；恢复场景图表缺失，用户以为图表坏了。
- 方案：把 `load()` 移到 `DOMContentLoaded`（或 `TBKit` 就绪回调）后再执行，或在 `__cdExtras` 失败时用 `setTimeout` 重试一次。

### LF-N127 引据表承诺「多目标排序」「切回前台立即重算」，实现只有单目标且无 visibilitychange（低，确认缺陷）
- 问题：`Formula & Standard References` 写「多个事件按目标时刻升序排列，先到期者优先展示」「页面切回前台须立即重算，补偿后台期间的定时器降频」，但页面只有单目标、localStorage 单对象，全文没有任何 `visibilitychange` 监听。
- 证据：`tools/life/countdown.html:433`、`:437-439`（引据条目）、`:185-186`（`state` 单对象）、全文无 `visibilitychange`（`setInterval` 仅在 `:308`）。
- 复现：设两个目标只能覆盖前一个；切到后台 1 小时再回来，读数在下一个 1 秒 tick 前保持旧值（最多滞后 1 秒，但无「立即重算」实现）。
- 影响：`tools/life/countdown.html`；引据表与实际能力不符，且「多目标」是用户高频诉求却缺失。
- 方案：要么实现多目标列表（数组 + 到期排序 + 逐条渲染），要么把引据表改为单目标口径；补 `document.addEventListener('visibilitychange', tick)` 兑现承诺。

**留存建议（tools/life/countdown.html）**
- localStorage 续跑 + 目标时刻差值计算的方式天然抗后台降频，保留；无需改成累计计数。
- 「元旦/国庆/本周六/下月初」四个预设命中日常场景，可再加「发薪日/生日」并允许自定义事件名。
- 到期后自动停表 + 明确「已到达」状态符合引据表口径，建议补浏览器通知（需用户授权）替代仅页面内 toast。

### LF-N128 面积接受负值与 0 并照常换算；0/负值的尺度感知仍提示「≈1 平方米」（低，确认缺陷）
- 问题：`convert()` 只判 `isNaN`，不判负数与 0；`__charRef` 用 `Math.abs(base)` 取对数最近参照，负值或 0 都会匹配到「1 平方米（桌面大小）」。
- 证据：`tools/life/area-converter.html:304-311`（仅 `isNaN` 判空，无范围校验）、`:560`（尺度模块守卫）、`:566`（`Math.log10(Math.abs(base)+1e-30)`）、`:574`（输出参照）。
- 复现：输入 `-5`、单位 m² → 结果区 `基准：-5 m² = -5 m²`，其余单位全为负；输入 `0` → 「你的输入 ≈ 0 平方米 💡 ≈ 1 平方米（桌面大小）」。
- 影响：`tools/life/area-converter.html`；面积无负数语义，负值结果会误导报价/登记核对。
- 方案：`v<0` 提示「面积不能为负」；`v===0` 走「0 面积」空态，不参与尺度匹配；顺带补 `min="0"`。

### LF-N129 公式框称「8 单位系数表互转」，结果区只输出 7 行（低，确认行数口径不一致）
- 问题：结果循环 `if(k !== from)` 跳过源单位，源单位数值只出现在「基准」行；页内「8 单位系数表互转」的表述会让用户预期看到 8 行对应值。
- 证据：`tools/life/area-converter.html:157`（公式框「8 单位系数表互转」）、`:315`（`if(k !== from) continue`）、`:314-318`（输出循环）。
- 复现：默认 1 m² → 结果区仅 7 行（mm²/cm²/km²/亩/公顷/英亩/ft²），无 m² 自身行；`weight-converter` 输入 1 g → 8 行（共 9 单位同样跳过源单位）。
- 影响：`tools/life/area-converter.html`；用户对照 8 单位清单时会以为漏算，且无法在同一列表里核对源单位系数。
- 方案：把源单位行也输出（标「源单位」），或明确写「列出其余 7 个单位」；`weight-converter` 同模板建议同步处理。

**留存建议（tools/life/area-converter.html）**
- 8 单位系数表与「基准 m² 两步换算」口径统一，双向复算闭合（1 ha→15 亩、1 acre→6.070284633 亩、1 ft²→0.09290304 m²），无需改系数。
- 「尺度感知」实物参照（车位/小两居/足球场/故宫）是差异化亮点，建议加「输入≈几个标准车位」这类倍数表达。
- 建议补「亩/公顷/英亩」对照速查行，方便农业与房产双口径。

### LF-N130 重量接受负值与 0，尺度感知仍提示「≈1 克（回形针）」（低，确认缺陷）
- 问题：与面积页同模板，`convert()` 只判 `isNaN`；`__charRef` 用绝对值匹配最近参照，负重量或 0 都落到 1 g。
- 证据：`tools/life/weight-converter.html:300-307`（仅 `isNaN` 判空，无范围校验）、`:556`（尺度模块守卫）、`:562`（`Math.log10(Math.abs(base)+1e-30)`）、`:570`（输出参照）。
- 复现：输入 `-3`、单位 kg → 结果区全为负值；输入 `0` → 「≈ 1 克（一枚回形针）」。
- 影响：`tools/life/weight-converter.html`；负质量无物理意义，易误用于净重/损耗核对。
- 方案：`v<0` 明确报错，`v===0` 空态；补 `min="0"`。

**留存建议（tools/life/weight-converter.html）**
- 9 单位覆盖公制/英制/市制/宝石（克拉），1 kg=2.204622622 lb、1 lb→oz→lb 往返闭合，系数无需调整。
- 「买菜 2 斤 / 钻石 0.5 克拉 / 快递 2.5 kg」预设贴合生活，建议再加「婴儿体重（克）」「食材配方（两）」。
- 尺度和实物参照（回形针/苹果/猫/行李箱/钢琴）很有辨识度，可保留并补「≈ 几瓶 500 mL 水」的直观类比。

### 覆盖小结（2026-11-04 并行批 P）
- 实读 7 页：`tools/life/stats-13.html`、`assessor-target.html`、`generator-price.html`、`recommender-8.html`、`countdown.html`、`area-converter.html`、`weight-converter.html`。
- 新增 21 条：高 1（LF-N114）/ 中 9（LF-N111、112、115、116、118、120、121、123、125）/ 低 11（LF-N113、117、119、122、124、126、127、128、129、130、131）。
- 换算类（面积/重量）用 node 复算并验证双向闭合：面积 1 ha↔15 亩、1 acre↔4046.8564224 m²、1 ft²↔0.09290304 m²；重量 1 lb↔453.59237 g、1 lb→oz→lb=1、1 jin=500 g，系数无误，缺陷集中在输入范围、显示格式与文案。
- 未做：浏览器交互/截图、`?lang=en-US` 英文态、移动端、`run_gates.py` 门禁与线上抽样；LF-N126 为源码时序推断（内联脚本早于 defer 的 `tool-kit.js`），未在真机复现。

## 2026-11-04 复核（并行批 Q）

范围：只读重读 `radiation-converter`、`density-converter`、`magnet-converter`、`pressure-converter`、`assessor-target`、`generator-price`、`countdown` 共 7 页当前工作树源码（含内联 JS、公式框、FAQ、引据表），关键数值用 `node -e` 复算。未开浏览器、未做英文态/移动端/门禁验证。

### LF-V4 换算器图表恒空白（原 LF-N110，已变化·缺陷仍在）
- 复核结论：机制仍成立（`parseFloat` 对中文结果恒 NaN），但「图表页签」这一呈现口径已过时——四页当前页签只有 结果/数据表/预设/历史，图表容器被并进「结果」面板。
- 证据：`density-converter.html:389`（`parseFloat(arr[j].d[rk])`）、`:393`（`chart.line`）、`:519`（`P["res"]` 含 `density_converterChart`）、`:151-154`（页签无「图表」）；`magnet-converter.html:392`、`:396`、`:520-523`；`pressure-converter.html:387`、`:391`、`:505-508`；`radiation-converter.html:391`、`:395`、`:549-550`。历史记录存的是 `res` 文本（如 `radiation:424`、`generator-price:376`）。
- 复算：`parseFloat("基准：1 Oe = 79.5774715 A/m")` → `NaN`；`parseFloat("基准：1 g/cm³ = 1000 kg/m³")` → `NaN`；`parseFloat("基准：1 bar = 100000 Pa")` → `NaN`，`nums.length` 恒 <2。
- 变化差异：旧条目按「点图表页签空白」描述，现应改为「结果面板内嵌空图表」。新建议：记录历史时另存 `__v`（基准值）供 `chart.line` 使用；若不做趋势图，直接移除 `*_converterChart` 容器与 `Extras` 图表分支，避免死代码。

### LF-V5 选址评分无上下限夹取，可见性 50 得 139.0（原 LF-N114，仍成立）
- 复核结论：`calc()` 未加任何 clamp/校验，越界值仍直接进权重。
- 证据：`tools/life/assessor-target.html:137`（`min="1" max="10"` 仅声明）、`:224-232`（`+value||0`、`visScore=vs*10`、总分直接加权）、`:241`（输出 `total.toFixed(1)`）。
- 复算：默认参数 + 可见性 50 → `vS=500`、`total=139.0`；人流 -8000 → `28.0`；竞争 -2 → `compScore=130`。
- 建议：沿用旧方案（统一 `clamp`，可见性 1–10，人流/人口/竞争/租金 ≥0，总分再夹 0–100）。

### LF-V6 店铺面积输入对评分零作用（原 LF-N115，仍成立）
- 复核结论：`shopArea` 仍只读取不使用，且「六项」自述仍在。
- 证据：`tools/life/assessor-target.html:136`（输入）、`:226`（`sa=` 后无引用）、`:232`（五项权重合计 1.0）、`:164`（「六项打分」）、`:10`（description 含面积）、`:129`（公式框写「五维」）。
- 复算：其余输入不变，面积 80 与 2000 均得 `76.0`。
- 建议：二选一——纳入坪效维度并重分配权重，或删除面积输入及全部「六项」措辞。

### LF-V7 人口 5000 封顶、租金缺「>300」档且公式框未披露（原 LF-N116，仍成立）
- 复核结论：分段逻辑与披露缺口均未变。
- 证据：`tools/life/assessor-target.html:229`（`Math.min(100, po/50)`）、`:230`（`>300 → 20`）、`:128`（公式框止于「≤300 计 40 分」）。
- 复算：人口 5000 与 20000 总分同为 `76.0`；租金 301 与 3000 均为 `20` 分。
- 建议：人口改分段/对数刻度；公式框补「>300 → 20 分」，并同步 deep-dive 算例。

### LF-V8 deep-dive 候选 B 示例 48 分与实算 50.5 不符（原 LF-N117，仍成立）
- 复核结论：算例数字未更新。
- 证据：`tools/life/assessor-target.html:168`（「约 48 分（一般）」）；算法 `:227-233`。
- 复算：人流 3000→30、竞争 5→25、人口 1 万→100、租金 200→60、可见性 5→50：`9+5+20+9+7.5 = 50.5`。
- 建议：改为「约 50.5 分」或调参使结果落 48；deep-dive 数字统一 node 实跑。

### LF-V9 报价宣称「随机组合」实为固定顺序循环（原 LF-N120，仍成立）
- 复核结论：`randItem` 仍定义未用，服务项按索引取用。
- 证据：`tools/life/generator-price.html:239`（`services[i % services.length]`）、`:211-213`（`randItem` 无引用）、`:155`（「随机组合」）、`:161`（FAQ「当前为随机组合生成」）。
- 复现/复算：数量 5 → 固定「网站开发→UI设计→品牌策划→法律咨询→翻译服务」；二次生成仅金额/编号变化。
- 建议：改 `randItem` 或把文案改为「按内置清单依次生成」，二选一后同步 deep-dive/FAQ。

### LF-V10 公式框无对应输入、「中文大写」实为小写数字（原 LF-N121，仍成立）
- 复核结论：唯一输入仍是生成数量；`numberToChinese` 仍输出小写中文数字。
- 证据：`tools/life/generator-price.html:120`（单价×数量×(1+税率)−折扣）、`:124`（仅 `id="cnt"`）、`:214-233`（`nums=['零','一','二'…]`）、`:155`（「中文大写」）、`:178-192`（成本加成等引据）。
- 复算：`numberToChinese(12345)` → 「一万二千三百四十五元整」，财务大写应为「壹万贰仟叁佰肆拾伍元整」。
- 建议：增单价/税率/折扣输入并实算，或把公式框改为「随机草案生成规则」；大写改用壹贰叁肆…映射。

### LF-V11 导出明细 CSV 只导历史表且结果截断 80 字（原 LF-N122，仍成立）
- 复核结论：导出仍取历史表；结果列仍 `slice(0,80)`。
- 证据：`tools/life/generator-price.html:362`（`return t.slice(0,80)`）、`:369-379`（历史表 时间/生成数量/结果）、`:437`（`exportTable('#generator_priceTable','generator-price.csv')`）、按钮 `:125`。
- 复现：生成 1 条合同 → CSV 只含 3 列，结果止于首条附近，第二至第八条缺失。
- 建议：导出当前 `#res` 全文（按条目拆行），历史另设「导出历史」。

### LF-V12 页面渲染两个「🔗 相关工具」区块（原 LF-N125，仍成立）
- 复核结论：两套 `data-related-tools="1"` 容器仍在。
- 证据：`tools/life/countdown.html:451`（含 `../funeral/grave-design.html`、`../wedding/seating-chart.html`）、`:478`（第二套）。
- 复现：同页「相关工具」标题出现两次，卡片 5+6 张叠放。
- 建议：删手工块保留构建注入的一套，并补静态断言「每页 `data-related-tools="1"` ≤1」。

### LF-V13 带已存目标刷新时「已过/剩余小时」图表空白（原 LF-N126，仍成立·静态分析）
- 复核结论：时序缺陷未变，未在真机复现。
- 证据：`tools/life/countdown.html:110`（`tool-kit.js` defer）、`:377`（解析期同步 `load()`）、`:189-192`（`load → showResult`）、`:289-298`（`__cdExtras` 的 `typeof TBKit==='undefined'` 直接 return）。
- 复现（源码推断）：有 localStorage 目标时刷新 → 倒计时正常、图表区空；点「开始倒计时」后才绘制。
- 建议：`load()` 延后到 `DOMContentLoaded`/`TBKit` 就绪，或在 `__cdExtras` 失败时 `setTimeout` 重试。

### LF-V14 引据表承诺多目标排序与 visibilitychange 重算，均未实现（原 LF-N127，仍成立）
- 复核结论：仍为单目标 `state` 对象，全文无 `visibilitychange` 监听。
- 证据：`tools/life/countdown.html:432-433`（「多个事件按目标时刻升序排列」）、`:437-438`（「切回前台须立即重算」）、`:186`（`var state={target:0,start:0,name:''}`）、`:308`（仅 `setInterval`）。
- 复现：设第二个目标即覆盖第一个；切后台回前台读数最多滞后 1 秒，无「立即重算」。
- 建议：改多目标数组+排序渲染，或把引据表改为单目标口径；补 `document.addEventListener('visibilitychange', tick)`。

### 承诺 vs 实际（Q 批专项）
- **复制**：`density-converter.html:106`/`:503`、`magnet-converter.html:106`/`:506`、`radiation-converter.html:106`/`:532` 均写「支持复制与导出」，但工具栏 `density:183-185`、`magnet:182-184`、`radiation:184-185` 无复制按钮，也无 `copyRes` 实现 —— 沿用 LF-N109，三页仍成立。
- **导出**：`generator-price.html:125` 按钮称「导出明细 CSV」，实际导出历史表且结果列被 `:362` 截断 80 字（`:437`），合同条款缺失 —— 沿用 LF-N122，仍成立。
- **核验**：`assessor-target.html:137` 声明 `min="1" max="10"`，`calc()` `:224-232` 未校验，可见性 50 仍得 139.0 —— 属「声明了校验但未实现」，与 LF-N114 同源。
- **自动识别**：7 页全文无「自动识别/智能识别」字样（`grep` 无命中），无新增承诺。
- **限时 / ROI / 难度**：本批 7 页均无此类承诺，沿用旧结论（无新增）。

### 跨页留存/优势建议（3 条）
1. **四页换算器合并一套结构化内核**：把 `parseFloat` 文本、7 单位输出、历史表、图表统一为「数值字段 + `fmt` + `exportTable`」模板，一次修好辐射/密度/磁场/压力（当前四页各复制一份，缺陷同步复制）；保留现有全单位并列输出与胸片/CT/地磁/MRI 预设，这是换算器最实用的部分。
2. **换算器加「复制全部结果 + 单位对照表导出」而非趋势图**：四页图表数据源本就是中文结果串，换算场景更常被贴进报告；复制按钮与「本次 vs 上次」差值卡比历史曲线更贴合使用路径。
3. **决策类保留骨架、补可核对输入**：`assessor-target` 保留五维加权、四档评级与 4 组预设，补面积坪效与「两铺并排对比卡」；`generator-price` 保留八条合同骨架与 30% 预付拆分，把随机金额换成单价/税率/折扣输入并导出全文；`countdown` 保留 localStorage 目标续跑与到达态，补多目标数组 + `visibilitychange`。

### 复核覆盖
- 7 页：`radiation-converter`、`density-converter`、`magnet-converter`、`pressure-converter`、`assessor-target`、`generator-price`、`countdown`。
- 剩余问题与待核内容见上文各条；已确认消除的旧问题已从清单移除。
- 未做：浏览器交互与截图、`?lang=en-US` 英文态、移动端、`run_gates.py` 门禁与线上抽样；LF-V13 仍为源码时序推断。最高优先：`assessor-target.html:224-232`（无夹取）、`radiation-converter.html:227`/`:541`（权重概念错位）、`generator-price.html:239`（固定循环）、`countdown.html:432-438`（承诺未实现）。

## 2026-11-04 回补复核（并行批 R）

范围：只读重读 `workday-calculator`、`parking-fee`、`shoe-size-converter`、`chinese-number`、`ring-size-converter`、`bra-size-converter`、`unit-converter` 共 7 页当前工作树源码（内联 JS、公式框、公式说明、deep-dive、FAQ），关键数值用 `node -e` 按源码逐函数复刻复算。未开浏览器、未构建、未跑门禁、未做任何 git 写操作。

### 工作日计算器非法日期防御（低，观察）
- 脚本注入非法日期（如 `2026-02-31`）时 `parseLocalDate` 返回 Invalid Date，可能静默输出「自然日总数 0 天」；正常 `<input type="date">` 操作不可产生，可显式校验无效日期。

### 罩杯边界文案（低，观察）
- `tools/life/bra-size-converter.html:302-303` 在胸围差恰为 7.5 cm 时归入 A 杯，而公式说明称「AA 差约 7.5 cm」；建议澄清边界，意码问题另见 LF-N137。

### 承诺 vs 实际（R 批专项）
- **工作日（已兑现）**：公式「含首尾 + 调休优先」（`workday-calculator.html:152`）↔ `while(d <= end)`（`:328`）与 `makeupDays` 优先（`:334-336`），复算 5 天区间与补班周六均一致。
- **停车（已兑现）**：公式「按自然日逐日 min(…, 封顶)」（`parking-fee.html:106`）↔ `splitDays`（`:234-255`）+ 逐日 `dayFee`（`:264`），36h→120、50h→140 与公式一致；注意事项 `:174` 仍写「按连续小时估算」，易被读成整段连续估算，建议改为「按自然日分段累计小时」（文案，低，未单列）。
- **鞋码（已兑现，外延未兑现）**：公式与三处示例（`shoe-size-converter.html:157`、`:192-195`、`:225`）↔ `euFromMm`/`toMm`/`fromMm`（`:283-310`）完全一致（EU42=US9=CN260）；但英文简介 `:159` 称覆盖「JP / children」，下拉只有 6 项且无 JP、无儿童，属文案超范围（低，未单列）。
- **戒指（部分未兑现）**：公式美码 2.76/36.25（`:157`、`:194`）与代码（`:290`、`:305`）内部自洽，但 deep-dive「52 mm≈US 6」（`:227`）实算 5.70652 → LF-N136；「欧码直通、54 mm→54 欧/14 意」（`:196`）实算一致（已兑现）。
- **罩杯（意码/日码未兑现）**：公式 10 cm→A、12.5 cm→B（`:157`）↔ 区间表（`:303-304`）一致；「意码」`:328` 恒等于国际杯级，无独立换算 → LF-N137；英文简介 `:159` 称覆盖「JP」，结果区无日码（低，未单列）。
- **油耗（已兑现）**：倒数单位标注（`unit-converter.html:675-677`）↔ `unitToBase`/`unitFromBase`（`:739-748`）一致，5 L/100km=20 km/L=47.043 mpg(US)，quick `:684` 的 8→29.4 实算 29.404；0/负值缺口见 LF-N138。
- **同页遗留（非本批 9 条）**：`unit-converter.html:590` 的 dBm 仍只标 `special: 'dbm'` 而无换算实现，选中后结果清空（原 LF-N31 仍成立）；本批 7 页工具栏均无「复制」承诺（`grep 复制` 无命中），不新增复制类缺口。

### 回补覆盖
- 7 页：`workday-calculator`、`parking-fee`、`shoe-size-converter`、`chinese-number`、`ring-size-converter`、`bra-size-converter`、`unit-converter`。
- 生活类复核中的剩余观察与待处理问题见上文各条；已确认消除的旧问题已从清单移除。
- 方法：逐页 Read + 按源码函数在 `/tmp` 复刻 `node` 复算（含跨日、往返、边界与非法输入）；未开浏览器、未做 `?lang=en-US`、移动端、导出/历史点击、`run_gates.py` 与线上抽样。

## 2026-11-04 回补复核（并行批 S）

范围：只读重读 `phone-lookup`、`length-converter`、`number-to-chinese`、`detector-checker-strength`、`countdown-timer`、`analysis-cost-10`、`stats-13` 共 7 页当前工作树源码（内联 JS、公式框、deep-dive、FAQ），关键数值用 `/tmp/recheck_life.js` 按源码逐函数复刻 `node` 复算（含区号、双向换算、含零分组、熵与破解时间、日期预设、脏行、小数份数）。未开浏览器、未构建、未跑门禁、未做任何 git 写操作。

### LF-V30 公式框称「同名买家合并计数」，FAQ 与代码按行重复计（原 LF-N111，仍成立）
- 复核结论：仍成立。公式框仍承诺「同名买家按同一人合并计数」，FAQ 仍写「同一姓名出现两次会算作两个条目」，代码仍 `people=rows.length` 逐行计数，无 `Map` 合并。
- 证据：`tools/life/stats-13.html:120`（公式框）、`:167`（FAQ 原句）、`:221-239`（仅 `rows.push` 后取长度）。
- 复算：`张丽,2` + `张丽,3` → 2 人 / 5 份 / 340.00 元 / 人均 170 元；按公式框应 1 人 5 份（人均 340 元）。
- 变化说明：与旧结论一致，行号仍为 `:120`、`:167`，无修复痕迹。新建议：二选一并同步公式框、FAQ、deep-dive（见 `:158` 对账场景）。

### LF-V31 占比/分档与漏斗/时段峰值均未实现（原 LF-N112，仍成立）
- 复核结论：仍成立。meta/公式框仍承诺「占比、分档金额」，intro 仍列「报名付款聚合 / 转化漏斗分层 / 时段峰值识别」；结果区仍只有 7 个汇总量。
- 证据：`tools/life/stats-13.html:10`（description）、`:120`（占比与分档公式）、`:245-251`（实际输出）、`:291-295`（intro 特性）。
- 复算：默认 5 行名单 → 仅人数、合计份数、人均份数、最多、最少、预售金额、人均金额；`stats_13Table/Chart/Hist`（`:347`、`:370`）只渲染历史与趋势，无单项占比/分档。
- 变化说明：与旧结论一致，无修复。新建议：补「逐人占比 + 分档金额」两行，或删除 description/intro 中未实现的付款、漏斗、时段措辞。

### LF-V32 带单位写法被当姓名、份数静默按 1 计；小数份数照收（原 LF-N113，仍成立）
- 复核结论：仍成立。`parts` 按逗号/分号/空白切分后只看末项是否可 `parseFloat`，末项为「箱/份」等即整行当姓名、份数回落 1；`qty<=0` 才回落 1，小数不拦截。
- 证据：`tools/life/stats-13.html:222-234`（切分、末项解析、`qty<=0` 回落）、`:163`（deep-dive 明示「0 或负数按 1 份」）。
- 复算：`张丽,2 箱` → 姓名「张丽 2 箱」、1 份、68.00 元（应 2 份 / 136.00 元）；`张丽,1.5` → 合计 1.5 份、102.00 元。
- 变化说明：与旧结论一致。新问题见 LF-N142（小数份数与合计取整冲突）。

### LF-N140 三位预算数被误当千分位，合法逗号分隔行遭跳过（中，Node 复现）
- `tools/life/analysis-cost-10.html:217-230` 先把数字后接逗号及三位数字的组合按千分位合并，再匹配名称、预算和实际。`办公 用品,100,120` 被错误归一为 `办公 用品,100120`，因缺少字段而跳过；全为异常行时只显示格式提示，混有有效行时会提示并列出被跳过的原文。
- 复现：输入 `办公 用品,100,120` 和 `团建,3000,3500`，结果只统计团建，预算 3000、实际 3500；把前者改为 `办公 用品 100 120` 才能正确计入。需区分字段分隔逗号与数字内部千分位。

### LF-N142 小数份数时「合计份数」按 0 位四舍五入，与金额对不上（中，确认源码缺陷）
- 描述：`fmt(total,0)` 用 `maximumFractionDigits:0`，1.5 显示为 2；而金额与人均份数仍按 1.5 计，同一结果区出现「2 份 × 68 = 102 元」的自相矛盾。
- 证据：`tools/life/stats-13.html:215`（`fmt` 定义）、`:246`（`fmt(total,0)`）、`:247`（人均份数保留 2 位）、`:249`（最多/最少 `fmt(qty,0)`）、`:244`（金额按原始 `qty`）。
- 复算：`张丽,1.5`、单价 68 → 合计份数「2」、人均份数「1.50 份/人」、预售金额 102.00 元（按 2 份应为 136 元）。
- 影响：接龙结算最关键的两个数字互相矛盾，用户按合计份数收款会多收 34 元。
- 方案：份数统一保留 1–2 位小数（至少与金额同精度），或解析阶段拒绝小数并逐行提示（与 LF-N113 一并处理）。

### LF-N143 长度换算 ≥1e6 结果改用科学计数法，且目标单位值重复输出（低，确认源码缺陷）
- 描述：`fmt` 对 `|n|≥1e6` 一律 `toExponential(6)`，公里→毫米这类常见换算显示 `1.000000e+6`；逐单位列表已含目标单位，末尾又单列一次「目标单位」。
- 证据：`tools/life/length-converter.html:313-319`（`fmt`）、`:331-335`（全单位列表）、`:336-340`（目标单位重复行）。
- 复算：1 km →「1.000000e+6 毫米」「100000 厘米」；42.195 km → 毫米「4.219500e+7」；默认 1 m→cm 时「100 厘米」出现两次。
- 影响：结果难以直接抄写；重复行让用户误以为存在两种结果。
- 方案：≥1e6 改用千分位十进制（或仅 ≥1e12 才科学计数法）；目标单位已在列表中时不再追加。

### LF-N144 「去重字符数 × log2(池)」对长随机口令系统性低估，等级偏低（低，确认源码缺陷）
- 描述：模型用去重字符数替代实际长度（重复字符「不增加信息量」），20 位随机小写通常只有 11–14 种字符，被算成 52–66 bits，而真实熵约 94 bits；另 `entropy` 封顶 100，使 ≥100 bits 口令的破解时间一律相同。
- 证据：`tools/life/detector-checker-strength.html:270-274`（`uniqueCount` 与乘法）、`:286`（封顶 100）、`:288-306`（等级阈值）、`:120`（公式框自述）、`:375`（生成器符号集实际 26 个，公式按 32 计）。
- 复算：`abacadaeafagahaiajak`（20 位、11 种、真实熵 94.0）→ 51.7 bits / 52 分「一般」；`abcdefghijklmnopqrst`（20 种）→ 94 分「极强」；封顶后强口令破解时间统一为约 4 万亿年。
- 影响：本来安全的随机口令被判「一般」并被建议「增加符号」，用户可能把强密码改弱；超强口令的破解时长失去区分度。
- 方案：改用「长度 × log2(池)」再按重复模式扣减，或同时展示「长度熵 / 字符集熵」；封顶后注明「≥100 bits」。

### 承诺 vs 实际（S 批专项）
- **长度（呈现待核）**：科学计数法与重复行见 LF-N143。
- **密码强度**：模型对长随机口令的偏差见 LF-N144。
- **倒计时**：春节日期表仅覆盖 2025–2030，表外提示手动选择。
- **预算**：逗号分隔数据误判为千分位，见 LF-N140。
- **接龙统计（三项仍未兑现）**：`:120` 同名合并 ↔ `:239` `rows.length`（LF-N111）；`:10`/`:120` 占比与分档 ↔ `:245-251` 无输出（LF-N112）；`:163`「0 或负数按 1 份」为明示行为，但小数份数与 `fmt(total,0)` 冲突（LF-N142）。本批仅 `stats-13:253` 与 `analysis-cost-10:239` 有「复制结果」按钮（走 `ToolBox.copyText`），本次未做点击验证，不新增复制类缺口。

### 回补覆盖
- 剩余问题见上文各条；已确认消除的旧问题已从清单移除。
- 方法：逐页 Read + 按源码函数在 `/tmp/recheck_life.js` 复刻 `node` 复算（区号、双向单位、含零分组、熵/破解时间、日期预设、脏行、小数份数）；未开浏览器、未做 `?lang=en-US`、移动端、`run_gates.py` 与线上抽样。
- 待进一步核对：`stats-13.html` 的人数、份数和占比输出，以及 `analysis-cost-10.html` 的异常行处理。

## AB 批 · 生活族矩阵：单位/日期时间（2026-11-04）

> 页面名后的「（死键 N）」= 该页第三层英文词典（`i18n/tools/en/<ind>/<slug>.json`）高优先死键数（来源 `plan/i18n-dead-keys.md`）；各线改本页时顺手清理，本批不修英文。

范围：只读实读 `tools/life/length-converter.html`、`weight-converter.html`、`temperature-converter.html`、`timestamp.html`、`date-diff.html`、`world-clock.html` 6 页当前工作树（内联 JS、公式框、默认值、深挖/引用表），关键值在 `/tmp` 用 `node` 按源码函数复刻复算。未开浏览器、未构建、未跑门禁、未做 git 写操作；编号承接 LF-N145，自 LF-N146 起。

### 矩阵（页面 / 实现方式 / 可验证性 / 结论）

| 页面 | 实现方式 | 可验证性（标准值复算） | 结论 |
|---|---|---|---|
| `length-converter.html`（长度）（死键 2） | 自写：10 单位「米」基准系数表 + 全单位并列输出；`toUnit` 目标下拉 | 1 in=25.4 mm ✓；1 mi=1.609344 km ✓；1 ly=9.460730e+12 km ✓；175 cm=68.8976378 in ✓；默认 1 m→100 cm ✓ | 系数无误、非回显；但「目标单位」下拉是死控件（LF-N147） |
| `weight-converter.html`（重量）（死键 4） | 自写：9 单位「克」基准系数表（与长度同模板，无目标下拉） | 1 lb=453.59237 g ✓；1 kg=2.204622622 lb ✓；1 斤=500 g、2 两=100 g ✓；1 t→克 `1000000` ✓ | 系数无误；负值/0 无拦截（延续 LF-N130），本波无新增 |
| `temperature-converter.html`（温度）（死键 3） | 自写：5 温标以摄氏为中转的线性公式 | 0°C=32°F=273.15K=491.67°R ✓；100°C=212°F/373.15K ✓；−40°C=−40°F ✓；491.67°R→0°C ✓；默认 25°C=77°F/298.15K/536.67°R/20°Ré ✓ | 公式正确；但五个输入框每次键入都被 `toFixed(2)` 重写（LF-N148，静态推断） |
| `timestamp.html`（时间戳）（死键 0） | 自写：`Date` + 手算时区偏移（非 Intl 时区库），秒/毫秒自动识别 | 1793750400 ↔ 2026-11-04T00:00:00Z ✓；1700000000 → 2023-11-14T22:13:20Z ✓；毫秒/秒互反 ✓ | 换算正确；默认时区为「浏览器本地」（本机 Asia/Shanghai 即 +8，非 UTC），选项含 +8/+9/−5，属通过 |
| `date-diff.html`（日期差/周数）（死键 3） | 自写：本地日期 `setDate` 逐日循环累计工作日/周末 | 默认 2026-01-01→2026-07-29 = 210 天/150 工作日/60 周末/30 完整周 ✓；同日=1 天 ✓；跨年 2024-01-01→2026-09-09=983 天 △（深挖写 981） | 主算法含首尾正确；「排除周末（只算工作日）」勾选后主天数不变（LF-N149） |
| `world-clock.html`（时区/会议）（死键 3） | 自写 + 原生 `Intl.DateTimeFormat`（timeZone 时区库），静态 offset 表兜底 | 北京 12:00 → 东京 13:00 / 伦敦 04:00 / 纽约前日 23:00 ✓；纽约比北京慢 13 小时 ✓；默认城市首位=北京 ✓ | 默认时区正确（Asia/Shanghai 优先，非 UTC）；但城市表含 6 个非法 IANA id（LF-N146） |

### 逐页结论（含默认态审查）

- **length-converter**：加载即算默认 1 m，基准行「1 米 = 1 米」+9 行全单位（源单位不单列，基准行已覆盖）。`fmt` 已改 ≥1e12 才科学计数法，旧 LF-N143 的 `1.000000e+6` 在本页已不出现。目标单位下拉 `:181-192` 在 `convert()` `:328-344` 中从未被读取，改选后输出完全不变 → 假控件。
- **weight-converter**：默认 1 g，输出 8 行 + 基准行；无 `toUnit`，不存在同类死控件。9 单位覆盖公制/英制/市制/宝石，系数全部对上标准值
- **temperature-converter**：默认 25°C 已联动四温标与体感/温度计，默认输出正确。风险全在交互：`updateAll()` `:428-441` 无条件把五个输入框写回 2 位小数，且五个框都绑 `oninput`，逐位键入多位数会被吞（未真机，属静态推断，见 LF-N148）。另：开尔文 −5 仍照算 −278.15°C，未按公式框「0K 为理论下限」拦截（低，未单列）。
- **timestamp**：默认无结果，只有每秒刷新的「当前毫秒/秒」卡片，默认态无错值。自动识别口径已由「字符串长度」改「数量级 <1e11 视为秒」，负数不再误判（源码注释 `:458-459`）。`dateResult` 用所选时区、`utcResult`/`isoResult` 恒 UTC，两者标注清楚；默认 `local` 在本机即 +8，未出现 UTC 默认。
- **date-diff**：默认 2026-01-01→2026-07-29 输出 210 天，工作日 150、周末 60、完整周 30，均可复算命中。两处不符：① 勾选「排除周末（只算工作日）」只改变时间轴一句文案，主数字仍 210（LF-N149）；② 引据表 `:222-224` 写「周编号以周一为首、含首个周四为第一周（ISO 8601-1）」，但代码只有 `floor(totalDays/7)` 的「完整周数」，无任何周序计算（文档越界，随 LF-N149 一并修文案即可）。
- **world-clock**：默认时钟墙按 北京/东京/伦敦/纽约 顺序，自动用 Intl 取当前夏令时（2026-11 伦敦 +0、纽约 −5），深挖算例「北京 12:00→纽约前日 23:00」复算一致，时区默认口径**通过**。但城市库 78 个 id 里 6 个不被 IANA/Intl 接受，选中后时钟永久空白（LF-N146）；「会议规划」城市按钮只渲染 `slice(0,20)`（全是亚洲城市），默认集合里的纽约/伦敦不在按钮列表中，无法取消（中低，随 LF-N146 一并修）。

### 问题表格（只记 ①高优 / ②假工具增量 / ③安全）

| 编号 | 级别 | 页面 | 问题 | 证据 |
|---|---|---|---|---|
| LF-N146 | ①高 | `world-clock.html` | 6 个非法 IANA 时区 id，选中后时钟卡恒为 `--:--:--` | `:360-437`（城市表）、`:523-540`（try/catch 静默吞异常） |
| LF-N147 | ①高 | `length-converter.html` | 「目标单位」下拉是死控件，改选不改变任何输出 | `:181-192`、`:328-344`（convert 只读 fromUnit） |
| LF-N148 | ①高（静态推断） | `temperature-converter.html` | 每次键入即把当前输入框重写为 2 位小数，多位数被吞 | `:213/218/223/228/233`、`:428-441` |
| LF-N149 | ①中 | `date-diff.html` | 勾选「排除周末（只算工作日）」后主天数仍含周末 | `:146`、`:260`、`:272`、`:294` |
| LF-N150 | ② | 换算器家族 | 20 个换算页中 13 个的核心能力已被 `unit-converter` 单页覆盖 | `unit-converter.html:308-475`；`length-converter.html:295-306`；`weight-converter.html:276-286`；`temperature-converter.html:174` |
| LF-N151 | ② | 日期家族 | 日期差/日期加减/年龄被拆成 5 页且互相重叠 | `date-difference-calculator.html:178-210`、`:247-248`、`:485-510`；`date-diff.html:130-150`；`date-add-subtract.html:145`；`age-calculator.html:182`；`age-in-days.html:145` |
| LF-N152 | ③安全 | 本波 6 页及 life 全族 | 每页注入无 SRI 的第三方远程脚本 bytegoofy push.js | 例 `length-converter.html:107-117`；`tools/life/` 71 个页面命中 |

### 逐条说明

#### LF-N150（②假工具增量）换算器家族 20 页，13 页核心能力已被 `unit-converter` 覆盖
- 证据：`unit-converter.html:308-475` 的 15 个分类含长度/重量/面积/体积/温度/速度/时间/数据/压力/能量/功率/角度/频率/力/油耗；`length-converter.html:295-306` 仅 10 个单位且无市制（里/丈/尺/寸只在 unit-converter 有），`weight-converter.html:276-286` 9 个单位均被覆盖，`temperature-converter.html:174` 5 温标与 unit-converter 完全同集。
- 说明：`angle` / `area` / `data-unit` / `energy` / `frequency` / `length` / `power` / `pressure` / `speed` / `temperature` / `time` / `volume` / `weight` 共 13 页为核心换算能力的严格子集，只是各自复制了预设/历史/CSV/图表外壳；仅 `concentration`、`data-rate`、`density`、`flow-rate`、`magnet`、`radiation` 6 页有 unit-converter 未覆盖的单位。
- 建议：以 unit-converter 为主入口；13 个单类页若要保留，须补 unit-converter 没有的差异（市制单位、实物尺度参照、批量/表格导出），否则合并并按其 URL 规则走重定向，避免「同功能多 URL」稀释收录。

#### LF-N151（②假工具增量）日期家族 5 页互相重叠
- 证据：`date-difference-calculator.html:178-210`（日期差：天/周/月/年、含首日、含周末）+ `:247-248`、`:485-510`（年/月/周/天加减）已同时覆盖 `date-diff.html:130-150`（日期差/工作日/周数）与 `date-add-subtract.html:145`（日期加减）；年龄侧又被拆为 `age-calculator.html:182/490`（精确年龄+总周数）与 `age-in-days.html:145`（年龄天数）。
- 说明：同一「日期差」语义有 2 个页面、同一「日期加减」有 2 个页面，公式与边界口径（含首日/含周末）在各页分别实现，极易出现「换页结果不同」的信任问题。
- 建议：合并为「日期差 + 日期加减」一页与「年龄」一页；其余保留旧 URL 做重定向并按 §4.6 提死链，避免直接 404。

#### LF-N152（③安全）全站注入无 SRI 的第三方远程脚本 bytegoofy
- 证据：每页 head 内有 `<!-- TOOLBOX-TTZZ -->` 块，例 `length-converter.html:107-117`：动态 `createElement('script')` 并把 `el.src` 指向 `https://lf1-cdn-tos.bytegoofy.com/goofy/ttzz/push.js?...`，插到首个 script 前；无 `integrity`、无 `crossorigin`、无失败回调。`tools/life/` 下 71 个页面均含该块（6 个抽样页全部命中）。
- 风险：无完整性校验的第三方脚本在页面上下文拥有完整 DOM/localStorage 权限，可读取本工具写入的历史记录并向第三方发起请求；与页面 FAQ「数据不会上传到任何服务器」的承诺存在口径冲突（即使脚本当前仅做推送，也无法从仓库侧证明）。
- 建议：确认业务必要性后，改为首方承载或至少加 SRI + `crossorigin` 并在隐私说明中披露第三方域名；若仅为历史推送实验残留，整块移除。

### 统计（AB 批第 2 波）
- 实读 6 页：`length-converter`、`weight-converter`、`temperature-converter`、`timestamp`、`date-diff`、`world-clock`。
- 新增 7 条：①高优 4（LF-N146、N147、N148、N149）/ ②假工具增量 2（LF-N150、N151）/ ③安全 1（LF-N152）。
- 复算口径：长度 1 in=25.4 mm、1 mi=1.609344 km、1 ly=9.460730e+12 km；重量 1 lb=453.59237 g、1 kg=2.204622622 lb；温度 0°C=32°F=273.15K、−40°C=−40°F、491.67°R=0°C；时间戳 1793750400↔2026-11-04T00:00:00Z、1700000000→2023-11-14T22:13:20Z；日期差默认 210/150/60/30、同日 1 天；时区 北京 12:00→东京 13/伦敦 04/纽约前日 23。均为标准值/独立复算，未使用「同单位往返」作证。
- 未做：浏览器交互与截图（LF-N148 需真机复核）、`?lang=en-US` 英文态、移动端、`run_gates.py` 门禁与线上抽样；`world-clock` 非法时区为 node ICU 校验结果（与 Chrome 同用 ICU/CLDR，结论可直接复现）。
- 最高优先：`world-clock.html:360-437`（6 个非法时区 id）、`length-converter.html:328-344`（目标单位未参与换算）、`temperature-converter.html:428-441`（键入即重写，需真机确认）；其次 `date-diff.html:146`/`:272`（排除周末无效）与 `TOOLBOX-TTZZ` 第三方脚本。
