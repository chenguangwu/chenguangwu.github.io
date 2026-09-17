#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pulmonology/anti-tb-dosing",
  "inputs": {
    "wt": "55",
    "age": "45"
  },
  "expect": [
    "顺序"
  ]
},
{
  "slug": "pulmonology/calc-48",
  "inputs": {
    "pao2": "80",
    "fio2": "40",
    "map": "",
    "paco2": ""
  },
  "expect": [
    "200 P/F"
  ]
},
{
  "slug": "pulmonology/feigongneng-fev1-fvc-fenji",
  "inputs": {
    "fev1": "2.1",
    "fvc": "3.5",
    "fev1pred": "3.0",
    "fvcpred": "",
    "age": "60"
  },
  "expect": [
    "60.0% FEV1/FVC"
  ]
},
{
  "slug": "pulmonology/light-criteria",
  "inputs": {
    "pfProt": "42",
    "sProt": "65",
    "pfLdh": "320",
    "sLdh": "200",
    "sLdhUl": "250"
  },
  "expect": [
    "及肺栓塞等病因"
  ]
},
{
  "slug": "pulmonology/niv-settings",
  "inputs": {
    "vt": "8",
    "ibw": "60",
    "ph": "7.28"
  },
  "expect": [
    "一般"
  ]
},
{
  "slug": "pulmonology/oxygenation-index",
  "inputs": {
    "pao2": "65",
    "fio2": "40",
    "spo2": "92"
  },
  "expect": [
    "不可直接定级"
  ]
},
{
  "slug": "pulmonology/pneumothorax",
  "inputs": {
    "a": "2",
    "b": "3",
    "c": "2"
  },
  "expect": [
    "外科干预"
  ]
},
{
  "slug": "pulmonology/pulmonary-function",
  "inputs": {
    "fev1": "2.10",
    "fvc": "3.50",
    "fev1pp": "68",
    "fvcpp": "88"
  },
  "expect": [
    "评估吸入糖皮质激素指"
  ]
},
{
  "slug": "pulmonology/pulmonary-rehab",
  "inputs": {
    "mip": "45",
    "mep": "80",
    "age": "65"
  },
  "expect": [
    "耐量与生活质量"
  ]
},
{
  "slug": "pulmonology/respiratory-failure",
  "inputs": {
    "pao2": "55",
    "paco2": "62",
    "fio2": "21",
    "age": "65"
  },
  "expect": [
    "麻醉"
  ]
},
{
  "slug": "pulmonology/analysis-14",
  "inputs": {
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/bronchoscopy-grading",
  "inputs": {
    "tumorType": "1"
  },
  "expect": [
    "1级"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/copd-cat",
  "inputs": {
    "q'+i+'": "'+s+'"
  },
  "expect": [
    "+s+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/curb65",
  "inputs": {},
  "expect": [
    "CURB-65总分"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "pulmonology/gina-asthma",
  "inputs": {
    "a1": "2"
  },
  "expect": [
    "6/25"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/lung-cancer-tnm",
  "inputs": {
    "t": "T1b"
  },
  "expect": [
    "T1b"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/lung-rads",
  "inputs": {
    "size": "14"
  },
  "expect": [
    "14.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/rater-13",
  "inputs": {},
  "expect": [
    "近4周内手术史或近3天以上制动/卧床"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "pulmonology/self-assess-3",
  "inputs": {
    "q'+i+'": "'+opt.v+'"
  },
  "expect": [
    "+opt.v+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/smoking-cessation",
  "inputs": {
    "q1": "2"
  },
  "expect": [
    "尼古丁替代贴片(联合口香糖)或伐尼克兰(0.5mg渐增至1mg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/sputum-analysis",
  "inputs": {
    "vol": "45"
  },
  "expect": [
    "45mL/24h"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/stop-bang",
  "inputs": {},
  "expect": [
    "0/8"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "pulmonology/tb-resistance",
  "inputs": {
    "smear": "1+"
  },
  "expect": [
    "1+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/vibration-percussion",
  "inputs": {
    "lobe": "rul_post"
  },
  "expect": [
    "叩击同侧肩胛骨上方"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pulmonology/wells-pe",
  "inputs": {},
  "expect": [
    "1.3%)"
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
  console.log("==== pulmonology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
