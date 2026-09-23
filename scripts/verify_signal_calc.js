#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "signal/bandwidth-q", inputs: { f0: "2000", Q: "50" }, expect: ["40.000 带宽"], ref: "Δf=f0/Q=2000/50=40" },
  { slug: "signal/bit-rate-nyquist", inputs: { B: "4000", M: "32" }, expect: ["40000 最大码率", "10.00 每赫兹码率", "5.0000 每符号比特数"], ref: "R_max=2B·log₂(M)=2×4000×log₂(32)=40000 bps；每赫兹码率=R/B=2log₂M=10 bps/Hz（原实现误用 R/2=20000）；每符号比特数=log₂32=5" },
  { slug: "signal/carrier-freq", inputs: { fu: "1300", fl: "800" }, expect: ["1050.000 载波频率"], ref: "f_c=(fu+fl)/2=(1300+800)/2=1050（原 1200/800 中点与默认 1010/990 相同 → 逃生项）" },
  { slug: "signal/cascade-gain-db", inputs: { g1: "12", g2: "18", g3: "6" }, expect: ["36.000 总增益"], ref: "12+18+6=36dB" },
  { slug: "signal/damping-ratio", inputs: { c: "4", k: "100", m: "1" }, expect: ["0.2000 阻尼比"], ref: "ζ=c/(2√(km))=4/(2√100)=0.2" },
  { slug: "signal/db-power-ratio", inputs: { p1: "250", p2: "5" }, expect: ["16.990 分贝值"], ref: "去默认化：L=10·log₁₀(p1/p2)=10·log₁₀(50)=16.990 dB；功率比 50=5.0000e+1、幅值比 √50=7.0711、奈培值 1.9560 Np。默认 100/1 得 20.000 dB" },
  { slug: "signal/db-voltage-ratio", inputs: { v1: "25", v2: "0.5" }, expect: ["33.979 分贝值"], ref: "去默认化：L=20·log₁₀(v1/v2)=20·log₁₀(50)=33.979 dB；电压比 50.0000、反推电压比 50.0000、反推功率比 2500.0000。默认 10/1 得 20.000 dB" },
  { slug: "signal/duty-cycle", inputs: { ton: "3", T: "10" }, expect: ["30.00 占空比"], ref: "D=ton/T×100=3/10×100=30%" },
  { slug: "signal/energy-discrete", inputs: { s: "2 3 -2 1" }, expect: ["18.000 信号能量"], ref: "去默认化：E=Σx²=4+9+4+1=18.000；N=4、平均功率 E/N=4.5000、RMS=√4.5=2.1213。默认 1 2 3 -1 得 15.000" },
  { slug: "signal/fft-resolution", inputs: { fs: "8000", N: "1024" }, expect: ["7.8125 频率分辨率"], ref: "Δf=fs/N=8000/1024=7.8125" },
  { slug: "signal/first-order-rise", inputs: { tau: "0.01" }, expect: ["2.200e-2 上升时间"], ref: "t_r=2.2τ=2.2×0.01=0.022" },
  { slug: "signal/fourier-base", inputs: { T: "0.025" }, expect: ["40.00 基频"], ref: "去默认化：f₀=1/T=1/0.025=40.00 Hz；ω=2πf₀=251.327 rad/s、半周期 0.0125 s。默认 T=0.02 得 50.00 Hz" },
  { slug: "signal/gain-db", inputs: { vout: "20", vin: "0.5" }, expect: ["32.04 增益"], ref: "去默认化：G=20·log₁₀(Vout/Vin)=20·log₁₀(40)=32.04 dB；电压比 40.000、功率比 1600.0000。默认 10/1 得 20.00 dB" },
  { slug: "signal/group-delay", inputs: { dp: "-90", dw: "2000" }, expect: ["0.000785 群时延"], ref: "τ_g=-(dp·π/180)/dw=-(-90·π/180)/2000=0.000785s（原 dw=1000 与默认 dp=+90 仅差符号，0.001571 会被 -0.001571 命中 → 逃生项）" },
  { slug: "signal/natural-frequency-2nd", inputs: { k: "50", m: "2" }, expect: ["5.0000 固有角频率"], ref: "去默认化：ωₙ=√(k/m)=√(50/2)=5.0000 rad/s；fₙ=ωₙ/2π=0.7958 Hz、Tₙ=1.2566 s、47.7 cpm。默认 k=100/m=1 得 10.0000" },
  { slug: "signal/nyquist-rate", inputs: { fmax: "3000" }, expect: ["6,000 最小采样率"], ref: "f_s≥2·fmax=2×3000=6000" },
  { slug: "signal/peak-time-2nd", inputs: { wn: "50", zeta: "0.4" }, expect: ["0.0686 峰值时间"], ref: "t_p=π/(ωₙ√(1-ζ²))=π/(50·√0.84)≈0.0686" },
  { slug: "signal/pwm-average", inputs: { D: "35", Vcc: "12" }, expect: ["4.200 平均电压"], ref: "去默认化：V_avg=(D/100)·Vcc=0.35×12=4.200 V；V_rms=Vcc·√0.35=7.0993 V、关断期电压差 7.800 V。默认 50/5 得 2.500 V" },
  { slug: "signal/q-factor", inputs: { f0: "10000", bw: "100" }, expect: ["100.000 品质因数"], ref: "Q=f0/bw=10000/100=100" },
  { slug: "signal/rc-cutoff", inputs: { R: "2200", C: "1e-7" }, expect: ["723.43 截止频率"], ref: "去默认化：f_c=1/(2πRC)=1/(2π×2200×1e-7)=723.43 Hz；τ=RC=2.2e-4 s、t_r=2.2τ=4.84e-4 s。默认 1000/1e-6 得 159.15 Hz" },
  { slug: "signal/signal-power", inputs: { v: "12", R: "75" }, expect: ["1.9200 功率"], ref: "去默认化：P=V²/R=144/75=1.9200 W；I=12/75=0.1600 A、1920.0000 mW。默认 5/50 得 0.5000 W" },
  { slug: "signal/sine-rms", inputs: { Vpk: "20" }, expect: ["14.1421 有效值"], ref: "去默认化：V_rms=V_pk/√2=20/√2=14.1421 V；V_pp=40.0000、半周期平均 12.7324 V。默认 Vpk=10 得 7.0711" },
  { slug: "signal/snr-db", inputs: { ps: "50", pn: "2" }, expect: ["13.979 信噪比"], ref: "SNR=10·log₁₀(Ps/Pn)=10·log₁₀(25)=13.979dB（原 100/1 与默认 10/0.1 比值相同 → 逃生项）" },
  { slug: "signal/steady-state-error", inputs: { Kp: "19" }, expect: ["0.0500 稳态误差"], ref: "去默认化：e_ss=1/(1+Kp)=1/20=0.0500（5.00%）；稳态误差倒数 20.0000。默认 Kp=9 得 0.1000" }
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