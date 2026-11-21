# 生活综合 · tools/life（70 页）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

## 功能缺陷
- age 系页无「法定年龄事件」联动（投票/驾车/退休倒计时）。

## 优化点
- S2 场景：「宝宝 100 天纪念」「结婚 10 周年」；S4 分享卡：生日/年龄卡。

## 受影响范围
- tools/life/（70 页）

## 进度
- 🟢 长期增强（2026-11-21 复核：无缺陷项，转后续批次）

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

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 10 页（`tools/life/length-converter.html`、`weight-converter.html`、`volume-converter.html`、`area-converter.html`、`speed-converter.html`、`time-converter.html`、`event-countdown.html`、`holiday-calendar.html`、`age-in-days.html`、`date-difference-calculator.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### LF-N60 「月」系数与页面参照说明相差约一天（低，确认缺陷）
- 描述：实现与公式区均为 `month: 2629800`（30.4375 天 = 365.25/12），但页面底部仿实物参照的 FACTS 写「『月』取平均朔望月 29.53 天」，两种口径差 0.9 天。
- 证据：`tools/life/time-converter.html:279`、`:149`、`:530`
- 复现：1 月 → 实际 30.4375 天；同页 FACTS 声称 29.53 天（对应 2551392 s，而非 2629800 s）。
- 影响：`tools/life/time-converter.html`；用户按参照说明复核会得出与结果不一致的结论，月子/产假类场景按 29.53 天理解会少算约 1 天。
- 方案：FACTS 改为「月按 365.25/12 = 30.4375 天」，或增加「农历月（29.53 天）」切换并同步系数。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（`tools/life/number-to-chinese.html`、`tools/life/data-rate-converter.html`、`tools/life/report-profit.html`、`tools/life/frequency-converter.html`、`tools/life/energy-converter.html`、`tools/life/power-converter.html`、`tools/life/flow-rate-converter.html`、`tools/life/concentration-converter.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 页（`tools/life/detector-checker-strength.html`、`countdown-timer.html`、`countdown-2.html`、`color-name-finder.html`、`generator-random-1.html`、`cycle-4.html`、`reminder-cycle.html`、`cycle-pruning-lawn.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

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
