#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "misc2/car-residual",
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
  "slug": "misc2/cigarette-tar",
  "inputs": {
    "tar": "5",
    "nic": "0.4",
    "cigs": "10"
  },
  "expect": [
    "每日焦油摄入： 50.0 mg",
    "估算吸入焦油（按25%吸收率）： 12.5 mg/日"
  ],
  "ref": "原 all_default 弱用例（tar=10/nic=0.8/cigs=20 恰等于页面默认）+ expect「中焦油」是 renderTable() 渲染的**静态分级表**档位词（≤5 极低 / 5-8 低 / 8-12 中 / >12 高 四档在默认态同样出现 ⇒ 零判别力）。改为 tar=5/nic=0.4/cigs=10：每日焦油 5×10 = 50.0 mg、每日尼古丁 0.4×10 = 4.00 mg、每月 50×30 = 1,500.0 mg（1.50 g）、每年 50×365 = 18,250.0 mg（18.25 g）、吸入按 25% 吸收率 50×0.25 = 12.5 mg/日。默认态 200.0 / 6,000.0 / 73,000.0 mg（跨档）"
},
{
  "slug": "misc2/screen-size",
  "inputs": {
    "width": "720",
    "height": "1280",
    "diagonal": "6.5"
  },
  "expect": [
    "PPI 像素密度： 225.94",
    "0.92 MP"
  ],
  "ref": "原 all_default 弱用例（1080/2400/6.7 恰等于页面默认）+ expect「细腻」是精细度档位词。改为 720×1280 @6.5\"：PPI = √(720²+1280²)/6.5 = 1468.60/6.5 = 225.94、像素数 720×1280 = 0.9216 MP → 0.92 MP、长宽比 9:16、物理宽 720/225.94 = 3.187\"、物理高 1280/225.94 = 5.665\"、点距 25.4/225.94 = 0.1124 mm；精细度跨档为「清晰」（默认 PPI √(1080²+2400²)/6.7 = 392.81 ⇒「细腻」）"
},
{
  "slug": "misc2/tax-refund",
  "inputs": {
    "amount": "80000",
    "rate": "0.06"
  },
  "expect": [
    "实退金额： 7,600.00 JPY",
    "折合人民币： ¥456.00"
  ],
  "ref": "原 all_default 弱用例（amount=50000/rate=0.048 恰等于页面默认）+ expect「日元可退税」是结果末尾的**静态说明文案**（国家表说明列）。改 amount=80000（rate=0.06 是 JPY→CNY **汇率**，不是退税率）：退税率取目的地表（日本 10%）⇒ 可退 80000×10% = 8,000.00 JPY、手续费 5% = 400.00 JPY、实退 7,600.00 JPY、折合人民币 7600×0.06 = ¥456.00（购物额折合 80000×0.06 = ¥4,800.00）。默认态 5,000 / 250 / 4,750 JPY、¥228.00"
},
{
  "slug": "misc2/coin-grade",
  "inputs": {
    "grade": "au"
  },
  "expect": [
    "仅在币面最高点"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc2/instrument-tuning",
  "inputs": {
    "baseFreq": "660"
  },
  "expect": [
    "1047.685"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc2/insurance-fee",
  "inputs": {
    "value": "7500"
  },
  "expect": [
    "500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc2/luggage-size",
  "inputs": {
    "size": "20"
  },
  "expect": [
    "国际标准随身尺寸约55×40×20cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "misc2/shoe-size",
  "inputs": {
    "footLen": "383"
  },
  "expect": [
    "请输入200-320mm之间的脚长"
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
  console.log("==== misc2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
