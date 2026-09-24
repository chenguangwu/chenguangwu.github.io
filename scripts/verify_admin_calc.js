#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "admin/register-depreciation",
  "inputs": {
    "aCost": "10000",
    "aSalvage": "500",
    "aLife": "5"
  },
  "expect": [
    "电子设备"
  ]
},
{
  "slug": "admin/supplies-forecast",
  "inputs": {
    "window": "2",
    "safetyFactor": "1.5"
  },
  "expect": [
    "151.5 下月预测",
    "227.3 建议采购量"
  ],
  "ref": "非默认输入（默认 window=3 / safetyFactor=1.2）：data 六个月的 120/135/128/142/155/148 是页面顶层常量，不随输入变化。移动平均窗口取 2 ⇒ 下月预测 nextMa = (155+148)÷2 = 151.5；建议采购量 = 151.5 × 1.5 = 227.25 ⇒ fmt 取 1 位小数 = 227.3。默认态为 148.3 / 178.0（两串均不含）。注：月均 138.0、最高 155.0、波动范围 120.0~155.0 只由常量 data 决定、与注入字段无关 ⇒ 默认态同样命中，故一律不锚（BATCH98 教训：锚点在默认态命中即零判别力）。"
},
{
  "slug": "admin/travel-subsidy",
  "inputs": {
    "mealStd": "150",
    "transStd": "120"
  },
  "expect": [
    "4,890 补贴总额(元)",
    "1,050 伙食补助"
  ],
  "ref": "非默认输入（默认 mealStd=100 / transStd=80）：trips 三条为页面顶层常量（北京/一类城市/3天、成都/三类城市/2天、苏州/四类城市/2天，共 7 天）。伙食合计 = 150×7 = 1,050；交通合计 = 120×7 = 840；住宿 = 500×3 + 400×2 + 350×2 = 3,000；补贴总额 = 1,050+840+3,000 = 4,890。默认态为 700 / 560 / 4,260（两串均不含）。注：出差天数 7、住宿限额 3,000 与注入字段无关（只随常量 trips 与城市档位变化）⇒ 不锚。"
},
{
  "slug": "admin/analysis-30",
  "inputs": {
    "data": "办公用品,20000,23500\n差旅费,50000,42000\n水电费,30000,34500\n通讯费,12000,10800\n维修费,15000,15000"
  },
  "expect": [
    "预算合计： 127000.00",
    "预算执行率： 99.06%",
    "总差异： -1200.00"
  ],
  "ref": "预算127000、实际125800、总差异−1200、执行率99.06%；超支2项合计8000（默认3项预算65000/实际63000、差异−2000，且默认最大超支项同为水电费，故 avoid 该项、改断言总差异）"
},
{
  "slug": "admin/checker-manager-training-hr",
  "clicks": [
    "MODULES.forEach(function(m,mi){m.items.forEach(function(it,ii){document.getElementById('m'+mi+'_'+ii).value='2';});});calc()"
  ],
  "expect": [
    "全部项目已落实",
    "8/8"
  ],
  "ref": "静态控件数为 0（12 个评分 select 由 MDULES 遍历运行期拼 innerHTML 生成，id 形如 m0_0…m2_3），故用 clicks 在页面作用域内把全部 select 置为已落实（2 分）后调 calc()。三个模块各 4 项 × 2 分 = 24 满分 ⇒ 全 2 分后 totalScore=24、rate=100% ⇒ 走 gaps 为空的分支渲染「全部项目已落实」，模块表每行得分列为 8/8。默认态全 0 分 ⇒ rate=0%、渲染「需整改项（12）」、模块列 0/8（两串均不含，原 expect「0/8」即默认渲染串、零判别力，已废弃）。"
},
{
  "slug": "admin/detector-time",
  "inputs": {},
  "expect": [
    "请添加会议日程并填写时间"
  ],
  "ref": "结构性不可注入（沿用 tcm-diagnosis/etiology-tree 的处理口径）：日程行由 addRow() 用 document.createElement + #rows.appendChild 建立，detect() 靠 document.querySelectorAll('#rows .input-row') 遍历取值。桩环境的 dynRecord 只登记 innerHTML 解析出的标签（不含容器 div 自身），故该选择器恒返回空 ⇒ addRow 后在桩里永远得到「共 0 个有效日程」。实测 clicks=[addRow(...)×2] 仍无法产出冲突结果（且 FAIL 时的 blob 会被兜底阶段的无参 render() 覆盖回默认，容易误判「clicks 未生效」）。维持 no_inputs，断言初始化渲染串。"
},
{
  "slug": "admin/meeting-conflict",
  "clicks": [
    "events=[{name:'甲',start:'08:00',end:'09:30'},{name:'乙',start:'09:00',end:'11:00'},{name:'丙',start:'13:00',end:'14:00'}];renderList();render()"
  ],
  "expect": [
    "冲突：甲 与 乙",
    "重叠时段：09:00 - 09:30（重叠 30 分钟）",
    "270分钟"
  ],
  "ref": "静态控件数为 0（日程行由 renderList() 运行期拼 innerHTML），故用 clicks 在页面作用域重写顶层 events 数组后调 renderList()/render()。三条日程：甲 08:00-09:30、乙 09:00-11:00（二者重叠 09:00-09:30 = 30 分钟）、丙 13:00-14:00 ⇒ 有效日程 3、冲突 1 处、总时长 = 90+120+60 = 270 分钟。页面默认 events 为晨会/产品评审/午餐/客户拜访/部门周会（2 处冲突、总时长 360、时间范围 09:00-16:00）⇒ 三串均不含（原 expect「00-16」即默认渲染的时间范围串、零判别力，已废弃）。"
},
{
  "slug": "admin/version-control",
  "inputs": {
    "fileName": "项目方案书",
    "author": "张三",
    "changeNote": "",
    "bumpType": "minor"
  },
  "expect": [
    "0.1.0"
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
  console.log("==== admin calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
