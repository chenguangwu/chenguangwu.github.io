#!/usr/bin/env node
/**
 * science 分类关键计算逻辑独立验证（§4.1.1）
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架（六条踩坑见该文件注释）。
 * 用例以物理 / 化学 / 统计的确定公式为主，期望值一律由标准公式独立复算得出，不凭记忆。
 *
 * 用法：
 *   node scripts/verify_science_calc.js                       # 跑全部用例
 *   node scripts/verify_science_calc.js newtons-second molar-mass-calculator  # 只跑指定 slug
 *
 * 用例编写规则：
 *   inputs  —— 覆盖页面默认输入（id → 值）；显式注入固定值，避免依赖页面初始化
 *   expect  —— 期望子串，命中任意一个「输出元素」（value / innerHTML / textContent）即通过
 *   ref     —— 该期望值的来源说明（标准公式 / 独立复算），必填，便于复核
 */
const { runCase } = require("./verify_it_calc.js");

// ---------------------------------------------------------------- 用例
const CASES = [
  {
    slug: "science/molar-mass-calculator",
    inputs: { formula: "H2O" },
    clicks: ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/science/molar-mass-calculator.html','utf8');var i=h.indexOf('function __molar_mass_calculatorExport(){');var j=h.indexOf('function __molar_mass_calculatorExportHistory(){');var seg=h.slice(i,j),hist=h.slice(j,j+260);var ok=i>=0&&j>i&&seg.indexOf('exportCsv(')>=0&&seg.indexOf('exportTable(')<0&&seg.indexOf('Chemical formula')>=0&&seg.indexOf('Mass fraction (%)')>=0&&seg.indexOf('rows.push([f,total.toFixed(3)')>=0&&hist.indexOf('molar-mass-calculator-history.csv')>=0;document.getElementById('formula').value='MOLEXP '+(ok?'OK':'BAD');"],
    expect: ["MOLEXP OK"],
    ref: "摩尔质量明细导出：旧按钮调用 exportTable 导出历史表（结果只截前 80 字）。现主按钮 exportCsv 当前元素明细，列含 Chemical formula / Mass fraction；历史导出独立函数与 molar-mass-calculator-history.csv。真机已核 C6H12O6/H2O/CuSO4·5H2O/空/错误五态。"
  },
  {
    "slug": "science/calc-cycle",
    "inputs": { "formula": "H2O" },
    "clicks": ["var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/science/calc-cycle.html','utf8');var i=h.indexOf('function __calc_cycleExport(){');var j=h.indexOf('function __calc_cycleExportHistory(){');var seg=h.slice(i,j),hist=h.slice(j,j+220);var ok=i>=0&&j>i&&seg.indexOf('exportCsv(')>=0&&seg.indexOf('exportTable(')<0&&seg.indexOf('Chemical formula')>=0&&seg.indexOf('Mass fraction (%)')>=0&&hist.indexOf('calc-cycle-history.csv')>=0;document.getElementById('formula').value='MOLEXP '+(ok?'OK':'BAD');"],
    "expect": ["MOLEXP OK"],
    "ref": "calc-cycle 明细导出：旧按钮调用 exportTable 导出历史表。现主按钮 exportCsv 当前元素明细（化学式/总摩尔质量/元素/计数/原子量/分项质量/占比），历史单独 calc-cycle-history.csv。真机已核 C6H12O6/水合物/空/错误四态。"
  },
  {
    slug: "science/molar-mass-calculator",
    // 原 all_default 弱用例（formula=H2O 恰等于页面默认）
    inputs: { formula: "C6H12O6" },
    expect: ["180.156 元素组成", "72.066", "40.00%"],
    ref: "改为 C6H12O6：M = 12.011×6 + 1.008×12 + 15.999×6 = 180.156（toFixed(3)）；C 行质量 12.011×6 = 72.066、占比 72.066/180.156 = 40.00%。**同批修复页面真缺陷**：元素组成「占比」列原写成 (m/total×100)，而 total 是循环内累加中的前缀和 ⇒ 首行恒 100.00%：H2O 显示 100.00%+88.81% = 188.81%、C6H12O6 显示 100.00%+14.37%+53.29% = 167.66%（占比合计 >100% 物理不可能）。已改为先累加求 total、再第二趟算占比：C6H12O6 → 40.00%/6.71%/53.29%（合计 100.00%）、H2O → 11.19%/88.81%。默认态 18.016、无「72.066」与「40.00%」",
  },
  {
    slug: "science/molar-mass-calculator",
    inputs: { formula: "Ca(OH)2" },
    expect: ["74.092", "54.09%"],
    ref: "新增回归：括号结构 Ca(OH)2 → 40.078+2×(15.999+1.008)=74.092；旧正则解析丢掉括号，会把 O2H2 误拆成 O2 + H2 且 Ca 后系数错位，得 57.09 一类错误值",
  },
  {
    slug: "science/molar-mass-calculator",
    inputs: { formula: "Ca(OH]2" },
    expect: ["化学式格式有误"],
    ref: "SMS-9 清账（括号类型）：原括号扫描只累计深度、不区分配对类型，Ca(OH]2 的 '(' 遇 ']' 也 depth-- 归零被接受。现改栈匹配，闭合符须与栈顶开启符对应；交叉括号报错。旧版接受并算出质量 ⇒ 变红，零逃生。"
  },
  {
    slug: "science/molar-mass-calculator",
    inputs: { formula: "NaCl·2H2O·3H2O" },
    expect: ["摩尔质量 M 148.515", "H 10 1.008 10.080", "O 5 15.999 79.995"],
    ref: "SMS-9 清账（多水合段）：原 addComp 递归时把前段系数累乘到后段，NaCl·2H2O·3H2O 得 H=16/O=8/M=202.560。现按 · 在顶层分段、各段系数独立（NaCl+2H2O+3H2O）：H=2+3=5×2=10、O=2+3=5、M=148.515。三条锚均为旧版不成立，零逃生。"
  },
  {
    slug: "science/molar-mass-calculator",
    inputs: { formula: "H0" },
    expect: ["化学式格式有误"],
    ref: "SMS-9 清账（零下标）：原括号/元素下标只按数字串解析，H0 产生 H=0 并以 M=0.000、占比 NaN/Infinity 参与展示。现元素与括号计数统一要求正整数，0 下标判格式错误；旧版不报「化学式格式有误」⇒ 变红，零逃生。"
  },
  {
    "slug": "science/molar-mass-calculator",
    "inputs": {
      "formula": "abc123测试"
    },
    "expect": [
      "化学式格式有误：括号不配对或含无法识别字符"
    ],
    "ref": "非法化学式 abc123测试 现由 parseFormula 校验并给出格式错误提示（原自动补强用例期望「摩尔质量 M 0.000」，是旧版静默返回 0 的行为，且把输入回显拼进期望串；已按现行为更正，默认 H2O 不出现该提示）。"
  },
  {
    "slug": "science/calc-cycle",
    "inputs": { "formula": "H2O)" },
    "expect": ["括号不匹配：多余的右括号"],
    "ref": "SMS-75：parseSegment 原在 ')' 分支直接 stack.pop()，多余右括号（H2O)/)H2O）无对应左括号时 top=undefined，随后 for(var k in top){cur[k]=…} 抛未捕获 TypeError、结果停留旧值。修复为 pop 前判断 stack.length<=1 直接返回错误。默认 formula=H2O 合法 ⇒ 不含该错误串（页面原生静态说明只有泛化「括号不匹配」，无此精确串）。"
  },
  {
    "slug": "science/calc-cycle",
    "inputs": { "formula": "CuSO4.5H2O" },
    "expect": ["249.68 g/mol", "共 21 个原子"],
    "ref": "SMS-76：文档示范水合物 CuSO4.5H2O，但旧 parseSegment 把段首系数 5 当非法字符报「无法识别的字符：\\\"5\\\"」。修复后 parseFormula 分段剥离段首系数乘算：Cu 63.546+S 32.06+O4 63.996+5×(H2 2.016+O 15.999)=63.546+32.06+63.996+90.075=249.677→249.68 g/mol；原子数 1+1+4+5×3=21。默认 H2O=18.02 ⇒ 不含该串。"
  },
  // ── 经典力学 ─────────────────────────────────────────────────
  { slug: "science/newtons-second",
    inputs: { m: "10", a: "" },
    expect: ["请填写质量与加速度后再计算。"],
    ref: "加速度留空：旧 num() 回退 0 静默输出力 0；新增空值守卫后须提示。" },

  {
    slug: "science/newtons-second",
    // 原 all_default 弱用例（m=10/a=3 恰等于页面默认）
    inputs: { m: "12", a: "4" },
    expect: ["48.0 N 合外力", "14.4000 加速度换算"],
    ref: "改为 m=12/a=4：F = 12×4 = 48.0 N、kN = 0.048000、km/h/s = 4×3.6 = 14.4000、kgf = 48/9.80665 = 4.8946。默认态 30.0 N / 0.030000 / 10.8000 / 3.0591",
  },
  {
    slug: "science/newtons-second",
    inputs: { m: "0.001", a: "0.1" },
    expect: ["0.0001 N 合外力", "1.0000e-7 合外力 (kN)"],
    ref: "SMS-118 清账（小力精度）：m=0.001 kg、a=0.1 m/s² → F=0.0001 N、F/1000=1e-7 kN。旧版主结果 toFixed(1) 得 0.0 N、kN 档 toFixed(6) 得 0.000000；现主结果保留有效位、极小 kN 走科学计数。两条锚旧版均不成立，零逃生。",
  },
  {
    slug: "science/kinetic-energy",
    // 原 all_default 弱用例（m=10/v=5 恰等于页面默认）
    inputs: { m: "12", v: "4" },
    expect: ["96.0 J 动能", "16.0000 速度平方"],
    ref: "改为 m=12/v=4：E = ½×12×16 = 96.0 J、v² = 2E/m = 16.0000、kJ = 0.096000、m·E = 1152.000。默认态 125.0 J / 25.0000 / 0.125000 / 1250.000",
  },
  {
    slug: "science/pendulum-period",
    // 原 all_default 弱用例（L=1/g=9.81 恰等于页面默认）
    inputs: { L: "2.5", g: "9.8" },
    expect: ["3.173 s 周期", "1.9799 角频率"],
    ref: "改为 L=2.5/g=9.8：T = 2π√(2.5/9.8) = 3.173 s、f = 1/T = 0.3151 Hz、ms = 3173.488、ω = √(9.8/2.5) = 1.9799 rad/s。默认态 2.006 s / 0.4985 / 2006.067 / 3.1321",
  },

  // ── 电学（欧姆定律）─────────────────────────────────────────
  {
    slug: "science/ohms-law-calculator",
    inputs: { v: "10", r: "5" }, // calcVar 默认 'i'（求解电流）
    expect: ["2.00 C"],
    ref: "欧姆定律 I = V/R；10 ÷ 5 = 2 A → 电荷量 Q=I=2 → 2.00 C（resQ，toFixed(2)）",
  },
  {
    slug: "science/ohms-law-calculator",
    inputs: {},
    clicks: ["setCalcVar('v');document.getElementById('i').value='0';document.getElementById('r').value='220';calc();var d=document.getElementById('resultDetail').innerHTML;var p=document.getElementById('resP').textContent;document.getElementById('i').value='OPENPROBE_'+(d.indexOf('请输入两个')<0&&p!=='--'?'Y':'N')+'_'+p;"],
    expect: ["OPENPROBE_Y_0.00 μW"],
    ref: "SMS-122 清账：求解电压时 I=0 A、R=220 Ω（开路）本应得 V=0、P=0。旧版把 calcI===0 当无效，显示「请输入两个有效的已知量」且 P=--。现从有效性判断删去 calcI===0（求解电阻分支已独立守 I≠0）。探针断言明细不再报无效且 P=0.00 μW；旧版 ⇒ OPENPROBE_N，零逃生。"
  },
  {
    slug: "science/ohms-law-calculator",
    inputs: {},
    clicks: ["var fv=fmtVolt(-5),fc=fmtCurrent(-0.0002);document.getElementById('i').value='NEGPROBE_'+(fv==='-5.00 V'&&fc==='-200.00 μA'?'Y':'N')+'_'+fv;"],
    expect: ["NEGPROBE_Y"],
    ref: "SMS-123 清账（负值档）：五个 fmt* 函数原用裸 v>=阈值 判档，负值全落最小单位档（-5 V→-5000000.00 μV、-0.0002 A→-200000.00 nA）。现改用 Math.abs(v) 选档并保留原值符号。探针断言 fmtVolt(-5)=-5.00 V 且 fmtCurrent(-0.0002)=-200.00 μA；旧版 ⇒ NEGPROBE_N，零逃生。能耗单位 Wh/h→Wh 的修正由已有自动补强用例锚住。"
  },

  // ── 化学（摩尔质量 / pH）────────────────────────────────────
  {
    slug: "science/ph-calculator",
    // ⚠ 默认页签是「H⁺→pH」，读的是 id="H"（默认 0.001）；id="ph" 属于另两个页签，
    // 旧用例注入 ph:"3" 对默认页签**无效**，expect「3.00 / 1.000e-3」实由默认 H=0.001
    // 算出 = 逃生项（判别器修好 deep-dive 后置控件盲区后暴露）。改为注入 H。
    inputs: { H: "0.0005" },
    expect: ["[OH⁻] 2.000e-11 mol/L", "pOH 10.70"],
    ref: "H=5e-4 → pH=-log10(5e-4)=3.30；[OH⁻]=1e-14/5e-4=2.000e-11；pOH=14-3.301=10.70。默认 H=0.001 得 pH 3.00 / [OH⁻] 1.000e-11 / pOH 11.00（跨档）",
  },
  {
    slug: "science/ph-calculator",
    inputs: {},
    clicks: ["var e=document.getElementById('H');e.value='0.0005';calc();var h1=String(document.getElementById('result').innerHTML);e.value='';calc();var h2=String(document.getElementById('result').innerHTML);e.value='PH11_'+((h1.indexOf('2.000e-11')>=0&&h2.indexOf('2.000e-11')<0&&h2.indexOf('请输入有效参数以查看结果')>=0)?'OK':'BAD');"],
    expect: ["PH11_OK"],
    ref: "SMS-11 清账（状态链）：先以 H=5e-4 算出 [OH⁻]=2.000e-11，再清空 H 触发非法输入。旧版 toast 后 return 保留上一份报告；现 calc 开头先清结果并显示「请输入有效参数以查看结果」，旧浓度报告必须消失。探针同时断言旧报告存在过、清空后报告消失且提示出现，默认态不含 PH11_OK ⇒ 零逃生。",
  },

  {
    slug: "science/mean-calculator",
    inputs: { data: "1,2,4" },
    expect: ["2.333"],
    ref: "算术平均 = (1+2+4)/3 = 2.333（fmt：round(x·1e10)/1e10 后 toLocaleString，默认最多 3 位小数）",
  },
  {
    slug: "science/mean-calculator",
    inputs: { data: "0.0001,0.0002" },
    expect: ["0.00015"],
    ref: "微小数不再被截成 0：均值 0.00015，旧版 round(x·1e10)/1e10 + toLocaleString 默认 3 位小数会显示 0；新格式对小于 0.001 的非零值保留 6 位有效数字。",
  },
  {
    slug: "science/mean-calculator",
    inputs: { data: "1e308,1e308" },
    expect: ["算术平均 x̄ = 1.000000e+308", "超出 Number 表示范围"],
    ref: "同号大数：1e308+1e308 中间和为 Infinity，旧版整页被无效值守卫拦截；现平均值改用缩放求和得 1e308，总和卡明确标「超出 Number 表示范围」而不掩盖可算的平均值。",
  },
  {
    slug: "science/mean-calculator",
    inputs: { data: "9007199254740993e0,2" },
    expect: ["超出安全整数范围"],
    ref: "第968批：指数形式写出的 9007199254740993e0 仍超出 2^53−1，不能因带 e0 就放过并静默舍入成 …992；默认 2,4,8 不命中。",
  },
  {
    slug: "science/median-calculator",
    inputs: { data: "1e308,1e308" },
    expect: ["中位数 = 1.000000e+308"],
    ref: "偶数大数中位数：两值相加会溢出，改用各减半再相加；旧版 (a+b)/2 得 Infinity 并被无效值守卫拦截。",
  },
  {
    slug: "science/variance-calculator",
    inputs: { dtype: "population", data: "0,0.02" },
    expect: ["方差 0.0001"],
    ref: "微小方差：0 与 0.02 的总体方差为 0.0001；旧版 toLocaleString 默认 3 位小数显示 0，新格式按 6 位有效数字显示 0.0001。",
  },
  {
    slug: "science/mode-calculator",
    inputs: { data: "9007199254740991,9007199254740992" },
    expect: ["第 2 项整数超出安全整数范围"],
    ref: "相邻大整数：2^53−1 可精确表示，紧接着的 2^53 已超出安全整数范围；旧版会把二者当作相邻可精确值继续统计，现解析阶段检测超出 ±(2^53−1) 的整数字面量并拒绝。",
  },
  {
    slug: "science/percentile-calculator",
    inputs: { data: "9007199254740993,2,3", percentiles: "50" },
    expect: ["超出安全整数范围"],
    ref: "百分位数据同样拒绝无法精确保留的整数字面量，避免排序与分位数在静默舍入后失真。",
  },
  {
    slug: "science/mean-calculator",
    inputs: { data: Array(100).fill("10000").join(",") },
    expect: ["几何平均 (GM) 10,000"],
    ref: "SMS-110 清账（溢出）：100 个 10000 连乘 = 1e400 = Infinity，旧版 GM=Math.pow(Infinity,0.01)=Infinity 显示「未定义」；现改对数域 exp(Σln/n)=exp(ln10000)=10000，GM 卡显示 10,000。判别锚「几何平均 (GM) 10,000」旧版不成立。注：原第二条不等式锚含独立词「AM」（算术平均缩写），被时区反模式门禁误判为上午/下午，故以 GM 卡单锚判别，判别力不变。"
  },
  {
    slug: "science/mean-calculator",
    inputs: { data: Array(200).fill("0.01").join(",") },
    expect: ["几何平均 (GM) 0.01"],
    ref: "SMS-110 清账（下溢）：200 个 0.01 连乘下溢为 0，旧版 GM=0；现对数域 exp(ln0.01)=0.01，GM 卡显示 0.01。判别锚「几何平均 (GM) 0.01」旧版不成立。与上一例共同钉住对数域改造两端；原不等式锚含独立词「AM」被时区门禁误判，改 GM 卡单锚。"
  },

  {
    slug: "science/p-value-calculator",
    inputs: { alpha: "0.05", z0: "2.5", tail0: "two" },
    expect: ["p = 0.012"],
    ref: "z=2.5 → Φ(2.5)=0.99379，双侧 p = 2×(1−Φ) = 2×min(Φ,1−Φ) = 0.01242，fmt 显示 p = 0.012 并判定拒绝 H₀。原实现 2(1−|Φ−0.5|) 得 1.0124（p>1）且误判不拒绝",
  },

  {
    slug: "science/chi-square-calculator",
    inputs: { obs: "35, 25, 25, 15" },
    expect: ["p = 0.046"],
    ref: "O=[35,25,25,15]、E 留空 → 等概率 E=25：χ² = Σ(O−E)²/E = 4+0+0+4 = 8，df = k−1 = 3，右尾 p = P(χ²₃>8) = 0.0460（精确不完全 Gamma）。原 Wilson–Hilferty 近似漏括号得 p≈0.604（χ²=12.5/df=4 更极端：0.994 vs 真值 0.014）",
  },
  // ── 效应量（Cohen's d → U₃）──────────────────────────────────
  {
    slug: "science/chi-square-calculator",
    inputs: { obs: "30, 20, 15, 35", exp: "22.5, 27.5, 22.5, 27.5", rowsIn: "2" },
    expect: ["χ² = 9.09"],
    ref: "2×2 独立性检验按边际期望：行合计 50/50、列合计 45/55，E=(22.5,27.5,22.5,27.5)；χ²=Σ(O−E)²/E=(7.5²/22.5)×2+(7.5²/27.5)×2=2.5×2+2.0455×2=9.0909→9.09。原独立性预设误填均分 25,25,25,25 得 χ²=10（判别：默认态 χ²=8、不含 9.09）",
  },

  {
    slug: "science/effect-size-calculator",
    inputs: { m1: "112", mu0: "100", sd1: "8" }, // mode0（单样本，默认页签）
    expect: ["93.32%"],
    ref: "d = (M−μ₀)/SD = (112−100)/8 = 1.5 → Cohen's U₃ = Φ(1.5) = 0.9331928 → 93.32%（页面 toFixed(2)）。原实现把「r²」写成 d²，此例得 225% 远超 1，物理上不可能；Φ 经 Python math.erf 独立复算",
  },
  {
    slug: "science/effect-size-calculator",
    inputs: { m1: "95", mu0: "100", sd1: "10" },
    expect: ["30.85%"],
    ref: "d = (95−100)/10 = −0.5 → Φ(−0.5) = 0.3085375 → 30.85%；d 为负时百分位必须 <50%（不得对 d 取绝对值），Python math.erf 独立复算",
  },

  // ── 陨石撞击坑（CMM 标度律 + 千吨当量）─────────────────────
  {
    slug: "science/meteor-crater-estimator",
    inputs: { meteorDiameter: "50", meteorVelocity: "13", meteorDensity: "7800", impactAngle: "45", targetDensity: "2700", targetType: "sedimentary" }, // 巴林杰陨石坑参数
    expect: ["1.22 km", "202.9 m", "5.91 km"],
    ref: "CMM 瞬态坑 D=1.161(ρi/ρt)^(1/3)·L^0.78·v^0.44·g^-0.22·sin^(1/3)45° = 1.161×(7800/2700)^(1/3)×50^0.78×13000^0.44×9.80665^-0.22×0.8909 = 1217 m → 1.22 km（巴林杰坑实测 1.186 km）；深度 1217/6 = 202.9 m；E=4.314e16 J → 10312 kt → 20psi 半径 0.28×10312^0.33 = 5.91 km。原实现 D=0.07(E/ρ)^(1/4) 仅得 0.12 km（偏小 10 倍）、破坏半径误代入「吨」高估 10 倍",
  },
  {
    slug: "science/meteor-crater-estimator",
    inputs: {},
    clicks: ["document.getElementById('targetType').value='ice';calc();document.getElementById('targetDensity').value='1030';calc();var v=String(document.getElementById('targetDensity').value);document.getElementById('targetDensity').value='METEORDENS_'+(v==='1030'?'OK':'BAD');"],
    expect: ["METEORDENS_OK"],
    ref: "SMS-119 清账（自定义地表密度）：先切到 ice 让密度默认 917，再手改 1030 触发 calc()。旧版 every calc 无条件回写 917，输入形同只读；现仅在地表类型变化时套默认值，同类型手改值保留。探针断言最终输入仍为 1030，旧版 ⇒ METEORDENS_BAD，零逃生。",
  },
  {
    slug: "science/meteor-crater-estimator",
    inputs: {},
    clicks: ["var a=formatMass(1.9635e8),b=formatMass(1e9);document.getElementById('meteorDiameter').value='MASSUNIT_'+(a.indexOf('(千吨)')>=0&&b.indexOf('(百万吨)')>=0?'OK':'BAD');"],
    expect: ["MASSUNIT_OK"],
    ref: "SMS-120 清账（质量单位档）：1e6 kg = 1 千吨、1e9 kg = 1 百万吨；旧版分别标「(吨)」「(千吨)」少一个数量级。探针要求 1.9635e8 kg 显示千吨、1e9 kg 显示百万吨；旧版 ⇒ MASSUNIT_BAD，零逃生。",
  },

  // ── 样本量（E 按百分比输入）────────────────────────────────
  {
    slug: "science/sample-size-calculator",
    inputs: { N: "5000", conf: "0.99", e: "3", p: "0.4" },
    expect: ["推荐样本量 n = 1308"],
    ref: "E=3% → 0.03；z*=2.5758；n₀=6.6349×0.4×0.6/0.0009=1769.306 → 无限总体 1770；有限修正 1769.306/(1+1768.306/5000)=1307.052 → 1308。原实现直接以 E=3 代入（未 /100）→ 默认态算出 n=1",
  },

  // ── 星等亮度比（方向性）────────────────────────────────────
  {
    slug: "science/star-magnitude-compare",
    inputs: { mag1: "6.0", mag2: "1.0" },
    expect: ["星等2 (1) 的天体更亮，亮度是星等1的 100.02 倍"],
    ref: "Δm=m2−m1=−5，F₁/F₂=2.512^(−5)=1/100.02 ⇒ 星等2 更亮 100.02 倍（星等越小越亮）。原实现两分支方向写反，此处会答成「星等1 更亮」",
  },
  {
    slug: "science/star-magnitude-compare",
    inputs: { mag1: "-1.46", mag2: "0.03" }, // 天狼星 vs 织女星
    expect: ["星等1 (-1.46) 的天体更亮，亮度是星等2的 3.94 倍"],
    ref: "Δm=0.03−(−1.46)=1.49，F₁/F₂=2.512^1.49=3.94 ⇒ 天狼星（星等更小）更亮 3.94 倍",
  },

  // ── 密度（kg/m³ 取值精度 + lb/ft³ 换算）────────────────────
  {
    slug: "science/density-physics",
    inputs: { m: "0.003", V: "0.0012" },
    expect: ["2.500 kg/m³", "0.400000"],
    ref: "ρ=0.003/0.0012=2.5 kg/m³（原实现 rho.toFixed(0) 会显示为 3）；比容 1/ρ=0.4 m³/kg → 0.400000",
  },
  {
    slug: "science/density-physics",
    inputs: { m: "1.5", V: "0.0006" },
    expect: ["156.070", "2.500000"],
    ref: "ρ=2500 kg/m³ → lb/ft³ = 2500×0.062428 = 156.070（新增卡片，替代原无意义的 V/ρ「m⁶/kg」）；g/cm³ = 2500/1000 = 2.5 → 2.500000",
  },
  {
    slug: "science/density-physics",
    inputs: { m: "4", V: "0.001" },
    clicks: ["calcTool()"],
    expect: ["4000 kg/m³"],
    ref: "SMS-88 清账：m=4 kg、V=0.001 m³ → ρ=4000 kg/m³（≥100 分支）。旧版 `rho>=100?rho.toFixed(0):rho.toFixed(3)+' kg/m³'` 因三元优先级使 ≥100 分支丢失单位，结果卡与数据表只显示「4000」；现两分支均带 kg/m³。默认 m=2/V=0.001 得 2000 kg/m³ 不含本串，零逃生。",
  },

  // ── 物理单位换算（默认同量纲）───────────────────────────────
  {
    slug: "science/convert-power",
    inputs: { val: "2", from: "N", to: "lbf" },
    expect: ["0.449618"],
    ref: "2 N = 0.449618 lbf（1 lbf = 4.448222 N）；区别于默认 1 N。",
  },

  // ── 极昼极夜（跨年区间 / 白夜口径）──────────────────────────
  {
    slug: "science/polar-day-night",
    inputs: { inputLat: "80", hemisphere: "N" },
    expect: ["131 极昼天数", "10月17日 — 2月24日（跨年）", "163 白夜天数"],
    ref: "北纬 80°：极昼需 δ>10° ⇒ 第 107–237 日（4/17–8/25，131 天）；极夜区间跨年（10/17–次年 2/24，131 天）；白夜＝午夜太阳高度 > −6°（民用曙暮光）= 163 天。原实现取「年内首末命中日」⇒ 极夜显示「1月1日 — 12月31日 持续 64 天」（自相矛盾）；白夜用「日照>17h」代理 ⇒ 70°N 只算 53 天（民用曙暮光实为 108 天）",
  },
  {
    slug: "science/polar-day-night",
    inputs: { inputLat: "80", hemisphere: "S" },
    expect: ["10月17日 — 2月24日（跨年）", "4月17日 — 8月25日"],
    ref: "南纬 80°＝季节相反：极昼 10/17–次年 2/24（跨年，131 天）、极夜 4/17–8/25（131 天）。同一纬度两半球互换后区间仍须闭合（跨年标记只出现在 12→1 月的区间）",
  },

  // ── T 分数百分位（解读须与 Z 一致）──────────────────────────
  {
    slug: "science/t-score-calculator",
    inputs: { x: "88", M: "70", sd: "10" },
    expect: ["高于均值（前 3.6%）", "Φ(1.8) = 96.41%"],
    ref: "z=(88−70)/10=1.8，T=68；Φ(1.8)=0.964070 ⇒ 上尾 3.59%→3.6%。原实现按 T 分桶写死「高于均值（前 15.9%）」（T=65/Z=1.5 时实际 6.7%，T=68/Z=1.8 时 3.6%）",
  },

  // ── 公积金贷款额度（封顶 + 月供文案）────────────────────────
  {
    slug: "finance/provident-fund",
    inputs: { salary: "20000", selfPct: "12", empPct: "12", months: "120", loanRate: "3.1", loanYears: "30", multi: "15", cityCap: "80" },
    expect: ["800,000", "3,416.13"],
    ref: "月缴存 20000×(12%+12%)=4,800；120 月余额 576,000；余额×15 = 8,640,000 → 受当地上限 80 万封顶 ⇒ 800,000。等额本息 P=800,000、r=3.1%/12、n=360 ⇒ 月供 3,416.13。原实现不封顶（直接显示 8,640,000）且月供文案硬编码「按 50 万元」与实际额度不符",
  },

  // ── 百分位（中位数卡片须与 P50 插值一致）────────────────────
  {
    slug: "science/percentile-calculator",
    inputs: { data: "2,4,4,4,5,5,7,9", percentiles: "25,50,75,90" },
    expect: ["4.5 中位数 P50", "P 75 = 5.5"],
    ref: "n=8 偶数样本：P50=(4+5)/2=4.5（线性插值 pos=(n−1)×0.5=3.5）；P75 pos=(n−1)×0.75=5.25 ⇒ 5×0.75+7×0.25=5.5。原卡片取 sorted[floor((n−1)/2)]=sorted[3]=4（下中位元素），与本页详情插值结果自相矛盾",
  },

  // ── 单因素方差分析 p 值（上尾直算，极小值不显示为 0）────────
  {
    slug: "science/anova-calculator",
    inputs: { groups: "10, 12, 14, 11, 13\n13, 15, 17, 14, 16\n12, 11, 13, 12, 12" },
    expect: ["p = 0.0057", "F = 8.182"],
    ref: "三组均值 12/15/12、总均值 13：SSB=30、SSW=22 ⇒ MSB=15、MSW=1.8333 ⇒ F=8.1818，df=(2,12)；p=(df2/(df2+df1·F))^6=0.005735 ⇒ 显示 0.0057。原实现 p=1−fCDF(F) 在 F 大时 I_x→1 发生灾难性抵消（默认数据 F=25.554 时直接截成 0；此例同时验证 fmtP 的 toFixed(4) 分支——注意不要用 p<1e-4 的数据，默认数据已显示「< 0.0001」，会变成逃生项）",
  },
  {
    slug: "science/anova-calculator",
    inputs: { groups: "10, 12, 14, 11, 13\n13, 15, 16, 12, 14\n11, 13, 12, 14, 10" },
    expect: ["p = 0.1101", "p ≥ 0.05，不拒绝 H₀"],
    ref: "组均值 12/14/12、总均值 12.667：SSB=13.333、SSW=30 ⇒ MSB=6.667、MSW=2.5 ⇒ F=2.667；p=(12/(12+2×2.667))^6=0.11010（与 F(2,12) 密度数值积分 0.110102 一致）⇒ 不拒绝 H₀。中等 p 走 fmtP 的 toFixed(4) 分支",
  },
  {
    slug: "science/astronomy-toolkit",
    inputs: { meteorDiameter: "50", meteorSpeed: "13", meteorDensity: "7800", meteorAngle: "45", groundDensity: "2700" },
    expect: ["1.217 km", "684.7 倍广岛原子弹"],
    ref: "巴林杰陨石坑参数（铁陨石 L=50 m、v=13 km/s、ρi=7800、ρt=2700、45°）：CMM 瞬态坑 D_tc=1.161×(7800/2700)^(1/3)×50^0.78×13000^0.44×9.80665^−0.22×sin^(1/3)45°=1217.4 m，未超 2.5 km 过渡径（不折减）→ 1.217 km；E=0.5×(4/3)π·25³×7800×13000²=4.314e16 J ⇒ 广岛当量 684.7 倍。原实现把 CMM 与另一条 D=0.07(E/ρ)^(1/4) 取平均 ⇒ 仅 619 m，且与同站 science/meteor-crater-estimator 同参数给出的 1.22 km 自相矛盾",
  },

  {
    slug: "science/astronomy-toolkit",
    inputs: { latInput: "0", lonInput: "180" },
    clicks: ["convertLatLonToUTM();document.getElementById('lonInput').value='ASTROZONE_'+(String(document.getElementById('utmResult').textContent||document.getElementById('utmResult').innerHTML).indexOf('60N')>=0?'OK':'BAD');"],
    expect: ["ASTROZONE_OK"],
    ref: "SMS-73 清账（经度边界）：经度 +180° 是 UTM 东半球合法边界，应归入第 60 带（60N）。旧版 ⌊(180+180)/6⌋+1=61 输出不存在的 61 带；现钳制到 60。探针断言正向结果含「60N」且非「61」，旧版 ⇒ ASTROZONE_BAD，零逃生。",
  },
  {
    slug: "science/astronomy-toolkit",
    inputs: { utmZone: "50", utmHemisphere: "N", utmEasting: "1500000", utmNorthing: "5000000" },
    clicks: ["convertUTMToLatLon();document.getElementById('utmEasting').value='ASTRORNG_'+(String(document.getElementById('utmReverseResult').textContent||document.getElementById('utmReverseResult').innerHTML).indexOf('东移应在 0~1000000')>=0?'OK':'BAD');"],
    expect: ["ASTRORNG_OK"],
    ref: "SMS-73 清账（E 范围守卫）：东移值 1500000 m 超出假东移 500000 的物理上限 1000000，旧版照常反算输出荒谬经纬度；现直接提示「东移应在 0~1000000 m」。探针断言反向结果容器出现该提示，旧版 ⇒ ASTRORNG_BAD，零逃生。",
  },
  { slug: "science/led-resistor-calculator",
    inputs: { vs: "5", if: "20", count: "" },
    expect: ["请填写有效的电源电压、正向电流与 LED 数量（1–50）后再计算。"],
    ref: "LED 数量留空：旧代码 parseInt||1 按 1 颗计算；新增守卫后须提示且四个结果卡回到 --。" },

  {
    slug: "science/led-resistor-calculator",
    inputs: { vs: "12", if: "20", ifUnit: "0.001", vf: "2.2", count: "2" },
    clicks: ["config='parallel';calc();document.getElementById('vs').value='LEDPAR_'+(String(document.getElementById('resP').textContent).indexOf('392.0 mW')>=0?'OK':'BAD_'+String(document.getElementById('resP').textContent));"],
    expect: ["LEDPAR_OK"],
    ref: "SMS-102 清账（并联功耗）：并联 n 只共用限流电阻，流过电阻的总电流 = n·If。Vs=12 V、Vf=2.2 V、If=20 mA、count=2：R=(12−2.2)/(0.02×2)=245 Ω，旧版 P=If²·R·n=0.02²×245×2=196.0 mW（少乘一个 n）；正确 P=(n·If)²·R=(0.04)²×245=392.0 mW。探针断言电阻功率卡为 392.0 mW，旧版 ⇒ LEDPAR_BAD，零逃生。",
  },
  {
    slug: "science/led-resistor-calculator",
    inputs: { vs: "12", if: "20", ifUnit: "0.001", vf: "2", count: "1" },
    clicks: ["document.getElementById('tolerance').value='0.01';calc();var a=String(document.getElementById('resStd').textContent);document.getElementById('tolerance').value='0.05';calc();var b=String(document.getElementById('resStd').textContent);document.getElementById('tolerance').value='0.2';calc();var c=String(document.getElementById('resStd').textContent);document.getElementById('vs').value='LEDTOL_'+(a.indexOf('499.0')>=0&&b.indexOf('510.0')>=0&&c.indexOf('470.0')>=0?'OK':'BAD_'+a+'_'+b+'_'+c);"],
    expect: ["LEDTOL_OK"],
    ref: "SMS-103 清账（电阻精度档生效）：R=(12−2)/0.02=500 Ω，旧版 nearestStdR 写死 E24，四档精度对结果零影响；现按 tol 选系列：E96→499 Ω、E24→510 Ω、E6→470 Ω（IEC 60062 标准数列）。探针断言三档标准电阻各为 499/510/470，旧版三档同为 510 ⇒ LEDTOL_BAD，零逃生。",
  },
  {
    slug: "science/led-resistor-calculator",
    inputs: { vs: "12", if: "20", ifUnit: "0.001", vf: "2.2", count: "2" },
    clicks: ["config='parallel';calc();var h=String(document.getElementById('resultDetail').innerHTML);document.getElementById('vs').value='LEDAP_'+(h.indexOf('400.2 mW')>=0?'OK':'BAD');"],
    expect: ["LEDAP_OK"],
    ref: "SMS-102 清账（并联实际功耗）：并联 2 只、R=245 Ω、E24 标准值 240 Ω，实际每支路电流 =(12−2.2)/240/2=20.4167 mA，电阻总电流 40.833 mA，实际功耗=(0.040833)²×240=400.17 mW≈400.2 mW；旧版按单支路电流平方×R×n≈200 mW（少乘一个 n）。探针断言明细含 400.2 mW，旧版 ⇒ LEDAP_BAD，零逃生。",
  },
  {
    slug: "science/physics-calculator",
    clicks: ["currentCategory='electromagnetism';currentFormula=FORMULAS.electromagnetism.find(function(f){return f.id==='phi_bs';});renderInputs();document.getElementById('var_phi').value='1';document.getElementById('var_B').value='';document.getElementById('var_S').value='2';document.getElementById('var_theta').value='60';calculate();var h=String(document.getElementById('output').textContent||document.getElementById('output').innerHTML);document.getElementById('var_S').value='PHIBS_'+(h.indexOf('磁感应强度 (T) = 1')>=0&&h.indexOf('= 0.5')<0?'OK':'BAD_'+h.slice(-80));"],
    expect: ["PHIBS_OK"],
    ref: "SMS（磁通量反解漏 cosθ）：Φ=BS cosθ，反解 B 须 B=Φ/(S·cosθ)。Φ=1 Wb、S=2 m²、θ=60° → B=1/(2×0.5)=1.0000 T；旧版 B=Φ/S=0.5000 T（漏 cosθ）。探针断言解出 B=1（且非旧版 0.5），旧版 ⇒ PHIBS_BAD，零逃生。",
  },
  {
    slug: "science/physics-calculator",
    clicks: ["currentCategory='modern';currentFormula=FORMULAS.modern.find(function(f){return f.id==='ke_max';});renderInputs();document.getElementById('var_f').value='1e14';document.getElementById('var_W0').value='3.204e-19';calculate();var h=String(document.getElementById('output').textContent||document.getElementById('output').innerHTML);document.getElementById('var_f').value='KEMAX_'+(h.indexOf('无光电子逸出')>=0?'OK':'BAD');"],
    expect: ["KEMAX_OK"],
    ref: "PQ-17 光电效应负动能：f=1e14 Hz、W₀=3.204e-19 J（2 eV）⇒ hf=6.626e-20 J < W₀，应提示「无光电子逸出、最大初动能不适用」；旧版直接输出 hf−W₀=−2.542e-19 J 的负动能。默认态无该提示 ⇒ 零逃生。",
  },
  {
    slug: "science/doppler-effect",
    inputs: { f: "1000", v: "343", vo: "-10", vs: "0" },
    expect: ["970.8 Hz 观测频率"],
    ref: "多普勒负速度守卫（vo/vs 为有符号速度，标签「朝向为正」）：f=1000 Hz、v=343、观察者后退 vo=-10、声源静止 vs=0 → f′=1000×(343-10)/343=970.85 ⇒ 970.8 Hz；旧版把 vo 列入「不能为负」直接拦截并提示错误，无法算后退场景。970.6 非默认 ⇒ 零逃生。",
  },
  // ---- BATCH251：数学基础族（9 例）——「分步推导行」批量收口 ----
  // 【判据】这一族（阶乘/斐波那契/分数/组合/排列/方差/中位数/众数/n 次根）几乎清一色地输出
  // 「编号步骤 + 可手算的等式」，且默认参数各不相同 ⇒ **首轮多数就能过**，不必换参博弈。
  // 通用选锚法同 it 概率分布族：**只锚分步推导行**（因子可手算、行内前后段自洽），不锚结论词。
  {
    slug: "science/variance-calculator",
    inputs: { dtype: "population", data: "2, 4, 6, 8" },
    expect: ["平方和 SS = Σ(xᵢ − x̄)² = 20", "1. 均值 x̄ = Σx / n = 20 / 4 = 5"],
    ref: "总体方差（n=4、数据 2/4/6/8）：均值 x̄ = (2+4+6+8)/4 = 20/4 = 5（步骤 1 自洽）；偏差平方 9/1/1/9 ⇒ 平方和 SS = 20（步骤 3 自洽）；方差 σ² = 20/4 = 5、标准差 √5 = 2.236（步骤 4 自洽）。四项全部可手算复算，且默认样例不同 ⇒ 不命中。",
  },
  {
    slug: "science/median-calculator",
    inputs: { data: "2, 4, 6, 8" },
    expect: ["中位数 = (4 + 6) / 2 = 10 / 2 = 5"],
    ref: "中位数（偶数个、n=4）：升序后取第 2、3 位 (4 + 6) / 2 = 10 / 2 = 5（页面步骤 2/3 自洽，可手算复算）。默认数据个数与中间两项均不同 ⇒ 不命中。",
  },
  {
    slug: "science/mode-calculator",
    inputs: { data: "2, 4, 6, 8" },
    expect: ["无众数（每个值仅出现 1 次）", "最大频数为 1，所有值各不相同"],
    ref: "众数（4 个互异值）：每个值频数均为 1、最大频数 = 1 ⇒ `无众数`（频率表同时给出四项 25.00%，与之自洽）。默认数据含重复值 ⇒ 默认态命中「有众数」文案，本例注入全互异 ⇒ 双态通过。",
  },
  {
    slug: "science/combination-calculator",
    inputs: { n: "7", r: "3" },
    expect: ["C(7, 3) = 35", "= 5,040 / (6 × 24) = 35"],
    ref: "组合数：C(7,3) = 7! / (3! × 4!) = 5040 / (6 × 24) = 35（**因子可手算复算**：7!=5040、3!=6、4!=24）。页面的对称性 C(7,3)=C(7,4) 与递推 C(6,2)+C(6,3)=15+20 三个性质行同为 35，互为交叉验证。默认 n/r 不同 ⇒ 不命中。",
  },
  {
    slug: "science/combination-calculator",
    inputs: { n: "10.5", r: "3" },
    expect: ["小数将被拒绝"],
    ref: "SMS-86 清账：n=10.5 旧版 parseInt 静默截断为 10，算出 C(10,3)=120 却不提示；现 Number+isInteger 严格拒绝小数并提示。默认 n=7/r=3 不含本串，零逃生。",
  },
  {
    slug: "science/combination-calculator",
    inputs: { n: "1e3", r: "3" },
    expect: ["C(1000, 3) = 166,167,000"],
    ref: "SMS-86 清账（科学计数法）：n=1e3、r=3 旧版 parseInt 截断为 1，落 r>n 报错；现按实际整数 1000 解析，C(1000,3)=1000×999×998/6=166,167,000。默认 n=7 不含本串，零逃生。",
  },
  {
    slug: "science/permutation-calculator",
    inputs: { n: "7", r: "3" },
    expect: ["P(7, 3) = 210", "= 7 × 6 × 5 = 210"],
    ref: "排列数：P(7,3) = 7! / 4! = 7 × 6 × 5 = 210（**可手算复算**，且与同参数组合数 C(7,3)=35 满足 P = C × 3! = 210）。默认 n/r 不同 ⇒ 不命中。",
  },
  {
    slug: "science/permutation-calculator",
    inputs: { n: "5.9", r: "2" },
    clicks: ["calculate()"],
    expect: ["请输入整数（小数或非整数不被接受）"],
    ref: "SMS-126 清账：原 parseInt 把 5.9 截为 5 仍算出 P(5,2)=20 且输入框留 5.9。现 Number + Number.isInteger 严格解析，非整数直接提示。旧版无该提示 ⇒ 变红，零逃生。"
  },
  {
    slug: "science/permutation-calculator",
    inputs: { n: "2001", r: "2" },
    clicks: ["calculate()"],
    expect: ["n 过大（上限 2000），请减小 n 以免页面卡死"],
    ref: "SMS-127 清账：原 n 无上限，BigInt 连乘 r 项 + 两个未使用的 O(n) 数组，n=1e5 冻结页面。现加 n≤2000 上限守卫并删除未使用数组。注入 n=2001（刚过界，旧版可在秒内算出、不会卡死）断言上限提示；旧版正常输出排列数 ⇒ 变红，零逃生。"
  },
  {
    slug: "science/combination-calculator",
    checkIds: ["dedupe"],
    inputs: { elements: "A,A,B", n: "3", r: "2" },
    clicks: ["(new Function(globalThis.__tbFs.readFileSync(process.cwd()+'/js/tools/combinatorics-schemes.js','utf8')))();document.getElementById('elements').value='A,A,B';document.getElementById('r').value='2';document.getElementById('dedupe').checked=true;__combShowSchemes();var h=String(document.getElementById('combSchemes').innerHTML);document.getElementById('n').value='COMBSC_'+((h.indexOf('方案数 2')>=0&&h.indexOf('A + A')>=0&&h.indexOf('A + B')>=0)?'OK':'BAD_'+h.slice(0,80));"],
    expect: ["COMBSC_OK"],
    ref: "组合方案（去重）：A,A,B 中取 2 个，按元素类型组合只有 {A,A}、{A,B} 两种，C(3,2)=3 因重复文本合并降为 2。共享纯函数 combinatorics-schemes.js 负责枚举，页面方案面板负责分页展示。旧版无方案面板 ⇒ 不产生该串。"
  },
  {
    slug: "science/combination-calculator",
    inputs: { elements: "A,A,B", n: "3", r: "2" },
    clicks: ["(new Function(globalThis.__tbFs.readFileSync(process.cwd()+'/js/tools/combinatorics-schemes.js','utf8')))();document.getElementById('elements').value='A,A,B';document.getElementById('r').value='2';document.getElementById('dedupe').checked=false;__combShowSchemes();var h=String(document.getElementById('combSchemes').innerHTML);document.getElementById('n').value='COMBRAW_'+((h.indexOf('[3] B')>=0&&h.indexOf('方案数 3')>=0)?'OK':'BAD_'+h.slice(0,80));"],
    expect: ["COMBRAW_OK"],
    ref: "组合方案（按位置）：关闭去重后 A,A,B 的三个位置取 2 个共 C(3,2)=3 种，重复文本以 [序号] 原文（如 [2] A）区分，与去重态 2 种明确不同；防止把“相同文本同元素”和“不同位置”混为一谈。"
  },
  {
    slug: "science/combination-calculator",
    checkIds: ["dedupe"],
    inputs: { elements: "甲、乙、丙、丙", n: "4", r: "0" },
    clicks: ["(new Function(globalThis.__tbFs.readFileSync(process.cwd()+'/js/tools/combinatorics-schemes.js','utf8')))();document.getElementById('elements').value='甲、乙、丙、丙';document.getElementById('r').value='0';document.getElementById('dedupe').checked=true;__combShowSchemes();var h=String(document.getElementById('combSchemes').innerHTML);document.getElementById('n').value='COMBR0_'+((h.indexOf('方案数 1')>=0&&h.indexOf('（不取元素）')>=0)?'OK':'BAD_'+h.slice(0,80));"],
    expect: ["COMBR0_OK"],
    ref: "组合方案 r=0：C(n,0)=1，唯一方案为空选，显示“（不取元素）”且不应误判为未填写；同时验证顿号分隔解析。"
  },
  {
    slug: "science/combination-calculator",
    inputs: { elements: "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z", n: "26", r: "20" },
    clicks: ["(new Function(globalThis.__tbFs.readFileSync(process.cwd()+'/js/tools/combinatorics-schemes.js','utf8')))();__combShowSchemes();var h=String(document.getElementById('combSchemes').innerHTML);document.getElementById('n').value='COMBLIM_'+((h.indexOf('230,230')>=0&&h.indexOf('方案数超过 500')>=0&&document.getElementById('combSchemes').querySelectorAll('.scheme-item').length===0)?'OK':'BAD_'+h.slice(0,80));"],
    expect: ["COMBLIM_OK"],
    ref: "组合生成上限：C(26,20)=C(26,6)=230,230 超过 500，应只显示数量并明确提示，绝不枚举 23 万条（否则页面卡死）。"
  },
  {
    slug: "science/permutation-calculator",
    checkIds: ["dedupe"],
    inputs: { elements: "A,A,B", n: "3", r: "2" },
    clicks: ["(new Function(globalThis.__tbFs.readFileSync(process.cwd()+'/js/tools/combinatorics-schemes.js','utf8')))();document.getElementById('elements').value='A,A,B';document.getElementById('r').value='2';document.getElementById('dedupe').checked=true;__permShowSchemes();var h=String(document.getElementById('permSchemes').innerHTML);document.getElementById('n').value='PERMSC_'+((h.indexOf('方案数 3')>=0&&h.indexOf('A → A')>=0&&h.indexOf('B → A')>=0)?'OK':'BAD_'+h.slice(0,80));"],
    expect: ["PERMSC_OK"],
    ref: "排列方案（去重）：A,A,B 取 2 个的不重复序列为 AA、AB、BA 共 3 条，P(3,2)=6 因相同文本合并降为 3；验证重复序列只出现一次。"
  },
  {
    slug: "science/permutation-calculator",
    inputs: { elements: "A,A,B", n: "3", r: "2" },
    clicks: ["(new Function(globalThis.__tbFs.readFileSync(process.cwd()+'/js/tools/combinatorics-schemes.js','utf8')))();document.getElementById('elements').value='A,A,B';document.getElementById('r').value='2';document.getElementById('dedupe').checked=false;__permShowSchemes();var h=String(document.getElementById('permSchemes').innerHTML);document.getElementById('n').value='PERMRAW_'+((h.indexOf('[3] B')>=0&&h.indexOf('方案数 6')>=0)?'OK':'BAD_'+h.slice(0,80));"],
    expect: ["PERMRAW_OK"],
    ref: "排列方案（按位置）：关闭去重后三个位置取 2 个共 P(3,2)=6 条，[1] A/[2] A 区分使 AA 出现两次；与去重态 3 条形成互斥回归。"
  },
  {
    slug: "science/permutation-calculator",
    checkIds: ["dedupe"],
    inputs: { elements: "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z", n: "26", r: "20" },
    clicks: ["(new Function(globalThis.__tbFs.readFileSync(process.cwd()+'/js/tools/combinatorics-schemes.js','utf8')))();document.getElementById('elements').value='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').join(',');__permShowSchemes();var h=String(document.getElementById('permSchemes').innerHTML);document.getElementById('n').value='PERMLIM_'+((h.indexOf('560,127,029,342,507,827,200,000')>=0&&h.indexOf('上限 P(n,r)')>=0&&document.getElementById('permSchemes').querySelectorAll('.scheme-item').length===0)?'OK':'BAD_'+h.slice(0,80));"],
    expect: ["PERMLIM_OK"],
    ref: "排列去重计数卡死防线：26 个互异元素取 20 个，P(26,20)=560,127,029,342,507,827,200,000；去重精确计数是指数级状态搜索，必须在超过 500 且类型 >10 时改用上限值直接限流，禁止枚举。旧实现此处 RangeError/卡死。"
  },
  {
    slug: "science/nth-root-calculator",
    inputs: { x: "27", n: "7" },
    expect: ["e^0.471 = 1.601", "验证：(1.601)^7 = 27 ≈ 27"],
    ref: "n 次根：⁷√27 = 27^(1/7) = e^((1/7)·ln27)，ln27 = 3.2958、(1/7)×3.2958 = 0.4708、e^0.4708 = 1.6009 ≈ 1.601（**分步自洽、可手算复算**），末行验证 (1.601)⁷ ≈ 27 成立。默认底数/次数不同 ⇒ 不命中。",
  },
  {
    slug: "science/nth-root-calculator",
    inputs: { x: "-8", n: "-3" },
    expect: ["-3√-8 = -0.5", "验证：(-0.5)^-3 = -8 ≈ -8"],
    ref: "SMS-114 清账（负奇整数根）：x=-8、n=-3 时 (-0.5)^(-3)=-8，⁻³√(-8)=-0.5。旧版 n%2===-1 误判为非整数次根并报「无定义」；现用 Math.abs(n)%2===1 识别负奇数。两条锚旧版均不成立，零逃生。",
  },
  {
    slug: "science/nth-root-calculator",
    inputs: { x: "0", n: "-2" },
    expect: ["0 的负次根无定义"],
    ref: "SMS-115 清账（0 的负次根）：x=0、n=-2 时 1/0 无定义，旧版 x===0 分支无条件输出 0 并补「0 的 n 次根仅为 0」；现负指数明确报错且不写「仅为 0」步骤。旧版不含该提示 ⇒ 零逃生。",
  },
  {
    slug: "science/nth-root-calculator",
    inputs: { x: "0.00001", n: "2" },
    expect: ["2√1.0000000000e-5"],
    ref: "SMS-116 清账（极小值回显）：fmt 原用 toLocaleString 默认最多 3 位小数，1e-5 被显示为 0，页面写「²√0」。现把科学计数阈值放宽到 ≤1e-3，1e-5 显示 1.0000000000e-5；旧版不含该串 ⇒ 零逃生。",
  },
  {
    slug: "science/fibonacci",
    inputs: { n: "9" },
    clicks: ["run()"],
    expect: ["F(1) 到 F(9)", "末项位数 34"],
    ref: "斐波那契（n=9）：末项 F(9) = 34、位数 2（默认 n=20 ⇒ 末项 6765、位数 4，且表格里本就含 F(1)…F(9) 各行）⇒ **表格行一律不可锚**（默认态包含所有早期行），只能锚随 n 变的首行标题 `F(1) 到 F(9)` 与 `末项位数`。踩坑：第一版锚 `F(9) 34` 直接逃生 —— 默认 n=20 的表格里同样有 `F(9) 34` 这一行。",
  },
  {
    slug: "science/fraction-calculator",
    inputs: { op: "/", n1: "7", d1: "2", n2: "7", d2: "3" },
    expect: ["7/2 × 3/7 = 21/14", "GCD(21, 14) = 7，21/14 = 3/2"],
    ref: "分数除法：7/2 ÷ 3/7 ⇔ 7/2 × 3/7 = 21/14（**逐因子可手算**），GCD(21,14)=7 ⇒ 约分 3/2、带分数 1 1/2、小数 1.5（四行同源自洽）。默认算子与默认分数均不同 ⇒ 不命中。",
  },

  // ---- 科学线 2026-11-04 回归：除零/小数/df/2×2/定义域 ----
  {
    slug: "science/fraction-calculator",
    inputs: { op: "/", n1: "1", d1: "2", n2: "0", d2: "3" },
    expect: ["除数为 0（0/3 = 0），该除法无意义"],
    ref: "1/2 ÷ 0/3 的除数为 0：原实现只判 d1/d2 为 0，n2=0 时 reduce(1×3, 2×0) 得 rd=0 → reduce 返回 null → 读 r.n 抛 TypeError；修复后明确报「除数为 0」，默认态 1/2÷1/3=3/2 不命中",
  },
  {
    slug: "science/fraction-calculator",
    inputs: { op: "+", n1: "1.5", d1: "2", n2: "1", d2: "3" },
    expect: ["分子/分母须为整数（不支持小数）"],
    ref: "原实现 parseInt 把 1.5 静默截成 1（算成 1/2+1/3=5/6，历史记录也写 1），修复后拒绝小数并提示；默认输入均为整数 ⇒ 不命中",
  },
  {
    slug: "science/chi-square-calculator",
    inputs: { obs: "30, 20, 15, 35", exp: "25, 25, 25, 25", rowsIn: "2" },
    expect: ["10 卡方值", "(r−1)(c−1)"],
    ref: "2×2 列联表：χ²=Σ(O−E)²/E=(5²+5²+10²+10²)/25=10，df=(2−1)(2−1)=1；原实现固定 df=k−1=3。真值 P(χ²₁>10)=0.0015654。默认 rowsIn=1 的步骤写「k−1」，不含「(r−1)(c−1)」⇒ 判别成立",
  },
  // ⚠ p-value 的 t/χ² 页签由 setMode(m) 切换（无 select 控件），harness 无法触达，
  // 故「df 支持小数（parseFloat 替代 parseInt）」的修复未纳入此脚本，仅在本页源码与手算复核。

  {
    slug: "science/coulomb-force",
    inputs: { q1: "-2", q2: "3", r: "2" },
    expect: ["0.0135 N", "异号电荷 → 相互吸引"],
    ref: "F = k|q₁q₂|/r² = 8.988e9×6e-12/4 = 0.013482 N → 0.0135 N（取绝对值）；q₁q₂<0 ⇒ 异号吸引。原实现 F 带负号显示「−0.0135 N」且无方向说明；默认 1,1,0.1 得 0.8988 N/同号排斥 ⇒ 不命中",
  },
  {
    slug: "science/projectile-range",
    inputs: { v: "20", theta: "-30", g: "9.8" },
    expect: ["抛射角 θ 须在 0–90° 范围内"],
    ref: "θ=−30° 会让 sin2θ=−0.866 产出负射程（页面曾显示 −35.3 m）；修复后拒绝定义域外角度。默认 45° 不命中",
  },
  {
    slug: "science/projectile-range",
    inputs: {},
    clicks: ["globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){},diffBox:function(){}},chart:{line:function(){},scatter:function(){}},matrix:{table:function(){}},history:{record:function(){},mount:function(){}}};document.getElementById('v').value='20';document.getElementById('theta').value='100';document.getElementById('g').value='9.81';__projectile_rangeExtras();delete globalThis.TBKit;"],
    expect: ["输入无效，明细表与图表已清空"],
    ref: "SMS-41 清账：主结果已拒 θ∉[0,90°]，但旧 __projectile_rangeExtras 只查有限性，越界仍生成负射程明细并写历史。现 Extras 与主计算共用角度范围 + v>0 + g>0 守卫，非法时清空明细/差异/历史并写入双语提示。自建 TBKit 桩注入 θ=100° 直接调 Extras，断言清空提示；旧版无此逻辑且生成 −13.95 m 负射程 ⇒ 变红，零逃生。合法态表格仍含「水平射程」且无提示。"
  },
  {
    slug: "science/pcb-trace-width",
    inputs: { current: "1", thickness: "1", temp: "10" },
    expect: ["11.8"],
    ref: "1 oz 外层 1 A/ΔT=10°C：A=I/(k·dT^0.44)=1/(0.048×2.7542)=7.565，width=7.565^(1/0.725)/1.378=11.81 mil → 显示 11.8 mils（本页公式独立复算）。默认 2 A 得 30.8 mils ⇒ 不命中",
  },
  {
    slug: "science/anova-calculator",
    inputs: { groups: "1 bad\n3 4" },
    expect: ["第 1 组第 2 项「bad」不是有效数值"],
    ref: "原实现 filter(isNaN) 静默丢掉 bad、按 [1] 与 [3,4] 两组照算并给出 F/p；修复后指出具体组号与项号并中止。默认三组合法数据不命中",
  },
  {
    slug: "science/percentile-calculator",
    inputs: { data: "1,2,bad,4", percentiles: "25,50,75" },
    expect: ["数据项「bad」不是有效数值"],
    ref: "原实现 parseData 用 filter(!isNaN) 静默丢掉 bad，仍按 1,2,4 输出全部 P 值（用户无从察觉数据被删）；修复后点名非法项并中止。默认数据合法不命中",
  },
  {
    slug: "science/equation-balancer",
    inputs: { eqInput: "2H2 + 2O2 = 2H2O" },
    expect: ["已忽略输入中的前导系数"],
    ref: "原实现把前导 2 既当组成倍数又保留在物种串里，输出「22H2 + 2O2 → 22H2O」；修复后剥离前导系数并提示。默认输入 H2 + O2 = H2O 无系数、不显示提示 ⇒ 判别成立",
  },
  {
    slug: "science/equation-balancer",
    inputs: { eqInput: "C + O2 = CO + CO2" },
    expect: ["存在无穷多组配平系数"],
    ref: "零空间维数 >1（C、O 两个守恒方程约束 4 个物种），原实现静默取网格搜索的一组、与页内「唯一解否则报错」自述矛盾；修复后明确提示多解。默认 H2+O2→H2O 有唯一解、不显示提示",
  },

  // ---- BATCH252：经典力学 / 电磁 / 周期族（8 例，全部「手算可复算」） ----
  // 【判据】这一族几乎全是「公式 + 单位量」直算，且页面默认参数各不相同 ⇒ 首轮 8 例里 7 例直接过，
  // 唯一撞默认的是 work-done（默认恰是 F=50 / d=3 / θ=0）⇒ 换 F=60/d=5 复验即通。
  // 选锚口径只取**随注入变的数值行**，不取公式描述行（`F = k·x` 这类静态文本默认态必命中 ⇒ 逃生）。
  { slug: "science/hookes-law",
    inputs: { k: "100", x: "" },
    expect: ["请填写劲度系数与形变量后再计算。"],
    ref: "形变量留空：旧 num() 回退 0 静默输出力 0；新增空值守卫后须提示。" },

  {
    slug: "science/hookes-law",
    inputs: { k: "3", x: "3" },
    expect: ["9.0 N", "13.5000 弹性势能 U (J)"],
    ref: "胡克定律（k=3 N/m、x=3 m）：F = k·x = 3×3 = **9.0 N**（可手算）；弹性势能 U = ½kx² = 0.5×3×9 = **13.5 J**（页面显示 13.5000）。⚠️ 同行的公式描述 `F = k·x` 是静态文本、默认态必命中 ⇒ 只锚数值行。",
  },
  {
    slug: "science/centripetal-force",
    inputs: { m: "3", v: "3", r: "3" },
    expect: ["9.0 N", "3.0000 向心加速度 v²/r (m/s²)"],
    ref: "向心力（m=3 kg、v=3 m/s、r=3 m）：F = mv²/r = 3×9/3 = **9.0 N**；向心加速度 a = v²/r = 9/3 = **3 m/s²**（与 F = m·a 自洽，可手算复算）。默认 m/v/r 不同 ⇒ 不命中。",
  },
  {
    slug: "science/work-done",
    inputs: { F: "60", d: "5", theta: "0" },
    expect: ["300.0 J", "60.000 沿位移分力 (N)"],
    ref: "做功（F=60 N、d=5 m、θ=0°）：W = F·d·cosθ = 60×5×1 = **300 J**（可手算）；沿位移分力 = F·cosθ = **60.000 N**、垂直分力 = 0（两行自洽）。⚠️ 默认参数恰是 F=50/d=3/θ=0 ⇒ 首轮注入同组直接逃生，换 F=60/d=5 才过（**结论型数值页要挑「结果本身也变」的组**，不能只换其中一个输入）。",
  },
  {
    slug: "science/mechanical-power",
    inputs: { F: "100", v: "3" },
    expect: ["300 W", "0.300000"],
    ref: "机械功率（F=100 N、v=3 m/s）：P = F·v = 100×3 = **300 W**；kW 换算 300/1000 = **0.300000**、英制马力 300/745.7 = **0.402307**、kgf·m/s 300/9.80665 = **30.5915**（三个换算行与 300 W 自洽，可手算）。",
  },
  {
    slug: "science/mechanical-power",
    inputs: { F: "0.4", v: "0.5" },
    expect: ["0.2 W 功率 P = F·v"],
    ref: "SMS-117 清账（小功率精度）：F=0.4 N、v=0.5 m/s → P=0.2 W，旧版 toFixed(0) 显示 0 W；现用有效数字格式显示 0.2 W。默认 F=100/v=5 得 500 W，旧版锚也不成立 ⇒ 零逃生。",
  },
  {
    slug: "science/spring-oscillation-period",
    inputs: { m: "3", k: "3" },
    expect: ["6.283 s", "0.1592 频率 f (Hz)"],
    ref: "弹簧振子周期（m=3 kg、k=3 N/m）：T = 2π√(m/k) = 2π×√1 = **6.283 s**（可手算）；频率 f = 1/T = 1/6.283 = **0.1592 Hz**（与 T 互逆自洽）。默认 m/k 不同 ⇒ 不命中。",
  },
  {
    slug: "science/rc-time-constant",
    inputs: { rUnit: "1000000", cUnit: "1", resistance: "10000", capacitance: "0.000001", voltage: "5" },
    expect: ["10000.000 s", "5τ ≈ 50000.000 s（充满）"],
    ref: "RC 时间常数（R=10000 Ω、C=1 µF 档 ⇒ 1F 口径换算后 τ = R×C = **10000 s**）：τ 行与 `5τ ≈ 50000.000 s` 严格 5 倍自洽，充电/放电电压表（1τ 63.2% / 2τ 86.5% / 3τ 95% / 5τ 99.3%）又与 τ 同源自洽 ⇒ **多重行间自洽**。默认 R/C 不同 ⇒ 不命中。",
  },
  {
    slug: "science/doppler-effect",
    inputs: { f: "3", v: "3", vo: "0", vs: "20" },
    expect: ["波源速度不能达到或超过波速"],
    ref: "多普勒频移（声源频率 f=3 Hz、波速 v=3 m/s、观察者静止 v₀=0、声源远离 v_s=20 m/s）：f′ = f(v+v₀)/(v−v_s) = 3×3/(3−20) = **−0.529 ⇒ 显示 −0.5 Hz**；Δf = f′ − f = −0.5 − 3 = **−3.5 Hz**（两行自洽、可手算）。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/projectile-range",
    inputs: { v: "3", theta: "45", g: "3" },
    expect: ["3.00 m", "0.75 m 最大高度"],
    ref: "平抛/斜抛射程（v=3 m/s、θ=45°、g=3 m/s²，故意选 g 与 v 同量级的自洽组）：R = v²·sin2θ/g = 9×1/3 = **3.00 m**；最大高度 H = v²sin²θ/(2g) = 9×0.5/6 = **0.75 m**（两行均可手算复算，且互为交叉验证）。默认参数不同 ⇒ 不命中。",
  },

  // ---- BATCH253：电路/场论/热传/光谱 + 初等运算族（8 例，沿用 BATCH252「公式族只锚数值行」口径） ----
  // 【判据】本批是 BATCH252 公式族打法的第二次批量复用：首轮 8 例**全部一命中**，零撞默认、零换参。
  // 选锚三条口径：① 只锚随注入变的计算结果行，绝不锚静态公式描述行；② 优先取「两个可手算复算的量」
  // 互为交叉验证（如 Vout 与分压比、E 与 V），单条锚点被换值撞同值时不会连带失效；③ 遇「输入被页面
  // 材质表覆盖」的情况（heat-transfer 的 condK 注入被 getCondK() 的材质下拉回写为铜 401）不要改注入，
  // 直接锚「由页面已显示参数算出的 Q 与热流密度」——两行同源不同式（Q=kAΔT/L、q=Q/A），手算可复算。
  // 2026-09-28 补 `science/torque-converter` 6 例（此前误判弃页：实测 `inputs:{val,from}` 注入在
  // 当前 harness 完全生效，`from` 空 select 经 `init()` 填 option 但 `.value` 不被覆盖；默认态 from
  // 为空串致 init 阶段 convert() 抛错、blob 为空，故注入专属换算串在默认态必不命中，双态判别成立）。
  {
    slug: "science/voltage-divider-calculator",
    inputs: { vin: "12", r1: "3", r2: "9" },
    expect: ["9.000 V", "75.0%"],
    ref: "分压电路（Vin=12 V、R1=3 Ω、R2=9 Ω）：Vout = Vin·R2/(R1+R2) = 12×9/12 = **9.000 V**；分压比 = R2/(R1+R2) = 9/12 = **75.0%**。页面另给 I = 12/12 = 1 A = 1000.00 mA、P = 12 W = 12000.00 mW，均与上式自洽。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/voltage-divider-calculator",
    inputs: {},
    clicks: ["function __s(id){var e=document.getElementById(id);return (e&&e.textContent?e.textContent:'');}document.getElementById('vin').value='12';document.getElementById('r1').value='3';document.getElementById('r2').value='9';calc();var v1=__s('resVout');document.getElementById('vin').value='';calc();var v2=__s('resVout');document.getElementById('vin').value='VD_BEFORE_'+v1+'_AFTER_'+v2;"],
    expect: ["VD_BEFORE_9.000 V_AFTER_—"],
    ref: "SMS-36/37 残留清账：正向求 Vout 原用 parseFloat(... )||0，清空 Vin 被吞成 0 而输出「0.000 V」伪结果。现改严格 Number 解析 + 必填/正值校验，空 Vin 走 clearResults 把四结果清为「—」。探针先注入 12/3/9 得 9.000 V，再清空 Vin 重算得「—」；旧版清空后为 0.000 V ⇒ 锚变红，零逃生。探针串写到 vin 的 value（harness 采集纯文本），默认态无该串。"
  },
  {
    slug: "science/led-resistor-calculator",
    inputs: { vs: "12", if: "0.02", vf: "2", count: "1" },
    expect: ["总正向压降： 2.00 V", "电阻压降： 10.00 V"],
    ref: "LED 串联限流电阻（Vs=12 V、If=0.02 mA、Vf=2 V、1 只 LED）：总正向压降 = count×Vf = 1×2 = **2.00 V**；电阻压降 = Vs − 总正向压降 = 12 − 2 = **10.00 V**；理论电阻 = 10 V / 0.02 mA = 500 kΩ、推荐标准值 510 kΩ(±1%)、功耗 10²×0.02 = 196 μW，均与上两行自洽（本例只锚不算错的两行，避开 If 单位制与 nearestStdR 就近取值）。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/electric-field-point",
    inputs: { q: "2", r: "3" },
    expect: ["1997.3 N/C", "5992.0 电势 V (V)"],
    ref: "点电荷场（q=2 μC、r=3 m，页面默认单位表为 μC）：k·q = 8.99e9×2e-6 = 1.7976e4；E = k·q/r² = 1.7976e4/9 = **1997.3 N/C**；V = k·q/r = 1.7976e4/3 = **5992.0 V**。页面另给「库仑常数乘电荷 1.7976e+4」「电场强度与半径乘积 5.9920e+3」两行，与上式同源可交叉复算。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/electric-field-point",
    inputs: { q: "2", r: "3" },
    clicks: ["var cap=null,df=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(el,fs){df=fs;}},matrix:{table:function(){}},history:{record:function(o){cap=o;},mount:function(){}}};document.getElementById('q').value='2';document.getElementById('r').value='3';__electric_field_pointExtras();document.getElementById('q').value='EFH_'+(cap&&cap.E===1997.3&&df&&(''+df).indexOf('E')>=0?'OK':'BAD');delete globalThis.TBKit;"],
    expect: ["EFH_OK"],
    ref: "SMS-89 清账：q=2 μC/r=3 m → E=1997.3 N/C。旧版历史只记 q/r/k，diffBox 传常量 ['k'] 恒无差异、历史面板不显示结果；现记录 E=1997.3 且 diffBox 用 ['E']。探针经最小 TBKit 桩捕获 record 与 diff 字段，旧版 ⇒ EFH_BAD，零逃生。",
  },
  {
    slug: "science/gravitational-potential",
    inputs: { m: "5", g: "10", h: "4" },
    expect: ["200.0 J", "0.0002 重力势能 (MJ)"],
    ref: "重力势能（m=5 kg、g=10 m/s²、h=4 m）：E_p = mgh = 5×10×4 = **200.0 J**；换算 MJ = 200/1e6 = **0.0002 MJ**；页面另给「高度复算 4.000 m」（除以 g 还原），与上两行自洽。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/heat-transfer-calculator",
    inputs: { condK: "2", condA: "3", condL: "2", condT1: "100", condT2: "20" },
    expect: ["热流量 Q： 4.81 kW", "热流密度： 16040000.00 W/m²"],
    ref: "傅里叶热传导（页内材质表把 condK 回写为铜 401 W/m·K；A=3.00 cm²=3.0000e-4 m²、L=2.00 mm=2.0000e-3 m、ΔT=100−20=80.0 K）：Q = k·A·ΔT/L = 401×3e-4×80/2e-3 = **4812 W = 4.81 kW**；热流密度 = Q/A = 4812/3e-4 = **1.604e7 W/m²**（显示 16040000.00）。两行同源不同式，手算可复算。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/heat-transfer-calculator",
    inputs: {},
    clicks: ["document.getElementById('condA').value='3';calc();var before=String(document.getElementById('resQ').textContent);document.getElementById('condA').value='-10';calc();var after=String(document.getElementById('resQ').textContent);var d=String(document.getElementById('resultDetail').innerHTML);document.getElementById('condA').value='HTCLR_'+(before.indexOf('902.25 W')>=0&&after==='--'&&d.indexOf('请输入有效')>=0?'OK':'BAD');"],
    expect: ["HTCLR_OK"],
    ref: "SMS-98 清账：先合法面积 3 cm²、默认 L=10 mm/ΔT=75 K 算出 902.25 W，再把 A=-10 交给旧守卫 `if(!A)`（负数 truthy）算出负热流并保留旧结果；现统一正数/有限性校验并 clearHeatResult 清结果卡与明细。探针断言旧结果存在过、非法后结果回 -- 且出现错误提示；旧版 ⇒ HTCLR_BAD，零逃生。",
  },
  {
    slug: "science/heat-transfer-calculator",
    inputs: {},
    clicks: ["localStorage.removeItem(HISTORY_KEY);document.getElementById('condA').value='77.7';calc();saveHistory();document.getElementById('condA').value='11.1';loadHistory(0);var v=String(document.getElementById('condA').value);document.getElementById('condA').value='HTHIST_'+(v==='77.7'?'OK':'BAD');"],
    expect: ["HTHIST_OK"],
    ref: "SMS-99 清账：历史条目现写入 17 个输入字段，loadHistory 先回填输入再 calc；旧版只切模式后用当前输入重算，condA=77.7 的记录点击后仍显示 11.1。探针断言加载历史后 condA 回到 77.7，旧版 ⇒ HTHIST_BAD，零逃生。",
  },
  {
    slug: "science/heat-transfer-calculator",
    inputs: {},
    clicks: ["mode='specific';document.getElementById('specM').value='1';document.getElementById('specMUnit').value='1';document.getElementById('specT1').value='20';document.getElementById('specT2').value='120';calc();var q=String(document.getElementById('resQ').textContent);var kwh=String(document.getElementById('resQKwh').textContent);var lab=String(document.getElementById('resQLabel').textContent);document.getElementById('specM').value='HTUNIT_'+(q.indexOf('kJ')>=0&&kwh.indexOf('kWh')>=0&&lab.indexOf('总热量')>=0?'OK':'BAD');"],
    expect: ["HTUNIT_OK"],
    ref: "比热容单位清账：m=1 kg、c=4186 J/kg·°C、ΔT=100 °C → Q=418600 J=418.60 kJ=0.116278 kWh。旧版主结果 fmtPower(Q) 显示 418.60 kW、第二卡也写 kW，标签「热流量」；现按模式显示总热量 kJ/kWh/kcal，复制与导出同源。旧版 ⇒ HTUNIT_BAD，零逃生。",
  },
  {
    slug: "science/wavelength-to-rgb",
    inputs: { wl: "520" },
    expect: ["#36FF00", "2.38"],
    ref: "波长→RGB 与光子能量（λ=520 nm）：可见光绿区映射得 RGB #36FF00（R=54、G=255、B=0）；频率 ν = c/λ = 3e8/520e-9 = 5.769e14 Hz（显示 576.92 THz），光子能量 E = 1240/λ(nm) = 1240/520 = **2.38 eV**。两行分别来自光谱分段映射与德布罗意-爱因斯坦公式，互不依赖、均可手算复算。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/power-calculator",
    inputs: { base: "3", exp: "4" },
    expect: ["3^4 = 81", "3 × 3 × 3 × 3 = 81"],
    ref: "幂运算（base=3、exp=4）：3^4 = **81**；页面展开式 3 × 3 × 3 × 3 = **81** 与结果行逐字符自洽（避免只锚最终结果、展开行不自洽）。默认参数（2^10=1024 一类）不同 ⇒ 不命中。",
  },
  {
    slug: "science/root-calculator",
    inputs: { x: "27" },
    expect: ["√27 = 3√3 ≈ 5.196", "验证：5.196 × 5.196 = 27 ≈ 27"],
    ref: "开平方与化简（x=27）：√27 = √(9×3) = **3√3 ≈ 5.196**；页面自验行 5.196 × 5.196 = 26.98 ≈ 27，与化简式同源可交叉复算；页面另给 x² = 729 作反向校验。默认参数（√2 一类）不同 ⇒ 不命中。",
  },

  // ---- BATCH254：描述统计 / 相关 / 显著性族（8 例）——「分步推导行」的第三轮复用 ----
  // 【判据】统计族比公式族多一层「n 与排序」耦合，但产出形态同样是**可手算的分步行**，打法不变：
  // 锚「同一量的两个不同算式行」或「计算步骤行里的中间量」。本批唯一撞默认的是 `quadratic-equation`，
  // 原因是它的默认参数恰为 a=1/b=-3/c=2（Δ=9−8=1，与注入的 1/−5/6 判别式同为 1）⇒ 原锚 `√Δ = √1 = 1`
  // 在默认态必命中。**教训：判别式这类「只由 a、b、c 组合、与分区间无关的量」撞默认值概率高，优先锚
  // 「直接含注入值字面量的行」（`(5 + 1) / 2` 里的 5 来自 −b）而不是「只含判别式结果的行」。**
  // 本批弃页：`science/probability-calculator`（单页挂 5 种分布、字段重名 x1/x2/k1 跨分布复用 ⇒ 只命中
  // 默认分布分支，注入无法可靠定位到目标分布 ⇒ 不硬写）。
  {
    slug: "science/quartile-calculator",
    inputs: { data: "2, 4, 6, 8, 10, 12" },
    clicks: ["calculate()"],
    expect: ["IQR = Q3 − Q1 = 9.5 − 4.5 = 5", "上界 = Q3 + 1.5×IQR = 9.5 + 7.5 = 17"],
    ref: "四分位数（线性插值法，n=6）：pos = (n−1)×p ⇒ Q1 位置 = 5×0.25 = 1.25 ⇒ Q1 = 4 + 0.25×(6−4) = **4.5**；Q2 位置 = 2.5 ⇒ Q2 = 6 + 0.5×(8−6) = **7**；Q3 位置 = 3.75 ⇒ Q3 = 8 + 0.75×(10−8) = **9.5**。IQR = 9.5 − 4.5 = **5**；异常值上界 = 9.5 + 1.5×5 = **17**、下界 = 4.5 − 7.5 = −3（三条均可手算复算，且互为一体）。默认数据不同 ⇒ 不命中。",
  },
  {
    slug: "science/correlation-calculator",
    inputs: { xData: "1, 2", yData: "3, 4" },
    clicks: ["calculate()"],
    expect: ["样本量过小：n = 2", "不能据此推断总体相关强度或统计显著性"],
    ref: "n=2 小样本：只要 X/Y 都有差异，Pearson r 必然为 ±1；页面必须保留 r 但明确说明不能推断总体相关或显著性。默认 5 组数据不出现该提示 ⇒ 非逃生。"
  },
  {
    slug: "science/correlation-calculator",
    inputs: { xData: "1, 2, 3, 4, 5", yData: "2, 4, 6, 8, 10" },
    clicks: ["calculate()"],
    expect: ["r = 20 / √(10 × 40) = 20 / 20 = 1", "Σ(xᵢ−x̄)² = 10；Σ(yᵢ−ȳ)² = 40"],
    ref: "皮尔逊相关系数（X=1..5、Y=2,4,6,8,10，完全正线性）：x̄=3、ȳ=6；Σ(xᵢ−x̄)(yᵢ−ȳ) = 8+2+0+2+8 = **20**；Σ(xᵢ−x̄)² = 4+1+0+1+4 = **10**、Σ(yᵢ−ȳ)² = 16+4+0+4+16 = **40**；r = 20/√(10×40) = 20/20 = **1**、r² = 1（100% 可解释）。明细表合计行 10/40/20 与上面三式逐项自洽。默认数据不同 ⇒ 不命中。",
  },
  {
    slug: "science/calc-stats",
    inputs: { data: "2, 4, 6, 8", typ: "mean" },
    clicks: ["calc()"],
    expect: ["方差（样本） 6.6667", "标准差（样本） 2.5820"],
    ref: "样本统计量（n=4，数据 2,4,6,8）：均值 = 20/4 = **5.0000**；Σ(xᵢ−5)² = 9+1+1+9 = 20 ⇒ 样本方差 = 20/(4−1) = **6.6667**、样本标准差 = √6.6667 = **2.5820**、变异系数 = 2.5820/5 = 51.64%；极差 = 8−2 = 6.0000、Q1 = 3.5000、Q3 = 6.5000、IQR = 3.0000，均与上两行同源可交叉复算。默认数据不同 ⇒ 不命中。",
  },
  {
    slug: "science/calc-stats",
    inputs: { data: "0,1,2,3,4", typ: "sample" },
    clicks: ["calc()"],
    expect: ["均值 2.0000", "方差（样本） 2.5000"],
    ref: "数据列表以 0 开头（0,1,2,3,4）：n=5、均值=10/5=2.0000、样本方差=Σ(x−2)²/4=(4+1+0+1+4)/4=2.5000。修复前 ①__D 把 data 误登记为分母字段、②全零守卫对 textarea 用 parseFloat 取首段=0 → 合法数据被拒「data 是本计算的分母」；修复后按分隔符拆值逐项判断。默认数据不同 ⇒ 不命中",
  },
  {
    slug: "science/statistics-calculator",
    inputs: { data: "2, 4, 6, 8, 10", dtype: "population" },
    clicks: ["calculate()"],
    expect: ["方差（总体）= Σ(xᵢ − x̄)² / n = 8", "标准差 = √方差 = √8 = 2.828"],
    ref: "总体描述统计（n=5，数据 2,4,6,8,10，population 口径）：Σx = **30**、均值 x̄ = 30/5 = **6**；总体方差 = Σ(xᵢ−6)²/n = (16+4+0+4+16)/5 = 40/5 = **8**；总体标准差 = **√8 = 2.828**；标准误 SE = 2.828/√5 = 1.265、中位数 6、极差 8、偏度 0（对称）、峰度 −1.3（扁峰），均与上式自洽。默认数据/dtype 不同 ⇒ 不命中。",
  },
  {
    slug: "science/statistics-calculator",
    inputs: { data: "5, 5, 5", dtype: "population" },
    clicks: ["calculate()"],
    expect: ["—/不适用（方差为 0，样本无偏度）"],
    ref: "常数数据方差为0，偏度/峰度无定义；旧版 fmt(NaN)='未定义' 却按 skew>0/skew<0 判假落入'对称/正态'；新版 isFinite 门控显示不适用。默认数据不含此串，强判别"
  },
  {
    slug: "science/exp-calculator",
    inputs: { x: "5" },
    clicks: ["calculate()"],
    expect: ["e^5 = 148.413", "e^(−5) = 1 / e^5 = 0.007"],
    ref: "自然指数（x=5）：e ≈ 2.718281828459045 ⇒ e^5 = **148.413**；e^(−5) = 1/148.413 = **0.007**；双曲函数 sinh = (eˣ−e⁻ˣ)/2 = (148.413−0.007)/2 = 74.203、cosh = 74.21、tanh = sinh/cosh = 1，与上行同源可交叉复算；10ˣ = 100,000、2ˣ = 32 亦自洽。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/exp-calculator",
    inputs: { x: "1000" },
    clicks: ["calculate()"],
    expect: ["tanh(x) = sinh/cosh 1"],
    ref: "SMS-90 清账：x=1000 时 e^x 溢出为 ∞，旧版 sinh/cosh 均 ∞、tanh=NaN，fmt(NaN) 落 '-∞' 分支（x=1000 与 x=-1000 同为 -∞）；现用稳定式 tanh=±(1−e^(−2|x|))/(1+e^(−2|x|))，x=1000 得 +1。默认 x=2 得 tanh≈0.96 不含本串，零逃生。",
  },
  {
    slug: "science/exp-calculator",
    inputs: { x: "0.0005" },
    clicks: ["calculate()"],
    expect: ["x = 5.000000e-4", "e^5.000000e-4 = 1.000500"],
    ref: "SMS-91 清账：x=5e-4 旧版 fmt 普通分支用无精度 toLocaleString，Node 默认三位小数把 x 与 e^x 都显示 0，与 e^x 恒正矛盾；现阈值收紧到 |x|<1e-3 走科学计数，x 显示 5.000000e-4、e^x=exp(0.0005)=1.000500125 → 1.000500。旧版不含两串，零逃生。",
  },
  {
    slug: "science/power-calculator",
    inputs: { base: "2", exp: "-10" },
    clicks: ["calculate()"],
    expect: ["2^-10 = 9.7656250000e-4"],
    ref: "SMS-132 清账：2^-10=1/1024=0.0009765625，旧版普通分支 toLocaleString 三位小数显示 0.001（丢失 2.4% 精度），现阈值 <1e-3 走 toExponential(10) 得 9.7656250000e-4。默认 2^10=1024 不含此串，零逃生。",
  },
  {
    slug: "science/quadratic-equation",
    inputs: { a: "-1", b: "0", c: "-1" },
    clicks: ["solve()"],
    expect: ["x₁ 0 + 1i", "x₂ 0 − 1i"],
    ref: "a<0 的共轭复根：x²+1=0 → x=±i。虚部须一正一负；修复前 im=sq/(2a) 在 a=−1 时为 −1，两根拼成「0 + -1i」与「0 − 1i」都是 −i；修复后 im 取绝对值，得「x₁0 + 1i」「x₂0 − 1i」。默认 a=1 实根不命中",
  },
  {
    slug: "science/quadratic-equation",
    inputs: { a: "1", b: "-5", c: "6" },
    clicks: ["solve()"],
    expect: ["精确：x = (5 + 1) / 2", "精确：x = (5 - 1) / 2"],
    ref: "一元二次方程求根（a=1、b=−5、c=6）：Δ = b² − 4ac = 25 − 24 = **1** ⇒ √Δ = 1，x = (−b ± √Δ)/(2a) = (**5 ± 1**)/2 ⇒ x₁ = **3**、x₂ = **2**。**默认参数恰为 a=1/b=−3/c=2，其 Δ 同样为 1** ⇒ 判别式结果行（`√Δ = √1 = 1`）在默认态必命中，是本例唯一可用的判别式行 ⇒ 改锚两条「含注入值字面量 5」的精确根表达式。默认态的 −b = 3 ⇒ 其式为 `(3 + 1) / 2`，与本例不同 ⇒ 双态通过。",
  },
  {
    slug: "science/significant-figures",
    inputs: { num: "1234.5678", digits: "3" },
    clicks: ["calc()"],
    expect: ["保留 3 位有效数字： 1230", "科学计数法： 1.23e+3"],
    ref: "有效数字（1234.5678 保留 3 位）：从左起非零数 1 起算第 3 位 = 百位 ⇒ 四舍五入到百位 = **1230**；科学计数法 = **1.23e+3**（1.23×10³ 与原值同量级）。两行分别对应「定点记数」与「科学记数」两种表示，手算可复算且互不依赖。默认参数不同 ⇒ 不命中。",
  },

  // ---- BATCH255：向量/三角/化学/运动学/地理/π/字母表/湿球湿度族（8 例） ----
  // 【判据】本批收的是**「固定查表 + 公式混合」三类新形态**：① `nato-phonetic`（纯查表，产物 = 字母→NATO 词，
  // 逐字母手算复算，默认输入不含 SOS）；② `pi-digits`（查表 + 截断，**唯一可锚的是「位数」行** —— 只锚数字串
  // `3.1415926535` 会因默认态的更长 π 串含同一子串而**必命中**，必须连「10 位数」前缀一起锚）；
  // ③ `astro-geo-calculator` 湿度分支（Magnus 公式：饱和水汽压 42.34 / 31.60 hPa、实际水汽压 28.25 hPa、
  // RH = 28.25/42.34 = 66.7%，四行同源可交叉复算）。
  // 【判据】「换值撞同值」的两种新形态：① **常量换算表页**（`science-pressure-converter` 默认 val 恰为 1，
  // 与注入同值 ⇒ 全线输出同串 ⇒ 弃）；② 默认组与注入组恰好相同反而省事（`calc-1` 自洽组直接一次过）。
  // **处置仍是「先跑双态、撞了换组」，不能因为「默认就好算」而跳过核验。**
  // 本批弃页：`vector-calculator`／`matrix-calculator`（注入用的是**动态 id** —— `id="a'+i+'"` 由 `build()`
  // 生成，判别器 `pageDefaults()` 只能回退 HTML 里的静态控件 ⇒ 这些键在「模拟注入失败」时**回不去默认值**，
  // 用例照样 PASS ⇒ 被判别器判为逃生项。**这是「双态核验过了、门禁仍红」的一类新形态，见 SKILL「动态 id」条。**
  // 其余弃页：`equation-balancer`（默认样例就是 H₂+O₂→H₂O，注入同反应 ⇒ 产物同串）、
  // `battery-life-calculator`（默认态同命中 ⇒ 逃生）、`science-pressure-converter`（默认 val 恰为 1 ⇒ 撞同值）、
  // `wire-gauge-converter` / `science-flow-rate`（注入被 setMode 下拉回写或单位不自洽 ⇒ 无法手算复算）、
  // `rfc-validator`（只有输入回显 + 「格式不符」结论词）、`periodic-table`（运行时建表，harness 内无产物）、
  // `calc-4` / `calc-5`（「留空求未知」型，harness 内无法留空 ⇒ 提前 return）。
  {
    slug: "science/coulomb-force",
    inputs: { q1: "2", q2: "3", r: "2" },
    clicks: ["calcTool()"],
    expect: ["0.0135 N", "0.0270 电势能 U (J)"],
    ref: "库仑静电力（q₁=2 μC、q₂=3 μC、r=2 m）：F = k·q₁q₂/r² = 8.99e9×2e-6×3e-6/4 = 0.05394/4 = **0.0135 N**；电势能 U = k·q₁q₂/r = 0.05394/2 = **0.0270 J**；页面另给「q₁ 在 r 处场强 E = 4494 N/C」（= k·q₁/r²），与上式同源可交叉复算。默认电荷/半径不同 ⇒ 不命中。",
  },
  {
    slug: "science/log-calculator",
    inputs: { x: "8", base: "2" },
    clicks: ["calculate()"],
    expect: ["log 2 (8) = 3", "= ln(8) / ln(2) = 2.079 / 0.693 = 3"],
    ref: "对数（x=8、底 n=2）：换底公式 log_n(x) = ln(x)/ln(n) = 2.079/0.693 = **3**，验证 2³ = 8；页面同给 log₁₀8 = 0.903、ln 8 = 2.079，与上两行同源自洽。默认底数/真数不同 ⇒ 不命中。",
  },
  {
    slug: "science/log-calculator",
    inputs: { x: "0.00001", base: "10" },
    clicks: ["calculate()"],
    expect: ["x = 1.000000e-5"],
    ref: "SMS-105 清账（极小真数回显）：fmt 原用 toLocaleString 默认最多 3 位小数，1e-5 显示为 0，页面写「x = 0」；现把科学计数阈值放宽到 ≤1e-3，1e-5 显示 x = 1.000000e-5。旧版锚不成立 ⇒ 零逃生。",
  },
  {
    slug: "science/trigonometry-calculator",
    inputs: { x: "3", y: "4" },
    clicks: ["calculate()"],
    expect: ["角度 → 弧度：3° × π/180 = 0.052", "tan = sin/cos = 0.052/0.999 = 0.052"],
    ref: "三角函数（x=3°）：弧度 = 3×π/180 = **0.052**；sin(3°) = **0.052**、cos(3°) = **0.999** ⇒ tan = 0.052/0.999 = **0.052**（应为 0.0524，页面按 3 位有效数字截断 ⇒ 与 sin 行同源自洽）；csc = 1/sin = 19.107、sec = 1/cos = 1.001、cot = 19.081，与上面三行互为例函数关系可交叉复算。默认角度不同 ⇒ 不命中。",
  },
  {
    slug: "science/chemistry-calculator",
    inputs: { gasP: "2", gasV: "10", gasN: "1", gasT: "300" },
    clicks: ["calcGas()"],
    expect: ["P = nRT/V = 1 × 8.314 × 300 / 10 = 249.42 Pa", "P = 249.42 Pa"],
    ref: "理想气体状态方程求压强（n=1 mol、V=10 L、T=300 K、R=8.314 J/(mol·K)）：P = nRT/V = 1×8.314×300/10 = **249.42 Pa**；页面高亮结果与上式逐字符自洽，并给出摄氏温度 300 K − 273.15 = 26.85 °C 作交叉校验。默认 gasFind 分支不同 ⇒ 不命中。",
  },
  {
    slug: "science/chemistry-calculator",
    inputs: {},
    clicks: ["var a=calcMolarMass('H2Zz'),b=calcMolarMass('2H2O'),c=calcMolarMass('CuSO4.5H2O');document.getElementById('formula').value='CHM83_'+(a.error&&Math.abs(b.totalMass-36.032)<0.01&&Math.abs(c.totalMass-249.7)<0.01?'OK':'BAD');"],
    expect: ["CHM83_OK"],
    ref: "SMS-83 清账：未知元素 H2Zz 旧版静默跳字给 2.016，现返回 error；2H2O 旧版段首系数丢失给 18.016，现按 2 个水分子 = 36.032；CuSO4.5H2O 旧版点号未解析给 177.636，现按结晶水（本页 O=16.00）= 249.70。探针断言三者同时成立，旧版 ⇒ CHM83_BAD，零逃生。",
  },
  {
    slug: "science/chemistry-calculator",
    inputs: {},
    clicks: ["currentCategory='concentration';selectCategory('concentration');document.getElementById('concType').value='dilution';renderConcInputs();document.getElementById('concC1').value='1';document.getElementById('concV1').value='2';document.getElementById('concC2').value='';document.getElementById('concV2').value='4';calcConcentration();var h1=String(document.getElementById('output').textContent||document.getElementById('output').innerHTML);document.getElementById('concC2').value='0.5';document.getElementById('concV2').value='';calcConcentration();var h2=String(document.getElementById('output').textContent||document.getElementById('output').innerHTML);document.getElementById('concC1').value='CHMDIL_'+(h1.indexOf('C₂ = 0.5')>=0&&h2.indexOf('V₂ = 4')>=0?'OK':'BAD');"],
    expect: ["CHMDIL_OK"],
    ref: "SMS-84 清账：稀释公式 C₁V₁=C₂V₂。C₁=1、V₁=2，留空 C₂ 且给 V₂=4 → C₂=1×2/4=0.5；留空 V₂ 且给 C₂=0.5 → V₂=1×2/0.5=4。旧版 C₂ 留空即报「请输入最终浓度」、给了 C₂ 又被覆盖，两个方向无法都算；现恰好留空一个即可双向求解。探针断言两向结果都出现，旧版 ⇒ CHMDIL_BAD，零逃生。",
  },
  {
    slug: "science/chemistry-calculator",
    inputs: { gasP: "101325", gasV: "0.0224", gasT: "-10", gasN: "1" },
    clicks: ["calcGas()"],
    expect: ["热力学温度须大于 0"],
    ref: "SMS-85 清账：理想气体 T=-10 K 旧版直接算 n=PV/(RT) 得负物质的量；现非求解字段校验正数，T≤0 明确报错并停算。默认 T=300 不含本串，零逃生。",
  },
  {
    slug: "science/calc-1",
    inputs: { height: "80", v0: "0", gravity: "10" },
    clicks: ["calc()"],
    expect: ["落地时间 t： 4.0000 秒", "落地速度 v： 40.0000 米/秒"],
    ref: "自由落体（h=80 m、v₀=0、g=10 m/s²，忽略空气阻力）：由 h = ½gt² 得 t = √(2h/g) = √(160/10) = **4.0000 s**；落地速度 v = gt = 10×4 = **40.0000 m/s**；平均速度 = h/t = 80/4 = **20.0000 m/s**（三行同源自洽）。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/geo-distance-calculator",
    inputs: { lat1: "0", lon1: "0", lat2: "0", lon2: "1" },
    clicks: ["calculate()"],
    expect: ["大圆距离： 111.1949 km", "初始方位角： 270.0000°"],
    ref: "Haversine 大圆距离（A=(0°,0°)、B=(0°,1°)，地球半径 6371 km）：同纬度 1° 子午弧长 = 6371×π/180 = **111.1949 km**；初始方位角 = atan2(sin Δλ·cos φ₂, cos φ₁·sin φ₂ − sin φ₁·cos φ₂·cos Δλ)，φ₁=φ₂=0 ⇒ 正西方向 = **270.0000°**（页面标注「正西 (W)」）。两行可分别手算复算且互为方向校验。默认经纬度对不同 ⇒ 不命中。",
  },
  {
    slug: "science/geo-distance-calculator",
    inputs: {},
    clicks: ["document.getElementById('lat1').value='100';document.getElementById('lon1').value='0';document.getElementById('lat2').value='0';document.getElementById('lon2').value='0';calculate();var e=document.getElementById('error1');var t=String(e.textContent||'');var s=!!(e.classList&&e.classList.contains&&e.classList.contains('show'));document.getElementById('lat1').value='GEOERR_'+(t.indexOf('纬度范围应为 -90 ~ 90')>=0&&s?'OK':'BAD');"],
    expect: ["GEOERR_OK"],
    ref: "SMS-97 清账（同组错误容器）：lat1=100 非法、lon1=0 合法。旧版 validateInput 每次先 error1.classList.remove('show')，后校验的 lon1 把 lat1 的错误提示抹掉（文本仍在但不可见）；现按字段保存错误并聚合渲染，纬度越界提示保持可见。探针同时断言文本与 show 状态，旧版 ⇒ GEOERR_BAD，零逃生。",
  },
  {
    slug: "science/pi-digits",
    inputs: { n: "10" },
    clicks: ["run()"],
    expect: ["10 位数 3.1415926535…"],
    ref: "π 前 N 位（n=10）：π = **3.1415926535…**。**关键在锚「位数」行而不是数字串** —— 默认 n 更大时页面输出的 π 串含 `3.1415926535` 作前缀，只锚该数字串会被默认态子串命中（逃生），锚 `10 位数 …` 才随 n 变。默认位数不同 ⇒ 不命中。",
  },
  {
    slug: "science/nato-phonetic",
    inputs: { input: "SOS" },
    clicks: ["convert()"],
    expect: ["S Sierra O Oscar S Sierra"],
    ref: "NATO 字母表转写（输入 SOS，默认 setMode 为字母模式）：S → **Sierra**、O → **Oscar**、S → **Sierra**，逐字母对应、无公式依赖，可逐字手算复算。默认输入串不同 ⇒ 不命中。",
  },
  {
    slug: "science/nato-phonetic",
    inputs: { input: "YZ" },
    clicks: ["setMode('ansi');convert();var h=String(document.getElementById('output').innerHTML);document.getElementById('input').value='ANSIYZ_'+(h.indexOf('YOKE')>=0&&h.indexOf('ZEBRA')>=0&&h.indexOf('YOUNG')<0&&h.indexOf('ZEBA')<0?'OK':'BAD');"],
    expect: ["ANSIYZ_OK"],
    ref: "SMS-112 清账（ANSI 词表）：旧 ANSI 老表 Y=YOUNG、Z=ZEBA，现改 Y=YOKE、Z=ZEBRA。探针切 ANSI 后转写 YZ，断言新词齐全且旧词不再出现；默认 NATO 模式不含这些锚 ⇒ 零逃生。",
  },
  {
    slug: "science/nato-phonetic",
    inputs: {},
    clicks: ["var s=String(__nato_phoneticExtras);var cb=null;globalThis.TBKit={util:{isEn:function(){return false;},diffBox:function(){},exportTable:function(){}},matrix:{table:function(){}},chart:{line:function(){}},history:{list:function(){return [];},record:function(){},mount:function(_,f){cb=f;}}};__nato_phoneticRender(['input'],'结果',false);if(cb)cb({input:'SOS',__natoMode:0,结果:'S Sierra O Oscar S Sierra'});delete globalThis.TBKit;var h=String(document.getElementById('output').innerHTML);document.getElementById('input').value='NATOHIST_'+(s.indexOf('__natoMode')>=0&&typeof modeIdx==='number'&&modeIdx===0&&h.indexOf('Sierra')>=0&&h.indexOf('SUGAR')<0?'OK':'BAD');"],
    expect: ["NATOHIST_OK"],
    ref: "SMS-113 清账（历史模式回填）：旧版历史点击无条件 setMode()（无参）→ else 分支强制 ANSI，NATO 模式记录也被切到 ANSI（S→SUGAR）。现 Extras 写入 __natoMode，mount 回调按保存值恢复；探针用 mode=0 的 NATO 记录断言恢复 modeIdx=0 且输出 Sierra 而非 SUGAR，并要求源码确实写入 __natoMode。旧版 ⇒ NATOHIST_BAD，零逃生。",
  },
  {
    slug: "science/astro-geo-calculator",
    inputs: { "hum-dry": "30", "hum-wet": "25", "prs-alt": "1000" },
    clicks: ["calcHumidity()"],
    expect: ["66.7% 相对湿度（Magnus 公式近似）", "28.25 实际水汽压（hPa）"],
    ref: "干湿球湿度（干球 30 °C、湿球 25 °C、气压 1000 hPa，Magnus 近似）：干球饱和水汽压 = 6.112·e^(17.62×30/(243.12+30)) = **42.34 hPa**、湿球 = 6.112·e^(17.62×25/(243.12+25)) = **31.60 hPa**、干湿温差 = **5.0 °C**；实际水汽压 e = e_wet − P·Δt·0.00066·(1+0.00371·t_wet) = 31.60 − 1000×5×0.00066×(1+0.00371×25) = **28.25 hPa**；相对湿度 = 28.25/42.34 = **66.7%**。四行同源可交叉复算。默认参数不同 ⇒ 不命中。",
  },
  {
    slug: "science/calc-2",
    inputs: { gasR: "0.0821", P: "1", V: "1", n: "1", T: "273" },
    clicks: ["calc()"],
    expect: ["常规表示： 22.4133 Pa", "计算结果： 2.2413e+1 Pa"],
    ref: "理想气体状态方程求压强（R=0.0821 L·atm/(mol·K)、V=1、n=1、T=273 K，解目标 = P）：P = nRT/V = 1×0.0821×273/1 = **22.4133 Pa**（科学计数 2.2413e+1）；页面另给常规表示与前三行逐字符自洽。默认 solveFor / 已知量不同 ⇒ 不命中。",
  },

  // ---- BATCH256：坐标/距离/号段/压力/电池族（5 例）——「撞同值 ⇒ 换一组参数」第三次奏效 ----
  // 【判据】本批最有价值的一条判据是 **「撞默认 ⇒ 换组」在**常量换算表页**与**电量页**上都成立**：
  // `science-pressure-converter` 默认 val 恰为 1（BATCH255 判过逃生 ⇒ 弃），把 val 换到 2 后
  // `2 kPa = 20 mbar = 15.0012 mmHg` 全线随值变 ⇒ 双态过；`battery-life-calculator` 默认组与
  // 注入组同为 1 Ah/0.1 A（⇒ 同为 0.37 W / 3.70 Wh 而逃生），换 2000 mAh/200 mA 后 0.74 W / 7.40 Wh
  // 双态过。**处置顺序固定为：先跑双态 → 撞默认就换一组 → 换组还撞才弃**，不要因为「第一次撞了」就下弃页结论。
  // 【判据】UTM 换算页只锚**可手算的带号/中央经线**（zone = ⌊lon/6⌋+1 = 51，central meridian = 6×zone−3 = 123.0°），
  // 东移值 309049.536 m 依赖完整 UTM 投影、无法手算 ⇒ 一律不锚。
  // 本批弃页：`tide-height-estimator`（注入 lat 后默认态仍命中 ⇒ 逃生，且注入态本身也不过）、
  // `gcd-calculator` / `lcm-calculator`（**两页共用 `nums` 单输入框 + 递归实现**，喂 2 个数也会死循环吃光 4 GB
  // 内存，且报错里**不带页面名** ⇒ 与 BATCH251 的 OOM 是同一形态，直接弃）、`passphrase-generator`
  // （`wordCount` 注入不生效，熵值与词数行恒为默认值 ⇒ 锚不上）、`text-extract-phones` /
  // `calculator`（运行时建 DOM，harness 内产物为空）、`resistor-color-code`（`formatResistance` 在桩内抛错 ⇒
  // 反向模式产物不可达）、`barcode-pharmacode`（编码库未加载）、`pcb-trace-width`（IPC 线宽公式无法手算复算）。
  // 注：`logic-gate-simulator` 已于 2026-11-05 解锁（共享桩补齐 dataset 与 tbody 段作用域后立例，见下条）。
  {
    // 2026-11-05：共享桩补 dataset / tbody 段作用域后本页解锁（原判「运行时建 DOM，产物为空」）。
    // 页面末尾直接 init() → selectGate('AND')；真值表行由 innerHTML 生成，高亮时读 tr.dataset.row。
    slug: "science/logic-gate-simulator",
    // 默认态：AND，inputA/inputB 均为 0。clicks 改为 XOR 并把 A 置 1（B 保持 0）。
    clicks: ["selectGate('XOR');toggleInput('A');"],
    expect: ["1 XOR 0 =", "XOR（异或门）：输入不同输出1"],
    ref: "默认态 AND(0,0) ⇒ 输出 0、表达式 0 AND 0 = 0、提示 AND（与门）：两输入全1输出1；注入"
      + "selectGate('XOR') + toggleInput('A') ⇒ inputA=1/inputB=0，XOR(1,0) = 1 ⇒ 输出 1、表达式 1 XOR 0 = 1、"
      + "提示改为 XOR（异或门）：输入不同输出1。两态输出 0 vs 1、提示文本互斥 ⇒ 判别明确、非逃生。",
  },
  {
    slug: "science/latlon-utm-converter",
    inputs: { lat: "31", lon: "121" },
    clicks: ["convertLL2UTM()"],
    expect: ["51 UTM带号", "中央经线： 123.0°"],
    ref: "经纬度→UTM（北纬 31°、东经 121°）：带号 = ⌊121/6⌋+1 = **51**；中央经线 = 6×51−3 = **123.0°**（页面同样标出半球 N、比例因子 1.000050、收敛角 −0.8829°，但东移值 309049.536 m 依赖完整投影、不可手算 ⇒ 不锚）。默认经纬度不同 ⇒ 不命中。",
  },
  {
    slug: "science/calc-distance",
    inputs: { lat1: "0", lon1: "0", lat2: "0", lon2: "1" },
    clicks: ["calc()"],
    expect: ["111.195 距离 (km)", "69.093 距离 (英里)"],
    ref: "两点距离（A=(0°,0°)、B=(0°,1°)，地球半径 6371 km）：大圆距离 = 6371×π/180 = **111.195 km**；英里换算 = 111.195×0.621371 = **69.093 mi**、海里 = **60.040 NM**；初始方位角 = **90.0°（东）**、中点 (0.00000, 0.50000)、距离 = **111194.9 m**，四行同源可交叉复算。默认坐标不同 ⇒ 不命中。",
  },
  {
    slug: "science/calc-distance",
    inputs: { lat1: "40", lon1: "116", lat2: "31.907", lon2: "116" },
    clicks: ["calc()"],
    expect: ["1 小时 0 分"],
    ref: "飞行时间分钟进位：A=(40,116)、B=(31.907,116) 距离≈899.9km，÷900=0.9999h，分钟 round(0.9999×60)=60 → 须进位为「1 小时 0 分」，不得显示「0 小时 60 分」。默认坐标不同 ⇒ 不命中",
  },
  {
    slug: "life/phone-lookup",
    inputs: { input: "13812345678" },
    clicks: ["validate()"],
    expect: ["数字位数： 11", "推断国家： 中国（中国大陆手机号格式）"],
    ref: "手机号段识别（输入 13812345678）：位数 = **11**（11 位国内手机号）；按 138 号段前缀查表得归属国家「**中国（中国大陆手机号格式）**」与推断运营商「移动」，归一化结果与输入同值（11 位无需补 86）。号段结论与位数行均由注入值唯一决定，可手算复算。默认号码不同 ⇒ 不命中。",
  },
  {
    // 遮蔽回归：本页本地格式化函数已改名 fmtPress，避免被 js/common.js 的全局 fmtNum 覆盖。
    // 3 Pa 换到 kPa / MPa 均是非零极小值（0.003 / 3e-6）；若被全局 2 位小数实现接管，会显示 0.00。
    slug: "science/science-pressure-converter",
    inputs: { val: "3", from: "Pa" },
    clicks: ["convert()"],
    expect: ["3.0000 m", "3.0000 μ"],
    ref: "本地 fmtPress 按 SI 前缀定标并保留 4 位小数：3 Pa = 0.003 kPa ⇒ (0.003×1000).toFixed(4)='3.0000'+' m'；3 Pa = 3e-6 MPa ⇒ (3e-6×1e6).toFixed(4)='3.0000'+' μ'。全局 fmtNum（固定 2 位、无单位）会渲染成 '0.00'，故本断言只有本地实现生效才命中。val 取 3 而非 1 是为了避开页面默认态（默认 val=1/from=kPa 的 MPa 卡正好也是 '1.0000 m'）——否则判别器「换回默认值」时仍命中，会被判逃生项。",
  },
  {
    slug: "science/science-pressure-converter",
    inputs: { val: "2", from: "kPa" },
    clicks: ["convert()"],
    expect: ["20.0000 m bar · 巴", "15.0012 mmHg · 毫米汞柱"],
    ref: "压力单位换算（2 kPa → 各单位）：1 kPa = 10 mbar、7.5006 mmHg ⇒ 2 kPa = **20.0000 mbar**、**15.0012 mmHg**；同组另有 2.0000 MPa（应为 0.002，页面按各目标单位自动定标显示为 2.0000 m MPa）、290.0755 PSI、203.9432 mmH₂O、19.7385 atm，均与「×2」自洽。换算系数是常量表，但**数值随输入的 val 变** ⇒ 换值后与默认（val=1）不命中。",
  },
  {
    slug: "science/battery-life-calculator",
    inputs: { cap: "2000", curr: "200", volt: "3.7" },
    clicks: ["calc()"],
    expect: ["0.74 W", "7.40 Wh"],
    ref: "电池放电（容量 2000 mAh = 2 Ah、电流 200 mA = 0.2 A、电压 3.7 V）：功率 P = 3.7×0.2 = **0.74 W**；电能 E = 3.7×2 = **7.40 Wh**；续航 = 2 Ah/0.2 A = **10 小时**（页面时间轴 100%→0 秒/10 小时、90%→1 小时…与之一致）。默认组（1 Ah / 0.1 A）在 BATCH255 判过逃生 ⇒ 本例换组到 2 Ah / 0.2 A 后 0.74 W / 7.40 Wh 双态过。",
  },
  {
    slug: "science/battery-life-calculator",
    inputs: {},
    clicks: ["var __exp=0;globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){__exp++;}},diffBox:function(){}};document.getElementById('cap').value='3000';document.getElementById('curr').value='100';document.getElementById('volt').value='3.7';document.getElementById('eff').value='1.5';__batteryExport();document.getElementById('cap').value='BATEXP_'+__exp+'_'+(document.querySelector('#battHidden tbody')?document.querySelector('#battHidden tbody').innerHTML.indexOf('3000')>=0?'Y':'N':'N');delete globalThis.TBKit;"],
    expect: ["BATEXP_0_N"],
    ref: "SMS-38 残留清账：导出函数原只守 capV/currV/volt，效率 eff 非法（如 150%）仍导出。现与主计算同口径要求容量/电流/电压>0 且 0<eff≤1，非法时提示且不导出。自建 TBKit 桩捕获 exportTable 调用次数 + 检查 #battHidden tbody：注入 eff=1.5 ⇒ 旧版导出 1 次且表含 3000（BATEXP_1_Y），修复后 0 次且表空（BATEXP_0_N）⇒ 变红，零逃生。"
  },
  {
    slug: "science/prime-number",
    inputs: { num: "91" },
    clicks: ["run()"],
    expect: ["91 不是素数"],
    ref: "素数判定（n=91 = 7×13）：页面走试除法，试到 i=7 时 91 % 7 === 0 ⇒ 判定「**不是素数**」，并列出最早发现的因子 7 与商 13。这条判**否定结论**比肯定结论更有判别力 —— 默认样例 97 是真素数，默认态绝不可能出现「不是素数」三个字。",
  },
  {
    slug: "science/prime-number",
    inputs: { num: "89" },
    clicks: ["run()"],
    expect: ["89 是素数"],
    ref: "素数判定（n=89，√89 ≈ 9.43 ⇒ 只需试 2,3,5,7，均不整除）：判定「**是素数**」，并给出位数 2、前一个素数 89−2=**89**…（实际为向前回溯得到的 89 之前的素数 83…本例锚定的「89 是素数」只依赖试除结论，无需依赖派生值）。与 91 那条互为反向对照，两条同页共存、互不削弱。",
  },
  {
    slug: "science/prime-number",
    inputs: { num: "97.9" },
    clicks: ["run()"],
    expect: ["请输入正整数"],
    ref: "严格整数解析（SMS-134）：parsePositiveInt 用 Number() 后 Number.isSafeInteger 校验，小数 97.9 不是整数 ⇒ 拒绝并提示「请输入正整数」，不再被旧 parseInt 静默截成 97 而误判「97 是素数」。默认态 num=97 是真素数，不命中该提示；旧版注入失败会判「97 是素数」⇒ 本用例变红，判别力真实。",
  },
  {
    slug: "science/prime-number",
    inputs: { num: "1e3" },
    clicks: ["run()"],
    expect: ["1000 不是素数"],
    ref: "科学计数解析（SMS-134）：number 输入框 value 对「1e3」保留原串，parsePositiveInt 用 Number('1e3')=1000 且为安全整数 ⇒ 按 1000 判定为合数「1000 不是素数」；旧 parseInt('1e3') 截成 1 判「1 不是素数」，与本 expecting 串不同 ⇒ 注入失败即变红。1000=2³×5³ 有因子 2，否定结论只依赖数值 1000。",
  },
  {
    slug: "science/si-unit-converter",
    inputs: { fromValue: "5", fromUnit: "7", toUnit: "10" },
    clicks: ["convert()"],
    expect: ["5,000"],
    ref: '独立复算：长度量，5 千米(km,×1e3) → 米(m,×1)，result=5×1e3/1=5000，fmt 走 toLocaleString(\'zh-CN\') 得千分位 \'5,000\'。select 的 selected 在桩不生效，fromUnit/toUnit 均显式注入索引（7=km,10=m）。默认态 fromValue=1、两 select 桩取首个 option(index 0=Ym) ⇒ result=1，不命中 \'5,000\'。'
  },
  {
    slug: "science/si-unit-converter",
    inputs: { fromValue: "3", fromUnit: "10", toUnit: "13" },
    clicks: ["convert()"],
    expect: ["3,000"],
    ref: '独立复算：3 米(m,×1) → 毫米(mm,×1e-3)，result=3×1/1e-3=3000 ⇒ \'3,000\'。fromUnit=10(m),toUnit=13(mm)。'
  },
  {
    slug: "science/si-unit-converter",
    inputs: { fromValue: "2", fromUnit: "7", toUnit: "13" },
    clicks: ["convert()"],
    expect: ["2,000,000"],
    ref: '独立复算：2 千米(km,×1e3) → 毫米(mm,×1e-3)，result=2×1e3/1e-3=2e6 ⇒ \'2,000,000\'。fromUnit=7(km),toUnit=13(mm)。'
  },
  {
    slug: "science/si-unit-converter",
    inputs: { fromValue: "10", fromUnit: "10", toUnit: "13" },
    clicks: ["convert()"],
    expect: ["10,000"],
    ref: '独立复算：10 米(m,×1) → 毫米(mm,×1e-3)，result=10×1/1e-3=10000 ⇒ \'10,000\'。避坑：原 \'1,000\' 会被 runCase 步骤3 兜底无参调用 showPrefixTable() 的\'千\'(k,factor 1e3)命中（同 countdown 兜底副作用逃生），改用 \'10,000\' 不在词头表/导出单位表。fromUnit=10(m),toUnit=13(mm)。'
  },
  {
    slug: "science/si-unit-converter",
    inputs: { fromValue: "7", fromUnit: "7", toUnit: "12" },
    clicks: ["convert()"],
    expect: ["700,000"],
    ref: '独立复算：7 千米(km,×1e3) → 厘米(cm,×1e-2)，result=7×1e3/1e-2=7e5=700000 ⇒ \'700,000\'。fromUnit=7(km),toUnit=12(cm)。'
  },
  {
    slug: "science/si-unit-converter",
    inputs: { fromValue: "9", fromUnit: "7", toUnit: "13" },
    clicks: ["convert()"],
    expect: ["9,000,000"],
    ref: '独立复算：9 千米(km,×1e3) → 毫米(mm,×1e-3)，result=9×1e3/1e-3=9e6=9000000 ⇒ \'9,000,000\'。fromUnit=7(km),toUnit=13(mm)。'
  },
  {
    afterLoad: true,
    slug: "science/torque-converter",
    inputs: { val: "20", from: "lbft" },
    expect: ["2.711636e+1 牛·米 (N·m)"],
    ref: '扭矩换算（val=20，源单位 lb·ft）：baseNm = 20 × 1.35581795 = 27.116359 N·m；目标 N·m 列 = baseNm / 1 = 27.116359 → toExponential(6) 得 2.711636e+1。Python 独立复算 20×1.35581795=27.116359 与页面一致。锚取跨单位（N·m）派生量而非 lb·ft 同单位回显（同单位列恒等于输入 20→2e+1 属输入回显，不锚）。默认态（无注入：from 为空串导致 init 阶段 convert() 抛错、blob 为空）不命中该串。'
  },
  {
    afterLoad: true,
    slug: "science/torque-converter",
    inputs: { val: "5", from: "kgfm" },
    expect: ["4.903325e+1 牛·米 (N·m)"],
    ref: 'val=5，源单位 kgf·m：baseNm = 5 × 9.80665 = 49.03325 N·m；N·m 列 = 49.03325 → 4.903325e+1。Python 独立复算 5×9.80665=49.03325 一致。锚跨单位（N·m）派生量。默认态 blob 为空不命中。'
  },
  {
    afterLoad: true,
    slug: "science/torque-converter",
    inputs: { val: "3", from: "kNm" },
    expect: ["3.059149e+2 千克力·米 (kgf·m)"],
    ref: 'val=3，源单位 kN·m：baseNm = 3 × 1000 = 3000 N·m；kgf·m 列 = 3000 / 9.80665 = 305.9149 → 3.059149e+2。Python 独立复算 3000/9.80665≈305.9149 一致。锚取 kgf·m 跨单位量（kN·m 同单位列恒为输入 3→3e+3 属回显，不锚）。默认态不命中。'
  },
  {
    afterLoad: true,
    slug: "science/torque-converter",
    inputs: { val: "100", from: "lbin" },
    expect: ["1.129848e+1 牛·米 (N·m)"],
    ref: 'val=100，源单位 lb·in：baseNm = 100 × 0.11298483 = 11.298483 N·m；N·m 列 = 11.298483 → 1.129848e+1。Python 独立复算 100×0.11298483=11.298483 一致。锚跨单位（N·m）派生量（lb·in 同单位列恒为输入 100→1e+2 属回显，不锚）。默认态不命中。'
  },
  {
    afterLoad: true,
    slug: "science/torque-converter",
    inputs: { val: "50000", from: "gfcm" },
    expect: ["4.903325e+0 牛·米 (N·m)"],
    ref: 'val=50000，源单位 gf·cm：baseNm = 50000 × 9.80665e-5 = 4.903325 N·m；N·m 列 = 4.903325 → 4.903325e+0。Python 独立复算 50000×0.0000980665=4.903325 一致。锚跨单位（N·m）派生量。默认态不命中。'
  },
  {
    afterLoad: true,
    slug: "science/torque-converter",
    inputs: { val: "1000", from: "ozfin" },
    expect: ["7.061552e+0 牛·米 (N·m)"],
    ref: 'val=1000，源单位 ozf·in：baseNm = 1000 × 0.0070615518 = 7.0615518 N·m；N·m 列 = 7.0615518 → 四舍五入 7.061552e+0。Python 独立复算 1000×0.0070615518=7.0615518 一致。锚跨单位（N·m）派生量（ozf·in 同单位列恒为输入 1000→1e+3 属回显，不锚）。默认态不命中。'
  },

  // ── 零用例加固（2026-10-06）──────────────────────────
  {
    slug: "science/calc-5",
    inputs: { speed: "25", distance: "180" },
    expect: ["距离 s（m） 180.0000", "时间 t（s） 7.2000", "时间换算：7.20 秒"],
    ref: "注入非默认(默认 speed=10/distance=100)：以距离为目标解时间 t = s/v = 180/25 = 7.2 s（4 位小数）⇒ 7.2000，换算串 7.20 秒。默认态 100/10 = 10.0000 / 10.00 秒，三条均不命中。",
  },
  {
    slug: "science/calc-4",
    inputs: { density: "1250", mass: "8" },
    expect: ["质量 m（kg） 8.0000", "体积 V（m³） 0.006400", "体积 6.4000 L"],
    ref: "注入非默认(默认 density=1000/mass=1)：以质量为目标解体积 V = m/ρ = 8/1250 = 0.0064 m³（toFixed 6 ⇒ 0.006400）⇒ 6.4000 L；密度换算 1250 kg/m³ = 1.2500 g/cm³。默认态 1/1000 = 0.001000 / 1.0000 L，三条均不命中。",
  },
  {
    slug: "science/resistor-color-code",
    inputs: { revValue: "4700", revTol: "1" },
    expect: ["4.7 k\u03a9 \u6700\u63a5\u8fd1 E24 \u6807\u51c6\u503c\uff0c\u8272\u73af\uff1a\u9ec4 \u00b7 \u7d2b \u00b7 \u7ea2 \u00b7 \u68d5"],
    ref: "\u53cd\u67e5\u8272\u73af\uff1a4700 \u03a9 \u4e24\u4f4d\u6709\u6548\u6570\u5b57 4/7 \u21d2 \u7b2c1\u73af\u9ec4(4)\u3001\u7b2c2\u73af\u7d2b(7)\uff1b4700/(47\u00d710)=1 \u21d2 \u4e58\u6570\u9700 100 \u21d2 \u7b2c3\u73af\u7ea2(100\u00d7)\uff1b\u7cbe\u5ea6\u6ce8\u5165 revTol=1\uff08\u00b11%\uff09 \u21d2 \u7b2c4\u73af\u68d5\u3002\u624b\u5de5\u67e5\u8868\u6838\u5bf9\uff0c\u4e0d\u4f9d\u8d56\u9875\u9762\u8f93\u51fa\u3002\u9ed8\u8ba4 revValue=10000 \u21d2 10 k\u03a9 \u68d5\u00b7\u9ed1\u00b7\u7ea2\u00b7\u68d5\uff0c\u4e0d\u547d\u4e2d\u3002"
  },
  {
    slug: "science/resistor-color-code",
    inputs: { revValue: "6800", revTol: "1" },
    expect: ["6.8 k\u03a9 \u6700\u63a5\u8fd1 E24 \u6807\u51c6\u503c\uff0c\u8272\u73af\uff1a\u84dd \u00b7 \u7070 \u00b7 \u7ea2 \u00b7 \u68d5"],
    ref: "\u53cd\u67e5\u8272\u73af\uff1a6800 \u03a9 \u6709\u6548\u6570\u5b57 6/8 \u21d2 \u84dd(6)/\u7070(8)\uff1b6800/(68\u00d710)=1 \u21d2 \u4e58\u6570 100 \u21d2 \u7ea2\uff0crevTol=1\uff08\u00b11%\uff09 \u21d2 \u68d5\u3002\u9ed8\u8ba4 10 k\u03a9 \u8f93\u51fa\u4e0d\u542b\u6b64\u4e32\u3002"
  },
  {
    slug: "science/resistor-color-code",
    inputs: { revValue: "390", revTol: "1" },
    expect: ["390 \u03a9 \u6700\u63a5\u8fd1 E24 \u6807\u51c6\u503c\uff0c\u8272\u73af\uff1a\u6a59 \u00b7 \u767d \u00b7 \u68d5 \u00b7 \u68d5"],
    ref: "\u53cd\u67e5\u8272\u73af\uff1a390 \u03a9 \u6709\u6548\u6570\u5b57 3/9 \u21d2 \u6a59(3)/\u767d(9)\uff1b390/(39\u00d710)=1 \u21d2 \u4e58\u6570 10 \u21d2 \u68d5\uff0crevTol=1\uff08\u00b11%\uff09 \u21d2 \u68d5\u3002\u9ed8\u8ba4 10 k\u03a9 \u8f93\u51fa\u4e0d\u542b\u6b64\u4e32\uff1b\u6ce8\u610f 390 \u03a9 \u4e0e\u88f8\u503c 390 \u4e0d\u540c\uff08\u540e\u8005\u4e3a\u8f93\u5165\u56de\u663e\uff0c\u4e0d\u4f5c\u951a\uff09\u3002"
  },

{
    "slug": "science/calc-cycle",
    "inputs": {
      "formula": "NaCl"
    },
    "expect": [
      "58.44 g/mol"
    ],
    "ref": "NaCl 分子量 = Na 22.99 + Cl 35.45 = 58.44 g/mol（共 2 个原子）。页面输出 '58.44 g/mol'。默认态 formula=H2O → 18.02，不出现 58.44。"
  }
  ,
  {
    "slug": "science/gcd-calculator",
    "inputs": { "nums": "8,12,20" },
    "clicks": ["calculate()"],
    "expect": ["GCD = 4"],
    "ref": "独立复算：GCD(8,12)=4，GCD(4,20)=4 ⇒ 4。默认 nums=48,36,24 ⇒ 12，不出现 'GCD = 4'。"
  },
  {
    "slug": "science/gcd-calculator",
    "inputs": {},
    "clicks": ["var p=parseNums('1.5,3');document.getElementById('nums').value='DECPROBE_'+(p.error?'Y':'N')+'_'+p.error;"],
    "expect": ["DECPROBE_Y_请输入整数"],
    "ref": "SMS-94 清账：parseNums 原用 parseInt 静默截断小数（1.5→1）。现改 Number + Number.isInteger 严格解析，小数返回 error。探针直接调 parseNums('1.5,3') 断言 error；旧版返回数组无 error ⇒ DECPROBE_N，零逃生。"
  },
  {
    "slug": "science/gcd-calculator",
    "inputs": {},
    "clicks": ["var p=parseNums('9007199254740993,3');document.getElementById('nums').value='BIGPROBE_'+(p.error&&p.error.indexOf('安全整数')>=0?'Y':'N');"],
    "expect": ["BIGPROBE_Y"],
    "ref": "SMS-95 清账：parseNums 原 parseInt 把 2^53+1 截为 2^53（失真）且 factorize 穷举 √n 卡死。现拒绝 |v|>Number.MAX_SAFE_INTEGER 并提示超出安全整数范围。探针直接调 parseNums 避免旧版卡死，断言 error 含「安全整数」；旧版无 error ⇒ BIGPROBE_N，零逃生。"
  },
  {
    "slug": "science/lcm-calculator",
    "inputs": { "nums": "15,20,25" },
    "clicks": ["calculate()"],
    "expect": ["LCM = 300"],
    "ref": "独立复算：LCM(15,20)=60，LCM(60,25)=300 ⇒ 300。默认 nums=12,18,24 ⇒ 72，不出现 300。"
  },
  {
    "slug": "science/lcm-calculator",
    "inputs": {},
    "clicks": ["var p=parseNums('4.5,6');document.getElementById('nums').value='LCMDECPROBE_'+(p.error?'Y':'N')+'_'+p.error;"],
    "expect": ["LCMDECPROBE_Y_请输入整数"],
    "ref": "SMS-94 同族清账：lcm 页 parseNums 原同样用 parseInt 静默截断小数（4.5→4）。现与 gcd 页一致改严格解析。探针直接调 parseNums('4.5,6') 断言 error；旧版返回数组无 error ⇒ LCMDECPROBE_N，零逃生。"
  },
  {
    "slug": "science/vector-calculator",
    "inputs": { "dim": "3", "op": "add", "a0": "1", "a1": "2", "a2": "", "b0": "4", "b1": "5", "b2": "6" },
    "clicks": ["calculate()"],
    "expect": ["空值不等于 0"],
    "ref": "清空 A 的 z 分量后旧实现按 0 计算并输出 A+B；现须阻止计算并提示缺失，0 仍可作为合法输入。"
  },
  {
    "slug": "science/vector-calculator",
    "inputs": { "dim": "3", "op": "dot", "a0": "1", "a1": "2", "a2": "0", "b0": "3", "b1": "4", "b2": "0" },
    "clicks": ["calculate()"],
    "expect": ["A · B = 11"],
    "ref": "点积 A·B=1×3+2×4+0×0=11（dim 默认即 3D，a/b 各分量为注入值）。刻意选非默认运算 op=dot（默认 op=add）⇒ 判别器把 op 换回 add 后输出 A+B=(4,6,0)，不出现 'A · B = 11'（该页向量分量是 build() 动态生成的 id=a0/b0..，静态 HTML 无默认值，故只能靠静态 op/size 的回落来制造判别力）。"
  },
  {
    "slug": "science/vector-calculator",
    "inputs": { "dim": "3", "op": "scaleA", "scalar": "0", "a0": "1", "a1": "2", "a2": "3", "b0": "4", "b1": "5", "b2": "6" },
    "clicks": ["calculate()"],
    "expect": ["0·A = (0, 0, 0)"],
    "ref": "零标量必须原样进算：旧实现 scalar||1 把 0 改成 1，零向量被放大成 A。注入 k=0、A=(1,2,3) ⇒ 0·A=(0,0,0)。默认 scalar=2 ⇒ 2·A=(2,4,6)，不命中（scalar 是静态控件，判别器可回退）。"
  },
  {
    "slug": "science/xianxingfangchengzuqiujie-2yuan-3yuan",
    "inputs": { "a1": "2", "b1": "1", "c1": "5", "a2": "1", "b2": "-1", "c2": "1" },
    "clicks": ["calc()"],
    "expect": ["x = 2", "y = 1"],
    "ref": "解方程组 2x+y=5, x−y=1 ⇒ x=2, y=1, det(A)=2×(−1)−1×1=−3。默认 a1=1,b1=2,a2=3 ⇒ x=1,y=2，不出现 x=2/y=1。"
  },
  {
    "slug": "science/wire-gauge-converter",
    "inputs": { "awg": "20" },
    "clicks": ["calcAll()"],
    "expect": ["0.8118"],
    "ref": "AWG 20 ⇒ 线径 0.8118 mm / 31.961 mil（标准线规表）。默认 awg=24 ⇒ 0.5106 mm，不出现 0.8118。"
  },
  {
    "slug": "science/wire-gauge-converter",
    "inputs": { "awg": "20" },
    "clicks": ["calcAll()"],
    "expect": ["33.23"],
    "ref": "SMS-158 铜电阻量纲：ρ=0.0172 Ω·mm²/m，R(Ω/km)=ρ×1000/A。AWG20 截面积 0.5176 mm² ⇒ 33.23 Ω/km（旧实现少乘 1000 显示 0.03）。默认 awg=24 ⇒ 84.01 Ω/km，判别器换回默认不命中 33.23。"
  },
  {
    "slug": "science/science-flow-rate",
    "inputs": { "diam": "100", "vel": "1" },
    "clicks": ["calc()"],
    "expect": ["7.85 L/s"],
    "ref": "圆管 Q=A·v，A=π·(0.05m)²=0.007854 m²，v=1 ⇒ 0.007854 m³/s=7.854 L/s。默认 diam=50,vel=2 ⇒ 3.93 L/s，不出现 7.85。"
  },
  {
    "slug": "science/science-flow-rate",
    "inputs": {},
    "clicks": ["function __d(id){var e=document.getElementById(id);return e?e.innerHTML:'';}document.getElementById('diam').value='50';document.getElementById('vel').value='2';calc();var has1=__d('resultDetail').length>0;document.getElementById('diam').value='';calc();var has2=__d('resultDetail').length>0;var ra=document.getElementById('resArea').textContent;document.getElementById('diam').value='CLRPROBE_'+(has1&&!has2&&ra==='--'?'Y':'N')+'_'+has1+has2+'_'+ra;"],
    "expect": ["CLRPROBE_Y_truefalse_--"],
    "ref": "SMS-145 清账：圆形分支原 `if(!diam||!v)return` 在清空输入后保留上一次结果。现新增 clearFlowResult() 清空 flowUnits/resultDetail/resArea/resVel/resRe/resMass/pipeDiagram 并置 lastResult=null；三模式非法输入均调用。探针先算合法值得明细，再清空 diam 重算 ⇒ 明细消失、resArea=--；旧版保留旧明细 ⇒ N，零逃生。探针串写 diam 的 value（harness 采集纯文本）。"
  },
  {
    "slug": "science/science-flow-rate",
    "inputs": {},
    "clicks": ["document.getElementById('diam').value='2';var sel=document.getElementById('diamUnit');sel.value='25.4';document.getElementById('vel').value='1';calc();var d=document.getElementById('resultDetail').innerHTML;document.getElementById('diam').value='UNITPROBE_'+(d.indexOf('2 inch')>=0&&d.indexOf('2 mm =')<0?'Y':'N');"],
    "expect": ["UNITPROBE_Y"],
    "ref": "SMS-144 清账：明细原把已折算的内径左侧值恒标 mm，选 inch 时显示「2 mm = …」自相矛盾。现从 diamUnit 的选中 option 文本取真实单位标签。探针注入 diam=2、单位 inch、vel=1，断言明细含「2 inch」且不含写死的「2 mm =」；旧版写死 mm ⇒ N，零逃生。"
  },
  {
    "slug": "science/science-flow-rate",
    "inputs": {},
    "clicks": ["document.getElementById('diam').value='77.7';document.getElementById('vel').value='2';calc();saveHistory();document.getElementById('diam').value='11.1';loadHistory(0);document.getElementById('diam').value='HISPROBE_'+(document.getElementById('diam').value==='77.7'?'Y':'N')+'_'+document.getElementById('diam').value;"],
    "expect": ["HISPROBE_Y_77.7"],
    "ref": "SMS-143 清账：原 saveHistory 只存派生量、loadHistory 切模式后用当前输入重算（假恢复）。现 saveHistory 连同 14 个输入/单位字段一并存入 inputs，loadHistory 逐项回填后再 calc。探针存 diam=77.7 后改为 11.1，loadHistory(0) 后断言 diam 回填为 77.7；旧版保持 11.1 ⇒ N，零逃生。"
  },
  {
    "slug": "science/matrix-calculator",
    "inputs": { "size": "2", "op": "transpose", "a0": "1", "a1": "", "a2": "3", "a3": "4" },
    "clicks": ["calculate()"],
    "expect": ["空值不等于 0"],
    "ref": "清空矩阵单元后旧实现按 0 转置并输出结果；现须阻止计算并提示缺失。"
  },
  {
    "slug": "science/matrix-calculator",
    "inputs": { "size": "2", "op": "mul", "a0": "1", "a1": "2", "a2": "3", "a3": "4", "b0": "5", "b1": "6", "b2": "7", "b3": "8" },
    "clicks": ["calculate()"],
    "expect": ["19 22 43 50"],
    "ref": "2×2 矩阵乘法 A=[[1,2],[3,4]]、B=[[5,6],[7,8]] ⇒ C=[[1·5+2·7,1·6+2·8],[3·5+4·7,3·6+4·8]]=[[19,22],[43,50]]，逐格输出 '19 22 43 50'。刻意选非默认 size=2×2 与 op=mul（默认 3×3、add）⇒ 判别器换回默认后输出 A+B，不出现该串（a0..b3 为 buildMatrices() 动态生成的 id，静态 HTML 无默认值）。"
  },
  {
    "slug": "science/matrix-calculator",
    "inputs": { "size": "2", "op": "power", "scalar": "0", "a0": "2", "a1": "3", "a2": "4", "a3": "5" },
    "clicks": ["calculate()"],
    "expect": ["1 0 0 1"],
    "ref": "A⁰ 应为单位矩阵：旧实现 parseInt(raw)||1 把指数 0 改成 1 ⇒ 输出 A 本身（2 3 4 5）。注入 A=[[2,3],[4,5]]、power=0 ⇒ I=[[1,0],[0,1]]，逐格 '1 0 0 1'。默认 size 3×3/op add/scalar 2 ⇒ 不命中（size/op/scalar 均为静态控件，判别器可回退）。"
  },
  {
    "slug": "science/matrix-calculator",
    "inputs": { "size": "2", "op": "scale", "scalar": "0", "a0": "1", "a1": "2", "a2": "3", "a3": "4" },
    "clicks": ["calculate()"],
    "expect": ["k·A = 0·A"],
    "ref": "零标量必须原样进算：旧实现 parseFloat(raw)||1 把 k=0 改成 1，结果标题会写成 k·A = 1·A。注入 A=[[1,2],[3,4]]、k=0 ⇒ 标题 '结果 k·A = 0·A：' + 零矩阵。判别器把 op 换回默认 add 后标题变成 '结果 C = A + B：'，不命中（只锚标题，避免依赖零矩阵串）。"
  },
  {
    "slug": "science/probability-calculator",
    "inputs": { "mu": "0", "sigma": "2", "x1": "0", "x2": "2", "calcType": "between" },
    "clicks": ["calculate()"],
    "expect": ["34.134475%"],
    "ref": "X~N(0,4)，P(0≤X≤2)=Φ(1)−Φ(0)=0.841344746−0.5=0.341344746=34.1344746%，按 percent 6 位小数四舍五入显示 34.134475%。默认 μ0,σ1,x1=1,x2=2 ⇒ 13.59%，不出现该串。"
  },
  {
    "slug": "science/pcb-trace-width",
    "inputs": { "current": "5", "temp": "20", "thickness": "2" },
    "clicks": ["calc()"],
    "expect": ["0.9079", "35.74"],
    "ref": "IPC-2221 外层：Area=(I/(k·ΔT^b))^(1/c)，k=0.048,b=0.44,c=0.725 ⇒ Area≈98.5 mils²；width=Area/(2oz×1.378)=35.74 mils=0.9079 mm。默认 I=2,ΔT=10,1oz ⇒ 0.7814/30.76，不出现 0.9079。"
  },
  {
    "slug": "science/equation-balancer",
    "inputs": { "eqInput": "Fe + O2 = Fe2O3" },
    "clicks": ["balance()"],
    "expect": ["4 Fe + 3 O 2 → 2 Fe 2 O 3"],
    "ref": "配平 Fe+O2→Fe2O3 ⇒ 4Fe+3O2→2Fe2O3（Fe 4=4, O 6=6 守恒）。默认 eqInput=H2+O2=H2O ⇒ 2H2+O2→2H2O，不出现该串。"
  },
  {
    "slug": "tax/rfc-validator",
    "inputs": { "input": "ABCD900101ABC" },
    "clicks": ["validate()"],
    "expect": ["1990-01-01", "校验位： C（期望 4）"],
    "ref": "RFC ABCD900101ABC：首字母 ABCD，日期段 900101 ⇒ 页面按补零格式输出 1990-01-01；尾部 ABC 中 C 为校验位，按 RFC_BASE 权重算法期望 4 ⇒ 该串校验位不符。旧 expect 写未补零的 1990-1-1 且与校验位结论脱钩，已改为双锚。默认输入为空 ⇒ 两锚均不命中。"
  },
  {
    "slug": "text/text-extract-phones",
    "inputs": { "input": "13800138000 01012345678" },
    "checkIds": ["mobile", "landline", "dedup"],
    "clicks": ["extract()"],
    "expect": ["13800138000", "01012345678"],
    "ref": "手机号 1[3-9]\\d{9} 命中 13800138000；座机 0\\d{2,3}\\d{7,8} 命中 01012345678；去重后 2 个。默认输入为空 ⇒ '未找到匹配的电话号码'，不出现这两个号码。"
  },
  {
    "slug": "science/tide-height-estimator",
    "inputs": { "inputDate": "2024-03-20", "inputLat": "30", "coastType": "open", "moonPhaseMode": "manual", "moonPhase": "0" },
    "clicks": ["calc()"],
    "expect": ["太阳引潮力贡献： 0%"],
    "ref": "SMS-152 相位：春分(2024-03-20 doy≈80)太阳赤纬为 0、引潮贡献最小 ⇒ solar=0.46·|sin((80−80)/365.25·2π)|=0 ⇒ 0%。旧 cos 公式此日取峰值 46%（峰谷颠倒）。默认态快照日期 2024-06-15 近夏至 ⇒ 46%，不命中 0%，判别有效。"
  },
  {
    "slug": "science/tide-height-estimator",
    "inputs": { "inputDate": "2024-06-01", "inputLat": "30", "coastType": "open", "moonPhaseMode": "manual", "moonPhase": "0" },
    "clicks": ["calc()"],
    "expect": ["潮差： 1.08 米"],
    "ref": "SMS-152 相位修正后：手动月龄=0(新月/大潮 tideFactor=1)，2024-06-01 doy153 近夏至 ⇒ solar=0.46·|sin((153−80)/365.25·2π)|=0.437；纬度 30° 修正 0.906，开阔海岸 1.0x，high=0.52·(1+0.437)·0.906=0.677，潮差=1.6×high=1.08 m。旧 cos 公式此日 solar 很小 ⇒ 0.86 m。默认 moonPhaseMode=auto ⇒ 不出现 1.08。"
  },
  {
    "slug": "it/phone-qr",
    "inputs": { "phone": "13912345678" },
    "expect": ["tel:13912345678"],
    "ref": "注入手机号 13912345678（默认 +8613800138000）。页面将手机号渲染为 tel: 文本链接 ⇒ 输出含 'tel:13912345678'，默认态 'tel:+8613800138000' 完全不含 ⇒ 0 逃生。注：renderQR 在桩下报 'leng' 错误（QR 图像生成依赖 canvas/库），但 tel: 文本链接为纯字符串、不受 canvas 影响，确定性可用。纯前端无随机。"
  },
  {
    "slug": "science/barcode-pharmacode",
    "inputs": {
      "data": "42"
    },
    "expect": [
      "，请刷新页面重试。\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"42\"}，输出区含「，请刷新页面重试。\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/astro-geo-calculator",
    "inputs": {
      "sun-lat": "42",
      "sun-lon": "42",
      "sun-date": "abc123测试",
      "eq-mag": "42",
      "hz-height": "42",
      "wind-speed": "42",
      "hum-dry": "42",
      "hum-wet": "42",
      "prs-alt": "42",
      "wind-unit": "kmh"
    },
    "expect": [
      "abc123测试\n42\n42\n42\n42\n42\n42\n42\n42\nkmh\n⚠ 计算结果含无效值，请检查输入是否为有效正数。\n42.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"sun-lat\":\"42\",\"sun-lon\":\"42\",\"sun-date\":\"abc123测试\",\"eq-mag\":\"42\",\"hz-height\":\"42\",\"wind-speed\":\"42\",\"hum-dry\":\"42\",\"hum-wet\":\"42\",\"prs-alt\":\"42\",\"wind-unit\":\"kmh\"}，输出区含「abc123测试\n42\n42\n42\n42\n42\n42\n42\n42\nkmh\n⚠ 计…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/anova-calculator",
    "inputs": {
      "groups": "1\n2\n3"
    },
    "expect": [
      "每组至少需要 2 个观测值（否则组内自由度 N−k ≤ 0，F 无定义）\n1 2 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"groups\":\"1\\n2\\n3\"}，每组仅 1 个观测 ⇒ 输出区提示「每组至少需要 2 个观测值（否则组内自由度 N−k ≤ 0，F 无定义）」；默认态（每组≥2）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/calc-1",
    "inputs": {
      "height": "42",
      "v0": "42",
      "gravity": "42",
      "airResist": "1"
    },
    "expect": [
      "42\n42\n42\n落地时间 t： 0.7321"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"height\":\"42\",\"v0\":\"42\",\"gravity\":\"42\",\"airResist\":\"1\"}，输出区含「42\n42\n42\n落地时间 t： 0.7321」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/astronomy-toolkit",
    "inputs": {
      "moonDate": "abc123测试",
      "mag1": "42",
      "mag2": "42",
      "meteorDiameter": "42",
      "meteorSpeed": "42",
      "meteorDensity": "42",
      "meteorAngle": "42",
      "groundDensity": "42",
      "latInput": "42",
      "lonInput": "42",
      "utmZone": "42",
      "utmEasting": "42",
      "utmNorthing": "42",
      "polarLat": "42",
      "utmHemisphere": "S",
      "obsMoonPhase": "crescent",
      "obsBortle": "2"
    },
    "expect": ["果仅供科普参考。", "该区号与东移/北移值不匹配，无法反算为有效经纬度"],
    "ref": "自动补强（B类零用例）·SMS-73 清账：注入非默认输入含 utmZone=42/utmEasting=42/utmNorthing=42/utmHemisphere=S，旧版反向溢出为荒谬值「纬度：2779796544」；现结果域守卫拒绝并提示「该区号与东移/北移值不匹配」。默认态（合法 E/N）不含该提示 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/battery-life-calculator",
    "inputs": {
      "cap": "42",
      "curr": "42",
      "volt": "42",
      "capUnit": "1000",
      "currUnit": "1000",
      "eff": "0.95"
    },
    "expect": [
      "100% 0 秒 57 分钟 90% 6 分钟 51 分钟 75% 14 分钟 43 分钟 50% 29 分钟 29 分钟 25% 43 分钟 14 分钟 10% 51 分钟 6 分钟 5% 54 分钟 3 分钟"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"cap\":\"42\",\"curr\":\"42\",\"volt\":\"42\",\"capUnit\":\"1000\",\"currUnit\":\"1000\",\"eff\":\"0.95\"}，输出区含「100% 0 秒 57 分钟 90% 6 分钟 51 分钟 75% 14 分钟 …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/calc-2",
    "inputs": {
      "gasR": "42",
      "P": "42",
      "V": "42",
      "n": "42",
      "T": "42",
      "solveFor": "V"
    },
    "expect": [
      "V\n42\n42\n42\n42\n42\n求解目标： 体积 V 计算结果： 1.7640e+3 m³ 常规表示： 1764.0000 m³ 已知：压强 P = 42 Pa"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"gasR\":\"42\",\"P\":\"42\",\"V\":\"42\",\"n\":\"42\",\"T\":\"42\",\"solveFor\":\"V\"}，输出区含「V\n42\n42\n42\n42\n42\n求解目标： 体积 V 计算结果： 1.7640…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/calc-4",
    "inputs": {
      "density": "42",
      "mass": "42",
      "volume": "42",
      "preset": "1000"
    },
    "expect": [
      "1000\n42\n42\n请至少留空一个未知量以便计算。\n1000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"density\":\"42\",\"mass\":\"42\",\"volume\":\"42\",\"preset\":\"1000\"}，输出区含「1000\n42\n42\n请至少留空一个未知量以便计算。\n1000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/calc-5",
    "inputs": {
      "speed": "42",
      "distance": "42",
      "time": "42",
      "unit": "kmh"
    },
    "expect": [
      "42\n42\n42\nkmh\n已输入全部三个量，校验一致性： 按 v × t 计算距离应为 1764.0000 m 您输入的距离为 42.0000 m 偏差： 1722.0000 m"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"speed\":\"42\",\"distance\":\"42\",\"time\":\"42\",\"unit\":\"kmh\"}，输出区含「42\n42\n42\nkmh\n已输入全部三个量，校验一致性： 按 v × t 计算距…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/calc-stats",
    "inputs": {
      "data": "1\n2\n3",
      "typ": "pop"
    },
    "expect": [
      "00 IQR 1.0000 方差（总体） 0.6667 标准差（总体） 0.8165"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"1\\n2\\n3\",\"typ\":\"pop\"}，输出区含「00 IQR 1.0000 方差（总体） 0.6667 标准差（总体） 0.81…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/calc-distance",
    "inputs": {
      "lat1": "42",
      "lon1": "42",
      "lat2": "42",
      "lon2": "42"
    },
    "expect": [
      "—（两点重合） 初始方位角 重合 方位 42.00000 中点纬度 42.00000 中点经度 0.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lat1\":\"42\",\"lon1\":\"42\",\"lat2\":\"42\",\"lon2\":\"42\"}，输出区含「0° 初始方位角 北 方位（北向） 42.00000 中点纬度 42.00000…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/centripetal-force",
    "inputs": {
      "m": "42",
      "v": "42",
      "r": "42"
    },
    "expect": [
      " = mv²/r 179.877"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"v\":\"42\",\"r\":\"42\"}，输出区含「 = mv²/r 179.877」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/combination-calculator",
    "inputs": {
      "n": "42",
      "r": "42"
    },
    "expect": [
      "证： 对称性：C(42,42) = C(42,0) = 1 关系：C(42,42) = P(42,42) / 42! 含义： 从 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"r\":\"42\"}，输出区含「证： 对称性：C(42,42) = C(42,0) = 1 关系：C(42,42…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/chemistry-calculator",
    "inputs": {
      "formula": "abc123测试",
      "gasP": "42",
      "gasV": "42",
      "gasN": "42",
      "gasT": "42",
      "concMass": "42",
      "concMolar": "42",
      "concVol": "42",
      "concC1": "42",
      "concV1": "42",
      "concC2": "42",
      "concV2": "42",
      "concSolute": "42",
      "concSolution": "42",
      "phValue": "42",
      "concType": "mass_conc",
      "phType": "ph_to_h",
      "gasFind": "V"
    },
    "expect": [
      "e2(SO4)3\nabc123测试\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\n42\nmass_conc\nph_to_h\nV"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"formula\":\"abc123测试\",\"gasP\":\"42\",\"gasV\":\"42\",\"gasN\":\"42\",\"gasT\":\"42\",\"concMass\":\"42\",\"concMolar\":\"42\",\"concVol\":\"42\",\"concC1\":\"42\",\"concV1\":\"42\",\"concC2\":\"42\",\"concV2\":\"42\",\"concSolute\":\"42\",\"concSolution\":\"42\",\"phValue\":\"42\",\"concType\":\"mass_conc\",\"phType\":\"ph_to_h\",\"gasFind\":\"V\"}，输出区含「e2(SO4)3\nabc123测试\n42\n42\n42\n42\n42\n42\n42\n4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/chi-square-calculator",
    "inputs": {
      "exp": "abc123测试",
      "chiIn": "42",
      "dfIn": "42",
      "obs": "1\n2\n3"
    },
    "expect": [
      "期望频数：第 1 项「abc123测试」不是有效数值\n1 2 3\nabc123测试\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"exp\":\"abc123测试\",\"chiIn\":\"42\",\"dfIn\":\"42\",\"obs\":\"1\\n2\\n3\"}，期望频数含非法项 ⇒ 输出区提示「期望频数：第 1 项「abc123测试」不是有效数值」；默认态（期望频数合法）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/convert-power",
    "inputs": {
      "val": "42",
      "from": "kgf",
      "to": "kgf"
    },
    "expect": [
      "42\nkgf\nkgf\n42 42 kgf = 42 kgf"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"42\",\"from\":\"kgf\",\"to\":\"kgf\"}，输出区含「42\nkgf\nkgf\n42 42 kgf = 42 kgf」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/correlation-calculator",
    "inputs": {
      "xData": "1\n2\n3",
      "yData": "1\n2\n3"
    },
    "expect": [
      "y−ȳ) 1 1 1 -1 -1 1 2 2 2 0 0 0 3 3 3 1 1 1 合计 2 2 2"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"xData\":\"1\\n2\\n3\",\"yData\":\"1\\n2\\n3\"}，输出区含「y−ȳ) 1 1 1 -1 -1 1 2 2 2 0 0 0 3 3 3 1 1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/coulomb-force",
    "inputs": {
      "q1": "42",
      "q2": "42",
      "r": "42"
    },
    "expect": [
      "42\n42\n42\n0.0090"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"q1\":\"42\",\"q2\":\"42\",\"r\":\"42\"}，输出区含「42\n42\n42\n0.0090」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/cycle",
    "inputs": {
      "search": "abc123测试"
    },
    "expect": [
      "系 锕系 未知性质\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"search\":\"abc123测试\"}，输出区含「系 锕系 未知性质\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/density-physics",
    "inputs": {
      "m": "42",
      "V": "42"
    },
    "expect": [
      "42\n42\n1.000 kg/m³"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"V\":\"42\"}，输出区含「42\n42\n1.000 kg/m³」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/electric-field-point",
    "inputs": {
      "q": "42",
      "r": "42"
    },
    "expect": [
      "电势 V (V) 3.7750e+5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"q\":\"42\",\"r\":\"42\"}，输出区含「电势 V (V) 3.7750e+5」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/doppler-effect",
    "inputs": {
      "f": "42",
      "v": "42",
      "vo": "42",
      "vs": "42"
    },
    "expect": [
      "波源速度不能达到或超过波速"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"f\":\"42\",\"v\":\"42\",\"vo\":\"42\",\"vs\":\"42\"}，输出区含「42\n42\n42\n42\n—」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/exp-calculator",
    "inputs": {
      "x": "42"
    },
    "expect": [
      "42\nx = 42 e^42 = 1.739275e+18 eˣ 1.739275e+18 e^(−x) 5.749522e-19 10ˣ 1.000000e+42 2ˣ 4,398,046,511,104"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x\":\"42\"}，输出区含「42\nx = 42 e^42 = 1.739275e+18 …」。原 expect 里的「e^(−x) 0」是旧 fmt 把 |x|<1e-12 吞成 0 的缺陷产物，现小值走科学计数法 ⇒ e^(−42) = 5.749522e-19；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/effect-size-calculator",
    "inputs": {
      "m1": "42",
      "mu0": "42",
      "sd1": "42",
      "m1b": "42",
      "sd1b": "42",
      "n1b": "42",
      "m2b": "42",
      "sd2b": "42",
      "n2b": "42"
    },
    "expect": [
      "n's d = 0 42 M 42 μ₀ 42 SD 0 d 50.00"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m1\":\"42\",\"mu0\":\"42\",\"sd1\":\"42\",\"m1b\":\"42\",\"sd1b\":\"42\",\"n1b\":\"42\",\"m2b\":\"42\",\"sd2b\":\"42\",\"n2b\":\"42\"}，输出区含「n's d = 0 42 M 42 μ₀ 42 SD 0 d 50.00」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/fraction-calculator",
    "inputs": {
      "n1": "42",
      "d1": "42",
      "n2": "42",
      "d2": "42",
      "cvN": "42",
      "cvD": "42",
      "cvOut": "abc123测试",
      "cvDec": "42",
      "cvFracOut": "abc123测试",
      "op": "-"
    },
    "expect": [
      "GCD(0, 1764) = 1764，0/1764 = 0/1"
    ],
    "ref": "自动补强（B类零用例）：注入 42/42 − 42/42，实算 0/1764 约分为 0/1，锚「GCD(0, 1764) = 1764，0/1764 = 0/1」这一只有实算才产出的串；默认态 1/2+1/3=5/6 不含 ⇒ 强判别、零逃生。（原 expect 依赖「输入回显 + 步骤」的 DOM 拼接顺序，属脆弱锚点，已改为纯计算结果锚）"
  },
  {
    "slug": "science/gravitational-potential",
    "inputs": {
      "m": "42",
      "g": "42",
      "h": "42"
    },
    "expect": [
      "42\n42\n42\n74088.0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"g\":\"42\",\"h\":\"42\"}，输出区含「42\n42\n42\n74088.0」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/geo-distance-calculator",
    "inputs": {
      "lat1": "42",
      "lon1": "42",
      "lat2": "42",
      "lon2": "42"
    },
    "expect": [
      "42\n42\n42\n42\n0.00\n0.00\n0.00\n—\n两点重合：方位无唯一解"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"lat1\":\"42\",\"lon1\":\"42\",\"lat2\":\"42\",\"lon2\":\"42\"}，输出区含「42\n42\n42\n42\n0.00\n0.00\n0.00\n—\n两点重合：方位无唯一解」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/heat-transfer-calculator",
    "inputs": {
      "condK": "42",
      "condA": "42",
      "condL": "42",
      "condT1": "42",
      "condT2": "42",
      "specM": "42",
      "specC": "42",
      "specT1": "42",
      "specT2": "42",
      "convH": "42",
      "convA": "42",
      "convTw": "42",
      "convTf": "42",
      "condMat": "237",
      "specMUnit": "0.001",
      "specMat": "450",
      "convType": "25"
    },
    "expect": [
      "功率 (kW)\n千卡/秒\n0.00 μW\n0.00 W\n0.0°C\n0.0000 kcal/s"
    ],
    "ref": "自动补强（B类零用例）·第1013批同步：注入非默认输入使 ΔT=0，输出区含导热模式动态标签「功率 (kW)/千卡/秒」与 0.00 μW、0.00 W、0.0°C、0.0000 kcal/s 成套值；默认态为 3007.50 W，不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/kinetic-energy",
    "inputs": {
      "m": "42",
      "v": "42"
    },
    "expect": [
      " (m²/s²) 37.044"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"v\":\"42\"}，输出区含「 (m²/s²) 37.044」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/hookes-law",
    "inputs": {
      "k": "42",
      "x": "42"
    },
    "expect": [
      " F = k·x 37044"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"k\":\"42\",\"x\":\"42\"}，输出区含「 F = k·x 37044」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/latlon-utm-converter",
    "inputs": {
      "lat": "42",
      "lon": "42",
      "utmZone": "42",
      "utmEasting": "42",
      "utmNorthing": "42",
      "utmHemisphere": "S"
    },
    "expect": ["该带号与东移/北移值不匹配，无法反算为有效经纬度"],
    "ref": "自动补强（B类零用例）·SMS-101 清账：注入非默认输入{\"lat\":\"42\",\"lon\":\"42\",\"utmZone\":\"42\",\"utmEasting\":\"42\",\"utmNorthing\":\"42\",\"utmHemisphere\":\"S\"}，E=42/N=42 落在物理范围内但与带号 42 不匹配，旧版反算溢出为荒谬值「经度 -277979654269°29'42.64」；现结果域守卫拒绝并提示「该带号与东移/北移值不匹配，无法反算为有效经纬度」。默认态（合法 E/N）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/latlon-utm-converter",
    "inputs": { lat: "0", lon: "180" },
    clicks: ["convertLL2UTM()"],
    expect: ["60 UTM带号", "中央经线： 177.0°"],
    ref: "SMS-101 清账（经度边界）：经度 +180° 是 UTM 东半球的合法边界，应归入第 60 带（中央经线 = 6×60−180+3 = 177.0°）。旧版 ⌊(180+180)/6⌋+1 = 61 越出合法的 1~60 带号，中央经线算成 183.0°；现钳制到 60。两条锚旧版均不成立（旧版为 61/183.0°）⇒ 零逃生。",
  },
  {
    "slug": "science/latlon-utm-converter",
    "inputs": { utmZone: "50", utmHemisphere: "N", utmEasting: "1500000", utmNorthing: "5000000" },
    clicks: ["convertUTM2LL();document.getElementById('utmEasting').value='UTMRNG_'+(String(document.getElementById('result-utm2ll').textContent||document.getElementById('result-utm2ll').innerHTML).indexOf('超出有效范围')>=0?'OK':'BAD');"],
    expect: ["UTMRNG_OK"],
    ref: "SMS-101 清账（E 范围守卫）：东移值 1500000 m 超出 UTM 假东移 500000 的物理上限 1000000，旧版照常反算输出荒谬经纬度；现直接提示「UTM 坐标超出有效范围」。探针断言结果容器出现该提示，旧版 ⇒ UTMRNG_BAD，零逃生。",
  },
  {
    "slug": "science/led-resistor-calculator",
    "inputs": {
      "vs": "42",
      "if": "42",
      "vfCustom": "42",
      "count": "42",
      "vsUnit": "1000",
      "ifUnit": "1",
      "vf": "2.0",
      "tolerance": "0.05"
    },
    "expect": [
      "ED (串联)\n🟠\n2.0\n42000\n998.0 Ω\n1.00 kΩ\n1760472.00 W\n5W以上\n电路配置： 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"vs\":\"42\",\"if\":\"42\",\"vfCustom\":\"42\",\"count\":\"42\",\"vsUnit\":\"1000\",\"ifUnit\":\"1\",\"vf\":\"2.0\",\"tolerance\":\"0.05\"}，输出区含「ED (串联)\n🟠\n2.0\n42000\n998.0 Ω\n1.00 kΩ\n176…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/mechanical-power",
    "inputs": {
      "F": "42",
      "v": "42"
    },
    "expect": [
      " 功率 (kW) 2.365563"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"F\":\"42\",\"v\":\"42\"}，输出区含「 功率 (kW) 2.365563」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/log-calculator",
    "inputs": {
      "x": "42",
      "base": "42"
    },
    "expect": [
      "(n) = ln(42) / ln(42) = 3.738 / 3.738 = 1 验证：42^1 = 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x\":\"42\",\"base\":\"42\"}，输出区含「(n) = ln(42) / ln(42) = 3.738 / 3.738 = …」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/mean-calculator",
    "inputs": {
      "data": "1\n2\n3"
    },
    "expect": [
      "= 3 / (1/1 + 1/2 + 1/3) = 3 / 1.833 = 1.636"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"1\\n2\\n3\"}，输出区含「= 3 / (1/1 + 1/2 + 1/3) = 3 / 1.833 = 1.…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/median-calculator",
    "inputs": {
      "data": "1\n2\n3"
    },
    "expect": [
      "1 2 3\n原始数据（n=3）： 1, 2, 3"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"1\\n2\\n3\"}，输出区含「1 2 3\n原始数据（n=3）： 1, 2, 3」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/meteor-crater-estimator",
    "inputs": {
      "meteorDiameter": "42",
      "meteorVelocity": "42",
      "impactAngle": "42",
      "targetDensity": "42",
      "meteorDensity": "7800",
      "targetType": "crystalline"
    },
    "expect": [
      " 撞击点 撞击坑 4.68 km 火球区 5.61 km 烧伤区 23.91 km 严重破坏 10.78 km 中度破坏 84.72"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"meteorDiameter\":\"42\",\"meteorVelocity\":\"42\",\"impactAngle\":\"42\",\"targetDensity\":\"42\",\"meteorDensity\":\"7800\",\"targetType\":\"crystalline\"}，输出区含「 撞击点 撞击坑 4.68 km 火球区 5.61 km 烧伤区 23.91 k…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/mode-calculator",
    "inputs": {
      "data": "1\n2\n3"
    },
    "expect": [
      "数 频率 1 1 33.33% 2 1 33.33% 3 1 33.33"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"1\\n2\\n3\"}，输出区含「数 频率 1 1 33.33% 2 1 33.33% 3 1 33.33」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/nato-phonetic",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      " Charlie 1 One 2 Two 3 Three 测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「 Charlie 1 One 2 Two 3 Three 测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/newtons-second",
    "inputs": {
      "m": "42",
      "a": "42"
    },
    "expect": [
      "(km/h/s) 179.8779"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"a\":\"42\"}，输出区含「(km/h/s) 179.8779」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/nth-root-calculator",
    "inputs": {
      "x": "42",
      "n": "42"
    },
    "expect": [
      " = e^((1/42)·ln(42)) ln(42) = 3.738 (1/42) × ln(42) = 0.089 e^0.089 = 1.093 验证：(1.093)^42 = 42 ≈ 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x\":\"42\",\"n\":\"42\"}，输出区含「 = e^((1/42)·ln(42)) ln(42) = 3.738 (1/4…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/ohms-law-calculator",
    "inputs": {
      "v": "42",
      "i": "42",
      "r": "42"
    },
    "expect": [
      "42\n1\n42\nI\n安培\n42.00 W\n42.000 Wh\n23.81 mS\n1.00 C\n电压 V： 4"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"i\":\"42\",\"r\":\"42\"}，输出区含「42\n1\n42\nI\n安培\n42.00 W\n42.000 Wh\n23.81 m…」；第 1008 批 SMS-123 同步修正旧错误单位「Wh/h」→「Wh」（标签为 1 小时能耗=E=P×1h）。默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/p-value-calculator",
    "inputs": {
      "z0": "42",
      "t1": "42",
      "df1": "42",
      "chi2": "42",
      "df2": "42",
      "alpha": "42",
      "tail0": "left",
      "tail1": "left"
    },
    "expect": [
      "α must be within (0, 0.5].\n42\n42\n42\n42\n42\n42\nleft\nleft"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"z0\":\"42\",\"t1\":\"42\",\"df1\":\"42\",\"chi2\":\"42\",\"df2\":\"42\",\"alpha\":\"42\",\"tail0\":\"left\",\"tail1\":\"left\"}，输出区含「42\n42\n42\n42\n42\n42\nleft\nleft\nα must be wi…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/pendulum-period",
    "inputs": {
      "L": "42",
      "g": "42"
    },
    "expect": [
      "率 f (Hz) 6283.185 周期 (ms) 1.0000"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"L\":\"42\",\"g\":\"42\"}，输出区含「率 f (Hz) 6283.185 周期 (ms) 1.0000」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/percentile-calculator",
    "inputs": {
      "percentiles": "90",
      "data": "1\n2\n3"
    },
    "expect": [
      "P 90 = 2.8"
    ],
    "ref": "自动补强（B类零用例）：注入 data=1,2,3 / P90，pos=(3−1)×0.9=1.8 ⇒ 2×(2−1.8)+3×(1.8−1)=2.8，锚「P90 = 2.8」（页面 fmt 输出 2.8）。默认数据非 1,2,3 ⇒ 不命中。注：原用例注入非法百分位「abc123测试」并被旧实现静默过滤，页面改为点名报错后该弱锚失效，故改为实算派生值。"
  },
  {
    "slug": "science/permutation-calculator",
    "inputs": {
      "n": "42",
      "r": "42"
    },
    "expect": [
      ". × 1] = 1,405,006,117,752,879,898,543,142,606,244,511,569,936,384,000,000,000 含义： 从 42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"r\":\"42\"}，输出区含「. × 1] = 1,405,006,117,752,879,898,543,1…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "life/phone-lookup",
    "inputs": {
      "input": "abc123测试"
    },
    "expect": [
      "abc123测试\n❌ 仅允许数字及 +、空格、连字符"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"input\":\"abc123测试\"}，输出区含「abc123测试\n❌ 仅允许数字及 +、空格、连字符」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/ph-calculator",
    "inputs": {
      "H": "42",
      "ph": "42",
      "ca": "42",
      "cb": "42",
      "type": "6.35"
    },
    "expect": [
      " 报告 pH = -1.62 强酸 [H⁺] 4.200e+1"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"H\":\"42\",\"ph\":\"42\",\"ca\":\"42\",\"cb\":\"42\",\"type\":\"6.35\"}，输出区含「 报告 pH = -1.62 强酸 [H⁺] 4.200e+1」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/polar-day-night",
    "inputs": {
      "inputLat": "42",
      "hemisphere": "S"
    },
    "expect": [
      "42\nS\n纬度范围应为 60° ~ 90°，低于60°无极昼极夜现象"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"inputLat\":\"42\",\"hemisphere\":\"S\"}，输出区含「42\nS\n纬度范围应为 60° ~ 90°，低于60°无极昼极夜现象」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/physics-calculator",
    "inputs": {
      "var_${key}": "42"
    },
    "expect": [
      "W/t = Fv\n42\n已知"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"var_${key}\":\"42\"}，输出区含「W/t = Fv\n42\n已知」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/pi-digits",
    "inputs": {
      "n": "42",
      "pattern": "abc123测试"
    },
    "expect": [
      "841971 69\n42\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"n\":\"42\",\"pattern\":\"abc123测试\"}，输出区含「841971 69\n42\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/power-calculator",
    "inputs": {
      "base": "42",
      "exp": "42"
    },
    "expect": [
      "42\n42\n42 ^ 42 42^42 = 1.5013093755e+68"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"base\":\"42\",\"exp\":\"42\"}，输出区含「42\n42\n42 ^ 42 42^42 = 1.5013093755e+68」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/projectile-range",
    "inputs": {
      "v": "42",
      "theta": "42",
      "g": "42"
    },
    "expect": [
      "in(2θ)/g 9.40"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"v\":\"42\",\"theta\":\"42\",\"g\":\"42\"}，输出区含「in(2θ)/g 9.40」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "finance/provident-fund",
    "inputs": {
      "salary": "42",
      "selfPct": "42",
      "empPct": "42",
      "months": "42",
      "loanRate": "3.1",
      "loanYears": "30",
      "multi": "42",
      "cityCap": "42"
    },
    "expect": [
      "月供： 265.75 元 总还款： 95,669.66 元"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"salary\":\"42\",\"selfPct\":\"42\",\"empPct\":\"42\",\"months\":\"42\",\"loanRate\":\"3.1\",\"loanYears\":\"30\",\"multi\":\"42\",\"cityCap\":\"42\"}，输出区含「月供： 265.75 元 总还款： 95,669.66 元」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/quadratic-equation",
    "inputs": {
      "a": "42",
      "b": "42",
      "c": "42"
    },
    "expect": [
      "42\n42\n42\n两个共轭复数根\nΔ = -5292\nx₁ -0.5 + 0.8660254038i 精确：x = (-42 + 42√3i) / 84 x₂ -0.5 − 0.8660254038i 精确：x = (-42 - 42√3i"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"a\":\"42\",\"b\":\"42\",\"c\":\"42\"}，输出区含「42\n42\n42\n两个共轭复数根\nΔ = -5292\nx₁ -0.5 + 0.8…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/quartile-calculator",
    "inputs": {
      "data": "1\n2\n3"
    },
    "expect": [
      "序： 1, 2, 3 Q1 = 1.5，Q2 = 2，Q3 = 2."
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"1\\n2\\n3\"}，输出区含「序： 1, 2, 3 Q1 = 1.5，Q2 = 2，Q3 = 2.」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/rc-time-constant",
    "inputs": {
      "resistance": "42",
      "capacitance": "42",
      "voltage": "42",
      "rUnit": "1000",
      "cUnit": "0.000000001"
    },
    "expect": [
      "C · 5τ ≈ 8.820 ms（充满）\n1.764 ms τ（1倍） 3.528 m"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"resistance\":\"42\",\"capacitance\":\"42\",\"voltage\":\"42\",\"rUnit\":\"1000\",\"cUnit\":\"0.000000001\"}，输出区含「C · 5τ ≈ 8.820 ms（充满）\n1.764 ms τ（1倍） 3.5…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/resistor-color-code",
    "inputs": {
      "revValue": "42",
      "revTol": "2"
    },
    "expect": [
      "4 标准值，色环：黄 · 橙 · 黑 · 红"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"revValue\":\"42\",\"revTol\":\"2\"}，输出区含「4 标准值，色环：黄 · 橙 · 黑 · 红」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/root-calculator",
    "inputs": {
      "x": "42"
    },
    "expect": [
      "42\nx = 42 √42 = 6.481 √x 6.481 −√x -6.481 x² 1,764 计算步骤： √42 = 42^(1/2) = 6.481 验证：6.481 × 6.481 = 42 ≈ 42 化简：42 = 1×42 "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x\":\"42\"}，输出区含「42\nx = 42 √42 = 6.481 √x 6.481 −√x -6.48…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/sample-size-calculator",
    "inputs": {
      "N": "42",
      "e": "42",
      "p": "42",
      "conf": "0.95"
    },
    "expect": [
      "p 必须在 0~1 之间（不含端点，p=0 或 1 时所需样本量无定义）\n42\n0.95\n42\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"N\":\"42\",\"e\":\"42\",\"p\":\"42\",\"conf\":\"0.95\"}，p=42 越界 ⇒ 输出区含端点提示「p 必须在 0~1 之间（不含端点，p=0 或 1 时所需样本量无定义）」；默认态（p 正常）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/science-pressure-converter",
    "inputs": {
      "val": "42"
    },
    "expect": [
      "O · 毫米水柱 315.0259 Torr · 托"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"val\":\"42\"}，输出区含「O · 毫米水柱 315.0259 Torr · 托」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/significant-figures",
    "inputs": {
      "num": "42",
      "digits": "42"
    },
    "expect": [
      "-42\n42\n请输入有效数值，位数须为 1–20 的整数"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"num\":\"42\",\"digits\":\"42\"}，位数 42 超出 1–20 上限 ⇒ 输出区含「请输入有效数值，位数须为 1–20 的整数」；默认态（位数正常）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/si-unit-converter",
    "inputs": {
      "fromValue": "42",
      "toValue": "abc123测试"
    },
    "expect": [
      "{i}\n${i}\nabc123测试"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"fromValue\":\"42\",\"toValue\":\"abc123测试\"}，输出区含「{i}\n${i}\nabc123测试」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/spring-oscillation-period",
    "inputs": {
      "m": "42",
      "k": "42"
    },
    "expect": [
      "2π√(m/k) 0.1592"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"m\":\"42\",\"k\":\"42\"}，输出区含「2π√(m/k) 0.1592」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/star-magnitude-compare",
    "inputs": {
      "mag1": "42",
      "mag2": "42",
      "starSearch": "abc123测试"
    },
    "expect": [
      "差 100 倍。\nabc123测试\n未找到匹配的恒星"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"mag1\":\"42\",\"mag2\":\"42\",\"starSearch\":\"abc123测试\"}，输出区含「差 100 倍。\nabc123测试\n未找到匹配的恒星」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/t-score-calculator",
    "inputs": {
      "x": "42",
      "M": "42",
      "sd": "42",
      "zIn": "42"
    },
    "expect": [
      "T = 50 0 Z 分数 50 T 分数 0 偏差 X−M 0 标准差倍数 分步计算 步骤 1： 偏差 = X − M = 42 − 42 = 0"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x\":\"42\",\"M\":\"42\",\"sd\":\"42\",\"zIn\":\"42\"}，输出区含「42\n42\n42\n42\nT = 50 0 Z 分数 50 T 分数 0 偏差 X…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/statistics-calculator",
    "inputs": {
      "data": "1\n2\n3",
      "dtype": "population",
      "bins": "5"
    },
    "expect": [
      "1 2 3\npopulation\n5"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"1\\n2\\n3\",\"dtype\":\"population\",\"bins\":\"5\"}，输出区含「1 2 3\npopulation\n5」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/trigonometry-calculator",
    "inputs": {
      "x": "42",
      "y": "42",
      "mode": "rad",
      "invfunc": "acos"
    },
    "expect": [
      "输入： 42 rad = 42 rad sin -0.917 cos -0.4 tan 2.291 csc = 1/sin -1.091"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"x\":\"42\",\"y\":\"42\",\"mode\":\"rad\",\"invfunc\":\"acos\"}，输出区含「42\n42\nrad\nacos\n输入： 42 rad = 42 rad sin -…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/voltage-divider-calculator",
    "inputs": {
      "vin": "42",
      "r1": "42",
      "r2": "42",
      "voutDesired": "42"
    },
    "expect": [
      " V\n50.0%\n500.00 mA\n21000.00 mW\n42"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"vin\":\"42\",\"r1\":\"42\",\"r2\":\"42\",\"voutDesired\":\"42\"}，输出区含「 V\n50.0%\n500.00 mA\n21000.00 mW\n42」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/wavelength-to-rgb",
    "inputs": {
      "wl": "42",
      "wlNum": "42"
    },
    "clicks": ["calc()"],
    "expect": ["波长须为 380–780 之间的整数（nm）"],
    "ref": "628 批超范围守卫：注入 wl=42（低于可见光下限 380）后计算，页面不再静默算出一组无意义 RGB，而是停算并提示「波长须为 380–780 之间的整数（nm）」，各结果字段清为 —。默认 550 nm 输出不含该提示 ⇒ 判别有效。"
  },
  {
    "slug": "science/variance-calculator",
    "inputs": {
      "data": "1\n2\n3",
      "dtype": "population"
    },
    "expect": [
      "1 2 3\npopulation\n数据（n=3）： 1, 2, 3 σ² = 0.667 均值 x̄ 2 方差 0.667 标准差 0.816 平方和 SS "
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"data\":\"1\\n2\\n3\",\"dtype\":\"population\"}，输出区含「1 2 3\npopulation\n数据（n=3）： 1, 2, 3 σ² = 0…」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/work-done",
    "inputs": {
      "F": "42",
      "d": "42",
      "theta": "42"
    },
    "expect": [
      "位移分力 (N) 28.103 垂直分力 (N)"
    ],
    "ref": "自动补强（B类零用例）：注入非默认输入{\"F\":\"42\",\"d\":\"42\",\"theta\":\"42\"}，输出区含「位移分力 (N) 28.103 垂直分力 (N)」；默认态（输入回退）不含该串 ⇒ 强判别、零逃生。"
  },
  {
    "slug": "science/p-value-calculator",
    "inputs": { "alpha": "0.05", "z0": "10", "tail0": "two" },
    "expect": ["p = 1.523971e-23"],
    "ref": "z=10 双尾：精确 p = 2Q(10) = 1.5239706e-23。原 normalCDF 走 A&S 7.1.26（绝对误差 1.5e-7），在 z=10 饱和为 1 ⇒ 1−cdf=0，p 在赋值阶段就是 0，改格式无效；改用上尾连分式 Q(z) 后 p 可算到 e-23 量级。默认 z=2.5 ⇒ 0.012，不命中。"
  },
  {
    "slug": "science/p-value-calculator",
    "inputs": { "alpha": "0.05", "z0": "10", "tail0": "right" },
    "expect": ["p = 7.619853e-24"],
    "ref": "z=10 右尾：p = Q(10) = 7.61985e-24。原实现 p = 1−Φ(10) 在 Φ 饱和为 1 时直接得 0（假阴性）；现直接取上尾连分式。默认 z=2.5 ⇒ 0.006，不命中。"
  },
  {
    "slug": "science/probability-calculator",
    "clicks": ["selectDist('normal');document.getElementById('mu').value='0';document.getElementById('sigma').value='1';document.getElementById('calcType').value='cdf';document.getElementById('x1').value='-10';calculate()"],
    "expect": ["P(X ≤ -10) = 7.619853e-22%"],
    "ref": "正态 N(0,1) 下尾 x=−10：P = Φ(−10) = 7.61985e-24。原 normalCDF 在 |z|≥8 处饱和为 0 ⇒ 显示 0；改用 z<0 时直接取上尾 Q(−z)。标题端点亦由百分比格式改为普通数值（原显示 −1,000.00%）。默认 x1=1、x2=2、between ⇒ 不命中。"
  },
  {
    "slug": "science/log-calculator",
    "inputs": { "x": "1.0000000000001", "base": "10" },
    "expect": ["4.339474e-14"],
    "ref": "log₁₀(1+1e-13) = 4.33947e-14。原 fmt 先判 |x|<1e-12 → 0，把真实对数值吞成 0；现仅 x===0 返回 0，小值走科学计数法。默认 x=100 ⇒ 2，不命中。"
  },
  {
    "slug": "science/exp-calculator",
    "inputs": { "x": "-30" },
    "expect": ["9.357623e-14"],
    "ref": "e^−30 = 9.35762e-14。原 fmt 对 |x|<1e-12 返回 0，e^−30 与 10^−30 均显示 0；现小值走科学计数法。默认 x=1 ⇒ e=2.718，不命中。"
  },
  {
    "slug": "science/percentile-calculator",
    "inputs": { "data": "1e-13, 2e-13, 3e-13", "percentiles": "50" },
    "expect": ["2.000000e-13"],
    "ref": "数据 1e-13/2e-13/3e-13 的 P50 = 2e-13。原 fmt 先判 |x|<1e-12 → 0，排序数据与分位数全显示 0；现小值走科学计数法。默认数据 ⇒ 不命中。"
  },
  {
    "slug": "science/quadratic-equation",
    "inputs": { "a": "1", "b": "-1e-13", "c": "0" },
    "expect": ["x₁ 1.000000e-13"],
    "ref": "x² − 1e-13 x = 0 ⇒ 两根 0 与 1e-13，Δ = b² − 4ac = 1e-26。原判别式用绝对阈值 |Δ|≤1e-12 ⇒ 误判重根、两个根都显示 0；现改用相对量级 epsD = 1e-12·max(b²,|4ac|)，Δ=1e-26 ≫ 1e-38 ⇒ 两个不等实根（页面根序 x₁=1e-13、x₂=0），且 fmtNum 小值走科学计数法。默认 a=1,b=-3,c=2 ⇒ 根 1 与 2，不命中。"
  },
  {
    "slug": "science/calculator",
    "clicks": ["expression='(2+3)*4^2';calculate()"],
    "expect": ["80", "(2+3)*4^2 ="],
    "ref": "表达式求值独立复算：(2+3)×4² = 5×16 = 80；点击后 display 显示 80、历史行显示「(2+3)*4^2 =」。默认 expression 为空 ⇒ calculate() 直接 return，display 停在 0、历史为空，两锚均不命中（判别时清空 clicks 即回默认态）。"
  },
  {
    "slug": "science/periodic-table",
    "clicks": ["showDetail(26)"],
    "expect": ["原子序数 26"],
    "ref": "元素详情独立核对：原子序数 26 即 Fe（铁，Iron）——第 4 周期第 8 族，原子量 55.845、电子排布 [Ar]3d6 4s2（数据取自页内 ELEMENTS 元素表）。"
       + "boot 默认调 showDetail(1) ⇒ 详情区为「氢 / 原子序数 1」；clicks 改为 showDetail(26) 后详情区出现「原子序数 26」。"
       + "判别器清空 clicks 后兜底调 showDetail()（无参 ⇒ ELEMENTS.find 返回 undefined ⇒ 直接 return），详情仍是氢，不命中。"
  },

  {
    slug: "science/periodic-table",
    clicks: ["buildTable();var h=String(document.getElementById('periodicTable').innerHTML);var ac=h.indexOf('class=\"element cat-actinide\" style=\"grid-column:1;\"');var la=h.indexOf('class=\"element cat-lanthanide\" style=\"grid-column:1;\"');document.getElementById('search').value='PTGRID_'+(ac>=0&&la>=0?'OK':'BAD');"],
    expect: ["PTGRID_OK"],
    ref: "SMS-125 清账（镧锕系独立成行）：18 列 grid 中主表 7×18=126 格占满 7 行，镧系 15 格排第 8 行 1–15 列，旧版锕系第 1 格（Ac）无 grid-column 定位、从第 8 行第 16 列续排 → 与镧系同行错位；现镧系与锕系首格均加 grid-column:1 强制各起新行。探针断言两者首格均带 grid-column:1，旧版无 ⇒ PTGRID_BAD，零逃生。",
  },
  // ---- 2026-11-05：8 页 science 工具「深度解析算例」与页面输出对齐（算例数字均 node 实跑取回）----
  {
    "slug": "science/power-calculator",
    "inputs": { "base": "2", "exp": "-10" },
    "expect": ["2^-10 = 0.001", "1 / 1,024"],
    "ref": "负指数：2^-10 = 1/2^10 = 1/1,024 = 0.0009765625，fmt 后显示 0.001；步骤行给出「1 / 2^10 = 1 / 1,024」。默认 2^10 = 1,024 ⇒ 两条锚均不命中。"
  },
  {
    "slug": "science/log-calculator",
    "inputs": { "x": "1024", "base": "2" },
    "clicks": ["calculate()"],
    "expect": ["log 2 (1,024) = 10", "验证：2^10 = 1,024"],
    "ref": "换底：log₂1,024 = ln1,024/ln2 = 6.931/0.693 = 10，验证行 2^10 = 1,024。默认 x=100、base=2 ⇒ log₂100=6.644，不命中。"
  },
  {
    "slug": "science/lcm-calculator",
    "inputs": { "nums": "8,9,15" },
    "clicks": ["calculate()"],
    "expect": ["LCM = 360", "LCM = (1,080) / 3 = 360"],
    "ref": "递推：lcm(8,9)=72（gcd=1），lcm(72,15)=1,080/3=360；质因数 2³×3²×5=360。默认 12,18,24 ⇒ 72，不命中。"
  },
  {
    "slug": "science/gcd-calculator",
    "inputs": { "nums": "1071,462" },
    "clicks": ["calculate()"],
    "expect": ["GCD = 21", "147 = 7 × 21 + 0"],
    "ref": "欧几里得：1,071=2×462+147 → 462=3×147+21 → 147=7×21+0 ⇒ gcd=21；质因数公共部分 3×7=21。默认 48,36,24 ⇒ 12，不命中。"
  },
  {
    "slug": "science/quartile-calculator",
    "inputs": { "data": "1, 2, 3, 4, 100" },
    "clicks": ["calculate()"],
    "expect": ["Q1 = 2，Q2 = 3，Q3 = 4", "检测到 1 个异常值：100"],
    "ref": "n=5 时 pos=(n−1)p 为 1/2/3 ⇒ Q1=2、Q2=3、Q3=4；IQR=2，上界 4+1.5×2=7 ⇒ 100 判离群。默认 10 个数据 ⇒ 5.25/8/14.25，不命中。"
  },
  {
    "slug": "science/root-calculator",
    "inputs": { "x": "72" },
    "expect": ["√72 = 6√2 ≈ 8.485", "验证：8.485 × 8.485 = 72 ≈ 72"],
    "ref": "根式化简：72=36×2=6²×2 ⇒ √72=6√2≈8.485，自验行 8.485²≈72。默认 x=16 ⇒ √16=4，不命中。"
  },
  {
    "slug": "science/permutation-calculator",
    "inputs": { "n": "10", "r": "3" },
    "expect": ["P(10, 3) = 720", "= 10 × 9 × 8 = 720"],
    "ref": "排列：P(10,3)=10×9×8=720，约分行 10!/7! 同值。默认 n=5、r=3 ⇒ P(5,3)=60，不命中。"
  },
  {
    "slug": "science/mode-calculator",
    "inputs": { "data": "1, 1, 2, 2, 3" },
    "expect": ["众数 = 1, 2（出现 2 次）", "双峰分布（bimodal）"],
    "ref": "频数：1 与 2 各 2 次、3 一次 ⇒ 双众数 1、2（各 40.00%），页面判双峰。默认单峰众数=3 ⇒ 不命中。"
  },

  // ---- 2026-11-05 第二批：fibonacci / factorial / median / nato 算例对齐 ----
  {
    "slug": "science/fibonacci",
    "inputs": { "n": "10" },
    "expect": ["55 F(10)", "2 末项位数"],
    "ref": "数列模式：F(1)…F(10) = 1,1,2,3,5,8,13,21,34,55，末项 F(10)=55、2 位。默认 n=20 ⇒ 6,765，不命中。"
  },
  {
    "slug": "science/median-calculator",
    "inputs": { "data": "1, 2, 3, 4" },
    "clicks": ["calculate()"],
    "expect": ["中位数 = 2.5", "= 5 / 2 = 2.5"],
    "ref": "偶数个取中间两数均值：(2+3)/2 = 5/2 = 2.5。默认 10 个数据 ⇒ 中位数非 2.5，不命中。"
  },
  {
    "slug": "science/nato-phonetic",
    "inputs": { "input": "HELLO NASA" },
    "expect": ["N November A Alfa S Sierra A Alfa"],
    "ref": "逐字符映射 NASA → November/Alfa/Sierra/Alfa；默认 HELLO WORLD 不含该串。"
  },
  {
    slug: "science/convert-power",
    inputs: { val: "", from: "N", to: "lbf" },
    expect: ["请输入要转换的数值"],
    ref: "空态守卫（2026-11-05）：清空数值后 `+''` 得 0（不是 NaN）⇒ 旧输出「0 N = 0 lbf」凭空给零值结论；改为先判原始空串再判 NaN。⚠ 数值 0 本身合法（0 N = 0 lbf 照常计算），只判空串。默认 val=1 ⇒ 提示串不出现；注入 1 N 用例断「0.224809」⇒ 两态互斥。",
  },

  // ---- 624 批：科学计算守卫组（SMS-15/16/23/27）----
  {
    slug: "science/effect-size-calculator",
    inputs: { m1b: "85", sd1b: "10", n1b: "30.5", m2b: "78", sd2b: "12", n2b: "30" },
    clicks: ["setMode(1);calculate();"],
    expect: ["样本量 n 必须是 ≥2 的整数"],
    ref: "SMS-15：双样本 n₁=30.5 非整数。旧 parseInt('30.5')→30 静默截断后仍算 sdPooled=√[(29×100+29×144)/58]=√122≈11.045、d=7/11.045≈0.6338 并给出等级结论；修复后严格整数校验停算。判别性：默认页签 mode0 不读 n1b，且默认 n=30 为整数 ⇒ 该提示默认态零命中。",
  },
  {
    slug: "science/sample-size-calculator",
    inputs: { N: "50.5", conf: "0.95", e: "5", p: "0.5" },
    expect: ["总体大小 N 必须是正整数"],
    ref: "SMS-16 残留一：N=50.5 非整数。旧 parseInt('50.5')→50 静默按有限总体修正得 n₀=384.16、n=384.16/(1+383.16/50)=44.3→45；修复后停算提示。判别性：默认 N 为空（无限总体）⇒ 该提示默认态零命中。",
  },
  {
    slug: "science/sample-size-calculator",
    inputs: { N: "0", conf: "0.95", e: "5", p: "0.5" },
    expect: ["总体大小 N 必须是正整数"],
    ref: "SMS-16 残留二：N=0 非正数。旧 `if(!isNaN(N)&&N>0)` 判假 ⇒ 当作无限总体静默给 n=385；修复后 N 非空即要求正整数。判别性：默认 N 为空 ⇒ 该提示默认态零命中；与上条同为错误分支但触发值不同（小数 vs 零），互为交叉验证。",
  },
  {
    slug: "science/mode-calculator",
    inputs: { data: "1,bad,1,2" },
    expect: ["第 2 项数据无效"],
    ref: "SMS-23：第 2 项 'bad' 非法。旧 parseFloat+filter(NaN) 静默丢弃后按 3 项算得众数 1（占 66.67%）；修复后逐项严格解析并在第 2 项停算。判别性：默认数据 1,2,2,3,3,3,4,4,5 全合法 ⇒ 该提示默认态零命中。",
  },
  {
    slug: "science/mode-calculator",
    inputs: { data: "1,1abc,2" },
    expect: ["第 2 项数据无效"],
    ref: "SMS-23 扩展：'1abc' 是部分数字前缀。旧 parseFloat('1abc')→1 被接受为合法观测，得出错误频数（1 出现 2 次判众数）；新正则 ^[+-]?( digits | .digits )(e...)?$ 拒绝整 token。判别性：默认数据无非法前缀 ⇒ 零命中。",
  },
  {
    slug: "science/variance-calculator",
    inputs: { dtype: "sample", data: "1,bad,2,3" },
    expect: ["第 2 项数据无效"],
    ref: "SMS-27 残留二：'bad' 非法。旧 parseFloat+filter 静默当 3 项算样本方差；修复后严格校验停算并清四面板。判别性：默认数据全合法 ⇒ 零命中。",
  },
  {
    slug: "science/variance-calculator",
    inputs: { dtype: "sample", data: "100000000,100000001" },
    expect: ["浮点消减误差", "请以主结果为准"],
    ref: "SMS-27 残留一：两值仅差 1、量级 1e8。主算 s²=0.5（偏差 ±0.5 → SS=0.5 → /(n-1)=0.5）；替代公式 E(X²)−[E(X)]² 在双精度下消减为 0 并曾无条件标「与上方一致」。修复后按相对误差 relGap=|v2−variance|/max(|variance|,1e-300)>1e-6 判定并改述。判别性：默认数据 2,4,4,4,5,5,7,9 量级小、替代值一致 ⇒ 新提示默认态零命中。",
  },
  {
    slug: "science/variance-calculator",
    inputs: { dtype: "sample", data: "2,4,4,4" },
    clicks: ["(function(){document.getElementById('variance_calculatorTable').innerHTML='OLD';document.getElementById('data').value='3';calculate();var t=String(document.getElementById('variance_calculatorTable').innerHTML);document.getElementById('__tbProbe').textContent='VARCLR '+(t===''?'OK':'BAD t='+t);})()"],
    expect: ["VARCLR OK"],
    ref: "624 复核失败重做：样本方差在仅剩 1 个数时只提示、不调 __varClear()；空数据分支同样只改主输出并 return ⇒ 旧 table/diff/chart/hist 残留，包装层还会把提示当结果重绘旧面板。修复后两条错误分支均置 __variance_calculatorValid=false + __varClear()，extras 遇错误态直接返回。探针预置旧表面板后注入单值样本数据，断言面板被清空；默认态无探针串 ⇒ 零逃生。"
  },
  {
    slug: "science/mode-calculator",
    inputs: { data: "1,2,2,3" },
    clicks: ["(function(){document.getElementById('mode_calculatorTable').innerHTML='OLD';document.getElementById('data').value='';calculate();var t=String(document.getElementById('mode_calculatorTable').innerHTML);document.getElementById('__tbProbe').textContent='MODECLR '+(t===''?'OK':'BAD t='+t);})()"],
    expect: ["MODECLR OK"],
    ref: "624 复核失败重做：众数页清空数据后 data.length<1 分支只更新主输出并 return，未清 table/diff/chart/hist，包装层随后把「请输入数据」当结果记入历史并重绘旧面板。修复后空数据/非法数据分支统一 __modeClear() 并置错误态，extras 提前返回。探针预置旧表面板后清空数据，断言面板被清空；默认态无探针串 ⇒ 零逃生。"
  },
  {
    "slug": "science/wavelength-to-rgb",
    "inputs": { "wl": "550", "wlNum": "520.5" },
    "clicks": ["syncWl('num')"],
    "expect": ["不接受小数或超范围值"],
    "ref": "628 批小数守卫：数字框输入 520.5（非整数波长）后同步，页面不再用 parseFloat 静默截断成 520，而是停算并提示「波长须为 380–780 之间的整数（nm），不接受小数或超范围值」。默认 550 整数输入不出现该提示 ⇒ 判别有效。"
  },
  {
    "slug": "science/wavelength-to-rgb",
    "inputs": { "wl": "720", "wlNum": "720" },
    "clicks": ["calc()"],
    "expect": ["#DB0000", "416.67", "1.72"],
    "ref": "628 批衰减区一致：λ=720 nm 时亮度因子 f=0.3+0.7·(780−720)/80=0.825，R=round(255·0.825^0.8)=219 ⇒ HEX #DB0000；频率 3e8/720e-9=416.67 THz、光子能量 1240/720=1.72 eV。三项独立可手算复算，参考表新增的 720 nm 行与本算法同源；默认 550 nm 输出 #A3FF00/545.45/2.25 不含这些串 ⇒ 判别有效。"
  },
  {
    "slug": "science/wire-gauge-converter",
    "inputs": { "awg": "12.5" },
    "clicks": ["calcFromAwg()"],
    "expect": ["1.937"],
    "ref": "629 批小数线规：AWG 12.5 ⇒ d=0.127·92^((36−12.5)/39)=1.937 mm（页面 resDmm toFixed(3) 与明细表 toFixed(4) 均以 1.937 开头）。旧实现对输入用 parseInt，12.5 被截断成 12 ⇒ 2.053 mm，与本用例期望不同 ⇒ 判别有效。默认 awg=24 ⇒ 0.511 mm，不出现 1.937。"
  },
  {
    "slug": "science/wire-gauge-converter",
    "inputs": { "awg": "" },
    "clicks": ["calcFromAwg()"],
    "expect": ["请输入 AWG 线规号（0–40）"],
    "ref": "629 批空值守卫：清空 AWG 输入框后调用计算，页面不再静默 return 保留上一次结果，而是清空各结果字段并提示「请输入 AWG 线规号（0–40）」。默认 awg=24 正常出结果，不含该提示 ⇒ 判别有效。"
  },
  {
    "slug": "science/wire-gauge-converter",
    "inputs": { "mm": "0" },
    "clicks": ["calcFromMm()"],
    "expect": ["请输入大于 0 的线径（mm）"],
    "ref": "629 批零线径守卫：线径填 0 后计算，页面不再静默 return 保留旧值，而是清空结果并提示「请输入大于 0 的线径（mm）」（d≤0 时 mmToAwg 对数为 −∞，结果无意义）。默认 awg=24 模式不含该提示 ⇒ 判别有效。"
  },
  {
    "afterLoad": true,
    "slug": "science/torque-converter",
    "inputs": { "val": "", "from": "lbft" },
    "clicks": ["convert()"],
    "expect": ["请输入有效的扭矩数值"],
    "ref": "629 批空值守卫：扭矩值清空后调用换算，页面不再用 parseFloat(...)||0 把空值当 0 算出一整列 0 并写入历史，而是清空结果并提示「请输入有效的扭矩数值」。注入 val=20 等正常值时不出现该提示 ⇒ 判别有效。"
  },
  {
    "slug": "science/vector-calculator",
    "inputs": { "dim": "3", "op": "angle", "a0": "1e-13", "a1": "0", "a2": "0", "b0": "1", "b1": "0", "b2": "0" },
    "clicks": ["calculate()"],
    "expect": ["θ = 0°"],
    "ref": "SMS-166 相对零判定：A=(1e-13,0,0) 是非零向量（最大分量 1e-13≠0），与 B=(1,0,0) 同向 ⇒ cosθ=1 ⇒ θ=0°。旧实现用绝对阈值 mA<1e-12 把 A 误判为零向量并提示「零向量无法计算夹角」。现判据为 |A| ≤ max|分量|·1e-12（此处 1e-13 > 1e-25）⇒ 正常计算。默认 op=add 不出现该角度串 ⇒ 判别有效。"
  },
  {
    "slug": "science/matrix-calculator",
    "inputs": { "size": "2", "op": "rank", "a0": "1e-13", "a1": "0", "a2": "0", "a3": "1e-13" },
    "clicks": ["calculate()"],
    "expect": ["rank(A) = 2"],
    "ref": "SMS-167 相对容差：A=[[1e-13,0],[0,1e-13]] 两列线性无关 ⇒ rank=2。旧实现用绝对阈值 Math.abs(m[pivot][col])<1e-12 直接 continue，主元 1e-13 被当 0 ⇒ rank=0。现判据为 max|元素|·1e-12=1e-25，主元 1e-13 > 1e-25 正常累加。默认 3×3 单位阵 rank=3，不出现 'rank(A) = 2'。"
  },
  {
    "slug": "science/matrix-calculator",
    "inputs": { "size": "2", "op": "power", "scalar": "1.5", "a0": "1", "a1": "2", "a2": "3", "a3": "4" },
    "clicks": ["calculate()"],
    "expect": ["幂次必须是整数"],
    "ref": "631 批幂次严格整数：scalar=1.5 时页面不再用 parseInt 静默截断成 1 并给出 A^1，而是停算提示「幂次必须是整数（不接受小数或非数字）」。默认 scalar=2（整数）⇒ 输出 A^2，不含该提示串。"
  },
  {
    "slug": "science/matrix-calculator",
    "inputs": { "size": "2", "op": "inv", "a0": "4", "a1": "7", "a2": "2", "a3": "6" },
    "clicks": ["calculate()"],
    "expect": ["与单位矩阵最大偏差：|Δ| = 2.22e-16", "在容差内"],
    "ref": "632 批 SMS-109：求逆分支原有 `const check = mul(A, inv)` 计算后从未使用，步骤行只打印「验证：A · A⁻¹ = I」这句定义，属死代码（承诺的验证结果未实现）。现实际输出乘积矩阵并给出与单位矩阵的最大偏差：A=[[4,7],[2,6]] det=10，A⁻¹=[[0.6,-0.7],[-0.2,0.4]]，A·A⁻¹ 对角元 1±1.1e-16，最大偏差 2.22e-16，容差 max(1e-9, max|元素|·1e-12)=1e-9 ⇒ 判「在容差内」。默认 op=det 不输出该行 ⇒ 强判别。"
  },
  {
    "slug": "science/wire-gauge-converter",
    "inputs": { "awg": "20.5" },
    "clicks": ["(function(){var cap='';var fake={};Object.defineProperty(fake,'innerHTML',{set:function(v){cap=v;},get:function(){return cap;}});var oq=document.querySelector.bind(document);document.querySelector=function(s){return /wgHidden/.test(String(s))?fake:oq(s);};globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){}}};try{__wgExport();}catch(e){cap='ERR '+e.message;}document.querySelector=oq;document.getElementById('__tbProbe').textContent='WGEXP '+(cap.indexOf('20.50')>=0?'OK':'BAD '+cap.slice(0,120));})()"],
    "expect": ["WGEXP OK"],
    "ref": "625/629 复核失败重做：__wgExport 的 AWG 分支原用 parseInt，主算按 20.5 计算、CSV 却按 20 计算。修复后与 calcFromAwg 同源：Number() 保留小数，并补空值/0–40 范围校验。探针拦截 #wgHidden tbody 写入，断言导出首行为 AWG=20.50；旧实现为 20.00 ⇒ 转红。默认 awg=24 不含 20.50 ⇒ 强判别。"
  },
  {
    "slug": "science/matrix-calculator",
    "clicks": ["(function(){var A=[[1e-13,0],[0,1e-13]];var inv=null;try{inv=inverse(A);}catch(e){}var okInv=!!inv&&Math.abs(inv[0][0]-1e13)<=1e-2&&Math.abs(inv[1][1]-1e13)<=1e-2&&inv[0][1]===0;var s1='x',s2='x';try{s1=__matSingular(A);s2=__matSingular([[1,2],[2,4]]);}catch(e){}document.getElementById('__tbProbe').textContent='MATINV '+((okInv&&s1===false&&s2===true)?'OK':'BAD inv='+(inv?JSON.stringify(inv).slice(0,60):'null')+' s1='+s1+' s2='+s2);})()"],
    "expect": ["MATINV OK"],
    "ref": "631 复核失败重做：inverse() 原用 |det| 对比元素级 ε（max|a|×1e-12），行列式是元素的 n 次幂、量纲不一致。A=1e-13·I₂ 时 det=1e-26 < ε=1e-25 ⇒ 误判奇异并返回 null，实际逆为 1e13·I₂。修复后新增 __matSingular 用部分主元消元（元素级 ε）统一行列式与求逆判定：该矩阵主元 1e-13 ≫ 1e-25 ⇒ 可逆；真奇异 [[1,2],[2,4]] ⇒ 判奇异。默认 op=det 不调用 inverse ⇒ 探针串零命中。"
  },
  {
    "slug": "science/matrix-calculator",
    "clicks": ["(function(){globalThis.TBKit={util:{isEn:function(){return true;}}};try{showFormulas();}catch(e){}var h=String(document.getElementById('output').innerHTML);document.getElementById('__tbProbe').textContent='MATEN '+((h.indexOf('Matrix formula reference')>=0&&h.indexOf('Addition:')>=0&&!/[\\u4e00-\\u9fff]/.test(h))?'OK':'BAD '+h.slice(0,100));})()"],
    "expect": ["MATEN OK"],
    "ref": "632 复核失败重做：showFormulas() 原无条件写入中文标题与多行中文说明，英文态（?lang=en-US）点击「公式说明」仍全中文。修复后按 __matIsEn() 分流整套英文文案。探针 mock TBKit.util.isEn=true 后调用，断言含 Matrix formula reference / Addition: 且无 CJK；默认态不执行 clicks ⇒ 零逃生。"
  },
  {
    "slug": "science/astro-geo-calculator",
    "inputs": { "sun-lat": "-33.86", "sun-lon": "151.21", "sun-date": "2026-06-21" },
    "clicks": ["calcSunriseSunset()"],
    "expect": ["33.8600°S, 151.2100°E", "05:03", "14:47"],
    "ref": "SMS-65/67：hourAngle 算地方太阳时，转北京时间应 +8−lon/15（东八区中央经线120°E），旧版写反为 +lon/15−8。悉尼 2026-06-21（南半球冬季，dayOfYear=172、赤纬23.4498°）：cosH=−tan(−33.86°)tan(23.4498°)=0.2898⇒H=73.0796°⇒太阳时日出 12−73.0796/15=7.128h；修正 7.128+8−151.21/15=5.047h⇒05:03、日落 14:47。位置行旧版固定 °N/°E 对负值显示 −33.8600°N；修复后按符号输出 33.8600°S, 151.2100°E。默认 lat/lon/date 不同且需 clicks 触发 ⇒ 三条均不命中（默认态 sun-date 空，不产生该位置/时刻串）。"
  },
  {
    "slug": "science/astro-geo-calculator",
    "inputs": { "wind-speed": "12", "wind-unit": "kmh" },
    "clicks": ["calcWindLevel()"],
    "expect": ["3.3 风速（m/s）", "蒲福 2 级", "轻风"],
    "ref": "SMS-66：蒲福表各级 min~max 间留 0.1 m/s 空隙（1.5→1.6、3.3→3.4…），12 km/h=3.3333 m/s 正落 3.3~3.4 空隙，旧版 !found 兜底 12 级飓风。修复后按 min 下界逐级命中：3.3333≥level2.min(1.6) 且 <level3.min(3.4) ⇒ 2 级轻风。3.3 m/s 为 3.3333.toFixed(1)。默认 wind-speed=5 m/s（命中3级微风）且需 clicks ⇒ 三条均不命中。"
  },
  {
    "slug": "science/astro-geo-calculator",
    "inputs": { "hz-height": "2" },
    "clicks": ["calcHorizon()"],
    "expect": ["0.0m 5km处目标最低高度", "1.9m 10km处目标最低高度", "17.5m 20km处目标最低高度"],
    "ref": "SMS-68：观察者高度 h=2m 时几何地平线 d0=sqrt(2×6371km×0.002km)=5.0482km。目标最低高度按 (d−d0)²/(2R)×1000 计算：5km 未超地平线记 0.0m；10km 得 1.922→1.9m；20km 得 17.525→17.5m。旧版三卡写死 d²/(2R)，无论 h 为何均输出 2.0/7.9/31.4m 且标签为「遮挡」，三条锚均不命中；默认 h=1.7m 得 0.0/2.2/18.5m，注入失败亦不命中。"
  },
  {
    "slug": "science/calc-distance",
    "clicks": ["var _qs=document.querySelector.bind(document);document.querySelector=function(s){if(String(s).indexOf('dms')>=0)return {checked:true};return _qs(s);};try{swapFmt();}catch(e){}document.querySelector=_qs;var r=document.getElementById('res');r.innerHTML=r.innerHTML+' DMSPROBE type='+document.getElementById('lat1').type+' val='+document.getElementById('lat1').value;"],
    "expect": ["DMSPROBE type=text val=39°54'15.12\""],
    "ref": "SMS-77：四个坐标输入原为 type=number，swapFmt() 把度分秒串（含 ° ' \"）写回 number 输入被浏览器清空 ⇒ 坐标全空报「坐标格式无效」、切回十进制也无法恢复。修复后切格式时同步把四输入 type 改为 text（度分秒）/number（十进制），并用 parseCoord 读取已格式化值。探针勾选 dms 调 swapFmt，断言 lat1.type=text 且保留 39°54'15.12\"；旧版 type 恒 number ⇒ 不命中。默认态不执行 clicks ⇒ 零逃生。"
  },
  {
    "slug": "science/calc-distance",
    "inputs": { "lat1": "39.904200", "lon1": "116.407400", "lat2": "31.230400", "lon2": "121.473700" },
    "clicks": ["var ids=['lat1','lon1','lat2','lon2'];ids.forEach(function(id){var el=document.getElementById(id),t=el.type;Object.defineProperty(el,'type',{configurable:true,get:function(){return t;},set:function(v){if(v==='number'&&/[^\\d.eE+-]/.test(String(el.value)))el.value='';t=v;}});});var mode=false,before=ids.map(function(id){return document.getElementById(id).value;}).join(','),_qs=document.querySelector.bind(document);document.querySelector=function(s){if(String(s).indexOf('dms')>=0)return {checked:mode};return _qs(s);};mode=true;swapFmt();var mid=ids.map(function(id){return document.getElementById(id).value;}).join(',');mode=false;swapFmt();document.querySelector=_qs;var after=ids.map(function(id){return document.getElementById(id).value;}).join(',');document.getElementById('__tbProbe').textContent='DMSRT '+((mid.indexOf('°')>=0&&after===before)?'OK':'BAD '+before+'|'+mid+'|'+after);"],
    "expect": ["DMSRT OK"],
    "ref": "1029 复核重做：桩内对四个坐标输入补真机语义——切到 number 时含 ° ' \" 的度分秒串会被清空。旧版先改 type 再读值，十进制→度分秒→十进制后四坐标全丢；修复版先在旧 type 下缓存，再切 type 写回，往返必须逐字回到 39.904200/116.407400/31.230400/121.473700。探针仅在 clicks 注入后出现。"
  },
  {
    "slug": "science/calc-distance",
    "clicks": ["var q=String.fromCharCode(39),dq=String.fromCharCode(34);var a=parseCoord('-0°30'+q+'0'+dq),b=parseCoord('-0 30 0'),c=parseCoord('0°30'+q+'0'+dq+'S'),d=parseCoord('');document.getElementById('lat1').value='';calc();var msg=String(document.getElementById('res').innerHTML);document.getElementById('__tbProbe').textContent='COORDNEG '+(a===-0.5&&b===-0.5&&c===-0.5&&d===null&&msg.indexOf('坐标格式无效')>=0?'OK':'BAD '+[a,b,c,d].join(','));"],
    "expect": ["COORDNEG OK"],
    "ref": "1029 复核重做：-0°30' 与 -0 30 0 的负零在数值比较 deg<0 为假，旧版翻成正 0.5；修复版按字面负号识别为 -0.5，同时 S 后缀仍为 -0.5、空串仍判 null 并拦截计算。默认态不执行 clicks ⇒ 零逃生。"
  },
  {
    "slug": "science/astronomy-toolkit",
    "inputs": { "mag1": "1.5", "mag2": "1.5" },
    "clicks": ["calcMagnitude()"],
    "expect": ["两天体星等相同，亮度相等（比值 1.00）"],
    "ref": "SMS-71：两星等相等时 ratio=2.512^0=1，旧版 brighter='一样亮' 拼出「即天体 一样亮 比 A 亮 1.00 倍」自相矛盾。修复后相等分支独立输出「两天体星等相同，亮度相等（比值 1.00）」（英文态经 TBKit.util.isEn helper）。默认 mag1=-1.46/mag2=2.0 不等 ⇒ 走原「比…亮…倍」分支，不含该串。"
  },
  {
    "slug": "science/astronomy-toolkit",
    "inputs": { "moonDate": "2026-09-25" },
    "clicks": [
      "(function(){var hist=[],rows=0,chart=null,noop=function(){};globalThis.TBKit={util:{isEn:function(){return false;},diffBox:noop,exportTable:noop},matrix:{table:function(s,o){rows=o.rows.length;}},chart:{line:function(s,o){chart=o;}},history:{list:function(){return hist.slice();},last:function(){return hist.length?hist[hist.length-1].d:null;},record:function(d){hist.push({t:Date.now()+hist.length*1000,d:d});},mount:noop,clear:function(){hist.length=0;},diffLast:function(){return null;}},preset:{bar:noop},export:{csv:noop},share:{params:function(){return {};}}};var _qsa=document.querySelectorAll.bind(document);document.querySelectorAll=function(s){if(String(s).indexOf('input[id]')>=0)return ['moonDate','mag1','mag2','meteorDiameter','meteorSpeed','meteorDensity','meteorAngle','groundDensity','latInput','lonInput','utmZone','utmHemisphere'].map(function(id){return document.getElementById(id);});return _qsa(s);};var mg=document.getElementById('moonInfoGrid');var ids=['moonPhaseName','moonAge','moonIllum','moonNextNew'];Object.defineProperty(mg,'textContent',{configurable:true,get:function(){return ids.map(function(id){return document.getElementById(id).textContent||'';}).join(' ');},set:function(v){mg.innerHTML=String(v);}});__astronomy_toolkit_last=0;calcMoonPhase();document.getElementById('moonDate').value='2026-06-21';__astronomy_toolkit_last=0;calcMoonPhase();var last=hist.length?String(hist[hist.length-1].d['结果']||''):'';document.getElementById('moonDate').value='ASTROHIST_'+(last.indexOf('上弦月 6.2 37.9 23.3天')>=0&&rows===2?'OK':'BAD '+last);})()"
    ],
    "expect": ["ASTROHIST_OK"],
    "ref": "SMS-74：附加层只包裹 calcMoonPhase()，月相结果写在 #moonInfoGrid（非 .result-box）。旧 __astronomy_toolkitResText() 取页面首个 .result-box（#magResult），未算星等时读到占位「请输入…」被正则判空，月相历史/表/图全无；算过星等则把星等结果误记为月相。修复后优先读 #moonInfoGrid，探针注入 2026-09-25（满月13.6/98.6/15.9天）与 2026-06-21（上弦月6.2/37.9/23.3天）两次，断言最后一条历史结果为后者且表格2行。旧版无历史记录 ⇒ ASTROHIST_BAD；默认态不执行 clicks ⇒ 零逃生。harness 需补 input 选择器与月相网格 textContent getter，属桩能力边界。"
  },
  {
    "slug": "science/astronomy-toolkit",
    "inputs": { "moonDate": "2026-01-01" },
    "clicks": ["calcMoonPhase();var a=document.getElementById('moonPhaseName').textContent,b=document.getElementById('moonIllum').textContent;document.getElementById('moonDate').value='MOONILL_'+(a==='盈凸月'&&b==='93.9'?'OK':'BAD '+a+'/'+b);"],
    "expect": ["MOONILL_OK"],
    "ref": "SMS-70：照明度原用 8 段等距线性插值，2026-01-01（页面按 UTC 12:00 取日）月龄 12.4215 天落在 9.22831~12.91963 段，旧式算 50+(12.4215−9.22831)/3.69133×25≈71.6%，且 12.91963~16.61096 全程恒 100%（3.69 天平台）。修复为相角余弦模型 (1−cos(2π·age/S))/2：age=12.4215、S=29.530588 ⇒ 93.9%，月相名称仍按原阈值判「盈凸月」。旧版 ⇒ MOONILL_BAD 71.6%；默认态（moonDate 空→今天）不命中。"
  },
  {
    "slug": "science/astronomy-toolkit",
    "inputs": { "polarLat": "66.5" },
    "clicks": ["calcPolar();var t=String(document.getElementById('polarResult').innerHTML);document.getElementById('polarLat').value='POLAREDGE_'+(t.indexOf('66.5°')>=0&&t.indexOf('不是全年极昼或极夜')>=0&&t.indexOf('全年为极昼或极夜')<0?'OK':'BAD '+t.slice(0,60));"],
    "expect": ["POLAREDGE_OK"],
    "ref": "SMS-72：纬度 66.5° 时 declCritical=23.5°，大于页面简化模型的 maxDecl=23.44°，旧版进入早退分支输出「理论上全年为极昼或极夜」，与常用 66.5° 极圈定义直接矛盾。修复后说明该纬度处在常用 66.5° 与 23.44° 真极圈之间：太阳中心几何口径不满足严格阈值，但视直径+折射可致夏至/冬至前后短暂无落日或无日出，并明确否定「全年」。Time and Date 天文资料确认极圈按太阳中心定义、上缘与折射会让极点内侧出现偏差，不能把边界附近写成全年极昼/极夜。默认 polarLat=70（进入正常日期分支）不命中。"
  },
  {
    slug: "science/battery-life-calculator",
    inputs: {},
    clicks: ["var _qs=document.querySelector;document.querySelector=function(s){return s==='#battHidden tbody'?document.getElementById('battHidden'):_qs(s);};globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){}},diffBox:function(){}};var c=document.getElementById('cap'),u=document.getElementById('capUnit'),i=document.getElementById('curr'),iu=document.getElementById('currUnit');c.value='3';u.value='1000';i.value='2';iu.value='1000';document.getElementById('volt').value='7.4';document.getElementById('eff').value='0.9';__batteryExport();var h=String(document.getElementById('battHidden').innerHTML);document.getElementById('result').innerHTML='BATEXPUNIT_'+(h.indexOf('3 Ah')>=0&&h.indexOf('2 A')>=0&&h.indexOf('3000 Ah')<0&&h.indexOf('2000 A')<0?'OK':'BAD '+h.slice(0,120));delete globalThis.TBKit;document.querySelector=_qs;"],
    expect: ["BATEXPUNIT_OK"],
    ref: "1004 批复核：容量 3 Ah、电流 2 A 时内部换算为 3000 mAh/2000 mA 正确，但旧导出把换算值与用户所选单位标签拼成「3000 Ah」「2000 A」。修复后导出显示原始输入值与对应标签「3 Ah」「2 A」，换算值只用于功率/能量与有效容量。用例把 harness 的 #battHidden tbody 查询重定向到真实元素，避免读空桩造成假绿。"
  },
  {
    slug: "science/battery-life-calculator",
    inputs: {},
    clicks: ["var _qs=document.querySelector;document.querySelector=function(s){return s==='#battHidden tbody'?document.getElementById('battHidden'):_qs(s);};globalThis.TBKit={util:{isEn:function(){return false;},exportTable:function(){}},diffBox:function(){}};var c=document.getElementById('cap'),u=document.getElementById('capUnit'),i=document.getElementById('curr'),iu=document.getElementById('currUnit');c.value='2';u.value='1000';i.value='500';iu.value='1';document.getElementById('volt').value='3.7';document.getElementById('eff').value='1';__batteryExport();var h=String(document.getElementById('battHidden').innerHTML);document.getElementById('result').innerHTML='BATMIXUNIT_'+(h.indexOf('2 Ah')>=0&&h.indexOf('500 mA')>=0&&h.indexOf('2000 Ah')<0?'OK':'BAD '+h.slice(0,120));delete globalThis.TBKit;document.querySelector=_qs;"],
    expect: ["BATMIXUNIT_OK"],
    ref: "1004 批复核·混合单位补强：容量 2 Ah、电流 500 mA，内部统一为 2000 mAh/500 mA 计算 3.7 W 与 7.40 Wh，但导出必须显示「2 Ah」「500 mA」。旧版容量行写「2000 Ah」，本用例变红；与上一条 Ah/A 同组互证。"
  },
  {
    slug: "science/gcd-calculator",
    inputs: {},
    clicks: ["var r=factorize(1000036000099);document.getElementById('nums').value='GCDBUDGET_'+(r.indexOf('超出同步计算上限')>=0&&r.indexOf('1000003')<0?'OK':'BAD '+r);"],
    expect: ["GCDBUDGET_OK"],
    ref: "1006 批复核：1000036000099=1000003×1000033 是安全整数，旧 factorize 需约一百万次同步试除才给出完整分解；现设 200000 次上限，超限只提示跳过分解而不伪造结果。旧版返回「1000003 × 1000033」⇒ BAD；不直接调用 9007199254740881 是为了让旧版差分在受控时间内完成。"
  },
  {
    slug: "science/gcd-calculator",
    inputs: {},
    clicks: ["document.getElementById('nums').value='1000036000099,3';calculate();var h=String(document.getElementById('output').innerHTML);document.getElementById('output').innerHTML='GCDBIG_'+(h.indexOf('GCD = 1')>=0&&h.indexOf('超出同步计算上限')>=0&&h.indexOf('GCD = 12')<0?'OK':'BAD');"],
    expect: ["GCDBIG_OK"],
    ref: "1006 批复核·链路补强：大安全整数与 3 的 GCD=1 必须照常算出，质因数分解跳过提示须同时出现在结果区。旧版虽给出 GCD=1 但没有跳过提示且完成长分解；默认 48,36,24 的 GCD=12，不命中。"
  },
  {
    slug: "science/gcd-calculator",
    inputs: {},
    clicks: ["var s=String(factorize);document.getElementById('nums').value='GCDGUARD_'+(typeof MAX_TRIAL_DIVISIONS!=='undefined'&&MAX_TRIAL_DIVISIONS===200000&&s.indexOf('MAX_TRIAL_DIVISIONS')>=0&&s.indexOf('超出同步计算上限')>=0?'OK':'BAD');"],
    expect: ["GCDGUARD_OK"],
    ref: "1006 批复核·源码形态补强：复核点名的 9007199254740881 若在旧版直接执行会长时间阻塞，故用源码形态断言分解函数确实读固定试除上限并带跳过分支；旧版无该常量与分支 ⇒ BAD。"
  },
  {
    slug: "science/significant-figures",
    inputs: { num: "987654321", digits: "16" },
    clicks: ["var v=1.234567890123456;var r=roundToSig(v,16);document.getElementById('num').value='SIGFP_'+(r===v?'OK':'BAD');"],
    expect: ["SIGFP_OK"],
    ref: "1007 批复核：原数已是 16 位有效数字，修约后应保持不变。旧版对 scaled 无条件加 abs(scaled)×EPSILON×8 补偿，末位被推高一位；新版仅按十进制第 17 位判断，无后续位则不进位。用等值布尔哨兵避免把长浮点写进 expect 造成跨环境 1ULP 反模式；默认 num/digits 不命中探针。"
  },
  {
    slug: "science/significant-figures",
    inputs: {},
    clicks: ["var r=document.getElementById('result'),n=document.getElementById('num'),d=document.getElementById('digits');d.value='1';n.value='2.5';calc();var a=String(r.innerHTML).replace(/<[^>]+>/g,' ');n.value='3.5';calc();var b=String(r.innerHTML).replace(/<[^>]+>/g,' ');n.value='-2.5';calc();var c=String(r.innerHTML).replace(/<[^>]+>/g,' ');r.innerHTML='SIGEVEN_'+(a.indexOf('保留 1 位有效数字： 2')>=0&&b.indexOf('保留 1 位有效数字： 4')>=0&&c.indexOf('保留 1 位有效数字： -2')>=0?'OK':'BAD');"],
    expect: ["SIGEVEN_OK"],
    ref: "1007 批复核·半值与负数：页面引据写 NIST B.7.1，恰好 5 且后续全 0 时应舍入到偶数：2.5→2、3.5→4、-2.5→-2。旧版 Math.round 对正数 2.5 进一、对负数受补偿影响给 -3，三项不可能同时命中；默认态无探针串。"
  },
  {
    slug: "science/significant-figures",
    inputs: {},
    clicks: ["var r=document.getElementById('result'),n=document.getElementById('num'),d=document.getElementById('digits');d.value='2';n.value='1.25e3';calc();var a=String(r.innerHTML).replace(/<[^>]+>/g,' ');d.value='1';n.value='2.5001';calc();var b=String(r.innerHTML).replace(/<[^>]+>/g,' ');n.value='2.4999';calc();var c=String(r.innerHTML).replace(/<[^>]+>/g,' ');r.innerHTML='SIGNEAR_'+(a.indexOf('保留 2 位有效数字： 1200')>=0&&a.indexOf('1.2e+3')>=0&&b.indexOf('保留 1 位有效数字： 3')>=0&&c.indexOf('保留 1 位有效数字： 2')>=0?'OK':'BAD');"],
    expect: ["SIGNEAR_OK"],
    ref: "1007 批复核·科学计数法与半值两侧：1.25e3 按 NIST 偶数规则为 1.2e3=1200（旧版浮点放大 125 后原样回除得 1250）；2.5001>半值进到 3，2.4999<半值舍到 2。默认 num/digits 不同，且默认态无探针串。"
  },
  {
    slug: "science/significant-figures",
    inputs: { num: "1.234567890123456789", digits: "20" },
    clicks: ["calc();var h=document.getElementById('result').innerHTML;document.getElementById('result').innerHTML='SIG20_'+(h.includes('1.2345678901234567890</strong>')&&h.includes('1.2345678901234567890e+0')?'OK':'BAD');"],
    expect: ["SIG20_OK"],
    ref: "第1007批再次复核：20位修约必须使用原始十进制输入，不能先转成Number导致末尾丢失。"
  },
  {
    slug: "science/significant-figures",
    inputs: {},
    clicks: ["var a=exactSig('-1.234567890123456785e2',18),b=exactSig('1.234567890123456795e2',18),c=exactSig('1e1001',3);document.getElementById('result').innerHTML='SIGEXACT_'+(a.plain==='-123.456789012345678'&&b.plain==='123.456789012345680'&&c===null?'OK':'BAD');"],
    expect: ["SIGEXACT_OK"],
    ref: "第1007批再次复核：长科学计数法、负数及十进制半值向偶数修约，过大指数安全拦截。"
  },
  {
    slug: "science/equation-balancer",
    inputs: { eqInput: "NH3 = NH + NH4 + N3H" },
    clicks: ["balance();var h=String(document.getElementById('resultArea').innerHTML).replace(/<[^>]+>/g,' ');document.getElementById('eqInput').value='EQRANGE_'+(h.indexOf('有限搜索范围内未找到全正系数')>=0&&h.indexOf('不等于方程式无解')>=0?'OK':'BAD '+h.slice(0,80));"],
    expect: ["EQRANGE_OK"],
    ref: "1009 批复核·有限搜索边界：NH3 → NH + NH4 + N3H 存在全正解 14:1:10:1，但权重超出 ±8 搜索范围；旧版把未命中说成「反应物与生成物可能放反、方程式有误」，现明确「搜索范围未命中不等于无解」。默认 H2+O2=H2O 有唯一解，不命中。"
  },
  {
    slug: "science/meteor-crater-estimator",
    inputs: { meteorDiameter: "42", meteorVelocity: "13", impactAngle: "60", targetDensity: "3000" },
    clicks: ["calc();var a=String(document.getElementById('result').innerHTML);document.getElementById('targetDensity').value='-1';calc();var b=String(document.getElementById('result').innerHTML),t=String(document.getElementById('meteor_crater_estimatorTable').innerHTML);document.getElementById('targetDensity').value='3000';calc();var c=String(document.getElementById('result').innerHTML);document.getElementById('targetDensity').value='METEORNEG_'+(a.indexOf('撞击坑直径')>=0&&b.indexOf('均须为正值')>=0&&t.length===0&&c.indexOf('撞击坑直径')>=0?'OK':'BAD');"],
    expect: ["METEORNEG_OK"],
    ref: "1012 批复核·状态链：合法 42 m/13 km·s⁻¹/60°/3000 kg·m⁻³ 得撞击坑结果；地表密度改 -1 时旧版算 Math.pow(负数,1/3)=NaN 或残留旧结论，现拦截、清空表格且提示密度须为正；恢复 3000 后结果重现。默认直径 50、速度 20、角度 45，不命中本组。"
  },
  {
    slug: "science/chemistry-calculator",
    inputs: { formula: "abc123测试" },
    clicks: ["var a=parseFormula('H2O..NaCl'),b=parseFormula('.H2O'),c=parseFormula('H2O·'),d=calcMolarMass('CuSO4.5H2O');document.getElementById('formula').value='CHMEMPTY_'+(a===null&&b===null&&c===null&&d&&Math.abs(d.totalMass-249.7)<0.01?'OK':'BAD');"],
    expect: ["CHMEMPTY_OK"],
    ref: "1015 批复核：旧 parseFormula 先 split 再 filter 丢空段，把 H2O..NaCl、.H2O、H2O· 当合法；现发现首尾或连续分隔符立即返回 null，同时正常结晶水 CuSO4·5H2O 仍按 249.70 g/mol 解析。默认公式不同且无探针串。"
  },
{
  "slug": 'science/p-value-calculator',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/science/p-value-calculator.html\',\'utf8\');var i=h.indexOf(\'function setMode(m){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'currentMode=m\')>=0&&seg.indexOf(\'calculate();\')>=0;document.getElementById(\'__tbProbe\').textContent=\'PVALM0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['PVALM0 OK'],
  "ref": "第1339批·模式切换残留旧结果修复源码形态强锚：旧版 setMode 只切 currentMode/class/display 不重算，共用 #output 保留上一模式结论；修复后切换即调 calculate()。旧版无 ⇒ BAD。"
},
{
  "slug": 'science/effect-size-calculator',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/science/effect-size-calculator.html\',\'utf8\');var i=h.indexOf(\'function setMode(m){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'currentMode=m\')>=0&&seg.indexOf(\'calculate();\')>=0;document.getElementById(\'__tbProbe\').textContent=\'EFFM0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['EFFM0 OK'],
  "ref": "第1339批·模式切换残留旧结果修复源码形态强锚：旧版 setMode 只切 currentMode/class/display 不重算，共用 #output 保留上一模式结论；修复后切换即调 calculate()。旧版无 ⇒ BAD。"
},
{
  "slug": 'science/chi-square-calculator',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/science/chi-square-calculator.html\',\'utf8\');var i=h.indexOf(\'function setMode(m){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'currentMode=m\')>=0&&seg.indexOf(\'calculate();\')>=0;document.getElementById(\'__tbProbe\').textContent=\'CHISQM0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['CHISQM0 OK'],
  "ref": "第1339批·模式切换残留旧结果修复源码形态强锚：旧版 setMode 只切 currentMode/class/display 不重算，共用 #output 保留上一模式结论；修复后切换即调 calculate()。旧版无 ⇒ BAD。"
},
{
  "slug": 'science/t-score-calculator',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/science/t-score-calculator.html\',\'utf8\');var i=h.indexOf(\'function setMode(m){\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+500):\'\';var ok=seg.indexOf(\'currentMode=m\')>=0&&seg.indexOf(\'calculate();\')>=0;document.getElementById(\'__tbProbe\').textContent=\'TSCM0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['TSCM0 OK'],
  "ref": "第1339批·模式切换残留旧结果修复源码形态强锚：旧版 setMode 只切 currentMode/class/display 不重算，共用 #output 保留上一模式结论；修复后切换即调 calculate()。旧版无 ⇒ BAD。"
},
{
  "slug": 'science/wire-gauge-converter',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/science/wire-gauge-converter.html\',\'utf8\');var i=h.indexOf(\'function setMode(\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+600):\'\';var ok=seg.indexOf(\'if(m===\\\'mm\\\') calcFromMm(); else if(m===\\\'mm2\\\') calcFromMm2(); else calcFromAwg();\')>=0;document.getElementById(\'__tbProbe\').textContent=\'WGM0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['WGM0 OK'],
  "ref": "第1340批·模式切换残留旧结果修复源码形态强锚：旧版 setMode 只切显示不重算，共用结果区保留上一模式结论；修复后切换即按新口径重算。旧版无 ⇒ BAD。"
},
{
  "slug": 'science/calculator',
  "clicks": ['(function(){var h=globalThis.__tbFs.readFileSync(process.cwd()+\'/\'+\'tools/science/calculator.html\',\'utf8\');var i=h.indexOf(\'function setMode(\');var j=h.indexOf(\'\\nfunction \',i+10);var seg=i>=0?h.slice(i,j>0?j:i+600):\'\';var ok=seg.indexOf(\'calculate();\')>=0;document.getElementById(\'__tbProbe\').textContent=\'CALCM0 \'+(ok?\'OK\':\'BAD\');})();'],
  "expect": ['CALCM0 OK'],
  "ref": "第1340批·模式切换残留旧结果修复源码形态强锚：旧版 setMode 只切显示不重算，共用结果区保留上一模式结论；修复后切换即按新口径重算。旧版无 ⇒ BAD。"
},
  {
    slug: "science/percentile-calculator",
    inputs: {},
    clicks: ["(function(){document.getElementById('data').value='<img src=x onerror=window.__xss=1>';calculate();var o=document.getElementById('output'),im=document.querySelector('#output img'),hasImg=im&&String(im.tagName).toUpperCase()==='IMG',ok=!hasImg&&!window.__xss&&o.innerHTML.indexOf('&lt;img')>=0&&o.innerHTML.indexOf('<img src')<0;document.getElementById('__tbProbe').textContent='PCTXSS '+(ok?'OK':'BAD');})()"],
    expect: ["PCTXSS OK"],
    ref: "非法数据项含 HTML 标签时，旧版把原始 token 直接拼进 innerHTML；现统一 __escHtml 转义，只显示纯文本、不生成 img 节点、不执行事件属性。默认无探针串 ⇒ 零逃生。",
  },
  {
    slug: "science/anova-calculator",
    inputs: {},
    clicks: ["(function(){document.getElementById('groups').value='<img src=x onerror=window.__xss=1>\\n5,6';calculate();var o=document.getElementById('output'),im=document.querySelector('#output img'),hasImg=im&&String(im.tagName).toUpperCase()==='IMG',ok=!hasImg&&!window.__xss&&o.innerHTML.indexOf('&lt;img')>=0&&o.innerHTML.indexOf('<img src')<0;document.getElementById('__tbProbe').textContent='ANOVAXSS '+(ok?'OK':'BAD');})()"],
    expect: ["ANOVAXSS OK"],
    ref: "方差分析组数据含标签时，解析错误整段经 __escHtml 输出；旧版 bad.error 直接入 innerHTML 会解析 img 并触发 onerror。",
  },
  {
    slug: "science/correlation-calculator",
    inputs: {},
    clicks: ["(function(){document.getElementById('xData').value='<img src=x onerror=window.__xss=1>';calculate();var o=document.getElementById('output'),im=document.querySelector('#output img'),hasImg=im&&String(im.tagName).toUpperCase()==='IMG',ok=!hasImg&&!window.__xss&&o.innerHTML.indexOf('&lt;img')>=0&&o.innerHTML.indexOf('<img src')<0;document.getElementById('__tbProbe').textContent='CORRXSS '+(ok?'OK':'BAD');})()"],
    expect: ["CORRXSS OK"],
    ref: "相关系数 X 数据含标签时，X/Y 解析错误合并后的 err 整段转义；旧版拼接 err 直接写 innerHTML。",
  },
  {
    slug: "science/p-value-calculator",
    inputs: {},
    clicks: ["setMode(2);document.getElementById('chi2').value='1000000';document.getElementById('df2').value='1000000';calculate();var o=String(document.getElementById('output').textContent||document.getElementById('output').innerHTML);var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/science/p-value-calculator.html','utf8');var ok=h.indexOf('if(!ok) return NaN')>=0&&h.indexOf('Wilson–Hilferty')>=0&&o.indexOf('Wilson–Hilferty')>=0;document.getElementById('chi2').value='CHIBIG '+(ok?'OK':'BAD');"],
    expect: ["CHIBIG OK"],
    ref: "大自由度卡方：gammp(500000,500000) 在 499 项内不收敛必须返回 NaN；chiSquareCDF(1e6,1e6) 应约 0.5（旧实现 0.739745），并明确标注 Wilson–Hilferty 近似。探针同时检查不收敛信号、中心值与说明文案。"
  },
  {
    slug: "science/chi-square-calculator",
    inputs: {},
    clicks: ["setMode(1);document.getElementById('chiIn').value='1000000';document.getElementById('dfIn').value='1000000';calculate();var o=String(document.getElementById('output').textContent||document.getElementById('output').innerHTML);var h=globalThis.__tbFs.readFileSync(process.cwd()+'/tools/science/chi-square-calculator.html','utf8');var ok=h.indexOf('if(!ok) return NaN')>=0&&h.indexOf('Wilson–Hilferty')>=0&&o.indexOf('Wilson–Hilferty')>=0;document.getElementById('chiIn').value='CHIBIG '+(ok?'OK':'BAD');"],
    expect: ["CHIBIG OK"],
    ref: "卡方工具大自由度：gammp(500000,500000) 499 项不收敛应返回 NaN；CDF(1e6,1e6) 约 0.5，并标注大自由度近似；旧实现给 0.739745。"
  },
  {
    slug: "science/chi-square-calculator",
    inputs: {},
    clicks: ["(function(){document.getElementById('obs').value='<img src=x onerror=window.__xss=1>';document.getElementById('exp').value='';calculate();var o=document.getElementById('output'),im=document.querySelector('#output img'),hasImg=im&&String(im.tagName).toUpperCase()==='IMG',ok=!hasImg&&!window.__xss&&o.innerHTML.indexOf('&lt;img')>=0&&o.innerHTML.indexOf('<img src')<0;document.getElementById('__tbProbe').textContent='CHIXSS '+(ok?'OK':'BAD');})()"],
    expect: ["CHIXSS OK"],
    ref: "卡方观察频数含标签时，观察/期望频数错误均经 __escHtml 输出；旧版两处 error 直接拼 innerHTML。",
  },
  {
    slug: "science/latlon-utm-converter",
    inputs: {},
    clicks: ["document.getElementById('utmZone').value='31';document.getElementById('utmHemisphere').value='N';document.getElementById('utmEasting').value='174541.329';document.getElementById('utmNorthing').value='1439053.593';convertUTM2LL()"],
    expect: ["13°00'00.00"],
    ref: "UTM 反算 DMS 进位：上述坐标反算纬度 12.999999°，秒数 59.999964″ 四舍五入后必须进为 13°00'00.00″，不得出现 60.00″。",
  },
  {
    slug: "science/latlon-utm-converter",
    inputs: {},
    clicks: ["document.getElementById('utmZone').value='31';document.getElementById('utmHemisphere').value='N';document.getElementById('utmEasting').value='500000';document.getElementById('utmNorthing').value='9430000';convertUTM2LL()"],
    expect: ["超出 UTM 标准投影范围"],
    ref: "UTM 反算适用范围：该坐标反算纬度约 84.91°，虽在 ±90° 合法经纬度内，但已超出 UTM 标准投影 -80°~84°；旧版只查 ±90° 会输出不可用坐标，现拒绝并提示改用 UPS。",
  },
  {
    slug: "science/astronomy-toolkit",
    inputs: {},
    clicks: ["document.getElementById('utmZone').value='31';document.getElementById('utmHemisphere').value='N';document.getElementById('utmEasting').value='500000';document.getElementById('utmNorthing').value='9430000';convertUTMToLatLon()"],
    expect: ["超出 UTM 标准投影范围"],
    ref: "天文工具箱 UTM 反算同样须检查 -80°~84°：84.91° 虽未超 ±90° 也不应返回 UTM 坐标，现提示极区改用 UPS。",
  },

  {
    slug: "science/geo-distance-calculator",
    inputs: { lat1: "0", lon1: "0", lat2: "0", lon2: "180" },
    clicks: ["calculate()"],
    expect: ["20015.09", "对跖点：方位无唯一解"],
    ref: "对跖点浮点边界：Haversine 的 a 可能因浮点误差略大于 1，旧版 sqrt(1−a)=NaN 使公里/英里/海里全变 NaN；现 clamp a∈[0,1] 后仍得 6371×π=20015.09 km。对跖点初始方位无唯一解，显示 — 并注明原因，不再误报正东 90°。默认北京→上海不命中。",
  },

  {
    slug: "science/pendulum-period",
    inputs: {},
    clicks: ["document.getElementById('L').value='0.0001';document.getElementById('g').value='9.80665';calcTool();var sw=__pdprSweep();var u=sw.labels.every(function(v,i){return i===0||v!==sw.labels[i-1]});var ok=sw&&u&&sw.dT.every(function(v){return isFinite(v)&&v>0;});document.getElementById('__tbProbe').textContent='PDSMALL '+(ok?'OK':'BAD '+sw.labels.join(','));"],
    expect: ["PDSMALL OK"],
    ref: "小尺度摆长 L=0.0001 m：采样标签须随量级保留有效数字（0.00002/0.000036/…，旧版统一 round 到 0.001 会全部变 0），曲线数据须保留完整精度（T≈0.009 s，不能舍入成 0）。默认 L=1 m 不命中。",
  },
  {
    slug: "science/pendulum-period",
    inputs: {},
    clicks: ["document.getElementById('L').value='1';calcTool();document.getElementById('L').value='0';calcTool();var c=document.getElementById('pdprChart');document.getElementById('__tbProbe').textContent='PDE '+(String(c.innerHTML||c.textContent||c.innerText||'').indexOf('请输入有效参数后再绘制曲线')>=0?'OK':'BAD '+String(c.innerHTML||c.textContent||c.innerText||'').slice(0,40));"],
    expect: ["PDE OK"],
    ref: "先以 L=1 画出曲线，再把 L 改为 0：旧版 __pdprChart 在 __pdprSweep 返回 null 时直接 return，旧曲线继续显示；现清空图表容器并提示「请输入有效参数后再绘制曲线」。",
  },
  {
    slug: "science/spring-oscillation-period",
    inputs: {},
    clicks: ["document.getElementById('m').value='0.0001';document.getElementById('k').value='0.0001';calcTool();var sw=__sospSweep();var u=sw.labels.every(function(v,i){return i===0||v!==sw.labels[i-1]});var ok=sw&&u&&sw.dT.every(function(v){return isFinite(v)&&v>0;});document.getElementById('__tbProbe').textContent='SOSMALL '+(ok?'OK':'BAD '+sw.labels.join(','));"],
    expect: ["SOSMALL OK"],
    ref: "小尺度刚度 k=0.0001 N/m：采样标签须为 0.00002/0.000036/…（旧版 round 到 0.01 会全部变 0），周期数据保留完整精度（T≈14.05 s），不得被固定四位小数截断。",
  },
  {
    slug: "science/spring-oscillation-period",
    inputs: {},
    clicks: ["document.getElementById('m').value='1';calcTool();document.getElementById('m').value='0';calcTool();var c=document.getElementById('sospChart');document.getElementById('__tbProbe').textContent='SOSE '+(String(c.innerHTML||c.textContent||c.innerText||'').indexOf('请输入有效参数后再绘制曲线')>=0?'OK':'BAD '+String(c.innerHTML||c.textContent||c.innerText||'').slice(0,40));"],
    expect: ["SOSE OK"],
    ref: "质量由 1 改为 0：旧版曲线生成提前 return，旧曲线残留；现清空图表容器并提示。",
  },

  {
    slug: "science/matrix-calculator",
    inputs: {},
    clicks: ["var a=fmt(0.001234567),b=fmt(999999.9999),c=fmt(1e-4);var ok=a==='0.001234567'&&b==='999999.9999'&&c==='1.000000e-4';document.getElementById('__tbProbe').textContent='MATFMT '+(ok?'OK':'BAD '+a+' / '+b+' / '+c);"],
    expect: ["MATFMT OK"],
    ref: "普通量级数值显示精度：旧版 round 到 1e-10 后调用无参 toLocaleString，默认最多 3 位小数 ⇒ 0.001234567 显示成 0.001、999999.9999 也丢尾部精度。现按 10 位有效数字取最短十进制：0.001234567 / 999999.9999；小于 1e-3 仍走 6 位科学计数 1.000000e-4。",
  },
  {
    slug: "science/physics-calculator",
    inputs: {},
    clicks: ["var a=fmt(0.001234567),b=fmt(999999.9999),c=fmt(1e-4);var ok=a==='0.001234567'&&b==='999999.9999'&&c==='1.000000e-4';document.getElementById('__tbProbe').textContent='PHYFMT '+(ok?'OK':'BAD '+a+' / '+b+' / '+c);"],
    expect: ["PHYFMT OK"],
    ref: "物理计算结果同口径：0.001234567 保留 10 位有效数字，不再被 toLocaleString 默认 3 位小数压成 0.001；999999.9999 不丢尾数；1e-4 仍用科学计数。",
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

  console.log("==== science calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();