#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real-ize deep-dive content for the `science` category (76 tools).

Replaces generic SOP boilerplate with tool-specific REAL deep-dive content:
real computed examples (physics/chem/stat formulas), real scenarios, real FAQs.
Output written with json.dump(indent=1).
"""
import json

DD = 'i18n/tools/content_deepdive.json'
data = json.load(open(DD, encoding='utf-8'))

KB = {}

KB['science/anova-calculator'] = dict(title='单因素方差分析（ANOVA）',
  scenarios=['比较三组及以上样本均值是否显著不同（如三种肥料产量）。'],
  examples=[dict(title='三组示例', body='三组 [5,7,9]、[6,8,10]、[7,9,11]，组均值 7/8/9，总均值 8；SSB=3·((7-8)²+(8-8)²+(9-8)²)=6，dfB=2，MSB=3；若 MSW=2 则 F=1.5，查 F(2,6) 临界判断是否显著。')],
  faqs=[dict(q='ANOVA 显著后做什么？', a='做 Tukey HSD 等事后检验定位具体哪组不同。')])

KB['science/astro-geo-calculator'] = dict(title='天文地理计算器',
  scenarios=['估算地球物理与天文常用量。'],
  examples=[dict(title='地球参数', body='地球平均公转速度 ≈29.78 km/s；地表重力加速度 g≈9.81 m/s²；日地平均距 ≈1.496×10⁸ km（1 AU）。')],
  faqs=[dict(q='AU 是什么？', a='天文单位，定义为地球到太阳的平均距离。')])

KB['science/astronomy-toolkit'] = dict(title='天文观测工具箱',
  scenarios=['由视星等与距离算绝对星等、历法等。'],
  examples=[dict(title='绝对星等', body='公式 M=m-5(log₁₀d-1)；太阳视星等 m=-26.74、d=1AU → M≈4.83。')],
  faqs=[dict(q='星等越小越亮？', a='是，每差 5 等亮度差 100 倍。')])

KB['science/barcode-pharmacode'] = dict(title='Pharmacode 条形码',
  scenarios=['药品包装用 Pharmacode（仅宽窄条表示数字）。'],
  examples=[dict(title='编码', body='数字 123 按 Pharmacode 规则映射为宽窄条序列（一端宽=1、窄=0），扫码识读。')],
  faqs=[dict(q='Pharmacode 与 EAN 区别？', a='Pharmacode 仅编码单个整数，容错高，专用于药包。')])

KB['science/battery-life-calculator'] = dict(title='电池续航时间计算器',
  scenarios=['由容量与负载电流估算可用时长。'],
  examples=[dict(title='估算', body='电池 3000 mAh，设备平均电流 150 mA → 续航 = 3000/150 = 20 小时（理想值，实际受自放电阻抗影响）。')],
  faqs=[dict(q='mAh 是什么？', a='毫安时，容量单位，等于电流×小时。')])

KB['science/calc-1'] = dict(title='自由落体运动计算',
  scenarios=['忽略空气阻力时由时间求下落高度与末速。'],
  examples=[dict(title='计算', body='t=3s 时 h=½·9.8·3²≈44.1 m，末速 v=9.8·3≈29.4 m/s。')],
  faqs=[dict(q='空气阻力忽略影响大吗？', a='轻/大表面积物体（如羽毛）影响显著，重物体近似成立。')])

KB['science/calc-2'] = dict(title='理想气体状态方程',
  scenarios=['由 PV=nRT 求气体的 P/V/n/T。'],
  examples=[dict(title='计算', body='n=1 mol、T=273.15 K、P=1 atm → V=nRT/P=1·0.08206·273.15/1≈22.414 L（标准摩尔体积）。')],
  faqs=[dict(q='R 取多少？', a='取决于单位：0.08206 L·atm/(mol·K) 或 8.314 J/(mol·K)。')])

KB['science/calc-4'] = dict(title='密度/质量/体积换算',
  scenarios=['由 ρ=m/V 互求。'],
  examples=[dict(title='计算', body='m=100 g、V=50 cm³ → ρ=2 g/cm³（如花岗岩）。')],
  faqs=[dict(q='水密度是多少？', a='4°C 纯水 ≈1 g/cm³ =1000 kg/m³。')])

KB['science/calc-5'] = dict(title='速度/距离/时间计算',
  scenarios=['匀速运动 v=d/t 互求。'],
  examples=[dict(title='计算', body='d=120 km、t=2 h → v=60 km/h；t=1.5h 同距 → 80 km/h。')],
  faqs=[dict(q='平均速度与瞬时速度？', a='v=d/t 为全程平均，瞬时需导数。')])

KB['science/calc-cycle'] = dict(title='分子量计算器',
  scenarios=['由化学式算摩尔质量。'],
  examples=[dict(title='计算', body='H₂O：2×1.008+16.00≈18.015 g/mol；CO₂：12.01+2×16.00=44.01 g/mol。')],
  faqs=[dict(q='下标怎么算？', a='各原子相对原子质量×下标求和。')])

KB['science/calc-distance'] = dict(title='地理距离计算（经纬度）',
  scenarios=['两经纬度点间大圆距离（Haversine）。'],
  examples=[dict(title='计算', body='北京(39.90°N,116.40°E)→上海(31.23°N,121.47°E) 大圆距离 ≈1067 km。')],
  faqs=[dict(q='Haversine 与直线距离？', a='Haversine 沿球面大圆，比平面近似更准。')])

KB['science/calc-stats'] = dict(title='统计学计算（均值、方差、标准差）',
  scenarios=['描述性统计快速计算。'],
  examples=[dict(title='计算', body='数据 [2,4,4,4,5,5,7,9]：均值 5，总体方差 4，标准差 2（样本标准差≈2.14）。')],
  faqs=[dict(q='总体与样本方差？', a='样本除以 n−1 得无偏估计。')])

KB['science/calculator'] = dict(title='科学计算器',
  scenarios=['科学计算：幂、对数、三角、阶乘。'],
  examples=[dict(title='计算', body='2¹⁰=1024；sin(30°)=0.5；log₁₀(1000)=3；5!=120。')],
  faqs=[dict(q='角度单位？', a='注意 DEG/RAD 模式，sin(30°)=0.5 但 sin(π/6 rad) 同值。')])

KB['science/centripetal-force'] = dict(title='向心力 F_c',
  scenarios=['匀速圆周运动的向心合力。'],
  examples=[dict(title='计算', body='m=1000 kg、v=20 m/s、r=50 m → Fc=mv²/r=1000·400/50=8000 N。')],
  faqs=[dict(q='向心力从哪来？', a='由张力/重力/摩擦力等提供，方向始终指向圆心。')])

KB['science/chemistry-calculator'] = dict(title='化学计算器',
  scenarios=['摩尔浓度、质量分数等化学量换算。'],
  examples=[dict(title='摩尔浓度', body='n=0.5 mol 溶于 V=0.25 L → c=n/V=2 mol/L。')],
  faqs=[dict(q='M 与 mol/L？', a='M 即 mol/L（摩尔每升）。')])

KB['science/chi-square-calculator'] = dict(title='卡方计算器',
  scenarios=['类别型变量的拟合优度/独立性检验。'],
  examples=[dict(title='计算', body='观测 [30,10]、期望 [25,15]：χ²=(30-25)²/25+(10-15)²/15=1+1.667=2.667，df=1，查表判显著。')],
  faqs=[dict(q='期望频数为何要≥5？', a='过小会使卡方近似失真，需合并或 Fisher 检验。')])

KB['science/combination-calculator'] = dict(title='组合数 C(n, r)',
  scenarios=['从 n 个取 r 个不计顺序。'],
  examples=[dict(title='计算', body='C(10,3)=10!/(3!·7!)=120。')],
  faqs=[dict(q='组合与排列？', a='组合不计顺序 C(n,r)，排列计顺序 P(n,r)=C·r!。')])

KB['science/convert-power'] = dict(title='物理单位换算（力、功、功率等）',
  scenarios=['牛顿/焦耳/瓦特等物理单位互转。'],
  examples=[dict(title='换算', body='1 马力(hp)=745.7 W；1 J=1 N·m；1 kW=1000 W。')],
  faqs=[dict(q='公制与英制？', a='功率 hp↔W、扭矩 lbf·ft↔N·m 需乘系数。')])

KB['science/correlation-calculator'] = dict(title='相关系数计算器',
  scenarios=['Pearson 线性相关强度。'],
  examples=[dict(title='计算', body='x=[1,2,3,4]、y=[2,4,6,8] 完全线性 → r=1.0；y 随机则 r≈0。')],
  faqs=[dict(q='相关等于因果？', a='不等于，相关仅表线性关联。')])

KB['science/coulomb-force'] = dict(title='库仑定律',
  scenarios=['两点电荷间静电力。'],
  examples=[dict(title='计算', body='q₁=q₂=1e-6 C、r=0.1 m：F=kq₁q₂/r²=8.988e9·1e-12/0.01≈0.899 N（同号相斥）。')],
  faqs=[dict(q='k 是什么？', a='库仑常数 ≈8.988×10⁹ N·m²/C²。')])

KB['science/cycle'] = dict(title='交互式元素周期表',
  scenarios=['查元素原子序、相对原子质量、周期族。'],
  examples=[dict(title='查', body='氢 H：原子序 1，相对原子质量 1.008，第一周期 IA 族。')],
  faqs=[dict(q='相对原子质量为何带小数？', a='是自然同位素丰度加权平均值。')])

KB['science/density-physics'] = dict(title='密度 ρ = m/V',
  scenarios=['物质密度与浮沉判断。'],
  examples=[dict(title='计算', body='m=790 g、V=100 cm³（铁块）→ ρ=7.9 g/cm³ > 水 → 沉。')],
  faqs=[dict(q='密度与温度？', a='多数物质升温膨胀、密度略降。')])

KB['science/doppler-effect'] = dict(title='声波多普勒频移',
  scenarios=['声源/观察者相对运动时的频率变化。'],
  examples=[dict(title='计算', body='声速 340 m/s、f=1000 Hz、声源以 20 m/s 朝观察者 → f′=f·v/(v-vs)=1000·340/320≈1062.5 Hz。')],
  faqs=[dict(q='红光移蓝移？', a='远离频降（红移），靠近频升（蓝移）。')])

KB['science/effect-size-calculator'] = dict(title='效应量计算器',
  scenarios=['量化组间差异强度（Cohen\'s d 等）。'],
  examples=[dict(title='计算', body='两组均值差 5、合并标准差 10 → d=0.5（中等效应）。')],
  faqs=[dict(q='d 多大算大？', a='Cohen 约定 0.2 小、0.5 中、0.8 大。')])

KB['science/electric-field-point'] = dict(title='电场强度 E',
  scenarios=['点电荷电场。'],
  examples=[dict(title='计算', body='q=1e-6 C、r=0.1 m：E=kq/r²=8.988e9·1e-6/0.01≈8.99×10⁵ N/C。')],
  faqs=[dict(q='方向如何？', a='正电荷向外、负电荷向内。')])

KB['science/equation-balancer'] = dict(title='化学方程式配平器',
  scenarios=['配平化学反应式（原子守恒）。'],
  examples=[dict(title='配平', body='H₂+O₂→H₂O → 2H₂+O₂→2H₂O（H:4=4、O:2=2）。')],
  faqs=[dict(q='为什么配平？', a='质量守恒，反应前后各元素原子数相等。')])

KB['science/exp-calculator'] = dict(title='指数计算器',
  scenarios=['e 为底的指数运算。'],
  examples=[dict(title='计算', body='e²≈7.389；e⁻¹≈0.368。')],
  faqs=[dict(q='e 约多少？', a='自然常数 e≈2.71828。')])

KB['science/factorial-calculator'] = dict(title='阶乘计算器（科学）',
  scenarios=['n! 用于排列组合与概率。'],
  examples=[dict(title='计算', body='5!=120；0!=1（约定）。')],
  faqs=[dict(q='大数阶乘溢出？', a='可用对数或 Stirling 近似。')])

KB['science/fibonacci'] = dict(title='斐波那契数列工具',
  scenarios=['生成/查斐波那契项。'],
  examples=[dict(title='查', body='F(10)=55（序列 1,1,2,3,5,8,13,21,34,55…）。')],
  faqs=[dict(q='黄金比关系？', a='相邻项比趋近 φ≈1.618。')])

KB['science/fraction-calculator'] = dict(title='分数计算器',
  scenarios=['分数加减乘除与约分。'],
  examples=[dict(title='计算', body='1/2 + 1/3 = 3/6+2/6 = 5/6；约分 4/8=1/2。')],
  faqs=[dict(q='带分数怎么处理？', a='先转假分数再运算。')])

KB['science/gcd-calculator'] = dict(title='最大公约数（GCD）',
  scenarios=['约分、周期同步。'],
  examples=[dict(title='计算', body='gcd(48,18)：48=18·2+12，18=12+6，12=6·2 → gcd=6。')],
  faqs=[dict(q='与 LCM 关系？', a='gcd(a,b)·lcm(a,b)=a·b。')])

KB['science/geo-distance-calculator'] = dict(title='地理距离计算器',
  scenarios=['多点到点距离/半径圈。'],
  examples=[dict(title='计算', body='北京→上海 ≈1067 km（同 Haversine）。')],
  faqs=[dict(q='含海拔吗？', a='一般按球面，不计海拔差。')])

KB['science/gravitational-potential'] = dict(title='重力势能 E_p',
  scenarios=['提升物体储存的势能。'],
  examples=[dict(title='计算', body='m=10 kg、h=5 m：Ep=mgh=10·9.8·5=490 J。')],
  faqs=[dict(q='势能零点？', a='地面约定为 0，是相对量。')])

KB['science/heat-transfer-calculator'] = dict(title='热传递计算器',
  scenarios=['显热 Q=mcΔT。'],
  examples=[dict(title='计算', body='1 kg 水从 20°C 升到 100°C：Q=mcΔT=1·4186·80≈334,880 J（≈335 kJ）。')],
  faqs=[dict(q='相变热另算？', a='是，沸腾/熔化需额外潜热。')])

KB['science/hookes-law'] = dict(title='胡克定律 F = kx',
  scenarios=['弹性体受力与形变成正比。'],
  examples=[dict(title='计算', body='k=200 N/m、x=0.1 m → F=kx=20 N。')],
  faqs=[dict(q='胡克定律适用范围？', a='仅弹性限度内，超限则塑性变形。')])

KB['science/kinetic-energy'] = dict(title='动能 E_k',
  scenarios=['运动物体的动能。'],
  examples=[dict(title='计算', body='m=1000 kg、v=20 m/s：Ek=½mv²=0.5·1000·400=200,000 J。')],
  faqs=[dict(q='与速度平方关系？', a='动能随速度平方增长，倍速能耗翻四倍。')])

KB['science/latlon-utm-converter'] = dict(title='经纬度与 UTM 坐标转换',
  scenarios=['地理坐标 ↔ UTM 投影（分带）。'],
  examples=[dict(title='转换', body='(39.90°N,116.40°E) → UTM 50N 带，东向约 442 km、北向约 4416 km（近似）。')],
  faqs=[dict(q='UTM 为何分带？', a='减小投影变形，每 6° 一带。')])

KB['science/lcm-calculator'] = dict(title='最小公倍数（LCM）',
  scenarios=['通分、周期同步。'],
  examples=[dict(title='计算', body='lcm(4,6)=12；lcm(4,6,8)=24。')],
  faqs=[dict(q='与 GCD 关系？', a='lcm(a,b)=a·b/gcd(a,b)。')])

KB['science/led-resistor-calculator'] = dict(title='LED 限流电阻计算器',
  scenarios=['串联电阻保护 LED。'],
  examples=[dict(title='计算', body='Vs=5V、Vf=2V、If=20mA → R=(5-2)/0.02=150 Ω（取标称 150Ω）。')],
  faqs=[dict(q='不串电阻会怎样？', a='电流过大烧毁 LED。')])

KB['science/log-calculator'] = dict(title='对数计算器',
  scenarios=['常用对数/自然对数。'],
  examples=[dict(title='计算', body='log₁₀(1000)=3；ln(e³)=3；log₂(8)=3。')],
  faqs=[dict(q='换底公式？', a='logₐb=ln b/ln a。')])

KB['science/logic-gate-simulator'] = dict(title='逻辑门模拟器',
  scenarios=['验证与/或/非/异或真值表。'],
  examples=[dict(title='模拟', body='AND(1,0)=0；XOR(1,1)=0、XOR(1,0)=1。')],
  faqs=[dict(q='NAND 通用吗？', a='是，NAND 可构成任意逻辑。')])

KB['science/matrix-calculator'] = dict(title='矩阵计算器',
  scenarios=['行列式/逆/乘/转置。'],
  examples=[dict(title='计算', body='[[3,2],[5,7]]⁻¹=(1/11)[[7,-2],[-5,3]]；行列式 11。')],
  faqs=[(dict(q='奇异矩阵？', a='行列式为 0 不可逆。'))])

KB['science/mean-calculator'] = dict(title='平均数计算器',
  scenarios=['算术平均。'],
  examples=[dict(title='计算', body='[10,20,30] → 均值=(10+20+30)/3=20。')],
  faqs=[dict(q='均值易受影响？', a='对极端值敏感，常配合中位数看。')])

KB['science/mechanical-power'] = dict(title='功率 P = F·v',
  scenarios=['力与速度方向的功率。'],
  examples=[dict(title='计算', body='F=100 N、v=5 m/s（同向）→ P=Fv=500 W。')],
  faqs=[dict(q='单位？', a='瓦特 W = 焦耳/秒 = N·m/s。')])

KB['science/median-calculator'] = dict(title='中位数计算器',
  scenarios=['排序取中间，抗极端值。'],
  examples=[dict(title='计算', body='[1,3,5,7,9] 中位数=5；[1,2,3,4] 中位数=(2+3)/2=2.5。')],
  faqs=[dict(q='偶数个怎么办？', a='取中间两数平均。')])

KB['science/meteor-crater-estimator'] = dict(title='陨石撞击坑直径估算',
  scenarios=['按撞击能量估坑径（经验式）。'],
  examples=[dict(title='估算', body='直径 1 km、密度 3000 kg/m³、速度 20 km/s 的陨石，动能约 10¹⁹ J，坑径经验估算约数百米至 1 km 级。')],
  faqs=[dict(q='公式可靠吗？', a='为经验缩放关系，受角度/靶岩影响。')])

KB['science/mode-calculator'] = dict(title='众数计算器',
  scenarios=['出现最频繁的值。'],
  examples=[dict(title='计算', body='[1,2,2,3] 众数=2；可多峰。')],
  faqs=[dict(q='多个众数？', a='可多峰，均列出。')])

KB['science/molar-mass-calculator'] = dict(title='化学式摩尔质量计算器',
  scenarios=['由分子式算摩尔质量。'],
  examples=[dict(title='计算', body='NaCl：22.99+35.45=58.44 g/mol；C₆H₁₂O₆=180.16 g/mol。')],
  faqs=[dict(q='括号怎么算？', a='括号内原子数乘括号外系数。')])

KB['science/nato-phonetic'] = dict(title='NATO 音标字母',
  scenarios=['无线电报字母防误听。'],
  examples=[dict(title='转换', body='`AB` → Alfa Bravo；`C3` → Charlie Three。')],
  faqs=[dict(q='与 it 音标同？', a='同一 NATO 标准，跨分类一致。')])

KB['science/newtons-second'] = dict(title='牛顿第二定律 F = ma',
  scenarios=['合力、质量、加速度关系。'],
  examples=[dict(title='计算', body='m=10 kg、a=2 m/s² → F=ma=20 N。')],
  faqs=[dict(q='F 是合力？', a='是合外力，含所有方向。')])

KB['science/nth-root-calculator'] = dict(title='n 次方根计算器',
  scenarios=['开方（平方根/立方根等）。'],
  examples=[dict(title='计算', body='∛27=3；⁴√16=2。')],
  faqs=[dict(q='负根？', a='偶次根非负实根，奇次根可负（如 ∛-8=-2）。')])

KB['science/ohms-law-calculator'] = dict(title='欧姆定律计算器',
  scenarios=['V=IR 互求。'],
  examples=[dict(title='计算', body='I=2 A、R=5 Ω → V=IR=10 V；P=VI=20 W。')],
  faqs=[dict(q='功率怎么算？', a='P=VI=I²R=V²/R。')])

KB['science/p-value-calculator'] = dict(title='P 值计算器',
  scenarios=['由检验统计量算显著性 p。'],
  examples=[dict(title='计算', body='双尾 Z=1.96 → p≈0.05；Z=2.58 → p≈0.01。')],
  faqs=[dict(q='p<0.05 含义？', a='在原假设下如此极端结果概率<5%，倾向拒绝。')])

KB['science/passphrase-generator'] = dict(title='密码短语生成器',
  scenarios=['用词序列替代弱口令（高熵好记）。'],
  examples=[dict(title='生成', body='4 词示例 `correct-horse-battery-staple`（熵远高于同长随机符）。')],
  faqs=[dict(q='为何比口令强？', a='词序列长度大、熵高且易记。')])

KB['science/pcb-trace-width'] = dict(title='PCB 走线宽度计算器',
  scenarios=['按电流/温升求铜箔线宽。'],
  examples=[dict(title='估算', body='1 A、温升 10°C、1 oz 铜 → 线宽约 0.5–0.8 mm（IPC-2152 近似）。')],
  faqs=[dict(q='铜厚影响？', a='铜越厚载流越大，线宽可更窄。')])

KB['science/pendulum-period'] = dict(title='单摆周期 T',
  scenarios=['小角度下单摆周期。'],
  examples=[dict(title='计算', body='L=1 m：T=2π√(L/g)=2π√(1/9.8)≈2.006 s。')],
  faqs=[dict(q='大角度准吗？', a='仅小角度（<15°）近似，大角度周期更长。')])

KB['science/percentile-calculator'] = dict(title='百分位数计算器',
  scenarios=['数据分布的位置度量。'],
  examples=[dict(title='计算', body='[1,2,3,4,5,6,7,8,9,10] 第 90 百分位 ≈9.1。')],
  faqs=[dict(q='与四分位关系？', a='Q1/P25、Q2/P50、Q3/P75。')])

KB['science/periodic-table'] = dict(title='元素周期表',
  scenarios=['查元素基本属性。'],
  examples=[dict(title='查', body='Fe 铁：原子序 26，相对原子质量 55.85，第四周期 VIII 族。')],
  faqs=[dict(q='镧系锕系？', a='单独排在下方两行。')])

KB['science/permutation-calculator'] = dict(title='排列数 P(n, r)',
  scenarios=['从 n 取 r 计顺序。'],
  examples=[dict(title='计算', body='P(10,3)=10·9·8=720。')],
  faqs=[dict(q='与组合关系？', a='P(n,r)=C(n,r)·r!。')])

KB['science/ph-calculator'] = dict(title='酸碱 pH 值计算器',
  scenarios=['pH=-log₁₀[H⁺]。'],
  examples=[dict(title='计算', body='[H⁺]=1e-7 mol/L → pH=7（中性）；[H⁺]=1e-3 → pH=3（酸性）。')],
  faqs=[dict(q='pOH 呢？', a='pH+pOH=14（25°C）。')])

KB['science/phone-lookup'] = dict(title='电话号码查询',
  scenarios=['按号段识别运营商/归属地。'],
  examples=[dict(title='查', body='`1380013` 段属中国移动（示例）；具体以最新号段表为准。')],
  faqs=[dict(q='携号转网后准吗？', a='号段仅反映原注册运营商，携转后可能变化。')])

KB['science/phone-qr'] = dict(title='电话二维码',
  scenarios=['生成 tel: 二维码一键拨号。'],
  examples=[dict(title='生成', body='`tel:+8613800138000` → QR，扫码唤起拨号。')],
  faqs=[dict(q='扫码直接拨出？', a='唤起拨号界面，需用户确认。')])

KB['science/physics-calculator'] = dict(title='物理计算器',
  scenarios=['综合物理公式速算。'],
  examples=[dict(title='计算', body='自由落体 2s 末速 v=gt≈19.6 m/s；平抛水平位移 x=v₀t。')],
  faqs=[dict(q='单位要统一？', a='务必统一到 SI 再代入。')])

KB['science/pi-digits'] = dict(title='圆周率 π 位数查询',
  scenarios=['查 π 的各位数字。'],
  examples=[dict(title='查', body='π≈3.1415926535 8979323846…；第 1 位小数是 1，前 10 位 1415926535。')],
  faqs=[dict(q='π 有多少位？', a='无理数，已算至数万亿位，日常用 3.1416 足矣。')])

KB['science/polar-day-night'] = dict(title='极昼极夜日期判断',
  scenarios=['按纬度与日期判断是否极昼/极夜。'],
  examples=[dict(title='判断', body='北极圈（≥66.5°N）约 3/21–9/23 极昼、9/23–次年 3/21 极夜（近似）。')],
  faqs=[dict(q='南极相反？', a='是，南北半球季节相反。')])

KB['science/power-calculator'] = dict(title='幂计算器',
  scenarios=['乘方/开方。'],
  examples=[dict(title='计算', body='2¹⁰=1024；3⁴=81；10⁻²=0.01。')],
  faqs=[dict(q='负指数？', a='a⁻ⁿ=1/aⁿ。')])

KB['science/prime-number'] = dict(title='素数工具',
  scenarios=['判断素数/列素数。'],
  examples=[dict(title='判断', body='97 不能被 2..√97≈9 的素数整除 → 素数；91=7×13 合数。')],
  faqs=[dict(q='有无最大素数？', a='无，素数无穷多。')])

KB['science/probability-calculator'] = dict(title='概率计算器',
  scenarios=['古典概率与组合概率。'],
  examples=[dict(title='计算', body='掷一骰得 6 的概率=1/6≈16.7%；两独立事件都发生=P(A)·P(B)。')],
  faqs=[dict(q='互斥与独立？', a='互斥不能同时发生；独立互不影响。')])

KB['science/projectile-range'] = dict(title='斜抛射程与最大高度',
  scenarios=['抛体运动轨迹参数。'],
  examples=[dict(title='计算', body='v₀=30 m/s、θ=45°：射程 R=v₀²sin2θ/g=900·1/9.8≈91.8 m；最大高度 H=v₀²sin²θ/(2g)≈22.96 m。')],
  faqs=[dict(q='45° 最远？', a='同初速下 45° 射程最大（不计空气阻力）。')])

KB['science/provident-fund'] = dict(title='公积金计算器',
  scenarios=['估算公积金月缴存。'],
  examples=[dict(title='计算', body='缴存基数 5000、比例 12%：个人 600 + 单位 600 = 1200 元/月。')],
  faqs=[dict(q='基数有上下限？', a='按当地社平工资设封顶保底。')])

KB['science/quadratic-equation'] = dict(title='二次方程求解器',
  scenarios=['ax²+bx+c=0 求根。'],
  examples=[dict(title='求解', body='x²-5x+6=0：Δ=25-24=1，x=(5±1)/2 → x=2 或 3。')],
  faqs=[dict(q='判别式 Δ<0？', a='无实根，有共轭复根。')])

KB['science/quartile-calculator'] = dict(title='四分位数计算器',
  scenarios=['Q1/Q2/Q3 划分数据。'],
  examples=[dict(title='计算', body='[1..100] 共 100 数：Q1≈25.75、Q2=50.5、Q3≈75.25（线性插值法）。')],
  faqs=[dict(q='算法有几种？', a='有包含/排除中位数等不同约定，结果略异。')])

KB['science/range-calculator'] = dict(title='极差计算器',
  scenarios=['最大值-最小值。'],
  examples=[dict(title='计算', body='[3,7,2,9] → 极差=9-2=7。')],
  faqs=[dict(q='极差局限？', a='仅看两端，易受离群值影响。')])

KB['science/rc-time-constant'] = dict(title='RC 时间常数 (τ) 计算器',
  scenarios=['一阶 RC 充放电时间常数。'],
  examples=[dict(title='计算', body='R=1 kΩ、C=100 µF → τ=RC=0.1 s；充电到 63.2% 需 1τ，到 95% 约 3τ。')],
  faqs=[dict(q='τ 物理意义？', a='电压升至终值的 63.2% 所需时间。')])

KB['science/resistor-color-code'] = dict(title='电阻色码解码器',
  scenarios=['由色环读阻值与公差。'],
  examples=[dict(title='解码', body='棕黑红金：1-0-×10²-±5% → 1 kΩ ±5%。')],
  faqs=[dict(q='四环与五环？', a='五环多一位精度环，读法是有效数字不同。')])

KB['science/rfc-validator'] = dict(title='墨西哥 RFC 验证',
  scenarios=['校验墨西哥税号 RFC 格式与校验位。'],
  examples=[dict(title='校验', body='`ABC123456T1A` 按 RFC 规则校验结构与校验位（示例格式）。')],
  faqs=[(dict(q='RFC 含日期？', a='是个人/公司税号，含出生或注册日期片段。'))])

KB['science/root-calculator'] = dict(title='平方根计算器',
  scenarios=['平方根与任意根。'],
  examples=[dict(title='计算', body='√144=12；√2≈1.414。')],
  faqs=[dict(q='负数开方？', a='实数范围内无定义，复数域为 i√|x|。')])

KB['science/sample-size-calculator'] = dict(title='样本量计算器',
  scenarios=['按置信度与误差估所需样本。'],
  examples=[dict(title='计算', body='Z=1.96、p=0.5、e=0.05 → n=Z²p(1-p)/e²≈384（95% 置信、±5% 误差）。')],
  faqs=[dict(q='p 取多少？', a='未知时取 0.5 得最大样本量。')])

KB['science/science-flow-rate'] = dict(title='管道流量计算器',
  scenarios=['Q=Av 体积流量。'],
  examples=[dict(title='计算', body='管径 d=0.1 m → A=π·0.05²≈0.00785 m²，v=2 m/s → Q≈0.0157 m³/s（≈15.7 L/s）。')],
  faqs=[dict(q='与流速关系？', a='截面积固定时流量与流速成正比。')])

KB['science/science-pressure-converter'] = dict(title='压力单位转换器',
  scenarios=['Pa/kPa/atm/mmHg/bar 互转。'],
  examples=[dict(title='换算', body='1 atm=101.325 kPa=760 mmHg≈1.013 bar。')],
  faqs=[dict(q='mmHg 与 Torr？', a='近相等，1 Torr≈133.322 Pa。')])

KB['science/si-unit-converter'] = dict(title='国际单位(SI)转换器',
  scenarios=['SI 词头互转（k/m/µ/n）。'],
  examples=[dict(title='换算', body='5 km=5000 m；2.5 µA=2.5e-6 A。')],
  faqs=[dict(q='词头含义？', a='k=10³、m=10⁻³、µ=10⁻⁶、n=10⁻⁹。')])

KB['science/significant-figures'] = dict(title='有效数字计算器',
  scenarios=['按有效数字修约。'],
  examples=[dict(title='修约', body='12.345 保留 3 位有效数字 → 12.3；0.00456 有 3 位有效数字。')],
  faqs=[dict(q='四舍五入规则？', a='4 舍 6 入，5 看前位奇偶（银行家法）或进一。')])

KB['science/spring-oscillation-period'] = dict(title='简谐振动周期 T',
  scenarios=['弹簧振子周期。'],
  examples=[dict(title='计算', body='m=1 kg、k=100 N/m → T=2π√(m/k)=2π√0.01≈0.628 s。')],
  faqs=[dict(q='质量越大越慢？', a='是，T∝√m。')])

KB['science/star-magnitude-compare'] = dict(title='星等亮度对比',
  scenarios=['由星等差算亮度比。'],
  examples=[dict(title='对比', body='两星差 5 等 → 亮度比=10^(0.4·5)=100 倍；差 1 等→约 2.512 倍。')],
  faqs=[dict(q='公式？', a='L₁/L₂=10^(0.4(m₂-m₁))。')])

KB['science/statistics-calculator'] = dict(title='统计计算器',
  scenarios=['描述统计与推断一键算。'],
  examples=[dict(title='计算', body='[2,4,6,8] 均值 5、方差 6.67（样本）。')],
  faqs=[dict(q='偏度峰度？', a='描述分布不对称与尖峭程度。')])

KB['science/t-score-calculator'] = dict(title='T 分数计算器',
  scenarios=['单样本/两样本 t 统计量。'],
  examples=[dict(title='计算', body='x̄=105、μ=100、s=15、n=36 → t=(105-100)/(15/6)=2.0，df=35。')],
  faqs=[dict(q='t 与 z 区别？', a='σ 未知用小样本 t，大样本近似 z。')])

KB['science/text-extract-phones'] = dict(title='提取电话号码',
  scenarios=['从文本批量抽取号码。'],
  examples=[dict(title='提取', body='"联系 138-0013-8000 或 010-12345678" → 抽出两串号码并去格式。')],
  faqs=[dict(q='格式怎么归一？', a='去分隔符保留数字，按号段识别。')])

KB['science/tide-height-estimator'] = dict(title='潮汐高度估算',
  scenarios=['半日潮潮高经验估算。'],
  examples=[dict(title='估算', body='半日潮平均潮差 2 m、基准 0.5 m → 高/低潮约 +1.5 / -0.5 m（示意）。')],
  faqs=[dict(q='潮汐受什么影响？', a='月球引力为主，加地形与气象。')])

KB['science/torque-converter'] = dict(title='扭矩单位转换器',
  scenarios=['N·m / lbf·ft / kgf·cm 互转。'],
  examples=[dict(title='换算', body='10 N·m≈7.376 lbf·ft；1 kgf·cm≈0.098 N·m。')],
  faqs=[dict(q='扭矩与功？', a='扭矩是转动力矩，功=扭矩×转角。')])

KB['science/trigonometry-calculator'] = dict(title='三角函数计算器',
  scenarios=['sin/cos/tan 及反函数。'],
  examples=[dict(title='计算', body='sin(30°)=0.5；cos(60°)=0.5；tan(45°)=1（DEG 模式）。')],
  faqs=[dict(q='角度还是弧度？', a='注意模式，30°=π/6 rad。')])

KB['science/variance-calculator'] = dict(title='方差计算器',
  scenarios=['离散程度。'],
  examples=[dict(title='计算', body='[2,4,4,4,5,5,7,9] 总体方差 4、样本方差≈4.57。')],
  faqs=[dict(q='方差与标准差？', a='标准差是方差平方根，单位与原数据一致。')])

KB['science/vector-calculator'] = dict(title='向量计算器',
  scenarios=['加减/点积/模长。'],
  examples=[dict(title='计算', body='(3,4) 模长 √(9+16)=5；点积 (1,2)·(3,4)=11。')],
  faqs=[dict(q='夹角？', a='cosθ=点积/(|a||b|)。')])

KB['science/voltage-divider-calculator'] = dict(title='电阻分压器计算器',
  scenarios=['串联分压求某点电压。'],
  examples=[dict(title='计算', body='Vin=9V、R1=1k、R2=2k → Vout=Vin·R2/(R1+R2)=9·2000/3000=6 V。')],
  faqs=[dict(q='负载影响？', a='带载会降低输出，需高阻输入。')])

KB['science/wavelength-to-rgb'] = dict(title='可见光波长转 RGB 颜色',
  scenarios=['按波长(380–750nm)近似颜色。'],
  examples=[dict(title='转换', body='650 nm→红 rgb(255,0,0)；520 nm→绿 rgb(0,255,0)；450 nm→蓝 rgb(0,0,255)。')],
  faqs=[dict(q='超出可见范围？', a='<380 紫外、>750 红外，无对应 RGB。')])

KB['science/wire-gauge-converter'] = dict(title='AWG 线规转换器',
  scenarios=['AWG 号 ↔ 直径/载流。'],
  examples=[dict(title='换算', body='AWG 20 → 直径 ≈0.812 mm，载流约 5 A（PVC 绝缘近似）。')],
  faqs=[dict(q='号越大线越细？', a='是，AWG 号与直径反比。')])

KB['science/work-done'] = dict(title='功 W = F·d·cosθ',
  scenarios=['力沿位移做功。'],
  examples=[dict(title='计算', body='F=100 N、d=5 m、θ=0° → W=Fd cosθ=500 J。')],
  faqs=[dict(q='垂直力不做功？', a='力垂直位移(θ=90°)时 cosθ=0，不做功。')])

KB['science/xianxingfangchengzuqiujie-2yuan-3yuan'] = dict(title='线性方程组求解（2元/3元）',
  scenarios=['解二元/三元一次方程组。'],
  examples=[dict(title='求解', body='2x+y=5、x-y=1 → 代入 y=x-1 → 2x+(x-1)=5 → x=2、y=1。')],
  faqs=[dict(q='无解/无穷解？', a='系数成比例时退化，需判别。')])

KB['science/yiyuanercifangchengqiujie'] = dict(title='一元二次方程求解',
  scenarios=['ax²+bx+c=0 求根。'],
  examples=[dict(title='求解', body='x²-5x+6=0 → x=2 或 3（Δ=1）。')],
  faqs=[dict(q='判别式？', a='Δ=b²-4ac 决定根的性质。')])

KB['science/z-score-calculator'] = dict(title='Z 分数计算器',
  scenarios=['标准化偏离均值的个数。'],
  examples=[dict(title='计算', body='x=70、μ=60、σ=10 → z=(70-60)/10=1（高于均值 1 个标准差）。')],
  faqs=[dict(q='z 含义？', a='负值低于均值，绝对值表偏离程度。')])

# ---------- apply ----------
changed = 0
for slug, entry in KB.items():
    if slug not in data:
        continue
    new = {'title': entry['title'], 'scenarios': entry['scenarios'],
           'examples': entry['examples'], 'faqs': entry['faqs']}
    if data[slug] != new:
        data[slug] = new
        changed += 1

print(f"KB entries: {len(KB)}  changed: {changed}")
with open(DD, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write('\n')
print("written.")
