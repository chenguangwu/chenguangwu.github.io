#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "audit/npv-discount",
  "inputs": {},
  "clicks": ["for(var i=0;i<75;i++)addFlow();document.getElementById('__tbProbe').textContent='NPVCAP n='+flows.length+' cap='+(typeof __NPV_MAX_FLOWS!=='undefined'?__NPV_MAX_FLOWS:'NA');"],
  "expect": ["NPVCAP n=60 cap=60"],
  "ref": "复核失败重做·T-N7 1/2（添加期数上限）：重复调用 addFlow() 75 次，期数必须停在 60 而不是无限增长。修复后 NPVCAP n=60 cap=60；修复前 n=80 且无上限常量 ⇒ 真变红。默认态不执行 clicks、无探针串 ⇒ 零逃生。"
},
{
  "slug": "audit/npv-discount",
  "inputs": {},
  "clicks": ["__npvLS('cfCount','61');var ok=__npvRestoreFlows();document.getElementById('__tbProbe').textContent='NPVREST ok='+(ok?1:0)+' n='+flows.length;"],
  "expect": ["NPVREST ok=1 n=60"],
  "ref": "复核失败重做·T-N7 2/2（越界快照截断恢复）：用页面自身的 __npvLS 把 cfCount 写成 61 再调 __npvRestoreFlows()：越界值应截断到上限 60 并成功恢复，而不是整体拒绝退回默认 5 期。修复后 NPVREST ok=1 n=60；修复前 ok=0 n=5 ⇒ 真变红。默认态 localStorage 无该键、不执行 clicks ⇒ 零逃生。"
},{
  "slug": "audit/npv-discount",
  "inputs": { "rate": "0", "init": "1e308" },
  "clicks": ["try{flows=[-1e308,1e308];calc();}catch(e){}"],
  "expect": ["累计现值溢出"],
  "ref": "第五批 T-N6 复核重做：折现率 0、初始投资 1e308、两期现金流 -1e308/+1e308。修复前只检查最终 NPV（正负相消后仍有限），累计现值中途溢出成 -Infinity、明细显示 -- 却仍允许导出。现逐期检查折现因子/单期现值/现值合计/累计现值，任一非有限即 __npvBlock 清空结论/明细/图表并拦导出。默认态 rate 11% 无溢出提示 ⇒ 强判别。"
},
{
  "slug": "audit/ratio-analysis",
  "inputs": {
    "curAssets": "820000",
    "inventory": "260000",
    "curLiab": "410000",
    "totalAssets": "1800000",
    "totalLiab": "760000",
    "equity": "1040000",
    "revenue": "1500000",
    "cogs": "900000",
    "netProfit": "240000"
  },
  "expect": [
    "16.00%",
    "23.08%",
    "1.37: 1",
    "42.22%"
  ],
  "ref": "净利率=240000/1500000=16.00%；ROA=240000/1800000=13.33%；ROE=240000/1040000=23.08%；"
     + "速动比率=(820000−260000)/410000=1.3658→1.37；资产负债率=760000/1800000=42.22%；"
     + "流动比率=820000/410000=2.00；存货周转率=900000/260000=3.46 次。"
     + "原 expect「净利率」是指标卡标题（静态文本）；且默认态毛利率同为 40.00%（与注入态撞值）⇒ 一律不锚。"
     + "评级词「良好」与「10 / 10」两态同现，亦不锚。",
  },
{
  "slug": "audit/audit-sample",
  "inputs": {
    "reliance": "98",
    "tolerable": "5",
    "expected": "1",
    "popN": "5000",
    "tolerableErr": "50000",
    "expectedErr": "10000",
    "stdDev": "150",
    "varReliance": "95"
  },
  "expect": [
    "在98%的可信赖程度下"
  ],
  "ref": "auto-restore"
},
{
  "slug": "audit/depreciation-compare",
  "inputs": {
    "cost": "100003",
    "salvage": "5000",
    "life": "5"
  },
  "expect": [
    "95,003.00 应折旧总额"
  ],
  "ref": "独立复算：应折旧总额 = 原值 100,003 − 残值 5,000 = 95,003.00。⚠ 原 expect '100003' 为原值输入回显（零判别力），已改为应折旧总额（含千分位格式化，输入回显不可能命中）；默认态 0 ⇒ 0.00，不命中。"
},
{
  "slug": "audit/irr-table",
  "inputs": {
    "rateStart": "0",
    "rateEnd": "33",
    "rateStep": "1"
  },
  "expect": [
    "507.27"
  ],
  "ref": "auto-restore"
},
{
  "slug": "audit/npv-discount",
  "inputs": {
    "rate": "11",
    "init": "100000",
    "annuityAmt": "25000",
    "annuityN": "5"
  },
  "expect": [
    "615.67"
  ],
  "ref": "auto-restore"
},
{
  "slug": "audit/npv-discount",
  "inputs": {
    "rate": "-99",
    "init": "100000",
    "annuityAmt": "25000",
    "annuityN": "1000"
  },
  "radios": { "mode": "annuity" },
  "expect": [
    "折现因子或净现值溢出"
  ],
  "ref": "T-N6 复核失败修复：折现率 -99%、初始投资 10万、年金 2.5万、1000 期（等额年金模式），折现因子 1/0.01^(t+1) 溢出致 NPV 非有限；修复后必须阻断结论/明细/导出并提示，不得再输出 -- NPV 却仍给 24900.00% ROI 与千行明细。注入态与默认态(率 11%)该提示不命中 ⇒ 强判别。"
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

  console.log("==== audit calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
