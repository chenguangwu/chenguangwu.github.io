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
      "350.0 kg"
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
    "expect": ["20.0 L", "17.9 kg", "8.94 kg", "26.8 kg", "89.38 元", "8.0 天", "3.58 kg"],
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
  ,{
    "slug": "beekeeping/honey-estimator",
    "inputs": {"hives":"10","area":"120"},
    "expect": ["350.0 kg"],
    "ref": "第829批：10 群需求 40 亩，120 亩恰为 3 倍。旧实现面积 >3 倍才加成、刚超阈值即 +10%，现达到需求后固定 1.0，10×35=350.0 kg；与 200 亩同值，证明无阈值跳变。"
  },
  {
    "slug": "beekeeping/winter-feed-syrup",
    "inputs": { "n":"5","vol":"0.00000001","ratio":"2","price":"5","daily":"0.5","days":"10" },
    "expect": ["每群补饲量 0.001–100 L"],
    "ref": "第865批：小于 0.001 L 的微量补饲四舍五入后显示 0.0 L，与实际喂入不符；现下限 0.001 L，直接拒绝并提示有效区间。"
  },
  {
    "slug": "beekeeping/winter-feed-syrup",
    "inputs": { "n":"5","vol":"4","ratio":"2","price":"5","daily":"0.5","days":"10" },
    "expect": ["缺口 1.00 L/群","合计 5.00 L","计划与备料不匹配"],
    "ref": "第829批：计划 10 天×0.5 L/群=5 L/群，实备 4 L/群 ⇒ 缺口 1.0 L/群、合计 5.0 L。旧实现只显示「按计划10天」与消耗15天，不比较两者。"
  },
  {
    "slug": "beekeeping/winter-feed-syrup",
    "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/beekeeping/winter-feed-syrup.html','utf8');var ok=h.indexOf('../agriculture/cycle-honey.html')>=0&&h.indexOf('../agriculture/detector-13.html')>=0&&h.indexOf('../it/gitignore-generator.html')<0&&h.indexOf('../it/ast-viewer.html')<0;document.getElementById('__tbProbe').textContent='TB852R '+(ok?'OK':'BAD');})();"],
    "expect": ["TB852R OK"],
    "ref": "第852批：越冬补饲的 5 个开发工具推荐（.gitignore / properties / API 签名 / ASCII 树 / AST）全部替换为养蜂与农业相关页，保留养蜂采蜜量估算；探针断言旧 /it/ 链接已消失。"
  }
,
{
    "slug": "beekeeping/winter-feed-syrup",
    "inputs": { "n":"1","vol":"0.001","ratio":"2","price":"5","daily":"0.05","days":"30" },
    "expect": ["1.00 mL","1.34 kg","894 mg","447 mg","0.004 元"],
    "ref": "第865批：每群仅 0.001 L 时固定 toFixed(1) 会显示 0.0 L/0.0 kg；日耗按页面下限 0.05 L 不影响糖量；现按量级自适应为 mL/mg，糖 894 mg、水 447 mg、总重 1.34 kg、成本 0.004 元。"
  }
,
  {
    "slug": "beekeeping/winter-feed-syrup",
    "inputs": { "n":"5","vol":"4","ratio":"2","price":"5","daily":"0.5","days":"10" },
    "clicks": ["var cap=null;var old=__wsCsvDownload;__wsCsvDownload=function(n,rows){cap=rows;};exportCSV();__wsCsvDownload=old;var t=cap?cap.map(function(r){return r.join('|');}).join(' / '):'';document.getElementById('__tbProbe').textContent='WCSV '+((t.indexOf('每日消耗|0.50')>=0&&t.indexOf('计划天数|10')>=0&&t.indexOf('计划期需糖浆|5.0')>=0&&t.indexOf('计划期缺口（每群）|-1.00 L')>=0&&t.indexOf('计划期缺口（合计）|-5.00 L')>=0)?'OK':'BAD:'+t);"],
    "expect": ["WCSV OK"],
    "ref": "复核失败重做·导出复用差额：5 群、4 L/群、0.5 L/天、10 天 ⇒ 计划需 5 L/群，缺口 1.00 L/群、合计 5.00 L；CSV 必须同时含每日消耗、计划天数、计划期需糖浆与每群/合计缺口。旧导出只有预计饲喂天数。"
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
