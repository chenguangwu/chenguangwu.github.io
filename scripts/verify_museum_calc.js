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
