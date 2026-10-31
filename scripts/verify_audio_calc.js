#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "audio/analysis-1",
  "inputs": {
    "fs": "8000",
    "N": "1024",
    "bin": "10"
  },
  "expect": [
    "78.125"
  ],
  "ref": "Δf=8000/1024=7.8125 Hz，目标 bin10 对应频率=10×7.8125=78.125 Hz（独立计算）"
},
{
  "slug": "audio/audio-cut",
  "inputs": {
    "startInput": "0",
    "endInput": "0"
  },
  "expect": [
    "00.000"
  ],
  "ref": "结构性不可改造（保留 all_default，勿重复评估）：结果区（selDurTxt / resultBox）由音频文件解码后的 "
     + "duration 驱动，harness 无文件输入 ⇒ 注入 startInput / endInput 后输出逐字不变（2026-09-25 实测）。"
},
{
  "slug": "audio/audio-waveform",
  "inputs": {
    "waveColor": "#FF6B35",
    "smoothing": "3.8"
  },
  "expect": [
    "3.8"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
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

  console.log("==== audio calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
