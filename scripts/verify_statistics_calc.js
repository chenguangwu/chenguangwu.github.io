#!/usr/bin/env node
/**
 * statistics 分类关键计算逻辑独立验证（收口批次 E，第 18 道门禁）。
 *
 * 复用 scripts/verify_it_calc.js 的 DOM stub 与 runCase 框架。
 * 期望值一律由页面公式独立复算得出，不取页面输出。
 *
 * 注意：statistics-4（置信区间）与 statistics-5（样本量）的逆正态 z 反解公式已于 2026-09-16 专项修复
 *      （原实现 cl=95 反解出 z≈0.0008，CI 退化为样本均值、样本量恒为 1；现改用 Acklam probit
 *      normalInv，cl=95 → z≈1.96、cl=99 → z≈2.576）。下方已补两页回归断言。
 *
 * 用法：
 *   node scripts/verify_statistics_calc.js
 *   node scripts/verify_statistics_calc.js z-score-calc t
 */
const { runCase } = require("./verify_it_calc.js");

const CASES = [
  // ── Z 分数（z = (x−μ)/σ）─────────────────────────────────────────
  {
    slug: "statistics/z-score-calc",
    inputs: { x: "130", mu: "110", sigma: "8" },
    expect: ["2.500"],
    ref: "z = (130−110)/8 = 2.500",
  },
  // ── 单样本 t 统计量（t = (x̄−μ₀)/(s/√n)）──────────────────────────
  {
    slug: "statistics/t",
    inputs: { xbar: "55", mu0: "50", s: "5", n: "16" },
    expect: ["4.0000", "15", "5.0000"],
    ref: "t = 5/(5/4) = 4.0000；df = 15；差值 = 5.0000",
  },
  // ── t 统计量（同 t，另一入口）────────────────────────────────────
  {
    slug: "statistics/t-score",
    inputs: { xbar: "110", mu: "100", s: "12", n: "36" },
    expect: ["5.000"],
    ref: "t = 10/(12/6) = 5.000",
  },
  // ── 变异系数（CV = σ/μ×100%）─────────────────────────────────────
  {
    slug: "statistics/coefficient-of-variation",
    inputs: { mu: "8", sigma: "3" },
    expect: ["37.50"],
    ref: "CV = 3/8×100 = 37.50%",
  },
  // ── 变异系数比较（两组 CV）───────────────────────────────────────
  {
    slug: "statistics/statistics-10",
    inputs: { mean1: "200", sd1: "30", mean2: "50", sd2: "4" },
    expect: ["15.00", "8.00"],
    ref: "CV_A = 30/200×100 = 15.00%；CV_B = 4/50×100 = 8.00%（A 更离散）",
  },
  // ── 加权平均数（Σvw/Σw）─────────────────────────────────────────
  {
    slug: "statistics/statistics-11",
    inputs: { v1: "70", w1: "0.2", v2: "85", w2: "0.3", v3: "95", w3: "0.5" },
    expect: ["87.0000"],
    ref: "x̄_w = (70×0.2+85×0.3+95×0.5)/1.0 = 87.0/1 = 87.0000",
  },
  // ── 均值标准误（SE = σ/√n）───────────────────────────────────────
  {
    slug: "statistics/standard-error",
    inputs: { sigma: "24", n: "16" },
    expect: ["6.0000"],
    ref: "SE = 24/√16 = 24/4 = 6.0000",
  },
  // ── 比例标准误（SE = √[p(1−p)/n]）───────────────────────────────
  {
    slug: "statistics/standard-error-proportion",
    inputs: { p: "0.2", n: "100" },
    expect: ["0.0400"],
    ref: "SE = √(0.2×0.8/100) = √0.0016 = 0.0400",
  },
  // ── 对立事件概率（1 − P(A)）──────────────────────────────────────
  {
    slug: "statistics/probability-complement",
    inputs: { p: "0.65" },
    expect: ["0.3500"],
    ref: "P(Aᶜ) = 1 − 0.65 = 0.3500",
  },
  // ── 四分位距与异常值边界（Tukey 1.5×IQR）────────────────────────
  {
    slug: "statistics/iqr",
    inputs: { data_count: "8", min_: "5", q1: "20", median_: "35", q3: "50", max_: "80" },
    expect: ["30.0000", "-25.0000", "95.0000"],
    ref: "IQR = 50−20 = 30；下限 = 20−1.5×30 = -25.0000；上限 = 50+1.5×30 = 95.0000；中位数 = 35",
  },
  // ── 正态区间概率（Φ((b−μ)/σ) − Φ((a−μ)/σ)）──────────────────────
  {
    slug: "statistics/statistics",
    inputs: { mu: "10", sigma: "2", a: "6", b: "14" },
    expect: ["95.450", "4.550"],
    ref: "z = ±2；P = [Φ(2) − Φ(−2)]×100 = 95.450%；区间外 = 4.550%",
  },
  // ── 二项 PMF（P(X=k) = C(n,k)pᵏ(1−p)^(n−k)）─────────────────────
  {
    slug: "statistics/binomial-pmf",
    inputs: { n: "12", k: "4", p: "0.5" },
    expect: ["0.12085", "495"],
    ref: "C(12,4) = 495；P(X=4) = 495×0.5^12 = 495/4096 = 0.12085",
  },
  // ── 二项 CDF（P(X≤x)）───────────────────────────────────────────
  {
    slug: "statistics/binomial-cdf",
    inputs: { n: "10", p: "0.5", x: "3" },
    expect: ["0.1719"],
    ref: "P(X≤3) = (C(10,0)+…+C(10,3))/2^10 = 176/1024 = 0.1719",
  },
  // ── 标准正态 CDF（Φ(z)）─────────────────────────────────────────
  {
    slug: "statistics/normal-cdf",
    inputs: { z: "2" },
    expect: ["0.97725", "2.275"],
    ref: "Φ(2) = 0.97725；右尾 = (1−Φ)×100 = 2.275%",
  },
  // ── 泊松 PMF（P(X=k) = e^−λ·λᵏ/k!）─────────────────────────────
  {
    slug: "statistics/poisson-pmf",
    inputs: { lam: "3", k: "2" },
    expect: ["0.22404"],
    ref: "P(X=2) = e^−3×3²/2! = 0.22404",
  },
  // ── 百分等级（低于数 + 0.5×等于数）/n ───────────────────────────
  {
    slug: "statistics/percentile-rank",
    inputs: { data: "50,60,70,80,90", val: "70" },
    expect: ["50.00"],
    ref: "低于 70 的 2 个、等于 1 个 → (2+0.5)/5×100 = 50.00%",
  },
  // ── 比例置信区间（p̂ ± z√(p̂(1−p̂)/n)）───────────────────────────
  {
    slug: "statistics/confidence-proportion",
    inputs: { x: "45", n: "150", z: "1.96" },
    expect: ["0.3000", "0.2267", "0.3733"],
    ref: "p̂ = 0.3000；SE = √(0.3×0.7/150) = 0.03742；CI = 0.3000 ± 1.96×0.03742 = [0.2267, 0.3733]",
  },
  // ── 均值样本量（n = ⌈(zσ/e)²⌉）──────────────────────────────────
  {
    slug: "statistics/sample-size-mean",
    inputs: { sigma: "20", e: "4", z: "2.576" },
    expect: ["166", "165.9"],
    ref: "n = (2.576×20/4)² = 165.89 → 向上取整 166",
  },
  // ── 比例样本量（n = ⌈z²p(1−p)/e²⌉）─────────────────────────────
  {
    slug: "statistics/sample-size-proportion",
    inputs: { p: "0.4", e: "0.04", z: "1.96" },
    expect: ["577", "576.2"],
    ref: "n = 1.96²×0.4×0.6/0.04² = 576.24 → 向上取整 577",
  },
  // ── 相对风险（RR = [a/(a+b)]/[c/(c+d)]）─────────────────────────
  {
    slug: "statistics/relative-risk",
    inputs: { a: "30", b: "70", c: "15", d: "85" },
    expect: ["0.3000", "0.1500"],
    ref: "暴露组 = 30/100 = 0.3000；非暴露组 = 15/100 = 0.1500；RR = 2.0000",
  },
  // ── 比值比（OR = ad/bc）─────────────────────────────────────────
  {
    slug: "statistics/odds-ratio",
    inputs: { a: "50", b: "50", c: "25", d: "75" },
    expect: ["3.0000", "0.3333"],
    ref: "OR = (50×75)/(50×25) = 3750/1250 = 3.0000；倒数 = 0.3333",
  },
  // ── 皮尔逊相关系数（r）──────────────────────────────────────────
  {
    slug: "statistics/correlation-coefficient",
    inputs: { x: "1,2,3,4", y: "2,4,6,9" },
    expect: ["0.9944", "0.9888"],
    ref: "r = Σ(x−x̄)(y−ȳ)/√(Σ(x−x̄)²Σ(y−ȳ)²) = 11.5/√(5.0×26.75) = 0.9944；r² = 0.9888",
  },
  // ── 均值/中位数/极差/总和（固定 7 个数据）───────────────────────
  {
    slug: "statistics/statistics-12",
    inputs: { n1: "5", n2: "8", n3: "12", n4: "15", n5: "18", n6: "22", n7: "25" },
    expect: ["15.0000", "15.0000", "20.0000", "105.0000"],
    ref: "均值 = 105/7 = 15.0000；升序第4个 = 15.0000；极差 = 25−5 = 20.0000；总和 = 105.0000",
  },
  // ── 标准差/方差/CV（固定 7 个数据，样本分母 n−1）────────────────
  {
    slug: "statistics/statistics-13",
    inputs: { n1: "1", n2: "2", n3: "3", n4: "4", n5: "5", n6: "6", n7: "7", type: "1" },
    expect: ["4.6667", "2.1602", "54.01"],
    ref: "均值 = 28/7 = 4.0；Σ(x−4)² = 28.0；样本方差 = 28.0/6 = 4.6667；标准差 = 2.1602；CV = 2.1602/4×100 = 54.01%（注：等差数列的离差平方和只与步长有关，故须改步长才能改变方差）",
  },
  // ── 偏度与超额峰度（总体矩）─────────────────────────────────────
  {
    slug: "statistics/statistics-7",
    inputs: { d1: "1", d2: "2", d3: "3", d4: "4", d5: "5", d6: "6", d7: "7", d8: "8", d9: "9", d10: "10" },
    expect: ["0.0000", "-1.2242"],
    ref: "均值 5.5；m₂ = 8.25、m₃ = 0.0、m₄ = 120.8625；偏度 = 0.0/8.25^1.5 = 0.0000；超额峰度 = 120.8625/8.25² − 3 = -1.2242"
       + "超额峰度 = 150.4257/6.09² − 3 = 1.0559",
  },
  // ── 单样本 t 检验（t、df、双侧 p）───────────────────────────────
  {
    slug: "statistics/one-sample-t-test",
    inputs: { xbar: "54", mu0: "50", sd: "8", n: "25" },
    expect: ["2.5000", "0.0197"],
    ref: "t = 4/(8/5) = 2.5000；df = 24；双侧 p = 2×(1−T_cdf(2.5000,24)) = 0.0197",
  },
  // ── 单样本 Z 检验（z = (x̄−μ₀)/(σ/√n)、双侧 p = 2(1−Φ(|z|))）─────
  {
    slug: "statistics/one-sample-z-test",
    inputs: { xbar: "103", mu0: "100", sigma: "10", n: "25" },
    expect: ["1.5000", "0.1336"],
    ref: "z = 3/(10/5) = 1.5000；双侧 p = 2×(1−Φ(1.5)) = 2×0.066807 = 0.1336（Python math.erf 独立复算）。原实现 p=2(1−erf(|z|/√2)) 得 0.2672，恰为正确值的 2 倍",
  },
  // ── F 方差齐性检验（F = s₁²/s₂²、双侧 p）───────────────────────
  {
    slug: "statistics/f-test-variance",
    inputs: { s1: "36", s2: "9", n1: "13", n2: "11" },
    expect: ["4.0000", "0.0357", "12", "10"],
    ref: "F = 36/9 = 4.0000；df = 12, 10；双侧 p = 2×P(F>4.0000) = 0.0357",
  },
  // ── 卡方检验（χ² = Σ(O−E)²/E）──────────────────────────────────
  {
    slug: "statistics/chi-square-test",
    inputs: { o: "30,25,45", e: "33,33,34" },
    expect: ["5.7709"],
    ref: "χ² = (30−33)²/33+(25−33)²/33+(45−34)²/34 = 5.7709；df = 3−1 = 2",
  },
  // ── 最小二乘回归拟合（a、b、预测）───────────────────────────────
  {
    slug: "statistics/statistics-16",
    inputs: { x1: "1", x2: "2", x3: "3", x4: "4", x5: "5", y1: "3", y2: "5", y3: "6", y4: "9", y5: "11", xp: "6" },
    expect: ["2.0000", "0.8000", "12.8000"],
    ref: "n=5，Σx=15，Σy=34，Σx²=55，Σxy=122；a = (5×122−15×34)/(5×55−15²) = 2.0000；b = 0.8000；x=6 → ŷ = 12.8000"
       + "b = (30.6−2.06×15)/5 = −0.06；ŷ(6) = 2.06×6−0.06 = 12.3000",
  },
  // ── 几何平均数（乘积的 n 次根）──────────────────────────────────
  {
    slug: "statistics/geometric-mean",
    inputs: { data: "2,4,8" },
    expect: ["4.00000"],
    ref: "G = (2×4×8)^(1/3) = 64^(1/3) = 4.00000",
  },
  // ── 调和平均数（倒数均值之倒数）─────────────────────────────────
  {
    slug: "statistics/harmonic-mean",
    inputs: { data: "30,60,20" },
    expect: ["30.0000"],
    ref: "H = 3/(1/30+1/60+1/20) = 3/0.1 = 30.0000",
  },
  // ── 极差（max − min）────────────────────────────────────────────
  {
    slug: "statistics/range-stat",
    inputs: { xs: "5, 11, 3, 8, 14" },
    expect: ["11.00"],
    ref: "R = 14 − 3 = 11.00",
  },
  // ── 平均绝对偏差（MAD = Σ|xi−x̄|/n）─────────────────────────────
  {
    slug: "statistics/mean-absolute-deviation",
    inputs: { xs: "5, 11, 3, 8, 14" },
    expect: ["3.4400"],
    ref: "x̄ = 8.2；Σ|x−8.2| = 17.2；MAD = 17.2/5 = 3.4400",
  },
  // ── 样本方差（n−1 分母）─────────────────────────────────────────
  {
    slug: "statistics/variance-list",
    inputs: { xs: "5, 11, 3, 8, 14" },
    expect: ["19.7000"],
    ref: "x̄ = 8.2；Σ(x−8.2)² = 78.8；s² = 78.8/4 = 19.7000",
  },
  // ── 样本标准差 ──────────────────────────────────────────────────
  {
    slug: "statistics/stddev-list",
    inputs: { xs: "5, 11, 3, 8, 14" },
    expect: ["4.4385"],
    ref: "s = √(78.8/4) = 4.4385",
  },
  // ── 总体方差（N 分母）───────────────────────────────────────────
  {
    slug: "statistics/population-variance",
    inputs: { data: "5,11,3,8,14" },
    expect: ["8.2000", "15.7600", "3.9699"],
    ref: "μ = 8.2000；σ² = 78.8/5 = 15.7600；σ = 3.9699",
  },
  // ── 样本方差（data 入口）────────────────────────────────────────
  {
    slug: "statistics/sample-variance",
    inputs: { data: "5,11,3,8,14" },
    expect: ["8.2000", "19.7000", "4.4385"],
    ref: "x̄ = 8.2000；s² = 78.8/4 = 19.7000；s = 4.4385",
  },
  // ── 均值置信区间（逆正态 z 反解，2026-09-16 专项修复）────────────
  {
    slug: "statistics/statistics-4",
    inputs: { xbar: "100", s: "12", n: "36", cl: "95" },
    expect: ["96.0801", "103.9199"],
    ref: "z = Φ⁻¹(0.975) = 1.95996；margin = 1.95996×12/√36 = 3.9199；CI = 100±3.9199",
  },
  // ── 样本量估计（均值/比例，逆正态 z 反解，2026-09-16 专项修复）──
  {
    slug: "statistics/statistics-5",
    inputs: { me: "0.04", cl: "95", sigma: "0.48", p: "0.36" },
    expect: ["554"],
    ref: "z = 1.95996；n_mean = (1.95996×0.48/0.04)² = 553.17；n_prop = 1.95996²×0.36×0.64/0.04² = 553.17；两者同为 554（σ²=p(1−p) 设计）",
  },  {
    slug: "statistics/cohens-d",
    inputs: {},
    clicks: ["document.getElementById('m1').value='31';document.getElementById('m2').value='27';calcTool();"],
    expect: ['0.8000 Cohen\'s d 大'],
    ref: 's1=s2=5、n1=n2=20 ⇒ 合并标准差 sp = √(((20−1)×25+(20−1)×25)/38) = **5**；d = (31−27)/5 = **0.8000**。强度判读 `|d|<0.8?\'中\':\'大\'`：0.8 不满足 `<0.8` ⇒ 落 `大`，本条把「恰在边界上归上一档」钉住（若误写 `<=0.8` 会得「中」）。刻意用**数值+标签联合锚**（`0.8000 Cohen\'s d 大`）而非裸标签——「大 效应强度」单独出现会被例⑤例⑦以外的默认态之外的用例撞上，且裸标签不带被测数值。默认态 d=0.6000 中，锚不命中。',
  },
  {
    slug: "statistics/cohens-d",
    inputs: {},
    clicks: ["document.getElementById('m1').value='29.5';document.getElementById('m2').value='27';calcTool();"],
    expect: ['0.5000 Cohen\'s d 中'],
    ref: 'd = (29.5−27)/5 = **0.5000**；`|d|<0.5?\'小\':…` 不成立 ⇒ `中`。与上一条构成「0.5/0.8 两条边界各归上一档」的成对对照：任一条的边界比较符写反（`<` ↔ `<=`）都会被另一条抓。默认态 0.6000 中，`0.5000 Cohen\'s d 中` 不命中。',
  },
  {
    slug: "statistics/cohens-d",
    inputs: {},
    clicks: ["document.getElementById('m1').value='28';document.getElementById('m2').value='27';calcTool();"],
    expect: ['0.2000 Cohen\'s d 小'],
    ref: 'd = (28−27)/5 = **0.2000**；`|d|<0.2?\'极小\':…` 不成立 ⇒ `小`。三条边界例（0.2/0.5/0.8）合起来把 `极小→小→中→大` 的四档阶梯全数钉住。默认态 0.6000 中，锚不命中。',
  },
  {
    slug: "statistics/cohens-d",
    inputs: {},
    clicks: ["document.getElementById('m1').value='100';document.getElementById('m2').value='100';calcTool();"],
    expect: ['0.0000 Cohen\'s d 极小'],
    ref: '两组均值相等 ⇒ d = 0/5 = **0.0000**，`|d|<0.2` 成立 ⇒ `极小`。本条覆盖 d 恰为 0 的退化路径（分子为 0，不是 NaN），也是四档里唯一能取到「极小」的入口（其余档位都需要非零差）。`toFixed(4)` 的负零/取整分支一并覆盖。默认态 0.6000 中，锚不命中。',
  },
  {
    slug: "statistics/cohens-d",
    inputs: {},
    clicks: ["document.getElementById('m1').value='25';document.getElementById('m2').value='30';document.getElementById('s1').value='4';document.getElementById('s2').value='4';document.getElementById('n1').value='15';document.getElementById('n2').value='15';calcTool();"],
    expect: ['-1.2500 Cohen\'s d 大'],
    ref: 'sp = √(((15−1)×16+(15−1)×16)/28) = **4**；d = (25−30)/4 = **−1.2500**，`toFixed(4)` 保留负号。强度按 `Math.abs(d)` 判读：|−1.25| ≥ 0.8 ⇒ `大`，本条压住「负效应量取绝对值再分档」——若漏 abs 会把 −1.25 连环判成极小/小/中（三个 `<` 全命中）。默认态 0.6000 中，锚不命中。',
  },
  {
    slug: "statistics/cohens-d",
    inputs: {},
    clicks: ["document.getElementById('m1').value='20';document.getElementById('m2').value='15';document.getElementById('s1').value='3';document.getElementById('s2').value='7';document.getElementById('n1').value='10';document.getElementById('n2').value='30';calcTool();"],
    expect: ['0.7953 Cohen\'s d 中'],
    ref: '不等方差+不等样本量的加权合并：sp = √((9×9 + 29×49)/38) = √(1502/38) = √39.5263 = **6.286996**；d = 5/6.286996 = **0.795292** ⇒ `toFixed(4)` = 0.7953，|d| < 0.8 ⇒ `中`。本条压住合并方差的 `n−1` 加权（若误用 n 加权或漏 √，数值立刻偏离 0.7953）；0.7953 与 0.8 边界只差 0.005，分档错一档也会被数值锚暴露。默认态 0.6000，锚不命中。',
  },
  {
    slug: "statistics/linear-regression",
    inputs: {},
    clicks: ["document.getElementById(\'x\').value=\'1,2,3,4,5\';document.getElementById(\'y\').value=\'3,5,7,9,11\';calcTool();"],
    expect: ['1.0000 截距 a', '2.0000 斜率 b', '7.000 x=3 预测 y'],
    ref: '完美直线 y=2x+1：x̄=3、ȳ=7，num=Σ(x−x̄)(y−ȳ)=10、den=Σ(x−x̄)²=10 ⇒ b=**2.0000**、a=7−2×3=**1.0000**、预测 y(3)=1+6=**7.000**。斜率恰为整数、截距恰为 1，任何一处 Σ 漏项/除错都会偏离；三条锚分别是「截距」「斜率」「外推」，数值+标签联合形态。默认态（1..5 / 2,4,5,4,5）是 2.2000 / 0.6000 / 4.000，全不命中。',
  },
  {
    slug: "statistics/linear-regression",
    inputs: {},
    clicks: ["document.getElementById(\'x\').value=\'0,1,2,3\';document.getElementById(\'y\').value=\'5,3,6,2\';calcTool();"],
    expect: ['4.9000 截距 a', '-0.6000 斜率 b', '3.100 x=3 预测 y'],
    ref: 'x̄=1.5、ȳ=4，num=(−1.5)(1)+(−0.5)(−1)+(0.5)(2)+(1.5)(−2)=−3、den=2.25+0.25+0.25+2.25=5 ⇒ b=**−0.6000**、a=4+0.6×1.5=**4.9000**、y(3)=4.9−1.8=**3.100**。x 从 0 起排（截距不再等于首项 y 值），负斜率同时覆盖 `toFixed(4)` 的负号渲染。默认态三条全不命中。',
  },
  {
    slug: "statistics/linear-regression",
    inputs: {},
    clicks: ["document.getElementById(\'x\').value=\'1,2,3\';document.getElementById(\'y\').value=\'2,4,6\';calcTool();"],
    expect: ['0.0000 截距 a', '6.000 x=3 预测 y'],
    ref: '过原点直线 y=2x：b=**2.0000**、a=4−2×2=**0.0000**（`toFixed(4)` 的零渲染）、y(3)=**6.000**。不锚 `2.0000 斜率 b`——它与例①的斜率同值（跨用例撞车无害但无判别力），改锚本条独有的截距与预测值。默认态 2.2000/0.6000/4.000，全不命中。',
  },
  {
    slug: "statistics/linear-regression",
    inputs: {},
    clicks: ["document.getElementById(\'x\').value=\'2,4,6,8\';document.getElementById(\'y\').value=\'1,1,1,1\';calcTool();"],
    expect: ['0.0000 斜率 b', '1.0000 截距 a'],
    ref: '水平线：ȳ=1 恒定 ⇒ num=Σ(x−x̄)×0=0 ⇒ b=**0.0000**、a=1−0=**1.0000**、y(3)=1.000。本条覆盖「斜率恰为零」的退化路径（den≠0、num=0），与例④共同构成 0/0 守卫之外的两种零形态；若把 b 写成 num/den 时 den 用错（如 n 而非 Σ(x−x̄)²），0.0000 仍成立但例①②会先抓，本条主要钉「num=0 ⇒ 截距=ȳ」这条链。默认态 0.6000，锚不命中。',
  },
  {
    slug: "statistics/linear-regression",
    inputs: {},
    clicks: ["document.getElementById(\'x\').value=\'5,3,1\';document.getElementById(\'y\').value=\'1,2,3\';calcTool();"],
    expect: ['3.5000 截距 a', '-0.5000 斜率 b'],
    ref: 'x 倒序输入（5,3,1）：x̄=3、ȳ=2，num=(2)(−1)+0+(−2)(1)=−4、den=8 ⇒ b=**−0.5000**、a=2+0.5×3=**3.5000**、y(3)=2.000。x 倒序验证 Σ(x−x̄)² 与顺序无关、num 符号由 x−x̄ 与 y−ȳ 的配对决定（若 den 误用 Σ(x−x̄) 而非平方，此处立刻为负 ⇒ NaN 守卫）。默认态全不命中。',
  },
  {
    slug: "statistics/linear-regression",
    inputs: {},
    clicks: ["document.getElementById(\'x\').value=\'1,2,3,4\';document.getElementById(\'y\').value=\'1,2,3\';calcTool();"],
    expect: ['1.0000 斜率 b', '3.000 x=3 预测 y'],
    ref: 'x 4 个、y 3 个 ⇒ `n=Math.min(xa.length,ya.length)=3`，只取前三对 (1,1)(2,2)(3,3) ⇒ b=**1.0000**、a=0、y(3)=**3.000**。本条钉住 `Math.min` 截断：若页面误用 xa.length(4)，ya[3] 为 undefined ⇒ NaN ⇒ 结果区落到「⚠ 计算结果含无效值」警告，三条锚全不出现 ⇒ 被抓。默认态（两串等长）不命中。',
  },

  // ── §7.4 零用例加固：statistics 确定性数值页（注入非默认 + harness 实测锚）──
  {
    slug: "statistics/z",
    inputs: { x: "92", mu: "80", sigma: "8" },
    expect: ["1.5000", "93.32 %", "1.50 σ"],
    ref: "注入非默认(默认 x=85/mu=75/sigma=10)：Z = (92−80)/8 = 1.5000；标准正态累积 ⇒ 百分位 93.32%；距均值 1.50σ。默认态 Z=1.0000/84.13%/1.00σ 均不命中。"
  },
  {
    slug: "statistics/paired-t-test",
    inputs: { dbar: "3.5", sd: "4", n: "20" },
    expect: ["3.9131", "19", "0.0009"],
    ref: "注入非默认(默认 2.5/3/15)：SE = 4/√20 = 0.8944 ⇒ t = 3.5/0.8944 = 3.9131；df = 20−1 = 19；双侧 p ≈ 0.0009。默认态 t=3.2275/df=14/p=0.0065 均不命中。"
  },
  {
    slug: "statistics/one-way-anova",
    inputs: { m1: "12", m2: "15", m3: "19", s1: "3", s2: "3", s3: "3", n1: "12", n2: "12", n3: "12" },
    expect: ["16.4444 F 统计量", "2, 33"],
    ref: "注入非默认(默认 10/12/14，s=2，n=10)：总均值 = 15.333 ⇒ SSB = 12×[(12−15.333)²+(15−15.333)²+(19−15.333)²] = 296 ⇒ MSB = 148；MSW = 9（组内方差）⇒ F = 148/9 = 16.4444，自由度 (组间 2, 组内 33)。⚠ 不用 p 值作锚：默认组间差异也显著，p 同为极小值，四舍五入后易同形 ⇒ 改锚 F 与自由度串。默认态 F=10.0000/(2, 27) 不命中。"
  },
  {
    slug: "statistics/independent-t-test",
    inputs: { m1: "35", m2: "30", s1: "6", s2: "6", n1: "25", n2: "25" },
    expect: ["2.9463", "48", "0.0050"],
    ref: "注入非默认(默认 30/27，s=5，n=20)：pooled s² = 36 ⇒ SE = 6×√(1/25+1/25) = 1.6971 ⇒ t = 5/1.6971 = 2.9463；df = 25+25−2 = 48；双侧 p ≈ 0.0050。默认态 t=1.8974/df=38/p=0.0652 均不命中。"
  },
  {
    slug: "statistics/cramers-v",
    inputs: { a: "55", b: "45", c: "25", d: "75" },
    expect: ["18.7500", "0.3062"],
    ref: "注入非默认(默认 40/60/20/80)：N = 200；χ² = N(ad−bc)²/[(a+b)(c+d)(a+c)(b+d)] = 200×(4125−1125)²/(100×100×80×120) = 18.7500；Cramér's V = √(χ²/N) = √0.09375 = 0.3062。默认态 10.0000/0.2236 不命中。"
  },
  {
    slug: "statistics/pooled-variance",
    inputs: { n1: "15", s1: "3", n2: "18", s2: "4" },
    expect: ["12.839"],
    ref: "注入非默认(默认 n1=10/s1=2/n2=12/s2=3)：合并方差 s_p² = [(n1−1)s1² + (n2−1)s2²]/(n1+n2−2) = [(14×9)+(17×16)]/31 = (126+272)/31 = 12.839。默认态 6.650 不命中。"
  },

{
    "slug": "statistics/p",
    "inputs": {
      "z": "1.96"
    },
    "expect": [
      "双尾 p 值： 0.049996",
      "单尾 p 值： 0.024998"
    ],
    "ref": "标准正态分布 P 值：z = 1.96 时单尾 p = 1 − Φ(1.96) = 0.024998（Φ(1.96) = 0.975002），双尾 p = 2 × 0.024998 = 0.049996。页面输出与独立复算（误差函数法）吻合。HTML 默认 z=2.0 → 双尾 0.045500、单尾 0.022750，默认态不产生该组值。"
  },
  {
    "slug": "statistics/correlation-r-squared",
    "inputs": {
      "r": "0.85"
    },
    "expect": [
      "0.7225 决定系数 R²",
      "0.277500 未被解释的变异比例",
      "2.603604 决定优势比",
      "72.2500 解释力 (%)",
      "3.603604 方差膨胀因子 VIF"
    ],
    "ref": "r = 0.85 → R² = r² = 0.7225；未解释变异 = 1 − 0.7225 = 0.2775；决定优势比 = R²/(1−R²) = 0.7225/0.2775 = 2.603604；解释力 = R² × 100% = 72.25%；VIF = 1/(1−R²) = 1/0.2775 = 3.603604。页面输出与独立复算逐项吻合。HTML 默认 r=0.8 → R²=0.6400、优势比 1.777778，默认态不产生该组值。"
  }
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
      else { fails.push(c.slug); }
    } catch (e) {
      fails.push(c.slug);
    }
  }
  console.log("==== statistics calc " + pass + "/" + cases.length + " ====");
  if (fails.length) process.exit(1);
}
if (require.main === module) main();