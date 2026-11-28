#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "procurement/analysis-cost",
  "inputs": {
    "Q": "1000",
    "oldP": "50",
    "newP": "42",
    "N": "12",
    "inv": "20000"
  },
  "expect": [
    "8,000.00",
    "16.00",
    "96,000.00",
    "76,000.00",
    "2.50"
  ],
  "ref": "采购节约：单次节约=(50-42)×1000=8,000.00；节约率=16.00%；年节约=8000×12=96,000.00；净年节约=96000-20000=76,000.00；回收期=20000/8000=2.50次（独立复算；默认组 单次节约=7,500.00/节约率=15.00%，注入失败即不命中）"
},
{
  "slug": "procurement/assessor-26",
  "inputs": {
    "capital": "750",
    "bizYears": "5",
    "revenue": "2000",
    "debtRatio": "45",
    "capacity": "120",
    "passRate": "98.5",
    "complaint": "0.5",
    "onTime": "96",
    "coopYears": "3"
  },
  "expect": ["准入评分（示例模型）", "74", "优选供应商（参考）", "阈值 85/70/60 仅为可配置示例"],
  "ref": "auto-restore"
},

{
  "slug": "procurement/rater-price",
  "inputs": {"wQuality":"40","wPrice":"35","wDelivery":"25"},
  "clicks": ["var D=[[98.5,100,96],[95,92,0],[99,110,92]];D.forEach(function(a,i){var g=document.querySelectorAll('#supplierRows input[data-field=passRate]')[i];var q=document.querySelectorAll('#supplierRows input[data-field=price]')[i];var d=document.querySelectorAll('#supplierRows input[data-field=onTime]')[i];if(g)g.value=a[0];if(q)q.value=a[1];if(d)d.value=a[2];});calc();"],
  "expect": ["报价须填大于 0 的数值", "已暂停排名与推荐"],
  "ref": "第1119批：报价 0 不参与比价，不得让最低价为 0 后仍输出排名与推荐。"
},
{
  "slug": "procurement/stats-on-time-1",
  "inputs": {"total":"100","ontime":"20","good":"20","both":"30"},
  "expect": ["交集不成立", "0–20"],
  "ref": "第1119批：总数100、准时20、合格20时交集只能是0–20；30 须拒绝，旧版会输出负的准时但不良率。"
},
{
  "slug": "procurement/stats-on-time-1",
  "inputs": {"total":"100","ontime":"20.5","good":"20","both":"10"},
  "expect": ["批次数须为非负整数"],
  "ref": "第1119批：批次数不得为小数。"
},
{
  "slug": "procurement/stats-on-time-qualified",
  "inputs": {"total":"100","ontime":"20","qualified":"20","both":"30"},
  "expect": ["交集不成立", "0–20"],
  "ref": "第1119批：实测交集超出可行范围须拒绝，不能当独立估算继续算。"
},
{
  "slug": "procurement/analysis-cost",
  "inputs": {"Q":"100","oldP":"100","newP":"110","N":"6","inv":"5000"},
  "expect": ["无法回收", "无正节约"],
  "ref": "第1119批：新单价高于原单价、且有投入时不得显示 0 次/0 年回收期。"
},
{
  "slug": "procurement/analysis-cost",
  "inputs": {"Q":"100","oldP":"100","newP":"80","N":"0","inv":"0"},
  "expect": ["无法按年计算"],
  "ref": "第1119批：年采购次数为 0 且有单次节约时不得除零或给 0 年回收期。"
},
{
  clicks: ["calc()"],
  "slug": "procurement/wuliu-yunshufangshi-yunfei-bidui",
  "inputs": {"v0":"500","v1":"200","roadRate":"0.5","railRate":"0.25"},
  "expect": ["50.00", "25.00", "0.5000 元/(t·km)", "0.2500 元/(t·km)"],
  "ref": "第1119批：500 km、200 kg、0.5/0.25 元每吨公里 ⇒ 公路 50 元、铁路 25 元；单位费率须与总运费分开显示。"
},
{
  "slug": "procurement/assessor-26",
  "inputs": {"capital":"750","bizYears":"5","revenue":"2000","debtRatio":"","capacity":"120","passRate":"98.5","complaint":"0.5","onTime":"96","coopYears":"3"},
  "expect": ["待评估", "debtRatio"],
  "ref": "第1119批：只清空资产负债率也必须待评估，不能当 0 获得低负债满分并输出准入建议。"
},
{
  "slug": "procurement/assessor-26",
  "inputs": {"capital":"750","bizYears":"5","revenue":"2000","debtRatio":"101","capacity":"120","passRate":"98.5","complaint":"0.5","onTime":"96","coopYears":"3"},
  "expect": ["须在 0–100%"],
  "ref": "第1119批：资产负债率超过 100% 须拒绝。"
},
{
  "slug": "procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi",
  "inputs": {"v0":"-1"},
  "expect": ["项目金额须填写 ≥0 的数值"],
  "ref": "第1119批：负金额不得进入方式对比或合规结论。"
},
{
  "slug": "procurement/eoq",
  "inputs": {
    "demand": "15000",
    "orderCost": "100",
    "holdCost": "8",
    "leadTime": "7"
  },
  "expect": [
    "612.37",
    "287.67"
  ],
  "ref": "EOQ=√(2×15000×100/8)=612.37；提前期 7 天、日均需求 15000/365=41.0959 ⇒ ROP=287.67 件（默认 demand 10000/LT 7 得 191.78，两串均失配）"
},
{
  "slug": "procurement/eoq",
  "inputs": {"demand":"365","orderCost":"100","holdCost":"8","leadTime":"4000"},
  "clicks": ["var h=String(document.getElementById('detailResult').innerHTML);document.getElementById('__tbProbe').textContent='EOLTMAX '+(h.indexOf('0 到 3650')>=0&&h.indexOf('3650 ×')<0?'OK':'BAD '+h.slice(0,60));"],
  "expect": ["EOLTMAX OK"],
  "ref": "586：LT=4000 旧版静默截为 3650 并按 ROP=10×3650=36500 计算；修复后字段级拒绝，提示 0–3650，不出 ROP。合法 LT=7 默认态不命中该提示串。"
},
{
  "slug": "procurement/eoq",
  "inputs": {"demand":"365","orderCost":"100","holdCost":"8","leadTime":""},
  "clicks": ["var h=String(document.getElementById('detailResult').innerHTML);document.getElementById('__tbProbe').textContent='EOLTEMPTY '+(h.indexOf('留空')>=0?'OK':'BAD '+h.slice(0,60));"],
  "expect": ["EOLTEMPTY OK"],
  "ref": "586：LT 留空旧版静默当 0、ROP=0 仍出结果；修复后提示留空不出 ROP。合法 LT=7 默认态不命中该提示串。"
},
{
  "slug": "procurement/rater-price",
  "inputs": {
    "wQuality": "60",
    "wPrice": "35",
    "wDelivery": "25"
  },
  "clicks": ["var D=[[98.5,100,96],[95,92,98],[99,110,92],[96,100,95]];D.forEach(function(a,i){var g=document.querySelectorAll('#supplierRows input[data-field=passRate]')[i];var q=document.querySelectorAll('#supplierRows input[data-field=price]')[i];var d=document.querySelectorAll('#supplierRows input[data-field=onTime]')[i];if(g)g.value=a[0];if(q)q.value=a[1];if(d)d.value=a[2];});calc();"],
  "expect": [
    "推荐供应商",
    "供应商A"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/stats-on-time-1",
  "inputs": {
    "total": "300",
    "ontime": "255",
    "good": "270",
    "both": "240"
  },
  "expect": [
    "准时率 85.00%",
    "联合合格率（准时且合格） 80.00%",
    "准时但不良率 5.00%",
    "未同时达标率（迟到或质量不良） 20.00%"
  ],
  "ref": "非默认输入+独立复算：准时率255/300=85.00%、联合合格率240/300=80.00%、准时不良率15/300=5.00%、未同时达标率60/300=20.00%（默认120/100/108/90 输出 83.33/75/8.33/25；expect 用「标签+数值」上下文串，规避 5.00%⊂25.00% 的子串假命中）。Z3 修复前标签为「未达标率（非准时且合格）」，易误读为「迟到且合格」子集；改为并集口径「未同时达标率（迟到或质量不良）」。"
},
{
  "slug": "procurement/stats-on-time-qualified",
  "inputs": {
    "total": "300",
    "ontime": "255",
    "qualified": "270"
  },
  "expect": [
    "85.00",
    "90.00",
    "76.50"
  ],
  "ref": "到货准时合格：总300/准时255/合格270 → 准时率85.00%、合格率90.00%、准时且合格(255×270/300²)76.50%（独立复算，非默认输入）"
},
{
  "slug": "procurement/supplier-score",
  "inputs": {
    "wQuality": "60",
    "wPrice": "25",
    "wDelivery": "20",
    "wService": "15"
  },
  "expect": [
    "建议合计100%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "procurement/supplier-score",
  "inputs": {
    "wQuality": "0",
    "wPrice": "0",
    "wDelivery": "0",
    "wService": "0"
  },
  "expect": [
    "权重合计必须大于 0"
  ],
  "ref": "修复前四权重全 0 兜底分母 100，仍给四家供应商 0 分排名；现拒绝"
},
{
  "slug": "procurement/supplier-score",
  "inputs": {
    "wQuality": "-5",
    "wPrice": "25",
    "wDelivery": "20",
    "wService": "15"
  },
  "expect": [
    "请填写 0–100 的权重"
  ],
  "ref": "修复前负权重参与归一化；现字段级拒绝"
},
{
  "slug": "procurement/wuliu-yunshufangshi-yunfei-bidui",
  "inputs": {
    "v0": "800",
    "v1": "300"
  },
  "expect": [
    "120.00 元",
    "60.00 元",
    "0.4000 元/(t·km)"
  ],
  "ref": "公路=800×300×0.0005=120.00元；铁路×0.00025=60.00；单位=800×0.0005=0.4000元/(t·km)（默认500/200→50.00/25.00/0.2500，注入失败即不命中）"
},
  {
    "slug": "procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi",
    "inputs": {
      "v0": "42",
      "v1": "42"
    },
    "expect": [
      "待核对事项",
      "项目金额（万元，仅记录）",
      "本页不输出“合规/不合规”"
    ],
    "ref": "第1119批：移除按金额判定法定程序；42 万元只作记录，输出三方式流程与核对清单。"
  },
{ slug:"procurement/assessor-26", inputs:{"capital":"","bizYears":"","revenue":"","debtRatio":"","capacity":"","passRate":"","complaint":"","onTime":"","coopYears":""}, expect:["待评估：请补全全部字段后再评分"], ref:"第1119批：全部字段留空须标待评估，不输出 0 分假结果，也不得把空当 0。" }
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

  console.log("==== procurement calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
