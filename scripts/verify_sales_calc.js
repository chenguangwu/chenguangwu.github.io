#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs;
globalThis.__tbRoot = process.cwd();
const path = require("path");
const COMMISSION_PATH = path.join(__dirname, "..", "tools", "sales", "commission-calculator.html");

// 558 复核失败：末档上限此前仍可编辑，但 getTiers() 无条件替换为 Infinity；
// 禁用末档输入并明确固定无穷，是唯一不产生「填了却不算」歧义的口径。
function commissionStaticChecks() {
  const src = fs.readFileSync(COMMISSION_PATH, "utf8");
  const targetSrc = fs.readFileSync(path.join(__dirname, "..", "tools", "sales", "target-breakdown.html"), "utf8");
  const funnelSrc = fs.readFileSync(path.join(__dirname, "..", "tools", "sales", "conversion-funnel.html"), "utf8");
  return [
    {
      name: "阶梯提成末档上限输入禁用（固定无穷）",
      ok: /t\.cap === Infinity\s*\?\s*'[^']*tier-cap[^']*disabled[^']*'\s*:/.test(src)
        && !/placeholder="上限\(元\)"[^']*disabled/.test(src)
        && /newLast\.querySelector\('\.tier-cap'\)\.disabled = true/.test(src)
        && /last\.querySelector\('\.tier-cap'\)\.disabled = true/.test(src),
    },
    {
      name: "目标分解改名同步刷新结果表",
      ok: targetSrc.includes("oninput=\"members['+i+'].name=this.value;calc()\"")
        && targetSrc.includes("'<strong>'+ToolBox.escHtml(String(c))+'</strong>'")
        && !targetSrc.includes("rows.push([__tbSt('合计','Total')"),
    },
    {
      name: "转化漏斗阶段名转义后写入 innerHTML",
      ok: funnelSrc.includes("ToolBox.escHtml(stages[i].name")
        && funnelSrc.includes("'<span>'+(stages[i].name||'—')+'</span>'")===false,
    },
  ];
}

const CASES = [
{
  "slug": "sales/commission-calc",
  "inputs": {
    "sales": "375000",
    "base": "0",
    "taxThreshold": "5000"
  },
  "expect": [ "22,500 元" ],
  "ref": "auto-restore"
},
{
  "slug": "sales/commission-calculator",
  "inputs": {
    "sales": "150000",
    "fixedRate": "5",
    "baseSalary": "5000",
    "threshold": "20000",
    "baseRate": "8",
    "teamSales": "500000",
    "teamRate": "6",
    "shareRatio": "0.3"
  },
  "expect": [ "7,500.00 计算：销售额" ],
  "ref": "auto-restore"
},
{
  "slug": "sales/conversion-funnel",
  "inputs": {
    "preset": "ecom"
  },
  "expect": [
    "50.00%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/cost-price-margin",
  "inputs": {
    "cost": "90",
    "price": "100",
    "margin": "40"
  },
  "expect": ["36.00 利润额（元）"],
  "ref": "独立复算：mode 默认 price（成本加成口径）：售价=90×1.4=126.00，利润额=36.00；售价口径利润率=36/126=28.571%→28.6%，加价率=36/90=40.0%。"
     + "Z2 修复前「利润率」行误输出加成率 40.0%（与加价率同值），全页无 28.6% ⇒ 强判别、零逃生。"
     + "对照表值（25%/42.9%/66.7%/100%）与默认态均不含 28.6%。",
},
{
  "slug": "sales/cost-price-margin",
  "inputs": {
    "mode": "cost",
    "cost": "100",
    "price": "125",
    "margin": "20"
  },
  "expect": [
    "16.7%"
  ],
  "ref": "独立复算：mode=cost：成本=125÷1.2=104.17，利润额=20.83；售价口径利润率=20.83/125=16.667%→16.7%，加价率=20.0%。"
     + "Z2 修复前该分支「利润率」行输出 20.0%（加价率同值），全页无 16.7% ⇒ 强判别。",
},
{
  "slug": "sales/moving-average",
  "inputs": {
    "window": "6",
    "periods": "3",
    "data": "120\n135\n128\n142\n150\n165\n170"
  },
  "expect": [
    "148"
  ],
  "ref": "auto-restore"
},
{
  // WMA 预测权重方向：最新值应拿最大权重。
  "slug": "sales/moving-average",
  "inputs": {
    "window": "3",
    "periods": "1",
    "data": "120\n130\n150\n190"
  },
  "clicks": [
    "setMethod('wma');calc();"
  ],
  "expect": [
    "预测 1 — 167"
  ],
  "ref": "WMA(3) 对最新 3 期 [130,150,190] 按 1/2/3 加权：130×1+150×2+190×3=1000，÷6=166.67 ⇒ 展示 167。旧预测分支把最旧值赋最大权重：(130×3+150×2+190×1)÷6=146.67 ⇒ 147，故「预测 1 — 167」可强判别。"
},
{
  "slug": "sales/moving-average",
  "inputs": { "window": "5", "periods": "2", "data": "1200\n1250\n1300\n1400" },
  "clicks": [
    "calc();document.getElementById('data').value='1500';calc();var t=document.getElementById('resultTable');document.getElementById('__tbProbe').textContent='MAONLY '+document.getElementById('forecastLbl').textContent+' table='+(t.innerHTML?t.innerHTML.length:0);"
  ],
  "expect": ["MAONLY 至少需要 2 期历史数据（当前 1 期） table=0"],
  "ref": "542 复核失败重做：先多期算出结果，再只留 1 期 ⇒ 结果标签改为「至少需要 2 期历史数据（当前 1 期）」且表格清空；旧实现 data.length<2 直接 return，旧结果与表格仍在 ⇒ 本串不命中。"
},
{
  "slug": "sales/moving-average",
  "inputs": { "window": "3", "periods": "1", "data": "100\n110\n120\n" },
  "clicks": [
    "document.getElementById('__tbProbe').textContent='MAN '+parseData().length+' '+JSON.stringify(parseData());"
  ],
  "expect": ["MAN 3 [100,110,120]"],
  "ref": "542 复核失败重做：split 后先滤空串再转数值，末尾换行不再生成 0 值第 4 期；旧实现 +'' = 0 ⇒ MAN 4 [100,110,120,0]，本串不命中。"
},
{
  "slug": "sales/price-calculator",
  "inputs": {
    "cost": "150",
    "fixedCost": "0",
    "markup": "40",
    "targetProfit": "20000",
    "volume": "500",
    "compPrice": "180",
    "deviation": "-5",
    "custValue": "300",
    "captureRate": "60"
  },
  "expect": [
    "210.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/sales-forecast",
  "inputs": {
    "paramN": "3",
    "forecastN": "3",
    "histData": "",
    "method": "wma"
  },
  "expect": [
    "219,333.33"
  ],
  "ref": "注入 histData 为空（页面回填默认 12 期样本）、method=wma、paramN=3、forecastN=3 ⇒ 加权移动平均（权重 1/2/3）下期预测 219,333.33；默认 ma 方法得 205,833.33，不命中。"
},
{
  "slug": "sales/stacked-discount",
  "inputs": {
    "price": "899"
  },
  "expect": [
    "819.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "sales/target-breakdown",
  "inputs": {
    "total": "1500"
  },
  "expect": [ "1,500.00 万元", "权重总和 80" ],
  "ref": "注入 total=1500 万元（默认 1000）⇒ 汇总显示「1,500.00 万元」；默认 4 名成员权重 25/20/25/10 合计 80，显示「权重总和 80」。两串均随金额变化，默认态不含 1,500.00。"
},
{
  "slug": "sales/target-breakdown",
  "clicks": ["globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){}},chart:{bar:function(){}}};members=[{name:'甲',weight:10},{name:'乙',weight:10},{name:'丙',weight:10}];document.getElementById('total').value='1000';document.getElementById('mode').value='avg';calc();var tbEl=null;var q=document.querySelector;document.querySelector=function(s){var e=q.call(document,s);if(s==='#tbkHidden tbody')tbEl=e;return e;};__tbkExport();document.querySelector=q;var h=String(tbEl&&tbEl.innerHTML);document.getElementById('__tbProbe').textContent='TB559 '+((h.indexOf('33.4%')>=0&&h.indexOf('33.3%')>=0&&h.indexOf('33.3%')!==h.lastIndexOf('33.3%')&&h.indexOf('100.0%')>=0)?'OK':'BAD:['+h+']');"],
  "expect": ["TB559 OK"],
  "ref": "559 复核失败重做：1000 均分 3 人 ⇒ 目标 333.34/333.33/333.33，占比尾差归最大项后为 33.4/33.3/33.3%。导出旧实现另按 target/total 重算，得到 33.3/33.3/33.3%，与主表不一致却仍写合计 100.0%。探针读导出表并要求同时出现 33.4% 与两个 33.3%（后者用首末索引不同判断）。默认态（4 人、权重模式）不产生该组合。"
},
{
  "slug": "sales/target-breakdown",
  "clicks": ["globalThis.TBKit={util:{isEn:function(){return false;}},chart:{bar:function(){}}};members=[{name:'甲',weight:-10},{name:'乙',weight:30}];document.getElementById('total').value='1000';document.getElementById('mode').value='weight';var c=0;TBKit.chart.bar=function(){c++;};calc();var t=String(document.getElementById('resultTable').innerHTML);document.getElementById('__tbProbe').textContent='TB559N '+((c===0&&t.indexOf('权重不能为负数')>=0)?'OK':'BAD:c='+c);"],
  "expect": ["TB559N OK"],
  "ref": "559 复核失败重做：权重 -10/30 时主表报「权重不能为负数」，但旧 __tbExtras 只校验合计 > 0（此处 20 > 0）⇒ 仍调用图表绘制负目标，且无效时不清除旧图。现图表复用同一完整校验（非负 + 合计 > 0）并清空画布；探针把 chart.bar 替换为计数桩，要求调用次数为 0 且主表错误提示存在。"
},

{
    "slug": "sales/commission-calculator",
    "inputs": {
      "sales": "250000",
      "fixedRate": "8"
    },
    "expect": [
      "应得提成 ¥20,000.00"
    ],
    "ref": "提成 = 250000 × 8% = ¥20,000.00。页面输出 '应得提成 ¥20,000.00'。默认态其他输入不产生 ¥20,000.00。"
  },
  {
    "slug": "sales/price-calculator",
    "inputs": {
      "cost": "100",
      "fixedCost": "0",
      "markup": "30",
      "targetProfit": "0",
      "volume": "1",
      "compPrice": "0",
      "deviation": "0",
      "custValue": "0",
      "captureRate": "0"
    },
    "expect": [
      "建议售价 ¥130.00"
    ],
    "ref": "售价 = 100 × (1 + 30%) = ¥130.00。页面输出 '建议售价 ¥130.00'。默认态其他输入不产生 ¥130.00。"
  },
  {
    "slug": "sales/conversion-funnel",
    "inputs": { "preset": "ecom" },
    "clicks": ["stages.forEach(function(s,i){if(i>0)s.count=0;});calc()"],
    "expect": [" · —"],
    "ref": "边界负例：漏斗上一阶段为 0 时转化率 0/0 无定义，旧实现 `count || 1` 把分母兜成 1，真机出现 3300%/40000% 这类放大值；现显示 —（不可计算）。默认各阶段人数为正、全部比率有限，不出现「 · —」。"
  },
  {
    "slug": "sales/conversion-funnel",
    "clicks": ["stages[0].count=0;calc()"],
    "expect": ["请填写首阶段人数后再计算漏斗转化率。"],
    "ref": "空态守卫（2026-11-05）：首阶段人数为 0 时旧实现仍渲染「0 → 0 · 共 N 个阶段」与整表 0 值漏斗，现只给填写提示并清空整体转化率框与明细表。⚠ 只有首阶段（分母）0 视为无数据，后续阶段 0 人（流失 100%）仍照常计算。注入 preset=ecom 用例断 50.00% ⇒ 两态互斥。页面阶段行为动态插入，无法按 id 注入，故用 clicks 置零。",
  },
  {
    "slug": "sales/conversion-funnel",
    "clicks": ["stages.forEach(function(s){s.count=0;});calc();var f=document.getElementById('funnel').innerHTML;document.getElementById('__tbProbe').textContent='F463SA '+stages.length+' '+((f.indexOf('请填写首阶段人数')<0&&f.indexOf('width:0%')>=0&&document.getElementById('overallBox').innerHTML.indexOf('—')>=0)?'OK':'BAD');"],
    "expect": ["F463SA 4 OK"],
    "ref": "第463批复核失败重做：0 是合法人数。原 calc() 把首阶段 0 一律当未填写，全零漏斗也被拒，无法展示记录要求的 0% 柱宽。修复后区分「全阶段均 0」（合法全零漏斗，展示 width:0%、整体转化率 —）与「首阶段 0 但后续为正」（分母为 0 却有下游，保留原填写提示）。协议串绑定 stages.length=4 且要求全零态出现 0% 柱宽、无填写提示、整体 —；判别器注入失败（回退旧守卫）时全零仍报填写提示 ⇒ 探针变 BAD。",
  },
  {
    "slug": "sales/commission-calculator",
    "inputs": { "sales": "120000" },
    "clicks": ["currentMode='team';document.getElementById('teamSales').value='-500000';calc()"],
    "expect": ["团队销售额不能为负数"],
    "ref": "12-M5：团队销售额 -500,000、费率 6%、份额 0.3 原先照算提成 ¥-9,000；现在明确拒绝并清空缓存。注入非默认销售额 120000，默认团队档不出现该文案。"
  },
  {
    "slug": "sales/stacked-discount",
    "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/'+\'tools/sales/stacked-discount.html\',\'utf8\');var i=h.indexOf(\'if(price<=0)\');var s=i>=0?h.slice(i,i+420):\'\';var ok=(s.match(/getElementById\\(\'detailTable\'\\).innerHTML=\'\'/g)||[]).length>=1&&s.indexOf(\'badRate\')>=0;document.getElementById(\'__tbProbe\').textContent=\'STKDCL \'+(ok?\'OK\':\'BAD\');})();"],
    "expect": ["STKDCL OK"],
    "ref": "第1344批 早退残留：stacked-discount 的 price<=0 与 badRate 两分支原只改 finalVal/finalLbl 不清 #detailTable，旧明细表残留；修复后两分支 return 前清空明细表。"
  },

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

  const stat = commissionStaticChecks();
  const staticFails = stat.filter((s) => !s.ok);
  for (const s of staticFails) console.log("❌ [static] " + s.name);

  console.log("==== sales calc " + pass + "/" + cases.length + " ====");
  if (staticFails.length) console.log("❌ static " + (stat.length - staticFails.length) + "/" + stat.length + " 未通过");
  if (fails.length || staticFails.length) process.exit(1);
}
if (require.main === module) main();
