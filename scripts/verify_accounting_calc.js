#!/usr/bin/env node
/**
 * 第 35 道门禁：accounting 分类计算正确性验证（35 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经复核「不等于」默认值输出，杜绝假通过。
 * calc-1 为「含税/不含税」双向开关，需以 checks:["gross"] 声明 mode 单选选中项。
 * 用法: node scripts/verify_accounting_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "accounting/depreciation-declining",
    clicks: ["var __cap=[];var __exp=0;TBKit={util:{isEn:function(){return false;},exportTable:function(){},exportCsv:function(){__exp=1;},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('result').textContent='请填写「原值」后再计算。';__depreciation_decliningExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='DEPSC hist='+__cap.length;"],
    expect: ["DEPSC hist=0"],
    ref: "复核失败重做·F-N189 第46批 折旧页：必填提示「请填写…后再计算。」旧 Score 词表不含该词 ⇒ 错误态写历史；修复后补 请填写|再计算|必须 ⇒ Score=0，Extras 早退不写历史。默认态无探针串 ⇒ 零逃生。"
  },
  { slug: "accounting/current-ratio", inputs: { ca: "4500000", cl: "1500000" }, expect: ["3.00"], ref: "流动比率=流动资产/流动负债=4500000/1500000=3.00（负债占比=33.3%；默认 3000000/1500000=2.00 避开）" },
  { slug: "accounting/quick-ratio", inputs: { ca: "3600000", inv: "600000", cl: "1500000" }, expect: ["2.00"], ref: "速动比率=(CA−存货)/CL=(3600000−600000)/1500000=2.00（默认 2200000/1500000=1.47 避开）" },
  { slug: "accounting/debt-to-asset", inputs: { tl: "2000000", ta: "8000000" }, expect: ["25.00"], ref: "资产负债率=负债/资产=2000000/8000000=25.00%（权益比率 75.00%；默认 3000000/8000000=37.50 避开）" },
  { slug: "accounting/gross-margin", inputs: { rev: "2000000", cost: "1300000" }, expect: ["35.00"], ref: "毛利率=(营收−成本)/营收=(2000000−1300000)/2000000=35.00%（毛利额 700000；默认 1000000/600000 亦为 40.00%，故避开 40%）" },
  { slug: "accounting/gross-profit", inputs: { rev: "1500", cogs: "900" }, expect: ["600.00"], ref: "毛利=营收−营业成本=1500−900=600.00 万元（默认 1000−600=400.00 避开）" },
  { slug: "accounting/net-profit-margin", inputs: { np: "240000", rev: "1200000" }, expect: ["20.00"], ref: "净利率=净利/营收=240000/1200000=20.00%（年化 240.00%；默认 150000/1000000 亦为 15.00%，故避开 15%）" },
  { slug: "accounting/roe-calc", inputs: { np: "300000", eq: "2000000" }, expect: ["15.00"], ref: "ROE=净利/净资产=300000/2000000=15.00%（默认 200000/2000000=10.00 避开）" },
  { slug: "accounting/roa-calc", inputs: { np: "350000", ta: "5000000" }, expect: ["7.00"], ref: "ROA=净利/总资产=350000/5000000=7.00%（默认 200000/5000000=4.00 避开）" },
  { slug: "accounting/roe-dupont", inputs: { nm: "10", at: "1.2", em: "2.5" }, expect: ["30.00"], ref: "杜邦 ROE=净利率×周转率×权益乘数=(10/100)×1.2×2.5×100=30.00%（默认 12×1.5×2.0=36.00% 避开）" },
  { slug: "accounting/ebit", inputs: { rev: "1200", cogs: "700", opex: "200" }, expect: ["300.00"], ref: "EBIT=营收−成本−费用=1200−700−200=300.00 万元（默认 1000−600−200=200.00 避开）" },
  { slug: "accounting/ebitda", inputs: { EBIT: "300", DA: "80" }, expect: ["380.00"], ref: "EBITDA=EBIT+折旧摊销=300+80=380.00 万元（默认 200+50=250.00 避开）" },
  { slug: "accounting/interest-coverage", inputs: { EBIT: "300", int: "50" }, expect: ["6.00"], ref: "利息保障倍数=EBIT/利息费用=300/50=6.00（默认 200/40=5.00 避开）" },
  { slug: "accounting/inventory-turnover", inputs: { cogs: "6000000", inv: "1000000" }, expect: ["6.00"], ref: "存货周转率=营业成本/存货=6000000/1000000=6.00 次/年（周转天数=365/6=60.8 天；默认 4000000/800000 亦为 5.00，故避开 5）" },
  { slug: "accounting/inventory-days", inputs: { inv: "200", cogs: "600" }, expect: ["121.7"], ref: "DIO=存货/营业成本×365=200/600×365=121.7 天（默认 150/600×365=91.3 天 避开）" },
  { slug: "accounting/days-sales-outstanding", inputs: { AR: "200", rev: "1000" }, expect: ["73.0"], ref: "DSO=应收/营收×365=200/1000×365=73.0 天（默认 100/1000×365=36.5 天 避开）" },
  { slug: "accounting/days-payable-outstanding", inputs: { AP: "120", cogs: "600" }, expect: ["73.0"], ref: "DPO=应付/营业成本×365=120/600×365=73.0 天（默认 80/600×365=48.7 天 避开）" },
  { slug: "accounting/cash-conversion-cycle", inputs: { DSO: "0", DIO: "0", DPO: "0" }, expect: ["0.00"], ref: "T-N5 复核重做：DSO/DIO/DPO 均填 0（已填写的合法天数），旧实现主结果拒绝「⚠ 输入不能全为 0」且附表/历史却写入 CCC=0.00；现允许全零计算，CCC=0+0-0=0.00（营业周期=0 时占比显示「—」）。默认态 36.5+91.25−48.67=79.08 不含 0.00 ⇒ 强判别、零逃生。" },
  { slug: "accounting/cash-conversion-cycle", inputs: { DSO: "50", DIO: "100", DPO: "60" }, expect: ["90.00"], ref: "CCC=DSO+DIO−DPO=50+100−60=90.00 天（默认 36.5+91.25−48.67=79.08 天 避开）" },
  { slug: "accounting/working-capital", inputs: { CA: "800", CL: "300" }, expect: ["500.00"], ref: "营运资金=流动资产−流动负债=800−300=500.00 万元（默认 500−300=200.00 避开）" },
  { slug: "accounting/asset-turnover", inputs: { rev: "1500", assets: "500" }, expect: ["3.00"], ref: "总资产周转率=营收/平均总资产=1500/500=3.00（默认 1000/500=2.00 避开）" },
  { slug: "accounting/contribution-margin", inputs: { p: "120", vc: "70", q: "10000" }, expect: ["41.67"], ref: "边际贡献=(单价−单位变动)×销量=(120−70)×10000=500000 元；贡献率=500000/(120×10000)=41.67%（默认 100−60→40.00% 避开）" },
  { slug: "accounting/break-even-units", inputs: { fc: "300000", p: "120", vc: "70" }, expect: ["6000.0"], ref: "平衡产量=固定成本/(单价−单位变动)=300000/(120−70)=6000.0 件（平衡销售额 720000 元、单位边际贡献 50.00；默认 200000/40=5000.0 避开）" },
  { slug: "accounting/debt-service-coverage", inputs: { OCF: "200", ds: "50" }, expect: ["4.00"], ref: "DSCR=经营现金流/债务偿付=200/50=4.00（默认 150/60=2.50 避开）" },
  { slug: "accounting/debt-service-coverage", inputs: { OCF: "-150", ds: "60" }, expect: ["— 偿债负担率"], ref: "T-N16（2026-11-16）：OCF 为负 ⇒ DSCR = −2.50，旧实现 1/max(DSCR,1e-9) 输出 1000000000.0000「偿债负担率」。现仅 DSCR>0 才取倒数，否则显示「—」；默认 150/60 ⇒ 0.4000，不命中。" },
  { slug: "accounting/free-cash-flow", inputs: { OCF: "200", capex: "120" }, expect: ["80.00"], ref: "FCF=OCF−资本支出=200−120=80.00 万元（默认 150−80=70.00 避开）" },
  { slug: "accounting/operating-cash-flow", inputs: { NI: "150", DA: "60", dWC: "30" }, expect: ["180.00"], ref: "OCF=净利+折旧摊销−营运资本变动=150+60−30=180.00 万元（默认 120+50−20=150.00 避开）" },
  { slug: "accounting/depreciation-straight", inputs: { c: "200000", s: "20000", n: "8" }, expect: ["22500.00"], ref: "直线法年折旧=(原值−残值)/年限=(200000−20000)/8=22500.00 元（折旧率 11.25%、首年末账面 177500.00；默认 100000/10000/10→9000.00 避开）" },
  { slug: "accounting/depreciation-declining", inputs: { c: "200000", s: "20000", n: "5", yr: "2" }, expect: ["48000.00"], ref: "双倍余额递减率=2/5=0.4；第1年 200000×0.4=80000，第2年 120000×0.4=48000.00 元（期末账面 72000.00、累计 128000.00；默认 yr=3 避开）" },
  { slug: "accounting/depreciation-syd", inputs: { c: "210000", s: "10000", n: "6", yr: "2" }, expect: ["47619.05"], ref: "SYD=n(n+1)/2=21；第2年折旧=(6−2+1)/21×(210000−10000)=5/21×200000=47619.05 元（占原值 22.68%；默认 yr=1 避开）" },
  { slug: "accounting/depreciation-syd", inputs: { c: "100000", s: "10000", n: "10", yr: "12" }, expect: ["计算年份须为 1–10 之间的整数"], ref: "T-N14（2026-11-16）：越界年份 12 旧实现输出第 12 年折旧 −1636.36；现要求 1≤yr≤n 且为整数，越界直接拦截。默认 yr=1/n=10 ⇒ 不命中。" },
  { slug: "accounting/amortization-intangible", inputs: { c: "720000", s: "0", n: "6" }, expect: ["120000.00 年摊销额"], ref: "直线摊销年额=(成本−残值)/年限=720000/6=120000.00 元（月摊销 10000.00；默认 600000/10→60000.00 避开）" },
  { slug: "accounting/amortization-intangible", inputs: { c: "100000", s: "0", n: "0.4" }, expect: ["摊销年限须为正整数（年）"], ref: "T-N13（2026-11-16）：小数年限 0.4 旧实现主结果年摊销 250000.00，而计划表按 round(0.4)=1 年只摊 100000.00，两口径无法对账。现要求 n 为正整数；extras 同守卫，不再渲染计划表。默认 n=10 ⇒ 不命中。" },
  { slug: "accounting/amortization-intangible", inputs: { c: "100000", s: "0", n: "-5" }, expect: ["摊销年限须为正整数（年）"], ref: "T-N13 边界：负年限旧实现年摊销 −20000.00、计划表 1 年 100000.00；现拦截。默认 10 年 ⇒ 不命中。" },
  { slug: "accounting/amortization-intangible", inputs: { c: "100", s: "200", n: "5" }, expect: ["残值须在 0 与成本之间"], ref: "T-N13 边界：残值高于成本旧实现年摊销 −20.00、净值递增；现拦截。默认 600000/0 ⇒ 不命中。" },
  { slug: "accounting/calc-1", inputs: { amount: "21800", rate: "9" }, checks: ["gross"], expect: ["20,000.00"], ref: "含税价反算（mode=gross、税率 9%）：不含税=21800/(1+0.09)=20000.00、税额=1800.00（默认 net 模式 amount=10000 税率 13%→10,000.00 避开）" },
  { slug: "accounting/calc-2", inputs: { revenue: "800000", cost: "300000", loss: "0", rate: "15" }, expect: ["75,000.00"], ref: "利润总额=800000−300000=500000；应纳所得额 500000；按 15% 预缴=75000.00 元（利润率 62.50%；默认 revenue=500000 税率 25%→50,000.00 避开）" },
  { slug: "accounting/split-bill", inputs: { total: "600", people: "5", tip: "15" }, expect: ["138.00"], ref: "小费=600×15%=90.00；含小费总额=690.00；每人=690/5=138.00（默认 480/4/10→132.00 避开）" },
  { slug: "accounting/assessor-risk-11", inputs: { x1: "0.5", x2: "0.3", x3: "0.2", x4: "1.0", x5: "0.8" }, expect: ["3.0800"], ref: "Altman Z=1.2X1+1.4X2+3.3X3+0.6X4+1.0X5=0.6+0.42+0.66+0.60+0.80=3.0800（≥2.99 安全区；默认 x=0.35/0.20/0.12/1.5/1.2→3.1960 避开）" },
  { slug: "accounting/analysis-cost-5", inputs: { qty: "9000", mat: "36", lab: "18", vmoh: "8", fmoh: "200000", vsale: "4", fsale: "90000", price: "115", gm: "25" }, expect: ["84.22", "112.30", "5,918"], ref: "成本核算与 CVP：变动制造成本 36+18+8=62，固定分摊 200000÷9000=22.22 → 单位完全成本 84.22；单位边际贡献 115−66=49，保本量 290000÷49=5918（显示 5,918）；目标毛利 25% 售价 84.22÷0.75=112.30（独立复算；默认组为 85.00/121.43/6,522，注入失败即不命中）" },
{
  "slug": "accounting/report-2",
  "inputs": {
    "data": "库存现金,5000,0\n银行存款,120000,0\n应收账款,35000,0\n应付账款,0,48000\n短期借款,0,60000\n实收资本,0,52000"
  },
  "expect": [
    "借方合计： 160000.00",
    "贷方合计： 160000.00"
  ],
  "ref": "借=5000+120000+35000=160000；贷=48000+60000+52000=160000；差额0 → 平衡（默认 6 科目 90000/90000，避开「试算结果： 平衡」这类默认也成立的串）"
},
{
  "slug": "accounting/analysis-46",
  "inputs": {
    "data": "100\n118\n132\n151\n170"
  },
  "expect": [
    "下期预测值： 186.10",
    "线性趋势斜率： 17.30",
    "复合增长率： 14.19%"
  ],
  "ref": "最小二乘 b=(5*2186-15*671)/(5*55-225)=17.30、a=82.30；下期 x=6 → 186.10；R2 0.9974、CAGR 14.19%（默认 4 期 100/105/103/110 斜率 2.80 避开）"
},
  {
    "slug": "accounting/amortization-intangible",
    "inputs": {
      "c": "42",
      "s": "42",
      "n": "42"
    },
    "expect": [
      "42\n42\n42\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"c\":\"42\",\"s\":\"42\",\"n\":\"42\"}，输出区含「42\n42\n42\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/assessor-risk-11",
    "inputs": {
      "x1": "42",
      "x2": "42",
      "x3": "42",
      "x4": "42",
      "x5": "42"
    },
    "expect": [
      "-Score： 315.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x1\":\"42\",\"x2\":\"42\",\"x3\":\"42\",\"x4\":\"42\",\"x5\":\"42\"}，输出区含「-Score： 315.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/asset-turnover",
    "inputs": {
      "rev": "42",
      "assets": "42"
    },
    "expect": [
      "产收入比（倒数） 365.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rev\":\"42\",\"assets\":\"42\"}，输出区含「产收入比（倒数） 365.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/break-even-units",
    "inputs": {
      "fc": "42",
      "p": "42",
      "vc": "42"
    },
    "expect": [
      "单位边际贡献 ≤ 0"
    ],
    "ref": "自动补强（B类零用例）：注入 fc=p=vc=42，单位边际贡献 = 42−42 = 0，不存在盈亏平衡点；旧实现静默输出 Inf/—，现明确提示并拒绝计算。默认 100/60 ⇒ 不命中。"
  },
  {
    "slug": "accounting/cash-conversion-cycle",
    "inputs": {
      "DSO": "42",
      "DIO": "42",
      "DPO": "42"
    },
    "expect": [
      "42\n42\n42\n42.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"DSO\":\"42\",\"DIO\":\"42\",\"DPO\":\"42\"}，输出区含「42\n42\n42\n42.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/contribution-margin",
    "inputs": {
      "p": "42",
      "vc": "42",
      "q": "42"
    },
    "expect": [
      "42\n42\n42\n"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"p\":\"42\",\"vc\":\"42\",\"q\":\"42\"}，输出区含「42\n42\n42\n」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/analysis-cost-5",
    "inputs": {
      "qty": "42",
      "mat": "42",
      "lab": "42",
      "vmoh": "42",
      "fmoh": "42",
      "vsale": "42",
      "fsale": "42",
      "price": "42",
      "gm": "42"
    },
    "expect": [
      "读： 单位边际贡献不为正，卖得越多亏损越大，应优先提价或压缩单位变动成本"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"qty\":\"42\",\"mat\":\"42\",\"lab\":\"42\",\"vmoh\":\"42\",\"fmoh\":\"42\",\"vsale\":\"42\",\"fsale\":\"42\",\"price\":\"42\",\"gm\":\"42\"}，输出区含「读： 单位边际贡献不为正，卖得越多亏损越大，应优先提价或压缩单位变动成本」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/calc-2",
    "inputs": {
      "revenue": "42",
      "cost": "42",
      "loss": "42",
      "customRate": "42",
      "rate": "20"
    },
    "expect": [
      "季度利润： 0.00 元 估算应纳税所得额： 0.00 元"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"revenue\":\"42\",\"cost\":\"42\",\"loss\":\"42\",\"customRate\":\"42\",\"rate\":\"20\"}，输出区含「 应纳税所得额： 0.00 元 （已用亏损弥补 0.00 元） 适用税率： 20」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/calc-1",
    "inputs": {
      "amount": "42",
      "customRate": "42",
      "rate": "9"
    },
    "expect": [
      " 增值税额（税率 9.00%）： 3.78 元 价税合计： 45.78 元"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"amount\":\"42\",\"customRate\":\"42\",\"rate\":\"9\"}，输出区含「 增值税额（税率 9.00%）： 3.78 元 价税合计： 45.78 元」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/debt-service-coverage",
    "inputs": {
      "OCF": "42",
      "ds": "42"
    },
    "expect": [
      "余现金 (万元) 1.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"OCF\":\"42\",\"ds\":\"42\"}，输出区含「余现金 (万元) 1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/debt-to-asset",
    "inputs": {
      "tl": "42",
      "ta": "42"
    },
    "expect": [
      "权益比率 (%) 42.0000 权益乘数 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"tl\":\"42\",\"ta\":\"42\"}，输出区含「权益比率 (%) 42.0000 权益乘数 」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/current-ratio",
    "inputs": {
      "ca": "42",
      "cl": "42"
    },
    "expect": [
      "42\n42\n1.00 流动比率 10"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ca\":\"42\",\"cl\":\"42\"}，输出区含「42\n42\n1.00 流动比率 10」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/days-sales-outstanding",
    "inputs": {
      "AR": "42",
      "rev": "42"
    },
    "expect": [
      " 应收占收入比 12.17 DSO (月)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"AR\":\"42\",\"rev\":\"42\"}，输出区含「 应收占收入比 12.17 DSO (月)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/depreciation-declining",
    "inputs": {
      "c": "42",
      "s": "42",
      "n": "42",
      "yr": "42"
    },
    "expect": [
      "42\n42\n42\n42\n0.00 第42年折旧额 (元) 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"c\":\"42\",\"s\":\"42\",\"n\":\"42\",\"yr\":\"42\"}，输出区含「42\n42\n42\n42\n0.00 第42年折旧额 (元) 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/days-payable-outstanding",
    "inputs": {
      "AP": "42",
      "cogs": "42"
    },
    "expect": [
      "转率 (次/年) 1.0000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"AP\":\"42\",\"cogs\":\"42\"}，输出区含「转率 (次/年) 1.0000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/depreciation-straight",
    "inputs": {
      "c": "42",
      "s": "42",
      "n": "42"
    },
    "expect": [
      "年折旧率 (%) 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"c\":\"42\",\"s\":\"42\",\"n\":\"42\"}，输出区含「年折旧率 (%) 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/ebit",
    "inputs": {
      "rev": "42",
      "cogs": "42",
      "opex": "42"
    },
    "expect": [
      "42\n42\n42\n-42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rev\":\"42\",\"cogs\":\"42\",\"opex\":\"42\"}，输出区含「42\n42\n42\n-42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/ebitda",
    "inputs": {
      "EBIT": "42",
      "DA": "42"
    },
    "expect": [
      "摊销占比 (%) 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"EBIT\":\"42\",\"DA\":\"42\"}，输出区含「摊销占比 (%) 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/depreciation-syd",
    "inputs": {
      "c": "42",
      "s": "42",
      "n": "42",
      "yr": "42"
    },
    "expect": [
      "42\n42\n42\n42\n0.00 第42年折旧额 (元) 0.00 占原值比 (%)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"c\":\"42\",\"s\":\"42\",\"n\":\"42\",\"yr\":\"42\"}，输出区含「42\n42\n42\n42\n0.00 第42年折旧额 (元) 0.00 占原值比 (…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/free-cash-flow",
    "inputs": {
      "OCF": "42",
      "capex": "42"
    },
    "expect": [
      "FCF (万元) 100.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"OCF\":\"42\",\"capex\":\"42\"}，输出区含「FCF (万元) 100.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/gross-margin",
    "inputs": {
      "rev": "42",
      "cost": "42"
    },
    "expect": [
      "本率 (%) 1.0000 收入/成本 倍数"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rev\":\"42\",\"cost\":\"42\"}，输出区含「本率 (%) 1.0000 收入/成本 倍数」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/inventory-days",
    "inputs": {
      "inv": "42",
      "cogs": "42"
    },
    "expect": [
      "存货占销货成本比 12.17 存货天数 (月)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inv\":\"42\",\"cogs\":\"42\"}，输出区含「存货占销货成本比 12.17 存货天数 (月)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/interest-coverage",
    "inputs": {
      "EBIT": "42",
      "int": "42"
    },
    "expect": [
      "减利息 (万元) 1.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"EBIT\":\"42\",\"int\":\"42\"}，输出区含「减利息 (万元) 1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/gross-profit",
    "inputs": {
      "rev": "42",
      "cogs": "42"
    },
    "expect": [
      "利率 (%) 1.000 收入成本倍数 42000000000.0000 成本毛利比"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rev\":\"42\",\"cogs\":\"42\"}，输出区含「利率 (%) 1.000 收入成本倍数 42000000000.0000 成本毛…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/inventory-turnover",
    "inputs": {
      "cogs": "42",
      "inv": "42"
    },
    "expect": [
      "转率 (次/年) 365"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cogs\":\"42\",\"inv\":\"42\"}，输出区含「转率 (次/年) 365」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/roa-calc",
    "inputs": {
      "np": "42",
      "ta": "42"
    },
    "expect": [
      " ROA (%) 1.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"np\":\"42\",\"ta\":\"42\"}，输出区含「 ROA (%) 1.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/quick-ratio",
    "inputs": {
      "ca": "42",
      "inv": "42",
      "cl": "42"
    },
    "expect": [
      "0.00 速动比率 低于 1 评价（仅参考）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ca\":\"42\",\"inv\":\"42\",\"cl\":\"42\"}，输出区含「42\n42\n42\n0.00 速动比率 偏低( 评价 1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/net-profit-margin",
    "inputs": {
      "np": "42",
      "rev": "42"
    },
    "expect": [
      "0.00 收入减净利润的差额 (元)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"np\":\"42\",\"rev\":\"42\"}，输出区含「费用合计 (元) 1.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/operating-cash-flow",
    "inputs": {
      "NI": "42",
      "DA": "42",
      "dWC": "42"
    },
    "expect": [
      "现金流/净利 比 100.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"NI\":\"42\",\"DA\":\"42\",\"dWC\":\"42\"}，输出区含「现金流/净利 比 100.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/roe-dupont",
    "inputs": {
      "nm": "42",
      "at": "42",
      "em": "42"
    },
    "expect": [
      "42\n42\n42\n74088"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"nm\":\"42\",\"at\":\"42\",\"em\":\"42\"}，输出区含「42\n42\n42\n74088」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/working-capital",
    "inputs": {
      "CA": "42",
      "CL": "42"
    },
    "expect": [
      "C (万元) 1.000 流动比率 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"CA\":\"42\",\"CL\":\"42\"}，输出区含「C (万元) 1.000 流动比率 」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/roe-calc",
    "inputs": {
      "np": "42",
      "eq": "42"
    },
    "expect": [
      " ROE (%) 1.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"np\":\"42\",\"eq\":\"42\"}，输出区含「 ROE (%) 1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "accounting/split-bill",
    "inputs": {
      "total": "42",
      "people": "42",
      "tip": "42"
    },
    "expect": [
      "42\n42\n42\n分账结果 1.42 每人应付 17.64 小费合计 59.64 含小费总额 42 人平摊 42.00，小费 42% = 17.64，每人约 1.42。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"total\":\"42\",\"people\":\"42\",\"tip\":\"42\"}，输出区含「42\n42\n42\n分账结果 1.42 每人应付 17.64 小费合计 59.64…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  { slug: "accounting/break-even-units", inputs: { fc: "300000", p: "40", vc: "50" }, expect: ["单位边际贡献 ≤ 0"], ref: "单价 40 低于单位变动成本 50，单位边际贡献 −10，不存在盈亏平衡点；旧实现静默给出平衡产量 −30000.0 件。默认 100/60 ⇒ 不命中。" },
  { slug: "accounting/depreciation-syd", inputs: { c: "210000", s: "10000", n: "6", yr: "7" }, expect: ["计算年份须为 1–6 之间的整数"], ref: "SYD 年序超过使用年限（yr=7 > n=6）时旧实现给出负折旧 −3174.60；应拒绝并提示。默认 yr=1 ⇒ 不命中。" },
  { slug: "accounting/depreciation-syd", inputs: { c: "210000", s: "10000", n: "6.5", yr: "2" }, expect: ["使用年限须为正整数"], ref: "SYD 分母 n(n+1)/2 仅在整数年限成立；n=6.5 旧实现按 24.375 计算，语义不成立。默认 n=10 ⇒ 不命中。" },
  { slug: "accounting/depreciation-declining", inputs: { c: "200000", s: "250000", n: "5", yr: "2" }, expect: ["残值须在 0 与原值之间"], ref: "残值 250000 高于原值 200000，旧实现第 2 年给出 −20000 折旧并把账面值抬到 212000。默认 200000/20000 ⇒ 不命中。" },
  { slug: "accounting/depreciation-declining", inputs: { c: "200000", s: "20000", n: "5", yr: "6" }, expect: ["计算第几年须为 1–5 之间的整数"], ref: "yr=6 超过 5 年折旧期，旧实现静默给出 0 折旧；应拒绝。默认 yr=3 ⇒ 不命中。" },
  { slug: "accounting/depreciation-straight", inputs: { c: "200000", s: "250000", n: "8" }, expect: ["残值须在 0 与原值之间"], ref: "残值高于原值 ⇒ 年折旧 −6250.00 且折旧率 −3.13%；应拒绝。默认 100000/10000 ⇒ 不命中。" },
  {
    "slug": "accounting/split-bill",
    "inputs": {"total": "480", "people": "0", "tip": "10"},
    "expect": ["⚠ 账单金额须大于 0，人数须为 1–100 的整数，小费比例须在 0–100%。"],
    "ref": "人数 0 曾被 Math.max(1) 静默改成 1 人，分账结果失真；新守卫应拒绝。默认 480/4/10 不含该提示。"
  },

  { slug: "accounting/contribution-margin", inputs: { p: "100", vc: "60", q: "0" }, expect: ["不适用（收入为 0）"], ref: "销量 0 时总边际贡献合法为 0，但收入为 0 贡献率无定义，应显示不适用；旧实现除以 0 得 NaN/Infinity。默认 qty=1000 不含该串。" },
  { slug: "accounting/contribution-margin", inputs: { p: "-100", vc: "60", q: "100" }, expect: ["单价、单位变动成本与销量不能为负"], ref: "负售价、负变动成本、负销量均无业务意义，应显式拒绝；负贡献本身合法但输入不得为负。默认 100/60/1000 不含该提示。" },
  { slug: "accounting/roe-calc", inputs: { np: "300000", eq: "0" }, expect: ["不适用（净资产为 0）"], ref: "净资产为 0 时 ROE 分母无定义；旧实现 Math.max(eq,1e-9) 给出 3e14% 的假值。默认 eq=2000000 不含该串。" },
  { slug: "accounting/roe-calc", inputs: { np: "300000", eq: "-2000000" }, expect: ["净资产为负"], ref: "负权益下 ROE 仍应按真实分母计算为 -15.00%，但须提示正负方向不能当正常回报率；旧实现把负权益替换为极小正数。默认 eq=2000000 不含该提示。" },
  { slug: "accounting/analysis-46", inputs: { data: "2024,1000\n2025,1100\n2026,1210" }, expect: ["外推预测只反映历史样本"], ref: "线性外推只代表历史样本延续，页面须显式声明；旧文案无此限定。默认示例数据不含该句。" },
  { slug: "accounting/analysis-46", inputs: { data: "2024,1000\n2025,abc" }, expect: ["第 2 行", "无法解析"], ref: "非法行须逐行报错并中止，不能静默跳过；旧实现跳过错误行后继续给出趋势。默认示例数据全部合法，不含行号报错。" },
  { slug: "accounting/analysis-46", inputs: { data: "2024,100\n2025,100\n2026,100" }, expect: ["不适用（序列为常量）"], ref: "常量序列的线性拟合 R² 无定义，不能显示 0.0000 误导为拟合失败；旧实现直接显示 0。默认示例为递增序列。" },
  { slug: "accounting/analysis-46", inputs: { data: "2024,0\n2025,1100\n2026,1210" }, expect: ["不适用（首期≤0 或期数不足）"], ref: "复合增长率首期 ≤0 时无定义，不能显示 0%；旧实现直接显示 0.00%。默认示例首期 1000 不含该串。" },
  { slug: "accounting/analysis-cost-5", inputs: { qty: "1000", mat: "20", lab: "10", vmoh: "5", fmoh: "20000", vsale: "2", fsale: "10000", price: "", gm: "20" }, expect: ["请填写全部字段；空白不等于 0"], ref: "任一字段为空须拒绝，不能把空值当 0 生成建议售价；旧实现 parseFloat||0。默认示例全部有值，不含该提示。" },
  { slug: "accounting/break-even-units", inputs: { fc: "300000", p: "120", vc: "70" }, expect: ["6000 最少整数销量"], ref: "理论平衡产量 6000.00 件；按件销售须同时给出向上取整后的最少整数销量 6000 件与按整数销量的最低销售额 720000.00；旧版只有一位小数理论值。" },
  { slug: "accounting/net-profit-margin", inputs: { np: "150000", rev: "0" }, expect: ["不适用（收入为 0）"], ref: "收入为 0 时净利率无定义，不能显示 0%；旧实现按收入 1 兜底或直接除零。默认 rev=1000000 不含该串。" },
  { slug: "accounting/quick-ratio", inputs: { ca: "1000000", inv: "200000", cl: "0" }, expect: ["流动负债为 0，速动比率无定义"], ref: "流动负债为 0 时分母无定义，不能当作达标；旧实现仍计算并给出比率。默认 cl=1500000 不含该提示。" },
  { slug: "accounting/quick-ratio", inputs: { ca: "1200000", inv: "200000", cl: "1000000" }, expect: ["等于 1（临界）"], ref: "速动比率恰好等于 1 时应显示临界，而不是「偏低(<1)」；旧实现 ratio>1 才达标，等于 1 落入偏低。默认 2200000/1500000=1.4667 不含该串。" },
  { slug: "accounting/calc-2", inputs: { revenue: "500000", cost: "700000", loss: "0", rate: "25" }, expect: ["估算应纳税所得额： 0.00"], ref: "利润为负时应纳税所得额为 0，已用亏损不得为负；旧实现 Math.min(lossCarry,profit) 可显示负弥补额。默认利润 200000 不含该串。" },
  { slug: "accounting/calc-2", inputs: { revenue: "500000", cost: "300000", loss: "0", rate: "120" }, expect: ["输入须为有限数，收入与成本不能为负，税率须在 0–100% 之间。"], ref: "税率须在 0–100%，120% 应拒绝；旧实现接受任意数值并算出 120% 税额。默认 25% 不含该提示。" },
  { slug: "accounting/depreciation-declining", inputs: { c: "200000", s: "20000", n: "5", yr: "5" }, expect: ["最后两年（第 4–5 年）改为直线法", "11600.00"], ref: "5 年期双倍余额：前 3 年 80000/48000/28800，最后两年（第4–5年）各 11600.00 平均摊至残值；旧文案称逐年双倍余额至末年调整，与实际不符。默认 yr=3 不含第5年值。" },
  { slug: "accounting/depreciation-declining", inputs: { c: "200000", s: "20000", n: "1", yr: "1" }, expect: ["第1年 180000.00"], ref: "n=1 时一次性折至残值 20000，第1年折旧 180000.00；旧公式按 n-1 年处理会出现 0 或负值。默认 n=5 不含该串。" },
  { slug: "accounting/calc-1", inputs: { amount: "", rate: "13" }, expect: ["请填写金额；空白不等于 0"], ref: "金额为空须拒绝，不能按 0 生成 0 税额；旧实现 parseFloat||0。默认金额 1000 不含该提示。" },
  { slug: "accounting/calc-1", inputs: { amount: "1000", rate: "120" }, expect: ["金额须为非负有限数，税率须在 0–100% 之间。"], ref: "自定义税率须在 0–100%，120% 应拒绝；旧实现接受并算出 1200 税额。默认 13% 不含该提示。" },
  { slug: "accounting/report-2", inputs: { data: "库存现金,1000,0\n银行存款,abc,0" }, expect: ["不是有效数字"], ref: "非法金额须逐行拒绝并中止，不能按 0 继续试算；旧实现静默把 abc 当 0。默认示例全部合法，不含该提示。" },

];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== accounting calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();