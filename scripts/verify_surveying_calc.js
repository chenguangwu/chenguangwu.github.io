#!/usr/bin/env node
/**
 * 第 28 道门禁：surveying 分类计算正确性验证（16 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：scale-converter（mode 切换 + 多单位下拉，stub 不稳）；
 *       circular-curve / vertical-curve-elev / stadia-distance（多分支/多输出）；
 *       convert-* 系列（通用系数换算，语义弱）。
 * 用法: node scripts/verify_surveying_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "surveying/slope-percent",
    inputs: { h: "8", d: "50" },
    expect: ["16.00", "9.09"],
    ref: "坡度=8/50×100=16.00%；坡度角=atan(8/50)×180/π=9.09°（默认 5/100 避开）",
  },
  {
    slug: "surveying/horizontal-distance",
    inputs: { l: "200", a: "30" },
    expect: ["173.205", "100.000"],
    ref: "水平距=200×cos30°=173.205；高差=200×sin30°=100.000（默认 150/10 避开）",
  },
  {
    slug: "surveying/external-distance-curve",
    inputs: { R: "200", D: "90" },
    expect: ["82.843"],
    ref: "外距 E=R(sec(D/2)−1)=200×(1/cos45°−1)=82.843（默认 100/60 避开）",
  },
  {
    slug: "surveying/tangent-length-curve",
    inputs: { R: "200", D: "90" },
    expect: ["200.000"],
    ref: "切线长 T=R·tan(D/2)=200×tan45°=200.000（默认 100/60 避开）",
  },
  {
    slug: "surveying/chord-length-curve",
    inputs: { R: "200", D: "90" },
    expect: ["282.843"],
    ref: "弦长 C=2R·sin(D/2)=2×200×sin45°=282.843（默认 100/60 避开）",
  },
  {
    slug: "surveying/middle-ordinate-curve",
    inputs: { R: "200", D: "90" },
    expect: ["58.579"],
    ref: "中点垂距 M=R(1−cos(D/2))=200×(1−cos45°)=58.579（默认 100/60 避开）",
  },
  {
    slug: "surveying/coordinate-distance-2d",
    inputs: { x1: "0", y1: "0", x2: "6", y2: "8" },
    expect: ["10.000"],
    ref: "D=√(6²+8²)=10.000（默认 0,0,3,4 避开）",
  },
  {
    slug: "surveying/coordinate-distance-3d",
    inputs: { x1: "0", y1: "0", z1: "0", x2: "2", y2: "3", z2: "6" },
    expect: ["7.000"],
    ref: "d=√(2²+3²+6²)=7.000（默认 0,0,0/100,100,50 避开）",
  },
  {
    slug: "surveying/bearing-from-coordinates",
    inputs: { dN: "100", dE: "173.205" },
    expect: ["60.00"],
    ref: "α=atan2(173.205,100)×180/π=60.00°（默认 100/100 避开）",
  },
  {
    slug: "surveying/earthwork-pyramid-volume",
    inputs: { A: "150", h: "6" },
    expect: ["300.00"],
    ref: "V=A·h/3=150×6/3=300.00 m³（默认 100/3 避开）",
  },
  {
    slug: "surveying/coordinate-rotation",
    inputs: { x: "10", y: "10", t: "90" },
    expect: ["-10.000", "10.000"],
    ref: "绕原点转 90°：X'=10cos90−10sin90=−10.000；Y'=10sin90+10cos90=10.000（默认 10/0/30 避开）",
  },
  {
    slug: "surveying/area-coordinates",
    inputs: { xs: "0,200,200,0", ys: "0,0,200,200" },
    expect: ["40000.00"],
    ref: "鞋带公式：200×200 正方形面积=40000.00 m²（默认 100×100 避开）",
  },
  {
    slug: "surveying/triangulation-side",
    inputs: { a: "100", A: "30", B: "90" },
    expect: ["200.000"],
    ref: "正弦定理 b=a·sinB/sinA=100×sin90°/sin30°=200.000（默认 100/45/60 避开）",
  },
  {
    slug: "surveying/end-area-volume",
    inputs: { A1: "20", A2: "40", L: "60" },
    expect: ["1800.00"],
    ref: "平均断面法 V=(A1+A2)/2·L=(20+40)/2×60=1800.00 m³（默认 10/20/50 避开）",
  },
  {
    slug: "surveying/prismoidal-volume",
    inputs: { A1: "10", Am: "20", A2: "30", L: "60" },
    expect: ["1200.00"],
    ref: "棱台公式 V=L/6·(A1+4Am+A2)=60/6×(10+80+30)=1200.00 m³（默认 10/15/20/50 避开）",
  },
  {
    slug: "surveying/grade-angle",
    inputs: { a: "45" },
    expect: ["100.00", "1.000"],
    ref: "角度→坡度：tan45°×100=100.00%；坡比=1/tan45°=1.000（默认 5° 避开）",
  },
  {
    "slug": "surveying/analysis-cycle",
    "inputs": {
      "data": "W1,1.5\nW2,3.8\nW3,6.9\nW4,9.4\nW5,11.2",
      "thr": "10",
      "vr": "2.5"
    },
    "expect": [
      "累计变形： 11.20",
      "最大单期变化： 3.10",
      "平均变化速率： 2.24"
    ],
    "ref": "各期变化=1.5/2.3/3.1/2.5/1.8 → 累计变形=11.20 mm（超阈值10）、最大单期变化=3.10 mm(W3，超速率2.5)、平均速率=11.2/5=2.24 mm/期（独立复算；默认 第1期2.1/第2期4.5/第3期7.2/第4期8.0 → 累计8.00、最大单期2.70、平均2.00，注入失败即不命中）"
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
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== surveying calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();