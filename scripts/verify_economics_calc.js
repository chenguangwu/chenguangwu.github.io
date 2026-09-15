#!/usr/bin/env node
/**
 * economics 分类计算正确性验证（27 个确定性数值工具，全覆盖）
 * 期望值由独立复算得出（node 按页面公式 toFixed 精确对齐），输入全避开页面默认值。
 * 用法: node scripts/verify_economics_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "economics/average-propensity-consume",
    inputs: { C: "600", Y: "1500" },
    expect: ["0.400"],
    ref: "APC=C/Y=600/1500=0.400" },

  { slug: "economics/balance-of-trade",
    inputs: { X: "300", M: "250" },
    expect: ["50"],
    ref: "BoT=X−M=300−250=50" },

  { slug: "economics/cobb-douglas",
    inputs: { A: "2", K: "100", al: "0.5", L: "64" },
    expect: ["160.00"],
    ref: "Y=A·K^α·L^(1−α)=2·√100·√64=2·10·8=160.00" },

  { slug: "economics/compound-amount",
    inputs: { p: "5000", r: "4", t: "5", n: "2" },
    expect: ["6094.97", "1094.97"],
    ref: "F=5000(1+4/100/2)^(2·5)=6094.97；利息=1094.97" },

  { slug: "economics/cross-elasticity",
    inputs: { qx1: "100", qx2: "80", py1: "10", py2: "12" },
    expect: ["-1.222"],
    ref: "中点弹性 e=(ΔQ/Qmid)/(ΔP/Pmid)=(−20/90)/(2/11)=−1.222（互补品）" },

  { slug: "economics/elasticity-demand",
    inputs: { q1: "120", q2: "100", p1: "8", p2: "10" },
    expect: ["-0.818"],
    ref: "中点弹性 e=(ΔQ/Qmid)/(ΔP/Pmid)=(−20/110)/(2/9)=−0.818" },

  { slug: "economics/fisher-equation",
    inputs: { r: "1.5", pi: "2.5" },
    expect: ["4.00"],
    ref: "i=r+π=1.5+2.5=4.00%" },

  { slug: "economics/fv-annuity",
    inputs: { pmt: "500", i: "2", n: "10" },
    expect: ["5474.86", "474.86"],
    ref: "FV=500·((1.02^10−1)/0.02)=5474.86；利息=474.86" },

  { slug: "economics/gdp-expenditure",
    inputs: { C: "800", I: "250", G: "180", NX: "-30" },
    expect: ["1200"],
    ref: "Y=C+I+G+NX=800+250+180−30=1200" },

  { slug: "economics/gdp-growth-rate",
    inputs: { gt: "1200", gp: "1000" },
    expect: ["20.00"],
    ref: "g=(1200−1000)/1000·100=20.00%" },

  { slug: "economics/income-elasticity",
    inputs: { q1: "100", q2: "90", i1: "1000", i2: "1100" },
    expect: ["-1.105"],
    ref: "中点收入弹性 e=(ΔQ/Qmid)/(ΔI/Imid)=(−10/95)/(100/105)=−1.105（劣等品）" },

  { slug: "economics/inflation-rate",
    inputs: { cpi0: "100", cpi1: "108" },
    expect: ["8.00", "8.00"],
    ref: "π=(108−100)/100·100=8.00%；CPI 变化=8.00" },

  { slug: "economics/labor-force",
    inputs: { E: "200", U: "20" },
    expect: ["220"],
    ref: "LF=E+U=200+20=220" },

  { slug: "economics/labor-force-participation",
    inputs: { lf: "200", pop: "250" },
    expect: ["80.0"],
    ref: "LFP=lf/pop·100=200/250·100=80.0%" },

  { slug: "economics/marginal-product-labor",
    inputs: { dq: "30", dl: "5" },
    expect: ["6.00"],
    ref: "MPL=ΔQ/ΔL=30/5=6.00" },

  { slug: "economics/marginal-propensity-consume",
    inputs: { dc: "60", dy: "150" },
    expect: ["0.400"],
    ref: "MPC=ΔC/ΔY=60/150=0.400" },

  { slug: "economics/mpc-from-multiplier",
    inputs: { k: "4" },
    expect: ["0.750"],
    ref: "MPC=1−1/k=1−1/4=0.750" },

  { slug: "economics/nominal-to-real",
    inputs: { nom: "121", pi: "0.10" },
    expect: ["110.00"],
    ref: "Real=Nom/(1+π)=121/1.10=110.00" },

  { slug: "economics/okuns-law",
    inputs: { g: "2", gp: "5" },
    expect: ["1.50", "-3.00"],
    ref: "Δu=−0.5·(2−5)=1.50；增长缺口=2−5=−3.00" },

  { slug: "economics/present-value",
    inputs: { fv: "10000", r: "4", t: "5" },
    expect: ["8219.27", "1780.73"],
    ref: "PV=10000/1.04^5=8219.27；贴现额=1780.73" },

  { slug: "economics/pv-annuity",
    inputs: { pmt: "500", i: "2", n: "10" },
    expect: ["4491.29", "508.71"],
    ref: "PV=500·(1−1.02^−10)/0.02=4491.29；贴现=508.71" },

  { slug: "economics/real-gdp",
    inputs: { nominal: "1210", defl: "10" },
    expect: ["1100.00", "110.00"],
    ref: "Real=1210/1.10=1100.00；价格扭曲=110.00" },

  { slug: "economics/rule-of-72",
    inputs: { rate: "8" },
    expect: ["9.00", "9.01"],
    ref: "72/8=9.00 年；精确=ln2/ln(1.08)=9.01 年" },

  { slug: "economics/spending-multiplier",
    inputs: { mpc: "0.5" },
    expect: ["2.00", "-1.00"],
    ref: "k=1/(1−0.5)=2.00；k_t=−0.5/0.5=−1.00（原用 0.75 得 4.00/−3.00，其中 \"4.00\" 是默认输出 \"-4.00\" 的子串，会假通过）" },

  { slug: "economics/tax-multiplier",
    inputs: { mpc: "0.6" },
    expect: ["-1.50"],
    ref: "k_t=−MPC/(1−MPC)=−0.6/0.4=−1.50" },

  { slug: "economics/unemployment-rate",
    inputs: { unemp: "500", lf: "8000" },
    expect: ["6.25", "7500"],
    ref: "u=500/8000·100=6.25%；就业=8000−500=7500" },

  { slug: "economics/velocity-of-money",
    inputs: { P: "1", Y: "3000", M: "500" },
    expect: ["6.00"],
    ref: "V=P·Y/M=1·3000/500=6.00" },
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
  console.log("==== economics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();