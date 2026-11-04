#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "livestock/ammonia-ventilation",
  "inputs": {
    "nh3Current": "38",
    "nh3Target": "15",
    "houseLength": "30",
    "houseWidth": "10",
    "houseHeight": "3",
    "nh3Gen": "0"
  },
  "expect": ["1394 m³/h", "23.2 m³/min", "换气次数 1.5 次/h"],
  "ref": "独立复算：舍体积 30×10×3=900 m³；Q=900×ln(38/15)/(1×0.6)=900×0.92921/0.6=1393.9 ⇒ 1394 m³/h；每分钟 1394/60=23.2；换气 1394/900=1.549 ⇒ toFixed(1)=1.5 次/h。默认态（25/15/0.6）为 900×0.5108/0.6=766 m³/h，三条均不命中。"
},
{
  "slug": "livestock/analysis-18",
  "inputs": {
    "hens": "8000",
    "days": "5",
    "eggs": "35200",
    "eggw": "60",
    "feed": "4700"
  },
  "expect": [
    "88.00",
    "2.23",
    "40,000"
  ],
  "ref": "蛋鸡产蛋：饲养日=8000×5=40000，产蛋率=35200/40000=88.00%；总蛋重=35200×60/1000=2112kg，料蛋比=4700/2112=2.23（独立复算，非页面默认值）",
},
{
  "slug": "livestock/animal-welfare-score",
  "inputs": {
    "s1": "10",
    "s2": "8",
    "s3": "7",
    "s4": "7",
    "s5": "6",
    "s6": "8",
    "s7": "8",
    "s8": "6",
    "s9": "7"
  },
  "expect": [
    "74.6"
  ],
  "ref": "独立复算：9 项权重 1/1/1/1/1/1.2/1/1/1，总权重 9.2；加权总分 = 10×1+8+7+7+6+8×1.2+8+6+7 = 68.6；finalScore = 68.6÷9.2×10 = 74.5652 ⇒ 74.6。原 expect「100.0」是 s1=12 被 range max=10 截断后的逃生态（全部 10 分）；「良好」等级标签不能作锚（默认态 72.4 同样是「良好」，注入失败时仍 PASS ⇒ 逃生物），故只留 74.6。默认态（8/8/7/7/6/8/8/6/7）为 72.4，不命中。"
},
{
  "slug": "livestock/calc-58",
  "inputs": {
    "ped": "P,\nQ,\nR,P,Q\nS,P,Q\nT,R,S"
  },
  "clicks": ["calc()"],
  "expect": [
    "0.25000",
    "25.000%",
    "5 个体总数"
  ],
  "ref": "通径法：T 的父母 R、S 为全同胞，共同祖先 P、Q（均为始祖、F=0）。"
     + "F_T=Σ(1/2)^(n1+n2+1)×(1+F_A)：R-P-S 路径 (1/2)^3=0.125，R-Q-S 路径 0.125 ⇒ F_T=0.25 ⇒ 25.000%。"
     + "个体总数=5。原系谱（X,B,C）所有个体 F=0.00000，原 expect「0.00000」即默认态常量 ⇒ 零判别力。",
  },
{
  "slug": "livestock/calving-interval",
  "inputs": {
    "daysToFirstBreed": "113",
    "breedTimes": "3",
    "gestation": "283"
  },
  "expect": [ "33% 受胎率(估)" ],
  "ref": "独立复算：受胎率 = 1 ÷ 配种次数 3 × 100% = 33.33% ⇒ 页面 toFixed(0) 取 33%。产犊间隔/空怀天数不可作锚——上次产犊日期留空时脚本固定取「今天−365 天」，间隔恒 365、空怀恒 365−283=82，与默认态完全相同（注入失败仍 PASS 即逃生物）；daysToFirstBreed=113 只是「产后首次配种」回显。默认配种 2 次 ⇒ 50%，与本条 33% 不同，具判别力。"
},
{
  "slug": "livestock/calving-interval",
  "inputs": { "gestation": "0" },
  "expect": [ "请输入有效妊娠期" ],
  "ref": "0 天妊娠期无生物学意义：旧实现 `num('gestation') || 283` 会把留空/0 静默回退默认 283 天，用户输入 0 却按 283 计算；改为显式拒绝。默认 283 不出现该提示。"
},
{
  "slug": "livestock/estimate-yield",
  "inputs": { "qty": "1000", "ts": "20", "hrt": "0" },
  "expect": [ "水力停留时间（>0 天）" ],
  "ref": "HRT=0 时反应器容积恒为 0 m³，旧 `valid` 只校验 qty>0 && ts>0，仍会把 0 容积当作有效结果输出；改为要求 hrt>0。默认 hrt=20 不出现该提示。"
},
{
  "slug": "livestock/estimate-yield",
  "inputs": { "qty": "1000", "ts": "120", "hrt": "20" },
  "expect": [ "TS（0–100%）" ],
  "ref": "含固率 >100% 无物理意义（旧实现仅要求 ts>0，120% 会照算）；改为 ts≤100 拦截。默认 ts=20 不出现该提示。"
},
{
  "slug": "livestock/fattening-pig-timeline",
  "inputs": { "currentWeight": "60", "targetWeight": "110", "adg": "800", "fcr": "0", "feedPrice": "3.5" },
  "expect": [ "料肉比（>0）" ],
  "ref": "料肉比 0 会让预计饲料消耗与饲料成本恒为 0，旧实现只校验体重/日增重；改为 fcr>0（饲料单价 ≥0）显式拒绝。默认 fcr=2.8 不出现该提示。"
},
{
  "slug": "livestock/poultry-light-program",
  "inputs": { "currentAge": "0" },
  "expect": [ "请输入有效日龄（≥1 天）" ],
  "ref": "旧实现 `parseInt(age) || 1` 把 0 日龄静默改成 1 日龄并显示「1 天」，与用户输入不符；改为显式拒绝。默认 1 日龄不出现该提示。"
},
{
  "slug": "livestock/castration-timing",
  "inputs": {
    "animalType": "cattle"
  },
  "expect": [
    "cattle"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。"
},
{
  "slug": "livestock/detector-12",
  "inputs": {
    "afb1": "15",
    "zea": "100",
    "don": "1000",
    "ota": "50"
  },
  "expect": [
    "75%"
  ],
  "ref": "独立复算：猪默认限量 AFB1 20 μg/kg、ZEA 250、DON 1000、OTA 100；注入 15/100/1000/50 ⇒ 占比 75%/40%/100%/50%，最大项为 AFB1 15÷20×100 = 75%。"
},
{
  "slug": "livestock/disinfectant-dilution",
  "inputs": {
    "stockConc": "8",
    "targetConc": "0.1",
    "totalVol": "10"
  },
  "expect": [
    "9875ml"
  ],
  "ref": "独立复算：母液体积 = 目标 0.1% × 总液量 10 L ÷ 原液 8% = 0.125 L；加水量 = 10 − 0.125 = 9.875 L = 9875 ml，与页面输出单位 ml 一致（1 L = 1000 ml）。"
},
{
  "slug": "livestock/dongtishouroulv-beibiaohouceding",
  "inputs": {
    "bf": "27",
    "lw": "100"
  },
  "expect": ["48.65%","36.5 瘦肉重 (kg)"],
  "ref": "独立复算：瘦肉率 = 62 − 0.55×背膘 27 − 0.025×(100 − 活重 100) + 母猪校正 1.5 = 62 − 14.85 + 0 + 1.5 = 48.65%；胴体重 = 活重 100 × 屠宰率 75% = 75.0 kg；瘦肉重 = 75.0 × 48.65% = 36.4875 ⇒ 36.5 kg。「75.0 胴体重」不作锚——默认活重同为 100 kg ⇒ 胴体重默认态也是 75.0，注入失败仍 PASS（逃生物）。默认背膘 18 ⇒ 瘦肉率 53.60%、瘦肉重 40.2，与两条锚均不命中。"
},
{
  "slug": "livestock/estimate-yield",
  "inputs": {
    "qty": "1500",
    "ts": "20",
    "hrt": "20"
  },
  "expect": [
    "126.00"
  ],
  "ref": "独立复算：默认畜种为猪（产气率 0.42 m³/kg TS）；干物质量 = 存栏 1500 × 含固率 20% = 300 kg；日产沼气 = 300 × 0.42 = 126.00 m³。默认态 qty=1000 ⇒ 200×0.42 = 84.00，与 126.00 不同，具判别力。"
},
{
  "slug": "livestock/fattening-pig-timeline",
  "inputs": {
    "currentWeight": "90",
    "targetWeight": "120",
    "adg": "800",
    "fcr": "2.8",
    "feedPrice": "3.5"
  },
  "expect": [
    "预计饲养天数 38"
  ],
  "ref": "独立复算：(120 − 90) ÷ 0.8 kg/天 = 37.5 ⇒ 向上取整 38 天；「预计出栏日期」用 new Date() 相对今天推算、绝对日期漂移，故只锚与今天无关的饲养天数。"
},
{
  "slug": "livestock/feed-conversion-ratio",
  "inputs": {
    "startWeight": "45",
    "endWeight": "100",
    "totalFeed": "180",
    "days": "90",
    "feedKg": "180",
    "feedPrice": "3.5",
    "gainKg": "70",
    "salePrice": "18"
  },
  "expect": [
    "3.273"
  ],
  "ref": "独立复算：增重 = 100 − 45 = 55 kg；料肉比 = 总耗料 180 ÷ 55 = 3.2727 ⇒ 3.273（页面三位小数）。输入里的 days / feedPrice / salePrice 卡片另算，本条只锚 FCR。"
},
{
  "slug": "livestock/heat-stress-index",
  "inputs": {
    "temp": "45",
    "humidity": "70",
    "windSpeed": "0.5"
  },
  "expect": [
    "103.92"
  ],
  "ref": "独立复算：THI = (1.8×45 + 32) − (0.55 − 0.0055×70)×(1.8×45 − 26) = 113 − 0.165×55 = 103.925；JS toFixed(2) 因二进制表示得 103.92（浮点舍入边界），与页面一致。风速修正后的调整值另计，本条只锚原始 THI。"
},
{
  "slug": "livestock/inbreeding-coefficient",
  "inputs": {
    "ne": "75",
    "generations": "5",
    "fa": "0",
    "n1": "2",
    "n2": "2",
    "numAncestors": "1"
  },
  "expect": [
    "3.29%",
    "0.667%",
    "96.71%"
  ],
  "ref": "独立复算：ΔF = 1 ÷ (2×Ne 75) = 0.006667 ⇒ 0.667%/代；5 代累积 F = 1 − (1 − 0.006667)^5 = 1 − 0.96711 = 0.03289 ⇒ 3.29%；遗传多样性保留 = 0.96711 ⇒ 96.71%。原 expect「1/(2×75)」只是公式文本回显。"
},
{
  "slug": "livestock/manure-amount",
  "inputs": {
    "count": "150",
    "days": "365",
    "moisture": "85",
    "customManure": "0",
    "collectRate": "90"
  },
  "expect": [
    "2315.9",
    "347.39",
    "2387.6"
  ],
  "ref": "独立复算：泌乳牛日产粪 47 kg × 150 头 × 365 天 = 2,573,250 kg；收集率 90% ⇒ 2,315,925 kg = 2315.9 t；干物质 = 2,315,925 × (1 − 85%) = 347,388.75 kg = 347.39 t；堆肥体积按密度 1000 − (100−85)×2 = 970 kg/m³ ⇒ 2387.6 m³。原 expect 只是「150头奶牛在365天内产生约」的输入回显。"
},
{
  "slug": "livestock/manure-pit-capacity",
  "inputs": {
    "count": "300",
    "dailyManure": "45",
    "moisture": "88",
    "cleanCycle": "7",
    "pitDepth": "2.5",
    "storageDays": "90"
  },
  "expect": [
    "13500.0"
  ],
  "ref": "独立复算：日产粪量 = 存栏 300 × 单头 45 kg/天 = 13500.0 kg/天，与页面「日产粪量」卡单位 kg 一致；清粪周期 7 天与池深 2.5 m 只影响池容积卡，本条锚日产粪量。"
},
{
  "slug": "livestock/milk-yield-scc",
  "clicks": ["records=[{day:1,yield:28.5,scc:12},{day:2,yield:30.2,scc:15},{day:3,yield:31.8,scc:18},{day:4,yield:33.1,scc:22}];analyze()"],
  "expect": [
    "30.9 平均产奶量",
    "上升趋势（斜率 1.54 kg/天）",
    "33.1 最高产奶量"
  ],
  "ref": "顶层数组 records 注入 4 条（页面要求 ≥2 条才分析）：均值 (28.5+30.2+31.8+33.1)/4 = 30.9；线性回归 Sxy = 7.7、Sxx = 5 ⇒ 斜率 1.54 kg/天；最大产奶量 33.1。默认态为源码内置记录（26.93），三串均不命中。"
},
{
  "slug": "livestock/mycotoxin-limit",
  "inputs": {
    "measuredValue": "23"
  },
  "expect": [
    "230.0%"
  ],
  "ref": "独立复算：默认毒素为黄曲霉毒素 B1、默认畜种育肥猪，限量 10 μg/kg；实测 23 ÷ 10 × 100 = 230.0%。若改毒素/畜种可命中其它限量行，本条锚默认组合。"
},
{
  "slug": "livestock/poultry-light-program",
  "inputs": {
    "currentAge": "4"
  },
  "expect": [
    "22小时"
  ],
  "ref": "独立复算：4 日龄落在「4~7 日龄」光照程序行，该行照时 22 h；默认 1 日龄落在「1~3 日龄」行（23 h）。本断言是表驱动查表结果，非页面计算结果存档。"
},
{
  "slug": "livestock/silage-density-ph",
  "inputs": {
    "siloLength": "15",
    "siloWidth": "4",
    "siloHeight": "2.5",
    "siloWeight": "80",
    "dmContent": "33",
    "phValue": "4.0",
    "phDM": "33",
    "smellScore": "4"
  },
  "expect": [
    "150.00"
  ],
  "ref": "独立复算：窖体积 = 长 15 × 宽 4 × 高 2.5 = 150.00 m³；鲜重密度 = 80 t × 1000 ÷ 150 = 533.3 kg/m³；干物质密度 = 533.3 × 33% = 176。默认（长 10）体积 100.0 m³，与 150.00 不冲突。"
},
{
  "slug": "livestock/stats-7",
  "inputs": {
    "tot": "300",
    "mild": "21",
    "hard": "9"
  },
  "expect": [
    "3.00",
    "10.00",
    "270"
  ],
  "ref": "产犊难产：总数 300、轻度助产 21、难产 9 → 顺产 270 头；难产率=9/300=3.00%，需助产率=30/300=10.00%（独立复算，非页面默认值）",
},
{
  "slug": "livestock/vaccine-schedule",
  "inputs": {
    "animalType": "layer"
  },
  "expect": [
    "禽流感H5+H7灭活苗"
  ],
  "ref": "独立复算：免疫程序表按 animalType 取行，layer（蛋鸡）程序首条为「禽流感H5+H7灭活苗」，表驱动查表结果；默认 cow 程序首条为口蹄疫疫苗，注入后必命中蛋鸡行。"
},
{
  "slug": "livestock/vaccine-schedule",
  "inputs": {
    "animalType": "cattle",
    "birthDate": "2026-11-20"
  },
  "checkIds": ["showDate"],
  "expect": [
    "2027年3月20日",
    "2027年11月20日"
  ],
  "ref": "牛程序 120 日龄 ⇒ 2027-03-20、365 日龄 ⇒ 2027-11-20，均跨年；旧实现只显示「3月20日 / 11月20日」不带年份，跨年计划无法区分。默认出生日期为空 ⇒ 不输出日期串，两条锚均不命中；注入失败回退默认亦不命中。"
},
{
  "slug": "livestock/water-feed-ratio",
  "inputs": {
    "waterIntake": "12",
    "feedIntake": "2.5",
    "temp": "22"
  },
  "expect": [ "4.80 : 1", "12.00 L/头·天" ],
  "ref": "独立复算：饮水 12 L ÷ 采食 2.5 kg = 4.8 ⇒ 页面保留两位「4.80 : 1」；12.00 L/头·天 为饮水输入回显，仅作单位一致性锚（L/头·天 与输入标签一致）。默认态（10/2/22）比值为 5.00。"
},
{
  "slug": "livestock/weaning-weight-survival",
  "inputs": {
    "bornAlive": "18",
    "weanedAlive": "11",
    "weanDay": "28",
    "avgWeight": "7.5",
    "standardWeight": "6.0",
    "belowStandard": "2"
  },
  "expect": [
    "61.1%"
  ],
  "ref": "独立复算：断奶成活率 = 断奶存活 11 ÷ 产活仔 18 × 100 = 61.111 ⇒ 61.1%。默认态（20/17）为 85.0%，与 61.1% 不同，具判别力。"
},
{
  "slug": "livestock/withdrawal-period",
  "inputs": {
    "withdrawalDays": "14",
    "drugSelect": "oxytetracycline"
  },
  "expect": [
    "休药期 28 天"
  ],
  "ref": "独立复算：药品表 oxytetracycline（土霉素）休药期 28 天，表驱动查表；“结束日期”用 new Date() 相对今天，故只锚与今天无关的表值。"
},
{
  "slug": "livestock/yufeirizengzhong-liaoroubiquxian",
  "inputs": {
    "w0": "450",
    "w1": "480",
    "days": "120",
    "feed": "1100",
    "price": "3.2"
  },
  "expect": [
    "117.33"
  ],
  "ref": "独立复算：增重 = 480 − 450 = 30 kg；料肉比 = 耗料 1100 ÷ 30 = 36.6667；每公斤增重成本 = 36.6667 × 3.2 元/kg = 117.333 ⇒ 117.33 元。默认态（w0 400 / w1 450）为 70.00 元，不命中。"
}
,
{
  "slug": "livestock/breeding-timing",
  "inputs": { "animalType": "sow" },
  "expect": ["妊娠期 约 114 天"],
  "ref": "注入非默认动物类型 sow（默认 cow）→ 妊娠期 114 天（默认牛 280 天）；妊娠期为物种固定常数、与基准日无关，默认态不含，0 逃生。"
}
,
{
  "slug": "livestock/silage-density-ph",
  "inputs": { "siloLength": "10", "siloWidth": "4", "siloHeight": "2.5", "siloWeight": "80", "dmContent": "33", "phValue": "3.8", "phDM": "32", "smellScore": "5" },
  "dumpIds": ["resultPH"],
  "expect": ["综合评分 97.0 / 100"],
  "ref": "独立复算：玉米青贮 pH 3.8 ≤ 4.0 ⇒ phScore 95；干物质 32% 落在 30–40 ⇒ dmScore 100；气味 5/5 ⇒ smellScore 100。综合 = 95×0.6 + 100×0.2 + 100×0.2 = 97.0。默认（pH 4.0/33%/4）恰为 93.0，故不能用 93.0 作锚；旧线性 phScore（≈100）得 100.0，本条 97.0 只有分级子分口径生效才产出。"
},
{
  "slug": "livestock/silage-density-ph",
  "inputs": { "siloLength": "10", "siloWidth": "4", "siloHeight": "2.5", "siloWeight": "80", "dmContent": "33", "phValue": "3.9", "phDM": "18", "smellScore": "1" },
  "dumpIds": ["resultPH"],
  "expect": ["67.0 / 100", "综合品质 一般"],
  "ref": "独立复算：pH 3.9 优秀 ⇒ phScore 95；干物质 18%（<20）⇒ dmScore 30；气味 1/5 ⇒ smellScore 20。综合 = 95×0.6 + 30×0.2 + 20×0.2 = 67.0 ⇒ 一般。旧实现 pH 优秀却因低干物质/低气味仍得 70.0 ⇒ 良好，本条即针对「pH 优秀但综合一般」的矛盾；默认态干物质 33%、气味 4 得 92.0 优秀，两条均不命中。"
},
{
  "slug": "livestock/ammonia-ventilation",
  "inputs": { "nh3Current": "10", "nh3Target": "15", "houseLength": "30", "houseWidth": "10", "houseHeight": "3", "efficiency": "0.6", "nh3Gen": "50" },
  "dumpIds": ["result"],
  "expect": ["7937 维持通风量", "需维持至少 7937 m³/h", "约 8.8 次/h"],
  "ref": "独立复算：当前 10 ppm ≤ 目标 15 ppm，但持续产氨 50 g/h ⇒ 维持通风量 = 50×1000 ÷ (15×0.7) ÷ 0.6 = 7936.5079 ⇒ 7937 m³/h；换气 = 7937 ÷ 900 = 8.8 次/h。旧实现此分支只提示「正常通风即可」、不输出维持风量，三条均不命中；默认态（25/15/0 g/h）浓度高于目标、走稀释分支，亦不命中。"
},
  // ── 热应激：湿度留空必须拦截，不能静默按 0% 降级 ────────────────
  {
    "slug": "livestock/heat-stress-index",
    "inputs": { "temp": "30", "humidity": "", "windSpeed": "0.5", "animalType": "dairy" },
    "expect": ["请输入有效温度（-20~50℃）和相对湿度（0~100%）"],
    "ref": "湿度留空 ⇒ 旧实现 num() 转 0%、THI 70.6 判「轻微」；修复后必须拦截提示。30℃/70% 的 THI 为 81.4，默认态（30℃/70%）不出现该提示。"
  },
  // ── 热应激：湿度 >100% 属不可能值，必须拦截 ────────────────────
  {
    "slug": "livestock/heat-stress-index",
    "inputs": { "temp": "30", "humidity": "150", "windSpeed": "0.5", "animalType": "dairy" },
    "expect": ["请输入有效温度（-20~50℃）和相对湿度（0~100%）"],
    "ref": "RH 150% 超出物理上限 ⇒ 必须拦截；旧实现算出 THI 93.7 判「危险」。默认 70% 不触发。"
  },
  // ── 霉菌毒素：ZEN 150 μg/kg（仔猪料限量 250）应判「合格/60%」──
  {
    "slug": "livestock/mycotoxin-limit",
    "inputs": { "toxinType": "zearalenone", "feedCategory": "piglet", "measuredValue": "150" },
    "expect": ["60.0%", "合格"],
    "ref": "ZEA 仔猪料限量 250 μg/kg ⇒ 占比 150/250 = 60.0%，判「合格」；默认毒素/实测值不命中这两条。旧正文算例称 150 应超标，现正文已与本表口径对齐并注明以现行标准/当地法规为准。"
  },
  // ── 水料比：温度留空不能按 0℃ 收窄正常区间后误判 ────────────────
  {
    "slug": "livestock/water-feed-ratio",
    "inputs": { "waterIntake": "12", "feedIntake": "2.5", "temp": "", "animalType": "pig" },
    "expect": ["请输入有效温度（-20~50℃）"],
    "ref": "温度留空 ⇒ 旧实现按 0℃ 修正（正常区间收窄约 40%），把 4.8 的水料比误判为偏高；修复后必须拦截。默认 22℃ 不出现该提示。"
  },
  // ── 储粪池：含水率留空不能按 0% 导致密度 800、体积按 0 安全系数归零 ──
  {
    "slug": "livestock/manure-pit-capacity",
    "inputs": { "count": "300", "dailyManure": "45", "moisture": "150", "cleanCycle": "7", "pitDepth": "2.5", "storageDays": "90", "safetyFactor": "1.2" },
    "expect": ["请输入有效含水率（0~100%）和安全系数（>0）"],
    "ref": "含水率 150% 超出物理上限 ⇒ 旧实现算密度 900 kg/m³ 并照常给池容；安全系数若留空/为 0 还会使储存体积归零。修复后必须拦截。默认含水率 82% 不触发。"
  },
  // ── 去势时机：非法日期不能再输出 NaN 年月日 ─────────────────────
  {
    "slug": "livestock/castration-timing",
    "inputs": { "birthDate": "not-a-date", "animalType": "cattle" },
    "expect": ["请输入有效的出生日期"],
    "ref": "出生日期非法 ⇒ new Date('not-a-date') 为 Invalid Date，旧实现输出 NaN年NaN月NaN日；修复后必须拦截。默认当天日期不触发。"
  },
  // ── 粪量估算：含水率/收集率越界不能静默产出负干物质或 0 收集量 ──
  {
    "slug": "livestock/manure-amount",
    "inputs": { "count": "150", "days": "365", "moisture": "120", "customManure": "0", "collectRate": "90", "animalType": "pig" },
    "expect": ["请输入有效含水率（0~100%）和收集率（0~100]"],
    "ref": "含水率 120% 超出物理上限 ⇒ 旧实现算干物质为负、密度 960；修复后必须拦截。默认 85% 不触发。"
  },
  // ── 断奶成绩：断奶头数不能大于出生头数（成活率 >100%）──────────
  {
    "slug": "livestock/weaning-weight-survival",
    "inputs": { "bornAlive": "18", "weanedAlive": "20", "weanDay": "28", "avgWeight": "7.5", "standardWeight": "6.0", "belowStandard": "2" },
    "expect": ["断奶头数不应大于出生头数，低于标准头数应在0~断奶头数之间"],
    "ref": "断奶 20 > 出生 18 ⇒ 成活率 111.1%，旧实现照常判「优秀」；修复后必须拦截。默认 18/11 不触发。"
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

  console.log("==== livestock calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
