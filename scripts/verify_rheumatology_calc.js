#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "rheumatology/anti-ccp",
  "inputs": {
    "ccp": "120",
    "rf": "45",
    "crp": "12",
    "esr": "28"
  },
  "expect": [
    "观察滴度变化"
  ]
},
{
  "slug": "rheumatology/complement-level",
  "inputs": {
    "c3": "0.5",
    "c4": "0.08",
    "ch50": "15"
  },
  "expect": [
    "发数周"
  ]
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
  "slug": "rheumatology/igg4-level",
  "inputs": {
    "igg4": "5.8",
    "igg": "18",
    "ige": "350",
    "eos": "0.6",
    "c3": "1.3"
  },
  "expect": [
    "病理诊断"
  ]
},
{
  "slug": "rheumatology/il6-inflammation",
  "inputs": {
    "il6": "25",
    "crp": "35",
    "esr": "45",
    "ferritin": "500",
    "plt": "450",
    "fib": "5.5"
  },
  "expect": [
    "肝酶"
  ]
},
{
  "slug": "rheumatology/lupus-anticoagulant",
  "inputs": {
    "dsc": "45",
    "dcc": "35",
    "dnm": "32",
    "ssc": "42",
    "scc": "35",
    "snm": "33"
  },
  "expect": [
    "但需评估血栓风险因素"
  ]
},
{
  "slug": "rheumatology/mda5-antibody",
  "inputs": {
    "ferritin": "800",
    "ck": "150",
    "crp": "15",
    "ldh": "300"
  },
  "expect": [
    "抑制剂"
  ]
},
{
  "slug": "rheumatology/sapho-syndrome",
  "inputs": {
    "duration": "3",
    "vas": "5"
  },
  "expect": [
    "评估治疗反应"
  ]
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
