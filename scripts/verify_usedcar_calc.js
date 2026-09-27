#!/usr/bin node
"use strict";
// usedcar 覆盖说明（2026-09-27）：本分类 12 页（index 除外）已全部定论 ——
// 已有用例 9 例覆盖 car-purchase-cost / detector-19 / recorder-maintenance / tester-12 /
// usedcar-valuation / wear / calc-73 / estimate-38 / ershouchetanpanyijiakongjianyuce。
// 结构性不可注入、暂不立例（判据见 §10.5 B 组，理由随后续批次复核）：
//   checker-3 / rater-37 —— 计分项 select（ck_<key>）由 buildList() 运行期 innerHTML 拼出，
//   且页面 init 末尾直接调 calc()；桩内这些 id 取到空串 ⇒ statusOpts.find() 返回 undefined ⇒
//   初始化即抛 Cannot read properties of undefined (reading score) ⇒ 整页无产物。
//   真机里 option 自带 selected、不会取空，故属桩盲区而非页面缺陷；又因 ids 动态、
//   判别器 clearInject 无法把它们换回默认 ⇒ 即使改 clicks 也不能构造「注入 PASS / 默认 FAIL」。
//   detector-19 同型但 init 用 v===1/v===2 比较、不读 .score，故可用 clicks 改造成功（见下）。
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "usedcar/car-purchase-cost",
  "inputs": {
    "price": "225000",
    "taxRate": "10",
    "insurance": "8000",
    "plate": "800"
  },
  "expect": [
    "256300.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/detector-19",
  "clicks": [
    "(function(){var C={smell:2,carpet:2,seatbelt:1,seatrail:1,ceiling:1,dashboard:0,electrics:1,harness:0,engbay:0,silt:2,fluid:2,sparetire:0,headlight:0,waterline:2};for(var k in C){var e=document.getElementById('ck_'+k);if(e){e.value=C[k];}}calc();})();"
  ],
  "expect": [
    "54%",
    "73%"
  ],
  "ref": "旧用例的输入键是字面量模板 ck_'+it.key+'、expect 只是回显注入串（逃生项口径）。改为 clicks 写全 14 项：确认（v=2）smell/carpet/silt/fluid/waterline、可疑（v=1）seatbelt/seatrail/ceiling/electrics、其余 v=0。totalScore=2*(3+3+3+3+3)+1*(3+2+2+2)=39、totalWeight=36*2=72 ⇒ 风险指数 54%；分组 内饰 19/26=73%、电子 2/16=13%、发动机舱 12/20=60%、外观 6/10=60%。清空 clicks 后各 ck_ 取空值 v=0 ⇒ 风险指数 0%，与本值不重合"
},
{
  "slug": "usedcar/recorder-maintenance",
  "inputs": {
    "vName": "我的车辆",
    "curKm": "120000",
    "carValue": "80000"
  },
  "expect": [
    "120000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/tester-12",
  "inputs": {
    "batteryV": "18.4",
    "chargingV": "14.2"
  },
  "expect": [
    "18.4V"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/usedcar-valuation",
  "inputs": {
    "newPrice": "180000",
    "age": "3",
    "mileage": "3"
  },
  "expect": [
    "153000.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/wear",
  "inputs": {
    "odo": "90000",
    "age": "3",
    "bench": "15000",
    "unit": "0.5",
    "value": "100000",
    "tol": "20"
  },
  "expect": [
    "90000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "usedcar/calc-73",
  "inputs": {
    "price": "28",
    "age": "5",
    "mileage": "12",
    "brand": "domestic",
    "condition": "fair"
  },
  "expect": [
    "11.63",
    "16.37",
    "58.3%"
  ],
  "ref": "retained=0.85*0.91^(age-1)=0.5829；里程 factor：expected=1.5*5=7.5、ratio=12/7.5=1.6 ⇒ 1-min(0.30,0.6*0.20)=0.88；value=28*0.5829*BRAND.domestic(0.90)*COND.fair(0.90)*0.88=11.63 ⇒ 保值率 41.5%、累计贬值 16.37、基础系数 58.3%。默认态 price=20/age=3/km=5 ⇒ 15.32/76.6/4.68，与本值不重合"
},
{
  "slug": "usedcar/estimate-38",
  "inputs": {
    "price": "12",
    "year": "2020",
    "displacement": "2.0",
    "cityType": "tier2",
    "agencyFee": "300",
    "newPlate": "yes"
  },
  "expect": [
    "2,570",
    "13,189"
  ],
  "ref": "排量 2.0L ⇒ VVT=420、过户 tier2=600、上牌 tier2=300、车船税 420、交强险 950、代办 300；不含税支出=600+420+300+950+300=2,570；含税合计=120,000/1.13*0.10+2,570=10,619+2,570=13,189。默认态 price=8/1.6L/tier1 ⇒ 总费用 2,470 量级，与本值不重合"
},
{
  "slug": "usedcar/ershouchetanpanyijiakongjianyuce",
  "inputs": {
    "askPrice": "10",
    "age": "4",
    "mileage": "6",
    "bench": "1.5",
    "condition": "poor",
    "heat": "cold",
    "style": "aggressive"
  },
  "expect": [
    "27.0%",
    "7.30–8.65",
    "7.98"
  ],
  "ref": "base=COND.poor(0.18)+HEAT.cold(0.05)+min(0.08,4*0.01=0.04)=0.27 ⇒ 议价空间 27.0%；合理区间=10*(1-0.27)=7.30 ~ 10*(1-0.15)=8.65；首次出价 7.00；目标价=7.30+(8.65-7.30)*0.5=7.9750 ⇒ 7.98。默认 condition=good/heat=normal/style=normal ⇒ 空间 10.0% 量级，与本值不重合"
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
  console.log("==== usedcar calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
