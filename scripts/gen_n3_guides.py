# -*- coding: utf-8 -*-
"""N3 高价值指南扩容生成器：25 篇使用指南，分 5 批落地（每批 5 篇）。
复用 scripts/gen_guides2.py 的范式：写指南 HTML + 合并 json/guides.json + 更新 guides/index.html。
运行：python3 scripts/gen_n3_guides.py <batch>    # batch = 1..5
"""
import os, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
SITE = 'https://chenguangwu.github.io'

# 每篇：slug(=工具 basename 去 .html), ind, base(工具文件名), name, desc, intro,
#       features, scenarios, steps, tips, faqs[(q,a),...]
BATCHES = [
 # ---- batch 01 ----
 [
  {
   'slug': 'calc-1',
   'ind': 'accounting',
   'base': 'calc-1.html',
   'name': '增值税计算',
   'desc': '增值税计算使用指南：输入销售额、进项税额与税率，自动计算应纳税额与税负。',
   'intro': '增值税是对商品流转环节增值额征收的税种。本工具按"应纳税额 = 销项税额 − 进项税额"计算，输入不含税销售额、适用税率与已认证的进项税额，即可得出当期应纳增值税，全程本地计算。',
   'features': ['输入不含税销售额与适用税率(13%/9%/6%等)', '自动计算销项税额', '扣除已认证进项税额得出应纳税额', '支持小规模纳税人征收率(3%)速算', '显示税负率便于测算'],
   'scenarios': ['小规模/一般纳税人测算当期增值税', '报价前反推含税与不含税金额', '比对不同税率下的税负差异'],
   'steps': ['选择纳税人类型与适用税率', '输入不含税销售额', '输入可抵扣的进项税额', '点击计算查看销项、进项与应纳税额', '按需切换含税/不含税口径'],
   'tips': ['工具按"增值额"计税，进项须取得合规抵扣凭证才计入', '含税价转不含税价 = 含税价 ÷(1+税率)', '小规模纳税人通常用 3% 征收率，不抵扣进项'],
   'faqs': [('为什么算出来要减进项税额？', '增值税只对"增值"部分征收，进项税是你替上游垫付、可抵扣的税额。'), ('能给个例子吗？', '不含税销售额 10000 元、税率 13%，销项 1300 元；若已有进项 300 元，则应纳 1000 元。')],
   'en_name': 'VAT Calculator',
   'en_desc': 'VAT Calculator Guide: enter sales, input tax and rate to compute the payable VAT and tax burden.',
   'en_intro': 'VAT is levied on the value added at each stage of circulation. This tool computes "payable VAT = output tax − input tax". Enter the ex-tax sales, applicable rate and certified input tax to get the current payable VAT, all locally.',
   'en_features': ['Enter ex-tax sales and rate (13%/9%/6% etc.)', 'Auto-compute output tax', 'Subtract certified input tax for payable VAT', 'Small-rate (3%) quick calc for small businesses', 'Show tax-burden rate'],
   'en_scenarios': ['Estimate current VAT for small/general taxpayers', 'Reverse含税/不含税 before quoting', 'Compare burden across rates'],
   'en_steps': ['Pick taxpayer type and rate', 'Enter ex-tax sales', 'Enter deductible input tax', 'Click to see output/input/payable', 'Toggle含税/不含税'],
   'en_tips': ['VAT is on value added; input needs a valid certificate to count', 'Ex-tax = 含税 ÷ (1+rate)', 'Small businesses usually use 3%, no input deduction'],
   'en_faqs': [('Why subtract input tax?', 'VAT hits only the "added" part; input tax is paid upstream and deductible.'), ('Can you show an example?', 'Ex-tax 10000, rate 13% → output 1300; with input 300, payable 1000.')],
  },

  {
   'slug': 'simple-interest',
   'ind': 'banking',
   'base': 'simple-interest.html',
   'name': '单利利息',
   'desc': '单利利息使用指南：输入本金、年利率与年限，计算单利利息与到期总额。',
   'intro': '单利是按原始本金计息、利息不再生息的方式。公式：利息 = 本金 × 年利率 × 年限。输入本金、年利率(%)与年限，即时得到利息与本息和。',
   'features': ['输入本金/年利率/年限', '实时计算单利利息与到期总额', '切换按年/按月(年限可为小数)', '对比复利差异的提示'],
   'scenarios': ['民间借贷利息估算', '短期理财收益测算', '教学演示单利与复利区别'],
   'steps': ['输入本金(元)', '输入年利率(如 5 表示 5%)', '输入年限(可为 0.5 等小数)', '查看利息与本息和'],
   'tips': ['单利利息不产生"利滚利"', '年利率用百分数(5 即 0.05)', '年限支持小数，如 1.5 年'],
   'faqs': [('单利和复利差在哪？', '单利只对本金计息，复利连本带息再计息；长期下复利明显更高。'), ('能给个例子吗？', '本金 10000、年利率 5%、1 年，利息 = 10000×0.05×1 = 500 元，到期 10500 元。')],
   'en_name': 'Simple Interest',
   'en_desc': 'Simple Interest Guide: enter principal, annual rate and years to compute simple interest and maturity amount.',
   'en_intro': 'Simple interest accrues only on the original principal, not on interest. Formula: interest = principal × annual rate × years. Enter principal, annual rate (%) and years for instant interest and total.',
   'en_features': ['Enter principal/rate/years', 'Real-time simple interest and maturity', 'Yearly/monthly toggle (years can be decimal)', 'Note comparing with compound'],
   'en_scenarios': ['Private loan interest estimate', 'Short-term wealth return', 'Teach simple vs compound'],
   'en_steps': ['Enter principal', 'Enter annual rate (5 means 5%)', 'Enter years (decimal like 0.5 ok)', 'View interest and total'],
   'en_tips': ['Simple interest does not compound', 'Rate in % not decimal', 'Long tenor makes compound much larger'],
   'en_faqs': [('Simple vs compound?', 'Simple never compounds interest; compound earns on interest too.'), ('Can you show an example?', 'Principal 10000, 5%, 2 years → interest 1000, total 11000.')],
  },

  {
   'slug': 'break-even-units',
   'ind': 'accounting',
   'base': 'break-even-units.html',
   'name': '盈亏平衡产量',
   'desc': '盈亏平衡产量使用指南：输入固定成本、单价与单位变动成本，计算不亏本的最小销量。',
   'intro': '盈亏平衡点(BEP)是收入等于总成本、利润为零的产销量。公式：BEP = 固定成本 ÷(单价 − 单位变动成本)。输入三项即可得到保本销量与保本销售额。',
   'features': ['输入固定成本/单价/单位变动成本', '计算保本销量与保本金额', '显示单位边际贡献', '校验单价>变动成本避免无解'],
   'scenarios': ['创业测算最少卖多少才不亏', '定价决策对比不同单价下的保本点', '评估新产品的可行性'],
   'steps': ['输入固定成本(房租/工资等)', '输入销售单价', '输入每单位变动成本(材料/运费)', '点击计算查看保本销量与保本金额'],
   'tips': ['单价必须高于单位变动成本，否则边际贡献为负、永远无法保本', '保本金额 = 保本销量 × 单价'],
   'faqs': [('固定成本和变动成本怎么分？', '固定成本不随产量变(租金)，变动成本随产量正比(原材料)。'), ('能给个例子吗？', '固定成本 10000、单价 50、单位变动 30，则 BEP = 10000÷(50−30)=500 件。')],
   'en_name': 'Break-Even Units',
   'en_desc': 'Break-Even Units Guide: enter fixed cost, price and variable cost per unit to find the break-even point.',
   'en_intro': 'Break-even is where total revenue equals total cost. Enter fixed cost, unit price and unit variable cost to compute units and revenue needed to break even.',
   'en_features': ['Fixed cost / price / unit variable cost', 'Break-even units and revenue', 'Contribution margin view', 'Local computation'],
   'en_scenarios': ['New product feasibility', 'Set sales targets', 'Pitch financials to investors'],
   'en_steps': ['Enter fixed cost', 'Enter unit price and variable cost', 'View break-even units and revenue'],
   'en_tips': ['Price must exceed variable cost or never breaks even', 'Each unit sold covers fixed cost after margin', 'Sensitivity: lower fixed → lower target'],
   'en_faqs': [('What is contribution margin?', 'Price minus variable cost; it covers fixed cost per unit sold.'), ('Can you show an example?', 'Fixed 10000, price 50, var 30 → BE 500 units.')],
  },

  {
   'slug': 'effective-annual-rate',
   'ind': 'banking',
   'base': 'effective-annual-rate.html',
   'name': '有效年利率 (EAR)',
   'desc': '有效年利率(EAR)使用指南：输入名义年利率与每年复利次数，计算真实年化收益率。',
   'intro': '名义利率若按月/按日复利，真实年化收益会高于名义值。EAR = (1 + 名义利率/n)^n − 1。输入名义年利率与复利次数(如 12 表示按月)，得到有效年利率。',
   'features': ['输入名义年利率与复利次数 n', '计算 EAR 有效年利率', '对比不同复利频率的真实收益', '支持连续复利提示'],
   'scenarios': ['比较不同计息周期的存款/理财真实收益', '读懂"年化"背后的复利效应', '贷款实际成本折算'],
   'steps': ['输入名义年利率(如 6 表示 6%)', '输入每年复利次数(12=月,4=季,365=日)', '查看 EAR 结果'],
   'tips': ['复利次数越多 EAR 越高', '日复利(n=365)已接近连续复利', 'EAR 永远 ≥ 名义利率'],
   'faqs': [('为什么 EAR 比名义利率高？', '因为利息也在生息(利滚利)。'), ('能给个例子吗？', '名义 6%、按月复利，EAR = (1+0.06/12)^12 − 1 ≈ 6.17%。')],
   'en_name': 'Effective Annual Rate',
   'en_desc': 'Effective Annual Rate (EAR) Guide: convert a nominal rate with periodic compounding into the true annual rate.',
   'en_intro': 'EAR reflects the real annual cost when interest compounds more than once a year. Enter the nominal rate and compounding frequency to get EAR.',
   'en_features': ['Nominal rate and frequency input', 'Compute EAR', 'Compare nominal vs effective', 'Local computation'],
   'en_scenarios': ['Compare loan/card offers', 'Understand true borrowing cost', 'Teaching APR vs EAR'],
   'en_steps': ['Enter nominal annual rate', 'Enter compounding per year', 'View EAR'],
   'en_tips': ['EAR is always ≥ nominal when compounding >1', 'Credit cards compound daily — EAR much higher', 'Use EAR to compare honestly'],
   'en_faqs': [('EAR vs APR?', 'APR is nominal; EAR includes compounding, the true cost.'), ('Can you show an example?', 'Nominal 12% monthly → EAR ≈ 12.68%.')],
  },

  {
   'slug': 'fd-quarterly',
   'ind': 'banking',
   'base': 'fd-quarterly.html',
   'name': '定期存款（按季复利）',
   'desc': '定期存款(按季复利)使用指南：输入本金、年利率与年限，计算按季度复利到期的本息总额。',
   'intro': '定期存款若按季结息并转存，实际是季度复利。公式：到期额 = 本金 ×(1 + 年利率/4)^(4×年限)。输入三项即得到期金额与总利息。',
   'features': ['输入本金/年利率/年限', '按季度复利计算到期本息', '显示总利息', '与单利对比展示复利增益'],
   'scenarios': ['规划定期存款到期金额', '比较不同存期收益', '教学复利计算'],
   'steps': ['输入本金', '输入年利率(如 2.75)', '输入存期年限(可为小数)', '查看季度复利到期额与利息'],
   'tips': ['季度复利每年计息 4 次', '存期越长复利增益越明显', '年利率用百分数输入'],
   'faqs': [('按季复利和按年计息差多少？', '按季把利息再投资，到期略高。'), ('能给个例子吗？', '本金 10000、年利率 4%、存 2 年，到期 = 10000×(1+0.04/4)^8 ≈ 10828.75 元。')],
   'en_name': 'Fixed Deposit Quarterly',
   'en_desc': 'Fixed Deposit (Quarterly) Guide: compute maturity of a term deposit with quarterly compounding.',
   'en_intro': 'For a fixed deposit paying quarterly, interest compounds four times a year. Enter principal, annual rate and months to see maturity.',
   'en_features': ['Principal / rate / months', 'Quarterly compounding', 'Maturity value', 'Local computation'],
   'en_scenarios': ['Compare bank deposits', 'Plan short-term savings', 'Teaching compounding'],
   'en_steps': ['Enter principal and annual rate', 'Enter months', 'View maturity'],
   'en_tips': ['Quarterly means 4 compounding periods a year', 'Early withdrawal usually loses interest', 'Rate is annual nominal'],
   'en_faqs': [('Quarterly vs annual?', 'Quarterly compounds more often, slightly higher return.'), ('Can you show an example?', '10000 at 4% for 12 months quarterly ≈ 10406.')],
  },

 ],

 # ---- batch 02 ----
 [
  {
   'slug': 'fraction-calculator',
   'ind': 'science',
   'base': 'fraction-calculator.html',
   'name': '分数计算器',
   'desc': '分数计算器使用指南：支持分数加减乘除与约分，输出最简分数与小数。',
   'intro': '处理真分数/假分数/带分数的四则运算，自动通分、约分并给出最简结果与小数近似。纯本地计算。',
   'features': ['分数加/减/乘/除', '自动约分至最简', '输出小数近似', '支持带分数输入', '显示计算过程'],
   'scenarios': ['学生作业检查', '食谱分量按比例缩放', '工程尺寸分数换算'],
   'steps': ['输入第一个分数的分子分母', '选择运算符', '输入第二个分数', '点击计算查看最简结果与小数'],
   'tips': ['结果自动约分到最简(如 2/4→1/2)', '除分数等于乘其倒数', '分母为 0 会报错'],
   'faqs': [('带分数怎么输入？', '先化成假分数再输入，如 1½ = 3/2。'), ('能给个例子吗？', '1/2 + 1/4 = 2/4 + 1/4 = 3/4 = 0.75。')],
   'en_name': 'Fraction Calculator',
   'en_desc': 'Fraction Calculator Guide: add, subtract, multiply and divide fractions, with auto-simplification to the lowest terms and a decimal result.',
   'en_intro': 'Work with proper, improper and mixed fractions: the tool finds a common denominator, simplifies automatically and shows the simplest result plus a decimal approximation. Local computation.',
   'en_features': ['Add/subtract/multiply/divide fractions', 'Auto-simplify to lowest terms', 'Decimal approximation', 'Mixed-number input', 'Show the steps'],
   'en_scenarios': ['Check student homework', 'Scale recipe amounts', 'Convert fractional engineering dimensions'],
   'en_steps': ['Enter numerator and denominator of the first fraction', 'Pick an operator', 'Enter the second fraction', 'Click calculate to see the simplest result and decimal'],
   'en_tips': ['Results auto-reduce (e.g. 2/4 → 1/2)', 'Dividing by a fraction = multiplying by its reciprocal', 'A zero denominator raises an error'],
   'en_faqs': [('How do I enter a mixed number?', 'Convert it to an improper fraction first, e.g. 1½ = 3/2.'), ('Can you show an example?', '1/2 + 1/4 = 2/4 + 1/4 = 3/4 = 0.75.')],
  },

  {
   'slug': 'gcd-calculator',
   'ind': 'science',
   'base': 'gcd-calculator.html',
   'name': '最大公约数',
   'desc': '最大公约数(GCD)使用指南：输入多个整数，计算它们的最大公约数并展示步骤。',
   'intro': '最大公约数是能同时整除一组数的最大正整数。采用辗转相除法(欧几里得算法)逐步求解，支持两个数或更多数。',
   'features': ['输入两个或多个整数', '辗转相除法展示步骤', '支持负数取绝对值', '与最小公倍数联动'],
   'scenarios': ['分数约分', '任务分组/周期对齐', '密码学基础运算'],
   'steps': ['输入整数 a 与 b', '点击计算', '查看 GCD 及每一步余数变化'],
   'tips': ['GCD(a,b) 对负数取绝对值后计算', '多个数可逐个两两求 GCD', 'GCD 为 1 说明互质'],
   'faqs': [('三个数怎么求？', '先求前两个的 GCD，再与第三个数求 GCD。'), ('能给个例子吗？', 'GCD(48,18)：48=18×2+12，18=12×1+6，12=6×2+0 → GCD=6。')],
   'en_name': 'Greatest Common Divisor',
   'en_desc': 'Greatest Common Divisor (GCD) Guide: enter several integers to compute their GCD and show the steps.',
   'en_intro': 'The greatest common divisor is the largest positive integer dividing a set of numbers. Solved step by step with the Euclidean algorithm (successive division), for two or more numbers.',
   'en_features': ['Two or more integers', 'Euclidean steps shown', 'Negatives use absolute value', 'Works with LCM'],
   'en_scenarios': ['Reduce fractions', 'Align task groups / cycles', 'Foundations of cryptography'],
   'en_steps': ['Enter integers a and b', 'Click calculate', 'See the GCD and each remainder change'],
   'en_tips': ['GCD(a,b) uses absolute value for negatives', 'More than two: take GCD pairwise', 'GCD = 1 means coprime'],
   'en_faqs': [('How with three numbers?', 'Take the GCD of the first two, then GCD with the third.'), ('Can you show an example?', 'GCD(48,18): 48=18×2+12, 18=12×1+6, 12=6×2+0 → GCD=6.')],
  },

  {
   'slug': 'lcm-calculator',
   'ind': 'science',
   'base': 'lcm-calculator.html',
   'name': '最小公倍数',
   'desc': '最小公倍数(LCM)使用指南：输入多个整数，计算最小公倍数，常与 GCD 配合。',
   'intro': '最小公倍数是能被一组数同时整除的最小正整数。利用 LCM(a,b)=|a×b|÷GCD(a,b) 计算，支持多个数。',
   'features': ['输入多个整数', '基于 GCD 求 LCM', '支持负数取绝对值', '分步展示'],
   'scenarios': ['分数通分', '周期事件对齐(如每 3 天与每 4 天重合)', '排班轮换'],
   'steps': ['输入整数', '点击计算', '查看 LCM 结果'],
   'tips': ['LCM×GCD = |a×b|', '多个数可两两求 LCM', 'LCM 不会小于其中最大数'],
   'faqs': [('和 GCD 什么关系？', 'LCM(a,b)=a×b÷GCD(a,b)。'), ('能给个例子吗？', 'LCM(4,6)=4×6÷GCD(4,6)=24÷2=12。')],
   'en_name': 'Least Common Multiple',
   'en_desc': 'Least Common Multiple (LCM) Guide: enter several integers to compute the LCM, often used with GCD.',
   'en_intro': 'The least common multiple is the smallest positive integer divisible by a set of numbers. Uses LCM(a,b)=|a×b|÷GCD(a,b), for multiple numbers.',
   'en_features': ['Several integers', 'LCM from GCD', 'Negatives use absolute value', 'Step-by-step'],
   'en_scenarios': ['Common denominator for fractions', 'Align periodic events (every 3 vs every 4 days)', 'Shift rotation'],
   'en_steps': ['Enter integers', 'Click calculate', 'See the LCM result'],
   'en_tips': ['LCM × GCD = |a×b|', 'More than two: take LCM pairwise', 'LCM is never smaller than the largest number'],
   'en_faqs': [('Relation to GCD?', 'LCM(a,b)=a×b÷GCD(a,b).'), ('Can you show an example?', 'LCM(4,6)=4×6÷GCD(4,6)=24÷2=12.')],
  },

  {
   'slug': 'quadratic-equation',
   'ind': 'science',
   'base': 'quadratic-equation.html',
   'name': '一元二次方程求解',
   'desc': '一元二次方程求解使用指南：输入 a/b/c，求根公式给出实根/复根与判别式。',
   'intro': '形如 ax²+bx+c=0 的方程，判别式 Δ=b²−4ac 决定根的性质。公式 x=(−b±√Δ)/(2a)，自动给出两个实根或共轭复根。',
   'features': ['输入系数 a/b/c', '计算判别式 Δ', '给出两个实根或复根', '显示求根公式与步骤', 'a≠0 校验'],
   'scenarios': ['物理抛物线运动求落点', '利润最大化建模', '中学数学验算'],
   'steps': ['输入 a/b/c(a≠0)', '点击求解', '查看 Δ 与两个根'],
   'tips': ['Δ>0 两实根，Δ=0 一重根，Δ<0 两共轭复根', '复根含虚数单位 i', '系数为 0 时提示非一元二次'],
   'faqs': [('没有实数解怎么办？', 'Δ<0 时出现复根，工具会以 a±bi 形式给出。'), ('能给个例子吗？', 'x²−5x+6=0，Δ=25−24=1，根 x=2 与 x=3。')],
   'en_name': 'Quadratic Equation Solver',
   'en_desc': 'Quadratic Equation Solver Guide: enter a/b/c; the formula gives real/complex roots and the discriminant.',
   'en_intro': 'For ax²+bx+c=0, the discriminant Δ=b²−4ac decides the root type. Formula x=(−b±√Δ)/(2a) yields two real or conjugate complex roots automatically.',
   'en_features': ['Enter a/b/c', 'Compute discriminant Δ', 'Two real or complex roots', 'Show formula and steps', 'Validate a≠0'],
   'en_scenarios': ['Physics: projectile landing point', 'Profit-maximization modeling', 'High-school math check'],
   'en_steps': ['Enter a/b/c (a≠0)', 'Click solve', 'See Δ and the two roots'],
   'en_tips': ['Δ>0 two real, Δ=0 one double, Δ<0 two conjugate complex', 'Complex roots use the unit i', 'a=0 prompts "not quadratic"'],
   'en_faqs': [('No real solution?', 'When Δ<0 the roots are complex; the tool shows them as a±bi.'), ('Can you show an example?', 'x²−5x+6=0, Δ=25−24=1, roots x=2 and x=3.')],
  },

  {
   'slug': 'equation-balancer',
   'ind': 'science',
   'base': 'equation-balancer.html',
   'name': '化学方程式配平器',
   'desc': '化学方程式配平使用指南：输入反应式，自动配平各物质系数并校验原子守恒。',
   'intro': '根据质量守恒，调整反应物与生成物系数使两边每种原子数相等。输入如 "H2 + O2 = H2O"，工具给出配平后的 "2H2 + O2 = 2H2O"。',
   'features': ['支持多物种反应式输入', '矩阵法/代数法配平', '校验左右原子数守恒', '输出最简整数系数'],
   'scenarios': ['中学化学作业', '实验投料比估算', '理解质量守恒'],
   'steps': ['输入未配平方程式(用 + 连反应物，= 分隔生成物)', '点击配平', '查看配平系数与原子守恒表'],
   'tips': ['用 + 分隔物质、= 或 → 分隔两边', '系数默认最简整数', '无法配平(如信息不足)会提示'],
   'faqs': [('配平失败常见原因？', '物质写错、电荷未平衡或反应本身不成立。'), ('能给个例子吗？', 'H2 + O2 = H2O → 配平为 2H2 + O2 = 2H2O(4H、2O 两边守恒)。')],
   'en_name': 'Chemical Equation Balancer',
   'en_desc': 'Chemical Equation Balancer Guide: enter a reaction; auto-balance coefficients and verify atom conservation.',
   'en_intro': 'By mass conservation, adjust reactant and product coefficients until each atom count matches on both sides. Enter e.g. "H2 + O2 = H2O"; the tool returns "2H2 + O2 = 2H2O".',
   'en_features': ['Multi-species reaction input', 'Matrix / algebraic balancing', 'Verify atom conservation', 'Simplest integer coefficients'],
   'en_scenarios': ['High-school chemistry homework', 'Estimate feed ratios for experiments', 'Understand mass conservation'],
   'en_steps': ['Enter the unbalanced equation (+ between reactants, = separates products)', 'Click balance', 'See coefficients and the atom-conservation table'],
   'en_tips': ['Use + between species, = or → between sides', 'Coefficients are simplest integers', 'Unbalanceable input (incomplete) is reported'],
   'en_faqs': [('Common reasons it fails?', 'Wrong species, unbalanced charge, or a reaction that does not hold.'), ('Can you show an example?', 'H2 + O2 = H2O → 2H2 + O2 = 2H2O (4H, 2O conserved).')],
  },

 ],

 # ---- batch 03 ----
 [
  {
   'slug': 'pregnancy-due-date',
   'ind': 'health',
   'base': 'pregnancy-due-date.html',
   'name': '预产期计算器',
   'desc': '预产期计算器使用指南：输入末次月经或受孕日期，估算预产期与当前孕周。',
   'intro': '常用 Naegele 法则：末次月经(LMP)首日 + 280 天(40 周)估算预产期(EDC)。输入 LMP 或 B 超孕周，得到预产期与当前孕周、孕天数。',
   'features': ['按末次月经或受孕日推算', '输出预产期与孕周/天数', '提示早/中/晚孕期阶段', '本地计算不存储'],
   'scenarios': ['准妈妈记录孕期里程碑', '产检日程规划', '向家人同步预产期'],
   'steps': ['选择输入方式(末次月经/受孕日)', '输入对应日期', '点击计算查看预产期与当前孕周'],
   'tips': ['预产期为估算，仅约 5% 宝宝在当天出生', '月经周期不规律者以 B 超孕周更准', '本结果非医疗诊断'],
   'faqs': [('预产期准吗？', 'EDC 是统计估算，实际分娩多在 ±2 周内，仅供规划参考。'), ('能给个例子吗？', 'LMP 为 2026-01-01，EDC ≈ 2026-10-08(加 280 天)。')],
   'en_name': 'Pregnancy Due Date',
   'en_desc': 'Pregnancy Due Date Guide: enter LMP or conception date to estimate the due date and current week.',
   'en_intro': 'Common Naegele rule: LMP first day + 280 days (40 weeks) → EDC. Enter LMP or ultrasound week to get due date and current gestation. Local computation.',
   'en_features': ['By LMP or conception', 'Due date and week/days', 'Trimester hint', 'Local computation'],
   'en_scenarios': ['Track pregnancy milestones', 'Plan checkups', 'Share due date with family'],
   'en_steps': ['Choose input (LMP/conception)', 'Enter the date', 'View due date and gestation'],
   'en_tips': ['EDC is an estimate; only ~5% deliver on that day', 'Irregular cycles: use ultrasound week', 'Not a medical diagnosis'],
   'en_faqs': [('Is the due date exact?', 'It is a statistical estimate; real delivery is usually within ±2 weeks.'), ('Can you show an example?', 'LMP 2026-01-01 → EDC ≈ 2026-10-08 (+280 days).')],
  },

  {
   'slug': 'water-intake-calculator',
   'ind': 'health',
   'base': 'water-intake-calculator.html',
   'name': '每日饮水量计算器',
   'desc': '每日饮水量计算器使用指南：按体重、运动量与环境估算每日建议饮水量。',
   'intro': '常用基准约 30–35 mL/kg/天，再按运动时长与高温环境上浮。输入体重、运动时长与环境因素，得到每日建议饮水量(mL/杯数)。',
   'features': ['按体重给基准饮水量', '运动时长与高温上浮', '输出 mL 与约合数杯水(250mL/杯)', '本地计算'],
   'scenarios': ['健身/减脂期补水规划', '炎热户外作业饮水安排', '日常健康管理'],
   'steps': ['输入体重(kg)', '输入每日运动时长(分钟)', '勾选高温/干燥环境', '查看建议饮水量'],
   'tips': ['约 250–300 mL 为一杯', '咖啡/茶等利尿饮品不计入主要补水', '特殊疾病(肾/心)遵医嘱'],
   'faqs': [('一定要喝满吗？', '为区间建议，口渴、尿色浅黄即为充足信号，不必强迫。'), ('能给个例子吗？', '60kg、运动 30 分钟，基准约 60×35=2100mL，运动上浮约 +350mL，建议约 2450mL(≈10 杯)。')],
   'en_name': 'Daily Water Intake',
   'en_desc': 'Daily Water Intake Guide: estimate daily water need from weight, exercise and environment.',
   'en_intro': 'A common baseline is ~30–35 mL/kg/day, raised by exercise and heat. Enter weight, exercise minutes and environment for a daily target (mL/cups). Local computation.',
   'en_features': ['Base intake by weight', 'Exercise and heat adjustment', 'mL and cups (250mL)', 'Local computation'],
   'en_scenarios': ['Hydration in fitness/fat-loss', 'Outdoor hot-work planning', 'Daily health management'],
   'en_steps': ['Enter weight (kg)', 'Enter daily exercise minutes', 'Check hot/dry environment', 'View target'],
   'en_tips': ['~250–300 mL per cup', 'Coffee/tea are mild diuretics, not main hydration', 'Special conditions (kidney/heart) follow a doctor'],
   'en_faqs': [('Must you hit it exactly?', 'It is a range; thirst and light-yellow urine signal enough.'), ('Can you show an example?', '60kg, 30min exercise → ~2100mL +350 ≈ 2450mL (≈10 cups).')],
  },

  {
   'slug': 'heart-rate-zones',
   'ind': 'health',
   'base': 'heart-rate-zones.html',
   'name': '心率区间计算器',
   'desc': '心率区间计算器使用指南：输入年龄与静息心率，按储备心率法给出五档训练区间。',
   'intro': '采用 Karvonen 储备心率法：目标心率 = (最大心率 − 静息心率)×强度% + 静息心率，最大心率常用 220−年龄。输出燃脂/有氧/无氧等区间。',
   'features': ['输入年龄与静息心率', '五档强度区间(50%–90%)', '基于储备心率法更个性化', '本地计算'],
   'scenarios': ['制定有氧/减脂训练强度', '跑步机配速对应心率', '运动安全上限参考'],
   'steps': ['输入年龄', '输入静息心率(晨起静坐测得)', '选择强度档', '查看对应心率区间'],
   'tips': ['最大心率 ≈ 220−年龄 为经验值，个体差异大', '静息心率越低说明心肺越好', '本结果非医疗建议'],
   'faqs': [('储备心率法比最大心率法好？', '它纳入了静息心率，对训练者更个性化。'), ('能给个例子吗？', '30 岁、静息 60，最大≈190，储备=130；70% 强度区间=(190−60)×0.7+60=151 bpm。')],
   'en_name': 'Heart Rate Zones',
   'en_desc': 'Heart Rate Zones Guide: enter age and resting heart rate for five training zones by the Karvonen method.',
   'en_intro': 'Karvonen method: target HR = (max HR − resting HR) × intensity% + resting HR, max HR ≈ 220 − age. Output fat-burn/aerobic/anaerobic zones. Local computation.',
   'en_features': ['Age and resting HR input', 'Five intensity zones (50%–90%)', 'Reserve-based, personalized', 'Local computation'],
   'en_scenarios': ['Aerobic/fat-loss intensity', 'Treadmill pace to HR', 'Safety ceiling reference'],
   'en_steps': ['Enter age', 'Enter resting HR (morning, rested)', 'Pick intensity', 'View HR zone'],
   'en_tips': ['Max HR ≈ 220−age is a rule of thumb, varies', 'Lower resting HR = fitter heart', 'Not medical advice'],
   'en_faqs': [('Why reserve method?', 'It includes resting HR, more personal for trainees.'), ('Can you show an example?', '30y, rest 60, max≈190, reserve 130; 70% → 151 bpm.')],
  },

  {
   'slug': 'waist-hip-ratio',
   'ind': 'health',
   'base': 'waist-hip-ratio.html',
   'name': '腰臀比计算器',
   'desc': '腰臀比(WHR)计算器使用指南：输入腰围与臀围，评估中心性肥胖风险。',
   'intro': 'WHR = 腰围 ÷ 臀围，是评估腹部脂肪与心血管/代谢风险的重要指标。输入两项围度，得到 WHR 并给出风险分级(男/女阈值不同)。',
   'features': ['输入腰围与臀围', '计算 WHR', '按性别给风险分级', '本地计算'],
   'scenarios': ['减脂效果评估', '慢病风险自查', '健身围度记录'],
   'steps': ['输入腰围(脐部水平)', '输入臀围(最宽处)', '选择性别', '查看 WHR 与风险等级'],
   'tips': ['女性 WHR>0.85、男性>0.90 属中心性肥胖高风险', '测量时自然呼吸、软尺贴合不勒肉', '需配合 BMI 综合判断'],
   'faqs': [('男女标准不同？', '因脂肪分布差异，男性阈值更高。'), ('能给个例子吗？', '腰围 80cm、臀围 100cm，WHR=0.80(女性属健康范围)。')],
   'en_name': 'Waist-to-Hip Ratio',
   'en_desc': 'Waist-to-Hip Ratio (WHR) Guide: enter waist and hip to assess central obesity risk.',
   'en_intro': 'WHR = waist ÷ hip, a key indicator of abdominal fat and cardio/metabolic risk. Enter both for WHR and risk grade (thresholds differ by sex). Local computation.',
   'en_features': ['Waist and hip input', 'WHR', 'Risk grade by sex', 'Local computation'],
   'en_scenarios': ['Fat-loss evaluation', 'Chronic-risk self-check', 'Fitness circumference log'],
   'en_steps': ['Enter waist (navel level)', 'Enter hip (widest)', 'Pick sex', 'View WHR and grade'],
   'en_tips': ['Women WHR>0.85, men>0.90 = high central risk', 'Measure relaxed, soft tape snug', 'Combine with BMI'],
   'en_faqs': [('Different by sex?', 'Yes, due to fat distribution; men have a higher threshold.'), ('Can you show an example?', 'Waist 80cm, hip 100cm → WHR 0.80 (healthy for women).')],
  },

  {
   'slug': 'convert',
   'ind': 'fitness',
   'base': 'convert.html',
   'name': '跑步配速转换器',
   'desc': '跑步配速转换器使用指南：在分钟/公里配速与公里/小时速度间互转。',
   'intro': '配速(pace)是每公里耗时(分:秒)，速度是每小时公里数(km/h)。二者互为倒数：速度 = 60÷配速(分钟)。输入其一即得另一。',
   'features': ['配速↔速度互转', '支持分:秒输入', '实时换算', '本地计算'],
   'scenarios': ['按目标完赛时间反推配速', '跑步机速度换算野外配速', '训练计划制定'],
   'steps': ['输入配速(分:秒/公里)或速度(km/h)', '切换换算方向', '查看结果'],
   'tips': ['配速越小越快', '速度 = 60 ÷ 配速(分钟)，如配速 6:00 = 10 km/h', '长跑常用配速描述强度'],
   'faqs': [('配速和速度哪个常用？', '路跑多说配速(分/公里)，跑步机多显速度(km/h)。'), ('能给个例子吗？', '配速 5:00/公里 = 60÷5 = 12 km/h。')],
   'en_name': 'Running Pace Converter',
   'en_desc': 'Running Pace Converter Guide: convert between min/km pace and km/h speed.',
   'en_intro': 'Pace is minutes per km; speed is km per hour. They are reciprocal: speed = 60 ÷ pace(min). Enter either to get the other. Local computation.',
   'en_features': ['Pace ↔ speed', 'Min:sec input', 'Real-time', 'Local computation'],
   'en_scenarios': ['Reverse pace from goal time', 'Treadmill speed to outdoor pace', 'Training plan'],
   'en_steps': ['Enter pace (min:sec/km) or speed (km/h)', 'Switch direction', 'View result'],
   'en_tips': ['Smaller pace = faster', 'Speed = 60 ÷ pace(min); pace 6:00 = 10 km/h', 'Road runners use pace'],
   'en_faqs': [('Pace or speed?', 'Road runners say pace (min/km); treadmills show speed (km/h).'), ('Can you show an example?', 'Pace 5:00/km = 60÷5 = 12 km/h.')],
  },

 ],

 # ---- batch 04 ----
 [
  {
   'slug': 'favicon-generator',
   'ind': 'design',
   'base': 'favicon-generator.html',
   'name': 'Favicon 生成器',
   'desc': 'Favicon 生成器使用指南：上传图片或输入文字/Emoji，生成多尺寸网站图标并下载。',
   'intro': 'Favicon 是浏览器标签、书签栏显示的小图标，建议提供 16/32/48/180 等多尺寸以适配各设备。本工具本地生成，不上传图片。',
   'features': ['图片/文字/Emoji 生成图标', '输出多尺寸(含 apple-touch-icon)', '一键下载 .ico/.png', '本地处理不上传'],
   'scenarios': ['新网站/博客上线配图标', '替换老旧低清 favicon', 'App 桌面图标预览'],
   'steps': ['上传图片或输入文字/Emoji', '选择尺寸与格式', '预览效果', '点击下载'],
   'tips': ['透明背景 PNG 最通用', '苹果设备需 180×180 apple-touch-icon', '图标越简洁小尺寸越清晰'],
   'faqs': [('为什么要多尺寸？', '不同场景(标签/主屏)取不同尺寸，单图会模糊或裁切。'), ('能给个例子吗？', '上传正方形 Logo，生成 32×32 用于标签、180×180 用于 iPhone 主屏。')],
   'en_name': 'Favicon Generator',
   'en_desc': 'Favicon Generator Guide: upload an image or enter text/Emoji to generate multi-size icons and download.',
   'en_intro': 'A favicon is the small icon in browser tabs and bookmarks; provide 16/32/48/180 etc. for devices. Generated locally, image not uploaded.',
   'en_features': ['Image/text/Emoji to icon', 'Multiple sizes (incl. apple-touch-icon)', 'One-click .ico/.png', 'Local, not uploaded'],
   'en_scenarios': ['New site/blog launch icon', 'Replace old low-res favicon', 'App home-screen preview'],
   'en_steps': ['Upload image or enter text/Emoji', 'Pick size and format', 'Preview', 'Download'],
   'en_tips': ['Transparent PNG is most universal', 'Apple needs 180×180 apple-touch-icon', 'Simpler icon = clearer when small'],
   'en_faqs': [('Why multiple sizes?', 'Different surfaces (tab/home) use different sizes; one image blurs or crops.'), ('Can you show an example?', 'Upload a square logo → 32×32 for tab, 180×180 for iPhone home.')],
  },

  {
   'slug': 'image-compress',
   'ind': 'design',
   'base': 'image-compress.html',
   'name': '图片压缩',
   'desc': '图片压缩使用指南：本地压缩 JPEG/PNG/WebP，减小体积并预览前后对比。',
   'intro': '在不明显损失画质前提下降低图片体积，加快网页加载、节省存储。支持质量滑杆调节，所有处理在浏览器本地完成，图片不上传。',
   'features': ['JPEG/PNG/WebP 压缩', '质量滑杆实时调节', '显示压缩前后体积与比率', '原图/结果对比预览', '本地处理不上传'],
   'scenarios': ['网页/博客图片优化', '微信/邮件发送前瘦身', '手机相册导出压缩'],
   'steps': ['选择或拖入图片', '拖动质量滑杆看预览', '查看体积与压缩率', '点击下载'],
   'tips': ['照片类用 JPEG/WebP(有损)体积小', '线条/文字图用 PNG 保清晰', '质量 70–85 通常肉眼难辨'],
   'faqs': [('压缩会丢画质吗？', '有损格式会，但 80% 以上通常肉眼难察；可对比预览再决定。'), ('能给个例子吗？', '2MB 照片压到 300KB(约 85% 质量)，网页加载从 3s 降到 <1s。')],
   'en_name': 'Image Compressor',
   'en_desc': 'Image Compressor Guide: compress JPEG/PNG/WebP locally with before/after preview.',
   'en_intro': 'Shrink images without visible quality loss to speed up pages and save space. Quality slider supported, all in-browser, image not uploaded.',
   'en_features': ['JPEG/PNG/WebP compress', 'Quality slider', 'Show size and ratio', 'Before/after preview', 'Local, not uploaded'],
   'en_scenarios': ['Web/blog image optimization', 'Shrink before email/WeChat', 'Phone album export'],
   'en_steps': ['Choose or drop an image', 'Drag quality slider to preview', 'Check size and ratio', 'Download'],
   'en_tips': ['Photos: JPEG/WebP (lossy) smaller', 'Line/text: PNG keeps crisp', '70–85% usually imperceptible'],
   'en_faqs': [('Does it lose quality?', 'Lossy formats do, but ≥80% is usually imperceptible; preview to decide.'), ('Can you show an example?', '2MB photo → 300KB at ~85% quality, load 3s→<1s.')],
  },

  {
   'slug': 'image-format-converter',
   'ind': 'design',
   'base': 'image-format-converter.html',
   'name': '图片格式转换器',
   'desc': '图片格式转换器使用指南：在 PNG/JPEG/WEBP/BMP 间互转，本地处理不上传。',
   'intro': '不同格式适用不同场景：PNG 透明无损、JPEG 照片小、WebP 现代高效、BMP 无损无压。上传图片选择目标格式即可转换并下载。',
   'features': ['PNG/JPEG/WEBP/BMP 互转', '批量可选', '透明背景在 JPEG 下填白提示', '本地处理'],
   'scenarios': ['透明 Logo 转 PNG', '照片转 WebP 省流量', '老软件只认 BMP 时转换'],
   'steps': ['上传图片', '选择目标格式', '如需 JPEG 设置背景色', '点击转换并下载'],
   'tips': ['PNG→JPEG 会丢透明(变白底)', 'WebP 体积通常最小但老浏览器不兼容', '转换不改变像素内容只换封装'],
   'faqs': [('转 JPEG 透明没了？', 'JPEG 不支持透明，工具会用白底填充；需透明请留 PNG/WebP。'), ('能给个例子吗？', '透明 PNG Logo 转 JPEG 用于不支持透明的老系统，背景自动填充白色。')],
   'en_name': 'Image Format Converter',
   'en_desc': 'Image Format Converter Guide: convert between PNG/JPEG/WebP/BMP locally.',
   'en_intro': 'Formats fit different needs: PNG transparent lossless, JPEG small photos, WebP modern efficient, BMP lossless no compression. Upload and pick target, download. Local.',
   'en_features': ['PNG/JPEG/WebP/BMP', 'Batch optional', 'Transparent→white note for JPEG', 'Local processing'],
   'en_scenarios': ['Transparent logo to PNG', 'Photo to WebP to save traffic', 'Old software only takes BMP'],
   'en_steps': ['Upload image', 'Pick target format', 'Set background for JPEG', 'Convert and download'],
   'en_tips': ['PNG→JPEG drops transparency (white)', 'WebP smallest but old browsers incompatible', 'Conversion changes wrapper, not pixels'],
   'en_faqs': [('Transparency gone in JPEG?', 'JPEG has no alpha; tool fills white; keep PNG/WebP for transparency.'), ('Can you show an example?', 'Transparent PNG logo → JPEG for legacy systems, background auto white.')],
  },

  {
   'slug': 'text-diff',
   'ind': 'biz',
   'base': 'text-diff.html',
   'name': '文本差异对比',
   'desc': '文本差异对比使用指南：粘贴两段文本，高亮新增/删除/修改内容。',
   'intro': '逐行或逐字符比较两份文本，直观标出差异，适合核对代码、合同、文案的改动。纯前端，内容不上传。',
   'features': ['行/词级差异高亮', '新增(绿)/删除(红)标注', '支持长文本', '本地比对不上传'],
   'scenarios': ['代码改动复核', '合同/条款前后比对', '翻译稿与原文对照'],
   'steps': ['粘贴原文本到左框、改动文本到右框', '选择比较粒度(行/词)', '点击对比查看高亮差异'],
   'tips': ['行级适合大段改动、词级适合单句微调', '空行也算差异', '敏感文本本地处理更安全'],
   'faqs': [('为什么一整段都标红？', '可能是中间插入/删除了内容导致后续整体错位，改用词级比对更准。'), ('能给个例子吗？', '原文"你好世界"，改后"你好，世界"，词级高亮"世界"前多了"，"。')],
   'en_name': 'Text Diff',
   'en_desc': 'Text Diff Guide: paste two texts and highlight added / removed / changed content.',
   'en_intro': 'Compare two texts line by line or character by character, marking differences clearly — ideal for checking code, contracts or copy changes. Front-end only, nothing uploaded.',
   'en_features': ['Line / word-level highlight', 'Added (green) / removed (red) marks', 'Long-text support', 'Local compare, no upload'],
   'en_scenarios': ['Review code changes', 'Compare contract clauses before/after', 'Check translation against the original'],
   'en_steps': ['Paste original into the left box, changed into the right', 'Choose granularity (line/word)', 'Click compare to see highlighted diffs'],
   'en_tips': ['Line level for big edits, word level for single-sentence tweaks', 'Blank lines also count as diffs', 'Sensitive text is safer processed locally'],
   'en_faqs': [('Why is a whole block red?', 'An inserted/deleted chunk may shift everything after it; use word level for accuracy.'), ('Can you show an example?', 'Original "你好世界", changed "你好，世界" → word level highlights the added "，" before "世界".')],
  },

  {
   'slug': 'text-extract-urls',
   'ind': 'biz',
   'base': 'text-extract-urls.html',
   'name': '提取 URL',
   'desc': '提取 URL 使用指南：从大段文本中批量提取所有链接，去重并可复制。',
   'intro': '粘贴含链接的文章/日志/邮件，一键提取其中全部 http/https 链接，自动去重，方便批量检查或导出。本地处理。',
   'features': ['正则提取 http/https 链接', '自动去重', '按出现顺序列出', '一键复制全部'],
   'scenarios': ['从网页源码/笔记收集链接', '日志里抽取请求 URL', '批量核对外链'],
   'steps': ['粘贴文本', '点击提取', '查看去重后的链接列表', '复制或全部导出'],
   'tips': ['仅匹配带协议的完整链接', '去重按字符串精确比对', '相对路径(无 http)不会被识别'],
   'faqs': [('为什么有的链接没被提取？', '缺少 http(s):// 的相对路径不会被匹配，需补全协议。'), ('能给个例子吗？', '粘贴"详见 https://a.com 与 https://a.com 重复"，提取得 1 条去重链接。')],
   'en_name': 'URL Extractor',
   'en_desc': 'URL Extractor Guide: batch-extract all links from a block of text, dedupe and copy.',
   'en_intro': 'Paste articles/logs/email containing links and extract every http/https link in one click, auto-deduplicated for batch checking or export. Local processing.',
   'en_features': ['Regex extract http/https links', 'Auto-dedupe', 'List in appearance order', 'Copy all at once'],
   'en_scenarios': ['Collect links from page source / notes', 'Pull request URLs from logs', 'Batch-check outbound links'],
   'en_steps': ['Paste the text', 'Click extract', 'See the deduplicated link list', 'Copy or export all'],
   'en_tips': ['Only full links with a protocol match', 'Dedupe is exact string compare', 'Relative paths (no http) are not recognized'],
   'en_faqs': [('Why is a link missing?', 'Relative paths without http(s):// are not matched; add the protocol.'), ('Can you show an example?', 'Paste "see https://a.com and https://a.com again" → 1 deduplicated link.')],
  },

 ],

 # ---- batch 05 ----
 [
  {
   'slug': 'text-compare',
   'ind': 'biz',
   'base': 'text-compare.html',
   'name': '文本并排对比',
   'desc': '文本并排对比使用指南：左右双栏展示两段文本，逐行对齐标出不同。',
   'intro': '与差异对比互补，双栏并排更利于人工逐行审阅长文档。支持滚动同步，纯本地。',
   'features': ['左右双栏并排', '逐行对齐高亮差异', '同步滚动', '本地不上传'],
   'scenarios': ['中英文逐句对照', '两版方案并排审阅', '翻译稿左右校订'],
   'steps': ['左框贴原文、右框贴对比文', '点击对比', '滚动查看逐行差异'],
   'tips': ['文档过长时先分段对比更清晰', '与文本差异对比互补使用', '本地处理敏感文本更安全'],
   'faqs': [('和"文本差异对比"区别？', '并排适合人工逐行读，差异对比适合看改动摘要。'), ('能给个例子吗？', '左栏中文稿、右栏译稿，逐行核对漏译句。')],
   'en_name': 'Side-by-Side Text Compare',
   'en_desc': 'Side-by-Side Text Compare Guide: show two texts in left/right columns, aligned line by line with differences marked.',
   'en_intro': 'Complements Text Diff: two columns side by side are better for manual, line-by-line review of long documents. Synced scrolling, fully local.',
   'en_features': ['Left/right two columns', 'Line-aligned diff highlight', 'Synced scrolling', 'Local, no upload'],
   'en_scenarios': ['Sentence-by-sentence CN/EN review', 'Compare two proposal versions', 'Proofread translations left/right'],
   'en_steps': ['Paste source left, compare text right', 'Click compare', 'Scroll to see line-by-line diffs'],
   'en_tips': ['For very long docs, compare in sections first', 'Use with Text Diff for summaries', 'Sensitive text is safer local'],
   'en_faqs': [('Difference from "Text Diff"?', 'Side-by-side suits manual line reading; Diff suits a change summary.'), ('Can you show an example?', 'Left column CN draft, right column translation; check line by line for missing sentences.')],
  },

  {
   'slug': 'summary-second-hand',
   'ind': 'realestate',
   'base': 'summary-second-hand.html',
   'name': '二手房税费（契税/个税/增值税）汇总',
   'desc': '二手房税费汇总使用指南：输入成交价与房屋信息，估算契税、个税与增值税。',
   'intro': '二手房交易涉及契税(按面积/套数)、个税(满五唯一免征)、增值税及附加(满二免征)。输入成交价、面积、持有年限与是否唯一，得到各项税费估算。仅供参考，以当地政策为准。',
   'features': ['估算契税/个税/增值税及附加', '满二/满五唯一免征判断', '按首套/二套与面积分级', '结果汇总'],
   'scenarios': ['买房前测算过户成本', '卖房算到手金额', '比对不同房源税费负担'],
   'steps': ['输入成交总价与面积', '选择是否首套、是否唯一住房、持有年限', '点击计算查看各项税费'],
   'tips': ['满两年免征增值税及附加、满五唯一免征个税', '首套 90㎡以下契税 1%', '本估算不含中介费与贷款费'],
   'faqs': [('"满五唯一"是什么意思？', '房产证满 5 年且家庭唯一住房，可免个税，能省一笔。'), ('能给个例子吗？', '首套 80㎡、成交 200 万、满五唯一，契税 1%=2 万，个税/增值税均免征。')],
   'en_name': 'Second-Hand Home Tax Summary',
   'en_desc': 'Second-Hand Home Tax Guide: enter price and property info to estimate deed tax, personal-income tax and VAT.',
   'en_intro': 'Second-hand deals involve deed tax (by area/units), personal-income tax (waived if "five years and only"), and VAT plus surcharge (waived if "two years"). Enter price, area, holding years and uniqueness for an estimate. For reference only; local policy governs.',
   'en_features': ['Estimate deed tax / personal-income tax / VAT & surcharge', '"Two-year"/"five-year-only" waiver check', 'By first/second home and area tier', 'Summarized result'],
   'en_scenarios': ['Estimate transfer cost before buying', 'Compute net proceeds when selling', 'Compare tax burden across listings'],
   'en_steps': ['Enter total price and area', 'Choose first/second home, only residence, holding years', 'Click to see each tax'],
   'en_tips': ['≥2 years waives VAT & surcharge; ≥5 years and only residence waives personal-income tax', 'First home ≤90㎡ deed tax 1%', 'Estimate excludes agent and loan fees'],
   'en_faqs': [('What is "five years and only"?', 'Title held ≥5 years and the family’s only residence waives personal-income tax — a real saving.'), ('Can you show an example?', 'First home 80㎡, price 2M, five-years-only: deed tax 1%=20k, personal-income & VAT waived.')],
  },

  {
   'slug': 'option-breakeven-call',
   'ind': 'securities',
   'base': 'option-breakeven-call.html',
   'name': '看涨期权盈亏平衡',
   'desc': '看涨期权盈亏平衡使用指南：输入行权价与权利金，计算到期盈亏平衡股价。',
   'intro': '买入看涨期权到期盈亏平衡 = 行权价 + 权利金。输入两项即得 BE 股价，并提示"股价高于 BE 才盈利"。仅供学习，非投资建议。',
   'features': ['计算看涨期权盈亏平衡股价', '显示盈亏平衡公式', '本地计算', '风险提示'],
   'scenarios': ['期权策略学习', '到期盈利阈值测算', '对比不同权利金的成本'],
   'steps': ['输入行权价', '输入每股权利金', '查看 BE 股价与盈利条件'],
   'tips': ['BE = 行权价 + 权利金', '股价必须超过 BE 才回本', '期权有归零风险，非投资建议'],
   'faqs': [('为什么还要加权利金？', '权利金是买入成本，只有股价涨过行权价+权利金才覆盖成本。'), ('能给个例子吗？', '行权价 100、权利金 5，则 BE = 105；到期股价>105 才盈利。')],
   'en_name': 'Call Option Break-Even',
   'en_desc': 'Call Option Break-Even Guide: add the premium to the strike to find the break-even price at expiry.',
   'en_intro': 'A long call breaks even when the underlying price equals strike plus premium paid. Enter strike and premium to see the break-even and payoff shape.',
   'en_features': ['Strike and premium input', 'Break-even price', 'Payoff hint', 'Local computation'],
   'en_scenarios': ['Option trading planning', 'Understand cost to profit', 'Teaching options'],
   'en_steps': ['Enter strike price', 'Enter premium paid', 'View break-even = strike + premium'],
   'en_tips': ['Must exceed strike+premium to profit', 'Options expire worthless if below', 'Know assignment risk'],
   'en_faqs': [('When does a call profit?', 'Underlying > strike + premium at expiry.'), ('Can you show an example?', 'Strike 100, premium 5 → BE 105.')],
  },

  {
   'slug': 'oil-change-countdown',
   'ind': 'automotive',
   'base': 'oil-change-countdown.html',
   'name': '机油更换倒计时',
   'desc': '机油更换倒计时使用指南：按里程或时间设置提醒，本地记录下次保养。',
   'intro': '机油寿命受里程与存放时间双重影响。设置保养周期(如 5000km/6 个月)，记录上次更换，工具本地倒计时提醒下次换油。数据仅存浏览器。',
   'features': ['按里程或时间设周期', '本地记录上次更换', '倒计时提醒下次保养', '数据存 localStorage'],
   'scenarios': ['私家车主保养提醒', '车队简易维保管理', '新手记住首保时间'],
   'steps': ['设置周期(里程/月)', '记录上次更换里程或日期', '查看倒计时', '到点提醒'],
   'tips': ['全合成机油周期更长(约 1 万 km/年)', '长期短途/拥堵应提前', '数据存本地，清缓存会丢失'],
   'faqs': [('按里程还是按时间？', '以先到者为准，长期不开也要按时间换(机油会氧化)。'), ('能给个例子吗？', '周期 5000km/6 月，已跑 3000km，则剩 2000km 或剩余月数先到者提醒。')],
   'en_name': 'Oil Change Countdown',
   'en_desc': 'Oil Change Countdown Guide: set a reminder by mileage or time; record the next service locally.',
   'en_intro': 'Oil life is governed by both mileage and storage time. Set a service interval (e.g. 5000km / 6 months), record the last change, and the tool counts down locally. Data stays in the browser.',
   'en_features': ['Interval by mileage or time', 'Record last change locally', 'Countdown to next service', 'Data in localStorage'],
   'en_scenarios': ['Car owner service reminder', 'Simple fleet maintenance', 'Remember first service for new drivers'],
   'en_steps': ['Set interval (km / months)', 'Record last change mileage or date', 'See the countdown', 'Alert when due'],
   'en_tips': ['Full-synthetic intervals are longer (~10k km / year)', 'Frequent short/ congested trips: change earlier', 'Data is local; clearing cache loses it'],
   'en_faqs': [('By mileage or by time?', 'Whichever comes first; even if rarely driven, change by time (oil oxidizes).'), ('Can you show an example?', 'Interval 5000km/6mo, already 3000km → 2000km or remaining months, whichever first.')],
  },

  {
   'slug': 'baker-percentage',
   'ind': 'baking',
   'base': 'baker-percentage.html',
   'name': '烘焙百分比换算',
   'desc': '烘焙百分比换算使用指南：以面粉为 100% 基准，换算各配料实际用量。',
   'intro': '烘焙配方用"烘焙百分比"：面粉=100%，其余配料按占面粉重量比表示。输入面粉重量与各配料百分比，得到实际克数；或反向由克数算百分比。本地计算。',
   'features': ['以面粉 100% 为基准', '输入百分比得实际克数', '反向由克数算百分比', '支持多配料'],
   'scenarios': ['缩放配方产量', '统一不同配方比例', '按手头面粉量配其他料'],
   'steps': ['输入面粉重量(基准 100%)', '输入水/糖/酵母等百分比', '查看各配料实际克数'],
   'tips': ['面粉永远是 100%', '液体总量常 60–75% 为宜', '百分比相加可判断配方干湿'],
   'faqs': [('为什么面粉是 100%？', '它是配方基准，其他配料都相对它表达，便于等比重算。'), ('能给个例子吗？', '面粉 500g、水 70%，则水=350g；酵母 2%→10g。')],
   'en_name': 'Baker’s Percentage Converter',
   'en_desc': 'Baker’s Percentage Converter Guide: use flour as the 100% baseline to convert each ingredient to its actual weight.',
   'en_intro': 'Baking recipes use "baker’s percentage": flour = 100%, everything else is a ratio to flour weight. Enter flour weight and each ingredient’s percentage for actual grams, or reverse from grams to percentage. Local computation.',
   'en_features': ['Flour = 100% baseline', 'Percentage → actual grams', 'Grams → percentage (reverse)', 'Multiple ingredients'],
   'en_scenarios': ['Scale recipe yield', 'Unify ratios across recipes', 'Size other ingredients to your flour'],
   'en_steps': ['Enter flour weight (baseline 100%)', 'Enter percentages for water/sugar/yeast etc.', 'See each ingredient’s actual grams'],
   'en_tips': ['Flour is always 100%', 'Total liquid often 60–75% is good', 'Sum of percentages hints at dough wetness'],
   'en_faqs': [('Why is flour 100%?', 'It is the baseline; other ingredients are expressed relative to it for easy rescaling.'), ('Can you show an example?', 'Flour 500g, water 70% → water=350g; yeast 2% → 10g.')],
  },

 ],

]
TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title{head_title_attr}>{title}使用指南 - ToolBox</title>
<meta name="description"{head_desc_attr} content="{desc}">
<meta property="og:title"{head_title_attr2} content="{title}使用指南 - ToolBox">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{canonical}">
<meta property="og:description"{head_desc_attr} content="{desc}">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 免费在线工具与使用指南">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title"{head_title_attr2} content="{title}使用指南 - ToolBox">
<meta name="twitter:description"{head_desc_attr} content="{desc}">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 免费在线工具与使用指南">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="zh-CN" href="{canonical}">
<link rel="alternate" hreflang="en-US" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"{title}使用指南","description":"{desc}","author":{"@type":"Organization","name":"ToolBox"},"inLanguage":"zh-CN"}
</script>
<script defer src="https://chenguangwu.github.io/js/i18n.js"></script>
<script defer src="https://chenguangwu.github.io/js/guide-en-pack.js"></script>
<script defer src="https://chenguangwu.github.io/js/guide-i18n.js"></script>
<style>
:root{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}
header{padding:18px 20px;border-bottom:1px solid var(--border);background:#fff;}
.breadcrumb a{color:var(--primary);text-decoration:none;margin-right:6px;}
.breadcrumb a:hover{text-decoration:underline;}
main{max-width:780px;margin:0 auto;padding:28px 20px 60px;}
h1{font-size:28px;margin:0 0 8px;}
.lead{font-size:16px;color:var(--muted);margin:0 0 22px;}
h2{font-size:20px;margin:28px 0 10px;color:var(--primary);}
ul,ol{padding-left:22px;}
li{margin:6px 0;}
dl{margin:0;}
dt{font-weight:700;margin-top:12px;}
dd{margin:4px 0 0;color:var(--muted);}
.back{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}
.back a{color:var(--primary);font-weight:700;text-decoration:none;}
footer{text-align:center;color:var(--muted);font-size:13px;padding:24px;border-top:1px solid var(--border);}
</style>
</head>
<body>
<header><nav class="breadcrumb"><a href="{home}">ToolBox</a> / <a href="{home}#guides"{nav_attr}>{nav_fb}使用指南</a> / <span{title_attr}>{title}</span></nav></header>
<main>
<h1{title_attr}>{title} 使用指南</h1>
<p class="lead"{intro_attr}>{intro}</p>
<h2{sec_features}>核心功能</h2>
<ul>{features}</ul>
<h2{sec_scenarios}>适用场景</h2>
<ul>{scenarios}</ul>
<h2{sec_steps}>使用步骤</h2>
<ol>{steps}</ol>
<h2{sec_tips}>实用技巧</h2>
<ul>{tips}</ul>
<h2{sec_faqs}>常见问题</h2>
<dl>{faqs}</dl>
<div class="back"><a href="{tool_url}">→ 去使用 {title}（免费 · 纯前端 · 数据不上传）</a></div>
</main>
<footer>© 2026 ToolBox · 纯前端在线工具 · 数据不上传，安全可靠</footer>
</body>
</html>
'''

def li(items, slug, field, en_items=None):
    out = []
    for i, x in enumerate(items):
        if en_items and i < len(en_items) and en_items[i]:
            key = 'guide.%s.%s.%d' % (slug, field, i)
            out.append('<li data-i18n="%s" data-i18n-fb="%s">%s</li>'
                       % (key, html.escape(str(x)), html.escape(str(x))))
        else:
            out.append('<li>%s</li>' % html.escape(str(x)))
    return ''.join(out)

# 全站通用 section / 导航词（固定，不随 slug 变化）
GUIDE_EN_PACK = {
    'guide._section.features': 'Key Features',
    'guide._section.scenarios': 'Use Cases',
    'guide._section.steps': 'How to Use',
    'guide._section.tips': 'Pro Tips',
    'guide._section.faqs': 'FAQ',
    'guide._nav.guides': 'Guides',
}

def render_faqs(g):
    out = []
    en = g.get('en_faqs')
    for i, (q, a) in enumerate(g['faqs']):
        if en and i < len(en) and en[i]:
            qk = 'guide.%s.faqs.%d.q' % (g['slug'], i)
            ak = 'guide.%s.faqs.%d.a' % (g['slug'], i)
            out.append('<dt data-i18n="%s" data-i18n-fb="%s">%s</dt><dd data-i18n="%s" data-i18n-fb="%s">%s</dd>'
                       % (qk, html.escape(q), html.escape(q), ak, html.escape(a), html.escape(a)))
        else:
            out.append('<dt>%s</dt><dd>%s</dd>' % (html.escape(q), html.escape(a)))
    return ''.join(out)

def render(g):
    fn = '%s-guide.html' % g['slug']
    canonical = '%s/guides/%s' % (SITE, fn)
    has_en = 'en_name' in g
    if has_en:
        for fld in ('name', 'desc', 'intro', 'features', 'scenarios', 'steps', 'tips', 'faqs'):
            ek = 'en_' + fld
            if ek not in g:
                continue
            if fld in ('features', 'scenarios', 'steps', 'tips'):
                for i, v in enumerate(g[ek]):
                    GUIDE_EN_PACK['guide.%s.%s.%d' % (g['slug'], fld, i)] = v
            elif fld == 'faqs':
                for i, (q, a) in enumerate(g[ek]):
                    GUIDE_EN_PACK['guide.%s.faqs.%d.q' % (g['slug'], i)] = q
                    GUIDE_EN_PACK['guide.%s.faqs.%d.a' % (g['slug'], i)] = a
            elif fld == 'name':
                GUIDE_EN_PACK['guide.%s.title' % g['slug']] = g[ek]
                GUIDE_EN_PACK['guide.%s.back' % g['slug']] = 'Open %s (Free · client-side · no upload)' % g[ek]
            else:
                GUIDE_EN_PACK['guide.%s.%s' % (g['slug'], fld)] = g[ek]
        title_attr = ' data-i18n="guide.%s.title" data-i18n-fb="%s 使用指南"' % (g['slug'], html.escape(g['name']))
        intro_attr = ' data-i18n="guide.%s.intro" data-i18n-fb="%s"' % (g['slug'], html.escape(g['intro']))
        nav_attr = ' data-i18n="guide._nav.guides" data-i18n-fb="使用指南"'
        nav_fb = ''
        sec_features = ' data-i18n="guide._section.features" data-i18n-fb="核心功能"'
        sec_scenarios = ' data-i18n="guide._section.scenarios" data-i18n-fb="适用场景"'
        sec_steps = ' data-i18n="guide._section.steps" data-i18n-fb="使用步骤"'
        sec_tips = ' data-i18n="guide._section.tips" data-i18n-fb="实用技巧"'
        sec_faqs = ' data-i18n="guide._section.faqs" data-i18n-fb="常见问题"'
        head_title_attr = ' data-i18n-head="guide.%s.title" data-i18n-head-fb="%s使用指南 - ToolBox"' % (g['slug'], html.escape(g['name']))
        head_title_attr2 = ' data-i18n-head="guide.%s.title" data-i18n-head-fb="%s使用指南 - ToolBox" data-attr="content"' % (g['slug'], html.escape(g['name']))
        head_desc_attr = ' data-i18n-head="guide.%s.desc" data-i18n-head-fb="%s" data-attr="content"' % (g['slug'], html.escape(g['desc']))
    else:
        title_attr = intro_attr = nav_attr = nav_fb = ''
        sec_features = sec_scenarios = sec_steps = sec_tips = sec_faqs = ''
        head_title_attr = head_title_attr2 = head_desc_attr = ''
    page = (TPL
        .replace('{title}', html.escape(g['name']))
        .replace('{desc}', html.escape(g['desc']))
        .replace('{canonical}', canonical)
        .replace('{intro}', html.escape(g['intro']))
        .replace('{features}', li(g['features'], g['slug'], 'features', g.get('en_features')))
        .replace('{scenarios}', li(g['scenarios'], g['slug'], 'scenarios', g.get('en_scenarios')))
        .replace('{steps}', li(g['steps'], g['slug'], 'steps', g.get('en_steps')))
        .replace('{tips}', li(g['tips'], g['slug'], 'tips', g.get('en_tips')))
        .replace('{faqs}', render_faqs(g))
        .replace('{tool_url}', SITE + '/tools/%s/%s' % (g['ind'], g['base']))
        .replace('{home}', SITE + '/')
        .replace('{title_attr}', title_attr)
        .replace('{intro_attr}', intro_attr)
        .replace('{nav_attr}', nav_attr)
        .replace('{nav_fb}', nav_fb)
        .replace('{sec_features}', sec_features)
        .replace('{sec_scenarios}', sec_scenarios)
        .replace('{sec_steps}', sec_steps)
        .replace('{sec_tips}', sec_tips)
        .replace('{sec_faqs}', sec_faqs)
        .replace('{head_title_attr}', head_title_attr)
        .replace('{head_title_attr2}', head_title_attr2)
        .replace('{head_desc_attr}', head_desc_attr))
    return fn, page

def main():
    if len(sys.argv) >= 2:
        bi = int(sys.argv[1]) - 1
        assert 0 <= bi < len(BATCHES), 'batch 超出范围'
        batches = [BATCHES[bi]]
    else:
        batches = BATCHES
    os.makedirs(GUIDES_DIR, exist_ok=True)
    guide_map = []
    allg = [g for batch in batches for g in batch]
    for g in allg:
        fn, page = render(g)
        open(os.path.join(GUIDES_DIR, fn), 'w', encoding='utf-8').write(page)
        guide_map.append({'tool': g['base'], 'guide': '../../guides/%s' % fn, 'title': g['name'] + '使用指南'})
        print('OK: guides/%s' % fn)
    # 导出英文字典到 js/guide-en-pack.js（多批次脚本共享合并）
    export_js(GUIDE_EN_PACK)
    # 合并 guides.json（按 tool 去重）
    jf = os.path.join(ROOT, 'json', 'guides.json')
    old = json.load(open(jf, encoding='utf-8')) if os.path.exists(jf) else []
    existing = {m['tool'] for m in old}
    merged = old + [m for m in guide_map if m['tool'] not in existing]
    json.dump(merged, open(jf, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('guides.json 合并完成，共 %d 条（本批 +%d）' % (len(merged), len(guide_map)))
    # 指南中心 index.html 追加条目
    ip = os.path.join(GUIDES_DIR, 'index.html')
    if os.path.exists(ip):
        s = open(ip, encoding='utf-8').read()
        new_li = ''.join(
            '<li><a href="https://chenguangwu.github.io/guides/%s-guide.html">%s使用指南</a><span style="color:var(--muted);font-size:13px;"> — %s</span></li>'
            % (g['slug'], html.escape(g['name']), html.escape(g['desc'])) for g in allg)
        if '</ul>' in s:
            s = s.replace('</ul>', new_li + '</ul>', 1)
            open(ip, 'w', encoding='utf-8').write(s)
            print('guides/index.html 追加 %d 条' % len(allg))

def export_js(pack):
    # 合并到 js/guide-en-pack.js（多批次脚本共享同一字典，避免互相覆盖）
    path = os.path.join(ROOT, 'js', 'guide-en-pack.js')
    merged = {}
    if os.path.exists(path):
        try:
            txt = open(path, encoding='utf-8').read()
            m = txt.find('window.GUIDE_EN_PACK')
            if m >= 0:
                js_part = txt[txt.index('=', m) + 1:].strip()
                if js_part.endswith(';'):
                    js_part = js_part[:-1]
                existing = json.loads(js_part)
                if isinstance(existing, dict):
                    merged.update(existing)
        except Exception:
            pass
    merged.update(pack)
    header = "/* Auto-generated by scripts/gen_*_guides.py — merged EN dictionary for guide pages. Do not edit by hand. */\n"
    open(path, 'w', encoding='utf-8').write(header + 'window.GUIDE_EN_PACK = ' + json.dumps(merged, ensure_ascii=False, indent=2) + ';\n')
    print('js/guide-en-pack.js 字典导出 %d 条(本批 %d)' % (len(merged), len(pack)))

if __name__ == '__main__':
    main()
