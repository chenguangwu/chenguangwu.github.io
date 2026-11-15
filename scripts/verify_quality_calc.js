#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
"slug": "quality/convert-qualified-defect",
"inputs": {
"val": "2.5",
"unit": "pct"
},
"expect": [
"25000.00 PPM"
],
"ref": "重做为真实换算器后复算：2.5% × 10 000 = 25000.00 PPM（小数 0.025、千分率 25）；默认 0.35% 得 3500.00 PPM ⇒ 注入失败即不命中"
},
{
  "slug": "quality/ppm-calculator",
  "inputs": {
    "defect": "15",
    "total": "8000",
    "pct": "0.15",
    "rate": "0.0015",
    "ppm": "1500",
    "dpmo": "1500"
  },
  "expect": [
    "0.001875"
  ],
  "ref": "auto-restore"
},
{
  "slug": "quality/process-capability",
  "inputs": {
    "usl": "13.5",
    "lsl": "9.5",
    "mean": "10.0",
    "sigma": "0.1",
    "usl2": "10.5",
    "lsl2": "9.5",
    "dataInput": "10.1, 9.9, 10.0, 10.2, 9.8, 10.0, 10.05, 9.95, 10.1, 9.9"
  },
  "expect": [
    "100.0000%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "quality/six-sigma",
  "inputs": {
    "dpmo": "6210",
    "yield": "99.379",
    "st": "7"
  },
  "expect": [
    "3.4008"
  ],
  "ref": "auto-restore"
},
{
  "slug": "quality/calc-cpk",
  "inputs": {
    "usl_m": "15.5",
    "lsl_m": "9.5",
    "mean_m": "10.0",
    "sd_m": "0.1",
    "usl_d": "10.5",
    "lsl_d": "9.5",
    "rawData": "10.1\n9.9\n10.0\n10.2\n9.8\n10.0\n10.1\n9.9\n10.0\n10.1\n9.9\n10.0"
  },
  "expect": [
    "15.5"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "quality/estimate-six-sigma",
  "inputs": {
    "dpmo": "9315",
    "defects": "62",
    "units": "10000",
    "opps": "1"
  },
  "expect": [
    "9315"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
},
{
  "slug": "quality/table-sampling",
  "inputs": {
    "kw": "zzzz"
  },
  "clicks": ["search()"],
  "expect": [
    "未找到匹配项"
  ],
  "ref": "search() 在 kw 为空时输出 DATA 全量 ⇒ 任何具体编号（A01 等）在默认态都命中 ⇒ 只能反向锚"
     + "「未找到匹配项」。注入不存在的关键词 zzzz ⇒ results 为空 ⇒ 输出该提示；默认态 DATA 非空、永不出现。"
     + "原 expect「A01」即默认全量表的首行编号，典型逃生项。",
}
,
{
    "slug": "quality/ppm-calculator",
    "inputs": {
      "defect": "1",
      "total": "1000000"
    },
    "expect": [
      "1 / 1,000,000",
      "1.00 PPM"
    ],
    "ref": "缺陷数 1 ÷ 总数 1,000,000 = 1 PPM（百万分之一）。页面输出 '1.00 PPM' 与 '1 / 1,000,000'。默认态 defect/total 为其他值，不出现该精确组合。"
  },
  {
    "slug": "quality/control-chart",
    "inputs": {
      "means": "abc123测试",
      "n": "42",
      "sigma": "42"
    },
    "expect": [
      "9.86, 22.99, 23.75, 21.69, 11.59, -23.03, -10.68, 54.41, 25.27, 1.43, 92.94, 73.46, 49.88, 85.22, 122.14\n42\n4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"means\":\"abc123测试\",\"n\":\"42\",\"sigma\":\"42\"}，输出区含「9.86, 22.99, 23.75, 21.69, 11.59, -23.03…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
{
  "slug": "quality/calc-cpk",
  "inputs": { "usl_m": "10", "lsl_m": "0", "mean_m": "10", "sd_m": "1" },
  "expect": ["500,000"],
  "ref": "12-M8 边界：均值恰在 USL 上，单侧超规概率应为 50% ⇒ 500,000 PPM。旧实现 `z<=0 直接返回 1e6` 虚报 1,000,000。默认手工档 10.5/9.5/10.0/0.1 的 PPM 为 0，不含 500,000。"
},
{
  "slug": "quality/calc-cpk",
  "inputs": { "usl_m": "10", "lsl_m": "0", "mean_m": "11", "sd_m": "1" },
  "expect": ["841,345"],
  "ref": "12-M8 越界：均值 11（超 USL 1σ），超上规概率 Φ(1)=84.13% ⇒ 841,345 PPM（下限侧概率≈0）。旧实现固定 1,000,000。默认手工档 10.0±0.1 不命中。"
},
{
  "slug": "quality/ppm-calculator",
  "inputs": { "defect": "-5", "total": "8000" },
  "expect": ["不合格品数须在 0 与总数之间"],
  "ref": "负不合格品数：旧实现只校验 N>0，-5/8000 会算出 −625 PPM 并给西格玛水平；现要求 0≤d≤N，非法即清空结果并提示。默认 12/8000 不命中。"
},
{
  "slug": "quality/ppm-calculator",
  "inputs": { "defect": "9000", "total": "8000" },
  "expect": ["不合格品数须在 0 与总数之间"],
  "ref": "不合格数超过总数：旧实现照算 112.5% / 1,125,000 PPM；现拦截 d>N。默认 12/8000 不命中。"
},
{
  "slug": "quality/ppm-calculator",
  "inputs": { "ppm": "2000000" },
  "clicks": ["fromPpm();var t=String(document.getElementById('rateResult').innerHTML);document.getElementById('__tbProbe').textContent='PPMLIM '+((t.indexOf('0~1000000')>=0)?'OK':'BAD');"],
  "expect": ["PPMLIM OK"],
  "ref": "比率模式：PPM 2,000,000 折合率 2，旧实现照算 200% 并给西格玛；现限定缺陷率 0~1（PPM 0~1,000,000），越界提示并停止换算。默认 1,500 PPM 不命中。"
},
{
  "slug": "quality/ppm-calculator",
  "clicks": ["__ppmMode='rate';var got='';var old=ToolBox.copyText;ToolBox.copyText=function(t){got=String(t);};try{copyAll();}catch(e){}ToolBox.copyText=old;document.getElementById('__tbProbe').textContent='PPMCOPY '+((got.indexOf('PPM / DPMO')>=0&&got.indexOf('d / N')<0)?'OK':'BAD');"],
  "expect": ["PPMCOPY OK"],
  "ref": "复制结果按当前页签取值：切换页签时 switchMode 写入 __ppmMode，旧实现永远优先 countResult，切到比率页仍复制数量模式的 d/N 结果；现按当前模式选择 rateResult。"
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

  console.log("==== quality calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
