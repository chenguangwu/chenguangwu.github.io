#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "chess/bridge-scoring",
  "inputs": {
    "level": "5",
    "tricks": "11"
  },
  "expect": [
    "100 定约分",
    "300 奖金分",
    "+400 总分"
  ],
  "ref": "非默认输入（默认 level=3 / tricks=9，花色默认 curSuit='C' 梅花 ⇒ perTrick=20）：需要墩数 = 5+6 = 11，tricks=11 ⇒ 刚好完成（超墩 0）。定约分 = (5×20+0首墩) × 1（未加倍）= 100；≥100 ⇒ 成局奖金 300（无局）；超墩分 = 0；总分 = 100+300+0 = 400。默认态为 60 / 50 / +110（三串均不含）。注：加倍/有局两个 select 默认取首项（value 0 = 未加倍 / 无局），花色 `curSuit` 是页面顶层 var（默认 'C'），本用例不改动它。"
},
{
  "slug": "chess/elo-rating",
  "inputs": {
    "myRating": "2000",
    "oppRating": "1800",
    "kValue": "40",
    "games": "5"
  },
  "expect": [
    "+48.1 总分变化",
    "9.61 每局变化",
    "76.0% 预期胜率",
    "2048 新等级分"
  ],
  "ref": "非默认输入（默认 myRating=1500 / oppRating=1600 / kValue=20（option 带 selected）/ games=1；result select 首项 value=1 即「胜利」，本用例沿用默认）：期望得分 Ea = 1÷(1+10^((1800−2000)/400)) = 1÷(1+10^(−0.5)) = 0.759746；胜率 = 75.9746% ⇒ 76.0%；每局变化 = 40×(1−0.759746) = +9.61016 ⇒ +9.61；5 局总变化 = 48.0508 ⇒ +48.1；新等级分 = 2000+48.0508 = 2048.05 ⇒ 2048。默认态为 +12.8 / 12.80 / 36.0% / 1513（四串均不含）。"
},
{
  "slug": "chess/go-territory",
  "inputs": {
    "komi": "0.5",
    "blackTerritory": "60",
    "blackCaptures": "5",
    "whiteTerritory": "40",
    "whiteCaptures": "2"
  },
  "expect": [
    "65.0 黑方总目",
    "42.5 白方总目",
    "+22.5 目差",
    "领先 22.5 目"
  ],
  "ref": "非默认输入（默认 komi=6.5 / bT=50 / bC=3 / wT=48 / wC=5）：黑方总目 = 60+5 = 65.0；白方总目 = 40+2+0.5 = 42.5；目差 = 65 − 42.5 = +22.5 ⇒ 黑方胜、提示「领先 22.5 目」。默认态为 53.0 / 59.5 / −6.5（白方胜，提示文案不同，四串均不含）。注：`method` select 的两个分支代码相同（均为 bT+bC / wT+wC+komi）⇒ 改 method 无输出差异，不锚。"
},
{
  "slug": "chess/gomoku-forbidden",
  "inputs": {
    "boardInput": "000000000000000\n000000000000000\n000000000000000\n000000000000000\n000000000000000\n000000000000000\n000000000000000\n000001100000000\n000000010000000\n000000010000000\n000000000000000\n000000000000000\n000000000000000\n000000000000000\n000000000000000\njudge:H8"
  },
  "clicks": ["loadBoardInput()"],
  "expect": ["同时形成 2 个活三"],
  "ref": "粘贴 15 行局面 + judge:H8：F8/G8 与 H6/H7 已有黑，H8 落下后横向 F8-G8-H8、纵向 H6-H7-H8 均为可补成活四的活三，横竖各计 1 个 ⇒ 渲染「该点同时形成 2 个活三…构成三三禁手」。默认态 result 为空，且静态规则表只写「一手同时形成两个活三」，不含「同时形成 2 个活三」这一动态结果串。"
},
{
  "slug": "chess/gomoku-forbidden",
  "inputs": {},
  "clicks": ["loadPreset(1)"],
  "expect": ["长连禁手", "形成 6 连"],
  "ref": "预设「长连示例」：D8..H8 五连，待判 I8 补成六连 ⇒ 长连禁手分支（结果区「黑棋形成 6 连（≥6）…判长连禁手，黑方判负」）。注意「长连禁手」在静态规则说明表中出现多次，须同时锚定动态串「形成 6 连」才有判别力。"
},
{
  "slug": "chess/gomoku-forbidden",
  "inputs": {},
  "clicks": ["loadPreset(2)"],
  "expect": ["五连胜利"],
  "ref": "预设「五连胜利」：G8..J8 四连，待判 K8 补成恰好五连 ⇒ 五连胜利分支（「黑棋在 1 个方向形成恰好五连，为胜利条件」）。静态页面无「五连胜利」四字（正文写作「五连（恰好五连）为胜利」），故该锚点只在动态结果出现。"
}
,
{
  "slug": "chess/xiangqi-endgame",
  "inputs": {},
  "expect": [
    "成杀条件：双炮同线且前炮能借后炮作架"
  ],
  "ref": "结构性不可注入（沿用 tcm-diagnosis/etiology-tree 口径）：页面无任何 input/select，内容由常量对象 `ENDGAMES` 经 renderEndgames() 一次性渲染进三个 tab 容器（`$('tab-one/two/classic').innerHTML`），交互只有 switchTab() 的 classList.toggle 与 toggleCard() 的 classList.toggle —— **两者都不写入任何被采集的字符串**，15 个杀法卡片的标题、成杀条件与要点在初始渲染时已同时落盘 ⇒ 无论怎么点，可用文本集合完全相同、无任何随交互变化的输出。维持 no_inputs，断言首卡「重炮」的成杀条件（旧版伪着法「黑将5平6」已随页面重写删除）。"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else {
        fails.push(c.slug);
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match"));
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== chess calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
