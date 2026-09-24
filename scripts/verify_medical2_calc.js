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
    "urgentDays": "30"
  },
  "clicks": ["var __d=function(n){var t=new Date();t.setDate(t.getDate()+n);return t.toISOString().slice(0,10);};localStorage.getItem=function(){return JSON.stringify([{name:'阿莫西林胶囊',spec:'0.25g×24粒',batch:'B-EXP',expiry:__d(-20),qty:12,location:'常温柜A2'},{name:'布洛芬片',spec:'0.1g×20片',batch:'B-URG',expiry:__d(12),qty:8,location:'阴凉柜B1'},{name:'维生素C片',spec:'100mg×60片',batch:'B-WAR',expiry:__d(120),qty:30,location:'常温柜C3'},{name:'葡萄糖注射液',spec:'500ml',batch:'B-OK',expiry:__d(600),qty:5,location:'库房D1'}]);};loadData();render()"],
  "expect": [
    "4 药品总数",
    "1 已过期",
    "葡萄糖注射液"
  ],
  "ref": "localStorage 覆写法（BATCH101 打法）：clicks 内覆写 localStorage.getItem 返回四条药品，"
     + "再调 loadData() 灌进顶层 data[]、render() 渲染 —— 等价于「用户本就有库存数据」。"
     + "效期用相对今天 ±N 天构造（−20/12/120/600）⇒ 分级恒为 已过期 1 / 临期紧急 1 / 近效期 1 / 正常 1，"
     + "不受运行日期漂移影响。**必须显式 loadData()**，否则 data 仍为空、命中会落到兜底的 saveForm()。"
     + "原 expect「添加药品」是空列表页按钮文案（默认态常量）。",
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
