#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "safety/accident-stats",
  "inputs": {
    "hours": "750000",
    "fatal": "0",
    "severe": "1",
    "minor": "4",
    "lti": "3",
    "lostDays": "45"
  },
  "expect": [
    "750000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/analysis-3",
  "inputs": {
    "data": "203.0.113.7 ssh_fail\n203.0.113.7 ssh_fail\n203.0.113.7 ssh_fail\n203.0.113.7 ssh_fail\n192.168.1.5 login_fail",
    "thr": "3"
  },
  "expect": [
    "203.0.113.7 / ssh_fail：4 次"
  ],
  "ref": "同一 IP+事件 ≥3 次判定：203.0.113.7/ssh_fail 计 4 次 → 进可疑列表（独立计数）"
},
{
  "slug": "safety/assessor-drill",
  "inputs": {
    "people": "180",
    "floors": "6",
    "tStart": "09:00:00",
    "tEnd": "09:04:30"
  },
  "expect": [
    "40.0"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/detector-strength",
  "inputs": { "pw": "Zx9#kQ2!vLp7" },
  "clicks": ["analyze()"],
  "expect": [
    "88 / 100",
    "78.8",
    "12 密码长度"
  ],
  "ref": "非默认密码 Zx9#kQ2!vLp7（默认 pw 为空，兜底阶段 genPassword() 会生成 16 位 → 98/100、105.1 熵、16 长度）。字符集 = 26+26+10+33 = 95，熵 = 12×log2(95) = 78.84 → 78.8；长度 12、评分 88。默认态无此三串；「4/4 字符种类」在两态都出现（16 位生成密码同样含四类）⇒ 不可锚。"
},
{
  "slug": "safety/generator-21",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/generator-hazard",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/hazard-checklist",
  "inputs": {
    "scenario": "建筑"
  },
  "expect": [
    "建筑"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/ppe-replacement",
  "inputs": {
    "name": "安全帽",
    "cycle": "1095",
    "type": "呼吸器"
  },
  "expect": [
    "呼吸器"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/random-13",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/reminder-cycle-protection",
  "inputs": {
    "ppeCycle": "548"
  },
  "expect": [
    "548"
  ],
  "ref": "auto-restore"
},
{
  "slug": "safety/safety-quiz",
  "inputs": {},
  "clicks": [
    "shuffle=function(a){return a;};startQuiz();for(var i=0;i<qOrder.length;i++){choose(qOrder[i].a);nextQ();}"
  ],
  "expect": [
    "安全知识掌握优秀！"
  ],
  "ref": "startQuiz() 用 shuffle(QUESTIONS).slice(0,15) 随机抽题 ⇒ 顶层 shuffle 直接覆写成恒等（页面函数、非进程级全局），qOrder 即 QUESTIONS 前 15 题；再逐题 choose(qOrder[i].a) 全答对、nextQ() 推进（renderQ() 会重置 answered 门控）。 finishQuiz() 落 pct=100 分支 ⇒ 「安全知识掌握优秀！」。默认态 / 兜底阶段无参调 finishQuiz 时 score=0、wrongList 空 ⇒ 落「正确率较低…」+「无错题，全部答对！」两条（后者是 else 兜底分支，同 BATCH97，刻意不锚）。旧锚「15」是题数常量，默认态必命中，判别力 0，已弃。"
},
  // 注：safety/stats-report-frequency 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== safety calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
