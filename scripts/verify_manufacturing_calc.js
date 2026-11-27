#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "manufacturing/capacity-planning", inputs: {"machines":"8","capacityPer":"250","shifts":"3","demand":"30000","workDays":"20"}, expect: ["理论月产能 120,000 件","日产能 6,000 件","产能利用率 25.0%"], ref: "月产能 8×250×20×3 = 120000、日产能 8×250×3 = 6000、利用率 30000/120000 = 25.0%（默认 5×200×22×2 = 44000、40.0%）；shifts 必须显式注入（harness 取首个 option=1，真机 selected=2）；本页仅有「计算」按钮绑定 ⇒ 命中通道为兜底 calc()（via=calc）" },
  { slug: "manufacturing/defect-rate", inputs: {"total":"5000","defects":"120","processes":"4"}, expect: ["不良率 (Defect Rate) 2.400%","滚动直通率 (RTY) - 4工序 90.74%","PPM (百万缺陷数) 24,000"], ref: "不良率 120/5000 = 2.400%、FTY 97.60%、RTY 0.976⁴ = 90.74%、PPM 24000、DPMO 6000（默认 0.500%/99.50%/97.52%/10000）；原 expect「建议加强质量控制」是页面常驻文案 ⇒ 逃生项（无 input 绑定，命中通道为兜底 calc()）" },
  { slug: "manufacturing/inventory-calculator", inputs: {"annualDemand":"18000","orderCost":"150","holdCost":"15","dailyDemand":"50","leadTime":"10","stdDev":"12","serviceLevel":"2.33"}, expect: ["EOQ 经济订货量 600 件","年订货次数 30.0 次","EOQ 最优总成本（不含安全库存） ¥9,000"], ref: "EOQ = √(2×18000×150/15) = 600、年订 18000/600 = 30.0 次、周期 365/30 ≈ 12 天、总成本 √(2DSH) = 9000（默认 EOQ 490、24.5 次、¥6,928）；serviceLevel 必须显式注入（harness 取首个 option=1.28，真机 selected=1.65）；原 expect 是标签片段 ⇒ 逃生项" },
  { slug: "manufacturing/production-efficiency", inputs: {"plannedTime":"","downtime":"","cycleTime":"","output":"","goodOutput":""}, clicks: ["calc()"], expect: ["请填写计划时间与节拍时间后再计算 OEE。"], ref: "空计划时间/节拍不得保留默认 87.5%/59.5% 的旧 OEE 结果；默认 500/60/25/500/475 不含该提示。" },
  { slug: "manufacturing/production-efficiency", inputs: {"plannedTime":"420","downtime":"90","cycleTime":"25","output":"600","goodOutput":"570"}, expect: ["可用率 (Availability) 78.6%","性能率 (Performance) 75.8%","56.5% OEE"], ref: "运行 420−90 = 330 → 可用率 78.6%（默认 87.5%）；理论产量 330×60/25 = 792 → 性能率 600/792 = 75.8%（默认 59.5%）；OEE = 0.785714×0.757576×0.95 = 56.5%（默认 49.5%）。**注意**：合格率默认 475/500 与注入 570/600 同为 95.0% ⇒ 「合格率 (Quality) 95.0%」是逃生项，不可作 expect。原 expect「世界级标准」是提示文案常驻串 ⇒ 同样不可用" },
  { slug: "manufacturing/quality-control", inputs: {"usl":"10.8","lsl":"9.4","mean":"10.05","stddev":"0.12","n":"40","sigmaOverall":"0.18"}, expect: ["CPK (综合能力指数) 1.806","CP (潜在能力) 1.944","PPK (长期能力) 1.296"], ref: "T = 1.4、CP = 1.4/0.72 = 1.944；CPU = 0.75/0.36 = 2.083、CPL = 0.65/0.36 = 1.806 → CPK = 1.806；PPK 改用长期标准差 0.18：1.4/(6×0.18) = 1.296（旧口径用 σ_LT≈0.120256 得 1.940，已废弃）；未填 sigmaOverall 时结果为「未计算（未填长期标准差）」" },
  {
    "slug": "manufacturing/capacity-planning",
    "inputs": {
      "machines": "10",
      "capacityPer": "300",
      "demand": "30000",
      "workDays": "20",
      "shifts": "2"
    },
    "expect": [
      "理论月产能 120,000 件 日产能 6,000 件 产能利用率 25.0%"
    ],
    "ref": "自动补强（B类零用例）：原注入 workDays=42 超出页面 1–31 合法域，页面正确走「每月工作日为 1–31 的整数」卫语句、不产出 148,176；已改为合法非默认 machines=10/capacityPer=300/shifts=2/workDays=20/demand=30000 ⇒ 月产能 10×300×20×2 = 120,000、日产能 10×300×2 = 6,000、利用率 30000/120000 = 25.0%（默认 5/200/22 组合不重合）。"
  },
  {
    "slug": "manufacturing/production-efficiency",
    "inputs": {
      "plannedTime": "480",
      "downtime": "30",
      "cycleTime": "60",
      "output": "400",
      "goodOutput": "380"
    },
    "expect": [
      "可用率 (Availability) 93.8% 停机损失 6.3%"
    ],
    "ref": "独立复算：runTime=480−30=450，可用率=450/480=93.8%、停机损失 6.3%；idealCount=450×60/60=450，性能率=400/450=88.9%（旧实现封顶 1.5 可让 OEE 超 100%）；合格率=380/400=95.0%；OEE=0.9375×0.8889×0.95=79.2%。默认 480/60/30/500/475 得可用率 87.5%/停机损失 12.5%，不命中。"
  },
  {
    "slug": "manufacturing/production-efficiency",
    "inputs": {
      "plannedTime": "60",
      "downtime": "60",
      "cycleTime": "30",
      "output": "500",
      "goodOutput": "475"
    },
    "expect": [
      "停机时间须小于计划时间（且不能为负）。"
    ],
    "ref": "DT=PT 时 runTime=0、availability=0、idealCount=0 ⇒ 旧代码 performance=min(0/0→NaN,1.5) 经字符串兜底显示「—」，但 OEE 无意义；新增 DT<PT 守卫后须提示并中止。默认 DT=60/PT=480 不命中。"
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
    "slug": "manufacturing/quality-control",
    "inputs": {
      "usl": "110",
      "lsl": "90",
      "mean": "105",
      "stddev": "3",
      "n": "100",
      "sigmaOverall": "4"
    },
    "expect": [
      "PPK (长期能力) 0.417"
    ],
    "ref": "独立复算：T=110−90=20，PPK=min((110−105)/(3×4), (105−90)/(3×4))=min(0.417,1.250)=0.417；旧实现把 PP=T/(6σ)=20/24=0.833 直接当作 PPK，故该串仅修复后命中 ⇒ 强判别。"
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
      "货量 年订货次数 4.6 次 订货周期约 80 天 周期平均库存（EOQ/2，不含安全库存） 5 件 安全库存（向上取整） 450 件 Z=1.65 × 42 × √42 = 449.12 件"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"annualDemand\":\"42\",\"orderCost\":\"42\",\"holdCost\":\"42\",\"dailyDemand\":\"42\",\"leadTime\":\"42\",\"stdDev\":\"42\",\"serviceLevel\":\"1.65\"}，输出区含「货量 … 周期平均库存（EOQ/2，不含安全库存） 5 件 安全库存（向上取整） 450 件 …」；SS=1.65×42×√42=449.12，向上取整450；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "manufacturing/inventory-calculator",
    "inputs": {
      "annualDemand": "1000",
      "orderCost": "0",
      "holdCost": "2",
      "dailyDemand": "10",
      "leadTime": "5",
      "stdDev": "2",
      "serviceLevel": "1.65"
    },
    "expect": [
      "是本计算的分母，不能为 0"
    ],
    "ref": "新增守卫：S=0 时旧代码 EOQ=0、年订货次数=∞、订货成本=0 并输出伪结果（Infinity 被替换成 —，周期 0 天）。桩内 __tbInputGuard 已把 orderCost 列为分母并先行拦截，页面自身 D/S/H≤0 守卫为第二道；默认订货成本非 0，不命中 ⇒ 强判别。"
  },
  { slug: "manufacturing/defect-rate", inputs: {"total":"1000","defects":"100","defectQty":"1200","processes":"2"}, expect: ["600,000"], ref: "多缺陷场景：缺陷数 1200 可大于投入 1000（旧实现 d>t 直接拦截）；DPMO=(1200/1000)×10⁶/2=600,000，PPM 仍按不良品 100/1000=100,000 ⇒ 强判别" },
  {
    "slug": "manufacturing/defect-rate",
    "inputs": {
      "total": "42",
      "defects": "42",
      "processes": "42"
    },
    "expect": [
      "量分析报告 投入 42 件 · 不良品 42 件 · 缺陷 42 个 · 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"total\":\"42\",\"defects\":\"42\",\"processes\":\"42\"}，输出区含「量分析报告 投入 42 件 · 不良 42 件 · 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  }

  ,
  { slug: "manufacturing/quality-control", clicks: ["document.getElementById('mean').value='';calc();"], expect: ["「样本平均值」不能为空"], ref: "均值留空不得按 0 计算；旧实现 +value||0 会把空均值当 0 并输出 CPK/良率。默认均值 10.0 不命中。" },
  { slug: "manufacturing/quality-control", inputs: {"usl":"0","lsl":"-1","mean":"-0.5","stddev":"0.1","n":"30"}, expect: ["CPK (综合能力指数) 1.667"], ref: "明确输入 0 与负数规格边界合法：T=1、CPU=0.5/0.3=1.667、CPL=0.5/0.3=1.667 ⇒ CPK=1.667。旧实现 +value||0 本身可算，但 0 校验缺失新分支须允许。" },
  { slug: "manufacturing/quality-control", clicks: ["cur='cp';renderTypes();calc();"], expect: ["CP 潜在能力（未扣除均值偏移）","不能用 CP 代替实际能力"], ref: "切换 CP 模式后输出重点改为 CP 与适用条件，不再是同一组 CPK 结果；旧实现仅改选中样式。" },
  { slug: "manufacturing/quality-control", inputs: {"sigmaOverall":""}, clicks: ["cur='ppk';renderTypes();calc();"], expect: ["PPK 长期能力（需填 σ_总体）","未计算（未填长期标准差）"], ref: "PPK 模式未填长期 σ 时明确不计算，不以短期 σ 近似；旧实现切换 PPK 后仍输出 CPK 全套。" },
  { slug: "manufacturing/quality-control", inputs: {"n":"2.5"}, expect: ["「样本数」须为整数"], ref: "样本数小数拒绝；旧实现仅提示 PPK 小样本、不校验整数。" },
  { slug: "manufacturing/capacity-planning", clicks: ["document.getElementById('demand').value='0';calc();"], expect: ["无订单/闲置","无订单：理论月产能"], ref: "需求 0 合法并显示闲置产能；旧实现 d<=0 直接报错。" },
  { slug: "manufacturing/capacity-planning", clicks: ["cur='bottleneck';renderModes();calc();"], expect: ["瓶颈工序（按月产能升序） 装配","缺口 14,720 件"], ref: "默认多工序表：车削2×180×2×22=15,840、铣削1×150×2×22=6,600、装配1×120×2×22=5,280；需求20,000 ⇒ 瓶颈装配、缺口14,720。旧实现称单工序即瓶颈、无多工序比较。" },
  { slug: "manufacturing/capacity-planning", clicks: ["document.getElementById('processTable').value='车削,2,abc,2';calc();"], expect: ["多工序产能表有误","第1行：单台班产能须大于 0"], ref: "多工序表逐行严格解析，非数字产能停止计算；旧实现无多工序表。" },
  { slug: "manufacturing/inventory-calculator", inputs: {"leadTime":"-5"}, expect: ["平均日需求、交货期与需求标准差须为非负有限数"], ref: "负交期不得进入 √L 计算；0 合法、负数拒绝。默认 7 不命中。" },
  { slug: "manufacturing/inventory-calculator", inputs: {"dailyDemand":"40","leadTime":"2","stdDev":"10","serviceLevel":"1.65"}, clicks: ["document.getElementById('roundMode').value='ceil';calc();"], expect: ["安全库存（向上取整） 24 件","23.33"], ref: "SS=1.65×10×√2=23.33；向上取整 24，四舍五入 23。默认交期7不命中。" },
  { slug: "manufacturing/production-efficiency", inputs: {"plannedTime":"480","downtime":"0","cycleTime":"60","output":"500","goodOutput":"480"}, expect: ["性能率原始比值 104.2% 超过 100%","截断前 OEE 为 100.0%"], ref: "理想 480 件、产出500 ⇒ 原始104.17%，封顶100%；可用100%、合格96% ⇒ 主OEE96.0%、截断前100.0%。旧实现静默截断无提示。" }

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

  console.log("==== manufacturing calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();