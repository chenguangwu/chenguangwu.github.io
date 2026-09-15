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
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
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
    "ped": "S,\nA,\nD,\nB,S,A\nC,S,D\nX,B,C"
  },
  "expect": [
    "0.00000"
  ],
  "ref": "auto-restore(default)"
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
    "2026年10月22日"
  ],
  "ref": "auto-restore"
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
  "inputs": {},
  "expect": [
    "26.93"
  ],
  "ref": "auto-restore(default)"
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
    "data": "10,20,30,40,50,60,70,80_X"
  },
  "expect": [
    "80_X"
  ],
  "ref": "auto-restore"
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
    "2026年10月13日"
  ],
  "ref": "auto-restore"
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
