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
  "slug": "quality/process-capability",
  "inputs": {
    "usl2": "10.5",
    "lsl2": "9.5",
    "dataInput": "10.1, 9.9, 10.0, 10.2, 9.8"
  },
  "clicks": [
    "document.getElementById('tab-manual').classList.remove('active');document.getElementById('tab-data').classList.add('active');calc();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='PC71 '+((t.indexOf('Cpk 实际能力')>=0&&t.indexOf('请填写')<0)?'OK':'BAD');"
  ],
  "expect": [
    "PC71 OK"
  ],
  "ref": "数据模式只校验当前页签：旧守卫把隐藏的手工档 usl/lsl/mean/sigma 也列为必填，数据页在手工档为空时直接报「请填写过程均值」；现按 tab-data 只校验 usl2/lsl2/dataInput。"
},
{
  "slug": "quality/process-capability",
  "inputs": {
    "usl": "10",
    "lsl": "10.5",
    "mean": "10",
    "sigma": "0.1"
  },
  "expect": [
    "USL 必须大于 LSL"
  ],
  "ref": "规格限颠倒：旧实现照算 Cp=-0.83、Cpk=-1.67 并给「能力不足」；现 USL≤LSL 直接拦截。默认 13.5/9.5 合法，不命中。"
},
{
  "slug": "quality/process-capability",
  "inputs": {
    "usl2": "10.5",
    "lsl2": "9.5",
    "dataInput": "10.1, abc, 9.9, 10.0"
  },
  "clicks": [
    "document.getElementById('tab-manual').classList.remove('active');document.getElementById('tab-data').classList.add('active');calc();"
  ],
  "expect": [
    "无法解析的片段"
  ],
  "ref": "样本含非法片段：旧 parseData 静默丢词后按 3 个数出结果；现列出「abc」等无法解析片段并停止计算。"
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
    "dataInput": "10.1, 9.9, 10.0, 10.2, 9.8"
  },
  "clicks": [
    "document.getElementById('tab-manual').classList.remove('active');document.getElementById('tab-data').classList.add('active');var got='';var old=ToolBox.copyText;ToolBox.copyText=function(t){got=String(t);};try{copyResult();}catch(e){}ToolBox.copyText=old;document.getElementById('__tbProbe').textContent='PCCOPY '+((got.indexOf('Cpk=')>=0&&got.indexOf('DPMO=')>=0)?'OK':'BAD');"
  ],
  "expect": [
    "PCCOPY OK"
  ],
  "ref": "数据页复制与屏幕一致：旧 copyResult 固定读手工档并重算，数据页复制出的是另一组 Cp/Cpk；现按当前页签取数并重算。"
},
{
  "slug": "quality/six-sigma",
  "inputs": {
    "dpmo": "6210"
  },
  "clicks": [
    "document.getElementById('dpmo').value='6210';fromDpmo();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='SSBASE '+((t.indexOf('4.00σ')>=0&&t.indexOf('良好')>=0&&t.indexOf('99.3790%')>=0)?'OK':'BAD');"
  ],
  "expect": [
    "SSBASE OK"
  ],
  "ref": "默认 6210 DPMO ⇒ 长期 4.00σ、短期 5.50σ、合格率 99.3790%、等级「良好（4σ）」；原自动用例依赖 st=7 被钳到 6σ 的输出，6σ 上限改为显式拦截后不再适用。"
},
{
  "slug": "quality/six-sigma",
  "clicks": ["document.getElementById('dpmo').value='2000000';fromDpmo();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='SSD '+((t.indexOf('DPMO 不能超过 1,000,000')>=0)?'OK':'BAD');"],
  "expect": ["SSD OK"],
  "ref": "DPMO 2,000,000：旧实现把合格率钳到 1e-9 仍展示原 DPMO 与 0.0000% 合格率；现越界即提示并停止计算。默认 6210 不命中。"
},
{
  "slug": "quality/six-sigma",
  "clicks": ["document.getElementById('yield').value='150';fromYield();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='SSY '+((t.indexOf('合格率不能超过 100%')>=0)?'OK':'BAD');"],
  "expect": ["SSY OK"],
  "ref": "合格率 150%：旧实现得 DPMO=-500000 并显示负 DPMO；现拦截 >100%。"
},
{
  "slug": "quality/six-sigma",
  "clicks": ["document.getElementById('st').value='8';fromSt();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='SST '+((t.indexOf('短期水平请不超过 6')>=0)?'OK':'BAD');"],
  "expect": ["SST OK"],
  "ref": "短期水平 8σ：旧实现输入保留 8 而结果钳到 6σ，屏幕自相矛盾；现按 6σ（3.4 DPMO）上限拦截。"
},
{
  "slug": "quality/six-sigma",
  "clicks": ["fromDpmo();var got='';var old=ToolBox.copyText;ToolBox.copyText=function(t){got=String(t);};try{copyResult();}catch(e){}ToolBox.copyText=old;document.getElementById('__tbProbe').textContent='SSCOPY '+((got&&got.indexOf('短期西格玛水平')>=0)?'OK':'BAD');"],
  "expect": ["SSCOPY OK"],
  "ref": "复制结果：结果区为 HTML 卡片（无 innerText），旧实现取空串并弹无参 i18nText；现回退到 textContent/innerHTML 去标签后复制，文本非空且含「短期西格玛水平」。"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
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
