#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "signal/bandwidth-q", inputs: { f0: "2000", Q: "50" }, expect: ["40.000 带宽"], ref: "Δf=f0/Q=2000/50=40" },
  { slug: "signal/bit-rate-nyquist", inputs: { B: "4000", M: "32" }, expect: ["40000 最大码率", "10.00 每赫兹码率", "5.0000 每符号比特数"], ref: "R_max=2B·log₂(M)=2×4000×log₂(32)=40000 bps；每赫兹码率=R/B=2log₂M=10 bps/Hz（原实现误用 R/2=20000）；每符号比特数=log₂32=5" },
  { slug: "signal/carrier-freq", inputs: { fu: "1300", fl: "800" }, expect: ["1050.000 载波频率"], ref: "f_c=(fu+fl)/2=(1300+800)/2=1050（原 1200/800 中点与默认 1010/990 相同 → 逃生项）" },
  { slug: "signal/cascade-gain-db", inputs: { g1: "12", g2: "18", g3: "6" }, expect: ["36.000 总增益"], ref: "12+18+6=36dB" },
  { slug: "signal/damping-ratio", inputs: { c: "4", k: "100", m: "1" }, expect: ["0.2000 阻尼比"], ref: "ζ=c/(2√(km))=4/(2√100)=0.2" },
  { slug: "signal/db-power-ratio", inputs: { p1: "100", p2: "1" }, expect: ["20.000 分贝值"], ref: "10·log₁₀(100/1)=20" },
  { slug: "signal/db-voltage-ratio", inputs: { v1: "10", v2: "1" }, expect: ["20.000 分贝值"], ref: "20·log₁₀(10/1)=20" },
  { slug: "signal/duty-cycle", inputs: { ton: "3", T: "10" }, expect: ["30.00 占空比"], ref: "D=ton/T×100=3/10×100=30%" },
  { slug: "signal/energy-discrete", inputs: { s: "1 2 3 -1" }, expect: ["15.000 信号能量"], ref: "E=Σx²=1+4+9+1=15" },
  { slug: "signal/fft-resolution", inputs: { fs: "8000", N: "1024" }, expect: ["7.8125 频率分辨率"], ref: "Δf=fs/N=8000/1024=7.8125" },
  { slug: "signal/first-order-rise", inputs: { tau: "0.01" }, expect: ["2.200e-2 上升时间"], ref: "t_r=2.2τ=2.2×0.01=0.022" },
  { slug: "signal/fourier-base", inputs: { T: "0.02" }, expect: ["50.00 基频"], ref: "f0=1/T=1/0.02=50Hz" },
  { slug: "signal/gain-db", inputs: { vout: "10", vin: "1" }, expect: ["20.00 增益"], ref: "G=20·log₁₀(Vout/Vin)=20·log₁₀(10)=20dB" },
  { slug: "signal/group-delay", inputs: { dp: "-90", dw: "2000" }, expect: ["0.000785 群时延"], ref: "τ_g=-(dp·π/180)/dw=-(-90·π/180)/2000=0.000785s（原 dw=1000 与默认 dp=+90 仅差符号，0.001571 会被 -0.001571 命中 → 逃生项）" },
  { slug: "signal/natural-frequency-2nd", inputs: { k: "100", m: "1" }, expect: ["10.0000 固有角频率"], ref: "ωₙ=√(k/m)=√(100/1)=10rad/s" },
  { slug: "signal/nyquist-rate", inputs: { fmax: "3000" }, expect: ["6,000 最小采样率"], ref: "f_s≥2·fmax=2×3000=6000" },
  { slug: "signal/peak-time-2nd", inputs: { wn: "50", zeta: "0.4" }, expect: ["0.0686 峰值时间"], ref: "t_p=π/(ωₙ√(1-ζ²))=π/(50·√0.84)≈0.0686" },
  { slug: "signal/pwm-average", inputs: { D: "50", Vcc: "5" }, expect: ["2.500 平均电压"], ref: "Vavg=(D/100)·Vcc=(50/100)·5=2.5V" },
  { slug: "signal/q-factor", inputs: { f0: "10000", bw: "100" }, expect: ["100.000 品质因数"], ref: "Q=f0/bw=10000/100=100" },
  { slug: "signal/rc-cutoff", inputs: { R: "1000", C: "1e-6" }, expect: ["159.15 截止频率"], ref: "fc=1/(2πRC)=1/(2π·1000·1e-6)=159.15Hz" },
  { slug: "signal/signal-power", inputs: { v: "5", R: "50" }, expect: ["0.5000 功率"], ref: "P=v²/R=25/50=0.5W" },
  { slug: "signal/sine-rms", inputs: { Vpk: "10" }, expect: ["7.0711 有效值"], ref: "Vrms=Vpk/√2=10/√2=7.0711V" },
  { slug: "signal/snr-db", inputs: { ps: "50", pn: "2" }, expect: ["13.979 信噪比"], ref: "SNR=10·log₁₀(Ps/Pn)=10·log₁₀(25)=13.979dB（原 100/1 与默认 10/0.1 比值相同 → 逃生项）" },
  { slug: "signal/steady-state-error", inputs: { Kp: "9" }, expect: ["0.1000 稳态误差"], ref: "e_ss=1/(1+Kp)=1/(1+9)=0.1" },
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