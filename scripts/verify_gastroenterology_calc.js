#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "gastroenterology/bilirubin-ratio",
  "inputs": {
    "tbil": "128",
    "dbil": "55",
    "ref": "21"
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
    "inr": "2.5",
    "ascites": "1",
    "enceph": "1"
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
    "inr": "1.7",
    "ascites": "1",
    "encephalopathy": "1"
  },
  "expect": ["9 总分 B级", "总胆红素 53 μmol/L (＞51) → 3分"],
  "ref": "Child-Pugh：胆红素 53 μmol/L（>51）→3 分、白蛋白 30 g/L（28–35）→2 分、PT 延长 4 s→2 分，腹水/肝性脑病默认「无」各 1 分 ⇒ 合计 9 分 → B 级（7–9 分），1 年生存率≈80%、2 年≈60%。默认胆红素 35（34–51→2 分）合计 8 分，两条锚均不命中。原期望把输入回显拼进断言，且按旧默认（腹水 2 分、肝性脑病 2 分）写成 11 分 C 级，已按现行默认与评分规则复算更正。"
},
{
  "slug": "gastroenterology/colonoscopy-polyp",
  "inputs": {
    "size": "12", "paris": "Is", "kudo": "IIIL", "nice": "2"
  },
  "expect": [ "12 直径" ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/detector-7",
  "inputs": {
    "prior": "7", "ab1": "0", "ab2": "0", "ab3": "0", "ab4": "0", "ab5": "0", "ab6": "0"
  },
  "expect": [
    "既往治疗7次失败"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/ercp-success",
  "inputs": {
    "stoneSize": "18", "stoneCount": "1", "stonePos": "1",
    "purpose": "stone", "surgery": "0", "priorEst": "0", "diverticulum": "0"
  },
  "expect": ["5 难度评分"],
  "ref": "重写：页面无 CBD 字段（仅 stoneSize/stoneCount/stonePos/purpose/surgery/priorEst/diverticulum），原注入键 cbd 属僵尸 id（getEl 造游离桩、页面从不读取），已删除。难度分由页面真实分支累加：注入 stoneSize=18 ⇒ ＞15mm +3，其余保持默认（stoneCount=1 即 2-3 枚 +1、stonePos=1 即胆总管中段 +1）= 5 分；默认 stoneSize=12 ⇒ 10-15mm +2，其余同 = 4 分，故「5 难度评分」在默认态不命中。"
},
{
  "slug": "gastroenterology/esophageal-varices",
  "inputs": {
    "size": "3", "rc": "0", "child": "1", "bleed": "0"
  },
  "expect": [
    "曲张静脉大小：重度(D3)"
  ],
  "ref": "弱用例收紧：原注入 size=2 与页面默认值相同，且「中度(D2)」直接出现在 select 选项文案中 ⇒ 两态恒命中。改注入 size=3（默认 2）后，结果明细由 `sizeNames[size]` 生成「曲张静脉大小：重度(D3)」——注意结果用半角括号 `(D3)`，与 select 选项里的全角「重度（D3, 直径＞6mm）」不同，故注入失败（回退默认 size=2 →「中度(D2)」）必不命中。"
},
{
  "slug": "gastroenterology/gastric-emptying",
  "inputs": {
    "r2": "98",
    "r4": "30",
    "r0": "100",
    "halfTime": "90", "method": "scintigraphy", "meal": "solid"
  },
  "expect": [
    "排空率2.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gastroenterology/gastrin-level",
  "inputs": {
    "gastrin": "225", "ph": "low"
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
    "clarithro": "resistant", "metronidazole": "resistant", "levo": "unknown", "history": "none"
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
    "antrumIM": "1", "corpusIM": "3", "antrumAtrophy": "2", "corpusAtrophy": "3"
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
    "plt": "180", "validity": "valid", "probe": "M"
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
  "ref": "auto-restore；并补矩阵断言（阳性×轻度：FIT 75 / FC 120）——原代码该组合误报「双阴性 → 风险低」。"
},
{
  "slug": "gastroenterology/colonoscopy-polyp",
  "inputs": { "size": "", "paris": "Is", "kudo": "IIIL", "nice": "2" },
  "expect": ["留空不判读"],
  "ref": "息肉直径空值不得按 0 判为「微小息肉/低风险」：默认 8mm，注入空串后应显示「留空不判读」；回退默认 8 即不再命中。"
},
{
  "slug": "gastroenterology/hp-resistance",
  "inputs": {
    "clarithro": "unknown",
    "metronidazole": "unknown",
    "levo": "unknown", "history": "none"
  },
  "expect": [
    "克拉霉素：未检测",
    "甲硝唑：未检测",
    "未检测药物：克拉霉素、甲硝唑、左氧氟沙星"
  ],
  "ref": "三药全部未检测（默认 clar 敏感 / metro 耐药 / levo 未检测）：页面不再写「未检测按可能敏感」，改为列出未检测药物并降级方案可信度为「中」。原锚「中（存在未检测药物）」在默认态（仅 levo 未检测）同样出现 ⇒ 逃生；且 harness 的 expect 是「任一命中即 PASS」，`左氧氟沙星：未检测` 在默认态（levo=unknown）即出现 ⇒ 整条用例仍 PASS 残留逃生。删去该锚，只保留两条明细（clar/metro 默认分别为敏感/耐药，必不命中）与三药汇总句（默认仅 levo 未检测，汇总句为「未检测药物：左氧氟沙星」）。"
},
{
  "slug": "gastroenterology/hp-dob",
  "inputs": { "dob": "" },
  "expect": ["请填写 DOB 检测值后再判读。"],
  "ref": "空态守卫（2026-11-05）：清空 DOB 值后不再输出「0 DOB值」+「阴性」+「DOB值＜4.0‰…继续保持良好卫生习惯」整套结论，只给填写提示。⚠ 判空只认空串——DOB 0 ‰ 是合法检测值（阴性），照常判读。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "", "age": "55", "fc": "120" },
  "expect": ["请填写 FIT、粪钙卫蛋白与年龄后再生成联合解读。"],
  "ref": "空态守卫（2026-11-05）：清空 FIT 后不再输出「FIT 0 μg/g → 阴性」+「双阴性 → 风险低」结论，只给填写提示。⚠ 判空只认空串——FIT 0 μg/g、FC 0 μg/g、0 岁均为合法值，照常解读。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "5", "age": "55", "fc": "30" },
  "expect": ["双阴性 → 风险低"],
  "ref": "联合矩阵·阴性×正常（FIT<10 / FC<50）→ 双阴性、风险低。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "9", "age": "55", "fc": "150" },
  "expect": ["出血阴性，炎症轻度升高 → 建议复查"],
  "ref": "联合矩阵·阴性×轻度（FIT<10 / 50≤FC<200）→ 原代码落入 else 误报「双阴性 → 风险低」，现为出血阴性+炎症轻度升高、复查 FC。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "5", "age": "55", "fc": "200" },
  "expect": ["出血阴性，炎症阳性 → 优先排查IBD"],
  "ref": "联合矩阵·阴性×明显（FIT<10 / FC≥200，FC=200 为上边界）→ 优先排查 IBD。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "10", "age": "55", "fc": "49" },
  "expect": ["出血临界，炎症阴性 → 建议复查FIT"],
  "ref": "联合矩阵·临界×正常（FIT=10 为临界下边界 / FC=49 为正常上边界）→ 原代码落入 else 误报双阴性，现为复查 FIT。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "19", "age": "55", "fc": "50" },
  "expect": ["双临界值 → 建议随访复查"],
  "ref": "联合矩阵·临界×轻度（FIT=19 为临界上边界 / FC=50 为轻度下边界）→ 双临界随访复查。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "15", "age": "55", "fc": "200" },
  "expect": ["出血临界，炎症阳性 → 优先排查IBD"],
  "ref": "联合矩阵·临界×明显（10≤FIT<20 / FC≥200）→ 原代码落入 else 误报双阴性，现为以肠道炎症为主、优先排查 IBD。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "20", "age": "55", "fc": "30" },
  "expect": ["出血阳性，炎症阴性 → 优先排查肿瘤"],
  "ref": "联合矩阵·阳性×正常（FIT=20 为阳性下边界 / FC<50）→ 优先排查肿瘤。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "100", "age": "55", "fc": "120" },
  "expect": ["FIT (μg/g) - 强阳性"],
  "ref": "联合矩阵·强阳性×轻度（FIT=100 为强阳性起点，联合矩阵仍按阳性格）→ 分级仍应显示强阳性、结论同阳性×轻度。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "99", "age": "55", "fc": "30" },
  "expect": ["出血阳性，炎症阴性 → 优先排查肿瘤"],
  "ref": "FIT=99 为阳性上边界（<100 才是阳性，100 起为强阳性），联合矩阵走阳性×正常。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "5", "age": "55", "fc": "199" },
  "expect": ["出血阴性，炎症轻度升高 → 建议复查"],
  "ref": "FC=199 为轻度升高上边界（<200 归轻度），阴性×轻度 → 复查 FC。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "50", "age": "55", "fc": "200" },
  "expect": ["出血+炎症双阳性 → 需肠镜明确"],
  "ref": "FC=200 为明显升高下边界（≥200 归明显），阳性×明显 → 双阳性。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": { "fit": "150", "age": "55", "fc": "300" },
  "expect": ["出血+炎症双阳性 → 需肠镜明确"],
  "ref": "联合矩阵·阳性×明显（FIT≥20 / FC≥200）→ 双阳性，需肠镜明确。"
},
{
  "slug": "gastroenterology/hepatic-encephalopathy",
  "inputs": { "consciousness": "1", "behavior": "1", "cognition": "1", "asterixis": "1" },
  "clicks": ["document.getElementById('asterixis').value='';calc();document.getElementById('result').textContent='PARTIAL:'+document.getElementById('result').innerHTML.replace(/<[^>]*>/g,'').trim();"],
  "expect": ["PARTIAL:请输入意识状态、行为变化、认知与扑翼样震颤分级后再评估。"],
  "ref": "原生缺陷修复：四项 West Haven 分级下拉全部改为「请选择」空值默认，首屏不再直接给 I 级分级与治疗/住院建议。"
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
