#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "tcm-chemistry/calc-44",
  "inputs": {
    "K": "7",
    "v0": "100",
    "v": "25",
    "target": "99"
  },
  "expect": ["4.552358675"],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/capsule-filling",
  "inputs": {
    "height": "45",
    "diameter": "80",
    "bulkDensity": "0.5",
    "tapDensity": "0.7",
    "targetWeight": "300",
    "fillDensity": "0.5",
    "moisture": "5"
  },
  "expect": [
    "arctan(45/40.0)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/chromatography-gradient",
  "inputs": {
    "colDiameter": "6",
    "sampleWeight": "2"
  },
  "expect": ["alkaloid\n1:50\n6\n2\n硅胶柱层析方案 6 柱径(cm) 7.1 装柱高度(cm) 200 柱体积BV(mL) 100 硅胶用量(g) 装柱参数： 1:50 硅胶（100g），柱径6cm，装柱高度约7.1cm，柱体积约200mL（1BV）。 注意： 柱高/柱径比建议≥10:1，当前为1.2:1，建议减小柱径或增加硅胶量。 梯度洗脱方案（生物碱） 洗脱体系：石油醚 → 乙酸乙酯 1 2 3 4 5 6 7 1 石油醚 : 乙酸乙酯 = 100:0 洗脱体积：2-3BV（约400 mL）| 目标：极性杂质/色素 2 石油醚 : 乙酸乙酯 = 90:10 洗脱体积：2BV（约400 mL）| 目标：低极性生物碱 3 石油醚 : 乙酸乙酯 = 80:20 洗脱体积：2BV（约400 mL）| 目标：中等极性生物碱 4 石油醚 : 乙酸乙酯 = 70:30 洗脱体积：2BV（约400 mL）| 目标：中等极性生物碱 5 石油醚 : 乙酸乙酯 = 50:50 洗脱体积：3BV（约600 mL）| 目标：高极性生物碱 6 石油醚 : 乙酸乙酯 = 0:100 洗脱体积：3BV（约600 mL）| 目标：强极性生物碱 7 石油醚 : 乙酸乙酯 = MeOH冲洗 洗脱体积：2BV（约400 mL）| 目标：残留强极性成分 改性建议： 可加0.5%-1%二乙胺改性 操作要点： 1. 硅胶活化：105°C活化30min 2. 干法/湿法装柱，确保无气泡、无裂痕 3. 上样浓度10%-20%，尽量薄层 4. 流速控制：1-2 BV/h 5. 每BV收集1管，TLC监控合并"],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/concentration-calc",
  "inputs": {
    "targetTemp": "75",
    "vacuum": "",
    "atm": "760"
  },
  "expect": [
    "288.5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/content-assay",
  "inputs": {
    "stdMass": "15",
    "stdConc": "0.50",
    "isMass": "8.00",
    "isConc": "0.40",
    "stdArea": "500000",
    "isArea": "450000",
    "factor": "0.889",
    "sampleMass": "500",
    "sampleIS": "8.00",
    "sampleVol": "25",
    "sampleArea": "480000",
    "sampleISArea": "440000",
    "lossOnDrying": "0"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/crystallization-yield",
  "inputs": {
    "feedAmount": "15",
    "dissolveTemp": "70",
    "crystalTemp": "10",
    "solHigh": "8.5",
    "solLow": "0.8",
    "solventVol": "120",
    "lossRate": "5"
  },
  "expect": [
    "120mL溶剂在70°C仅能溶10.20g"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/detector-4",
  "inputs": {
    "herb1": "甘草_X",
    "herb2": "甘遂"
  },
  "expect": [
    "甘草_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/extraction-counts",
  "inputs": {
    "K": "8",
    "ratio": "0.5",
    "target": "95",
    "total": "100"
  },
  "expect": [
    "1/(1+8×0.5)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/extraction-solvent",
  "inputs": {
    "compoundType": "alkaloid_salt"
  },
  "expect": [
    "可用0.5%-1%盐酸/硫酸乙醇溶液提取"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/fingerprint-similarity",
  "inputs": {
    "refData": "80,120,60,40,25",
    "s1": "82,118,62,38,26",
    "s2": "70,140,50,55,20",
    "s3": "95,100,80,30,35",
    "s4": "60,150,45,60,15"
  },
  "clicks": ["calc()"],
  "expect": [
    "0.9547",
    "0.8863",
    "0.9380 平均相关系数"
  ],
  "ref": "独立复算 Pearson：ref 均值 65（dx=15,55,−5,−25,−40，Σdx²=5500）；"
     + "s2 均值 67（dy=3,73,−17,−12,−47，Σdy²=7980），Σdxdy=6325 ⇒ r=6325/√(5500×7980)=0.9547；"
     + "s3 均值 68（dy=27,32,12,−38,−33，Σdy²=4430），Σdxdy=4375 ⇒ r=4375/√(5500×4430)=0.8863；"
     + "四样平均=(0.9985+0.9547+0.8863+0.9126)/4=0.9380。原 7 峰数据为页面默认态。",
},
{
  "slug": "tcm-chemistry/granule-quality",
  "inputs": {
    "totalWt": "150",
    "s1": "2",
    "s2": "15",
    "s3": "55",
    "s4": "20",
    "s5": "5",
    "s6": "3",
    "moisture": "4.0",
    "rsd": "3.0",
    "assay": "98",
    "sizeScore": "5"
  },
  "expect": [
    "2680"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/hplc-optimization",
  "inputs": {
    "colLength": "375",
    "colID": "4.6",
    "flowRate": "1.0",
    "t0": "2.5",
    "kPrime": "3.0",
    "gradSlope": "0",
    "rt_plate": "10.5",
    "peakWidth": "0.5",
    "t0_plate": "2.5",
    "L_plate": "250",
    "tr1": "8.5",
    "tr2": "10.2",
    "w1": "0.4",
    "w2": "0.5"
  },
  "expect": [
    "6.23"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/impurity-limit",
  "inputs": {
    "sampleWt": "150",
    "sampleVol": "10",
    "stdWt": "1",
    "stdVol": "10",
    "sampleSpot": "10",
    "stdSpot": "10",
    "sampleSpotIntensity": "3",
    "stdSpotIntensity": "5",
    "stdConcSemi": "0.1",
    "sampleAmount": "100"
  },
  "expect": [
    "0.150000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/metabolite-prediction",
  "inputs": {
    "mw": "405"
  },
  "expect": [
    "405"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/ointment-release",
  "inputs": {
    "concA": "30",
    "solCs": "5",
    "diffD": "0.001",
    "time": "6",
    "thickness": "0.1"
  },
  "expect": [
    "((2×30-5)×5×0.00050×6)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/pharmacokinetics",
  "inputs": {
    "dose": "150",
    "bio": "50",
    "vd": "50",
    "cl": "5",
    "ka": "1.0",
    "tau": "12",
    "weight": "60"
  },
  "expect": [
    "(75.00×1)/(50×0.9000)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/response-factor",
  "inputs": {
    "refName": "黄芩苷",
    "refConc": "3.1",
    "refArea": "500000",
    "cn${i}": "${d.name}",
    "cc${i}": "${d.conc}",
    "ca${i}": "${d.area}",
    "cq${i}": "${(d.conc*10).toFixed(2)}"
  },
  "expect": [
    "161290"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/solubility-guide",
  "inputs": {
    "searchBox": "zzz"
  },
  "expect": [
    "未找到匹配成分"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部成分，不产此串）"
},
{
  "slug": "tcm-chemistry/stability-test",
  "inputs": {
    "ea": "125.14",
    "accelTemp": "40",
    "accelTime": "6",
    "storageTemp": "25",
    "accelDeg": "2.5",
    "accelMonths": "6",
    "interDeg": "1.0",
    "interMonths": "12",
    "specLimit": "10"
  },
  "expect": [
    "125.1×1000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/structure-identification",
  "inputs": {
    "irInput": "3400, 2920, 1700, 1600, 1520, 1450, 1280, 1070",
    "uvInput": "220, 270, 310",
    "nmrInput": "12.5, 9.8, 7.5, 7.3, 6.9, 6.5, 3.8",
    "msM": "405",
    "msFrag": "242, 224, 152, 124, 96"
  },
  "expect": [
    "(丢失163)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/toxicity-dose",
  "inputs": {
    "dose": "750",
    "humanWeight": "60",
    "ld50": "500"
  },
  "expect": ["mouse\nhuman\n750\nbsa\n60\n100\n等效剂量换算 750 小鼠 LD50(mg/kg) 60.81 人等效(mg/kg) 60.81 人等效剂量(mg/kg) 0.6081 安全起始剂量(mg/kg) 换算结果： 小鼠 LD50 = 750 mg/kg 体表面积法：Dose₂ = Dose₁ × (Km₁/Km₂) = 750 × (3/37) 人 等效剂量 = 60.81 mg/kg 人体等效剂量(HED)估算： HED = 动物剂量 × (Km动物 / Km人) = 750 × (3/37) = 60.81 mg/kg 安全起始剂量(MRD) = HED / 安全系数 = 60.81 / 100 = 0.6081 mg/kg 60kg成人总剂量 = 0.6081 × 60 = 36.49 mg 安全系数说明： ×10：同种动物重复实验，毒性明确 ×100：常规新药研究（默认） ×1000：毒性未知或高毒性物质 注意：实际临床起始剂量还需考虑药效学、药代学数据 常用Km值参考： 小鼠Km=3 (20g) | 大鼠Km=5.9 (150g) | 豚鼠Km=8 (400g) 家兔Km=12 (1.8kg) | 犬Km=20 (10kg) | 人Km=37 (60kg)\n500\noral\n毒性分级结果 500 LD50(mg/kg) 口服 给药途径 中等毒 毒性等级 毒性分级： 中等毒 需较大剂量才致命，如小檗碱(LD50约~400mg/kg) WHO经口急性毒性分级表 分级 LD50(mg/kg) 说明 剧毒 ≤1 极微量致命 高毒 1-50 少量致命 中等毒 50-500 较大剂量致命 低毒 500-5000 相对安全 微毒/无毒 >5000 基本无毒 中药常见毒性成分参考： 乌头碱 LD50≈0.3mg/kg(剧毒) | 士的宁 LD50≈2mg/kg(高毒) 马钱子碱 LD50≈50mg/kg(高毒) | 苦参碱 LD50≈150mg/kg(中等毒) 小檗碱 LD50≈400mg/kg(中等毒) | 黄芩苷 LD50>5000mg/kg(无毒)"],
  "ref": "auto-restore"
},
{
  "slug": "tcm-chemistry/compatibility-taboo",
  "clicks": ["document.getElementById('herbA').value='乌头';document.getElementById('herbB').value='半夏';checkClassic()"],
  "expect": ["乌头 与 半夏", "乌头组"],
  "ref": "⚠ 该页两个 select 的选项由 initHerbs() 在 DOMContentLoaded 时填充，而 harness step-3 兜底会再调 initHerbs ⇒ inputs 字段注入会被冲回默认（甘草/甘遂）。改用 clicks 在页面作用域设值并直接调 checkClassic()（step-2.5 立即判定，不等 step-3）。注入「乌头 + 半夏」命中十八反乌头组（乌头反半夏/瓜蒌/贝母/白蔹/白及）⇒ 输出『禁止配伍！乌头 与 半夏 属于 十八反』。⚠ expect 只取『乌头 与 半夏』+『十八反』：默认态（甘草/甘遂）虽也含『十八反』，但不含『乌头 与 半夏』，判别器实测两条均会变红（OR 语义下同态需全部命中才逃生）。"
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

  console.log("==== tcm-chemistry calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
