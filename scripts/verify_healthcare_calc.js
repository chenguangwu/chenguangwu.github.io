#!/usr/bin/env node
/**
 * 第 23 道门禁：healthcare 分类计算正确性验证（35 个工具 / 35 个用例）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 用法: node scripts/verify_healthcare_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
globalThis.__tbFs = fs;
const path = require("path");

// 425 复核失败：指南正文曾套用通用统计模板，与三列收支汇总工具不符。
function analysisReportCostGuideChecks() {
  const read = (...parts) => fs.readFileSync(path.join(__dirname, "..", ...parts), "utf8");
  const guide = read("guides", "analysis-report-cost-guide.html");
  const tool = read("tools", "healthcare", "analysis-report-cost.html");
  const en = JSON.parse(read("i18n", "guides", "analysis-report-cost-guide.json")).map || {};
  const ldBlocks = [...guide.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)].map((m) => m[1]);
  const jsonLd = ldBlocks.find((b) => /"@type"\s*:\s*"FAQPage"/.test(b)) || "";
  const visibleFaq = [...guide.matchAll(/<dt>([^<]+)<\/dt>/g)].map((m) => m[1]);
  const ldFaq = [...jsonLd.matchAll(/"name":\s*"([^"]+)"/g)].map((m) => m[1]);
  const stale = ["均值 x̄", "方差 σ²", "质量月报", "方差用 n", "中位数 = 排序后"];
  return [
    {
      name: "财务指南已清除通用统计模板口径",
      ok: stale.every((s) => guide.indexOf(s) < 0 && !Object.keys(en).some((k) => k.indexOf(s) >= 0)),
    },
    {
      name: "财务指南正文按科室收支三列口径",
      ok: guide.indexOf("结余 = 收入 − 成本") >= 0
        && guide.indexOf("科室盈亏盘点") >= 0
        && guide.indexOf("收入为 0 的科室怎么处理？") >= 0
        && tool.indexOf("成本率") >= 0 && tool.indexOf("结余率") >= 0,
    },
    {
      name: "结构化 FAQ 与可见 FAQ 逐字一致",
      ok: ldFaq.length === visibleFaq.length && visibleFaq.length > 0
        && visibleFaq.every((q, i) => q === ldFaq[i]),
    },
    {
      name: "英文映射覆盖新正文且无旧统计键",
      ok: !!en["财务（成本/利润/报表）分析使用指南"]
        && !!en["：内科,100,70 与 外科,80,90 ⇒ 收入合计 180.00、成本合计 160.00、结余 +20.00、全院成本率 88.89%、结余率 +11.11%；结余最高为内科（+30.00），亏损科室 1 个（外科 −10.00）。若两科室均为 100,100，则结余 0.00、结余率 0.00%、亏损科室 0 个。"]
        && stale.every((s) => !Object.keys(en).some((k) => k.indexOf(s) >= 0)),
    },
  ];
}

const CASES = [
  // ---------- 儿科给药与剂量 ----------
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "80", dose: "15", conc: "32" },
    expect: ["单次药量： 31.3", "已按 1000 mg 封顶"],
    ref: "体重+单次双封顶：80 kg×15 mg/kg = 1200 mg，超过成人单次极量 1000 mg ⇒ 单次按 1000 mg 封顶 = 31.25 → 31.3 mL；日总量上限 min(80×60=4800, 4000)=4000 mg，故日上限 = floor(4000/1000)=4 次。修复前未做单次封顶，输出 37.5 mL/1200 mg 且日上限 3 次（超过成人单次极量）。默认 15kg/15mg/kg 为 7.0 mL，两锚均不命中。",
  },
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "20", dose: "10", conc: "32" },
    expect: ["单次药量： 6.3"],
    ref: "单次液量 = 20×10÷32 = 6.25 → 6.3 mL；日上限次数 = ⌊20×60÷32÷6.25⌋ = 6。⚠ 原锚裸「6.3」被 03-47 新增 refWeightBox 静态提示「16.3 kg」子串误伤（默认态命中→逃生项），改「单次药量： 6.3」派生串（默认 7.0 不含）。",
  },
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "20", dose: "5", conc: "32" },
    expect: ["日上限次： 6 次"],
    ref: "日上限次数 = min(floor(60/5)=12, 6) = 6：对乙酰氨基酚日总量 ≤60 mg/kg/d，同时受 q4h 给药间隔约束、24h 最多 6 次；若只按总量反推会得 12 次，与说明书给药间隔矛盾。默认 15kg/15mg/kg 为 4 次，零交集。",
  },
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "20", dose: "12", conc: "32" },
    expect: ["日上限次： 5 次"],
    ref: "每日上限按对乙酰氨基酚 60 mg/kg/d 反推：日总量上限 = 20×60 = 1200 mg，单次 20×12 = 240 mg ⇒ ⌊1200÷240⌋ = 5 次（旧实现按 75 mg/kg 得 ⌊1500÷240⌋ = 6 次，超过现行上限）。默认 15kg/15mg/kg 输出「日上限次：4 次」，与本用例零交集。",
  },
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "20", dose: "10", conc: "32", liver: "c" },
    expect: ["Child-Pugh C 级肝功能不全：对乙酰氨基酚以肝清除为主，应避免使用"],
    ref: "drug-dosing 模板铺开（03-47）：肝功能 C 级红字警示（对乙酰氨基酚肝清除为主）。默认 liver=normal 无该串 ⇒ 判别力成立。",
  },
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "15", dose: "80", conc: "32" },
    expect: ["单次剂量已超过每日上限（900 mg/天）"],
    ref: "D-N15（2026-11-16）：体重 15 kg、80 mg/kg ⇒ 单次 1200 mg 封顶 1000 mg，日上限 = min(15×60=900, 4000) = 900 mg ⇒ 单次已超日上限。旧实现输出「日上限次：0 次」而无任何超限提示；现给红字警示且不渲染 0 次。默认 15 kg/15 mg/kg ⇒ 225/900，不命中。",
  },
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "5", age: "0.17", dose: "15", conc: "32" },
    expect: ["3 月龄以下婴儿发热应及时就医"],
    ref: "D-N16（2026-11-16）：年龄输入曾只调用 updateWeightHint()，不触发 calc()，先按默认 4 岁算出剂量后再改年龄会保留旧结果。现 oninput 同时调用 calc()，0.17 岁（≈2 月龄）立即出现就医警示。默认 age=4 ⇒ 不命中。",
  },
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "20", dose: "10", conc: "32" },
    expect: ["当前体重偏差 23%"],
    ref: "WHO P50 中位体重核对：age 默认 4 岁/男 P50=16.3 kg，|20−16.3|÷16.3=22.7%→toFixed(0)=23%。默认 weight=15 偏差 8% ⇒ 随注入变化、零交集。",
  },
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "6", dose: "15", conc: "32", age: "0.15" },
    expect: ["3 月龄以下婴儿发热应及时就医，不建议自行使用退热药"],
    ref: "D-N16：age=0.15 岁 = 1.8 月龄，＜3 月龄 ⇒ 拒绝计算并提示就医；旧实现年龄只读不分支、仍输出 2.8 mL，默认 age=4 岁也不含该提示 ⇒ 零命中。",
  },
  {
    slug: "healthcare/antipyretic-dose",
    inputs: { weight: "6", dose: "15", conc: "32", age: "0.4" },
    expect: ["6 月龄及以下婴儿用药需医师评估，请遵医嘱。"],
    ref: "D-N16：age=0.4 岁 = 4.8 月龄 ⇒ 仍计算单次 2.8 mL，并追加 ≤6 月龄医师评估提示；默认 4 岁无该提示 ⇒ 强判别。",
  },
  {
    slug: "healthcare/healthcare",
    inputs: { adult_dose: "500", child_weight: "100", adult_weight: "70", max_factor: "1" },
    expect: ["受限剂量： 500.00"],
    ref: "按体重 = 500×(100÷70) = 714.29 mg；受限 = min(714.29, 500×1) = 500.00 mg（最大倍数 ≥1，成人剂量封顶生效）；比例 = 100÷70×100 = 142.86%。默认 500/20/70/2 → 受限 142.86，注入失败即不命中。",
  },
  {
    slug: "healthcare/healthcare",
    inputs: { adult_dose: "500", child_weight: "20", adult_weight: "70", max_factor: "0" },
    expect: ["最大倍数限制须 ≥ 1"],
    ref: "D-N6：max_factor=0 时旧实现受限剂量 = min(142.86, 500×0) = 0.00 mg，静默输出 0 剂量。修复后 <1 拒绝计算并提示「最大倍数限制须 ≥ 1」，不再输出 0 mg；默认 max_factor=2 正常计算，不含该提示 ⇒ 判别力成立。",
  },
  {
    slug: "healthcare/healthcare",
    inputs: { adult_dose: "0", child_weight: "20", adult_weight: "70", max_factor: "2" },
    expect: ["成人剂量须大于 0 mg"],
    ref: "D-N6（0 值分支）：成人剂量填 0 时旧实现输出「按体重剂量 0.00 / 受限剂量 0.00 mg」，既无意义又静默；修复后拒绝计算并提示。默认 500 mg 正常，不含该串 ⇒ 零命中。",
  },
  {
    slug: "healthcare/bsa-calculator",
    inputs: { weight: "8", height: "70", age: "0" },
    expect: ["BSA： 0.400", "所用公式： Haycock"],
    ref: "D-N30 0 岁分支：Haycock = 0.024265×8^0.5378×70^0.3964 = 0.400 m²；旧条件 age>0 把 0 岁排除，走 DuBois 0.007184×8^0.425×70^0.725 = 0.386 并标「成人，≥18 岁」。默认 65kg/170cm/30 岁 ⇒ 1.754/DuBois，不命中。",
  },
  {
    slug: "healthcare/weight-dosage",
    inputs: { weight: "18", mgkg: "12", freq: "3" },
    expect: ["216.0", "72.0"],
    ref: "日剂量 = 18×12 = 216 mg/天；单次 = 216÷3 = 72 mg/次",
  },

  // ---------- 评分类 ----------
  {
    slug: "healthcare/apgar",
    inputs: { appearance: "2", pulse: "2", grimace: "1", activity: "2", respiration: "2" },
    expect: ["9"],
    ref: "Apgar = 2+2+1+2+2 = 9 分（7–10 为正常）",
  },
  {
    slug: "healthcare/chads-vasc",
    inputs: { c: "1", h: "1", a: "0", d: "0", s: "0", v: "1", age65: "0", sex_f: "0" },
    expect: ["3", "高危"],
    ref: "CHA₂DS₂-VASc = 心衰1 + 高血压1 + 血管病1 = 3 分 → 高危",
  },
  {
    slug: "healthcare/morse",
    inputs: { hist: "0", sec_diag: "15", aid: "0", iv: "20", gait: "10", mental: "15" },
    expect: ["60"],
    ref: "Morse = 0+15+0+20+10+15 = 60 → >50 高风险",
  },
  {
    slug: "healthcare/nrs2002",
    inputs: { bmi: "3", weight_loss: "1", intake: "2", severity: "2", age70: "0" },
    expect: ["营养受损评分： 3 分 总分： 5 分"],
    ref: "营养受损 = max(3,1,2) = 3（修复前三项相加得 6）；总分 = 3+2+0 = 5（修复前 8）；≥3 → 存在营养风险。默认 1/1/1/2/1 得 1/4，不命中；不锚「存在营养风险： 是」，默认 4 分同样为「是」，会逃生。",
  },
  {
    slug: "healthcare/nrs2002",
    inputs: { bmi: "5", weight_loss: "0", intake: "0", severity: "0", age70: "0" },
    expect: ["请为每项输入 0–3 的整数分值，不能留空或超出范围"],
    ref: "越界拒绝：bmi=5 超出 0–3，直接提示并清空结果（不再静默限幅）；默认 1/1/1/2/1 合法，不出现该提示。",
  },
  {
    slug: "healthcare/wells",
    inputs: { dvt: "3", pe: "3", hr: "0", imm: "1.5", dvt_hist: "0", hem: "1", cancer: "0" },
    expect: ["评分： 21 分"],
    ref: "2026-10-25 权威权重修正后：Wells = 3×3+3×3+0+1.5×1.5+0+1+0 = 21.25 → toFixed(0) 21 分，>6 高度临床概率（旧 0/1 简化口径 8.5 已废止；「高度」分级标签与输入无关，作锚点即逃生项，改锚评分值；默认 1/1/1/1/1/0/0 → 11 分避开）",
  },
  {
    slug: "healthcare/checker-manager",
    inputs: { s0: "10", s1: "10", s2: "10", s3: "10", s4: "10", s5: "10", s6: "10", s7: "10", temp: "22", humid: "50" },
    expect: ["100.0"],
    ref: "总分 = 8×10 = 80，达标率 = 80÷80×100 = 100.0%",
  },

  // ---------- 血压与循环 ----------
  {
    slug: "healthcare/blood-pressure-grade",
    inputs: { sys: "130", dia: "85" },
    expect: ["脉压： 45 mmHg"],
    ref: "脉压 = 130−85 = 45 mmHg；收缩压 130/舒张压 85 属中国指南正常高值（修复前误判「3 等级」）。默认 120/80 同判正常高值但脉压 40，不命中；不锚「分级： 正常高值」，默认态同样命中会逃生。",
  },
  {
    slug: "healthcare/blood-pressure-grade",
    inputs: { sys: "140", dia: "90" },
    expect: ["脉压： 50 mmHg", "分级： 1 级高血压"],
    ref: "脉压 = 140−90 = 50 mmHg；收缩压 140 且舒张压 90 → 1 级高血压（修复前误判「4 等级」）。默认 120/80 为正常高值，不命中。",
  },
  {
    slug: "healthcare/blood-pressure-grade",
    inputs: { sys: "80", dia: "120" },
    expect: ["收缩压须大于舒张压"],
    ref: "收缩压 80 < 舒张压 120，物理上不可能 → 拒绝计算并提示（修复前输出「5 等级、脉压 −40」）。默认 120/80 有效，不命中。",
  },
  {
    slug: "healthcare/map",
    inputs: { sbp: "135", dbp: "85", hr: "70" },
    expect: ["101.7", "50"],
    ref: "MAP = 85 + (135−85)÷3 = 85 + 16.667 = 101.7 mmHg；脉压 = 50；≥70 判为正常",
  },
  {
    slug: "healthcare/qtc",
    inputs: { qt: "420", hr: "50", formula: "1" },
    expect: ["383.4"],
    ref: "RR = 60÷50 = 1.2 s；Bazett（下拉默认）= 420÷√1.2 = 420÷1.09545 = 383.4 ms；性别默认男 ⇒ 上限 450 ms、判未延长。",
  },
  {
    slug: "healthcare/qtc",
    inputs: { qt: "500", hr: "50", formula: "1" },
    expect: ["判定： 延长", "456.4"],
    ref: "D-N33：QT=500、HR=50、Bazett：RR=1.2，QTc=500÷√1.2=456.4 ms，超过男上限 450 ⇒ 判「延长」；默认 400/75 得 447.2/未延长，注入后不再命中默认串。",
  },

  // ---------- 体成分与代谢 ----------
  {
    slug: "healthcare/bmi-calculator",
    inputs: { height: "175", weight: "70", waist: "80", targetWeight: "65" },
    expect: ["22.9"],
    ref: "BMI = 70 ÷ 1.75² = 70 ÷ 3.0625 = 22.857 → 22.9 kg/m²",
  },
  {
    slug: "healthcare/bmr-calculator",
    inputs: { weight: "80", height: "175", age: "30", sex: "1" },
    expect: ["1749"],
    ref: "Mifflin-St Jeor（男）= 10×80 + 6.25×175 − 5×30 + 5 = 800 + 1093.75 − 150 + 5 = 1748.75 → 1749 kcal/天",
  },
  {
    slug: "healthcare/body-fat-estimator",
    inputs: { weight: "70", height: "175", age: "30", sex: "1" },
    expect: ["22.9", "18.1"],
    ref: "BMI = 70÷1.75² = 22.857；体脂率 = 1.2×22.857 + 0.23×30 − 10.8 − 5.4 = 27.43 + 6.9 − 16.2 = 18.13 → 18.1%",
  },
  {
    slug: "healthcare/bsa-calculator",
    inputs: { weight: "70", height: "175", age: "30" },
    expect: ["1.848"],
    ref: "Du Bois = 0.007184 × 70^0.425 × 175^0.725 = 0.007184 × 6.0843 × 42.284 = 1.848 m²",
  },
  {
    slug: "healthcare/bsa-calculator",
    inputs: { weight: "10", height: "80", age: "2" },
    expect: ["BSA： 0.476", "所用公式： Haycock"],
    ref: "D-N30：2 岁 10kg/80cm ⇒ Haycock = 0.024265×10^0.5378×80^0.3964 = 0.476 m²；旧实现忽略年龄、恒用 DuBois 得 0.458，且页内无公式标签 ⇒ 默认成人 1.754/DuBois 亦不命中。",
  },
  {
    slug: "healthcare/ibw",
    inputs: { height: "175", sex: "1" },
    expect: ["70.6", "77.6", "63.5"],
    ref: "Devine（男）= 50 + 0.91×(175−152.4) = 50 + 20.566 = 70.6 kg；上限 ×1.1 = 77.6；下限 ×0.9 = 63.5",
  },
  {
    slug: "healthcare/map",
    inputs: { sbp: "180", dbp: "120", hr: "90" },
    expect: ["MAP： 140.0", "偏高（需排查）"],
    ref: "D-N34 高值分级：MAP = 120 + (180−120)/3 = 140.0；旧实现 m≥70 一律「正常」，现 ≥100 判「偏高（需排查）」。默认 120/80 ⇒ 93.3 正常，不命中。",
  },
  {
    slug: "healthcare/map",
    inputs: { sbp: "90", dbp: "40", hr: "110" },
    expect: ["MAP： 56.7", "偏低", "心率： 110 次/分"],
    ref: "D-N34 低值 + 心率展示：90/40 ⇒ MAP = 40 + 50/3 = 56.7、脉压 50.0 ⇒ 偏低；心率 110 仅记录不参与公式，避免字段读入后成为死输入。",
  },
  {
    slug: "healthcare/map",
    inputs: { sbp: "80", dbp: "120" },
    expect: ["舒张压不得高于收缩压"],
    ref: "D-N34 顺序守卫：舒张压 120 > 收缩压 80 ⇒ 拒绝计算，不输出负脉压与错误分级。",
  },
  {
    slug: "healthcare/ideal-weight",
    inputs: { height: "180", sex: "0" },
    expect: ["70.5"],
    ref: "D-N35 Devine（女 180 cm）= 45.5 + 2.3×(180/2.54−60) = 45.5 + 2.3×10.866 = 70.5 kg；默认 170/男 ⇒ 65.9，不命中。",
  },
  {
    slug: "healthcare/ideal-weight",
    inputs: { height: "150", sex: "1" },
    expect: ["身高需 ≥ 152.4 cm"],
    ref: "D-N35 身高守卫：150 cm 低于 5 英尺 ⇒ 拒绝并提示改用儿科/专用公式；旧实现输出 Devine 50+2.3×(−0.94)=47.8 并继续渲染。",
  },
  {
    slug: "healthcare/ibw",
    inputs: { height: "100", sex: "0" },
    expect: ["公式不适用于此身高范围"],
    ref: "D-N28 负值守卫：女性 100 cm ⇒ 45.5 + 0.91×(100−152.4) = −2.2 kg；旧实现输出 IBW −2.2、上限 −2.4、下限 −2.0。修复后拒绝并提示公式不适用。默认 170/男 ⇒ 66.0 kg 正常，不含该串。",
  },
  {
    slug: "healthcare/ibw",
    inputs: { height: "148", sex: "1" },
    expect: ["身高低于 150 cm"],
    ref: "D-N28 低身高提示：男 148 cm ⇒ 50 + 0.91×(148−152.4) = 46.0 kg（正值但偏低），追加 Devine 适用范围提示；默认 170 cm 不命中。",
  },
  {
    slug: "healthcare/ibw",
    inputs: { height: "170", sex: "1", tbw: "100" },
    expect: ["校正体重 ABW： 79.6", "（IBW + 0.4 × (实际体重 − IBW)）"],
    ref: "ABW = IBW + 0.4×(TBW−IBW)：170 cm 男 IBW = 50 + 0.91×17.6 = 66.016；TBW 100 kg ⇒ 66.016 + 0.4×(100−66.016) = 79.6096 → 79.6。默认态（170 cm 男、TBW 留空）不输出 ABW 行 ⇒ 两条均不命中（不复用默认就有的「IBW 66.0」串）。",
  },
  {
    slug: "healthcare/ideal-weight",
    inputs: { height: "175", sex: "1" },
    expect: ["Devine）： 70.5", "Hamwi： 72.0", "Robinson： 68.9"],
    ref: "175 cm 男性，in=68.8976、超出 8.8976 英寸：Devine = 50+2.3×8.8976 = 70.46 ⇒ 70.5；Hamwi = 48+2.7×8.8976 = 72.02 ⇒ 72.0；Miller = 56.2+1.41×8.8976 = 68.75 ⇒ 68.7；Robinson = 52+1.9×8.8976 = 68.91 ⇒ 68.9。默认态 170 cm 男性为 65.9 / 66.9 / 64.9 / 64.8，均不命中。旧用例只锚 Devine 单值，已随四公式实现更新。"
  },
  {
    slug: "healthcare/healthcare-5",
    inputs: { weight: "65", activity: "1.2", goal: "1.5" },
    expect: ["62.4", "93.6", "31.2"],
    ref: "维持 = 65×0.8×1.2 = 62.4 g；目标 = 62.4×1.5 = 93.6 g（1.44 g/kg/日）；每餐 = 93.6÷3 = 31.2 g（D-N36 由四餐改三餐，与引据「宜分三餐均匀摄入」一致）",
  },
  {
    slug: "healthcare/healthcare-5",
    inputs: { weight: "70", activity: "1", goal: "0.8" },
    expect: ["44.8", "14.9", "低于 WHO/FAO/UNU 成人最低 0.8 g/kg/日"],
    ref: "D-N36 低蛋白提示：70×0.8×1 = 56.0；×0.8 = 44.8 g；÷3 = 14.9 g；折合 0.64 g/kg/日 <0.8 ⇒ 红字提示。旧实现静默输出 0.64 g/kg 的「减脂」方案。默认 1.2/1.2 ⇒ 1.152 g/kg，不命中。",
  },
  {
    slug: "healthcare/healthcare-5",
    inputs: { weight: "70", activity: "0.5", goal: "1.2" },
    expect: ["活动系数 1–2.5"],
    ref: "D-N36 白名单：活动系数 0.5 越界 ⇒ 拒绝并提示常用范围，不再输出减半的蛋白质需求。",
  },
  {
    slug: "healthcare/blood-pressure-grade",
    inputs: { sys: "145", dia: "85" },
    expect: ["单纯收缩期高血压", "脉压： 60"],
    ref: "D-N48 分级：145/85 ⇒ 收缩压 ≥140 且舒张压 <90 ⇒ 单纯收缩期高血压；脉压 60。旧实现默认 120/80 输出「3 等级」，现为「正常高值」。",
  },
  {
    slug: "healthcare/blood-pressure-grade",
    inputs: { sys: "185", dia: "115" },
    expect: ["3 级高血压"],
    ref: "D-N48 高值分支：185/115 ⇒ 收缩压 ≥180 或舒张压 ≥110 ⇒ 3 级高血压。",
  },
  {
    slug: "healthcare/blood-pressure-grade",
    inputs: { sys: "80", dia: "120" },
    expect: ["收缩压须大于舒张压"],
    ref: "D-N48 顺序守卫：舒张压 120 > 收缩压 80 ⇒ 拒绝计算，不输出负脉压。",
  },
  {
    slug: "healthcare/healthcare-4",
    inputs: { dyspnea: "0", rest: "0", limits: "1" },
    expect: ["NYHA 分级： 3 级", "答案存在矛盾"],
    ref: "D-N50 矛盾守卫：勾「活动明显受限」但气短为 0 ⇒ 判 3 级并红字提示复核；旧实现判 I 级无症状。默认 1/0/0 走 II 级，不命中。",
  },
  {
    slug: "healthcare/healthcare-4",
    inputs: { dyspnea: "", rest: "", limits: "" },
    expect: ["请完整填写三项"],
    ref: "D-N50 空态守卫：三项全空 ⇒ 拒绝判读；旧实现按 0 计 ⇒ I 级无症状。",
  },
  {
    slug: "healthcare/fat-loss-deficit",
    inputs: { loss: "5", days: "10", targetWeight: "70" },
    expect: ["超过 1000 kcal/天"],
    ref: "减脂缺口高强度提示（763 批补查）：5×7700 = 38500 kcal，÷10 = 3850 kcal/天；超过 1000 ⇒ 红字提示延长周期/咨询营养师。既有 4 kg/50 天 ⇒ 616 不命中。判别器实测数值锚「3850」在默认快照也命中（页面固定算例），已移除，仅留依赖输入的提示锚。",
  },
  {
    slug: "healthcare/fat-loss-deficit",
    inputs: { loss: "120", days: "30", targetWeight: "60" },
    expect: ["目标减重不能大于等于目标体重"],
    ref: "减脂缺口逻辑守卫（763 批补查）：减重 120 kg ≥ 目标体重 60 kg ⇒ 起始体重为负（−60 kg），旧实现直接输出 −60.0 kg；修复后拒绝并提示核对。",
  },
  {
    slug: "healthcare/fat-loss-deficit",
    inputs: { loss: "4", days: "50", targetWeight: "70" },
    expect: ["30800", "616", "74"],
    ref: "总缺口 = 4×7700 = 30800 kcal；日缺口 = 30800÷50 = 616；起始体重 = 70+4 = 74 kg",
  },
  {
    slug: "healthcare/water-intake",
    inputs: { weight: "70", activity: "1.2", climate: "1.1" },
    expect: ["3234", "13"],
    ref: "饮水量 = 70×35×1.2×1.1 = 3234 mL；杯数 = 3234÷250 = 12.94 → 13 杯",
  },

  // ---------- 肾功 ----------
  {
    slug: "healthcare/egfr",
    inputs: { scr: "100", age: "60", sex: "1", race: "1" },
    expect: ["70.1", "2"],
    ref: "CKD-EPI（男）：Scr = 100÷88.4 = 1.1312 mg/dL；min(1.1312÷0.9,1) = 1 → 1；max = 1.2569 → 1.2569^(−1.209) = 0.75839；0.993^60 = 0.65605；eGFR = 141×0.75839×0.65605 = 70.15 → 70.1，60–89 为 G2 期",
  },
  {
    slug: "healthcare/egfr",
    inputs: { scr: "120", age: "65", sex: "1", race: "0" },
    expect: ["54.3", "G3a"],
    ref: "B1 回归：种族系数注入 0（旧实现直接乘 0 ⇒ eGFR 0.0、误判 5 期）。修正后 0 按无校正系数 1 处理：Scr=120÷88.4=1.3575 mg/dL，max(1.3575÷0.9,1)=1.5083 → ^(−1.209)=0.60843；0.993^65=0.63346；eGFR=141×0.60843×0.63346=54.34 → 54.3，45–59 为 G3a。默认态 80/50/男 ⇒ 98.6/G1，与本用例零交集。",
  },
  {
    slug: "healthcare/egfr-calculator",
    inputs: { scr: "1.2", age: "60", sex: "2" },
    expect: ["45.8"],
    ref: "MDRD（女）= 175 × 1.2^(−1.154) × 60^(−0.203) × 0.742 = 175 × 0.81033 × 0.43550 × 0.742 = 45.83 → 45.8 mL/min/1.73m²",
  },
  {
    slug: "healthcare/egfr-calculator",
    inputs: { scr: "120", age: "65", sex: "2", scrUnit: "umol" },
    expect: ["39.1", "G3b"],
    ref: "D-N31 µmol/L + 分期：120 µmol/L ÷ 88.4 = 1.3575 mg/dL；女 65 岁 ⇒ 175×1.3575^(−1.154)×65^(−0.203)×0.742 = 39.13 → 39.1，落在 30–44 ⇒ G3b。修复前无单位切换（120 被当 mg/dL ⇒ 0.9）、无分期。判别器实测单位串「mL/min/1.73m²」在默认快照也命中，已移除，仅留依赖输入的数值与分期锚。",
  },
  {
    slug: "healthcare/gfr-cockcroft",
    inputs: { age: "50", weight: "70", scr: "80", sex: "1", height: "155" },
    expect: ["98.83"],
    ref: "D-N22：CrCl = (140−50)×70 ÷ [72×(80÷88.4)] = 96.6875 mL/min；BSA(DuBois, 70kg/155cm) = 0.007184×70^0.425×155^0.725 = 1.6925 m²；归一 = 96.6875×1.73÷1.6925 = 98.83。旧实现身高硬编码 170 cm ⇒ 得 92.43，注入后零命中。",
  },
  {
    slug: "healthcare/gfr-cockcroft",
    inputs: { age: "60", weight: "65", scr: "90", sex: "0" },
    expect: ["60.30"],
    ref: "Scr = 90÷88.4 = 1.01810 mg/dL；CrCl = (140−60)×65 ÷ (72×1.01810) × 0.85 = 5200÷73.303×0.85 = 60.30 mL/min",
  },
  {
    slug: "healthcare/gfr-cockcroft",
    inputs: { age: "60", weight: "100", scr: "90", sex: "1", height: "170", wtBasis: "abw" },
    expect: ["CrCl： 86.88", "计算体重：79.6 kg（校正体重 ABW"],
    ref: "肥胖口径：170 cm 男 IBW = 50 + 0.91×17.6 = 66.016；ABW = 66.016 + 0.4×(100−66.016) = 79.6096 → 79.6 kg；CrCl = (140−60)×79.6096 ÷ (72×90/88.4) = 6368.77÷73.30 = 86.88 mL/min。默认口径 TBW（70 kg）得 96.69 且显示「实际体重 TBW」⇒ 两条均不命中。",
  },
  {
    slug: "healthcare/gfr-cockcroft",
    inputs: { age: "50", weight: "70", scr: "80", sex: "1", height: "0" },
    expect: ["身高必须大于 0（用于体表面积归一）"],
    ref: "G01-A3：身高 0 会让 BSA=0、归一值除零，旧实现只拦负值（__N）与纯分母零（__D），身高 0 仍输出 CrCl 与 BSA 0。注入身高 0 ⇒ 守卫提示；默认身高 170 不含该串 ⇒ 强判别。",
  },

  // ---------- 输液与电解质 ----------
  {
    slug: "healthcare/healthcare-2",
    inputs: { volume: "250", time_min: "60", drop: "15" },
    expect: ["3750", "62.50", "0.96"],
    ref: "总滴数 = 250×15 = 3750 滴；滴速 = 3750÷60 = 62.50 滴/分；秒/滴 = 60÷62.5 = 0.96",
  },
  {
    slug: "healthcare/healthcare-2",
    inputs: { volume: "1000", time_min: "240", drop: "15" },
    expect: ["≈65 滴/分"],
    ref: "D-N17（2026-11-16）：新增泵速（mL/h）与 5 滴/分档位提示。1000 mL / 240 min ⇒ 62.5 滴/分，按 5 取整 ⇒ 65 滴/分。默认 500/120/20 ⇒ 83.3 → ≈85，不命中。"
  },
  {
    slug: "healthcare/healthcare-2",
    inputs: { volume: "500", time_min: "2", drop: "20" },
    expect: ["输液时间须在 5–1440 分钟之间"],
    ref: "D-N17 边界：时间 2 分钟旧实现输出 5000.0 滴/分的物理不可能值；现要求 5–1440 分钟。默认 120 ⇒ 不命中。"
  },
  {
    slug: "healthcare/healthcare-2",
    inputs: { volume: "500", time_min: "120", drop: "42" },
    expect: ["非常用滴系数（10/15/20/60 滴/mL）"],
    ref: "D-N17 提示：42 滴/mL 不属于常用规格，计算照常但追加核对输液器提示；默认 drop=20 ⇒ 不命中。"
  },
  {
    slug: "healthcare/healthcare-3",
    inputs: { na_inf: "140", tbw: "35", target: "132", current: "120" },
    expect: ["0.56"],
    ref: "预期升幅 = (140−120) ÷ (35+1) = 20÷36 = 0.5556 → 0.56 mmol/L；目标差距 = 132−120 = 12 mmol/L",
  },
  {
    slug: "healthcare/healthcare-3",
    inputs: { na_inf: "154", tbw: "30", target: "135", current: "120" },
    expect: ["13.7 L", "570 mL/h", "7.3–9.1 L"],
    ref: "D-N21 容量/速度：升幅 = (154−120)÷(30+1) = 1.0968 → 1.10；差距 15.0；所需液量 15÷1.0968 = 13.68 → 13.7 L；24h 均速 13.68×1000÷24 = 570 mL/h；按 8–10 mmol/L 上限单日最多 8÷1.0968=7.3 至 10÷1.0968=9.1 L。修复前只输出「预期升幅」，无液量与速度。输入 30/135 均非默认（42/130）。",
  },
  {
    slug: "healthcare/healthcare-3",
    inputs: { na_inf: "154", tbw: "30", target: "125", current: "130" },
    expect: ["目标血钠低于当前血钠"],
    ref: "D-N21 反向目标守卫：目标 125 < 当前 130 ⇒ 差距 −5.0，须红字提示核对目标/当前值，不得输出负液量或负速度。默认 130 > 118 ⇒ 不命中。",
  },
  {
    slug: "healthcare/healthcare-3",
    inputs: { na_inf: "110", tbw: "30", target: "130", current: "120" },
    expect: ["输注液钠浓度须高于当前血钠"],
    ref: "D-N21 无提升守卫：输注液钠 110 ≤ 当前 120 ⇒ 每升升幅 ≤ 0，须提示无法提升血钠，不得输出 Infinity/负液量。默认 154 > 118 ⇒ 不命中。",
  },
  {
    slug: "healthcare/parkland",
    inputs: { weight: "60", tbsa: "25", hours: "6" },
    expect: ["6000", "3000", "3000", "2250"],
    ref: "Parkland 24h = 4×60×25 = 6000 mL；前 8h 半量 3000、后 16h 半量 3000；6h 处于前 8h 段 ⇒ 累计应输 = 3000×6÷8 = 2250 mL（分段累计；旧实现按 24h 均摊为 1500，少 750）。默认 70/30/0 ⇒ 8400/4200/4200/0，注入值全非默认。",
  },
  {
    slug: "healthcare/parkland",
    inputs: { weight: "60", tbsa: "25", hours: "8" },
    expect: ["当前累计应输（按 8h/16h 分段）： 3000"],
    ref: "8h 边界：前 8h 应达到半量 3000 mL（6000 的 1/2），旧实现为 6000×8÷24 = 2000。输入 60/25/8 全非默认。",
  },
  {
    slug: "healthcare/parkland",
    inputs: { weight: "60", tbsa: "25", hours: "12" },
    expect: ["当前累计应输（按 8h/16h 分段）： 3750"],
    ref: "12h 处于后 16h 段：3000 + 3000×(12−8)÷16 = 3000 + 750 = 3750 mL；旧实现 6000×12÷24 = 3000。",
  },
  {
    slug: "healthcare/parkland",
    inputs: { weight: "60", tbsa: "25", hours: "30" },
    expect: ["当前累计应输（按 8h/16h 分段）： 6000", "已输注时间超过 24 小时"],
    ref: "超过 24h 守卫：hours=30 钳到 24 ⇒ 累计 = 半量 3000 + 3000×(24−8)÷16 = 6000（24h 总量封顶），并提示已超 24h；旧实现 6000×30÷24 = 7500，超过总量且无上限提示。",
  },
  {
    slug: "healthcare/healthcare-4",
    inputs: { dyspnea: "1", rest: "0", limits: "1" },
    expect: ["3", "III 明显受限"],
    ref: "静息无症状 + 有呼吸困难 + 活动受限 → NYHA III 级（明显受限）",
  },
  {
    slug: "healthcare/resp-rate",
    inputs: { rr: "24", age: "40", state: "1" },
    expect: ["呼吸过速（3 级）", "偏离范围中值： 8"],
    ref: "成人 18–<65 岁范围 12–20，24 > 20 → 呼吸过速（3 级）；偏离范围中值 |24−16| = 8。默认 16 → 正常、偏离 0，不命中这两串 ⇒ 强判别。",
  },
  {
    slug: "healthcare/resp-rate",
    inputs: { rr: "40", age: "0.5", state: "1" },
    expect: ["参考范围（婴儿（&lt;1 岁））： 30–60 次/分"],
    ref: "D-N47 年龄分段：0.5 岁 40 次/分落在婴儿 30–60 ⇒ 正常；旧实现固定 12–20 判「3 级异常」并显示偏离 24。判别器实测「状态： 正常 （1 级）」在默认快照也命中，已移除，仅留依赖年龄分段的参考区间锚。",
  },
  {
    slug: "healthcare/resp-rate",
    inputs: { rr: "30", age: "30", state: "2" },
    expect: ["运动后（不按静息分级）", "运动上限参考： 40"],
    ref: "D-N47 运动态：30 次/分、state=2 ⇒ 不按静息 12–20 分级，仅给运动上限参考；旧实现仍判「3 级异常」而同一卡片写「运动上限 40」，自相矛盾。",
  },

  // ---------- 血醇 ----------
  {
    slug: "healthcare/bac-calculator",
    inputs: { volume: "500", abv: "5", weight: "70", sex: "1", hours: "1" },
    expect: ["0.026"],
    ref: "酒精 = 500×5÷100×0.789 = 19.725 g；BAC = 19.725÷(0.68×70)÷10 = 0.041439 − 0.015×1 = 0.026439 → 0.026 g/100mL",
  },

  // ---------- 孕产与儿童 ----------
  {
    slug: "healthcare/due-date-calc",
    inputs: { lmp: "140", cycleLen: "28", ovulationDay: "14" },
    expect: [ "20.0 周" ],
    ref: "孕周 = 140÷7 = 20.0 周；距预产期 = 280−140 = 140 天；距排卵 = 140−14 = 126 天",
  },
  {
    slug: "healthcare/bmi-2",
    inputs: { age: "8", bmi: "20", sex: "1" },
    expect: ["0.32"],
    ref: "Z = (20 − 16.5 − 8×0.35) ÷ 2.2 = 0.7÷2.2 = 0.318 → 0.32（|Z| < 2 判为正常）",
  },

  // ---------- 统计、心率与能量 ----------
{
  "slug": "healthcare/analysis-report-cost",
  "inputs": { "data": "内科,1200000,980000\n外科,1500000,1350000\n儿科,600000,720000\n检验科,900000,540000" },
  "expect": [
    "收入合计： 4200000.00",
    "收支结余： +610000.00",
    "成本率： 85.48%"
  ],
  "ref": "收入=1200000+1500000+600000+900000=4200000；成本=980000+1350000+720000+540000=3590000；结余=+610000；成本率=3590000/4200000=85.48%（默认三科室 2250000/2070000/结余+180000，避开）"
},
  {
    slug: "healthcare/heart-rate-zones",
    inputs: { age: "40", rhr: "60", lthr: "170", maxhrInput: "190" },
    expect: ["180", "156"],
    ref: "Karvonen（默认 hrr 法）：最大心率 = 220−40 = 180；HRR = 180−60 = 120；Z3 上限 = 60 + 120×0.8 = 156",
  },
  {
    slug: "healthcare/tdee-calculator",
    inputs: { age: "30", height: "175", weight: "80", bf: "20", act: "1.55" },
    expect: ["1752", "2716"],
    ref: "给体脂率 20% 时走 Katch-McArdle：瘦体重 = 80×(1−20÷100) = 64 kg；BMR = 370 + 21.6×64 = 1752.4 → 1752；TDEE = 1752×1.55 = 2715.6 → 2716 kcal（活动系数 1.55 为默认中强度）",
  },
  { slug: "healthcare/analysis-report-cost", inputs: {data:"騼杖,300000,270000\n心内科,500000,460000\n皮屏小,200000,220000\n急費科,120000,100000"}, expect: ["1120000.00"], ref: "粘贴区四行「科室,收入,成本」：收入合计 = 300,000+500,000+200,000+120,000 = **1,120,000.00**；成本合计 1,050,000.00，收支结余 = +70,000.00（默认 3 科室 2,250,000.00，注入失败即不命中）" },
  { slug: "healthcare/analysis-report-cost", inputs: {data:"騼杖,300000,270000\n心内科,500000,460000\n皮屏小,200000,220000\n急費科,120000,100000"}, expect: ["93.75%"], ref: "成本率 = 成本合计 1,050,000 ÷ 收入合计 1,120,000 × 100% = **93.75%**（默认 2,070,000÷2,250,000 得 92.00%）；结余率 6.25% 与之相加为 100%" },
  { slug: "healthcare/analysis-report-cost", inputs: {data:"騼杖,300000,270000\n心内科,500000,460000\n皮屏小,200000,220000\n急費科,120000,100000"}, expect: ["心内科"], ref: "结余最高科室取各行结余最大值：骨科 +30,000、心内科 +40,000、皮肤科 −20,000、急诊科 +20,000 ⇒ **心内科**（默认「内科」）；同组亏损科室数 = 1（皮肤科成本 > 收入）" },
  {
    "slug": "healthcare/antipyretic-dose",
    "inputs": {
      "weight": "42",
      "dose": "42",
      "conc": "42"
    },
    "expect": [
      "单次药量： 23.8"
    ],
    "ref": "注入非默认输入，42 kg×42 mg/kg=1764 mg 超过成人单次极量 1000 mg ⇒ 单次按 1000 mg 封顶 = 1000÷42 = 23.8 mL（修复前无单次封顶会输出 42.0 mL/1764 mg）。默认 15×15÷32=7.0 mL 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/apgar",
    "inputs": {
      "appearance": "42",
      "pulse": "42",
      "grimace": "42",
      "activity": "42",
      "respiration": "42"
    },
    "expect": [
      "42\n42\n42\n42\n4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"appearance\":\"42\",\"pulse\":\"42\",\"grimace\":\"42\",\"activity\":\"42\",\"respiration\":\"42\"}，输出区含「42\n42\n42\n42\n4」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/bac-calculator",
    "inputs": {
      "volume": "42",
      "abv": "42",
      "weight": "42",
      "sex": "42",
      "hours": "42"
    },
    "expect": [
      "42\n42\n42\n42\n4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"volume\":\"42\",\"abv\":\"42\",\"weight\":\"42\",\"sex\":\"42\",\"hours\":\"42\"}，输出区含「42\n42\n42\n42\n4」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/bmi-2",
    "inputs": {
      "age": "42",
      "bmi": "42",
      "sex": "42"
    },
    "expect": [
      " 百分位近似： 100.0 % 评估： 超重"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"bmi\":\"42\",\"sex\":\"42\"}，输出区含「 百分位近似： 100.0 % 评估： 超重」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/bmr-calculator",
    "inputs": {
      "weight": "42",
      "height": "42",
      "age": "42",
      "sex": "42"
    },
    "expect": [
      "42\n42\n42\n42\nBMR： 312 kcal/天"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"height\":\"42\",\"age\":\"42\",\"sex\":\"42\"}，输出区含「42\n42\n42\n42\nBMR： 312 kcal/天」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/body-fat-estimator",
    "inputs": {
      "weight": "42",
      "height": "42",
      "age": "42",
      "sex": "42"
    },
    "expect": [
      "42\n42\n42\n42\nBMI： 238.1 体脂率： 290.0 %"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"height\":\"42\",\"age\":\"42\",\"sex\":\"42\"}，输出区含「42\n42\n42\n42\nBMI： 238.1 体脂率： 290.0 %」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/bmi-calculator",
    "inputs": {
      "height": "42",
      "weight": "42",
      "waist": "42",
      "targetWeight": "42"
    },
    "expect": [
      "42\n42\n42\n42\n238.1\n肥胖"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"height\":\"42\",\"weight\":\"42\",\"waist\":\"42\",\"targetWeight\":\"42\"}，输出区含「42\n42\n42\n42\n238.1\n肥胖」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/bsa-calculator",
    "inputs": {
      "weight": "42",
      "height": "42",
      "age": "42"
    },
    "expect": [
      "42\n42\n42\nBSA： 0.529 m²"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"height\":\"42\",\"age\":\"42\"}，输出区含「42\n42\n42\nBSA： 0.529 m²」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/chads-vasc",
    "inputs": {
      "c": "42",
      "h": "42",
      "a": "42",
      "d": "42",
      "s": "42",
      "v": "42",
      "age65": "42",
      "sex_f": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n42\n评分： 420 分 风险分层： 高危"
    ],
    "ref": "自动补强（B类零用例，2026-10-25 A₂ 权重修正后）：注入非默认输入（8 项全 42），评分=42×(1+1+2+1+2+1+1+1)=420 分 风险分层高危；默认态（全 0 → 0 分低危）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/checker-manager",
    "inputs": {
      "s0": "42",
      "s1": "42",
      "s2": "42",
      "s3": "42",
      "s4": "42",
      "s5": "42",
      "s6": "42",
      "s7": "42",
      "temp": "42",
      "humid": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"s0\":\"42\",\"s1\":\"42\",\"s2\":\"42\",\"s3\":\"42\",\"s4\":\"42\",\"s5\":\"42\",\"s6\":\"42\",\"s7\":\"42\",\"temp\":\"42\",\"humid\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/due-date-calc",
    "inputs": {
      "lmp": "42",
      "cycleLen": "42",
      "ovulationDay": "42"
    },
    "expect": [
      "42\n42\n42\n当前孕周： 6.0 周 距预产期： 238 天 距排卵期： 0 天"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lmp\":\"42\",\"cycleLen\":\"42\",\"ovulationDay\":\"42\"}，输出区含「42\n42\n42\n当前孕周： 6.0 周 距预产期： 238 天 距排卵期： 0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/egfr",
    "inputs": {
      "scr": "150",
      "age": "70",
      "sex": "0",
      "race": "1.159"
    },
    "expect": [
      "eGFR： 34.9",
      "G3b"
    ],
    "ref": "CKD-EPI 2009 女性（sex=0）+ 非裔系数 1.159：Scr=150 µmol/L→1.6968 mg/dL，141×1^−0.329×2.424^−1.209×0.993^70×1.018×1.159=34.88→34.9，分期 G3b（原自动补强用例注入 sex=42 为非法选项，页面被 __tbInputGuard 拦截，期望串恒不成立，已改为合法非默认输入）"
  },
  {
    "slug": "healthcare/gfr-cockcroft",
    "inputs": {
      "age": "42",
      "weight": "42",
      "scr": "42",
      "sex": "42",
      "height": "42"
    },
    "expect": [
      "CrCl： 120.32"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"weight\":\"42\",\"scr\":\"42\",\"sex\":\"42\",\"height\":\"42\"}，CrCl = (140−42)×42 ÷ (72×(42÷88.4)) × 1 = 120.32 mL/min；默认态 60 岁/70kg/90µmol/L 得 70.94 ⇒ 不命中。D-N22 新增身高项后原「四值前缀」串失效，改为单锚 CrCl 值。"
  },
  {
    "slug": "healthcare/egfr-calculator",
    "inputs": {
      "scr": "2.5",
      "age": "72",
      "sex": "2"
    },
    "expect": [
      "eGFR： 18.9",
      "G4"
    ],
    "ref": "MDRD 简化式：175×2.5^−1.154×72^−0.203×0.742（女性）=18.93→18.9，分期 G4（原自动补强用例注入 sex=42 为非法选项，被输入守卫拦截，期望串恒不成立，已改为合法非默认输入）"
  },
  {
    "slug": "healthcare/fat-loss-deficit",
    "inputs": {
      "loss": "42",
      "days": "42",
      "targetWeight": "42"
    },
    "expect": [
      "42\n42\n42\n⚠ 目标减重不能大于等于目标体重"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"loss\":\"42\",\"days\":\"42\",\"targetWeight\":\"42\"}，命中减脂缺口逻辑守卫（减重 42 ≥ 目标体重 42）；默认态（输入回退，70+4）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/healthcare-2",
    "inputs": {
      "volume": "42",
      "time_min": "42",
      "drop": "42"
    },
    "expect": [
      "42\n42\n42\n总滴数： 1764 滴 滴速： 42.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"volume\":\"42\",\"time_min\":\"42\",\"drop\":\"42\"}，输出区含「42\n42\n42\n总滴数： 1764 滴 滴速： 42.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/healthcare-3",
    "inputs": {
      "na_inf": "42",
      "target": "42",
      "current": "42"
    },
    "expect": [
      "每输注 1 L 预期升幅： 0.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"na_inf\":\"42\",\"target\":\"42\",\"current\":\"42\"}，输出区含「每输注 1 L 预期升幅： 0.00」（745 批标签改为每升口径）；默认态升幅 0.84 ⇒ 零逃生。"
  },
  {
    "slug": "healthcare/healthcare-3",
    "inputs": {
      "na_inf": "160",
      "tbw": "40",
      "target": "135",
      "current": "120"
    },
    "expect": [
      "每输注 1 L 预期升幅： 0.98",
      "达到目标所需液量： 15.4 L",
      "按 24h 均速输注： 641 mL/h"
    ],
    "ref": "835 批复核失败重做：原用例 inputs 154/42/130/118 恰为页面默认值，expect 三串又取自深解静态算例 ⇒ 注入失败时默认态即命中（all_default 假通过）。改用非默认输入 160/40/135/120：每升升幅 (160−120)/(40+1)=40/41=0.9756→0.98；目标差距 135−120=15.0；所需液量 15/0.9756=15.375→15.4 L；24h 均速 15.375×1000/24=640.6→641 mL/h。三锚均来自 calc() 结果容器、随输入变化，默认态 0.84/14.3/597 全不命中。"
  },
  {
    "slug": "healthcare/healthcare-5",
    "inputs": {
      "weight": "42",
      "activity": "2",
      "goal": "1.5"
    },
    "expect": [
      "维持需求： 67.2 g 目标需求： 100.8 g（2.40 g/kg/日） 每餐建议（三餐均分）： 33.6 g"
    ],
    "ref": "自动补强（B类零用例）：注入 42 kg/活动 2/目标 1.5，输出「维持需求： 67.2 g 目标需求： 100.8 g（2.40 g/kg/日） 每餐建议（三餐均分）： 33.6 g」；默认 70/1.2/1.2 ⇒ 目标 80.6、每餐 26.9，整串零交集。活动/目标已加白名单，原 42/42 输入会走越界提示，故更新为合法非默认值。"
  },
  {
    "slug": "healthcare/healthcare-4",
    "inputs": {
      "dyspnea": "0",
      "rest": "1",
      "limits": "0"
    },
    "expect": [
      "NYHA 分级： 4 级 解释： IV 静息症状"
    ],
    "ref": "边界分支：静息症状=1 ⇒ IV 级；默认 1/0/0 走 II 级，不出现该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/healthcare",
    "inputs": {
      "adult_dose": "42",
      "child_weight": "42",
      "adult_weight": "42",
      "max_factor": "42"
    },
    "expect": [
      "42\n42\n42\n42\n按体重剂量： 42.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"adult_dose\":\"42\",\"child_weight\":\"42\",\"adult_weight\":\"42\",\"max_factor\":\"42\"}，输出区含「42\n42\n42\n42\n按体重剂量： 42.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/ibw",
    "inputs": {
      "height": "42",
      "sex": "42"
    },
    "expect": [
      "身高须为 100–250 cm 的正数"
    ],
    "ref": "D-N28 身高守卫：height=42 cm 越界（<100）⇒ 拒绝计算并提示「身高须为 100–250 cm 的正数」，不再输出负 IBW（修复前 -50.5 kg）。默认 height=170 合法，不含该提示 ⇒ 判别力成立。"
  },
  {
    "slug": "healthcare/ideal-weight",
    "inputs": {
      "height": "42",
      "sex": "42"
    },
    "expect": [
      "身高需 ≥ 152.4 cm（5 英尺）才能套用这些公式"
    ],
    "ref": "身高 42 cm 低于 5 英尺基准 ⇒ 页面走「公式外推不可靠」保护分支，不再输出负值（旧断言 -54.5 kg 是未加保护的负值外推，已随实现修正）。默认态 170 cm 正常输出，不含该警告串。"
  },
  {
    "slug": "healthcare/heart-rate-zones",
    "inputs": {
      "age": "42",
      "rhr": "42",
      "lthr": "42",
      "maxhrInput": "42"
    },
    "expect": [
      "Z3 Z4 Z5\n42 静息 137 有氧起点 151 无氧起点 178 最大\n💚 静息心率：优秀 运动员水平，心肺功能很好"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"rhr\":\"42\",\"lthr\":\"42\",\"maxhrInput\":\"42\"}，输出区含「Z3 Z4 Z5\n42 静息 137 有氧起点 151 无氧起点 178 最大\n…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/map",
    "inputs": {
      "sbp": "42",
      "dbp": "42",
      "hr": "42"
    },
    "expect": [
      "42\n42\n42\nMAP： 42.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sbp\":\"42\",\"dbp\":\"42\",\"hr\":\"42\"}，输出区含「42\n42\n42\nMAP： 42.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/morse",
    "inputs": {
      "hist": "42",
      "sec_diag": "42",
      "aid": "42",
      "iv": "42",
      "gait": "42",
      "mental": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n总分： 252"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"hist\":\"42\",\"sec_diag\":\"42\",\"aid\":\"42\",\"iv\":\"42\",\"gait\":\"42\",\"mental\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n总分： 252」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/nrs2002",
    "inputs": {
      "bmi": "3",
      "weight_loss": "0",
      "intake": "0",
      "severity": "3",
      "age70": "1"
    },
    "expect": [
      "营养受损评分： 3 分 总分： 7 分"
    ],
    "ref": "边界分支：营养受损 max(3,0,0)=3、总分 3+3+1=7；默认 1/1/1/2/1 得 1/4，不命中 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/qtc",
    "inputs": {
      "qt": "420",
      "hr": "50",
      "formula": "2"
    },
    "expect": [
      "所用公式： Fridericia",
      "395.2"
    ],
    "ref": "D-N33：公式下拉选 2=Fridericia，RR=60÷50=1.2，QTc=420÷∛1.2=420÷1.062659=395.2 ms；旧实现忽略公式字段、恒输出 Bazett 447.2，且不含「Fridericia」标签 ⇒ 默认态零命中。"
  },
  {
    "slug": "healthcare/parkland",
    "inputs": {
      "weight": "42",
      "tbsa": "42",
      "hours": "42"
    },
    "expect": [
      "42\n42\n42\n24h 总量： 7056"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"tbsa\":\"42\",\"hours\":\"42\"}，输出区含「42\n42\n42\n24h 总量： 7056」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/resp-rate",
    "inputs": {
      "rr": "42",
      "age": "30",
      "state": "2"
    },
    "expect": [
      "运动后（不按静息分级）",
      "运动上限参考： 40"
    ],
    "ref": "运动态分支：state=2 时不按静息范围分级，仅给 40 次/分上限；默认 state=1 走静息分级，不含这两串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/water-intake",
    "inputs": {
      "weight": "42",
      "activity": "42",
      "climate": "42"
    },
    "expect": [
      "42\n42\n42\n推荐饮水量： 259308"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"weight\":\"42\",\"activity\":\"42\",\"climate\":\"42\"}，输出区含「42\n42\n42\n推荐饮水量： 259308」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/tdee-calculator",
    "inputs": {
      "age": "42",
      "height": "170",
      "weight": "42",
      "bf": "42",
      "act": "1.375"
    },
    "expect": [
      "量 (kcal) 77g 蛋白质 139g 碳水化合物 41"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"height\":\"42\",\"weight\":\"42\",\"bf\":\"42\",\"act\":\"1.375\"}，输出区含「量 (kcal) 77g 蛋白质 139g 碳水化合物 41」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "healthcare/weight-dosage",
    "inputs": {
      "weight": "42",
      "mgkg": "42",
      "freq": "8"
    },
    "expect": [
      "日剂量： 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入，日剂量 = 42×42 = 1764 mg/天（freq 取 8，满足 1–24 整数限界）。⚠ 03-48 在 freq 后插入 age/sex 输入 + refWeightBox 容器，原值序列锚「42\n42\n42\n日剂量： 1764」断链，改派生串「日剂量： 1764」（默认 20×10=200 不含）⇒ 强判别、零逃生。2026-11-16 freq 由 42 改为 8（D-N14 限界）。"
  },
  {
    "slug": "healthcare/weight-dosage",
    "inputs": {
      "weight": "18",
      "mgkg": "12",
      "freq": "3"
    },
    "expect": [
      "当前体重偏差 10%"
    ],
    "ref": "WHO P50 中位体重核对（03-48）：age 默认 4 岁/男 P50=16.3 kg，|18−16.3|÷16.3=10.4%→10%。默认 weight=20 偏差 23% ⇒ 随注入变化、零交集。"
  },
  {
    "slug": "healthcare/weight-dosage",
    "inputs": { "weight": "20", "mgkg": "10", "freq": "0.5" },
    "expect": ["每日次数须为 1–24 的整数"],
    "ref": "D-N14（2026-11-16）：freq=0.5 旧实现输出日剂量 200.0、单次 400.0（单次 > 日总量）。现要求 1≤freq≤24 且为整数，0.5 直接拦截；默认 freq=2 ⇒ 不命中。"
  },
  {
    "slug": "healthcare/weight-dosage",
    "inputs": { "weight": "20", "mgkg": "10", "freq": "100" },
    "expect": ["每日次数须为 1–24 的整数"],
    "ref": "D-N14 上界：freq=100 旧实现输出单次 2.0 mg 且不提示；现 1–24 限界。默认 2 ⇒ 不命中。"
  },
  {
    "slug": "healthcare/wells",
    "inputs": {
      "dvt": "42",
      "pe": "42",
      "hr": "42",
      "imm": "42",
      "dvt_hist": "42",
      "hem": "42",
      "cancer": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n评分： 525 分 临床概率： 高度"
    ],
    "ref": "自动补强（B类零用例，2026-10-25 权威权重修正后 3/3/1.5/1.5/1.5/1/1）：注入非默认输入（7 项全 42），评分=42×12.5=525 分 临床概率高度；默认态（全 0 → 0 分低度）不含该串 ⇒ 强判别、零逃生。"
  },
  { slug: "healthcare/apgar",
    inputs: { appearance: "", pulse: "", grimace: "", activity: "", respiration: "" },
    expect: ["请填写全部 Apgar 项目（0–2 分）后再判读。"],
    ref: "空态守卫：五项全清空后不再按 0 计算（旧实现 → 总分 0「重度窒息」），只输出填写提示。显式填 0 仍视为合法评分（0 分 = 重度窒息），故守卫按存在性判断而非「0 即无效」。默认态全 2 ⇒ 提示串不出现。" },
  { slug: "healthcare/chads-vasc",
    inputs: { c: "", h: "", a: "", d: "", s: "", v: "", age65: "", sex_f: "" },
    expect: ["请逐项填写危险因素分值（0/1/2）后再判读。"],
    ref: "空态守卫：八项全清空后旧实现按 0 计 → 评分 0「低危」；改为只输出填写提示。显式全填 0 仍判低危（合法）。默认态 h=1 ⇒ 评分 1「低中危」，提示串不出现。" },
  { slug: "healthcare/morse",
    inputs: { hist: "", sec_diag: "", aid: "", iv: "", gait: "", mental: "" },
    expect: ["请填写全部 Morse 跌倒评分项后再判读。"],
    ref: "空态守卫：六项全清空后旧实现按 0 计 → 总分 0「低风险」；改为只输出填写提示。显式全填 0 仍为 0 分（合法）。默认态 25/15/15/20/10/15=100「高风险」，提示串不出现。" },
  { slug: "healthcare/wells",
    inputs: { dvt: "", pe: "", hr: "", imm: "", dvt_hist: "", hem: "", cancer: "" },
    expect: ["请逐项填写 Wells 评分后再判读。"],
    ref: "空态守卫：七项全清空后旧实现按 0 计 → 评分 0「低度」；改为只输出填写提示。显式全填 0 仍判低度（合法）。默认态 1/1/1/1/1/0/0=7.5「高度」，提示串不出现。" },
  { slug: "healthcare/healthcare-5",
    inputs: { weight: "", activity: "", goal: "" },
    expect: ["请填写体重与活动系数（均需大于 0）后再判读。"],
    ref: "空态守卫：体重/活动系数/目标系数清空或为 0 时旧实现输出 0.0g（伪剂量）；改为范围提示。默认态 70/1.2/1.2 ⇒ 提示串不出现。" },
{
  "slug": "healthcare/heart-rate-zones",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/healthcare/heart-rate-zones.html','utf8');var i=h.indexOf('function calc(){');var seg=i>=0?h.slice(i,i+1200):'';var ok=seg.indexOf('__hrzClear')>=0&&seg.indexOf('isFinite(parseFloat(s))')>=0&&seg.indexOf('rhr>=maxHr')>=0&&seg.indexOf('lt<=rhr||lt>=maxHr')>=0&&seg.indexOf('|| 30')<0&&seg.indexOf('|| 65')<0&&seg.indexOf('|| 190')<0;document.getElementById('__tbProbe').textContent='HRZGUARD '+(ok?'OK':'BAD');})();"],
  "expect": ["HRZGUARD OK"],
  "ref": "第1307批·心率区间空值与倒置修复源码形态强锚：calc 须 rawNum 判空/isFinite、无 ||30/65/190 默认回退、rhr<maxHr、乳酸阈 lt 在(rhr,maxHr)之间，无效走 __hrzClear 清全部区间与评价。旧版四处 || 回退且无关系校验、lactate 法 maxHr190/lthr190 得 Z4 190-181 倒置 ⇒ BAD；真机交互由复核方覆盖。"
}
,
{
  "slug": "healthcare/bmr-calculator",
  "inputs": {
    "weight": "",
    "height": "",
    "age": "",
    "sex": ""
  },
  "expect": [
    "请填写体重、身高、年龄并选择性别"
  ],
  "ref": "全空时不得算出 -161 kcal/天（BMRCLR）；旧实现无守卫，性别空即走女性分支"
},
{
  "slug": "healthcare/ideal-weight",
  "inputs": {
    "sex": ""
  },
  "expect": [
    "请选择性别后再计算"
  ],
  "ref": "性别未选时不得静默按女性公式给理想体重（IWCLR）"
},
{ slug:"healthcare/bmi-2", inputs:{"age":"","bmi":"","sex":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"healthcare/due-date-calc", inputs:{"lmp":"","cycleLen":"","ovulationDay":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"healthcare/water-intake", inputs:{"weight":"","activity":"","climate":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
  {
    "slug": "healthcare/tdee-calculator",
    "inputs": {"age": "5", "height": "170", "weight": "65", "bf": "", "act": "1.375"},
    "expect": ["⚠ 年龄须在 10–120 岁，身高 100–250 cm，体重 20–300 kg；体脂率如填写须在 0–70%。"],
    "ref": "5 岁儿童被当作成人套 Mifflin 公式仍出 TDEE；新守卫应拒绝。默认 30/170/65 不含该提示。"
  },

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

  const stat = analysisReportCostGuideChecks();
  const staticFails = stat.filter((s) => !s.ok);
  for (const s of staticFails) console.log("❌ [static] " + s.name);

  console.log("==== healthcare calc " + pass + "/" + cases.length + " ====");
  if (staticFails.length) console.log("❌ static " + (stat.length - staticFails.length) + "/" + stat.length + " 未通过");
  if (fails.length || staticFails.length) process.exit(1);
}
if (require.main === module) main();