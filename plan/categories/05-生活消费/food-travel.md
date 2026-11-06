# 餐饮/旅行 · tools/{food,food-processing,restaurant,baking,travel}（~90 页）

## 2026-11-06 酒店小费工具静态续审

### 复制结果漏税，与页面总额不一致（高，代码确认）
- `tools/hotel/tip-calculator.html:139-154,271-285,309-315`：页面总额包含税费，复制函数却只算消费加小费。消费 120、小费 15%、税率 10%、2 人时，页面总额 150、人均 75，复制文本总额 138、人均 69；税率标签又写「仅显示参考」，与实际计入总额矛盾。
- 同一函数以 `||` 将空消费/小费/税率当作 0、空人数当作 1，未阻止负小费和负税率（`:272-292`）。建议统一计算与复制口径、标清税费是否计入，区分空值和合法 0 并校验人数和比例；未运行页面。

## 已知问题
## 功能缺陷
- 烘焙换算缺「面粉含水量/酵母鲜干换算」高频项。
- 旅行缺「多币种行程记账」（手动汇率本地算）。
- 餐厅菜单毛利页缺「定价反推」（目标毛利率→定价）。

## 优化点
- S2 场景：烘焙「6 寸→8 寸换算」「淡奶油打发比例」；旅行「日本 7 天预算表」。
- S3 分步：卡路里页营养素拆解图。

## 受影响范围
- tools/food/、tools/food-processing/、tools/restaurant/、tools/baking/、tools/travel/（~90 页）

## 进度
- 🔴 待开发

## 2026-11-03 第一轮抽样补充

### 旅行日期跨时区偏移及状态错误（高，确认函数缺陷）
- 问题与证据：`tools/travel/travel-days-counter.html:246-267` 混用 UTC 日期解析、本地 setDate 和 UTC 输出；Node 模拟洛杉矶时区，2024-03-08 点击加 7 天返回得到 03-14 而非 03-15。上海时间 2024-05-12 10:00、返回日期 05-12 时已显示旅行结束；倒序日期亦可输出负天数。真实浏览器时区未复测。
- 影响：`tools/travel/travel-days-counter.html`，行程与天数错误。
- 方案：统一日历日期运算，明确返回日全天状态，拒绝倒序日期；回归夏令时及午夜。可允许用户主动本地保存并清除多个行程，展示倒计时和住宿晚数。

### 糖度逆算未收敛仍显示相互矛盾结果（高，确认函数缺陷）
- 问题与证据：`tools/food/syrup-brix-converter.html:318-336,352-383`，输入 SG 2.0000 时原函数输出 100 Brix 和 SG 2，而 100 Brix 用本页正向公式回代约 1.2367；逆迭代限于 0–100，未校验收敛。
- 影响：`tools/food/syrup-brix-converter.html`，页面允许输入范围内结果不自洽。
- 方案：界定模型适用范围并验证回代误差，无解或不收敛时提示；公式适用性另由专业人士核验。

### 零宏量营养素被当碳水 100%（中，确认函数缺陷）
- 问题与证据：`tools/food/nutrition-calculator.html:490-507` 总宏量热量为零时以 `||1` 代替分母，碳水用余数，原函数对全零自定义食物显示 0%、0%、100% 并提示蛋白偏低。
- 影响：`tools/food/nutrition-calculator.html`，无可计算分母却给出比例和判断。
- 方案：零分母时显示不可计算，不给营养比例与评价；可支持用户主动本地保存、编辑和删除自定义食物及其数据来源，不上传。

### 覆盖
- 本次只读抽查以上 3 页，以页面原函数内存 DOM 桩执行为依据；其余餐饮旅行页、真实浏览器、移动端和线上未验证。

## 2026-11-03 续查（并行批）：餐饮与旅行

### FT-N1 分数/负数量不缩放且被误读（高，确认）
- 证据：`tools/food/cooking-converter.html:731` 正则只认 `[\d.]+` 开头。复现：`1/2 杯 糖`×1.5 → num=1、unit 空、name=`/2 杯 糖`，显示「1 杯 → 1.5 杯」；`½ 杯 糖`、`-100 克 面粉` 落 else 原样输出、不缩放无提示。
- 影响：常见的半杯/半勺配方被静默放大，负数不报错。
- 方案：解析混合分数与 Unicode 分数，负数显式拒绝；补单测。
- 工具：`tools/food/cooking-converter.html`

### FT-N2 菜系筛选无效、时间上限静默放宽（高，确认）
- 证据：`tools/food/recipe-generator.html:448-451` 仅排除川/粤；`japanese/western/korean/thai` 的 `substring(0,2)` 永不命中中文标签，全部通过。预设「日料三文鱼」(`:652`) 走 fish 类目，实际出「清蒸鲈鱼/糖醋鲤鱼」。`:467-470` 无匹配时保留原列表，选「15 分钟」仍出 40/90 分钟菜谱。
- 影响：筛选器等同装饰，用户误以为条件生效。
- 方案：用显式菜系标签映射；无结果提示可选菜系；超时不静默回退。
- 工具：`tools/food/recipe-generator.html`

### FT-N3 预算公式与实现相反（高，确认）
- 证据：`:161` 写明「住宿=每晚房价×晚数」「餐饮=每人每天×人数×天数」；`:300-301` 实际 `hotelPerNight*days`、`foodPerDay*days`（不乘人数），`:243` FAQ 又说不乘人数。7 天默认算 7 晚（应 6 晚），2 人餐饮少算一半。
- 影响：总额、人均、占比整体偏移。
- 方案：住宿改独立「晚数」字段（默认天数−1），餐饮乘人数，同步改公式框/FAQ。
- 工具：`tools/travel/travel-budget-calculator.html`

### FT-N4 夏令时切换日偏移取错 1 小时（高，确认）
- 证据：`:367-375` 把当地时刻当 UTC 求偏移，`:338-339` 再回减。Node 复现：纽约 2024-03-10 03:00 → 偏移 -300 → UTC 08:00 → 显示 04:00；正确 UTC 07:00（EDT -240）。
- 影响：DST 前后 1–2 小时误差，跨日可能错一天；与页面「自动处理夏令时」承诺不符。
- 方案：用 `Intl` 两轮求当地时刻偏移（先估后校正），补 DST 边界回归。
- 工具：`tools/travel/timezone-converter-advanced.html`

### FT-N5 饮食记录无日期边界、坏数据白屏（中，确认）
- 证据：`tools/food/food-calorie-counter.html:309` 直接 `JSON.parse(localStorage)` 无 try；`:333-339` 只存时刻无日期，`:366` 仍叫「今日记录」，隔日继续累加；值被写坏即抛异常，`renderFoods()` 不执行。
- 影响：跨日统计失真；一次写坏永久白屏。
- 方案：按 `YYYY-MM-DD` 分桶并清理旧桶；解析失败回退空数组。
- 工具：`tools/food/food-calorie-counter.html`

### FT-N6 历史恢复只重算一个标签页（中，确认）
- 证据：`tools/food/cooking-converter.html:820-831` 恢复全部输入后仅调 `calcIngredient()`；`volAllResult`、`tempMain`、`portionResult` 仍是旧值。
- 影响：恢复的配方与显示结果不一致。
- 方案：恢复后按当前 tab 调对应函数并刷新各 tab 汇总。
- 工具：`tools/food/cooking-converter.html`

### FT-N7 英文态动态结果残留中文（中，确认）
- 证据：`cooking-converter.html:537,645-652` 输出「常用单位换算：/重量约为：」；`recipe-generator.html:481-525` 输出中文菜名/食材/步骤；`travel-budget-calculator.html:306-309` 输出「人均…每天…/交通/住宿」；`timezone-converter-advanced.html:359-363` 拼接「源时区/目标时区/UTC 时刻」。第三层 `i18n/tools/en/{food,travel}/*.json` 无这些整句键，运行时整节点精确匹配无法命中。
- 影响：`?lang=en-US` 下核心输出仍中文。
- 方案：生成时按语言选词表，或把结果容器并入第三层整句键。
- 工具：上述四页

### 留存优化（按页落点）
- `cooking-converter.html`：保存「配方卡」（全 5 tab 值）+ 一键恢复并全量重算，导出 Markdown。
- `food-calorie-counter.html`：日期分桶、保留最近 7 天、一键复制昨日一餐。
- `recipe-generator.html`：一次给 3 个候选而非纯随机；加收藏与购物清单。
- `travel-budget-calculator.html`：晚数独立输入、多套方案并排对比、补分享文本。

### 续查覆盖
- 实读：`tools/food/cooking-converter.html`、`tools/food/food-calorie-counter.html`、`tools/food/recipe-generator.html`、`tools/food/convert-ratio-seasoning.html`、`tools/travel/travel-budget-calculator.html`、`tools/travel/timezone-converter-advanced.html`。
- `convert-ratio-seasoning.html:168` 单行实现、`calc()` 恢复后正常重算，未发现数值缺陷；仅支持单一基准量，无多调料清单，属功能缺口（中，确认）。
- 全部结论来自源码与 Node 复算；真实浏览器、移动端、线上英文态未验证。

## 2026-11-03 续查（并行批 J）

### FT-N8 配方缩放器默认示例含字面 `\n`，5 行配方只解析出 1 行（高，确认）
- 描述：`tools/baking/recipe-scaler.html:113` 的 textarea 初值中写的是字面反斜杠加 n（不是真实换行）；`:211` 却按真实换行 `split(/\n/)`。结果整段被当成一行。
- 证据：Node 复现文件原值：`lines=1`，正则 `:216` 解析为 `name=面粉`、`val=200`、unit 为「g\n糖=100g\n鸡蛋=2个\n牛奶=150ml\n黄油=50g」（把后 4 项全吞掉），输出仅「面粉：300g\n糖=100g…」一条；`:227` resetForm 同样写入字面 `\n`，重置后仍错。页面示例表 `:165-172` 展示 5 行正常结果，与实际输出矛盾。
- 影响：核心功能失效，倍数只作用于第 1 项，用户看到单行乱码。
- 方案：初值改用真实换行（或 JS 赋值时用 `\n` 转义），解析前把字面 `\n` 归一成换行；未解析行给可见提示。

### FT-N9 托运按「三边和」的航司被按单边判断，恒不通过（高，确认）
- 描述：`tools/travel/luggage-size-checker.html:436-445` 对所有航司都用 `l<=al+1 && w<=aw+1 && h<=ah+1`；而国际航司 checkin 数据是 `[158,0,0,23]`（158 为三边和），宽/高限值为 0。
- 证据：`:439` 的 `maxSum` 算出后从未使用。Node 复现：55×40×20cm、7kg 选国泰/新航/全日空 → `sizeOk=false`（`40<=0+1` 不成立），显示「❌ 不符合」，而三边和 115 ≤ 158 本应通过。
- 影响：约 15 家「三边和」口径的国际航司托运判定永远失败，随身/托运对比结论失真。
- 方案：`aw/ah` 为 0 时改用 `l+w+h <= al`；「接近超限」同样按和判定；非零维度航司保留逐边比较。

### FT-N10 百分比输入框每敲一键整表重绘，无法连续输入（高，确认）
- 描述：`tools/baking/baker-percentage.html:304` 每个百分比输入绑定 `oninput="updatePct(...)"`；`:315-320` 的 updatePct 调 `renderTable()`；`:293-309` 用 `body.innerHTML=html` 重建整个 tbody，当前聚焦的 input 被替换。
- 证据：源码路径确定：键入第 1 个字符 → 重绘 → 原 input 不在 DOM，后续击键无处落下。例如在「水 65」框输入 `12`，实际只能录入 `1`，需再点一次才能补 `2`。Node 仅验证了重建路径，浏览器焦点行为未实测。
- 影响：调百分比主流程基本不可用，自定义配料比例难以输入。
- 方案：input 事件只更新 `ingredients[idx].pct` 与结果单元格，不重建 tbody；或重建后按 idx 恢复 focus/selection。

### FT-N11 目标毛利率边界未校验且 0 被静默改成 60（中，确认）
- 描述：`tools/restaurant/menu-pricing.html:141` 目标毛利率 `min=1 max=95`（HTML 属性不阻止键入）；`:244` `parseFloat(...)||60` 把 0 当空值回退；`:247` 只拦 `>=99`。
- 证据：Node 复现（食材 12、人工 20%、固定 3）：margin=-5 → 售价 16.57、毛利 -0.83；margin=100 → 售价 0、毛利 -17.4；margin=0 实际按 60 算得 43.50。另 `:180-238` 两个「相关工具」区块重复渲染同一组 6 条链接。
- 影响：可产出低于成本价/零售价且无提示；0% 目标被悄悄改写；页面出现重复模块。
- 方案：限定 1–95（或 1–99）并显式报错；用 `isNaN` 判空而非 `||`；删掉重复的相关工具区块。

### FT-N12 放大模具时百分比文案多算了 100 个百分点（中，确认）
- 描述：`tools/baking/mold-volume.html:382-385` 放大分支输出「需增加 (ratio*100)%」，把「增至」写成「增加」。
- 证据：Node 复现 6 寸(15×7)→8 寸(20×7)：V=1237→2199，ratio=1.78，页面提示「需增加 178% 的面糊量」；实际只需增加 78%（或增至 178%）。缩小分支 `:385` 的「需减少至原配方的 178%」口径正确，可见仅放大分支写错。
- 影响：按提示加 178% 会得到 2.78 倍面糊，远超目标容积，易溢出。
- 方案：改为「需增加 (ratio-1)*100%」，两分支统一为「需调整至 ratio*100%」。

### FT-N13 汇率 0/空/负数未校验，反向金额与符号错误（中，确认）
- 描述：`tools/travel/currency-cheat-sheet.html:457` 用 `+rate.value||defaultRate`；`:189` 汇率输入无 `min`；`:466`、`:483` 直接用该值相乘/相除。
- 证据：Node 复现：清空或输入 0 → 静默回落 7.20（底部仍宣称「当前汇率」）；输入 -5 → ¥100 显示 -500，正反向金额均为负。
- 影响：错误汇率被当成有效牌价，速查表金额符号与换算方向相反。
- 方案：`isNaN` 判空并要求 `rate>0`，非法时显示占位与提示而非回退默认值；导出路径同样拦截。

### FT-N14 出成率/份数越界被静默兜底，成本失真（中，确认）
- 描述：`tools/restaurant/dish-cost-card.html:273-276` 份数 `||1`、出成率 `||100`；`:141` `max=100` 不约束键入；`:289-292` 直接用该值计算。
- 证据：Node 复现默认食材原料成本 10.00 元：出成率 95% → 单份 10.53；改 150% → 6.67（低估 37%）；改 0 → 静默按 100% 得 10.00；份数 0 → 按 1。
- 影响：出成率 >100 或为 0 时成本、毛利率整体偏移，且无任何警告。
- 方案：出成率限 1–100、份数 ≥1，越界显式提示；不要用 `||` 兜底。

### FT-N15 小费页币种选项取值重复，负账单输出负小费（低，确认）
- 描述：`tools/travel/international-tip-calculator.html:200-206` 中 JPY 与 CNY 两个 option 的 `value` 都是 `¥`，`cur` 无法区分；`:321` 账单 `||0` 不校验负数；`:301` 美国餐厅为 `[15,20,25]`，`:325` 解构只取前两项。
- 证据：Node 复现账单 -100、美国餐厅 → 小费区间 `-15 ~ -20`、总计 -117.5。
- 影响：日元/人民币选择器等同失效；异常账单给出负小费；25% 档数据永不生效。
- 方案：option value 用 ISO 代码、展示层再取符号；账单要求 ≥0；数据改为 `{min,max}` 结构去掉多余元素。

### 留存优化
- `recipe-scaler.html`：配方行支持「目标份数→倍数」直算，保存多套配方卡并导出购物清单。
- `luggage-size-checker.html`：保存「我的行李箱」档案，一键跨航司对比；托运同时展示三边和与单边双口径。
- `baker-percentage.html`：局部更新输入与结果、按面粉量反推总重、保存配方模板。
- `menu-pricing.html`：三档毛利率并排对比、含税价、成本构成占比。
- `mold-volume.html`：内置常见模具库，按 60/70/80% 填充率给区间。
- `currency-cheat-sheet.html`：汇率有效性校验、多币种同屏速查、离线保存最近牌价。
- `dish-cost-card.html`：多菜品成本卡管理与批量导出。
- `international-tip-calculator.html`：按币种小数位取整、增加「账单已含服务费」开关。

### 续查覆盖
- 本次实读并复算 8 页：`tools/baking/recipe-scaler.html`、`tools/baking/baker-percentage.html`、`tools/baking/mold-volume.html`、`tools/restaurant/menu-pricing.html`、`tools/restaurant/dish-cost-card.html`、`tools/travel/luggage-size-checker.html`、`tools/travel/currency-cheat-sheet.html`、`tools/travel/international-tip-calculator.html`。
- 证据均来自源码行号与 Node 同逻辑内存复算；未做真实浏览器、英文态、移动端、线上与门禁验证。
- 其余餐饮/旅行/食品加工页仍未覆盖，建议后续批次继续。
