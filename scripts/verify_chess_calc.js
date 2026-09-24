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
    "patternType": "overline",
    "stoneCount": "6",
    "liveCount": "0"
  },
  "expect": [
    "黑棋形成6连（超过五连），违反长连禁手规则。黑方判负"
  ],
  "ref": "非默认输入（默认 patternType 取首项 three_three / stoneCount=3 / liveCount=2）：切到 overline 分支且 stones=6 ≥ 6 ⇒ 落「长连禁手」子分支，专属文案「黑棋形成6连（超过五连），违反长连禁手规则。黑方判负。」；默认态为 three_three + live=2 ⇒ 渲染「三三禁手 / 黑棋一手同时形成2个活三…」（不含该串）。**注意**：等级词「长连禁手」在页面静态规则说明表里出现 6 次 ⇒ 零判别力，不可单独作锚点（已弃用原 expect「结合实际棋盘分析」—— 那是页脚常驻免责文案）。"
},
{
  "slug": "chess/xiangqi-endgame",
  "inputs": {},
  "expect": [
    "黑将5平6"
  ],
  "ref": "结构性不可注入（沿用 tcm-diagnosis/etiology-tree 口径）：页面无任何 input/select，内容由常量对象 `ENDGAMES` 经 renderEndgames() 一次性渲染进三个 tab 容器（`$('tab-one/two/classic').innerHTML`），交互只有 switchTab() 的 classList.toggle 与 toggleCard() 的 classList.toggle —— **两者都不写入任何被采集的字符串**，且 14 个残局的标题与全部步骤在初始渲染时已同时落盘 ⇒ 无论怎么点，可用文本集合完全相同、无任何随交互变化的输出。维持 no_inputs，断言初始化渲染中的棋谱串。"
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
  console.log("==== chess calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
