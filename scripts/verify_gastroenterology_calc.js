#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
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
    "size": "12", "paris": "IIa", "kudo": "I", "nice": "3"
  },
  "expect": [ "高", "EUS评估浸润深度", "不宜直接按普通息肉内镜切除" ],
  "ref": "NICE 3 = 深层 SM 癌：旧版只判「中-高」，综合建议落「内镜下完整切除」；新版必须判高风险并提示 EUS/外科评估。默认 nice=2、size=8 ⇒ 不命中。"
},
{
  "slug": "gastroenterology/colonoscopy-polyp",
  "inputs": {
    "size": "25", "paris": "Is", "kudo": "IIIL", "nice": "2"
  },
  "expect": [ "ESD整块切除" ],
  "ref": "≥20mm 大息肉：综合建议不得只写「内镜下完整切除」，应提示 ESD 整块切除。默认 8mm ⇒ 不命中。"
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
    "r2": "60", "r4": "5", "r0": "100", "halfTime": "", "method": "scintigraphy", "meal": "solid"
  },
  "expect": [ "82.8", "由2h/4h残留率估算" ],
  "ref": "T½ 自动估算：r0=100、r2=60、r4=5，留空 T½ 时按指数模型两点均值 k=( -ln(.6)/2 + -ln(.05)/4 )/2≈0.5021，T½=ln2/k≈82.8 分钟。旧版格空按 0 判「排空过快」，且从不估算。"
},
{
  "slug": "gastroenterology/gastric-emptying",
  "inputs": {
    "r2": "65", "r4": "5", "r0": "100", "halfTime": "", "method": "scintigraphy", "meal": "solid"
  },
  "expect": [ "2小时残留率65%（＞60%）", "胃排空延迟（胃轻瘫）" ],
  "ref": "2h 延迟纳入综合：r2=65>60、r4=5≤10、T½ 估约 86 分钟不超 90，旧版综合只看 4h/T½ 会判正常；新版必须判排空延迟。"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
  "expect": ["Ⅳ期 OLGIM分期 Ⅳ期 OLGA分期","每年随访胃镜"],
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
  "slug": "gastroenterology/hp-dob",
  "inputs": { "dob": "" },
  "expect": ["请填写检测值后再判读。", "Please enter the test value before interpreting."],
  "ref": "空态守卫（2026-11-05）：清空 DOB 值后不再输出「0 DOB值」+「阴性」+「DOB值＜4.0‰…继续保持良好卫生习惯」整套结论，只给填写提示。⚠ 判空只认空串——DOB 0 ‰ 是合法检测值（阴性），照常判读。提示文案已改为中英双语合并句「请填写检测值后再判读。」，旧期望「请填写 DOB 检测值后再判读。」随之更新。"
},
{
  "slug": "gastroenterology/hp-dob",
  "inputs": { "dob": "3.0" },
  "checkIds": ["onPPI"],
  "expect": ["灰区/临界（用药期间）"],
  "ref": "535 复核失败重做：13C DOB 3.0 属灰区，勾选 PPI 只追加用药提示，不得改判阴性或「结果不可靠」。旧实现 warnings 分支先于灰区分支 ⇒「结果不可靠（可能假阴性）」并称阴性，本串不命中。"
},
{
  "slug": "gastroenterology/hp-dob",
  "inputs": { "dob": "120", "testType": "14c" },
  "checkIds": ["onPPI"],
  "expect": ["弱阳性（+）（用药期间，结果可能受抑制）"],
  "ref": "535 复核失败重做：14C 120 DPM 应保留弱阳性（+）分级，用药仅追加「（用药期间，结果可能受抑制）」；旧实现用药分支吞掉分级并断言「感染较重」，本串不命中。"
},
{
  "slug": "gastroenterology/hp-dob",
  "inputs": { "dob": "" },
  "clicks": [
    "document.getElementById('testType').value='14c';calc();document.getElementById('__tbProbe').textContent='HPLABEL '+document.getElementById('dobLabel').textContent;"
  ],
  "expect": ["HPLABEL DPM（衰变数/分钟）"],
  "ref": "535 复核失败重做：空值提前 return 移到单位/标签切换之后，清空输入切到 14C 时单位标签仍同步为 DPM；旧实现标签切换在 return 之后，保留上一次的「DOB值 (‰)」⇒ 本串不命中。"
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
},
{
  "slug": "gastroenterology/child-pugh",
  "inputs": { "bilirubin": "53", "albumin": "30", "pt": "4", "inr": "1.7", "ascites": "", "encephalopathy": "1" },
  "expect": ["请填写：腹水程度"],
  "ref": "L-N45 核销：腹水下拉改为「请选择」空值默认，缺项不再按 0 分参与求和，结果区列出缺项并停止评分。"
},
{
  "slug": "gastroenterology/child-pugh",
  "inputs": { "bilirubin": "100", "albumin": "40", "pt": "0", "inr": "1", "ascites": "1", "encephalopathy": "1" },
  "clicks": ["document.getElementById('pbc').checked=true;calc();"],
  "expect": ["总胆红素 100 μmol/L (68–170，PBC) → 2分"],
  "ref": "L-N46 核销：勾选 PBC 后胆红素按 68/170 分档，100 μmol/L 记 2 分（非 PBC 为 3 分）；默认不勾选，该串仅在 PBC 注入态出现。"
},
{
  "slug": "gastroenterology/glasgow-pancreatitis",
  "inputs": { "age": "55", "wbc": "15", "glucose": "10", "ldh": "350", "ast": "200", "calcium": "", "albumin": "", "pao2": "", "urea": "8" },
  "expect": ["未填写：钙、白蛋白、PaO₂", "55 岁"],
  "ref": "L-N47 核销：钙/白蛋白/PaO₂ 空值不再按 0 触发「低于阈值 +1」，改为不计分并列出缺项；三项清空后总分 0。原「轻症可能性大」在纯默认态也命中（逃生），改为「未填写…」+ 注入年龄 55 岁回显双锚；旧实现 3 分 ⇒ 重症急性胰腺炎。"
},
{
  "slug": "gastroenterology/cdai",
  "inputs": { "hct": "" },
  "expect": ["请填写红细胞压积 Hct"],
  "ref": "L-N50 核销：Hct 空值不再按 0 计算（旧实现凭空 +222 分推入中度活动），改为拦截并提示。"
},
{
  "slug": "gastroenterology/cdai",
  "inputs": { "hct": "70" },
  "expect": ["红细胞压积 Hct 应为 20–60%"],
  "ref": "L-N50 核销：Hct 超出 20–60% 合法性校验即报错不出分。"
},
{
  "slug": "gastroenterology/cdai",
  "inputs": { "hct": "30" },
  "expect": ["Hct 标准 42% − 实测 30% = 12.0", "× 6 = 72.0"],
  "ref": "L-N51 核销并去默认化：注入 Hct=30（页面默认 35）⇒ 女性标准 42% − 30% = 12.0，×6 = 72.0；旧实现标准 37% 时得 7.0/42.0，两锚都不命中。默认态 7.0 不含本串。"
},
{
  "slug": "gastroenterology/saag-ascites",
  "inputs": { "serumAlb": "", "ascitesAlb": "12" },
  "expect": ["请填写血清白蛋白与腹水白蛋白"],
  "ref": "L-N52 核销：血清白蛋白空值不再按 0 计算（旧实现得 SAAG=-12 并判「非门脉高压性腹水」），改为缺项提示不出结论。"
},
{
  "slug": "gastroenterology/saag-ascites",
  "inputs": { "serumAlb": "12", "ascitesAlb": "40" },
  "expect": ["数值异常：血清白蛋白与腹水白蛋白均应在 0–60 g/L"],
  "ref": "L-N52 核销：腹水白蛋白高于血清白蛋白属录入错误，显式报错而非静默算出负 SAAG。"
},
{
  "slug": "gastroenterology/bilirubin-ratio",
  "inputs": { "tbil": "85", "dbil": "", "ref": "21" },
  "clicks": ["var o=document.getElementById('result');var bad=o.innerHTML.indexOf('请填写总胆红素')>=0;document.getElementById('dbil').value='30';calc();var good=o.innerHTML.indexOf('35.3%')>=0;document.getElementById('__tbProbe').textContent='BILR '+(bad&&good?'OK':'BAD');"],
  "expect": ["BILR OK"],
  "ref": "L-N54 状态链：DBIL 空值先显式拒绝（旧实现按 0 算成 0.0% 并误判溶血/Gilbert），再注入 DBIL=30 ⇒ 30/85=35.3% 且判肝细胞性黄疸。纯默认态两值皆空时拒绝提示也出现，原单锚属逃生，改探针锁「拒绝→恢复」整链。"
},
{
  "slug": "gastroenterology/hepatic-encephalopathy",
  "inputs": { "consciousness": "0", "behavior": "0", "cognition": "0", "asterixis": "0" },
  "expect": ["未做（不诊断 MHE）", "无临床肝性脑病"],
  "ref": "L-N53 核销：四项全正常且 MHE 专项测试未做时输出「无临床肝性脑病」，不再等同 MHE 并建议乳果糖；旧实现直接输出「轻微型肝性脑病（MHE）」+ 乳果糖。"
},
{
  "slug": "gastroenterology/bilirubin-ratio",
  "inputs": { "tbil": "21", "dbil": "15", "ref": "21" },
  "expect": ["孤立性直接胆红素升高"],
  "ref": "L-N55 核销：DBIL 上限（6.8/8.0）已参与判断，TBIL 21 未超上限但 DBIL 15>6.8 ⇒ 孤立性直接胆红素升高；旧实现只看 TBIL，误判「正常范围」。"
},
{
  "slug": "gastroenterology/bilirubin-ratio",
  "inputs": { "tbil": "30", "dbil": "60", "ref": "21" },
  "expect": ["录入有误，已停止计算"],
  "ref": "L-N56 核销：DBIL>TBIL 显式报错并停止计算，不再静默封顶后输出「梗阻性黄疸」。"
},
{
  "slug": "gastroenterology/mayo-score",
  "inputs": { "stool": "2", "bleeding": "0", "endoscopy": "0", "physician": "0" },
  "expect": ["未达临床缓解（单项活动）"],
  "ref": "L-N57 核销：临床缓解须「总分 ≤2 且便次 ≤1 且无便血」，总分 2（便次 2 分）⇒ 未达临床缓解；旧实现仅看总分判「缓解期」。"
},
{
  "slug": "gastroenterology/ibd-nutrition",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/gastroenterology/ibd-nutrition.html','utf8');var ok=h.indexOf('min:0,max:7')>=0&&h.indexOf('\"lo\":0,\"hi\":3')>=0&&h.indexOf('\"lo\":3,\"hi\":5')>=0&&h.indexOf('\"lo\":5,\"hi\":null')>=0&&h.indexOf('\"lo\":null,\"hi\":5')<0&&h.indexOf('有营养风险\",\"en\":\"At risk')<0;document.getElementById('__tbProbe').textContent='IBD197 '+(ok?'OK':'BAD');"],
  "expect": ["IBD197 OK"],
  "ref": "03-197 IBD 参考标尺量程塌缩：旧 bands 两端均单边 null → refBar 推导 lo0=hi0=5 兜底 5–6，低分 clamp 最左且高亮「有营养风险」，与文本 <3低/≥3中/≥5重 相反。本批显式 min:0,max:7 + 三段 bands [0,3)低/[3,5)中/[5,∞)重 与文本分级同源。源码形态哨兵：旧双边 null/错标消失、新量程与分段出现；默认态不产哨兵（仅 clicks 读源码），零逃生。"
},
{
  "slug": "gastroenterology/ibd-nutrition",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/gastroenterology/ibd-nutrition.html','utf8');var ok=h.indexOf('cat=health')>=0&&h.indexOf('MedicalApplication')>=0&&h.indexOf('cat=finance')<0&&h.indexOf('FinanceApplication')<0;document.getElementById('__tbProbe').textContent='IBD198CAT '+(ok?'OK':'BAD');"],
  "expect": ["IBD198CAT OK"],
  "ref": "03-198 IBD 营养风险筛查页分类纠正：医疗页误标 cat=finance/JSON-LD FinanceApplication，改 cat=health（唯一源），build 自动重生成 MedicalApplication + 行业 JSON/相关工具卡/sitemap/sw。源码形态哨兵：含 cat=health + MedicalApplication 且无旧串；默认态不产哨兵（仅 clicks 读源码），零逃生。"
},
{
  "slug": "gastroenterology/esophageal-varices",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/gastroenterology/esophageal-varices.html','utf8');var ok=h.indexOf('cat=health')>=0&&h.indexOf('MedicalApplication')>=0&&h.indexOf('cat=finance')<0&&h.indexOf('FinanceApplication')<0;document.getElementById('__tbProbe').textContent='EV194CAT '+(ok?'OK':'BAD');"],
  "expect": ["EV194CAT OK"],
  "ref": "03-194 食管静脉曲张页分类纠正：医疗页误标 cat=finance/FinanceApplication，改 cat=health（唯一源），build 自动重生成 MedicalApplication。源码形态哨兵：含 cat=health + MedicalApplication 且无旧串；默认态不产哨兵（仅 clicks 读源码），零逃生。"
},
{
  "slug": "gastroenterology/capsule-endoscopy",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/gastroenterology/capsule-endoscopy.html','utf8');var a=h.split('===null').length-1;var b=h.split('d+=1440').length-1;var c=h.split('min:0,max:480').length-1;var ok=a>=3&&b>=1&&c>=1;document.getElementById('__tbProbe').textContent='CAPFIX '+(ok?'OK':'BAD');})();"],
  "expect": ["CAPFIX OK"],
  "ref": "第1330批·胶囊内镜跨零点负值/00:00判缺失/SBTT标尺量程修复源码形态强锚：判空改 ===null(00:00合法) before=0/fixed=3；elapsed 对负差 +1440 跨日归一化 before=0/fixed=1；标尺显式 min:0,max:480 三段同源 before=0/fixed=1。旧版无 ⇒ BAD。三锚均不含引号规避 harness 转义。"
},
{
  "slug": "gastroenterology/ibd-nutrition",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/gastroenterology/ibd-nutrition.html','utf8');var a=h.indexOf('__bmiRaw')>=0;var b=h.indexOf('__albRaw')>=0;var c=h.indexOf('!isFinite(bmi)')>=0;var d=h.indexOf('!isFinite(albumin)')>=0;var z=h.indexOf('bmi=parseFloat(document.getElementById(\\'bmi\\').value)||0')<0;var ok=a&&b&&c&&d&&z;document.getElementById('__tbProbe').textContent='IBD195 '+(ok?'OK':'BAD');})();"],
  "expect": ["IBD195 OK"],
  "ref": "第1331批·IBD清空BMI/白蛋白按最差档计分修复源码形态强锚：原 parseFloat(.)||0 把空/非法变0，BMI0落<17→3分、白蛋白0落<30→+2分；修复后原始判空+NaN，计分维度 !isFinite 时跳过。四锚 before 全0/fixed 有值。"
},
 {
  "slug": "gastroenterology/gastrin-level",
  "inputs": {"gastrin":"105","ph":"low"},
  "expect": ["正常范围","105 pg/mL"],
  "ref": "参考上限 115：105 应为正常；旧实现 <100 会误判轻度升高。"
},
{
  "slug": "gastroenterology/detector-7",
  "inputs": {"ab1":"1","ab2":"0","ab3":"1","ab4":"1","ab5":"0","ab6":"0","prior":"0"},
  "expect": ["多重耐药·需个体化","共 3 种"],
  "ref": "3 种耐药且含克拉霉素：旧分支先命中「不含克拉霉素」降级；现应先报多重耐药。"
},
{
  "slug": "gastroenterology/stool-occult-quant",
  "inputs": {"fit":"8","fc":"40","age":"50","status":"screening"},
  "expect": ["双阴性 → 风险低"],
  "ref": "「筛查阴性」预设应由 FIT 10（临界值）改为 8（阴性），使预设名与判读一致。"
},
{
  "slug": "gastroenterology/nafld-fibroscan",
  "inputs": {"lsm":"8","cap":"260","validity":"valid","probe":"XL"},
  "expect": ["仅适用于 M 探头"],
  "ref": "XL 探头不得套用 M 探头阈值；旧实现照常输出 F2/S1。"
},
{
  "slug": "gastroenterology/nafld-fibroscan",
  "inputs": {"lsm":"20","cap":"320","validity":"unreliable","probe":"M"},
  "expect": ["不可判定（可靠性存疑）","不作为分期依据"],
  "ref": "可靠性存疑时旧实现仍显示 F4/S3；现应改「不可判定」并声明不作分期依据。"
},
{
  "slug": "gastroenterology/esophageal-varices",
  "inputs": {"size":"3","rc":"3","child":"3","bleed":"1"},
  "expect": ["再出血风险","二级预防"],
  "ref": "有出血史不应再报「首次出血风险」与一级预防；现按再出血与二级预防输出。"
},
{
  "slug": "gastroenterology/ibd-nutrition",
  "inputs": {"activity":"0","extent":"0","bmi":"20","weightLoss":"0","albumin":"38","intake":"0","age":"45","complications":"2"},
  "expect": ["中度营养风险"],
  "ref": "瘘管/脓肿应为 3 分：旧选项值 1 只加 2 分，总分 2 判低风险；现总分 3 判中度。"
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
