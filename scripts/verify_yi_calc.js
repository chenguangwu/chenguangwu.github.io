#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "yi/64-gua",
  "inputs": {},
  "clicks": [
    "selectedGua=GUA.find(function(g){return g.num===10;});renderDetail();"
  ],
  "expect": [
    "履虎尾,不咥人,亨"
  ],
  "ref": "clicks 直设顶层 selectedGua + 调 renderDetail()：默认态无选中 ⇒ renderDetail 早返回、不渲染详情；注入后渲染第10卦·履卦详情，卦辞「履虎尾,不咥人,亨」为详情独有锚点（默认列表仅显「第N卦 名卦」不含卦辞，已双态核验默认态无此串）。"
},
{
  "slug": "yi/bagua-viewer",
  "clicks": [
    "showGua('坤');"
  ],
  "expect": [
    "厚德载物，柔顺贞静，含弘光大。"
  ],
  "ref": "弱用例去默认化（BATCH118）：原锚「乾卦」（八卦名字串，默认列表本身含全部卦名 + 自然·五行 ⇒ 判别力0）。clicks 经 showGua('坤') 渲染坤卦详情，expect 锚坤卦专属「卦德」串「厚德载物，柔顺贞静，含弘光大。」；默认态只有八卦列表、无「卦象/卦德/象征」详情文本 ⇒ 零逃生项。"
},
{
  "slug": "yi/yi-yao",
  "inputs": {},
  "clicks": [
    "selectYao(5);"
  ],
  "expect": [
    "飞龙在天"
  ],
  "ref": "clicks 调 selectYao(5) 选第5爻 ⇒ renderYaoText 渲染卦1第5爻爻辞「飞龙在天」（默认只渲染初九「潜龙勿用」，已双态核验默认态无「飞龙在天」）。selectYao 内 querySelectorAll('.yao-item') 为 class 选择器、harness 支持；currentGua 由页面初始化置卦1，注入态产出正确。"
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
  console.log("==== yi calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
