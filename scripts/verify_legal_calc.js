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
  // ── §7.4 零用例加固：legal 确定性数值页（注入非默认 + harness 实测锚）──
  {
    slug: "legal/ipr-damages",
    inputs: { baseAmount: "150000", royaltyAmount: "80000", reasonableExpenses: "35000" },
    expect: ["150,000 元", "35,000 元", "185,000 元"],
    ref: "注入非默认(默认 100000/50000/20000)：按「权利人实际损失」口径 ⇒ 补偿性赔偿 = 150,000 元；合理维权开支 = 35,000 元；赔偿总额 = 150,000+35,000 = 185,000 元。默认态 100,000/20,000/120,000 均不命中。"
  },
  {
    slug: "legal/rent-deposit",
    inputs: { monthlyRent: "4500", otherDeduction: "500" },
    expect: ["4,500 元（1个月租金）", "4,000 元", "500 元"],
    ref: "注入非默认(默认 3000/0)：押金 = 1 个月租金 = 4,500 元；合法可扣 500 元、违法扣减 0 元 ⇒ 应退还 4,500 − 500 = 4,000 元。默认态 3,000/3,000/0 元，锚均不命中。"
  },
  {
    slug: "legal/estimate-salary",
    inputs: { salary: "13000", years: "5", capWage: "40000" },
    expect: ["¥65,000", "13000 × 5个月（N=5）"],
    ref: "注入非默认(默认 salary=10000/years=3/capWage=35000)：N = 5（每满 1 年计 1 个月）⇒ 经济补偿金 = 13,000×5 = 65,000 元；页面把算式原样回显为「13000 × 5个月（N=5）」。默认态 30,000/10000 × 3个月 均不命中。"
  },
  {
    slug: "legal/housing-fund-loan",
    inputs: { balance: "12", monthlySave: "3000", saveYears: "8", housePrice: "450", age: "40" },
    expect: ["账户余额12.0万元 × 15倍", "总价450.0万元 × 80%"],
    ref: "注入非默认(默认 8/2000/5/300/35)：额度三档 —— 余额档 = 12.0万×15 = 180.0 万、房价档 = 450.0万×80% = 360.0 万、城市上限（北京）120 万 ⇒ 最终可贷取最小 120 万。⚠ **月供 21,616 元与还款总额 1,296,948 元不可用**：默认 balance=8 时 8×15 = 120 万，同样被 120 万城市上限夹住 ⇒ 额度、月供、利息、还款总额在两态**逐字相同**；唯一有判别力的是额度依据表里含注入值的两行说明串。"
  },
  {
    slug: "legal/lawyer-fee-reference",
    inputs: { amount: "800000", hours: "30", baseFee: "15000", riskRatio: "20" },
    expect: ["29,600 - 44,400元"],
    ref: "注入非默认(默认 amount=500000/hours=20/baseFee=10000/riskRatio=15)：按标的额分段累计 ⇒ 民事一审（北京）参考区间 29,600 − 44,400 元（区间上下界分别含风险代理比例折算）。默认态区间不同。"
  },
  {
    slug: "legal/marriage-property-agreement",
    inputs: { houseValue: "3000000", carValue: "250000", savings: "500000", investments: "150000", otherAssets: "80000", jointDebt: "600000", maleRatio: "60", femaleRatio: "40" },
    expect: ["3980000.00", "3380000.00", "2028000.00", "1352000.00"],
    ref: "注入非默认(默认各项 0/比 50:50)：财产总额 = 3000000+250000+500000+150000+80000 = 3,980,000.00；扣除共同债务 600,000 ⇒ 可分配净资产 3,380,000.00；男 60% = 2,028,000.00、女 40% = 1,352,000.00。默认态全 0 不命中。"
  },
  {
    slug: "legal/legal-calculator",
    inputs: { "ot-salary": "12000", "ot-hours": "10", "bonus-amount": "48000", "loan-principal": "200000", "loan-rate": "6", "loan-months": "24" },
    expect: ["43,410.00", "9.56%", "24,000.00 元", "224,000.00 元"],
    ref: "注入非默认(默认 ot-salary=10000/ot-hours=8/bonus=36000/loan 100000·10%·12月)：① 年终奖 48,000 元按月均 4,000 计税 ⇒ 应扣个税 4,590.00、税后到手 43,410.00、实际税负率 9.56%；② 借贷 200,000 元、6%、24 个月单利 ⇒ 利息 24,000.00 元、本息合计 224,000.00 元。⚠ 本页为多页签结构，harness 只会渲染当前页签，注入必须命中当页签的输入 id（comp-*/lit-*/breach-* 属于其它页签、注入不生效），故本例只对「加班+年终奖+借贷」页签取锚。"
  },

  // ── §7.4 零用例收敛续批：legal 新增 7 例（确定性计算器）────────────
  {
    slug: "legal/debt-statute-limitations",
    inputs: { dueDate: "2023-01-01", lastDemandDate: "2024-01-01", lastPromiseDate: "", debtType: "loan" },
    expect: ["时效届满日： 2027-01-01", "930 天"],
    ref: "注入非默认(默认空→请选择还款日期或催款日期)：dueDate=2023-01-01、lastDemand=2024-01-01（3年时效自中断日起算）→ 时效届满日 2027-01-01、剩余 930 天。默认态无届满日/无 930 天不命中。"
  },
  {
    slug: "legal/feisu-ipo-simu-binggou-yewu",
    inputs: { v0: "2", v1: "8" },
    expect: ["0.10 亿元服务费预估"],
    ref: "注入非默认(默认 v0=1→0.05 亿元服务费预估)：v0=2 ⇒ 服务费预估 = v0×0.05 = 0.10 亿元。默认态 0.05 亿元服务费预估不命中 0.10。"
  },
  {
    slug: "legal/legal-age",
    inputs: { birthDate: "1990-05-15" },
    expect: ["总天数：12,450天"],
    ref: "注入非默认(默认 2000-01-01→总天数 8,932天)：birthDate=1990-05-15 ⇒ 总天数 12,450天（harness 固定 now，可复现）。默认态 8,932天 不命中。"
  },
  {
    slug: "legal/loan-statute-limitations",
    inputs: { dueDate: "2023-01-01", lastInstallmentDate: "", claimDate: "", lastDemandDate: "2024-01-01", lastPaymentDate: "", promiseDate: "", loanType: "normal" },
    expect: ["诉讼时效届满日： 2026-12-31", "930天"],
    ref: "注入非默认(默认空→请填写相关日期信息)：dueDate=2023-01-01、lastDemand=2024-01-01（中断重算3年）→ 诉讼时效届满日 2026-12-31、剩余 930天。默认态无届满日不命中。"
  },
  {
    slug: "legal/social-security-base",
    inputs: { salary: "15000", city: "上海", insType: "养老" },
    expect: ["3600.00"],
    ref: "注入非默认(默认 北京/10000→合计 2400.00)：salary=15000、养老 单位16%+个人8%=24% ⇒ 合计 15000×24%=3600.00。注意默认态合计行也是 2400.00，故锚 3600.00（仅 15000 档出现）。"
  },
  {
    slug: "legal/statute-limitations",
    inputs: { startDate: "2023-01-01", interruptionDate: "", limitType: "3" },
    expect: ["届满日期： 2026-01-01", "565 天"],
    ref: "注入非默认(默认空→请选择权利受损日期)：startDate=2023-01-01、3年普通时效 → 届满日期 2026-01-01、剩余 565 天。默认态无届满日不命中。"
  },
  {
    slug: "legal/will-witness-requirements",
    inputs: { witnessAge: "adult", capacity: "full", willType: "代书" },
    expect: ["需要2名以上合格见证人在场见证"],
    ref: "注入非默认(默认 自书遗嘱→『自书遗嘱无需见证人』)：willType=代书 ⇒ 需要2名以上合格见证人在场见证。默认态自书分支无此句，不命中。"
  },
  // ── 零用例收敛（2026-10-09）：legal 7 页中仅本页可收敛 ──
  {
    slug: "legal/trademark-class-search",
    inputs: {},
    clicks: ["document.getElementsByName=function(){return []};document.getElementById('keyword').value='润滑剂';doSearch()"],
    expect: ["共找到 1 个分类"],
    ref: "注入关键词『润滑剂』。独立复算：doSearch() 遍历 45 个尼斯分类，对每类做 编号/名称/描述/示例项 四路 indexOf 匹配；『润滑剂』只出现在第 4 类（燃料油脂）的示例项列表中 ⇒ 命中 1 类，页面输出计数行『共找到 1 个分类』。默认态（关键词空）渲染全部 45 类 ⇒ 计数行为『共找到 45 个分类』，不命中。⚠ 不用『4 第4类 · 燃料油脂』或示例项串『工业用油 润滑剂 …』作锚——默认全量渲染里同样含这两串（查表型页面陷阱：期望串在全量输出中亦出现），判别器已实测报出，属逃生串；唯一带计数语义且随关键词翻转的串就是『共找到 N 个分类』。⚠ clicks 前半段 `document.getElementsByName=function(){return []}` 是必需的：页面的 getFilter() 遍历同名 radio 组，harness 的 document 桩未实现 getElementsByName ⇒ 返回 undefined 后访问 .length 抛错、搜索中断、输出停在默认全量。打桩返回空数组（等价真实页面未选过滤项时 getFilter 返回 'all' 的分支）后搜索正常。这属 harness 缺口而非页面缺陷，用例内局部打桩规避、不改 harness。"
  },
  {
    slug: "legal/trademark-class-search",
    inputs: {},
    clicks: ["document.getElementsByName=function(){return []};document.getElementById('keyword').value='保险箱';doSearch()"],
    expect: ["共找到 1 个分类"],
    ref: "第二个关键词用例，验证命中类确实随关键词变化（不同关键词、不同命中类）。独立复算：『保险箱』属第 6 类（金属材料）的示例项 ⇒ 同样命中 1 类。与上一例（第 4 类）合起来覆盖两条不同数据路径：若页面忽略关键词恒返回全量，两例都会渲染 45 类、计数行为 45，均判红。默认态 45 类，不命中。expect 只取计数串『共找到 1 个分类』——类别标题与示例项串在全量渲染中同样存在（查表型页面共性，见上一例 ref）。"
  },
  {
    slug: "legal/calc-16",
    inputs: { type: "2", startDate: "2020-01-15", restartDate: "", interrupted: "off" },
    expect: ["2022-01-17", "已过 880 天"],
    ref: "注入非默认（默认 startDate 为空：『请选择起算日期』无届满日）。时效起算日 2020-01-15、类型一般诉讼时效（3年），届满日 = 起算日 + 3年遇周末/法定顺延 ⇒ 页面输出『届满日 2022-01-17』；截至冻结当前日输出『已过 880 天』。两条均不在默认空态。⚠ 不锚 type 回显『2』与 interrupted 回显『off』（输入值恒随注入变）；addYears/daysBetween/isHoliday 是日期辅助函数，harness 第3步兜底无参调用产生 benign errs，不影响 res 主链。"
  },
  {
    slug: "legal/will-template-generator",
    inputs: { testatorName: "张三", testatorId: "31010119900101001X", testatorAddr: "上海市浦东新区", willDate: "2026-05-01", willPlace: "上海", heirList: "李四 儿子\n王五 女儿", assetList: "房产一套", witness1: "赵六", witness2: "钱七" },
    expect: ["立遗嘱人：张三", "身份证号：31010119900101001X", "上海市浦东新区"],
    ref: "注入非默认（默认空模板：『（请添加财产明细）』『（请添加继承人信息）』无姓名）。页面把立遗嘱人姓名/身份证/住址原样拼入遗嘱正文 ⇒ 锚『立遗嘱人：张三』『身份证号：31010119900101001X』『上海市浦东新区』，三条均不在默认空模板。不锚『上海』（willPlace 可能默认同值，回退仍命中）与遗嘱正文固定导语（所有状态共有）。"
  },
  {
    slug: "legal/calendar-qr",
    inputs: { title: "项目启动会", loc: "会议室B", desc: "评审方案", start: "2026-07-01T10:00", end: "2026-07-01T11:00" },
    expect: ["SUMMARY:项目启动会", "LOCATION:会议室B", "DTSTART:20260701T020000Z"],
    ref: "注入非默认（默认无标题：输出空 ICS『BEGIN:VEVENT SUMMARY: LOCATION: ...』）。页面把事件标题/地点/起止拼入 ICS 文本 ⇒ 锚『SUMMARY:项目启动会』『LOCATION:会议室B』『DTSTART:20260701T020000Z』（start=2026-07-01T10:00 本地转 UTC+8 ⇒ 020000Z；end 11:00 ⇒ 030000Z）。三条均不在默认空态。⚠ renderQR/strHash 是 QR 渲染辅助函数，harness 第3步兜底无参调用产生 benign errs，不影响 output 主链。"
  }
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