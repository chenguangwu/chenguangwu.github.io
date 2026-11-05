#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
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
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
  "ref": "auto-restore"
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
  "expect": ["9\n1\n2.5\n85\n50000\n8\n1.2\n2\n34 册 每层容量 612 册 单架容量 82 架 所需书架 11 排 排数 88.0 米 排架总长 149.6 ㎡ 估算面积 单架容量示意（每层 34 册） 项目 数值 每层有效长度 85.0 cm 每层册数 34 册 单架册数（9层×2面） 612 册 每排书架数 8 架 单排长度 8.00 米 排架总长 88.0 米 通道总长 13.2 米 所需书架 82 架 / 11 排 填充率建议 80%~90%，预留取书空间。估算面积按排架总长×(通道宽+0.5m架深)粗算，实际需结合阅览区、工作区综合规划。"],
  "ref": "auto-restore"
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

  console.log("==== library calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
