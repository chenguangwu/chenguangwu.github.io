#!/usr/bin node
"use strict";
const fs = require("fs");
const { runCase } = require("./verify_it_calc.js");
globalThis.__tbFs = fs;
const CASES = [
{
  "slug": "gardening/balcony-sunlight",
  "inputs": { "dir": "north", "floor": "high", "season": "winter" },
  "expect": [
    "0.5 小时 每日直射光照（北向·冬）"
  ],
  "ref": "补齐静态 option 后可直接注入：北向冬季基准 0h + 高层 +0.5h ⇒ 0.5h（默认 南向·中层·春 = 6+0=6.0h）；光照类型降为耐阴、推荐植物换为耐阴清单。非默认输入 + 独立复算。"
},
{
  "slug": "gardening/balcony-sunlight",
  "inputs": { "dir": "west", "floor": "low", "season": "summer" },
  "expect": [
    "5.0 小时 每日直射光照（西向·夏）"
  ],
  "ref": "西向夏季基准 6h − 低层遮挡 1h = 5h ⇒ 5.0h，落入 4≤h<6 的「半日照」档（默认态 6.0h 为全日照，不含 5.0/半日照）。"
},
{
  "slug": "gardening/pot-capacity",
  "clicks": ["currentShape='frustum';renderInputs();document.getElementById('top').value=24;document.getElementById('bottom').value=18;document.getElementById('height').value=20;calc();var h=document.getElementById('result').innerHTML;document.getElementById('__tbProbe').textContent=(h.indexOf('6974 cm³')>=0?'T1':'T0')+(h.indexOf('6001 cm³')>=0?'U1':'U0')+(h.indexOf('圆台盆')>=0?'N1':'N0')"],
  "expect": ["T1U1N1"],
  "ref": "圆台盆（679 新增）：上口 24 / 下底 18 / 高 20 → R=12、r=9，V=π×20/3×(144+108+81)=π×2220=**6974 cm³**；排水层 2cm 按收口切片 526 cm³、顶部留空 1cm 447 cm³ ⇒ 可用 **6001 cm³**、土 7.20 kg。修复前无圆台形状，只能按圆柱 Φ24 算 9048 cm³、高估约 30%。"
},
{
  "slug": "gardening/pot-capacity",
  "inputs": {"diameter":"20","height":"5"},
  "expect": ["942 cm³", "陶粒 1cm"],
  "ref": "浅盆排水层分档（679，N209）：内径 20、内高 5cm → 盆高 <8cm 取 1cm 排水层，总 1570.8 − 排水 314.2 − 顶空 314.2 = **942 cm³**，结果卡显示「陶粒 1cm」；修复前固定 2cm 仅 628 cm³。"
},
{
  "slug": "gardening/pot-capacity",
  "inputs": {"diameter":"20","height":"2"},
  "expect": ["盆高过小"],
  "ref": "浅盆高度下限（679，N208）：内径 20、内高 2cm → 排水 1 + 顶空 1 = 2cm，无有效容积，页面提示「盆高过小」并停算；修复前按 2cm 排水算出负土壤体积（−0.16 L）。"
},
{
  "slug": "gardening/compost-calculator",
  "inputs": {},
  "clicks": ["materials[0].idx=12;materials[0].weight=4;materials[1].idx=4;materials[1].weight=2;calc()"],
  "expect": [
    "12.4:1 混合 C:N 比",
    "鸡粪 10:1 4.00 4.00 0.4000 57.1%"
  ],
  "ref": "原料行的 <select>/<input> 由 renderMaterialList() 拼 innerHTML 生成（无静态 id ⇒ clicks 直接改顶层 materials 再 calc()）：鸡粪(10:1)4kg 氮代理 4/10=0.4000、咖啡渣(20:1)2kg=0.1000、蔬菜废料(15:1)1kg=0.0667 ⇒ 总重 7.00、总氮 0.5667 ⇒ C:N=7/0.5667=12.35→12.4:1，鸡粪占比 4/7=57.1%（默认 落叶2/草坪1/蔬菜1 = 26.7:1）。非默认输入+独立复算。"
},
{
  "slug": "gardening/garden-calendar",
  "clicks": [
    "setMonth(12)"
  ],
  "expect": [
    "12月 园艺工作 · 北方 共 3 项工作"
  ],
  "ref": "去默认化（原 expect「10月」＝默认当月态，注入失败仍命中 → 逃生项）：clicks 调 setMonth(12)（无 this 依赖），render() 输出 12 月北方园艺「12月 园艺工作 · 北方 共 3 项工作 修剪 冬季修剪...」；默认九月显示「9月 ...」不含「12月 ... 北方」，注入失败即不命中。（注：setZone('south') 触发 buildMonthText 在南方分区有未定义项报错，故只切月份、走默认北方分区。）"
},
{
  "slug": "gardening/garden-layout",
  "inputs": {
    "area": "30"
  },
  "expect": [
    "3265"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/garden-tools",
  "inputs": {
    "searchInput": "zzz"
  },
  "expect": [
    "未找到匹配的工具，请调整筛选条件"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部工具，不产此串）"
},
{
  "slug": "gardening/pest-identifier",
  "inputs": {
    "searchInput": "zzz"
  },
  "expect": [
    "未找到匹配的病虫害，请调整筛选条件"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部病虫害，不产此串）"
},
{
  "slug": "gardening/plant-calendar",
  "inputs": {},
  "clicks": [
    "toggleCat('leaf');"
  ],
  "expect": [
    "（筛选 8 种）"
  ],
  "ref": "clicks 注入：toggleCat('leaf') 把叶菜加入 currentCats，renderView → renderMonthView 仅在过滤集非空时拼出派生串「（筛选 N 种）」，N = 该分类蔬菜数；离线独立复算 VEGGIES 中 cat='leaf' 共 8 种（leaf 8 / melon 6 / fruit 5 / root 5 / allium 3 / bean 3 / other 1，合计 31）⇒ 锚取值 8。旧锚「11-12月」是番茄收获期的静态字段字面量 ⇒ 判别力 0。注意该页 currentMonth 取 new Date()（会渲染「📍 九月 (本月)」这类随日期漂移的串），但「（筛选 8 种）」与日期无关 ⇒ 跨天稳定。清 clicks 后过滤集为空、该串不渲染 ⇒ 零逃生项。"
},
{
  "slug": "gardening/plant-calendar",
  "clicks": [
    "showMonthView=true;renderView();var h=String(document.getElementById('view').innerHTML);var i=h.indexOf('三月'),j=h.indexOf('四月',i+1);var seg=i>=0?h.slice(i,j>0?j:i+1600):'';var names=['黄瓜','萝卜','白菜','生菜','韭菜','葱','西瓜','南瓜','冬瓜','苦瓜','丝瓜','茼蒿'];document.getElementById('__tbProbe').textContent='M182 '+names.map(function(n){return seg.indexOf('>'+n+'<')>=0?'1':'0';}).join('')"
  ],
  "expect": ["M182 111111111111"],
  "ref": "12-N182 月份区间未展开：旧实现 renderMonthView 用 v.seed.includes('3月') 字面子串匹配，区间开头的「3-4月 / 8月」不含连续「3月」，导致三月漏 12 种（黄瓜/萝卜/白菜/生菜/韭菜/葱/西瓜/南瓜/冬瓜/苦瓜/丝瓜/茼蒿），同时「1月」误命中「11-12月」的 11 月。修复后 __monthsOf 展开 a-b月 与「常年」为月集合，三月播种应有 21 种。本用例取 12 个旧版必漏品种，逐个检查是否落在三月卡片 <span> 内；旧版全漏得 000000000000 ⇒ 红，修复版全中 ⇒ 绿。定位用汉字「三月/四月」h4 边界，与 new Date() 当前月无关 ⇒ 跨天稳定；探针串只在 clicks 注入后出现 ⇒ 零逃生。"
},
{
  "slug": "gardening/plant-calendar",
  "clicks": [
    "toggleSeason('spring');showMonthView=true;renderView();var h=String(document.getElementById('view').innerHTML);var m=h.match(/（筛选 (\\d+) 种）/);document.getElementById('__tbProbe').textContent='N183 '+(m?m[1]:'NA')"
  ],
  "expect": ["N183 31"],
  "ref": "12-N183 季节筛选同源于区间未展开：旧 getFiltered 用 v.seed.includes('3月')，春季 3/4/5 月实际 25 种，漏 生菜(3-9月)/大蒜·洋葱(收获5-6月)/毛豆(4-6月)/苋菜(4-6月)/空心菜(4-7月)，应为 31 种。修复后与 N182 共用 __monthsOf 做月份集合交集。探针只在 toggleSeason 注入后出现（默认无筛选不渲染「（筛选 N 种）」）⇒ 零逃生；旧版得 25 红、修复版 31 绿。"
},
{
  "slug": "gardening/plant-care",
  "inputs": {
    "searchInput": "zzz"
  },
  "expect": [
    "未找到匹配的植物，请调整筛选条件"
  ],
  "ref": "auto-restore（去默认化：注入无匹配关键词 zzz → 过滤结果为空；回退空词则列出全部植物，不产此串）"
},
{
  "slug": "gardening/pot-capacity",
  "inputs": {
    "${f.id}": "${f.value}_X"
  },
  "expect": [
    "_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/recommender",
  "inputs": {
    "cnt": "12"
  },
  "clicks": ["var __r=Math.random;Math.random=function(){return 0.1;};gen();Math.random=__r"],
  "expect": [
    "12. 吊兰 | 春季·晴天·疏松透气 → 建议每3-5天1次，保持土壤微润，避免积水"
  ],
  "ref": "纯随机页：clicks 内钉死 Math.random=0.1 并**用完即恢复**（进程级全局，不恢复会污染后续用例默认态）。"
     + "PLANTS/SEASONS/WEATHERS/SOILS 长度分别为 12/4/4/4 ⇒ floor(0.1×len) 依次取索引 1/0/0/0"
     + "=吊兰/春季/晴天/疏松透气；freq 判 weather=晴天 ⇒ 每3-5天1次；tips 判 plant=吊兰 ⇒ 保持土壤微润，避免积水。"
     + "cnt=12 ⇒ 末条编号为 12.，默认态（5 条）不可能出现。原 expect「建议每10-14天1次」是随机档位文案（默认态亦命中）。",
  },
{
  "slug": "gardening/soil-ph",
  "inputs": {
    "soilPh": "9.5"
  },
  "expect": [
    "+2.6"
  ],
  "ref": "第1066批 N172 口径统一后重锚：月季适宜 6.0-6.9，实测 9.5 ⇒ 偏差卡取距最近上边界 9.5−6.9=+2.6（旧中点口径 9.5−6.45=+3.05→「+3.0」，与建议「偏碱 2.6」同屏矛盾）。"
},
{
  "slug": "gardening/soil-ph",
  "clicks": [
    "document.getElementById('soilPh').value='';calc();var h=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='N171 '+(h.indexOf('请输入有效的 pH 值')>=0&&h.indexOf('偏酸')<0&&h.indexOf('0.0')<0?'OK':'BAD '+h.slice(0,90))"
  ],
  "expect": ["N171 OK"],
  "ref": "12-N171 空输入被 +''=0 误判为 pH 0：旧守卫 isNaN(0)||0<0||0>14 全部不成立，直接输出「当前土壤 pH 0.0」「⚠️ 偏酸」及整套加石灰方案。修复后先 trim 判空再 parseFloat，空值走「请输入有效的 pH 值（0-14）」并停算。本用例清空输入后同时要求有效提示存在、偏酸结论与 0.0 均不存在，三重条件杜绝旧版蒙混；默认 6.5 为完全适配，注入失败不产任一哨兵 ⇒ 零逃生。"
},
{
  "slug": "gardening/watering-schedule",
  "inputs": {
    "potSize": "30"
  },
  "expect": [
    "1.08L"
  ],
  "ref": "auto-restore"
},
{
  "slug": "gardening/soil-ph",
  "clicks": [
    "document.getElementById('plant').value='月季';document.getElementById('soilPh').value='9.5';calc();var h=String(document.getElementById('result').innerHTML).replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ');var ok=h.indexOf('+2.6')>=0&&h.indexOf('偏碱 2.6')>=0&&h.indexOf('+3.0')<0;document.getElementById('__tbProbe').textContent='SOILPH172 '+(ok?'OK':'BAD '+h.slice(h.indexOf('偏差'),h.indexOf('偏差')+90));"
  ],
  "expect": ["SOILPH172 OK"],
  "ref": "第1066批 N172：月季适宜 6.0-6.9，实测 9.5 ⇒ 距离最近上边界 9.5−6.9=2.6。偏差卡与建议文案必须用同一边界口径：新实现偏差卡「+2.6」、建议「土壤偏碱 2.6 个单位」同屏一致；旧实现偏差卡用中点 9.5−6.45=+3.0，与建议 2.6 自相矛盾。哨兵要求 +2.6 与「偏碱 2.6」同时出现且无 +3.0，默认 soilPh=6.5 在范围内不触发 ⇒ 依赖 clicks 注入，强判别零逃生。"
},
{
  "slug": "gardening/soil-ph",
  "clicks": [
    "document.getElementById('plant').value='蓝莓';document.getElementById('soilPh').value='6.8';calc();var h=String(document.getElementById('result').innerHTML);var a=h.indexOf('130-260 g/m²')>=0&&h.indexOf('按差值 1.3 个单位')>=0&&h.indexOf('降 1.3 个 pH')>=0;document.getElementById('soilPh').value='4.4';calc();var h2=String(document.getElementById('result').innerHTML);var b=h2.indexOf('10-30 g/m²')>=0&&h2.indexOf('按差值 0.1 个单位')>=0&&h2.indexOf('升 0.1 个 pH')>=0;document.getElementById('__tbProbe').textContent='SOILPH173 '+(a&&b?'OK':'BAD');"
  ],
  "expect": ["SOILPH173 OK"],
  "ref": "12-N173 调节剂用量按差值缩放（双向强锚）：蓝莓 4.5-5.5，实测 6.8 偏碱 1.3 单位 ⇒ 硫磺粉每单位基准 100-200g/m²×1.3=130-260 g/m²、效果「降 1.3 个 pH」；实测 4.4 偏酸 0.1 单位 ⇒ 石灰粉每单位基准 100-300g/m²×0.1=10-30 g/m²、效果「升 0.1 个 pH」。旧版把整表 dose 原样渲染（恒为 100-200 g / 100-300 g、效果恒为「1 个 pH」），两个方向哨兵均不命中；默认 soilPh=6.5 完全适配不产出调节剂，注入失败零逃生。"
},
{
  "slug": "gardening/watering-schedule",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/gardening/watering-schedule.html','utf8');var ok=h.indexOf('单次约 234ml')<0&&h.indexOf('单次 20×1.0×0.6×0.9×10=108ml')>=0;document.getElementById('__tbProbe').textContent='WATEREX '+(ok?'OK':'BAD');"],
  "expect": ["WATEREX OK"],
  "ref": "第1089批 N198：冬季室内单次水量按页内公式 round(盆径×基础系数×季节系数×环境系数×10)=round(20×1.0×0.6×0.9×10)=108ml；旧算例把环境频率系数 1.3 误当水量系数写成 234ml。源码形态判别：旧串消失且新代入式+108ml 出现才通过。"
},
{
  "slug": "gardening/pruning-calendar",
  "clicks": ["selectSeason('autumn');var info=String(document.getElementById('seasonInfo').innerHTML);var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/gardening/pruning-calendar.html','utf8');var i=h.indexOf('function __pruning_calendarExport(){'),j=h.indexOf('function __pruning_calendarPresets(){');var ex=j>i?h.slice(i,j):'';var dd=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/content_deepdive.json','utf8');var rose=PLANTS.find(p=>p.name==='月季');var ok=rose.seasons.autumn==='ok'&&info.indexOf('不宜修剪 5 种')>=0&&ex.indexOf(\"TBKit.util.exportTable('#pruning_calendarTable'\")<0&&ex.indexOf('TBKit.util.exportCsv')>=0&&ex.indexOf('PLANTS.forEach')>=0&&ex.indexOf('SEASONS.forEach')>=0&&h.indexOf(\"name:'月季', icon:'🌹', seasons:{spring:'best',summer:'ok',autumn:'ok',winter:'best'}\")>=0&&h.indexOf(\"name:'栀子花', icon:'🌼', seasons:{spring:'avoid',summer:'ok',autumn:'best',winter:'avoid'}\")>=0&&h.indexOf(\"name:'杜鹃', icon:'🌺', seasons:{spring:'avoid',summer:'best',autumn:'avoid',winter:'ok'}\")>=0&&dd.indexOf('春冬 best（冬季休眠期重剪）、夏秋 ok')>=0;document.getElementById('__tbProbe').textContent='PRUNECAL '+(ok?'OK':'BAD');"],
  "expect": ["PRUNECAL OK"],
  "ref": "12-N225/N226：导出函数不再读搜索历史表，改为 PLANTS×SEASONS 全矩阵经 exportCsv 输出；杜鹃秋季、栀子花春季改 avoid，与自身描述一致；月季冬季按公式框重剪改 best。注入秋季后不宜植物由旧版 4 种变 5 种，默认春季为 3 种，零逃生；源码形态同时校验深解算例口径。"
},
{
  "slug": "gardening/lawn-mowing",
  "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/gardening/lawn-mowing.html','utf8');var en=globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/en/gardening/lawn-mowing.json','utf8');var ok=h.indexOf('早熟禾 5 至 8 cm')<0&&h.indexOf('结缕草 2.5 至 5 cm')<0&&h.indexOf('高羊茅 6 至 9 cm')<0&&h.indexOf('早熟禾 4–5 cm')>=0&&h.indexOf('结缕草 3–5 cm')>=0&&h.indexOf('高羊茅 5–6 cm')>=0&&h.indexOf('秋季约每 10 天 1 次')>=0&&en.indexOf('Kentucky bluegrass 5 to 8 cm')<0&&en.indexOf('Kentucky bluegrass 4-5 cm')>=0&&en.indexOf('about every 10 days in autumn')>=0;document.getElementById('__tbProbe').textContent='LAWNFM '+(ok?'OK':'BAD');"],
  "expect": ["LAWNFM OK"],
  "ref": "12-N227：公式框原写早熟禾 5–8、结缕草 2.5–5、高羊茅 6–9 cm，与 GRASSES 数据表（4–5 / 3–5 / 5–6 cm）冲突；生长期每 5–7 天又与秋季每 10 天冲突。修复后公式为数据表口径并区分春季 5–7 天、秋季 10 天、冬季 2–4 周；中英源同时校验，旧版任一旧串命中即红。"
  },
  {
    "slug": "gardening/reminder-cycle-succulent",
    "clicks": ["var d=parseLocalDate('2026-11-06');var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/gardening/reminder-cycle-succulent.html','utf8');var ok=!!d&&d.getFullYear()===2026&&d.getMonth()===10&&d.getDate()===6&&h.indexOf('new Date(plant.lastWater)')<0&&h.indexOf('new Date(todayStr())')<0&&h.indexOf('parseLocalDate(plant.lastWater)')>=0&&h.indexOf('parseLocalDate(todayStr())')>=0;document.getElementById('__tbProbe').textContent='LOCALDATE '+(ok?'OK':'BAD');"],
    "expect": ["LOCALDATE OK"],
    "ref": "YYYY-MM-DD 原先用 new Date(字符串) 按 UTC 午夜解析，西半球本地显示前一天；现 parseLocalDate 按本地年月日构造，上次浇水与今天/剩余天数不再整体偏一天。旧版无该函数且两处仍是裸 new Date ⇒ 哨兵红；默认态不产生该哨兵。"
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

  console.log("==== gardening calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
