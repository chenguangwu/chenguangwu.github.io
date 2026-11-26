#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "tunnel/advance-rate",
  "inputs": {
    "inL": "6",
    "inEta": "0.9",
    "inDrill": "3",
    "inBlast": "1",
    "inVent": "0.5",
    "inMuck": "3",
    "inSupport": "2",
    "inCycles": "3"
  },
  "expect": [
    "10.80"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tunnel/gas-monitor",
  "inputs": {
    "inGas": "3.5"
  },
  "expect": [
    "3.50%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tunnel/lining-thickness",
  "inputs": {
    "inB": "15"
  },
  "expect": [ "90 cm" ],
  "ref": "auto-restore"
},
{
  "slug": "tunnel/support-design",
  "inputs": {
    "inB": "18",
    "inH": "8"
  },
  "expect": [ "5.4 m" ],
  "ref": "auto-restore"
},
{
  "slug": "tunnel/ventilation-calc",
  "inputs": {
    "inA": "90",
    "inV": "2.5",
    "inL": "1000",
    "inN": "800",
    "inQco": "0.02",
    "inDelta": "100",
    "inAco": "60"
  },
  "expect": [
    "810000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "tunnel/support-design",
  "clicks": ["var zh=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/tunnel.json','utf8');var en=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/en/tunnel/support-design.json','utf8');var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/tunnel/support-design.html','utf8');var ok=zh.indexOf('1/3~1/4')<0&&zh.indexOf('支护展开长度')>=0&&en.indexOf('developed length')>=0&&h.indexOf('inShape')>=0;document.getElementById('__tbProbe').textContent='TUNNELMETA '+(ok?'OK':'BAD');"],
  "expect": ["TUNNELMETA OK"],
  "ref": "12-N9：页面公式框早已按代码改为 k_L=0.20~0.45、喷层按级别固定，但权威 intro 与由其生成的 meta/og/JSON-LD 仍写「跨度的 1/3~1/4」，英译词典还残留塌落拱旧口径死键。源码形态断言中英权威源与页面 meta 全部无旧串且新串到位；旧版必红，默认态不产生该哨兵，零逃生。"
},
{
  "slug": "tunnel/gas-monitor",
  "inputs": {
    "inGas": ""
  },
  "expect": [
    "0–100"
  ],
  "ref": "浓度为空时清空瓦斯判定（GASCLR）；旧实现 !isFinite 直接 return，上一档「0.50% / 注意」残留"
},
{
  "slug": "tunnel/lining-thickness",
  "inputs": {
    "inB": ""
  },
  "expect": [
    "请填写大于 0 的开挖跨度"
  ],
  "ref": "跨度为空时清空衬砌厚度（LINCLR）"
},
{
  "slug": "tunnel/support-design",
  "inputs": {
    "inB": ""
  },
  "expect": [
    "请填写大于 0 的开挖跨度与高度"
  ],
  "ref": "跨度为空时清空支护参数（SUPCLR）"
},
{
  "slug": "tunnel/gas-monitor",
  "inputs": {
    "inGas": "-1"
  },
  "expect": [
    "负值或超出量程"
  ],
  "ref": "负浓度必须拒绝并清空旧分级，旧实现会落入安全档"
},
{
  "slug": "tunnel/advance-rate",
  "clicks": ["var e=document.getElementById('inEta');e.value='1.2';calc();"],
  "expect": ["请检查输入"],
  "ref": "利用率>1 时必须清空旧进尺、旧统计与复制数据"
},
{
  "slug": "tunnel/advance-rate",
  "clicks": ["var e=document.getElementById('inDrill');e.value='25';calc();"],
  "expect": ["无法估算 1000 m 工期"],
  "ref": "单循环超过24h、日进尺为0时不得给出1000m工期"
},
{
  "slug": "tunnel/support-design",
  "clicks": ["var s=document.getElementById('inShape');s.value='arch';calc();"],
  "expect": ["22.85 m","半圆拱+直墙","16 根"],
  "ref": "拱形断面展开长度 2×(H−B/2)+πB/2，12×8 取 22.85 m，根数随长度变化"
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

  console.log("==== tunnel calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
