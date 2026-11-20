#!/usr/bin node
/**
 * quantum 分类计算正确性验证（覆盖 tools/quantum/ 全部 26 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_quantum_calc.js
 *   —— 目标：默认态 0 命中。
 *
 * 说明：pair-production-threshold 现按轻子种类 + 靶核反冲质量数计算，已纳入 CASES。
 *
 * 跑法:
 *   node scripts/verify_quantum_calc.js                # 全部
 *   node scripts/verify_quantum_calc.js hydrogen-energy-level  # 单页
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");
// harness 的点击代码在 new Function 里执行，模块局部 require 不可见；显式挂到全局供静态源码断言使用。
globalThis.__tbFs = require("fs");

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
    expect: ["0.4763"],
    ref: "r_n=a₀·n²=5.2918e-11×9=4.7626 Å" },

  { slug: "quantum/bohr-orbit-radius",
    inputs: { n: "0" },
    expect: ["请填写不小于 1 的「主量子数 n」"],
    ref: "n=0 无轨道，必须提示补填" },

  { slug: "quantum/bohr-orbit-radius",
    inputs: { n: "2" },
    expect: ["0.2117"],
    ref: "n=2 合法，r=a₀·n²=5.2918e-11×4=2.1167 Å" },
  { slug: "quantum/boltzmann-population",
    inputs: { dE: "0.5", T: "400" },
    expect: ["5.015e-7"],
    ref: "N₂/N₁=exp(−ΔE/kT)=exp(−0.5×1.602e-19/(1.381e-23×400))=5.015e-7" },
  { slug: "quantum/compton-shift",
    inputs: { th: "60" },
    expect: ["0.00121"],
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
    expect: ["-1.5111 能级"],
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
    expect: ["0.000e+0", "0.000", "不能逸出（hf 低于 φ）"],
    ref: "hf=6.626e-34×4e14=2.6504e-19 J < φ=3.0×1.602e-19=4.806e-19 J ⇒ 不能逸出；最大动能按物理定义取 max(0, hf−φ)=0 J=0 eV（原实现输出负动能 −2.156e-19 J/−1.346 eV，非物理）" },
  { slug: "quantum/photoelectric-threshold",
    inputs: { phi: "2.3" },
    expect: ["5.561e+14"],
    ref: "f₀=φ/h=2.3×1.602e-19/6.626e-34=5.561e14 Hz" },
  { slug: "quantum/photon-energy",
    inputs: { lam: "800e-9" },
    expect: ["2.483e-19", "1.550"],
    ref: "E=hc/λ=6.626e-34×2.998e8/800e-9=2.483e-19 J=1.550 eV" },
  {
    "slug": "quantum/photon-energy",
    "inputs": { lam: "500e-9" },
    "clicks": ["var cap=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(sel,keys){cap=keys;}},matrix:{table:function(){}},history:{record:function(){},mount:function(){}}};__photon_energyExtras();document.getElementById('__tbProbe').textContent='DIFF '+(cap?cap.join(','):'NONE');"],
    "expect": ["DIFF lam"],
    "ref": "998 差异对照监视真实输入（PQ-22）：旧版 diffBox 监视常量 H，永远没有差异；修复后监视 λ。默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    "slug": "quantum/photon-energy",
    "inputs": { lam: "-500e-9" },
    "expect": ["波长 λ 必须为正数"],
    "ref": "998 波长正值守卫（PQ-22）：旧版负波长直接算出负能量与负 eV；修复后主区与明细同时拒绝。默认 500e-9 不含该串。"
  },
  { slug: "quantum/photon-flux",
    inputs: { P: "1e-3", lam: "" },
    expect: ["请填写光功率与波长后再计算。"],
    ref: "波长留空：旧代码按 0 输出光子通量 0；新增守卫后须提示。" },

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
    inputs: { ml: "" },
    expect: ["请填写磁量子数 m_l（−10 至 10 之间的整数）后再计算。"],
    ref: "磁量子数留空：旧代码按 0 输出零磁矩；新增守卫后须提示。" },

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
      "0.000e+0 最大动能 K (J) 0.000 K (eV) 不能逸出（hf 低于 φ） 判定"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"phi\":\"42\"}，hf≪φ ⇒ 最大动能取 0 且判定「不能逸出（hf 低于 φ）」；默认态（f=1e15、φ=2）输出为「能逸出」不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "quantum/pair-production-threshold",
    "inputs": {
      "lepton": "mu",
      "targetA": "27"
    },
    "expect": [
      "212.2177"
    ],
    "ref": "注入 μ 子对 + 铝靶 A=27（默认 e/A=0）：E=2·m_μ·c²·(1+m_μ/M)，M=27×1.66053906660e-27=4.48345e-26 kg，m_μ/M=0.004201 ⇒ E=3.400e-11 J=212.2177 MeV；默认态 1.0220 MeV 不命中。"
  },
  {
    "slug": "quantum/pair-production-threshold",
    "inputs": {
      "lepton": "mu",
      "targetA": ""
    },
    "expect": [
      "⚠ 请填写靶核质量数 A（0 表示不计反冲）。"
    ],
    "ref": "999 空靶核质量数守卫（PQ-09）：旧版 parseFloat('') 得 NaN 后静默按 0 计算纯阈值；修复后空值提示补填，显式 0 仍表示不计反冲。默认 targetA=0 不含该串。"
  },
  {
    "slug": "quantum/pair-production-threshold",
    "inputs": {
      "lepton": "mu",
      "targetA": ""
    },
    "clicks": ["var rows=-1,rec=0;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(sel,cfg){rows=cfg&&cfg.rows?cfg.rows.length:-1;}},history:{record:function(){rec++;},mount:function(){}}};__pair_production_thresholdExtras();document.getElementById('__tbProbe').textContent='PPBLANK '+((rows===0&&rec===0)?'OK':'BAD rows='+rows+' rec='+rec);"],
    "expect": [
      "PPBLANK OK"
    ],
    "ref": "999 空靶核质量数不得生成明细或写入历史（PQ-09）：旧版按 A=0 写出 8 行明细并 record；修复后先清表且 record 不被调用。探针只在 clicks 注入后出现，默认态零逃生。"
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
      "42\n42\n⚠ n₁ 与 n₂ 必须不同，否则不存在跃迁（1/λ=0）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\"}，两能级相同 ⇒ 输出区提示「⚠ n₁ 与 n₂ 必须不同，否则不存在跃迁（1/λ=0）」（原实现会得 1/λ=0 并输出 Infinity）；默认态（n₁=2、n₂=3）不含该串 ⇒ 强判别、零逃生。"
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
      "ml": "3"
    },
    "expect": [
      "3 磁矩 μ (μ_B) 2.782e-23"
    ],
    "ref": "m_l=3（非默认 1）：μ=3μ_B=2.782e-23 J/T，页面按 μ_B 口径显示 9.274e-24 每玻尔磁子；原哨兵 42 超出新增 −10 至 10 校验范围。"
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
  },
  {
    "slug": "quantum/compton-shift",
    "inputs": { "th": "270" },
    "clicks": ["var rows=-1,rec=0;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(sel,cfg){rows=cfg&&cfg.rows?cfg.rows.length:-1;}},history:{record:function(){rec++;},mount:function(){}}};__compton_shiftExtras();document.getElementById('__tbProbe').textContent='COM270 '+((rows===0&&rec===0)?'OK':'BAD rows='+rows+' rec='+rec);"],
    "expect": ["COM270 OK"],
    "ref": "1000 康普顿散射明细同步主区角度定义域（PQ-05）：旧版 θ=270° 主区报错但明细仍生成 2 行并写历史；修复后先清表且不记录。探针只在 clicks 注入后出现，默认 90° 不含该串。"
  },
  {
    "slug": "quantum/compton-shift",
    "inputs": { "th": "45" },
    "clicks": ["var cap=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(sel,keys){cap=keys;}},matrix:{table:function(){}},history:{record:function(){},mount:function(){}}};__compton_shiftExtras();document.getElementById('__tbProbe').textContent='CDIFF '+(cap?cap.join(','):'NONE');"],
    "expect": ["CDIFF th"],
    "ref": "1000 康普顿差异对照监视真实散射角而非常量 H：旧版 diffBox 固定监视 H，修复后监视 th；默认态不执行 clicks，零逃生。"
  },
  {
    "slug": "quantum/zeeman-splitting",
    "inputs": { "B": "-1" },
    "clicks": ["var rows=-1,rec=0;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(sel,cfg){rows=cfg&&cfg.rows?cfg.rows.length:-1;}},history:{record:function(){rec++;},mount:function(){}}};__zeeman_splittingExtras();document.getElementById('__tbProbe').textContent='ZEENEG '+((rows===0&&rec===0)?'OK':'BAD rows='+rows+' rec='+rec);"],
    "expect": ["ZEENEG OK"],
    "ref": "1000 塞曼分裂明细同步主区 B≥0 校验（PQ-08）：旧版 B=-1 主区报错但明细仍写 4 行并记历史；修复后清表且不记录。默认 B=1 不含该串。"
  },
  {
    "slug": "quantum/zeeman-splitting",
    "inputs": { "B": "0" },
    "clicks": ["var cap=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(sel,keys){cap=keys;}},matrix:{table:function(){}},history:{record:function(){},mount:function(){}}};__zeeman_splittingExtras();document.getElementById('__tbProbe').textContent='ZDIFF '+(cap?cap.join(','):'NONE');"],
    "expect": ["ZDIFF B"],
    "ref": "1000 塞曼差异对照监视真实磁感应强度而非常量 μ_B；B=0 是合法输入，旧版 diffBox 监视 muB，修复后监视 B。默认态不执行 clicks，零逃生。"
  },
  {
    "slug": "quantum/rydberg-wavelength",
    "inputs": { "n1": "2", "n2": "2" },
    "clicks": ["var rows=-1,rec=0;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(sel,cfg){rows=cfg&&cfg.rows?cfg.rows.length:-1;}},history:{record:function(){rec++;},mount:function(){}}};__rydberg_wavelengthExtras();document.getElementById('__tbProbe').textContent='RYDEQ '+((rows===0&&rec===0)?'OK':'BAD rows='+rows+' rec='+rec);"],
    "expect": ["RYDEQ OK"],
    "ref": "1001 里德伯明细同步主区 n₁≠n₂ 校验：旧版 n₁=n₂=2 仍写波长 Infinity 的 2 行明细并记历史；修复后清表且不记录。默认 2/3 不含该串。"
  },
  {
    "slug": "quantum/rydberg-wavelength",
    "inputs": { "n1": "4", "n2": "6" },
    "clicks": ["var keys=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(sel,k){keys=k;}},matrix:{table:function(){}},history:{record:function(){},mount:function(){}}};__rydberg_wavelengthExtras();document.getElementById('__tbProbe').textContent='RYDIFF '+(keys?keys.join(','):'NONE');"],
    "expect": ["RYDIFF n1,n2"],
    "ref": "1001 里德伯差异框监视真实能级 n1/n2 而非常量 H；默认态不执行 clicks，零逃生。"
  },
  {
    "slug": "quantum/rydberg-wavelength",
    "inputs": { "n1": "3", "n2": "4" },
    "clicks": ["var p=null;globalThis.TBKit={preset:{bar:function(sel,items){p=items;}},util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(){}},history:{record:function(){},mount:function(){}}};__rydberg_wavelengthPresets();var vals=p?p.map(function(x){return x.values.n1+'/'+x.values.n2;}).join('|'):'NONE';document.getElementById('__tbProbe').textContent='RYDPRE '+vals;"],
    "expect": ["RYDPRE 2/3|4/6|3/4"],
    "ref": "1001 里德伯 0.5× 预设由非法 1/1.5 改为 3→4；旧版预设探针为 2/3|4/6|1/1.5，修复后为 2/3|4/6|3/4。默认态不执行 clicks，零逃生。"
  },
  {
    "slug": "quantum/photoelectric-effect",
    "inputs": { "f": "1e14", "phi": "2" },
    "clicks": ["var rows=null,rec=0;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){}},matrix:{table:function(sel,cfg){rows=cfg&&cfg.rows?cfg.rows:null;}},history:{record:function(){rec++;},mount:function(){}}};__photoelectric_effectExtras();var s=rows?JSON.stringify(rows):'NONE';document.getElementById('__tbProbe').textContent='PENOPHOTO '+((s.indexOf('无光电子，最大动能不适用')>=0&&rec===1)?'OK':'BAD '+s);"],
    "expect": ["PENOPHOTO OK"],
    "ref": "1001 光电效应低于阈值时明细不再把钳到 0 的负能量差称作最大动能（旧版写 -1.586e+0 J / -0.991 eV），改为「无光电子，最大动能不适用」；默认 f=1e15 不含该串。"
  },
  {
    "slug": "quantum/photoelectric-effect",
    "inputs": { "f": "3e15", "phi": "1.5" },
    "clicks": ["var cap=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(sel,keys){cap=keys;}},matrix:{table:function(){}},history:{record:function(){},mount:function(){}}};__photoelectric_effectExtras();document.getElementById('__tbProbe').textContent='PED '+(cap?cap.join(','):'NONE');"],
    "expect": ["PED f,phi"],
    "ref": "1001 光电效应差异框监视真实输入 f/phi 而非常量 H；默认态不执行 clicks，零逃生。"
  },
  {
    "slug": "quantum/photoelectric-effect",
    "inputs": { "f": "1e14", "phi": "2" },
    "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/quantum/photoelectric-effect.html','utf8');document.getElementById('__tbProbe').textContent='PEDEEP '+(h.indexOf('hf&lt;Φ 时 hf−Φ 为负值，仅表示能量不足')>=0&&h.indexOf('没有逸出电子，因此 K_max 不适用')>=0&&h.indexOf('K_max&lt;0')<0&&h.indexOf('无光电子 emission')<0?'OK':'BAD');"],
    "expect": ["PEDEEP OK"],
    "ref": "1001 复核重做：深度解析权威源须与低于阈值时的主结果一致——负值是 hf−Φ 能量差，没有逸出电子故 K_max 不适用；旧版正文写「K_max<0，无光电子 emission」，旧句不命中。harness 的 body 桩不含静态正文，故直接读构建后页面源码；探针仅在 clicks 注入后出现，且同时要求新句命中、旧句与混英文词消失。"
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

  console.log("==== quantum calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();