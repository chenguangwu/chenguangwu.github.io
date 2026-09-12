#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""science 分类的「📐 计算公式 / 原理」数据（供通用 scripts/fix_formula.py 消费）。

条目形态：
  {'eq': '公式', 'desc': '依据/口径说明'}                  —— A 无框插入 / B 缺 desc 补齐
  {'desc': ...}                                            —— 仅补 desc（非计算类给口径说明）
  {'eq': ..., 'desc': ..., 'force_eq': True}               —— 页面已有 eq 但错误/空泛，强制替换
  {'eq': ..., 'desc': ..., 'title': ...}                   —— 顺带规范 formula-title

覆盖 39 处：无框 25 / 空壳 3 / 错公式 1 / eq 套话 2 / desc 套话 1 / 缺 desc 5 / eq 空泛 2。
刻意不改：遗留真实写法（<h4>+<div class="formula">+变量说明，内容真实）共 14 页 —— 参照
finance/cpf-validator 先例（写法不同但内容真实即非缺口），如 battery-life-calculator、
ohms-law-calculator、pcb-trace-width、ph-calculator、rc-time-constant、voltage-divider-calculator、
wire-gauge-converter、heat-transfer-calculator、astro-geo-calculator、wavelength-to-rgb 等。
"""

TITLE_CALC = '📐 计算公式 / 原理'

MAP = {
    # ───────── A 类：无 formula-box 元素（25） ─────────
    'anova-calculator': {
        'eq': 'F = MS<sub>组间</sub> / MS<sub>组内</sub>，MS = SS/df',
        'desc': '单因素方差分析：组间均方与组内均方之比服从 F 分布，df₁ = k−1、df₂ = N−k；'
                'F 越大说明各组均值差异越显著（配合 p 值判断）。',
    },
    'chemistry-calculator': {
        'eq': 'n = m/M　c = n/V　pH = −log₁₀[H⁺]　PV = nRT (R=8.314 J·mol⁻¹·K⁻¹)',
        'desc': '化学计算器按上述基本关系分别处理摩尔质量、溶液浓度、酸碱度与理想气体状态；'
                '计算时需先统一为 SI 单位（质量 g、体积 L、温度 K）。',
    },
    'chi-square-calculator': {
        'eq': 'χ² = Σ (Oᵢ − Eᵢ)² / Eᵢ',
        'desc': '卡方统计量度量观测频数 O 与期望频数 E 的偏离程度；df 由表格维度决定'
                '（拟合优度 df=k−1，独立性检验 df=(r−1)(c−1)），再查卡方分布得 p 值。',
    },
    'effect-size-calculator': {
        'eq': "Cohen's d = (M₁ − M₂) / SD<sub>pooled</sub>",
        'desc': '效应量衡量两组均值差异的实际大小：SD_pooled = √[((n₁−1)s₁² + (n₂−1)s₂²)/(n₁+n₂−2)]。'
                'd≈0.2 小、0.5 中、0.8 大；与样本量无关，可跨研究比较。',
    },
    'equation-balancer': {
        'eq': 'Σ vᵢ·E(反应物) = Σ vᵢ·E(生成物)，每种元素守恒',
        'desc': '配平即求解线性方程组：为每种元素列出原子守恒方程，求最小正整数系数解；'
                '系数比唯一（或成整数倍）时方程式可配平，否则报错提示无法配平。',
    },
    'fraction-calculator': {
        'eq': 'a/b ± c/d = (ad ± bc)/bd　(a/b)×(c/d) = ac/bd　(a/b)÷(c/d) = ad/bc',
        'desc': '分数四则运算的通分/约分规则，结果自动约分为最简分数，并可导出带分数或小数形式。',
    },
    'latlon-utm-converter': {
        'eq': 'E = k₀·N·[A + (1−T+C)A³/6 + …]，N = k₀·[M + N·tanφ·(A²/2 + …)]',
        'desc': 'WGS84 椭球横轴墨卡托投影：k₀=0.9996、长半轴 a=6378137 m、扁率 f=1/298.257223563，'
                '结果换算到指定 UTM 带（每带 6°），北半球/南半球以 0/10000000 m 为假北偏移。',
    },
    'logic-gate-simulator': {
        'eq': 'AND: Y = A·B　OR: Y = A+B　NOT: Y = Ā　XOR: Y = A⊕B',
        'desc': '按布尔代数真值表逐门求值：AND 全 1 才输出 1、OR 有 1 即输出 1、NOT 取反、'
                'XOR 相异输出 1；多级电路按拓扑顺序依次传播信号。',
    },
    'matrix-calculator': {
        'eq': '(AB)<sub>ij</sub> = Σ<sub>k</sub> A<sub>ik</sub>B<sub>kj</sub>　det(A) 按余子式展开',
        'desc': '支持加减、乘法、数乘、转置、行列式与逆矩阵；乘法的前提是前列数等于后行数，'
                '逆矩阵仅在行列式非零（可逆）时存在。',
    },
    'p-value-calculator': {
        'eq': 'z = (x̄ − μ₀)/(σ/√n)　t = (x̄ − μ₀)/(s/√n)',
        'desc': '按检验类型把统计量换算为 p 值：z 检验查标准正态、t 检验查 t 分布（df=n−1）、'
                '卡方检验查 χ² 分布；支持单尾/双尾，p 小于显著性水平即拒绝原假设。',
    },
    'passphrase-generator': {
        'eq': '熵 ≈ n · log₂(W)（bit）',
        'desc': '口令强度用熵度量：n 为词数、W 为词表大小（如 7776 词）。'
                '叠加大小写变换、数字与符号替换会进一步提高熵，但需按实际可选集重新估算。',
    },
    'periodic-table': {
        'desc': '元素周期表：按 IUPAC 2021 标准收录 118 种元素，给出原子序数、相对原子质量、'
                '电子构型、电负性、熔沸点与常见氧化态；支持按名称/符号检索与按类别筛选。',
        'title': TITLE_CALC,
    },
    'physics-calculator': {
        'eq': 'F = ma　W = Fs·cosθ　E<sub>k</sub> = ½mv²　E<sub>p</sub> = mgh',
        'desc': '按所选物理量套用对应公式：牛顿第二定律求合力、功与功率、动能与势能、'
                '动量与冲量等；输入需统一为 SI 单位。',
    },
    'pi-digits': {
        'eq': 'π/4 = 4·arctan(1/5) − arctan(1/239)（Machin 公式）',
        'desc': '圆周率按 Machin 类反正切级数高精度计算并按需截取位数；可检索数字串在 π 中的'
                '首次出现位置（如生日、编号）。',
    },
    'prime-number': {
        'eq': 'n 为素数 ⇔ n>1 且不存在 p ∈ [2, √n] 使 p | n',
        'desc': '素性判定采用试除到 √n（辅以小素数预筛与 6k±1 步进加速）；'
                '区间筛法用埃拉托斯特尼筛列出范围内的全部素数。',
    },
    'probability-calculator': {
        'eq': 'P(a<X<b) = Φ((b−μ)/σ) − Φ((a−μ)/σ)',
        'desc': '正态分布概率按标准正态累积分布 Φ 求区间概率；二项/泊松等分布按各自概率质量函数'
                '累加，二项分布在 n 较大时可用正态近似。',
    },
    'quadratic-equation': {
        'eq': 'x = (−b ± √(b² − 4ac)) / 2a',
        'desc': '二次方程求根公式，判别式 Δ = b²−4ac：Δ>0 两实根、Δ=0 重根、Δ<0 一对共轭复根；'
                'a=0 时退化为一次方程。',
    },
    'sample-size-calculator': {
        'eq': 'n₀ = z²·p(1−p)/e²　n = n₀ / [1 + (n₀−1)/N]',
        'desc': '比例估计的样本量：z 为置信水平对应分位数（95%→1.96）、p 为预期比例、e 为允许误差；'
                '有限总体 N 时按第二式做修正。',
    },
    'si-unit-converter': {
        'eq': '值<sub>目标</sub> = 值<sub>源</sub> × 10<sup>(指数<sub>源</sub> − 指数<sub>目标</sub>)</sup>',
        'desc': '国际单位制词头换算：以 10 的幂为基准（k=10³、m=10⁻³、μ=10⁻⁶ 等），'
                '换算等价于两端词头指数的差值；非十进制单位（时间、角度）单独按定义折算。',
    },
    'statistics-calculator': {
        'eq': 'x̄ = Σxᵢ/n　s² = Σ(xᵢ−x̄)²/(n−1)　s = √s²',
        'desc': '描述统计：均值、样本方差与标准差、极差、中位数与四分位数；'
                '样本方差用 n−1（贝塞尔校正）以保证无偏估计，总体方差用 N。',
    },
    't-score-calculator': {
        'eq': 't = (x̄ − μ₀)/(s/√n)（单样本）　t = (x − M)/SD（T 分数）',
        'desc': '把原始分数换算为 t 分数：心理学 T 分数以均值 50、标准差 10 为标尺（T = 50 + 10z）；'
                '统计检验的 t 统计量则按样本均值与标准误计算，df=n−1。',
    },
    'trigonometry-calculator': {
        'eq': 'sinθ = 对边/斜边　cosθ = 邻边/斜边　tanθ = 对边/邻边',
        'desc': '直角三角形边角关系与单位圆定义；支持 sin/cos/tan 及其反函数、双曲函数，'
                '角度与弧度可切换，反函数结果按象限给出主值。',
    },
    'vector-calculator': {
        'eq': 'A·B = Σaᵢbᵢ　|A| = √(Σaᵢ²)　A×B = (a₂b₃−a₃b₂, a₃b₁−a₁b₃, a₁b₂−a₂b₁)',
        'desc': '向量运算：点积得数量（可用于求夹角 cosθ = A·B/(|A||B|)）、叉积得垂直向量（三维）；'
                '加减与数乘按分量逐项计算。',
    },
    'z-score-calculator': {
        'eq': 'z = (x − μ) / σ',
        'desc': '标准分数表示某值距均值多少个标准差：z=0 为均值、±1 约覆盖 68%、±2 约 95%、'
                '±3 约 99.7%（正态分布下）；可按样本均值/标准差或给定 μ、σ 计算。',
    },

    # ───────── C 类：空壳框（仅 title，3） ─────────
    'convert-power': {
        'eq': '1 CGS 功率单位 = 10⁻⁷ W　1 hp = 745.7 W　1 卡/秒 = 4.184 W',
        'desc': '按类别（力/能量/功率/压力等）在 SI 与常用单位之间换算：'
                '先归一到该类别的基本单位再折算，非十进制单位（如马力、卡）按定义系数换算。',
        'title': TITLE_CALC,
    },
    'resistor-color-code': {
        'eq': '4 环：R = (10·d₁ + d₂) × 10<sup>m</sup> Ω，容差 ±d₄　'
              '5 环：R = (100·d₁ + 10·d₂ + d₃) × 10<sup>m</sup> Ω',
        'desc': '按色环读阻值：前几环为有效数字、次一环为乘数（10 的幂）、末环为容差；'
                '四环电阻±5%/±10%，五环电阻精度更高（如±1%）。金/银环也可表示 ×0.1、×0.01。',
        'title': TITLE_CALC,
    },
    'significant-figures': {
        'eq': '结果位数 ≤ 参与运算中有效数字最少者（乘除）/ 小数位最少者（加减）',
        'desc': '有效数字规则：非零数字与夹在中间的 0 有效、前导 0 无效、小数部分尾随 0 有效；'
                '乘除取最少有效位数、加减取最少小数位数，本项目按此给出规范化结果。',
        'title': TITLE_CALC,
    },

    # ───────── D 类：eq 错公式（1） ─────────
    'calc-1': {
        'eq': 'h = v₀t + ½gt²　落地速度 v = v₀ + gt',
        'desc': '匀加速自由落体：默认 g = 9.8 m/s²；开启空气阻力时按二次阻力模型数值求解，'
                '末速趋于终端速度。',
        'force_eq': True,
    },

    # ───────── E 类：eq 套话/空泛（2） ─────────
    'calc-stats': {
        'eq': 'x̄ = Σxᵢ/n　s² = Σ(xᵢ−x̄)²/(n−1)　s = √s²',
        'desc': '描述统计量：均值、样本方差（贝塞尔校正 n−1）与标准差，并给出极差、中位数、'
                '四分位数与直方图分箱；数据类型可选样本/总体。',
        'force_eq': True,
    },
    'xianxingfangchengzuqiujie-2yuan-3yuan': {
        'eq': 'Cramer 法则：xᵢ = det(Aᵢ)/det(A)（det(A) ≠ 0 时有唯一解）',
        'desc': '线性方程组求解：系数行列式非零时按 Cramer 法则或用高斯消元求唯一解；'
                '行列式为零时判定为无解或有无穷多解（系数成比例）。',
        'force_eq': True,
    },

    # ───────── F 类：desc 套话（1） ─────────
    'yiyuanercifangchengqiujie': {
        'desc': '一元二次方程 ax²+bx+c=0 求根：判别式 Δ=b²−4ac 决定根的性质'
                '（Δ>0 两实根、=0 重根、<0 共轭复根），结果同时给出顶点与对称轴。',
    },

    # ───────── G 类：有 eq 缺 desc（5） ─────────
    'correlation-calculator': {
        'desc': 'Pearson 相关系数 r ∈ [−1, 1]：衡量两个变量的线性相关程度与方向，'
                '并给 R² = r²（解释方差比例）；n<3 或任一方差为 0 时无法定义。',
    },
    'nth-root-calculator': {
        'desc': 'n 次方根 ⁿ√x = x^(1/n)：n 为奇数时负数亦有实根，n 为偶数时仅非负数有实根；'
                'n=0 无定义。',
    },
    'percentile-calculator': {
        'desc': '按线性插值法（R-7，与 Excel PERCENTILE.INC 一致）求分位数：'
                'pos = (n−1)·p，取相邻两数按小数部分加权；另给出 p 分位对应排名。',
    },
    'range-calculator': {
        'desc': '极差 = 最大值 − 最小值，是最简单的离散程度度量；同时输出均值、中位数与'
                '标准差便于对照（极差对异常值敏感）。',
    },
    'variance-calculator': {
        'desc': '总体方差用 N、样本方差用 n−1（贝塞尔校正）：样本方差是无偏估计，'
                'n=1 时无定义；同时输出标准差与均值。',
    },

    # ───────── H 类：eq 偏空泛（2） ─────────
    'meteor-crater-estimator': {
        'eq': 'D ≈ 1.161·(ρᵢ/ρₜ)<sup>1/3</sup>·L<sup>0.78</sup>·v<sup>0.44</sup>·g<sup>−0.22</sup>·sin<sup>1/3</sup>θ',
        'desc': '撞击坑标度律（π-scaling）：D 为坑径、L 为撞击体直径、v 为撞击速度、'
                'θ 为入射角、ρᵢ/ρₜ 为撞击体与靶体密度比；释放能量 E ≈ ½mv²。',
        'force_eq': True,
    },
    'provident-fund': {
        'eq': '月缴存额 = 缴存基数 × (单位比例 + 个人比例)　贷款额度 = f(账户余额, 基数)',
        'desc': '住房公积金测算：缴存基数通常有当地上下限，比例多在 5%–12%；'
                '贷款额度按当地"余额倍数 / 基数 / 房价比例"三项取最低，月供按等额本息计算。',
        'force_eq': True,
    },
}
