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
    "🤍 茉莉花 花前修剪 早春重剪"
  ],
  "ref": "顺序保持型筛选 ⇒ 锚过滤后跨条目相邻串（同 office/excel-formula-reference 口径）。currentFilter 是模块级 var、render() 是顶层函数，可直接赋值重渲；注意不可调 setFilter(filter,btn)（btn 为 undefined 时 btn.classList 抛错）。桂花已改为「花后至早春」，timing==='before' 只剩茉莉花 1 条 ⇒ 过滤态首张卡即茉莉花，旧跨条目串不再成立；改锚茉莉花自身「花前修剪 早春重剪」。全量默认态中间隔多张卡，仍可判别。"
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
},
{ slug:"gardening2/fertilizer-ppm", inputs:{targetPpm:"200",waterAmount:"1",nutrientPct:"200"}, clicks:["calc()"], expect:["养分含量须在 0–100%"], ref:"养分 200% 旧实现按 200% 求用量，得到半量误导；新实现拒绝 >100%。默认 20 不出现。" },
{ slug:"gardening2/fertilizer-ppm", clicks:["document.getElementById('mode').value='calcPpm';document.getElementById('nutrientPct').value='200';document.getElementById('targetPpm').value='1';document.getElementById('waterAmount').value='1';calc();"], expect:["养分含量须在 0–100%"], ref:"反算模式同样校验养分 ≤100%，旧实现只查 >0。" },
{ slug:"gardening2/pruning-time", inputs:{}, clicks:["var g=PLANTS.filter(function(x){return x.name==='桂花';})[0];document.getElementById('__tbProbe').textContent='GH '+g.timing+' '+g.timingText;"], expect:["GH after 花后至早春"], ref:"桂花从「花前修剪」改正为「花后至早春」，避开秋季花芽期；旧数据同时写「花前修剪（秋季前）」和「秋季花前不修剪」自相矛盾。" },
{ slug:"gardening2/lawn-height", clicks:["currentGrass=2;currentSeason='spring';renderGrass();renderHeight();"], expect:["5 cm 早熟禾","春季"], ref:"早熟禾春季留茬由 4 cm 改 5 cm，落入同页说明的 5–8 cm；旧值 4 cm 低于说明下限。" },
{ slug:"gardening2/lawn-height", clicks:["var n=document.querySelectorAll('#grassGrid button.grass-card').length;var p=document.querySelectorAll('#grassGrid button[aria-pressed]').length;document.getElementById('__tbProbe').textContent='BTN '+n+' '+p;"], expect:["BTN 8 8"], ref:"草种卡改为原生 button（可 Tab/Enter/空格），每张带 aria-pressed；旧实现为 div+onclick，键盘不可选。" },
{ slug:"gardening2/pest-control", clicks:["document.getElementById('pcCrop').value='果树';__pcCropNote();"], expect:["本页不判断某产品是否在该作物上登记"], ref:"新增作物选择只用于提醒核对登记范围，不据此给通用安全期；旧页面直接给固定药剂/间隔/采收期。" },
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = []
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
