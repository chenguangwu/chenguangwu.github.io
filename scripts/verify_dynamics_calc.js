#!/usr/bin/env node
/**
 * dynamics 分类计算正确性验证（23 个确定性数值工具，全覆盖）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 用法: node scripts/verify_dynamics_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "dynamics/angular-momentum-conservation",
    inputs: { I1: "4", w1: "6", I2: "2" },
    expect: ["12.000"],
    ref: "ω₂=I1·ω1/I2=4·6/2=12.000 rad/s" },

  { slug: "dynamics/angular-momentum",
    inputs: { I: "2", w: "3" },
    expect: ["6.000"],
    ref: "L=I·ω=2·3=6.000 kg·m²/s" },

  { slug: "dynamics/banked-curve",
    inputs: { r: "200", th: "45", g: "9.81" },
    expect: ["44.29"],
    ref: "v=√(r·g·tanθ)=√(200·9.81·1)=44.29 m/s" },

  { slug: "dynamics/coefficient-restitution",
    inputs: { v1: "10", v2: "2", v1p: "4", v2p: "5" },
    expect: ["0.125"],
    ref: "e=(v2p−v1p)/(v1−v2)=(5−4)/(10−2)=0.125" },

  { slug: "dynamics/elastic-collision-1d",
    inputs: { m1: "3", m2: "5", v1: "6", v2: "2" },
    expect: ["1.000", "5.000"],
    ref: "一维弹性碰撞：v1′=((m1−m2)v1+2m2v2)/(m1+m2)=1.000；v2′=(2m1v1−(m1−m2)v2)/(m1+m2)=5.000" },

  { slug: "dynamics/hooke-force",
    inputs: { k: "150", x: "0.2" },
    expect: ["30.00"],
    ref: "F=k·x=150·0.2=30.00 N" },

  { slug: "dynamics/impulse",
    inputs: { F: "250", dt: "0.4" },
    expect: ["100.00"],
    ref: "J=F·Δt=250·0.4=100.00 N·s" },

  { slug: "dynamics/inclined-plane-accel",
    inputs: { th: "45", mu: "0.2", g: "9.8" },
    expect: ["5.544"],
    ref: "a=g(sinθ−μcosθ)=9.8(sin45−0.2cos45)=5.544 m/s²" },

  { slug: "dynamics/inelastic-collision",
    inputs: { m1: "4", m2: "6", v1: "5", v2: "2" },
    expect: ["3.200"],
    ref: "v=(m1v1+m2v2)/(m1+m2)=(4·5+6·2)/10=3.200 m/s" },

  { slug: "dynamics/kinetic-friction",
    inputs: { mu: "0.25", N: "200" },
    expect: ["50.00"],
    ref: "Fk=μ·N=0.25·200=50.00 N" },

  { slug: "dynamics/moment-of-inertia-point",
    inputs: { m: "3", r: "0.4" },
    expect: ["0.480"],
    ref: "I=m·r²=3·0.4²=0.480 kg·m²" },

  { slug: "dynamics/momentum-conservation",
    inputs: { m1: "2000", v1: "15", m2: "1000", v2: "10" },
    expect: ["13.333"],
    ref: "v′=(m1v1+m2v2)/(m1+m2)=(2000·15+1000·10)/3000=13.333 m/s" },

  { slug: "dynamics/momentum",
    inputs: { m: "1200", v: "25" },
    expect: ["30000.0"],
    ref: "p=m·v=1200·25=30000.0 kg·m/s" },

  { slug: "dynamics/period-pendulum",
    inputs: { L: "2.5", g: "9.81" },
    expect: ["3.172"],
    ref: "T=2π√(L/g)=2π√(2.5/9.81)=3.172 s" },

  { slug: "dynamics/power-force",
    inputs: { F: "3000", v: "8" },
    expect: ["24000.0", "24.00"],
    ref: "P=F·v=3000·8=24000.0 W；kW=24.00" },

  { slug: "dynamics/power-rotational",
    inputs: { tau: "7", w: "3" },
    expect: ["21.00"],
    ref: "P=τ·ω=7·3=21.00 W" },

  { slug: "dynamics/rotational-kinetic-energy",
    inputs: { I: "2", w: "4" },
    expect: ["16.000"],
    ref: "E=½Iω²=0.5·2·4²=16.000 J" },

  { slug: "dynamics/spring-potential",
    inputs: { k: "300", x: "0.2" },
    expect: ["6.000"],
    ref: "U=½k·x²=0.5·300·0.2²=6.000 J" },

  { slug: "dynamics/static-friction-max",
    inputs: { mu: "0.4", N: "250" },
    expect: ["100.00"],
    ref: "Fmax=μ·N=0.4·250=100.00 N" },

  { slug: "dynamics/terminal-velocity",
    inputs: { m: "100", g: "9.81", rho: "1.225", cd: "0.8", A: "0.5" },
    expect: ["63.28"],
    ref: "vt=√(2mg/(ρ·Cd·A))=√(2·100·9.81/(1.225·0.8·0.5))=63.28 m/s" },

  { slug: "dynamics/torque-force",
    inputs: { r: "0.3", F: "200", th: "60" },
    expect: ["51.96"],
    ref: "τ=r·F·sinθ=0.3·200·sin60=51.96 N·m" },

  { slug: "dynamics/weight-force",
    inputs: { m: "85", g: "9.8" },
    expect: ["833.00", "84.91"],
    ref: "W=m·g=85·9.8=833.00 N；kgf=833/9.81=84.91" },

  { slug: "dynamics/work-energy-theorem",
    inputs: { m: "5", v1: "2", v2: "8" },
    expect: ["150.00"],
    ref: "W=½m(v2²−v1²)=0.5·5·(64−4)=150.00 J" },
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
  console.log(`\n==== dynamics calc ${pass}/${cases.length} ====`);
  if (errs.length) { console.log("\nfailed:"); errs.forEach((c) => console.log(`  - ${c.slug}: ${JSON.stringify(c.expect)}`)); process.exit(1); }
}

main();
