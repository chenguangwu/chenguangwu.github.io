#!/usr/bin node
"use strict";
const fs = require("fs");
const { runCase } = require("./verify_it_calc.js");
globalThis.__tbFs = fs;
const CASES = [
// ── 第1173批：成绩分析多分数解析、0分线、超满分提示与算例精度 ──
{
  "slug": "edu2/exam-analysis",
  "inputs": { "scoreInput": "92,85,78,88" },
  "expect": ["4 参考人数", "85.8 平均分"],
  "ref": "EL-J108：整行逗号分隔的纯分数须拆成 4 名学生，均值 (92+85+78+88)/4=85.75→85.8；旧版只取第二个数当分数且把首数当姓名，得 1 人/85.0。默认 loadSample 为 15 人 ⇒ 零逃生。"
},
{
  "slug": "edu2/exam-analysis",
  "inputs": { "passLine": "0", "excellentLine": "0", "scoreInput": "甲,92\n乙,58" },
  "expect": ["100.0% 及格率", "100.0% 优秀率"],
  "ref": "EL-J109：及格线与优秀线填 0 须按 0% 生效，两人均达标；旧版 parseFloat||60/85 会回退成 60/85 分，得 50.0%/0.0%。默认 60/85 不命中。"
},
{
  "slug": "edu2/exam-analysis",
  "inputs": { "scoreInput": "甲,105\n乙,90" },
  "expect": ["有 1 个分数超过满分 100"],
  "ref": "EL-J110：超满分须给出明确提示并归入最高分段；旧版分段上界 full+1 使 105 不入任何段，分段人数之和小于参考人数。默认样例无超满分。"
},
{
  "slug": "edu2/exam-analysis",
  "inputs": { "fullScore": "110" },
    "clicks": ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/exam-analysis.html','utf8');var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu2/exam-analysis']);var sq=String.fromCharCode(39);var boot='if(String(document.getElementById('+sq+'scoreInput'+sq+').value||'+sq+sq+').trim()) calc();';var ok=d.indexOf('均值=78.4')>=0&&d.indexOf('78.38')<0&&h.indexOf('已清空输入')>=0&&h.indexOf('__exam_analysisScaleSample')<0&&h.indexOf(boot)>=0;document.getElementById('__tbProbe').textContent='JDOC:'+(ok?'OK':'BAD');"],
    "expect": ["JDOC:OK"],
    "ref": "EL-J112：权威源算例均值精度须与页面 toFixed(1) 一致（78.4），清空须有 Toast；第1188批又删掉 __exam_analysisScaleSample 并取消首屏自动载样，现改为断言缩放样例函数不存在且只有 scoreInput 非空才 calc()。旧版保留样例缩放函数并首屏自动载样 ⇒ 必红。"
},
{
    "slug": "edu2/exam-analysis",
    "clicks": ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'fullScore',type:'text',value:''},{id:'scoreInput',type:'textarea',value:'张三,92'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};var __r=document.getElementById('result');__r.textContent='平均分 85.5 · 及格率 90%';__r.style=__r.style||{};__r.style.display='none';__exam_analysis_last=0;__exam_analysisExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='EXAMHIDE n='+__cap.length;"],
    "expect": ["EXAMHIDE n=0"],
    "ref": "复核失败重做·考试隐藏旧结果被采集：清空满分后 calc() 只隐藏 #result 并弹 Toast，旧结果文本仍留在隐藏容器；旧 ResText 照读 ⇒ 写历史且同值去重连失败都不记，CSV 保留旧通过结果。修复后 ResText 判 style.display==='none' 直接返回 '' ⇒ 失效态不入账。用例把结果区置为旧有效文本再隐藏走真实 Extras；修复前 n=1、修复后 n=0，默认态无探针串 ⇒ 零逃生。"
  },
{
  "slug": "edu2/exam-analysis",
  "inputs": {
    "fullScore": "120",
    "passLine": "50",
    "excellentLine": "80",
    "scoreInput": "甲,108\n乙,96\n丙,90\n丁,72\n戊,60"
  },
  "clicks": [
    "calc()"
  ],
  "expect": [
    "85.2 平均分",
    "17.14 标准差",
    "100.0% 及格率"
  ],
  "ref": "满分 120 / 及格线 50% / 优秀线 80% ⇒ 及格分 60、优秀分 96；5 人 108/96/90/72/60 ⇒ 均值 426/5=85.2、标准差 √(1468.8/5)=17.14、及格 5/5=100.0%、优秀 2/5=40.0%（独立复算）。默认走 loadSample 15 人（74.9 / 14.24 / 80.0%）⇒ 三个锚点全不命中。原 expect「不及格」由 loadSample 兜底渲染的等级词产出（常量）⇒ 已替换。**注意不锚 40.0%** —— 该串在默认兜底段（60% 以下 6/15）同样出现，无判别力。"
},
{
  "slug": "edu2/exam-countdown",
  "inputs": {
    "examName": "高考_X"
  },
  "expect": [
    "高考_X"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "edu2/schedule-conflict",
  "inputs": {
    "courseInput": "物理,王老师,D401,2,1,2\n化学,王老师,E502,2,1,2\n生物,赵老师,D401,2,1,2\n历史,孙老师,F603,4,1,2"
  },
  "clicks": [
    "detect()"
  ],
  "expect": [
    "物理（D401） 化学（E502）",
    "D401 物理（王老师） 生物（赵老师）"
  ],
  "ref": "4 条课程两两比对：物理·化学 同为周二第 1-2 节且同教师王老师 ⇒ 教师冲突 1；物理·生物 同为周二第 1-2 节且同教室 D401 ⇒ 教室冲突 1；历史在周四 ⇒ 无冲突（独立复算）。默认走 loadSample 8 条（0/0/无冲突）⇒ 两个锚点不命中；且样本课程名与锚点无交集（样本含「物理,王老师,A101」但无全角括号写法）⇒ 原 expect「A101」是 sample 文本常量 ⇒ 已替换。"
},
{
  "slug": "edu2/wrong-book",
  "inputs": {
    "filterStatus": "pending"
  },
  "clicks": [
    "data=[{id:'w1',subject:'数学',type:'选择题',question:'函数定义域求解',reason:'粗心',answer:'x>0',status:'pending',created:'2026-09-01',reviewDate:'2026-09-30'},{id:'w2',subject:'英语',type:'完形填空',question:'词义辨析',reason:'词汇量不足',answer:'选B',status:'mastered',created:'2026-09-05',reviewDate:'2026-09-25'},{id:'w3',subject:'数学',type:'解答题',question:'导数应用求极值',reason:'概念不清',answer:'先求导',status:'reviewing',created:'2026-09-10',reviewDate:'2026-09-28'}];render()"
  ],
  "expect": [
    "数学（1 题）",
    "函数定义域求解",
    "解析：x>0"
  ],
  "ref": "顶层 var data 用 clicks 覆写三条（pending / reviewing / mastered 各一）+ filterStatus=pending（非默认「全部状态」）⇒ filtered 只剩 1 条 ⇒ 列表渲染「数学（1 题）」与题目、解析文本（独立复算：bySubject 按 filtered 分组）。默认 data 为空、filterStatus 为空 ⇒ 只渲染「暂无错题…」（0 错题总数）⇒ 三个锚点全不命中。原 expect「pending」是 fStatus 下拉的 option value 常量 ⇒ 已替换。**不锚 dueCount 与「剩 N 天」** —— 依赖运行日、日期一变即失效。注：兜底阶段无参调用 loadData() 会用桩 getItem(null) 清空 data，但 expect 在阶段 2 已判定（同 BATCH103 的 assessor-risk-8）。"
}
,
{
  "slug": "edu2/study-progress",
  "inputs": {"targetDate":"2026-12-31","dailyHours":"6"},
  "expect": ["2024-07-31 预计完成日", "46 天 预计还需"],
  "ref": "注入非默认 targetDate(默认 2024-07-30→2026-12-31) 与 dailyHours(默认 4→6)：预计完成日 2024-08-22→2024-07-31（dailyHours=6 加快进度提前完成）、预计还需 68 天→46 天（剩余工时/每日时长）。页面用默认 sample 4 科目(数学/英语/专业课/政治) 数据，calc 读 targetDate/dailyHours 纯 input（不依赖 now，稳定）。**锚 now 无关的计算结果**，规避 (a) 输入回显 2026-12-31（out 开头）(b) 距目标天数 929 依赖 harness 固定 now（未来 now 基准变化即失效）。默认态不命中 2024-07-31 / 46 天。"
},
{
  "slug": "language/idiom-solitaire",
  "clicks": [
    "gameMode='pinyin';gameRunning=true;currentChar='力';score=0;document.getElementById('idiomInput').value='刻骨铭心';submitIdiom();var w=document.getElementById('waitingChar').innerHTML;document.getElementById('chainList').textContent='IDIOM_MISS:'+(gameRunning?1:0)+'|SCORE='+score+'|END='+(w.indexOf('游戏结束')>=0?1:0);"
  ],
  "expect": [
    "IDIOM_MISS:0|SCORE=0|END=1"
  ],
  "ref": "EL-J10 回归：拼音模式下 currentChar='力'、输入「刻骨铭心」（首字「刻」），两者都不在 PINYIN_MAP 中。旧实现 inputPy===targetPy 即 undefined===undefined 放行；新实现缺拼音时退回汉字相同判定，首字不同 ⇒ 拒绝并结束，比分保持 0。"
},
{
  "slug": "language/idiom-solitaire",
  "clicks": [
    "gameMode='exact';gameRunning=true;currentChar='一';score=0;document.getElementById('idiomInput').value='一马当';submitIdiom();var w=document.getElementById('waitingChar').innerHTML;document.getElementById('chainList').textContent='IDIOM_DB:'+(gameRunning?1:0)+'|SCORE='+score+'|END='+(w.indexOf('游戏结束')>=0?1:0);"
  ],
  "expect": [
    "IDIOM_DB:0|SCORE=0|END=1"
  ],
  "ref": "EL-J10 回归：不在成语库的残缺输入「一马当」必须拒绝并提示，不能因首字匹配而加分。"
},
{
  "slug": "language/idiom-solitaire",
  "clicks": [
    "chain=[];gameMode='exact';gameRunning=true;currentChar='一';score=0;document.getElementById('idiomInput').value='一马当先';submitIdiom();document.getElementById('chainList').textContent='IDIOM_OK:'+(gameRunning?1:0)+'|SCORE='+score;"
  ],
  "expect": [
    "IDIOM_OK:1|SCORE=1"
  ],
  "ref": "EL-J10 正向对照：合法成语「一马当先」仍应计分并继续游戏，避免修复把正常接龙一并拒掉。"
},
{
  "slug": "language/idiom-solitaire",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/language/idiom-solitaire.html','utf8');var m=h.match(/var IDIOM_DB = \\[([\\s\\S]*?)\\n\\];/);var a=JSON.parse('['+m[1]+']');var ok=a.length===883&&a.every(function(x){return x.length===4})&&new Set(a).size===a.length;document.getElementById('chainList').textContent='JIDIOM:'+(ok?'OK':'BAD');"],
  "expect": ["JIDIOM:OK"],
  "ref": "EL-J11：词库须全四字且无重复（清理后 883 条）；旧版 903 条含 15 组重复与 5 条三/五字熟语 ⇒ BAD。"
},
{
  "slug": "language/grammar-checker",
  "clicks": [
    "document.getElementById('input-text').value='   ';check();document.getElementById('grammar_checkerPresets').textContent='G_EMPTY:'+document.getElementById('s-issues').textContent+'|PROMPT:'+(document.getElementById('result').innerHTML.indexOf('请输入文本后再检查')>=0?1:0);"
  ],
  "expect": [
    "G_EMPTY:0|PROMPT:1"
  ],
  "ref": "EL-J14 回归：空白输入应 0 问题并提示「请输入文本后再检查」；旧实现虽然提前返回但结果区为空、无提示。"
},
{
  "slug": "language/grammar-checker",
  "clicks": [
    "document.getElementById('input-text').value='你好世界';check();document.getElementById('grammar_checkerPresets').textContent='G_NONE:'+document.getElementById('s-issues').textContent+'|OK:'+(document.getElementById('result').innerHTML.indexOf('未发现明显的语法问题')>=0?1:0);"
  ],
  "expect": [
    "G_NONE:0|OK:1"
  ],
  "ref": "EL-J14 回归：4 字无规则文本旧实现会被可选正则 `做?坐?` 的零长度匹配刷出 5 条问题（N+1）；新实现跳过空匹配 ⇒ 0 条。"
},
{
  "slug": "language/grammar-checker",
  "clicks": [
    "document.getElementById('input-text').value='他做车去上班';check();document.getElementById('grammar_checkerPresets').textContent='G_HIT:'+document.getElementById('s-issues').textContent+'|MARK:'+(document.getElementById('result').innerHTML.indexOf('做车')>=0?1:0);"
  ],
  "expect": [
    "G_HIT:1|MARK:1"
  ],
  "ref": "EL-J14 正向对照：把空匹配规则替换为具体 `/做(车|下|着|位)/` 后，「做车」应恰好命中 1 条并在结果中标记。"
},
{
  "slug": "chinese/chinese-character",
  "clicks": [
    "var bad=__ccValidate();document.getElementById('ccPreset').textContent='CC:'+bad+'|HAN='+charDB['汉'].strokes+'|GUO='+charDB['国'].radical+'|AI='+charDB['爱'].strokes+'|XI='+charDB['曦'].pinyin+'|XING='+charDB['行'].pinyin;"
  ],
  "expect": [
    "CC:|HAN=5|GUO=囗|AI=10|XI=xī|XING=xíng / háng"
  ],
  "ref": "EL-J15 回归：数据自检 0 问题；汉=5 画、国部首=囗、爱=10 画；并新增「曦」「行（多音）」，不再只有 20 字且笔画/部首错误。"
},
{
  "slug": "chinese/chinese-character",
  "clicks": [
    "document.getElementById('charInput').value='曦';lookup();document.getElementById('ccPreset').textContent='CC_XI:'+document.getElementById('displayPinyin').textContent+'|INFO:'+(document.getElementById('infoGrid').innerHTML.indexOf('20')>=0?1:0)+'|RAD:'+(document.getElementById('infoGrid').innerHTML.indexOf('日')>=0?1:0);"
  ],
  "expect": [
    "CC_XI:xī|INFO:1|RAD:1"
  ],
  "ref": "EL-J15 回归：深挖示例查询「曦」应命中并显示 xī、20 画、日部（旧 20 字库未收录）。"
},
{
  "slug": "chinese/chinese-character",
  "clicks": [
    "document.getElementById('charInput').value='鑫';lookup();document.getElementById('ccPreset').textContent='CC_MISS:'+document.getElementById('displayPinyin').textContent+'|HINT:'+(document.getElementById('infoGrid').innerHTML.indexOf('未收录')>=0?1:0);"
  ],
  "expect": [
    "CC_MISS:未收录|HINT:1"
  ],
  "ref": "EL-J15 回归：未收录字「鑫」应明确提示未收录，避免用户误以为数据错误；页面已标注收录范围（45 字，非完整字典）。"
},
{
  "slug": "edu2/schedule-conflict",
  "inputs": {
    "courseInput": "物理,王老师,D401,2,1,2\n化学,王老师,E502,2,1.5,2\n生物,赵老师,D401,2,1abc,2\n历史,孙老师,F603,4,1,2"
  },
  "clicks": ["detect();var h=String(document.getElementById('result').innerHTML).replace(/<[^>]+>/g,' ');var ok=h.indexOf('已拒绝 2 行')>=0&&h.indexOf('第2行星期/节次须为整数')>=0&&h.indexOf('第3行星期/节次须为整数')>=0&&h.indexOf('课程总数')>=0;document.getElementById('__tbProbe').textContent='STRICT '+(ok?'OK':'BAD '+h.slice(h.indexOf('已拒绝'),h.indexOf('已拒绝')+160));"],
  "expect": ["STRICT OK"],
  "ref": "第1091批 J10：旧版 parseInt 把 1.5/1abc 静默截成 1，四行全计入；严格整数解析后第2/3行被拒绝并在结果区列出行号与原因，仅两门合法课保留。哨兵同时锚拒绝计数与两条行号原因，旧版无拒绝串必然变红。"
},
{
  "slug": "edu2/schedule-conflict",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/edu2/schedule-conflict.html','utf8').replace(/\\s+/g,' ');var ok=h.indexOf('loadSample(); }catch(e2){}')<0&&h.indexOf('detect(); }catch(e2){}')>=0&&h.indexOf('a.start≤b.end 且 b.start≤a.end')>=0&&h.indexOf('a.start&lt;b.end 且 b.start&lt;a.end')<0&&h.indexOf('[start,end)')<0&&h.indexOf('[start,end]')>=0;document.getElementById('__tbProbe').textContent='SCHEDFIX '+(ok?'OK':'BAD');"],
  "expect": ["SCHEDFIX OK"],
  "ref": "第1091批 J10 源码形态：历史回调回填后必须调 detect()（旧版 loadSample() 会把 courseInput 重写为固定 SAMPLE，历史回放失效）；FAQ 与 constRef 区间口径统一为离散整节闭区间 [start,end]，旧半开表述与 [start,end) 必须消失。旧版四项全命中旧串，必然变红。"
},
{
  "slug": "edu2/study-progress",
  "inputs": {"dailyHours": "4"},
  "clicks": ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/study-progress.html','utf8');var d=JSON.stringify(JSON.parse(fs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8'))['edu2/study-progress']);var ok=h.indexOf('function addWorkdays')>=0&&h.indexOf('function workdaysUntil')>=0&&h.indexOf('addWorkdays(today, needDays)')>=0&&d.indexOf('跳过周六日')>=0&&document.getElementById('dailyHours').value==='4';document.getElementById('__tbProbe').textContent='SPWORK '+(ok?'OK':'BAD');"],
  "expect": ["SPWORK OK"],
  "ref": "EL-J132：旧版 estDate=today+needDays*86400000 按日历天推进，与说明「按工作日计」不符。现 addWorkdays 跳过周六日推进完成日、workdaysUntil 按工作日评估目标，权威源 FAQ 同步「跳过周六日」。源码+权威源哨兵，旧版必红。"
},
{
  "slug": "edu2/study-progress",
  "inputs": {"dailyHours": "3"},
  "clicks": ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/study-progress.html','utf8');var ok=h.indexOf('if(!isFinite(done) || !isFinite(total) || !isFinite(hours)')>=0&&h.indexOf('parseSubjects.invalid = invalid')>=0&&h.indexOf('isFinite(rawDaily) && rawDaily>0')>=0&&document.getElementById('dailyHours').value==='3';document.getElementById('__tbProbe').textContent='SPNAN '+(ok?'OK':'BAD');"],
  "expect": ["SPNAN OK"],
  "ref": "EL-J133：旧版 hours 直接 parseFloat、dailyHours 仅 ||4，NaN 传播后整表显示「—」且无原因。现 parseSubjects 校验 isFinite(hours)&&>0、跳过非法行并计数提示，dailyHours 用 isFinite&&>0 否则 4。源码哨兵，旧版必红。"
},
{
  "slug": "edu2/study-progress",
  "inputs": {"dailyHours": "5"},
  "clicks": ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/study-progress.html','utf8');var ok=h.indexOf('calendarDaysToTarget < 0')>=0&&h.indexOf('目标已逾期')>=0&&h.indexOf('已逾期 ')>=0&&document.getElementById('dailyHours').value==='5';document.getElementById('__tbProbe').textContent='SPOVER '+(ok?'OK':'BAD');"],
  "expect": ["SPOVER OK"],
  "ref": "EL-J134：旧版目标日期已过时 daysToTarget 钳成 0、落入中性 else「设置目标日期可评估」，完全不提逾期。现 calendarDaysToTarget<0 单独分支显示「目标已逾期 N 天」+相对目标卡标「目标已逾期」。源码哨兵避开 harness 无参兜底重复调 calc 的日期状态干扰，dailyHours 注入非默认值。"
},
{
  "slug": "edu2/study-progress",
  "inputs": {"dailyHours": "6"},
  "clicks": ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/study-progress.html','utf8');var ok=h.indexOf('subjects: document.getElementById(\\'subjectInput\\').value')>=0&&h.indexOf('targetDate: document.getElementById(\\'targetDate\\').value')>=0&&h.indexOf('dailyHours: document.getElementById(\\'dailyHours\\').value')>=0&&h.indexOf('__study_progressDetail = list.map')>=0&&h.indexOf('study-progress-detail.csv')>=0&&document.getElementById('dailyHours').value==='6';document.getElementById('__tbProbe').textContent='SPPERSIST '+(ok?'OK':'BAD');"],
  "expect": ["SPPERSIST OK"],
  "ref": "EL-J135：旧版 saveInput 仅存科目纯文本、targetDate/dailyHours 每次重置，导出绑历史快照表而非当前明细。现存 JSON 三字段（兼容旧纯文本 fillSaved）、导出用 __study_progressDetail 生成「科目/完成/总数/完成度/剩余工时」明细 CSV。源码哨兵，旧版必红。"
},
{
  "slug": "edu2/wrong-book",
  "clicks": ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/wrong-book.html','utf8');var ok=h.indexOf('function parseLocalDate(s)')>=0&&h.indexOf('return new Date(Number(m[1]), Number(m[2])-1, Number(m[3]));')>=0&&h.indexOf('new Date(it.reviewDate)')<0&&h.split('parseLocalDate(it.reviewDate)').length-1===3;document.getElementById('__tbProbe').textContent='WBLOCAL '+(ok?'OK':'BAD');"],
  "expect": ["WBLOCAL OK"],
  "ref": "EL 当日错题到期复核：reviewDate 保存的是本地日历日期字符串，旧版 new Date('YYYY-MM-DD') 按 UTC 解析，在 UTC- 时区会落到前一天，导致“今日复习”在统计卡里被当到期/逾期。现统一 parseLocalDate 按本地零点解析，三处引用一并替换；源码哨兵，旧版必红。"
},
{
  slug: "edu2/exam-countdown", inputs: {examDate:"2027-01-03"},
  clicks: ["var NativeDate=Date;Date=class extends NativeDate{constructor(...a){super(...(a.length?a:['2026-12-30T12:00:00']));}static now(){return new NativeDate('2026-12-30T12:00:00').getTime();}};document.getElementById('countHoliday').checked=true;calc();var h=document.getElementById('result').innerHTML;var cross=h.indexOf('未内置 2027 年')>=0&&h.indexOf('处理 2026 年')>=0;document.getElementById('examDate').value='2026-12-31';calc();var single=document.getElementById('result').innerHTML.indexOf('未内置')<0;Date=NativeDate;document.getElementById('__tbProbe').textContent='HOLYEARS:'+(cross&&single?'OK':'BAD');"],
  expect: ["HOLYEARS:OK"], ref: "跨年分别披露已覆盖与缺表年份，单年已覆盖不提示缺表。"
},
{
  "slug": "edu2/exam-countdown",
  "clicks": ["var fs=globalThis.__tbFs;var h=fs.readFileSync(process.cwd()+'/tools/edu2/exam-countdown.html','utf8');var ok=h.indexOf('var studyDays = workdays + (countWeekend ? weekends : 0);')>=0&&h.indexOf('周末计入可复习天数')>=0&&h.indexOf('可复习天数（含周末）')>=0&&h.indexOf('workdays--')<0;document.getElementById('__tbProbe').textContent='EXCWKND '+(ok?'OK':'BAD');"],
  "expect": ["EXCWKND OK"],
  "ref": "R 批承诺复核：旧版 countWeekend 只改卡片显示，可复习天数不随勾选变化；节假日在 weekday 分支 workdays-- 后又 workdays++，实际未扣减。现 studyDays 按勾选含/不含周末，标签与说明同步，节假日只计一次不再错扣；源码哨兵，旧版必红。"
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

  console.log("==== edu2 calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
