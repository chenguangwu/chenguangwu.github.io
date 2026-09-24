#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  // 原为 all_default 弱用例 + expect「满足要求」是判定文案（二值判读词，逃生项）。
  // 均布模式（calcMode 默认 uniform）：f = 5qL⁴/(384EI)，[f] = L/limitN。注入值刻意让校核不通过（跨分支）。
  { slug: "bridge/deflection-calc", inputs: {"inL":"30","inE":"32.5","inI":"0.08","inQ":"60","inLimit":"600"},
    expect: ["跨中最大挠度 f： 243.389 mm", "挠跨比： 1/123 （限值 1/600）"],
    ref: "EI = 32.5e9×0.08 = 2.6e9；q = 60 kN/m = 60000 N/m；f = 5×60000×30⁴/(384×2.6e9) = 0.243389 m → 243.389 mm；[f] = 30/600 = 0.05 m → 50.00 mm；挠跨比 = 30/0.243389 = 123.3 → 1/123 ⇒ 校核不通过（默认 12.821 mm / 1/1560 为通过）。**判定词「不满足/满足要求」一律不作 expect**（二值判读词）。" },
  // 原为 all_default 弱用例 + expect「单桩承担」是标签片段（逃生项）。
  // up = πd、Ap = πd²/4、侧阻 = up×Σ(qsi×li)、端阻 = qp×Ap、Ra = 侧阻+端阻、桩数 = ceil(N/Ra)。
  { slug: "bridge/foundation-calc", inputs: {"inD":"1.5","inL":"30","inQp":"1500","inQs1":"50","inL1":"8","inQs2":"70","inL2":"10","inQs3":"90","inN":"20000"},
    expect: ["单桩承载力特征值 Ra： 12923.7 kN", "总侧阻力： 10273.0 kN（侧阻合计 2180.0 kPa·m）", "需要桩数： 2 根（单桩承担 10000.0 kN）"],
    ref: "up = π×1.5 = 4.712 m；Ap = π×1.5²/4 = 1.7671 m²；侧阻区间和 = 50×8 + 70×10 + 90×(30−8−10) = 400+700+1080 = 2180 kPa·m；总侧阻 = 4.712×2180 = 10273.0 kN；端阻 = 1500×1.7671 = 2650.7 kN；Ra = 12923.7 kN；桩数 = ceil(20000/12923.7) = 2 根，单桩承担 10000.0 kN。（默认 d=1.2/L=25 得 Ra=6823.5、侧阻 5466.4，均失配）" },
  // 原为 all_default 弱用例 + expect「活载」是标签片段（逃生项）。
  // factor(等级) 与 laneReduction(车道数) 双系数同时切换：Ⅱ级 0.75、4 车道 0.67（默认 Ⅰ级 1.0、3 车道 0.78）。
  { slug: "bridge/load-calc", inputs: {"inL":"40","inB":"10","inG":"150","inGrade":"2","inLane":"4","inQp":"4.0","inBw":"1.5"},
    expect: ["跨中弯矩 M： 39171.0 kN·m（均布 36621.0 + 集中 2550.0）", "车道均布荷载 qk： 7.88 kN/m × 4 车道 × 折减 0.67 = 21.11 kN/m", "支点剪力 V： 3789.6 kN"],
    ref: "qk = 10.5×0.75 = 7.875 kN/m；Pk = (270+90×(40−5)/45)×0.75 = 340×0.75 = 255.0 kN；qLane = 7.875×4×0.67 = 21.105 → 21.11；qPeople = 4.0×(1.5×2) = 12.0；qTotal = 183.105；M均布 = 183.105×40²/8 = 36621.0、M集中 = 255×40/4 = 2550.0、M = 39171.0；V = 183.105×40/2 + 255/2 = 3789.6。默认（Ⅰ级/3 车道）M=20014.1、qk 行 = 10.50×3×0.78、V=2508.6，三串均失配。" },
  // 原为 all_default 弱用例 + expect「万元」是单位词（逃生项）。
  // 主梁混凝土 = 面积×跨径×梁数×孔数；铺装 = 桥宽×跨径×厚度×孔数；钢筋 = 混凝土×含筋率/1000；
  // 造价 = 混凝土量×单价 + 钢筋吨数×单价。
  { slug: "bridge/material-qty", inputs: {"inL":"25","inNbeam":"8","inArea":"1.0","inB":"9","inT":"0.2","inSpan":"6","inRatio":"150","inPc":"650","inPs":"5000"},
    expect: ["混凝土总量： 1470.00 m³", "钢筋用量： 180000 kg = 180.00 t（含筋率 150 kg/m³）", "材料造价： 混凝土 95.55 万 + 钢筋 90.00 万 = 185.55 万元"],
    ref: "主梁/孔 = 1.0×25×8 = 200 m³ → 全桥 200×6 = 1200 m³；铺装 = 9×25×0.2×6 = 270 m³；总量 = 1470 m³；钢筋 = 1200×150/1000 = 180.00 t（180000 kg）；造价 = 1470×650/10000 = 95.55 万 + 180×5000/10000 = 90.00 万 = 185.55 万元。默认（30/6/1.2/12/0.15/5/120/600/4500）总量 1350.00、钢筋 129.60 t、造价 139.32 万元，三串均失配。" },
  // 原为 all_default 弱用例 + expect「单孔总荷载」是标签片段（逃生项）。
  // 注意：harness 的 select 默认取**首个 option**（simple），而真机取 `selected`（continuous）⇒ 必须显式注入 inType。
  // 连续梁：内支点 M = wL²/12、跨中 M = wL²/24（简支则为 wL²/8）—— 注入后走连续梁分支。
  { slug: "bridge/span-calc", inputs: {"inLt":"400","inN":"4","inType":"continuous","inG":"180","inQ":"80"},
    expect: ["内支点最大弯矩： 216666.7 kN·m（M=(g+q)L²/12）", "单孔总荷载： 26000.0 kN", "桥墩数： 3 个（含 4 个墩台位置）"],
    ref: "L = 400/4 = 100.00 m、桥墩 = 4−1 = 3 个；w = 180+80 = 260.0 kN/m；内支点 M = 260×100²/12 = 216666.7、跨中 M = 260×100²/24 = 108333.3；单孔总荷载 = 260×100 = 26000.0 kN。默认（300/5/150/60，harness 取首个 option=simple）落在简支分支：L=60.00、桥墩 4 个、跨中 M=94500.0、单孔总荷载 12600.0，三串均失配。" }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== bridge calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();