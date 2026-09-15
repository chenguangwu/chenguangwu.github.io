#!/usr/bin/env node
/**
 * 第 46 道门禁：acoustics 分类计算正确性验证（28 个确定性数值工具，全覆盖）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值（resetForm 预设），且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * acoustics 目录 28 页全部为纯数值计算（calcTool + num()），无外部状态依赖，故全覆盖。
 * 用法: node scripts/verify_acoustics_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "acoustics/absorption-coeff-sabine",
    inputs: { V: "200", S: "150", rt: "1.5" },
    expect: ["0.143", "21.47"],
    ref: "ᾱ=0.161×200/(150×1.5)=0.143；总吸声量 A=ᾱ×S=0.143×150=21.47（默认 100/130/0.8→0.155，避开）" },

  { slug: "acoustics/acoustic-impedance",
    inputs: { rho: "1.4", c: "340" },
    expect: ["476.0"],
    ref: "Z=ρ·c=1.4×340=476.0（默认 1.2/343→411.6，避开）" },

  { slug: "acoustics/beat-frequency",
    inputs: { f1: "500", f2: "506" },
    expect: ["6.00", "503.00"],
    ref: "拍频=|500−506|=6.00；平均=(500+506)/2=503.00（默认 440/444→4.00，避开）" },

  { slug: "acoustics/combine-two-spl",
    inputs: { l1: "90", l2: "84" },
    expect: ["90.97", "0.97"],
    ref: "L=10·log₁₀(10⁹+10^8.4)=90.97；比响者高出=90.97−90=0.97（默认 80/80→83.01，避开）" },

  { slug: "acoustics/critical-distance",
    inputs: { V: "400", rt: "2.0", Q: "2" },
    expect: ["2.82"],
    ref: "r_c=0.141·√(2×400/2)=0.141×20=2.82（默认 200/1.0/1→1.99，避开）" },

  { slug: "acoustics/decibel-power-ratio",
    inputs: { p1: "4", p2: "64" },
    expect: ["12.04", "16.000"],
    ref: "L=10·log₁₀(64/4)=10·log₁₀(16)=12.04；线性比=16.000（默认 1/10→10.00，避开）" },

  { slug: "acoustics/decibel-power",
    inputs: { P: "100", P0: "2" },
    expect: ["16.99", "50.000"],
    ref: "L=10·log₁₀(100/2)=16.99；功率比=50.000（默认 10/1→10.00，避开）" },

  { slug: "acoustics/decibel-voltage-ratio",
    inputs: { v1: "3", v2: "30" },
    expect: ["20.00", "10.000"],
    ref: "L=20·log₁₀(30/3)=20.00；线性比=10.000（默认 1/3.16→9.99，避开）" },

  { slug: "acoustics/decibel-voltage",
    inputs: { V: "50", V0: "2" },
    expect: ["27.96", "25.000"],
    ref: "L=20·log₁₀(50/2)=27.96；电压比=25.000（默认 10/1→20.00，避开）" },

  { slug: "acoustics/doppler-acoustic",
    inputs: { f: "500", v: "340", vs: "40" },
    expect: ["566.67", "66.67"],
    ref: "f′=500×340/(340−40)=170000/300=566.67；偏移=66.67（默认 440/343/34.3→488.89，避开）" },

  { slug: "acoustics/freq-to-note",
    inputs: { f: "1000" },
    expect: ["B5", "83", "+21"],
    ref: "MIDI=69+12·log₂(1000/440)=83.206→round=83；音名=NAMES[11]+(floor(83/12)−1)=B5；音分=round(0.206×100)=+21（默认 440→A4，避开）" },

  { slug: "acoustics/intensity-inverse-square",
    inputs: { I1: "200", r1: "2", r2: "4" },
    expect: ["50.00", "136.99"],
    ref: "I₂=200×(2/4)²=50.00；声强级=10·log₁₀(50/1e-12)=136.99（默认 100/1/2→25.00，避开）" },

  { slug: "acoustics/intensity-level",
    inputs: { I: "1e-4" },
    expect: ["80.00"],
    ref: "L_I=10·log₁₀(1e-4/1e-12)=10·log₁₀(1e8)=80.00（默认 1e-6→60.00，避开）" },

  { slug: "acoustics/mass-law-tl",
    inputs: { f: "1000", m: "20" },
    expect: ["38.02"],
    ref: "TL=20·log₁₀(1000×20)−48=20·log₁₀(20000)−48=86.02−48=38.02（默认 500/10→25.98，避开）" },

  { slug: "acoustics/pipe-closed",
    inputs: { v: "340", L: "0.4" },
    expect: ["212.50", "637.50"],
    ref: "f₁=340/(4×0.4)=212.50；三次谐波=212.5×3=637.50（默认 343/0.5→171.50，避开）" },

  { slug: "acoustics/pipe-open",
    inputs: { v: "340", L: "0.4" },
    expect: ["425.00", "850.00"],
    ref: "f₁=340/(2×0.4)=425.00；二次谐波=425×2=850.00（默认 343/0.5→343.00，避开）" },

  { slug: "acoustics/reverberation-time",
    inputs: { V: "200", A: "25" },
    expect: ["1.288", "0.1250"],
    ref: "T₆₀=0.161×200/25=1.288；吸声面密度=A/V=25/200=0.1250（默认 100/10→1.610，避开）" },

  { slug: "acoustics/room-axial-mode",
    inputs: { L: "4", n: "2", c: "340" },
    expect: ["85.00"],
    ref: "f=n·c/(2L)=2×340/(2×4)=85.00（默认 5/1/343→34.30，避开）" },

  { slug: "acoustics/sound-intensity-level",
    inputs: { I: "1e-5" },
    expect: ["70.00"],
    ref: "L=10·log₁₀(1e-5/1e-12)=10·log₁₀(1e7)=70.00（默认 1e-6→60.00，避开）" },

  { slug: "acoustics/sound-intensity-spherical",
    inputs: { P: "2", r: "1" },
    expect: ["1.592e-1", "112.02"],
    ref: "I=2/(4π×1)=1.592e-1；声强级=10·log₁₀(1.59155e11)=112.02（默认 1/2→1.989e-2，避开）" },

  { slug: "acoustics/sound-power-level",
    inputs: { W: "0.1" },
    expect: ["110.00"],
    ref: "L_W=10·log₁₀(0.1/1e-12)=10·log₁₀(1e11)=110.00（默认 0.01→100.00，避开）" },

  { slug: "acoustics/sound-pressure-level",
    inputs: { p: "2" },
    expect: ["100.00"],
    ref: "SPL=20·log₁₀(2/20e-6)=20·log₁₀(1e5)=100.00（默认 0.632→90.00，避开）" },

  { slug: "acoustics/sound-speed-air",
    inputs: { T: "30" },
    expect: ["349.40", "97.06"],
    ref: "v=331.4+0.6×30=349.40；km/h=349.40/3.6=97.06（默认 T=20→343.40，避开）" },

  { slug: "acoustics/spl-add",
    inputs: { L1: "90", L2: "84" },
    expect: ["90.97", "0.97"],
    ref: "L=10·log₁₀(10⁹+10^8.4)=90.97；增量=90.97−90=0.97（默认 80/80→83.01，避开）" },

  { slug: "acoustics/spring-natural-freq",
    inputs: { k: "800", m: "2" },
    expect: ["3.1831", "20.0000"],
    ref: "f=(1/2π)·√(800/2)=20/(2π)=3.1831；ω=2π×3.1831=20.0000（默认 100/1→1.5915，避开）" },

  { slug: "acoustics/string-fundamental",
    inputs: { L: "0.5", T: "200", mu: "0.005" },
    expect: ["200.00", "400.00"],
    ref: "f₁=(1/(2×0.5))·√(200/0.005)=1×200=200.00；二次谐波=400.00（默认 0.65/80/0.01→68.80，避开）" },

  { slug: "acoustics/wavelength-frequency",
    inputs: { v: "340", f: "170" },
    expect: ["2.0000", "200.00"],
    ref: "λ=v/f=340/170=2.0000 m；cm=200.00（默认 343/440→0.7795，避开）" },

  { slug: "acoustics/wavelength-from-freq",
    inputs: { f: "500", c: "340" },
    expect: ["0.6800", "68.00"],
    ref: "λ=c/f=340/500=0.6800 m；cm=68.00（默认 1000/343→0.3430，避开）" },
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
  console.log("==== acoustics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();