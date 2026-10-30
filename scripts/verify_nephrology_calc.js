#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "nephrology/aki-kdigo",
  "inputs": {
    "baselineScr": "120",
    "currentScr": "180",
    "urine": "0.3",
    "duration": "8"
  },
  "expect": [
    "1.50倍基线"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/ca-p-product",
  "inputs": {
    "calcium": "5.2",
    "phosphorus": "1.8",
    "albumin": "35",
    "pth": "300"
  },
  "expect": [
    "5.30",
    "钙磷乘积 9.54 mmol²/L² → 落在 显著升高"
  ],
  "ref": "校正血钙 = 5.2 + 0.02×(40−35) = 5.30 mmol/L；Ca×P = 5.30 × 1.8 = 9.54 mmol²/L² ⇒ 落在「显著升高」带（≥5.5）"
},
{
  "slug": "nephrology/calc-1",
  "inputs": {
    "scrValue": "150",
    "age": "66",
    "sex": "female"
  },
  "expect": [
    "eGFR： 31.0 mL/min/1.73m² CKD 分期： G3b（中-重度下降）"
  ],
  "ref": "独立复算：Scr 150 μmol/L ÷88.4 = 1.697 mg/dL，女性、66 岁，CKD-EPI 2021 ⇒ eGFR ≈ 31.0 ⇒ G3b（30–44）。⚠ 原用例只断言单位回显 'mgdl'（输入值回显、零判别力），已改为 eGFR 数值+分期串。默认态预填 88.4/58/男 ⇒ eGFR 明显高于 31，不含该串 ⇒ 无逃生。"
},
{
  "slug": "nephrology/ckd-staging",
  "inputs": {
    "egfr": "68",
    "uacr": "150"
  },
  "expect": [
    "68",
    "eGFR 68 mL/min/1.73m² → 落在 G2 轻度↓（健康参考 ≥90）",
    "UACR 150 mg/g → 落在 A2 微量"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/ckd-staging",
  "inputs": {
    "egfr": "28",
    "uacr": "400",
    "baseDate": "2024-01-15"
  },
  "expect": [
    "随访计划（基线 2024-01-15，很高风险）",
    "第1次复查：2024-05-15"
  ],
  "ref": "随访计划生成器（03-52）：egfr=28→G4、uacr=400→A3 ⇒ 很高风险 ⇒ 间隔 4 个月×3 次。2024-01-15 +4/+8/+12 个月 = 2024-05-15 / 2024-09-15 / 2025-01-15（2024 闰年含 2/29 不影响月加法）。默认 baseDate 为空 ⇒ 日程块不渲染，两条锚均随注入出现、零交集。"
},
{
  "slug": "nephrology/creatinine-clearance",
  "inputs": {
    "uCr24": "15",
    "uVol": "1500",
    "scr": "100",
    "bsa": "1.73"
  },
  "expect": [
    "(10000",
    "校正Ccr 104.2 mL/min → 落在 正常"
  ],
  "ref": "Ccr=(10000×1.04)/100=104.2 mL/min（BSA 1.73 无需校正）；参考区间定位：落在「正常」带（80–120 mL/min）"
},
{
  "slug": "nephrology/dialysis-ktv",
  "inputs": {
    "preBUN": "38",
    "postBUN": "8",
    "duration": "240",
    "weightLoss": "2",
    "postWeight": "65"
  },
  "expect": [
    "透析充分（理想）"
  ],
  "ref": "spKt/V = -ln(8/38 - 0.008×4) + (4-3.5×0.2105)×2/65 ≈ 1.82 ≥ 目标1.2+0.2=1.4（freq 默认3次/周）→ 透析充分（理想）。原用例 expect 为派生公式片段「(4-3.5×0.2105)×2/65」，偏弱，改为充分性结论强串；默认参数算得不同 spKt/V，与「透析充分（理想）」零交集。S3 标尺 refBar(#ktvRefBar) 已加（bands: 不足/临界/达标/理想，max2.5）。"
},
{
  "slug": "nephrology/diuretic-conversion",
  "inputs": {
    "fromDose": "60"
  },
  "expect": [
    "60.0mg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/edema-grading",
  "inputs": {
    "depth": "7",
    "recovery": "30"
  },
  "expect": [
    "4+"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/hematuria-source",
  "inputs": {
    "rbcCount": "50",
    "dysmorphic": "113",
    "g1": "8",
    "protein": "1.2"
  },
  "expect": [
    "畸变红细胞113%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/jixingshensunshang-kdigo-fenqi",
  "inputs": {
    "baseline": "120",
    "current": "180",
    "weight": "70",
    "uo6": "",
    "uo12": "",
    "uo24": ""
  },
  "expect": [
    "1.5-1.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/manager-1",
  "inputs": {
    "patientAge": "83"
  },
  "expect": [
    "83"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/microalbuminuria",
  "inputs": {
    "uacrVal": "68",
    "uacrMmol": "5.1",
    "concVal": "30",
    "h24Val": "40"
  },
  "expect": [
    "68.0",
    "68.0 mg/g → 落在 微量"
  ],
  "ref": "UACR 68 mg/g 落在微量白蛋白尿带（30–300 mg/g）；参考区间定位文本随 uacrVal 联动"
},
{
  "slug": "nephrology/nephrotic-syndrome",
  "inputs": {
    "age": "young"
  },
  "expect": [
    "但成人起效慢(需8-16周)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/peritoneal-equilibrium",
  "inputs": {
    "dialysateCr": "675",
    "plasmaCr": "800",
    "dialysateGlu": "25",
    "initialGlu": "75",
    "dpAlb": "0.03"
  },
  "expect": [
    "短时多次交换(每次留腹1-2h)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/proteinuria-24h",
  "inputs": {
    "protein24h": "5.5",
    "uVol": "1500"
  },
  "expect": [
    "5.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/renal-anemia-epo",
  "inputs": {
    "hgb": "128",
    "weight": "65",
    "ferritin": "200",
    "tsat": "25"
  },
  "expect": [
    "当前HGB(128)接近或达到目标(110)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/renal-biopsy",
  "inputs": {
    "lmGlomerular": "mesangial_prolif"
  },
  "expect": [
    "mesangial_prolif"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/renal-tubular-acidosis",
  "inputs": {
    "bloodpH": "11.3",
    "hco3": "17",
    "urinepH": "6.5",
    "potassium": "3.2",
    "uag": "25",
    "feHco3": "2"
  },
  "expect": [
    "11.3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/shenxiaoqiulvguolv-24h-jiganqingchu-ccr",
  "inputs": {
    "scr": "120",
    "ucr": "8.8",
    "vol": "1500",
    "height": "170",
    "weight": "65",
    "age": "40"
  },
  "expect": [
    "76.4"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/urine-electrolyte",
  "inputs": {
    "uNa": "75",
    "uK": "40",
    "uCl": "60",
    "uVol": "1500",
    "sNa": "138",
    "sCr": "90",
    "uCr": "8"
  },
  "expect": [
    "0.61%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/urine-osmolality",
  "inputs": {
    "uOsm": "525",
    "sOsm": "295",
    "uVol": "60"
  },
  "expect": [
    "-0.78"
  ],
  "ref": "auto-restore"
},
{
  "slug": "nephrology/vascular-calcification",
  "inputs": {
    "l1a": "4",
    "l1p": "0",
    "l2a": "2",
    "l2p": "1",
    "l3a": "2",
    "l3p": "1",
    "l4a": "1",
    "l4p": "0"
  },
  "expect": [
    "总分10分"
  ],
  "ref": "auto-restore"
}
,
{
  "slug": "nephrology/uacr",
  "inputs": { "albumin": "30", "ucr": "10" },
  "expect": ["26.5 UACR (mg/g)"],
  "ref": "注入非默认白蛋白30/尿肌酐10（默认35/8.8）→ UACR=30/(8.8×0.113)=30/0.994≈26.5 mg/g（默认35.2）；26.5 为转换后数值，默认态不含，0 逃生。"
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

  console.log("==== nephrology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
