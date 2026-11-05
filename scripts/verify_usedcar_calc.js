#!/usr/bin node
"use strict";
// usedcar 覆盖说明（2026-09-27）：本分类 12 页（index 除外）已全部定论 ——
// 已有用例 9 例覆盖 car-purchase-cost / detector-19 / recorder-maintenance / tester-12 /
// usedcar-valuation / wear / calc-73 / estimate-38 / ershouchetanpanyijiakongjianyuce。
// checker-3 / rater-37（2026-11-05 改造）：计分项 select（ck_<key>）由 buildList() 运行期
//   innerHTML 拼出，页面 init 末尾直接调 calc()；桩内这些 id 若取空串 ⇒ statusOpts.find() 返回
//   undefined ⇒ 初始化即抛 Cannot read properties of undefined (reading score)。
//   解法：inputs 同时注入全部 ck_*（让 boot 的 calc() 拿到合法档位、不抛错），再用 clicks 把
//   其中若干项改档后重算 —— expect 只认「click 后的分数」；判别器 clearInject 清空 clicks 后
//   回退兜底只能复现注入态的全优分（100），与 expect 不重合 ⇒ 既不 skip 也无逃生项。
//   （ck_* 是运行期 id、pageDefaults 取不到，故 inputs 侧这些键会被判别器保留注入值。）
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
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
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
  "expect": [ "22,500 超额里程费" ],
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
},
{
  "slug": "usedcar/car-residual",
  "inputs": {
    "price": "200000",
    "years": "5"
  },
  "expect": [
    "51.00%",
    "¥98,000.00"
  ],
  "ref": "原 all_default 弱用例（price=150000/years=3 恰等于页面默认）+ expect「估算残值」是结果卡片的静态标签。默认方法 method=rule（54321 阶梯），速率表 RULE_RATES=[0.15,0.12,0.10,0.08,0.06] ⇒ years=5 时累计折旧率 = 0.15+0.12+0.10+0.08+0.06 = 0.51。改为 price=200000/years=5：累计折旧 200000×0.51 = 102,000 → 折旧率 51.00%、残值 max(200000−102000, 200000×5%) = ¥98,000.00。默认态 3 年 ⇒ 0.37 → 37.00% / ¥94,500.00（跨档）。注：life/salvage 仅在 straight/double 方法下参与计算，rule 模式下零影响，故不再注入以免造成「看似非默认」的假象"
},
{
  "slug": "usedcar/car-residual",
  "inputs": {
    "method": "straight",
    "price": "120000",
    "years": "4",
    "life": "-10",
    "salvage": "5"
  },
  "expect": [
    "折旧年限需在 1–30 年之间"
  ],
  "ref": "负折旧年限回归：直线法 life=-10 时旧版 annualDep=(120000−6000)/−10=−11400、dep=−45600 ⇒ 残值 ¥165,600.00（高于新车价）、折旧率 −38.00%。修复后 calc 在方法分支前置校验 life∈[1,30]，直接输出「折旧年限需在 1–30 年之间」且不出残值。输入 price/year/life 均非页面默认（150000/3/10），默认态无该提示 ⇒ 判别有效；同时 years 校验 0–30、rate 统一由 (1−residual/price)×100 计算，保证年限越残值越低且折旧率与残值一致"
},
{
  "slug": "usedcar/car-purchase-cost",
  "inputs": {
    "price": "",
    "taxRate": "",
    "insurance": "",
    "plate": ""
  },
  "expect": [
    "请填写 车价、购置税率、保险费、上牌费 后再计算"
  ],
  "ref": "空态守卫：四项留空 ⇒ 提示，不再按 0 兜底把落地价算成 0.00。默认态各字段有初值并输出总价，不含该提示 ⇒ 可判别。"
  },
  {
    "slug": "usedcar/checker-3",
    "inputs": {
      "ck_frame": "4",
      "ck_floorpan": "4",
      "ck_subframe": "4",
      "ck_shock": "4",
      "ck_control": "4",
      "ck_spring": "4",
      "ck_exhaust": "4",
      "ck_fuel": "4",
      "ck_brakeline": "4",
      "ck_wheelwell": "4",
      "ck_bushing": "4"
    },
    "clicks": [
      "document.getElementById('ck_frame').value='1';calc()"
    ],
    "expect": ["86", "严重问题(1项)"],
    "ref": "11 项权重合计 19（frame3/floorpan2/subframe2/shock2/control2/spring1/exhaust1/fuel2/brakeline2/wheelwell1/bushing1）。"
       + "注入全部「好(4)」⇒ boot calc 得 19×100/19 = 100 分、优秀。clicks 把大梁/车架改为「严重(1)」"
       + "（score10×weight3）后重算：totalScore=1900−300+30=1630 ⇒ 1630/19=85.79 ⇒ 86 分、仍「优秀」；"
       + "问题项 1 个且为 v=1 ⇒ 报告出现「严重问题(1项)」。默认态（无 clicks）仍是 100 分、0 问题项，两锚均不命中。"
  },
  {
    "slug": "usedcar/rater-37",
    "inputs": {
      "ck_start": "5",
      "ck_idle": "5",
      "ck_accel": "5",
      "ck_vibration": "5",
      "ck_oilleak": "5",
      "ck_coolantleak": "5",
      "ck_transleak": "5",
      "ck_sound": "5",
      "ck_smoke": "5",
      "ck_temp": "5",
      "ck_cel": "5"
    },
    "clicks": [
      "(function(){['start','oilleak','sound','cel'].forEach(function(k){document.getElementById('ck_'+k).value='1';});calc();})()"
    ],
    "expect": ["57", "发现 4 项问题"],
    "ref": "11 项权重合计 27（start3/idle3/accel2/vibration2/oilleak3/coolantleak2/transleak2/sound3/smoke2/temp2/cel3）。"
       + "注入全部「优秀(5)」⇒ boot calc = 27×100/27 = 100 分、优秀。clicks 把启动性能/机油渗漏/异响/故障灯改为"
       + "「严重(1)」（score10×weight3）后重算：totalScore=2700−4×300+4×30=1540 ⇒ 1540/27=57.04 ⇒ 57 分「一般」；"
       + "问题项 4 个 ⇒ 报告出现「发现 4 项问题」。默认态（无 clicks）仍为 100 分、0 问题项，两锚均不命中。"
  },
  {
    "slug": "usedcar/detector-19",
    "clicks": ["document.getElementById('ck_smell').value='0';calc()"],
    "expect": ["待检测：还有 13 项未检查"],
    "ref": "新契约（2026-11-05）：14 项检测默认「未检查（请选择）」（value=''），未检查项不计入正常、不输出风险指数/结论/购买建议。仅把 ck_smell 设为正常(0) 后 calc ⇒ 结果区显示「待检测：还有 13 项未检查」。默认态 14 项全未检查；全部设为正常(0) 才输出「未发现泡水痕迹 · 0%」；ck_smell=2 ⇒「疑似泡水车 · 8%」。判别器清空 clicks 后 calc 回落到全未检查（14 项），expect 失配。"
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

  console.log("==== usedcar calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
