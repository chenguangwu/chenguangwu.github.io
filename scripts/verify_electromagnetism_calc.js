#!/usr/bin node
/**
 * electromagnetism 分类计算正确性验证（覆盖 tools/electromagnetism/ 全部 26 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed / toExponential 精确对齐），输入全避开页面默认值。
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
    inputs: { C1: "10", C2: "22" },
    expect: ["32.0000", "6.8750"],
    ref: "C=10+22=32 µF；串联等效=1/(1/10+1/22)=6.8750 µF" },

  { slug: "electromagnetism/capacitors-series",
    inputs: { C1: "4", C2: "4" },
    expect: ["2.0000", "8.0000"],
    ref: "C=1/(1/4+1/4)=2 µF；并联等效=4+4=8 µF" },

  { slug: "electromagnetism/coil-torque",
    inputs: { N: "200", I: "0.5", A: "0.01", B: "0.1", th: "90" },
    expect: ["0.1000"],
    ref: "τ=N·I·A·B·sinθ=200·0.5·0.01·0.1·1=0.1000 N·m" },

  { slug: "electromagnetism/current-density",
    inputs: { I: "5", A: "1e-6" },
    expect: ["5.000e+6"],
    ref: "J=I/A=5/1e-6=5e6 A/m²" },

  { slug: "electromagnetism/drift-velocity",
    inputs: { I: "1", A: "1e-6", n: "8.5e28" },
    expect: ["7.343e-5"],
    ref: "v_d=I/(n·A·e)=1/(8.5e28·1e-6·1.602e-19)=7.343e-5 m/s" },

  { slug: "electromagnetism/electric-potential-point",
    inputs: { q: "2e-6", r: "2" },
    expect: ["8987.552"],
    ref: "V=k·q/r=8.98755e9·2e-6/2=8987.552 V" },

  { slug: "electromagnetism/electric-power",
    inputs: { V: "12", I: "2" },
    expect: ["24.000", "0.0240"],
    ref: "P=V·I=12·2=24 W；P/1000=0.0240 kW" },

  { slug: "electromagnetism/energy-capacitor",
    inputs: { C: "2e-6", V: "10" },
    expect: ["100.000", "1.000e-4"],
    ref: "E=½CV²=0.5·2e-6·100=1e-4 J=100 µJ" },

  { slug: "electromagnetism/energy-inductor",
    inputs: { L: "0.1", I: "2" },
    expect: ["0.2000"],
    ref: "E=½LI²=0.5·0.1·4=0.2000 J" },

  { slug: "electromagnetism/faraday-induction",
    inputs: { N: "100", dPhi: "0.002", dt: "0.1" },
    expect: ["2.0000", "0.020000"],
    ref: "ε=N·|ΔΦ|/Δt=100·0.002/0.1=2 V；每匝=2/100=0.02 V" },

  { slug: "electromagnetism/force-wire-field",
    inputs: { B: "0.5", I: "10", L: "0.2", th: "90" },
    expect: ["1.0000"],
    ref: "F=B·I·L·sinθ=0.5·10·0.2·1=1.0000 N" },

  { slug: "electromagnetism/free-space-impedance",
    inputs: {},
    expect: ["376.73"],
    ref: "Z₀=√(μ₀/ε₀)=√(4π·1e-7/8.854e-12)=376.73 Ω" },

  { slug: "electromagnetism/inductance-solenoid",
    inputs: { N: "100", A: "0.01", l: "0.2" },
    expect: ["0.6283"],
    ref: "L=μ₀N²A/l=4π·1e-7·100²·0.01/0.2=6.283e-4 H=0.6283 mH" },

  { slug: "electromagnetism/lc-resonance",
    inputs: { L: "1", C: "1" },
    expect: ["5032.92", "5.0329"],
    ref: "f=1/(2π√(LC))，L=1mH,C=1µF → f=5032.92 Hz=5.0329 kHz" },

  { slug: "electromagnetism/magnetic-flux",
    inputs: { B: "0.001", A: "0.01" },
    expect: ["1.000e-5", "10.00"],
    ref: "Φ=B·A=0.001·0.01=1e-5 Wb；Φ·1e6=10 µWb" },

  { slug: "electromagnetism/ohms-law",
    inputs: { I: "2", R: "50", V: "5" },
    expect: ["100.00", "200.000"],
    ref: "V 模式：V=I·R=2·50=100 V；P=V·I=100·2=200 W" },

  { slug: "electromagnetism/resistivity-law",
    inputs: { rho: "1.68e-8", L: "1", A: "1e-6" },
    expect: ["0.01680"],
    ref: "R=ρL/A=1.68e-8·1/1e-6=0.01680 Ω" },

  { slug: "electromagnetism/resistors-parallel",
    inputs: { R1: "10", R2: "10" },
    expect: ["5.000", "0.2000"],
    ref: "R=1/(1/10+1/10)=5 Ω；电导=1/5=0.2000 S" },

  { slug: "electromagnetism/resistors-series",
    inputs: { R1: "10", R2: "20", R3: "30" },
    expect: ["60.000", "0.01667"],
    ref: "R=10+20+30=60 Ω；电导=1/60=0.01667 S" },

  { slug: "electromagnetism/rl-time-constant",
    inputs: { L: "0.1", R: "10" },
    expect: ["0.0100"],
    ref: "τ=L/R=0.1/10=0.0100 s" },

  { slug: "electromagnetism/solenoid-field",
    inputs: { n: "1000", I: "1" },
    expect: ["1.257e-3", "1.257"],
    ref: "B=μ₀·n·I=4π·1e-7·1000·1=1.257e-3 T=1.257 mT" },

  { slug: "electromagnetism/inductors-parallel",
    inputs: { L1: "2", L2: "2" },
    expect: ["1.0000", "1.0000"],
    ref: "L=1/(1/2+1/2)=1 mH；总倒感=1/1=1 1/mH" },

  { slug: "electromagnetism/inductors-series",
    inputs: { L1: "1", L2: "2" },
    expect: ["3.0000", "0.6667"],
    ref: "L=1+2=3 mH；并联等效=1/(1/1+1/2)=0.6667 mH" },
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
