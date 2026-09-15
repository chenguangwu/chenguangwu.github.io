#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "accessibility/braille-translator",
  "inputs": {
    "srcInput": "hello 2026",
    "caseSel": "upper"
  },
  "expect": [
    "upper"
  ],
  "ref": "auto-restore"
},
{
  "slug": "accessibility/sign-language",
  "inputs": {},
  "expect": [
    "43"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "accessibility/voice-synthesis",
  "inputs": {
    "rate": "1",
    "pitch": "1",
    "vol": "1",
    "text": "欢迎使用语音合成工具，在这里输入文字即可朗读。",
    "langFilter": "zh"
  },
  "expect": [
    "zh"
  ],
  "ref": "auto-restore"
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
