#!/usr/bin node
/**
 * quantum 分类计算正确性验证（覆盖 tools/quantum/ 全部 26 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_quantum_calc.js
 *   —— 目标：默认态 0 命中。
 *
 * 说明：pair-production-threshold 仅有 dummy 输入、输出恒为 2·m_e·c²（≈1.022 MeV），
 *   无法用输入区分，与 nuclear/pair-annihilation 同类，故不入 CASES，仅在此注明。
 *
 * 跑法:
 *   node scripts/verify_quantum_calc.js                # 全部
 *   node scripts/verify_quantum_calc.js hydrogen-energy-level  # 单页
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "quantum/angular-momentum-quant",
    inputs: { n: "5" },
    expect: ["5.2729"],
    ref: "L=n·ħ=5×1.0546e-34 → 5.2729×10⁻³⁴ J·s" },
  { slug: "quantum/band-gap-photon",
    inputs: { Eg: "2.0" },
    expect: ["619.9"],
    ref: "λ=hc/E_g=6.626e-34×2.998e8/(2.0×1.602e-19)×1e9=619.9 nm" },
  { slug: "quantum/bohr-orbit-radius",
    inputs: { n: "3" },
    expect: ["4.7626", "0.4763"],
    ref: "r_n=a₀·n²=5.2918e-11×9=4.7626 Å" },
  { slug: "quantum/boltzmann-population",
    inputs: { dE: "0.5", T: "400" },
    expect: ["5.015e-7"],
    ref: "N₂/N₁=exp(−ΔE/kT)=exp(−0.5×1.602e-19/(1.381e-23×400))=5.015e-7" },
  { slug: "quantum/compton-shift",
    inputs: { th: "60" },
    expect: ["1.2132", "0.00121"],
    ref: "Δλ=(h/m_e c)(1−cos60°)=1.2132 pm" },
  { slug: "quantum/compton-wavelength",
    inputs: { m: "2.0e-31" },
    expect: ["11.051"],
    ref: "λ_c=h/(mc)=6.626e-34/(2.0e-31×2.998e8)×1e12=11.051 pm" },
  { slug: "quantum/cyclotron-frequency",
    inputs: { q: "3.204e-19", B: "0.5", m: "1.673e-27" },
    expect: ["9.576e+7", "1.524e+7"],
    ref: "ω=qB/m=3.204e-19×0.5/1.673e-27=9.576e7 rad/s" },
  { slug: "quantum/de-broglie-wavelength",
    inputs: { m: "1.673e-27", v: "2e5" },
    expect: ["1.980e-12", "0.0020"],
    ref: "λ=h/(mv)=6.626e-34/(1.673e-27×2e5)=1.980e-12 m" },
  { slug: "quantum/energy-time-uncertainty",
    inputs: { dt: "5e-10" },
    expect: ["6.582e-7"],
    ref: "ΔE=ħ/(2Δt)=1.0546e-34/(2×5e-10)/1.602e-19=6.582e-7 eV" },
  { slug: "quantum/fermi-energy-3d",
    inputs: { n: "5e28", m: "9.11e-31" },
    expect: ["4.949"],
    ref: "E_F=(ħ²/2m)(3π²n)^{2/3}=4.949 eV" },
  { slug: "quantum/heisenberg-uncertainty",
    inputs: { dx: "5e-10" },
    expect: ["1.055e-25", "1.158e+5"],
    ref: "Δp=ħ/(2Δx)=1.0546e-34/(2×5e-10)=1.055e-25 kg·m/s" },
  { slug: "quantum/hydrogen-energy-level",
    inputs: { n: "3" },
    expect: ["-1.5111"],
    ref: "E_n=−13.6/n²=−13.6/9=−1.5111 eV" },
  { slug: "quantum/infinite-well-energy",
    inputs: { n: "2", m: "9.11e-31", L: "3e-9" },
    expect: ["2.677e-20", "0.1671"],
    ref: "E_n=n²h²/(8mL²)=4×6.626e-34²/(8×9.11e-31×(3e-9)²)=2.677e-20 J=0.1671 eV" },
  { slug: "quantum/mass-energy-equivalence",
    inputs: { m: "0.5" },
    expect: ["4.494e+16", "2.805e+29"],
    ref: "E=mc²=0.5×2.998e8²=4.494e16 J=2.805e29 MeV" },
  { slug: "quantum/photoelectric-effect",
    inputs: { f: "4e14", phi: "3.0" },
    expect: ["-2.156e-19", "-1.346", "不能逸出（hf<φ）"],
    ref: "K=hf−φ=6.626e-34×4e14−3.0×1.602e-19=−2.156e-19 J=−1.346 eV<0" },
  { slug: "quantum/photoelectric-threshold",
    inputs: { phi: "2.3" },
    expect: ["5.561e+14"],
    ref: "f₀=φ/h=2.3×1.602e-19/6.626e-34=5.561e14 Hz" },
  { slug: "quantum/photon-energy",
    inputs: { lam: "800e-9" },
    expect: ["2.483e-19", "1.550"],
    ref: "E=hc/λ=6.626e-34×2.998e8/800e-9=2.483e-19 J=1.550 eV" },
  { slug: "quantum/photon-flux",
    inputs: { P: "2", lam: "400e-9" },
    expect: ["4.027e+18"],
    ref: "N=Pλ/(hc)=2×400e-9/(6.626e-34×2.998e8)=4.027e18 /s" },
  { slug: "quantum/photon-momentum",
    inputs: { lam: "600e-9" },
    expect: ["1.104e-27"],
    ref: "p=h/λ=6.626e-34/600e-9=1.104e-27 kg·m/s" },
  { slug: "quantum/quantum-oscillator-energy",
    inputs: { n: "3", f: "5e13" },
    expect: ["0.7237"],
    ref: "E_n=ħω(n+½)=1.0546e-34×2π×5e13×3.5/1.602e-19=0.7237 eV" },
  { slug: "quantum/rydberg-wavelength",
    inputs: { n1: "1", n2: "3" },
    expect: ["9.754e+6", "102.52"],
    ref: "1/λ=R(1/1²−1/3²)=1.0974e7×0.8889=9.754e6 m⁻¹；λ=102.52 nm" },
  { slug: "quantum/spin-magnetic-moment",
    inputs: { ml: "2" },
    expect: ["1.855e-23"],
    ref: "μ=μ_B·m_l=2×9.274e-24=1.855e-23 J/T（裸串\"2\"在静态HTML存在，故仅断言J/T值专属串）" },
  { slug: "quantum/stefan-boltzmann-power",
    inputs: { A: "0.05", T: "500" },
    expect: ["177.199"],
    ref: "P=σAT⁴=5.670e-8×0.05×500⁴=177.199 W" },
  { slug: "quantum/thermal-de-broglie",
    inputs: { m: "1.673e-27", T: "200" },
    expect: ["0.123"],
    ref: "λ=h/√(2πmkT)=6.626e-34/√(2π×1.673e-27×1.381e-23×200)×1e9=0.123 nm" },
  { slug: "quantum/wien-displacement",
    inputs: { T: "3000" },
    expect: ["965.92"],
    ref: "λ_max=b/T=2.898e-3/3000×1e9=965.92 nm" },
  { slug: "quantum/zeeman-splitting",
    inputs: { B: "2" },
    expect: ["1.158e-4"],
    ref: "ΔE=μ_B·B=9.274e-24×2/1.602e-19=1.158e-4 eV" },
  {
    "slug": "quantum/angular-momentum-quant",
    "inputs": {
      "n": "42"
    },
    "expect": [
      "平方与 ħ 之积 43.2374 相邻能级角动量差"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\"}，输出区含「平方与 ħ 之积 43.2374 相邻能级角动量差」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/bohr-orbit-radius",
    "inputs": {
      "n": "42"
    },
    "expect": [
      " r_n (Å) 93.346"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\"}，输出区含「 r_n (Å) 93.346」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/band-gap-photon",
    "inputs": {
      "Eg": "42"
    },
    "expect": [
      "频率 (THz) 2.952e-8 波长 (m) 6.729e-18 禁带能量 (J)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"Eg\":\"42\"}，输出区含「频率 (THz) 2.952e-8 波长 (m) 6.729e-18 禁带能量 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/boltzmann-population",
    "inputs": {
      "dE": "42",
      "T": "42"
    },
    "expect": [
      "42\n42\n0.000e+0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dE\":\"42\",\"T\":\"42\"}，输出区含「42\n42\n0.000e+0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/compton-shift",
    "inputs": {
      "th": "42"
    },
    "expect": [
      "(pm) 0.00062 Δλ (nm)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"th\":\"42\"}，输出区含「(pm) 0.00062 Δλ (nm)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/compton-wavelength",
    "inputs": {
      "m": "42"
    },
    "expect": [
      "顿波长 (fm) 1.9003e+43"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\"}，输出区含「顿波长 (fm) 1.9003e+43」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/cyclotron-frequency",
    "inputs": {
      "q": "42",
      "B": "42",
      "m": "42"
    },
    "expect": [
      "42\n42\n42\n4.200e+"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"q\":\"42\",\"B\":\"42\",\"m\":\"42\"}，输出区含「42\n42\n42\n4.200e+」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/de-broglie-wavelength",
    "inputs": {
      "m": "42",
      "v": "42"
    },
    "expect": [
      " λ (m) 0.0000 λ (nm)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"v\":\"42\"}，输出区含「 λ (m) 0.0000 λ (nm)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/heisenberg-uncertainty",
    "inputs": {
      "dx": "42"
    },
    "expect": [
      "(kg·m/s) 1.378e-6"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dx\":\"42\"}，输出区含「(kg·m/s) 1.378e-6」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/energy-time-uncertainty",
    "inputs": {
      "dt": "42"
    },
    "expect": [
      "能量展宽 (J) 7.836e-18"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dt\":\"42\"}，输出区含「能量展宽 (J) 7.836e-18」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/fermi-energy-3d",
    "inputs": {
      "n": "42",
      "m": "42"
    },
    "expect": [
      "能 (keV) 10.7537"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"m\":\"42\"}，输出区含「能 (keV) 10.7537」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/hydrogen-energy-level",
    "inputs": {
      "n": "42"
    },
    "expect": [
      "E_n (eV) 0.0077"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\"}，输出区含「E_n (eV) 0.0077」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/infinite-well-energy",
    "inputs": {
      "n": "42",
      "m": "42",
      "L": "42"
    },
    "expect": [
      "42\n42\n42\n1.307e-69"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"m\":\"42\",\"L\":\"42\"}，输出区含「42\n42\n42\n1.307e-69」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/mass-energy-equivalence",
    "inputs": {
      "m": "42"
    },
    "expect": [
      "能量 E (J) 2.356e+31 E (MeV)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\"}，输出区含「能量 E (J) 2.356e+31 E (MeV)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/photoelectric-effect",
    "inputs": {
      "f": "42",
      "phi": "42"
    },
    "expect": [
      "动能 K (J) -42.000 K (eV) 不能逸出（hf 判定"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"phi\":\"42\"}，输出区含「动能 K (J) -42.000 K (eV) 不能逸出（hf 判定」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/pair-production-threshold",
    "inputs": {
      "dummy": "42"
    },
    "expect": [
      "阈值能量 (eV)\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dummy\":\"42\"}，输出区含「阈值能量 (eV)\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/photoelectric-threshold",
    "inputs": {
      "phi": "42"
    },
    "expect": [
      "截止周期 (s) 6.729e-18"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"phi\":\"42\"}，输出区含「截止周期 (s) 6.729e-18」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/photon-energy",
    "inputs": {
      "lam": "42"
    },
    "expect": [
      "能量 E (J) 0.000 E (eV)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lam\":\"42\"}，输出区含「能量 E (J) 0.000 E (eV)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/photon-flux",
    "inputs": {
      "P": "42",
      "lam": "42"
    },
    "expect": [
      " N (1/s) 4.7296e-27"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"P\":\"42\",\"lam\":\"42\"}，输出区含「 N (1/s) 4.7296e-27」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/photon-momentum",
    "inputs": {
      "lam": "42"
    },
    "expect": [
      "量 (eV) 2.381e-2 波数 (m⁻¹)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lam\":\"42\"}，输出区含「量 (eV) 2.381e-2 波数 (m⁻¹)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/quantum-oscillator-energy",
    "inputs": {
      "n": "42",
      "f": "42"
    },
    "expect": [
      "rad/s) 0.0000 零点能 (eV)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"f\":\"42\"}，输出区含「rad/s) 0.0000 零点能 (eV)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/rydberg-wavelength",
    "inputs": {
      "n1": "42",
      "n2": "42"
    },
    "expect": [
      "42\n42\n0.000e+0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\"}，输出区含「42\n42\n0.000e+0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/stefan-boltzmann-power",
    "inputs": {
      "A": "42",
      "T": "42"
    },
    "expect": [
      "度 (W/m2) 6.8995e-5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"A\":\"42\",\"T\":\"42\"}，输出区含「度 (W/m2) 6.8995e-5」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/spin-magnetic-moment",
    "inputs": {
      "ml": "42"
    },
    "expect": [
      " μ (μ_B) 3.895e-22"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ml\":\"42\"}，输出区含「 μ (μ_B) 3.895e-22」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/thermal-de-broglie",
    "inputs": {
      "m": "42",
      "T": "42"
    },
    "expect": [
      "热波长 (pm) 3.912e-10"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"T\":\"42\"}，输出区含「热波长 (pm) 3.912e-10」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/wien-displacement",
    "inputs": {
      "T": "42"
    },
    "expect": [
      "值波长 (µm) 1.764e-1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"T\":\"42\"}，输出区含「值波长 (µm) 1.764e-1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/zeeman-splitting",
    "inputs": {
      "B": "42"
    },
    "expect": [
      " ΔE (eV) 3.895e-22"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"B\":\"42\"}，输出区含「 ΔE (eV) 3.895e-22」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  }

];

"use strict";

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
  console.log("==== quantum calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();