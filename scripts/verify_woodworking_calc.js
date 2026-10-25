#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "woodworking/angle-cut",
  "inputs": {
    "jointAngle": "135",
    "segments": "2",
    "miterAngle": "45",
    "bevelAngle": "0",
    "startWidth": "50",
    "endWidth": "20",
    "taperLength": "200"
  },
  "expect": [
    "56.25°"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/board-feet",
  "inputs": {
    "thicknessIn": "4",
    "widthIn": "6",
    "lengthFt": "8",
    "quantity": "1",
    "price": "5",
    "convertValue": "100"
  },
  "expect": [
    "16.0000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/moisture-content",
  "inputs": {
    "wetWeight": "180",
    "dryWeight": "100"
  },
  "expect": [
    "每100cm收缩0.00cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/mortise-size",
  "inputs": {
    "thickness": "30",
    "width": "80"
  },
  "expect": ["through\n30\n80\n0.4\nmedium\n12 榫厚(mm) 56 榫宽(mm) 90 榫深(mm) 12 肩宽(mm)\n板宽 undefinedmm 榫 undefinedmm 榫深 undefinedmm\n榫卯类型： 贯通榫 | 木材： 中硬 板厚： 30 mm ，板宽： 80 mm 榫厚： 12 mm （板厚 × 40%） 榫宽： 56 mm （板宽 × 70%） 榫深： 90 mm （板厚 × 3.0） 两侧肩宽： 12 mm （每侧） 上下颊高： 9 mm （每侧） ✓ 尺寸已计算 ：以上为推荐榫头尺寸，实际加工可根据木材状态微调。 * 尺寸为理论计算值，实际需根据木材含水率、纹理方向和加工精度调整。"],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/wood-screws",
  "inputs": {
    "totalThick": "45",
    "topThick": "15"
  },
  "expect": [
    "穿透下层约83%"
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

  console.log("==== woodworking calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
