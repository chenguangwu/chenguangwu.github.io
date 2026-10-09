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
},
{
  "slug": "accessibility/ramp-slope",
  "inputs": { "height": "90", "ratio": "10", "sceneSel": "resident" },
  "expect": ["10.80 水平长度(m)", "该坡度下单段最大高差为 75cm"],
  "ref": "注入 height=90（默认 40）+ sceneSel=resident（默认 general）。⚠ ratio 的注入被页面的场景联动覆盖回 1:12（选场景会写回标准坡度比），这是真机 onchange 行为 ⇒ 水平长度按 1:12 算：L = 90×12 = 1080 cm = 10.80 m；斜长 = √(1080²+90²) = 10.84 m；坡度 8.33%（4.76°）。居住区场景单段限高 75 cm ⇒ 90 cm 超限，输出「需设休息平台分段」提示。默认态（40 cm / general）为 4.80 m 且达标无提示，两串均不出现。⚠ 该页原「初始化失败」：页面用 document.createElementNS 建 SVG 示意图，harness 未建模该 API ⇒ 整页不可验证；已补 createElementNS 桩（返回与 createElement 同构节点）。"
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
