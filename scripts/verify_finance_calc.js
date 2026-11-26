#!/usr/bin/env node
/**
 * finance 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）；
 * 与之区别仅在于用例集：finance 用校验位算法（Luhn / mod-11 / mod-97 / Verhoeff 等）
 * 与金融公式（单利、贷款月供、ROI、NPV、盈亏平衡、增值税）的独立复算。
 *
 * 用法：
 *   node scripts/verify_finance_calc.js                        # 跑全部用例
 *   node scripts/verify_finance_calc.js credit-card-luhn tax   # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化/运行日期
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（校验位算法 / 标准公式 / 独立复算），必填，便于复核
 *
 * 期望值一律由独立实现或 python 复算得出，不凭记忆。反例（无效号）同样纳入：
 * 验证「算法对无效输入给出正确判定」与验证正例同等重要。
 * 注意：依赖图表（canvas）或依赖「今天」的工具刻意不纳入，否则门禁会随环境失败。
 */
const fs = require("fs");
globalThis.__tbFs = fs;
globalThis.__tbRoot = process.cwd();
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  {
    slug: "finance/word-search",
    inputs: {},
    clicks: ["var s=String(__tbn),g=String(__tbnRecordOnce),rs=String(render);document.getElementById('__tbProbe').textContent='WSMECH '+((typeof __tbnCur!=='undefined'&&g.indexOf('__tbnRecorded')>=0&&s.indexOf('var acc=__tbnCur')>=0&&s.indexOf('last.t!==now')>=0&&rs.indexOf('__tbn()')<0)?'OK':'BAD');"],
    expect: ["WSMECH OK"],
    ref: "第134批 F-N165 成绩历史恒 0：旧实现 __tbn 挂在 render 包装上、开局 found 为空记 0，acc 取 found.size，去重 last.v!==acc 让恒 0 只留一条。修复后 acc 取缓存 __tbnCur（endSelect 更新）、去重改 {t,v} 整体比对（last.t!==now）、记录走 __tbnRecordOnce 标志位、render 不再自动记成绩。四条同时命中才 OK；旧源码字符串均不满足 ⇒ 强判别、零逃生（默认态与注入态同为空 inputs，但锁的是实现机制，旧源码必 BAD）。"
  },
  {
    slug: "finance/report-1",
    inputs: { inv: "400000", pct: "80", capital: "500000", retained: "200000", premium: "0", profit: "150000", dec: "2" },
    clicks: ["calc()"],
    expect: ["长期股权投资（全额） 400,000.00", "借方 700,000.00 / 贷方 700,000.00 借贷平衡 ✓"],
    ref: "第132批 F-N81 负商誉借贷平衡：旧实现贷方长期股权投资只记 parentShare=560,000（「母公司享有部分」），负商誉另贷 160,000 ⇒ 借 700,000 / 贷 860,000 差 -160,000（=|diff|）。修复后贷方按全额 inv=400,000 冲销，借 700,000 = 贷 400,000+140,000+160,000=700,000，并补合计行。两条分别绑定全额冲销金额与借贷平衡合计；默认 inv=800,000 金额不同、旧源码无合计行且写「享有部分」⇒ 均不命中，零逃生。",
  },
  {
    slug: "finance/report-1",
    inputs: { inv: "900000", pct: "80", capital: "500000", retained: "200000", premium: "0", profit: "150000", dec: "2" },
    clicks: ["calc()"],
    expect: ["长期股权投资（全额） 900,000.00", "借方 1,040,000.00 / 贷方 1,040,000.00 借贷平衡 ✓"],
    ref: "第132批 F-N81 商誉借贷平衡：inv=900000、parentShare=560000 ⇒ 商誉 diff=340000；旧实现借 500000+200000+340000=1,040,000、贷 560000+140000=700000 差 340000=diff。修复后贷方全额 inv=900000+少数 140000=1,040,000=借方，合计行标「借贷平衡 ✓」。绑定注入金额 inv=900000 与平衡合计；默认 inv=800000 不命中、旧源码贷方写 560000 且无合计行 ⇒ 零逃生。",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "1000000", rate: "4.2", years: "0" },
    clicks: ["calc();var s=document.getElementById('summary'),r=document.getElementById('res'),b=document.querySelector('#schedule tbody');document.getElementById('__tbProbe').textContent='C4Y0 '+((!s||!s.innerHTML)&&(!b||!b.innerHTML)&&r&&r.innerHTML.indexOf('贷款期限须为大于 0')>=0?'OK':'BAD');"],
    expect: ["C4Y0 OK"],
    ref: "第129批 F-N70：旧 years=parseInt(...)||1 把 0 兜成 1 年，照常输出 12 期/85,241.31 元月供并留下明细。修复后 0/空/负/非数字字段级拒绝、清 #summary 与 #schedule tbody、#res 写期限须>0 提示。注入 years=0 命中；默认 30 为合法态 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "1000000", rate: "4.2", years: "-5" },
    clicks: ["calc();var s=document.getElementById('summary'),r=document.getElementById('res'),b=document.querySelector('#schedule tbody');document.getElementById('__tbProbe').textContent='C4YNEG '+((!s||!s.innerHTML)&&(!b||!b.innerHTML)&&r&&r.innerHTML.indexOf('贷款期限须为大于 0')>=0&&r.innerHTML.indexOf('-60')<0?'OK':'BAD');"],
    expect: ["C4YNEG OK"],
    ref: "第129批 F-N70：旧负年限产出「-60 期」、-15,006.91 元负月供、空明细却仍显示；修复后负期限走字段级拒绝、清残留、无负期数回显。注入 years=-5 命中；默认 30 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "1000000", rate: "4.2", years: "2.5" },
    clicks: ["calc();var s=document.getElementById('summary');document.getElementById('__tbProbe').textContent='C4YDEC '+((s&&s.innerHTML.indexOf('30 期')>=0&&s.innerHTML.indexOf('24 期')<0)?'OK':'BAD');"],
    expect: ["C4YDEC OK"],
    ref: "第129批 F-N70：旧 parseInt(2.5)=2 截断为 24 期；修复后 parseFloat + Math.round(years*12)=30 期，期数卡片用 n 回显。注入 years=2.5 命中 30 期；默认 30 年=360 期、旧源码=24 期 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/payroll-calculator",
    inputs: { pension: "-1" },
    clicks: ["calc();var g=document.getElementById('statGrid'),t=document.getElementById('tableWrap');document.getElementById('__tbProbe').textContent='PAYCLR '+((!g||!g.innerHTML)&&(!t||!t.innerHTML)&&__payroll_calculatorScore('')===0&&currentResult===null?'OK':'BAD');"],
    expect: ["PAYCLR OK"],
    ref: "第128批 F-N35 拒绝态残留（真机发现）：旧 calc() 的 fail() 只往 #res 写提示就 return，statGrid 汇总卡与 tableWrap 逐期明细仍挂上一次合法方案；且 Score 纯关键词词表，「养老保险比例不能为负数。」不含任何失败词 ⇒ 无效输入被记成通过。修复后 fail() 清两容器 + currentResult=null + monthlyData=[]，Score 改按业务状态判定。注入 pension=-1 命中；默认 pension=8 为合法态 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/payroll-calculator",
    inputs: { threshold: "6000" },
    clicks: ["calc();var cr=currentResult&&currentResult.inputs;var src=String(loadHistory);document.getElementById('__tbProbe').textContent='PAYHIST '+(cr&&cr.threshold==='6000'&&Object.keys(cr).length===16&&src.indexOf('PAYROLL_INPUT_IDS')>=0&&src.indexOf('h.inputs')>=0?'OK':'BAD');"],
    expect: ["PAYHIST OK"],
    ref: "第128批 F-N36：旧版 currentResult 只存 15 个结果字段，loadHistory() 只回填 salary/bonus/city 三项 ⇒ 同名历史在不同比例/基数/扣除下重算出不同个税（真机实测回放结果 != 原结果）。修复后存 16 个输入的完整 inputs 快照并整体回填，旧记录缺 inputs 时回退并在列表标注「按当前参数重算」。注入 threshold=6000 且快照恰 16 键才 OK；默认 5000 或旧源码无 inputs ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/payroll-calculator",
    inputs: { baby: "777" },
    clicks: ["var s=__payrollInputSnap();var src=String(__payroll_calculatorExtras);document.getElementById('__tbProbe').textContent='PAYSNAP '+(Object.keys(s).length===16&&s.baby==='777'&&src.indexOf('keys.length>24')>=0?'OK':'BAD');"],
    expect: ["PAYSNAP OK"],
    ref: "第128批 通用历史快照截断：本页 16 个输入全部影响结果，旧 Extras/Export 两处 keys.length>12 会把 baby/medicalBig/threshold/city 永久挤出历史表与回放。修复放宽到 24。注入 baby=777 才命中；默认 0 或旧源码 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/payroll-calculator",
    inputs: { bonus: "30000" },
    expect: ["年终奖并入综合所得", "更优方式"],
    ref: "年终奖单独/并入两方案对比：bonus>0 时输出两种税额及更优方式；默认 bonus=0 不含该串，强判别。"
  },
  {
    slug: "finance/investment-roi",
    inputs: { cost: "10000", return: "13000", years: "2", unit: "year", discount: "5", annualCash: "" },
    clicks: ["calcSimple()"],
    expect: ["静态回收期（未提供年均现金回流）"],
    ref: "第934批：只填期末终值、未提供各期现金流时不再用 成本/(净利润/年数) 虚构回收期；显示未提供年均回流。默认参数同样不含确定年数。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { cost: "10000", return: "13000", years: "2", unit: "year", discount: "5", annualCash: "5000" },
    clicks: ["calcSimple()"],
    expect: ["静态回收期（按年均现金回流）", "2.00年"],
    ref: "第934批：显式提供年均现金回流 5000 时，回收期 = 10000/5000 = 2.00 年，并标注固定年度现金流假设；默认留空 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { aCost: "10000", aRate: "0", aYears: "5", aAdd: "1000", bCost: "10000", bRate: "0", bYears: "5", bAdd: "1000" },
    clicks: ["switchTab('compare');calcCompare();document.getElementById('aCost').value='-1';calcCompare();var h=String(document.getElementById('compareStats').innerHTML);document.getElementById('__tbProbe').textContent='ROIREJ '+(h.indexOf('须为有效正数')>=0&&h.indexOf('15,000')<0?'OK':'BAD');"],
    expect: ["ROIREJ OK"],
    ref: "第127批 真机发现的真 bug：calcCompare() 对成本/期限 ≤0 是静默 return，既不给提示也不清结果区，上一次合法方案的 15,000 仍挂着，历史却按新输入判 0（同屏自相矛盾、可导出旧报价）。修复为字段级拒绝 + __roiReject 清残留。同一用例内先算合法 0%+追加（15,000）再拒绝；旧源码保留旧结果 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/investment-roi",
    inputs: { aCost: "10000", aRate: "0", aYears: "5", aAdd: "1000", bCost: "10000", bRate: "0", bYears: "5", bAdd: "1000" },
    clicks: ["switchTab('compare');calcCompare();var h=String(document.getElementById('compareStats').innerHTML);document.getElementById('__tbProbe').textContent='ROIZERO '+(h.indexOf('15,000')>=0&&h.indexOf('-100.00%')<0&&h.indexOf('NaN')<0&&h.indexOf('0.00%')>=0&&h.indexOf('持平')>=0?'OK':'BAD');"],
    expect: ["ROIZERO OK"],
    ref: "第127批 F-N33 0% 利率 + 每年追加：旧 calcFV 与绘图 calcFVAt 各写一遍 ((1+r)^t−1)/r，r=0 得 0/0=NaN，fmt 后结果卡显示「-- 方案A终值」与「-100.00% A年化」（比清单记录的整卡替换更隐蔽）。修复抽成 roiFutureValue 统一公式，r=0 走 add*t，并用 expm1/log1p 消除 r→0 的浮点抵消；实测两方案终值均 15,000、资金加权年化均 0.00%、判持平。注入态（0% + 追加 1000）命中；默认态 aRate=8 终值 14,000+ ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/investment-roi",
    inputs: { aCost: "100", aRate: "9", aYears: "2", aAdd: "0", bCost: "100", bRate: "10", bYears: "2", bAdd: "100" },
    clicks: ["switchTab('compare');calcCompare();var h=String(document.getElementById('compareStats').innerHTML);document.getElementById('__tbProbe').textContent='ROIIRR '+(h.indexOf('118.81')>=0&&h.indexOf('352')>=0&&h.indexOf('9.00%')>=0&&h.indexOf('10.00%')>=0&&h.indexOf('8.32%')<0&&h.indexOf('>方案B<')>=0&&h.indexOf('>方案A<')<0?'OK':'BAD');"],
    expect: ["ROIIRR OK"],
    ref: "第127批 F-N34 清单原例：A 100 元 @9%/2 年不追加，B 100 元 @10%/2 年每年追加 100。旧版把 B 的「总收益/累计投入」按 2 年开方得 8.32%，低于 A 的 9.00% ⇒ 误判 A 更优（2026-11-06 复核明确仍待修）。修复按各期投入时点反解资金加权 IRR ⇒ A 9.00% / B 10.00%、终值 118.81 / 352、判 B 更优（结果卡 winner 值为「方案B」）；断言同时排除 8.32% 并要求 winner 不是「方案A」。注入态命中；默认态两方案 10,000 元 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/investment-roi",
    inputs: { aCost: "10000", aRate: "100000", aYears: "5", aAdd: "0", bCost: "10000", bRate: "3", bYears: "5", bAdd: "0" },
    clicks: ["switchTab('compare');calcCompare();var h=String(document.getElementById('compareStats').innerHTML);document.getElementById('__tbProbe').textContent='ROINULL '+(h.indexOf('无法确定')>=0&&h.indexOf('持平')<0&&h.indexOf('NaN')<0?'OK':'BAD');"],
    expect: ["ROINULL OK"],
    ref: "第127批 复核方判据「未检出当无解 → 保守无法确定」：aRate=100000% 时 FV 远超二分区间上界能覆盖的终值，roiMoneyWeightedIrr 端点同号返回 null。修复后判优显示「无法确定」而不是把求解失败当成「持平」或伪造上限；旧累计 ROI 开方版会给出有限年化并判 A ⇒ BAD。注入态命中；默认态 aRate=8 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/investment-roi",
    inputs: { bCost: "5000" },
    clicks: ["switchTab('compare');var src=String(__investment_roiScore)+String(__investment_roiSnap);var f1=typeof __investment_roi_f1,f2=typeof __investment_roi_f2;var okIn=String(document.getElementById('bCost').value)==='5000';document.getElementById('__tbProbe').textContent='ROITAB '+(okIn&&src.indexOf('aCost')>=0&&src.indexOf('.tab-panel.active')>=0&&f1==='function'&&f2==='function'?'OK':'BAD');"],
    expect: ["ROITAB OK"],
    ref: "第127批 机制层防回退：旧版 Extras 只包装 calcSimple，定投/方案对比两个真实入口完全不写历史；Snap 全表抓 17 键再截断到 12，bCost/bRate/bAdd 永远进不了历史；Score 恒读 simple 的 cost/years 与 simpleStats。修复后三个入口均包装、快照收窄到活动 tab、Score 按 tab 业务状态判定。harness stub 不支持复杂选择器与真历史，故锁源码级特征 + 注入值 bCost=5000（注入失败回默认值 10000 ⇒ BAD）。"
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: { downPct: "150" },
    clicks: ["calc();var g=document.getElementById('statGrid'),t=document.getElementById('tableWrap'),r=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='LEASECLR '+((g&&!g.innerHTML)&&(t&&!t.innerHTML)&&r.indexOf('首付比例须在 0–100%')>=0?'OK':'BAD');"],
    expect: ["LEASECLR OK"],
    ref: "第126批 F-N117 拒绝态清空残留：旧版越界时只写错误提示到 #res，汇总卡片 statGrid、逐期明细 tableWrap、图表仍挂着上一次合法方案，同屏自相矛盾。修复后越界分支清空这两个容器并 clearRect 图表。注入 downPct=150 命中；默认合法态两个容器都有内容 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: { downPct: "150" },
    clicks: ["calc();var s0=__lease_payment_calculatorScore('');document.getElementById('downPct').value='0';calc();var s1=__lease_payment_calculatorScore('');document.getElementById('__tbProbe').textContent='LEASESCORE '+(s0===0&&s1===1?'OK':'BAD');"],
    expect: ["LEASESCORE OK"],
    ref: "第126批 F-N117 Score 按业务状态判定：旧 Score 靠关键词词表，「首付比例须在 0–100% 之间」「手续费不能为负」等拒绝提示不含任何失败词 ⇒ 无效输入被记成通过并允许导出。修复后读 calc() 越界分支置的 currentResult===null 直接判 0，合法态仍判 1。同用例内连测两态；默认态 s0 恒为 1 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: { fee: "0" },
    clicks: ["var a=[];['0','5000','20000'].forEach(function(f){document.getElementById('fee').value=f;calc();a.push(currentResult.nominalRate);});document.getElementById('__tbProbe').textContent='LEASEIRR '+(a[0]<a[1]&&a[1]<a[2]&&Math.abs(a[1]-9.48)<0.05?'OK':'BAD');"],
    expect: ["LEASEIRR OK"],
    ref: "第126批 F-N114 防回退：清单复现本金 10 万 / 6% / 36 期，手续费 0/5000/20000。旧版 cashFlows[0] 用 principal+fee 把费用当多借本金，IRR 随费用上升反而下降；修复为净融资额 principal-fee 后实测 6.00% / 9.48% / 21.68% 严格递增（5000 时与清单 node 独立复算 9.48% 一致）。同用例内三态连算；默认 fee=0 单态不产生该探针 ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "4.5", months: "240", monthly: "4000", prepay: "0" },
    clicks: ["calc();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='MPHIGH '+(t.indexOf('提示：填写的月供高于合同应还月供')>=0&&t.indexOf('3163.25')>=0?'OK':'BAD');"],
    expect: ["MPHIGH OK"],
    ref: "第125批 F-N91 高月供提示：旧版 mpWarn 只在 mp 低于应还月供时告警，用户把月供填高时看不出对照口径已变。修复后补带应还月供 3163.25 的中性提示，并明确对照方案按填写月供计算、节省只归因于本次提前还款。注入 monthly=4000（应还 3163.25）命中；默认态不出现该提示 ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "4.5", months: "240", monthly: "4000", prepay: "0" },
    clicks: ["TBKit={util:{isEn:function(){return true;}}};calc();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='MPENCJK '+(t.indexOf('Baseline')>=0&&t.indexOf('：')<0?'OK':'BAD');"],
    expect: ["MPENCJK OK"],
    ref: "第125批 EN 态零 CJK 泄漏：结果区基线行把全角冒号「：」硬编码在 __mpTx 之外，EN 态输出「Baseline …：monthly」泄漏 CJK；低月供告警同样是纯中文。修复后冒号走 __mpTx('：', ': ')、告警双语化。探针注入 TBKit.util.isEn=true 后检查 EN 态结果区出现 Baseline 且无全角冒号；中文默认态不含 Baseline ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "4.5", months: "240", monthly: "3000", prepay: "20000" },
    clicks: ["var __oa=amortizeExact;amortizeExact=function(){return {months:10,total:1,interest:0};};calc();var t=String(document.getElementById('result').innerHTML);amortizeExact=__oa;document.getElementById('__tbProbe').textContent='MPNEG '+(t.indexOf('var(--danger)')>=0&&t.indexOf('出现负节省')>=0?'OK':'BAD');"],
    expect: ["MPNEG OK"],
    ref: "第125批 F-N92 负节省不得标绿：旧版节省行恒 var(--success)，负节省会当收益展示且无说明。修复后按 __saveNum 正负切换 var(--danger) 并追加「出现负节省」提示。真实输入下节省恒非负，故探针临时把 amortizeExact 替成极小 total 构造负节省边界（属合法边界构造，不改页面实现）；默认态无 danger/负节省文案 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "0", months: "240", monthly: "3000", prepay: "0" },
    clicks: ["calc();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='MPZERO '+(t.indexOf('总利息 <strong>0.00</strong> 元')>=0&&t.indexOf('220,000')<0&&t.indexOf('较对照方案节省（元）')>=0?'OK':'BAD');"],
    expect: ["MPZERO OK"],
    ref: "第125批 F-N91/F-N93 0% 利率防回退：清单复现 50 万 / 0% / 240 期 / 月供 3000 / 提前还款 0，旧版输出「原方案总利息 220,000.00」并凭空产生等额节省；修复后基线为逐期精确摊还，总利息 0.00、两方案节省 0.00、期数整数 167。探针读 innerHTML（harness stub 的 innerHTML 不派生 textContent）；默认 4.5% 态总利息非 0 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "0", months: "240", monthly: "3000", prepay: "0" },
    clicks: ["var n=remainingMonths(500000,0,3000);document.getElementById('__tbProbe').textContent='MPRM0 '+(n===167?'OK':'BAD');"],
    expect: ["MPRM0 OK"],
    ref: "第125批 F-N93 0 利率期数取整：清单要求 0 利率分支返回整数期（500000/3000 ⇒ 167 期，末期不足额），旧版 return p/pmt 得 166.666…。本函数现已不参与结论区（结论统一走 amortizeExact 整数摊还），但仍按清单口径把死代码收口为 Math.ceil。探针直接调用该函数断言 167；旧源码返回小数 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "4.5", months: "240", monthly: "1500", prepay: "0" },
    clicks: ["calc();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='MPNEGTRUE '+(t.indexOf('属于负摊还：本金逐期增加')>=0?'OK':'BAD');"],
    expect: ["MPNEGTRUE OK"],
    ref: "复核失败重做·负摊还识别：首期利息 500000×4.5%/12=1875，月供 1500 低于利息，本金逐期增加；旧提示把「低于或接近利息」与「超出 1200 期」混为一谈，修复后明确输出「属于负摊还：本金逐期增加」。默认 4.5%/3000 月供高于利息 ⇒ 不出现该串。",
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "4.5", months: "240", monthly: "1875", prepay: "0" },
    clicks: ["calc();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='MPEQINT '+(t.indexOf('本金不会减少（仅付利息）')>=0&&t.indexOf('并非本金增加的负摊还')>=0?'OK':'BAD');"],
    expect: ["MPEQINT OK"],
    ref: "复核失败重做·仅付利息不等于负摊还：月供恰等于首期利息 1875 时本金不减少但也不增加，旧提示统一称负摊还；修复后区分「仅付利息、本金不减少」并说明与本金增加的负摊还不同。默认 3000 月供 ⇒ BAD。",
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "4.5", months: "240", monthly: "1876", prepay: "0" },
    clicks: ["calc();var t=String(document.getElementById('result').innerHTML);document.getElementById('__tbProbe').textContent='MPTERMCAP '+(t.indexOf('这是模拟期数上限，不是负摊还')>=0?'OK':'BAD');"],
    expect: ["MPTERMCAP OK"],
    ref: "复核失败重做·超出模拟上限不是负摊还：月供 1876 高于首期利息 1875、本金持续减少，但 1200 期内仍未还清；旧实现返回 null 后统一称负摊还。修复后输出「模拟期数上限，不是负摊还」。默认 3000 月供 167 期还清 ⇒ BAD。",
  },
  {
    slug: "finance/salary-calculator",
    inputs: { salary: "20000" },
    clicks: ["currentMode='monthly';var d=document.getElementById.bind(document);d('salary').value='20000';d('baseSalary').value='0';d('housingBase').value='0';d('monthsPerYear').value='12';d('threshold').value='5000';calculate();var ti=d('totalInsurance').textContent,pa=d('pensionAmount').textContent;d('__tbProbe').textContent='SALZERO '+(String(ti).indexOf('¥0.00')===0&&String(pa).indexOf('¥0.00')===0?'OK':'BAD');"],
    expect: ["SALZERO OK"],
    ref: "第124批 F-N101 缴费基数合法 0：旧版 getNum('baseSalary') || monthlySalary 把 0 当空值回退月薪，无法表达「不缴社保」。修复用 __salaryNum 区分空/非数字与合法 0，基数 0 ⇒ 五险一金合计与养老均为 ¥0.00。探针在 calculate() 后立刻读取结果容器，避开 harness 兜底函数重跑覆盖；默认态 ¥4,500.00 / ¥1,600.00 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/salary-calculator",
    inputs: { monthsPerYear: "13" },
    clicks: ["currentMode='monthly';var d=document.getElementById.bind(document);d('salary').value='20000';d('baseSalary').value='20000';d('housingBase').value='20000';d('threshold').value='5000';d('monthsPerYear').value='12';calculate();var t12=d('annualTax').textContent;d('monthsPerYear').value='13';calculate();var t13=d('annualTax').textContent;d('__tbProbe').textContent='SALM13 '+(t12==='¥5,880'&&t13==='¥6,580'?'OK':'BAD');"],
    expect: ["SALM13 OK"],
    ref: "第124批 F-N100 年度扣除同口径：独立复算（月薪 20000、社保 22.5%、起征点 5000、专项 3500/月、无年终奖）——12 月 240000−54000−60000−42000=84000 → 84000×10%−2520=5880；13 月 260000−58500−65000−45500=91000 → 91000×10%−2520=6580（旧版固定乘 12 得 7430）。探针同一次用例内连算两态，旧源码两值都不同 ⇒ 变红；默认 12 月单态不产生该探针 ⇒ 零逃生。"
  },
  {
    slug: "finance/salary-calculator",
    inputs: { salary: "240000", salaryMode: "annual" },
    clicks: ["currentMode='monthly';var d=document.getElementById.bind(document);d('salary').value='240000';d('baseSalary').value='20000';d('housingBase').value='20000';d('monthsPerYear').value='12';d('threshold').value='5000';calculate();switchMode('annual');var net=d('netSalary').textContent,hero=d('afterTaxAmount').textContent,gross=d('grossSalary').textContent;d('__tbProbe').textContent='SALAN '+(net===hero&&gross==='¥240,000.00'?'OK':'BAD');"],
    expect: ["SALAN OK"],
    ref: "第124批 F-N99 年薪模式同口径：旧版明细卡 netSalary 恒用 netMonthly、grossSalary 恒用 monthlySalary，与 hero 的年度值同屏矛盾。修复后明细卡/比例/柱状图全部按当前模式，年薪 240000 ⇒ grossSalary ¥240,000.00 且 netSalary === afterTaxAmount（¥180,120.00）。探针锁两处相等与年值；默认月薪 20000 态 grossSalary 为 ¥20,000.00 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/salary-calculator",
    inputs: {
      salary: "20000", baseSalary: "20000", housingBase: "20000", threshold: "5000", monthsPerYear: "12",
      childrenEdu: "0", continuingEdu: "0", housingLoan: "0", housingRent: "0", elderly: "0", infant: "0",
      currentMonth: "6", ytdIncome: "100000", ytdTaxWithheld: "2730", ytdInsurance: "22500"
    },
    clicks: ["calculate();var d=document.getElementById.bind(document);d('__tbProbe').textContent='CUMOK '+((d('cumTaxable').textContent==='¥6.30万'&&d('cumTax').textContent==='¥3,780.00'&&d('cumCurrentDue').textContent==='¥1,050.00'&&d('cumNet').textContent==='¥14,450.00')?'OK':'BAD');"],
    expect: ["CUMOK OK"],
    ref: "累计预扣复算：第 6 月、本月初累计收入 100000、已预扣 2730、累计五险一金 22500；本月 20000、社保 4500、起征 5000、专项 0。累计所得 = 120000−27000−30000=63000 ⇒ 63000×10%−2520=3780；本月应预扣 = 3780−2730=1050；本月税后 = 20000−4500−1050=14450。默认第 1 月/0 累计为另一态 ⇒ 强判别。",
  },
  {
    slug: "finance/salary-calculator",
    inputs: { monthsPerYear: "0" },
    clicks: ["currentMode='monthly';var d=document.getElementById.bind(document);d('monthsPerYear').value='0';calculate();var b=String(d('salaryBaseNote').innerHTML),a=d('afterTaxAmount').textContent;d('__tbProbe').textContent='SALM0 '+(b.indexOf('每年计薪月数须为正数')>=0&&a==='--'?'OK':'BAD');"],
    expect: ["SALM0 OK"],
    ref: "第124批 F-N101 计薪月数 0 明确拒绝：旧版 `|| 12` 静默兜底，0 还会让年薪折算除零。修复后写出带业务口径的拒绝提示并清空数值区（不残留上一次结果、不产生 Infinity/NaN）。探针同时锁提示与清空；默认 12 月为正常结果 ⇒ BAD ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "1000000", annualRate: "4.9", loanYears: "30", prepayMonth: "24", prepayAmount: "100000", repayMethod: "equal" },
    clicks: ["document.getElementById('prepayCard').style.display='block';calc();var ok=scheduleData.length<360&&document.getElementById('prepayResult').innerHTML.indexOf('还款后剩余本金')>=0&&document.getElementById('yearlyTable').innerHTML.length>0;document.getElementById('__tbProbe').textContent='PREPAYOK '+(ok?'OK':'BAD');"],
    expect: ["PREPAYOK OK"],
    ref: "第24期提前还10万缩期：calcPrepay 必须重建 scheduleData（<360期）并重绘逐年表；旧实现只写 prepayResult、表仍360期 ⇒ BAD。calc 本身会重算并应用提前还款，故只看最终 scheduleData<360，避免把 297 期误判为失败。",
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "-8", housePrice: "300" },
    expect: ["⚠ 输入不能为负数：账户余额 -8 万元。请更正后再计算，无效输入不展示额度依据与还款明细。"],
    ref: "第121批 F-N97 公积金贷款负余额：旧实现只做 parseFloat||0，依据表按原值显示「余额 × 15 倍 −120.0 万」而最终额度被夹到 0.0 万，同一结果区自相矛盾。修复后直接拒绝并在 #result 写出带当前取值的提示。注入 balance=-8 命中；默认 8 万合法态不出现该串 ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "8", housePrice: "-50" },
    expect: ["⚠ 输入不能为负数：房屋总价 -50 万元。请更正后再计算，无效输入不展示额度依据与还款明细。"],
    ref: "第121批 F-N97 负房价分支：与负余额同一拒绝路径但命中不同的输入字段，锁住「房屋总价 -50 万元」这一带值文案；默认房价 300 万合法态不出现 ⇒ 强判别。Score 同步按输入业务状态判 0（真机回归覆盖）。"
  },
  {
    slug: "finance/mortgage-calculator",
    inputs: { loanAmount: "100", rate: "4.2", years: "30", downPayment: "120" },
    expect: ["首付比例须为 0%（含）至 100%（不含），当前输入 120%"],
    ref: "第121批 F-N95 房贷非法首付：旧实现只 resetDisplay() 静默清空数字、不留任何提示，饼图还保留上一次本金/利息比例。修复后按非法字段写出带当前取值的明确提示到结果区（#scheduleBody）。注入 120 命中；默认 30% 合法态不出现 ⇒ 强判别。"
  },
  {
    slug: "finance/mortgage-calculator",
    inputs: { loanAmount: "100", rate: "4.2", years: "30", downPayment: "30" },
    clicks: ["calculate();document.getElementById('downPayment').value='120';calculate();var p=document.getElementById('pieChart');var bg=(p&&p.style)?String(p.style.background):'';document.getElementById('__tbProbe').textContent='MCPIE '+(bg===''?'EMPTY':'KEPT');"],
    expect: ["MCPIE EMPTY"],
    ref: "第121批 F-N95 饼图残留：先按合法参数写入 conic-gradient，再把首付改成 120 触发非法分支，探针读取 #pieChart.style.background。旧版 resetDisplay() 不清饼图 ⇒ KEPT，修复后清空回退 CSS 全灰 ⇒ EMPTY。默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/mortgage-prepayment",
    clicks: ["var __cap=null;TBKit={util:{isEn:function(){return false;},exportTable:function(s,n){__cap={sel:s,name:n};},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(){}},export:{csv:function(n,r){__cap={name:n,rows:r};}}};var __og=document.getElementById;document.getElementById=function(id){if(id==='result')return {querySelectorAll:function(){return [{tagName:'P',textContent:'对照方案（不提前还款）'},{tagName:'TR',querySelectorAll:function(){return [{textContent:'对比项'},{textContent:'① 缩短期限（月供不变）'},{textContent:'② 降低月供（期限不变）'}];}}];}};return __og(id);};__mortgage_prepaymentExport();document.getElementById=__og;document.getElementById('__tbProbe').textContent='MPEX '+(__cap&&__cap.name?__cap.name:'NA')+' rows='+(__cap&&__cap.rows?__cap.rows.length:0);"],
    expect: ["MPEX mortgage-prepayment-detail.csv rows=3"],
    ref: "第121批 F-N94 提前还款「导出明细 CSV」：旧版把 TBKit 自动历史表 #mortgage_prepaymentTable 传给 exportTable，不含两方案明细。修复后导出当前结果区 #result 的逐行明细并调用 TBKit.export.csv，文件名 -detail.csv。用例桩住 result 只有 1 段 + 1 行对比表 ⇒ rows=3；默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/vat-calculator",
    clicks: ["var __cap=null;TBKit={util:{isEn:function(){return false;},exportTable:function(s,n){__cap={n:n};},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(){}},export:{csv:function(n,r){__cap={name:n,rows:r};}}};var __og=document.getElementById;document.getElementById=function(id){if(id==='singleResult')return {textContent:'不含税价 2,358.49',querySelectorAll:function(q){if(String(q).indexOf('.result-item')>=0)return [{querySelector:function(s){return {textContent:s==='.label'?'不含税价':'2,358.49'};}}];return [];}};return __og(id);};__vat_calculatorExport();document.getElementById=__og;document.getElementById('__tbProbe').textContent='VATEX '+(__cap&&__cap.name?__cap.name:'NA')+' n='+(__cap&&__cap.rows?__cap.rows.length:0);"],
    expect: ["VATEX vat-calculator-detail.csv n=2"],
    ref: "第122批 F-N112 增值税单笔「导出明细 CSV」：旧版把 TBKit 自动历史表 #vat_calculatorTable 传给 exportTable，不含当前单笔四项结果。修复后导出 #singleResult 的 result-item 明细并走 TBKit.export.csv，文件名 -detail.csv。用例桩住结果区只有 1 项明细 ⇒ rows=2（表头 + 1 行）；默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/vat-calculator",
    inputs: { batchInput: "1000\nabc\n5000", batchRate: "13" },
    clicks: ["var __f=null;ToolBox={downloadText:function(n,t){__f=String(t);},showToast:function(){},copyText:function(){},formatNumber:function(v,d){return String(v);}};exportBatchCSV();document.getElementById('__tbProbe').textContent='VATSUM '+(__f&&__f.indexOf('合计（逐行舍入后相加）,,5309.74,690.26,6000.00')>=0?'OK':'BAD');"],
    expect: ["VATSUM OK"],
    ref: "第122批 F-N112 批量 CSV 补合计：注入 3 行含 1 行非数字（abc 被忽略），有效两行按含税 13% 倒推：逐行舍入后不含税 884.96+4424.78=5309.74、税额 115.04+575.22=690.26、含税 6000.00；合计必须等于逐行显示值之和（旧的汇总后再舍入口径会得 5309.73/690.27）。默认批量 5 行合计 7,522.12 不含该串 ⇒ 强判别。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { sd2: "2000", special: "0" },
    expect: ["明细合计 ¥2,000.00/月尚未应用"],
    ref: "第123批 F-N109 个税页扣除明细未应用：填了子女教育 2000、上方 special 仍为 0 时，旧版结果区只显示「明细合计 ¥2,000.00」却按 0 扣税，两个口径并排无说明。修复后明确写出「尚未应用」及当前真正生效的 ¥0.00/月。默认 7 项全 0 时按设计不提示（避免首屏误报）⇒ 该串不出现，强判别。"
  },
  {
    slug: "finance/tax-calculator",
    clicks: ["var __cap=null;TBKit={util:{isEn:function(){return false;},exportTable:function(s,n){__cap={sel:s,name:n};},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(){}},export:{csv:function(){}}};ToolBox={showToast:function(){},formatNumber:function(v){return String(v);},setResult:function(){},copyText:function(){},downloadText:function(){}};__taxExport();var t=String(document.getElementById('taxResultTable').innerHTML);document.getElementById('__tbProbe').textContent='TAXEXP '+(t.indexOf('单独计税·全年个税合计')>=0&&t.indexOf('专项附加扣除明细合计')>=0&&t.indexOf('当前生效的专项附加扣除')>=0?'OK':'OLD');"],
    expect: ["TAXEXP OK"],
    ref: "第123批 F-N108 个税导出 CSV 补全：旧版 __taxExport 只写工资 7 行，不含奖金两方案/全年合计与 7 项扣除明细。修复后 #taxResultTable 追加这些行，探针读取导出表内容判定。默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    "slug": "finance/npv-calculator",
    "inputs": {"rate": "8", "init": "100"},
    "clicks": ["updateCF(0, 230)", "updateCF(1, -132)", "updateCF(2, 0)", "updateCF(3, 0)"],
    "expect": ["多根 IRR 内部收益率", "9.9%", "20.0%"],
    "ref": "清单复核案例：现金流 −100、+230、−132 在 r=10%、20% 均为 NPV 零点（残差 ~1e-14），但两根落在均匀扫描的同一粗区间（0~0.25）、端点同号；旧实现端点变号法漏判返回「无解」。修复后每段加中点采样，左右各二分捕获两跟（9.99%、20.00%）并判「多根」。默认态不同 ⇒ 无探针串、零逃生。"
  },
  {
    "slug": "finance/npv-calculator",
    "inputs": { "init": "100", "rate": "8" },
    "clicks": ["updateCF(0,221);updateCF(1,-122.1);document.getElementById('__tbProbe').textContent='IRR211 '+(function(){var r=calcIRR(100,[221,-122.1]);return r.status+':'+(r.rates||[]).map(function(x){return (x*100).toFixed(1);}).join(',');})();"],
    "expect": ["IRR211 multiple:10.0,11.0"],
    "ref": "复核失败点：现金流 −100、+221、−122.1 在 r=10% 与 11% 有两个紧邻实根；旧中点采样仍落在同号子区间而漏判无解。修复后以 x=1/(1+r) 多项式按导数临界点分段隔离，两个根均捕获。锚定为注入向量派生的探针串（默认态不执行 clicks，零逃生）。"
  },
  {
    "slug": "finance/npv-calculator",
    "inputs": { "init": "100", "rate": "8" },
    "clicks": ["updateCF(0,220);updateCF(1,-121);document.getElementById('__tbProbe').textContent='IRRDBL '+(function(){var r=calcIRR(100,[220,-121]);return r.status+':'+(r.rate===undefined?'NA':(r.rate*100).toFixed(2));})();"],
    "expect": ["IRRDBL ok:10.00"],
    "ref": "复核失败点：现金流 −100、+220、−121 在 r=10% 有重根（判别式恰为 0），旧实现端点同号且中点不精确命中而误报无解。修复后对分位精确二次重根直接给唯一解 10.00%。探针串绑定注入向量，默认态不命中。"
  },
  {
    "slug": "finance/npv-calculator",
    "inputs": { "init": "100", "rate": "8" },
    "clicks": ["updateCF(0,400);updateCF(1,-600);updateCF(2,400);updateCF(3,-100);document.getElementById('__tbProbe').textContent='IRRQUAD '+calcIRR(100,[400,-600,400,-100]).status;"],
    "expect": ["IRRQUAD uncertain"],
    "ref": "复核失败点补充：四重根（−100、+400、−600、+400、−100）在机器精度下无法可靠判定，修复后明确返回 uncertain（页面显示「无法确定」），绝不误称无解，也不伪造唯一根。探针串绑定注入向量，默认态不命中。"
  },
  {
    "slug": "finance/depreciation-calculator",
    "inputs": {"cost": "10000", "salvage": "1000", "life": "5", "totalUnits": "10000", "yearUnits": "3000x,2500,2000,1500,1000"},
    "clicks": ["calc();var h=String(document.getElementById('stats').innerHTML);document.getElementById('__tbProbe').textContent='DEP53BAD '+(h.indexOf('请按使用年限逐年填写')>=0?'OK':'BAD');"],
    "expect": ["DEP53BAD OK"],
    "ref": "F-N53 审计修复回归：旧实现 parseFloat 把 \"3000x\" 读成 3000，工作量法照常出现；修复后严格纯数字校验拒绝该输入，提示「请按使用年限逐年填写」。默认态 yearUnits 合法且无 DEP53BAD 探针 ⇒ 零逃生。"
  },
  {
    "slug": "finance/depreciation-calculator",
    "inputs": {"cost": "10000", "salvage": "1000", "life": "5", "totalUnits": "10000", "yearUnits": "5000,5000,5000,5000,5000"},
    "clicks": ["calc();var h=String(document.getElementById('stats').innerHTML);document.getElementById('__tbProbe').textContent='DEP53OVR '+(h.indexOf('超过总工作量')>=0?'OK':'BAD');"],
    "expect": ["DEP53OVR OK"],
    "ref": "F-N53 审计修复回归：5 年各 5000 合计 25000 > 总工作量 10000，旧实现静默截断无任何提示；修复后 calcUnits 标记 overflow、stats 提示「超过总工作量…已截封顶」。默认态合计 10000 不超额、无 DEP53OVR 探针 ⇒ 零逃生。"
  },
  {
    slug: "finance/housing-fund-loan",
    clicks: ["var __cap=null;TBKit={util:{isEn:function(){return false;},exportTable:function(sel,name){__cap={sel:sel,name:name};},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return [];},last:function(){return null;},record:function(){},mount:function(){}},preset:{bar:function(){}}};var __oq=document.querySelector;document.querySelector=function(s){return {querySelectorAll:function(q){return [{tagName:'TR'}];}};};__housing_fund_loanExport();document.querySelector=__oq;document.getElementById('__tbProbe').textContent='EXPH sel='+(__cap?__cap.sel:'NA')+' name='+(__cap?__cap.name:'NA');"],
    expect: ["EXPH sel=#housing_fund_loanDetail name=housing-fund-loan.csv"],
    ref: "复核失败重做·F-N189 第46批 公积金贷款：导出目标应是真实业务明细容器，而非历史记录表。旧实现把 TBKit.util.exportTable 指向 #<pre>Table（历史摘要），修复后指向该页业务明细容器。用例桩捕获 exportTable 的选择器与文件名，默认态不执行 clicks、无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/gstin-validator",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('output').textContent=\"校验流程已完成。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。校验结论：校验失败，该 GSTIN 无效。\";__gstin_validatorExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNGS score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNGS score=0"],
    ref: "复核失败重做·F-N189 第二批/第42–44批 GSTIN：失败结论/必填提示位于 80 字摘要之后，旧 Score 只看 ResText 前 80 字 ⇒ 误记通过(1)；修复后 Score 读 FullResText 完整文本，命中失败词 ⇒ 0。历史展示仍用摘要。默认态无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/meid-validator",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('output').textContent=\"校验流程已完成。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。校验结论：校验失败，该 MEID 无效。\";__meid_validatorExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNME score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNME score=0"],
    ref: "复核失败重做·F-N189 第二批/第42–44批 MEID：失败结论/必填提示位于 80 字摘要之后，旧 Score 只看 ResText 前 80 字 ⇒ 误记通过(1)；修复后 Score 读 FullResText 完整文本，命中失败词 ⇒ 0。历史展示仍用摘要。默认态无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/abn-validator",
    inputs: { input: "2222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222" },
    clicks: ["validate();document.getElementById('__tbProbe').textContent='FNAB score='+__abn_validatorScore();"],
    expect: ["FNAB score=0"],
    ref: "ABN 长无效输入走真实校验，失败状态不受历史摘要截断影响。"
  },
  {
    slug: "finance/aadhaar-validator",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('output').textContent=\"校验流程已完成。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。校验结论：校验失败，该 Aadhaar 无效。\";__aadhaar_validatorExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNAA score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNAA score=0"],
    ref: "复核失败重做·F-N189 第二批/第42–44批 Aadhaar：失败结论/必填提示位于 80 字摘要之后，旧 Score 只看 ResText 前 80 字 ⇒ 误记通过(1)；修复后 Score 读 FullResText 完整文本，命中失败词 ⇒ 0。历史展示仍用摘要。默认态无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/bic-validator",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('output').textContent=\"校验流程已完成。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。校验结论：校验失败，该 BIC 无效。\";__bic_validatorExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNBV score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNBV score=0"],
    ref: "复核失败重做·F-N189 第二批/第42–44批 BIC：失败结论/必填提示位于 80 字摘要之后，旧 Score 只看 ResText 前 80 字 ⇒ 误记通过(1)；修复后 Score 读 FullResText 完整文本，命中失败词 ⇒ 0。历史展示仍用摘要。默认态无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/calc-5",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('res').textContent=\"计算流程已完成。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。请填写「投资成本」后再计算。\";__calc_5Extras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNC5 score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNC5 score=0"],
    ref: "复核失败重做·F-N189 第二批/第42–44批 calc-5：失败结论/必填提示位于 80 字摘要之后，旧 Score 只看 ResText 前 80 字 ⇒ 误记通过(1)；修复后 Score 读 FullResText 完整文本，命中失败词 ⇒ 0。历史展示仍用摘要。默认态无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/dca-calculator",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('res').textContent=\"计算流程已完成。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。请填写「每月定投」后再计算。\";__dca_calculatorExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNDC score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNDC score=0"],
    ref: "复核失败重做·F-N189 第二批/第42–44批 dca-calculator：失败结论/必填提示位于 80 字摘要之后，旧 Score 只看 ResText 前 80 字 ⇒ 误记通过(1)；修复后 Score 读 FullResText 完整文本，命中失败词 ⇒ 0。历史展示仍用摘要。默认态无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/imei-validator",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('output').textContent=\"校验流程已完成。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。校验结论：校验失败，该 IMEI 无效。\";document.getElementById('__histOptIn').checked=true;__imei_validatorExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNIMEI score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNIMEI score=0"],
    ref: "复核失败重做·F-N189 第一批 IMEI：校验失败结论位于 80 字摘要之后，旧 Score 只看 ResText 前 80 字 ⇒ 误记通过(1)；修复后 Score 读 FullResText 完整文本，命中「校验失败/无效」⇒ 0。历史展示仍为摘要，不影响。默认态无探针串 ⇒ 零逃生。"
  },
  {
    slug: "finance/gst-validator",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('output').textContent=\"校验流程已完成。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。校验结论：校验失败，该 GSTIN 无效。\";__gst_validatorExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNGST score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNGST score=0"],
    ref: "复核失败重做·F-N189 第一批 GSTIN：同 IMEI，失败结论在截断摘要之后。修复后 FullResText 判定 ⇒ 0（旧 1）。"
  },
  {
    slug: "finance/iccid-validator",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('output').textContent=\"校验流程已完成。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。正在整理格式说明与逐步分解。校验结论：校验失败，该 ICCID 无效。\";document.getElementById('__histOptIn').checked=true;__iccid_validatorExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNICCID score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNICCID score=0"],
    ref: "复核失败重做·F-N189 第一批 ICCID：同 IMEI，失败结论在截断摘要之后。修复后 FullResText 判定 ⇒ 0（旧 1）。"
  },
  {
    slug: "finance/bic-lookup",
    clicks: ["var __cap=[];TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){}},matrix:{table:function(){}},history:{list:function(){return __cap;},last:function(){return __cap.length?__cap[__cap.length-1]:null;},record:function(r){__cap.push(r);},mount:function(){}},preset:{bar:function(){}}};var __els=[{id:'x',type:'text',value:'1'}];var __oq=document.querySelectorAll;document.querySelectorAll=function(s){return __els;};document.getElementById('output').textContent=\"⚠ 格式有效，但离线库中未收录该 BIC，请核对。正在整理银行代码信息。正在整理银行代码信息。正在整理银行代码信息。正在整理银行代码信息。正在整理银行代码信息。正在整理银行代码信息。正在整理银行代码信息。正在整理银行代码信息。\";__bic_lookupExtras();document.querySelectorAll=__oq;document.getElementById('__tbProbe').textContent='FNBIC score='+(__cap.length?__cap[__cap.length-1].__tbScore:'NA');"],
    expect: ["FNBIC score=1"],
    ref: "复核失败重做·F-N189 第一批 BIC：格式有效但离线库未知的警告（⚠）被通用词表判失败(0)；修复后从失败词表移除 ⚠（警告≠失败），FullResText 判定 ⇒ 1。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "", insurance: "3000", special: "2000", threshold: "5000" },
    clicks: ["__taxExport()"],
    expect: ["请填写税前月薪后再导出"],
    ref: "第五批 F-N18 复核重做：清空月薪并计算后主结果已提示必填，但点击导出旧 __taxExport() 仍以 parseFloat(...)||0 生成「零应缴个税/零税后收入」CSV。现导出在最前面复用必填状态（且先于 TBKit 检查），空月薪时清空结果表并提示、不导出；显式填 0 仍合法可导出。默认 salary=20000 点击导出不产生该提示 ⇒ 强判别。"
  },
  // ── 校验位算法类（11 正例 + 2 反例）──────────────────────────────
  {
    slug: "finance/credit-card-luhn",
    inputs: { input: "4532015112830366" },
    expect: [ "4532015112830366 长度：" ],
    ref: "Luhn（模 10）：4532015112830366 为公开测试卡号，加权和 mod 10 == 0；expect 取页面回显的数字串（含具体卡号 ⇒ 默认预填 4111111111111111 不命中，判别力保留）",
  },
  {
    slug: "finance/credit-card-luhn",
    inputs: { input: "00" },
    expect: [ "数字： 00 长度： 2 位 Luhn 校验： ✅ 通过 ⚠️ 该数字串通过 Luhn 算法，但长度 2 位不是有效卡号长度" ],
    ref: "F-N67 真锁：2 位「00」Luhn 算法虽通过（0+0），但必须点明「长度 2 位不是有效卡号长度」，不再误称「✅ 卡号通过 Luhn 校验」。旧实现必命中「卡号通过」⇒ 反相变红；默认 16 位预填不含该串 ⇒ 零逃生。",
  },
  {
    slug: "finance/aba-validator",
    inputs: { input: "011000015" },
    expect: ["前缀分类： 01 - 美联储第 1 区（Boston）"],
    ref: "ABA 3-7-1 权重：Σ = 3×0+7×1+1×1+3×0+7×0+1×0+3×0+7×1+1×5 = 20，mod 10 == 0；expect 取页面回显「美联储分区： 01 - Boston」（含分区城市 ⇒ 默认预填 021000021 输出「02 - New York」不命中，消除「✅ 有效」通用串导致的逃生）",
  },
  {
    slug: "finance/aba-validator",
    inputs: { input: "000000000" },
    expect: ["前缀分类： 00 - 美国政府/财政部"],
    ref: "F-N212 前缀白名单：全零 000000000 校验和 0 通过但前缀 00 非法；旧实现仅报「00 - 未知/特殊用途」仍判 ✅，修复后直接 ❌。默认预填前缀 02 ⇒ 不命中，强判别。",
  },
  {
    slug: "finance/iban-validator",
    inputs: { ibanInput: "GB82WEST12345698765432" },
    expect: ["GB82 WEST 1234 5698 7654 32"],
    ref: "ISO 13616：后 4 位前移 → 字母 A=10…Z=35 → 大数 mod 97 == 1（GB82 为公开示例）；expect 取页面回显的 4 位分组格式串（含具体 IBAN ⇒ 默认预填 DE89370400440532013000 的格式化值 DE89 3704 0044 0532 0130 00 不命中）",
  },
  {
    slug: "finance/cpf-validator",
    inputs: { input: "52998224725" },
    expect: ["529.982.247-25"],
    ref: "巴西 CPF 模 11 双校验：前 9 位算 DV1，前 10 位算 DV2，余数 <2 记 0；expect 取页面回显的格式化串（含具体号码 ⇒ 默认预填 11144477735 的格式化值 111.444.777-35 不命中）",
  },
  {
    slug: "finance/cnpj-validator",
    inputs: { input: "11222333000181" },
    expect: ["11.222.333/0001-81"],
    ref: "巴西 CNPJ 模 11 双校验：权重 [5,4,3,2,9,8,7,6,5,4,3,2]，余数 <2 记 0；expect 取页面回显的格式化串（含具体号码 ⇒ 默认预填 00000000000191 的格式化值 00.000.000/0001-91 不命中）",
  },
  {
    slug: "finance/cnpj-validator",
    inputs: { input: "11ABC2223330001-81" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='FNCNPJ '+document.getElementById('input').value+' '+((h.indexOf('第 3 位含非法字符「A」')>=0&&h.indexOf('✅ CNPJ 号码有效')<0)?'OK':'BAD');"],
    expect: ["FNCNPJ 11ABC2223330001-81 OK"],
    ref: "F-N168 字母拒绝：11ABC2223330001-81 剥离字母后是合法 CNPJ 11222333000181，旧实现 replace(\\D,'') 静默剔除 ABC 后判「✅ CNPJ 号码有效」；新实现白名单守卫点名第 3 位非法字符 A 并拒绝。默认态合法 ⇒ 零逃生。",
  },
  {
    slug: "finance/cnpj-validator",
    inputs: { input: "00000000000000" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='FNCNPZ '+document.getElementById('input').value+' '+((h.indexOf('全部数字相同，非有效 CNPJ')>=0&&h.indexOf('校验和： ✅ 通过')>=0)?'OK':'BAD');"],
    expect: ["FNCNPZ 00000000000000 OK"],
    ref: "F-N169 全同数字分流：00000000000000 的两个 mod-11 期望其实为 0/0 与末位相符，失败原因是「数字全同」而非「校验和失败」。旧实现统一输出「❌ 校验和失败」误导定位；新实现独立报告校验和通过，并提示「全部数字相同，非有效 CNPJ」。默认预填 00000000000191 非全同 ⇒ 零逃生。",
  },
  {
    slug: "finance/cnpj-validator",
    inputs: { input: "<img src=x onerror=1>" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent='FNCXSS '+((h.indexOf('&lt;img')>=0&&h.indexOf('<img')<0)?'ESC':'RAW');"],
    expect: ["FNCXSS ESC"],
    ref: "CNPJ 自 XSS 转义（同族第89批模式顺带修）：旧实现把 raw 原样拼入 innerHTML，输入 <img src=x onerror=1> 即执行；新实现 esc() 转义输出 &lt;img。默认态不含探针串 ⇒ 零逃生。",
  },
  {
    slug: "finance/abn-validator",
    inputs: { input: "98765432122" },
    expect: ["98 765 432 122"],
    ref: "澳洲 ABN：首位减 1 后加权 [10,1,3,5,7,9,11,13,15,17,19] 求和 mod 89 == 0（98765432122 有效）；expect 取页面回显格式化串「98 765 432 122」。刻意不用 51824753556（其格式化 51 824 753 556 与页面 placeholder 相同 ⇒ 恒命中成逃生项），默认预填 53004085616 的格式化 53 004 085 616 亦不命中",
  },
  {
    slug: "finance/isbn-validator",
    inputs: { isbnInput: "9780306406157" },
    expect: ["978-0-306-40615-7"],
    ref: "ISBN-13：Σ 前 12 位交替权重 1/3 → 校验位 = (10 - Σ mod 10) mod 10 == 第 13 位；expect 取页面归一化格式「978-0-306-40615-7」（输入专属，默认预填 9787111111115 的归一化 978-7-111-11111-5 不命中 ⇒ 消除静态「校验通过」逃生项）。",
  },
  {
    slug: "finance/sin-validator",
    inputs: { input: "046454286" },
    expect: ["046-454-286"],
    ref: "加拿大 SIN 使用 Luhn：046454286 加权和 mod 10 == 0；expect 取页面回显的格式化串「046-454-286」（含具体号码 ⇒ 默认预填 130692544 的格式化值 130-692-544 不命中）",
  },
  {
    slug: "finance/sin-validator",
    inputs: { input: "000-000-000" },
    expect: ["首字符： 0 - Not issued 校验算法： Luhn（模 10） 校验和： ❌ 未通过 ❌ 校验和失败，SIN 无效"],
    ref: "F-N209 全零：000000000 Luhn 虽通过但首字符 0 页面自述 Not issued（CRA 未发行）⇒ 无效。旧实现仅看 Luhn 判 ✅。默认预填首位 1 ⇒ 不命中。",
  },
  {
    slug: "finance/sin-validator",
    inputs: { input: "130692544abc" },
    expect: ["❌ SIN 只能包含数字、空格或连字符"],
    ref: "F-N209 字母剥离：旧实现 replace(\\D,'') 把 abc 剥离后按 130692544 判 ✅；修复后含字母直接拒绝。默认预填纯数字 ⇒ 不命中。",
  },
  {
    slug: "finance/dni-validator",
    inputs: { input: "12345678Z" },
    expect: ["Z（期望 Z）"],
    ref: "西班牙 DNI：校验字母 = 'TRWAGMYFPDXBNJZSQVHLCKE'[数字 mod 23]，12345678 mod 23 = 14 → Z；expect 取独有「校验字母：Z（期望 Z）」（含具体字母 ⇒ 默认预填 87654321X 输出 X（期望 X）不命中）",
  },
  {
    slug: "finance/dni-validator",
    inputs: { input: "12345678Z" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent='DNIT '+document.getElementById('input').value+' '+(h.indexOf('字母表（TRWAGMYFPDXBNJZSQVHLCKE）')>=0?'OK':'BAD');"],
    expect: ["DNIT 12345678Z OK"],
    ref: "F-N204 字母表长度锁：官方 DNI 映射表只有 23 字符 TRWAGMYFPDXBNJZSQVHLCKE，旧表多一个尾 T（虽因 %23 不取到第 24 位而行为侥幸正确，但 FAQ/输出说明误导）。用例带输入号并断言输出算法行的闭括号边界，旧 24 字符表 hits BAD ⇒ 真判别；默认预填无 DNIT 探针 ⇒ 零逃生。",
  },
  {
    slug: "finance/npi-validator",
    inputs: { input: "1234567893" },
    expect: ["输入： 1234567893 校验算法： Luhn（前缀 80840） 校验和： ✅ 通过 ✅ NPI 号码有效"],
    ref: "F-N210 号段修正后首位 1 为合法段，不再有「通常不以 0 或 1 开头」误导提示；80840+1234567893 过 Luhn ⇒ ✅ 有效。expect 取带输入号的完整串（默认预填 4234567897 首位 4 修复后判未分配号段，不命中）⇒ 强判别。",
  },
  {
    slug: "finance/npi-validator",
    inputs: { input: "2234567891" },
    expect: ["校验和： ✅ 通过 ✅ NPI 号码有效"],
    ref: "CMS 已发行号段 2，80840 + 2234567891 通过 Luhn。",
  },
  {
    slug: "finance/npi-validator",
    inputs: { input: "5234567893" },
    expect: ["首位 5 为未分配号段（CMS 已发行号段首位为 1 或 2），号码无效"],
    ref: "F-N210 号段写反：首位 5 属未分配段，旧实现仅 Luhn 通过后判「✅ 有效」，修复后直接 ❌。expect 带首位 5（默认预填首位 4 不命中）⇒ 强判别。",
  },
  {
    slug: "finance/aadhaar-validator",
    inputs: { input: "234123412346" },
    expect: ["2341 2341 2346"],
    ref: "印度 Aadhaar 使用 Verhoeff（十进制非线性和校验），234123412346 校验位正确；expect 取页面回显的格式化串「2341 2341 2346」（含具体号码 ⇒ 默认预填 345678901238 的格式化值 3456 7890 1238 不命中，判别力保留）",
  },
  {
    slug: "finance/tfn-validator",
    inputs: { input: "123456789" },
    expect: ["校验和不匹配"],
    ref: "澳洲 TFN 反例：权重 [1,4,3,7,5,8,6,9,10]，Σ = 323，323 mod 11 = 4 ≠ 0 → 校验和不匹配；第949批把「校验和失败/无效」改为「不匹配、格式检查未通过」，不推断号码不存在。",
  },
  {
    slug: "finance/ird-validator",
    inputs: { input: "123456789" },
    expect: ["输入： 123456789 格式化： 123-456-789 长度： 9 位"],
    ref: "新西兰 IRD 反例：补 0 后 base = 01234567、校验位 9，加权 mod 11 期望 ≠ 9 → 无效。原 expect「校验和失败」在 F-N220 修复中默认态一度变非法时命中 ⇒ 逃生，改锁带输入号的连续串。",
  },
  {
    slug: "finance/ird-validator",
    inputs: { input: "49091850" },
    expect: ["输入： 49091850 格式化： 049-091-850 长度： 8 位 校验算法： 加权模 11（primary 3,2,7,6,5,4,3,2；得 10 改用 secondary 7,4,3,2,5,2,7,6） 校验和： ✅ 通过 ✅ 长度与校验和检查通过"],
    ref: "F-N220 合法号：8 位 49091850 补前导 0 → base 04909185，primary Σ=154 → rem 0 → 校验位 0（第 9 位）⇒ ✅。旧实现 base 取 substring(1,9) 错位判 ❌。第934批把结论改为「长度与校验和检查通过，无法确认登记/归属」；expect 跨「长度/校验算法/校验和/新结论」取连续串（带输入号）。默认预填 490918507 ⇒ 不命中。",
  },
  {
    slug: "finance/ird-validator",
    inputs: { input: "10000019" },
    expect: ["输入： 10000019 格式化： 010-000-019 长度： 8 位 校验算法： 加权模 11（primary 3,2,7,6,5,4,3,2；得 10 改用 secondary 7,4,3,2,5,2,7,6） 校验和： ❌ 未通过 ❌ 校验和未通过，该号码不符合 IRD 校验规则"],
    ref: "F-N220 非法号：8 位 10000019 补 0 → base 01000001 期望校验位 7 ≠ 9 ⇒ ❌；旧实现错位判 ✅。与 10000009（合法）镜像。默认预填 490918507 合法 ⇒ 不命中。",
  },

  {
    slug: "finance/ird-validator",
    inputs: { input: "100000131" },
    expect: ["输入： 100000131"],
    ref: "主权重结果为 10，备用权重得校验位 1。",
  },
  {
    slug: "finance/ird-validator",
    inputs: { input: "100000132" },
    expect: ["输入： 100000132", "❌ 校验和失败，IRD 无效"],
    ref: "相同前八位经备用权重应为 1，校验位 2 无效。",
  },

  // ── 金融公式类（7 个，期望值由 python 独立复算）────────────────────
  {
    slug: "finance/simple-interest",
    inputs: { principal: "25000", rate: "3.6", years: "4" },
    expect: ["3,600 元", "28,600 元", "900 元"],
    ref: "去默认化：单利 利息 = P×r×t = 25000×3.6%×4 = 3600（每年 900），本利和 28600。默认 10000/5%/3 → 500、1,500、11,500，不含上述串",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "850000", rate: "3.85", years: "25" },
    expect: ["4,416.51", "1,324,954.06", "474,954.06"],
    ref: "去默认化：等额本息 月供 = P×i×(1+i)^n/((1+i)^n−1)，i = 3.85%/12 = 0.00320833、n = 300 ⇒ 4416.51；还款总额 1,324,954.06、总利息 474,954.06（= 总额 − 850,000）。默认 100万/4.2%/30 → 4,890.17、1,760,461.83、760,461.83、360 期",
  },
  {
    slug: "finance/calc-5",
    inputs: { cost: "80000", value: "128000", years: "3" },
    expect: ["60.00%", "48,000.00", "16.96%"],
    ref: "去默认化：净收益 = 128000−80000 = 48000；总 ROI = 48000/80000 = 60%；年化 = 1.6^(1/3)−1 = 16.96%。默认 100000/150000/5 → 50.00%、50,000.00、8.45%",
  },
  {
    slug: "finance/calc-5",
    inputs: { cost: "0", value: "150000", years: "5" },
    expect: ["投资成本必须大于 0"],
    ref: "F-N74 零成本：旧实现 netProfit=150000、ROI 0.00%、年化 0.00%，零回报却大额盈利；修复后字段级拒绝。默认成本 100000 ⇒ 不命中。",
  },
  {
    slug: "finance/calc-5",
    inputs: { cost: "-100000", value: "150000", years: "5" },
    expect: ["投资成本必须大于 0"],
    ref: "F-N74 负成本：旧实现把成本额加进收益得 netProfit=250000，ROI 却 0.00%；修复后同样拒绝。默认成本 100000 ⇒ 不命中。",
  },
  {
    slug: "finance/calc-5",
    inputs: { cost: "100000", value: "0", years: "5" },
    expect: ["年化回报率（复利）： -100.00%"],
    ref: "本金全损时 1+ROI=0，正年限的复利年化为 -100%，而非无法计算。",
  },
  {
    slug: "finance/calc-5",
    inputs: { cost: "100000", value: "-50000", years: "5" },
    expect: ["亏损超过本金，无法按复利年化"],
    ref: "F-N75 倒亏：ROI = −150% ⇒ 1+roi<0，旧实现年化同样显示 0.00%；修复后拒绝伪零回报。默认 ROI 50% ⇒ 两条均不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { fc: "180000", price: "75", vc: "45" },
    expect: ["450,000 盈亏平衡收入", "6000 盈亏平衡销量", "4.00 经营杠杆系数"],
    ref: "去默认化：单位边际贡献 = 75−45 = 30；盈亏平衡销量 = 180000/30 = 6000 件、平衡收入 = 6000×75 = 450,000 元；经营杠杆 = 8000×30/60000 = 4.00（预计销量 8000 沿用默认）。默认 100000/50/30 → 20.00、5000 件、250,000、2.67。**注意「30.00 单位边际贡献」不可作 expect** —— harness 兜底会调 addScenario() 生成一个模板场景，其单位边际贡献恰为 30.00 ⇒ 默认态也命中（实测 3/3 命中，属逃生项）。同理边际贡献率 40.00% 与默认态同值，也不可用",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { detailEnd: "" },
    clicks: ["generateDetailTable()"],
    expect: ["结束销量不能为空；0 是有效值，请明确输入 0。"],
    ref: "第933批：明细结束销量不再用 `|| 20000` 静默回退；空串必须点名提示。默认 20000 ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { detailStart: "20000", detailEnd: "0", detailStep: "1000" },
    clicks: ["generateDetailTable()"],
    expect: ["结束销量须不小于起始销量（当前 20000 → 0）"],
    ref: "第933批：倒序范围不再自动改写为 start+10×step；明确拒绝。默认 0→20000 ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { detailStart: "0", detailEnd: "100000", detailStep: "1" },
    clicks: ["generateDetailTable()"],
    expect: ["当前范围将生成 100001 行，超过 500 行上限"],
    ref: "第933批：生成前预计算行数，超过 500 行直接拒绝，避免极小步长构造海量 DOM/CSV。默认 21 行 ⇒ 不命中。",
  },
  {
    slug: "finance/vat-calculator",
    inputs: { amount: "2500", customRate: "6" },
    expect: ["2,358.49", "141.51"],
    ref: "去默认化：含税价倒推 不含税 = 2500/1.06 = 2358.49、税额 = 141.51（单笔页签读 customRate）。默认 1000/13% → 884.96、115.04；注意批量页签用 batchRate（未注入，仍 13%）输出 2,212.39/287.61，不会撞车",
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "", insurance: "3000", special: "2000", threshold: "5000" },
    expect: ["请填写税前月薪（元）"],
    ref: "F-N18 复核重做：清空税前月薪（空值）后，旧实现把空当 0 算出「¥0.00 税额」「¥0.00 税后」并给出年终奖对比结论；现空值直接清空结果并提示「请填写税前月薪（元）」，不输出任何数值/结论。默认态（salary=20000）正常出税表不命中该提示 ⇒ 强判别、零逃生。",
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "50000", insurance: "8000", special: "3000", threshold: "6000" },
    expect: ["> 25,000 且 ≤ 35,000 元 25% ✓ 适用"],
    ref: "非默认输入使应纳税所得额=50000-8000-6000-3000=33000 → 落入第3级并高亮「✓ 适用」。级距按开放/闭合边界显示为「> 25,000 且 ≤ 35,000」，与 >25000 且 ≤35000 的计算判断一致；旧版写 25,001 - 35,000 会漏掉 25000.01–25000.99 的小数金额。默认 20000/3000/2000/5000 ⇒ 所得 10000 落第2级，不命中。",
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "20000", insurance: "3000", special: "2000", threshold: "5000", bonus: "30000", sd1: "2000", sd7: "3000", sd4: "12000" },
    expect: ["专项附加扣除明细合计： ¥6,000.00"],
    ref: "专项附加扣除 7 项明细（2026-10-25 新增 / plan 标注「搜索需求极大」）：婴幼儿照护 2000 + 赡养老人 3000 + 大病医疗 12000/年 ÷ 12 = 1000 ⇒ 明细合计 6000 元/月，渲染在结果区首行。**同时绑定分摊口径**（大病医疗按年填入须摊到月，若误按 12000 全额计则合计变 17000，本例即变红）与金额格式化。默认态七项全 0 ⇒ 合计 ¥0.00，不含该串 ⇒ 零逃生。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { sd4: "100000" },
    clicks: ["calculate()"],
    expect: ["专项附加扣除明细合计： ¥6,666.67", "大病医疗按 80000 元/年封顶，实际计入 ¥6,666.67/月（原填 ¥100,000.00/年，未封顶将摊成 ¥8,333.33/月）。"],
    ref: "F-N19 大病医疗年度封顶：sd4 填 100000 元/年，旧实现直接 v/12=8333.33/月 ⇒ 多扣、税额仅 156.67；现按 80000 元/年封顶后摊月 = 6666.67/月，独立复算税额 323.33。两条分别绑定封顶后的合计与「实际采用值」说明行（均在结果容器 bonusBox 内）。默认态七项全 0 ⇒ 合计 ¥0.00 且无说明行；旧代码合计 ¥8,333.33 也无说明行 ⇒ 任一回归即变红，零逃生。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { sd5: "1000", sd6: "1500" },
    clicks: ["calculate()"],
    expect: ["专项附加扣除明细合计： ¥1,500.00", "已按较大者 ¥1,500.00/月（住房租金）计入，另一项 ¥1,000.00/月未计入。"],
    ref: "F-N19 房贷利息/住房租金互斥：同一纳税年度内两项不可同时扣除，同时填写时仅按较大者 1500 计入（独立复算税额 840.00），旧实现直加得 2500、税额 740。两条分别绑定互斥后的合计与「较大者/未计入」说明行。默认态 ¥0.00 且无说明行 ⇒ 零逃生。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { sd1: "2000", sd4: "12000", sd5: "1000", sd6: "1500" },
    clicks: ["calculate()"],
    expect: ["专项附加扣除明细合计： ¥4,500.00"],
    ref: "F-N19 组合回归：sd4=12000/年未触顶 ⇒ 摊月 1000；sd5/sd6 互斥取 1500；sd1=2000 ⇒ 合计 4500。旧实现 1000+1000+1500+2000=5500。既验证封顶逻辑不误伤未超限的大病医疗，也验证互斥与其余四项叠加口径；默认态 ¥0.00 ⇒ 零逃生。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { sd4: "12000", sd5: "1000" },
    clicks: ["calculate()"],
    expect: ["专项附加扣除明细合计： ¥2,000.00"],
    ref: "F-N19 单项回归护栏：只填房贷利息、无租金、大病医疗未触顶 ⇒ 12000/12=1000 + 房贷 1000 = 2000，且不应出现互斥说明行。确认新增互斥逻辑不得误伤合法单项场景；注入失败回落默认 ⇒ ¥0.00 不命中。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { insurance: "-2000" },
    clicks: ["calculate()"],
    expect: ["⚠ 社保公积金不能为负数，请填写 ≥ 0 的数值。", "20000\n-2000\n—\n—\n—\n—\n—\n—\n—"],
    ref: "F-N18 负社保字段级拒绝：旧实现把 −2000 当作抵扣放大应税所得（台账独立复算 special=0：12000→17000、税 990→1990；页面默认 special=2000 下为 10000→15000、税 790→1590）；现 __taxCheck() 拒绝负值、__taxBlock() 把 7 个结果元素清成「—」并在结果容器给出字段名错误提示，不再参与计算。默认态社保 3000 为正 ⇒ 不命中。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "-1" },
    clicks: ["calculate()"],
    expect: ["⚠ 税前月薪不能为负数，请填写 ≥ 0 的数值。", "-1\n—\n—\n—\n—\n—\n—\n—"],
    ref: "F-N18 负月薪字段级拒绝：旧实现 Math.max(0,…) 只兜住应纳税所得额，税后收入直接显示负值；现字段级拒绝并清结果。默认态 20000 ⇒ 不命中。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { special: "-5" },
    clicks: ["calculate()"],
    expect: ["⚠ 专项附加扣除不能为负数，请填写 ≥ 0 的数值。"],
    ref: "F-N18 负专项附加字段级拒绝：与第 35 批 __sdAudit() 的明细负值 0 兜底分层——明细项按 0、主输入 special 为负则整页拒绝。默认态 2000 ⇒ 不命中。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { threshold: "-1" },
    clicks: ["calculate()"],
    expect: ["⚠ 起征点不能为负数，请填写 ≥ 0 的数值。", "20000\n3000\n0\n-1\n—"],
    ref: "F-N18 负起征点字段级拒绝：起征点为负会凭空放大应税所得，现拒绝且清结果。默认态 5000 ⇒ 不命中。"
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "2000", insurance: "3000", special: "0", threshold: "5000", bonus: "0" },
    clicks: ["calculate()"],
    expect: ["¥0.00\n¥0.00\n¥0.00\n3%", "社保公积金已超过税前月薪，税后收入按 0 显示（原始差额为负），请核对填写。"],
    ref: "F-N18 税后收入 0 下限与归因：月薪 2000、社保 3000（均为合法非负值）时旧实现显示「¥-1,000.00」；现 afterTax = max(0, 2000−3000−0) = ¥0.00，并在结果容器说明原始差额为负、请核对填写。默认态税后 ¥16,210.00 ⇒ 不命中。"
  },
  {
    slug: "finance/dca-calculator",
    inputs: { monthly: "1000", years: "10", rate: "8", initial: "0", target: "200000" },
    expect: ["达成所需年化收益率： 9.58%", "还需再提高 1.58 个百分点。"],
    ref: "止盈目标反推年化（2026-10-25 新增功能 / plan 条目）：月投 1000、10 年（120 期、期末投）、预期年化 8% 只能到 ¥182,946.04；反推达 ¥200,000 所需年化 = 9.58%（二分求解 FV(r)=target），比设定的 8% 高 1.58 个百分点。两条分别绑定求解结果与差额结论：**反推求解器、timing 口径（期初/期末）、百分点文案任一回归即变红**。target 为空（默认）时不渲染该段 ⇒ 零逃生。"
  },
  {
    slug: "finance/number-to-words",
    inputs: { inputVal: "900807.05" },
    expect: ["nine hundred thousand eight hundred seven", "point zero five"],
    ref: "去默认化：900807.05 → nine hundred thousand eight hundred seven point zero five。**同时守住两个已修 P0 缺陷**：① 小数位原用 decPart = n − intPart 的浮点差，900807.05 − 900807 = 0.04999999… ⇒ 会读成 point zero four nine nine…；② ones[0] 是空串（整数读法 0 不发音），原实现会把小数里的 0 吞掉 ⇒ 读成 point five。任一缺陷回归，本例即变红",
  },
  {
    slug: "finance/cagr",
    inputs: { start: "100", end: "200", years: "5" },
    clicks: ["calcTool()"],
    expect: ["14.87"],
    ref: "独立复算：CAGR=(200/100)^(1/5)−1=2^0.2−1=0.148698 ⇒ 14.87%（页面同步给出小数 0.1487）。默认起止/年限不同 ⇒ 不命中。",
  },
  {
    slug: "finance/isbn-validator",
    inputs: { isbnInput: "9780306406157" },
    clicks: ["validate()"],
    expect: ["0-306-40615-2"],
    ref: "ISBN-13 校验位可手算：978030640615 按权重 1/3 加权求和 ⇒ 校验位 7；去掉 978 与校验位后按组号/出版者/书名分段 ⇒ 对应 ISBN-10 为 0-306-40615-2。默认样例与注入不同 ⇒ 不命中。",
  },
  {
    slug: "finance/nric-validator",
    inputs: { input: "S1234567D" },
    expect: ["校验字母： D（期望 D）"],
    ref: "新加坡 NRIC：前缀 S（2000 年前出生公民）+ 7 位数字 1234567，按加权表 mod 11 得余数 ⇒ 校验字母 D。默认态输入不同 ⇒ 不命中。",
  },
  {
    slug: "finance/nric-validator",
    inputs: { input: "M1234567K" },
    expect: ["校验字母： K（期望 K） ✅ NRIC/FIN 号码有效"],
    ref: "MOM M 系列：加权和 106，加偏移 3，余数 10，反向索引官方 M 表得 K。",
  },
  {
    slug: "finance/nric-validator",
    inputs: { input: "M1234567X" },
    expect: ["校验字母： X（期望 K） ❌ 校验和失败，号码无效"],
    ref: "M 系列错误校验位不得通过。",
  },
  {
    slug: "finance/nric-validator",
    inputs: { input: "M0000004X" },
    expect: ["校验字母： X（期望 X） ✅ NRIC/FIN 号码有效"],
    ref: "MOM M 系列余数 0：加权和 8，加 3 后为 11，反向索引官方 M 表得 X。",
  },
  {
    slug: "finance/nric-validator",
    inputs: { input: "M0000009K" },
    expect: ["校验字母： K（期望 K） ✅ NRIC/FIN 号码有效"],
    ref: "MOM M 系列余数 10：加权和 18，加 3 后为 21，反向索引官方 M 表得 K。",
  },
  {
    slug: "finance/nric-validator",
    inputs: { input: "T1234567J" },
    expect: ["校验字母： J（期望 J） ✅ NRIC/FIN 号码有效"],
    ref: "T 前缀加权和 106 加 4，余数 0，NRIC 表得 J。",
  },
  {
    slug: "finance/nric-validator",
    inputs: { input: "F1234567N" },
    expect: ["校验字母： N（期望 N） ✅ NRIC/FIN 号码有效"],
    ref: "F 前缀加权和 106，余数 7，FIN 表得 N。",
  },
  {
    slug: "finance/nric-validator",
    inputs: { input: "G1234567X" },
    expect: ["校验字母： X（期望 X） ✅ NRIC/FIN 号码有效"],
    ref: "G 前缀加权和 106 加 4，余数 0，FIN 表得 X。",
  },
  {
    slug: "finance/ifsc-validator",
    inputs: { input: "HDFC0001234" },
    expect: ["分支代码： 001234"],
    ref: "IFSC = 4 位银行代码 + 保留位 0 + 6 位分支代码；HDFC0001234 ⇒ 银行 HDFC Bank、保留位 0、分支 001234。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/gstin-validator",
    inputs: { input: "27AAPFU0939F1ZV" },
    expect: ["校验位： V（期望 V）"],
    ref: "GSTIN 第 15 位为 mod-36 校验位：前 14 位字符编码按序加权求和 mod 36 ⇒ V。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/gstin-validator",
    inputs: { input: "99AAPFU0939F1ZK" },
    expect: ["州代码： 99 - Centre Jurisdiction（特殊辖区）（99 为 Centre Jurisdiction / Other Country 特殊注册码，不等同普通州）", "✅ GSTIN 有效（99 特殊辖区）"],
    ref: "F-N193 裁断回填（2026-11-21）：99 是 GST 已分配的特殊注册码（Centre Jurisdiction / Other Country OIDAR），不是「未分配州码」。校验位 K 正确 ⇒ 判格式有效，并加注「不等同普通州」。默认预填 09AABCU9603R1ZL 不含 99 ⇒ 不命中。",
  },
  {
    slug: "finance/routing-number-validator",
    inputs: { input: "011000015" },
    expect: ["前缀分类： 01 - 美联储第 1 区（Boston）"],
    ref: "ABA 路由号 9 位，按 3-7-1 权重加总 ⇒ 校验通过；前两位 01 对应波士顿联邦储备区。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/routing-number-validator",
    inputs: { input: "990000000" },
    expect: ["前缀 99 不在公开分配范围，无法判断该号码是否已分配"],
    ref: "F-N216 前缀白名单：前缀 99 校验和通过但未分配；旧实现仅报「99 - 未知/特殊用途」仍判 ✅，修复后直接 ❌。默认预填前缀 02 ⇒ 不命中，强判别。",
  },
  {
    slug: "finance/stock-profit-calculator",
    inputs: { buyPrice: "10", buyQty: "100", sellPrice: "12" },
    clicks: ["calc()"],
    expect: ["+189.38"],
    ref: "买入 100×10=1000、卖出 100×12=1200，价差 200 元扣双向佣金/印花税/过户费合计 10.62 ⇒ 净盈亏 +189.38（+18.84%），且 189.38+10.62=200 可对账。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { revenue: "1000", cogs: "600" },
    expect: ["毛利润 400.00 (40.0%)"],
    ref: "毛利=1000−600=400 ⇒ 毛利率 40.0%。默认态不同 ⇒ 不命中（期间费用沿用默认值的占比串不进锚）。",
  },
  {
    slug: "finance/imei-validator",
    inputs: { input: "490154203237518" },
    expect: ["TAC（前 8 位）： 49015420"],
    ref: "IMEI 分段：TAC 前 8 位 49015420、型号识别 490154、SNR 323751、校验位 8。该页同场结论存在自相矛盾（列出「期望校验位 0」仍判有效），属既有缺陷；本例只锁定可独立复算的分段解析段，不把缺陷结论固化进基线。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/portfolio-return",
    inputs: { r1: "10", r2: "5", w1: "50", w2: "50" },
    clicks: ["calcTool()"],
    expect: ["7.50"],
    ref: "组合预期收益 = 10×50% + 5×50% = 7.50%，权重合计 100%。默认态权重/收益不同 ⇒ 不命中。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "10000", salvage: "1000", life: "5" },
    clicks: ["calc()"],
    expect: ["1,800 直线法首年折旧"],
    ref: "可折旧总额 9000：直线法首年 (10000−1000)/5=1800、双倍余额 10000×2/5=4000、年数总和 5/15×9000=3000。锚取能独立复算的直线法值；默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "10000", salvage: "1000", life: "5.5" },
    clicks: ["calc()"],
    expect: ["使用年限须为 1–100 的整数（折旧按整年计提）"],
    ref: "小数年限 5.5 年：旧实现 parseInt 静默截断为 5 年、照常给出结果；现要求 1–100 整数年并提示。默认 5 年 ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "10", vc: "6", fc: "10000" },
    expect: ["2500 盈亏平衡销量(件)"],
    ref: "盈亏平衡销量 = 固定成本 /(单价−单位变动成本) = 10000/(10−6) = 2500 件，单位边际贡献 4.00 元、平衡收入 25,000 元。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "50", vc: "60", fc: "100000" },
    expect: ["不存在盈亏平衡点"],
    ref: "F-N59 亏损产品：单价 50 < 单位变动成本 60 ⇒ 单位边际贡献 −10、真实边际贡献率 −20%，不存在平衡点。旧实现硬写 cmRatio:0 得「−10.00 / 0.00%」自相矛盾；现明确拒绝。默认 price50/vc30 ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "50", vc: "30", fc: "-100000" },
    expect: ["固定成本、单位变动成本与销量不能为负数"],
    ref: "F-N59 负固定成本：fc=−100000 旧实现 beq=fc/cm 得 −5000 件、平衡收入 −250000 元仍照常渲染；现字段级拒绝。默认 fc=100000 ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "50", vc: "30", fc: "-100000" },
    clicks: ["scenarios=[];clearCanvas=function(){};addScenario();drawSensitivityChart=function(){};calcSensitivity();generateDetailTable();var calls=0;ToolBox.downloadText=function(){calls++};exportCSV();document.getElementById('__tbProbe').textContent='BEPGUARD scenarios='+scenarios.length+' sens='+(document.getElementById('sensGrid').innerHTML.indexOf('-5000')<0?1:0)+' detail='+(document.getElementById('detailTable').innerHTML.indexOf('-100,000')<0?1:0)+' exports='+calls;"],
    expect: ["BEPGUARD scenarios=0 sens=1 detail=1 exports=0"],
    ref: "负固定成本不能经场景、敏感性、明细和 CSV 入口绕过校验。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "50", vc: "60", fc: "100000" },
    clicks: ["scenarios=[];addScenario();var r=calcBEP(100000,50,60);document.getElementById('__tbProbe').textContent='BEPLOSS count='+scenarios.length+' ratio='+r.cmRatio+' compare='+(String(document.getElementById('scenarioCompare').innerHTML).indexOf('-20.00%')>=0?'OK':'BAD');"],
    expect: ["BEPLOSS count=1 ratio=-20 compare=OK"],
    ref: "亏损场景仍可比较，单价 50、成本 60 的真实边际贡献率为 −20%。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "50", vc: "30", fc: "0", sensPct: "0" },
    clicks: ["drawSensitivityChart=function(){};calcSensitivity();var h=String(document.getElementById('sensGrid').innerHTML);document.getElementById('__tbProbe').textContent='BEPZERO '+(h.indexOf('0 件')>=0&&h.indexOf('售价 +0%')>=0&&h.indexOf('NaN')<0?'OK':'BAD');"],
    expect: ["BEPZERO OK"],
    ref: "零固定成本合法；零变化幅度不得回退为 10% 或产生 NaN。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "50", vc: "30", fc: "100000" },
    clicks: ["clearCanvas=function(){};drawSensitivityChart=function(){};calc();calcSensitivity();generateDetailTable();var before=String(document.getElementById('sensGrid').innerHTML).indexOf('5000 件')>=0&&String(document.getElementById('detailTable').innerHTML).indexOf('100,000.00')>=0;document.getElementById('fc').value='-100000';calc();var s=String(document.getElementById('sensGrid').innerHTML),d=String(document.getElementById('detailTable').innerHTML);document.getElementById('__tbProbe').textContent='BEPSTALE '+(before&&s.indexOf('5000 件')<0&&d.indexOf('100,000.00')<0?'OK':'BAD');"],
    expect: ["BEPSTALE OK"],
    ref: "有效结果切换到负成本时清除敏感性与明细的旧数据。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "10", vc: "10", fc: "10000" },
    expect: ["不存在盈亏平衡点"],
    ref: "单位边际贡献 = 10−10 = 0 时原实现给 inf、页面显示「-」并仍渲染安全边际/经营杠杆；现明确提示不存在盈亏平衡点。默认 单价/成本不同 ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { price: "0", vc: "6", fc: "10000" },
    expect: ["请输入大于 0 的产品单价"],
    ref: "单价 0（空值或误填）原实现静默算出 inf/0 指标；现拦截提示。默认单价非 0 ⇒ 不命中。",
  },
  {
    slug: "finance/vat-calculator",
    inputs: { amount: "2000" },
    expect: ["不含税价 1,769.91", "230.09"],
    ref: "重写：原注入 rate（页面无此 id，真实为 customRate）且 amount=1000 恰为默认值 ⇒ 注入落空、断言「含税价 1,130.00」是默认态字面值。改为 amount=2000（默认 1000）、默认 13% 含税倒推 ⇒ 不含税 2000/1.13=1,769.91、税额 230.09、含税 2,000.00。默认态为 1,130.00 一档，两条均不命中。",
  },
  {
    slug: "finance/tax-bracket",
    inputs: { income: "60000" },
    clicks: ["calc()"],
    expect: ["应缴税款： 3,480 元"],
    ref: "应纳税所得额 60000 落入 10% 级（>36000），速算扣除数 2520 ⇒ 60000×10%−2520=3480。默认所得额不同 ⇒ 不命中。",
  },
  {
    slug: "finance/tax-bracket",
    inputs: { income: "36000" },
    clicks: ["calc()"],
    expect: ["34,920 元"],
    ref: "档位边界：36000 属 3% 档（0<所得≤36000），税 = 36000×3%−0 = 1080，税后余额 = 36000−1080 = 34920（锚动态余额而非静态税率表里的 3% / 1080）。若误写成 `<36000` 则落 10% 档，税仍巧合为 1080，但本条配合下一条 36001 的 10% 跳档可锁定边界。"
  },
  {
    slug: "finance/tax-bracket",
    inputs: { income: "36001" },
    clicks: ["calc()"],
    expect: ["34,920.9 元"],
    ref: "36001 落入 10% 档，税 = 36001×10%−2520 = 1080.1，税后余额 = 34920.9。与 36000 档仅差 1 元但税率跳档，两条余额锚共同锁定边界不含等号。默认 100000 不命中。"
  },
  {
    slug: "finance/number-to-words",
    inputs: { inputVal: "1234" },
    clicks: ["convert()"],
    expect: ["one thousand two hundred thirty-four"],
    ref: "1234 ⇒ one thousand two hundred thirty-four。与既有 900807.05 用例互补（后者守小数位缺陷，本例守整数段）。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "finance/number-to-words",
    inputs: { inputVal: "1000000000000" },
    clicks: ["convert()"],
    expect: ["超出范围（最大 ±999,999,999,999）"],
    ref: "F-N83 真锁：恰好 1e12 是页面声明上限之外的边界，必须拒绝。旧守卫 `> 1e12` 放过，numberToWords 的 scales 只到 billion ⇒ 单位丢失退化成「one」；现 `>= 1e12` 拦截。默认 1234567.89（远小于上限）不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "99.99" },
    clicks: ["convert()"],
    expect: ["玖拾玖元玖角玖分"],
    ref: "99.99 ⇒ 玖拾玖元玖角玖分（角、分各读一次，不漏「零」）。默认金额不同 ⇒ 不命中。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "100200300.00" },
    clicks: ["convert()"],
    expect: ["壹亿零贰拾万零叁佰元整"],
    ref: "W3-B 1亿+20万+300：亿→万、万→个位两级缺位各补一个「零」，角分为 0 加「整」⇒ 壹亿零贰拾万零叁佰元整。"
       + "旧整数分组不补零 ⇒ 壹亿贰拾万叁佰元整，本断言不命中。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "100000000.01" },
    clicks: ["convert()"],
    expect: ["壹亿元零壹分"],
    ref: "W3-B 1亿+1分：中间两组整为零 ⇒ 壹亿；有分无角补「零」⇒ 壹亿元零壹分。"
       + "旧实现整组零错拼成「壹亿万」且零位重复 ⇒ 输出与断言不符。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "1.005" },
    clicks: ["convert()"],
    expect: ["壹元零壹分"],
    ref: "第939批：改为拒绝超过两位小数，1.005 明示 3 位小数并停止转换，不再静默四舍五入到 0.01。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "1.999" },
    clicks: ["convert()"],
    expect: ["贰元整"],
    ref: "W3-B 分位进位满 100：1.999 → 2.00 ⇒ 贰元整。旧实现 f=100 后 CN[10] 不存在 ⇒ 输出「壹元undefined角」，本断言不命中。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "0.005" },
    clicks: ["convert()"],
    expect: ["零元零壹分"],
    ref: "W3-B 0.005 四舍五入到 0.01 ⇒ 零元零壹分（整数为 0 时仍完整输出元/角/分，不出现 undefined）。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "1.234" },
    clicks: ["convert()"],
    expect: ["壹元贰角叁分"],
    ref: "第939批：1.234 明示 3 位小数并拒绝，不再静默截断/取整为 1.23。",
  },
  {
    slug: "finance/word-frequency",
    inputs: { input: "apple banana apple cherry" },
    clicks: ["analyze()"],
    expect: ["apple 2 (50.00%)"],
    ref: "词频统计：apple 出现 2 次占 50%、banana/cherry 各 1 次占 25%（总 4 次），唯一词 3、TTR 75%。结果区同时给出英文 summary 行。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "finance/mirror-text",
    inputs: { input: "abc" },
    clicks: ["convert()"],
    expect: ["ɔdɒ"],
    ref: "逐字符镜像：a↔ɔ、b↔d、c↔ɔ ⇒ 输出 ɔdɒ（同时给出 transform: scaleX(-1) 的 CSS 方案）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/mirror-text",
    inputs: { input: "a😀b" },
    clicks: ["convert()"],
    expect: ["d😀ɒ"],
    ref: "F-N211 emoji 码点反转：a😀b → 映射 ɒ😀d → 按码点反转 d😀ɒ；旧实现 split('') 按 UTF-16 码元反转，把 😀 的代理项对拆成孤立代理输出乱码。默认态 Hello World! ⇒ 不命中。",
  },
  {
    slug: "finance/mirror-text",
    inputs: { input: "a👩‍💻🇨🇳👍🏽e\u0301😀𠀀b" },
    clicks: ["convert()"],
    expect: ["d𠀀😀ɘ\u0301👍🏽🇨🇳👩‍💻ɒ"],
    ref: "F-N211 字素簇倒序：ZWJ、国旗、肤色、组合重音内部顺序不变，单 emoji、增补汉字及映射字母也正确。",
  },
  {
    slug: "finance/mirror-text",
    clicks: ["var original=Intl.Segmenter;try{Intl.Segmenter=undefined;document.getElementById('input').value='a👩‍💻🇨🇳👍🏽e\\u0301b';convert();document.getElementById('__tbProbe').textContent='MIRRORFALLBACK='+document.getElementById('result').textContent;}finally{Intl.Segmenter=original;}"],
    expect: ["MIRRORFALLBACK=dɘ\u0301👍🏽🇨🇳👩‍💻ɒ"],
    ref: "无 Intl.Segmenter 的兼容回退：保持常见组合重音、肤色、旗帜和 ZWJ 簇。",
  },
  {
    slug: "automotive/vin-validator",
    inputs: { vinInput: "1M8GDM9AXKP042788" },
    clicks: ["validate()"],
    expect: ["校验位 (第 9) X"],
    ref: "VIN 17 位：WMI=1M8、VDS=GDM9AX（第 9 位为校验位 X）、VIS=KP042788，地区北美、年份 K ⇒ 1989/2019。校验位可独立复算（权重表 mod 11）。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "finance/abn-validator",
    inputs: { input: "51824753556" },
    expect: ["输入： 51824753556"],
    ref: "澳洲 ABN：首位 −1 后按权重 10,1,3,…,19 加权，求和 mod 89 = 0 即通过 ⇒ 51824753556 有效；expect 取页面回显的原始输入「输入： 51824753556」（含具体号码 ⇒ 默认预填 53004085616 回显 53004085616 不命中；刻意不取「校验和：✅ 通过」通用串，以免预填后默认态亦命中成逃生项）",
  },
  {
    slug: "finance/ein-validator",
    inputs: { input: "123456789" },
    expect: ["格式化： 12-3456789"],
    ref: "美国 EIN 按 2 位前缀 + 7 位序号格式化 ⇒ 12-3456789，并映射到 IRS 中心。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/swift-bic-validator",
    inputs: { input: "DEUTDEFF500" },
    expect: ["分支代码： 500"],
    ref: "BIC 11 位：银行代码 DEUT、国家 DE、位置 FF、分支 500；可独立按 4/2/2/3 分段校验。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/dni-validator",
    inputs: { input: "12345678Z" },
    expect: ["校验字母： Z（期望 Z）"],
    ref: "西班牙 DNI：8 位数字 mod 23 映射到字母表 TRWAGMYFPDXBNJZSQVHLCKE ⇒ 12345678 对应 Z。可手算，结论双写「实得/期望」判别力最强。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/dni-validator",
    inputs: { input: "12345678Z" },
    clicks: ["dniCheck=function(){return false;};validate();var h=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent='DNIFN '+document.getElementById('input').value+' '+(h.indexOf('❌ 校验字母不符，DNI 无效')>=0?'OK':'BAD');"],
    expect: ["DNIFN 12345678Z OK"],
    ref: "F-N205 复用锁：把页面顶层 dniCheck 临时替换为恒 false 后，validate() 的最终结论必须随之变 ❌；旧实现在 validate 内另算一遍 `letter === expected`，替换 dniCheck 不产生任何影响 ⇒ 探针 BAD。输入号绑定避免静态逃生。",
  },
  {
    slug: "finance/npi-validator",
    inputs: { input: "1234567890" },
    expect: ["❌ 校验和失败，NPI 无效"],
    ref: "美国 NPI 反例：80840 + 1234567890 的 Luhn 加权和 mod 10 ≠ 0 ⇒ 页面如实报「❌ 校验和失败，NPI 无效」。默认预填 4234567897 为有效号（Luhn 通过）⇒ 默认态显示「✅ 通过」，绝不出现失败串（与上一例正例互为镜像）。替代原「✅ 通过」通用串（预填后恒命中 ⇒ 逃生）。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "120000", annualRate: "6", loanYears: "10" },
    clicks: ["calc()"],
    expect: ["1,332.25 首月月供", "6.17% 有效年化（按月复利）"],
    ref: "等额本息月供 = P·i·(1+i)^n/((1+i)^n−1)，i=6%/12=0.005、n=120 ⇒ 1,332.25 元；首期利息 600.00、本金 732.25、剩余本金 119,267.75。有效年化 = (1+6%/12)^12−1 = **6.17%**，与名义 6% 并列。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "120000", annualRate: "6", loanYears: "2.5" },
    clicks: ["calc()"],
    expect: ["贷款年限须为正整数年"],
    ref: "贷款年限 2.5 年：旧实现按小数年限折期数（30 期）照算；现要求正整数年并提示。默认 30 年 ⇒ 不命中。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "120000", annualRate: "6", loanYears: "2" },
    clicks: ["calc();var before=scheduleData.length;document.getElementById('loanYears').value='2.3';calc();var noTable=!document.getElementById('scheduleTable').innerHTML&&!document.getElementById('yearlyTable').innerHTML;var exported=false;ToolBox.downloadText=function(){exported=true;};exportCSV();document.getElementById('__tbProbe').textContent='LOANSTALE '+(before===24&&scheduleData.length===0&&noTable&&!exported?'OK':'BAD');"],
    expect: ["LOANSTALE OK"],
    ref: "有效 2 年计划后改为非法 2.3 年，必须清空旧还款计划和表格并禁止导出旧数据。"
  },
  {
    slug: "investment/irr-calc",
    inputs: { cf0: "1000", cf1: "-1100", cf2: "0", cf3: "0", cf4: "0" },
    clicks: ["calcTool()"],
    expect: ["10.00 内部收益率 IRR (%)"],
    ref: "IRR 二分方向修正（investment/irr-calc）：现金流 1000,-1100,0,0,0 的真实根为 10%。修复前二分方向反置（npv(mid)>0 时误把 lo=mid）收敛到 hi=10 ⇒ 输出 1000%；修正为「扫掠找首个变号区间再标准二分」得 10.00%。默认态（cf0=-1000,300,400,500,200 ⇒ IRR≈15.32%）不含 10.00 串 ⇒ 强判别。",
  },
  {
    slug: "finance/simple-interest",
    inputs: { principal: "20000", rate: "4", years: "2" },
    clicks: ["calc()"],
    expect: ["累计利息： 1,600 元"],
    ref: "单利：每年利息 20000×4%=800，2 年累计 1,600，本利和 21,600。默认样例恰为 10000/5%/3 年 ⇒ 必须换一组数才破双态。",
  },
  {
    slug: "finance/simple-interest",
    inputs: { principal: "10000", rate: "10", years: "10" },
    clicks: ["calc()"],
    expect: ["25,937.42", "5,937.42"],
    ref: "同条件复利并列：10,000×(1+10%)^10 = **25,937.42**，比单利本利和 20,000 多 **5,937.42**。默认 10000/5%/3 年 ⇒ 复利 11,576.25、差额 1,576.25，不命中。",
  },
  {
    slug: "finance/credit-card-type",
    inputs: { input: "4111111111111111" },
    expect: ["卡片类型（前缀初步判断）： Visa"],
    ref: "卡BIN 识别：4111… 为 Visa（长度 16 校验通过）。默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "finance/currency-symbol",
    inputs: { searchInput: "USD" },
    clicks: ["showDetail()"],
    expect: ["共找到 1 种货币"],
    ref: "按关键字过滤货币表，`USD` 命中 1 种（附符号与详情页）。默认态（无关键字）命中数不同 ⇒ 不命中。",
  },
  {
    slug: "finance/inflation-calculator",
    inputs: { amt: "120000", rate: "2.5", years: "15" },
    clicks: ["switchMode('backward')"],
    expect: ["折现到现在，价值： ¥ 82,855.87"],
    ref: "反向模式（未来金额 → 现值）：PV = FV / (1+r)^n = 120,000 / 1.025^15 = **82,855.87**。旧实现把反向写成了 FV×(1+r)^n ⇒ 错误输出 185,060.29；输入刻意避开页面默认 100,000/3/20，否则注入失败时反向仍出 55,367.58、兜底 switchMode() 会误命中（逃生项）。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { cost: "10000", return: "12000", years: "2" },
    clicks: ["switchTab()"],
    expect: ["20.00% 总回报率 ROI"],
    ref: "ROI=(12000−10000)/10000=20.00%，净利润 +2,000 元，同场给出 10.00% 简单年化与 NPV 884.35。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { monthly: "1000", freq: "monthly", annualRate: "12", period: "5" },
    clicks: ["switchTab('regular')", "calcRegular()"],
    expect: [
      "82,486.37 期末终值",
      "37.48% 累计收益率（总收益/累计投入）",
      "12.00% 年化收益率（IRR·名义）",
      "12.68% 有效年化（IRR·复利）",
    ],
    ref: "定投 1,000/月、期初投入、年化 12%（月利率 1%）、5 年 ⇒ 终值 = 1000×((1.01^60−1)/0.01)×1.01 = 82,486.37，累计投入 60,000，累计收益率 22,486.37/60,000 = 37.48%；按 60 期 −1,000 与期末 +82,486.37 的真实现金流求每期 IRR=1%，名义年化 1%×12=12.00%、有效年化 1.01^12−1=12.68%。旧实现用累计投入开方年化只得约 6.57% ⇒ 本例不命中。默认态（月投 1,000/年化 8%/5 年）不同 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { monthly: "1500", freq: "weekly", annualRate: "6", period: "3" },
    clicks: ["switchTab('regular')", "calcRegular()"],
    expect: ["6.00% 年化收益率（IRR·名义）", "6.18% 有效年化（IRR·复利）"],
    ref: "周投 1,500、期初投入、年化 6%（周利率 6%/52）、3 年 ⇒ 156 期现金流求解每期 IRR，名义年化须回到 6.00%、有效年化 = (1+0.06/52)^52−1 ≈ 6.18%；两口径并存。默认态（月投/年化 8%）不同 ⇒ 不命中。",
  },
  {
    slug: "finance/currency-lookup",
    inputs: { input: "USD" },
    expect: ["US Dollar（美元）", "符号： $"],
    ref: "ISO 4217 查询：`USD` ⇒ 名称 US Dollar、符号 $、最小单位 2 位、使用地区美国。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/currency-lookup",
    inputs: { input: "JPY" },
    expect: ["最小单位位数： 0（无小数）"],
    ref: "F-N87 真锁：最小单位位数说明须闭合括号「0（无小数）」。旧实现缺右括号渲染成「0（无小数」，现补全。默认态 EUR 是「2（1/100）」不含该串 ⇒ 零逃生；JPY 为 0 位小数，绑定输入。",
  },
  {
    slug: "finance/vcard-qr",
    inputs: { fn: "Zhang", ln: "San", org: "ACME", title: "Eng", tel: "13800138000", email: "a@b.com", url: "https://a.com" },
    clicks: ["generate()"],
    expect: ["FN:ZhangSan"],
    ref: "vCard 3.0 文本：姓/名写入 `N:San;Zhang;;;`，字段名用大写驼峰（`FN`/`ORG`/`TEL`/`EMAIL`/`URL`），电话带 `;TYPE=CELL`。产物与输入形态不同 ⇒ 天然非回显。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/vcard-qr",
    inputs: { fn: "李四", ln: "测试", org: "ACME", title: "Eng", tel: "13900000000", email: "li@example.com", url: "https://li.example.com" },
    clicks: ["var cap={};qrcode=function(t,e){cap.ec=e;return {addData:function(d){cap.data=d;},make:function(){cap.made=true;},getModuleCount:function(){return 21;},isDark:function(r,c){return r===0&&c===0;}};};qrcode.stringToBytesFuncs={'UTF-8':function(){}};var txt=buildVcard();var g=renderQR(txt);document.getElementById('__tbProbe').textContent='VCREAL '+document.getElementById('fn').value+' '+(cap.data===txt&&cap.ec==='M'&&cap.made&&g&&g.length===29&&g[4][4]===1?'OK':'BAD');"],
    expect: ["VCREAL 李四 OK"],
    ref: "F-N223 真编码锁：用可控 qrcode 桩替换后，renderQR 必须把 buildVcard() 全文交给 qrcode(0,'M').addData()/make()，并按 getModuleCount()+4 静区生成网格；旧伪随机网格既不调用库也不产生 29×29 静区布局 ⇒ 探针 BAD。输入姓名绑定避免静态逃生。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { strike: "100", premium: "5", s0: "300", contracts: "1", mult: "100", fee: "0" },
    clicks: ["calc();var n=document.getElementById('chartNote');document.getElementById('__tbProbe').textContent='OPTITM '+(n&&n.textContent.indexOf('300')>=0?'OK':'BAD');"],
    expect: ["OPTITM OK"],
    ref: "第934批：深度实值 S=300 必须进入横轴范围并在图下注明；旧范围 K±max(0.4K,4p)=60–140 会丢掉当前价标记。默认 S=110 ⇒ 不命中。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { strike: "100", premium: "5", s0: "10", contracts: "1", mult: "100", fee: "0" },
    clicks: ["calc();var n=document.getElementById('chartNote');document.getElementById('__tbProbe').textContent='OPTOTM '+(n&&n.textContent.indexOf('10')>=0?'OK':'BAD');"],
    expect: ["OPTOTM OK"],
    ref: "第934批：深度虚值 S=10 同样纳入横轴并标注；旧范围 60–140 不显示当前情景。默认 S=110 ⇒ 不命中。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { s0: "100", strike: "105", premium: "3", mult: "100", fee: "1" },
    clicks: ["switchTab()"],
    expect: ["盈亏平衡点： 108.02 元", "全区间最大净亏损： ¥302.00"],
    ref: "看涨买方：盈亏平衡点 = 105 + 3 + 手续费/股 0.02 = 108.02 元；到期价 100 < 行权价 ⇒ 不行权，全区间最大净亏损 = 权利金 300 + 手续费 2 = ¥302.00。修复后平衡点也含手续费，与总盈亏同口径；默认 fee=2 ⇒ 108.04 不同 ⇒ 不命中。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { s0: "100", strike: "110", premium: "5", mult: "100", fee: "3", contracts: "2" },
    expect: ["全区间指标的价格 S ≥ 0；最大/最小净盈亏已计入开仓+平仓手续费（¥12.00）"],
    ref: "F-N58 含费口径专用锁：手续费 3元/张 × 2 张 × 开平 2 次 = ¥12.00，新增说明行须回显该金额并声明全区间最大/最小净盈亏与总盈亏同口径。旧实现无此行 ⇒ 不命中；默认 fee=2/1张 ⇒ ¥4.00 ⇒ 不命中。绑定输入算得的手续费金额，避免静态文案逃生；该行在四种 tab 状态下均渲染，不受 harness 跨用例 tab 状态污染影响。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { s0: "100", strike: "105", premium: "0", mult: "100", fee: "0" },
    clicks: ["switchTab()"],
    expect: ["行权价与期权金需大于 0"],
    ref: "期权金 0（空值）原实现照算、盈亏平衡点 = 行权价，显示「保本」；现拦截提示。默认权利金 3 ⇒ 不命中。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { s0: "100", strike: "105", premium: "3", mult: "100", fee: "-10" },
    clicks: ["switchTab()"],
    expect: ["手续费不能为负数"],
    ref: "负手续费原实现让总亏损变小、甚至出现「手续费补贴」；现拦截提示。默认手续费 1 ⇒ 不命中。",
  },
  {
    slug: "finance/credit-card-bin",
    inputs: { input: "411111" },
    expect: ["发卡机构： Chase Bank (测试卡)"],
    ref: "BIN 库查询：`411111` ⇒ 网络 Visa、类型 Credit、国家 US、机构 Chase Bank（测试卡）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/credit-card-bin",
    inputs: { input: "220012" },
    expect: ["BIN： 220012 卡片网络： MIR"],
    ref: "F-N88 真锁：220012 是 MIR BIN（2200–2204），须判 MIR。旧正则 Mastercard `2[2-7]\\d{2}` 先命中且 MIR 排其后 ⇒ 判 Mastercard，反相变红；默认 411111 判 Visa、不含该串 ⇒ 零逃生。",
  },
  {
    slug: "finance/credit-card-bin",
    inputs: { input: "272100" },
    expect: ["BIN： 272100 卡片网络： 未知网络"],
    ref: "F-N88 真锁：272100 超出 Mastercard 2 系列精确上界 2720 ⇒ 未知网络。旧正则 `2[2-7]\\d{2}` 泛吞 2700–2799 ⇒ 判 Mastercard，反相变红；默认 411111 判 Visa、不含该串 ⇒ 零逃生。",
  },
  {
    slug: "finance/bic-lookup",
    inputs: { input: "DEUTDEFF500" },
    expect: ["银行名称： Deutsche Bank (德国)"],
    ref: "BIC 反查：`DEUTDEFF500` ⇒ 银行代码 DEUT ⇒ Deutsche Bank（德国）、国家 DE、位置 FF、分支 500。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/bic-lookup",
    inputs: { input: "Deutsche Bank" },
    expect: ["按行名检索：DEUTSCHE BANK", "DEUT — Deutsche Bank (德国)"],
    ref: "F-N186 反向按行名检索：`Deutsche Bank` 含空格非 BIC 形态 ⇒ 在 BANK_DB 银行名中大小写不敏感命中 DEUT。旧实现取前 4 位 DEUT 命中后因长度 13 报「BIC 长度应为 8 或 11 位」，无检索能力。默认预填 CHASUS33 ⇒ 不命中。",
  },
  {
    slug: "finance/bic-lookup",
    inputs: { input: "NotARealBank" },
    expect: ["离线库中未找到匹配的行名"],
    ref: "F-N186 反向检索无匹配：非 BIC 形态且无行名命中 ⇒ 明确提示未找到；旧实现取前 4 位 NOTA 未收录并报长度错误。默认预填 CHASUS33 ⇒ 不命中。",
  },
  {
    slug: "finance/bic-lookup",
    inputs: { input: "ABCDEFGH" },
    expect: ["国家代码： EF - 非 ISO 3166-1 国家码", "❌ 国家代码 EF 不是 ISO 3166-1 alpha-2 代码", "❌ BIC 格式校验失败（长度须为 8 或 11 位，且国家/位置/分支码均须合法）"],
    ref: "F-N187 国家码白名单：EF 非 ISO 3166-1 alpha-2，旧实现仅显示「未知」并按长度判 ✅；修复后必须拒绝。默认 CHASUS33 国家 US 合法 ⇒ 不命中。",
  },
  {
    slug: "finance/bic-lookup",
    inputs: { input: "DEUTPTFF" },
    expect: ["国家代码： PT - 有效 ISO 代码（离线库未收录）"],
    ref: "F-N187 防误伤：PT 是 ISO 3166-1 有效代码但不在 23 项离线名称库，不能因名称缺失误判格式无效；旧实现显示「未知」但仍 ✅，新实现明确标注有效 ISO 后仍 ✅。默认国家 US 在名称库 ⇒ 不命中。",
  },
  {
    slug: "finance/postal-code-validator",
    inputs: { input: "100000" },
    expect: ["中国（CN）：6 位数字"],
    ref: "6 位数字邮编匹配多国格式：`100000` 命中 RU/CN/IN/SG 及「香港无邮编系统」。锚取可独立核对的国家条目。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/postal-code-validator",
    inputs: { input: "HELLO" },
    expect: ["不匹配任何已知国家的邮编格式"],
    ref: "F-N218 香港 /.*/ 默认通过：无前缀任意串 `HELLO` 旧实现仅命中香港显示「✅ 香港无邮编系统（默认通过）」，修复后香港仅在显式 HK: 前缀参与 ⇒ 落入「不匹配任何已知国家的邮编格式」。默认 100000 命中多国 ⇒ 不命中。",
  },
  {
    slug: "finance/postal-code-validator",
    inputs: { input: "HK:任意内容123" },
    expect: ["中国香港（HK）：香港无邮编系统"],
    ref: "F-N218 防误伤：显式 `HK:` 前缀仍应命中香港条目（香港无邮编系统，接受任意内容）；与无前缀 HELLO 被拒形成对照。默认 100000 不命中香港 ⇒ 不命中。",
  },
  {
    slug: "finance/postal-code-validator",
    inputs: { input: "1000001" },
    expect: ["日本（JP）：3-4 格式（连字符可省）"],
    ref: "F-N219 日本无连字符邮编：`1000001`（东京 100-0001）7 位数字应命中 JP；旧正则强制 `\\d{3}-\\d{4}` 拒之，仅命中香港被误判国家。默认 100000 不命中 JP ⇒ 不命中。",
  },
  {
    slug: "finance/postal-code-validator",
    inputs: { input: "01310100" },
    expect: ["巴西（BR）：5-3 格式（连字符可省）"],
    ref: "F-N219 巴西无连字符邮编：`01310100`（01310-100）8 位数字应命中 BR；旧正则强制连字符拒之，仅命中香港。默认 100000 不命中 BR ⇒ 不命中。",
  },
  {
    slug: "finance/zip-code-validator",
    inputs: { input: "95014" },
    expect: ["前 3 位（SCF）： 950"],
    ref: "美国 ZIP：`95014` ⇒ 5 位 ZIP + 前 3 位 SCF 950（未映射到已知州/地区）。expect 只锁依赖输入的「前 3 位（SCF）： 950」；原第二条「✅ ZIP Code 格式有效」为通用串，默认预填 10001 也有效 ⇒ 恒命中变逃生，已删除。",
  },
  {
    slug: "finance/zip-code-validator",
    inputs: { input: "00000" },
    expect: ["输入： 00000 ❌ ZIP 00000–00500、99951–99999 为 USPS 未分配段"],
    ref: "F-N208 未分配段：00000 形状合法但不在 USPS 00501–99950 分配范围，旧实现判「✅ 格式有效」；修复后 ❌。默认预填 10001 ⇒ 不命中。",
  },
  {
    slug: "finance/zip-code-validator",
    inputs: { input: "99999" },
    expect: ["输入： 99999 ❌ ZIP 00000–00500、99951–99999 为 USPS 未分配段"],
    ref: "F-N208 未分配段：99999 超出 USPS 上限 99950，旧实现判「✅ 格式有效」；修复后 ❌。expect 带输入号区分 00000 用例。默认预填 10001 ⇒ 不命中。",
  },
  {
    slug: "finance/voter-id-validator",
    inputs: { input: "ABC1234567" },
    expect: ["三字母前缀： AB•（仅格式字段，不推断邦/州或签发机构）", "不核验该号码是否已登记"],
    ref: "印度 EPIC 选民 ID：3 字母 + 7 位序号，仅格式校验。F-N213 州码行加「未核对有效性」标注，避免任意 3 字母被误当合法州码；expect 带输入州码 ABC（默认 XYZ 不命中）⇒ 强判别，静态标注串单列会逃生故不单列。",
  },
  {
    slug: "finance/imsi-validator",
    inputs: { input: "310150123456789" },
    expect: ["MNC（第 4-6 位）： 150 - 未知运营商 移动用户识别码 MSIN： 123456789"],
    ref: "MCC 310 的 MNC 为三位，未收录 150 也不能截成两位。",
  },
  {
    slug: "finance/imsi-validator",
    inputs: { input: "310410123456789" },
    expect: ["MNC（第 4-6 位）： 410 - AT&T 移动用户识别码 MSIN： 123456789"],
    ref: "F-N217 三位 MNC：310410（AT&T）第 4-6 位 MNC 在库命中 ⇒ 按 3 位展示、MSIN 从第 7 位切 123456789；旧实现固定 2 位显示 41、MSIN 多带一位 0123456789。默认预填 460001234567890（2 位 MNC 00）⇒ 不命中。",
  },
  {
    slug: "finance/imsi-validator",
    inputs: { input: "460011234567890" },
    expect: ["MNC（第 4-5 位）： 01 - China Unicom 中国联通"],
    ref: "中国 460 的 MNC 使用两位。",
  },
  {
    slug: "finance/imsi-validator",
    inputs: { input: "999123456789012" },
    expect: ["MNC 位数无法确定，无法解析 MNC 和 MSIN"],
    ref: "未知 MCC 不应猜测 MNC 长度和 MSIN。",
  },
  {
    slug: "finance/meid-validator",
    inputs: { input: "490154203237518" },
    expect: ["制造商代码（前 8 位）： 49015420", "序列号（后 6 位）： 323751"],
    ref: "MEID 十六进制形态：前 8 位 49015420 为制造商码、后 6 位 323751 为序列号。该页同场的「校验位： 8（期望 C）❌ 校验失败」与 `it/imei-validator` 对同一号码的结论相反，属既有缺陷；本例只锁定可独立复算的分段解析段。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/meid-validator",
    inputs: { input: "A0000012345678G" },
    expect: ["输入： A0000012345678G ❌ 含非法字符（仅允许 0-9、A-F 及空格/连字符）"],
    ref: "F-N206 非 hex 字符剥离：旧实现 replace(/[^0-9A-F]/g,'') 把 G 剥离后按 14 位合法 MEID 判 ✅；修复后含 G 直接拒绝。默认预填 A0000012345678（纯 hex）⇒ 不命中。",
  },
  {
    slug: "finance/meid-validator",
    inputs: { input: "A000-0012-3456-78" },
    expect: ["输入： A000-0012-3456-78 格式： 十六进制（14 位） 制造商代码（前 8 位）： A0000012"],
    ref: "F-N206 防误伤：常见连字符分隔写法仍允许（分隔符清洗后按 14 位 hex 解析），制造商码 A0000012。与含 G 被拒形成对照。默认预填不同 ⇒ 不命中。",
  },
  {
    slug: "finance/meid-validator",
    inputs: { input: "A0000012345679" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='MEIDFIX '+document.getElementById('input').value+' '+((h.indexOf('⚠ 仅格式通过，未提供校验位，无法完成校验')>=0&&h.indexOf('十进制表示： 045035996579124857（同一 MEID）')>=0&&h.indexOf('校验算法： 参考 Luhn Base16（非标准，仅供格式自检）')>=0)?'OK':'BAD');"],
    expect: ["MEIDFIX A0000012345679 OK"],
    ref: "F-N207 三合一锁：14 位 hex 缺校验位时旧实现一律 ✅，且无 hex↔dec 换算、算法自称 Luhn-like；修复后必须同时给出「无法完成校验」、十进制等价 045035996579124857 与非标准算法标注。输入号绑定避免静态逃生。",
  },
  {
    slug: "finance/meid-validator",
    inputs: { input: "045035996579124856" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='MEIDDEC '+document.getElementById('input').value+' '+(h.indexOf('十六进制表示： A0000012345678（同一 MEID）')>=0?'OK':'BAD');"],
    expect: ["MEIDDEC 045035996579124856 OK"],
    ref: "F-N207 十进制→十六进制互证：BigInt('045035996579124856').toString(16) 补零为 A0000012345678，页面必须展示同一 MEID 的十六进制表示；旧实现无任何换算行 ⇒ 探针 BAD。输入号绑定避免静态逃生。",
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "100000", rate: "5", months: "360", monthly: "536.82", prepay: "10000" },
    clicks: ["calc()"],
    expect: ["含本次提前还款的总支出（元） 164820.20 184204.90", "较对照方案节省（元） 28436.35 9051.66"],
    ref: "F-N224 新口径下重写（F-N224/F-N233 同批改测试）：以「同月供 536.82、不提前还款」为对照，逐期精确摊还 361 期、总还款 193256.56；提前还 10000 后① 289 期、累计 154820.20，② 月供降至 482.56、361 期累计 174204.90。**本次提前偿还的 10000 元本金仍是支出**：含本金的真实总支出分别为 164820.20 / 184204.90，节省 28436.35 / 9051.66。旧 P1 缺陷（漏减 prepay）若回归，两条 expect 立即变红。显式注入 monthly 使本例不受默认月供调整影响；默认态（500000/4.5/240/3163.25/20000）不含这些数值 ⇒ 零逃生。",
  },
  {
    slug: "finance/retirement-calculator",
    inputs: {
      currentSavings: "100000",
      monthlyContribution: "5000",
      returnRate: "5",
      inflation: "3",
      retireAge: "60",
      lifeAge: "90",
      monthlyExpense: "8000",
    },
    clicks: ["calc()"],
    expect: ["450.91万 退休时资产（名义）", "77.4% 资金充足度"],
    ref: "30 岁起每月存 5,000、60 岁退休、lifeAge 90：名义退休资产 441.85 万，4% 法则所需 582.54 万 ⇒ 充足度 75.8%（不足），退休后实际月支取 6,675.55 元。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/dea-validator",
    inputs: { input: "ABC123" },
    expect: ["长度必须为 9 字符（2 字母 + 7 数字）"],
    ref: "DEA 编号规则 = 2 字母 + 7 数字共 9 位，`ABC123` 只有 6 位 ⇒ 长度校验直接失败。默认态为空输入，不命中本串。",
  },
  {
    slug: "finance/dea-validator",
    inputs: { input: "AB0134623" },
    expect: ["7 位数字： 0134623 校验和： ✅ 通过 ✅ DEA 号码有效"],
    ref: "DEA 校验：奇数位 0+3+6=9，偶数位之和 (1+4+2)×2=14，总和 23，校验位为 3。",
  },
  {
    slug: "finance/dea-validator",
    inputs: { input: "AB0118785" },
    expect: ["7 位数字： 0118785 校验和： ❌ 未通过 ❌ 校验和失败，DEA 号码无效"],
    ref: "DEA 校验：奇数位 0+1+7=8，偶数位之和 (1+8+8)×2=34，总和 42，校验位应为 2，而非 5。",
  },
  {
    slug: "finance/dea-validator",
    inputs: { input: "AB1234563" },
    expect: ["7 位数字： 1234563 校验和： ✅ 通过 ✅ DEA 号码有效"],
    ref: "DEA 校验：1+3+5+2×(2+4+6)=33，取个位 3；不能对乘积逐位求和。",
  },
  {
    slug: "finance/dea-validator",
    inputs: { input: "AB1234565" },
    expect: ["7 位数字： 1234565 校验和： ❌ 未通过 ❌ 校验和失败，DEA 号码无效"],
    ref: "DEA 反例：123456 的正确校验位是 3，而非 5。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: { initial: "2000", monthly: "300", rate: "4", years: "5" },
    clicks: ["switchTiming()"],
    expect: ["¥22,331.69"],
    ref: "初始 2,000 + 每月定投 300、共 60 期、年化 4%（月末扣款）⇒ 期末 22,331.69、累计收益率 +11.66%。刻意换掉默认的首组参数（默认 initial 1,000/monthly 500/rate 5/years 10 得 79,288.15）⇒ 不命中。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: {
      initial: "10000",
      monthly: "1000",
      rate: "8",
      years: "10",
      buyFee: "0.5",
      sellFee: "0.5",
      manageFee: "1",
      custodyFee: "0.2",
    },
    clicks: ["setRate(8)"],
    expect: ["费用合计 ¥12,291.97"],
    ref: "初始申购费 50、月投申购费 600、加赎回费；月末按增长后净值买入，期末资产 188,989.59，费用合计改为 12,291.97：除申购费 650、赎回费 944.95 外，新口径把逐月计提的管理费 10,728.63 与托管费 2,145.73 一并计入；净值得失仍由扣除费率后的月收益率驱动，不重复扣减。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: { rate: "12" },
    clicks: ["clearHistory();document.getElementById('rate').value='12';setRate();calc();"],
    expect: ["有效年化（按月复利） 12.68%"],
    ref: "无参调用 setRate() 不得把利率写成 undefined/0：注入 12% 后应保持 12%，并列显示名义 12.00% 与按月复利有效年化 (1+12%/12)^12−1 = 12.68%。默认 8% ⇒ 8.30%，不命中。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: { initial: "10000", monthly: "1000", years: "10", rate: "8" },
    clicks: ["document.getElementById('__tbProbe').textContent='FN45IRR='+calcIRR(getVal('monthly'),getVal('initial'),getVal('years')*12,184434.02,true).toFixed(2)"],
    expect: ["FN45IRR=6.32"],
    ref: "F-N45 月初扣款 IRR 时点：initial 10000 / monthly 1000 / 10 年 / 8%，月末扣款 IRR 6.40%（现金流 t=0 初始、t=1..120 月投、t=120 回收）；月初扣款首期应落在 t=0，真实现金流 IRR 6.32%。旧实现 monthStart 形参传入 calcIRR 却完全未使用，月初仍算成 6.40% ⇒ 不命中。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: {
      initial: "0",
      monthly: "0",
      rate: "0",
      years: "10",
      buyFee: "0",
      sellFee: "0",
      manageFee: "0",
      custodyFee: "0",
    },
    clicks: ["calc()"],
    expect: ["无法计算（请输入有效现金流）"],
    ref: "全 0 输入：初始本金、月定投、费率均为 0 ⇒ 现金流全 0、无正负号变化，IRR 无根。旧二分法把 high 一路压到 −0.5，输出 −600.00% 假结果；修复后应显示「无法计算（请输入有效现金流）」。默认/正常输入仍输出有限 IRR ⇒ 本用例可区分。",
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: { pv: "100000", months: "60", downPct: "10", rate: "0", fee: "1000" },
    clicks: ["calc()"],
    expect: ["每月还款：¥1,500.00"],
    ref: "租赁物 100,000、首付 10%（10,000）⇒ 融资金额 90,000，分 60 期等额本息 ⇒ 月供 1,500.00，总还款 101,000。该页名义利率注入不生效（显示 0.00%），故只锚与利率无关的本金/期数派生量。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-calculator",
    inputs: { initial: "10000", additional: "1000", years: "10", final: "25000" },
    clicks: ["calc()"],
    expect: ["期末价值： 25,000 元", "累计回报率： 127.27%"],
    ref: "初始 10,000 + 追加 1,000（共 11,000）⇒ 期末 25,000，累计回报率 (25000−11000)/11000 = 127.27%，CAGR 8.56%。默认态 final=18000 得 累计回报率 38.46% ⇒ 不命中。",
  },
  {
    slug: "finance/number-to-words-chinese",
    inputs: { inputVal: "1234" },
    clicks: ["convert()"],
    expect: ["一千二百三十四"],
    ref: "1234 的中文读法：一千二百三十四（「二」非「两」，十位「十」不补零）。默认态为空输入，不命中。",
  },
  {
    slug: "finance/number-to-words-chinese",
    inputs: { inputVal: "4.499999" },
    clicks: ["convert()"],
    expect: ["中文读法： 四点四九九九九九"],
    ref: "中文读数按输入字符串逐位读小数、保留末尾零：4.499999 ⇒ 四点四九九九九九，不再四舍五入成四点五。",
  },
  {
    slug: "finance/number-to-words-chinese",
    inputs: { inputVal: "9.99999" },
    clicks: ["convert()"],
    expect: ["中文读法： 九点九九九九九"],
    ref: "中文读数按输入字符串逐位读小数、保留末尾零：9.99999 ⇒ 九点九九九九九，不再四舍五入进位成十。",
  },
  {
    slug: "finance/number-to-words-chinese",
    inputs: { inputVal: "1.23456" },
    clicks: ["convert()"],
    expect: ["一点二三四五六"],
    ref: "中文读数按输入字符串逐位读小数：1.23456 ⇒ 一点二三四五六，不截断也不进位。",
  },
  {
    slug: "finance/iccid-validator",
    inputs: { input: "8986011234567890123" },
    expect: ["国家代码（E.164，变长）： 86", "校验位： 3"],
    ref: "ICCID 19 位：前 2 位 89 = ITU 电信、第 3-4 位 86 = 中国、第 5-7 位 011 = 发卡机构、末位 3 为 Luhn 校验位。该号 Luhn 实际不通过（页内如实报「❌ 校验失败」），本例只锁分段解析段。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/iccid-validator",
    inputs: { input: "8930123456789012347" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='FN182 '+document.getElementById('input').value+' '+((h.indexOf('30 - 希腊')>=0&&h.indexOf('无法由此不完整的代码表确定')>=0&&h.indexOf('Japan')<0)?'OK':'BAD');"],
    expect: ["FN182 8930123456789012347 OK"],
    ref: "E.164 国家码 30 为希腊，不应凭不可靠前缀表推断日本运营商。",
  },
  {
    slug: "finance/iccid-validator",
    inputs: { input: "88123456789012345676" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='FN183 '+document.getElementById('input').value+' '+((h.indexOf('非 89 电信行业标识，不是 ICCID')>=0&&h.indexOf('✅ ICCID 有效')<0)?'OK':'BAD');"],
    expect: ["FN183 88123456789012345676 OK"],
    ref: "F-N183 非 89 前缀拒绝：88123456789012345676 为 20 位、Luhn true，但 MII=88 非电信标识；旧实现只看 Luhn ⇒「✅ ICCID 有效」自相矛盾；新实现非 89 直接判「❌ 非 89 电信行业标识，不是 ICCID」。默认预填 89 ⇒ 不命中。",
  },
  {
    slug: "finance/iccid-validator",
    inputs: { input: "89123456789012345675" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='FN184 '+document.getElementById('input').value+' '+((h.indexOf('国家代码（E.164，变长）： 1 - 北美')>=0&&h.indexOf('国家代码（E.164，变长）： 12')<0)?'OK':'BAD');"],
    expect: ["FN184 89123456789012345675 OK"],
    ref: "F-N184 变长国家码最长匹配：891234... 的 89 之后国家码为 1 位（E.164 NANP=1），旧实现固定 substring(2,4)取'12'判未知⇒错位；新实现 E.164 表 3→1 位最长匹配命中 1=北美（NANP）。该号 Luhn 通过、非默认预填 ⇒ 零逃生。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "49155402372518" },
    expect: ["国家代码： +49 - 德国", "E.164 格式： +49155402372518"],
    ref: "E.164：去掉前缀 0 后 14 位 ≤ 15 上限，+49 为德国。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "+44" },
    expect: ["❌ 缺少国内号码"],
    ref: "只有英国国家码，不是完整号码。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "+49" },
    expect: ["❌ 缺少国内号码"],
    ref: "只有德国国家码，不是完整号码。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "+44 1" },
    expect: ["⚠️ 已识别国家码，但未校验该国家的国内号码格式或长度"],
    ref: "英国短号不得断言有效，仅报告缺少对应国别规则。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "+44 7911 123456" },
    expect: ["⚠️ 已识别国家码，但未校验该国家的国内号码格式或长度"],
    ref: "英国号码也只能识别前缀，不能未经规则确认有效。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "+1 2025550123" },
    expect: ["✅ 符合 NANP 10 位号码格式"],
    ref: "NANP 的 10 位长度规则保持有效。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "+86 13900139000" },
    expect: ["归一化： 8613900139000"],
    ref: "中国号码规则保持有效。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "13800138000" },
    expect: ["缺国家码，无法判定（疑似 +86 中国大陆手机号）"],
    ref: "F-N215 本地号误判：无 + 的中国 11 位号旧实现命中前缀 '1' 硬判美加 +1、国内 3800138000 + NANP 通过；修复后提示疑似 +86 缺国家码。默认预填 +86 13800138000 ⇒ 不命中。",
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "999999999999" },
    expect: ["❌ 国家码未识别，无法验证号码格式"],
    ref: "F-N215 未识别国家码：CC_DB 无 999/99/9 前缀，旧实现落入本地号分支仍输出「✅ MSISDN 格式有效」零区分度；修复后 ❌。默认预填 +86 ⇒ 不命中。",
  },
  {
    slug: "finance/pan-validator",
    inputs: { input: "AAACN0927F" },
    expect: ["末位字母： F（PAN 无算术校验位，仅结构校验） ✅ PAN 号码格式有效"],
    ref: "印度 PAN：10 位，第 4 位 C = Company，前 5 位 AAACN 为实体代码，0927 为序号，末位 F 为结构字母。F-N200 把误导性「校验位」改为诚实标注。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/pan-validator",
    inputs: { input: "ABCZS1234E" },
    expect: ["❌ 第 4 位实体类型 Z 非官方类型（仅 A/B/C/F/G/H/J/L/P/T）"],
    ref: "F-N199 未知实体类型：第 4 位 Z 不在官方 10 种内，旧实现显示「未知类型」仍判 ✅；修复后 ❌。默认预填第 4 位 P（合法）⇒ 不命中。",
  },
  {
    slug: "finance/pan-validator",
    inputs: { input: "ABCKS1234E" },
    expect: ["❌ 第 4 位实体类型 K 非官方类型（仅 A/B/C/F/G/H/J/L/P/T）"],
    ref: "F-N199 非官方类型：K (Krishik) 非印度税务官方实体类型，旧表收录并判 ✅；修复后从表中移除并判 ❌。默认预填 P ⇒ 不命中。",
  },
  {
    slug: "finance/tin-validator",
    inputs: { input: "123456789" },
    expect: ["SSN 格式： 123-45-6789", "Area： 123 Group： 45 Serial： 6789"],
    ref: "美国 TIN 中的 SSN：9 位分三段 123-45-6789（Area/Group/Serial）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/uan-validator",
    inputs: { input: "333333333333" },
    expect: ["前 2 位（展示切片，非官方语义）： 33 中 5 位（展示切片，非官方语义）： 33333"],
    ref: "F-N149 分段口径中性化：旧输出「区域：33 / EPFO 办公室：33333」暗示官方字段语义但 EPFO 未公开该映射；改为纯展示切片并显式标注非官方语义，绑定输入值 33/33333 ⇒ 默认态不命中、旧源码无该文案。",
  },
  {
    slug: "finance/sort-code-validator-validator",
    inputs: { input: "112233" },
    expect: ["银行归属： 不推断", "银行归属：不推断"],
    ref: "第944批移除前两位静态银行推断；只保留格式校验与银行归属不推断说明。",
  },
  {
    slug: "finance/sort-code-validator-validator",
    inputs: { input: "12A34B56" },
    expect: ["输入： 12A34B56 ❌ Sort Code 仅允许数字、空格或连字符，含字母为格式错误"],
    ref: "F-N197 含字母拒绝：旧实现 replace(\\D,'') 剥离 A/B 后按 123456 判 ✅ 并给银行名；deep-dive 却承诺含字母提示格式错误。修复后直接拒绝。默认预填 200000 ⇒ 不命中。",
  },
  {
    slug: "finance/nie-validator",
    inputs: { input: "12345678Z" },
    expect: ["首字符为 X/Y/Z，中间 7 位数字，末尾大写字母"],
    ref: "西班牙 NIE 须以 X/Y/Z 开头 + 7 位数字 + 校验字母；喂入的 `12345678Z` 是 DNI 形态（数字开头）⇒ 如实报格式不符。默认态为空输入 ⇒ 不命中。",
  },
  {
    slug: "finance/nie-validator",
    inputs: { input: "Z1234567R" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='FN180 '+document.getElementById('input').value+' '+((h.indexOf('Z - 分配序列')>=0&&h.indexOf('早期')<0&&h.indexOf('中期')<0&&h.indexOf('现行')<0&&h.indexOf('当年批次')<0)?'OK':'BAD');"],
    expect: ["FN180 Z1234567R OK"],
    ref: "F-N180 前缀文案中性化：Z1234567R 为合法非默认 NIE（mod23=1→R），前缀行须为「Z - 分配序列（非身份类别或有效期）」，且不得再出现早期/中期/现行/当年批次等无依据时间断言。旧文案「Z - 外国人（现行）」命中「现行」⇒ BAD 变红；探针绑定输入锚 ⇒ 默认态零逃生。",
  },
  {
    slug: "finance/nie-validator",
    inputs: { input: "Y1234567X" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='FN181 '+document.getElementById('input').value+' '+((typeof nieLetter==='function'&&nieCheck('Y1234567X')===true&&nieCheck('Y1234567Y')===false&&h.indexOf('（期望 X）')>=0)?'OK':'BAD');"],
    expect: ["FN181 Y1234567X OK"],
    ref: "F-N181 单一真源：期望字母抽成 nieLetter() 供 nieCheck 判定 + validate 展示共用。Y1234567X 合法（mod23=10→X），断言 nieLetter 函数存在、nieCheck 正反例正确、展示期望字母 X。旧实现无 nieLetter、validate 内联映射 ⇒ typeof 为 undefined ⇒ BAD 变红；探针绑定输入锚 ⇒ 零逃生。",
  },
  {
    slug: "finance/esn-validator",
    inputs: { input: "356938035643809" },
    expect: ["ESN HEX 应为 8 位十六进制"],
    ref: "ESN 有两种形态：8 位十六进制或 11 位十进制，15 位既非 HEX8 也非 DEC11 ⇒ 如实报格式不符（页内同场提示「ESN 已被 MEID 取代」）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/car-loan-calculator",
    inputs: { price: "200000", downPct: "20", rate: "4.5", years: "5" },
    clicks: ["calculate()"],
    expect: ["2,982.88", "18,972.98", "4.59%"],
    ref: "车价 200,000 首付 20% ⇒ 贷款 160,000，4.5%/年 60 期 ⇒ 月供 2,982.88、利息合计 18,972.98、利息占比 10.6%，落地总价 224,569.12；有效年化 = (1+4.5%/12)^12−1 = **4.59%**，与名义 4.5% 并列。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/analysis-risk",
    inputs: { s: "1000000", v: "600000", f: "100000", i: "50000", t: "25", n: "100000", dec: "2" },
    clicks: ["calc()"],
    expect: ["DCL = 1.33 × 1.20 = 1.60"],
    ref: "经营杠杆 DOL = 贡献边际 400,000 ÷ EBIT 300,000 = 1.33；财务杠杆 DFL = EBIT 300,000 ÷ (EBIT−利息 50,000) = 1.20；总杠杆 DCL = 1.33 × 1.20 = 1.60。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/analysis-risk",
    inputs: { s: "1000000", v: "600000", f: "400000", i: "0", t: "25", n: "100000", dec: "2" },
    clicks: ["calc()"],
    expect: ["EBIT 为 0（盈亏平衡），DOL/DFL/DCL 杠杆系数无定义，无法计算"],
    ref: "F-N80 真锁：收入 100 万 − 变动 60 万 − 固定 40 万 ⇒ EBIT=0，利息 i=0。旧实现 i===0 分支优先，同屏三卡均「—」却仍提示「DFL = 1」；现按 ebit===0 优先提示「杠杆系数无定义」。默认 f=20 万（EBIT=20 万）不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/analysis-risk",
    inputs: { s: "1000000", v: "600000", f: "400000", i: "10000", t: "25", n: "100000", dec: "2" },
    clicks: ["calc()"],
    expect: ["DFL = 0.00 ÷ (0.00 − 10000.00) = —"],
    ref: "EBIT 为零时百分比杠杆无定义，非零利息下 DFL 也应显示 —。",
  },
  {
    slug: "finance/analysis-5",
    inputs: {
      pre: "20000",
      ca: "60000",
      cl: "40000",
      inv: "30000",
      cash: "20000",
      tl: "150000",
      ta: "300000",
    },
    clicks: ["calc()"],
    expect: ["流动比率 1.50"],
    ref: "流动比率 = 流动资产 60,000 ÷ 流动负债 40,000 = 1.50。刻意同时录入大额存货(80,000)与预付费用(100,000)使速动比率算出 −3.00 —— 这是该页既有缺陷（速动资产口径把预付费用逐项扣了两次），因此只锚纯可复算的流动比率，不把缺陷值固化成正确。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/analysis-5",
    inputs: { ta: "1200000", tl: "1500000", ca: "500000", cl: "300000" },
    clicks: ["calc()"],
    expect: ["产权比率 — 3 警戒 无法计算 负债总额 1500000.00 ÷ 所有者权益 -300000.00"],
    ref: "F-N79 真锁①：资产 120 万、负债 150 万 ⇒ 权益 −30 万（资不抵债）。旧实现 equity!==0 照算 de=−5 并标「偏低」，与 FAQ「权益为负显示无法计算」相反；现 equity>0 才计算，负权益显示「—/无法计算」。锚点绑定 tl=1500000 与负权益串；默认 tl=70 万（权益正）不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/analysis-5",
    inputs: { ta: "1500000", tl: "500000", ca: "500000", cl: "300000" },
    clicks: ["calc()"],
    expect: ["产权比率 0.50 3 警戒 稳健 负债总额 500000.00 ÷ 所有者权益 1000000.00"],
    ref: "F-N79 真锁②：资产 150 万、负债 50 万 ⇒ 权益 100 万、de=0.5。旧用 tagHigh(de,1,2,2) 把 <1 标「偏低」，与同行参考「<1 稳健」矛盾；现专用四档标「稳健」。锚点绑定 de=0.50 与 ta/tl；默认 de=70/50=1.4（一般）不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/analysis-5",
    inputs: { ta: "400000", tl: "300000", ca: "300000", cl: "100000", inv: "100000", pre: "10000", cash: "50000" },
    clicks: ["calc()"],
    expect: ["产权比率 3.00 3 警戒 偏高 负债总额 300000.00 ÷ 所有者权益 100000.00"],
    ref: "产权比率恰为 3 时属于偏高而非警戒。",
  },
  {
    slug: "finance/analysis-5",
    inputs: { ta: "400000", tl: "300100", ca: "300000", cl: "100000", inv: "100000", pre: "10000", cash: "50000" },
    clicks: ["calc()"],
    expect: ["产权比率 3.00 3 警戒 警戒 负债总额 300100.00 ÷ 所有者权益 99900.00"],
    ref: "产权比率略大于 3 时即使显示为 3.00 也应警戒。",
  },
  {
    slug: "finance/assessor-manager",
    inputs: {
      revenue: "1000000",
      currentRatio: "2",
      debtRatio: "0.4",
      profitMargin: "0.15",
      overdue: "1",
      creditHistory: "1",
    },
    clicks: ["calc()"],
    expect: ["示例合计： 75 /100"],
    ref: "该页把利润率/负债率按「百分数字符串」显示（注入 0.15 显示成 `净利润率：0.15%`），属既有百分比口径缺陷；本例只锚评分侧的 `75 /100` 结论。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/assessor-manager",
    inputs: {
      debtRatio: "-20", currentRatio: "1.8", revenue: "5000",
      profitMargin: "12", overdue: "1", creditHistory: "5",
    },
    clicks: ["calc()"],
    expect: ["资产负债率不能为负数，请核对输入"],
    ref: "F-N82 真锁：资产负债率 −20（非法负值）旧实现 dr<=50 得满档 25 分并把评级推到 AAA；现字段级校验拒绝。默认 dr=55（合法）不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/assessor-manager",
    inputs: {
      debtRatio: "", currentRatio: "1.8", revenue: "5000",
      profitMargin: "12", overdue: "1", creditHistory: "5",
    },
    clicks: ["calc()"],
    expect: ["资产负债率须填写有效数字，不能留空或非数字"],
    ref: "F-N82 真锁：资产负债率留空旧实现 `||0` 得满档 25 分；现字段级校验拒绝空值。默认 dr=55（非空）不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/assessor-manager",
    inputs: { debtRatio: "55", currentRatio: "1.8", revenue: "5000", profitMargin: "-5", overdue: "1", creditHistory: "5" },
    clicks: ["calc()"],
    expect: ["净利润率 -5%", "示例合计： 64 /100"],
    ref: "亏损企业的负净利润率应按原分档得零分，而非拒绝评分。",
  },
  {
    slug: "finance/assessor-manager",
    inputs: { debtRatio: "55", currentRatio: "1.8", revenue: "5000", profitMargin: "", overdue: "1", creditHistory: "5" },
    clicks: ["calc()"],
    expect: ["净利润率须填写有效数字，不能留空或非数字"],
    ref: "净利润率允许负数，但不允许空值。",
  },
  ...[
    ["currentRatio", "-1", "流动比率不能为负数"],
    ["revenue", "-1", "年营业收入不能为负数"],
    ["overdue", "-1", "逾期次数不能为负数"],
    ["creditHistory", "-1", "信用历史不能为负数"],
    ["debtRatio", "101", "资不抵债：负债超过资产"],
    ["overdue", "1.5", "逾期次数须为非负整数"],
  ].map(([field, value, message]) => ({
    slug: "finance/assessor-manager",
    inputs: { [field]: value }, clicks: ["calc()"], expect: [message],
    ref: "逐项保留负数、负债率范围与逾期次数整数校验。",
  })),
  {
    slug: "finance/report-1",
    inputs: { premium: "5000", inv: "100000", capital: "500000", pct: "0.12" },
    clicks: ["calc()"],
    expect: ["子公司净资产 = 实收资本 500,000.00 + 未分配利润 200,000.00 + 评估增值 5,000.00 = 705,000.00 元"],
    ref: "子公司净资产 = 实收资本 500,000 + 未分配利润 200,000 + 评估增值 5,000 = 705,000（纯加法段，可独立复算）。该页 `pct` 按百分数解读（注入 0.12 得股权 0.12%、少数股东权益 704,154），属既有缺陷 ⇒ 本例只锁加法段，不把缺陷值固化成正确。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/report-1",
    inputs: { inv: "800000", capital: "500000", retained: "200000", pct: "0" },
    clicks: ["calc()"],
    expect: ["持股比例须大于 0 且不超过 100（当前 0%）"],
    ref: "F-N89 真锁：持股 0% 旧实现 p=0、diff=inv 全额确认为商誉（与「不纳入合并范围」相反）；现 pct<=0 拦截。默认 pct=80（合法）不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { rate: "10", init: "10000" },
    clicks: ["addCashFlow()", "document.getElementById('cf_4').value='0';updateCF(4,'0')"],
    expect: ["-490.4 NPV 净现值"],
    ref: "初始 10,000 / 折现 10% / 年年末 +3,000 ⇒ NPV = −10,000 + 2,727.27 + 2,479.34 + 2,253.94 + 2,049.04 ≈ −490.4，页内同场给 IRR 7.71%、PI 0.951、回收期 3.33 期。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { rate: "9", init: "5000" },
    clicks: ["updateCF(0, -1500)", "updateCF(1, -1500)", "updateCF(2, -1500)", "updateCF(3, -1500)"],
    expect: ["-8,796.94 NPV 净现值 范围内未找到 IRR 内部收益率",
             "IRR： ⚠ 在 −99.99% 至 100000% 搜索范围内未找到零点（或现金流同号）；不能据此断定无实根，请改用 NPV / PI 判断可行性 PI ✗ 不可行 明细按实际折现率 9.00% 计算。"],
    ref: "初始流出 5,000、四期均为 −1,500 ⇒ 现金流同号、NPV 恒为负（r=9% 独立复算 −8,796.94），可搜索区间内无 IRR 零点。修复后既不用 1000% 边界伪解，也不把「范围内未找到」写成「无实根」，而是提示改用 NPV / PI 判断可行性。两条分别绑定注入向量派生的 NPV 数值与 9.00% 折现率明细；默认态（四期 +3,000）不命中 ⇒ 强判别、零逃生。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { rate: "9", init: "100" },
    clicks: ["updateCF(0, 200)", "updateCF(1, 500)", "updateCF(2, -600)", "updateCF(3, 0)"],
    expect: ["多根 IRR 内部收益率", "IRR： ✗ 存在多个根", "无唯一解，不可行"],
    ref: "现金流 −100、+200、+500、−600 存在多次变号 ⇒ NPV 在求解区间内有多个零点（如 r≈0% 与 r≈220% 等）；按区间符号扫描识别多根后明确提示 IRR 无唯一解、不可行，不输出任一单点当成结论。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/payroll-calculator",
    inputs: {},
    clicks: ["document.getElementById('salary').value='20000';document.getElementById('base').value='20000';calc();var ok=currentResult&&Math.abs(currentResult.monthlyTax-740)<0.01;document.getElementById('res').innerHTML='PAY740 '+(ok?'OK':'BAD');"],
    expect: ["个人所得税 ¥740.00", "¥14,760 税后月薪"],
    ref: "月薪 20,000、五险一金基数同 20,000、专项附加扣除 1,000/月 ⇒ 应纳税所得额，个税 740.00 元、税后到手 14,760 元、公积金账户 4,800/月（个人+单位）。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/car-loan-calculator",
    inputs: { price: "200000", downPct: "20", rate: "", years: "5" },
    clicks: ["calculate();document.getElementById('__tbProbe').textContent='C462RATE '+document.getElementById('price').value+'/'+document.getElementById('downPct').value+'/'+document.getElementById('rate').value+' '+((document.getElementById('monthlyPay').textContent==='--')?'EMPTY':'NUM');document.getElementById('rate').value='0';calculate();document.getElementById('__tbProbe').textContent+=String(document.getElementById('monthlyPay').textContent)!=='--'?' ZOK':' ZBAD';"],
    expect: ["C462RATE 200000/20/ EMPTY ZOK"],
    ref: "第462批复核失败重做：calculate() 原先把 rateRaw==='' 直接兜成 0，清空利率仍按零利率给出完整还款表，属于「非法输入静默改 0」；修复后原始串为空即 resetDisplay()（月供回 '--'），显式填 0 仍是合法零利率方案。协议串绑定注入的车价/首付/空利率并要求同用例内 0 值恢复可算；默认态 rate=5.5% 不产生 C462RATE 串 ⇒ 强判别。",
  },
  {
    slug: "finance/ifsc-validator",
    inputs: { input: "SBIN0001234" },
    clicks: ["var __oq=document.querySelectorAll;document.querySelectorAll=function(){return [document.getElementById('input')];};var __cap=[];TBKit={util:{isEn:function(){return false},exportTable:function(){},copy:function(){},diffBox:function(){},formatNumber:function(v){return String(v)}},chart:{line:function(){},bar:function(){},donut:function(){}},matrix:{table:function(){}},preset:{bar:function(){}},history:{list:function(){return __cap.map(function(d,i){return {t:i,d:d}})},last:function(){return __cap[0]||null},record:function(r){__cap.unshift(r)},mount:function(){},clear:function(){}}};var __g=document.getElementById('input');var __sync=function(){var o=document.getElementById('output');o.textContent=String(o.innerHTML).replace(/<[^>]*>/g,'').replace(/\s+/g,' ').trim();};__g.value='SBIN0001234';validate();__sync();__ifsc_validatorExtras(true);var __n=__cap.length;__g.value='';validate();__sync();__ifsc_validatorExtras(true);var __r=__cap[0]||{};document.getElementById('__tbProbe').textContent='C113CLR '+__g.value.length+' '+(__cap.length>__n?'MORE':'SAME')+' '+String(__r['结果']||'')+' '+String(__r.__tbScore);document.querySelectorAll=__oq;"],
    expect: ["C113CLR 0 MORE 等待输入... NaN"],
    ref: "第113批复核失败重做：原 __ifsc_validatorExtras() 在 __ifsc_validatorResText() 为空时直接 return，先有效后清空不会记录空快照，导出/历史继续沿用上一条有效记录冒充当前值。修复后仅在「确已清空且最新历史非空态」时记一条 Result=等待输入...、Score=NaN 的空态快照，既不冒充通过也不冒充失败。协议自建 TBKit.history 桩并要求清空后记录数增加且末条 Score 为 NaN；默认态（空输入）不执行 clicks ⇒ 零逃生。",
  },
  {
    slug: "finance/bic-validator",
    inputs: { input: "DEUTDEFF500" },
    expect: ["银行代码： DEUT", "国家代码： DE", "分支代码： 500"],
    ref: "BIC 11 位 = 银行代码 DEUT + 国家代码 DE + 位置代码 FF + 分支代码 500，格式校验通过。默认态为空输入 ⇒ 不命中。",
  },
  {
    slug: "finance/curp-validator",
    inputs: { input: "GOMC800101HDFLRN09" },
    expect: ["校验位： 9（期望 1）"],
    ref: "墨西哥 CURP：姓名首字母 GOMC + 生日 800101 + 性别 H（男）+ 州代码 DF + 辅音 LRN。同场如实报「校验位： 9（期望 1）❌ 校验失败」—— 该号确实不是合法 CURP（这是内容问题不是代码缺陷），本例只锁校验位比对段。默认态不同 ⇒ 不命中。",
  },
  // ---- BATCH261：finance 分类「CAPM/复利/债券/租金回报/凯利/真实费率/免息期/寿险需求」族（8 例） ----
  {
    slug: "finance/capm-return",
    inputs: { rf: "0.04", beta: "1.5", rm: "0.10", obs: "0.15" },
    clicks: ["calcTool()"],
    expect: ["β × (R m − R f ) = 1.5 × 6.000% = 9.000%", "E(R) = 4.000% + 9.000% = 13.0000%"],
    ref: "CAPM 单因子模型（无风险利率 Rf = 4%、β = 1.5、市场收益率 Rm = 10%、资产预期收益 15%）：市场风险溢价 = Rm − Rf = 10% − 4% = **6.000%**；风险补偿 = β×(Rm−Rf) = 1.5×6% = **9.000%**；必要收益率 E(R) = 4% + 9% = **13.0000%**。整页把中间式直接印在明细区，两条 expect 分别是「一步乘法」与「一步加法」，且与卡片上的「β 1.25 ⇒ 11.500%」对照行不同源。默认组（3% / 1.2 / 8% ⇒ 溢价 5%、补偿 6%、E(R) 9.0000%）不命中。",
  },
  {
    slug: "finance/capm-return",
    inputs: { rf: "0.04", beta: "1.5", rm: "0.10", obs: "0.15" },
    clicks: ["var u=document.getElementById('unit');u.value='100';__capmSwitchUnit();document.getElementById('__tbProbe').textContent='UNIT '+u.value+' RF '+document.getElementById('rf').value+' RM '+document.getElementById('rm').value+' OBS '+document.getElementById('obs').value"],
    expect: ["UNIT 100 RF 4 RM 10 OBS 15"],
    ref: "F-N60 口径互转专用锁：切到百分数口径后，rf/rm/obs 须从 0.04/0.10/0.15 互转为 4/10/15（β 不换算）。旧实现无 onchange/无互转 ⇒ 输入仍 0.04/0.10/0.15 ⇒ 不命中。probe 挂 __tbProbe 抓转换后的实际输入值，避免仅靠结果串在小数口径下碰巧命中。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "20000", rate: "6", years: "10", annual: "0" },
    clicks: ["calc()"],
    expect: ["20,000.00 0.00 1,200.00 21,200.00", "21,200.00 0.00 1,272.00 22,472.00", "32,000.00 单利本利和（定投不计息）"],
    ref: "复利计算器（本金 20,000 元、年利率 6%、期限 10 年、每年追加投入 0，默认频率「年复利」）：第 1 行期初 20,000.00、追加 0.00、利息 = 20,000×6% = **1,200.00**、期末 **21,200.00**；第 2 行期初改为上一行期末 21,200.00、追加 0.00、利息 = 21,200×6% = **1,272.00**（多出的 72.00 元正是「利滚利」的证据）、期末 **22,472.00**。并列单利口径（本金单利、定投不计息）= 20,000×(1+6%×10) = **32,000.00**，与复利 35,816.95 对照。默认本金 10,000 / 5% ⇒ 不命中。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "20000", rate: "6", years: "10.5", annual: "0" },
    clicks: ["calc()"],
    expect: ["投资年限 10.5 年按整年计息，已按 10 年计算"],
    ref: "小数年限 10.5 年：复利年表与终值只能按整年计息，旧实现直接拿 10.5 年计算导致表内行数与终值口径不一致；现明确提示已按 10 年计。默认 20 年 ⇒ 不命中。",
  },
  {
    slug: "finance/bond-yield-calculator",
    inputs: { "y-face": "1000", "y-coupon": "6", "y-price": "800", "y-years": "5" },
    clicks: ["calc()"],
    expect: ["当期收益率： 7.50%", "年利息收入： ¥60.00"],
    ref: "债券收益率（面值 1,000 元、票面利率 6%、买入价 800 元、剩余 5 年）：年利息 = 1,000×6% = **¥60.00**；当期收益率（Current Yield）= 年利息/市价 = 60/800 = **7.50%**（一步相除）。同一价格下 YTM 是迭代解（页面给 11.476%，手算不可复算）⇒ **不锚 YTM**，只锚这两个一步量。默认组（1,000 / 5% / 950 ⇒ 年利息 50 / 当期收益率 5.26%）不命中。",
  },
  {
    slug: "finance/bond-yield-calculator",
    inputs: { "y-face": "100", "y-coupon": "5", "y-price": "110", "y-years": "1" },
    clicks: ["calc()"],
    expect: ["-4.545%", "Σ 现金流现值 = ¥110.00"],
    ref: "负收益率（面值 100、票息 5%、价格 110、剩余 1 年、年付一次）：唯一现金流 = 105，YTM = 105/110 − 1 = **−4.545%**（页面按每期利率在 (−1,∞) 区间二分，价格高于全部现金流时解落在负利率侧）。定价校验：105/(1−4.545%) = **¥110.00**，残差 ¥0.00 ⇒ 区间解自洽。旧实现只在 0–100% 搜索、并把下界 0 当结果 ⇒ 显示 0.000%。默认组（1,000 / 5% / 950 / 5 年 ⇒ YTM≈6.19%）两条都不命中。",
  },
  {
    slug: "finance/bond-yield-calculator",
    inputs: { "y-face": "100", "y-coupon": "5", "y-price": "82", "y-years": "3", "y-type": "zero" },
    clicks: ["calc()"],
    expect: ["6.839%", "（零息债券：无票息）", "年利息收入： ¥0.00"],
    ref: "零息债券（面值 100、价格 82、剩余 3 年、年付一次，票面利率输入 5% 应被忽略）：YTM = (100/82)^(1/3) − 1 = **6.839%**（按 `face/price` 复利开方，一步可复算）。零息模式无票息 ⇒ 页面必须把年利息/总利息清零并输出「（零息债券：无票息）」；旧实现无论类型都按 `face×票面利率` 显示 ¥5.00。默认组（附息、1,000 / 5% / 950 / 5 年）三条都不命中。",
  },
  {
    slug: "finance/bond-yield-calculator",
    inputs: { "p-face": "100", "p-coupon": "5", "p-rate": "6", "p-years": "3", "p-freq": "1", "p-type": "zero" },
    clicks: ["currentMethod='price'; calc()"],
    expect: ["债券理论价格： ¥83.96", "当期收益率： 0.00%", "年利息： ¥0.00 （零息债券：无票息）", "零息债券不付息，价格由面值按市场利率折现得到，票面利率输入不参与计算"],
    ref: "F-N4 残留分支：债券定价（price）页选零息债，面值 100、市场利率 6%、剩余 3 年、年付一次，票面利率输入框故意填 5%（应被忽略）。价格 = 100/(1.06)^3 = **¥83.96**（一步复算）；升贴水 = 83.96 − 100 = **折价 ¥16.04**。零息债券无票息 ⇒ 年利息必须 ¥0.00、当期收益率必须 0.00%，并标注「（零息债券：无票息）」与说明「票面利率输入不参与计算」。旧实现 `annualCoupon = face × couponRate / 100` 无视 type ⇒ 显示年利息 ¥5.00、当期收益率 5.96%，并给出「溢价/折价发行：票面利率 vs 市场利率」的错误归因。判别力实测：附息态（同参数 p-type=coupon）四条全部不命中，纯默认快照（ytm 分支、1,000 / 5% / 950 / 5 年）四条也全部不命中；clicks 阶段 `currentMethod='price'; calc()` 命中，因 harness 兜底阶段会以 `switchMethod(undefined)` 覆盖 #res，故必须走 click 阶段观测。",
  },
  {
    slug: "finance/bond-yield-calculator",
    inputs: { "p-face": "100", "p-coupon": "5", "p-rate": "6", "p-years": "3", "p-freq": "1", "p-type": "coupon" },
    clicks: ["currentMethod='price'; calc()"],
    expect: ["年利息： ¥5.00", "当期收益率： 5.14%"],
    ref: "F-N4 回归护栏：附息债在债券定价页必须照常计息，不能被零息改动误清零。面值 100、票面利率 5%、市场利率 6%、3 年、年付一次 ⇒ 年利息 = 100×5% = **¥5.00**；价格 = 5/1.06 + 5/1.06² + 105/1.06³ = **¥97.33**；当期收益率 = 5/97.3258×100 = **5.14%**。零息态（同参数 p-type=zero）与纯默认快照都不含这两条 ⇒ 强判别。",
  },
  {
    slug: "finance/rental-yield-calculator",
    inputs: { price: "500", area: "100", rent: "8000", fee: "0", heat: "2000", tax: "1000" },
    clicks: ["calc()"],
    expect: ["毛回报率 1.92%", "年净收入 87,000"],
    ref: "房租回报率（总价 500 万、面积 100㎡、月租 8,000 元、无中介费、取暖 2,000 元/年、税费其他 1,000 元/年）：年租金收入 = 8,000×12 = 96,000 元；毛回报率 = 96,000/5,000,000 = **1.92%**（一步相除）；年度成本合计 = 取暖 2,000 + 装修折旧 5,000 + 维修基金 1,000 + 税费 1,000 = 9,000 元；年净收入 = 96,000 − 9,000 = **87,000 元**。两条一个「毛口径」一个「净口径」，同源不同式。默认组（300 万 / 5,000 元 ⇒ 2.00% / 5 万）不命中。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "k-capital": "200000", "k-winrate": "60", "k-ratio": "2.5", "k-fraction": "0.4" },
    clicks: ["calc()"],
    expect: ["/ 2.5 = 44.00%", "建议仓位比例： 17.60%"],
    ref: "凯利公式仓位（资金 20 万、胜率 60%、盈亏比 2.5:1、按半凯利即 fraction=0.4 使用）：f* = (p×b − q)/b = (60%×2.5 − 40%)/2.5 = (1.5−0.4)/2.5 = **44.00%**；建议仓位比例 = 凯利分数 × fraction = 44% × 40% = **17.60%**；建议仓位金额 = 200,000 × 17.6% = ¥35,200（同页第三行）。整条链路三个量都只由注入值一步得出。默认组（10 万 / 55% / 2 / 0.5 ⇒ 32.50% / 16.25%）不命中。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "m-initial": "2000", "m-multiplier": "2", "m-times": "3", "m-droppct": "10" },
    clicks: ["switchMethod('martingale')"],
    expect: ["85.78（相对初始价下跌14.22%）"],
    ref: "F-N54 马丁格尔平均成本 = 累计投入 / 累计股数（各层按各自价格折算）：2000/100=20、4000/90=44.4444、8000/81=98.7654 股，累计 14000/163.2099 = ¥85.78，相对初始价 100 跌 14.22%。旧实现 avg=cumCost/(cumPos/price) 恒等于当期价 ¥81.00（跌 19.00%）⇒ 不命中。默认马丁格尔 1000/2/5/10 ⇒ 平均 ¥71.23、跌幅 28.77%，亦不命中。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "m-initial": "2000", "m-multiplier": "2", "m-times": "3", "m-droppct": "10" },
    clicks: ["switchMethod('martingale');document.getElementById('m-droppct').value='100';calc();document.getElementById('__tbProbe').textContent='MARTZERO '+(currentResult===null&&document.getElementById('statGrid').innerHTML===''&&document.getElementById('res').innerHTML.indexOf('跌幅')>=0?'OK':'BAD');"],
    expect: ["MARTZERO OK"],
    ref: "100% 跌幅导致后续成交价为零，应提示并清除上次有效结果和统计。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "m-initial": "2000", "m-multiplier": "2", "m-times": "3", "m-droppct": "101" },
    clicks: ["switchMethod('martingale');document.getElementById('__tbProbe').textContent='MARTOVER '+(currentResult===null&&document.getElementById('res').innerHTML.indexOf('跌幅')>=0?'OK':'BAD');"],
    expect: ["MARTOVER OK"],
    ref: "越界跌幅不可生成买入计划。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "m-initial": "2000", "m-multiplier": "2", "m-times": "3", "m-droppct": "0" },
    clicks: ["switchMethod('martingale');document.getElementById('__tbProbe').textContent='MARTFLAT '+(currentResult&&currentResult.positions.length===3&&currentResult.avgPrice===100?'OK':'BAD');"],
    expect: ["MARTFLAT OK"],
    ref: "零跌幅是有效输入，三层价格与平均成本均为 100。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "m-initial": "2000", "m-multiplier": "2", "m-times": "3", "m-droppct": "10" },
    clicks: ["switchMethod('martingale');document.getElementById('m-droppct').value='100';calc();localStorage.clear();saveHistory();var exports=0,kc=document.getElementById('k-capital'),oldkc=kc.value;kc.value='0';var neg=__position_size_calculatorScore('一切正常');kc.value=oldkc;var err=__position_size_calculatorScore(String(document.getElementById('res').innerHTML))===0;TBKit={util:{isEn:function(){return false},exportTable:function(){exports++}},history:{last:function(){return null},record:function(){}}};__position_size_calculatorExtras(true);__position_size_calculatorExport();document.getElementById('__tbProbe').textContent='MARTHIST '+(!localStorage.getItem(HISTORY_KEY)&&exports>0&&err&&neg===0?'OK':'BAD');"],
    expect: ["MARTHIST OK"],
    ref: "复核判据契约同步（第117批）：100% 跌幅无效态下，① 原生 saveHistory 仍不得写 localStorage（防旧结果残留）；② Export 不得再被 currentResult 守卫吞掉（旧源码首行 return ⇒ exportTable 不调用 ⇒ 不命中）；③ Score 必须按业务输入与业务结论判定：错误文案判 0、k-capital=0 时即使文案正常也判 0（旧 Score 纯关键词词表对'一切正常'返回 1 ⇒ 不命中）。harness 自研 stub 的 innerHTML 不派生 textContent，ResText 恒空 ⇒ 拒绝态入历史/趋势/导出属 harness 盲区，由真机 JSDOM scripts/_verify_finance_history_batch117.mjs 全链路覆盖；本用例锁的是 harness 可判别的三点，非放宽门禁。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "m-initial": "2000", "m-multiplier": "2", "m-times": "1", "m-droppct": "100" },
    clicks: ["switchMethod('martingale');document.getElementById('__tbProbe').textContent='MARTONE '+(currentResult&&currentResult.positions.length===1&&currentResult.avgPrice===100?'OK':'BAD');"],
    expect: ["MARTONE OK"],
    ref: "单层只在初始价格成交，不触发后续跌幅。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "m-initial": "2000", "m-multiplier": "2", "m-times": "20", "m-droppct": "99.99999999999999" },
    clicks: ["switchMethod('martingale');document.getElementById('__tbProbe').textContent='MARTFINITE '+(currentResult===null?'OK':'BAD');"],
    expect: ["MARTFINITE OK"],
    ref: "极端跌幅导致价格或股数溢出时不能生成虚假成本。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: { initial: "0", monthly: "0", years: "10", rate: "8" },
    expect: ["无法计算（请输入有效现金流）"],
    ref: "F-N43 零现金流：initial=0/monthly=0 ⇒ 现金流全 0，无正负号变化，IRR 不存在。旧实现固定区间二分后取中点 −0.5×12×100 = −600%；修复后 calcIRR 返回 NaN，渲染「无法计算（请输入有效现金流）」。默认 monthly=1000 ⇒ IRR 有限 ⇒ 不命中。",
  },
  {
    slug: "finance/installment-real-rate",
    inputs: { P: "24000", n: "24", r: "1.2" },
    clicks: ["calcTool()"],
    expect: ["1,288.00 每期还款额（元）", "6,912.00 总手续费（元）"],
    ref: "分期实际费率（本金 24,000 元、24 期、月手续费率 1.2%）：每期手续费 = 24,000×1.2% = 288.00 元，每期本金 = 24,000/24 = 1,000.00 元 ⇒ 每期还款 **1,288.00 元**（一步相加）；总手续费 = 288.00×24 = **6,912.00 元**。注意注入值刻意避开默认组（12,000 / 12 / 0.6）—— 那组算出的「1,072.00 / 864.00」才是默认值 ⇒ 若沿用默认值会出现「注入值 == 默认值」的伪判别。默认组不同 ⇒ 不命中。",
  },
  {
    slug: "finance/credit-card-grace-period",
    inputs: { amt: "5000", yield: "2.0" },
    clicks: ["calcTool()"],
    expect: ["46 天 最长免息期（7月10日消费）", "¥12.60 该笔资金收益（2%年化）"],
    ref: "第703批真实日期口径：账单10/还款25、默认入账延迟1天，按当前起24个月逐日计算，最长免息期 46 天（7月10日消费）、最短 16 天；5,000×2%×46/365 = **¥12.60**。旧用例的 44/29 天来自固定 30 天假口径，已随真实日期实现更新。",
  },
  {
    slug: "finance/credit-card-grace-period",
    inputs: { bill: "12", due: "28", amt: "5000", yield: "2.0" },
    clicks: ["calcTool()"],
    expect: ["47 天 最长免息期（7月12日消费）", "¥12.88 该笔资金收益（2%年化）"],
    ref: "账单12/还款28、入账延迟1天：按真实自然日逐日计算，最长免息期 **47 天**（7月12日消费）；5,000×2%×47/365 = **¥12.88**。旧固定 30 天口径会得到 45 天 / ¥12.33，本用例可区分真实日期实现。",
  },
  {
    slug: "finance/credit-card-grace-period",
    inputs: { bill: "28", due: "5", amt: "5000", yield: "2.0" },
    clicks: ["calcTool()"],
    expect: ["39 天", "¥10.68"],
    ref: "账单28/还款次月5、入账延迟1天：真实日期逐日计算最长免息期 **39 天**（7月28日消费）；5,000×2%×39/365 = **¥10.68**。旧固定 30 天口径为 36 天 / ¥9.86 ⇒ 本用例区分真实日期实现。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "25", dt_expense: "15", dt_debt: "50", dt_existing: "20" },
    clicks: ["calc()"],
    expect: ["250万 (年收入×10)", "2.5万 年收入×10%"],
    ref: "家庭保障缺口测算（输入为「当前年收入 25 万」等四项）：寿险保额 = 年收入×10 = **250 万**（覆盖 10 年收入替代）；年保费预算 = 年收入×10% = **2.5 万**；重疾保额 = 年收入×5 = 125 万；意外险保额 = 年收入×10 = 250 万。四条**全部只由年收入一步乘出**，同页还给出「寿险 280 万」（覆盖家庭负债口径，与 250 万属不同规则 ⇒ 本身就是一条天然阴性对照）。默认组年收入 20 万 ⇒ 200 万 / 2 万，不命中。",
  },
  // ---- BATCH262：finance 分类「CAGR/折旧/利润率/股价/期权/单利/金价/盈亏平衡/折扣链/房贷/积分/薪资」族（12 例） ----
  {
    slug: "finance/cagr",
    inputs: { start: "80", end: "240", years: "6" },
    clicks: ["calcTool()"],
    expect: ["20.09 CAGR (%)", "0.2009 增长率 (小数)"],
    ref: "年化复合增长率（期初 80 万元、期末 240 万元、6 年）：CAGR = (240/80)^(1/6) − 1 = 3^0.166667 − 1 = **20.09%**，页面同时给出小数口径 **0.2009**，两条同源于一个幂运算、可一步复核。默认组（100→200 / 7 年 ⇒ 10.49% / 0.1049）不命中。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "90000", salvage: "6000", life: "3", totalUnits: "8000" },
    clicks: ["calc()"],
    expect: ["28,000 直线法首年折旧", "42,000 SYD首年折旧"],
    ref: "固定资产折旧（原值 90,000、残值 6,000、年限 3 年）：可折旧总额 = 90,000 − 6,000 = 84,000；直线法首年 = 84,000/3 = **28,000**；年限总和法首年 = 84,000×3/(3×4/2) = **42,000**。两条都是一步乘除，且刻意避开第一组注入值（80,000 / 4,000 / 4 年 ⇒ 19,000 / 30,400）—— 那组算出的直线法首年恰好 19,000，与默认组（100,000 / 5,000 / 5 年）撞同值 ⇒ 首轮判逃生项，换组后方有判别力。默认组不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { revenue: "2000000", cogs: "1100000" },
    clicks: ["calc()"],
    expect: ["毛利润 90.00万 (45.0%)", "净利率 22.13%"],
    ref: "利润率（营业收入 200 万、营业成本 110 万，其余费用沿用默认档）：毛利润 = 200 − 110 = 90.00 万，毛利率 = 90/200 = **45.0%**；营业利润 = 90 − 23 − 6 = 61.00 万 ⇒ 营业利润率 **30.50%**；EBITDA 67.00 万；利润总额 59.00 万，所得税（25%）14.75 万 ⇒ 净利润 **44.25 万**，净利率 = 44.25/200 = **22.13%**（折旧摊销 6 万已扣除）。默认组（100 万 / 60 万 ⇒ 40.00万 / 40.0%）不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { revenue: "5000000", cogs: "2000000", sellingExp: "0", adminExp: "0", rdExp: "0", finExp: "0", da: "300000", taxRate: "0" },
    clicks: ["calc()"],
    expect: ["净利率 54.00%", "EBITDA利润率 60.00%"],
    ref: "折旧摊销修复判别：收入 500 万、成本 200 万、期间费用 0、折旧摊销 30 万、利息与税 0。修复后营业利润 = 300 − 30 = 270.00 万、净利率 = 270/500 = **54.00%**，EBITDA = 300 万 ⇒ **60.00%**；旧实现不扣折旧摊销（净利率 60.00%、EBITDA 利润率 66.00%）⇒ 不命中。默认态输出 6.75% 与 17.00%，亦不命中。",
  },
  {
    slug: "finance/stock-profit-calculator",
    inputs: { buyPrice: "12.5", buyQty: "800", sellPrice: "14.2", commissionRate: "0.025", stampRate: "0.05", transferRate: "0.001", minCommission: "5" },
    clicks: ["calc()"],
    expect: ["+1,344.11", "+13.43%"],
    ref: "股票买卖盈亏（买入 12.50 × 800 股 = 10,000、卖出 14.20 × 800 = 11,360，佣金 0.025% 最低 5 元、印花税 0.05% 单边、过户费 0.001%）：买入成本 = 10,000 + 佣金 5.00（按 0.025% 仅 2.50 元，触发「最低 5 元」档）= 10,005.10；卖出费用 = 佣金 5.00 + 印花税 5.68 + 过户费 0.11 = 10.79 ⇒ 净收入 11,349.21；净盈亏 = 11,349.21 − 10,005.10 = **+1,344.11**，收益率 = 1,344.11/10,005.10 = **+13.43%**。两条同源、均可一步复核。默认组（10 / 11 / 1000 股）不命中。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { strike: "90", premium: "4", s0: "105", contracts: "2", mult: "100", fee: "2" },
    clicks: ["calc()"],
    expect: ["盈亏平衡点： 94.04 元", "总盈亏：+¥2,192.00"],
    ref: "看涨期权买方盈亏（行权价 90、权利金 4 元/股、到期价 105、2 张 × 乘数 100、手续费 2 元/侧）：盈亏平衡点 = 90 + 4 + 手续费/股 0.04 = **94.04 元**（含开平手续费）；权利金成本 = 4×100×2 = 800.00，交易手续费合计 8.00（开仓+平仓）；总盈亏 = (105 − 90 − 4)×100×2 − 8 = 2,200 − 8 = **+2,192.00**。一条「一步相加」、一条「（价差−权利金）×乘数×张数 − 手续费」，同源不同式。默认组（100 / 5 / 110 / 1 张）不命中。",
  },
  {
    slug: "finance/simple-interest",
    inputs: { principal: "25000", rate: "4.5", years: "4" },
    clicks: ["calc()"],
    expect: ["每年利息： 1,125 元", "本利和： 29,500 元"],
    ref: "单利（本金 25,000、年利率 4.5%、4 年）：每年利息 = 25,000×4.5% = **1,125 元**；累计利息 = 1,125×4 = 4,500；本利和 = 25,000 + 4,500 = **29,500 元**。页面逐年明细第 1 年末累计利息 1,125 / 本利和 26,125，第 4 年末 4,500 / 29,500，与两条锚同源。默认组（10,000 / 5% / 3 年 ⇒ 1,500 / 14,500）不命中。",
  },
  {
    slug: "finance/gold-price-calculator",
    inputs: { goldPrice: "650", weightInput: "10", weightUnit: "g", puritySel: "0.9999", discountRate: "100", usdRate: "" },
    clicks: ["switchMode('wt');calcAll()"],
    expect: ["10.0000 克", "¥ 6,500.00"],
    ref: "第934批：金价为足金999.9基准，同纯度按 纯度/0.9999 折算；10g×650 不再算成 6499.35，而是 6500.00。默认金价 600 ⇒ 本用例显式 650。",
  },
  {
    slug: "finance/gold-price-calculator",
    inputs: { goldPrice: "650", weightInput: "10", weightUnit: "g", puritySel: "0.75", discountRate: "100", usdRate: "" },
    clicks: ["switchMode('wt');calcAll()"],
    expect: ["¥ 4,875.49"],
    ref: "第934批：18K（0.75）10g 按 650÷0.9999×0.75 = 487.549/克 ⇒ 4875.49，与同纯度正反算互逆。默认纯度 999.9 ⇒ 不命中。",
  },
  {
    slug: "finance/gold-price-calculator",
    inputs: { goldPrice: "600", usdRate: "7.1", discountRate: "90", weightInput: "8" },
    clicks: ["calcAll()"],
    expect: ["10.8344 克", "¥600.00/克"],
    ref: "黄金折算（总投入 6,500 元、足金 999.9 含金量 99.99%、现价 600 元/克）：页面自印计算式 6,500 ÷ (含金量 99.99% × ¥**600.00**/克) = **10.8344 克**，其中 600.00 即注入现价（一步取值）、10.8344 即该式结果（6,500/(0.9999×600) = 10.83447，一步可复算）。同页纯度表列出足金 99.99% 每克 599.94 元、18K 金每克 450.00 元，均 = 600×纯度 ⇒ 自洽。默认现价 650 ⇒ 10.0015 克，不命中。",
  },
  {
    slug: "finance/gold-price-calculator",
    inputs: { goldPrice: "650", discountRate: "150", weightInput: "10" },
    clicks: ["calcAll()"],
    expect: ["回收折价率须在 0–100% 之间，请修改后重试。"],
    ref: "F-N63 折价率上界：150% ⇒ 旧实现只靠 HTML max 属性、JS 读入后不校验，输出回收估价 ¥9,749.03（高于金料总值 6,499.35）。修复后字段级拒绝。默认 95% ⇒ 不命中。",
  },
  {
    slug: "finance/gold-price-calculator",
    inputs: { goldPrice: "650", discountRate: "-10", weightInput: "10" },
    clicks: ["calcAll()"],
    expect: ["回收折价率须在 0–100% 之间，请修改后重试。"],
    ref: "F-N63 折价率下界：−10% ⇒ 旧实现输出负回收价 ¥−649.94 并进入复制/导出/历史。修复后字段级拒绝。默认 95% ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { fc: "150000", price: "60", vc: "35", taxRate: "25" },
    clicks: ["calc()"],
    expect: ["变动成本总额：280,000.00 元", "经营杠杆系数： 4.00"],
    ref: "本量利分析（固定成本 150,000、单价 60、单位变动成本 35、销量沿用默认 8,000、所得税 25%）：销售收入 = 8,000×60 = 480,000 元；变动成本总额 = 8,000×35 = **280,000.00 元**（一步相乘）；盈亏平衡量 = 150,000/(60−35) = 6,000 件 ⇒ 安全边际量 2,000 件、安全边际率 25.00%；息税前利润 = 480,000 − 280,000 − 150,000 = 50,000；经营杠杆系数 = 贡献边际 200,000 ÷ 50,000 = **4.00**（一步相除）。默认组（100,000 / 50 / 30 ⇒ 400,000 / 利润 160,000 / DOL 1.50）不命中。",
  },
  {
    slug: "finance/discount-calculator",
    inputs: { price: "250" },
    clicks: ["discounts=[0.7];calc()"],
    expect: ["¥ 175.00", "7.00 折"],
    ref: "叠加折扣链（原价 250 元；折扣链是页面私有数组 `discounts`，经 clicks 直接置为 [0.7] 再调 calc()）：折后价 = 250×0.7 = **¥ 175.00**，综合折扣率 30.0%，相当于 **7.00 折**。该页折扣输入框是 `renderDiscountChain()` 运行期生成的**无 id 输入框**（oninput 指向 `updateDiscount(i, this.value)`）⇒ `inputs` 注入不到，必须用 clicks 改写页面级数组。首轮试过 `discounts=[0.8]`，恰好等于该页默认折扣 ⇒ 默认态也命中（逃生项），改 0.7 后才有判别力。默认组不命中。",
  },
  {
    slug: "finance/mortgage-calculator",
    inputs: { loanAmount: "300", rate: "5.2", downPayment: "40" },
    clicks: ["calculate()"],
    expect: ["¥2,084.00", "¥7,800.00", "5.33%"],
    ref: "商业贷款（房价 300 万、年利率 5.2%、首付比例 40%、年限取页面默认 30 年）：贷款本金 = 房价×(1−首付) = 3,000,000×60% = **1,800,000**；首月利息 = 1,800,000×5.2%/12 = **¥7,800.00**（一步相乘）；月供 9,884.00 ⇒ 首月本金 = 9,884.00 − 7,800.00 = **¥2,084.00**（一步相减），尾列剩余余额 1,797,916.00 自洽。默认组（房价 100 万 / 4.2% / 首付 30% ⇒ 本金 70 万、月供 3,423.12、首月利息 2,450.00）不命中。有效年化 = (1+5.2%/12)^12−1 = **5.33%**，与名义 5.2% 并列；默认 4.2% ⇒ 4.28%。",
  },
  {
    slug: "finance/loan-comparison",
    inputs: {"a-principal":"100000","a-rate":"6","a-months":"36","b-principal":"100000","b-rate":"4.8","b-months":"36","c-principal":"100000","c-rate":"4.6","c-months":"30"},
    clicks: ["calc()"],
    expect: ["6.17%"],
    ref: "方案 A 名义年利率 6%、按月计息 ⇒ 有效年化 (1+6%/12)^12−1 = **6.17%**，须与名义值并列展示；默认 A 为 4.8% ⇒ 4.91%，不命中。",
  },
  {
    slug: "finance/mortgage-calculator",
    inputs: { loanAmount: "100", rate: "0", downPayment: "30" },
    clicks: ["calculate()"],
    expect: ["¥1,944.44", "1 ¥1,944.44 ¥1,944.44 ¥0.00 ¥698,055.56"],
    ref: "零利率合法分支（房价 100 万、首付 30% ⇒ 本金 70 万、30 年 = 360 期）：月供 = 700,000 ÷ 360 = **¥1,944.44**（一步相除，页面走 `monthlyRate === 0` 的均分分支而非被 `!annualRate` 拒绝）；首行本金 1,944.44、利息 ¥0.00、余额 698,055.56 三者自洽。默认年利率 4.2% ⇒ 月供 3,423.12、首月利息 2,450.00，两条都不命中。",
  },
  {
    slug: "finance/points-redemption-value",
    inputs: { pts: "20000", val: "25", fee: "0" },
    clicks: ["document.getElementById('pts').value='20000';document.getElementById('val').value='25';document.getElementById('fee').value='0';calcTool()"],
    expect: ["12.50 每万分兑换价值（元）", "0.13 每 100 分兑换价值（元）"],
    ref: "积分兑换价值（积分 20,000 个、标价 25 元、加钱 0 元）：每万分兑换价值 = 25 ÷ (20,000/10,000) = **12.50 元**；每 100 分兑换价值 = 12.50/100 = **0.13 元**（同一数值换百分之一口径，同源只差一个百分数）。默认组（10,000 分 / 20 元 ⇒ 20.00 / 0.20）不命中。",
  },
  {
    slug: "finance/points-redemption-value",
    inputs: { pts: "10000", val: "20", fee: "30" },
    clicks: ["calcTool()"],
    expect: ["加钱金额已超过商品价值，换购不划算，请核对输入"],
    ref: "F-N68 真锁：加钱 30 元 > 商品价值 20 元时净价值为负，旧实现照常输出负「净得价值/每万分价值」并判「偏亏」；现显式拦截点明「加钱已超过商品价值」。默认 fee=0（未超）不命中；fee==val（补强用例 42/42/42）仍合法不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/points-redemption-value",
    inputs: { pts: "20000", val: "25", fee: "-5" },
    clicks: ["calcTool()"],
    expect: ["需加钱换购金额不能为负数"],
    ref: "负加钱额原实现等于「平台倒贴」，净价值反而高于标价；现拦截提示。默认加钱 0 ⇒ 不命中。",
  },
  {
    slug: "finance/points-redemption-value",
    inputs: { pts: "20000", val: "0", fee: "0" },
    clicks: ["calcTool()"],
    expect: ["0.00 每万分兑换价值（元）"],
    ref: "第705批口径：商品价值 0 是合法输入（零价值赠品），不再拦截；净价值 0、每万分价值 0.00，并给「偏亏」参考分级。默认 20 元 ⇒ 20.00，不命中。",
  },
  {
    slug: "finance/salary-calculator",
    inputs: { baseSalary: "40000", pensionRate: "8", medicalRate: "2", unemploymentRate: "0.5", housingRate: "12", housingBase: "40000" },
    clicks: ["calculate()"],
    expect: ["¥9,000.00", "¥4,800.00"],
    ref: "薪资五险一金（缴费基数 40,000：养老 8% / 医疗 2% / 失业 0.5% / 公积金 12%，工伤与生育默认 0）：公积金 = 40,000×12% = **¥4,800.00**（一步相乘）；五险一金合计 = 40,000×(8%+2%+0.5%+0+0+12%) = 40,000×22.5% = **¥9,000.00**（一条式）。同页个税按起征额 36,000 元与超额累进表计算，与本两项自洽。默认基数 20,000 ⇒ 2,400 / 4,500，不命中。",
  },
  {
    slug: "finance/salary-calculator",
    inputs: { salaryMode: "annual", salary: "240000" },
    clicks: ["calculate()"],
    expect: ["⚠ 五险一金缴费基数 ¥240,000.00/月 高于税前工资 ¥20,000.00/月"],
    ref: "第124批 F-N98 契约同步（用例过期，非页面 bug）：旧版年薪模式沿用月薪默认缴费基数，同屏输出「年五险一金 ¥64.80万 / 税后年收入 ¥-408,000.00」这类不可能的负工资，旧 expect 把该缺陷固化成契约。修复后按业务状态拒绝、写出带当前取值的提示并清空数值区。注入 salary=240000 使提示含 240,000.00 与 20,000.00；默认态（20,000.00 / 1,666.67）不含该串 ⇒ 强判别、零逃生。F-N15 模式快照与状态链由真机 JSDOM 独立脚本覆盖（harness 存在跨用例 salaryMode 残留，不能作为模式锁）。"
  },
  {
    slug: "finance/salary-calculator",
    inputs: { housingLoan: "1000", housingRent: "1500" },
    clicks: ["calculate()"],
    expect: ["已按较大者 ¥1,500.00/月（住房租金）计入，另一项 ¥1,000.00/月未计入", "专项附加扣除合计 ¥3,500.00 元/月。"],
    ref: "F-N15 房贷利息/租金互斥（租金更大）：同一纳税年度内两项不可同时扣除，同时填写时仅按较大者 1500 计入，合计 = 1500 + 赡养老人 2000 = 3500；旧实现直加 1000+1500+2000 = 4500 且无任何说明。结果容器 salaryDeductionNote 输出实际采用值与未计入项，两条都依赖注入值。默认态只填租金 1500、房贷 0 ⇒ 不触发互斥、无说明行 ⇒ 零逃生。"
  },
  {
    slug: "finance/salary-calculator",
    inputs: { housingLoan: "2000", housingRent: "1000" },
    clicks: ["calculate()"],
    expect: ["已按较大者 ¥2,000.00/月（房贷利息）计入，另一项 ¥1,000.00/月未计入", "专项附加扣除合计 ¥4,000.00 元/月。"],
    ref: "F-N15 互斥方向回归护栏（房贷更大）：较大者换成房贷利息 2000，说明行须标注「房贷利息」并把租金 1000 列为未计入，合计 = 2000 + 2000 = 4000；防止实现写成固定取租金或固定保留房贷。默认态不命中。"
  },

  // ---- BATCH263：finance 分类「卡号 Luhn 反例 / 免息天数 / 夏普比率 / IRR」收口族（4 例） ----
  {
    slug: "finance/credit-card-validator",
    inputs: { cardInput: "4532015112830360" },
    clicks: ["validate()"],
    expect: ["Luhn 校验： ❌ 未通过", "❌ Luhn 校验失败，卡号无效"],
    ref: "卡号校验**反例**（Visa 号 4532 0151 1283 0360，末位把原校验位 6 改成 0）：页面输出「卡号格式化： 4532 0151 1283 0360 / 卡组织识别： Visa / 长度校验： ✅ 当前 16 位」但「Luhn 校验： ❌ 未通过」。本页默认态卡号为空 ⇒ 只显示「请在上方输入卡号以开始校验」，绝不可能出现否定结论 ⇒ 这是一条**零成本的廉价判别**。与既有 `credit-card-luhn` 正例（4532015112830366 通过）互为镜像。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "8000", dailyRate: "0.05", billDay: "2", dueDay: "20", minRatio: "10", repayType: "full" },
    clicks: ["['billAmount','dailyRate','billDay','dueDay','minRatio'].forEach(function(id){document.getElementById(id).value={billAmount:'8000',dailyRate:'0.05',billDay:'2',dueDay:'20',minRatio:'10'}[id];});document.getElementById('repayType').value='full';calc()"],
    expect: ["38 免息天数"],
    ref: "信用卡免息期天数（账单日 2 号、还款日 20 号）：因 dueDay > billDay ⇒ 免息天数 = (还款日 − 账单日) + 20 = 20 − 2 + 20 = **38 天**，再经 `min(max(x,20),56)` 裁剪后仍为 38。刻意避开默认组（账单日 10 / 还款日 30 ⇒ 40 天）—— 首轮按默认值注入时该行恒为 40、默认态也命中 ⇒ 判逃生项，改账单日/还款日后才有判别力。全额还款 ⇒ 循环利息 0.00、应还 8,000.00 与「免息期内无息」自洽。",
  },
  {
    slug: "finance/sharpe-ratio",
    inputs: { portReturn: "14", portStd: "20", riskFree: "2" },
    clicks: ["currentTab='inputs'; calc()"],
    expect: ["每期无风险利率 = 2.00% ÷ 12 = 0.167%", "每期夏普比率 = 13.833 ÷ 20.000 = 0.6917", "年化夏普 = 0.6917 × √12 = 2.3960"],
    ref: "夏普比率（组合收益率 14%、标准差 20%、无风险利率 2%、年化系数 12）：无风险利率为年化口径，须先折算到每期 = 2%/12 = **0.167%**；超额收益 = 14.000 − 0.167 = **13.833%**；每期夏普 = 13.833 ÷ 20.000 = **0.6917**，年化 = 0.6917 × √12 = **2.3960**（旧实现直接 14 − 2 得 0.6000，属月/年口径混算）。默认组（8 / 12 / 3）为 0.4167，不命中。注意该页 `calc()` 依赖 `currentTab`：harness 内 `oninput` 触发的 `switchTab` 会抛 `charAt` of undefined ⇒ 必须在 clicks 里先 `currentTab='inputs'` 再调 `calc()`。",
  },
  {
    slug: "finance/sharpe-ratio",
    inputs: { portReturn: "14", portStd: "20", riskFree: "-5" },
    clicks: ["currentTab='inputs'; calc()"],
    expect: ["无风险利率须为非负数"],
    ref: "负无风险利率原实现照算并产出正/负夏普；现拦截。默认输入 3% 不出现该提示。",
  },
  {
    slug: "finance/sharpe-ratio",
    inputs: { riskFree: "" },
    clicks: ["currentTab='series';calc()"],
    expect: ["无风险利率（年化 %）不能为空；如确实为 0，请明确输入 0。"],
    ref: "第933批：无风险利率留空不再当 0 静默计算；必须明确输入 0 才按零利率处理。默认 3% ⇒ 不命中。",
  },
  {
    slug: "finance/sharpe-ratio",
    inputs: { returns: "1,abc,3", riskFree: "2" },
    clicks: ["currentTab='series';calc()"],
    expect: ["收益率序列含 1 个无法解析的项：「abc」"],
    ref: "第933批：收益序列不再静默跳过 abc 按 1,3 计算；标出无效项并暂停。默认序列全部合法 ⇒ 不命中。",
  },
  {
    slug: "finance/sharpe-ratio",
    inputs: { portReturn: "", portStd: "20", riskFree: "2" },
    clicks: ["currentTab='inputs';calc()"],
    expect: ["组合平均收益率（%）不能为空；如确实为 0，请明确输入 0。"],
    ref: "第933批：直接输入模式空组合收益不再按 0 计算；0 必须明确输入。默认 8% ⇒ 不命中。",
  },
  {
    slug: "finance/irr-calculator",
    inputs: { discountRate: "8" },
    clicks: ["cashFlows=[{period:0,amount:-10000,label:'初始'},{period:1,amount:11000,label:'收益'}]; calc()"],
    expect: ["10.00%"],
    ref: "内部收益率（一次性投入 −10,000、一年后收回 11,000，贴现率 8%）：IRR 是方程 −10,000 + 11,000/(1+r) = 0 的解 ⇒ 1+r = 11,000/10,000 ⇒ **IRR = 10.00%**，页面 `irrValue` 直接显示该值，并据此把字体染绿（IRR ≥ 贴现率）。该页现金流表由页面私有数组 `cashFlows` 驱动、`inputs` 注入不到 ⇒ 用 clicks 直接赋数组（必须带 `label` 字段，否则 `updateLabel` 会抛错）再调 `calc()`。默认态 `cashFlows` 为空 ⇒ 输出 `--`，不命中。",
  },
  {
    slug: "finance/irr-calculator",
    inputs: { discountRate: "8", periodUnit: "month" },
    clicks: ["cashFlows=[{period:0,amount:100000,label:'贷款到账'}];for(var __i=1;__i<=12;__i++)cashFlows.push({period:__i,amount:-8884,label:'第'+__i+'月还款'});calc()"],
    expect: ["每期 IRR = 0.9984%", "年化 IRR = 12.6615%", "12.66%"],
    ref: "贷款现金流方向（T0 放款 +100,000、其后 12 个月每月还款 −8,884，期数单位=月）：方程 100,000 = 8,884×[1−(1+i)⁻¹²]/i ⇒ 每期（月）IRR = **0.9984%**，年化 = (1+0.9984%)¹²−1 = **12.6615%**。页面区间求解按端点符号（NPV 随利率递增），收敛后残差 |NPV| ≈ 1e-10（远小于 `scale×1e-8`）。旧实现固定假设「NPV 随利率递减」⇒ 会跑到 1000% 上限且不报警。默认项目预设（期数单位=年、IRR≈16.7%）两条都不命中。",
  },
  {
    slug: "finance/irr-calculator",
    inputs: { discountRate: "8" },
    clicks: ["cashFlows=[{period:0,amount:-50000,label:'首年保费'},{period:1,amount:-50000,label:'第2年保费'},{period:2,amount:-50000,label:'第3年保费'},{period:10,amount:200000,label:'第10年领取'}];calc()"],
    expect: ["每期 IRR = 3.2442%", "NPV @ 折现率 8.00% = -46,524.54", "T10"],
    ref: "稀疏期号折现（保险预设：T0/T1/T2 各 −50,000，T10 +200,000，期数单位=年）：按真实期号折现，8% 下 NPV = −50,000 −50,000/1.08 −50,000/1.08² + 200,000/1.08¹⁰ = **−46,524.54**；IRR 解 −50,000−50,000/(1+r)−50,000/(1+r)²+200,000/(1+r)¹⁰ = 0 ⇒ r = **3.2442%**。旧实现把 T10 当数组下标第 3 期 ⇒ 8% 下 NPV 显示约 +19,603（错号），本用例两条数值锚均可判别。默认项目预设（5 期连续、IRR≈16.7%）不命中。",
  },

  // ---- BATCH264：finance 分类「发票生成器 single/split/combine/reverse 四路径」族（4 例） ----
  {
    slug: "finance/invoice-generator",
    inputs: { "s-total": "20000", customTax: "13" },
    clicks: ["calc()"],
    expect: ["¥17,699.12", "= 20,000.00 ÷ 1.13 = ¥17,699.12"],
    ref: "单一模式（价税分离）：不含税 = 价税合计 ÷ (1 + 13%) = 20,000 ÷ 1.13 = **17,699.12**，页面公式行原样回显该算式，两条同源不同式（一条是结果、一条是算式）。默认组（10,000 / 9%）⇒ 不含税 9,174.31，且公式行写的是 ÷ 1.09，两条都不命中。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "sp-total": "25000", "sp-limit": "5000", "sp-type": "excl" },
    clicks: ["currentMethod='split'; calc()"],
    expect: ["5 张发票", "¥2,250.00"],
    ref: "拆分模式（金额字段按不含税口径）：张数 = ceil(25,000 ÷ 5,000) = **5 张**，每张不含税 5,000、税额 = 5,000 × 9% = 450 ⇒ 税额合计 = 450 × 5 = **2,250.00**、价税合计 = (5,000+450) × 5 = **27,250.00**。刻意注入 sp-type=excl 让税额由 450×5 一次乘得（默认第一个选项 total 口径下 sumExcl 与 sumTax 是除不尽的循环小数，不好复算）；默认组（100,000 / 10,000）⇒ 10 张，不命中。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "cb-amt1": "5000", "cb-amt2": "3000", "cb-amt3": "1000", "cb-amt4": "0", "cb-target": "9001" },
    clicks: ["currentMethod='combine'; calc()"],
    expect: ["凑整金额： ¥9,000.00", "差额： ¥1.000000 ⚠️ 超出允许范围"],
    ref: "凑整模式：目标 9,001 元，面额 5,000 / 3,000 / 1,000（4 号面额填 0 被过滤），搜索器先命中 1,000 × 9 = **9,000** 这条零成本组合 ⇒ 凑整金额 **9,000**、差额 = |9,000 − 9,001| = **1.000000**，大于容差 0.01 ⇒ 判定「⚠️ 超出允许范围」。锚不碰「目标金额 9,001.00」（那是输入回显），只锚与 target 不同的派生行。默认组（目标 50,000）的差额为 0 ⇒ 命中的是同位置的 ✅ 分支，不命中本条。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "rv-total": "20000", "rv-tax": "1600" },
    clicks: ["currentMethod='reverse'; calc()"],
    expect: ["反推税率： 8.6957%", "= 1,600.00 ÷ 18,400.00 × 100% = 8.6957%"],
    ref: "反推模式：不含税 = 20,000 − 1,600 = **18,400**，税率 = 1,600 ÷ 18,400 × 100% = **8.6957%**，公式行把除数与被除数一并回显 ⇒ 可完全手算复核。默认组（10,000 / 825.69）⇒ 税率 9.0000%，两条都不同。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "rv-total": "10000", "rv-tax": "15000" },
    clicks: ["currentMethod='reverse'; calc()"],
    expect: ["税额不得超过含税金额"],
    ref: "F-N77：反推税额越界（15,000 > 10,000）旧实现给出不含税 −5,000、税率 0.0000% 与矛盾公式；修复后先校验 0 ≤ tax ≤ total 并标红停止。默认组 10,000 / 825.69 不命中该拒绝语。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "rv-total": "10000", "rv-tax": "-1" },
    clicks: ["currentMethod='reverse'; calc()"],
    expect: ["税额不得小于 0"],
    ref: "F-N77：税额为负时旧实现把不含税放大到 10,001 并输出负税率；修复后拒绝 tax < 0。默认组税额 825.69 为正，不命中。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "rv-total": "10000", "rv-tax": "10000" },
    clicks: ["currentMethod='reverse'; calc()"],
    expect: ["不含税为 0，无法反推税率"],
    ref: "F-N77：税额恰等于含税金额时不含税为 0，旧实现静默输出 0.0000% 税率；修复后明确提示无法反推并停止。默认组 10,000 / 825.69 不会命中该提示。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "sp-total": "80000", "sp-limit": "-5000" },
    clicks: ["currentMethod='split'; calc()"],
    expect: ["单张限额必须大于 0"],
    ref: "负限额（避开 HTML 默认 10,000）：旧实现 count = ceil(80,000 / −5,000) = −16 ⇒ count<=1 直接出 1 张，负限额被静默接受；修复后入口校验 limit > 0 并停止计算。清空/填 0 时 getVal 兜底 0 同样命中该守卫（旧实现 count=Infinity 会进入 Infinity 次 for 循环把标签页冻死；此处选负值只为让用例在修复前也能快速返回、不挂死门禁）。",
  },

  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "36", dt_expense: "22", dt_debt: "120", dt_existing: "25" },
    clicks: ["switchMethod('dual-ten'); calc()"],
    expect: ["455万", "180 万保额", "年收入36万×10 + 负债120万 − 已有保障25万 = 455万"],
    ref: "双十法则非默认组（年收入 36 万、负债 120 万、存量保障 25 万）：寿险保额 = max(年收入×10 + 负债 − 存量, 0) = 360 + 120 − 25 = **455 万**；重疾 = max(年收入×5, 30) = 180 万；明细拆解行同步展示完整算式（F-N55 修复后与结果卡一致，旧实现硬写 360 万年收入×10 与 455 万结果卡矛盾）。三条 expect 分别锚在 stat 卡、险种配置条、明细拆解行上，同源不同式，可一步复核。默认组（年收入 20 / 负债 80 / 存量 10）⇒ 270 / 100 / 算式 200+80−10=270，三条都不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "28", dt_expense: "15", dt_debt: "90", dt_existing: "33" },
    clicks: ["switchMethod('dual-ten'); calc()"],
    expect: ["年收入28万×10 + 负债90万 − 已有保障33万 = 337万"],
    ref: "F-N55 明细与结果卡一致性专用锁：寿险 = 28×10 + 90 − 33 = 337 万；明细行须展示完整算式并与结果卡 337万 同源。旧实现明细硬写「280万 (年收入×10)」与结果卡 337万 矛盾 ⇒ 本串不命中。仅锚这一条输入绑定串，避免 stat 卡正确值让整个 expect「或」命中掩盖明细修复。默认组算式 20×10+80−10=270 ⇒ 不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "10", dt_expense: "8", dt_debt: "0", dt_existing: "200" },
    clicks: ["switchMethod('dual-ten'); calc()"],
    expect: ["年收入10万×10 + 负债0万 − 已有保障200万 = -100万；取零下限后 = 0万"],
    ref: "F-N55 触底：先准确展示原算式 −100 万，再显示零下限后的结果 0 万，不能把未经截断的算式直接写成等于 0。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "10", dt_expense: "8", dt_debt: "0", dt_existing: "100" },
    clicks: ["switchMethod('dual-ten');var r=String(document.getElementById('res').innerHTML),s=String(document.getElementById('statGrid').innerHTML);document.getElementById('__tbProbe').textContent='INSZERO '+(r.indexOf('年收入10万×10 + 负债0万 − 已有保障100万 = 0万；取零下限后 = 0万')>=0&&s.indexOf('0万')>=0?'OK':'BAD');"],
    expect: ["INSZERO OK"],
    ref: "原始结果恰好为零，明确展示零下限后结果并匹配结果卡。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "28", dt_expense: "15", dt_debt: "90", dt_existing: "33" },
    clicks: ["switchMethod('dual-ten');var r=String(document.getElementById('res').innerHTML),s=String(document.getElementById('statGrid').innerHTML);document.getElementById('dt_expense').value='99';calc();var r2=String(document.getElementById('res').innerHTML),s2=String(document.getElementById('statGrid').innerHTML);document.getElementById('__tbProbe').textContent='INSPOS '+(r.indexOf('年收入28万×10 + 负债90万 − 已有保障33万 = 337万；取零下限后 = 337万')>=0&&s.indexOf('337万')>=0&&s2.indexOf('337万')>=0&&r2.indexOf('年支出不进入本法则公式')>=0&&r2.indexOf('99万')>=0?'OK':'BAD');"],
    expect: ["INSPOS OK"],
    ref: "正值明细与结果卡一致；修改年支出不改变寿险计算并保留参考项说明。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "10.04", dt_expense: "8", dt_debt: "0", dt_existing: "0" },
    clicks: ["switchMethod('dual-ten');var r=String(document.getElementById('res').innerHTML),s=String(document.getElementById('statGrid').innerHTML);document.getElementById('__tbProbe').textContent='INSDEC '+(r.indexOf('= 100.4万；取零下限后 = 100.4万')>=0&&r.indexOf('100.4 万保额')>=0&&s.indexOf('100.4万')>=0?'OK':'BAD');"],
    expect: ["INSDEC OK"],
    ref: "允许小数输入时，明细、结果卡和险种建议同为 100.4 万，不泄漏浮点噪声或静默取整。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { ft_income: "45", ft_members: "5" },
    clicks: ["switchMethod('four-three'); calc()"],
    expect: ["450万", "4.5万", "投资比例 18.0万"],
    ref: "4321 法则（年收入 45 万、家庭 5 人）：人均可支配 = 45 ÷ 5 = 9 万，重疾 = max(9×3, 30) = 30 万；寿险 = max(年收入×10, 50) = 450 万；年保费预算 = 45×10% = 4.5 万；投资 = 45×40% = 18.0 万/年、生活 13.5、储蓄 9.0。默认组（20 万 / 3 人）⇒ 200 / 2.0 / 8.0 万，三条都不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { lv_age: "35", lv_retire: "65", lv_income: "30", lv_growth: "5", lv_consume: "40", lv_discount: "6" },
    clicks: ["switchMethod('life-value'); calc()"],
    expect: ["446万", "工作年限 30年", "年净贡献 18.0万"],
    ref: "生命价值法（现年 35、退休 65、年收入 30 万、收入增长 5%、个人消费 40%、贴现率 6%）：工作年限 = 65 − 35 = 30 年（页面取 Math.max(差, 1) 下限，此处不触底）；年净贡献 = 30 × (1 − 40%) = 18.0 万；生命价值 = Σ_{i=0..29} 18 × 1.05^i ÷ 1.06^{i+1}，python 独立复算 = **446 万**（取整后写回）。默认组（30 / 60 / 20 / 3% / 30% / 5%）⇒ 另一组值，三条都不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { nd_income: "25", nd_expense: "15", nd_mortgage: "150", nd_other_debt: "20", nd_education: "60", nd_parents: "40", nd_final: "15", nd_assets: "30", nd_spouse_income: "12", nd_years: "15" },
    clicks: ["switchMethod('needs'); calc()"],
    expect: ["生活支出缺口 45万", "家庭负债 170万", "300 万保额"],
    ref: "需求分析法：家庭负债 = 房贷 150 + 其他负债 20 = 170 万；生活支出缺口 = max((家庭开支 15 − 配偶收入 12) × 保障年限 15, 0) = 3 × 15 = 45 万；寿险保额 = max(170 + 教育 60 + 赡养 40 + 身后费用 15 + 缺口 45 − 已有资产 30, 0) = **300 万**。默认组（20 / 12 / 80 / 10 / 50 / 30 / 10 / 20 / 10 / 20）⇒ 负债 90、缺口 40、保额 200，三条都不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { nd_income: "20", nd_expense: "12", nd_mortgage: "80", nd_other_debt: "10", nd_education: "50", nd_parents: "30", nd_final: "10", nd_assets: "500", nd_spouse_income: "10", nd_years: "20" },
    clicks: ["switchMethod('needs'); calc()"],
    expect: ["子女教育 50万", "生活支出缺口 40万", "赡养父母 30万"],
    ref: "需求分析法反向上界：已有资产 500 万足以覆盖全部缺口（负债 90 + 教育 50 + 赡养 30 + 身后 10 + 缺口 (12−10)×20 = 40，合计 220 万）⇒ 寿险保额 = max(220 − 500, 0) = 0 万，但三项费用明细仍各自独立成立（50 / 40 / 30 万），可验证「保额归零 ≠ 明细被抹平」。锚全部取自明细行，不碰任何含 0 的输出。默认组（资产 20 万）⇒ 保额 200、缺口 40，明细行仍是默认口径但「子女教育 50万」等同串在双十/4321 默认组不存在（默认组根本没有这三行 ⇒ 不命中）。",
  },

  // ── 零用例加固（2026-10-06）──────────────────────────
  {
    slug: "finance/analysis-cost-1",
    inputs: { total: "250000", dec: "3" },
    expect: ["本成本池合计单位分摊额 = 250,000.000 ÷ 5,000.000 = 50.000 元 / 件", "250.000分摊率（元 / 单位基数）", "50.000本成本池合计单位分摊额（元 / 件）"],
    ref: "注入非默认(默认 total=120000/dec=2)：作业成本分配法 分摊额 = 250,000；分摊率 = 250,000 ÷ Σ基数 1,000 = 250.000 元/单位基数；综合单位成本 = 50.000 元/件。默认态 24.00（120,000 ÷ 5,000），三条均不命中。",
  },
  {
    slug: "finance/analysis-cost-1",
    inputs: { total: "120000", dec: "2", outQty: "1500,-500,1000" },
    clicks: ["calc()"],
    expect: ["合计 1,000.00 100.00% 120,000.00 —"],
    ref: "F-N84 真锁：产量含负值 -500，旧实现 qtyOk 只比条数、sumQty 累加负数得 2000 ⇒ 综合单位成本 60.00，合计行末位为 60.00；现 qtyOk 要求逐项有限且非负，负值使整体降级，合计行末位为「—」。锚点含 total=120,000（Σ基数默认 1,000）；默认 outQty=1500,2500,1000（全正，末位 24.00）不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/analysis-cost-1",
    inputs: { outQty: "1500,-500,1000" },
    clicks: ["calc()"],
    expect: ["产量必须为非负且有效的数字"],
    ref: "负产量应明确提示无效，而非误报条数不一致。",
  },
  {
    slug: "finance/analysis-cost-1",
    inputs: { outQty: "1500,abc,1000" },
    clicks: ["calc()"],
    expect: ["产量必须为非负且有效的数字"],
    ref: "非法产量应明确提示无效。",
  },
  {
    slug: "finance/analysis-cost-1",
    inputs: { outQty: "1500,1000" },
    clicks: ["calc()"],
    expect: ["产量条数（2）与对象条数（3）不一致"],
    ref: "产量数量不匹配时保留对应提示。",
  },
  {
    slug: "finance/analysis-44",
    inputs: { items: "X,-500,600\n主体工程,500000,530000" },
    clicks: ["calcBatch()"],
    expect: ["第 1 行「X」：计划投资须为大于 0"],
    ref: "F-N85 真锁：批量行 X 计划 -500（录入符号错误），旧 calcBatch 仅 isFinite 校验，负分母把超支翻成 -220% 且判「明显节约」；现 pl<=0 的行跳过并汇总提示。默认 items 无负计划（跳过 0）不命中 ⇒ 零逃生。",
  },

  // ── 零用例加固（2026-10-09）──────────────────────────
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "50" },
    expect: ["6.8966"],
    ref: "静态汇率表 USD=1、CNY=7.25；50 元 CNY→USD = 50/7.25 = 6.8966。锚点避开了「始终存在的速查表」里的 362.50（USD 50→362.50 CNY，注入失败也命中 ⇒ 假逃生项），改用随注入量变化的 6.8966。默认 fromAmount=100 → 13.7931，不命中。",
  },
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "200", rateMode: "manual", manualRate: "0.138" },
    clicks: ["calc()"],
    expect: ["27.6000"],
    ref: "手动汇率正向：1 CNY = 0.138 USD（默认币对 CNY→USD），200 CNY = 200 × 0.138 = **27.6000**。默认内置汇率 7.25⇒27.5862、默认手动 7.25⇒1,450，均不命中。该锚同时守住「手动汇率必须按当前币对取用」——旧实现任意币对都乘同一数值。",
  },
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "200", rateMode: "manual", manualRate: "0.138" },
    clicks: ["document.getElementById('toAmount').value='27.6'; calcReverse()"],
    expect: ["200.0000"],
    ref: "手动汇率反向：1 CNY = 0.138 USD ⇒ 1 USD = 1/0.138 CNY；27.6 USD 反向换算 = 27.6 / 0.138 = **200.0000**。旧实现反向仍做乘法 ⇒ 27.6 × 0.138 = 3.8088（缺陷复现值），绝不命中 200.0000。默认态与手动 7.25 同样不命中。",
  },
  {
    slug: "finance/text-reverse-words",
    inputs: { input: "Hello World", mode: "allchar" },
    expect: ["dlroW olleH"],
    ref: "按 allchar 模式整体反转：Hello World → dlroW olleH。默认态（mode=space、输入为「Hello World ToolBox/中文」两行）按词反转，输出不含 dlroW olleH ⇒ 不命中。",
  },
  {
    slug: "finance/text-reverse-words",
    inputs: { input: "COPY_ANCHOR_2026" },
    clicks: ["var __cpText='',__cpErr='none',__copied=false,__bv='复制结果';var __btn={};Object.defineProperty(__btn,'textContent',{get:function(){return __bv;},set:function(v){__bv=String(v);if(__bv.indexOf('✅ 已复制')>=0)__copied=true;}});__btn.closest=function(){return this;};var __ev={target:{closest:function(){return __btn;}}};document.getElementById('result').textContent=document.getElementById('input').value;navigator.clipboard.writeText=function(t){__cpText=String(t);return {then:function(cb){try{if(typeof cb==='function')cb();}catch(e){__cpErr=String(e&&e.message||e);}}}};try{copyResult(__ev);}catch(e){__cpErr=String(e&&e.message||e);}document.getElementById('__tbProbe').textContent='FN177 '+(__copied?'COPIED':'NO')+'|'+__cpErr+'|'+__cpText;"],
    expect: ["FN177 COPIED|none|COPY_ANCHOR_2026"],
    ref: "F-N177 复制回调防回归锁：copyResult(ev) 必须用形参 ev 的 target.closest('.btn') 取按钮，在 writeText().then() 回调里把文案改为「✅ 已复制」且回调不抛。修复前用全局 event（harness 页面作用域无 event）⇒ 回调抛 TypeError、按钮文案不变 ⇒ 探针为『FN177 NO|event is not defined|…』不命中；探针用 __tbProbe 记录按钮是否曾被写入「✅ 已复制」（避开 setTimeout 同步恢复污染）+ 绑定输入锚 ⇒ 零逃生。",
  },
  {
    slug: "finance/text-reverse-words",
    inputs: { input: "他说「你好，世界」。", mode: "zhchar" },
    clicks: ["document.getElementById('keepPunc').checked=true;reverse();document.getElementById('__tbProbe').textContent='FN179 '+document.getElementById('input').value+' '+document.getElementById('result').textContent;"],
    expect: ["FN179 他说「你好，世界」。 界世「好你，说他」。"],
    ref: "F-N179 中文标点原位防回归锁：keepPunc 用 Unicode 标点类 \\p{P} 覆盖「」等中文引号，zhchar 模式逐字切分后标点固定原位、仅汉字反转 ⇒ 界世「好你，说他」。（旧手写字符集不含「」⇒ 参与反转得 」界世好你，「说他。，不命中。）探针绑定输入锚与 __tbProbe ⇒ 默认态零逃生。",
  },
  {
    slug: "finance/futures-pnl-calculator",
    inputs: { openPrice: "4000", closePrice: "4200", lots: "2", marginRate: "10", openFee: "25", closeFee: "35" },
    expect: ["119,880.00", "240,000.00"],
    ref: "沪深300乘数 300、做多：盈亏点数=(4200−4000)×1=200；盈亏=200×300×2=120,000；手续费=(25+35)×2=120 ⇒ 净盈亏 119,880.00；合约价值=4000×300×2=2,400,000；保证金=2,400,000×10%=240,000.00。默认态(3500/3550/1/12/30/30)→净额 14,940.00、保证金 126,000.00，两条均不命中。",
  },
  {
    slug: "finance/gst-validator",
    inputs: { input: "27AAPFU0939F1ZV" },
    expect: ["校验位： V（期望 V）"],
    ref: "修复前 gstChecksum 用 const factor 却在循环里重赋值 ⇒ 所有浏览器都抛「Assignment to constant variable」整页失效；已改为 let。该号前 14 位 mod-36 校验位 = V 与末位一致 ⇒ 有效。expect 取页面回显「校验位： V（期望 V）」（含具体校验字符 ⇒ 默认预填 09AABCU9603R1ZL 输出「L（期望 L）」不命中，消除「✅ 有效」通用串导致的逃生）。",
  },
  {
    slug: "finance/gst-validator",
    inputs: { input: "00AAPFU0939F1ZB" },
    expect: ["❌ 州码 00 不在 GST 州/属地代码列表（现行 01–24、26、27、29–38；97 为 Other Territory）。", "校验位： B（期望 B）"],
    ref: "F-N170 未分配州码硬判：旧实现州码只用于展示，`zChar==='Z'` 且 mod-36 校验位正确即判「✅ GST 号码有效」，`00AAPFU0939F1ZB` 被判有效。现州码白名单参与结论，给出「州码 00 不在列表」并判「❌ GST 校验失败（州码不合法）」；第二条锚点验证错误态仍保留 PAN/实体/Z/校验位拆解（输入定位）。默认 09AABCU9603R1ZL 为合法 09 ⇒ 两条均不命中。",
  },
  {
    slug: "finance/gst-validator",
    inputs: { input: "99AAPFU0939F1ZK" },
    expect: ["99 - Centre Jurisdiction (special)", "✅ GST 号码有效"],
    ref: "F-GST99 口径统一：99 为 Centre Jurisdiction / Other Country 特殊注册码（与 gstin-validator 一致），不是未分配州码；校验位 K 正确 ⇒ 判格式有效。默认 09AABCU9603R1ZL 不含 99 ⇒ 不命中。",
  },
  {
    slug: "finance/gst-validator",
    inputs: { input: "25AAPFU0939F1ZZ" },
    expect: ["❌ 州码 25（Daman and Diu）已停用，现行应使用 26。"],
    ref: "F-N171 停用码 25：达曼和第乌 2020-01-26 并入「Dadra and Nagar Haveli and Daman and Diu」统一用 26；旧表仍把 25 列为 Daman and Diu 且判有效。现 25 从现行表移除，归到停用表并指引入 26。默认态 09 ⇒ 不命中。",
  },
  {
    slug: "finance/gst-validator",
    inputs: { input: "28AAPFU0939F1ZT" },
    expect: ["❌ 州码 28（Andhra Pradesh (Old)）已停用，现行应使用 37。"],
    ref: "F-N171 停用码 28：安得拉邦旧码，现行使用 37；旧表 `'28':'Andhra Pradesh (Old)'` 且判有效。现归到停用表并指引 37，同时保留 37/38 在现行表。默认态 09 ⇒ 不命中。",
  },
  {
    slug: "finance/gst-validator",
    inputs: { input: "26AAPFU0939F1ZX" },
    expect: ["州代码： 26 - Dadra and Nagar Haveli and Daman and Diu", "校验位： X（期望 X）"],
    ref: "F-N171 行政区名全称回归护栏：26 由旧半名「Dadra and Nagar Haveli」改为合并后全称，且仍是合法码 ⇒ 校验位 X 正确时应判有效。防止把停用逻辑误伤到 26。默认态 09 - Uttar Pradesh ⇒ 不命中。",
  },
  {
    slug: "finance/gst-validator",
    inputs: { input: "38AAPFU0939F1ZS" },
    expect: ["州代码： 38 - Ladakh", "校验位： S（期望 S）"],
    ref: "F-N170 白名单覆盖新增码护栏：38 Ladakh（2019 新增）与 37 安得拉邦新码必须留在现行表并判有效，避免「删旧码」时把新码一起误删。默认态 09 ⇒ 不命中。",
  },
  {
    "slug": "finance/aadhaar-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： abc123测试 ❌ 第 1 位含非法字符「a」"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，F-N151 修复后含字母在第 1 位报「非法字符「a」」（旧实现静默剔除后按位数判）；输出区绑定输入串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/aba-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "❌ 含非法字符：仅允许数字、空格或连字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，非法字符须被明确拒绝，不能静默剥离后计算。"
  },
  {
    "slug": "finance/abn-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "❌ 含非法字符：仅允许数字、空格或连字符"
    ],
    "ref": "ABN 非法字符必须明确拒绝，不能静默剔除或直接插入 HTML。"
  },
  {
    "slug": "finance/amount-in-words",
    "inputs": {
      "money": "42"
    },
    "expect": [
      "42\n中文大写： 肆拾贰元整"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"money\":\"42\"}，输出区含「42\n中文大写： 肆拾贰元整」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/analysis-5",
    "inputs": {
      "ca": "42",
      "inv": "42",
      "pre": "42",
      "cash": "42",
      "cl": "42",
      "tl": "42",
      "ta": "42",
      "dec": "42"
    },
    "expect": [
      "明细与合计不一致"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ca\":\"42\",\"inv\":\"42\",\"pre\":\"42\",\"cash\":\"42\",\"cl\":\"42\",\"tl\":\"42\",\"ta\":\"42\",\"dec\":\"42\"}，输出区含「质量需进一步核查。 所有者权益不为正（0.00 元），产权比率与权益乘数无法反映…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/analysis-risk",
    "inputs": {
      "s": "42",
      "v": "42",
      "f": "42",
      "i": "42",
      "t": "42",
      "n": "42",
      "dec": "42"
    },
    "expect": [
      "小数位数须为 0–4 的整数。"
    ],
    "ref": "第935批：dec=42 越界不再静默回退 2，而是明确提示 0–4 整数并停止计算；旧实现会照常输出敏感性表。"
  },
  {
    "slug": "finance/assessor-manager",
    "inputs": {
      "debtRatio": "42",
      "currentRatio": "42",
      "revenue": "42",
      "profitMargin": "42",
      "overdue": "42",
      "creditHistory": "42"
    },
    "expect": [
      "教学示例，不是真实信用评估。", "示例合计： 72 /100"
    ],
    "ref": "第935批：六项 42 分档得分 25+15+2+20+0+10=72，输出改为教学示例与分项表；旧自动用例锚定的「信用评估报告/催收策略」结构已移除。"
  },
  {
    "slug": "finance/analysis-cost-1",
    "inputs": {
      "total": "42",
      "outQty": "abc123测试",
      "dec": "42",
      "rows": "1\n2\n3",
      "baseName": "工时"
    },
    "expect": [
      "分摊额 本成本池单位分摊额 对象 1 1.00 16.67% 7.00 — 对象 2 2.00 33.33% 14.00 — 对象 3 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"total\":\"42\",\"outQty\":\"abc123测试\",\"dec\":\"42\",\"rows\":\"1\\n2\\n3\",\"baseName\":\"工时\"}，输出区含「分摊额 单位成本 对象 1 1.00 16.67% 7.00 — 对象 2 2.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/bic-lookup",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n按行名检索：ABC123测试 ❌ 离线库中未找到匹配的行名"
    ],
    "ref": "F-N186 同步：反向检索分支接管含中文的非 BIC 输入，`abc123测试` 修复后走行名检索并提示未找到（旧实现报「银行代码必须为大写字母」）；默认态（CHASUS33）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/cagr",
    "inputs": {
      "start": "42",
      "end": "42",
      "years": "42"
    },
    "expect": [
      "GR (%) 0.0000 增长率 (小数)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"start\":\"42\",\"end\":\"42\",\"years\":\"42\"}，输出区含「GR (%) 0.0000 增长率 (小数)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/bic-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（8 或 11） ❌ 前 4 位必须为字母（银行代码）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（8 或 11） ❌…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "finance/capm-return",
    "inputs": {
      "unit": "100",
      "rf": "42",
      "beta": "42",
      "rm": "42",
      "obs": "42"
    },
    "expect": [
      "00% ，α = 42.000% − 42.000% = 0.000% α 接近 0，实际收益与 CAPM 要求回报基本吻合，未发现明显的定价偏差。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rf\":\"42\",\"beta\":\"42\",\"rm\":\"42\",\"obs\":\"42\",\"unit\":\"100\"}，输出区含「00% ，α = 42.000% − 42.000% = 0.000% α 接近…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/cnpj-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： abc123测试 ❌ 第 1 位含非法字符「a」：CNPJ 只能包含数字及 . / - 分隔符。"
    ],
    "ref": "F-N168 字符白名单守卫（第98批同步）：注入非默认输入{\"input\":\"abc123测试\"}，旧实现先 replace(\\D,'') 静默剥离字母后按 123 判位数错误；新实现先白名单守卫点名第 1 位非法字符「a」。默认态（合法预填）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/break-even-calculator",
    "inputs": {
      "fc": "42",
      "price": "42",
      "vc": "42",
      "qty": "42",
      "pname": "abc123测试",
      "taxRate": "42",
      "chartMaxQty": "42",
      "chartStep": "42",
      "sensPct": "42",
      "detailStart": "42",
      "detailEnd": "42",
      "detailStep": "42"
    },
    "expect": [
      "42 1,764.00 1,764.00 42.00 1,806.00 0.00 -42.00 -2.38%"
    ],
    "ref": "第933批：detailStart=detailEnd=42、step=42 时只生成 1 行（42 件），不再把 end<=start 自动扩成 start+10×step；旧实现会扩到 462 并生成 42/84/…/252 多行。默认 0–20000 不命中。"
  },
  {
    "slug": "finance/calc-4",
    "inputs": {
      "amount": "42",
      "rate": "42",
      "years": "42",
      "type": "equal-principal"
    },
    "expect": [
      "42\n42\n42\nequal-principal\n1.55 元 首月还款 413.17 还款总额（元） 371.17 总利息（元） 504"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"amount\":\"42\",\"rate\":\"42\",\"years\":\"42\",\"type\":\"equal-principal\"}，输出区含「42\n42\n42\nequal-principal\n1.55 元 首月还款 413…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/calc-5",
    "inputs": {
      "cost": "42",
      "value": "42",
      "years": "42",
      "extra": "42"
    },
    "expect": [
      "0 元，最终价值 42.00 元，其他成本 42.00 元）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cost\":\"42\",\"value\":\"42\",\"years\":\"42\",\"extra\":\"42\"}，输出区含「0 元，最终价值 42.00 元，其他成本 42.00 元）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/bond-yield-calculator",
    "inputs": {
      "y-face": "42",
      "y-coupon": "42",
      "y-price": "42",
      "y-years": "42",
      "c-face": "42",
      "c-coupon": "42",
      "c-price": "42",
      "h-buy": "42",
      "h-sell": "42",
      "h-face": "42",
      "h-coupon": "42",
      "h-years": "42",
      "p-face": "42",
      "p-coupon": "42",
      "p-rate": "42",
      "p-years": "42",
      "y-freq": "2",
      "y-type": "zero",
      "h-freq": "2",
      "p-freq": "2",
      "p-type": "zero"
    },
    "expect": [
      "42\n42\n42\n42\n2\nzero\n📋 详细结果\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n2\n2\nzero"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"y-face\":\"42\",\"y-coupon\":\"42\",\"y-price\":\"42\",\"y-years\":\"42\",\"c-face\":\"42\",\"c-coupon\":\"42\",\"c-price\":\"42\",\"h-buy\":\"42\",\"h-sell\":\"42\",\"h-face\":\"42\",\"h-coupon\":\"42\",\"h-years\":\"42\",\"p-face\":\"42\",\"p-coupon\":\"42\",\"p-rate\":\"42\",\"p-years\":\"42\",\"y-freq\":\"2\",\"y-type\":\"zero\",\"h-freq\":\"2\",\"p-freq\":\"2\",\"p-type\":\"zero\"}，输出区含「42\n42\n42\n42\n2\nzero\n📋 详细结果\n42\n42\n42\n42\n4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/cpf-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： abc123测试 ❌ 第 1 位含非法字符「a」"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，F-N154 修复后含字母在第 1 位报「非法字符「a」」（旧实现静默剔除后按位数判）；输出区绑定输入串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/credit-card-bin",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "只能包含数字、空格或连字符"
    ],
    "ref": "BIN 输入含字母须拒绝，不能静默剥离后继续识别。"
  },
  {
    "slug": "finance/credit-card-luhn",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "只能包含数字、空格或连字符"
    ],
    "ref": "含非数字的 Luhn 输入须拒绝，不能静默剥离非法字符。"
  },
  {
    "slug": "finance/car-loan-calculator",
    "inputs": {
      "price": "42",
      "downPct": "42",
      "rate": "42",
      "taxRate": "42",
      "regFee": "42",
      "vehicleTax": "42",
      "compInsurance": "42",
      "commInsurance": "42",
      "years": "2",
      "insYears": "2"
    },
    "expect": [
      "51.11%"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"price\":\"42\",\"downPct\":\"42\",\"rate\":\"42\",\"taxRate\":\"42\",\"regFee\":\"42\",\"vehicleTax\":\"42\",\"compInsurance\":\"42\",\"commInsurance\":\"42\",\"years\":\"2\",\"insYears\":\"2\"}，输出区含「42\n42\n42\n2\n1.52\n12.05\n36.41\n33.1%\n51.11%\n0.0万\n1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。51.11% 为名义 42% 按月复利的有效年化 (1+42%/12)^12−1。"
  },
  {
    "slug": "finance/credit-card-type",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "只能包含数字、空格或连字符"
    ],
    "ref": "卡类型输入含非法字符须拒绝，不能静默剥离后识别。"
  },
  {
    "slug": "finance/credit-card-grace-period",
    "inputs": {
      "amt": "42",
      "yield": "42"
    },
    "expect": [
      "¥2.22 该笔资金收益（42%年化）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"amt\":\"42\",\"yield\":\"42\"}，真实日期口径最长免息期 46 天，收益 42×42%×46/365 = **¥2.22**；默认态不含该串 ⇒ 强判别、零逃生。"
  },
  
  {
    "slug": "finance/curp-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（应为 18）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（应为 18）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/currency-lookup",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\nInput: abc123测试 ❌ 本工具未收录该代码或名称 当前仅维护"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\nInput: abc123测试 ❌ 未找到匹配的货币 支持：I…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/currency-symbol",
    "inputs": {
      "searchInput": "abc123测试"
    },
    "expect": [
      "\n未找到匹配的货币\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"searchInput\":\"abc123测试\"}，输出区含「\n未找到匹配的货币\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/dea-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（应为 9） ❌ 长度必须为 9 字符（2 字母 + 7 数字）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（应为 9） ❌ 长…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/currency-converter",
    "inputs": {
      "fromAmount": "42",
      "fromSearch": "abc123测试",
      "toAmount": "42",
      "toSearch": "abc123测试",
      "batchFromSearch": "abc123测试",
      "batchToSearch": "abc123测试",
      "quickSearch": "abc123测试",
      "batchInput": "1\n2\n3"
    },
    "expect": [
      "1.00 🇨🇳 0.1379 🇺🇸",
      "2,207.6250"
    ],
    "ref": "批量换算 + 汇率来源（2026-10-25 新增功能同步）：batchInput=\"1\\n2\\n3\" ⇒ 批量表首行「1.00 🇨🇳 0.1379 🇺🇸」（CNY→USD，1 ÷ 7.25 = 0.1379）；toAmount=42 触发反算 ⇒ fromAmount 收敛为 304.50 USD，正向结果「2,207.6250」CNY（304.50 × 7.25）。两条均绑定注入值：默认态（batch 为 100/500/1000…、fromAmount=100 ⇒ 725.0000）都不含 ⇒ 零逃生。同时固定「汇率来源：内置参考值（静态，非实时）」这一新增口径标注不被误删（改文案本例即变红）。旧 expect 为输入回显长串，因新增「汇率来源」控件与速查表区块打断了回显序列，已按实测更新。"
  },
  {
    "slug": "finance/compound-interest",
    "inputs": {
      "principal": "42",
      "rate": "42",
      "years": "42",
      "annual": "42",
      "freq": "2",
      "investTime": "end"
    },
    "expect": [
      "0 0.00 1 42.00 42.00 19.49 103.49 84.00 19.49 2 103.49 42.00 48.03 193.52 126.00 67.52 3 193.52 42.00 89.81 325.34 168.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"principal\":\"42\",\"rate\":\"42\",\"years\":\"42\",\"annual\":\"42\",\"freq\":\"2\",\"investTime\":\"end\"}，输出区含「0 0.00 1 42.00 42.00 19.49 103.49 84.00 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/dni-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（应为 9） ❌ 长度必须为 9 字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（应为 9） ❌ 长…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/depreciation-calculator",
    "inputs": {
      "cost": "42",
      "salvage": "42",
      "life": "42",
      "totalUnits": "42"
    },
    "expect": [
      "请检查：原值 > 残值 ≥ 0，使用年限须为 1–100 的整数（折旧按整年计提）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cost\":\"42\",\"salvage\":\"42\",\"life\":\"42\",\"totalUnits\":\"42\"}，输出区含「42\n42\n42\n42\n请检查：原值 > 残值 ≥ 0，使用年限须为正整数（折旧按整年计提）」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/discount-calculator",
    "inputs": { "price": "250" },
    "clicks": ["updateDiscount(0,'8');calc()"],
    "expect": ["¥ 200.00"],
    "ref": "0–10 折单位修正：折扣链输入 8（即 8 折）⇒ 250×0.8 = ¥200.00、节省 ¥50.00；旧实现把输入 8 当 0.8 折 ⇒ 250×0.08 = ¥20.00（与 8 折差 10 倍）。默认价 100 下回退注入得 ¥80.00，不命中。"
  },
  {
    "slug": "finance/dns-record-info",
    "inputs": {
      "filterInput": "abc123测试"
    },
    "expect": [
      "abc123测试\n未找到匹配的记录类型"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"filterInput\":\"abc123测试\"}，输出区含「abc123测试\n未找到匹配的记录类型」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/esn-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 ❌ 第 7 位含非法字符「测」"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，F-N156 修复后含中文「测」在第 7 位报「非法字符」（旧实现静默剔除后按位数判格式不符）；输出区绑定输入串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/ein-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "输入： abc123测试 ❌ 含非法字符，仅允许数字、空格和连字符"
    ],
    "ref": "EIN 非数字字符不得被静默剔除，输入含字母时应报告非法字符。"
  },
  {
    "slug": "finance/generator-report-1",
    "inputs": {
      "rev": "2000",
      "costRate": "50",
      "opex": "300",
      "taxRate": "25",
      "asset": "1500",
      "debtRatio": "40",
      "dep": "100",
      "capex": "200",
      "dividend": "100",
      "cash0": "500"
    },
    "expect": [
      "净利润 525.00"
    ],
    "ref": "确定性算例：收入 2000、成本率 50% → 毛利 1000 − 费用 300 = 营业利润 700，税率 25% → 所得税 175、净利润 525；默认参数净利润 150.00，注入态不含该串 ⇒ 区分真三表勾稽与随机模拟。"
  },
  {
    slug: "finance/generator-report-1",
    inputs: { rev: "1000", costRate: "65", opex: "150", taxRate: "25", asset: "1200", debtRatio: "45", dep: "60", capex: "80", dividend: "30", cash0: "200", depMode: "excluded", wc: "50" },
    clicks: ["gen()"],
    expect: ["未含，已在营业利润中扣除 60.00", "净利润 105.00", "经营活动 115.00", "营运资本增加 50.00"],
    ref: "第933批：折旧未含在费用时单独扣除一次 ⇒ 营业利润 350−150−60=140、税 35、净利 105；间接法 105+60−50=115 经营现金流。旧实现不扣折旧，净利 165、CFO 225。默认折旧含在费用 ⇒ 不命中。",
  },
  {
    "slug": "finance/futures-pnl-calculator",
    "inputs": {
      "openPrice": "42",
      "closePrice": "42",
      "lots": "42",
      "marginRate": "42",
      "openFee": "42",
      "closeFee": "42"
    },
    "expect": [
      "· 保证金10%\n42\n42\n42\n42\n42\n42\n盈亏金额 -3,528.00 手续费 3,528"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"openPrice\":\"42\",\"closePrice\":\"42\",\"lots\":\"42\",\"marginRate\":\"42\",\"openFee\":\"42\",\"closeFee\":\"42\"}，输出区含「· 保证金10%\n42\n42\n42\n42\n42\n42\n盈亏金额 -3,528.0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/gst-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（应为 15） ❌ 长度必须为 15 字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（应为 15） ❌ …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/gstin-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（应为 15） ❌ 长度必须为 15 字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（应为 15） ❌ …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/iccid-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "含非法字符，仅允许数字、空格和连字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： abc123测试 ⚠️ ICCID 通常为 19 或 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/iban-validator",
    "inputs": {
      "ibanInput": "abc123测试"
    },
    "expect": [
      "❌ 格式错误：IBAN 应以 2 位国家代码 + 2 位校验位 + BBAN 组成"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"ibanInput\":\"abc123测试\"}，输出区含「n6!n10!n\nabc123测试\n❌ 格式错误：IBAN 应以 2 位国家代码…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/imei-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "输入： abc123测试 ❌ 含非法字符，仅允许数字、空格和连字符"
    ],
    "ref": "IMEI 和 IMEISV 不得静默丢弃输入中的非法字符。"
  },
  {
    "slug": "finance/dca-calculator",
    "inputs": {
      "monthly": "42",
      "years": "42",
      "rate": "42",
      "initial": "42"
    },
    "expect": [
      "收益率 第1年 ¥504.00 ¥546.00 ¥676.75 +¥130.75 +23.95% 第2年 ¥504.00 ¥1,050.00 ¥1,635.89 +¥455.15 +55.80% 第3年 ¥504.00 ¥1,554.00 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"monthly\":\"42\",\"years\":\"42\",\"rate\":\"42\",\"initial\":\"42\"}，输出区含「收益率 第1年 ¥504.00 ¥546.00 ¥676.75 +¥130.75…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/ifsc-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（应为 11） ❌ 长度必须为 11 字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（应为 11） ❌ …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/gold-price-calculator",
    "inputs": {
      "goldPrice": "42",
      "usdRate": "42",
      "discountRate": "42",
      "weightInput": "42",
      "totalInput": "42",
      "convInput": "42",
      "puritySel": "0.999",
      "weightUnit": "kg",
      "convUnit": "kg"
    },
    "expect": [
      " 钱（qian） 8,400.0000 42.0000千克 = 42,000.000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"goldPrice\":\"42\",\"usdRate\":\"42\",\"discountRate\":\"42\",\"weightInput\":\"42\",\"totalInput\":\"42\",\"convInput\":\"42\",\"puritySel\":\"0.999\",\"weightUnit\":\"kg\",\"convUnit\":\"kg\"}，输出区含「 钱（qian） 8,400.0000 42.0000千克 = 42,000.0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/imsi-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "含非法字符，仅允许数字、空格和连字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： abc123测试 ⚠️ IMSI 通常为 15 位数字…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/insurance-calculator",
    "inputs": {
      "dt_income": "42",
      "dt_expense": "42",
      "dt_debt": "42",
      "dt_existing": "42",
      "ft_income": "42",
      "ft_members": "42",
      "lv_age": "42",
      "lv_retire": "42",
      "lv_income": "42",
      "lv_growth": "42",
      "lv_consume": "42",
      "lv_discount": "42",
      "nd_income": "42",
      "nd_expense": "42",
      "nd_mortgage": "42",
      "nd_other_debt": "42",
      "nd_education": "42",
      "nd_parents": "42",
      "nd_final": "42",
      "nd_assets": "42",
      "nd_spouse_income": "42",
      "nd_years": "42"
    },
    "expect": [
      "况咨询专业保险顾问\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"dt_income\":\"42\",\"dt_expense\":\"42\",\"dt_debt\":\"42\",\"dt_existing\":\"42\",\"ft_income\":\"42\",\"ft_members\":\"42\",\"lv_age\":\"42\",\"lv_retire\":\"42\",\"lv_income\":\"42\",\"lv_growth\":\"42\",\"lv_consume\":\"42\",\"lv_discount\":\"42\",\"nd_income\":\"42\",\"nd_expense\":\"42\",\"nd_mortgage\":\"42\",\"nd_other_debt\":\"42\",\"nd_education\":\"42\",\"nd_parents\":\"42\",\"nd_final\":\"42\",\"nd_assets\":\"42\",\"nd_spouse_income\":\"42\",\"nd_years\":\"42\"}，输出区含「况咨询专业保险顾问\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/irr-calculator",
    "inputs": {
      "discountRate": "42",
      "periodUnit": "month"
    },
    "expect": [
      "T1 ✕ T2 ✕ T3 ✕ T4 ✕ T5 ✕ T6 ✕",
      "month",
      "42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"discountRate\":\"42\",\"periodUnit\":\"month\"}。2026-11-07 F-N8 同批重采：页面新增只读输入 `irrCashflowSnapshot` 后，cfList 与期数单位之间多了一段现金流快照值，旧锚「5 ✕ T6 ✕\\n42\\nmonth」的跨元素拼接被截断，属**用例过期**而非页面缺陷；新锚改为「快照值 + month + 42」，同时锁住快照输入存在与注入生效。默认态（year / 8）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/ird-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "含非法字符，仅允许数字、空格和连字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： abc123测试 ⚠️ IRD 必须为 8 或 9 位…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/installment-real-rate",
    "inputs": {
      "P": "42",
      "n": "42",
      "r": "42"
    },
    "expect": [
      " 本期还款 1 1.00 17.64 18.64 2 1.00 17.64 18.64 3 1.00 17.64 18.64 4 1.00 17.64 18.64 5 1.00 17.64 18.64 6 1.00 17.64 18.64 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"P\":\"42\",\"n\":\"42\",\"r\":\"42\"}，输出区含「 本期还款 1 1.00 17.64 18.64 2 1.00 17.64 18…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/investment-calculator",
    "inputs": {
      "initial": "42",
      "final": "42",
      "years": "42",
      "additional": "42"
    },
    "expect": [
      "42\n42\n42\n42\n初始投入： 42 元 追加投入： 42 元 总投入： 84 元 期末价值： 42 元 累计盈亏： -42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"initial\":\"42\",\"final\":\"42\",\"years\":\"42\",\"additional\":\"42\"}，输出区含「42\n42\n42\n42\n初始投入： 42 元 追加投入： 42 元 总投入： 8…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/inflation-calculator",
    "inputs": {
      "amt": "42",
      "rate": "42",
      "years": "42"
    },
    "expect": [
      "年份 年初金额 当年通胀 年末购买力 累计缩水 第1年 ¥42.00 ¥12.42 ¥29.58 29.58%"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"amt\":\"42\",\"rate\":\"42\",\"years\":\"42\"}，正向表格首行应为「年初 42.00 → 年末 29.58」，缩水 12.42（29.58%）。旧期望串是反向分支的递增序列（靠兜底 switchMode() 污染命中）；反向公式修正后须改锚正向首行。默认态 100,000/3%/20 年 ⇒ 不命中。"
  },
  {
    "slug": "finance/investment-roi",
    "inputs": {
      "cost": "42",
      "return": "42",
      "years": "42",
      "discount": "42",
      "monthly": "42",
      "annualRate": "42",
      "period": "42",
      "aCost": "42",
      "aRate": "42",
      "aYears": "42",
      "aAdd": "42",
      "bCost": "42",
      "bRate": "42",
      "bYears": "42",
      "bAdd": "42",
      "unit": "month",
      "freq": "weekly"
    },
    "expect": [
      "-29.69 NPV 净现值 0.29 获利指数 PI -- 投资回收期 3.50年 持有期",
      "91,728 累计投入"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cost\":\"42\",\"return\":\"42\",\"years\":\"42\",\"discount\":\"42\",\"monthly\":\"42\",\"annualRate\":\"42\",\"period\":\"42\",\"aCost\":\"42\",\"aRate\":\"42\",\"aYears\":\"42\",\"aAdd\":\"42\",\"bCost\":\"42\",\"bRate\":\"42\",\"bYears\":\"42\",\"bAdd\":\"42\",\"unit\":\"month\",\"freq\":\"weekly\"}，输出区含「00% 简单年化 -29.69 NPV 净现值 0.29 获利指数 PI -- …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/invoice-generator",
    "inputs": {
      "customTax": "42",
      "s-total": "42",
      "s-excl": "42",
      "s-tax": "42",
      "sp-total": "42",
      "sp-limit": "42",
      "cb-target": "42",
      "cb-tolerance": "42",
      "cb-amt1": "42",
      "cb-amt2": "42",
      "cb-amt3": "42",
      "cb-amt4": "42",
      "rv-total": "42",
      "rv-tax": "42",
      "rv-excl": "42",
      "sp-method": "max",
      "sp-type": "excl"
    },
    "expect": [
      "计 ÷ (1 + 42%) = 42.00 ÷ 1.42 = ¥29.58",
      "肆拾贰圆整"
    ],
    "ref": "价税分离 + 金额大写（2026-10-25 新增功能同步）：四分支与拆票参数全取 42 ⇒ 单票口径 42 ÷ 1.42 = 29.58（不含税）、税额 12.42；结果区追加「🧾 发票行（价税分离）」四行（不含税金额/税率/税额/价税合计），并把价税合计 42.00 转成人民币大写「肆拾贰圆整」（票据口径：肆拾贰+圆+整）。三个串分别绑定计算公式、新增发票行区块与大写算法（默认态 10000 → 壹万圆整，不含这些串）⇒ 零逃生；大写进位/单位（拾佰仟万亿）任一回归本例即变红。"
  },
  {
    "slug": "finance/meid-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 ❌ 含非法字符（仅允许 0-9、A-F 及空格/连字符）"
    ],
    "ref": "F-N206 同步：含字母 G-Z/中文的非法输入修复后走「含非法字符」拒绝（旧实现剥离字母按清洗位数报长度错误）；默认态纯 hex A0000012345678 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/mirror-text",
    "inputs": {
      "input": "1\n2\n3"
    },
    "expect": [
      "1 2 3\nƐ S 1\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\"}，输出区含「1 2 3\nƐ S 1\n1 2 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/loan-comparison",
    "inputs": {
      "a-principal": "42",
      "a-rate": "42",
      "a-months": "42",
      "b-principal": "42",
      "b-rate": "42",
      "b-months": "42",
      "c-principal": "42",
      "c-rate": "42",
      "c-months": "42"
    },
    "expect": [
      "方案 A 月供： 1.92 元 总利息：38.79 元 还款总额：80.79 元"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a-principal\":\"42\",\"a-rate\":\"42\",\"a-months\":\"42\",\"b-principal\":\"42\",\"b-rate\":\"42\",\"b-months\":\"42\",\"c-principal\":\"42\",\"c-rate\":\"42\",\"c-months\":\"42\"}，输出区含「案 ，0.00 元\n42\n42\n42\n42\n42\n42\n42\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/mortgage-prepayment",
    "inputs": {
      "principal": "42",
      "rate": "42",
      "months": "42",
      "monthly": "42",
      "prepay": "42",
      "precision": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n提前还款金额已覆盖本金"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"principal\":\"42\",\"rate\":\"42\",\"months\":\"42\",\"monthly\":\"42\",\"prepay\":\"42\",\"precision\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n提前还款金额已覆盖本金」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/msisdn-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n❌ 仅允许数字及 +、空格、连字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n❌ 仅允许数字及 +、空格、连字符」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/nie-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（应为 9） ❌ 长度必须为 9 字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（应为 9） ❌ 长…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/mortgage-calculator",
    "inputs": {
      "loanAmount": "42",
      "rate": "42",
      "downPayment": "42",
      "years": "10"
    },
    "expect": [
      "¥243,600.00",
      "1 ¥8,665.62 ¥139.62 ¥8,526.00 ¥243,460.38"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"loanAmount\":\"42\",\"rate\":\"42\",\"downPayment\":\"42\",\"years\":\"10\"}。修复后贷款本金 = 42 万×(1−42%) = **¥243,600.00**（旧实现忽略首付 ⇒ 42 万，本串不命中）；月供 8,665.62、首月利息 = 243,600×42%/12 = **¥8,526.00**、首月本金 139.62、余额 243,460.38 自洽。默认态（房价 100 万 / 4.2% / 首付 30% / 30 年 ⇒ 本金 70 万）不含这两串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/npi-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： 123 ⚠️ NPI 必须为 10 位数字（当前 3 位）"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： 123 ⚠️ NPI 必须为 10 位数字（当前 3 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/nric-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（应为 9） ❌ 长度必须为 9 字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（应为 9） ❌ 长…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/number-to-words-chinese",
    "inputs": {
      "inputVal": "abc123测试"
    },
    "expect": [
      "abc123测试\n请输入有效数字"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inputVal\":\"abc123测试\"}，输出区含「abc123测试\n请输入有效数字」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/number-to-words",
    "inputs": {
      "inputVal": "abc123测试"
    },
    "expect": [
      "abc123测试\n请输入有效数字"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inputVal\":\"abc123测试\"}，输出区含「abc123测试\n请输入有效数字」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/npv-calculator",
    "inputs": {
      "rate": "42",
      "init": "42"
    },
    "clicks": ["cashFlows=['3000','3000','3000','3000'];renderCashFlows();calc()"],
    "expect": [
      "折现率： 42.00%"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"rate\":\"42\",\"init\":\"42\"}，输出区含「第4期 +0 0 +8,958 折现率： 42.00% NPV ≥ 0： ✓ 可…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/lease-payment-calculator",
    "inputs": {
      "pv": "42",
      "downPct": "42",
      "rate": "42",
      "months": "42",
      "fv": "42",
      "fee": "42",
      "type": "principal",
      "timing": "begin"
    },
    "expect": [
      "⚠ 期初还款仅支持等额本息；等额本金与先息后本请选择期末还款。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pv\":\"42\",\"downPct\":\"42\",\"rate\":\"42\",\"months\":\"42\",\"fv\":\"42\",\"fee\":\"42\",\"type\":\"principal\",\"timing\":\"begin\"}，输出区含「余本金 第1期 ¥0.45 ¥-0.42 ¥0.87 ¥24.78 第2期 ¥0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    slug: "finance/password-generator-advanced",
    inputs: { "len": "8", "count": "3" },
    clicks: ["document.getElementById('up').checked=true;document.getElementById('lo').checked=true;document.getElementById('nm').checked=true;generate();var before=String(document.getElementById('output').innerHTML).length;clearAll();document.getElementById('__tbProbe').textContent='PGCLR before='+(before>0?'Y':'N')+' after='+String(document.getElementById('output').innerHTML).length+' strength='+String(document.getElementById('strengthText').textContent);"],
    expect: ["PGCLR before=Y after=0 strength=点击生成按钮"],
    ref: "F-N142 核实锁：旧按钮 onclick 只声明常量，生成 3 条后清空无效；现 clearAll() 同时清 #output 与强度条并把文案复位「点击生成按钮」。探针绑定 before>0 与 after=0，默认态无 PGCLR 探针串 ⇒ 零逃生。",
  },
  {
    slug: "finance/password-generator-advanced",
    inputs: { "len": "8", "count": "3" },
    clicks: ["document.getElementById('up').checked=true;document.getElementById('lo').checked=true;document.getElementById('nm').checked=true;generate();var q=document.querySelectorAll;document.querySelectorAll=function(sel){if(sel==='#output .hist-item'){return [{textContent:'AAAAAAAA'},{textContent:'BBBBBBBB'},{textContent:'CCCCCCCC'}];}return q(sel);};var t='';navigator.clipboard={writeText:function(s){t=String(s);return Promise.resolve();}};copyResult();document.querySelectorAll=q;document.getElementById('__tbProbe').textContent='PGCOPY='+JSON.stringify(t);"],
    expect: ["PGCOPY=\"AAAAAAAA\\nBBBBBBBB\\nCCCCCCCC\""],
    ref: "F-N144 核实锁：stub DOM 不建模 innerHTML 子元素 textContent（#output.textContent 为空、.hist-item 节点无文本），故注入 querySelectorAll 桩返回三条固定文本，直接验证 copyResult 的逐行 join('\n') 行为：旧实现取整块 textContent ⇒ 无换行；现逐条文本换行拼接 ⇒ 三条各行。探针由 clicks 写入，默认态无 PGCOPY 串。",
  },
  {
    slug: "finance/password-generator-advanced",
    clicks: ["updateStrengthBatch(['a','Abcdefgh1!']);document.getElementById('__tbProbe').textContent='PGBAT '+String(document.getElementById('strengthText').textContent);"],
    expect: ["PGBAT 强度：弱 (1/5)（批量按最弱一条）"],
    ref: "F-N145 核实锁：批量强度取最弱一条并标注「批量按最弱一条」；第933批改为按随机空间熵估算，'a'（1 位小写，约 4.7 bit）得 1 分而非旧字符种类计分的 0 分，'Abcdefgh1!' 约 66 bit 得 4 分 ⇒ 取最弱 1 分「弱」。默认态无 PGBAT 探针串 ⇒ 零逃生。",
  },
  {
    slug: "finance/password-generator-advanced",
    inputs: { "len": "8", "count": "2" },
    clicks: ["__password_generator_advanced_last=0;__password_generator_advancedSnap=function(){return {count:'2',len:'8'};};__password_generator_advancedResText=function(){return 'AAAAAAAA BBBBBBBB';};var rec=null;if(typeof TBKit==='undefined'){TBKit={util:{isEn:function(){return false},diffBox:function(){}},history:{record:function(r){rec=r;},last:function(){return null;},mount:function(){},list:function(){return [];}},matrix:{table:function(){}}};}else{TBKit.util=TBKit.util||{};TBKit.util.isEn=function(){return false;};TBKit.util.diffBox=function(){};TBKit.history={record:function(r){rec=r;},last:function(){return null;},mount:function(){},list:function(){return [];}};TBKit.matrix=TBKit.matrix||{};TBKit.matrix.table=function(){};}__password_generator_advancedExtras();document.getElementById('__tbProbe').textContent='PGMASK='+(rec?String(rec['结果']||''):'NOREC');"],
    expect: ["PGMASK=已生成 2 条 · 长度 8（未保存明文）"],
    ref: "F-N143 隐私锁：stub 的组合选择器不识别 input[id],select[id] 等，故对快照/结果文本注入桩函数，直接验证 Extras 写入历史的 rk 字段是掩码而非明文：旧实现 rec[rk]=res（明文）⇒ 不命中；现写「已生成 N 条 · 长度 L（未保存明文）」。绑定注入 len=8/count=2，默认态无 PGMASK 探针。",
  },
  {
    "slug": "finance/password-generator-advanced",
    "inputs": {
      "len": "42",
      "exclude": "abc123测试",
      "count": "42"
    },
    "expect": [
      "生成数量须为 1–20 的整数（当前 42）"
    ],
    "ref": "第933批：生成数量不再接受越界值；len=42 合法但 count=42 超出 1–20，必须拒绝并提示，不能静默生成 42 条。默认 count=1 ⇒ 不命中。"
  },
  {
    "slug": "finance/pan-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（应为 10） ❌ 长度必须为 10 字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： ABC123测试 长度： 8 字符（应为 10） ❌ …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/option-profit-calculator",
    "inputs": {
      "strike": "42",
      "premium": "42",
      "s0": "42",
      "contracts": "42",
      "mult": "42",
      "fee": "42"
    },
    "expect": [
      " 元 合约数量： 42 张 × 乘数 42 权利金成本： ¥74,088"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"strike\":\"42\",\"premium\":\"42\",\"s0\":\"42\",\"contracts\":\"42\",\"mult\":\"42\",\"fee\":\"42\"}，输出区含「 元 合约数量： 42 张 × 乘数 42 权利金成本： ¥74,088」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/portfolio-return",
    "inputs": {
      "w1": "42",
      "r1": "42",
      "w2": "42",
      "r2": "42"
    },
    "expect": [
      "权重合计为 84.00%，不是 100%。剩余 16.00% 对应的资产与收益未定义"
    ],
    "ref": "第933批：42/42 权重合计 84%，默认拒绝当作完整组合；旧实现输出 42.00 并仅标偏差。默认 60/40 合计 100% ⇒ 不命中。"
  },
  {
    "slug": "finance/points-redemption-value",
    "inputs": {
      "pts": "42",
      "val": "42",
      "fee": "42"
    },
    "expect": [
      "0.00 每万分兑换价值（元） 0.00 每 100 分兑换价值（元） 偏亏"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"pts\":\"42\",\"val\":\"42\",\"fee\":\"42\"}，净价值 0，输出「0.00 每万分兑换价值（元） 0.00 每 100 分兑换价值（元） 偏亏」；默认态 20.00 不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/postal-code-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 ❌ 不匹配任何已知国家的邮编格式"
    ],
    "ref": "F-N218 同步：香港 /.*/ 不再默认通过，带中文的任意串 `abc123测试` 修复后落入「不匹配任何已知国家的邮编格式」；默认态（100000）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/position-size-calculator",
    "inputs": {
      "k-capital": "42",
      "k-winrate": "42",
      "k-ratio": "42",
      "k-fraction": "42",
      "f-capital": "42",
      "f-percent": "42",
      "f-price": "42",
      "f-stop": "42",
      "r-capital": "42",
      "r-riskpct": "42",
      "r-price": "42",
      "r-stop": "42",
      "m-initial": "42",
      "m-multiplier": "42",
      "m-times": "42",
      "m-droppct": "42"
    },
    "expect": [
      "凯利分数须在 0%–100% 之间。"
    ],
    "ref": "逐项范围校验：全部字段注入 42 时，胜率 42%（合法）、盈亏比 42（合法）、凯利分数 42 是 42% 还是 4200% 的歧义输入，页面按百分数字段读取 42 并判定超过 100% ⇒ 拒绝计算。旧实现若直接乘 fraction=42 会给出 1706% 的荒谬仓位；现字段级拒绝。默认 10000/55%/2/100% 合法且不出现该提示 ⇒ 注入专属，零逃生。"
  },
  {
    "slug": "finance/report-1",
    "inputs": {
      "inv": "42",
      "pct": "42",
      "capital": "42",
      "retained": "42",
      "premium": "42",
      "profit": "42",
      "dec": "42"
    },
    "expect": [
      "少数股东损益 = 42.00 × 58% = 24.36 元 长期股权投资低于按账面净资产计算的应享份额，简化差额 10.92 元。该负数 不是可直接计入营业外收入的负商誉"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inv\":\"42\",\"pct\":\"42\",\"capital\":\"42\",\"retained\":\"42\",\"premium\":\"42\",\"profit\":\"42\",\"dec\":\"42\"}，输出区含「少数股东损益 = 42.00 × 58% = 24.36 元 长期股权投资低于按账面净资产…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/mutual-fund-calculator",
    "inputs": {
      "monthly": "42",
      "years": "42",
      "rate": "42",
      "initial": "42",
      "buyFee": "42",
      "manageFee": "42",
      "custodyFee": "42",
      "sellFee": "42"
    },
    "expect": [
      "期末资产 ¥403.68 累计收益 -¥20,806.32 费用合计 ¥32,413.35"
    ],
    "ref": "月末买入下 42 年、42% 收益和各项 42% 费率时，期末资产 403.68、亏损 20,806.32；费用合计改为 32,413.35，除申购/赎回费外包含逐月管理费与托管费，旧用例只统计交易费 9,200.52 会系统性偏低。"
  },
  {
    "slug": "finance/rental-yield-calculator",
    "inputs": {
      "price": "42",
      "area": "42",
      "rent": "42",
      "fee": "42",
      "heat": "42",
      "decor": "42",
      "repair": "42",
      "agency": "42",
      "tax": "42",
      "loanRatio": "42",
      "loanRate": "42",
      "loanYears": "42",
      "rentMode": "year",
      "loanType": "principal"
    },
    "expect": [
      "成本明细 物业费 504 元 取暖费 42 元 装修折旧 42 元 维修基金 42 元 中介费 42 元 税费及其他 42 元 合计 714 元\n42\n42\n42\nprincipal"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"price\":\"42\",\"area\":\"42\",\"rent\":\"42\",\"fee\":\"42\",\"heat\":\"42\",\"decor\":\"42\",\"repair\":\"42\",\"agency\":\"42\",\"tax\":\"42\",\"loanRatio\":\"42\",\"loanRate\":\"42\",\"loanYears\":\"42\",\"rentMode\":\"year\",\"loanType\":\"principal\"}，输出区含「成本明细 物业费 504 元 取暖费 42 元 装修折旧 42 元 维修基金 4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/routing-number-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "❌ 含非法字符：仅允许数字、空格或连字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，非法字符须被明确拒绝，不能静默剥离后计算。"
  },
  {
    "slug": "finance/payroll-calculator",
    "inputs": {
      "salary": "42",
      "bonus": "42",
      "pension": "42",
      "medical": "42",
      "unemployment": "42",
      "housing": "42",
      "base": "42",
      "children": "42",
      "continuing": "42",
      "housingLoan": "42",
      "rent": "42",
      "elderly": "42",
      "baby": "42",
      "medicalBig": "42",
      "threshold": "42",
      "city": "beijing"
    },
    "expect": [
      "年终奖并入综合所得"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"salary\":\"42\",\"bonus\":\"42\",\"pension\":\"42\",\"medical\":\"42\",\"unemployment\":\"42\",\"housing\":\"42\",\"base\":\"42\",\"children\":\"42\",\"continuing\":\"42\",\"housingLoan\":\"42\",\"rent\":\"42\",\"elderly\":\"42\",\"baby\":\"42\",\"medicalBig\":\"42\",\"threshold\":\"42\",\"city\":\"beijing\"}，输出区含「计个税 第1月 ¥42.00 ¥9.45 ¥0.00 ¥32.55 ¥0.00 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/payroll-calculator",
    "inputs": { "salary": "15000", "pension": "-8" },
    "expect": ["养老保险比例不能为负数"],
    "ref": "负社保比例原实现照算，五险一金为负 ⇒ 税后到手反而超过税前；现拦截提示。默认 8% 不出现该提示。"
  },
  {
    "slug": "finance/payroll-calculator",
    "inputs": { "salary": "" },
    "expect": ["税前工资须为 ≥0 的数字"],
    "ref": "空工资原实现 +el.value||0 ⇒ 全 0 结果；现显式提示。默认 15000 不出现该提示。"
  },
  {
    "slug": "finance/payroll-calculator",
    "inputs": { "salary": "15000", "base": "0" },
    "expect": ["8,280.00", "171,720.00"],
    "ref": "社保基数显式填 0（原实现 `base || salary` 无法表达「不缴」）：五险一金 0；月应纳税所得 15000−0−5000−1000=9000；全年 108000 ⇒ 个税 = 108000×10%−2520 = 8280；年税后 = 180000−8280 = 171720。默认基数 15000 的个税为 4230、年税后 175770，两锚均不命中。"
  },
  {
    "slug": "finance/rental-yield-calculator",
    "inputs": { "price": "300", "area": "0", "rentMode": "month", "rent": "5000", "fee": "0", "heat": "0", "decor": "0", "repair": "0", "agency": "0", "tax": "0", "loanRatio": "70", "loanRate": "0", "loanYears": "30", "loanType": "equal" },
    "clicks": ["toggleLoan();"],
    "expect": ["5,833"],
    "ref": "0% 利率分支：贷款 300×70% = 210 万、360 期 ⇒ 月供 = 2100000/360 = 5833（等额本息公式分母 0 会得 NaN，旧实现输出 —）。默认关闭贷款，结果卡不含「月供 5,833」。"
  },
  {
    "slug": "finance/rental-yield-calculator",
    "inputs": { "price": "", "rent": "5000" },
    "expect": ["请输入大于 0 的房屋总价（万元）"],
    "ref": "空房价原实现 `||0` ⇒ 总价 0、回报率恒 0%；现拦截提示。默认 300 万不出现该提示。"
  },
  {
    "slug": "finance/cagr",
    "inputs": { "start": "100", "end": "-50", "years": "2" },
    "expect": ["终值必须大于 0"],
    "ref": "负终值时 Math.pow(负值, 1/2) = NaN，原实现静默显示「—」；现拦截并说明 CAGR 无定义。默认 100→180 不出现该提示。"
  },
  {
    "slug": "finance/retirement-calculator",
    "inputs": {
      "age": "42",
      "retireAge": "42",
      "lifeAge": "42",
      "currentSavings": "42",
      "monthlyContribution": "42",
      "returnRate": "42",
      "inflation": "42",
      "monthlyExpense": "42"
    },
    "expect": [
      "42\n42\n42\n42\n42\n42\n42\n42\n年龄顺序：当前",
      "⚠ 年龄顺序无效，年度明细与导出数据已清空，请修正后再计算。"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"age\":\"42\",\"retireAge\":\"42\",\"lifeAge\":\"42\",\"currentSavings\":\"42\",\"monthlyContribution\":\"42\",\"returnRate\":\"42\",\"inflation\":\"42\",\"monthlyExpense\":\"42\"}，输出区含「42\n42\n42\n42\n42\n42\n42\n42\n年龄顺序：当前」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/profit-margin-calculator",
    "inputs": {
      "revenue": "42",
      "cogs": "42",
      "sellingExp": "42",
      "adminExp": "42",
      "rdExp": "42",
      "finExp": "42",
      "da": "42",
      "taxRate": "42",
      "revRev": "42",
      "targetMargin1": "42",
      "expRatio1": "42",
      "costCost": "42",
      "targetMargin2": "42",
      "taxRate2": "42",
      "batchStart": "42",
      "batchEnd": "42",
      "batchStep": "42",
      "batchM1": "42",
      "batchM2": "42",
      "batchM3": "42",
      "batchM4": "42",
      "dupontNI": "42",
      "dupontRev": "42",
      "dupontAssets": "42",
      "dupontEquity": "42",
      "marginType1": "operating",
      "marginType2": "operating"
    },
    "expect": [
      "目标营业成本： 6.72 元 对应毛利率： 84.00%\n42\noperating\n42\n42\n目标营业利润率： 42% 单位成本：42.00 元 假设期间费用率：25% 目标售价： 127.27 元 对应毛利率： 67.00%\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"revenue\":\"42\",\"cogs\":\"42\",\"sellingExp\":\"42\",\"adminExp\":\"42\",\"rdExp\":\"42\",\"finExp\":\"42\",\"da\":\"42\",\"taxRate\":\"42\",\"revRev\":\"42\",\"targetMargin1\":\"42\",\"expRatio1\":\"42\",\"costCost\":\"42\",\"targetMargin2\":\"42\",\"taxRate2\":\"42\",\"batchStart\":\"42\",\"batchEnd\":\"42\",\"batchStep\":\"42\",\"batchM1\":\"42\",\"batchM2\":\"42\",\"batchM3\":\"42\",\"batchM4\":\"42\",\"dupontNI\":\"42\",\"dupontRev\":\"42\",\"dupontAssets\":\"42\",\"dupontEquity\":\"42\",\"marginType1\":\"operating\",\"marginType2\":\"operating\"}，输出区含「目标营业成本： 6.72 元 对应毛利率： 84.00%\n42\noperatin…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/sharpe-ratio",
    "inputs": {
      "portReturn": "42",
      "portStd": "42",
      "riskFree": "42",
      "returns": "1\n2\n3",
      "annualize": "12"
    },
    "expect": [
      "每期无风险利率 = 42.00% ÷ 12 = 3.500%",
      "每期夏普比率 = -1.500 ÷ 0.816 = -1.8371",
      "年化夏普 = -1.8371 × √12 = -6.3640",
      "评级（按年化夏普）： 差"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"portReturn\":\"42\",\"portStd\":\"42\",\"riskFree\":\"42\",\"returns\":\"1\\n2\\n3\",\"annualize\":\"12\"}，序列均值 2、总体标准差 0.816；年化无风险利率 42% 折算到每期 3.500%，超额收益 = 2 − 3.5 = −1.500%，每期夏普 = −1.8371、年化 = −6.3640，只给一个评级「差」。默认态（输入回退）不含这些串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/sin-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n❌ SIN 只能包含数字、空格或连字符"
    ],
    "ref": "F-N209 同步：含字母/中文的非法字符输入修复后走「只能包含数字、空格或连字符」拒绝（旧实现剥离字母按 3 位报错）；默认态（130692544）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/salary-calculator",
    "inputs": {
      "salary": "42",
      "bonus": "42",
      "baseSalary": "42",
      "housingBase": "42",
      "pensionRate": "42",
      "medicalRate": "42",
      "unemploymentRate": "42",
      "injuryRate": "42",
      "maternityRate": "42",
      "housingRate": "42",
      "childrenEdu": "42",
      "continuingEdu": "42",
      "housingLoan": "42",
      "housingRent": "42",
      "elderly": "42",
      "infant": "42",
      "threshold": "42",
      "monthsPerYear": "42"
    },
    "clicks": ["calculate()"],
    "expect": [
      "⚠ 五险一金缴费基数 ¥42.00/月 高于税前工资 ¥1.00/月"
    ],
    "ref": "第124批 F-N98/F-N100 契约同步（用例过期，非页面 bug）：18 项 42 注入、计薪月数 42 时旧版输出年应税额与 ¥-4,361.28 负收入，旧 expect 超长串把该缺陷固化成契约。修复后按业务状态拒绝，提示含当前基数 42.00 与折算月薪 1.00（42÷42）。显式 clicks=calculate() 保证动态结果区被 harness 采集（无 clicks 时新形态不进 blob）。互斥说明行仍由用例 #3/#4 锁定，本例只锚转换后的拒绝态；默认态（20,000.00 / 1,666.67）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/sort-code-validator-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： abc123测试 ❌ Sort Code 仅允许数字、空格或连字符，含字母为格式错误"
    ],
    "ref": "F-N197 同步：含字母/中文输入修复后走「含字母为格式错误」拒绝（旧实现剥离字母按 3 位报错）；默认态（200000）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/swift-bic-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： ABC123测试 长度： 8 字符（8 或 11） ❌ 仅允许字母、数字及空格/连字符分隔"
    ],
    "ref": "第119批 F-N146 契约同步：注入 abc123测试 时新版先做字符白名单校验，明确拒绝非法字符（旧版误报「前 4 位必须为字母」）；旧源码不含「仅允许字母、数字及空格/连字符分隔」⇒ 强判别、零逃生。默认态不含该串。"
  },
  {
    "slug": "finance/simple-interest",
    "inputs": {
      "principal": "42",
      "rate": "42",
      "years": "42",
      "mode": "annual"
    },
    "expect": [
      " 年末：累计利息 229.32 元，本利和 271.32 元 第 14 年末：累计利息 246.96 元，本利和 288.96 元 第 15 年末：累计利息 264.6 元，本利和 306.6 元 第 16 年末：累计利息 282.24 元"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"principal\":\"42\",\"rate\":\"42\",\"years\":\"42\",\"mode\":\"annual\"}，输出区含「 年末：累计利息 229.32 元，本利和 271.32 元 第 14 年末：累…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/stock-profit-calculator",
    "inputs": {
      "buyPrice": "42",
      "buyQty": "42",
      "sellPrice": "42",
      "commissionRate": "42",
      "stampRate": "42",
      "transferRate": "42",
      "minCommission": "42"
    },
    "expect": [
      "佣金、印花税与过户费合计不能达到 100%。"
    ],
    "ref": "自动补强（B类零用例，已按费率上限修正）：全量注入 42 使佣金 42% + 印花税 42% + 过户费 42% = 126%（≥100%）⇒ 卖出净额会变负，现拦截提示；默认 0.03%/0.05%/0.001% 不含该提示 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/tax-bracket",
    "inputs": {
      "income": "42"
    },
    "expect": [
      "应缴税款： 1.26 元 应纳税所得额减本次估算税额： 40.74 元 这不是到手工资：应纳税所得额已由收入减去扣除得出，本页也未再扣五险一金与专项附加；需要税后工资请到「个税计算器」填写完整收入与扣除，避免重复扣减。 实际税率： 3.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"income\":\"42\"}，输出区含「 元 应缴税款： 1.26 元 应纳税所得额减本次估算税额： 40.74 元 实际税率： 3.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。标签由「税后所得」改为「税后余额」，避免把应纳税所得额的税后余额误当到手工资。"
  },
  {
    "slug": "finance/tax-calculator",
    "inputs": {
      "salary": "42",
      "insurance": "42",
      "special": "42",
      "threshold": "42",
      "bonus": "42000"
    },
    "expect": [
      "¥3,990.00",
      "¥1,680.00",
      "全年少缴 ¥2,310.00"
    ],
    "ref": "年终奖双口径对比（2026-10-25 新增功能同步）：月薪四键取 42 ⇒ 月度与年度应纳税所得额均为 0，奖金 42000 单独计税=42000÷12=3500 落月度第2级(10%/扣210) ⇒ 42000×10%−210=3990；并入综合所得走年度表第2级(10%/扣2520) ⇒ 42000×10%−2520=1680。两口径差 2310，页面须给出「并入综合所得…全年少缴 ¥2,310.00」。三个串分别绑定单独税额、并入税额与差额结论：任一档位/速算扣除数/年度表口径回归，或新增 bonus 输入被移除，本例即变红；默认态(奖金30000、两口径同为900)不含这些串 ⇒ 零逃生"
  },
  {
    "slug": "finance/text-reverse-words",
    "inputs": {
      "input": "1\n2\n3",
      "mode": "zhchar"
    },
    "expect": [
      "1 2 3\n3 2 1\nzhchar"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"1\\n2\\n3\",\"mode\":\"zhchar\"}，输出区含「1 2 3\n3 2 1\nzhchar」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/tin-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： abc123测试 ❌ 含非法字符：号码只能包含数字、连字符与空格"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： abc123测试 ❌ 含非法字符…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/tfn-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "输入： abc123测试 ❌ 含非法字符：仅允许数字、空格或连字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输入安全回显且非法字符须被明确拒绝。"
  },
  {
    "slug": "finance/uan-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： abc123测试 ❌ 第 1 位含非法字符「a」"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，F-N148 修复后含字母在第 1 位报错「非法字符「a」」（旧实现静默剔除 abc/测试 后按 3 位报长度错）；输出区绑定输入串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/vcard-qr",
    "inputs": {
      "fn": "abc123测试",
      "ln": "abc123测试",
      "tel": "abc123测试",
      "email": "abc123测试",
      "org": "abc123测试",
      "title": "abc123测试",
      "url": "abc123测试"
    },
    "expect": [
      "ON:3.0 N:abc123测试;abc123测试;;; FN:abc123测试abc123测试 ORG:abc123测试 TITLE:abc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fn\":\"abc123测试\",\"ln\":\"abc123测试\",\"tel\":\"abc123测试\",\"email\":\"abc123测试\",\"org\":\"abc123测试\",\"title\":\"abc123测试\",\"url\":\"abc123测试\"}，输出区含「ON:3.0 N:abc123测试;abc123测试;;; FN:abc123测…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/vat-calculator",
    "inputs": {
      "customRate": "42",
      "amount": "42",
      "batchRate": "42",
      "batchInput": "1\n2\n3",
      "dir": "exclusive",
      "batchDir": "exclusive"
    },
    "expect": [
      "增值税额（按输入税率） 含税价 1 1.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"customRate\":\"42\",\"amount\":\"42\",\"batchRate\":\"42\",\"batchInput\":\"1\\n2\\n3\",\"dir\":\"exclusive\",\"batchDir\":\"exclusive\"}，输出区含「额 含税价 1 1.00 1.00 0.42 1.42 2 2.00 2.00 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/word-frequency",
    "inputs": {
      "topN": "42",
      "minLen": "42",
      "input": "1\n2\n3",
      "ignoreCase": "0"
    },
    "expect": [
      "1 2 3\n没有符合条件的词\n0\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"topN\":\"42\",\"minLen\":\"42\",\"input\":\"1\\n2\\n3\",\"ignoreCase\":\"0\"}，输出区含「1 2 3\n没有符合条件的词\n0\n42\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/voter-id-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入（已脱敏）： AB••••测试 长度： 8 字符（应为 10） ❌ 长度必须为 10 字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入（已脱敏）： AB••••测试 长度： 8 字符（应为 10） ❌ …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/word-wrap",
    "inputs": {
      "width": "42",
      "input": "1\n2\n3",
      "mode": "word"
    },
    "expect": [
      "1 2 3\n1 2 3\n42\nword"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"width\":\"42\",\"input\":\"1\\n2\\n3\",\"mode\":\"word\"}，输出区含「1 2 3\n1 2 3\n42\nword」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/zip-code-validator",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n输入： abc123测试 ❌ 格式不符。ZIP 应为 5 位数字或 5 位-4 位格式"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n输入： abc123测试 ❌ 格式不符。ZIP 应为 5 位数…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/loan-amortization",
    "inputs": {
      "loanAmount": "42",
      "annualRate": "42",
      "loanYears": "42",
      "balloonMonths": "42",
      "balloonRatio": "42",
      "prepayMonth": "42",
      "prepayAmount": "42",
      "repayMethod": "principal"
    },
    "clicks": ["calc();var ok=document.getElementById('loanAmount').value==='42'&&document.getElementById('scheduleTable').innerHTML.indexOf('1.55')>=0;document.getElementById('__tbProbe').textContent='LOANAUTO '+(ok?'OK':'BAD');"],
    "expect": [
      "LOANAUTO OK"
    ],
    "ref": "注入 42 元 / 42% / 42 年 / 等额本金：首月月供 = 42/504 + 42×42%/12 = 1.55 元；默认参数月供量级为数千元，不含 1.55 ⇒ 注入失败必红。"
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "12", housePrice: "450", age: "40" },
    expect: ["账户余额12.0万元 × 15倍", "总价450.0万元 × 80%"],
    ref: "注入非默认(默认 8/2000/5/300/35)：额度三档 —— 余额档 = 12.0万×15 = 180.0 万、房价档 = 450.0万×80% = 360.0 万、城市上限（北京）120 万 ⇒ 最终可贷取最小 120 万。⚠ **月供 21,616 元与还款总额 1,296,948 元不可用**：默认 balance=8 时 8×15 = 120 万，同样被 120 万城市上限夹住 ⇒ 额度、月供、利息、还款总额在两态**逐字相同**；唯一有判别力的是额度依据表里含注入值的两行说明串。"
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "12", housePrice: "450", age: "40", rate: "4.5" },
    expect: ["4.59%"],
    ref: "年利率 4.5%（名义）⇒ 有效年化 = (1+4.5%/12)^12−1 = **4.59%**，与名义值并列；默认 2.85% ⇒ 2.89%，不命中。"
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "12", housePrice: "450", age: "40", rate: "99" },
    expect: ["贷款年利率须填写 0–20%"],
    ref: "年利率 99% 超出 0–20% 有效区间：旧实现静默回退 2.85% 不告知；现显式标注「输入无效已按 2.85% 计」。默认 2.85% 且有效 ⇒ 不命中。"
  },
  {
    slug: "finance/housing-fund-loan",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/housing-fund-loan.html','utf8');var ok=h.indexOf('基于现行法律法规计算')<0&&h.indexOf('非官方实时政策')>=0&&h.indexOf('以当地公积金中心审批为准')>=0;document.getElementById('__tbProbe').textContent='HFDESC '+(ok?'OK':'BAD');"],
    expect: ["HFDESC OK"],
    ref: "第1384批·示例参数不得表述为现行法规：meta/OG/Twitter/JSON-LD/正文均不再出现「基于现行法律法规计算」，明确 2026-11 示例、非官方实时政策、以当地公积金中心审批为准。"
  },

  {
    "slug": "finance/loan-amortization",
    "inputs": {
      "loanAmount": "120000",
      "annualRate": "6",
      "loanYears": "2",
      "repayMethod": "equal"
    },
    "expect": [
      "第1年 63,821.68 58,205.02 5,616.66 61,794.98",
      "第2年 63,821.68 61,794.98 2,026.70 0.00"
    ],
    "ref": "逐年表：月供 5,318.47（120000×0.005×1.005^24/0.12716），年还款 12×5,318.47=63,821.68；第1年本金 120000−61794.98=58,205.02、利息 63821.68−58205.02=5,616.66；第2年本金恰为第1年末余额 61,794.98、期末清零 0.00 —— 行间自洽。默认态（50万/4.9%/30年）逐年值均不同 ⇒ 零交集。"
  },

  // ---- F-N9/F-N10：复利年限上限/负定投、分期费率校验/IRR 残差（2026-11-03） ----
  {
    slug: "finance/compound-interest",
    inputs: { principal: "10000", rate: "0", years: "2000", annual: "0" },
    clicks: ["calc()"],
    expect: ["已按 1000 年上限计算（实际使用 1000 年）"],
    ref: "F-N9：年限 2000 年超过 1000 年上限，结果区必须明示「已按 1000 年上限计算（实际使用 1000 年）」；旧实现静默按 1000 年算且不回显。默认态（20 年）不含该提示 ⇒ 注入失败即失配。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "10000", rate: "5", years: "10", annual: "-1000" },
    clicks: ["calc()"],
    expect: ["定投金额不能为负数"],
    ref: "F-N9：定投金额 -1000 为负，必须触发字段级错误并停止计算（旧实现把它当年金投入，逐年扣减余额却仍标「定投」）。默认态 annual=12000 ⇒ 不出现该错误 ⇒ 判别力成立。",
  },
  {
    slug: "finance/installment-real-rate",
    inputs: { P: "12000", n: "12", r: "-0.5" },
    clicks: ["calcTool()"],
    expect: ["每期手续费率不能为负数"],
    ref: "F-N10：每期手续费率 -0.5% 为负，必须单独报错并停止求解（旧实现只校验本金/期数，负费率会算出看似可信的年化）。默认态 r=0.6 ⇒ 不命中。",
  },
  {
    slug: "finance/installment-real-rate",
    inputs: { P: "12000", n: "12", r: "100" },
    clicks: ["calcTool()"],
    expect: ["真实月利率超出求解区间上限 100%", "PV 残差 996.83 元"],
    ref: "F-N10：本金 12000、12 期、每期费率 100% ⇒ 每期还款 13000；PV(月利率 100%) = 13000×(1−2^-12) = 12996.826171875，比本金多 996.826171875 ⇒ 真实根越出 [0,1] 区间，页面须提示「超出求解区间上限 100%」并给出 PV 残差 996.83 元。默认态 r=0.6 求解正常 ⇒ 不命中。",
  },
  {
    slug: "finance/installment-real-rate",
    inputs: { P: "24000", n: "24", r: "1.2" },
    clicks: ["calcTool()"],
    expect: ["第 0 期 +24,000.00（收到分期本金）", "第 1–24 期 −1,288.00（支付还款）"],
    ref: "F-N10：现金流方向展示（便于核对 IRR 符号约定）——期初收到本金 24,000.00，此后 24 期每期支付 1,000.00（本金）+288.00（手续费）=1,288.00，方向分别为 +/−。默认态（12,000 / 12 期 / 0.6%）为 +12,000.00 与 −1,072.00 ⇒ 不命中。",
  },
  {
    slug: "finance/installment-real-rate",
    inputs: { P: "24000", n: "24", r: "1.2" },
    clicks: ["calcTool()"],
    expect: ["28.81%"],
    ref: "24,000 元分 24 期、每期费率 1.2% ⇒ 真实月利率约 2.124%，有效年化 (1+i)^12−1 = **28.81%**（单利近似 ×12 仅约 25.49%）。默认（12,000 / 12 期 / 0.6%）有效年化约 14.5% ⇒ 不命中。",
  },
  {
    slug: "finance/installment-real-rate",
    inputs: { P: "12000", n: "12.5", r: "0.6" },
    clicks: ["calcTool()"],
    expect: ["分期期数须为正整数"],
    ref: "期数 12.5：旧实现 Math.floor 静默截成 12 期照算；现直接拒绝并提示不按小数折算。默认 12 期 ⇒ 不命中。",
  },
  {
    slug: "finance/loan-comparison",
    inputs: {"a-principal":"0","a-rate":"5","a-months":"12","b-principal":"50000","b-rate":"4.8","b-months":"24","c-principal":"80000","c-rate":"4.6","c-months":"36"},
    expect: ["⚠ 无效方案：贷款金额须大于 0 且不超过 1 万亿元，已排除比较", "月供最低： B 方案"],
    ref: "F-N1：方案 A 本金 0 ⇒ 月供恒 0，必须标记无效并排除比较；仅 B、C 参与，B 月供 2189.09 最低；本金/期数不同须提示不可仅按月供判优。默认三方案本金 100000、均有效 ⇒ 不命中无效提示。",
  },
  {
    slug: "finance/loan-comparison",
    inputs: {"a-principal":"0","a-rate":"5","a-months":"12","b-principal":"0","b-rate":"4.8","b-months":"0","c-principal":"0","c-rate":"4.6","c-months":"0"},
    expect: ["⚠ 没有有效方案：请至少填写一组贷款金额与月数后再比较。"],
    ref: "F-N1：三方案全部本金/期数为 0 ⇒ 全部无效，不得显示「月供最少」推荐，只给出无有效方案提示。默认三方案均有效 ⇒ 不命中。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: {"monthly":"1000","years":"1","rate":"12","initial":"12000","target":"0"},
    clicks: ["switchTiming('begin')","calc()"],
    expect: ["累计收益： +¥2,204.40", "年化收益率（资金加权）： 12.00%", "有效年化 12.68%"],
    ref: "F-N5：初始本金 12000 发生在 t=0、12 期定投按期初时点落位求 IRR ⇒ 名义 12.00%/有效 12.68%；旧口径把初始本金均摊到每月，资金加权年化虚高（约 17%）。默认 monthly 1000/10 年/8% ⇒ 不命中。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: {"monthly":"1000","years":"1","rate":"-12","initial":"12000","target":"0"},
    expect: ["累计收益： -¥2,001.87", "累计收益率： -8.34%", "年化收益率（资金加权）： -12.00%"],
    ref: "F-N6：年化 −12%、初始 12000、月投 1000、1 年 ⇒ 期末 21998.13，累计亏损 2001.87，必须带负号显示 -¥2,001.87 / -8.34%，IRR 名义 -12.00%。默认 8% 正收益 ⇒ 不命中。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: {"monthly":"1000","years":"1","rate":"5","initial":"0","target":"1000000000"},
    expect: ["目标超出可反推范围（年化 −99%～500%）", "无法反推所需收益率"],
    ref: "F-N6：月投 1000、1 年、目标 10 亿远超 500% 年化上限（期末约 15.44 万）⇒ 不得静默返回 500%，须提示目标超出可反推范围。默认目标 200000 有解 ⇒ 不命中。",
  },
  {
    slug: "finance/retirement-calculator",
    inputs: {"age":"30","retireAge":"60","lifeAge":"85","currentSavings":"0","monthlyContribution":"500","returnRate":"0","inflation":"0","monthlyExpense":"2000"},
    expect: ["18.00万 退休时资产（名义）", "600.00 退休后月支取（实际）"],
    ref: "F-N7：年化 0% 时定投 500×12×30 年 = 18.00 万，退休后按 4% 法则月支取 600.00；旧代码年金公式除以 r=0 产生 NaN。默认 6% ⇒ 不命中。",
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: {"pv":"100000","downPct":"0","rate":"6","months":"36","fv":"0","fee":"5000","type":"equal","timing":"begin"},
    expect: ["还款方式： 等额本息 · 期初还款", "名义年化（月 IRR × 12）： 10.03%"],
    ref: "期初还款首期落在 t=0、手续费 5000 计入 t=0 现金流（净融资 95,000）；按页面实际摊销表独立复算：t=0 现金流 −91,972.94、月利率 0.8358% ⇒ 名义年化 10.03%。旧口径把首期折现到 t=1 且漏算手续费，得约 5.67%。默认 fee=0、期末还款 ⇒ 不命中。",
  },
  {
    slug: "finance/vat-calculator",
    inputs: { amount: "1000", customRate: "-50" },
    expect: ["税率须为 0–100 之间的数字"],
    ref: "F-N20：自定义税率 -50 越界（旧实现 onCustomRate 让 currentRate=-50 直接参与计算，含税价倒推得到负数税额），必须字段级拒绝、不输出结果；默认税率 13% ⇒ 不命中。",
  },
  {
    slug: "finance/vat-calculator",
    inputs: { amount: "1000", customRate: "150" },
    expect: ["税率须为 0–100 之间的数字"],
    ref: "F-N20：自定义税率 150 越界（旧实现按 150% 计算，不含税 = 1000/2.5 = 400），必须字段级拒绝；默认 13% ⇒ 不命中。",
  },
  {
    slug: "finance/vat-calculator",
    inputs: { batchInput: "1000\nabc\n5000", batchRate: "13" },
    expect: ["已忽略 1 行", "5,309.73"],
    ref: "F-N20：批量 3 行中 `abc` 非数字必须跳过并提示已忽略 1 行；有效行 1000/5000 按含税价倒推，不含税合计 = 1000/1.13 + 5000/1.13 = 5,309.73（旧实现把 abc 当 0 并纳入行号，不出现忽略提示）。默认批量 1000/2500/5000 ⇒ 合计 7,522.12，不命中 5,309.73。",
  },
  {
    slug: "finance/simple-interest",
    inputs: { principal: "20000", rate: "5", years: "3", mode: "annual" },
    expect: ["每年取息现金流", "第 3 年末 1,000 3,000", "合计 3,000 3,000"],
    ref: "F-N21：每年取息 = 20000×5% = 1,000/年，第 3 年末累计 3,000，合计行 3,000；总利息与到期一次性（20000×5%×3=3,000）相同，差别仅在时点。默认 mode=simple ⇒ 不渲染现金流表，不命中。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "12000", annualRate: "0", loanYears: "1", repayMethod: "equal" },
    expect: ["1,000.00 首月月供", "0.00 总利息", "12,000.00 总还款额"],
    ref: "F-N24：r=0 时等额本息月供应退化为 本金/期数 = 12000/12 = 1,000.00，利息恒 0，总还款 12,000.00（旧实现守卫直接拦截 r=0，且 0/0 公式得 NaN）。默认 100 万/4.2%/30 年 ⇒ 不命中。",
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "400000", rate: "6", months: "240", monthly: "3500", prepay: "40000", precision: "101" },
    expect: ["已回退为默认 2 位", "3,500.00"],
    ref: "F-N28：precision=101 超出 0–6，旧实现 (x).toFixed(101) 抛 RangeError；修复后回退默认 2 位并提示。月供 3500 按 2 位渲染为 3,500.00。默认 precision=2、monthly=3000 ⇒ 无回退提示且不含 3,500.00，不命中。",
  },
  {
    slug: "finance/provident-fund",
    inputs: { salary: "15000", selfPct: "12", empPct: "12", months: "60", loanRate: "3.1", loanYears: "0" },
    clicks: ["calc()"],
    expect: ["贷款年限须为 1–30 之间的整数。", "⚠ 贷款参数无效：请先修正标红的字段。"],
    ref: "F-N38：贷款年限 0 ⇒ 旧实现 loanMonths=0、分母 1−(1+r)^0=0，月供 Infinity、总还款 NaN 被格式化成「—」。修复后字段级报错并停止计算。默认 30 年 ⇒ 不命中。",
  },
  {
    slug: "finance/provident-fund",
    inputs: { salary: "15000", selfPct: "12", empPct: "12", months: "60", loanRate: "-3.1", loanYears: "30" },
    clicks: ["calc()"],
    expect: ["贷款利率须为 0–10% 之间的数字。", "⚠ 贷款参数无效：请先修正标红的字段。"],
    ref: "F-N38：利率 −3.1% ⇒ 旧实现 monthlyRate>0 为假，月供 0 却输出总利息 −489,999.99。修复后拒绝负利率。默认 3.1% ⇒ 不命中。",
  },
  {
    slug: "finance/discount-calculator",
    inputs: { finalPrice: "80", discountRate: "12" },
    clicks: ["setMode(1)"],
    expect: ["折扣须为大于 0 且不超过 10 折（如 8 表示 8 折）；0 折时原价无法唯一确定。"],
    ref: "F-N48：反向模式折扣率 12 超出「几折」口径 0–10 ⇒ 旧实现得原价 66.67、节省 −13.33；修复后字段级拒绝。默认折扣率 8 ⇒ 不命中。",
  },
  {
    slug: "finance/discount-calculator",
    inputs: { finalPrice: "80", discountRate: "-8" },
    clicks: ["setMode(1)"],
    expect: ["折扣须为大于 0 且不超过 10 折（如 8 表示 8 折）；0 折时原价无法唯一确定。"],
    ref: "F-N48：折扣率 −8 ⇒ 旧实现直接除得负原价 −100.00、节省 −180.00；修复后拒绝负折扣。默认 8 ⇒ 不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { revRev: "1000", targetMargin1: "120" },
    clicks: ["calcReverse()"],
    expect: ["目标利润率与期间费用占比须在 0–100% 之间"],
    ref: "F-N56 收入侧同源缺陷：目标毛利率 120% ⇒ 旧实现 targetCost = 1000×(1−1.2) 得 −200.00（负成本）；现拦截。默认目标毛利率 30% ⇒ 不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { costCost: "60", targetMargin2: "120" },
    clicks: ["calcReverse()"],
    expect: ["目标利润率须在 0%–100% 之间（不含 100%）。"],
    ref: "F-N56：单位成本 60、目标毛利率 120% ⇒ 旧实现 cost/(1−1.2) 得目标售价 −300.00；修复后字段级报错。默认 40% ⇒ 不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { costCost: "60", targetMargin2: "100" },
    clicks: ["calcReverse()"],
    expect: ["目标利润率须在 0%–100% 之间（不含 100%）。"],
    ref: "F-N56：目标毛利率 100% ⇒ 旧实现除零得 Infinity 并被格式化为「—」；修复后明确拒绝 100%。默认 40% ⇒ 不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { batchStart: "0", batchEnd: "0", batchStep: "10", batchM1: "0" },
    clicks: ["calcBatch()"],
    expect: ["0.00"],
    ref: "第934批：成本 0、毛利率 0% 都保留为有效值，不再回退 10/20%；表格输出成本 0.00。默认 10–100/20% ⇒ 不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { batchStart: "0", batchEnd: "100", batchStep: "0.001" },
    clicks: ["calcBatch()"],
    expect: ["当前范围将生成 100001 行，超过 500 行上限"],
    ref: "第934批：极小步长生成前行数预检，超过 500 行直接拒绝，避免海量循环/DOM。默认 21 行 ⇒ 不命中。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { batchM1: "120" },
    clicks: ["calcBatch()"],
    expect: ["毛利率1须在 0%–100% 之间（当前 120%）"],
    ref: "F-N56/第934批：批量毛利率 120% 超出 0–100%，修复后明确拒绝并提示区间，不再输出负价格或「不可达」。默认四档 20/30/40/50% ⇒ 不命中。",
  },
  {
    slug: "banking/apy-calculator",
    inputs: { r: "0.05", n: "0" },
    clicks: ["calcTool()"],
    expect: ["⚠ 年复利次数 n 必须为正整数（如 12 表示每月复利）。"],
    ref: "F-N14：n=0 ⇒ 旧实现 pow(Infinity,0)=1，APY 显示 0.000%；修复后拒绝非正整数。默认 n=12 ⇒ 不命中。",
  },
  {
    slug: "banking/apy-calculator",
    inputs: { r: "0.05", n: "-12" },
    clicks: ["calcTool()"],
    expect: ["⚠ 年复利次数 n 必须为正整数（如 12 表示每月复利）。"],
    ref: "F-N14：n=−12 ⇒ 旧实现 pow(1−0.00417,−12) 得 5.1381% 的伪结果；修复后拒绝负次数。默认 n=12 ⇒ 不命中。",
  },
  {
    slug: "banking/apy-calculator",
    inputs: { r: "5", n: "12" },
    clicks: ["calcTool()"],
    expect: ["若想表达 5%，请填写 0.05"],
    ref: "F-N14：r 为小数口径，输入 5（想表达 5%）⇒ 旧实现按 500% 得 6434.50%；修复后提示换算口径。默认 r=0.05 ⇒ 不命中。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { rate: "-150", init: "10000" },
    expect: ["折现率须高于 -100%（等于或低于 -100% 时无法折现）。"],
    ref: "F-N31：折现率 −150% ⇒ 旧实现 1+r<0 使幂运算符号交替，NPV 虚增为 20,000、PI 3.000 且仍标「可行」；修复后字段级拒绝。默认 8% ⇒ 不命中。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { rate: "-100", init: "10000" },
    expect: ["折现率须高于 -100%（等于或低于 -100% 时无法折现）。"],
    ref: "F-N31：折现率 −100% ⇒ 旧实现 1+r=0 使 NPV 为 Infinity、被格式化成「—」，可行性仍判「可行」；修复后拒绝边界值。默认 8% ⇒ 不命中。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { rate: "8", init: "10000" },
    clicks: ["cashFlows=[-1000,-1000];calc();"],
    expect: ["范围内未找到"],
    ref: "F-N29 核销（2026-11-16）：现金流全为流出（−1000/−1000）时 NPV 恒负、无 IRR。旧实现固定二分到上限 1000% 并判「可行」；现 calcIRR 返回 {status:'none', reason:'no-positive'}，结果卡显示「范围内未找到」，不再给可行结论。默认现金流含正值 ⇒ 正常 IRR，不命中该文案。"
  },
  {
    slug: "finance/investment-roi",
    inputs: { aCost: "1000", aRate: "10", aYears: "5", aAdd: "0", bCost: "5000", bRate: "3", bYears: "5", bAdd: "0" },
    clicks: ["switchTab('compare')", "calcCompare()"],
    expect: ["方案A 更优方案（按资金加权年化 IRR 判优）"],
    ref: "F-N34：A 1,000 元 @10%/5 年 → 终值 1,610.51、资金加权年化 10.00%；B 5,000 元 @3%/5 年 → 终值 5,796.37、年化 3.00%。旧实现按终值判 B 更优（投入更多者占优），上一版改按「累计 ROI 开方」判 A；第 127 批改为按各期实际投入时点反解 IRR 判优，卡片标签同步改为「按资金加权年化 IRR 判优」（属测试契约同步，非页面回归）。默认两方案 10,000 元 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { aCost: "10000", aRate: "8", aYears: "5", aAdd: "-1000", bCost: "10000", bRate: "12", bYears: "5", bAdd: "0" },
    clicks: ["switchTab('compare')", "calcCompare()"],
    expect: ["每年追加须 ≥ 0；如需从本金中取出，请按真实现金流另行计算。"],
    ref: "F-N34：A 追加 −1,000 ⇒ 旧实现按 p.add > 0 判断后直接跳过，静默当作 0 追加并放大投入基数；修复后字段级报错。默认追加 0 ⇒ 不命中。",
  },
  {
    slug: "finance/futures-pnl-calculator",
    inputs: { lots: "0" },
    expect: ["手数须为不小于 1 的整数。"],
    ref: "F-N47：手数 0 ⇒ 旧实现 parseInt(0) || 1 静默按 1 手计算，给出完整净盈亏；修复后字段级拒绝非正手数。默认 1 手 ⇒ 不命中。",
  },
  {
    slug: "finance/futures-pnl-calculator",
    inputs: { marginRate: "0" },
    expect: ["保证金比例须在 0%–100% 之间（不含 0%）。"],
    ref: "F-N47：保证金比例 0 ⇒ 旧实现保证金为 0、保证金收益率显示 +0.00%，与大额盈亏自相矛盾；修复后字段级拒绝。默认 12% ⇒ 不命中。",
  },
  {
    slug: "finance/futures-pnl-calculator",
    inputs: { lots: "0" },
    clicks: ["copyResult()"],
    expect: ["输入有误，无法复制结果"],
    ref: "F-N47 复制绕过校验：手数 0 时 calc() 显示字段错误，但旧 copyResult() 仍按 ||1 兜底生成并复制完整盈亏；修复后 copyResult() 先走 validateInputs() 并拒绝复制。默认态复制正常 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-calculator",
    inputs: { initial: "10000", final: "8000", years: "5", additional: "-5000" },
    expect: ["追加投入须 ≥ 0；如需从本金中取出，请按真实现金流另行计算。"],
    ref: "F-N46：初始 10,000、期末 8,000、追加 −5,000 ⇒ 旧实现 totalInv=5,000、累计盈亏 +3,000、回报率 +60.00%、CAGR +9.86%，把真实亏损包装成高收益；修复后字段级拒绝负追加。默认追加 0 ⇒ 不命中。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: { initial: "10000", monthly: "1000", years: "1", rate: "-50" },
    expect: ["-¥6,682 总收益"],
    ref: "F-N44：初始 10,000、月投 1,000、1 年、年化 −50%，月末买入 ⇒ 总收益 −6,682.30；亏损卡片须显示负号。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: { initial: "10000", monthly: "1000", years: "1", rate: "-50" },
    expect: [" -30.37% 累计收益率"],
    ref: "F-N44：月末买入时累计收益率为 −30.37%，只应有一个负号；前导空格防止误匹配双负号。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: { initial: "10000", monthly: "1000", years: "1", rate: "-50" },
    expect: ["-¥6,682.30"],
    ref: "F-N44：月末买入后明细按两位小数展示亏损 −¥6,682.30，不得丢失负号。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "10000", salvage: "1000", life: "5", totalUnits: "10000", yearUnits: "3000,0,0,0,0" },
    clicks: ["calc()"],
    expect: ["2,700 工作量法首年"],
    ref: "F-N53：可折旧总额 9,000 / 总工作量 10,000 ⇒ 0.9 元/单位，首年 3,000 工作量 ⇒ 2,700；旧实现把总工作量按年限均摊，工作量法恒等于直线法 1,800。默认 100,000/10,000 ⇒ 不命中。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "10000", salvage: "1000", life: "5", totalUnits: "10000", yearUnits: "20000,0,0,0,0" },
    clicks: ["calc()"],
    expect: ["9,000 工作量法首年"],
    ref: "F-N53：首年工作量 20,000 超出总工作量 ⇒ 按可折旧总额封顶 9,000，期末余额保留下限 1,000；旧实现无封顶且按均摊得 1,800。默认 100,000/10,000 ⇒ 不命中。",
  },
  {
    slug: "finance/stock-profit-calculator",
    inputs: { buyPrice: "-10", buyQty: "1000", sellPrice: "11" },
    clicks: ["calc()"],
    expect: ["买入价须大于 0。"],
    ref: "F-N57：买入价 −10、1,000 股、卖出 11 ⇒ 旧实现买入成本 −9,995.10、盈亏 +20,984.49 而百分比 +0.00%；修复后字段级报错并清空结果。默认 10.00 ⇒ 不命中。",
  },
  {
    slug: "finance/stock-profit-calculator",
    inputs: { buyPrice: "10", buyQty: "0", sellPrice: "11" },
    clicks: ["calc()"],
    expect: ["买入数量须为正整数。"],
    ref: "F-N57：数量清空 ⇒ 旧实现只按最低佣金 5 元计成本、盈亏 −5.00/−100.00%；修复后拒绝非正数量并禁用复制/导出。默认 1,000 股 ⇒ 不命中。",
  },
  {
    slug: "finance/stock-profit-calculator",
    inputs: { buyPrice: "10", buyQty: "1000", sellPrice: "11", commissionRate: "-5" },
    clicks: ["calc()"],
    expect: ["费率须在 0–100% 之间，最低佣金不能为负。"],
    ref: "负佣金率原实现把手续费算成负数 ⇒ 盈亏被抬高、复制/导出带出与直觉相反的数值；现拦截。默认 0.03% ⇒ 不命中。",
  },

  {
    slug: "finance/tfn-validator",
    inputs: { input: "100000001" },
    expect: ["格式化： 100 000 001 长度： 9 位"],
    ref: "澳洲 TFN 9 位 100000001：1×1 + 1×10 = 11，11 mod 11 = 0 ⇒ 合法；旧权重末位 11 得 1 + 11 = 12 会被误拒。"
       + "锚点刻意改为「格式化后的分组串」——原锚「✅ TFN 号码有效」在默认值 876543210 下同样成立（该默认值本身也是合法 TFN），"
       + "属逃生项；分组串只在注入值命中，默认态为「格式化： 876 543 210」故不重合。",
  },
  {
    slug: "finance/tfn-validator",
    inputs: { input: "12345678" },
    expect: ["格式化： 012 345 678 长度： 8 位"],
    ref: "F-N196 8 位 TFN 分组：补前导 0 后按 3-3-3 显示 012 345 678；旧实现 3-3-2 切成 123 456 78（末组仅 2 位）。默认预填 876543210（9 位）⇒ 不命中。",
  },
  {
    slug: "finance/tfn-validator",
    inputs: { input: "100000062" },
    expect: ["格式化： 100 000 062 长度： 9 位 校验算法： 加权模 11（权重 1,4,3,7,5,8,6,9,10） 校验和： ❌ 未通过"],
    ref: "F-N195 权重末位锁定：官方权重 10 时 100000062 加权和 75、余 9 ⇒ ❌；旧权重 11 时和 77、余 0 误判 ✅。默认预填 876543210（合法）⇒ 不命中。",
  },
  {
    slug: "finance/curp-validator",
    inputs: { input: "BOXA100820HMNERNB7" },
    expect: ["出生日期： 100820（2010-8-20）"],
    ref: "CURP 第 17 位为字母 B 表示 2000 年后出生：年份 = 2000 + 10 = 2010，而非旧的 yy<30 启发式。校验位 7 由 mod-10 加权算得。默认态 1931 ⇒ 不命中。",
  },
  {
    slug: "finance/curp-validator",
    inputs: { input: "GARW150820HMNERN58" },
    expect: ["出生日期： 150820（1915-8-20）"],
    ref: "F-N202 数字同音位锁定：第 17 位为 5（数字）⇒ 1900+15=1915；旧 yy<30 启发式会显示 2015。校验位 8 由 mod-10 加权算得。默认态不同 ⇒ 不命中。",
  },
  {
    slug: "finance/curp-validator",
    inputs: { input: "BOXW100820HZZERNA6" },
    expect: ["州代码： ZZ - 未知 ❌ 未分配/非法州码", "❌ CURP 校验失败"],
    ref: "F-N203 州码白名单：ZZ 不在 RENAPO 州码全集，即使日期 2010-08-20 合法且校验位 6 吻合也必须拒绝；旧实现仅展示「未知」并放行。默认态州码有效 ⇒ 不命中。",
  },
  {
    slug: "finance/curp-validator",
    inputs: { input: "BOXW310230HMNERNA4" },
    expect: ["出生日期： 310230（❌ 无效）", "❌ CURP 校验失败"],
    ref: "F-N203 日期按各月天数与闰年校验：1931-02-30 不存在，即便校验位 4 吻合也必须拒绝；防止退回 mm<=12&&dd<=31 粗校验。默认态 1931-08-20 ⇒ 不命中。",
  },
  {
    slug: "finance/curp-validator",
    inputs: { input: "BOXW310820HMNERNA08" },
    expect: ["长度： 19 字符（应为 18） ❌ 格式不符。应为：18 位 = 4 字母 + 6 数字(YYMMDD) + H/M/X + 2 字母(州) + 3 辅音 + 1 字母数字 + 1 校验位"],
    ref: "F-N201 非法长度也要给结论：默认样例已修为 18 位，但旧失败分支只在 raw.length===18 时追加 ❌，19 位输入只回显长度。锁 19 位输入的完整失败串；默认 18 位合法样例不命中。",
  },
  {
    slug: "finance/tin-validator",
    inputs: { input: "000000000" },
    expect: ["❌ 不属于 SSN/ITIN/EIN 任何有效号段"],
    ref: "9 位兜底：Area 000 属 SSN 禁用号段、group 00 不满足 ITIN 70–88、EIN 前缀 00 不在 IRS 分配号段 ⇒ 必须判无效（旧逻辑无条件当 EIN 通过）。",
  },
  {
    slug: "finance/tin-validator",
    inputs: { input: "12-3456789" },
    expect: ["类型： EIN (雇主识别号)", "EIN 格式： 12-3456789"],
    ref: "F-N191 防回归锁：2-7 连字符写法必须按原文判为 EIN（旧实现按 3-2-4 切片报 SSN），并按 2+7 展示；默认 456789012 判 SSN ⇒ 不命中。F-N192 公式框三分支属静态文案，harness 不采集 constRefBox，按源码 diff 核实。",
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "4.5", months: "240", monthly: "500", prepay: "20000", precision: "2" },
    clicks: ["calc()"],
    expect: ["属于负摊还：本金逐期增加"],
    ref: "月供 500 低于当期利息 500000×0.375%=1875，本金逐期增加 ⇒ 复核修复后明确标记「属于负摊还：本金逐期增加」；旧实现循环到 1200 期上限后返回 1200，产生负的伪节省。默认 500000/4.5/240/3000/20000 ⇒ 33 期内还清，不命中。",
  },
  {
    slug: "finance/portfolio-return",
    inputs: { r1: "24", r2: "16", w1: "120", w2: "80" },
    clicks: ["calcTool()"],
    expect: ["权重合计为 200.00%，不是 100%", "剩余 -100.00% 对应的资产与收益未定义"],
    ref: "第933批：120/80 合计 200%，默认拒绝把多余权重当作完整组合；旧实现直接输出 41.60 并只标偏差。默认 60/40 ⇒ 不命中。",
  },
  {
    slug: "finance/portfolio-return",
    inputs: { r1: "24", r2: "16", w1: "120", w2: "80" },
    clicks: ["document.getElementById('normalizeWeights').checked=true;calcTool();"],
    expect: ["归一化组合预期收益 (%)", "已按比例归一化（原合计 200.00%）", "20.80"],
    ref: "第933批：显式勾选归一化后，120/80 按 60%/40% 缩放，rp=0.6×24+0.4×16=20.80，并标注归一化假设；默认 60/40 不命中。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { init: "0", rate: "8" },
    clicks: ["calc()"],
    expect: ["明细与导出已清空"],
    ref: "清空初始投资后旧实现只改统计卡，明细表/图表/导出仍沿用上一次结果；现同步清空并提示。默认初始投资 10000 ⇒ 注入失败不命中。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "8000", dailyRate: "0.1", billDay: "2", dueDay: "20", minRatio: "10", repayType: "minimum" },
    clicks: ["calc()"],
    expect: ["最低还款有效年利率约 42.58%（名义年化 36.50%）"],
    ref: "日利率 0.1%：名义年化 0.1×365=36.50%，按月（30 天）复利的有效年化 (1+0.1%×30)^12−1=42.58%。旧实现只报名义 36.50% 却称「年化」，与页面有效年化卡口径不一致。默认日利率 0.05% ⇒ 注入失败不命中。",
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: {"pv":"100000","downPct":"0","rate":"6","months":"36","fv":"0","fee":"0","type":"equal","timing":"begin"},
    expect: ["8,974"],
    ref: "期初还款（年金先付）：月利率 0.5%、36 期，月供 3,027.06 于每期期初支付，总利息 = 3,027.06×36 − 100,000 = 8,974.16 ⇒ 总利息 8,974；旧实现用先付报价却按期末计息、末期 balloon，总利息 9,569（末期 3,622.42），与报价不一致。默认期末还款 ⇒ 不命中。",
  },
  {
    slug: "finance/inflation-calculator",
    inputs: { amt: "0", rate: "3", years: "20" },
    expect: ["「amt」是本计算的分母，不能为 0"],
    ref: "边界例：当前金额 0 会使购买力变化率 (现值/0−1)×100 无定义，页面已有 __tbInputGuard 分母守卫并显式提示（已拦截，无需改算）。默认态 100,000 元不出现该串。",
  },
  {
    slug: "finance/analysis-risk",
    inputs: {},
    clicks: ["var map={s:'1000',v:'0',f:'0',i:'1000',t:'0',n:'1',dec:'2'};for(var k in map){document.getElementById(k).value=map[k];}calc();document.getElementById('__tbProbe').textContent='DFLZERO '+(document.getElementById('res').innerHTML.indexOf('(1000.00 − 1000.00) = —')>=0?'OK':'BAD');"],
    expect: ["DFL = 1000.00 ÷ (1000.00 − 1000.00) = —"],
    ref: "边界负例：DFL = EBIT ÷ (EBIT−利息)，利息恰好等于 EBIT 时 EBT=0，旧实现把 0 校验写在分子 ebit!==0 上 ⇒ 输出 Infinity；现分母 ebt===0 返回 —。默认态 EBIT 300,000 / 利息 50,000 不命中。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "k-capital": "100000", "k-winrate": "55", "k-ratio": "0", "k-fraction": "0.5" },
    expect: ["盈亏比须大于 0"],
    ref: "边界负例：凯利公式 f*=(p×b−q)/b 在盈亏比 b=0 时分母为 0，旧实现输出 Infinity 仓位；现显式拒绝。默认态盈亏比 2 不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { ft_income: "20", ft_members: "0" },
    clicks: ["switchMethod('four-three')"],
    expect: ["家庭人口数须不小于 1"],
    ref: "边界负例：4321 法则的人均保额 = 年收入/家庭人口数，人口 0 时分母为 0，旧实现输出 Infinity；现显式拒绝。默认 3 人不命中。",
  },
  {
    slug: "finance/portfolio-return",
    inputs: { w1: "", w2: "40", r1: "12", r2: "8" },
    expect: ["请填写：资产1权重"],
    ref: "空态守卫（A 类）：w1 留空时旧实现 num('')=0 → 权重合计 40%、偏差 -60.00% 并照算组合收益；现前置判空点名缺失字段。默认 w1=60 ⇒ 不命中。",
  },
  {
    slug: "finance/portfolio-return",
    inputs: { w1: "0", w2: "0" },
    expect: ["权重合计为 0"],
    ref: "非空但非法：两项权重均为显式 0 时组合无有效权重，旧实现输出「⚠️ 偏差 -100.00%」这类结论；现提示至少给一项非零权重。默认 60/40 ⇒ 不命中。",
  },
  // ---- F-N224–F-N233 金融贷款族修复批次 · 小批 A（5 例，强判别） ----
  {
    slug: "finance/loan-comparison",
    inputs: {"a-principal":"100000","a-rate":"","a-months":"36","b-principal":"100000","b-rate":"4.8","b-months":"36","c-principal":"100000","c-rate":"4.6","c-months":"30"},
    clicks: ["calc()"],
    expect: ["方案 A ⚠ 无效方案：年利率须在 0%–100% 之间，已排除比较 方案 B 月供： 2988.12 元"],
    ref: "F-N229：方案 A 年利率留空，旧实现 `isFinite(NaN)?:0` 静默按 0%（月供 2777.78、有效年化 0.00%）参与排名；现判无效并排除，B 方案 100000/4.8%/36 期月供 2988.12 元照常展示。expect 把 A 的无效提示与 B 的独立复算月供绑成一条，默认态（A 4.8% 有效）不含该串 ⇒ 零逃生。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "10000", dailyRate: "0.05", minRatio: "1", repayType: "minimum" },
    clicks: ["calc()"],
    expect: ["10,509.29 循环利息总额 17,515.49 120 期累计已付", "⚠️ 120 期内未还清，剩余本金 2,993.80 元未计入累计已付"],
    ref: "F-N225：日息万五、最低还款 1%，逐月 `pay=min(余额×1%+余额×0.0005×30, 余额+息)` 模拟 120 期 ⇒ 累计利息 10,509.29 元、剩余本金 2,993.80 元、累计已付 =(10000−2993.80)+10509.29 = **17,515.49** 元。旧实现 `总支出=bill+利息` 报 20,509.29，把未付本金当已付。两条 expect 分别锁定数值与剔除口径；默认（10% 最低还款、55 期还清）不命中。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "10000", dailyRate: "0.05", minRatio: "10", repayType: "installment", installmentFee: "0.75", installmentMonths: "12" },
    clicks: ["calc()"],
    expect: ["16.22% 实际年化（单利近似 ×12）", "17.48% 对照：按月复利有效年化"],
    ref: "F-N230：分期 10000 元 /12 期 /0.75% 手续费，每期 908.33 元，IRR 月利率二分 80 次 ⇒ 单利近似 ×12 = 16.22%、按月复利 EAR = 17.48%。旧实现只把 EAR 标成「实际年化利率」，与 `installment-real-rate` 的双列命名冲突；现两列并列。默认态为 minimum 模式、不出现这两个标签 ⇒ 零逃生。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "10000", dailyRate: "0.05", billDay: "0", dueDay: "30", minRatio: "10", repayType: "minimum" },
    clicks: ["calc()"],
    expect: ["账单日与还款日须为 1–31 的整数"],
    ref: "F-N122：账单日 0 旧实现 `+value||1` 静默变 1、非法 99 被免息天数 clamp 掩盖，任何日期都照常出结果；现 billDay/dueDay 校验 1–31 整数，非法即字段级拒绝并清结果区。expect 锁拒绝提示；默认态 10/30 合法不命中 ⇒ 零逃生。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "10000", dailyRate: "0.05", billDay: "2", dueDay: "20", minRatio: "10", repayType: "minimum" },
    clicks: ["calc()"],
    expect: ["账单日 2 日 / 还款日 20 日仅用于估算免息天数，不参与循环利息与分期计息"],
    ref: "F-N122：口径透明——结果区标注账单日/还款日仅估算免息期、不参与计息（按 30 天/月模拟），消除「日期影响利息」的误解。expect 绑定注入的 2/20 具体日期（默认态 10/30 不命中 ⇒ 零逃生）；旧实现无此标注即变红。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "120000", annualRate: "6", loanYears: "10", balloonMonths: "", balloonRatio: "", prepayMonth: "", prepayAmount: "" },
    clicks: ["calc()"],
    expect: ["1,332.25 首月月供 39,869.52 原计划总利息"],
    ref: "F-N226：等额本息下清空「期末尾款比例 / 气球期数 / 提前还款期数 / 提前还款金额」四个隐藏字段，旧 `__tbInputGuard` 把 7 字段全列必填 ⇒ 直接报「请填写…后再计算」；现仅校验当前模式参与计算的字段，120000/6%/10 年正常输出月供 1,332.25、总利息 39,869.52（独立复算 M=P·i(1+i)^n/((1+i)^n−1)）。默认态 500000/4.9%/30 年不命中。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "1000000", annualRate: "4.9", loanYears: "5", repayMethod: "balloon", balloonMonths: "120", balloonRatio: "50" },
    clicks: ["calc()"],
    expect: ["气球贷还款期数（120 月）不能超过贷款年限 × 12（60 月），请调整后再计算"],
    ref: "F-N228：气球贷 `loanMonths=balloonMonths` 完全忽略 years，旧实现 5 年贷款配 120 期仍照常出表、年限与还款期数无关联提示；现校验 `balloonMonths > floor(years)*12` 即拒绝（120 > 60），并在合法路径结果区如实说明年限仅作期数上限。默认（30 年 /60 期）不命中。",
  },

  // ---- F-N224–F-N233 金融贷款族修复批次 · 小批 B（提前还款归因） ----
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "4.5", months: "240", monthly: "4000", prepay: "0" },
    clicks: ["calc()"],
    expect: ["较对照方案节省（元） 0.00 0.00 两种方式节省相同（0.00 元）", "169 个月（缩短 0 个月） 169 个月（不变）"],
    ref: "F-N224：提前还款金额为 0、月供 4000（高于应还 3163.25）时，旧实现拿「应还月供 × 240 期 = 759179.25」当基准、却用 4000 算新方案，报「节省 83,179.42」——纯属多还月供的效应。现以同月供不提前还款的 169 期、675955.07 元为对照，两方案总支出均 675955.07 ⇒ 两列节省精确为 0.00、期数缩短 0 个月。默认态（prepay=20000）不含 ⇒ 零逃生。",
  },
  {
    slug: "finance/mortgage-prepayment",
    inputs: { principal: "500000", rate: "4.5", months: "240", monthly: "3000", prepay: "20000" },
    clicks: ["calc()"],
    expect: ["对照方案（不提前还款，月供不变）：月供 3000.00 元 × 263 期，总还款 786133.97 元", "245 个月（缩短 18 个月） 263 个月（不变）"],
    ref: "F-N233：月供 3000 低于应还 3163.25，旧实现以应还月供 240 期为基准，①显示「245 个月（延长 5 个月）」却同时报省 4,179.25，结论自相矛盾。现对照方案按实际月供 3000 逐期摊还需 263 期 / 786133.97 元，提前还 20000 后① 245 期即「缩短 18 个月」、② 保持 263 期，并保留「月供低于应还月供」负摊还警示。默认态月供已回填 3163.25（对照 240 期）⇒ 不命中。",
  },

  // ---- F-N224–F-N233 金融贷款族修复批次 · 小批 B（先息后本/气球贷提前还款） ----
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "1000000", annualRate: "4.9", loanYears: "30", repayMethod: "interest", prepayMonth: "24", prepayAmount: "100000" },
    clicks: ["calc(); calcPrepay()"],
    expect: ["还款后剩余本金： 900,000.00 元 节省利息： 137,200.00 元", "节省利息： 137,200.00 元 先息后本 / 气球贷按剩余本金逐期计息"],
    ref: "F-N227：先息后本每期只付 `本金 × 月利率`、本金到期一次归还。100 万 / 4.9% / 360 期、第 24 期提前还 10 万 ⇒ 剩余 336 期每期少付 100000 × 0.049/12 = 408.33 元利息，共 **137,200.00** 元。旧实现 `savedInterest` 只累加原计划剩余利息（1,372,000）、从不减新计划利息，且 reduceTerm 把 newMonths 留空 ⇒ 虚报 10 倍；现按本金冲减口径精确计算并注明「不重摊期数」（缩短 0 期）。默认态为等额本息且未打开提前还款面板 ⇒ 不命中。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "1000000", annualRate: "4.9", loanYears: "30", repayMethod: "balloon", balloonMonths: "60", balloonRatio: "50", prepayMonth: "24", prepayAmount: "100000" },
    checks: ["reducePayment"],
    clicks: ["calc(); calcPrepay()"],
    expect: ["减少月供： 0.00 元 新月供：11,454.39 元", "节省利息： 14,700.00 元"],
    ref: "F-N227：气球贷 60 期、第 24 期提前还 10 万，剩余 36 期按本金冲减口径省息 100000 × 0.049/12 × 36 = **14,700.00** 元。降月供分支旧实现只在 equal / principal 给 `newPayment` 赋值，其余模式恒 0 ⇒ 显示「新月供 0.00 元」；现气球贷提前还款冲减期末尾款、月供保持 11,454.39 元不变（减少 0.00 元）。将 `checks` 设为 reducePayment 使 `querySelector` 取降月供；判别器清空 checks 后回落到缩期态 ⇒ 不产生逃生。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "1000000", annualRate: "4.9", loanYears: "30", prepayMonth: "24", prepayAmount: "-100000" },
    clicks: ["calc(); calcPrepay()"],
    expect: ["提前还款金额须大于 0"],
    ref: "F-N227：提前还款金额为负时，旧实现 `newBalance = balanceBefore - (-100000)` 令剩余本金凭空增加 10 万且照常给出「节省利息」结论；现前置拒绝（须 > 0）。默认提前还款额 100000 为正 ⇒ 不命中。",
  },

  // ---- F-N8：投入时点 / 现金流序列纳入历史快照（两页各一组强判别） ----
  {
    slug: "finance/dca-calculator",
    inputs: { dcaTiming: "end", monthly: "1000", years: "1", rate: "12", initial: "0", target: "0" },
    clicks: ["__dcaSyncTiming(); calc()"],
    expect: ["期末总资产： ¥12,682.50", "累计收益： +¥682.50"],
    ref: "F-N8：投入时点此前只存在 JS 变量 `timing`，通用历史快照只扫 `input[id]` ⇒ 历史恢复后沿用当前时点、无法重现原结果。现新增带 id 的只读快照输入 `dcaTiming`，历史的 `mount` 回填回调显式调用 `__dcaSyncTiming()` 把时点同步回 JS 变量与按钮后再 `calc()`（不在每次 calc 里隐式覆盖，避免盖掉用户当期选择）。注入 `dcaTiming=end` 并在 clicks 里模拟该恢复回调（期末投入）、月投 1000、1 年、年化 12%、初始 0：期末资产 = Σ 1000×1.01^k (k=0..11) = **¥12,682.50**，累计收益 **+¥682.50**；期初投入同参数为 12,809.33。三态实测：注入 begin 与纯默认快照（10 年 / 8%）都不命中这两条；旧版没有 `dcaTiming` 输入 ⇒ 注入失败、只会给期初值，同样不命中。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: { dcaTiming: "begin", monthly: "1000", years: "1", rate: "12", initial: "0", target: "0" },
    clicks: ["__dcaSyncTiming(); calc()"],
    expect: ["期末总资产： ¥12,809.33"],
    ref: "F-N8 回归护栏：显式回填 `dcaTiming=begin` 必须仍按**期初**投入计算，期末资产 = Σ 1000×1.01^k (k=1..12) = **¥12,809.33**，与上面的期末投入 12,682.50 相差一个月利息，证明时点切换是双向可逆的（不是把整页锁死在期末）。纯默认快照（10 年 / 8% ⇒ 184,165.68）不命中。",
  },
  {
    slug: "finance/irr-calculator",
    inputs: { irrCashflowSnapshot: "T0:-100,T1:115", discountRate: "8", periodUnit: "year" },
    clicks: ["__irrRestoreFromSnapshot(); calc()"],
    expect: ["15.00%", "每期 IRR = 15.0000%", "NPV @ 折现率 8.00% = 6.48"],
    ref: "F-N8：现金流控件由 `renderFlows()` 动态生成且无 id，通用历史快照漏掉全部期号与金额 ⇒ 恢复历史后仍用当前现金流。现新增只读快照输入 `irrCashflowSnapshot`（`T期号:金额` 序列），历史的 `mount` 回填回调显式调用 `__irrRestoreFromSnapshot()` 按快照重建现金流再 `calc()`；`renderFlows` / `updateAmount` 等在每次变化时写回快照并落 localStorage，保证快照不落后于内存。刻意不在 `calc()` 里隐式读回（否则会覆盖用户当期输入与 clicks 直接赋数组）。注入 `T0:-100,T1:115` 并在 clicks 里模拟该恢复回调、贴现率 8%、期数单位=年：IRR = 115/100 − 1 = **15.00%**（页面 `每期 IRR = 15.0000%`）；NPV = −100 + 115/1.08 = **+6.48**。三态实测：只注入贴现率/期数单位（不注入快照）与纯默认快照（project 预设 IRR≈16.60%）三条都不命中；旧版无该输入 ⇒ 注入失败，同样不命中。刻意避开 `-100/230/-132` 双根现金流（多根识别属另案 F-N29）。",
  },
  {
    slug: "finance/shebeizulinfeilvjisuan",
    inputs: { price: "500000", months: "24", depYears: "8", maintRate: "3", profitRate: "8", salvageRate: "150" },
    clicks: ["calc()"],
    expect: ["残值率须在 0–100% 之间，维护费率与利润率不得为负。"],
    ref: "F-N64 残值率上界：s=150% ⇒ 旧实现 depreciableBase 为负、月折旧/租金可为负，仍输出正 ROI。修复后 readInputs 字段级拒绝。默认 s=5 ⇒ 不命中。",
  },
  {
    slug: "finance/shebeizulinfeilvjisuan",
    inputs: { price: "500000", months: "24", depYears: "8", maintRate: "3", profitRate: "8", salvageRate: "12", disposal: "salvage" },
    clicks: ["calc()"],
    expect: ["¥9166.67 月租金 (元)", "-50.00% 投资回报率 ROI", "按折旧期末残值回收"],
    ref: "F-N64 正常态 + ROI 公式口径：P=50万/T=24/Y=8/r=3/m=8/s=12，显式选择按折旧期末残值回收 ⇒ 残值 60000、月折旧 4583.33、月租 9166.67；总租金 220000 + 回收 60000 − 原值 500000 − 维护 30000 = −250000 ⇒ ROI −50.00%（旧实现漏扣维护得 −44.00%）。第933批起默认改为按租期末账面价值回收，故本用例显式指定 salvage。",
  },
  {
    slug: "finance/shebeizulinfeilvjisuan",
    inputs: { price: "500000", months: "24", depYears: "8", maintRate: "3", profitRate: "8", salvageRate: "12", disposal: "book" },
    clicks: ["calc();var t=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='RENTBOOK '+(t.indexOf('390000.00')>=0?'B':'N')+' '+(t.indexOf('16.00%')>=0?'R':'N');"],
    expect: ["RENTBOOK B R"],
    ref: "第933批：短租期默认按租期末账面价值回收。月折旧 4583.33×24=110,000 累计折旧，账面 500,000−110,000=390,000；净收益 220,000+390,000−500,000−30,000=80,000 ⇒ ROI 16.00%。用拼接探针同时锁定两个值，避免只命中通用标签「租期内累计折旧 (元)」的逃生。旧实现无论租期都用残值 60,000，得 −44.00%。",
  },
  {
    slug: "finance/isbn-validator",
    inputs: { isbnInput: "4006381333931" },
    clicks: ["validate()"],
    expect: ["前缀 400 不是 978/979，这是普通商品条码（EAN-13），不是 ISBN"],
    ref: "F-N129 防回归锁：合法 EAN-13 商品码 4006381333931（mod-10 校验和正确但前缀 400 非 ISBN）必须判「非 ISBN 前缀」，不得宣称「ISBN-13 校验通过」。默认 978 前缀不命中。源码 HEAD 已修，本锁防未来把前缀判断改回仅查 mod-10 的退化。",
  },
  {
    slug: "finance/isbn-validator",
    inputs: { isbnInput: "1234567890" },
    clicks: ["validate()"],
    expect: ["源 ISBN-10 校验未通过，不生成对应 ISBN-13"],
    ref: "F-N130 防回归锁：1234567890 校验和 210 mod 11 = 1（应为 0），源 ISBN-10 非法 ⇒ 结果区不得生成对应 ISBN-13。默认 978 前缀走 13 位分支不命中。源码 HEAD 已修，本锁防未来把「对应 ISBN-13」无条件输出的退化。",
  },
  {
    slug: "finance/iban-validator",
    inputs: { ibanInput: "ZZ121234567890" },
    expect: ["国家代码未收录，仅完成数学校验，不能判定有效"],
    ref: "F-N132 防回归锁：ZZ121234567890 后四位前移后 BigInt mod-97 == 1（数学校验通过）但国家代码 ZZ 未收录 ⇒ 总体结论必须判「不能判定有效」，不得显示绿色「✅ mod-97 校验通过」假阳性。默认 DE89 国家已收录不命中。源码 HEAD 已修（总体结论三态），本锁防未来把国家存在性从结论中剔除的退化。",
  },
  {
    slug: "finance/iban-validator",
    inputs: { ibanInput: "SA0380000000608010167519" },
    clicks: ["validate();var h=String(document.getElementById('result').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='IBSA '+document.getElementById('ibanInput').value+' '+((h.indexOf('沙特阿拉伯 (SA)')>=0&&h.indexOf('长度校验： ✅ 当前 24 位，期望 24 位')>=0&&h.indexOf('国家、长度与 mod-97 校验均通过')>=0)?'OK':'BAD');"],
    expect: ["IBSA SA0380000000608010167519 OK"],
    ref: "F-N133 防回归锁：SA0380000000608010167519 长度 24、mod-97==1，沙特阿拉伯必须收录、长度 24 校验通过、总体判有效，三项用探针 AND 串一次断言。旧表仅 33 国不含 SA ⇒ 三项皆不满足得 BAD。⚠️ 用 __tbProbe 而非静态 blob：页面预置国家表格含所有国名，直接写 blob 会被表格串干扰/默认态命中；探针仅取 result 容器且绑定输入号 ⇒ 零逃生。参考 MEID/DNI 用例模式。",
  },
  {
    slug: "finance/bic-validator",
    inputs: { input: "DEUT DEFF" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='BICSP '+document.getElementById('input').value+' '+((h.indexOf('长度： 8 字符')>=0&&h.indexOf('银行代码： DEUT')>=0&&h.indexOf('BIC 代码格式有效')>=0)?'OK':'BAD');"],
    expect: ["BICSP DEUT DEFF OK"],
    ref: "F-N137 防回归锁：标准 4+2+2 空格写法「DEUT DEFF」先 replace(/[\\s-]/g,'') 清洗为 DEUTDEFF(8 位) 后应判格式有效；旧实现只 trim 不清洗 ⇒ 长度变 9 报「长度必须为 8 或 11」。探针 AND 断言长度 8 + 银行代码 + 格式有效三项，绑定原始输入串 ⇒ 默认态不命中。",
  },
  {
    slug: "finance/bic-validator",
    inputs: { input: "<img src=x onerror=alert(1)>" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent='BICXSS '+((h.indexOf('&lt;IMG')>=0&&h.indexOf('<IMG')<0&&h.indexOf('<img')<0)?'ESC':'RAW');"],
    expect: ["BICXSS ESC"],
    ref: "F-N136 防回归锁：用户输入 <img src=x onerror=alert(1)> 经 toUpperCase+去空格得 <IMGSRC=XONERROR=ALERT(1)>，写入 innerHTML 前必须 esc() 转义为 &lt;IMG…&gt;；旧实现直接拼 raw ⇒ 输出含裸 <IMG 可执行。探针断言含 &lt;IMG 且不含裸 <IMG/<img ⇒ 零逃生（与输入值无关，纯转义行为锁）。",
  },
  {
    slug: "finance/currency-symbol",
    inputs: { searchInput: "AUD" },
    clicks: ["search();var g=String(document.getElementById('currencyGrid').innerHTML);var n=(g.match(/AUD/g)||[]).length;document.getElementById('__tbProbe').textContent='CURDEDUP '+(currencies.length===149&&n===2?'OK':'BAD len='+currencies.length+' aud='+n);"],
    expect: ["CURDEDUP OK"],
    ref: "F-N138 去重锁：原始数组 153 条、AUD/XCD/UGX/NIO 各重复 2 次，运行时按 code 去重后应剩 149 条 ⇒ 搜索 AUD 只渲染 1 张卡片。旧实现不去重为 153 条/2 张卡片。语义化卡片后 AUD 同时出现在 aria-label 与代码行，故探针断言 currencies.length===149 且 AUD 字符串===2（1 张卡片）（不依赖 resultStat，harness 下该计数被二次渲染污染）⇒ 真判别、零逃生。",
  },
  {
    slug: "finance/currency-symbol",
    inputs: { searchInput: "" },
    clicks: ["var c=null;for(var i=0;i<currencies.length;i++){if(currencies[i].code==='CNY'){c=currencies[i];break;}}document.getElementById('__tbProbe').textContent='CURCNY '+(c&&c.subunit==='Fen'&&c.subunitRate===100?'OK':'BAD '+(c?c.subunit+'/'+c.subunitRate:'NOCNY'));"],
    expect: ["CURCNY OK"],
    ref: "F-N140 辅单位锁：CNY 的辅单位应为 Fen、换算 100（1 Yuan = 100 Fen）。旧实现 subunit:'Jiao/Fen' + subunitRate:10 显示「1 Yuan = 10 Jiao/Fen」。探针遍历去重后 currencies 找 CNY 读 subunit/subunitRate 两字段（不依赖 showDetail，harness 下其 index 参数被包装污染）⇒ 真判别、零逃生。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "10000", dailyRate: "", minRatio: "10", repayType: "minimum" },
    clicks: ["calc()"],
    expect: ["日利率不能为空；如确为 0，请明确输入 0。"],
    ref: "第934批：日利率留空不再按 0 当成免息；明确提示补全。默认 0.05% ⇒ 不命中。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "10000", dailyRate: "0", minRatio: "10", repayType: "minimum", installmentFee: "0", installmentMonths: "12" },
    clicks: ["showCompare()"],
    expect: ["两种方案总支出相同"],
    ref: "第934批：零利率 + 零手续费时最低还款 10 期还清、分期 12 期，总支出均 10000；差额小于 0.01 元时不再固定说最低还款更省钱。默认 0.05%/0.75% ⇒ 不命中。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "10000", dailyRate: "-0.05", minRatio: "10", repayType: "minimum" },
    clicks: ["calc()"],
    expect: ["日利率须为 ≥0 的有效数字（当前 -0.05%）"],
    ref: "F-N124 负值拒绝：日利率 −0.05 旧实现 +value/100||0 → 负利率照算得负利息/负总支出；第934批改为严格的空值/有限/非负校验，提示「日利率须为 ≥0 的有效数字（当前 -0.05%）」。默认日利率 0.05 ⇒ 不命中。",
  },
  {
    slug: "finance/uan-validator",
    inputs: { input: "10A1234567890" },
    clicks: ["validate()"],
    expect: ["第 3 位含非法字符「A」"],
    ref: "F-N148 字母剔除修复：10A1234567890 旧实现 replace(/\\D/g,'') 静默剔除 A → 101234567890（12 位）判「✅ UAN 格式有效」；修复后含字母在第 3 位报错并指出字符。输入绑定串 ⇒ 默认态不命中。",
  },
  {
    slug: "finance/uan-validator",
    inputs: { input: "10-1234567890" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='UANHY '+document.getElementById('input').value+' '+((h.indexOf('101234567890')>=0&&h.indexOf('12 位')>=0&&h.indexOf('UAN 格式有效')>=0&&h.indexOf('非法字符')<0)?'OK':'BAD');"],
    expect: ["UANHY 10-1234567890 OK"],
    ref: "F-N148 防误伤：连字符分隔是合法写法，去掉分隔符后 101234567890 共 12 位、首字符 1 ⇒ 格式有效且不报非法字符。探针 AND 四项并绑输入号（静态结论串「✅ UAN 格式有效」在默认态也命中会成逃生，故走探针）⇒ 零逃生。",
  },
  {
    slug: "finance/aadhaar-validator",
    inputs: { input: "234123412346A" },
    clicks: ["validate()"],
    expect: ["第 13 位含非法字符「A」"],
    ref: "F-N151 字母拒绝：合法 Aadhaar 234123412346 尾随字母 A，旧实现 replace(/\\D/g,'') 静默剔除后判有效；修复后第 13 位报「非法字符「A」」。绑定输入与位置 ⇒ 默认态不命中。",
  },
  {
    slug: "finance/cpf-validator",
    inputs: { input: "abc11144477735" },
    clicks: ["validate()"],
    expect: ["第 1 位含非法字符「a」"],
    ref: "F-N154 字母拒绝：abc11144477735 旧实现静默剔除 abc 得 11144477735（合法 CPF）判有效，与 FAQ「含字母判格式错误」矛盾；修复后第 1 位报「非法字符「a」」。绑定输入与位置 ⇒ 默认态不命中。",
  },
  {
    slug: "finance/cpf-validator",
    inputs: { input: "111.444.777-35" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='CPFPT '+((h.indexOf('格式化： 111.444.777-35')>=0&&h.indexOf('CPF 号码有效')>=0&&h.indexOf('非法字符')<0)?'OK':'BAD');"],
    expect: ["CPFPT OK"],
    ref: "F-N154 防误伤：点/连字符是 CPF 标准分组写法（111.444.777-35），清洗后 11144477735 合法有效且不报非法字符。探针 AND 三项（静态「✅ CPF 号码有效」默认态命中会成逃生，故走探针）⇒ 零逃生。",
  },
  {
    slug: "finance/cpf-validator",
    inputs: { input: "<img src=x onerror=alert(1)>" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent='CPFXSS '+((h.indexOf('&lt;img')>=0&&h.indexOf('<img')<0&&h.indexOf('<IMG')<0)?'ESC':'RAW');"],
    expect: ["CPFXSS ESC"],
    ref: "F-N150 自 XSS：输入 <img src=x onerror=alert(1)>，四页原样插值 ${raw} 会执行；修复后 esc(raw) 转义为 &lt;img…&gt;（这四页未大写化，保留小写）。探针断言含 &lt;img 且不含裸 <img/<IMG ⇒ 零逃生（纯转义行为锁）。",
  },
  {
    slug: "finance/esn-validator",
    inputs: { input: "80A1B2C3" },
    clicks: ["validate()"],
    expect: ["12810597059（3 位制造商码 + 8 位序列号）"],
    ref: "F-N155 十进制标准拼接：80A1B2C3（制造商 0x80=128、序列 0xA1B2C3=10597059）应输出标准 11 位十进制 ESN 12810597059（3+8 拼接）。旧实现 parseInt(hex,16) 整体转十进制得 02158080707（互不可逆）。输入绑定串 ⇒ 默认 A1B2C3D4 不同值不命中。",
  },
  {
    slug: "finance/esn-validator",
    inputs: { input: "A1B2C3D4G" },
    clicks: ["validate()"],
    expect: ["第 9 位含非法字符「G」"],
    ref: "F-N156 非法字符拒绝：A1B2C3D4G 第 9 位 G 非十六进制，旧实现 replace(/[^0-9A-F]/g,'') 静默剔除后按 8 位 HEX 判有效；修复后按整体形态判并报第 9 位非法字符。输入绑定串 ⇒ 默认态不命中。",
  },
  {
    slug: "finance/esn-validator",
    inputs: { input: "00000000" },
    clicks: ["validate()"],
    expect: ["制造商码 0x00 为保留码，ESN 无效"],
    ref: "F-N156 保留码拒绝：8 位 HEX 00000000 制造商码 0x00（MFR_DB 标 RESERVED）应判无效。旧实现无条件输出「✅ ESN HEX 格式有效」。输入绑定保留码 ⇒ 默认态不命中。",
  },
  {
    slug: "finance/ein-validator",
    inputs: { input: "00-0000000" },
    clicks: ["validate()"],
    expect: ["前缀 00 属已知保留/未分配段，按格式规则判无效"],
    ref: "F-N157 前缀判据锁：00 是 IRS 保留/未分配前缀，should 判无效。旧实现 IRS_PREFIX 查表只用于展示、无条件 ✅；修复后 EIN_INVALID_PREFIX 黑名单参与判据。默认 01-1234567 有效前缀不命中。",
  },
  {
    slug: "finance/ein-validator",
    inputs: { input: "1-2-3-4-5-6-7-8-9" },
    clicks: ["validate()"],
    expect: ["格式化： 12-3456789"],
    ref: "F-N158 分隔符容错口径：乱分隔 1-2-...-9 剥离后 123456789，归一化为 12-3456789 并判有效（公式框已改为「剥离分隔符后 9 位数字」口径，与实现自洽）。旧实现公式写 ^\\d{2}-\\d{7}$ 与行为矛盾。默认 01-1234567 不同值不命中。",
  },
  {
    slug: "finance/imei-validator",
    inputs: { input: "356938035643809" },
    clicks: ["validate();var h=String(document.getElementById('output').innerHTML).replace(/<[^>]*>/g,' ').replace(/\\s+/g,' ');document.getElementById('__tbProbe').textContent='IMEIFIX '+document.getElementById('input').value+' '+((h.indexOf('校验位： 9（期望 9） ✅')>=0&&h.indexOf('IMEI 号码有效')>=0)?'OK':'BAD');"],
    expect: ["IMEIFIX 356938035643809 OK"],
    ref: "F-N172 校验位相位修复：356938035643809 是 Luhn 合法 15 位 IMEI（校验位 9），期望位必须由前 14 位本体反推得 9，不得出现「校验位 9（期望 0）❌」与「✅ 有效」同屏矛盾。旧实现把含校验位的整串从右 alt=false 求和致期望恒 0。探针 AND 两串并绑输入号（裸 blob 中该串在判别器注入失败态仍命中别处，故走探针）⇒ 零逃生。",
  },
  {
    slug: "finance/imei-validator",
    inputs: { input: "3569380356438097" },
    clicks: ["validate()"],
    expect: ["长度： 16 位（IMEISV）", "软件版本号 SVN： 97", "IMEISV 不含校验位，仅检查 16 位数字结构"],
    ref: "IMEISV 由 8 位 TAC、6 位 SNR 和 2 位 SVN 构成，不含 Luhn 校验位，不能宣称校验通过。",
  },

  // ---------------- 第 119 批：F-N160/161/162（word-wrap）、F-N146、F-N152 判别锁 ----------------
  {
    slug: "finance/swift-bic-validator",
    inputs: { input: "DEUT DE FF 500" },
    expect: ["已忽略 3 个空格/连字符分隔符"],
    ref: "F-N146 4-2-2-3 分组书写：DEUT DE FF 500 含 3 个空格，归一化后按 DEUTDEFF500 校验并注明忽略数量；旧源码只 trim+uppercase ⇒ 长度 14 报错、不含该串 ⇒ 不命中。默认态不含。",
  },
  {
    slug: "finance/swift-bic-validator",
    inputs: { input: "<img src=x onerror=alert(1)>" },
    clicks: ["validate();var h=document.getElementById('output').innerHTML;document.getElementById('__tbProbe').textContent='SWXSS '+(h.indexOf('<img')<0&&h.indexOf('&lt;IMG')>=0&&h.indexOf('仅允许字母、数字')>=0?'OK':'BAD');"],
    expect: ["SWXSS OK"],
    ref: "F-N146 顺带修回显 XSS：非法输入须转义后回显并明确拒绝，不能把 <img> 原样插入 innerHTML；旧源码无转义、无白名单分支 ⇒ 不命中。探针绑定被测输入。",
  },
  {
    slug: "finance/aadhaar-validator",
    inputs: { input: "00-0000-0000-00" },
    expect: ["格式化： 0000 0000 0000"],
    ref: "F-N152 首位 0/1 分支须与常规分支一样给出「输入/格式化/长度」上下文；旧源码该分支只输出一句错误后早退，不含格式化行 ⇒ 不命中。默认态不含。",
  },
  {
    slug: "finance/word-wrap",
    inputs: { width: "8" },
    clicks: ["document.getElementById('countBytes').checked=true;document.getElementById('__tbProbe').textContent='WWBYTES '+(visualLen('中文测试')===12&&visualLen('😀')===4?'OK':'BAD');"],
    expect: ["WWBYTES OK"],
    ref: "F-N161 按真实 UTF-8 字节计：中文 3 字节 ⇒「中文测试」=12、emoji=4；旧实现把 CJK 记 2 字节、emoji 记 1 ⇒ 8/1，不命中。与 deep-dive/FAQ「中文 UTF-8 占 3 字节」口径一致。",
  },
  {
    slug: "finance/word-wrap",
    inputs: { width: "20", mode: "chinese" },
    clicks: ["document.getElementById('input').value='这是一个没有任何标点的超长连续中文句子用于测试按中文断句模式是否会在宽度不足时继续强行折行';wrap();var ls=document.getElementById('result').textContent.split('\\n');document.getElementById('__tbProbe').textContent='WWZH '+(ls.length>=3&&ls.every(function(l){return l.length<=20;})?'OK':'BAD');"],
    expect: ["WWZH OK"],
    ref: "F-N162 无标点超长中文句必须退回逐段强折：宽 20、45 字长句应至少 3 行且每行 ≤20；旧 chinese 分支整段压成一行 ⇒ 不命中。探针绑定被测输入。",
  },
  {
    slug: "finance/word-wrap",
    inputs: { width: "20", mode: "word" },
    clicks: ["document.getElementById('hanging').checked=true;document.getElementById('keepExisting').checked=false;document.getElementById('input').value='This is a fairly long English clause that must wrap onto several lines for the hanging indent';wrap();var ls=document.getElementById('result').textContent.split('\\n');document.getElementById('__tbProbe').textContent='WWHANG '+(ls.length>=3&&ls.slice(1).every(function(l){return l.indexOf('  ')===0;})?'OK':'BAD');"],
    expect: ["WWHANG OK"],
    ref: "F-N160 首行/悬挂缩进四模式统一生效：word 模式勾悬挂缩进后，续行须以 2 空格开头且计入行宽；旧实现只有 soft 分支读 indent/hanging ⇒ 续行无前缀、不命中。",
  },

  // ---------------- 第 120 批：F-N103 清空同步、F-N105 口径防回退 ----------------
  {
    slug: "finance/simple-interest",
    inputs: { principal: "10000", rate: "5", years: "3" },
    clicks: ["calc();['simple_interestTable','simple_interestDiff','simple_interestChart','simple_interestHist'].forEach(function(id){var e=document.getElementById(id);if(e)e.innerHTML='<tr><td>OLD</td></tr>';});clearAll();var ids=['simple_interestTable','simple_interestDiff','simple_interestChart','simple_interestHist'];var empty=ids.every(function(id){var e=document.getElementById(id);return e&&!e.innerHTML;});document.getElementById('__tbProbe').textContent='SICLR '+(empty?'OK':'BAD');"],
    expect: ["SICLR OK"],
    ref: "F-N103：清空须同步清掉历史表/趋势图/差异框/历史列表。探针先模拟上次计算留下的 OLD 记录再 clearAll；旧实现只清输入与 resultBox ⇒ 容器残留、不命中。",
  },
  {
    slug: "finance/tax-bracket",
    inputs: { income: "200000" },
    clicks: ["calc()"],
    expect: ["应纳税所得额减本次估算税额： 176,920 元"],
    ref: "F-N105 口径防回退：应税所得 200,000 → 税 200,000×20%−16,920=23,080，税后应税余额 176,920。旧文案「税后所得」不含该口径说明 ⇒ 不命中；默认 100,000（92,520）亦不命中 ⇒ 零逃生。",
  },

  // ---------------- C 组复核失败重做：第113/157/202/203/205/210/211/156 批 ----------------
  {
    slug: "finance/ifsc-validator",
    inputs: { input: "SBIN0FAILED" },
    clicks: ["validate();var __v=String(document.getElementById('input').value);document.getElementById('__tbProbe').textContent='C113IFSC '+(__ifsc_validatorScore('结论 '+__v)===1&&__v.indexOf('FAILED')>=0?'OK':'BAD');"],
    expect: ["C113IFSC OK"],
    ref: "第113批 IFSC：SBIN0FAILED 含 FAILED 字样但符合 ^[A-Z]{4}0[A-Z0-9]{6}$，格式有效。旧 Score 对含用户输入的全文跑 /Failed/i ⇒ 0；修复后按本页格式结论与结构化标记判定 ⇒ 1。探针把注入的 input 拼进评分文本复现污染，旧源码 BAD ⇒ 零逃生。",
  },
  {
    slug: "finance/ifsc-validator",
    inputs: { input: "SBIN0001234" },
    clicks: ["var __g=document.getElementById('input'),__p=document.getElementById('__tbProbe');validate();var a=__ifsc_validatorScore('');__g.value='###';validate();var b=__ifsc_validatorScore('');__g.value='SBIN0001234';validate();var c=__ifsc_validatorScore('');__p.textContent='C113CHAIN '+((a===1&&b===0&&c===1)?'OK':'BAD');"],
    expect: ["C113CHAIN OK"],
    ref: "第113批 IFSC 状态链合法→非法→恢复：三类注入输入分别得 1/0/1，结论随输入变化、非法态不与合法态同值，恢复后不残留旧结论（覆盖历史/趋势复用同一 Score 的语义）。",
  },
  {
    slug: "finance/bic-validator",
    inputs: { input: "INVALIDE" },
    clicks: ["validate();var __v=String(document.getElementById('input').value);document.getElementById('__tbProbe').textContent='C157BIC '+(__bic_validatorScore('结论 '+__v)===1&&__v.indexOf('INVALID')>=0?'OK':'BAD');"],
    expect: ["C157BIC OK"],
    ref: "第157批 FN189 BIC：INVALIDE 的前七位 INVALID 是用户数据、但格式校验通过。旧全文词表 /Invalid/i 命中输入 ⇒ 记 0；修复后只认结论级短语与结构化标记 ⇒ 1。评分文本含注入输入以复现污染，旧源码 BAD ⇒ 零逃生。",
  },
  {
    slug: "finance/iban-validator",
    inputs: { ibanInput: "ZZ191234" },
    clicks: ["validate();var __s=__iban_validatorScore('');document.getElementById('__tbProbe').textContent='C113IBAN '+(isNaN(__s)?'MANUAL':(__s===1?'PASS':'FAIL'));"],
    expect: ["C113IBAN MANUAL"],
    ref: "第113批 IBAN：ZZ191234 国家码 ZZ 未收录、但页面 mod97Check 实测 rem=1（数学校验通过），结论为 ⚠️ 无法判定有效性。旧词表命中「本工具未收录不代表 IBAN 无效」的「无效」⇒ 0；修复后仅认结构化标记（无 ✅/❌）⇒ NaN/MANUAL。简报写的 ZZ101 实测 rem=69 属明确失败，另见下条。",
  },
  {
    slug: "finance/iban-validator",
    inputs: { ibanInput: "ZZ101" },
    clicks: ["validate();document.getElementById('__tbProbe').textContent='C113IBAN0 '+(__iban_validatorScore('')===0?'OK':'BAD');"],
    expect: ["C113IBAN0 OK"],
    ref: "第113批 IBAN 明确失败：ZZ101 在页面 mod97Check 下 rem=69，输出「❌ mod-97 校验失败」⇒ 0。与上条「未收录+数学通过⇒MANUAL」两态不同值，证明无法判定未被当成失败、真实失败也未被放过。",
  },
  {
    slug: "finance/imei-validator",
    inputs: { input: "490154203237518" },
    clicks: ["validate();document.getElementById('__tbProbe').textContent='C113IMEI15 '+(__imei_validatorScore('')===1?'OK':'BAD');"],
    expect: ["C113IMEI15 OK"],
    ref: "第113批 IMEI：15 位且 Luhn 校验通过 ⇒ 1（可校验通过）。修复前 14 位本体也被记 1，见下条状态链。",
  },
  {
    slug: "finance/imei-validator",
    inputs: { input: "49015420323751" },
    clicks: ["var __g=document.getElementById('input'),__p=document.getElementById('__tbProbe');var a=__imei_validatorScore('');__g.value='4901542032375188';var b=__imei_validatorScore('');__g.value='abcdefghijklmno';var c=__imei_validatorScore('');__p.textContent='C113IMEI3 '+((isNaN(a)&&isNaN(b)&&c===0)?'OK':'BAD');"],
    expect: ["C113IMEI3 OK"],
    ref: "第113批 IMEI：14 位本体不含校验位、16 位 IMEISV 均无法判定有效性 ⇒ NaN/MANUAL（不得冒充通过），纯字母非法输入 ⇒ 0。三个不同注入输入得 MANUAL/MANUAL/0，连续不同输入不残留、空/无法判定不与失败同值。",
  },
  {
    slug: "finance/isbn-validator",
    inputs: { isbnInput: "9787111111115" },
    clicks: ["var __g=document.getElementById('isbnInput'),__p=document.getElementById('__tbProbe');validate();var a=__isbn_validatorScore('');__g.value='';validate();var b=__isbn_validatorScore('');__g.value='123';validate();var c=__isbn_validatorScore('');__p.textContent='C113ISBN '+((a===1&&isNaN(b)&&c===0)?'OK':'BAD');"],
    expect: ["C113ISBN OK"],
    ref: "第113批 其他待复核 ISBN：合法 13 位 ⇒ 1、清空是待输入态 ⇒ NaN/MANUAL（旧源码把清空记未通过）、长度非法 ⇒ 0。修复同时把 Score 输入 id 从通用 input 改为本页真实 isbnInput、输出容器改 result 优先（原读错恒空恒 MANUAL）。三态不同值。",
  },
  {
    slug: "finance/iccid-validator",
    inputs: { input: "abc" },
    clicks: ["validate();var __h=String(document.getElementById('output').innerHTML||'');document.getElementById('__tbProbe').textContent='C113ICCID '+((__h.indexOf('含非法字符')>=0||__h.indexOf('Invalid characters')>=0)?'OK':'BAD');"],
    expect: ["C113ICCID OK"],
    ref: "第113批 ICCID：纯字母 abc 旧实现用 if(!digits) 剥离后当等待输入、ResText 过滤不入历史；修复后区分空输入与非空非法输入，输出固定中英文「❌ 含非法字符」（用户输入不进 innerHTML）。旧源码输出「等待输入」不含该提示 ⇒ BAD ⇒ 零逃生。",
  },
  {
    slug: "finance/imsi-validator",
    inputs: { input: "abc" },
    clicks: ["validate();var __h=String(document.getElementById('output').innerHTML||'');document.getElementById('__tbProbe').textContent='C113IMSI '+((__h.indexOf('含非法字符')>=0||__h.indexOf('Invalid characters')>=0)?'OK':'BAD');"],
    expect: ["C113IMSI OK"],
    ref: "第113批 IMSI：同 ICCID，纯字母非法输入须输出「❌ 含非法字符」固定文案并入历史，不得被剥离成空态等待输入。注入 abc 命中，旧源码 BAD。",
  },
  {
    slug: "finance/ird-validator",
    inputs: { input: "abc" },
    clicks: ["validate();var __h=String(document.getElementById('output').innerHTML||'');document.getElementById('__tbProbe').textContent='C113IRD '+((__h.indexOf('含非法字符')>=0||__h.indexOf('Invalid characters')>=0)?'OK':'BAD');"],
    expect: ["C113IRD OK"],
    ref: "第113批 IRD：同 ICCID/IMSI，纯字母 abc 判非法并输出固定中英文提示。三页同一修复模式，注入 abc 命中、旧源码 BAD。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: { monthly: "0", years: "10", rate: "8", initial: "0" },
    clicks: ["calc();var __o=document.getElementById('res'),__sg=document.getElementById('statGrid'),__tw=document.getElementById('tableWrap'),__tm=document.getElementById('totalMonths');document.getElementById('__tbProbe').textContent='C157DCA0 '+((__dca_calculatorScore('')===0&&__sg.innerHTML===''&&__tw.innerHTML===''&&__tm.textContent===''&&String(__o.innerHTML||'').indexOf('初始本金与每月定投均为 0')>=0)?'OK':'BAD');"],
    expect: ["C157DCA0 OK"],
    ref: "第731C批改口径：monthly=0 且 initial=0 才是无本金可增长的无意义输入，提示「初始本金与每月定投均为 0」并清空统计/表格/期数；月投入单项为 0、初始本金 >0 应正常计算（见下条）。旧口径把 monthly 一律当分母拒绝，与复利模型不符。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: { monthly: "1000", years: "1", rate: "0", initial: "0", target: "12000" },
    clicks: ["document.getElementById('__tbProbe').textContent='C157DCAREQ '+(__dca_calculatorScore('计算结果 Required annualized return: 0.00% 正常结束')===1?'OK':'BAD');"],
    expect: ["C157DCAREQ OK"],
    ref: "第157批 定投英文结果：正常标签 'Required annualized return:' 曾被旧 /required/i 命中 ⇒ 记 0；修复后只认结论级拒绝短语、按必填/分母边界判定 ⇒ 1。注入必填项均合法、评分文本含该英文标签；与上条拒绝态两态不同值。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "10000", rate: "5", years: "20", annual: "12000" },
    clicks: ["var __g=document.getElementById('principal'),__p=document.getElementById('__tbProbe');var a=__compound_interestScore('');__g.value='';try{calc();}catch(e){}var b=__compound_interestScore('');__g.value='0';var c=__compound_interestScore('');__p.textContent='C202CI '+((a===1&&isNaN(b)&&c===1)?'OK':'BAD');"],
    expect: ["C202CI OK"],
    ref: "第202批 复利空本金：旧 calc 用 parseFloat(principal.value)||0 把空静默按 0 计算并记通过；修复后空字符串停算并 resetDisplay 清终值/年表、Score ⇒ NaN/MANUAL，显式 0 仍为合法数值 ⇒ 1。三态不同值，不以禁止合法的 0 代替空值判断。",
  },
  {
    slug: "finance/simple-interest",
    inputs: { principal: "10000", rate: "5", years: "3" },
    clicks: ["var __g=document.getElementById('principal'),__p=document.getElementById('__tbProbe');var a=__simple_interestScore('');__g.value='';var b=__simple_interestScore('');__g.value='0';var c=__simple_interestScore('');__p.textContent='C203SI '+((a===1&&isNaN(b)&&c===1)?'OK':'BAD');"],
    expect: ["C203SI OK"],
    ref: "第203批 单利空本金：清空本金旧 calc 仍产出本金 0/利息 0 的结果并记通过、导出显示「本金：0 元」；修复后空态停算只提示、Score ⇒ MANUAL，显式 0 合法 ⇒ 1。与复利页同口径，三态不同值。",
  },
  {
    slug: "finance/retirement-calculator",
    inputs: { age: "30", retireAge: "60", lifeAge: "85" },
    clicks: ["var __g=document.getElementById('age'),__p=document.getElementById('__tbProbe');var a=__retirement_calculatorScore('');__g.value='70';var b=__retirement_calculatorScore('');__g.value='30';var c=__retirement_calculatorScore('');__p.textContent='C203RET '+((a===1&&b===0&&c===1)?'OK':'BAD');"],
    expect: ["C203RET OK"],
    ref: "第203批 退休年龄顺序状态链：30<60<85 ⇒ 1；age=70≥60 顺序无效 ⇒ 0；恢复 30 ⇒ 1。旧 Score 未识别年龄顺序拒绝态恒记 1。兜底刻意不含 ❌，保留「资金不足/接近目标」为有效计算结论，不把所有警告当计算失败。",
  },
  {
    slug: "finance/retirement-calculator",
    inputs: { age: "70", retireAge: "60", lifeAge: "85" },
    clicks: ["calc();var __r=document.getElementById('resultBox');document.getElementById('__tbProbe').textContent='C203RET0 '+((__retirement_calculatorScore('')===0&&String(__r.innerHTML||'').indexOf('年龄顺序无效')>=0)?'OK':'BAD');"],
    expect: ["C203RET0 OK"],
    ref: "第203批 退休拒绝态：age=70 时 calc 显示「年龄顺序无效」、清年度明细并返回（clearYearlyOutput），Score ⇒ 0，历史与导出不再冒充通过。",
  },
  {
    slug: "finance/word-wrap",
    inputs: { input: "abcd", width: "2", mode: "soft" },
    clicks: ["var __m=document.getElementById('mode'),__r=document.getElementById('result');document.getElementById('indent').checked=true;document.getElementById('hanging').checked=true;var __ok=true;['soft','hard','word','chinese'].forEach(function(m){__m.value=m;wrap();var __t=String(__r.textContent||'');if(__t.indexOf('宽度不足')<0&&__t.indexOf('Width is too small')<0)__ok=false;});document.getElementById('__tbProbe').textContent='C205WW '+(__ok?'OK':'BAD');"],
    expect: ["C205WW OK"],
    ref: "第205批 word-wrap：宽 2 且勾选首行/悬挂缩进时，四种模式旧实现均输出长度 3 的 ['  a','  b','  c','  d'] 超宽行；修复后统一在 width<=缩进宽 时明确提示并停止折行。四模式逐一 wrap 均须含「宽度不足」提示；旧源码不含 ⇒ BAD ⇒ 零逃生。",
  },
  {
    slug: "finance/word-wrap",
    inputs: { input: "abcd", width: "20", mode: "soft" },
    clicks: ["var __g=document.getElementById('input'),__w=document.getElementById('width'),__p=document.getElementById('__tbProbe');document.getElementById('indent').checked=false;document.getElementById('hanging').checked=false;var a=__word_wrapScore('');__w.value='2';document.getElementById('indent').checked=true;var b=__word_wrapScore('');__g.value='';var c=__word_wrapScore('');__p.textContent='C205WW3 '+((a===1&&b===0&&isNaN(c))?'OK':'BAD');"],
    expect: ["C205WW3 OK"],
    ref: "第205批 word-wrap Score 三态：正常折行 ⇒ 1、宽 2 带缩进拒绝态 ⇒ 0、清空输入 ⇒ NaN/MANUAL。修复后按真实控件状态判定、不再解析用户输入全文（折行工具输入可含 无效/Failed/Invalid 等任意词），旧全文词表会把这些正常输入误记未通过。",
  },
  {
    slug: "finance/word-wrap",
    inputs: { input: "中文测试", width: "3", mode: "soft" },
    clicks: ["document.getElementById('indent').checked=true;document.getElementById('hanging').checked=false;document.getElementById('countBytes').checked=true;wrap();var __t=String(document.getElementById('result').textContent||'');document.getElementById('__tbProbe').textContent='C205WWCP '+((__t.indexOf('说明')>=0||__t.indexOf('Note:')>=0)?'OK':'BAD');"],
    expect: ["C205WWCP OK"],
    ref: "第205批 单码点超宽：宽 3 + 首行缩进（可用宽 1）+ 按 UTF-8 字节计时，中文单码点 3 字节 > 可用宽度，takeByLen 的 i===0 兜底整码点输出（不拆代理项、不无进展）；修复后追加固定中英文「说明」，不静默输出超宽行。旧源码无该说明 ⇒ BAD。",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "1000000", rate: "4.2", years: "0.01" },
    clicks: ["calc();var __s=document.getElementById('summary'),__r=document.getElementById('res'),__b=document.querySelector('#schedule tbody');document.getElementById('__tbProbe').textContent='C210C4 '+((__calc_4Score('')===0&&(!__s||!__s.innerHTML)&&(!__b||!__b.innerHTML)&&(String(__r.innerHTML||'').indexOf('0 期')>=0||String(__r.innerHTML||'').indexOf('过短')>=0))?'OK':'BAD');"],
    expect: ["C210C4 OK"],
    ref: "第210批 贷款零期：years=0.01 → n=Math.round(0.12)=0，旧实现仍输出「首月还款 —/还款总额 0.00/0 期」并记通过；修复后 n<1 停算、清 summary 与 schedule tbody、写「贷款期限过短，舍入后为 0 期」提示，Score ⇒ 0。",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "1000000", rate: "4.2", years: "2.5" },
    clicks: ["var __g=document.getElementById('years'),__p=document.getElementById('__tbProbe');var a=__calc_4Score('');__g.value='0.01';var b=__calc_4Score('');__g.value='2.5';var c=__calc_4Score('');__p.textContent='C210C4CH '+((a===1&&b===0&&c===1)?'OK':'BAD');"],
    expect: ["C210C4CH OK"],
    ref: "第210批 贷款期限状态链：2.5 年（30 期）⇒ 1、0.01 年（0 期）⇒ 0、恢复 2.5 年 ⇒ 1。与上条拒绝态配合，三态不同值、恢复不残留。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { init: "100", rate: "15" },
    clicks: ["var __r=calcIRR(parseFloat(document.getElementById('init').value),[230,-132]);document.getElementById('__tbProbe').textContent='C156NPV '+((__r.status==='multiple'&&__r.rates.length===2)?'OK':'BAD');"],
    expect: ["C156NPV OK"],
    ref: "第156批 NPV 多根：init=100、现金流 230/-132 在 10% 与 20% 有两个 IRR 根，折现率 15% 下 NPV≈+0.189 仍可行。旧 calc 识别多根后写「存在多个根……无唯一解，不可行」与正 NPV「可行」自相矛盾；修复后多根明细改「单一 IRR 判据不适用，请改用 NPV / PI 判断可行性」，不再把多根等同不可行。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { init: "100", rate: "8" },
    clicks: ["var __r=calcIRR(parseFloat(document.getElementById('init').value),[100101]);document.getElementById('__tbProbe').textContent='C156NPVN '+((__r.status==='none')?'OK':'BAD');"],
    expect: ["C156NPVN OK"],
    ref: "第156批 范围外根：init=100、首期 100101 的数学 IRR=100001% 超出搜索上限 100000%，算法返回 none（no-root）。旧首屏摘要简写「无解」易被理解为数学上不存在解；修复后统计卡与明细改称「范围内未找到」并注明搜索区间，与全局无解区分。",
  },
  {
    slug: "finance/retirement-calculator",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/retirement-calculator.html','utf8');var i=h.indexOf('function clearYearlyOutput()');var s=i>=0?h.slice(i,i+260):'';var ok=s.indexOf(\"('yearlyTable')\")>=0&&s.indexOf(\"('sensitivityTable')\")>=0&&s.indexOf(\"sens.innerHTML = ''\")>=0;document.getElementById('__tbProbe').textContent='RETSENS '+(ok?'OK':'BAD');"],
    expect: ["RETSENS OK"],
    ref: "第1343批 清空残留：原 clearYearlyOutput 只清年度明细表，非法分支（年龄顺序无效/输入守卫）触发后敏感性分析表 #sensitivityTable 仍保留上一次合法计算旧数据，形成主结果报错+明细旧值矛盾；改为同步清空敏感性表。",
  },
  {
    slug: "finance/compound-interest",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/compound-interest.html','utf8');var i=h.indexOf('function resetDisplay()');var s=i>=0?h.slice(i,i+520):'';var ok=s.indexOf(\"getElementById('chart')\")>=0&&s.indexOf('getContext')>=0&&s.indexOf('clearRect')>=0;document.getElementById('__tbProbe').textContent='CMPCHART '+(ok?'OK':'BAD');"],
    expect: ["CMPCHART OK"],
    ref: "第1343批 清空残留：原 resetDisplay 清了数值卡与年度表但未擦除 canvas#chart 上旧柱状图（清空路径不触发 drawChart 的 clearRect）；改为清空时判空安全擦除画布。",
  },
  {
    slug: "finance/position-size-calculator",
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/position-size-calculator.html','utf8');var i=h.indexOf('if(!isFinite(ratio)||ratio<=0)');var s=i>=0?h.slice(i,i+180):'';var ok=s.indexOf('__psFail')>=0&&h.indexOf('currentResult = null;')>=0;document.getElementById('__tbProbe').textContent='POSSTAT '+(ok?'OK':'BAD');"],
    expect: ["POSSTAT OK"],
    ref: "第1344批 分支残留：凯利模式 ratio<=0 早退分支原只写 #res 就 return，#statGrid 保留上次合法计算的统计卡（martingale 分支有清，口径不一）；改为早退同步清空 statGrid。",
  },

{ slug:"finance/profit-margin-calculator", inputs:{"revenue":"","cogs":"","sellingExp":"","adminExp":"","rdExp":"","finExp":"","da":"","taxRate":"","revRev":"","targetMargin1":"","expRatio1":"","costCost":"","targetMargin2":"","taxRate2":"","batchStart":"","batchEnd":"","batchStep":"","batchM1":"","batchM2":"","batchM3":"","batchM4":"","dupontNI":"","dupontRev":"","dupontAssets":"","dupontEquity":""}, expect:["请填写必要的输入参数后再计算"], ref:"全部输入留空不得输出 0/0.00 假结果（NUMCLR）" },
  {
    slug: "finance/installment-real-rate",
    inputs: { P: "18000", n: "24", r: "0.6" },
    expect: ["14.10% 有效年化"],
    ref: "多期数并排：同一本金与每期费率下列出 6/12/24/36 期的每期还款、总手续费与有效年化；锁定功能不回退。"
  },

  {
    "slug": "finance/car-loan-calculator",
    "inputs": { "insYears": "3" },
    "expect": ["保险合计（3年）", "落地总价（首付+税费+3年保险+车船税+上牌）"],
    "ref": "保险年数口径：控件可选 1/2/3 年并按年数相乘，旧标题固定写「首年保险」；修复后标签随选择显示 3 年，落地总价说明同步补车船税。"
  },
  {
    "slug": "finance/loan-comparison",
    "inputs": { "a-principal": "100000", "a-rate": "4", "a-months": "60", "b-principal": "100000", "b-rate": "4", "b-months": "120" },
    "expect": ["月供最低： B 方案", "总利息最低： A 方案", "仅反映月现金流，不代表总成本最低"],
    "ref": "不同期数排名口径：B 期数更长月供更低，但总利息更高；旧实现把月供最少标成绿色「月供最少」，容易被当成最优。修复后同时给出月供最低与总利息最低，并明确前者不代表总成本。"
  },
  {
    "slug": "finance/loan-comparison",
    "inputs": { "a-principal": "100000", "a-rate": "4", "a-months": "60", "b-principal": "100000", "b-rate": "5", "b-months": "60", "c-principal": "100000", "c-rate": "6", "c-months": "60" },
    "expect": ["总利息最少： A 方案"],
    "ref": "同本金同期数：月供与总利息同序，直接以总利息最少作为结论；旧文案「月供最少」在相同条件下虽等价，但未点明比较维度。"
  },
{
  "slug": "finance/mortgage-calculator",
  "inputs": {"loanAmount": "100", "rate": "4.9", "years": "30", "downPayment": "30"},
  "clicks": ["var tb=document.getElementById('scheduleBody');var before=(tb.innerHTML.match(/<tr>/g)||[]).length;document.getElementById('scheduleToggle').fire('click');var after=(tb.innerHTML.match(/<tr>/g)||[]).length;var ok=before===24&&after===360;document.getElementById('__tbProbe').textContent='MCFULL '+before+'/'+after+(ok?' OK':' BAD');"],
  "expect": ["MCFULL 24/360 OK"],
  "ref": "30 年 360 期：默认只渲染前 24 期，点击‘显示全部期数’后应渲染 360 行；旧版无切换按钮且固定 slice(0,24)。"
},


{ slug:"finance/lease-payment-calculator", inputs:{pv:"100000",downPct:"0",rate:"6",months:"36",fv:"0",fee:"100000",type:"equal",timing:"end"}, clicks:["calc()"], expect:["不可计算（净融资额或现金流无有效 IRR）"], ref:"租赁物 100000、首付 0、手续费 100000 ⇒ 净融资额 0，后续付款全为正、现金流无符号变化，IRR 无解；旧实现 calcIRR 返回 NaN 后仍 toFixed 输出 NaN%。" },
{ slug:"finance/lease-payment-calculator", inputs:{pv:"100000",downPct:"0",rate:"0",months:"12",fv:"0",fee:"0",type:"equal",timing:"end"}, clicks:["calc()"], expect:["名义年化（月 IRR × 12）： 0.00%"], ref:"名义利率 0、无手续费、12 期等额还款：现金流 −100000 后按月收回，IRR=0，应输出 0.00% 而非不可计算；防止无解守卫误伤合法零利率。" },
  {
    slug: "finance/dca-calculator",
    inputs: { monthly: "0", years: "1", rate: "12", initial: "12000", target: "0" },
    clicks: ["switchTiming('begin')","calc()"],
    expect: ["期末总资产： ¥13,521.90", "累计收益： +¥1,521.90"],
    ref: "第731C批：monthly=0、initial=12000、1 年、12% 期初复利 ⇒ 12000×1.01^12=13,521.90，收益 1,521.90；旧守卫把 monthly 当分母拒绝 0，导致初始本金单独增长也无法计算。默认 monthly=1000 ⇒ 不命中。"
  },
  {
    slug: "finance/sharpe-ratio",
    inputs: { returns: "5\n5", riskFree: "0", annualize: "1" },
    clicks: ["calc()"],
    expect: ["标准差必须大于 0：当前 2 个收益率全部相同"],
    ref: "第731C批：序列 5,5 标准差为 0，旧实现把夏普直接置 0 并评级；现拒绝并清空统计卡，说明夏普无定义。默认收益序列有波动 ⇒ 不命中。"
  },
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "12abc", batchInput: "100\n12abc\n1,234.56" },
    clicks: ["calc();calcBatch()"],
    expect: ["金额不是有效数字", "第 2 行「12abc」", "不是有效金额", "1,234.56"],
    ref: "第731C批：主分支 12abc 旧 parseFloat 得 12；现严格拒绝。批量第 2 行 12abc 标红且不换算，合法千分位 1,234.56 仍正常。默认金额合法 ⇒ 不命中。"
  },
  {
    slug: "finance/gold-price-calculator",
    inputs: { goldPrice: "650", usdRate: "", discountRate: "95", weightInput: "", totalInput: "6500", puritySel: "0.9999", weightUnit: "g" },
    clicks: ["calcAll()"],
    expect: ["黄金重量不能为空", "美元金额未计算（美元汇率留空）"],
    ref: "第731C批：重量留空旧实现按 0 克显示 ¥0；现明确报空值。美元汇率留空不得显示 $0，改为未计算。默认重量 10、汇率 7.25 ⇒ 不命中。"
  },
  {
    slug: "finance/gold-price-calculator",
    inputs: { goldPrice: "0", usdRate: "7.25", discountRate: "95", weightInput: "10", totalInput: "6500", puritySel: "0.9999", weightUnit: "g" },
    clicks: ["calcAll()"],
    expect: ["黄金单价必须大于 0"],
    ref: "第731C批：金价为 0 时反算重量会出现除零；现前置拒绝并说明，不输出 0 克/零元。默认金价 650 ⇒ 不命中。"
  },
  {
    slug: "finance/investment-roi",
    inputs: { monthly: "1000", freq: "monthly", annualRate: "-12", period: "1" },
    clicks: ["calcRegular()"],
    expect: ["-752.1"],
    ref: "第731C批：定投年化 -12%、月投 1000、1 年 ⇒ 期初投入终值 11,247.9、累计投入 12,000、亏损 752.1；旧模板固定加 + 号并上绿色，现按亏损显示负号/红色。默认 8% 正收益 ⇒ 不命中。",
  },
  {
    slug: "finance/number-to-words-chinese",
    inputs: { inputVal: "10010" },
    clicks: ["convert()"],
    expect: ["一万零一十"],
    ref: "中文读数分组十位：10010 = 一万 + 零一十；仅整个数的最高读法才省略「一」，分组内部保留 ⇒ 一万零一十（旧实现一万零十）。",
  },
  {
    slug: "finance/number-to-words-chinese",
    inputs: { inputVal: "1.00009" },
    clicks: ["convert()"],
    expect: ["一点零零零零九"],
    ref: "小数按输入字符串逐位读、保留末尾零：1.00009 ⇒ 一点零零零零九，不四舍五入/截断（旧实现四点位后四舍五入得一点零零零一）。",
  },
  {
    slug: "finance/currency-converter",
    inputs: { rateMode: "manual", manualRate: "", fromAmount: "100" },
    clicks: ["calc()"],
    expect: ["手动汇率必须是大于 0 的有效数字"],
    ref: "手动模式空汇率必须阻止换算并提示，不能静默回退内置表；结果区不得出现内置汇率换算金额。",
  },
  {
    slug: "finance/currency-converter",
    inputs: { rateMode: "manual", manualRate: "7", fromAmount: "100" },
    clicks: ["calc();swapCurrencies();document.getElementById('__tbProbe').textContent='CCSWAP '+document.getElementById('manualRate').value+' '+document.getElementById('toAmount').value;"],
    expect: ["CCSWAP 0.142857142857 14.2857"],
    ref: "手动汇率 1 CNY=7 USD，交换后 1 USD=1/7 CNY；100 USD ⇒ 14.2857 CNY。交换只换币种不取倒数会把 100 USD 算成 700 CNY。",
  },
  {
    slug: "finance/currency-converter",
    inputs: { rateMode: "manual", manualRate: "0.138", fromAmount: "200" },
    clicks: ["var __st={};globalThis.localStorage={getItem:function(k){return __st[k]==null?null:__st[k]},setItem:function(k,v){__st[k]=String(v)},removeItem:function(k){delete __st[k]}};calc();saveHistory();var h=JSON.parse(localStorage.getItem('currency_history:finance'))[0];document.getElementById('rateMode').value='builtin';document.getElementById('manualRate').value='9';renderHistory();document.getElementById('__tbProbe').textContent='CCHIST '+h.rateSource+' '+h.rate+' '+h.result+' '+((String(document.getElementById('historyList').innerHTML).indexOf('27.6000')>=0)?'SAVED':'LIVE');"],
    expect: ["CCHIST manual 0.138 27.6 SAVED"],
    ref: "历史必须保存当次汇率来源、汇率和结果；切回内置/改手动汇率后列表仍显示保存值 27.6000，而不是按当前汇率重算。",
  },
  {
    slug: "finance/currency-converter",
    clicks: ["globalThis.TBKit={util:{isEn:function(){return true;}}};document.getElementById('batchFromSearch').value='Yen';filterOptions('batchFrom');var t=String(document.getElementById('batchFromOptions').innerHTML);document.getElementById('__tbProbe').textContent='CCNAME '+(t.indexOf('Japanese Yen')>=0?'YEN':'MISS')+' '+(t.indexOf('日元')<0?'CLEAN':'ZH');"],
    expect: ["CCNAME YEN CLEAN"],
    ref: "第933批：英文态货币列表使用英文名称，搜索 Yen 命中 Japanese Yen，且不再渲染中文「日元」。默认中文态不命中。",
  },
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "5000", rateMode: "manual", manualRate: "7.25", presetFromCurrency: "USD", presetToCurrency: "CNY", presetBatchFromCurrency: "USD", presetBatchToCurrency: "CNY" },
    clicks: ["__ccApplyPresetCurrencies();var t=String(document.getElementById('resultDisplay').innerHTML).replace(/,/g,'');document.getElementById('__tbProbe').textContent='CCPRESET '+(t.indexOf('36250')>=0?'OK':'BAD');"],
    expect: ["CCPRESET OK"],
    ref: "第934批：5000 美元换人民币预设同时设置源/目标币与 7.25 手动汇率，结果 5000×7.25=36250；旧预设只改金额/汇率，默认 CNY→USD 会把 7.25 算成 1 CNY=7.25 USD。",
  },
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "100", batchInput: "100", rateMode: "manual", manualRate: "7" },
    clicks: ["calcBatch();var d1=String(document.getElementById('batchResult').innerHTML);document.getElementById('manualRate').value='8';calc();var d2=String(document.getElementById('batchResult').innerHTML);var csv='';ToolBox.downloadText=function(n,c){csv=String(c);};exportBatchCSV();document.getElementById('__tbProbe').textContent='CCSYNC '+(d1.indexOf('700.0000')>=0?'OLD':'NO')+' '+(d2.indexOf('800.0000')>=0?'NEW':'NO')+' '+(csv.indexOf('800.0000')>=0?'CSV':'BAD');"],
    expect: ["CCSYNC OLD NEW CSV"],
    ref: "第933批：批量表随单笔手动汇率变化同步重算；改 7→8 后屏幕与导出都使用 800.0000，不再出现屏幕 700、导出 800 的分叉。默认内置汇率不命中。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "100000", salvage: "-5000", life: "5" },
    clicks: ["var msg='';var old=ToolBox.showToast;ToolBox.showToast=function(m){msg=String(m);};exportCSV();document.getElementById('__tbProbe').textContent='DEPBLOCK '+msg;"],
    expect: ["DEPBLOCK 导出已阻止：请确保原值 > 残值 ≥ 0"],
    ref: "CSV 导出必须复用页面残值校验：负残值阻断导出并说明原因，不再输出负折旧/错误净值。",
  },
  {
    slug: "finance/credit-card-interest",
    inputs: { billAmount: "5", dailyRate: "0", minRatio: "100", repayType: "minimum" },
    clicks: ["calc()"],
    expect: ["5.00 首月最低还款"],
    ref: "账单 5 元、日利率 0、最低比例 100%：首月最低还款取模拟明细首期付款 5.00（本金+利息上限），不能显示 10 元下限。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { revenue: "0", cogs: "500" },
    clicks: ["calc()"],
    expect: ["未定义 毛利率 毛利润 -500.00"],
    ref: "收入为 0 时毛利率等比率分母为 0，显示未定义并保留可计算利润金额 -500.00；不能显示 0%。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: { years: "10.5" },
    clicks: ["calc()"],
    expect: ["定投年限须为 1–50 的整数年"],
    ref: "定投年限不得静默夹到 1–50 或向下取整：10.5 年明确拒绝，并清空当前结果。",
  },
  {
    slug: "finance/investment-calculator",
    inputs: { initial: "10000", final: "", years: "5", additional: "0" },
    clicks: ["calc()"],
    expect: ["请填写期末价值"],
    ref: "期末价值留空必须提示补全，不能按 0 计算成全部亏损；显式输入 0 才走 -100% 分支。",
  },
  {
    slug: "finance/investment-calculator",
    inputs: { initial: "10000", final: "0", years: "5", additional: "0" },
    clicks: ["calc()"],
    expect: ["年化收益率 CAGR： -100.00%"],
    ref: "期末价值显式填 0 合法：CAGR = -100.00%，与留空未填写区分。",
  },
  {
    slug: "finance/investment-calculator",
    inputs: { initial: "10000", final: "18000", years: "0.000000001", additional: "0" },
    clicks: ["calc()"],
    expect: ["数值超出可计算范围"],
    ref: "极短年限 + 1.8 倍回报使 expm1(log(1.8)/1e-9) 溢出；必须拒绝并禁止保存/导出，不能显示破折号却标记有效。",
  },
  {
    slug: "finance/irr-calculator",
    inputs: {},
    clicks: ["cashFlows=[{period:0,amount:-100,label:'T0'},{period:1,amount:200,label:'T1'},{period:2,amount:-100,label:'T2'}];renderFlows();calc();document.getElementById('__tbProbe').textContent='IRRROOT '+document.getElementById('irrValue').textContent;"],
    expect: ["IRRROOT 0.00%"],
    ref: "现金流 -100/200/-100 的 NPV = -100r²/(1+r)²，在 r=0 处与零轴相切；旧实现只找变号区间会报无零点。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: {},
    clicks: ["cashFlows=[-100,50,60];renderCashFlows();document.getElementById('__tbProbe').textContent='NPVSNAP '+document.getElementById('npvFlowSnapshot').value;"],
    expect: ["NPVSNAP -100|50|60"],
    ref: "现金流变更后必须写入完整有序快照，供历史恢复重建期数。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: {},
    clicks: ["var cb;TBKit={util:{isEn:function(){return false},diffBox:function(){}},matrix:{table:function(){}},history:{list:function(){return [{t:Date.now(),d:{npvFlowSnapshot:'-100|50|60|70',__tbScore:1,'结果':'x'}}]},mount:function(s,fn){cb=fn},last:function(){return null}},chart:{line:function(){}}};__npv_calculatorRender(['npvFlowSnapshot'],'结果',false);cb({npvFlowSnapshot:'-100|50|60|70'});document.getElementById('__tbProbe').textContent='NPVREST '+document.getElementById('npvFlowSnapshot').value;"],
    expect: ["NPVREST -100|50|60|70"],
    ref: "历史恢复必须按快照重建 4 期，而不是只更新当前页面已有 cf_ 输入；第4期必须出现。",
  },
  {
    slug: "finance/analysis-cost-1",
    inputs: { total: "100", rows: "A,1\nB,1\nC,1", dec: "2", outQty: "" },
    clicks: ["calc()"],
    expect: ["分摊额明细相加为 99.99 元"],
    ref: "100 元平均分给 3 项、显示两位各 33.33，显示明细合计 99.99 与总成本 100.00 差 0.01；必须检测显示精度差异。",
  },
  {
    slug: "finance/analysis-cost-1",
    inputs: { total: "100", rows: "A,1\nB,1\nC,1", dec: "2", outQty: "" },
    clicks: ["document.getElementById('tailAdjust').checked=true;calc()"],
    expect: ["明细合计与总成本一致"],
    ref: "启用尾差处理后最后一项调整为 33.34，显示明细合计 = 100.00，并明确提示。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "sp-total": "100", "sp-limit": "34", "sp-method": "equal", "sp-type": "total" },
    clicks: ["currentMethod='split';calc();document.getElementById('__tbProbe').textContent='INVEQ '+currentResult.invoices.map(function(i){return i.amount.toFixed(2)}).join(',')+'|'+currentResult.sumTotal.toFixed(2);"],
    expect: ["INVEQ 33.34,33.33,33.33|100.00"],
    ref: "100 元按 34 限额均分为 3 张：按分分配余数 ⇒ 33.34+33.33+33.33=100.00，三张均 ≤34；旧实现 33.33×3 显示合计 99.99。",
  },
  {
    slug: "finance/invoice-generator",
    inputs: { "sp-total": "10500", "sp-limit": "10000", "sp-method": "lastsmall", "sp-type": "total" },
    clicks: ["currentMethod='split';calc();document.getElementById('__tbProbe').textContent='INVLAST '+currentResult.invoices.length+' '+Math.max.apply(null,currentResult.invoices.map(function(i){return i.amount}));"],
    expect: ["INVLAST 2 10000"],
    ref: "总额 10500、限额 10000 的最后一张较小模式必须拆成 10000+500，任何一张都不得超过限额；旧实现因 1.1 倍阈值直接输出 10500 一张。",
  },
  {
    slug: "finance/loan-comparison",
    inputs: { "a-principal": "100000", "a-rate": "101", "a-months": "12", "b-principal": "100000", "b-rate": "0", "b-months": "12" },
    clicks: ["calc()"],
    expect: ["年利率须在 0%–100% 之间", "8333.33"],
    ref: "利率 101% 超出合理范围被排除；0% 仍合法，B 方案月供 100000/12 = 8333.33。",
  },
  {
    slug: "finance/bond-yield-calculator",
    inputs: { "y-price": "" },
    clicks: ["switchTab('formula', document.querySelectorAll('.tab-btn')[1]);document.getElementById('__tbProbe').textContent='BONDTAB '+(document.getElementById('tabFormula').classList.contains('active')?'OK':'BAD');"],
    expect: ["BONDTAB OK"],
    ref: "公式标签不依赖当前计算模式输入；隐藏的 y-price 留空也不能阻断 tab 切换。",
  },
  {
    slug: "finance/word-wrap",
    inputs: { input: "😀中A", width: "1" },
    clicks: ["document.getElementById('countBytes').checked=false;wrap();"],
    expect: ["😀", "中", "A"],
    ref: "第931批：字符模式按字素簇/码点切分，宽度 1 时单个 emoji 保持完整，不再把代理对拆成两行。"
  },
  {
    slug: "finance/shebeizulinfeilvjisuan",
    inputs: { price: "100", months: "12", depYears: "1", maintRate: "12", profitRate: "0", salvageRate: "0" },
    clicks: ["calc()"],
    expect: ["维护费用合计 (元)", "净收益 (元，已扣维护与购置)", "¥0.00"],
    ref: "第931批：净收益按租金 + 残值 − 购置 − 租期内维护支出计算；原值100、租12月、维护12%、零利润时净收益为0，不再误报12。"
  },
  {
    slug: "finance/shebeizulinfeilvjisuan",
    clicks: ["document.getElementById('price').value='0';document.getElementById('months').value='12';document.getElementById('depYears').value='1';calc();saveHistory();var k=historyKey();var n=JSON.parse(localStorage.getItem(k)||'[]').length;document.getElementById('__tbProbe').textContent='RENTBAD '+n;"],
    expect: ["RENTBAD 0"],
    ref: "第931批：历史保存复用完整计算校验；原值为 0 时计算已拒绝，不再把无效方案写入历史。"
  },
  {
    slug: "finance/word-frequency",
    inputs: { input: "a a b", topN: "1", minLen: "1" },
    clicks: ["document.getElementById('enOnly').checked=true;document.getElementById('zhOnly').checked=false;document.getElementById('filterStopwords').checked=false;analyze();"],
    expect: ["(66.67%)", "全部词次（3）为分母"],
    ref: "第931批：词条百分比以过滤后全部词次为分母；Top N=1 时 a 出现 2/3 仍显示 66.67%，不因只展示 1 条变成 100%。"
  },
  {
    slug: "finance/word-frequency",
    inputs: { input: "a cat dog", topN: "5", minLen: "3" },
    clicks: ["document.getElementById('enOnly').checked=true;document.getElementById('zhOnly').checked=false;analyze();"],
    expect: ["cat", "dog", "总词次"],
    ref: "第931批：英文分词同样应用最小词长；minLen=3 时 a 被过滤，只统计 cat/dog。"
  }
,
  {
    slug: "finance/word-search",
    inputs: { level: "easy", theme: "colors", customWords: "" },
    clicks: ["start();var g=document.getElementById('grid'),w=document.getElementById('words');document.getElementById('__tbProbe').textContent='WS10 '+((SIZE===10&&WORDS_PER_GAME===6&&words.length===6)?'OK':'BAD')+' size='+SIZE+' words='+words.length;"],
    expect: ["WS10 OK"],
    ref: "第931批：难度选择驱动网格与词数；easy=10×10/6 词，颜色主题词库。旧实现固定 12×12、8 词且无难度控件，必 BAD。"
  },
  {
    slug: "finance/word-search",
    inputs: { level: "medium", theme: "colors", customWords: "ab\n1\n_x" },
    clicks: ["start();var g=document.getElementById('grid');document.getElementById('__tbProbe').textContent='WSBAD '+((document.getElementById('output').textContent.indexOf('没有有效英文单词')>=0&&(g.children?g.children.length:0)===0)?'OK':'BAD');"],
    expect: ["WSBAD OK"],
    ref: "第931批：自定义词表过滤掉少于 3 个字母或非英文的项；全无效时不生成矩阵并给出明确提示，不静默回退主题词库。"
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "+86 13800138000" },
    clicks: ["var src=String(__msisdn_validatorExtras);var oi=src.indexOf('__histOptIn'),ck=src.indexOf('!opt.checked'),rr=src.indexOf('history.record'),mk=src.indexOf('MaskText(res');document.getElementById('__tbProbe').textContent='MSNOHIST '+((oi>=0&&ck>oi&&rr>ck&&mk>=0)?'OK':'BAD')+' g='+oi+','+ck+','+rr+','+mk;"],
    expect: ["MSNOHIST OK"],
    ref: "第931批：通信标识默认不持久化；未勾选保存选项时验证后历史必须为 0 条。旧实现 validate 后自动 record，必 BAD。"
  },
  {
    slug: "finance/imsi-validator",
    inputs: {},
    clicks: ["var src=String(__imsi_validatorExtras);var oi=src.indexOf('__histOptIn'),ck=src.indexOf('!opt.checked'),rr=src.indexOf('history.record'),mk=src.indexOf('MaskText(res');document.getElementById('__tbProbe').textContent='IMSINOHIST '+((oi>=0&&ck>oi&&rr>ck&&mk>=0)?'OK':'BAD')+' g='+oi+','+ck+','+rr+','+mk;"],
    expect: ["IMSINOHIST OK"],
    ref: "第931批：IMSI 页面默认不写历史；未勾选时长度 0。"
  },
  {
    slug: "finance/iccid-validator",
    inputs: {},
    clicks: ["var src=String(__iccid_validatorExtras);var oi=src.indexOf('__histOptIn'),ck=src.indexOf('!opt.checked'),rr=src.indexOf('history.record'),mk=src.indexOf('MaskText(res');document.getElementById('__tbProbe').textContent='ICCIDNOHIST '+((oi>=0&&ck>oi&&rr>ck&&mk>=0)?'OK':'BAD')+' g='+oi+','+ck+','+rr+','+mk;"],
    expect: ["ICCIDNOHIST OK"],
    ref: "第931批：ICCID 页面默认不写历史；未勾选时长度 0。"
  },
  {
    slug: "finance/imei-validator",
    inputs: {},
    clicks: ["var src=String(__imei_validatorExtras);var oi=src.indexOf('__histOptIn'),ck=src.indexOf('!opt.checked'),rr=src.indexOf('history.record'),mk=src.indexOf('MaskText(res');document.getElementById('__tbProbe').textContent='IMEINOHIST '+((oi>=0&&ck>oi&&rr>ck&&mk>=0)?'OK':'BAD')+' g='+oi+','+ck+','+rr+','+mk;"],
    expect: ["IMEINOHIST OK"],
    ref: "第931批：IMEI 页面默认不写历史；未勾选时长度 0。"
  },
  {
    slug: "finance/msisdn-validator",
    inputs: { input: "+86 13800138000" },
    clicks: ["var t=__msisdn_validatorMaskText('输入 +86 13800138000 归一化 8613800138000',['+86 13800138000']);document.getElementById('__tbProbe').textContent='MSMASK '+((t.indexOf('13800138000')<0&&t.indexOf('8613800138000')<0&&t.indexOf('86****8000')>=0)?'OK':'BAD')+' '+t;"],
    expect: ["MSMASK OK"],
    ref: "第931批：显式勾选后历史只存脱敏值 13****8000，完整号码 13800138000 与归一化 8613800138000 均不得出现在历史序列化结果里，输入字段为 86****8000。"
  }

,
  {
    slug: "finance/futures-pnl-calculator",
    inputs: {},
    clicks: ["var __st={};globalThis.localStorage={getItem:function(k){return __st[k]||null},setItem:function(k,v){__st[k]=String(v)},removeItem:function(k){delete __st[k]}};globalThis.ToolBox={formatNumber:function(v,d){return Number(v).toFixed(d).replace(/\B(?=(\d{3})+(?!\d))/g,',')},showToast:function(){},toggleToolTheme:function(){}};localStorage.setItem('futures_trades',JSON.stringify([{code:'IF',contract:'沪深300股指期货',direction:1,openPrice:3000,closePrice:3010,lots:2,multiplier:100,marginRate:12,openFee:20,closeFee:20}]));loadTrade(0);var g=String(document.getElementById('resultGrid').innerHTML),c=String(document.getElementById('contractName').textContent);document.getElementById('__tbProbe').textContent='FUTMULT '+(currentContract.multiplier===100&&c.indexOf('历史乘数 100')>=0&&g.replace(/,/g,'').indexOf('1920.00')>=0?'OK':'BAD')+' m='+currentContract.multiplier;"],
    expect: ["FUTMULT OK"],
    ref: "第932批：历史交易保存的合约乘数为 100，内置 IF 当前乘数为 300；恢复历史必须用保存值 100。开平仓 3000→3010、2 手、双边手续费各 20 ⇒ 盈亏 10×100×2−80=1,920.00。旧实现按当前 300 算得 5,920.00，必 BAD。"
  },
  {
    slug: "finance/loan-amortization",
    inputs: { prepayMonth: "", prepayAmount: "100000" },
    clicks: ["document.getElementById('prepayCard').style.display='block';calcPrepay();var a=String(document.getElementById('prepayResult').innerHTML);document.getElementById('prepayMonth').value='0';calcPrepay();var b=String(document.getElementById('prepayResult').innerHTML);document.getElementById('__tbProbe').textContent='LAPM '+(a.indexOf('请输入提前还款期数')>=0&&a.indexOf('不会默认按第 1 期')>=0&&b.indexOf('1 至最后一期之前的整数')>=0?'OK':'BAD');"],
    expect: ["LAPM OK"],
    ref: "第932批：提前还款期数留空/填 0 不得被 `||1` 静默当首期；空串给「不会默认按第 1 期」提示，0 给范围提示。旧实现两者都按第 1 期直接生成方案，两个提示均不出现 ⇒ BAD。"
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "10000", rate: "6", years: "10", annual: "0" },
    clicks: ["document.getElementById('freq').value='12';calc();var fv=window.__ciLast.totalFV;var box=String(document.getElementById('__charCiVal').textContent);document.getElementById('__tbProbe').textContent='CIDEEP '+((box.indexOf('¥'+Math.round(fv))>=0&&String(document.getElementById('__charCiRows').innerHTML).indexOf('12 次/年')>=0)?'OK':'BAD')+' fv='+fv;"],
    expect: ["CIDEEP OK"],
    ref: "第932批：解读模块必须复用主结果——月复利、定投 0 时，解读终值应与主结果 totalFV 一致并标出 12 次/年。旧 __finUpdate 自行按年复利 P(1+r)^t 计算（10,000×1.06^10≈17,908），主结果月复利≈18,194，必 BAD。"
  },
  {
    slug: "finance/car-loan-calculator",
    inputs: { price: "200000", downPct: "20", rate: "60", years: "5" },
    clicks: ["calculate();var a=String(document.getElementById('monthlyPay').textContent);var v=__car_loan_calculator_valid;document.getElementById('__tbProbe').textContent='CARMAX '+((a==='--'&&v===false)?'OK':'BAD')+' pay='+a+' valid='+v;"],
    expect: ["CARMAX OK"],
    ref: "第932批：年利率 60% 超出 0–50% 合理输入范围，必须清空结果、valid=false，导出入口也不得放行。旧实现只校验 >=0，60% 仍算出月供并允许导出 ⇒ BAD。"
  },
  {
    slug: "finance/routing-number-validator",
    inputs: { input: "310000004" },
    clicks: ["validate();var o=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent='RT31 '+(o.indexOf('储蓄机构前缀（对应美联储第 11 区）')>=0&&o.indexOf('只说明 9 位数字结构自洽')>=0?'OK':'BAD');"],
    expect: ["RT31 OK"],
    ref: "第932批：前缀 21–32 属储蓄机构号段，31 对应美联储第 11 区（21→1…31→11），不能写成 Michigan/Ohio 等州名；校验通过只声明 3-7-1 加权模 10 结构自洽，不判机构有效。旧映射把 31 写成 New York (Thrift)、结论「路由号码有效」⇒ BAD。"
  },
  {
    slug: "finance/routing-number-validator",
    inputs: { input: "610000005" },
    clicks: ["validate();var o=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent='RT61 '+(o.indexOf('电子交易标识（对应美联储第 1 区）')>=0&&o.indexOf('Paris')<0?'OK':'BAD');"],
    expect: ["RT61 OK"],
    ref: "第932批：前缀 61–72 是电子交易标识号段（61→第 1 区），不是 Paris/FR；旧映射把 61 写成 Paris (FR) 属明显错误。"
  },
  {
    slug: "finance/routing-number-validator",
    inputs: { input: "990000000" },
    clicks: ["validate();var o=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent='RTUNK '+((o.indexOf('不在公开分配范围')>=0&&o.indexOf('无法判断该号码是否已分配')>=0&&o.indexOf('不能确认号码已分配')<0)?'OK':'BAD');"],
    expect: ["RTUNK OK"],
    ref: "第932批：未知前缀 99 校验和虽通过，也只能说「不在公开范围、无法判断是否已分配」，不得直接判无效、也不得判有效；旧实现输出「未分配/非法，路由号码无效」⇒ BAD。"
  },

  // ===== 第935批新增 =====
  {
    slug: "finance/npv-calculator",
    inputs: { rate: "", init: "10000" },
    clicks: ["calc()"],
    expect: ["请填写折现率（如确为 0，请输入 0）"],
    ref: "第935批：折现率留空不再按 0% 计算，明确提示补全并清除结果；显式 0 仍合法。默认 8% ⇒ 不命中。",
  },
  {
    slug: "finance/npv-calculator",
    inputs: { rate: "8", init: "10000" },
    clicks: ["updateCF(0, '')"],
    expect: ["第 1 期现金流未填写（如确为 0，请明确输入 0）"],
    ref: "第935批：现金流留空不再保存为 0；提示具体期数。已有用例 updateCF(3,0) 覆盖显式 0 合法。",
  },
  {
    slug: "finance/simple-interest",
    inputs: { principal: "10000", rate: "", years: "3" },
    clicks: ["calc()"],
    expect: ["请填写年利率和期限（如确为 0，请明确输入 0）"],
    ref: "第935批：利率留空不再按 0 计算，提示补全并清除旧结论；显式 0 利率仍走正常计算。",
  },
  {
    slug: "finance/currency-symbol",
    inputs: {},
    clicks: ["var i=-1;for(var k=0;k<currencies.length;k++){if(currencies[k].code==='CLF'){i=k;break;}}showDetail(i);"],
    expect: ["暂无数据（无辅单位）", "不适用（无辅单位换算关系）"],
    ref: "第935批：CLF 无辅单位时详情显示暂无数据，换算比例显示不适用，不再输出「1 Unidad de Fomento = 1」空单位等式。",
  },
  {
    slug: "finance/assessor-manager",
    inputs: { debtRatio: "55", currentRatio: "1.8", revenue: "5000", profitMargin: "12", overdue: "1", creditHistory: "5" },
    clicks: ["calc()"],
    expect: ["教学示例，不是真实信用评估。", "示例输入与分项得分", "示例授信算术", "本页不输出催收阶段"],
    ref: "第935批：固定分档累加改为教学示例，展示六项得分与假设；删除授信审批与催收动作结论。",
  },
  {
    slug: "finance/text-reverse-words",
    inputs: { input: "hello, world!", mode: "space" },
    clicks: ["document.getElementById('keepPunc').checked=true;reverse();"],
    expect: ["world, hello!"],
    ref: "第935批：保留标点时单词、空白、标点分开识别；hello, world! 反转后标点原位，为 world, hello!（旧实现标点跟随词移动）。",
  },
  {
    slug: "finance/text-reverse-words",
    inputs: { input: "a👨‍👩‍👧‍👦b", mode: "allchar" },
    expect: ["b👨‍👩‍👧‍👦a"],
    ref: "第935批：所有字符反转按 Unicode 字素簇处理，家庭 emoji 的 ZWJ 序列不被拆成代理项乱码；旧 split('') 会破坏该 emoji。",
  },
  {
    slug: "finance/installment-real-rate",
    inputs: { P: "1000", n: "6", r: "100" },
    clicks: ["calcTool()"],
    expect: ["未求解（月 IRR 超出 100% 上限"],
    ref: "第935批：期数对比复用主结果求根与残差校验；本金 1000、6 期、每期费率 100% 时真实月 IRR 超出 100% 区间，对比表不再展示截断年化。",
  },
  {
    slug: "finance/analysis-risk",
    inputs: { s: "1000000", v: "600000", f: "100000", i: "50000", t: "101", n: "100000", dec: "2" },
    clicks: ["calc()"],
    expect: ["所得税税率须在 0%–100% 之间（当前 101%），已停止计算且不自动截断。"],
    ref: "第935批：税率 101% 不再静默截到 100%，提示越界并停止；输入框仍保留 101，结果区不再给杠杆结论。",
  },
  {
    slug: "finance/analysis-risk",
    inputs: { s: "1000000", v: "600000", f: "100000", i: "50000", t: "", n: "100000", dec: "2" },
    clicks: ["calc()"],
    expect: ["所得税税率未填写，已停止计算；如确为 0，请明确输入 0。"],
    ref: "第935批：税率留空与显式 0 分开处理；空值提示具体字段并停止，0% 仍可正常计算。",
  },
  {
    slug: "finance/rental-yield-calculator",
    inputs: { price: "300", area: "80", rent: "5000", fee: "300", heat: "2400", decor: "5000", repair: "1000", agency: "0", tax: "2000", loanRatio: "70", loanRate: "4.2", loanYears: "30" },
    clicks: ["document.getElementById('loanType').value='principal';loanEnabled=true;calc()"],
    expect: ["首月月供", "首月月供后现金流", "末月"],
    ref: "第935批：等额本金月供逐月递减，卡片改标首月月供、末月与平均值；旧实现把首月值当通用月供与现金流。",
  },
  // ===== 第936批新增 =====
  {
    slug: "finance/lease-payment-calculator",
    inputs: { pv: "100000", downPct: "20", rate: "6", months: "36", fv: "0", fee: "0", type: "principal", timing: "begin" },
    clicks: ["calc()"],
    expect: ["期初还款仅支持等额本息；等额本金与先息后本请选择期末还款。"],
    ref: "第936批：期初模式不再对等额本金/先息后本生成与 IRR 口径不一致的明细；不支持组合明确拒绝并清空结果。等额本息期初仍由既有 10.03% 用例覆盖。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { dupontNI: "150000", dupontRev: "0", dupontAssets: "2000000", dupontEquity: "800000" },
    clicks: ["calcDupont()"],
    expect: ["销售净利率： 未定义", "营业收入为 0", "不能用 0% 代替"],
    ref: "第936批：营业收入 0 时销售净利率未定义，不再显示 0.00%；ROE 仍按净利润/净资产独立计算，不把无关分母的 0 传播成结论。",
  },
  {
    slug: "finance/profit-margin-calculator",
    inputs: { dupontNI: "150000", dupontRev: "1000000", dupontAssets: "2000000", dupontEquity: "0" },
    clicks: ["calcDupont()"],
    expect: ["净资产收益率（ROE）： 未定义", "平均净资产为 0，权益乘数与 ROE 未定义", "不输出盈利能力或杠杆高低结论"],
    ref: "第936批：零净资产时 ROE/权益乘数未定义，停止盈利能力与杠杆结论；资产负债率仍按 (资产−负债)/资产 显示 100%。",
  },
  {
    slug: "finance/discount-calculator",
    inputs: { price: "100" },
    clicks: ["updateDiscount(0, 8);calc();toTaxFromDiscount();"],
    expect: ["¥ 90.40 税后金额", "¥ 10.40 税额（13%）"],
    ref: "第936批：折扣结果新增「转入含税计算」按钮；100 元 8 折=80 元，按税前加税 13% 得 90.40，兑现页面介绍的回填能力。旧实现 setMode(2) 只重建默认输入。",
  },
  {
    slug: "finance/credit-card-type",
    inputs: { input: "4111111111111111" },
    clicks: ["validate()"],
    expect: ["输入数字（已脱敏）： 411111 •••• •••• 1111"],
    ref: "第936批：结果与历史快照不再回显完整卡号，只保留前 6 位 BIN 与后 4 位；旧实现输出 16 位原文并存入历史。",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "1000000", rate: "4.2", years: "30" },
    clicks: ["calc()"],
    expect: ["已省略", "全部 360 期", "第 360 期"],
    ref: "第936批：明细表明确标注第 13–359 期省略并提示完整 CSV；内部与隐藏导出表保存全部 360 期，汇总与明细同源。旧表只存前 12+末期且无省略说明。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "f-capital": "100000", "f-percent": "10", "f-price": "50", "f-stop": "60" },
    clicks: ["switchMethod('fixed');calc();"],
    expect: ["止损价须低于买入价；本工具仅支持做多", "❌ 止损价须低于买入价"],
    ref: "第936批：固定比例模式校验买入/止损关系，止损价高于买入价时拒绝并清空 currentResult/统计/图表，保存按钮随即失效；旧实现显示负风险。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { aCost: "1000", aRate: "0", aYears: "0.5", aAdd: "100", bCost: "1000", bRate: "0", bYears: "1.5", bAdd: "100" },
    clicks: ["switchTab('compare');calcCompare();"],
    expect: ["A 共 1 次、B 共 2 次", "方案A终值 ¥ 1,100.00", "方案B终值 ¥ 1,200.00"],
    ref: "第936批：每年期初追加按真实离散日期发生：0.5 年仅 t=0 一次（A 投入 1100），1.5 年在 t=0、1 两次（B 投入 1200）；旧实现按 0.5/1.5 比例折算成 50/150 元。零利率下终值等于累计投入，可直观验证次数。",
  }
,
  // ===== 第937批新增 =====
  {
    slug: "finance/simple-interest",
    inputs: { principal: "1000", rate: "10", years: "0.5" },
    clicks: ["calc()"],
    expect: ["不足一年按 (1+年利率)^年数 比例折算", "比单利少 1.19"],
    ref: "第937批：0.5 年、10% 时复利本利和 1048.81 低于单利 1050，旧文案固定「比单利多」并显示负差额；现按差额正负输出多/少/相同，并说明不足一年按幂次比例折算、非真实付息日复利。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "10000", rate: "", years: "10" },
    clicks: ["calc()"],
    expect: ["请输入年化利率（如确为 0%，请明确输入 0）"],
    ref: "第937批：年化利率留空不再按 0% 复利计算并显示「本利和等于本金」；显式输入 0 仍合法，负值/年限 0 也改为具体提示。",
  },
  {
    slug: "finance/currency-converter",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/currency-converter.html','utf8');var a=h.indexOf('role=\"tab\"')>=0&&h.indexOf('aria-selected')>=0&&h.indexOf('id=\"tabbtn-about\"')>=0&&h.indexOf('role=\"button\" tabindex=\"0\"')>=0;document.getElementById('__tbProbe').textContent='CCTAB '+(a?'OK':'BAD');"],
    expect: ["CCTAB OK"],
    ref: "第937批：五个页签改为原生 button + role=tab/aria-selected/aria-controls，切换时同步 roving tabindex；旧实现为无键盘入口的 div。历史项改为可聚焦 role=button 并支持 Enter/Space，删除改为独立命名按钮。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "1234.56" },
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/amount-in-words.html','utf8');var a=h.indexOf('href=\"tax-calculator.html\"')>=0,b=h.indexOf('href=\"invoice-generator.html\"')>=0,c=h.indexOf('onclick=\"copyPlainResult()\"')>=0;document.getElementById('__tbProbe').textContent='AWREL '+((a&&b&&c)?'OK':'BAD');"],
    expect: ["AWREL OK"],
    ref: "第937批：相关推荐从单词反转/字数统计等文本工具换成数字转中文、英文金额、发票、个税、税后工资、贷款月供等财务工具；新增「复制纯大写金额」避免把整段报告复制进票据。",
  },
  {
    slug: "finance/assessor-manager",
    inputs: { debtRatio: "55", currentRatio: "1.8", revenue: "5000", profitMargin: "12", overdue: "1", creditHistory: "5" },
    clicks: ["localStorage.removeItem('tbk_hist_'+location.pathname);calc();__assessor_managerExtras(true);var n=JSON.parse(localStorage.getItem('tbk_hist_'+location.pathname)||'[]').length;document.getElementById('__tbProbe').textContent='ASPRIV '+((n===0&&document.getElementById('assessorRememberHistory').checked===false)?'OK':'BAD');"],
    expect: ["ASPRIV OK"],
    ref: "第937批：客户财务指标属敏感信息，历史默认不写入；只有本机勾选「保存评估历史」才记录，并提供清除入口。旧实现每次 calc 自动写入 localStorage。",
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "", housePrice: "200", city: "shanghai" },
    clicks: ["calc()"],
    expect: ["账户余额尚未填写", "留空不会被当作零额度计算"],
    ref: "第937批：账户余额留空不再 parseFloat||0 后显示 0 额度，而是点名缺项并提示 0 需显式输入；显式 0 仍合法。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: { monthly: "1000", years: "10", rate: "8", initial: "0", buyFee: "0.15", manageFee: "1.5", custodyFee: "0.25", sellFee: "0.5" },
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/mutual-fund-calculator.html','utf8');var a=h.indexOf('totalFees += monthly * buyFee + balance * (monthlyManageFee + monthlyCustodyFee)')>=0,b=h.indexOf('管理费/托管费按当月存量资产逐月计提')>=0;document.getElementById('__tbProbe').textContent='MFFEE '+((a&&b)?'OK':'BAD');"],
    expect: ["MFFEE OK"],
    ref: "第937批：费用合计过去只累计申购/赎回费，管理费与托管费只体现在净值扣减、未计入金额；现按每月计费基数把两类年费并入 totalFees，并用 42 年 42% 极端组复核数值 32,413.35。",
  },
  {
    slug: "finance/ird-validator",
    inputs: { input: "490918507" },
    clicks: ["var m=__ird_validatorMask('490918507');var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/ird-validator.html','utf8');var a=h.indexOf(\"out[e.id]=e.id==='input'?__ird_validatorMask(v):v\")>=0,b=h.indexOf('__ird_validatorMigrateLegacy')>=0;document.getElementById('__tbProbe').textContent='IRDPRIV '+((m==='49*****07'&&a&&b)?'OK':'BAD')+' m='+m;"],
    expect: ["IRDPRIV OK"],
    ref: "第937批：历史与结果快照只保存脱敏税号（前 2 后 2），完整 8–9 位号码不落 localStorage；历史回放遇到掩码明确提示重新输入，并迁移清理旧的全号记录。",
  },

  // ===== 第938批新增 =====
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "100" },
    clicks: ["document.getElementById('rateMode').value='manual';__ccToggleManual();document.getElementById('manualRate').value='0.9';resetCalc();"],
    expect: ["100.00 🇨🇳 人民币 13.7931", "builtin"],
    ref: "第938批：重置不再保留旧手动汇率/模式，恢复 CNY→USD、金额 100、rateMode=builtin、manualRate=7.25 并隐藏手动输入；旧实现只改币种与金额，其他币对的手动汇率会套到重置后的币对。",
  },
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "" },
    clicks: ["calc();"],
    expect: ["请输入要换算的金额；留空不等同于 0，如确为 0 请明确输入 0"],
    ref: "第938批：空输入不再当 0 输出换算结论，点名留空与显式 0 的区别；旧实现 parseFloat('')||0 会静默按零换算。",
  },
  {
    slug: "finance/currency-converter",
    inputs: { fromAmount: "0" },
    clicks: ["calc();"],
    expect: ["0.00 🇺🇸 USD 美元 0.0000"],
    ref: "第938批：显式 0 合法，两侧都按 0 展示（源 0.00、目标 0.0000），与空输入的提示态区分。",
  },
  {
    slug: "finance/tax-bracket",
    inputs: { income: "300000" },
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/tax-bracket.html','utf8');var i=JSON.parse(globalThis.__tbFs.readFileSync(process.cwd()+'/i18n/tools/finance.json','utf8'))['tax-bracket'];var a=h.indexOf('中国居民个人综合所得税率表（年度）')>=0&&h.indexOf('这不是到手工资')>=0&&h.indexOf('中国 2024')<0;var b=i['zh-CN'].intro.indexOf('不适用于经营所得')>=0&&i['en-US'].intro.indexOf('verified Nov 2026')>=0;document.getElementById('res').innerHTML='<p>TBDESC '+((a&&b)?'OK':'BAD')+'</p>';"],
    expect: ["TBDESC OK"],
    ref: "第938批：税率表描述限定为中国居民个人综合所得年度表，补规则来源/施行日/核验日期/不适用范围；结果改称「应纳税所得额减本次估算税额」并非到手工资。旧文案「支持常见税表」「中国 2024」与实际单一表不符。",
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "20000", insurance: "2000", special: "1000", threshold: "", bonus: "30000" },
    clicks: ["calculate()"],
    expect: ["请填写起征点；如确为 0 请明确输入 0，留空不会按 0 计税。"],
    ref: "第938批：起征点留空不再 parseFloat||0 当 0 计税，点名字段并清空结果/导出；显式 0 合法。默认 5000 ⇒ 不命中。",
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "20000", insurance: "2000", special: "1000", threshold: "5000", bonus: "-1" },
    clicks: ["calculate()"],
    expect: ["全年一次性奖金不能为负数。"],
    ref: "第938批：负奖金不再落入 renderBonus 的 <=0 分支被当作未填写；字段级提示并停止结果与导出。默认奖金 30000 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { monthly: "500", annualRate: "10", period: "60", freq: "weekly" },
    clicks: ["calcRegular()"],
    expect: ["定投期限上限为 50 年", "约 3120 期"],
    ref: "第938批：60 年周投约 3,120 期，超 50 年上限直接拒绝，不构造现金流数组、不跑 IRR；上限附近 50 年周投 2600 期仍可计算。",
  },
  {
    slug: "finance/analysis-44",
    inputs: { plan: "100000", actual: "108000", warnPct: "2", alertPct: "4", nextPlan: "100000", nextActual: "110000" },
    clicks: ["calc()"],
    expect: ["双重预警", "超过严重阈值", "当前阈值 ±2% / 4%", "后续情景合计"],
    ref: "第938批：阈值本地可调，8% 在 4% 严重阈值下判严重超支；金额 8,000 与比例 8% 双重预警；后续 100k/110k 合计 200k/218k=9% 继续超阈值。旧实现固定 5/10 且仅比例判定。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "1000000" },
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/loan-amortization.html','utf8');var a=h.indexOf('原计划总利息')>=0&&h.indexOf('原计划总还款额')>=0&&h.indexOf('原计划期数')>=0;var b=h.indexOf('提前还款后</strong>：总利息')>=0&&h.indexOf('少付利息')>=0&&h.indexOf('drawPieChart(amount, __newInt, __laTx(')>=0;var c=h.indexOf('提前结清后</strong>：总利息')>=0&&h.indexOf('drawPieChart(amount, __newInterest, __laTx(')>=0;document.getElementById('res').innerHTML='<p>LACMP '+((a&&b&&c)?'OK':'BAD')+'</p>';"],
    expect: ["LACMP OK"],
    ref: "第938批：顶部汇总改标「原计划」；提前还款两种方式均并列原计划/新计划的总利息、总还款、期数与差额，饼图改用提前后利息并标注方案；提前结清同样给出新旧对照。旧实现顶部旧汇总与明细新计划同屏无区分，饼图仍画原计划利息。",
  },

  // ===== 第939批新增 =====
  {
    slug: "finance/car-loan-calculator",
    inputs: { price: "150000", regFee: "", taxRate: "10", vehicleTax: "420", compInsurance: "950", commInsurance: "5000" },
    clicks: ["calculate()"],
    expect: ["请填写有效的上牌费用（非负数字）；如确为 0 请明确输入 0，留空或负数不会按 0 计入落地总价。"],
    ref: "第939批：费用字段空值不再 parseFloat||0 静默按 0 计入落地总价；点名字段并清空相关总额。默认上牌费 500 ⇒ 不命中。",
  },
  {
    slug: "finance/car-loan-calculator",
    inputs: { price: "150000", regFee: "500", taxRate: "10", vehicleTax: "420", compInsurance: "-1", commInsurance: "5000" },
    clicks: ["calculate()"],
    expect: ["请填写有效的交强险（非负数字）"],
    ref: "第939批：负数费用不再被控件 min 之外静默接受并拉低总价；字段级提示。默认交强险 950 ⇒ 不命中。",
  },
  {
    slug: "finance/mutual-fund-calculator",
    inputs: { monthly: "1000", years: "10", rate: "8", initial: "0" },
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/mutual-fund-calculator.html','utf8');var a=h.indexOf('id=\"reinvest\" checked disabled')>=0;var b=h.indexOf('现金分红会减少基金份额并产生现金流入')>=0&&h.indexOf('统一按红利再投资计算')>=0;document.getElementById('res').innerHTML='<p>MFDIV '+((a&&b)?'OK':'BAD')+'</p>';"],
    expect: ["MFDIV OK"],
    ref: "第939批：现金分红无法合理模拟，故禁用切换并说明统一按红利再投资口径；旧实现复选框只改文案、现金流未使用该选项，切换后资产与 IRR 不变。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "1.999" },
    clicks: ["convert()"],
    expect: ["已四舍五入到分：2.00 元 → 贰元整", "原始输入 1.999 有 3 位小数"],
    ref: "第939批：超过两位小数不再静默四舍五入到 2.00 并显示贰元整，而是拒绝并说明未取整；复制/导出不会生成未提示的进位结果。1.999 默认不出现该提示。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "0.005" },
    clicks: ["convert()"],
    expect: ["已四舍五入到分：0.01 元 → 壹元零壹分", "原始输入 0.005 有 3 位小数"],
    ref: "第939批：0.005 也不再静默进位到 0.01 元；边界拒绝而非隐藏取整。",
  },
  {
    slug: "finance/postal-code-validator",
    inputs: { input: "10001" },
    clicks: ["validate('CN');"],
    expect: ["不符合所选 中国（CN）的邮编格式：6 位数字"],
    ref: "第939批：可选国家后按所选规则校验，10001 不符合中国 6 位数字；旧实现只按格式列表匹配，无法指定国家。默认自动识别不含该提示。",
  },
  {
    slug: "finance/postal-code-validator",
    inputs: { input: "100000" },
    clicks: ["validate('CN');"],
    expect: ["中国（CN）：6 位数字", "格式匹配不确认邮编真实存在、已分配或地址可投递"],
    ref: "第939批：中文态结果国家名显示中文，并明确仅格式匹配、不证明邮编存在或可投递；旧实现显示 China 与绿色勾选，易被当成真实国家确认。",
  },
  {
    slug: "finance/rental-yield-calculator",
    inputs: { price: "300", rent: "5000", vacancyMonths: "2", fee: "300", heat: "2400", decor: "5000", repair: "1000", agency: "0", tax: "2000" },
    clicks: ["calc()"],
    expect: ["50,000", "空置 2 个月"],
    ref: "第939批：空置 2 个月 ⇒ 年租金 5,000×10=50,000，不再全年满租按 60,000；结果与回报率、对比、导出同一口径。默认空置 0 ⇒ 60,000，不命中。",
  },
  {
    slug: "finance/rental-yield-calculator",
    inputs: { price: "300", rent: "5000", vacancyMonths: "" },
    clicks: ["calc()"],
    expect: ["空置月数须为 0–12 的整数；不空置请明确填 0。"],
    ref: "第939批：空置月数留空不再静默按 0（全年满租）；显式 0 合法，空串提示。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { lv_age: "60", lv_retire: "60", lv_income: "20", lv_growth: "3", lv_consume: "30", lv_discount: "5" },
    clicks: ["switchMethod('life-value');calc();"],
    expect: ["剩余工作年限按 0 年计"],
    ref: "第939批：当前年龄等于退休年龄时不再 Math.max(…,1) 强行计一年收入，生命价值保额为 0 并说明；默认 30/60 ⇒ 30 年，不命中。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { lv_age: "30.5", lv_retire: "60", lv_income: "20", lv_growth: "3", lv_consume: "30", lv_discount: "5" },
    clicks: ["switchMethod('life-value');calc();"],
    expect: ["当前年龄与退休年龄须填写整数岁；小数年龄会让剩余工作年限与显示不一致"],
    ref: "第939批：小数年龄不再被循环取整后仍显示原小数年限；明确要求整数。默认 30/60 ⇒ 不命中。",
  },
  {
    slug: "finance/investment-calculator",
    inputs: { initial: "10000", final: "18000", years: "5", additional: "5000" },
    clicks: ["calc();"],
    expect: ["资金加权年化：未计算（未填追加日期）", "期初假设估算年化", "未提供日期时不把该估算称为 CAGR"],
    ref: "第939批：有追加但无日期时不再直接称 CAGR；仅给累计回报并把年化标注为期初假设估算，提示填写日期。默认追加 0 ⇒ 不出现。",
  },
  {
    slug: "finance/investment-calculator",
    inputs: { initial: "10000", final: "18000", years: "5", additional: "5000", additionalDate: "2023-01-01" },
    clicks: ["calc();"],
    expect: ["资金加权年化（按现金流时点）", "已按该时点折现求解"],
    ref: "第939批：填写追加日期后按初始 0 年、追加 t 年、期末 5 年求 XIRR，不再把 5,000 全部当第 0 年投入；旧实现仅用总投入算 CAGR。",
  },
  {
    slug: "finance/currency-symbol",
    inputs: { searchInput: "美元" },
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/currency-symbol.html','utf8');var a=h.indexOf('<button type=\"button\" class=\"filter-tab')>=0&&h.indexOf('aria-pressed=\"false\"')>=0;var b=h.indexOf('<button type=\"button\" class=\"currency-card\" aria-label=')>=0;var c=h.indexOf('role=\"dialog\" aria-modal=\"true\"')>=0&&h.indexOf(\"e.key === 'Escape'\")>=0&&h.indexOf('__curLastFocus')>=0;document.getElementById('res').innerHTML='<p>CURKB '+((a&&b&&c)?'OK':'BAD')+'</p>';"],
    expect: ["CURKB OK"],
    ref: "第939批：地区筛选与货币卡片改语义化 button 并公布 aria-pressed；详情弹层 role=dialog/aria-modal、打开聚焦关闭按钮、Escape 关闭并归还焦点。旧实现为 div onclick，键盘不可达且无焦点管理。",
  }
,
  // ===== 第940批新增 =====
  {
    slug: "finance/mortgage-calculator",
    inputs: { calcMode: "principal", loanAmount: "70", rate: "4.2", years: "30", downPayment: "30" },
    clicks: ["setCalcMode();document.getElementById('loanAmount').value='70';calculate()"],
    expect: ["贷款本金：¥700,000.00", "计算前提：直接输入贷款本金 ¥700,000.00，未再按首付比例扣减"],
    ref: "已知贷款本金入口：计算入口选 principal、本金 70 万，首付 30% 仍留在表单但不得再扣一次；旧实现固定按房价×(1−首付) ⇒ 49 万，少算 21 万。两条分别绑定贷款本金合计与前提文案；默认 price 模式（房价 100 万/首付 30% ⇒ 70 万）虽然金额同为 70 万，但前提文案是「房价 ¥1,000,000.00 × 首付 30%」，不会命中第二条 ⇒ 强判别。",
  },
  {
    slug: "finance/mortgage-calculator",
    inputs: { loanAmount: "100", rate: "4.2", years: "30", downPayment: "30" },
    clicks: ["calculate();var sumI=0,sumPay=0;__mcSchedule.forEach(function(r){sumI+=r.interest;sumPay+=r.payment;});var totalI=parseFloat(document.getElementById('totalInterest').textContent.replace(/[^0-9.-]/g,''));var totalPay=parseFloat(document.getElementById('totalPayment').textContent.replace(/[^0-9.-]/g,''));var last=__mcSchedule.length?__mcSchedule[__mcSchedule.length-1].balance:999;document.getElementById('__tbProbe').textContent='MCROUND '+((Math.abs(sumI-totalI)<0.005&&Math.abs(sumPay-totalPay)<0.005&&last===0)?'OK':'BAD')+' rows='+__mcSchedule.length;"],
    expect: ["MCROUND OK rows=360"],
    ref: "逐期舍入对账：明细按分显示，逐期利息/月供之和必须与上方总利息/总还款额在 0.01 内一致，末期余额归零。旧实现合计按未舍入浮点、明细各自 toFixed ⇒ 逐项求和与合计可差数分；末期余额也可能残留极小值。默认 100 万/4.2%/30 年即触发，探针同时锁 360 行与三项等式 ⇒ 旧版 BAD、零逃生。",
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "8000.01", insurance: "0", special: "0", threshold: "5000" },
    clicks: ["calculate()"],
    expect: ["> 3,000 且 ≤ 12,000 元 10% ✓ 适用"],
    ref: "小数金额边界：应纳税所得额 = 8000.01 − 0 − 5000 − 0 = 3000.01，按 >3000 且 ≤12000 应落第2级。旧版显示 3,001–12,000，会让 3000.01 看起来不属于任何显示区间；新版开放/闭合边界与计算一致。默认所得 10000 也落第2级，但旧文案同样显示 3,001–12,000 ⇒ 以带「> 3,000 且 ≤」的新串锁定修复，零逃生。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "120000", annualRate: "6", loanYears: "10", prepayMonth: "1", prepayAmount: "10000", repayMethod: "equal" },
    clicks: ["document.getElementById('prepayCard').style.display='block';calc();var s12=scheduleData.filter(function(r){return r.month<=12;}).slice(-1)[0];var want=(typeof fmt==='function'&&s12)?fmt(s12.balance):'';var html=document.getElementById('yearlyTable').innerHTML;document.getElementById('__tbProbe').textContent='LOANYR '+((s12&&want&&html.indexOf(want)>=0&&scheduleData.length<120)?'OK':'BAD')+' rows='+scheduleData.length;"],
    expect: ["LOANYR OK"],
    ref: "第1期后提前还款 1 万：年度汇总必须按还款期数归属年度聚合，提前还款行与其所在期同年、不额外占月份。修复前按数组每 12 行分组，第一年只含第1–11期+提前还款行，第12期被挤到第二年，首行年末余额与第12期余额不符。探针比较首行年末余额与 scheduleData 中 month≤12 的最后一期余额，并要求提前后总期数<120 ⇒ 旧实现 BAD。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "100000", annualRate: "0.00000000000001", loanYears: "30", repayMethod: "equal" },
    clicks: ["calc();var r=document.getElementById('resultBox').innerHTML;document.getElementById('__tbProbe').textContent='LOANTINY '+((r.indexOf('277.78')>=0&&r.indexOf('Infinity')<0&&r.indexOf('NaN')<0)?'OK':'BAD');"],
    expect: ["LOANTINY OK"],
    ref: "极小正利率数值稳定性：本金 100,000、30 年（360 期）、年利率 1e-14% 的月利率约 8.3e-19，旧式 (1+r)^n−1 因浮点归零 ⇒ 月供 Infinity。新实现用 expm1/log1p，并在 r<1e-12 时退化为本金/期数 = 277.78；结果区不得出现 Infinity/NaN。默认 4.9% 月供不同 ⇒ 零逃生。",
  },
  {
    slug: "finance/report-1",
    inputs: { inv: "800000", pct: "80", capital: "500000", retained: "200000", premium: "0", profit: "150000", dec: "2" },
    clicks: ["calc()"],
    expect: ["简化合并差额（非直接商誉）", "该差额不能直接确认为商誉", "教学用抵销示意（不是可直接入账的分录）"],
    ref: "合并差额口径：默认 80 万 − 70 万×80% = 24 万，旧版直接写「合并价差（商誉）」并在提示里称「确认为商誉」；新版统计卡改称「简化合并差额（非直接商誉）」，结果提示明确不能直接确认商誉，抵销表标明仅为教学示意。三条分别锁标签、结论与分录标题；旧源码均不含 ⇒ 零逃生。",
  },
  {
    slug: "finance/inflation-calculator",
    inputs: { amt: "100000", rate: "3", years: "0" },
    clicks: ["calc()"],
    expect: ["年限须为 1–1000 的整数年（当前输入 0）", "0 也不会按 1 年计算"],
    ref: "年限 0 不再静默按 1 年：旧实现 Math.max(1, Math.floor(0)) ⇒ 主结果按 1 年、辅助解读仍用原始值，口径分裂。新版统一校验为 1–1000 整数年，0 与小数都拒绝并清空统计/表格/图表。默认 20 年 ⇒ 不命中。",
  },
  {
    slug: "finance/inflation-calculator",
    inputs: { amt: "100000", rate: "3", years: "1.5" },
    clicks: ["calc()"],
    expect: ["年限须为 1–1000 的整数年（当前输入 1.5）", "小数年限不四舍五入"],
    ref: "小数年限 1.5：旧实现主结果向下取整为 1 年，而页面说明/解读仍按 1.5 年，同屏两个期限。新版明确只支持整数年，拒绝小数并说明不四舍五入；默认 20 年不命中。",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "1000000", rate: "", years: "30" },
    clicks: ["calc()"],
    expect: ["请填写年利率；留空不会按 0% 计算"],
    ref: "空利率不再按零息放款：旧实现 parseFloat('')||0 ⇒ 0% 利率，照常输出 30 年零息计划；新版区分空值与合法 0，空串直接停止并清空汇总/明细。默认 4.2% 不命中。",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "-100000", rate: "4.2", years: "30" },
    clicks: ["calc()"],
    expect: ["贷款金额须为正数（当前输入 -100000 元）", "负数与 0 均不支持"],
    ref: "负本金：旧实现 parseFloat(-100000)||0 ⇒ 负月供与负总还款；新版要求本金 >0 并停止计算、清空旧结果。默认 100 万不命中。",
  },
  {
    slug: "finance/calc-4",
    inputs: { amount: "12000", rate: "0", years: "1" },
    clicks: ["calc()"],
    expect: ["1,000.00 元", "12,000.00 元", "利息 0.00 元"],
    ref: "显式 0% 利率仍合法：本金 12,000、1 年 12 期 ⇒ 月供 1,000.00、总还款 12,000.00、利息 0.00。旧实现虽然也能算，但空值与 0 不分；新版只拒绝空值，明确输入 0 必须继续出结果。默认 4.2% 金额不同 ⇒ 强判别。",
  },
  // ===== 第941批新增 =====
  {
    slug: "finance/inflation-calculator",
    inputs: { amt: "100000", rate: "3", years: "10" },
    clicks: ["switchMode('backward');var d=getYearData(10);var n=document.getElementById('chartNote');document.getElementById('__tbProbe').textContent='INFBASE '+((d[0].neededAmount===100000&&d[10].neededAmount===100000&&n.textContent.indexOf('固定输入的未来金额')>=0&&document.getElementById('legendNA').textContent.indexOf('固定未来金额')>=0)?'OK':'BAD');"],
    expect: ["INFBASE OK"],
    ref: "反向模式固定未来金额基准：输入 100,000 是「未来第10年」的固定金额，图表红线应保持水平 100,000（各年 neededAmount 均等于输入），蓝线为折现价值；图例/说明须写明固定未来金额与基准日今天。旧实现 neededAmount=amt×(1+r)^n 逐年增长，图例仍叫「未来金额」⇒ BAD。默认正向模式需要金额本来就是增长的 ⇒ 不命中。",
  },
  {
    slug: "finance/analysis-44",
    inputs: { plan: "100000", actual: "108000", warnPct: "5", alertPct: "10" },
    clicks: ["calc()"],
    expect: ["计划/实际支出比", "不是 EVM 的 CPI", "不反映完成量"],
    ref: "口径纠偏：计划/实际=100000/108000≈0.9259 只是支出比例；挣值 CPI 需 EV÷AC，页面不得再称成本绩效指数。旧实现结果区写「成本绩效指数 CPI：0.9259」⇒ 不命中。默认 100k/108k 相同但旧标签不同 ⇒ 锁文案。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "100000", salvage: "10000", life: "101" },
    clicks: ["calc()"],
    expect: ["使用年限最多支持 100 年（当前输入 101）", "更长年限会生成过多期数并拖慢页面"],
    ref: "年限上限：旧实现只校验正整数，101 年会一次性生成 4 种方法×101 行表格与图表标签；新实现拒绝 >100 并提示拆分。默认 5 年 ⇒ 不命中。",
  },
  {
    slug: "finance/car-loan-calculator",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/car-loan-calculator.html','utf8');var ok=h.indexOf('等额本息、等额本金两种还款方式')>=0&&h.indexOf('总利息与逐期明细')>=0&&h.indexOf('算等额本息车贷月供与总利息')<0;document.getElementById('__tbProbe').textContent='CARSEO '+(ok?'OK':'BAD');"],
    expect: ["CARSEO OK"],
    ref: "搜索/分享/结构化描述必须覆盖两种还款方式、月供、总利息、逐期明细与购车费用，不能只说「算等额本息车贷月供与总利息」；默认页面旧描述含该残缺句 ⇒ BAD。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { strike: "100", premium: "120", s0: "10", contracts: "1", mult: "100", fee: "0" },
    clicks: ["switchType('put','buy');calc()"],
    expect: ["无平衡点（理论平衡价 -20.00 元 < 0，非负标的价格区间内不可达）", "无盈利区间（全区间净亏损）", "全区间最大净盈利： ¥0（无盈利区间，最好情形仍为净亏损 ¥2,000.00）"],
    ref: "看跌买方权利金 120 > 行权价 100：理论平衡价 100−120=−20 在 S≥0 不可达；全区间 payoff 最大为 100，扣 120 权利金后最好仍亏 20/股 ⇒ 最大净盈利应显示 ¥0 并说明最好情形净亏 ¥2,000，不得显示负的最大盈利或负平衡价。旧实现 bep=−20、maxProfit=−20 照写 ⇒ BAD。默认 call 100/5 不命中。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { strike: "100", premium: "120", s0: "10", contracts: "1", mult: "100", fee: "0" },
    clicks: ["switchType('put','sell');calc()"],
    expect: ["无平衡点（理论平衡价 -20.00 元 < 0，非负标的价格区间内不可达）", "全区间最大净亏损： ¥0（无亏损区间，最差情形仍为净盈利 ¥2,000.00）", "S ≥ 0 全区间净盈利"],
    ref: "看跌卖方权利金 120 > 行权价 100：最差情形 S=0 仍收 120−100=20/股，全区间净盈利；理论平衡价 −20 不可达。最大净亏损应显示 ¥0 并说明最差仍盈利 ¥2,000，不得显示负的最大亏损。旧实现 maxLoss=K−p=−20 ⇒ 「最大亏损 −2,000」⇒ BAD。",
  },
  {
    slug: "finance/payroll-calculator",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/payroll-calculator.html','utf8');var ok=h.indexOf('住房贷款利息与住房租金不能同时扣除')>=0&&h.indexOf('同期只能二选一')>=0&&h.indexOf('function housingDeductionInput')>=0&&h.indexOf('housingLoan')>=0&&h.indexOf('rent')>=0;document.getElementById('__tbProbe').textContent='PAYSRC '+(ok?'OK':'BAD');"],
    expect: ["PAYSRC OK"],
    ref: "源码守卫：calc 前置拒绝两项同时>0 并提示「同期只能二选一」；housingDeductionInput 在任一项输入时把另一项清 0，双 0 合法。旧实现两项直接相加 ⇒ BAD。真机已验证 1000+1500 拒绝、输入租金自动清贷款、0/0 正常出结果。",
  },
  {
    slug: "finance/register-depreciation",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/register-depreciation.html','utf8');var ok=h.indexOf('固定资产登记与折旧台账')>=0&&h.indexOf('不含盘点状态')>=0&&h.indexOf('不按自然月自动计提')>=0&&h.indexOf('资产清单（筛选与搜索，不含盘点状态）')>=0&&h.indexOf('<h3>资产盘点</h3>')<0;document.getElementById('__tbProbe').textContent='REGSEP '+(ok?'OK':'BAD');"],
    expect: ["REGSEP OK"],
    ref: "能力边界纠偏：页面/描述改称登记与折旧台账，明确不含盘点状态、盘点差异、月度计提或指定期间汇总，并把「资产盘点」标题改为资产清单；旧文案称盘点管理、使用场景写月度计提 ⇒ BAD。",
  },
  // ===== 第942批新增 =====
  {
    slug: "finance/retirement-calculator",
    inputs: { age: "30.5", retireAge: "60", lifeAge: "85", currentSavings: "50000", monthlyContribution: "1000", returnRate: "6", inflation: "3", monthlyExpense: "5000" },
    clicks: ["calc()"],
    expect: ["当前年龄须为 0–120 的整数"],
    ref: "小数年龄会让逐年循环与退休年数不一致：必须拒绝并清空年度明细。默认 30 整数不命中。",
  },
  {
    slug: "finance/retirement-calculator",
    inputs: { age: "30", retireAge: "60", lifeAge: "85", currentSavings: "50000", monthlyContribution: "1000", returnRate: "6", inflation: "-100", monthlyExpense: "5000" },
    clicks: ["calc()"],
    expect: ["通胀率须大于 -100% 且不超过 30%"],
    ref: "-100% 通胀会使实际收益率分母为 0：必须拒绝。默认 3% 不命中。",
  },
  {
    slug: "finance/retirement-calculator",
    inputs: { age: "10", retireAge: "80", lifeAge: "120", currentSavings: "50000", monthlyContribution: "1000", returnRate: "6", inflation: "3", monthlyExpense: "5000" },
    clicks: ["calc()"],
    expect: ["跨度不得超过 100 年"],
    ref: "110 年跨度会生成过多年度数据：拒绝并清空。默认 55 年不命中。",
  },
  {
    slug: "finance/car-loan-calculator",
    inputs: { price: "", downPct: "30", rate: "5.5", years: "3", taxRate: "10", regFee: "500", vehicleTax: "420", compInsurance: "950", commInsurance: "5000" },
    clicks: ["calculate()"],
    expect: ["请填写车价（元）", "结果区已置为待输入状态"],
    ref: "车价为空时不能只把结果置 --：必须说明具体哪一项无效。默认 150000 不命中。",
  },
  {
    slug: "finance/car-loan-calculator",
    inputs: { price: "150000", downPct: "0", rate: "0", years: "3", taxRate: "10", regFee: "500", vehicleTax: "420", compInsurance: "950", commInsurance: "5000" },
    clicks: ["calculate()"],
    expect: ["4,166.67", "0.00%"],
    ref: "合法 0 首付 + 0% 利率仍须计算：15 万/36 期=4,166.67，利息 0。旧实现此前已支持但错误提示改造后不能误伤零值。默认 30%/5.5% 不命中。",
  },
  {
    slug: "finance/sharpe-ratio",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/sharpe-ratio.html','utf8');var ok=h.indexOf('6 ÷ 12 = 0.500')>=0&&h.indexOf('方向取决于超额收益的符号')>=0&&h.indexOf('2%÷12=0.1667%')>=0&&h.indexOf('= 2.000')<0;document.getElementById('__tbProbe').textContent='SHRPE '+(ok?'OK':'BAD');"],
    expect: ["SHRPE OK"],
    ref: "直接模式 6%/12%=0.500 而非 2.000；样本标准差方向须按超额收益符号说明；月频先把年化无风险利率除以 12。旧文案 2.000/样本必然偏大/未折算月频 ⇒ BAD。",
  },
  {
    slug: "finance/futures-pnl-calculator",
    inputs: { openPrice: "4000", closePrice: "4100", lots: "1", marginRate: "10", openFee: "", closeFee: "2" },
    clicks: ["calc()"],
    expect: ["开仓手续费不能留空"],
    ref: "空手续费不能静默按 0：须明确输入 0。默认开仓手续费非空 ⇒ 不命中。",
  },
  {
    slug: "finance/futures-pnl-calculator",
    inputs: { openPrice: "4000", closePrice: "4100", lots: "1", marginRate: "10", openFee: "-1", closeFee: "2" },
    clicks: ["calc()"],
    expect: ["开仓手续费须为有限非负数"],
    ref: "负手续费会被当成收入加到净盈亏：必须拒绝。默认非负 ⇒ 不命中。",
  },
  {
    slug: "finance/futures-pnl-calculator",
    inputs: { openPrice: "4000", closePrice: "4100", lots: "1", marginRate: "10", openFee: "0", closeFee: "0" },
    clicks: ["calc()"],
    expect: ["手续费 0.00 元", "盈亏金额"],
    ref: "显式 0/0 手续费合法，净盈亏=100 点×10=1,000 元、手续费 0。默认费率非 0 ⇒ 不命中。",
  },
  {
    slug: "finance/compound-interest",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/compound-interest.html','utf8');var ok=h.indexOf('g = (1 + r/n)^n')>=0&&h.indexOf('年末投入 k=1、年初投入 k=g')>=0&&h.indexOf('PMT 是「每年」定投一次')>=0;document.getElementById('__tbProbe').textContent='CIFORM '+(ok?'OK':'BAD');"],
    expect: ["CIFORM OK"],
    ref: "公式必须用年度增长因子 g 的年金式，并区分年初×g、年末×1，避免把每年 PMT 当每复利期投入。旧公式 PMT·((1+r/n)^(nt)−1)/(r/n) ⇒ 1200 元算成 15,219 ⇒ BAD。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "0", rate: "12", years: "1", annual: "1200", freq: "12", investTime: "end" },
    clicks: ["calc()"],
    expect: ["1,200"],
    ref: "本金 0、12%/月复利、每年年末投 1200、1 年：年末投入当年不计息 ⇒ 终值 1,200，与代码一致。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "0", rate: "12", years: "1", annual: "1200", freq: "12", investTime: "start" },
    clicks: ["calc()"],
    expect: ["1,352"],
    ref: "年初投入多增长一年：1200×(1+12%/12)^12=1200×1.126825=1,352.19 ⇒ 显示 1,352。旧公式口径不一致。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "10000", rate: "0", years: "5", annual: "1200", freq: "12", investTime: "start" },
    clicks: ["calc()"],
    expect: ["16,000"],
    ref: "零利率：本金 10,000 + 每年 1,200×5 = 16,000；年初/年末不应有差异，也不能除零。",
  },
  {
    slug: "finance/analysis-5",
    inputs: { ca: "500000", inv: "180000", pre: "20000", cash: "80000", cl: "0", tl: "700000", ta: "1200000", dec: "2" },
    clicks: ["calc()"],
    expect: ["流动负债为 0：流动比率、速动比率、现金比率不适用", "营运资金", "58.33%"],
    ref: "零流动负债只让三个短期比率不适用，营运资金 500,000 与资产负债率 58.33% 仍须计算；旧实现整体 return 隐藏全部指标 ⇒ BAD。",
  },
  {
    slug: "finance/number-to-words-chinese",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/number-to-words-chinese.html','utf8');var ok=h.indexOf('绝对值 < 10¹³')>=0&&h.indexOf('最多 13 位整数')>=0&&h.indexOf('不是金额大写')>=0&&h.indexOf('票据/发票请使用中文大写金额工具')>=0&&h.indexOf('最大 ±1万亿')<0&&h.indexOf('适合票据与财务书写')<0;document.getElementById('__tbProbe').textContent='CNREAD '+(ok?'OK':'BAD');"],
    expect: ["CNREAD OK"],
    ref: "范围说明须与实际拒绝阈值一致，并明确本工具输出普通读数而非票据大写；旧文案「最大 ±1万亿」「适合票据」⇒ BAD。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { prepayMonth: "2.5" },
    clicks: ["calcPrepay()"],
    expect: ["提前还款期数须为整数"],
    ref: "小数期数不得进入 base[0.5] 造成逐期表错位，应提示须为整数；旧实现只判范围 ⇒ BAD。",
  },
  {
    slug: "finance/position-size-calculator",
    inputs: { "r-capital": "10000", "r-riskpct": "50", "r-price": "10", "r-stop": "9.5" },
    clicks: ["calc()"],
    expect: ["资金上限", "未使用风险预算", "1000"],
    ref: "风险预算理论股数 10,000 股，但可用资金仅能买 1,000 股；结果须按资金上限截断并提示未用完风险预算，不得输出 10,000 股。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { monthly: "100", period: "0.01", freq: "monthly" },
    clicks: ["calcRegular()"],
    expect: ["定投期限不足 1 期"],
    ref: "月频 0.01 年仅 0.12 期，不足 1 期应明确拒绝，不得用近似期数输出终值。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { monthly: "100", period: "0.1", freq: "yearly" },
    clicks: ["calcRegular()"],
    expect: ["定投期限不足 1 期"],
    ref: "年频 0.1 年不足 1 期同判；历史问题为图表 0 点而结果仍出值。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { chartMaxQty: "-1" },
    clicks: ["drawChart()"],
    expect: ["必须为正数"],
    ref: "负最大销量会使 q+=step 永不终止；必须在绘图前拒绝非正数并清空画布。",
  },
  {
    slug: "finance/amount-in-words",
    inputs: { money: "abc" },
    clicks: ["convert();document.getElementById('__tbProbe').textContent='AW-VALID '+(__amountInWordsValid===false?'OK':'BAD');"],
    expect: ["请输入有效金额", "AW-VALID OK"],
    ref: "无效输入只显示错误，复制/导出/历史不得把错误提示当作结果；旧实现复制按钮可复制报错文本 ⇒ BAD。",
  },
  {
    slug: "finance/credit-card-grace-period",
    inputs: {},
    clicks: ["var c=__ccCycle(__ccDate(2026,11,6),5,25,1);document.getElementById('__tbProbe').textContent='CC '+(__ccLabel(c.stmt)+'|'+__ccLabel(c.due)+'|'+c.grace);"],
    expect: ["CC 1月5日|1月25日|50"],
    ref: "账单日次日入账应落到下一期账单 1月5日、还款 1月25日，免息 50 天；旧对照表写「入账次月账单/顺延」不落具体日期 ⇒ BAD。",
  },
  {
    slug: "finance/car-loan-calculator",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/car-loan-calculator.html','utf8');var ok=h.indexOf('Number.isInteger(years)')>=0&&h.indexOf(\"priceRaw === ''\")>=0&&h.indexOf('downPct > 100')>=0;document.getElementById('__tbProbe').textContent='CAREXP '+(ok?'OK':'BAD');"],
    expect: ["CAREXP OK"],
    ref: "导出须重新校验原始输入（空值、负利率、首付>100%、年限非整数），不能只靠旧计划与价格/年限两项。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: { years: "1.5" },
    clicks: ["calc()"],
    expect: ["定投年限须为 1–50 的整数年"],
    ref: "1.5 年不得静默截断为 1 年；应按整数年校验并停止计算。",
  },
  {
    slug: "finance/dca-calculator",
    inputs: { years: "10" },
    clicks: ["window.__dl=0;ToolBox.downloadText=function(){window.__dl++;};document.getElementById('years').value='1.5';exportCSV();document.getElementById('__tbProbe').textContent='DCA-DL '+window.__dl;"],
    expect: ["DCA-DL 0"],
    ref: "非法年限下导出不得调用下载；计算返回空值时导出须提前停止。",
  },
  {
    slug: "finance/sort-code-validator-validator",
    inputs: { input: "200000" },
    clicks: ["validate()"],
    expect: ["银行归属：", "不推断", "格式有效"],
    ref: "页面不得再用前两位硬编码推断 Barclays 等银行归属；应明确只验证格式。",
  },
  {
    slug: "finance/number-to-words",
    inputs: { inputVal: "123.45", currencyMode: "USD" },
    clicks: ["convert()"],
    expect: ["one hundred twenty-three dollars and forty-five cents", "45/100"],
    ref: "货币格式须输出货币名称、分币与票据 x/100 写法；旧页面只有逐位 point 小数 ⇒ BAD。",
  },
  {
    slug: "finance/analysis-cost-1",
    inputs: { rows: "A,100\nB,abc", total: "1000" },
    clicks: ["calc()"],
    expect: ["第 2 行", "B,abc", "无法解析"],
    ref: "混合有效/非法行不得只对 A 分摊 100%；应逐行报错并停止结论。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { cost: "10000", "return": "13000", years: "2", unit: "year", discount: "-100" },
    clicks: ["calcSimple()"],
    expect: ["折现率须大于 -100%"],
    ref: "折现率 -100% 使现值分母为 0，必须字段级拒绝并清除旧图。",
  },
  {
    slug: "finance/investment-roi",
    inputs: { monthly: "1000", annualRate: "-100", period: "5", freq: "monthly" },
    clicks: ["calcRegular()"],
    expect: ["年化收益率须大于 -100%"],
    ref: "定投收益率 -100% 使单期增长因子为 0，须拒绝而不是输出伪终值。",
  },
  {
    slug: "finance/payroll-calculator",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/payroll-calculator.html','utf8');var ok=h.indexOf('税前工资须为 ≥0 的数字')>=0&&h.indexOf('工资与年终奖均为 0')>=0;document.getElementById('res').innerHTML='PAY0 '+(ok?'OK':'BAD');"],
    expect: ["PAY0 OK"],
    ref: "工资 0 须合法（仅年终奖测算），但工资与年终奖同时为 0 应拒绝；旧实现直接拒绝工资 0 ⇒ BAD。真机另测组合。",
  },
  {
    slug: "finance/payroll-calculator",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/payroll-calculator.html','utf8');var ok=h.indexOf('留空不等于 0')>=0&&h.indexOf('var val = raw;')>=0;document.getElementById('res').innerHTML='PAYR '+(ok?'OK':'BAD');"],
    expect: ["PAYR OK"],
    ref: "比例留空须提示补全，只有显式 0 才表示不缴；旧实现静默按 0 ⇒ BAD。",
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/lease-payment-calculator.html','utf8');document.getElementById('res').innerHTML='LEASE-RATE '+(h.indexOf('annualRate < 0 || annualRate > 100')>=0?'OK':'BAD');"],
    expect: ["LEASE-RATE OK"],
    ref: "负利率/极端利率须拒绝，不能进入幂运算产生无意义月供。",
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/lease-payment-calculator.html','utf8');var ok=h.indexOf('名义年化（月 IRR × 12）')>=0&&h.indexOf('有效年化（(1+月 IRR)¹²−1')>=0&&h.indexOf('Math.pow(1 + irr, 12) - 1')>=0;document.getElementById('res').innerHTML='LEASE-APR '+(ok?'OK':'BAD');"],
    expect: ["LEASE-APR OK"],
    ref: "页面旧称实际年化却只给月 IRR×12；须同时展示名义与月复利有效年化。",
  },
  {
    slug: "finance/analysis-5",
    inputs: { ca: "500000", inv: "180000", pre: "20000", cash: "600000", cl: "300000", tl: "700000", ta: "1200000" },
    clicks: ["calc()"],
    expect: ["现金 ≤ 流动资产", "明细与合计不一致"],
    ref: "现金大于流动资产属明细勾稽错误，必须停止评级；旧实现照算 ⇒ BAD。",
  },
  {
    slug: "finance/analysis-5",
    inputs: {},
    clicks: ["document.getElementById('ca').value='';calc();var r=document.getElementById('res');var ok=r.innerHTML.indexOf('请填写「流动资产」')>=0;r.innerHTML='A5-EMPTY '+(ok?'OK':'BAD');"],
    expect: ["A5-EMPTY OK"],
    ref: "空值不得当 0；0 仍须合法可计算。",
  },

  // ===== 第945批新增 =====
  {
    slug: "finance/compound-interest",
    inputs: { principal: "10000", rate: "0", years: "1", annual: "0" },
    clicks: ["calc();var tb=document.getElementById('yearTableBody');var first=String(tb.innerHTML).split('</tr>')[0];var ok=first.indexOf('<td>0</td>')>=0&&first.indexOf('10,000.00')>=0&&first.indexOf('0.00')>=0;document.getElementById('res').innerHTML='CI0 '+(ok?'OK':'BAD '+first);"],
    expect: ["CI0 OK"],
    ref: "第 0 年行必须自洽：期初余额 0 + 投入 10,000 + 利息 0 = 期末 10,000；旧实现把期初也写成 10,000，行内加减不平。",
  },
  {
    slug: "finance/generator-report-1",
    inputs: { rev: "100", costRate: "0", opex: "0", taxRate: "0", asset: "100", debtRatio: "0", dep: "10", capex: "10", dividend: "0", cash0: "20", wc: "0" },
    clicks: ["gen();var h=document.getElementById('res').innerHTML;var ok=h.indexOf('三表勾稽')>=0&&h.indexOf('期末非现金资产 80.00')>=0&&h.indexOf('差额 0.00 ✓')>=0;document.getElementById('res').innerHTML='GR '+(ok?'OK':'BAD '+h.slice(0,200));"],
    expect: ["GR OK"],
    ref: "期初非现金 80 − 折旧 10 + 资本开支 10 = 80，期末现金 120 ⇒ 期末资产 200；期初权益 100 + 净利润 100 = 200，资产负债表必须被利润表与现金流解释，不能只在表内自平。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "1000000", annualRate: "4.9", loanYears: "10", repayMethod: "balloon", balloonMonths: "30.5", balloonRatio: "50" },
    clicks: ["calc()"],
    expect: ["气球贷还款期数须为正整数月"],
    ref: "气球贷期数 30.5 月旧实现 Math.floor(30.5)=30 静默照算；现拒绝小数并提示改为 30 或 31。默认等额本息 ⇒ 不命中。",
  },
  {
    slug: "finance/break-even-calculator",
    inputs: { fc: "100", price: "30", vc: "0", qty: "10", taxRate: "0" },
    clicks: ["calc();var h=document.getElementById('statGrid').innerHTML;var ok=h.indexOf('最低整数件保本收入')>=0&&h.indexOf('120')>=0&&h.indexOf('理论保本收入')>=0;document.getElementById('res').innerHTML='BE '+(ok?'OK':'BAD '+h.slice(0,200));"],
    expect: ["BE OK"],
    ref: "保本量 100/30=3.33 件，按件向上取整 4 件；收入必须同步为 4×30=120 元，不能销量显示 4 件而收入仍按 3.33×30=100 元。",
  },
  {
    slug: "finance/register-depreciation",
    inputs: {},
    clicks: ["assets=[{id:'A1',name:'测试设备',cat:'电子设备',date:'2025-01-01',cost:10000,salvage:500,life:5,method:'straight'}];renderList();editAsset('A1');var picked=document.getElementById('aName').value;document.getElementById('aCost').value='20000';addAsset();var ok=picked==='测试设备'&&assets.length===1&&assets[0].cost===20000&&document.getElementById('saveAssetBtn').textContent==='登记资产'&&typeof importAssets==='function'&&typeof backupAssets==='function'&&isValidAsset({id:'B',name:'x',cat:'其他',date:'2025-01-01',cost:100,salvage:0,life:2,method:'syd'})&&!isValidAsset({name:'x',date:'2025/01/01',cost:100,salvage:0,life:2,method:'syd'});document.getElementById('assetList').innerHTML='RD '+(ok?'OK':'BAD');"],
    expect: ["RD OK"],
    ref: "台账必须可编辑而非只能删了重录：编辑入口回填原记录并原地更新（不得追加第二条）；同时暴露 JSON 备份/导入函数，导入记录校验日期与成本残值年限方法。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "1000000", annualRate: "4.9", loanYears: "30", prepayMonth: "24", prepayAmount: "100000" },
    clicks: ["calc();document.getElementById('loanAmount').value='0';calc();calcPrepay();var h=document.getElementById('prepayResult').innerHTML;var ok=h.indexOf('请先完成主贷款计算')>=0;document.getElementById('prepayResult').innerHTML='LP '+(ok?'OK':'BAD '+h.slice(0,120));"],
    expect: ["LP OK"],
    ref: "先按 100 万成功计算，再把主参数改成 0 触发提前退出；提前还款不得复用上一轮 originalScheduleData 的旧计划，必须提示先完成主贷款计算。",
  },
  {
    slug: "finance/analysis-risk",
    inputs: { s: "100", v: "100", f: "50", i: "20", t: "25", n: "100" },
    clicks: ["calc()"],
    expect: ["未确认亏损抵税"],
    ref: "EBIT=-50、利息 20 ⇒ 税前 -70：默认不得凭空确认 17.50 税盾，所得税按 0，明细必须写明未确认亏损抵税；旧实现无条件乘 (1-25%) ⇒ 不出现该提示。",
  },
  {
    slug: "finance/analysis-risk",
    inputs: { s: "100", v: "100", f: "50", i: "20", t: "25", n: "100" },
    checkIds: ["taxBenefit"],
    clicks: ["calc()"],
    expect: ["-52.50"],
    ref: "同上，显式勾选「亏损可抵税」后税前 -70 才确认 17.50 税盾，净利润 -52.50；默认态净利润 -70 ⇒ 不命中，用于区分两种口径。",
  },
  {
    slug: "finance/currency-converter",
    inputs: {},
    clicks: ["document.getElementById('manualRate').value='7.25';fromCurrency='EUR';var switched=__ccBindManualPair();var cleared=document.getElementById('manualRate').value==='';var sameKey=__ccManualPair==='EUR>USD';var ok=switched&&cleared&&sameKey;document.getElementById('resultDisplay').innerHTML='CC '+(ok?'OK':'BAD cleared='+cleared+' pair='+__ccManualPair);"],
    expect: ["CC OK"],
    ref: "CNY→USD 的手动汇率 7.25 在切到 CNY→EUR 后必须清空并要求重填；旧实现直接沿用 7.25 把欧元换算成 7.25 人民币，量级完全错误。",
  },

// ===== 第946批新增 =====
  {
    slug: "finance/portfolio-return",
    inputs: {},
    clicks: ["var r=__portfolioReturnWeighted([{name:'资产1',w:50,r:10},{name:'资产2',w:30,r:5},{name:'黄金',w:20,r:20}],false);var ok=Math.abs(r.rp-10.5)<1e-9&&r.contrib.length===3&&Math.abs(r.contrib[2].c-4)<1e-9&&r.wSum===100;document.getElementById('__tbProbe').textContent='PR '+(ok?'OK':'BAD '+JSON.stringify(r));"],
    expect: ["PR OK"],
    ref: "两项以上资产必须能参与加权：50%×10 + 30%×5 + 20%×20 = 10.5，第三项贡献 4 个百分点；旧实现只接受两个资产，添加第三项无任何作用。",
  },
  {
    slug: "finance/loan-amortization",
    inputs: { loanAmount: "1000000", annualRate: "4.9", loanYears: "1100", repayMethod: "balloon", balloonMonths: "12001", balloonRatio: "50" },
    clicks: ["calc()"],
    expect: ["12000"],
    ref: "气球期数 12001 期超过明细 12000 期硬上限，必须明确拒绝；旧实现被 Math.min 截成 12000 后照算，期限被悄悄改写。",
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "8", housePrice: "300", age: "35", loanYears: "20" },
    clicks: ["var q=__hfQuota(8,300,{limit:50,multiple:10},0.6);var ok=q.maxLoan===50&&q.amountByBalance===80&&q.amountByPrice===180&&__hfRuleValid(50,10,60)&&!__hfRuleValid(50,10,101);document.getElementById('__tbProbe').textContent='HF '+(ok?'OK':'BAD '+JSON.stringify(q));"],
    expect: ["HF OK"],
    ref: "手动规则 50 万/10 倍/60%：余额 8×10=80、房价 300×60%=180、上限 50 ⇒ 估算 50 万，并标注手动来源与条件估算；旧实现写死城市表，无法用本地细则覆盖。",
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "8", housePrice: "300" },
    clicks: ["document.getElementById('manualRules').checked=true;document.getElementById('hfRatio').value='101';calc();"],
    expect: ["手动规则无效"],
    ref: "房价贷款比例 101% 越界必须拒绝，不能静默按 1.01 倍房价给出超过房价的贷款。",
  },
  {
    slug: "finance/register-depreciation",
    inputs: {},
    clicks: ["var ok=calcDepreciation(10000,500,101,'straight').length===0&&calcDepreciation(10000,500,100,'straight').length===100&&!isValidAsset({name:'x',date:'2025-01-01',cost:100,salvage:0,life:101,method:'straight'});document.getElementById('assetList').innerHTML='RD2 '+(ok?'OK':'BAD');"],
    expect: ["RD2 OK"],
    ref: "年限 101 年必须判无效并返回空表，100 年仍可算；旧实现无上限，101 年虽只多 1 行，但极大年限会阻塞页面。",
  },
  {
    slug: "finance/vat-calculator",
    inputs: {},
    clicks: ["var ex=__vatRound2(0.05),tax=__vatRound2(0.05*0.13),incl=__vatRound2(0.05*1.13);var rowIncl=3*incl;var rawIncl=__vatRound2(3*0.05*1.13);var ok=ex===0.05&&tax===0.01&&incl===0.06&&__vatRound2(rowIncl)===0.18&&rawIncl===0.17;document.getElementById('batchInput').value='VAT '+(ok?'OK':'BAD '+[ex,tax,incl,rowIncl,rawIncl].join('/'));"],
    expect: ["VAT OK"],
    ref: "0.05×13%=0.0065，逐行税额进位 0.01、含税 0.06，三行合计 0.18；未舍入三行含税和 0.1695 四舍五入为 0.17。合计必须等于逐行显示值之和，并披露 0.01 差额。",
  },
  {
    slug: "finance/discount-calculator",
    inputs: {},
    clicks: ["setMode(1);document.getElementById('finalPrice').value='999';useQuick(0.8);var ok=document.getElementById('price').value==='100'&&document.getElementById('bigPrice').textContent.indexOf('80.00')>=0;document.getElementById('__tbProbe').textContent='DQS '+(ok?'OK':'BAD '+document.getElementById('price').value+' / '+document.getElementById('bigPrice').textContent);"],
    expect: ["DQS OK"],
    ref: "从「已知折后价」点 8 折速算：应切到已知原价模式并把原价设为示例 100，结果 80 元；旧实现只改折扣，原价仍留 999，算出 799.20 与速算「省 20%」严重不符。",
  },
  {
    slug: "finance/discount-calculator",
    inputs: {},
    clicks: ["document.getElementById('price').value='250';calc();document.querySelectorAll('#inputArea input[type=number]').forEach(function(e){e.value='';});calc();var ok=document.getElementById('bigPrice').textContent.trim()==='—'&&document.getElementById('detailResult').innerHTML.indexOf('请输入参数')>=0;document.getElementById('__tbProbe').textContent='DEM '+(ok?'OK':'BAD '+document.getElementById('bigPrice').textContent);"],
    expect: ["DEM OK"],
    ref: "清空全部数值输入后大号结果必须清为占位符，不能保留上一轮 250 元折后价；旧实现只在明细区提示，大号结果仍显示旧值。",
  },
  {
    slug: "finance/discount-calculator",
    inputs: {},
    clicks: ["document.getElementById('price').value='250';discounts=[0.7];renderDiscountChain();calc();setMode(1);document.getElementById('finalPrice').value='120';document.getElementById('discountRate').value='6';setMode(0);var p0=document.getElementById('price').value==='250'&&discounts[0]===0.7;setMode(1);var p1=document.getElementById('finalPrice').value==='120'&&document.getElementById('discountRate').value==='6';document.getElementById('__tbProbe').textContent='DMS '+(p0&&p1?'OK':'BAD p0='+p0+' p1='+p1);"],
    expect: ["DMS OK"],
    ref: "模式 0 输入 250 元、7 折，切到模式 1 填 120/6，再切回模式 0 原价与折扣链仍在，再切回模式 1 折后价与折扣率也仍在；旧实现每次 setMode 重建输入区，全部丢光。",
  },
  // ===== 第947批新增 =====
  {
    slug: "finance/irr-calculator",
    inputs: {},
    clicks: ["cashFlows[1].amount=null;renderFlows();calc();var d=document.getElementById('irrDetail').innerHTML.trim();document.getElementById('__tbProbe').textContent='IRRBLANK '+((document.getElementById('irrWarn').textContent.indexOf('留空不按 0 计算')>=0&&document.getElementById('irrValue').textContent==='--'&&d==='')?'OK':'BAD');"],
    expect: ["IRRBLANK OK"],
    ref: "第947批：第 1 期金额留空（null，不再 parseFloat||0）时 calc() 必须停止计算并提示，IRR 显示 --、明细为空；旧实现把空当 0 继续算出一个假 IRR。默认全额有值不命中。",
  },
  {
    slug: "finance/number-to-words",
    inputs: { inputVal: "999999999998.99999" },
    clicks: ["convert()"],
    expect: ["nine hundred ninety-eight point nine nine nine nine nine"],
    ref: "第947批：按输入字符串拆分整数/小数，不再先 parseFloat。999999999998.99999 的整数读法须以 ninety-eight 结尾；旧版浮点进位为 999999999999 会读成 ninety-nine。",
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: { rate: "" },
    clicks: ["calc()"],
    expect: ["年利率尚未填写；如确为 0% 请明确输入 0"],
    ref: "第947批：利率留空不再按 0 静默计算，提示用户显式填 0；默认 rate=6 不命中。",
  },
  {
    slug: "finance/lease-payment-calculator",
    inputs: { months: "1.5" },
    clicks: ["calc()"],
    expect: ["租期须为 1–360 的整数月"],
    ref: "第947批：1.5 期不再被 Math.floor 静默改成 1 期，明确拒绝小数；默认 60 期不命中。",
  },
  {
    slug: "finance/analysis-44",
    inputs: { items: "X,-500,600\nY,100,abc\nZ,100,-20\n主体工程,500000,530000" },
    clicks: ["calcBatch()"],
    expect: ["第 2 行「Y」：实际投资不是完整数字", "第 3 行「Z」：实际投资为负；退款冲减请单独记录"],
    ref: "第947批：批量逐行整串校验并输出行级错误。Y 的 abc、Z 的负支出都不得再被 parseFloat 部分吞下或当退款；第三行合法仍出表。旧实现仅 isFinite 且无行级错误，不命中。",
  },
  {
    slug: "finance/bond-yield-calculator",
    inputs: {},
    clicks: ["switchMethod('current');document.getElementById('c-price').value='';calc();var g=document.getElementById('statGrid').innerHTML.trim();document.getElementById('__tbProbe').textContent='BONDCLEAR '+((g===''&&document.getElementById('res').innerHTML.indexOf('请填写当前价格')>=0)?'OK':'BAD');"],
    expect: ["BONDCLEAR OK"],
    ref: "第947批：按当前模式校验输入；当期收益率模式清空价格必须拒绝，且 statGrid 旧结果一并清空，不能只改文字。默认 YTM 有效结果 statGrid 有内容 ⇒ 强判别。",
  },
  {
    slug: "finance/compound-interest",
    inputs: { principal: "10000", rate: "1000000", years: "100", annual: "0" },
    clicks: ["calc()"],
    expect: ["数值溢出：当前利率与年限组合超出可计算范围", "请降低年化利率或缩短年限后重试"],
    ref: "第947批：利率 1,000,000%、100 年使余额溢出 Infinity；必须在入表前停止，清空年表/图表且 totalFV 显示 --。旧实现继续渲染 Infinity 年表并允许导出，不命中。",
  },
  {
    slug: "finance/inflation-calculator",
    inputs: { amt: "10000", rate: "-5", years: "10" },
    clicks: ["calc()"],
    expect: ["购买力增加：67.02%", "通缩使同样金额能买到更多"],
    ref: "第947批：负通胀（通缩）下购买力上升，文案按方向写“购买力增加”，不再固定“缩水”。默认 rate=3 走缩水分支不命中。",
  },
  {
    slug: "finance/inflation-calculator",
    inputs: { amt: "10000", rate: "-100", years: "10" },
    clicks: ["calc()"],
    expect: ["年通胀率须大于 -100%"],
    ref: "第947批：-100% 使价格因子为 0，必须明确拒绝而不是输出 Infinity/0 折现；默认 3% 不命中。",
  },
  // ===== 第948批新增 =====
  {
    slug: "finance/stock-profit-calculator",
    inputs: { buyPrice: "10", buyQty: "100", sellPrice: "10", commissionRate: "0", stampRate: "0", transferRate: "0", minCommission: "100000" },
    clicks: ["calc();"],
    expect: ["2,010.00 元/股"],
    ref: "第948批：最低佣金 10 万元时真实保本价 2010 元；旧固定上界 200 元导致搜索停在 200 附近。分段解析解直接命中 2010。",
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "8", housePrice: "300", age: "", loanYears: "20", rate: "2.85" },
    clicks: ["calc()"],
    expect: ["年龄须填写 18–70 岁的整数"],
    ref: "第948批：年龄留空不再静默按 30 岁；默认 35 不命中。",
  },
  {
    slug: "finance/housing-fund-loan",
    inputs: { balance: "8", housePrice: "300", age: "35", loanYears: "20", rate: "0" },
    clicks: ["calc()"],
    expect: ["每月还款", "5,000 元", "利息总额", "0 元"],
    ref: "第948批：显式 0% 利率按零利率公式，月供=120 万/240=5000、利息 0；旧实现等额本息分支利率为 0 时月供保持 0。",
  },
  {
    slug: "finance/option-profit-calculator",
    inputs: { strike: "100", premium: "5", mult: "100", contracts: "1", fee: "2", s0: "105" },
    clicks: ["calc();"],
    expect: ["105.04", "每股净盈亏（含费用）", "-0.04"],
    ref: "第948批：K100/P5/乘数100/1张/单边费2，S=105 总净盈亏 -4 元；平衡点 105.04，每股净盈亏 -0.04，收益率 -0.8%。旧版未把费用计入收益率与曲线。",
  },
  {
    slug: "finance/analysis-5",
    inputs: { ca: "500000", inv: "10000", pre: "240000", cash: "80000", cl: "300000", tl: "700000", ta: "1200000" },
    clicks: ["calc();"],
    expect: ["主要拖累项为预付费用（占流动资产 48.0%）", "可调整的经验参考"],
    ref: "第948批：速动 0.83 的真因是预付费用 48%，旧版一律归因存货占比高。默认 18/2 万时存货占 36% 且预付 4%，不命中。",
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "4000", insurance: "0", special: "0", threshold: "5000", bonus: "12000", bonusMode: "auto" },
    clicks: ["calculate()"],
    expect: ["并入综合所得（年度累进表）", "¥0.00", "全年少缴 ¥360.00"],
    ref: "第948批：月薪 4000 低于 5000 起征点，年度未用扣除 1.2 万先抵奖金，合并税额应为 0 而非 360；旧版先把月应纳税所得额截 0 再×12。",
  },
  {
    slug: "finance/discount-calculator",
    inputs: {},
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/discount-calculator.html','utf8');var ok=(h.match(/class=\"qs-item\"/g)||[]).length===9&&h.indexOf('<button type=\"button\" class=\"qs-item\"')>=0&&h.indexOf('aria-label=\"第 ${i + 1} 级折扣')>=0&&h.indexOf('aria-label=\"删除第 ${i + 1} 级折扣\"')>=0;document.getElementById('__tbProbe').textContent='QSA11Y '+(ok?'OK':'BAD');"],
    expect: ["QSA11Y OK"],
    ref: "第948批：9 个快捷项改为语义 button 并带折扣 aria-label；动态第 2 级输入带序号名称。旧 div 无法键盘聚焦且动态输入无名称。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { dt_income: "20", dt_expense: "12", dt_debt: "80", dt_existing: "10", assumeMultiple: "5", assumeHealthMin: "50", assumePremiumPct: "8" },
    clicks: ["calc();"],
    expect: ["年收入20万×5 + 负债80万 − 已有保障10万 = 170万", "年收入×8%"],
    ref: "第948批：收入倍数/重疾最低/保费比例可调，5 倍时寿险 170 万、保费 1.6 万；旧版写死 10 倍与 10% 不命中。",
  },

  {
    slug: "finance/futures-pnl-calculator",
    inputs: {},
    clicks: ["var v={openPrice:'3500',closePrice:'3501',lots:'1',marginRate:'12',openFee:'1000',closeFee:'1000'};Object.keys(v).forEach(function(k){document.getElementById(k).value=v[k];});setDirection(1);calc();"],
    expect: ["盈亏金额", "+1.00", "毛盈亏 300.00", "-1,700.00"],
    ref: "第949批：点数 +1.00 与净亏损并存时，点数按价格方向显示正号与红色，净盈亏另按扣费结果显示；旧版点数沿用净亏损符号。",
  },
  {
    slug: "finance/voter-id-validator",
    inputs: { input: "ABC1234567" },
    clicks: ["validate()"],
    expect: ["输入（已脱敏）： AB••••••67"],
    ref: "第949批：选民号仅内存校验，输出只显示脱敏号码；旧版输入区显示完整号码并写入历史。",
  },
  {
    slug: "finance/tax-calculator",
    inputs: { salary: "30000", insurance: "3000", special: "2000", threshold: "5000", bonus: "0", bonusMode: "auto" },
    clicks: ["calculate()"],
    expect: ["第 3 级", "20% ✓ 适用"],
    ref: "第949批：应纳税所得额 2 万落在 1.2 万–2.5 万档，动态档位文本应为第 3 级、20% 适用；旧版档位文案固定中文且重算后英文态可能残留。",
  },
  {
    slug: "finance/mortgage-calculator",
    inputs: { loanAmount: "100", rate: "4.2", years: "30", downPayment: "30" },
    clicks: ["calculate();var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/finance/mortgage-calculator.html','utf8');var ok=h.indexOf('Payment amount (CNY)')>=0&&h.indexOf('Show all payments')>=0&&h.indexOf('Collapse (first 24)')>=0;document.getElementById('__tbProbe').textContent='MORTGAGE I18N '+(ok?'OK':'BAD');"],
    expect: ["MORTGAGE I18N OK"],
    ref: "第949批：明细提示、展开按钮与 CSV 列名按当前语言生成；旧版固定中文，英文态展开/下载后出现中文。",
  },
  {
    slug: "finance/tfn-validator",
    inputs: {},
    clicks: ["document.getElementById('input').value='876543210';validate();"],
    expect: ["长度与校验和检查通过", "无法确认该号码是否已分配、当前状态或归属某人"],
    ref: "第949批：校验和通过只证明长度与校验和匹配，不再宣称号码有效；旧版输出「TFN 号码有效」。",
  },
  {
    slug: "finance/insurance-calculator",
    inputs: { lv_age: "30", lv_retire: "60", lv_income: "20", lv_growth: "3", lv_consume: "120", lv_discount: "5", assumeMultiple: "10", assumeHealthMin: "30", assumePremiumPct: "10" },
    clicks: ["switchMethod('life-value')"],
    expect: ["个人消费占比须不大于 100"],
    ref: "第949批：生命价值法逐字段校验，个人消费占比 120% 越界明确拒绝并清空结果；旧版 getVal 直接按 1.2 消费计算，产出不合理的负生命价值。空输入拒绝另由 Puppeteer 真机覆盖。",
  },
  {
    slug: "finance/depreciation-calculator",
    inputs: { cost: "100000", salvage: "100000", life: "5", totalUnits: "10000", yearUnits: "3000,2500,2000,1500,1000" },
    clicks: ["calc();var lg=document.getElementById('legend');document.getElementById('__tbProbe').textContent=(lg.children.length===0&&document.getElementById('compareTable').textContent.trim()==='')?'DEP OK':'DEP BAD';"],
    expect: ["DEP OK"],
    ref: "第949批：残值等于原值时拒绝计算，同时清空图例与表格，避免残留上一方案曲线；旧版只清表格。",
  },
  {
    slug: "finance/mortgage-calculator",
    inputs: { loanAmount: "0.000001", rate: "0", years: "30", downPayment: "0" },
    clicks: ["calculate()"],
    expect: ["按分舍入后月供为 0.00 元", "不能生成正常还款计划"],
    ref: "第940批：本金 0.01 元、0% 利率、30 年，月供 0.0000278 元按分舍入为 0；旧实现把全部余额塞进首期并显示已结清，现明确拒绝并提示无法生成正常计划。默认 100 万/4.2% 不命中。"
  },
  {
    slug: "finance/mortgage-calculator",
    inputs: { loanAmount: "0.000012", rate: "100", years: "30", downPayment: "0" },
    clicks: ["calculate()"],
    expect: ["按分舍入后月供为 0.01 元", "不足以覆盖当期利息"],
    ref: "第940批：本金 0.12 元、100% 利率、30 年，月供与首期利息均按分舍入为 0.01 元，月供不高于利息；旧实现首期本金为 0 后直接结清，现拒绝。"
  },
  {
    slug: "finance/register-depreciation",
    inputs: {},
    clicks: ["assets=[{id:'OLD',name:'超龄设备',cat:'其他',date:'2025-01-01',cost:10000,salvage:0,life:101,method:'straight'},{id:'NEW',name:'正常设备',cat:'其他',date:'2025-01-01',cost:10000,salvage:0,life:5,method:'straight'}];renderSummary();renderList();document.getElementById('aName').value='新购资产';document.getElementById('aCost').value='2000';document.getElementById('aSalvage').value='0';document.getElementById('aLife').value='5';addAsset();var raw=JSON.parse(localStorage.getItem('tb_assets'));var listHtml=String(document.getElementById('assetList').innerHTML);var sumHtml=String(document.getElementById('summaryGrid').innerHTML);document.getElementById('__tbProbe').textContent='RD3 '+((raw.length===3&&raw.filter(function(a){return a.life===101;}).length===1&&listHtml.indexOf('待修正旧记录')>=0&&sumHtml.indexOf('待修正旧记录')>=0)?'OK':'BAD')+' '+raw.length;"],
    expect: ["RD3 OK 3"],
    ref: "第946批：加载含 101 年旧记录的台账后新增一条资产，save 必须保留全部 3 条（旧记录 1 条 life=101 不丢失），并在列表与汇总区展示「待修正旧记录」；旧实现加载即 filter，新增后 localStorage 只剩 2 条。"
  },

];

// ---------------------------------------------------------------- main
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

  console.log("==== finance calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();