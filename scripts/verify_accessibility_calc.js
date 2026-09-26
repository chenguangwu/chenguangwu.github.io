#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "accessibility/braille-translator",
  "inputs": {
    "srcInput": "ab",
    "caseSel": "upper"
  },
  "expect": [
    "⠁⠃",
    "原文： AB 字母 2 个 · 数字 0 个 · 盲文符号 2 格"
  ],
  "ref": "盲文翻译：注入 ab + caseSel=upper ⇒ 结果区渲染盲文点字符 ⠁⠃（A=点1、B=点1+2），统计串为「原文： AB 字母 2 个 · 数字 0 个 · 盲文符号 2 格」。默认态是 hello 2026 ⇒ ⠓⠑⠇⠇⠕ ⠼⠃⠚⠃⠋ / 字母 5 个 · 数字 4 个 · 盲文符号 11 格，双态强判别。旧锚 expect [\"upper\"] 是输入值回显、零判别力，已替换。"
},
{
  "slug": "accessibility/sign-language",
  "inputs": {
    "searchInput": "zzzqx"
  },
  "expect": [
    "未找到匹配词汇"
  ],
  "ref": "关键词过滤型：inputs 写 searchInput=zzzqx ⇒ oninput=render() 过滤 43 条词汇得空集 ⇒ 「未找到匹配词汇」。默认态渲染全量 43 条、blob 无该串（已双态核验），故为排他锚点。"
},
{
  "slug": "accessibility/voice-synthesis",
  "inputs": {
    "rate": "1",
    "pitch": "1",
    "vol": "1",
    "text": "abcde",
    "langFilter": "zh"
  },
  "expect": [
    "5 字"
  ],
  "ref": "语音合成：harness 无 speechSynthesis ⇒ supported=false ⇒ loadVoices() 首行即 return，音色列表永远为空、无从锚定；唯一不依赖该分支的派生量是 updateCharCount() 写入的 #charCount（注入 abcde ⇒ 5 字，默认 23 字）。旧锚 expect [\"zh\"] 是 langFilter 输入值回显、零判别力，已替换。"
}
];
async function main() {
  const only = process.argv.slice(2);
  const cases = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cases) {
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== accessibility calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
