#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pet/aquarium-light",
  "inputs": {},
  "clicks": [
    "selectLevel('medium');"
  ],
  "expect": [
    "适中光照，最常见水草 · 共 5 种水草"
  ],
  "ref": "clicks 注入：selectLevel('medium') 改写 currentLevel（页面初始为 'all'），renderLevelInfo 产出中光档专属正文（等级名 · 光照区间 · 档位描述 · 该档水草数），plantList 同步收敛为 5 种中光水草。旧锚「0.3-0.5」取自静态 levelGrid 卡片（默认态即渲染含该串的三档卡片）⇒ 判别力 0、原 ref 已定性为逃生项。注意本页零参 showAll() 会在兜底遍历中把 currentLevel 复位为 'all'，故只能锚 clicks 阶段的输出；清 clicks 后重跑停在「显示全部 16 种水草」⇒ 零逃生项。"
},
{
  "slug": "audio/audio-sample-rate",
  "inputs": {
    "duration": "90"
  },
  "expect": ["8 kHz 电话 语音通话，频响至4kHz 16 kHz 语音 语音识别，频响至8kHz 22.05 kHz 低质量 网络音频，频响至11kHz 44.1 kHz CD音质 音乐标准，频响至20kHz 48 kHz 专业 影视标准，频响至24kHz 96 kHz 高清 专业录音，频响至48kHz 192 kHz 录音棚 母带制作，频响至96kHz\n44100\n48000\n16\n2\n90\n44.1 kHz → 48 kHz\n升采样：不会恢复已丢失的高频信息，仅插值处理\n1411 源比特率(kbps) 1536 目标比特率(kbps) 15.14 源文件(MB) 16.48 目标文件(MB) 22.1 源频响(kHz) 24.0 目标频响(kHz)"],
  "ref": "auto-restore"
},
{
  "slug": "life/candle-burn-time",
  "inputs": {
    "weight": "300",
    "diameter": "70"
  },
  "expect": [
    "36小时26分钟"
  ],
  "ref": "auto-restore"
},
{
  "slug": "ceramics/ceramic-firing",
  "inputs": {
    "fireType": "glaze"
  },
  "expect": [
    "过石英转变点573°C"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/convert-fps",
  "inputs": {
    "val": "45",
    "fps": "30"
  },
  "expect": [
    "1.50"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/convert-sample",
  "inputs": {
    "val": "66150",
    "sr": "44.1"
  },
  "expect": [
    "66150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beekeeping/honey-estimator",
  "inputs": {
    "hives": "15",
    "area": "50"
  },
  "expect": ["🌼 油菜花 春季主要蜜源，分布广 基准 45kg/群 🌳 椴树 东北优质蜜源，产量高 基准 60kg/群 🍒 荔枝 华南重要蜜源，品质好 基准 50kg/群 🌸 槐树（洋槐） 初夏蜜源，蜜质清亮 基准 40kg/群 🌻 向日葵 夏季蜜源，适应性强 基准 38kg/群 🌺 混合花源 多种花源交替，最常见 基准 35kg/群 🥭 龙眼 华南优质蜜源 基准 48kg/群 🍎 枣花 夏季蜜源，蜜质浓稠 基准 42kg/群\n15\n50\n1.0\n1.0\n437.5 kg\n预估年度产蜜量（约875斤）· 花源偏少，建议扩大蜜源或减少蜂群\n29.2 单群产蜜(kg) 875 总产量(斤) ¥17500 预估收入(40元/kg) 60 建议花源(亩)"],
  "ref": "auto-restore"
},
{
  "slug": "gardening/lawn-mowing",
  "inputs": {
    "season": "summer"
  },
  "expect": [
    "6cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "niche/photography-exposure",
  "inputs": {
    "aperture": "1.8"
  },
  "expect": [
    "1/15s"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/pruning-calendar",
  "inputs": {
    "searchInput": "zzzqx"
  },
  "expect": [
    "未找到匹配的植物"
  ],
  "ref": "关键词过滤型：inputs 写 searchInput=zzzqx ⇒ oninput=filterPlants() ⇒ renderPlants() 得空集 ⇒ 「未找到匹配的植物」。默认态渲染当季 16 种植物全量、blob 无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "niche/recommender-temp-pottery",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "niche/succulent-watering",
  "inputs": {
    "season": "summer"
  },
  "expect": [
    "每20天"
  ],
  "ref": "auto-restore"
},
{
  "slug": "video/video-fps",
  "inputs": {
    "duration": "15"
  },
  "expect": [
    "1800"
  ],
  "ref": "auto-restore"
},
  {
    "slug": "gardening/reminder-cycle-succulent",
    "inputs": {
      "plantName": "abc123测试",
      "plantLastWater": "abc123测试"
    },
    "expect": [
      "无植物，请先添加\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"plantName\":\"abc123测试\",\"plantLastWater\":\"abc123测试\"}，输出区含「无植物，请先添加\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
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

  console.log("==== niche calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
