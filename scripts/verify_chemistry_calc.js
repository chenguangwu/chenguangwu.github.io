#!/usr/bin/env node
/**
 * chemistry 分类计算正确性验证（27 个确定性数值工具，全覆盖）
 * 期望值由独立复算得出，输入避开页面默认值，含「默认态假通过自检」。
 * 用法: node scripts/verify_chemistry_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "chemistry/acid-base-titration",
    inputs: { Ca: "0.5", Va: "100", na: "1", Cb: "0.2", nb: "1" },
    expect: ["250.00", "0.5000"],
    ref: "Vb=0.5*100*1/(0.2*1)=250.00；回算=0.2*250*1/(100*1)=0.5000" },

  { slug: "chemistry/arrhenius",
    inputs: { A: "2e13", Ea: "52000", T: "310" },
    expect: ["3.458e+4"],
    ref: "k=2e13*exp(-52000/(8.314*310))=3.458e4；指数项=-20.18" },

  { slug: "chemistry/boiling-point-elevation",
    inputs: { Kb: "0.512", m: "0.5", i: "2" },
    expect: ["0.5120", "100.5120"],
    ref: "ΔTb=0.512*0.5*2=0.5120；沸点=100.5120" },

  { slug: "chemistry/buffer-ph",
    inputs: { pKa: "4.76", Abase: "0.1", HA: "0.2" },
    expect: ["4.459", "0.500"],
    ref: "pH=4.76+log10(0.1/0.2)=4.459；比值=0.500" },

  { slug: "chemistry/dilution-c1v1",
    inputs: { c1: "0.5", v1: "100", c2: "0.1", v2: "0" },
    expect: ["500.00", "50.000"],
    ref: "V2=0.5*100/0.1=500.00；C·V=50.000" },

  { slug: "chemistry/empirical-formula",
    inputs: { p1: "24", a1: "12", p2: "4", a2: "1", p3: "32", a3: "16" },
    expect: ["1.00", "2.00", "1.00"],
    ref: "moles=2,4,2→min2→比值1.00,2.00,1.00" },

  { slug: "chemistry/gas-density",
    inputs: { P: "200", M: "44", T: "300" },
    expect: ["3.5282", "0.003528"],
    ref: "ρ=200*44/(8.314*300)=3.5282 g/L；kg/m3=0.003528" },

  { slug: "chemistry/gibbs-free-energy",
    inputs: { dH: "50", dS: "0.1", T: "300" },
    expect: ["20.000", "非自发 (ΔG>0)"],
    ref: "ΔG=50-300*0.1=20.000>0→非自发" },

  { slug: "chemistry/ideal-gas-volume",
    inputs: { n: "2", P: "150", T: "350" },
    expect: ["38.799", "350.00"],
    ref: "V=2*8.314*350/150=38.799 L；回算T=350.00" },

  { slug: "chemistry/kp-kc",
    inputs: { Kc: "0.5", T: "400", dn: "2" },
    expect: ["5.530e+6", "3325.6"],
    ref: "Kp=0.5*(8.314*400)^2=5.530e6；RT=3325.6" },

  { slug: "chemistry/limiting-reagent",
    inputs: { mA: "10", MA: "40", a: "1", mB: "15", MB: "60", b: "2", MP: "18", c: "1" },
    expect: ["0.2500", "0.2500", "0.1250", "2.250"],
    ref: "nA=0.25,nB=0.25,ξA=0.25,ξB=0.125→限量B；产量=0.125*1*18=2.250" },

  { slug: "chemistry/mass-fraction",
    inputs: { ms: "20", mt: "100" },
    expect: ["20.00", "80.00"],
    ref: "w=20/100*100=20.00%；溶剂=80.00" },

  { slug: "chemistry/mass-percent",
    inputs: { ms: "25", msol: "200" },
    expect: ["0.1250", "12.50", "175.00"],
    ref: "w=25/200=0.1250；%=12.50；溶剂=175.00" },

  { slug: "chemistry/mass-to-moles",
    inputs: { m: "18", M: "18" },
    expect: ["1.0000", "1.0000"],
    ref: "n=18/18=1.0000；倒数=1.0000" },

  { slug: "chemistry/molality",
    inputs: { n: "0.5", ms: "0.2" },
    expect: ["2.5000", "2500.00"],
    ref: "b=0.5/0.2=2.5000 mol/kg；mmol=2500.00" },

  { slug: "chemistry/molarity",
    inputs: { n: "0.25", V: "0.5" },
    expect: ["0.5000", "500.00"],
    ref: "c=0.25/0.5=0.5000 mol/L；mmol=500.00" },

  { slug: "chemistry/mole-fraction",
    inputs: { n1: "2", n2: "3", n3: "5" },
    expect: ["20.00", "30.00", "50.00", "10.0000"],
    ref: "x1=20.00%,x2=30.00%,x3=50.00%；总=10.0000" },

  { slug: "chemistry/nernst-equation",
    inputs: { E0: "1.1", n: "2", Q: "10", T: "298" },
    expect: ["1.0704"],
    ref: "E=1.1-(8.314*298/(2*96485))*ln10=1.0704；(RT/nF)ln10=0.02956" },

  { slug: "chemistry/normality",
    inputs: { n: "0.5", z: "2", V: "0.25" },
    expect: ["4.0000", "4.0000"],
    ref: "N=0.5*2/0.25=4.0000" },

  { slug: "chemistry/partial-pressure",
    inputs: { x: "0.3", Pt: "100" },
    expect: ["30.00", "70.00"],
    ref: "Pi=0.3*100=30.00；其余=70.00" },

  { slug: "chemistry/ph-from-ka",
    inputs: { C: "0.01", Ka: "1e-5" },
    expect: ["3.162e-4", "3.500"],
    ref: "h=sqrt(1e-5*0.01)=3.162e-4；pH=3.500" },

  { slug: "chemistry/ph-to-h",
    inputs: { pH: "3" },
    expect: ["1.000e-3", "3.000"],
    ref: "[H+]=10^-3=1.000e-3；回算pH=3.000" },

  { slug: "chemistry/poh-to-ph",
    inputs: { OH: "1e-3" },
    expect: ["3.000", "11.000", "1.000e-11"],
    ref: "pOH=3.000；pH=11.000；[H+]=1.000e-11" },

  { slug: "chemistry/reaction-quotient",
    inputs: { rP: "2", rN: "1", pP: "4", pN: "2", K: "5" },
    expect: ["8.0000", "逆向进行 (Q>K)"],
    ref: "Q=4^2/2^1=8.0000>K=5→逆向进行" },

  { slug: "chemistry/resistivity-from-r",
    inputs: { R: "10", A: "2", L: "5" },
    expect: ["4.000e-6", "2.500e+5"],
    ref: "ρ=10*(2e-6)/5=4.000e-7 Ω·m；κ=2.500e5 S/m" },

  { slug: "chemistry/solubility-product",
    inputs: { cA: "0.01", mA: "2", cB: "0.02", mB: "1" },
    expect: ["2.000e-6", "1.414e-3"],
    ref: "Ksp=0.01^2*0.02=2.000e-6；s=sqrt=1.414e-3" },

  { slug: "chemistry/solution-dilution",
    inputs: { C1: "2", V1: "100", C2: "0.5" },
    expect: ["300.00"],
    ref: "V2=2*100/0.5=400.00；加水=300.00" },

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
  console.log("==== chemistry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();