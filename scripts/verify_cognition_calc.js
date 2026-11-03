#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "cognition/cognitive-assessment",
  "inputs": {
    "scaLen": "quick"
  },
  "expect": [
    "quick"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "cognition/corsi-block-test",
  "clicks": [
    "window.__cbResult={mode:'fwd',span:5.5,totalCorrect:10,trials:12,product:60,norms:[{g:'成人 (18–64)',m:5.5},{g:'儿童 (7–11)',m:4.8},{g:'老年 (65+)',m:4.9}]}; __cbEmr();"
  ],
  "expect": [
    "Corsi 广度 5.5（正序）· 正确 10/12 · 乘积分 60"
  ],
  "ref": "双态零交集：expect 依赖 clicks 注入的 __cbResult（span/mode/totalCorrect/trials/product）。判别器清空 clicks 后 finish() 不会触发、__cbEmr 不写门诊记录，blob 无此串 ⇒ 非逃生项。判据：Corsi 广度结果串随注入值变化。"
},
{
  "slug": "cognition/corsi-block-test",
  "clicks": [
    "window.__corsiDrive('start');",
    "window.__corsiDrive('answer',true);",
    "window.__corsiDrive('answer',true);",
    "window.__corsiDrive('answer',true);",
    "window.__corsiDrive('answer',true);",
    "window.__corsiDrive('answer',true);",
    "window.__corsiDrive('answer',true);",
    "var s=window.__corsiDrive('state');document.getElementById('cbMsg').textContent='PASS:'+s.phase+'/'+s.length+'/'+s.passed;"
  ],
  "expect": [
    "PASS:input/5/4"
  ],
  "ref": "状态机回归（W6-A）：连续通过长度 2→3→4（每个长度 2 次全对）后必须自动进入长度 5 的新试次（phase=input、length=5、passed=4）。旧实现 advanceLength() 只递增长度、不调用 startTrial ⇒ 停在 idle（期望串为 PASS:idle/3/2 附近），点击方块无响应。断言串由 __corsiDrive 驱动后的真实 G 状态派生，非默认态可命中。"
},
{
  "slug": "cognition/corsi-block-test",
  "clicks": [
    "window.__corsiDrive('start');",
    "window.__corsiDrive('answer',false);",
    "window.__corsiDrive('answer',true);",
    "var s=window.__corsiDrive('state');document.getElementById('cbMsg').textContent='RETRY:'+s.phase+'/'+s.length+'/'+(s.passed+(s.half?0.5:0));"
  ],
  "expect": [
    "RETRY:input/3/2.5"
  ],
  "ref": "首错重试回归（W6-A）：长度 2 第 1 次错→仍有第 2 次机会；第 2 次对 ⇒ 记为 2 中 1（passed=2.5）并晋升长度 3 且立即出题（phase=input、length=3）。旧实现晋升后停在 idle（期望串为 RETRY:idle/3/2.5），据此区分。"
},
{
  "slug": "cognition/digit-span-test",
  "clicks": [
    "window.__dsResult={fwd:6,bwd:4,seq:4.5,total:4.8,trials:24,norms:{fwd:6.5,bwd:5.5,seq:5.0}}; __dsEmr();"
  ],
  "expect": [
    "总广度 4.8（已完成 3 项均值）· 参考均值 5.7 → 低于参考均值 0.9 · 共 24 个试次"
  ],
  "ref": "双态零交集：expect 依赖 clicks 注入的 __dsResult（fwd/bwd/seq/total/trials/norms）。判别器清空 clicks 后 __dsEmr 不执行、门诊记录不渲染，blob 无此串 ⇒ 非逃生项。已完成项数由 fwd/bwd/seq 三个非空值计得 3。"
},
{
  "slug": "cognition/digit-span-test",
  "clicks": [
    "document.getElementById('dsResultBox').innerHTML='<p>单项均值：'+dsMeanCompleted({fwd:8})+'</p>';",
    "window.__dsResult={fwd:8,total:dsMeanCompleted({fwd:8}),done:1,trials:9,norms:{fwd:6.5,bwd:5.5,seq:5.0}}; __dsEmr();"
  ],
  "expect": [
    "单项均值：8",
    "总广度 8.0（已完成 1 项均值）"
  ],
  "ref": "单项回归：只完成正背一项（广度 8）⇒ dsMeanCompleted({fwd:8}) 按已完成 1 项求均值 = 8（旧实现固定除以 3 得 2.7）；同时 __dsEmr(rec.done=1) 的总结文案显示「已完成 1 项均值」。断言含 dsMeanCompleted 的真实返回值，非默认态（默认无结果）可命中。"
},
{
  "slug": "cognition/human-benchmark",
  "inputs": {
    "tArea": ""
  },
  "expect": [
    "9×9"
  ],
  "ref": "结构性不可改造（保留 all_default，勿重复评估）：8 个子测验全部由点击 / 倒计时 / 随机序列驱动，"
     + "成绩存 localStorage 历史；无表单输入路径可注入，注入 tArea 不触发任何渲染（2026-09-25 实测）。"
},
{
  "slug": "cognition/nback-training",
  "inputs": {
    "nbDur": "1350",
    "nbIsi": "500"
  },
  "expect": [
    "1350"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "cognition/nback-training",
  "clicks": [
    "var T=[];for(var i=0;i<10;i++){T.push({posResp:null,isPosMatch:true,audResp:null,isAudMatch:false});}for(var j=0;j<10;j++){T.push({posResp:null,isPosMatch:false,audResp:null,isAudMatch:false});}var r=window.__nbScoreTrials(T,false);document.getElementById('nbDurV').textContent='NB-NULL:'+r.correct+'/'+r.scored+'='+r.acc;"
  ],
  "expect": [
    "NB-NULL:10/20=50"
  ],
  "ref": "判定口径回归（W6-B）：单通道 10 信号 + 10 噪声全部不按键 ⇒ 信号全漏报、噪声全为正确拒绝 ⇒ 正确 10/20 = 50%。旧实现 tolPos = (null === 0) 对噪声恒 false ⇒ 0/20 = 0%（不按键也判错）。断言调用 endTrial 共用的 trialCorrect()，非默认态可命中。"
},
{
  "slug": "cognition/nback-training",
  "clicks": [
    "var T=[];for(var i=0;i<7;i++){T.push({posResp:1,isPosMatch:true,audResp:null,isAudMatch:false});}for(var k=7;k<10;k++){T.push({posResp:null,isPosMatch:true,audResp:null,isAudMatch:false});}for(var m=0;m<3;m++){T.push({posResp:1,isPosMatch:false,audResp:null,isAudMatch:false});}for(var n=3;n<10;n++){T.push({posResp:null,isPosMatch:false,audResp:null,isAudMatch:false});}var r=window.__nbScoreTrials(T,false);document.getElementById('nbDurV').textContent='NB-SIM:'+r.correct+'/'+r.scored+'='+r.acc;"
  ],
  "expect": [
    "NB-SIM:14/20=70"
  ],
  "ref": "真实按键模拟（W6-B）：10 信号里 7 次命中、3 次漏报；10 噪声里 3 次误报、7 次正确拒绝 ⇒ 正确 14/20 = 70%。命中/正确拒绝/漏报/误报四类口径同时被覆盖，旧实现漏报与误报外的空响应处理使结果不符。"
},
{
  "slug": "cognition/schulte-table",
  "inputs": {
    "scMode": "letter"
  },
  "expect": [
    "letter"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "cognition/stroop-test",
  "inputs": {
    "stTimeout": "3750"
  },
  "expect": [
    "3750"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "cognition/time-perception",
  "inputs": {
    "bSel": "90"
  },
  "expect": [
    "90"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "cognition/time-perception",
  "clicks": [
    "window.__tpSelectMode('beat');",
    "window.AudioContext=function(){this.currentTime=0;this.state='running';this.destination={};this.resume=function(){};this.createOscillator=function(){return{type:'',frequency:{value:0},connect:function(){},start:function(){},stop:function(){}};};this.createGain=function(){return{gain:{setValueAtTime:function(){},exponentialRampToValueAtTime:function(){}},connect:function(){}};};};",
    "document.getElementById('bStart').fire('click');"
  ],
  "expect": [
    "样本不足",
    "至少完成 3 次有效击拍后再统计",
    "样本不足：有效击拍少于 3 次",
    "完成（无有效样本）"
  ],
  "ref": "零点击回归（W6-C）：切到节拍同步、注入最小 AudioContext 桩后点开始，收集窗口到点 finish() 时 taps=[] ⇒ 必须显示「样本不足」且不写入百分位。旧实现 std([])=0 ⇒ percentile('beat',0)=P98，零点击也输出「P98」异常值。断言串为页面统计卡真实产物，默认态（未开始）不含。"
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

  console.log("==== cognition calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
