#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "acupuncture/acupoint-injection",
  "inputs": {
    "points": "5"
  },
  "expect": [
    "5.00ml"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/acupoint-location",
  "inputs": { "realCm": "27", "targetCun": "6" },
  "clicks": ["selectRegion('chest');calc()"],
  "expect": [
    "3.00 每寸厘米",
    "18.00 cm",
    "天突(胸骨上窝)→歧骨(胸剑联合)"
  ],
  "ref": "selectRegion('chest') 自动选中首段「天突(胸骨上窝)→歧骨(胸剑联合)」（标准折量 9 寸）；实测 27 cm ⇒ 每寸 27/9 = 3.00 cm；目标 6 寸 ⇒ 定位 6×3.00 = 18.00 cm。默认态 currentPart 未选、realCm 为空 ⇒ result 只出提示文案，三串均不命中。"
},
  // 注：acupuncture/analysis-10 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "acupuncture/bloodletting-therapy",
  "inputs": {
    "points": "6"
  },
  "expect": [
    "1.32ml"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/cupping-mark-analysis",
  "clicks": [
    "selectMark('red');analyze();"
  ],
  "expect": [
    "鲜红 辨证分析"
  ],
  "ref": "弱用例去默认化（BATCH118）：原锚默认态「5-7」（消退天数常量，判别力0）。clicks 经 selectMark('red')+analyze() 切到鲜红罐印，expect 锚「鲜红 辨证分析」标题 —— 页面默认 currentMark 为 purple（默认态渲染「紫红 辨证分析」），故红色分析只在非默认态出现；清 clicks 兜底遍历不产出该串 ⇒ 零逃生项（锚「紫红」会撞默认态，不可用）。"
},
{
  "slug": "acupuncture/cupping-pressure",
  "inputs": {
    "time": "10",
    "part": "shoulder"
  },
  "expect": [
    "255"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/deqi-sensation",
  "inputs": {
    "patientScore": "5",
    "doctorScore": "5",
    "propagation": "1"
  },
  "expect": [
    "2.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/ear-acupressure",
  "inputs": {},
  "expect": [
    "将王不留行籽(或磁珠)贴于0.5×0.5cm胶布中央"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "acupuncture/electroacupuncture",
  "inputs": {
    "duration": "20",
    "purpose": "spasm"
  },
  "expect": [
    "spasm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/flash-cupping",
  "inputs": {
    "time": "10",
    "part": "shoulder"
  },
  "expect": [
    "10分钟)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/guasha-direction",
  "inputs": {
    "purpose": "pain"
  },
  "expect": [
    "舒筋止痛可重点在阿是穴及痛点周围加重"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/intradermal-needle",
  "inputs": {
    "part": "face"
  },
  "expect": [
    "0.35"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/meridian-pathway",
  "inputs": {
    "sensType": "partial"
  },
  "expect": [
    "部分感传(短程)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/moxibustion-count",
  "inputs": {
    "moxaType": "aiJiong"
  },
  "expect": [
    "1.40"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/needle-retention",
  "inputs": {
    "age": "adult"
  },
  "expect": [
    "1.10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/needling-depth",
  "inputs": {
    "bodyType": "medium"
  },
  "expect": [
    "0.25寸"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/pediatric-tuina",
  "inputs": {
    "constitution": "weak"
  },
  "expect": [
    "144"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/recommender-acupoint",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/recommender-time",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore(default-hit)（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "acupuncture/tuina-frequency",
  "inputs": {
    "duration": "8"
  },
  "expect": [
    "1024"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/tuina-medium",
  "inputs": {
    "technique": "ca"
  },
  "expect": [
    "适配擦/推法"
  ],
  "ref": "auto-restore"
},
{
  "slug": "acupuncture/warm-needle-moxibustion",
  "inputs": {
    "ambTemp": "38"
  },
  "expect": [
    "38"
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
  console.log("==== acupuncture calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
