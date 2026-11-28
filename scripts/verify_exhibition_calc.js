#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "exhibition/assessor-60",
  "inputs": {
    "boothCost": "8",
    "buildCost": "4",
    "travelCost": "3",
    "days": "5",
    "visitors": "800",
    "leads": "200",
    "intents": "90",
    "deals": "36",
    "revenue": "60"
  },
  "clicks": [
    "calc()"
  ],
  "expect": [
    "4.00×",
    "300.0%",
    "单线索成本 ¥750",
    "收集线索 200 25.0%"
  ],
  "ref": "总投入 15 万、签约 60 万 ⇒ 签约额/总投入 4.00×，净 ROI=(60−15)/15=300.0%；到访→线索 200/800=25.0%，单线索成本 15×10000/200=¥750；漏斗逐层 800≥200≥90≥36 通过。默认组为 2.50×/150%/24.0%/¥833，与本例锚点不相交。"
},
{
  "slug": "exhibition/assessor-evacuation",
  "inputs": {
    "area": "4000",
    "capacity": "1500",
    "exits": "6",
    "width": "3.5",
    "distance": "30",
    "load": "6"
  },
  "checkIds": [
    "fireAlarm",
    "sprinkler",
    "smokeExhaust",
    "emergencyLight",
    "broadcast"
  ],
  "clicks": [
    "calc()"
  ],
  "expect": [
    "未触发本页检查项",
    "1.3 出口通行时间(分)",
    "0.38 人员密度(人/m²)"
  ],
  "ref": "密度 1500/4000=0.375；总净宽 6×3.5=21.0m，需要 1500×0.6/100=9.0m，宽度通过；距离 30≤40、荷载 6≥4；5 项消防设施勾满 ⇒ 待核项 0，输出「未触发本页检查项」而非「安全合格」。出口通行时间 1500/(21×55)=1.299→1.3 分（不再乘 60）；「加权提示分」为 0 单独显示。"
},
{
  "slug": "exhibition/analysis-61",
  "inputs": { "vis": "3000", "data": "展位费,120000,120000\n搭建费,80000,96000\n物料印刷,25000,22000\n人员差旅,40000,52000\n宣传推广,30000,28000" },
  "expect": [
    "预算合计： 295000.00",
    "实际合计： 318000.00",
    "单位观众成本： 106.00"
  ],
  "ref": "预算 120000+80000+25000+40000+30000=295000；实际 120000+96000+22000+52000+28000=318000；单位成本 318000/3000=106.00（默认 2000 人 130000/135000/67.50，避开）"
},
{
  "slug": "exhibition/analysis-pnl",
  "inputs": {
    "leads": "520",
    "conv": "15",
    "aov": "9600",
    "vcpct": "58",
    "sponsor": "45000",
    "ticket": "12000",
    "booth": "95000",
    "build": "42000",
    "travel": "15000",
    "material": "8000",
    "staff": "18000"
  },
  "expect": [
    "193,496.00",
    "108.71",
    "121,000.00"
  ],
  "ref": "展会盈亏：订单=520×15%=78 单，销售=748800；固定支出=95000+42000+15000+8000+18000=178000，直接收入=57000，待覆盖=121000；净盈亏=748800+57000−178000−434304=193496.00，ROI=193496÷178000=108.71%（独立复算；默认组为 53,200.00/35.95/110,000.00，注入失败即不命中）"
},
{
  clicks: ["calc()"],
  "slug": "exhibition/assessor-61",
  "expect": ["未完成前不生成评分与建议"],
  "ref": "默认 6 个下拉均为「请选择（未评估）」，不再把首项 5 分当默认结果；未选全时只提示待选维度。"
},
{
  "slug": "exhibition/assessor-61",
  "inputs": {"e1":"4","e2":"4","e3":"4","e4":"5","e5":"4","e6":"4","w1":"2"},
  "clicks": ["calc();"],
  "expect": ["4.14", "自评良好", "权重合计 7.0"],
  "ref": "评分 4/4/4/5/4/4，权重 2/1/1/1/1/1：加权均值=(8+4+4+5+4+4)/7=29/7=4.1429→4.14，标准化 24.9/30；≥3.5 且 <4.5 ⇒ 自评良好。默认等权 4.17 与本例零交集。"
},
{
  "slug": "exhibition/stats-12",
  "inputs": {
    "flow": "14:00,300\n15:00,180\n16:00,220",
    "dwell": "2,4,6,8,10",
    "rating": "1,2,3,4,5"
  },
    "expect": [
      "峰值时段： 14:00",
      "总流量： 700",
      "标准差 1.41"
    ],
  "ref": "流量合计300+180+220=700、峰值14:00(300)、均流233.33；停留2/4/6/8/10→均值6.00/中位6.00/极差8.00；评分1-5→均值3.00/标准差1.41（独立复算；默认 流量470/峰值10:00、停留均值6.71/中位6/极差9、评分均值4.00/标准差1.07，注入失败即不命中）"
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

  console.log("==== exhibition calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
