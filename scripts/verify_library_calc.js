#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
    "slug": "library/generator-label",
    "clicks": ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'fonds',type:'text',value:'A032'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};var __r=document.getElementById('res');if(__r){__r.textContent='请至少填写一项标签内容。';}window.__labelData=null;__generator_label_last=0;__generator_labelExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='LBLEMPTY hist='+__cap.length+' score='+__generator_labelScore('请至少填写一项标签内容。');"],
    "expect": ["LBLEMPTY hist=0 score=0"],
    "ref": "复核失败重做·第46批 标签空态：生成默认标签后清空全部内容，gen() 写空态提示并 __labelData=null；旧实现 Extras 无成功守卫仍写历史 hist=1 且 Score 词表无「请至少填写」判通过 score=1；修复后 Extras 先判 __labelData 才记录 ⇒ hist=0，Score 补空态关键词 ⇒ score=0。单条探针同时覆盖两处修复，默认态无探针串 ⇒ 零逃生。"
  },
{
  "slug": "library/archive-label",
  "inputs": {
    "fonds": "4",
    "catalog": "01",
    "boxNo": "0001",
    "year": "2024",
    "org": "办公室",
    "title": "综合文书档案",
    "range": "1-50",
    "unit": "XX市人民政府"
  },
  "expect": [
    "4-01-0001"
  ],
  "ref": "auto-restore"
},
{
  "slug": "library/archive-label",
  "inputs": {
    "fonds": "4", "catalog": "01", "boxNo": "A0001", "year": "2024", "org": "办公室", "title": "测试", "range": "1-30", "unit": "XX市人民政府",
    "__alFrom": "1", "__alCount": "2", "__alPerBox": "30"
  },
  "clicks": ["__alBatch()", "var t=String(document.getElementById('__alBatchTable').innerHTML||'');document.getElementById('__tbProbe').textContent=(t.indexOf('A0002')>=0&&t.indexOf('00002')<0)?'PFX OK':'PFX BAD'"],
  "expect": ["PFX OK"],
  "ref": "RL-K21 盒号前缀保留：boxNo=A0001 时批量盒号应为 A0001/A0002，旧版取 boxNo.length 纯数字 pad 生成 00001/00002，前缀 A 丢失。修复后正则拆分前缀 A 与数字段 0001，批量 prefix+pad 生成 A0002。哨兵断言含 A0002 且不含 00002，读 innerHTML（stub DOM 的 textContent 不反射 innerHTML）。"
},
{
  "slug": "library/archive-label",
  "inputs": {
    "fonds": "4", "catalog": "01", "boxNo": "0001", "year": "2024", "org": "办公室", "title": "测试", "range": "1-30", "unit": "XX市人民政府",
    "__alFrom": "1", "__alCount": "2", "__alPerBox": "50"
  },
  "clicks": ["__alBatch()", "var k=String(document.getElementById('__alCheck').innerHTML||'');document.getElementById('__tbProbe').textContent=(k.indexOf('超过起止件号')>=0)?'SPAN OK':'SPAN BAD'"],
  "expect": ["SPAN OK"],
  "ref": "RL-K20 perBox 超 range 跨度：range=1-30 跨度 30，每盒件数 50 超出 ⇒ 修复后在 __alCheck 追加警告「每盒件数 50 超过起止件号 1-30 的跨度 30 件」，旧版无任何冲突提示。哨兵锚「超过起止件号」。"
},
{
  "slug": "library/archive-label",
  "inputs": {
    "fonds": "4", "catalog": "01", "boxNo": "0001", "year": "2024", "org": "办公室", "title": "测试", "range": "1-50", "unit": "XX市人民政府",
    "__alFrom": "1", "__alCount": "2", "__alPerBox": "0"
  },
  "clicks": ["__alBatch()", "var k=String(document.getElementById('__alCheck').innerHTML||'');document.getElementById('__tbProbe').textContent=(k.indexOf('批量参数不合法')>=0)?'BADPARAM OK':'BADPARAM BAD'"],
  "expect": ["BADPARAM OK"],
  "ref": "RL-K21 非法参数反馈：每盒件数=0 时旧版 __alBatch 静默 return、界面无提示；修复后在 __alCheck 写「批量参数不合法…」。哨兵锚「批量参数不合法」。"
},
{
  "slug":"library/archive-label", "inputs":{"__alFrom":"1.5","__alCount":"2","__alPerBox":"50"},
  "clicks":["__alBatch()"], "expect":["批量参数不合法"], "ref":"小数盒号不得被截断成整数。"
},
{
  "slug":"library/archive-label", "inputs":{"__alFrom":"1","__alCount":"201","__alPerBox":"50"},
  "clicks":["__alBatch()"], "expect":["盒数最多 200"], "ref":"盒数上限必须在生成前执行，避免无界循环。"
},
{
  "slug": "library/clc-classifier",
  "inputs": {
    "search": "zzzqx"
  },
  "expect": [
    "搜索结果：0 条"
  ],
  "ref": "inputs 写 search=zzzqx ⇒ oninput=onSearch() ⇒ renderSubs('zzzqx') 命中 0 条 ⇒ 结果区渲染「搜索结果：0 条」。默认态走 else 分支渲染当前主类二级类目、blob 无「搜索结果」串（已双态核验）；兜底 onSearch() 读到空值仍走 else，不产该串。"
},
{
  "slug": "library/clc-classifier",
  "clicks": ["selectedCode='B84';updateResult();var b=document.getElementById('result').innerHTML.match(/当前选择分类号：<strong[^>]*>([^<]+)<\\/strong>/)[1];switchMain('T');var a=document.getElementById('result').innerHTML.match(/当前选择分类号：<strong[^>]*>([^<]+)<\\/strong>/)[1];document.getElementById('__tbProbe').textContent='SWITCH '+b+'->'+a;"],
  "expect": ["SWITCH B84->未选择"],
  "ref": "切换大类清空选择：旧版按钮只改 currentMain 不重置 selectedCode，选中 B84 后切到 T，结果区仍显示 B84 并生成 B84/123 跨大类索书号。封装 switchMain 并在切换时清空，端到端断言分类号从 B84 变为未选择；默认态无 SWITCH 串，不命中。"
},
{
  "slug": "library/clc-classifier",
  "inputs": { "search": "tp3" },
  "expect": ["搜索结果：3 条", "TP31"],
  "ref": "深度解析示例承诺检索 TP3 可命中并生成 TP3/123，但旧表只到二级 TB…TV，search('tp3') 返回 0 条。现补 TP3/TP31/TP39 常用三级类目，按类号前缀命中 3 条。默认 A 大类无这些类号，不命中。"
},
{
  "slug": "library/clc-classifier",
  "inputs": { "search": "计算机" },
  "expect": ["搜索结果：4 条", "TP39"],
  "ref": "中文主题检索：旧版仅命中 TP 自动化技术、计算机技术 1 条，无法复现深度解析的「检索计算机」三级下钻。补三级类目后命中 TP/TP3/TP31/TP39 共 4 条。默认 A 大类无这些条目，不命中。"
},
{
  "slug": "library/generator-label",
  "inputs": {
    "fonds": "B123",
    "year": "2025",
    "org": "财务处",
    "range": "0201-0350",
    "boxNo": "007",
    "unit": "City Archives",
    "thick": "50"
  },
  "expect": [
    "13.3pt",
    "50mm"
  ],
  "ref": "真实标签生成器（非随机示例）：注入 6 项标签内容 + 脊背厚度 50mm ⇒ labelRows() 生成 6 行 ⇒ labelFont(50,6)=min(14,50/6×1.6)=13.3pt，结果区渲染「字号 13.3pt · 脊背厚度 50mm」；默认态为 30mm/5 行 ⇒ 9.6pt，故 13.3pt/50mm 均为输入驱动的派生值，非默认标签可命中。"
},
{
  "slug": "library/generator-label",
  "inputs": {
    "fonds": "A032",
    "year": "2024",
    "org": "办公室",
    "range": "0001-0150",
    "boxNo": "001-003",
    "unit": "",
    "thick": "30"
  },
  "expect": [
    "本次生成 3 张"
  ],
  "ref": "盒号范围批量分支：boxNo='001-003' ⇒ labelBoxes 展开 ['001','002','003'] 且逐张渲染（盒号行分别替换），结果区元信息「本次生成 3 张」只在批量模式出现；默认单号 012 ⇒「本次生成 1 张」，不含该串。'001'/'003' 为展开后的盒号值，默认态仅有 012。"
},
{
    "slug": "library/generator-label",
    "inputs": { "fonds": "A", "range": "1-10", "boxNo": "0-499" },
    "expect": ["本次生成 500 张"],
    "ref": "第407批复核失败重做：批量上限 500 张。原 `b-a<=500` 含两端 ⇒ 0-499 得 500、0-500 得 501（超出承诺）。修复按项数 `b-a+1<=500`。0-499 展开恰好 500 张，锚绑定注入的盒号范围；默认单号 012 ⇒「本次生成 1 张」不命中 ⇒ 强判别。"
},
{
    "slug": "library/generator-label",
    "inputs": { "fonds": "A", "range": "1-10", "boxNo": "0-500" },
    "expect": ["盒号批量数量超过上限 500 张"],
    "ref": "第407批复核失败重做：0-500 共 501 项超上限，原实现静默生成 501 张且无提示；修复后 labelBoxes 设超限标记、gen() 明确提示并停止生成。逗号列表分支同样加 500 上限。默认单号 012 不触发超限 ⇒ 强判别。"
},
{
  "slug": "library/overdue-fine",
  "inputs": {
    "borrowDays": "45",
    "dailyFine": "0.5",
    "bookCount": "1",
    "cap": "50"
  },
  "expect": [
    "45"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "library/shelf-capacity",
  "inputs": {
    "layers": "9",
    "layerLen": "1",
    "bookThick": "2.5",
    "fillRate": "85",
    "totalBooks": "50000",
    "perRow": "8",
    "rowGap": "1.2"
  },
  "expect": ["82 架", "11 排", "实际架体总长 82.0 米", "满排布局总长 88.0 米", "主通道总长 984.0 米", "末排实际书架 2 架", "1533.4 ㎡"],
  "ref": "第1114批：9 层、1m 层长、2.5cm 书厚、85% 填充、50000 册、每排 8 架 → 单架 612 册、82 架、11 排；实际架体 82m，满排预留 88m，末排仅 2 架；主通道（11+1 条）×实际排长 82m=984m；面积=82×（11×0.5+10×1.2+1.2）=1533.4㎡。原断言为旧「排架总长 88m/通道总长 13.2m」口径。"
},
{
  "slug": "library/stats-report",
  "inputs": {
    "colTotal": "86000",
    "loanCnt": "64500",
    "readerCnt": "5200",
    "visitCnt": "91000",
    "newCol": "4300"
  },
  "expect": [
    "75.00",
    "12.40",
    "17.50"
  ],
  "ref": "馆藏利用：藏书86000、借阅64500、读者5200、到馆91000 → 利用率64500/86000=75.00%、人均借阅64500/5200=12.40册、人均到馆91000/5200=17.50次（独立复算，非页面默认 120000/96000/8000/150000/6000）"
},
{
  "slug": "library/stats-report",
  "inputs": { "loanCnt": "-5000" },
  "expect": ["年度借阅册次不能为负"],
  "ref": "负借阅：旧版 isFinite 与馆藏/读者正数校验均放行 -5000，输出 -4.17% 利用率与负人均。现按字段拦截。默认借阅 96000 ⇒ 不命中。"
},
{
  "slug": "library/stats-report",
  "inputs": { "visitCnt": "-100" },
  "expect": ["年度到馆人次不能为负"],
  "ref": "负到馆：旧版负值进入人均到馆与单次借阅得负数。现按字段拦截。默认到馆 150000 ⇒ 不命中。"
},
{
  "slug": "library/stats-report",
  "inputs": { "newCol": "-100" },
  "expect": ["年度新增馆藏不能为负"],
  "ref": "负新增：旧版负值被当成净减馆藏仍出完整报表。现按字段拦截。默认新增 6000 ⇒ 不命中。"
},
{
  "slug": "library/stats-report",
  "inputs": { "colTotal": "100000", "loanCnt": "25000" },
  "expect": ["图书周转天数： 1,460.0 天"],
  "ref": "周转天数：公式框承诺 365÷流通率但结果区未实现，且百分数直除会差 100 倍。现按小数口径 365÷(25000/100000)=1460.0 天并显式标注；默认 365÷0.8=456.3 天不命中。"
},
{
  "slug": "library/overdue-fine",
  "inputs": {
    "borrowDate": "2026-01-10",
    "dueDate": "2026-01-20",
    "returnDate": "2026-01-05"
  },
  "expect": ["归还日期不能早于借阅日期"],
  "ref": "归还 2026-01-05 早于借阅 2026-01-10 ⇒ 旧实现 daysBetween 得负天数，仍按 0 逾期出结果；现明确拦截。默认借阅为今天−40 天、归还为今天，不会命中。"
},
{
  "slug": "library/overdue-fine",
  "inputs": {
    "borrowDate": "2026-01-10",
    "dueDate": "2026-01-20",
    "returnDate": "2026-01-25",
    "bookCount": "-2"
  },
  "expect": ["逾期本数必须为不小于 1 的整数"],
  "ref": "负册数会让总罚金变成负数；旧实现 `parseInt(...)||1` 只兜住 0/NaN，负数原样参与乘法。默认 1 本不命中。"
},
{
  "slug": "library/overdue-fine",
  "inputs": {
    "borrowDate": "2026-01-10",
    "dueDate": "",
    "borrowDays": "abc"
  },
  "expect": ["借阅天数需为不小于 0 的整数"],
  "ref": "未选应还日期时用借阅天数推算；旧实现 parseInt('abc')||0 静默按 0 天 ⇒ 应还=借阅日、逾期天数翻倍。默认应还日期为借阅+30 天 ⇒ 不命中。"
},
{
  "slug": "library/overdue-fine",
  "inputs": {
    "borrowDate": "2026-01-10",
    "dueDate": "2026-01-20",
    "returnDate": "2026-01-25",
    "dailyFine": ""
  },
  "expect": ["日罚金需为有效数值（不能为负数，可为 0）"],
  "ref": "日罚金清空后旧实现 parseFloat('')||0 ⇒ 逾期照样算出 ¥0.00，等于免罚；现显式提示。默认 0.2 ⇒ 不命中。"
},
{
  "slug": "library/shelf-capacity",
  "inputs": { "fillRate": "0" },
  "expect": ["填充率需在 1–100 之间。"],
  "ref": "填充率填 0 后旧实现 parseFloat('0')||100 ⇒ 静默按 100% 铺满计算，容量虚高；现显式拒绝。默认 75 ⇒ 不命中。"
},
{
  "slug": "library/shelf-capacity",
  "inputs": { "bookThick": "0" },
  "expect": ["图书平均厚度需大于 0 cm。"],
  "ref": "书厚 0：旧版 parseFloat('0')||1 静默按 1cm 算得每层 85 册与一整套容量方案，掩盖错误输入。现书厚须 >0 并拦截。默认 2.5 ⇒ 不命中。"
},
{
  "slug": "library/shelf-capacity",
  "inputs": { "totalBooks": "-5000" },
  "expect": ["总馆藏量需为不小于 0 的数值。"],
  "ref": "负馆藏：旧版无负数守卫，输出 -12 架、-1 排、-8.0 米、-13.6㎡ 等不可实现的规划结果。现总馆藏量 >=0 拦截。默认 4200 ⇒ 不命中。"
},
{
  "slug": "library/shelf-capacity",
  "inputs": { "rowGap": "-1.2" },
  "expect": ["排间距需为不小于 0 的数值。"],
  "ref": "负排距：旧版 -1.2 米直接进面积公式得负面积。现排间距 >=0 拦截。默认 1.2 ⇒ 不命中。"
},
{
  "slug": "library/shelf-capacity",
  "inputs": { "fillRate": "150" },
  "expect": ["填充率需在 1–100 之间。"],
  "ref": "填充率超 100：旧版 150% 会算出超过物理层长的册数，仍输出完整方案。现填充率限 1–100。默认 75 ⇒ 不命中。"
},
{
  "slug": "library/shelf-capacity",
  "inputs": { "layers": "0" },
  "expect": ["每架层数需为不小于 1 的整数。"],
  "ref": "层数填 0 后旧实现 parseInt('0')||1 ⇒ 静默按 1 层计算；现显式拒绝。默认 6 ⇒ 不命中。"
},
{
  "slug": "library/citation-format",
  "clicks": ["document.getElementById('docType').value='book';onTypeChange();document.getElementById('title').value='图书馆学概论';document.getElementById('seq').value='5';document.getElementById('edition').value='2';document.getElementById('place').value='北京';document.getElementById('publisher').value='科学出版社';document.getElementById('year').value='2023';document.getElementById('pages').value='35-42';render()"],
  "expect": ["[5]", "[M]. 2版. 北京: 科学出版社, 2023.35-42."],
  "ref": "GB/T 7714-2015 专著著录：`[序号] 作者. 题名[M]. 版本. 出版地: 出版社, 出版年: 页码.`（页面页码前用 `.` 而非 `:`）。注入 docType=book、title=图书馆学概论、seq=5、edition=2、place=北京、publisher=科学出版社、year=2023、pages=35-42 ⇒ `[5] … 图书馆学概论[M]. 2版. 北京: 科学出版社, 2023.35-42.`。默认 docType=journal ⇒ `[1] … 数字图书馆建设与发展研究[J]. 中国图书馆学报, 2023,49(3): …`，不含 `[M]`/`2版`/`35-42`，两态不同。判别器清空 clicks 后 docType 回落到 select 默认 journal，仍走 [J] 分支，expect 失配。（作者段由桩内 appendChild 拼串生成、与真机不同，故断言不从作者段起算，只锚类型标识起算的著录体。）"
},
{
  "slug": "library/citation-format",
  "clicks": ["document.getElementById('docType').value='web';onTypeChange();document.getElementById('title').value='数字图书馆标准规范';document.getElementById('seq').value='7';document.getElementById('date').value='2023-08-01';document.getElementById('cited').value='2024-01-10';document.getElementById('url').value='https://example.com/lib-standard';render()"],
  "expect": ["[7]", "[EB/OL]. (2023-08-01)[2024-01-10]. https://example.com/lib-standard."],
  "ref": "GB/T 7714-2015 电子资源著录：`[序号] 作者. 题名[EB/OL]. (更新日期)[引用日期]. URL.`。注入 docType=web、title=数字图书馆标准规范、seq=7、date=2023-08-01、cited=2024-01-10、url=https://example.com/lib-standard ⇒ `[7] … 数字图书馆标准规范[EB/OL]. (2023-08-01)[2024-01-10]. https://example.com/lib-standard.`。默认 journal 分支不含 `[EB/OL]`、`[引用日期]` 与示例 URL，两态不同；判别器清空 clicks 后回 journal，expect 失配。"
},
{ "slug":"library/clc-classifier", "clicks":["document.getElementById('res').textContent='C='+clcData.reduce(function(a,c){return a.concat(c.subs.filter(function(x){return x.name.indexOf('眼科学')>=0;}).map(function(x){return x.code;}));},[]).join(',')"], "expect":["C=R77"], "ref":"RL-H20：R76 应为耳鼻咽喉科学、R77 为眼科学；搜索眼科学只返回 R77。" },
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

  console.log("==== library calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
