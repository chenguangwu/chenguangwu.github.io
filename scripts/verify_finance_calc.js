#!/usr/bin/env node
/**
 * finance 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）；
 * 与之区别仅在于用例集：finance 用校验位算法（Luhn / mod-11 / mod-97 / Verhoeff 等）
 * 与金融公式（单利、贷款月供、ROI、NPV、盈亏平衡、增值税）的独立复算。
 *
 * 用法：
 *   node scripts/verify_finance_calc.js                        # 跑全部用例
 *   node scripts/verify_finance_calc.js credit-card-luhn tax   # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化/运行日期
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（校验位算法 / 标准公式 / 独立复算），必填，便于复核
 *
 * 期望值一律由独立实现或 python 复算得出，不凭记忆。反例（无效号）同样纳入：
 * 验证「算法对无效输入给出正确判定」与验证正例同等重要。
 * 注意：依赖图表（canvas）或依赖「今天」的工具刻意不纳入，否则门禁会随环境失败。
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  // ── 校验位算法类（11 正例 + 2 反例）──────────────────────────────
  {
    slug: "finance/credit-card-luhn",
    inputs: { input: "4532015112830366" },
    expect: ["✅ 通过"],
    ref: "Luhn（模 10）：4532015112830366 为公开测试卡号，加权和 mod 10 == 0",
  },
  {
    slug: "finance/aba-validator",
    inputs: { input: "011000015" },
    expect: ["ABA 路由号码有效"],
    ref: "ABA 3-7-1 权重：Σ = 3×0+7×1+1×1+3×0+7×0+1×0+3×0+7×1+1×5 = 20，mod 10 == 0",
  },
  {
    slug: "finance/iban-validator",
    inputs: { ibanInput: "GB82WEST12345698765432" },
    expect: ["mod-97 校验通过"],
    ref: "ISO 13616：后 4 位前移 → 字母 A=10…Z=35 → 大数 mod 97 == 1（GB82 为公开示例）",
  },
  {
    slug: "finance/cpf-validator",
    inputs: { input: "52998224725" },
    expect: ["CPF 号码有效"],
    ref: "巴西 CPF 模 11 双校验：前 9 位算 DV1，前 10 位算 DV2，余数 <2 记 0",
  },
  {
    slug: "finance/cnpj-validator",
    inputs: { input: "11222333000181" },
    expect: ["CNPJ 号码有效"],
    ref: "巴西 CNPJ 模 11 双校验：权重 [5,4,3,2,9,8,7,6,5,4,3,2]，余数 <2 记 0",
  },
  {
    slug: "finance/abn-validator",
    inputs: { input: "51824753556" },
    expect: ["ABN 号码有效"],
    ref: "澳洲 ABN：首位减 1 后加权 [10,1,3,5,7,9,11,13,15,17,19] 求和 mod 89 == 0",
  },
  {
    slug: "finance/isbn-validator",
    inputs: { isbnInput: "9780306406157" },
    expect: ["校验通过"],
    ref: "ISBN-13：Σ 前 12 位交替权重 1/3 → 校验位 = (10 - Σ mod 10) mod 10 == 第 13 位",
  },
  {
    slug: "finance/sin-validator",
    inputs: { input: "046454286" },
    expect: ["SIN 号码有效"],
    ref: "加拿大 SIN 使用 Luhn：046454286 加权和 mod 10 == 0",
  },
  {
    slug: "finance/dni-validator",
    inputs: { input: "12345678Z" },
    expect: ["DNI 有效"],
    ref: "西班牙 DNI：校验字母 = 'TRWAGMYFPDXBNJZSQVHLCKET'[数字 mod 23]，12345678 mod 23 = 5 → Z",
  },
  {
    slug: "finance/npi-validator",
    inputs: { input: "1234567893" },
    expect: ["NPI 号码有效"],
    ref: "美国 NPI：前缀 80840 拼接后过 Luhn，80840 + 1234567893 加权和 mod 10 == 0",
  },
  {
    slug: "finance/aadhaar-validator",
    inputs: { input: "234123412346" },
    expect: ["Aadhaar 号码有效"],
    ref: "印度 Aadhaar 使用 Verhoeff（十进制非线性和校验），234123412346 校验位正确",
  },
  {
    slug: "finance/tfn-validator",
    inputs: { input: "123456782" },
    expect: ["校验和失败"],
    ref: "澳洲 TFN 反例：权重 [1,4,3,7,5,8,6,9,11]，Σ = 255，255 mod 11 = 2 ≠ 0 → 无效",
  },
  {
    slug: "finance/ird-validator",
    inputs: { input: "123456789" },
    expect: ["校验和失败"],
    ref: "新西兰 IRD 反例：base = 23456789，权重 [3,2,7,6,5,4,3,2]，Σ = 170 → 期望校验位 6 ≠ 9 → 无效",
  },

  // ── 金融公式类（7 个，期望值由 python 独立复算）────────────────────
  {
    slug: "finance/simple-interest",
    inputs: { principal: "25000", rate: "3.6", years: "4" },
    expect: ["3,600 元", "28,600 元", "900 元"],
    ref: "去默认化：单利 利息 = P×r×t = 25000×3.6%×4 = 3600（每年 900），本利和 28600。默认 10000/5%/3 → 500、1,500、11,500，不含上述串",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "850000", rate: "3.85", years: "25" },
    expect: ["4,416.51", "1,324,954.06", "474,954.06"],
    ref: "去默认化：等额本息 月供 = P×i×(1+i)^n/((1+i)^n−1)，i = 3.85%/12 = 0.00320833、n = 300 ⇒ 4416.51；还款总额 1,324,954.06、总利息 474,954.06（= 总额 − 850,000）。默认 100万/4.2%/30 → 4,890.17、1,760,461.83、760,461.83、360 期",
  },
  {
    slug: "finance/calc-5",
    inputs: { cost: "80000", value: "128000", years: "3" },
    expect: ["60.00%", "48,000.00", "16.96%"],
    ref: "去默认化：净收益 = 128000−80000 = 48000；总 ROI = 48000/80000 = 60%；年化 = 1.6^(1/3)−1 = 16.96%。默认 100000/150000/5 → 50.00%、50,000.00、8.45%",
  },
  {
    slug: "finance/calc-3",
    inputs: { initial: "-200000", rate: "10", flows: "60000,60000,60000,60000,60000" },
    expect: ["27,447.21", "1.1372"],
    ref: "去默认化：NPV = −200000 + 60000×年金现值系数(10%,5) = −200000 + 60000×3.7907868 = 27,447.21；PI = 227447.21/200000 = 1.1372。默认 −100000/8%/30000×5 → 19,781.30、1.1978",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { fc: "180000", price: "75", vc: "45" },
    expect: ["450,000 盈亏平衡收入", "6000 盈亏平衡销量", "4.00 经营杠杆系数"],
    ref: "去默认化：单位边际贡献 = 75−45 = 30；盈亏平衡销量 = 180000/30 = 6000 件、平衡收入 = 6000×75 = 450,000 元；经营杠杆 = 8000×30/60000 = 4.00（预计销量 8000 沿用默认）。默认 100000/50/30 → 20.00、5000 件、250,000、2.67。**注意「30.00 单位边际贡献」不可作 expect** —— harness 兜底会调 addScenario() 生成一个模板场景，其单位边际贡献恰为 30.00 ⇒ 默认态也命中（实测 3/3 命中，属逃生项）。同理边际贡献率 40.00% 与默认态同值，也不可用",
  },
  {
    slug: "finance/vat-calculator",
    inputs: { amount: "2500", customRate: "6" },
    expect: ["2,358.49", "141.51"],
    ref: "去默认化：含税价倒推 不含税 = 2500/1.06 = 2358.49、税额 = 141.51（单笔页签读 customRate）。默认 1000/13% → 884.96、115.04；注意批量页签用 batchRate（未注入，仍 13%）输出 2,212.39/287.61，不会撞车",
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "50000", insurance: "8000", special: "3000", threshold: "6000" },
    expect: ["25,001 - 35,000 元 25% ✓ 适用"],
    ref: "非默认输入使应纳税所得额=50000-8000-6000-3000=33000 → 落入第3级(25001-35000)并高亮「✓ 适用」。该级下限修复后为 25001（修复前误把各级下限都写成 3,001）。期望串同时绑定级距与高亮标记：注入失败(回退默认→第2级激活)或旧代码(3,001)均不匹配，既判别力有效又测到修复",
  },
  {
    slug: "finance/number-to-words",
    inputs: { inputVal: "900807.05" },
    expect: ["nine hundred thousand eight hundred seven", "point zero five"],
    ref: "去默认化：900807.05 → nine hundred thousand eight hundred seven point zero five。**同时守住两个已修 P0 缺陷**：① 小数位原用 decPart = n − intPart 的浮点差，900807.05 − 900807 = 0.04999999… ⇒ 会读成 point zero four nine nine…；② ones[0] 是空串（整数读法 0 不发音），原实现会把小数里的 0 吞掉 ⇒ 读成 point five。任一缺陷回归，本例即变红",
  },
  {
    slug: "finance/cagr",
    inputs: { start: "100", end: "200", years: "5" },
    clicks: ["calcTool()"],
    expect: ["14.87"],
    ref: "独立复算：CAGR=(200/100)^(1/5)−1=2^0.2−1=0.148698 ⇒ 14.87%（页面同步给出小数 0.1487）。默认起止/年限不同 ⇒ 不命中。",
  },
  {
    slug: "finance/isbn-validator",
    inputs: { isbnInput: "9780306406157" },
    clicks: ["validate()"],
    expect: ["0-306-40615-2"],
    ref: "ISBN-13 校验位可手算：978030640615 按权重 1/3 加权求和 ⇒ 校验位 7；去掉 978 与校验位后按组号/出版者/书名分段 ⇒ 对应 ISBN-10 为 0-306-40615-2。默认样例与注入不同 ⇒ 不命中。",
  },
  {
    slug: "finance/nric-validator",
    inputs: { input: "S1234567D" },
    expect: ["校验字母： D（期望 D）"],
    ref: "新加坡 NRIC：前缀 S（2000 年前出生公民）+ 7 位数字 1234567，按加权表 mod 11 得余数 ⇒ 校验字母 D。默认态输入不同 ⇒ 不命中。",
  },
  {
    slug: "finance/ifsc-validator",
    inputs: { input: "HDFC0001234" },
    expect: ["分支代码： 001234"],
    ref: "IFSC = 4 位银行代码 + 保留位 0 + 6 位分支代码；HDFC0001234 ⇒ 银行 HDFC Bank、保留位 0、分支 001234。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/gstin-validator",
    inputs: { input: "27AAPFU0939F1ZV" },
    expect: ["校验位： V（期望 V）"],
    ref: "GSTIN 第 15 位为 mod-36 校验位：前 14 位字符编码按序加权求和 mod 36 ⇒ V。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/routing-number-validator",
    inputs: { input: "011000015" },
    expect: ["美联储分区： 01 - Boston"],
    ref: "ABA 路由号 9 位，按 3-7-1 权重加总 ⇒ 校验通过；前两位 01 对应波士顿联邦储备区。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/stock-profit-calculator",
    inputs: { buyPrice: "10", buyQty: "100", sellPrice: "12" },
    clicks: ["calc()"],
    expect: ["+189.38"],
    ref: "买入 100×10=1000、卖出 100×12=1200，价差 200 元扣双向佣金/印花税/过户费合计 10.62 ⇒ 净盈亏 +189.38（+18.84%），且 189.38+10.62=200 可对账。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { revenue: "1000", cogs: "600" },
    expect: ["毛利润 400.00 (40.0%)"],
    ref: "毛利=1000−600=400 ⇒ 毛利率 40.0%。默认态不同 ⇒ 不命中（期间费用沿用默认值的占比串不进锚）。",
  },
  {
    slug: "finance/imei-validator",
    inputs: { input: "490154203237518" },
    expect: ["TAC（前 8 位）： 49015420"],
    ref: "IMEI 分段：TAC 前 8 位 49015420、型号识别 490154、SNR 323751、校验位 8。该页同场结论存在自相矛盾（列出「期望校验位 0」仍判有效），属既有缺陷；本例只锁定可独立复算的分段解析段，不把缺陷结论固化进基线。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/portfolio-return",
    inputs: { r1: "10", r2: "5", w1: "50", w2: "50" },
    clicks: ["calcTool()"],
    expect: ["7.50"],
    ref: "组合预期收益 = 10×50% + 5×50% = 7.50%，权重合计 100%。默认态权重/收益不同 ⇒ 不命中。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "10000", salvage: "1000", life: "5" },
    clicks: ["calc()"],
    expect: ["1,800 直线法首年折旧"],
    ref: "可折旧总额 9000：直线法首年 (10000−1000)/5=1800、双倍余额 10000×2/5=4000、年数总和 5/15×9000=3000。锚取能独立复算的直线法值；默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "10", vc: "6", fc: "10000" },
    expect: ["2500 盈亏平衡销量(件)"],
    ref: "盈亏平衡销量 = 固定成本 /(单价−单位变动成本) = 10000/(10−6) = 2500 件，单位边际贡献 4.00 元、平衡收入 25,000 元。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/vat-calculator",
    inputs: { amount: "1000", rate: "13", dir: "add" },
    expect: ["含税价 1,130.00"],
    ref: "13% 增值税：不含税 1000 ⇒ 税额 130.00 ⇒ 含税价 1130.00。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/tax-bracket",
    inputs: { income: "60000" },
    clicks: ["calc()"],
    expect: ["应缴税款： 3,480 元"],
    ref: "应纳税所得额 60000 落入 10% 级（>36000），速算扣除数 2520 ⇒ 60000×10%−2520=3480。默认所得额不同 ⇒ 不命中。",
  },
  {
    slug: "finance/number-to-words",
    inputs: { inputVal: "1234" },
    clicks: ["convert()"],
    expect: ["one thousand two hundred thirty-four"],
    ref: "1234 ⇒ one thousand two hundred thirty-four。与既有 900807.05 用例互补（后者守小数位缺陷，本例守整数段）。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "99.99" },
    clicks: ["convert()"],
    expect: ["玖拾玖元玖角玖分"],
    ref: "99.99 ⇒ 玖拾玖元玖角玖分（角、分各读一次，不漏「零」）。默认金额不同 ⇒ 不命中。",
  },
  {
    slug: "finance/word-counter",
    inputs: { input: "apple banana apple cherry" },
    clicks: ["analyze()"],
    expect: ["4 英文单词"],
    ref: "统计口径：非空白字符切词 ⇒ 4 个英文单词、25 总字符数（含空格）、0 中文字符。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "finance/word-frequency",
    inputs: { input: "apple banana apple cherry" },
    clicks: ["analyze()"],
    expect: ["apple 2 (50.00%)"],
    ref: "词频统计：apple 出现 2 次占 50%、banana/cherry 各 1 次占 25%（总 4 次），唯一词 3、TTR 75%。结果区同时给出英文 summary 行。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "finance/mirror-text",
    inputs: { input: "abc" },
    clicks: ["convert()"],
    expect: ["ɔdɒ"],
    ref: "逐字符镜像：a↔ɔ、b↔d、c↔ɔ ⇒ 输出 ɔdɒ（同时给出 transform: scaleX(-1) 的 CSS 方案）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/vin-validator",
    inputs: { vinInput: "1M8GDM9AXKP042788" },
    clicks: ["validate()"],
    expect: ["校验位 (第 9) X"],
    ref: "VIN 17 位：WMI=1M8、VDS=GDM9AX（第 9 位为校验位 X）、VIS=KP042788，地区北美、年份 K ⇒ 1989/2019。校验位可独立复算（权重表 mod 11）。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "finance/abn-validator",
    inputs: { input: "51824753556" },
    expect: ["校验和： ✅ 通过"],
    ref: "澳洲 ABN：首位 −1 后按权重 10,1,3,…,19 加权，求和 mod 89 = 0 即通过 ⇒ 51824753556 有效。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/ein-validator",
    inputs: { input: "123456789" },
    expect: ["格式化： 12-3456789"],
    ref: "美国 EIN 按 2 位前缀 + 7 位序号格式化 ⇒ 12-3456789，并映射到 IRS 中心。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/swift-bic-validator",
    inputs: { input: "DEUTDEFF500" },
    expect: ["分支代码： 500"],
    ref: "BIC 11 位：银行代码 DEUT、国家 DE、位置 FF、分支 500；可独立按 4/2/2/3 分段校验。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/dni-validator",
    inputs: { input: "12345678Z" },
    expect: ["校验字母： Z（期望 Z）"],
    ref: "西班牙 DNI：8 位数字 mod 23 映射到字母表 TRWAGMYFPDXBNJZSQVHLCKET ⇒ 12345678 对应 Z。可手算，结论双写「实得/期望」判别力最强。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/npi-validator",
    inputs: { input: "1789123456" },
    expect: ["校验和： ✅ 通过"],
    ref: "美国 NPI：前缀 80840 + 10 位，按 Luhn 校验 ⇒ 1789123456 通过。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "120000", annualRate: "6", loanYears: "10" },
    clicks: ["calc()"],
    expect: ["1,332.25 首月月供"],
    ref: "等额本息月供 = P·i·(1+i)^n/((1+i)^n−1)，i=6%/12=0.005、n=120 ⇒ 1,332.25 元；首期利息 600.00、本金 732.25、剩余本金 119,267.75。可独立复算，默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/simple-interest",
    inputs: { principal: "20000", rate: "4", years: "2" },
    clicks: ["calc()"],
    expect: ["累计利息： 1,600 元"],
    ref: "单利：每年利息 20000×4%=800，2 年累计 1,600，本利和 21,600。默认样例恰为 10000/5%/3 年 ⇒ 必须换一组数才破双态。",
  },
  {
    slug: "finance/salary-after-tax",
    inputs: { gross: "20000", ins: "1000", ded: "500", months: "12" },
    clicks: ["calcTool()"],
    expect: ["1,290.00 当月个税"],
    ref: "应纳税所得额 = 20000 − 1000（五险一金）− 500（专项附加）− 5000（减除费用）= 13,500 ⇒ 适用 20% 与速算扣除 1410 ⇒ 13500×20%−1410 = 1290。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/credit-card-type",
    inputs: { input: "4111111111111111" },
    expect: ["卡片类型： Visa"],
    ref: "卡BIN 识别：4111… 为 Visa（长度 16 校验通过）。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "finance/currency-symbol",
    inputs: { searchInput: "USD" },
    clicks: ["showDetail()"],
    expect: ["共找到 1 种货币"],
    ref: "按关键字过滤货币表，`USD` 命中 1 种（附符号与详情页）。默认态（无关键字）命中数不同 ⇒ 不命中。",
  },
  {
    slug: "finance/inflation-calculator",
    inputs: { amt: "1000", rate: "3", years: "10" },
    clicks: ["switchMode()"],
    expect: ["¥ 1,343.92"],
    ref: "通胀口径：¥1,000 按年 3% 经 10 年 ⇒ 1,000×1.03^10 = 1,343.92，标注为「现在值 → 10 年后等价」，同时给出贬值幅度 −34.39%（=1−1/1.3439）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { cost: "10000", return: "12000", years: "2" },
    clicks: ["switchTab()"],
    expect: ["20.00% 总回报率 ROI"],
    ref: "ROI=(12000−10000)/10000=20.00%，净利润 +2,000 元，同场给出 10.00% 简单年化与 NPV 884.35。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/currency-lookup",
    inputs: { input: "USD" },
    expect: ["US Dollar（美元）", "符号： $"],
    ref: "ISO 4217 查询：`USD` ⇒ 名称 US Dollar、符号 $、最小单位 2 位、使用地区美国。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/vcard-qr",
    inputs: { fn: "Zhang", ln: "San", org: "ACME", title: "Eng", tel: "13800138000", email: "a@b.com", url: "https://a.com" },
    clicks: ["generate()"],
    expect: ["FN:ZhangSan"],
    ref: "vCard 3.0 文本：姓/名写入 `N:San;Zhang;;;`，字段名用大写驼峰（`FN`/`ORG`/`TEL`/`EMAIL`/`URL`），电话带 `;TYPE=CELL`。产物与输入形态不同 ⇒ 天然非回显。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { s0: "100", strike: "105", premium: "3", mult: "100", fee: "1" },
    clicks: ["switchTab()"],
    expect: ["盈亏平衡点： 108.00 元", "最大亏损： ¥300.00"],
    ref: "看涨买方：盈亏平衡点 = 行权价 + 权利金 = 105 + 3 = 108.00 元；到期价 100 < 行权价 ⇒ 不行权，亏损 = 权利金 300 + 手续费 2 = ¥300.00。可独立复算。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/credit-card-bin",
    inputs: { input: "411111" },
    expect: ["发卡机构： Chase Bank (测试卡)"],
    ref: "BIN 库查询：`411111` ⇒ 网络 Visa、类型 Credit、国家 US、机构 Chase Bank（测试卡）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/bic-lookup",
    inputs: { input: "DEUTDEFF500" },
    expect: ["银行名称： Deutsche Bank (德国)"],
    ref: "BIC 反查：`DEUTDEFF500` ⇒ 银行代码 DEUT ⇒ Deutsche Bank（德国）、国家 DE、位置 FF、分支 500。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/postal-code-validator",
    inputs: { input: "100000" },
    expect: ["China（CN）：6 位数字"],
    ref: "6 位数字邮编匹配多国格式：`100000` 命中 RU/CN/IN/SG 及「香港无邮编系统」。锚取可独立核对的国家条目。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/zip-code-validator",
    inputs: { input: "95014" },
    expect: ["前 3 位（SCF）： 950", "✅ ZIP Code 格式有效"],
    ref: "美国 ZIP：`95014` ⇒ 5 位 ZIP + 前 3 位 SCF 950（未映射到已知州/地区）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/voter-id-validator",
    inputs: { input: "ABC1234567" },
    expect: ["州代码： ABC", "校验算法： 无（EPIC 为格式校验）"],
    ref: "印度 EPIC 选民 ID：3 字母州代码 + 7 位序号，仅做格式校验（无校验位）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/imsi-validator",
    inputs: { input: "310150123456789" },
    expect: ["MCC（前 3 位）： 310 - 美国", "MNC（第 4-5 位）： 15 - 未知运营商"],
    ref: "IMSI 15 位分段：MCC=310（美国）、MNC=15（未知运营商）、MSIN=0123456789；官方说明 IMSI 无标准校验位，仅格式校验。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/meid-validator",
    inputs: { input: "490154203237518" },
    expect: ["制造商代码（前 8 位）： 49015420", "序列号（后 6 位）： 323751"],
    ref: "MEID 十六进制形态：前 8 位 49015420 为制造商码、后 6 位 323751 为序列号。该页同场的「校验位： 8（期望 C）❌ 校验失败」与 `it/imei-validator` 对同一号码的结论相反，属既有缺陷；本例只锁定可独立复算的分段解析段。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "100000", rate: "5", months: "360", prepay: "10000" },
    clicks: ["calc()"],
    expect: ["剩余期数约 33 个月"],
    ref: "提前还本 10,000 元：原月供 536.82 元不变，冲掉本金后剩余期数由 360 期压缩到约 33 期，节省利息 94,255.78 元。同时守住「模式二（降低月供）月供 483.14 元、期限不变」这条分支。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/retirement-calculator",
    inputs: {
      currentSavings: "100000",
      monthlyContribution: "5000",
      returnRate: "5",
      inflation: "3",
      retireAge: "60",
      lifeAge: "90",
      monthlyExpense: "8000",
    },
    clicks: ["calc()"],
    expect: ["441.85万 退休时资产（名义）", "75.8% 资金充足度"],
    ref: "30 岁起每月存 5,000、60 岁退休、lifeAge 90：名义退休资产 441.85 万，4% 法则所需 582.54 万 ⇒ 充足度 75.8%（不足），退休后实际月支取 6,675.55 元。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/dea-validator",
    inputs: { input: "ABC123" },
    expect: ["长度必须为 9 字符（2 字母 + 7 数字）"],
    ref: "DEA 编号规则 = 2 字母 + 7 数字共 9 位，`ABC123` 只有 6 位 ⇒ 长度校验直接失败。默认态为空输入，不命中本串。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: { initial: "2000", monthly: "300", rate: "4", years: "5" },
    clicks: ["switchTiming()"],
    expect: ["¥22,331.69"],
    ref: "初始 2,000 + 每月定投 300、共 60 期、年化 4%（月末扣款）⇒ 期末 22,331.69、累计收益率 +11.66%。刻意换掉默认的首组参数（默认 initial 1,000/monthly 500/rate 5/years 10 得 79,288.15）⇒ 不命中。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: {
      initial: "10000",
      monthly: "1000",
      rate: "8",
      years: "10",
      buyFee: "0.5",
      sellFee: "0.5",
      manageFee: "1",
      custodyFee: "0.2",
    },
    clicks: ["setRate()"],
    expect: ["费用合计 ¥1,206.39"],
    ref: "费用合计 = 申购 0.5% + 赎回 0.5% + 管理费 1%/年 + 托管 0.2%/年 在 13 万累计投入上的累计扣费 1,206.39 元。注意该页存在「预期年化显示为 0.00%」的注入失效缺陷，本例只锚费用合计，不把缺陷值固化成正确。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: { pv: "100000", months: "60", downPct: "10", fee: "1000" },
    clicks: ["setRate()"],
    expect: ["每月还款：¥1,500.00"],
    ref: "租赁物 100,000、首付 10%（10,000）⇒ 融资金额 90,000，分 60 期等额本息 ⇒ 月供 1,500.00，总还款 101,000。该页名义利率注入不生效（显示 0.00%），故只锚与利率无关的本金/期数派生量。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-calculator",
    inputs: { initial: "10000", additional: "1000", years: "10", final: "25000" },
    clicks: ["calc()"],
    expect: ["期末价值： 25,000 元", "累计回报率： 127.27%"],
    ref: "初始 10,000 + 追加 1,000（共 11,000）⇒ 期末 25,000，累计回报率 (25000−11000)/11000 = 127.27%，CAGR 8.56%。默认态 final=18000 得 累计回报率 38.46% ⇒ 不命中。",
  },
  {
    slug: "finance/number-to-words-chinese",
    inputs: { inputVal: "1234" },
    clicks: ["convert()"],
    expect: ["一千二百三十四"],
    ref: "1234 的中文读法：一千二百三十四（「二」非「两」，十位「十」不补零）。默认态为空输入，不命中。",
  },
  {
    slug: "finance/iccid-validator",
    inputs: { input: "8986011234567890123" },
    expect: ["国家代码（第 3-4 位）： 86", "校验位： 3"],
    ref: "ICCID 19 位：前 2 位 89 = ITU 电信、第 3-4 位 86 = 中国、第 5-7 位 011 = 发卡机构、末位 3 为 Luhn 校验位。该号 Luhn 实际不通过（页内如实报「❌ 校验失败」），本例只锁分段解析段。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "49155402372518" },
    expect: ["国家代码： +49 - 德国", "E.164 格式： +49155402372518"],
    ref: "E.164：去掉前缀 0 后 14 位 ≤ 15 上限，+49 为德国。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/pan-validator",
    inputs: { input: "AAACN0927F" },
    expect: ["校验位： F ✅ PAN 号码格式有效"],
    ref: "印度 PAN：10 位，第 4 位 C = Company，前 5 位 AAACN 为实体代码，0927 为序号，末位 F 为校验位（第四位为 C 时格式校验通过）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/tin-validator",
    inputs: { input: "123456789" },
    expect: ["SSN 格式： 123-45-6789", "Area： 123 Group： 45 Serial： 6789"],
    ref: "美国 TIN 中的 SSN：9 位分三段 123-45-6789（Area/Group/Serial）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/uan-validator",
    inputs: { input: "333333333333" },
    expect: ["区域： 33 EPFO 办公室： 33333"],
    ref: "印度 EPFO UAN 为 12 位纯格式校验：首两位 33 = 区域码，接着 8 位机构码，末 2 位序号。该页额外标注「首字符通常为 1」的软提示，属正常提示不是缺陷。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/sort-code-validator-validator",
    inputs: { input: "112233" },
    expect: ["可能银行： Lloyds Bank"],
    ref: "英国 Sort Code 6 位，前 2 位 11 对应 Lloyds Bank。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/nie-validator",
    inputs: { input: "12345678Z" },
    expect: ["首字符为 X/Y/Z，中间 7 位数字，末尾大写字母"],
    ref: "西班牙 NIE 须以 X/Y/Z 开头 + 7 位数字 + 校验字母；喂入的 `12345678Z` 是 DNI 形态（数字开头）⇒ 如实报格式不符。默认态为空输入 ⇒ 不命中。",
  },
  {
    slug: "finance/esn-validator",
    inputs: { input: "356938035643809" },
    expect: ["ESN HEX 应为 8 位十六进制"],
    ref: "ESN 有两种形态：8 位十六进制或 11 位十进制，15 位既非 HEX8 也非 DEC11 ⇒ 如实报格式不符（页内同场提示「ESN 已被 MEID 取代」）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/car-loan-calculator",
    inputs: { price: "200000", downPct: "20", rate: "4.5", years: "5" },
    clicks: ["calculate()"],
    expect: ["2,982.88", "18,972.98"],
    ref: "车价 200,000 首付 20% ⇒ 贷款 160,000，4.5%/年 60 期 ⇒ 月供 2,982.88、利息合计 18,972.98、利息占比 10.6%，落地总价 224,569.12。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/analysis-risk",
    inputs: { f: "100000", dec: "10", n: "5" },
    clicks: ["calc()"],
    expect: ["DCL = 1.33 × 1.20 = 1.60"],
    ref: "经营杠杆 DOL = 贡献边际 400,000 ÷ EBIT 300,000 = 1.33；财务杠杆 DFL = EBIT 300,000 ÷ (EBIT−利息 50,000) = 1.20；总杠杆 DCL = 1.33 × 1.20 = 1.60。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/analysis-5",
    inputs: {
      pre: "100000",
      ca: "60000",
      cl: "40000",
      inv: "80000",
      cash: "20000",
      tl: "150000",
      ta: "300000",
    },
    clicks: ["calc()"],
    expect: ["流动比率 1.50"],
    ref: "流动比率 = 流动资产 60,000 ÷ 流动负债 40,000 = 1.50。刻意同时录入大额存货(80,000)与预付费用(100,000)使速动比率算出 −3.00 —— 这是该页既有缺陷（速动资产口径把预付费用逐项扣了两次），因此只锚纯可复算的流动比率，不把缺陷值固化成正确。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/assessor-manager",
    inputs: {
      revenue: "1000000",
      currentRatio: "2",
      debtRatio: "0.4",
      profitMargin: "0.15",
      overdue: "1",
      creditHistory: "1",
    },
    clicks: ["calc()"],
    expect: ["信用评分： 75 /100"],
    ref: "该页把利润率/负债率按「百分数字符串」显示（注入 0.15 显示成 `净利润率：0.15%`），属既有百分比口径缺陷；本例只锚评分侧的 `75 /100` 结论。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/report-1",
    inputs: { premium: "5000", inv: "100000", capital: "500000", pct: "0.12" },
    clicks: ["calc()"],
    expect: ["子公司净资产 = 实收资本 500,000.00 + 未分配利润 200,000.00 + 评估增值 5,000.00 = 705,000.00 元"],
    ref: "子公司净资产 = 实收资本 500,000 + 未分配利润 200,000 + 评估增值 5,000 = 705,000（纯加法段，可独立复算）。该页 `pct` 按百分数解读（注入 0.12 得股权 0.12%、少数股东权益 704,154），属既有缺陷 ⇒ 本例只锁加法段，不把缺陷值固化成正确。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { rate: "10", init: "10000" },
    clicks: ["addCashFlow()"],
    expect: ["-490.4 NPV 净现值"],
    ref: "初始 10,000 / 折现 10% / 年年末 +3,000 ⇒ NPV = −10,000 + 2,727.27 + 2,479.34 + 2,253.94 + 2,049.04 ≈ −490.4，页内同场给 IRR 7.71%、PI 0.951、回收期 3.33 期。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/payroll-calculator",
    inputs: { salary: "20000", base: "20000" },
    clicks: ["switchTab()"],
    expect: ["个人所得税 ¥740.00", "¥14,760 税后月薪"],
    ref: "月薪 20,000、五险一金基数同 20,000、专项附加扣除 1,000/月 ⇒ 应纳税所得额，个税 740.00 元、税后到手 14,760 元、公积金账户 4,800/月（个人+单位）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/calc-2",
    inputs: { initial: "10000" },
    clicks: ["calc()"],
    expect: ["无法计算 IRR"],
    ref: "只有初始投入、无后续现金流 ⇒ 符号未变化、数据不足 ⇒ 如实报 IRR 不可解（这正是该页的边界分支，不是缺陷）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/bic-validator",
    inputs: { input: "DEUTDEFF500" },
    expect: ["银行代码： DEUT", "国家代码： DE", "分支代码： 500"],
    ref: "BIC 11 位 = 银行代码 DEUT + 国家代码 DE + 位置代码 FF + 分支代码 500，格式校验通过。默认态为空输入 ⇒ 不命中。",
  },
  {
    slug: "finance/curp-validator",
    inputs: { input: "GOMC800101HDFLRN09" },
    expect: ["校验位： 9（期望 1）"],
    ref: "墨西哥 CURP：姓名首字母 GOMC + 生日 800101 + 性别 H（男）+ 州代码 DF + 辅音 LRN。同场如实报「校验位： 9（期望 1）❌ 校验失败」—— 该号确实不是合法 CURP（这是内容问题不是代码缺陷），本例只锁校验位比对段。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/driver-license-validator",
    inputs: { input: "DL123456789012" },
    expect: ["不匹配任何已知驾照格式"],
    ref: "喂入一个拼凑串 ⇒ 该页如实报「不匹配任何已知驾照格式（支持美国多州/加拿大/英国/德国/澳大利亚/中国）」。默认态为空输入 ⇒ 不命中。",
  },
  // ---- BATCH261：finance 分类「CAPM/复利/债券/租金回报/凯利/真实费率/免息期/寿险需求」族（8 例） ----
  {
    slug: "finance/capm-return",
    inputs: { rf: "0.04", beta: "1.5", rm: "0.10", obs: "0.15" },
    clicks: ["calcTool()"],
    expect: ["β × (R m − R f ) = 1.5 × 6.000% = 9.000%", "E(R) = 4.000% + 9.000% = 13.0000%"],
    ref: "CAPM 单因子模型（无风险利率 Rf = 4%、β = 1.5、市场收益率 Rm = 10%、资产预期收益 15%）：市场风险溢价 = Rm − Rf = 10% − 4% = **6.000%**；风险补偿 = β×(Rm−Rf) = 1.5×6% = **9.000%**；必要收益率 E(R) = 4% + 9% = **13.0000%**。整页把中间式直接印在明细区，两条 expect 分别是「一步乘法」与「一步加法」，且与卡片上的「β 1.25 ⇒ 11.500%」对照行不同源。默认组（3% / 1.2 / 8% ⇒ 溢价 5%、补偿 6%、E(R) 9.0000%）不命中。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "20000", rate: "6", years: "10", annual: "0" },
    clicks: ["calc()"],
    expect: ["20,000.00 0.00 1,200.00 21,200.00", "21,200.00 0.00 1,272.00 22,472.00"],
    ref: "复利计算器（本金 20,000 元、年利率 6%、期限 10 年、每年追加投入 0，默认频率「年复利」）：第 1 行期初 20,000.00、追加 0.00、利息 = 20,000×6% = **1,200.00**、期末 **21,200.00**；第 2 行期初改为上一行期末 21,200.00、追加 0.00、利息 = 21,200×6% = **1,272.00**（多出的 72.00 元正是「利滚利」的证据）、期末 **22,472.00**。锚取**相邻两行的「本金 → 利息」递推**，第 2 行不可能由默认值撞出（默认本金 10,000 / 5% ⇒ 利息 500.00 / 525.00）。",
  },
  {
    slug: "finance/bond-yield-calculator",
    inputs: { "y-face": "1000", "y-coupon": "6", "y-price": "800", "y-years": "5" },
    clicks: ["calc()"],
    expect: ["当期收益率： 7.50%", "年利息收入： ¥60.00"],
    ref: "债券收益率（面值 1,000 元、票面利率 6%、买入价 800 元、剩余 5 年）：年利息 = 1,000×6% = **¥60.00**；当期收益率（Current Yield）= 年利息/市价 = 60/800 = **7.50%**（一步相除）。同一价格下 YTM 是迭代解（页面给 11.476%，手算不可复算）⇒ **不锚 YTM**，只锚这两个一步量。默认组（1,000 / 5% / 950 ⇒ 年利息 50 / 当期收益率 5.26%）不命中。",
  },
  {
    slug: "finance/rental-yield-calculator",
    inputs: { price: "500", area: "100", rent: "8000", fee: "0", heat: "2000", tax: "1000" },
    clicks: ["calc()"],
    expect: ["毛回报率 1.92%", "年净收入 87,000"],
    ref: "房租回报率（总价 500 万、面积 100㎡、月租 8,000 元、无中介费、取暖 2,000 元/年、税费其他 1,000 元/年）：年租金收入 = 8,000×12 = 96,000 元；毛回报率 = 96,000/5,000,000 = **1.92%**（一步相除）；年度成本合计 = 取暖 2,000 + 装修折旧 5,000 + 维修基金 1,000 + 税费 1,000 = 9,000 元；年净收入 = 96,000 − 9,000 = **87,000 元**。两条一个「毛口径」一个「净口径」，同源不同式。默认组（300 万 / 5,000 元 ⇒ 2.00% / 5 万）不命中。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "k-capital": "200000", "k-winrate": "60", "k-ratio": "2.5", "k-fraction": "0.4" },
    clicks: ["calc()"],
    expect: ["/ 2.5 = 44.00%", "建议仓位比例： 17.60%"],
    ref: "凯利公式仓位（资金 20 万、胜率 60%、盈亏比 2.5:1、按半凯利即 fraction=0.4 使用）：f* = (p×b − q)/b = (60%×2.5 − 40%)/2.5 = (1.5−0.4)/2.5 = **44.00%**；建议仓位比例 = 凯利分数 × fraction = 44% × 40% = **17.60%**；建议仓位金额 = 200,000 × 17.6% = ¥35,200（同页第三行）。整条链路三个量都只由注入值一步得出。默认组（10 万 / 55% / 2 / 0.5 ⇒ 32.50% / 16.25%）不命中。",
  },
  {
    slug: "finance/installment-real-rate",
    inputs: { P: "24000", n: "24", r: "1.2" },
    clicks: ["calcTool()"],
    expect: ["1,288.00 每期还款额（元）", "6,912.00 总手续费（元）"],
    ref: "分期实际费率（本金 24,000 元、24 期、月手续费率 1.2%）：每期手续费 = 24,000×1.2% = 288.00 元，每期本金 = 24,000/24 = 1,000.00 元 ⇒ 每期还款 **1,288.00 元**（一步相加）；总手续费 = 288.00×24 = **6,912.00 元**。注意注入值刻意避开默认组（12,000 / 12 / 0.6）—— 那组算出的「1,072.00 / 864.00」才是默认值 ⇒ 若沿用默认值会出现「注入值 == 默认值」的伪判别。默认组不同 ⇒ 不命中。",
  },
  {
    slug: "finance/credit-card-grace-period",
    inputs: { amt: "5000", yield: "2.0" },
    clicks: ["calcTool()"],
    expect: ["¥12.05 最长免息期资金收益（2%年化）", "¥7.95 账单日次日 vs 当天消费收益差"],
    ref: "信用卡免息期资金收益（账单金额 5,000 元、按 2% 年化理财）：把 5,000 元多占 44 天，收益 = 5,000×2%×44/365 = **¥12.05**；账单日当天消费只能占 29 天 ⇒ 5,000×2%×29/365 = **¥7.95**，两值同用一个式、只差天数（44 / 29），差额 4.10 元正是「账单日次日消费」这一最佳实践的量化依据。默认组金额 10,000 ⇒ 24.11 / 15.89，不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "25", dt_expense: "15", dt_debt: "50", dt_existing: "20" },
    clicks: ["calc()"],
    expect: ["250万 (年收入×10)", "2.5万 年收入×10%"],
    ref: "家庭保障缺口测算（输入为「当前年收入 25 万」等四项）：寿险保额 = 年收入×10 = **250 万**（覆盖 10 年收入替代）；年保费预算 = 年收入×10% = **2.5 万**；重疾保额 = 年收入×5 = 125 万；意外险保额 = 年收入×10 = 250 万。四条**全部只由年收入一步乘出**，同页还给出「寿险 280 万」（覆盖家庭负债口径，与 250 万属不同规则 ⇒ 本身就是一条天然阴性对照）。默认组年收入 20 万 ⇒ 200 万 / 2 万，不命中。",
  },
  // ---- BATCH262：finance 分类「CAGR/折旧/利润率/股价/期权/单利/金价/盈亏平衡/折扣链/房贷/积分/薪资」族（12 例） ----
  {
    slug: "finance/cagr",
    inputs: { start: "80", end: "240", years: "6" },
    clicks: ["calcTool()"],
    expect: ["20.09 CAGR (%)", "0.2009 增长率 (小数)"],
    ref: "年化复合增长率（期初 80 万元、期末 240 万元、6 年）：CAGR = (240/80)^(1/6) − 1 = 3^0.166667 − 1 = **20.09%**，页面同时给出小数口径 **0.2009**，两条同源于一个幂运算、可一步复核。默认组（100→200 / 7 年 ⇒ 10.49% / 0.1049）不命中。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "90000", salvage: "6000", life: "3", totalUnits: "8000" },
    clicks: ["calc()"],
    expect: ["28,000 直线法首年折旧", "42,000 SYD首年折旧"],
    ref: "固定资产折旧（原值 90,000、残值 6,000、年限 3 年）：可折旧总额 = 90,000 − 6,000 = 84,000；直线法首年 = 84,000/3 = **28,000**；年限总和法首年 = 84,000×3/(3×4/2) = **42,000**。两条都是一步乘除，且刻意避开第一组注入值（80,000 / 4,000 / 4 年 ⇒ 19,000 / 30,400）—— 那组算出的直线法首年恰好 19,000，与默认组（100,000 / 5,000 / 5 年）撞同值 ⇒ 首轮判逃生项，换组后方有判别力。默认组不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { revenue: "2000000", cogs: "1100000" },
    clicks: ["calc()"],
    expect: ["毛利润 90.00万 (45.0%)", "净利率 24.38%"],
    ref: "利润率（营业收入 200 万、营业成本 110 万，其余费用沿用默认档）：毛利润 = 200 − 110 = 90.00 万，毛利率 = 90/200 = **45.0%**；营业利润 67.00 万 ⇒ 营业利润率 **33.50%**；利润总额 65.00 万，所得税（25%）16.25 万 ⇒ 净利润 **48.75 万**，净利率 = 48.75/200 = **24.38%**。四条全部只用注入值与默认档一步相除/相减。默认组（100 万 / 60 万 ⇒ 40.00万 / 40.0%）不命中。",
  },
  {
    slug: "finance/stock-profit-calculator",
    inputs: { buyPrice: "12.5", buyQty: "800", sellPrice: "14.2", commissionRate: "0.025", stampRate: "0.05", transferRate: "0.001", minCommission: "5" },
    clicks: ["calc()"],
    expect: ["+1,344.11", "+13.43%"],
    ref: "股票买卖盈亏（买入 12.50 × 800 股 = 10,000、卖出 14.20 × 800 = 11,360，佣金 0.025% 最低 5 元、印花税 0.05% 单边、过户费 0.001%）：买入成本 = 10,000 + 佣金 5.00（按 0.025% 仅 2.50 元，触发「最低 5 元」档）= 10,005.10；卖出费用 = 佣金 5.00 + 印花税 5.68 + 过户费 0.11 = 10.79 ⇒ 净收入 11,349.21；净盈亏 = 11,349.21 − 10,005.10 = **+1,344.11**，收益率 = 1,344.11/10,005.10 = **+13.43%**。两条同源、均可一步复核。默认组（10 / 11 / 1000 股）不命中。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { strike: "90", premium: "4", s0: "105", contracts: "2", mult: "100", fee: "2" },
    clicks: ["calc()"],
    expect: ["盈亏平衡点： 94.00 元", "总盈亏：+¥2,192.00"],
    ref: "看涨期权买方盈亏（行权价 90、权利金 4 元/股、到期价 105、2 张 × 乘数 100、手续费 2 元/侧）：盈亏平衡点 = 行权价 + 权利金 = 90 + 4 = **94.00 元**（一步相加）；权利金成本 = 4×100×2 = 800.00，交易手续费合计 8.00（开仓+平仓）；总盈亏 = (105 − 90 − 4)×100×2 − 8 = 2,200 − 8 = **+2,192.00**。一条「一步相加」、一条「（价差−权利金）×乘数×张数 − 手续费」，同源不同式。默认组（100 / 5 / 110 / 1 张）不命中。",
  },
  {
    slug: "finance/simple-interest",
    inputs: { principal: "25000", rate: "4.5", years: "4" },
    clicks: ["calc()"],
    expect: ["每年利息： 1,125 元", "本利和： 29,500 元"],
    ref: "单利（本金 25,000、年利率 4.5%、4 年）：每年利息 = 25,000×4.5% = **1,125 元**；累计利息 = 1,125×4 = 4,500；本利和 = 25,000 + 4,500 = **29,500 元**。页面逐年明细第 1 年末累计利息 1,125 / 本利和 26,125，第 4 年末 4,500 / 29,500，与两条锚同源。默认组（10,000 / 5% / 3 年 ⇒ 1,500 / 14,500）不命中。",
  },
  {
    slug: "finance/gold-price-calculator",
    inputs: { goldPrice: "600", usdRate: "7.1", discountRate: "90", weightInput: "8" },
    clicks: ["calcAll()"],
    expect: ["10.8344 克", "¥600.00/克"],
    ref: "黄金折算（总投入 6,500 元、足金 999.9 含金量 99.99%、现价 600 元/克）：页面自印计算式 6,500 ÷ (含金量 99.99% × ¥**600.00**/克) = **10.8344 克**，其中 600.00 即注入现价（一步取值）、10.8344 即该式结果（6,500/(0.9999×600) = 10.83447，一步可复算）。同页纯度表列出足金 99.99% 每克 599.94 元、18K 金每克 450.00 元，均 = 600×纯度 ⇒ 自洽。默认现价 650 ⇒ 10.0015 克，不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { fc: "150000", price: "60", vc: "35", taxRate: "25" },
    clicks: ["calc()"],
    expect: ["变动成本总额：280,000.00 元", "经营杠杆系数： 4.00"],
    ref: "本量利分析（固定成本 150,000、单价 60、单位变动成本 35、销量沿用默认 8,000、所得税 25%）：销售收入 = 8,000×60 = 480,000 元；变动成本总额 = 8,000×35 = **280,000.00 元**（一步相乘）；盈亏平衡量 = 150,000/(60−35) = 6,000 件 ⇒ 安全边际量 2,000 件、安全边际率 25.00%；息税前利润 = 480,000 − 280,000 − 150,000 = 50,000；经营杠杆系数 = 贡献边际 200,000 ÷ 50,000 = **4.00**（一步相除）。默认组（100,000 / 50 / 30 ⇒ 400,000 / 利润 160,000 / DOL 1.50）不命中。",
  },
  {
    slug: "finance/discount-calculator",
    inputs: { price: "250" },
    clicks: ["discounts=[0.7];calc()"],
    expect: ["¥ 175.00", "7.00 折"],
    ref: "叠加折扣链（原价 250 元；折扣链是页面私有数组 `discounts`，经 clicks 直接置为 [0.7] 再调 calc()）：折后价 = 250×0.7 = **¥ 175.00**，综合折扣率 30.0%，相当于 **7.00 折**。该页折扣输入框是 `renderDiscountChain()` 运行期生成的**无 id 输入框**（oninput 指向 `updateDiscount(i, this.value)`）⇒ `inputs` 注入不到，必须用 clicks 改写页面级数组。首轮试过 `discounts=[0.8]`，恰好等于该页默认折扣 ⇒ 默认态也命中（逃生项），改 0.7 后才有判别力。默认组不命中。",
  },
  {
    slug: "finance/mortgage-calculator",
    inputs: { loanAmount: "300", rate: "5.2", downPayment: "100" },
    clicks: ["calculate()"],
    expect: ["¥43,889.00", "¥13,000.00"],
    ref: "商业贷款月供（贷款额 300 万、年利率 5.2%、首付 100 万，年限取页面默认）：首月利息 = 余额 3,000,000×5.2%/12 = **¥13,000.00**（一步相乘）；月供 56,889.00 ⇒ 首月本金部分 = 56,889.00 − 13,000.00 = **¥43,889.00**（一步相减），尾列剩余余额 2,956,111.00 与之自洽。锚取「先算利息、再由月供反推本金」两行，**回避了需要迭代求解的月供公式本身**，因此 ref 里每个数字都能手算复核。默认组（100 万 / 4.2% / 30 年）不命中。",
  },
  {
    slug: "finance/points-redemption-value",
    inputs: { pts: "20000", val: "25", fee: "0" },
    clicks: ["calcTool()"],
    expect: ["12.50 每万分兑换价值（元）", "0.13 每 100 分兑换价值（元）"],
    ref: "积分兑换价值（积分 20,000 个、标价 25 元、加钱 0 元）：每万分兑换价值 = 25 ÷ (20,000/10,000) = **12.50 元**；每 100 分兑换价值 = 12.50/100 = **0.13 元**（同一数值换百分之一口径，同源只差一个百分数）。默认组（10,000 分 / 20 元 ⇒ 20.00 / 0.20）不命中。",
  },
  {
    slug: "finance/salary-calculator",
    inputs: { baseSalary: "40000", pensionRate: "8", medicalRate: "2", unemploymentRate: "0.5", housingRate: "12", housingBase: "40000" },
    clicks: ["calculate()"],
    expect: ["¥9,000.00", "¥4,800.00"],
    ref: "薪资五险一金（缴费基数 40,000：养老 8% / 医疗 2% / 失业 0.5% / 公积金 12%，工伤与生育默认 0）：公积金 = 40,000×12% = **¥4,800.00**（一步相乘）；五险一金合计 = 40,000×(8%+2%+0.5%+0+0+12%) = 40,000×22.5% = **¥9,000.00**（一条式）。同页个税按起征额 36,000 元与超额累进表计算，与本两项自洽。默认基数 20,000 ⇒ 2,400 / 4,500，不命中。",
  },

  // ---- BATCH263：finance 分类「卡号 Luhn 反例 / 免息天数 / 夏普比率 / IRR」收口族（4 例） ----
  {
    slug: "finance/credit-card-validator",
    inputs: { cardInput: "4532015112830360" },
    clicks: ["validate()"],
    expect: ["Luhn 校验： ❌ 未通过", "❌ Luhn 校验失败，卡号无效"],
    ref: "卡号校验**反例**（Visa 号 4532 0151 1283 0360，末位把原校验位 6 改成 0）：页面输出「卡号格式化： 4532 0151 1283 0360 / 卡组织识别： Visa / 长度校验： ✅ 当前 16 位」但「Luhn 校验： ❌ 未通过」。本页默认态卡号为空 ⇒ 只显示「请在上方输入卡号以开始校验」，绝不可能出现否定结论 ⇒ 这是一条**零成本的廉价判别**。与既有 `credit-card-luhn` 正例（4532015112830366 通过）互为镜像。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "8000", dailyRate: "0.05", billDay: "2", dueDay: "20", minRatio: "10", lateFeeRatio: "5", repayType: "full" },
    clicks: ["calc()"],
    expect: ["38 免息天数"],
    ref: "信用卡免息期天数（账单日 2 号、还款日 20 号）：因 dueDay > billDay ⇒ 免息天数 = (还款日 − 账单日) + 20 = 20 − 2 + 20 = **38 天**，再经 `min(max(x,20),56)` 裁剪后仍为 38。刻意避开默认组（账单日 10 / 还款日 30 ⇒ 40 天）—— 首轮按默认值注入时该行恒为 40、默认态也命中 ⇒ 判逃生项，改账单日/还款日后才有判别力。全额还款 ⇒ 循环利息 0.00、应还 8,000.00 与「免息期内无息」自洽。",
  },
  {
    slug: "finance/sharpe-ratio",
    inputs: { portReturn: "14", portStd: "20", riskFree: "2" },
    clicks: ["currentTab='inputs'; calc()"],
    expect: ["夏普比率 = 12.000 ÷ 20.000 = 0.6000", "超额收益 = 14.000 - 2.00 = 12.000%"],
    ref: "夏普比率（组合收益率 14%、标准差 20%、无风险利率 2%）：超额收益 = 14.000 − 2.00 = **12.000%**；夏普比率 = 12.000 ÷ 20.000 = **0.6000**。页面把两个中间式都印在明细区 ⇒ 两条 expect 各自都是一步相除/相减。注意该页 `calc()` 依赖 `currentTab`：harness 内 `oninput` 触发的 `switchTab` 会抛 `charAt` of undefined ⇒ 必须在 clicks 里先 `currentTab='inputs'` 再调 `calc()`，否则结果区停在默认态。默认组（8 / 12 / 3 ⇒ 0.4167）不命中。",
  },
  {
    slug: "finance/irr-calculator",
    inputs: { discountRate: "8" },
    clicks: ["cashFlows=[{period:0,amount:-10000,label:'初始'},{period:1,amount:11000,label:'收益'}]; calc()"],
    expect: ["10.00%"],
    ref: "内部收益率（一次性投入 −10,000、一年后收回 11,000，贴现率 8%）：IRR 是方程 −10,000 + 11,000/(1+r) = 0 的解 ⇒ 1+r = 11,000/10,000 ⇒ **IRR = 10.00%**，页面 `irrValue` 直接显示该值，并据此把字体染绿（IRR ≥ 贴现率）。该页现金流表由页面私有数组 `cashFlows` 驱动、`inputs` 注入不到 ⇒ 用 clicks 直接赋数组（必须带 `label` 字段，否则 `updateLabel` 会抛错）再调 `calc()`。默认态 `cashFlows` 为空 ⇒ 输出 `--`，不命中。",
  },

  // ---- BATCH264：finance 分类「发票生成器 single/split/combine/reverse 四路径」族（4 例） ----
  {
    slug: "finance/invoice-generator",
    inputs: { "s-total": "20000", customTax: "13" },
    clicks: ["calc()"],
    expect: ["¥17,699.12", "= 20,000.00 ÷ 1.13 = ¥17,699.12"],
    ref: "单一模式（价税分离）：不含税 = 价税合计 ÷ (1 + 13%) = 20,000 ÷ 1.13 = **17,699.12**，页面公式行原样回显该算式，两条同源不同式（一条是结果、一条是算式）。默认组（10,000 / 9%）⇒ 不含税 9,174.31，且公式行写的是 ÷ 1.09，两条都不命中。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "sp-total": "25000", "sp-limit": "5000", "sp-type": "excl" },
    clicks: ["currentMethod='split'; calc()"],
    expect: ["5 张发票", "¥2,250.00"],
    ref: "拆分模式（金额字段按不含税口径）：张数 = ceil(25,000 ÷ 5,000) = **5 张**，每张不含税 5,000、税额 = 5,000 × 9% = 450 ⇒ 税额合计 = 450 × 5 = **2,250.00**、价税合计 = (5,000+450) × 5 = **27,250.00**。刻意注入 sp-type=excl 让税额由 450×5 一次乘得（默认第一个选项 total 口径下 sumExcl 与 sumTax 是除不尽的循环小数，不好复算）；默认组（100,000 / 10,000）⇒ 10 张，不命中。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "cb-amt1": "5000", "cb-amt2": "3000", "cb-amt3": "1000", "cb-amt4": "0", "cb-target": "9001" },
    clicks: ["currentMethod='combine'; calc()"],
    expect: ["凑整金额： ¥9,000.00", "差额： ¥1.000000 ⚠️ 超出允许范围"],
    ref: "凑整模式：目标 9,001 元，面额 5,000 / 3,000 / 1,000（4 号面额填 0 被过滤），搜索器先命中 1,000 × 9 = **9,000** 这条零成本组合 ⇒ 凑整金额 **9,000**、差额 = |9,000 − 9,001| = **1.000000**，大于容差 0.01 ⇒ 判定「⚠️ 超出允许范围」。锚不碰「目标金额 9,001.00」（那是输入回显），只锚与 target 不同的派生行。默认组（目标 50,000）的差额为 0 ⇒ 命中的是同位置的 ✅ 分支，不命中本条。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "rv-total": "20000", "rv-tax": "1600" },
    clicks: ["currentMethod='reverse'; calc()"],
    expect: ["反推税率： 8.6957%", "= 1,600.00 ÷ 18,400.00 × 100% = 8.6957%"],
    ref: "反推模式：不含税 = 20,000 − 1,600 = **18,400**，税率 = 1,600 ÷ 18,400 × 100% = **8.6957%**，公式行把除数与被除数一并回显 ⇒ 可完全手算复核。默认组（10,000 / 825.69）⇒ 税率 9.0000%，两条都不同。",
  },

  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "36", dt_expense: "22", dt_debt: "120", dt_existing: "25" },
    clicks: ["switchMethod('dual-ten'); calc()"],
    expect: ["455万", "180 万保额", "360万 (年收入×10)"],
    ref: "双十法则非默认组（年收入 36 万、负债 120 万、存量保障 25 万）：寿险保额 = max(年收入×10 + 负债 − 存量, 0) = 360 + 120 − 25 = **455 万**；重疾 = max(年收入×5, 30) = 180 万；意外 = 年收入×10 = 360 万；年保费预算 = 年收入×10% = 3.6 万。三条 expect 分别锚在 stat 卡、险种配置条、明细拆解行上，同源不同式，可一步复核。默认组（年收入 20 / 负债 80 / 存量 10）⇒ 270 / 100 / 200 万，三条都不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "10", dt_expense: "8", dt_debt: "0", dt_existing: "200" },
    clicks: ["switchMethod('dual-ten'); calc()"],
    expect: ["50 万保额", "1.0万", "100万 (年收入×10)"],
    ref: "存量保障金反超需求：年收入×10 + 负债 = 100 + 0 < 存量 200 ⇒ 寿险保额 = max(…, 0) = 0 万；同组重疾 = max(10×5, 30) = 50 万、年保费预算 = 10×10% = 1.0 万。刻意不锚任何「0 万 / 0 万保额」串：harness 兜底阶段会以 switchMethod(undefined) 重跑 calc()，currentMethod 落空 ⇒ 四个保额量全部取初值 0 并写回结果区，该串在默认态 likewise 命中 ⇒ 逃生项。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { ft_income: "45", ft_members: "5" },
    clicks: ["switchMethod('four-three'); calc()"],
    expect: ["450万", "4.5万", "投资比例 18.0万"],
    ref: "4321 法则（年收入 45 万、家庭 5 人）：人均可支配 = 45 ÷ 5 = 9 万，重疾 = max(9×3, 30) = 30 万；寿险 = max(年收入×10, 50) = 450 万；年保费预算 = 45×10% = 4.5 万；投资 = 45×40% = 18.0 万/年、生活 13.5、储蓄 9.0。默认组（20 万 / 3 人）⇒ 200 / 2.0 / 8.0 万，三条都不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { lv_age: "35", lv_retire: "65", lv_income: "30", lv_growth: "5", lv_consume: "40", lv_discount: "6" },
    clicks: ["switchMethod('life-value'); calc()"],
    expect: ["446万", "工作年限 30年", "年净贡献 18.0万"],
    ref: "生命价值法（现年 35、退休 65、年收入 30 万、收入增长 5%、个人消费 40%、贴现率 6%）：工作年限 = 65 − 35 = 30 年（页面取 Math.max(差, 1) 下限，此处不触底）；年净贡献 = 30 × (1 − 40%) = 18.0 万；生命价值 = Σ_{i=0..29} 18 × 1.05^i ÷ 1.06^{i+1}，python 独立复算 = **446 万**（取整后写回）。默认组（30 / 60 / 20 / 3% / 30% / 5%）⇒ 另一组值，三条都不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { nd_income: "25", nd_expense: "15", nd_mortgage: "150", nd_other_debt: "20", nd_education: "60", nd_parents: "40", nd_final: "15", nd_assets: "30", nd_spouse_income: "12", nd_years: "15" },
    clicks: ["switchMethod('needs'); calc()"],
    expect: ["生活支出缺口 45万", "家庭负债 170万", "300 万保额"],
    ref: "需求分析法：家庭负债 = 房贷 150 + 其他负债 20 = 170 万；生活支出缺口 = max((家庭开支 15 − 配偶收入 12) × 保障年限 15, 0) = 3 × 15 = 45 万；寿险保额 = max(170 + 教育 60 + 赡养 40 + 身后费用 15 + 缺口 45 − 已有资产 30, 0) = **300 万**。默认组（20 / 12 / 80 / 10 / 50 / 30 / 10 / 20 / 10 / 20）⇒ 负债 90、缺口 40、保额 200，三条都不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { nd_income: "20", nd_expense: "12", nd_mortgage: "80", nd_other_debt: "10", nd_education: "50", nd_parents: "30", nd_final: "10", nd_assets: "500", nd_spouse_income: "10", nd_years: "20" },
    clicks: ["switchMethod('needs'); calc()"],
    expect: ["子女教育 50万", "生活支出缺口 40万", "赡养父母 30万"],
    ref: "需求分析法反向上界：已有资产 500 万足以覆盖全部缺口（负债 90 + 教育 50 + 赡养 30 + 身后 10 + 缺口 (12−10)×20 = 40，合计 220 万）⇒ 寿险保额 = max(220 − 500, 0) = 0 万，但三项费用明细仍各自独立成立（50 / 40 / 30 万），可验证「保额归零 ≠ 明细被抹平」。锚全部取自明细行，不碰任何含 0 的输出。默认组（资产 20 万）⇒ 保额 200、缺口 40，明细行仍是默认口径但「子女教育 50万」等同串在双十/4321 默认组不存在（默认组根本没有这三行 ⇒ 不命中）。",
  },

  // ── 零用例加固（2026-10-06）──────────────────────────
  {
    slug: "finance/analysis-cost-1",
    inputs: { total: "250000", dec: "3" },
    expect: ["综合单位成本 = 250,000.000 ÷ 5,000.000 = 50.000 元 / 件", "250.000分摊率（元 / 单位基数）", "50.000综合单位成本（元 / 件）"],
    ref: "注入非默认(默认 total=120000/dec=2)：作业成本分配法 分摊额 = 250,000；分摊率 = 250,000 ÷ Σ基数 1,000 = 250.000 元/单位基数；综合单位成本 = 50.000 元/件。默认态 24.00（120,000 ÷ 5,000），三条均不命中。",
  },

  // ── 零用例加固（2026-10-09）──────────────────────────
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "50" },
    expect: ["6.8966"],
    ref: "静态汇率表 USD=1、CNY=7.25；50 元 CNY→USD = 50/7.25 = 6.8966。锚点避开了「始终存在的速查表」里的 362.50（USD 50→362.50 CNY，注入失败也命中 ⇒ 假逃生项），改用随注入量变化的 6.8966。默认 fromAmount=100 → 13.7931，不命中。",
  },
  {
    slug: "finance/text-reverse-words",
    inputs: { input: "Hello World", mode: "allchar" },
    expect: ["dlroW olleH"],
    ref: "按 allchar 模式整体反转：Hello World → dlroW olleH。默认态（mode=space、输入为「Hello World ToolBox/中文」两行）按词反转，输出不含 dlroW olleH ⇒ 不命中。",
  },
  {
    slug: "finance/futures-pnl-calculator",
    inputs: { openPrice: "4000", closePrice: "4200", lots: "2", marginRate: "10", openFee: "25", closeFee: "35" },
    expect: ["119,880.00", "240,000.00"],
    ref: "沪深300乘数 300、做多：盈亏点数=(4200−4000)×1=200；盈亏=200×300×2=120,000；手续费=(25+35)×2=120 ⇒ 净盈亏 119,880.00；合约价值=4000×300×2=2,400,000；保证金=2,400,000×10%=240,000.00。默认态(3500/3550/1/12/30/30)→净额 14,940.00、保证金 126,000.00，两条均不命中。",
  },
  {
    slug: "finance/gst-validator",
    inputs: { input: "27AAPFU0939F1ZV" },
    expect: ["✅ GST 号码有效"],
    ref: "修复前 gstChecksum 用 const factor 却在循环里重赋值 ⇒ 所有浏览器都抛「Assignment to constant variable」整页失效；已改为 let。该号前 14 位 mod-36 校验位 = V 与末位一致 ⇒ 有效。默认态输入为空 → 「等待输入...」，不命中。",
  },
];

// ---------------------------------------------------------------- main
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== finance calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();