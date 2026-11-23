#!/usr/bin node
"use strict";
const fs = require("fs");
const { runCase } = require("./verify_it_calc.js");
globalThis.__tbFs = fs;
const CASES = [
{
  "slug": "project/analysis-28",
  "inputs": {
    "sn'+idx+'": "'+ToolBox.escHtml(s.name)+'_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "project/analysis-28",
  "clicks": ["['A','B','C','D'].forEach(function(n,k){document.getElementById('sn'+k).value=n;});document.getElementById('sp0').value='2';document.getElementById('si0').value='5';document.getElementById('sp1').value='3';document.getElementById('si1').value='3';document.getElementById('sp2').value='2';document.getElementById('si2').value='1';document.getElementById('sp3').value='2';document.getElementById('si3').value='1';syncSh();calc();var t=String(document.getElementById('res').innerHTML);var okT=t.indexOf('B（关注度 9）')>=0&&t.indexOf('A（关注度 10）')<0&&t.indexOf('权力≥3 且利益≥3')>=0;document.getElementById('__tbProbe').textContent='STAKE '+(okT?'OK':'BAD');"],
  "expect": ["STAKE OK"],
  "ref": "象限判据必须统一为权力≥3且利益≥3：B(3,3) 关注度 9 应进重点管理清单，A(2,5) 关注度 10 不应进；旧实现 one 清单按≥10、正文按象限，会出现 9 进 10 不进的自相矛盾。"
},
{
  "slug": "project/analysis-28",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/project/analysis-28.html','utf8');var i=h.indexOf('function calc(){');var seg=i>=0?h.slice(i,i+260):'';var ok=seg.indexOf('shData.some')>=0&&seg.indexOf('String(s.name).trim()')>=0;document.getElementById('__tbProbe').textContent='SHNAME '+(ok?'OK':'BAD');"],
  "expect": ["SHNAME OK"],
  "ref": "第1369/1371批·通用数字空态守卫不适用修复：calc 先 syncSh，再以真实必填项 shData.name 判定，任一干系人名称为空即阻止分级/策略；旧版只查 number/date ⇒ 永不触发 ⇒ BAD。"
},
{
  "slug": "project/assessor-risk-9",
  "inputs": {
    "p1": "2"
  },
  "expect": ["2\n3\n3\n3\n3\n3\n3\n3\n3\n3\n最高风险值： 9 / 25 整体风险等级： 中风险 风险项 计算 风险值 等级 风险1 概率2×影响3 6分 中风险 风险2 概率3×影响3 9分 中风险 风险3 概率3×影响3 9分 中风险 风险4 概率3×影响3 9分 中风险 风险5 概率3×影响3 9分 中风险 风险1 6 风险2 9 风险3 9 风险4 9 风险5 9 所有风险项均在可控范围内，建议定期复评并持续监控。"],
  "ref": "auto-restore"
},
{
  "slug": "project/checker-12",
  "inputs": {
    "c1": "1"
  },
  "expect": [
    "95%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "project/checker-training-hr-1",
  "inputs": {
    "h1": "1"
  },
  "expect": [
    "95%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "project/checker-training-hr-1",
  "inputs": {
    "h2": "0"
  },
  "expect": [
    "评价等级： 不合格",
    "触发一票否决规则"
  ],
  "ref": "HSE 关键项一票否决：仅将第 2 项「特种作业持证」置 0，其余 9 项默认 2，总分 18、达标率 90%（按分数本应评优秀）。关键项为 1/2/3/4/5/9，任一为 0 必须降级为不合格。断言结果区出现『评价等级： 不合格』和『触发一票否决规则』；旧实现无关键项门槛，会输出『优秀』，本用例不命中。"
},
{
  "slug": "project/checker-training-hr-1",
  "inputs": {
    "h10": "0"
  },
  "expect": [
    "HSE实施优秀（90%）"
  ],
  "ref": "非关键项不回归：第 10 项「安全文化建设」不属于关键项（关键项为 1/2/3/4/5/9），置 0 后总分 18、达标率 90%，仍应评优秀。锚取页面提示原文『HSE实施优秀（90%）』；若把关键项门槛误扩大到全部 10 项，本用例会降级为不合格、不命中。"
},
{
  "slug": "project/manager-cost",
  "inputs": {
    "projName": "默认项目",
    "bac": "150000",
    "totalDays": "90"
  },
  "expect": [ "71,118 按当前进度效率" ],
  "ref": "auto-restore"
},
{
  "slug": "project/manager-cost",
  "inputs": { "bac": "150000", "totalDays": "0" },
  "clicks": ["calcEVM();var k=String(document.getElementById('kpiGrid').innerHTML);var f=String(document.getElementById('forecastBox').innerHTML);var ok=k.indexOf('请检查输入')>=0&&k.indexOf('计划总工期须为正整数')>=0&&f.indexOf('预计总工期')<0;document.getElementById('__tbProbe').textContent='EVM0 '+(ok?'OK':'BAD '+k.slice(0,140));"],
  "expect": ["EVM0 OK"],
  "ref": "第1093批 I7：totalDays=0 旧版 parseInt(0)||1 静默按 1 天预测、输入框仍显示 0；修复后统一 __evmValid() 前置拦截，显示字段级错误且不产出工期预测。哨兵同时锚错误串与预测区清空，旧版必红。"
},
{
  "slug": "project/manager-cost",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/project/manager-cost.html','utf8');var ok=h.indexOf('d.totalDays ?? 90')>=0&&h.indexOf('if(__evmValid().length)')>=0&&h.indexOf('parseInt(')<0&&h.indexOf('parseFloat(val) || 0')<0;document.getElementById('__tbProbe').textContent='EVMFIX '+(ok?'OK':'BAD');"],
  "expect": ["EVMFIX OK"],
  "ref": "第1093批 I7 源码形态：保存加载用 ?? 保留 0（旧 || 90 覆盖 0）、导出复用 __evmValid() 拒绝无效输入（旧裸写 ev/bac 得 Infinity%）、全页清除 parseInt(...)||1 与 parseFloat(val)||0 的静默替换。"
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

  console.log("==== project calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
