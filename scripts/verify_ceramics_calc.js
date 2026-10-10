#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "ceramics/clay-shrinkage",
  "inputs": {
    "wet": "150",
    "dry": "135",
    "fired": "120",
    "targetFired": "200",
    "totalShrink": "18"
  },
  "clicks": [
    "calc();calcReverse()"
  ],
  "expect": [
    "20.00%",
    "10.00%",
    "11.11%",
    "243.90"
  ],
  "ref": "S干=(150−135)/150=10.00%、S烧=(135−120)/135=11.11%、S总=(150−120)/150=20.00%（独立复算）；反向 L₀=L₂/(1−S总)=200/(1−0.18)=243.90 mm。默认 120/112/100 ⇒ 6.67% / 10.71% / 16.67%、L₀=116.28 ⇒ 四个锚点全不命中。原 expect「公式」是 calcReverse 的 step-line 标签常量（默认态同样渲染）⇒ 已替换。"
},
{
  "slug": "ceramics/glaze-ratio",
  "inputs": {
    "totalW": "1500",
    "w_'+idx+'": "-"
  },
  "expect": [
    "375.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ceramics/glaze-temp",
  "inputs": {},
  "expect": [
    "1060°C"
  ],
  "ref": "结构性不可注入（2026-10-10 复核，原 ref 为 auto-restore(default) 未评估项）：页面唯一输入为 #search（oninput=renderTable），renderTable 按锥号/温度子串过滤 CONES 表；过滤结果恒为默认全量表的子集，且无「未找到匹配」提示、无结果计数 ⇒ 不存在「注入态有而默认态无」的正串可锚（判据：关键词过滤+空关键词输出全量型页，只能反向锚空结果提示，本页无该提示）。维持 no_inputs，断言默认全量表常量串「1060°C」（CATS 低温釉 range 与锥 01 行均含，常量）。"
},
{
  "slug": "ceramics/kiln-firing",
  "clicks": ["switchTab('porcelain');"],
  "expect": [
    "峰值温度 1300°C，总烧成时间 约 12~15 小时。"
  ],
  "ref": "独立复算：SCHED.porcelain = {peak:1300, totalDesc:'约 12~15 小时'}；switchTab() 把 cur 换成 'porcelain' 后 render() 从 SCHED[cur] 取峰值与总时长，渲染「峰值温度 1300°C，总烧成时间 约 12~15 小时。」；默认 cur='bisque'（980°C / 约 8~10 小时）⇒ 串不同。switchTab(t,btn) 的 btn 有 if(btn) 判空，可省略。"
},
{
  "slug": "ceramics/wheel-speed",
  "inputs": {
    "diameter": "23"
  },
  "expect": [
    "0.230"
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
  console.log("==== ceramics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
