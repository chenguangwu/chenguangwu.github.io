#!/usr/bin node
"use strict";
const fs = require("fs");
const { runCase } = require("./verify_it_calc.js");
globalThis.__tbFs = fs;
const CASES = [
{
  "slug": "accessibility/braille-translator",
  "inputs": {"srcInput": ""},
  "clicks": ["doTranslate()"],
  "expect": ["请输入文本后再转译。"],
  "ref": "空输入守卫：清空 srcInput 后点转译，必须给输入提示，不得输出「原文：（空）字母 0 个 · 数字 0 个 · 盲文符号 0 格」的伪统计；默认 hello 2026 不含该提示。"
},
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
  "slug": "accessibility/braille-translator",
  "inputs": {
    "srcInput": "12"
  },
  "expect": [
    "⠼⠁⠃",
    "原文： 12 字母 0 个 · 数字 2 个 · 盲文符号 3 格"
  ],
  "ref": "数字点位回归：1→a=⠁、2→b=⠃（不是 c 的 ⠉），数字前加数字符 ⠼ ⇒ ⠼⠁⠃、3 格。深度解析原写「2→⠉」与代码/FAQ 矛盾，已改「2→⠃」。"
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
},
{
  "slug": "accessibility/ramp-slope",
  "clicks": ["document.getElementById('sceneSel').value='general';document.getElementById('height').value='200';document.getElementById('ratio').value='50';calc();var h=String(document.getElementById('tipBox').innerHTML);var ok=h.indexOf('建议设 1 处休息平台')>=0&&h.indexOf('单段最大高差为 120cm')>=0;document.getElementById('__tbProbe').textContent='RAMP50 '+(ok?'OK':'BAD '+h);"],
  "expect": ["RAMP50 OK"],
  "ref": "第1092批 J2：H=200cm、1:50 → 单段最大高差 120cm 超限，水平 100m；每段水平上限=120×50÷100=60m，平台数=ceil(100/60)−1=1。旧版平台数仅在 X∈[10,20) 计算，X=50 恒为 0 ⇒ 无平台建议，哨兵变红。clicks 里先定场景再覆写 ratio，避免 onScene 联动覆盖。"
},
{
  "slug": "accessibility/ramp-slope",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/accessibility/ramp-slope.html','utf8');var ok=h.indexOf('var allowedRun = specMaxH > 0 ? (specMaxH * X / 100) : 0;')>=0&&h.indexOf('msg = needPlatform')>=0&&h.indexOf('每段坡道水平长度超过 9m 或高差超过 0.75m')<0&&h.indexOf('1:20 为 24m')>=0;document.getElementById('__tbProbe').textContent='RAMPFIX '+(ok?'OK':'BAD');"],
  "expect": ["RAMPFIX OK"],
  "ref": "第1092批 J2 源码形态：needPlatform 必须进入提示分支（旧版算后从未使用）；平台上限按坡度×单段高差统一（1:20=24m），旧「超过9m一律设平台」与按 X 分段的两套口径均须消失。"
},
{
  "slug": "accessibility/sign-language",
  "inputs": {"searchInput":"mom"},
  "expect": ["Mother","Little finger out","Terms of address"],
  "ref": "第830批：英文检索需匹配英文词/别名并渲染英文卡片。mom 命中「妈妈」的 enAlias；卡片输出 Mother、英文动作说明与 Terms of address。中文态默认 43 条不含该组串，零逃生。"
},
{
  "slug": "accessibility/accessible-restroom",
  "clicks": ["updateScope();document.getElementById('__tbProbe').textContent='SCOPE830 '+((document.getElementById('scopeNotice').textContent.indexOf('GB 55019-2021 现行版本')>=0&&document.getElementById('scopeNotice').textContent.indexOf('旧版对照')>=0)?'OK':'BAD');"],
  "expect": ["SCOPE830 OK"],
  "ref": "第830批：按所在地/项目类型给出适用规范提示；中国大陆默认提示查阅 GB 55019-2021 现行版本并将 GB 50763-2012 标为旧版对照。旧版无 updateScope 与 scopeNotice，探针必红。"
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

  console.log("==== accessibility calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
