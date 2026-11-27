#!/usr/bin node
"use strict";
const fs = require("fs");
globalThis.__tbFs = fs;
globalThis.__tbRoot = process.cwd();
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
    "ref": "⚠ 输入回显（结构性不可修）：注入态与默认态输出逐字节相同，无依赖输入的派生量可锚，维持原断言不制造逃生。 [auto-restore]"
},
{
  "slug": "startup/calc-1",
  "inputs": {
    "reg": "4500", "office": "20000", "equipment": "30000", "inventory": "20000",
    "brand": "15000", "otherOne": "5000", "salary": "30000", "rent": "5000",
    "marketing": "5000", "ops": "3000", "months": "12", "reserve": "3"
  },
  "expect": ["739,500.00", "645,000.00", "15.0"],
  "ref": "一次性 94,500 + 运营 516,000 + 储备 129,000 = 739,500；期初支付一次性后剩 645,000；跑道 645,000÷43,000=15.0，不再把一次性重复计入可支配现金。"
},
{
  "slug": "startup/calc-1",
  "inputs": { "reg": "", "months": "12", "reserve": "3" },
  "expect": ["留空不按 0"],
  "ref": "单项留空必须报缺项，不得按 0 参与合计。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": { "bk1": "400", "bk2": "350", "bk3": "300", "bk4": "250", "bk5": "200" },
  "clicks": ["calcBerkus()"],
  "expect": [
    "Berkus 估值：1,500.00 万元（上限 2,500.00 万）",
    "各项明细：价值主张 400.00 + 技术 350.00 + 执行 300.00 + 市场 250.00 + 落地 200.00"
  ],
  "ref": "Berkus 五维 400+350+300+250+200=1,500 万。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {
    "sc_avg": "3000", "sc1": "130", "sc2": "120", "sc3": "115", "sc4": "110",
    "sc5": "105", "sc6": "100", "sc7": "110"
  },
  "clicks": ["calcScorecard()"],
  "expect": [
    "加权调整系数：18.3%",
    "记分卡估值：3,547.50 万元（基准 3,000.00 万 × 1.183）"
  ],
  "ref": "adjSum=0.1825，3000×1.1825=3,547.50。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": { "vc_exit": "100000", "vc_roi": "20", "vc_years": "4", "vc_inv": "1000" },
  "clicks": ["document.getElementById('vc_mode').value='total';calcVC();"],
  "expect": [
    "回报口径：投资期总回报 20 倍",
    "投后估值 = 100,000.00 ÷ 20.00 = 5,000.00 万",
    "投前估值 = 5,000.00 − 1,000.00 = 4,000.00 万",
    "投资人持股：20.00%"
  ],
  "ref": "总回报倍数口径：100000÷20=5000，投前 4000，持股 1000/5000=20%。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": { "vc_exit": "100000", "vc_roi": "20", "vc_years": "4", "vc_inv": "1000" },
  "clicks": ["document.getElementById('vc_mode').value='annual';calcVC();"],
  "expect": [
    "回报口径：年化 20% × 4 年",
    "投后估值 = 100,000.00 ÷ (1+0.2000)^4 = 48,225.31 万",
    "投前估值 = 48,225.31 − 1,000.00 = 47,225.31 万",
    "投资人持股：2.07%"
  ],
  "ref": "年化口径：100000/1.2^4=48,225.31，投前 47,225.31，持股 2.07%。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": { "dcf_n": "5", "dcf_cf0": "200", "dcf_g": "20", "dcf_r": "15", "dcf_tg": "4" },
  "clicks": ["calcDCF()"],
  "expect": [
    "各期现值合计：1,138.25 万",
    "终值现值（永续增长 4.00%）：2,339.31 万",
    "DCF 估值：3,477.56 万元"
  ],
  "ref": "cf0=200、g=20%、r=15%、tg=4%、n=5，node 独立复算一致。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {
    "cmp_rev": "800", "cmp_mau": "20", "cmp_ps_lo": "6", "cmp_ps_hi": "12",
    "cmp_uv_lo": "300", "cmp_uv_hi": "600"
  },
  "clicks": ["calcComp()"],
  "expect": [
    "PS 法：收入 800.00 万 × (6.00 - 12.00) = 4,800.00 - 9,600.00 万",
    "单用户法：月活 20.00 万 × (300.00 - 600.00) 元 = 6,000.00 - 12,000.00 万",
    "对标端点区间：4,800.00 - 12,000.00 万（区间中点 8,400.00 万）"
  ],
  "ref": "区间两端取各法最低/最高端点 4800/12000，中点=(4800+12000)/2=8400，不是四端点平均。"
},
{
  "slug": "startup/valuation-calculator",
  "inputs": {
    "bk1": "400", "bk2": "350", "bk3": "300", "bk4": "250", "bk5": "200",
    "sc_avg": "3000", "sc1": "130", "sc2": "120", "sc3": "115", "sc4": "110",
    "sc5": "105", "sc6": "100", "sc7": "110", "vc_exit": "100000", "vc_roi": "20",
    "vc_years": "4", "vc_inv": "1000", "dcf_n": "5", "dcf_cf0": "200", "dcf_g": "20",
    "dcf_r": "15", "dcf_tg": "4", "cmp_rev": "800", "cmp_mau": "20",
    "cmp_ps_lo": "6", "cmp_ps_hi": "12", "cmp_uv_lo": "300", "cmp_uv_hi": "600"
  },
  "clicks": ["document.getElementById('vc_mode').value='annual';calcAll(true);"],
  "expect": [
    "综合端点区间：1,500.00 - 47,225.31 万元",
    "端点平均 11,564.34 万",
    "1,500.00 最低估值(万)"
  ],
  "ref": "五法值 [1500,3547.5,47225.31,3477.56,8400]，min1500/max47225.31/端点平均11564.34；对标按区间中点计一票。"
},
{
  "slug": "startup/burn-rate",
  "inputs": {
    "cash": "100000",
    "income": "0",
    "salary": "175000",
    "rent": "0",
    "marketing": "0",
    "other": "0"
  },
  "expect": [
    "约 17 天后",
    "0.57 个月"
  ],
  "ref": "BS-N4：现金 10 万、月净消耗 17.5 万 ⇒ runway=0.5714 个月 <1 ⇒ 不再把耗尽日显示为当天，按天给出 round(0.5714×30)=17 天后；跑道值 0.57 个月。默认参数（runway=18）不含这两个串。"
},
{
  "slug": "startup/burn-rate",
  "inputs": {},
  "clicks": [
    "document.getElementById('result').innerHTML='clamp:'+(function(d){return d.getFullYear()+'-'+(d.getMonth()+1)+'-'+d.getDate();})(addMonthsClamped(new Date(2026,0,31),1));"
  ],
  "expect": [
    "clamp:2026-2-28"
  ],
  "ref": "BS-N4 月末 clamp：1 月 31 日 + 1 个月应落在 2 月 28 日（2026 非闰年），旧 setMonth 会溢出到 3 月 3 日。直接调用页内 addMonthsClamped 验证。"
},
{
  "slug": "startup/equity-calculator",
  "inputs": {
    "w_idea": "1", "w_money": "1", "w_time": "1", "w_res": "1",
    "f1name": "甲", "f1idea": "9", "f1money": "0", "f1time": "0", "f1res": "0",
    "f2name": "乙", "f2idea": "3", "f2money": "0", "f2time": "0", "f2res": "0",
    "f3name": "丙", "f3idea": "3", "f3money": "0", "f3time": "0", "f3res": "0"
  },
  "clicks": ["calc()"],
  "expect": ["甲 60.00%", "乙 20.00%", "丙 20.00%", "创始团队合计 100.00%"],
  "ref": "页面原用 appendChild + innerHTML 生成无 id 的创始人行，桩不建动态行 ⇒ 零覆盖。已给行内输入加稳定 id（f{n}name/idea/money/time/res），readFounders 改为按 id 读取（删除行仍靠 getElementById 判空跳过），行为不变。实跑值：权重全 1，三位创始人创意分 9/3/3 ⇒ 总分 15，持股 9/15=60.00%、3/15=20.00%、20.00%，创始团队合计 100.00%（weighted 模式无期权池）；甲 60% 触发「相对控制权（≥51%）」。旧期望：无用例（零覆盖）。新期望：上列四条；默认态为 张三/李四/王五（权重 3/1/2/2，创意 8/5/3）⇒ 均为其他百分比，四条均不命中。"
},
{
  "slug": "startup/equity-calculator",
  "inputs": {
    "w_idea": "1", "w_money": "1", "w_time": "1", "w_res": "1",
    "f1name": "甲", "f1idea": "9", "f1money": "0", "f1time": "0", "f1res": "0",
    "f2name": "乙", "f2idea": "3", "f2money": "0", "f2time": "0", "f2res": "0",
    "f3name": "丙", "f3idea": "3", "f3money": "0", "f3time": "0", "f3res": "0"
  },
  "clicks": [
    "calc();var t=equityReportText();var R=document.getElementById('result');R.innerHTML+=' <b>EQCOPY '+((t.indexOf('【股权变动历程】')>=0&&t.indexOf('甲：持股 60.00%')>=0)?'OK':'BAD')+'</b>';"
  ],
  "expect": ["EQCOPY OK"],
  "ref": "融资稀释复制修复：复制文本改由 `__equityLast`（calc 的最终表 + capHistory）生成，不再重新按 hash 比例算融资前股权，并新增「股权变动历程」。旧实现文本无该标题、且融资模式下缺投资人行。默认态未 calc 时 `equityReportText()` 为空，不命中。"
}
,
{
  "slug": "startup/equity-calculator",
  "clicks": ["(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+'/' +'tools/startup/equity-calculator.html','utf8');var i=h.indexOf('f.idea < 0');var s=i>=0?h.slice(i,i+700):'';var ok=s.indexOf(\"getElementById('result').innerHTML\")>=0&&s.indexOf('poolPct < 0 || poolPct >= 100')>=0&&(s.match(/getElementById\\('result'\\).innerHTML/g)||[]).length>=2;document.getElementById('__tbProbe').textContent='EQCLR '+(ok?'OK':'BAD');})();"],
  "expect": ["EQCLR OK"],
  "ref": "第1345批 equity-calculator 贡献负值/期权池越界两早退原只 showToast，不清 #result(股权表+变动历程)；对齐同函数另两分支写法补清空。"
},
{ slug:"startup/burn-rate", inputs:{"cash":"","income":"","salary":"","rent":"","marketing":"","other":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
{
  "slug": "startup/burn-rate",
  "inputs": {"cash":"100000","income":"","salary":"175000","rent":"0","marketing":"0","other":"0"},
  "expect": ["空值不按 0 处理"],
  "ref": "第828批：部分字段留空时旧 getInputs 用 `||0` 当 0，月收入空被当成 0 仍算出跑道。现在空值返回 NaN 并阻断，提示明确要求非负数且空值不按 0 处理。"
},
{
  "slug": "startup/burn-rate",
  "inputs": {"cash":"100000","income":"100000","salary":"100000","rent":"0","marketing":"0","other":"0"},
  "expect": ["收支持平", "不能推断已盈利"],
  "ref": "第828批：净消耗恰为 0 时旧分支按 `<=0` 归入「已有正向现金流/已盈利」。现在单独判收支持平，明确现金不增不减且不能推断盈利。"
},
{
  "slug": "startup/burn-rate",
  "inputs": {"cash":"190000","income":"0","salary":"100000","rent":"0","marketing":"0","other":"0"},
  "expect": ["1.9 个月", "整月+小数月×30天"],
  "ref": "第828批：跑道 1.9 个月旧实现只加 floor(1.9)=1 个月，耗尽日期提前 0.9 个月。现在整月 + 小数月×30 天近似并标注口径；探针断 1.9 个月与近似说明。"
}

];
function equityFundingStaticChecks() {
  const h = require("fs").readFileSync(require("path").join(__dirname, "..", "tools", "startup", "equity-calculator.html"), "utf8");
  return [{
    name: "融资轮统一校验后再应用",
    ok: h.includes("const parsed = [];") && h.includes("let roundError") && h.includes("if(roundError){") && h.includes("parsed.forEach") && !/r-amount[^;]{0,60}\|\| 0/.test(h),
  }];
}
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

  const stat = equityFundingStaticChecks();
  const staticFails = stat.filter((s) => !s.ok);
  for (const x of staticFails) console.log("❌ [static] " + x.name);
  console.log("==== startup calc " + pass + "/" + cases.length + " ====");
  if (fails.length || staticFails.length) process.exit(1);
}
if (require.main === module) main();
