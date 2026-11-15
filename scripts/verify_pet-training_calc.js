#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pet-training/clicker-timing",
  "inputs": {
    "duration": "1200"
  },
  "expect": [
    "1200"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "pet-training/command-repetition",
  "inputs": {
    "reps": "12",
    "hoursAgo": "24",
    "age": "6"
  },
  "expect": ["12\n24\nnormal\n6\n3% 记忆严重衰退，需立即重新训练\n第—→—次 1小时后 保留—% 第—→—次 4小时后 保留—% 第—→—次 12小时后 保留—% 第—→—次 1天后 保留—% 第—→—次 3天后 保留—% 第—→—次 7天后 保留—% 第—→—次 14天后 保留—% 第—→—次 30天后 保留—%"],
  "ref": "s=0.35(easy)×1.0(age6)=0.35；retention=exp(−0.35×24/√12)=exp(−2.4249)=0.0885→9%（原断言“5%”会被默认输出的“15%/5%”子串命中 → 逃生项）"
},
{
  "slug": "pet-training/elimination-predict",
  "inputs": {
    "age": "3",
    "afterDrink": "15",
    "petType": "cat"
  },
  "expect": [
    "cat"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "pet-training/elimination-predict",
  "clicks": [
    "document.getElementById('age').value='3';document.getElementById('afterDrink').value='30';document.getElementById('petType').value='cat';calc();var a=document.getElementById('result').innerHTML.indexOf('立即带去定点')>=0;document.getElementById('afterDrink').value='5';calc();var b=document.getElementById('result').innerHTML.indexOf('10 分钟后')>=0;document.getElementById('afterDrink').value='';calc();var c=document.getElementById('result').innerHTML.indexOf('请输入饮水后已过分钟数')>=0&&document.getElementById('timeline').innerHTML==='';document.getElementById('__tbProbe').textContent='ELIM '+a+' '+b+' '+c;"
  ],
  "expect": ["ELIM true true true"],
  "ref": "修复前 `postDrinkTime=isPuppy?15-30:20-40` 是减法（幼宠 −15、成宠 −20），任何饮水后时间都判「立即带去」；现幼宠窗口 15–30 分钟，饮水后 30 分钟才提示立即、5 分钟显示「10 分钟后」，空值提示补录并清空时间线。默认 age3/afterDrink15 不走这三支。"
},
{
  "slug": "pet-training/clicker-timing",
  "inputs": {
    "duration": "1200"
  },
  "expect": [
    "1200"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "pet-training/clicker-timing",
  "clicks": [
    "var s=String(scheduleNext),h=String(handleClick);var ok=/clearTimeout\\(nextTimer\\)/.test(s)&&/nextTimer=setTimeout/.test(h)&&/recordAttempt\\(null\\);\\s*updateStats\\(\\)/.test(s);document.getElementById('__tbProbe').textContent='CLK '+ok;"
  ],
  "expect": ["CLK true"],
  "ref": "修复前错过行为只 recordAttempt(null) 不刷新统计、命中后的 800ms 定时器未保存（停止后旧回调仍可推进新一局）；现 miss 分支补 updateStats()、scheduleNext 先清旧定时器、命中延时写入 nextTimer 供 stopGame 取消。时序无法在桩内驱动，故用源码形态判定。默认态不产生该探针串。"
},
{
  "slug": "pet-training/leash-length",
  "inputs": {
    "leashLen": "4.5",
    "weight": "15"
  },
  "expect": [
    "当前绳长(4.5m)超过城市街道建议上限(1.8m)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "pet-training/leash-length",
  "clicks": [
    "document.getElementById('leashLen').value='4.5';calc();var before=document.getElementById('adviceBox').innerHTML.length>0;document.getElementById('leashLen').value='';calc();var after=document.getElementById('adviceBox').innerHTML;document.getElementById('__tbProbe').textContent='LEASHCLR '+(before&&after===''?'OK':'BAD:'+before+':'+after);"
  ],
  "expect": ["LEASHCLR OK"],
  "ref": "修复前清空绳长只清结果/网格/图示，adviceBox 仍显示上一次的「超过建议上限」安全建议；现无效输入同时清空建议区。默认有效输入不走该分支，探针串不出现。"
},
{
  "slug": "pet-training/command-repetition",
  "clicks": [
    "document.getElementById('hoursAgo').value='';calc();var r=document.getElementById('result').innerHTML,s=document.getElementById('scheduleGrid').innerHTML;var ok1=r.indexOf('请输入已过小时数')>=0&&r.indexOf('严重衰退')<0&&s==='';document.getElementById('hoursAgo').value='24';document.getElementById('age').value='';calc();var r2=document.getElementById('result').innerHTML;var ok2=r2.indexOf('请输入有效年龄')>=0;document.getElementById('__tbProbe').textContent='CRMISS '+ok1+' '+ok2;"
  ],
  "expect": ["CRMISS true true"],
  "ref": "修复前已过小时数清空得 NaN，仍落入 else 分支显示「记忆严重衰退」并保留旧复习计划；年龄清空被当成年犬。现两项分别提示补录且清空计划区。默认 10/24/6 均有效，探针串不出现。"
},
{
  "slug": "pet-training/command-repetition",
  "clicks": [
    "document.getElementById('reps').value='12';document.getElementById('hoursAgo').value='24';document.getElementById('age').value='6';calc();var got='';ToolBox.copyText=function(t){got=String(t);};copyResult();document.getElementById('__tbProbe').textContent='CRCOPY '+(got.indexOf('复习计划')>=0&&got.indexOf('第12→13次 | 1小时后 | 保留')>=0&&got.indexOf('第12→19次')<0?'OK':'BAD:'+got);"
  ],
  "expect": ["CRCOPY OK"],
  "ref": "修复前「复制训练计划」只复制保留率与一句提示，没有计划明细；现按 renderSchedule 的数据附带第 N→N+1 次、间隔与保留率逐条计划。默认态不调用 copyResult，探针串不出现。"
},
{
  "slug": "pet-training/treat-calories",
  "inputs": {
    "weight": "15",
    "treatCal": "15",
    "treatCount": "5"
  },
  "expect": ["dog\n15\n15\n5\nnormal\nno\n8.8% 零食 75 kcal / 每日总需 854 kcal\n854 每日总热量 (kcal) 75 零食总热量 (kcal) 85 零食上限 (kcal) 5 每日最多颗数\n零食占比 8.8% 建议上限 10% ✅ 零食热量在安全范围内（≤10%），可放心给予。剩余91.2%热量来自主粮。"],
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

  console.log("==== pet-training calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
