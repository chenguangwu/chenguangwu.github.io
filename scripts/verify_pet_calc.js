#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "pet/analysis-cost-profit-1",
  "inputs": {
    "visits": "250",
    "aov": "360",
    "vc": "150",
    "rent": "15000",
    "staff": "25000",
    "util": "4000",
    "other": "6000"
  },
  "expect": [
    "14,500.00",
    "181.0",
    "210.00"
  ],
  "ref": "宠物门店盈亏：unit=360−150=210.00；fixed=15000+25000+4000=44,000.00；profit=(250×360−250×150)+6000−44000=14,500.00；beVisits=(44000−6000)/210=181.0（独立复算；默认组为 25,400.00/170.6/170.00，注入失败即不命中）"
},
{
  "slug": "pet/checker-16",
  "inputs": {
    "bizType": "shop"
  },
  "expect": [
    "shop"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "pet/checker-diagnosis",
  "inputs": {
    "age": "3",
    "temp": "38.5",
    "weight": "10",
    "duration": "2",
    "species": "cat"
  },
  "expect": [
    "cat"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "pet/convert-25",
  "inputs": {
    "species": "dog",
    "age": "5"
  },
  "expect": [
    "人类年龄 ≈ 36.0 岁"
  ],
  "ref": "去默认化：狗 5 岁 ⇒ 24+(5−2)×4 = 36.0 岁。默认态 species=dog/age=3 ⇒ 28.0 岁，不命中。"
},
{
  "slug": "pet/convert-25",
  "inputs": {
    "species": "dog",
    "age": "1"
  },
  "expect": [
    "人类年龄 ≈ 15.0 岁"
  ],
  "ref": "去默认化：狗 1 岁 ⇒ 15.0 岁。默认态不命中。"
},
{
  "slug": "pet/convert-25",
  "inputs": {
    "species": "cat",
    "age": "7"
  },
  "expect": [
    "人类年龄 ≈ 44.0 岁"
  ],
  "ref": "去默认化：猫 7 岁 ⇒ 24+(7−2)×4 = 44.0 岁。默认态不命中。"
},
{
  "slug": "pet/pet-feeding-calc",
  "inputs": {
    "weight": "15",
    "calDensity": "3.5"
  },
  "expect": [
    "534 RER静息能量(kcal)",
    "244 g/天"
  ],
  "ref": "合并自 pets/feeding-amount（去默认化：15kg → RER=70×15^0.75=533.5→534 kcal；×1.6÷3.5=243.9→244 g/天。默认 10kg 得 394 kcal / 180 g/天）"
},
{
  "slug": "pet/grooming-guide",
  "clicks": [
    "setPet('dog');selectBreed('bichon');"
  ],
  "expect": [
    "圆球装"
  ],
  "ref": "合并自 pets/grooming-guide（弱用例去默认化：原锚默认「该品种暂无造型数据」（判别力0）。clicks 经 setPet('dog')+selectBreed('bichon') 切到比熊造型，expect 锚比熊专属「圆球装」；清 clicks 兜底遍历不产出 ⇒ 零逃生项）"
},
{
  "slug": "pet/kennel-space",
  "inputs": {
    "count": "4",
    "days": "7"
  },
  "expect": [
    "24.0 ㎡ 犬舍总面积",
    "61.5 ㎡ 总所需面积（4只中型犬 · 7天）"
  ],
  "ref": "合并自 pets/kennel-space（去默认化：默认中型犬 4只/7天 → 犬舍 6×4=24.0 ㎡，活动区 15×(1+3×0.5)=37.5，总 61.5 ㎡。不可用小型犬值 16.0/36.0：零参兜底 selectSize() 会把尺寸重置为小型犬，同样产出该串 → 逃生项）"
},
{
  "slug": "pet/pet-medicine",
  "inputs": {
    "weight": "15"
  },
  "expect": [
    "15"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "pet/reminder-vaccine-deworming",
  "clicks": [
    "var d=new Date();d.setDate(d.getDate()+1);var p2=function(n){return (n<10?'0':'')+n;};var tomorrow=d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate());document.getElementById('petName').value='甲';document.getElementById('petSpecies').value='cat';document.getElementById('petBirth').value='2020-01-01';addPet();var h=String(document.getElementById('petList').innerHTML);var i=h.indexOf('recDate_');var pid=i>=0?h.slice(i+8).split(String.fromCharCode(34))[0]:'';document.getElementById('recDate_'+pid).value=tomorrow;addCustomRecord(pid);document.getElementById('__tbProbe').textContent='FUT '+((pid&&document.getElementById('logCard').style.display==='none')?'0':'1');"
  ],
  "expect": [
    "FUT 0"
  ],
  "ref": "未来日期记录拒绝：先用 addPet 建一只猫档案，从 #petList 渲染串取回 recDate_<id> 输入并把补录日期设为明天，再调用 addCustomRecord ⇒ 不应写入任何记录（记录日志卡保持 display:none，探针 FUT 0）；旧实现无日期上限，明天日期会入库并让 renderLog 显示日志卡（探针 FUT 1）。默认态（不执行 clicks）无探针串 ⇒ 零逃生。"
},
{
  "slug": "pet/reminder-vaccine-deworming",
  "clicks": [
    "var d=new Date();d.setDate(d.getDate()+5);var p2=function(n){return (n<10?'0':'')+n;};document.getElementById('petName').value='乙';document.getElementById('petBirth').value=d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate());addPet();document.getElementById('__tbProbe').textContent='BIRTH '+((String(document.getElementById('petList').innerHTML).indexOf('暂无宠物档案')>=0)?'0':'1');"
  ],
  "expect": [
    "BIRTH 0"
  ],
  "ref": "未来出生日期拒绝：出生日期设为 5 天后调用 addPet ⇒ 不应新增宠物（#petList 仍为「暂无宠物档案」，探针 BIRTH 0）；旧实现只校验非空，未来出生日期会入库并据此推算全部免疫到期日（探针 BIRTH 1）。默认态无探针串 ⇒ 零逃生。"
},
{
  "slug": "pet/reminder-vaccine-deworming",
  "inputs": {
    "petWeight": "0",
    "recDate_'+p.id+'": "'+fmtDate(today())+'",
    "petSpecies": "cat"
  },
  "expect": [
    "cat"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "pet/training-planner",
  "inputs": {
    "age": "senior"
  },
  "expect": [
    "狗狗 · 老年期"
  ],
    ref: "age=senior（老年期 7 岁+）⇒ 计划概要渲染「狗狗 · 老年期 · 每日20分钟 · 1个训练目标」。⚠ 原注入 junior 恰为页面 select 默认选中项、原 expect「junior」只是 select 值回显 ⇒ 默认态同样命中（真逃生），故改注入非默认年龄段并锚结果区派生串。默认态为「狗狗 · 青少年」，不含老年期。",
},
{
  "slug": "pet/fish-tank-volume",
  "inputs": {
    "length": "90",
    "width": "30",
    "diameter": "40",
    "frontLen": "60",
    "backLen": "50",
    "bowWidth": "30",
    "height": "35",
    "substrate": "5"
  },
  "expect": [
    "19.26"
  ],
  "ref": "auto-restore"
},

{
  "slug": "pet/training-planner",
  "inputs": { "age": "junior", "dailyTime": "20" },
  "clicks": ["selectPet('dog',{classList:{add:function(){}}});toggleGoal('house');var v=Array.from(document.getElementById('planOverview').innerHTML.matchAll(/class=\"v\">([^<]+)/g),function(m){return m[1];}).join(',');document.getElementById('planOverview').textContent='V:'+v+'|T:'+document.querySelectorAll('#weeklyPlan .task-item').length;"],
  "expect": ["V:7,20,3,9|T:28"],
  "ref": "深度解析算例复算：基础服从 5 项 + 如厕训练 4 项 = 9 项，20 分钟时段数 3，每日 min(3+1,9)=4 条，一周 7×4=28 条。默认只选基础服从 ⇒ 末位为 5 ⇒ 不命中。"
},
{
  "slug": "pet/training-planner",
  "inputs": { "age": "junior", "dailyTime": "45" },
  "clicks": ["selectPet('dog',{classList:{add:function(){}}});var v=Array.from(document.getElementById('planOverview').innerHTML.matchAll(/class=\"v\">([^<]+)/g),function(m){return m[1];}).join(',');document.getElementById('planOverview').textContent='V:'+v+'|T:'+document.querySelectorAll('#weeklyPlan .task-item').length;"],
  "expect": ["V:7,45,4,5|T:35"],
  "ref": "深度解析算例二复算：只选基础服从 5 项、45 分钟时段数 4，每日 min(4+1,5)=5 条，一周 35 条。默认 20 分钟 ⇒ V:7,20,3,5|T:28 ⇒ 不命中。"
},

{
  "slug": "pet/pet-age",
  "inputs": {
    "petAge": "6"
  },
  "expect": [
    "40岁"
  ],
  "ref": "433 复核：年龄表首项对应 1 岁，猫 6 岁取 CAT_AGES[5]=40（修复前按 petAge 直接索引得 44）"
},
{
  "slug": "pet/pet-age",
  "inputs": {
    "petAge": "0"
  },
  "expect": [
    "0岁"
  ],
  "ref": "433 复核：猫 0 岁折 0（修复前取 CAT_AGES[0]=15，历史页为 0）；6 岁默认态不含该串"
},
{
  "slug": "pet/pet-age",
  "inputs": {
    "petAge": "1"
  },
  "expect": [
    "15岁"
  ],
  "ref": "433 复核：猫 1 岁取年龄表首项 15（修复前取 CAT_AGES[1]=24，历史页为 15）；6 岁默认态不含该串"
},

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

  console.log("==== pet calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
