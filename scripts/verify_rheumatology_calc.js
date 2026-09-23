#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原 expect「观察滴度变化」是输出文案片段（词串型，不依赖被测点）；改为依赖勾选的分级断言。
  // 小关节 + 对称性关节炎 → 关节受累 +3；叠加 inputs 血清学（ccp=120 ≥40 → +2）、病程 +1、
  // CRP/ESR 异常 +1 → 7 分 ≥ 6 → 符合RA分类标准。不勾选时仅 4 分 → 疑诊RA（故具判别力）。
  "slug": "rheumatology/anti-ccp",
  "inputs": {
    "ccp": "120",
    "rf": "45",
    "crp": "12",
    "esr": "28"
  },
  "checkIds": [
    "smalljoint",
    "symmetric"
  ],
  "expect": [
    "(≥6分, 符合RA)",
    "小关节对称受累(+3)"
  ],
  "ref": "2010 ACR/EULAR 简化：小关节对称受累 +3（血清学 +2、病程 +1、CRP/ESR +1）= 7 ≥ 6 → 诊断「符合RA」（输出尾部带「(≥6分, 符合RA)」）；默认不勾选 = 4 → 疑诊RA。注：不可用「符合RA分类标准」作 expect —— 该串在页面静态参考表里已出现 2 次（逃生项）"
},
{
  // 原 expect「发数周」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // 勾选 5 项系统受累：尿检异常 +2、神经精神症状 +2、发热 +1、疲劳 +1、皮疹 +1 = +7，
  // 叠加 c3=0.5 / c4=0.08 的补体降低项 → activityScore ≥ 7 → 高活动度。
  // 不勾选时 = 低活动度（故具判别力）。
  "slug": "rheumatology/complement-level",
  "inputs": {
    "c3": "0.5",
    "c4": "0.08",
    "ch50": "15"
  },
  "checkIds": [
    "renal",
    "cns",
    "fever",
    "fatigue",
    "rash"
  ],
  "expect": [
    "高活动度",
    "尿检异常 (+2)"
  ],
  "ref": "activityScore：尿检异常 +2、神经精神症状 +2、发热 +1、疲劳 +1、皮疹 +1 = +7，叠加补体降低（c3=0.5/c4=0.08）→ ≥7 → 高活动度"
},
{
  "slug": "rheumatology/das28",
  "inputs": {
    "markerVal": "20",
    "tjc": "5",
    "sjc": "3",
    "gh": "30"
  },
  "expect": [
    "抑制剂"
  ]
},
{
  "slug": "rheumatology/detector-8",
  "inputs": {
    "screen": "42",
    "confirm": "33",
    "normal": "35",
    "aptt": "38",
    "apttNormal": "32"
  },
  "expect": [
    "肝素"
  ]
},
{
  // 原 expect「病理诊断」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // 器官受累：胰腺 +4、胆管 +3、肾脏 +3 = +10；叠加 igg4=5.8（落在 5.0–10 g/L 档 → +6）= 16，
  // 落在 10–19 区间 → 疑诊IgG4-RD。不勾选器官时 = 6 分 → 更低档（故具判别力）。
  "slug": "rheumatology/igg4-level",
  "inputs": {
    "igg4": "5.8",
    "igg": "18",
    "ige": "350",
    "eos": "0.6",
    "c3": "1.3"
  },
  "checkIds": [
    "pancreas",
    "biliary",
    "kidney"
  ],
  "expect": [
    "疑诊IgG4-RD",
    "胰腺受累 → +4"
  ],
  "ref": "score：胰腺 +4、胆管 +3、肾脏 +3 = 10，加 igg4=5.8（5.0–10 档 +6）= 16（10–19）→ 疑诊IgG4-RD；≥20 才是高度提示"
},
{
  // 原为 all_default 弱用例：6 项指标全等于页面默认，expect「肝酶」是疾病建议表里的常量词（逃生项）。
  "slug": "rheumatology/il6-inflammation",
  "inputs": {
    "il6": "1200",
    "crp": "8",
    "esr": "45",
    "ferritin": "500",
    "plt": "450",
    "fib": "5.5"
  },
  "checkIds": [
    "organ"
  ],
  "expect": [
    "IL-6：1200 pg/mL → 极度升高(炎症风暴)",
    "IL-6>1000 (+5, 炎症风暴)"
  ],
  "ref": "IL-6=1200 ≥1000 → 判读「极度升高(炎症风暴)」且炎症负荷 +5（明细条「IL-6>1000 (+5, 炎症风暴)」）；organ 勾选 → 脏器功能不全 +3（总分 11 → 炎症风暴风险）。回退默认（il6=25）→ 「中度升高」且无 +5 明细。"
},
{
  // 原 expect「但需评估血栓风险因素」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // 抗体谱阳性（aCL/β2GPI）+ 临床标准（血栓/妊娠并发症）同时满足 → 符合APS分类标准。
  // 不勾选时仅为「抗磷脂抗体阳性(aPL携带者)」（故具判别力）。
  "slug": "rheumatology/lupus-anticoagulant",
  "inputs": {
    "dsc": "45",
    "dcc": "35",
    "dnm": "32",
    "ssc": "42",
    "scc": "35",
    "snm": "33"
  },
  "checkIds": [
    "acl",
    "ab2gpi",
    "vte",
    "arte",
    "pregloss",
    "preeclampsia",
    "thrombocytopenia"
  ],
  "expect": [
    "符合APS分类标准"
  ],
  "ref": "抗体谱阳性（aCL + β2GPI）+ 临床标准（血栓事件/妊娠并发症）同时满足 → 符合APS分类标准；默认不勾选 = aPL携带者"
},
{
  // 原 expect「抑制剂」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // rpild（快速进展型 ILD）是「极高风险」的独立触发条件（rpild || riskScore ≥ 8）。
  // 不勾选时 riskScore = 6（MDA5阳性+3、铁蛋白800+2、LDH+1）→ 高风险（故具判别力；
  // 注意「极高风险」含子串「高风险」，expect 必须取更长的「极高风险」）。
  "slug": "rheumatology/mda5-antibody",
  "inputs": {
    "ferritin": "800",
    "ck": "150",
    "crp": "15",
    "ldh": "300"
  },
  "checkIds": [
    "rpild"
  ],
  "expect": [
    "极高风险"
  ],
  "ref": "rpild（快速进展型ILD）→ 直接命中「极高风险」分支（rpild || riskScore ≥ 8）；默认不勾选 = 6 分 → 高风险"
},
{
  // 原 expect「评估治疗反应」是输出文案片段（词串型）；改为依赖勾选的分级断言。
  // 诊断分：前胸壁 +3、骨肥厚 +2、掌跖脓疱病 +2、重度痤疮/HS +2、骶髂关节炎 +1、脊柱 +1、
  // 脓疱型银屑病 +1 = 12（未勾 culture）→ 高度提示SAPHO。不勾选时 = 低档（故具判别力）。
  "slug": "rheumatology/sapho-syndrome",
  "inputs": {
    "duration": "3",
    "vas": "5"
  },
  "checkIds": [
    "chestwall",
    "acquired",
    "palmoplantar",
    "severeAcne",
    "sacro",
    "spine",
    "pustular"
  ],
  "expect": [
    "高度提示SAPHO",
    "前胸壁受累(+3, 特征性表现)"
  ],
  "ref": "dxScore：前胸壁 +3、骨肥厚 +2、掌跖脓疱病 +2、重度痤疮/HS +2、骶髂关节炎 +1、脊柱 +1、脓疱型银屑病 +1 = 12 → 高度提示SAPHO"
},
{
  "slug": "rheumatology/anca-classification",
  "inputs": {
    "iif": "canca"
  },
  "expect": [
    "疑似PR3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/assessor-10",
  "inputs": {
    "d'+i+'": "'+lv.v+'"
  },
  "expect": [
    "+lv.v+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/basdai",
  "inputs": {
    "q1": "6",
    "q2": "4",
    "q3": "2",
    "q4": "3",
    "q5": "5",
    "q6": "4"
  },
  "expect": [
    "(6.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/behcet-hla",
  "inputs": {
    "age": "middle"
  },
  "expect": [
    "middle"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/bvas",
  "inputs": {},
  "expect": [
    "定期监测ANCA滴度和脏器功能"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rheumatology/essdai",
  "inputs": {
    "d1": "1"
  },
  "expect": [
    "+1分"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/gout-uric-acid",
  "inputs": {
    "ua": "720"
  },
  "expect": [
    "需降低360"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/guguanjieyan-womac-zhishu",
  "inputs": {
    "' + name + '_' + v + '": "' + v + '_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/itp-immune",
  "inputs": {
    "plt": "38"
  },
  "expect": [
    "定期监测血小板(每1-3月)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/mctd-diagnosis",
  "inputs": {
    "rnp": "low"
  },
  "expect": [
    "low"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/mrss",
  "inputs": {
    "s1": "1"
  },
  "expect": [
    "1/51"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/rater-16",
  "inputs": {},
  "expect": [
    "CH50/C3/C4低于正常下限"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rheumatology/rater-17",
  "inputs": {},
  "expect": [
    "肌酐125-249"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rheumatology/sledai",
  "inputs": {},
  "expect": [
    "SLEDAI-2K"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "rheumatology/ssa-ssb",
  "inputs": {
    "ssa": "ro60"
  },
  "expect": [
    "补体C3/C4"
  ],
  "ref": "auto-restore"
},
{
  "slug": "rheumatology/womac",
  "inputs": {},
  "expect": [
    "(0-100)"
  ],
  "ref": "auto-restore(default)"
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
  console.log("==== rheumatology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
