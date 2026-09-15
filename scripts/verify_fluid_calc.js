#!/usr/bin node
/**
 * fluid 分类计算正确性验证（覆盖 tools/fluid/ 全部 23 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed / toExponential 精确对齐），输入全避开页面默认值。
 * 用法: node scripts/verify_fluid_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "fluid/bernoulli-pressure",
    inputs: { p1: "100000", v1: "2", v2: "5", rho: "850" },
    expect: ["91075.0", "8.93"],
    ref: "p₂=p₁+½ρ(v₁²−v₂²)=100000+0.5·850·(4−25)=91075.0 Pa；压差=(100000−91075)/1000=8.93 kPa" },

  { slug: "fluid/buoyancy-force",
    inputs: { rho: "1025", V: "0.2", g: "9.81" },
    expect: ["2011.05"],
    ref: "F=ρgV=1025·9.81·0.2=2011.05 N" },

  { slug: "fluid/capillary-pressure",
    inputs: { g: "0.058", D: "0.0005" },
    expect: ["464.0"],
    ref: "ΔP=4γ/D=4·0.058/0.0005=464.0 Pa" },

  { slug: "fluid/capillary-rise",
    inputs: { gamma: "0.0728", th: "20", rho: "1000", r: "0.001", g: "9.81" },
    expect: ["13.95"],
    ref: "h=2γcosθ/(ρgr)=2·0.0728·cos20°/(1000·9.81·0.001)=0.013949 m=13.95 mm" },

  { slug: "fluid/cavitation-number",
    inputs: { p: "200000", pv: "12300", rho: "998", v: "5" },
    expect: ["15.046"],
    ref: "σ=(p−p_v)/(½ρv²)=(200000−12300)/(0.5·998·25)=15.046" },

  { slug: "fluid/chezy-velocity",
    inputs: { C: "60", R: "0.8", S: "0.002" },
    expect: ["2.400"],
    ref: "v=C√(RS)=60·√(0.8·0.002)=60·0.04=2.400 m/s" },

  { slug: "fluid/continuity-equation",
    inputs: { a1: "0.02", v1: "1.5", a2: "0.004" },
    expect: ["7.500"],
    ref: "v₂=A₁v₁/A₂=0.02·1.5/0.004=7.500 m/s" },

  { slug: "fluid/froude-number",
    inputs: { v: "4", L: "2", g: "9.81" },
    expect: ["0.903"],
    ref: "Fr=v/√(gL)=4/√(9.81·2)=4/4.42945=0.903" },

  { slug: "fluid/hydraulic-diameter",
    inputs: { A: "0.05", P: "0.9" },
    expect: ["0.2222"],
    ref: "D_h=4A/P=4·0.05/0.9=0.2222 m" },

  { slug: "fluid/hydrostatic-pressure",
    inputs: { rho: "1025", h: "25", g: "9.81" },
    expect: ["251381.3", "251.38"],
    ref: "P=ρgh=1025·9.81·25=251381.25 Pa；251381.25/1000=251.38 kPa" },

  { slug: "fluid/kinematic-viscosity",
    inputs: { mu: "0.0025", rho: "850" },
    expect: ["2.941e-6"],
    ref: "ν=μ/ρ=0.0025/850=2.941e-6 m²/s" },

  { slug: "fluid/laplace-sphere-pressure",
    inputs: { g: "0.045", R: "0.0008" },
    expect: ["112.5"],
    ref: "ΔP=2γ/R=2·0.045/0.0008=112.5 Pa" },

  { slug: "fluid/manning-velocity",
    inputs: { n: "0.02", R: "0.6", S: "0.004" },
    expect: ["2.2496"],
    ref: "v=(1/n)·R^(2/3)·√S=(1/0.02)·0.6^(2/3)·√0.004=50·0.71138·0.0632456=2.2496 m/s" },

  { slug: "fluid/minor-loss-head",
    inputs: { K: "1.5", v: "3", g: "9.81" },
    expect: ["0.6881"],
    ref: "h=Kv²/(2g)=1.5·9/(2·9.81)=13.5/19.62=0.6881 m" },

  { slug: "fluid/orifice-discharge",
    inputs: { cd: "0.6", a: "0.002", dp: "20000", rho: "900" },
    expect: ["8.000e-3"],
    ref: "Q=C_d·A·√(2Δp/ρ)=0.6·0.002·√(40000/900)=0.0012·6.66667=8.000e-3 m³/s" },

  { slug: "fluid/pitot-velocity",
    inputs: { dP: "1200", rho: "1.5" },
    expect: ["40.00"],
    ref: "v=√(2ΔP/ρ)=√(2400/1.5)=√1600=40.00 m/s" },

  { slug: "fluid/poiseuille-flow",
    inputs: { dp: "2000", r: "0.005", mu: "0.0012", L: "2" },
    expect: ["2.045e-4", "204.531"],
    ref: "Q=πΔp·r⁴/(8μL)=π·2000·6.25e-10/(8·0.0012·2)=2.045e-4 m³/s；×1e6=204.531 mL/s" },

  { slug: "fluid/pressure-drop-darcy",
    inputs: { f: "0.025", L: "25", D: "0.2", rho: "850", v: "3" },
    expect: ["11953.1"],
    ref: "ΔP=f(L/D)(ρv²/2)=0.025·(25/0.2)·(850·9/2)=0.025·125·3825=11953.125 Pa" },

  { slug: "fluid/stagnation-pressure",
    inputs: { p: "100000", rho: "1.225", v: "30" },
    expect: ["100551.3"],
    ref: "p₀=p+½ρv²=100000+0.5·1.225·900=100551.25 Pa" },

  { slug: "fluid/stokes-settling",
    inputs: { r: "2e-4", rhop: "2600", rhof: "1000", mu: "0.0015", g: "9.81" },
    expect: ["0.093013"],
    ref: "v=2r²(ρ_p−ρ_f)g/(9μ)=2·4e-8·1600·9.81/(9·0.0015)=0.093013 m/s" },

  { slug: "fluid/venturi-flow-rate",
    inputs: { A1: "0.02", A2: "0.005", dP: "2000", rho: "850" },
    expect: ["0.01120"],
    ref: "Q=A₂√(2Δp/[ρ(1−(A₂/A₁)²)])=0.005·√(4000/(850·(1−0.0625)))=0.005·2.24045=0.01120 m³/s" },

  { slug: "fluid/volume-flow-rate",
    inputs: { a: "0.35", v: "2.5" },
    expect: ["0.875", "875.0"],
    ref: "Q=Av=0.35·2.5=0.875 m³/s；×1000=875.0 L/s（默认 0.2·3=0.600 会撞车，故改此组）" },

  { slug: "fluid/weber-number",
    inputs: { rho: "850", v: "3", L: "0.05", sig: "0.03" },
    expect: ["12750.0"],
    ref: "We=ρv²L/σ=850·9·0.05/0.03=382.5/0.03=12750.0" },
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
  console.log("==== fluid calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();