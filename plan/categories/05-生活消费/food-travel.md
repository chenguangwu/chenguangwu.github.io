# 餐饮/旅行 · tools/{food,food-processing,restaurant,baking,travel}（~90 页）

> 2026-11-21 第214批核销：小费空值/负值、糖度逆算范围、营养零分母、预算晚数/餐饮人数、菜单毛利/汇率/成本边界已修；本文件其余项仍在。
>
> 以下仅保留仍待处理/待复核项；已修复项见 `plan/已修复/2026-11-21-*.md`。

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
- 🟢 长期增强（2026-11-21 复核：无缺陷项，转后续批次）

## 2026-11-03 第一轮抽样补充

### 旅行日期跨时区偏移及状态错误（高，确认函数缺陷）
- 问题与证据：`tools/travel/travel-days-counter.html:246-267` 混用 UTC 日期解析、本地 setDate 和 UTC 输出；Node 模拟洛杉矶时区，2024-03-08 点击加 7 天返回得到 03-14 而非 03-15。上海时间 2024-05-12 10:00、返回日期 05-12 时已显示旅行结束；倒序日期亦可输出负天数。真实浏览器时区未复测。
- 影响：`tools/travel/travel-days-counter.html`，行程与天数错误。
- 方案：统一日历日期运算，明确返回日全天状态，拒绝倒序日期；回归夏令时及午夜。可允许用户主动本地保存并清除多个行程，展示倒计时和住宿晚数。

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

## 2026-11-06 旅行工具静态续审（清单 647–648）

- `tools/travel/travel-photo-storage.html:255-292`：天数清空或 0 按 1、照片数或视频时长清空按 0，负数参与计算并仍给存储卡建议；推荐卡容量按平均估算而非最大范围或自身提示的 2–3 倍冗余。容量估算口径及实际可用容量须结合设备核验。
- `tools/travel/visa-requirement-checker.html:371-384,415-450,483-498`：秘鲁、智利等需满足其他签证条件却统一标记为“免签”，筛选及统计把有条件免签计入普通免签，卡片备注才提示条件，容易高估无需额外条件的数量；固定资料可能过时，页面也提示以官方信息为准，本次未核验现行政策。两页仅静态分析，未运行浏览器。

## 2026-11-06 旅行工具静态续审（清单 638–645）

- `tools/travel/jet-lag-recovery.html:172-221,401-417,457-491`：飞行时长虽读取但不参与计划，出发时间未读取；默认北京到北京时 diff=0，时间表计算 `0/0` 被替换为破折号且主结果仍称向西飞行。直接相减固定时区偏移，未处理夏令时及跨日界线最短方向；作息建议须专业复核。
- `tools/travel/luggage-size-checker.html:419-460`：旧 FT-N9 的单边误判已变化，当前在宽高上限为 0 时按三边和判断，需运行回归才能销账。清空或负数输入被当成 0 或直接参与判断，可能输出符合要求；实际航司政策须以航司为准。
- `tools/travel/luggage-size.html:244-260,264-280`：18 寸示例厚 23cm、20 寸厚 24cm，却称可随身；18 寸备注称符合多数航司 55×40×20 内，两者厚度均超过 20cm。航司参考有时效性，未核对实时政策。
- `tools/travel/passport-validator.html`：格式匹配不等于护照真伪或有效性，未进行联网核验。（原未转义注入路径已于第 954 批修复并真机回放验证，从待办删除。）
- `tools/travel/road-trip-gas-cost.html:370-401,404-425,526-537,580-616`：旧 12-N159 的纯电预设已切换为 1.2 元/kWh 并更新主界面标签，不应沿用原油价结论；但历史恢复只调用 calc、不调用 syncUnitLabels，油电标签可能与恢复车辆不符；对比卡固定写 L/耗油量，即使电车也是如此。自定义车辆名注入路径已于第 954 批修复并真机回放验证，从待办删除；其余问题仍未运行注入。
- `tools/travel/timezone-lookup.html`：原 `data-zh` 属性注入路径已于第 954 批修复并真机回放验证，从待办删除；当前时刻把主机时区偏移加到时间戳后又用 `toISOString()`，主机不在 UTC 时额外引入主机偏移（主机 UTC+8、查询 UTC+8 会显示 UTC 时间）。重复 `Asia/Kolkata` 后项覆盖前项使加尔各答无法按城市名检索；固定标准偏移已声明不含夏令时，但 `Asia/Almaty` 的 UTC+6 数据应复核现行偏移。
- `tools/travel/travel-adapter-guide.html:251-303`：搜索按国家名过滤并重绘，插头类型与电压为固定表；未核验国家资料或设备兼容性，转换插头不能替代变压器。

### 2026-11-06 FT-N15 静态续审补充
- `tools/travel/international-tip-calculator.html:182-205,301-315,318-335`：旧 FT-N15 关键代码仍在；货币下拉没有 onchange，单独换币种不会刷新结果。美国酒店/行李员 `[2,5]` 也统一按账单 2%–5% 计算，而页面未区分固定额/比例口径；账单清空按 0、人数清空或 0 按 1，仍输出结论。小费惯例及固定额口径须专业核验，未运行页面。

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
