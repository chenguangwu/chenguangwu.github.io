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
},
{
  "slug": "logistics2/storage-allocation",
  "inputs": {
    "skuInput": "苹果,100\n香蕉,100\n橙子,100\n梨,100\n桃,100\n葡萄,100",
    "totalRows": "9"
  },
  "expect": [
    "66.6%",
    "合计校验：✓ 商品数 6 行 = 明细 6 行；频次 600 = 明细合计 600；排数 5+2+2 = 9；占比合计 100.0%"
  ],
  "clicks": [
    "document.getElementById('skuInput').value=['苹果,100','香蕉,100','橙子,100','梨,100','桃,100','葡萄,100'].join(String.fromCharCode(10));document.getElementById('totalRows').value='9';calc();"
  ],
  "ref": "W5-A 汇总/明细闭合：6 个等频次 SKU（默认样例 14 个不复现）⇒ A=4/B=1/C=1，占比原始值 66.7+16.7+16.7=100.1 超 0.1；修复后尾差从频次最大类 A 扣回得 66.6%，合计校验行 5+2+2=9 排、占比 100.0%。旧实现占比合计 100.1% 且无「合计校验」行，两条期望均不命中。"
},
{
  "slug": "logistics2/storage-allocation",
  "inputs": {
    "skuInput": "苹果,100\n香蕉,100\n橙子,100\n梨,100\n桃,100\n葡萄,100",
    "totalRows": "9",
    "doorPos": "back"
  },
  "expect": [
    "合计校验：✓ 商品数 6 行 = 明细 6 行；频次 600 = 明细合计 600；排数 5+2+2 = 9；占比合计 100.0%",
    "66.6%"
  ],
  "clicks": [
    "document.getElementById('skuInput').value=['苹果,100','香蕉,100','橙子,100','梨,100','桃,100','葡萄,100'].join(String.fromCharCode(10));document.getElementById('totalRows').value='9';document.getElementById('doorPos').value='back';calc();"
  ],
  "ref": "W5-A 门在后端时，汇总排号须由明细派生（旧实现汇总硬编码从第 1 排起、明细却是「第 5-9 排」）；合计校验与尾差校正同样命中。"
},
{
  "slug": "logistics2/loading-utilization",
  "inputs": {
    "truckL": "6.8",
    "truckW": "2.3",
    "truckH": "2.4",
    "truckLoad": "5000",
    "boxL": "10",
    "boxW": "3",
    "boxH": "3",
    "boxWeight": "15",
    "planQty": "5"
  },
  "expect": ["单件尺寸大于车厢"],
  "ref": "06-F5（高优）：单件 10×3×3 m 大于车厢 6.8×2.3×2.4 m，六向 fit 全为 0 ⇒ 修复后 bestFit=0 走提示分支输出「单件尺寸大于车厢，无法装载」；旧实现 bestOrient 为 null，渲染读 bestOrient.nx 抛 TypeError、结果区空白。默认 0.6×0.4×0.5 不含该串。"
},
{
  "slug": "logistics2/loading-utilization",
  "inputs": {
    "truckL": "5",
    "truckW": "3",
    "truckH": "2",
    "truckLoad": "5000",
    "boxL": "1.5",
    "boxW": "1.2",
    "boxH": "2",
    "boxWeight": "10",
    "planQty": "10"
  },
  "expect": ["8 最大可装件数"],
  "ref": "06-F6（中优）：车厢 5×3×2、货物 1.5×1.2×2。旧 3 向枚举最大 6 件（[1.5,1.2,2]→3×2×1）；补全 6 向全排列后 [1.2,1.5,2]→floor(5/1.2)×floor(3/1.5)×floor(2/2)=4×2×1=8 件；重量上限 floor(5000/10)=500 ⇒ 最大可装 8、体积受限。"
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

  console.log("==== logistics2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
