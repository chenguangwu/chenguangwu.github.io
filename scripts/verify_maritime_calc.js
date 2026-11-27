#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "maritime/anchorage-capacity", inputs: {"shipLength":"250","waterDepth":"25","scopeFactor":"6","safetyMargin":"60","anchorageArea":"8","layoutMode":"grid"}, expect: ["150.0 出链长度 (m)","846,400 单船面积 (m²)","9 可容船舶数"], ref: "出链 25×6 = 150.0 m、旋回 150+250+60 = 460.0 m；方格排布 920² = 846,400 m²/船 ⇒ floor(8,000,000/846,400) = 9 艘（默认 200/20/5/50/5 圆形 ⇒ 100.0/350.0/384,845/12 艘）；layoutMode=grid 必须显式注入（harness 取首个 option=circle）" },
  { slug: "maritime/compass-correction", inputs: {"variation":"8","deviation":"-2","convertDir":"t2c","headingInput":"100"}, expect: ["094.0° 罗航向 CH","092.0° 磁航向 MH","6.0°E 罗经差"], ref: "t2c：TH 100 → MH = 100−8 = 92 → CH = 92−(−2) = 94；罗经差 Dev+Var = −2+8 = 6.0°E（默认 c2t/45/-5/3 ⇒ CH 045.0°、CH 43.0°、2.0°W）；convertDir=t2c 必须显式注入（harness 取首个 option=c2t）" },
  { slug: "maritime/speed-distance", inputs: {"calcTarget":"time","speedValue":"18","distValue":"450"}, expect: ["25.00 时间 (小时)","450.00 航程 (海里)","1天 1小时"], ref: "目标=航行时间：450 nm ÷ 18 kn = 25.00 h、易读 1天 1小时（默认 目标=航程 15×12 = 180.00 nm）；calcTarget=time 必须显式注入（harness 取首个 option=distance）" },
  { slug: "maritime/stowage-factor", inputs: {"calcMode":"capacity","sfInput":"0.8","totalWeight":"6000","holdCapacity":"9000","dwt":"7000"}, expect: ["4,800 所需舱容 (m³)","53.3% 舱容利用率","7,000 最大装载 (吨)"], ref: "capacity 模式：所需舱容 6000×0.8 = 4,800 m³、舱容利用率 4800/9000 = 53.3%、载重利用率 6000/7000 = 85.7%；舱容上限 9000/0.8 = 11,250 t > DWT 7,000 t ⇒ 载重受限，最大装载 7,000 t（默认 sf 模式 ⇒ 1.667 m³/t/59.80/0.600，完全不同分支）；calcMode=capacity 必须显式注入（harness 取首个 option=sf）。**注**：本页 onCargoChange() 与 compass 类无参联动函数同名同型，兜底阶段会把 volume/weight/sfInput 覆盖回 custom 预设（100/60/1.5）⇒ 最终 dump 显示 1.5，但 expect 在注入阶段判定（via=input event）" },
  { slug: "maritime/tide-window", inputs: {"draft":"6.0","ukc":"0.8","chartDepth":"4.0"}, expect: ["2.80 所需潮高 (m)","1.70 潮高余量 (m)"], ref: "所需潮高 = 吃水 6.0 + UKC 0.8 − 海图水深 4.0 = 2.80 m、潮高余量 = 高潮 4.50 − 2.80 = 1.70 m（默认 5.0/0.5/3.0 ⇒ 2.50 m、2.00 m）；时间用页面默认值（14:20/08:05/20:15，type=time 可注入但无需改）" },
  {
    "slug": "maritime/anchorage-capacity",
    "inputs": {
      "shipLength": "42",
      "waterDepth": "42",
      "scopeFactor": "42",
      "safetyMargin": "42",
      "anchorageArea": "42",
      "layoutMode": "grid"
    },
    "expect": [
      "径） 布锚方式： 方格固定泊位 单船占用面积： 13,660,416 m²（13.660416"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"shipLength\":\"42\",\"waterDepth\":\"42\",\"scopeFactor\":\"42\",\"safetyMargin\":\"42\",\"anchorageArea\":\"42\",\"layoutMode\":\"grid\"}，输出区含「径） 布锚方式： 方格固定泊位 单船占用面积： 13,660,416 m²（1,…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "maritime/compass-correction",
    "inputs": {
      "variation": "42",
      "deviation": "42",
      "headingInput": "42",
      "convertDir": "t2c"
    },
    "expect": [
      "318.0° 罗航向 CH"
    ],
  },
  {
    "slug": "maritime/stowage-factor",
    "inputs": {
      "volume": "42",
      "weight": "42",
      "sfInput": "42",
      "totalWeight": "42",
      "holdCapacity": "42",
      "dwt": "42",
      "cargoType": "grain",
      "calcMode": "capacity"
    },
    "expect": [
      "capacity\n1.4\n42\n42\n42\n0\n59 所需舱容 (m³) 140.0% 舱容利用率 100.0% 载重利用率 30 最大装载 (吨) 积载因数： 1.400 m³/t 总货量： 42 吨 所需舱容： 59 m³（42 × 1.4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"volume\":\"42\",\"weight\":\"42\",\"sfInput\":\"42\",\"totalWeight\":\"42\",\"holdCapacity\":\"42\",\"dwt\":\"42\",\"cargoType\":\"grain\",\"calcMode\":\"capacity\"}，输出区含「capacity\n1.4\n42\n42\n42\n0\n59 所需舱容 (m³) 140.0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "maritime/speed-distance",
    "inputs": {
      "speedValue": "42",
      "timeValue": "42",
      "distValue": "42",
      "calcTarget": "time",
      "speedUnit": "kmh",
      "timeUnit": "day",
      "distUnit": "km"
    },
    "expect": [
      "里) 计算目标：航行时间 航速多单位 22.678 节 = 42.000 km/h = 11.66"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"speedValue\":\"42\",\"timeValue\":\"42\",\"distValue\":\"42\",\"calcTarget\":\"time\",\"speedUnit\":\"kmh\",\"timeUnit\":\"day\",\"distUnit\":\"km\"}，输出区含「里) 计算目标：航行时间 航速多单位 22.678 节 = 42.000 km/…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "maritime/tide-window",
    "inputs": {
      "highTideTime": "abc123测试",
      "highTideHeight": "42",
      "lowTideTime": "abc123测试",
      "lowTideHeight": "42",
      "nextLowTideTime": "abc123测试",
      "nextLowTideHeight": "42",
      "chartDepth": "42",
      "draft": "42",
      "ukc": "42",
      "transitTime": "42"
    },
    "expect": [
      "abc123测试\n42\nabc123测试\n42\nabc123测试\n42\n42\n42\n42\n42\n本轮潮汐潮高不足，无法通航 通航状态 42.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"highTideTime\":\"abc123测试\",\"highTideHeight\":\"42\",\"lowTideTime\":\"abc123测试\",\"lowTideHeight\":\"42\",\"nextLowTideTime\":\"abc123测试\",\"nextLowTideHeight\":\"42\",\"chartDepth\":\"42\",\"draft\":\"42\",\"ukc\":\"42\",\"transitTime\":\"42\"}，输出区含「abc123测试\n42\nabc123测试\n42\nabc123测试\n42\n42\n4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  { slug: "maritime/speed-distance", inputs: { calcTarget: "distance", speedValue: "", timeValue: "" }, expect: ["航速未填写；时间未填写。请补全后再计算航程。"], ref: "空态守卫：目标=航程且航速/时间清空时不再输出 0.00 海里与 0 小时，只给填写提示（旧实现 ⇒ 0.00/0.000/0.0 三单位全 0）。默认态 12 kn × 15 h ⇒ 180.00 nm，提示串不出现。" },
{
  "slug": "maritime/compass-correction",
  "inputs": { "variation": "", "deviation": "3", "headingInput": "45", "convertDir": "c2t" },
  "expect": ["请填写磁差、自差与航向后再换算。"],
  "ref": "空态守卫（2026-11-05）：清空磁差后不再输出「000.0° 罗航向 / 磁差 0.0°E / 罗经差 3.0°E」三向换算结果，只给填写提示。⚠ 判空只认空串——磁差 0°、自差 0°、航向 000°（正北）均为合法值，照常换算。"
},
{
  "slug": "maritime/tide-window",
  "inputs": {
    "highTideTime": "05:00",
    "highTideHeight": "4.0",
    "lowTideTime": "23:00",
    "lowTideHeight": "1.0",
    "nextLowTideTime": "11:00",
    "nextLowTideHeight": "1.0",
    "chartDepth": "3.0",
    "draft": "5.0",
    "ukc": "0.5",
    "transitTime": "60"
  },
  "expect": [
    "02:00（+1天） - 08:01（+1天）",
    "推荐通航开始：04:31（+1天），推荐完成：05:31（+1天）"
  ],
  "ref": "跨午夜区间展开（2026-11-16）：低潮 23:00（前一日）→ 高潮 05:00 → 次日低潮 11:00，所需潮高 5.0+0.5−3.0=2.5 m，余弦模型在 ±180 min 内 ≥2.5，页面按分钟逐点采样且含两端 ⇒ 02:00–08:01 共 361 个可通航分钟点、最晚出港 07:31。旧实现直接沿用 05:00=300 的绝对分钟，搜索区间变成 1320→720 导致循环空转，误报「本轮潮汐潮高不足，无法通航」⇒ 两条锚全失配。旧 ref 写 360 分钟是区间长度口径，与页面 inclusive 采样口径不一致，已按实测输出校正。判别器实测固定结论串「可乘潮通航」在默认快照也命中，已删，仅留依赖注入时刻的窗口与进出港时间串。"
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

  console.log("==== maritime calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();