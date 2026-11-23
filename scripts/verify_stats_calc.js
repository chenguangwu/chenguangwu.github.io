#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
globalThis.__tbRoot = process.cwd();
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "stats/data-distribution",
  "inputs": {
    "bins": "6",
    "data": "5,8,12,15,18,21,24,27,30,33,36,39,42,45,48,51"
  },
  "clicks": ["calc()"],
  "expect": [
    "16 样本数 n",
    "454.00 总和 Σ",
    "28.375 均值 x̄"
  ],
  "ref": "n=16；Σ=5+8+12+…+51=454；均值=454/16=28.375；中位数=(27+30)/2=28.500；极差=51−5=46；"
     + "σ²=196.609、σ=14.022、CV=49.42%。bins=6 ⇒ 组距=(51−5)/6=7.67。"
     + "原 expect「0.1」是 alpha 输入回显（且默认态同样含该串）⇒ 零判别力，已换非默认数据与统计锚点。",
},
{
  "slug": "stats/regression-analysis",
  "inputs": {
    "pred-x": "17",
    "x-data": "1,2,3,4,5,6,7,8,9,10",
    "y-data": "2.1,3.9,6.2,7.8,10.2,11.9,14.1,15.8,18.3,19.7"
  },
  "expect": [
    "33.8467"
  ],
  "ref": "auto-restore"
},
{
  "slug": "stats/sample-size",
  "inputs": {
    "e": "3",
    "p": "0.5",
    "n": "0",
    "conf": "0.95"
  },
  "expect": [
    "1,068",
    "误差 ±3.00%"
  ],
  "ref": "原注入 e=5/p=0.5/n=0/conf=0.95 与页面默认 value/selected 全部相同 ⇒ 默认态即命中「z² = 3.842」，零判别力。改为非默认误差 e=3%：n₀ = 1.96²×0.5×0.5/0.03² = 3.8416×0.25/0.0009 = 1067.11 → ⌈1067.11⌉ = 1068；默认 e=5% 为 385，与本用例零交集。"
},
{
  "slug": "stats/statistical-tests",
  "inputs": {
    "one-mu": "30",
    "one-data": "12,15,18,22,25,28,30,32,35,38"
  },
  "expect": [
    "-1.6413"
  ],
  "ref": "默认样本 12…38：n=10、均值 25.5、s=8.6700、SE=2.7417；μ₀=30 ⇒ t=(25.5−30)/2.7417=−1.6413（页面 toFixed(4)）。改动 μ₀ 后由 input 事件即时重算（此前必须点按钮，直接改输入结果区不变）。μ₀ 默认 20 ⇒ t=2.0061，不命中；原用例 one-data 带 '_X' 且 expect 为输入回显（恒绿）已替换。"
},
{
  "slug": "stats/regression-analysis",
  "inputs": { "x-data": "1,2", "y-data": "3,5" },
  "expect": ["样本数至少为 3 组"],
  "ref": "12-M7：n=2 时旧实现 ssRes/(n−2)=0/0 得 NaN，标准误、t、区间全为 NaN 仍渲染；现在要求 ≥3 组并提示。"
},
{
  "slug": "stats/regression-analysis",
  "inputs": { "x-data": "1,2,3", "y-data": "2,4,6" },
  "clicks": ["document.getElementById('equation').textContent='TC='+tCrit95(18)"],
  "expect": ["TC=2.101"],
  "ref": "12-M7：t 临界值由固定 2.306（仅 df=8）改为按 df 查表；df=18（n=20）应为 2.101。默认 n=10 ⇒ df=8 ⇒ 2.306，不命中。"
},
{
  "slug": "stats/regression-analysis",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/' +'tools/stats/regression-analysis.html','utf8');var h=globalThis.__tbFs.readFileSync(process.cwd()+'/'+'tools/stats/regression-analysis.html','utf8');var i=h.indexOf('if(xs.length !== ys.length');var s=i>=0?h.slice(i,i+900):'';var ok=s.indexOf('model = null')>=0&&(s.match(/getElementById\\('result'\\).innerHTML=''/g)||[]).length>=2&&s.indexOf('clearRect')>=0;document.getElementById('__tbProbe').textContent='REGCLR '+(ok?'OK':'BAD');})();"],
  "expect": ["REGCLR OK"],
  "ref": "第1345批 regression-analysis 两早退(样本不足/sxx|syy<=0)原只改 #equation，不清 #result/canvas/model；改为两处同步清空并重置 model。"
},
{
  "slug": "stats/regression-analysis",
  "clicks": ["var hh=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/stats/regression-analysis.html','utf8');var ci=hh.indexOf('function calc(){');var cs=ci>=0?hh.slice(ci,ci+500):'';var pi=hh.indexOf('function predictVal(){');var ps=pi>=0?hh.slice(pi,pi+320):'';var ok=cs.indexOf('__numReq')<0&&cs.indexOf('pred-result')>=0&&ps.indexOf('__raw===')>=0&&ps.indexOf('请先输入 X 值后再预测')>=0;document.getElementById('__tbProbe').textContent='REGROPT '+(ok?'OK':'BAD');"],
  "expect": ["REGROPT OK"],
  "ref": "第1345批·预测 X 空值早退残留修复：预测输入改为独立可选项，calc 不再用 pred-x 做必填早退，并在拟合时清空上轮预测；predictVal 空值时单独提示。旧版 calc 首部 pred-x 必填 ⇒ BAD。"
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

  console.log("==== stats calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
