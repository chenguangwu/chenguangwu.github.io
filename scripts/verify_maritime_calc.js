#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "maritime/anchorage-capacity", inputs: {"shipLength":"250","waterDepth":"25","scopeFactor":"6","safetyMargin":"60","anchorageArea":"8","layoutMode":"grid"}, expect: ["150.0 出链长度 (m)","846,400 单船面积 (m²)","9 可容船舶数"], ref: "出链 25×6 = 150.0 m、旋回 150+250+60 = 460.0 m；方格排布 920² = 846,400 m²/船 ⇒ floor(8,000,000/846,400) = 9 艘（默认 200/20/5/50/5 圆形 ⇒ 100.0/350.0/384,845/12 艘）；layoutMode=grid 必须显式注入（harness 取首个 option=circle）" },
  { slug: "maritime/compass-correction", inputs: {"variation":"8","deviation":"-2","convertDir":"t2c","headingInput":"100"}, expect: ["094.0° 罗航向 CH","092.0° 磁航向 MH","6.0°E 罗经差"], ref: "t2c：TH 100 → MH = 100−8 = 92 → CH = 92−(−2) = 94；罗经差 Dev+Var = −2+8 = 6.0°E（默认 c2t/45/-5/3 ⇒ CH 045.0°、CH 43.0°、2.0°W）；convertDir=t2c 必须显式注入（harness 取首个 option=c2t）" },
  { slug: "maritime/speed-distance", inputs: {"calcTarget":"time","speedValue":"18","distValue":"450"}, expect: ["25.00 时间 (小时)","450.00 航程 (海里)","1天 1小时"], ref: "目标=航行时间：450 nm ÷ 18 kn = 25.00 h、易读 1天 1小时（默认 目标=航程 15×12 = 180.00 nm）；calcTarget=time 必须显式注入（harness 取首个 option=distance）" },
  { slug: "maritime/stowage-factor", inputs: {"calcMode":"capacity","sfInput":"0.8","totalWeight":"6000","holdCapacity":"9000","dwt":"7000"}, expect: ["4,800 所需舱容 (m³)","53.3% 舱容利用率","7,000 最大装载 (吨)"], ref: "capacity 模式：所需舱容 6000×0.8 = 4,800 m³、舱容利用率 4800/9000 = 53.3%、载重利用率 6000/7000 = 85.7%；舱容上限 9000/0.8 = 11,250 t > DWT 7,000 t ⇒ 载重受限，最大装载 7,000 t（默认 sf 模式 ⇒ 1.667 m³/t/59.80/0.600，完全不同分支）；calcMode=capacity 必须显式注入（harness 取首个 option=sf）。**注**：本页 onCargoChange() 与 compass 类无参联动函数同名同型，兜底阶段会把 volume/weight/sfInput 覆盖回 custom 预设（100/60/1.5）⇒ 最终 dump 显示 1.5，但 expect 在注入阶段判定（via=input event）" },
  { slug: "maritime/tide-window", inputs: {"draft":"6.0","ukc":"0.8","chartDepth":"4.0"}, expect: ["2.80 所需潮高 (m)","1.70 潮高余量 (m)"], ref: "所需潮高 = 吃水 6.0 + UKC 0.8 − 海图水深 4.0 = 2.80 m、潮高余量 = 高潮 4.50 − 2.80 = 1.70 m（默认 5.0/0.5/3.0 ⇒ 2.50 m、2.00 m）；时间用页面默认值（14:20/08:05/20:15，type=time 可注入但无需改）" }
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
  console.log("==== maritime calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();