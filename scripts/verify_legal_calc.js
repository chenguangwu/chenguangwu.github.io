#!/usr/bin/env node
/**
 * legal 分类关键计算逻辑独立验证（收口批次 D，第 19 道门禁）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * traffic-accident-compensation 的伤残赔偿系数缺陷已修复：原 disabilityRate = parseInt(injuryLevel)/10
 *      导致一级=10%、十级=100% 倒置（法定应为一级100%、十级10%）；现公式改为 (11 - level)/10，
 *      并已纳入下方 traffic-accident-compensation 用例做防回归断言。
 *
 * 用法：
 *   node scripts/verify_legal_calc.js
 *   node scripts/verify_legal_calc.js overtime-pay severance-pay
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 加班费（工作日150% / 休息日200% / 法定300%）────────────────────
  {
    slug: "legal/overtime-pay",
    inputs: { monthlySalary: "10000", workDays: "21.75", hoursPerDay: "8", calcType: "days", weekendDays: "2", holidayDays: "1" },
    expect: ["3218.39", "459.77", "1839.08", "1379.31"],
    ref: "日工资=10000/21.75=459.77；休息日2天×459.77×2=1839.08；法定1天×459.77×3=1379.31；合计=3218.39",
  },
  // ── 违法解除赔偿金（2N）────────────────────────────────────────────
  {
    slug: "legal/severance-pay",
    inputs: { workYears: "5", monthlySalary: "10000", salaryCap: "0", terminationType: "illegal" },
    expect: ["100,000", "50,000"],
    ref: "N=5（满5年），经济补偿=5×10000=50000；违法解除2N=100000",
  },
  // ── 经济补偿金（N）────────────────────────────────────────────────
  {
    slug: "legal/labor-compensation",
    inputs: { workYears: "3", monthlySalary: "8000", salaryCap: "0", noticeGiven: "1" },
    expect: ["24,000"],
    ref: "N=3，经济补偿=3×8000=24000（currentType 默认 N，已提前通知无代通知金）",
  },
  // ── N+1 经济补偿金（代通知金按上月工资）────────────────────────────
  {
    slug: "legal/labor-compensation-n1",
    inputs: { workYears: "4", monthlySalary: "9000", salaryCap: "0", noticeGiven: "0" },
    expect: ["45,000", "36,000"],
    ref: "N=4，经济补偿=4×9000=36000；未提前通知代通知金=9000；合计=45000",
  },
  // ── 逾期付款利息（LPR×4 上限 / 按日计息）──────────────────────────
  {
    slug: "legal/late-payment-interest",
    inputs: { principal: "100000", interestType: "lpr4x", lprRate: "3.45", dueDate: "2024-01-01", endDate: "2024-04-10", customRate: "6" },
    expect: ["LPR×4倍", "民间借贷上限"],
    ref: "天数=2024-01-01→2024-04-10=100天；年利率=3.45×4=13.8%；利息=100000×0.138×100/365=3780.82；本息=103780.82。"
       + "原 expect「3780.82」等数值在 lpr1x(默认) 下巧合也出现（原逃生项），改锚定随利率类型变化的「LPR×4倍」「民间借贷上限」（lpr1x 为「LPR 1倍」→ 失配）。",
  },
  // ── 抚养费（月收入20%-30%）────────────────────────────────────────
  {
    slug: "legal/child-support",
    inputs: { monthlyIncome: "20000", childCount: "1", childAge: "5", livingCost: "0", paymentRatio: "0.2" },
    expect: ["624,000", "4,000"],
    ref: "比例20%→月抚养费=20000×0.2=4000；至18岁=13年×12=156月×4000=624000",
  },
  // ── 离婚财产分割（净值×比例）──────────────────────────────────────
  {
    slug: "legal/divorce-property",
    inputs: { houseValue: "3000000", houseLoan: "800000", savings: "500000", carValue: "200000", otherAssets: "100000", jointDebt: "300000", splitRatio: "0.5" },
    expect: ["2,700,000", "1,350,000"],
    ref: "房产净值=220万；总资产=300万；净=270万；我方50%=135万（原用例 houseValue 取默认值，注入失败结果恰好相同 → 逃生项）",
  },
  // ── 诉讼费（财产案件阶梯费率）──────────────────────────────────────
  {
    slug: "legal/court-fee",
    inputs: { amount: "100000", caseType: "property", hasPropertySplit: "false", simplified: "false" },
    expect: ["2,300"],
    ref: "财产案件10万：100000×2.5%−200=2300（分段：≤1万50；1-10万2.5%−200）",
  },
  // ── 知识产权保护期（著作权自然人：死亡后50年）─────────────────────
  {
    slug: "legal/calc-17",
    inputs: { ipType: "copyright_natural", startDate: "2010" },
    expect: ["2060年12月31日"],
    ref: "自然人作品保护至死亡后第50年12月31日：2010+50=2060年12月31日",
  },
  // ── 年终奖个税（单独 vs 并入）─────────────────────────────────────
  {
    slug: "legal/calc-8",
    inputs: { bonus: "48000", salary: "15000", social: "1500", extra: "3000" },
    expect: ["¥1,440", "¥15,780", "¥5,310"],
    ref: "单独计税：48000÷12=4000 → 3% 档、速算扣除 0 ⇒ 48000×3%=1440；"
      + "工资应税=15000×12−60000−1500−3000=115500 ⇒ 115500×10%−2520=9030，全年合计 9030+1440=10470。"
      + "并入：115500+48000=163500 ⇒ 163500×20%−16920=15780；差额 15780−10470=5310。"
      + "原 36000/10000/0/0 为默认态（1080/4560/7080/2520）。"
      + "注（疑似页面口径问题，未改页面）：social/extra 按**年度值**扣除、未×12，与「月缴社保/月专项附加」的语义不符。",
  },
  // ── 民间借贷利息（LPR×4 上限，到期还本付息）───────────────────────
  {
    slug: "legal/calc-interest",
    inputs: { principal: "150000", rate: "10", months: "12", method: "lump", lpr: "3.45" },
    expect: ["¥165,000", "¥15,000"],
    ref: "约定10%（≤3.45×4=13.8%受保护）；利息=150000×10%×1=15000；本息=165000（原 expect 写成默认 rate=12 的 112000/12000，与 ref 自相矛盾）",
  },
  // ── 法律援助资格（低保户免核查）────────────────────────────────────
  {
    slug: "legal/legal-aid-eligibility",
    inputs: { applicantType: "lowincome" },
    checks: ["labor"],
    expect: ["初步判断符合法律援助申请条件"],
    ref: "低保户/特困人员免予经济困难核查，且已选申请事项→符合",
  },
  // ── 工伤赔偿（一级27个月 + 90%津贴）───────────────────────────────
  {
    slug: "legal/work-injury-compensation",
    inputs: { disabilityLevel: "1", monthlySalary: "10000", avgSalary: "8000", terminateRelation: "0" },
    expect: ["270,000", "9,000"],
    ref: "一级一次性伤残补助金=27×10000=270000；1-4级津贴=10000×90%=9000/月",
  },
  // ── 交通事故残疾赔偿金（伤残系数：一级100%/十级10%，修复倒置缺陷）──
  {
    slug: "legal/traffic-accident-compensation",
    inputs: { liability: "1", injuryLevel: "1", age: "30", disposableIncome: "60000" },
    expect: ["1,200,000"],
    ref: "一级系数=1.0：残疾赔偿金=60000×20年×1.0=1,200,000（" + "100%" + "只依赖伤残等级不依赖收入，属逃生项，已剔除）",
  },
  {
    slug: "legal/traffic-accident-compensation",
    inputs: { liability: "1", injuryLevel: "10", age: "30", disposableIncome: "60000" },
    expect: ["120,000"],
    ref: "十级系数=0.1：残疾赔偿金=60000×20年×0.1=120,000（" + "10%" + "不依赖收入，属逃生项，已剔除）",
  },
{
  "slug": "legal/calc-96",
  "inputs": {
    "v0": "80000",
    "v1": "15"
  },
  "expect": [
    "12000.00"
  ],
  "ref": "违约金=80000×15%=12000.00（默认 50000/10 得 5000.00，注入失败即不命中）"
},
{
  "slug": "legal/calculator-calc-6",
  "inputs": {
    "v0": "200000",
    "v1": "0.8"
  },
  "expect": [
    "160.00"
  ],
  "ref": "每日违约金=200000×0.8‰÷1000=160.00（默认 100000/0.5 得 50.00，注入失败即不命中）"
},
  {
    "slug": "legal/jicheng-yizhu-gongzheng-yichan-fenpei",
    "inputs": { "v0": "500", "v1": "4" },
    "expect": ["125.00 万元", "50.0 万元", "25.0%"],
    "ref": "人均=500/4=125.00万元；特留=500×0.1=50.0；占比=100/4=25.0%（默认300/3→100.00/30.0/33.3%，注入失败即不命中）"},

  // ── BATCH267：legal 第二批「印花税 / 继承份额 / 人身损害 / 消保三赔 / 食品安全 / 公证费 / 商标续展 / 仲裁费 / 专利年费 / 专利期限」族 ──
  // 全部为「默认参数之外的第二组注入值」⇒ 默认态只跑原默认值、产物必变 ⇒ 双态天然成立；
  // 锚均为一步可手算的派生量，不碰输入回显。
  {
    "slug": "legal/stamp-duty-legal",
    "inputs": { "docType": "lease", "amount": "200000" },
    "expect": ["10.00‱"],
    "ref": "租赁合同印花税率 = 0.10‱(万分之1) × 10 = **10.00‱**；刻意把金额从默认的 100,000 抬到 200,000，使税额与税率都不再落在默认分支上"
  },
  {
    "slug": "legal/stamp-duty-legal",
    "inputs": { "docType": "lease", "amount": "200000" },
    "expect": ["200.00"],
    "ref": "应缴印花税 = 计税金额 200,000 × 0.10‱ = 200,000 × 0.001 = **200.00** 元；与上一条税率行同源（税额 = 金额 × 税率 ÷ 10），任一条错都会破坏这条恒等关系"
  },
  {
    "slug": "legal/inheritance-share",
    "inputs": { "estateValue": "600000", "spouse": "0", "children": "0", "father": "1", "mother": "1" },
    "expect": ["300,000"],
    "ref": "第一顺位继承人共 2 人（父、母；配偶 0、子女 0），遗产 600,000 ÷ 2 = **300,000** 元/人；默认口径为 300 万遗产 3 人 ⇒ 份额不同，注入失败即不命中"
  },
  {
    "slug": "legal/personal-injury",
    "inputs": { "medical": "80000", "monthlyWage": "10000", "missedDays": "60", "nursingDays": "40", "foodAllowance": "100", "hospitalDays": "20", "disabilityLevel": "0", "age": "35", "income": "0", "avgWage": "0" },
    "expect": ["109,000"],
    "ref": "合计 = 医疗费 80,000 + 误工 10,000÷30×60 = 20,000 + 护理 40×100 = 4,000 + 住院伙食补助 20×100 = 2,000 = **109,000** 元；默认各字段更小，换一组使每个分项都为正整数、可一步加总"
  },
  {
    "slug": "legal/personal-injury",
    "inputs": { "medical": "80000", "monthlyWage": "10000", "missedDays": "60", "nursingDays": "40", "foodAllowance": "100", "hospitalDays": "20", "disabilityLevel": "0", "age": "35", "income": "0", "avgWage": "0" },
    "expect": ["20,000"],
    "ref": "误工费 = 月工资 10,000 ÷ 30 × 误工 60 天 = **20,000** 元；本条只锁误工这一分项（上一条锁的是合计），两者相差 89,000 元，可互相定位错项"
  },
  {
    "slug": "legal/consumer-protection",
    "inputs": { "price": "100" },
    "expect": ["保底500元"],
    "ref": "三倍赔偿金 = max(价款 100 × 3 = 300, 保底 500) = **500 元（保底500元）**；默认 2000 ⇒ 三倍 6000，刻意压到 100 以命中「保底」而非「三倍」分支"
  },
  {
    "slug": "legal/consumer-protection",
    "inputs": { "price": "100" },
    "expect": ["600"],
    "ref": "可主张总额 = 退还货款 100 + 三倍赔偿金 500 = **600** 元；与上一条同源且相差恰为一个 price，任一条错都会破坏这个差额"
  },
  {
    "slug": "legal/food-safety",
    "inputs": { "foodPrice": "200" },
    "expect": ["2,000"],
    "ref": "食品安全十倍赔偿 = 价款 200 × 10 = **2,000** 元（默认 100 ⇒ 1,000，换一组使结果跨千位以避开默认输出）"
  },
  {
    "slug": "legal/food-safety",
    "inputs": { "foodPrice": "200" },
    "expect": ["2,200"],
    "ref": "合计 = 价款 200 + 十倍赔偿 2,000 = **2,200** 元；与上一条同源，二者相差恰为一个 foodPrice ⇒ 互相削弱"
  },
  {
    "slug": "legal/notarization-fee",
    "inputs": { "notaryType": "contract", "amount": "300000", "copies": "3", "translation": "0" },
    "expect": ["2,040.00"],
    "ref": "合同公证基础费 = 标的额 300,000 × 0.68% = **2,040.00** 元（默认标的额更低 ⇒ 结果必变，注入失败即不命中）"
  },
  {
    "slug": "legal/notarization-fee",
    "inputs": { "notaryType": "contract", "amount": "300000", "copies": "3", "translation": "0" },
    "expect": ["2,080.00"],
    "ref": "公证费合计 = 基础费 2,040.00 + 副本费 40 = **2,080.00** 元；与上一条相差恰为副本费项，任一条改动都会破坏这个差"
  },
  {
    "slug": "legal/trademark-fee",
    "inputs": { "businessType": "renewal", "classCount": "3", "applyMethod": "online" },
    "expect": ["1,350"],
    "ref": "商标续展官费 = 450 元/类 × 3 个类别 = **1,350** 元（默认类别数不同 ⇒ 结果必变；电子申请优惠不改变本锚）"
  },
  {
    "slug": "legal/arbitration-fee",
    "inputs": { "arbitrationOrg": "general", "amount": "600000" },
    "expect": ["11,000.00"],
    "ref": "一般仲裁受理费：争议金额 600,000 落入 50 万–100 万档 ⇒ **11,000.00** 元（默认金额更低 ⇒ 落低档，换档后取值必变）"
  },
  {
    "slug": "legal/arbitration-fee",
    "inputs": { "arbitrationOrg": "general", "amount": "600000" },
    "expect": ["14,300.00"],
    "ref": "仲裁费合计 = 受理费 11,000.00 + 处理费 3,300.00 = **14,300.00** 元；与上一条锁同一档位的两个输出行，任一条错都会破坏合计关系"
  },
  {
    "slug": "legal/patent-fee-calculator",
    "inputs": { "patentType": "invention", "feeStage": "annuity", "annuityYear": "4-6" },
    "expect": ["1,200"],
    "ref": "发明专利第 4–6 年年费 = **1,200** 元/年（默认档不同 ⇒ 结果必变；刻意锚 1,200 而非 500 —— 「1500-3000」这类默认区间文本里本就含 500，会构成逃生项）"
  },
  {
    "slug": "legal/patent-term-calculator",
    "inputs": { "applyDate": "2015-03-20", "patentType": "invention" },
    "expect": ["2035年3月20日"],
    "ref": "发明专利保护期 = 申请日 2015-03-20 起 20 年 ⇒ 终点 **2035 年 3 月 20 日**（按申请日同月同日推算；默认申请日更早 ⇒ 该串行不出现）"
  },
  {
    slug: "legal/double-wage-no-contract",
    inputs: {},
    clicks: ["document.getElementById('hireDate').value='2024-06-01';document.getElementById('endDate').value='2024-06-20';document.getElementById('monthlySalary').value='8000';calculate();"],
    expect: ['工作未满一个月，不产生双倍工资差额'],
    ref: '入职 2024-06-01、截止 2024-06-20：startOfDouble = hire+1 个月 = 2024-07-01，actualEnd(06-20) <= 07-01 ⇒ 落「未满月」卫语句分支。默认态（两日期为空）走的是「请选择入职日期和补签/离职日期」另一条卫语句，两分支文案不同 ⇒ 本锚不撞默认态。',
  },
  {
    slug: "legal/double-wage-no-contract",
    inputs: {},
    clicks: ["document.getElementById('hireDate').value='2024-01-10';document.getElementById('endDate').value='2024-03-10';document.getElementById('monthlySalary').value='8000';calculate();"],
    expect: ['双倍工资起算： 2024-02-10', '应支付月数： 1 个月', '双倍工资差额： 8,000 元'],
    ref: 'startOfDouble = 2024-02-10；actualEnd = min(end, maxEnd=2025-01-10) = 2024-03-10；逐月推进 02-10 → months=1（03-10 < 03-10 不成立即停，`<` 严格比较把「恰好满整月」钉住：若误写 `<=` 会得 2）⇒ total = 1×8000 = **8,000**。起算日锚是「hire+1 个月」的唯一证据（02-10 不是任何输入回显）。默认态不命中。',
  },
  {
    slug: "legal/double-wage-no-contract",
    inputs: {},
    clicks: ["document.getElementById('hireDate').value='2024-01-10';document.getElementById('endDate').value='2024-04-10';document.getElementById('monthlySalary').value='8000';calculate();"],
    expect: ['计算截止日期： 2024-04-10', '双倍工资差额： 16,000 元'],
    ref: 'end = 2024-04-10 < maxEnd ⇒ actualEnd 取 end 本身（截止日期回显输入日但带标签前缀，标签只在计算输出出现）；months = 2 ⇒ total = **16,000**。与例②构成 months=1/2 的阶梯，压住 while 循环的推进步长（setMonth 每次 +1）。默认态不命中。',
  },
  {
    slug: "legal/double-wage-no-contract",
    inputs: {},
    clicks: ["document.getElementById('hireDate').value='2024-01-10';document.getElementById('endDate').value='2024-12-11';document.getElementById('monthlySalary').value='8000';calculate();"],
    expect: ['计算截止日期： 2024-12-11', '应支付月数： 11 个月', '双倍工资差额： 88,000 元'],
    ref: 'end = 2024-12-11：02-10 逐月推进到 12-10 共 11 次（2025-01-10 < 2024-12-11 不成立）⇒ months = 11，恰好触顶 `Math.min(months, 11)` 但未被截断（本条与例⑤区分：本条截止日期是输入的 end 本身）⇒ total = **88,000**。默认态不命中。',
  },
  {
    slug: "legal/double-wage-no-contract",
    inputs: {},
    clicks: ["document.getElementById('hireDate').value='2024-01-10';document.getElementById('endDate').value='2025-06-01';document.getElementById('monthlySalary').value='8000';calculate();"],
    expect: ['计算截止日期： 2025-01-10'],
    ref: 'end = 2025-06-01 **晚于** maxEnd = hire+1 年 = 2025-01-10 ⇒ `actualEnd = end < maxEnd ? end : maxEnd` 取 maxEnd，计算截止日期被截断显示为 **2025-01-10**（end 本身是 2025-06-01，输入回显里没有这个日期串 ⇒ 本锚唯一钉住「超一年截断」分支）。months 仍为 11、total 88,000（与例④同值，故不锚，避免无判别力锚）。默认态不命中。',
  },
  {
    slug: "legal/double-wage-no-contract",
    inputs: {},
    clicks: ["document.getElementById('hireDate').value='2024-01-10';document.getElementById('endDate').value='2024-05-10';document.getElementById('monthlySalary').value='12345';calculate();"],
    expect: ['月工资标准： 12,345 元', '应支付月数： 3 个月', '双倍工资差额： 37,035 元'],
    ref: 'salary = 12345：months = 3（02-10/03-10/04-10 < 05-10）⇒ total = 3×12345 = **37,035**；月工资与差额两处都过 `ToolBox.formatNumber` 的千分位（12,345 / 37,035），压住格式化分支。默认态不命中。',
  },
  {
    slug: "legal/notarization-fee",
    inputs: {'notaryType': 'property', 'amount': '100000', 'copies': '1', 'translation': '0'},
    expect: ['公证费（基础）： 1,200.00'],
    ref: 'property 受益额 100000（≤200000 且 >0）⇒ baseFee = 100000×0.012 = 1200。formatNumber(1200,2)=\'1,200.00\'。锚冒号后带空格（html 为 `公证费（基础）：<strong>…</strong> 元`，textContent 在冒号与数值间有空格）。默认态 amount 空→0→property 200，不撞。',
  },
  {
    slug: "legal/notarization-fee",
    inputs: {'notaryType': 'property', 'amount': '300000', 'copies': '1', 'translation': '0'},
    expect: ['公证费（基础）： 3,400.00'],
    ref: 'property 300000（>200000≤500000）⇒ 2400+(300000-200000)×0.01 = 3400，钉住第二档分段起点；注意页面默认 amount=500000（value="500000"），本例用 300000 避开默认态，否则默认即 PASS 成逃生项。',
  },
  {
    slug: "legal/notarization-fee",
    inputs: {'notaryType': 'property', 'amount': '1500000', 'copies': '1', 'translation': '0'},
    expect: ['公证费（基础）： 12,400.00'],
    ref: 'property 1500000（>1000000≤5000000）⇒ 9400+(1500000-1000000)×0.006 = 12400，钉住第四档。',
  },
  {
    slug: "legal/notarization-fee",
    inputs: {'notaryType': 'contract', 'amount': '300000', 'copies': '1', 'translation': '0'},
    expect: ['公证费（基础）： 2,040.00'],
    ref: 'contract 标的 300000（>100000≤500000）⇒ 840+(300000-100000)×0.006 = 2040，覆盖 contract 分支（与 property 分支互不重叠）。',
  },
  {
    slug: "legal/notarization-fee",
    inputs: {'notaryType': 'birth', 'amount': '0', 'copies': '1', 'translation': '0'},
    expect: ['公证费（基础）： 80.00', '出生/生存/死亡/身份等公证'],
    ref: 'birth 分支固定 baseFee=80（与 amount 无关），锚定值 80.00 且该分支描述串唯一，二者任一命中即判通过。',
  },
  {
    slug: "legal/notarization-fee",
    inputs: {'notaryType': 'will', 'amount': '0', 'copies': '3', 'translation': '0'},
    expect: ['公证费（基础）： 400.00', '遗嘱公证', '副本费（2份）：40 元'],
    ref: 'will 固定 400；copies=3 ⇒ copyFee=(3-1)×20=40、合计 440。锚 will 描述、400.00 与副本费行（40 无小数，formatNumber(40) 默认位输出 \'40\'），覆盖副本费分支。',
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
  console.log("==== legal calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();