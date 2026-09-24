#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "dance/bpm-rhythm",
  "inputs": {
    "bpm": "150",
    "beatsPerBar": "4",
    "beatsPerMove": "4",
    "duration": "60"
  },
  "expect": [
    "400.0 节拍间隔"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/choreography-timeline",
  "inputs": {
    "bpm": "123",
    "segCount": "6",
    "barsPerSeg": "4",
    "startTime": "0",
    "segName'+i+'": "'+name+'"
  },
  "expect": [
    "7.80秒"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/flexibility-test",
  "inputs": {
    "reach": "18",
    "age": "25"
  },
  "expect": [
    "18.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/partner-distance",
  "inputs": {
    "armSpan1": "173",
    "armSpan2": "160",
    "margin": "10"
  },
  "expect": [
    "10.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/rotation-stability",
  "inputs": {
    "rotations": "11",
    "time": "4",
    "height": "165"
  },
  "expect": [
    "17.28"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/tester-4",
  "inputs": {
    "age": "28",
    "score": "15"
  },
  "expect": [
    "28岁年龄段"
  ],
  "ref": "auto-restore"
},
{
  "slug": "dance/assessor-csat-1",
  "inputs": {},
  "clicks": ["document.getElementById('d_teach').value='5';document.getElementById('d_curr').value='4';document.getElementById('d_prog').value='5';document.getElementById('d_venue').value='4';document.getElementById('d_serv').value='5';calc()"],
  "expect": [
    "4.65 / 5.0 分",
    "教学质量 5分 1.25",
    "评估优秀 ，各维度表现均衡"
  ],
  "ref": "五维 <select id=\"d_<key>\"> 由 renderItems() 拼 innerHTML 生成（静态无 id ⇒ clicks 按 d_teach/d_curr/d_prog/d_venue/d_serv 赋值后调 calc()）：加权 5×0.25+4×0.20+5×0.25+4×0.15+5×0.15 = 1.25+0.80+1.25+0.60+0.75 = 4.65 ⇒ 优秀（默认值在桩下为空 ⇒ 0.00/不合格）。非默认输入+独立复算。"
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
  console.log("==== dance calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
