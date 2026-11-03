#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
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
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
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
