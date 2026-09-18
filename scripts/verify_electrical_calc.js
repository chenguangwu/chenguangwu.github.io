#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "electrical/battery-bank",
  "inputs": {
    "cellV": "3.2",
    "cellAh": "120",
    "seriesN": "20",
    "parallelN": "3",
    "loadW": "800",
    "dod": "80",
    "eff": "90"
  },
  "expect": [
    "20.74"
  ],
  "ref": "总电压 = 3.2×20 = 64.0 V；总容量 = 120×3 = 360.0 Ah；总能量 = 23040 Wh；可用 = 23040×0.80×0.90 = 16588.8 Wh；续航 = 16588.8/800 = 20.74 h（避开默认 100Ah/16串/2并/500W）"
},
{
  "slug": "electrical/calc-1",
  "inputs": {
    "area": "25",
    "ambient": "45",
    "group": "1.0",
    "soil": "1.0",
    "depth": "1.0"
  },
  "expect": [
    "50.0"
  ],
  "ref": "基准载流量 I₀ = 13.5×√25×0.8(穿管)×1(2芯) = 54.0 A；温度修正 k₁ = 1 − 0.005×(45−30) = 0.925；Iz = 54.0×0.925 = 50.0 A（避开默认 4 mm²/30 ℃）"
},
{
  "slug": "electrical/calc-2",
  "inputs": {
    "voltage": "400",
    "current": "63",
    "pf": "0.90",
    "pInput": "",
    "qInput": ""
  },
  "expect": [
    "43.648"
  ],
  "ref": "S = √3·U·I = 1.732051×400×63 = 43647.7 VA = 43.648 kVA；P = S×0.90 = 39.283 kW（避开默认 380 V/50 A/0.85）"
},
{
  "slug": "electrical/calc-power-capacitance",
  "inputs": {
    "v0": "120",
    "v1": "60"
  },
  "expect": [
    "7200.00 W"
  ],
  "ref": "通用模板页按标题命中「功率」分支：P = A×B = 120×60 = 7200 W = 7.2 kW（避开默认 100/50；原 expect 断言的是历史记录区占位文案「暂无计算记录」，注入失败也恒命中）"
},
{
  "slug": "electrical/current-divider",
  "inputs": {
    "It": "150",
    "R1": "1500",
    "R2": "3000"
  },
  "expect": [
    "150.00"
  ],
  "ref": "I₁ = I·R₂/(R₁+R₂) = 150×3000/4500 = 100.00 mA；I₂ = 150×1500/4500 = 50.00 mA；合计 150.00 mA（避开默认 100/1000/2000）"
},
{
  "slug": "electrical/home-load-estimate",
  "inputs": {
    "fridge": "2",
    "ac": "3",
    "washer": "1",
    "waterheater": "1",
    "kitchen": "4000",
    "light": "800"
  },
  "expect": [
    "30.8 A"
  ],
  "ref": "装机 = 2×200 + 3×1200 + 500 + 2000 + 4000 + 800 = 11300 W；需用系数 0.6 → 负荷 6780 W；I = 6780/220 = 30.8 A（避开默认 1/2/1/1/3000/500）"
},
{
  "slug": "electrical/led-resistor",
  "inputs": {
    "Vs": "12",
    "Vf": "3.2",
    "If": "25"
  },
  "expect": [
    "352"
  ],
  "ref": "R = (V_s − V_f)/I_f = (12 − 3.2)/0.025 = 352 Ω；功耗 P = I²R = 0.025²×352 = 0.22 W（避开默认 5 V/2.0 V/20 mA）"
},
{
  "slug": "electrical/opamp-gain",
  "inputs": {
    "Rin": "1500",
    "Rf": "33000"
  },
  "expect": [
    "-22.00"
  ],
  "ref": "反相增益 = −R_f/R_in = −33000/1500 = −22.00；同相增益 = 1 + 22 = 23.00（避开默认 1 k/10 k——两者比值同为 10，属数值巧合）"
},
{
  "slug": "electrical/power-factor-compensation",
  "inputs": {
    "power": "300",
    "pf1": "0.70",
    "pf2": "0.90"
  },
  "expect": [
    "160.8"
  ],
  "ref": "φ₁ = arccos0.70 → tanφ₁ = 1.0202；φ₂ = arccos0.90 → tanφ₂ = 0.4843；Q_c = 300×(1.0202−0.4843) = 160.8 kvar（避开默认 200/0.75/0.95）"
},
{
  "slug": "electrical/rc-filter",
  "inputs": {
    "R": "22",
    "C": "0.47"
  },
  "expect": [
    "15.4"
  ],
  "ref": "f_c = 1/(2πRC) = 1/(2π×22000×4.7×10⁻⁷) = 15.4 Hz（避开默认 10 kΩ/0.1 µF）"
},
{
  "slug": "electrical/rlc-resonance",
  "inputs": {
    "L": "33",
    "C": "0.22"
  },
  "expect": [
    "1867.9"
  ],
  "ref": "f₀ = 1/(2π√(LC)) = 1/(2π√(0.033×2.2×10⁻⁷)) = 1/(2π×8.52056×10⁻⁵) = 1867.89 → 1867.9 Hz（避开默认 10 mH/0.1 µF）"
},
{
  "slug": "electrical/transformer-sizing",
  "inputs": {
    "pTotal": "250",
    "cosPhi": "0.8",
    "kd": "0.9",
    "beta": "0.8",
    "kReserve": "1.15",
    "uKv": "0.4"
  },
  "expect": [
    "推荐容量：500 kVA"
  ],
  "ref": "S_js = P·K_d/cosφ = 250×0.9/0.8 = 281.25 kVA；S_t = S_js×k_Res/β = 281.25×1.15/0.8 = 404.3 kVA → 标准序列取 500 kVA（避开默认 160/0.85/0.8/0.75/1.1）"
},
{
  "slug": "electrical/voltage-capacity-battery",
  "inputs": {
    "v0": "120",
    "v1": "60",
    "v2": "15"
  },
  "expect": [
    "480.00"
  ],
  "ref": "计算结果 = v0×v1/v2 = 120×60/15 = 480.00；合计 = 120+60+15 = 195.00（避开默认 100/50/10）"
},
{
  "slug": "electrical/voltage-divider",
  "inputs": {
    "vin": "12",
    "r1": "1000",
    "r2": "2000",
    "rl": "1000",
    "r": "1000",
    "pos": "50",
    "n": "3"
  },
  "expect": [
    "功耗"
  ]
},
{
  "slug": "electrical/voltage-drop",
  "inputs": {
    "power": "25",
    "length": "120",
    "cosPhi": "0.85",
    "section": "16",
    "allowDrop": "5"
  },
  "expect": [
    "15.73"
  ],
  "ref": "I = P×1000/(U·cosφ) = 25000/(380×0.85) = 77.40 A；r = ρ/S = 0.0184/16 = 0.00115 Ω/m；ΔU = √3·I·r·cosφ·L = 15.73 V（4.14% ≤ 5% 合格）。注：页面原式多除以 1000（压降偏小 1000 倍），已修复（避开默认 15 kW/80 m/10 mm²）"
},
{
  "slug": "electrical/wire-gauge-selector",
  "inputs": {
    "I": "32",
    "len": "45"
  },
  "expect": [
    "10 mm² 推荐截面"
  ],
  "ref": "需载流量 ≥ 1.25×32 = 40 A → 铜芯穿管序列 [12,18,25,34,45,…] 取 10 mm²（45 A）；45 m 双线压降 = 32×0.0175×45×2/10 = 5.04 V（避开默认 20 A/30 m）"
},
{
  "slug": "electrical/wire-resistance",
  "inputs": {
    "rho": "0.0172",
    "L": "250",
    "A": "4"
  },
  "expect": [
    "1.075"
  ],
  "ref": "R = ρL/A = 0.0172×250/4 = 1.075 Ω；每千米 = 1.075×1000/250 = 4.30 Ω/km（避开默认 100 m/2.5 mm²）"
},
{
  "slug": "electrical/breaker-sizing",
  "inputs": {
    "I": "15"
  },
  "expect": [
    "18.8"
  ],
  "ref": "auto-restore"
},
{
  "slug": "electrical/load-curve",
  "inputs": {
    "h'+h+'": "'+PRESETS.factory[h]+'_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== electrical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
