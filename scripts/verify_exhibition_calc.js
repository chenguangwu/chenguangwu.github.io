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
    "4.00 ROI 投入产出比",
    "单线索成本 ¥750",
    "意向客户 90 45.0%"
  ],
  "ref": "总投入 tc=8+4+3=15 万、签约额 60 万 ⇒ ROI=60/15=4.00（≥3 ⇒ 效果优异）；线索转化 200/800=25.0%、意向转化 90/200=45.0%、签约转化 36/200=18.0%；单线索成本 15×10000/200=¥750（独立复算）。默认组 5/3/2 + 500/120/45/8/25 ⇒ 2.50 / 24.0% / 37.5% / 6.7% / ¥833，与本例三个锚点零交集。原 expect「月内推进签约转化」是 info-box 常驻句尾（注入失败同样命中）⇒ 已替换。days 未被 calc() 读取（零影响键）⇒ 仅作记录。"
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
    "所有安全指标均满足规范要求",
    "77.9 估算疏散时间(分)",
    "0.38 人员密度(人/m²)"
  ],
  "ref": "密度 1500/4000=0.375（≤0.5 合格）；总疏散宽度 6×3.5=21.0 m ≥ 需要 1500×0.65/100=9.75 m；距离 30≤40、荷载 6≥4 均合格；checkIds 勾满 5 项消防设施 ⇒ issues 空、score=0 ⇒ 渲染「所有安全指标均满足规范要求」；疏散时间 1500/(21×55)×60=77.92→77.9 分（独立复算）。默认组 5000/2000/4/3.0/35/5 且 checkbox 在桩内全未勾 ⇒ score=13 ⇒ 不合格 + 五项「缺失」（原 expect「应急广播缺失」即出自这里，属常量型逃生项）⇒ 与本例三个锚点零交集。"
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
  "slug": "exhibition/assessor-61",
  "inputs": {
    "e1": "4"
  },
  "expect": [
    "均值4.83"
  ],
  "ref": "auto-restore"
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
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== exhibition calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
