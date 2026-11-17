#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs;
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
},
{
  "slug": "daily-goods/shoe-size",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/daily-goods/shoe-size.html','utf8');var noCN=h.indexOf('即 CN 250')<0&&h.indexOf('CN 250)')<0;var newCN=h.indexOf('即 CN 25.0')>=0;var noEU=h.indexOf('40.25 ≈ 40')<0;var newEU=h.indexOf('40.25 → 40.5')>=0;document.getElementById('__tbProbe').textContent=(noCN&&newCN&&noEU&&newEU)?'__SHOE_G2_OK__':'__SHOE_G2_BAD__ '+[noCN,newCN,noEU,newEU].join(',');"],
  "expect": ["__SHOE_G2_OK__"],
  "ref": "第1100批 G2：CN 口径统一 cm 制（公式框「脚长250mm即CN250」改为 CN25.0，与代码 cn=cm/说明卡255mm→25.5/算例CN26.0 一致）；EU 按 0.5 分度取半（「40.25≈40」改为「40.25→40.5」，与 half(40.25)=40.5 一致），meta/JSON-LD/说明卡四处同步。旧版必红。"
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
