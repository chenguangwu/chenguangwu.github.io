#!/usr/bin/env python3
"""science 分类 deep-dive 条数补齐（§4.1.3：scenarios>=2、faqs>=2）。

背景：science 99 个工具的 deep-dive 条目内容真实（非套话），但 scenarios / faqs
各仅 1 条，未达 §4.1.3 的条数门槛。本脚本为每个工具**追加** 1 条真实场景与
1 条真实 FAQ（不覆盖既有内容，按内容去重幂等）。

用法：
  python3 scripts/fix_science_deepdive.py --dry-run
  python3 scripts/fix_science_deepdive.py --apply
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")
IND = "science"

# slug -> {"sc": 追加场景, "faq": (问题, 答案)}
ADD = {
    "anova-calculator": {
        "sc": "判断多组实验条件（如不同温度下的反应产率）之间是否存在系统性差异。",
        "faq": ("需要多少样本量？", "每组一般建议不少于 5 个观测；组数越多、组间差异越小，需越大样本才能检出（可用 G*Power 一类方法估算）。"),
    },
    "astro-geo-calculator": {
        "sc": "教学或科普中快速核对地球、月球、太阳的常用物理量。",
        "faq": ("与 WGS84 椭球一致吗？", "该工具用球面近似（半径约 6371 km），高精度测绘需改用椭球模型。"),
    },
    "astronomy-toolkit": {
        "sc": "观测前估算目标天体是否落在肉眼或望远镜的可见范围内。",
        "faq": ("距离模数是什么？", "m−M=5·lg d−5，用于由视星等与距离推绝对星等（d 以 pc 计）。"),
    },
    "barcode-pharmacode": {
        "sc": "药盒印刷制版前生成产线扫描器可读取的单整数编码。",
        "faq": ("有校验位吗？", "没有。Pharmacode 不含校验位，依靠宽窄条间距容错，仅编码单个整数。"),
    },
    "battery-life-calculator": {
        "sc": "选型时比较不同容量电池在固定负载下的续航差异。",
        "faq": ("为何实测比计算短？", "温度、放电倍率、截止电压与自放电都会缩短实际时长（Peukert 效应）。"),
    },
    "calc-1": {
        "sc": "安全评估中估算高处坠物落地时间与冲击速度。",
        "faq": ("g 取多少？", "标准重力加速度 9.80665 m/s²，工程计算常取 9.8 或 10。"),
    },
    "calc-2": {
        "sc": "气缸压缩、气球升空等场景下由已知量求压强或体积。",
        "faq": ("真实气体偏差大吗？", "高压低温下偏差明显，需用范德华方程等真实气体模型修正。"),
    },
    "calc-4": {
        "sc": "用称重加排水法测不规则固体的密度。",
        "faq": ("空心会影响吗？", "会。含孔洞或空腔会使表观密度偏低，需先排除封闭空隙。"),
    },
    "calc-5": {
        "sc": "行程规划中按距离与限速估算所需耗时。",
        "faq": ("单位怎么统一？", "注意 km/h 与 m/s 的换算关系：1 m/s = 3.6 km/h。"),
    },
    "calc-cycle": {
        "sc": "配制溶液前由浓度、体积与摩尔质量计算所需质量。",
        "faq": ("结晶水算进去吗？", "要算。如 CuSO₄·5H₂O 需把 5 个结晶水计入摩尔质量。"),
    },
    "calc-distance": {
        "sc": "粗略估算两地直线距离，用于运费或行程初判。",
        "faq": ("地球半径取多少？", "平均半径约 6371 km；赤道半径 6378 km、极半径 6357 km。"),
    },
    "calc-stats": {
        "sc": "实验数据录入后快速得到均值与离散程度指标。",
        "faq": ("何时用样本标准差？", "当数据来自总体的抽样时，用 n−1 作分母得到无偏估计。"),
    },
    "calculator": {
        "sc": "课堂演算与工程现场快速计算复合表达式。",
        "faq": ("精度有多高？", "双精度浮点约 15–16 位有效数字，连续运算应避免逐步舍入误差。"),
    },
    "centripetal-force": {
        "sc": "估算车辆转弯或旋转机械所需向心力，用于结构强度校核。",
        "faq": ("离心力真实存在吗？", "在惯性参考系中不存在，那是转动参考系中的惯性效应。"),
    },
    "chemistry-calculator": {
        "sc": "配制标准溶液时由目标浓度反算所需质量或体积。",
        "faq": ("质量分数与摩尔浓度如何换算？", "质量分数按质量百分比计，换算需借助溶液密度。"),
    },
    "chi-square-calculator": {
        "sc": "遗传学中检验观测分离比是否符合孟德尔理论比例。",
        "faq": ("自由度怎么定？", "拟合优度检验 df=类别数−1；独立性检验 df=(行数−1)×(列数−1)。"),
    },
    "combination-calculator": {
        "sc": "抽奖选号或分组时计算不重复的组合总数。",
        "faq": ("允许重复怎么算？", "可重组合数为 C(n+r−1, r)。"),
    },
    "convert-power": {
        "sc": "核对电机或发动机铭牌在不同单位制下的参数。",
        "faq": ("瓦与伏安有何区别？", "交流中视在功率（VA）与有功功率（W）相差一个功率因数。"),
    },
    "correlation-calculator": {
        "sc": "分析两组测量数据之间的线性关联强度。",
        "faq": ("非线性关系怎么办？", "Pearson 只衡量线性关系，非线性可改用 Spearman 秩相关。"),
    },
    "coulomb-force": {
        "sc": "静电实验或带电粒子间作用力的量级估算。",
        "faq": ("介质有影响吗？", "有。公式中的 k 对应真空，介质中需除以相对介电常数 εr。"),
    },
    "cycle": {
        "sc": "查元素的相对原子质量与周期族位置，用于配平与性质推断。",
        "faq": ("表中的原子量是同位素吗？", "不是。表中为自然同位素丰度的加权平均值，单一同位素质量需另查。"),
    },
    "density-physics": {
        "sc": "通过密度对比初判材料真伪（如掺假金属密度偏低）。",
        "faq": ("常见单位怎么换算？", "1 g/cm³ = 1000 kg/m³。"),
    },
    "doppler-effect": {
        "sc": "解释救护车由远及近时警笛音调升高的现象。",
        "faq": ("光也有多普勒效应吗？", "有，但需用相对论公式处理，与声波公式不同。"),
    },
    "effect-size-calculator": {
        "sc": "元分析中把不同量纲的研究结果统一成可比效应量。",
        "faq": ("与 p 值有何区别？", "p 值受样本量影响大，效应量反映的是实际差异大小。"),
    },
    "electric-field-point": {
        "sc": "估算点电荷周围不同距离处的电场强度。",
        "faq": ("多个电荷怎么办？", "按叠加原理做矢量相加。"),
    },
    "equation-balancer": {
        "sc": "化学作业与工艺配比中快速配平反应式。",
        "faq": ("氧化还原反应也能配吗？", "可以，但复杂氧化还原建议用化合价升降或半反应法辅助校验。"),
    },
    "exp-calculator": {
        "sc": "复利增长、放射性衰变等指数模型的数值计算。",
        "faq": ("e 怎么定义？", "e = lim(n→∞)(1+1/n)ⁿ ≈ 2.71828，是无理数。"),
    },
    "factorial-calculator": {
        "sc": "排列组合与概率问题中计算分母的阶乘。",
        "faq": ("非整数阶乘怎么算？", "用 Gamma 函数推广：Γ(n+1) = n!。"),
    },
    "fibonacci": {
        "sc": "生成数列用于算法教学或分析自然界的比例现象。",
        "faq": ("递推式是什么？", "F(n)=F(n−1)+F(n−2)，通常取 F(1)=F(2)=1。"),
    },
    "fraction-calculator": {
        "sc": "配方比例与图纸尺寸中的分数运算与约分。",
        "faq": ("结果会自动约分吗？", "会自动按最大公约数化为最简分数。"),
    },
    "gcd-calculator": {
        "sc": "分数约分与齿轮齿数匹配时求最大公约数。",
        "faq": ("多个数怎么求？", "两两求 gcd 再与下一个数继续求即可。"),
    },
    "geo-distance-calculator": {
        "sc": "物流或旅行中估算两点间的地面直线距离。",
        "faq": ("与导航里程为何不同？", "这里算的是球面大圆距离，实际路程还包含道路绕行与地形起伏。"),
    },
    "gravitational-potential": {
        "sc": "水利工程或吊装作业中估算提升重物所需的能量。",
        "faq": ("远距离还用 mgh 吗？", "远距离需用万有引力势能 Ep=−GMm/r，近地小高度才可近似 mgh。"),
    },
    "heat-transfer-calculator": {
        "sc": "加热或冷却设备的热负荷与能耗估算。",
        "faq": ("比热容单位是什么？", "J/(kg·K)；水的比热容约 4186 J/(kg·K)。"),
    },
    "hookes-law": {
        "sc": "弹簧秤标定或弹性元件刚度设计中计算受力形变。",
        "faq": ("弹簧串并联刚度怎么算？", "串联 1/k=1/k₁+1/k₂，并联 k=k₁+k₂。"),
    },
    "kinetic-energy": {
        "sc": "估算车辆碰撞能量或刹车距离所需的动能。",
        "faq": ("接近光速还成立吗？", "不成立，高速时需用相对论动能公式，日常速度用 ½mv² 已足够。"),
    },
    "latlon-utm-converter": {
        "sc": "GIS 数据在不同坐标系之间转换以统一量算口径。",
        "faq": ("UTM 和经纬度哪个更好用？", "小范围内 UTM 便于按米量距；跨带使用时需换带，否则变形增大。"),
    },
    "lcm-calculator": {
        "sc": "齿轮啮合周期同步或分数通分时求最小公倍数。",
        "faq": ("多个数怎么求？", "两两求 lcm 再与下一个数继续求即可。"),
    },
    "led-resistor-calculator": {
        "sc": "Arduino 或单片机驱动 LED 时选取限流电阻。",
        "faq": ("电阻功率怎么选？", "P=I²R，建议按计算值留 2 倍以上余量，常用 1/4 W。"),
    },
    "log-calculator": {
        "sc": "分贝、pH、地震震级等对数尺度量的计算。",
        "faq": ("log 与 ln 有何区别？", "log 通常指以 10 为底的常用对数，ln 是以 e 为底的自然对数。"),
    },
    "logic-gate-simulator": {
        "sc": "数字电路入门时验证真值表与组合逻辑表达式。",
        "faq": ("各门的逻辑符号是什么？", "与用 ∧、或用 ∨、非用 ¬，异或用 ⊕。"),
    },
    "matrix-calculator": {
        "sc": "求解线性方程组或做线性变换的矩阵运算。",
        "faq": ("什么条件下可逆？", "必须是方阵且行列式不为零。"),
    },
    "mean-calculator": {
        "sc": "成绩单或测量数据快速求算术平均。",
        "faq": ("加权平均怎么算？", "各数值乘对应权重求和后，再除以权重之和。"),
    },
    "mechanical-power": {
        "sc": "机械输出功率估算与电机选型。",
        "faq": ("功率与扭矩什么关系？", "P=T·ω，其中 ω 为角速度（rad/s）。"),
    },
    "median-calculator": {
        "sc": "收入、房价等偏态分布数据中看典型水平。",
        "faq": ("中位数与均值差很大说明什么？", "说明分布偏斜或存在离群值，此时中位数更具代表性。"),
    },
    "meteor-crater-estimator": {
        "sc": "科普或行星地质研究中估算撞击坑的量级。",
        "faq": ("靶岩性质有影响吗？", "有。松散沉积层形成的坑径更大，坚硬基岩则相对较小。"),
    },
    "mode-calculator": {
        "sc": "问卷或销售数据中找出出现最频繁的类别。",
        "faq": ("数据都不重复怎么办？", "此时无众数；若全部值出现次数相同，也可视为全都是众数。"),
    },
    "molar-mass-calculator": {
        "sc": "化学计量与溶液配制中计算物质摩尔质量。",
        "faq": ("与分子量有何区别？", "数值相同，摩尔质量的单位是 g/mol。"),
    },
    "nato-phonetic": {
        "sc": "电话或无线电口述编号时避免同音字母听错。",
        "faq": ("数字怎么读？", "可用 Tree/Fower 等惯例读法，或直接逐个读数字。"),
    },
    "newtons-second": {
        "sc": "估算加速度、制动力或推进所需的合力。",
        "faq": ("变质量情况适用吗？", "不适用，火箭等变质量系统需用动量定理处理。"),
    },
    "nth-root-calculator": {
        "sc": "工程中开方求几何平均或做量纲还原。",
        "faq": ("与分数指数什么关系？", "ⁿ√a = a^(1/n)，二者等价。"),
    },
    "ohms-law-calculator": {
        "sc": "电路设计或故障排查中计算电流、压降与阻值。",
        "faq": ("非纯电阻电路适用吗？", "交流电路需改用阻抗 Z 计算，纯电阻才可直接用 R。"),
    },
    "p-value-calculator": {
        "sc": "科研中由 Z 或 t 统计量换算显著性水平。",
        "faq": ("单尾和双尾怎么选？", "取决于备择假设是否有方向；双侧检验的 p 值是单侧的两倍。"),
    },
    "passphrase-generator": {
        "sc": "为重要账户生成既好记又高强度的登录口令。",
        "faq": ("几个词才够安全？", "在常用词库下，4–6 个随机词通常即可达到 70 比特以上熵。"),
    },
    "pcb-trace-width": {
        "sc": "电源或大电流走线设计时确定铜箔线宽。",
        "faq": ("内层与外层有区别吗？", "有。内层散热条件差，同等电流需要更宽的线。"),
    },
    "pendulum-period": {
        "sc": "用单摆实验测量重力加速度或调校摆钟。",
        "faq": ("与摆球质量有关吗？", "无关。周期只取决于摆长与重力加速度（等时性）。"),
    },
    "percentile-calculator": {
        "sc": "成绩排名或体检指标的相对位置定位。",
        "faq": ("百分位数是什么含义？", "第 P 百分位表示有 P% 的数据小于或等于该值。"),
    },
    "periodic-table": {
        "sc": "化学教学与推理中查询元素的关键属性。",
        "faq": ("电负性有什么规律？", "同周期从左到右增大，同主族从上到下减小。"),
    },
    "permutation-calculator": {
        "sc": "密码位数与赛程排序等计较顺序的计数问题。",
        "faq": ("有重复元素怎么算？", "总数除以各重复元素个数的阶乘。"),
    },
    "ph-calculator": {
        "sc": "水质检测、土壤分析或实验室溶液的酸碱度计算。",
        "faq": ("温度会影响 pH 吗？", "会。Kw 随温度变化，中性点并非恒为 7。"),
    },
    "phone-lookup": {
        "sc": "判断陌生来电的大致归属地与运营商类型。",
        "faq": ("虚拟号段怎么识别？", "170/171 等属虚拟运营商号段，归属地信息仅供参考。"),
    },
    "phone-qr": {
        "sc": "在名片或海报上放二维码，扫码即可一键拨号。",
        "faq": ("兼容性如何？", "使用标准 tel: URI，主流扫码器均支持。"),
    },
    "physics-calculator": {
        "sc": "物理作业与实验数据的多公式速算。",
        "faq": ("矢量和标量要注意什么？", "矢量需考虑方向不能直接代数相加，标量可直接运算。"),
    },
    "pi-digits": {
        "sc": "教学演示或校验高精度算法输出。",
        "faq": ("有什么记忆方法？", "常用谐音口诀或按 5–10 位分组记忆。"),
    },
    "polar-day-night": {
        "sc": "旅行或摄影规划极昼、极夜出现的时段。",
        "faq": ("极昼能持续多久？", "极点附近约半年，纬度越高持续越长，极圈附近仅一天。"),
    },
    "power-calculator": {
        "sc": "快速计算幂、根与负指数。",
        "faq": ("0 的 0 次方等于几？", "数学上通常约定为 1，不同计算器实现可能不一致。"),
    },
    "prime-number": {
        "sc": "数论学习与密码学基础中的素数判定演示。",
        "faq": ("大数怎么判断？", "试除法只适合小数，大数用 Miller-Rabin 等概率算法。"),
    },
    "probability-calculator": {
        "sc": "游戏、抽奖与统计中的古典概率计算。",
        "faq": ("条件概率怎么算？", "P(A|B)=P(AB)/P(B)，要求 P(B)>0。"),
    },
    "projectile-range": {
        "sc": "体育投掷、弹道与抛体实验中估算射程与高度。",
        "faq": ("有空气阻力时差别大吗？", "实际射程会小于理论值，速度越高、弹体越轻差异越大。"),
    },
    "provident-fund": {
        "sc": "估算每月公积金缴存额与年度累积额度。",
        "faq": ("缴存比例范围是多少？", "一般为 5%–12%，具体上下限由各地住房公积金管理中心规定。"),
    },
    "quadratic-equation": {
        "sc": "抛物线零点与工程优化问题的求根计算。",
        "faq": ("韦达定理是什么？", "两根之和 x₁+x₂=−b/a，两根之积 x₁·x₂=c/a。"),
    },
    "quartile-calculator": {
        "sc": "绘制箱线图或分析数据分布形态。",
        "faq": ("四分位距有什么用？", "IQR=Q3−Q1，常以超出 1.5×IQR 作为离群值判据。"),
    },
    "range-calculator": {
        "sc": "质量控制中快速查看数据的波动幅度。",
        "faq": ("与标准差有何不同？", "极差只看最大值与最小值，标准差利用了全部数据。"),
    },
    "rc-time-constant": {
        "sc": "设计 RC 滤波、延时或按键去抖电路。",
        "faq": ("上升时间怎么估？", "从 10% 升到 90% 约需 2.2τ。"),
    },
    "resistor-color-code": {
        "sc": "维修或实验中由色环读出电阻阻值与公差。",
        "faq": ("色环方向怎么定？", "公差环（金或银色）位于末端，据此确定读数方向。"),
    },
    "rfc-validator": {
        "sc": "录入墨西哥客户或供应商税号前做格式校验。",
        "faq": ("个人与公司格式有区别吗？", "有。个人 RFC 为 13 位，公司为 12 位，均由字母与数字构成。"),
    },
    "root-calculator": {
        "sc": "几何平均、方差还原等需要开方的运算。",
        "faq": ("与幂运算什么关系？", "√a 等价于 a^0.5，可推广到任意次根 a^(1/n)。"),
    },
    "sample-size-calculator": {
        "sc": "问卷或实验设计前估算所需的最小样本量。",
        "faq": ("总体较小时要修正吗？", "要。用有限总体修正 n' = n/(1+(n−1)/N)。"),
    },
    "science-flow-rate": {
        "sc": "给排水与管道输送能力的流量估算。",
        "faq": ("层流和湍流怎么区分？", "按雷诺数 Re=ρvd/μ：Re<2000 为层流，Re>4000 为湍流。"),
    },
    "science-pressure-converter": {
        "sc": "把仪表读数在不同压力单位之间核对换算。",
        "faq": ("绝对压和表压有何区别？", "表压 = 绝对压 − 当地大气压。"),
    },
    "si-unit-converter": {
        "sc": "科研数据在不同数量级之间统一换算。",
        "faq": ("词头能连用吗？", "不能。如 kk 不合法，应写作 M（兆）。"),
    },
    "significant-figures": {
        "sc": "实验数据报出时确定合理的结果位数。",
        "faq": ("乘除怎么定位数？", "结果的有效数字位数取参与运算各数中位数最少者。"),
    },
    "spring-oscillation-period": {
        "sc": "弹簧振子实验或减振系统的周期估算。",
        "faq": ("与振幅有关吗？", "理想线性弹簧下与振幅无关，大振幅超出线性区后才会有偏差。"),
    },
    "star-magnitude-compare": {
        "sc": "天文观测前估算目标天体亮度与可见性。",
        "faq": ("视星等和绝对星等什么区别？", "视星等是实际观测亮度，绝对星等是归算到 10 pc 距离后的亮度。"),
    },
    "statistics-calculator": {
        "sc": "一站式得到描述统计量与常用检验统计量。",
        "faq": ("偏度为 0 就是正态吗？", "不一定，还需结合峰度与分布图综合判断。"),
    },
    "t-score-calculator": {
        "sc": "小样本均值检验与置信区间的计算。",
        "faq": ("配对样本怎么做？", "先求每对数据之差，再对差值序列做单样本 t 检验。"),
    },
    "text-extract-phones": {
        "sc": "从名片或网页文本中批量提取联系电话。",
        "faq": ("会误提取普通数字吗？", "有可能。工具按号段与位数规则匹配，结果建议人工复核。"),
    },
    "tide-height-estimator": {
        "sc": "海钓或赶海前估算潮位高低与时段。",
        "faq": ("大潮小潮怎么来的？", "朔望时日月引潮力叠加形成大潮，上弦与下弦前后形成小潮。"),
    },
    "torque-converter": {
        "sc": "机械装配时按力矩扳手要求换算扭矩单位。",
        "faq": ("扭矩与功率什么关系？", "P=T·ω，扭矩乘以角速度即为功率。"),
    },
    "trigonometry-calculator": {
        "sc": "工程测量与几何题中的边角关系计算。",
        "faq": ("反三角函数值域是多少？", "arcsin 主值 [−90°,90°]，arccos 主值 [0°,180°]，arctan 主值 (−90°,90°)。"),
    },
    "variance-calculator": {
        "sc": "质量一致性与投资风险波动性的分析。",
        "faq": ("为什么除以 n−1？", "为使样本方差成为总体方差的无偏估计（贝塞尔校正）。"),
    },
    "vector-calculator": {
        "sc": "力学分析与计算机图形学中的向量运算。",
        "faq": ("叉积有什么用？", "结果垂直于两向量，其模等于两向量张成的平行四边形面积。"),
    },
    "voltage-divider-calculator": {
        "sc": "分压取样电路与传感器偏置电路的设计。",
        "faq": ("分压电路耗电吗？", "耗电。分压电阻本身有持续电流，电池供电场景需注意静态功耗。"),
    },
    "wavelength-to-rgb": {
        "sc": "光谱实验或激光波长的视觉颜色预览。",
        "faq": ("显示器的颜色准吗？", "显示器 RGB 无法完全复现单色光谱色，仅作近似参考。"),
    },
    "wire-gauge-converter": {
        "sc": "布线选型时按 AWG 号对照线径与载流量。",
        "faq": ("载流量与敷设方式有关吗？", "有关。环境温度高、多线捆扎或穿管时都需要降额使用。"),
    },
    "work-done": {
        "sc": "起重、搬运等场景中估算力所做的功。",
        "faq": ("多个力做功怎么算？", "合外力做功等于各分力做功的代数和（含负功）。"),
    },
    "xianxingfangchengzuqiujie-2yuan-3yuan": {
        "sc": "解应用题（如鸡兔同笼）或电路节点方程。",
        "faq": ("用什么方法求解？", "消元法或代入法；当系数行列式不为零时有唯一解。"),
    },
    "yiyuanercifangchengqiujie": {
        "sc": "求抛物线与横轴交点及最优化问题的驻点。",
        "faq": ("能因式分解和用公式法一样快吗？", "能分解时更快，不能分解时直接用求根公式即可。"),
    },
    "z-score-calculator": {
        "sc": "成绩或体检指标的标准化比较与排名换算。",
        "faq": ("怎么得到概率？", "由 z 值查标准正态分布表得到累积概率 P(Z<z)。"),
    },
}


def load(path):
    return json.load(open(path, encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not (a.dry_run or a.apply):
        print("需指定 --dry-run 或 --apply")
        return 1

    dd = load(DD)
    changed = []
    skipped = []
    for slug, add in ADD.items():
        key = IND + "/" + slug
        entry = dd.get(key)
        if not entry:
            skipped.append((slug, "无 deep-dive 条目"))
            continue
        n_sc = n_fq = 0
        scs = entry.setdefault("scenarios", [])
        if add["sc"] not in scs:
            scs.append(add["sc"])
            n_sc = 1
        q, ans = add["faq"]
        faqs = entry.setdefault("faqs", [])
        if not any((f.get("q") == q) for f in faqs if isinstance(f, dict)):
            faqs.append({"q": q, "a": ans})
            n_fq = 1
        if n_sc or n_fq:
            changed.append((slug, len(entry.get("scenarios") or []), len(entry.get("faqs") or [])))

    print("目标工具: %d；本次补充: %d；跳过: %d" % (len(ADD), len(changed), len(skipped)))
    for slug, nsc, nfq in changed[:8]:
        print("  %-42s scenarios=%d faqs=%d" % (slug, nsc, nfq))
    if len(changed) > 8:
        print("  … 其余 %d 个" % (len(changed) - 8))
    for slug, why in skipped:
        print("  ⚠️ 跳过 %s：%s" % (slug, why))

    if a.dry_run:
        print("\n（dry-run，未写入；加 --apply 生效）")
        return 0

    json.dump(dd, open(DD, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n已写入 %s（indent=1）" % os.path.relpath(DD, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
