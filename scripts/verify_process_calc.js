#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "process/cp-index",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "sigma": "0.01"
  },
  "expect": [
    "85.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/cp-index",
  "inputs": {
    "usl": "10",
    "lsl": "10.5",
    "sigma": "0.01"
  },
  "expect": [
    "USL 必须大于下规格限 LSL"
  ],
  "ref": "规格限颠倒：旧实现输出 Cp=-8.333 并正常展示公差带；现拦截。默认 10.05/9.95 合法，不命中。"
},
{
  "slug": "process/cp-index",
  "inputs": {
    "usl": "10.05",
    "lsl": "9.95",
    "sigma": "-0.01"
  },
  "expect": [
    "过程标准差 σ 必须大于 0"
  ],
  "ref": "负标准差：旧实现直接算出 Cp=-1.667；现拦截 σ≤0。"
},
{
  "slug": "process/cpk-index",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "mu": "10.0",
    "sigma": "0.01"
  },
  "expect": [
    "15.05"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "process/cpk-with-shift",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "nominal": "10.0",
    "shift": "0.02",
    "sigma": "0.01"
  },
  "expect": [
    "15.05"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "process/cpk-with-shift",
  "inputs": {
    "usl": "10.05",
    "lsl": "9.95",
    "nominal": "10.0",
    "shift": "0.02",
    "sigma": "0"
  },
  "expect": [
    "过程标准差 σ」是本计算的分母，不能为 0"
  ],
  "ref": "σ=0：分母守卫先行拦截并标红「过程标准差 σ」。默认 0.01 合法，不命中。"
},
{
  "slug": "process/cpk-with-shift",
  "inputs": {
    "usl": "10.05",
    "lsl": "9.95",
    "nominal": "10.0",
    "shift": "0.02",
    "sigma": "-0.01"
  },
  "expect": [
    "过程标准差 σ 必须大于 0"
  ],
  "ref": "负 σ：分母守卫只拦 0，旧实现直接算 Cpk=-1.667；现显式要求 σ>0。"
},
{
  clicks: ["calc()"],
  "slug": "process/defect-probability",
  "inputs": {
    "usl": "15.05",
    "mu": "10.0",
    "sigma": "0.01"
  },
  "expect": [ "低于双精度可表示范围" ],
  "ref": "z=505 远超双精度可表示范围：修复前以 toFixed(4) 显示 0.0000% 和 0.0 DPMO，把极小概率误报为零；现明确标注低于可表示范围，并非实际零。"
},
{
  "slug": "process/dpmo-calc",
  "inputs": {
    "def": "186",
    "units": "2000",
    "opp": "10"
  },
  "expect": [
    "9300.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/dpmo-calc",
  "inputs": {
    "def": "30000",
    "units": "2000",
    "opp": "10"
  },
  "expect": [
    "缺陷数不能超过总机会数"
  ],
  "ref": "缺陷数 30,000 > 总机会 20,000：旧实现算出 1,500,000 DPMO（>100%）；现按机会上界拦截。默认 186/20000 合法，不命中。"
},
{
  "slug": "process/dpmo-calc",
  "inputs": {
    "def": "-5",
    "units": "2000",
    "opp": "10"
  },
  "expect": [
    "缺陷数须为非负整数"
  ],
  "ref": "负缺陷数：旧实现输出 -250.0 DPMO；现要求非负整数。"
},
{
  "slug": "process/first-pass-yield",
  "inputs": {
    "good": "1440",
    "total": "1600"
  },
  "expect": [
    "90.00"
  ],
  "ref": "1440/1600=90.00%。判别器实测旧输入 1425/1500 与页面默认 950/1000 同为 95.00%（默认态命中），已换非默认比例；默认态不出现 90.00。"
},
{
  "slug": "process/first-pass-yield",
  "inputs": {
    "good": "1100",
    "total": "1000"
  },
  "expect": [
    "首次合格数不能大于投入数"
  ],
  "ref": "修复前 1100/1000 输出 110% 与 -100 不良；现按「首次合格数」字段拒绝"
},
{
  "slug": "process/pp-index",
  "inputs": {
    "usl": "10.05",
    "lsl": "9.95",
    "slt": "-0.015"
  },
  "expect": [
    "σ_lt 必须大于 0"
  ],
  "ref": "负标准差修复前得 Pp≈-1.111；现拒绝"
},
{
  "slug": "process/ppk-index",
  "inputs": {
    "usl": "10.05",
    "lsl": "9.95",
    "mu": "10.0",
    "slt": "-0.015"
  },
  "expect": [
    "σ_lt 必须大于 0"
  ],
  "ref": "负标准差修复前得 Ppk≈-1.111；现拒绝"
},
{
  clicks: ["calc()"],
  "slug": "process/defect-probability",
  "inputs": {
    "usl": "10.05",
    "mu": "10.0",
    "sigma": "-0.01"
  },
  "expect": [
    "σ 必须大于 0"
  ],
  "ref": "负标准差修复前 z=-5 得约 99.99997%；现拒绝"
},
{
  "slug": "process/measurement-uncertainty",
  "inputs": {
    "u1": "3.5",
    "u2": "0.3",
    "u3": "0.2"
  },
  "expect": [
    "3.5185"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/measurement-uncertainty",
  "inputs": {
    "u1": "-1",
    "u2": "0.3",
    "u3": "0.2"
  },
  "expect": [
    "不确定度分量不能为负值"
  ],
  "ref": "修复前 u1=-1 得合成值 1.0630 且照常输出；现拒绝"
},
{
  "slug": "process/measurement-uncertainty",
  "inputs": {
    "u1": "0",
    "u2": "0",
    "u3": "0"
  },
  "expect": [
    "至少一个不确定度分量应大于 0"
  ],
  "ref": "修复前三项清零仍输出 0 不确定度；现拒绝"
},
{
  "slug": "process/rolled-throughput-yield",
  "inputs": {
    "y1": "0",
    "y2": "0",
    "y3": "0"
  },
  "expect": [
    "0.00",
    "100.00"
  ],
  "ref": "三道工序 0% 是合法工况：RTY=0.00%、总不良率 100.00%；修复前被通用全零守卫误拒绝"
},
{
  "slug": "process/pp-index",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "slt": "0.015"
  },
  "expect": [
    "56.667"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/ppk-index",
  "inputs": {
    "usl": "15.05",
    "lsl": "9.95",
    "mu": "10.0",
    "slt": "0.015"
  },
  "expect": [ "56.667 Pp" ],
  "ref": "auto-restore"
},
{
  "slug": "process/rolled-throughput-yield",
  "inputs": {
    "y1": "97",
    "y2": "97",
    "y3": "99"
  },
  "expect": [
    "93.15"
  ],
  "ref": "修正（2026-11-05）：旧用例注入 y1=147%（不可能的良率）并期待 141.16%——把越界输入当成了正确输出。良率上限 100%，现改为 y1=97% ⇒ RTY=0.97×0.97×0.99=93.15%。"
},
{
  "slug": "process/rolled-throughput-yield",
  "inputs": { "y1": "95" },
  "expect": ["91.23"],
  "ref": "单字段注入：仅改工序1良率 95%（y2=97、y3=99 取默认）⇒ RTY=91.23%，默认 94.11% ⇒ 强判别。"
},
{
  "slug": "process/rolled-throughput-yield",
  "inputs": { "y1": "120" },
  "expect": ["每道工序的一次通过率须为 0–100%"],
  "ref": "越界防护：一次通过率 >100% 时不再输出 764.46% 这类伪结果，只提示并清空结果表；默认 98/97/99 不出现该提示。"
},
{
  "slug": "process/sigma-level",
  "inputs": {
    "dpmo": "9315"
  },
  "expect": [
    "2.353"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/sigma-level",
  "inputs": { "dpmo": "0" },
  "expect": [ "不能据此断言" ],
  "ref": "DPMO=0 时 y=1、invNorm(1) 无有限值：旧版错误显示「≥6σ 上限」；现明确说明不能断言总体零风险，并提示可填已检验机会数给 3/N 置信上界。"
},
{
  "slug": "process/tolerance-rss",
  "inputs": {
    "t1": "3.1",
    "t2": "0.15",
    "t3": "0.2"
  },
  "expect": [
    "3.110"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/tolerance-worst-case",
  "inputs": {
    "t1": "3.1",
    "t2": "0.15",
    "t3": "0.2"
  },
  "expect": [
    "3.450"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/tolerance-worst-case",
  "inputs": { "t1": "-0.2", "t2": "0.15", "t3": "0.2" },
  "expect": ["公差须为非负数"],
  "ref": "负公差拦截（685 批）：t₁=-0.2 时旧版得总公差 0.150（比单项还小），现应提示去掉负号；默认 0.1/0.15/0.2 不含该文案"
},
{
  "slug": "process/tolerance-rss",
  "inputs": { "t1": "-0.2", "t2": "0.15", "t3": "0.2" },
  "expect": ["公差须为非负数"],
  "ref": "负公差拦截（685 批）：旧版线性叠加 0.150 且 RSS 占比 213.44%，现应提示绝对值；默认态不含该文案"
},
{
  "slug": "process/xbar-control-limits",
  "inputs": {
    "mean": "75",
    "sigma": "2",
    "n": "5"
  },
  "expect": [
    "77.683"
  ],
  "ref": "auto-restore"
},
{
  "slug": "process/cp-index",
  "inputs": {
    "usl": "10.05",
    "lsl": "9.95",
    "sigma": "0.0001"
  },
  "clicks": ["var s=document.getElementById('sigma');var min=s.getAttribute('min');s.value='0.0001';calcTool();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='CPMIN '+(min==='0.0001'&&h.indexOf('166.667')>=0?'OK':'BAD min='+min);"],
  "expect": ["CPMIN OK"],
  "ref": "1054 复核重做：σ 输入除原有的 >0 计算守卫外，还须有表单下限 min=0.0001；边界值 0.0001 仍可算出 Cp=(10.05−9.95)/(6×0.0001)=166.667。旧版无 min 属性 ⇒ BAD；默认 σ=0.01 不含该探针。"
},
{
  "slug": "process/first-pass-yield",
  "inputs": { "good": "950.5", "total": "1000" },
  "expect": ["首次合格数须为非负整数"],
  "ref": "非整数件数：旧实现按 950.5 件照算 95.05%；现要求计数为非负整数，默认 950/1000 不命中。"
},
{
  clicks: ["calc()"],
  "slug": "process/defect-probability",
  "inputs": { "usl": "10.05", "mu": "10.0", "sigma": "0.01" },
  "expect": ["2.867e-5", "0.287"],
  "ref": "z=5 的极小尾概率：旧版 toFixed(4) 显示 0.0000%、DPMO 0.0；现以科学计数显示 2.867e-5%、DPMO 0.287，不再舍入为零。"
},
{
  "slug": "process/xbar-control-limits",
  "inputs": { "mean": "50", "sigma": "-2", "n": "5" },
  "expect": ["标准差 σ 须为有限非负值"],
  "ref": "负 σ：旧版算出 UCL=47.317、LCL=52.683（上下限颠倒）；现拒绝并清空主结果/明细，默认 σ=2 不命中。"
},
{
  "slug": "process/xbar-control-limits",
  "inputs": { "mean": "50", "sigma": "2", "n": "2.5" },
  "expect": ["子组大小 n 须为有限正整数"],
  "ref": "小数 n：旧版按 √2.5 计算；现要求正整数，默认 n=5 不命中。"
},
{
  "slug": "process/tolerance-rss",
  "inputs": { "t1": "0", "t2": "0", "t3": "0" },
  "expect": ["不适用（线性叠加为 0，0/0）"],
  "ref": "三项全零：旧版用 (sum||1) 把分母变 1，比例显示 0.00%；现标 0/0 不适用，两个总公差仍为 0.000。"
},
{
  "slug": "process/dpmo-calc",
  "inputs": { "def": "124", "units": "2000", "opp": "10.5" },
  "expect": ["5904.8", "21000"],
  "ref": "平均机会数：每单位 10.5 个机会（可为平均值），总机会=21000，DPMO=124/21000×1e6≈5904.8；默认 10 机会为 6200.0，强判别。"
},
{
  "slug": "process/dpmo-calc",
  "inputs": { "def": "1", "units": "1.5", "opp": "2" },
  "expect": ["单位数须为正整数"],
  "ref": "小数单位数：旧版按 1.5 件计算并输出总机会 3；现要求单位数为正整数。"
},
{
  "slug": "process/sigma-level",
  "inputs": { "dpmo": "0", "sampleN": "1000000" },
  "expect": ["3.00 DPMO", "95% 置信上界"],
  "ref": "零缺陷有限样本：填 1,000,000 机会后按 3/N 给 95% 上界≈3 DPMO，而不是「≥6σ 上限」；与无样本的提示分支互斥。"
},
{
  "slug": "process/rolled-throughput-yield",
  "inputs": { "y1": "98", "y2": "100", "y3": "99" },
  "expect": ["97.02", "100% 工序不降低 RTY"],
  "ref": "100% 工序：0.98×1×0.99=97.02%；用来纠正「工序越多 RTY 越低」的绝对说法。"
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

  console.log("==== process calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
