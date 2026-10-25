#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "gastroenterology/bilirubin-ratio",
  "inputs": {
    "tbil": "128",
    "dbil": "55"
  },
  "expect": [
    "直接胆红素比值35-60%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/calc-1",
  "inputs": {
    "biliUnit": "mgdl"
  },
  "expect": [
    "mgdl"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/capsule-endoscopy",
  "inputs": {
    "ingest": "08:00_X",
    "duodenum": "08:25",
    "cecum": "11:30",
    "excrete": "16:00"
  },
  "expect": [
    "00_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/cdai",
  "inputs": {
    "stool": "21",
    "pain": "10",
    "wellbeing": "7",
    "complications": "1",
    "loperamide": "0",
    "mass": "0",
    "hct": "35",
    "weight": "-5"
  },
  "expect": ["21\n10\n7\n1\n0\n0\n35\nfemale\n-5\n168 CDAI评分 轻度活动 疾病活动度 评分明细 稀便次数 21 × 2 = 42 腹痛评分 10 × 5 = 50 全身状况 7 × 7 = 49 并发症 1 × 20 = 20 止泻药 0 × 30 = 0 腹部包块 0 × 10 = 0 Hct偏差 2.0 × 6 = 12.0 体重偏差 -5% × 1 = -5.0 轻度活动期。考虑调整5-ASA剂量或加用局部治疗，营养支持，必要时使用布地奈德。"],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/child-pugh",
  "inputs": {
    "bilirubin": "53",
    "albumin": "30",
    "pt": "4",
    "inr": "1.7"
  },
  "expect": ["53\n30\n4\n1.7\n2\n2\n11 总分 C级 Child-Pugh分级 评分明细 总胆红素 53 μmol/L (＞51) → 3分 白蛋白 30 g/L (28-35) → 2分 PT延长 → 2分 腹水：中-大量（不易控制） → 2分 肝性脑病：III-IV级 → 2分 预后参考： 1年生存率≈45%，2年生存率≈35% 肝功能失代偿，禁忌大型手术。建议尽早评估肝移植指征，加强对症支持治疗。"],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/colonoscopy-polyp",
  "inputs": {
    "size": "12"
  },
  "expect": [
    "12"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/detector-7",
  "inputs": {
    "prior": "7"
  },
  "expect": [
    "既往治疗7次失败"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/ercp-success",
  "inputs": {
    "stoneSize": "18",
    "cbd": "12"
  },
  "expect": ["5 难度评分"],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/esophageal-varices",
  "inputs": {
    "size": "2"
  },
  "expect": [
    "中度(D2)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/gastric-emptying",
  "inputs": {
    "r2": "98",
    "r4": "30",
    "r0": "100",
    "halfTime": "90"
  },
  "expect": [
    "排空率2.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/gastrin-level",
  "inputs": {
    "gastrin": "225"
  },
  "expect": [
    "225"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/gastroscopy-atlas",
  "inputs": {
    "search": "zzzqx"
  },
  "expect": [
    "未找到匹配的条目"
  ],
  "ref": "关键词过滤型：inputs 写 search=zzzqx ⇒ oninput=filterAtlas() ⇒ renderAtlas() 得空集 ⇒ 「未找到匹配的条目」。默认态（search 空）渲染全量条目、blob 无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "gastroenterology/glasgow-pancreatitis",
  "inputs": {
    "age": "83",
    "wbc": "15",
    "glucose": "10",
    "ldh": "350",
    "ast": "200",
    "calcium": "2.0",
    "albumin": "32",
    "urea": "8",
    "pao2": "65"
  },
  "expect": [
    "83岁"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/hepatic-encephalopathy",
  "inputs": {
    "consciousness": "1"
  },
  "expect": ["1\n1\n1\n1\nⅠ级"],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/hp-dob",
  "inputs": {
    "dob": "12.5"
  },
  "expect": [
    "12.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/hp-resistance",
  "inputs": {
    "clarithro": "resistant"
  },
  "expect": ["bid/tid，14天（避开克拉霉素）"],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/ibd-nutrition",
  "inputs": {
    "bmi": "27.5",
    "weightLoss": "8",
    "albumin": "32",
    "age": "45"
  },
  "expect": [
    "27.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/intestinal-metaplasia",
  "inputs": {
    "antrumIM": "1"
  },
  "expect": ["1\n3\n2\n3\nⅡ期 OLGIM分期 Ⅲ期 OLGA分期 中度风险 胃癌风险 评估明细 胃窦肠化生：轻度 胃体肠化生：重度 胃窦萎缩：中度 胃体萎缩：重度 随访建议： 每1-2年随访胃镜 中度肠化生范围，胃癌风险升高。建议根除Hp后定期随访，增强筛查意识。"],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/mayo-score",
  "inputs": {
    "stool": "1"
  },
  "expect": [
    "2次/日"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/nafld-fibroscan",
  "inputs": {
    "lsm": "14.5",
    "cap": "310",
    "ast": "45",
    "plt": "180"
  },
  "expect": [
    "2)每6-12个月复查FibroScan监测进展"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/saag-ascites",
  "inputs": {
    "serumAlb": "42",
    "ascitesAlb": "12"
  },
  "expect": [
    "30.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": {
    "fit": "75",
    "age": "55",
    "fc": "120"
  },
  "expect": [
    "75"
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

  console.log("==== gastroenterology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
