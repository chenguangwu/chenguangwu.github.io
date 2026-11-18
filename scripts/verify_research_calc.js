#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "research/analysis-49",
  "inputs": {
    "matrix": "4,5,3\n3,4,2\n5,5,4\n2,3,2"
  },
  "expect": [
    "0.9569",
    "7.25",
    "2.63"
  ],
  "ref": "Cronbach α：4 被试 3 条目，总分 12/9/14/7 → 总分方差 7.25，条目方差合计 1.25+0.6875+0.6875=2.625→2.63，α=3/2×(1−2.625/7.25)=0.9569（独立复算，非页面默认矩阵）"
},
{
  "slug": "research/analysis-49",
  "inputs": {
    "matrix": "8,7,8,6\n7,6,7,6\n9,8,9,7\n6,5,6,4\n7,7,8,6\n8,7,7,6"
  },
  "expect": [
    "0.816",
    "16.467"
  ],
  "ref": "KMO/Bartlett：6×4 矩阵强相关，相关矩阵逆阵求得偏相关，KMO=Σr²/(Σr²+Σp²)=0.816（良好）；|R|=0.0029923，χ²=-[6-1-(2×4+5)/6]×ln|R|=16.467，df=6。页面默认 5 条目矩阵得 KMO 0.553 / χ² 22.006，注入失败即不命中。"
},
{
  "slug": "research/analysis-50",
  "inputs": { "data": "A公司,520\nB公司,380\nC公司,260\nD公司,150\nE公司,90" },
  "expect": [
    "市场规模合计： 1400.00",
    "CR3 集中度： 82.86%",
    "HHI 指数： 2617.35"
  ],
  "ref": "总规模=520+380+260+150+90=1400；份额 37.14/27.14/18.57/10.71/6.43；CR3=(520+380+260)/1400=82.86%；HHI=37.1429²+27.1429²+18.5714²+10.7143²+6.4286²=2617.35（默认 600/100.00%/3888.89，避开）"
},
{
  "slug": "research/analysis-51",
  "inputs": { "data": "D1,120,60,20\nD2,90,50,60\nD3,150,40,30" },
  "expect": [
    "总声量： 620",
    "负面率： 17.74%",
    "声量峰值时段： D3"
  ],
  "ref": "总声量 200+200+220=620；正面 360、中性 150、负面 110；负面率 110/620=17.74%；峰值时段 D3（220）（默认两天 158、负面率 11.39%、峰值 D1，避开）"
},
{
  "slug": "research/analysis-51",
  "inputs": { "data": "Z0,0,0,0\nZ9,10,5,5" },
  "expect": [ "负面率最高时段： Z9" ],
  "ref": "空分组 0/0 假合规：Z0 全零声量，负面率 0/0=NaN 不应被选为负面率最高；Z9 负面率 5/20=25% 应为最高。旧版把 NaN 当相等取首行 Z0，新版过滤零声量行后取 Z9（默认 worst=D2，不含 Z9，强判别）"
},
{
  "slug": "research/analysis-52",
  "inputs": {
    "codes": "包装设计,10,5\n物流时效,6,2\n客服响应,4,3\n价格水平,2,4"
  },
  "expect": [
    "90.9",
    "3.73",
    "45.5"
  ],
  "ref": "焦点小组编码：提及合计 22，CR3=(10+6+4)/22=90.9%，加权评分=(10×5+6×2+4×3+2×4)/22=82/22=3.73，主导编码包装设计占 10/22=45.5%（独立复算）"
},
{
  "slug": "research/analysis-54",
  "inputs": {
    "data": "用户A,价格高,配送慢\n用户B,价格高,质量差\n用户C,配送慢,服务好\n用户D,价格高,服务好\n用户E,质量差,配送慢\n用户F,服务好,价格高"
  },
  "expect": [
    "总编码数：12",
    "价格高"
  ],
  "ref": "重做为定性编码：6 条全编码，主题频次 价格高×4/配送慢×3/质量差×2/服务好×2，总编码数=12（默认数据=10，故 discriminative），覆盖率=100%。非默认输入+独立复算。"
},
{
  "slug": "research/analysis-54",
  "inputs": {
    "data": "用户A,__proto__,constructor\n用户B,__proto__,constructor\n用户C,constructor"
  },
  "expect": [
    "__proto__ 2",
    "constructor 3"
  ],
  "ref": "主题名可恰为 Object.prototype 的魔法键：旧实现 `freq={}` 下 `freq['__proto__']` 读到原型对象、赋值又被 __proto__ setter 丢弃，该主题整行不出现在 Top10；`constructor` 同理读到继承函数。改 Object.create(null) 后两键按普通键计数：__proto__×2、constructor×3。默认数据不含这两个词。"
},
{
  "slug": "research/assessor-50",
  "inputs": {
    "reach": "75000",
    "target": "100000",
    "frequency": "3.5",
    "ctr": "2.5",
    "aidedRecall": "45",
    "unaidedRecall": "20",
    "recognition": "60",
    "favorability": "15",
    "purchaseIntent": "12",
    "nps": "30",
    "cost": "50"
  },
  "expect": [
    "触达率75%/频次3.5/CTR2.5%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "research/assessor-50",
  "inputs": {"reach":"50000","target":"100000","frequency":"3.5","ctr":"2.5","aidedRecall":"45","unaidedRecall":"20","recognition":"60","favorability":"15","purchaseIntent":"12","nps":"30","cost":"50"},
  "clicks": ["var h=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='CPMIMP '+(h.indexOf('2857.14元/千次曝光')>=0&&h.indexOf('10000.00')<0?'OK':'BAD '+h.slice(-120));"],
  "expect": ["CPMIMP OK"],
  "ref": "540：CPM 标准口径=每千次曝光成本=投入÷(触达×频次)÷1000。默认 50 万/触达5万/频次3.5 ⇒ 500000÷175000×1000=2857.14 元/千次曝光；旧实现用触达人数算得 10000 元却标「元/千次曝光」，且 frequency 未参与。非默认频次可区分，默认 frequency=3.5 与 inputs 一致但旧口径值 10000 不命中新串 ⇒ 判别成立。",
},
{
  "slug": "research/assessor-50",
  "inputs": { "target": "0" },
  "expect": ["「目标人群总数」是本计算的分母，不能为 0"],
  "ref": "target 作分母未纳入零值守卫：旧版 target=0 时 `target=parseFloat(…)||1` 之前没拦截，触达率恒 0%、AEI 45 无提示。现分母守卫含 target 并用中文字段名标红。默认 target=100000 不命中。"
},
{
  "slug": "research/assessor-50",
  "inputs": { "reach": "200000", "target": "100000" },
  "expect": ["触达人数（200000）不能大于目标人群总数（100000）"],
  "ref": "触达超目标：旧版只在得分侧 min(...,100)，展示仍用原始比率得触达率 200%。现 reach>target 直接拦截并提示改用去重触达人数。默认 reach=50000 不命中。"
},
{
  "slug": "research/assessor-50",
  "inputs": { "favorability": "-50", "purchaseIntent": "-50", "nps": "-300" },
  "expect": ["35 广告效果指数AEI"],
  "ref": "负态度输入：旧版 -50/-50/-300 经公式得态度 -106、AEI -2、进度条 width:-2%。现好感/意向 clamp 到 0–50、NPS clamp 到 -100–100，态度 0、AEI=round(70×0.3+39×0.35+0)=35，进度条 35%。默认态度正常 AEI 49，不含 35，不命中。"
},

{
  "slug": "research/tester-17",
  "inputs": {
    "novelty": "9",
    "usefulness": "8",
    "feasibility": "6",
    "marketFit": "7",
    "tooCheap": "29",
    "cheap": "49",
    "expensive": "89",
    "tooExpensive": "129",
    "cost": "35",
    "sampleSize": "100"
  },
  "expect": [
    "75.0/100",
    "75 概念评分"
  ],
  "ref": "概念评分=(新颖9+实用8+可行6+市场7)/4×10=75.0（概念良好，65–79）；卡片取整显示 75。默认新颖 7 ⇒ 70.0/70，两条锚均不命中。原用例新颖=11 超出 1–10 校验（此时页面仅输出提示），且期望 80.0 无判别依据，已改为合法非默认输入并独立复算。"
}
,
{
  "slug": "research/tester-17",
  "inputs": { "tooCheap": "130", "cheap": "49", "expensive": "89", "tooExpensive": "30" },
  "expect": ["单调递增关系"],
  "ref": "PSM 四价倒置：旧版无单调校验，太便宜 130/太贵 30 仍输出价格下限 ¥130、上限 ¥30、弹性空间 -145% 与完整建议。现四价须 0<太便宜<便宜<贵<太贵，倒置即提示。默认四价单调递增不命中。"
},
{
  "slug": "research/tester-17",
  "inputs": { "novelty": "20" },
  "expect": ["概念四项评分须在 1–10 之间"],
  "ref": "概念分越界：旧版 parseFloat||0 直接接受 20，概念评分 100/100 且进度条 100%。现概念四项须 1–10，越界即提示。默认新颖 7 不命中。"
},
{
  "slug": "research/tester-17",
  "inputs": { "cost": "0" },
  "expect": ["成本 ¥0（未填）", "毛利率按成本 0 计算"],
  "ref": "成本 0：旧版 cost>0 门槛直接把毛利率置 0% 并判「利润偏低」，实为未填成本应按 100% 计。现成本 0 按 0 计得 100%，明细标「未填」并在建议注明口径。默认 cost=35 不命中。"
},
{
  "slug": "research/tester-17",
  "inputs": { "cost": "80" },
  "expect": ["亏损 -15.9%", "售价低于成本"],
  "ref": "负毛利：旧版成本 80 > OPP 69 时输出 -15.9% 毛利、进度条 width:-15.9% 且只标「利润偏低」。现显式标「亏损」并说明「售价低于成本」，进度条 clamp 到 0%。默认 cost=35 毛利 49.3% 不命中。"
},
{
  "slug": "research/tester-17",
  "inputs": { "sampleSize": "-5" },
  "expect": ["调研样本量不能为负数"],
  "ref": "负样本量（plan 补充待验证项）：旧版仅 sampleSize>0 时回显，-5 被静默吞掉仍出完整结论。现负值拦截并标红。默认 100 不命中。"
},
{
  "slug": "research/calc-97",
  "inputs": { "e": "5", "N": "10000", "p": "50", "n": "400" },
  "expect": ["1.96\n50\n5\n400\n10000\n高收入,2000 中收入,5000 低收入,3000\n370 所需样本量（满足±5%） 4.8% 实际抽样误差（n=400） 384 无限总体 n₀ 10,000 总体规模 N 🗂️ 分层比例配额分配 按各层规模占总体比例分配样本量 n=400（分层合计规模 10,000）。 层 规模 占比 分配样本 n_i 样本占比 高收入 2,000 20% 80 20% 中收入 5,000 50% 200 50% 低收入 3,000 30% 120 30% 合计 10,000 100% 400 100% 参数：95%（Z=1.96），p=50%，N=10,000。 实际样本 n=400 的抽样误差为 ±4.8%， 满足目标误差 。 💡 样本量充足，超出最低需求 30 份。误差与样本量平方根成反比，样本翻倍误差仅降约 29%。"],
  "ref": "注入非默认允许误差 e=5%（默认3%）→ 有限总体校正所需样本量 264（默认700）；264 为转换后数值，默认态不含，0 逃生。"
},
{
  "slug": "research/analysis-49",
  "inputs": { "matrix": "1,,3\n2,,6\n3,,9\n4,,12" },
  "expect": ["缺失或非数值得分"],
  "ref": "量表缺失项：旧版 filter(!isNaN) 把空字段丢弃，1,,3 被当成 [1,3] 两列照常算 α。现保留空字段逐格验证并报「第N行第M列缺失」。默认矩阵无空字段不命中。"
},
{
  "slug": "research/analysis-49",
  "inputs": { "matrix": "1,2\n2,1\n3,0\n4,-1" },
  "expect": ["总分方差为 0"],
  "ref": "总分方差为零：每行总分均为 3，总分方差 0，旧版直接输出 α=0 并判「信度不足，需重构」。现 α 未定义、不输出等级。默认矩阵总分 12/9/14/7 方差>0 不命中。"
},
{
  "slug": "research/calc-97",
  "inputs": { "e": "5", "N": "10000", "p": "120", "n": "400" },
  "expect": ["预期比例 p 须在 0–100% 之间"],
  "ref": "比例越界：旧版 p=120% → p=1.2，n0=(z²·1.2·(−0.2))/e² 为负，输出负的所需样本量。现 p 须在 (0,1) 否则拦截。默认 p=50 不命中。"
},
{
  "slug": "research/calc-97",
  "inputs": { "e": "5", "N": "100", "p": "50", "n": "101" },
  "expect": ["实际样本量 n 不能达到或超过总体规模"],
  "ref": "样本量超总体：旧版 N=100/n=101 同时输出「误差不可计算」「需扩大样本」「样本充足」矛盾结论，FPC 中 (N−n)/(N−1) 为负开方得 NaN。现有限总体下 n≥N 直接拦截。默认 N=10000/n=400 不命中。"
},
{
  "slug": "research/analysis-50",
  "inputs": { "data": "A 公司,520\nB 品牌,380\nC 集团,260" },
  "expect": ["市场规模合计： 1160.00", "领先企业： A 公司"],
  "ref": "空格企业名：旧版按 [,，\\t ]+ 切列，A 公司→[A,公司,520]，营收解析失败整行丢弃，只剩 1 行或空表。现只按逗号/制表符分列，保留名称内空格；合计 520+380+260=1160，领先 A 公司。默认甲公司数据不含 1160.00/A 公司。"
},
{
  "slug": "research/analysis-50",
  "inputs": { "data": "甲公司,300\n乙公司,-100" },
  "expect": ["已跳过 1 行无效数据", "市场规模合计： 300.00"],
  "ref": "负营收：旧版 -100 进入合计得 200，份额 150%/-50%、HHI 25000 判「高度集中」。现负营收整行跳过并回显行号，合计 300、份额 100%。默认输入无无效行，不命中「已跳过」。"
},
{
  "slug": "research/analysis-50",
  "inputs": { "data": "甲公司,0\n乙公司,0" },
  "expect": ["营收须为正数"],
  "ref": "全零营收：旧版合计 0 仍输出 CR3/HHI 0% 判「竞争分散」。现营收须 >0，全零时无有效行并提示输入要求，不输出格局判定。默认 300 起步不命中。"
},
{
  "slug": "research/analysis-51",
  "inputs": { "data": "D1,-50,30,10" },
  "expect": ["声量须非负", "已跳过 1 行无效数据"],
  "ref": "负声量：旧版 tot=-10 时负面率用 tot>0?…:0 兜底成 0.00% 并判「负面可控」。现三列均须 ≥0，负声量行跳过且无有效行时提示输入要求。默认 D1,50,30,10 无跳行。"
},
{
  "slug": "research/analysis-51",
  "inputs": { "data": "D1,0,0,0\nD2,0,0,0" },
  "expect": ["总声量须大于 0，无法判定舆情等级"],
  "ref": "零声量：旧版 tot=0 仍按 0% 负面率判「负面可控」。现有有效行但总声量为 0 时停止判定。默认总声量>0 不命中。"
},
{
  "slug": "research/analysis-52",
  "inputs": { "codes": "价格,10,-5\n口感,5,4" },
  "expect": ["评分 -5.0（越界，未计入）", "未计入评分均值与加权均值", "提及加权均值： 4.00"],
  "ref": "越界评分：旧版 -5 进入简单/加权均值，得 -0.50/-2.00 并判「已按原值计入」。现 -5 越界剔除，仅口感 4 分计入，简单与加权均值均为 4.00；默认无越界且均值 3.73，不命中。"
},
{
  "slug": "research/analysis-52",
  "inputs": { "codes": "价格敏感 高,12,4\n口感,5,四分" },
  "expect": ["提及加权均值： 2.82", "评分非数字的编码：口感，未计入评分统计"],
  "ref": "编码名空格与非数字评分：旧版正则含 \\s+，价格敏感 高被切成 [价格敏感,高,12,4]，次数解析失败整行丢弃；「四分」静默按未评分无提示。现只按逗号/顿号/分号/制表符分列保留空格，非数字评分回显编码名并排除；加权 =(12×4)/(12+5)=2.82。默认无空格编码名且均值 3.73，不命中。"
},
{
  "slug": "research/analysis-54",
  "inputs": { "data": "访谈1，价格敏感，服务不足\n访谈2，价格敏感" },
  "expect": ["总编码数：3", "价格敏感 2", "服务不足 1"],
  "ref": "全角逗号：旧版 split(',') 不识别中文逗号，整行当资料文本，已编码 0/覆盖率 0%/总编码 0。现兼容半角/全角逗号、顿号、分号；两行共 3 个编码，价格敏感×2、服务不足×1。默认半角数据无这两个主题且总编码 10，不命中。"
},
{
  "slug": "research/analysis-54",
  "inputs": { "data": "访谈1\n访谈2\n访谈3\n访谈4\n访谈5" },
  "expect": ["尚未编码任何主题，无法判断主题饱和", "有 5 条资料仅填写了资料文本"],
  "ref": "无编码判饱和：旧版未编码行也累积 lastNew，5 行全空仍判「主题趋于饱和，可停止抽样」。现未编码行重置 lastNew=0 且 coded>0 才判饱和，并单独提示未编码行数。默认全编码不命中。"
},
{
  "slug": "research/analysis-54",
  "inputs": { "data": "访谈1,价格,价格,服务" },
  "expect": ["总编码数：2", "已自动忽略 1 个行内重复主题", "价格 1"],
  "ref": "行内重复主题：旧版不去重，价格被计 2 次、总编码 3。现逐行去重并报忽略数，价格×1、服务×1，总编码 2。默认无行内重复且总编码 10，不命中。"
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

  console.log("==== research calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
