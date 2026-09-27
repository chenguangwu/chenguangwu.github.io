#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "museum/era-comparator",
  "inputs": {},
  "clicks": ["document.getElementById('era1').value='3';document.getElementById('era2').value='9';compare()"],
  "expect": [
    "时间跨度相差: 839 年",
    "秦朝 15 年 vs 唐朝 289 年 (差 274 年)",
    "比值 4.0 倍"
  ],
  "ref": "两个朝代 <select> 的 option 由 JS 按 ERAS 下标填充（静态无 option ⇒ clicks 赋值后调 compare()）：era1=3 秦朝(s=-221,dur=15,人口约2000万)、era2=9 唐朝(s=618,dur=289,人口约8000万) ⇒ 起始年差 |−221−618|=839、时长差 |15−289|=274、人口比 8000/2000=4.0（默认 清朝 vs 现代中国 = 305/192/3.5）。非默认输入+独立复算。"
},
{
  "slug": "museum/exhibit-spacing",
  "inputs": {
    "artWidth": "120",
    "artHeight": "100",
    "centerH": "150",
    "hAngle": "30",
    "vAngle": "15",
    "eyeH": "155",
    "viewers": "2",
    "shoulder": "60"
  },
  "expect": [
    "216.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/historical-calendar",
  "inputs": {
    "date-input": "2008-08-08"
  },
  "clicks": ["update()"],
  "expect": [
    "2008 年 8 月 8 日",
    "星期五",
    "戊子年",
    "属鼠"
  ],
  "ref": "注入 2008-08-08 ⇒ 公历 2008 年 8 月 8 日、星期五（datetime 独立复算一致）、干支 戊子年"
     + "（(2008−4)%10=4→戊、(2008−4)%12=0→子）、生肖 属鼠。"
     + "不锚「距今 N 天」—— harness 用固定时钟 FrozenDate，该值随基准日漂移（实测 5790）。"
     + "原 expect「undefined-NaN-undefined」是兜底阶段无参 selectDate() 的产物（y/m/d 全 undefined ⇒ 拼出该串），"
     + "它既非页面缺陷也零判别力（默认态即命中）。",
},
{
  "slug": "museum/lighting-lux",
  "inputs": {
    "lampCount": "7",
    "lumens": "500",
    "distance": "0.8",
    "beamAngle": "36",
    "utilCoef": "0.7",
    "area": "2",
    "trans": "92"
  },
  "expect": [
    "11452"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/showcase-monitor",
  "inputs": {
    "temp": "30",
    "rh": "55",
    "tempSwing": "2",
    "rhSwing": "5"
  },
  "expect": [
    "建议降温至"
  ],
  "ref": "auto-restore"
},
{
  "slug": "museum/timeline-viewer",
  "clicks": [
    "currentTheme='世界历史';renderTimeline();"
  ],
  "expect": [
    "前 3100 年 上下埃及统一"
  ],
  "ref": "去默认化（原 expect「2070」＝默认「中国历史」主题下夏朝建立 -2070 的渲染串，注入失败仍命中 → 逃生项）：clicks 置顶层全局 currentTheme='世界历史' 后调 renderTimeline()，timeline 渲染世界史首条「前 3100 年 上下埃及统一 政治 古埃及第一王朝建立」；默认中国历史显示「夏朝建立 ... -2070」，注入失败即不命中。"
},
{
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "20",
    "perExhibit": "60",
    "moveTime": "20",
    "introTime": "30",
    "available": "50"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "26分50秒 讲解总时长",
    "+23分10秒",
    "150 秒"
  ],
  "ref": "总时长 = 20×60 + (20−1)×20 + 30 = 1200+380+30 = 1610 秒 ⇒ fmtTime 26分50秒；可用 = 50×60 = 3000 秒 ⇒ 50分0秒；时间差 = +1390 秒 ⇒ +23分10秒（充裕）；每件可用 = floor(3000/20) = 150 秒。默认态（30 件/90 秒/移动 30/开场 60/可用 90 分钟）为 1时0分30秒 / +29分30秒 / 180 秒，三条全不命中。"
},
{
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "10",
    "perExhibit": "90",
    "moveTime": "10",
    "introTime": "20",
    "available": "15"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "略超时",
    "8089 秒",
    "减少讲解展品数至 8 件"
  ],
  "ref": "总时长 = 10×90 + 9×10 + 20 = 1010 秒 ⇒ 16分50秒；可用 = 15×60 = 900 秒 ⇒ 15分0秒；时间差 = −110 秒（≥−300 ⇒ 「略超时」档）；压缩建议：单件讲解 cutPer = floor((90×900 − 9×10 − 20)/10) = 8089 秒、展品数 = floor((900−20)/(90+10)) = 8 件。默认态为「时间充裕」，三条全不命中。"
},
{
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "40",
    "perExhibit": "120",
    "moveTime": "30",
    "introTime": "60",
    "available": "40"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "1时40分30秒 讲解总时长",
    "严重超时",
    "缩短单件讲解至 7169 秒"
  ],
  "ref": "总时长 = 40×120 + 39×30 + 60 = 4800+1170+60 = 6030 秒 ⇒ 1时40分30秒；可用 = 2400 秒 ⇒ 40分0秒；时间差 = −3630 秒（< −300 ⇒ 「严重超时」）；每件可用 = floor(2400/40) = 60 秒；cutPer = floor((120×2400 − 39×30 − 60)/40) = 7169 秒。默认态全不命中。"
},
{
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "1",
    "perExhibit": "50",
    "moveTime": "30",
    "introTime": "10",
    "available": "10"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "× 0 段 = 0 秒",
    "600 秒",
    "1分0秒 讲解总时长"
  ],
  "ref": "总时长 = 1×50 + 0（count>1 为假 ⇒ 移动 0 段）+ 10 = 60 秒 ⇒ 1分0秒；可用 = 600 秒 ⇒ 10分0秒；时间差 = +540 秒；每件可用 = floor(600/1) = 600 秒。表格里「移动时间 × 0 段 = 0 秒」是本例独有形态，默认态（29 段移动）不命中。"
},
{
  "slug": "museum/audio-guide-timer",
  "inputs": {
    "exhibitCount": "5",
    "perExhibit": "60",
    "moveTime": "10",
    "introTime": "20",
    "available": "0"
  },
  "clicks": [
    "calcQuick();"
  ],
  "expect": [
    "每件可用时长 0 秒",
    "缩短单件讲解至 0 秒",
    "至 -1 件"
  ],
  "ref": "可用 = 0 秒 ⇒ 每件可用时长 0 秒、`avail>0` 为假 ⇒ avgPer = 0；时间差 = −360 秒（< −300 ⇒ 严重超时）；cutPer = floor((60×0 − 4×10 − 20)/5) = −12 ⇒ Math.max(−12,0) = 0 秒；展品数 = floor((0−20)/(60+10)) = −1 件（负数，可用时间为 0 时的边界产物，非真实场景）。本条锚页面当前实际产物，页面修正负数值后须同步更新。"
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
  console.log("==== museum calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
