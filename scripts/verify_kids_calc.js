#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "kids/focus-timer",
  "inputs": {
    "focusMin": "25",
    "restMin": "8",
    "goalCount": "6"
  },
  "clicks": ["renderStats()"],
  "expect": [
    "6 今日目标"
  ],
  "ref": "目标数直接由 goalCount 渲染 ⇒ 注入 6 得「6 今日目标」（默认 4）。"
     + "原 expect「今日完成度」是统计卡标题（静态文本，回退默认仍命中 ⇒ 逃生项）。"
     + "注：今日番茄 / 累计番茄取自 localStorage（harness 恒空 ⇒ 恒 0），不可断言。",
  },
{
  "slug": "kids/memory-palace",
  "inputs": {
    "srcInput": "圆周率 3.1415926",
    "cellCount": "12"
  },
  "expect": [ "已编码 4 条内容", "12 个格子", "末页保留 8 个空位" ],
  "ref": "数字分位把 8 位数字拆成 4 段；12 格刚好一页、末页保留 8 个空位。修复前按格子数循环复制片段（31/41/59/26 重复填充），且超量内容被静默丢弃。"
},
{
  "slug": "kids/mirror-letter",
  "inputs": {
    "typeSel": "number"
  },
  "expect": [
    "number"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "kids/mirror-letter",
  "clicks": [
    "var bad='AHIMOTUVWXY018',ok1=true,ok2=true,ok3=true;document.getElementById('typeSel').value='letter';document.getElementById('diffSel').value='easy';for(var i=0;i<200;i++){if(bad.indexOf(genTarget())>=0){ok1=false;break;}}document.getElementById('typeSel').value='number';for(var j=0;j<200;j++){if(bad.indexOf(genTarget())>=0){ok2=false;break;}}document.getElementById('diffSel').value='hard';document.getElementById('typeSel').value='mixed';for(var k=0;k<200;k++){var t=genTarget();for(var m=0;m<t.length;m++){if(bad.indexOf(t[m])>=0)ok3=false;}}round.right=3;round.total=4;resetGame();var ok4=round.right===0&&round.total===0;document.getElementById('__tbProbe').textContent='MLPOOL '+ok1+' '+ok2+' '+ok3+' '+ok4;"
  ],
  "expect": ["MLPOOL true true true true"],
  "ref": "修复前字母/数字池含 A/H/I/M/O/T/U/V/W/X/Y 与 0/1/8 等左右翻转眼几乎不变的字形，镜像标记只能靠猜；现剔除这些字形（含困难双字模式逐字校验），并把本轮对错计数 round.right/total 在重新开始时归零（完成提示改用本轮而非累计）。默认 letter 池不含该探针串。"
},
{
  "slug": "kids/multiplication-practice",
  "clicks": ["stats.right=17;stats.total=20;stats.bestStreak=6;renderStats();"],
  "expect": [
    "85% 正确率"
  ],
  "ref": "独立复算：正确率 = round(stats.right / stats.total * 100) = round(17/20*100) = 85，renderStats() 把「85%」与卡片标签「正确率」一起写进 #statGrid；默认 stats 全 0 ⇒ 显示「0% 正确率」。stats 是页面顶层 var，可在页面作用域直接改字段后重渲染。"
},
{
  "slug": "kids/multiplication-practice",
  "clicks": [
    "var ok=/if\\(game\\.done\\) return;/.test(String(checkAnswer))&&/game\\.done = true;/.test(String(handleRight))&&/game\\.done = true;/.test(String(handleWrong))&&/skip && !game\\.done/.test(String(nextQuestion))&&/clearTimeout\\(game\\.nextId\\)/.test(String(nextQuestion))&&/game\\.nextId=setTimeout/.test(String(handleRight));document.getElementById('__tbProbe').textContent='MPSRC '+ok;"
  ],
  "expect": ["MPSRC true"],
  "ref": "修复前已答题仍可被「换一题」重复计次、旧切题定时器不取消；现 checkAnswer 以 game.done 早退，handleRight/handleWrong 置 done，nextQuestion 仅对未答题计次并先清 game.nextId，切题延时统一写入 game.nextId。计时器与页面状态在 DOM 桩内不同步，故用源码形态判定。默认态无该探针串。"
},
{
  "slug": "kids/memory-palace",
  "inputs": {
    "srcInput": "1234567890123456789012345678901234567890",
    "cellCount": "9"
  },
  "expect": [ "已编码 20 条内容", "3 页", "末页保留 7 个空位" ],
  "ref": "数字分位每 2 位一段共 20 条；9 格分页 ⇒ 3 页 27 格，末页 7 个空位，全部内容保留、不再循环重复。"
},
{
  "slug": "kids/multiplication-practice",
  "clicks": [
    "resetGame();var a0=game.a,b0=game.b;nextQuestion(true);var ch1=(game.a!==a0||game.b!==b0);nextQuestion(true);var ch2=(game.a!==a0||game.b!==b0);document.getElementById('__tbProbe').textContent='MPADV '+ch1+' '+ch2+' pos'+game.pos;"
  ],
  "expect": ["MPADV true true pos3"],
  "ref": "阶梯模式按未掌握乘数推进：初始 2×1，跳过 1 后到 2×2、再跳到 2×3，此时待答位置 pos=3；修复前用 idx%9 且跳过不增 idx，下一题仍是原题。"
},
{
  "slug": "kids/stroke-order",
  "inputs": {
    "charInput": "我"
  },
  "clicks": [
    "loadChar('我')"
  ],
  "expect": [
    "1 撇 2 横 3 竖钩 4 提 5 斜钩 6 撇 7 点"
  ],
  "ref": "charInput=我（7 画）⇒ loadChar('我') 后 render() 把 #totalNo 置 7 并重建 #strokeChips 为「1 撇 2 横 3 竖钩 4 提 5 斜钩 6 撇 7 点」。⚠ 原注入 charInput=永/speedSel=900 恰为页面默认（input value=永、select selected 900），原 expect「900」只是 select 值回显 ⇒ 默认态同样命中（真逃生）；且该页 oninput 在桩内不触发，必须用 clicks 调 loadChar。默认态（永=5 画）为「1 点 2 横折钩 3 横撇 4 撇 5 捺」，与新锚零交集。"
},
{
  "slug": "kids/stroke-order",
  "clicks": ["loadChar('好')"],
  "expect": ["1 撇点 2 撇 3 横 4 横撇 5 竖钩 6 横"],
  "ref": "好=女(撇点/撇/横)+子(横撇/竖钩/横)；任务报告称后半仍标撇点/撇/横，实际数据已正确，补此用例锁定回归，防后续被改回。默认字永的 5 画与锚点零交集。"
},
{
  "slug": "kids/memory-palace",
  "clicks": ["document.getElementById('srcInput').value='';generate();"],
  "expect": ["请先输入要记忆的内容"],
  "ref": "空输入不再回退 3.1415926 示例；generate 直接清空并提示，不生成宫殿/摘要。默认输入圆周率非空，不命中该提示。"
},
{
  "slug": "kids/memory-palace",
  "inputs": {"srcInput": "床前明月光疑是地上霜", "cellCount": "25"},
  "clicks": ["document.getElementById('modeSel').value='shape';generate();"],
  "expect": ["只编码数字"],
  "ref": "谐音象形模式只取数字，纯中文诗句没有数字时明确提示切换到逐字编码，不再静默塞入 3/1/4 示例。"
},
{
  "slug": "kids/focus-timer",
  "clicks": ["document.getElementById('focusMin').value='0';var r=applyCustom(true);document.getElementById('__tbProbe').textContent='FOCUS '+r+' '+state.focusSec;"],
  "expect": ["FOCUS false 900"],
  "ref": "专注 0 分钟越界（合法 5–45 整数），applyCustom 返回 false 且不改 state.focusSec（默认 15 分钟=900 秒），不再用 ||15 静默回退。"
},
{
  "slug": "kids/mirror-letter",
  "clicks": ["resetGame();var i0=round.idx;round.skipped++;nextRound(true);document.getElementById('__tbProbe').textContent='MIRSKIP '+i0+' '+round.idx+' '+round.skipped+' answered'+round.answered;"],
  "expect": ["MIRSKIP 1 1 1 answeredfalse"],
  "ref": "跳过（nextRound(true)）不推进 idx、不计入 total，仅累加 skipped；第 1 题连续跳过仍停在第 1 题，不会因 idx>=limit 提前结束。默认 idx=1/skipped=0。"
},
{
  "slug": "kids/multiplication-practice",
  "clicks": ["resetGame();game.answer=6;game.done=false;var t0=stats.total;var inp=document.getElementById('answer');inp.value='6.9';checkAnswer();document.getElementById('__tbProbe').textContent='MPDEC '+(stats.total===t0)+' '+game.done;"],
  "expect": ["MPDEC true false"],
  "ref": "6.9 不再被 parseInt 截成 6 判对：非整数输入给提示且不增加 stats.total、不置 game.done；合法整数仍走 Number(val)===game.answer。"
},
{
  "slug": "kids/focus-timer",
  "clicks": ["state.focusSec=300;state.restSec=60;state.phase='focus';state.paused=false;state.endAt=Date.now()-7*60*1000;stats.today=todayStr();stats.done=0;stats.total=0;tick();document.getElementById('__tbProbe').textContent='FOCUSCATCH '+state.phase+' '+stats.done+' '+stats.total+' '+state.remaining;"],
  "expect": ["FOCUSCATCH focus 2 2 300"],
  "ref": "后台 12 分钟（专注5+休息1×2）后恢复：按截止时间连续结算 2 个专注阶段，进入第 3 个完整专注（300 秒），不再只补 1 个阶段并从休息重新开始。默认 15/5 分钟与探针不同源。"
},
{
  "slug": "kids/memory-palace",
  "clicks": ["generate();startRecall();var cells=document.querySelectorAll('#palace .cell');var hidden=cells[0].classList.contains('hide');revealCell(0,true);changePage(1);changePage(-1);cells=document.querySelectorAll('#palace .cell');var kept=cells[0].classList.contains('reveal');window.__memBody=document.body||document.documentElement;document.getElementById('__tbProbe').textContent='MEMRECALL '+(window.__memBody&&window.__memBody.classList&&window.__memBody.classList.contains('recall-mode'))+' '+hidden+' '+kept;"],
  "expect": ["MEMRECALL true true true"],
  "ref": "回忆模式隐藏待记忆输入与编码对照表；首格初始隐藏，揭示后翻页再返回仍保持 reveal。修复前只隐藏格子，输入框与编码表仍直接暴露答案，翻页后揭示状态丢失。"
},
{
  "slug": "kids/memory-palace",
  "clicks": ["generate();var src=String(exportPalaceCsv);var ok=src.indexOf('memory-palace.csv')>=0&&src.indexOf('页码,位置,内容,联想,状态')>=0&&src.indexOf('Math.floor(i / perPage) + 1')>=0&&src.indexOf('c.empty ?')>=0;document.getElementById('__tbProbe').textContent='MEMCSV '+ok;"],
  "expect": ["MEMCSV true"],
  "ref": "导出改为从 palace 逐格生成页码/位置/内容/联想/状态 CSV，另保留历史摘要导出；修复前“导出明细”调用通用历史表，只有输入与 80 字摘要。"
},
{
  "slug": "kids/stroke-order",
  "clicks": ["loadChar('我');curStep=getStrokes().length;render();"],
  "expect": ["点（最后一笔）✓ 完成"],
  "ref": "7 画「我」前进到最后一笔时，当前笔画名仍显示「点」并附完成状态；修复前 curStep>=total 直接显示「完成 ✓」，最后一笔名称被覆盖。默认「永」末笔为捺，与锚点不同源。"
},
{
  "slug": "kids/mirror-letter",
  "clicks": ["showGuide();"],
  "expect": ["不是左右镜像", "旋转约 180°", "竖直中线"],
  "ref": "6/9 说明改为“旋转约 180°近似对应，不是左右镜像”，并明确本练习沿竖直中线翻转；修复前写成“上下颠倒互为镜像”，与左右翻转练习冲突。默认指南盒隐藏，不命中。"
},
{
  "slug": "kids/multiplication-practice",
  "clicks": ["resetGame();game.done=false;game.timeLimit=5;game.deadline=Date.now()-100;game.answer=6;var t0=stats.total;var inp=document.getElementById('answer');inp.value='6';checkAnswer();if(game.nextId){clearTimeout(game.nextId);game.nextId=null;}document.getElementById('__tbProbe').textContent='MPLATE '+(stats.total===t0+1)+' '+(String(document.getElementById('hint').innerHTML).indexOf('时间到')>=0)+' '+(String(checkAnswer).indexOf('Date.now() >= game.deadline')>=0);"],
  "expect": ["MPLATE true true true"],
  "ref": "提交答案时先校验截止时间：已超时即使答案正确也按“时间到”判错并计次，后台节流不再额外给答题时间。默认 8 秒未超时，且答案 6 与默认题 2×3 相同，但 stats.total 默认 0、探针要求 +1，默认态不命中。"
},
{
  "slug": "kids/multiplication-practice",
  "clicks": ["resetGame();game.mode='asc';game.level=2;game.mastered={1:true,2:true,3:true,4:true,5:true,6:true,7:true,8:true};game.idx=8;game.pos=9;game.b=9;game.a=2;game.answer=18;stats.total=0;stats.right=0;handleRight();var lv=game.level;var idx=game.idx;resetGame();game.mastered={1:true,2:true,3:true,4:true,5:true,6:true,7:true,8:true};game.idx=8;game.pos=9;game.b=9;nextQuestion(true);document.getElementById('__tbProbe').textContent='MPMASTER '+lv+' '+idx+' '+game.level+' '+game.idx;"],
  "expect": ["MPMASTER 3 0 2 8"],
  "ref": "阶梯模式第 9 个未掌握乘数答对才升到第 3 关；若只是跳过第 9 题，掌握数仍 8、停在 2 关。修复前按 idx%9 升关，跳过/超时也推进 pos，未答全九题即可通关。"
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

  console.log("==== kids calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
