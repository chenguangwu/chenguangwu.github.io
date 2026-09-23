#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "mechanical/beam-point-load",
  "inputs": {
    "L": "5",
    "F": "15",
    "E": "25",
    "I": "8000",
    "b": "200",
    "h": "400"
  },
  "expect": [
    "18.75 最大弯矩 M (kN·m)",
    "19.53 跨中挠度 δ (mm)",
    "3.52 跨中弯曲应力 σ (MPa)"
  ],
  "ref": "去默认化（原 4/10/30/5000/150/300 全为默认值，expect「跨中弯曲应力」只是卡片标签、默认态同样出现）：M=F·L/4=15×5/4=18.75 kN·m；δ=F·L³/(48EI)=15000×125/(48×25e9×8e−5)=19.53 mm（I=8000 cm⁴=8e−5 m⁴）；σ=M/W，W=b·h²/6=200×400²/6=5.333e6 mm³ ⇒ 18.75e6/5.333e6=3.52 MPa。默认态为 10.00/8.89/4.44"
},
{
  "slug": "mechanical/calc-1",
  "inputs": {
    "d1": "140",
    "d2": "355",
    "a": "900",
    "n1": "1460",
    "slip": "2",
    "power": "7.5"
  },
  "expect": [
    "10.70 带速 v（m/s）",
    "2590.4 基准带长 Ld（mm）",
    "700.8 有效拉力 F（N）",
    "2.590 带长（m）"
  ],
  "ref": "去默认化（原 125/315/800/1450/1.5/5.5 全为默认值，expect「推荐带速」是页脚静态提示文案）：i=355/140=2.54；i′=355/(140×0.98)=2.59；v=π·d₁·n₁/60000=π×140×1460/60000=10.70 m/s；n₂=1460/2.5875=564.3；α₁=180−(355−140)/900×57.3=166.3°；Ld≈2590.4 mm；F=1000P/v=7500/10.70=700.8 N。默认态为 9.49/2302.4/579.5/2.302。**注意**：包角 166.3° 与默认 166.4° 仅差 0.1，刻意不锚"
},
{
  "slug": "mechanical/calc-2",
  "inputs": {
    "z1": "21",
    "z2": "63",
    "p": "19.05",
    "a0": "600",
    "n1": "980",
    "power": "11"
  },
  "expect": [
    "6.53 链速 v（m/s）",
    "106 链节数 Lp（取偶）",
    "127.82 小轮分度圆（mm）",
    "1683.5 紧边拉力 F（N）"
  ],
  "ref": "去默认化（原 19/57/15.875/500/970/7.5 全为默认值，expect「普通滚子链」是页脚静态提示文案）：i=3.00；v=z₁·p·n₁/60000=21×19.05×980/60000=6.53 m/s；n₂=980/3=326.7；Lp=2×600/19.05+42+(42/2π)²×19.05/600=106.41→取偶 106；d₁=p/sin(π/z₁)=127.82 mm；F=1000×11/6.5346=1683.5 N。**同时修页面量纲错**：包角原式用 (z₂−z₁)·p（周长差，比直径差大约 π 倍）⇒ 已改为 (d₂−d₁)，本例 155.7°（原 103.6°）、默认态 158.0°（原 110.9°）。**注意**：传动比 3.00 换值后不变，不可作 expect"
},
{
  "slug": "mechanical/centrifugal-force",
  "inputs": {
    "m": "15",
    "r": "0.8",
    "rpm": "900"
  },
  "expect": [
    "106591.7 离心力 F (N)",
    "106.59 离心力 F (kN)",
    "94.25 角速度 ω (rad/s)"
  ],
  "ref": "去默认化（原 10/0.5/600 全为默认值，expect「角速度」只是卡片标签）：ω=2π×900/60=94.248 rad/s；F=m·ω²·r=15×8882.6×0.8=106591.7 N=106.59 kN。默认态为 19739.2/19.74/62.83"
},
{
  "slug": "mechanical/flywheel-energy",
  "inputs": {
    "m": "80",
    "r": "0.45",
    "rpm": "1200"
  },
  "expect": [
    "8.100 转动惯量 I (kg·m²)",
    "63955.0 转动动能 E (J)",
    "63.96 转动动能 E (kJ)"
  ],
  "ref": "去默认化（原 50/0.3/1000 全为默认值，expect「转动动能」只是卡片标签）：实心圆盘 I=m·r²/2=80×0.2025/2=8.100 kg·m²；ω=2π×1200/60=125.664 rad/s；E=½·I·ω²=0.5×8.1×15791.4=63955.0 J=63.96 kJ。默认态为 2.250/12337.0/12.34"
},
{
  "slug": "mechanical/gear-ratio",
  "inputs": {
    "z1": "18",
    "z2": "54",
    "n1": "1450",
    "T1": "150",
    "eta": "0.95"
  },
  "expect": [
    "3.000 传动比 i (=z₂/z₁)",
    "483.3 输出转速 n₂ (rpm)",
    "427.5 输出转矩 T₂ (N·m)"
  ],
  "ref": "去默认化（原 20/40/1500/100/0.97 全为默认值，expect「输出转矩」只是卡片标签）：i=54/18=3.000；n₂=1450/3=483.3 rpm；T₂=T₁·i·η=150×3×0.95=427.5 N·m。默认态为 2.000/750.0/194.0"
},
{
  "slug": "mechanical/lever-advantage",
  "inputs": {
    "Lin": "1.5",
    "Lout": "0.25"
  },
  "expect": [
    "6.00 机械增益 MA (=L₁/L₂)",
    "0.17 所需动力 / 阻力"
  ],
  "ref": "去默认化（原 1.0/0.2 全为默认值，expect「阻力」只是卡片标签尾部）：MA=L₁/L₂=1.5/0.25=6.00；动力/阻力=L₂/L₁=0.1667→0.17。默认态为 5.00/0.20"
},
{
  "slug": "mechanical/spring-rate",
  "inputs": {
    "d": "5",
    "D": "30",
    "n": "6",
    "G": "79"
  },
  "expect": [
    "弹簧刚度"
  ]
},
{
  "slug": "mechanical/torque-power",
  "inputs": {
    "P": "11",
    "n": "960"
  },
  "expect": [
    "109.4 转矩 T (N·m)",
    "100.53 角速度 ω (rad/s)",
    "11.0 校验功率 P (kW)"
  ],
  "ref": "去默认化（原 7.5/1450 全为默认值，expect「校验功率」只是卡片标签）：ω=2π×960/60=100.531 rad/s；T=P/ω=11000/100.531=109.42 N·m；校验功率=T·ω/1000=11.0 kW（回算闭合）。默认态为 49.4/151.84/7.5"
},
{
  "slug": "mechanical/bearing-life",
  "inputs": {
    "cLoad": "53",
    "pLoad": "8",
    "rpm": "1500",
    "a3": "1"
  },
  "expect": [
    "1×1×1×3231"
  ],
  "ref": "auto-restore"
},
{
  "slug": "mechanical/belt-drive",
  "inputs": {
    "n1": "1453",
    "d1": "120",
    "d2": "360",
    "center": "500",
    "slip": "2"
  },
  "expect": [
    "1453×120/360×0.98"
  ],
  "ref": "auto-restore"
},
{
  "slug": "mechanical/cutting-speed",
  "inputs": {
    "diameter": "53",
    "rpm": "800",
    "millD": "20",
    "millN": "3000",
    "teeth": "4"
  },
  "expect": [
    "×53×240/1000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "mechanical/gear-parameters",
  "inputs": {
    "module": "5",
    "z1": "24",
    "z2": "36",
    "alpha": "20",
    "haCoef": "1",
    "cCoef": "0.25",
    "x1": "0",
    "x2": "0"
  },
  "expect": [
    "120.0+10.00+0.00"
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
  console.log("==== mechanical calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
