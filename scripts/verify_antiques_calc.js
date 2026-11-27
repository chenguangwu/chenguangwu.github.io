#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "antiques/bronze-identification",
  "inputs": {
    "era": "xia"
  },
  "expect": [
    "xia"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "antiques/calligraphy-style",
  "inputs": {
    "era": "shang"
  },
  "expect": [
    "shang"
  ],
  "ref": "auto-restore（默认下拉值为全部年代 ⇒ 渲染完整年代目录，任何年代条目文本都会在默认态命中 ⇒ 无法改用条目锚，维持原断言） [被覆盖的前条说明：⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。]"
},
{
  "slug": "antiques/furniture-style",
  "inputs": {
    "era": "song"
  },
  "expect": [
    "song"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "antiques/porcelain-date",
  "inputs": {
    "dynasty": "tang"
  },
  "expect": [
    "tang"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "antiques/porcelain-date",
  "inputs": {
    "dynasty": "song",
    "search": "青瓷"
  },
  "expect": [
    "汝窑天青釉温润如玉"
  ],
  "ref": "宋代+青瓷过滤命中宋代条目，expect 为宋代专属釉色描述；唐代/默认态不含该串，零逃生。"
},
{
  "slug": "antiques/rater-1",
  "inputs": {
    "ctype": "stamp",
    "i_perf": "3",
    "i_gum": "3",
    "i_center": "3",
    "i_creases": "3",
    "i_stain": "3",
    "i_color": "3"
  },
  "expect": [
    "自定义档（不是机构等级）"
  ],
  "ref": "邮票六项全严重 ⇒ 得分 1、自定义档 E（扣分触底）；expect 为「自定义档（不是机构等级）」标签及触底结果 E，明确不是机构等级。"
},
{
  "slug": "antiques/rater-1",
  "inputs": {
    "ctype": "stamp",
    "i_perf": "0",
    "i_gum": "0",
    "i_center": "0",
    "i_creases": "0",
    "i_stain": "0",
    "i_color": "3"
  },
  "expect": [
    "82",
    "82"
  ],
  "ref": "邮票仅颜色严重扣 18 ⇒ 100-18=82；用于锁定自定义扣分结果，不宣称机构评级。"
},
{
  "slug": "antiques/seal-identification",
  "inputs": {
    "era": "qin"
  },
  "expect": [
    "qin"
  ],
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
    "slug": "antiques/calligraphy-style",
    "inputs": {"era":"nanbei"},
    "expect": ["南北朝","郑文公碑"],
    "ref": "第865批：补南北朝时期条目，筛选后应出现魏碑代表《郑文公碑》。"
  },
  {
    "slug": "antiques/calligraphy-style",
    "inputs": {"era":"sui"},
    "expect": ["隋代","龙藏寺碑"],
    "ref": "第865批：补隋代条目，筛选后应出现《龙藏寺碑》。"
  },
  {
    "slug": "antiques/calligraphy-style",
    "inputs": {"era":"yuan"},
    "expect": ["元代","赵孟頫"],
    "ref": "第865批：补元代条目，筛选后应出现赵孟頫。"
  },
  {
    "slug": "antiques/rater-1",
    "inputs": {"ctype":"coin"},
    "clicks": ["document.getElementById('i_obverse').value='3';onItemChange();document.getElementById('ctype').value='stamp';renderItems();document.getElementById('ctype').value='coin';renderItems();calc();document.getElementById('__tbProbe').textContent='TB865R '+((document.getElementById('i_obverse').value==='3')?'OK':'BAD');"],
    "expect": ["TB865R OK","58"],
    "ref": "第865批：切换纪念币→邮票→纪念币后，纪念币正面磨损的“严重”选择应保留，评分按 70−12=58 重算（不再回到满分）。"
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

  console.log("==== antiques calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
