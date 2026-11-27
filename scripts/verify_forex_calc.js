#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "forex/cross-rate",
  "inputs": {
    "baseUsd": "4.085",
    "quoteUsd": "0.00665",
    "amount": "1000"
  },
  "expect": [
    "614.2857"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forex/leverage-calc",
  "inputs": {
    "lots": "4",
    "baseUsdRate": "1",
    "balance": "10000",
    "stopOut": "50"
  },
  "expect": ["2.00% 距强平波动", "强平净值 = 已用保证金 $4,000.00 × 50% = $2,000.00", "可承受亏损 = 账户余额 $10,000 - 强平净值 $2,000.00 = $8,000.00", "价格反向波动 2.00% 触发强平"],
  "ref": "auto-restore"
},
{
  "slug": "forex/lot-size",
  "inputs": { "balance": "50000", "riskPct": "1", "stopPips": "30", "pair": "USDJPY" },
  "expect": ["2.50 建议手数", "$500 风险金额", "盈亏比 = 100 ÷ 30"],
  "ref": "注入非默认（默认 balance=10000 / riskPct=2 / stopPips=50 / pair=EURUSD）：风险金额 = 50000×1% = $500；USD/JPY 的 pip=0.01、报价货币 USD 汇率 150（option 的 data 值）⇒ 每手每点 = 100000×0.01÷150 = $6.6667；每手止损 = 30×6.6667 = $200 ⇒ 手数 = 500÷200 = 2.50；盈亏比 = 止盈 100 ÷ 止损 30 = 3.33。默认态 0.40 手 / $200 / 2.00，三串均不出现。⚠ 该页此前因 `selectedOptions[0].dataset.pip` 未建模而整页初始化失败，harness 补 mkOpt 后可读数。"
},
{
  "slug": "forex/pip-calc",
  "inputs": { "pair": "USDJPY", "lotSize": "1", "pips": "80", "accountCcy": "CNY" },
  "expect": ["¥48.33 每点价值", "波动80点盈亏 = +¥3,866.67"],
  "ref": "注入非默认（默认 EURUSD / 0.01 手 / 50 点 / USD）：合约单位 = 1×100000 = 100,000 USD；USD/JPY 的 1 点 = 0.01 ⇒ 点值 = 100000×0.01 = 1,000 JPY ⇒ ÷150 = $6.67 ⇒ ×7.25（CNY 账户汇率）= ¥48.33；80 点盈亏 = 48.33×80 = +¥3,866.67。默认态 $0.10 / 1,000 合约 / +$5.00，两串均不出现。"
},
{
  "slug": "forex/spread-cost",
  "inputs": { "pair": "GBPUSD", "lots": "3", "days": "2" },
  "expect": ["$60.00 点差成本", "总交易成本 = $60.00 + $21.00 + $21.00 = $102.00"],
  "ref": "注入非默认（默认 EURUSD / lots=1 / days=0）：⚠ 选 pair 会联动改写 ask/bid（GBP/USD 的 data 报价 1.2752/1.275）⇒ 不手工注入 ask/bid（注入也会被覆盖，真机同样）。点差 = 0.00020 ⇒ 2.0 点；每手每点 = 100000×0.0001÷1 = $10 ⇒ 点差成本 = 3×2.0×10 = $60.00；佣金 = 3×7 = $21.00；隔夜现金流 = 3×(−3.5)×2 = −$21.00（付出），隔夜成本 = +$21.00 ⇒ 总成本 = 60+21+21 = $102.00。默认态点差成本 $20.00 / 总成本 $27.00，两串均不出现。"
},
{ slug:"forex/pip-calc", inputs:{"rate":"","quoteUsdRate":"","pips":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{
  "slug": "forex/pip-calc",
  "inputs": { "pair": "USDCHF", "lotSize": "1", "pips": "10", "accountCcy": "USD", "quoteUsdRate": "0.885" },
  "expect": ["$11.30 每点价值", "波动10点盈亏 = +$112.99"],
  "ref": "第1064批：USD/CHF 报价货币 CHF，1 手 1 点=10 CHF，按 1 USD=0.885 CHF 换算为 $11.30；10 点 $112.99。旧默认 1.13 会得到 $8.85，方向不一致。"
},
{
  "slug": "forex/lot-size",
  "inputs": { "balance": "10000", "riskPct": "2", "stopPips": "50", "pair": "USDCHF", "maxLots": "10", "quoteUsdRate": "0.885" },
  "expect": ["0.35 建议手数", "$200.00 实际亏损"],
  "ref": "第1064批：USD/CHF 每手每点=$11.2994，50 点风险=$564.97，$200 风险对应 0.35 手；旧 1.13 会低估每点价值并给出偏小手数。"
},
{
  "slug": "forex/spread-cost",
  "inputs": { "pair": "USDCHF", "lots": "1", "days": "0", "quoteUsdRate": "0.885" },
  "expect": ["$22.60 点差成本", "$29.60 总交易成本"],
  "ref": "第1064批：USD/CHF 点差 2 点，每点 $11.2994 ⇒ 点差成本 $22.60，加佣金 $7 得 $29.60；旧 1.13 会得到 $17.70/$24.70。"
}
,
{
  "slug": "forex/lot-size",
  "inputs": { "balance": "10000", "riskPct": "2", "stopPips": "1250", "pair": "EURUSD", "minLot": "0.01", "lotStep": "0.01", "maxLots": "10" },
  "expect": ["理论手数 = 0.0160 手", "建议交易手数 = 0.01 手", "$125.00"],
  "ref": "第1100批·保守取整：风险金额200、每手风险=1250×10=12500 ⇒ 理论0.0160手；旧显示 toFixed(2)=0.02 手却按 0.016 算风险。修复后按 0.01 步长向下取整为 0.01 手，按 0.01 重算实际亏损=125.00（占1.25%），不得出现 0.02 或 $200.00。"
},
{
  "slug": "forex/lot-size",
  "inputs": { "balance": "1000", "riskPct": "1", "stopPips": "1000", "pair": "EURUSD", "minLot": "0.01", "lotStep": "0.01", "maxLots": "10" },
  "expect": ["不足最低手数", "当前风险预算无法满足"],
  "ref": "第1100批·最小手数：风险10、每手风险10000 ⇒ 理论0.001手，按0.01步长取整为0，低于平台最小0.01；应明确提示无法下单，建议手数为0，不得输出0.001或四舍五入到0.01。"
},
{
  "slug": "forex/lot-size",
  "inputs": { "balance": "10000", "riskPct": "5", "stopPips": "50", "pair": "EURUSD", "minLot": "0.01", "lotStep": "0.1", "maxLots": "10" },
  "expect": ["建议交易手数 = 1.0 手", "按 0.1 手步长向下取整"],
  "ref": "第1100批·大步长：风险500、每手风险500 ⇒ 理论1.0 手，按 0.1 步长仍1.0；锁定步长文案与一位小数显示。若注入理论 1.05 更易区分，此用例锁定步长文案与一位小数。"
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

  console.log("==== forex calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
