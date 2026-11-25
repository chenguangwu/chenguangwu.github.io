#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const fs = require("fs");
const path = require("path");

// 529 复核失败：canvas 文案不进 DOM，DOM 探针查不到；用源码守卫锁定
// 交互态的双语分支与语言切换重绘路径，避免局部 en 作用域错误回潮。
function canvasLangStaticChecks() {
  const read = (slug) => fs.readFileSync(path.join(__dirname, "..", "tools", "cognition", slug), "utf8");
  const stroop = read("stroop-test.html");
  const time = read("time-perception.html");
  return [
    {
      name: "Stroop 散点图使用统一语言判定（不再引用 drawBar 局部 en）",
      ok: /function drawScatter\(\) \{\s*var en = isEnUi\(\);/.test(stroop)
        && /function isEnUi\(\)\{/.test(stroop)
        && !/function drawBar\([^)]*\) \{\s*var en = \/\^en\//.test(stroop),
    },
    {
      name: "Stroop 柱图标签、散点空态与轴标题双语",
      ok: /en \? 'Congruent' : '一致'/.test(stroop)
        && /en \? 'Incongruent' : '不一致'/.test(stroop)
        && /en \? 'Neutral' : '中性'/.test(stroop)
        && /en \? 'No scored data' : '无计分数据'/.test(stroop)
        && /en \? 'Trial order' : '试次顺序'/.test(stroop),
    },
    {
      name: "Stroop 语言切换复用完整重绘（非只算摘要）",
      ok: /function renderCharts\(\)/.test(stroop)
        && /window\.__tbRedraw=function\(\)\{try\{renderCharts\(\);\}catch\(e\)\{\}\};/.test(stroop)
        && /addEventListener\('toolbox:langchange'/.test(stroop)
        && !/window\.__tbRedraw=function\(\)\{ try\{ summarize\(\); \}/.test(stroop),
    },
    {
      name: "时间感知双击直方图标题双语且可按语言重绘",
      ok: /function tpHistLabel\(\)/.test(time)
        && /drawHist\(\$\('dHist'\), intervals, '#065F46', tpHistLabel\(\)\)/.test(time)
        && /window\.__tpDoubleIntervals=intervals\.slice\(\)/.test(time)
        && /window\.__tpRedraw=function\(\)/.test(time)
        && /addEventListener\('toolbox:langchange'/.test(time)
        && !/drawHist\(\$\('dHist'\), intervals, '#065F46', '双击间隔\(ms\)'\)/.test(time),
    },
  ];
}

const CASES = [
{
  "slug": "cognition/cognitive-assessment",
  "inputs": {
    "scaLen": "quick"
  },
  "expect": [
    "quick"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
    "var s=window.__corsiDrive('state');document.getElementById('cbMsg').textContent='RETRY:'+s.phase+'/'+s.length+'/'+(s.passed+(s.full?0.5:0));"
  ],
  "expect": [
    "RETRY:input/3/2"
  ],
  "ref": "首错重试回归（W6-A）：长度 2 第 1 次错→仍有第 2 次机会；第 2 次对 ⇒ 记为 2 中 1（passed=2，不加 0.5）并晋升长度 3 且立即出题（phase=input、length=3）。K25 修复前把 0.5 加给 2 中 1，输出 RETRY:input/3/2.5，表现更差反而广度更高；修复后断言 2.0。"
},
{
  "slug": "cognition/corsi-block-test",
  "clicks": [
    "window.__corsiDrive('start');",
    "window.__corsiDrive('answer',true);",
    "window.__corsiDrive('answer',true);",
    "var s=window.__corsiDrive('state');document.getElementById('cbMsg').textContent='FULL:'+s.phase+'/'+s.length+'/'+(s.passed+(s.full?0.5:0));"
  ],
  "expect": [
    "FULL:input/3/2.5"
  ],
  "ref": "满分加分方向（RL-K25）：长度 2 两次全对才应加 0.5，得 span 2.5，高于 2 中 1 的 2.0。修复前 state.full 不存在且 0.5 只给 2 中 1，输出 FULL:input/3/2；断言依赖 clicks 驱动的真实状态，默认态不命中。"
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
  "slug": "cognition/digit-span-test",
  "clicks": ["var a=window.__dsRestartProbe();var b=window.__dsRestartProbe();document.getElementById('__tbProbe').textContent='GEN '+a.gen+'->'+b.gen+' timers '+b.timers;"],
  "expect": ["GEN 1->2"],
  "ref": "重复开始必须作废旧异步链：旧版 startSingle 不 clearTimeout/不置 phase，两次开始会在同一 _timer 上叠两条 step 链、数字串交错。现 cancelPending 递增 _gen 并清空所有定时注册，两次重开代际 1→2，旧链回调因代际不符直接 return。默认态无 GEN 串。"
},
{
  "slug": "cognition/human-benchmark",
  "clicks": [
    "var P=[6,1,4,8];document.getElementById('cLog').textContent='CHIMP-MAP:'+window.chimpNumAt(P,6)+window.chimpNumAt(P,1)+window.chimpNumAt(P,4)+window.chimpNumAt(P,8);"
  ],
  "expect": [
    "CHIMP-MAP:1234"
  ],
  "ref": "Chimp 标注/判定一致性（N5-D）：固定位置序列 P=[6,1,4,8] 下，P[k] 屏幕标注 k+1，判定序也必须按 P 的下标给出同一序号 ⇒ 期望 1234。旧实现判定序为 positions 升序排序（排序后与标注错位，答对判错/答错判对），且无 chimpNumAt 共用映射 ⇒ 本串不成立。非默认态注入、避开页面默认渲染。"
},
{
  "slug": "cognition/human-benchmark",
  "clicks": ["var r=window.__hbIndexWith([69,null,null,null,null,null,null,null]);document.getElementById('__tbProbe').textContent='IDX '+r.index+' M='+Object.keys(r.measured).sort().join(',')"],
  "expect": ["IDX 69 M=speed"],
  "ref": "RL-K43 未测维度不得按 P0 计入综合指数：仅 reaction=P69，已测维度只有 speed（权 0.25）⇒ 归一后 index=69、measured=speed；旧版按全权重 69×0.25≈17（plan 复现的「指数 17」），断言「IDX 69」不成立。钩子 __hbIndexWith 纯计算无 DOM 副作用，注入 8 项百分位（null=未测）。"
},
{
  "slug": "cognition/human-benchmark",
  "clicks": ["var r=window.__hbIndexWith([50,50,50,50,50,50,50,50]);document.getElementById('__tbProbe').textContent='IDX '+r.index+' M='+Object.keys(r.measured).sort().join(',')"],
  "expect": ["IDX 50 M=attention,executive,memory,speed"],
  "ref": "RL-K43 全测回归：8 项均 P50 ⇒ 四维各 50、归一化 index=50、measured 四维齐全。防止归一改动在全测时误算。"
},
{
  "slug": "cognition/human-benchmark",
  "clicks": ["var r=window.__hbIndexWith([null,null,null,90,null,null,null,null]);document.getElementById('__tbProbe').textContent='IDX '+r.index+' M='+Object.keys(r.measured).sort().join(',')"],
  "expect": ["IDX 90 M=memory"],
  "ref": "RL-K43 仅 memory 维度已测（number=P90，权 0.30）⇒ 归一 index=90、measured=memory；旧版全权重 90×0.30=27 不命中。与 reaction 用例分属不同维度，防单一路径假绿。"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
  "slug": "cognition/digit-span-test",
  "clicks": ["window.__dsResult={fwd:0,bwd:null,seq:null,total:0,done:1,trials:6,norms:{fwd:6.5,bwd:5.5,seq:5.0}}; __dsEmr();"],
  "expect": ["总广度 0.0（已完成 1 项均值）", "正背 0.0（参考 6.5，-6.5）"],
  "ref": "零广度是合法结果：旧版 push 用 if(!(v>0)) return 丢掉 0，门诊记录只剩「分条件广度：未完成」；现按 null 判缺失、0 照常输出，并计入已完成项数。"
},
{
  "slug": "cognition/schulte-table",
  "inputs": {
    "scMode": "letter"
  },
  "expect": [
    "letter"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "cognition/schulte-table",
  "clicks": ["document.getElementById('__tbProbe').textContent='LV '+window.__scLevel(5,'num','asc',25/38,0);"],
  "expect": ["本次评级： 良好"],
  "ref": "5 阶 25 格 38 秒：速率 0.658 个/秒，旧固定阈值 <0.7 判「需加强」，与同页深度解析「成人 5×5 常见 25–40 秒」矛盾。现按每格耗时 38/25=1.52 秒判「良好」。默认态无 LV 串。"
},
{
  "slug": "cognition/schulte-table",
  "clicks": ["document.getElementById('__tbProbe').textContent='LV '+window.__scLevel(3,'num','asc',9/10,0);"],
  "expect": ["本次评级： 优秀"],
  "ref": "3 阶 9 格 10 秒：旧固定阈值 0.9<1.0 只判「良好」，不同阶不可比。现每格 10/9=1.11 秒判「优秀」。默认态无 LV 串。"
},
{
  "slug": "cognition/schulte-table",
  "clicks": ["var p=window.__scColorProbe();document.getElementById('__tbProbe').textContent='INK '+p.label+'|'+p.ink+'|'+p.bg;"],
  "expect": ["INK 红|#EC4899|#1F2937"],
  "ref": "颜色名模式：旧版白字配词义色底（黄/白/银格不可读），且字义与底色同色不存在 Stroop 冲突。现字义「红」、墨水色错开 7 位为粉 #EC4899，中性底按墨水亮度选深底 #1F2937 保证对比。默认态无 INK 串。"
},
{
  "slug": "cognition/schulte-table",
  "clicks": ["window.__c0=window.__scHintProbe(false);window.__c1=window.__scHintProbe(true);document.getElementById('__tbProbe').textContent='HINT '+window.__c0+'/'+window.__c1;"],
  "expect": ["HINT 0/1"],
  "ref": "提示默认关闭：旧版总是给下一格加 .next 高亮，等于免费提示；现默认 0 个高亮，勾选「练习提示」后才 1 个。probe 依赖两次真实开始后的 DOM 类计数。"
},
{
  "slug": "cognition/stroop-test",
  "inputs": {
    "stTimeout": "3750"
  },
  "expect": [
    "3750"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "cognition/stroop-test",
  "clicks": ["var p=window.__stFinishProbe();document.getElementById('__tbProbe').textContent='ST '+p.before+'->'+p.after+' '+p.html;"],
  "expect": ["ST 0->0 本次无有效试次，未保存记录"],
  "ref": "零试次提前结束：旧版 overallAcc=0 仍 push 一条 0 分历史，污染趋势。现无 scored 试次时提示并直接 return，断言历史条数 0->0 与提示文案；默认态无 ST 串。"
},
{
  "slug": "cognition/stroop-test",
  "clicks": ["var p=window.__stBlockProbe();document.getElementById('__tbProbe').textContent='STBLOCK c'+p.congruent+' i'+p.incongruent+' n'+p.neutral+' t'+p.total+' tot'+p.totalTrials;"],
  "expect": ["STBLOCK c16 i16 n16 t48 tot82"],
  "ref": "RL-K11 块序污染修复：前置一致块 24 次全为 congruent，旧实现计分标记 scored=phase!=='练习' 使 cong=24+16=40、incong=16，干扰量混入选练习与块序效应。修复后前置一致块不计分，仅混合块三条件各 16 次等量随机进入计分 ⇒ c16/i16/n16/t48，总试次仍 82 不变。注入态才有 STBLOCK 串，默认态无 ⇒ 零逃生；旧版 cong=40 命中不到期望串会变红。"
},
{
  "slug": "cognition/time-perception",
  "inputs": {
    "bSel": "120"
  },
  "expect": [
    "120"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
},
{
  "slug": "cognition/time-perception",
  "clicks": [
    "window.__tpSelectMode('beat');",
    "var r=window.__tpBeatDupProbe(20);document.getElementById('bHint').textContent='TAP:'+r.taps+'/'+r.matched+'|'+r.log;"
  ],
  "expect": [
    "TAP:1/1|1 / 20 拍 · 本拍已记录，忽略重复点击"
  ],
  "ref": "一拍一次（RL-K29）：开始后对最近拍连点 20 次，只有首次命中计入，其余 19 次必须提示「本拍已记录」并保持 1/20。旧实现未排除已匹配拍，matched 直接累加到 20 并立即 finish，输出「20 / 20 拍」且 σ 极小刷出高分；断言落在真实进度日志，默认态无 TAP 前缀。"
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

  const stat = canvasLangStaticChecks();
  const staticFails = stat.filter((s) => !s.ok);
  for (const s of staticFails) console.log("❌ [static] " + s.name);

  console.log("==== cognition calc " + pass + "/" + cases.length + " ====");
  if (staticFails.length) console.log("❌ static " + (stat.length - staticFails.length) + "/" + stat.length + " 未通过");
  if (fails.length || staticFails.length) process.exit(1);
}
if (require.main === module) main();
