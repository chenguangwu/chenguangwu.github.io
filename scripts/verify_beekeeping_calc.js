#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "12",
      "area": "48"
    },
    "expect": [
      "420.0 kg"
    ],
    "ref": "12群×48亩 混合花源基准35kg（默认10群/50亩为350.0，避开）"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "20"
    },
    "expect": [
      "175.0 kg"
    ],
    "ref": "花源不足按面积折减(20/40=0.5)"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "200"
    },
    "expect": [
      "385.0 kg"
    ],
    "ref": "花源充足(>3倍需求)加成1.1"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "10",
      "area": "40"
    },
    "clicks": [
      "selectSource('rapeseed');calc();"
    ],
    "expect": [
      "450.0 kg"
    ],
    "ref": "油菜花源基准45kg/群"
  },
  {
    "slug": "beekeeping/honey-estimator",
    "inputs": {
      "hives": "",
      "area": "40"
    },
    "expect": [
      "请输入有效参数"
    ],
    "ref": "蜂箱空值提示"
  },
  {
    "slug": "beekeeping/winter-feed-syrup",
    "inputs": { "n": "5", "vol": "4", "ratio": "2", "price": "5", "daily": "0.5", "days": "10" },
    "expect": ["20.0 L", "17.9 kg", "8.9 kg", "26.8 kg", "89 元", "8.0 天", "3.6 kg"],
    "ref": "越冬糖浆独立复算：总糖浆=5×4=20 L；2:1 糖质量分数=2/3，实测密度 1.34 kg/L ⇒ 总重 26.8 kg、糖 17.9 kg、水 8.9 kg；成本按单价 5 元=89 元；饲喂天数=4/0.5=8.0；每群糖量 3.6 kg。"
  },  {
    "slug": "beekeeping/honey-estimator",
    "clicks": ["document.getElementById('hives').value='1.5';calc();var c=0;var old=ToolBox.copyText;ToolBox.copyText=function(){c++;};copyResult();ToolBox.copyText=old;document.getElementById('__tbProbe').textContent='TB828H '+((String(document.getElementById('honeyResult').textContent).trim()==='--'&&c===0)?'OK':'BAD');"],
    "expect": ["TB828H OK"],
    "ref": "第828批：1.5 群旧实现仍可计算，无效时复制又把 parseFloat 空值兜成 0、复制 0 kg。现在蜂箱须正整数，无效结果置 -- 且复制前检查 __honeyLast；探针替换 copyText 计数，要求零调用。"
  },
  {
    "slug": "beekeeping/winter-feed-syrup",
    "clicks": ["var c=0;var old=clearChart;clearChart=function(){c++;};document.getElementById('n').value='';calcTool();clearChart=old;document.getElementById('__tbProbe').textContent='TB828W '+((c>0&&document.getElementById('result').innerHTML.indexOf('请完整填写')>=0)?'OK':'BAD');"],
    "expect": ["TB828W OK"],
    "ref": "第828批：无效输入时旧实现只替换结果文字，上一次的成功柱状图仍留在 canvas。现在无效分支调用 clearChart() 清空画布；探针包裹 clearRect 计数并要求提示同时出现。"
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

  console.log("==== beekeeping calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
