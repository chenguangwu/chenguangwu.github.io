#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "structural/allowable-stress", inputs: { sy: "400", n: "2" }, expect: ["200.00 许用应力"], ref: "σ_allow=400/2=200" },
  { slug: "structural/angle-of-twist", inputs: { T: "800", L: "3", G: "80e9", d: "0.08" }, expect: ["0.00746 扭转角"], ref: "θ=TL/(GJ)" },
  { slug: "structural/axial-strain", inputs: { dL: "0.005", L: "2" }, expect: ["0.00250 轴向应变"], ref: "ε=0.005/2=0.0025" },
  { slug: "structural/beam-shear-stress", inputs: { V: "1000", A: "0.05" }, expect: ["30.000 最大剪应力"], ref: "τ=3V/(2A)=30000/0.1=300MPa" },
  { slug: "structural/bearing-pressure", inputs: { N: "500", A: "25" }, expect: ["20.000 基底压力"], ref: "p=500/25=20Pa?" },
  { slug: "structural/cantilever-end-moment", inputs: { F: "20", L: "3" }, expect: ["60.000 固定端弯矩"], ref: "M=20×3=60kN·m" },
  { slug: "structural/deflection-cantilever-point", inputs: { F: "500", L: "4", E: "200e9", d: "0.2" }, expect: ["0.6791 挠度"], ref: "δ=FL³/(3EI)" },
  { slug: "structural/deflection-cantilever-udl", inputs: { w: "2000", L: "3", E: "200e9", d: "0.15" }, expect: ["4.074 挠度"], ref: "δ=wL⁴/(8EI)" },
  { slug: "structural/euler-buckling", inputs: { E: "210e9", I: "2e-6", L: "3" }, expect: ["460581.5 临界载荷"], ref: "P_cr=π²EI/L²" },
  { slug: "structural/hoop-stress", inputs: { p: "3e6", r: "0.6", t: "0.02" }, expect: ["90.00 环向应力"], ref: "σ_h=pr/t=3e6×0.6/0.02=90MPa" },
  { slug: "structural/longitudinal-stress", inputs: { p: "3e6", r: "0.6", t: "0.02" }, expect: ["45.00 纵向应力"], ref: "σ_l=pr/(2t)=45MPa" },
  { slug: "structural/moment-of-inertia-rect", inputs: { b: "0.15", h: "0.25" }, expect: ["1.953e-4 惯性矩"], ref: "I=bh³/12" },
  { slug: "structural/radius-of-gyration", inputs: { I: "2e-6", A: "2e-3" }, expect: ["0.03162 回转半径"], ref: "r=√(I/A)" },
  { slug: "structural/section-modulus-rect", inputs: { b: "0.15", h: "0.25" }, expect: ["1.562e-3 截面模量"], ref: "W=bh²/6" },
  { slug: "structural/slenderness-ratio", inputs: { L: "3", r: "0.05" }, expect: ["60.00 长细比"], ref: "λ=L/r=3/0.05=60" },
  { slug: "structural/ss-point-deflection", inputs: { P: "2000", L: "4", E: "210e9", I: "2e-6" }, expect: ["6349.206 挠度"], ref: "δ=PL³/(48EI)" },
  { slug: "structural/ss-udl-moment", inputs: { w: "20", L: "6" }, expect: ["90.000 最大弯矩"], ref: "M=wL²/8=20×36/8=90" },
  { slug: "structural/stress-concentration", inputs: { Kt: "2.5", snom: "150" }, expect: ["375.00 最大应力"], ref: "σ_max=2.5×150=375" },
  { slug: "structural/thermal-strain", inputs: { a: "12e-6", dT: "200" }, expect: ["0.00240 热应变"], ref: "ε=αΔT=2.4e-3" },
  { slug: "structural/torsional-shear-shaft", inputs: { T: "1000", d: "0.06" }, expect: ["23.58 剪应力"], ref: "τ=16T/(πd³)" },
  { slug: "structural/von-mises-2d", inputs: { sx: "200e6", sy: "80e6", t: "50e6" }, expect: ["194.68 等效应力"], ref: "σ_vm=√(σx²-σxσy+σy²+3τ²)" },
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
  console.log("==== structural calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();