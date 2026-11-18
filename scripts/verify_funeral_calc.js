#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  slug: "funeral/reminder-3", inputs: {lYear:"2020"},
  clicks: ["var NativeDate=Date;Date=class extends NativeDate{constructor(...a){super(...(a.length?a:['2026-11-18T12:00:00']));}static now(){return new NativeDate('2026-11-18T12:00:00').getTime();}};var d=getNextDate({type:'lunar',yearly:true,lMonth:4,lDay:1,lLeap:true});var ok=d&&d.getFullYear()===2058&&lunarToSolar(2026,4,1,true)===null;Date=NativeDate;document.getElementById('__tbProbe').textContent='LEAPNEXT:'+(ok?'OK':'BAD');"],
  expect: ["LEAPNEXT:OK"], ref: "2026 年后闰四月下一次为 2058，且无该闰月时不转换。"
},
{
  "slug": "funeral/ceremony-timeline",
  "inputs": {
    "startTime": "09:00",
    "scale": "medium"
  },
  "expect": [
    "medium"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "funeral/funeral-budget-planner",
  "inputs": {
    "newCat": "ritual"
  },
  "expect": [
    "ritual"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "funeral/grave-design",
  "inputs": {
    "title": "故先考",
    "name": "李公讳某某",
    "birthYear": "一九四五年",
    "deathYear": "二〇二三年",
    "stoneW": "3.8",
    "stoneH": "1.0",
    "plotL": "2.5",
    "plotW": "1.5",
    "epitaph": "慈父一生勤俭持家，德厚流光，恩泽子孙。痛于二〇二三年某月某日溘然长逝，享年七十八岁。立碑永志，以示追思。"
  },
  "expect": [ "面积 3.80" ],
  "ref": "auto-restore"
},
{
  "slug": "funeral/memorial-date",
  "inputs": {
    "memTitle": "先考_X",
    "memName": ""
  },
  "expect": [
    "先考_X"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "funeral/urn-size",
  "inputs": {
    "weight": "98",
    "height": "170"
  },
  "expect": [
    "23×16×16"
  ],
  "ref": "auto-restore"
},
  {
    "slug": "funeral/reminder-3",
    "inputs": {
      "sName": "abc123测试",
      "sDate": "abc123测试",
      "lName": "abc123测试",
      "lYear": "42",
      "lMonth": "2"
    },
    "expect": [
      "，请在上方添加。\n⚠ 计算结果含无效值，请检查输入是否为有效正数。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sName\":\"abc123测试\",\"sDate\":\"abc123测试\",\"lName\":\"abc123测试\",\"lYear\":\"42\",\"lMonth\":\"2\"}，输出区含「，请在上方添加。\n⚠ 计算结果含无效值，请检查输入是否为有效正数。」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "funeral/ceremony-timeline",
    "clicks": [
      "steps=[{id:1,time:'23:30',name:'签到',dur:20,desc:''},{id:2,time:'00:15',name:'告别',dur:30,desc:''}];render();var h=String(document.getElementById('timeline').innerHTML),s=String(document.getElementById('summary').innerHTML);document.getElementById('__tbProbe').textContent='CER='+((h.indexOf('23:30')>=0&&h.indexOf('23:30')<h.indexOf('00:15（次日）'))?'OK':'BAD')+' END='+(s.indexOf('00:45（次日）')>=0?'Y':'N');"
    ],
    "expect": ["CER=OK END=Y"],
    "ref": "修复前 render() 每次先用开始时间 09:00 覆盖手输时间、再按 HH:mm 字符串排序，跨午夜时次日 00:15 排到前一日 23:30 之前、结束时间也不带日偏移；现 render 不再覆盖手输时间，按录入顺序折算绝对分钟排序并标「（次日）」，末环节 23:30+20+30=次日 00:45。默认态无该探针串。"
  },
  {
    "slug": "funeral/reminder-3",
    "clicks": ["var d=getNextDate({type:'lunar',lYear:2020,lMonth:5,lDay:5,lLeap:false,yearly:false});var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/funeral/reminder-3.html','utf8');var ok=!!d&&d.getFullYear()===2020&&h.indexOf('if(lDay>(isLeap?leapDays(lYear):monthDays(lYear,lMonth)))return null;')>=0&&h.indexOf('lunarToSolar(it.lYear,lm,ld,leap)')>=0&&h.indexOf('y<=2099')>=0&&h.indexOf('now.getFullYear()+20')<0;document.getElementById('__tbProbe').textContent='LUNARREM '+(ok?'OK':'BAD '+String(d&&d.getFullYear()));"],
    "expect": ["LUNARREM OK"],
    "ref": "一次性农历提醒按添加时选定的原年计算（2020 年五月初五仍落 2020 年，旧版从当前年起找会落 2026 年）；每年重复的闰月搜索覆盖数据表至 2099 年；lunarToSolar 增加农历大小月校验，小月三十日不再悄悄换算到下月。默认态不产生该哨兵。"
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

  console.log("==== funeral calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
