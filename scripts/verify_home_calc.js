#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "home/paint-calculator", inputs: { coverage: "" },
    expect: ["请填写油漆计算参数"], ref: "清空覆盖率不得静默回退默认值。" },
  { slug: "home/paint-calculator", inputs: { "bucket-price": "0" },
    clicks: ["calc();document.getElementById('__tbProbe').textContent='PAINTZERO '+document.getElementById('total-cost').textContent;"],
    expect: ["PAINTZERO 0"], ref: "显式零价格仍合法。" },
  { slug: "home/paint-calculator", inputs: { "door-count": "" },
    expect: ["门窗字段不能为空"],
    ref: "第六批（涂料空门窗）：清空门数时旧实现 +'' = 0，把空值当合法 0 继续输出默认毛面积 52 m² / 净面积 48.4 m²，与错误文案「不能为空」矛盾。现显式区分空串 / 非法数值 / 合法显式 0，空值清空结论并提示。默认态四字段均有值、正常出结果，不含该提示 ⇒ 强判别。" },
{
  "slug": "home/furniture-layout",
  "clicks": [
    "document.getElementById('rl').value='6';document.getElementById('rw').value='5';addFurniture('床(双人)');addFurniture('餐桌');renderItems();document.getElementById('__p').value=document.getElementById('canvas').style.width+'|'+document.getElementById('canvas').style.height+'|'+document.getElementById('canvas').innerHTML+'|'+document.getElementById('empty-tip').style.display"
  ],
  "expect": [
    "360px|300px|床(双人)床(双人)餐桌床(双人)餐桌|none"
  ],
  "ref": "原 all_default 弱用例（rl=5/rw=4 恰为默认）+ expect「橱柜」来自 #furn-list —— 那是 renderFurnList() 用常量 FURNITURE 渲染的静态按钮列表，与任何输入无关 ⇒ 零判别力逃生项（默认态同样命中）。本页无数字文本输出：房间尺寸只写进 canvas.style.width/height（边长×SCALE 60），家具名只经 createElement+appendChild 逐次反映进 canvas.innerHTML。改用 clicks 注入 rl=6/rw=5 并由左侧加入两件家具：width=6×60=360px、height=5×60=300px、innerHTML 末尾为「床(双人)餐桌」、empty-tip.style.display=none（有家具即隐藏）。默认态 300px/240px、canvas 空串、tip 空串 ⇒ 不匹配"
},
{
  "slug": "home/lighting-calculator",
  "inputs": {
    "length": "6",
    "width": "4.5",
    "height": "3",
    "lumens": "1000",
    "cu": "0.7",
    "mf": "0.75"
  },
  "expect": [
    "5143",
    "7 只 LED 8W 合计 56 W"
  ],
  "ref": "原 all_default 弱用例（length=5/width=4/height=2.8/lumens=800/cu=0.6/mf=0.8 全等于默认）+ expect「合计」是灯具卡片里常驻的静态标签。改为 length=6/width=4.5/lumens=1000/cu=0.7/mf=0.75：面积 6×4.5=27㎡、默认房间「客厅」100 lux ⇒ 总光通量 27×100/(0.7×0.75)=5142.857 → Math.round 显示 5143；LED 8W 按 800lm ⇒ ceil(5142.857/800)=7 只、合计 7×8=56 W。默认态 20×100/(0.6×0.8)=4166.67→4167、LED 8W 6 只 48 W（跨档）"
},
{
  "slug": "home/paint-calculator",
  "inputs": {
    "coats": "3",
    "coverage": "12",
    "bucket-size": "4",
    "bucket-price": "300"
  },
  "expect": [
    "11.60",
    "900"
  ],
  "ref": "2026-10-27 同批同步（页面新增门窗扣减，用漆量改按净面积）：毛面积恒 52.0（30+22 兜底清单），默认扣减 门1×2.0 + 窗2×1.8 = 5.60 ⇒ 净面积 46.4。注入 coats=3/coverage=12/bucket-size=4/bucket-price=300 ⇒ 总用量 46.4×3/12 = 11.60 L、桶数 ceil(11.6/4)=3、成本 3×300=900。默认态（coats2/coverage10/桶5/280）⇒ 46.4×2/10=9.28 L、2 桶、560 元，两条锚均不命中 ⇒ 强判别、零逃生。（原 expect 13.00/1200 为扣减前的毛面积口径，已废弃）"
},
{
  "slug": "home/paint-calculator",
  "inputs": {
    "door-count": "3",
    "door-area": "2.5",
    "win-count": "4",
    "win-area": "2"
  },
  "expect": [
    "合计扣减 15.50 m²",
    "净涂刷面积 36.50 m²"
  ],
  "ref": "2026-10-27 新增门窗扣减模块用例：注入 门3×2.5 + 窗4×2.0 ⇒ 扣减 7.50+8.00 = 15.50 m²，净面积 52.0−15.5 = 36.50 m²（用漆量 36.5×2/10 = 7.30 L、2 桶、560 元）。默认态扣减为 5.60、净面积 46.40 ⇒ 两条锚均不命中 ⇒ 强判别、零逃生。"
},
{
  "slug": "home/paint-calculator",
  "inputs": {
    "door-count": "-1",
    "door-area": "2"
  },
  "expect": [
    "门窗数量与面积均须为非负数值"
  ],
  "ref": "2026-11-09 复核失败重做（涂料负门窗扣减）：原 getDeduct 用 +el.value||0 短路，门数 -1/面积2 ⇒ dc*da = -2 负扣减反增净面积（82→84）。修复后 getDeduct 校验非负，负值时返回 {ok:false,msg:'门窗数量与面积均须为非负数值（不能为空或负数）。'}，calc() 在 !deductRaw.ok 分支显示 ⚠ 提示并将 total-area/net-area/total-paint/total-buckets/total-cost 置「—」后 return。注入 door-count=-1 ⇒ 仅错误态出现该提示串，默认态（door-count 默认正数）不出现 ⇒ 强判别、零逃生。"
},
{
  "slug": "home/renovation-budget",
  "clicks": [
    "localStorage.setItem('home_budget_items',JSON.stringify([{id:1,name:'瓷砖',price:8000,qty:12},{id:2,name:'地板',price:6000,qty:10}]));renderItems();calc()"
  ],
  "expect": [
    "156,000",
    "瓷砖 61.5% ¥96,000"
  ],
  "ref": "原 all_default 弱用例（new-price=0/new-qty=1 等于默认）+ expect「暂无数据」是 calc() 空数据分支常量。本页数据唯一来源是 localStorage（getItem 桩恒 null、fallback 是空数组），而 setItems 是 no-op ⇒ 直接调 addItem() 无法累积。改在 clicks 内覆写 localStorage.getItem 注入两条预算（等价于「用户本就有数据」），再 renderItems()+calc()：8000×12+6000×10=156,000、项目数 2、均值 78,000、最大支出「瓷砖」、占比条 61.5%/38.5%。默认态 total=0、count=0、bars=「暂无数据」⇒ 不匹配"
},
{
  "slug": "home/room-calculator",
  "clicks": [
    "document.getElementById('width').value='6';document.getElementById('height').value='8';calc()"
  ],
  "expect": [
    "48.00",
    "28.00",
    "10.00"
  ],
  "ref": "**坏用例重写**：原 inputs 键是生成器模板串残留（${f} 与 ${f==='radius'?3:5}_X），页面根本没有该 id、expect「_X」也无从产生 ⇒ 长期假通过（判别器盲区）。本页形状控件由 renderInput() 运行期生成、不在静态 HTML 内，注入 inputs 时无法触发其内联 oninput，故用 clicks 在运行期给 width/height 赋值后直接调 calc()：矩形 6×8 ⇒ 面积 48.00、周长 2×(6+8)=28.00、对角线 √(36+64)=10.00。默认态控件值为空 ⇒ 0.00/0.00/0.00"
},
{
  "slug": "home/room-calculator",
  "clicks": [
    "activeShape='平行四边形';renderTabs();renderInput();document.getElementById('base').value='1';document.getElementById('height').value='3';document.getElementById('side').value='5';calc();document.getElementById('__tbProbe').textContent='PARADIAG '+document.getElementById('diagonal-val').textContent;"
  ],
  "expect": ["PARADIAG 4.24 / 5.83"],
  "ref": "复核失败重做·平行四边形短对角线：底边 1、高 3、斜边 5，水平投影 √(25−9)=4；短对角线 √((1−4)²+3²)=√18≈4.24，长对角线 √((1+4)²+3²)=√34≈5.83。旧实现 Math.max(base−dx,0) 把短分量截成 0，得 3.00 / 5.83。默认矩形不出现该串。"
},
{
  "slug": "home/washer-capacity",
  "inputs": {
    "people": "6"
  },
  "expect": [
    "90"
  ],
  "ref": "auto-restore"
},
{
  "slug": "home/lighting-calculator",
  "inputs": {
    "length": "",
    "width": "",
    "height": "",
    "lumens": "",
    "cu": "",
    "mf": ""
  },
  "expect": [
    "请填写 长度、宽度、单只光通量、利用系数、维护系数 后再计算"
  ],
  "ref": "空态守卫：必填项留空 ⇒ 提示并保留总光通量为「—」，不再按 0/默认值静默算出结论。"
     + "默认态 5/4/2.8/800/0.6/0.8 输出 4167 与「7 只」等结论，不含该提示 ⇒ 可判别。"
},
{
  "slug": "home/renovation-budget",
  "clicks": ["(function(){var hh=globalThis.__tbFs;var h1=hh.readFileSync(process.cwd()+'/tools/home/renovation-budget.html','utf8');var i1=h1.indexOf('function updateItem(');var sg=i1>=0?h1.slice(i1,i1+1200):'';var okg=sg.indexOf('isFinite(num)')>=0&&sg.indexOf('num < 0')>=0&&sg.indexOf('totalEl.innerHTML')>=0&&h1.indexOf('data-id=')>=0;var h2=hh.readFileSync(process.cwd()+'/tools/hotel/tip-calculator.html','utf8');var i2=h2.indexOf('function tipRead()');var sg2=i2>=0?h2.slice(i2,i2+3000):'';var okt=sg2.indexOf('taxAmount')>=0&&sg2.indexOf('mode==='+String.fromCharCode(39)+'inclusive'+String.fromCharCode(39)+' ? bill + tip : bill + taxAmount + tip')>=0&&sg2.indexOf('taxAmount = bill*tax/100')>=0&&sg2.indexOf('tax>0')>=0;document.getElementById('__tbProbe').textContent='RENITEM '+(okg?'OK':'BAD')+' TIPTAX '+(okt?'OK':'BAD');})();"],
  "expect": ["RENITEM OK TIPTAX OK"],
  "ref": "第1306批双源码形态强锚(承载页 home/renovation-budget)：①装修明细 updateItem 校验数值并定点刷该行 .total、行带 data-id；旧版空串入总计且只 calc 不刷行 ⇒ BAD。②tip-calculator tipRead 须区分含税/未含税总额（含税 bill+tip、未含税 bill+taxAmount+tip）并拦截负税率；旧版漏税 ⇒ BAD。真机交互由复核方覆盖。"
},
{
  "slug": "home/water-filter-lifespan",
  "inputs": { "cap": "5000", "daily": "10", "margin": "85", "price": "150" },
  "clicks": ["try{calcTool()}catch(e){};var t=String(document.getElementById('result').innerHTML);var ok=['3613 L','361 天','1.01 支/年','152 元/年','0.0415 元/L'].every(function(x){return t.indexOf(x)>=0;});document.getElementById('__tbProbe').textContent='WALL '+(ok?'OK':'BAD');"],
  "expect": ["WALL OK"],
  "ref": "非默认算例：有效 5000×0.85×0.85≈3613 L；3613/10≈361 天；365/361≈1.01 支/年；150×1.01≈152 元/年；150/3613≈0.0415 元/L。组合探针要求五项全部命中，避免 expect 任一命中即通过的弱断言；默认 4000/8/90/120 不命中。"
},
{
  "slug": "home/water-filter-lifespan",
  "inputs": { "cap": "" },
  "expect": ["请填写滤芯额定净水量、每日净水用量、安全余量与滤芯单价（单价可为 0）后再计算。"],
  "ref": "清空额定净水量必须出明确空态提示，不得把空串当 0 后显示大于 0 提示或静默给结论。"
},
{
  "slug": "home/water-filter-lifespan",
  "inputs": { "margin": "" },
  "expect": ["请填写滤芯额定净水量、每日净水用量、安全余量与滤芯单价（单价可为 0）后再计算。"],
  "ref": "清空安全余量同样走必填提示，避免误报「需在 50%–100% 之间」。"
},
{
  "slug": "home/ac-energy-cost",
  "inputs": { "power": "1200", "hours": "6", "days": "25", "months": "3", "price": "0.8", "standby": "3", "standbyHours": "18" },
  "clicks": ["try{calcTool()}catch(e){};var t=String(document.getElementById('result').innerHTML);var ok=['7.25 kWh','181.3 kWh','544.0 kWh','¥5.80','¥145.08','¥435.24','316 kg'].every(function(x){return t.indexOf(x)>=0;});document.getElementById('__tbProbe').textContent='ACALL '+(ok?'OK':'BAD');"],
  "expect": ["ACALL OK"],
  "ref": "非默认算例：1200 W×6 h+3 W×18 h=7.254 kWh；月 181.35→181.3 kWh；季 544.05→544.0 kWh；日电费 5.8032→5.80 元；月 145.08 元；季 435.24 元；CO₂ 544.05×0.58=315.55→316 kg。组合探针要求七项全部命中；默认 1100/8/30/4/0.6 不命中。"
},
{
  "slug": "home/ac-energy-cost",
  "inputs": { "power": "", "hours": "8" },
  "expect": ["请填写额定功率、每日运行小时、使用天数、电价与待机参数后再计算。"],
  "ref": "清空额定功率必须出明确必填提示，不得把空串当 0 后显示「需大于 0 W」或静默给结论。"
},
{
  "slug": "home/ac-energy-cost",
  "inputs": { "power": "0" },
  "expect": ["额定功率需大于 0 W。"],
  "ref": "显式 0 W 非法，必须提示；与空串提示区分。"
},
{
  "slug": "home/ac-energy-cost",
  "inputs": { "power": "1000", "price": "0" },
  "expect": ["¥0.00"],
  "ref": "电价 0 是合法输入（自发电/赠电场景），不得被空态守卫拦死，日电费应显示 0.00 元。"
},
{
  "slug": "home/ac-energy-cost",
  "inputs": { "hours": "20", "standbyHours": "10" },
  "expect": ["每日运行小时与待机小时合计超过 24 小时，请核对，避免重复计算。"],
  "ref": "交叉校验：运行 20 h + 待机 10 h = 30 h，超过一天，必须提示核对；不能默默把 30 小时都计入。"
},
{
  "slug": "home/water-filter-lifespan",
  "inputs": { "cap": "4000", "daily": "8", "margin": "90", "price": "120", "start": "2026-01-01" },
  "clicks": [
    "calcTool();var c=document.getElementById('lifeChart');var ok1=c.style.display!=='none'&&String(document.getElementById('result').innerHTML).indexOf('L')>=0;document.getElementById('start').value='';calcTool();var ok2=c.style.display==='none'&&String(document.getElementById('result').innerHTML).indexOf('请填写开始使用日期后再计算。')>=0;document.getElementById('start').value='2026-02-01';calcTool();var ok3=c.style.display!=='none'&&String(document.getElementById('result').innerHTML).indexOf('预计更换日期')>=0;document.getElementById('__tbProbe').textContent='WLCHART '+(ok1&&ok2&&ok3?'OK':'BAD '+c.style.display);"
  ],
  "expect": ["WLCHART OK"],
  "ref": "第531批：先有效计算显示图表，再清空日期计算必须隐藏并清除旧图，最后恢复日期再次显示。旧实现只替换 result 后 return，画布保留上次「预计可用天数/年换芯」柱状数据。"
},
{
  "slug": "home/ac-energy-cost",
  "inputs": { "power": "1000", "hours": "8", "days": "30", "months": "4", "price": "-1", "standby": "2", "standbyHours": "16" },
  "expect": ["电价不能为负（可为 0）。"],
  "ref": "第524批：负电价必须拒绝，不能靠 HTML min 属性；错误提示要明确 0 仍合法。"
},
{
  "slug": "home/ac-energy-cost",
  "inputs": { "power": "1000", "hours": "8", "days": "100", "months": "4", "price": "0.6", "standby": "2", "standbyHours": "16" },
  "expect": ["每月使用天数需为 1–31 的整数。"],
  "ref": "第524批：每月 100 天越界必须拒绝；计算与导出共用 inputError，避免只靠 max=31。"
},
{
  "slug": "home/water-filter-lifespan",
  "inputs": { "start": "" },
  "expect": ["请填写开始使用日期后再计算。"],
  "ref": "清空开始使用日期必须提示，不得静默回退今天导致预计更换日期与用户输入不一致。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "storage", "people": "3", "sim": "1", "minutes": "10", "flow": "8", "cold": "15", "target": "70", "tank": "60", "power": "2", "price": "0.6" },
  "expect": ["储水温度需不低于目标水温（当前 60°C，目标 70°C）。"],
  "ref": "第537批：储水温度 60°C 低于目标 70°C 时不得把 hotFraction 截为 1 后给推荐，必须提示不可达。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "storage", "people": "3", "sim": "3", "minutes": "20", "flow": "8", "cold": "15", "target": "40", "tank": "60", "power": "2", "price": "0.6" },
  "expect": ["超出可选规格上限 200 L"],
  "ref": "第537批：3 人同时洗 20 分钟、8 L/min ⇒ 估算储水容量远超 200 L 上限，nextSize 旧实现仍返回 200 L；修复后必须提示无可用规格。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "gas", "people": "4", "sim": "3", "minutes": "10", "flow": "10", "cold": "10", "target": "35", "tank": "60", "power": "2", "price": "0.6" },
  "expect": ["超出规格表上限 24 L/min"],
  "ref": "第537批：3 路同时 10 L/min、温升 25°C ⇒ 需 30 L/min，超过燃气规格表 24 L/min 上限；旧实现仍推荐 24 L/min。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "instant", "people": "3", "sim": "2", "minutes": "10", "flow": "10", "cold": "15", "target": "40", "tank": "60", "power": "2", "price": "0.6" },
  "expect": ["超出规格表上限（24 kW / 100 A）"],
  "ref": "第537批：2 路同时 10 L/min、温升 25°C ⇒ 34.9 kW，超过即热规格表 24 kW 与空开 100 A 上限；旧实现返回 24 kW/100 A 并给出不足推荐。"
},
{
  "slug": "home/appliance-lifespan",
  "inputs": { "type": "fridge", "start": "2099-01-01", "price": "3000" },
  "clicks": ["var oa=alert,msg='';alert=function(m){msg=String(m);};try{exportCSV();}catch(e){}alert=oa;document.getElementById('__tbProbe').textContent='AEXP '+(msg==='首次使用日期不能晚于今天。'?'OK':'BAD '+msg);"],
  "expect": ["AEXP OK"],
  "ref": "第533批：未来首次使用日期在页面计算被拒，导出也必须共用 inputError 拒绝，不能生成 CSV。"
},
{
  "slug": "home/appliance-lifespan",
  "inputs": { "type": "fridge", "start": "2020-01-01", "price": "3000" },
  "clicks": ["var oa=alert,msg='';alert=function(m){msg=String(m);};try{exportCSV();}catch(e){}alert=oa;document.getElementById('__tbProbe').textContent='AEXOK '+(msg===''?'OK':'BAD '+msg);"],
  "expect": ["AEXOK OK"],
  "ref": "合法日期必须可正常导出，不得被新增日期校验误伤；日期 2020-01-01 早于今天。"
},
{
  "slug": "home/repair-or-replace",
  "inputs": { "type": "fridge", "age": "6", "repair": "-100", "newPrice": "3000", "newLife": "10", "repairLife": "4", "risk": "none" },
  "clicks": ["var oa=alert,msg='';alert=function(m){msg=String(m);};try{exportCSV();}catch(e){}alert=oa;document.getElementById('__tbProbe').textContent='REXP '+(msg.indexOf('维修报价不能为负')>=0?'OK':'BAD '+msg);"],
  "expect": ["REXP OK"],
  "ref": "第535批：负维修报价在页面计算被拒，导出也必须共用 inputError 拒绝，不能写出负成本 CSV。"
},
{
  "slug": "home/appliance-lifespan",
  "inputs": { "type": "fridge", "start": "2020-01-01", "price": "3000" },
  "expect": ["2030-01-01", "¥300 元/年", "安全期内"],
  "ref": "固定首次使用日 2020-01-01、冰箱参考 10 年 ⇒ 建议更换日期恒为 2030-01-01；购买价 3000/10=300 元/年；2026 年当前仍在安全期。三条同时命中，能区分年限表错误、日期加年错误或年均成本算法错误。"
},
{
  "slug": "home/appliance-lifespan",
  "inputs": { "type": "washer", "start": "2010-01-01", "price": "2500" },
  "expect": ["已超安全年限", "已超"],
  "ref": "洗衣机参考 8 年，2010 年首次使用到 2026 年已 16 年以上，必须判「已超安全年限」并显示超出年数；默认冰箱安全期不会命中。"
},
{
  "slug": "home/appliance-lifespan",
  "inputs": { "type": "washer", "start": "" },
  "expect": ["请选择家电类型并填写首次使用日期后再计算。"],
  "ref": "清空首次使用日期必须出明确空态提示，不得静默按今天起算并给出更换日期。"
},
{
  "slug": "home/appliance-lifespan",
  "inputs": { "start": "2035-01-01" },
  "expect": ["首次使用日期不能晚于今天。"],
  "ref": "未来日期非法，必须提示；不得把未来日期算成负已用年限或 0 后照常给安全期结论。"
},
{
  "slug": "home/appliance-lifespan",
  "inputs": { "type": "fan", "start": "2018-01-01", "price": "0" },
  "expect": ["¥0 元/年", "2028-01-01"],
  "ref": "购买价 0 是合法输入（赠品/自装），不得被空态守卫拦死；电风扇参考 10 年，2018 首次使用 ⇒ 更换日期 2028-01-01，年均成本显示 ¥0/年。"
},
{
  "slug": "home/repair-or-replace",
  "inputs": { "type": "fridge", "age": "6", "repair": "600", "newPrice": "4000", "newLife": "10", "repairLife": "4", "saving": "0", "risk": "none" },
  "expect": ["¥150 元/年", "¥400 元/年", "维修更划算"],
  "ref": "冰箱剩 4 年、维修 600/4=150 元/年；新机 4000/10=400 元/年，维修更划算。注入新机价 4000 与默认 3000 不同，避免默认态命中。"
},
{
  "slug": "home/repair-or-replace",
  "inputs": { "type": "fridge", "age": "6", "repair": "1600", "newPrice": "3000", "newLife": "10", "repairLife": "2", "saving": "0", "risk": "none" },
  "expect": ["¥800 元/年", "优先换新"],
  "ref": "维修 1600 只能用 2 年 ⇒ 800 元/年，高于新机 300 元/年，必须判优先换新。"
},
{
  "slug": "home/repair-or-replace",
  "inputs": { "type": "waterHeater", "age": "9", "repair": "400", "newPrice": "1200", "newLife": "8", "repairLife": "2", "saving": "0", "risk": "sometimes" },
  "expect": ["优先换新", "安全优先"],
  "ref": "储水式热水器参考 8 年、已用 9 年且有偶发故障 ⇒ 安全优先，必须换新；不能只因维修 200 元/年低于新机 150 元/年就判维修。"
},
{
  "slug": "home/repair-or-replace",
  "inputs": { "type": "washer", "age": "" },
  "expect": ["请填写家电类型、已用年限、维修报价、新机价格、新机寿命与维修后可用年限后再计算。"],
  "ref": "清空已用年限必须提示，不得把空串当 0 后继续给出维修建议。"
},
{
  "slug": "home/repair-or-replace",
  "inputs": { "type": "fan", "age": "5", "repair": "0", "newPrice": "1000", "newLife": "10", "repairLife": "5", "saving": "0", "risk": "none" },
  "expect": ["¥0 元/年", "维修更划算"],
  "ref": "维修报价 0 是合法输入（保修内/免费维修），不得被空态守卫拦死；0 元维修必须判维修更划算。"
},
{
  "slug": "home/repair-or-replace",
  "inputs": { "type": "microwave", "age": "8", "repair": "-100" },
  "expect": ["已用年限与维修报价不能为负；新机价格、新机寿命与维修后可用年限需大于 0。"],
  "ref": "负维修报价非法，必须提示；不能按负成本算出维修永远更划算。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "storage", "people": "4", "sim": "1", "minutes": "10", "flow": "8", "cold": "15", "target": "40", "tank": "60", "power": "2", "price": "0.6" },
  "expect": ["80 L", "44 L", "60 L", "94 分钟", "11.6 kWh", "¥7.0 元/天"],
  "ref": "4 人、1 人同时洗、10 分钟、8 L/min：混合 80 L，60°C 热水 80×(25/45)=44.4→44 L，储水 44.4/0.8=55.6→60 L；60 L×4.186×45/2 kW/60=94.2→94 分钟；4 人日能耗 11.6 kWh、电费 11.6×0.6=7.0 元。人数 4 与默认 3 不同，避开默认态。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "storage", "people": "3", "sim": "2", "minutes": "10", "flow": "8", "cold": "15", "target": "40", "tank": "60", "power": "2", "price": "0.6" },
  "expect": ["160 L", "89 L", "120 L", "188 分钟"],
  "ref": "两人同时洗：混合 160 L，热水 88.9→89 L，储水需求 111.1→120 L；整罐加热 120×4.186×45/2/60=188.4→188 分钟。同时洗澡人数 2 与默认 1 不同，能区分漏乘同时人数。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "gas", "people": "4", "sim": "2", "minutes": "10", "flow": "9", "cold": "10", "target": "40", "tank": "60", "power": "2", "price": "0.6" },
  "expect": ["180 L", "108 L", "10.8 L/min", "24 L/min"],
  "ref": "燃气：2 人同时、9 L/min、温升 30°C ⇒ 单淋浴额定 9×30/25=10.8 L/min，合计 21.6→24 L/min；混合 180 L、60°C 热水 108 L。类型与默认不同，能区分按 25°C 标定与漏乘同时人数。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "instant", "people": "1", "sim": "1", "minutes": "8", "flow": "7", "cold": "18", "target": "40", "tank": "60", "power": "8", "price": "0.6" },
  "expect": ["10.7 kW", "12 kW", "63 A"],
  "ref": "即热：7 L/min、温升 22°C ⇒ 7×4.186×22/60=10.74→10.7 kW，下一档 12 kW；电流 48.8 A×1.25=61.0→63 A 空开。类型与默认不同，能区分功率漏乘温升或空开未留余量。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "gas", "people": "" },
  "expect": ["请填写家庭人数、淋浴参数与热水器设置后再计算。"],
  "ref": "清空家庭人数必须提示，不得把空串当 0 后继续给容量建议。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "instant", "people": "1", "cold": "20", "target": "15" },
  "expect": ["目标水温需高于进水温度"],
  "ref": "目标水温低于进水温度属非法，必须提示；不得用负温升算出负功率或无效结果。"
},
{
  "slug": "home/renovation-budget",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/home/renovation-budget.html','utf8');var i=h.indexOf('function updateItem');var seg=i>=0?h.slice(i,i+700):'';var ok=seg.indexOf('inp.value = it[field]')>=0&&seg.indexOf('已恢复上次有效值')>=0&&h.indexOf('data-field')>=0&&h.indexOf('onchange')>=0;document.getElementById('__tbProbe').textContent='RENOV '+(ok?'OK':'BAD');"],
  "expect": ["RENOV OK"],
  "ref": "第1306批·非法价量显示与存储分裂修复：价/量改为 change 提交，空值/负数/非数时恢复控件上次有效值并提示；旧版直接 return，控件显示空/负而小计总额仍用旧值 ⇒ BAD。真机清空单价恢复 100，负数量恢复 2。"
},
{
  "slug": "home/water-filter-lifespan",
  "inputs": { "cap": "4000", "daily": "8", "margin": "40", "price": "120" },
  "clicks": ["var oa=alert,msg='';alert=function(m){msg=String(m);};try{exportCSV();}catch(e){}alert=oa;document.getElementById('__tbProbe').textContent='WEXP '+(msg.indexOf('50%')>=0&&msg.indexOf('100%')>=0?'OK':'BAD')+' '+msg;"],
  "expect": ["WEXP OK"],
  "ref": "第522批：安全余量 40% 时计算已拒绝，导出必须走同一校验、不得输出 40% 的换芯日期与成本；旧版 exportCSV 只查容量/日用量 ⇒ BAD。"
},
{
  "slug": "home/water-filter-lifespan",
  "inputs": { "cap": "4000", "daily": "8", "margin": "90", "price": "-5" },
  "clicks": ["var oa=alert,msg='';alert=function(m){msg=String(m);};try{exportCSV();}catch(e){}alert=oa;document.getElementById('__tbProbe').textContent='WNEG '+(msg.indexOf('负数')>=0?'OK':'BAD')+' '+msg;"],
  "expect": ["WNEG OK"],
  "ref": "第522批：滤芯单价为负时计算与导出都必须拒绝，不得输出负成本；旧版导出无价格校验 ⇒ BAD。"
},
{
  "slug": "home/water-filter-lifespan",
  "inputs": { "cap": "4000", "daily": "8", "margin": "90", "price": "0" },
  "clicks": ["try{calcTool()}catch(e){};var t=String(document.getElementById('result').innerHTML);var oa=alert,msg='';alert=function(m){msg=String(m);};try{exportCSV();}catch(e){}alert=oa;var ok=t.indexOf('0 元/年')>=0&&t.indexOf('0.0000 元/L')>=0&&msg==='';document.getElementById('__tbProbe').textContent='WZERO '+(ok?'OK':'BAD');"],
  "expect": ["WZERO OK"],
  "ref": "第522批：单价 0 是合法输入（赠品/免费滤芯），必须正常算出 0 元/年、0.0000 元/L，且导出不报错；把 0 当空值会误拦 ⇒ BAD。"
},
{
  "slug": "home/water-filter-lifespan",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/home/water-filter-lifespan.html','utf8');var parts=h.split('<script');var fb='';for(var k=1;k<parts.length;k++){var seg=parts[k].split('</script>')[0];if(seg.indexOf('FAQPage')>=0){fb=seg.slice(seg.indexOf('{'),seg.lastIndexOf('}')+1);break;}}var q=null;try{q=JSON.parse(fb);}catch(e){}var n=q&&q.mainEntity?q.mainEntity.length:0;var ro=q&&q.mainEntity&&q.mainEntity.some(function(x){return x.name==='RO 膜也要按这个算吗？'&&x.acceptedAnswer&&x.acceptedAnswer.text.indexOf('TDS')>=0&&x.acceptedAnswer.text.indexOf('安全余量设多少')<0;});var dd=h.split('<dt').length-1;var de=h.split('<dd').length-1;var di=h.indexOf('name=\"desc-en\"');var ds=di>=0?h.indexOf('content=\"',di)+9:-1;var deTxt=ds>=0?h.slice(ds,h.indexOf('\"',ds)):'';var trunc=['cartr','water','qualit'].some(function(w){return deTxt.slice(-w.length)===w;});var ok=n===4&&ro&&dd===4&&de===4&&deTxt.length<=160&&trunc===false;document.getElementById('__tbProbe').textContent='WFAQ '+(ok?'OK':'BAD')+' n='+n+' ro='+ro+' dt/dd='+dd+'/'+de+' en='+deTxt.length;"],
  "expect": ["WFAQ OK"],
  "ref": "第433批：可见 4 组 dt/dd 问答，FAQPage mainEntity 必须同为 4 项，RO 膜问答独立成项且答案不含上一题；第522批：desc-en 不得在 cartr 等词中间截断。旧版 3 项并把 RO 问答并入上一题、desc-en 截到 cartr ⇒ BAD。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "gas", "people": "4", "sim": "2", "minutes": "10", "flow": "9", "cold": "10", "target": "40", "tank": "", "power": "", "price": "" },
  "expect": ["180 L", "10.8 L/min", "24 L/min"],
  "ref": "燃气模式不依赖储水温度/加热功率/电价：三项留空仍应给出混合水量、温升25°C流量与建议升数，结果不得出现储水热水量或电费。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "instant", "people": "1", "sim": "1", "minutes": "8", "flow": "7", "cold": "18", "target": "40", "tank": "", "power": "8", "price": "0.6" },
  "expect": ["10.7 kW", "12 kW", "63 A"],
  "ref": "即热模式不依赖储水温度：tank 留空仍应给出持续功率、建议功率与空开，不得因无关字段留空阻断计算。"
},
{
  "slug": "home/water-heater-sizing",
  "inputs": { "type": "storage", "people": "1.5", "sim": "1", "minutes": "10", "flow": "8", "cold": "15", "target": "40", "tank": "60", "power": "2", "price": "0.6" },
  "expect": ["家庭人数与同时洗澡人数必须是正整数"],
  "ref": "step=1 不阻止脚本计算：1.5 人必须提示为正整数，不得按 1.5 人估算日需求。"
},
{
  "slug": "home/repair-or-replace",
  "inputs": { "type": "fridge", "age": "10", "repair": "200", "newPrice": "3000", "newLife": "10", "repairLife": "2", "saving": "0", "risk": "none" },
  "expect": ["0（先检查）", "不适用", "参考安全年限已用完", "先专业检查"],
  "ref": "冰箱参考 10 年、已用 10 年 ⇒ 剩余 0 年：维修后年限取 0，维修年均成本与差额不适用，必须给专业检查结论；旧实现绕开封顶按 2 年算出 100 元/年并判维修更划算。"
},
{
  "slug": "home/water-filter-lifespan",
  "clicks": ["document.getElementById('price').value='';calcTool();var t=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='WBLANK '+(t.indexOf('滤芯单价（单价可为 0）')>=0&&t.indexOf('元/年')<0?'OK':'BAD');"],
  "expect": ["WBLANK OK"],
  "ref": "单价空串不得被 num() 当 0 后显示免费滤芯：必须提示补填；显式 0 仍合法（另有用例覆盖）。"
},
{
  "slug": "home/water-filter-lifespan",
  "clicks": ["document.getElementById('price').value='0';calcTool();var t=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent='WZ2 '+(t.indexOf('0 元/年')>=0&&t.indexOf('0.0000 元/L')>=0?'OK':'BAD '+t);"],
  "expect": ["WZ2 OK"],
  "ref": "显式 0 是合法的免费/赠品滤芯价格，必须正常算出零成本，不得被空态守卫误伤。"
},
{
  "slug": "home/renovation-budget",
  "clicks": ["try{localStorage.setItem('home_budget_items',JSON.stringify([{id:1,name:'旧草稿',price:100,qty:1}]));}catch(e){}var o=window.confirm;window.confirm=function(){return true;};applyBudgetPreset('basic');window.confirm=o;var b=document.getElementById('undoPresetBtn');var ok=b&&!b.disabled&&getItems().length>1;restoreSnapshot();var back=getItems().length===1&&getItems()[0].name==='旧草稿';document.getElementById('__tbProbe').textContent='RENUNDO '+(ok&&back?'OK':'BAD ok='+ok+' back='+back);"],
  "expect": ["RENUNDO OK"],
  "ref": "预设覆盖必须确认并保留撤销快照：确认覆盖后撤销按钮可用，restoreSnapshot 能恢复覆盖前唯一旧草稿；旧 applyBudgetPreset 直接覆盖且无撤销。"
},
{
  "slug": "home/renovation-budget",
  "clicks": ["try{localStorage.setItem('home_budget_items',JSON.stringify([{id:1,name:'保留我',price:100,qty:1}]));}catch(e){}var o=window.confirm;window.confirm=function(){return false;};applyBudgetPreset('basic');window.confirm=o;var kept=getItems().length===1&&getItems()[0].name==='保留我';document.getElementById('__tbProbe').textContent='RENCANCEL '+(kept?'OK':'BAD');"],
  "expect": ["RENCANCEL OK"],
  "ref": "预设覆盖点取消时必须保留原草稿，不得写入模板。"
},
{
  "slug": "home/renovation-budget",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/home/renovation-budget.html','utf8');var ok=h.indexOf('<button type=\"button\" class=\"del\" aria-label=\"删除')>=0&&h.indexOf('undoPresetBtn')>=0&&h.indexOf('本工具不设预算上限')>=0&&h.indexOf('能设预算上限、跟踪实际支出吗？')>=0;document.getElementById('__tbProbe').textContent='RENA11Y '+(ok?'OK':'BAD');"],
  "expect": ["RENA11Y OK"],
  "ref": "删除控件须为带项目名 aria-label 的真实 button；文案统一声明不设预算上限、不跟踪实际支出，并保留撤销入口。"
},
{
  "slug": "home/washer-capacity",
  "inputs": {"people": "4"},
  "expect": ["8–9 kg", "81 L"],
  "ref": "第867批：4 人按对照表推荐 8–9 kg，用水按上限 9 kg × 滚筒 9L/kg = 81L；旧实现 4×2.5=10kg 与 FAQ 8–9kg 冲突。"
},
{
  "slug": "home/washer-capacity",
  "inputs": {"people": "2.5"},
  "expect": ["家庭人口必须为正整数"],
  "ref": "第867批：小数人数不再被 Math.floor 静默取整，明确提示必须为正整数。"
},
{
  "slug": "home/furniture-layout",
  "clicks": ["document.getElementById('rl').value='1';document.getElementById('rw').value='1';addFurniture('床(双人)');__flClamp();var m=__flMetrics();document.getElementById('__tbProbe').textContent='FLMET '+m.overlap.toFixed(2)+'|'+m.outside.toFixed(2);"],
  "expect": ["FLMET 0.00|2.60"],
  "ref": "第867批：1×1m 房间放 1.8×2m 床，旧算法把房外 2.60m² 算成重叠；现房内重叠 0.00、越界 2.60。"
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

  console.log("==== home calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();

