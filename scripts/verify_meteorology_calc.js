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
  {
    slug: "meteorology/apparent-temperature",
    inputs: {},
    clicks: ["document.getElementById('T').value='20';document.getElementById('RH').value='50';document.getElementById('ws').value='0';calcTool();"],
    expect: ['19.8 °C 体感温度 AT', '11.66 水汽压 e (hPa)', '0.2 体感温差 (°C)'],
    ref: 'Steadman 简化：e = (50/100)×6.105×exp(17.27×20/257.7) = 3.0525×3.819876 = **11.6598** ⇒ `11.66`；AT = 20+0.33×11.6598−0.70×0−4 = **19.8477** ⇒ `19.8`；体感温差 = 20−19.8477 = **0.1523** ⇒ `0.2`。ws=0 把风速项压成 0，钉住 0.33e 与 −4.0 两个常数项。默认态（30/70/2）是 34.4 / 29.60 / −4.4，三条锚全不命中。',
  },
  {
    slug: "meteorology/apparent-temperature",
    inputs: {},
    clicks: ["document.getElementById('T').value='35';document.getElementById('RH').value='90';document.getElementById('ws').value='1';calcTool();"],
    expect: ['46.9 °C 体感温度 AT', '-11.9 体感温差 (°C)'],
    ref: 'e = 0.9×6.105×exp(17.27×35/272.7) = 5.4945×9.179238 = **50.4065** ⇒ `50.41`；AT = 35+0.33×50.4065−0.7−4 = **46.9342** ⇒ `46.9`；体感温差 = 35−46.9342 = **−11.9342** ⇒ `-11.9`（负温差 = 体感比气温更热，toFixed 的负号渲染一并覆盖）。默认态全不命中。',
  },
  {
    slug: "meteorology/apparent-temperature",
    inputs: {},
    clicks: ["document.getElementById('T').value='0';document.getElementById('RH').value='50';document.getElementById('ws').value='10';calcTool();"],
    expect: ['-10.0 °C 体感温度 AT', '3.05 水汽压 e (hPa)', '10.0 体感温差 (°C)'],
    ref: 'T=0 ⇒ exp(0)=1 ⇒ e = 0.5×6.105 = **3.0525** ⇒ `3.05`（指数项归一，钉住 exp 分母 237.7+T 在 T=0 时的退化）；AT = 0+1.0073−7−4 = **−9.9927** ⇒ `-10.0`；体感温差 = **9.9927** ⇒ `10.0`。大风 (ws=10) 把 −0.70×ws 项拉到 −7，与 −4.0 常数叠加成 −11，压住风速系数 0.70。默认态全不命中。',
  },
  {
    slug: "meteorology/apparent-temperature",
    inputs: {},
    clicks: ["document.getElementById('T').value='25';document.getElementById('RH').value='0';document.getElementById('ws').value='3';calcTool();"],
    expect: ['0.00 水汽压 e (hPa)', '18.9 °C 体感温度 AT'],
    ref: 'RH=0 ⇒ e = 0（**0.00**），湿度项整项消失 ⇒ AT = 25−2.1−4 = **18.9**。本条是 e=0 的唯一入口（其余用例 RH 都 >0），钉住「湿度项 ×0 ⇒ AT 只剩 T−0.7ws−4」这条链；体感温差 = 6.1 不锚（避免与例⑤⑥同型）。默认态 e=29.60、AT=34.4，全不命中。',
  },
  {
    slug: "meteorology/apparent-temperature",
    inputs: {},
    clicks: ["document.getElementById('T').value='-10';document.getElementById('RH').value='60';document.getElementById('ws').value='5';calcTool();"],
    expect: ['-16.9 °C 体感温度 AT', '1.72 水汽压 e (hPa)'],
    ref: '负温：exp 分母 = 237.7−10 = 227.7，指数 = −172.7/227.7 = −0.758454 ⇒ exp = 0.468375 ⇒ e = 0.6×6.105×0.468375 = **1.71609** ⇒ `1.72`；AT = −10+0.56631−3.5−4 = **−16.93369** ⇒ `-16.9`。负温下指数为负、e 变小、体感更冷，本条把「负温分支」（T 进分母 237.7+T 与分子 17.27×T 同号）钉住。默认态全不命中。',
  },
  {
    slug: "meteorology/apparent-temperature",
    inputs: {},
    clicks: ["document.getElementById('T').value='30';document.getElementById('RH').value='70';document.getElementById('ws').value='20';calcTool();"],
    expect: ['21.8 °C 体感温度 AT', '8.2 体感温差 (°C)'],
    ref: '与默认态同温同湿（T=30/RH=70 ⇒ e=29.60 相同），只把 ws 2→20：AT = 30+9.768−14−4 = **21.768** ⇒ `21.8`、体感温差 = **8.2**。本条与默认态（34.4/−4.4）构成「同一组 T/RH、只改风速」的成对对照，风速系数 0.70 若写错（如 0.07 或 7.0），AT 会偏离 21.8 而被数值锚抓。刻意不锚 e（29.60 与默认态同值 ⇒ 逃生项）。默认态 AT=34.4，两条锚不命中。',
  },
  // ── §7.4 零用例加固：meteorology 确定性数值页（注入非默认 + harness 实测锚）──
  {
    slug: "meteorology/precipitation-calc",
    inputs: { amt: "25", dur: "90", area: "1500" },
    expect: ["16.7 mm/h", "37.50 m³", "37500 升"],
    ref: "注入非默认(默认 18/60/1000)：降水强度 = 25 mm / 1.5 h = 16.7 mm/h（判定等级「暴雨」）；面积 1500 m² 上折合水量 = 0.025 m × 1500 = 37.50 m³ = 37500 升。默认态 18.0 mm/h / 18.00 m³ / 18000 升 均不命中。"
  },
  {
    slug: "meteorology/analysis-tide",
    inputs: { z0: "2.50", hM2: "1.50", gM2: "15", hS2: "0.45", gS2: "55", hK1: "0.35", gK1: "140", hO1: "0.30", gO1: "220", hours: "36" },
    expect: ["36:00 4.01 m", "27:00 3.58 m", "33:00 1.21 m"],
    ref: "注入非默认(默认 z0=2.00/各分潮振幅相位/hours=24)：由 M2/S2/K1/O1 四个分潮叠加 z = z0 + Σhᵢ·cos(σᵢt − gᵢ)，取 hours=36 ⇒ 逐 3 小时潮位表延伸到 27:00/33:00/36:00，末位 36:00 潮位 4.01 m。默认态只到 24:00，三条均不命中（hours 是唯一控制表长的键）。"
  },
  {
    slug: "meteorology/humidex",
    inputs: { T: "34", RH: "80" },
    expect: ["52.1", "42.51", "18.1"],
    ref: "注入非默认(默认 T=30/RH=70)：水汽压 e = 6.112×10^(7.5T/(237.7+T))×RH/100 ⇒ 42.51 hPa；Humidex = T + (e−10)×5/9 ⇒ 34 + 32.51×0.5556 = 52.1（增量 18.1）。默认态 41.8/29.60/10.9 均不命中。"
  },
  {
    slug: "meteorology/temp-pressure",
    inputs: { temp: "28", rh: "75", pres: "1005.5" },
    expect: ["37.74", "28.30", "23.2°", "1.151"],
    ref: "注入非默认(默认 25/60/1013.25)：饱和水汽压 = 6.112×10^(7.5×28/(237.3+28)) = 37.74 hPa；实际水汽压 = 37.74×75% = 28.30 hPa；露点 ≈ 23.2°C；空气密度 ρ = (Pd/(Rd·T)) + (Pv/(Rv·T)) = 1.151 kg/m³。默认态 31.67/19.00/16.7°/1.183 均不命中。"
  },
  {
    slug: "meteorology/heat-index",
    inputs: { temp: "36", rh: "65", wind: "4" },
    expect: ["51.0°", "36.0°", "+15.0°"],
    ref: "注入非默认(默认 32/70/2)：按 Rothfusz 炎热指数回归式（含湿度、风速校正）⇒ 体感温度 51.0°C，与实际气温 36.0°C 相差 +15.0°，舒适度等级「危险」。默认态 40.3°（温差 +8.3°）不命中。"
  },
  {
    slug: "meteorology/analysis-31",
    inputs: { obs: "28.5", norm: "24.2", sd: "1.4" },
    expect: ["4.30 ℃", "17.8%", "3.07", "异常偏高"],
    ref: "注入非默认(默认 obs=26.8/norm=24.2/sd=1.1)：距平 = 28.5 − 24.2 = 4.30 ℃；距平百分率 = 4.30/24.2 = 17.8%；标准化距平 σ = 4.30/1.4 = 3.07 ⇒ 达异常量级 ⇒「异常偏高」。默认态 2.60/10.7%/2.36（显著偏强）均不命中。"
  },
  {
    slug: "meteorology/wet-bulb-temperature",
    inputs: { T: "32", RH: "70" },
    expect: ["27.46 °C"],
    ref: "注入非默认(默认 T=25/RH=60)：Stull 经验式 T_w = T·atan(0.151977·(RH+8.313659)^0.5) + atan(T+RH) − atan(RH−1.676331) + 0.00391838·RH^1.5·atan(0.023101·RH) − 4.686035 ⇒ 27.46 °C。默认态 19.19 °C 不命中。"
  },
  {
    slug: "meteorology/assessor-29",
    inputs: { pa_cur: "45", pa_avg: "80", spi_cur: "25", spi_avg: "80", spi_std: "40" },
    expect: ["-1.38", "(25 - 80) / 40"],
    ref: "注入非默认(默认 35/80/30/80/40)：SPI ≈ (spi_cur − spi_avg)/spi_std = (25 − 80)/40 = −1.38，页面把算式原样回显。⚠ 「中旱」不能作锚：默认 spi_cur=30 ⇒ SPI = −1.25，也落在 −1.5~−1.0 的中旱档 ⇒ 该文案两态相同；改锚 SPI 数值本身与含注入值的算式串。另 pa_cur/pa_avg 不影响这两条锚，仅作陪注入。"
  },

{
    "slug": "meteorology/taifengdingqiang",
    "inputs": {
      "pc": "980"
    },
    "expect": [
      "43.1 最大风速 (m/s)",
      "83.8 最大风速 (节)",
      "强台风 STY"
    ],
    "ref": "台风中心气压-最大风速换算：p = 980 hPa 查 GB/T 28591-2012 等级表对应 Vmax = 43.1 m/s；节速换算 43.1 × 1.94384 = 83.77 ≈ 83.8 节；980 hPa 属强台风（STY）等级。页面输出 43.1 m/s、83.8 节、强台风与标准换算表吻合。HTML 默认 pc=950 → 66.0 m/s，默认态不产生 43.1。"
  },
  {
    "slug": "meteorology/precipitation-rate",
    "inputs": {
      "mm": "25"
    },
    "expect": [
      "600.00 按 24 小时折算降水量 (mm)",
      "0.9843 降水量 (in 英寸)",
      "0.006944 降水强度 (mm/s)"
    ],
    "ref": "降水强度 25 mm/h：24 小时折算 = 25 × 24 = 600.00 mm；英寸换算 = 25 / 25.4 = 0.98425 ≈ 0.9843 in；单位秒换算 = 25 / 3600 = 0.006944 mm/s。页面输出与独立复算吻合。HTML 默认 mm=12 → 288.00 / 0.4724 / 0.003333，默认态不产生该组值。"
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
  console.log("==== meteorology calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();