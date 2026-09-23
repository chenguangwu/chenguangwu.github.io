#!/usr/bin node
"use strict";
// 第十七批（pulmonology）弱用例去默认化：
// 全部用例采用「非默认输入 + 独立复算 expect」，expect 必须依赖被测点的计算结果，
// 不得取页面源码字面量或输入值回显（注入失败时用例必须 FAIL）。
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 默认 wt=55/age=45 → 风险因素「年龄≥35」→ 中危；注入 wt=40/age=30 → 无风险因素 → 低危
  "slug": "pulmonology/anti-tb-dosing",
  "inputs": {
    "wt": "40",
    "age": "30"
  },
  "expect": [
    "风险因素：无"
  ],
  "ref": "auto-restore"
},
{
  // 默认 pao2=80/fio2=40 → P/F=200 重度 ARDS；注入 90/21 → P/F=429 → 氧合功能正常
  "slug": "pulmonology/calc-48",
  "inputs": {
    "pao2": "90",
    "fio2": "21"
  },
  "expect": [
    "氧合功能正常，无需特殊氧疗支持。"
  ],
  "ref": "auto-restore"
},
{
  // 默认 2.1/3.5 → 比值 60.0% 阻塞；注入 3.0/3.5 → 85.7% ≥0.70 → 无阻塞
  "slug": "pulmonology/feigongneng-fev1-fvc-fenji",
  "inputs": {
    "fev1": "3.0",
    "fvc": "3.5",
    "fev1pred": "3.0",
    "fvcpred": "2.0",
    "age": "40"
  },
  "expect": [
    "FEV1/FVC = 0.857 ≥ 0.70，无阻塞性通气障碍。"
  ],
  "ref": "auto-restore"
},
{
  // 默认 42/65/320/200 → 渗出液；注入 20/65/100/200 → 三项均不达标 → 漏出液
  "slug": "pulmonology/light-criteria",
  "inputs": {
    "pfProt": "20",
    "sProt": "65",
    "pfLdh": "100",
    "sLdh": "200",
    "sLdhUl": "250"
  },
  "expect": [
    "结论：漏出液"
  ],
  "ref": "auto-restore"
},
{
  // 默认 copd/8/60 → 480 mL；注入 cardiac/10/70 → 700 mL
  "slug": "pulmonology/niv-settings",
  "inputs": {
    "indication": "cardiac",
    "vt": "10",
    "ibw": "70",
    "ph": "7.30"
  },
  "expect": [
    "目标潮气量 = 10 mL/kg × 70 kg = 700 mL"
  ],
  "ref": "auto-restore"
},
{
  // 默认 65/40 → P/F=163；注入 90/30 → P/F=300（PEEP 复选框 harness 不可注入，故以 P/F 明细判读）
  "slug": "pulmonology/oxygenation-index",
  "inputs": {
    "pao2": "90",
    "fio2": "30",
    "spo2": "95"
  },
  "expect": [
    "P/F = 90 / 0.30 = 300"
  ],
  "ref": "auto-restore"
},
{
  // 默认 a/b/c=2/3/2 → 23% 中大量；注入 1/1/1 → 10% 少量且无症状
  "slug": "pulmonology/pneumothorax",
  "inputs": {
    "a": "1",
    "b": "1",
    "c": "1"
  },
  "expect": [
    "压缩＜20%且无症状，可观察吸氧"
  ],
  "ref": "auto-restore"
},
{
  // 默认 2.10/3.50 → 60.0% 阻塞 GOLD 2；注入 3.0/3.5/95/95 → 85.7% 正常
  "slug": "pulmonology/pulmonary-function",
  "inputs": {
    "fev1": "3.0",
    "fvc": "3.5",
    "fev1pp": "95",
    "fvcpp": "95",
    "cutoff": "0.70"
  },
  "expect": [
    "通气功能正常，未见阻塞性或限制性通气障碍。"
  ],
  "ref": "auto-restore"
},
{
  // 默认 mip=45 → 高于下限 43（正常）；注入 mip=30 → 吸气肌无力
  "slug": "pulmonology/pulmonary-rehab",
  "inputs": {
    "mip": "30",
    "mep": "30",
    "age": "65"
  },
  "expect": [
    "吸气肌无力"
  ],
  "ref": "auto-restore"
},
{
  // 默认 pao2=55/paco2=62 → II型呼衰；注入 80/40 → 未达呼衰标准
  "slug": "pulmonology/respiratory-failure",
  "inputs": {
    "pao2": "80",
    "paco2": "40",
    "fio2": "21",
    "age": "65"
  },
  "expect": [
    "无低氧性呼衰"
  ],
  "ref": "auto-restore"
},
  // 注：pulmonology/analysis-14 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  // 默认 tumorType=0 → 0级原位/表浅；注入 3 → 3级浸润型
  "slug": "pulmonology/bronchoscopy-grading",
  "inputs": {
    "tumorType": "3"
  },
  "expect": [
    "提示浸润性癌，评估分期，可能需放化疗/手术"
  ],
  "ref": "auto-restore"
},
{
  // 8 题（q0-q7）每题 0-5；注入全 5 → 总分 40 → 极重度影响
  "slug": "pulmonology/copd-cat",
  "inputs": {
    "q0": "5",
    "q1": "5",
    "q2": "5",
    "q3": "5",
    "q4": "5",
    "q5": "5",
    "q6": "5",
    "q7": "5"
  },
  "expect": [
    "影响极重，多学科综合管理"
  ],
  "ref": "auto-restore"
},
{
  // 勾选 C(意识模糊)+U(尿素氮>7) → CURB-65 = 2 分 → 中危、30天死亡风险约 9.2%、建议住院。
  // 默认态 0 分 → 低危（约1.5%）/门诊治疗，故本 expect 具判别力。
  // checkIds 注入复选框选中态（页面用 getElementById(id).checked 读取，见 harness 2026-09-24 升级）。
  "slug": "pulmonology/curb65",
  "checkIds": [
    "c",
    "u"
  ],
  "expect": [
    "中(约9.2%)",
    "住院治疗"
  ],
  "ref": "CURB-65 五项各 1 分：C(意识模糊)+U(尿素氮>7)=2 → 中危（30天死亡风险约 9.2%）→ 住院治疗"
},
{
  // ACT 五项 a1-a5 各 1-5；注入全 4 → 总分 20 → 良好控制
  "slug": "pulmonology/gina-asthma",
  "inputs": {
    "a1": "4",
    "a2": "4",
    "a3": "4",
    "a4": "4",
    "a5": "4"
  },
  "expect": [
    "20/25 ACT总分 良好控制"
  ],
  "ref": "auto-restore"
},
{
  // 默认 T1a → ⅠA1期；注入 T2a/N0/M0 → ⅠB期
  "slug": "pulmonology/lung-cancer-tnm",
  "inputs": {
    "t": "T2a",
    "n": "N0",
    "m": "M0"
  },
  "expect": [
    "分期 = ⅠB期"
  ],
  "ref": "auto-restore"
},
{
  // 默认 size=9 → 4A（3个月复查）；注入 size=5 → 2 类（年度复查）
  "slug": "pulmonology/lung-rads",
  "inputs": {
    "type": "solid",
    "size": "5"
  },
  "expect": [
    "Lung-RADS 2 年度低剂量CT复查。"
  ],
  "ref": "auto-restore"
},
{
  // Wells 7 项（q0-q6，动态 id）注入全「是」→ 3+3+1.5+1.5+1.5+1+1 = 12.5 → 高风险
  "slug": "pulmonology/rater-13",
  "inputs": {
    "q0": "1",
    "q1": "1",
    "q2": "1",
    "q3": "1",
    "q4": "1",
    "q5": "1",
    "q6": "1"
  },
  "expect": [
    "PE概率约 49.9%"
  ],
  "ref": "auto-restore"
},
{
  // FTND 6 题（q0-q5，动态 id）注入 3/1/1/3/1/1 → 总分 10 → 极高依赖
  "slug": "pulmonology/self-assess-3",
  "inputs": {
    "q0": "3",
    "q1": "1",
    "q2": "1",
    "q3": "3",
    "q4": "1",
    "q5": "1"
  },
  "expect": [
    "尼古丁依赖程度极高，生理依赖严重，自行戒烟极困难，需专业医疗干预。"
  ],
  "ref": "auto-restore"
},
{
  // q1-q6 注入全 0 → 总分 0 → 轻度依赖（默认组合为 7 分重度依赖）
  "slug": "pulmonology/smoking-cessation",
  "inputs": {
    "q1": "0",
    "q2": "0",
    "q3": "0",
    "q4": "0",
    "q5": "0",
    "q6": "0"
  },
  "expect": [
    "依赖程度轻。以行为干预为主(识别触发情境、延迟技巧)"
  ],
  "ref": "auto-restore"
},
{
  // 默认 char=浆液性 → 无警示；注入 bloody → 血性痰警示
  "slug": "pulmonology/sputum-analysis",
  "inputs": {
    "char": "bloody"
  },
  "expect": [
    "血性痰需排查肺结核、肺癌、支扩"
  ],
  "ref": "auto-restore"
},
{
  // 勾选 S/T/O/P/BMI 共 5 项 → 5/8 → 高危（强烈建议 PSG）。
  // 原用例 inputs 为空、expect 取默认态输出 "0/8"（注入失败亦命中）⇒ 零判别力，已去默认化。
  "slug": "pulmonology/stop-bang",
  "checkIds": [
    "s",
    "t",
    "o",
    "p",
    "bmi"
  ],
  "expect": [
    "5/8"
  ],
  "ref": "STOP-BANG 八项各 1 分：S(打鼾)+T(疲倦)+O(呼吸暂停)+P(高血压)+BMI>35 = 5 → 5/8 → 高危"
},
{
  // 默认（harness 首选项）smear=neg → 传染性低；注入 3+/pos/rif_s → 有传染性需隔离
  "slug": "pulmonology/tb-resistance",
  "inputs": {
    "smear": "3+",
    "culture": "pos",
    "xpert": "rif_s"
  },
  "expect": [
    "有传染性，需呼吸道隔离"
  ],
  "ref": "auto-restore"
},
{
  // 默认 rul_ap → 右上叶尖段（叩击同侧肩胛上方）；注入 rml → 右中叶（叩击右侧乳头下方）
  "slug": "pulmonology/vibration-percussion",
  "inputs": {
    "lobe": "rml"
  },
  "expect": [
    "叩击右侧乳头下方区域"
  ],
  "ref": "auto-restore"
},
{
  // 勾选 DVT(3)+其他诊断(3)+心率>100(1.5) → 7.5 分 > 6 → 高危（概率约 37.5%，直接 CTPA）。
  // 原用例 inputs 为空、expect 取默认态 "1.3%)"（0 分低危）⇒ 零判别力，已去默认化。
  "slug": "pulmonology/wells-pe",
  "checkIds": [
    "dvt",
    "alt",
    "hr"
  ],
  "expect": [
    "37.5%"
  ],
  "ref": "Wells PE 加权：DVT 3 + 其他诊断可能 3 + 心率>100 1.5 = 7.5 > 6 → 高危（～37.5%）"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== pulmonology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
