#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "decor/ceiling-panel-quantity",
  "inputs": {
    "L": "7.2",
    "W": "3.6",
    "pl": "600",
    "pw": "600",
    "loss": "5"
  },
  "expect": [
    "25.92"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/curtain-fabric",
  "inputs": {
    "rodW": "5.5",
    "curtainH": "2.6",
    "sideHem": "0.05",
    "topBottomHem": "0.3",
    "patternLoss": "0"
  },
  "expect": ["5.5\n2.6\n2\n2.8\n0.05\n0.3\n0\n14.50 m 需购布料总长（幅宽 2.8m）\n窗帘杆宽： 5.5 m ，褶皱倍数 2 所需布料宽：5.5 × 2 = 11.00 m 所需幅数：11.00 ÷ 2.70（幅宽 2.8 − 两侧缝边 0.10）= 5 幅 每幅用料：2.6 + 0.3（缝边）+ 0（对花）= 2.90 m 总用料：5 × 2.90 = 14.50 m 实际展开宽：14.00 m，实际褶皱倍数 2.55 用料面积： 40.60 ㎡\n💡 选购建议 • 同一花色一次购齐，避免色差 • 建议多买 0.29 m 备用 • 纱帘褶皱倍数建议 2.5-3 倍更飘逸 • 有花纹布料需计算对花损耗 • 双层（布+纱）需分别计算后相加"],
  "ref": "auto-restore"
},
{
  "slug": "decor/detector-18",
  "inputs": {
    "hcho": "3.08",
    "tvoc": "0.50",
    "benzene": "0.05",
    "ammonia": "0.15",
    "radon": "200"
  },
  "expect": [
    "(3850%)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/paint-color-mix",
  "inputs": {
    "paintKg": "8"
  },
  "expect": ["奶油白 米黄 杏粉 浅粉 浅蓝 豆绿 灰绿 浅紫 暖灰 咖啡 砖红 藏青\n8\n1\n奶油白 色浆总添加量： 80.0 g （占漆 1%） 色浆分配 铁黄（60%） 48.0 g 铁红（30%） 24.0 g 铁黑（10%） 8.0 g 💡 建议先取少量乳胶漆小样试色，确认效果后再按比例调配整桶。色浆需缓慢加入并充分搅拌，避免一次性过量。"],
  "ref": "auto-restore"
},
{
  "slug": "decor/scheduler",
  "inputs": {
    "projName": "家装工程_X"
  },
  "expect": [
    "家装工程_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/skirting-length",
  "inputs": {
    "roomLen": "8",
    "roomWid": "4",
    "doors": "1",
    "doorWid": "0.9",
    "windows": "0",
    "winWid": "1.5",
    "wasteSk": "5",
    "wasteCo": "8",
    "skLen": "2.4",
    "coLen": "2.4"
  },
  "expect": [
    "24.26"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/wallpaper-quantity",
  "inputs": {
    "perimeter": "18",
    "height": "2.8",
    "deduct": "6",
    "rollWidth": "0.53",
    "rollLen": "10",
    "pattern": "0.32",
    "waste": "5"
  },
  "expect": [
    "44.40"
  ],
  "ref": "auto-restore"
},
{
  "slug": "decor/room-illumination",
  "inputs": { "area": "45", "lux": "300", "roomType": "kitchen" },
  "expect": ["14 盏 建议", "14063 所需光通量(lm)", "实际照度： 161 lux"],
  "ref": "注入 area=45（默认 20）+ roomType=kitchen（默认 living）。⚠ 选 roomType 会联动改写目标照度（厨房 150 lux）⇒ 注入的 lux=300 被覆盖，这是真机 onchange 行为，故实际按 150 lux 计算：所需光通量 = 面积×照度÷(利用系数 0.6 × 维护系数 0.8) = 45×150÷0.48 = 14062.5 ⇒ 14063 lm；单灯 12W×90 lm/W = 1080 lm ⇒ 盏数 = ⌈14063÷1080⌉ = 14；实际照度 = 14×1080×0.48÷45 = 161.28 ⇒ 161 lux。默认态（20㎡ / living 100lux）为 4 盏 / 4167 lm / 104 lux，三串均不出现。"
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

  console.log("==== decor calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
