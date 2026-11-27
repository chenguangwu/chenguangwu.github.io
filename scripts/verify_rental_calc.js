#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "rental/assessor-24",
  "inputs": {"income":"12003","rent":"4000","workYears":"5","creditScore":"700"},
  "clicks": ["calc();"],
  "expect": ["33.3%"],
  "ref": "2026-11-28 第1138批：输出租金收入比与资料核对进度，不再评级/押金/拒租。12003/4000=33.3%，默认 0/6 项核对。"
},
{
  "slug": "rental/generator-32",
  "inputs": {"partyA":"甲","partyB":"乙","addr":"某路1号","area":"60","start":"2026-01-01","end":"2026-12-31","rent":"3000","depositMonths":"1","payment":"monthly"},
  "clicks": ["gen();"],
  "expect": ["房屋租赁合同（草稿）"],
  "ref": "2026-11-28 第1138批：核心条款固定顺序输出，不再随机抽取。断言草稿标题、双方信息与租金条款同时存在。"
},
{
  "slug": "rental/recommender-5",
  "inputs": {"people":"3","devices":"6","usage":"daily","area":"90"},
  "clicks": ["gen();"],
  "expect": ["200–300 Mbps"],
  "ref": "2026-11-28 第1138批：固定规则推荐。3 人/6 设备/日常用途/90㎡ 估算 110 Mbps，推荐 200–300 Mbps 与双路由 mesh。"
},
{
  "slug": "rental/reminder-4",
  "inputs": {"rAddress":"测试地址","rTenant":"测试租客","rRent":"3003","rStart":"2026-01-01","rEnd":"2026-06-30"},
  "clicks": ["addLease();"],
  "expect": ["¥3,003"],
  "ref": "2026-11-28 第1138批：新增租约后列表按本地日期渲染，显示租金 3003 与地址。"
},
{
  "slug": "rental/rental-yield",
  "inputs": {"price":"1200003","rent":"4500","cost":"15000","vacancy":"1"},
  "clicks": ["calc();"],
  "expect": ["34.8 年"],
  "ref": "2026-11-28 第1138批：空置 1 月单独扣损失，毛 4.50%、净 2.88%、静态回本约 34.8 年。"
},
{
  "slug": "rental/calc-commission-1",
  "inputs": {"amount":"300","rate":"2","serviceFee":"0","customPct":"50"},
  "expect": ["60,000 佣金"],
  "ref": "auto-restore"
},
{
  "slug": "rental/cycle-11",
  "inputs": {},
  "clicks": ["switchMeter('water');"],
  "expect": ["单价（元/吨）"],
  "ref": "clicks 注入：switchMeter('water') 将当前表由电切水，费率区显示「单价（元/吨）」。"
},
{
  "slug": "rental/rent-2",
  "inputs": {"targetArea":"135","growth":"2","rentA":"4500","areaA":"85","adjA":"-15","wA":"1","rentB":"5200","areaB":"95","adjB":"2","wB":"1","rentC":"4800","areaC":"88","adjC":"0","wC":"1"},
  "clicks": ["calc();"],
  "expect": ["样本：3"],
  "ref": "2026-11-28 第1138批：目标面积必填；三个有效案例输出建议租金，并显示样本数与口径提示。"
},
{
  "slug": "rental/rent-2",
  "inputs": {"targetArea":"90","growth":"2","rentA":"4500","areaA":"85","adjA":"-150","wA":"1","rentB":"5200","areaB":"95","adjB":"2","wB":"1","rentC":"4800","areaC":"88","adjC":"0","wC":"1"},
  "clicks": ["calc();"],
  "expect": ["综合修正须在 −50%~+50% 之间"],
  "ref": "综合修正 −150% 越界，逐项提示并阻止输出修正表。"
},
{
  "slug": "rental/rent-2",
  "inputs": {"targetArea":"90","growth":"2","rentA":"4500","areaA":"85","adjA":"-3","wA":"1","rentB":"5200","areaB":"95","adjB":"60","wB":"1","rentC":"4800","areaC":"88","adjC":"0","wC":"1"},
  "clicks": ["calc();"],
  "expect": ["综合修正须在 −50%~+50% 之间"],
  "ref": "案例 B 综合修正 +60% 越上界，逐项提示并阻止输出修正表。"
},
{
  "slug": "rental/calc-commission-1",
  "inputs": {"amount":"","rate":"2"},
  "expect": ["请填写金额（万元）与佣金比例（%）后再计算。"],
  "ref": "空态守卫：清空成交金额后只给填写提示，不渲染 0 元结论。serviceFee 默认 0 属合法值。"
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

  console.log("==== rental calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
