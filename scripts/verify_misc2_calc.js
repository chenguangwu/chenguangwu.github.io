#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "it/screen-size",
  "inputs": {
    "width": "720",
    "height": "1280",
    "diagonal": "6.5"
  },
  "expect": [
    "PPI 像素密度： 225.94",
    "0.92 MP"
  ],
  "ref": "原 all_default 弱用例（1080/2400/6.7 恰等于页面默认）+ expect「细腻」是精细度档位词。改为 720×1280 @6.5\"：PPI = √(720²+1280²)/6.5 = 1468.60/6.5 = 225.94、像素数 720×1280 = 0.9216 MP → 0.92 MP、长宽比 9:16、物理宽 720/225.94 = 3.187\"、物理高 1280/225.94 = 5.665\"、点距 25.4/225.94 = 0.1124 mm；精细度跨档为「清晰」（默认 PPI √(1080²+2400²)/6.7 = 392.81 ⇒「细腻」）"
},
{
  "slug": "music/instrument-tuning",
  "inputs": {
    "baseFreq": "660"
  },
  "expect": [
    "1047.685"
  ],
  "ref": "auto-restore"
},
{
  "slug": "express/insurance-fee",
  "inputs": {
    "value": "7500"
  },
  "expect": [
    "500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/luggage-size",
  "inputs": {
    "size": "24"
  },
  "expect": [
    "三边总和： 127 cm"
  ],
  "ref": "尺寸结果卡按 SIZE_DATA[size] 渲染：24 寸 = 60×41×26 cm，三边和 60+41+26 = 127 cm，携带方式「需托运」（超过随身 115 cm 限制）。原注入 size=20 与页面默认 selected 相同 ⇒ 默认即 108 cm，零判别力；且原锚「国际标准随身尺寸约55×40×20cm」是页面 FAQ 静态文案，与输入无关。"
},
{
  "slug": "daily-goods/shoe-size",
  "inputs": {
    "footLen": "383"
  },
  "expect": [
    "请输入200-320mm之间的脚长"
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

  console.log("==== misc2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
