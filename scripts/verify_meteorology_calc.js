#!/usr/bin/env node
/**
 * 第 26 道门禁：meteorology 分类计算正确性验证（10 个确定性物理气象工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 覆盖：露点、风寒、饱和水汽压、绝对湿度、云底高度、气压高度、ISA 温度、相对湿度、蒲福风级。
 * 用法: node scripts/verify_meteorology_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  {
    slug: "meteorology/dew-point",
    inputs: { T: "20", RH: "50" },
    expect: ["9.26"],
    ref: "Magnus 式：g=ln(0.5)+17.625×20/263.04=0.6468；Td=243.04×0.6468/(17.625-0.6468)=9.26 °C",
  },
  {
    slug: "meteorology/wind-chill",
    inputs: { T: "-10", v: "15" },
    expect: ["-16.7"],
    ref: "WCT=13.12+0.6215×(-10)-11.37×15^0.16+0.3965×(-10)×15^0.16=-16.7 °C",
  },
  {
    slug: "meteorology/saturation-vapor-pressure",
    inputs: { T: "20" },
    expect: ["23.33"],
    ref: "Tetens 式：e_s=6.1094×exp(17.625×20/263.04)=23.33 hPa",
  },
  {
    slug: "meteorology/absolute-humidity",
    inputs: { T: "20", RH: "50" },
    expect: ["8.61"],
    ref: "AH=1320.65×(50/100)×exp(17.67×20/263.5)/(20+273.15)=8.61 g/m³",
  },
  {
    slug: "meteorology/cloud-base-height",
    inputs: { T: "30", Td: "10" },
    expect: ["2500"],
    ref: "H=(30-10)×125=2500 m（默认温差 10°C 得 1250，此处 20°C 温差得 2500，避开默认值）",
  },
  {
    slug: "meteorology/pressure-altitude",
    inputs: { P: "800", P0: "1013.25" },
    expect: ["1949"],
    ref: "h=44330×(1-(800/1013.25)^0.1903)=1949 m（默认 P=900 得 989，此处避开）",
  },
  {
    slug: "meteorology/isa-temperature",
    inputs: { h: "3" },
    expect: ["-4.5"],
    ref: "T=15-6.5×3=-4.5 °C（对流层每 km 降 6.5°C；默认 h=5 得 -17.5，此处避开）",
  },
  {
    slug: "meteorology/relative-humidity",
    inputs: { T: "20", Td: "10" },
    expect: ["52.5"],
    ref: "RH=100×exp(17.625×10/253.04 - 17.625×20/263.04)=52.5 %",
  },
  {
    slug: "meteorology/beaufort-scale",
    inputs: { v: "20" },
    expect: ["8 级", "大风"],
    ref: "v=20 m/s 落入 ub[8]=20.7 区间 → 8 级（大风）；默认 v=10 得 5 级（和风），此处避开",
  },
  {
    slug: "meteorology/capeduiliuyouxiaoweineng",
    inputs: { tp: "32", te: "24", plfc: "850", pel: "250" },
    expect: ["2848.0 J/kg"],
    ref: "Δz=R_d·Tm/g·ln(p1/p2)=287.04×((305.15+297.15)/2)/9.80665×ln(850/250)=10787m；CAPE=g·(ΔT/Te)·Δz=9.80665×(8/297.15)×10787=2848.0 J/kg（旧版把气压差 Pa 当厚度直接代入 → 同组输入 463705 J/kg；默认 25/20/700/300 亦有 195831，均不重合）",
  },  {
    slug: "meteorology/air-aqi",
    inputs: {"pm25": "55", "pm10": "60"},
    expect: ['55.0 μg/m³ 75', 'PM10 60.0 μg/m³ 55', 'AQI 75 良'],
    ref: 'PM2.5 55 落在 HJ633 第 2 段 [35,75) ⇒ IAQI = (100−50)/(75−35)×(55−35)+50 = 1.25×20+50 = **75**（不是端点 50 也不是 100，线性插值被唯一钉住）；PM10 60 落在第 2 段 [50,150) ⇒ 0.5×(60−50)+50 = **55**。此时 max IAQI 是 PM2.5 的 75 ⇒ 首要污染物 PM2.5、AQI = round(75) = 75 ⇒ 「良」。刻意不锚「首要污染物： PM2.5」与「PM2.5 ★」——默认组（PM2.5 75）的首要污染物同样是 PM2.5，这两条在默认态命中 ⇒ 逃生项；改锚由注入浓度直接决定的两行（`55.0 μg/m³ 75` / `PM10 60.0 μg/m³ 55`）。默认态是 AQI 100 / 75.0 μg/m³ 100，三条锚全不命中。',
  },
  {
    slug: "meteorology/air-aqi",
    inputs: {"pm25": "10", "pm10": "10", "so2": "10", "no2": "102", "co": "0.5", "o3": "10"},
    expect: ['首要污染物： NO₂', 'NO₂ ★ 102.0', 'AQI 111 轻度污染'],
    ref: '把 NO₂ 抬到 102：落在第 3 段 [80,180) ⇒ IAQI = (150−100)/(180−80)×(102−80)+100 = 0.5×22+100 = **111**，六项里唯一最高（PM2.5 10→14、PM10 10→10、SO₂ 10→10、CO 0.5→12、O₃ 10→3）⇒ 首要污染物从默认的 PM2.5 换成 NO₂、AQI = 111。111 > 100 ⇒ `aqiLevel` 的「≤100 为良」不成立，落 `轻度污染`，本条由此把等级判读的边界从上方钉住（与默认态的「良」互为对照）。三条锚分别覆盖「max IAQI 换人」「★ 只出现在首要污染物行」「等级分档」。',
  },
  {
    slug: "meteorology/air-aqi",
    inputs: {"pm25": "115"},
    expect: ['AQI 150 轻度污染', 'PM2.5 115.0 μg/m³ 150'],
    ref: 'PM2.5 = 115 正好落在第 3 段右端点（115 <= 115 命中该段）⇒ IAQI = (150−100)/(115−75)×(115−75)+100 = 1.25×40+100 = **150**，AQI = 150，而 `aqiLevel` 是 `<=150` ⇒ 判「轻度污染」。本条压两处：`calcIAQI` 的 `c<=s[1]` 闭区间（若写成开区间会掉到第 4 段得 200）与分档的 `<=`（150 归轻度而非中度）。默认态 AQI 100 / 良，两条锚全不命中。',
  },
  {
    slug: "meteorology/air-aqi",
    inputs: {"pm25": "600"},
    expect: ['AQI 500 严重污染', 'PM2.5 600.0 μg/m³ 500'],
    ref: 'PM2.5 = 600 超过分段表最高档右端 500 ⇒ 七个段全不命中，跳过循环执行 `return 500` 兜底。于是 max IAQI = 500 ⇒ AQI = 500 ⇒ `严重污染`（`aqiLevel` 最后一个 return 分支）。本条覆盖「超最高限值的回落路径」，也是全站唯一能把 AQI 顶到 500 的入口。默认态 AQI 100，两条锚全不命中。',
  },
  {
    slug: "meteorology/air-aqi",
    inputs: {"pm25": "-1", "pm10": "-1", "so2": "-1", "no2": "-1", "co": "-1", "o3": "-1"},
    expect: ['首要污染物： 无', 'AQI 0 优', '空气质量令人满意'],
    ref: '六项全置 −1 ⇒ `calcIAQI` 的 `c<0` 卫语句全数命中并 return null ⇒ `iaqiList` 为空、`maxIAQI` 保持初值 0、`primary` 保持空串 ⇒ 渲染 `primary||\'无\'` 的兜底分支打印「首要污染物： 无」，AQI 走 `Math.round(0)` = 0 ⇒ 判「优」。本条唯一覆盖 `primary||\'无\'` 与空列表两个分支（其余五条都没走）。默认态必打印具体污染物名，三条锚全不命中。',
  },
  {
    slug: "meteorology/air-aqi",
    inputs: {"pm25": "20", "pm10": "0", "so2": "0", "no2": "0", "co": "0", "o3": "0"},
    expect: ['AQI 29 优', 'PM2.5 20.0 μg/m³ 29', 'CO 0.00 mg/m³ 0'],
    ref: 'PM2.5 = 20 在第 1 段 [0,35] ⇒ IAQI = (50−0)/(35−0)×20 = **28.571** ⇒ AQI = round = 29（若按截断或按未取整算会得 28，本条把取整钉住）；其余五项为 0 ⇒ IAQI 恒 0，仍进表（0 不触发 `c<0`）。浓度列走 `it.c.toFixed(it.c<10?2:1)` 的小数位分档，故本条同时出现 `20.0`（≥10 一位小数）与 `CO 0.00 mg/m³`（<10 两位小数）两种形态，分档写反会被抓。默认态 AQI 100，三条锚全不命中。',
  },

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
  console.log("==== meteorology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();