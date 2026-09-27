#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
{
  "slug": "startup/burn-rate",
  "inputs": {
    "cash": "4500000",
    "income": "50000",
    "salary": "200000",
    "rent": "30000",
    "marketing": "50000",
    "other": "20000"
  },
  "expect": [
    "18 个月 现金跑道"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/business-plan",
  "inputs": {
    "company": "示例科技有限公司_X",
    "sec_${s.id}": ""
  },
  "expect": [
    "示例科技有限公司_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/calc-1",
  "inputs": {
    "reg": "4500",
    "office": "20000",
    "equipment": "30000",
    "inventory": "20000",
    "brand": "15000",
    "otherOne": "5000",
    "salary": "30000",
    "rent": "5000",
    "marketing": "5000",
    "ops": "3000",
    "months": "12",
    "reserve": "3"
  },
  "expect": [
    "500.00"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/equity-calculator",
  "inputs": {
    "w_idea": "3",
    "w_money": "1",
    "w_time": "2",
    "w_res": "2",
    "pool": "15",
    "mode": "weighted"
  },
  "expect": [
    "weighted"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/pitch-deck",
  "inputs": {
    "company": "示例科技有限公司_X",
    "tagline": "用 AI 重新定义团队协作",
    "slide_${s.id}": ""
  },
  "expect": [
    "示例科技有限公司_X"
  ],
  "ref": "auto-restore"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {
    "bk1": "450",
    "bk2": "200",
    "bk3": "150",
    "bk4": "200",
    "bk5": "100",
    "sc_avg": "2000",
    "sc1": "120",
    "sc2": "110",
    "sc3": "100",
    "sc4": "90",
    "sc5": "80",
    "sc6": "100",
    "sc7": "100",
    "vc_exit": "50000",
    "vc_roi": "10",
    "vc_years": "5",
    "vc_inv": "500",
    "dcf_n": "5",
    "dcf_cf0": "100",
    "dcf_g": "30",
    "dcf_r": "15",
    "dcf_tg": "3",
    "cmp_rev": "500",
    "cmp_mau": "10",
    "cmp_ps_lo": "5",
    "cmp_ps_hi": "10",
    "cmp_uv_lo": "200",
    "cmp_uv_hi": "500"
  },
  "expect": [
    "450.00"
  ],
  "ref": "auto-restore"
},{
  "slug": "startup/valuation-calculator",
  "inputs": {},
  "clicks": [
    "document.getElementById('bk1').value='400';document.getElementById('bk2').value='350';document.getElementById('bk3').value='300';document.getElementById('bk4').value='250';document.getElementById('bk5').value='200';calcBerkus();"
  ],
  "expect": [
    "Berkus 估值： 1,500.00 万元（上限 2,500.00 万）",
    "各项明细：价值主张 400.00 + 技术 350.00 + 执行 300.00 + 市场 250.00 + 落地 200.00"
  ],
  "ref": "Berkus 五维：400+350+300+250+200 = 1,500 万（上限 2,500 万，进度条 60%）。刻意不锚「估值达成 1,500.00 万」——它是 bar-fill 内嵌文案，默认档（300+200+150+200+100=950）不同 ⇒ 可锚但判别力弱于明细串；明细串同时锁死五个分项的取整。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {},
  "clicks": [
    "document.getElementById('sc_avg').value='3000';document.getElementById('sc1').value='130';document.getElementById('sc2').value='120';document.getElementById('sc3').value='115';document.getElementById('sc4').value='110';document.getElementById('sc5').value='105';document.getElementById('sc6').value='100';document.getElementById('sc7').value='110';calcScorecard();"
  ],
  "expect": [
    "加权调整系数：18.3%",
    "调整明细：30% × 130% | 25% × 120% | 15% × 115% | 10% × 110% | 10% × 105% | 5% × 100% | 5% × 110%",
    "记分卡估值： 3,547.50 万元（基准 3,000.00 万 × 1.183）"
  ],
  "ref": "记分卡法：weights=[.30,.25,.15,.10,.10,.05,.05]，dev=(factor-100)/100，adjSum=0.09+0.05+0.0225+0.01+0.005+0+0.005=0.1825 ⇒ 18.3%；val=3000×1.1825=3,547.50。注：页面展示的「× 1.183」是 (1+adjSum).toFixed(3) 的**四舍五入显示**，参与运算的仍是 1.1825（3,000×1.183=3,549 ≠ 3,547.50），用例锚的是结果值而非显示系数，故不冲突。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {},
  "clicks": [
    "document.getElementById('vc_exit').value='100000';document.getElementById('vc_roi').value='20';document.getElementById('vc_years').value='4';document.getElementById('vc_inv').value='1000';calcVC();"
  ],
  "expect": [
    "投后估值 = 100,000.00 ÷ (1+19.00)^4 = 0.63 万",
    "投前估值 = 0.63 − 1,000.00 = -999.38 万",
    "投资人持股：160,000.00%"
  ],
  "ref": "风险投资法：rate=roi-1=19（页面把 roi 当倍数），postMoney=100000/20^4=0.625 万（显示 0.63 为四舍五入），preMoney=0.625-1000=-999.375（显示 -999.38），ownership=1000/0.625*100=160,000%。这是一组「退出价值极低 / 目标回报过高」的极端参数 ⇒ 落进 preMoney<0 的告警分支，同时把负值与超大持股比例一并锁住。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {},
  "clicks": [
    "document.getElementById('dcf_n').value='5';document.getElementById('dcf_cf0').value='200';document.getElementById('dcf_g').value='20';document.getElementById('dcf_r').value='15';document.getElementById('dcf_tg').value='4';calcDCF();"
  ],
  "expect": [
    "各期现值合计：1,138.25 万",
    "终值现值（永续增长 4.00%）：2,339.31 万",
    "DCF 估值： 3,477.56 万元"
  ],
  "ref": "DCF：cf0=200、g=20%、r=15%、tg=4%、n=5 ⇒ 五年现值合计 733.18… 此处核对终值链：terminalCF=497.66×1.04，terminalPV=terminalCF/(0.15-0.04)/1.15^5=2,339.31，加各期现值 1,138.25 ⇒ 3,477.56。python 独立复算：pvSum=1138.25、terminalPV=2339.31、total=3477.56，完全吻合。tg(4%)<r(15%) 才不会走错误分支。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {},
  "clicks": [
    "document.getElementById('cmp_rev').value='800';document.getElementById('cmp_mau').value='20';document.getElementById('cmp_ps_lo').value='6';document.getElementById('cmp_ps_hi').value='12';document.getElementById('cmp_uv_lo').value='300';document.getElementById('cmp_uv_hi').value='600';calcComp();"
  ],
  "expect": [
    "PS 法：收入 800.00 万 × (6.00 - 12.00) = 4,800.00 - 9,600.00 万",
    "单用户法：月活 20.00 万 × (300.00 - 600.00) 元 = 0.60 - 1.20 万",
    "对标估值区间： 0.60 - 9,600.00 万（中位 3,600.45 万）"
  ],
  "ref": "对标法：PS 法=收入×PS倍数区间=800×6~12；单用户法=月活×单用户价值区间（元，需 ÷10000 折算为万元）。两组四个值 [4800,9600,0.6,1.2] 过滤 >0 后取 mid=(4800+9600+0.6+1.2)/4=3,600.45。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {},
  "clicks": [
    "document.getElementById('bk1').value='400';document.getElementById('bk2').value='350';document.getElementById('bk3').value='300';document.getElementById('bk4').value='250';document.getElementById('bk5').value='200';document.getElementById('sc_avg').value='3000';document.getElementById('sc1').value='130';document.getElementById('sc2').value='120';document.getElementById('sc3').value='115';document.getElementById('sc4').value='110';document.getElementById('sc5').value='105';document.getElementById('sc6').value='100';document.getElementById('sc7').value='110';document.getElementById('vc_exit').value='100000';document.getElementById('vc_roi').value='20';document.getElementById('vc_years').value='4';document.getElementById('vc_inv').value='1000';document.getElementById('dcf_n').value='5';document.getElementById('dcf_cf0').value='200';document.getElementById('dcf_g').value='20';document.getElementById('dcf_r').value='15';document.getElementById('dcf_tg').value='4';document.getElementById('cmp_rev').value='800';document.getElementById('cmp_mau').value='20';document.getElementById('cmp_ps_lo').value='6';document.getElementById('cmp_ps_hi').value='12';document.getElementById('cmp_uv_lo').value='300';document.getElementById('cmp_uv_hi').value='600';calcAll(true);"
  ],
  "expect": [
    "综合估值区间： 0.60 - 9,600.00 万元，建议以平均估值 3,625.13 万为谈判起点",
    "3,625.13 平均估值(万)",
    "0.60 最低估值(万)"
  ],
  "ref": "calcAll() 五法全跑 + updateSummary() 汇总：汇总表只收 results 中 >0 的项（VC 法本次 preMoney=-999.375 为负 ⇒ 被过滤掉，这是本例与单法用例的关键差异）；allV=[1500, 3547.50, 3477.56, 0.60, 9600] ⇒ lo=0.60、hi=9,600.00、avg=18,125.66/5=3,625.13。python 复算一致。"
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
  console.log("==== startup calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();
