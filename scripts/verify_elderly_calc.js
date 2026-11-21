#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "elderly/aid-height",
  "inputs": {
    "height": "248",
    "shoe": "2"
  },
  "expect": [
    "250.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/assessor-35",
  "inputs": {
    "age": "113"
  },
  "expect": [ "113 年龄" ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/assessor-36",
  "inputs": {
    "s1": "1"
  },
  "expect": [
    "关注"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/assessor-37",
  "inputs": {
    "q1": "4"
  },
  "expect": [
    "均值4.80"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/assessor-risk-1",
  "inputs": {
    "e1": "2"
  },
  "expect": [
    "加装夜灯和感应灯"
  ],
  "ref": "auto-restore"
},
{
  "slug": "elderly/bp-trend",
  "inputs": {
    "logPeriod": "上午"
  },
  "expect": [
    "上午"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "elderly/eldercare-level",
  "inputs": {},
  "checks": [
    "2"
  ],
  "expect": [
    "需高频照护，建议专业护理人员介入并评估康复计划。"
  ],
  "ref": "checks 注入：本页 7 个 radio 组（name=a0..a6，每题 0/1/2，HTML 默认选中第一项即 0 分）经 `document.querySelector('input[name=aN]:checked').value` 读数；harness 的 querySelector(':checked') 桩只认 `checks`（querySelectorAll 那条才认 radios），且把首个值返回给所有组 ⇒ 声明 checks:[\"2\"] 等价「7 题全选最重档」，独立复算 score=7×2=14 ≥10 ⇒ 三级（重度）+ 该照护建议。旧锚「1.」是题号列表字面量 ⇒ 判别力 0。清 checks 后落到默认 0 分项、score=0 ⇒ 一级（轻度）不产出该句 ⇒ 零逃生项。"
},
{
  "slug": "elderly/fall-risk",
  "inputs": {},
  "clicks": [
    "getScore=function(){return 3;};renderAdvice();"
  ],
  "expect": [
    "卫生间、厨房铺设防滑地垫，保持地面干燥"
  ],
  "ref": "（2026-09-24 曾记为「getScore 走 input[name=..]:checked 属性选择器 ⇒ 结构性不可注入」，本批次推翻）getScore 是顶层函数声明，在页面作用域里可整体替换；覆写后直接调 renderAdvice() 即可让全部 12 条条件项入列，命中 e1 分支专属串。默认态 getScore 返回 null ⇒ items 为空，只 push「继续保持良好的居家与生活习惯」，不含该串。旧锚「行走时是否需要借助辅助器具或他人搀扶」是静态题干、默认态必命中，判别力 0，已弃。"
},
{
  "slug": "elderly/fall-risk",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/elderly/fall-risk.html','utf8');var noOld=h.indexOf('Morse 评分')<0&&h.indexOf('Morse 2009')<0&&h.indexOf('>45 高危')<0&&h.indexOf('条目加权求和')<0;var hasNew=h.indexOf('本页自建问卷')>=0&&h.indexOf('风险占比 &lt;25% / &lt;50% / &lt;75% / ≥75%')>=0&&h.indexOf('12 题选项分值累加')>=0;document.getElementById('__tbProbe').textContent='FR1287 '+(noOld&&hasNew?'OK':'BAD');"],
  "expect": ["FR1287 OK"],
  "ref": "12-L8 引据表模板串味：页面实为 12 题自建问卷（环境6+身体6）、满分 25、按风险占比 <25%/<50%/<75% 分低/中/高/极高，引据表却错挂 Morse 2009「>45 高危」（0-25 分体系永不可达、分级名也不属 Morse 口径）。本批删虚假 Morse 引用、改标真实自建口径。源码形态哨兵：旧版四项 Morse 串任一出现即红；修复版须同时含三个新口径串。默认态不产生该哨兵（仅在 clicks 读源码后出现），零逃生。"
},
{
  "slug": "elderly/reminder-time",
  "inputs": {
    "time1": "08:00",
    "time2": "20:00",
    "medHours": "12"
  },
  "expect": [
    "12"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
}
,
{
  "slug": "elderly/wheelchair-width",
  "inputs": { "sceneSel": "corridor", "chairSel": "electric", "useSel": "assist" },
  "expect": ["建议走廊净宽 ≥ 1500 mm"],
  "ref": "注入非默认场景 corridor/electric/assist（默认 door/manual/self）→ 输出段变「走廊通行 电动轮椅…建议走廊净宽 ≥ 1500 mm」；默认态为门洞 800mm，不含该串，0 逃生。"
},
{
  "slug": 'elderly/bp-trend',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/elderly/bp-trend.html\',\'utf8\');var i=h.indexOf(\'function switchTab(name, ev){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'if(!name||!ev)\')>=0&&seg.indexOf(\'drawChart(); renderHistory(); return;\')>=0;document.getElementById(\'__tbProbe\').textContent=\'BPTRH0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['BPTRH0 OK'],
  "ref": "第1336批·历史恢复无参切换函数抛错修复源码形态强锚：旧版 function switchTab(name, ev){ 无参调用解引用参数抛错被 catch 吞、结果不重算；修复后无参分支安全重算本页主结果并 return。旧版无 ⇒ BAD。"
},
{ slug:"elderly/assessor-35", inputs:{"age":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" }
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

  console.log("==== elderly calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
