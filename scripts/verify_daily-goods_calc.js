#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  {
    "slug": "daily-goods/shoe-size",
    "inputs": {
      "footLen": "250"
    },
    "expect": [
      "39.5",
      "25.0"
    ],
    "ref": "250mm→EU39.5/CN25.0"
  },
  {
    "slug": "daily-goods/shoe-size",
    "inputs": {
      "footLen": "300",
      "gender": "w"
    },
    "expect": [
      "16.5",
      "14"
    ],
    "ref": "300mm 女码 US16.5/UK14"
  },
  {
    "slug": "daily-goods/shoe-size",
    "inputs": {
      "footLen": "100"
    },
    "expect": [
      "请输入200-320mm之间的脚长"
    ],
    "ref": "越界提示"
  },
  {
    "slug": "daily-goods/shoe-size",
    "inputs": {
      "footLen": ""
    },
    "expect": [
      "请输入200-320mm之间的脚长"
    ],
    "ref": "空值提示"
  },
  {
    "slug": "daily-goods/trash-bag-size",
    "inputs": { "bl": "50", "bw": "40", "bh": "60", "wt": "0", "over": "5", "sharp": "0" },
    "expect": ["180.0 cm", "90.0 cm", "85.0 cm", "120.0 L", "144.0 L", "0.012 mm"],
    "ref": "塑料袋公式独立复算：袋口周长=2×(50+40)=180；折径=90；袋长=60+40/2+5=85；桶容积=50×40×60/1000=120 L；建议袋容积=144 L；0 kg 与 0% 尖锐物取最薄档 0.012 mm。旧空态守卫若把 0 当未填写会不输出结果 ⇒ 强判别。"
  },
  {
    "slug": "daily-goods/trash-bag-size",
    "inputs": { "bl": "45", "bw": "35", "bh": "55", "wt": "5", "over": "10", "sharp": "15" },
    "expect": ["特大（80×100 cm）", "有现成规格"],
    "ref": "非默认桶 45×35、高 55、壁厚 5、外翻 10 ⇒ 折径 80.0、袋长 82.5；候选必须同时满足宽度和长度，最小可用规格为 80×100。默认 40×30/高 50 得 70×80，不命中。"
  },
  {
    "slug": "daily-goods/trash-bag-size",
    "inputs": { "bl": "60", "bw": "50", "bh": "100", "wt": "5", "over": "10", "sharp": "20" },
    "expect": ["定制（≥110×135 cm）", "需定制"],
    "ref": "深桶：折径 110、袋长 100+25+10=135；最大现成 100×120 仍不满足，必须明确标为定制，不能推荐 100×120。"
  },
  {
    "slug": "daily-goods/trash-bag-size",
    "inputs": {},
    "clicks": [
      "calcTool();document.getElementById('bl').value='';calcTool();var cv=document.getElementById('fitChart');var em=document.getElementById('chartEmpty');document.getElementById('__tbProbe').textContent='CHART '+cv.getAttribute('data-empty')+'|'+(em.hidden?'hidden':'shown')+'|'+document.getElementById('result').textContent.slice(0,30);"
    ],
    "expect": ["CHART 1|shown|"],
    "ref": "先合法计算再清空桶口长：结果区提示为空，旧图表必须清空并显示等待参数的空态；data-empty=1、chartEmpty 可见。"
  },
  {
    "slug": "daily-goods/trash-bag-size",
    "inputs": { "bl": "40abc", "bw": "30", "bh": "50", "wt": "6", "over": "10", "sharp": "20" },
    "expect": ["参数无效"],
    "ref": "严格数值校验：`40abc` 不得被 parseFloat 截成 40 参与计算，必须报参数无效并清空图表。"
  },
  {
    "slug": "daily-goods/trash-bag-size",
    "inputs": { "bl": "30", "bw": "40", "bh": "50", "wt": "0", "over": "10", "sharp": "0" },
    "expect": ["75.0 cm", "70×80 cm"],
    "ref": "第1098批·长宽互换：30×40×50、外翻10，短边仍为30，袋长=50+30/2+10=75.0；与 40×30 输入结果一致，推荐同为 70×80。旧公式用 bw/2 会得 80 cm，随输入顺序变化。"
  },
  {
    "slug": "daily-goods/trash-bag-size",
    "inputs": { "bl": "40", "bw": "30.4", "bh": "50", "wt": "0", "over": "10", "sharp": "0" },
    "expect": ["70.4 cm", "75.2 cm", "80×100 cm"],
    "ref": "第1098批·临界小数：40×30.4×50、外翻10 ⇒ 折径70.4、袋长75.2；屏幕保留一位小数，不能四舍五入成 70/95，导出同口径。"
  },
  {
    "slug": "daily-goods/trash-bag-size",
    "inputs": {},
    "clicks": [
      "var __bl=document.getElementById('bl');__bl.value='60';__bl.fire('input');"
    ],
    "expect": ["90.0 L", "180.0 cm"],
    "ref": "第1098批·快照一致：输入桶口长改为 60 并触发 input 后，输入桶口长改为 60 并触发 input 后，屏幕必须立即从默认 60 L 更新为 90 L；exportCSV 只读 lastCalc 快照，不再按当前输入二次重算。"
  },
  {
    "slug": "daily-goods/shoe-size",
    "inputs": {},
    "clicks": [
      "var __toast='',__copied='',__exported=0;window.ToolBox={showToast:function(m){__toast=m;},copyText:function(t){__copied=t;}};ToolBox=window.ToolBox;TBKit={util:{isEn:function(){return false;},exportTable:function(){__exported=1;}}};document.getElementById('footLen').value='100';calc();copyResult();__shoe_sizeExport();document.getElementById('__tbProbe').textContent='SHOEBAD '+((__toast.indexOf('200')>=0&&__copied===''&&__exported===0&&document.getElementById('shoe_sizeTable').textContent==='')?'OK':'BAD');"
    ],
    "expect": ["SHOEBAD OK"],
    "ref": "第1099批·无效输入守卫：脚长 100 越界后复制与导出都必须被拦截，提示包含 200；附表清空，不能复制错误提示或导出上一轮表格。"
  },

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

  console.log("==== daily-goods calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
