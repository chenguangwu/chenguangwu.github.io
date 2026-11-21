# 餐饮/旅行 · tools/{food,food-processing,restaurant,baking,travel}（~90 页）

> 2026-11-21 第215批核销：旅行天数日历/状态、时区夏令时两轮偏移、配方分数解析与恢复全量重算、菜系/时间筛选已修。
>
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

### 覆盖
- 本次只读抽查以上 3 页，以页面原函数内存 DOM 桩执行为依据；其余餐饮旅行页、真实浏览器、移动端和线上未验证。

## 2026-11-03 续查（并行批）：餐饮与旅行

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
