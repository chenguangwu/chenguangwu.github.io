#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "travel/aim-trainer",
  "inputs": {},
  "expect": [
    "30.0s"
  ],
  "ref": "结构性不可注入（2026-09-24 travel 批）：页面静态 HTML 中 input/select/textarea 计数为 0（实测 grep -cE '<input|<select|<textarea' = 0），靶场由 start()/reset() 按钮驱动、按钮无 id 且不在 harness 的 elements 表内，也无 clicks 注入 ⇒ 只能渲染默认串。保留在 no_inputs 基线。"
},
{
  "slug": "travel/business-name-generator",
  "inputs": {
    "count": "15"
  },
  "expect": [
    "15"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/currency-cheat-sheet",
  "inputs": {
    "rate": "7.20",
    "customAmounts": "1,5,10,20,50,100",
    "currency": "EUR,7.80,🇪🇺,€,欧元"
  },
  "expect": [
    "1560"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/emergency-phrasebook",
  "inputs": {},
  "expect": [
    "ee-mer-jen-see"
  ],
  "ref": "结构性不可注入（2026-09-24 travel 批）：input/select/textarea 计数为 0；短语表与语言按钮均由 JS 模板渲染，切语言靠 setLang('<lang>') 按钮 onclick（无 id、不在 elements 表、无 clicks），且 setLang 属 DESTRUCTIVE 前缀已被 harness 兜底排除 ⇒ 只能渲染默认英文表。保留在 no_inputs 基线。"
},
{
  "slug": "travel/international-tip-calculator",
  "inputs": {
    "bill": "150",
    "people": "1"
  },
  "expect": [
    "150"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/jet-lag-recovery",
  "inputs": {
    "flightHours": "12",
    "fromTz": "9"
  },
  "expect": [
    "-14小时"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/luggage-size-checker",
  "inputs": {
    "l": "83",
    "w": "40",
    "h": "20",
    "wt": "7"
  },
  "expect": [
    "83×40×20cm"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/packing-list",
  "inputs": {},
  "expect": [
    "0/6"
  ],
  "ref": "结构性不可注入（2026-09-24 travel 批）：页面带 id 的控件只有 input#tripName（默认「我的旅行」）与 input#tripDate，实测注入 tripName=测试行程A 后输出与默认态逐字一致（渲染主体 renderList() 只读 currentData.categories，tripName 仅在 saveList() 写 localStorage 时使用，而 saveList 不在 harness 兜底调用序列内）⇒ 输入不影响任何渲染结果；清单勾选靠 div.checkbox 的 toggleItem(i,j) onclick、换模板靠 loadTemplate('x') onclick，均无 id 不可注入。保留在 no_inputs 基线。"
},
{
  "slug": "travel/passport-validator",
  "inputs": {
    "input": "E12345678"
  },
  "expect": [
    "中国（CN）：1 字母 + 8 数字",
    "通用 ICAO 9303（XX）：9 位机器可读字符"
  ],
  "ref": "去默认化（原 expect「等待输入...」＝空输入分支，注入失败仍命中 → 逃生项）：注入 E12345678（1 字母 + 8 数字）后 validate() 按 PASSPORT_FORMATS 逐条正则匹配，同时命中中国 CN（/^[EeKkGgDd]\\d{8}$/）与通用 ICAO 9303（/^[A-Z0-9<]{9}$/）两项；默认空输入只输出「等待输入...」不含这两串，注入失败即不命中。"
},
{
  "slug": "travel/recommender-10",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "6."
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/recommender-9",
  "inputs": {
    "cnt": "8"
  },
  "expect": [
    "8. "
  ],
  "ref": "auto-restore（原断言为静态标题，注入失败仍命中 → 逃生项；改为断言条数/第8条）"
},
{
  "slug": "travel/road-trip-gas-cost",
  "inputs": {
    "distance": "750",
    "consumption": "8",
    "price": "7.5",
    "tolls": "200",
    "people": "2"
  },
  "expect": [
    "60.0L"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/timezone-lookup",
  "inputs": {
    "input": "Asia/Tokyo"
  },
  "expect": [
    "日本标准时间",
    "+09:00（UTC+9）"
  ],
  "ref": "去默认化（原 expect「等待输入...」＝空输入分支，注入失败仍命中 → 逃生项）：注入 IANA 名 Asia/Tokyo，validate() 走 TIMEZONES[raw] 精确命中分支，输出名称「日本标准时间」+「UTC 偏移：+09:00（UTC+9）」；默认空输入只输出「等待输入...」。"
},
{
  "slug": "travel/travel-adapter-guide",
  "inputs": {
    "search": "日本"
  },
  "expect": [
    "日本\n日本 Type A Type B ⚡ 100V"
  ],
  "ref": "去默认化 + P0 缺陷修复：原 render(list) 用 if(!list.length) 判空，而 plugs/filter 传入的是**对象**（无 length ⇒ 恒 truthy ⇒ 恒判空）⇒ 整页搜索无论输入什么都只显示「未找到」，默认态亦然（原 expect 正是这个「未找到」）。已修：if(!list||!Object.keys(list).length)。修复后注入 search=日本 只渲染日本一张卡（Type A/B、⚡100V），默认态（搜索框空）渲染全部 35 国、不含「日本\\n日本 …」这种回显紧邻卡片的排布 ⇒ 注入失败即不命中。"
},
{
  "slug": "travel/travel-budget-calculator",
  "inputs": {
    "days": "11",
    "people": "2",
    "transport": "3000",
    "accommodation": "500",
    "food": "200",
    "tickets": "800",
    "shopping": "1000",
    "emergency": "1000"
  },
  "expect": [
    "(22.2%)"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/travel-days-counter",
  "inputs": {
    "start": "2026-10-01",
    "end": "2026-10-05"
  },
  "expect": [
    "5 天 (4晚)",
    "📅 2026-10-01 出发"
  ],
  "ref": "去默认化（原 expect「8 天 (7晚)」＝页面默认值 start=2024-06-22 / end=2024-06-29 的行程时长，注入失败仍命中 → 逃生项）：注入 2026-10-01 → 2026-10-05，calc() 算 days = ceil(4 天)+1 = 5、nights = 4，卡片显示「5 天 (4晚)」+ 详情行「📅 2026-10-01 出发」。两串均与注入日期绑定、且与真实当天无关（不锚「距离出发还有 N 天」这类随 now 漂移的分支）；默认 2024-06-22/29 得 8 天 7 晚，注入失败即不命中。"
},
{
  "slug": "travel/travel-insurance-comparison",
  "inputs": {
    "days": "21"
  },
  "expect": [
    "120-240"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/travel-photo-storage",
  "inputs": {
    "days": "11",
    "perDay": "100",
    "videoMin": "10"
  },
  "expect": [
    "1100"
  ],
  "ref": "auto-restore"
},
{
  "slug": "travel/visa-requirement-checker",
  "inputs": {
    "search": "日本"
  },
  "expect": [
    "需提前办理签证，有3年/5年多次往返\n🏯 东亚"
  ],
  "ref": "去默认化（原 expect「持有效美/日/澳等签证可免7天」是默认全量 54 国列表里菲律宾那行的静态数据，注入失败仍命中 → 逃生项）：注入 search=日本，filter() 把列表收敛到日本一行，输出「日本 需签证 东亚 需提前办理签证，有3年/5年多次往返」紧邻下方地区统计「🏯 东亚 2个国家/地区」；该「备注\\n统计」相邻串只在过滤后成立（默认态日本行后面紧跟的是「韩国 需签证」），注入失败即不命中。"
},
{
  "slug": "travel/world-timezone-converter",
  "inputs": {
    "localTime": "14:30",
    "localDate": "2026-10-01"
  },
  "expect": [
    "10月1日周四"
  ],
  "ref": "去默认化（原 expect「北京/上海」是卡片里恒显示的静态城市名标签，注入失败仍命中 → 逃生项）：注入 localTime=14:30 / localDate=2026-10-01 后 render() 走 now=new Date('2026-10-01T14:30') 分支（不再回填当天），六个默认城市卡片的日期全部由该基准日推出（北京/上海 10月1日周四、洛杉矶 9月30日周三 昨天）；默认态基于当天显示 6月15日周六，注入失败即不命中。（注：harness 环境下 toTimeString() 被桩成固定串故时刻段恒为 00:00，因此只锚日期段。）"
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
  console.log("==== travel calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
