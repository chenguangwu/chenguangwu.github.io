#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "woodworking/angle-cut",
  "inputs": {
    "jointAngle": "135",
    "segments": "2",
    "miterAngle": "45",
    "bevelAngle": "0",
    "startWidth": "50",
    "endWidth": "20",
    "taperLength": "200"
  },
  "expect": [
    "67.50° 每侧斜接角",
    "22.50° 锯台设置角"
  ],
  "ref": "接头夹角135°：每侧斜接角=135÷2=67.50°，锯台=90−67.50=22.50°；旧公式额外把每段角再折半得56.25°。段数2/4 只影响多边形示意。"
},
{
  "slug": "woodworking/board-feet",
  "inputs": {
    "thicknessIn": "4",
    "widthIn": "6",
    "lengthFt": "8",
    "quantity": "1",
    "price": "5",
    "convertValue": "100"
  },
  "expect": [
    "16.0000"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/moisture-content",
  "inputs": {
    "wetWeight": "180",
    "dryWeight": "100"
  },
  "expect": [
    "每100cm收缩0.00cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/mortise-size",
  "inputs": {
    "thickness": "30",
    "width": "80"
  },
  "expect": ["榫厚： 12 mm","实际板厚比 40%","贯通榫基准 40% × 1 倍率 × 硬度因子 1","榫宽： 56 mm","榫深： 90 mm"],
  "ref": "#861 榫厚倍率口径：贯通榫 1.0× 标准 = 板厚 40%，结果同时给出实际板厚比、榫型基准与硬度因子。"
},
{
  "slug": "woodworking/wood-screws",
  "inputs": {
    "totalThick": "45",
    "topThick": "15"
  },
  "expect": [
    "穿透下层约67%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "woodworking/board-feet",
  "inputs": {
    "thicknessIn": "0",
    "widthIn": "6",
    "lengthFt": "8",
    "quantity": "10",
    "price": "5"
  },
  "clicks": [
    "calcBF();var g=String(document.getElementById('bfGrid').innerHTML),r=String(document.getElementById('bfResult').innerHTML);document.getElementById('__tbProbe').textContent='BF0 '+((g===''&&r.indexOf('请输入有效尺寸')>=0)?'OK':'BAD');"
  ],
  "expect": [
    "BF0 OK"
  ],
  "ref": "厚度 0：旧代码只改结果文字、结果卡 bfGrid 仍保留上一次的 40 BF 汇总；现无效尺寸同时清空 bfGrid 与结果，避免旧采购数据被误读。默认 1×6×8×10 为有效输入，不命中。"
},
{
  "slug": "woodworking/board-feet",
  "inputs": {
    "thicknessIn": "1",
    "widthIn": "6",
    "lengthFt": "8",
    "quantity": "0",
    "price": "5"
  },
  "clicks": [
    "calcBF();var g=String(document.getElementById('bfGrid').innerHTML),r=String(document.getElementById('bfResult').innerHTML);document.getElementById('__tbProbe').textContent='BFQ '+((g===''&&r.indexOf('数量须为正整数')>=0)?'OK':'BAD');"
  ],
  "expect": [
    "BFQ OK"
  ],
  "ref": "数量 0：旧代码 parseInt(...)||1 把 0 静默改成 1 根并输出结果；现要求正整数，非法时清空结果卡并提示。默认 quantity=1 合法，不命中。"
},
{ slug:"woodworking/wood-screws", clicks:["document.getElementById('totalThick').value='10';document.getElementById('topThick').value='5';recommend();document.getElementById('__tbProbe').textContent='WS861 '+document.getElementById('result').innerText;"], expect:["WS861","无法选到不穿透的标准长度","穿入下层至少 5.0mm","总厚−2mm"], ref:"#861 薄板：总厚10/上层5 旧实现先限总厚再强制≥12并向上取整 → 推荐15mm 穿透；现明确无法满足并提供替代连接方式。" },
{ slug:"woodworking/wood-screws", clicks:["document.getElementById('totalThick').value='30';document.getElementById('topThick').value='30';recommend();document.getElementById('__tbProbe').textContent='WS861B '+document.getElementById('result').innerText;"], expect:["WS861B","上层厚度必须小于总厚度"], ref:"#861 板厚关系：上层等于总厚时下层为0，旧实现继续算穿透比例；现拦截。" },
{ slug:"woodworking/angle-cut", clicks:["document.getElementById('jointAngle').value='90';document.getElementById('segments').value='2';calcMiter();document.getElementById('__tbProbe').textContent='AC861 '+document.getElementById('miterResult').innerText;"], expect:["AC861","每侧斜接角： 45.00°","锯台设置角度（从垂直方向）： 45.00°"], ref:"#861 直角相框：90° 两根材料每侧切45°，锯台设45°；旧公式输出斜接67.5/锯台22.5。" },
{ slug:"woodworking/angle-cut", clicks:["document.getElementById('jointAngle').value='90';document.getElementById('segments').value='100000';calcMiter();document.getElementById('__tbProbe').textContent='AC861B '+document.getElementById('miterResult').innerText+'|'+document.getElementById('miterVis').innerHTML.length;"], expect:["AC861B","段数须为 2–12 的整数","|0"], ref:"#861 大段数：旧实现按段数循环生成SVG，100000 段可卡死；现范围校验并清空旧示意。" },
{ slug:"woodworking/angle-cut", clicks:["document.getElementById('jointAngle').value='90';document.getElementById('segments').value='2.5';calcMiter();document.getElementById('__tbProbe').textContent='AC861C '+document.getElementById('miterResult').innerText;"], expect:["AC861C","段数须为 2–12 的整数"], ref:"#861 小数段数：旧 parseInt 静默截断为2；现要求整数并提示。" },
{ slug:"woodworking/angle-cut", clicks:["document.getElementById('startWidth').value='50';document.getElementById('endWidth').value='50';document.getElementById('taperLength').value='200';calcTaper();document.getElementById('__tbProbe').textContent='AC861D '+document.getElementById('taperResult').innerText;"], expect:["AC861D","直切，无锥度","0° 直切","不需调整锯台角度"], ref:"#861 零锥度：起止宽相等时旧文本 1:Infinity 触发通用无效值替换；现显示直切与0锥度。" },
{ slug:"woodworking/angle-cut", clicks:["document.getElementById('startWidth').value='';document.getElementById('endWidth').value='20';document.getElementById('taperLength').value='200';calcTaper();document.getElementById('__tbProbe').textContent='AC861E '+document.getElementById('taperResult').innerText;"], expect:["AC861E","均须为大于 0 的有限数值","已清除旧结果"], ref:"#861 空宽度：旧 parseFloat||0 把空值当0；现拦截并清空旧结果。" },
{ slug:"woodworking/moisture-content", clicks:["document.getElementById('wetWeight').value='';document.getElementById('dryWeight').value='100';calc();document.getElementById('__tbProbe').textContent='MC861 '+document.getElementById('result').innerText;"], expect:["MC861","湿重不得留空","已清除旧结果"], ref:"#861 缺湿重：旧实现 wet=0 进入负含水率分支仍展示结果；现拦截并清空。" },
{ slug:"woodworking/moisture-content", clicks:["document.getElementById('wetWeight').value='90';document.getElementById('dryWeight').value='100';calc();document.getElementById('__tbProbe').textContent='MC861B '+document.getElementById('result').innerText+'|'+document.getElementById('dataGrid').innerHTML.length;"], expect:["MC861B","湿重不能小于绝干重量","|0"], ref:"#861 湿重<绝干重：旧实现提示数据异常但仍展示负含水率与收缩；现不输出结果卡。" },
{ slug:"woodworking/moisture-content", clicks:["document.getElementById('wetWeight').value='100';document.getElementById('dryWeight').value='100';calc();document.getElementById('__tbProbe').textContent='MC861C '+document.getElementById('result').innerText;"], expect:["MC861C","含水率： 0.00%","很低（近绝干）"], ref:"#861 湿重=绝干重：合法0%含水率，须正常计算，不得被空态/负值守卫拦截。" },
{ slug:"woodworking/mortise-size", clicks:["document.getElementById('thickness').value='';document.getElementById('width').value='80';calc();document.getElementById('__tbProbe').textContent='MS861 '+document.getElementById('result').innerText+'|'+document.getElementById('dataGrid').innerHTML.length;"], expect:["MS861","请填写大于 0 的板厚","|0"], ref:"#861 空板厚：旧 parseFloat||20 静默替换为20；现拦截并清空结果。" },
{ slug:"woodworking/mortise-size", clicks:["document.getElementById('thickness').value='20';document.getElementById('width').value='';calc();document.getElementById('__tbProbe').textContent='MS861B '+document.getElementById('result').innerText;"], expect:["MS861B","请填写大于 0 的板厚、板宽与榫厚倍率"], ref:"#861 空板宽：旧||80 静默替换；现拦截。" },
{ slug:"woodworking/mortise-size", clicks:["document.getElementById('thickness').value='25';document.getElementById('width').value='100';document.getElementById('jointType').value='dovetail';document.getElementById('ratio').value='1';document.getElementById('hardness').value='medium';calc();document.getElementById('__tbProbe').textContent='MS861C '+document.getElementById('result').innerText;"], expect:["MS861C","实际板厚比 60%","燕尾榫基准 60% × 1 倍率 × 硬度因子 1"], ref:"#861 比例口径：燕尾榫标准 1.0× 即板厚60%，结果明确实际比例与基准，不再把选项误读为40%。" },
{ slug:"woodworking/board-feet", clicks:["switchMode('convert',document.querySelector('.unit-tab:nth-child(2)'));document.getElementById('convertValue').value='';calcConvert();document.getElementById('__tbProbe').textContent='BF861 '+document.getElementById('convertResult').innerText;"], expect:["BF861","请填写要换算的数值"], ref:"#861 换算空值：旧 parseFloat||0 仍输出全0结果；现仅提示填写。" },
{ slug:"woodworking/board-feet", clicks:["switchMode('convert',document.querySelector('.unit-tab:nth-child(2)'));document.getElementById('convertValue').value='-10';calcConvert();document.getElementById('__tbProbe').textContent='BF861B '+document.getElementById('convertResult').innerText;"], expect:["BF861B","材积不能为负数"], ref:"#861 换算负值：旧实现计算负材积；现范围错误提示。" },
{ slug:"woodworking/board-feet", clicks:["switchMode('convert',document.querySelector('.unit-tab:nth-child(2)'));document.getElementById('convertValue').value='0';calcConvert();document.getElementById('__tbProbe').textContent='BF861C '+document.getElementById('convertResult').innerText;"], expect:["BF861C","板英尺(BF)： 0.0000","立方米(m³)： 0.000000"], ref:"#861 换算合法零：0 应正常换算为全0，不得被空值守卫拦截。" }
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

  console.log("==== woodworking calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
