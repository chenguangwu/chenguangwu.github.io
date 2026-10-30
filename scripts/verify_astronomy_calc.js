#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "astronomy/apparent-magnitude-distance",
  "inputs": {
    "m": "4",
    "M": "1"
  },
  "expect": [
    "129.863"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/atmospheric-refraction",
  "inputs": {
    "h": "45"
  },
  "expect": [
    "0.0169"
  ],
  "ref": "auto-restore"
},
{
"slug": "astronomy/convert-15",
"inputs": {
"val": "7",
"unit": "mag"
},
"expect": [
"1.995e+15 J"
],
"ref": "复算：E = 10^(1.5×7+4.8) = 10^15.3 = 1.995e+15 J（≈0.477 百万吨 TNT）；默认 M=6 得 6.310e+13 J ⇒ 不命中"
},
{
  "slug": "astronomy/convert-17",
  "inputs": {
    "val": "12:00",
    "from": "-8"
  },
  "expect": ["12:00\n-8\n1\n21:00 同日"],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/convert-18",
  "inputs": { "val": "540", "mode": "p2h" },
  "expect": ["海拔 h = 5003.5 m"],
  "ref": "气压 540 hPa → 海拔=44330·(1−(540/1013.25)^(1/5.255))=5003.5 m（默认 1013.25 得 0.0 m，注入态不重合）"
},
{
  "slug": "astronomy/convert-18",
  "inputs": { "val": "5360", "mode": "h2p" },
  "expect": ["气压 P = 514.76 hPa"],
  "ref": "海拔 5360 m → 气压=1013.25·(1−5360/44330)^5.255=514.76 hPa"
},
{
  "slug": "astronomy/crater-estimator",
  "inputs": {
    "diameter": "150",
    "density": "3000",
    "velocity": "20",
    "angle": "45"
  },
  "expect": [
    "1.060e+18"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/gravitational-force",
  "inputs": {
    "m1": "5.97e24",
    "m2": "7.35e22",
    "r": "1.0e8"
  },
  "expect": [
    "2.929e+21 引力 F (N)"
  ],
  "ref": "独立复算：F = G·m₁·m₂/r² = 6.674e−11 × 5.97e24 × 7.35e22 / (1.0e8)² = 2.929e21 N。⚠ 原用例注入 '5.97e24_X' 并断言同串（输入回显、零判别力）；默认参数（地月 3.84e8）算得 1.986e20 N，与本串不同 ⇒ 无逃生（已实测）。"
},
{
  "slug": "astronomy/horizon-distance",
  "inputs": {
    "h": "4.7"
  },
  "expect": [
    "7738.7"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/hubble-redshift-distance",
  "inputs": {
    "z": "3.01"
  },
  "expect": [
    "12891.08"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/humidity-calculator",
  "inputs": {
    "tDry": "38",
    "tWet": "20",
    "pAtm": "1013.25"
  },
  "expect": [
    "66.22"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/kepler-equation",
  "inputs": {
    "Mdeg": "135",
    "e": "0.1"
  },
  "expect": [
    "138.776"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/kepler-third-period",
  "inputs": {
    "a": "1.496e11",
    "M": "3.978e30"
  },
  "expect": [
    "258.25 轨道周期 T (天)"
  ],
  "ref": "独立复算：T = 2π√(a³/(GM)) = 2π√((1.496e11)³/(6.674e−11×3.978e30)) ≈ 2.231e7 s = 258.25 天。⚠ 原用例注入 '1.496e11_X' 并断言同串（输入回显、零判别力）；默认中心天体质量 1.989e30 得 365.22 天，与本串不同 ⇒ 无逃生（已实测）。"
},
{
  "slug": "astronomy/light-travel-time",
  "inputs": {
    "d": "5.0e11"
  },
  "expect": [
    "27.797 传播时间 t (min)"
  ],
  "ref": "独立复算：t = d/c = 5.0e11/2.998e8 = 1667.8 s = 27.797 min。⚠ 原用例注入 '1.496e11_X' 并断言同串（输入回显、零判别力）；默认 1 AU ⇒ 8.317 min，与本串不同 ⇒ 无逃生。"
},
{
  "slug": "astronomy/magnitude-comparator",
  "inputs": {
    "nameA": "太阳",
    "magA": "-39.7",
    "nameB": "满月",
    "magB": "-12.6"
  },
  "expect": [
    "1.4437×10"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/moon-illumination",
  "inputs": {
    "D": "7"
  },
  "expect": [
    "45.9"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/observation-conditions",
  "inputs": {
    "latInput": "22.3193",
    "lonInput": "114.1694",
    "cloudInput": "85"
  },
  "expect": [
    "5.2 / 10 观测条件：一般"
  ],
  "ref": "独立复算：云量 85% ⇒ 天气项 3.2、光污染 6.0、月光 5.7 加权得 5.2/10 ⇒ 评级「一般」。⚠ 原 expect '59.9042' 为纬度输入回显（零判别力）。首版改锚「6.5/10 良好」经判别器实测为逃生（默认云量即 6.5），故改用 cloud=85 的 5.2/10 ⇒ 默认态不含该串。"
},
{
  "slug": "astronomy/observation-conditions",
  "inputs": {
    "dateInput": "2026-06-01"
  },
  "expect": [
    "距角 58.7°"
  ],
  "ref": "行星可见性模块：注入固定日期 2026-06-01（默认态为「今天」，距角随日变化 ⇒ 注入失败必变红）。JPL 近似轨道要素算得该日太阳黄经 70.66°、土星地心黄经 12.0° ⇒ 距角 58.7°，评价串「条件良好（距角 58.7°）」。expect 带「距角」上下文，避免裸数字被其它数值子串误命中。"
},
{
  "slug": "astronomy/schwarzschild-radius",
  "inputs": {
    "M": "4.0e30"
  },
  "expect": [
    "5.941 史瓦西半径 r_s (km)"
  ],
  "ref": "独立复算：r_s = 2GM/c² = 2×6.674e−11×4.0e30/(3.0e8)² = 5.941e3 m = 5.941 km。⚠ 原用例注入 '1.989e30_X' 并断言同串（输入回显、零判别力）；默认 M=1.989e30 得 2.954 km，与本串不同 ⇒ 无逃生。"
},
{
  "slug": "astronomy/solar-declination",
  "inputs": {
    "N": "258"
  },
  "expect": [
    "2.216"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/stellar-parallax",
  "inputs": {
    "p": "3.1"
  },
  "expect": [
    "0.323"
  ],
  "ref": "auto-restore"
},
{
  "slug": "astronomy/tide-estimator",
  "inputs": {
    "range": "5",
    "lat": "30",
    "date": "2026-06-21"
  },
  "expect": [
    "6.70 m"
  ],
  "ref": "预测潮差 = range×倍率 = 5×1.34 = 6.70（原断言“5.9 天”是月龄，与 range 无关 → 逃生项）"
}
,
  {
    "slug": "astronomy/sunrise-sunset",
    "inputs": {"inputDate":"2026-06-21","inputLat":"39.9","inputLon":"116.4","inputTz":"8"},
    "clicks": ["calc()"],
    "expect": ["04:46 日出时间", "19:46 日落时间"],
    "ref": "注入非默认 inputDate=2026-06-21(默认空→不计算日出日落) + lat=39.9/lon=116.4/tz=8：夏至北半球日出 04:46、日落 19:46（基于日期+经纬度+时区确定性，不依赖 now）。锚 now 无关值，规避「太阳当前高度 40.5°」等 now 相关串。默认态 inputDate 空→不计算→不命中。"
  }
  ,{
    "slug": "astronomy/earth-curvature",
    "inputs": { "obsHeight": "10", "targetDist": "50", "targetHeight": "20" },
    "expect": ["117.62", "11.29"],
    "ref": "默认 obsHeight=1.7/targetDist=10/targetHeight=5(无折射)→地平线4.65km/遮挡2.24m/可见2.76m。注入 obsHeight=10/targetDist=50/targetHeight=20→地平线=3.57×√10=11.29km、遮挡=(50−11.29)²/(2×6371)×1000=117.62m(目标20m<117.62m→完全遮挡)。锚 117.62 与 11.29，均≠默认态，零逃生。"
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

  console.log("==== astronomy calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
