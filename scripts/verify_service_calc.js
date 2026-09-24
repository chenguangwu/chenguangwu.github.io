#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "service/complaint-analysis",
  "inputs": {
    "keywords": "物流:配送,快递,发货,慢,延迟,到货;质量:质量,坏了,破损,缺陷,次品;服务:态度,客服,不理, rude,敷衍;价格:贵,涨价,价格,收费,乱收费;售后:退款,退货,售后,维修,保修_X",
    "complaintText": ""
  },
  "expect": [
    "保修_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "service/csat-score",
  "inputs": {
    "s5": "120",
    "s4": "60",
    "s3": "20",
    "s2": "10",
    "s1": "6"
  },
  "clicks": ["calc()"],
  "expect": [
    "83.3% CSAT",
    "4.29 平均星级",
    "216 总评价数"
  ],
  "ref": "总评价数=120+60+20+10+6=216；CSAT=(120+60)/216=83.33%；"
     + "平均星级=(600+240+60+20+6)/216=4.287→4.29；NPS=(120−16)/216=48.1→48。"
     + "原 45/30/12/8/5 为默认态。等级词「良好」两态同现，不入断言。"
},
{
  "slug": "service/response-time",
  "inputs": {
    "slaTarget": "45"
  },
  "expect": [
    "100.0%"
  ],
  "ref": "auto-restore"
},
{
  "slug": "service/script-template",
  "inputs": {},
  "expect": [
    "实在不好意思让您久等了"
  ],
  "ref": "auto-restore(default)"
},
{
  "slug": "service/ticket-priority",
  "clicks": ["tickets=[{name:'支付页面报错',urgency:5,importance:4},{name:'发票开具咨询',urgency:2,importance:3},{name:'账号无法登录',urgency:4,importance:5}];render()"],
  "expect": [
    "1. 支付页面报错",
    "紧急度：5/5 · 重要度：4/5 · 最高优先 20",
    "发票开具咨询"
  ],
  "ref": "顶层数组 tickets 注入 3 条：score = urgency × importance ⇒ 支付页面报错 5×4 = 20（并列最高、排序取其先）、账号无法登录 4×5 = 20、发票开具咨询 2×3 = 6。默认态为源码内置 6 条工单（系统宕机 5/5、25 分），三串均不命中。"
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
  console.log("==== service calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
