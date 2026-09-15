#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "thermodynamics/adiabatic-tv", inputs: {"T1": "300", "V1": "1", "V2": "2", "gamma": "1.4"}, expect: ["-45.79 末态温度"], ref: "adiabatic-tv 公式" },
  { slug: "thermodynamics/biot-number", inputs: {"h": "50", "L": "0.05", "k": "400"}, expect: ["0.0063 毕渥数"], ref: "biot-number 公式" },
  { slug: "thermodynamics/boyles-law", inputs: {"P1": "100", "V1": "2", "P2": "50"}, expect: ["2.0000 体积放大倍数"], ref: "boyles-law 公式" },
  { slug: "thermodynamics/charles-law", inputs: {"V1": "1", "T1": "273.15", "T2": "373.15"}, expect: ["1.3661 体积放大倍数"], ref: "charles-law 公式" },
  { slug: "thermodynamics/compressor-isentropic-work", inputs: {"T1": "300", "PR": "8", "g": "1.4", "Rgas": "287"}, expect: ["244529.7 单位质量压缩功"], ref: "compressor-isentropic-work 公式" },
  { slug: "thermodynamics/convective-heat-rate", inputs: {"h": "10", "A": "2", "dT": "20"}, expect: ["400.00 换热率"], ref: "convective-heat-rate 公式" },
  { slug: "thermodynamics/cp-cv-ratio", inputs: {"cp": "1005", "Rgas": "287"}, expect: ["1.400 比热比"], ref: "cp-cv-ratio 公式" },
  { slug: "thermodynamics/diesel-efficiency", inputs: {"r": "18", "rho": "2", "g": "1.4"}, expect: ["63.16 热效率"], ref: "diesel-efficiency 公式" },
  { slug: "thermodynamics/entropy-change", inputs: {"Q": "4186", "T": "373.15"}, expect: ["11.218 熵变"], ref: "entropy-change 公式" },
  { slug: "thermodynamics/entropy-generation", inputs: {"dsSys": "10", "dsSurr": "-9"}, expect: ["1.000 熵产"], ref: "entropy-generation 公式" },
  { slug: "thermodynamics/first-law", inputs: {"Q": "1000", "W": "400"}, expect: ["60.00 占吸热比"], ref: "first-law 公式" },
  { slug: "thermodynamics/fourier-number", inputs: {"alpha": "1e-5", "t": "100", "L": "0.01"}, expect: ["10.000 傅里叶数"], ref: "fourier-number 公式" },
  { slug: "thermodynamics/gay-lussac-law", inputs: {"P1": "100", "T1": "300", "T2": "400"}, expect: ["1.3333 压强放大倍数"], ref: "gay-lussac-law 公式" },
  { slug: "thermodynamics/grashof-number", inputs: {"g": "9.81", "beta": "0.003", "dT": "10", "L": "0.1", "nu": "1.5e-5"}, expect: ["6 格拉晓夫数"], ref: "grashof-number 公式" },
  { slug: "thermodynamics/heat-conduction", inputs: {"k": "400", "A": "0.01", "dT": "100", "L": "0.1"}, expect: ["400000.0 热流密度"], ref: "heat-conduction 公式" },
  { slug: "thermodynamics/humid-air-enthalpy", inputs: {"t": "25", "w": "0.01"}, expect: ["25.150 干空气部分"], ref: "humid-air-enthalpy 公式" },
  { slug: "thermodynamics/ideal-gas-pressure", inputs: {"n": "1", "T": "273.15", "V": "22.414"}, expect: ["101319.2 压强"], ref: "ideal-gas-pressure 公式" },
  { slug: "thermodynamics/isothermal-work", inputs: {"n": "1", "T": "300", "V1": "1", "V2": "2"}, expect: ["1728.8 膨胀功"], ref: "isothermal-work 公式" },
  { slug: "thermodynamics/latent-heat", inputs: {"m": "1", "L": "334000"}, expect: ["0.334 热量"], ref: "latent-heat 公式" },
  { slug: "thermodynamics/linear-expansion", inputs: {"alpha": "1.2e-5", "L0": "1000", "dT": "50"}, expect: ["1000.600 末长"], ref: "linear-expansion 公式" },
  { slug: "thermodynamics/lmtd-heat-exchanger", inputs: {"dt1": "60", "dt2": "30"}, expect: ["43.28 对数平均温差"], ref: "lmtd-heat-exchanger 公式" },
  { slug: "thermodynamics/newton-cooling", inputs: {"T0": "100", "Tinf": "20", "k": "0.05", "t": "30"}, expect: ["37.85 t 时刻温度"], ref: "newton-cooling 公式" },
  { slug: "thermodynamics/otto-efficiency", inputs: {"r": "10", "g": "1.4"}, expect: ["60.19 热效率"], ref: "otto-efficiency 公式" },
  { slug: "thermodynamics/polytropic-work", inputs: {"p1": "100", "v1": "1", "p2": "50", "v2": "2", "n": "1.3"}, expect: ["0.00 过程功"], ref: "polytropic-work 公式" },
  { slug: "thermodynamics/specific-heat-q", inputs: {"m": "1", "c": "4186", "T1": "20", "T2": "30"}, expect: ["41.860 热量"], ref: "specific-heat-q 公式" },
  { slug: "thermodynamics/stefan-boltzmann", inputs: {"eps": "1", "A": "1", "T": "300"}, expect: ["459.27 辐射出射度"], ref: "stefan-boltzmann 公式" },
  { slug: "thermodynamics/thermal-resistance-series", inputs: {"L1": "0.1", "k1": "0.04", "L2": "0.2", "k2": "1.0", "A": "1"}, expect: ["0.37 总传热系数"], ref: "thermal-resistance-series 公式" }];

async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    const r = await runCase(c);
    if (r.ok) { pass++; console.log(`  ✅ ${c.slug} (via ${r.via})`); }
    else { fails.push(c.slug); console.log(`  ❌ ${c.slug} ${r.why}`);
      if (r.sample) console.log(`     got: ${r.sample.slice(0, 100)}`);
    }
  }
  console.log(`\n==== thermodynamics calc ${pass}/${cases.length} ====`);
  if (fails.length) process.exit(1);
}
main();
