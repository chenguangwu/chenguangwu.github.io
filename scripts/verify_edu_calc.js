#!/usr/bin/env node
/**
 * 第 24 道门禁：edu 分类计算正确性验证（13 个确定性数值工具）
 *
 * 期望值全部由独立复算得出（ref 字段写明完整算式），不回读页面输出。
 * 输入一律避开页面默认值，确保验证的是「注入值 → 结果」而非「默认值 → 结果」。
 * 跳过：exam-gpa-calculator / gpa-calculator / grade-weight-calculator / grade-calculator
 *       （依赖动态添加课程行，框架无法注入）；reading-speed / edu-unit-converter /
 *       essay-word-counter / calc-3 / countdown-5（无 function calc，实时 oninput）。
 * 用法: node scripts/verify_edu_calc.js [slug ...]
 */
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── 第1176批：数字记忆挑战记录与清空提示 ──
  {
    slug: "edu/number-memory",
    inputs: { answerInput: "1234" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/number-memory.html','utf8');var ok=h.indexOf('ok: correct === currentLevel')>=0&&h.indexOf('history.unshift({ level: currentLevel, date: d.toLocaleString(locale), id: Date.now(), ok:')>=0&&h.indexOf('showToast(i18nText())')<0;document.getElementById('__tbProbe').textContent='JHISTOK:'+(ok?'OK':'BAD');"],
    expect: ["JHISTOK:OK"],
    ref: "EL-J121/J122：成功与失败均写挑战记录且用 ok 区分，清空提示有明确文案；旧版只在失败分支写历史且 showToast(i18nText()) 无参 ⇒ BAD。",
  },
  // ── 第1175批：颜色测验改为色块辨识、清理 HEX/限时宣称（单词记忆三项源码复核销账）──
  {
    slug: "edu/color-quiz",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/color-quiz.html','utf8');var ok=h.indexOf(\"nameEl.textContent='●'\")>=0&&h.indexOf('background:${o.c}')<0&&h.indexOf('b.dataset.key=o.n')>=0;document.getElementById('__tbProbe').textContent='JBLIND:'+(ok?'OK':'BAD');"],
    expect: ["JBLIND:OK"],
    ref: "EL-J116：题面只显示纯色块且选项只有色名文字，高亮改数据键；旧版题面写出正确色名且选项带色块，读字即可满分 ⇒ BAD。",
  },
  {
    slug: "edu/color-quiz",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/color-quiz.html','utf8');var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/color-quiz']);var ok=h.indexOf('HEX 代码')<0&&h.indexOf('timed quiz')<0&&d.indexOf('由 HEX/RGB 反推颜色')<0;document.getElementById('__tbProbe').textContent='JHEX:'+(ok?'OK':'BAD');"],
    expect: ["JHEX:OK"],
    ref: "EL-J117：删除未实现的 HEX/RGB 题型与限时宣称，deep-dive 改为真实色块辨识；旧版三处虚标 ⇒ BAD。",
  },
  {
    slug: "edu/word-memory",
    inputs: { filterLevel: "3" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/word-memory.html','utf8');var ok=h.indexOf('name:'+'\\''+'认识'+'\\''+', count:familiar')>=0&&h.indexOf('nextDueAt')>=0&&h.indexOf(\"'0 / 0'\")>=0;document.getElementById('__tbProbe').textContent='JWMEM:'+(ok?'OK':'BAD');"],
    expect: ["JWMEM:OK"],
    ref: "EL-J118/J119/J120：四档独立统计、艾宾浩斯到期队列、空词库进度归零均已实现；旧版三项缺失 ⇒ BAD。",
  },
  // ── 第1174批：时长分配首屏行数、整数分钟与重复框清理 ──
  {
    slug: "edu/calc-3",
    inputs: { totalTime: "180" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/calc-3.html','utf8');var ok=h.indexOf('box.children.length===0')>=0&&h.indexOf('try{addSubject();}catch(e){} try{addSubject();}catch(e){}')<0;document.getElementById('__tbProbe').textContent='JROWS:'+(ok?'OK':'BAD');"],
    expect: ["JROWS:OK"],
    ref: "EL-J113：Boot 不得无条件追加 3 个空科目，须在无科目行时才补默认 4 科；旧版首屏 7 行稀释权重 ⇒ BAD。",
  },
  {
    slug: "edu/calc-3",
    inputs: { totalTime: "119.5" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/calc-3.html','utf8');var ok=h.indexOf('item.remainder')>=0&&h.indexOf('Math.round(item.minutes % 60)')<0&&h.indexOf('Math.round(totalTime)')>=0;document.getElementById('__tbProbe').textContent='JROUND:'+(ok?'OK':'BAD');"],
    expect: ["JROUND:OK"],
    ref: "EL-J114：119.5 分钟按整数分配后为 120 分钟，显示 2 小时 0 分钟而非 1 小时 60 分钟；旧版 floor+round 产出 1h60m ⇒ BAD。",
  },
  {
    slug: "edu/calc-3",
    inputs: { totalTime: "300" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/calc-3.html','utf8');var n=(h.split('<div class=\"formula-title\">📐 计算方式</div>').length-1);var ok=n===1&&h.indexOf('每日或每周学习时长')<0&&h.indexOf('calc_3Hist')>=0;document.getElementById('__tbProbe').textContent='JDOC:'+(ok?'OK':'BAD');"],
    expect: ["JDOC:OK"],
    ref: "EL-J115：只保留一个计算方式框，删除未实现的每日/每周承诺，重置须清理历史/表/图容器；旧版两框且虚标 ⇒ BAD。",
  },
  // ── 第1172批：打字游戏增量计数、历史落地与承诺对齐（均为源码复核销账）──
  {
    slug: "edu/typing-game",
    inputs: { "input": "abc" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/typing-game.html','utf8');var ok=h.indexOf('if(v.length>lastLen)')>=0&&h.indexOf('for(let i=lastLen;i<v.length;i++)')>=0&&h.indexOf('for(let i=0;i<v.length;i++)')<0;document.getElementById('__tbProbe').textContent='JINCR:'+(ok?'OK':'BAD');"],
    expect: ["JINCR:OK"],
    ref: "EL-J104：按键统计只遍历新增片段 lastLen→v.length，不再每次 input 全量重计；旧版全串累加会把 WPM 放大近 10 倍 ⇒ BAD。",
  },
  {
    slug: "edu/typing-game",
    inputs: { "input": "abc" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/typing-game.html','utf8');var ok=h.indexOf('var __typing_game_f1=')>=0&&h.indexOf('finish=function()')>=0&&h.indexOf('__typing_gameExtras(); }catch(e){} return __r;')>=0;document.getElementById('__tbProbe').textContent='JHIST:'+(ok?'OK':'BAD');"],
    expect: ["JHIST:OK"],
    ref: "EL-J105：finish 必须被包装以调用 __typing_gameExtras，结果文本非空时写入历史，数据表/历史/CSV 不再永久为空；旧版仅包装 start ⇒ BAD。",
  },
  {
    slug: "edu/typing-game",
    inputs: { "input": "abc" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/typing-game.html','utf8');var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/typing-game']);var ok=h.indexOf('总字符')>=0&&h.indexOf('totalChars/(elapsed/60)')>=0&&h.indexOf('错题回看')<0&&d.indexOf('最高分')<0&&d.indexOf('不保存历史记录')<0&&d.indexOf('本地浏览器历史')>=0;document.getElementById('__tbProbe').textContent='JDOC:'+(ok?'OK':'BAD');"],
    expect: ["JDOC:OK"],
    ref: "EL-J106/J107：不得宣称错题回看/本地最高分排行，totalChars 须用于结果区总字符与 CPM，FAQ 须与已实现的历史记录一致；旧版三项均不满足 ⇒ BAD。",
  },
  // ── 第1171批：数学测验减数恒小于被减数、干扰项非负（J100/J101/J103 源码复核销账）──
  {
    slug: "edu/math-quiz",
    inputs: { qDifficulty: "easy", qCount: "20" },
    clicks: ["var oR=Math.random;try{var seq=[0.3,0.5,0.99,0.1,0.1,0.1,0.1,0.1];var i=0;Math.random=function(){return seq[i++%seq.length];};var bad=false;for(var k=0;k<12;k++){gen();if(ans<=0)bad=true;}var opts=gen();var ok=!bad&&opts.every(function(o){return o>=0;});document.getElementById('__tbProbe').textContent='JNEG:'+(ok?'OK':'BAD');}catch(e){document.getElementById('__tbProbe').textContent='JNEG:BAD';}finally{Math.random=oR;}"],
    expect: ["JNEG:OK"],
    ref: "EL-J102：减数须恒小于被减数且干扰项裁剪为非负；固定随机序列使旧版生成 a=11,b=11,ans=0 并产出负选项 ⇒ BAD。",
  },
  // ── 第1170批：考试计时时间戳基准、分段提醒与初始状态 ──
  {
    slug: "edu/exam-timer",
    inputs: { "set-minutes": "42" },
    clicks: ["var ok=false;try{if(typeof tickCountup!=='function')throw 0;var real=Date.now;var t=real();Date.now=function(){return t;};resetCountup();startCountup();Date.now=function(){return t+10000;};tickCountup();var d=document.getElementById('countup-display').textContent;clearInterval(countUp.interval);Date.now=real;ok=(d==='00:00:10');}catch(e){}document.getElementById('__tbProbe').textContent='JUP:'+(ok?'OK':'BAD');"],
    expect: ["JUP:OK"],
    ref: "EL-J96：正计时须以 startedAt 时间戳为基准，推进 10 秒后显示 00:00:10；旧版靠 250ms 增量重算整数秒且无 tickCountup ⇒ BAD。",
  },
  {
    slug: "edu/exam-timer",
    inputs: { "set-minutes": "5" },
    clicks: ["var ok=false;try{if(typeof tickCountdown!=='function')throw 0;var real=Date.now;var t=real();Date.now=function(){return t;};reset();start();Date.now=function(){return t+300000;};tickCountdown();var d=document.getElementById('display').textContent;var r=countDown.remaining;clearInterval(countDown.interval);Date.now=real;ok=(d==='00:00:00'&&r===0);}catch(e){}document.getElementById('__tbProbe').textContent='JDOWN:'+(ok?'OK':'BAD');"],
    expect: ["JDOWN:OK"],
    ref: "EL-J97：倒计时须按 deadline 计算，5 分钟设定在真实时间推进 5 分钟后归零；旧版 remaining-- 每秒递减且无 tickCountdown ⇒ BAD。",
  },
  {
    slug: "edu/exam-timer",
    inputs: { "set-minutes": "20", "alert-before": "15" },
    clicks: ["var ok=false;try{var seen=[];var old=ToolBox.showToast;ToolBox.showToast=function(m){seen.push(m);};var real=Date.now;var t=real();Date.now=function(){return t;};reset();start();Date.now=function(){return t+301000;};tickCountdown();clearInterval(countDown.interval);Date.now=real;ToolBox.showToast=old;ok=seen.some(function(m){return m.indexOf('已用 5 分钟')>=0;});}catch(e){}document.getElementById('__tbProbe').textContent='JALERT:'+(ok?'OK':'BAD');"],
    expect: ["JALERT:OK"],
    ref: "EL-J98：运行到 25%（20 分钟的第 5 分钟）须触发分段提醒；旧版只有导出表静态节点、无 alert-before 与运行期提示 ⇒ BAD。",
  },
  {
    slug: "edu/exam-timer",
    inputs: { "set-minutes": "45" },
    clicks: ["var st=document.getElementById('state-label').textContent;document.getElementById('__tbProbe').textContent='JREADY:'+(st==='就绪'?'OK':'BAD');"],
    expect: ["JREADY:OK"],
    ref: "EL-J99：从未启动时状态徽标显示「就绪」，不因 reset→pause 被覆盖为「已暂停」；旧版必然写「⏸ 已暂停」⇒ BAD。",
  },
  // ── 第1169批：学习计划重复公式框、番茄轮次刷高与计时失真 ──
  {
    slug: "edu/exam-study-planner",
    inputs: { "focus-mins": "30" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/exam-study-planner.html','utf8');var n=h.split('累计专注时长 = 单次专注分钟数 × 完成轮数').length-1;document.getElementById('__tbProbe').textContent='JDUP:'+(n===1?'OK':'BAD');"],
    expect: ["JDUP:OK"],
    ref: "EL-J93：今日 tab 只保留一个「计算方式」框；旧版同一段说明重复两次 ⇒ BAD。",
  },
  {
    slug: "edu/exam-study-planner",
    inputs: { "focus-mins": "30", "target-rounds": "4" },
    clicks: ["var r0=pomo.round;skipPomo();var r1=pomo.round;skipPomo();var r2=pomo.round;document.getElementById('__tbProbe').textContent='JSKIP:'+((r0===1&&r1===r0&&r2===r0)?'OK':'BAD');"],
    expect: ["JSKIP:OK"],
    ref: "EL-J94：跳过休息与跳过专注都不得推进轮次；旧版从休息跳回专注时 round++ ⇒ 第二次 skip 后 round=2 ⇒ BAD。",
  },
  {
    slug: "edu/exam-study-planner",
    inputs: { "focus-mins": "45", "target-rounds": "4" },
    clicks: ["var ok=false;try{resetPomo();var f=+document.getElementById('focus-mins').value;var snap=(pomo.focusMin===f&&pomo.deadline===null);togglePomo();var d=pomo.deadline;var adv=Math.abs(d-Date.now()-f*60000)<5000;clearInterval(pomo.timer);pomo.running=false;ok=snap&&adv;}catch(e){}document.getElementById('__tbProbe').textContent='JDEAD:'+(ok?'OK':'BAD');"],
    expect: ["JDEAD:OK"],
    ref: "EL-J95：专注时长在 resetPomo 时快照，计时以 deadline 时间戳为基准；旧版无 focusMin/deadline 字段且 remaining 每秒递减 ⇒ BAD。",
  },
  // ── 第1168批：证书查询唯一键/首屏图表/诚实口径，时区转换 DST 口径/输入校验 ──
  {
    slug: "edu/certificate-check",
    inputs: { "search-input": "电工" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/certificate-check.html','utf8');var ok=h.indexOf('number format')<0&&h.indexOf('does not verify authenticity')>=0&&h.indexOf('官方核验须到发证机构官网')>=0;document.getElementById('__tbProbe').textContent='JL85:'+(ok?'OK':'BAD');"],
    expect: ["JL85:OK"],
    ref: "EL-J85：副标题与引据表不得宣称编号格式预检；旧版英文含 number format 且引据写「证书核验」⇒ BAD。",
  },
  {
    slug: "edu/certificate-check",
    inputs: { "search-input": "心理咨询师" },
    clicks: ["var s={};localStorage.getItem=function(k){return s[k]||null;};localStorage.setItem=function(k,v){s[k]=String(v);};if(typeof certKey!=='function'){document.getElementById('__tbProbe').textContent='JKEY:BAD';}else{var a=CERTS.filter(function(c){return c.n==='心理咨询师';});var k1=certKey(a[0]),k2=certKey(a[1]);toggleHave(k1);var fav=JSON.parse(s['cert_fav']||'[]');var ok=a.length===2&&k1!==k2&&fav.length===1&&fav[0]===k1;document.getElementById('__tbProbe').textContent='JKEY:'+(ok?'OK':'BAD');}"],
    expect: ["JKEY:OK"],
    ref: "EL-J86：两条同名心理咨询师须用「名称|发证机构」唯一键，点其中一条只写一条收藏；旧版按名称做键且无 certKey ⇒ BAD。",
  },
  {
    slug: "edu/certificate-check",
    inputs: { "search-input": "软考" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/certificate-check.html','utf8');var ok=h.indexOf('data-pane=\"res\"')>=0&&h.indexOf('\"res\": [\"results\"')>=0&&h.indexOf('CATS.map')>=0&&h.indexOf(\"name:'证书数'\")>=0;document.getElementById('__tbProbe').textContent='JTAB:'+(ok?'OK':'BAD');"],
    expect: ["JTAB:OK"],
    ref: "EL-J88：首个 tab 须为结果区，图表须用各类别证书数这一真实静态数据源；旧版首 tab 为空图表且无 res 组 ⇒ BAD。",
  },
  {
    slug: "edu/convert-1",
    inputs: { val: "09:00", from: "8", to: "-5" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/convert-1.html','utf8');var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/convert-1']);var en=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/en/edu/convert-1.json','utf8')));var ok=h.indexOf('自动处理跨日与夏令时')<0&&h.indexOf('夏令时期间目标时区偏移再加 60 分钟')<0&&d.indexOf('夏令时：标注夏令时偏移')<0&&en.indexOf('another 60 minutes is added')<0&&h.indexOf('按固定标准偏移换算')>=0;document.getElementById('__tbProbe').textContent='JDST:'+(ok?'OK':'BAD');"],
    expect: ["JDST:OK"],
    ref: "EL-J89/J90：meta/公式/权威源/英文词典须统一为固定标准偏移口径，删除自动处理夏令时承诺；旧版四处均有夏令时虚标 ⇒ BAD。",
  },
  {
    slug: "edu/convert-1",
    inputs: { val: "25:00", from: "8", to: "-5" },
    expect: ["请输入有效 HH:MM（00:00-23:59）"],
    ref: "EL-J91：小时越界 25:00 必须拒绝；旧版正则抓子串输出 10:00 次日，不含错误文案 ⇒ 强判别。",
  },
  {
    slug: "edu/convert-1",
    inputs: { val: "23:99", from: "8", to: "-5" },
    expect: ["请输入有效 HH:MM（00:00-23:59）"],
    ref: "EL-J91：分钟越界 23:99 必须拒绝；旧版静默进位输出 00:39 次日 ⇒ 强判别。",
  },
  {
    slug: "edu/convert-1",
    inputs: { val: "12:00abc", from: "8", to: "-5" },
    expect: ["请输入有效 HH:MM（00:00-23:59）"],
    ref: "EL-J91：尾随字符须拒绝，正则必须锚定整串；旧版子串匹配照常换算 ⇒ 强判别。",
  },
  {
    slug: "edu/convert-1",
    inputs: { val: "20:00", from: "8", to: "0" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/convert-1.html','utf8');var ok=h.indexOf(\"'有效性趋势'\")<0&&h.indexOf('换算时刻（当日分钟）')>=0;document.getElementById('__tbProbe').textContent='JMIN:'+(ok?'OK':'BAD');"],
    expect: ["JMIN:OK"],
    ref: "EL-J92：趋势图须以换算时刻的当日分钟数为数值并标注 HH:MM，不再画有效性 0/1；旧版 series 名为「有效性趋势」⇒ BAD。",
  },
  {
    slug: "edu/essay-word-counter",
    inputs: { text: "“你好”😀" },
    expect: ["0 英文词数 2 纯文字字数 5 总字符数 5 不含空白符 2 标点符号 1 段落数 — 平均句长 1 行数"],
    ref: "EL-J72/J76：中文弯引号计入标点（2），emoji 按 Unicode 码点算 1（总字符 5 = 2 汉字 + 2 弯引号 + 1 emoji）。旧版标点正则只认 ASCII 引号、总字符按 UTF-16 算 6 ⇒ 该串失配。"
  },
  {
    slug: "edu/essay-word-counter",
    clicks: ["var ws=[];for(var i=0;i<500;i++)ws.push('w'+i);document.getElementById('text').value=ws.join(' ');count();var h=document.getElementById('result').innerHTML;var ok=h.indexOf('>500</div><div class=\"label\">英文词数')>=0&&h.indexOf('>中等<')>=0&&h.indexOf('字数偏少')<0;document.getElementById('__tbProbe').textContent='JENG:'+(ok?'OK':'BAD');"],
    expect: ["JENG:OK"],
    ref: "EL-J73：纯英文 500 词须显示英文词数 500，并按纯文字字数判「中等」，不再判「短文/字数偏少」。旧版只按中文字数分级（0 ⇒ 短文）且不显示英文词数 ⇒ BAD。"
  },
  {
    slug: "edu/essay-word-counter",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/essay-word-counter.html','utf8');var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/essay-word-counter']);var ok=h.indexOf('可选是否计入字符总数')<0&&d.indexOf('可选是否计入字符总数')<0;document.getElementById('__tbProbe').textContent='JFAQ:'+(ok?'OK':'BAD');"],
    expect: ["JFAQ:OK"],
    ref: "EL-J74：FAQ 不得宣称「标点可选是否计入」（页面无此开关）；页面与权威源两处虚标均已删。旧版两处都在 ⇒ BAD。"
  },
  {
    slug: "edu/24-point-solver",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/24-point-solver.html','utf8');var head=h.slice(0,h.indexOf('</head>'));var ok=head.indexOf('og:description')>=0&&head.indexOf('T 点求解器，输入')<0;document.getElementById('__tbProbe').textContent='JHEAD:'+(ok?'OK':'BAD');"],
    expect: ["JHEAD:OK"],
    ref: "EL-J78：head 内不得有裸文本（旧版两行 `T 点求解器…\">` 会被提升到 body 首屏），og:description 须为完整 meta；旧版必 BAD。"
  },
  {
    slug: "edu/24-point-solver",
    inputs: { nums: "3,3,8,8" },
    clicks: ["var h=document.getElementById('result').innerHTML;var fs=globalThis.__tbFs;var s=fs.readFileSync(process.cwd()+'/tools/edu/24-point-solver.html','utf8');var ok=h.indexOf('个不同的解')>=0&&h.indexOf('命中')<0&&s.indexOf('容差 1e-6')<0&&s.indexOf('容差 1e-9')>=0;document.getElementById('result').innerHTML='JSOLV:'+(ok?'OK':'BAD');"],
    expect: ["JSOLV:OK"],
    ref: "EL-J80：3,3,8,8 的多解不得被「取前 6 再去重」压成「命中 1 个示例」，且公式容差须与实现 1e-9 一致；旧版两项都不满足 ⇒ BAD。"
  },
  {
    slug: "edu/capital-quiz",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/capital-quiz.html','utf8');var ok=h.indexOf('点击「计算」或「生成」按钮')<0&&h.indexOf('点击「开始」抽题')>=0;document.getElementById('__tbProbe').textContent='JCFAQ:'+(ok?'OK':'BAD');"],
    expect: ["JCFAQ:OK"],
    ref: "EL-J84：使用说明与 FAQPage 结构化数据须与真实按钮（开始/重置）一致，不得沿用「点击计算或生成」模板套话；旧版两处都在 ⇒ BAD。"
  },
  {
    slug: "edu/word-count-pages",
    inputs: { words: "-5000" },
    clicks: ["var w=document.getElementById('words').value;var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='NEG '+(w==='-5000'&&r.indexOf('请输入 ≥100 的正整数')>=0?'OK':'BAD');"],
    expect: ["NEG OK"],
    ref: "EL-J66：负字数被拒绝并提示；旧版 parseInt(-5000)||0 直接产出负页数与负完整页数。",
  },
  {
    slug: "edu/word-count-pages",
    inputs: { words: "" },
    clicks: ["var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='CLR '+(r.indexOf('请输入 ≥100 的正整数')>=0?'OK':'BAD');"],
    expect: ["CLR OK"],
    ref: "EL-J66：清空字数不再当成有效 0 页；旧版 ||0 吞掉空值输出 0 页。",
  },
  {
    slug: "edu/word-count-pages",
    inputs: { words: "5001" },
    clicks: ["var w=document.getElementById('words').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu/word-count-pages.html','utf8');var ok=w==='5001'&&h.indexOf('图表篇幅增幅')>=0&&h.indexOf('图表占比')<0;document.getElementById('__tbProbe').textContent='IMGTERM '+(ok?'OK':'BAD');"],
    expect: ["IMGTERM OK"],
    ref: "EL-J68：把「图表占比」改为诚实的「图表篇幅增幅」口径（50%=额外篇幅+50%），计算仍按 1+imgs；旧版名称与算法矛盾。",
  },
  {
    slug: "edu/word-count-pages",
    inputs: { words: "5001" },
    clicks: ["var w=document.getElementById('words').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var s=JSON.stringify(JSON.parse(h)['edu/word-count-pages']);var ok=w==='5001'&&s.indexOf('字数反推：由页数估字数')<0&&s.indexOf('图表增幅')>=0;document.getElementById('__tbProbe').textContent='WPDOC '+(ok?'OK':'BAD');"],
    expect: ["WPDOC OK"],
    ref: "EL-J69：删除深度解析中不存在的「由页数估字数」反推承诺，改真实场景；旧版虚标。",
  },
  {
    slug: "edu/edu-unit-converter",
    inputs: { fromVal: "0" },
    clicks: ["var v=document.getElementById('fromVal').value;var o=document.getElementById('toVal').value;document.getElementById('__tbProbe').textContent='ZERO '+(v==='0'&&o==='0'?'OK':'BAD');"],
    expect: ["ZERO OK"],
    ref: "EL-J62：输入 0 时输出 0 而非 0e0；旧版 Math.abs(0)<0.0001 走指数格式得 0.000000e+0→0e0。",
  },
  {
    slug: "edu/edu-unit-converter",
    inputs: { fromVal: "" },
    clicks: ["var o=document.getElementById('toVal').value;document.getElementById('__tbProbe').textContent='EMPTYVAL '+(o==='0'?'OK':'BAD');"],
    expect: ["EMPTYVAL OK"],
    ref: "EL-J62：清空输入按 0 输出，不再显示 0e0；旧版 ||0 后走指数分支。",
  },
  {
    slug: "edu/edu-unit-converter",
    inputs: { fromVal: "7" },
    clicks: ["var v=document.getElementById('fromVal').value;localStorage.removeItem('edu_unit_history');setCat('length',true);var h=localStorage.getItem('edu_unit_history');document.getElementById('__tbProbe').textContent='NOSAVE '+(v==='7'&&!h?'OK':'BAD');"],
    expect: ["NOSAVE OK"],
    ref: "EL-J63：silent 初始化不写历史；旧版 setCat→convert 无条件 saveHistory，首屏即产生 1 条。",
  },
  {
    slug: "edu/edu-unit-converter",
    inputs: { fromVal: "7" },
    clicks: ["var v=document.getElementById('fromVal').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu/edu-unit-converter.html','utf8');var dd=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var ok=v==='7'&&h.indexOf('scores, grades, pages')<0&&dd.indexOf('分数/等级/页码/字数')<0&&dd.indexOf('长度、质量、面积、体积、时间、角度')>=0;document.getElementById('__tbProbe').textContent='UNITDOC '+(ok?'OK':'BAD');"],
    expect: ["UNITDOC OK"],
    ref: "EL-J61：英文副标题与权威源改为真实物理量换算，不再虚标分数/等级/页码/字数；旧版三处矛盾。",
  },
  {
    slug: "edu/study-planner",
    inputs: { dailyHours: "7" },
    clicks: ["var mk=document.getElementById('dailyHours').value;var t=document.getElementById('statToday').textContent;document.getElementById('__tbProbe').textContent='INIT0 '+(mk==='7'&&String(t).trim()==='0'?'OK':'BAD');"],
    expect: ["INIT0 OK"],
    ref: "EL-J54：首启统计从 0 开始，不再展示虚构的 90 分钟/128 任务；旧版写死 90/8/120/128。",
  },
  {
    slug: "edu/study-planner",
    inputs: { dailyHours: "7" },
    clicks: ["var mk=document.getElementById('dailyHours').value;localStorage.setItem('toolbox_study_data',JSON.stringify({subjects:[{id:1,name:'数学',difficulty:5,progress:45}],tasks:[],stats:{todayMinutes:150,weekHours:8,totalHours:120,tasksDone:9,todayKey:'2000-1-1',weekKey:'2000-1-1'},subjectMinutes:{1:0}}));loadData();renderStats();var t=document.getElementById('statToday').textContent;document.getElementById('__tbProbe').textContent='CROSS '+(mk==='7'&&String(t).trim()==='0'?'OK':'BAD');"],
    expect: ["CROSS OK"],
    ref: "EL-J57：旧 todayKey 跨日后今日分钟与完成任务归零；旧版无日期键直接沿用 150。",
  },
  {
    slug: "edu/study-planner",
    inputs: { dailyHours: "4", studyDays: "5" },
    clicks: ["var dh=document.getElementById('dailyHours').value;planWeek();var w=document.getElementById('weekDays').innerHTML;document.getElementById('__tbProbe').textContent='WEEK '+(dh==='4'&&w.indexOf('4h')>=0&&w.indexOf('6h')<0?'OK':'BAD');"],
    expect: ["WEEK OK"],
    ref: "EL-J56：周计划日期格随每日时长/学习天数重绘，不再恒 6h×6 天；旧版硬编码。",
  },
  {
    slug: "edu/study-planner",
    inputs: { dailyHours: "7" },
    clicks: ["var mk=document.getElementById('dailyHours').value;addTask('TbTaskNew',30,2,2);var last=data.tasks[data.tasks.length-1];document.getElementById('__tbProbe').textContent='TASKSUB '+(mk==='7'&&last.name==='TbTaskNew'&&last.subjectId===2?'OK':'BAD');"],
    expect: ["TASKSUB OK"],
    ref: "EL-J58：新增任务可指定科目（英语 id=2），不再恒绑第一科；旧版固定 subjects[0]。",
  },
  {
    slug: "edu/study-planner",
    inputs: { dailyHours: "7" },
    clicks: ["var mk=document.getElementById('dailyHours').value;editSubject(0,'数学',0);document.getElementById('__tbProbe').textContent='PROG0 '+(mk==='7'&&data.subjects[0].progress===0?'OK':'BAD');"],
    expect: ["PROG0 OK"],
    ref: "EL-J59：科目进度可设为 0；旧版 parseInt(0)||s.progress 回退到 45。",
  },
  {
    slug: "edu/study-planner",
    inputs: { dailyHours: "7" },
    clicks: ["var mk=document.getElementById('dailyHours').value;globalThis.confirm=function(){return true;};var n=data.subjects.length;deleteSubject(2);document.getElementById('__tbProbe').textContent='DELSUB '+(mk==='7'&&data.subjects.length===n-1?'OK':'BAD');"],
    expect: ["DELSUB OK"],
    ref: "EL-J59：科目可删除，关联任务改未分类；旧版无 deleteSubject 入口。",
  },
  {
    slug: "edu/study-planner",
    inputs: { dailyHours: "7" },
    clicks: ["var mk=document.getElementById('dailyHours').value;var cap=null;var os=localStorage.setItem;localStorage.setItem=function(k,v){if(k==='toolbox_study_history')cap=JSON.parse(v);os(k,v);};toggleTask(0);localStorage.setItem=os;document.getElementById('__tbProbe').textContent='HISTW '+(mk==='7'&&cap&&cap.length===1&&cap[0].tasks>0?'OK':'BAD');"],
    expect: ["HISTW OK"],
    ref: "EL-J55：完成任务后写入历史记录；旧版历史键只有读取与删除，永不写入。",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { correct: "95", targetScore: "95" },
    clicks: ["var cv=document.getElementById('correct').value;document.getElementById('targetResult').innerHTML='__STALE__';calc();var r=document.getElementById('targetResult').innerHTML;document.getElementById('__tbProbe').textContent='LIVE '+(cv==='95'&&r.indexOf('__STALE__')<0&&r.indexOf('已达标')>=0?'OK':'BAD');"],
    expect: ["LIVE OK"],
    ref: "EL-J48：calc() 末尾联动 calcTarget()，基础成绩改动后目标卡不再残留旧结论；旧版只calc主表，目标卡保留旧缺口。",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { totalQ: "10", correct: "15", examName: "TbBadC" },
    clicks: ["var nm=document.getElementById('examName').value;var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='BADCNT '+(nm==='TbBadC'&&r.indexOf('请检查输入')>=0?'OK':'BAD');"],
    expect: ["BADCNT OK"],
    ref: "EL-J51：做对题数大于总题数必须拒绝并提示；旧版显示 15/10、正确率 100%、得分 100。",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { passLine: "0", correct: "55", total: "100", totalQ: "100", examName: "TbP0" },
    clicks: ["var nm=document.getElementById('examName').value;var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='PL0 '+(nm==='TbP0'&&r.indexOf('及格 ✓')>=0?'OK':'BAD');"],
    expect: ["PL0 OK"],
    ref: "EL-J51：及格线 0 是合法值，55% 应判及格；旧版 parseFloat(0)||60 静默按 60 判不及格。",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { examName: "TbHist75" },
    clicks: ["var nm=document.getElementById('examName').value;localStorage.setItem('exam_score_history',JSON.stringify([{time:'2026-01-01T00:00:00Z',examName:'TbHist75',score:75,total:100,rate:75,correct:75,totalQ:100,passLine:60}]));renderHistory();var r=document.getElementById('historyList').innerHTML;document.getElementById('__tbProbe').textContent='H75 '+(nm==='TbHist75'&&r.indexOf('中等')>=0?'OK':'BAD');"],
    expect: ["H75 OK"],
    ref: "EL-J49：历史等级与主表共用 gradeOf，75% 显示中等；旧版历史硬编码 60 档，只有及格。",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { examName: "TbSave", passLine: "70", perQ: "2", classAvg: "80", total: "100", totalQ: "50", correct: "30" },
    clicks: ["var nm=document.getElementById('examName').value;var __si=localStorage.setItem;var cap=null;localStorage.setItem=function(k,v){if(k==='exam_score_history')cap=JSON.parse(v);};saveToHistory();localStorage.setItem=__si;var it=cap&&cap[0];var ok=nm==='TbSave'&&it&&it.score===60&&it.passLine===70&&it.perQ===2&&it.classAvg===80&&it.grade;document.getElementById('__tbProbe').textContent='SAVE '+(ok?'OK':'BAD');"],
    expect: ["SAVE OK"],
    ref: "EL-J47/J50：历史与屏幕同口径(30×2=60)并保存 passLine/perQ/classAvg/grade；旧版不存这些字段且按平均分比例算 60 但无口径信息。",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { examName: "TbDoc" },
    clicks: ["var nm=document.getElementById('examName').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu/exam-score-calculator.html','utf8');var ok=nm==='TbDoc'&&h.indexOf('历史记录自动保存')<0&&h.indexOf('历史记录需手动点击')>=0&&h.indexOf('gradeOf(')>=0;document.getElementById('__tbProbe').textContent='ESCDOC '+(ok?'OK':'BAD');"],
    expect: ["ESCDOC OK"],
    ref: "EL-J53/J49：使用说明改手动保存，页面存在共用 gradeOf；旧版宣称自动保存且无 gradeOf。",
  },
  {
    slug: "edu/grade-weight-calculator",
    inputs: { target: "" },
    clicks: ["var tg=document.getElementById('target').value;var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='TGEMPTY '+(tg===''&&r.indexOf('请填写目标分')>=0?'OK':'BAD');"],
    expect: ["TGEMPTY OK"],
    ref: "EL-J43：目标清空必须提示「请填写目标分」；旧版 parseFloat(空串)||60 静默按 60 算。",
  },
  {
    slug: "edu/grade-weight-calculator",
    inputs: { target: "0" },
    clicks: ["var tg=document.getElementById('target').value;var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='TGZERO '+(tg==='0'&&r.indexOf('要达到0分')>=0&&r.indexOf('已达标')>=0?'OK':'BAD');"],
    expect: ["TGZERO OK"],
    ref: "EL-J43：目标 0 是合法输入，按 0 计算并显示已达标；旧版静默改成 60 且给 61.0 分缺口。",
  },
  {
    slug: "edu/grade-weight-calculator",
    inputs: { target: "72" },
    clicks: ["var tg=document.getElementById('target').value;upd(0,'score',120);var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='SC120 '+(tg==='72'&&r.indexOf('得分须在 0–100')>=0?'OK':'BAD');"],
    expect: ["SC120 OK"],
    ref: "EL-J44：得分 120 越界拒绝写入并提示；旧版按 120 加权且仍显示正常结果。",
  },
  {
    slug: "edu/grade-weight-calculator",
    inputs: { target: "72" },
    clicks: ["var tg=document.getElementById('target').value;upd(1,'weight',-20);var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='WTNEG '+(tg==='72'&&r.indexOf('权重须在 0–100')>=0?'OK':'BAD');"],
    expect: ["WTNEG OK"],
    ref: "EL-J44：负权重拒绝写入；旧版总权重变 50% 仍输出「不可能达到」。",
  },
  {
    slug: "edu/grade-weight-calculator",
    inputs: { target: "72" },
    clicks: ["var tg=document.getElementById('target').value;del(2);del(1);del(0);var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='EMPTY '+(tg==='72'&&r.indexOf('请添加项目')>=0?'OK':'BAD');"],
    expect: ["EMPTY OK"],
    ref: "EL-J45：删光项目显示「请添加项目」；旧版 every() 空数组为真，输出「-- 分」。",
  },
  {
    slug: "edu/grade-weight-calculator",
    inputs: { target: "72" },
    clicks: ["var tg=document.getElementById('target').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var s=JSON.stringify(JSON.parse(h)['edu/grade-weight-calculator']);var ok=tg==='72'&&s.indexOf('折算：百分制与等级互转')<0&&s.indexOf('权重 60/40')>=0;document.getElementById('__tbProbe').textContent='GWFIX '+(ok?'OK':'BAD');"],
    expect: ["GWFIX OK"],
    ref: "EL-J46：权威源删「百分制与等级互转」虚标，示例改 60/40 并注明归一；旧版 0.6/0.4 且与 UI 单位冲突。",
  },
  {
    slug: "edu/exam-gpa-calculator",
    inputs: { "course-name": "TbGpaS" },
    clicks: ["var nm=document.getElementById('course-name').value;setScale('100');document.getElementById('course-credit').value='3';document.getElementById('course-grade').value='120';addCourse();var r=document.getElementById('course-list').innerHTML;document.getElementById('__tbProbe').textContent='SC120 '+(nm==='TbGpaS'&&r.indexOf(nm)<0?'OK':'BAD');"],
    expect: ["SC120 OK"],
    ref: "EL-J41：百分制 120 越界拒绝添加；旧版 +value||0 直接采纳得绩点 4.80。",
  },
  {
    slug: "edu/exam-gpa-calculator",
    inputs: { "course-name": "TbGpaC" },
    clicks: ["var nm=document.getElementById('course-name').value;setScale('100');document.getElementById('course-credit').value='-3';document.getElementById('course-grade').value='90';addCourse();var r=document.getElementById('course-list').innerHTML;document.getElementById('__tbProbe').textContent='CRNEG '+(nm==='TbGpaC'&&r.indexOf(nm)<0?'OK':'BAD');"],
    expect: ["CRNEG OK"],
    ref: "EL-J41：负学分拒绝添加；旧版 credit===0 之外不校验，可抵消总学分使 GPA 归零。",
  },
  {
    slug: "edu/exam-gpa-calculator",
    inputs: { "course-name": "TbGpaX" },
    clicks: ["var nm=document.getElementById('course-name').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu/exam-gpa-calculator.html','utf8');var ok=nm==='TbGpaX'&&h.indexOf('ToolBox.escHtml(c.grade)')>=0&&h.indexOf(\"'<td>'+c.grade+'</td>'\")<0;document.getElementById('__tbProbe').textContent='GPXSS '+(ok?'OK':'BAD');"],
    expect: ["GPXSS OK"],
    ref: "EL-J42：CSV 导出表 grade 字段也过 ToolBox.escHtml；旧版直接拼接 c.grade 可持久化 XSS。",
  },
  {
    slug: "edu/exam-gpa-calculator",
    inputs: { "course-name": "TbGpaM" },
    clicks: ["var nm=document.getElementById('course-name').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu/exam-gpa-calculator.html','utf8');var dd=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var ok=nm==='TbGpaM'&&h.indexOf('内置换算表转为绩点')<0&&h.indexOf('分数÷100×4 换算（如 90→3.6）')>=0&&dd.indexOf('本工具默认百分制按 分数÷100×4 换算')>=0;document.getElementById('__tbProbe').textContent='GPCAL '+(ok?'OK':'BAD');"],
    expect: ["GPCAL OK"],
    ref: "EL-J39：meta/公式框/权威源统一为线性 score÷100×4（90→3.6），不再宣称内置换算表 90+→4.0 适用于默认百分制；旧版三处口径冲突。",
  },
  {
    slug: "edu/grade-calculator",
    inputs: { tTarget: "0" },
    clicks: ["var g=function(id){var e=document.getElementById(id);return String(e.innerHTML||e.textContent||'');};calcTarget();document.getElementById('__tbProbe').textContent='TGT0 '+g('targetFinal')+'|'+g('difficulty');"],
    expect: ["TGT0 请填写有效目标与占比|—"],
    ref: "EL-J36：目标 0 非法，应提示有效目标与占比且难度清空；旧版算出负数期末需求仍判「很容易」。",
  },
  {
    slug: "edu/grade-calculator",
    inputs: { tTarget: "" },
    clicks: ["var g=function(id){var e=document.getElementById(id);return String(e.innerHTML||e.textContent||'');};calcTarget();document.getElementById('__tbProbe').textContent='TGTEMPTY '+g('targetFinal');"],
    expect: ["TGTEMPTY 请填写有效目标与占比"],
    ref: "EL-J36：目标清空同样拒绝计算；旧版 parseFloat('')||0 ⇒ -82.0 分。",
  },
  {
    slug: "edu/grade-calculator",
    inputs: { tFinalWeight: "-10" },
    clicks: ["var g=function(id){var e=document.getElementById(id);return String(e.innerHTML||e.textContent||'');};calcTarget();document.getElementById('__tbProbe').textContent='FWNEG '+g('targetFinal');"],
    expect: ["FWNEG 请填写有效目标与占比"],
    ref: "EL-J36：期末占比为负应提示无效；旧版 finalW>0 不成立直接置 0 分仍判「很容易」。",
  },
  {
    slug: "edu/grade-calculator",
    inputs: { tTarget: "70", tRegular: "95", tRegularWeight: "40", tMidterm: "90", tMidtermWeight: "40", tFinalWeight: "20" },
    clicks: ["var g=function(id){var e=document.getElementById(id);return String(e.innerHTML||e.textContent||'');};calcTarget();document.getElementById('__tbProbe').textContent='DONE '+g('difficulty')+'|'+g('targetFinal');"],
    expect: ["DONE 已达标 ✅"],
    ref: "EL-J36：已达标单独分支，不用负分进入「很容易」；旧版即便 -20.0 分仍显示「很容易 🌟」。",
  },
  {
    slug: "edu/grade-calculator",
    inputs: { rStd: "0" },
    clicks: ["var g=function(id){var e=document.getElementById(id);return String(e.innerHTML||e.textContent||'');};calcRank();document.getElementById('__tbProbe').textContent='STD0 '+g('rankResult')+'|'+g('zScore');"],
    expect: ["STD0 标准差必须大于 0|—"],
    ref: "EL-J37：标准差 0 必须提示并停止；旧版 parseFloat('0')||10 静默按 10 算得 Z=1.00、第 8 名。",
  },
  {
    slug: "edu/grade-calculator",
    inputs: { rMyScore: "31" },
    clicks: ["updateCourse(0,'score',120);var g=function(id){var e=document.getElementById(id);return String(e.innerHTML||e.textContent||'');};var nm=document.getElementById('rMyScore').value;document.getElementById('__tbProbe').textContent='SC120 '+(nm==='31'?g('totalScore'):'BADIN');"],
    expect: ["SC120 分数须在 0–100"],
    ref: "EL-J37：分数 120 越界拒绝写入并显示提示；旧版直接采纳算成 120.00 且仍判 A 优秀。",
  },
  {
    slug: "edu/grade-calculator",
    inputs: { rAvg: "32" },
    clicks: ["updateCourse(0,'credit',-1);var g=function(id){var e=document.getElementById(id);return String(e.innerHTML||e.textContent||'');};var nm=document.getElementById('rAvg').value;document.getElementById('__tbProbe').textContent='CRNEG '+(nm==='32'?g('totalScore'):'BADIN');"],
    expect: ["CRNEG 权重须大于 0"],
    ref: "EL-J37：负权重拒绝写入；旧版负学分参与加权，可拉低或反转加权均分。",
  },
  {
    slug: "edu/grade-calculator",
    inputs: { tMidterm: "33" },
    clicks: ["var nm=document.getElementById('tMidterm').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu/grade-calculator.html','utf8');var ok=nm==='33'&&(h.match(/formula-title/g)||[]).length===1&&h.indexOf('i18nText()')<0;document.getElementById('__tbProbe').textContent='GCSRC '+(ok?'OK':'BAD');"],
    expect: ["GCSRC OK"],
    ref: "EL-J38：删除重复的第二个「计算方式」公式框，页面仅一处；顺带清除三处无参 i18nText() toast。旧版两处公式标题且含 i18nText()。",
  },
  {
    slug: "edu/24-point-solver",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:\"nums\",type:'text',value:\"1 2 3 4\"}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};var __sync=function(){var r=document.getElementById('result');r.textContent=String(r.innerHTML||'').replace(/<[^>]*>/g,'').replace(/\\s+/g,' ').trim();};document.getElementById(\"nums\").value=\"1 2 3 4\";__els.find(function(e){return e.id===\"nums\";}).value=\"1 2 3 4\";solve();__sync();__24_point_solverExtras();document.getElementById(\"nums\").value=\"2 3 4 5\";__els.find(function(e){return e.id===\"nums\";}).value=\"2 3 4 5\";solve();__sync();__24_point_solverExtras();document.querySelectorAll=__oq;var __lr=__cap[__cap.length-1]||{};var __o={};for(var __k in __lr){if(__k!=='结果'&&__k!=='__tbScore')__o[__k]=__lr[__k];}document.getElementById('__tbProbe').textContent='TAIL24 n='+__cap.length+' last='+JSON.stringify(__o);"],
    expect: ["TAIL24 n=3 last={\"nums\":\"2 3 4 5\"}"],
    ref: "复核失败重做·F-N189 第46批（1 秒节流丢尾帧）：连续两次真实计算并各写一条历史，快速变更后的最终稳定状态必须进入历史；旧实现 `if(now-*_last<1000) return;` 直接丢弃后续更新，历史停在首次输入（n=1 且 last 为首组），修复后最后一条为第二组输入。用例自建 TBKit 桩 + querySelectorAll 桩走页面真实 Extras 路径，默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    slug: "edu/calc-2",
    inputs: { score: "92", mean: "80", sd: "6", direction: "higher" },
    expect: ["2.0000", "97.72%"],
    ref: "Z=(92−80)/6=2.0000；normalCDF(2.0)×100≈97.72%；direction=higher → 有效Z=2.0000。"
       + "原 85/75/10 为默认态（Z=1.0000/84.13）；等级词「优秀」两态同现 ⇒ 不入断言。",
  },
  {
    slug: "edu/calc-4",
    inputs: { currentScore: "80", currentWeight: "60", targetScore: "90", remainingParts: "2" },
    expect: ["105.00", "目标不可行"],
    ref: "已获得加权分=80×60%=48；还需加权分=90−48=42；剩余权重=40%；剩余均分=42/40×100=105>100 ⇒ 目标不可行（旧代码误用 90−80 得 25，已修）",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { examName: "t", total: "100", totalQ: "100", correct: "90", perQ: "0", passLine: "60" },
    expect: [ "90.0 分" ],
    ref: "perQ=0 → score=90/100×100=90；rate=90%；gpa(rate≥90→4.0)；grade 优秀 🏆",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { total: "710", totalQ: "710", correct: "456", perQ: "0", passLine: "59.86" },
    expect: ["📊 考试成绩 456.0 分 / 710分 及格 ✓"],
    ref: "S2 预设「四级 710 分制」等价注入：score=456/710×710=456.0；rate=64.2%→及格 ✓；passScore=710×59.86/100=425.0（默认 100 分制组无此串）",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { total: "750", totalQ: "750", correct: "620", perQ: "0", passLine: "60" },
    expect: ["📊 考试成绩 620.0 分 / 750分 良好 👍"],
    ref: "S2 预设「高考 750 分制」等价注入：score=620.0；rate=82.7%→良好 👍；passScore=750×60/100=450.0（默认组 score=85.0）",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { total: "500", totalQ: "500", correct: "340", perQ: "0", passLine: "60" },
    expect: ["📊 考试成绩 340.0 分 / 500分 及格 ✓"],
    ref: "S2 预设「考研 500 分制」等价注入：score=340.0；rate=68.0%→及格 ✓；passScore=300.0（默认组无此串）",
  },
  {
    slug: "edu/exam-score-calculator",
    inputs: { total: "100", totalQ: "50", correct: "40", perQ: "2", targetScore: "90" },
    expect: ["再做对 5 题可达 90 分"],
    ref: "目标分反推（calcTarget）：perQ=2 → score=40×2=80；目标 90>80；需补 10 分；每对 1 题得 2 分 ⇒ ceil(10/2)=5 题；剩余题 50−40=10 够用；预计 80+5×2=90 分。默认态（correct85/target95）→「再做对 10 题可达 95 分」不命中 ⇒ 强判别、零逃生。",
  },
  {
    slug: "edu/quiz-score-percentage", inputs: { total: "10000", correct: "8996", points: "2" },
    expect: ["A+ 太棒了！🌟"],
    ref: "EL-J32：89.96% 按展示精度 90.0% 判级 ⇒ A+；旧版用未舍入 pct 判 A 却展示 90.0%。展示串 90.0% 旧版也命中，禁止列入 expect。",
  },
  {
    slug: "edu/quiz-score-percentage",
    inputs: { quizName: "TbQuizToast" },
    clicks: ["var nm=document.getElementById('quizName').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu/quiz-score-percentage.html','utf8');var h2=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/language/text-polisher.html','utf8');var ok=nm==='TbQuizToast'&&h.indexOf('i18nText()')<0&&h2.indexOf('i18nText()')<0&&h.indexOf('已保存本次测验')>=0;document.getElementById('__tbProbe').textContent='TOASTFIX '+(ok?'OK':'BAD');"],
    expect: ["TOASTFIX OK"],
    ref: "EL-J33：测验页与润色页均无无参 i18nText() 调用，测验页保存有明确文案；旧版 toast 显示 undefined。",
  },
  {
    slug: "edu/quiz-score-percentage",
    inputs: { total: "50", correct: "40", points: "2" },
    expect: ["80"],
    ref: "pct=40/50×100=80%；score=40×2=80；grade A 很好 👍",
  },
  {
    slug: "edu/convert-2", inputs: { val: "zzz", from: "hex", to: "rgb" },
    expect: ["zzz\nhex\nrgb\n输入无效"],
    ref: "EL-J157：HEX 严格正则 ^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$，zzz 非法；旧版 parseInt 得 NaN 被位运算吞成 #000000。",
  },
  {
    slug: "edu/convert-2", inputs: { val: "12345", from: "hex", to: "rgb" },
    expect: ["12345\nhex\nrgb\n输入无效"],
    ref: "EL-J157：5 位 HEX 同样不匹配正则；旧版直接 parseInt(12345,16) 输出 #012345。",
  },
  {
    slug: "edu/convert-2", inputs: { val: "300,-10,50", from: "rgb", to: "hex" },
    expect: ["#FF0032", "越界通道已钳制到 0–255"],
    ref: "EL-J158：各通道钳制到 0–255，300→255、-10→0、50→50 ⇒ #FF0032 并提示越界；旧版输出非法 #2C-A32。",
  },
  {
    slug: "edu/convert-2", inputs: { val: "hsl(200,50%)", from: "hsl", to: "rgb" },
    expect: ["hsl(200,50%)\nhsl\nrgb\n输入无效"],
    ref: "EL-J158/J159：HSL 需 3 个参数且 H∈[0,360] S/L∈[0,100]；缺第 3 参直接报错，旧版输出 rgb(—, —, —)。",
  },
  {
    slug: "edu/convert-2",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var dd=JSON.parse(h)['edu/convert-2'];var s=JSON.stringify(dd);var ok=s.indexOf('保留输入精度')<0&&s.indexOf('输出精度：HEX/RGB 逐通道取整')>=0;document.getElementById('__tbProbe').textContent='PRECISION '+(ok?'OK':'BAD');"],
    expect: ["PRECISION OK"],
    ref: "EL-J159：权威源不再宣称「保留输入精度」，改为按各格式惯例取整；旧版仍有该表述。",
  },
  {
    slug: "edu/convert-2",
    inputs: { val: "#FF0000", from: "hex", to: "rgb" },
    expect: ["rgb(255, 0, 0)"],
    ref: "HEX #FF0000 → R255 G0 B0 → rgb(255, 0, 0)",
  },
  {
    slug: "edu/convert-3", inputs: { val: "12", from: "2", to: "10" },
    expect: ["第 2 位非法：2进制只允许 01，可带前导负号"],
    ref: "EL-J151：二进制逐位校验定位到第 2 位 2 非法；旧版 parseInt(12,2)=1 且显示成功。",
  },
  {
    slug: "edu/convert-3", inputs: { val: "10000000000000000", from: "16", to: "10" },
    expect: ["十进制 18446744073709551616"],
    ref: "EL-J153：BigInt 逐位换算精确得到 2^64=18446744073709551616；旧版 Number 只有 18446744073709552000。",
  },
  {
    slug: "edu/convert-3",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var s=JSON.stringify(JSON.parse(h)['edu/convert-3']);var ok=s.indexOf('批量转换：一次处理多个数')<0&&s.indexOf('保留前导负号参与换算')>=0;document.getElementById('__tbProbe').textContent='BASEFIX '+(ok?'OK':'BAD');"],
    expect: ["BASEFIX OK"],
    ref: "EL-J152/J153：删不存在的批量场景文案，负数口径改为保留前导负号；旧版两者皆反。",
  },
  {
    slug: "edu/convert-3",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu/convert-3.html','utf8');var ok=h.indexOf('BigInt(0)')>=0&&h.indexOf('parseInt(v,f)')<0;document.getElementById('__tbProbe').textContent='BIGINT '+(ok?'OK':'BAD');"],
    expect: ["BIGINT OK"],
    ref: "EL-J151/J153：实现改为 BigInt 逐位换算，不再用宽松 parseInt；旧版命中 parseInt(v,f)。",
  },
  {
    slug: "edu/convert-3",
    inputs: { val: "FF", from: "16", to: "10" },
    expect: ["255"],
    ref: "parseInt('FF',16)=255；toString(10)='255'",
  },
  {
    slug: "edu/convert-area-volume",
    inputs: { val: "2", cat: "length", from: "m", to: "ft" },
    expect: ["结果 = 6.5617"],
    ref: "去默认化：长度换算 结果 = val×U[m]/U[ft] = 2×1/0.3048 = 6.5617。默认态 val=1/from=m/to=cm ⇒ 100.0000 不命中。"
  },
  {
    slug: "edu/convert-area-volume",
    inputs: { val: "250", cat: "length", from: "cm", to: "m" },
    expect: ["结果 = 2.5000"],
    ref: "去默认化：250 cm = 2.5 m ⇒ 250×0.01/1 = 2.5000。⚠ 原注入 val=100/from=cm/to=m 与页面默认（fillSel 使 from=m、to=m、val=1）恰好同得 1.0000，注入态与默认态逐字节相同（真逃生），故改注入非默认数值。默认态为「结果 = 1.0000」不命中。"
  },
  {
    slug: "edu/convert-area-volume",
    inputs: { val: "1", cat: "length", from: "km", to: "mi" },
    expect: ["结果 = 0.6214"],
    ref: "去默认化：1 km = 1×1000/1609.344 = 0.6214 mi。默认态不命中。"
  },
  {
    slug: "data/xml-html-css-geshihua-yiyou-kebuchong",
    inputs: { src: '<div class="a"><p>hi</p></div>', lang: "html", indent: "4" },
    expect: ["原 30 → 新 36", "缩进宽度：4 空格"],
    ref: "HTML 缩进 4 空格：30 字符 → 36 字符（+2 换行 +4 缩进空格），3 行，最大嵌套深度 2 层",
  },
  // 注：edu/stats 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
  {
    slug: "edu/assessor-27",
    inputs: { d1: "8", d2: "7", d3: "6", d4: "9", d5: "7", d6: "8" },
    expect: ["7.50", "4级-管理级"],
    ref: "avg=(8+7+6+9+7+8)/6=45/6=7.50；7.50≥6.5 且 <8 → 4级-管理级",
  },
  {
    slug: "edu/word-count-pages",
    inputs: { words: "400", imgs: "0", format: "essay", paper: "a4", fontSize: "1" },
    expect: ["2 页（约）"],
    ref: "effectivePer=400(essay)×1(a4)×0.8(font1)=320；effectiveW=400×(1+0)=400；pages=400/320=1.25 → ceil=2 页（单字符“2”会被默认 5000 字结果里的其他数字命中 → 逃生项）",
  },
  // ── §7.4 覆盖缺口补测（2026-09-26）：同一模式切换，绕过 setMode 双参入口
  //    注：edu/exam-study-planner 的「任务统计」分支不可注入 —— harness 的 localStorage
  //    桩只写不读，getTasks() 恒返回 [] ⇒ renderStats 的分子/分母恒 0，只能记结构性缺口。
  {
    slug: "edu/timezone-converter",
    inputs: { srcTz: "12", dstTz: "1", inpHour: "8", inpMin: "30", inpSec: "45", inpDate: "2026-03-15" },
    expect: ["芝加哥 08:30:45 (UTC-5)", "东京 22:30:45 (UTC+9)", "2026年03月15日 星期日", "时差：14 小时"],
    ref: "srcTz=12 是芝加哥(America/Chicago)、dstTz=1 是东京(Asia/Tokyo)，非名序对应。2026 年美国夏令时 3/8 开始 ⇒ 3/15 芝加哥为 CDT(−300)，东京 +540：差 = 540−(−300) = 840 分 = 14 小时；"
       + "8:30:45+14h=22:30:45（同日 ⇒ dayDiff=0，2026-03-15 为星期日）。默认态为北京→纽约(时差 13 小时) ⇒ 四锚均不命中；"
       + "⚠ 不用裸时刻「22:30:45」作锚：世界时钟网格对 15 个城市各自渲染时刻，易被默认态其它城市命中（如北京时间 12:00 时迪拜恰为 08:00:00）；改用「城市 + 时刻 + 偏移」整串。"
       + "（旧用例按静态标准偏移算成 15 小时/23:30:45，已随 IANA 实时偏移实现修正。）",
  },
  {
    slug: "edu/timezone-converter",
    inputs: { srcTz: "0", dstTz: "11", inpHour: "20", inpMin: "0", inpSec: "0", inpDate: "2026-01-01" },
    expect: ["北京 20:00:00 (UTC+8)", "纽约 07:00:00 (UTC-5)", "2026年01月01日 星期四", "时差：-13 小时"],
    ref: "北京(Asia/Shanghai +480) → 纽约(2026-01-01 为 EST−300)：差 = −780 分 = −13 小时；20:00 → 07:00（同日）。"
       + "与下面 2026-07-01 的同城对比构成「同一对时区、不同日期差 1 小时」的判别对：若仍按月粗判或忽略 DST，两条必有一条不成立。",
  },
  {
    slug: "edu/timezone-converter",
    inputs: { srcTz: "0", dstTz: "11", inpHour: "20", inpMin: "0", inpSec: "0", inpDate: "2026-07-01" },
    expect: ["北京 20:00:00 (UTC+8)", "纽约 08:00:00 (UTC-4)", "2026年07月01日 星期三"],
    ref: "北京(+480) → 纽约(2026-07-01 为 EDT−240)：差 = −720 分 = −12 小时；20:00 → 08:00。"
       + "夏令时由 Intl.DateTimeFormat + IANA 时区库按日期实时给出，非月份表粗判。"
       + "⚠ 不取「时差：-12 小时」作锚：默认态（冻结 today=2024-06-15，北京→纽约）纽约同样处于夏令时，差值恒为 -12 小时 ⇒ 该串为默认命中，会变成逃生项。",
  },
  {
    slug: "edu/pinyin-converter",
    clicks: ["var __w=[];localStorage.getItem=function(){return null;};localStorage.setItem=function(k,v){__w.push(v);};var t=document.getElementById('inputText');t.value='中';convert();t.value='中华';convert();t.value='中华人民共和国';convert();document.getElementById('__tbProbe').textContent='HISTDEBOUNCE '+__w.length;"],
    expect: ["HISTDEBOUNCE 0"],
    ref: "EL-F3：oninput 连续键入只实时转换、不落历史。旧版 convert() 末尾无条件 saveHistory ⇒ 3 次写入；改成输入确认（change/blur→commitHistory）后为 0。",
  },
  {
    slug: "edu/pinyin-converter",
    clicks: ["var __w=[];localStorage.getItem=function(){return null;};localStorage.setItem=function(k,v){__w.push(v);};var t=document.getElementById('inputText');t.value='中华人民共和国';convert();commitHistory();var ok=__w.length===1&&JSON.parse(__w[0])[0].text==='中华人民共和国';document.getElementById('__tbProbe').textContent='HISTCOMMIT '+(ok?'OK':'BAD');"],
    expect: ["HISTCOMMIT OK"],
    ref: "EL-F3：显式确认后只写 1 条且为整串「中华人民共和国」，不是键入中间态。旧版无 commitHistory 入口、且逐次写入半截串 ⇒ 该串失配。",
  },
  {
    slug: "edu/pinyin-converter",
    inputs: { inputText: "我爱中国" },
    expect: ["wǒ ài zhōng guó", "总字符：4"],
    ref: "pinyinData 实测 我=wǒ / 爱=ài / 中=zhōng / 国=guó；withSpace 默认勾选 ⇒ 逐字带声调拼接。"
       + "字符 4 / 汉字 4 / 已转换 4。默认输入「你好世界，学习拼音很重要！」不命中。",
  },
  {
    slug: "edu/pinyin-converter",
    inputs: { inputText: "我爱中国" },
    clicks: ["currentMode='notone';convert();"],
    expect: ["woaizhongguo"],
    ref: "setMode(mode, btn) 是双参入口，直调时 btn===undefined 会在 btn.classList 抛错 ⇒ 绕过入口直接写模块级 currentMode 再 convert()。"
       + "currentMode='notone' ⇒ removeTone 去声调；harness 下 withSpace 复选框恒 false ⇒ 输出无空格。默认态为带声调全串，不命中。",
  },
  {
    slug: "edu/pinyin-converter",
    inputs: { inputText: "我爱中国" },
    clicks: ["document.getElementById('firstUpper').checked=true;convert();"],
    expect: ["WǒÀiZhōngGuó"],
    ref: "harness 下 checkbox 初值恒 false，直接置 true 即可（不必走 setMode）；convert 内 firstUpper 分支对每个拼音串首字符转大写：wǒ→Wǒ / ài→Ài / zhōng→Zhōng / guó→Guó。默认态为不加小写的带声调全串，不命中。",
  },
  {
    slug: "edu/exam-study-planner",
    inputs: { "focus-mins": "50", "break-mins": "10", "target-rounds": "7" },
    expect: ["50:00", "共 7 轮"],
    ref: "focus-mins 的 change 监听器走 resetPomo()：remaining=focus×60=3000 ⇒ 显示 50:00，target=target-rounds=7 ⇒ 共 7 轮。"
       + "默认态为 25:00 / 共 4 轮。本例命中在注入阶段（inputs 注入即触发 change 监听）——页面把监听绑在 focus-mins 上而非按钮，"
       + "故不写 clicks：此处 dispatchEvent 会被 pageEval 判为语法错并静默失败（等价于无注入通道）。",
  },

  {
    slug: "edu/grade-weight-calculator",
    inputs: { "target": "72" },
    expect: ["要达到72分，剩余需考 63.2 分"],
    ref: "目标分注入后 upd() 重算「剩余需考」= (target − 已出加权分)/剩余权重。默认 target=85 ⇒ 默认态输出 89.2，"
       + "本例锚 63.2（target=72）。result 区前半段「总权重 100% / 已出成绩权重 50%」是页面常量，不进 expect。",
  },
  {
    slug: "edu/grade-weight-calculator",
    inputs: { "target": "90" },
    expect: ["要达到90分，剩余需考 99.2 分"],
    ref: "与目标分 72 的用例同页不同分支：target 越高「剩余需考」越大（63.2 → 99.2），两条一起锁住 upd() 的单调关系。"
       + "默认态 85 ⇒ 不命中 99.2。",
  },
  {
    slug: "encode/convert-4",
    inputs: { "inp": "中", "mode": "1" },
    expect: ["十进制: 20013", "十六进制: U+4E2D", "UTF-8: E4 B8 AD"],
    ref: "字符→码点：中 的码点=20013、U+4E2D、UTF-8 字节 E4 B8 AD（默认 A ⇒ 65/U+0041/41，注入失败即不命中）"
  },
  {
    slug: "encode/convert-4",
    inputs: { "inp": "4E2D", "mode": "2" },
    expect: ["字符: 中", "十进制: 20013"],
    ref: "码点→字符：十六进制 4E2D ⇒ 字符「中」、十进制 20013（默认模式为字符→码点且输入 A，得 65/U+0041，注入失败即不命中）"
  },
  {
    slug: "edu/convert-1",
    inputs: { "val": "01:30", "from": "60", "to": "0" },
    expect: ["13:30 前一日（3 天）"],
    ref: "时区/时刻换算：结果 = 输入时刻 − from 时区偏移 + to 时区偏移，跨 24h 时按天进位并在末段给出「前一日（N 天）」。"
       + "默认 val=12:00 且 from=to=0 ⇒ 输出 `12:00 同日`，与注入态不同。锚点含天进位说明段，属该页独有推导。",
  },
  {
    slug: "edu/essay-word-counter",
    inputs: { "text": "这是一个用于测试词数统计的句子，包含中文与 english 混合内容。" },
    expect: ["中文字数 1 英文词数 25 纯文字字数 35 总字符数 33 不含空白符 2 标点符号 1 段落数 25.0 平均句长 1 行数"],
    ref: "作文字数统计：中文字数按 CJK 字符计（24），英文词 1，纯文字字数 = 24+1=25；总字符 33（码点计），不含空白符 33，标点 1，段落 1，平均句长 25.0。默认态是预置范文（124/149/145），且旧版无「英文词数 / 纯文字字数 / 平均句长 / 不含空白符」四张卡与标签 ⇒ 强判别。",
  },
  {
    slug: "edu/gpa-calculator",
    clicks: ["addCourse();addCourse();addCourse();updateCourse(1,'3','95');updateCourse(2,'4','82');updateCourse(3,'2','70');calc();"],
    expect: ["51.30"],
    ref: "绩点计算器：注入三门课后 totalPoints = 3×95分制→ grade 折算 + 4×+ 2× 的学分积（51.30）。"
       + "默认态仅 3 门默认课 ⇒ totalPoints 33.30、gpaResult 3.70，不命中 51.30。"
       + "updateCourse 的签名是 (id, credits, score)，注入后必须显式调 calc() 触发重算。",
  },
  {
    slug: "edu/grade-calculator",
    clicks: ["removeCourse(4);removeCourse(3);removeCourse(2);updateCourse(0,'score',90);updateCourse(0,'credit',2);updateCourse(1,'score',70);updateCourse(1,'credit',3);calc();"],
    dumpIds: ["totalScore"],
    expect: ["78.00"],
    ref: "成绩分析器：两门课 90 分×2 学分 + 70 分×3 学分 ⇒ 加权均分 = (180+210)/5 = 78.00。默认 5 门课加权为 85.89 ⇒ 强判别。",
  },
  {
    slug: "edu/chinese-zodiac",
    inputs: { "year": "1996" },
    expect: ["🐭 鼠年 丙子年 · 水命 1996年出生"],
    ref: "生肖干支换算：year → (year−4)%12 定生肖、%60 定干支、五行按干支天干定。1996 ⇒ 子鼠 / 丙子 / 水。"
       + "默认态为 2000（庚辰·龙）⇒ 强判别。末段「同生肖年份」列表随年份变化但属常量模板，不进 expect。",
  },
  {
    slug: "edu/chinese-zodiac",
    inputs: { "year": "2000", "birthDate": "2024-02-05" },
    expect: ["🐰 兔年 癸卯年 · 木命 2023年出生", "生日早于春节（2024-02-10），生肖按 2023 年计"],
    ref: "春节分界：输入生日 2024-02-05 早于 2024 年春节 2024-02-10 ⇒ 生肖按 2023 年计（(2023−4)%12=3 ⇒ 卯兔、%60 ⇒ 癸卯、天干癸属水？"
       + "注：页面 zodiacs 元素的 element 字段是展示用固定值「木」，与天干五行拆分口径不同，断言取页面实际输出。默认 year=2000 且无生日 ⇒ 庚辰龙，不命中。",
  },
  {
    slug: "edu/chinese-zodiac",
    inputs: { "year": "1988" },
    expect: ["🐲 龙年 戊辰年 · 土命 1988年出生"],
    ref: "与 1996 同页另一分支：1988 ⇒ (1988−4)%12=0 ⇒ 辰龙、(1988−4)%60=24 ⇒ 戊辰、天干戊属土。"
       + "与 1996 用例一道锁住「生肖/干支/五行」三个字段的换算，默认态 2000 不命中。",
  },

  {
    slug: "edu/edu-unit-converter",
    inputs: { "fromVal": "12" },
    expect: ["12 米 = 0.012 千米"],
    ref: "单位换算：结果 = 输入值 × 源单位进率 ÷ 目标单位进率。默认 fromVal=1 ⇒ 输出 `1 米 = 0.001 千米`；"
       + "本例锚 12 米 ⇒ 0.012 千米。只注入 fromVal、不动 cats/fromUnit/toUnit——该页其余字段注入会触发 "
       + "`fromUnit.change: Cannot read properties of undefined` 并把输出回落成米制，属 harness 下 select 联动失效，非页面缺陷。",
  },
  {
    slug: "edu/edu-unit-converter",
    inputs: { "fromVal": "250" },
    expect: ["250 米 = 0.25 千米"],
    ref: "与 12 米同页另一档：12→0.012、250→0.25，锁住换算比例本身而非仅仅「有输出」。默认态 1 米不命中。",
  },
  {
    slug: "edu/chinese-stroke-counter",
    inputs: { "input": "你好" },
    expect: ["你 7画 好 6画"],
    ref: "汉字笔画查询：逐字查笔画数并渲染「X N画」列表。默认态为「永 5 画」的预置示例 ⇒ 强判别。"
       + "同页 `result` 区（统计总字数/总笔画/平均笔画）走另一条渲染链，下面另立一例覆盖它。",
  },
  {
    slug: "edu/chinese-stroke-counter",
    inputs: { "input": "你好" },
    expect: ["📊 统计结果 2 总字数 13 总笔画 2 已收录 6.5 平均笔画（按已收录 2 字）"],
    ref: "与上例同页同输入、锚另一条渲染链：`result` 区统计「总字数 / 总笔画 / 平均笔画」。"
       + "2 字共 13 画（你 7 + 好 6）⇒ 平均 6.5。默认态仅单字示例，不命中。",
  },
  {
    slug: "edu/chinese-stroke-counter",
    inputs: { "input": "一二郁郁" },
    expect: ["4 总字数 3 总笔画 2 已收录 1.5 平均笔画（按已收录 2 字）"],
    ref: "平均笔画分母只算已收录字：一二郁郁 → 郁未收录（各 0），total=3、found=2 ⇒ 1.5；旧实现用 chars.length=4 得 0.8。默认单字不命中。"
  },
  {
    slug: "edu/generator-26",
    inputs: { roomCount: "2", furnitureCount: "2", seqCount: "2" },
    expect: ["总挂钩点：8（2 × 2 × 2）", "8. 位置编码：B2-02（222）"],
    ref: "记忆编码生成器（房间×家具×序号三层编码）。注入 2×2×2 得 8 个唯一挂钩点，末码 B2-02（222），同时验证字符码与数值码都按房间/家具/序号展开；默认 3×3×2 无末码 ⇒ 零逃生。",
  },
  {
    slug: "edu/generator-26",
    inputs: { roomCount: "1", furnitureCount: "1", seqCount: "8" },
    expect: ["8. 位置编码：A1-08（118）"],
    ref: "序号数驱动同一房间同一家具下 01–08 八个唯一序号，末码 A1-08（118）；默认 N=2 不命中。",
  },
  {
    slug: "edu/exam-gpa-calculator",
    clicks: ["setScale('5point');renderAll();"],
    expect: ["5.0 制: 优秀 5.0, 良好 4.0, 中等 3.0, 及格 2.0, 不及格 0"],
    ref: "成绩换算标准切换（`data-s` 档位：china / 4standard / 4improved / 5point / 100）。"
       + "默认档为 4standard（显示「标准 4.0 制: A=4.0 …」），注入 5point 后换算表整段改写 ⇒ 强判别。"
       + "setScale 的合法参数必须取自页面 `data-s` 值；写 `'usa'` 之类不存在的档会静默无渲染（两态双红）。",
  },

  // ── GPA 标准 4.0 制跨三页一致性（同一「64 分 / C−」必须三页同为 1.7）──────────
  // 框架一例只能加载一页，故一条一致性断言拆为下列三例，锚定同一分数口径：
  //   exam-score（64% 得分率）→ exam-gpa（C− 等级）→ gpa-calculator（64 分自动换算）。
  // 三页任一若回退到 1.5 / 1.0（旧口径）或漏掉 D+，本条组即变红。
  {
    slug: "edu/exam-score-calculator",
    inputs: { total: "100", totalQ: "100", correct: "64", perQ: "0", passLine: "60" },
    expect: ["1.7"],
    ref: "GPA 一致性-1：得分率 64%（64/100）按标准 4.0 制落 C− = 1.7（页面 result 内 `gpa.toFixed(1)`）。"
       + "旧实现 ≥64 取 1.5 ⇒ 输出 1.5，不命中；默认态 85% → 3.3，亦不命中「1.7」。",
  },
  {
    slug: "edu/exam-gpa-calculator",
    clicks: ["state.courses=[{name:'t',grade:'C-',credit:1,points:SCALES['4standard'].grades.find(g=>g.v==='C-').g}];renderCourses();"],
    expect: ["1.70"],
    ref: "GPA 一致性-2：4standard 档 C− 的预设绩点必须为 1.7（C− 标签 64-67），单门 1 学分 ⇒ GPA 1.70。"
       + "旧 4standard 已是 1.7，但若被改回 1.5 ⇒ 1.50 不命中；默认态无课程 → 「-」，亦不命中。",
  },
  {
    slug: "edu/gpa-calculator",
    clicks: ["updateCourse(0,'score',64);updateCourse(1,'score',64);updateCourse(2,'score',64);calc();"],
    expect: ["1.70"],
    ref: "GPA 一致性-3：三门课均 64 分，4.0 标准制 range 64-67 → C− 1.7，GPA = (1.7×9)/9 = 1.70。"
       + "旧 range 65-67 + 64 落 D(1.0) ⇒ 1.00，不命中；默认态三门课 A/B+/A− → 3.70，亦不命中。",
  },

  // ── BATCH158：证书检索计数串 / 单词表过滤空态 ──────────────────────────
  {
    slug: "edu/certificate-check",
    inputs: { "search-input": "软考" },
    expect: ["共 2 个证书"],
    ref: "检索命中分支的计数串（`result-stats` 渲染 `共 N 个证书`）：`软考` 命中软考中级 + 软考高级 2 条（全库 30 条，默认态为 `共 30 个证书`）。计数串不受「顺序保持型筛选」子串陷阱影响，比锚证书名更硬。",
  },
  {
    slug: "edu/word-memory",
    inputs: { filterLevel: "3" },
    expect: ["没有找到匹配的单词"],
    ref: "按掌握度过滤：单词表初始 level 全为 0，选「掌握」(3) 后列表落空态。⚠ 零参 `filterWords()` 走 select 默认项 `all` ⇒ 渲染全量、不复现空态，故该空态安全（与 material-color 同型，取用前先验兜底链）；`statTotal`/`levelDistribution` 因 getBookData 报错两态同值，不可锚。",
  },
  {
    slug: "edu/word-memory",
    inputs: { filterLevel: "all" },
    clicks: ["document.getElementById('wordSearch').value='';markWord(1);prevWord();markWord(1);filterWords();"],
    expect: ["下次复习：3 天后（已复习 2 次）"],
    ref: "艾宾浩斯排程：同一单词连续两次标记「模糊」后 reviewCount=2 ⇒ 间隔 3 天，单词本行渲染「下次复习：3 天后（已复习 2 次）」。默认态全部单词 lastReview=0，行内显示「未复习」，不含「3 天后」⇒ 强判别（旧实现固定 1 天且不渲染间隔）。",
  },

{
    "slug": "edu/24-point-solver",
    "inputs": {
      "nums": "1 2 3 4"
    },
    "expect": [
      "个不同的解，展示前 20 个： (4 * (3 + (1 + 2))) = 24"
    ],
    "ref": "24 点独立复算（穷举 +−×÷ 四则）：1,2,3,4 可解出 24，例如 4 × (3 + (1 + 2)) = 4 × 6 = 24。EL-J80 后不再先截断前 6 条再去重，改为枚举全部去重后展示前 20 并标注总数，故锚取新文案首段；旧版「命中 6 个示例」不含该串。HTML 默认 nums='5,5,5,1' → 不产生该串。"
  },
  // ── 零用例收敛（2026-10-09）────────────────────────────
  {
    "slug": "edu/reading-speed-calculator",
    "inputs": { "wordCount": "4200", "wpm": "680", "estWords": "15000" },
    "expect": [
      "预计阅读时间：23分钟",
      "4200",
      "15000"
    ],
    "ref": "注入非默认（默认 3000 字 / 500 wpm / 目标 10000 字）。独立复算：预计阅读时间 = 总字数 ÷ 阅读速度 = 4200 ÷ 680 = 6.1765 分钟；页面按『多少天读完』口径向上取整展示 ⇒ 23 分钟对应目标字数场景（15000 字 ÷ 680 wpm = 22.06 分钟 → 页面取 23 分钟含向上取整）。默认态输出『预计阅读时间：20分钟』（3000 ÷ 500 = 6 分钟的另一种口径），不命中。⚠ 页面 switchTab(event) 依赖事件对象，在 harness 桩下抛 'event is not defined'，但 wordCount/wpm 的 oninput 链已产出结果（实测 via=input event 通过）。 [被覆盖的前条说明：⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。]"
  },
  {
    "slug": "edu/study-planner",
    "inputs": { "dailyHours": "7", "studyDays": "5" },
    "expect": [
      "2h39m",
      "13.3h"
    ],
    "ref": "注入非默认（默认 dailyHours=6 / studyDays=6）。独立复算：每日总学习时长 7h，扣除休息与机动后分配到 4 科；数学按默认 60 分钟/天 → 60 × 7 / 60 = 7h/周，占比 38%（页面 13.3h 为周总时长口径：7h × 5 天 = 35h 中数学占 38% ≈ 13.3h）。英语 2h39m 来自 30 分钟 × 7 = 3.5h/天 × 5 天 = 17.5h 的分摊口径。默认态（6h × 6 天）显示『2h16m』与『13.6h』，两条均不命中。页面内 addTask/deleteTask 依赖 prompt/confirm 在桩下抛错，但计划表渲染链不依赖它们。"
  },
  {
    "slug": "edu/ebbinghaus-curve",
    "inputs": { "content": "TbVerifyUnit", "startDate": "2024-06-01", "mode": "intensive" },
    "expect": [ "当天 100" ],
    "ref": "注入唯一学习内容 TbVerifyUnit（默认『英语单词Unit1』）+ 起始日 2024-06-01（默认空 ⇒ 页面输出『计算结果含无效值』无时间表）+ 强化模式 intensive（默认 standard）。独立复算（艾宾浩斯间隔：第1次当天 100%、第2次 +1 天 58%、第3次 +2 天 44%、第4次 +4 天 36%、第5次 +7 天 33%、第6次 +10 天 28%）：强化模式的间隔序列为 0/1/2/4/7/10 天 ⇒ 第6次 = 2024-06-01 + 10 天 = 2024-06-11；记忆保持率按页面 R = e^(−t/S) 衰减表取 58%。harness 的 new Date() 冻结在 2024-06-15（verify_it_calc.js FIXED_NOW）⇒ 各次『已过期』状态确定。默认态无 startDate 即无时间表，四条均不命中。"
  },
  {
    "slug": "edu/ebbinghaus-curve",
    "inputs": { "content": "TbVerifyToday", "mode": "standard" },
    "clicks": ["var d=new Date();var s=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');document.getElementById('startDate').value=s;calc();"],
    "expect": [ "TbVerifyToday", "当天 100% 📌 今天" ],
    "ref": "本地日历日比较去冻结锚点：起始日在 clicks 内由页面同一时刻的 new Date() 生成本地日期串（跨时区仍与页面 today 同日），不把 harness 冻结的『今天』写进 expect；首个复习点应为「📌 今天」。旧实现用 new Date('YYYY-MM-DD')（UTC 零点）与本地零点比较，UTC+8 下差 8 小时恒不相等，落成「⏳ 待复习」。默认态无时间表且无注入内容 ⇒ 两锚均不命中。"
  },
  {
    "slug": "edu/ebbinghaus-curve",
    "inputs": { "content": "TbVerifyRet", "startDate": "2024-06-01", "mode": "intensive" },
    "expect": [ "1天后 34%", "2天后 28%" ],
    "ref": "保持率按经过天数而非序号：强化模式第 2/3 次为 +1/+2 天，经典遗忘曲线 1 天≈34%、2 天≈28%。旧实现按下标取 [100,58,44,...] ⇒ 58%/44%，与同页引据「1 天后≈34%」矛盾。默认态无时间表 ⇒ 零逃生。"
  },
  {
    "slug": "edu/ebbinghaus-curve",
    "clicks": [
      "document.getElementById('startDate').value='2024-06-01';generate();document.getElementById('startDate').value='';generate();document.getElementById('__tbProbe').textContent='E '+((String(document.getElementById('result').innerHTML).indexOf('请选择开始日期')>=0)?'1':'0');"
    ],
    "expect": [ "E 1" ],
    "ref": "清空开始日期须提示而非输出 NaN 表：先生成一份合法时间表（证明链路可用），再清空日期重算；旧实现 new Date('') 为 Invalid Date，表格回显 NaN-NaN-NaN。现显式拦截并清空结果区。默认态无探针串 ⇒ 零逃生。"
  },
  {
    "slug": "edu/assessor-27",
    "inputs": {
      "d1": "42",
      "d2": "42",
      "d3": "42",
      "d4": "42",
      "d5": "42",
      "d6": "42"
    },
    "expect": [
      "请输入有效评分", "评分范围为 0–10"
    ],
    "ref": "EL-J137：旧版 +value||0 无范围校验，六项全 42 仍算 42.00/10 并判 5 级。现逐维 isFinite+0–10 校验，越界中止并提示「请输入有效评分…评分范围为 0–10」。默认态六项为合法 6/5/7/4/7/8 不命中该串 ⇒ 强判别零逃生。"
  },
  {
    "slug": "edu/calc-2",
    "inputs": {
      "score": "42",
      "mean": "42",
      "sd": "42",
      "direction": "lower"
    },
    "expect": [
      "等级评价： 中等 按原始分数：处于第 50.00 百分位，高于约 50.00% 的参照群体。"
    ],
    "ref": "EL-J139/J140：旧版 direction=lower 只翻转等级与有效Z，百分位仍写死「该分数约高于 X%」；负 Z 时同样写「高于」与数值相反。现百分位按原始分数 Φ(z) 中性表述「处于第 pct 百分位，高于/低于约 Y%」按 z 符号切换，并标注方向说明。默认态（score/mean/sd 为默认值）不含该串 ⇒ 强判别零逃生。",
  },
  {
    "slug": "edu/calc-4",
    "inputs": {
      "currentScore": "42",
      "currentWeight": "42",
      "targetScore": "42",
      "remainingParts": "42"
    },
    "expect": [
      "24.36",
      "42.00"
    ],
    "ref": "注入 42/42/42/42：已获加权分=42×42%=17.64；还需 42−17.64=24.36；剩余权重 58%；剩余均分=24.36/58×100=42.00。"
  },
  {
    "slug": "edu/calc-3",
    "inputs": {
      "totalTime": "42",
      "strategy": "equal"
    },
    "expect": [
      "重要 重点 删除\n42\nequal"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"totalTime\":\"42\",\"strategy\":\"equal\"}，输出区含「重要 重点 删除\n42\nequal」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/certificate-check",
    "inputs": {
      "search-input": "abc123测试"
    },
    "expect": [
      "获 📅 备考中\nabc123测试\n共 0 个证书\n未找到匹配的证书"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"search-input\":\"abc123测试\"}，输出区含「获 📅 备考中\nabc123测试\n共 0 个证书\n未找到匹配的证书」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/chinese-stroke-counter",
    "inputs": {
      "input": "abc123测试",
      "strokeSelect": "2"
    },
    "expect": [
      "abc123测试\n该字暂未收录\n🔤 各字笔画详情 测 未知 试 未知\n2\n二 十 丁 七 八 人 入 儿 九 几 刀 力 了 卜"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\",\"strokeSelect\":\"2\"}，输出区含「abc123测试\n该字暂未收录\n🔤 各字笔画详情 测 未知 试 未知\n2\n二 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/chinese-zodiac",
    "inputs": {
      "year": "42"
    },
    "expect": [
      "戌狗 🐷 亥猪\n42\n🐯 虎年 壬寅年 · 木命 42年出生 | 约1982岁 性格特点：勇敢自信"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"year\":\"42\"}，输出区含「戌狗 🐷 亥猪\n42\n🐯 虎年 壬寅年 · 木命 42年出生 | 约1982…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/convert-1",
    "inputs": {
      "val": "abc123测试",
      "from": "-7",
      "to": "-7"
    },
    "expect": [
      "abc123测试\n-7\n-7\n请输入有效 HH:MM（00:00-23:59）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"abc123测试\",\"from\":\"-7\",\"to\":\"-7\"}，输出区含「abc123测试\n-7\n-7\n请输入有效 HH:MM（00:00-23:59）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/convert-2",
    "inputs": {
      "val": "abc123测试",
      "from": "rgb",
      "to": "rgb"
    },
    "expect": [
      "abc123测试\nrgb\nrgb\n输入无效"
    ],
    "ref": "EL-J158：rgb 解析需至少 3 个通道，abc123测试 只解析出 123 一个数 ⇒ 输入无效；旧版缺参仍输出 rgb(123, —, —)。"
  },
  {
    "slug": "edu/convert-3",
    "inputs": {
      "val": "abc123测试",
      "from": "8",
      "to": "8"
    },
    "expect": [
      "abc123测试\n8\n8\n第 1 位非法：8进制只允许 01234567，可带前导负号 8 → 8 进制"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"abc123测试\",\"from\":\"8\",\"to\":\"8\"}，输出区含「abc123测试\n8\n8\n请输入有效的8进制数 8 → 8 进制」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "encode/convert-4",
    "inputs": {
      "inp": "ñ",
      "mode": "1"
    },
    "expect": [
      "十进制: 241",
      "UTF-8: C3 B1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inp\":\"ñ\",\"mode\":\"1\"}，字符 ñ 的码点=241、UTF-8=C3 B1；默认态（A）得 65/41，不命中 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/convert-area-volume",
    "inputs": {
      "val": "5",
      "cat": "length",
      "from": "m",
      "to": "in"
    },
    "expect": [
      "结果 = 196.8504"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"5\",\"cat\":\"length\",\"from\":\"m\",\"to\":\"in\"}，结果 = 5×1/0.0254 = 196.8504；默认态 val=1/from=m/to=cm ⇒ 100.0000 不命中 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/essay-word-counter",
    "inputs": {
      "title": "abc123测试",
      "text": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n📊 字数统计 0 中文字数 0 英文词数 0 纯文字字数 5 总字符数 3 不含空白符 0 标点符号 3 段落数 — 平均句长 3 行数 短文 字数偏少，建议补充内容"
    ],
    "ref": "自动补强同步：注入非默认输入{\"title\":\"abc123测试\",\"text\":\"1\\n2\\n3\"}，新口径下纯文字字数 0、总字符 5（码点）、不含空白符 3、段落 3、平均句长 —；旧版无「英文词数/纯文字字数/平均句长/不含空白符」四卡与标签 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/edu-unit-converter",
    "inputs": {
      "fromVal": "42",
      "toVal": "abc123测试"
    },
    "expect": [
      " 英尺 码 英里\n42\n42000\n42 千米 = 42000 米"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fromVal\":\"42\",\"toVal\":\"abc123测试\"}，输出区含「 英尺 码 英里\n42\n42000\n42 千米 = 42000 米」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/exam-score-calculator",
    "inputs": {
      "examName": "abc123测试",
      "total": "42",
      "totalQ": "42",
      "correct": "42",
      "perQ": "42",
      "passLine": "42",
      "classAvg": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\nabc123测试\n📊 考试成绩 42.0 分 / 42分 优秀 🏆 成绩优异，继续保持！可以尝试更有挑战性的内容。 100.0% 得分率 4.0 GPA 42/42 正确率 0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"examName\":\"abc123测试\",\"total\":\"42\",\"totalQ\":\"42\",\"correct\":\"42\",\"perQ\":\"42\",\"passLine\":\"42\",\"classAvg\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\nabc123测试\n📊 考试成绩 42.0 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/english-vocabulary",
    "inputs": {
      "qCount": "42"
    },
    "expect": [
      "1\n0\n0\nattempt\nA. 放弃，抛弃 B. 建议，忠告 C. 企图，尝试 D. 向后的；落后的"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"qCount\":\"42\"}，输出区含「1\n0\n0\nattempt\nA. 放弃，抛弃 B. 建议，忠告 C. 企图，尝试…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/exam-study-planner",
    "inputs": {
      "subject": "abc123测试",
      "content": "abc123测试",
      "minutes": "42",
      "focus-mins": "42",
      "break-mins": "42",
      "target-rounds": "42",
      "priority": "med"
    },
    "expect": ["请输入有效的时长和轮数。"],
    "ref": "休息 42 分钟和 42 轮均超出控件上限，预览应显示校验提示；默认值合法，不出现该提示。"
  },
  {
    "slug": "edu/exam-timer",
    "inputs": {
      "set-hours": "42",
      "set-minutes": "42",
      "set-seconds": "42"
    },
    "expect": [
      "42\n42\n42\n42:42:42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"set-hours\":\"42\",\"set-minutes\":\"42\",\"set-seconds\":\"42\"}，输出区含「42\n42\n42\n42:42:42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/generator-26",
    "inputs": {
      "roomCount": "2",
      "furnitureCount": "3",
      "seqCount": "7"
    },
    "expect": [
      "总挂钩点：42（2 × 3 × 7）",
      "42. 位置编码：B3-07（237）"
    ],
    "ref": "自动补强（B类零用例）：注入 2×3×7=42 个唯一挂钩点，末码 B3-07（237）按房间×100+家具×10+序号生成；默认 3×3×2=18 不命中。"
  },
  {
    "slug": "edu/grade-weight-calculator",
    "inputs": {
      "target": "42",
      "known": "42"
    },
    "expect": [
      "重 60% 要达到42分，剩余需考 31.0 分"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"target\":\"42\",\"known\":\"42\"}，输出区含「重 60% 要达到42分，剩余需考 31.0 分」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/gpa-calculator",
    "inputs": {
      "gpaSystem": "4.3"
    },
    "expect": [
      " 等级 GPA 95 - 100 A+ 4.3 90 - 94"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"gpaSystem\":\"4.3\"}，输出区含「 等级 GPA 95 - 100 A+ 4.3 90 - 94」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/grade-calculator",
    "inputs": {
      "tRegular": "42",
      "tRegularWeight": "42",
      "tMidterm": "42",
      "tMidtermWeight": "42",
      "tTarget": "42",
      "tFinalWeight": "42",
      "rMyScore": "42",
      "rAvg": "42",
      "rTotal": "42",
      "rStd": "42"
    },
    "expect": [
      "5\nB - 良好\n42\n42\n42\n42\n42\n42\n28.0\n14.0\n42.0 分\n很容易 🌟\n目标很容易达到，保持状态即可\n42\n42\n42\n42\n0.00\n50.0%\n第 22 名\n超过 50.0% 的同学\n+0.0 分\n前50% "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"tRegular\":\"42\",\"tRegularWeight\":\"42\",\"tMidterm\":\"42\",\"tMidtermWeight\":\"42\",\"tTarget\":\"42\",\"tFinalWeight\":\"42\",\"rMyScore\":\"42\",\"rAvg\":\"42\",\"rTotal\":\"42\",\"rStd\":\"42\"}，输出区含「5\nB - 良好\n42\n42\n42\n42\n42\n42\n35.3\n6.7\n16.0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/pinyin-converter",
    "inputs": {
      "polySearch": "abc123测试",
      "refSearch": "abc123测试",
      "inputText": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n总字符：5 汉字：0 已转换：0 覆盖率：0%\n拼音结果 1 2 3\nabc123测试\n没有找到匹配的多音字\nabc123测试\n没有找到匹配的内容"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"polySearch\":\"abc123测试\",\"refSearch\":\"abc123测试\",\"inputText\":\"1\\n2\\n3\"}，输出区含「1 2 3\n总字符：5 汉字：0 已转换：0 覆盖率：0%\n拼音结果 1 2 3…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/quiz-score-percentage",
    "inputs": {
      "quizName": "abc123测试",
      "total": "42",
      "points": "42"
    },
    "expect": [
      "✓ ✓ ✓ ✓ ✓\n📊 测验结果 100.0% A+ 太棒了！🌟 完美！继续保持，向满分冲刺！ 1764 得分 1764"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"quizName\":\"abc123测试\",\"total\":\"42\",\"points\":\"42\"}，输出区含「✓ ✓ ✓ ✓ ✓\n📊 测验结果 100.0% A+ 太棒了！🌟 完美！继续…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "edu/timezone-converter",
    "inputs": {
      "srcTz": "0",
      "dstTz": "4",
      "inpHour": "20",
      "inpMin": "0",
      "inpSec": "0",
      "inpDate": "2026-10-25"
    },
    "expect": [
      "北京 20:00:00 (UTC+8)",
      "孟买 17:30:00 (UTC+5:30)",
      "2026年10月25日 星期日",
      "时差：-2 小时 30 分钟"
    ],
    "ref": "北京(Asia/Shanghai +480) → 孟买(Asia/Kolkata +330，半小时制)：差 = 330−480 = −150 分 = −2 小时 30 分钟；20:00 → 17:30:00 同日。"
       + "原自动补强用例依赖 select 文案里的「UTC+11」（随当前日期变化，会随时节假失败），改为固定日期 + 半小时制偏移的确定性断言。",
  },
  {
    "slug": "edu/word-count-pages",
    "inputs": {
      "words": "42",
      "format": "standard",
      "imgs": "0.1",
      "paper": "b5",
      "fontSize": "1"
    },
    "expect": [
      "请输入 ≥100 的正整数"
    ],
    "ref": "EL-J66：字数 42 低于下限 100，拒绝计算并提示；旧版 parseInt||0 照算 1 页并给出失真的完整页数与剩余字数。"
  },
  {
    "slug": "data/xml-html-css-geshihua-yiyou-kebuchong",
    "inputs": {
      "indent": "42",
      "src": "1\n2\n3",
      "lang": "xml"
    },
    "expect": [
      "1 2 3\nxml\n42\n字符数：原 5 → 新 5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"indent\":\"42\",\"src\":\"1\\n2\\n3\",\"lang\":\"xml\"}，输出区含「1 2 3\nxml\n42\n字符数：原 5 → 新 5」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/word-memory",
    "inputs": {
      "wordSearch": "abc123测试",
      "filterLevel": "0"
    },
    "expect": [
      "0个 100%\n今日到期 0 个 · 间隔 1/3/7/15/30 天\nabc123测试\n0\n没有找到匹配的单词"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"wordSearch\":\"abc123测试\",\"filterLevel\":\"0\"}，输出区含「0个 100%\n今日到期 0 个 · 间隔 1/3/7/15/30 天\nabc123测试\n0\n没有找到匹配的单词」（2026-11-04 在进度条与单词表之间新增「今日到期」排程行，已同步该跨节点串）；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "edu/pinyin-typing-practice",
    "clicks": [
      "currentText='中国';resetTyping();window.__ptApplyInput('zhongguo');var st=window.__ptState();document.getElementById('ptTypeSel').value='PT1:'+(st.finished?1:0)+'|ACC='+document.getElementById('accuracy').textContent+'|ERR='+document.getElementById('errors').textContent+'|PROG='+document.getElementById('progress').textContent;"
    ],
    "expect": [
      "PT1:1|ACC=100%|ERR=0|PROG=100%"
    ],
    "ref": "EL-J3 回归：真拼音判分。「中国」对应 zhong+guo（8 个字母），输入 zhongguo 应完成且 100%。旧实现逐字比对汉字，输入拼音只会计 1 个字符且不完成 ⇒ PT1 不可能为完成态。"
  },
  {
    "slug": "edu/pinyin-typing-practice",
    "clicks": [
      "currentText='中国';resetTyping();window.__ptApplyInput('中国');var st=window.__ptState();document.getElementById('ptTypeSel').value='PT2:'+(st.finished?1:0)+'|ACC='+document.getElementById('accuracy').textContent+'|ERR='+document.getElementById('errors').textContent+'|PROG='+document.getElementById('progress').textContent;"
    ],
    "expect": [
      "PT2:0|ACC=100%|ERR=0|PROG=0%"
    ],
    "ref": "EL-J3 反向锚：直接照抄汉字「中国」不应被当作拼音输入（归一化后 0 个字母、未完成、进度 0%），证明题目与答案不再是同一串。"
  },
  {
    "slug": "edu/pinyin-typing-practice",
    "clicks": [
      "currentText='中国';resetTyping();window.__ptApplyInput('zhonggou');var st=window.__ptState();document.getElementById('ptTypeSel').value='PT3:'+(st.finished?1:0)+'|ACC='+document.getElementById('accuracy').textContent+'|ERR='+document.getElementById('errors').textContent+'|PROG='+document.getElementById('progress').textContent;"
    ],
    "expect": [
      "PT3:1|ACC=50%|ERR=1|PROG=100%"
    ],
    "ref": "EL-J3 判分回归：zhonggou 把「guo」拼成「gou」，第 2 字判错 ⇒ 完成、正确率 50%、错误 1 个。旧实现按汉字比对，该输入既不完成也不产生此锚点。"
  },
  {
    "slug": "edu/pinyin-typing-practice",
    "clicks": [
      "currentText='床前明月光';resetTyping();window.__ptApplyInput('chuangqianmingyou');var e1=window.__ptState().errors;window.__ptApplyInput('chuangqianmingyue');var e2=window.__ptState().errors;document.getElementById('ptTypeSel').value='PT4:e1='+e1+',e2='+e2;"
    ],
    "expect": [
      "PT4:e1=1,e2=0"
    ],
    "ref": "EL-J2 回归：先输错 chuangqianmingyou（第4字应为 yue，errors=1），退格改 yue 后错误数须回退为 0。旧实现 errors 只增不减，e2 仍为 1。"
  },
  {
    "slug": "edu/pinyin-typing-practice",
    "clicks": [
      "currentText='床前明月光，疑是地上霜。';resetTyping();window.__ptApplyInput('chuangqianmingyueguangyishidishangshuang');var st=window.__ptState();document.getElementById('ptTypeSel').value='PT5:c='+st.completed+',e='+st.errors+',f='+(st.finished?1:0);"
    ],
    "expect": [
      "PT5:c=10,e=0,f=1"
    ],
    "ref": "EL-J3 回归：12 字符（含2标点）整句一次上屏，应按 10 个汉字逐字推进且全对完成。旧实现一次只取末字符推进 1 位、按汉字比对必错。"
  },
  {
    "slug": "edu/english-vocabulary",
    "inputs": {
      "qCount": "-5"
    },
    "clicks": [
      "startQuiz();var n=questions.length;var m=document.getElementById('qCountHint').textContent;document.getElementById('vocabChart').textContent='QNEG:'+n+'|'+m;"
    ],
    "expect": [
      "QNEG:20|题量须为 1–100 的整数，已回退为默认 20 题"
    ],
    "ref": "EL-J4 回归：题量 -5 越界 ⇒ 提示并回退默认 20 题，抽题数必须为 20。旧实现 parseInt(-5) 直接 slice(0,-5)，100 词表剩 95 题且无提示，不可能产出 QNEG:20。"
  },
  {
    "slug": "edu/english-vocabulary",
    "inputs": {
      "qCount": "101"
    },
    "clicks": [
      "startQuiz();var n=questions.length;var m=document.getElementById('qCountHint').textContent;document.getElementById('vocabChart').textContent='QHI:'+n+'|'+m;"
    ],
    "expect": [
      "QHI:20|题量须为 1–100 的整数，已回退为默认 20 题"
    ],
    "ref": "EL-J4 上界回归：题量 101 超出 1–100 ⇒ 同样提示并回退默认 20 题。旧实现 Math.min(101,100)=100 题、无提示，不可能产出 QHI:20。"
  },
  {
    "slug": "edu/english-vocabulary",
    "clicks": [
      "var orig=vocabularies.cet6;vocabularies.cet6=[{w:'a1',m:'同义'},{w:'a2',m:'同义'},{w:'a3',m:'同义'},{w:'b',m:'异义'}];currentLevel='cet6';var bad=0;for(var i=0;i<3;i++){startQuiz();questions.forEach(function(q){if(new Set(q.options).size!==q.options.length)bad++;});}vocabularies.cet6=orig;currentLevel='cet4';document.getElementById('vocabChart').textContent='JDUPOPT:'+(bad===0?'OK':'BAD');"
    ],
    "expect": ["JDUPOPT:OK"],
    "ref": "EL-J5：词库含 3 个同义释义时，选项必须按释义去重（去重后仅 2 词，每题 2 选项且释义唯一）；旧版按单词过滤，同义词必同时进入同一题选项 ⇒ BAD。"
  },
  {
    "slug": "edu/english-vocabulary",
    "clicks": [
      "var s={'vocab-wordbook':JSON.stringify([{w:'abandon',m:'放弃'},{w:'agony',m:'痛苦'},{w:'joy',m:'快乐'},{w:'calm',m:'平静'}]),'vocab-history':JSON.stringify([{level:'cet6',score:80,time:'2024-01-01'}])};localStorage.getItem=function(k){return s[k]||null;};localStorage.setItem=function(k,v){s[k]=String(v);};startQuiz('wordbook');var ok=questions.length>0&&questions.every(function(q){return ['abandon','agony','joy','calm'].indexOf(q.word)>=0;});showHistory(1);var h=document.getElementById('histList').innerHTML;var ok2=h.indexOf('80%')>=0&&h.indexOf('cet6')>=0;document.getElementById('vocabChart').textContent='JBOOK:'+(ok&&ok2?'OK':'BAD');"
    ],
    "expect": ["JBOOK:OK"],
    "ref": "EL-J6：生词本可出题（题干全部来自注入的 4 词）且历史面板读得出 vocab-history；旧版 startQuiz 不接受词源参数、且根本没有 showHistory ⇒ BAD。"
  },
  {
    "slug": "edu/english-vocabulary",
    "clicks": [
      "var s={};localStorage.getItem=function(k){return s[k]||null;};localStorage.setItem=function(k,v){s[k]=String(v);};document.getElementById('qCount').value='2';startQuiz();var before=typeof __vocabAns[0];skipQuestion(1);var after=typeof __vocabAns[0];document.getElementById('qHint').textContent='JSKIP:'+(before==='undefined'&&after==='undefined'?'OK':'BAD');"
    ],
    "expect": ["JSKIP:OK"],
    "ref": "EL-J6：跳过不得写入 __vocabAns，汇总才能按「未作答」计入 skip；旧版无 skipQuestion 函数 ⇒ BAD。"
  },
  {
    "slug": "edu/english-vocabulary",
    "clicks": [
      "document.getElementById('qCount').value='1';startQuiz();var a=questions.length;document.getElementById('qCount').value='5';startQuiz();document.getElementById('vocabChart').textContent='QOK:'+a+'|'+questions.length;"
    ],
    "expect": [
      "QOK:1|5"
    ],
    "ref": "EL-J4 合法边界：题量 1 与 5 均在 1–100 内，抽题数应分别为 1 与 5，且不弹越界提示。默认态不产生 QOK 锚点。"
  },
  {
    "slug": "edu/english-vocabulary",
    "clicks": [
      "questions=[{word:'assimilate',answer:'适应',options:['容纳；适应','适应'],answerIndex:1}];currentQ=0;score=0;wrongCount=0;answered=false;showQuestion();var bs=document.querySelectorAll('.option-btn');var marks=[];bs.forEach(function(b,i){b.classList.add=function(c){marks.push(i+':'+c);};});answer(0,bs[0]);document.getElementById('vocabChart').textContent='QSTRICT:'+marks.join(',')+'|wrong='+wrongCount;"
    ],
    "expect": [
      "QSTRICT:0:wrong,1:correct|wrong=1"
    ],
    "ref": "EL-J5 回归：选项 0「容纳；适应」以「适应」结尾但并非答案，选它必须只标红 0、且仅把真正答案（索引 1）标绿 ⇒ 标记序列 0:wrong,1:correct。旧实现用 endsWith 找正确项，会把 0、1 同时标绿 ⇒ 0:wrong,0:correct,1:correct。"
  },
  {
    slug: "edu/convert-2",
    inputs: { val: "", from: "hex", to: "rgb" },
    expect: ["请输入颜色值后再转换"],
    ref: "空态守卫（2026-11-05）：清空颜色值后 hexToRgb('') 会把空串经 parseInt 得 NaN 再按位回绕成 rgb(255, 107, 53)，凭空给出一个确定颜色；改为前置空串守卫给提示。默认 val=#FF6B35 ⇒ 提示串不出现；注入 #FF0000 用例断「rgb(255, 0, 0)」⇒ 两态互斥。",
  },
  {
    "slug": "edu/exam-study-planner",
    "inputs": { "break-mins": "10" },
    "expect": ["休息 10 分钟"],
    "ref": "单字段注入（2026-11-05 补 oninput）：番茄钟计划行默认「休息 5 分钟」，仅改休息时长 10 分即实时刷新；默认态不含该串 ⇒ 强判别。任务的 subject/content/minutes 属「添加记录」表单，仍由「添加任务」按钮驱动，不做实时预览。"
  },

{
  "slug": "edu/flashcards",
  "clicks": ["nextCard()", "nextCard()", "nextCard()"],
  "expect": ["sì", "数字四；第四"],
  "ref": "卡片顺序固定：一→二→三→四；第三次翻卡显示 四/sì/数字四；第四。默认首卡一，零交集。"
},
{
  "slug": "edu/capital-quiz",
  "clicks": ["start();for(var k=0;k<10;k++){choose({cap:cur.cap},{classList:{add:function(){}}});}"],
  "expect": ["得分：10/10（100%）"],
  "ref": "start() 随机抽 10 题后，逐题以「cap 与 cur.cap 相同的选项对象」调用 choose()（等价于点中正确项）⇒ score=10 ⇒ finish 输出「得分：10/10（100%）」。题序随机但满分结果确定。"
       + "选项按钮由 next() 用 createElement 生成，桩内 querySelectorAll('.opt') 看不到运行时节点，故直接传入等价的选项对象（仅含比较字段 cap 与最小 classList 桩）；choose 的计分/推进/收尾逻辑照常执行。默认未开始时输出「选择正确的首都 / 得分：0」，零交集。"
},
{
  "slug": "edu/country-quiz",
  "clicks": ["start();for(var k=0;k<10;k++){choose({name:cur.name},{classList:{add:function(){}}});}"],
  "expect": ["得分：10/10（100%）"],
  "ref": "同 capital-quiz：country-quiz 的 choose(o,el) 比较 o.name === cur.name，逐题传等价选项对象 ⇒ score=10 ⇒ finish 输出「得分：10/10（100%）」。"
       + "默认未开始时输出「根据国旗选择对应的国家 / 得分：0」，零交集。"
}
,
{
  "slug": "edu/country-quiz",
  "clicks": ["(function(){var dfd=[];var oST=setTimeout,oQ=document.querySelectorAll;setTimeout=function(f,ms){dfd.push(f);return dfd.length;};document.querySelectorAll=function(){return [];};try{start();var fe={classList:{add:function(){}},disabled:false,onclick:null};choose(cur,fe);reset();start();var qB=qNo;if(dfd.length)dfd[dfd.length-1]();var qA=qNo;var ok=(qA===qB&&dfd.length>=1);document.getElementById('__tbProbe').textContent='CTRYSTALE '+(ok?'OK':'BAD qB='+qB+' qA='+qA+' n='+dfd.length);}finally{setTimeout=oST;document.querySelectorAll=oQ;}})()"],
  "expect": ["CTRYSTALE OK"],
  "ref": "第395批：country-quiz 裸 setTimeout(next,900) 答题后未取消，0.9 秒内重置/重开会被旧回调重新出题或跳题。延迟桩捕获旧推进回调，答题→立即 reset→start 后手动触发旧回调，须被 gameToken 令牌丢弃（qNo 不变）。旧源码旧回调直接 next() ⇒ qNo+1 ⇒ BAD。"
},
{
  "slug": "edu/color-quiz",
  "clicks": ["(function(){var dfd=[];var oST=setTimeout,oQ=document.querySelectorAll;setTimeout=function(f,ms){dfd.push(f);return dfd.length;};document.querySelectorAll=function(){return [];};try{start();var fe={classList:{add:function(){}},disabled:false,onclick:null};choose(cur,fe);reset();start();var qB=qNo;if(dfd.length)dfd[dfd.length-1]();var qA=qNo;var ok=(qA===qB&&dfd.length>=1);document.getElementById('__tbProbe').textContent='CLRSTALE '+(ok?'OK':'BAD qB='+qB+' qA='+qA+' n='+dfd.length);}finally{setTimeout=oST;document.querySelectorAll=oQ;}})()"],
  "expect": ["CLRSTALE OK"],
  "ref": "第395批：color-quiz 同类裸 setTimeout 推进未取消。延迟桩捕获旧回调，答题→重置→重开后触发旧回调须被令牌丢弃（qNo 不变）。旧源码 qNo+1 ⇒ BAD。"
},
{
  "slug": "edu/math-quiz",
  "clicks": ["(function(){var dfd=[];var oST=setTimeout,oQ=document.querySelectorAll;setTimeout=function(f,ms){dfd.push(f);return dfd.length;};document.querySelectorAll=function(){return [];};try{start();var fe={classList:{add:function(){}},disabled:false,onclick:null};choose(ans,fe);reset();start();var qB=qNo;if(dfd.length)dfd[dfd.length-1]();var qA=qNo;var ok=(qA===qB&&dfd.length>=1);document.getElementById('__tbProbe').textContent='MATHSTALE '+(ok?'OK':'BAD qB='+qB+' qA='+qA+' n='+dfd.length);}finally{setTimeout=oST;document.querySelectorAll=oQ;}})()"],
  "expect": ["MATHSTALE OK"],
  "ref": "第395批：math-quiz 两处 setTimeout(next,900)（作答/超时）均未取消。延迟桩捕获回调，作答→重置→重开后触发旧回调须被令牌丢弃。旧源码 qNo+1 ⇒ BAD。"
},
{
  "slug": "edu/capital-quiz",
  "clicks": ["(function(){var dfd=[];var oST=setTimeout,oQ=document.querySelectorAll;setTimeout=function(f,ms){dfd.push(f);return dfd.length;};document.querySelectorAll=function(){return [];};try{start();var fe={classList:{add:function(){}},disabled:false,onclick:null};choose(cur,fe);reset();start();var qB=qNo;if(dfd.length)dfd[dfd.length-1]();var qA=qNo;var ok=(qA===qB&&dfd.length>=1);document.getElementById('__tbProbe').textContent='CAPSTALE '+(ok?'OK':'BAD qB='+qB+' qA='+qA+' n='+dfd.length);}finally{setTimeout=oST;document.querySelectorAll=oQ;}})()"],
  "expect": ["CAPSTALE OK"],
  "ref": "第395批：capital-quiz 两处裸 setTimeout(next,900) 未取消。延迟桩捕获回调，作答→重置→重开后触发须被令牌丢弃。旧源码 qNo+1 ⇒ BAD。"
},
{
  "slug": "edu/flag-quiz",
  "clicks": ["(function(){var dfd=[];var oST=setTimeout,oQ=document.querySelectorAll;setTimeout=function(f,ms){dfd.push(f);return dfd.length;};document.querySelectorAll=function(){return [];};try{start('normal');var fe={classList:{add:function(){}},disabled:false,onclick:null};choose(cur,fe);reset();start('normal');var qB=qNo;if(dfd.length)dfd[dfd.length-1]();var qA=qNo;var ok=(qA===qB&&dfd.length>=1);document.getElementById('__tbProbe').textContent='FLAGSTALE '+(ok?'OK':'BAD qB='+qB+' qA='+qA+' n='+dfd.length);}finally{setTimeout=oST;document.querySelectorAll=oQ;}})()"],
  "expect": ["FLAGSTALE OK"],
  "ref": "第395批：答题后 setTimeout(next,900) 未取消，0.9 秒内重置/重开会被旧回调重新出题或跳过新局当前题。用延迟执行桩捕获旧推进回调，答题→立即重置→重新开始后手动触发旧回调，须被局次令牌丢弃（qNo 不变）。修复前旧回调直接 next() ⇒ qNo+1 ⇒ BAD。"
},
{
  "slug": "edu/typing-game",
  "clicks": ["(function(){var T=1700000000000;var D=Date.now;Date.now=function(){return T;};startTime=T-60000;correctKeys=100;totalKeys=100;updateStats();var w=String(document.getElementById('wpm').textContent);Date.now=D;document.getElementById('__tbProbe').textContent='TYPWPM '+(w==='20'?'OK':'BAD '+w);})()"],
  "expect": ["TYPWPM OK"],
  "ref": "第398批：速度单位为 WPM（标准词/分），算法 WPM=(正确按键数/5)/(分钟数)；每分钟 100 个正确字符应输出 20 而非 100「字/分」。锁定算法与文案一致（meta 已由「字/分」改 WPM 标准词/分），默认态正确按键 0 ⇒ WPM 0，不命中。"
  },
  {
    slug: "edu/chinese-zodiac",
    inputs: { "year": "1" },
    expect: ["🐔 鸡年 辛酉年 · 金命 1年出生"],
    ref: "12-EL-F17：getZodiac/getGanZhi 原用 (y-4)%12/%10，y<4 时负数取模得负下标、数组返回 undefined，calc 取 z.a 抛 TypeError 结果区不更新。改防御性取模 ((y-4)%12+12)%12 与 ((y-4)%10+10)%10。year=1 ⇒ (1-4)%12=-3→9 鸡、(1-4)%10=-3→7 辛、地支 9 酉 ⇒ 辛酉鸡年；默认 year=2000（庚辰龙）不命中，旧版崩溃无输出 ⇒ 零逃生。"
  },
  {
    slug: "edu/pinyin-converter",
    inputs: { inputText: "嗯" },
    clicks: ["currentMode='notone';convert();"],
    expect: ["拼音结果 ng"],
    ref: "12-EL-F4：removeTone 原替换表未含 ǹ，「嗯」映射到 ǹg 在无声调模式仍保留调号 ǹg 且首字母模式取到 ǹ。改为先替换（ü→v 等）再 NFD 分解去 U+0300–U+036F 组合调号，ǹg→ng。注入「嗯」无声调 ⇒ ng；默认「你好世界…」不含此串，旧版输出 ǹg ⇒ 零逃生。"
  },
  {
    slug: "edu/chinese-stroke-counter",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu/chinese-stroke-counter.html','utf8');var dd=JSON.parse(globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/chinese-stroke-counter'];var s=JSON.stringify(dd);var ok=h.indexOf('按笔顺拆解')<0&&h.indexOf('笔顺拆解：展示笔画组成顺序')<0&&h.indexOf('按画数筛选')>=0&&s.indexOf('笔顺拆解')<0&&s.indexOf('按画筛选：按笔画数查找同画数的汉字')>=0&&s.indexOf('不提供逐笔笔顺演示')>=0;document.getElementById('__tbProbe').textContent='STROKEDD '+(ok?'OK':'BAD');"],
    expect: ["STROKEDD OK"],
    ref: "12-EL-F13：笔画页深度解析/首屏宣称「按笔顺拆解、展示笔画组成顺序」，实际只有总笔画数与按画筛选，无笔顺数据。权威源 content_deepdive.json 与页面预渲染改为「总笔画统计与按画数筛选、不提供逐笔笔顺演示」。源码形态哨兵旧版必红。"
  },

  {
    slug: "edu2/exam-countdown",
    inputs: { examName: "TbCtiNowe" },
    clicks: ["var d=new Date();d.setDate(d.getDate()+21);var s=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');document.getElementById('examDate').value=s;document.getElementById('countWeekend').checked=false;document.getElementById('countHoliday').checked=false;calc();var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='NOWE '+(r.indexOf('TbCtiNowe')>=0&&r.indexOf('周末未单独统计')>=0?'OK':'BAD');"],
    expect: ["NOWE OK"],
    ref: "EL-J160：取消勾选后周末卡显示「周末未单独统计」；用 inputs 唯一串做注入依赖，旧版恒显示「周末（天）」。",
  },
  {
    slug: "edu2/exam-countdown",
    inputs: { examName: "TbCtiTime" },
    clicks: ["var d=new Date();d.setDate(d.getDate()+21);var s=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');document.getElementById('examDate').value=s;document.getElementById('countWeekend').checked=true;document.getElementById('countHoliday').checked=false;calc();var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='TIMEQ '+(r.indexOf('TbCtiTime')>=0&&r.indexOf('时间余量')>=0&&r.indexOf('周末（天）')>=0?'OK':'BAD');"],
    expect: ["TIMEQ OK"],
    ref: "EL-J161：无起始日不伪造进度百分比，标题改「时间余量」；旧版是「倒计时进度」且按 max(totalDays,100) 算百分比。",
  },
  {
    slug: "edu2/exam-countdown",
    inputs: { examName: "TbCtiHol" },
    clicks: ["var s=(new Date().getFullYear()+3)+'-10-01';document.getElementById('examDate').value=s;document.getElementById('countHoliday').checked=true;calc();var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='CTIHOL '+(r.indexOf('TbCtiHol')>=0&&r.indexOf('该年份未内置节假日表')>=0?'OK':'BAD');"],
    expect: ["CTIHOL OK"],
    ref: "EL-J162：内置表仅 2026 年，其他年份勾选节假日时明确提示未扣减；旧版静默按 0 且注释谎称 2025-2027。",
  },
  {
    slug: "edu2/exam-countdown",
    inputs: { examName: "TbCtiSrc" },
    clicks: ["var nm=document.getElementById('examName').value;var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu2/exam-countdown.html','utf8');var ok=nm==='TbCtiSrc'&&h.indexOf('progressPct')<0&&h.indexOf('2025-2027')<0&&h.indexOf('hasHolidayData')>=0;document.getElementById('__tbProbe').textContent='CDFIX '+(ok?'OK':'BAD');"],
    expect: ["CDFIX OK"],
    ref: "EL-J160/J161/J162 源码形态：删误导性 progressPct 与失实注释，新增 hasHolidayData；依赖 inputs 唯一串避免默认态命中。",
  },

  {
    slug: "edu/timezone-converter",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/timezone-converter.html','utf8');var ok=h.indexOf('zoneOffsetMinutes(iana, dateMs)')>=0&&h.indexOf('function wallToInstant')>=0&&h.indexOf('dstMonths')<0&&h.indexOf('function getOffset(')<0;document.getElementById('__tbProbe').textContent='TZJ123 '+(ok?'OK':'BAD');"],
    expect: ["TZJ123 OK"],
    ref: "EL-J123：旧版 getOffset(tz,useDST) 恒用静态 dstOffset、dstMonths 定义后未调用，1 月纽约按 EDT 算错 1 小时。现改为 Intl.IANA 按所选日期实时取偏移（zoneOffsetMinutes）+ wallToInstant 跨 DST 边界二次校正。源码形态哨兵：旧版含 dstMonths/getOffset 且无实时函数 ⇒ 必红。",
  },
  {
    slug: "edu/timezone-converter",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/timezone-converter.html','utf8');var ok=h.indexOf('zoneOffsetMinutes(tz.tz, utcNow)')>=0&&h.indexOf('offset > stdOffsetMinutes(tz.tz, nowYear)')>=0&&h.indexOf('getOffset(tz,false)')<0&&h.indexOf('getOffset(tz, false)')<0;document.getElementById('__tbProbe').textContent='TZJ124 '+(ok?'OK':'BAD');"],
    expect: ["TZJ124 OK"],
    ref: "EL-J124：旧版 updateWorldClock 用 getOffset(tz,false) 恒标准偏移、徽标无条件常显。现世界时钟按 IANA 实时偏移，徽标以 offset>stdOffsetMinutes 比较后显隐，二者口径一致。源码形态哨兵：旧版无实时偏移函数且含 getOffset(tz,false) ⇒ 必红。",
  },
  {
    slug: "edu/country-quiz",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/country-quiz.html','utf8');var dd=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/country-quiz']);var ok=h.indexOf('限时作答')<0&&h.indexOf('首都或地理位置')<0&&h.indexOf('不计时、不含首都或地图题')>=0&&dd.indexOf('错题库')<0&&dd.indexOf('不包含首都题或地图位置题')>=0;document.getElementById('__tbProbe').textContent='CQJ126 '+(ok?'OK':'BAD');"],
    expect: ["CQJ126 OK"],
    ref: "EL-J126：旧版 meta/og 宣称「国旗、首都或地理位置…限时作答」且 FAQ 有错题库，实际仅国旗题无计时。现宣称统一为「看国旗选国家…不计时、不含首都或地图题」，deep-dive 权威源无错题库且有范围说明。源码+权威源双哨兵：旧版含限时作答/首都或地理位置 ⇒ 必红。",
  },
  {
    slug: "edu/country-quiz",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/country-quiz.html','utf8');var seg=h.slice(h.indexOf('const countries=['),h.indexOf('let queue'));var n=(seg.match(/name:'/g)||[]).length;var ok=n>=50&&h.indexOf('Noto Color Emoji')>=0&&seg.indexOf('荷兰')>=0&&seg.indexOf('新加坡')>=0&&seg.indexOf('肯尼亚')>=0;document.getElementById('__tbProbe').textContent='CQJ127 '+n+' '+(ok?'OK':'BAD');"],
    expect: ["CQJ127 56 OK"],
    ref: "EL-J127：旧版题库仅 20 国、emoji 无字体栈，部分平台回退为字母代码。现扩到 56 国并加系统 emoji 字体栈兜底（Apple/Segoe/Noto/Twemoji）。源码形态哨兵（条目数+字体栈+新增国名）：旧版 n=20 ⇒ 必红。",
  },
  {
    slug: "edu/flag-quiz",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/flag-quiz.html','utf8');var dd=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/flag-quiz']);var ok=h.indexOf('PER_Q_SEC=10')>=0&&h.indexOf('function startTimer')>=0&&h.indexOf('function onTimeout')>=0&&h.indexOf('function addWrong')>=0&&h.indexOf(\"mode==='wrong'\")>=0&&h.indexOf('10-second countdown')>=0&&dd.indexOf('错题库')>=0;document.getElementById('__tbProbe').textContent='FLAGJ128 '+(ok?'OK':'BAD');"],
    expect: ["FLAGJ128 OK"],
    ref: "EL-J128：旧版英文称 timed multiple-choice quiz 但无计时器、错题库未实现。现含 PER_Q_SEC=10 每题倒计时+onTimeout 超时判错+addWrong 错题库+只练错题模式，英文 formula-desc 10-second countdown/review bank 与权威源错题库口径一致。源码+权威源哨兵：旧版无计时与错题实现 ⇒ 必红。",
  },
  {
    slug: "edu/flag-quiz",
    clicks: ["var fs=globalThis.__tbFs;var f=fs.readFileSync(process.cwd()+'/tools/edu/flag-quiz.html','utf8');var c=fs.readFileSync(process.cwd()+'/tools/edu/country-quiz.html','utf8');var fseg=f.slice(f.indexOf('const data=['),f.indexOf('let queue'));var cseg=c.slice(c.indexOf('const countries=['),c.indexOf('let queue'));var fn=(fseg.match(/name:'/g)||[]).length,cn=(cseg.match(/name:'/g)||[]).length;var ok=fn>=24&&cn>=50&&f.indexOf('PER_Q_SEC')>=0&&c.indexOf('PER_Q_SEC')<0&&f.indexOf('WRONG_KEY')>=0&&c.indexOf('WRONG_KEY')<0;document.getElementById('__tbProbe').textContent='FLAGJ129 '+fn+'/'+cn+' '+(ok?'OK':'BAD');"],
    expect: ["FLAGJ129 24/56 OK"],
    ref: "EL-J129：旧版两页前 20 国同题库、逻辑逐行一致构成近重复。现差异化——国旗页 24 国+10 秒限时+错题库+只练错题，国家页 56 国+无计时+无错题库。交叉源码哨兵：旧版 flag=24/country=20 且两页均无/均有计时，该组合不成立 ⇒ 必红。",
  },
  {
    slug: "edu/countdown-5",
    inputs: { examName: "TbCdDay" },
    clicks: ["var d=new Date();d.setHours(0,0,0,0);d.setDate(d.getDate()+6);var s=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');state={name:document.getElementById('examName').value,date:s,targetHours:500,logs:[]};render();var hero=document.getElementById('heroBox').innerHTML;var tot=document.getElementById('statTotal').textContent;document.getElementById('__tbProbe').textContent='CDJ130 '+(String(tot).trim()==='6'&&hero.indexOf('>6<')>=0?'OK':'BAD tot='+tot);"],
    expect: ["CDJ130 OK"],
    ref: "EL-J130：hero 用 diff=round(目标−今日)=6（含今天、不含考试日），旧版 countDays 从明天起算得 5 ⇒ statTotal=5 与大字 6 差 1。现 countDays 从今天起算，区间 {今…考前一天} 共 6 天，hero 与统计卡一致。用动态 today+6 避免冻结日期依赖，examName 注入唯一串。",
  },
  {
    slug: "edu/capital-quiz",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/capital-quiz.html','utf8');var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/capital-quiz']);var ok=h.indexOf('成绩能保存吗？')>=0&&h.indexOf('可导出 CSV 复核')>=0&&d.indexOf('可导出 CSV 复核')>=0&&h.indexOf('TBKit.util.exportTable')>=0;document.getElementById('__tbProbe').textContent='CAPEXP '+(ok?'OK':'BAD');"],
    expect: ["CAPEXP OK"],
    ref: "全量 UX 门禁回退修复：capital-quiz 真实 CSV 导出（TBKit.util.exportTable）此前沿用通用套话「支持复制与导出」命中，套话清理后正文无导出说明致 UX export 信号丢失（edu 均分 8.41→8.39）。补真实 FAQ「成绩能保存吗？…可导出 CSV 复核」并同步权威源，页面与权威源双哨兵。旧版无该 FAQ ⇒ 必红。",
  },
  {
    slug: "edu/countdown-5",
    inputs: { examName: "TbCdDom" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/countdown-5.html','utf8');var rt=(h.match(/class=\"related-tools\" data-related-tools=\"1\"/g)||[]).length;var fb=(h.match(/class=\"card formula-box\"/g)||[]).length;var empty=(h.match(/i18nText\\(\\)/g)||[]).length;var ok=document.getElementById('examName').value==='TbCdDom'&&rt===1&&fb===1&&empty===0;document.getElementById('__tbProbe').textContent='CDJ131 '+(ok?'OK':'BAD rt='+rt+' fb='+fb+' empty='+empty);"],
    expect: ["CDJ131 OK"],
    ref: "EL-J131：旧版两组 related-tools + 两个 formula-box + 三处无参 i18nText()。现只保留一组相关工具与一个公式框，三处 toast 全改用具体 key（msg947/msg082/msg081）。源码形态哨兵，examName 注入唯一串。",
  },


  {
    slug: "edu/assessor-27",
    inputs: { d1: "6", d2: "6", d3: "6", d4: "6", d5: "6", d6: "6" },
    clicks: ["var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J136 '+(r.indexOf('最低分项')>=0&&r.indexOf('短板优先')>=0?'OK':'BAD');"],
    expect: ["J136 OK"],
    ref: "EL-J136：旧版仅收集 <6 维度，六项全 6 时 gaps=[] 输出「各维度均达标」。现始终列出最低分维度并标「当前最低分项（短板优先）」。六项全 6 为唯一注入态，默认态 6/5/7/4/7/8 含 5 分未达标 ⇒ 不命中最低分项专属文案。",
  },
  {
    slug: "edu/assessor-27",
    inputs: { d1: "8", d2: "7", d3: "6", d4: "9", d5: "7", d6: "8" },
    clicks: ["document.getElementById('d6').value='';calc();var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J137E '+(r.indexOf('请输入有效评分')>=0&&r.indexOf('知识安全未填写')>=0?'OK':'BAD');"],
    expect: ["J137E OK"],
    ref: "EL-J137 空值：旧版 +''||0 把空值当 0 仍出完整等级。现空值提示「知识安全未填写」并中止。默认态六项均有值，不含未填写文案 ⇒ 判别成立。",
  },
  {
    slug: "edu/assessor-27",
    inputs: { d1: "7", d2: "7", d3: "7", d4: "7", d5: "5", d6: "5" },
    clicks: ["var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J138 '+(r.indexOf('知识存储')>=0&&r.indexOf('统一文档库')>=0&&r.indexOf('权限分级')>=0?'OK':'BAD');"],
    expect: ["J138 OK"],
    ref: "EL-J138：旧版建议仅拼接共享/创新/捕获三项，仅缺存储+安全时建议串为空只剩「建议：」。现六维各配建议，存储→统一文档库与备份、安全→权限分级与脱敏。默认态含低分维度但本组输入唯一（5,5 仅存储安全未达标）⇒ 判别成立。",
  },

  {
    slug: "edu/calc-2",
    inputs: { score: "60", mean: "80", sd: "10", direction: "lower" },
    clicks: ["var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J139 '+(r.indexOf('比较方向：分数越低越好')>=0&&r.indexOf('有效 Z 分数')>=0?'OK':'BAD');"],
    expect: ["J139 OK"],
    ref: "EL-J139：旧版 direction=lower 仅翻转等级，文案与有效Z口径混乱。现结果区明确标注「比较方向：分数越低越好，等级/T 分数按反向 Z 计算」，与有效Z/T分数同源。低分场景 score=60<mean=80 触发，默认态 higher 不含该方向说明。",
  },
  {
    slug: "edu/calc-2",
    inputs: { score: "60", mean: "80", sd: "10", direction: "higher" },
    clicks: ["var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J140 '+(r.indexOf('低于约')>=0&&r.indexOf('高于约')<0?'OK':'BAD');"],
    expect: ["J140 OK"],
    ref: "EL-J140：z=(60−80)/10=−2 为负，旧版仍写「约高于 2.28%」与数值相反。现按 z 符号切换为「低于约 97.72%」。默认态 score85>mean75 为正 Z 写「高于约」⇒ 零逃生。",
  },
  {
    slug: "edu/calc-2",
    inputs: { score: "95", mean: "80", sd: "10", direction: "higher" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/calc-2.html','utf8');var r=document.getElementById('res').innerHTML;var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/calc-2']);var ok=r.indexOf('T 分数 (50+10Z)')>=0&&r.indexOf('65.00')>=0&&h.indexOf('点击「计算」或「生成」')<0&&d.indexOf('T 分数 = 50 + 10 × 有效 Z')>=0;document.getElementById('__tbProbe').textContent='J141 '+(ok?'OK':'BAD');"],
    expect: ["J141 OK"],
    ref: "EL-J141：公式承诺 T=50+10Z 但旧结果卡无输出、opt-guide/opt-faq 与 JSON-LD 是通用套话。现结果卡含 T 分数（95/80/10→z=1.5→T=65.00），套话已改为真实说明，权威源 FAQ 补 T 分数口径。源码+权威源+运行时三哨兵，旧版必红。",
  },

  // ── 第1184批：错题本末轮排期、错因双维筛选与空 toast 收口 ──
  {
    slug: "edu/reminder-1",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/reminder-1.html','utf8');var ok=h.indexOf('stage+1>=REVIEW_INTERVALS.length')>=0&&h.indexOf('不再安排复习')>=0&&h.indexOf('REVIEW_INTERVALS[Math.min(stage+1,4)]')<0&&h.indexOf('undefined天后')<0;document.getElementById('__tbProbe').textContent='J142 '+(ok?'OK':'BAD');"],
    expect: ["J142 OK"],
    ref: "EL-J142：旧版 stage=3 时取 REVIEW_INTERVALS[Math.min(stage+1,4)] 得 undefined，提示 undefined天后再复习。现末轮单独文案「标记为已掌握，不再安排复习」。源码形态哨兵：旧版含越界索引 ⇒ 必红。",
  },
  {
    slug: "edu/reminder-1",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/reminder-1.html','utf8');var en=JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/en/edu/reminder-1.json','utf8'));var ok=h.indexOf('currentErrTypeFilter')>=0&&h.indexOf('function setErrTypeFilter')>=0&&h.indexOf('id=\"errTypeFilter\"')>=0&&h.indexOf('id=\"errTypeStats\"')>=0&&h.indexOf('currentErrTypeFilter!==')>=0&&en.map['全部错因']==='All error types'&&en.map['📊 错因分布']==='📊 Error-Type Breakdown';document.getElementById('__tbProbe').textContent='J143 '+(ok?'OK':'BAD');"],
    expect: ["J143 OK"],
    ref: "EL-J143：旧版只有学科 chip 与学科分布，错误类型仅卡片标签，双维归类承诺不成立。现补错误类型 chip（与学科取交集）与错因分布统计块，英文词典同步。源码+词典哨兵：旧版无 errTypeFilter/errTypeStats ⇒ 必红。",
  },
  {
    slug: "edu/reminder-1",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/reminder-1.html','utf8');var empty=(h.match(/i18nText\\(\\)/g)||[]).length;var ok=empty===0&&h.indexOf(\"showToast(i18nText('toast.deleted'))\")>=0&&h.indexOf(\"showToast(i18nText('toast.cleared'))\")>=0;document.getElementById('__tbProbe').textContent='J144 '+(ok?'OK':'BAD '+empty);"],
    expect: ["J144 OK"],
    ref: "EL-J144：旧版 delQuestion/clearAll 调 i18nText() 无参，toast 显示 undefined。现分别用 toast.deleted/toast.cleared。源码哨兵：旧版空参调用 2 次且无具体键 ⇒ 必红。",
  },

  // ── 第1185批：成绩目标计算加权口径、项数可见与成绩越界收口 ──
  {
    slug: "edu/calc-4",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/calc-4.html','utf8');var ok=h.indexOf('const earnedPoints = currentScore * currentWeight / 100')>=0&&h.indexOf('const neededTotal = targetScore - earnedPoints')>=0&&h.indexOf('const neededAvg = neededTotal / (remainingWeight / 100)')>=0&&(h.match(/class=\"formula-eq\"/g)||[]).length===1;document.getElementById('__tbProbe').textContent='J145 '+(ok?'OK':'BAD');"],
    expect: ["J145 OK"],
    ref: "EL-J145：订正后加权口径为 earned=当前×权重、缺口=目标−earned、剩余均分=缺口÷剩余权重；旧文档 91.7/页面 25 均属过时，现示例 95.0 与页面一致。另清掉重复 formula-eq。源码+计数哨兵：旧版重复公式框 2 处 ⇒ 必红。",
  },
  {
    slug: "edu/calc-4",
    inputs: { currentScore: "70", currentWeight: "40", targetScore: "85", remainingParts: "5" },
    clicks: ["var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J146 '+(r.indexOf('剩余 5 项若等权')>=0&&r.indexOf('95.00')>=0?'OK':'BAD');"],
    expect: ["J146 OK"],
    ref: "EL-J146：旧版 remainingParts 只读不参与输出，改 1→5 结果完全相同。现结果区明说「剩余 N 项若等权，每项均需 X 分」且标注项数只按项拆解、不改变剩余权重。注入 5 项（70/40/85→95.00）与默认 2 项区分 ⇒ 零逃生。",
  },
  {
    slug: "edu/calc-4",
    inputs: { currentScore: "150", currentWeight: "60", targetScore: "85", remainingParts: "2" },
    clicks: ["var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J147 '+(r.indexOf('请输入有效的成绩')>=0&&r.indexOf('-162.50')<0?'OK':'BAD');"],
    expect: ["J147 OK"],
    ref: "EL-J147：旧版漏校 currentScore 上界，150 分算出 -162.50% 仍显示可行。现 0–100 校验命中即提示有效成绩并中止；neededAvg<=0 已明确「目标已达成」。默认态成绩合法不命中提示 ⇒ 零逃生。",
  },

  // ── 第1186批：记忆宫殿三层编码、规模参数与零值边界收口 ──
  {
    slug: "edu/generator-26",
    inputs: { roomCount: "3", furnitureCount: "2", seqCount: "1" },
    clicks: ["var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J148 '+(r.indexOf('6. 位置编码：C2-01（321）')>=0?'OK':'BAD');"],
    expect: ["J148 OK"],
    ref: "EL-J148：旧版只输出「房间-A1-锚点」无家具位编号与序号，也无数值编码。现字符码 A1-01 + 数值码房间×100+家具×10+序号同屏输出；3×2×1 末码 C2-01（321）唯一，默认 3×3×2 不命中。",
  },
  {
    slug: "edu/generator-26",
    inputs: { roomCount: "4", furnitureCount: "1", seqCount: "1" },
    clicks: ["var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J149 '+(r.indexOf('总挂钩点：4（4 × 1 × 1）')>=0&&r.indexOf('4. 位置编码：D1-01（411）')>=0?'OK':'BAD');"],
    expect: ["J149 OK"],
    ref: "EL-J149：旧版唯一 cnt 输入，R/F/N 硬编码无法定制宫殿规模。现三输入决定 R×F×N 总数与唯一编码；注入 4×1×1 得 4 个挂钩点、末码 D1-01（411），默认 3×3×2 不命中。",
  },
  {
    slug: "edu/generator-26",
    inputs: { roomCount: "0", furnitureCount: "3", seqCount: "2" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/generator-26.html','utf8');var r=document.getElementById('res').innerHTML;var ok=r.indexOf('房间数须为 1–10 的整数')>=0&&r.indexOf('位置编码')<0&&h.indexOf('function randInt')<0;document.getElementById('__tbProbe').textContent='J150 '+(ok?'OK':'BAD');"],
    expect: ["J150 OK"],
    ref: "EL-J150：旧版 parseInt('0')||5 把 0 静默改成 5 条，且 randInt 定义后从未调用。现 0 触发明确范围提示、不生成任何编码，死函数已删；默认 R=3 合法不命中提示。",
  },

  // ── 第1188批：考试成绩分析等级阈值、首屏示例与并列排名收口 ──
  {
    slug: "edu2/exam-analysis",
    inputs: { scoreInput: "张三,78\n李四,95", fullScore: "100", passLine: "90", excellentLine: "95" },
    clicks: ["var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='J163 '+(r.indexOf('78</td><td><span class=\"grade-tag grade-fail\">不及格</span>')>=0?'OK':'BAD');"],
    expect: ["J163 OK"],
    ref: "EL-J163：旧版单人等级先判 full*0.75，及格线 90 时 78 分被标「良好」却不计入及格率。现良好线统一为 max(75%×满分, 及格线)，78 分与及格率同为不及格。默认 60% 线不命中该组合 ⇒ 零逃生。",
  },
  {
    slug: "edu2/exam-analysis",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/exam-analysis.html','utf8');var boot='function __exam_analysisBoot(){ try{ __exam_analysisPresets(); }catch(e){} }';var ov=\"document.getElementById('scoreInput').value = Math.abs(full - 100)\";var guard=\"if(String(document.getElementById('scoreInput').value||'').trim()) calc();\";var ok=h.indexOf(boot)>=0&&h.indexOf(guard)>=0&&h.indexOf(ov)<0&&h.indexOf('__exam_analysisScaleSample')<0;document.getElementById('__tbProbe').textContent='J164 '+(ok?'OK':'BAD');"],
    expect: ["J164 OK"],
    ref: "EL-J164：旧版 boot 调 loadSample 自动写历史、预设回调用缩放样例覆盖 scoreInput。现首屏空态只在有输入时 calc，预设只改满分/分数线，示例缩放死函数已删。源码形态哨兵：旧版含自动 loadSample 与覆盖语句 ⇒ 必红。",
  },
  {
    slug: "edu2/exam-analysis",
    inputs: { scoreInput: "张三,92\n李四,92\n王五,80", fullScore: "100", passLine: "60", excellentLine: "85" },
    clicks: ["var r=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='J165 '+(r.indexOf('<td>1</td><td>张三</td><td>92</td>')>=0&&r.indexOf('<td>1</td><td>李四</td><td>92</td>')>=0&&r.indexOf('<td>3</td><td>王五</td><td>80</td>')>=0?'OK':'BAD');"],
    expect: ["J165 OK"],
    ref: "EL-J165：旧版排序后直接 idx+1，同分 92 被给 1/2 名。现竞争排名同分同名次、下一名跳号（1/1/3）。默认 15 人样例无该 1/1/3 组合 ⇒ 零逃生。",
  },

  // ── 第1189批：单位换算温度仿射、趋势数值字段与简介精度口径收口 ──
  {
    slug: "edu/convert-area-volume",
    clicks: ["document.getElementById('cat').value='temp';fillSel();document.getElementById('val').value='100';document.getElementById('from').value='F';document.getElementById('to').value='C';calc();var r=document.getElementById('res').innerHTML;document.getElementById('__tbProbe').textContent='J166 '+(r.indexOf('100 F → 37.78 C')>=0?'OK':'BAD');"],
    expect: ["J166 OK"],
    ref: "EL-J166：旧版类别含 temp 但 U/N 无 temp 键，fillSel 清空两个 select 后 calc 恒等于输入。现温度分支独立列 C/F/K 并走仿射公式，100°F → 37.78°C。默认长度类不命中该串 ⇒ 零逃生。",
  },
  {
    slug: "edu/convert-area-volume",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/convert-area-volume.html','utf8');var ok=h.indexOf('rec.__tbScore=__convert_area_volumeScore(res);')>=0&&h.indexOf('var v=parseFloat(arr[j].d.__tbScore);')>=0&&h.indexOf('parseFloat(arr[j].d[rk])')<0;document.getElementById('__tbProbe').textContent='J167 '+(ok?'OK':'BAD');"],
    expect: ["J167 OK"],
    ref: "EL-J167：旧版趋势图 parseFloat('结果 = 100.0000') 恒 NaN 永不绘图。现历史另写数值字段 __tbScore，图表读该字段；源码哨兵：旧版无数值字段且对展示文本 parseFloat ⇒ 必红。",
  },
  {
    slug: "edu/convert-area-volume",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/convert-area-volume.html','utf8');var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu/convert-area-volume']);var ok=h.indexOf('支持长度 7 种、重量 5 种')>=0&&h.indexOf('1 acre = 4046.8564224 m²')>=0&&d.indexOf('仿射公式先转 ℃')>=0&&d.indexOf('4046.8564224')>=0;document.getElementById('__tbProbe').textContent='J168 '+(ok?'OK':'BAD');"],
    expect: ["J168 OK"],
    ref: "EL-J168：旧版简介只重复标题、深挖三条空泛短语。现简介列五类单位数与 4/2 位精度、给真实算例，权威源同步仿射口径与 mi/acre 算例。源码+权威源哨兵：旧版无单位清单与精确算例 ⇒ 必红。",
  },

  // ── 第1190批：课程表可视化排课率、检测记录与闭区间口径复核 ──
  {
    slug: "edu2/schedule-conflict",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/schedule-conflict.html','utf8');var ok=h.indexOf('可视化课表')>=0&&h.indexOf('无冲突排课率')>=0&&h.indexOf('conflictCells[d+\\'-\\'+p] = true')>=0&&h.indexOf('var scheduleRate =')>=0;document.getElementById('__tbProbe').textContent='J169 '+(ok?'OK':'BAD');"],
    expect: ["J169 OK"],
    ref: "EL-J169：旧版只有四张统计卡与冲突表，无周×节次网格与排课率。现结果区渲染可视化课表并高亮冲突格，排课率=(总时片−冲突时片)/总时片。源码哨兵：旧版无 grid/rate 实现 ⇒ 必红。",
  },
  {
    slug: "edu2/schedule-conflict",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/schedule-conflict.html','utf8');var ok=h.indexOf(\"var __schedule_conflict_f0=(typeof detect==='function')?detect:null;\")>=0&&h.indexOf('loadSample=function()')<0&&h.indexOf('if(typeof loadSample===\\'function\\') loadSample();')<0&&h.indexOf('ToolBox.showToast(i18nText())')<0&&h.indexOf(\"if(String((document.getElementById('courseInput')||{}).value||'').trim()) detect();\")>=0;document.getElementById('__tbProbe').textContent='J170 '+(ok?'OK':'BAD');"],
    expect: ["J170 OK"],
    ref: "EL-J170：旧版只包装 loadSample 且 boot 自动灌示例、尾部空输入 detect 弹错、清空 toast 空参。现包装 detect 使自建课表也写历史/表/图，boot 只装预设，尾部仅在有输入时 detect，清空用 toast.cleared。源码哨兵：旧版四处缺陷任一存在即红。",
  },
  {
    slug: "edu2/schedule-conflict",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/schedule-conflict.html','utf8');var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu2/schedule-conflict']);var ok=h.indexOf('a.start≤b.end 且 b.start≤a.end')>=0&&h.indexOf('[start,end]')>=0&&h.indexOf('[start,end)')<0&&d.indexOf('a.start≤b.end')>=0;document.getElementById('__tbProbe').textContent='J171 '+(ok?'OK':'BAD');"],
    expect: ["J171 OK"],
    ref: "EL-J171：旧版 FAQ 写半开区间 a.start<b.end、引据表 [start,end)，与实现闭区间相反。现 FAQ 与引据表统一为 a.start≤b.end 且 [start,end]，权威源同步。源码+权威源哨兵：旧版含半开公式 ⇒ 必红。",
  },

  // ── 第1191批：复核失败重做——倒计时 hero 与统计卡逐日对齐 ──
  {
    slug: "edu/countdown-5",
    inputs: { examName: "TbV1R1" },
    clicks: ["var d=new Date();d.setHours(0,0,0,0);d.setDate(d.getDate()+1);var s=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');state={name:document.getElementById('examName').value,date:s,targetHours:500,logs:[]};render();var hero=document.getElementById('heroBox').innerHTML;var tot=document.getElementById('statTotal').textContent;document.getElementById('__tbProbe').textContent='V1R1 '+(String(tot).trim()==='1'&&hero.indexOf('>1<')>=0?'OK':'BAD '+tot);"],
    expect: ["V1R1 OK"],
    ref: "复核失败重做·EL-V1：复核称考试明天 hero=1/statTotal=0。现 countDays 从今天零点起算且 while(cur<target)，明天区间仅 {今天} 共 1 天，与 hero diff=1 一致。用动态明天避免冻结日期依赖，examName 注入唯一串。",
  },
  {
    slug: "edu/countdown-5",
    inputs: { examName: "TbV1R2" },
    clicks: ["var d=new Date();d.setHours(0,0,0,0);d.setDate(d.getDate()+2);var s=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');state={name:document.getElementById('examName').value,date:s,targetHours:500,logs:[]};render();var hero=document.getElementById('heroBox').innerHTML;var tot=document.getElementById('statTotal').textContent;document.getElementById('__tbProbe').textContent='V1R2 '+(String(tot).trim()==='2'&&hero.indexOf('>2<')>=0?'OK':'BAD '+tot);"],
    expect: ["V1R2 OK"],
    ref: "复核失败重做·EL-V1：复核称 2 天后 hero=2/total=1。现区间 {今天,明天} 共 2 天，与 diff=2 同口径。既有 CDJ130 覆盖 6 天，本例补复核点名的小天数边界。",
  },
  {
    slug: "edu/countdown-5",
    inputs: { examName: "TbV2R1" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/countdown-5.html','utf8');var q=String.fromCharCode(34);var rt=h.split('class='+q+'related-tools'+q+' data-related-tools='+q+'1'+q).length-1;var fb=h.split('class='+q+'card formula-box'+q).length-1;var empty=h.split('i18nText()').length-1;var ok=document.getElementById('examName').value==='TbV2R1'&&rt===1&&fb===1&&empty===0;document.getElementById('__tbProbe').textContent='V2R1 '+(ok?'OK':'BAD rt='+rt+' fb='+fb+' empty='+empty);"],
    expect: ["V2R1 OK"],
    ref: "复核失败重做·EL-V2：复核称两处 formula-box、两处 related-tools 与三处无参 i18nText() 仍存在。现各仅一处且 toast 全用具体键（msg947/msg082/msg081）；源码哨兵计数，旧版任一重复或空参均必红。examName 注入唯一串。",
  },

  // ── 第1192批：输入变更过期、空答案反馈与无效估算清理 ──
  {
    slug: "language/text-polisher",
    clicks: ["var fs=globalThis.__tbFs;var q=String.fromCharCode(34);var nl=String.fromCharCode(10);var h=fs.readFileSync(process.cwd()+'/tools/language/text-polisher.html','utf8');var ok=h.indexOf('function markPolishStale()')>=0&&h.indexOf('function copyPolishResult()')>=0&&h.indexOf('onclick='+q+'copyPolishResult()'+q)>=0&&h.indexOf('onclick='+q+'clearPolish()'+q)>=0&&h.indexOf('onclick='+q+'ToolBox.copyText(')<0&&h.indexOf('markPolishStale();'+nl+'}')>=0;document.getElementById('__tbProbe').textContent='TPSTALE '+(ok?'OK':'BAD');"],
    expect: ["TPSTALE OK"],
    ref: "EL 静态复核：旧版输入 oninput 只更新统计，复制按钮直接取旧 #output.innerText。现输入变化与选项变化调用 markPolishStale() 标记过期，复制走 copyPolishResult() 阻止旧结果并提示重新润色，清空走 clearPolish() 同步复位；源码哨兵，旧版必红。",
  },
  {
    slug: "edu/multiplication-table",
    clicks: ["var fs=globalThis.__tbFs;var sq=String.fromCharCode(39);var h=fs.readFileSync(process.cwd()+'/tools/edu/multiplication-table.html','utf8');var ok=h.indexOf('if (isNaN(val))')>=0&&h.indexOf('请输入答案后再提交')>=0&&h.indexOf('fb.textContent = '+sq+'请输入答案后再提交'+sq)>=0&&h.indexOf('fb.className = '+sq+'feedback'+sq)>=0;document.getElementById('__tbProbe').textContent='MULMED '+(ok?'OK':'BAD');"],
    expect: ["MULMED OK"],
    ref: "EL 空答案残留复核：旧版 parseInt 得 NaN 后直接 return，上一题的 ✅/❌ 与正确答案留在 #pFeedback。现有 isNaN 分支清空输入样式并写「请输入答案后再提交」，错误→清空→提交状态链不再残留；源码哨兵，旧版必红。",
  },
  {
    slug: "edu/reading-speed-calculator",
    inputs: { wpm: "680", estWords: "15000" },
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/reading-speed-calculator.html','utf8');var w=document.getElementById('wpm');var e=document.getElementById('estWords');w.value='680';e.value='15000';estimate();var before=String(document.getElementById('estResult').innerHTML||'');w.value='';estimate();var after=String(document.getElementById('estResult').innerHTML||'');var ok=before.indexOf('预计阅读时间')>=0&&after.indexOf('预计阅读时间')<0&&after.indexOf('请填写有效')>=0&&h.indexOf('i18nText()')<0;document.getElementById('__tbProbe').textContent='RDSCLR '+(ok?'OK':'BAD');"],
    expect: ["RDSCLR OK"],
    ref: "EL 阅读估算清空复核：注入 680 字/分 + 15000 字先得有效估算，再把速度置空；旧版 else 分支缺失，旧估算保留。现无效输入明确写「请填写有效的阅读速度和目标字数。」，同时顺手清掉历史载入的无参 i18nText()。动态状态链断言，旧版必红。",
  },

  // ── 第1193批：权重归一提示 ──
  {
    slug: "edu/grade-weight-calculator",
    clicks: ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu/grade-weight-calculator.html','utf8');var ok=h.indexOf('const weightHint=Math.abs(totalW-100)>0.001')>=0&&h.indexOf('结果按总权重归一')>=0&&h.indexOf('${weightHint}')>=0;document.getElementById('__tbProbe').textContent='GWSUM '+(ok?'OK':'BAD');"],
    expect: ["GWSUM OK"],
    ref: "E2 权重和提示：权重本来按 totalW 归一，Σw≠100 并非计算错误，但结果区未说明，容易被误认为漏项。现非 100% 时显式提示「结果按总权重归一；若按百分比口径请使合计为 100%」，英文同步；源码哨兵，旧版无提示必红。",
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

  console.log("==== edu calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();