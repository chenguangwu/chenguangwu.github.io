#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "logistics2/inventory-aging",
  "inputs": {
    "period": "200",
    "threshold": "180"
  },
  "expect": [
    "60.0 83 ¥12,500",
    "16,000 ¥48,000"
  ],
  "ref": "原 all_default 弱用例（period=90/threshold=180 恰等于页面默认）+ expect「降价处理或退供应商」是结论句常量。样本 7 行取自页面 textarea 默认值。改为 period=200：周转天数 = 库存量 ÷（出库量 ÷ period）⇒ 矿泉水 5000÷(12000/200) = 83、纸巾 2000÷(3000/200) = 133、工艺品 400÷(5/200) = 16,000（默认 period=90 时为 37 / 60 / 7,200）。注意「呆滞品数 4」「呆滞金额占比 77.0%（142,000/184,500）」在两态同为 4 件 / 142,000 ⇒ **不具判别力、不锚**"
},
{
  "slug": "logistics2/loading-utilization",
  "inputs": {
    "boxL": "0.5",
    "boxW": "0.4",
    "boxH": "0.4",
    "boxWeight": "12",
    "planQty": "800"
  },
  "expect": [
    "340 最大可装件数",
    "170.5%"
  ],
  "ref": "原 all_default 弱用例（truck 6.8/2.3/2.4、box 0.6/0.4/0.5、weight 15、planQty 500 全等于页面默认）+ expect「建议装载」是结论句常量。改为 box 0.5×0.4×0.4 / 12kg、planQty=800：单件体积 0.08 m³，三向择优摆放 floor(6.8/0.4)×floor(2.3/0.4)×floor(2.4/0.5) = 17×5×4 = 340 件为体积上限；车厢 6.8×2.3×2.4 = 37.536 → 37.54 m³；计划 800 件 ⇒ 货物总体积 800×0.08 = 64.00 m³ ⇒ 利用率 64.00/37.536 = 170.5%（超装）、重量 800×12 = 9,600 kg ÷ 5,000 = 192.0%（超载）；重量上限 floor(5000/12) = 416 件，满载总重取较小约束 340×12 = 4,080 kg ⇒ 建议装载 340 件。默认态单件 0.12 m³、上限与利用率均跨档"
},
{
  "slug": "logistics2/packaging-cushion",
  "inputs": {
    "weight": "8",
    "dropH": "60",
    "fragility": "40"
  },
  "expect": [
    "5.6 cm 建议厚度",
    "11.3 cm 总缓冲层厚度"
  ],
  "ref": "原 all_default 弱用例（weight=3/dropH=80/fragility=60 恰等于页面默认）+ expect「跌落下不受损」是结论句常量。改为 8kg/60cm/G40（材料取默认 eps，系数 C=3.2）：厚度 t = C·h/G = 3.2×60/40 = 4.8 cm，重量修正 1+ln(8+1)×0.08 = 1.17578 ⇒ 5.6437 → 5.6 cm；总缓冲层 2t = 11.3 cm；静应力 = 8 ÷ (max(8×0.01, 0.02)×10000) = 0.0100 kg/cm²；脆值 40 < 50 ⇒ 等级「极易碎」。默认态 4.7 cm / 9.5 cm /「易碎」（脆值 60 落 50–80 档）跨档"
},
{
  "slug": "logistics2/picking-route",
  "inputs": {
    "aisles": "12",
    "aisleLen": "25",
    "aisleGap": "4",
    "speed": "1.5",
    "pickTime": "8",
    "picksPerAisle": "4"
  },
  "expect": [
    "总耗时 10 分 13 秒",
    "24.6%"
  ],
  "ref": "原 all_default 弱用例（8 通道/20m/3m/1.2m·s⁻¹/10s/3 点 恰等于页面默认）+ expect「式更优」是结论句片段。改为 12 通道 × 25m、间距 4m、1.5 m/s、单点 8s、每通道 4 点：拣货点 12×4 = 48；S 型通道内 12×25 = 300.0 m、U 型 2×300 = 600.0 m、通道间横向 (12−1)×4 = 44.0 m ⇒ 总 344.0 / 644.0 m；行走耗时 344/1.5 = 229.3s = 3分49秒、拣货 48×8 = 384s = 6分24秒 ⇒ 总 10分13秒（U 型 13分33秒）；节省 (813−613)/813 = 24.6%。默认态 总耗时 6 分 31 秒 / 节省 25.4%（跨档）"
},
{
  "slug": "logistics2/storage-allocation",
  "inputs": {
    "totalRows": "13",
    "skuInput": ""
  },
  "expect": [
    "7-13"
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
  console.log("==== logistics2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
