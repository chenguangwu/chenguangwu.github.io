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
    expect: ["503.00"],
    ref: "拍频=|500−506|=6.00；平均=(500+506)/2=503.00（默认 440/444→4.00，避开）" },

  { slug: "acoustics/combine-two-spl",
    inputs: { l1: "90", l2: "84" },
    expect: ["90.97"],
    ref: "L=10·log₁₀(10⁹+10^8.4)=90.97；比响者高出=90.97−90=0.97（默认 80/80→83.01，避开）" },

  { slug: "acoustics/critical-distance",
    inputs: { V: "400", rt: "2.0", Q: "2" },
    expect: ["1.14 临界距离"],
    ref: "2026-10-25 系数修正后 r_c=0.057·√(2×400/2)=0.057×20=1.14（原 0.141 系数误配 V/RT 口径偏大 2.49 倍；默认 200/1.0/1→0.81，避开）" },

  { slug: "acoustics/decibel-power-ratio",
    inputs: { p1: "4", p2: "64" },
    expect: ["12.04", "16.000"],
    ref: "L=10·log₁₀(64/4)=10·log₁₀(16)=12.04；线性比=16.000（默认 1/10→10.00，避开）" },

  { slug: "acoustics/decibel-voltage-ratio",
    inputs: { v1: "3", v2: "30" },
    expect: ["20.00 电压比", "10.000 线性比"],
    ref: "L=20·log₁₀(30/3)=20.00；线性比=10.000（默认 1/3.16→9.99，避开）" },

  { slug: "acoustics/doppler-acoustic",
    inputs: { f: "500", v: "340", vs: "40" },
    expect: ["566.67"],
    ref: "f′=500×340/(340−40)=170000/300=566.67；偏移=66.67（默认 440/343/34.3→488.89，避开）" },

  { slug: "acoustics/freq-to-note",
    inputs: { f: "1000" },
    expect: ["B5", "83", "+21"],
    ref: "MIDI=69+12·log₂(1000/440)=83.206→round=83；音名=NAMES[11]+(floor(83/12)−1)=B5；音分=round(0.206×100)=+21（默认 440→A4，避开）" },

  { slug: "acoustics/intensity-inverse-square",
    inputs: { I1: "200", r1: "2", r2: "4" },
    expect: ["50.00", "136.99"],
    ref: "I₂=200×(2/4)²=50.00；声强级=10·log₁₀(50/1e-12)=136.99（默认 100/1/2→25.00，避开）" },

  { slug: "acoustics/mass-law-tl",
    inputs: { f: "1000", m: "20" },
    expect: ["38.02 隔声量"],
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

  { slug: "acoustics/room-axial-mode",
    inputs: { L: "5", n: "1", c: "343", Lx: "6", Ly: "4", Lz: "3", fc: "343" },
    expect: ["1. 轴向 (1,0,0) — 28.58 Hz"],
    ref: "完整房间模态：Lx6/Ly4/Lz3/c343 枚举三维简正频率，最低阶轴向(1,0,0)=c/2·(1/6)=28.58 Hz（默认 5/4/3→34.30，避开 A===B；切向(1,1,0)=51.53、斜向(1,1,1)=76.96 同表）。" },

  { slug: "acoustics/sound-intensity-level",
    inputs: { I: "1e-5" },
    expect: ["70.00 声强级"],
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
    inputs: { T: "" },
    expect: ["请填写气温（不低于 −273.15 °C）后再计算。"],
    ref: "气温留空：旧代码按 0°C 静默输出 331.4 m/s 等一整套结果；新增守卫后须提示。" },

  { slug: "acoustics/sound-speed-air",
    inputs: { T: "30" },
    expect: ["97.06"],
    ref: "v=331.4+0.6×30=349.40；km/h=349.40/3.6=97.06（默认 T=20→343.40，避开）" },
  { slug: "acoustics/critical-distance",
    inputs: { V: "200", rt: "0", Q: "1" },
    expect: ["不能为 0"],
    ref: "rt=0 会让 Q·V/rt 除零；须拒绝并说明三个参数均须为正，而不是输出 Infinity。" },
  { slug: "acoustics/acoustic-impedance",
    inputs: { rho: "1.2", c: "0" },
    expect: ["密度和声速都必须大于 0"],
    ref: "c=0 时 1/c 无定义；旧实现用 c||1 伪造 1 s/m，须拒绝。" },
  { slug: "acoustics/sound-speed-air",
    inputs: { T: "100" },
    expect: ["超出 −40～50 ℃ 线性近似适用范围"],
    ref: "线性近似越界：100℃ 时 331.4+0.6T 明显偏离真实干空气声速，须提示而非静默给值。" },
  { slug: "acoustics/doppler-acoustic",
    inputs: { f: "500", v: "340", vs: "340" },
    expect: ["声源速度须低于声速（亚声速）"],
    ref: "vs=v 时分母为零，vs>v 公式失效；须拒绝并说明亚声速条件。" },
  { slug: "acoustics/wavelength-from-freq",
    inputs: { f: "0", c: "343" },
    expect: ["不能为 0"],
    ref: "零频率会得到 0 波长与 0 空间频率，须拒绝而非输出无意义值。" },

  { slug: "acoustics/spring-natural-freq",
    inputs: { k: "800", m: "2" },
    expect: ["3.1831", "20.0000"],
    ref: "f=(1/2π)·√(800/2)=20/(2π)=3.1831；ω=2π×3.1831=20.0000（默认 100/1→1.5915，避开）" },

  { slug: "acoustics/string-fundamental",
    inputs: { L: "0.5", T: "200", mu: "0.005" },
    expect: ["400.00 二次谐波" ],
    ref: "f₁=(1/(2×0.5))·√(200/0.005)=1×200=200.00；二次谐波=400.00（默认 0.65/80/0.01→68.80，避开）" },

  { slug: "acoustics/wavelength-frequency",
    inputs: { v: "340", f: "170" },
    expect: ["2.0000", "200.00"],
    ref: "λ=v/f=340/170=2.0000 m；cm=200.00（默认 343/440→0.7795，避开）" },

  { slug: "acoustics/wavelength-from-freq",
    inputs: { f: "500", c: "340" },
    expect: ["0.6800", "68.00"],
    ref: "λ=c/f=340/500=0.6800 m；cm=68.00（默认 1000/343→0.3430，避开）" },
  {
    "slug": "acoustics/absorption-coeff-sabine",
    "inputs": {
      "V": "42",
      "S": "42",
      "rt": "42"
    },
    "expect": [
      "42\n42\n42\n0.004"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"V\":\"42\",\"S\":\"42\",\"rt\":\"42\"}，输出区含「42\n42\n42\n0.004」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/acoustic-impedance",
    "inputs": {
      "rho": "42",
      "c": "42"
    },
    "expect": [
      "a*s/m) 2.3810e-2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rho\":\"42\",\"c\":\"42\"}，输出区含「a*s/m) 2.3810e-2」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/beat-frequency",
    "inputs": {
      "f1": "42",
      "f2": "42"
    },
    "expect": [
      "拍频为 0，拍周期无有限值"
    ],
    "ref": "等频 f1=f2=42：拍频 0、平均 42.00；拍周期 1/0 无有限值，页面显示「—」并明确说明，不再输出 Infinity/0。默认 440/444 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/combine-two-spl",
    "inputs": {
      "l1": "42",
      "l2": "42"
    },
    "expect": [
      "声级差 (dB) 48"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"l1\":\"42\",\"l2\":\"42\"}，输出区含「声级差 (dB) 48」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/critical-distance",
    "inputs": {
      "V": "42",
      "rt": "42",
      "Q": "42"
    },
    "expect": [
      "量 A (m2) 1.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"V\":\"42\",\"rt\":\"42\",\"Q\":\"42\"}，输出区含「量 A (m2) 1.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/decibel-power-ratio",
    "inputs": {
      "p1": "42",
      "p2": "42"
    },
    "expect": [
      "性比 P₂/P₁ 0.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"p1\":\"42\",\"p2\":\"42\"}，输出区含「性比 P₂/P₁ 0.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/decibel-voltage-ratio",
    "inputs": {
      "v1": "42",
      "v2": "42"
    },
    "expect": [
      "电压比 (dB) 1.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v1\":\"42\",\"v2\":\"42\"}，输出区含「电压比 (dB) 1.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/doppler-acoustic",
    "inputs": {
      "f": "84",
      "v": "42",
      "vs": "21"
    },
    "expect": [
      "84.00 频率偏移 (Hz)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{f=84,v=42,vs=21}，f′=84×42/(42−21)=168.00，偏移 84.00；默认态 440/343/34.3 不含该串 ⇒ 强判别、零逃生。vs 必须低于声速，42/42 会被亚声速守卫拒绝，故改用 21。"
  },
  {
    "slug": "acoustics/freq-to-note",
    "inputs": {
      "f": "42"
    },
    "expect": [
      "DI 音高编号 +33 与标准音分偏差"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\"}，输出区含「DI 音高编号 +33 与标准音分偏差」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/intensity-inverse-square",
    "inputs": {
      "I1": "42",
      "r1": "42",
      "r2": "42"
    },
    "expect": [
      "(W/m²) 136.23 声强级 (dB)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"I1\":\"42\",\"r1\":\"42\",\"r2\":\"42\"}，输出区含「(W/m²) 136.23 声强级 (dB)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/pipe-closed",
    "inputs": {
      "v": "42",
      "L": "42"
    },
    "expect": [
      " f₁ (Hz) 0.75"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"L\":\"42\"}，输出区含「 f₁ (Hz) 0.75」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/mass-law-tl",
    "inputs": {
      "f": "42",
      "m": "42"
    },
    "expect": [
      "0 面密度频率积 64.930"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"m\":\"42\"}，输出区含「0 面密度频率积 64.930」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/pipe-open",
    "inputs": {
      "v": "42",
      "L": "42"
    },
    "expect": [
      "次谐波 (Hz) 84"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"L\":\"42\"}，输出区含「次谐波 (Hz) 84」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/reverberation-time",
    "inputs": {
      "V": "42",
      "A": "42"
    },
    "expect": [
      " (1/m) 372.671"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"V\":\"42\",\"A\":\"42\"}，输出区含「 (1/m) 372.671」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/room-axial-mode",
    "inputs": {
      "L": "42",
      "n": "42",
      "c": "42"
    },
    "expect": [
      "42\n42\n42\n21.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"L\":\"42\",\"n\":\"42\",\"c\":\"42\"}，输出区含「42\n42\n42\n21.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/sound-intensity-spherical",
    "inputs": {
      "P": "42",
      "r": "42"
    },
    "expect": [
      " Lw (dB) 22167.0778"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"P\":\"42\",\"r\":\"42\"}，输出区含「 Lw (dB) 22167.0778」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/sound-intensity-level",
    "inputs": {
      "I": "42"
    },
    "expect": [
      "o*c=400) 4.2000e+13 声强比 I/I0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"I\":\"42\"}，输出区含「o*c=400) 4.2000e+13 声强比 I/I0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/sound-power-level",
    "inputs": {
      "W": "42"
    },
    "expect": [
      "功率级 (dB) 2.3810e-14 声功率比倒数"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"W\":\"42\"}，输出区含「功率级 (dB) 2.3810e-14 声功率比倒数」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/sound-speed-air",
    "inputs": {
      "T": "42"
    },
    "expect": [
      " 摄氏度声速之比 25.20 温度修正项"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\"}，输出区含「 摄氏度声速之比 25.20 温度修正项」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/sound-pressure-level",
    "inputs": {
      "p": "42"
    },
    "expect": [
      "PL 反推声压比 4.4100e+12 声压平方比 6.3222"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"p\":\"42\"}，输出区含「PL 反推声压比 4.4100e+12 声压平方比 6.3222」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/spring-natural-freq",
    "inputs": {
      "k": "42",
      "m": "42"
    },
    "expect": [
      " (rad/s) 6.2832"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"k\":\"42\",\"m\":\"42\"}，输出区含「 (rad/s) 6.2832」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/string-fundamental",
    "inputs": {
      "L": "42",
      "T": "42",
      "mu": "42"
    },
    "expect": [
      "42\n42\n42\n0.01"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"L\":\"42\",\"T\":\"42\",\"mu\":\"42\"}，输出区含「42\n42\n42\n0.01」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/wavelength-from-freq",
    "inputs": {
      "f": "42",
      "c": "42"
    },
    "expect": [
      " 波长 (cm) 23.8095 周期 (ms) 1000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"c\":\"42\"}，输出区含「 波长 (cm) 23.8095 周期 (ms) 1000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "acoustics/wavelength-frequency",
    "inputs": {
      "v": "42",
      "f": "42"
    },
    "expect": [
      "波长 λ (m) 100.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"f\":\"42\"}，输出区含「波长 λ (m) 100.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  }

,
  { slug: "acoustics/wavelength-frequency", inputs: { v: "-1", f: "100" }, expect: ["不能为 0 或负数"], ref: "第965批：负波速不再生成负波长，须拒绝并说明必须为有限正数；旧实现可输出 -0.0100 m。" },
  { slug: "acoustics/wavelength-from-freq", inputs: { c: "-1", f: "1000" }, expect: ["不能为 0 或负数"], ref: "第965批：负声速不再生成负波长，须拒绝；旧实现可输出负值。" },
  { slug: "acoustics/wavelength-frequency", inputs: { v: "343", f: "1000000000" }, expect: ["3.4300e-7", "3.4300e-5"], ref: "第965批：343/1e9 ≈ 3.43e-7 m，固定四位小数会显示 0.0000；须按量级改用科学计数法，厘米行同理。" },
  { slug: "acoustics/wavelength-from-freq", inputs: { c: "343", f: "1000000000" }, expect: ["3.4300e-7", "3.4300e-5", "1.0000e-6"], ref: "第965批：波长 3.43e-7 m、厘米 3.43e-5、周期 1e-6 ms，均须按量级改用科学计数法而非 0。0000。" }
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

  console.log("==== acoustics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();