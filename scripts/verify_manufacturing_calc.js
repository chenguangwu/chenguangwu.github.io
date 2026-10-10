#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "manufacturing/capacity-planning", inputs: {"machines":"8","capacityPer":"250","shifts":"3","demand":"30000","workDays":"20"}, expect: ["理论月产能 120,000 件","日产能 6,000 件","产能利用率 25.0%"], ref: "月产能 8×250×20×3 = 120000、日产能 8×250×3 = 6000、利用率 30000/120000 = 25.0%（默认 5×200×22×2 = 44000、40.0%）；shifts 必须显式注入（harness 取首个 option=1，真机 selected=2）；本页仅有「计算」按钮绑定 ⇒ 命中通道为兜底 calc()（via=calc）" },
  { slug: "manufacturing/defect-rate", inputs: {"total":"5000","defects":"120","processes":"4"}, expect: ["不良率 (Defect Rate) 2.400%","滚动直通率 (RTY) - 4工序 90.74%","PPM (百万缺陷数) 24,000"], ref: "不良率 120/5000 = 2.400%、FTY 97.60%、RTY 0.976⁴ = 90.74%、PPM 24000、DPMO 6000（默认 0.500%/99.50%/97.52%/10000）；原 expect「建议加强质量控制」是页面常驻文案 ⇒ 逃生项（无 input 绑定，命中通道为兜底 calc()）" },
  { slug: "manufacturing/inventory-calculator", inputs: {"annualDemand":"18000","orderCost":"150","holdCost":"15","dailyDemand":"50","leadTime":"10","stdDev":"12","serviceLevel":"2.33"}, expect: ["EOQ 经济订货量 600 件","年订货次数 30.0 次","最小总库存成本 ¥9,000"], ref: "EOQ = √(2×18000×150/15) = 600、年订 18000/600 = 30.0 次、周期 365/30 ≈ 12 天、总成本 √(2DSH) = 9000（默认 EOQ 490、24.5 次、¥6,928）；serviceLevel 必须显式注入（harness 取首个 option=1.28，真机 selected=1.65）；原 expect 是标签片段 ⇒ 逃生项" },
  { slug: "manufacturing/production-efficiency", inputs: {"plannedTime":"420","downtime":"90","cycleTime":"25","output":"600","goodOutput":"570"}, expect: ["可用率 (Availability) 78.6%","性能率 (Performance) 75.8%","56.5% OEE"], ref: "运行 420−90 = 330 → 可用率 78.6%（默认 87.5%）；理论产量 330×60/25 = 792 → 性能率 600/792 = 75.8%（默认 59.5%）；OEE = 0.785714×0.757576×0.95 = 56.5%（默认 49.5%）。**注意**：合格率默认 475/500 与注入 570/600 同为 95.0% ⇒ 「合格率 (Quality) 95.0%」是逃生项，不可作 expect。原 expect「世界级标准」是提示文案常驻串 ⇒ 同样不可用" },
  { slug: "manufacturing/quality-control", inputs: {"usl":"10.8","lsl":"9.4","mean":"10.05","stddev":"0.12","n":"40"}, expect: ["CPK (综合能力指数) 1.806","CP (潜在能力) 1.944","PPK (长期能力) 1.940"], ref: "T = 1.4、CP = 1.4/0.72 = 1.944；CPU = 0.75/0.36 = 2.083、CPL = 0.65/0.36 = 1.806 → CPK = 1.806；σ_LT = 0.12×∛(1+1/156) = 0.120256 → PPK = 1.940（默认 CP 1.111/CPK 1.111/PPK 1.108）；原 expect「能力过剩」是判定标准表格常驻串 ⇒ 逃生项" },
  {
    "slug": "manufacturing/capacity-planning",
    "inputs": {
      "machines": "42",
      "capacityPer": "42",
      "demand": "42",
      "workDays": "42",
      "shifts": "2"
    },
    "expect": [
      "/月 理论月产能 148,176 件 日产能 3,528 件 产能利用率 0.0% ✅ 充足"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"machines\":\"42\",\"capacityPer\":\"42\",\"demand\":\"42\",\"workDays\":\"42\",\"shifts\":\"2\"}，输出区含「/月 理论月产能 148,176 件 日产能 3,528 件 产能利用率 0.0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "manufacturing/production-efficiency",
    "inputs": {
      "plannedTime": "42",
      "downtime": "42",
      "cycleTime": "42",
      "output": "42",
      "goodOutput": "42"
    },
    "expect": [
      "ability) 0.0% 停机损失 100.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"plannedTime\":\"42\",\"downtime\":\"42\",\"cycleTime\":\"42\",\"output\":\"42\",\"goodOutput\":\"42\"}，输出区含「ability) 0.0% 停机损失 100.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "manufacturing/quality-control",
    "inputs": {
      "usl": "42",
      "lsl": "42",
      "mean": "42",
      "stddev": "42",
      "n": "42"
    },
    "expect": [
      "移 PPK 长期\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"usl\":\"42\",\"lsl\":\"42\",\"mean\":\"42\",\"stddev\":\"42\",\"n\":\"42\"}，输出区含「移 PPK 长期\n42\n42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "manufacturing/inventory-calculator",
    "inputs": {
      "annualDemand": "42",
      "orderCost": "42",
      "holdCost": "42",
      "dailyDemand": "42",
      "leadTime": "42",
      "stdDev": "42",
      "serviceLevel": "1.65"
    },
    "expect": [
      "货量 年订货次数 4.6 次 订货周期约 80 天 平均库存 5 件 安全库存 449 件 Z=1.65 × 42 × √42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"annualDemand\":\"42\",\"orderCost\":\"42\",\"holdCost\":\"42\",\"dailyDemand\":\"42\",\"leadTime\":\"42\",\"stdDev\":\"42\",\"serviceLevel\":\"1.65\"}，输出区含「货量 年订货次数 4.6 次 订货周期约 80 天 平均库存 5 件 安全库存 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "manufacturing/defect-rate",
    "inputs": {
      "total": "42",
      "defects": "42",
      "processes": "42"
    },
    "expect": [
      "量分析报告 投入 42 件 · 不良 42 件 · 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"total\":\"42\",\"defects\":\"42\",\"processes\":\"42\"}，输出区含「量分析报告 投入 42 件 · 不良 42 件 · 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== manufacturing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();