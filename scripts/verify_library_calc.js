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
  "ref": "auto-restore"
},
{
  "slug": "library/clc-classifier",
  "inputs": {},
  "expect": [
    "TP/W285"
  ],
  "ref": "auto-restore(default)"
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
  "expect": [
    "168.0"
  ],
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
    try { const r = await runCase(c); if (r.ok) pass++; else fails.push(c.slug); }
    catch (e) { fails.push(c.slug); }
  }
  console.log("==== library calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
