# 营销/销售 · tools/{marketing,advertising,sales}（~70 页）

## 已知问题

## 功能缺陷
- ROI 页缺「多渠道对比表」（同预算分三渠道敏感性）。
- 广告缺「A/B 测试显著性判定」（样本量+转化率→p 值，纯前端可算）。

## 优化点
- ✅ S2 场景（2026-10-26）：ad-roi 加「抖音千川」预设按钮（CPM 模式 预算1万/CPM45/CTR1.8%/CVR4%/客单260/毛利45% ⇒ ROAS 4.16 / ROI 26.5%）；funnel-calculator 加「私域 SOP」模板（进群2万→加微1200→首单180→复购45）。verify marketing 117→118、判别器 0 逃生、Playwright 真机 zh 正常 + EN 零 CJK、门禁 218/218。
- S3 分步：盈亏平衡点图解。

## 受影响范围
- tools/marketing/（46）、tools/advertising/、tools/sales/

## 进度
- 🟡 续批中（S2 已落地；剩余：多渠道对比表 / A-B 显著性缺口确认 / S3 盈亏平衡图解）

## 2026-11-03 第一轮抽样补充

### 零贬损者时比值被算成有限数（中，确认函数缺陷）
- 问题与证据：`tools/marketing/marketing-nps-calculator.html:199-210,470-471` 推荐者 10、贬损者 0 时，`p/(d||1)` 输出比值 10.00；原函数在内存 DOM 桩复现。NPS 主值仍为 100。
- 影响：`tools/marketing/marketing-nps-calculator.html`，无法表达无贬损者的比值被误写成普通数值。
- 方案：零分母显示不适用或无贬损者，人数按非负整数校验。

### 漏斗零基数仍输出转化率（中，确认函数缺陷）
- 问题与证据：`tools/sales/conversion-funnel.html:272-298` 前一阶段为 0、后一阶段为 100 时以 `||1` 作为分母，原函数显示环节转化率 10000%、整体转化率 0%。
- 影响：`tools/sales/conversion-funnel.html`，不可计算的比例被当有效结果。
- 方案：零基数显示不可计算，后一阶段人数超过前序时提示；可允许用户主动保存、清除各期具名阶段快照，比较环节变化。

### 覆盖
- 本次抽查上述 2 页，原函数内存 DOM 桩，未实测浏览器、线上和其余营销销售页面。

## 2026-11-03 续查（并行批 F）

### MS-F1 叠加折扣的「折扣」输入标度与标签自相矛盾，负值/超 100 无拦截（高，确认）
- 描述：输入框标签写「折扣（如 8 = 8折）」，但计算与预设按百分数口径（80 = 8折）；用户按标签输入 8 会得到原价的 8%，即 0.8 折。同一输入还允许键盘录入负数与 >100，直接产出负价或加价结果。
- 证据：`tools/sales/stacked-discount.html:263`（标签「折扣（如 8 = 8折）」，`min=0 max=100`）、`:280-283`（预设 rate 80/85，暗示百分数口径）、`:300-301`（`cur = cur * (d.value/100)`）、`:275`（新增折扣默认 90）。node 内存复算：原价 100、折扣 8 → 最终价 `8.00` 元（等效 0.8 折）；原价 100、折扣 -50 → 最终价 `-50.00` 元；折扣 120 → 价格上浮。
- 影响：`tools/sales/stacked-discount.html`。按标签操作即错 10 倍，是本页最主要的功能性缺陷；负价会连带污染下方图表与 CSV 导出。
- 方案：标签统一改为「折扣率（%，80 = 8折）」并补 `0–100` 提示，或改为「几折」口径（`value*10`）。计算前钳制 `0 ≤ value ≤ 100`，越界给出提示而非静默计算。

### MS-F2 等效折数被写成「省多少折」，与同页示例口径冲突（中，确认）
- 描述：结果副标题用 `总优惠/原价×100` 得到的「省百分比」直接拼成「相当于 X 折」，导出列更用 `总优惠/原价×10` 拼「X 折」。语义应为「成交价是几折」，两处都算成了优惠幅度。
- 证据：`tools/sales/stacked-discount.html:309-313`（`effRate=(totalSave/price*100)`，输出 `相当于 ${effRate} 折`）、`:350-352`（`(totalSave/price*10).toFixed(2)+' 折'`）。node 复算：原价 500、8 折后满 300 减 50 → 成交 350 元、省 150 元，页面显示「相当于 30.0 折」，导出显示「3.00 折」；而 `:199` 的深度解析原文写「相当于原价的 7 折」「省 30%」，形成同页三套口径。
- 影响：`tools/sales/stacked-discount.html` 结果区与 CSV。对外报价/核算时「30 折」与「3 折」都会被误读。
- 方案：统一换算为 `成交价/原价×10`（此例 7.0 折），标签写「成交价 ≈ 7.0 折（省 30%）」；导出列同步改为同一换算。

### MS-F3 阶梯提成的档位上限非单调时重复计佣（中，确认）
- 描述：`getTiers()` 只把最后一档强制设为 `Infinity`，不校验中间档上限递增；`calcTiered()` 用 `Math.min(sales, cap) - prevCap` 分段，上一档上限大于下一档时区间为负、`prevCap` 回退，导致同一段业绩被重复计入。
- 证据：`tools/sales/commission-calculator.html:384-400`（读取档位、仅末档强制 Infinity）、`:402-415`（`seg=Math.min(sales,cap)-prevCap`，`seg>0` 才累加，但 `prevCap` 仍被赋成较小值）。node 复算：档位上限 100000/50000/Infinity、比例 3%/5%/8%、销售额 200000 → 输出佣金 `15000`；按正确分段（0–10万×3%、10万以上×8%）应为 `11000`，多计 4000 元。
- 影响：`tools/sales/commission-calculator.html`「阶梯提成」模式，用户手动改档（含 `+ 添加阶梯` 后把旧末档填成有限值）时可能虚增佣金。
- 方案：读取档位后按上限升序排序并校验严格递增；遇逆序档位直接提示「区间上限须递增」，不进入计算。

### MS-F4 「利润率」输入实为加价率，且页内参考表公式与实现相反（中，确认）
- 描述：售价计算模式用 `成本×(1+输入率)`，输入率是加价率，但输入框标签与结果卡都叫「利润率」；同页「公式与标准引据」表却写 `售价 = 成本/((1-毛利率))`，与实现相反。公式框内虽有加价率口径的括注，但标签层仍误导。
- 证据：`tools/sales/cost-price-margin.html:145`（`label 利润率（%）`）、`:272-275`（`const p=cost*(1+margin)`，输出「利润率（毛利/售价）」「加价率（毛利/成本）」）、`:203`（参考表 `cost/(1-margin)`）。node 复算：成本 60、输入 40 → 售价 `84.00`、利润率输出 `28.6%`，即「输入 40% 利润率」与「输出 28.6% 利润率」同屏并存。
- 影响：`tools/sales/cost-price-margin.html`。用户按「利润率 40%」定价会得到低于预期的售价；参考表口径与实现相反，交叉核对时必然对不上。
- 方案：输入标签改为「加价率（成本加成 %）」，或增加口径切换（加价率/毛利率）。参考表公式改为 `售价=成本×(1+加价率)`，并保留「毛利率 = 加价率/(1+加价率)」的换算说明。

### MS-F5 均分/权重分解的合计行与逐行取整合计不一致，负权重无拦截（中，确认）
- 描述：逐行目标用 `fmt()`（`Math.round` 取整）显示，合计行用未取整的 `sumTarget` 取整显示；成员数不能整除总目标时，用户看到的逐行之和与合计差 1 个单位。权重模式还允许负权重，可产出超过总目标的正目标与负目标。
- 证据：`tools/sales/target-breakdown.html:357`（`fmt = Math.round(n).toLocaleString`）、`:315-322`（`share` 未取整、合计用 `fmt(sumTarget)`）、`:324-327`（逐行 `fmt(r.target)`、占比 `toFixed(1)`）。node 复算：总目标 1000、3 人均分 → 逐行显示 333/333/333（合计 999）、合计行显示 `1,000`、占比 33.3%×3=99.9% 但合计行写 `100%`；权重 30 与 -10、总目标 1000 → 目标 `1500` 与 `-500`。
- 影响：`tools/sales/target-breakdown.html` 结果表与 CSV。评审会上「合计对不上」会被误判为分解错误；负目标无法解释。
- 方案：逐行与合计统一保留 1–2 位小数（或对合计做「尾差归入最大项」），并在权重输入处校验 `≥0`，合计为 0/负数时提示改用均分。

### MS-F6 无固定成本且毛利为零时仍断言「盈亏平衡销量 1 件」，竞品价可算出负售价（中，确认）
- 描述：`breakEven` 仅在 `grossProfit>0` 时计算，但 `fixedCost=0` 走的是另一分支，无条件输出「盈亏平衡销量：1 件（无固定成本时，售价 > 成本即盈利）」。当售价等于或低于成本时该断言与事实相反。竞品参照模式对偏差率不设下限，可得出负售价。
- 证据：`tools/sales/price-calculator.html:397-399`（`breakEven = grossProfit>0 ? Math.ceil(fixedCost/grossProfit) : Infinity`）、`:432-440`（`fixedCost>0` 才判 Infinity，否则固定输出 1 件）、`:378-383`（`deviation` 仅校验 `isNaN`）。node 复算：成本 100、加成 0%、固定成本 0 → 建议售价 100、毛利 0，页面输出「盈亏平衡销量：1 件」；竞品价 100、偏差 -150% → 建议售价 `-50.00`。
- 影响：`tools/sales/price-calculator.html`。零毛利场景给出错误的保本结论；负售价可被直接抄进报价单。
- 方案：`fixedCost=0` 分支改为按 `grossProfit` 判定：`>0` 才说「1 件即可盈利」，`=0` 说「不盈不亏」，`<0` 说「每卖一件亏损，无法保本」。偏差率补 `-100 ≤ deviation` 下限。

### MS-F7 目标利润率 ≥ 毛利率时目标 ROAS 静默消失；无效提示指向错误字段（中，确认）
- 描述：`targetRoas` 只在 `0 < targetProfit < margin` 时计算，其余情况整块卡片不渲染、无任何说明；毛利率输入合法但售价为空/非法时，统一提示「请输入有效数值（毛利率0-100之间）」，指错字段。
- 证据：`tools/marketing/marketing-break-even-roas.html:386-389`（仅校验 price/margin 的 `isNaN`，提示文案只提毛利率）、`:396-399`（`targetProfit>0 && targetProfit<margin` 才赋值）、`:425-431`（`targetRoas` 为空则整卡不渲染）。node 复算：毛利率 40、目标利润率 50（或 40）→ `targetRoas = null`；毛利率 40、当前 ROAS 3 → 净利率 `6.67%`，与页面展示口径一致。
- 影响：`tools/marketing/marketing-break-even-roas.html`。用户以为「填了目标利润率没生效」，实际是数学上不可达，页面未告知。
- 方案：`targetProfit ≥ margin` 时渲染占位说明「目标利润率须低于毛利率（当前毛利率 40%）」；错误提示按具体空字段分别给出，售价为空时提示「请输入产品客单价」。

### MS-F8 LTV 为 0 时仍输出 0:1、-100% ROI 与破折号回本周期；回本周期硬编码 36 个月（中，LTV 校验确认 / 寿命假设待验证）
- 描述：`calc()` 只拒绝 `cac<=0`，`ltv=0` 照常进入计算：比率 0.00:1、ROI -100%、`paybackMonths = cac/(ltv/36) = Infinity`，经全局 `Infinity→—` 替换后显示「— 个月」。此外回本周期以 `LTV/36`（隐含 36 个月生命周期、月净贡献均摊）推算，但页面无寿命输入、也未声明该假设。
- 证据：`tools/marketing/marketing-ltv-cac-ratio.html:418-430`（仅 `cac<=0` 拦截；`paybackMonths = cac/(ltv/36)`）、`:456`（`${paybackMonths.toFixed(1)} 个月`）、`:485`（结果串 `replace(/Infinity|NaN/g,'—')`）。node 复算：LTV 0、CAC 500 → ratio `0.00`、ROI `-100.0%`、payback `Infinity`（渲染为「— 个月」）；LTV 3000、CAC 500 → 回本 `6.0` 个月（= 500÷(3000/36)，即假定 3000 元分 36 个月回收）。
- 影响：`tools/marketing/marketing-ltv-cac-ratio.html`。零 LTV 是明显无效输入却给出完整结论卡；回本周期在寿命≠36 个月时系统性偏离（如 12 个月寿命应为 2 个月）。
- 方案：补 `ltv<=0` 校验并提示；新增「客户生命周期（月）」输入（默认 36）替代硬编码，或把该项改名为「按 36 个月寿命估算的回本月数」并在卡片注明假设。

### 留存优化
- `tools/sales/stacked-discount.html`：折扣层支持拖动排序（当前只能删后重加才能换顺序），并在结果区并列展示「先折后减 / 先减后折」两种顺序的成交价差，正好呼应页面已写「顺序不同结果不同」的示例。
- `tools/sales/commission-calculator.html`：阶梯档位表增加「区间（上档—本档）× 比例 × 该段佣金」的分解列，让 15000 这类合计可被逐段核对；同时保存档位配置到 localStorage，避免每次重填。
- `tools/sales/cost-price-margin.html`：把「利润率 ↔ 加价率对照表」改为按当前输入高亮对应行，并在结果卡加一行「若按毛利率口径 40%，售价应为 …」，直接消除两种口径的混淆。
- `tools/sales/target-breakdown.html`：结果表增加「差额」列（逐行合计 − 总目标）并允许一键把尾差补给权重最大者，替代当前只能眼看合计对不上。
- `tools/sales/price-calculator.html`：四种定价模式并列对比（同一成本/固定成本下四个建议售价与毛利率），当前需切换模式逐次记录。
- `tools/marketing/marketing-break-even-roas.html`：把「盈亏平衡 ROAS」「目标 ROAS」「当前 ROAS」三值画成一条数轴并标出所处区间，替代纯卡片陈列；参考表可按用户输入的毛利率高亮所属行业行。
- `tools/marketing/marketing-ltv-cac-ratio.html`：增加 LTV 构建器（客单价 × 年购买频次 × 寿命年数 × 毛利率），让 LTV 从「拍一个数」变成可追溯推导，同时把 36 个月假设显式化。

### 续查覆盖
- `tools/sales/stacked-discount.html`
- `tools/sales/commission-calculator.html`
- `tools/sales/cost-price-margin.html`
- `tools/sales/target-breakdown.html`
- `tools/sales/price-calculator.html`
- `tools/marketing/marketing-break-even-roas.html`
- `tools/marketing/marketing-ltv-cac-ratio.html`
- 本次仅做源码阅读与 node 内存复算（按页面 `calc()` 表达式重写同名函数取输出），未做浏览器、英文态、移动端、门禁或线上验证；`marketing-ltv-cac-ratio` 的 36 个月寿命属产品假设，标注为待验证。

## 2026-11-03 续查（并行批 J）

### MS-J1 CPA 页转化率与毛利率无上界，可算出 200% 转化率与超收入毛利（中，确认）
- 描述：`calc()` 只校验营销总花费与新增客户数，点击量、毛利率两个百分数输入没有业务上界。新增客户数超过点击量时转化率直接 >100%；毛利率手输 >100 时毛利超过收入，ROI 被同步放大。
- 证据：`tools/marketing/marketing-cpa-calculator.html:425`（仅校验 `totalSpend`/`newCustomers`）、`:432`（`cvr = (newCustomers / clicks) * 100`）、`:435-436`（`grossProfit = revenue * (grossMargin / 100)`）、`:216`（`max="100"` 只是表单约束，不阻止 `oninput` 计算）。node 内存复算：点击量 100、新增客户 200 → 转化率 `200.00%`；毛利率 150 → 毛利 `89,700`（收入 59,800）。
- 影响：`tools/marketing/marketing-cpa-calculator.html`。CVR 200% 被当作真实效率；毛利超收入会让 ROI 与「净盈利」结论失真。
- 方案：`clicks > 0` 时校验 `newCustomers <= clicks`，超出提示「新增客户数不能超过点击量」；毛利率钳制 `0–100`，越界提示而非静默计算。

### MS-J2 ROAS 页亏损时「盈亏平衡 ROAS」输出负值（中，确认）
- 描述：盈亏平衡 ROAS 用 `100 / 当前毛利率` 计算，而当前毛利率在亏损时为负数，于是输出负数倍率；收入为 0 时还会得到 `-0.00x`。该值在营销语境中没有意义，页面也没有「当前亏损、无盈亏平衡点」的说明。
- 证据：`tools/marketing/marketing-roas-calculator.html:449-452`（`profitMargin = (revenue - spend) / revenue * 100`）、`:498`（`(100 / (profitMargin || 1)).toFixed(2)`）。node 内存复算：花费 5,000、收入 4,500 → ROAS `0.90x`、毛利率 `-11.1%`、盈亏平衡 ROAS `-9.00x`。
- 影响：`tools/marketing/marketing-roas-calculator.html`。亏损投放会看到「盈亏平衡 ROAS -9x」，无法据此判断要提升到多少才保本。
- 方案：`profitMargin <= 0` 时显示「当前为亏损，需毛利率 >0 才有盈亏平衡 ROAS」，或改用 `1 / 目标毛利率` 并让用户输入目标毛利率；标签注明「按收入口径毛利率」。

### MS-J3 CAC 页算了回收期却从不展示，且 36 个月假设写死（中，确认）
- 描述：`paybackMonths` 在 `calc()` 中已算出，但结果模板没有任何位置引用它；同页深度解析却给出「回收期 ≈0.6 个月」的完整算例，形成「说明里有、结果里没有」的断层。该值还隐含固定 36 个月客户生命周期，页面无输入也无声明。
- 证据：`tools/marketing/marketing-cac-calculator.html:419`（`paybackMonths = cac / (ltv / 36)`）、`:446-456`（LTV 卡片只渲染 LTV、比率、健康状态、ROI，无回收期）、`:363`（深度解析「CAC=50、LTV=3000（按 36 个月摊）→ 回收期≈0.6 个月」）。node 内存复算：CAC 500、LTV 3,000 → `6.00` 个月，页面任何位置均不出现。
- 影响：`tools/marketing/marketing-cac-calculator.html`。用户读完深度解析后找不到对应结果；生命周期不等于 36 个月时该口径也无法调整。
- 方案：在 LTV:CAC 表补一行「回收期（按 36 个月摊）」并展示 `paybackMonths.toFixed(1)`；把 36 提为「客户生命周期（月）」输入（默认 36），或在该行标注假设。

### MS-J4 流失率页期末客户数超口径时出现负流失率与双负号（中，确认）
- 描述：`lost = start + newC - end` 未校验 `end <= start + newC`。期末客户数大于「期初+新增」时流失人数为负，流失率变负、留存率 >100%，表格还把负的 `lost` 拼成 `-${lost}`，渲染出「--50」两个负号。
- 证据：`tools/marketing/marketing-churn-rate.html:394-397`（`lost`、`churnRate`、`retentionRate` 均无下界校验）、`:419`（流失人数展示）、`:427`（`-${lost.toLocaleString()}`）。node 内存复算：期初 1,000、期末 1,050、新增 0 → 流失 `-50`、流失率 `-5.00%`、留存率 `105.00%`、表格「流失客户数 --50」。
- 影响：`tools/marketing/marketing-churn-rate.html`。口径误填或跨期统计时，页面给出「负流失、105% 留存」的自相矛盾结论，且预期生命周期变为 `—`。
- 方案：校验 `end <= start + newC`，超出提示「期末客户数不能超过期初+新增（当前上限 X）」；流失人数为负时展示 0 并标记口径异常，而不是拼出双负号。

### MS-J5 转化率页未拦截「转化数 > 访问量」，出现 150% 转化率与负流失率（中，确认）
- 描述：只校验访问量 >0，转化数可以随意超过访问量。页面随即输出 >100% 的 CVR、负的「未转化数」和负的「流失率」，且全部按正常指标配色展示。
- 证据：`tools/marketing/marketing-conversion-rate-calculator.html:394`（仅校验 `visitors` 与 `conversions` 是否为数字、`visitors > 0`）、`:399`（`cvr = conversions / visitors * 100`）、`:444`（`visitors - conversions`）、`:471`（`100 - cvr`）。node 内存复算：访问 100、转化 150 → CVR `150.00%`、未转化 `-50`、流失率 `-50.0%`。
- 影响：`tools/marketing/marketing-conversion-rate-calculator.html`。跨渠道重复计数或误填时，页面把不可能的比例当成有效结果，CPA 与 ROI 也随错误转化数计算。
- 方案：校验 `0 <= conversions <= visitors`，超出提示；若业务上确实存在「一次访问多次转化」，则增加「转化次数口径」开关并相应改分母说明。

### MS-J6 销售预测页置信区间用历史值标准差而非残差，且两句文案自相矛盾（中，确认）
- 描述：`forecast()` 的 95% 区间固定用 `std(hist)`（历史观测值的离散度），而 `linreg()` 已算出残差标准差 `sigma` 却从未使用。页面一处写「基于历史残差标准差」，另一处写「以历史标准差 σ」，两种口径并存。完美线性趋势会被展示成很宽的区间。
- 证据：`tools/sales/sales-forecast.html:240`（文案「基于历史残差标准差的近似 95% 置信区间」）、`:275`（文案「以历史标准差 σ 给出 ±1.96σ」）、`:410-411`（`sigma = std(residuals)` 返回）、`:485-488`（实际 `sigma = std(hist)` 并据此生成 `ci`）、`:537`（结果行渲染 `r.ci`）。node 内存复算：历史 [100,110,120] → 线性拟合预测 130、残差 σ `0.00`，页面区间却是 `[110.4, 149.6]`（±1.96×历史 σ 10）。
- 影响：`tools/sales/sales-forecast.html`。趋势平稳的数据被误判为高度不确定；线性回归分支的残差信息被丢弃，区间宽度与模型拟合质量无关。
- 方案：线性回归用 `lr.sigma`，MA/WMA/EMA 用滚动一步预测残差；无法计算残差时（样本过少）明确标注「以历史波动近似」。两句文案统一为同一口径。

### MS-J7 折扣率页折后价高于原价时输出负折扣率与「12 折」（中，确认）
- 描述：由折后价反推折扣的模式只校验 `salePrice >= 0`，没有要求 `salePrice <= origPrice`。折后价高于原价时折扣率为负、折数变成 >10 折、节省金额为负却仍用绿色展示；「节省金额」反推模式在 `saveAmount > origPrice` 时同理会得到负折后价。
- 证据：`tools/marketing/marketing-discount-rate.html:438-446`（仅拦截 `origPrice <= 0 || salePrice < 0`）、`:458`（`discountZhe = 10 - discountPct / 10`）、`:484-486`（折数、节省金额渲染）。node 内存复算：原价 100、折后价 120 → 折扣率 `-20.0%`、折数 `12.0折`、节省 `-¥20.00`（绿色）。
- 影响：`tools/marketing/marketing-discount-rate.html` 的模式二与模式三。录入「加价」或记错原价时，页面把涨价解释成 12 折优惠，报价核对会直接读错。
- 方案：模式二校验 `0 <= salePrice <= origPrice`，模式三校验 `0 <= saveAmount <= origPrice`；越界提示「折后价不能高于原价」。百分比模式同步钳制 `0 <= discountPct <= 100`。

### MS-J8 移动平均页 WMA 预测权重方向与历史计算相反（高，确认）
- 描述：历史 WMA 给最近一期最大权重（`data[i-j] * (n-j)`），但预测分支按 `seg2[w] * (seg2.length-w)` 计算，`seg2[0]` 是最旧值却拿到最大权重，方向整体颠倒。结果是同一窗口下「移动平均」列与「下一期预测」值不一致，趋势上升时预测被系统性压低。
- 证据：`tools/sales/moving-average.html:285`（历史 WMA：`s += data[i-j] * (n-j)`，最新权重 n）、`:306-309`（预测 WMA：`ws += seg2[w] * (seg2.length-w)`，最旧权重最大）、`:130`（公式框「WMA：权重 w = N−j（近期权重大）」）、`:206`（深度解析算例写「(110×1+130×2+140×3)/6 = 133.33」）。node 内存复算：窗口 [110,130,140] → 历史 WMA `131.67`、预测 WMA `121.67`，正确预测应为 `131.67`（深度解析的 133.33 本身也算错，按 110/130/140 应为 131.67）。
- 影响：`tools/sales/moving-average.html` 的 WMA 模式。下一期预测值偏低（上升趋势）或偏高（下降趋势），且与页面同时展示的移动平均线脱节，用户会以为模型在正常外推。
- 方案：预测分支改为与历史同口径（`seg2[w] * (w+1)`，越靠后权重越大），或抽成同一个 `wmaAt(series, n)` 函数供历史与预测复用；同时把深度解析示例的 133.33 修正为 131.67。

### MS-J9 窗口 N 大于历史期数时移动平均表整列为空且无提示（中，确认）
- 描述：SMA/WMA 的移动平均序列循环从 `i = n-1` 开始，`n > data.length` 时循环一次都不执行，`maSeries` 为空；页面只判断「数据 <2 期」就放行，结果表只剩预测行，没有任何说明。
- 证据：`tools/sales/moving-average.html:147`（`window` 允许 `max=20`）、`:272`（仅 `if(data.length<2) return`）、`:278`（`for(var i=n-1;i<data.length;i++)`）、`:324-327`（按 `maSeries` 生成行）。node 内存复算：数据 5 期、N=10 → `maSeries` 长度 `0`，预测值仍输出 `3`（全序列均值），表格无任何「移动平均」历史行。
- 影响：`tools/sales/moving-average.html`。窗口大于样本时用户看到「有预测、无历史」，容易误判为页面未计算或数据丢失。
- 方案：`n > data.length` 时提示「窗口 N 不能大于历史期数（当前 5 期）」并阻止计算，或把 N 自动钳制到 `data.length` 并在标签上注明。

### 留存优化
- `tools/marketing/marketing-cpa-calculator.html`：把「CPA / CPC / CVR」画成同一漏斗的三段（花费 → 点击 → 新客），让 200% 这类异常在图形上直接暴露。
- `tools/marketing/marketing-roas-calculator.html`：增加「毛利率」输入并把「盈亏平衡 ROAS / 当前 ROAS / 目标 ROAS」并列到同一数轴，替代当前用当前毛利率反推的隐式假设。
- `tools/marketing/marketing-cac-calculator.html`：回收期展示后，增加「营销端/销售端回收期」拆分，直接看出该先压缩哪一段费用。
- `tools/marketing/marketing-churn-rate.html`：结果区加一行口径提示（期初口径 vs 期末口径），并允许按月连续录入多期，画流失率趋势而不是单期快照。
- `tools/marketing/marketing-conversion-rate-calculator.html`：把 CVR 的分子分母做成可切换口径（访问→转化、点击→转化），避免「转化数超过访问量」这类跨口径误填。
- `tools/sales/sales-forecast.html`：置信区间同时给出「残差 σ」与「历史 σ」两种宽度并允许切换，让用户看到模型拟合质量对区间的影响。
- `tools/marketing/marketing-discount-rate.html`：三种模式共用一个「原价 + 折后价」双向滑块，拖动时实时显示折扣率/折数/节省，从交互上消除「折后价高于原价」的录入可能。
- `tools/sales/moving-average.html`：结果表增加一行「下期预测」并高亮，同时把 WMA 的权重序列（1/2/3）直接列在表头，预测口径错误可被肉眼核对。

### 续查覆盖
- `tools/marketing/marketing-cpa-calculator.html`
- `tools/marketing/marketing-roas-calculator.html`
- `tools/marketing/marketing-cac-calculator.html`
- `tools/marketing/marketing-churn-rate.html`
- `tools/marketing/marketing-conversion-rate-calculator.html`
- `tools/sales/sales-forecast.html`
- `tools/marketing/marketing-discount-rate.html`
- `tools/sales/moving-average.html`
- 本次仅做源码阅读与 node 内存复算（按页面 `calc()` / `forecast()` 表达式在 node 中重写同名逻辑取输出），未做浏览器、英文态、移动端、门禁或线上验证；`marketing-cac-calculator` 的 36 个月生命周期属产品假设，`sales-forecast` 的季节周期自动钳制行为仅按源码推断，均标注为待验证。

