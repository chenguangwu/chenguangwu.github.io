#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "ceramics/clay-shrinkage",
  "inputs": {
    "wet": "150",
    "dry": "135",
    "fired": "120",
    "targetFired": "200",
    "totalShrink": "18"
  },
  "clicks": [
    "calc();calcReverse()"
  ],
  "expect": [
    "20.00%",
    "10.00%",
    "11.11%",
    "243.90"
  ],
  "ref": "S干=(150−135)/150=10.00%、S烧=(135−120)/135=11.11%、S总=(150−120)/150=20.00%（独立复算）；反向 L₀=L₂/(1−S总)=200/(1−0.18)=243.90 mm。默认 120/112/100 ⇒ 6.67% / 10.71% / 16.67%、L₀=116.28 ⇒ 四个锚点全不命中。原 expect「公式」是 calcReverse 的 step-line 标签常量（默认态同样渲染）⇒ 已替换。"
},
{
  "slug": "ceramics/glaze-ratio",
  "inputs": {
    "totalW": "1500",
    "w_'+idx+'": "-"
  },
  "expect": [
    "375.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ceramics/glaze-temp",
  "inputs": {
    "coneTargetTemp": "1150"
  },
  "expect": [
    "最接近测温锥：4 · 1142°C · 中温"
  ],
  "ref": "改用页面真实计算输入：#coneTargetTemp（默认 1200，oninput=__coneLookup）。注入 1150 ⇒ 与 CONES 最近的锥 4（1142°C，中温），差值 +8°C（「高于锥号 4（1142°C）8°C」）、华氏 ≈2102.0 °F，判定在 ±30°C 容差内。原断言「1060°C」是默认全量表 CONES 的常量行（锥 01），与输入无关 ⇒ 零判别力，且该页本就有可注入的计算器，无需以 no_inputs 兜底。"
},
{
  "slug": "ceramics/kiln-firing",
  "clicks": ["switchTab('porcelain');"],
  "expect": [
    "峰值温度 1300°C，总烧成时间 约 12~15 小时。"
  ],
  "ref": "独立复算：SCHED.porcelain = {peak:1300, totalDesc:'约 12~15 小时'}；switchTab() 把 cur 换成 'porcelain' 后 render() 从 SCHED[cur] 取峰值与总时长，渲染「峰值温度 1300°C，总烧成时间 约 12~15 小时。」；默认 cur='bisque'（980°C / 约 8~10 小时）⇒ 串不同。switchTab(t,btn) 的 btn 有 if(btn) 判空，可省略。"
},
{
  "slug": "ceramics/wheel-speed",
  "inputs": {
    "diameter": "23"
  },
  "expect": [
    "0.230"
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

  console.log("==== ceramics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
