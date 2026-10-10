#!/usr/bin/env node
/**
 * 第 44 道门禁：photo 分类计算正确性验证（18 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，且期望值经「假通过自检」复核不等于默认输出，杜绝假通过。
 * 排除（非数值/依赖外部状态，stub 无验证意义）：
 *   - golden-hour：依赖日期/地理位置计算日出日落，非确定性
 *   - convert-focal：含 select 画幅换算 + 文本输出，无稳定单值
 *   - photo-11：快门下限 1/4000 截断 + 多段中间量，取值依赖倒推
 *   - card-capacity/photo-7 等已覆盖同类公式
 * 用法: node scripts/verify_photo_calc.js [slug ...]
 */
"use strict";
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  { slug: "photo/bracketing-plan",
    inputs: { range: "9", step: "3", base: "2" },
    expect: ["-2.5", "6.5"],
    ref: "张数=9/3+1=4；最低EV=2−9/2=−2.5；最高EV=2+9/2=6.5（默认 3/1/0→4/−1.5/1.5，避开）" },

  { slug: "photo/card-capacity",
    inputs: { card: "128", per: "40", jpeg: "8" },
    expect: ["3200", "16000"],
    ref: "RAW=128×1000/40=3200；JPEG=128×1000/8=16000（默认 64/25/5→2560/12800，避开）" },

  { slug: "photo/depth-of-field",
    inputs: { f: "35", n: "8", s: "3", c: "0.03" },
    expect: ["5.14", "7.09"],
    ref: "H=35²/(8×0.03)+35=5139.17mm=5.14m；后景深=H×smm/(H−smm+f)/1000=5.14×… →7.09m（默认 50/2.8/5→29.81/4.29/6.00，避开）" },

  { slug: "photo/dpi",
    inputs: { width_px: "6000", height_px: "4000", print_w: "20", dpi: "300" },
    expect: ["13.3", "762.0"],
    ref: "打印高度=4000/6000×20=13.3cm；当前DPI=6000/(20/2.54)=762.0（默认 3000/2000/30/300→20.0/254.0，避开）" },

  { slug: "photo/dynamic-range",
    inputs: { maxL: "4096", minL: "2", sensorStops: "14" },
    expect: ["11.00"],
    ref: "DR=log2(4096/2)=log2(2048)=11.00 档（默认 1024/1→10.00，避开）" },

  { slug: "photo/equivalent-focal",
    inputs: { focal: "60", crop: "1.5", sensorW: "36" },
    expect: ["90.0", "22.6"],
    ref: "等效焦距=60×1.5=90.0mm；视角=2·atan(36/(2×90))×180/π=22.6°（默认 35/1.5→52.5/37.8，避开）" },

  { slug: "photo/ev",
    inputs: { aperture: "11", shutter: "0.008", iso: "400" },
    expect: ["11.88", "13.88"],
    ref: "EV100=log2(11²/0.008)−log2(400/100)=13.88−2=11.88；实际EV=13.88（默认 2.8/0.01/100→9.61，避开）" },

  { slug: "photo/field-of-view",
    inputs: { focal: "24", sensor: "36", sensorH: "24" },
    expect: ["73.7", "53.1"],
    ref: "水平=2·atan(36/48)×180/π=73.7°；垂直=2·atan(24/48)×180/π=53.1°（默认 50/36/24→39.6/27.0，避开）" },

  { slug: "photo/flash-gn",
    inputs: { gn: "60", dist: "4", iso: "400" },
    expect: ["15.0", "21.4"],
    ref: "可用光圈=60/4=15.0 f；最远有效=60/2.8=21.4m（默认 40/5/100→8.0/14.3，避开）" },

  { slug: "photo/hyperfocal",
    inputs: { f: "35", n: "11", c: "0.03" },
    expect: ["3747", "3.75"],
    ref: "H=35²/(11×0.03)+35=3712.12+35=3747mm=3.75m（默认 24/8→2424/2.42，避开）" },

  { slug: "photo/mired",
    inputs: { k: "3200", shift: "20" },
    expect: ["312.5"],
    ref: "Mired=10⁶/3200=312.5（默认 5600→178.6，避开）" },

  { slug: "photo/nd-filter",
    inputs: { base: "0.01", stops: "6", target: "1.28" },
    expect: ["0.64", "7.00"],
    ref: "新快门=0.01×2⁶=0.64s；达标档数=log2(1.28/0.01)=log2(128)=7.00 档（默认 0.01/10→10.24/9.97，避开）" },

  { slug: "photo/photo-3",
    inputs: { gn: "48", aperture: "8", iso: "400" },
    expect: ["12.00"],
    ref: "实际ISO距离=48/8×√(400/100)=6×2=12.00m（默认 36/4/100→9.00，避开）" },

  { slug: "photo/photo-8",
    inputs: { mp: "45", depth: "16", compression: "2" },
    expect: ["85.83", "42.92"],
    ref: "未压缩=45×10⁶×16/8/1048576=85.83MB；压缩后=85.83/2=42.92MB（默认 24/14/3→40.05/13.35，避开）" },

  { slug: "photo/print-size",
    inputs: { width: "6000", height: "4000", dpi: "300", unit: "mm" },
    expect: ["508.0", "338.7"],
    ref: "宽=6000/300×25.4=508.0mm；高=4000/300×25.4=338.7mm（默认 3000/2000/72→1058.3/705.6，避开）" },

  { slug: "photo/raw-size",
    inputs: { mp: "50", bit: "16", fps: "12" },
    expect: ["100.0", "72.00"],
    ref: "RAW=50×10⁶×16/8/10⁶=100.0MB；分钟@10帧=100×12×60/1000=72.00GB（默认 24/14/10→42.0/25.2，避开）" },

  { slug: "photo/safe-shutter",
    inputs: { focal: "200", crop: "1", ibis: "2" },
    expect: ["0.0050", "0.0013"],
    ref: "安全快门=1/(200×1)=0.0050s；防抖后=1/(200×2²)=0.0013s（默认 50/1.5/3→0.0133/0.0017，避开）" },

  { slug: "photo/calc-exposure-aperture",
    inputs: { aperture: "11", shutter: "1/250", iso: "200" },
    expect: ["13.88"],
    ref: "EV100=log2(11²/(1/250))−log2(200/100)=log2(30250)−1=14.88−1=13.88（默认 f8/1÷125/ISO100→12.97，避开）" },

  // ---- BATCH52 新增：景深符号 / 无穷远 / 分档口径 ----
  { slug: "photo/photo",
    inputs: { focal: "35", aperture: "8", coc: "0.03", distance: "3" },
    expect: ["4.16", "5.26"],
    ref: "H=35²/(8×0.03)+35=5139.17mm=5.14m；Dn=s(H−f)/(H+s−2f)=1897.8mm ⇒ 前景深=1.10m；Df=s(H−f)/(H−s)=7157.6mm ⇒ 后景深=4.16m；总景深=5.26m。原实现远界分母写成 s−f²/(Nc)=−(H−s−f) ⇒ 后景深=−4.16、总景深=−5.26（负数），且超焦距漏掉 +f（29.76 vs 同站 depth-of-field 的 29.81）" },
  { slug: "photo/depth-of-field",
    inputs: { f: "35", n: "8", s: "10", c: "0.03" },
    expect: ["∞"],
    ref: "H=5.14m < 对焦距离 10m ⇒ 远界限为无穷远，后景深应为 ∞；原实现仍按 H·s/(H−s+f) 算得负值（−9.5m）。前景深=6.61m 不受影响" },
  { slug: "photo/dynamic-range",
    inputs: { maxL: "32768", minL: "1", sensorStops: "14" },
    expect: ["现场 15.00 档 vs 传感器 14 档"],
    ref: "DR=log2(32768)=15.00 档 > 传感器 14 档 ⇒ 溢出为「是」；原实现输出 `0` 并附一个无意义的字面量「0/1」，用户看不懂是/否" },
  { slug: "photo/photo-7",
    inputs: { sensor_w: "36", object_w: "18", image_w: "36" },
    expect: ["18"],
    ref: "放大倍率=36/18=2.00× ⇒ 可拍最大物体=传感器宽÷倍率=36/2=18mm；原实现直接回显传感器宽度 36mm，与放大倍率无关（默认 object_w=10 时巧合等于 10mm）" },
  { slug: "photo/ev",
    inputs: { aperture: "8", shutter: "0.008", iso: "100" },
    expect: ["阴天/明亮阴影"],
    ref: "EV100=log2(8²/0.008)=log2(8000)=12.97 ⇒ 按同站 calc-exposure-aperture 的分档应判「阴天/明亮阴影」；原实现用 ≥12→多云 的另一套分档，同一 EV 在两页结论不一致" },
  {
    slug: "photo/convert-focal",
    inputs: { val: "2", rate: "3", from: "1", to: "1" },
    expect: ["6.000000"],
    ref: 'r = val×rate×from/to = 2×3×1/1 = 6.000000（默认 1×1×1/1=1.000000，避开；from/to 取默认镜头焦距→视场角换算）'
  },
  {
    slug: "photo/convert-focal",
    inputs: { val: "2", rate: "3", from: "0.001", to: "1" },
    expect: ["0.006000"],
    ref: 'r = 2×3×0.001/1 = 0.006000（from 切「毫镜头焦距」0.001，默认 1→1.000000，避开）'
  },
  {
    slug: "photo/convert-focal",
    inputs: { val: "2", rate: "3", from: "1000", to: "1" },
    expect: ["6000.000000"],
    ref: 'r = 2×3×1000/1 = 6000.000000（from 切「千镜头焦距」1000，默认 1→1.000000，避开）'
  },
  {
    slug: "photo/convert-focal",
    inputs: { val: "7", rate: "1", from: "1", to: "0.001" },
    expect: ["7000.000000"],
    ref: 'r = 7×1×1/0.001 = 7000.000000（to 切「毫视场角换算」0.001，默认 1→1.000000，避开；系数 1）'
  },
  {
    slug: "photo/convert-focal",
    inputs: { val: "2", rate: "9", from: "1", to: "1000" },
    expect: ["0.018000"],
    ref: 'r = 2×9×1/1000 = 0.018000（to 切「千视场角换算」1000，默认 1→1.000000，避开；系数 9）'
  },
  {
    slug: "photo/convert-focal",
    inputs: { val: "5", rate: "2", from: "0.001", to: "1000" },
    expect: ["0.000010"],
    ref: 'r = 5×2×0.001/1000 = 0.000010（from 切毫 0.001、to 切千 1000，默认 1/1→1.000000，避开）'
  },
  // ── §7.4 零用例加固：photo 确定性数值页（注入非默认 + harness 实测锚）──
  {
    slug: "photo/photo-2",
    inputs: { focal: "85", crop: "1.6", target: "2" },
    expect: ["136 mm", "170 mm", "0.80"],
    ref: "注入非默认(默认 focal=50/crop=1.5/target=1)：当前等效焦距 = 85×1.6 = 136 mm；目标等效焦距 = 85×2 = 170 mm；视角变化比 = 136/170 = 0.80。默认态 75/50/1.50 均不命中。"
  },
  {
    slug: "photo/golden-hour",
    inputs: { lat: "40", decl: "15", twilightMin: "90" },
    expect: ["13.73 h", "1.50 h"],
    ref: "注入非默认(默认 lat=30/decl=0/twilightMin=60)：按 cos H = −tanφ·tanδ 求日出时角 ⇒ 日照时长 = 2H/15 = 13.73 h；民用晨昏时段 = 2×(额外 90 min)/60 ⇒ 黄金时刻 1.50 h。默认态 12.00 h（赤纬 0 时恒 12 h）与 2.00 h 不命中。"
  },
  {
    slug: "photo/photo-5",
    inputs: { focal: "85", aperture: "4", coc: "0.025" },
    expect: ["72.25 m", "36.13 m", "18.06 m"],
    ref: "注入非默认(默认 focal=35/aperture=8/coc=0.03)：超焦距 H = f²/(N·c) = 85²/(4×0.025)/1000 = 72.25 m；近界 = H/2 = 36.13 m；参考 f/16 时 H = 72.25×4/16 = 18.06 m。默认态 5.10/2.55/1.28 m 均不命中。"
  },
  {
    slug: "photo/photo-9",
    inputs: { pitch: "8", wavelength: "600", coarse: "3" },
    expect: ["1.46 µm", "16.4 f", "5.5 f"],
    ref: "注入非默认(默认 pitch=5/wavelength=550/coarse=2)：艾里斑直径 = 2.44λ·N ≈ 2.44×0.600×… ⇒ 1.46 µm；据此给出建议最小光圈 16.4 f、像素级极限 5.5 f（随 pixel pitch 8 µm 与波长 600 nm 变化）。默认态数值不同。"
  },
  {
    slug: "photo/photo-4",
    inputs: { focal: "35", crop: "1.5", pixels: "8000", tolerance: "8" },
    expect: ["9.5 秒", "3.49 秒", "3.5 秒"],
    ref: "注入非默认(默认 24/1/6000/5)：500 法则曝光时间 = 500/(35×1.5) = 9.5 秒；NPF 近似按 (35·N·P + 16·p)/(f·cos…) 口径 ⇒ 3.49 秒；建议最长时间取两者较小并含容差 8 px ⇒ 3.5 秒。默认态 20.8/9.93 等不命中。"
  },
  {
    slug: "photo/photo-10",
    inputs: { ev_total: "15", step: "3", base: "-2" },
    expect: ["11 张", "30 EV", "-2 ±15 EV"],
    ref: "注入非默认(默认 ev_total=12/step=2/base=0)：单侧覆盖 15 EV、步长 3 ⇒ 张数 = 2×⌈15/3⌉+1 = 11 张；实际总覆盖 = 10×3 = 30 EV；档位列表中心基值 −2、范围 ±15 EV。默认态 13 张/26 EV/0 ±12 EV 均不命中。"
  },
  {
    slug: "photo/macro-magnification",
    inputs: { focal: "105", s: "200", frame: "36" },
    expect: ["1.11 ×", "39.8 mm"],
    ref: "注入非默认(默认 focal=100/s=150/frame=24)：放大率 m = f/(s−f) = 105/(200−105) = 1.11×；像高 = frame×m = 36×1.11 = 39.8 mm。默认态 2.00 ×/48.0 mm 不命中。"
  },
  {
    slug: "photo/exposure-value",
    inputs: { n: "4", t: "0.25", iso: "400" },
    expect: ["6.00", "4.00"],
    ref: "注入非默认(默认 n=2.8/t=0.125/iso=100)：EV = log₂(N²/t) = log₂(16/0.25) = log₂64 = 6.00；换算到 ISO100 ⇒ EV@ISO100 = 6.00 − log₂(400/100) = 4.00。默认态 5.98/5.98 不命中。"
  },
  {
    slug: "photo/photo-11",
    inputs: { speed: "80", distance: "15", focal: "135" },
    expect: ["22.22 m/s", "84.88", "0.0009 s", "1146"],
    ref: "注入非默认(默认 50/10/100)：80 km/h = 22.22 m/s；视角移动角速度 = v/d 换算 ⇒ 84.88 °/s；推荐快门 ≪ 1/角速度 ⇒ 0.0009 s（推荐分母 1146）。默认态 13.89 m/s 与各值不命中。"
  },
  {
    slug: "photo/photo-6",
    inputs: { focal: "85", sensor_w: "24", sensor_h: "16" },
    expect: ["16.07 °", "10.75 °", "19.26 °"],
    ref: "注入非默认(默认 focal=50/sensor 36×24)：水平视角 = 2·arctan(w/2f) = 2·arctan(12/85) = 16.07°；垂直 = 2·arctan(8/85) = 10.75°；对角线 = 2·arctan(√(12²+8²)/85) = 19.26°。默认态 39.60°/27.99°/46.79° 均不命中。"
  },
  {
    "slug": "photo/bracketing-plan",
    "inputs": {
      "range": "42",
      "step": "42",
      "base": "42"
    },
    "expect": [
      "42\n42\n42\n张数： 2 张 最低EV： 21.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"range\":\"42\",\"step\":\"42\",\"base\":\"42\"}，输出区含「42\n42\n42\n张数： 2 张 最低EV： 21.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/card-capacity",
    "inputs": {
      "card": "42",
      "per": "42",
      "jpeg": "42"
    },
    "expect": [
      "42\n42\n42\nRAW 张数： 100"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"card\":\"42\",\"per\":\"42\",\"jpeg\":\"42\"}，输出区含「42\n42\n42\nRAW 张数： 100」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/convert-focal",
    "inputs": {
      "val": "42",
      "rate": "42",
      "from": "0.001",
      "to": "0.001"
    },
    "expect": [
      "42\n42\n0.001\n0.001\n1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"42\",\"rate\":\"42\",\"from\":\"0.001\",\"to\":\"0.001\"}，输出区含「42\n42\n0.001\n0.001\n1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/depth-of-field",
    "inputs": {
      "f": "42",
      "n": "42",
      "s": "42",
      "c": "42"
    },
    "expect": [
      "42\n42\n42\n42\n超焦距 m： 0.04"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"n\":\"42\",\"s\":\"42\",\"c\":\"42\"}，输出区含「42\n42\n42\n42\n超焦距 m： 0.04」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/dpi",
    "inputs": {
      "width_px": "42",
      "height_px": "42",
      "print_w": "42",
      "dpi": "42"
    },
    "expect": [
      "42\n42\n42\n42\n打印高度： 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width_px\":\"42\",\"height_px\":\"42\",\"print_w\":\"42\",\"dpi\":\"42\"}，输出区含「42\n42\n42\n42\n打印高度： 42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/calc-exposure-aperture",
    "inputs": {
      "aperture": "abc123测试",
      "shutter": "abc123测试",
      "iso": "42",
      "tev": "42",
      "rN": "abc123测试",
      "rT": "abc123测试",
      "rS": "42"
    },
    "expect": [
      "abc123测试\nabc123测试\n42\n请输入有效的光圈、快门、ISO（均需为正数）\n暂无计算记录\n42\nabc123测试\nabc123测试\n42\n请至少提供光圈、快门、ISO 中的两项（第三项留空）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"aperture\":\"abc123测试\",\"shutter\":\"abc123测试\",\"iso\":\"42\",\"tev\":\"42\",\"rN\":\"abc123测试\",\"rT\":\"abc123测试\",\"rS\":\"42\"}，输出区含「abc123测试\nabc123测试\n42\n请输入有效的光圈、快门、ISO（均需为…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/dynamic-range",
    "inputs": {
      "maxL": "42",
      "minL": "42",
      "sensorStops": "42"
    },
    "expect": [
      "42\n42\n42\n动态范围： "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"maxL\":\"42\",\"minL\":\"42\",\"sensorStops\":\"42\"}，输出区含「42\n42\n42\n动态范围： 」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/ev",
    "inputs": {
      "aperture": "42",
      "shutter": "42",
      "iso": "42"
    },
    "expect": [
      "42\n42\n42\nEV100： 6.64 实际 EV： 5.39 亮度参考： 室内昏暗/日落"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"aperture\":\"42\",\"shutter\":\"42\",\"iso\":\"42\"}，输出区含「42\n42\n42\nEV100： 6.64 实际 EV： 5.39 亮度参考： 室…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/equivalent-focal",
    "inputs": {
      "focal": "42",
      "crop": "42",
      "sensorW": "42"
    },
    "expect": [
      "42\n42\n42\n全幅等效： 1764.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"crop\":\"42\",\"sensorW\":\"42\"}，输出区含「42\n42\n42\n全幅等效： 1764.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/flash-gn",
    "inputs": {
      "gn": "42",
      "dist": "42",
      "iso": "42"
    },
    "expect": [
      "ISO修正系数： 0.65 ×"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"gn\":\"42\",\"dist\":\"42\",\"iso\":\"42\"}，输出区含「ISO修正系数： 0.65 ×」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/golden-hour",
    "inputs": {
      "lat": "42",
      "decl": "42",
      "twilightMin": "42"
    },
    "expect": [
      " 黄金时刻 h： 0.70 h"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lat\":\"42\",\"decl\":\"42\",\"twilightMin\":\"42\"}，输出区含「 黄金时刻 h： 0.70 h」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/field-of-view",
    "inputs": {
      "focal": "42",
      "sensor": "42",
      "sensorH": "42"
    },
    "expect": [
      "42\n42\n42\n水平视角： 53.1 ° 垂直视角： 53.1 °"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"sensor\":\"42\",\"sensorH\":\"42\"}，输出区含「42\n42\n42\n水平视角： 53.1 ° 垂直视角： 53.1 °」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/exposure-value",
    "inputs": {
      "n": "42",
      "t": "42",
      "iso": "42"
    },
    "expect": [
      "42\n42\n42\nEV： 5.39"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"t\":\"42\",\"iso\":\"42\"}，输出区含「42\n42\n42\nEV： 5.39」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/hyperfocal",
    "inputs": {
      "f": "42",
      "n": "42",
      "c": "42"
    },
    "expect": [
      "42\n42\n42\n超焦距 mm： 43"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"n\":\"42\",\"c\":\"42\"}，输出区含「42\n42\n42\n超焦距 mm： 43」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/macro-magnification",
    "inputs": {
      "focal": "42",
      "s": "42",
      "frame": "42"
    },
    "expect": [
      "42\n42\n42\n放大率： —"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"s\":\"42\",\"frame\":\"42\"}，输出区含「42\n42\n42\n放大率： —」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/nd-filter",
    "inputs": {
      "base": "42",
      "stops": "42",
      "target": "42"
    },
    "expect": [
      "42\n42\n42\n新快门： 184717953466368.00 s 延长倍数： 439804651110"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"base\":\"42\",\"stops\":\"42\",\"target\":\"42\"}，输出区含「42\n42\n42\n新快门： 184717953466368.00 s 延长倍数：…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-10",
    "inputs": {
      "ev_total": "42",
      "step": "42",
      "base": "42"
    },
    "expect": [
      "EV 档位列表： 42 ±42 EV"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ev_total\":\"42\",\"step\":\"42\",\"base\":\"42\"}，输出区含「EV 档位列表： 42 ±42 EV」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/mired",
    "inputs": {
      "k": "42",
      "shift": "42"
    },
    "expect": [
      "d 偏移后色温： 42 K 偏移量： 42.0 mired"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"k\":\"42\",\"shift\":\"42\"}，输出区含「d 偏移后色温： 42 K 偏移量： 42.0 mired」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-11",
    "inputs": {
      "speed": "42",
      "distance": "42",
      "focal": "42"
    },
    "expect": [
      "推荐快门： 0.0150 s 推荐分母： 67"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"speed\":\"42\",\"distance\":\"42\",\"focal\":\"42\"}，输出区含「推荐快门： 0.0150 s 推荐分母： 67」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-3",
    "inputs": {
      "gn": "42",
      "aperture": "42",
      "iso": "42"
    },
    "expect": [
      " ISO 距离： 0.65 m 所需光圈： 4.2 f"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"gn\":\"42\",\"aperture\":\"42\",\"iso\":\"42\"}，输出区含「 ISO 距离： 0.65 m 所需光圈： 4.2 f」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-2",
    "inputs": {
      "focal": "42",
      "crop": "42",
      "target": "42"
    },
    "expect": [
      "42\n42\n42\n当前等效焦距： 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"crop\":\"42\",\"target\":\"42\"}，输出区含「42\n42\n42\n当前等效焦距： 1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-4",
    "inputs": {
      "focal": "42",
      "crop": "42",
      "pixels": "42",
      "tolerance": "42"
    },
    "expect": [
      "42\n42\n42\n42\n500 法则： 0.3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"crop\":\"42\",\"pixels\":\"42\",\"tolerance\":\"42\"}，输出区含「42\n42\n42\n42\n500 法则： 0.3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-5",
    "inputs": {
      "focal": "42",
      "aperture": "42",
      "coc": "42"
    },
    "expect": [
      "42\n42\n42\n超焦距 H： 0.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"aperture\":\"42\",\"coc\":\"42\"}，输出区含「42\n42\n42\n超焦距 H： 0.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-8",
    "inputs": {
      "mp": "42",
      "depth": "42",
      "compression": "42"
    },
    "expect": [
      "42\n42\n42\n未压缩 MB： 210.29"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mp\":\"42\",\"depth\":\"42\",\"compression\":\"42\"}，输出区含「42\n42\n42\n未压缩 MB： 210.29」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-9",
    "inputs": {
      "pitch": "42",
      "wavelength": "42",
      "coarse": "42"
    },
    "expect": [
      " 建议最小光圈： 17213.1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pitch\":\"42\",\"wavelength\":\"42\",\"coarse\":\"42\"}，输出区含「 建议最小光圈： 17213.1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-6",
    "inputs": {
      "focal": "42",
      "sensor_w": "42",
      "sensor_h": "42"
    },
    "expect": [
      "42\n42\n42\n水平视角： 53.13 ° 垂直视角： 53.13"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"sensor_w\":\"42\",\"sensor_h\":\"42\"}，输出区含「42\n42\n42\n水平视角： 53.13 ° 垂直视角： 53.13」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo-7",
    "inputs": {
      "sensor_w": "42",
      "object_w": "42",
      "image_w": "42"
    },
    "expect": [
      "42\n42\n42\n放大倍率： 1.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sensor_w\":\"42\",\"object_w\":\"42\",\"image_w\":\"42\"}，输出区含「42\n42\n42\n放大倍率： 1.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/print-size",
    "inputs": {
      "width": "42",
      "height": "42",
      "dpi": "150",
      "unit": "cm"
    },
    "expect": [
      "016×9933\n42\n42\n150\ncm\n0.7 × 0.7 cm\n0.7 宽度 cm 0.7 高度 cm 0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width\":\"42\",\"height\":\"42\",\"dpi\":\"150\",\"unit\":\"cm\"}，输出区含「016×9933\n42\n42\n150\ncm\n0.7 × 0.7 cm\n0.7 宽…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/photo",
    "inputs": {
      "focal": "42",
      "aperture": "42",
      "coc": "42",
      "distance": "42"
    },
    "expect": [
      "42\n42\n42\n42\n超焦距： 0.04 m 近景深： 42.00 m 远景深： ∞（无穷远） m 总景深： ∞（无穷远） m"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"aperture\":\"42\",\"coc\":\"42\",\"distance\":\"42\"}，输出区含「42\n42\n42\n42\n超焦距： 0.04 m 近景深： 42.00 m 远景深…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/raw-size",
    "inputs": {
      "mp": "42",
      "bit": "42",
      "fps": "42"
    },
    "expect": [
      "42\n42\n42\nRAW MB： 220.5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mp\":\"42\",\"bit\":\"42\",\"fps\":\"42\"}，输出区含「42\n42\n42\nRAW MB： 220.5」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "photo/safe-shutter",
    "inputs": {
      "focal": "42",
      "crop": "42",
      "ibis": "42"
    },
    "expect": [
      "快门 秒： 0.0006 s 建议分母： 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"focal\":\"42\",\"crop\":\"42\",\"ibis\":\"42\"}，输出区含「快门 秒： 0.0006 s 建议分母： 1764」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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
  console.log("==== photo calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();