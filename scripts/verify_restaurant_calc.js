#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "restaurant/delivery-time",
  "inputs": {
    "distance": "6.5",
    "speed": "20",
    "prepTime": "15",
    "pickupWait": "5",
    "deliverWait": "3"
  },
  "expect": [
    "6.5km"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/dish-cost-card",
  "inputs": {
    "dishName": "宫保鸡丁",
    "dishQty": "4",
    "dishPrice": "38",
    "yieldRate": "95"
  },
  "expect": [
    "37.11"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/menu-margin",
  "clicks": ["dishes=[{name:'宫保鸡丁',cost:18,price:48},{name:'麻婆豆腐',cost:8,price:26},{name:'清蒸鲈鱼',cost:45,price:98}];calc()"],
  "expect": [
    "¥172.00 总售价",
    "58.7% 综合毛利率",
    "69.2%"
  ],
  "ref": "顶层数组 dishes 注入：总售价 48+26+98 = ¥172.00、总成本 18+8+45 = ¥71.00、总毛利 ¥101.00、综合毛利率 101/172×100 = 58.7%；麻婆豆腐 (26−8)/26×100 = 69.2%。默认态为源码内置菜单（166.00），三串均不命中。"
},
{
  "slug": "restaurant/menu-margin",
  "inputs": {
    "tmCost": "20",
    "tmMargin": "60"
  },
  "expect": [
    "建议售价: 50.00 元",
    "单品毛利: 30.00 元"
  ],
  "ref": "2026-10-27 新增「目标毛利率定价反推」：注入成本20、目标毛利率60% ⇒ 售价=20/(1−0.6)=50.00、单品毛利30.00、校验 20÷0.40=50.00。默认态成本10/毛利率50% ⇒ 售价20.00，两锚均不命中 ⇒ 强判别零逃生。"
},
{
  "slug": "restaurant/menu-pricing",
  "inputs": {
    "material": "18",
    "labor": "20",
    "fixed": "3",
    "margin": "60"
  },
  "expect": [
    "24.60"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/safety-stock",
  "inputs": {
    "ingName": "鸡腿肉",
    "avgDaily": "8",
    "maxDaily": "8",
    "avgLead": "3",
    "maxLead": "7",
    "orderCost": "50",
    "holdCost": "12",
    "currentStock": "20",
    "workDays": "365"
  },
  "expect": [
    "每次订156.0kg"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/seasoning-scaler",
  "inputs": {
    "origServings": "5",
    "targetServings": "6"
  },
  "expect": [
    "×1.20"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/table-turnover",
  "inputs": {
    "hours": "15",
    "tables": "20",
    "avgTime": "45",
    "occupancy": "70",
    "perTable": "3",
    "avgSpend": "65"
  },
  "expect": [
    "30.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "restaurant/taste-preference",
  "inputs": {},
  "clicks": [
    "localStorage.getItem=function(k){return k==='taste_preference_records'?JSON.stringify([{taste:'sweet',time:'2026-01-01'},{taste:'sweet',time:'2026-01-02'},{taste:'sour',time:'2026-01-03'}]):null;};renderGrid();renderStats();"
  ],
  "expect": [
    "🍬 甜 2 票"
  ],
  "ref": "localStorage 覆写注入（同 BATCH116 cleaning/appliance-cycle 打法）：本页记录唯一数据源是 TASTE_KEY='taste_preference_records'，renderGrid/renderStats 每次都经 loadRecords() 重读 ⇒ 覆写 localStorage.getItem 后再强制重渲染即等价「用户已投 甜×2、酸×1」，独立复算得 甜 2 票 / 酸 1 票 / 总 3 票。不走 recordTaste() 是因为 tastes 常量在另一个 <script> 块，pageEval 作用域取不到 ⇒ 调用必抛 undefined.name。旧锚「暂无记录…」是空态提示 ⇒ 判别力 0。清 clicks 后 localStorage 无记录 ⇒ 退回空态提示 ⇒ 零逃生项。"
},
  {
    slug: "restaurant/bbq-portion",
    inputs: { people: "14", type: "korean", drink: "yes" },
    clicks: ["calcTool()"],
    expect: ["6300 g", "2800 g", "30 瓶"],
    ref: "韩式烤肉（meatPer=450、skewerPer=0）：肉 450×14=6300 g；蔬菜 200×14=2800 g；"
       + "主食 150×14=2100 g；含饮品 round(14×700/330)=round(29.70)=30 瓶。"
       + "原 expect 的 72 串/2100 g/1200 g/13 瓶 即默认态（6 人中式含饮品）输出，属逐字回显默认结果、零判别力；"
       + "且 2100 g 与默认态肉类总量同值（回退默认仍命中，会成逃生项）故不入断言。",
  },

  {
    slug: "restaurant/hotpot-portion",
    inputs: { people: "4", style: "meat", intensity: "normal" },
    expect: ["1320 g", "600 g", "360 g", "320 g", "1000 ml"],
    ref: "总量 4×600×1.0=2400 g；肉 2400×0.55=1320；蔬菜 2400×0.25=600；"
       + "豆制品 2400×0.15=360；主食 4×80=320；汤底 4×250=1000 ml",
  },
{
  "slug": "restaurant/taste-preference",
  "inputs": {},
  "clicks": ["var a=[];for(var i=0;i<50;i++)a.push({taste:'sweet',time:'2026-11-05'});for(var i=0;i<40;i++)a.push({taste:'salty',time:'2026-11-05'});for(var i=0;i<30;i++)a.push({taste:'spicy',time:'2026-11-05'});localStorage.getItem=function(k){return k==='taste_preference_records'?JSON.stringify(a):null;};renderGrid();renderStats();"],
  "expect": ["41.7%", "33.3%", "25.0%", "42%"],
  "ref": "深度解析算例复算：甜 50 / 咸 40 / 辣 30，总 120 ⇒ 50÷120=41.7%、40÷120=33.3%、30÷120=25.0%；最高占比 41.67% 取整 42%。默认空态只有提示、无百分比 ⇒ 不命中。"
},
{
  "slug": "restaurant/menu-pricing",
  "inputs": {"material": "", "labor": "", "fixed": "", "margin": ""},
  "clicks": ["calc()"],
  "expect": ["请填写原料成本、人工费率、固定成本与目标毛利率后再计算。"],
  "ref": "空态：四项全清后不再按 0/默认 60 计算，改为提示；默认 12/350/8/60 ⇒ 成本与售价报告，不命中。"
},
  {
    slug: "restaurant/safety-stock",
    inputs: { avgDaily: "", maxDaily: "8", avgLead: "3", maxLead: "7", orderCost: "50", holdCost: "12", currentStock: "20" },
    expect: ["请填写平均日消耗量、最大日消耗量、平均/最大到货天数、单次订货成本、单位持有成本与当前库存后再计算。"],
    ref: "空态守卫（2026-11-05）：清空平均日消耗量后不再渲染「0.0 安全库存 / 0.0 再订货点 / 0.0 经济订货量 / 0 预计可用天数」与「⚠️ 低于安全库存！」风险结论，只给填写提示。⚠ 判空用原始空串——currentStock=0（库存用光）、orderCost=0、holdCost=0 均为合法值，不在拦截范围。注入 8/8/3/7/50/12/20 用例断「每次订156.0kg」⇒ 两态互斥。",
  },
  {
    "slug": "restaurant/dish-cost-card",
    "clicks": ["var q=document.getElementById('dishQty');var step=q.getAttribute('step');document.getElementById('dishName').value='半份测试';q.value='1.5';calc();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='DISHSTEP '+(step==='0.5'&&h.indexOf('半份测试')>=0&&h.indexOf('¥')>=0?'OK':'BAD step='+step);"],
    "expect": ["DISHSTEP OK"],
    "ref": "937预设步长：份数「大规模」预设 1.5 须合法，输入 min=1 且 step=0.5 才符合 HTML 默认步长；旧版无 step（默认 1）1.5 触发 stepMismatch。探针同时要求 step=0.5、1.5 份参与计算产出结果容器。默认态 step 缺失⇒BAD。"
  },
  {
    "slug": "restaurant/safety-stock",
    "clicks": ["var $=function(id){return document.getElementById(id);};function set(v){var ids=['avgDaily','maxDaily','avgLead','maxLead','orderCost','holdCost','currentStock','workDays'],ks=['avgDaily8','maxDaily8','avgLead3','maxLead7','orderCost50','holdCost12','currentStock20','workDays365'];for(var i=0;i<ids.length;i++) $(ids[i]).value=String(v[ks[i]]);}$('ingName').value='守卫测试';set({avgDaily8:-5,maxDaily8:8,avgLead3:3,maxLead7:7,orderCost50:50,holdCost12:12,currentStock20:20,workDays365:365});calc();var neg=/平均日消耗量须大于 0/.test($('result').innerHTML);set({avgDaily8:5,maxDaily8:8,avgLead3:3,maxLead7:7,orderCost50:50,holdCost12:0,currentStock20:20,workDays365:365});calc();var hc=/单位持有成本须大于 0/.test($('result').innerHTML);set({avgDaily8:5,maxDaily8:8,avgLead3:3,maxLead7:7,orderCost50:50,holdCost12:12,currentStock20:20,workDays365:400});calc();var wd=/年营业天数须为 1–366/.test($('result').innerHTML);set({avgDaily8:5,maxDaily8:8,avgLead3:3,maxLead7:7,orderCost50:50,holdCost12:12,currentStock20:20,workDays365:365});calc();var ok=/安全库存/.test($('result').innerHTML)&&/经济订货量/.test($('result').innerHTML);document.getElementById('__tbProbe').textContent=(neg&&hc&&wd&&ok)?'__SAFE_L7_OK__':'__SAFE_L7_BAD__ '+[neg,hc,wd,ok].join(',');"],
    "expect": ["__SAFE_L7_OK__"],
    "ref": "第1101批 L7：旧版 avgDaily=-5 使年需求负、EOQ NaN→「—」、daysLeft 恒 0 仍判「低于安全库存」；holdCost=0 被 ||0.01 静默替换；workDays=400 无校验。新：日均≤0/持有成本≤0/营业天数非1-366均报字段错误并清空表，合法值正常出安全库存+EOQ。旧版三哨兵全红。"
  },
{ slug:"restaurant/delivery-time", inputs:{"distance":"","speed":"","prepTime":"","pickupWait":"","deliverWait":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"restaurant/seasoning-scaler", inputs:{"origServings":"","targetServings":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"restaurant/table-turnover", inputs:{"hours":"","tables":"","avgTime":"","occupancy":"","perTable":"","avgSpend":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{ slug:"restaurant/delivery-time", clicks:["calc();var had=!!window._resultText;['distance','speed','prepTime','pickupWait','deliverWait'].forEach(function(id){document.getElementById(id).value='';});calc();var g='';ToolBox.copyText=function(t){g+=String(t)};copyResult();document.getElementById('__tbProbe').textContent='B616DT '+((had&&!window._resultText&&g==='')?'OK':'BAD g='+g.slice(0,40));"], expect:["B616DT OK"], ref:"第1366批空态缓存：默认计算后清空时间输入，calc 提前返回必须清 empty _resultText，copyResult 不得复制旧送达时间。旧实现保留旧串 ⇒ BAD。" },
{ slug:"restaurant/seasoning-scaler", clicks:["calc();var had=!!window._copyText;['origServings','targetServings'].forEach(function(id){document.getElementById(id).value='';});calc();var g='';ToolBox.copyText=function(t){g+=String(t)};copyResult();document.getElementById('__tbProbe').textContent='B616SS '+((had&&!window._copyText&&g==='')?'OK':'BAD g='+g.slice(0,40));"], expect:["B616SS OK"], ref:"第1367批空态缓存：默认缩放后清空人数，calc 提前返回必须清 _copyText，复制不得输出旧缩放清单。旧实现保留旧串 ⇒ BAD。" },
{ slug:"restaurant/table-turnover", clicks:["calc();['hours','tables','avgTime','occupancy','perTable','avgSpend'].forEach(function(id){document.getElementById(id).value='';});calc();var bar=document.getElementById('resultRefBar').innerHTML;var g='';ToolBox.copyText=function(t){g+=String(t)};copyResult();document.getElementById('__tbProbe').textContent='B616TT '+((bar===''&&!window._resultText&&g==='')?'OK':'BAD bar='+bar.length+' g='+g.slice(0,30));"], expect:["B616TT OK"], ref:"第1368批空态缓存：默认翻台率结果后清空全部输入，calc 必须同时清 resultRefBar 与 _resultText；旧评价标尺和复制串均不得残留。旧实现两者保留 ⇒ BAD。" }
,{ slug:"restaurant/menu-margin", clicks:["dishes=[{name:'空成本',cost:'',price:48},{name:'负售价',cost:10,price:-5}];calc();"], expect:["成本须为 ≥0 的数值","售价须为 ≥0 的数值","未计算"], ref:"菜品成本/售价不再 ||0 兜底：空成本与负售价分别列出行号与提示并停止计算；旧实现按 0 计、负售价照算毛利。" }
,{ slug:"restaurant/menu-margin", clicks:["dishes=[{name:'赠品',cost:5,price:0},{name:'正常菜',cost:10,price:30}];calc();"], expect:["不适用（售价 0）","综合毛利率"], ref:"售价 0 的赠品毛利率不可定义，显示「不适用」并从低/高毛利统计与图中排除；综合毛利率只按有售价菜品计算 20/30=66.7%。旧实现显示 0.0% 并计入统计。" }
,{ slug:"restaurant/seasoning-scaler", inputs:{"origServings":"4","targetServings":""}, clicks:["calc();"], expect:["目标人数须为大于 0 的数值"], ref:"单项目标人数留空不再静默按 1；空值/0/负数均停止缩放。" }
,{ slug:"restaurant/seasoning-scaler", clicks:["seasonings=[{name:'盐',amount:'-2',unit:'g'}];renderRows();calc();"], expect:["原用量须为 ≥0 的数值","未缩放"], ref:"负用量不再输出负调料量，停止并提示行号。" }
,{ slug:"restaurant/dish-cost-card", inputs:{"dishName":"半份","dishQty":"0.5","dishPrice":"20","yieldRate":"95"}, clicks:["calc();"], expect:["半份 标准成本卡","¥"], ref:"份数 0.5 半份合法并参与成本计算；旧实现 qty<1 拒绝，与提示「允许半份」矛盾。" }
,{ slug:"restaurant/table-turnover", inputs:{"hours":"10","tables":"10","avgTime":"60","occupancy":"0","perTable":"4","avgSpend":"50"}, clicks:["calc();"], expect:["0.00","¥0"], ref:"上座率合法 0% 不再被 ||100 替换为满座：实际翻台率 0.00、日接待 0 桌、营业额 ¥0；旧实现输出正常客流。" }
,{ slug:"restaurant/bbq-portion", inputs:{"people":"2","type":"bbq","drink":"yes"}, clicks:["calcTool();"], expect:["5 瓶","1650 ml","基准 1400 ml"], ref:"2 人×700ml=1400ml，330ml/瓶须向上取整为 5 瓶（1650ml）；旧四舍五入得 4 瓶 1320ml，低于基准。" }
,{ slug:"restaurant/delivery-time", inputs:{"distance":"0","speed":"20","prepTime":"10","pickupWait":"3","deliverWait":"2"}, clicks:["calc();"], expect:["0km","0 分钟"], ref:"零距离合法：基础骑行 0 分钟，不再静默替换为 1km；速度仍须 >0。" }
,{ slug:"restaurant/delivery-time", inputs:{"distance":"5","speed":"","prepTime":"10","pickupWait":"3","deliverWait":"2"}, clicks:["calc();"], expect:["平均车速须为大于 0 的数值","未计算"], ref:"速度空值不再回退 20，明确提示并停止。" }

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

  console.log("==== restaurant calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
