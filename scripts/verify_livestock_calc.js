#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "livestock/ammonia-ventilation",
  "inputs": {
    "nh3Current": "38",
    "nh3Target": "15",
    "houseLength": "30",
    "houseWidth": "10",
    "houseHeight": "3",
    "nh3Gen": "0"
  },
  "expect": [
    "1195"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/analysis-18",
  "inputs": {
    "hens": "8000",
    "days": "5",
    "eggs": "35200",
    "eggw": "60",
    "feed": "4700"
  },
  "expect": [
    "88.00",
    "2.23",
    "40,000"
  ],
  "ref": "蛋鸡产蛋：饲养日=8000×5=40000，产蛋率=35200/40000=88.00%；总蛋重=35200×60/1000=2112kg，料蛋比=4700/2112=2.23（独立复算，非页面默认值）",
},
{
  "slug": "livestock/animal-welfare-score",
  "inputs": {
    "s1": "12",
    "s2": "8",
    "s3": "7",
    "s4": "7",
    "s5": "6",
    "s6": "8",
    "s7": "8",
    "s8": "6",
    "s9": "7"
  },
  "expect": [
    "100.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/calc-58",
  "inputs": {
    "ped": "P,\nQ,\nR,P,Q\nS,P,Q\nT,R,S"
  },
  "clicks": ["calc()"],
  "expect": [
    "0.25000",
    "25.000%",
    "5 个体总数"
  ],
  "ref": "通径法：T 的父母 R、S 为全同胞，共同祖先 P、Q（均为始祖、F=0）。"
     + "F_T=Σ(1/2)^(n1+n2+1)×(1+F_A)：R-P-S 路径 (1/2)^3=0.125，R-Q-S 路径 0.125 ⇒ F_T=0.25 ⇒ 25.000%。"
     + "个体总数=5。原系谱（X,B,C）所有个体 F=0.00000，原 expect「0.00000」即默认态常量 ⇒ 零判别力。",
  },
{
  "slug": "livestock/calving-interval",
  "inputs": {
    "daysToFirstBreed": "113",
    "breedTimes": "2",
    "gestation": "283"
  },
  "expect": [
    "113"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/castration-timing",
  "inputs": {
    "animalType": "cattle"
  },
  "expect": [
    "cattle"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/detector-12",
  "inputs": {
    "afb1": "15",
    "zea": "100",
    "don": "1000",
    "ota": "50"
  },
  "expect": [
    "75%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/disinfectant-dilution",
  "inputs": {
    "stockConc": "8",
    "targetConc": "0.1",
    "totalVol": "10"
  },
  "expect": [
    "9875ml"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/dongtishouroulv-beibiaohouceding",
  "inputs": {
    "bf": "27",
    "lw": "100"
  },
  "expect": [
    "45.65%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/estimate-yield",
  "inputs": {
    "qty": "1500",
    "ts": "20",
    "hrt": "20"
  },
  "expect": [
    "126.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/fattening-pig-timeline",
  "inputs": {
    "currentWeight": "90",
    "targetWeight": "120",
    "adg": "800",
    "fcr": "2.8",
    "feedPrice": "3.5"
  },
  "expect": [
    "预计饲养天数 38"
  ],
  "ref": "auto-restore；页面「预计出栏日期」用 new Date() 相对今天推算，绝对日期随真实日期漂移（写用例时的「今天」已过期 1 天），故改断言由输入确定、与今天无关的「预计饲养天数 38」（(120-90)/0.8=37.5→ceil 38），规避日期型门禁偶挂"
},
{
  "slug": "livestock/feed-conversion-ratio",
  "inputs": {
    "startWeight": "45",
    "endWeight": "100",
    "totalFeed": "180",
    "days": "90",
    "feedKg": "180",
    "feedPrice": "3.5",
    "gainKg": "70",
    "salePrice": "18"
  },
  "expect": [
    "3.273"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/heat-stress-index",
  "inputs": {
    "temp": "45",
    "humidity": "70",
    "windSpeed": "0.5"
  },
  "expect": [
    "103.92"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/inbreeding-coefficient",
  "inputs": {
    "ne": "75",
    "generations": "5",
    "fa": "0",
    "n1": "2",
    "n2": "2",
    "numAncestors": "1"
  },
  "expect": [
    "1/(2×75)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/manure-amount",
  "inputs": {
    "count": "150",
    "days": "365",
    "moisture": "85",
    "customManure": "0",
    "collectRate": "90"
  },
  "expect": [
    "150头奶牛在365天内产生约"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/manure-pit-capacity",
  "inputs": {
    "count": "300",
    "dailyManure": "45",
    "moisture": "88",
    "cleanCycle": "7",
    "pitDepth": "2.5",
    "storageDays": "90"
  },
  "expect": [
    "13500.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/milk-yield-scc",
  "clicks": ["records=[{day:1,yield:28.5,scc:12},{day:2,yield:30.2,scc:15},{day:3,yield:31.8,scc:18},{day:4,yield:33.1,scc:22}];analyze()"],
  "expect": [
    "30.9 平均产奶量",
    "上升趋势（斜率 1.54 kg/天）",
    "33.1 最高产奶量"
  ],
  "ref": "顶层数组 records 注入 4 条（页面要求 ≥2 条才分析）：均值 (28.5+30.2+31.8+33.1)/4 = 30.9；线性回归 Sxy = 7.7、Sxx = 5 ⇒ 斜率 1.54 kg/天；最大产奶量 33.1。默认态为源码内置记录（26.93），三串均不命中。"
},
{
  "slug": "livestock/mycotoxin-limit",
  "inputs": {
    "measuredValue": "23"
  },
  "expect": [
    "230.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/poultry-light-program",
  "inputs": {
    "currentAge": "4"
  },
  "expect": [
    "22小时"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/silage-density-ph",
  "inputs": {
    "siloLength": "15",
    "siloWidth": "4",
    "siloHeight": "2.5",
    "siloWeight": "80",
    "dmContent": "33",
    "phValue": "4.0",
    "phDM": "33",
    "smellScore": "4"
  },
  "expect": [
    "150.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/stats-7",
  "inputs": {
    "tot": "300",
    "mild": "21",
    "hard": "9"
  },
  "expect": [
    "3.00",
    "10.00",
    "270"
  ],
  "ref": "产犊难产：总数 300、轻度助产 21、难产 9 → 顺产 270 头；难产率=9/300=3.00%，需助产率=30/300=10.00%（独立复算，非页面默认值）",
},
{
  "slug": "livestock/vaccine-schedule",
  "inputs": {
    "animalType": "layer"
  },
  "expect": [
    "禽流感H5+H7灭活苗"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/water-feed-ratio",
  "inputs": {
    "waterIntake": "12",
    "feedIntake": "2.5",
    "temp": "22"
  },
  "expect": [
    "12.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/weaning-weight-survival",
  "inputs": {
    "bornAlive": "18",
    "weanedAlive": "11",
    "weanDay": "28",
    "avgWeight": "7.5",
    "standardWeight": "6.0",
    "belowStandard": "2"
  },
  "expect": [
    "61.1%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "livestock/withdrawal-period",
  "inputs": {
    "withdrawalDays": "14",
    "drugSelect": "oxytetracycline"
  },
  "expect": [
    "休药期 28 天"
  ],
  "ref": "auto-restore；页面「休药期结束日期」用 new Date() 相对今天推算，绝对日期随真实日期漂移（写用例时的「今天」已过期 1 天），故改断言由药品表确定、与今天无关的「休药期 28 天」（土霉素 oxytetracycline 对应休药期），规避日期型门禁偶挂"
},
{
  "slug": "livestock/yufeirizengzhong-liaoroubiquxian",
  "inputs": {
    "w0": "450",
    "w1": "480",
    "days": "120",
    "feed": "1100",
    "price": "3.2"
  },
  "expect": [
    "117.33"
  ],
  "ref": "auto-restore"
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
  console.log("==== livestock calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
