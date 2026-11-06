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

## 2026-11-06 静态续审：营销 8 页

> 仅阅读当前源码，未运行页面或浏览器；历史条目是当时的证据，以下说明当前关键代码变化，不代表完整回归通过。

- `marketing-ltv-calculator.html:423-435,491-507`：简单模式除客单价外将空值回退 0，清空频次、生命周期或毛利率仍输出 LTV 和相关指标；生命周期为 0 又显示默认 3 年。旧“回本周期未显示”条目已过时：`:454-469` 现有 CAC 回收期，且简单模式没有 CAC 输入；旧月均价值口径问题仍在。
- `marketing-nps-calculator.html:392-409,470-471,494-505`：零贬损者比值仍用 `d||1`；人数只检验总和大于 0，负数或小数仍能参与计算与保存。
- `marketing-price-elasticity.html:394-421,492-505`：原价等于新价时弹性和历史均记 0，仍给“完全无弹性”和降价建议；策略按弹性绝对值推断收入，未使用实际收入变化，例如价格 100→200、销量 100→0 时实际收入从 10000 降至 0，却称单位弹性且收入不变。
- `marketing-qr-campaign-tracker.html:248-259`：链接直接拼接查询串；落地页带 `#` 时参数落入片段而非查询串。`:260-270` 已改用本地二维码库，旧第三方上传结论不适用于当前源码；生成链接并非实际扫码统计。
- `marketing-roas-calculator.html:458-464,510-511`：毛利率恰为 100% 时 `gm < 100` 将保本 ROAS 判为无平衡点并误称毛利率≤0，实际应为 1x；空毛利率也当作 0。历史以广告费后利润率反推保本的关键代码已变更。
- `marketing-sales-funnel.html:309-319,328-341`：当前已拒绝后级人数大于前级，历史超 100% 条目不再适用于该路径；但允许后续连续为 0，前级为 0 时计算 `0/0`，最终文本替换为破折号而没有解释不可计算。
- `marketing-utm-builder.html:243-256,258-280,301-334`：当前已将参数放到锚点前、替换同名参数，输出用 `textContent`，并提供批量链接；历史锚点错位、直接插 HTML 与“仅单条”结论的关键代码已变。source、medium、campaign 仍为必填。
- `social-media-image-sizes.html:480-493,530-551`：筛选和导出均按平台名匹配，旧“平台名搜索导出不匹配”关键代码已变；尺寸数据的权威性本轮未核验。

## 2026-11-06 字数工具静态续审

- `tools/marketing/xiaohongshu-counter.html:229-247`：清空或将上限填 0 时 `||1000` 静默恢复 1000，状态仍显示“正常”；字符数按 UTF-16 `text.length` 计，单个非 BMP 表情占两个单位。是否符合平台限制需另行核实；旧标题及正文分别统计的缺口关键代码仍在。未运行页面。

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

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 3 页（`tools/marketing/marketing-coupon-discount.html`、`tools/marketing/marketing-free-shipping-threshold.html`、`tools/marketing/marketing-ad-budget-allocator.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### MS-M1 优惠券页折扣率 0 被静默替换为 1，>1/负值无拦截（中，确认）
- 描述：`extra = parseFloat(...) || 1` 把合法的 0 折当空值，用户输入 0 折实际按不打折计算；`extra` 也无 0–1 区间校验，输入 1.5 会得到高于原价的“成交价”、负节省与“15 折”。购买数量用 `parseInt(...) || 1`，0 静默变 1、负数照常参与，负数量会显示负原价与负节省。
- 证据：`tools/marketing/marketing-coupon-discount.html:384-385,393-401,406-407,414`
- 复现：原价 299、券 50、门槛 199、折扣率 0、数量 1 → 实际最终 249.00、省 50.00、8.3 折（期望 0.00、省 299）；折扣率 1.5、券 0 → 448.50、省 -149.50、15.0 折（期望拦截）；数量 -2 → “原价 ¥-598.00 · 省 ¥-598.00”（node 复算）。
- 影响：`tools/marketing/marketing-coupon-discount.html`。0 折活动被算成不打折，1.5 折输入被包装成“15 折优惠”，结果可直接复制进促销方案。
- 方案：区分空值与有效 0，折扣率钳制 `0 ≤ extra ≤ 1`、数量要求为正整数；越界标红停止计算并跳过历史保存。

### MS-M2 优惠券页公式框把券按件抵扣，实现只在整单减一次（中，确认页内矛盾）
- 描述：公式框写 `最终价格 = (原价 × 折扣率 - 优惠券) × 数量`，代码实际为 `原价×数量×折扣率 − 券`，券每单只减一次；多件时两者相差 `券额×(数量−1)`。
- 证据：`tools/marketing/marketing-coupon-discount.html:249`（公式框）、`:393-396`（实现）
- 复现：原价 299、折扣 0.8、券 50、数量 2 → 页面 428.40；按公式框应为 378.40，差 50 元（node 复算）。
- 影响：`tools/marketing/marketing-coupon-discount.html`。多件订单按公式复核必然对不上页面结果，促销报价与对账会各用一套口径。
- 方案：公式框改为 `最终价格 = 原价×数量×折扣率 − 券额`，或在代码中按件重复抵扣并明确券可叠加次数。

### MS-M3 包邮页毛利率无区间校验，>100% 得负“商家成本”仍推荐凑单（中，确认）
- 描述：`margin` 未参与 isNaN 校验，也无 0–100 限制；>100% 时 `needMore×(1−margin/100)` 为负，仍被判“低于运费”并推荐凑单；空值 NaN 会把建议文案写成“商家成本约¥—”。
- 证据：`tools/marketing/marketing-free-shipping-threshold.html:241-242,244-258`
- 复现：购物车 78、门槛 99、运费 10、毛利率 150 → 需凑 21 元、商家成本 -10.50，页面仍建议“凑单”；毛利率留空 → “商家成本约¥—，低于运费¥10”（node 复算）。
- 影响：`tools/marketing/marketing-free-shipping-threshold.html`。毛利率误填或越界时仍给出“凑单更划算”，与负成本自相矛盾。
- 方案：毛利率要求 `0 ≤ margin ≤ 100` 且必须为有限数，越界/空值提示并停止建议输出。

### MS-M4 包邮页公式框“净收益=差额×毛利率−运费”与代码判据不等价（中，确认页内矛盾）
- 描述：公式框以“加购毛利 − 运费”判划算，代码以“凑单货成本（差额×(1−毛利率)）< 运费”判划算；同页深解算例采用后者。两判据在差额小于运费时给出相反结论。
- 证据：`tools/marketing/marketing-free-shipping-threshold.html:149`（公式框）、`:253-258`（代码）、`:191-195`（深解）
- 复现：购物车 88、门槛 98、运费 10、毛利率 45% → 代码成本 5.50<10，建议“凑单”；按公式净收益 4.50−10=-5.50，应判不划算（node 复算）。
- 影响：`tools/marketing/marketing-free-shipping-threshold.html`。按公式框自行复核会得到与页面相反的结论。
- 方案：统一为“凑单货成本 vs 运费”或“加购毛利 vs 运费”其中一种，并让公式框、深解与代码三处一致。

### MS-M5 广告预算页负分配比例产出负预算与负 ROAS（中，确认）
- 描述：仅排除三个比例之和为 0，不校验单值非负/上限；负比例经归一化后得到负预算、负收入，整体 ROAS 为负，页面仍按正常明细展示。
- 证据：`tools/marketing/marketing-ad-budget-allocator.html:250-259,269-271`
- 复现：总预算 100,000、比例 -40/35/25、ROAS 4/2.5/2 → 渠道 1 预算 -200,000、占比 -200.0%、收入 -800,000，整体 ROAS -1.13x（node 复算）。
- 影响：`tools/marketing/marketing-ad-budget-allocator.html`。误填负号即可让预算表出现负投放额与负回报，直接复制进季度预算会反向分配资金。
- 方案：三个比例均要求 `≥0`，总和 >0；越界提示“分配比例不能为负”，并对总和不为 100 时显示“已按比例归一化”的说明。

### MS-M6 广告预算页称“按 ROAS 目标智能分配”，实际只按手填比例拆分（中，确认名不符实）
- 描述：标题、简介、公式框写“根据 ROAS 目标和历史表现，智能分配多渠道广告预算”，但三个渠道比例全部由用户手输，代码只做归一化，没有任何按 ROAS 加权或目标反推逻辑；FAQ 反而要求用户自己“用历史 ROAS 归一化”。
- 证据：`tools/marketing/marketing-ad-budget-allocator.html:145,149,198,254-259`
- 复现：默认比例 40/35/25 保持不变，把 ROAS 从 4/2.5/2 改为 10/1/1，三个渠道预算与占比完全不变（node 复算）。
- 影响：`tools/marketing/marketing-ad-budget-allocator.html`。用户按“智能分配”预期改 ROAS 即可自动调预算，实际必须自己先算好比例，工具退化为百分比乘法器。
- 方案：增加“自动按 ROAS 加权 / 手动比例”开关，自动模式按 `ROAS_i / ΣROAS` 分配并允许锁定渠道；若不做，标题与公式框改为“按手填比例拆分预算”。

- 本轮实读 3 页：`tools/marketing/marketing-coupon-discount.html`、`tools/marketing/marketing-free-shipping-threshold.html`、`tools/marketing/marketing-ad-budget-allocator.html`；新增 6 条（高 0/中 6/低 0）；未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 其余页面；MS-M1 与既有 MS-F1 同属折扣率区间校验族但页面不同，MS-M5/MS-M6 与 MS-J1 同属输入校验/名实不符族但页面不同，编号续本文件 `MS-` 风格改用批 M，无重号。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 3 页（`tools/marketing/marketing-cpm-calculator.html`、`tools/marketing/marketing-markup-margin.html`、`tools/marketing/marketing-sales-funnel.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### MS-N1 加价率→利润率换算公式数量级错误，且利润率输入被完全忽略（高，确认）
- 描述：换算模式把加价率 m 代入 `marginRate = m/(1+m/100)*100`，正确应为 `m/(100+m)*100`，默认 50% 加价率被算成 3333.33% 利润率。同时 `convMargin`（g）读入后只做 isNaN 校验，从未进入任何结果；用户按利润率反算时输入被静默丢弃，预设还会把 convMargin=33.33 回填，进一步掩盖问题。
- 证据：`tools/marketing/marketing-markup-margin.html:443-453`（读取与公式，`:450` 为错误表达式）、`:235-240`（convMarkup/convMargin 输入）、`:581`（预设回填 convMargin）
- 复现：换算模式 m=50、g=33.33 → 实际利润率 3333.33%、售价 150.00、利润 50.00（期望利润率 33.33%）；m=0、g=50 → 实际利润率 0.00%、售价 100.00（期望按 50% 利润率反算加价率 100%、售价 200.00）（node 复算）。
- 影响：`tools/marketing/marketing-markup-margin.html`。定价页核心换算错两个数量级，“双向换算”实际单向；用户照结果定价会得到荒谬利润率。
- 方案：利润率改为 `m/(100+m)*100`；实现真正双向——输入 g 时 `m = g/(100-g)*100`（要求 `0 ≤ g < 100`），并在换算模式标明以哪个输入为准。

### MS-N2 加价/利润率换算页无区间校验，负值可得 -10000% 利润率（中，确认）
- 描述：两个换算输入只判 NaN，没有 `m ≥ 0`、`0 ≤ g < 100` 约束；负加价率进入换算公式会得到 -10000% 利润率，m=-100 时除零；负利润率同样放行但不参与计算。
- 证据：`tools/marketing/marketing-markup-margin.html:235-240`（仅前端 min/max）、`:443-453`（无区间校验）、`:450`（除零风险）
- 复现：换算模式 m=-50、g=33.33 → 利润率 -10000.00%、售价 50.00、利润 -50.00；m=-100 → 利润率 Infinity（结果区显示“—”）；g=-50 通过校验但结果完全不使用 g（node 复算）。
- 影响：`tools/marketing/marketing-markup-margin.html`。误带负号即可产出极端利润率或“—”，页面无任何错误提示，结果可被复制进报价单。
- 方案：要求 `m ≥ 0`、`0 ≤ g < 100` 且为有限数；越界字段标红并停止渲染结果。

### MS-N3 CPM 页点击量可超展示量，CTR 500% 无拦截（中，确认）
- 描述：`hasClicks` 只判断 `clicks > 0`，没有 `clicks ≤ impressions` 上界；点击量大于展示量时 CTR>100%、每点击展示数 <1 仍正常展示。负点击被同一判断静默忽略，联动指标整块隐藏且无输入错误提示。
- 证据：`tools/marketing/marketing-cpm-calculator.html:204`（点击输入）、`:395,404-406`（读取与 CTR）、`:439,447`（结果展示）
- 复现：花费 2000、展示 1000、点击 5000 → CTR 500.00%、CPC ¥0.40、每点击展示数 0（期望拦截“点击量不能大于展示量”）；点击 -100 → 联动卡消失且无提示（node 复算）。
- 影响：`tools/marketing/marketing-cpm-calculator.html`。异常埋点或手误即可产出“500% 点击率”并当作投放结论；负值则被静默吞掉。
- 方案：要求 `0 ≤ clicks ≤ impressions`，越界提示并停止计算；负值标红而非静默隐藏。

### MS-N4 销售漏斗页成交客户数可超商机数，末级转化 6000%（中，确认）
- 描述：5 个输入只做“非空 + visitors>0”守卫，未校验各阶段人数单调不增；成交客户大于商机时末级转化率 >100%，整体转化率也可 >100%；负值同样放行。
- 证据：`tools/marketing/marketing-sales-funnel.html:156`（成交输入）、`:293`（守卫）、`:314`（阶段转化）、`:322-323`（整体转化）
- 复现：访客 100、线索 10、合格 5、商机 2、成交 120 → 成交阶段转化率 6000.0%、整体转化率 120.000%（期望“成交数不能大于商机数”）；成交 -50 → 整体 -50.000%（node 复算）。
- 影响：`tools/marketing/marketing-sales-funnel.html`。漏斗条被 `Math.min(pct,100)` 截断，文字仍显示 6000%，图形与数字自相矛盾，瓶颈判断失真。
- 方案：校验 `visitors ≥ leads ≥ qualified ≥ opportunities ≥ customers ≥ 0`，越界停止并指出首个倒挂环节。

### MS-N5 销售漏斗页引据表整体转化率口径（成交/线索）与公式框/代码（成交/访客）矛盾（低，确认）
- 描述：引据表“整体转化率”写 `成交数/线索数 ×100%`，公式框与代码均为 `成交数/访客数`；同页两套口径，按引据表复核会得到不同数值。
- 证据：`tools/marketing/marketing-sales-funnel.html:149`（公式框）、`:216`（引据表）、`:322`（代码）
- 复现：访客 100000、线索 5000、成交 200 → 页面整体转化率 0.200%；按引据表口径 4.0%，相差 20 倍（node 复算）。
- 影响：`tools/marketing/marketing-sales-funnel.html`。用户按引据表复核对不上页面结果，KPI 汇报口径不一致。
- 方案：引据表改为 `成交数/访客数`，与公式框、代码统一。

- 本轮实读 3 页：`tools/marketing/marketing-cpm-calculator.html`、`tools/marketing/marketing-markup-margin.html`、`tools/marketing/marketing-sales-funnel.html`；新增 5 条（高 1/中 3/低 1）；未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 其余页面；与批 M 的 coupon/free-shipping/ad-budget 三页无重复，MS-N1 为换算公式错误族、MS-N3/N4 为输入上界校验族，均无重号。

## 2026-11-04 续查（并行批 O）

> 范围：本轮阅读 3 页（`tools/marketing/marketing-cpc-calculator.html`、`tools/marketing/marketing-roi.html`、`tools/marketing/utm-builder.html`）。仅源码 + `node -e` 内存复算，未开浏览器/未做 EN/移动端/门禁验证。

### MS-N6 投资 ROI 页“最终价值”被年化回写覆盖，字段无法编辑（高，确认）
- 问题：`calcInvestment()` 用“年化收益率输入框是否有值”当模式开关。首次计算走 else 分支，把算出的年化写回 `i_annual`（`:505`）；此后任何对“最终价值”的输入都会命中 `annualRate` 分支，用旧年化反算 `finalValue` 并回写“最终价值”输入框（`:500`）。该字段因此变成只读/自回归，且每次回写带浮点漂移。
- 证据：`tools/marketing/marketing-roi.html:243`（最终价值 `oninput="calcInvestment()"`）、`:247`（年化输入）、`:493-506`（模式判断与回写）、`:500`（覆盖用户输入）
- 复现：默认 本金 100000 / 最终价值 135000 / 期限 3 年 → 首次年化 10.52%；把“最终价值”改为 200000 → 输入被立即回写为 134,996.54，总 ROI 仍 35.00%（期望最终价值 200000、ROI 100.00%）；改期限为 5 年则最终价值被改成 164,893.82（node 复算）。
- 影响：`tools/marketing/marketing-roi.html`。投资回报页的核心输入不可用，用户无法按“已知终值求年化”，只能先清空年化框，交互无任何提示。
- 方案：改为显式模式（按最终价值 / 按年化收益率二选一），或给年化框加“用户已手动编辑”标记（dirty flag），仅该标记为真时走年化分支；回写前不要覆盖当前正在编辑的字段。

### MS-N7 广告 ROI 的“广告收入”填 0 被静默替换为 转化量×客单价（中，确认）
- 问题：`const finalRevenue = revenue || calcRevenue`，`revenue` 为 0（真实的“零收入”测试）时被 `||` 当成空值，回退到 `conversions * price`；结果卡“收入”、ROI、利润、ROAS 全部按回退值展示，页面无提示。
- 证据：`tools/marketing/marketing-roi.html:444`（读取）、`:450-451`（回退）、`:464-467`（展示）、`:459`（ROAS）
- 复现：广告投入 50000、广告收入 0、转化量 500、客单价 199 → 实际收入 99,500、利润 49,500、ROI 99.0%、ROAS 1.99（期望收入 0、利润 -50,000、ROI -100.0%）（node 复算）。
- 影响：`tools/marketing/marketing-roi.html`。投放全线亏损的场景会被算成盈利，ROI 结论方向相反。
- 方案：改为 `isNaN(revenue) ? calcRevenue : revenue`（只在空值/非数时回退），0 视为有效收入；若确实要用“转化×客单价”兜底，需在结果旁标注“收入按转化量×客单价估算”。

### MS-N8 营销 ROI 页比例与数值无区间校验，点击可超曝光、负值照算（中，确认）
- 问题：`m_*` 六个输入均无 `min`，读取用 `parseFloat(...)||0`，末尾只拦 `Infinity/NaN`；没有 `0≤ctr,cvr,repeat≤100` 与“点击 ≤ 曝光”约束。`ctr>100` 时点击量大于曝光、漏斗条宽度可 150%；负比例得到负点击/负收入/负 ROI。
- 证据：`tools/marketing/marketing-roi.html:212-221`（输入无 min）、`:392-398`（计算）、`:419,439`（仅 Infinity/NaN 守卫）、`:434`（漏斗宽度不钳制）
- 复现：曝光 100000、点击率 150、转化率 3、复购率 20 → 点击 150,000（大于曝光）、漏斗“点击”行宽 150%、行内转化率 150.0%；点击率 -5 → 点击 -5,000、转化 -150、收入 -53,820、ROI -638.2%（node 复算）。
- 影响：`tools/marketing/marketing-roi.html`。异常 CTR/CVR 或误带负号会产出与事实相反的 ROI，并可直接保存进历史记录。
- 方案：要求 `0 ≤ ctr,cvr,repeat ≤ 100`，曝光/投入/客单价 `≥ 0`；越界字段标红并停止渲染结果。

### MS-N9 CPC 页点击量可大于展示量，CTR 500% 无拦截（中，确认）
- 问题：`hasImpressions` 只判 `impressions > 0`，未校验 `clicks ≤ impressions`；点击量高于展示量时 CTR>100%、每千次展示成本异常放大，页面仍按正常指标卡展示。
- 证据：`tools/marketing/marketing-cpc-calculator.html:199`（点击输入）、`:401-403`（CTR/CPM 计算）、`:434-442`（展示）
- 复现：花费 3000、点击 5000、展示 1000 → CPC ¥0.60、CTR 500.00%、CPM ¥3,000.00（期望提示“点击量不能大于展示量”）（node 复算）。
- 影响：`tools/marketing/marketing-cpc-calculator.html`。异常埋点或手误即可得到“500% 点击率”，与既有 MS-N3（CPM 页）同族但页面不同。
- 方案：要求 `0 ≤ clicks ≤ impressions`（有展示量时），越界提示并停止计算；负展示量标红而非静默隐藏联动卡。

### MS-N10 CPC 页“行业基准对比”是按固定 ¥5 折算，口径无说明（低，确认）
- 问题：指标卡显示 `((cpc / 5) * 100).toFixed(0) + '%'`，恒定以 ¥5 为基准；页面说明、参考表、FAQ 均未提这个 ¥5 来自哪里（参考表电商区间是 ¥1.5–5、金融 ¥5–20），用户会误读成“优于行业 X%”。
- 证据：`tools/marketing/marketing-cpc-calculator.html:448-451`（指标）、`:259-266`（行业区间表）
- 复现：CPC ¥2.50 → 显示“行业基准对比 50%”；CPC ¥0.50 → 10%；CPC ¥10 → 200%（node 复算）。
- 影响：`tools/marketing/marketing-cpc-calculator.html`。同一数字在不同行业语义完全不同，易被当成行业对标结论。
- 方案：改为“相对 ¥5 基准水平”（并注明基准值），或按所选行业的区间中值计算；否则删除该指标。

### MS-N11 UTM 基础 URL 含 `#` 片段时，追踪参数被拼进 fragment（高，确认）
- 问题：追加参数只用 `url.includes('?') ? '&' : '?'` 判断，未处理 `#`。URL 带锚点时 `utm_*` 被拼到 `#` 之后，成为 fragment 的一部分；fragment 不会发送给服务器，渠道归因全部失效，但复制出来的链接外观正常。
- 证据：`tools/marketing/utm-builder.html:446-447`（单个生成）、`:512-513`（批量）、`:533-534`（复制全部）、`:548-549`（CSV）
- 复现：`https://shop.com/p#sku` → `https://shop.com/p#sku?utm_source=baidu`；`https://shop.com/p?x=1#sku` → `https://shop.com/p?x=1#sku&utm_source=baidu`（node 字符串复算），两种形态参数都在 `#` 之后（期望 `https://shop.com/p?utm_source=baidu#sku`）。
- 影响：`tools/marketing/utm-builder.html`。带锚点的落地页（商品 SKU、章节导航、单页应用路由很常见）投放后全部归因为 direct/none，而工具四条出口（单个/批量/复制/CSV）一致出错，用户极难自查。
- 方案：先按 `#` 切分 `base` 与 `fragment`，只在 `base` 上按 `?`/`&` 追加参数，最后再拼回 `#fragment`；对含多个 `#` 的异常 URL 给出提示。

### MS-N12 UTM 历史记录回填调用 `switchTab()` 无参，工具区变成空白（中，确认）
- 问题：TBKit 历史面板的回填回调末尾调用 `switchTab();`（无参数）。`switchTab` 先把所有 `.tab-content` 的 `active` 移除，再执行 `document.getElementById('tab-' + undefined)` → null → `.classList.add()` 抛 TypeError；异常被外层 `try/catch` 吞掉，页面停在“所有面板都不显示”的状态。
- 证据：`tools/marketing/utm-builder.html:679`（无参调用）、`:407-412`（先清空再取 `tab-undefined`）、`:668-682`（回调 try/catch 吞异常）
- 复现：生成任意链接并触发一次历史记录后，在历史面板点该记录 → 四个 tab 全部取消高亮、工具卡内容区空白（期望回到“单个生成”并回填参数）；控制台可见 `Cannot read properties of null` 被吞。
- 影响：`tools/marketing/utm-builder.html`。历史回填是留存主路径，点击后页面像“坏了”，用户只能刷新。
- 方案：改为 `switchTab('single')`，并给 `switchTab` 加 `if(!tab) return;` 与 `getElementById` 空值保护。

### MS-N13 批量导出 CSV 未做字段转义，含逗号即错列（低，确认）
- 问题：CSV 用模板字符串直接拼 `${item.source},${item.medium},${item.campaign},${url}`，没有引号包裹与 `"` 转义。`utm_*` 值经 `URLSearchParams` 编码（逗号变 `%2C`）是安全的，但第 4 列的 baseUrl 原样插入，域名/路径/查询里含逗号时列数错位。
- 证据：`tools/marketing/utm-builder.html:542`（表头）、`:548-550`（拼行，baseUrl 原样）
- 复现：baseUrl=`https://x.com/p?a=1,2`、source=`baidu` → 输出 `baidu,feed,campaign,https://x.com/p?a=1,2&utm_source=baidu`，该行被解析成 5 列（期望 4 列，含逗号的 URL 在引号内）（node 字符串复算）。
- 影响：`tools/marketing/utm-builder.html`。导出的渠道表在 Excel/表格工具中列错位，批量投放排期直接错行。
- 方案：所有字段统一 `"` 包裹并把内部 `"` 替换为 `""`；或以 `\t` 分隔导出 TSV。

#### 留存/优势建议（营销 3 页）
- CPC 页：① 把当前结果卡（花费/点击/展示/CPC/CTR/CPM）做成“导出本次结果”，现在导出按钮导的是历史表；② 参考表选行业后自动切换 CPC 分级阈值（当前写死 ¥1/3/8，与电商 ¥1.5–5 的口径不符）；③ 历史记录支持勾选 2–3 条做并排对比。
- ROI 页：① 营销/广告/投资三个计算器合并成“渠道对比”视图，同一预算下并列 ROI/ROAS；② 广告页增加“目标 ROI 反推可承受 CPA/CPC”；③ 权重/参数方案命名保存到 localStorage 并支持一键套用。
- UTM 页：① 批量表补 `utm_term`/`utm_content` 两列，与单个生成对齐；② 生成前校验协议/域名、检测重复 `utm_*` 与 `#` 片段；③ 历史按“批量组”聚合，支持一键复制整组并标注渠道。

- 本轮实读 3 页：`tools/marketing/marketing-cpc-calculator.html`、`tools/marketing/marketing-roi.html`、`tools/marketing/utm-builder.html`；新增 8 条（高 2/中 4/低 2）；未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N9 与既有 MS-N3 同属“点击超展示”族但页面不同，MS-N6/MS-N11 为本批新族（输入回写自覆盖 / URL fragment 拼接），MS-N7 为 `||` 零值吞没族，均无重号。

## 2026-11-04 续查（并行批 P）

> 范围：本轮阅读 3 页（`tools/marketing/marketing-ctr-calculator.html`、`tools/marketing/marketing-ltv-calculator.html`、`tools/marketing/marketing-google-ads-budget.html`）。仅源码 + `node -e` 内存复算，未开浏览器/未做 EN/移动端/门禁验证。

### MS-N14 CTR 页点击量可超展示量、转化数可超点击量，CTR 500%/CVR 250% 无拦截（高，确认）
- 问题：`calc()` 只校验展示量非 NaN 且 `imp>0`，对点击量与转化数既无非负校验，也没有“点击 ≤ 展示”“转化 ≤ 点击”的单调约束；`ctr=(clk/imp)*100`、`cvr=(conv/clk)*100` 直接输出，等级判定还把 500% 判成“优秀”。
- 证据：`tools/marketing/marketing-ctr-calculator.html:385`（唯一守卫）、`:390`（CTR）、`:393`（CVR）、`:397`（`ctr>=5` 判“优秀”）、`:436`（展示 `clk/imp`）
- 复现：展示 1000、点击 5000、花费 500、转化 10 → CTR 500.00%、等级“优秀”、CPC ¥0.10、CPM ¥500.00；点击 200、转化 500 → CVR 250.00%（期望提示“点击不能大于展示”“转化不能大于点击”并停止渲染）（node 复算）。
- 影响：`tools/marketing/marketing-ctr-calculator.html`。埋点异常或手误即得“500% 点击率/250% 转化率”，页面却按“优秀”正反馈，指标卡与等级结论都会误导投放复盘。
- 方案：加 `0 ≤ clk ≤ imp`、`0 ≤ conv ≤ clk`（有展示/点击时），越界字段标红并停止计算；等级判定前先确认 CTR 落在 0–100 区间。

### MS-N15 CTR 页负数点击照算，负 CTR 判“偏低”且 CPC 被静默归零（中，确认）
- 问题：输入框写了 `min="0"`，但 `min` 只参与表单校验，不阻止键入，`calc()` 也不读；点击为负时 `ctr` 为负、`level` 落到 `else` 分支显示“偏低”，而 `cpc` 因 `clk>0` 为假被置 0，真实值应为 `cost/clk`（负），两处口径同时失真。
- 证据：`:194-211`（四个 `min="0"` 输入）、`:379-400`（读取/计算/等级，无 `<0` 判断）、`:392`（`clk>0` 才给 CPC）
- 复现：展示 10000、点击 -200、花费 500 → CTR -2.00%、等级“偏低”、CPC 显示 ¥0.00（真实 -¥2.50）、CPM ¥50.00，结果卡仍写“-200次点击 / 10000次展示”（期望拦截负数）（node 复算）。
- 影响：`tools/marketing/marketing-ctr-calculator.html`。负号粘贴或键盘误触会得到负数指标，且 CPC 归零让人误判“没有点击成本”，容易把异常数据当成有效结论。
- 方案：读取后统一 `if (clk < 0 || conv < 0 || cost < 0) 报错`；`cpc` 改用 `cost>0 && clk!==0`，并在结果卡保留负值以暴露异常，不要静默归零。

### MS-N16 LTV 页“月均/周均/日均价值”按 ltv/12、/52、/365 均摊，无视客户生命周期（中，确认）
- 问题：三张相关指标卡固定用 `ltv/12`、`ltv/52`、`ltv/365`，把“整个生命周期的总毛利”按 1 年摊平；simple 模式的 `ltv` 已乘 `lifespan`（年），detail 模式的 `ltv` 已乘 `lifespanMonths`，生命周期均未进入除法。
- 证据：`:433-434`（simple 的 ltv 含 lifespan）、`:449-450`（detail 的 ltv 含 lifespanMonths）、`:489`/`:493`/`:497`（三个除法）、`:490`/`:494`/`:498`（“月均/周均/日均价值”标签）
- 复现：simple 默认 客单价 200、频次 4、生命周期 3 年、毛利率 30% → LTV ¥720，页面“月均价值 ¥60”，按生命周期摊平应为 720/(3×12)=¥20/月，高估 3 倍；detail 默认（月收入 99、流失 5%、毛利 70%）→ LTV ¥1,386，页面 ¥116/月，实际月毛利 99×0.7=¥69.3（node 复算）。
- 影响：`tools/marketing/marketing-ltv-calculator.html`。同一客户换成生命周期 1 年或 5 年，“月均价值”纹丝不动，用它做月度预算或 CAC 上限会系统性高估 1.7–3 倍。
- 方案：改为 `ltv/(lifespanYears*12)`、`ltv/(lifespanYears*52)`、`ltv/(lifespanYears*365)`（detail 模式用 `ltv/lifespanMonths`、`ltv/(lifespanMonths*30/7)`、`ltv/(lifespanMonths*30)`）；若坚持按 1 年摊平，则把标签改为“年均价值的 1/12”并注明口径。

### MS-N17 LTV 页回本周期写死 3 年且从未展示（中，确认）
- 问题：`payback = cac / (ltv / (inputs.lifespanYears || 3) / 12)`。simple 模式的 `inputs` 只有 `lifespan`（年），没有 `lifespanYears`，`||3` 恒取 3；更关键的是 `payback` 之后从未进入 `extra`（结果区只有 LTV:CAC 一张卡），整段计算悬空，全文仅此一处出现。
- 证据：`:435`（simple inputs 无 lifespanYears）、`:451`（detail 才有）、`:457`（写死 3）、`:458-464`（`extra` 只渲染 ratio）、`:456`（ratio）
- 复现：simple 客单价 200、频次 4、生命周期 1 年、毛利 30%、CAC 300 → LTV ¥240，页面无任何回本周期；按写死的 3 年折算得 45 个月，按真实 1 年应为 15 个月（3 倍偏差）（node 复算）。
- 影响：`tools/marketing/marketing-ltv-calculator.html`。回本周期是判断“是否加投”的核心指标，现在既算错（simple 模式）又看不到；后续若直接启用该变量，会按错误口径上线。
- 方案：删除 `payback` 或在结果区新增“回本周期 N 个月”卡，并按 `ltv/lifespan` 的年均毛利计算：`cac / (ltv/lifespanYears/12)`；simple 模式不要用 `||3` 兜底。

### MS-N18 LTV 页频次/生命周期/毛利率无上下界，负值或 >100% 照算（中，确认）
- 问题：simple 只拦 `arv<=0`，`freq`、`lifespan` 可为负；`margin` 输入写 `max="100"` 但 JS 不校验，200% 照算。detail 只拦 `mrr<=0||churn<=0`，`churn=100` 时生命周期压到 1 个月、`margin=150` 时 LTV 超毛收入 1.5 倍。
- 证据：`:220`/`:233`/`:239`（`max="100"`）、`:428`（仅 arv）、`:442`（仅 mrr/churn）、`:433-434`/`:447-450`（直接相乘）
- 复现：客单价 200、频次 -4、生命周期 3、毛利 30% → LTV ¥-720、LTV:CAC ¥-2.40:1 仍判“危险”；毛利率 150% → LTV ¥1,080 > 毛收入 ¥720；detail 毛利率 150%、流失 5% → LTV ¥2,079（>毛收入 ¥1,386）（node 复算）。
- 影响：`tools/marketing/marketing-ltv-calculator.html`。负数与超 100% 毛利率会给出负 LTV 或“LTV 大于客户毛收入”的物理不可能值，但页面照常给健康度结论。
- 方案：`freq>0 && lifespan>0 && 0≤margin≤100`，detail 追加 `0<churn≤100`；越界标红并停止渲染。

### MS-N19 Google Ads 预算页只有 CPC>0 校验，负点击出负预算却配正 ROAS，转化率 150% 照算（高，确认）
- 问题：`if(...||cpc<=0)` 是唯一约束，`targetClicksDay`、`convRate`、`avgOrderValue` 均无 min/max 属性也无 JS 校验，更没有 `0≤cr≤100`。日预算、转化数、收入、ROAS 全部由原始值直乘，末尾只替换 `Infinity/NaN`，负数不处理。
- 证据：`tools/marketing/marketing-google-ads-budget.html:152-155`（四个输入无约束）、`:244`（唯一守卫）、`:248-253`（预算/转化/收入/ROAS 直算）
- 复现：CPC ¥3、目标日点击 -50、转化率 3%、客单价 ¥300 → 日预算 ¥-150、月预算 ¥-4,500、日转化 -1.5、日收入 ¥-450，ROAS 仍显示 **3.00x**（负÷负得正）；改点击 50、转化率 150 → 日转化 75（大于 50 次点击）、ROAS 150.00x（期望拦截“转化率 0–100、点击为非负”）（node 复算）。
- 影响：`tools/marketing/marketing-google-ads-budget.html`。负数预算与 150x ROAS 会直接出现在“日预算/月预算/ROAS”四张主卡上，误填一个负号就让亏损方案看起来“预算为负、回报 3 倍”，比直接报错更危险。
- 方案：四输入统一非负，且 `0≤convRate≤100`；`cpc>0`、`targetClicksDay>0`、`avgOrderValue>0` 才算有效；越界标红并停止渲染，不要只依赖 HTML `min`。

### MS-N20 Ads 页标题/公式承诺“目标转化量、转化成本/CPA”，实际无对应输入与输出；结果卡“日订单数”实为转化数（中，确认）
- 问题：meta/og/twitter 写“输入目标转化量、预期CPC或转化成本”，实际四个输入是 CPC/目标日点击/转化率/客单价；`formula-eq` 写“CPA = 花费 ÷ 转化数”，代码从未计算 CPA，结果区也没有 CPA 卡。`dailyConv` 本质是转化数（可为小数），标签却叫“日订单数”。
- 证据：`:10`（meta）、`:149`（公式含 CPA）、`:152-155`（实际输入）、`:248-259`（只输出预算/转化/收入/ROAS）、`:258`（“日订单数”）
- 复现：默认参数（CPC 3、点击 50、转化率 3%、客单价 300）→ 页面“日订单数 1.5”，且全页找不到 CPA（期望 CPA=150/1.5=¥100，或按“目标转化量 ÷ 转化率”反推所需点击）（源码检查）。
- 影响：`tools/marketing/marketing-google-ads-budget.html`。按 meta 找“目标转化量/CPA”的用户拿不到结果；“1.5 个订单”这种小数在订单口径下也不成立，复制进投放计划会口径混乱。
- 方案：二选一——补“目标转化量”输入并反推预算/点击、同时输出 CPA 卡；或把 meta/og/twitter 与公式框收窄为“按 CPC×点击估预算与 ROAS”，删掉 CPA 句，标签改“日转化数”。

### MS-N21 LTV 详情模式“预期生命周期”重复展示两次（低，确认）
- 问题：detail 模式结果里，“详细拆解”表格有一行“预期生命周期 N 个月”（`:481`），下方“相关指标”卡又给一张同值卡（`:500-502`），同一数字在结果区出现两遍；simple 模式只有后者。
- 证据：`:481`（条件行）、`:500-502`（相关指标卡）
- 复现：切到详情模式、默认参数 → 两处都显示“20 个月”（源码检查）。
- 影响：`tools/marketing/marketing-ltv-calculator.html`。结果区冗余，弱化真正新增的指标（月均/周均/日均）。
- 方案：detail 模式删掉相关指标里的“预期生命周期”，或把它换成“预计留存月数对应的年数”。

#### 留存/优势建议（营销 3 页）
- CTR 页：① 增加“点击 ≤ 展示、转化 ≤ 点击”的校验与占比条（与 MS-N14 同批修）；② 结果卡支持“按渠道/素材保存基准 CTR”并做环比；③ 补“目标 CTR 反推所需展示量/点击量”的反算视图。
- LTV 页：① simple 与 detail 两种口径并排展示同一客户，避免用户切模式后无法对照；② 加 CAC 敏感性（CAC ±20% 时 LTV:CAC 与回本周期变化）；③ 支持按新客/复购分群保存多组 LTV 并导出。
- Ads 页：① 补“按目标转化量反推预算/点击”模式（兑现 meta）；② 输出 CPA 与盈亏平衡 ROAS（客单价×毛利率），并标“ROAS 低于该值即亏损”；③ 预设改为“行业 CPC × 转化率”组合并持久化到 localStorage。

- 本轮实读 3 页：`tools/marketing/marketing-ctr-calculator.html`、`tools/marketing/marketing-ltv-calculator.html`、`tools/marketing/marketing-google-ads-budget.html`；新增 8 条（高 2/中 5/低 1）；未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N14 与既有 MS-N3（CPM 页）/MS-N9（CPC 页）同属“点击超展示”族但页面不同，MS-N16/MS-N17 与 MS-J3（CAC 页 36 个月回本假设）同属“生命周期写死”族但页面不同，MS-N19 为“全字段无界”新族，MS-N19/MS-N20 与 MS-M5/MS-M6（`marketing-ad-budget-allocator.html`）页面不同，均无重号。

## 2026-11-04 续查（并行批 Q）

### MS-N22 广告 ROI 页同屏存在三种 ROI 口径，默认参数下最高与最低相差约 5.8 倍（高，确认）
- 问题：公式说明、引据表和代码各用一种 ROI 定义：说明写“ROI=毛利÷预算”，引据表写“ROI=(毛利−广告花费)/广告花费”，代码写“利润÷总成本”。三者分母与是否扣除货品/固定成本完全不同，但页面未标注适用口径。
- 证据：`tools/marketing/ad-roi.html:140`（`毛利=收入×(1−成本率)−固定成本，ROI=毛利÷预算`）、`:210`（引据表 `ROI = (广告带来的毛利 − 广告花费)/广告花费`）、`:300-303`（`totalCost=预算+货品成本+固定成本`、`roi=profit/totalCost*100`）、`:192-193`（引用表又写 ROI=(收入−总成本)/总成本）
- 复现：默认 预算 10000、CPC 2、CTR 3%、CVR 5%、客单价 200、成本率 50%、固定成本 0 → 收入 50000、货品成本 25000、总成本 35000、利润 15000，页面 ROI `42.9%`；按 `:140` 口径 毛利 25000÷预算 10000 = `250.0%`；按 `:210` 口径 (25000−10000)÷10000 = `150.0%`（node 复算）。同一组输入可读出三个结论。
- 影响：`tools/marketing/ad-roi.html`。用户按任一口径手算都无法与页面结果对上，投放复盘与预算审批会被错误口径误导；深度解析 `:245-246` 的算例反而只与代码口径一致。
- 方案：全页统一为“利润÷总成本（含货品与固定成本）”，并在公式框、引据表、深度解析同步改写；如需保留行业常用的“广告毛利÷花费”，另立一行“广告端 ROI（不含固定成本）”并明确标注，禁止两个都叫 ROI。

### MS-N23 盈亏平衡判定忽略固定成本，成本率 100% 时亏损仍标“✓ 盈利”（高，确认）
- 问题：`breakEvenRoas=1/毛利率` 只反映货品成本，不含固定成本；判定 `roasOk = roas >= breakEvenRoas` 完全不看 `profit`。成本率恰为 100% 时 `grossMargin=0`，`breakEvenRoas` 被置 0，任何非负 ROAS 都判盈利。
- 证据：`tools/marketing/ad-roi.html:305`（`breakEvenRoas = grossMargin>0?1/grossMargin:0`）、`:321-325`（仅用 ROAS 比较并输出“✓ 盈利/✗ 亏损”）、`:250`（FAQ“ROAS≥1.67 就不亏”同样未提固定成本）、`:300-301`（固定成本已进入 `totalCost`）
- 复现：默认参数 + 固定成本 20000 → 利润 `-5000`、ROI `-9.1%`，页面仍显示“✓ 盈利”（ROAS 5 ≥ 2）；成本率 100 → 利润 `-10000`、ROI `-16.7%`、盈亏平衡 ROAS 显示 `0.00`，仍“✓ 盈利”（node 复算）。
- 影响：`tools/marketing/ad-roi.html` 盈亏平衡卡与亏损挽回提示。固定成本较高或毛利率极低时，页面把亏损方案判成盈利，直接反向指导加预算。
- 方案：保本 ROAS 改为 `(预算+固定成本)/(预算×(1−成本率))`；毛利率 ≤0 时直接输出“无法通过销售覆盖成本”，不再给数值阈值；`roasOk` 改为 `profit>0` 或与利润符号联合判定。

### MS-N24 亏损挽回阈值漏掉成本率与固定成本，建议值被低估约 10 倍（高，确认）
- 问题：`neededCvr` 用 `(预算/客单价)/点击量`，`aovNeeded` 用 `预算/(点击量×转化率)`，都等价于“让收入等于预算”，没有考虑货品成本与固定成本；而实际保本要求 `收入×(1−成本率)=预算+固定成本`。
- 证据：`tools/marketing/ad-roi.html:329-332`（仅在 `!roasOk` 时计算）、`:330`（`neededCvr=(budget/aov)/clicks`）、`:331`（`aovNeeded=budget/(clicks*cvr)`）、`:246`（深解同一错误公式：点击 5000/客单价 300/预算 10000 → “0.67% 才保本”，未扣毛利率）
- 复现：成本率 90%、预算 10000、CPC 2 → 点击 5000、CVR 5%、客单价 200。页面建议“转化率提升至 `1.00%`、客单价提升至 `40 元`”；实际保本需收入 `100000`（=10000/(1−0.9)）→ CVR `10%`、客单价 `400 元`（node 复算），建议值低估 10 倍。深解 `:246` 的算例同样错：毛利率 40%、点击 5000、客单价 300、预算 10000 → 页面给 `0.67%`，实际需 `1.11%`（收入需 10000/0.6=16667，转化 55.6 单）。
- 影响：`tools/marketing/ad-roi.html` 亏损挽回提示。用户照 1% 转化率目标优化仍会持续亏损，且会误判“只差一点”。
- 方案：先算 `neededRevenue=(预算+固定成本)/(1−成本率)`，再反推 `neededCvr=neededRevenue/(点击×客单价)` 与 `neededAov=neededRevenue/转化数`；`成本率≥100%` 时不渲染该建议，改为“当前单位经济模型无法保本”。

### MS-N25 CPC 模式下 CTR 不影响 ROI，与“调整 CTR 即可比较方案”矛盾（中，确认）
- 问题：CPC 分支点击量只由预算/CPC 决定，CTR 仅用于反推展示量；收入、利润、ROI、ROAS 全都不含 CTR。但公式说明写“调整出价 / CTR / CVR 即可比较不同投放方案盈亏”。
- 证据：`tools/marketing/ad-roi.html:140`（文案）、`:286-290`（`clicks=budget/cpc`，`impressions=clicks/ctr`）、`:297-303`（收入起算于 `clicks*cvr`，未用 `impressions`）
- 复现：CPC 模式下 CTR 1% 与 5% → ROI 均为 `42.9%`，仅展示量从 `500000` 变为 `100000`（node 复算）；用户以为在比较两种素材，实际 ROI 纹丝不动。
- 影响：`tools/marketing/ad-roi.html` CPC 模式。按文案调 CTR 做 A/B 对比时看不到任何 ROI 变化，容易被误判为“素材无效”。
- 方案：文案改为“CPC 模式 CTR 仅影响展示量，不改变 ROI；如需按 CTR 联动，请切 CPM 模式”，或在 CPC 模式隐藏 CTR 输入并明确提示。

### MS-N26 邮件标题评分与页面自带“低分标题”示例矛盾（历史结论；部分代码已变化，待重新核算）

> 2026-11-06 静态复核：感叹号已匹配中英文（`tools/marketing/email-subject-line-tester.html:560-564`），且预览正文现参与垃圾词得分（`:537-554`），旧 85 分复算不再适用；示例一致性需用当前默认正文重新核验。
- 问题：深度解析把「【限时】点击领取你的专属优惠券！！！」当作“过长、3 个感叹号、含「领取/免费」类触发词”的低分案例，但该串实际长度 18（未过长）、用的是全角“！”（不触发扣分）、词表里没有“领取”且标题根本没有“免费”，评分器给它 85 分，落在“优秀 👍”档（≥80）。深层原因是全角感叹号不触发扣分、垃圾词扣分被正面词加分抵消。
- 证据：`tools/marketing/email-subject-line-tester.html:314`（深解“低分标题”）、`:535-545`（垃圾词累加）、`:557-560`（仅匹配 ASCII `!` 且数量 >2 才扣 5）、`:581-587`（正面词 +3）、`:592-595`（≥80 判“优秀”）
- 复现：`【限时】点击领取你的专属优惠券！！！` → 字符 18（不扣）、方括号 −2、垃圾词 限时 −3/点击 −8/优惠 −5、全角“！”不触发 −5、正面词“优惠”使 `posPct=80` 再加 +3 → 总分 `85`，输出“优秀 👍”（node 复算）。页面自己的反例被判为优秀。
- 影响：`tools/marketing/email-subject-line-tester.html` 评分主结论与深解/示例直接冲突，用户无法判断该信谁的分数。
- 方案：感叹号检测改为同时匹配全角 `！` 并统计总数量；正面词与垃圾词去重（同一词不得既加又减）；把 `:314` 的示例改为真实低分串（如含“免费/中奖/100%”），或用该串回归测试锁定分数。

### MS-N27 垃圾词与好评词同表双计，明显垃圾标题仍得 83–85 分（中，确认）
- 问题：`优惠`、`折扣`、`恭喜` 同时出现在 `spamWords` 与 `positiveWords`，同一词先扣分再加分；`免费领取`、`恭喜中奖` 这类典型垃圾标题只被扣 10–15 分，情感项又因“命中正面词”加 3 分，最终仍在“优秀”档。
- 证据：`tools/marketing/email-subject-line-tester.html:362-396`（两份词表重叠）、`:537-545`（垃圾词累加）、`:562-571`（正面词只数命中个数，不区分词义）、`:581-587`（`posPct>50` 加 3）
- 复现：`恭喜中奖` → 短标题 −5、垃圾词 恭喜 −5/中奖 −10、正面词“恭喜”使 `posPct=80` +3 → `83` 优秀；`免费领取` → 短标题 −5、免费 −10、无正面词（`posPct=50`）→ `85` 优秀（node 复算）。
- 影响：`tools/marketing/email-subject-line-tester.html`。标题党/诱导词被判“优秀”，与工具“检测垃圾邮件触发词”的核心定位相反。
- 方案：从正面词表移除 `优惠/折扣/恭喜`；垃圾词按类型加权并对总分设置“命中 spam 类词 ≥2 个则最高 59 分”的硬上限；情感项改为基于净情感词数，而非命中即 +3。

### 邮件标题空态表格仍展示内置示例情感分数（中，源码确认）
- `tools/marketing/email-subject-line-tester.html:430-447,450-462,495-508`：清空标题后主评分和情感条归零，图表标题标注「内置示例标题」，但表格使用同一示例数据且标题仍为「情感评分明细」，未注明示例，可能被误读为当前空输入的评分。未运行页面；建议表格也标注示例或随空态清空。

### MS-N28 “预览正文”输入从不参与评分与垃圾词检测（历史结论；当前源码已变化，待运行回归）

> 2026-11-06 静态复核：当前 `scanText = subject + ' ' + preview`，垃圾词检测及扣分已覆盖正文（`tools/marketing/email-subject-line-tester.html:537-554`）；情感与长度仍只按标题，以下「从不参与」为历史证据，未运行回归。
- 问题：页面收集 `previewText` 并渲染到两个预览框，但 `analyze()` 只读取 `subject`；垃圾词、长度、情感、建议全部不看预览正文。真实邮件客户端会同时展示 preheader，垃圾过滤也会扫描它。
- 证据：`tools/marketing/email-subject-line-tester.html:193-194`（输入与 `oninput="analyze()"`）、`:470-595`（`analyze()` 内仅出现 `subject`，无 `previewText`）、`:485-488`（预览框使用 preview）
- 复现：标题“会议纪要”，预览正文填“免费 中奖 !!!”——分数、垃圾词命中、情感三项与留空预览完全一致（源码核对 + 逻辑复算）。
- 影响：`tools/marketing/email-subject-line-tester.html`。用户以为补全预览正文能提高检测覆盖，实际该字段只影响下方 mock 预览的展示。
- 方案：检测文本改为 `subject + ' ' + previewText`（长度分仍只对标题）；或把该字段改名“预览正文（仅展示）”，避免被当作检测输入。

### MS-N29 UTM 基础 URL 含 `#` 片段时参数被拼进 fragment（高，确认）
- 问题：只用 `url.includes('?')` 选择 `?`/`&` 分隔符，未处理 `#`。带锚点的落地页会把 `utm_*` 拼到 `#` 之后，参数不会发送给服务器，渠道归因全部丢失，但复制出的链接外观正常。
- 证据：`tools/marketing/marketing-utm-builder.html:258-259`（`sep=url.includes('?')?'&':'?'`、`finalUrl=url+sep+params`）、`:262-263`（结果与复制按钮直接使用 `finalUrl`）
- 复现：`https://shop.com/p#sku` → `https://shop.com/p#sku?utm_source=wechat&utm_medium=social&utm_campaign=summer_promo`；期望 `https://shop.com/p?utm_source=...&utm_campaign=...#sku`（node 字符串复算）。与既有 MS-N11（`tools/marketing/utm-builder.html`）同族，但本页只有单链接出口，无批量分支。
- 影响：`tools/marketing/marketing-utm-builder.html`。带 SKU/章节/单页路由锚点的投放全部归为 direct/none，且工具无任何校验或警告。
- 方案：先按 `#` 切分为 `base` 与 `fragment`，只在 `base` 上判断 `?` 并追加参数，最后拼回 `#fragment`；多处 `#` 时提示 URL 异常。

### MS-N30 四项全必填与自身 FAQ“仅 source 必填”及 UTM 规范矛盾（中，确认）
- 问题：生成逻辑要求 `url/source/medium/campaign` 四项都非空，否则整块拒绝；但 FAQ 明说“utm_source 必填，medium/campaign 强烈建议”，且标准 UTM 只强制 source。medium/campaign 缺失的用户被迫乱填。
- 证据：`tools/marketing/marketing-utm-builder.html:248-251`（四项空值统一拦截）、`:198`（FAQ“utm_source 必填，medium/campaign 强烈建议”）
- 复现：url `https://x.com/p` + source `wechat`，medium/campaign 留空 → 页面提示“请填写网址、来源、媒介、活动名称（必填项）”；期望生成 `https://x.com/p?utm_source=wechat`（并给出“建议补 medium/campaign”的黄色提示）。
- 影响：`tools/marketing/marketing-utm-builder.html`。只想快速打来源标签的用户被挡在门外，或被迫填写假 medium/campaign，污染报表。
- 方案：仅 `url`（且需是合法 http/https）与 `source` 必填；medium/campaign 为空时照常生成并在结果下方提示“缺少 medium/campaign，渠道报表可能无法细分”。

### MS-N31 UTM 值不做大小写归一，也不检测/替换已有 utm 参数（中，确认）
- 问题：输入仅 `trim()`，没有 `toLowerCase()`，也不解析已有查询串。`WeChat` 与 `wechat` 会成为 GA4 两个来源；URL 已带 `utm_source` 时再追加同名 key，形成重复参数，不同解析器取值不一致。
- 证据：`tools/marketing/marketing-utm-builder.html:241-257`（读取仅 trim，`params.set` 只写新值）、`:258-259`（直接拼接，未解析/去重）
- 复现：source 填 `WeChat` → `utm_source=WeChat`；url 填 `https://x.com/?utm_source=google` → `...?utm_source=google&utm_source=WeChat`（node 复算）。GA4 渠道报表出现 `WeChat`/`wechat` 两条，或按“后者覆盖/前者优先”产生不一致归因。
- 影响：`tools/marketing/marketing-utm-builder.html`。批量投放时大小写混用会系统性拆分渠道数据，重复 key 还会让部分分析平台取错来源。
- 方案：`utm_source/medium/campaign/term/content` 统一 `trim().toLowerCase()`（活动代号允许保留数字/下划线）；解析已有 URL，发现同名 `utm_*` 时提示“将覆盖原值”并 `set` 替换而非追加。

### MS-N32 复制按钮内联 onclick 的转义是空操作，含单引号或标签的 URL 会失效/注入（中，确认）
- 问题：结果用模板字符串拼进 `innerHTML`，复制按钮写成 `onclick="ToolBox.copyText('${finalUrl.replace(/'/g,"\'")}')"`。替换串 `"\'"` 在双引号字符串里就是单个 `'`，等于没有转义；URL 含 `'` 时内联 JS 语法错误，含 `<`/`>` 时被当作 HTML 解析。
- 证据：`tools/marketing/marketing-utm-builder.html:260-265`（`r.innerHTML=...`）、`:262`（`${finalUrl}` 直接插入文本）、`:263`（`replace(/'/g,"\'")`）
- 复现：url `https://x.com/o'brien` + source `wechat` → 生成 `onclick="ToolBox.copyText('https://x.com/o'brien?utm_source=wechat...')"`，点击复制无任何反应（控制台 SyntaxError）；url `https://x.com/<img src=x onerror=alert(1)>` → 预览 div 渲染出图片并执行脚本（自输入场景）。
- 影响：`tools/marketing/marketing-utm-builder.html` 复制按钮与结果预览。含撇号的品牌/活动路径无法复制；HTML 注入虽为本地自输入，但会破坏结果区并可能被粘贴分享的 URL 触发。
- 方案：移除内联 `onclick`，改为 `button.addEventListener('click', ()=>ToolBox.copyText(finalUrl))` 并用 `textContent` 渲染 URL；或至少用 `JSON.stringify(finalUrl)` 生成字符串字面量并对展示文本做 HTML 转义。

#### 留存建议（营销 3 页）

**留存建议（tools/marketing/ad-roi.html）**
- 把三种 ROI 口径合成一个可切换的下拉（利润/总成本、广告毛利/花费、毛利/预算），结果卡同步显示所选公式与分子分母，避免同屏三个数。
- 盈亏平衡区补“保本转化数/保本客单价/保本 ROAS”三件套，并加入固定成本灵敏度（0/当前值/2 倍）并列对比。

**留存建议（tools/marketing/email-subject-line-tester.html）**
- 评分卡改成“100 分构成条”：长度/垃圾词/标点/情感各扣多少分逐项展开，点每一项可高亮标题中的命中片段。
- 增加“Gmail 桌面/iPhone 收件箱”两种真实像素宽度截断预览（按 CSS `ch` 或 canvas 测宽），并把预览正文纳入垃圾词扫描。

**留存建议（tools/marketing/marketing-utm-builder.html）**
- 生成前先解析 URL（协议/域名/查询/锚点），自动把参数插到 `?` 与 `#` 之间，并对已有 `utm_*`、大小写重复给出“将覆盖”的确认。
- 增加多行批量模式（每行一组 source/medium/campaign），一次生成 N 条并导出 CSV，兑现深度解析 `:191` 的“批量生成”承诺。

### 承诺 vs 实际（Q 批专项）

- `tools/marketing/ad-roi.html:10` 宣称“盈亏平衡点”，实际只有 `:320-325` 的 ROAS 阈值，没有保本单量/保本销售额；`:140` 宣称“调整 CTR 即可比较”，CPC 模式下 CTR 不进 ROI（见 MS-N25）。
- `tools/marketing/email-subject-line-tester.html:10` 宣称“帮助提升邮件打开率与送达率”，`:187` 副标题写“likely open rate”，但 `:470-595` 只有关键词启发式打分，无打开率预测、无 SPF/DKIM/垃圾过滤送达率检测；`:682-684` 宣称“多维度数据分析/图表可视化”，页面无任何图表元素。
- `tools/marketing/marketing-utm-builder.html:191` 宣称“批量生成多活动链接导入投放后台”，实际只有 `:241-265` 的单链接生成；`:442` 宣称“图表可视化”，但 `:338-342` 用 `parseFloat` 解析以“生成的UTM追踪链接：”开头的结果串恒为 NaN，图表永不渲染；`:440` “多维度数据分析”仅有单条链接输入。

### 覆盖
- 本轮实读 3 页：`tools/marketing/ad-roi.html`、`tools/marketing/email-subject-line-tester.html`、`tools/marketing/marketing-utm-builder.html`。
- 新增 11 条：高 5（MS-N22/23/24/26/29）、中 6（MS-N25/27/28/30/31/32）、低 0。
- 未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N29 与既有 MS-N11（`utm-builder.html`）同属“fragment 拼接”族但页面不同，MS-N22/23/24 为“ROI 口径/保本判定”新族，其余为评分词表、必填校验、内联转义族，均无重号。
- 未做浏览器实测、英文态（`?lang=en-US`）核对、移动端视口验证与门禁运行；金额/比率均由 node 按源码同式复算。

### MS-N33 弧弹性页两个深解算例按简单百分比算，第二个算例收入多写 6600 元（高，确认）
- 问题：页面公式与 `calc()` 都声明用弧弹性（中点法），但深解两个算例用 `(q2−q1)/q1` 与 `(p2−p1)/p1` 的简单变化率；第二个算例收入也写错。
- 证据：`tools/marketing/calc-price-elasticity.html:126`（中点法公式）、`:166-170`（`midQ/midP` 计算）、`:386`（“−15%/+10%=−1.5”）、`:387`（“100000 升到 113300”）。
- 复现（node）：P1=100,Q1=1000,P2=110,Q2=850 → 中点法 Ed=(−150/925)/(10/105)=−1.7027（页面写 −1.5），收入 93500（页面正确）；P2=110,Q2=970 → Ed=(−30/985)/(10/105)=−0.3198（页面写 −0.3），收入 106700（页面写 113300，差 6600）。
- 影响：用户照深解复算会得到与工具不一致的弹性与收入；第二个算例把“提价 10% + 销量 −3%”误算成收入 +13.3%，实际 +6.7%，会误导提价决策。
- 方案：深解算例改用与 `calc()` 同一中点法函数计算并回填数值；把 113300 改为 106700，并补一句“若按简单百分比法才得 −1.5/−0.3”。

### MS-N34 ΔP=0 时 Ed 未定义，页面却判“单位弹性、收入基本不变”（中，确认）
- 问题：`ed=pctP!==0?pctQ/pctP:NaN` 后 `abs=NaN`，三个判读分支全部不命中，落入 `else` 的单位弹性；但销量可能已大幅变化、收入已变。
- 证据：`tools/marketing/calc-price-elasticity.html:166-171`、`:175-184`、`:189-190`。
- 复现（node）：P1=P2=100、Q1=1000、Q2=1300 → `pctP=0`、`ed=NaN`、`abs=NaN`；结果卡 Ed/|Ed| 显示“-”，判读却是“单位弹性（|Ed|=1）”、建议“收入基本不变”；同屏收入 100000→130000（+30000，+30%）。
- 影响：价格不变、靠销量增长的正常场景会出现自相矛盾的结论。
- 方案：`dP===0` 单独分支：`dQ===0` 显示“价格与销量均未变”，否则显示“价格未变，弹性无定义”，建议只按收入变化给出；不要把 NaN 归入单位弹性。

### MS-N35 参考表公式带负号，与页面“带符号”口径及代码符号相反（低，确认）
- 问题：`:127` 明确“Ed=需求变化率÷价格变化率（带符号）”，代码 `ed=pctQ/pctP`（正常需求为负）；但参考表 `:351` 写 `Ed = −(%ΔQ)/(%ΔP)`，多一个负号，正常需求变正。
- 证据：`tools/marketing/calc-price-elasticity.html:127`、`:170`、`:351`。
- 复现（node）：P1=100,Q1=1000,P2=90,Q2=1300 → 代码 Ed=(300/1150)/(−10/95)=−2.4783；按参考表 −(%ΔQ)/(%ΔP)=+2.4783。
- 影响：同一页两种符号约定；用户对照教材/考试公式会认为工具算错。
- 方案：参考表去掉负号，或明确标注“Ed 取绝对值口径”；结果卡同时给“带符号 Ed”和“|Ed|”，并在参考表注明取绝对值。

### MS-N36 预算分配把输入占比当实际占比，合计≠100% 时表内百分比与分配额不符（中，确认）
- 问题：分配额按 `totalBudget*c.ratio/totalRatio` 归一，但表格“占比”直接显示 `c.ratio%`，合计行显示 `totalRatio%`；三项各 40% 时每项实际 33.33%，表内仍写 40%，合计写 120%。
- 证据：`tools/marketing/cpc-calculator.html:476-477`（合计）、`:483`（归一分配）、`:491`（显示 c.ratio）、`:503`（合计 totalRatio）。
- 复现（node）：总预算 50000、三渠道 40/40/40 → `totalRatio=120`，每渠道 50000×40/120=16666.67（33.33%）；表内“40%”×3、“合计 120%”。
- 影响：预算分配页最核心的占比展示错误，用户会按 40% 做渠道预算。
- 方案：合计≠100% 时表内占比改为 `(c.ratio/totalRatio*100)`，合计固定 100%，并提示“输入合计 120%，已按比例归一”；或直接拒绝非 100% 输入。

### MS-N37 费用换算/预算分配/效果估算均无范围校验，负数产生负点击、负转化与负预算（中，确认）
- 问题：三个计算入口都用 `parseFloat(...)||0`，只做了 NaN/Infinity 兜底，没有要求正数；`calcBudget` 也只判断 `totalRatio>0` 才分配，未拒绝负预算/负 CPC。
- 证据：`tools/marketing/cpc-calculator.html:399-428`（换算）、`:473-511`（分配）、`:514-534`（估算）。
- 复现（node）：预算 −10000、CPC 2、CTR 2.5%、CVR 3% → CPC ¥2、CPM ¥0、CPA ¥0、展现 −200000、点击 −5000、转化 −150；效果估算 `estCpa=−80` → 预算 −80000、收入 299000、利润 199600、ROI 0.0%。
- 影响：负指标可被计算并进入历史/导出；ROI 在负预算时被 `budget>0` 直接置 0，结果不可解释。
- 方案：换算要求 budget/unitPrice/ctr/cvr>0；分配要求 totalBudget≥0、每个 ratio 0–100 且合计>0；估算要求 targetConv/estCpa/estCtr/estCvr/estPrice>0、estMargin 0–100；不满足时结果区红字提示且不写历史。

### MS-N38 上一级为 0 时同一环节表格显示 100%、漏斗图与 CSV 显示 0%（中，确认）
- 问题：汇总表 `prevVal>0?val/prevVal*100:100`，可视化与 CSV 同条件却回退 0；同一数据在三个出口给出相反值。首级为 0 时整体转化固定 0%，也没有“不可计算”提示。
- 证据：`tools/marketing/funnel-calculator.html:439`（整体）、`:457`（表格 100 兜底）、`:477`（可视化 0 兜底）、`:568`（CSV 0 兜底）。
- 复现（node）：步骤 100→0→100 → 首级 100、末级 100、整体 100%；第三级汇总表 100.00%（100/0 命中 100 兜底），可视化 0.0%，CSV 0.00%；若首级 0→100→100，整体 0.00%。
- 影响：零值多来自埋点缺失；用户会同时看到 100% 和 0% 两个结论，且导出 CSV 与页面不一致。
- 方案：抽 `rate(prev,val)`，`prev<=0` 返回 `null`，汇总/可视化/CSV 统一显示“—/不可计算”；首级 <=0 时整体也显示“—”，并在输入行标红提示“上一级为 0，无法计算环比”。

### MS-N39 meta 承诺“定位转化流失瓶颈”，实际仅按 <50% 标红，未计算流失人数/排序（中，确认）
- 问题：`rateClass` 只看 `stepRate>=50`；没有 `prev-val` 流失人数列、没有最大流失环节、没有排序。深解“支付环节最严重”靠人工判断。
- 证据：`tools/marketing/funnel-calculator.html:10`、`:15` meta；`:459`、`:484-485` 标红逻辑；`:307` 深解人工结论。
- 复现（源码）：1000→950→100→90 → 环比 95%、10.53%、90%；页面只把中间级标 down，未输出“流失 850 人”或“最大流失环节”；代码中无 `drop`/`max` 排序变量。
- 影响：“定位瓶颈”需用户自己心算；与 meta/深解承诺不符。
- 方案：增加 `lost = prev-val` 列，按 lost 降序取 Top1，在结果卡输出“最大流失：第 X 级→第 Y 级，流失 N 人（环比 Z%）”并高亮；阈值可配置（默认 50%）。

### MS-N40 深解“支付环节 10% 掉单最严重”把环比转化率写成掉单率（低，确认）
- 问题：10% 是“支付/下单”的环比转化率，掉单率应为 90%；同页 FAQ 还把“客单价”写成“乘客单价”。
- 证据：`tools/marketing/funnel-calculator.html:307`（“逐级 50%/20%/10%…支付环节 10% 掉单最严重”）、`:312`（“各级乘客单价估算 GMV”）。
- 复现（node）：下单 1000→支付 100 → 转化 10%，掉单=(1000−100)/1000=90%；按页面“10% 掉单”会少算 800 单。
- 影响：深解与 FAQ 的口径/用词错误，影响用户理解与 SEO 文案质量。
- 方案：改为“支付环节转化率仅 10%（掉单率 90%）”；“乘客单价”改“客单价”。

#### 留存建议（R 批 3 页）

**留存建议（tools/marketing/calc-price-elasticity.html）**
- 在 `calc()` 中统一 `elasticity(p1,q1,p2,q2)` 返回 `{ed, defined}`，`dP=0` 或 `q1=q2` 时输出“弹性无定义”，并由同一函数生成表格/图表/深解算例，杜绝 100/0 分叉。
- 深解算例改为中点法实算值（−1.7027、−0.3198）并把收入 106700 写进页面；参考表去掉负号或统一注明“取绝对值”。

**留存建议（tools/marketing/cpc-calculator.html）**
- 预算分配在输入合计≠100% 时显示“合计 X%，已按比例归一”：表内“占比”用 `c.ratio/totalRatio*100`，并补“剩余/超出”提示；否则禁止分配。
- 统一入口校验：预算、单价、CTR/CVR、目标转化、CPA、客单价 >0，毛利率 0–100；不合规时在结果区给红色错误，不写历史。

**留存建议（tools/marketing/funnel-calculator.html）**
- 抽一个 `rate(prev,val)` 返回 `null`（`prev<=0`），summary/visual/CSV 共用，0 级显示“—/不可计算”，不再用 100 兜底。
- 增加“流失人数=prev-val”列并按降序高亮 Top1 瓶颈，同步在结果卡显示“最大流失环节 + 流失人数”，兑现 meta。

### 承诺 vs 实际（R 批专项）

- `tools/marketing/calc-price-elasticity.html:10`、`:123` 宣称“采用弧弹性（中点法）…给出定价策略建议”，`:166-183` 核心计算已实现；但 `:386-387` 两个深解算例仍用简单百分比、`:387` 收入写成 113300，`:351` 参考表又给公式加负号，形成三处口径冲突（见 MS-N33/N35）。
- `tools/marketing/cpc-calculator.html:10` 宣称“在 CPC/CPM/CPA 间换算…估算投放效果”，`:399-428`、`:514-534` 三种计费换算与效果估算已实现；但 `:483` 按合计归一分配而 `:491`/`:503` 仍显示输入占比，“预算分配”的承诺与实际分配不一致（见 MS-N36），且全页无正数范围校验（MS-N37）。
- `tools/marketing/funnel-calculator.html:10`、`:15` 宣称“定位转化流失瓶颈”，`:454-468` 只输出各级环比/总体转化率，`:459` 仅按 <50% 标红，未计算流失人数和最大流失环节；深解 `:307` 的“最严重”是人工结论（见 MS-N39）。

### 覆盖
- 本轮实读 3 页：`tools/marketing/calc-price-elasticity.html`、`tools/marketing/cpc-calculator.html`、`tools/marketing/funnel-calculator.html`。
- 新增 8 条：高 1（MS-N33）、中 5（MS-N34/36/37/38/39）、低 2（MS-N35/40）。
- 未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N35 为“同页符号/口径矛盾”新族，MS-N36/37 为“占比归一化/范围校验”新族，MS-N38/39 为“零值兜底分叉/瓶颈未实现”新族，均无重号。
- 未做浏览器实测、英文态（`?lang=en-US`）核对、移动端视口验证与门禁运行；金额/比率/弹性均由 node 按源码同式复算。

## 2026-11-04 续查（并行批 S）

### MS-N41 品牌“7 维审计/评分”只剩单系数，市场占有率是死输入（高，确认缺陷）

- 问题：标题、摘要、功能介绍宣称基于 Interbrand 的 7 维品牌审计/评分，实际只输入一个“品牌强度系数”，没有 7 个子项、权重或审计清单；`市场占有率` 只回显，完全不参与估值。
- 证据：`tools/marketing/assessor-51.html:10`（Interbrand 评估思路）、`:123`（structured scorecard / audit maturity）、`:205`/`:232`/`:286`（7 维度）、`:131`（唯一 strength 输入）、`:134`（share 输入）、`:214-232`（calc 只用 `st`，`share` 仅在 `:231` 回显）。
- 复现：node 按 `:218-229` 同式算默认值 → 品牌净利润 3250 万元、调整折现率 13.25%、PV 17460.48 万元；仅把 share 15 改成 90，源码无 share 引用，PV 仍为 17460.48。
- 影响：用户以为完成了“7 维审计/评分”，实际只得到一个线性强度分；SEO 与功能承诺不符。
- 方案：要么补 7 个子评分（每维 0–10 + 权重）并加权成 strength，输出维度得分/雷达图/缺失项清单；要么把标题、meta、功能列表收窄为“单系数品牌资产估值”，删除 7 维与审计表述，并移除 share 或让它进入市场地位调整。

### MS-N42 深解算例 1137 与源码口径不符，品牌强度调整被忽略（中，确认）

- 问题：深解写“强度 0.8、折现率 10%、5 年 → 品牌资产现值约 1137 万元”，但源码先按 `adjustedDiscount=dr/100+(1−st)×0.05` 得 11%，PV 应为 1108.77；1137 是按 10% 直接折现、未加强度调整的结果。
- 证据：`tools/marketing/assessor-51.html:165`（1137 万元算例）、`:220-222`（调整折现率与折现循环）。
- 复现：node → `300×Σ(1.11^-i, i=1..5)=1108.77`；若按 1.10 折现才得 1137.24，差 28.47 万元。
- 影响：页面示例不可复现，用户用计算器对照会得到不同答案，损害可信度。
- 方案：示例改为 1108.77；若坚持 1137，则明确标注“不考虑品牌强度调整、按 10% 折现”，并同步公式说明；示例值应由同一段逻辑生成。

### MS-N43 强度/贡献率/折现率/年限无范围校验，极端输入算出 1.78e82（中，确认）

- 问题：calc 没有输入守卫；空值用 `||0`/`||1` 静默兜底；贡献率可 >100、强度可 <0 或 >1、折现率可为负、年限可负/0（0 被替换为 1）。
- 证据：`tools/marketing/assessor-51.html:215-222`（取值、兜底、adjustedDiscount、循环）。
- 复现：node → `st=3` 时 adjusted=0.02、PV=29193.40（默认 17460.48）；`st=23.4` 时 adjusted≈−1、PV=1.78e82；contribution=200 时品牌净利润翻倍。清空折现率会变成 1% 而非 12%。
- 影响：明显越界/误输入仍输出“权威”估值，可能被用于投融资沟通。
- 方案：显式校验 contribution 0–100、strength 0–1、discount >0、years 1–50 的整数；违规在结果区报错且不写历史；不要用 `||` 把空值变成 0/1。

### MS-N44 达人报价基准 100–500 元/千粉，与深解 10 元/千粉差 40 倍，默认输出 49.5 万（高，确认）

- 问题：calc 按粉丝量级硬编码 cpmBase=100/200/300/400/500，50 万粉取 400；深解示例明确“基础千粉价 10 元”，5 万粉 ×10×1.2=600 元。按同系数，50 万粉应约 12375 元，页面默认却给 495000 元。
- 证据：`tools/marketing/marketing-influencer-pricing.html:149`（“粉丝数÷1000×CPM”）、`:152-155`（默认 500000/3/1.5/1.5）、`:248-255`（cpmBase 档位与 engBonus）、深解 `:191`（10 元/千粉、600 元）。
- 复现：node 同式 → `500×400×1.1×1.5×1.5=495000`；按深解 10 元/千粉 → `500×10×1.1×1.5×1.5=12375`，差 40 倍。深解 50k 案例若按页面档位 cpm=200，则 `50×200×1.1=11000`，也不是 600。
- 影响：报价锚点高一个数量级，商务议价直接失真；深解与工具互相打脸。
- 方案：把“千粉单价”改为用户输入（默认 10 元/千粉），粉丝量级只做系数或建议区间；若要保留 CPM，则必须按“预估曝光量”而非粉丝数计算；深解案例与代码共用同一基准表。

### MS-N45 互动率/平台系数/内容系数无校验，负互动率算出负报价（中，确认）

- 问题：仅校验 followers/eng 为 NaN 且 followers>0（`:244`）；platformFactor/contentType 为空或负数、eng 为负都不拦截；`engBonus=1+(eng−2)/10` 可为负。
- 证据：`tools/marketing/marketing-influencer-pricing.html:241-255`。
- 复现：node → `eng=−20` 时 engBonus=−1.2、price=−540000 元；platformFactor 留空 → price=NaN；contentType=−1 → 负报价。
- 影响：结果区出现负报价/NaN，用户无法判断是输入错误还是模型结果。
- 方案：eng 限 0–100、platform/content 必须 >0；空值/NaN/负值在结果区报“请填写有效系数”，不输出报价区间。

### MS-N46 “CPM”被当成千粉成本，与参考表定义相反（低，确认文案/口径）

- 问题：公式把 `粉丝数÷1000×CPM` 称为 CPM，但参考表定义 CPM=报价/预估曝光×1000（千次曝光成本），两者不是同一量纲。
- 证据：`tools/marketing/marketing-influencer-pricing.html:149`、`:188`（“CPM（千粉成本）”）、`:219-220`（参考表 CPM 定义）。
- 复现：静态对照：源码 `:255` 只用 followers/1000 乘 cpmBase，页面没有“预估曝光/阅读”输入，无法计算真正的 CPM。
- 影响：懂投放的用户会误读，跨工具/跨达人比较口径不一致。
- 方案：改名“千粉报价（元/千粉）”，或增加“预估曝光/阅读”输入按 `:220` 真正算 CPM，并与千粉价分列展示。

### MS-N47 中英混排时密度分母错位，英文关键词低报 3–15 倍；中文未分词（中，确认）

- 问题：只要正文含汉字，`totalChinese>0` 就一律用中文字数作分母，英文关键词分子只算 `count×1`；纯英文关键词在中文正文里会被系统性低报。中文只做子串计数，没有分词。正文只要出现 1 个汉字，纯英文内容也会切到中文字数分母，密度反而暴增。
- 证据：`tools/marketing/marketing-keyword-density.html:247-259`（尤其 `:257-259` 的注释与实际公式）、`:216`（参考表写“按分词后的出现次数统计”）。
- 复现：node → 500 个汉字中含 5 次“SEO”：`:259` 得 `5×1/500=1.00%`；按字符密度 `5×3/515=2.91%`，低报约 3 倍；若关键词是 15 字符英文短语则低报 15 倍。
- 影响：SEO 健康/堆砌判断错误，用户可能误删内容或继续堆词。
- 方案：按内容主语言选择分母；统一为“关键词字符数/参与统计的总字符数（含中英文数字）”，中文短语用 `keyword.length`、英文单词用整词匹配；页面明示“不做中文分词”，或引入 `Intl.Segmenter('zh',{granularity:'word'})` 提供分词模式。

### MS-N48 健康区间三处口径不一：2.5% 与 3%（低，确认）

- 问题：公式框写“1% 至 2.5%”，深解、参考表、结果文案写“1%–3%”，代码判读也用 1–3。
- 证据：`tools/marketing/marketing-keyword-density.html:152`、`:190`、`:221`、`:260`、`:269`。
- 复现：静态检索：`2.5%` 仅出现在 `:152`；`1%-3%` 出现在 `:190`/`:260`/`:269`。以 density=2.8% 跑 `:260` 得“✅ 密度健康”，按 `:152` 已超上限。
- 影响：同一页面给出相反建议。
- 方案：抽 `DENSITY_MIN/MAX` 常量并全页引用；确定采用 1–3 或 1–2.5，深解与参考表同步。

### MS-N49 深解写“多笔记赞藏评粉汇总/赞粉比”，实际只是单篇字数计数器（高，确认）

- 问题：深解场景与示例要求录入 30 篇笔记的赞、藏、评、粉，算篇均互动、爆款占比、赞粉比；页面只有一个正文 textarea，没有任何点赞/收藏/评论/粉丝输入或汇总表。
- 证据：`tools/marketing/xiaohongshu-counter.html:391-399`（多笔记/赞粉比深解）、`:127-131`（唯一 textarea 与单一上限）、`:229-246`（calc 只数字符/行/词/话题）。
- 复现：静态：`document.querySelectorAll('input,textarea')` 只有 `#text` 与 `#limit`；深解 `:398` 的 45000/6000/8000 无对应字段，node 无法按该案例构造输入。
- 影响：核心承诺未实现，深解与工具能力错位，属于典型“内容先行、功能未落地”。
- 方案：二选一：① 新增多笔记表格（每行赞/藏/评/粉），汇总篇均互动、赞粉比、爆款占比；② 把深解整段改写为字数、话题、表情统计，删除多笔记与赞粉比表述。

### MS-N50 宣称统计“标题与正文”，实际无标题字段；emoji 按 UTF-16 多计（中，确认）

- 问题：meta 说统计“标题与正文字符数”，页面只有正文 textarea 和一个 1000 上限，标题 20 字规则未体现。字符直接用 `text.length`，代理对/ZWJ/旗帜 emoji 被算成 2/11/4 个字符。
- 证据：`tools/marketing/xiaohongshu-counter.html:43`、`:128-131`、`:232`、`:151`、`:156-157`。
- 复现：node → `'😀'.length=2`、`'👨‍👩‍👧‍👦'.length=11`、`'🇨🇳'.length=4`；若平台按 1 个表情计，50 个 emoji 会虚增 50–500 字符，提前报“超出”。
- 影响：标题合规无法检查；emoji 文案误报超限。
- 方案：拆“标题（20 字）/正文（1000 字）”两个输入与各自计数；用 `[...text].length` 或 `Intl.Segmenter` 按字素簇计，并标注“emoji 按 1 个计”，可另留 UTF-16 技术计数。

### MS-N51 话题标签只认半角 `#`，全角 `＃` 漏计；上限 0/负数被静默改成 1000（低，确认）

- 问题：正则 `/#[^#\s]+/g` 不含全角 `＃`；`Number(value)||1000` 把 0/NaN/负数都当 1000。
- 证据：`tools/marketing/xiaohongshu-counter.html:234-235`。
- 复现：node → `'＃秋日穿搭'.match(/#[^#\s]+/g)` 为 null（0 个），`'#a #b'` 为 2；把上限填 0，`:235` 得 1000，仍按 1000 判剩余。
- 影响：手机中文键盘常用全角＃，话题数偏少；上限 0 无法表达“不允许正文”的校验。
- 方案：正则改 `[#＃]`；上限用 `Number.isFinite` + `>0` 校验，0/负数报错而非兜底 1000。

### MS-N52 名为“活动追踪器”，实际只生成链接/图片，没有扫码与转化字段（高，确认）

- 问题：meta、正文、深解都说统计线下物料扫码效果、对比各码扫码与转化；实际输入只有 URL/source/location/campaign/qrId，输出只有追踪链接和二维码图，没有扫码数、转化数、汇总或渠道对比。
- 证据：`tools/marketing/marketing-qr-campaign-tracker.html:10`、`:145`、`:188-193`、`:239-266`。
- 复现：静态：`#result` 只插入 `<img>`、trackUrl 与复制按钮（`:259-266`）；源码没有 `scan`/`conversion`/“扫码”输入；深解 `:192-193` 的 1200/800/300、60/120 无字段可填。
- 影响：用户按“追踪器”使用拿不到任何活动数据；SEO 承诺落空。
- 方案：要么增加“每个码的曝光/扫码/转化”手工录入与汇总（localStorage 持久化），输出扫码率、转化率、渠道对比；要么把标题/meta/深解收窄为“UTM 二维码生成器”，删除统计与转化案例。

### MS-N53 二维码由第三方 `api.qrserver.com` 生成，trackUrl 全量外发，和“数据不上传”冲突（高，确认）

- 问题：结果图 `src` 把含 campaign/location/qr_id 的完整 trackUrl 编码进第三方 API 查询串；打开页面即发起外部请求，第三方可见落地页与活动参数。meta 仍称“纯前端运行、数据不上传”。
- 证据：`tools/marketing/marketing-qr-campaign-tracker.html:258-261`（第三方 API 与 `<img src>`）、`:10`（数据不上传）。
- 复现：`node -e 'const t="https://a.com/p?utm_source=x&location=y"; console.log("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data="+encodeURIComponent(t))'` → 输出 query 内含完整链接；页面无本地二维码库。
- 影响：违反项目纯前端/数据不外发约束；活动链接（可能含未公开落地页、门店编号）泄露给第三方，离线或被墙时二维码不显示。
- 方案：内置本地二维码生成（打包 qrcode 库或 canvas 实现），禁止运行时第三方请求；若短期保留，必须明示第三方并移除敏感参数，长期替换。

### MS-N54 带 `#fragment` 的落地页把 UTM 拼进片段；UTM 字段与公式不符且可重复/注入（中，确认）

- 问题：`sep` 只看 `?` 不看 `#`，`https://x/p#top` 会拼成 `...#top?utm_...`，参数进不了服务端。已有 `utm_source` 时直接追加同名参数；公式承诺 `utm_term/utm_content` 但无输入；trackUrl 未转义直接进 innerHTML，onclick 的 `replace(/'/g,"\'")` 是无效转义（`\'` 等于 `'`）。
- 证据：`tools/marketing/marketing-qr-campaign-tracker.html:149`、`:151-156`、`:250-257`、`:264-265`。
- 复现：node → `new URL('https://example.com/p#top?utm_medium=qrcode&utm_source=x')` 得 `search=''`、`hash='#top?utm_medium=qrcode&utm_source=x'`，`searchParams.get('utm_source')` 为 null；base 已有 `?utm_source=a` 时输出两个同名参数。
- 影响：最常见的锚点落地页追踪全部失效；重复参数让分析平台取值不确定；含引号/尖括号的 campaign 可破坏复制按钮或注入 DOM。
- 方案：用 `new URL(baseUrl)`，保留/写回 `hash`，统一操作 `searchParams`（自动去重/编码）后 `toString()`；补 term/content 输入或删公式表述；输出用 `ToolBox.escHtml`，复制按钮用事件绑定而非内联 onclick。

#### 留存建议（S 批 5 页）

**留存建议（tools/marketing/assessor-51.html）**
- 若保留“审计”定位：新增 7 维评分表（每维 0–10 + 权重），`strength=加权和/10`，输出维度得分、雷达图与缺失项清单；否则删除 `:205`/`:232`/`:286` 的 7 维文案，标题改为“品牌资产估值（单系数）”。
- 补范围校验与空值报错；`share` 要么进入市场地位调整（如按份额对 strength 加减分），要么删除输入与 `:231` 回显。
- 深解算例改用 `:220-222` 的实算值 1108.77，示例数字由脚本生成，避免再次手写。

**留存建议（tools/marketing/marketing-influencer-pricing.html）**
- 把“千粉单价”做成输入（默认 10 元/千粉），粉丝量级只给建议系数/区间；删除硬编码 100–500 或改成可配置基准表，确保深解 `:191` 与 `:248-255` 同源。
- 校验 eng 0–100、platform/content >0；负值/空值报错，不输出负报价；结果区同时给“报价区间 + 千粉价 + 按曝光计的 CPM”，避免术语混淆。
- 可选：增加预算、预估曝光、转化率、客单输入，给“性价比/ROI”一个可计算口径，而不只比较粉丝数。

**留存建议（tools/marketing/marketing-keyword-density.html）**
- 抽 `density()` 纯函数：按内容主语言选分母，中文短语用字符、英文用整词，分母包含中英文数字；结果区显示“当前分母口径”。
- 统一阈值常量与文案（1–3 或 1–2.5）；在结果卡标明采用哪一档。
- 若要支持分词，提供“分词模式/字符模式”切换，并说明 `Intl.Segmenter` 的切分口径。

**留存建议（tools/marketing/xiaohongshu-counter.html）**
- 拆标题/正文两栏：标题上限 20、正文上限 1000（可改），各自计数与超限提示；话题、链接单列。
- 字符计数改字素簇（`[...text]` 或 `Intl.Segmenter`），结果注明“emoji 按 1 个计”；UTF-16 计数可作为可选技术口径。
- 若保留 `:391-399` 深解，新增多笔记表（赞/藏/评/粉）与篇均、赞粉比、爆款占比；否则整段改写为字数规则。

**留存建议（tools/marketing/marketing-qr-campaign-tracker.html）**
- 若保留“追踪器”：增加曝光/扫码/转化手工录入，按 `qr_id` 汇总扫码率、转化率、渠道对比，localStorage 持久化；深解案例改为可填字段。
- 二维码改本地生成（qrcode 库或 canvas），移除 `api.qrserver.com`，页面明示“所有数据留在浏览器”。
- 链接拼接改用 `new URL` + `searchParams`，处理 `#`、去重、补 term/content 或删公式；输出统一 `escHtml` 与事件绑定复制。

### 承诺 vs 实际（S 批专项）

- `tools/marketing/assessor-51.html:10`/`:123`/`:205` 宣称 Interbrand 7 维评分与品牌审计，实际 `:131` 只有一个 strength 系数、`:134` 的 share 仅在 `:231` 回显，`:214-232` 无 7 维加权；深解 `:165` 的 1137 也与 `:220-222` 的 1108.77 不符（见 MS-N41/N42）。
- `tools/marketing/marketing-influencer-pricing.html:149` 宣称按 CPM 估算报价，`:248-255` 实际用 100–500 元/千粉，深解 `:191` 却用 10 元/千粉，默认输出 495000 元 vs 同系数 12375 元（见 MS-N44）；`:241-255` 无负值/空值校验（MS-N45）。
- `tools/marketing/marketing-keyword-density.html:152` 写 1%–2.5%，`:190`/`:221`/`:260`/`:269` 写 1%–3%；`:247-259` 的混排分母导致英文词低报，且 `:216` 宣称“按分词”但实际只做子串计数（见 MS-N47/N48）。
- `tools/marketing/xiaohongshu-counter.html:43` 宣称统计“标题与正文”，实际 `:128-131` 只有正文与单一上限；深解 `:391-399` 的多笔记赞藏评粉/赞粉比在 `:229-246` 无任何实现（见 MS-N49/N50）。
- `tools/marketing/marketing-qr-campaign-tracker.html:10`/`:145`/`:188-193` 宣称统计扫码与转化，实际 `:239-266` 只生成链接/图片；`:258-261` 又把 trackUrl 发给第三方 `api.qrserver.com`，与 `:10` 的“数据不上传”冲突（见 MS-N52/N53）；`:256` 未处理 `#`（MS-N54）。

### 覆盖

- 本轮实读 5 页：`tools/marketing/assessor-51.html`、`tools/marketing/marketing-influencer-pricing.html`、`tools/marketing/marketing-keyword-density.html`、`tools/marketing/xiaohongshu-counter.html`、`tools/marketing/marketing-qr-campaign-tracker.html`。
- 新增 14 条：高 5（MS-N41/44/49/52/53）、中 6（MS-N42/43/45/47/50/54）、低 3（MS-N46/48/51）。
- 未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N41 为“多维度/审计承诺未实现”族，MS-N44 为“基准单价与深解差一个数量级”族，MS-N52 为“追踪器无追踪”族，均与既有编号无重号。
- 未做浏览器实测、英文态（`?lang=en-US`）核对、移动端视口验证与门禁运行；金额/比率/密度均由 node 按源码同式复算，二维码 fragment 用 `new URL()` 验证。

## T 批 marketing 覆盖（2026-11-04）

### MS-N55 市场份额页不拦负数，零总额静默保留上一次结果（高，确认缺陷）
- 问题：数值输入只设 `min="0"`，键盘录入负值仍进入计算；合计 `total<=0` 时直接 `return`，既不报错也不清空旧结果。
- 证据：`tools/marketing/market-share.html:265`（`min="0"` + `comps[i].value=+this.value`）、`:278`（`if(total<=0){ return; }`）、`:280-284`（份额/HHI 直接按行计算）
- 复现：企业A=-2000、企业B=3000（合计1000）→ 页面份额 -200%/300%、HHI 130000、等级“高度寡占”；期望拒绝负值并提示。把全部数值改为0 → 页面无提示，仍显示上一次的 HHI/CR4/饼图；期望显示“合计须大于0”。
- 影响：`tools/marketing/market-share.html` 结果区与饼图；负份额会被当成真实市场份额，零总额时旧结论被误认为本次结果。
- 方案：计算前校验每个 `value>=0` 且 `total>0`，否则清空结果区并给出错误提示；不要用 `return` 静默跳过。

### MS-N56 HHI/CR4 把合并行“其他”当成单一企业，集中度被系统性高估（高，确认缺陷）
- 问题：页面默认数据含“其他 4000”，代码把该行与具名企业同等平方求和、参与 CR4，等于假设“其他”份额由一家公司独占。
- 证据：`tools/marketing/market-share.html:254`（默认 `{name:'其他', value:4000}`）、`:280-284`（`shares` 直接平方、`slice(0,4)` 求和）、`:288-291`（按 HHI 判集中度）
- 复现：企业A=3000、“其他”=7000 → HHI=5800“高度寡占”、CR4=100%；若“其他”实为70家各1%，真实 HHI=970“竞争型”。默认预设同理会把 2755 的“中度寡占”进一步抬高。
- 影响：`tools/marketing/market-share.html` 的 HHI/CR4 与竞争格局结论；用户按预设录入“其他”即得到偏高的集中度。
- 方案：识别名称为“其他/Other”的行，HHI/CR4 仅对具名企业计算，并提示“未覆盖份额 X%”；或拆出“其他”输入企业数后按均分估算。

### MS-N57 样本量深解 90%/99% 算例数值错误（高，确认缺陷）
- 问题：同一组 p=0.5、e=5% 下，深解写 90%→267、99%→663；按页面自身 Cochran 公式实算应为 271、664。
- 证据：`tools/marketing/estimate-sample-size-confidence.html:400`（深解“n≈267…→663”）、`:197-198`（`n0=(z*z)*p*(1-p)/(e*e)`）
- 复现：p=50%、e=5%：90% 置信 `1.645²×0.25/0.0025=270.6→271`；99% 置信 `2.576²×0.25/0.0025=663.58→664`；95%=385 正确。页面写 267/663，267 对应隐含 z≈1.634，与所列 1.645 不符。
- 影响：`tools/marketing/estimate-sample-size-confidence.html` 深解；用户拿深解核对计算器会误判工具算错，教学值本身不可复现。
- 方案：深解改为 271/664，并由脚本按 `cochran()` 同式生成示例数字。

### MS-N58 预期比例允许 0/100，直接输出 0 份样本（中，确认缺陷）
- 问题：比例校验仅排除 `p<0||p>1`，端点 0%、100% 被放行，Cochran 公式分子为 0，样本量变为 0。
- 证据：`tools/marketing/estimate-sample-size-confidence.html:203`（`if(p<0||p>1)`）、`:204-215`（n0/nInf/nFpc 展示）、`:235`（应答率放大）
- 复现：p=0（或100）、e=5%、95%、N=0 → “无限总体样本量 n₀ 0”“实际需发放问卷约 0 份”；期望提示比例须在 (0,100) 内，或按 p=50% 计算。
- 影响：`tools/marketing/estimate-sample-size-confidence.html` 结果区与多置信水平表全部为 0，结论不可用于任何调研。
- 方案：改为 `p<=0||p>=100` 报错；若产品希望保留端点，则自动改用 p=0.5 并明示。

### MS-N59 A/B 深解 z≈2.45/p≈0.014 与池化 z 检验实算不符（高，确认缺陷）
- 问题：250/2000 与 260/2000 的两比例检验，池化标准误算出 z≈2.97、双侧 p≈0.003，深解却写 2.45/0.014。
- 证据：`tools/marketing/marketing-ab-test-significance.html:211`（深解“z≈2.45，双侧 p≈0.014”）、`:302-305`（`pPool`/`se`/`z`/`pValue`）
- 复现：A 200/2000=10%，B 260/2000=13%，pPool=0.115，se=√(0.115×0.885×(1/2000+1/2000))=0.010088，z=0.03/0.010088=2.9737，双侧 p=0.00294；页面写 2.45/0.014。
- 影响：`tools/marketing/marketing-ab-test-significance.html` 深解；显著性结论不变，但数值错约20%、p 值差约5倍，临界样本判断会被带偏。
- 方案：深解改为 z≈2.974、p≈0.0029，示例数字由同式脚本生成。

### MS-N60 A 组转化数为 0 被误判“分母不能为0”而拒绝计算（高，确认缺陷）
- 问题：输入守卫把 `conversionsA` 硬编码进分母集合，值为 0 时整页报错；但 0 转化是合法观测，z 检验仍可计算，真正无定义的只有“相对提升”。
- 证据：`tools/marketing/marketing-ab-test-significance.html:257`（`__D={"conversionsA":"conversionsA"}`）、`:263-266`（值为0即返回“是本计算的分母”）、`:302-307`（p 值与 lift 公式）
- 复现：A 组访客1000/转化0、B 组访客1000/转化20 → 页面报“「A组转化数」是本计算的分母，不能为0”，不出 p 值；期望照算：pPool=0.01、se≈0.004449、z≈4.49、p≈7e-6，仅相对提升显示“不适用（基线为0）”。
- 影响：`tools/marketing/marketing-ab-test-significance.html`；冷启动/新素材常见的 0 转化组合被整页阻断，错误文案还把转化数说成分母。
- 方案：移除该零值守卫；`pA===0` 时 lift 显示“不适用”，p 值与显著性照常输出。

### MS-N61 价格弹性页深解用端点百分比，页面公式与代码是中点法（高，确认缺陷）
- 问题：公式框与 `calc()` 明确用弧弹性/中点法，深解算例却按 `ΔQ/q1 ÷ ΔP/p1` 的端点法写 -2.0。
- 证据：`tools/marketing/price-elasticity.html:163`（“弧弹性/中点法 PED=(ΔQ÷平均Q)÷(ΔP÷平均P)”）、`:262-264`（代码同式）、`:206`（深解 200→180、500→600 → -2.0）
- 复现：p1=200→p2=180、q1=500→q2=600：中点法 `(100/550)/(-20/190)=-1.727`，页面结果区为 -1.727；深解写 -2.0（端点法）。期望深解改为 -1.727 或全页统一端点法。
- 影响：`tools/marketing/price-elasticity.html` 深解与结果区；同一页两套口径，手算核对差 13.6%。
- 方案：深解改用中点法并写 -1.73；补一句“端点法与中点法的差异”，避免用户拿 -2.0 反推。

### MS-N62 价格未变化时弹性变成 Infinity/NaN，仍输出“富有弹性”或“单位弹性”及策略建议（高，确认缺陷）
- 问题：`dP=0` 时 `(dQ/avgQ)/(dP/avgP)` 得到 ±Infinity；若销量也未变则为 NaN。等级判断未拦截非有限值，Infinity 落入“富有弹性”，NaN 落入 else“单位弹性”。
- 证据：`tools/marketing/price-elasticity.html:259`（只校验四项>0）、`:263-265`（dP 作除数）、`:268-276`（>1/<1/else 三支）
- 复现：p1=p2=100、q1=1000→q2=2000 → 弹性值显示“—”，等级仍“富有弹性”，提示“降价可增加总收入”；p1=p2 且 q1=q2 → 0/0=NaN，显示“单位弹性/总收入基本不变”。期望显示“无法计算（价格未变化）”，不输出等级与建议。
- 影响：`tools/marketing/price-elasticity.html` 结果卡与建议区；价格未变的真实场景被赋予虚构弹性与定价建议。
- 方案：`if(dP===0)` 提前返回错误并清空等级/建议/图表；`!isFinite(ped)` 一律按不可计算处理。

### MS-N63 标语生成器没有产品/卖点/情感调性输入，深解算例不可复现（高，确认缺陷）
- 问题：页面只有主题、品牌名、数量三个输入；生成逻辑是 8 条固定模板替换 `[B]`。深解却称可按“运动手表/记录心跳”“极简笔记 App”和热血/温暖/极简调性生成。
- 证据：`tools/marketing/tagline-generator.html:169-177`（输入仅 theme/brand/count）、`:272-286`（`templates` + `replace(/\[B\]/g,brand)`）、深解 `:213`（情感调性）、`:216-217`（运动手表/极简 App 示例）
- 复现：选“科技”+品牌“运动手表”→ 只会输出“让 运动手表 连接未来”等 8 条模板句；无法输入“记录心跳”，也得不到“记录每一次心跳”“为奔跑而生”；页面无调性选项。期望提供 product/feature/tone 字段或删除深解承诺。
- 影响：`tools/marketing/tagline-generator.html`；宣称按产品定位与调性生成，实际只做品牌名替换，输出与产品特性无关。
- 方案：增加产品/卖点/调性输入与对应模板库；否则把文案与深解改为“品牌名替换式标语模板”。
- 假工具候选：是（类型 C）

### MS-N64 话题标签生成器给中文关键词加英文复数/词缀，输出非词标签（高，确认缺陷）
- 问题：变体1无条件拼 `s`，变体2拼英文后缀；中文关键词因此出现“#健身减脂s”“#健身减脂Vibes”。变体2的首字母与词干还来自两次独立随机选取，可能拼出“Vife”这类非词。
- 证据：`tools/marketing/hashtag-generator.html:274`（`tags.add('#'+base+'s')`）、`:279`（`suffixes[randInt(...)].charAt(0)... + suffixes[randInt(...)].slice(1)`）、`:268-280`（按关键词循环）
- 复现：输入“健身减脂”、变体数≥3 → 输出“#健身减脂”“#健身减脂s”“#健身减脂Life/Vibes”；输入“shoes” → “#shoess”；`:279` 在大小写模式下可能得到“#健身减脂Vife”。期望中文只用中文后缀（分享/推荐/攻略），英文按 s/es/去y 规则，且首字母与词干取同一后缀。
- 影响：`tools/marketing/hashtag-generator.html` 输出区与复制结果；中文用户拿到的标签基本无搜索量，英文用户会得到错误拼写。
- 方案：按语种分支；改 `const s=pick(suffixes); base+(lower?s:s[0].toUpperCase()+s.slice(1))`；中文提供中文后缀池。

### MS-N65 深解宣称“主题词→长尾/人群/场景扩展”，实际只做机械拼接（高，确认缺陷）
- 问题：深解称输入“健身减脂”会得到 #减脂餐 #居家健身 #新手健身 #运动打卡 #刷脂训练、输入“穿搭”会得到 #小个子女生穿搭 #平价穿搭；代码只生成“关键词+s/英文后缀/年份/另一关键词”，没有近义词、人群或场景词库。
- 证据：`tools/marketing/hashtag-generator.html:205`（“按主题词扩展出长尾标签组合”）、`:208-209`（深解示例）、`:269-289`（base/plural/suffix/year/组合词）
- 复现：输入“健身减脂”、变体3 → 实际集合仅 `#健身减脂`、`#健身减脂s`、`#健身减脂Xxx`（随机英文后缀），深解所列 5 个标签一个都不出现；“穿搭”也不会出现“#小个子女生穿搭”“#平价穿搭”。期望实现语义词库或删除“长尾扩展”承诺。
- 影响：`tools/marketing/hashtag-generator.html` 的定位与深解；用户按示例操作得不到承诺结果。
- 方案：补中文品类/人群/场景词库并按相关性组合排序；否则把功能改称“关键词变体生成”，同步改写深解。
- 假工具候选：是（类型 C）

### MS-N66 口号生成器无品牌/产品/调性输入，输出是固定 50 条随机抽选（高，确认缺陷）
- 问题：页面只有“场景+数量”，五个场景各 10 条硬编码句子，随机抽取后加感叹号；深解却称可输入“咖啡/年轻/提神”“财税软件/专业/可信”生成对应口号。
- 证据：`tools/marketing/slogan-generator.html:165-177`（仅 scene/count）、`:258-264`（5×10 固定 `SLOGANS`）、`:267-279`（`pick(list)` 随机抽取）、深解 `:211-212`
- 复现：选“促销”只能得到“限时优惠，错过即无！”等固定句；无品牌/产品/关键词输入，无法生成深解中的“每一口，醒来的理由”“让每一笔账都经得起查”。期望提供品牌/产品/调性输入并生成相关内容。
- 影响：`tools/marketing/slogan-generator.html`；用户以为是个性化生成，实际只是固定句随机洗牌，深解案例全部不可复现。
- 方案：增加品牌/产品/核心卖点/调性字段与组合模板；否则删除“生成器”承诺，改为“口号示例库/随机挑选”。
- 假工具候选：是（类型 A）

### MS-N67 图片尺寸深解给出的微博/朋友圈尺寸与页内数据表冲突（高，确认缺陷）
- 问题：深解写“微博配图 1400×700、朋友圈 1200×900”，数据表分别只有 1080×1080；深解还写小红书 1080×1350，数据表无该条（1080×1350 属于 Instagram）。
- 证据：`tools/marketing/social-media-image-sizes.html:250`（微博 1400×700、朋友圈 1200×900）、`:251`（小红书 1080×1350）、`:306`（朋友圈图片 1080×1080）、`:321`（微博配图 1080×1080）、`:347-351`（小红书仅 1080×1440 等）、`:398`（Instagram 1080×1350）
- 复现：阅读深解后按“微博配图 1400×700”做图；在页面选平台“微博”，列表只显示 1080×1080，没有任何 1400×700 条目。期望深解与数据表同源。
- 影响：`tools/marketing/social-media-image-sizes.html`；速查页最核心的尺寸可信度被破坏，用户会按错误像素导出。
- 方案：深解改为引用 `platformData` 的条目；增加构建期脚本比对深解尺寸与数据表，禁止手写第二套数字。

### MS-N68 搜索“微博”页面有结果，导出 CSV 为空（中，确认缺陷）
- 问题：渲染过滤包含平台名 `p.name`，导出过滤只查 `s.name/s.type`，两个筛选口径不一致。
- 证据：`tools/marketing/social-media-image-sizes.html:492`（`matchSearch` 含 `p.name`）、`:540`（导出 `matchSearch` 不含 `p.name`）
- 复现：搜索框输入“微博” → 页面显示 6 条微博尺寸；点“导出尺寸表” → CSV 只有表头，0 行。期望导出当前筛选的 6 行。
- 影响：`tools/marketing/social-media-image-sizes.html` 导出文件；用户按平台名搜索后导出会得到空表。
- 方案：抽出统一 `filterSizes()` 供渲染与导出复用；或在导出侧补 `p.name.includes(search)`。

### MS-N69 中文话题生成器宣称“品类→人群→场景”长尾，实际只拼“关键词+分享/推荐”+固定通用词（高，确认缺陷）
- 问题：宣称的语义扩展未实现；输出固定为关键词、关键词+分享、关键词+推荐，再叠加 15 个通用词（含平价、学生党、yyds、绝绝子）与平台/季节词，与品类和人群无关。
- 证据：`tools/marketing/marketing-chinese-hashtag-generator.html:190`（“按品类词扩展出成分党、人群、场景等长尾标签”）、`:193`（深解 #平价护肤 #敏感肌护肤 #成分党 #学生党护肤）、`:249`（27 个固定 `commonTags`）、`:258-269`（仅做字符串拼接与前缀截取）
- 复现：输入“国货护肤” → 实际得到 `#国货护肤 #国货护肤分享 #国货护肤推荐 #好物分享…#平价 #学生党…#yyds #绝绝子` 等；深解所列 `#平价护肤 #敏感肌护肤 #成分党 #学生党护肤` 全部缺失。输入“早C晚A”也不会出现 `#护肤流程 #抗初老 #熬夜党护肤`。期望实现语义词库或删除该承诺。
- 影响：`tools/marketing/marketing-chinese-hashtag-generator.html`；用户按深解预期操作得到大量无关通用标签，宣称的长尾覆盖不成立。
- 方案：建立“品类/成分/人群/场景”词库并按关键词组合；否则把文案改为“关键词+通用标签模板”，删除深解示例。
- 假工具候选：是（类型 A）

### MS-N70 广告 ROI 同页两套公式，默认参数得 80% vs 200%（高，确认缺陷）
- 问题：公式框与代码按“（收入−广告费−商品成本）/广告费”计算；参考表却写“（收入−广告费）/广告费”，把 ROI 等同于 ROAS−1。
- 证据：`tools/marketing/calc-1.html:125`（含商品成本）、`:157`（参考表不含商品成本）、`:229-233`（`cogs=revenue*costRate`、`profit=revenue-spend-cogs`、`roi=profit/spend`）
- 复现：花费10000、收入30000、成本率40% → 计算器 ROI=8000/10000=80%；按参考表公式 `(30000-10000)/10000=200%`。同一组输入相差 2.5 倍。期望统一为 80%，参考表改为含商品成本，或把该项改名为“ROAS−1（不含货成本）”。
- 影响：`tools/marketing/calc-1.html` 参考表与结果区；对外复盘/跨工具比较时 ROI 口径打架，80% 与 200% 会被当成两个投放效果。
- 方案：改参考表公式为 `(收入−广告费−商品成本)/广告费`；并在表中注明“不含运营/人力等费用”。

### MS-N71 “ROAS>1 表示广告未亏损”忽略商品成本，1.5 仍会亏损（高，确认缺陷）
- 问题：ROAS 只比较收入与广告费，未扣商品成本；在成本率 70% 时盈亏平衡 ROAS 应为 1/(1−0.7)=3.33，页面却称 ROAS>1 即未亏损。
- 证据：`tools/marketing/calc-1.html:178`（“通常 ROAS > 1 表示广告未亏损”）、`:229-233`（利润已扣 `cogs`）、`:237-239`（ROI/ROAS 展示）
- 复现：花费10000、收入15000、成本率70% → ROAS=1.5，页面判“未亏损”；实际商品成本10500、净利润−5500、ROI=−55%。期望提示“ROAS 1.5 < 盈亏平衡 3.33，实际亏损”。
- 影响：`tools/marketing/calc-1.html` 注意事项与结果解读；高货成本品类（美妆/服饰）会据此继续投放亏损计划。
- 方案：按 `1/(1-costRate)` 计算盈亏平衡 ROAS 并比较，文案改为“ROAS 超过盈亏平衡值才未亏损”。

### MS-N72 广告花费为 0 时仍输出 ROI 0%、ROAS 0，但净利润为正（中，确认缺陷）
- 问题：`spend>0 ? 计算 : 0` 把不可计算的回报率写成 0，且利润仍按收入−商品成本计算。
- 证据：`tools/marketing/calc-1.html:232-233`（`roas = spend>0 ? ... : 0`、`roi = spend>0 ? ... : 0`）、`:231`（`profit` 不受 spend 影响）
- 复现：花费0、收入30000、成本率40% → 页面 ROI 0.00%、ROAS 0.00，同时显示净利润 18000 元、利润率 60%。期望提示“广告花费须大于0”或显示“不可计算”。
- 影响：`tools/marketing/calc-1.html` 结果区；零广告费场景下“利润为正但 ROI 为 0%”自相矛盾。
- 方案：`spend<=0` 时报错并停止计算；不要用 0 兜底。

### MS-N73 目标人数/预算为 0 被 `||1` 兜底，评分可到 -790.8 或 100“卓越”（高，确认缺陷）
- 问题：`targetPax`、`budget` 用 `+value||1`，0 被静默替换为 1，到场率/预算执行率放大数万倍；评分只 `Math.min(100,score)` 不设下限。
- 证据：`tools/marketing/assessor-65.html:216-217`（`tp=...+targetPax||1`、`bg=...+budget||1`）、`:221-225`（比率与加权、`Math.min(100,score)`）
- 复现：预算0、支出45万、目标500/实际450、满意度8.5、达成85% → budgetRate=4500%，score=22.5+(100−4400)×0.2+25.5+21.25=−790.75，页面显示“-790.8/100”。目标0、实际450 → attendanceRate=45000%，score=11314.75 被截成100 → 评级“卓越”。期望两项为0时提示“不能为0”并停止计算。
- 影响：`tools/marketing/assessor-65.html` 评分与等级；空值/漏填会得到极端负分或虚假“卓越”。
- 方案：校验 `targetPax>0`、`budget>0`；`score=Math.max(0,Math.min(100,score))`；预算执行率异常时提示而非直接入分。

### MS-N74 FAQ 称四维权重“可调”，实际权重硬编码（高，确认缺陷）
- 问题：FAQ 明确写“可调高达成率权重，调整后重算即可”，页面没有任何权重输入，`calc()` 用固定 0.25/0.2/0.3/0.25。
- 证据：`tools/marketing/assessor-65.html:170`（FAQ 可调权重）、`:223`（`attendanceRate*0.25+(100-...)*0.2+sf*10*0.3+ar*0.25`）
- 复现：页面找不到权重字段；按 FAQ 想调高达成率权重只能改源码。期望提供4个权重输入（校验合计100%）或删除 FAQ 承诺。
- 影响：`tools/marketing/assessor-65.html` FAQ 与用户操作；承诺的定制能力不存在。
- 方案：增加四项权重输入并归一化/校验；或改写 FAQ 为“当前固定权重，暂不支持调整”。

### MS-N75 参考表写中点法，计算器却用端点百分比，示例 -1.50 实为 -1.703（高，确认缺陷）
- 问题：同一页参考表列“弧弹性中点法”，但 `calc()` 用 `(newQ-oldQ)/oldQ ÷ (newP-oldP)/oldP`；示例从 100→110、1000→850 写 -1.50，按中点法应为 -1.703。
- 证据：`tools/marketing/marketing-price-elasticity.html:313`（中点法公式）、`:399-401`（端点百分比）、`:239`（端点示例 -2）、`:348`（深解 -1.5）
- 复现：原价100→110、原销量1000→850 → 页面 E=−15%/10%=−1.50；按同页中点法 `(150/1850)/(10/210)=−1.703`。期望结果 -1.703 或全页统一端点法。
- 影响：`tools/marketing/marketing-price-elasticity.html` 公式表/深解/结果区；三套口径并存，弹性 1.5 与 1.7 会影响“富有弹性”的表述强度。
- 方案：`calc()` 改用中点法（与 `price-elasticity.html` 一致），同步改 `:239`、`:348` 示例为 -1.73/-1.70。

### MS-N76 价格未变时把弹性置 0 并判“完全无弹性”，策略建议与收入卡片自相矛盾（高，确认缺陷）
- 问题：`priceChangePct===0` 时直接令 `elasticity=0`，随后按 `|E|<0.1` 判“完全无弹性”；策略分支又按 `priceChangePct>0` 判断，0 落入“降价策略无效”。
- 证据：`tools/marketing/marketing-price-elasticity.html:401`（`priceChangePct !== 0 ? ... : 0`）、`:410`（`absElasticity<0.1` → “完全无弹性”）、`:418-419`（`priceChangePct>0 ? 提价有效 : 降价无效`）
- 复现：原价=新价=100、原销量1000→新销量2000 → 弹性0.00、“完全无弹性”，收入变化 +100%，策略却输出“降价策略无效，收入减少”。期望价格未变时显示“无法计算（价格未变化）”，不输出弹性类型与策略。
- 影响：`tools/marketing/marketing-price-elasticity.html` 结果卡与策略区；价格未变的促销/换量场景会得到错误的“无弹性”结论和反向建议。
- 方案：`if(priceChangePct===0)` 提前报错；类型阈值改为“0<|E|<0.1 近零弹性”，不要用 0 冒充完全无弹性。

### MS-N77 互动率分子漏掉收藏，参考表与深解却按含收藏计算，5% 算例不可复现（高，确认缺陷）
- 问题：公式框与 `calc()` 只汇总点赞+评论+分享，页面也没有收藏输入；参考表和深解却写“点赞+评论+转发+收藏”，示例把收藏 60 计入总数 500。
- 证据：`tools/marketing/marketing-engagement-rate.html:149`（`(点赞+评论+分享)`）、`:177`（`(点赞+评论+转发+收藏)`）、`:212`（300+120+60+20=500 → 5%）、`:153-155`（仅 likes/comments/shares 输入）、`:240`（`totalEng=likes+comments+shares`）
- 复现：粉丝10000、赞300、评120、转20（页面可填全部）→ 页面 ER=(300+120+20)/10000=4.40%；深解同场景写 500/10000=5%，但页面无处输入收藏60。期望增加收藏字段并计入，或统一为不含收藏并把示例改成 4.4%。
- 影响：`tools/marketing/marketing-engagement-rate.html` 结果区与深解；“含收藏”的行业口径无法复现，用户按示例填数会少算 12% 互动量。
- 方案：增加 saves 输入并令 `totalEng=saves+likes+comments+shares`；同步公式框、参考表与深解。

### MS-N78 互动数允许负数，输出负互动率（中，确认缺陷）
- 问题：点赞/评论/分享仅做 `||0`，负值被保留，总互动数可为负，互动率随之为负。
- 证据：`tools/marketing/marketing-engagement-rate.html:235-240`（`parseFloat(...)||0` 保留负数并直接求和）、`:245`（`totalEng/followers*100`）
- 复现：粉丝10000、点赞−100、评论0、分享0 → 总互动−100，页面 ER=−1.00%；期望提示互动数不能为负或按0处理。
- 影响：`tools/marketing/marketing-engagement-rate.html` 结果区；负互动率不可能存在，会直接误导复盘。
- 方案：校验 `likes/comments/shares >= 0`，越界报错并清空结果。

## 2026-11-06 静态续审：营销工具第 418–423 页

- **历史结论状态更新**：MS-M5 所述负比例现已由 `marketing-ad-budget-allocator.html:254-257` 拒绝，非 100% 合计也在 `:259-262` 明示归一化；仍需运行回归，MS-M6 的手动比例而非智能分配逻辑仍在。MS-J3 所述回收期不展示已过时：`marketing-cac-calculator.html:463-465` 已展示回收期并声明 36 个月假设。MS-N38 的表格/图表/CSV 零分母不一致仍在，MS-N60 的 A 组零转化守卫仍在；MS-F7 目标利润率不可达时无说明仍在。
- **中文话题输入进入 HTML 和内联脚本，存在注入及复制损坏风险**：`marketing-chinese-hashtag-generator.html:241-243,258-276` 将关键词和行业直接拼入 `innerHTML` 的标签文本、单标签 `onclick` 字符串和全部复制按钮模板字面量，无 HTML 或 JS 上下文转义。含单引号、反引号或 HTML 标记的用户输入可破坏对应结构；潜在脚本注入仅由源码推断，未执行攻击或验证可利用性。建议用文本节点渲染并通过事件监听器绑定复制值。
- **零预算和零获客成本的除数未定义**：`marketing-ad-budget-allocator.html:250-267,272,281` 允许预算为 0，收入也为 0，整体 ROAS 的 `0/0` 最终被替换为 `—`；`marketing-cac-calculator.html:409-428,455-465,489-505` 允许营销和销售费用同时为 0，LTV 存在时比率及 ROI 除以零、替换为 `—` 却仍显示“健康”，LTV 留空时费用占比也是 `0/0`。应保留零成本的 CAC，明确相关比率不可计算并避免给出健康结论。
- **CAC 保存校验与计算不一致**：`marketing-cac-calculator.html:413-420,508-525` 的计算会拒绝负费用和非正 LTV，但保存仅检查数值及客户数；因此无效费用或 LTV 仍可存历史，历史列表还会根据无效 CAC 分级。应共用校验逻辑。
- **A/B 转化数缺少有效区间校验**：`marketing-ab-test-significance.html:293-314` 仅限制访客数为正，未拒绝负转化或转化数超过访客数；例如两组各 100 访客、150 转化时合并比例为 1.5、标准误为 NaN，结果替换成 `—` 仍给出“不显著”结论。应限制转化数介于 0 与访客数之间，并对标准误为零单独处理。
- 本批共阅读 `funnel-calculator`、`marketing-ab-test-significance`、`marketing-ad-budget-allocator`、`marketing-break-even-roas`、`marketing-cac-calculator`、`marketing-chinese-hashtag-generator` 6 页；仅源码分析，未运行页面、注入或浏览器，未计入双跑。

## 2026-11-06 静态续审：营销工具第 424–429 页

- **历史结论状态更新**：MS-J4（期末超过期初加新增）、MS-J5（转化超过访问）、MS-J7（折后价或优惠超原价）、MS-M1（零折及越界）、MS-N3（点击超过展示）和 MS-J2（新增客户超过点击及毛利率越界）原述计算路径已分别加入校验；`marketing-coupon-discount.html:380-398` 区分空值与零值并由计算和保存共用校验。上述结论仅按源码更新，未做运行回归；优惠券按订单减一次仍是现行计算，公式框须另对照。
- **保存历史绕过计算校验**：`marketing-churn-rate.html:393-401,475-487`、`marketing-conversion-rate-calculator.html:398-405,491-502`、`marketing-cpa-calculator.html:429-439,567-580`、`marketing-cpm-calculator.html:402-405,490-500`、`marketing-discount-rate.html:436-465,531-554` 的保存路径均缺少部分计算约束。例如期初 100、期末 150、新增 0 在流失页显示口径错误，但历史仍可存流失率 -50%；折后价高于原价也可存负折扣。应让保存与计算共用同一校验。
- **折扣页清空数值被当成 0**：`marketing-discount-rate.html:429-431,442-444,455-457` 对折扣率、折后价、优惠额使用 `parseFloat(...) || 0`；清空折后价会直接得到 0 元和 100% 优惠，清空折扣率则得到无折扣结果。应区分空串与合法 0，在缺失时停止结果和历史保存。
- **零转化历史 CPA 与当前结果不一致**：`marketing-conversion-rate-calculator.html:407-411,426-430,533-545` 对零转化显示 CPA 不可计算，但历史列表仍将花费除以零并把 `Infinity` 替换为 `—`，未附不可计算原因；且花费大于 0、收入为 0 时 ROI 卡被隐藏，不能呈现零收入对应的亏损。应区分输入缺失与真实零收入并统一结果与历史口径。
- **零花费边界处理有缺口**：`marketing-cpm-calculator.html:398-400` 把 0 花费当无效，尽管展示量非零时 CPM 为 0；`marketing-cpa-calculator.html:449-450,464-485` 对 0 花费强制 ROI 为 0，并在客单和毛利均正时显示 `+0.0%`，而该 ROI 的分母为 0。应分别保留可算的零成本与标注不可计算的比率。
- 本批共阅读 `marketing-churn-rate`、`marketing-conversion-rate-calculator`、`marketing-coupon-discount`、`marketing-cpa-calculator`、`marketing-cpm-calculator`、`marketing-discount-rate` 6 页；仅源码分析，未运行浏览器，不计双跑。

## 2026-11-06 静态续审：营销工具第 430–435 页

- **历史结论状态更新**：MS-N78 所述互动数负值现由 `marketing-engagement-rate.html:245-247` 拦截；MS-M3 的包邮毛利率缺失及越界现由 `marketing-free-shipping-threshold.html:244-255` 拦截；MS-F8 的 LTV 零值路径现被拒绝，回本周期已标明按 36 个月分摊（`marketing-ltv-cac-ratio.html:422-424,456`）。仅按源码确认，未做运行回归。Google 广告负数输入、达人报价参数缺校验、关键词混排口径的既有关键路径仍在。
- **关键词正文只有标点时仍给密度结论**：`marketing-keyword-density.html:243-260` 仅判断内容非空，标点正文经清洗后 `totalWords=0`；例如正文 `!!!`、关键词 `a`，密度为 `0/0`，展示时替换成 `—`，但比较 NaN 均不成立，最终建议“密度过高”。应在分母为零时说明缺少可统计内容，不输出评价。
- **互动数清空被当作零**：`marketing-engagement-rate.html:233-249` 的点赞、评论、分享通过 `parseFloat(...) || 0` 处理；清空这三个字段仍按零生成总互动及互动率。展示量标为可选，其他字段若为必填应区分空串与合法 0，避免缺失数据被解释为零互动。
- **目标日点击为 0 时 ROAS 无定义**：`marketing-google-ads-budget.html:244-263` 允许日点击为 0，日预算与收入均为 0，`0/0` 被替换为 `—x` 而没有说明。应保留零预算及零收入，并明确 ROAS 不可计算；负值和转化率越界的既有问题见历史记录。
- 本批共阅读 `marketing-engagement-rate`、`marketing-free-shipping-threshold`、`marketing-google-ads-budget`、`marketing-influencer-pricing`、`marketing-keyword-density`、`marketing-ltv-cac-ratio` 6 页；仅源码分析，未运行浏览器，不计双跑。

## T 批收口

- 本轮审计 13 页：`market-share`、`estimate-sample-size-confidence`、`marketing-ab-test-significance`、`price-elasticity`、`tagline-generator`、`hashtag-generator`、`slogan-generator`、`social-media-image-sizes`、`marketing-chinese-hashtag-generator`、`calc-1`、`assessor-65`、`marketing-price-elasticity`、`marketing-engagement-rate`（均在 `tools/marketing/`）。
- 新增 24 条（高 20 / 中 4）：MS-N55～MS-N78；假工具候选 4 页（`tagline-generator` C、`hashtag-generator` C、`slogan-generator` A、`marketing-chinese-hashtag-generator` A）。
- 数值均由 `node -e` 按源码同式复算：样本量 271/664、A/B z=2.9737/p=0.00294、中点弹性 -1.727/-1.703、ROAS 盈亏平衡 1.667、评估分 -790.75、互动率 4.4%、HHI 5800/970。
- 未做浏览器、门禁、线上与英文态验证；仅静态阅读 + node 复算。

