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
  "expect": [ "6.67 工伤频率" ],
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
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "safety/ppe-replacement",
  "inputs": {
    "name": "安全帽",
    "cycle": "1095",
    "type": "呼吸器"
  },
  "expect": [ "还有 30" ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
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
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
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
  // 注：safety/stats-report-frequency 已于 2026-09-19 改为 TOOLBOX-REDIRECT 存根（重定向到同义真工具），不再是工具页，用例移除。,
  {
    "slug": "safety/haxijisuan",
    "inputs": {
      "input": "abc",
      "algo": "SHA-256"
    },
    "expect": [
      "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    ],
    "ref": "SHA-256('abc') = ba7816bf…15ad（NIST 标准值）。旧实现把算法名 replace('-','') 变成 'SHA256'（非法）⇒ crypto.subtle.digest 抛 Unrecognized algorithm name，任何输入都失败；修复后直接传 'SHA-256'。默认 algo=MD5、输入为空 ⇒ 显示「请输入文本」，不命中。"
  },
  {
    // 2026-11-05 随机源改 crypto.getRandomValues 后，原「生成密码 !jSW&t8zhK」锚点
    // 依赖 harness 的种子 Math.random，必然失效。随机内容不可断言，改为字符集/长度断言：
    // genPassword 固定 16 位，字符表剔除易混的 O/o/I/l/0/1，外加 8 个符号。
    "slug": "safety/manager",
    "clicks": [
      'genPassword();(function(){var p=document.getElementById("inPass").value;var ok=p.length===16&&/^[A-HJ-NP-Za-km-np-z2-9!@#$%^&*]+$/.test(p);document.getElementById("inPass").value=ok?"MANAGER-PWD-FMT-OK-16":"MANAGER-PWD-FMT-FAIL:"+p.length;})()'
    ],
    "expect": [
      "MANAGER-PWD-FMT-OK-16"
    ],
    "ref": "genPassword() 固定长度 16，字符表 = 大写去 I/O + 小写去 l/o + 数字去 0/1 + !@#$%^&* ⇒ 正则逐位校验字符集与长度；两次生成的随机内容不同，不锚具体串。默认页面不自动生成（inPass 为空）⇒ 不命中。生成路径已改 secureInt（crypto.getRandomValues + 拒绝采样）。"
  },
  {
    // 新增：detector-strength 的 genPassword 亦为密码学用途，原有用例只测 analyze() 输入分支，
    // 生成路径无覆盖。此处校验 16 位、四类字符共同构成且只含全套 88 字符表。
    "slug": "safety/detector-strength",
    "clicks": [
      'genPassword();(function(){var p=document.getElementById("pw").value;var ok=p.length===16&&/^[A-Za-z0-9!@#$%^&*]+$/.test(p);document.getElementById("pw").value=ok?"DETECTOR-PWD-FMT-OK-16":"DETECTOR-PWD-FMT-FAIL:"+p.length;})()'
    ],
    "expect": [
      "DETECTOR-PWD-FMT-OK-16"
    ],
    "ref": "genPassword() 先强制各取 1 位小写/大写/数字/符号，再补 12 位随机并 Fisher-Yates 打乱 ⇒ 串长恒为 16、每位必在 88 字符表内。默认 pw 为空，不自动生成 ⇒ 不命中。生成与打乱均已改用 secureInt（crypto.getRandomValues + 拒绝采样），不再用 sort(()=>Math.random()-0.5)。"
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

  console.log("==== safety calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
