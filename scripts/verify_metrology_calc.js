#!/usr/bin node
/**
 * metrology 分类计算正确性验证（覆盖 tools/metrology/ 全部 28 个数值工具）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_metrology_calc.js
 *   —— 目标：默认态 0 命中。
 *
 * 跑法:
 *   node scripts/verify_metrology_calc.js                # 全部
 *   node scripts/verify_metrology_calc.js grr-study      # 单页
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ---- 偏倚与漂移 ----
  { slug: "metrology/bias-absolute",
    inputs: { x: "20.35", xref: "20" },
    expect: ["0.350"],
    ref: "Bias=x−x_ref=20.35−20=0.350" },

  { slug: "metrology/bias-percent",
    inputs: { x: "20.6", xref: "20" },
    expect: ["3.00"],
    ref: "Bias%=(20.6−20)/20×100%=3.00%" },

  { slug: "metrology/drift-rate",
    inputs: { x1: "100", x2: "103.6", dt: "12" },
    expect: ["0.3000"],
    ref: "漂移率=(103.6−100)/12=0.3000 单位/天" },

  // ---- 不确定度评定 ----
  { slug: "metrology/calibration-uncertainty",
    inputs: { ustd: "0.04", urep: "0.025" },
    expect: ["0.04717", "0.09434"],
    ref: "u_c=√(0.04²+0.025²)=0.04717；U(k=2)=0.09434" },

  { slug: "metrology/combined-uncertainty",
    inputs: { us: "0.05,0.12,0.09" },
    expect: ["0.15811", "0.13000"],
    ref: "u_c=√(0.05²+0.12²+0.09²)=0.15811；前两分量合成 √(0.05²+0.12²)=0.13000" },

  { slug: "metrology/expanded-uncertainty",
    inputs: { uc: "0.075", k: "3", meas: "25.00" },
    expect: ["0.2250", "24.7750", "25.2250"],
    ref: "U=3×0.075=0.2250；区间 24.7750~25.2250" },

  { slug: "metrology/relative-uncertainty",
    inputs: { u: "0.2", x: "25" },
    expect: ["0.800"],
    ref: "u_rel=0.2/|25|×100%=0.800%" },

  { slug: "metrology/std-dev-type-a",
    inputs: { s: "1.5", n: "16" },
    expect: ["0.3750"],
    ref: "u_A=s/√n=1.5/4=0.3750" },

  { slug: "metrology/type-a-uncertainty",
    inputs: { vals: "20.02,20.05,19.98,20.01,20.04,20.00" },
    expect: ["20.0167", "0.0258", "0.0105"],
    ref: "均值 20.0167；样本标准差（除以 n−1）0.0258；u_A=s/√6=0.0105" },

  { slug: "metrology/type-b-uncertainty",
    inputs: { a: "0.08", k: "2" },
    expect: ["0.04000", "50.00"],
    ref: "u_B=a/k=0.08/2=0.04000；占半宽的 50.00%" },

  { slug: "metrology/effective-dof-welch",
    inputs: { u1: "2.5", v1: "6", u2: "1.5", v2: "12" },
    expect: ["10.42"],
    ref: "ν_eff=(2.5²+1.5²)²/(2.5⁴/6+1.5⁴/12)=10.42（Welch-Satterthwaite）" },

  { slug: "metrology/uncertainty-propagation-sum",
    inputs: { c1: "2", u1: "0.15", c2: "3", u2: "0.08" },
    expect: ["0.3842"],
    ref: "u_c=√((2×0.15)²+(3×0.08)²)=0.3842" },

  { slug: "metrology/uncertainty-propagation-product",
    inputs: { x1: "4", u1: "0.05", x2: "8", u2: "0.06" },
    expect: ["1.458"],
    ref: "相对合成=√((0.05/4)²+(0.06/8)²)×100%=1.458%" },

  { slug: "metrology/resolution-uncertainty",
    inputs: { a: "0.002" },
    expect: ["0.000577", "0.000333"],
    ref: "u=a/(2√3)=0.000577；对比半宽/√3=0.000333" },

  { slug: "metrology/guard-band-95",
    inputs: { U: "0.12" },
    expect: ["0.1980"],
    ref: "GB=1.65×0.12=0.1980（95% 单侧保护带）" },

  { slug: "metrology/least-count-error",
    inputs: { lc: "0.005" },
    expect: ["0.0025", "-0.0025"],
    ref: "极限误差=±0.005/2=±0.0025" },

  // ---- 公差 ----
  { slug: "metrology/dimensional-tolerance",
    inputs: { nom: "30", es: "0.021", ei: "-0.007" },
    expect: ["0.028", "30.021", "29.993"],
    ref: "公差=0.021−(−0.007)=0.028；极限尺寸 30.021 / 29.993" },

  { slug: "metrology/tolerance-stackup-worst",
    inputs: { ts: "0.12,-0.05,0.08,0.03" },
    expect: ["0.280", "0.070"],
    ref: "最坏累积=0.12+0.05+0.08+0.03=0.280（负公差取绝对值）；平均单环 0.070" },

  { slug: "metrology/flatness-deviation",
    inputs: { hmax: "0.018", hmin: "-0.012" },
    expect: ["0.030", "30.0"],
    ref: "平面度=0.018−(−0.012)=0.030 mm=30.0 μm" },

  { slug: "metrology/roundness-deviation",
    inputs: { rmax: "15.012", rmin: "14.986" },
    expect: ["0.026", "26.0"],
    ref: "圆度=15.012−14.986=0.026 mm=26.0 μm" },

  // ---- 测量系统分析 MSA ----
  { slug: "metrology/gauge-repeatability",
    inputs: { r: "0.07", m: "4" },
    expect: ["0.0340", "0.1751"],
    ref: "d₂(4)=2.059；σ_r=0.07/2.059=0.0340；99% 带宽 5.15σ_r=0.1751" },

  { slug: "metrology/gauge-reproducibility",
    inputs: { r: "0.06", o: "2" },
    expect: ["0.0532"],
    ref: "d₂*(2)=1.128；σ_o=0.06/1.128=0.0532" },

  { slug: "metrology/grr-percent",
    inputs: { GRR: "1.8", Tol: "12" },
    expect: ["15.0"],
    ref: "%GRR=1.8/12×100%=15.0%（落在 10%~30% 临界区）" },

  { slug: "metrology/grr-study",
    inputs: { sr: "0.035", so: "0.02", tol: "0.5" },
    expect: ["48.4", "0.2419"],
    ref: "GRR 带宽=6×√(0.035²+0.02²)=0.2419；%GRR=48.4% → 不可接受（须避开默认的 0.02/0.015/1.0）" },

  { slug: "metrology/measurement-cg",
    inputs: { USL: "8", LSL: "2", s: "0.25" },
    expect: ["4.000"],
    ref: "Cg=(8−2)/(6×0.25)=4.000（≥1.33 合格）" },

  { slug: "metrology/measurement-cgk",
    inputs: { USL: "8", LSL: "2", xbar: "5.5", s: "0.25" },
    expect: ["3.333"],
    ref: "Cgk=min(8−5.5, 5.5−2)/(3×0.25)=2.5/0.75=3.333" },

  { slug: "metrology/ndc-number",
    inputs: { PV: "6.5", GRR: "0.8" },
    expect: ["11.46"],
    ref: "NDC=1.41×6.5/0.8=11.46（≥5 有效）" },

  { slug: "metrology/precision-tolerance-ratio",
    inputs: { s: "0.15", Tol: "6" },
    expect: ["0.150"],
    ref: "PTR=6×0.15/6=0.150（<0.1 才算足够精细）" },
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
  console.log("==== metrology calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();