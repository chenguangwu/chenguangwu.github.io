#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "forensic-medicine/abuse-pattern",
  "inputs": {
    "age": "3",
    "victim": "elder"
  },
  "expect": [
    "3-4期"
  ],
  "ref": "auto-restore"
},
  // 注：forensic-medicine/analysis-15 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
{
  "slug": "forensic-medicine/blood-stain-screening",
  "inputs": {
    "preTest": "phenolphthalein"
  },
  "expect": [
    "酚酞试验(Kastle-Meyer法)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/bloodstain-pattern",
  "inputs": {
    "longAxis": "15",
    "shortAxis": "6",
    "aX": "0",
    "aY": "50",
    "aAngle": "45",
    "bX": "80",
    "bY": "50",
    "bAngle": "135",
    "aImpact": "30",
    "bImpact": "30",
    "stainHeight": "100"
  },
  "expect": [
    "arcsin(0.400)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/bone-age-estimation",
  "inputs": {
    "femurLen": "75",
    "crl": "120",
    "carpalNum": "3",
    "metaNum": "5",
    "radiusGrade": "5",
    "metaGrade": "4",
    "phalGrade": "5"
  },
  "expect": ["infant\n婴幼儿期骨龄推断（骨化中心计数法） 腕骨出现数（0-8） 掌指骨骨骺出现数（0-18） 通过腕部X线计数骨化中心数量推断年龄\nmale\n3\n5\n推断生物学年龄 3.4 岁 估算范围：2.4 ~ 4.9 岁（性别：男） 腕骨计数法 + 骨化中心综合评估 推断方法 推算详情 腕骨计数推算：4.0岁；掌指骨骺推算：2.5岁 注意事项 • 骨龄与实际日历年龄存在差异，受营养、内分泌、疾病影响 • 女性骨发育通常比男性早1-2年 • 成人骨龄推断标准差较大（±5-12年），应多方法综合使用 • 耻骨联合面法适用于25-60岁，超出此范围精度显著下降 • 推荐结合牙齿、颅缝、肋骨等多指标综合判断\n75\n120\n5\n4\n5"],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/burn-assessment",
  "inputs": {
    "palmArea": "0",
    "totalArea": "30",
    "thirdArea": "10",
    "burnDepth": "2s"
  },
  "expect": [
    "1-2周愈合"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/death-time-estimation",
  "inputs": {
    "rectalTemp": "48",
    "ambientTemp": "20",
    "bodyWeight": "70"
  },
  "expect": ["48\n20\n70\n0\n0.7\n1.0\n综合估算死后经过时间 0 分钟 估算范围：0 分钟 ~ -2146 分钟 0.0 Glaister法 (h) -38.6 Henssge法 (h) -10.8 温度差 ΔT (°C) 0.400 冷却常数 K 角膜混浊参考 当前判定： 透明 → 对应死后时间约 0-2 小时 ⚠️ 直肠温度≥37°C，尸体可能尚未充分冷却或存在发热因素 输入参数：Tr=48°C, Ta=20°C, 体重=70kg, 穿着系数=0.7, 环境系数=1\n— 0h — 1h — 2h — 3h — 4h — 6h — 8h — 10h — 12h — 16h — 20h — 24h\nundefined"],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/detector-10",
  "inputs": {
    "diatomCount": "23",
    "diatomType": "3",
    "waterType": "8"
  },
  "expect": [
    "23"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/dna-str-typing",
  "inputs": {
    "mixedAlleles": "10,11,12,13_X",
    "known1": "10,12",
    "known2": "11,13",
    "af_' + i + '": "",
    "mo_' + i + '": "",
    "ch_' + i + '": ""
  },
  "expect": [
    "13_X)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/drowning-diatom",
  "inputs": {
    "waterDiatom": "medium"
  },
  "expect": [
    "medium"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/electrocution-injury",
  "inputs": {
    "currentType": "dc"
  },
  "expect": [
    "dc"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/fall-injury",
  "inputs": {
    "fallHeight": "15",
    "bodyWeight": "70",
    "age": "40"
  },
  "expect": [
    "17.1"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/fracture-age",
  "inputs": {
    "lineClarity": "slight-blur"
  },
  "expect": [
    "2/5"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/hair-identification",
  "inputs": {
    "diameter": "120"
  },
  "expect": [
    "120"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/hanging-marks",
  "inputs": {
    "grooveWidth": "4.5"
  },
  "expect": [
    "4.5cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/livor-mortis",
  "inputs": {
    "blanching": "partial"
  },
  "expect": [
    "2/3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/poisoning-screening",
  "inputs": {
    "route": "inhalation"
  },
  "expect": [
    "inhalation"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/rigor-mortis",
  "inputs": {
    "bodyCondition": "muscular"
  },
  "expect": [
    "肌肉发达者尸僵强且持久"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/semen-stain-confirmation",
  "inputs": {
    "preTest": "uv"
  },
  "expect": [
    "紫外线照射试验"
  ],
  "ref": "auto-restore"
},
{
  "slug": "forensic-medicine/wound-description",
  "inputs": {
    "location": "头部",
    "length": "5",
    "width": "1",
    "bluntShape": "linear"
  },
  "expect": [
    "linear"
  ],
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

  console.log("==== forensic-medicine calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
