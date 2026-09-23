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
  "inputs": {},
  "expect": [
    "0-12"
  ],
  "ref": "auto-restore(default)"
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
  "inputs": {},
  "expect": [
    "(89%)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ent/facial-nerve-hb",
  "inputs": {},
  "expect": [
    "面神经功能障碍程度"
  ],
  "ref": "auto-restore(default)"
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
  "inputs": {},
  "expect": [
    "2级"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ent/grbas-scale",
  "inputs": {},
  "expect": [
    "总评(0-3)"
  ],
  "ref": "auto-restore(default)"
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
  "inputs": {},
  "expect": [
    "左侧(0-10)"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "ent/lund-mackay-score",
  "inputs": {},
  "expect": [
    "24"
  ],
  "ref": "auto-restore(default)"
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
  "inputs": {},
  "expect": [
    "声带运动功能正常"
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
  console.log("==== ent calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
