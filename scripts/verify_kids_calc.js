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
  "expect": [ "12 个记忆格子" ],
  "ref": "auto-restore"
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
