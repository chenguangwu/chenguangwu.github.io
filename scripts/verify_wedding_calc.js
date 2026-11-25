#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "wedding/countdown-timeline",
  "inputs": {
    "weddingTime": "10:00_X"
  },
  "expect": [
    "00_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/detector-2",
  "inputs": {
    "c1": "#e8638f_X",
    "c2": "#7c3aed"
  },
  "expect": [
    "e8638f_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/detector-33",
  "inputs": {
    "prof": "12",
    "punctual": "9",
    "creative": "7",
    "comm": "8",
    "contract": "95"
  },
  "expect": [
    "12/10(30%)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/material-checklist",
  "clicks": ["CATEGORIES=[{name:'婚宴用品',items:[{name:'喜糖礼盒',qty:30,price:18,status:'done'},{name:'定制喜帖',qty:200,price:3,status:'pending'}]},{name:'现场布置',items:[{name:'主舞台背景',qty:1,price:2800,status:'ordered'}]}];calc()"],
  "expect": [
    "¥3,940 总预算",
    "33% 完成",
    "婚宴用品 ¥1,140",
    "现场布置 ¥2,800"
  ],
  "ref": "顶层数组 CATEGORIES 注入：婚宴用品 30×18 + 200×3 = ¥1,140、现场布置 1×2800 = ¥2,800 ⇒ 总预算 ¥3,940、共 3 项物料、已到货 1 项 ⇒ 进度 1/3 = 33%。默认态 loadDefault 为 ¥50,200 / 23 项 / 30%；「3 总物料数」会被默认态「23 总物料数」作为子串命中 ⇒ 改锚两个分类合计。"
},
{
  "slug": "wedding/seating-chart",
  "inputs": {
    "perTable": "15",
    "mainTable": "8"
  },
  "expect": [
    "15人"
  ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/wedding-budget-planner",
  "inputs": {
    "totalBudget": "150000",
    "spent": "0",
    "cat-'+i+'": "'+amount+'"
  },
  "expect": [ "150,000 总预算" ],
  "ref": "auto-restore"
},
{
  "slug": "wedding/wedding-car-route",
  "inputs": {
    "departTime": "07:00_X",
    "carCount": "6"
  },
  "expect": [
    "00_X"
  ],
  "ref": "auto-restore"
},
  {
    slug: "wedding/wedding-banquet",
    inputs: { guests: "130", type: "round10", backup: "mid" },
    expect: ["12 桌 按预计到场 117 人订桌", "13 桌 全部受邀 130 人都到场", "14 桌 合计预订桌数"],
    ref: "130 人受邀、90% 到场 ⇒ 预计 117 人，ceil(117/10)=12 桌；全部到场 ceil(130/10)=13 桌；备桌 mid=2 ⇒ 合计 14 桌。默认 120 人 ⇒ 11/12/13 桌，不命中。",
  },

  {
    slug: "wedding/wedding-banquet",
    inputs: { guests: "137", type: "square8", backup: "big" },
    expect: ["16 桌 按预计到场 124 人订桌", "18 桌 全部受邀 137 人都到场", "19 桌 合计预订桌数", "约 124 人 预计到场（受邀 × 90%）"],
    ref: "type=square8 ⇒ perTable=8；预计到场 ceil(137×0.9)=124 ⇒ ceil(124/8)=16 桌；全部到场 ceil(137/8)=18 桌；backup=big ⇒ 3 桌 ⇒ 合计 19 桌。默认 120/round10/mid ⇒ 11/12/14 桌，不命中。",
  },

  {
    slug: "wedding/wedding-budget-planner",
    inputs: { totalBudget: "", spent: "" },
    expect: ["请填写 总预算、已花费 后再计算"],
    ref: "空态守卫：总预算与已花费留空 ⇒ 提示，不再按 0 兜底给出「已超支/剩余」结论。"
       + "默认态总预算有初值并渲染预算结论，不含该提示 ⇒ 可判别。",
  },
  {
    slug: "wedding/countdown-time",
    clicks: ["document.getElementById('weddingDate').value='2024-09-09';setWedding()"],
    expect: ["距离 9月9日 周一 婚礼", "86", "天后举行"],
    ref: "婚期 2024-09-09、基准日冻结 2024-06-15 ⇒ dayDiff = 86 ⇒ 主卡「距离 9月9日 周一 婚礼 / 86 / 天后举行」；同时生成 6 个里程碑（订婚/领证/策划/试妆/彩排/当天）。默认 state.weddingDate 为空 ⇒ emptyCard 显示、heroBox 置空，三锚均不命中（判别时清空 clicks 即回默认态）。"
  },
{
  "slug": "wedding/wedding-budget-planner",
  "inputs": {"totalBudget":"0","spent":"0"},
  "clicks": ["resetBudget()"],
  "expect": ["¥0总预算¥0已分配¥0剩余", "当前预算为 0，暂无已分配支出项"],
  "ref": "总预算 0 后重置分配：所有分类金额应为 0，结果卡总额/已分配/剩余均为 ¥0；旧 renderItems 的 `||100000` 会重新填入 ¥100,000 分类金额。默认 100000 不命中。"
},
{
  "slug": "wedding/countdown-timeline",
  "clicks": ["document.getElementById('weddingDate').value='2027-01-01';document.getElementById('weddingTime').value='00:30';calc();"],
  "expect": ["前一天", "21:30"],
  "ref": "跨日显示：仪式 00:30，化妆造型 offset -180 ⇒ 前一日 21:30；旧版负数取模输出 -3:30 或无日期提示。默认 10:00 当天不命中。"
},
{
  "slug": "wedding/seating-chart",
  "clicks": ["document.getElementById('guestName').value='测试宾客';addGuest();var g=guests[guests.length-1];toggleMain(g.id);"],
  "expect": ["主桌（1人）", "主桌"],
  "ref": "手动指定主桌：新宾客添加后勾选主桌，主桌卡应含 1 人；旧版主桌只按家族顺序自动填充，无勾选入口。默认空名单不命中。"
},
{
  "slug": "wedding/seating-chart",
  "clicks": ["document.getElementById('guestName').value='持久化宾客';addGuest();document.getElementById('__tbProbe').textContent='SEATSAVE '+(loadState()?'OK':'BAD');"],
  "expect": ["SEATSAVE OK"],
  "ref": "本地保存：添加宾客后 saveState 写入 localStorage，loadState 能读回；旧版刷新即丢失。默认空态不命中。"
},
{
  "slug": "wedding/seating-chart",
  "clicks": ["document.getElementById('guestName').value='锁桌宾客';addGuest();var g=guests[guests.length-1];lockGuest(g.id,'第二桌');"],
  "expect": ["第二桌", "锁桌宾客"],
  "ref": "手动调桌：lockGuest 指定第二桌后宾客落在该桌卡片，不再按分组自动分配。默认空名单不命中。"
},
{
  "slug": "wedding/wedding-budget-planner",
  "clicks": ["document.getElementById('spent').value='-1000';calc();"],
  "expect": ["以下金额须为有限非负数（允许 0）：已花费（≥0）"],
  "ref": "负金额守卫：总预算 100000、已花费 -1000 旧版显示剩余 101000；现在停止并逐项提示。默认 spent=0 不命中。"
},
{
  "slug": "wedding/wedding-car-route",
  "clicks": ["stops=[{name:'A',dur:0,distance:100,drive:20},{name:'B',dur:0,distance:0,drive:0}];renderStops();document.getElementById('departTime').value='08:00';document.getElementById('avgSpeed').value='30';document.getElementById('bufferMin').value='5';calc();"],
  "expect": ["08:25", "已填逐段预计行驶分钟的路段优先用你的估时"],
  "ref": "逐段估时：A→B 段距离 100km、预计行驶填 20 分钟，虽 30km/h 理论需 200 分钟，仍按 20+5 缓冲 ⇒ 08:00 出发 08:25 到达；旧版固定按距离/30 估算得 11:25。默认路线无 drive 值不命中。"
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

  console.log("==== wedding calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
