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
  "expect": [
    "44.1 kHz → 48 kHz",
    "1411源比特率(kbps)",
    "1536目标比特率(kbps)",
    "15.14源 PCM 数据量(MiB)",
    "16.48目标 PCM 数据量(MiB)",
    "升采样：不会恢复已丢失的高频信息，仅插值处理"
  ],
  "ref": "第1062批：修正旧断言仍写「频响至4kHz」/「源文件(MB)」与现行文案「理论上限4kHz」/「源 PCM 数据量(MiB)」不一致；90 秒时源/目标数据量 15.14/16.48 MiB，默认 60 秒为 10.09/10.99 ⇒ 非回显。"
,
  "ref": "auto-restore"
},
{
  "slug": "ceramics/ceramic-firing",
  "inputs": {
    "fireType": "glaze"
  },
  "expect": [
    "573→600°C",
    "跨过 573℃ 石英晶型转变点"
  ],
  "ref": "auto-restore"
},
{
  "slug": "beekeeping/honey-estimator",
  "inputs": {
    "hives": "15",
    "area": "50"
  },
  "expect": ["437.5 kg", "875 总产量(斤)", "29.2 单群产蜜(kg)", "建议花源(亩)"],
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
