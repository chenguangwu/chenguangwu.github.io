#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
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
    "13.00",
    "1200"
  ],
  "ref": "原 all_default 弱用例（coats=2/coverage=10/bucket-size=5/bucket-price=280 全等于默认）+ expect「客厅墙面」来自 localStorage 缺失时的常量兜底清单（30+22 两间房 ⇒ 总面积恒 52.0，与输入无关）。本页 getItem 桩恒 null、兜底 JSON 为常量，可注入的只有 4 个数值参数。改为 coats=3/coverage=12/bucket-size=4/bucket-price=300：总用量 52×3/12=13.00 L、桶数 ceil(13/4)=4、成本 4×300=1200。默认态 52×2/10=10.40 L、3 桶、840 元"
},
{
  "slug": "home/renovation-budget",
  "clicks": [
    "localStorage.getItem=function(){return JSON.stringify([{id:1,name:'瓷砖',price:8000,qty:12},{id:2,name:'地板',price:6000,qty:10}]);};renderItems();calc()"
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
  "slug": "home/washer-capacity",
  "inputs": {
    "people": "6"
  },
  "expect": [
    "90"
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
  console.log("==== home calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
