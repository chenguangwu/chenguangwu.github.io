# 金融计算 · tools/finance（115 页，第二大分类）

## 2026-11-06 已修记录独立复核：APY 和零利率贷款

- `node scripts/verify_finance_calc.js apy-calculator loan-amortization` 为 8/8，DOM 桩断言命中任一输出即通过；其结果不等于所有显示值、图表与导出已验证。

## 已知问题
### F1. 贷款/利率系「名义 vs 实际」口径页散
- `tools/finance/compound-interest.html` 的利率口径导航位于默认隐藏的「公式说明」面板，而非结果区之后；需切换面板才能看到。
- 🔴 「同输入多口径并排」未做（计算器组，量级大待裁）。

## 功能缺陷
- `tools/finance/loan-amortization.html` 的逐年汇总表提示提前还款后会同步重算，但 `calcPrepay()` 只更新提前还款结果，不修改 `scheduleData` 或重绘汇总表，表格仍为原还款计划。

## 优化点（G06 联动，金融是 S2/S3 最高 ROI 分类）
- S2 场景预设：「一线首套商贷 300 万 25 年」「二套 4.9% 上浮」「等额本息 vs 本金并排」。
- S3 分步：每月月供拆解（本金/利息/剩余）逐年表+堆叠图。
- S4 分享卡：个税/贷款结果最常被转发。
- F1+D11 打通：本分类做「计算器组」（输入一次，联动房贷/个税/提前还款）。

## 受影响范围
- tools/finance/（115 页）

## 进度
- 🔴 待开发：S4 分享卡；同输入多口径并排待裁。

## 2026-11-03 审计补充

### 留存优化：贷款比较显示可比性与总成本（中，建议）
- 证据：`tools/finance/loan-comparison.html:134-151,266-278` 支持三个不同本金和期数并排、CSV 和复制，但排名仅按月供。
- 影响：同页；方案：提示不同本金或期限的方案不可仅凭月供判优，给出总利息差、实际总还款及同本金/同期条件下比较入口；如补收费项应标明口径。

### 留存优化：车贷费用与展示期间对齐（低，建议）
- 证据：`tools/finance/car-loan-calculator.html:285-336,539-553` 支持保险年数，但结果标题固定称首年保险，代码按选定年数相乘。
- 影响：`tools/finance/car-loan-calculator.html`；方案：按实际选中年数动态显示保险与车船税期间，并提供贷款期限内现金流合计和费用假设说明。

### 覆盖
- 本次人工查 `tools/finance/loan-comparison.html`、`tools/finance/car-loan-calculator.html` 2 页；其余金融页未逐页复扫；历史已修声明未独立复验。

## 2026-11-03 续查：现金流、债券与退休规划


### 续查覆盖
- 新抽查 `tools/finance/irr-calculator.html`、`tools/finance/bond-yield-calculator.html`、`tools/finance/dca-calculator.html`、`tools/finance/retirement-calculator.html` 共 4 页，新增 7 条（6 条高优），均为源码及数值推导，未做浏览器、线上和门禁验证。


### 留存优化（按页落点，非确认缺陷）
- `tools/finance/compound-interest.html`：只能正算终值，缺「目标金额反推所需年限/月投」。建议加目标反推与「单利 vs 复利」并排对比，这是理财类搜索的主要意图。
- `tools/finance/installment-real-rate.html`：只有单一方案，无「多期数并排（12/24/36 期）」与手续费一次性/按期两种口径切换。建议并排展示不同期数的实际年化与总成本，便于用户直接比较。

### 续查覆盖
- 新抽查 `tools/finance/compound-interest.html`、`tools/finance/installment-real-rate.html` 共 2 页，新增 2 条中优与 2 条留存建议；为源码核查，未做浏览器、线上或门禁验证。

## 2026-11-03 续查（并行批）：金融回补
（路径均相对 `tools/`）




### 留存优化（按页落点）
- `finance/mortgage-calculator`：仅前 24 期；补首付+税费总成本与全表下载。
- `finance/housing-fund-loan`：规则硬编码 2024、年龄只提示；补利率可选与年龄压年限。
- `banking/apy-calculator`：补单利/复利/连续复利三列与 %/小数双输入。
- `finance/salary-calculator`：不可导出；补工资条导出与年终奖单独/合并对比。

### 续查覆盖
- 实读 6 页：finance 的 mortgage、housing、lease、salary；banking 的 apy、loan-to-value；node 复算，未做浏览器/线上验证。

## 2026-11-03 续查（并行批 I）




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

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 8 页（`tools/finance/profit-margin-calculator.html`、`depreciation-calculator.html`、`position-size-calculator.html`、`insurance-calculator.html`、`stock-profit-calculator.html`、`option-profit-calculator.html`、`break-even-calculator.html`、`capm-return.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证；历史已修声明未独立复验。

- 本轮实读 8 页：`tools/finance/profit-margin-calculator.html`、`tools/finance/depreciation-calculator.html`、`tools/finance/position-size-calculator.html`、`tools/finance/insurance-calculator.html`、`tools/finance/stock-profit-calculator.html`、`tools/finance/option-profit-calculator.html`、`tools/finance/break-even-calculator.html`、`tools/finance/capm-return.html`；新增 9 条（高 1 / 中 6 / 低 2）；未覆盖：其余 finance 页（约 71 页）未逐页复扫。
- 证据均由源码行号 + node 内存复算取得；未做浏览器、英文态、移动端、门禁与线上验证；历史已修声明未独立复验。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 8 页（`tools/finance/amount-in-words.html`、`tools/finance/number-to-words-chinese.html`、`tools/finance/gold-price-calculator.html`、`tools/finance/shebeizulinfeilvjisuan.html`、`tools/finance/register-depreciation.html`、`tools/finance/credit-card-validator.html`、`tools/finance/credit-card-luhn.html`、`tools/finance/points-redemption-value.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证；历史已修声明未独立复验。


- 本轮实读 8 页：`tools/finance/amount-in-words.html`、`tools/finance/number-to-words-chinese.html`、`tools/finance/gold-price-calculator.html`、`tools/finance/shebeizulinfeilvjisuan.html`、`tools/finance/register-depreciation.html`、`tools/finance/credit-card-validator.html`、`tools/finance/credit-card-luhn.html`、`tools/finance/points-redemption-value.html`；新增 9 条（高 2/中 4/低 3）；未覆盖：其余 finance 页（约 78 页）未逐页复扫。
- 证据均由源码行号 + node 内存复算取得；未做浏览器、英文态、移动端、门禁与线上验证；历史已修声明未独立复验。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 8 页（`tools/finance/calc-2.html`、`tools/finance/calc-3.html`、`tools/finance/calc-4.html`、`tools/finance/calc-5.html`、`tools/finance/invoice-generator.html`、`tools/finance/currency-converter.html`、`tools/finance/analysis-5.html`、`tools/finance/analysis-risk.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证；历史已修声明未独立复验。



- 本轮实读 8 页：`tools/finance/calc-2.html`、`tools/finance/calc-3.html`、`tools/finance/calc-4.html`、`tools/finance/calc-5.html`、`tools/finance/invoice-generator.html`、`tools/finance/currency-converter.html`、`tools/finance/analysis-5.html`、`tools/finance/analysis-risk.html`；新增 11 条（高 3/中 6/低 2）；未覆盖：其余 finance 页（约 66 页）未逐页复扫。
- 证据均由源码行号 + node 内存复算取得；未做浏览器、英文态、移动端、门禁与线上验证；历史已修声明未独立复验。

## 2026-11-04 续查（并行批 O）

> 范围：本轮阅读 8 页（`tools/finance/analysis-44.html`、`analysis-cost-1.html`、`assessor-manager.html`、`report-1.html`、`generator-report-1.html`、`number-to-words.html`、`currency-lookup.html`、`credit-card-bin.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证；历史已修声明未独立复验。


- 本轮实读 8 页：`tools/finance/analysis-44.html`、`tools/finance/analysis-cost-1.html`、`tools/finance/assessor-manager.html`、`tools/finance/report-1.html`、`tools/finance/generator-report-1.html`、`tools/finance/number-to-words.html`、`tools/finance/currency-lookup.html`、`tools/finance/credit-card-bin.html`；新增 10 条（高 1/中 5/低 4）；未覆盖：其余 finance 页（约 58 页）未逐页复扫。

## 2026-11-04 续查（并行批 O-P2）

范围：复读 `tools/finance/` 下 8 页（mortgage-calculator、mortgage-prepayment、housing-fund-loan、salary-calculator、simple-interest、tax-bracket、tax-calculator、vat-calculator），编号 F-N91~F-N113。说明：这 8 页在更早批次已有部分条目（F-N11/N12/N15/F-N18–N21/F-N26–N28），本段只记录本次复读新增或由旧修法引入的问题，不重复旧条目；F-N81~F-N90 段未改动。

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
- 覆盖统计：`tools/finance/` 共 116 个 HTML（含 index.html），本批实读 8 页；审计文档累计提及 66 个 finance 页面，其余约 50 页未逐页复扫。
- 验证边界：未做浏览器真机、英文态（`?lang=en-US`）、繁体、移动端与门禁（`_build.py`/`_test_static.py`/`_audit_links.py`/`_audit_assets.py`）验证；所有金额均在 `node -e` 内存复算，未修改仓库代码、未运行构建、未做 git 写操作。

## 2026-11-04 续查（并行批 P）

范围：复读 `tools/finance/` 下 8 页（lease-payment-calculator、credit-card-interest、credit-card-type、isbn-validator、iban-validator、bic-validator、currency-symbol、password-generator-advanced），编号 F-N114~F-N145。说明：lease 与 credit-card-interest 在旧批次有 F-N13/F-N22，本段只记录本次复读仍存在或由旧修法引入的问题，不重复旧结论；F-N1~F-N113 未改动。

### F-N122 信用卡利息页：账单日/到期日只影响「免息天数」展示，不参与任何计息（低，确认缺陷）
- 问题：`billDay`/`dueDay` 仅用于 `interestFreeDays` 文案，`simulateMinimum` 固定按 30 天计息、分期也不使用日期；`+value || 1` 使 0 变 1，免息天数再被 clamp 到 20–56，非法日期被掩盖。
- 证据：`tools/finance/credit-card-interest.html:376-377`（`|| 1`）、`:398-404`（免息天数与 clamp）、`:345`（固定 30 天）、`:448-461`（分期不看日期）
- 复现：账单日 10、到期日 30 → 免息 40 天、利息 1,493.89；只把到期日改 31 → 免息 41 天，利息与期数完全不变。期望日期变化至少改变计息天数，或明确标注「日期仅用于免息天数展示」。
- 影响：`tools/finance/credit-card-interest.html`；用户以为输入真实账单周期能提高精度，实际是装饰性字段。
- 方案：用实际账单周期天数代替固定 30，并校验 1–31；若暂不建模，则在日期输入旁注明「仅展示，不参与计息」。
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
- 覆盖统计：`tools/finance/` 共 116 个 HTML（含 index.html），本批实读 8 页；审计文档累计提及约 72 个 finance 页面，其余约 43 页未逐页复扫。
- 验证边界：未做浏览器真机、英文态（`?lang=en-US`）、繁体、移动端与门禁（`_build.py`/`_test_static.py`/`_audit_links.py`/`_audit_assets.py`）验证；金额与校验用例均在 `node -e` 内存复算（ISBN/IBAN/BIC 另用真实合法/非法样例），未修改仓库代码、未运行构建、未做 git 写操作、未在仓库建临时文件。F-N128 的 DOM 结论来自 HTML 解析与规范，F-N136 的实体绕过路径需真机复核。

## 2026-11-04 审计补充（Q 批：校验器/文本类 8 页）
### F-N147 六个校验页共用「数据表/历史/趋势图」模板：结果为文本，趋势图永不绘制、CSV 只导历史摘要（低，确认缺陷）
- 问题：`__*Extras` 用 `parseFloat` 解析结果文本（结果以「输入：」开头），恒为 `NaN`，`nums.length>=2` 永不成立 → 「结果趋势」图一次都不会出现；「导出明细 CSV」导出的是历史表（输入 + 文本摘要），首次使用前为空，且没有任何「是否通过」的结构化列。
- 证据：`tools/finance/swift-bic-validator.html:314`（ResText）、`:356`（parseFloat）、`:360`（≥2 才画图）、`:395`（exportTable 历史表）；同构块：`uan-validator.html:307,349,352,388`、`aadhaar-validator.html:341,383,386,422`、`cpf-validator.html:336,378,381,417`、`esn-validator.html:321,363,366,402`、`ein-validator.html:306,348,351,387`
- 复现：连续校验 `DEUTDEFF`、`DEUTDEFF500`、`DEUTDEXX` → 「数据表」3 行，切「结果」无趋势图；点「导出明细 CSV」得到 3 行「输入/结果」文本而非校验结论。期望单值校验页不挂趋势图，或把结果落成 `{代码,是否通过}` 两列。
- 影响：上述 6 页；模板噪音让用户以为存在统计能力，实际只有输入回放。
- 方案：把 `__*_skip` 置真关掉图表与趋势，保留「最近校验」列表；若保留图表，记录「通过=1/不通过=0」的结构化字段而非结果文本。

- **留存建议（tools/finance/swift-bic-validator.html）**：保留「8/11 位分段 + ISO 国家码校验 + 逐段诊断」的清晰结构（比 bic-validator 更完整），修空格归一化后即可留；建议与 bic-validator 二选一或明确分工（两页功能重叠）；补「XXX=主办公室 / 测试码」语义说明。

### F-N149 UAN 页：2/5/5 分段被标成「区域 / EPFO 办公室 / 序号」，无出处（低，待验证）
- 问题：结果区把 `digits[0:2]` 标为「区域」、`[2:7]` 为「EPFO 办公室」、`[7:12]` 为「序号」，公式框也作为「本页代码口径」陈述；EPFO 公开资料只定义 UAN 为 12 位编号，未定义该语义，页面未给来源，用户易把「区域」误读为所在邦。
- 证据：`tools/finance/uan-validator.html:153`（公式框分段）、`:245-247`（切片）、`:251-253`（输出标签）
- 复现：输入 `101234567890` → 「区域：10 / EPFO 办公室：12345 / 序号：67890」；按切片规则，任何以 `10` 开头的 UAN 都会显示「区域：10」，与该号实际办事机构无关。期望标注「仅展示分段，非官方语义」或删除段名。
- 影响：`tools/finance/uan-validator.html`
- 方案：标签改为「前 2 位 / 中 5 位 / 后 5 位（非官方语义）」，或补 EPFO 出处后再沿用现名。

- **留存建议（tools/finance/uan-validator.html）**：保留「12 位长度 + 首字符软判据」的透明口径与「无校验位」免责，轻量直给；修好字符白名单后可留；建议把无出处分段降级为「展示用切片」，并补「粘贴时带 UAN: 前缀自动清洗」的提示。
### F-N153 Aadhaar/CPF 的 `<title>` 与 EIN 的描述被截成半句（低，确认缺陷）
- 问题：`<title>印度 Aadhaar 验证 - 场景的号码格式检查`、`<title>巴西 CPF 验证 - 场景的号码合法性检查` 中「场景的」前被截断，主谓缺失（与 F-N131 同源的模板截断）；EIN 的 description 断在「打开浏览器即可」，缺「使用」。
- 证据：`tools/finance/aadhaar-validator.html:20`、`tools/finance/cpf-validator.html:20`、`tools/finance/ein-validator.html:10`
- 复现：读 `<title>` 与 SERP 预览 → 「印度 Aadhaar 验证 - 场景的号码格式检查」；期望「印度 Aadhaar 号码验证 - 身份核验场景的格式检查」。
- 影响：上述 3 页；搜索结果出现残句，标题与正文关键词（「Aadhaar 号码验证器」）不一致。
- 方案：补全为完整句式并同步 og/twitter/JSON-LD，例如「印度 Aadhaar 号码验证 - 12 位格式与 Verhoeff 校验位检查」。


- **留存建议（tools/finance/word-search.html）**：12×12 网格 + 八词随机 + 拖动/触摸划选 + 反向命中的交互完整，作为休闲记忆游戏可留（且 `cat=game` 属游戏类，放在 finance 行业与主题不符，若保留建议按 §7 评估迁移到 `tools/fun/`，走重定向存根并提死链）；`formula-desc` 已是真实说明（明确不支持自定义词表/尺寸/打印），引据表套话与英文标签已真修（F-N166/167，第101批）；**仍需修好成绩历史（F-N165）并清理 meta/intro/FAQ 残留的自定义/打印承诺（F-N164）后才适合继续对外**；游戏本身建议保留「内置词池 + 一键开始」的零配置形态。

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

- **留存建议（tools/finance/cnpj-validator.html）**：双 mod-11 + 根号/分支号/校验位拆分 + 合法默认样例，骨架正确，建议保留；F-N168/169 已真修（第98批，字符白名单守卫点名非法字符 + 全同数字单独提示 + 顺带 esc() 自 XSS 转义与动态标签 helper），可对外；建议与 CPF/CNPJ 类工具互链并保留「不验证真实性」免责。

- **留存建议（tools/finance/gst-validator.html）**：15 位拆分 + mod-36 校验 + 州码表是差异化能力，建议保留；F-N170/171 已核实真修（第99批：州码白名单硬判 + 25/28 停用码单列 + 26 全称，verify 四锁 00/99/25/28 齐全、9/9 全绿），可对外；建议补「PAN 第 4 位实体类型」说明与 GSTR 类工具互链。

- **留存建议（tools/finance/word-counter.html）**：实时统计 + 可读性 + 词频 + CSV 导出是高频文本能力（不属金融但通用），建议保留；F-N174/175（第93批）、F-N176（第100批，示例改实测 3/1/10 + chars/charsNoSpace 改 Unicode 码点计数 + 公式框口径）均已真修，可对外；建议与 word-frequency/word-wrap 互链。

- **留存建议（tools/finance/text-reverse-words.html）**：三模式 + 保留标点 + 每行/首字母 + 预设 + 复制，作为文本小工具可用，建议保留；F-N177/178/179 已真修（第94批），`cat=text` 却归 finance 行业，建议按 §7 评估迁移（待裁量，本批不做）。

- **留存建议（tools/finance/nie-validator.html）**：mod-23 + X/Y/Z 替换 + 期望字母回显，错误定位清晰，建议保留；F-N180/181 已真修（第95批，前缀文案中性化 + 双实现收敛 nieLetter 单一真源，并顺带把 validate 动态标签全过 i18n helper）；建议与 CPF/CNPJ 页交叉链接。

- **留存建议（tools/finance/iccid-validator.html）**：19/20 位 + Luhn + 分段展示对 SIM/物联网入库有实际价值，建议保留；F-N182/183/184/185 已真修（第96批，E.118 变长分段解析单一真源 parseIccid + 运营商变长前缀最长匹配 + 非89判无效 + E.164 国家码表 + 公式框/FAQ 纠正），可对外。

- **留存建议（tools/finance/bic-lookup.html）**：4+2+2+3 分段解析 + 离线银行表 + 国家名回显，作为汇款填单核对工具价值明确，建议保留；F-N188 已真修（第97批，deep-dive 场景与 FAQ 改为 BIC 专属内容：跨境汇款核对/四段拆解/8 vs 11 位/离线库 33 家/查不到走 SWIFT 官网）；F-N186/187 保留待裁量。

### F-N189 6 个校验页 + 文本反转页：「导出明细 CSV」实为历史表，趋势图 div 永不出现（中，确认缺陷）
- 问题：① 趋势图取 `parseFloat(arr[j].d[rk])`，而 `rk` 存的是整段结果文本（`ResText` 截 80 字，如「输入： … 校验和： ✅ 通过」），`parseFloat` 恒 `NaN`，`nums.length>=2` 永不成立，`#xxxChart` 永远空白（`cnpj:365/368-369`、`gst:388-389`、`imei:382-383`、`text-reverse:405/408-409`、`nie:366-367`、`iccid:384-385`、`bic:395/398-399`）。②「导出明细 CSV」导出的是 `#xxxTable`（历史表），且 `ResText` 用 `/请输入|无效|不正确|错误|Error|NaN/` 过滤（cnpj:328、gst:348、imei:342、text-reverse:368、nie:326、iccid:344、bic:358），CNPJ/IMEI/NIE/ICCID 的失败样本从不入表；首次点击只剩表头。
- 证据：`tools/finance/cnpj-validator.html:323-329`、`:365-369`、`:402-404`；`tools/finance/gst-validator.html:343-349`、`:388-389`、`:422-424`；`tools/finance/imei-validator.html:337-343`、`:382-383`、`:416-418`；`tools/finance/text-reverse-words.html:363-369`、`:408-409`、`:442-444`；`tools/finance/nie-validator.html:321-326`、`:366-367`、`:400-402`；`tools/finance/iccid-validator.html:339-345`、`:384-385`、`:418-420`；`tools/finance/bic-lookup.html:353-359`、`:398-399`、`:432-434`
- 复现（node 实算）：cnpj 页输入 `11222333000182`（校验失败）→ 结果区 ❌，但「数据表/历史」无新增行、CSV 不含该次；`parseFloat("输入： 11222333000181 格式化： …")` = `NaN`，两次计算后 `#cnpj_validatorChart` 仍为空。
- 影响：7 个页面；「趋势图/明细导出」两个可见控件长期空转，用户会反复点击。
- 方案：历史记录增加数值字段（如 `ok: valid?1:0`）供趋势图使用；CSV 改导「当前结果 + 时间」（或按钮改称「导出历史 CSV」）；失败样本也入库并单列「结论」字段。
- **⚠️ F-N189 未整体收口（全站专项，禁止自判完成）**：第 41 批全库扫描 `tools/**/*.html`（4907 页）发现该 Extras 模板是**全站通用注入块**，四特征齐全的旧模板页共 **3155 页**（旧过滤正则 3162、恒 NaN 趋势图 3168、`exportTable('#…Table')` 4503、`history.list().slice(0,10)` 3186），已修仅 15 页。`finance` 分类仍有 **87 页**未修，其余分布 `it 269 / design 82 / machinery 74 / sports 74 / biz 64 / agriculture 61 …` 共 100+ 分类。模板真源 `scripts/_ux_wire.py`（在 git 中，`gen_classic_extras` / `gen_custom_render` 两套注入块），**`_build.py` 不调用它** ⇒ 存量是固化产物、改 HTML 不会被 build 覆盖，但也不能靠改源 + build 自动铺开。跨分类**并非完全同构**（如 `agriculture/agri-calculator.html` 用 `querySelector('.result-box')` 且历史恢复回调额外 forEach 5 个计算函数）⇒ 铺开前须先分型，标准页整体替换、定制页做保留定制的精确局部编辑。下一步：改 `_ux_wire.py` 源防止未来重 wire 倒退 + finance 剩余 87 页分型统计 + 小批试点铺开。

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

> **AC 批 F-N224–F-N233 已全部消费完（2026-11-06）**：9 条修复并分别移交 `plan/已修复/2026-11-06-F-N225-N230-金融贷款族A.md`（6 条）与 `plan/已修复/2026-11-06-F-N224-N233-金融贷款族B.md`（3 条）；F-N231（城市公积金额度口径）已移 `plan/G01-公式与计算正确性裁量项.md` C6 待裁断清单，裁断前不改代码、不计入已修/未修。
> 下方「统计」为 2026-11-04 审计当时的登记数，属历史档案，不代表当前待办数量。

### 统计

- 页数 **10**；独立实现 **10** / 共享模块 **0**；同源模板 **2**（房贷→车贷）。
- 新增 **10** 条（高 **2** / 中 **8** / 假 **0** / 安全 **0**）；编号 F-N224–F-N233。
- 安全：本轮 10 页均注入模板级 `lf1-cdn-tos.bytegoofy.com/ttzz/push.js`（无 SRI），属全站模板既有项，不重复计数。
- 复核既有 13 条：已修/失效 8（F-N9/N10/N11/N12/N21/N23/N27/N96），仍成立 4（F-N25/F-N91/F-N92 部分/F-N97），部分 1（F-N22）；F-N26 已失效（基准已改用应还月供）。
- 复算口径：`M=P·r(1+r)^n/((1+r)^n−1)`、EAR=`(1+r)^12−1`、IRR 用 [0,1] 二分 80 次、信用卡按 `interest=余额×0.0005×30`、`pay=min(余额×比例+息,10)` 逐月；脚本 `/tmp/fin02_audit.js`（node 复算，未改仓库）。

## 2026-11-07 第 39 批 · 陈旧证据复核（10 条，逐条核源码 + 锁定用例，未改任何源码/用例）

> 背景：审计清单里这 10 条仍标「确认」，但后续 T / AC / F-N227 / F-N229 等批次已修，台账未同步。本批**逐条只读复核当前源码与 `verify_finance_calc.js` 实际用例**，确认「源码闭环 + 有强判别锁定用例」后统一标 **复核通过（陈旧证据）**；原条目作为历史档案保留。实跑 `node scripts/verify_finance_calc.js` = **379/379**、单文件判别力 `379 正确变红 / 0 逃生`。AC 批「复核既有 13 条」统计属 2026-11-04 历史快照，其中 F-N25/F-N26 的「仍成立/已失效」描述与当前源码不再对应，以本节为准。

| 编号 | 当前源码闭环 | 锁定用例锚点（`scripts/verify_finance_calc.js`） |
| --- | --- | --- |
| F-N24 零利率被拦截 | `generateSchedule()` 等额本息 `monthlyRate === 0 ? amount/totalMonths`、气球贷 r=0 分支；`__tbInputGuard` 分母表 `__D` 为空，不再整体拒绝 0% | F-N24 用例 `1,000.00 首月月供` / `0.00 总利息` / `12,000.00 总还款额`（12000/0%/1年） |
| F-N25 提前还款分支/负金额 | 先息后本、气球贷均按剩余本金/剩余期数重算；`prepayAmount` 前置拒绝 ≤0 | F-N227 三条：`还款后剩余本金： 900,000.00 元 节省利息： 137,200.00 元`、`减少月供： 0.00 元 新月供：11,454.39 元`、`提前还款金额须大于 0` |
| F-N26 输入月供不参与原方案 | `mortgage-prepayment` 已改「同月供不提前还款」为对照基准 | F-N224 `较对照方案节省（元） 0.00 0.00`、F-N233 `对照方案（不提前还款，月供不变）：月供 3000.00 元 × 263 期，总还款 786133.97 元` |
| F-N29 NPV IRR 无根返回 1000% | `calcIRR` 改端点符号扫描 + 多根识别 + 残差校验，返回 `none/no-positive` 与 `multiple` 状态 | `无解 IRR 内部收益率`、`IRR： ✗ 无解（现金流同号或 NPV 无零点），不可行`、`IRR： ✗ 存在多个根` |
| F-N41 通胀反向折现方向 | `getYearData()` 反向分支已改 `purchasingPower = amt / factor`（正向同式），不再放大 | `折现到现在，价值： ¥ 82,855.87`（120000/2.5%/15年） |
| F-N42 免息期空下拉框 | `bill` / `due` 两个 select 已生成 1–31 全部 option 并带 selected 默认值 | 12/28 组合 `45 天 最长免息期（账单日次日消费）` / `¥12.33`；28 日账单+次月 5 日 `36 天` / `¥9.86` |
| F-N43 定投零输入 −600% | `calcIRR` 先扫 `hasNeg`/`hasPos`，全同号返回 NaN | `无法计算（请输入有效现金流）` |
| F-N49 折扣 chip 单位反了 | chip 模板改 `value="${d * 10}"`、`min=0 max=10`、`placeholder …（0–10 折）`；`updateDiscount` 按「折」口径换算 | `¥ 175.00` / `7.00 折`；F-N48 两条 `折扣须在 0–10 折之间（如 8 表示 8 折）。` |
| F-N50 夏普无风险率错配 | `rfPeriod = annFactor > 1 ? riskFree / annFactor : riskFree`，结果区列出折算式 | `每期无风险利率 = 2.00% ÷ 12 = 0.167%`、`每期夏普比率 = 13.833 ÷ 20.000 = 0.6917`、`年化夏普 = 0.6917 × √12 = 2.3960` |
| F-N52 利润率页折旧未扣 | 公式框与计算链均含「营业利润 − 折旧摊销」「EBITDA = 营业利润 + 折旧摊销」 | `净利率 54.00%` / `EBITDA利润率 60.00%`（500万收入/200万成本/30万折旧） |

- **F-N189 已在第 40 / 41 批改完 `finance` 15 页**（详见 F-N189 条目）。但全库扫描确认该模板是全站通用注入块、尚有 **3155 页**未修，**F-N189 未整体收口**，按「禁止草率收口铁律」另立全站专项分批续修；本表上文「7 页 / 8 页 / 15 页」均只是 `finance` 子集。
- **待裁断**：99 是否作为 GST `Centre (CGST jurisdiction)` 特殊辖区码放行（见 F-N170 第 38 批处置），裁断前不改代码。

## 2026-11-07 第 42 批 · F-N189 全站专项（改模板真源 + 分型 + 试点 8 页，仍未整体收口）

- **改真源 `scripts/_ux_wire.py`**：F-N189 只影响 custom 模式，classic 一行未动。9 处精确替换（`gen_custom_render` 的 head/rows/mount/图表 4 处 + `apply_custom` 的 ResText/Score/Extras/Export 4 处 + 位置感知），`python3 -m py_compile` OK；载入改后模块调 `gen_custom_render('cnpj_validator','validate')` 生成 1757 字符，与已修 cnpj 页 Render 段**逐字一致** ⇒ 未来手动重 wire 不会再注入旧缺陷。`_build.py` 不调用它，改源不影响线上字节。
- **全站分型（4907 页扫描）**：四特征齐全旧模板 **3155 页**，其中**标准同构 3042（96.4%）可整体替换**、定制 107（须保留定制的局部编辑）、异常 6；**3148 页三容器齐全**（Chart/Table/导出按钮真实可见，非装饰）。`finance` 未修 86 页中标准 82。前缀必须从 `exportTable('#([^']+)Table','…')` 第 1 捕获组取（带 `#` 会全量假判 `no_boundary`）。
- **试点铺开 8 页**：`aadhaar-validator` / `aba-validator` / `abn-validator` / `amount-in-words` / `analysis-44` / `analysis-5` / `analysis-cost-1` / `analysis-risk`。参数自适应脚本自动抽取结果容器与计算函数，实测覆盖 `getElementById('output')+validate()`、`querySelector('.result-box')+convert()`、`getElementById('res')+calc()` 三种形态，8/8 与基准新段归一化同构。
- **通用两态锁 `scripts/_verify_fn189_rollout.mjs`**：`--pages` / `--cat` / `--head` / `--ref` / `--verbose` 参数化，页面参数自动抽取，后续所有铺开批次复用，不再每批派生脚本。当前 **209 PASS / 0 FAIL**、`--head` **153 FAIL / 48 PASS**。
- **待老板裁断**：是否一次性铺到全站 3042 标准页（大 diff + 全站产物变化 + 需完整 229 门禁兜底）。裁断前不擅自全量铺开，继续按每批 8–12 页小步推进；定制页另设计保留定制的局部编辑脚本。

## 2026-11-07 第 43 批 · F-N189 铺开工具固化 + finance 第二组 8 页

- **交付 `scripts/_fn189_rollout.py`**：`--cat` / `--pages` / `--dry` 参数化，从 cnpj 基准新段反推模板，自动抽取 5 个页面参数，先全批自检再写盘（边界唯一 / 旧过滤正则 / 恒 NaN 特征 / `__tbScore` 4 处 / csv 名 / 归一化同构），定制页明确拒绝。后续铺开批次复用，不再重写临时脚本。
- **铺开 8 页**：`assessor-manager` / `bic-validator` / `bond-yield-calculator` / `break-even-calculator` / `calc-2` / `calc-3` / `calc-4` / `calc-5`，`--dry` 与 `--apply` 均 8/8；第 33 批 F-N4 在 bond-yield 页的改动 7 处仍在（替换范围不相交）。
- **通用两态锁加固**：注入 canvas `getContext` Proxy 桩 + `canvasColorWithAlpha` / `resolveCanvasColor`；运行期改为直接驱动 `Extras()`（写输入 + 注入成功/失败结果文本），绕开页面 `calc()` 的真机依赖；`VirtualConsole` 静默已知噪音。回归：第 42 批 8 页仍 209 PASS、第 40/41 批抽 4 页 105 PASS。
- 第 44 批方向：finance 第三组 8 页；并设计 4 个定制页（`dca` / `irr` / `npv` / `password-generator-advanced`，均为前批加过快照/IRR 逻辑者）的保留定制局部编辑方案，禁止整体替换。

## 2026-11-08 第 44 批 · F-N189 finance 标准页第三组 + 定制页局部编辑工具

- **铺开工具补洞（真隐患）**：`_fn189_rollout.py` 原「拒绝定制页」只检查旧段长度 >2000，实测对 4 个定制页 `--dry` **全部放行**，整体替换会静默抹掉前批定制逻辑。已改为与 **标准旧段归一化骨架逐字比对**（`scripts/_fn189_std_old_seg_normalized.txt`，2892 字符，取自 HEAD 的 `capm-return`，`cpf-validator`/`credit-card-type` 逐字一致）；不一致即 FAIL 并提示走局部编辑。加固后实测 `dca-calculator` 被正确拒绝。
- **铺开标准页 8 页**：`capm-return` / `car-loan-calculator` / `compound-interest` / `cpf-validator` / `credit-card-bin` / `credit-card-interest` / `credit-card-luhn` / `credit-card-type`，`--dry` 与 apply 均 8/8，覆盖 `getElementById('result'|'output') + capmCalc/validate` 与 `querySelector('.result-box') + calc` 两类形态。
- **交付 `scripts/_fn189_custom_patch.py`**（定制页专用）：只替换 8 个修复锚点（ResText 过滤行+Score / 表头结论列 / 行内结论值 / 历史恢复跳过 `__tbScore` / 趋势数值源 / 趋势名 / Extras 写 `__tbScore` / 导出前补渲染），逐行保留定制。**核心断言**：归一化后「相对标准骨架的增删行集合」替换前后**完全一致** ⇒ 除 F-N189 修复外没动任何其它字节；另断言每锚点段内/全文各恰好 1 次、`__tbScore` 4 处、旧过滤消失、新段仍不同于基准（定制仍在）。
- **4 个定制页修完**：`dca-calculator`（F-N8 时点同步，定制差异 2 行）、`irr-calculator`（现金流快照重建，2 行）、`npv-calculator`（导出前初始投资校验，1 行）、`password-generator-advanced`（历史只存摘要、绝不存明文，6 行）；前批定制锚点全部原样保留。
- **通用两态锁加 `--custom`**：不再要求与基准新段同构，改为断言「仍与基准不同」+「前批定制锚点仍在」（内置 4 页锚点映射，未登记即 FAIL 强制留痕）；其余源码/运行期/EN 态断言不变。
- 证据：`_fn189_rollout.py` 8/8、`_fn189_custom_patch.py` 4/4、`verify_finance_calc.js` **379/379**、判别力 **379 正确变红 / 0 逃生**、id 审计僵尸 0、全站内联脚本 **17035 个 0 语法错**；两态锁标准页 **209 PASS / 0 FAIL**、定制页 **109 PASS / 0 FAIL**；负向锁标准 8 页 **160 FAIL / 41 PASS**、定制 4 页 **76 FAIL / 29 PASS**；`py_compile` OK。
- **finance 剩余归零**：全部 58 页标准模板已在本批与第 45 批（全站批量）覆盖范围；第 44 批结束时 finance 旧模板剩 58 页标准 + 0 定制。
- **老板裁断（2026-11-08）**：同意一次性把修法铺到全站标准页 ⇒ 第 45 批起转全站批量（标准 3018 / 定制 94 / 异常 29）。

## 2026-11-08 第 46 批 · F-N189 全站异常形态清零（31 页 + 工具链 9 处缺陷）

- **全站存量清零**：`_fn189_rollout_all.py --dry` → `custom 0 / std 0 / abnormal 0`（已修 3186 / 无关 1721），F-N189 不再有待修页。
- **6 类异常形态的根因与处置**：过滤行变体（`|⚠`/`|请填写`/`|应大于`/`|抽取中`/`|不能为|必须`）改结构正则改写；**导出目标 ≠ 表容器（5 页，导出恒空 CSV 的真 BUG）**以「唯一 `matrix.table` 容器优先」纠正，Export 内旧容器守卫一并修；**自研趋势源页（CD4/D8 比值、密文输出字节数、平均分/NSP数值）合法跳过趋势改写**，避免把页面兜底逻辑变成死代码；自拼导出族（`exportCsv` / Blob / PNG）分级断言；`chess/gomoku-forbidden` 缺 4 个容器 div 已补；数字开头 id 改走 `getElementById`。
- **工具链 9 处真缺陷**（详见移交文件）：幂等闸缺失导致重复插入 `rec.__tbScore=`（5 处）、导出锚点硬编码 `#<pre>Table` 写坏非标准 host 页、趋势名正则删掉 `name:` 键产出语法错、`OLD_FILTER` 精确串判定漏掉变体页、`classify` 误判半修页与自研趋势页、两态锁 `parsePage` 误取按钮 onclick 的 `exportTable`（前缀判成 `purity` 直接 FATAL）、锁内 `uncaughtException` 静默吞错（exit 0 假绿）、锁桩 `querySelector` 遇数字开头 id 崩溃 + `exportCsv`/Blob 导出不可观测。
- 证据：两态锁本批 35 页逐页 PASS（1 SKIP 已记明「需页面先完成真机计算」）、`--head` 负向正确 FAIL、全站 194 分类抽 2 页 **176 标准同构 + 12 定制全 PASS**、内联脚本 17035 段 0 语法错、`verify_calc.js ALL OK (84 pages)`、`verify_finance_calc.js 379/379`、判别力逃生 20=基线 / 跳过 7=基线（无新增）、全站导出 id 审计 3186 页仅 1 页异常已修。
