#!/usr/bin node
"use strict";
const fs = require("fs");
const { runCase } = require("./verify_it_calc.js");
globalThis.__tbFs = fs;
const CASES = [
{
  "slug": "project/analysis-28",
  "inputs": {"sn0": ""},
  "clicks": ["calc();"],
  "expect": ["请填写每位干系人的名称"],
  "ref": "干系人名称必填：空名称必须阻止分级与策略，旧版只在 DOM 取名称时兜底，空名称会被替换成默认名继续出结论。"
},
{
  "slug": "project/analysis-28",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/project/analysis-28.html','utf8');var ok=h.indexOf('highList.push(ToolBox.escHtml(name)')>=0&&h.indexOf('ToolBox.escHtml(r[0])')>=0;document.getElementById('res').innerHTML=(ok?'SAFE':'UNSAFE');"],
  "expect": ["SAFE"],
  "ref": "名称转义：重点管理清单与 CSV 表格单元格都复用 ToolBox.escHtml，尖括号名称不得进入实际标签。"
},
{
  "slug": "project/assessor-risk-9",
  "inputs": {"rn1":"供应链中断","ro1":"采购经理","rs1":"处理中","rd1":"2026-12-30","p1":"5","i1":"5"},
  "clicks": ["calc();"],
  "expect": ["供应链中断", "采购经理", "处理中", "2026-12-30", "概率5×影响5"],
  "ref": "风险明细：当前明细必须逐项包含名称、责任人、行动状态、复评日期和应对策略，不得再导出截断历史。"
},
{
  "slug": "project/checker-12",
  "inputs": {"c1": "1"},
  "expect": ["尚未完成检查"],
  "ref": "默认未检查：只设置第 1 项时其余 9 项仍为空，必须提示未完成，不得给出优秀/良好。"
},
{
  "slug": "project/checker-12",
  "clicks": ["for(var i=1;i<=10;i++)document.getElementById('c'+i).value='2';document.getElementById('c1').value='1';calc();"],
  "expect": ["95%", "良好"],
  "ref": "完成全部检查后按实际满分评级：19/20=95%，应为良好而非默认满分优秀。"
},
{
  "slug": "project/checker-12",
  "clicks": ["for(var i=1;i<=10;i++)document.getElementById('c'+i).value='2';document.getElementById('c1').value='na';calc();"],
  "expect": ["18 / 18", "不适用（不计分）"],
  "ref": "不适用项从分母扣除：一项 N/A 后满分 18，应输出 18/18。"
},
{
  "slug": "project/checker-training-hr-1",
  "inputs": {"h2": "0"},
  "expect": ["尚未完成检查"],
  "ref": "HSE 默认未检查：只设置关键项 0 分时其余项为空，必须提示未完成而不是直接一票否决。"
},
{
  "slug": "project/checker-training-hr-1",
  "clicks": ["for(var i=1;i<=10;i++)document.getElementById('h'+i).value='2';document.getElementById('h2').value='0';calc();"],
  "expect": ["不合格", "触发一票否决规则"],
  "ref": "HSE 一票否决：其余 9 项满分、关键项第 2 项 0 分，最终评级必须不合格。"
},
{
  "slug": "project/checker-training-hr-1",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/project/checker-training-hr-1.html','utf8');var ok=h.indexOf('if(naCount===0&&!veto.length&&')>=0;document.getElementById('res').innerHTML=(ok?'NOVBAR':'VBAR');"],
  "expect": ["NOVBAR"],
  "ref": "否决时隐藏参考标尺：触发一票否决后不再渲染只按总分显示“优秀”的参考条，避免同屏矛盾。"
},
{
  "slug": "project/checker-training-hr-1",
  "clicks": ["for(var i=1;i<=10;i++)document.getElementById('h'+i).value='2';document.getElementById('h10').value='0';calc();"],
  "expect": ["HSE实施优秀（90%）"],
  "ref": "非关键项不回归：第 10 项 0 分、其余满分，90% 仍评优秀，不得误触发一票否决。"
},
{
  "slug": "project/manager-cost",
  "clicks": ["calcEVM();"],
  "expect": ["状态日已过 30 天", "剩余计划 60 天"],
  "ref": "完工日期以状态日期为基准：默认 30 天前开工、90 天计划，应显示已过 30 天、剩余 60 天，不再从今天叠加整个总工期。"
},
{
  "slug": "project/manager-cost",
  "clicks": ["updatePeriod(0,'ac','0');updatePeriod(1,'ac','0');updatePeriod(2,'ac','0');"],
  "expect": ["预计完工总成本：不可用", "CPI 无定义"],
  "ref": "AC 为零时 CPI/EAC/ETC/VAC 必须不可用，不得把 EAC 回退为 BAC 或输出伪预测。"
},
{
  "slug": "project/manager-cost",
  "clicks": ["updatePeriod(0,'pv','');"],
  "expect": ["第1期 PV 须填写非负数"],
  "ref": "周期空值拦截：直接清空第一期 PV 后必须报第 1 期 PV 缺失，不得沿用上一次有效数值继续计算。"
},
{
  "slug": "project/manager-cost",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/project/manager-cost.html','utf8');var ok=h.indexOf('累计 PV')>=0&&h.indexOf('累计 EV')>=0&&h.indexOf('累计 AC')>=0&&h.indexOf('剩余预测天数')>=0&&h.indexOf('汇总')>=0&&h.indexOf('成本偏差 CV')>=0;document.getElementById('kpiGrid').innerHTML=(ok?'EVMHEAD OK':'BAD');"],
  "expect": ["已过 60 天", "总工期 93 天"],
  "ref": "状态日期口径：开始 2026-01-01、状态 2026-03-02 为 60 天，剩余 30 天按 SPI 0.92 推 33 天，预测总工期 93 天（默认计划 90 天）。"
},
{
  "slug": "project/manager-cost",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/project/manager-cost.html','utf8');var ok=h.indexOf('累计 PV')>=0&&h.indexOf('累计 EV')>=0&&h.indexOf('累计 AC')>=0&&h.indexOf('剩余预测天数')>=0&&h.indexOf('汇总')>=0&&h.indexOf('成本偏差 CV')>=0;document.getElementById('kpiGrid').innerHTML=(ok?'EVMHEAD OK':'BAD');"],
  "expect": ["EVMHEAD OK"],
  "ref": "中文 CSV 表头：导出按页面语言生成中文表头、剩余预测天数与汇总行，旧版固定 Period/Cum PV/Summary。"
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
        console.log("❌ " + c.slug + "  " + (r.why || "no expect match") + "  [" + (c.ref || "") + "]");
        if (r.errs && r.errs.length) console.log("     errs: " + JSON.stringify(r.errs));
        if (r.sample) console.log("     got: " + String(r.sample).slice(0, 300));
      }
    } catch (e) {
      fails.push(c.slug);
      console.log("❌ " + c.slug + "  THROWN: " + ((e && e.message) ? e.message : String(e)));
    }
  }

  console.log("==== project calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
