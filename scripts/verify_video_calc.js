#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "video/analysis-69",
  "inputs": {
    "selfViews": "12000",
    "selfLike": "8",
    "selfFinish": "55",
    "rivalViews": "3000,4000,3500,5000,2500"
  },
  "expect": [
    "竞品平均播放： 3600",
    "竞品中位播放： 3500",
    "相对均值差距： 233.3%",
    "市场定位： 头部账号"
  ],
  "ref": "非默认：竞品(3000,4000,3500,5000,2500)均值3600、中位3500；自身12000→差距(12000-3600)/3600=233.3%；12000>3600*1.5=5400→头部。默认(8000/5000,7000,6000,9000,4500)均值6300腰部，注入失败即不命中"
},
{
  "slug": "video/subtitle-tool",
  "inputs": {
    "offset-ms": "7",
    "speed-factor": "1",
    "srt-input": " 00:00:04,000\nHello World\">"
  },
  "expect": [
    "007"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-compressor",
  "inputs": {
    "duration": "15",
    "targetSize": "100"
  },
  "expect": [
    "910kbps"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-converter",
  "inputs": {
    "duration": "15"
  },
  "expect": [
    "4943.8MB"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-speed",
  "inputs": {
    "h": "7",
    "m": "30",
    "s": "0",
    "ms": "0",
    "fps": "30",
    "speed": "1.5"
  },
  "expect": [
    "810"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-trimmer",
  "inputs": {
    "start-h": "0",
    "start-m": "1",
    "start-s": "30",
    "end-h": "0",
    "end-m": "3",
    "end-s": "0"
  },
  "expect": [
    "00:01:30 → 00:03:00",
    "总时长: 00:01:30"
  ],
  "ref": "start=0×3600+1×60+30=90s ⇒ 00:01:30；end=3×60=180s ⇒ 00:03:00；片段时长=180−90=90s ⇒ 00:01:30。"
     + "原 expect「添加一个开始吧」是空列表提示（默认全 0 ⇒ 起止相同、无法成段，回退默认仍命中 ⇒ 逃生项）。"
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
  console.log("==== video calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
