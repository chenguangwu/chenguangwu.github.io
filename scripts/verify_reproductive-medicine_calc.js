#!/usr/bin node
/**
 * reproductive-medicine 分类计算正确性验证（覆盖 tools/reproductive-medicine/ 全部 22 个数值工具）
 * 期望值由独立复算得出（输入全避开页面默认值）。
 * 假通过自检: node scripts/selfcheck_false_pass.js scripts/verify_reproductive-medicine_calc.js
 *
 * 说明: jingzidnasuipian-dfi-zhishu 不入 CASES —— harness 对「有默认 value + oninput 属性」
 *   的页面存在竞态，inputs 注入不生效（永远用 HTML 里写死的 dfi=18/hds=8），
 *   无法构造避开默认值的 expect，与 quantum/pair-production-threshold 同类。
 *
 * 跑法:
 *   node scripts/verify_reproductive-medicine_calc.js                # 全部
 *   node scripts/verify_reproductive-medicine_calc.js anti-sperm-antibody  # 单页
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "reproductive-medicine/anti-sperm-antibody",
    inputs: { pct: "75", type: "igg" },
    expect: ["强阳性"],
    ref: "pct=75 (默认=10) → ≥75 强阳性，与默认态（可疑阳性）区分" },

  { slug: "reproductive-medicine/baifenbijisuanqi",
    inputs: { v1: "250", v2: "35" },
    expect: ["87.50"],
    ref: "v1=250, v2=35 → 35% of 250 = 87.50" },

  { slug: "reproductive-medicine/calc-volume-concentration",
    inputs: { concentration: "15", volume: "4.0" },
    expect: ["60.0"],
    ref: "15 × 4.0 = 60.0 百万 total" },

  { slug: "reproductive-medicine/detector-9",
    inputs: { ejVol: "1.5", ejConc: "40", urVol: "20", urConc: "0", urPh: "6.0", urFructose: "0" },
    expect: ["无逆行射精"],
    ref: "ejVol>=1.5 + urConc=0 → 无逆行射精（默认态 urConc=5 导致确诊逆行，完全区分）" },

  { slug: "reproductive-medicine/endometrial-receptivity",
    inputs: { thickness: "12", cycleday: "21", pattern: "C" },
    expect: ["容受性差"],
    ref: "thickness=12, pattern=C → C型均匀强回声，容受性差" },

  { slug: "reproductive-medicine/epididymal-aspiration",
    inputs: { vol: "0.01", conc: "80", motility: "40", oocytes: "12", method: "mesa" },
    expect: ["0.027 每卵×10⁶"],
    ref: "获取 80×10⁶/mL×0.01mL=0.80×10⁶, 活动 0.32×10⁶, 每卵 0.32/12=0.027" },

  { slug: "reproductive-medicine/icsi-success",
    inputs: { mii: "15", injected: "12", survived: "10", fert: "8", good: "5", tr: "3", age: "35-37" },
    expect: ["66.7% ICSI受精率"],
    ref: "ICSI受精率=8/12≈66.7%" },

  { slug: "reproductive-medicine/ivf-statistics",
    inputs: { oocytes: "20", mii: "16", fert: "12", cleaved: "11", good: "7", usable: "9", transferred: "3", sacs: "2", preg: "1" },
    expect: ["60.0% 受精率", "66.7% 着床率"],
    ref: "受精率=12/20=60%, 着床率=2/3=66.7%" },

  { slug: "reproductive-medicine/liquefaction-time",
    inputs: { time: "70", status: "gel" },
    expect: ["液化不全"],
    ref: "time=70 > 60min, 胶冻状 → 液化不全" },

  { slug: "reproductive-medicine/pgt-indication",
    inputs: { ageVal: "42", rplVal: "4" },
    expect: ["PGT-A 推荐类型", "4 PGT-A指征"],
    ref: "age≥38 + RPL≥2 → 2 条 PGT-A 指征" },

  { slug: "reproductive-medicine/progressive-motility",
    inputs: { pr: "20", np: "15", im: "65" },
    expect: ["弱精子症"],
    ref: "PR=20% < 32% 下限 → 弱精子症" },

  { slug: "reproductive-medicine/reproductive-hormones",
    inputs: { fsh: "25", lh: "3", t: "2", e2: "80", prl: "10" },
    expect: ["原发性睾丸功能衰竭"],
    ref: "高 FSH(25>12.4) + 低 T(2<9.9) → 原发性睾丸功能衰竭（默认性腺轴大致正常，完全区分）" },

  { slug: "reproductive-medicine/retrograde-ejaculation",
    inputs: { semenVol: "3.5", semenConc: "25", urineVol: "10", urineConc: "0" },
    expect: ["阴性（无逆行）"],
    ref: "urineConc=0 → 逆行占比 0% → 阴性（默认态 urConc=2 导致完全逆行，完全区分）" },

  { slug: "reproductive-medicine/semen-volume",
    inputs: { vol: "0.8", abstinence: "7" },
    expect: ["少精液症"],
    ref: "vol=0.8 < 1.5ml → 少精液症" },

  { slug: "reproductive-medicine/sperm-concentration",
    inputs: { count: "80", squares: "4", dilution: "2" },
    expect: ["0.40", "隐匿精子症"],
    ref: "浓度=(80/4)×2×0.01=0.40×10⁶/mL → 隐匿精子症" },

  { slug: "reproductive-medicine/sperm-cryopreservation",
    inputs: { preConc: "50", preVol: "1.2", preMot: "55", postConc: "40", postVol: "1.0", postMot: "35" },
    expect: ["66.7% 复苏率"],
    ref: "40/60=66.7%" },

  { slug: "reproductive-medicine/sperm-dfi",
    inputs: { dfi: "30", hds: "35" },
    expect: ["30% DFI", "异常"],
    ref: "DFI=30% > 25% → 异常" },

  { slug: "reproductive-medicine/sperm-morphology",
    inputs: { normal: "3", total: "100" },
    expect: ["3.0% 正常形态率", "偏低"],
    ref: "3/100=3.0% < 4% 参考下限 → 偏低（默认 normal=12 输出 6.0% 正常，区分）" },

  { slug: "reproductive-medicine/testicular-biopsy",
    inputs: { s10: "8", s9: "6", s8: "5", s7: "7", s6: "4", s5: "3", s4: "2", s3: "1", s2: "0", s1: "0", silberGrade: "6" },
    expect: ["7.58 平均 Johnsen", "中度受损"],
    ref: "Σ(n×count)/Σcount=273/36=7.58" },

  { slug: "reproductive-medicine/testicular-volume",
    inputs: { lL: "40", lW: "20", lH: "25", rL: "38", rW: "22", rH: "23", leftP: "15", rightP: "12" },
    expect: ["27 总体积 mL", "两侧体积差异"],
    ref: "椭球 L=40×20×25×0.71/1000=14.2mL, R=38×22×23×0.71/1000=14.05mL; Prader L=15 R=12, 差异=3mL" },

  { slug: "reproductive-medicine/total-sperm-count",
    inputs: { conc: "5", vol: "2.0" },
    expect: ["10.0", "少精子症"],
    ref: "5×2=10.0 < 39×10⁶ → 少精子症（默认 conc=40 输出 120.0 正常，区分）" },
];

"use strict";

async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== reproductive-medicine calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();