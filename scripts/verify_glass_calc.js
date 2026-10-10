#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "glass/annealing-curve", inputs: {"thick":"12","glass":"boro","coolTo":"100"}, expect: ["总退火时间 ≈ 84 时 17 分","565 保温温度(°C)","1.5 慢冷速率(°C/h)"], ref: "12mm 硼硅、冷至100℃：保温565℃×48min、慢冷1.5℃/h、总退火84时17分（默认6mm soda→50℃走另一组值）" },
  { slug: "glass/cutting-score", inputs: {"sheetW":"2200","sheetH":"1600","thick":"12","pieceW":"500","pieceH":"400","kerf":"4"}, expect: ["15 小片数量","5×3 排版旋转90°","85.2% 材料利用率"], ref: "2200×1600 原片切 500×400（kerf 4）：旋转90°排 5×3=15 片、利用率 85.2%、切割6次（默认 1830×1220 切 400×300）" },
  { slug: "glass/snell-refraction", inputs: {"n1":"1.52","n2":"1.0003","angle":"45"}, expect: ["入射角 45.0°","41.15°"], ref: "玻璃1.52→空气1.0003、45°：sinθ₂=1.0003×sin45/1.0003>1 触发全反射，临界角 arcsin(1.0003/1.52)=41.15°（默认空气→水、30° 为折射分支）" },
  { slug: "glass/thermal-bend", inputs: {"thick":"8","angle":"150","radius":"30","glass":"boro"}, expect: ["热弯温度 ≈ 795°C","78.5 弯曲弧长(mm)","88 保温时间(min)"], ref: "8mm 硼硅热弯 150°/R30：弧长 78.5mm、R/t=3.75、难度3 → 795°C、保温 88min（默认 5mm/90°/R60）" },
  { slug: "glass/thickness-selection", inputs: {"width":"1500","height":"1800","scene":"tabletop"}, expect: ["推荐最小厚度 10 mm（钢化）","2.70 面积(m²)","1.80 最大跨度(m)"], ref: "1500×1800 桌面/台面：面积 2.70m²、跨度 1.80m → 推荐 10mm 钢化（默认 800×1200 为窗户/采光分支）" },
  {
    "slug": "glass/cutting-score",
    "inputs": {
      "sheetW": "42",
      "sheetH": "42",
      "thick": "42",
      "pieceW": "42",
      "pieceH": "42",
      "kerf": "42"
    },
    "expect": [
      "Ny−2) = (1+1−2) = 0 次 结论 42×42×42mm 原片，按正向排版可切 1 片 42×42mm，利用率 100.0%，需切割 0 次。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sheetW\":\"42\",\"sheetH\":\"42\",\"thick\":\"42\",\"pieceW\":\"42\",\"pieceH\":\"42\",\"kerf\":\"42\"}，输出区含「Ny−2) = (1+1−2) = 0 次 结论 42×42×42mm 原片，按…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "glass/annealing-curve",
    "inputs": {
      "thick": "42",
      "coolTo": "42",
      "glass": "boro"
    },
    "expect": [
      "\udf21️ 临界慢冷 560°C → 510°C 0.002°C/min（0.1°C/h） 420 时 00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"thick\":\"42\",\"coolTo\":\"42\",\"glass\":\"boro\"}，输出区含「\udf21️ 临界慢冷 560°C → 510°C 0.002°C/min（0.1°C/…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "glass/thermal-bend",
    "inputs": {
      "thick": "42",
      "angle": "42",
      "radius": "42",
      "glass": "boro"
    },
    "expect": [
      "时间(min) 1.0 R/t 比 提示：弯曲半径 42mm 小于推荐最小值 105.0mm（2.5t），应力集中风险高，需专业模具与缓冷。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"thick\":\"42\",\"angle\":\"42\",\"radius\":\"42\",\"glass\":\"boro\"}，输出区含「时间(min) 1.0 R/t 比 提示：弯曲半径 42mm 小于推荐最小值 1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "glass/snell-refraction",
    "inputs": {
      "n1": "42",
      "n2": "42",
      "angle": "42",
      "m1": "1.33",
      "m2": "1.33"
    },
    "expect": [
      "inθ₁ = 1.33 × 0.6691 = 0.8899"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n1\":\"42\",\"n2\":\"42\",\"angle\":\"42\",\"m1\":\"1.33\",\"m2\":\"1.33\"}，输出区含「inθ₁ = 1.33 × 0.6691 = 0.8899」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "glass/thickness-selection",
    "inputs": {
      "width": "42",
      "height": "42",
      "scene": "door"
    },
    "expect": [
      "→ 推荐最小厚度 6 mm 步骤3 涉及安全，采用钢化玻璃 结论 42×42mm 玻璃（0.00m²）用于玻璃门，推荐 6mm钢化玻璃"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width\":\"42\",\"height\":\"42\",\"scene\":\"door\"}，输出区含「→ 推荐最小厚度 6 mm 步骤3 涉及安全，采用钢化玻璃 结论 42×42mm…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
  console.log("==== glass calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();