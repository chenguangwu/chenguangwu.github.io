#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "gardening2/fertilizer-ppm",
  "inputs": {
    "targetPpm": "150",
    "waterAmount": "5",
    "nutrientPct": "12"
  },
  "clicks": ["calc()"],
  "expect": [
    "6.25 g"
  ],
  "ref": "养分需求=150 mg/L × 5 L=750 mg；肥料量=750/0.12=6250 mg=6.25 g。"
     + "原 expect「约滴数」是结果区静态标签（回退默认仍命中 ⇒ 逃生项），且 200/1/20 为默认态。"
},
{
  "slug": "gardening2/lawn-height",
  "clicks": [
    "currentSeason='winter';renderGrass();renderHeight();"
  ],
  "expect": [
    "2 cm 狗牙根（百慕大） · 冬季"
  ],
  "ref": "去默认化（原 expect「推荐2.5cm」＝默认春季态，注入失败仍命中 → 逃生项）：harness 将元素 click() 桩成空操作，故改直接置顶层全局 currentSeason='winter' 后调 renderGrass()/renderHeight()，heightDisplay 渲染冬季草种留茬「2 cm 狗牙根（百慕大） · 冬季 · 暖季型（休眠期）」；默认春季显示「2.5 cm ... · 春季」，注入失败即不命中。（getTip 在暖季型冬季分支报错但被 clicks 的 try/catch 吞掉，不影响 heightDisplay 已写入。）"
},
{
  "slug": "gardening2/pruning-time",
  "inputs": {},
  "clicks": [
    "currentFilter='before';render();"
  ],
  "expect": [
    "去除内膛枝。 🤍 茉莉花"
  ],
  "ref": "顺序保持型筛选 ⇒ 锚过滤后跨条目相邻串（同 office/excel-formula-reference 口径）。currentFilter 是模块级 var、render() 是顶层函数，可直接赋值重渲；注意不可调 setFilter(filter,btn)（btn 为 undefined 时 btn.classList 抛错）。全表 18 条中 timing==='before' 仅桂花(第8条)与茉莉花(第12条)，默认全量渲染中间隔茶花/杜鹃/海棠 3 条 ⇒ 边界串「去除内膛枝。 🤍 茉莉花」仅过滤态成立；单条目内容（如「花前修剪（秋季前）」）默认态必有，不可锚。"
},
{
  "slug": "gardening2/watering-frequency",
  "inputs": {
    "potSize": "0"
  },
  "expect": [
    "请输入大于 0 的盆器口径"
  ],
  "ref": "修复前 0/空口径被 `||15` 静默替换为 15 cm，仍输出 0.18 L；现拒绝"
},
{
  "slug": "gardening2/watering-frequency",
  "inputs": {
    "potSize": "23"
  },
  "expect": [
    "0.42"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening2/fertilizer-ppm",
  "clicks": ["document.getElementById('mode').value='calcPpm';document.getElementById('targetPpm').value='1';document.getElementById('waterAmount').value='1.5';document.getElementById('nutrientPct').value='20';calc();var lab=document.getElementById('targetPpmLabel');var inp=document.getElementById('targetPpm');var h=String(document.getElementById('result').innerHTML);var ok=!!lab&&lab.textContent==='实际肥料用量 (g)'&&inp.placeholder==='如 1'&&h.indexOf('133 ppm')>=0&&h.indexOf('用量 1g')>=0;document.getElementById('__tbProbe').textContent='REVPPM '+(ok?'OK':'BAD '+(lab?lab.textContent:'nolabel')+' ph='+inp.placeholder+' '+h.slice(0,120));"],
  "expect": ["REVPPM OK"],
  "ref": "第1090批 J8：反算模式把 targetPpm 输入框当克数用，旧版标签仍写「目标浓度 (ppm)」/占位「如 200」，用户按标签填 200 会得到 40000ppm。修复后切 calcPpm 时标签动态改「实际肥料用量 (g)」、占位「如 1」，且预设值 1g/1.5L/20% → ppm=1×0.2×1e6÷1.5÷1000=133、结果回显「用量 1.000g」。旧版 label 无 id ⇒ lab 为 null，哨兵必然 BAD。"
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

  console.log("==== gardening2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
