#!/usr/bin node
/**
 * nuclear 分类计算正确性验证（覆盖 tools/nuclear/ 全部 28 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_nuclear_calc.js
 *   —— 目标：默认态 0 命中。
 *
 * 说明: pair-annihilation 为「常量物理事实页」——只有一个 dummy 输入，
 *       输出恒为电子静质量对应的 511.0 / 1022.0 keV，不随输入变化，
 *       无法用输入区分，故不作输入驱动断言（不纳入 CASES）。
 *
 * 跑法:
 *   node scripts/verify_nuclear_calc.js                # 全部
 *   node scripts/verify_nuclear_calc.js carbon-dating-age  # 单页
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "nuclear/absorbed-dose",
    inputs: { E: "0.3", m: "4" },
    expect: ["0.0750"],
    ref: "D=E/m=0.3/4=0.0750 Gy" },

  { slug: "nuclear/activity",
    inputs: { lam: "2.5e-9", n: "3e20" },
    expect: ["7.500e+11", "2.027e+1"],
    ref: "A=λN=2.5e-9×3e20=7.500e+11 Bq；7.500e+11/3.7e10=2.027e+1 Ci" },

  { slug: "nuclear/activity-decay",
    inputs: { a0: "250", lam: "0.002", t: "300" },
    expect: ["137.203"],
    ref: "A=A₀e^(−λt)=250×e^(−0.6)=137.203 Bq" },

  { slug: "nuclear/activity-from-halflife",
    inputs: { th: "3.8e8", N: "5e18" },
    expect: ["9.120e+9"],
    ref: "A=(ln2/t½)·N=0.69314718056/3.8e8×5e18=9.120e+9 Bq" },

  { slug: "nuclear/age-from-activity",
    inputs: { lam: "1.5e-11", N0: "2e20", N: "6e19" },
    expect: ["2543"],
    ref: "t=(1/λ)ln(N₀/N)=(1/1.5e-11)·ln(3.3333)=8.029e10 s ÷3.156e7=2543 年" },

  { slug: "nuclear/binding-energy",
    inputs: { dm: "0.35" },
    expect: ["5.223e-11", "326.023"],
    ref: "BE=Δm·u·c²=0.35×1.66053906660e-27×c²=5.223e-11 J=326.023 MeV" },

  { slug: "nuclear/binding-energy-per-nucleon",
    inputs: { dm: "0.6", a: "40" },
    expect: ["13.972"],
    ref: "BE/A=(0.6 u→MeV)/40=558.883/40=13.972 MeV/核子" },

  { slug: "nuclear/carbon-dating-age",
    inputs: { th: "5730", frac: "0.25" },
    expect: ["11460"],
    ref: "t=(t½/ln2)·ln(1/f)=5730/0.69314718056×ln4=11460 年（两个半衰期）" },

  { slug: "nuclear/decay-constant",
    inputs: { th: "4320" },
    expect: ["1.6045e-4"],
    ref: "λ=ln2/t½=0.69314718056/4320=1.6045e-4 年⁻¹" },

  { slug: "nuclear/decay-constant-from-halflife",
    inputs: { th: "5.2e10" },
    expect: ["1.333e-11"],
    ref: "λ=ln2/t½=0.69314718056/5.2e10=1.333e-11 s⁻¹" },

  { slug: "nuclear/decay-fraction",
    inputs: { lam: "3e-9", t: "2e8" },
    expect: ["0.4512"],
    ref: "f=1−e^(−λt)=1−e^(−0.6)=0.4512（已衰变 45.12%）" },

  { slug: "nuclear/dose-equivalent",
    inputs: { D: "1.5", Q: "5" },
    expect: ["7.50"],
    ref: "H=D·Q=1.5×5=7.50 Sv" },

  { slug: "nuclear/effective-halflife",
    inputs: { tp: "12", tb: "45" },
    expect: ["9.47"],
    ref: "1/t_eff=1/12+1/45 → t_eff=9.47 天（小于任一分量）" },

  { slug: "nuclear/fission-energy-yield",
    inputs: { n: "2e22", ef: "180" },
    expect: ["5.768e+11", "160.218"],
    ref: "E=N·E_f·1e6·e=2e22×180×1e6×1.602176634e-19=5.768e+11 J=160.218 kWh" },

  { slug: "nuclear/gamma-attenuation",
    inputs: { I0: "250", mu: "0.15", x: "8" },
    expect: ["75.299"],
    ref: "I=I₀e^(−μx)=250×e^(−1.2)=75.299（衰减约 70%）" },

  { slug: "nuclear/half-life-from-activity-nuclei",
    inputs: { N: "4e18", A: "2.2e9" },
    expect: ["40"],
    ref: "t½=N·ln2/A=4e18×0.69314718056/2.2e9=1.260e9 s ÷3.156e7=40 年" },

  { slug: "nuclear/half-life-from-lambda",
    inputs: { lam: "3.2e-4" },
    expect: ["2166.08"],
    ref: "t½=ln2/λ=0.69314718056/3.2e-4=2166.08 年" },

  { slug: "nuclear/mass-defect",
    inputs: { z: "8", nn: "8", M: "15.9949" },
    expect: ["0.13263", "123.545"],
    ref: "Δm=(Z·m_p+N·m_n−M·u)/u=0.13263 u → 123.545 MeV（氧-16）" },

  { slug: "nuclear/mean-life",
    inputs: { th: "2400" },
    expect: ["3462.47"],
    ref: "τ=t½/ln2=2400/0.69314718056=3462.47 年" },

  { slug: "nuclear/mean-life-from-halflife",
    inputs: { th: "1600" },
    expect: ["2308.3"],
    ref: "τ=t½/ln2=1600/0.69314718056=2308.3 年" },

  { slug: "nuclear/nuclear-radius",
    inputs: { A: "125" },
    expect: ["6.000"],
    ref: "R=r₀·A^(1/3)=1.2 fm×∛125=1.2×5=6.000 fm" },

  // 注意：默认态（4.0026/4.0015）为「放能反应」，若断言放能文本会在默认态即命中（假通过）。
  // 故改用吸能分支输入，既验证判定分支又在默认态不命中。
  { slug: "nuclear/q-value",
    inputs: { mi: "13.9990", mf: "14.0032" },
    expect: ["-3.9123", "吸能反应"],
    ref: "Q=(m_i−m_f)·u·c²=(−0.0042 u)→−3.9123 MeV<0，故为吸能反应" },

  { slug: "nuclear/radioactive-decay",
    inputs: { n0: "5000", lam: "0.0015", t: "400" },
    expect: ["2744.06", "54.88"],
    ref: "N=N₀e^(−λt)=5000×e^(−0.6)=2744.06；剩余比例 54.88%" },

  { slug: "nuclear/reaction-rate",
    inputs: { F: "2e14", s: "5e-28", N: "3e21" },
    expect: ["3.000e+8"],
    ref: "R=Φ·σ·N=2e14×5e-28×3e21=3.000e+8 s⁻¹" },

  { slug: "nuclear/specific-activity",
    inputs: { th: "1600", M: "40" },
    expect: ["2.067e+14"],
    ref: "λ=ln2/(1600×365.25×86400)；a=λ·N_A/(M/1000)=2.067e+14 Bq/kg" },

  { slug: "nuclear/specific-activity-from-halflife",
    inputs: { th: "2.4e9", M: "60" },
    expect: ["2.899e+12"],
    ref: "a=(ln2/t½)·N_A/M=0.69314718056/2.4e9×6.02214076e23/60=2.899e+12 Bq/g" },

  { slug: "nuclear/survival-probability",
    inputs: { lam: "4e-9", t: "1.5e8" },
    expect: ["0.5488"],
    ref: "P=e^(−λt)=e^(−0.6)=0.5488（与 decay-fraction 互补）" },
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
  console.log("==== nuclear calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();