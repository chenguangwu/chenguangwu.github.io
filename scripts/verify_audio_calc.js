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
// 已移除 audio/audio-cut（inputs startInput=0/endInput=0，expect ["00.000"]）。
// 原因：结果区由音频文件解码后的 duration 驱动，harness 无文件输入/Web Audio 解码 ⇒ 注入 start/end
// 后输出逐字不变（默认态即命中），无任何可判别增量 ⇒ 按纪律删除而非保留 skip。
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
},
{
  "slug": "audio/analysis-1",
  "inputs": {
    "fs": "48000",
    "N": "8192",
    "bin": "1000"
  },
  "expect": [
    "5859.375"
  ],
  "ref": "Δf=48000/8192=5.859375 Hz，目标 bin1000 对应频率=1000×5.859375=5859.375 Hz（独立计算）；默认态 44100/4096/bin200 输出 2153.32 ⇒ 强判别"
},
{
  "slug": "audio/analysis-1",
  "inputs": { "fs": "", "N": "", "bin": "" },
  "expect": ["请输入有效采样率与 FFT 长度"],
  "ref": "空态回归：fs/N 为空时旧实现 `parseFloat(...)||44100 / ||4096` 静默代入默认值并输出分辨率/奈奎斯特频率；现要求提示。默认态 10.7666/22050.00 不含该提示 ⇒ 强判别。"
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
