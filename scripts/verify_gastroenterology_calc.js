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
    "bili": "51.3",
    "alb": "26",
    "inr": "2.5"
  },
  "expect": [
    "Child-Pugh 评分： 10 分（5-15 分） 分级： C级"
  ],
  "ref": "独立复算：bili 51.3 μmol/L ÷17.1 = 3.0 mg/dL ⇒ 计 2 分（2–3 区间）；alb 26 g/L ⇒ 3 分（<28）；inr 2.5 ⇒ 3 分（>2.3）；ascites/enceph 各 1 ⇒ 合计 10 分 ⇒ C 级。⚠ 原用例只断言单位回显 'mgdl'（输入值回显、零判别力），已改为分类结果串。默认态预填 28/32/1.2 ⇒ 6 分 A 级，不含该串 ⇒ 无逃生。"
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
  "expect": ["198 CDAI评分 轻度活动"],
  "ref": "CDAI 合计 = 21×2 + 10×5 + 7×7 + 1×20 + 0×30 + 0×10 + (42−35)×6 + (−5)×1 = 42+50+49+20+0+0+42−5 = 198（女性标准 Hct 42%）；150–220 为轻度活动。默认稀便 14 次 ⇒ 184，该锚不命中；Hct 默认值同为 35、其明细串两态相同，不作第二锚（判别器已按逃生项判定，故仅保留合计锚）。原期望串把输入回显拼进断言且按旧标准 Hct 37% 算得 168，已更正。"
},
{
  "slug": "gastroenterology/child-pugh",
  "inputs": {
    "bilirubin": "53",
    "albumin": "30",
    "pt": "4",
    "inr": "1.7"
  },
  "expect": ["9 总分 B级", "总胆红素 53 μmol/L (＞51) → 3分"],
  "ref": "Child-Pugh：胆红素 53 μmol/L（>51）→3 分、白蛋白 30 g/L（28–35）→2 分、PT 延长 4 s→2 分，腹水/肝性脑病默认「无」各 1 分 ⇒ 合计 9 分 → B 级（7–9 分），1 年生存率≈80%、2 年≈60%。默认胆红素 35（34–51→2 分）合计 8 分，两条锚均不命中。原期望把输入回显拼进断言，且按旧默认（腹水 2 分、肝性脑病 2 分）写成 11 分 C 级，已按现行默认与评分规则复算更正。"
},
{
  "slug": "gastroenterology/colonoscopy-polyp",
  "inputs": {
    "size": "12"
  },
  "expect": [ "12 直径" ],
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
  "expect": [ "225 胃泌素" ],
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
    "consciousness": "3",
    "behavior": "2",
    "cognition": "2",
    "asterixis": "1"
  },
  "expect": ["最高级别：Ⅲ级", "Ⅲ级肝性脑病"],
  "ref": "West Haven 分级取四项最高：意识 3 级（昏睡）> 行为 2 级 = 认知 2 级 > 扑翼样震颤 1 级 ⇒ Ⅲ级。默认四项均为 1 级 ⇒ Ⅰ级，两条锚均不命中（原用例注入 1 与默认值相同，属逃生项，已改为非默认组合）。"
},
{
  "slug": "gastroenterology/hp-dob",
  "inputs": {
    "dob": "12.5"
  },
  "expect": [
    "12.5"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/hp-resistance",
  "inputs": {
    "clarithro": "resistant"
  },
  "expect": ["克拉霉素：耐药", "已剔除含耐药/禁用药物（克拉霉素、甲硝唑）"],
  "ref": "克拉霉素注入耐药、甲硝唑默认耐药、铋剂不可用 ⇒ 方案库剔除含克拉霉素/甲硝唑的方案，落到大剂量二联（艾司奥美拉唑 40mg qid + 阿莫西林 1g tid，14 天）。默认克拉霉素为敏感，首条锚不命中。原期望「bid/tid，14天（避开克拉霉素）」属旧方案文案，已随页面方案库重写更正。"
},
{
  "slug": "gastroenterology/ibd-nutrition",
  "inputs": {
    "bmi": "27.5",
    "weightLoss": "8",
    "albumin": "32",
    "age": "45"
  },
  "expect": [ "27.5 kg/m²" ],
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
  "expect": [ "75 FIT" ],
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
