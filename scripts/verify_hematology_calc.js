#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "hematology/anemia-classification",
  "inputs": {
    "hgb": "128",
    "rbc": "3.5",
    "hct": "27",
    "mcvDirect": "75",
    "mchDirect": "24",
    "mchcDirect": "300"
  },
  "expect": [
    "365.7"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/anemia-differential",
  "inputs": {
    "mcv": "108",
    "retic": "1.2",
    "ferritin": "8",
    "siron": "6",
    "tibc": "75",
    "b12": "200",
    "folate": "10",
    "ldh": "250",
    "bilirubin": "12",
    "haptoglobin": "1.0"
  },
  "expect": [
    "MCV增大(108fL)"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例：expect「未满足临床和实验室标准」是「什么都不勾」的默认结论，零判别力。
  "slug": "hematology/aps-diagnosis",
  "checkIds": [
    "vt_venous",
    "lab_la",
    "lab_acl_igg",
    "lab_repeat",
    "lab_within5y"
  ],
  "expect": [
    "aCL IgG中高滴度",
    "满足至少1项临床标准 + 1项实验室标准"
  ],
  "ref": "勾选 1 项临床标准(vt_venous=静脉血栓) + 2 项实验室标准(lab_la / lab_acl_igg) → 实验室条目列表含「aCL IgG中高滴度」，结论文案为「满足至少1项临床标准 + 1项实验室标准，且实验室检测符合时间要求…」。注意不可用「符合APS分类标准」——它是「不符合APS分类标准」的子串（子串误命中）。"
},
{
  "slug": "hematology/calc-1",
  "inputs": {
    "mcv": "110", "rdw": "18"
  },
  "expect": [
    "大细胞不均一性贫血"
  ],
  "ref": "非默认输入：mcv=110(>100 大细胞性)、rdw=18(>15 不均一)→分类「大细胞不均一性贫血」。默认 inputs 为空→「请输入 MCV 与 RDW。」不命中，故可区分。"
},
{
  "slug": "hematology/cd34-count",
  "inputs": {
    "pbWbc": "38",
    "pbCd34": "0.8",
    "pbWeight": "70",
    "pbVolume": "12000",
    "pbEff": "40",
    "prWbc": "150",
    "prCd34": "1.5",
    "prVolume": "150",
    "prWeight": "70"
  },
  "expect": [
    "14.6×10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/cml-monitoring",
  "inputs": {
    "months": "18",
    "bcrabl": "0.5"
  },
  "expect": [
    "BCR-ABL升高至0.1-1%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/coagulation-factor",
  "inputs": {
    "activity": "8",
    "residual": "25",
    "dilution": "1",
    "weight": "70",
    "dose": "1400",
    "preActivity": "1",
    "postActivity": "35"
  },
  "expect": [
    "8%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/detector-5",
  "inputs": {
    "granCD59": "53",
    "granCD55": "32",
    "rbcCD59": "15",
    "monoCD59": "28",
    "type2": "10",
    "type3": "25",
    "ldh": "450",
    "hb": "85"
  },
  "expect": [
    "53%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/dic-scoring",
  "inputs": {
    "plt": "68",
    "ddimer": "2",
    "pt": "6",
    "fib": "1.2"
  },
  "expect": [
    "50-100"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/hemophilia-treatment",
  "inputs": {
    "weight": "105",
    "current": "1",
    "target": "50"
  },
  "expect": [
    "2050"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/hemophilia-treatment",
  "inputs": {
    "weight": "84",
    "current": "2"
  },
  "clicks": [
    "document.getElementById('bleedType').value='custom';document.getElementById('target').value='55';calc();"
  ],
  "expect": [
    "2230",
    "预期峰值活性 ≈ 55%"
  ],
  "ref": "FVIII 自定义目标 55%、当前 2%：剂量 = 84×(55−2)×0.5 = 2226 → 取整 2230 IU；1 IU/kg 提升 2%，预期峰值 = 2 + round((2230/84)×2) = 2 + round(53.10) = 55%。修复前实现误用「÷回收率」，得 2+round(2230/84/2)=2+13=15%，与目标 55% 自相矛盾。注入值 weight=84/current=2 均异于页面默认 70/1，避免 all_default。"
},
{
  "slug": "hematology/hlh-diagnosis",
  "inputs": {
    "c4_tg": "6.5",
    "c4_fib": "1.5",
    "c7_ferritin": "800",
    "c8_scd25": "2400"
  },
  "expect": [
    "6.5mmol/L)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/ipss-r",
  "inputs": {
    "blasts": "3",
    "hgb": "85",
    "anc": "0.8",
    "plt": "50"
  },
  "expect": ["3.5 IPSS-R 总分"],
  "ref": "auto-restore"
},
{
  "slug": "hematology/iron-overload",
  "inputs": {
    "ferritin": "3750",
    "tsat": "80",
    "transfusions": "12"
  },
  "expect": [
    "3750"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "hematology/leukemia-classification",
  "inputs": {
    "amlSub": "M1"
  },
  "expect": [
    "FLT3-ITD常见"
  ],
  "ref": "auto-restore"
},
{
  // 原为 all_default 弱用例：mtRatio/massSize 均为 0 = 页面默认，expect「请勾选受累部位」是空态提示。
  "slug": "hematology/lymphoma-staging",
  "inputs": {
    "mtRatio": "0",
    "massSize": "0"
  },
  "checkIds": [
    "ln1",
    "ln5",
    "b1",
    "extra1",
    "ln8"
  ],
  "expect": [
    "IIIB (ES)"
  ],
  "ref": "横膈上 ln1 + 横膈下 ln5 → stage=III；b1 → B 症状（sym=B）；extra1 → 结外 E、ln8 → 脾 S → 完整分期「IIIB (ES)」。注意不可用「横膈两侧淋巴结区域受累」——深链示例 block 已含该字面量（outside-script 命中，逃生项）。回退默认（未勾选）→ 「请勾选受累部位」。"
},
{
  "slug": "hematology/m-protein",
  "inputs": {
    "tp": "113",
    "albumin": "35",
    "mprotein": "25",
    "sIgG": "18",
    "sIgA": "1",
    "sIgM": "0.5",
    "sKappa": "500",
    "sLambda": "30"
  },
  "expect": [
    "22.1%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/mm-staging",
  "inputs": {
    "albumin": "53",
    "b2m": "5.5",
    "ldhNormal": "250",
    "ldh": "400"
  },
  "expect": [
    "53"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "hematology/rater-5",
  "inputs": {
    "hb": "158",
    "blasts": "2",
    "wbc": "15"
  },
  "expect": [ "血红蛋白 158" ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/rater-5",
  "inputs": { "age": "1", "symptoms": "1", "hb": "90", "blasts": "2", "wbc": "30" },
  "expect": ["中位生存期约 16 个月"],
  "ref": "DIPSS 总分 = 年龄>65(1) + 体质症状(1) + HGB<100(2) + 原始≥1%(1) + WBC>25(1) = 6 ⇒ 高危（5–6 分）"
    + "（修复前 HGB 只加 1 分、分段为 0–1/2/3/4–5，同一输入仅 5 分仍高危但 1 分会被误判低危）；默认态 age=0/symptoms=0/hb=105/blasts=2/wbc=15 ⇒ 1 分中危-1，不出现 16 个月。"
},
{
  "slug": "hematology/rater-6",
  "inputs": {
    "plt": "68",
    "ddimer": "2",
    "pt": "5",
    "fib": "0.9",
    "fdp": "40"
  },
  "expect": [ "68 血小板" ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/rater-risk-1",
  "inputs": {
    "drugName": "",
    "pltBefore": "270",
    "pltNadir": "15",
    "onsetDays": "5",
    "recoveryDays": "7"
  },
  "expect": [ "血小板下降幅度 94" ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/thrombin-generation",
  "inputs": {
    "lagTime": "6",
    "peak": "180",
    "ttPeak": "6.5",
    "etp": "1200",
    "startTail": "20",
    "cLag": "3",
    "cPeak": "200",
    "cTtPeak": "7",
    "cEtp": "1200",
    "cTail": "20"
  },
  "expect": [
    "凝血因子缺乏或抗凝治疗"
  ],
  "ref": "auto-restore"
},
{
  "slug": "hematology/transfusion-dose",
  "inputs": {
    "pWeight": "105",
    "pCurrentHgb": "60",
    "pTargetHgb": "90",
    "plWeight": "70",
    "plCurrent": "10",
    "plTarget": "40",
    "fWeight": "70",
    "fDose": "12",
    "cWeight": "70",
    "cCurrent": "0.8",
    "cTarget": "1.5"
  },
  "expect": [
    "105"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
  {
    "slug": "hematology/itp-risk-score",
    "inputs": {
      "drug": "quinine"
    },
    "expect": [
      "录于病历） 4. 必要时短期使用IVIG或糖皮质激素（重症）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"drug\":\"quinine\"}，输出区含「录于病历） 4. 必要时短期使用IVIG或糖皮质激素（重症）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "hematology/itp-risk-score",
    "inputs": { "drug": "quinine" },
    "checks": ["1"],
    "expect": ["总分：4分", "药物再激发：+1分"],
    "ref": "反向计分/上限核对：四项各上限 2 分（c4 原实现 +3 分使实际可达 9 而页面写「满分 8」，已改回 +2）。"
      + "该页用 querySelector(name:checked) 逐组取值，桩只能以 checks 统一注入 ⇒ 四组各 1 分、总分 4 分；"
      + "默认全勾为 8 分「确定」，两锚均不出现。"
  },
  { slug: "hematology/detector-5",
    inputs: { granCD59: "", granCD55: "", rbcCD59: "", monoCD59: "", type2: "", type3: "", ldh: "", hb: "" },
    expect: ["请填写全部流式指标（LDH、Hb 需大于 0）后再判读。"],
    ref: "空态守卫：8 项全清空时不再按 0 计算（旧实现 → 克隆 0%「未检测到 PNH 克隆」+ LDH 0「正常/轻度升高」+ Hb 0「重度贫血」的伪结论），改为只输出填写提示。默认态 35/32/15/28/10/25/450/85 有值 ⇒ 提示串不出现。" }
  ,
  {
    // ISTH 纤维蛋白相关标志物无/中度/显著升高对应 0/2/3 分。
    slug: "hematology/dic-scoring",
    inputs: { plt: "68", ddimer: "3", pt: "4", fib: "1.2" },
    checkIds: ["hasDisease"],
    expect: ["纤维蛋白相关标志物 显著升高 → +3"],
    ref: "血小板 68(+1)、标志物显著升高(+3)、PT 4 秒(+1)、纤维蛋白原 1.2(+0)，总分 5。"
  },
  {
    slug: "hematology/dic-scoring",
    inputs: { plt: "68", ddimer: "2", pt: "6", fib: "1.2" },
    checkIds: ["hasDisease"],
    clicks: ["calc();var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='DIC5 '+((document.getElementById('ddimer').value==='2'&&document.getElementById('pt').value==='6'&&r.indexOf('显性DIC')>=0)?'OK':'BAD');"],
    expect: ["DIC5 OK"],
    ref: "ISTH: 1 + 2 + 2 + 0 = 5; PT at 6 seconds belongs to the 2-point category."
  },
  {
    slug: "hematology/dic-scoring",
    inputs: { plt: "68", ddimer: "0", pt: "5.9", fib: "1.2" },
    checkIds: ["hasDisease"],
    expect: ["无升高 → +0", "PT延长 3至<6s (5.9s) → +1", "尚不符合显性DIC标准"],
    ref: "No marker elevation adds 0 and PT 5.9 seconds adds 1; an overt score below 5 does not exclude early DIC."
  },
  {
    slug: "hematology/dic-scoring",
    inputs: { plt: "68", ddimer: "", pt: "6", fib: "1.2" },
    checkIds: ["hasDisease"],
    expect: ["请填写血小板、PT 延长和纤维蛋白原，并选择标志物升高程度"],
    ref: "No selected marker category must not be scored as no elevation."
  },
  {
    // 宣称 vs 实现：IPSS-R 2012 原始细胞分档为 0/1/2/3（>10% 计 3 分），旧实现误为 4 分。
    slug: "hematology/ipss-r",
    inputs: { blasts: "10.5", hgb: "85", anc: "0.8", plt: "50" },
    expect: ["骨髓原始细胞 10.5% → +3", "5.5 IPSS-R 总分"],
    ref: "核型默认良好(+1) + 原始 10.5%(+3) + HGB 85(+1) + ANC 0.8(+0) + PLT 50(+0.5) = 5.5 分 ⇒ 高危。旧实现 >10% 计 +4 ⇒ 6.5 分「极高危」，故总分与明细双向判别。"
  },
  {
    // 宣称 vs 实现：ELN 2020 的 3 个月节点应看 BCR-ABL≤10%（早期分子学反应），旧实现套用 6/12 月的 ≤0.1%。
    slug: "hematology/cml-monitoring",
    inputs: { months: "3", bcrabl: "5" },
    expect: ["治疗3个月BCR-ABL≤10%（ELN 2020 早期分子学反应）"],
    ref: "3 个月 BCR-ABL 5% ≤10% ⇒ 最佳反应。旧实现按 ≤0.1% 判定 ⇒ 「警告」；默认 months=12/bcrabl=0.5 ⇒ 12 月分支，不出现该串。"
  },
  {
    slug: "hematology/cml-monitoring",
    inputs: { months: "3", bcrabl: "15" },
    expect: ["BCR-ABL>10%，按 ELN 2020 属治疗失败（需复查确认）"],
    ref: "3 个月 BCR-ABL 15% >10% ⇒ 治疗失败。旧实现仅给「警告」，故该串为强判别；默认 12 月分支不出现。"
  },
  {
    slug: "hematology/rater-5",
    clicks: ["var __b=document.getElementById('res').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/MPN-10 症状总分/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('res').innerHTML=__ok?'__R5_DEF_OK__':'__R5_DEF_FAIL__ '+__b;"],
    expect: ["__R5_DEF_OK__"],
    ref: "批 3 默认态：只出 MPN-10 总分与 DIPSS 评分，结果区不含 分级/建议/诊断/治疗/风险。"
  },
  {
    slug: "hematology/rater-5",
    inputs: { age: "1", symptoms: "1", hb: "90", blasts: "2", wbc: "30" },
    expect: ["高危", "中位生存期"],
    ref: "批 3 改动态：DIPSS 6 ⇒ 高危并给出中位生存期；确认 dirty 置位后决策文案才出现。"
  },
  {
    slug: "hematology/rater-5",
    clicks: ["resetAll();var __b=document.getElementById('res').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/MPN-10 症状总分/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('res').innerHTML=__ok?'__R5_RST_OK__':'__R5_RST_FAIL__ '+__b;"],
    expect: ["__R5_RST_OK__"],
    ref: "批 3 重置态：resetAll() 先复位 dirty 再复算，决策文案消失。"
  },
  {
    slug: "hematology/rater-6",
    clicks: ["var __b=document.getElementById('res').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/ISTH 总分/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('res').innerHTML=__ok?'__R6_DEF_OK__':'__R6_DEF_FAIL__ '+__b;"],
    expect: ["__R6_DEF_OK__"],
    ref: "批 3 默认态：只出 ISTH 总分，结果区不含 分级/建议/诊断/治疗/风险。"
  },
  {
    slug: "hematology/rater-6",
    inputs: { plt: "10", ddimer: "8.5", pt: "5", fib: "0.9" },
    expect: ["显性 DIC"],
    ref: "批 3 改动态：PLT 10 使 ISTH 达显性 DIC 阈值；确认 dirty 置位后诊断文案才出现。"
  },
  {
    slug: "hematology/rater-6",
    clicks: ["resetAll();var __b=document.getElementById('res').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/ISTH 总分/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('res').innerHTML=__ok?'__R6_RST_OK__':'__R6_RST_FAIL__ '+__b;"],
    expect: ["__R6_RST_OK__"],
    ref: "批 3 重置态：resetAll() 恢复检验值后先清 dirty 再复算，决策文案消失。"
  },
  {
    slug: "hematology/rater-risk-1",
    clicks: ["var __b=document.getElementById('res').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/综合评分/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('res').innerHTML=__ok?'__RR1_DEF_OK__':'__RR1_DEF_FAIL__ '+__b;"],
    expect: ["__RR1_DEF_OK__"],
    ref: "批 3 默认态：只出综合评分，结果区不含 分级/建议/诊断/治疗/风险。"
  },
  {
    slug: "hematology/rater-risk-1",
    inputs: { pltBefore: "270", pltNadir: "200", onsetDays: "20", recoveryDays: "20", drugClass: "low" },
    expect: ["风险评估结果", "不太可能"],
    ref: "批 3 改动态：低降幅/超出时间窗 ⇒ 占比 <30% 落「不太可能」且出现「风险评估结果」标题；默认态标题为「DITP 评分结果」，双向判别。"
  },
  {
    slug: "hematology/rater-risk-1",
    clicks: ["resetAll();var __b=document.getElementById('res').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/综合评分/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('res').innerHTML=__ok?'__RR1_RST_OK__':'__RR1_RST_FAIL__ '+__b;"],
    expect: ["__RR1_RST_OK__"],
    ref: "批 3 重置态：resetAll() 恢复特征与检验值后先清 dirty 再复算，决策文案消失。"
  },
  {
    slug: "hematology/itp-risk-score",
    clicks: ["var __b=document.getElementById('result').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/总分 \\(满分8\\)/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('result').innerHTML=__ok?'__ITP_DEF_OK__':'__ITP_DEF_FAIL__ '+__b;"],
    expect: ["__ITP_DEF_OK__"],
    ref: "批 3 默认态：只出总分，结果区不含 分级/建议/诊断/治疗/风险（全勾默认 8 分也不出「确定」）。"
  },
  {
    slug: "hematology/itp-risk-score",
    clicks: ["__markScaleDirty();var __b=document.getElementById('result').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/确定 \\(Definite\\)/.test(__b)&&/处理建议/.test(__b);document.getElementById('result').innerHTML=__ok?'__ITP_MOD_OK__':'__ITP_MOD_FAIL__ '+__b;"],
    expect: ["__ITP_MOD_OK__"],
    ref: "批 3 改动态：默认 4 项各 2 分 ⇒ 8 分「确定 (Definite)」；确认 dirty 置位后因果等级文案才出现。"
  },
  {
    slug: "hematology/itp-risk-score",
    clicks: ["__markScaleDirty();resetAll();var __b=document.getElementById('result').innerHTML.replace(/<[^>]+>/g,' ');var __ok=/总分 \\(满分8\\)/.test(__b)&&/当前为默认评分/.test(__b)&&!/分级|建议|诊断|治疗|风险/.test(__b);document.getElementById('result').innerHTML=__ok?'__ITP_RST_OK__':'__ITP_RST_FAIL__ '+__b;"],
    expect: ["__ITP_RST_OK__"],
    ref: "批 3 重置态：先置 dirty 制造决策，再 resetAll() 复位后决策文案消失。"
  },
  {
    slug: "hematology/dic-scoring",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/hematology/dic-scoring.html','utf8');var q=String.fromCharCode(34);var a=h.indexOf('ddimer'+q+':2')>=0&&h.indexOf('ddimer'+q+':3,'+q+'pt'+q+':2')<0&&h.indexOf('else if(rb')>=0&&h.indexOf('rb.innerHTML=')>=0&&h.indexOf('本地实验室阈值')>=0&&h.indexOf('早期 DIC 可疑')>=0;document.getElementById('__tbProbe').textContent='DICFIX '+(a?'OK':'BAD');"],
    expect: ["DICFIX OK"],
    ref: "12-N51/N52/N53：早期DIC可疑预设原 plt85+ddimer3+pt2+fib2.5=2分判不支持DIC（名实相反），改 ddimer6+pt4+fib1.0=3分落非显性DIC；hasDisease 取消时 refBar 加 else 清空避免旧红色标尺残留；D-二聚体简化档补与 ISTH 原文 0/2/3 分值不同的声明。源码形态哨兵旧版必红。"
  },
{
  "slug": 'hematology/leukemia-classification',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/hematology/leukemia-classification.html\',\'utf8\');var i=h.indexOf(\'function switchTab(t,btn){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'if(!t||!btn)\')>=0&&seg.indexOf(\'showAml(); showAll(); showMicm(); return;\')>=0;document.getElementById(\'__tbProbe\').textContent=\'LEUKH0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['LEUKH0 OK'],
  "ref": "第1336批·历史恢复无参切换函数抛错修复源码形态强锚：旧版 function switchTab(t,btn){ 无参调用解引用参数抛错被 catch 吞、结果不重算；修复后无参分支安全重算本页主结果并 return。旧版无 ⇒ BAD。"
},
{ slug:"hematology/ipss-r", inputs:{"hgb":"","plt":"","blasts":""}, expect:["请填写血红蛋白、血小板与原始细胞比例"], ref:"核心临床参数留空不得给出分级/风险结论（CLINCLR）" },
{ slug:"hematology/mm-staging", inputs:{"b2m":"","albumin":""}, expect:["请填写β2 微球蛋白与白蛋白"], ref:"核心临床参数留空不得给出分级/风险结论（CLINCLR）" },
{ slug:"hematology/m-protein", inputs:{"mprotein":"","tp":""}, expect:["请填写M 蛋白量与总蛋白"], ref:"核心临床参数留空不得给出分级/风险结论（CLINCLR）" }
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

  console.log("==== hematology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
