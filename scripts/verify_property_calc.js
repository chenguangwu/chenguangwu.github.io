#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "property/analysis-40",
  "inputs": {
    "data": "租金收益率,3.2,4.5,high\n空置率,8,5,low\n能耗成本,12,9,low\n客户满意度,78,85,high"
  },
  "expect": [
    "综合差距评分：32.6%",
    "优先改进（Top3）：空置率（60.0%）"
  ],
  "ref": "重做为标杆对比：4 项差距率，综合差距评分=各项|rel|均值×100=（0.2889+0.6+0.3333+0.0824)/4×100=32.6；按|rel|降序取Top3（空置率60.0%/能耗成本33.3%/租金收益率28.9%）。非默认输入+独立复算。"
},
{
  "slug": "property/assessor-manager-1",
  "inputs": {
    "vendorName": "",
    "contractAmt": "75",
    "contractTerm": "12"
  },
  "expect": [
    "75万"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/calc-shared-property-fee",
  "inputs": {
    "totalArea": "150",
    "sharedRatio": "20",
    "feeRate": "2.5",
    "sharedFeeRate": "0.5",
    "customPeriod": "12"
  },
  "expect": [
    "390.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/checker-11",
  "inputs": {},
  "expect": [
    "0.00/5"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "property/checker-7",
  "inputs": {},
  "expect": [
    "公共照明完好率达95%以上"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "property/checker-recorder-drill",
  "inputs": {
    "drillCount": "75",
    "evacTime": "180",
    "inspector": ""
  },
  "expect": [
    "75人"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/cost-profit",
  "inputs": {
    "v0": "500",
    "v1": "800"
  },
  "expect": [
    "300.00",
    "37.50%",
    "62.50%",
    "1.60"
  ],
  "ref": "重做后真实预算：利润=收入-成本=800-500=300.00；利润率=300/800=37.50%（默认 270/324 得 54.00/16.67%，注入失败即不命中）"
},
{
  "slug": "property/cycle-elevator",
  "inputs": {
    "logDate_'+el.id+'": "'+todayStr()+'_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/elevator-energy",
  "inputs": {
    "liftCount": "5",
    "floors": "18",
    "floorHeight": "3",
    "power": "11",
    "loadRate": "40",
    "tripsPerDay": "200",
    "tripFloors": "6",
    "idleHours": "20",
    "idlePower": "0.5",
    "price": "0.8"
  },
  "expect": [
    "20421.75"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/energy",
  "inputs": {
    "v0": "800",
    "v1": "4"
  },
  "expect": [
    "3200.00"
  ],
  "ref": "采购运费=重量×运费率=800×4=3200.00（默认 500/3 得 1500.00，注入失败即不命中）"
},
{
  "slug": "property/fee-allocation",
  "inputs": {
    "totalFee": "75000"
  },
  "expect": [
    "75000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/rater-performance",
  "inputs": {
    "v0": "128",
    "w0": "20",
    "v1": "80",
    "w1": "20",
    "v2": "90",
    "w2": "15",
    "v3": "88",
    "w3": "15",
    "v4": "92",
    "w4": "15",
    "v5": "85",
    "w5": "15"
  },
  "expect": [
    "89.3"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/report-manager",
  "inputs": { "data": "物业费,320000,180000\n停车费,85000,22000\n广告位,40000,5000\n公共能耗,0,96000" },
  "expect": [
    "收入合计： 445000.00",
    "支出合计： 303000.00",
    "收支结余： +142000.00"
  ],
  "ref": "收入=320000+85000+40000+0=445000；支出=180000+22000+5000+96000=303000；结余=+142000；结余率=31.91%（默认 260000+60000=320000 / 150000+18000+45000=213000 / +107000，避开）"
},
{
  "slug": "property/response-1",
  "inputs": {
    "v0": "600",
    "v1": "700"
  },
  "expect": [
    "100 分钟",
    "1.67 h"
  ],
  "ref": "维修响应时长=响应-报修=700-600=100 分钟（默认 570/595 得 25 分钟，注入失败即不命中；含 B>=A 校验）"
},
{
  "slug": "property/response-4",
  "inputs": {
    "v0": "600",
    "v1": "1200"
  },
  "expect": [
    "600 分钟",
    "10.00 h"
  ],
  "ref": "维修完成时长=完成-报修=1200-600=600 分钟（默认 570/1110 得 540 分钟，注入失败即不命中）"
},
{
  "slug": "property/shared-area",
  "inputs": {
    "innerArea": "4800",
    "unitCount": "40"
  },
  "expect": [
    "4800.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "property/stats-manager",
  "inputs": {
    "tot": "300",
    "rent_cnt": "150",
    "visits": "450",
    "dur": "3",
    "price": "6",
    "rent_fee": "400"
  },
  "expect": [
    "3.00",
    "68.75",
    "303,000.00"
  ],
  "ref": "车场：总车位300/包月150 → 临停位150，周转率=450/150=3.00；在场=450×3/24=56.25，占用率=(150+56.25)/300=68.75%；月临停=450×3×6×30=243000，月租=150×400=60000，合计 303000.00（独立复算，非页面默认值）"
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
  console.log("==== property calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
