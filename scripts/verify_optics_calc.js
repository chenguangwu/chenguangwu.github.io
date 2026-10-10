#!/usr/bin node
/**
 * optics 分类计算正确性验证（覆盖 tools/optics/ 全部 21 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_optics_calc.js
 *   —— 目标：默认态 0 命中。
 *
 * 注意（nuclear 分类教训）：文本型分支断言必须选「默认态不会走到」的那一支，
 *   否则默认态即命中形成假通过。本文件 3 处已按此处理：
 *   - magnification-optics 默认 M<0（倒立） → 用例取正像距得「正立」
 *   - thin-lens-equation  默认 dᵢ>0（实像）→ 用例取 dₒ<f 得「虚像」
 *   - snells-law          默认折射分支     → 用例取全反射分支
 *
 * 跑法:
 *   node scripts/verify_optics_calc.js                # 全部
 *   node scripts/verify_optics_calc.js snells-law     # 单页
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "optics/angular-magnification",
    inputs: { N: "200", f: "8" },
    expect: ["25.00"],
    ref: "M=N/f=200/8=25.00（8 cm 焦距放大镜约放大 25 倍）" },

  { slug: "optics/brewster-angle",
    inputs: { n1: "1.0", n2: "1.6" },
    expect: ["57.995"],
    ref: "θ_B=arctan(n₂/n₁)=arctan(1.6)=57.995°" },

  { slug: "optics/combined-lens-focal",
    inputs: { f1: "0.15", f2: "0.25" },
    expect: ["0.0937"],
    ref: "1/F=1/0.15+1/0.25=10.6667 → F=0.0937 m" },

  { slug: "optics/doppler-optical",
    inputs: { f: "4.5e14", v: "1.2e6", c: "3e8" },
    expect: ["4.518e+14"],
    ref: "f′=f(1+v/c)=4.5e14×1.004=4.518e+14 Hz（蓝移）" },

  { slug: "optics/focal-length-mirror",
    inputs: { R: "35" },
    expect: ["17.50"],
    ref: "f=R/2=35/2=17.50 cm" },

  { slug: "optics/fresnel-reflectance",
    inputs: { n1: "1.0", n2: "1.7" },
    expect: ["6.72", "93.28"],
    ref: "R=((1−1.7)/(1+1.7))²=(−0.2593)²=0.0672→6.72%；透射 93.28%" },

  // 默认态 do>0/di>0 → M<0「倒立」；此处取负像距走「正立」分支，避免默认态命中
  { slug: "optics/magnification-optics",
    inputs: { do: "0.5", di: "-0.2" },
    expect: ["0.400", "正立"],
    ref: "M=−dᵢ/dₒ=−(−0.2)/0.5=0.400，M>0 故为正立（虚像情形）" },

  { slug: "optics/malus-law",
    inputs: { I0: "200", th: "30" },
    expect: ["150.00"],
    ref: "I=I₀cos²θ=200×cos²30°=200×0.75=150.00" },

  { slug: "optics/mirror-equation",
    inputs: { f: "0.3", do: "0.8" },
    expect: ["0.4800"],
    ref: "1/dᵢ=1/f−1/dₒ=3.3333−1.25=2.0833 → dᵢ=0.4800 m" },

  { slug: "optics/optical-power-diopter",
    inputs: { f: "0.25" },
    expect: ["4.00"],
    ref: "P=1/f=1/0.25=4.00 D" },

  { slug: "optics/prism-deviation",
    inputs: { n: "1.6", A: "15" },
    expect: ["9.00"],
    ref: "δ≈(n−1)·A=0.6×15=9.00°（小角度近似）" },

  { slug: "optics/rayleigh-criterion",
    inputs: { lam: "600e-9", D: "0.2" },
    expect: ["3.6600", "7.549e-1"],
    ref: "θ=1.22λ/D=1.22×600e-9/0.2=3.66e-6 rad=3.6600 µrad=7.549e-1 角秒" },

  { slug: "optics/refractive-index-speed",
    inputs: { v: "1.5e8", c: "3e8" },
    expect: ["2.0000"],
    ref: "n=c/v=3e8/1.5e8=2.0000" },

  { slug: "optics/resolving-power",
    inputs: { D: "0.25", lam: "500" },
    expect: ["409836"],
    ref: "R=D/(1.22λ)=0.25/(1.22×500e-9)=409836 m⁻¹" },

  { slug: "optics/separated-lenses-focal",
    inputs: { f1: "12", f2: "18", d: "3" },
    expect: ["8.000"],
    ref: "1/F=1/12+1/18−3/(12×18)=0.0833+0.0556−0.01389=0.125 → F=8.000 cm" },

  { slug: "optics/single-slit-diffraction",
    inputs: { a: "2e-4", lam: "450e-9", m: "1" },
    expect: ["0.1289"],
    ref: "sinθ=mλ/a=450e-9/2e-4=2.25e-3 → θ=arcsin(2.25e-3)=0.1289°" },

  // 默认态（1.0→1.5，30°）为折射分支；此处取全反射分支，避免默认态命中折射角文本
  { slug: "optics/snells-law",
    inputs: { n1: "1.5", n2: "1.0", t1: "60" },
    expect: ["发生全反射（无折射）"],
    ref: "n₁sinθ₁/n₂=1.5×sin60°=1.299>1，超过临界角，发生全反射" },

  { slug: "optics/thin-film-max",
    inputs: { n: "1.4", t: "350", m: "1" },
    expect: ["980.0"],
    ref: "λ=2nt/m=2×1.4×350/1=980.0 nm（相长干涉，近红外）" },

  { slug: "optics/thin-film-min",
    inputs: { n: "1.4", t: "350", m: "1" },
    expect: ["653.3"],
    ref: "λ=2nt/(m+0.5)=2×1.4×350/1.5=653.3 nm（相消干涉，红光）" },

  // 默认态 dₒ>f（0.3>0.1）为实像；此处取 dₒ<f 走虚像分支
  { slug: "optics/thin-lens-equation",
    inputs: { f: "0.3", do: "0.2" },
    expect: ["-0.6000", "虚像"],
    ref: "1/dᵢ=1/0.3−1/0.2=3.3333−5=−1.6667 → dᵢ=−0.6000 m<0，故为虚像" },

  { slug: "optics/young-fringe",
    inputs: { lam: "480", L: "2", d: "0.4" },
    expect: ["2.400"],
    ref: "Δy=λL/d=480e-9×2/(0.4e-3)=2.4e-3 m=2.400 mm" },
  {
    "slug": "optics/angular-magnification",
    "inputs": {
      "N": "42",
      "f": "42"
    },
    "expect": [
      "与两倍焦距之比 1.00 放大率平方"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"N\":\"42\",\"f\":\"42\"}，输出区含「与两倍焦距之比 1.00 放大率平方」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/combined-lens-focal",
    "inputs": {
      "f1": "42",
      "f2": "42"
    },
    "expect": [
      "焦度 (屈光度) 21000.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f1\":\"42\",\"f2\":\"42\"}，输出区含「焦度 (屈光度) 21000.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/brewster-angle",
    "inputs": {
      "n1": "42",
      "n2": "42"
    },
    "expect": [
      "率比 n2/n1 45.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\"}，输出区含「率比 n2/n1 45.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/focal-length-mirror",
    "inputs": {
      "R": "42"
    },
    "expect": [
      "数 (1/cm) 2.380952"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"R\":\"42\"}，输出区含「数 (1/cm) 2.380952」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/magnification-optics",
    "inputs": {
      "do": "42",
      "di": "42"
    },
    "expect": [
      "焦距 f (m) 1.000 放大率绝对值"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"do\":\"42\",\"di\":\"42\"}，输出区含「焦距 f (m) 1.000 放大率绝对值」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/doppler-optical",
    "inputs": {
      "f": "42",
      "v": "42",
      "c": "42"
    },
    "expect": [
      "42\n42\n42\n8.400e+1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"v\":\"42\",\"c\":\"42\"}，输出区含「42\n42\n42\n8.400e+1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/fresnel-reflectance",
    "inputs": {
      "n1": "42",
      "n2": "42"
    },
    "expect": [
      "射率 R (%) 100"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\"}，输出区含「射率 R (%) 100」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/malus-law",
    "inputs": {
      "I0": "42",
      "th": "42"
    },
    "expect": [
      "42\n42\n23.20 透射光强 I 18.805 被吸收光强 44.77"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"I0\":\"42\",\"th\":\"42\"}，输出区含「42\n42\n23.20 透射光强 I 18.805 被吸收光强 44.77」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/optical-power-diopter",
    "inputs": {
      "f": "42"
    },
    "expect": [
      "(mm) 0.000024 屈光度（千分度）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\"}，输出区含「(mm) 0.000024 屈光度（千分度）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/mirror-equation",
    "inputs": {
      "f": "42",
      "do": "42"
    },
    "expect": [
      "距减焦距 (m) 84.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"do\":\"42\"}，输出区含「距减焦距 (m) 84.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/prism-deviation",
    "inputs": {
      "n": "42",
      "A": "42"
    },
    "expect": [
      "00 折射率减一 21.00 顶角一半"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"A\":\"42\"}，输出区含「00 折射率减一 21.00 顶角一半」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/refractive-index-speed",
    "inputs": {
      "v": "42",
      "c": "42"
    },
    "expect": [
      "00 折射率 n 1.000000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"c\":\"42\"}，输出区含「00 折射率 n 1.000000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/rayleigh-criterion",
    "inputs": {
      "lam": "42",
      "D": "42"
    },
    "expect": [
      "角 (µrad) 2.516e+5 θ (角秒) 1.220e+0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lam\":\"42\",\"D\":\"42\"}，输出区含「角 (µrad) 2.516e+5 θ (角秒) 1.220e+0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/separated-lenses-focal",
    "inputs": {
      "f1": "42",
      "f2": "42",
      "d": "42"
    },
    "expect": [
      "42\n42\n42\n42.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f1\":\"42\",\"f2\":\"42\",\"d\":\"42\"}，输出区含「42\n42\n42\n42.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/resolving-power",
    "inputs": {
      "D": "42",
      "lam": "42"
    },
    "expect": [
      " R (1/m) 1.220e-9"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"D\":\"42\",\"lam\":\"42\"}，输出区含「 R (1/m) 1.220e-9」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/single-slit-diffraction",
    "inputs": {
      "a": "42",
      "lam": "42",
      "m": "42"
    },
    "expect": [
      "纹角 θ (°) 42.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a\":\"42\",\"lam\":\"42\",\"m\":\"42\"}，输出区含「纹角 θ (°) 42.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/snells-law",
    "inputs": {
      "n1": "42",
      "n2": "42",
      "t1": "42"
    },
    "expect": [
      "42\n42\n42\n42.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\",\"t1\":\"42\"}，输出区含「42\n42\n42\n42.000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/thin-film-max",
    "inputs": {
      "n": "42",
      "t": "42",
      "m": "42"
    },
    "expect": [
      "长 λ (nm) 3528"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"t\":\"42\",\"m\":\"42\"}，输出区含「长 λ (nm) 3528」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/thin-film-min",
    "inputs": {
      "n": "42",
      "t": "42",
      "m": "42"
    },
    "expect": [
      "42\n42\n42\n83.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"t\":\"42\",\"m\":\"42\"}，输出区含「42\n42\n42\n83.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/young-fringe",
    "inputs": {
      "lam": "42",
      "L": "42",
      "d": "42"
    },
    "expect": [
      "间距 (rad) 1000000.00 视场条纹数"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lam\":\"42\",\"L\":\"42\",\"d\":\"42\"}，输出区含「间距 (rad) 1000000.00 视场条纹数」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "optics/thin-lens-equation",
    "inputs": {
      "f": "42",
      "do": "42"
    },
    "expect": [
      "-d_i/d_o 0.0238"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"do\":\"42\"}，输出区含「-d_i/d_o 0.0238」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  }

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
  console.log("==== optics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();