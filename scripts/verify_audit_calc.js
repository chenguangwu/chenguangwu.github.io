#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs; // 供 clicks 内做源码形态判别（harness 点击串无 require）
const CASES = [
{
  "slug": "audit/npv-discount",
  "inputs": { "rate": "100", "init": "1" },
  "clicks": ["flows=[1e308,1e308];calc();document.getElementById('__tbProbe').textContent='NPVTOTAL '+(window.__npvBlocked?'BLOCKED':'VALID');"],
  "expect": ["NPVTOTAL BLOCKED"],
  "ref": "未折现现金流总额溢出时必须阻止回报率及明细导出。"
},
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
  "slug": "audit/ratio-analysis",
  "clicks": [
    "document.getElementById('curLiab').value='0';calc();var s=document.getElementById('solvency').innerHTML;document.getElementById('__tbProbe').textContent='RAZERO '+((s.indexOf('N/A')>=0&&s.indexOf('0.00: 1')===-1)?'OK':'BAD');"
  ],
  "expect": ["RAZERO OK"],
  "ref": "T-N12：流动负债 0 时分母无效，流动比率/速动比率不再显示 0.00:1「偏低」，改为 — + N/A；探针读取 #solvency 动态 HTML。默认 demo 流动负债 280000，不出现 N/A。"
},
{
  "slug": "audit/ratio-analysis",
  "clicks": [
    "['curAssets','inventory','curLiab','totalAssets','totalLiab','equity','revenue','cogs','netProfit'].forEach(function(k){document.getElementById(k).value='';});calc();var s=document.getElementById('summary').innerHTML;document.getElementById('__tbProbe').textContent='RAEMPTY '+((s.indexOf('有效指标不足')>=0&&s.indexOf('N/A')>=0)?'OK':'BAD');"
  ],
  "expect": ["RAEMPTY OK"],
  "ref": "T-N12：全部清空后 val() 返回 NaN，各比率不再当 0 评「良好」，综合区提示「有效指标不足，无法综合评价」并注明 N/A 不参与评分。默认 demo 五项有效，不命中。"
},
{
  "slug": "audit/ratio-analysis",
  "clicks": [
    "document.getElementById('curLiab').value='0';calc();var t=reportText();document.getElementById('__tbProbe').textContent='RACAP '+((t.indexOf('N/A（流动负债缺失或为 0）')>=0&&t.indexOf('流动比率: 2.43')===-1)?'OK':'BAD');"
  ],
  "expect": ["RACAP OK"],
  "ref": "T-N12：复制报告拆出 reportText() 并复用 calc() 的同一结果对象，流动负债 0 时输出「N/A（流动负债缺失或为 0）」，不再用 ||1 兜底成 680000.00 与页面卡片冲突。默认 demo 有流动负债，文本不含该串。"
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
    "rateStart": "5",
    "rateEnd": "20",
    "rateStep": "2"
  },
  "expect": [
    "13.00% -870.19 NPV 15.00%"
  ],
  "ref": "扫描步长判别：rateStart=5/rateEnd=20/rateStep=2 ⇒ 扫描表按 5/7/9… 跳行，「13.00% -870.19 NPV 15.00%」为步长 2 的相邻行序列（默认 0–30/1 是 13.00% …14.00%，不含本串）。原锚 12,315.00 是默认 demo 8% 行、撞默认态；改锚随 rateStep 变化的行序列。"
},
{
  "slug": "audit/irr-table",
  "inputs": {},
  "clicks": [
    "flows=[-5000,2000,3000];renderList();var s=__irr_tableSnap();document.getElementById('__tbProbe').textContent='IRRSNAP '+s.cf;"
  ],
  "expect": ["IRRSNAP -5000,2000,3000"],
  "ref": "T-N19（2026-11-16）：现金流输入由 renderList 动态生成且无 id，旧快照只含扫描参数，历史回放用「当前现金流」重算，记录结果不可复现。现 __irr_tableSnap 追加 cf = flows.join(',')，回放时优先还原 flows 再 renderList。默认现金流 -100000,25000,30000,35000,40000,30000 ⇒ 不命中该串。"
},
{
  "slug": "audit/irr-table",
  "inputs": {},
  "clicks": [
    "flows=[-1000,500];__irr_tableRender(['rateStart','cf'],'结果',false);var t=document.getElementById('irr_tableTable');document.getElementById('__tbProbe').textContent='IRRHIDE '+((t&&String(t.innerHTML||'').indexOf('cf')===-1)?'OK':'BAD');"
  ],
  "expect": ["IRRHIDE OK"],
  "ref": "T-N19 附带：cf 只用于回放，不出现在历史表列头（dispKeys 过滤 cf）；探针渲染一次后检查表内容不含 'cf'。"
},
{
  "slug": "audit/irr-table",
  "inputs": {
    "rateStart": "0",
    "rateEnd": "10000",
    "rateStep": "0.1"
  },
  "expect": ["扫描区间超过 2000 行"],
  "ref": "留存优化（2026-11-16）：扫描循环按 r+=step 浮点累加且无行数上限，10000/0.1 会生成 10 万行卡死页面。现限制 2000 行，超出时截止到第 2000 行并提示「请增大步长」。默认 0–30/1 ⇒ 31 行，不命中。"
},
{
  "slug": "audit/irr-table",
  "inputs": {},
  "clicks": [
    "flows=[-100,50];renderTable();"
  ],
  "expect": ["-50.0000%"],
  "ref": "T-N9：两期现金流 -100→50 的真实 IRR=-50%，旧实现二分区间 low=-0.99、high=1000（百分数）两端 NPV 同号直接返回 NaN，误报「请输入至少两期现金流」。新实现按 log10(1+r) 全区间扫描，主解 -50.0000%。默认 demo IRR≈12.638%，不命中。"
},
{
  "slug": "audit/irr-table",
  "inputs": {},
  "clicks": [
    "flows=[-100,200,-99.9999];var ir=calcIRR();document.getElementById('__tbProbe').textContent='IRR2 '+ir.ok+' '+ir.roots.map(function(x){return (x*100).toFixed(4)+'%';}).join(',');"
  ],
  "expect": ["IRR2 true -0.1000%,0.1000%"],
  "ref": "835 复核失败重做（相近根漏检）：现金流 [-100,200,-99.9999] 的真实 IRR 为 -0.1% 与 +0.1% 两根（代入 NPV≈0，中间 r=0 处 NPV≈+1e-4）。旧单级 2400 步在 r≈0 步长约 0.0054，两落入同一区间且两端同号 ⇒ 一个根都检不到；现每个外层区间再 8 等分细分，捕获双根。期望串含两个根且默认 demo（单根 12.638%）不命中 ⇒ 强判别。"
},
{
  "slug": "audit/irr-table",
  "inputs": {},
  "clicks": [
    "flows=[-100,5000000];renderTable();"
  ],
  "expect": ["4999900.0000%"],
  "ref": "T-N9：早期高回报 -100→5000000 的真实 IRR≈4,999,900%，旧区间上限 1000% 覆盖不到。新实现上限到 1e7%，可返回该根；默认 demo 不命中。"
},
{
  "slug": "audit/irr-table",
  "inputs": {},
  "clicks": [
    "flows=[-100,230,-132];renderTable();"
  ],
  "expect": ["10.0000%、20.0000%"],
  "ref": "T-N10：现金流 -100、230、-132 有两个 IRR（10%、20%），旧实现只做一次二分、两端同号返回 NaN，与扫描表高亮零点矛盾。新实现收集全部根并列出；默认 demo 只有单根 12.638%，不命中。"
},
{
  "slug": "audit/irr-table",
  "inputs": {},
  "clicks": [
    "flows=[0,0];renderTable();"
  ],
  "expect": ["请输入至少两期现金流（需有正有负）才能计算IRR"],
  "ref": "T-N9 区分提示：全零现金流既无正也无负，calcIRR 返回 reason=input，保留原「需有正有负」提示；若误用「区间内无解」文案本串失配。默认 demo 有正有负，不命中。"
},
{
  "slug": "audit/irr-table",
  "inputs": {
    "rateStart": "0",
    "rateEnd": "1",
    "rateStep": "1"
  },
  "clicks": [
    "flows=[-100,200,-100];renderTable();var t=document.getElementById('irrResult');document.getElementById('__tbProbe').textContent='IRREVEN '+((String(t.innerHTML).indexOf('0.0000%')>=0&&String(t.innerHTML).indexOf('共找到 1 个')>=0)?'OK':'BAD');"
  ],
  "expect": ["IRREVEN OK"],
  "ref": "803 复核失败重做：现金流 -100/200/-100 在 0% 处 NPV=0 为偶重根，全程不变号。旧实现只扫变号 ⇒ roots=[] 并提示「区间内无实数 IRR」。新实现对 |NPV| 采样局部极小做三分搜索（收敛阈值 scale×1e-10）补出该根，主解与列表均显示 0.0000%。默认 demo 12.638% 不命中。"
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
},
{
  "slug": "audit/irr-table",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/audit/irr-table.html','utf8');document.getElementById('__tbProbe').textContent='IRRFAQ '+(h.indexOf('页面会全部列出')<0&&h.indexOf('不保证穷尽全部根')>=0?'OK':'BAD');"],
  "expect": ["IRRFAQ OK"],
  "ref": "835绝对承诺移除：FAQ 旧句「页面会全部列出」与有限步长扫描的实现冲突；权威源改为「仅列出扫描命中的根，不保证穷尽全部根」。源码形态断言旧承诺消失且新限制出现，默认态不执行 clicks ⇒ 零逃生。"
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
