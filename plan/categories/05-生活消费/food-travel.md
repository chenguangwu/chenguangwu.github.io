# 餐饮/旅行 · tools/{food,food-processing,restaurant,baking,travel}（~90 页）

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
