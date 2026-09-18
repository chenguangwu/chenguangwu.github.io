#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
// food-processing 21 例：全部为非默认输入 + 独立复算 expect（Python Decimal/高精度）。
// 复算口径：每例期望值均由页面公式独立推出，且不与页面「深度解析」算例字面量碰撞。
const CASES = [
{
  // 非默认输入：n=2（默认 3）、T=90（默认 95）；Dref/Tref/Z 保持页面 pod 默认
  "slug": "food-processing/blanching-conditions",
  "inputs": { "n": "2", "Dref": "2.5", "Tref": "100", "Z": "25", "T": "90" },
  "expect": ["12.56"],
  "ref": "热烫时间 t = D_T×n = 2.5×10^((100−90)/25)×2 = 6.279716×2 = 12.5594 → 12.56 min（默认 T=95/n=3 得 11.89）"
},
{
  // 非默认输入：flour 800（默认 1000）/water 500（620）/otherLiquid 50（0）
  "slug": "food-processing/dough-absorption",
  "inputs": { "flour": "800", "flourMoist": "12", "water": "500", "otherLiquid": "50", "dryAdd": "30", "dryMoist": "3" },
  "expect": ["68.8%"],
  "ref": "吸水率 =(500+50)/800×100% = 68.75% → 68.8%（默认 1000/620 → 62.0%）"
},
{
  // 非默认输入：total 80（默认 50）/emul 60（42）/serum 20（8）
  "slug": "food-processing/emulsion-stability",
  "inputs": { "total": "80", "emul": "60", "serum": "20", "t": "20", "rpm": "4000" },
  "expect": ["75.0%"],
  "ref": "ESI = 60/80×100% = 75.0%（默认 42/50 → 84.0%）"
},
{
  // 非默认输入：vol 200（100）/b0 24（20）/b1 8（6）/eff 90（92）
  "slug": "food-processing/fermentation-brix",
  "inputs": { "vol": "200", "b0": "24", "b1": "8", "theoYield": "0.511", "eff": "90" },
  "expect": ["9.33%"],
  "ref": "糖耗 =(24−8)×10×200 = 32000 g → 酒精 = 32000×0.511×0.9 = 14716.8 g → ABV = 14716.8/0.789/200000×100 = 9.326% → 9.33%（默认 6.58%）"
},
{
  // 非默认输入：dia 80（默认 62）/h 150（120）；本页输入为 renderParams 动态渲染
  "slug": "food-processing/filling-volume",
  "inputs": { "dia": "80", "h": "150" },
  "expect": ["754.0"],
  "ref": "V = π×(80/2/10)²×(150/10) = π×16×15 = 753.98 → 754.0 mL（默认 62/120 → 362.3）"
},
{
  // 非默认输入：A 2（默认 1）/dP 200（100）/t 60（30）
  "slug": "food-processing/filtration-rate",
  "inputs": { "A": "2", "dP": "200", "mu": "1.0", "alpha": "1e11", "c": "20", "Rm": "1e10", "t": "60" },
  "expect": ["1687.09"],
  "ref": "a=1250、b=25；V=(−25+√(25²+4×1250×3600))/(2×1250)=1.687086 m³ → 1687.09 L（默认 A=1/dP=100/t=30 → 419.5）"
},
{
  // 非默认输入：w0 600（默认 500）/w1 540（475）/cycles 3（1）/baseLoss 6（5）/incRate 0.2（0.15）
  "slug": "food-processing/freeze-thaw-loss",
  "inputs": { "w0": "600", "w1": "540", "cycles": "3", "baseLoss": "6", "incRate": "0.2" },
  "expect": ["10.00%"],
  "ref": "实际失水率 =(600−540)/600×100% = 10.00%（默认 25/500 → 5.00%）"
},
{
  // 非默认输入：P0 25（20）/d0 2.0（1.5）/P 60（40）/b 0.5（0.6）/N 2（1）
  "slug": "food-processing/homogenization-pressure",
  "inputs": { "P0": "25", "d0": "2.0", "P": "60", "b": "0.5", "N": "2" },
  "expect": ["1.205"],
  "ref": "d = 2.0×(60/25)^(−0.5)×2^(−0.1) = 1.204540 → 1.205 μm（默认 40/20 → 0.990）"
},
{
  // 非默认输入：w0 150（默认 100）/m0 75（70）/w1 90（55）/m1 30（40）/k 0.5（0.65）
  "slug": "food-processing/oil-absorption-rate",
  "inputs": { "w0": "150", "m0": "75", "w1": "90", "m1": "30", "k": "0.5" },
  "expect": ["28.5%"],
  "ref": "水分蒸发 = 112.5−27 = 85.5 g → 吸油 = 0.5×85.5 = 42.75 g → 吸油率 = 42.75/150×100% = 28.5%（默认 31.2%）"
},
{
  // 非默认输入：vol 20（默认 10）/ph0 8.0（7.0）/ph1 5.0（4.5）/conc 2（1）；agent 保持 citric 默认
  "slug": "food-processing/ph-adjustment",
  "inputs": { "vol": "20", "ph0": "8.0", "ph1": "5.0", "conc": "2" },
  "expect": ["0.039g"],
  "ref": "dH=(10⁻⁵−10⁻⁸)×20=1.998e−4 mol；α=10^(5−3.13)/(1+10^(5−3.13))=0.98669；mol=2.02495e−4 → 质量 = 2.02495e−4×192.12 = 0.038903 → 0.039 g（默认 4.5/pH7 → 0.063 g）"
},
{
  // 非默认输入：d 80（默认 50）/Tf −2（−1.5）/Tinf −40（−35）/h 60（50）/L 250（230）/rho 1050（1000）/k 1.2（1.5）
  "slug": "food-processing/quick-freeze-time",
  "inputs": { "d": "80", "Tf": "-2", "Tinf": "-40", "h": "60", "L": "250", "rho": "1050", "k": "1.2" },
  "expect": ["153.5"],
  "ref": "Plank（平板 P=0.5/R=0.125）：t=(1050×250000/38)×(0.5×0.08/60+0.125×0.0064/1.2)=9210.53 s = 153.51 → 153.5 min（默认 81.0）"
},
{
  // 非默认输入：vol 1000（默认 500）/pvol 700（400）/o2init 1（2）/otr 30（20）/area 500（300）/days 90（180）
  "slug": "food-processing/residual-oxygen",
  "inputs": { "vol": "1000", "pvol": "700", "o2init": "1", "otr": "30", "area": "500", "days": "90" },
  "expect": ["10.00%"],
  "ref": "顶空 = 300 mL；初氧 = 3 mL；渗入 = 30×0.05×90×20/100 = 27 mL；终浓度 = 30/300×100% = 10.00%（默认 22.52 截顶 21.00%）"
},
{
  // 非默认输入：Tt 45（默认 37）/Ts 20（25）/thetaT 45（30）/Q10 3（2）
  "slug": "food-processing/shelf-life-aslt",
  "inputs": { "Tt": "45", "Ts": "20", "thetaT": "45", "Q10": "3" },
  "expect": ["701.5"],
  "ref": "θ_s = 45×3^((45−20)/10) = 45×15.588457 = 701.48 → 701.5 天（默认 30×2^1.2 = 68.9）"
},
{
  // 非默认输入：vol 4（默认 2）/wood 500（300）/smokeRate 6（5）/phenolRatio 10（8）/t 90（120）/vent 4（3）/temp 80（60）
  "slug": "food-processing/smoking-concentration",
  "inputs": { "vol": "4", "wood": "500", "smokeRate": "6", "phenolRatio": "10", "t": "90", "vent": "4", "temp": "80" },
  "expect": ["1458.33"],
  "ref": "产烟 2700 g 触木屑 70% 上限 = 350 g → 酚 35 g；产生速率 0.38889 g/min ÷ 通风 0.26667 m³/min = 1.45833 g/m³ → 1458.33 mg/m³（默认 1400）"
},
{
  // 非默认输入：feed 800（默认 500）/solid 45（40）/moist 3（4）/recovery 95（98）
  "slug": "food-processing/spray-drying",
  "inputs": { "feed": "800", "solid": "45", "moist": "3", "recovery": "95" },
  "expect": ["352.6"],
  "ref": "干物质 = 360 → 理论出粉 = 360/0.97 = 371.134 → 实际 = 371.134×0.95 = 352.577 → 352.6 kg/h（默认 204.2）"
},
{
  // 非默认输入：T 110（默认 121.1）/t 40（15）；本页输入为 renderParams 动态渲染且未绑 oninput，
  // 注入后由框架兜底调用 calc() 命中（via=calc），判别力仍有效（换回默认 T=121.1/t=15 得 F=15）
  "slug": "food-processing/sterilization-f-value",
  "inputs": { "T": "110", "Tref": "121.1", "Z": "10", "t": "40" },
  "expect": ["3.105"],
  "ref": "L = 10^((110−121.1)/10) = 0.077625 → F = 0.077625×40 = 3.1050 → 3.105 min（默认 1×15 = 15.000）"
},
{
  // 非默认输入：kw = 诱惑红（默认空 → 全表 36 条）
  "slug": "food-processing/additive-limit-lookup",
  "inputs": { "kw": "诱惑红" },
  "expect": ["共 1 条结果"],
  "ref": "搜索「诱惑红」→ 命中 1 条（默认空关键词渲染全表 36 条）"
},
  // 注：food-processing/estimate-analysis-1 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  // 页面输入为动态渲染的行内 input（无 id，无法按 id 注入）→ 保持 no_inputs；
  // 断言默认态真实值（勿依赖兜底副作用：delIn/delOut 被无参调用会删行把 88.89% 变成 87.50%）
  "slug": "food-processing/material-balance",
  "inputs": {},
  "expect": ["88.89%"],
  "ref": "默认 ins 合计 180、outs 合计 160 → 得率 = 160/180×100% = 88.89%（源码字面量 100/50/30 与 150/10）"
},
{
  // 非默认输入：yield 1500（默认 1000）→ 页面唯一可注入的 id 输入
  "slug": "food-processing/recipe-cost-calculator",
  "inputs": { "yield": "1500" },
  "expect": ["0.0081"],
  "ref": "总成本 = 6×515.464/1000+8×150/1000+55×120/1000+12×105.263/1000 = ¥12.1559 → 每克 = 12.1559/1500 = 0.008104 → 0.0081（默认 1000 g → 0.0122；勿取兜底 delRow 删行后的 0.0060）"
},
{
  // 非默认输入：aw 0.62（默认 0.85）；awSlider 同步 0.62。
  // 注意不能断言「需防霉」——默认态(0.85)的 advice「部分酵母霉菌可生长，需防霉」也含该串（恒命中逃生项）
  "slug": "food-processing/water-activity",
  "inputs": { "aw": "0.62", "awSlider": "0.62" },
  "expect": ["较稳定"],
  "ref": "aw=0.62 落入 [0.6,0.7) → 稳定性等级「较稳定」（默认 0.85 → 「中度易腐」）"
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
  console.log("==== food-processing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
