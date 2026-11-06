# 金融计算 · tools/finance（115 页，第二大分类）

## 2026-11-06 交互复核：NPV 内部收益率多根漏判（高，确认）

- 基线 `0781ef7e61`；独立 Chrome 在 `tools/finance/npv-calculator.html` 输入初始投资 100、两期现金流 230 和 -132、折现率 8%，结果显示“IRR 无解”，明细称“NPV 无零点，不可行”。
- 实际 `-100+230/(1+r)-132/(1+r)^2=0` 在 r=10%、20% 均有解，代入残差分别约 -1.42e-14、1.42e-14。第 402–429 行将 -0.9999 至 1000 均匀分成 4000 段，两个根落于同一网格区间、端点同号，凭变号扫描无法识别；偶数重根也可能遗漏。应采用可靠的多根及重根识别方法，未命中不等于无解。
- 此项是当前基线独立验证的新漏判，不沿用本文件早期可能已修复的 F-N29 旧复现作为现状。

## 已知问题
### F1. 贷款/利率系「名义 vs 实际」口径页散
- ✅ 导航已落地（2026-10-26）：compound-interest / simple-interest / installment-real-rate / credit-card-interest 四页 result 后加「🧭 利率口径导航」双语卡（__rateNav 五口径互链含 mortgage-calculator，TBKit EN 守卫回退中文；容器置 result 之后防跨元素值序列锚断裂）。
- 🔴 「同输入多口径并排」未做（计算器组，量级大待裁）。

### F2. invoice-generator 四分支文案为模板腔
- ✅ 已重做（核实 2026-10-26）：页面现为「价税分离与多单金额分摊计算器」，含发票式价税分离四行 + 人民币大写（票据口径）——条目过时删除。

### F3. currency-converter 汇率为静态示例
- ✅ 核实已实现（2026-10-26 复查源文件）：口径声明已置顶、rateMode 手动贴入汇率已上线、renderPairTable 常用货币对速查（对 CNY 双向 10 币种）已在——条目过时删除。

## 功能缺陷
- 个税计算器已含全档累进曲线；缺「年终奖单独/合并计税二选一对比」（刚需高频）。
- ~~提前还款页缺「部分提前/缩期 vs 减月供」对比矩阵~~ ✅ 核实已实现（2026-10-26 复查 mortgage-prepayment 源文件：模式1缩期/模式2减月供完整对比表 + 口径修正含 prepay + 结论行，此前批次已做）——条目过时删除。

## 优化点（G06 联动，金融是 S2/S3 最高 ROI 分类）
- S2 场景预设：「一线首套商贷 300 万 25 年」「二套 4.9% 上浮」「等额本息 vs 本金并排」。
- S3 分步：每月月供拆解（本金/利息/剩余）逐年表+堆叠图。
- S4 分享卡：个税/贷款结果最常被转发。
- F1+D11 打通：本分类做「计算器组」（输入一次，联动房贷/个税/提前还款）。

## 受影响范围
- tools/finance/（115 页）

## 进度
- 🟢 批次 2026-10-26 · S2 场景预设：`finance/loan-amortization` preset 栏加 3 枚场景（一线首套 300 万/25 年/3.9% 等额本息、二套 200 万/30 年/5.2% 等额本金、提前还款 50 万@24 期）。verify finance 239/239、判别器 0 逃生、门禁 218/218。
- 🟢 批次 2026-10-26 · F1 利率口径导航：四利率页 __rateNav 双语互链卡。⚠ tax-calculator「年终奖单独/合并对比」核实已实现（L359/L465），缺陷条目过时。
- 🟢 批次 2026-10-26 · S3 逐年拆解汇总表：`finance/loan-amortization` 加 #yearlyTable（scheduleData 按 12 期聚合：年还款/其中本金/其中利息/年末剩余本金，renderSchedule 末联动、提前还款重算同步；EN 双语表头）；verify 强用例（12万/6%/2年 → 第1年 63,821.68/58,205.02/5,616.66/61,794.98 + 第2年清零，行间自洽）。verify finance 240/240、判别器 0 逃生、门禁 218/218。
- 🔴 待开发：S4 分享卡；同输入多口径并排待裁。

## 2026-11-03 审计补充

### F-N1 贷款方案无效输入仍参与最低月供比较（高，确认缺陷）
- 问题：贷款额或月数为零、空值时返回零月供，仍参与最低月供排名，可能把无效方案推荐为「月供最少」。
- 证据：`tools/finance/loan-comparison.html:134-145,248-280`：数字输入无最小值约束；`pmt` 对 `p <= 0 || months <= 0` 返回 0；`calc` 未过滤无效方案直接按月供取最小值。此为源码确定路径，尚未真机点击。
- 影响：`tools/finance/loan-comparison.html`；复制结论也可能带走误导性推荐（`:283-285`）。
- 方案：对本金、利率及期数明确验证，标出无效方案并将其排除比较；全部无效时不显示推荐。增加空值、零月数、负利率等用例。

### 留存优化：贷款比较显示可比性与总成本（中，建议）
- 证据：`tools/finance/loan-comparison.html:134-151,266-278` 支持三个不同本金和期数并排、CSV 和复制，但排名仅按月供。
- 影响：同页；方案：提示不同本金或期限的方案不可仅凭月供判优，给出总利息差、实际总还款及同本金/同期条件下比较入口；如补收费项应标明口径。

### 留存优化：车贷费用与展示期间对齐（低，建议）
- 证据：`tools/finance/car-loan-calculator.html:285-336,539-553` 支持保险年数，但结果标题固定称首年保险，代码按选定年数相乘。
- 影响：`tools/finance/car-loan-calculator.html`；方案：按实际选中年数动态显示保险与车船税期间，并提供贷款期限内现金流合计和费用假设说明。

### 覆盖
- 本次人工查 `tools/finance/loan-comparison.html`、`tools/finance/car-loan-calculator.html` 2 页；其余金融页未逐页复扫；历史已修声明未独立复验。

## 2026-11-03 续查：现金流、债券与退休规划

### F-N2 IRR 稀疏现金流忽略实际期号（高，确认源码缺陷）
- 证据：`tools/finance/irr-calculator.html:344-349,419-432,455-458` 保险预设期号 T0、T1、T2、T10，计算时仅传排序后的金额数组，NPV 以数组下标作指数，T10 被当作 T3。折现率 8% 时显示 NPV 约 +19603 元，按实际 T10 约 -46525 元。
- 影响：`tools/finance/irr-calculator.html`；保险等跨期项目的收益和投资判断可能方向错误，删除中间期也有相同风险。
- 方案：按真实 period 折现或补零，验证稀疏期与删除中间期；输出逐期折现明细便于核对。

### F-N3 IRR 对贷款现金流求解方向错误（高，确认源码缺陷）
- 证据：`tools/finance/irr-calculator.html:350-364,445-450,463-489` 固定按 NPV 随利率递减的方向二分。贷款预设 T0 收 100000、12 期各还 8884 的现金流方向相反，收敛至上限 1000%；两端异号，因此无根警告不触发。数值求解对照每期约 0.9984%，若按月则有效年化约 12.66%。
- 影响：`tools/finance/irr-calculator.html`；贷款成本严重失真；期数单位还需明确。
- 方案：按端点符号维护区间并验证残差，无根或多根明确提示；标明每期及年化口径，贷款示例设置期数单位。

### F-N4 债券负收益率被截断、零息显示票息（高，确认源码缺陷）
- 证据：`tools/finance/bond-yield-calculator.html:544-568,600-618` 附息债到期收益率仅搜索 0–100%；面值 100、票息 5%、价格 110、1 年且年付的结果趋近 0%，正确为 -4.545%；零息分支仍计算并显示 `annualCoupon`、`totalCoupon`。
- 影响：`tools/finance/bond-yield-calculator.html`；负收益和零息现金流展示错误。
- 方案：支持可行负利率并检查求解区间和定价残差；零息模式统一清零票息，输出价格、现金流和收益率对照。

### F-N5 定投资金加权年化使用错误现金流（高，确认源码缺陷）
- 证据：`tools/finance/dca-calculator.html:376-408,431-454,510-533` 正算将初始本金在期初投入，反算却把全部投入均摊到每月；初始 12000、每月 1000、1 年、期初、年化 12% 时，页面反算约 17.02%，真实现金流的月利率 1%，对应名义年化 12%、有效年化约 12.68%。
- 影响：`tools/finance/dca-calculator.html`；有初始本金时资金加权业绩虚高。
- 方案：按实际发生时点构造现金流并求 IRR，区分名义与有效年化；展示每期投入明细并与一次性投资口径对照。

### F-N6 定投亏损丢负号、目标反推返回边界伪解（高，确认源码缺陷）
- 证据：`tools/finance/dca-calculator.html:437-453,459-507` 亏损时 `profitSign` 为空且金额取绝对值；初始 0、月投 1000、1 年、年化 -12%、期初时真实约亏 752.10 元，却显示正金额。目标 100 万时搜索上限固定 500%，未验证区间即输出该边界。
- 影响：`tools/finance/dca-calculator.html`；亏损可能误读为盈利，目标反推结果不可信。
- 方案：金额保留负号，反推核验边界与目标残差；超范围明确提示，提供目标/可达金额差距。

### F-N7 退休零收益年度支取无效及旧 CSV（高，确认源码缺陷）
- 证据：`tools/finance/retirement-calculator.html:372-385,395-415,448-495,656-665` 年化 0 时摘要采用零利率分支，年度明细却除以 `r=0` 得 NaN；年龄校验失败未清空旧 `yearlyData`，导出仍使用旧数组。
- 影响：`tools/finance/retirement-calculator.html`；摘要与明细矛盾，无效输入仍可导出旧方案；与 G10 的旧结果问题同类。
- 方案：统一资产及支取函数，处理零利率极限及有效负利率；失败清空/禁用旧导出，显示年度假设与现金流。

### F-N8 现金流及投入时点历史不能可靠恢复（中，确认源码路径）
- 证据：`tools/finance/irr-calculator.html:407-413,632-651,658-682,724-726` 现金流控件无 id，通用历史快照未保存各期金额；`tools/finance/dca-calculator.html:173-175,365-369,706-716,744-755` 投入时点存在变量 `timing`，未纳入输入快照。
- 影响：`tools/finance/irr-calculator.html`、`tools/finance/dca-calculator.html`；恢复历史后可能使用当前现金流或当前期初/期末模式，无法重现原结果，浏览器回填待测。
- 方案：完整持久化期号、金额、时点与输入参数，恢复后重算；分别导出真实现金流和历史对比，不将历史表称现金流明细。

### 续查覆盖
- 新抽查 `tools/finance/irr-calculator.html`、`tools/finance/bond-yield-calculator.html`、`tools/finance/dca-calculator.html`、`tools/finance/retirement-calculator.html` 共 4 页，新增 7 条（6 条高优），均为源码及数值推导，未做浏览器、线上和门禁验证。

### F-N9 复利年限超 1000 被静默截断、定投金额可为负（中，确认源码缺陷）
- 证据：`tools/finance/compound-interest.html:420` `Math.min(parseFloat(years)||0, 1000)`，输入 2000 年按 1000 年计算且页面不回显；`:421` 定投金额只做 `parseFloat||0`，无 `<0` 校验，`-1000` 会逐年减少余额却仍标为「定投」。
- 影响：`tools/finance/compound-interest.html`；长期测算被无声压缩，负投入产生与页面语义相反的结果。
- 方案：年限超上限时明确提示并显示实际使用年数；定投金额允许为空但禁止负数，字段级错误；结果区标注「按 1000 年上限计算」等口径。

### F-N10 分期实际利率无残差校验、负费率未拦截（中，确认源码缺陷）
- 证据：`tools/finance/installment-real-rate.html:276-291` 只校验本金与期数，`r` 可为负；二分区间固定 `[0, 1.0]`（月利率上限 100%），80 次迭代后直接采用区间中点，未验证 PV 残差，也未判断实际根是否越界。费率极高时输出上限值而无提示。
- 影响：`tools/finance/installment-real-rate.html`；负手续费或极端费率下「实际年化」仍显示为可信结果。
- 方案：校验费率 0–合理上限，求解后检查 `|PV−P|` 残差与根是否触及边界，越界时明确提示；负费率单独报错。展示每期还款的现金流方向，便于核对。

### 留存优化（按页落点，非确认缺陷）
- `tools/finance/compound-interest.html`：只能正算终值，缺「目标金额反推所需年限/月投」。建议加目标反推与「单利 vs 复利」并排对比，这是理财类搜索的主要意图。
- `tools/finance/installment-real-rate.html`：只有单一方案，无「多期数并排（12/24/36 期）」与手续费一次性/按期两种口径切换。建议并排展示不同期数的实际年化与总成本，便于用户直接比较。

### 续查覆盖
- 新抽查 `tools/finance/compound-interest.html`、`tools/finance/installment-real-rate.html` 共 2 页，新增 2 条中优与 2 条留存建议；为源码核查，未做浏览器、线上或门禁验证。

## 2026-11-03 续查（并行批）：金融回补
（路径均相对 `tools/`）

### F-N11 房贷首付未参与、零利率被拒（高，确认）
- 证据：`finance/mortgage-calculator:355` 读 downPaymentPct 后未用；100 万/30% 首付仍 4890.17（应 3423.12），CSV `:436` 同错；`:357` 的 `!annualRate` 拒 0%，`:371` 零分支不可达（100 万/30 年应 2777.78）。
- 影响/路径：`finance/mortgage-calculator.html`；房贷、明细、CSV 全错，零利率合法方案无法算。方案：首付扣贷款额、零利率均分。

### F-N12 公积金月缴存/年限无效、导出错表（高，确认）
- 证据：`finance/housing-fund-loan:329` 算 amountByMonthly，`:331` 取 min 漏掉；月缴 2000 改 0/20000 仍 120 万。`:201` 导出 `:596` 表实为 `:540` 历史表，非 `:399` 明细。
- 影响/路径：`finance/housing-fund-loan.html`；额度低估、导出不可核对。方案：纳入月缴项或删输入，明细单独导出。

### F-N13 租赁期初 IRR 时点错、手续费未计（高，确认）
- 证据：`finance/lease-payment-calculator:612` 租金全置 t=1..n，`:495` 期初已折减仍从 1 期算；10 万/6%/36 期 5.6655%（应 6.0000）。`:498` 总额含 fee，calcIRR 不含，fee 5000 仍 6.00%（实际约 2.75%）。
- 影响/路径：`finance/lease-payment-calculator.html`；期初与实际成本被低报。方案：首期 t=0、fee 入现金流。

### F-N14 APY 复利次数零/负未校验、单位易错（中高，确认）
- 证据：`banking/apy-calculator:224` 直接 pow；r=0.05、n=0 得 pow(Infinity,0)=1，显示 0.000%；n=-12 得 5.1381%。`:126` 只写名义年利率 r，输入 5 得 6434.50%。
- 影响/路径：`banking/apy-calculator.html`；非法 n 输出可信数字，单位误输放大百倍。方案：n 限正整数、r>-n，注明小数或 % 换算。

### F-N15 工资专项附加互斥缺失、模式不入历史（中，确认）
- 证据：`finance/salary-calculator:619` 房贷利息与租金直加，`:290` 仅文字提示；月薪 2 万/五险 4500/两项 2500 得税 590，仅租金应 690。`:803` 历史不存 currentMode，年薪 24 万刷新后按月薪算。
- 影响/路径：`finance/salary-calculator.html`；多扣税、恢复历史口径错误。方案：两项互斥、存模式。

### F-N16 LTV 负贷款被接受（中，确认）
- 证据：`banking/loan-to-value:220` 仅拦空值/NaN/分母 0；贷款 -10 万/价值 100 万得 LTV -10.0%、覆盖 100 万（`:283` max(loan,1)）、首付 110%。
- 影响/路径：`banking/loan-to-value.html`；负值被包装为有效结果。方案：限 >0、贷款>价值警示。

### F-N17 六页英文结果标签缺键（中，待验证）
- 证据：`i18n/tools/en` 与 `tool-i18n-en.js` 缺「最高可贷」「贷款价值比」「计算详情」「IRR」；精确匹配下疑似英文态残留中文，待探针。
- 影响/路径：上述 6 页；英文态可能中英混杂。方案：补字典并跑 `_en_i18n_probe.mjs --check`。

### 留存优化（按页落点）
- `finance/mortgage-calculator`：仅前 24 期；补首付+税费总成本与全表下载。
- `finance/housing-fund-loan`：规则硬编码 2024、年龄只提示；补利率可选与年龄压年限。
- `banking/apy-calculator`：补单利/复利/连续复利三列与 %/小数双输入。
- `finance/salary-calculator`：不可导出；补工资条导出与年终奖单独/合并对比。

### 续查覆盖
- 实读 6 页：finance 的 mortgage、housing、lease、salary；banking 的 apy、loan-to-value；node 复算，未做浏览器/线上验证。

## 2026-11-03 续查（并行批 I）

### F-N18 个税页负值输入产生负税后收入与虚增应税（中，确认）
- 证据：`finance/tax-calculator.html:184,188,195,199` 四个数字输入均无 `min`；`:506` 应税所得仅 `Math.max(0, …)` 兜底，`:525` `afterTax = salary - insurance - tax` 未再兜底。node 复算：月薪 2000、社保 3000（其余 0）→ 应税 0、税额 0、税后 −1000；月薪 20000、社保 −2000 → 应税 17000、税额 1990，而社保 3000 时为 990。
- 影响：`finance/tax-calculator.html`；负社保被当作抵扣放大应税所得、多缴税，负税后月薪直接显示为「¥-1,000.00」。
- 方案：月薪、社保、专项附加、起征点统一限 ≥0，税后收入下限 0 并标注；负值给字段级错误提示，不参与计算。

### F-N19 专项附加扣除明细未校验年度上限与互斥（中，确认）
- 证据：`:221-227` 七项仅设 `min="0"`，无 `max`；`:410-421` `__sdSum` 对大病医疗直接 `v/12`，未套 80000/年上限；住房贷款利息（sd5）与住房租金（sd6）可同时累加。node 复算：sd4=100000 → 计入 8333.33/月、税额 156.67；按 80000/年上限 6666.67 → 税额 323.33；房贷 1000+租金 1500 同填 → 扣 2500、税 740，仅租金 1500 时为 840。
- 影响：`finance/tax-calculator.html`；专项附加多扣、少缴，摘要与「明细合计」同屏却给出偏乐观税负；与 F-N15 同类的互斥缺失在本页再次出现。
- 方案：sd4 按 80000/年封顶后摊月；sd5 与 sd6 二选一并置灰另一项，超上限时提示实际采用值。

### F-N20 增值税税率/金额越界与非数字行静默按 0（中，确认）
- 证据：`:217,224,249` 仅写 `min/max` 属性，`onCustomRate`（`:404-411`）与 `calcSingle`（`:421-429`）从未 clamp 或检查 validity；批量 `:559-564` 用 `parseFloat(line)||0`。node 复算：含税 1000、税率 −50 → 不含税 2000、税额 −1000；不含税 1000、税率 150 → 税额 1500；批量行 "abc" 按 0 计入合计。
- 影响：`finance/vat-calculator.html`；负税额、超过 100% 的税额与 0 行都被当作有效结果，CSV/复制结果同样带出。
- 方案：税率限 0–100、金额限 ≥0，批量行非数字跳过并提示「已忽略 N 行」；导出与页面共用同一校验。

### F-N21 单利页「每年收息」选项不参与计算（中，确认）
- 证据：`finance/simple-interest.html:183-187` 定义 `select#mode`，但其只出现在 `:457-459` 预设与历史快照；`calc()`（`:310-338`）从未读取 mode。node 复算：10000 元/5%/3 年，两种模式输出完全相同（利息 1500、本利和 11500）。
- 影响：`finance/simple-interest.html`；用户切换「每年取息」得不到任何差异，控件形同装饰，也让人误以为已计入提前取息的现金流。
- 方案：删除该控件，或为「每年取息」输出逐期现金流表并说明其总利息与到期一次性相同、差别仅在时点。

### F-N22 信用卡最低还款模拟 120 期封顶与过低还款比例（高，确认）
- 证据：`finance/credit-card-interest.html:372-406` `maxMonths = 120` 硬停；`:384` `minPayment = Math.max(balance*minRatio+interest, 10)`；`:414` 直接显示 `months` 为「还清月数」。node 复算：账单 10000、日息 0.05%、最低比例 0% → 120 期后余额仍 10000、利息 18000、总支出 28000，仍显示「还清月数 120」；比例 1% → 120 期后余额 2993.80、总支出 20509.29，同样标 120 期；`showCompare`（`:491-505`）复用同一 120 期循环。
- 影响：`finance/credit-card-interest.html`；未还本金被当成已还清，总支出与还清时间系统性低估，对比结论同错。
- 方案：循环至余额清零，触顶时明确显示「120 期内未还清，剩余本金 X」；最低比例设合理下限，还款额低于当期利息时判定负摊还并告警；对比表同步。

### F-N23 气球贷「期末尾款比例」完全无效（高，确认）
- 证据：`finance/loan-amortization.html:419-435` 先算 `balloonAmount = amount*(balloonRatio/100)` 但全程未使用；月供按 `(1+m)^loanMonths` 全额摊还，末期 `pay = pmt + tempBal` 而 `tempBal≈0`。node 复算：100 万/4.9%/60 期月供 18825.45，尾款比例填 0 与 90 得到同一月供序列，末期无任何尾款。
- 影响：`finance/loan-amortization.html`；气球贷实际是 60 期普通等额本息，尾款与「低月供+到期大额」的产品特征完全丢失。
- 方案：月供只摊还 `(1-ratio)` 本金或按比例构造期末尾款，末期单独列出 balloonAmount；校验 ratio 0–100 与期数 >0。

### F-N24 贷款摊销页零利率被输入守卫拦截（中，确认）
- 证据：`:342-351` 守卫把 `annualRate` 列为分母项，值为 0 即返回「不能为 0」；`:391` 等额本息月供在 r=0 时为 `0/0`（NaN）。但等额本金/先息后本分支在 r=0 时数学上可算（利息为 0）。
- 影响：`finance/loan-amortization.html`；零息/贴息贷款无法测算，且把合法输入判为非法；与 F-N11 房贷页的零利率问题同类。
- 方案：r=0 时等额本息改用 `amount/totalMonths`、气球贷同理；守卫只拦截真正产生除零的路径，不再整体拒绝 0%。

### F-N25 提前还款分支未覆盖先息后本/气球贷，负金额可放大本金（中，确认）
- 证据：`:660-798`；`:753-782` 降低月供仅对 equal/principal 赋 `newPayment`，interest/balloon 下保持 0，页面显示「新月供 0.00」，减少月供等于当期月供（先息后本 100 万/4.9% 当期 4083.33）；`:668` prepayAmount 未限 ≥0，`:701` `newBalance = balanceBefore - prepayAmount`，输入 −100000 → 剩余本金从 969204.01 变为 1069204.01，「减少月供」显示 −547.59。
- 影响：`finance/loan-amortization.html`；两种还款方式得到不可能的 0 月供，负提前还款反向增加债务却无报错。
- 方案：按还款方式分别实现重算（先息后本按剩余本金/剩余期数，气球贷处理尾款）；prepayAmount 限 >0 且不超过剩余本金，负数直接报错。

### F-N26 提前还款页输入的「每月还款」不参与原方案（高，确认）
- 证据：`finance/mortgage-prepayment.html:132,260` 读取 `mp`，但 `:276-277` `before = monthlyPayment(p, annual, months)`、`totalBefore = before*months` 完全不用 mp；`:285-293` 降低月供也只按 `bal/months` 反推。node 复算：本金 50 万/4.5%/240 期，输入月供 3000，页面原方案月供 3163.25、总还款 759179.25；按输入 3000 应为 720000。
- 影响：`finance/mortgage-prepayment.html`；原方案与缩短期限模式（用 mp）基准不一致，「节省额」和「更省方案」结论失真。
- 方案：明确以输入月供为原方案基准（总还款 = mp×months），或改为「由本金/利率/期数计算月供并回填只读」；两种模式统一基准并在结果注明所用月供。

### F-N27 月供低于当期利息时 1200 期封顶输出负「缩短」（中高，确认）
- 证据：`:243-254` `remainingMonths` 上限 1200；`:280-282` `shortMonths = remainingMonths(...)`、`saveMonths = months - shortMonths`。node 复算：本金 50 万、提前还 2 万后余额 48 万，年利率 4.5%、月供 1000（当期利息 1800）→ 余额只增不减，返回 1200；页面显示「缩短 −960 个月」，总支出 1,220,000、节省 −460,820.75。
- 影响：`finance/mortgage-prepayment.html`；不可能还款的方案被当作有效结果，负期数与负节省额直接展示。
- 方案：先判定 `mp ≥ 当期利息`（否则提示负摊还、永不还清），再算期数；触上限时显示「1200 期内未还清」而非具体月数，并禁止负节省额结论。

### F-N28 「保留小数位数」>100 触发 RangeError（中，确认）
- 证据：`:136,262` precision 仅 `Math.max(0, parseInt(...))`、无上限；`:299-303` 直接 `toFixed(fixed)`，`calc()` 无 try/catch。node：`(1).toFixed(101)` 抛 `RangeError: toFixed() digits argument must be between 0 and 100`。
- 影响：`finance/mortgage-prepayment.html`；输入 101 后计算中断，结果区残留上一次内容，用户会误判为算错。
- 方案：precision 限 0–6（或 0–10），越界提示并回退默认值；或统一走安全格式化函数。

### 留存优化
- `finance/tax-calculator.html`：CSV 仅导出月度口径，年终奖两方案与「月度/年度」切换未随导出；建议补年终奖对比行与年度口径导出。
- `finance/simple-interest.html`：只有到期一次性/每年取息一个维度，缺「按天/按月计息」与「单利 vs 复利」并排；建议补两种计息口径对照，直接呼应「短期借贷不计复利」的场景。
- `finance/vat-calculator.html`：仅价税分离，缺「进项税抵扣后的应纳税额」与发票金额校验；建议加进项/销项与应纳税额小计。
- `finance/credit-card-interest.html`：对比卡只比最低还款与分期，缺「全额」与剩余本金曲线；建议三方案同表并画余额衰减。
- `finance/loan-amortization.html`：CSV 仅逐期明细，无逐年汇总与提前还款前后对比；建议导出包含年度聚合与提前还款前后两套表。
- `finance/mortgage-prepayment.html`：未计违约金/手续费，也无「提前还款时点」对比；建议补违约金输入与不同提前还款月份的节省曲线。
- `finance/tax-bracket.html`：仅年度应纳税所得额口径，缺税前收入→应税所得反推与月/年切换；建议补两项，减少用户手工换算。

### 续查覆盖
- 本次实读 7 页：`finance/tax-calculator`、`tax-bracket`、`vat-calculator`、`simple-interest`、`credit-card-interest`、`loan-amortization`、`mortgage-prepayment`；新增 11 条（高优 3 条：F-N22/F-N23/F-N26），`tax-bracket` 未发现缺陷（getBracket 在 36000/144000 边界与速算扣除一致，node 复算 100000 → 7480，与分档累加相同）。
- 证据均由源码行号 + node 内存复算取得；未做浏览器、英文态、移动端与门禁验证。

## 2026-11-03 续查（并行批 J）

### F-N29 NPV 页 IRR 无根仍返回上限 1000% 并判「可行」（高，确认）
- 问题：`calcIRR` 固定二分区间 `[-0.99, 10]`，只按「同号就抬 low」推进，从不校验端点异号或残差；现金流全为流出（或首期后仍无正值）时 NPV 永远为负，循环仍收敛到 high≈10，直接以 1000% 作为 IRR。
- 证据：`tools/finance/npv-calculator.html:381-396`（二分实现、`:395` 返回 mid）、`:427`（`irr = calcIRR(...)`）、`:433`（`irr >= r` 决定绿色）、`:457`（IRR 判「✓ 可行」）。node 复算：初始投资 10000、两期 −1000/−1000、折现率 8% → IRR 返回 10（即 1000%），同屏 NPV = −11,783.26（不可行），两项结论自相矛盾。
- 影响：`tools/finance/npv-calculator.html`；亏损/全流出项目被包装成超高收益且标「可行」，是投资决策页的核心误导。
- 方案：求解前检查 `npvAt(low)` 与 `npvAt(high)` 异号，无根时显示「无 IRR／现金流全为同号」；有根时校验残差并标注区间；IRR 越界（触 ±边界）明确提示而非当成结果。

### F-N30 NPV 页初始投资清空后旧明细与导出仍有效（中，确认）
- 问题：`calc()` 在 `init <= 0` 时只替换统计卡后 `return`，明细表、图表与历史读取的 `.result-box` 残留上一次结果；`exportCSV` 仍用当前（0）初始投资导出，历史记录也会把旧明细文本配到新输入上。
- 证据：`tools/finance/npv-calculator.html:398-404`（仅 `stats` 被改写并 return）、`:444-460`（明细写入 `#detail`）、`:563-571`（导出读 live 输入）、`:640-647`（`__npv_calculatorResText` 取首个 `.result-box`，即 `#detail`）。源码路径确定，未做点击验证。
- 影响：`tools/finance/npv-calculator.html`；用户清空初始投资后仍能看到旧 NPV/明细并可导出，历史记录与新参数错配。
- 方案：无效输入时统一清空 `stats`/`detail`/图表并禁用导出；历史只记录同一次有效计算的结果，或记录后校验结果与输入一致。

### F-N32 投资 ROI 页定投「年化收益率」以累计投入为基数严重低估（高，确认）
- 问题：定投终值按年金公式计算正确，但把全部累计投入当作期初一次性本金，`roi = 利润/累计投入`，再用 `pow(1+roi, 1/period)−1` 求年化；资金分期投入的时间价值被抹平，结果远低于输入的年化收益率。
- 证据：`tools/finance/investment-roi.html:547-556`（`:552` 年金终值、`:555` ROI、`:556` 年化）、`:563`（展示「年化收益率」）。node 复算：每月 1000 元、5 年、年化 12%（月利率 1%）→ 终值 82,486.37、累计投入 60,000、ROI 37.48%，页面年化输出 6.57%；该现金流真实现金流 IRR 即 12%。
- 影响：`tools/finance/investment-roi.html`；定投业绩被腰斩式低估，与同页「定投」语义冲突；与 F-N5 同类但为独立页面。
- 方案：按每期实际投入时点构造现金流求 IRR（月/周/年频率对应期数），区分名义年化与有效年化；同时展示累计投入、终值与 IRR，并与一次性投资口径并列。

### F-N33 投资 ROI 方案对比 0% 利率 + 追加投资输出 NaN（中，确认）
- 问题：`calcFV` 在 `add > 0` 时用 `((pow(1+r, years)−1)/r)`，`r=0` 得 `0/0=NaN`，整组统计被「计算结果含无效值」替换；图表同函数同缺陷。
- 证据：`tools/finance/investment-roi.html:668-675`（`:670` 只判 `p.add > 0`、`:672` 除零）、`:687-694`（NaN 守卫整卡替换）、`:717-724`（绘图复用同一公式）。node 复算：初始 10,000、年化 0%、5 年、每年追加 1,000 → 终值 NaN；0% 下正确终值应为 15,000。
- 影响：`tools/finance/investment-roi.html`；零收益/保本方案无法比较，而 0% 是合法输入。
- 方案：`r=0` 分支改为 `cost + add*years`，绘图同步；非零分支统一复用同一函数。

### F-N34 投资 ROI 方案对比：追加投入的年化口径导致错误排序（高，确认）
- `tools/finance/investment-roi.html:720-738` 先用全部投入计算累计 ROI，再按总期限开方，忽略追加资金的实际投入时点。例如均投 2 年，A 初始 100 元、年利率 9%、不追加；B 初始 100 元、年利率 10%、每年追加 100 元。页面将 B 的年化算为约 8.32%，低于 A 的 9%，判 A 更优；但 B 的假设年利率更高，不能这样跨不同现金流比较。
- 影响：追加投入导致收益率低估及方案排序失真。应按实际投入时点计算 IRR，同时明确比较口径。

### F-N35 工资税后页负百分比放大税基、缴费基数 0 被静默替换（中，确认）
- 问题：养老/医疗/失业/公积金比例仅由 HTML `min` 约束，`calc()` 未校验；负比例压低甚至反转五险一金，反而抬高应纳税所得额与税后工资。`base = getVal('base') || salary` 使填 0 的基数被工资静默替换。
- 证据：`tools/finance/payroll-calculator.html:479-482`（`getVal` 吞掉非法值）、`:491`（`|| salary` 回退）、`:501-508`（比例直乘、税基 `salary − insurance`）。node 复算（月薪 15,000、专项 1,000、其余默认，四比例合计 22.5%）：养老 8% → 五险一金 3,375、月应税 5,625、个税 352.50、到手 11,272.50；养老 −8% → 五险一金 975、应税 8,025、个税 592.50、到手 13,432.50；养老 −20% → 五险一金 −825、应税 9,825、到手 15,052.50（超过税前工资）。
- 影响：`tools/finance/payroll-calculator.html`；负比例让税负与到手工资双失真，0 基数用户无法表达「不缴」。
- 方案：各比例限 0–上限（养老 8/医疗 2 等按城市上限），越界字段报错；基数 0 视为无效并提示，或用空值语义区分「按工资」与「0」。

### F-N36 工资税后页历史恢复只回填工资/年终奖/城市（中，确认）
- 问题：历史只保存计算结果，恢复时 `salary`、`bonus`、`city` 三项回填，社保比例、缴费基数、六项专项附加与起征点仍用当前界面的值，重算结果不可复现。
- 证据：`tools/finance/payroll-calculator.html:583-599`（`currentResult` 不含输入项）、`:705-715`（`loadHistory` 仅三项赋值后 `calc()`）。源码路径确定，未做点击验证。
- 影响：`tools/finance/payroll-calculator.html`；同名历史记录在不同参数下重算出不同个税，与 F-N8/F-N15 的历史口径问题同类。
- 方案：历史记录完整输入快照（比例、基数、扣除项、起征点、城市），恢复后整体回填再计算；或历史条目直接保存完整结果并只读展示。

### F-N37 税后工资页「工作月数」控件不参与计算、税率表只列 5 档（中，确认）
- 问题：`months` 被读入却从未进入任何公式，改 3 个月与 1 个月结果完全相同；同页展示的税率表只列 1–5 级（至 30%），而计算使用完整 7 档，高收入者看到的「适用税率 45%」在表内无对应行。
- 证据：`tools/finance/salary-after-tax.html:261`（`months` 读入）、`:263-285`（全程未使用）、`:266`（7 档税率表）、`:288-299`（只输出 5 行）；另 `:273` 的 `net` 为未使用变量。node 复算：月薪 15,000、五险一金 1,650、专项 2,000 → 应税 6,350、个税 425，月数 1 与 3 输出一致。
- 影响：`tools/finance/salary-after-tax.html`；月数控件形同装饰，年度/多月汇总缺失；税率表与计算结果不自洽。
- 方案：删除月数输入，或补「N 个月合计税额/到手」与年度口径；税率表补齐 35%、45% 两档并高亮当前档。

### F-N39 租金回报页等额本息 0% 利率月供 NaN（中，确认）
- 问题：等额本息公式在 `monthlyRate=0` 时 `0/0`，而利率输入 `min="0"` 允许 0；月供与「月供后现金流」显示「—」，且未提示。
- 证据：`tools/finance/rental-yield-calculator.html:289`（利率 `min="0"`）、`:506-516`（`:510` 等额本息公式、`:511` 总利息、`:516` 现金流）。node 复算：房价 300 万、贷款比例 70%、0%、30 年 → 月供 NaN；正常 4.2% 时 10,269.36。
- 影响：`tools/finance/rental-yield-calculator.html`；无息/贴息贷款无法测算，现金流结果为空。
- 方案：`monthlyRate=0` 时月供取 `loanAmount/months`、总利息 0，本金分支同样处理；利率字段越界提示。

### F-N40 CAGR 页终值为负静默显示占位符（低，确认）
- 问题：`end` 无下限校验，负数进入 `Math.pow(e/s, 1/n)` 得 NaN；两枚结果卡被 `NaN→—` 兜底后只剩「—」，无任何错误说明或「负增长需改口径」提示。
- 证据：`tools/finance/cagr.html:218-227`（`:223` 幂运算、`:224-227` 两列结果）、`:239-249`（数据表重复计算）、`:300`（FAQ 已声明负值应改绝对变化）。node 复算：初值 100、终值 −50、2 年 → g=NaN，CAGR 与小数增长均显示「—」。
- 影响：`tools/finance/cagr.html`；用户不知道是输入非法还是页面故障，FAQ 与实现未打通。
- 方案：`end<0` 直接给字段错误并引导改用「绝对变化/亏损率」；或实现 `(end−start)/|start|` 的亏损口径并明确标注。

### 留存优化
- `tools/finance/npv-calculator.html`：现金流输入行无 `id`，历史快照只存折现率与初始投资（`renderCashFlows` 生成的 input 无 id），恢复历史无法复现现金流；建议给每期唯一 id 或整表 JSON 持久化，并在导出 CSV 中附 NPV/IRR/PI 结论。
- `tools/finance/investment-roi.html`：缺「一次性 vs 定投」同额对照与真实现金流 IRR 明细；方案对比仅终值维度，建议补增量 ROI 与投入差额列。
- `tools/finance/payroll-calculator.html`：年终奖仅单独计税，缺「并入综合所得」对比（与 tax-calculator 同类缺口，但在本页同样影响结论）；建议补两方案税额差。
- `tools/finance/salary-after-tax.html`：将废弃的月数控件改造为年度汇总，并把税率表补齐至 45% 档。
- `tools/finance/provident-fund.html`：额度仅「余额×倍数」，缺「月缴存额×剩余缴存月数」与年龄上限口径；建议双口径取小并展示计算过程。
- `tools/finance/rental-yield-calculator.html`：净回报未含空置率、租金涨幅与持有期退出收益，回收期也未计贷款；建议补空置率输入与含贷款的持有期 IRR。
- `tools/finance/cagr.html`：仅单一 CAGR 结果，缺「逐年数值 → 波动率/最大回撤」对照；建议补一条序列输入。

### 续查覆盖
- 本次实读 7 页：`finance/npv-calculator`、`investment-roi`、`cagr`、`payroll-calculator`、`salary-after-tax`、`provident-fund`、`rental-yield-calculator`；新增 12 条（高优 2 条：F-N29/F-N32；中优 9 条；低优 1 条）。
- 证据均为源码行号 + node 内存复算；刻意未重复 F-N15 已记录的「房贷利息+租金可同时扣」问题（`payroll-calculator.html:505` 同类但已覆盖）。未做浏览器、英文态、移动端、门禁与线上验证；历史已修声明未独立复验。

## 2026-11-03 续查（并行批 K）

> 范围：本轮阅读 8 页（`tools/finance/inflation-calculator.html`、`credit-card-grace-period.html`、`mutual-fund-calculator.html`、`investment-calculator.html`、`futures-pnl-calculator.html`、`discount-calculator.html`、`sharpe-ratio.html`、`portfolio-return.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证；历史已修声明未独立复验。

### F-N41 通胀页反向模式把折现值算成终值（高，确认）
- 描述：反向模式输入「未来金额」，`getYearData()` 却用 `purchasingPower = amt * factor` 复利放大，而文案与结果卡都称这是「折现到现在」的现值；正向分支另一路 `amt / factor` 才正确。
- 证据：`tools/finance/inflation-calculator.html:386-394`（`:392` 反向 `amt * factor`）、`:435-437`（结果文案「折现到现在」）、`:182`（通胀率无 min/max）。
- 复现：切「未来的钱现在值多少」，未来 100,000 元 / 3% / 20 年 → 页面 180,611.12 元（期望 55,367.58 元）；明细表与图表同样按放大后的序列绘制。
- 影响：`tools/finance/inflation-calculator.html`；反向折算方向相反，用户拿到的「等值现值」被放大约 3.26 倍（1.03²⁰×1.03²⁰），历史折算与保值目标全部失真。
- 方案：反向模式改为 `purchasingPower = amt / factor`；两模式的「购买力 / 所需金额」统一由同一函数按方向推导，并用 100 元 3% 10 年 ≈ 74.41 元的已知样例校验。

### F-N42 信用卡免息期两个日期下拉框从未生成选项（高，确认）
- 描述：`<select id="bill">` 与 `<select id="due">` 均为空标签，全文没有任何 `option` 生成或赋值逻辑；两处读值用 `parseInt(...) || 10 / || 25` 兜底，因此无论用户如何操作都只按账单日 10、还款日 25 计算。
- 证据：`tools/finance/credit-card-grace-period.html:128,132`（空 select）、`:263-266`（兜底 10/25）、`:303-307`（`resetForm` 只 `selectedIndex=0`）、`:365-367`（图表同样兜底）。
- 复现：页面打开即为空白下拉框，点「重置」或尝试切换 → 结果卡恒为「最长免息期 44 天 / 账单日当天 15 天」，表格固定「账单日 10 日、还款日 25 日」。
- 影响：`tools/finance/credit-card-grace-period.html`；核心输入（账单日/还款日）完全不可用，所有用户的免息期结论都是同一个默认值，属于工具不可用级缺陷。
- 方案：初始化时生成 1–28 的 option（或改为 number 输入并校验 1–28），移除 `||10/||25` 的静默兜底；空值给字段级错误。

### F-N43 定投页零输入现金流收敛到边界，年化 IRR 显示 −600%（高，确认）
- 描述：`calcIRR` 固定区间 `[-0.5, 1]`，100 次二分后直接取中点，不校验端点异号与残差。当每月定投与初始投入都为 0 时全部现金流为 0，NPV 恒为 0，`if(npv > 0)` 永不成立 → `high` 一路压到 `low=-0.5`，`-0.5×12×100 = -600%`。
- 证据：`tools/finance/mutual-fund-calculator.html:596-615`（`:603` 固定区间、`:610-614` 无残差校验）、`:480-482`（monthly/initial 均允许 0）、`:545`（直接采用返回值）、`:645`（展示「年化收益率（IRR）」）。
- 复现：初始投入 0、每月定投 0、年限 10（其他默认）→ 页面年化 IRR −600.00%，同屏总投入 ¥0、总收益 ¥0、期末 ¥0。
- 影响：`tools/finance/mutual-fund-calculator.html`；清空输入即出现不可能的 −600%，且任何无根现金流都会静默返回边界伪解（与 F-N29 同类，但属独立页面）。
- 方案：`totalInvest <= 0` 或现金流全零时不出 IRR 并提示；求解前检查两端 NPV 异号，收敛后校验残差，触边界明确提示「无解/超出区间」。

### F-N44 定投页亏损金额丢负号（中，确认）
- 描述：统计卡 `profitSign` 仅对盈利赋 `+`，金额又统一取 `Math.abs()`，亏损时符号为空 → 卡片只剩绝对值，文字层面看不到负号；同屏累计收益率仍为负。
- 证据：`tools/finance/mutual-fund-calculator.html:617-625`（`:619` 符号、`:623` `Math.abs`）、`:628-629`（结果区同样的 `profitSign` + `Math.abs`）。
- 复现：初始 10,000、每月 1,000、1 年、年化 −50% → 总收益 −6,400.93 元，卡片显示「¥6,401」，累计收益率显示 −29.10%。
- 影响：`tools/finance/mutual-fund-calculator.html`；金额与百分比符号不一致，红/绿色不足以替代负号，亏损易被读成盈利（与 F-N6 同类但为独立页面）。
- 方案：金额直接输出 `-¥6,400.93`（或统一 `formatSigned`），盈利才加 `+`；补亏损样例校验。

### F-N45 定投页初始申购费未计入费用合计、期初扣款 IRR 时点错位（中，确认）
- 描述：`totalFees` 从 0 开始，循环内只累加每月定投的申购费，初始投入按 `initial*(1-buyFee)` 扣了份额却从未计入费用；`calcIRR` 形参含 `monthStart` 但函数体完全不用，月度现金流始终放在 t=1..N。
- 证据：`tools/finance/mutual-fund-calculator.html:499-501`（费用初值 0、初始扣费只减份额）、`:511-512`（仅月投计费）、`:545` 与 `:596-601`（monthStart 传入未用、现金流固定 t=1..N）。
- 复现：初始 10,000、每月 1,000、10 年、年化 8%、申购费 1% → 费用合计 1,200 元（期望 1,300 元，少 100 元初始申购费）；勾选「月初」时页面 IRR 8.12%，按 t=0..119 的真实现金流为 8.00%（有效年化 8.30%）。
- 影响：`tools/finance/mutual-fund-calculator.html`；费用展示系统性偏低，期初/期末两种扣款给出与自身余额模型不一致的 IRR。
- 方案：把 `initial*buyFee` 计入 `totalFees`；`monthStart` 为真时现金流放 t=0..N−1 并重解 IRR，同时校验残差。

### F-N46 投资回报页负「追加投入」把亏损翻成盈利（中，确认）
- 描述：守卫只校验初始投入、期末价值、年限，`additional` 未限 ≥0 也未按取出处理；负值直接减少「总投入」，放大回报率。极端负值使总投入 ≤0 时，回报率/CAGR 又被静默记 0，与同屏盈亏金额矛盾。
- 证据：`tools/finance/investment-calculator.html:280`（读 add）、`:281`（守卫未含 add）、`:285-288`（`totalInv = init + add`、`totalInv > 0` 才计算）、`:294-300`（输出总投入、盈亏、回报率、CAGR）。
- 复现：初始 10,000、期末 8,000、5 年、追加 −5,000 → 总投入 5,000、累计盈亏 +3,000、累计回报率 +60.00%、CAGR +9.86%（原始现金流实为亏损）；追加 −20,000 → 总投入 −10,000，同屏显示「累计盈亏 +15,000」而回报率 0.00%。
- 影响：`tools/finance/investment-calculator.html`；任意负追加都能把亏损包装成高收益，极端值输出自相矛盾的卡片组合（与 F-N34 同类但属独立页面）。
- 方案：追加投入限 ≥0，负值走「取出」独立分支并按真实现金流求 IRR；总投入 ≤0 时整体报错而非部分置 0。

### F-N47 期货盈亏页 0 保证金率/0 手数被静默替换，收益率失真（中，确认）
- 描述：`lots = parseInt(...) || 1` 把 0 手替换成 1 手；`marginRate` 只做 `parseFloat || 0`，未校验 0 与负值；收盘价 0（`min="0"` 允许）也照算。保证金为 0 时 `returnRate` 记 0，与同屏大额盈亏冲突。
- 证据：`tools/finance/futures-pnl-calculator.html:237-263`（输入属性）、`:457`（手数兜底）、`:458`（保证金率兜底）、`:462-469`（盈亏与收益率）、`:479-480`（保证金/杠杆展示）。
- 复现（IF，乘数 300）：手数填 0 → 按 1 手算出净盈亏 14,940 元；保证金率填 0 → 保证金 0.00、杠杆 0.0x、收益率 +0.00%（实际盈亏 +14,940）；收盘价填 0 → 盈亏 −1,050,060、收益率 −833.38%；保证金率 −12 → 保证金 −126,000。
- 影响：`tools/finance/futures-pnl-calculator.html`；无效输入仍输出精确到分的「收益率」，0 手/0 保证金/负保证金被当成合法方案。
- 方案：手数限整数 ≥1 且空值报错；保证金率限 (0,100]；开/收盘价 >0 校验；保证金 ≤0 时不出收益率并提示。

### F-N49 折扣页叠加折扣控件显示「0.8 折」却按 8 折计算（中，确认）
- 描述：叠加链的 input 值是 0–1 的乘数（0.8），但模板在输入框后直接跟一个「折」字，渲染成「0.8 折」；用户按标签改成 8 时 `updateDiscount` 不做 ÷10 换算，整条折扣链变成 8 倍。
- 证据：`tools/finance/discount-calculator.html:326-328`（chip 模板 `${d}` + 「折」）、`:343-346`（`parseFloat(v) || 0` 直接存乘数）、`:367-370`（直接连乘）、`:380`（叠加式按乘数展示）。
- 复现：默认原价 100、chip 显示「0.8 折」→ 结果 80 元（即 8 折）；把 chip 改为 8（用户理解为 8 折）→ 结果 800 元、节省 −700 元、显示「−700.0% OFF」。
- 影响：`tools/finance/discount-calculator.html`；同一控件显示单位与计算单位相反，误改一次即放大 10 倍，且无任何范围提示（`min/max` 只约束了 spinner，手输不受限）。
- 方案：chip 显示 `value*10` 折、输入按「几折」解析后 ÷10；或统一改成「折扣率（0–1）」并去掉「折」字，两处单位保持一致。

### F-N50 夏普页无风险利率未随频率换算，默认值即口径错配（中，确认）
- 描述：默认收益序列是 15 期（按月），无风险利率默认 3%（年化），`calc()` 直接相减，未按年化系数把 Rf 折算到同频率；同时页面用未年化 Sharpe 与年化 Sharpe 各判一次评级，同一策略出现两个相反结论。
- 证据：`tools/finance/sharpe-ratio.html:130`（默认 15 期序列）、`:149`（Rf 默认 3）、`:153-158`（默认年化系数 12）、`:307-337`（直接 `portReturn - riskFree`）、`:349-353` 与 `:363-368`（两套评级同屏）。
- 复现：默认输入（均值 3.40%、σ 3.42%、Rf 3%）→ 夏普 0.117、年化 0.405「较差」；若按月对齐 Rf=0.25%，应为 0.921、年化 3.189。直接模式 8%/12%/Rf 3% + 默认「月→年」→ 0.417「较差」与 1.443「良好」同屏。
- 影响：`tools/finance/sharpe-ratio.html`；默认结果把夏普低估约 8 倍（0.117 vs 0.921），且同一组数据给出互相矛盾的评级。
- 方案：按年化系数把 Rf 换算到每期口径（或把 Rf 标签改为「每期无风险利率」并在切 tab 时同步）；只对最终选用口径输出一个评级，另一个作为参考值不评级。

### F-N51 组合收益页「权重合计」按小数显示、预设给出 200% 权重（低，确认）
- 描述：`w1/w2` 已先 ÷100，页脚却用 `(w1+w2).toFixed(2)` 展示，默认 60/40 显示「权重合计 1.00」而非 100%；「示例 2×」预设直接把权重设成 120/80（合计 200%）并按此加权，页面只列合计值、无任何超限提示。
- 证据：`tools/finance/portfolio-return.html:228`（合计显示）、`:246-252`（表格同值）、`:262-269`（预设 120/80）、`:123`（公式声明合计应≈100%）。
- 复现：默认 60/40 → 「权重合计 1.00」；点「示例 2×」→ 权重 120/80、合计 2.00、组合预期收益 41.60%，无警示。
- 影响：`tools/finance/portfolio-return.html`；单位错位让「≈100%」的校验形同虚设，演示预设输出 200% 权重的无意义结果。
- 方案：合计按百分比展示并在 ≠100% 时提示/归一；把「示例 2×」改为权重不变、收益按 2 倍映射的对照预设，避免直接写入非法权重。

- 本轮实读 8 页：`tools/finance/inflation-calculator.html`、`tools/finance/credit-card-grace-period.html`、`tools/finance/mutual-fund-calculator.html`、`tools/finance/investment-calculator.html`、`tools/finance/futures-pnl-calculator.html`、`tools/finance/discount-calculator.html`、`tools/finance/sharpe-ratio.html`、`tools/finance/portfolio-return.html`；新增 11 条（高 3 / 中 7 / 低 1）；未覆盖：其余 finance 页（约 90 页）未逐页复扫。
- 证据均由源码行号 + node 内存复算取得；未做浏览器、英文态、移动端、门禁与线上验证；历史已修声明未独立复验。

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 8 页（`tools/finance/profit-margin-calculator.html`、`depreciation-calculator.html`、`position-size-calculator.html`、`insurance-calculator.html`、`stock-profit-calculator.html`、`option-profit-calculator.html`、`break-even-calculator.html`、`capm-return.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证；历史已修声明未独立复验。

### F-N52 利润率页折旧摊销从未扣除，EBITDA 与净利润同时虚增（高，确认）
- 描述：`opExp` 只汇总销售/管理/研发费用，`ebit = opProfit` 未减折旧摊销；随后 `ebitda = ebit + da`，相当于在「未扣 D&A 的 EBIT」上再加一次折旧。净利率、利润总额、所得税均沿用该虚增利润，而同页饼图/成本构成又把折旧摊销当作独立成本项，口径自相矛盾。
- 证据：`tools/finance/profit-margin-calculator.html:445-455`（`:445` 期间费用只含三项、`:449-451` EBIT/EBITDA、`:453-456` 税与净利）、`:459-462`（四张利润率卡）、`:644-646`（饼图把折旧摊销列为成本却未从净利中扣）。
- 复现：默认值（收入 100 万、成本 60 万、销售 8 万、管理 10 万、研发 5 万、财务 2 万、折旧摊销 6 万、税率 25%）→ 页面 EBITDA 230,000、净利率 11.25%、净利润 112,500（期望 EBITDA 170,000、净利率 6.75%、净利润 67,500）。
- 影响：`tools/finance/profit-margin-calculator.html`；重资产企业的核心盈利指标被系统性高估（本例净利润虚增 40%），并污染行业对比与 CSV 导出。
- 方案：`ebit = gp − opExp − da`，`ebitda = ebit + da`；饼图与成本构成复用同一 `ebit`/`np`，删除重复现金流的二次计入；补一条含 D&A 的强用例。

### F-N53 折旧页「工作量法」每年均摊，结果恒等于直线法（中，确认）
- 描述：`calcUnits` 没有「当年工作量」输入，直接把总工作量按年限平均（`yearUnits = totalUnits / life`），再乘以单位折旧额，数学上等于 `(原值−残值)/年限`。页面公式说明却写「年折旧额 = 当年工作量 × 单位工作量折旧额」，`remainingUnits` 计算后从未使用。
- 证据：`tools/finance/depreciation-calculator.html:334-346`（`:340` 平均分配、`:343` 递减后未用）、`:207-208`（说明与实际不符）、`:170`（只有一个「总工作量」输入）。
- 复现：原值 100,000、残值 5,000、5 年、总工作量 10,000 → 每年折旧 19,000，与直线法 19,000 完全相同；任何总工作量取值都只改变单位折旧额与年工作量，乘积不变。
- 影响：`tools/finance/depreciation-calculator.html`；第四种方法退化为直线法的副本，四方法对比表出现两列相同数据，用户会误以为产量波动已计入。
- 方案：为每年（或每期）提供实际工作量输入，按 `当年工作量 × 单位折旧额` 计算并校验累计不超过可折旧总额；无法提供逐年工作量时删除该选项，避免伪方法。

### F-N54 仓位页马丁格尔「平均价」数学上恒等于当期价（中，确认）
- 描述：`avg = cumCost / (cumPos / price)`，而 `cumPos` 与 `cumCost` 在每层都相等，化简后 `avg === price`。平均持仓成本应为 `累计投入 / 累计股数`，页面却把累计投入除以「按当期价折算的股数」，导致每层平均价都等于该层价格，最终平均成本与真实成本相差数个百分点。
- 证据：`tools/finance/position-size-calculator.html:527-535`（`:528` 本层投入、`:529-533` 累计与错误 avg）、`:543`（采用该 avg）、`:620-627`（表格与「下跌 X%」结论）。
- 复现：初始仓位 1,000、2 倍、5 次、每次跌 10% → 第 5 层页面平均价 65.61 元（真实平均成本 71.23 元）；页脚「相对初始价下跌 34.39%」（按真实平均成本应为 28.77%）。
- 影响：`tools/finance/position-size-calculator.html`；加仓计划的回本价被低估约 8%，用户会误判反弹到 65.61 即可解套。
- 方案：累计股数改为 `cumShares += pos / price`，`avg = cumCost / cumShares`；全部层级与页脚统一用该 avg，并补一组可手算的强弱用例。

### F-N55 保险页双十法则明细金额与结果卡不一致、年支出输入无效（中，确认）
- 描述：结果卡用 `income*10 + debt − existing` 计算寿险保额，明细行却硬写 `income*10`；`dt_expense` 读入后从未参与任何公式，输入框形同装饰。
- 证据：`tools/finance/insurance-calculator.html:473-481`（`:474` 读入未用、`:478` 计算含负债/已有保障）、`:490`（明细值仅 `income*10`）、`:601`（结果卡用 `lifeInsurance`）。
- 复现：年收入 20 万、家庭负债 80 万、已有保障 10 万 → 寿险保额卡 270 万，同屏明细「寿险保额计算：200万（年收入×10）」；改年支出 12→0 或 100 万，所有结果不变。
- 影响：`tools/finance/insurance-calculator.html`；同一屏出现两个寿险保额，用户无法判断以哪个为准，年支出控件给出错误的可调预期。
- 方案：明细行改用 `lifeInsurance` 并列出「收入×10 + 负债 − 已有保障」过程；年支出要么纳入需求缺口，要么移除该输入。

### F-N57 股票盈亏页负买入价产生巨额正盈亏、百分比却归零（中，确认）
- 描述：买入价、卖出价只靠 HTML `min="0"`（手输不受限），`calc()` 未做任何范围校验；`buyTotal` 可为负，`pnl = sellTotal − buyTotal` 因此变成大额正数，而 `pnlPct` 以 `buyTotal > 0` 为门槛，负分母时直接记 0，同屏金额与百分比互相矛盾。数量清空时最低佣金仍产生 5 元成本。
- 证据：`tools/finance/stock-profit-calculator.html:190,194,201`（输入属性）、`:454-457`（读值无校验）、`:470-480`（买入成本可为负）、`:502-503`（`:503` `buyTotal > 0` 才计百分比）。
- 复现：买入价 −10、数量 1000、卖出价 11、默认费率 → 买入总成本 −9,995.10、盈亏金额 +20,984.49、盈亏百分比 +0.00%；数量清空 → 买入总成本 5.00、盈亏 −5.00、−100.00%（仅剩最低佣金）。
- 影响：`tools/finance/stock-profit-calculator.html`；非法价格被包装成翻倍收益，复制/导出的 CSV 同样带出矛盾数值。
- 方案：买入价/卖出价限 >0、数量限正整数；`buyQty<=0` 或价格为负时清空结果并禁用复制/导出；最低佣金只在成交量 >0 时计入。

### F-N58 期权页最大盈亏未扣手续费、合约数 0 被替换为 1（低，确认）
- 描述：`maxProfit`/`maxLoss` 只按权利金乘乘数、张数展示，未扣除 `totalFee`；而总盈亏已扣开平仓手续费，同屏最大亏损与总盈亏口径不一致。`contracts`/`mult` 用 `Math.max(1, …)` 兜底，清空或填 0 仍按 1 张/乘数 1 计算。
- 证据：`tools/finance/option-profit-calculator.html:456-457`（`:456` 张数兜底、`:457` 乘数兜底）、`:497-498`（手续费只进总盈亏）、`:544-553`（最大盈亏未扣费）。
- 复现：1 张、乘数 100、权利金 5、手续费 2 元/张 → 最大亏损显示 ¥500，含开平仓手续费应为 ¥504；清空「合约数量」→ 页面仍输出 1 张的完整结果。
- 影响：`tools/finance/option-profit-calculator.html`；风控口径少算手续费，空输入给出看似有效的结论。
- 方案：最大盈亏按「权利金 ± 手续费」计算并在文案注明含费；张数/乘数改为正整数校验，空值给字段错误而非默认 1。

### F-N59 盈亏平衡页亏损产品边际贡献率硬写 0%，负成本得负平衡销量（中，确认）
- 描述：`calcBEP` 在 `cm <= 0` 时直接返回 `cmRatio: 0`，页面同时显示「单位边际贡献 −10.00」与「边际贡献率 0.00%」，二者矛盾；固定成本为负时 `beq = fc/cm` 为负，直接渲染负的平衡销量与负平衡收入，且安全边际率按负 BEP 计算仍可能评为「很安全」。
- 证据：`tools/finance/break-even-calculator.html:364-368`（`:366` 强制 cmRatio 0）、`:387-391`（无负值提示）、`:198-207`（五个数字输入均无 min）。
- 复现：单价 50、单位变动成本 60、固定成本 10 万 → 单位边际贡献 −10.00、边际贡献率 0.00%（应为 −20.00%）、平衡销量「—」；固定成本 −10 万、单价 50、变动成本 30 → 平衡销量 −5,000 件、平衡收入 −250,000 元，页面照常渲染。
- 影响：`tools/finance/break-even-calculator.html`；亏损产品的边际贡献率被抹成 0，负成本输入产出不可能的平衡点，敏感性分析与多场景对比沿用同一函数。
- 方案：cm<0 时 cmRatio 输出真实负值并提示「单价低于变动成本，不存在平衡点」；固定成本、售价、销量限 ≥0，负 BEP 不出结果。

### F-N60 CAPM 页切换输入口径不重算、不换算已填数值（低，确认）
- 描述：`#unit` 下拉只决定除以 1 还是 100，但没有 `onchange`，切换后结果区仍是旧口径数值；同时已填的 0.03/0.08 不随口径换算，点击计算后直接缩小 100 倍，页面无任何提示。
- 证据：`tools/finance/capm-return.html:148-151`（select 无事件）、`:200-209`（`:203-204` 仅按 `unit` 除以 k）、`:260-265`（重置只设 unit=1 不换算其他输入）。
- 复现：默认（Rf 0.03、β 1.2、Rm 0.08）E(R) 9.0000%；切「百分数（3 表示 3%）」后结果区仍为 9.0000%，点「计算」后变为 0.0900%。
- 影响：`tools/finance/capm-return.html`；用户误以为切换口径已生效，或在切换后拿到缩小 100 倍的必要收益率。
- 方案：select 加 `onchange="capmCalc()"`，切换时把 Rf/Rm/实际收益按 100 倍互转并重算；或在结果区显著标注当前解读口径。

- 本轮实读 8 页：`tools/finance/profit-margin-calculator.html`、`tools/finance/depreciation-calculator.html`、`tools/finance/position-size-calculator.html`、`tools/finance/insurance-calculator.html`、`tools/finance/stock-profit-calculator.html`、`tools/finance/option-profit-calculator.html`、`tools/finance/break-even-calculator.html`、`tools/finance/capm-return.html`；新增 9 条（高 1 / 中 6 / 低 2）；未覆盖：其余 finance 页（约 71 页）未逐页复扫。
- 证据均由源码行号 + node 内存复算取得；未做浏览器、英文态、移动端、门禁与线上验证；历史已修声明未独立复验。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（`tools/finance/amount-in-words.html`、`tools/finance/number-to-words-chinese.html`、`tools/finance/gold-price-calculator.html`、`tools/finance/shebeizulinfeilvjisuan.html`、`tools/finance/register-depreciation.html`、`tools/finance/credit-card-validator.html`、`tools/finance/credit-card-luhn.html`、`tools/finance/points-redemption-value.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证；历史已修声明未独立复验。

### F-N61 金额大写转换器：零分组仍拼「万/亿」、三位小数产出 undefined 角（高，确认缺陷）
- 描述：`integerToCN` 从低位向高位遍历 4 位分组，无论该组是否为 `"0000"` 都执行 `out += part + BIG[b]`，零分组会凭空多出「万/亿」且不补「零」；小数部分 `f = Math.round((val - y) * 100)` 达到 100 时 `jiao = 10`，`CN[10]` 为 `undefined`，直接写入结果；另因浮点误差，1.005 被舍成 0 分而静默显示「壹元整」。
- 证据：`tools/finance/amount-in-words.html:250-251`（零分组仍拼 BIG）、`:262`（f 可为 100）、`:265-272`（`CN[jiao]` 无越界保护）、`:261`（1e-8 偏移不足以保证两位小数）
- 复现：输入 100000000 → 实际「壹亿万元整」（期望「壹亿元整」）；100000001 → 「壹亿万壹元整」（期望「壹亿零壹元整」）；100010001 → 「壹亿壹万壹元整」（期望「壹亿零壹万零壹元整」）；1.999 → 「壹元undefined角」、0.999 → 「零元undefined角」（期望按分进位为「贰元整 / 壹元整」）；1.005 → 「壹元整」（期望「壹元零壹分」）
- 影响：`tools/finance/amount-in-words.html`；支票、发票、合同的大写金额在含零分组或三位小数时直接错误或出现英文 `undefined`，属不可交付的财务文本。
- 方案：零分组跳过并统一补「零」（仅在非最高组且后续有值时），如「壹亿零壹万零壹」；小数改为 `Math.round(val * 100)` 后进位（`f >= 100` 时 `y += 1; f -= 100`），或直接解析输入字符串的小数位；对 `CN[jiao]` 加边界。

### F-N62 数字转中文（逐位小数）：浮点尾数被逐位读出（高，确认缺陷）
- 描述：`numberToChinese` 用 `decPart = n - intPart` 再做 `decPart.toString().replace(/^0\./, '')` 逐字符映射，二进制浮点尾差会原样进入中文结果，常见两位小数金额即可输出十几位错误数字。
- 证据：`tools/finance/number-to-words-chinese.html:315-328`（`:316` 浮点减法、`:325` 直接 toString 取小数位）
- 复现：输入 10012003.45 → 实际「一千零一万二千零三点四四九九九九九九九二五四九四一九四」（期望「…点四五」）；1.1 → 「一点一零零零零零零零零零零零零零零零九」（期望「一点一」）；3.14 → 小数段出现 `一四零零零零…`（期望「三点一四」）
- 影响：`tools/finance/number-to-words-chinese.html`；绝大多数带小数输入都会得到不可读的长串，且页面无异常提示。
- 方案：从原始输入字符串取小数部分（`v.split('.')[1]`），或 `toFixed(保留位数)` 后再逐位映射；不要用浮点差值。

### F-N63 金价回收页折价率无上下限，150% 回收价高于金价、负折价出负数（中，确认缺陷）
- 描述：`discountRate` 仅靠 HTML `max="100"` 限制，`calcAll()` 用 `parseFloat(...) || 0` 读取后未校验范围；折价率 >100 时回收估价超过金料总值，为负时输出负回收价，结果卡片仍按原样标注「回收估价（150%）」。
- 证据：`tools/finance/gold-price-calculator.html:238`（仅属性 max）、`:503-506`（读值无范围判断）、`:519`（`totalCny * discount / 100`）、`:529`（直接回显 discount）
- 复现：金价 650 元/克、足金 999.9、10 克 → 金料总值 ¥6,499.35；折价率 150% → 回收估价 ¥9,749.03（期望 ≤¥6,499.35）；折价率 −10% → ¥−649.94（期望报错或按 0）
- 影响：`tools/finance/gold-price-calculator.html`；回收金额可高于金料本身，负数也会进入复制/导出与历史记录。
- 方案：折价率限制 `0 ≤ d ≤ 100`（或 `0 < d ≤ 100`），越界标红并停止计算；结果卡显示实际采用的折价率且与输入联动。

### F-N64 设备租赁费率页残值率可越界，负折旧/负租金与 ROI 公式互斥（中，确认缺陷）
- 描述：`readInputs()` 只把 NaN 记为 0 并描红，`calc()` 仅校验 P/T/Y > 0；残值率 s、维护费率 r、利润率 m 可为负或 >100。s>100 时 `depreciableBase` 为负、月折旧为负，月租金可低于维护费；s<0 时残值转负、折旧基数被放大。同时信息框 ROI 公式 `(R×T − P×s)/(P×s)` 与实现 `(R×T + 残值 − P)/P` 完全不同。
- 证据：`tools/finance/shebeizulinfeilvjisuan.html:187-193`（只判 NaN）、`:197-209`（仅 P/T/Y 校验、`:201-209` 直接使用 s/r/m）、`:138`（s 仅属性 max）、`:146`（ROI 公式文案）
- 复现：P=500000、T=24、Y=8、r=3、m=8、s=150 → 期末残值 ¥750,000、月折旧 ¥−2,604.17、月租金 ¥1,979.17、ROI +59.50%（期望拒绝 s>100）；s=−50 → 月租金 ¥12,395.83、ROI −90.50%；默认参数下文案公式为 (9531.25×24−25000)/25000≈815%，页面实际 −49.25%
- 影响：`tools/finance/shebeizulinfeilvjisuan.html`；非法残值率会产生负折旧/负租金并被评为正回报，导出的 CSV 与复制结果同样带出。
- 方案：s 限 `0 ≤ s < 100`（至少 ≤100），r、m 限 ≥0；`iv.valid === false` 时停止计算；信息框 ROI 改为 `(R×T + P×s/100 − P)/P × 100%` 并注明租期短于折旧年限时可为负。

### F-N65 固定资产折旧页未来购入日期也按已提满一年计算（中，确认缺陷）
- 描述：`yearsElapsed = Math.floor((now - purchaseDate)/年)`，未来日期被负数分支强制置 0，随后仍取 `schedule[0]`（第 1 年年末数），因此尚未购入的资产立即显示「当前年度 1/N」、累计折旧一整年、账面价值已扣一年；同一映射也使恰好满 1 年的资产直接跳到第 2 年数。
- 证据：`tools/finance/register-depreciation.html:335-337`（`:336` 负数置 0、`:337` 取 `schedule[yearsElapsed]`）、`:421`（显示 `yearIdx + 1`）、`:266`（仅声明「购入当年按完整年度」）
- 复现：购入日期 2027-01-01、原值 10000、残值 500、5 年、直线法 → 实际「当前年度 1/5」、累计折旧 ¥1,900.00、账面 ¥8,100.00（期望 0 年、¥0.00、¥10,000.00）；购入日期恰为 2025-11-04（满 1 年）→ 实际第 2 年数 ¥3,800.00、账面 ¥6,200.00（按已完成年度应为 ¥1,900.00、¥8,100.00）
- 影响：`tools/finance/register-depreciation.html`；未来资产被提前计提，满年资产多提一年，资产清单汇总、导出 CSV 与明细表全部沿用该口径。
- 方案：未来日期直接返回 0 年/0 折旧/原值；按已完成年度取 `schedule[yearsElapsed - 1]`（第 0 年取原值），或明确把 `yearIdx` 解释为「当前计提年度」并在页面显著标注按整年计提。

### F-N66 信用卡校验页未知卡组织即使 Luhn 通过也永远停在「继续输入」（中，确认缺陷）
- 描述：未知 BIN 返回 `lengths: []`，`lengthOk` 恒 false，且 `digits.length >= brand.lengths[0]` 与 `undefined` 比较恒 false；因此 16 位、Luhn 完全通过的未知卡组织号永远落入最后的「⏳ 继续输入以完成校验…」，不会给出任何完成态或「卡组织未知」的结论。
- 证据：`tools/finance/credit-card-validator.html:331`（未知返回空 lengths）、`:386-391`（空 lengths 走通用长度文案）、`:400-406`（`:400` 与 undefined 比较、未知卡组织无法命中「卡号有效」）
- 复现：输入 9999999999999995（16 位、Luhn 通过、不匹配任何卡组织）→ 实际「长度校验 ⚠️ 当前 16 位（卡组织通常 13-19 位）」「Luhn 校验 ✅ 通过」「⏳ 继续输入以完成校验…」（期望「Luhn 通过，卡组织未知」或按 13-19 位通用长度判定完成）
- 影响：`tools/finance/credit-card-validator.html`；用户会误以为还差位数而继续输入，或误判有效卡号无法识别。
- 方案：把 Luhn 通过与长度校验解耦；未知卡组织时按 13-19 位通用长度给出「Luhn 通过（卡组织未知）」，不再提示继续输入。

### F-N67 信用卡 Luhn 页 2 位数「00/18」也显示通过（低，确认缺陷）
- 描述：`luhnCheck` 只拒绝长度 <2，`validate` 也仅提示「至少需要 2 位」，对 2 位数字不做卡号长度约束；因此 `00`、`18` 等非卡号长度字符串会得到「✅ 卡号通过 Luhn 校验」，文案中的「卡号」与实际输入不符（页面虽有「仅校验算法」免责声明）。
- 证据：`tools/finance/credit-card-luhn.html:234`（长度门槛 2）、`:247`（静默剥非数字）、`:250-256`（≥2 位即输出「卡号通过」）
- 复现：输入 `00` → 实际「长度 2 位、Luhn ✅ 通过、✅ 卡号通过 Luhn 校验」；输入 `18` 同样通过（期望提示「位数不足，非有效卡号长度」或至少不称其为卡号通过）
- 影响：`tools/finance/credit-card-luhn.html`；校验器被当作卡号有效性判断时会产生误报。
- 方案：增加 12-19 位长度门槛（或把输出改为「该数字串通过 Luhn」），并在长度不足时明确标注「仅算法通过，非卡号」。

### F-N68 积分兑换价值页加钱超过商品价值仍输出负值并判「偏亏」（低，确认缺陷）
- 描述：`val`、`fee` 仅靠 `min="0"`，`num()` 对空值与非法值一律回 0，`calcTool` 只校验 `pts > 0`；当 `fee > val` 时 `netVal` 为负，页面照常展示负的「净得价值/每万分价值」，并给出「偏亏」，没有指出加钱换购已超过商品现金价值。
- 证据：`tools/finance/points-redemption-value.html:130,134`（仅属性 min）、`:251`（非法值回 0）、`:256-266`（仅校验 pts、直接算 `val - fee`）
- 复现：积分 10000、商品现金价值 20、加钱 30 → 实际「净得价值 −10.00 元、每万分 −10.00 元、偏亏」（期望提示「加钱已超过商品价值」并拒绝/归零）；商品价值填 −20 → 同样输出负值结果
- 影响：`tools/finance/points-redemption-value.html`；负价值会进入历史记录与对比柱状图，用户可能把异常输入当成正常结论。
- 方案：val、fee 限 ≥0 且 fee ≤ val（或越界时显式提示并停止计算）；空值/非法值给字段错误而非静默按 0。

### F-N69 金额大写页描述与实现不符：声称输出英文单词，实际为中文大写（低，确认缺陷）
- 描述：页面标题、meta description、og/twitter description 与英文副标题均写「转换为英文单词大写 / English words」，但 `convert()` 输出的是中文「壹仟…元…角…分」，英文态文案与功能不一致。
- 证据：`tools/finance/amount-in-words.html:41,43,45`（三处 description 写英文单词）、`:116`（英文副标题 English words）、`:268-277`（实现输出中文大写）
- 复现：输入 1234.56 → 实际「壹仟贰佰叁拾肆元伍角陆分」，而页面描述承诺「英文单词大写」（期望改文案为「中文大写金额」或真正输出英文单词）
- 影响：`tools/finance/amount-in-words.html`；英文态用户按描述预期英文支票写法，得到中文结果，SEO 摘要也与实际功能不符。
- 方案：将 description/副标题统一改为「中文大写金额（人民币）」；若需英文能力，另加语言切换或独立工具，不要在现页混写。

- 本轮实读 8 页：`tools/finance/amount-in-words.html`、`tools/finance/number-to-words-chinese.html`、`tools/finance/gold-price-calculator.html`、`tools/finance/shebeizulinfeilvjisuan.html`、`tools/finance/register-depreciation.html`、`tools/finance/credit-card-validator.html`、`tools/finance/credit-card-luhn.html`、`tools/finance/points-redemption-value.html`；新增 9 条（高 2/中 4/低 3）；未覆盖：其余 finance 页（约 78 页）未逐页复扫。
- 证据均由源码行号 + node 内存复算取得；未做浏览器、英文态、移动端、门禁与线上验证；历史已修声明未独立复验。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 页（`tools/finance/calc-2.html`、`tools/finance/calc-3.html`、`tools/finance/calc-4.html`、`tools/finance/calc-5.html`、`tools/finance/invoice-generator.html`、`tools/finance/currency-converter.html`、`tools/finance/analysis-5.html`、`tools/finance/analysis-risk.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证；历史已修声明未独立复验。

### F-N70 贷款月供页期限解析：0 年静默变 1 年、小数被截断、负年限产出「−60 期」（中，确认缺陷）
- 描述：`years = parseInt($('years').value)||1` 把 0 与空值都兜成 1 年；`parseInt` 直接丢弃小数（2.5 年按 2 年算）；负数不被拦截，`n = years*12` 为负，等额本息仍按负期数幂运算给出负月供，而 `for(i=1;i<=n;i++)` 一次都不执行，摘要照常显示「−60 期」「还款总额 0.00」「总利息 0.00」。
- 证据：`tools/finance/calc-4.html:226-230`（`:228` parseInt+兜底、`:230` n=years*12）、`:238`（循环条件）、`:249`、`:264`（期数回显）、`:128`（min 属性不拦截手输/清空）
- 复现：本金 100 万、年利率 4.2%、期限 0 → 实际 12 期、首月 85,241.31 元（期望提示期限须 ≥1 年或按 0 期处理）；期限 2.5 → 实际 24 期（期望 30 期）；期限 −5 → 实际「−60 期」、首月 −15,006.91 元、还款总额 0.00、明细表为空（期望字段级报错并停止计算）
- 影响：`tools/finance/calc-4.html`；合法的小数期限被无声压缩、0 年被放大成 1 年，负期限还会输出负月供与空明细，历史记录与 CSV 导出沿用同一 `n`。
- 方案：期限限 `>0` 且按「年×12」取整（或新增「月」输入并明确口径）；0/空/负/非数字给字段错误，不进入计算；分母 `n<=0` 时直接返回。

### F-N71 IRR 页无实根仍返回 1000% 并把 NPV≈0 写进结论（高，确认缺陷）
- 描述：`irr()` 的二分回退固定区间 `[-0.99, 10]`，只按 `npv(lo)*fmid<0` 决定 hi，从不校验两端异号，也不校验最终残差；当现金流虽有正负但 NPV 无实根时，`lo` 被单调推向 `hi`，直接返回 `mid≈10`（1000%）。页面随后以该利率复算明细，并在结果文案中断言「项目净现值 NPV 约等于 0」。
- 证据：`tools/finance/calc-2.html:244-251`（`:249` 仅按符号推进、`:251` 直接 `return mid`）、`:264`、`:288`（结论文案）
- 复现：初始投资 −100、各期现金流 230、−132.5（NPV = −100 + 230x − 132.5x²，判别式 52900−53000 < 0，无实根）→ 实际 IRR 1000.0000%、明细末期累计 NPV −7.29，页面仍写「当折现率为 1000.0000% 时，项目净现值 NPV 约等于 0」（期望提示「该现金流无实根，IRR 不存在」）
- 影响：`tools/finance/calc-2.html`；非常规/多重符号变化现金流的 IRR 被伪造成上限值，用户会据此接受实际不可行的项目；与 F-N29（npv-calculator）同类但属独立页面，修复需覆盖本页。
- 方案：迭代后校验 `|NPV|` 残差（如 <1e-6）且端点异号，否则返回 `null`；`null` 时结果区只提示「无实根/多根，请改用 NPV」，不再展示「NPV≈0」；文案补明多根情形。

### F-N72 NPV 页折现率 −100% 时 NPV 为 Infinity，仍判「项目可行」（中，确认缺陷）
- 描述：折现率只做 `parseFloat/100`，未限制 `r > −100%`。`r = −100%` 时 `1+r = 0`，`df = 1/0 = Infinity`，NPV 变为 Infinity；卡片经全局 `Infinity|NaN → —` 替换显示「—」，但 `conclusion` 在替换前按 `npv > 0` 判定，输出「项目可行（NPV > 0）」。`r < −100%` 时折现因子逐期变号，NPV 成为无经济意义的数字却照常给出结论。
- 证据：`tools/finance/calc-3.html:223`（读值）、`:229`（`1/Math.pow(1+r,i+1)`）、`:231`、`:236`（结论）、`:242-243`（渲染）
- 复现：初始 −100,000、折现率 −100%、五期 30,000 → 实际 NPV「—」、PI「—」、结论「项目可行（NPV > 0）」（期望拒绝或提示折现率必须 > −100%）；折现率 −150% → 实际 NPV −760,000、PI −6.60，仍按正常口径展示
- 影响：`tools/finance/calc-3.html`；非法折现率下结论方向与数值不一致，投资者会看到「可行」却没有可读的 NPV；与 F-N31（npv-calculator）同类但为独立页面。
- 方案：折现率限 `(−100%, 上限)`，越界标红并停止；结论只在 `isFinite(npv)` 时给出，否则显示「折现率非法，无法判断」。

### F-N73 NPV 页非数字现金流被静默丢弃，后续各期整体前移（中，确认缺陷）
- 描述：`parseFlows()` 用 `parseFloat` 后 `filter(n=>!isNaN(n))`，任何拼错/空段/中文占位都被直接删除且不占期号，导致其后的现金流整体提前一期，NPV 被系统性高估；输入框仅提示「逗号/空格/换行分隔」，无非法项反馈。
- 证据：`tools/finance/calc-3.html:219`（filter）、`:228-232`（按数组下标折现）、`:128`（输入提示）
- 复现：初始 −100,000、折现率 8%、输入 `30000, abc, 30000` → 实际按 2 期解析，NPV −46,502.06（若把 abc 记为 0，3 期应为 −48,407.25，差 1,905.19）；输入 `30000,,30000` 同样被压成 2 期
- 影响：`tools/finance/calc-3.html`；手工粘贴财报现金流时的空列/占位符会让期数错位，NPV 与 PI 偏乐观，且用户无从发现。
- 方案：按分隔符逐段解析，非数字段保留期号并按 0 处理（或整表报错并提示「第 N 项不是数字」）；不要用 `filter` 改变期序。

### F-N74 ROI 页投资成本为 0/负时 ROI 归零，净收益却照常计算（中，确认缺陷）
- 描述：`roi = cost>0 ? netProfit/cost : 0`，但 `netProfit = value - cost - extra` 对非正成本不做任何限制。成本 0 或负数时，「净收益」仍按公式得出非零金额，与同屏「总 ROI 0.00%」直接矛盾；负成本甚至会把成本额加进收益。
- 证据：`tools/finance/calc-5.html:215-220`（`:220` 三元兜底）、`:227-231`（摘要卡）、`:233`（结果文案）
- 复现：成本 0、最终价值 150,000、5 年 → 实际 净收益 150,000.00、总 ROI 0.00%、年化 0.00%；成本 −100,000、最终价值 150,000 → 实际 净收益 250,000.00、总 ROI 0.00%（期望拒绝非正投资成本）
- 影响：`tools/finance/calc-5.html`；无本金/录入负号时得到「零回报却大额盈利」的组合，复制与导出同样带出，历史记录会保存矛盾结果。
- 方案：`cost` 限 `>0`，非正给字段错误并停止；确实需要「无成本」场景时另设分支并把净收益同步置「—」，避免 ROI 与净收益两套口径。

### F-N75 ROI 页亏损超过本金时年化静默显示 0.00%（低，确认缺陷）
- 描述：年化只在 `years>0 && roi>-1` 时计算，否则 `annualized` 保持初值 0；但摘要卡在 `years>0` 时无条件渲染 `annualized*100`，于是 ROI ≤ −100% 时总 ROI 显示 −100%/−150%，年化却显示 0.00%，且正文 `annualText` 为空，两处口径不一致。
- 证据：`tools/finance/calc-5.html:221-226`（`:223` 条件）、`:227-231`（`:230` 摘要无条件展示）
- 复现：成本 100,000、最终价值 0、5 年 → 实际 总 ROI −100.00%、年化回报率 0.00%（期望「—」或明确「亏损超过本金，无法按复利年化」）；最终价值 −50,000 → 总 ROI −150.00%、年化仍 0.00%
- 影响：`tools/finance/calc-5.html`；本金全损/倒亏的方案被显示成「年化零回报」，与结果正文缺少年化行相互掩盖，容易被误读为保本。
- 方案：年化仅在 `1+roi>0` 时输出；否则卡片显示「—」并在正文提示无法复利年化，或直接给出 −100% 并注明口径。

### F-N76 价税分摊页单张限额为 0 触发无限循环，页面冻结（高，确认缺陷）
- 描述：`getVal()` 对空值/非法值一律回 0，`count = Math.ceil(total/limit)` 在 `limit=0` 时为 `Infinity`；`count<=1` 不成立，等额拆分进入 `for(i=1;i<=Infinity;i++)` 无限追加发票，最大化与最后一张较小分支的 `while(remaining>limit)` 因剩余额永不减少同样死循环。`min="1"` 只约束步进器，清空输入或直接键入 0 均可触发。
- 证据：`tools/finance/invoice-generator.html:229`（min 属性）、`:512-515`（getVal 兜底 0）、`:563`（count）、`:568-573`（等额 for 循环）、`:577-581`（max while）、`:589-597`（lastsmall while）
- 复现：总金额 100,000、清空「单张限额」（或填 0）→ 实际标签页立即卡死、无任何输出（期望提示「单张限额必须大于 0」）；填 0.0001 时 `count=10⁹` 级，同样长时间无响应
- 影响：`tools/finance/invoice-generator.html`；普通输入即可挂死标签页，移动端可能因数组无限增长而 OOM 崩溃，属工具不可用级缺陷。
- 方案：`limit` 校验 `>0`（并设合理上限，如不超过总金额）；`count` 超过阈值（如 1000 张）时拒绝并提示；在三个拆分分支入口统一做 `if(!isFinite(count) || count>MAX) return`。

### F-N77 反推税额页税额超过含税金额仍输出负不含税与 0% 税率（中，确认缺陷）
- 描述：反推分支直接 `excl = total - tax`，仅当 `excl > 0` 才计算税率；`tax > total` 时不含税为负值，税率静默变为 0，页面仍渲染「不含税 −5,000.00」「反推税率 0.0000%」及公式行，复制/CSV 同样带出。
- 证据：`tools/finance/invoice-generator.html:275-276`（min 属性不拦截手输）、`:688-700`（`:691` excl、`:692` rate 兜底）、`:838-839`（回显与公式）
- 复现：含税金额 10,000、税额 15,000 → 实际 不含税 −5,000.00、反推税率 0.0000%，公式行显示「15,000.00 ÷ −5,000.00 × 100% = 0.0000%」（期望提示「税额不得超过含税金额」并停止）
- 影响：`tools/finance/invoice-generator.html`；负不含税与 0% 税率是相互矛盾的财务口径，用户可能据此填错开票信息。
- 方案：校验 `0 ≤ tax ≤ total`，越界标红停止；`excl === 0` 时提示「不含税为 0，无法反推税率」，不要输出 0%。

### F-N78 货币换算页手动汇率不区分币种对，反向仍做乘法（高，确认缺陷）
- 描述：`convert()` 在手动汇率模式下直接 `return amount * mr`，既不判断 from/to 方向，也不使用传入的币种代码；因此反向换算（`calcReverse` 传入 `to→from`）仍乘同一个 mr，任意币种对（USD→JPY、EUR→GBP 等）也都套用同一数值。速查表、批量换算、历史重算全部复用该函数。
- 证据：`tools/finance/currency-converter.html:542-547`（`:544` 直接乘）、`:637-642`（反向调用）、`:531-533`（速查表双向）、`:647-652`（同屏正反汇率）、`:776`（批量）
- 复现：手动汇率 0.138（1 CNY = 0.138 USD），100 CNY → 实际 13.80 USD（正确）；把 13.80 填回「到」做反向 → 实际 1.9044 CNY（期望 100）；切 USD→JPY 后 100 美元 → 实际 13.80 日元（期望约 1.47 万日元）；速查表同屏出现「1 USD = 0.138 CNY」与「1 CNY = 0.138 USD」两条互斥结论
- 影响：`tools/finance/currency-converter.html`；手动汇率本用于按当日牌价精确换算，却对反向与跨币种给出数量级错误，且页面仍标注「手动汇率（你填写）」让用户误信。
- 方案：手动模式区分方向（FROM→TO 乘 mr，TO→FROM 除 mr）；手动汇率只对当前选中的币种对生效，其他币种对退回内置表并在来源说明中标明；速查表在手动模式下切换为内置表或显式提示「仅当前币种对」。

### F-N79 偿债比率页权益为负仍计算并标「偏低」，与 FAQ 声明相反（中，确认缺陷）
- 描述：产权比率与权益乘数只在 `equity !== 0` 时置 NaN，权益为负仍照算负值；`tagHigh()` 对负值落入 `v<=low` 分支显示「偏低」，于是资不抵债企业被标成「偏低」而非「无法计算」。同一 `tagHigh(de,1,2,2)` 还把 de<1 的稳健区间标成「偏低」，与同行参考文案「< 1 稳健」自相矛盾。FAQ 明确写「权益为负时…页面会显示『无法计算』并给出提示」，实现未遵循。
- 证据：`tools/finance/analysis-5.html:253-256`（`:255-256` 仅判 `!==0`）、`:282-283`（tagHigh 调用与文案）、`:201`（FAQ 声明）、`:308-309`（负权益提示）
- 复现：资产总额 1,200,000、负债总额 1,500,000（所有者权益 −300,000）→ 实际 资产负债率 125.00%、产权比率 −5.00（判定「偏低」）、权益乘数 −4.00（判定「偏低」）（期望「—/无法计算」）；健康企业 de=0.5 → 判定「偏低」（参考文案应为「稳健」）
- 影响：`tools/finance/analysis-5.html`；资不抵债的极端信号被「偏低」弱化，且档位标签与参考文案不一致，信贷/授信场景下可能被误读。
- 方案：`equity <= 0` 时 de/em 置 NaN 显示「无法计算」并保留现有提示；产权比率改用四档判定（<1 稳健 / 1~2 一般 / 2~3 偏高 / >3 警戒），不要复用 `tagHigh(v,1,2,2)`。

### F-N80 杠杆页 EBIT=0 时提示仍称「DFL = 1」，与同屏「—」矛盾（低，确认缺陷）
- 描述：`dfl` 在 `ebit===0` 时置 NaN，但提示分支先判 `i===0`；当 EBIT 恰为 0（盈亏平衡）且利息为 0 时，页面输出「利息费用为 0，DFL = 1，EPS 只受经营杠杆影响（DCL = DOL）」，而同屏 DOL/DFL/DCL 三张卡均为「—」。
- 证据：`tools/finance/analysis-risk.html:239`（读入）、`:244-247`（`:246` ebit===0 → NaN）、`:284-285`（i===0 优先提示）
- 复现：营业收入 1,000,000、变动成本 600,000、固定成本 400,000（EBIT=0）、利息 0、税率 25%、股数 100,000 → 实际 DOL「—」、DFL「—」、DCL「—」、EPS 0.00，提示仍写「DFL = 1」（期望提示「EBIT 为 0，杠杆系数无定义」）
- 影响：`tools/finance/analysis-risk.html`；盈亏平衡点是敏感性分析的关键场景，提示语与实际数值相反，会误导用户认为财务杠杆安全。
- 方案：提示按 `ebit===0` 优先判定并说明杠杆系数无定义；仅在 `i===0 && ebit!==0` 时提示 DFL=1。

- 本轮实读 8 页：`tools/finance/calc-2.html`、`tools/finance/calc-3.html`、`tools/finance/calc-4.html`、`tools/finance/calc-5.html`、`tools/finance/invoice-generator.html`、`tools/finance/currency-converter.html`、`tools/finance/analysis-5.html`、`tools/finance/analysis-risk.html`；新增 11 条（高 3/中 6/低 2）；未覆盖：其余 finance 页（约 66 页）未逐页复扫。
- 证据均由源码行号 + node 内存复算取得；未做浏览器、英文态、移动端、门禁与线上验证；历史已修声明未独立复验。

## 2026-11-04 续查（并行批 O）

> 范围：本轮阅读 8 页（`tools/finance/analysis-44.html`、`analysis-cost-1.html`、`assessor-manager.html`、`report-1.html`、`generator-report-1.html`、`number-to-words.html`、`currency-lookup.html`、`credit-card-bin.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证；历史已修声明未独立复验。

### F-N81 报表合并页：简化抵销分录借贷不平，差额等于合并价差（高，确认缺陷）
- 描述：抵销分录把「长期股权投资」贷方只记母公司享有份额 `parentShare`，而不是全额长期股权投资 `inv`；商誉 / 负商誉又在分录里单独列示，于是借方合计与贷方合计相差恰好 `diff`，分录永远不平。
- 证据：`tools/finance/report-1.html:267-275`（`:271` 贷方金额为 `parentShare`；`:273-274` 商誉 / 负商誉另起一行）
- 复现：默认 长期股权投资 800,000、持股 80%、实收资本 500,000、未分配利润 200,000、增值 0 → 实际借方 500,000+200,000+240,000（商誉）=940,000，贷方 560,000+140,000=700,000，差 240,000（期望贷方「长期股权投资」800,000，借贷均 940,000，`node` 复算差值为 `diff`）
- 影响：`tools/finance/report-1.html`；页面自称「最简抵销分录便于对照账务处理」，但任何有商誉的合并都做不出平衡分录，直接抄进底稿会造成试算不平。
- 方案：贷方「长期股权投资」改用全额 `inv`；商誉借记 `diff`、负商誉贷记 `-diff`（按准则计入营业外收入或调整留存收益），并补一条借贷合计行自校验。

### F-N82 信用评估页：负值/空值资产负债率拿满分，评级与授信额度虚高（中，确认缺陷）
- 描述：六个输入统一用 `+value||0` 读入，负数与空串都落到合法档位；资产负债率 `dr<=50` 得 25 分（六项中权重最高），因此「负债率留空」或填 `-20` 都拿满档得分，进而把评级推到 AAA 并给出 0.3 倍营收的授信额度。
- 证据：`tools/finance/assessor-manager.html:201`（`+document.getElementById('debtRatio').value||0`）、`:205`（`dr<=50?25`）、`:209`（`od<=1?10` 使 `-5` 次逾期得 10 分）、`:214-215`（系数与额度）、`:188-190`（说明称「财务指标 75% + 信用记录 25%」，与 `:204-211` 六项直接累加不符）
- 复现：资产负债率 −20、流动比率 1.8、营收 5,000 万、净利率 12%、逾期 1 次、信用历史 5 年 → 实际 85 分 AAA、授信 1,500 万元（期望拒算或按「未知」给中性分）；资产负债率清空 → 按 0 计，得 25 分满档
- 影响：`tools/finance/assessor-manager.html`；负值与缺失值被当作「最优偿债能力」，贷前初筛方向性错误；说明文案的 75/25 加权口径也与实现相反。
- 方案：逐项做有限性与非负校验（`dr` 需 0–100、`cr`/`rev`/`pm`/`ch` 需 ≥0、`od` 需 ≥0 整数），空白不得落入最优档；同步把说明改成「六项分档直接累加」。

### F-N83 数字转英文页：±1e12 越界未拦截，输出退化成「one」/「minus one」（中，确认缺陷）
- 描述：范围守卫用 `Math.abs(n) > 1e12`，恰好 `1e12` 通过校验；`scales` 只到 `billion`，`1e12` 分成 5 段后 `scales[4]` 为 `undefined`，单位被静默丢弃，只剩首段 `one`。
- 证据：`tools/finance/number-to-words.html:321-324`（`> 1e12` 判据）、`:245`（`scales` 仅 4 项）、`:287-293`（`scale = scales[maxScale-i]`，`scale` 为空则拼接空串）
- 复现：输入 `1000000000000` → 实际 `one`（期望拒绝并提示或输出 `one trillion`）；`-1000000000000` → `minus one`；`999999999999` 正常输出 `nine hundred ninety-nine billion …`
- 影响：`tools/finance/number-to-words.html`；页面声明支持到 999,999,999,999，边界值却静默变成「one」，用于票据大写会直接写错金额。
- 方案：守卫改为 `>= 1e12`（或补 `trillion` 并相应扩大上限），越界统一走现有「超出范围」提示。

### F-N84 成本分摊页：综合单位成本分母吞掉非数字与负产量，与逐行「—」口径冲突（中，确认缺陷）
- 描述：产量条数与对象条数相同时即置 `qtyOk`，`sumQty` 只累加有限值且不排除负数，`unitTotal` 直接 `total/sumQty`；逐行单位成本却要求 `q>0`。于是同一张表里出现「合计产量按正负相抵后计算、个别行显示—」的自相矛盾结果，且负产量会缩小分母、抬高综合单位成本。
- 证据：`tools/finance/analysis-cost-1.html:273-277`（`qtyOk` 只比条数、`sumQty` 累加有限值）、`:291-293`（逐行 `q>0` 才折算）、`:295`（合计行展示 `unitTotal`）
- 复现：总成本 120,000、基数 300/500/200、产量 `1500,-500,1000` → 实际合计产量 2,000、综合单位成本 60.00，B 行单位成本「—」（期望出现负产量时提示并从分母剔除或拒算，不应把 2,000 当有效产量）；产量 `1500,abc,1000` → 综合 48.00，B 行同样「—」
- 影响：`tools/finance/analysis-cost-1.html`；综合单位成本是定价底线的主要依据，分母被负数或非法值污染后单价失真，且提示区仍显示「单位成本已按分摊额 ÷ 产量折算」。
- 方案：`qtyOk` 追加「全部为有限数且 `>=0`」；任一产量非法或为负即整体降级为「—」并给出提示；负值需明确是否允许冲减。

### F-N85 投资偏差页：批量模式接受负计划投资，−220% 判定成「明显节约」（中，确认缺陷）
- 描述：单笔 `calc()` 拦截 `plan<=0`，批量 `calcBatch()` 只校验 `isFinite`，负计划投资照样进入 `analyze()`；负数分母把超支翻成负偏差率，命中 `rate<-5` 分支后被判定为「明显节约」，CPI 也显示为负值。
- 证据：`tools/finance/analysis-44.html:203`（`analyze` 分档逻辑）、`:205`（单笔有 `plan<=0` 守卫）、`:206`（批量无守卫）
- 复现：批量行 `X,-500,600` → 实际 偏差额 1,100、偏差率 −220.00%、CPI −0.8333、判定「明显节约」（期望提示「计划投资需大于 0」并跳过该行）
- 影响：`tools/finance/analysis-44.html`；多项目台账里一条负计划（录入符号错误）会被读成节约，抵掉真实超支，纠偏结论反向。
- 方案：批量内对 `pl<=0` 的行跳过并在表格下汇总提示；`cpi<=0` 显示「—」。

### F-N86 报表生成页：生成数量为负时输出空白，0 与超限被静默替换（低，确认缺陷）
- 描述：`Math.min(+cnt||5,50)` 只做上限截断，负值原样进入 `for (i=1; i<=n)` 循环，一条也不生成；`0` 因 `||5` 变成 5 条，`100` 静默变成 50 条，页面都不回显实际取值。
- 证据：`tools/finance/generator-report-1.html:195`（`n` 计算）、`:197`（循环条件）、`:120`（`min="1" max="50"` 仅约束步进器）
- 复现：数量 `-3` → 实际结果区只剩「财务报表示例生成结果：」而无任何报表（期望提示 1–50 或按 1 条生成）；`0` → 静默 5 条；`100` → 静默 50 条
- 影响：`tools/finance/generator-report-1.html`；负值下用户看到空结果区却无任何错误提示，容易误判工具故障；静默改数也让「生成 50 条」与「生成 100 条」无法区分。
- 方案：读入后 `if(!(n>=1&&n<=50))` 走提示并 return，或在结果区标注「已按 50 条上限生成」。

### F-N87 货币查询页：最小单位位数说明缺右括号（低，确认缺陷）
- 描述：单结果分支拼装「最小单位位数」时只有左括号，`（` 与 `</p>` 之间缺少 `）`，页面直接渲染出未闭合的半句。
- 证据：`tools/finance/currency-lookup.html:302`
- 复现：输入 `USD` → 实际「最小单位位数：2（1/100」（期望「2（1/100）」）；输入 `JPY` → 「0（无小数」
- 影响：`tools/finance/currency-lookup.html`；输出被复制到单据说明时格式残缺，观感上像程序报错。
- 方案：`…（${r.minor === 0 ? '无小数' : '1/' + Math.pow(10,r.minor)}）</p>` 补齐括号。

### F-N88 信用卡 BIN 页：MIR 卡恒被判为 Mastercard，2721 起仍算 Mastercard（低，确认缺陷）
- 描述：网络探测按数组顺序首个命中即返回；Mastercard 正则 `^(5[1-5]|2[2-7]\d{2})` 覆盖 2200–2799，排在 MIR（`^220[0-4]`）之前，导致 MIR 分支永远不可达；同时 2721–2799 本不属于 Mastercard 2 系列也被判为 Mastercard。
- 证据：`tools/finance/credit-card-bin.html:257-267`（`:259` Mastercard 正则、`:266` MIR 正则、`:268-271` 顺序返回）
- 复现：输入 `220012`（MIR BIN）→ 实际「卡片网络：Mastercard」（期望 MIR）；`272100` → 实际「Mastercard」（期望 未知网络或按真实 BIN 归属）
- 影响：`tools/finance/credit-card-bin.html`；风控路由会按错误卡组织处理 MIR 卡，且页面「按前缀推断网络」的承诺在 2 系列上不成立。
- 方案：Mastercard 改为 `^(5[1-5]|22(2[1-9]|[3-6]\d|7[01]\d|720))` 精确到 2221–2720，并把 MIR / Maestro 等具体品牌移到泛匹配之前。

### F-N89 报表合并页：持股 0% 仍确认全额商誉（中，确认缺陷）
- 描述：持股比例只校验 0–100 范围，0% 视为合法；此时母公司享有份额为 0、少数股东权益等于全部净资产，合并价差等于全额长期股权投资并被展示为「商誉」，与「不纳入合并范围」的会计常识相反。
- 证据：`tools/finance/report-1.html:242-245`（仅范围校验）、`:247-250`（`parentShare`/`minority`/`diff`）、`:284-285`（商誉提示）
- 复现：持股 0%、长期股权投资 800,000、实收 500,000、留存 200,000 → 实际 母公司享有 0、少数股东权益 700,000、合并价差 800,000「确认为商誉」（期望 pct=0 提示参数无效，或直接提示无合并范围）
- 影响：`tools/finance/report-1.html`；0% 持股是常见录入错误，页面却输出一份看似完整的商誉测算，且抵销分录同为不平（叠加 F-N81）。
- 方案：`pct<=0` 直接提示「持股比例需大于 0」并清空结果区；`pct===100` 已有提示可保留。

### F-N90 报表合并页：深度解析算例的合并价差与所列参数对不上（低，确认缺陷）
- 描述：算例称「评估增值改 50,000、持股降到 60%、净利润改 −20,000」后合并价差为 −130,000，但长期股权投资仍为 800,000，母公司享有 330,000，按页面公式 `diff = inv − parentShare` 应为 +470,000；−130,000 只有在 `inv=200,000` 时成立，而该改动未在算例中说明。
- 证据：`tools/finance/report-1.html:192`（算例文本）、`:250`（`diff=inv-parentShare`）
- 复现：按算例文字只改增值/持股/净利润 → 实际合并价差 +470,000（商誉），期望 −130,000（负商誉），两者方向相反
- 影响：`tools/finance/report-1.html`；读者按算例复算会对不上，误以为公式或页面出错，削弱对工具结果的信任。
- 方案：算例显式写出「长期股权投资同时改为 200,000」，或按 `inv=800,000` 重算为 +470,000 商誉。

- 本轮实读 8 页：`tools/finance/analysis-44.html`、`tools/finance/analysis-cost-1.html`、`tools/finance/assessor-manager.html`、`tools/finance/report-1.html`、`tools/finance/generator-report-1.html`、`tools/finance/number-to-words.html`、`tools/finance/currency-lookup.html`、`tools/finance/credit-card-bin.html`；新增 10 条（高 1/中 5/低 4）；未覆盖：其余 finance 页（约 58 页）未逐页复扫。

## 2026-11-04 续查（并行批 O-P2）

范围：复读 `tools/finance/` 下 8 页（mortgage-calculator、mortgage-prepayment、housing-fund-loan、salary-calculator、simple-interest、tax-bracket、tax-calculator、vat-calculator），编号 F-N91~F-N113。说明：这 8 页在更早批次已有部分条目（F-N11/N12/N15/F-N18–N21/F-N26–N28），本段只记录本次复读新增或由旧修法引入的问题，不重复旧条目；F-N81~F-N90 段未改动。

### F-N91 提前还款页：原方案以「输入月供 × 剩余期数」为基准，未提前还款也会凭空产生「节省」（高，确认缺陷）
- 问题：`totalBefore = mp * months`，直接拿用户填写的月供当整段剩余期限的应还月供；当 mp 高于按本金/利率/期数算出的应还月供时，基线总额被放大，即使提前还款为 0，两条方案也会显示「缩短期限 / 降低月供」和巨额「节省」。
- 证据：`tools/finance/mortgage-prepayment.html:302-304`（基线）、`:306-308`（仅对 mp 低于应还月供告警）、`:328-334`（节省额）、`:340-346`（结论）
- 复现：本金 50 万、年利率 0%、240 期、月供 3,000、提前还款 0 → 页面「原方案总利息 220,000.00 元」、①节省 220,000.00、②节省 220,000.00；0% 利率实际总利息应为 0，期望节省 0。另一组：本金 50 万、4.5%、240 期、月供 4,000、提前还款 0 → 基线总还款 960,000、利息 460,000、①节省 284,000、②节省 200,820.75；按应还月供 3,163.25 的基线总还款应为 759,180、利息 259,180，无提前还款时两方案节省均应为 0。
- 影响：`tools/finance/mortgage-prepayment.html`；这是 F-N26「以输入月供为基准」修法引入的回归，用户只要把月供填得比实际高，就会得到一份虚高的「提前还款收益」，直接影响是否提前还款的决策。
- 方案：基线改为「应还月供 × 剩余期数」（应还月供由本金/利率/期数计算），或在 mp≠应还月供时同时给出 mp 对应的真实剩余期数并强制二次确认；`mpWarn` 应对高于应还月供同样告警。

### F-N92 提前还款页：月供低于应还月供时「②降低月供」反而升月供，原方案总利息为负（中，确认缺陷）
- 问题：①按输入的 mp 继续摊还，②按剩余本金/剩余期数重算月供；当 mp 低于应还月供时，②算出的月供可能高于用户填写的月供，标签「降低月供」与结果相反；同时基线 `mp×months` 可小于本金，得出负的「原方案总利息」，节省额为负仍按绿色展示。
- 证据：`tools/finance/mortgage-prepayment.html:302-304`（基线）、`:316-324`（② reduceMonthly）、`:328-334`（节省额与颜色）
- 复现：本金 50 万、4.5%、240 期、月供 2,000、提前还款 20,000 → ②月供 3,036.72（比输入的 2,000 更高）、原方案总利息 −20,000.00、①节省 −772,000.00（绿色）；期望 ②月供不高于当前输入（或明确提示按应还月供 3,163.25 重算），且总利息不得为负、负节省不得标绿。
- 影响：`tools/finance/mortgage-prepayment.html`；低收入月供场景会出现「越提前还越亏」的假结论，且把负利息当成正常基准。
- 方案：先校验 mp 是否覆盖当期利息并给出「无法按该月供还清」/「月供不足以覆盖利息」的阻断；负节省改为红色并追加「相较应还月供仍多付利息」的说明。

### F-N93 提前还款页：0% 利率下剩余期数为小数且原样展示（中，确认缺陷）
- 问题：`remainingMonths` 在月利率为 0 时直接 `return p / pmt`，未取整；`saveMonths`、`totalShort` 继续使用小数，页面把 `166.66666666666666`、`73.33333333333334` 这类浮点原样拼进结论。
- 证据：`tools/finance/mortgage-prepayment.html:243-245`（0 利率分支）、`:311-313`（totalShort/saveMonths）、`:352-354`（剩余期数文案）
- 复现：本金 50 万、年利率 0%、240 期、月供 3,000、提前还款 0 → 「剩余期数 166.66666666666666 个月（缩短 73.33333333333334 个月）」；期望显示 167 期（最后一期不足额）或按整数期摊销，而不是原始浮点。
- 影响：`tools/finance/mortgage-prepayment.html`；0% 是合法的边界输入（页面校验允许 0–100），结论区出现一串小数会被当成程序异常，且「166.67 期」在还款计划上没有意义。
- 方案：0 利率分支改为 `Math.ceil(p / pmt)` 并单独计算末期还款；所有期数展示统一 `Math.round/ceil`，`totalShort` 用整数期×mp（末期不足额时再回冲）。

### F-N94 提前还款页：「导出明细 CSV」导出的是历史表，不含两方案明细（低，确认缺陷）
- 问题：按钮文案为「导出明细 CSV」，实际调用 `exportTable('#mortgage_prepaymentTable')`，该表是 TBKit 自动历史表（时间 + 输入 + 结果字符串），不是「缩短期限 / 降低月供」的逐期现金流，也不是当前方案的对比明细。
- 证据：`tools/finance/mortgage-prepayment.html:140`（按钮）、`:405`（历史表渲染）、`:463`（导出目标）
- 复现：计算 50 万/4.5%/240 期/月供 3,163.25/提前还款 0 → 点「导出明细 CSV」，文件列为时间、本金、利率、期数、月供、提前还款、结果摘要；期望包含两种方案各自的剩余期数、月供、总还款、总利息、节省额，或直接导出逐期摊销表。
- 影响：`tools/finance/mortgage-prepayment.html`；用户拿到的「明细」无法复核或留档，和页面主打的「两种方案对比」不匹配。
- 方案：新增隐藏的 `#mortgage_prepaymentDetail` 表输出两方案对比与逐期计划，导出该表；历史表另设「导出历史 CSV」按钮。

### F-N95 房贷计算页：非法首付只清空数字、不留提示，且饼图保留上次比例（低，确认缺陷）
- 问题：首付比例 <0 或 ≥100 时直接 `resetDisplay()` 返回，没有任何错误文案；`resetDisplay` 只把数字节点置 `--`，没有重置 `#pieChart` 的 `background`（conic-gradient），上一次的本金/利息扇形继续显示。
- 证据：`tools/finance/mortgage-calculator.html:355-359`（非法分支）、`:433-438`（resetDisplay 未含饼图）、`:417-419`（饼图写入）
- 复现：默认 100 万/30 年/4.2%/首付 30% 计算后，把首付改为 120 → 月供、总利息、贷款总额等变 `--`，但饼图仍是上次的 70 万本金/利息比例，页面无「首付比例须 0–100%」提示；期望提示并清空/重置饼图。
- 影响：`tools/finance/mortgage-calculator.html`；用户可能误以为饼图仍是新参数的结果，且不知道为何结果消失。
- 方案：非法分支在结果区写入明确文案；`resetDisplay` 同时 `pie.style.background=''` 并隐藏/置灰饼图。

### F-N96 公积金贷款页：利率写死 3.1% 且标注「2024 年参考」，已高于 2024-05-18 起的 2.85%（中，确认缺陷）
- 问题：页面把首套公积金贷款利率固定为 3.1%，正文、深度解析和脚本常量三处一致，但 2024-05-18 起 5 年以上首套公积金贷款利率已下调至 2.85%（此后是否再调以官方为准）；用 3.1% 估算会系统性高估月供与总利息。
- 证据：`tools/finance/housing-fund-loan.html:205`（提示）、`:233`（深度解析）、`:237`（算例）、`:292`（`RATE = 0.031`）
- 复现：贷款 75 万、30 年：页面 3.1% → 月供 3,202.62 元、总利息 402,944.28 元；按 2.85% → 月供 3,101.68 元、总利息 366,604.94 元（月供高估 100.94 元、总利息高估 36,339.34 元）。深度解析算例「月供≈3202、总利息≈40.3 万」同样只对 3.1% 成立。
- 影响：`tools/finance/housing-fund-loan.html`；这是购房预算的主结果，利率口径过期会让用户高估还款压力，且「2024 年参考」的标注本身与 2024 年 5 月后的政策不符。
- 方案：把利率做成可选（2.85%/2.6%/自定义）或至少更新常量与文案并注明生效日期；深度解析算例同步重算（2.85% 下月供约 3,102、总利息约 36.7 万）。

### F-N97 公积金贷款页：负余额/负房价时依据行显示负额度，最终额度却按 0（低，确认缺陷）
- 问题：余额、房价只做 `parseFloat(...) || 0`，未拒绝负数；依据表按原值计算并展示负的「余额×N 倍」「房价 80%」，随后 `maxLoan < 0` 被夹到 0，同一结果区出现「−120 万」与「最高可贷 0 万」的矛盾。
- 证据：`tools/finance/housing-fund-loan.html:300-317`（取值与 clamp）、`:357-358`（依据行）
- 复现：余额 −8 万、房价 300 万、北京 15 倍 → 依据行「余额 × 15 倍 −120.0 万」「房价 80% 240.0 万」，最高可贷 0.0 万；期望负余额直接提示无效或按 0 展示，不应出现负额度行。
- 影响：`tools/finance/housing-fund-loan.html`；负数是常见录入错误，页面既不报错又给出自相矛盾的两组数字。
- 方案：`balance < 0 || housePrice < 0` 时提示并清空结果；或在计算依据行前先 `Math.max(0, ...)`，保证展示与最终额度同口径。

### F-N98 工资计算页：切到「年薪」后五险基数仍取月薪默认值，默认输入直接得到负到手（高，确认缺陷）
- 问题：年薪模式只把 `salaryInput` 当作年度收入并除以月数得到 `monthlySalary`，但五险/公积金基数输入仍是月度默认 20000，未随年薪换算；`baseSalary = getNum('baseSalary') || monthlySalary` 又因输入已有值而继续按 20000 扣费。默认薪资 20000 直接点「年薪计算」时，年收入 20000 却按年社保 54000 扣除，税后年收入为负。
- 证据：`tools/finance/salary-calculator.html:220`（五险基数默认 20000）、`:224`（公积金基数默认 20000）、`:583-596`（月/年换算与基数取值）、`:640-650`（年社保/年税/年净收入）
- 复现：保持默认薪资 20000，点「年薪计算」→ 月薪 1,666.67、月五险仍 4,500、年五险 54,000、年税 0、税后年收入 −34,000；期望年薪模式把基数按「年薪÷12」换算（或提示基数按月填写并给出 20000/12 示例），至少不能输出负收入。另一组：年薪 120,000、基数仍 20,000 → 年净 66,000；若基数随年薪变 10,000，年净 93,000，差 27,000。
- 影响：`tools/finance/salary-calculator.html`；切模式是首屏最常见的操作，默认状态即出现不可能的负工资，用户会直接不信任整页结果。
- 方案：年薪模式进入时把基数输入按 `年薪/12` 回填（或新增「基数按月/按年」单选）；`baseSalary <= 0` 或基数高于月薪时给出提示，禁止静默沿用旧值。

### F-N99 工资计算页：年薪模式下明细卡、税负率、到手比例、柱状图仍按月口径（中，确认缺陷）
- 问题：hero 的税前/个税/五险/税后四项在年薪模式切到年度值（且年度税含年终奖），但「税前工资/个税/税后到手」明细卡、`effectiveRate`、`takeHomeRate`、柱状图始终用 `monthlySalary / monthlyTax / netMonthly`，同屏混用月度和年度口径。
- 证据：`tools/finance/salary-calculator.html:663-672`（明细卡固定月值）、`:675-677`（三项比例固定月值）、`:684`（柱状图固定月值）、`:640-650`（年度值）
- 复现：年薪 240,000、年终奖 60,000、默认基数/专项 → hero 年税 11,880、税后 234,120；同屏明细仍「税前工资 20,000 / 个税 490 / 到手 15,010」，实际税负 2.5%（年度 3.96%）、到手比例 75.1%（年度 78.04%）。
- 影响：`tools/finance/salary-calculator.html`；用户在同一屏看到「税后年薪 234,120」和「税后到手工资 15,010」，无法判断哪个是最终结论，年终奖的税负也被比例卡忽略。
- 方案：年薪模式下明细卡改用年度四项（或明确加「月均」前缀），税负率/到手比例按 `annualTax/annualSalary`、`annualNet/annualSalary` 计算，柱状图改用年度金额。

### F-N100 工资计算页：每年工作月数≠12 时，社保按 N 月、起征点/专项固定按 12 月（低，确认缺陷）
- 问题：`annualInsurance = totalInsuranceMonthly * monthsPerYear`，但 `annualTaxable = annualSalary - annualInsurance - threshold * 12 - totalSpecialMonthly * 12`；当用户把「每年工作月数」改为 13 等非 12 值时，年度扣除口径不一致。
- 证据：`tools/finance/salary-calculator.html:583-584`（读取月数/起征点）、`:640-641`（年社保与年应税）
- 复现：月薪 20,000、每年工作月数 13、无年终奖 → 年社保 58,500，起征点仍 60,000、专项仍 42,000，年应税 99,500、税 7,430；若起征点/专项也按 13 月（65,000/45,500），年应税 91,000、税 6,580，差 850 元。
- 影响：`tools/finance/salary-calculator.html`；13 薪/季节性用工场景的年度个税会被高估，且与「每年工作月数」输入的语义矛盾。
- 方案：起征点与专项扣除同样乘以 `monthsPerYear`，或把该输入限定为 12 并说明只影响社保月数。

### F-N101 工资计算页：基数/起征点/月数输入 0 被 `||` 兜底成默认值，无法表达「基数为 0」（低，确认缺陷）
- 问题：`getNum('monthsPerYear') || 12`、`getNum('threshold') || 5000`、`getNum('baseSalary') || monthlySalary` 等把合法的 0 当成空值；用户想把五险基数设为 0（自由职业/不缴社保）时，实际仍按月薪扣费。
- 证据：`tools/finance/salary-calculator.html:583-584`、`:595-596`
- 复现：月薪 20,000，把五险基数改为 0 → 实际仍按 20,000 扣 4,500；期望 0 作为合法基数（或显式提示「0 将回退为工资基数」）。
- 影响：`tools/finance/salary-calculator.html`；无法模拟无社保/低基数场景，且用户不知道自己填的 0 被忽略。
- 方案：改用 `v !== '' && isFinite(v)` 判断，0 按 0 参与计算；仅在真正空值时回退默认。

### F-N102 单利计算页：「导出明细 CSV」导出历史表，年度现金流明细不可导出（低，确认缺陷）
- 问题：按钮文案「导出明细 CSV」，实际 `exportTable('#simple_interestTable')` 导出的是 TBKit 自动历史表；「每年取息」现金流表是直接拼进 `#resultBox` 的 HTML，没有独立 id，无法被导出。
- 证据：`tools/finance/simple-interest.html:191`（按钮）、`:342-356`（年度现金流表）、`:476`（导出目标）
- 复现：本金 10,000、年利率 5%、3 年、每年取息 → 结果区显示 3 行年度利息 + 合计 1,500；点「导出明细 CSV」得到时间/本金/利率/年限/模式/结果摘要，无任何年度现金流行；期望导出 3 行明细与合计。
- 影响：`tools/finance/simple-interest.html`；年度取息是页面的主卖点之一，导出的却是历史记录，留档价值低。
- 方案：给年度现金流表加 `#simple_interestDetail`，导出该表；历史表另设「导出历史」按钮。

### F-N103 单利计算页：清空后历史表/趋势图/差异框仍保留旧记录（低，确认缺陷）
- 问题：`clearAll()` 只清空输入和 `#resultBox`，未清 `#simple_interestTable`、`#simple_interestDiff`、`#simple_interestChart` 中已渲染的旧数据；结果区显示「请输入数据」，下方仍是上一次的计算记录。
- 证据：`tools/finance/simple-interest.html:364-369`
- 复现：计算 10,000/5%/3 年后点「清空」→ 结果区变「请输入数据」，但历史表仍有刚才的记录、趋势图仍显示旧柱；期望一并清空或提示「历史记录保留」。
- 影响：`tools/finance/simple-interest.html`；清空动作与可见状态不一致，用户可能把旧记录当成新结果。
- 方案：`clearAll` 同时清空三处容器（历史表可保留但需明示「历史记录未清空，可到下方删除」）。

### F-N104 税率档速查页：预设写「年薪 10/24/60 万」，但输入框是应纳税所得额（中，确认缺陷）
- 问题：预设把 100000/240000/600000 直接写入 `income`（应纳税所得额），标签却是「年薪 10 万/24 万/60 万」；页面公式明确「应纳税所得额 = 年收入 − 60,000 − 专项扣除 − 专项附加扣除」，预设绕过了这步换算，税额被显著高估。
- 证据：`tools/finance/tax-bracket.html:161`（输入标签）、`:447-449`（预设）、`:156`（换算公式）、`:301`（税额）
- 复现：点「年薪 24 万（跨档）」→ 输入 240,000 被当作应税所得，税 31,080；若按年薪 24 万先减 60,000 起征点（无专项），应税 180,000，税 19,080，页面多算 12,000。10 万档：预设税 7,480，按年薪 10 万（应税 40,000）税 1,480，多算 6,000。
- 影响：`tools/finance/tax-bracket.html`；预设是最常用的入口，标签与口径错位会让用户把「应税所得」当「年薪」，得出远高于实际的结果。
- 方案：预设改名「应税所得 10/24/60 万」；或增加「税前年薪」输入并按 60,000/专项扣除先换算后再查档。

### F-N105 税率档速查页：「税后所得」只是应税所得减税额，不是实际到手（低，确认缺陷）
- 问题：结果里的 `afterTax = income - tax`，其中 `income` 是应纳税所得额；「税后所得」既未加回 60,000 起征点，也未加回专项扣除，不能当作税后到手工资。
- 证据：`tools/finance/tax-bracket.html:301`（afterTax）、`:323`（税后所得文案）
- 复现：输入 100,000 → 税 7,480、「税后所得」92,520；若 100,000 是应税所得，实际到手至少为 100,000 + 60,000 − 7,480 = 152,520（无专项），相差 60,000。
- 影响：`tools/finance/tax-bracket.html`；用户会把 92,520 当成到手工资，低估实际收入。
- 方案：把标签改为「税后应税所得」；或新增「税前年收入」输入，输出真实税后到手。

### F-N106 税率档速查页：「导出明细 CSV」导出历史表，分档明细不可导出（低，确认缺陷）
- 问题：按钮文案「导出明细 CSV」，实际 `exportTable('#tax_bracketTable')` 导出 TBKit 自动历史表；「分档计算明细」（3%/10%…各档金额）拼在 `#resultBox` 内，没有独立可导出表。
- 证据：`tools/finance/tax-bracket.html:165`（按钮）、`:442`（导出目标）、`:169`（结果区）
- 复现：输入 100,000 → 结果区分档明细 3% 档 1,080 + 10% 档 6,400 = 7,480；点导出得到时间/输入/结果摘要，无各档金额；期望导出分档明细与合计。
- 影响：`tools/finance/tax-bracket.html`；速查页的核心价值是分档拆解，导出的却是历史记录。
- 方案：新增 `#tax_bracketDetail` 表输出各档金额/税率/速算扣除数，导出该表。

### F-N107 个税计算页：顶部「年个税估算」不含年终奖，与同屏奖金对比表的全年合计不一致（中，确认缺陷）
- 问题：`annualTax = tax * 12` 只把月度工资税年化，未含年终奖；而奖金对比表的「全年个税合计」= 工资年税 + 奖金税（单独或合并）。页面默认年终奖 30000，首屏就出现两个不同的「全年个税」。
- 证据：`tools/finance/tax-calculator.html:245`（年个税估算卡片）、`:534`（`tax*12`）、`:452-454`（奖金税额）、`:489`（全年个税合计列）
- 复现：默认（月薪 20,000、社保 3,000、专项 2,000、年终奖 30,000）→ 顶部 9,480，奖金表「单独计税·全年个税合计」10,380；年终奖改 100,000 → 顶部仍 9,480，奖金表 19,270。期望顶部改为「工资部分年个税」，或把所选奖金方案的税额计入总额。
- 影响：`tools/finance/tax-calculator.html`；用户会把 9,480 当作含奖金的全年税负，少算 900～9,790 元，直接影响年终奖发放方式的选择。
- 方案：卡片改名「工资部分年个税（不含奖金）」并在奖金表内高亮「全年合计」；或新增「全年总个税（含奖金）」卡片跟随 `bonusMode` 更新。

### F-N108 个税计算页：导出 CSV 不含奖金两方案与 7 项扣除明细（低，确认缺陷）
- 问题：`__taxExport` 只写工资部分的税前/社保/公积金/应税/税/税后/年税 7 行，不含奖金单独/合并税额、全年合计和专项附加扣除 7 项明细；页面提示「计算结果可导出为 CSV 备案」，导出内容与屏显不完整对应。
- 证据：`tools/finance/tax-calculator.html:249`（导出按钮）、`:556-586`（导出内容）
- 复现：默认参数 + 年终奖 30,000 → 屏显工资税 9,480、奖金单独合计 10,380；导出 CSV 只有工资 7 行，无奖金两方案；期望补充奖金税额/合计与扣除明细，或标注「仅工资部分」。
- 影响：`tools/finance/tax-calculator.html`；用户留档/报备时拿不到页面上最重要的奖金对比结论。
- 方案：导出表增加「奖金单独/并入/推荐方案/全年合计」与 7 项扣除行；文件名区分「工资部分」。

### F-N109 个税计算页：7 项扣除明细合计显示在结果旁，但未点「填入」时不参与计算（低，确认缺陷）
- 问题：`sdTotal` 由 7 项输入实时求和并显示，但税基仍使用上方 `special` 输入；用户填了明细却没点「填入」时，结果区同时出现「明细合计 ¥X」和按旧 `special` 算出的税额，两者口径不一致。
- 证据：`tools/finance/tax-calculator.html:231`（明细合计）、`:442-444`（结果区 sdLine）、`:506`（`special` 参与税基）
- 复现：把子女教育填 2,000、`special` 保持默认 2,000 → 明细合计 2,000 与税基一致；若只填子女教育 2,000 并把 `special` 改为 0，结果区仍显示「明细合计 2,000」但税基按 0 计算，税额偏高；期望明细合计自动应用或明确标注「未应用」。
- 影响：`tools/finance/tax-calculator.html`；扣除明细与税额并排展示，用户无法判断哪个数字真正生效，容易少扣 2,000～6,000/月。
- 方案：明细输入变化时自动同步 `special`，或在 `sdTotal` 旁显示「当前未应用，点击填入」状态；`renderBonus` 使用实际生效的 `special`。

### F-N110 增值税计算页：自定义历史与 TBKit 自动历史双存，清空/删除互不同步（中，确认缺陷）
- 问题：页面同时维护 `vat_calc_history`（自定义「历史记录」tab）和 TBKit 自动历史（单笔页 `#vat_calculatorTable`/`#vat_calculatorHist`）；「保存到历史」只写自定义一套，计算时 TBKit 另记一套，`clearHistory`/`deleteHistory` 只操作自定义列表。
- 证据：`tools/finance/vat-calculator.html:380`（自定义 key）、`:464-482`（保存/渲染）、`:542-547`（清空）、`:721-737`（TBKit 自动历史）
- 复现：计算 1,000 元含税/13% → 单笔页自动历史出现 1 条；点「保存到历史」→「历史记录」tab 出现 1 条；点「清空历史」→ tab 为空，但单笔页自动历史仍保留该条。期望统一一套存储，或清空时同步两处。
- 影响：`tools/finance/vat-calculator.html`；用户以为已清空，实际记录仍在本机（可被他人看到），且同一笔计算出现两份不同格式的历史。
- 方案：删除自定义 `vat_calc_history`，统一用 TBKit 历史；若必须保留自定义 tab，则在保存/删除/清空时同步 TBKit 的 key。

### F-N111 增值税计算页：TBKit 快照包含隐藏的批量输入/批次税率，历史表与 CSV 出现无关列（低，确认缺陷）
- 问题：`__vat_calculatorSnap` 用 `querySelectorAll('input,select,textarea')` 遍历页面全部控件，未按当前 tab 过滤；快照包含 `batchDir`、`batchRate` 和多行 `batchInput`，历史表因此出现隐藏字段列，`batchInput` 的换行会进入 CSV 单元格。
- 证据：`tools/finance/vat-calculator.html:686-697`（快照）、`:721-737`（历史表列）、`:779`（导出）
- 复现：单笔计算后打开自动历史表 → 列含 batchDir/batchRate/batchInput；导出 CSV 出现带换行的「批量输入」列。期望只快照当前 tab 可见字段，CSV 无跨行单元格。
- 影响：`tools/finance/vat-calculator.html`；历史表和导出文件被隐藏字段污染，`batchInput` 的多行文本会形成跨行单元格，影响对账阅读。
- 方案：按 tab 容器分别快照（单笔只取 `#tab-single` 内控件），排除 `textarea` 或至少把换行替换为空格。

### F-N112 增值税计算页：单笔「导出明细 CSV」导出历史表，批量 CSV 缺合计行（低，确认缺陷）
- 问题：单笔按钮调用 `exportTable('#vat_calculatorTable')`，导出的是自动历史而非当前计算结果；批量导出 `exportBatchCSV` 逐行写明细，但没有屏显的「合计」行（税额/含税/不含税合计）。
- 证据：`tools/finance/vat-calculator.html:234`（单笔按钮）、`:779`（单笔导出目标）、`:610`（批量合计行）、`:620-642`（批量导出）
- 复现：单笔 1,000 元含税/13% → 结果 884.96/115.04；点「导出明细 CSV」得到历史表（时间+输入+结果字符串），无当前单项明细；批量 3 行导出无「合计」。期望单笔导出当前结果四行，批量导出补合计行。
- 影响：`tools/finance/vat-calculator.html`；用户拿到的「明细」无法直接用于报销/对账，批量的合计还需手工再加一遍。
- 方案：单笔新增 `#vat_singleDetail` 表（不含税/税额/含税/税率）并导出；批量 CSV 末尾追加与屏显一致的合计行。

### F-N113 增值税计算页：1% 优惠仍标「疫情期间优惠政策」，表述已过时（低，确认缺陷）
- 问题：参考税率表把 1% 的政策依据写成「疫情期间优惠政策」；小规模纳税人 1% 征收率优惠已延续至 2027-12-31，继续用「疫情」表述会让用户误判适用期限。
- 证据：`tools/finance/vat-calculator.html:287`
- 复现：查看 1% 行 →「小规模优惠税率 / 疫情期间优惠政策」；期望「小规模纳税人 1% 优惠（执行至 2027-12-31）」。
- 影响：`tools/finance/vat-calculator.html`；税率适用期的说明与实际政策不一致，影响开票税率选择。
- 方案：更新为政策名称与有效期，并在页面注明「以最新税务总局公告为准」。

### 留存/优势建议（按页）
- **mortgage-calculator**：首付比例、等额本息/等额本金双算法和全表 CSV 导出已经具备，是相对同类页的优势；建议补「首付+税费+总利息」总成本与「月供/收入比」两个决策指标，并保留离线可用。
- **mortgage-prepayment**：两种提前还款方案并排对比（缩期/降月供）是核心优势；建议把基准固定为「原合同应还月供」，增加还款时点/违约金输入，并导出完整摊销计划。
- **housing-fund-loan**：城市规则表、余额倍数、房价 80% 三条依据透明展示是优势；建议利率可选（2.85%/2.6%/自定义）、按年龄压缩可选年限，并导出明细而非仅依据摘要。
- **salary-calculator**：月/年双模式、五险一金比例可调、7 项专项扣除是优势；建议补工资条 CSV 导出与年终奖单独/合并两方案对比，并在年薪模式统一年度口径。
- **simple-interest**：单利与「每年取息」现金流表是优势；建议增加单利 vs 复利并排、按天计息选项，并支持现金流明细导出。
- **tax-bracket**：分档金额、税率、速算扣除数透明是优势；建议增加「税前工资→应税所得」换算、档位边界提示（36,000/144,000/300,000…）与分档明细导出。
- **tax-calculator**：年终奖单独/合并两方案对比 + 7 项扣除明细是优势；建议统一「全年总个税」口径（含奖金）、导出完整对比表并保留离线计算。
- **vat-calculator**：含税/不含税双向换算、批量粘贴、自定义税率是优势；建议统一历史存储、批量 CSV 补合计，并增加进项税抵扣/发票金额校验。

- 本批实读 8 页，逐页通读整份 HTML（含内联 JS、公式框、deep-dive、FAQ）；新增 23 条（高 2 / 中 7 / 低 14），编号 F-N91~F-N113。
- 旧条目复核：F-N11（首付未参与）、F-N12（月缴存/导出错表）、F-N20（VAT 越界）、F-N21（单利模式未用）、F-N28（精度）在当前源码已修复；F-N18/F-N19（个税负值/专项上限）、F-N15（房贷+租金并存）、F-N27（1200 期封顶）仍存在，本段未重复编号；F-N26 改为「以输入月供为基准」后引入了 F-N91 的新基线失真。
- 覆盖统计：`tools/finance/` 共 116 个 HTML（含 index.html），本批实读 8 页；审计文档累计提及 66 个 finance 页面，其余约 50 页未逐页复扫。
- 验证边界：未做浏览器真机、英文态（`?lang=en-US`）、繁体、移动端与门禁（`_build.py`/`_test_static.py`/`_audit_links.py`/`_audit_assets.py`）验证；所有金额均在 `node -e` 内存复算，未修改仓库代码、未运行构建、未做 git 写操作。

## 2026-11-04 续查（并行批 P）

范围：复读 `tools/finance/` 下 8 页（lease-payment-calculator、credit-card-interest、credit-card-type、isbn-validator、iban-validator、bic-validator、currency-symbol、password-generator-advanced），编号 F-N114~F-N145。说明：lease 与 credit-card-interest 在旧批次有 F-N13/F-N22，本段只记录本次复读仍存在或由旧修法引入的问题，不重复旧结论；F-N1~F-N113 未改动。

### F-N114 租赁计算页：手续费被当成「额外本金流出」，实际年化随手续费上升反而下降（高，确认缺陷）
- 问题：`calcIRR` 把手续费与本金同向相加：`cashFlows[0] -= principal + fee`。手续费是承租人期初支付的成本，净融资额应为 `principal - fee`；现在把 fee 当成「多借出的本金」，导致费用越高、算出的收益率越低。
- 证据：`tools/finance/lease-payment-calculator.html:624`（t0 现金流）、`:586`（`*12` 年化）、`:648`/`:669`（「实际年化(IRR)」展示）、`:498`（总还款已含 fee）
- 复现：本金 100,000、0 首付、年利率 6%、36 期、手续费 5,000 → 页面月供 3,042.19、「实际年化(IRR)」2.75%（低于名义 6%）；按净融资 95,000 的借款人现金流 `node -e` 复算，真实成本约 9.48%（名义）/9.90%（有效）。手续费改为 0 → 6.00%；改为 20,000 会进一步降到负值附近。期望：手续费越高 IRR 越高。
- 影响：`tools/finance/lease-payment-calculator.html`；高手续费租赁方案被显示成「更便宜」，用户可能据此选错产品，属于核心结论错误。
- 方案：t0 现金流改为 `-(principal - fee)`（借款人视角取相反符号亦可），`totalPayment` 同步按「月供×期数+首付+fee」口径；补 fee=0/5000/20000 的单调性单测。

### F-N115 租赁计算页：残值/留购款在「先息后本」「等额本金」下双重计算，IRR 为负或无解（高，确认缺陷）
- 问题：先息后本末期只还「本金+当期利息」，并未把 `fv` 留购款加入末期还款，但 `calcIRR` 又在 t=n 额外扣一次 `fv`；等额本金同样末期不含留购款，导致现金流总额小于融资本金、IRR 无解显示「—」。「总还款额」也不含留购款。
- 证据：`tools/finance/lease-payment-calculator.html:566-569`（末期 `pay = principal + interest; balance = fv`）、`:582`（总还款=各期之和+fee）、`:630`（`cashFlows[n] -= fv`）、`:498`（等额型总还款同样不含 fv）
- 复现：10 万、6%、36 期、残值 20,000、先息后本 → 末期还款 100,500（不含留购款）、总还款 118,000、明细末期余额 20,000、「实际年化(IRR)」−0.74%；等额本金同参 → IRR 显示「—」，总还款 91,000（少 20,000）。期望末期还款 120,500（或明确留购款另付并计入总成本），IRR≈6%。
- 影响：`tools/finance/lease-payment-calculator.html`；残值租赁是页面主场景，实际成本被低估 2 万且年化为负/无解，直接误导留购决策。
- 方案：先息后本/等额本金的末期 `payment += fv`、`totalPayment` 含 fv；IRR 只通过付款行计入 fv，删除 `cashFlows[n] -= fv`；等额型保持公式口径并做三种模式的对账测试。

### F-N116 租赁计算页：期初等额还款明细出现负利息，明细合计与汇总卡片对不上（中，确认缺陷）
- 问题：期初模式先 `balance -= pmt` 再按剩余余额计息，末期余额已为负，末期利息变成负数；各期本金合计超过融资本金，明细利息合计与汇总卡片的「总利息」不一致。
- 证据：`tools/finance/lease-payment-calculator.html:505-508`（期初先冲减再计息）、`:499`（总利息公式）、`:515-520`（明细入表）
- 复现：10 万、6%、36 期、期初还款 → 末期利息 −44.87，明细利息合计 7,919.90 而卡片总利息 8,974.10，本金合计 101,054.21（>100,000）。期望末期利息≥0、本金合计=100,000、明细利息合计=卡片总利息。
- 影响：`tools/finance/lease-payment-calculator.html`；明细表与汇总卡自相矛盾，财务对账时无法解释差额（约 1,054 元）。
- 方案：期初模式改为「先计息、再还款」：`interest = balance*r; principalPart = pmt - interest; balance -= principalPart`，末期用剩余余额校正最后一期；或直接按 annuity-due 摊还公式生成整表。

### F-N117 租赁计算页：首付>100%、残值>本金均未校验，出现负融资额/负月供并照常导出（中，确认缺陷）
- 问题：首付比例只有 HTML `max=90`（不阻止键入），JS 直接 `pv*downPct/100`；残值也未限制 `≤principal`。极端输入会产生负融资本金、负月供、负总还款，进度条宽度超过 100%，且仍写入历史/导出。
- 证据：`tools/finance/lease-payment-calculator.html:187`（max=90）、`:471`/`:479`（无 JS 校验）、`:658-659`（`Math.max(downPct,5)` 直接作宽度）、`:512-513`（只对 fv 做余额赋值）
- 复现：首付 150% → 融资金额 −50,000、月供 −1,521.10、总利息 −4,759.49；残值 150,000 > 本金 100,000 → 月供 −771.10、总还款 −27,759.49、IRR 显示「—」。期望拒绝并提示「首付比例须 0–100%、残值不得超过融资本金」。
- 影响：`tools/finance/lease-payment-calculator.html`；负成本方案可被导出成正式报价附件，用户无法察觉输入越界。
- 方案：计算前校验 `0≤downPct≤100`、`0≤fv≤principal`、`fee≥0`；进度条宽度 `Math.min(Math.max(...),100)`；越界时在结果区显示错误而不是继续计算。

### F-N118 租赁计算页：0% 利率历史被 `|| 6` 回填成 6%，无法回放贴息方案（低，确认缺陷）
- 问题：`loadHistory` 用 `h.annualRate || 6`、`h.pv || 100000` 回填，合法的 0 被当成空值；0 利率/免息租赁的历史记录一点击就变成 6%。
- 证据：`tools/finance/lease-payment-calculator.html:836`（`h.pv || 100000`）、`:838`（`h.annualRate || 6`）
- 复现：计算 10 万、0% 利率、36 期并保存/自动记录 → 点该历史条目 → 利率输入变 6%，重算月供从 2,777.78 变 3,042.19。期望回填 0 并保持 2,777.78。
- 影响：`tools/finance/lease-payment-calculator.html`；厂商贴息/0 利率方案无法复现，历史记录失真。
- 方案：改为 `Number.isFinite(+h.annualRate) ? +h.annualRate : 6`，其余字段同样只在 `undefined/null` 时回退。

### F-N119 租赁计算页：第一个「导出明细 CSV」导出自动历史，逐期摊销要另一个按钮导出（低，确认缺陷）
- 问题：结果区上方「导出明细 CSV」调用 `__lease_payment_calculatorExport()`，导出的是 TBKit 自动历史表（时间+输入+结果摘要）；真正的逐期摊销由详情区「📥 导出CSV」`exportCSV()` 导出，两个按钮文案相近、目标不同。
- 证据：`tools/finance/lease-payment-calculator.html:219`（首个导出按钮）、`:994`（导出历史实现）、`:223`（第二个导出按钮）、`:856`（摊销导出实现）
- 复现：计算默认方案 → 点第一个「导出明细 CSV」得到历史摘要（无期数/本金/利息/余额）；点下方「导出CSV」才得到逐期明细。期望第一个按钮直接导出摊销表，历史另设「导出历史」。
- 影响：`tools/finance/lease-payment-calculator.html`；用户拿到的「明细」不是摊销计划，留档/对账价值低。
- 方案：删除重复按钮，保留一个「导出摊销明细 CSV」指向 `exportCSV()`；历史表另设独立入口并明确命名。

### F-N120 信用卡利息页：滞纳金比例输入完全无效，滞纳金总额恒为 0（中，确认缺陷）
- 问题：`simulateMinimum` 中 `payment = Math.min(minPayment, balance + interest)`，而 `minPayment = Math.max(balance*minRatio + interest, 10)`；当 `minRatio` 在 1%–100% 时，`payment` 恒等于 `minPayment`，`if (payment < balance*minRatio + interest)` 永假，`lateFee` 永远为 0。
- 证据：`tools/finance/credit-card-interest.html:346-352`（最低还款与滞纳金分支）、`:378-396`（比例校验 1%–100%）、`:433`（滞纳金总额卡片）
- 复现：账单 10,000、日息 0.05%、最低比例 10%、滞纳金比例 5%，任意期数 → 结果卡「滞纳金总额 0.00」，逐期表滞纳金列全 0；把比例改成 50% 仍为 0。期望按最低额缺口产生滞纳金，或删除该输入。
- 影响：`tools/finance/credit-card-interest.html`；用户以为已计入违约金，实际总支出少算；页面提供的是一个假开关。
- 方案：明确触发条件（如「未在到期日前还足最低额」）并按缺口计费，或移除「滞纳金比例」输入与「滞纳金总额」卡片；术语同步改为「违约金」。

### F-N121 信用卡利息页：宣称「按月计收复利」，模拟却按单利，18.25%/19.56% 两套年化同屏（中，确认缺陷）
- 问题：公式框写「按月计收复利」，但 `simulateMinimum` 每期只算 `balance * dailyRate * 30`，利息未滚入本金；建议卡用 `dailyRate*365` 得 18.25%（名义单利），右侧 EAR 组件用 `(1+dailyRate*30)^12-1` 得 19.56%（复利），三套口径并存。
- 证据：`tools/finance/credit-card-interest.html:212`（「按月计收复利」）、`:345`（单利计息）、`:443`（18.25%）、`:572`（建议卡年化）、`:818-819`（EAR 19.56%）
- 复现：10,000 元、日息 0.05%、最低 10% → 页面循环利息 1,493.89、55 期；按页面宣称的按月复利 `node -e` 复算为 1,757.01、64 期，差 263.12 元/9 期；同屏又显示「年化约 18.25%」与「真实年化 19.56%」。期望单一明确口径。
- 影响：`tools/finance/credit-card-interest.html`；最低还款成本被低估约 18%，用户对「还最低要多久/多付多少」判断失真。
- 方案：若按复利，改为 `balance = balance*(1+dailyRate*30) - payment`（或每期把利息计入余额）；若按单利，删除「复利」表述并注明「按 30 天单利近似」；建议卡统一使用 EAR 并标注「有效年利率」。

### F-N122 信用卡利息页：账单日/到期日只影响「免息天数」展示，不参与任何计息（低，确认缺陷）
- 问题：`billDay`/`dueDay` 仅用于 `interestFreeDays` 文案，`simulateMinimum` 固定按 30 天计息、分期也不使用日期；`+value || 1` 使 0 变 1，免息天数再被 clamp 到 20–56，非法日期被掩盖。
- 证据：`tools/finance/credit-card-interest.html:376-377`（`|| 1`）、`:398-404`（免息天数与 clamp）、`:345`（固定 30 天）、`:448-461`（分期不看日期）
- 复现：账单日 10、到期日 30 → 免息 40 天、利息 1,493.89；只把到期日改 31 → 免息 41 天，利息与期数完全不变。期望日期变化至少改变计息天数，或明确标注「日期仅用于免息天数展示」。
- 影响：`tools/finance/credit-card-interest.html`；用户以为输入真实账单周期能提高精度，实际是装饰性字段。
- 方案：用实际账单周期天数代替固定 30，并校验 1–31；若暂不建模，则在日期输入旁注明「仅展示，不参与计息」。

### F-N123 信用卡利息页：F-N22 部分修复后，方案对比仍未计 120 期后的剩余本金（中，确认缺陷）
- 问题：`showCompare` 的 `minTotal = bill + totalInterest + totalLateFee`，未加 `sim.balance`；120 期未还清时仍输出「更省钱」与节省额，只附一行「仅供参考」。
- 证据：`tools/finance/credit-card-interest.html:529-534`（模拟与 minTotal）、`:540-542`（结论/节省）、`:551-557`（未还清提示与结论渲染）
- 复现：账单 10,000、日息 0.05%、最低 1%、分期 12 期费率 0.75% → 最低方案 120 期后仍欠 2,993.80，页面总支出 20,509.29（少算剩余本金），节省额因此至少虚高 2,993.80；期望总支出含剩余本金，或未还清时不出结论/节省额。
- 影响：`tools/finance/credit-card-interest.html`；F-N22 修了「还清月数」的假象，但对比金额仍系统性失真，结论可能反转。
- 方案：`minTotal += sim.balance`；未还清时把「结论」改为「120 期内无法完成对比」，并隐藏节省额；分期按同一期限口径计算。

### F-N124 信用卡利息页：负日利率/负分期费率未校验，且「滞纳金」为已废止术语（低，确认缺陷）
- 问题：`dailyRate`、`instFee` 用 `+value/100 || 0`，负值照常参与计算，产生负利息/负总支出与负年化；页面仍使用 2017 年前「滞纳金」旧称，现行信用卡规则为「违约金」，且按时还足最低额本身不产生违约金。
- 证据：`tools/finance/credit-card-interest.html:375`（日利率）、`:383`（分期费率）、`:177`/`:433`/`:574`（「滞纳金」）
- 复现：日利率 −0.05 → 循环利息 −1,493.89、总支出 8,506.11；分期费率 −0.75%/期 → 「实际年化利率」为负。期望拒绝并提示「利率/费率须≥0」。
- 影响：`tools/finance/credit-card-interest.html`；负成本结果不符合业务常识，术语过时还会误导用户对逾期责任的认知。
- 方案：校验 `dailyRate ≥ 0`、`instFee ≥ 0`（并设合理上限），越界显示错误；全文改用「违约金」并说明触发条件。

### F-N125 信用卡类型页：标题/描述承诺「卡等级」，实现只有发卡组织与长度（中，确认缺陷）
- 问题：meta、og、h2、公式说明反复写「识别发卡组织与卡等级（如 Visa/Master/银联）」，但 `detect()` 只做前缀匹配 + 长度校验，输出只有品牌/长度，没有任何等级（普卡/金卡/白金）判定。
- 证据：`tools/finance/credit-card-type.html:10`（description）、`:14`/`:20`（标题）、`:162`/`:164`（公式说明/intro）、`:246-269`（唯一输出逻辑）
- 复现：输入默认 5500005555555559 → 输出「Mastercard / 16 位 / 类型识别完成」，无任何卡等级；期望要么给出等级，要么删除该承诺。
- 影响：`tools/finance/credit-card-type.html`；与 SEO 标题/描述不一致，用户按「查等级」进入却拿不到结果，转化与信任受损。
- 方案：把文案统一改为「识别发卡组织（BIN 前缀）」；若要等级，需内置离线 BIN 表并披露覆盖率与数据日期（不可只靠前缀猜等级）。

### F-N126 信用卡类型页：长度不足与超长共用「继续输入」，1 位数字就断言品牌（低，确认缺陷）
- 问题：`lenOk` 为 false 时统一输出「⏳ 继续输入以完成长度校验」；数字已超过 `brand.lengths` 上限时仍提示继续输入；输入 1 位「4」时已直接显示「卡片类型：Visa」。
- 证据：`tools/finance/credit-card-type.html:255-266`（品牌与长度分支）
- 复现：输入 20 位 `41111111111111111111` → 仍显示「继续输入」（期望「长度超出，Visa 最长 19 位」）；输入 `4` → 直接给 Visa（期望「前缀初步判断，继续输入」）。
- 影响：`tools/finance/credit-card-type.html`；表单校验提示方向相反，用户会继续追加数字；过早断言品牌会掩盖后续输入错误。
- 方案：按 `digits.length < min` / `在区间` / `> max` 三分支给出「继续输入 / 长度不符（超出）」，前缀命中时用「初步判断」措辞。

### F-N127 信用卡类型页：无 Luhn 却显示「✅ 类型识别完成」，品牌覆盖与示例文案不符（低，确认缺陷）
- 问题：页面没有任何 Luhn 校验，16 位且长度匹配就显示绿色「✅ 类型识别完成」；品牌表缺 Maestro(50/56–69)、Diners(30/36/38)、MIR(2200)，公式写「银联(62)」但代码还接受 88；deep-dive 示例「5 开头识别为 Mastercard」与实际 51–55/2221–2720 不符。
- 证据：`tools/finance/credit-card-type.html:239-244`（品牌表）、`:161`（公式区间）、`:197`（「5 开头=Mastercard」）、`:260-263`（完成态）
- 复现：`4111111111111112`（Visa 16 位，Luhn 非法）→ 显示「✅ 类型识别完成」；`5000000000000000` → 未知（期望 Maestro）；`8800000000000000` → 银联（公式未提 88）。期望单独显示 Luhn 结果，并修正示例/覆盖说明。
- 影响：`tools/finance/credit-card-type.html`；description 声称「用于表单校验与支付前端判断」，但非法卡号被判「完成」，容易让调用方误以为通过。
- 方案：增加 Luhn 行（通过/失败独立标识），把「完成」改为「前缀与长度匹配」；补 Maestro/Diners/MIR 或明确列出支持品牌；核实 88 前缀后再保留。

### F-N128 ISBN 验证页：输入标签缺少 `>`，`#result` 容器被吞掉，整页校验抛异常失效（高，确认缺陷）
- 问题：`<input ... value="9787111111115"` 行末没有闭合 `>`，下一行 `<div class="result-box" id="result">` 被 HTML 分词器当作 input 的属性继续解析，`#result` 容器不存在；重复的 `id` 被丢弃（若浏览器保留，也只会把 `innerHTML` 写进 input）。`validate()` 在 `getElementById('result')` 得到 null 后访问 `resultBox.innerHTML`，载入即抛 `TypeError`。
- 证据：`tools/finance/isbn-validator.html:167`（缺少 `>`）、`:169`（被吞的 `#result`）、`:376`（取容器）、`:379`/`:389`/`:435`（直接写 `innerHTML`）
- 复现：打开页面 → 控制台 `Cannot read properties of null (reading 'innerHTML')`；输入合法 `978-0-306-40615-7` 或点「转为 ISBN-13」均无结果（按钮内部也调用 `validate()`）。期望正常显示「ISBN-13 / 校验通过 / 对应 ISBN-10」。
- 影响：`tools/finance/isbn-validator.html`；校验、转换、示例三个主功能全部不可用，是本次 8 页中最严重的功能性故障。
- 方案：补上 `>`（`value="9787111111115">`），并加一个静态检查（每条 `<input>` 必须以 `>` 结束）；在修好后回归 `978-0-306-40615-7`、`0306406152`、`979` 三例。

### F-N129 ISBN 验证页：13 位只校验 mod-10，不校验 978/979，任意 EAN-13 被判「ISBN 校验通过」（中，确认缺陷）
- 问题：`isbn13Check` 只算加权校验位；`validate` 对任意 13 位都宣称「ISBN-13 ✅ 校验通过」，非 978/979 前缀还会落到「979 前缀无法转换」的提示。
- 证据：`tools/finance/isbn-validator.html:405-431`（13 位分支）、`:314-330`（`isbn13Check`）、`:430`（固定「979」文案）
- 复现（需先修复 F-N128 的 DOM 断链才能看到结果）：输入 `4006381333931`（合法 EAN-13，非 ISBN）→ 显示「ISBN-13 ✅ 校验通过」；点「转为 ISBN-10」→ 提示「仅 978 前缀的 ISBN-13 可转换为 ISBN-10」，但结果区的提示写成「979 前缀」。期望非 978/979 前缀直接判「不是 ISBN」。
- 影响：`tools/finance/isbn-validator.html`；把普通商品条码当书号，误导录入/库存系统。
- 方案：13 位分支先判 `prefix === '978' || prefix === '979'`，否则输出「非 ISBN 的 EAN-13 前缀」；转换提示按实际前缀生成。

### F-N130 ISBN 验证页：转换不校验源校验位，非法 ISBN-10 仍被转成合法 ISBN-13（中，确认缺陷）
- 问题：`convertTo13()` 只检查长度 10，`convertTo10()` 只检查长度 13 与 978 前缀，均不校验原号码的校验位；结果区在 ISBN-10 校验失败时也照常输出「对应 ISBN-13」。
- 证据：`tools/finance/isbn-validator.html:404`（校验失败仍输出对应 13）、`:438-448`（只查长度）、`:450-464`（只查长度/前缀）
- 复现（需先修复 F-N128）：输入 `1234567890`（ISBN-10 校验位错误）→ 点「转为 ISBN-13」→ 得到 `978-1-234-56789-7`，重新校验通过并显示合法；期望先提示「源 ISBN-10 校验失败，不能转换」。
- 影响：`tools/finance/isbn-validator.html`；用户会把伪造/误录的号码「洗白」为合法 ISBN，污染书号数据。
- 方案：转换前先跑 `isbn10Check`/`isbn13Check`，失败即 alert 并中止；结果区的「对应 ISBN」也仅在源校验通过时显示。

### F-N131 ISBN 验证页：标题/描述被截断成半句，分段算法固定 substring 与实际登记组不符（低，确认缺陷）
- 问题：`<title>` 与 og:title 是「ISBN 验证与转换 - 位为 10 时用 X 表示」，meta description 断在「求和后」，intro 也断在「求和后」；ISBN 分段固定 `substring(1,4)`/`substring(4,9)`，未按登记组（0/1/2/7 等）与出版者码长度解析，分段结果常错位。
- 证据：`tools/finance/isbn-validator.html:10-11`（description 断句）、`:15`/`:22`（标题残句）、`:170`（intro 断句）、`:400`（固定出版者 3 位）、`:414-417`（只按首字符分 1/2 位组号）
- 复现：`978-7-02-123456-?` 这类出版者码为 2 位的书号，页面把 `702` 当作出版者；标题在搜索结果里显示「位为 10 时用 X 表示」这类残句。期望标题/描述为完整句，分段标注「近似分组，非官方解析」。
- 影响：`tools/finance/isbn-validator.html`；SEO 摘要不可读，分段可视化被当成权威结果。
- 方案：重写 title/description/intro 为完整句；分段改为调用离线 ISBN 范围表，或明确标注「示意分组」并只保留 GS1 前缀/校验位的高置信分段。

### F-N132 IBAN 验证页：未知国家代码只要 mod-97=1 仍显示绿色「校验通过」，形成假阳性（中，确认缺陷）
- 问题：`country` 不存在时只提示「未知国家代码」，仍继续跑 mod-97；余数为 1 就输出绿色 `✅ mod-97 校验通过`，且不做长度校验，没有任何「整体无效」结论。
- 证据：`tools/finance/iban-validator.html:379-386`（国家/长度分支）、`:388-396`（mod-97 结论）
- 复现：构造 `ZZ121234567890`（`node -e` 复算余数=1，14 位）→ 输出「⚠️ 未知国家代码 ZZ」+「✅ mod-97 校验通过」，无红色失败标识。期望未知国家代码直接判无效，或至少显示「国家未知，不能判定有效」。
- 影响：`tools/finance/iban-validator.html`；跨境汇款场景会把伪造/错国代码的 IBAN 当成「校验通过」。
- 方案：把国家存在性与长度校验纳入总体结论（三者全过才显示绿色）；未知国家时不再输出独立「通过」标签，改显示「仅数学校验通过，无法确认有效性」。

### F-N133 IBAN 验证页：国家表仅 33 个，合法 SA/TR/UA 等 IBAN 被判「未知国家代码」（中，确认缺陷）
- 问题：`IBAN_COUNTRIES` 只覆盖 33 个国家/地区（源码注释写「部分主要国家」），缺少 SA、TR、UA、QA、IL、AE 之外的多数 IBAN 国家；未知代码又不做长度校验，导致真实合法 IBAN 被标未知。
- 证据：`tools/finance/iban-validator.html:274`（「部分主要国家」注释）、`:275-310`（33 条数据）、`:379-386`（未知分支）
- 复现：输入沙特合法 IBAN `SA0380000000608010167519`（24 位，mod-97=1）→ 显示「⚠️ 未知国家代码 SA」，长度校验缺失；期望识别 SA 并校验 24 位。同类：TR/UA 均不在表内。
- 影响：`tools/finance/iban-validator.html`；覆盖面被宣传为「国家 IBAN 长度速查表」，实际大量合法 IBAN 无法校验，跨境用户被误判。
- 方案：补全 IBAN 注册国家（至少 SA/TR/UA/QA/IL/JO/KW/BH 等），并在页面标注数据版本/覆盖数量；未知代码时明确「本工具未收录，不代表 IBAN 无效」。

### F-N134 IBAN 验证页：33 国中仅 4 国有示例，点击其余 29 国行无任何反应（低，确认缺陷）
- 问题：表头写「点击国家代码可快速加载示例」，`loadExample(cc)` 只对 `EXAMPLES` 中的 GB/DE/FR/CH 生效，其余国家静默返回，没有提示。
- 证据：`tools/finance/iban-validator.html:311-316`（仅 4 条示例）、`:401-406`（无 else 分支）、`:418`（整行可点击）、`:176`（提示文案）
- 复现：点击「沙特 SA」行 → 输入框不变、无任何提示；期望加载示例或提示「该国暂无示例」。点击 GB → 正常加载。
- 影响：`tools/finance/iban-validator.html`；用户以为页面坏了，示例表的价值被高估。
- 方案：为每个国家补一条合法示例（可用公开测试 IBAN），或去掉整行点击并在表头注明「仅 GB/DE/FR/CH 提供示例」。

### F-N135 IBAN 验证页：标题被截成「- 国家代码」，与页面实际能力不符（低，确认缺陷）
- 问题：`<title>`/og:title 是「IBAN 国际银行账号验证 - 国家代码」，后缀是半句；页面实际做的是 mod-97 + 国家长度 + BBAN 结构，标题没有表达核心能力。
- 证据：`tools/finance/iban-validator.html:14`/`:20`（标题）、`:67`（twitter:title）、`:180`（公式说明）
- 复现：搜索结果标题显示「IBAN 国际银行账号验证 - 国家代码」，期望「IBAN 验证 - mod-97 校验与国家长度速查」。
- 影响：`tools/finance/iban-validator.html`；SEO 点击率与主题相关性受损。
- 方案：改为完整标题并同步 og/twitter；保留「国家代码」作为正文关键词而非残句。

### F-N136 BIC 验证页：输入在正则校验前直接拼入 innerHTML，存在自 XSS 风险（低，待验证）
- 问题：`validate()` 先把 `raw` 拼进 `html`，再跑正则；无效输入分支也把 `raw` 写入 `out.innerHTML`，未转义。`toUpperCase()` 会破坏 `alert` 这类大小写敏感的标识符，但 HTML 字符实体在属性值中会先解码，`&#97;lert(1)` 仍可能还原为 `alert(1)`。
- 证据：`tools/finance/bic-validator.html:233`（仅 trim+uppercase）、`:237`（直接插值 `raw`）、`:249`/`:265`（写入 innerHTML）
- 复现：输入 `<img src=x onerror=&#97;lert(1)>` → 大写后实体仍解码为 `alert(1)`，加载失败图时可能执行；直接写 `onerror=alert(1)` 则因变成 `ALERT` 而不触发。期望只显示纯文本。需真机复核实体绕过路径。
- 影响：`tools/finance/bic-validator.html`；仅影响本机（无回显/存储型传播），但工具站仍不应允许输入执行脚本，且该输入可能进入历史快照。
- 方案：渲染前统一 `escapeHtml(raw)`，或先校验格式、只在通过后渲染；所有用户输入用 `textContent` 写入。

### F-N137 BIC 验证页：带空格/连字符的标准写法被拒，11 位主办公室仍显示「分支代码 XXX」，本地主题函数为死代码（低，确认缺陷）
- 问题：只做 `trim()`，不清洗空格/连字符，`DEUT DEFF` 长度变 9 直接报「长度必须为 8 或 11」；11 位 `DEUTDEFFXXX` 把 `XXX` 当普通分支代码显示，未说明「主办公室」；页面内 `toggleToolTheme()` 与按钮调用的 `ToolBox.toggleToolTheme()` 重复，本地函数从未执行。
- 证据：`tools/finance/bic-validator.html:233`（无清洗）、`:240-241`（长度判断）、`:255`（branch 直接 substring）、`:129`（按钮用 ToolBox）、`:267`（本地死函数）
- 复现：输入 `DEUT DEFF` → ❌ 长度必须为 8 或 11（期望去空格后通过）；输入 `DEUTDEFFXXX` → 「分支代码：XXX」（期望「主办公室（XXX）」）；`DEUTDEFF` → 正常。
- 影响：`tools/finance/bic-validator.html`；国际汇款单常见「4+2+2」空格写法被误判，主办公室语义不清；死代码增加维护成本。
- 方案：先 `replace(/\s|-/g,'')` 再校验；`branch === 'XXX'` 时标注主办公室；删除本地 `toggleToolTheme()` 或让按钮统一调用它。

### F-N138 货币符号页：数据数组重复 4 组，计数 153 与唯一 149、文案 170+ 三重不一致（中，确认缺陷）
- 问题：`currencies` 中 AUD、NIO、UGX、XCD 各出现 2 次（XCD 两条的国家文案还不同）；`renderCurrencies` 用 `list.length` 显示「共找到 N 种货币」，实际唯一代码只有 149 个，intro 却写「170+ 种」。
- 证据：`tools/finance/currency-symbol.html:176`（170+ 文案）、`:332`/`:472`（AUD 重复）、`:368`/`:424`（NIO 重复）、`:432`/`:455`（UGX 重复）、`:373`/`:463`（XCD 重复）、`:559`（按数组长度计数）
- 复现：打开页面 →「共找到 153 种货币」；搜索 `NIO` → 出现两张完全相同的尼加拉瓜科多巴卡片；导出 CSV 同样重复 4 行；期望去重后 149 条，或补足到文案承诺的 170+。
- 影响：`tools/finance/currency-symbol.html`；重复卡片/重复 CSV 行降低可信度，数量口径三处互相矛盾。
- 方案：按 `code` 去重（保留一条并合并国家说明），计数改用唯一码；文案改为实际数量或补齐缺失货币后同步。

### F-N139 货币符号页：混入非 ISO 4217 与已废止货币，仍按「当前货币」展示（中，确认缺陷）
- 问题：页面说明与 FAQ 以 ISO 4217 为依据，但数据含 XBT/ETH/KID/TVD 等非 ISO 代码；HRK（2023 年加入欧元区）、SLL（2022 年被 SLE 取代）、VEF（2018 年被 VES 取代）、ANG（2025 年被 XCG 取代）仍作为现行货币列出，无停用标识。
- 证据：`tools/finance/currency-symbol.html:360`（VEF）、`:380`（ANG）、`:386`（HRK）、`:437`（SLL）、`:470-474`（KID/TVD/XBT/ETH）
- 复现：搜索 `HRK` → 正常显示「克罗地亚库纳」卡片与详情，无任何停用提示；搜索 `XBT` → 比特币以「货币」卡片出现。期望过期项标注「已停用/已替换」或移出默认列表。
- 影响：`tools/finance/currency-symbol.html`；跨境合同/记账引用过期代码可能开票错误；「ISO 4217」定位被非 ISO 项稀释。
- 方案：增加 `status`（active/obsolete/non-iso）与 `replacedBy` 字段，默认折叠过期项并在详情提示；非 ISO 项单独分组，文案改为「ISO 4217 + 常用非 ISO 单位」。

### F-N140 货币符号页：VEF 缺符号字段，CNY/CNH 辅单位「Jiao/Fen × 10」语义错误（低，确认缺陷）
- 问题：VEF 没有 `symbol`，卡片用代码 `VEF` 充当大号符号、详情符号显示 `-`；CNY/CNH 的 `subunit:'Jiao/Fen'` 配 `subunitRate:10`，详情生成「1 Yuan = 10 Jiao/Fen」，既混用两个单位又算错分（1 元=10 角=100 分）。
- 证据：`tools/finance/currency-symbol.html:360`（VEF 无 symbol）、`:570`（`c.symbol || c.code`）、`:581`（详情标题）、`:329`/`:476`（CNY/CNH 辅单位）
- 复现：搜 `VEF` → 大号符号位显示「VEF」而非货币符号；点 CNY 详情 → 辅单位行「1 Yuan = 10 Jiao/Fen」。期望 VEF 标注历史符号并标停用；CNY 改为「1 Yuan = 100 Fen（10 Jiao）」。
- 影响：`tools/finance/currency-symbol.html`；卡片排版不一致，辅单位换算可能被用于报价/找零。
- 方案：VEF 补历史符号 `Bs.` 并标 `obsolete`；CNY/CNH 改 `subunit:'Fen', subunitRate:100`，另在详情加「1 角=10 分」说明。

### F-N141 货币符号页：导出后把隐藏的 153 行表格永久显示在页面上（低，确认缺陷）
- 问题：`#curTable` 初始 `display:none`，`__curExport()` 为导出临时填表后执行 `t.style.display=''`，导出结束不恢复隐藏；用户点一次导出，页面底部就多出整张表。
- 证据：`tools/finance/currency-symbol.html:202`（初始隐藏）、`:527-528`（导出后显示且不恢复）
- 复现：点「⬇️ 导出货币清单 CSV」→ 下载成功，页面下方立即出现 153 行表格且无关闭入口，刷新后才消失。期望导出后仍保持隐藏。
- 影响：`tools/finance/currency-symbol.html`；移动端页面被长表撑开，用户以为导出把数据「贴」到了页面上。
- 方案：导出完成后 `t.style.display='none'`；或把导出表放到屏幕外容器，不参与布局。

### F-N142 密码生成页：「清空」按钮 onclick 只是声明常量，点击完全无效（中，确认缺陷）
- 问题：「清空」按钮写成 `onclick="const __h0=''"`，只声明一个常量，既不清结果列表也不重置强度条；页面没有 `clearAll` 实现。
- 证据：`tools/finance/password-generator-advanced.html:189`（按钮）、`:192-196`（强度条）、`:307`（结果写入 `#output`）
- 复现：生成 3 条密码 → 点「清空」→ 列表与「强度：…（5/5）」完全不变；刷新页面才清空。期望清空结果与强度状态。
- 影响：`tools/finance/password-generator-advanced.html`；主要交互按钮失效，用户可能误以为旧密码仍在当前会话中。
- 方案：恢复 `clearAll()`：清空 `#output`、`#strengthText`、5 个 bar 背景，并重置 `updateStrength` 相关状态。

### F-N143 密码生成页：文案宣称「口令短语模式/不存储」，实际无该功能且明文密码写入 localStorage（中，确认缺陷）
- 问题：meta/og/深链均写「支持口令短语模式，纯前端生成不存储」，但页面没有任何 passphrase 输入或词表；`__password_generator_advancedExtras()` 把结果 `rec[rk]=res` 写入 TBKit 历史，生成过的明文密码会进入 localStorage、历史表和 CSV 导出。
- 证据：`tools/finance/password-generator-advanced.html:10`/`:15`（description/og）、`:223`（深链清单）、`:448`（`rec[rk]=res`）、`:454`（导出历史表）、`:304`（结果文本）
- 复现：生成一次 → 打开本页「历史」/单笔页自动历史表，能看到刚才的明文密码；点「导出明细 CSV」可把明文密码导出。搜索页面无任何 passphrase 控件。期望：要么实现口令短语，要么删除文案；历史不落盘或只存参数/掩码。
- 影响：`tools/finance/password-generator-advanced.html`；隐私承诺与实现相反，共用电脑或导出文件会泄露密码，属于安全/信任问题。
- 方案：设置 `__password_generator_advanced_skip = true` 或重写 extras 只记录长度/字符集等参数；实现 passphrase（词表+分隔符+大小写变换）或把文案改为「随机密码生成器」。

### F-N144 密码生成页：批量生成后「复制」把 10 条密码连写成一串，无法逐条使用（中，确认缺陷）
- 问题：`copyResult()` 取 `#output.textContent`，而每条密码是独立的 `.hist-item` div，`textContent` 不含换行/分隔符，批量复制得到 `pw1pw2…pw10`。
- 证据：`tools/finance/password-generator-advanced.html:304`（逐条 div）、`:325-326`（整块 textContent 复制）、`:461`（预设「32 位批量 10 条」）
- 复现：选预设「32 位批量 10 条」→ 生成 10 行 → 点「复制」→ 粘贴得到一条 320 字符连写字符串；期望每行一条、换行分隔。
- 影响：`tools/finance/password-generator-advanced.html`；批量模式的主操作不可用，用户需手工拆分。
- 方案：复制时 `[...document.querySelectorAll('#output .hist-item')].map(el=>el.textContent).join('\n')`；单条模式保持原行为。

### F-N145 密码生成页：随机数取模偏差、复制无失败回退且强度只评首条（低，确认缺陷）
- 问题：`randInt` 用 `a[0] % max` 取随机数，未做拒绝采样，存在模偏差；`copyResult` 对 `navigator.clipboard.writeText` 没有 catch，非安全上下文或权限被拒时按钮无任何反馈；`generate` 只在 `i===0` 时调用 `updateStrength`，批量 20 条仅展示首条强度。
- 证据：`tools/finance/password-generator-advanced.html:281-284`（randInt）、`:305`（仅首条更新强度）、`:326`（无 catch 的 clipboard）
- 复现：在非 HTTPS 或剪贴板权限被拒的环境点「复制」→ 无 alert、无回退、无错误提示；批量生成 20 条 → 强度条只反映第一条。期望复制失败给出提示并回退，批量模式至少提示「强度按首条展示」。
- 影响：`tools/finance/password-generator-advanced.html`；模偏差量级极小（2^-32），但不符合密码学最佳实践；复制静默失败与强度口径影响可用性。
- 方案：用拒绝采样（`limit = 2^32 - (2^32 % max)` 丢弃超出部分）；`copyResult` 加 `catch` 回退 `document.execCommand('copy')` 并 toast；批量时在强度旁标注「首条」或按最弱一条显示。

### 留存/优势建议（按页）
- **lease-payment-calculator**：等额/等额本金/先息后本三模式 + 期初/期末 + 残值 + 明细表/图表/IRR 的密度在同类页中少见；建议修好 IRR 口径与残值对账后，补「总成本（租金+首付+手续费+留购款）」和「不同手续费方案对比」，保留离线计算。
- **credit-card-interest**：最低还款逐期模拟表、分期 IRR 与双方案对比是差异化能力；建议保留并统一计息口径、接通账单日/到期日、补「全额还款」为第三方案。
- **credit-card-type**：一屏完成前缀识别、长度提示、品牌标签与输入示例，轻量直接；建议保留并补 Luhn 与 Maestro/Diners/MIR，修正「卡等级」文案。
- **isbn-validator**：ISBN-10/13 双校验、双向转换、GS1/组号/出版者分段与示例按钮齐备；修好 DOM 后是同类页中较完整的一版，建议保留并加批量校验/粘贴多行。
- **iban-validator**：mod-97、国家长度表、BBAN 结构与分段高亮组合专业；建议补全国家/示例并保留「仅校验格式，不验证账户真实性」的免责声明。
- **bic-validator**：8/11 位分段、ISO 3166 国家码校验与主题切换结构清晰；建议补「主办公室/测试码」说明与空格清洗，保留轻量单页形态。
- **currency-symbol**：153 条数据、五区域筛选、搜索、详情弹层与 CSV 导出覆盖面广；建议去重、标注 ISO 状态与停用项，保留离线查询与「代码优先于符号」的提示。
- **password-generator-advanced**：长度/字符集/排除/不重复/批量/预设/强度条组合完整，预设覆盖 PIN、强口令、API 密钥；建议实现真正的 passphrase 或删掉文案，历史不落盘，并保留预设一键生成。

- 本批实读 8 页，逐页通读整份 HTML（含内联 JS、公式框、deep-dive、FAQ、数据数组）；新增 32 条（高 3 / 中 15 / 低 14），编号 F-N114~F-N145。
- 旧条目复核：F-N13 的「期初租金时点」已修复（`lease-payment-calculator.html:627`），但 fee 由「未入现金流」改为「与本金融资同向相加」，方向仍错（见 F-N114）；F-N22 的「还清月数/最低比例」已修复，`showCompare` 未计剩余本金仍存在（见 F-N123）。
- 覆盖统计：`tools/finance/` 共 116 个 HTML（含 index.html），本批实读 8 页；审计文档累计提及约 72 个 finance 页面，其余约 43 页未逐页复扫。
- 验证边界：未做浏览器真机、英文态（`?lang=en-US`）、繁体、移动端与门禁（`_build.py`/`_test_static.py`/`_audit_links.py`/`_audit_assets.py`）验证；金额与校验用例均在 `node -e` 内存复算（ISBN/IBAN/BIC 另用真实合法/非法样例），未修改仓库代码、未运行构建、未做 git 写操作、未在仓库建临时文件。F-N128 的 DOM 结论来自 HTML 解析与规范，F-N136 的实体绕过路径需真机复核。

## 2026-11-04 审计补充（Q 批：校验器/文本类 8 页）

### F-N146 SWIFT/BIC 页：4-2-2-3 分组书写被直接判长度错误（低，确认缺陷）
- 问题：入口只做 `trim().toUpperCase()`，不清洗空格/连字符；汇款单常见的 `DEUT DE FF 500` 被当成 14 字符直接命中长度分支。同目录 `bic-validator.html` 的同类问题已记为 F-N137，本页（另一套实现）未同步修复。
- 证据：`tools/finance/swift-bic-validator.html:233`（仅 trim+uppercase）、`:238`（整体正则）、`:242-243`（长度分支）
- 复现：输入 `DEUT DE FF 500` → 「长度：14 字符（8 或 11）」+「❌ 长度必须为 8 或 11」；node 复算去空白后长度 11、正则 `^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?$` 通过。期望按 `DEUTDEFF500` 输出银行/国家/位置/分行四段。
- 影响：`tools/finance/swift-bic-validator.html`；照抄 SWIFT 报文/汇款单写法被判无效，用户误以为代码有误。
- 方案：先 `raw.replace(/[\s-]/g,'')` 再校验，长度行注明「已忽略 N 个分隔符」；分段诊断逻辑保持。

### F-N147 六个校验页共用「数据表/历史/趋势图」模板：结果为文本，趋势图永不绘制、CSV 只导历史摘要（低，确认缺陷）
- 问题：`__*Extras` 用 `parseFloat` 解析结果文本（结果以「输入：」开头），恒为 `NaN`，`nums.length>=2` 永不成立 → 「结果趋势」图一次都不会出现；「导出明细 CSV」导出的是历史表（输入 + 文本摘要），首次使用前为空，且没有任何「是否通过」的结构化列。
- 证据：`tools/finance/swift-bic-validator.html:314`（ResText）、`:356`（parseFloat）、`:360`（≥2 才画图）、`:395`（exportTable 历史表）；同构块：`uan-validator.html:307,349,352,388`、`aadhaar-validator.html:341,383,386,422`、`cpf-validator.html:336,378,381,417`、`esn-validator.html:321,363,366,402`、`ein-validator.html:306,348,351,387`
- 复现：连续校验 `DEUTDEFF`、`DEUTDEFF500`、`DEUTDEXX` → 「数据表」3 行，切「结果」无趋势图；点「导出明细 CSV」得到 3 行「输入/结果」文本而非校验结论。期望单值校验页不挂趋势图，或把结果落成 `{代码,是否通过}` 两列。
- 影响：上述 6 页；模板噪音让用户以为存在统计能力，实际只有输入回放。
- 方案：把 `__*_skip` 置真关掉图表与趋势，保留「最近校验」列表；若保留图表，记录「通过=1/不通过=0」的结构化字段而非结果文本。

- **留存建议（tools/finance/swift-bic-validator.html）**：保留「8/11 位分段 + ISO 国家码校验 + 逐段诊断」的清晰结构（比 bic-validator 更完整），修空格归一化后即可留；建议与 bic-validator 二选一或明确分工（两页功能重叠）；补「XXX=主办公室 / 测试码」语义说明。

### F-N148 UAN 页：字母被静默剔除，`10A1234567890` 判「格式有效」，与 deep-dive「含字母会提示错误」矛盾（中，确认缺陷）
- 问题：`digits = raw.replace(/\D/g,'')` 删掉任意非数字字符，只要剩下 12 位即通过；deep-dive 却写「含字母或位数不足会提示错误」，而公式框（`:153`）如实写「去除非数字字符」——同页三处口径不一致。
- 证据：`tools/finance/uan-validator.html:232-233`（trim + 剥离）、`:237-241`（仅按数字位数判）、`:189`（deep-dive 承诺）、`:153`（公式框口径）
- 复现：`10A1234567890` → 「✅ UAN 格式有效」；node 剥离后 `101234567890` 恰 12 位。`10O1234567890`（字母 O）同样通过。期望带字母即报「第 N 位含非法字符」。
- 影响：`tools/finance/uan-validator.html`；含字母串被判合法，文档自相矛盾。
- 方案：先判 `/[^0-9]/` 报错并指出位置再 return；仅放行空格/连字符，结果区回显归一化值；同步修 deep-dive 与公式框。

### F-N149 UAN 页：2/5/5 分段被标成「区域 / EPFO 办公室 / 序号」，无出处（低，待验证）
- 问题：结果区把 `digits[0:2]` 标为「区域」、`[2:7]` 为「EPFO 办公室」、`[7:12]` 为「序号」，公式框也作为「本页代码口径」陈述；EPFO 公开资料只定义 UAN 为 12 位编号，未定义该语义，页面未给来源，用户易把「区域」误读为所在邦。
- 证据：`tools/finance/uan-validator.html:153`（公式框分段）、`:245-247`（切片）、`:251-253`（输出标签）
- 复现：输入 `101234567890` → 「区域：10 / EPFO 办公室：12345 / 序号：67890」；按切片规则，任何以 `10` 开头的 UAN 都会显示「区域：10」，与该号实际办事机构无关。期望标注「仅展示分段，非官方语义」或删除段名。
- 影响：`tools/finance/uan-validator.html`
- 方案：标签改为「前 2 位 / 中 5 位 / 后 5 位（非官方语义）」，或补 EPFO 出处后再沿用现名。

- **留存建议（tools/finance/uan-validator.html）**：保留「12 位长度 + 首字符软判据」的透明口径与「无校验位」免责，轻量直给；修好字符白名单后可留；建议把无出处分段降级为「展示用切片」，并补「粘贴时带 UAN: 前缀自动清洗」的提示。

### F-N150 UAN/Aadhaar/CPF/EIN 四页：原始输入直接拼进 innerHTML（自 XSS），且四页未大写化（中，确认缺陷）
- 问题：四页都是 `trim()` 后原样插值 `${raw}`，未转义；与 `bic-validator.html`（F-N136）不同，这四页**没有** `toUpperCase()`，连「实体大小写绕过」都不需要——只要串里带足量数字通过长度门，`<img src=x onerror=alert(1)>` 会原样执行。
- 证据：`tools/finance/uan-validator.html:232`/`:236`；`aadhaar-validator.html:269`/`:273`；`cpf-validator.html:250`/`:254`；`ein-validator.html:241`/`:245`
- 复现：CPF 输入 `11144477735<img src=x onerror=alert(1)>` → 剥离后 11 位、通过长度门 → 「输入：」行渲染该标签并触发 `onerror`。期望只显示纯文本。
- 影响：上述 4 页；仅影响本机操作者，但输入常来自粘贴（聊天/邮件里的「示例税号」），仍属不应存在的执行面。
- 方案：统一加 `escapeHtml()` 后再插值，或「输入」行改用 `textContent`；四页共用同一渲染工具函数，避免逐页再犯。

### F-N151 Aadhaar 页：字母同样被静默剔除（`234123412346A` 通过），FAQ 只承认空格/连字符（低，确认缺陷）
- 问题：`digits = raw.replace(/\D/g,'')` 删掉字母；FAQ（`:197`）写「输入可含空格或连字符，页面会先归一化再校验」，隐含只有这两种分隔符可用；公式框（`:158`）与 deep-dive 均未说明任意字符会被吞。
- 证据：`tools/finance/aadhaar-validator.html:269-270`（剥离）、`:273`（回显 raw）、`:197`（FAQ）、`:284`（格式化只用 digits）
- 复现：`234123412346A` → 剥离 12 位且 Verhoeff 通过（node 复算 `234123412346` 校验值为 0）→ 「✅ Aadhaar 号码有效」；期望提示「末位含非法字符 A」。对照 `2341234123A6` → 只报 11 位，用户看不出字母被吞。
- 影响：`tools/finance/aadhaar-validator.html`；OCR/手输串里的杂字符被吞后误报有效。
- 方案：除 `[\s-]` 外一律报非法字符并指位；结果区回显「归一化后」号码便于对照。

### F-N152 Aadhaar 页：首位 0/1 分支只输出一句错误，丢失「输入/格式化」上下文（低，确认缺陷）
- 问题：`:279-281` 直接 return，结果区既不回显归一化号码也不显示长度，与常规分支（`:285-293` 固定输出 输入/格式化/长度/校验和）结构不一致；粘贴 `00-0000-0000-00` 时看不到页面解析成了什么。
- 证据：`tools/finance/aadhaar-validator.html:279-281`（早退）、`:285-288`（常规输出结构）
- 复现：输入 `00-0000-0000-00` → 结果区仅「❌ Aadhaar 不能以 0 或 1 开头」一行；期望并显示「输入 / 归一化：000000000000 / 长度：12」。
- 影响：`tools/finance/aadhaar-validator.html`
- 方案：该分支改为追加错误行后继续输出上下文，或复用统一的「输入/长度」头部。

- **留存建议（tools/finance/aadhaar-validator.html）**：Verhoeff 实现经 node 复算正确（`345678901238`、`234123412346` 通过，`234123412347` 失败），正反例与「不验证真实性」免责完整，是同类页里质量较高的一版，建议保留；失败时补「疑似第 N 位录错」的单错定位提示（Verhoeff 支持）；补多行/批量号码核验以覆盖表格场景。

### F-N153 Aadhaar/CPF 的 `<title>` 与 EIN 的描述被截成半句（低，确认缺陷）
- 问题：`<title>印度 Aadhaar 验证 - 场景的号码格式检查`、`<title>巴西 CPF 验证 - 场景的号码合法性检查` 中「场景的」前被截断，主谓缺失（与 F-N131 同源的模板截断）；EIN 的 description 断在「打开浏览器即可」，缺「使用」。
- 证据：`tools/finance/aadhaar-validator.html:20`、`tools/finance/cpf-validator.html:20`、`tools/finance/ein-validator.html:10`
- 复现：读 `<title>` 与 SERP 预览 → 「印度 Aadhaar 验证 - 场景的号码格式检查」；期望「印度 Aadhaar 号码验证 - 身份核验场景的格式检查」。
- 影响：上述 3 页；搜索结果出现残句，标题与正文关键词（「Aadhaar 号码验证器」）不一致。
- 方案：补全为完整句式并同步 og/twitter/JSON-LD，例如「印度 Aadhaar 号码验证 - 12 位格式与 Verhoeff 校验位检查」。

### F-N154 CPF 页：FAQ 称「含字母判为格式错误」，实际 `abc11144477735` 直接通过（中，确认缺陷）
- 问题：`:250-251` 剥离所有非数字；FAQ（`:197`）却说「含字母或位数不足会判为格式错误」。只要字母不改变数字位数，校验就走完并显示「✅ CPF 号码有效」；`:260` 的全同数字拦截也只覆盖 11 位同字，拦不住「字母 + 11 位」。
- 证据：`tools/finance/cpf-validator.html:250-251`、`:197`、`:260-262`
- 复现：`abc11144477735` → 「✅ CPF 号码有效」（node 剥离后 11 位、mod 11 双校验通过）；`11144477735@x` 同样通过。期望先判 `/[^0-9.\-\s]/` 报非法字符。
- 影响：`tools/finance/cpf-validator.html`
- 方案：同 F-N148：先做字符白名单校验并指出位置，再剥离 `.`/`-`/空格。

- **留存建议（tools/finance/cpf-validator.html）**：mod-11 双校验 + 「第 9 位注册地」映射表是差异化能力（与 cnpj-validator 互补），建议保留；修正 FAQ 与实现的字符口径；可补「粘贴多行批量校验」与 CNPJ 交叉链接。

### F-N155 ESN 页：HEX→「十进制表示」不是标准 11 位 ESN，两分支互不可逆（中，确认缺陷）
- 问题：`:257` 用 `parseInt(hex,16)` 直接转十进制（`80A1B2C3` → `02158080707`）；而 11 位十进制 ESN 的标准构成是「3 位制造商码 + 8 位序列号」（`128` + `10597059` = `12810597059`）。把页面自己给出的 `02158080707` 粘回 DEC 分支，前 3 位 `021` 被解析成制造商 `0x15`、序列号 `58080707`，与 HEX 分支的 `0x80 / A1B2C3（10597059）` 完全对不上，与 FAQ（`:192`）「同一设备两种形式可互转」相反。
- 证据：`tools/finance/esn-validator.html:257`（十进制输出）、`:261-262`（DEC 按 3+8 切）、`:192`（互转承诺）
- 复现（node 实算）：`80A1B2C3` → 页面十进制 `02158080707`，标准应为 `12810597059`；回填 `02158080707` → `0x15 / 58080707`（未知制造商），期望 `0x80 / 10597059`。
- 影响：`tools/finance/esn-validator.html`；用户按页面提示复制十进制去其它系统登记会填错设备标识。
- 方案：输出改为 `String(parseInt(hex.substring(0,2),16)).padStart(3,'0') + String(parseInt(hex.substring(2),16)).padStart(8,'0')`，文案写清「3 位制造商 + 8 位序列」。

### F-N156 ESN 页：清洗式识别让非法字符与保留制造商码都判「格式有效」（中，确认缺陷）
- 问题：`cleanHex` 删掉所有非 `0-9A-F` 字符，`A1B2C3D4G`（9 字符含非法 G）被裁成 8 位后判「✅ ESN HEX 格式有效」；同时 `0x00`（页面自己的 MFR_DB 标 `RESERVED`）与 `0xFF` 均照常通过，无保留值排除。
- 证据：`tools/finance/esn-validator.html:243`（清洗）、`:248`（8 位判定）、`:258`/`:269`（无条件 ✅）、`:232`（`'0x00':'RESERVED'`）
- 复现：`A1B2C3D4G` → ✅（期望「含非法字符 G」）；`00000000` → 「制造商 0x00 - RESERVED」+「✅ ESN HEX 格式有效」；`00000000000` → 同样 ✅（DEC 分支，0x00）。期望保留码判无效。
- 影响：`tools/finance/esn-validator.html`；垃圾串与保留码被视为可用 ESN，削弱校验意义。
- 方案：先按整体 `^[0-9A-F]{8}$` / `^[0-9]{11}$` 判形态（不清洗），再对 `0x00`/`0xFF` 输出「保留码，不可用」。

- **留存建议（tools/finance/esn-validator.html）**：HEX/DEC 双入口 + 制造商代码表 + 「ESN 已被 MEID 取代」提示，对小众旧设备检索仍有价值，建议保留；修正十进制拼接并排除保留码后可留；补一行「MEID 14 位请用 MEID 工具」的引导。

### F-N157 EIN 页：前缀「须为 IRS 有效前缀」完全未校验，`00-0000000` 判有效，12 等真实前缀反被标「其他」（中，确认缺陷）
- 问题：`IRS_PREFIX` 只有 21 项，`irsCampus = IRS_PREFIX[prefix] || '其他/现代分配'` 只用于展示，从未参与有效性判断，`:258` 是无条件 ✅。于是 `00-0000000` 显示「✅ EIN 格式有效」，而 deep-dive 自己的示例 `12-3456789`（12 属合法前缀）却显示「其他/现代分配」。公式框（`:153`）与 FAQ（`:193`）都承诺校验前缀落在有效范围；`:231` 注释还说前缀「now mostly legacy」，与输出标签「IRS 中心」的确定语气冲突。
- 证据：`tools/finance/ein-validator.html:153`、`:193`、`:231`、`:232-239`（21 项）、`:253`（查表兜底）、`:258`（无条件 ✅）、`:189`（示例 12-3456789）
- 复现：`00-0000000` → 「前缀：00 / IRS 中心：其他/现代分配 / ✅ EIN 格式有效」；`12-3456789` → 同样 ✅，中心显示「其他/现代分配」。期望 00 判无效、12 显示 Brookhaven。
- 影响：`tools/finance/ein-validator.html`；「前缀结构合法性」是本页唯一卖点，实际未生效。
- 方案：补全 IRS 现行前缀表（约 80 项）并作为硬判据：命中显示校区，未命中输出「❌ 前缀不在 IRS 分配范围」；表与文案同源。

### F-N158 EIN 页：公式写 `^\d{2}-\d{7}$`，实际任意分隔都通过（低，确认缺陷）
- 问题：公式框要求「两位-七位」的连字符格式，代码却剥离全部非数字，`:251` 再自造 `XX-XXXXXXX`；`1-2-3-4-5-6-7-8-9` 这类乱分隔照样通过。
- 证据：`tools/finance/ein-validator.html:153`（公式）、`:241-242`（剥离）、`:246`（只判位数）、`:251`（格式化）
- 复现：`1-2-3-4-5-6-7-8-9` → 「格式化：12-3456789」+「✅ EIN 格式有效」；期望按公式拒绝，或在结果注明「已忽略 8 个分隔符」。
- 影响：`tools/finance/ein-validator.html`；公式与实现互相打脸，用户无法判断到底哪种写法合法。
- 方案：二选一——严格按 `^\d{2}-\d{7}$`（并容错空格）；或把公式改成「剥离分隔符后须为 9 位数字」并回显归一化值。

- **留存建议（tools/finance/ein-validator.html）**：9 位格式 + 前缀→校区映射 + 「不验证真实性」免责的骨架可直接用，修好前缀判据后建议保留；补「SSN/ITIN 勿混用」提示与同目录税务类页交叉链接；`IRS 中心` 标签按实际语义改为「历史校区（多为遗产用途）」。

### F-N159 word-wrap 页：宽度 ≤2 且开「悬挂缩进」时死循环；宽度 1/负数会静默吞字符（高，确认缺陷）
- 问题：软换行 `avail = width - visualLen(prefix)` 可能为 0 或负。`takeByLen(rest,0)` 返回 `{text:'', rest:rest}`，`while(visualLen(rest) > width)` 永不推进 → 死循环；`avail<0` 时 `s.substr(0,-N)` 视作 0、`s.substr(-N)` 只留末尾 N 字符，中间字符被丢弃。`width` 仅靠 HTML `max=200` 约束（手输无效受控），`parseInt('-5')||20` 得 -5（负数 truthy），同样进入死循环。
- 证据：`tools/finance/word-wrap.html:308`（取值无 clamp）、`:321-324`（while + avail）、`:291-293`（takeByLen 的 substr 语义）、`:157`（仅 min/max 属性）
- 复现（node 模拟同函数）：宽度 2 + 悬挂缩进 → 100 次迭代仍未退出（死循环）；宽度 1 + 首行缩进 + 文本 `abcdef` → 输出 `["  ","f"]`，a–e 丢失；宽度 `-5` + 文本 `abcdefghij` → 连续 push 空串，死循环。期望宽度不足缩进时缩进置空或钳到下限。
- 影响：`tools/finance/word-wrap.html`；触发后标签页卡死，且丢字符违反 FAQ「不会增删字符」。
- 方案：入口 `width = Math.max(4, Math.min(200, parseInt(v) || 20))`；`avail = Math.max(1, width - prefix.length)`；`takeByLen` 加 `if(targetLen<=0) return {text:'', rest:''}` 或 `if(!chunk) break` 兜底。

### F-N160 word-wrap 页：首行缩进/悬挂缩进只在「软换行」生效，其余三模式静默忽略（中，确认缺陷）
- 问题：`prefix` 只在 `mode==='soft'` 分支计算（`:322`、`:329`），`hard`（`:331-338`）、`word`（`:339-351`）、`chinese`（`:352-365`）完全不读 `indent`/`hanging`；预设「英文条款按单词折行 50」正是 `mode:'word', hanging:true`（`:496`），勾了毫无效果。
- 证据：`tools/finance/word-wrap.html:322`/`:329`（仅 soft）、`:331-365`（三模式无 prefix）、`:496`（预设组合）
- 复现：选预设「英文条款按单词折行 50」→ 续行无 2 空格悬挂缩进；在「按单词」模式勾选悬挂缩进亦无变化。期望各模式一致生效，或置灰控件并注明「仅软换行」。
- 影响：`tools/finance/word-wrap.html`；预设与选项组合看起来支持、实际无效。
- 方案：把 prefix 计算移到 `paragraphs.forEach` 内按模式复用（word 模式按 `width - prefix` 折行）；或按模式禁用两枚勾选框并加说明。

### F-N161 word-wrap 页：「按字节」口径自相矛盾（勾选写 2 字节、FAQ 写 UTF-8 3 字节），宽字符漏计（中，确认缺陷）
- 问题：`:287`/`:296` 只把 `[\u4e00-\u9fff\uff00-\uffef]` 记 2 字节；勾选框（`:173`）写「按字节（中文 2 字节）」，deep-dive（`:218`）与 FAQ（`:221`）却写「中文 UTF-8 占 3 字节」。同一控件两套口径；emoji 与 CJK 扩展 B 区（`\u{20000}+`）按 1 计，行宽失真。
- 证据：`tools/finance/word-wrap.html:173`、`:218`、`:221`、`:287`、`:296`
- 复现：勾选「按字节」+ 宽度 24，输入 `中文测试` → 页面计 8（2×4）；按 FAQ 的 UTF-8 口径应为 12。期望明确「按 GBK 双字节」或改真 UTF-8 3 字节。
- 影响：`tools/finance/word-wrap.html`；固定宽度报表/老系统字段按错口径折行。
- 方案：统一为 UTF-8 字节（正则扩到 `\p{Script=Han}` + emoji，按码点判 3/4 字节），或把三处文案统一改成「中文按 2 字节（GBK）」。

### F-N162 word-wrap 页：「按中文断句」对无标点长句完全不折行（中，确认缺陷）
- 问题：`chinese` 分支只有「放得下就接、放不下就整段换行」，没有字符级兜底；不含标点的长句（单 token 长于 width）会被整体压成一行，输出超出设定宽度。
- 证据：`tools/finance/word-wrap.html:354`（token 正则）、`:356-362`（无强折兜底）
- 复现：宽度 20、输入 45 字无标点中文（`这是一个没有任何标点的超长连续中文句子用于测试按中文断句模式是否会在宽度不足时继续强行折行`）→ 输出单行 45 字（node 复算 maxLen=45）。期望超长 token 退回软换行逐字切分。
- 影响：`tools/finance/word-wrap.html`；中文长条款/公告在窄栏里溢出。
- 方案：`else` 分支判定 `visualLen(tok) > width` 时对 tok 用 `takeByLen` 逐段 push，再收尾剩余部分。

### F-N163 word-wrap 页：「导出明细 CSV」不导换行结果；opt-guide 按钮名/适用场景是套话；「预设」页签无独立面板（低，确认缺陷）
- 问题：① `__word_wrapExport` 导出 `#word_wrapTable`（历史表），不含换行后的文本，无历史时为空；② opt-guide 写「点击『计算』或『生成』按钮」，实际按钮是「换行」；③ opt-guide/opt-faq 的适用场景是「个人或家庭的理财规划、贷款与投资收益测算」，与文本换行无关（`:565`）；④ 页签 `pre` 映射到输入卡片内的 `#word_wrapPresets`（`:570`），点「预设」只是隐藏结果区，预设栏本来一直可见。
- 证据：`tools/finance/word-wrap.html:176`（预设栏在输入卡片内）、`:488-490`（exportTable 历史表）、`:565`（opt-guide/opt-faq 套话）、`:570`（pre→word_wrapPresets）
- 复现：换行一段文本 → 点「导出明细 CSV」→ `word-wrap.csv` 只有历史行（首次为空）；点「预设」页签 → 结果区消失、无新面板。期望导出当前结果，或把按钮改成「复制结果」；页签要么去掉要么迁出预设栏。
- 影响：`tools/finance/word-wrap.html`
- 方案：`__word_wrapExport` 改为导出 `#result` 文本（或加「导出结果 TXT」）；修 opt-guide 按钮名、换成本工具真实场景；删除 `pre` 页签或把 `#word_wrapPresets` 移入面板。

- **留存建议（tools/finance/word-wrap.html）**：四模式 + 场景预设 + 一键复制/清空，作为通用文本工具价值明确（不属金融但属高频），**修好死循环与丢字符后必须保留**；建议把「按字节」改成 GBK/UTF-8 可选项并让缩进在四模式统一生效；补「导出结果 TXT」以兑现导出承诺。

### F-N164 word-search 页：简介/FAQ 承诺「自定义词表、网格大小、方向、可打印」，实际固定 12×12 + 20 词池、零输入控件、无打印（高，确认缺陷）
- 问题：页面只有「开始/重置」两个按钮，全文 `<input>/<textarea>/<select>` 数量为 0（node 计数 0/0/0）；`SIZE=12` 与 `wordPool`（20 个动物词）均为常量；`placeWord` 只在 `[0,1]/[1,0]/[1,1]/[-1,1]` 四向随机；`window.print`/`@media print` 完全不存在。但 meta/og（`:10`/`:15`）、intro（`:155`）、deep-dive（`:189`/`:192`）、FAQ（`:195-196`）都宣称可自定义词表与网格大小/方向、可打印。
- 证据：`tools/finance/word-search.html:10`/`:15`、`:155`、`:189`、`:192`、`:195-196`、`:234-235`（常量）、`:163-164`（仅两个按钮）、`:263`（四方向）
- 复现：页面上找不到任何词表/尺寸输入 → 「开始」只生成 12×12、最多 8 个固定动物词；打印预览无专门样式。期望至少提供「词表 textarea + 尺寸 + 方向」，或删除全部承诺文案。
- 影响：`tools/finance/word-search.html`；宣传的核心玩法不存在，属承诺未实现。
- 方案：二选一——① 加 `#wordlist`（逗号分隔）+ 尺寸（8–15）+ 方向复选框，`SIZE` 改读输入并加打印 CSS；② 删除自定义/打印文案，改为「内置 20 个动物词、12×12 随机网格」。

### F-N165 word-search 页：练习成绩历史恒为 0，趋势图/导出按钮永不出现（中，确认缺陷）
- 问题：`__tbn` 取 `found.size`，但 `found = new Set()` 后紧接着 `render()`（`newGame` 内），`render` 只在开局调用一次（`:259`），`__tbn` 也只挂在 `render` 包装上（`:495`）→ 每次记录都取到 0；`:474` 的 `last.v !== acc` 去重使历史恒为 1 条，`:480` 的 `hist.length < 2` 分支永久停在「练习 2 次以上后显示成绩趋势图」。
- 证据：`tools/finance/word-search.html:258-259`（清空 found 后立即 render）、`:462-464`（取 found.size）、`:474`（去重）、`:480`（<2 提示）、`:495`（仅包装 render）
- 复现：玩到「全部找到」（found.size=8）→ 再点「开始」→ 页面下方仍是「练习 2 次以上后显示成绩趋势图。」；localStorage `__tbn_word_search` 只有 `[{t,v:0}]`。期望按局记录 `found.size`。
- 影响：`tools/finance/word-search.html`；成绩、趋势、CSV 三项能力全部失效。
- 方案：在 `endSelect` 命中后（`:357-359`）或通关时调一次 `__tbn()`，并把「上一局成绩」缓存后在 `newGame` 中记录；去重改用 `{t,v}` 整体比对。

### F-N166 word-search 页：公式框仍是占位套话，引据表写「子串匹配（可区分大小写/正则）」与页面无关（低，确认缺陷）
- 问题：`formula-desc` 是站点占位模板（「本工具为纯前端在线工具…依据对应领域标准与规范进行计算或处理，结果仅供参考」+「工具名称：找词游戏 - 金融财务领域的在线工具」）；`constRefBox` 的「文本查找 / 子串匹配（可区分大小写/正则） / 字符串匹配算法」是文本工具模板，页面既无文本查找也无正则。
- 证据：`tools/finance/word-search.html:152-153`、`:216-217`
- 复现：打开页面 → 工作原理下方显示「依据对应领域标准与规范进行计算或处理」；引据表列出「正则」能力，页面无任何搜索框。期望改为「随机装填 + 划选方向判定」的真实说明。
- 影响：`tools/finance/word-search.html`；套话削弱可信度，并误导用户以为可正则搜索。
- 方案：按 AGENTS 占位指纹清理 `formula-desc`；引据表换成「网格装填（随机放置/失败重试）/ 方向向量（行列增量）/ 命中判定（正向 + 反向）」三行。

### F-N167 word-search 页：`__tbn` 的成绩标签中英分支字面相同，英文态仍显示中文（低，确认缺陷）
- 问题：`var LBL = EN ? '已找到词数' : '已找到词数'` 两分支完全相同；同块 `T.hist/T.sc` 却有英文版，于是英文态会出现「Practice History（已找到词数）」混排，图表图例也仍是中文。
- 证据：`tools/finance/word-search.html:467-469`
- 复现：静态推演 `?lang=en-US`：标题 `Practice History（已找到词数）`；表格头用 `T.sc` 正常显示 `Score`，但图表系列名/标题用 `LBL` 仍为中文。期望 `EN ? 'Words found' : '已找到词数'`。
- 影响：`tools/finance/word-search.html`（英文态）
- 方案：`LBL` 英文分支改 `Words found`；顺带核对 `T` 其余键是否都被引用。

- **留存建议（tools/finance/word-search.html）**：12×12 网格 + 八词随机 + 拖动/触摸划选 + 反向命中的交互完整，作为休闲记忆游戏可留（且 `cat=game` 属游戏类，放在 finance 行业与主题不符，若保留建议按 §7 评估迁移到 `tools/fun/`，走重定向存根并提死链）；**修好成绩历史（F-N165）并删除未实现的词表/尺寸/打印文案（F-N164）后才适合继续对外**；游戏本身建议保留「内置词池 + 一键开始」的零配置形态。

### 承诺 vs 实际（Q 批专项）
- **word-search**：宣称「支持自定义词表与网格大小」「词表可以自定义吗？可以」「支持设定网格大小与方向」「页面提供可打印视图」——实际零输入控件、`SIZE=12` 常量、20 词固定池、无任何打印实现（`:10`/`:15`/`:155`/`:189`/`:192`/`:195-196` vs `:234-235`/`:163-164`）。**未实现**。
- **word-search 成绩历史**：「练习 2 次以上后显示成绩趋势图」「导出 CSV」——实际历史恒 0、永不满足 `<2` 分支，图表与导出按钮永不出现（`:474`/`:480` vs `:464`/`:495`）。
- **EIN 前缀校验**：「前两位须为 IRS 分配的有效 EIN 前缀」「页面主要校验长度、数字格式与前缀分区是否落在有效范围」——实际前缀只用于查表展示，无条件判有效，`00-0000000` 通过（`ein:153`/`:193`/`:189` vs `:253`/`:258`）。
- **UAN 字符规则**：「含字母或位数不足会提示错误」——实际字母被静默剥离，`10A1234567890` 判有效（`uan:189` vs `:233`）。
- **CPF 字符规则**：「含字母…会判为格式错误」——实际 `abc11144477735` 判有效（`cpf:197` vs `:251`）。
- **ESN 互转**：「同一设备两种形式可互转」——实际 HEX→DEC 输出非标准 11 位（页面 `02158080707`，标准 `12810597059`），回填后制造商/序列号全错（`esn:192` vs `:257`/`:261`）。
- **Aadhaar 归一化**：「输入可含空格或连字符，页面会先归一化」——实际连字母一起剥离（`234123412346A` 通过），归一化范围未披露（`aadhaar:197` vs `:270`）。
- **word-wrap 字节口径**：「按字节（中文 2 字节）」与「中文 UTF-8 占 3 字节」并存；且「不会增删字符」在宽度 1/负数时被打破（`word-wrap:173`/`:218`/`:221`/`:222` vs `:287`/`:293`）。
- **word-wrap 导出**：「可复制结果或导出使用」「导出明细 CSV」——实际导出的是历史摘要表，换行结果只能复制（`word-wrap:565`/`:176` vs `:490`）。
- **8 页共有的功能特点**：「采用标准金融计算公式」「支持多种参数灵活配置」——6 个校验页各只有一个文本框、无参数可配，格式校验也无「公式」；word-wrap/word-search 是文本/游戏工具，与金融无关（`swift:451-452`、`uan:444-445`、`aadhaar:478-479`、`cpf:473-474`、`esn:458-459`、`ein:443-444`、`word-wrap:550-551`、`word-search:446-447`）。**与实现不符，属模板套话**。

### 覆盖
- 实读 8 页（逐页通读整份 HTML：head/meta/title、公式框、简介、deep-dive、FAQ、constRef 表、opt-guide/opt-faq、内联 JS 与 TBKit 注入块）。新增 22 条（高 2 / 中 10 / 低 10），编号 F-N146~F-N167。
- 旧条目复核：本批 8 页此前无独立条目；F-N136/F-N137 属 `bic-validator.html`（同功能的另一实现），本页 `swift-bic-validator.html` 未重复立条；已确认现有最大号为 F-N145，本批从 F-N146 连续编号。
- 算法结论均 `node` 内存复算：Verhoeff（`345678901238` / `234123412346` 通过、`234123412347` 失败，实现正确）；CPF（`11144477735`、`52998224725` 通过，`52998224726` 失败）；ESN（HEX/DEC 交叉对照与标准 3+8 拼接）；word-wrap（宽度 2+悬挂死循环、宽度 1 丢字符、宽度 -5 死循环、中文长句 45 字不折行）；UAN/EIN/CPF/Aadhaar 的剥离行为。临时脚本在 `/tmp/finaudit.js`、`/tmp/fin2.js`，未在仓库建文件。
- 未覆盖说明：`tools/finance/` 其余约 107 页未复扫；本批仅静态审计，未逐页核对 `?lang=en-US` 英文态、繁体、移动端与打印表现；F-N150 的脚本执行路径、F-N164 的打印效果需真机复核。
- 验证边界：未开浏览器、未跑 `_build.py`、未跑门禁（`_test_static.py`/`_audit_links.py`/`_audit_assets.py`/`run_gates.py`），未做任何 git 写操作，未修改仓库代码。

### F-N168 CNPJ 页：非数字字符被静默剥离，含字母的号码照样判有效（中，确认缺陷）
- 问题：`validate()` 先 `raw.replace(/\D/g,'')` 把字母与其它符号一并删除，再只按清洗后的位数判形态（`:258`），`:263` 又用清洗结果自造格式化串。公式（`:157`）与简介（`:160`）都写「14 位数字」，FAQ 也未披露「会先剥离非数字」。
- 证据：`tools/finance/cnpj-validator.html:157`、`:160`、`:254`、`:258`、`:263`
- 复现（node 实算）：`11ABC2223330001-81` → 清洗后 `11222333000181`（14 位）→ `cnpjCheck` 返回 `true`，页面输出「✅ CNPJ 号码有效」；对照真·非法 `11222333000182` → `false`（❌，符合预期）。期望前者点名「含非法字符 A/B/C」。
- 影响：`tools/finance/cnpj-validator.html`；把字母 O/I 误当 0/1 的录入错误会被"自动修正"成通过，校验失去意义。
- 方案：先做原始串白名单（仅 `0-9` 与 `.`/`/`/`-`/空格），非法字符输出位置与字符；再剥离并回显归一化值。

### F-N169 CNPJ 页：全同数字报「校验和失败」，与 mod-11 实际结果矛盾（低，确认缺陷）
- 问题：`:245` 的全同数字短路先返回 false，`:274` 却统一输出「❌ 校验和失败，CNPJ 无效」。但全 0 的两个 mod-11 期望值恰为 0/0，与末两位一致——校验和其实"通过"，失败原因是「数字全同」而非「校验和」。
- 证据：`tools/finance/cnpj-validator.html:245`、`:248-250`、`:270-274`
- 复现（node 实算）：`00000000000000` → 页面「❌ 校验和失败」；复算 `d1=0`、`d2=0`，与 `digits[12]/[13]` 均为 0（校验和相符）。合法对照 `00000000000191`（Banco do Brasil）→ ✅。
- 影响：`tools/finance/cnpj-validator.html`；用户按提示去改校验位永远改不对，错误定位误导。
- 方案：全同数字单独输出「全部数字相同，非有效 CNPJ」，与「校验和不符」分开。

- **留存建议（tools/finance/cnpj-validator.html）**：双 mod-11 + 根号/分支号/校验位拆分 + 合法默认样例，骨架正确，建议保留；补齐字符白名单（F-N168）并拆分全同数字提示（F-N169）后可对外；建议与 CPF/CNPJ 类工具互链并保留「不验证真实性」免责。

### F-N170 GST 页：州码只用于展示，`00`/`99` 等非法州码也判有效（中，确认缺陷）
- 问题：`stateName = STATE_CODES[stateCode] || '未知州'` 仅用于拼展示文案（`:283`），有效性判断（`:291`）只看 `zChar==='Z'` 与末位校验字符，州码从不参与；而 FAQ（`:196`）承诺「拦截录入错误」、deep-dive（`:191`）把州码列为 15 位结构的首段，实际错填州码不会被拦截。
- 证据：`tools/finance/gst-validator.html:248-258`、`:283`、`:291`、`:191`、`:196`
- 复现（node 实算）：`00AAPFU0939F1ZB` → 页面「州代码：00 - 未知州」「✅ GST 号码有效」；`99AAPFU0939F1ZK` 同样 ✅；对照合法 `27AAPFU0939F1ZV` → ✅、错校验位 `27AAPFU0939F1ZW` → ❌。
- 影响：`tools/finance/gst-validator.html`；跨州错填（如把 27 输成 00）无法拦截，与 FAQ「拦截录入错误」不符。
- 方案：州码白名单硬判（含 37/38），未命中输出「❌ 州码不在 GST 州列表」并保留输入定位。

### F-N171 GST 页：州码表仍把 25/26 分列，2020 年合并后 25 已停用（低，确认缺陷）
- 问题：`STATE_CODES` 保留 `'25':'Daman and Diu'`、`'26':'Dadra and Nagar Haveli'`。两属地 2020-01-26 合并为「Dadra and Nagar Haveli and Daman and Diu」，GST 州码统一为 26，25 不再分配；页面仍对 25 判有效并显示旧名，26 也只显示半名。
- 证据：`tools/finance/gst-validator.html:254-255`、`:283`
- 复现（node 实算）：`25AAPFU0939F1ZZ` → 「州代码：25 - Daman and Diu」+ ✅；`26AAPFU0939F1ZX` → 「26 - Dadra and Nagar Haveli」+ ✅（缺「and Daman and Diu」）。
- 影响：`tools/finance/gst-validator.html`；现行税号显示过时行政区名，25 号段被误认为可用。
- 方案：删除 25 映射，26 改为全称；如仍需兼容历史数据，标注「25 已于 2020 合并至 26」。

- **留存建议（tools/finance/gst-validator.html）**：15 位拆分 + mod-36 校验 + 州码表是差异化能力，建议保留；补州码硬校验（F-N170）并更新 25/26（F-N171）后可对外；建议补「PAN 第 4 位实体类型」说明与 GSTR 类工具互链。

### F-N172 IMEI 页：期望校验位相位算错，15 位页内自相矛盾、14 位合法主体被判无效（高，确认缺陷）
- 问题：① `:269-278` 的 `expectedCheck` 把整串 `digits`（15 位时含校验位本身）从右往左以 `alt=false` 起步求和，再把 `(10-sum%10)%10` 当「期望位」；对任何 Luhn 合法的 15 位号码 `sum%10=0` → 期望恒为 0，与真实校验位（末位）必然不等，同页出现「校验位 9（期望 0）❌」与「✅ IMEI 号码有效」。② `:263` 对 14 位输入直接补 `'0'` 再跑 Luhn，等价于「要求真实校验位必须为 0」，约九成合法 14 位主体被判「❌ Luhn 校验失败」，且 `:283` 的「建议值」同样错（14 位时相位也反）。
- 证据：`tools/finance/imei-validator.html:255-264`、`:269-278`、`:283`、`:285-289`
- 复现（node 实算）：`356938035643809`（15 位，`luhnCheck` = true）→ 页面「校验位：9（期望 0）❌」+「✅ IMEI 号码有效」；`49015420323751`（14 位主体，真实校验位 8、页面建议 0）→ 补 0 后 `false` →「❌ Luhn 校验失败」。
- 影响：`tools/finance/imei-validator.html`；正确串号被判无效、错误「建议位」把人引向更错的号，属核心算法缺陷。
- 方案：`expected = luhnCheckDigit(prefix)`（从右起 `alt=true`）；14 位分支用 `prefix + expected` 判定并展示该位，不再补 `'0'`；15 位直接用 `check === expected`。

### F-N173 IMEI 页：IMEI / IMEISV 位数口径与 GSMA 规范不符，16 位 IMEISV 被直接拒绝（中，确认缺陷）
- 问题：公式（`:153`）写「IMEI 14 位，IMEISV 15 位」，输入标签（`:158`）写「15 位数字」，FAQ（`:192`）又写「14 位为设备主体…第 15 位是校验位；也有末两位为软件版本号」。3GPP TS 23.003 / GSMA 口径为：IMEI 15 位（14 + 1 校验位），IMEISV 16 位（14 + 2 位 SVN）。
- 证据：`tools/finance/imei-validator.html:153`、`:156`、`:158`、`:192`、`:255`
- 复现：合法 IMEISV `3569380356438097`（16 位）→ 页面「⚠️ IMEI 必须为 14 或 15 位数字（当前 16 位）」；合法 IMEI `356938035643809` → 进入校验（但期望位错，见 F-N172）。
- 影响：`tools/finance/imei-validator.html`；IMEISV 用户无法使用，FAQ 的「末两位为软件版本」也未落到实现。
- 方案：文案统一为 IMEI=15 / IMEISV=16；长度分支支持 16 位，末 2 位按 SVN 展示、不参与 Luhn。

- **留存建议（tools/finance/imei-validator.html）**：TAC/SNR 分段 + 离线型号表 + 二手设备场景，对串号核对仍有价值，建议保留；必须先修校验位相位与 14 位分支（F-N172），再补 16 位 IMEISV（F-N173）；可加「IMEI 逐步被 MEID 取代」的引导。

### F-N174 字数统计页：可读性「平均句长」按空白切分，纯中文恒 0.x 词/句、难度恒「简单」（中，确认缺陷）
- 问题：`words` 由空白切分（`:343`），`avgWordsPerSentence = words / sentences`（`:374`）、`difficulty` 按 >20/>12 判（`:376-378`）。中文句间无空格，整段只算 1 个"词"，可读性结论失真；与公式（`:194`）「英文单词 = [a-zA-Z]+」和 FAQ（`:255`）「汉字按字计数」的口径不一致。
- 证据：`tools/finance/word-counter.html:194`、`:255`、`:343`、`:348`、`:374-378`
- 复现（node 实算）：纯中文三句 `这是一个用于测试可读性的中文句子。它没有空格分隔词语。统计结果会显示平均句长。` → words=1、sentences=3、avg=0.3、难度「简单」；中英混排 `I love ToolBox. It is great! 中文也要统计。` → words=7（中文段算 1 词）、avg=2.3。
- 影响：`tools/finance/word-counter.html`；面向中文稿件时「平均句长/难度」无参考价值，且与宣传的「区分单词与汉字」矛盾。
- 方案：词数改用 `englishWords + chineseChars`（或按字符折算），难度阈值改按「词/字每句」并在 UI 注明口径；中英混排分别展示。

### F-N175 字数统计页：「显示词频」只统计英文，纯中文时列表与图表恒为空（中，确认缺陷）
- 问题：`showDensity` 先算出 `chineseSegments`（`:394`）却从未使用；计数只取 `text.toLowerCase().match(/[a-z]+/g)`（`:393-404`）。纯中文文本勾选「显示词频」后 `:406` 生成空列表，`:413` 仍强制显示区块，`#wcChart`（`:449-467`）同样只取拉丁词而画不出图。
- 证据：`tools/finance/word-counter.html:205`、`:215-218`、`:391-413`、`:450-467`、`:328-329`
- 复现（node 实算）：纯中文 `中文词频测试 中文词频测试` → `englishWords=0`、`chineseSegments=4` → 词频 0 项、图表空白；对照 `ToolBox toolbox` → 2 项正常。
- 影响：`tools/finance/word-counter.html`；中文用户的核心功能（中文高频词）不可用，页面宣称「高频词统计（前 10）」名不符实。
- 方案：把 `chineseSegments` 并入同一 `countMap`（中文按 2–4 字 n-gram），纯中文时无结果则提示「未检测到统计词」并隐藏区块。

### F-N176 字数统计页：deep-dive 示例数字全错，且「代码点」口径与 `text.length` 不符（低，确认缺陷）
- 问题：`:252` 示例称「ToolBox 工具箱」汉字 4 个、英文单词 1 个、字符 8 个（不含空格）；实际为汉字 3、英文 1、不含空格 10（含空格 11）。另引据表（`:277`）写「Unicode 文本计数（代码点）」，而 `chars = text.length`（`:341`）按 UTF-16 码元计，emoji 会被算 2。
- 证据：`tools/finance/word-counter.html:252`、`:277`、`:341`
- 复现（node 实算）：`ToolBox 工具箱` → chars=11、noSpace=10、cn=3、en=1；`😀` → `text.length`=2（代码点应为 1）。
- 影响：`tools/finance/word-counter.html`；示例与实现互相打脸，降低可信度；含 emoji 的字符数与「代码点」承诺不符。
- 方案：示例改为实测 3/1/10；`chars` 改 `[...text].length`，或把引据表改为「UTF-16 码元」。

- **留存建议（tools/finance/word-counter.html）**：实时统计 + 可读性 + 词频 + CSV 导出是高频文本能力（不属金融但通用），建议保留；先统一「词」口径（F-N174）、补中文词频（F-N175）、修正示例（F-N176）后可对外；建议与 word-frequency/word-wrap 互链。

### F-N177 单词顺序反转页：「复制结果」用全局 `event`，复制成功后按钮永不变「已复制」（低，确认缺陷）
- 问题：`:327-330` 在 `navigator.clipboard.writeText(...).then()` 回调里用全局 `event.target.closest('.btn')`。事件处理器返回后 `window.event` 已置空（Firefox 无 `window.event`），回调抛 TypeError，按钮文案更新永不执行；复制本身已完成。
- 证据：`tools/finance/text-reverse-words.html:324-331`
- 复现：输入 `I love ToolBox` → 结果为 `ToolBox love I`（node 复算一致）；点「复制结果」→ 剪贴板拿到正确文本，但按钮仍显示「复制结果」，控制台 `Cannot read properties of null (reading 'target')`。
- 影响：`tools/finance/text-reverse-words.html`；用户以为没复制成功而重复点击。
- 方案：`function copyResult(ev){ var btn=(ev&&ev.target||document.activeElement).closest('.btn'); ... }`，或按 id 取按钮。

### F-N178 单词顺序反转页：「预设」页签映射到常显的工具栏 div，点按只是隐藏结果卡（低，确认缺陷）
- 问题：`:523` 把 `pre` 面板映射到 `#text_reverse_wordsPresets`，而该 div 位于输入卡工具栏（`:171`），本来常显、且不是独立面板；`:534-536` 的 `show('pre')` 只把结果/数据表/图表/历史全部 `display:none`，预设条位置不变。
- 证据：`tools/finance/text-reverse-words.html:171`、`:178-182`、`:523`、`:534-536`
- 复现：点「预设」→ 结果卡整块消失、页面无新面板出现；再点「结果」才恢复。期望预设面板独立呈现（含 4 个场景按钮）。
- 影响：`tools/finance/text-reverse-words.html`；页签看起来有 4 个能力，实际只有 3 个可用。
- 方案：去掉 `pre` 页签，或把 `#text_reverse_wordsPresets` 移入 `<div class="tbk-panel">` 独立容器。

### F-N179 单词顺序反转页：「保留标点」字符集缺中文引号/破折号/省略号，标点仍随词移动（低，确认缺陷）
- 问题：`:295` 的标点判定只含 ASCII `,.!?;:'"()[]<>` 与 `，。！？；：、`，不含 `「」『』（）《》〈〉`、`…`、`—`、`·`。勾选「保留标点位置」时这些符号被当作普通词参与反转。
- 证据：`tools/finance/text-reverse-words.html:295-298`、`:167`、`:218`
- 复现（node 实算）：`他说「你好，世界」。` → keepPunc 开输出 `」界世好你，「说他。`（引号跑到句首/词间）；`价格—优惠…` → `…惠优—格价`。对照 `Hello, world.` → `world, Hello.`（逗号句号原位）。
- 影响：`tools/finance/text-reverse-words.html`；中文文案倒置时标点错位，FAQ「标点仍在句末」不成立。
- 方案：标点判定改用 `/\p{P}/u`（Unicode 标点类）并保留空白分支，避免手写字符集漏项。

- **留存建议（tools/finance/text-reverse-words.html）**：三模式 + 保留标点 + 每行/首字母 + 预设 + 复制，作为文本小工具可用，建议保留；修 copy 反馈（F-N177）、预设页签（F-N178）、标点集（F-N179）后可留；`cat=text` 却归 finance 行业，建议按 §7 评估迁移（本批不做）。

### F-N180 NIE 页：X/Y/Z 前缀被写成「早期/中期/现行」，与 FAQ「当年批次」互相矛盾（低，确认缺陷）
- 问题：`:264` 的 `prefixDesc` 固定输出「外国人（早期/中期/现行）」，FAQ（`:193`）却写「X、Y、Z 分别对应当年批次的外国人编号，仅表示发放时段」。两处对同一编码给出不同的时间含义，且「当年批次」= 今年发放的说法与「早期/中期」直接冲突；页面未给任何权威出处。
- 证据：`tools/finance/nie-validator.html:193`、`:258-265`
- 复现（node 实算）：`X1234567L` → 「前缀：X - 外国人（早期）」✅；`Z1234567R` → 「Z - 外国人（现行）」✅；同页 FAQ 仍称「当年批次」。合法/非法对照：`X1234567L` ✅、`X1234567M` ❌（期望 L）。
- 影响：`tools/finance/nie-validator.html`；用户会据「早期/现行」推断证件年代或有效性，属无依据断言。
- 方案：统一为「X/Y/Z 是 NIE 的分配序列（X 最早），不代表身份类别或有效期」；删除「当年批次/早期/中期/现行」。

### F-N181 NIE 页：`nieCheck` 与 `validate` 双实现，`nieCheck` 零调用（低，确认缺陷）
- 问题：`:232-241` 定义了完整校验函数 `nieCheck`，`validate` 却在 `:258-263` 复制同一套映射与 mod-23 逻辑，`nieCheck` 全页仅出现 1 次（只有定义）。一旦改算法只改一处，「校验结论」与「展示期望字母」就会漂移。
- 证据：`tools/finance/nie-validator.html:232-241`、`:258-263`、`:267-273`
- 复现：`grep -c nieCheck` = 1；`X1234567L` ✅ / `X1234567M` ❌ 由 `validate` 内联逻辑得出，`nieCheck` 不参与任何判断。
- 影响：`tools/finance/nie-validator.html`；维护期易产生两套口径（同类问题已在 word-wrap 的 prefix 分支出现）。
- 方案：`validate` 改为调用 `nieCheck(raw)`，并把「期望字母」抽成 `nieLetter(raw)` 供展示复用。

- **留存建议（tools/finance/nie-validator.html）**：mod-23 + X/Y/Z 替换 + 期望字母回显，错误定位清晰，建议保留；修正前缀文案（F-N180）、收敛双实现（F-N181）后可留；建议与 CPF/CNPJ 页交叉链接。

### F-N182 ICCID 页：运营商表 4/5 位键永远查不到，默认样本显示「未知运营商」（中，确认缺陷）
- 问题：`:270-273` 取 `issuerFull = digits.substring(0,7)`、`issuer = digits.substring(4,7)`，`:280` 只用这两个键查 `TELCO_IIN`。但表内 `:255-257` 的键是 4/5 位（`'8944'`、`'89014'`）或 3 位（`'086'`），7 位键根本不存在 → 4/5 位条目不可达；3 位 `issuer` 是「第 5-7 位」，与 `'8944'` 这种「89+国家码」前缀语义也不同。
- 证据：`tools/finance/iccid-validator.html:255-258`、`:270-273`、`:280`
- 复现（node 实算）：`8944501234567890124` → `issuerFull='8944501'`、`issuer='501'` → 「未知运营商」；而表内明写 `'8944':'France'`。`TELCO['8944501']` 与 `TELCO['501']` 均为 `undefined`。非法对照 `8944501234567890123` → Luhn ❌。
- 影响：`tools/finance/iccid-validator.html`；「可能的运营商」几乎恒为未知，运营商标识能力形同虚设。
- 方案：按 E.118 变长结构解析出「国家码 + 发卡方」，再用前缀匹配（最长优先）；或把表统一改为 7 位 IIN 前缀并重建。

### F-N183 ICCID 页：非 `89` 前缀仍输出「✅ ICCID 有效」，与上一行 ⚠️ 自相矛盾（中，确认缺陷）
- 问题：`:278` 对 `iin !== '89'` 只给「⚠️ 通常为 89」，`:287-288` 的有效性仍只由 Luhn 决定，于是非电信行业标识的号码被判「ICCID 有效」。
- 证据：`tools/finance/iccid-validator.html:270`、`:278`、`:286-290`
- 复现（node 实算）：`88123456789012345676`（20 位、Luhn true）→ 「主要行业标识符：88 ⚠️ 通常为 89」+「✅ ICCID 有效」；合法对照 `8944501234567890124` → ✅。
- 影响：`tools/finance/iccid-validator.html`；任意 19/20 位 Luhn 合法数字都会被当成 ICCID，校验边界失效。
- 方案：`iin !== '89'` 直接判「❌ 非 89 电信行业标识，不是 ICCID」；或降级输出「格式校验通过（未验证行业标识）」并去掉 ✅。

### F-N184 ICCID 页：国家码/发卡方按固定 2+3 位切分，变长结构下国别解析错位（低，确认缺陷）
- 问题：`:271` 固定 `substring(2,4)` 取国家码、`:272` 固定 `substring(4,7)` 取发卡方。ITU-T E.118 的 ICCID 在 `89` 后国家码为 1–3 位、发卡方 1–4 位，长度可变；美国 `89 1 …` 会被解析成国家码 `12`、发卡方 `345`，整段错位。
- 证据：`tools/finance/iccid-validator.html:270-273`、`:279-281`
- 复现（node 实算）：`89123456789012345675`（20 位、Luhn true）→ 页面「国家代码：12 - 未知」「发卡机构标识符：345」；期望国家码 `1`（美国）、发卡方从第 4 位起。合法对照 `8944501234567890124` → 国家 44。
- 影响：`tools/finance/iccid-validator.html`；美/加等 1 位国家码的卡号全部误读，物联网批量核对会错判归属。
- 方案：内置国家码表做 1–3 位最长匹配，再按剩余前缀查发卡方；无法确定时只显示「89 + 未解析」。

### F-N185 ICCID 页：公式框写「前 3 位 MCC（国家码）+ 2 位 MNC」，与结果区/FAQ 互相矛盾（低，确认缺陷）
- 问题：`:149` 的 `data-zh` 与可见英文都称「前 3 位 MCC（国家码）+ 2 位 MNC（运营商）」，但结果区 `:278-281` 明确「前 2 位行业标识 89 / 第 3-4 位国家代码 / 第 5-7 位发卡方」，FAQ `:190` 也写「前 2 位行业标识(89)+国家码」。ICCID 没有 MCC/MNC 概念（那是 IMSI 的结构）。
- 证据：`tools/finance/iccid-validator.html:149`、`:190`、`:278-281`
- 复现：默认 `8944501234567890124` → 公式说前 3 位是国家码，结果区说 `89` 是行业标识、`44` 才是国家码；同页两套结构。
- 影响：`tools/finance/iccid-validator.html`；结构说明自相矛盾，误导对 ICCID/IMSI 的区分。
- 方案：公式改为「89(IIN) + 1–3 位国家码 + 发卡方 + 账户 + Luhn 校验位」，删除 MCC/MNC。

- **留存建议（tools/finance/iccid-validator.html）**：19/20 位 + Luhn + 分段展示对 SIM/物联网入库有实际价值，建议保留；先修运营商表键（F-N182）与 `89` 判定（F-N183）、再统一变长解析与公式（F-N184/F-N185）后可对外。

### F-N186 BIC 页：meta 与简介承诺「反向按行名检索代码」，页面完全没有该能力（高，确认缺陷）
- 问题：meta description（`:10`）与简介段（`:155`）都写「也可反向按行名检索代码」，但页面只有一个 BIC 输入框（`:157-158`），`validate`（`:271-307`）全程是「代码 → 银行/国家」单向查表；没有任何名称输入、反向索引或候选列表。
- 证据：`tools/finance/bic-lookup.html:10`、`:155`、`:157-158`、`:271-307`
- 复现：输入行名 `Deutsche Bank` → `:272` 取前 4 位 `DEUT` 恰好命中表，`:299` 因长度 13 输出「❌ BIC 长度应为 8 或 11 位」；合法对照 `DEUTDEFF` → ✅。页面无处可按名称检索。
- 影响：`tools/finance/bic-lookup.html`；SEO 描述与核心承诺不实，用户按承诺找不到入口。
- 方案：二选一——① 增加「银行名称 → BIC 候选列表」（`BANK_DB` 反向遍历 + 关键词匹配，列出银行/国家/建议 BIC）；② 删除 meta/简介中的反向检索表述，改为「按 BIC 查银行与国家」。

### F-N187 BIC 页：国家码不校验，`EF`/`ZZ` 等非 ISO 代码也判「BIC 格式有效」（中，确认缺陷）
- 问题：`:288-291` 只把国家码查 23 项 `COUNTRY_NAMES`，未命中显示「未知」；`:299-300` 的有效性只看长度 8/11，`:277` 只校验前 4 位字母。于是不符合 ISO 3166-1 的国家码（`EF`、`ZZ`）照样通过，位置码（第 7-8 位）也完全不校验。
- 证据：`tools/finance/bic-lookup.html:265-270`、`:277`、`:288-300`
- 复现（node 实算）：`ABCDEFGH` → 「国家代码：EF - 未知」+「✅ BIC 格式有效」；`DEUTZZFF` → 「ZZ - 未知」+ ✅；合法对照 `DEUTDEFF` → 「DE - 德国」+ ✅。
- 影响：`tools/finance/bic-lookup.html`；乱填的 8 位串被判有效，「格式有效」失去区分度。
- 方案：国家码须命中 ISO 3166-1 alpha-2 全集（可内置精简表）；位置码两字符须为 `[A-Z0-9]`；未命中统一 ❌ 并指出具体段（银行/国家/位置/分支）。

### F-N188 BIC 页：deep-dive「常见使用场景」与 FAQ 是通用操作教程套话，无 BIC 专属内容（低，确认缺陷）
- 问题：`:184-186` 的场景是「先阅读BIC Query的输入说明…只改变一个输入变量重新运行…保留输入参数与结果」，属模板填充；FAQ（`:191-192`）只有「结果可以直接用于正式业务吗/如何复核结果」两条通用问答，没有 8 位 vs 11 位、位置码含义、离线库覆盖范围等本页核心问题。
- 证据：`tools/finance/bic-lookup.html:184-186`、`:189-193`
- 复现：通读页面，无一处解释 8 位与 11 位差异或「查不到银行怎么办」；场景段仍是操作步骤。
- 影响：`tools/finance/bic-lookup.html`；内容与工具主题脱节，削弱专业度与长尾覆盖。
- 方案：场景改为「跨境汇款填单核对收款行 / 拆解 BIC 四段 / 判断是否需 11 位分支码」；FAQ 补 8/11 位差异、离线库仅含 34 家常见机构、查不到时的官方查询途径。

- **留存建议（tools/finance/bic-lookup.html）**：4+2+2+3 分段解析 + 离线银行表 + 国家名回显，作为汇款填单核对工具价值明确，建议保留；补反向检索或删除承诺（F-N186）、加国家码校验（F-N187）、替换套话内容（F-N188）后可对外。

### F-N189 6 个校验页 + 文本反转页：「导出明细 CSV」实为历史表，趋势图 div 永不出现（中，确认缺陷）
- 问题：① 趋势图取 `parseFloat(arr[j].d[rk])`，而 `rk` 存的是整段结果文本（`ResText` 截 80 字，如「输入： … 校验和： ✅ 通过」），`parseFloat` 恒 `NaN`，`nums.length>=2` 永不成立，`#xxxChart` 永远空白（`cnpj:365/368-369`、`gst:388-389`、`imei:382-383`、`text-reverse:405/408-409`、`nie:366-367`、`iccid:384-385`、`bic:395/398-399`）。②「导出明细 CSV」导出的是 `#xxxTable`（历史表），且 `ResText` 用 `/请输入|无效|不正确|错误|Error|NaN/` 过滤（cnpj:328、gst:348、imei:342、text-reverse:368、nie:326、iccid:344、bic:358），CNPJ/IMEI/NIE/ICCID 的失败样本从不入表；首次点击只剩表头。
- 证据：`tools/finance/cnpj-validator.html:323-329`、`:365-369`、`:402-404`；`tools/finance/gst-validator.html:343-349`、`:388-389`、`:422-424`；`tools/finance/imei-validator.html:337-343`、`:382-383`、`:416-418`；`tools/finance/text-reverse-words.html:363-369`、`:408-409`、`:442-444`；`tools/finance/nie-validator.html:321-326`、`:366-367`、`:400-402`；`tools/finance/iccid-validator.html:339-345`、`:384-385`、`:418-420`；`tools/finance/bic-lookup.html:353-359`、`:398-399`、`:432-434`
- 复现（node 实算）：cnpj 页输入 `11222333000182`（校验失败）→ 结果区 ❌，但「数据表/历史」无新增行、CSV 不含该次；`parseFloat("输入： 11222333000181 格式化： …")` = `NaN`，两次计算后 `#cnpj_validatorChart` 仍为空。
- 影响：7 个页面；「趋势图/明细导出」两个可见控件长期空转，用户会反复点击。
- 方案：历史记录增加数值字段（如 `ok: valid?1:0`）供趋势图使用；CSV 改导「当前结果 + 时间」（或按钮改称「导出历史 CSV」）；失败样本也入库并单列「结论」字段。

### 承诺 vs 实际（R 批专项）
- **BIC 反向检索**：meta「也可反向按行名检索代码」/简介同句——实际仅 code→bank 单向查表，输入行名 `Deutsche Bank` 得到「❌ BIC 长度应为 8 或 11 位」（`bic:10`/`:155` vs `:271-307`）。**未实现**。
- **IMEI 14/15 位互认**：「输入 14 或 15 位」「14 位时按规则补校验位」——实际 14 位补 `'0'` 判 Luhn，合法 `49015420323751`（真实校验位 8）被判无效；15 位合法号码又把末位一并求和得到「期望 0」，页面出现「校验位 9（期望 0）❌ + ✅ 有效」自相矛盾（`imei:156`/`:185`/`:192` vs `:263`/`:269-278`/`:283`）。
- **ICCID 结构**：「前 3 位 MCC（国家码）+ 2 位 MNC」——实际结果区按「前 2 位 89 / 第 3-4 位国家码 / 第 5-7 位发卡方」解析，且运营商表键不可达（`iccid:149` vs `:270-281`/`:255-258`）。
- **字数统计口径**：「区分单词与汉字」「英文单词 = [a-zA-Z]+」——实际可读性用空白切分的 `words`（中文整段算 1 词，纯中文 avg 0.3、难度恒简单），词频只统计 `[a-z]+`，`chineseSegments` 计算后弃用（`word-counter:194`/`:255` vs `:343`/`:374-378`/`:394-404`）。
- **字数统计示例**：「ToolBox 工具箱 → 汉字 4、字符 8」——实测汉字 3、不含空格字符 10（`word-counter:252` vs node 复算）。
- **导出明细 CSV**（7 页）：按钮名写「导出明细」，实际导出历史表且失败样本被过滤，首次只剩表头（`cnpj:402-404`、`gst:422-424`、`imei:416-418`、`text-reverse:442-444`、`nie:400-402`、`iccid:418-420`、`bic:432-434` 的 `exportTable('#xxxTable')` vs `ResText` 的 `/请输入|无效|不正确|错误/` 过滤，如 `cnpj:328`）。**名不符实**。
- **「数据表/历史」页签**：`数据表` 与 `历史` 指向同一份最近 10 条历史记录（`#xxxTable` 由 `TBKit.history.list()` 渲染），不存在「本次计算的明细表」；单输入校验页却给出 3 个页签（`cnpj:148-152`、`gst:144-148`、`imei:144-148`、`nie:144-148`、`iccid:139-143`、`bic:144-148`）。
- **8 页共有功能特点/场景套话**：均写「采用标准金融计算公式」「支持多种参数灵活配置」「个人理财与投资规划 / 贷款还款方案计算 / 投资收益分析」，而 6 个校验页各只有一个文本框、无参数可配，2 个文本页与金融无关（`cnpj:460-467`、`gst:480-487`、`imei:474-481`、`word-counter:517-524`、`text-reverse:504-511`、`nie:458-465`、`iccid:476-483`、`bic:490-499`）。**模板套话**。
- **BIC 离线库覆盖**：页面未说明 `BANK_DB` 仅 34 家；未知银行只给「未在离线数据库中」提示，无官方查询引导（`bic:229-264` vs `:285-287`）。
- **NIE 前缀含义**：「早期/中期/现行」与 FAQ「当年批次」并存且互斥（`nie:264` vs `:193`）。**无依据断言**。

### 覆盖
- 实读 8 页（逐页通读整份 HTML：head/meta/title、formula-box、intro、deep-dive、FAQ、constRef 表、内联 JS 与 TBKit 注入块）。新增 22 条（高 2 / 中 9 / 低 11），编号 F-N168~F-N189。
- 编号衔接：已确认 `plan/categories/02-金融财务/finance.md` 与本仓库 `plan/` 下现有最大号为 F-N167，本批从 F-N168 连续编号。
- 算法结论均 `node` 内存复算：CNPJ（`11222333000181` 通过 / `11222333000182` 失败 / `00000000000000` 两校验位期望 0、0 / 含字母串清洗后 14 位通过）；GST（`27AAPFU0939F1ZV`、`09AABCU9603R1ZL` 通过；`00AAPFU0939F1ZB`、`99AAPFU0939F1ZK`、`26AAPFU0939F1ZX`、`25AAPFU0939F1ZZ` 通过且州码未拦截）；IMEI（`356938035643809` Luhn 通过但页面期望位 5≠9；`49015420323751` 真实校验位 8、页面补 0 判失败并「建议 0」）；ICCID（`8944501234567890124` 通过但运营商未知、`8944501234567890123` 失败、`88123456789012345676` 非 89 仍通过、`89123456789012345675` 国家码被切成 12）；BIC（`DEUTDEFF` 通过、`ABCDEFGH`/`DEUTZZFF` 亦判有效）；字数统计（示例 3/1/10、纯中文 avg 0.3、emoji 长度 2）；文本反转（`I love ToolBox`→`ToolBox love I`、中文引号在 keepPunc 下移位、CRLF 下 `\r` 移到行首）。临时脚本在 `/tmp/audit8.js`，未在仓库建文件。
- 未覆盖说明：`tools/finance/` 其余 108 页（含 `index.html`）未复扫；本批仅静态审计，未逐页核对 `?lang=en-US` 英文态、繁体、移动端与打印表现；F-N177 的 `window.event` 表现、F-N189 的图表/CSV 实际下载内容需真机复核。
- 验证边界：未开浏览器、未跑 `_build.py`、未跑门禁（`_test_static.py`/`_audit_links.py`/`_audit_assets.py`/`run_gates.py`），未做任何 git 写操作，未修改仓库代码（仅本 plan 文件追加）。

### F-N190 TIN 页：任何 9 位数字都被兜底判成「EIN 格式有效」，全零串也通过（高，确认缺陷）
- 问题：`:253-254` 先判 SSN、`:262` 再判 ITIN，其余一律落入 `:267` 的 `else`，`:272` 直接输出 `✅ TIN/EIN 格式有效`；全程没有 EIN 前缀校验，也没有「不属于任何号段」的出口。
- 证据：`tools/finance/tin-validator.html:253-254`、`:262`、`:267-273`
- 复现（node 实算）：`000000000` → area `000` 不满足 SSN、不以 9 开头 → 落入 EIN → ✅；`666-00-0000`、`900-00-0000` 同样 EIN ✅。合法对照 `456789012` → SSN ✅；`912-70-1234` → ITIN ✅。
- 影响：`tools/finance/tin-validator.html`；全零、666 段、900 段等明确无效号段被判「格式有效」，校验器对乱填输入零区分度。
- 方案：EIN 分支加 IRS 前缀白名单（01-06、11-16、20-27、30-39、40-48、50-59、60-67、70-88、91-99 等），未命中输出 ❌「不属于 SSN/ITIN/EIN 任何号段」，取消 `else` 兜底。

### F-N191 TIN 页：注释写「按格式判型」，实际只看数字串位置，EIN 写法被判成 SSN（中，确认缺陷）
- 问题：`:243-245` 注释为 `// Determine type by formatting` 并列出 `SSN: XXX-XX-XXXX` / `EIN: XX-XXXXXXX`，但 `:246-249` 只对 `digits` 做 3-2-4 切片，从不读取连字符位置；`:253` 满足 SSN 号段即报 SSN。
- 证据：`tools/finance/tin-validator.html:243-245`、`:246-253`、`:255-260`
- 复现：`12-3456789`（2-7 的 EIN 写法）→ 输出「类型：SSN (社会安全号)」「SSN 格式：123-45-6789」；`45678-9012` 同样判 SSN。合法对照 `123-45-6789` → SSN ✅。
- 影响：`tools/finance/tin-validator.html`；用户按 placeholder「123-45-6789 或 12-3456789」输入 EIN，被改写成 SSN 并显示错位分段，报税/开户核对会误判类型。
- 方案：先按原文连字符位置判型（`\d{3}-\d{2}-\d{4}`→SSN，`\d{2}-\d{7}`→EIN），无连字符时按号段推断并在结果标注「按号段推断」。

### F-N192 TIN 页：非数字字符被静默剥离，`abc123456789xyz` 判 SSN ✅；公式框只写 SSN 正则（中，确认缺陷）
- 问题：`:233` `raw.replace(/\D/g,'')` 丢弃任意字母/标点，`:237` 只校验剩余 9 位；公式框 `:153` 给出的唯一格式 `^\d{3}-?\d{2}-?\d{4}$` 只覆盖 SSN，与标签「TIN/SSN/EIN」（`:158`）及 ITIN 分支（`:262`）不符。
- 证据：`tools/finance/tin-validator.html:153`、`:233`、`:237-238`、`:262`
- 复现：`abc123456789xyz` → 9 位 → SSN ✅（原串含 6 个字母）；`TIN:123456789#` 亦 ✅。非法对照 `12345678` → 「⚠️ TIN 必须为 9 位数字（当前 8 位）」。
- 影响：`tools/finance/tin-validator.html`；号码夹字母/中文零拦截，与「格式校验」承诺不符；公式框结构也不覆盖 EIN/ITIN。
- 方案：原串先做 `/^[\d-]+$/` 白名单，含非法字符即 ❌ 并回显位置；公式框改为三分支结构，列 SSN area/group/serial 与 EIN/ITIN 号段规则。

### F-N193 GSTIN 页：州码从不校验，`99`/`00` 命中校验位仍判「GSTIN 有效」（中，确认缺陷）
- 问题：`:248-258` 的 `STATE_CODES` 只用于取显示名，`:282` 未命中兜底为「未知州」后照常往下走；`:290` 的通过条件只有 `zChar==='Z'` 且校验位相等，而正则 `:270` 允许任意两位数字。
- 证据：`tools/finance/gstin-validator.html:270`、`:282`、`:287-294`
- 复现（node 实算）：把合法 `27AAPFU0939F1ZV` 的州码改为 `99` 并按页面算法重算校验位 → `99AAPFU0939F1ZK`：页面输出「州代码：99 - 未知州」+「✅ GSTIN 有效」；`00AAPFU0939F1ZB` 同样 ✅。合法对照 `27AAPFU0939F1ZV` → 州 27 Maharashtra + ✅；校验位算法与官方样例吻合（`27AAPFU0939F1ZV`、`09AABCU9603R1ZL` 均算出 V/L）。
- 影响：`tools/finance/gstin-validator.html`；州码填错（含 00、39-96 等未分配段）仍判有效，供应商备案核对会放过错误 GSTIN。
- 方案：州码须命中 `STATE_CODES`（补齐 38 Ladakh、97 Other Territory 等），未命中直接 ❌「州码未分配」；校验位算法保持不变。

### F-N194 GSTIN 页：引据表把段序写成「…实体 + 校验 + Z」，与公式框相反（低，确认缺陷）
- 问题：`:157` 公式框为「2 位州码 + 10 位 PAN + 1 位实体码 + Z + 末位校验字符」，`:217` 的 constRef 表却写 `2state+10PAN+ent+check+Z`，把校验位排在 Z 之前。
- 证据：`tools/finance/gstin-validator.html:157`、`:216-217`
- 复现：按 `:217` 的顺序拼 `27AAPFU0939F1` + 校验位 + `Z`，第 14 位非 Z，必被 `:270` 正则拒绝；按 `:157` 顺序拼接才通过。
- 影响：`tools/finance/gstin-validator.html`；同页两处结构说明冲突，用户自造/校号时会按错顺序。
- 方案：`:217` 改为 `2state+10PAN+ent+Z+check`。

### F-N195 TFN 页：权重表末位写成 11（官方 10），第 9 位完全不参与校验（高，确认缺陷）
- 问题：`:231` `TFN_WEIGHTS=[1,4,3,7,5,8,6,9,11]`，ATO 公开权重为 `1,4,3,7,5,8,6,9,10`。末位取 11 时该项 `11*d ≡ 0 (mod 11)`：只要前 8 位加权和为 11 的倍数，末位 0-9 全部通过；反之官方合法的号码会被拒。
- 证据：`tools/finance/tfn-validator.html:231`、`:238-243`（对照 `:153` 公式框写 10、`:192` FAQ 写 11）
- 复现（node 实算）：`100000062` → 页面加权和 77、`77%11=0` → ✅，官方权重和 75 → 余 9 → 应 ❌；`100000001` → 页面和 12 → 余 1 → ❌，官方和 11 → 余 0 → 应 ✅。合法对照 `876543210`（默认值）两套权重都 ✅；`123456782` 两套都 ❌（页面和 255）。
- 影响：`tools/finance/tfn-validator.html`；校验基本失效，10 个末位里 9 个错号能过、真号会被拒，是本批最严重的一处算法错误。
- 方案：`:231` 改为 `[...,9,10]`，FAQ `:192` 同步；补一条断言用例覆盖「末位权重 10」。

### F-N196 TFN 页：constRef 引据串乱码「权重271…签到」，FAQ 与公式框权重冲突（低，确认缺陷）
- 问题：`:213` 的引据单元格为「9 位；加权(权重271...签到)模 11 校验」，是明显的生成残留/乱码；`:192` 的 FAQ 写权重「…6、9、11」，`:153` 公式框写「…6、9、10」，同页三处（含 `:239` 的表）对应两个不同的末位权重。另有 8 位输入时 `:256` 的 `(\d{3})(\d{3})(\d+)` 会切成「123 456 78」这种 3-3-2 分段。
- 证据：`tools/finance/tfn-validator.html:153`、`:192`、`:213`、`:239`、`:256`
- 复现：`12345678` → 输出「格式化：123 456 78」；同一页 FAQ（`:192`）与公式框（`:153`）给出的权重列表最后一项分别是 11 与 10。
- 影响：`tools/finance/tfn-validator.html`；引据表的乱码直接影响可信度，权重口径不一让用户无法自行复算。
- 方案：`:213` 重写为「9 位；权重 1,4,3,7,5,8,6,9,10 加权求和 mod 11 = 0」；8 位格式化改 3-3-2 并显式标注「8 位视作前补 0」。

### F-N197 Sort Code 页：含字母的输入被判「格式有效」，与 deep-dive 承诺相反（中，确认缺陷）
- 问题：`:233` 先 `replace(/\D/g,'')` 再判长度，`:264` 只要剩 6 位数字就无条件输出 ✅；`:189` 明确承诺「含字母或位数不符会提示格式错误」。
- 证据：`tools/finance/sort-code-validator-validator.html:189`、`:233`、`:237-241`、`:264`
- 复现：`12A34B56` → 剥离为 `123456` → 「前缀 12 / 可能银行 National Westminster Bank」+「✅ Sort Code 格式有效」；`12-34-56abc` 同样 ✅。合法对照 `12-34-56` ✅；非法对照 `1234567` → 「⚠️ 必须为 6 位数字（当前 7 位）」。
- 影响：`tools/finance/sort-code-validator-validator.html`；抄错的字母串被当成合法分行代码，转账前核对失效，且与页面自己的承诺直接冲突。
- 方案：原串加 `/^\d{2}-?\d{2}-?\d{2}$/` 校验，仅允许空格/`-` 作为分隔，其余字符 ❌ 并回显。

### F-N198 Sort Code 页：公式框写的是代码实现说明（含映射键值），不是公式（低，确认缺陷）
- 问题：`:153` 的 `formula-eq` 是一段约 250 字的实现叙述（「本页代码口径…剥离非数字后须恰为 6 位（不足/超出提示…）…01/02/07/60→NatWest、08/11/30/90→Lloyds…」），把 `bankMap` 的键值直接摊在公式位；而本工具确无算术（`:192` 已声明「无算术校验位」）。
- 证据：`tools/finance/sort-code-validator-validator.html:153`、`:192`、`:246-259`
- 复现：页面「📐 工作原理与说明」读到的是开发者口吻的行为描述，与 `:246-259` 的 `bankMap` 键值一一对应；`12-34-56` 的实际输出只有「格式化/前缀/可能银行/✅」四行，无任何算式。
- 影响：`tools/finance/sort-code-validator-validator.html`；公式框与全站风格割裂，移动端整段长文难读，也暴露实现细节。
- 方案：公式框改为「6 位数字，写作 XX-XX-XX；无算术校验位，仅校验长度与字符集；前 2 位为清算行号段，仅供参考」；映射表移入正文表格并标注来源与覆盖范围。

### F-N199 PAN 页：第 4 位实体类型从不校验，未知类型与虚构类型仍判 ✅（中，确认缺陷）
- 问题：`:264-265` 只做 `CARD_TYPES[fourthChar] || '未知类型'` 的展示，`:272` 无条件输出 `✅ PAN 号码格式有效`；`:238-242` 的类型表还含非官方 `K:'Krishik (Krishi 信托)'`。
- 证据：`tools/finance/pan-validator.html:238-242`、`:248`、`:264-265`、`:272`
- 复现：`ABCZS1234E` → 「第 4 字符：Z - 未知类型」+「✅ PAN 号码格式有效」；`ABCKS1234E` → 「K - Krishik (Krishi 信托)」+ ✅。合法对照 `ABCPS1234E` → P Person ✅；非法对照 `ABCP01234E` → 「❌ 第 6-9 位必须为数字」。
- 影响：`tools/finance/pan-validator.html`；任意 `[A-Z]{5}1234[A-Z]` 都能过，页面上唯一的实质规则（实体类型）形同虚设。
- 方案：第 4 位须命中官方 10 类（A/B/C/F/G/H/J/L/P/T），未命中 ❌「实体类型字符非法」；`K` 删除或补权威来源后再保留。

### F-N200 PAN 页：末位只打印不校验却标为「校验位」；三处示例互不一致（低，确认缺陷）
- 问题：`:271` 输出「校验位：${lastChar}」，但代码从不计算期望值（`:266-272` 只有赋值与拼接）；`:160` placeholder `AABPS1234C`、`:196` deep-dive 示例 `ABCPD1234E`、默认值 `ABCPS1234E` 三处互不相同，示例也未解释各字母位含义。
- 证据：`tools/finance/pan-validator.html:160`、`:196`、`:266-272`
- 复现（node 实算）：`ABCPS1234E` 与 `ABCPS1234Z` 两个末位都输出 ✅，页面只把字母原样回显（无「期望」值）；三处示例长度均为 10、正则均通过，但字母不同。
- 影响：`tools/finance/pan-validator.html`；用户误以为末位被算法验过（PAN 末位无公开校验算法）；示例不统一削弱可信度。
- 方案：「校验位」改称「第 10 位字符」并注明「无公开算法，本页仅校验为字母」；placeholder/示例/默认值统一为同一真实号码。

### F-N201 CURP 页：默认值与 placeholder 都是 19 位，页面加载后既不显示 ✅ 也不显示 ❌（高，确认缺陷）
- 问题：`:159` 的 `value="BOXW310820HMNERNA08"` 与 placeholder `BOXW310820HMNERNA09` 均为 19 字符（CURP 应为 18 位）；`:261-266` 的失败分支只在 `raw.length === 18` 时才追加「❌ 格式不符」，19 位输入直接 `return`，结果区只剩「输入：…」与「长度：19 字符（应为 18）」。
- 证据：`tools/finance/curp-validator.html:159`、`:258`、`:260-266`
- 复现（node 实算）：默认值长度 19；去掉多余的 `0` 后 `BOXW310820HMNERNA8`（18 位，末位 8 与 `curpChecksum` 吻合）→ ✅ CURP 有效；打开页面则只有长度提示、无任何结论。
- 影响：`tools/finance/curp-validator.html`；首屏样例本身就是非法串且不给判定，用户无法分辨「号码错」还是「页面坏」；占位符同样误导复制。
- 方案：默认值与 placeholder 改为 18 位合法样例（`BOXW310820HMNERNA8`）；`:261-266` 对所有非法长度都输出 ❌ 并给出当前位数。

### F-N202 CURP 页：世纪判定用 `yy<30`，与官方「第 17 位是数字/字母」规则不符（中，确认缺陷）
- 问题：`:274` `let year = yy < 30 ? 2000+yy : 1900+yy;`；RENAPO 规则为「第 17 位（同音防重位，正则内 `[0-9A-Z]`，见 `:260`）为数字 → 1900-1999，为字母 → 2000-2099」，与出生年份两位数字无关。
- 证据：`tools/finance/curp-validator.html:260`、`:269`、`:274`、`:280`
- 复现（node 实算）：`GARW150820HMNERN58`（YY=15、同音位 `5` 为数字 → 官方 1915-08-20）→ 页面 `yy=15<30` 显示「2015-8-20」；对照 `GARW150820HMNERNA8`（同音位 `A` 为字母 → 2015）页面也显示 2015，两者恰好同值。
- 影响：`tools/finance/curp-validator.html`；1930 年前出生者的出生年会被推后 100 年，年龄核验/开户 KYC 场景直接错判。
- 方案：`year = /[0-9]/.test(homonym) ? 1900+yy : 2000+yy`，并在结果里注明判定依据。

### F-N203 CURP 页：日期只查 1-12/1-31、州码不查表，2 月 30 日与 `ZZ` 州都能过（中，确认缺陷）
- 问题：`:275` `dateValid = mm>=1&&mm<=12&&dd>=1&&dd<=31` 不校验各月天数与闰年；`:277` `STATES[state] || '未知'` 仅展示，`:286` 的通过条件只有 `dateValid && 校验位相等`。
- 证据：`tools/finance/curp-validator.html:275`、`:277`、`:286-290`
- 复现（node 实算）：`BOXW310220HMNERNA4`（2 月 30 日，校验位 4 吻合）→ 「✅ CURP 有效」；`BOXW310820HMNEZZA0`（州码 ZZ）→ 「州代码：ZZ - 未知」+「✅ CURP 有效」。合法对照 `BOXW310820HMNERNA8` ✅；非法对照 `BOXW310020HMNERNA6`（月 00）→ ❌。
- 影响：`tools/finance/curp-validator.html`；伪造/抄错的出生日期与州码不拦截，「分段可解析」这一卖点失去校验价值。
- 方案：用 `Date` 反查月份天数（含 2 月 29 闰年）；州码须命中 `STATES` 全集（含 `NE` 境外出生），未命中 ❌。

### F-N204 DNI 页：字母表写成 24 字符（官方 23），deep-dive 算例「mod 23 = 5」实为 14（低，确认缺陷）
- 问题：`:231` `DNI_LETTERS='TRWAGMYFPDXBNJZSQVHLCKET'` 共 24 字符，官方表为 23 字符 `TRWAGMYFPDXBNJZSQVHLCKE`（`%23` 只用到前 23 位，行为侥幸正确）；`:153` 公式框写 23 字符版、`:192` FAQ 又重复 24 字符版；`:189` 示例称「12345678 mod 23 = 5 → 第 5 位为 Z」。
- 证据：`tools/finance/dni-validator.html:153`、`:189`、`:192`、`:231`
- 复现（node 实算）：`12345678 % 23 = 14`，`TRWAGMYFPDXBNJZSQVHLCKET[14] = 'Z'`（0 基第 15 个字符，非「第 5 位」）；`87654321 % 23 = 10 → 'X'`（默认值 ✅）。
- 影响：`tools/finance/dni-validator.html`；用户按 FAQ 的 24 字符表自行复算会错位，示例推导过程不可信。
- 方案：三处统一为 23 字符表；示例改为「余 14 → 第 15 个字符 Z」。

### F-N205 DNI 页：`dniCheck()` 定义后从未被调用，校验逻辑另写一份（低，确认缺陷）
- 问题：`:232-238` 定义 `dniCheck(s)`（含 `^\d{8}[A-Z]$` 正则与期望字母），但 `:257` 的 `validate()` 自己重算一遍，全文件无 `dniCheck(` 调用点。
- 证据：`tools/finance/dni-validator.html:232-238`、`:250-257`、`:261`
- 复现：全文仅 `:232` 一处定义，函数体内部引用（`:233`/`:237`），无任何调用；`validate` 的实际判定走 `:250` 与 `:257` 的副本。
- 影响：`tools/finance/dni-validator.html`；两套逻辑未来易漂移（改一处漏一处），并增加维护噪音。
- 方案：`validate()` 改为调用 `dniCheck(raw)` 复用，或内联后删除死函数。

### F-N206 MEID 页：非十六进制字符被静默剥离，`A0000012345678G` 判有效（中，确认缺陷）
- 问题：`:268` `raw.replace(/[^0-9A-F]/g,'')` 丢弃 G-Z、中文、符号；`:272-281` 只看清洗后的长度，`:294-296` 对 14 位直接 `valid = true`。
- 证据：`tools/finance/meid-validator.html:268`、`:272-281`、`:294-296`
- 复现（node 实算）：`A0000012345678G` → 清洗为 14 位 → ✅；`A0000012345678ZZ` 同样 ✅；`A000-0012-3456-78` 也被当成合法 14 位。合法对照 `A0000012345678` ✅；非法对照 `A000001234567` → 「❌ 长度不符（当前 13 位）」。
- 影响：`tools/finance/meid-validator.html`；抄错一位字母（G/H…）不报错，设备入库/维修核对失效。
- 方案：清洗只允许空格、`-`、`:`；含 `[G-Z]` 等非法字符直接 ❌ 并回显首个非法字符位置。

### F-N207 MEID 页：14 位一律判有效、「hex/dec 互证」承诺未实现、校验算法无出处（中，确认缺陷）
- 问题：`:294-296` 与 `:311-313` 在缺校验位时一律 `valid = true`，任何 14 位 hex / 18 位 dec 都 ✅，只给「建议校验位」；deep-dive `:187` 承诺「验证十六进制与十进制两种表示是否自洽」，但 `:266-318` 全程无 hex↔dec 换算或交叉比对；`:232`/`:236` 注释自述 `Luhn-like`/`Luhn-style`，未注明 3GPP2 依据。
- 证据：`tools/finance/meid-validator.html:187`、`:232-236`、`:294-296`、`:311-313`
- 复现（node 实算）：`A0000012345678`（14 hex）→ ✅ +「建议校验位 7」；同一 MEID 的十进制 `045035996579124856`（`0xA0000012345678` = 45035996579124856，前补 0 至 18 位）→ 也 ✅，但页面不给两串等价的对照；`A00000123456780`（15 hex、校验位错）→ ❌。
- 影响：`tools/finance/meid-validator.html`；把「长度校验」包装成「校验位校验」，用户误信；互证卖点不存在。
- 方案：14 位输入也按算出的校验位判定（或明确标注「仅长度，未校验」）；新增「hex↔dec 换算 + 两种表示一致性」结果行；算法注明来源，无权威来源时降级表述为「非标准参考算法」。

- **留存建议（tools/finance/tin-validator.html）**：SSN/ITIN/EIN 三类号段是美国报税、开户的高频合规场景，纯离线可用，建议保留；必须先修 EIN 兜底（F-N190）与按格式判型（F-N191），否则「任何 9 位数字都有效」等于无校验。
- **留存建议（tools/finance/gstin-validator.html）**：15 位 base36 校验位算法已用官方样例核对无误，印度开票/供应商备案刚需，建议保留；补州码白名单（F-N193）与修正引据段序（F-N194）后可对外。
- **留存建议（tools/finance/tfn-validator.html）**：ATO 公开的加权 mod 11 算法适合离线实现，需求真实，建议保留；但权重表末位必须先由 11 改回 10（F-N195），当前版本「错号能过、真号被拒」，负面价值大于正面。
- **留存建议（tools/finance/sort-code-validator-validator.html）**：只有 6 位格式校验、无离线分行表、无算法，可替代性强；建议保留但把定位降为「格式提示/整理」，并按 F-N197 恢复「含字母即报错」。
- **留存建议（tools/finance/pan-validator.html）**：10 位结构与实体类型解读对印度税务核对有实际价值，建议保留；修第 4 位类型校验（F-N199）、统一示例（F-N200）后可用。
- **留存建议（tools/finance/curp-validator.html）**：18 位分段 + 官方校验位算法是墨西哥身份核验的真实能力，建议保留；修 19 位默认值（F-N201）、世纪规则（F-N202）与日期/州码校验（F-N203）后可对外。
- **留存建议（tools/finance/dni-validator.html）**：mod 23 映射算法极简、样例可核，是本批 8 页中算法质量最高的一页，建议保留；只需修文档（F-N204）与死代码（F-N205）。
- **留存建议（tools/finance/meid-validator.html）**：hex/dec 双表示对 CDMA 设备入库/维修有实际价值，建议保留；先把「校验」降级为「长度/格式」并补 hex↔dec 互证（F-N206/F-N207）再对外。

### 承诺 vs 实际（S 批专项）
- **「校验位校验」**：TFN 权重末位取 11 使第 9 位恒被忽略（`tfn:231` vs `tfn:153`）；MEID 14 位直接 `valid=true`、只给「建议校验位」（`meid:294-296`）；PAN 末位只回显字母、不计算期望值（`pan:271`）。三页的标题/描述均写「校验格式与校验位」。**部分未实现**。
- **「导出明细 CSV」**（8 页同构）：按钮调 `TBKit.util.exportTable('#xxxTable', …)`（`tin:403`、`gstin:423`、`tfn:395`、`sort:393`、`pan:401`、`curp:419`、`dni:394`、`meid:452`），导出的是最近 10 条历史表而非本次明细；`ResText` 又用 `/请输入|无效|不正确|错误|Error|NaN/` 过滤（`tin:327`、`gstin:347`、`tfn:319`、`sort:317`、`pan:325`、`curp:343`、`dni:318`、`meid:376`），失败样本不入库，首次点击只有表头。与 F-N189 同一根因，**名不符实**。
- **「批量」**：8 页均只有单个 `<input type="text">`（`tin:159`、`gstin:163`、`tfn:159`、`sort:159`、`pan:166`、`curp:159`、`dni:159`、`meid:159`），无多行/分隔符批量入口；「数据表」页签仅渲染 `history.list().slice(0,10)`（`tin:337`、`gstin:357`、`tfn:329`、`sort:327`、`pan:335`、`curp:353`、`dni:328`、`meid:386`），不构成批量结果表。**无批量能力**。
- **Sort Code「含字母会提示格式错误」**：deep-dive 明文承诺（`sort:189`），实际 `\D` 剥离后判 ✅（`sort:233`/`:264`）。**未实现**。
- **MEID「验证十六进制与十进制两种表示是否自洽」**：承诺见 `meid:187`，实际无换算、无交叉校验（`:266-318`）。**未实现**。
- **TIN「区分不同类型 TIN 的号段规则」**：场景承诺见 `tin:187`，实际 SSN 有号段规则、ITIN 有中段规则，其余全部兜底为 EIN ✅（`tin:267-273`）。**部分未实现**。
- **CURP「输入 18 位个人身份代码」**：描述见 `curp:156`/meta `:10`，实际默认值与 placeholder 均为 19 位（`curp:159`）。**示例与承诺不一致**。
- **PAN「校验前缀、实体类型字符与校验字符格式」**：描述见 `pan:161`/meta `:10`，实际第 4 位只查表展示、未知类型仍 ✅（`pan:264-272`）。**部分未实现**。
- **8 页共有功能特点/场景套话**：均写「采用标准金融计算公式」「支持多种参数灵活配置」「个人理财与投资规划 / 贷款还款方案计算 / 投资收益分析」，而这 8 页都是单输入框的号码格式校验，无公式、无参数可配、与理财规划无关（`tin:459/466`、`gstin:479/486`、`tfn:451/458`、`sort:449/456`、`pan:457/464`、`curp:475/482`、`dni:450/457`、`meid:508/515`）。**模板套话**。

### 覆盖
- 实读 8 页（逐页通读整份 HTML：head/meta/title、formula-box、intro、deep-dive、FAQ、constRef 表、内联 JS 与 TBKit 注入块）。新增 18 条（高 3 / 中 9 / 低 6），编号 F-N190~F-N207。
- 编号衔接：已确认本文件现有最大号为 F-N189（`### F-N189 6 个校验页 + 文本反转页…`），本批从 F-N190 连续编号。
- 算法结论均 `node` 内存复算：GSTIN（`27AAPFU0939F1ZV`→V、`09AABCU9603R1ZL`→L 与官方样例吻合；`99AAPFU0939F1ZK`/`00AAPFU0939F1ZB` 州码非法仍通过）；TFN（`100000062` 页面和 77 余 0 判 ✅、官方权重和 75 余 9、`100000001` 页面和 12 余 1 判 ❌、官方和 11 余 0）；CURP（默认 19 字符、`BOXW310820HMNERNA8` 校验位 8 通过、`GARW150820HMNERN58` 官方 1915 页面 2015、`BOXW310220HMNERNA4` 2 月 30 日通过、`BOXW310820HMNEZZA0` 州 ZZ 通过）；DNI（`87654321%23=10→X`、`12345678%23=14→Z`、字母表 24 字符）；MEID（`0xA0000012345678`=45035996579124856、清洗后 `A0000012345678G` 仍 14 位、15 hex 校验位 7/0）；TIN（`000000000`/`666-00-0000`/`900-00-0000`→EIN、`12-3456789`→SSN、`abc123456789xyz`→SSN）；PAN（`ABCZS1234E` 未知类型仍 ✅、`ABCKS1234E`→Krishik、`ABCP01234E` 被拒）；Sort Code（`12A34B56`→123456 ✅）。临时脚本在 `/tmp/fin8/`，未在仓库建文件。
- 未覆盖说明：`tools/finance/` 其余 108 页（含 `index.html`）未复扫；本批仅静态审计，未核对 `?lang=en-US` 英文态、繁体产物、移动端与打印表现；`sort:246-259` 的 bankMap 各前缀归属、`pan:241` 的 `K` 类型、`meid:232-236` 的 Luhn base16 是否对应 3GPP2 规范均需权威资料复核（已在对应条目标注口径，未作断言）。
- 验证边界：未开浏览器、未跑 `_build.py`、未跑门禁（`_test_static.py`/`_audit_links.py`/`_audit_assets.py`/`run_gates.py`），未做任何 git 写操作，未修改仓库代码（仅本 plan 文件追加）。

## T 批 finance 覆盖（2026-11-04）

### F-N208 ZIP 页：`00000` / `99999` 判有效，USPS 未分配段零拦截（中，确认缺陷）
- 问题：只做 `^\d{5}$` 形状匹配（`:240-256`），不校验 USPS 分配范围（有效 5 位 ZIP 为 00501–99950）；`00000`、`99999` 都落入 5 位分支并被判 ✅（`:245-247`、`:273`）。
- 证据：`tools/finance/zip-code-validator.html:240-256`、`:273`
- 复现（node 实算）：`00000` → `re5` 通过 → 「✅ ZIP Code 格式有效」（前 3 位 `000 - 未知州/地区`）；`99999` → 同样 ✅。期望：两串均 ❌（未分配 ZIP 段），或降级为「格式合法但非有效 ZIP」。
- 影响：`tools/finance/zip-code-validator.html`；地址/账单录入核对时全零与越界 ZIP 被当有效。
- 方案：补数值范围判定 `501 <= Number(zip5) <= 99950`，并单独拒绝 `000/001/002` 等未分配前缀；州映射只作展示，查不到时不判错。

### F-N209 SIN 页：`000-000-000` 判「✅ 有效」，与首字符 `Not issued` 自相矛盾（高，确认源码缺陷）
- 问题：`luhnCheck()` 仅验 mod 10（`:232-243`），`validate()` 先 `raw.replace(/\D/g,'')` 剥离所有非数字（`:246`）再只判 9 位（`:250-254`），既不排除全零也不校验首字符号段；`:268` 已把首字符 `0` 映射为 `Not issued`，`:271-279` 仍输出 ✅。
- 证据：`tools/finance/sin-validator.html:232-243`、`:246`、`:250-254`、`:258-269`、`:271-279`
- 复现（node 实算）：输入 `000-000-000` → Luhn 和为 0 → 页面同时显示「首字符：0 - Not issued」与「✅ SIN 号码有效」；输入 `130692544abc` → 剥离字母后按 `130692544` 判 ✅。期望：`000000000` ❌（CRA 未发行且页面自述 Not issued），含字母输入 ❌。
- 影响：`tools/finance/sin-validator.html`；雇佣/报税场景把占位号或抄错的字母串当成合法 SIN。
- 方案：增加 `digits === '000000000'`、首字符 `0`/`8` 的拒绝分支；清洗仅允许空格与 `-`，出现其它字符直接 ❌ 并回显位置。

### F-N210 NPI 页：首位号段规则写反——默认样例 `4234567897` 判 ✅、合法首位 `1` 反被警告（高，确认源码缺陷）
- 问题：Luhn（前置 80840）实现正确（`:232-247`，`1234567893`/`1245319599`/`1679576722`/`1003000126` 与标准算法结果一致），但号段判断写反：`:259-261` 只对首位 `0`/`1` 提示「NPI 通常不以 0 或 1 开头（使用 1-9 范围）」，而 CMS 已发行的 NPI 首位恒为 `1` 或 `2`，`3`–`9` 才是未分配段。
- 证据：`tools/finance/npi-validator.html:232-247`、`:259-261`、`:159`
- 复现（node 实算）：默认值 `4234567897` 校验和通过 → 页面 ✅「NPI 号码有效」，但首位 `4` 属未发行段，不可能存在；placeholder 的合法 `1245319599` 反而触发「⚠️ 通常不以 0 或 1 开头」。期望：首位 `3`–`9` 直接 ❌，首位 `1`/`2` 不再提示。
- 影响：`tools/finance/npi-validator.html`；美国医疗服务提供者编号核对时把不可能存在的 NPI 当有效，且对真号发出误导性警告。
- 方案：改为 `if(!/^[12]/.test(digits))` 判 ❌（文案写「已发行 NPI 首位为 1 或 2」），删除现有反向提示；默认值换成首位 1 的合法样例。

### F-N211 镜像文字页：`split('')` 按 UTF-16 码元反转，emoji 被拆成孤立代理项输出乱码（中，确认缺陷）
- 问题：映射用 `for(const ch of text)`（按码点迭代，`:284-286`）是对的，但随后 `out.split('').reverse().join('')`（`:287`）按 UTF-16 码元反转，增补平面字符（emoji、部分符号）被拆散且代理项顺序颠倒。
- 证据：`tools/finance/mirror-text.html:284-288`
- 复现（node 实算）：输入 `a😀b` → 输出码点为 `d, \uDE00, \uD83D, ɒ`（孤立低/高代理项，浏览器显示为 `d�ɒ`）；期望 `b😀a`（`Array.from(out).reverse().join('')`）。
- 影响：`tools/finance/mirror-text.html`；含 emoji/生僻字的签名、水印文案复制出去即乱码。
- 方案：反转改用 `Array.from(out).reverse().join('')`（或 `[...out].reverse()`）；顺带覆盖组合字符（可先 `normalize('NFC')`）。

### F-N212 ABA 路由号页：只验 mod 10 校验和，`000000000` 与未分配前缀 `99` 全判有效（高，确认源码缺陷）
- 问题：`abaCheck()` 仅算 `3(d1+d4+d7)+7(d2+d5+d8)+(d3+d6+d9) mod 10`（`:231-236`，公式本身正确），`validate()` 不做美联储前缀白名单（`:247-256`），也不排除全零，直接 `:261-264` 输出 ✅。
- 证据：`tools/finance/aba-validator.html:231-236`、`:247-256`、`:261-264`
- 复现（node 实算）：`000000000` → 校验和 0 → 「✅ ABA 路由号码有效」（分区显示 `00 - 未知/特殊用途`）；`990000000` → 校验和通过、前缀 `99` 未分配 → 仍 ✅。期望：两者 ❌（ABA 路由号前缀仅 `01`–`12`、`21`–`32`、`61`、`80`，`00` 与 `99` 非法）。
- 影响：`tools/finance/aba-validator.html`；ACH/工资直存前核对路由号会把无效前缀放行，转账被退票。
- 方案：在 `abaCheck` 后加前缀判定 `/^(0[1-9]|1[0-2]|2[1-9]|3[0-2]|61|80)/`，并显式拒绝 9 位全零。

### F-N213 选民 ID（EPIC）页：州代码只展示不校验，`AAA0000000`/`ZZZ0000000` 判有效（中，确认缺陷）
- 问题：`:238` 只用 `^[A-Z]{3}\d{7}$`，`:250-255` 把前 3 位当「州代码」原样回显并直接 ✅；`:153` 明确写「校验算法：无（EPIC 为格式校验）」，但页面标题/描述承诺校验「格式与结构」，州码并不在结构校验范围内。
- 证据：`tools/finance/voter-id-validator.html:238`、`:250-255`、`:153`
- 复现：`AAA0000000` → 「州代码：AAA」+「✅ 选民 ID (EPIC) 格式有效」；`ZZZ0000000` 同样 ✅。期望：未收录的州码 ❌ 或明确标注「仅校验 3 字母 + 7 数字，州码未校验」。
- 影响：`tools/finance/voter-id-validator.html`；选民名册核对时任意 3 字母前缀被当成合法州码。
- 方案：补 EPIC 州/选举委员会代码白名单（或改为「州代码仅供参考，未校验」的显式文案），并把校验口径同步到 intro/FAQ。

### F-N214 NRIC/FIN 页：支持 `M` 前缀的承诺与正则冲突，全部 M 系列 FIN 被拒（高，确认源码缺陷）
- 问题：`:274` 的 `PREFIX_DESC` 含 `M:'外国人（FIN，2022 年后）'`，`:278` 报错文案也写「前缀必须为 S/T/F/G/M」，但真正的格式门槛 `:241`（`nricCheck`）与 `:276`（`validate`）都是 `^[STFG]\d{7}[A-Z]$`，`M` 一律判「格式不符」。另 `:253` 的校验字母表选择只有 S/T 走 A 表，F/G 走 B 表，M 无分支。
- 证据：`tools/finance/nric-validator.html:241`、`:253`、`:271-275`、`:276`、`:278`
- 复现（node 实算）：`M1234567K` → 触发「❌ 格式不符：1 字母 + 7 数字 + 1 校验字母」（正则不匹配）；`S1234567D`/`T1234567J`/`F1234567N`/`G1234567X` 均按各自字母表通过。期望：M 前缀被接受并按 F/G 同表（`XWUTRQPNMLK`）校验，仅校验位错才 ❌。
- 影响：`tools/finance/nric-validator.html`；2022 年后签发的 M 系列 FIN（新加坡外国人）全部判无效，页面自述能力与实现冲突。
- 方案：正则改 `^[STFGM]\d{7}[A-Z]$`，`offset` 纳入 M（与 G 同为 +4），字母表分支改为 `(prefix==='S'||prefix==='T') ? A : B`；补一条 M 系列正例。

### F-N215 MSISDN 页：国家码只做前缀字符串匹配，本地号被硬判 `+1`、未知国家码仍 ✅（高，确认源码缺陷）
- 问题：`:263-270` 从 3 位到 1 位依次匹配 `CC_DB`，命中即认定国家码，既不验证号码前导位（E.164 首字符须 1–9），也不校验国家码是否真实存在；`:278-282` 未命中时按「假设为本地号码」继续，`:302-304` 的 `else` 无条件输出「✅ MSISDN 格式有效」。
- 证据：`tools/finance/msisdn-validator.html:263-282`、`:302-304`、`:159`
- 复现（node 实算）：默认值 `13800138000` → 循环命中 `'1'` → 显示「国家代码：+1 - 美国/加拿大」「国内号码 3800138000」+「✅ 符合 NANP 10 位号码格式」；`999999999999` → `CC_DB` 无 `999` → 落入 else → 「✅ MSISDN 格式有效」。期望：前者提示「缺国家码，无法判定（疑似 +86）」；后者 ❌（`99` 非有效国家码）。
- 影响：`tools/finance/msisdn-validator.html`；中国本地 11 位号被标成美加号码，任意 4–15 位数字串都被判「格式有效」，校验零区分度。
- 方案：仅当输入带 `+` 才做国家码解析；无 `+` 且长度 > 国内号长时要求补国家码；对未收录的 1–3 位前缀输出 ⚠️/❌ 而非 ✅；补 `0` 开头直接拒绝。

### F-N216 路由号页（ABA 同构副本）：同样缺前缀白名单，`000000000`/`990000000` 判有效（高，确认源码缺陷）
- 问题：`abaCheck()` 与 `aba-validator.html` 完全同构（`:235-240` 只算 mod 10），`:253-262` 只做分区名映射、不做合法前缀判定，`:267-271` 直接 ✅。
- 证据：`tools/finance/routing-number-validator.html:235-240`、`:253-262`、`:267-271`
- 复现（node 实算）：`000000000` → 校验和 0 → 「✅ 路由号码有效」；`990000000` → 校验和通过、前缀 `99` 未分配 → 仍 ✅。期望：两者 ❌（前缀限 `01`–`12`、`21`–`32`、`61`、`80`）。
- 影响：`tools/finance/routing-number-validator.html`；与 `aba-validator.html` 同源的重复缺陷，修一处必须同步另一处，否则两页结论不一致。
- 方案：与 F-N212 共用同一段前缀校验逻辑（抽到公共函数或两处同步修改），并补全零拒绝。

### F-N217 IMSI 页：3 位 MNC 命中后仍按 2 位切片展示，MNC/MSIN 同时错位（中，确认缺陷）
- 问题：`:268-270` 先固定切 `mnc = digits.substring(3,5)`、`msin = digits.substring(5)`；`:276` 才尝试 `mncDb[mnc] || mncDb[digits.substring(3,6)]` 做 3 位匹配。命中 3 位 MNC 时，`:282` 仍展示 2 位 MNC，`:283` 的 MSIN 多带 1 位 MNC 尾数。
- 证据：`tools/finance/imsi-validator.html:268-270`、`:276`、`:282-283`
- 复现（node 实算）：`310410123456789`（MCC 310 / MNC 410 = AT&T，MSIN 123456789）→ 页面「MNC（第 4-5 位）：41 - AT&T」「MSIN：0123456789」。期望：MNC 显示 `410`、MSIN 显示 `123456789`。
- 影响：`tools/finance/imsi-validator.html`；物联网卡入库、运营商归属核对时 MSIN 多一位，与 SIM 厂商数据对不上。
- 方案：解析时先试 3 位 MNC，命中则 `mncLen=3`，`mnc=digits.substring(3,3+mncLen)`、`msin=digits.substring(3+mncLen)`，标签随 `mncLen` 显示「第 4-6 位」。

### F-N218 邮编页：香港分支写成 `/.*/`，任意字符串（含 `HELLO`）都返回「✅ 匹配香港」（高，确认源码缺陷）
- 问题：`FORMATS` 中香港条目的正则直接写 `pattern:/.*/`、`desc:'香港无邮编系统（默认通过）'`（`:257`）；`:274-280` 只要正则命中就记入 matches，`:293-297` 逐条输出 ✅，因此任何未被其他国家匹配的输入都会「默认通过」。
- 证据：`tools/finance/postal-code-validator.html:257`、`:274-280`、`:293-297`
- 复现（node 实算）：`HELLO` → 仅 HK 命中 → 「✅ Hong Kong（HK）：香港无邮编系统（默认通过）」；`ZZZ` 同样 ✅。期望：非邮编形态 ❌「不匹配任何已知国家的邮编格式」，香港仅在接受显式 `HK:` 前缀或空输入时提示「无邮编系统」。
- 影响：`tools/finance/postal-code-validator.html`；校验器对任意乱码返回成功，等同无校验。
- 方案：删除 HK 的 `/.*/` 通配，改为空串/显式 `HK:` 时单独提示；matches 为空时统一走 ❌ 分支。

### F-N219 邮编页：日本/巴西等「带连字符」正则拒掉无连字符的合法写法（中，确认缺陷）
- 问题：日本 `^\d{3}-\d{4}$`（`:249`）、巴西 `^\d{5}-\d{3}$`（`:254`）强制连字符；这两国的邮编在官方与日常写法中均可无分隔符（日本 7 位、巴西 8 位）。
- 证据：`tools/finance/postal-code-validator.html:249`、`:254`、`:281-292`
- 复现（node 实算）：`1000001`（日本东京 100-0001 的无连字符写法）→ JP 不匹配、只命中 HK → 页面输出「✅ Hong Kong」；`01310100`（巴西 01310-100）同样被当成香港。期望：分别匹配 Japan / Brazil 并给出对应格式说明。
- 影响：`tools/finance/postal-code-validator.html`；合法邮编被误判国家，跨境地址核对给出错误结论。
- 方案：JP 改 `^\d{3}-?\d{4}$`、BR 改 `^\d{5}-?\d{3}$`（其余强制分隔符的国家同理复核），并在输出中回显规范化后的带连字符形式。

### F-N220 IRD 页：加权取位整体错一位、无 secondary 权重回退，合法 IRD 被拒/非法 IRD 放行（高，确认源码缺陷）
- 问题：`irdCheck()` 先把输入补成 9 位，却取 `base = d.substring(1,9)`（`:248`）——官方口径是「8 位补前导 0 后取前 8 位作 base，第 9 位为校验位」，现实现丢掉首位、把校验位本身也算进加权；`:234-238` 定义了 `IRD_WEIGHTS` 的 secondary 行（`7,4,3,2,5,2,7,6`）但 `:247` 固定 `weightSet = 0`，`:252` 只用 primary，secondary 从未使用。`:156` 公式框还写成「mod 11 = 0」「9 位版前置补 0」，与官方「8 位补 0、check = 11 − rem」相反。
- 证据：`tools/finance/ird-validator.html:234-257`、`:248`、`:252`、`:255`、`:156`、`:162`
- 复现（node 实算）：`49091850`（官方 primary 和 154 → rem 0 → 校验位 0，合法）→ 页面 ❌；页面默认值 `490918503`（页面本身算出期望 3 = 末位 3，判 ✅；官方 base 49091850 的 rem 7 → 校验位 7，判非法）→ 页面 ✅；同批 `10000009`（官方合法）页面 ❌、`10000019`（官方非法）页面 ✅。期望：前两例结论对调。
- 影响：`tools/finance/ird-validator.html`；新西兰税务号（GST/雇主登记）核对时真号被拒、错号放行，且页面默认样例本身就是错的。
- 方案：`base = d.substring(0,8)`、`check = +d[8]`；primary 算出 `c=10` 时改用 secondary 重算，`c===10` 判无效；同步修正公式框为「8 位补前导 0，check = (11 − sum mod 11) mod 11，必要时用 secondary 权重」。

### F-N221 DEA 页：偶数位「先求和再取位和」，与官方「逐位乘 2 后按位求和」不等价（高，确认源码缺陷）
- 问题：`:243-248` 先 `s2 = 2*d[1] + 2*d[3] + 2*d[5]`，再 `Math.floor(s2/10) + s2%10`，即只把三项乘积之和做一次十进制位和；官方 DEA 校验是「第 1/3/5 位相加 + 第 2/4/6 位各自乘 2 后按位求和，取总和的个位为末位」。两者仅在个别巧合时相等。
- 证据：`tools/finance/dea-validator.html:237-249`、`:243-248`、`:153`
- 复现（node 实算）：`AB0134623` → 官方 `9 + (2+8+4) = 23` → 校验位 3（与末位一致，合法），页面 `s2 = 14 → 1+4 = 5 → 总 14 → 校验位 4` → ❌；`AB0118785` → 官方非法、页面 ✅。期望：前者 ✅、后者 ❌。
- 影响：`tools/finance/dea-validator.html`；美国药品流通/处方合规核对时合法 DEA 号被拒、非法号被放行，两个方向都错。
- 方案：改为 `sum2 = [2*d[1],2*d[3],2*d[5]].reduce((a,v)=>a+Math.floor(v/10)+v%10,0)`；补 `AB0134623`（合法）与 `AB0118785`（非法）两条回归用例。

### F-N222 贷款摊销页：年限允许非整数，`2.3 年` 只摊 27 期并留下 1.1 万本金、界面打印 27.599999…（高，确认源码缺陷）
- 问题：`totalMonths = Math.min(years * 12, 12000)`（`:386`）不做取整，`for (i = 1; i <= totalMonths; i++)`（`:393`）在非整数月数下少跑一期；月供却按 27.6 期贴现算出（`:392`），期末不归零；`:500` 直接把 `totalMonths` 原样输出。
- 证据：`tools/finance/loan-amortization.html:179`、`:386`、`:392-400`、`:484-487`、`:500`
- 复现（node 实算）：`500000 / 4.9% / 2.3 年` → 期数显示 `27.599999999999998`、表内仅 27 行、期末剩余本金 `11,478.24`、总利息 `29,685.69`；期望：期数取整为 28（或限制 `step=1` 只收整数年）并按 28 期重算月供，期末剩余本金为 0。
- 影响：`tools/finance/loan-amortization.html`；用户填 2.5 年尚正常、填 2.3/1.7 年即出现非零尾款与 15 位小数，还款计划表不可用。
- 方案：`totalMonths = Math.round(years * 12)`（小于 1 期时提示），并让 `years` 与 `totalMonths` 共用同一取整值；期数列用整数输出。

### F-N223 vCard 二维码页：所谓「二维码」是按文本 hash 播种的伪随机 33×33 网格，任何扫码器都读不出（高，确认源码缺陷）
- 问题：`renderQR()`（`:261-281`）只画三个定位角、时序线和一圈 `rnd()<0.5` 的「数据点」：`rnd` 由 `pseudoRandom(strHash(text))` 生成（`:248-249`、`:274-278`），没有字符编码、没有 Reed-Solomon 纠错、没有掩码选择或格式/版本信息；`drawQR()` 只是把该网格逐格填色（`:282-288`），`generate()` 把它当二维码贴到结果区（`:289-294`）。
- 证据：`tools/finance/vcard-qr.html:248-249`、`:261-281`、`:282-288`、`:289-294`
- 复现（源码判定）：输入默认 vCard 生成一张 231×231 的「像二维码」的图；该网格无 RS 码字与格式信息，任何解码器（手机扫码/ZXing）都无法还原 `BEGIN:VCARD` 文本，只有下方 `.qr-text` 明文可用。期望：输出可被扫码器还原为 vCard 的真二维码，或明确告知「本页仅生成 vCard 文本，不生成二维码」。
- 影响：`tools/finance/vcard-qr.html`；用户扫描后无任何结果，属于「宣称生成却无实际实现」。
- 方案：引入本地打包的 QR 编码库（如 `qrcode-generator`，锁版本、纯前端）走标准 QR 编码 + RS 纠错；或降级为 vCard 文本生成器并删除二维码画布与「扫码添加」文案。
- **假工具候选：是（类型 B——生成器输出为伪随机绘制，无真实编码实现）**

### T 批覆盖说明
- 本轮审计 19 页：`dns-record-info`、`zip-code-validator`、`sin-validator`、`ifsc-validator`、`npi-validator`、`mirror-text`、`abn-validator`、`aba-validator`、`voter-id-validator`、`nric-validator`、`msisdn-validator`、`word-frequency`、`routing-number-validator`、`imsi-validator`、`postal-code-validator`、`ird-validator`、`dea-validator`、`loan-amortization`、`vcard-qr`（后 3 页为 `finance.md` 未提及页中补齐）。
- 新增 16 条（高 11 / 中 5），编号 F-N208~F-N223；假工具候选 1 页（`vcard-qr`，类型 B）。
- 无高优/无条目（覆盖但不列缺陷）：`dns-record-info`（自述「纯速查，不做联网解析」，过滤与导出为真实实现）、`ifsc-validator`（4 字母 + `0` + 6 位字母数字，与 RBI 结构一致）、`abn-validator`（mod 89 权重 `10,1,3,…,19` 经复算正确，`51824753556`/`53004085616` 通过、`12345678901`/`00000000000` 拒绝；仅公式框漏写 10/1 两权重，属文案级）、`word-frequency`（占比分母为「展示词合计」且公式框已明示该口径，无高优）。
- 数值/规则均 `node -e` 内存复算（临时脚本 `/tmp/fin19_check.js`、`/tmp/fin19_check2.js`，未在仓库建文件），口径来源：SIN/Luhn（Service Canada）、NPI（CMS：首位 1/2 + 80840 Luhn）、ABA（美联储路由号前缀 01–12/21–32/61/80）、ABN（ATO mod 89）、DEA（第 1/3/5 位 + 第 2/4/6 位乘 2 后按位求和取个位）、IRD（NZ Inland Revenue primary/secondary 权重）、NRIC（新加坡 ICA S/T/F/G/M 校验字母表）。
- 未做浏览器/门禁/线上验证：未开浏览器、未跑 `_build.py`、未跑 `_test_static.py`/`_audit_links.py`/`_audit_assets.py`/`run_gates.py`，未做 git 写操作，未修改任何工具页/代码/样式/数据文件（仅本 plan 文件追加）。

## AC 批 · 贷款/还款/利息族（2026-11-04）

### 族矩阵

| 页面 | 实现方式 | 可逆或可验证 | 结论 |
|---|---|---|---|
| `tools/finance/loan-amortization` | 自写：4 种还款方式（等本息/等本金/先息后本/气球）+ 逐期摊销 | 逐期余额闭合可复算 | 主算法可信；提前还款扩展分支有错 |
| `tools/finance/mortgage-calculator` | 自写：等本息/等本金 + 24 期表 + CSV | PMT 复算一致，CSV 可核对 | 可信（F-N11 已修） |
| `tools/finance/housing-fund-loan` | 自写：额度三取小（余额×倍数/房价 80%/城市上限）+ 摊销 | 额度可复算 | 算术可信，政策口径存疑 |
| `tools/finance/car-loan-calculator` | 自写：PMT + 税金/保险分解；与房贷页同模板派生 | 月供/落地价可复算 | 可信 |
| `tools/finance/loan-comparison` | 自写：3×PMT 对比 | PMT/总利息可复算 | 可信；空利率被当 0% |
| `tools/finance/mortgage-prepayment` | 自写：PMT + 逐月循环求剩余期数 | 两种方案可重算 | 高月供/零提前还款时节省虚增 |
| `tools/finance/simple-interest` | 闭式 `I=Prt` | 可逆解 P/r/t | 可信（F-N21 已修） |
| `tools/finance/compound-interest` | 逐年/逐期迭代 | 年金终值可闭式核对 | 可信（F-N9 已修） |
| `tools/finance/credit-card-interest` | 最低还款逐月模拟；分期 IRR 二分 | 模拟可重放，IRR 可复算 | 默认可信；未还清时「总支出」错 |
| `tools/finance/installment-real-rate` | IRR 二分 + EAR | 残差/边界已提示 | 可信（F-N10 已修） |

### 独立实现 vs 共享实现

- 10 页均为**页内自写、无共享财务库**（外部仅 `tool-kit.js` 等脚手架）。
- **同源模板 2 页**：`mortgage-calculator` → `car-loan-calculator`（`setMethod/resetDisplay/exportCSV/calculateCosts` 与饼图代码逐段同构，行号 348/433、439/571、446/597）。
- 共用公式均为各自复写：等额本息 6 页（房贷/车贷/公积金/摊销/对比/提前还款）、等额本金 3 页（房贷/公积金/摊销）、IRR 二分 2 页（分期/信用卡）、逐期摊销表 4 页 → 跨页同参结果一致（100k/4.8%/36 → 2,988.12；1M/4.9%/30 → 5,307.27，见 `loan-comparison:248` 与 `loan-amortization:392`）。

### 逐页结论（默认态 10/10 与独立复算一致）

| 页面 | 页面默认输出 | 复算 | 判定 |
|---|---|---|---|
| loan-amortization | 500k/4.9%/360：月供 2,653.63、首期息 2,041.67、总息 455,308.10、有效年化 5.01% | 同 | 一致 |
| mortgage-calculator | 100 万/30% 首付/4.2%/30 年：3,423.12、总息 532,323.28、总额 1,232,323.28、4.28% | 同 | 一致 |
| housing-fund-loan | 北京/8 万/300 万/2.85%/20 年：120 万、6,565.42、总息 37.57 万 | min(120,240,120)=120 万；6,565.42 | 一致 |
| car-loan-calculator | 15 万/30%/5.5%/3 年：3,170.57、9,140.51、落地 65,144.34 | 同 | 一致 |
| loan-comparison | A 2,988.12/7,572.26；B 2,997.09/7,895.23；C 3,535.05/6,051.52 | 同 | 一致 |
| mortgage-prepayment | 应还月供 3,163.25×240=759,179.25；①245 期/省 4,179.25；②3,036.72/省 10,367.17 | 算术同，但①显示「延长 5 个月」 | 默认值矛盾（F-N224/F-N233） |
| simple-interest | 10,000/5%/3 年：1,500、11,500、复利 11,576.25 | 同 | 一致 |
| compound-interest | 10,000/5%/20 年/年投 12,000 期初：443,164、250,000、193,164、77.27% | 同 | 一致 |
| credit-card-interest | 10,000/万五/10%：首月 1,150、息 1,493.89、支出 11,493.89、55 期 | 同 | 一致 |
| installment-real-rate | 12,000/12 期/0.6%：1,072、费 72、×12 13.03%、EAR 13.84% | 同 | 一致 |

### 问题清单（新增）

| 编号 | 页面:行 | 级别 | 问题与期望值 |
|---|---|---|---|
| F-N224 | `tools/finance/mortgage-prepayment.html:304-307,312-318,335` | 高 | 基线固定用应还月供 3,163.25，且 `mpWarn` 只判 `mp<` 应还月供。本金 50 万/4.5%/240 期、月供 4,000、**提前还款 0** → 报「节省 83,179.42」，期望 0（纯属多还月供的效果）；应禁用或拆分归因（F-N91 仍成立，F-N26 已失效） |
| F-N225 | `tools/finance/credit-card-interest.html:430,439` | 高 | 未还清时 `总支出=bill+利息`。账单 1 万/日息万五/最低 1% → 显示 20,509.29 并称「120 期累计」，实际累计已付 17,515.49（差额=未还本金 2,993.80）；期望 17,515.49（F-N22 部分修复） |
| F-N226 | `tools/finance/loan-amortization.html:320,447` | 中 | 输入校验强制 7 个字段非空，含等额本息下隐藏的「期末尾款比例/气球期数/提前还款额」；清空隐藏项即「请填写…后再计算」。期望仅校验当前模式字段 |
| F-N227 | `tools/finance/loan-amortization.html:760-766,788-796,703,736` | 中 | 先息后本/气球贷提前还款：降月供分支 `newPayment` 恒 0（显示「新月供 0.00」），缩期分支不减新利息。100 万/4.9%/360 先息后本、第 24 期还 10 万 → 声称省 1,372,000，真实约 137,200（10 倍）；`prepayAmount=-100000` 使剩余本金反增 10 万（F-N25 仍成立） |
| F-N228 | `tools/finance/loan-amortization.html:423,503` | 中 | 气球贷模式 `years` 被忽略（`loanMonths=balloonMonths`），且不校验 `balloonMonths≤years*12`；100 万/30 年/气球 360 期 → 「还款期数 360」与「年限 30」无关联提示 |
| F-N229 | `tools/finance/loan-comparison.html:260-266` | 中 | 利率留空时 `isFinite(NaN)?:0` 静默按 0%，`valid` 不校验利率 → 显示「有效年化 0.00%」并参与排名。期望判无效并排除（F-N1 部分：无效方案已排除，空利率仍漏） |
| F-N230 | `tools/finance/credit-card-interest.html:463,482` vs `installment-real-rate.html:335-336,353` | 中 | 同名「实际年化」口径不一：同为 0.75%/12 期，信用卡显示「实际年化 17.48%」（EAR），分期页「×12=16.22%」「有效年化 17.48%」。期望统一命名并双列 |
| F-N231 | `tools/finance/housing-fund-loan.html:282,318-324` | 中 | 城市规则硬编码无出处：北京按「余额×15 倍」，与「每缴存 1 年贷 10 万、上限 120 万」口径不符（待官方核实）。期望改按缴存年限或标注来源/生效日（F-N96 已修，本条为额度规则） |
| F-N232 | `tools/finance/loan-comparison.html:126,179-180` | 中 | 公式框称「总成本=月供×期数+各项费用」、实际年化=「含费用 IRR」，页面既无费用输入也不算 IRR。期望删去费用/IRR 表述或补输入 |
| F-N233 | `tools/finance/mortgage-prepayment.html:131-132,357-359` | 中 | 默认月供 3,000 < 应还 3,163.25，①「缩短期限」却显示「延长 5 个月」同时「省 4,179.25」。期望默认回填应还月供，或对①强制否定结论（F-N27 已修复的 1,200 期触顶部分不重复） |

### 统计

- 页数 **10**；独立实现 **10** / 共享模块 **0**；同源模板 **2**（房贷→车贷）。
- 新增 **10** 条（高 **2** / 中 **8** / 假 **0** / 安全 **0**）；编号 F-N224–F-N233。
- 安全：本轮 10 页均注入模板级 `lf1-cdn-tos.bytegoofy.com/ttzz/push.js`（无 SRI），属全站模板既有项，不重复计数。
- 复核既有 13 条：已修/失效 8（F-N9/N10/N11/N12/N21/N23/N27/N96），仍成立 4（F-N25/F-N91/F-N92 部分/F-N97），部分 1（F-N22）；F-N26 已失效（基准已改用应还月供）。
- 复算口径：`M=P·r(1+r)^n/((1+r)^n−1)`、EAR=`(1+r)^12−1`、IRR 用 [0,1] 二分 80 次、信用卡按 `interest=余额×0.0005×30`、`pay=min(余额×比例+息,10)` 逐月；脚本 `/tmp/fin02_audit.js`（node 复算，未改仓库）。
