#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "hotel/currency-exchange",
  "inputs": {
    "fromCode": "CNY",
    "toCode": "USD",
    "rate": "0.138",
    "fee": "1.5",
    "amount": "10000",
    "direction": "forward"
  },
  "expect": [
    "150 手续费",
    "1,359.3 USD 到账金额"
  ],
  "ref": "原 all_default 弱用例（rate=0.138/fee=0/amount=10000 等于默认）+ expect「手续费」是 data-card 里常驻的静态标签。改为 fee=1.5（其余保持默认、方向 forward）：手续费 10000×1.5%=150、净额 9850、到账 9850×0.138=1359.3 → 显示 1,359.3 USD。默认态 fee=0 ⇒「0 手续费」、到账 1,380 USD（跨档）"
},
{
  "slug": "hotel/itinerary-planner",
  "inputs": {
    "totalDays": "4",
    "hoursPerDay": "9",
    "spotCount": "3",
    "avgHours": "2.5"
  },
  "expect": [
    "36h 总游玩时长",
    "5.4h 缓冲时间(15%)",
    "10.2h 1.13天"
  ],
  "ref": "**坏用例重写**：原 inputs 含生成器模板串残留（pri${i} 键），且 totalDays/hoursPerDay/spotCount/avgHours 四值恰等于页面默认 ⇒ 双重失效。景点行由 buildList() 运行期生成（不在静态 HTML 内），故保留 4 个静态参数并改为 totalDays=4/hoursPerDay=9/spotCount=3/avgHours=2.5：总时长 4×9=36h、缓冲 15%=5.4h、可玩 30.6h；优先级控件是运行期生成的、读不到值 ⇒ 每景回落 3、priSum=9、各景 30.6×3/9=10.2h → 10.2/9=1.13 天。默认态 40h/6h、6 景、5.67h/0.71 天"
},
{
  "slug": "hotel/occupancy-revpar",
  "inputs": {
    "totalRooms": "100",
    "soldRooms": "70",
    "revenue": "28000",
    "days": "1"
  },
  "expect": [
    "70% 出租率 OCC",
    "¥280 每可售房收入 RevPAR"
  ],
  "ref": "原 all_default 弱用例（totalRooms=120/soldRooms=96/revenue=38400/days=1 等于默认）+ expect「出租率」是 data-card 里常驻的静态标签。改为 100 间/售出 70/收入 28000/1 天：可用间夜 100、出租率 70%、ADR 28000/70=400、RevPAR 28000/100=280 ⇒ 评级「良好」（65≤occ<80）。默认态 80% / ¥400 / ¥320 /「优秀」；注意 ADR 默认与注入态同为 ¥400，故不锚 ADR"
},
{
  "slug": "hotel/tip-calculator",
  "inputs": {
    "bill": "240",
    "tipPct": "18",
    "people": "3",
    "tax": "6"
  },
  "expect": [
    "小费慷慨",
    "人均： 99.2"
  ],
  "ref": "auto-restore（去默认化：bill 240/18%/3人/税6% → tip=43.2、total=297.6、人均=99.2；默认 15%/2人 得「小费适中」+69.0）"
},
{
  "slug": "hotel/assessor-62",
  "inputs": {
    "q1": "4"
  },
  "expect": [
    "均值4.80"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hotel/checker-assessor",
  "inputs": {
    "q1": "4"
  },
  "expect": [
    "均值4.83"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hotel/luggage-weight",
  "inputs": {
    "days": "11"
  },
  "expect": [
    "13.5"
  ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== hotel calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
