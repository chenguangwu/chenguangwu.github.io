#!/usr/bin node
/**
 * electromagnetism 分类计算正确性验证（覆盖 tools/electromagnetism/ 全部 26 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed / toExponential 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_electromagnetism_calc.js
 *   —— 除 free-space-impedance（常数页无有效输入字段，默认态命中为其固有属性）外，其余用例默认态 0 命中。
 * 用法: node scripts/verify_electromagnetism_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "electromagnetism/b-field-wire",
    inputs: { I: "5", r: "0.02" },
    expect: ["5.000e-5", "50.00"],
    ref: "B=μ₀I/(2πr)=4π·1e-7·5/(2π·0.02)=5e-5 T；B·1e6=50 µT" },

  { slug: "electromagnetism/capacitance-parallel-plate",
    inputs: { A: "0.02", d: "0.002", er: "2" },
    expect: ["177.084"],
    ref: "C=ε₀εr·A/d=8.854e-12·2·0.02/0.002=1.7708e-10 F=177.084 pF" },

  { slug: "electromagnetism/capacitive-reactance",
    inputs: { C: "2", f: "50" },
    expect: ["1591.55", "-1591.55"],
    ref: "X_C=1/(2π·f·C)=1/(2π·50·2e-6)=1591.55 Ω；虚部=−X_C" },

  { slug: "electromagnetism/capacitors-parallel",
    inputs: { C1: "15", C2: "33" },
    expect: ["48.0000", "10.3125"],
    ref: "C=C₁+C₂=15+33=48 µF；串联等效=1/(1/15+1/33)=10.3125 µF" },

  { slug: "electromagnetism/capacitors-series",
    inputs: { C1: "4", C2: "4" },
    expect: ["2.0000", "8.0000"],
    ref: "C=1/(1/4+1/4)=2 µF；并联等效=4+4=8 µF" },

  { slug: "electromagnetism/coil-torque",
    inputs: { N: "150", I: "0.8", A: "0.02", B: "0.25", th: "30" },
    expect: ["0.3000"],
    ref: "τ=N·I·A·B·sinθ=150·0.8·0.02·0.25·sin30°=0.3000 N·m" },

  { slug: "electromagnetism/current-density",
    inputs: { I: "8", A: "2e-6" },
    expect: ["4.000e+6"],
    ref: "J=I/A=8/2e-6=4e6 A/m²" },

  { slug: "electromagnetism/drift-velocity",
    inputs: { I: "2", n: "5e28", A: "3e-6" },
    expect: ["8.322e-5"],
    ref: "v_d=I/(n·A·e)=2/(5e28·3e-6·1.602e-19)=8.322e-5 m/s" },

  { slug: "electromagnetism/electric-potential-point",
    inputs: { q: "2e-6", r: "4" },
    expect: ["4493.776"],
    ref: "V=k·q/r=8.98755e9·2e-6/4=4493.776 V" },

  { slug: "electromagnetism/electric-power",
    inputs: { V: "24", I: "3.5" },
    expect: ["84.000", "0.0840"],
    ref: "P=V·I=24·3.5=84.000 W；84/1000=0.0840 kW" },

  { slug: "electromagnetism/energy-capacitor",
    inputs: { C: "2e-6", V: "10" },
    expect: ["100.000", "1.000e-4"],
    ref: "E=½CV²=0.5·2e-6·100=1e-4 J=100 µJ" },

  { slug: "electromagnetism/energy-inductor",
    inputs: { L: "0.25", I: "3" },
    expect: ["1.1250"],
    ref: "E=½LI²=0.5·0.25·9=1.1250 J" },

  { slug: "electromagnetism/faraday-induction",
    inputs: { N: "100", dPhi: "0.002", dt: "0.1" },
    expect: ["2.0000", "0.020000"],
    ref: "ε=N·|ΔΦ|/Δt=100·0.002/0.1=2 V；每匝=2/100=0.02 V" },

  { slug: "electromagnetism/force-wire-field",
    inputs: { B: "0.8", I: "5", L: "0.3", th: "30" },
    expect: ["0.6000"],
    ref: "F=B·I·L·sinθ=0.8·5·0.3·sin30°=0.6000 N" },

  { slug: "electromagnetism/free-space-impedance",
    inputs: { x: "0" },
    expect: ["376.73"],
    ref: "Z₀=√(μ₀/ε₀)=376.73 Ω（常数页，页面无有效输入字段，默认态命中属固有；已用 selfcheck_false_pass.js 标注为例外）" },

  { slug: "electromagnetism/inductance-solenoid",
    inputs: { N: "250", A: "0.02", l: "0.5" },
    expect: ["3.1416"],
    ref: "L=μ₀N²A/l=4πe-7·250²·0.02/0.5=3.1416e-3 H=3.1416 mH" },

  { slug: "electromagnetism/lc-resonance",
    inputs: { L: "4", C: "9" },
    expect: ["838.82", "0.8388"],
    ref: "L=4 mH, C=9 µF → f=1/(2π√(LC))=838.82 Hz=0.8388 kHz" },

  { slug: "electromagnetism/magnetic-flux",
    inputs: { B: "0.004", A: "0.025" },
    expect: ["1.000e-4", "100.00"],
    ref: "Φ=B·A=0.004·0.025=1.000e-4 Wb；×1e6=100.00 µWb" },

  { slug: "electromagnetism/ohms-law",
    inputs: { I: "2", R: "50", V: "5" },
    expect: ["100.00", "200.000"],
    ref: "V 模式：V=I·R=2·50=100 V；P=V·I=100·2=200 W" },

  { slug: "electromagnetism/resistivity-law",
    inputs: { rho: "2.5e-8", L: "3", A: "2e-6" },
    expect: ["0.03750"],
    ref: "R=ρL/A=2.5e-8·3/2e-6=0.03750 Ω" },

  { slug: "electromagnetism/resistors-parallel",
    inputs: { R1: "15", R2: "30" },
    expect: ["10.000", "0.1000"],
    ref: "R=1/(1/15+1/30)=10.000 Ω；总倒导=1/10=0.1000 1/Ω" },

  { slug: "electromagnetism/resistors-series",
    inputs: { R1: "15", R2: "25", R3: "35" },
    expect: ["75.000", "0.01333"],
    ref: "R=15+25+35=75.000 Ω；总倒导=1/75=0.01333 1/Ω" },

  { slug: "electromagnetism/rl-time-constant",
    inputs: { L: "0.5", R: "25" },
    expect: ["0.0200"],
    ref: "τ=L/R=0.5/25=0.0200 s" },

  { slug: "electromagnetism/solenoid-field",
    inputs: { n: "2000", I: "3" },
    expect: ["7.540e-3", "7.540"],
    ref: "B=μ₀·n·I=4πe-7·2000·3=7.540e-3 T=7.540 mT" },

  { slug: "electromagnetism/inductors-parallel",
    inputs: { L1: "3", L2: "6" },
    expect: ["2.0000", "0.5000"],
    ref: "L=1/(1/3+1/6)=2.0000 mH；总倒感=1/2=0.5000 1/mH" },

  { slug: "electromagnetism/inductors-series",
    inputs: { L1: "3", L2: "5" },
    expect: ["8.0000", "1.8750"],
    ref: "L=3+5=8.0000 mH；并联等效=1/(1/3+1/5)=1.8750 mH" },
];


async function main() {
  const only = process.argv.slice(2);
  const cases = only.length
    ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o))
    : CASES;
  let pass = 0; const errs = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) { pass++; console.log(`  OK ${c.slug} (${r.via})`); }
    else { errs.push(c); console.log(`  NG ${c.slug} -- expect ${JSON.stringify(c.expect)}`);
      if (r.why) console.log(`     why: ${r.why}`);
      if (r.errs && r.errs.length) console.log(`     errs: ${JSON.stringify(r.errs)}`);
      if (r.sample) console.log(`     got: ${String(r.sample).slice(0, 400)}`); }
  }
  console.log(`\n==== electromagnetism calc ${pass}/${cases.length} ====`);
  if (errs.length) { console.log("\nfailed:"); errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`)); process.exit(1); }
}

main();
