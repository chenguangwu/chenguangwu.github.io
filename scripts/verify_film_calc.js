#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "film/aspect-ratio",
  "inputs": {
    "width": "1920",
    "height": "1080",
    "srcWidth": "1920",
    "srcHeight": "1080",
    "ratio": "2.35"
  },
  "expect": [ "2,741,040 px" ],
  "ref": "auto-restore"
},
{
  "slug": "film/color-grading",
  "inputs": {},
  "expect": [
    "2000-50000K"
  ],
  "ref": "结构性不可注入（2026-09-26 复核，原 ref 为 auto-restore(default) 未评估项）：页面有 `#searchInput` / `#filterSelect` 与顶层 `filterData()`，但 filterData 的唯一副作用是 `tr.style.display = '' | 'none'` —— harness 的 collectStrings 只采 DOM 的 `value`/`innerHTML`/`textContent`，**不采 style**，且 textContent 对隐藏行同样返回文本 ⇒ 任何过滤态与默认态采集结果完全相同。改用 `tr.remove()` 能让行消失，但那是 harness 侧删 DOM、不测页面筛选逻辑（折扣注入）⇒ 维持 no_inputs，断言初始化渲染串。"
},
{
  "slug": "film/convert-time-1",
  "inputs": {
    "h": "7",
    "m": "0",
    "s": "10",
    "f": "0",
    "fps": "25"
  },
  "expect": [
    "25210.000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/editing-timecode",
  "inputs": {
    "tcInput": "01:23:45:12",
    "totalFrames": "181251"
  },
  "expect": [
    "7552.125"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/render-time",
  "inputs": {
    "totalFrames": "6480",
    "frameTime": "8",
    "nodes": "4",
    "fps": "24",
    "hoursPerDay": "24",
    "retryRate": "5"
  },
  "expect": [
    "54432"
  ],
  "ref": "auto-restore"
},
{
  "slug": "film/vfx-shot",
  "inputs": {
    "shotCount": "180",
    "shotDuration": "5",
    "hoursPerShot": "40",
    "teamSize": "8",
    "dailyRate": "1500"
  },
  "expect": ["等级 系数 每镜头工时(h) 典型内容 简单 1.0 10-30 擦除威亚、贴片、简单合成 中等 1.5 30-60 绿幕合成、天空替换、简单CG 复杂 2.8 60-120 CG生物、场景延伸、粒子效果 高难 5.0 120-240 流体模拟、破坏效果、群集动画 极难 8.0 240-480 全CG镜头、角色面部动画、物理模拟\n180\n5\n2\n40\n8\n1500\n复杂度： 中等（×1.5） 调整后每镜头工时： 60.0 h 总工时： 10800 h 项目总工期： 168.8 工作日 （约 7.7 个月） 特效总时长： 15.0 分钟 （180镜头 × 5s） 总人工成本： ¥16,200,000 每镜头成本： ¥90,000 每秒成本： ¥18,000 评估： 大型项目（6个月内）"],
  "ref": "auto-restore"
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

  console.log("==== film calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
