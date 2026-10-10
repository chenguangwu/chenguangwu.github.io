#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  // 注：collectStrings 在剥离 <strong> 标签时会插入空格，故期望值含「： 」后的空格
  { slug: "martial/breathing-rhythm", inputs: {"breathRate":"30"}, expect: ["呼吸周期： 2.00 秒"] },
  { slug: "martial/kick-height", inputs: {"kickHeight":"200"}, expect: ["高度比（身高）： 117.6%"] },
  // routine-timer：standardTime 由 loadStandard() 按套路类型重算为区间中值（taijiquan → 360），
  // 完成耗时由 manualTime 注入（原仅计时器可写，页面加载即 myTime=0 → 速度比率 Infinity%，
  // 2026-09-23 已补 manualTime 输入 + myTime<=0 守卫）。
  // 例1 taijiquan 中值 360、耗时 330 → 速度比率 360/330×100 = 109.1%（在 300~420 允许范围内）
  { slug: "martial/routine-timer", inputs: { "routineType": "taijiquan", "manualTime": "330" }, expect: ["标准： 360 秒", "速度比率： 109.1%"] },
  // 例2 changquan 中值 80、耗时 95 → 速度比率 80/95×100 = 84.2%、偏差 +15.0、
  //     超上限扣分 (95−90)×0.5 = 2.5
  { slug: "martial/routine-timer", inputs: { "routineType": "changquan", "manualTime": "95" }, expect: ["速度比率： 84.2%", "+15.0"] },
  { slug: "martial/stance-center", inputs: {"frontRatio":"80"}, expect: ["前脚 80%"] },
  { slug: "martial/strike-resistance", inputs: {"trainYears":"3","freq":"7"}, expect: ["硬度指数： 119"] },
  {
    "slug": "martial/breathing-rhythm",
    "inputs": {
      "breathRate": "42",
      "actionType": "throw",
      "inhaleRatio": "0.5",
      "level": "1"
    },
    "expect": [
      "分） 呼吸周期： 1.43 秒 （吸0.48s : 呼0.95s） 匹配指数： 34 需调整 ⚠️ 呼吸偏快 ：当前频率高于推荐范围，可能影响发力节奏。建议放慢呼吸，加深吸气"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"breathRate\":\"42\",\"actionType\":\"throw\",\"inhaleRatio\":\"0.5\",\"level\":\"1\"}，输出区含「分） 呼吸周期： 1.43 秒 （吸0.48s : 呼0.95s） 匹配指数： …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "martial/kick-height",
    "inputs": {
      "height": "42",
      "legLen": "42",
      "kickHeight": "42",
      "kickType": "side",
      "level": "1"
    },
    "expect": [
      " 估算踢腿角度： 41.8° 踢腿过头顶，柔韧与技术俱佳。 ✓ 出色 ：踢腿高度已达头顶以上，柔韧性优秀"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"height\":\"42\",\"legLen\":\"42\",\"kickHeight\":\"42\",\"kickType\":\"side\",\"level\":\"1\"}，输出区含「 估算踢腿角度： 41.8° 踢腿过头顶，柔韧与技术俱佳。 ✓ 出色 ：踢腿高度…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "martial/routine-timer",
    "inputs": {
      "standardTime": "42",
      "tolerance": "42",
      "manualTime": "42",
      "routineType": "nanquan"
    },
    "expect": [
      "0 超出范围扣分\nnanquan\n75"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"standardTime\":\"42\",\"tolerance\":\"42\",\"manualTime\":\"42\",\"routineType\":\"nanquan\"}，输出区含「0 超出范围扣分\nnanquan\n75」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "martial/stance-center",
    "inputs": {
      "stepWidth": "42",
      "height": "42",
      "frontRatio": "42",
      "squatDepth": "42",
      "duration": "42",
      "stanceType": "bow"
    },
    "expect": [
      "） 稳定性指数： 66 耐力评分： 14 需加强 ⚠️ 重心偏差较大 ：承重比与标准弓步相差23%，建议调整姿势以提升稳定性。 ⚠️ 强度较高 ：当前姿势强度大且时长较长，注意适度休息，避免关节损伤"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"stepWidth\":\"42\",\"height\":\"42\",\"frontRatio\":\"42\",\"squatDepth\":\"42\",\"duration\":\"42\",\"stanceType\":\"bow\"}，输出区含「） 稳定性指数： 66 耐力评分： 14 需加强 ⚠️ 重心偏差较大 ：承重比与…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "martial/strike-resistance",
    "inputs": {
      "freq": "42",
      "trainYears": "1"
    },
    "expect": [
      " -- 硬度指数\n1\n42\n90\n\n86\n\n81\n\n76\n\n83\n\n91\n\n85\n\n38"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"freq\":\"42\",\"trainYears\":\"1\"}，输出区含「 -- 硬度指数\n1\n42\n90\n\n86\n\n81\n\n76\n\n83\n\n91\n\n85…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== martial calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();