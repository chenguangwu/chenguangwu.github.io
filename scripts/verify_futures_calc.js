#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "futures/futures-pricing",
  "inputs": {
    "spot": "7500",
    "rate": "4",
    "time": "0.25",
    "yield": "1",
    "storage": "0.5",
    "actualFuture": "5075"
  },
  "expect": [
    "565.91"
  ],
  "ref": "auto-restore"
},
{
  "slug": "futures/hedge-ratio",
  "inputs": {
    "sigmaS": "6",
    "sigmaF": "3.5",
    "rho": "0.85",
    "spotValue": "1000000",
    "futurePrice": "3800",
    "futureMult": "300"
  },
  "expect": [
    "1.4571"
  ],
  "ref": "auto-restore"
},
{
  clicks: ["calc()"],
  "slug": "futures/margin-calc",
  "inputs": {
    "price": "5700",
    "multiplier": "300",
    "marginRate": "12",
    "capital": "200000",
    "lots": "0",
    "fee": "10"
  },
  "expect": [ "205,200 每手保证金" ],
  "ref": "auto-restore"
},
{
  "slug": "futures/option-greeks",
  "inputs": {
    "spot": "150",
    "strike": "100",
    "rate": "3",
    "vol": "20",
    "time": "0.5",
    "div": "0"
  },
  "expect": [
    "51.4960"
  ],
  "ref": "auto-restore"
},
{
  "slug": "futures/option-greeks",
  "inputs": {
    "spot": "100",
    "strike": "100",
    "rate": "3",
    "vol": "20",
    "time": "0.5",
    "div": "0",
    "marketPrice": "6.371"
  },
  "expect": [
    "隐含波动率 IV: 20.00%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "futures/option-payoff",
  "inputs": {
    "strike": "150",
    "premium": "5"
  },
  "expect": [
    "145.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "futures/futures-pricing",
  "inputs": { "spot": "5000", "rate": "", "time": "0.25", "yield": "1", "storage": "0.5" },
  "expect": ["请填写现货价格、无风险利率、到期时间、便利收益率和存储成本率"],
  "ref": "第1063批：清空无风险利率不得按 0 继续给出理论价，必须提示并清空结果。"
},
{
  "slug": "futures/futures-pricing",
  "inputs": { "spot": "5000", "rate": "0", "time": "0.25", "yield": "1", "storage": "0.5" },
  "expect": ["4,993.75"],
  "ref": "第1063批：合法零利率仍应正常计算；连续复利 F=5000×e^((0+0.5%-1%)×0.25)=4993.75，与空值错误路径区分。"
},
{
  "slug": "futures/hedge-ratio",
  "inputs": { "sigmaS": "6", "sigmaF": "3.5", "rho": "", "spotValue": "1000000", "futurePrice": "3800", "futureMult": "300" },
  "expect": ["请填写现货标准差、期货标准差、相关系数"],
  "ref": "第1063批：清空相关系数不得按 0 生成零对冲结果，必须提示并清空结果。"
},
{
  clicks: ["calc()"],
  "slug": "futures/margin-calc",
  "inputs": { "price": "", "multiplier": "300", "marginRate": "12", "capital": "200000", "lots": "0", "fee": "10" },
  "expect": ["请填写价格、合约乘数、保证金比例和资金"],
  "ref": "第1063批：清空价格不得按 0 生成零保证金结果，必须提示并清空结果。"
},
{
  "slug": "futures/option-greeks",
  "inputs": { "spot": "100", "strike": "100", "rate": "3", "vol": "20", "time": "0.5", "div": "" },
  "expect": ["请填写标的价格、行权价、无风险利率、波动率、到期时间和股息率"],
  "ref": "第1063批：清空股息率不得按 0 继续定价，必须提示并清空 Greeks。"
},
{
  "slug": "futures/option-payoff",
  "inputs": { "strike": "150", "premium": "" },
  "expect": ["请输入有效的行权价和权利金；数值不能为空"],
  "ref": "第1063批：清空权利金不得按零成本出盈亏，必须提示并清空结果。"
},
{
  "slug": "futures/option-payoff",
  "inputs": { "strike": "150", "premium": "0" },
  "expect": ["150.00"],
  "ref": "第1063批：权利金合法零仍应计算，盈亏平衡点=150；与空值错误路径区分。"
},
  {
    "slug": "futures/option-greeks",
    "inputs": {"spot":"100","strike":"100","rate":"3","vol":"20","time":"0.5","div":"0","marketPrice":"6.371"},
    "clicks": ["var sp=document.getElementById('spot');sp.value='90';calc();"],
    "expect": ["隐含波动率 IV: 37.97%"],
    "ref": "IV 依赖现价/行权价/利率/期限/股息，任一变化后 calc() 必须重算 IV；现价改 90 后 IV 由约 15.06% 变为 37.97%。"
  },
  {
    "slug": "futures/option-greeks",
    "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/futures/option-greeks.html','utf8');document.getElementById('__tbProbe').textContent='REL:'+((h.indexOf('option-payoff.html')>=0&&h.indexOf('margin-calc.html')>=0&&h.indexOf('hedge-ratio.html')>=0&&h.indexOf('text-reverse-words')<0)?'OK':'BAD');"],
    "expect": ["REL:OK"],
    "ref": "相关推荐改为同目录期权损益、保证金、对冲比例与期货定价，移除单词反转/字数统计等无关文本工具。"
  },
  {
    "slug": "futures/option-payoff",
    "inputs": {"strike":"100","premium":"120"},
    "clicks": ["var ps=payoffSummary('put','buy',100,120);document.getElementById('__tbProbe').textContent='PUT120:'+((ps.maxProfitText==='无正收益'&&ps.bepText.indexOf('不可达')>=0)?'OK':'BAD');"],
    "expect": ["PUT120:OK"],
    "ref": "看跌 K=100、p=120：S=0 时最高损益 -20，任何 S≥0 都不能盈利，BEP=-20 不可达；不能再显示“最大盈利 -20”或负价格平衡点。"
  },
  {
    "slug": "futures/option-payoff",
    "inputs": {"strike":"100","premium":"100"},
    "clicks": ["var ps2=payoffSummary('put','buy',100,100);document.getElementById('__tbProbe').textContent='PUT100:'+(ps2.bepText.indexOf('0（仅 S=0 边界）')>=0?'OK':'BAD');"],
    "expect": ["PUT100:OK"],
    "ref": "p=K 边界：BEP=0 只在 S=0 成立，正价格下无盈利；标记为边界而非可交易平衡点。"
  },
  {
    "slug": "futures/hedge-ratio",
    "inputs": {"sigmaS":"3","sigmaF":"3.5","rho":"-0.85","spotValue":"1000000","futurePrice":"3800","futureMult":"300"},
    "expect": ["-0.7286","所选方向可执行手数 = 0 手","相关系数为负"],
    "ref": "负相关时 h*=-0.7286，按所选卖出方向不可执行；不得显示 -1 手并给正覆盖，需提示反向约 2 手。"
  },
  {
    "slug": "futures/hedge-ratio",
    "inputs": {"sigmaS":"6","sigmaF":"3.5","rho":"0.85","spotValue":"1000000","futurePrice":"3800","futureMult":"300"},
    "expect": ["理论覆盖率 h* = 145.7%","整数手数实际覆盖 = 114.0%"],
    "ref": "理论 h*=1.4571（145.7%），整数 1 手覆盖 1,140,000/1,000,000=114.0%；理论效果与整数执行分开显示。"
  },
  {
  clicks: ["calc()"],
    "slug": "futures/margin-calc",
    "inputs": {"price":"1000","multiplier":"1","marginRate":"100","capital":"1000","lots":"","fee":"10"},
    "expect": ["最大可开仓（含手续费）","0 手","每手占用现金 = 保证金 1,000 + 手续费 10"],
    "ref": "资金 1000、每手保证金 1000、手续费 10：计入手续费后最多 0 手，不能显示 1 手后剩余 -10。"
  },
  {
  clicks: ["calc()"],
    "slug": "futures/margin-calc",
    "inputs": {"price":"3800","multiplier":"300","marginRate":"12","capital":"200000","lots":"0","fee":"10"},
    "expect": ["最大可开仓（含手续费）","最大可开仓手数 = 200,000 ÷ 136,810 = 1 手","当前手数为 0 或留空"],
    "ref": "零手必须按未开仓处理，不再被替换为满仓；最大 1 手按 136,810 元/手（含 10 元手续费）计算。"
  },
  {
  clicks: ["calc()"],
    "slug": "futures/margin-calc",
    "inputs": {"price":"3800","multiplier":"300","marginRate":"12","capital":"200000","lots":"1.5","fee":"10"},
    "expect": ["手数须为非负整数"],
    "ref": "1.5 手不是可交易手数，必须拒绝而不是静默向下取整或替换为最大手数。"
  },
  {
    "slug": "futures/futures-pricing",
    "inputs": {"spot":"5000","rate":"4","time":"0.25","yield":"1","storage":"0.5","actualFuture":"5100"},
    "expect": ["实际价 - 理论价","实际价高于理论价","卖出期货、买入现货"],
    "ref": "diff=实际-理论=+56.08；标签与方向必须一致，旧版把 +差额解释成实际价低于理论价。"
  },
  {
    "slug": "futures/futures-pricing",
    "inputs": {"spot":"5000","rate":"4","time":"0.25","yield":"1","storage":"0.5","actualFuture":"5000"},
    "expect": ["实际价 - 理论价","实际价低于理论价","买入期货、卖出现货"],
    "ref": "实际 5000 < 理论 5043.90，diff 为负；应提示实际价低于理论价，并明确仅模型价差、未计交易成本。"
  },
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

  console.log("==== futures calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
