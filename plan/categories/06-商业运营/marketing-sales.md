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

