#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  // 原为 all_default 弱用例（注入值全等于页面默认）+ expect「暂无计算记录」是 localStorage 占位常量（逃生项）。
  // 需氧量 = 面积×水深×666.67×溶氧提升×0.001×品种系数；所需功率 = 需氧量×1.5；台数 = ceil(功率/单台功率)。
  { slug: "aquaculture/area-power", inputs: {"area":"20","depth":"2.0","delta":"4","unitpw":"1.5"},
    expect: ["160.00 所需功率（kW）", "107 建议台数（台）", "8.00 每亩功率（kW/亩）"],
    ref: "20×2.0×666.67×4×0.001×1.0 = 106.6672 → 106.67 kg；×1.5 = 160.0008 → 160.00 kW；ceil(160.0008/1.5) = 107 台；160.0008/20 = 8.00004 → 8.00 kW/亩。默认（10/1.5/3/3）为 30.00 kg / 45.00 kW / 16 台 / 4.50 kW/亩，三串均失配。" },
  // 原为 all_default 弱用例 + expect「暂无计算记录」（localStorage 占位常量，逃生项）。
  // 存活率 = 100 − 运输时长×温度系数×密度权重×均重权重×0.5；权重：密度 max(d/100,0.3)、均重 clamp(w/100,0.5,2.0)。
  { slug: "aquaculture/density-7", inputs: {"hours":"12","temp":"26","density":"200","weight":"250"},
    expect: ["64.0% 预估存活率", "72.00 风险指数", "28 建议密度（kg/m³）"],
    ref: "温度 26℃ → 系数 1.5；密度 200 → 2.0；均重 250 → clamp(2.5, 0.5, 2.0) = 2.0；风险 = 12×1.5×2.0×2.0 = 72.00；存活率 = 100 − 72×0.5 = 64.0% → 高风险；建议密度 = 1000/(12×1.5×2.0) = 27.78 → 28。默认（6/20/150/100）= 10.80 / 94.6% / 139，三串均失配。【判别力注：风险等级词「高风险」不作 expect —— 属二值判读词，且默认/注入态同用等级词体系】" },
  // 原为 all_default 弱用例 + expect「暂无计算记录」（localStorage 占位常量，逃生项）。
  // 日投喂率 = baseRate(均重)×tempFactor(水温)×品种系数；日投喂量 = 率/100×存塘量；每次量 = 日量/投喂次数。
  { slug: "aquaculture/frequency-9", inputs: {"weight":"300","temp":"28","species":"1.2","biomass":"5000"},
    expect: ["2.90% 日投喂率", "145.20 日投喂量（kg）", "48.40 每次投喂量（kg）"],
    ref: "均重 300g → baseRate 2.2、feedTimes 3；水温 28℃ → 系数 1.1；品种「虾蟹」系数 1.2 ⇒ 率 = 2.2×1.1×1.2 = 2.904 → 2.90%；日量 = 2.904/100×5000 = 145.20 kg；每次 = 145.2/3 = 48.40 kg；每吨 = 29.04 kg。默认（50/22/1.0/1000）= 2.80% / 28.00 / 7.00，三串均失配。" },
  // 原为 all_default 弱用例 + expect「暂无计算记录」（localStorage 占位常量，逃生项）。
  // 交换率 = 流量×60/容积（次/h，要求 ≥1）；溶氧供给 = 流量×(目标−进水溶氧)×60/1000 g/h；需氧 = 鱼卵数×0.001 g/h。
  // 注入值刻意让「交换率不足」而「溶氧充足」⇒ 结论从默认的「条件达标 ✓」翻转为「需调整 ✗」（跨分支）。
  { slug: "aquaculture/fuhua-shuiliu-rongyang-tiaojian", inputs: {"vol":"400","flow":"4","target":"9","inflow":"5","eggs":"800"},
    expect: ["0.60 水体交换率（次/h）", "0.160 溶氧余额（g/h）", "交换率 偏低 要求 ≥1 次/h"],
    ref: "交换率 = 4×60/400 = 0.60 次/h < 1 ⇒ 偏低；供给 = 4×(9−5)×60/1000 = 0.960 g/h；需氧 = 800×0.001 = 0.800 g/h；余额 = 0.160 g/h ≥ 0 ⇒ 溶氧充足；综合「需调整 ✗」（默认 6/200/8/6/10 → 交换率 1.80 达标、余额 0.710、「条件达标 ✓」）。**注意**：断言串里各 span 标签被 stripTags 替换为空格，故「交换率 偏低」中间有空格。" },
  // 原为 all_default 弱用例 + expect「暂无计算记录」（localStorage 占位常量，逃生项）。
  // diff = 目标−当前；调节量 = diff×体积/1000 kg CaCO₃；供给型分支（diff>0）另给碳酸氢钠×0.84、石灰×0.56。
  // 注入值刻意做成 diff<0 ⇒ 落到「需降低」分支（默认是「需提升」分支，跨分支 + 跨数值）。
  { slug: "aquaculture/hardness-water-quality", inputs: {"cur":"120","target":"80","vol":"2500"},
    expect: ["40.0 需降低（mg/L）", "100.00 等效调节量（kg, CaCO₃）"],
    ref: "diff = 80−120 = −40 → 需降低 40.0 mg/L；调节量 = −40×2500/1000 = −100 → 取绝对值 100.00 kg。默认（30/100/1000）走「需提升」分支（70.0 / 70.00），两串均失配。" }
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try {
      const r = await runCase(c);
      if (r.ok) { pass++; }
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== aquaculture calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();