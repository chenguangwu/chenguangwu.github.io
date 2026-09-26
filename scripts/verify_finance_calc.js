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