#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "signal/bandwidth-q", inputs: { f0: "2000", q: "50" }, expect: ["200.000 带宽"], ref: "Δf=1200/30=40" },
  { slug: "signal/bit-rate-nyquist", inputs: { B: "4000", M: "32" }, expect: ["40000 最大码率"], ref: "R_max=2×3000×log₂(16)=24000" },
  { slug: "signal/carrier-freq", inputs: { fupper: "1200", flower: "800" }, expect: ["1000.000 载波频率"], ref: "f_c=(1200+800)/2=1000" },
  { slug: "signal/cascade-gain-db", inputs: { g1: "12", g2: "18", g3: "6" }, expect: ["36.000 总增益"], ref: "12+18+6=36dB" },
  { slug: "signal/damping-ratio", inputs: { mp: "25" }, expect: ["0.1000 阻尼比"], ref: "欠阻尼" },
  { slug: "signal/db-power-ratio", inputs: { p1: "100", p2: "1" }, expect: ["20.000 分贝值"], ref: "10·log₁₀(100)=20" },
  { slug: "signal/db-voltage-ratio", inputs: { v1: "10", v2: "1" }, expect: ["20.000 分贝值"], ref: "20·log₁₀(10)=20" },
  { slug: "signal/duty-cycle", inputs: { ton: "3", t: "10" }, expect: ["30.00 占空比"], ref: "3/10=30%" },
  { slug: "signal/energy-discrete", inputs: { x1: "1", x2: "2", x3: "3", x4: "-1" }, expect: ["15.000 信号能量"], ref: "1+4+9+1=15" },
  { slug: "signal/fft-resolution", inputs: { fs: "8000", n: "1024" }, expect: ["7.8125 频率分辨率"], ref: "8000/1024=7.8125" },
  { slug: "signal/first-order-rise", inputs: { tau: "0.01" }, expect: ["2.200e-2 上升时间"], ref: "t_r=2.2τ" },
  { slug: "signal/fourier-base", inputs: { f0: "50" }, expect: ["50.00 基频"], ref: "f0=50Hz" },
  { slug: "signal/gain-db", inputs: { a: "10" }, expect: ["20.00 增益"], ref: "20·log₁₀(10)=20" },
  { slug: "signal/group-delay", inputs: { phasedeg: "-90", freq: "1000" }, expect: ["-0.001571 群时延"], ref: "τ_g=-dφ/dω" },
  { slug: "signal/natural-frequency-2nd", inputs: { wn: "10", zeta: "0.5" }, expect: ["10.0000 固有角频率"], ref: "ωₙ=10" },
  { slug: "signal/nyquist-rate", inputs: { fmax: "3000" }, expect: ["6,000 最小采样率"], ref: "f_s≥2×4000=8000" },
  { slug: "signal/peak-time-2nd", inputs: { wn: "50", zeta: "0.4" }, expect: ["0.0686 峰值时间"], ref: "t_p=π/(ωₙ√(1-ζ²))" },
  { slug: "signal/pwm-average", inputs: { d: "0.5", vhigh: "5" }, expect: ["2.500 平均电压"], ref: "0.5×5=2.5" },
  { slug: "signal/q-factor", inputs: { f0: "10000", l: "0.01", c: "1e-6" }, expect: ["100.000 品质因数"], ref: "Q=ω₀L/R" },
  { slug: "signal/rc-cutoff", inputs: { r: "1000", c: "1e-6" }, expect: ["159.15 截止频率"], ref: "1/(2πRC)=159.15Hz" },
  { slug: "signal/signal-power", inputs: { amp: "5" }, expect: ["0.5000 功率"], ref: "正弦功率=(5/√2)²=12.5" },
  { slug: "signal/sine-rms", inputs: { amp: "10" }, expect: ["7.0711 有效值"], ref: "10/√2" },
  { slug: "signal/snr-db", inputs: { s: "100", n: "1" }, expect: ["20.000 信噪比"], ref: "10·log₁₀(100)=20" },
  { slug: "signal/steady-state-error", inputs: { step: "1", kp: "9" }, expect: ["0.1000 稳态误差"], ref: "e_ss=1/(1+9)=0.1" },
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
  console.log("==== signal calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();