#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原为 all_default 弱用例：sell/cost 取页面默认 120/75，expect 是静态标签词「当前售价相对竞品均价」。
  "slug": "fire/analysis-cost-price-8",
  "inputs": {
    "sell": "88",
    "cost": "66",
    "data": "100,110,120"
  },
  "expect": [
    "¥22.00 单件毛利",
    "当前售价相对竞品均价 -20.00%"
  ],
  "ref": "毛利 = 88−66 = 22.00；毛利率 = 22/88×100 = 25.00%；竞品均价 = (100+110+120)/3 = 110.00；相对均价 = (88/110−1)×100 = −20.00%；88 < 100 ⇒ 「低于全部竞品」。默认态（120/75 + 默认竞品串）得 ¥45.00 与不同百分比，注入失败即不命中（textarea#data 亦可注入）。"
},
{
  // 原为 all_default 弱用例：expect「管损」是静态卡片文案片段。
  "slug": "fire/calc-water-pressure-hydrant",
  "inputs": {
    "staticP": "0.40",
    "elevation": "8",
    "nozzleP": "0.30",
    "lossP": "0.10"
  },
  "expect": [
    "0.478 MPa 所需入口压力",
    "-0.078 MPa 安全余量"
  ],
  "ref": "高程折算 = 8/102 = 0.0784 MPa；所需 = 0.0784+0.30+0.10 = 0.4784 → toFixed(3) 0.478；安全余量 = 0.40−0.4784 = −0.0784 → −0.078（结论同步翻转为「不足」）。默认 0.55/12/0.35/0.08 得 0.548 与 +0.002（「满足」），注入失败即不命中。"
},
{
  // 原为 all_default 弱用例：expect「出口能力」是静态标签词。
  "slug": "fire/estimate-time-flow",
  "inputs": {
    "people": "160",
    "width": "2.4",
    "flow": "1.5",
    "dist": "24",
    "speed": "1.2",
    "pre": "45"
  },
  "expect": [
    "109.4 s 总疏散时间",
    "出口能力 3.60 人/s"
  ],
  "ref": "行走 = 24/1.2 = 20.0 s；排队 = 160/(2.4×1.5) = 44.44 s；总 = 20+44.44+45 = 109.44 → 109.4 s；出口能力 = 2.4×1.5 = 3.60 人/s。默认 300/1.8/1.3/30/1/30 得 188.2 s、出口能力 2.34，注入失败即不命中。"
},
{
  // 原为 all_default 弱用例：expect「口数量」是静态文案片段（「出口数量」被切）。
  "slug": "fire/evacuation-time",
  "inputs": {
    "people": "200",
    "width": "2.0",
    "flow": "1.5",
    "dist": "20",
    "speed": "1.0",
    "pre": "60",
    "aset": "120"
  },
  "expect": [
    "RSET ≥ ASET，疏散不安全",
    "126.7s RSET 必需疏散时间"
  ],
  "ref": "tflow = 200/(2.0×1.5) = 66.67 s；ttravel = 20/1.0 = 20.0 s；RSET = 60 + 66.67 = 126.67 → 126.7 s；ASET 120 < RSET ⇒ 结论翻转为「RSET ≥ ASET，疏散不安全！」（默认态为「安全裕度 141.8s …疏散安全」）。注入失败即不命中。"
},
{
  // 原为 all_default 弱用例：expect「管网」是条形标签词。
  "slug": "fire/hydrant-pressure",
  "inputs": {
    "hgeo": "18",
    "hq": "12",
    "ld": "20",
    "q": "4",
    "lw": "60",
    "d": "80"
  },
  "expect": [
    "33.39 m 所需压力 H",
    "2.28 m 水带损失 Hd"
  ],
  "ref": "所需压力 H = Hgeo + Hq + Hd + Hw = 18 + 12 + 2.28 + 1.11 = 33.39 m（Hd 用水带直径/流量默认档位算）；水带损失 Hd = 2.28 m。默认 24/16/25/5/80/100 得 H 与 Hd 均不同，注入失败即不命中。"
},
{
  // 原为 all_default 弱用例：expect「降至危险高度」是静态标签词。
  "slug": "fire/smoke-spread",
  "inputs": {
    "hrr": "1500",
    "height": "4",
    "time": "90",
    "width": "3",
    "alpha": "0.02"
  },
  "expect": [
    "蔓延距离 138.9 m",
    "烟气层高度 2.26 m"
  ],
  "ref": "Heskestad 烟羽流：v_jet ≈ 1.54 m/s、蔓延距离 = v_jet×90 = 138.9 m；烟气层 = 4 − 0.012×1500^(1/3)×90^(2/3)/4^(1/3) = 2.26 m。默认 1000/3/120/2/0.01 得 189.0 m 与 0.94 m，注入失败即不命中。"
},
{
  "slug": "fire/detector-176",
  "inputs": {
    "f1": "2"
  },
  "expect": [
    "联动系统存在轻微问题"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire/detector-178",
  "inputs": {
    "cycle": "4"
  },
  "expect": [
    "缩短维保周期至1-2个月"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire/detector-44",
  "inputs": {
    "count": "15",
    "lastDate": "2024-01-01"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire/extinguisher-calc",
  "inputs": {
    "area": "1200"
  },
  "expect": [
    "1200"
  ],
  "ref": "auto-restore"
},
{
  "slug": "fire/response-drill",
  "inputs": {},
  "clicks": [
    "currentScenario=scenarios[0];currentOrder=[];currentStep=3;score=45;updateStats();"
  ],
  "expect": [
    "3/8"
  ],
  "ref": "updateStats() 把 currentStep + '/' + currentScenario.steps.length 写进 #progress；默认态（currentStep=0、currentScenario=null）不渲染该串。currentScenario 必须先显式赋 scenarios[0]，否则 updateStats() 里 null.steps 抛错。6 个场景步数不等，故只锚分母确定的 scenarios[0]（办公楼火灾，8 步）→「3/8」，规避 Math.random 选景偶发失败（旧锚「火灾」是 6 个场景名的公共子串，属默认态必命中的弱判别，已弃；旧锚「拨打119报警」仅 5/6 场景含）。"
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
  console.log("==== fire calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
