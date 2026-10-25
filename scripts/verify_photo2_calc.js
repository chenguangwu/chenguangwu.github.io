#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "photo2/exposure-triangle",
  "inputs": {
    "aperture": "1.8"
  },
  "expect": ["1.8\n0.01667\n100\n光圈 f/1.8 快门 1/60s ISO 100 EV 7.6\n等量曝光组合（EV 7.6） 调整 光圈 快门 ISO EV 偏差 var(--warning);\">-1.73 var(--warning);\">-0.71 var(--warning);\">+0.00 var(--warning);\">+2.36 var(--warning);\">+4.36 等量曝光：调整一档光圈/快门/ISO，用其他参数补偿，总进光量不变"],
  "ref": "auto-restore"
},
{
  "slug": "photo2/focal-length",
  "inputs": {
    "focal": "53"
  },
  "expect": [
    "37.5°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "photo2/video-storage",
  "inputs": {
    "bitrate": "20",
    "hours": "4",
    "minutes": "0",
    "audioBitrate": "128"
  },
  "expect": ["1920,1080\n30\n51.8\n128\n4\n0\n1\n91.28 GB 文件大小 51.93 总码率 Mbps 4时0分 录制时长 分辨率： 1920×1080 （2.1MP/帧） 总帧数： 432,000 帧 @30fps 每分钟存储： 389.5 MB 每小时存储： 22.82 GB 存储卡容量参考： 存储卡 可录时长 32 GB 1时24分 64 GB 2时48分 128 GB 5时36分 256 GB 11时13分 512 GB 22时26分"],
  "ref": "auto-restore"
},
{
  "slug": "photo2/white-balance",
  "inputs": {
    "kelvin": "5503"
  },
  "expect": [
    "5503K"
  ],
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

  console.log("==== photo2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
