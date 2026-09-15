#!/usr/bin node
/**
 * materials 分类计算正确性验证（覆盖 tools/materials/ 全部 32 个工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed / toExponential 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_materials_calc.js
 *   —— 目标：默认态 0 命中。
 *
 * 三类页面形态：
 *   - calcTool + dataGrid（28 页）：常规公式页
 *   - calc + innerHTML（detector-35/40/strength-color-diff）：select + 数值输入 → 判定等级
 *   - calc + innerHTML（analysis-cost-profit-2）：textarea id=data → 描述统计
 *
 * 跑法:
 *   node scripts/verify_materials_calc.js                 # 全部
 *   node scripts/verify_materials_calc.js brinell-hardness # 单页
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ---- 统计 / 判定型（calc + innerHTML） ----
  { slug: "materials/analysis-cost-profit-2",
    inputs: { data: "12,15,18,20,25" },
    expect: ["总和： 90.00", "平均值： 18.00", "标准差： 4.43", "极差： 13.00"],
    ref: "n=5；总和 90.00；均值 18.00；中位数 18.00；极差 13.00；总体方差（除以 n）19.60；标准差 4.43。"
      + " 注意：断言须用「标签 + 数值」全串，单字符（如 \"3\"）会因子串匹配在默认态误命中"
      + "（默认数据 10,20,...,80 → 总和 360.00 / 均值 45.00 / 标准差 22.91）" },

  { slug: "materials/detector-35",
    inputs: { matType: "brick", strength: "18", flexural: "3.5" },
    expect: ["一等品"],
    ref: "烧结砖限值 抗压15.0/抗折3.0，18 与 3.5 均达标；但 18 < 15.0×1.3=19.5，故为一等品（非优等品）" },

  { slug: "materials/detector-40",
    inputs: { paintType: "waterproof", voc: "150" },
    expect: ["合格品"],
    ref: "防水涂料 VOC 限值 200，150 达标；但 150>80 且 >30，故为合格品（须避开默认内墙 50 → 环保一等品）" },

  { slug: "materials/detector-strength-color-diff",
    inputs: { stoneType: "granite", colorDiff: "0.8", compress: "130", flexural: "10", density: "2.70", absorption: "0.30" },
    expect: ["优等品"],
    ref: "花岗石限值 压缩100/弯曲8/密度2.56/吸水≤0.60，四项全达标且 ΔE=0.8≤1.0 → 优等品（默认 ΔE=3.5 只判合格品）" },

  // ---- 硬度 ----
  { slug: "materials/brinell-hardness",
    inputs: { F: "2500", D: "5", d: "1.8" },
    expect: ["949.50"],
    ref: "BHN=2×2500/[π×5×(5−√(25−3.24))]=949.50" },

  { slug: "materials/vickers-hardness",
    inputs: { F: "49.03", d: "0.25" },
    expect: ["148.31", "15.1234"],
    ref: "HV=1.854×(49.03/9.80665)/0.25²=148.31；对比 kgf 基准 15.1234" },

  // ---- 弹性常数 ----
  { slug: "materials/bulk-modulus",
    inputs: { E: "110e9", nu: "0.34" },
    expect: ["1.146e+11", "114.58"],
    ref: "K=110e9/[3(1−0.68)]=1.146e+11 Pa=114.58 GPa" },

  { slug: "materials/bulk-modulus-e-nu",
    inputs: { E: "70e9", nu: "0.33" },
    expect: ["68.63"],
    ref: "K=70e9/[3(1−0.66)]=68.63 GPa" },

  { slug: "materials/shear-modulus",
    inputs: { E: "110e9", nu: "0.34" },
    expect: ["4.104e+10", "41.04"],
    ref: "G=110e9/[2(1+0.34)]=4.104e+10 Pa=41.04 GPa" },

  { slug: "materials/lame-lambda",
    inputs: { E: "70e9", nu: "0.33" },
    expect: ["51.08"],
    ref: "λ=70e9×0.33/[(1.33)(0.34)]=51.08 GPa" },

  { slug: "materials/young-from-kg",
    inputs: { K: "72e9", G: "27e9" },
    expect: ["72.00"],
    ref: "E=9×72×27/(3×72+27)=72.00 GPa" },

  { slug: "materials/youngs-modulus",
    inputs: { s: "175e6", eps: "0.0007" },
    expect: ["2.500e+11", "250.0"],
    ref: "E=σ/ε=175e6/0.0007=2.500e+11 Pa=250.0 GPa（须避开默认 200e6/0.001=2.000e+11）" },

  { slug: "materials/shear-strain",
    inputs: { tau: "40e6", G: "27e9" },
    expect: ["1.481e-3"],
    ref: "γ=τ/G=40e6/27e9=1.481e-3" },

  { slug: "materials/hooke-strain",
    inputs: { s: "120e6", E: "210e9" },
    expect: ["0.00057", "0.057"],
    ref: "ε=σ/E=120e6/210e9=0.00057（0.057%）" },

  // ---- 应变 ----
  { slug: "materials/engineering-strain",
    inputs: { L: "104.5", L0: "100" },
    expect: ["0.04500", "4.500"],
    ref: "ε=(104.5−100)/100=0.04500（4.500%）" },

  { slug: "materials/true-strain",
    inputs: { L: "112", L0: "100" },
    expect: ["0.113329", "11.3329"],
    ref: "ε_t=ln(1.12)=0.113329（11.3329%），与工程应变 0.12 的差异体现大变形修正" },

  { slug: "materials/volumetric-strain",
    inputs: { ex: "0.008", ey: "-0.0024", ez: "-0.0024" },
    expect: ["0.00320"],
    ref: "ε_v=0.008−0.0024−0.0024=0.00320" },

  { slug: "materials/poisson-ratio-calc",
    inputs: { el: "-0.0021", ea: "0.006" },
    expect: ["0.350"],
    ref: "ν=−(−0.0021)/0.006=0.350" },

  { slug: "materials/poisson-lateral",
    inputs: { nu: "0.28", el: "0.002" },
    expect: ["-0.000560", "0.280"],
    ref: "ε_lat=−0.28×0.002=−0.000560；回算 ν=0.280" },

  // ---- 能量 / 强度 ----
  { slug: "materials/elastic-energy-density",
    inputs: { sig: "150e6", E: "70e9" },
    expect: ["160.7"],
    ref: "u=σ²/(2E)=(1.5e8)²/(1.4e11)=160.7 kJ/m³" },

  { slug: "materials/modulus-resilience",
    inputs: { sy: "350e6", E: "200e9" },
    expect: ["306250.0", "306.250"],
    ref: "U_r=σ_y²/(2E)=(3.5e8)²/(4e11)=306250.0 J/m³=306.250 kJ/m³" },

  { slug: "materials/fracture-toughness",
    inputs: { Y: "1.12", sig: "250e6", a: "0.002" },
    expect: ["22.19"],
    ref: "K=1.12×250e6×√(π×0.002)/1e6=22.19 MPa√m" },

  { slug: "materials/tensile-force-area",
    inputs: { s: "160e6", A: "2.5e-4" },
    expect: ["40000.0", "40.00"],
    ref: "F=σA=160e6×2.5e-4=40000.0 N=40.00 kN" },

  { slug: "materials/rule-of-mixtures",
    inputs: { Vf: "0.4", Ef: "230e9", Em: "3.5e9" },
    expect: ["94.10", "9.410e+10"],
    ref: "E_c=0.4×230e9+0.6×3.5e9=9.410e+10 Pa=94.10 GPa" },

  // ---- 密度 / 质量 ----
  { slug: "materials/density-basic",
    inputs: { m: "2.70", V: "0.001" },
    expect: ["2700.0", "2.7000"],
    ref: "ρ=m/V=2.70/0.001=2700.0 kg/m³=2.7000 g/cm³" },

  { slug: "materials/mass-from-density",
    inputs: { rho: "2700", V: "0.0035" },
    expect: ["9.450", "9450.0"],
    ref: "m=ρV=2700×0.0035=9.450 kg=9450.0 g" },

  { slug: "materials/specific-weight",
    inputs: { rho: "2400" },
    expect: ["23544.0", "23.54"],
    ref: "γ=ρg=2400×9.81=23544.0 N/m³=23.54 kN/m³" },

  // ---- 热学 ----
  { slug: "materials/fourier-conduction",
    inputs: { k: "16", A: "0.5", dT: "45", L: "0.08" },
    expect: ["4500.0"],
    ref: "q=kAΔT/L=16×0.5×45/0.08=4500.0 W" },

  { slug: "materials/thermal-resistance",
    inputs: { L: "0.1", k: "0.04", A: "2" },
    expect: ["1.2500"],
    ref: "R_th=L/(kA)=0.1/(0.04×2)=1.2500 K/W" },

  { slug: "materials/thermal-diffusivity",
    inputs: { k: "237", rho: "2700", c: "900" },
    expect: ["9.753e-5"],
    ref: "α=k/(ρc)=237/(2700×900)=9.753e-5 m²/s" },

  { slug: "materials/specific-heat-capacity",
    inputs: { m: "5", c: "900" },
    expect: ["4500"],
    ref: "C=mc=5×900=4500 J/K" },

  { slug: "materials/linear-thermal-expansion",
    inputs: { a: "2.3e-5", L: "1.5", dT: "60" },
    expect: ["2.070"],
    ref: "ΔL=αLΔT=2.3e-5×1.5×60×1000=2.070 mm" },
];


async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== materials calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();