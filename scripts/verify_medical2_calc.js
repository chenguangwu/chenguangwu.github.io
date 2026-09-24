#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "medical2/bed-occupancy",
  "inputs": {
    "beds": "600",
    "openBeds": "550",
    "days": "31",
    "occupiedDays": "17500",
    "discharges": "1400"
  },
  "expect": [
    "102.6% 床位使用率",
    "2.55 床位周转次数",
    "12.5 天 平均住院日"
  ],
  "ref": "开放总床日 550×31 = 17,050；使用率 17500/17050 = 102.6%（>95 ⇒ 超负荷）；周转 1400/550 = 2.55；平均住院日 17500/1400 = 12.5 天（默认 480/30/13000/900 ⇒ 90.3% / 1.88 / 14.4 天 / 合理档，跨档）"
},
{
  "slug": "medical2/drug-expiry",
  "inputs": {
    "warningDays": "180",
    "urgentDays": "30",
    "fQty": "1"
  },
  "expect": [
    "添加药品"
  ],
  "ref": "结构性不可注入（保留 all_default）：页面唯一数据源是 localStorage 的 data[]，而 harness 的 localStorage 桩 getItem() 恒返回 null ⇒ data 恒为空，统计恒 0/0/0/0/0、列表恒「暂无药品记录」。注入 warningDays/urgentDays 只改分类阈值，空数据下零判别力；唯一写数据的 saveForm() 命中兜底 DESTRUCTIVE 正则的 ^save 前缀被跳过。故无任何可注入路径产生随输入变化的输出。"
},
{
  "slug": "medical2/iv-drip-speed",
  "inputs": {
    "vol1": "250",
    "drip1": "60",
    "factor1": "20",
    "vol2": "600",
    "hours2": "3",
    "factor2": "20"
  },
  "expect": [
    "1 小时 23 分钟 预计输液时间",
    "180.0 ml/h 每小时输液量",
    "12,000 滴"
  ],
  "ref": "calcTime：总滴数 250×20 = 5,000、时长 5000/60 = 83.3 分 = 1 小时 23 分钟、180.0 ml/h；calcSpeed：总滴数 600×20 = 12,000、滴速 12000/180 = 67 滴/分（默认 factor=15/500/40/500/4 ⇒ 3 小时 8 分钟 / 160.0 ml/h / 7,500 滴）；factor1/factor2 是 <select>，页面 selected=15、首项=10 ⇒ 必须显式注入 20"
},
{
  "slug": "medical2/surgery-duration",
  "inputs": {
    "procedure": "胃大部切除术",
    "prepTime": "30",
    "recoverTime": "20",
    "cleanTime": "15"
  },
  "expect": [
    "1 术式数量",
    "3 小时 50 分 最短用时",
    "4 小时 20 分 预计用时"
  ],
  "ref": "注入 procedure=胃大部切除术（普外 180-240 分）⇒ 经 onchange=addProcedure() 入 selected（1 项）；术前 30 + 复苏 20 + 台间清洁 0 = 50 分 ⇒ 最短 180+50 = 230 分 = 3 小时 50 分、预计 210+50 = 260 分 = 4 小时 20 分（默认 selected 为空 ⇒ result 隐藏、只显示「尚未选择术式，请从上方下拉添加」）；**注**：harness 桩不解析 HTML style 属性 ⇒ travelBox 判为可见（真机 display:none 时不计 preparation），断言按 harness 口径书写"
},
{
  "slug": "medical2/medical-abbrev",
  "inputs": {
    "searchInput": "qd"
  },
  "expect": [
    "1 匹配结果"
  ],
  "ref": "搜索 qd ⇒ 命中 1 条（默认空关键词渲染全部 96 条 ⇒ 「96 匹配结果」）；原 expect「每6小时一次」属整表渲染的静态词表逃生项（默认态也渲染该行）。**注意**：绝不可再锚「qd quaque die…」行本身 —— 该行在默认全表渲染时同样出现，会立刻退化成逃生项（expect 任一命中即 PASS）"
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
  console.log("==== medical2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
