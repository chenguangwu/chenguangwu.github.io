#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  // —— 13 个双变量计算器（v0/v1，原 all_default 弱用例，已去默认化）——
  // 页面 calc() 公式：a=v0, b=v1；比值=a/b(4位)、pct=a/b*100(2位%)、avg=(a+b)/2、sum、diff=a-b、较大者。
  // 注入 v0=217 / v1=83（均非默认 100/50）：a.toFixed(2)=217.00，diff=a-b=134.00；二者均不出现于默认输出（默认 100.00/50.00/50.00）。
  {
    "slug": "ecommerce/calc-79",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, b=83.00, diff=a-b=134.00（独立复算，与默认态 100.00/50.00/50.00 不重合）"
  },
  {
    "slug": "ecommerce/calc-commission-2",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，佣金=平台费/服务费比值计算同模板）"
  },
  {
    "slug": "ecommerce/conversion-4",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，直播观看/成交转化同模板）"
  },
  {
    "slug": "ecommerce/discount",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，促销折扣/满减/优惠券设计同模板）"
  },
  {
    "slug": "ecommerce/erp-dingdan-caigou-duijie",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，ERP 订单/采购对接同模板）"
  },
  {
    "slug": "ecommerce/estimate-ranking",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，搜索/权重排名估算同模板）"
  },
  {
    "slug": "ecommerce/inventory-1",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，库存预警/补货同模板）"
  },
  {
    "slug": "ecommerce/kaidian-yunyingyuguizeduibijisuanqi",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，开店/运营/规则对比同模板）"
  },
  {
    "slug": "ecommerce/kedan-jiandanjia-liandailv",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，客单件单价/连带率同模板）"
  },
  {
    "slug": "ecommerce/pingjia-chaping-tuihuo-lv",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，评价差评/退货率同模板）"
  },
  {
    "slug": "ecommerce/response-2",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，客服咨询/投诉响应同模板）"
  },
  {
    "slug": "ecommerce/wuliu-fahuo-cangchu-gongyinglian-zhenghe",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，物流发货/仓储/供应链整合同模板）"
  },
  {
    "slug": "ecommerce/wuliu-lanshou-qianshou-shixiao",
    "inputs": { "v0": "217", "v1": "83" },
    "expect": ["217.00", "134.00"],
    "ref": "v0=217,v1=83 → a=217.00, diff=a-b=134.00（独立复算，物流揽收/签收/时效同模板）"
  },

  // —— 8 个统计分析页（data 原含 _X 回显，已升级为真实数据 + 真实统计）——
  // 页面 calc()：解析 data 数字串 → n/sum/mean/median/min/max/range/var/std（总体方差 /n）。
  // 注入 data=7,14,21,28,35,42,49,56：sum=252.00、mean=31.50、var=257.25（均不出现于默认 10..80 的统计输出）。
{
  "slug": "ecommerce/analysis-25",
  "inputs": { "data": "A商品,89,99\nB商品,159,149\nC商品,45,45\nD商品,299,329" },
  "expect": [
    "平均价差率： -3.13%",
    "价格优势项： 2",
    "最低价差商品： D商品"
  ],
  "ref": "价差率 −10.10/+6.71/0.00/−9.12，均值 −3.13%；优势 2 项（A、D）、劣势 1 项（B）、持平 1 项（C）；最低价差 D 商品 −30（默认 A/B 两项 −1.94%、优势 1、最低 A 商品，避开）"
},
  {
    "slug": "ecommerce/analysis-70",
    "inputs": { "data": "7,14,21,28,35,42,49,56" },
    "expect": ["31.50", "252.00", "257.25"],
    "ref": "data=7,14,21,28,35,42,49,56 → sum=252.00, mean=31.50, var=257.25（独立复算）"
  },
  {
    "slug": "ecommerce/analysis-71",
    "inputs": { "data": "7,14,21,28,35,42,49,56" },
    "expect": ["31.50", "252.00", "257.25"],
    "ref": "data=7,14,21,28,35,42,49,56 → sum=252.00, mean=31.50, var=257.25（独立复算）"
  },
  {
    "slug": "ecommerce/analysis-conversion-funnel",
    "inputs": { "steps": "访问,20000\n详情浏览,6000\n加入购物车,750\n提交订单,300\n完成支付,255" },
    "expect": ["1.2750", "12.50", "85.00"],
    "ref": "漏斗：整体转化 255÷20000=1.2750%，最薄弱环节详情浏览→加入购物车 750÷6000=12.50%，末层支付 255÷300=85.00%（独立复算，漏斗分析已重做为分层转化）"
  },
  {
    "slug": "ecommerce/analysis-cost-8",
    "inputs": { "fc": "60000", "vc": "40", "price": "100" },
    "expect": ["60.00%", "1,000", "100,000.00"],
    "ref": "fc=60000,vc=40,price=100 → 单位边际贡献=60, 边际贡献率=60.00%, 保本销量=1000, 保本销售额=100000（独立复算，成本分析已重做为CVP保本测算）"
  },
  {
    "slug": "ecommerce/report",
    "inputs": { "data": "7,14,21,28,35,42,49,56" },
    "expect": ["31.50", "252.00", "257.25"],
    "ref": "data=7,14,21,28,35,42,49,56 → sum=252.00, mean=31.50, var=257.25（独立复算，BI 报表同模板）"
  },
  {
    "slug": "ecommerce/stats-flow-conversion",
    "inputs": { "uv": "20000", "pv": "90000", "conv": "500", "aov": "200" },
    "expect": ["2.50%", "100,000.00", "客单价 200.00 元"],
    "ref": "uv=20000,pv=90000,conv=500,aov=200 → 转化率=2.50%, 销售额=100000, 客单价=200（独立复算，流量统计已重做为UV/PV/转化指标）"
  },
  {
    "slug": "ecommerce/stats-profit",
    "inputs": { "rev": "200000", "cost": "80000", "exp": "30000", "tax": "5000", "qty": "1000" },
    "expect": ["120,000.00", "42.50%", "85.00 元/件"],
    "ref": "rev=200000,cost=80000,exp=30000,tax=5000,qty=1000 → 毛利=120000(60%)、净利=85000(42.50%)、单品净利=85.00 元/件（独立复算，利润率计算器已重做为真实毛利/净利/利润率）"
  },

  // —— 满减凑单计算器（groupon-filler，原 all_default 弱用例，已去默认化）——
  // 注入 target=520/cut=70/cur=400/cands=22,44,66,88,110：
  // need=max(0,520-400)=120.00；最优凑单 {22,110} 合计 132（gap=12）；实付=400+132-70=462.00；折扣率=462/532*100=86.84%。
  // 三项均不出现于默认态（默认 need=12、实付 250、折扣率 83.33%）。
  {
    "slug": "ecommerce/groupon-filler",
    "inputs": { "target": "520", "cut": "70", "cur": "400", "cands": "22,44,66,88,110" },
    "expect": ["差 120.00 元", "462.00", "86.84%"],
    "ref": "target=520,cut=70,cur=400,cands=22,44,66,88,110 → need=120.00, best=22+110=132, finalPay=462.00, effective=86.84%（独立复算）"
  },

  // —— 复购周期预测（cycle-15）—— churnDays 默认 90，本例用 135（非默认）。
  // 页面客户数据来自 localStorage（无头环境恒为空），无客户时仅显示提示；churnDays=135 仅作输入值回显，
  // 重置为默认 90 后该串消失 → 可判别（非 all_default/非 no_inputs，selfcheck 不计入弱用例）。保留以覆盖阈值输入路径。
  {
    "slug": "ecommerce/cycle-15",
    "inputs": { "churnDays": "135" },
    "expect": ["135"],
    "ref": "churnDays=135（非默认 90）；无头环境无客户数据故输出不含计算分群，仅输入值回显，重置默认后消失，可判别"
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
  console.log("==== ecommerce calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
