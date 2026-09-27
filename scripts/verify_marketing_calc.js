#!/usr/bin/env node
/**
 * 第 25 道门禁：marketing 分类计算正确性验证（14 个确定性数值工具 / 24 个用例）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：estimate-sample-size-confidence（含 select :checked 查询，stub 不稳）；
 *       funnel-calculator / market-share（多行/多 competitor 动态结构，框架难注入）；
 *       ad-roi / marketing-roi（buyMode 切换全局 + 多分支）。
 * 用法: node scripts/verify_marketing_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "marketing/marketing-ctr-calculator",
    inputs: { impressions: "10000", clicks: "500", cost: "2000", conversions: "50" },
    expect: ["10.00", "4.00"],
    ref: "ctr=500/10000×100=5.00；cvr=50/500×100=10.00；cpc=2000/500=4.00；cpm=2000/10000×1000=200.00",
  },
  {
    slug: "marketing/marketing-conversion-rate-calculator",
    inputs: { visitors: "1000", conversions: "50", totalCost: "5000", avgOrder: "200" },
    expect: ["5.00", "100.00"],
    ref: "cvr=50/1000×100=5.00；cpa=5000/50=100.00；revenue=50×200=10000；roas=10000/5000=2.00",
  },
  {
    slug: "marketing/marketing-churn-rate",
    inputs: { startCustomers: "1000", endCustomers: "900", newCustomers: "100", arpu: "50" },
    expect: ["20.00", "80.00", "5.00"],
    ref: "lost=1000+100-900=200；churnRate=200/1000×100=20.00；retention=80.00；lifespan=1/(0.2)=5.00",
  },
  {
    slug: "marketing/marketing-roas-calculator",
    inputs: { adSpend: "8000", adRevenue: "50000" },
    expect: ["6.25x", "广告毛利润 ¥42,000.00"],
    ref: "roas=50000/8000=6.25；profit=42000；profitMargin=42000/50000×100=84.0（原 10000/40000 与默认 5000/20000 比值相同 → 逃生项）",
  },
  {
    slug: "marketing/marketing-cac-calculator",
    inputs: { marketingSpend: "8000", salesSpend: "2000", newCustomers: "100", ltv: "500" },
    expect: ["100.00", "80.00"],
    ref: "totalSpend=10000；cac=10000/100=100.00；marketingCAC=8000/100=80.00；ltvCacRatio=500/100=5.00",
  },
  {
    slug: "marketing/marketing-ltv-calculator",
    inputs: { mrrDetail: "100", churnDetail: "10", marginDetail: "60", cacDetail: "200" },
    expect: ["600.00", "3.00"],
    ref: "默认 detail 模式：lifespanMonths=1/(10/100)=10；ltvGross=100×10=1000；ltv=1000×0.6=600.00；LTV:CAC=600/200=3.00",
  },
  {
    slug: "marketing/marketing-markup-margin",
    inputs: { costMarkup: "180", markupRate: "35" },
    expect: ["¥243.00", "¥63.00", "25.93%"],
    ref: "price=180×1.35=243.00；profit=63.00；marginRate=63/243×100=25.93%。"
       + "原 100/50 即页面默认态，150.00/33.33 回退默认仍命中 ⇒ 逃生项，已换非默认输入。",
  },
  {
    slug: "marketing/marketing-discount-rate",
    inputs: { origPrice: "200", discountPct: "20" },
    expect: ["160.00", "40.00"],
    ref: "salePrice=200×0.8=160.00；saveAmount=40.00（percent 模式默认）",
  },
  {
    slug: "marketing/marketing-break-even-roas",
    inputs: { price: "100", margin: "40" },
    expect: ["40.00"],
    ref: "marginRatio=0.4；breakEvenRoas=1/0.4=2.50；profitPerUnit=100×0.4=40.00",
  },
  {
    slug: "marketing/calc-1",
    inputs: { spend: "25000", revenue: "90000", conversions: "250", costRate: "25" },
    expect: ["170.00%", "3.60", "42,500.00", "47.22%"],
    ref: "cogs=90000×0.25=22500；profit=90000−25000−22500=42500；roi=42500/25000=170.00%；"
       + "roas=90000/25000=3.60；利润率=42500/90000=47.22%；cpa=25000/250=100.00"
       + "（与默认态 CPA 同值 ⇒ 不入断言，否则回退默认仍命中）。",
  },
  {
    slug: "marketing/marketing-ltv-cac-ratio",
    inputs: { ltv: "600", cac: "200" },
    expect: ["3.00", "200.00"],
    ref: "ratio=600/200=3.00；profit=400；roi=(400/200)×100=200.00；paybackMonths=200/(600/36)=12.00",
  },
  {
    slug: "marketing/calc-price-elasticity",
    inputs: { p1: "100", q1: "100", p2: "90", q2: "120" },
    expect: ["-1.727"],
    ref: "midQ=110,midP=95；pctQ=20/110×100=18.18；pctP=-10/95×100=-10.53；ed=18.18/-10.53=-1.73（|Ed|>1 富有弹性）",
  },
  {
    slug: "marketing/price-elasticity",
    inputs: { p1: "100", q1: "100", p2: "110", q2: "80" },
    expect: ["-2.33"],
    ref: "avgQ=90,avgP=105；pctQ=-20/90×100=-22.22；pctP=10/105×100=9.52；ped=-22.22/9.52=-2.33（|Ed|>1 富有弹性）",
  },
  // ── 广告投放 ROI 测算（marketing/ad-roi）：CPC / CPM 双计费分支 ──
  {
    // CPC 盈利档：非默认（预算 2 万元、CPC 4 元、CTR 2%、CVR 6%、客单 300 元、毛利 40%＋固定成本 1000 元）
    slug: "marketing/ad-roi",
    inputs: { budget: "20000", cpc: "4", ctr: "2", cvr: "6", aov: "300", costRate: "40", fixedCost: "1000" },
    clicks: ["setBuy('cpc');calc();"],
    expect: ["4.50 ROAS", "57.9% 综合 ROI", "250,000 展示量"],
    ref: "CPC 分支：点击 = 20000/4 = 5000；展示 = 点击/CTR = 5000/2% = 250,000；转化 = 5000×6% = 300；"
     + "收入 = 300×300 = 90000；商品成本 = 90000×40% = 36000；总成本 = 20000+36000+1000 = 57000；"
     + "利润 = 33000；ROAS = 90000/20000 = 4.50；ROI = 33000/57000 = 57.89% ⇒ 57.9%。盈亏平衡 ROAS"
     + " = 1/(1−40%) = 1.67，4.50 ≥ 1.67 ⇒ 盈利。默认态（1 万元 / CPC 2 / CTR 3% / CVR 5% /客单 200 /"
     + "毛利 50% / 固定 0）为 −33.3% / ROAS 5.00，三条均不命中。",
  },
  {
    // CPC 亏损档：非默认（预算 5000、CPC 5、CTR 1%、CVR 2%、客单 100、毛利 60%＋固定 200）
    slug: "marketing/ad-roi",
    inputs: { budget: "5000", cpc: "5", ctr: "1", cvr: "2", aov: "100", costRate: "60", fixedCost: "200" },
    clicks: ["setBuy('cpc');calc();"],
    expect: ["0.40 ROAS", "-68.8% 综合 ROI", "5.00%"],
    ref: "点击 = 5000/5 = 1000；展示 = 1000/1% = 100,000；转化 = 20；收入 = 2000；商品成本 = 1200；"
     + "总成本 = 5000+1200+200 = 6400；利润 = −4400；ROAS = 0.40；ROI = −4400/6400 = −68.75% ⇒ −68.8%。"
     + "盈亏平衡 ROAS = 1/40% = 2.50；补亏提示「转化率需提升至 (5000/100)/1000 = 5.00% 或客单价提升至"
     + " 5000/(1000×2%) = 250 元」。默认态三条全不命中。",
  },
  {
    // CPM 计费分支（buyMode 默认 cpc，用例显式切 cpm）：非默认（预算 8000、CPM 40、CTR 2.5%、CVR 4%）
    slug: "marketing/ad-roi",
    inputs: { budget: "8000", cpm: "40", ctr: "2.5", cvr: "4", aov: "250", costRate: "45", fixedCost: "500" },
    clicks: ["setBuy('cpm');calc();"],
    expect: ["6.25 ROAS", "61.3% 综合 ROI", "200,000 展示量"],
    ref: "CPM 分支：展示 = 8000/40×1000 = 200,000；点击 = 200,000×2.5% = 5000；转化 = 200；收入 ="
     + " 200×250 = 50000；商品成本 = 22500；总成本 = 8000+22500+500 = 31000；利润 = 19000；"
     + "ROAS = 50000/8000 = 6.25；ROI = 19000/31000 = 61.29% ⇒ 61.3%；盈亏平衡 ROAS = 1/55% = 1.82。"
     + "注意 CPC 分支会读 #cpc（默认值 2），本例不参与计算（默认态走 cpc 分支，三条全不命中）。",
  },
  {
    // 零转化边界：CVR=0 ⇒ 转化/收入为 0，CPA 回落 0；客单价补亏项出现 ∞（fmt(Infinity)）
    slug: "marketing/ad-roi",
    inputs: { budget: "1000", cpc: "3", cvr: "0", fixedCost: "300" },
    clicks: ["setBuy('cpc');calc();"],
    expect: ["-100.0% 综合 ROI", "∞ 元"],
    ref: "点击 = 1000/3 = 333.33 ⇒ 展示 11,111；转化 0、收入 0、商品成本 0；总成本 = 1000+0+300 = 1300；"
     + "利润 = −1300；ROAS = 0；ROI = −1300/1300 = −100.0%。CPA 走 `conversions>0?budget/conversions:0` ⇒ 0。"
     + "亏损建议里「客单价提升至 budget/(clicks×cvr) = 1000/0 = ∞」是页面在 CVR=0 下的自然产物（非缺陷，"
     + "修复 ∞ 显示后本条须同步更新）。costRate 沿用默认 50%（默认态同值，不参与本条判定）。⚠ 本例不锚"
     + "「0 转化数」—— harness 默认态下各 input 为空串 ⇒ 整条链算出全 0，同样产出「0 转化数」，"
     + "锚它即成逃生项，故只保留 −100.0% 与 ∞ 两条。",
  },
  {
    // ⚠ 页面逻辑缺陷（已留档报老板，未擅改）：costRate=100 ⇒ 毛利率 0 ⇒ 盈亏平衡 ROAS 恒 0
    //   ⇒ roasOk 恒真，亏损（利润 −5000、ROI −35.7%）却显示「✓ 盈利」与「当前盈利」
    slug: "marketing/ad-roi",
    inputs: { budget: "5000", cpm: "50", ctr: "2", cvr: "3", aov: "150", costRate: "100", fixedCost: "0" },
    clicks: ["setBuy('cpm');calc();"],
    expect: ["0.00 盈亏平衡 ROAS", "-35.7%"],
    ref: "CPM：展示 = 5000/50×1000 = 100,000，点击 2000，转化 60，收入 9000，商品成本 = 9000×100% = 9000，"
     + "总成本 = 5000+9000 = 14000，利润 = −5000 ⇒ ROI = −35.7%、ROAS = 1.80。"
     + "毛利率 = 1−100% = 0 ⇒ breakEvenRoas = 1/0 走 else 分支取 0（`grossMargin>0?1/grossMargin:0`）"
     + " ⇒ roasOk = 1.80≥0 恒真 ⇒ 页面输出「✓ 盈利」/**「当前盈利」**，与利润为负矛盾。"
     + "本条用例锚的是页面**当前实际产物**（修复后须同步更新）。",
  },  {
    slug: "marketing/cpc-calculator",
    inputs: { budget: "20000", unitPrice: "4", ctr: "2", cvr: "2.5" },
    clicks: ["setMode('cpc');document.getElementById('budget').value='20000';document.getElementById('unitPrice').value='4';document.getElementById('ctr').value='2';document.getElementById('cvr').value='2.5';calcConvert();"],
    expect: ['250,000', '¥80.00', '¥160.00'],
    ref: 'CPC 模式（unitPrice 即点击单价）：点击 = 20000÷4 = 5000；展示 = 5000÷2% = **250,000**；转化 = 5000×2.5% = 125 ⇒ CPA = 20000÷125 = **¥160.00**、CPM = 20000÷(250000÷1000) = **¥80.00**。三条锚分属「展示反推」「转化率 → CPA」「展示量 → CPM」三个独立系数，默认态（¥50.00 / ¥66.67 / 200,000）全不命中。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { unitPrice: "40", ctr: "5", cvr: "8" },
    clicks: ["setMode('cpm');document.getElementById('unitPrice').value='40';document.getElementById('ctr').value='5';document.getElementById('cvr').value='8';calcConvert();"],
    expect: ['250,000', '¥10.00'],
    ref: 'CPM 模式（unitPrice 改为千次展示单价）：展示 = 10000÷40×1000 = **250,000**；点击 = 250000×5% = 12500；转化 = 12500×8% = 1000 ⇒ CPC = 10000÷12500 = ¥0.80、CPA = 10000÷1000 = **¥10.00**。本条与上一条同预算但走完全不同的反推方向，任一条口径写反都会被另一条抓到。两条教训均来自逃生项：① 首轮锚 CPA `¥50.00` —— harness 兜底无参调用把 `currentMode` 写成非 cpc 值后，另一分支恰好也算出 50；② 点击量 `12,500` —— **inputs 里的赋值在默认态同样生效**（只有模式不同），于是默认态用同一组 40/5 走 cpm 分支也会得到 12,500。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { budget: "15000", unitPrice: "75", ctr: "4", cvr: "5" },
    clicks: ["setMode('cpa');document.getElementById('budget').value='15000';document.getElementById('unitPrice').value='75';document.getElementById('ctr').value='4';document.getElementById('cvr').value='5';calcConvert();"],
    expect: ['100,000', '¥150.00', '¥75.00'],
    ref: 'CPA 模式（unitPrice 即行动单价）：转化 = 15000÷75 = 200；点击 = 200÷5% = 4000；展示 = 4000÷4% = **100,000** ⇒ CPM = 15000÷(100000÷1000) = **¥150.00**、CPC = 15000÷4000 = ¥3.75。三模式的差异只在「哪个量由 unitPrice 直达」，本条 CPA 列恒等于输入单价 ¥75.00。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { totalBudget: "80000" },
    clicks: ["document.getElementById('totalBudget').value='80000';calcBudget();"],
    expect: ['¥34,286', '53,333', '19,048'],
    ref: '预算分配表：总预算 80000，渠道按 ratio 分摊。微信（30%）得 80000×30/70 = 34285.71 ⇒ 千分位化后 **¥34,286**，其点击量 = 34285.71÷1.8 = **19,048**；合计点击 = 5714+19048+28571 = **53,333**。注意 harness 兜底会无参调 `addChannel()` 给渠道清单多加一条 10% 渠道（合计占比 70% 而非 100%），故本条只锚按比例缩放的量，不锚逐渠道转化量；首轮锚的合计 CPA `¥53.16` 也是逃生项——该量与总预算**无关**（转化量与预算同比例缩放），默认态同样命中。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { targetConv: "500", estCpa: "60", estCtr: "2.5", estCvr: "5", estPrice: "299", estMargin: "45" },
    clicks: ["calcEstimate();"],
    expect: ['¥37,275', '124.3%', '400.0K'],
    ref: '预估标签页：预算 = 500×60 = **¥30,000**；收入 = 500×299 = ¥149,500；利润 = 149500×45% − 30000 = 67275 − 30000 = **¥37,275**；点击 = 500÷5% = 10000、展示 = 10000÷2.5% = 400000 ⇒ **400.0K**；ROI = 37275÷30000×100 = 124.25 ⇒ **124.3%**。默认态该页根本不执行 calcEstimate（结果区停留在 HTML 静态占位 ¥39,600 / 49.5%），三条锚全不命中。',
  },
  {
    slug: "marketing/cpc-calculator",
    inputs: { targetConv: "1000", estCpa: "120", estCtr: "2.5", estCvr: "5", estPrice: "299", estMargin: "10" },
    clicks: ["calcEstimate();"],
    expect: ['¥-90,100', '-75.1%', '800.0K'],
    ref: '同式的亏本分支：预算 = 1000×120 = ¥120,000、收入 = 299,000；利润 = 299000×10% − 120000 = 29900 − 120000 = **¥-90,100**（负号与千分位同时出现）；ROI = −90100÷120000×100 = −75.083 ⇒ **−75.1%**；展示 = (1000÷5%)÷2.5% = 800000 ⇒ **800.0K**。与上一条构成同式异参对照：同一批系数，利润由其唯一变量（毛利率 45% vs 10%）决定正负。',
  },

  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "150", freeShipThreshold: "99", shippingFee: "10", avgMargin: "45" },
    expect: ["✅ 已满足包邮条件"],
    ref: '免费门槛：购物车 ¥150 ≥ 阈值 ¥99 ⇒ 已包邮，输出「✅ 已满足包邮条件」。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "50", freeShipThreshold: "99", shippingFee: "12", avgMargin: "40" },
    expect: ["还差 ¥49.00 包邮", "建议直接支付运费¥12更划算"],
    ref: '未包邮差额 = 99−50 = ¥49.00；凑单成本 = 49×(1−40%) = ¥29.40 ≥ 运费¥12 ⇒ 直接付运费更划算。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "80", freeShipThreshold: "99", shippingFee: "8", avgMargin: "50" },
    expect: ["还差 ¥19.00 包邮", "建议直接支付运费¥8更划算"],
    ref: '差额 = 99−80 = ¥19.00；凑单成本 = 19×50% = ¥9.50 ≥ 运费¥8 ⇒ 付运费更划算。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "85", freeShipThreshold: "99", shippingFee: "15", avgMargin: "30" },
    expect: ["还差 ¥14.00 包邮", "建议凑单¥14的商品（商家成本约¥9.80，低于运费¥15）"],
    ref: '差额 = 99−85 = ¥14.00；凑单成本 = 14×70% = ¥9.80 < 运费¥15 ⇒ 建议凑单。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "90", freeShipThreshold: "99", shippingFee: "25", avgMargin: "10" },
    expect: ["还差 ¥9.00 包邮", "建议凑单¥9的商品（商家成本约¥8.10，低于运费¥25）"],
    ref: '差额 = 99−90 = ¥9.00；凑单成本 = 9×90% = ¥8.10 < 运费¥25 ⇒ 建议凑单。',
  },
  {
    slug: "marketing/marketing-free-shipping-threshold",
    name: "包邮门槛计算器",
    inputs: { currentCart: "30", freeShipThreshold: "50", shippingFee: "5", avgMargin: "60" },
    expect: ["还差 ¥20.00 包邮", "建议直接支付运费¥5更划算"],
    ref: '阈值改 ¥50：差额 = 50−30 = ¥20.00；凑单成本 = 20×40% = ¥8.00 ≥ 运费¥5 ⇒ 付运费更划算。',
  }
,
  {
    slug: "marketing/marketing-engagement-rate",
    name: "社交媒体互动率计算器",
    inputs: { followers: "10000", likes: "300", comments: "120", shares: "60", impressionsEng: "0" },
    expect: ["总互动数：480", "互动率（按粉丝）：4.80%"],
    ref: 'totalEng=300+120+60=480；按粉丝互动率=480/10000×100=4.80%；impressions=0 ⇒ 无「基于展示」行。',
  },
  {
    slug: "marketing/marketing-engagement-rate",
    name: "社交媒体互动率计算器",
    inputs: { followers: "20000", likes: "500", comments: "100", shares: "80", impressionsEng: "50000" },
    expect: ["总互动数：680", "互动率（按粉丝）：3.40%", "基于展示的互动率：1.36%"],
    ref: 'totalEng=500+100+80=680；按粉丝=680/20000×100=3.40%；基于展示=680/50000×100=1.36%。',
  },
  {
    slug: "marketing/marketing-engagement-rate",
    name: "社交媒体互动率计算器",
    inputs: { followers: "1000", likes: "80", comments: "30", shares: "20", impressionsEng: "0" },
    expect: ["总互动数：130", "互动率（按粉丝）：13.00%"],
    ref: 'totalEng=80+30+20=130；按粉丝=130/1000×100=13.00%；impressions=0 无展示行。',
  },
  {
    slug: "marketing/marketing-engagement-rate",
    name: "社交媒体互动率计算器",
    inputs: { followers: "5000", likes: "200", comments: "50", shares: "50", impressionsEng: "10000" },
    expect: ["总互动数：300", "互动率（按粉丝）：6.00%", "基于展示的互动率：3.00%"],
    ref: 'totalEng=200+50+50=300；按粉丝=300/5000×100=6.00%；基于展示=300/10000×100=3.00%。',
  },
  {
    slug: "marketing/marketing-engagement-rate",
    name: "社交媒体互动率计算器",
    inputs: { followers: "1000000", likes: "1000", comments: "200", shares: "100", impressionsEng: "0" },
    expect: ["总互动数：1,300", "互动率（按粉丝）：0.13%"],
    ref: 'totalEng=1000+200+100=1300（千分位 1,300）；按粉丝=1300/1000000×100=0.13%；impressions=0 无展示行。',
  },
  {
    slug: "marketing/marketing-engagement-rate",
    name: "社交媒体互动率计算器",
    inputs: { followers: "30000", likes: "150", comments: "30", shares: "20", impressionsEng: "80000" },
    expect: ["总互动数：200", "互动率（按粉丝）：0.67%", "基于展示的互动率：0.25%"],
    ref: 'totalEng=150+30+20=200；按粉丝=200/30000×100=0.6667⇒0.67%；基于展示=200/80000×100=0.25%。',
  },
  {
    slug: "marketing/marketing-influencer-pricing",
    inputs: { followersInf: "5000", engRateInf: "4", platformFactor: "1.0", contentType: "1.0" },
    expect: ["达人层级：素人/KOC", "参考报价：¥420 - ¥780", "建议报价：¥600"],
    ref: 'f=5000<10000⇒cpmBase=100,素人/KOC；engBonus=1+(4-2)/10=1.2；price=5×100×1.2×1.0×1.0=600；low=420；high=780'
  },
  {
    slug: "marketing/marketing-influencer-pricing",
    inputs: { followersInf: "50000", engRateInf: "5", platformFactor: "1.2", contentType: "1.5" },
    expect: ["达人层级：尾部达人", "参考报价：¥16,380 - ¥30,420", "建议报价：¥23,400"],
    ref: 'f=50000⇒cpmBase=200,尾部达人；engBonus=1.3；price=50×200×1.3×1.2×1.5=23400；low=16380；high=30420'
  },
  {
    slug: "marketing/marketing-influencer-pricing",
    inputs: { followersInf: "300000", engRateInf: "6", platformFactor: "2.0", contentType: "2.5" },
    expect: ["达人层级：腰部达人", "参考报价：¥441,000 - ¥819,000", "建议报价：¥630,000"],
    ref: 'f=300000⇒cpmBase=300,腰部达人；engBonus=1.4；price=300×300×1.4×2.0×2.5=630000；low=441000；high=819000'
  },
  {
    slug: "marketing/marketing-influencer-pricing",
    inputs: { followersInf: "800000", engRateInf: "3", platformFactor: "1.5", contentType: "1.0" },
    expect: ["参考报价：¥369,600 - ¥686,400", "建议报价：¥528,000"],
    ref: 'f=800000⇒cpmBase=400,肩部达人分支；engBonus=1.1；price=800×400×1.1×1.5×1.0=528000；low=369600；high=686400。锚用价格串（bare 预置 500000→肩部同档，纯『达人层级：肩部达人』串会与默认态撞车逃生，故改用依赖全部输入的价格区间串）'
  },
  {
    slug: "marketing/marketing-influencer-pricing",
    inputs: { followersInf: "2000000", engRateInf: "4", platformFactor: "1.0", contentType: "1.5" },
    expect: ["达人层级：头部达人", "参考报价：¥1,260,000 - ¥2,340,000", "建议报价：¥1,800,000"],
    ref: 'f=2000000≥1e6⇒cpmBase=500,头部达人；engBonus=1.2；price=2000×500×1.2×1.0×1.5=1800000；low=1260000；high=2340000'
  },
  {
    slug: "marketing/marketing-influencer-pricing",
    inputs: { followersInf: "200000", engRateInf: "2", platformFactor: "1.2", contentType: "2.5" },
    expect: ["达人层级：腰部达人", "参考报价：¥126,000 - ¥234,000", "建议报价：¥180,000"],
    ref: 'f=200000⇒cpmBase=300,腰部达人；engBonus=1+(2-2)/10=1.0；price=200×300×1.0×1.2×2.5=180000；low=126000；high=234000'
  },
  {
    slug: "marketing/marketing-sales-funnel",
    inputs: { visitors: "10000", leads: "2000", qualified: "800", opportunities: "300", customers: "120" },
    expect: ["整体转化率：1.200%", "转化率: 20.0%"],
    ref: 'v=10000 l=2000 q=800 o=300 c=120；整体=120/10000×100=1.200%；第二锚取本级转化率 20.0%（默认态各级 5.0/40.0/40.0/25.0，不撞车）'
  },
  {
    slug: "marketing/marketing-sales-funnel",
    inputs: { visitors: "50000", leads: "10000", qualified: "4000", opportunities: "1500", customers: "750" },
    expect: ["整体转化率：1.500%", "转化率: 37.5%"],
    ref: 'v=50000 l=10000 q=4000 o=1500 c=750；整体=750/50000×100=1.500%；第二锚取本级转化率 37.5%（默认态各级 5.0/40.0/40.0/25.0，不撞车）'
  },
  {
    slug: "marketing/marketing-sales-funnel",
    inputs: { visitors: "20000", leads: "5000", qualified: "2500", opportunities: "1000", customers: "400" },
    expect: ["整体转化率：2.000%", "转化率: 50.0%"],
    ref: 'v=20000 l=5000 q=2500 o=1000 c=400；整体=400/20000×100=2.000%；第二锚取本级转化率 50.0%（默认态各级 5.0/40.0/40.0/25.0，不撞车）'
  },
  {
    slug: "marketing/marketing-sales-funnel",
    inputs: { visitors: "8000", leads: "2400", qualified: "1200", opportunities: "600", customers: "100" },
    expect: ["整体转化率：1.250%", "转化率: 16.7%"],
    ref: 'v=8000 l=2400 q=1200 o=600 c=100；整体=100/8000×100=1.250%；第二锚取本级转化率 16.7%（默认态各级 5.0/40.0/40.0/25.0，不撞车）'
  },
  {
    slug: "marketing/marketing-sales-funnel",
    inputs: { visitors: "25000", leads: "6000", qualified: "3000", opportunities: "900", customers: "225" },
    expect: ["整体转化率：0.900%", "转化率: 24.0%"],
    ref: 'v=25000 l=6000 q=3000 o=900 c=225；整体=225/25000×100=0.900%；第二锚取本级转化率 24.0%（默认态各级 5.0/40.0/40.0/25.0，不撞车）'
  },
  {
    slug: "marketing/marketing-sales-funnel",
    inputs: { visitors: "120000", leads: "36000", qualified: "12000", opportunities: "4800", customers: "960" },
    expect: ["整体转化率：0.800%", "转化率: 33.3%"],
    ref: 'v=120000 l=36000 q=12000 o=4800 c=960；整体=960/120000×100=0.800%；第二锚取本级转化率 33.3%（默认态各级 5.0/40.0/40.0/25.0，不撞车）'
  },
  {
    slug: "marketing/marketing-google-ads-budget",
    inputs: { avgCpc: "2", targetClicksDay: "80", convRate: "5", avgOrderValue: "200" },
    expect: ["月预估收入：¥24,000", "5.00x"],
    ref: 'cpc=2 clicks=80 cr=5 aov=200；日预算=2×80=160、月预算=4,800；日订单=80×5/100=4.0；日收入=800、月收入=24,000；ROAS=(5/100×200)/2=5.00x（与点击量无关）。锚1 用全键月收入、锚2 用 ROAS，均避开默认串集'
  },
  {
    slug: "marketing/marketing-google-ads-budget",
    inputs: { avgCpc: "5", targetClicksDay: "40", convRate: "4", avgOrderValue: "600" },
    expect: ["月预估收入：¥28,800", "4.80x"],
    ref: 'cpc=5 clicks=40 cr=4 aov=600；日预算=5×40=200、月预算=6,000；日订单=40×4/100=1.6；日收入=960、月收入=28,800；ROAS=(4/100×600)/5=4.80x（与点击量无关）。锚1 用全键月收入、锚2 用 ROAS，均避开默认串集'
  },
  {
    slug: "marketing/marketing-google-ads-budget",
    inputs: { avgCpc: "1.5", targetClicksDay: "200", convRate: "2", avgOrderValue: "150" },
    expect: ["月预估收入：¥18,000", "2.00x"],
    ref: 'cpc=1.5 clicks=200 cr=2 aov=150；日预算=1.5×200=300、月预算=9,000；日订单=200×2/100=4.0；日收入=600、月收入=18,000；ROAS=(2/100×150)/1.5=2.00x（与点击量无关）。锚1 用全键月收入、锚2 用 ROAS，均避开默认串集'
  },
  {
    slug: "marketing/marketing-google-ads-budget",
    inputs: { avgCpc: "4", targetClicksDay: "120", convRate: "3", avgOrderValue: "800" },
    expect: ["月预估收入：¥86,400", "6.00x"],
    ref: 'cpc=4 clicks=120 cr=3 aov=800；日预算=4×120=480、月预算=14,400；日订单=120×3/100=3.6；日收入=2,880、月收入=86,400；ROAS=(3/100×800)/4=6.00x（与点击量无关）。锚1 用全键月收入、锚2 用 ROAS，均避开默认串集'
  },
  {
    slug: "marketing/marketing-google-ads-budget",
    inputs: { avgCpc: "6", targetClicksDay: "60", convRate: "5", avgOrderValue: "400" },
    expect: ["月预估收入：¥36,000", "3.33x"],
    ref: 'cpc=6 clicks=60 cr=5 aov=400；日预算=6×60=360、月预算=10,800；日订单=60×5/100=3.0；日收入=1,200、月收入=36,000；ROAS=(5/100×400)/6=3.33x（与点击量无关）。锚1 用全键月收入、锚2 用 ROAS，均避开默认串集'
  },
  {
    slug: "marketing/marketing-google-ads-budget",
    inputs: { avgCpc: "10", targetClicksDay: "30", convRate: "8", avgOrderValue: "1000" },
    expect: ["月预估收入：¥72,000", "8.00x"],
    ref: 'cpc=10 clicks=30 cr=8 aov=1000；日预算=10×30=300、月预算=9,000；日订单=30×8/100=2.4；日收入=2,400、月收入=72,000；ROAS=(8/100×1000)/10=8.00x（与点击量无关）。锚1 用全键月收入、锚2 用 ROAS，均避开默认串集'
  }
];

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
  console.log("==== marketing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();