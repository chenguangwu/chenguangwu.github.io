#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  // 原为 no_inputs 弱用例：expect「26-50%」来自 grade=2 的默认档，与勾选无关。
  "slug": "ent/adenoid-grading",
  "checkIds": [
    "s1",
    "s6"
  ],
  "expect": [
    "存在手术指征（腺样体面容）",
    "伴随症状： 张口呼吸、腺样体面容"
  ],
  "ref": "grade 默认 2（II度）；勾选 s1(张口呼吸)+s6(腺样体面容) → 症状列表拼接，且 s6 直接触发手术指征（surgReason=[腺样体面容]）。回退默认（未勾选、grade=2 且 s5 未勾选）→ 输出「目前暂无明确手术指征」，两串均不命中。"
},
{
  "slug": "ent/ahi-severity",
  "inputs": {
    "apneas": "45",
    "hypopneas": "50",
    "sleepHours": "6",
    "lowSpO2": "82",
    "odCount": "60",
    "arousals": "40"
  },
  "expect": [
    "15.8"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/allergy-skin-test",
  "inputs": {
    "histWheal": "12",
    "histFlare": "20",
    "allerWheal": "5",
    "allerFlare": "15"
  },
  "expect": [
    "但小于阳性对照的1/2"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/calc-1",
  "inputs": {
    "rhinorrhea": "3",
    "sneeze": "3",
    "itch": "2",
    "congestion": "3"
  },
  "expect": [
    "TNSS 总分： 11 分（0-12 分） 症状程度： 极重度"
  ],
  "ref": "TNSS 四症状各 0-3 分（rhinorrhea/sneeze/itch/congestion select）；注入 3/3/2/3 ⇒ 总分 11 > 9 ⇒ classify() 返回「极重度」并输出「建议耳鼻喉科就诊，评估药物治疗方案。」。默认 0/0/0/0 ⇒ 总分 0「轻度」。原 expect「0-12」是结果区固定文案「（0-12 分）」，与输入无关（常量型逃生项）。"
},
{
  "slug": "ent/caloric-test",
  "inputs": {
    "rw": "38",
    "lw": "22",
    "rc": "20",
    "lc": "18"
  },
  "expect": [
    "18.4%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/eustachian-tube",
  "clicks": [
    "selections.valsalva_tm=0;selections.valsalva_subj=0;selections.tympanogram=0;selections.reflex_ipsi=1;selections.toynbee=0;symptomSelected={'耳闷胀感':1};symptomNone=false;calc()"
  ],
  "expect": [
    "需手术干预，明确病因（肿瘤、腺样体肥大等）"
  ],
  "ref": "5 项客观检查（valsalva_tm/valsalva_subj/tympanogram/reflex_ipsi/toynbee）默认合计 16/18 ⇒「0级·正常」；clicks 置 0/0/0/1/0 并把症状「耳闷胀感」计 1 分（symptomNone=false）⇒ 综合评分 0-1=-1→0 ⇒「IV级·极重度障碍」+「需手术干预」。默认态为「0级·正常」。原 expect「(89%)」是默认态进度条 16/18=88.9% 的文案（常量型逃生项）。"
},
{
  "slug": "ent/facial-nerve-hb",
  "clicks": [
    "grade=5;calc()"
  ],
  "expect": [
    "重度面神经功能障碍。需行面神经电图评估，若变性>90%需考虑面神经减压术。需眼部保护。预后较差。"
  ],
  "ref": "页面顶层 var grade 默认 1 ⇒ House-Brackmann I级·正常；clicks 置 grade=5 后 calc() ⇒ V级·重度功能障碍及其治疗建议「需行面神经电图评估，若变性>90%需考虑面神经减压术」。默认态只有 I级 文案。原 expect「面神经功能障碍程度」是结果区固定小标题（常量型逃生项）。"
},
{
  "slug": "ent/fistula-test",
  "inputs": {
    "positivePressure": "450",
    "negativePressure": "200"
  },
  "expect": [
    "正压450mmH"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/gag-reflex",
  "clicks": [
    "grade=4;calc()"
  ],
  "expect": [
    "咽反射极度敏感，严重影响口腔检查和治疗操作。可能与心理因素、焦虑或神经官能症有关。"
  ],
  "ref": "var grade 默认 2 ⇒「2级·反射正常」；clicks 置 grade=4 ⇒ 4级·极度敏感及临床建议「进行口腔操作前可考虑表面麻醉或行为干预」。原 expect「2级」恰是默认档名（常量型逃生项）。"
},
{
  "slug": "ent/grbas-scale",
  "clicks": [
    "scores.G=3;scores.R=3;scores.B=2;scores.A=1;scores.S=0;calc()"
  ],
  "expect": [
    "嗓音重度异常，G评分多为3分，严重影响交流，需综合治疗",
    "粗糙声明显（声带振动不规则，可见于声带息肉、肿瘤等）"
  ],
  "ref": "var scores={G,R,B,A,S} 默认全 0 ⇒ 总分 0/15「正常」；clicks 置 3/3/2/1/0 ⇒ 总分 9 ⇒「重度异常」+ 特征分析两条（R>=2 粗糙声明显、B>=2 气息声明显）。原 expect「总评(0-3)」是 stat-card 的 lbl（常量型逃生项）。"
},
{
  "slug": "ent/hearing-loss-classification",
  "inputs": {
    "ac500": "38",
    "ac1000": "30",
    "ac2000": "35",
    "ac4000": "40",
    "bc500": "10",
    "bc1000": "15",
    "bc2000": "15",
    "bc4000": "20"
  },
  "expect": [
    "38"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/laryngeal-nerve",
  "inputs": {
    "f0": "180",
    "jitter": "2.5",
    "shimmer": "5.0",
    "nhr": "0.20",
    "hnr": "15",
    "mpt": "8"
  },
  "expect": [
    "180"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/lund-kennedy-score",
  "clicks": [
    "scores.L={polyp:2,edema:2,discharge:2,scar:2,crust:2};scores.R={polyp:2,edema:2,discharge:2,scar:2,crust:2};calc()"
  ],
  "expect": [
    "黏膜炎症严重，建议行鼻内镜手术"
  ],
  "ref": "var scores={L:{polyp,edema,discharge,scar,crust}, R:{…}} 默认全 0 ⇒ 总分 0/20「轻度」；clicks 置双侧各 2 ⇒ 总分 20 > 13 ⇒「重度」+「黏膜炎症严重，建议行鼻内镜手术」。原 expect「左侧(0-10)」是 stat-card 的 lbl（常量型逃生项）。"
},
{
  "slug": "ent/lund-mackay-score",
  "clicks": [
    "scores.right={maxillary:2,anterior_ethmoid:2,posterior_ethmoid:2,sphenoid:2,frontal:2,omc:2};scores.left={maxillary:2,anterior_ethmoid:2,posterior_ethmoid:2,sphenoid:1,frontal:1,omc:2};calc()"
  ],
  "expect": [
    "全组鼻窦严重受累",
    "强烈建议尽早手术，术后定期随访"
  ],
  "ref": "var scores={right:{6 组鼻窦}, left:{…}} 默认全 0 ⇒ 0/24「轻度」；clicks 置右 12（maxillary 2 等全 2）、左 10 ⇒ 总分 22 > 20 ⇒「极重度」+「全组鼻窦严重受累」+「强烈建议尽早手术」。原 expect「24」是分母「/ 24 分」（常量型逃生项）。"
},
{
  "slug": "ent/nasal-resistance",
  "inputs": {
    "lp": "225",
    "lv": "350",
    "rp": "150",
    "rv": "400"
  },
  "expect": [
    "0.237"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/pure-tone-audiometry",
  "inputs": {
    "ptDur": "1050",
    "ptVol": "100"
  },
  "expect": [
    "1050"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/tdi-score",
  "inputs": {
    "scoreT": "9",
    "scoreD": "10",
    "scoreI": "11"
  },
  "expect": [
    "62.5%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/temporal-resolution-hearing",
  "inputs": {
    "trGapSlider": "20",
    "trModFreq": "4",
    "trModDepth": "30",
    "trGapMode": "manual"
  },
  "expect": [
    "manual"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/tinnitus-matching",
  "inputs": {
    "loudness": "8",
    "masking": "50"
  },
  "expect": [
    "42"
  ],
  "ref": "auto-restore"
},
{
  // 原为 no_inputs 弱用例：expect「26-50%」来自 grade=2 的默认档，与勾选无关。
  "slug": "ent/tonsil-grading",
  "checkIds": [
    "s1",
    "s4"
  ],
  "expect": [
    "存在手术指征（反复发作≥3次/年、扁桃体周围脓肿史）"
  ],
  "ref": "grade 默认 2（II度）；勾选 s1(反复扁桃体炎)+s4(周围脓肿史) → surgReason 依序拼接为「反复发作≥3次/年、扁桃体周围脓肿史」。回退默认（未勾选、grade=2）→ 「目前暂无明确手术指征」，该串不命中。"
},
{
  "slug": "ent/tympanic-perforation",
  "inputs": {
    "perfD": "6",
    "perfW": "2",
    "tmD": "10",
    "tmW": "9"
  },
  "expect": [
    "13.3%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/tympanometry",
  "inputs": {
    "tpp": "0",
    "sc": "3.7",
    "ecv": "1.0",
    "grad": "40"
  },
  "expect": [
    "3.70"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ent/vocal-cord-assessment",
  "clicks": [
    "sel.mobility='固定';sel.position='中间位';sel.side='双侧';sel.closure='无法闭合';calc()"
  ],
  "expect": [
    "声带完全麻痹（III度）",
    "双侧声带麻痹可致喉梗阻及呼吸困难，需评估气道安全性，必要时行气管切开"
  ],
  "ref": "var sel={mobility:正常,side:左侧,position:正中位,closure:完全闭合,arytenoid:活动正常} 默认 ⇒「声带运动正常」；clicks 置 mobility=固定/position=中间位/side=双侧/closure=无法闭合 ⇒「声带完全麻痹（III度）」+「双侧声带麻痹可致喉梗阻…行气管切开」+「声门闭合不全…声带内移术」。原 expect「声带运动功能正常」是默认档 advice 片段（常量型逃生项）。"
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
  console.log("==== ent calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
