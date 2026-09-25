#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "gardening/balcony-sunlight",
  "inputs": {},
  "clicks": ["document.getElementById('dir').value='north';document.getElementById('floor').value='high';document.getElementById('season').value='winter';calcTool()"],
  "expect": [
    "1.0 小时 每日直射光照（北向·冬）",
    "虎皮兰、一叶兰、蕨类、竹芋、白掌 推荐植物"
  ],
  "ref": "三个 <select> 的 option 由 JS 填充（静态 HTML 无 option ⇒ 只能 clicks 赋值）：注入 北向+高楼层+冬季 ⇒ sunTab.north.winter=0.5、floorAdj.high=+0.5 ⇒ hours=1.0（默认 南向·中楼层·春 = 6+0=6.0）；光照类型降为耐阴、推荐植物换为耐阴清单。非默认输入+独立复算。"
},
{
  "slug": "gardening/compost-calculator",
  "inputs": {},
  "clicks": ["materials[0].idx=12;materials[0].weight=4;materials[1].idx=4;materials[1].weight=2;calc()"],
  "expect": [
    "12.4:1 混合 C:N 比",
    "鸡粪 10:1 4.00 4.00 0.4000 57.1%"
  ],
  "ref": "原料行的 <select>/<input> 由 renderMaterialList() 拼 innerHTML 生成（无静态 id ⇒ clicks 直接改顶层 materials 再 calc()）：鸡粪(10:1)4kg 氮代理 4/10=0.4000、咖啡渣(20:1)2kg=0.1000、蔬菜废料(15:1)1kg=0.0667 ⇒ 总重 7.00、总氮 0.5667 ⇒ C:N=7/0.5667=12.35→12.4:1，鸡粪占比 4/7=57.1%（默认 落叶2/草坪1/蔬菜1 = 26.7:1）。非默认输入+独立复算。"
},
{
  "slug": "gardening/garden-calendar",
  "clicks": [
    "setMonth(12)"
  ],
  "expect": [
    "12月 园艺工作 · 北方 共 3 项工作"
  ],
  "ref": "去默认化（原 expect「10月」＝默认当月态，注入失败仍命中 → 逃生项）：clicks 调 setMonth(12)（无 this 依赖），render() 输出 12 月北方园艺「12月 园艺工作 · 北方 共 3 项工作 修剪 冬季修剪...」；默认九月显示「9月 ...」不含「12月 ... 北方」，注入失败即不命中。（注：setZone('south') 触发 buildMonthText 在南方分区有未定义项报错，故只切月份、走默认北方分区。）"
},
{
  "slug": "gardening/garden-layout",
  "inputs": {
    "area": "30"
  },
  "expect": [
    "3265"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/garden-tools",
  "inputs": {
    "searchInput": "zzz"
  },
  "expect": [
    "未找到匹配的工具，请调整筛选条件"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部工具，不产此串）"
},
{
  "slug": "gardening/pest-identifier",
  "inputs": {
    "searchInput": "zzz"
  },
  "expect": [
    "未找到匹配的病虫害，请调整筛选条件"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部病虫害，不产此串）"
},
{
  "slug": "gardening/plant-calendar",
  "inputs": {},
  "expect": [
    "11-12月"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "gardening/plant-care",
  "inputs": {
    "searchInput": "zzz"
  },
  "expect": [
    "未找到匹配的植物，请调整筛选条件"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部植物，不产此串）"
},
{
  "slug": "gardening/pot-capacity",
  "inputs": {
    "${f.id}": "${f.value}_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/recommender",
  "inputs": {
    "cnt": "12"
  },
  "clicks": ["var __r=Math.random;Math.random=function(){return 0.1;};gen();Math.random=__r"],
  "expect": [
    "12. 吊兰 | 春季·晴天·疏松透气 → 建议每3-5天1次，保持土壤微润，避免积水"
  ],
  "ref": "纯随机页：clicks 内钉死 Math.random=0.1 并**用完即恢复**（进程级全局，不恢复会污染后续用例默认态）。"
     + "PLANTS/SEASONS/WEATHERS/SOILS 长度分别为 12/4/4/4 ⇒ floor(0.1×len) 依次取索引 1/0/0/0"
     + "=吊兰/春季/晴天/疏松透气；freq 判 weather=晴天 ⇒ 每3-5天1次；tips 判 plant=吊兰 ⇒ 保持土壤微润，避免积水。"
     + "cnt=12 ⇒ 末条编号为 12.，默认态（5 条）不可能出现。原 expect「建议每10-14天1次」是随机档位文案（默认态亦命中）。",
  },
{
  "slug": "gardening/soil-ph",
  "inputs": {
    "soilPh": "9.5"
  },
  "expect": [
    "+3.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/watering-schedule",
  "inputs": {
    "potSize": "30"
  },
  "expect": [
    "1.08L"
  ],
  "ref": "auto-restore"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== gardening calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
