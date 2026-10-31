#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "cardiology/ambulatory-bp",
  "inputs": {
    "avg24_sbp": "213",
    "avg24_dbp": "88",
    "day_sbp": "150",
    "day_dbp": "92",
    "night_sbp": "128",
    "night_dbp": "78",
    "lowest_sbp": "120",
    "morning_sbp": "165"
  },
  "expect": [
    "213/88"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/ambulatory-bp",
  "inputs": {
    "avg24_sbp": "148",
    "avg24_dbp": "86",
    "followDate": "2024-03-10"
  },
  "expect": [
    "随访计划（评估日 2024-03-10，24h平均 高血压）",
    "第3次随访：2024-06-08（评估后 90 天"
  ],
  "ref": "随访计划生成器（03-66）：avg24 148/86 ≥135/85 ⇒ 24h平均 高血压 ⇒ 日程 14/30/90/365 天。2024-03-10 +90 天 = 2024-06-08（3 月余 21 + 4 月 30 + 5 月 31 = 82，余 8 天 → 6/8；闰年 2/29 在起点前不影响）。默认 followDate 为空 ⇒ 日程块不渲染；discriminator 将 avg24_sbp 换回默认 142、followDate 换回空 ⇒ 两条锚零交集。日期对固定、与运行日无关（铁律④）。"
},
{
  "slug": "cardiology/antiarrhythmic-class",
  "clicks": [
    "showClass('4', {classList:{add:function(){},remove:function(){}}})"
  ],
  "expect": [
    "IV类",
    "钙通道阻滞剂"
  ],
  "ref": "clicks 直接调 showClass('4', 哑 classList)→IV类 非二氢吡啶类钙通道阻滞剂（维拉帕米/地尔硫䓬）。默认态为 I类（钠通道阻滞剂），故「IV类」可区分。"
},
{
  // 原用例 inputs 为空、expect 取「非复杂型Stanford B型」—— 那是建立在**旧 harness 失真**上的：
  // extent 组真机默认选中 ascDesc（HTML checked），旧桩 getElementsByName 恒 [] ⇒ getRadio 返回 0
  // ⇒ 被当成「非升主动脉受累」而落入 B 型。2026-09-24 起 harness 回落 HTML 默认选中态，
  // 真机默认（extent=ascDesc）实为 **A 型**（急诊外科手术），故原 expect 已不成立。
  // 现改为显式声明输入（不再受默认态影响）：extent=descOnly → B 型；malPerf=1 → 复杂型 →
  // 紧急 TEVAR（默认态 A 型输出「急诊外科手术」，故本 expect 具判别力）。
  "slug": "cardiology/aortic-dissection",
  "radios": {
    "extent": "descOnly"
  },
  "checkIds": [
    "malPerf"
  ],
  "expect": [
    "紧急TEVAR(腔内修复)",
    "复杂型Stanford B型夹层"
  ],
  "ref": "extent=descOnly（仅降主动脉）→ Stanford B 型 / DeBakey IIIa；malPerf=脏器灌注不良 → complicated → 紧急 TEVAR 腔内修复"
},
{
  "slug": "cardiology/aspirin-prevention",
  "inputs": {
    "age": "83",
    "ascvd": "12"
  },
  "expect": [
    "83岁"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例（空输入只能断言提示语，零判别力）。
  "slug": "cardiology/calc-1",
  "inputs": {
    "sbp": "150",
    "dbp": "95"
  },
  "checkIds": [
    "diabetes"
  ],
  "expect": [
    "1级高血压（轻度）",
    "高危 / 很高危"
  ],
  "ref": "classifyBP(150,95) → 1级高血压（轻度）（收缩压140-159 或 舒张压90-99）；riskLayer 见 diabetes=true → 「高危 / 很高危」（糖尿病/靶器官损害/确诊CVD 任一即高危）。回退默认（空输入）→ 仅提示「请输入有效的收缩压和舒张压」；不勾选 → 低危。两串均不命中。"
},
{
  "slug": "cardiology/calc-3",
  "inputs": {
    "age": "2"
  },
  "expect": [
    "2.2%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/cardiac-rehab-mets",
  "inputs": {
    "mets": "8",
    "weight": "70"
  },
  "expect": [
    "1960"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/chads2-vasc",
  "inputs": {
    "sex": "f"
  },
  "expect": ["f\n2\n3 CHA₂DS₂-VASc 总分 3.2% 卒中年风险 推荐OAC 抗凝建议 评分明细 年龄≥75岁 → +2 女性 → +1 总分 = 3 抗凝决策 推荐口服抗凝药(OAC)：华法林(INR 2–3)或DOAC(达比加群/利伐沙班/阿哌沙班/艾多沙班)。"],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/ckd-epi",
  "inputs": {
    "age": "98",
    "scr": "1.3",
    "uacr": "80"
  },
  "expect": [
    "ACEI/ARB/SGLT2i治疗"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/coronary-calcium",
  "inputs": {
    "age": "93",
    "cacs": "280"
  },
  "expect": [
    "50–75百分位"
  ],
  "ref": "注入 age=93/cacs=280：CACS=280 落 [100,400) → 中度钙化；年龄分位 50–75百分位（默认 age=62/cacs=280 同为中钙，但分位是 ≥75百分位 ⇒ 「50–75百分位」随注入变化、零交集）。原 expect「93岁」输入回显、「中度钙化」默认态同命中（cacs 默认恰为 280）均不可用。S3 参考区间标尺 refBar(#cacsRefBar) 已加（bands: 无/轻/中/广/重，max1500），harness 因 TBKit 守卫不渲染但文本定位已落 #result。"
},
{
  "slug": "cardiology/coronary-calcium",
  "inputs": {
    "sex": "m",
    "age": "55",
    "cacs": "50",
    "followDate": "2024-01-15"
  },
  "expect": [
    "随访计划（评估日 2024-01-15，轻度钙化）",
    "第1次随访：2027-01-14（评估后 1095 天"
  ],
  "ref": "随访计划生成器铺开五（03-73）：CACS=50 → 轻度钙化 → 1095 天复查；2024-01-15+1095 天（含 2024-02-29 闰日，366+365+365）= 2027-01-14。followDate 默认空 ⇒ 日程块不渲染，老用例零交集。"
},
{
  "slug": "cardiology/coronary-calcium",
  "inputs": {
    "sex": "f",
    "age": "70",
    "cacs": "600",
    "followDate": "2024-01-15"
  },
  "expect": [
    "随访计划（评估日 2024-01-15，广泛钙化）",
    "第1次随访：2025-01-14（评估后 365 天"
  ],
  "ref": "CACS=600 → 广泛钙化 → 365 天年度复查 + 冠脉 CTA 评估；2024-01-15+365 天（跨 2024-02-29）= 2025-01-14。"
},
{
  "slug": "cardiology/cpet-analysis",
  "inputs": {
    "peakVO2": "20.5",
    "at": "9.5",
    "veVco2": "34",
    "rer": "1.12",
    "pctPred": "58"
  },
  "expect": [ "20.5 峰值VO₂" ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/echo-report",
  "inputs": {
    "lvef": "72",
    "lvesv": "55",
    "lvidd": "56",
    "la": "42",
    "ao": "32",
    "rv": "22",
    "ea": "0.8",
    "eprime": "6"
  },
  "expect": [
    "72%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/grace-score",
  "inputs": {
    "age": "102",
    "hr": "95",
    "sbp": "130",
    "cr": "1.2"
  },
  "expect": ["+64 心率 95次/分"],
  "ref": "auto-restore"
},
{
  // radios 注入单选组（htn=1 高血压、stroke=1 卒中史），checkIds 注入复选（drugs 合并抗血小板/NSAIDs、
  // alcohol 酗酒）→ 1+1+1+1 = 4 分 → 高危、出血风险 8.70%。
  // 原用例 inputs 为空、expect 取默认态 "1.13%"（0 分低危）⇒ 零判别力，已去默认化。
  "slug": "cardiology/has-bled",
  "radios": {
    "htn": "1",
    "stroke": "1"
  },
  "checkIds": [
    "drugs",
    "alcohol"
  ],
  "expect": [
    "8.70%"
  ],
  "ref": "HAS-BLED 九项各 1 分：高血压 1 + 卒中史 1 + 合并抗血小板/NSAIDs 1 + 酗酒 1 = 4 分 → 高危（出血风险 8.70%）"
},
{
  "slug": "cardiology/holter-grading",
  "inputs": {
    "pvcTotal": "12750",
    "pvcHr": "520",
    "vtBeats": "0",
    "vtSec": "0"
  },
  "expect": [
    "12750/100000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/hypertension-jnc",
  "inputs": {
    "sbp": "233",
    "dbp": "95"
  },
  "expect": [
    "233/95"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/hypertension-jnc",
  "inputs": {
    "sbp": "145",
    "dbp": "92",
    "followDate": "2024-01-15"
  },
  "expect": [
    "随访计划（评估日 2024-01-15，中危）",
    "第2次随访：2024-04-14（评估后 90 天"
  ],
  "ref": "随访计划生成器（03-65）：sbp=145→2级、dbp=92→2级 ⇒ 1级高血压；无危险因素/TOD/ACC（默认未勾选）⇒ 中危（grade≥2 分支）。中危日程 30/90 天：2024-01-15 +30 天 = 2024-02-14（闰年 2 月 29 天不影响）、+90 天 = 2024-04-14（16+29+31=76 天到 3 月底，余 14 天 → 4/14）。默认 followDate 为空 ⇒ 日程块不渲染，两条锚均随注入出现、零交集；日期对固定、与运行日无关（铁律④）。"
},
{
  "slug": "cardiology/myocardial-bridge",
  "inputs": {
    "compression": "98",
    "diastolic": "10",
    "length": "25",
    "depth": "3"
  },
  "expect": [
    "98%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/nt-probnp",
  "inputs": {
    "age": "108",
    "ntprobnp": "1850"
  },
  "expect": [
    "NT-proBNP≥1800 pg/mL(>75岁截断值)",
    "NT-proBNP 1850 pg/mL → 落在 纳入区（>75岁，纳入截断 1800 pg/mL）"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/nyha-classification",
  "inputs": {
    "walk": "480"
  },
  "expect": [
    "480米"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/pericardial-effusion",
  "inputs": {
    "depth": "33"
  },
  "expect": [
    "2000mL"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/rater-risk-3",
  "inputs": {
    "age": "98",
    "hr": "80",
    "sbp": "130",
    "cr": "1.0"
  },
  "expect": [
    "114"
  ],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/statin-dose",
  "inputs": {
    "ldl": "6.8"
  },
  "expect": ["6.8\n1.8\n6.8 当前 LDL-C 1.8 目标 LDL-C 73.5% 所需降幅 高强度 他汀强度 计算过程 当前LDL-C = 6.8 mmol/L 目标LDL-C = 1.8 mmol/L 所需降幅 = (6.8−1.8)/6.8×100% = 73.5% 预计达标后LDL-C = 1.80 mmol/L 他汀强度等级： 高强度 联合用药建议 单药最大降幅可能不足，建议联合治疗 高强度他汀(最大降幅~55%) + 依折麦布(额外~20%) 联合后预期降幅：~64% 联合仍不达标：加用PCSK9抑制剂(额外降50–60%) 需联合用药 单药最大他汀可能无法达标，建议联合依折麦布和PCSK9抑制剂。"],
  "ref": "auto-restore"
},
{
  "slug": "cardiology/timi-score",
  "inputs": {
    "s_age": "2"
  },
  "expect": [
    "2/14"
  ],
  "ref": "auto-restore"
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

  console.log("==== cardiology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
