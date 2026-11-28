#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "urban/building-height",
  "inputs": {
    "inD": "40",
    "inLat": "25",
    "inCoeff": "auto",
    "inFloorH": "3",
    "inH0": "50",
    "inL": "3000",
    "inSafety": "0",
    "inLimit": "60",
    "inFloorH2": "3",
    "inDiff": "0.6",
    "inParapet": "1.2"
  },
  "expect": [
    "取 13 层（39.0 m）"
  ],
  "ref": "确定性算例：D=40 m、纬度 25°N → 自动间距系数 1.0，H=40.0 m，40/3=13.3 → 取 13 层（39.0 m）；默认 D=30/35°N 得 7 层，注入态不含该串 ⇒ 锁定层数与高度派生值，可区分随机/回显。"
},
{
  "slug": "urban/calc-spacing",
  "inputs": {
    "height": "45",
    "lat": "39.9",
    "date": "2024-12-22",
    "hours": "2"
  },
  "expect": [ "89.60 正午阴影长度" ],
  "ref": "auto-restore"
},
{
  "slug": "urban/calc-spacing",
  "inputs": { "height": "30", "lat": "39.9", "date": "2024-12-22", "hours": "48" },
  "expect": ["超过当日理论日长", "目标不可实现"],
  "ref": "目标 48h 远超冬至日理论日长（约 9.3h），停止计算，不再用周期三角函数给出有限间距。"
},
{
  "slug": "urban/calc-spacing",
  "inputs": { "height": "30", "lat": "80", "date": "2024-12-21", "hours": "2" },
  "expect": ["极夜", "当日无日照"],
  "ref": "北纬 80° 冬至为极夜，日长 0；任何正目标时长均不可实现。"
},
{
  "slug": "urban/calc-spacing",
  "inputs": { "height": "40", "lat": "39.9", "date": "2024-12-22", "hours": "2" },
  "expect": ["正午前后对称", "需专业复核"],
  "ref": "有效态附模型范围说明（正午对称、无其他遮挡），避免把估算当审批结论。"
},
{
  "slug": "urban/green-ratio",
  "inputs": {
    "inTotal": "75000",
    "inGreen": "17500",
    "inCanopy": "22000",
    "inPop": "3000"
  },
  "expect": [ "7.50 公顷" ],
  "ref": "auto-restore"
},
{
  "slug": "urban/green-ratio",
  "inputs": { "inTotal": "100", "inGreen": "80", "inCanopy": "50", "inOverlap": "30", "inPop": "10" },
  "expect": ["绿化覆盖率：(80+50−30) ÷ 100 × 100% = 100.00 %", "重叠面积已按填写值扣除"],
  "ref": "绿地 80 + 树冠 50 − 重叠 30 = 并集 100，覆盖率 100%；旧实现直接 80+50=130% 重复计数。"
},
{
  "slug": "urban/green-ratio",
  "inputs": { "inTotal": "100", "inGreen": "80", "inCanopy": "50", "inOverlap": "60", "inPop": "10" },
  "expect": ["重叠面积不能超过绿地面积与树冠投影面积中的较小值"],
  "ref": "重叠 60 > min(80,50)=50，几何关系不成立，停止计算。"
},
{
  "slug": "urban/green-ratio",
  "inputs": { "inTotal": "100", "inGreen": "120", "inCanopy": "50", "inOverlap": "0", "inPop": "10" },
  "expect": ["绿地面积不能大于总用地面积"],
  "ref": "绿地面积 120 > 总用地 100，拒绝计算。"
},
{
  "slug": "urban/green-ratio",
  "inputs": { "inTotal": "200", "inGreen": "80", "inCanopy": "50", "inOverlap": "", "inPop": "10" },
  "expect": ["重叠面积留空按 0 计算"],
  "ref": "重叠留空按 0 并明确提示可能高估覆盖率。"
},
{
  "slug": "urban/land-use",
  "inputs": {
    "inPop": "80000",
    "area_R": "300",
    "area_A": "80",
    "area_B": "60",
    "area_M": "100",
    "area_S": "150",
    "area_U": "20",
    "area_G": "120"
  },
  "clicks": ["calc()"],
  "expect": [ "830.0 ha", "103.8 m²" ],
  "ref": "auto-restore"
},
{
  "slug": "urban/parking-ratio",
  "inputs": { "inArea": "10000", "inRatio": "1", "inVisitor": "100", "inSpaceArea": "30", "inAccessible": "2" },
  "clicks": ["calc();"],
  "expect": ["常规车位：100 − 100 = 0 个", "从访客车位划出"],
  "ref": "访客 100% ⇒ 常规车位 0；无障碍 2 个计入总车位、从访客车位划出，不再声称“含在常规车位内”造成 0 个常规却含 2 个无障碍的矛盾。"
},
{
  "slug": "urban/parking-ratio",
  "inputs": { "inArea": "10000", "inRatio": "1", "inVisitor": "20", "inSpaceArea": "30", "inAccessible": "20" },
  "clicks": ["calc();"],
  "expect": ["无障碍车位比例须在 0–10% 之间"],
  "ref": "无障碍比例 20% 越界，停止计算。"
},
{
  "slug": "urban/population-density",
  "inputs": { "inPop": "50000", "inArea": "200", "inResArea": "", "inAreaC": "200", "inPerCap": "100", "inResRatio": "40", "inNetDensity": "500" },
  "expect": ["未完成校核", "居住用地面积缺失", "人口净密度无法计算"],
  "ref": "居住用地面积留空：净密度不可计算，显示未完成校核，不再把净密度当 0 参与并判定“符合”。"
},
{
  "slug": "urban/population-density",
  "inputs": { "inPop": "50000", "inArea": "200", "inResArea": "250", "inAreaC": "200", "inPerCap": "100", "inResRatio": "40", "inNetDensity": "500" },
  "expect": ["居住用地面积不能大于总用地面积"],
  "ref": "居住用地 250 > 总用地 200，几何关系错误，停止计算。"
},
{
  "slug": "urban/parking-ratio",
  "inputs": {
    "inArea": "60000",
    "inRatio": "1.2",
    "inVisitor": "25",
    "inSpaceArea": "30",
    "inAccessible": "3",
    "inUnit": "100m2"
  },
  "clicks": ["calc();"],
  "expect": [
    "÷ 100 × 1.2 = 720.0"
  ],
  "ref": "非默认输入 60000/1.2/25/30/3 派生：60,000÷100×1.2=720.0 个车位；原 expect「100m2」是固定单位标签（两态均命中，判别器实测逃生）。默认态 50,000÷100×1=500.0，不命中。不注入 inType：该 select 的 onchange=onTypeChange() 会把 inArea/inRatio 重置为类型默认，导致派生值回退。"
},
{
  "slug": "urban/population-density",
  "inputs": {
    "inPop": "75000",
    "inArea": "200",
    "inResArea": "80",
    "inAreaC": "200",
    "inPerCap": "100",
    "inResRatio": "40",
    "inNetDensity": "500"
  },
  "expect": [
    "75000"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
}
,{
  "slug": "urban/building-height",
  "inputs": { "inD": "30", "inLat": "35", "inCoeff": "auto", "inFloorH": "3", "inH0": "100", "inL": "1000", "inSlope": "0.02", "inSafety": "0", "inGround": "100", "inLimit": "60", "inFloorH2": "3", "inDiff": "0.6", "inParapet": "1.2" },
  "clicks": ["calcAviation();"],
  "expect": ["120.0 m（绝对高程）", "地面以上可用高度：120.0 − 100 = 20.0 m", "6 层"],
  "ref": "跑道与地面标高均 100m、L=1000m、坡度2% ⇒ 限制面标高120m；地面以上可用高度=120−100=20m、6层。旧实现直接显示120m并当建筑高度。"
},
{
  "slug": "urban/building-height",
  "inputs": { "inD": "30", "inLat": "35", "inCoeff": "auto", "inFloorH": "3", "inH0": "50", "inL": "3000", "inSlope": "0.02", "inSafety": "0", "inGround": "0", "inLimit": "1.8", "inFloorH2": "3", "inDiff": "0.6", "inParapet": "1.2" },
  "clicks": ["calcFloor();"],
  "expect": ["无可建楼层", "可用于楼层的高度 ≤0"],
  "ref": "限高 1.8 = 高差0.6+女儿墙1.2 ⇒ 可用于楼层高度 0，边界即无可建楼层，不再输出 0/负层数和“满足”。"
},
{
  "slug": "urban/building-height",
  "inputs": { "inD": "30", "inLat": "35", "inCoeff": "auto", "inFloorH": "3", "inH0": "50", "inL": "3000", "inSlope": "0.02", "inSafety": "0", "inGround": "0", "inLimit": "1.0", "inFloorH2": "3", "inDiff": "0.6", "inParapet": "1.2" },
  "clicks": ["calcFloor();"],
  "expect": ["可用于楼层的高度 ≤0"],
  "ref": "限高 1.0 < 0.6+1.2=1.8 ⇒ 可用于楼层高度为负，必须停止输出。"
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

  console.log("==== urban calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
