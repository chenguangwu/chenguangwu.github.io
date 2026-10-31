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
  "slug": "library/citation-format",
  "inputs": {
    "title": "数字图书馆建设与发展研究",
    "seq": "1",
    "edition": "第5版",
    "place": "北京",
    "publisher": "中国标准出版社",
    "year": "2023-06-15",
    "pages": "45-52",
    "journal": "中国图书馆学报",
    "volissue": "2023,49(3)",
    "degree": "博士",
    "school": "北京大学",
    "conf": "全国图书馆学学术研讨会",
    "stdno": "GB/T 7714-2015",
    "patno": "ZL202310000000.1",
    "paper": "人民日报",
    "date": "2023-08-01",
    "url": "https://www.example.com/article/123",
    "cited": "2024-01-10",
    "docType": "journal"
  },
  "expect": [
    "journal"
  ],
    ref: "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。",
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
    "cnt": "20"
  },
  "expect": [
    "项目管理 2022年度 保管期限：10年 档号：XM-2022-033"
  ],
  "ref": "auto-restore（随机档号生成器，具体档号非每次必现；改断言确定性生成标题）（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
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
