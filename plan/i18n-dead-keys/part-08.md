### meteorology（dead 18 / dynamic 0 / fragment 5 / harmless 0）

- `tools/meteorology/air-aqi.html` : `AQI = 逐污染物分段线性插值` : dead
- `tools/meteorology/apparent-temperature.html` : `AT = 体感温度（温湿风综合）` : dead
- `tools/meteorology/assessor-29.html` : `干旱评估用两类指标：降水距平百分率 Pa=(当前降水量−同期均值)÷同期均值×100%，按 Pa 阈值分级（≥−15% 无旱、−30% 轻旱、−50% 中旱、−70% 重旱、<−70% 特旱）；标准化降水指数 SPI=(当前−均值)÷标准差，按 SPI 阈值（≥−0.5 无旱、−1.0 轻旱、−1.5 中旱、−2.0 …(+27字)` : dead
- `tools/meteorology/beaufort-scale.html` : `风速 v ↔ 蒲福风级 n` : dead
- `tools/meteorology/calc-55.html` : `月相照明率 = (1+cos φ)/2` : dead
- `tools/meteorology/calc-84.html` : `日照辐射量 = 辐照度 × 时长` : dead
- `tools/meteorology/cloud-identify.html` : `云按云底高度分四族：高云（>5km）、中云（2.5—5km）、低云（<2.5km）、直展云（垂直发展旺盛）。` : dead
- `tools/meteorology/dew-point.html` : `露点 Td = Magnus 公式反解` : dead
- `tools/meteorology/heat-index.html` : `HI = 体感指数（温湿综合）` : dead
- `tools/meteorology/humidity-1.html` : `露点舒适度 = f(温度, 露点)` : dead
- `tools/meteorology/jiaotongqixianganquantishi.html` : `道路气象安全按三项分级综合研判：能见度 vis（<50m 特级、<200m 红、<500m 橙、<1000m 黄、其余良好）、路面温度 rt（<−3℃ 红、<0℃ 橙、<2℃ 黄）、侧风 v（≥24m/s 红，逐级下降）。任一要素达红/橙级即给出对应管制建议（限速、防滑、封闭），保障行车安全。` : dead
- `tools/meteorology/lvyouqixiangzhishu.html` : `旅游气象指数按温度(T)、湿度(RH)、风速(V)、紫外线(UV)四项舒适度加权：温度分=100−|T−22|×3.5、湿度分=100−|RH−55|×0.9、风速分=100−|V−3|×6、紫外线分=100−UV×9（均截断 0–100）；综合 idx=0.35×T分+0.20×RH分+0.20×V分+0.25×UV…(+50字)` : dead
- `tools/meteorology/nongyeqixiangjianyi.html` : `农业气象建议基于作物积温：生育进度=累积 GDD÷该作物所需 GDD 上限×100，划分播种-出苗/苗期-分蘖/拔节-抽穗/灌浆-结铃/成熟等生育期；播种适宜性按气温 T 与作物播种温区[sowT]、最适温区[optT]判定；降水量 P<10mm 提示灌溉缺水，依生育期与降水给出收割与防涝建议。` : dead
- `tools/meteorology/precipitation-rate.html` : `采用中国气象局常用分级：小雨<2.5、中雨<8、大雨<16、暴雨<50、大暴雨<100。` : dead
- `tools/meteorology/qiyaxitongyidonglujing.html` : `💡 高压（P>1020）多晴好天气，低压（P<1000）多阴雨；3小时变压 ΔP>1.5 表示系统快速接近，<-1.5 表示低压加深、天气转坏。` : dead
- `tools/meteorology/strength-3.html` : `雷达回波强度：反射率因子 Z=10^(dBZ/10)，降水率 R=(Z/200)^(1/1.6) mm/h；冰雹概率由 dBZ 与回波顶高 h 联合估计；液态水含量 VIL=3.44×10⁻⁶·Z^(4/7)·h（kg/m²）；按 dBZ 阈值（<30 弱对流、<50 强对流、≥55 冰雹可能、≥60 强冰雹）判定对流…(+18字)` : dead
- `tools/meteorology/wet-bulb-temperature.html` : `湿球温度 T_w（迭代近似）` : dead
- `tools/meteorology/wind-direction.html` : `风向方位 = 角度 → 16 方位` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/meteorology/analysis-31.html` : `距平 = 观测值 − 常年平均值` : fragment
  - `tools/meteorology/analysis-31.html` : `标准化距平 σ = 距平 ÷ 历史标准差` : fragment
  - `tools/meteorology/analysis-tide.html` : `潮型系数 F = (H_K1 + H_O1) ÷ (H_M2 + H_S2)` : fragment
  - `tools/meteorology/speed-11.html` : `Z = 200·R^1.6，故 R = (Z/200)^(1/1.6)` : fragment
  - `tools/meteorology/taifengdingqiang.html` : `节 = 0.5144 m/s。气压越低，最大风速越强。` : fragment

### metrology（dead 11 / dynamic 1 / fragment 1 / harmless 0）

- `tools/metrology/bias-absolute.html` : `偏倚 = x − x_ref` : dead
- `tools/metrology/bias-percent.html` : `偏倚% = (x − x_ref)/x_ref × 100%` : dead
- `tools/metrology/expanded-uncertainty.html` : `k=2 约 95% 置信。 报告形式：测得值 ±U。` : dead
- `tools/metrology/flatness-deviation.html` : `平面度 = 最高点 − 最低点` : dead
- `tools/metrology/gauge-repeatability.html` : `重复性 = R̄/d₂` : dead
- `tools/metrology/gauge-reproducibility.html` : `再现性 = R̄/d₂*` : dead
- `tools/metrology/grr-percent.html` : `%GRR<10% 测量系统可接受。` : dead
- `tools/metrology/grr-study.html` : `%GRR<10% 良好。` : dead
- `tools/metrology/least-count-error.html` : `极限误差 = ±(分度值/2)` : dead
- `tools/metrology/precision-tolerance-ratio.html` : `PTR<0.1 通常分辨率足够。` : dead
- `tools/metrology/roundness-deviation.html` : `圆度 = R_max − R_min` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/metrology/detector-139.html` : `12 个月` : fragment
  - `tools/metrology/detector-139.html` : `3 个月` : dynamic

### mining（dead 2 / dynamic 4 / fragment 1 / harmless 0）

- `tools/mining/convert-grade-ore.html` : `矿石价值(元) = 金属总量 × 金属价格(元/g)` : dead
- `tools/mining/excavation-volume.html` : `长方体 V=L·W·D；梯形截面 V=(上底宽+下底宽)/2×深×长（含边坡时上底=下底+2·深·边坡）；圆柱 V=πR²H，圆台 V=πH/3·(R₁²+R₁R₂+R₂²)；虚方=实方×松散系数 swell；成本=实方×单价。` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/mining/convert-grade-ore.html` : `金属总量(g) = 品位(g/t) × 矿石量(t)` : fragment
  - `tools/mining/convert-grade-ore.html` : `品位需填写 ≥0 的数值（g/t）` : dynamic
  - `tools/mining/convert-grade-ore.html` : `矿石量需填写 ≥0 的数值（t）` : dynamic
  - `tools/mining/convert-grade-ore.html` : `金属价格需填写 ≥0 的数值（元/g）` : dynamic
  - `tools/mining/excavation-volume.html` : `上口宽不能小于底宽，请核对输入` : dynamic

### misc（dead 9 / dynamic 0 / fragment 0 / harmless 0）

- `tools/misc/index.html` : `使用 Canvas 绘制常见函数图像：一次函数、二次函数、三角函数、指数函数、对数函数，支持自定义参数与坐标范围。` : dead
- `tools/misc/index.html` : `内置 30+ 常用物理学常数，含数值、单位、符号与说明，支持搜索与分类筛选。数据基于 CODATA 2018 推荐值。` : dead
- `tools/misc/index.html` : `在 SI 单位前缀（nano / micro / milli / kilo / Mega / Giga / Tera 等）之间换算数值。` : dead
- `tools/misc/index.html` : `支持复数的加、减、乘、除运算及与极坐标（模、幅角）的相互转换，并在复平面上直观绘制点的位置，适用于工程数学与电路相量分析的教学演示。` : dead
- `tools/misc/index.html` : `标准小数与科学记数法（a×10ⁿ）双向互转，支持工程记数法与 E 记数法。` : dead
- `tools/misc/index.html` : `生成奇数阶幻方使各行列对角线和相等，可调阶数并校验，用于数学游戏与教学演示，纯前端生成棋盘可复制。` : dead
- `tools/misc/index.html` : `用 4 个数字和 +、−、×、÷、括号 组成表达式，使结果等于 24。每个数字必须且只能用一次。` : dead
- `tools/misc/index.html` : `输入逻辑表达式，自动识别变量并生成完整真值表。支持与或非、异或、蕴含、等价等运算。` : dead
- `tools/misc/index.html` : `选择分布类型（正态、泊松、二项），输入均值/方差或成功概率与试验次数等参数，计算对应概率密度函数与累积分布概率。用于概率统计教学、质量分析与风险建模。` : dead

### misc2（dead 11 / dynamic 0 / fragment 0 / harmless 0）

- `tools/misc2/index.html` : `二手车残值计算` : dead
- `tools/misc2/index.html` : `列出各品牌与国家的鞋码对照（欧、美、英、厘米），输入已知码查对应尺码，方便网购选号，纯前端查表。` : dead
- `tools/misc2/index.html` : `基于十二平均律生成各音名的标准频率对照表，默认基准A4=440Hz并支持自定义基准音高，供乐器校音、合唱定调与声学教学快速查阅参考。` : dead
- `tools/misc2/index.html` : `屏幕尺寸计算器由分辨率宽高与对角线英寸求 PPI 像素密度，并换算实际显示尺寸，适合选购显示器、手机与投影设备的清晰度评估。` : dead
- `tools/misc2/index.html` : `快递保价费计算器按声明价值与快递公司费率估算保价费用，支持多家快递对比，适合寄件前成本预估与贵重物品保护决策。` : dead
- `tools/misc2/index.html` : `查阅 18–30 寸主流行李箱的长宽高与容量规格，并对照各航空公司随身行李与托运行李的尺寸重量限制。用于出行前选择符合航司规定的箱包，避免登机受阻。` : dead
- `tools/misc2/index.html` : `生活杂项工具集合收录了 9 个免费在线工具，覆盖生活杂项场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/misc2/index.html` : `输入境外购物金额、目的地国家税率与实时汇率，估算可退税款金额与退税后的实际花费。用于出境旅游购物前预估退税收益、比较不同目的地划算程度。` : dead
- `tools/misc2/index.html` : `输入新车购置价与已使用年限，按前5年分别折旧 15%、12%、10%、8%、6%、之后每年约 5% 的曲线估算二手车剩余价值。用于家用车快速估值、置换参考与残值预测。` : dead
- `tools/misc2/index.html` : `输入香烟标注的焦油/尼古丁含量与每日吸烟支数，估算每日焦油与尼古丁摄入总量及相对暴露风险。用于烟民了解吸烟负荷，结果仅供健康意识参考。` : dead
- `tools/misc2/index.html` : `选择或输入钱币品相等级（谢尔登分级 Sheldon 1–70），查看对应磨损程度说明、评分要点与收藏保值建议。用于钱币收藏者快速对照品相、评估钱币价值。` : dead

### museum（dead 6 / dynamic 7 / fragment 1 / harmless 0）

- `tools/museum/era-comparator.html` : `历史朝代对比。历史人文工具，帮助查询与了解历史文化知识。` : dead
- `tools/museum/historical-calendar.html` : `历史日历是一款历史人文领域的在线工具。历史人文工具，帮助查询与了解历史文化知识。` : dead
- `tools/museum/index.html` : `历史日历是一款免费的在线文博展陈工具，历史日历是一款历史人文领域的在线工具。历史人文工具，帮助查询与了解历史文化知识。纯前端运行、数据不上传、无需注册，打开浏览器即可使用。` : dead
- `tools/museum/index.html` : `历史时间轴是一款免费的在线文博展陈工具，历史时间轴是一款历史人文领域的在线工具。历史人文工具，帮助查询与了解历史文化知识。纯前端运行、数据不上传、无需注册，打开浏览器即可使用。` : dead
- `tools/museum/index.html` : `历史朝代对比是一款免费的在线文博展陈工具，历史朝代对比。历史人文工具，帮助查询与了解历史文化知识。纯前端运行、数据不上传、无需注册，打开浏览器即可使用。` : dead
- `tools/museum/timeline-viewer.html` : `历史时间轴是一款历史人文领域的在线工具。历史人文工具，帮助查询与了解历史文化知识。` : dead

  其它成因样例（共 8 条，仅列前 5）：
  - `tools/museum/lighting-lux.html` : `达标 ✓` : dynamic
  - `tools/museum/lighting-lux.html` : `平均照度超标 ✕` : dynamic
  - `tools/museum/lighting-lux.html` : `中心照度过曝 ✕` : dynamic
  - `tools/museum/visitor-route.html` : `检测到负距离，已按绝对值纳入计算。` : dynamic
  - `tools/museum/visitor-route.html` : `必看节点` : fragment

### music（dead 3 / dynamic 2 / fragment 1 / harmless 0）

- `tools/music/index.html` : `音乐艺术工具集合收录了 19 个免费在线工具，覆盖音乐艺术场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/music/random-training-rhythm.html` : `鼓手/器乐练习者用空格或点击跟节拍器敲击，练稳定律动；随机节奏型用于读谱与节奏型参考` : dead
- `tools/music/web-tuner.html` : `MIDI = 69 + 12·log2(f / A4参考频率)；A4 参考 440 Hz 时，440 Hz → MIDI 69 → A4，音分 = (69−69)×100 = 0（准）。446 Hz → MIDI≈69.246 → +24.6 cents（偏高）；参考改为 442 Hz 时 442 Hz 同样对应 A4…(+7字)` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/music/random-training-rhythm.html` : `节奏准确率 = 命中节拍数 ÷ 总节拍数 × 100%；单次偏差 = 实际点击时刻 − 标准节拍时刻（正为拖后、负为提前），平均偏差 = Σ 偏差 ÷ 次数；稳定度可用偏差标准差衡量，标准差低于 30 ms 为稳定；节拍间隔 = 60000 ÷ BPM 毫秒（如 120 BPM 为 500 ms）。` : fragment
  - `tools/music/random-training-rhythm.html` : `已停止` : dynamic
  - `tools/music/random-training-rhythm.html` : `跟拍中… 共 ` : dynamic

### nephrology（dead 19 / dynamic 23 / fragment 4 / harmless 0）

- `tools/nephrology/aki-kdigo.html` : `AKI诊断：48h Scr↑≥26.5 μmol/L 或 7天↑≥1.5×基线 或 尿量<0.5 mL/kg/h。分期：1期 1.5–1.9×；2期 2.0–2.9×；3期 ≥3× 或 ≥353.6 μmol/L 或 尿量<0.3 mL/kg/h×≥24h；取肌酐/尿量较重者` : dead
- `tools/nephrology/ca-p-product.html` : `换算：钙磷乘积 mmol²/L² × 12.45 = mg²/dL²。目标值<55 mg²/dL²（4.4 mmol²/L²）。` : dead
- `tools/nephrology/ckd-staging.html` : `G3a+A2→高风险，建议 2 次/年随访并转诊肾内科。` : dead
- `tools/nephrology/ckd-staging.html` : `G4(15–29)+A3→很高风险，≥3 次/年随访，积极管理并发症并准备肾脏替代。` : dead
- `tools/nephrology/creatinine-clearance.html` : `Ccr 50-80 为轻度损害，25-50 为中度损害，10-25 为重度损害，<10 为终末期肾病。` : dead
- `tools/nephrology/creatinine-clearance.html` : `提示：收集24h尿液前3天需低蛋白饮食（<40g/d），禁食肉食，避免剧烈运动，以保证肌酐排泄稳定。Ccr反映肾小球滤过功能，但肾小管也分泌少量肌酐，故Ccr略高于真实GFR。本工具仅供学习参考。` : dead
- `tools/nephrology/creatinine-clearance.html` : `本页按 Ccr 分段：≥80 正常范围、50–79 轻度下降、25–49 中度下降、10–24 重度下降、<10 极重度下降。该分段仅为 Ccr 的功能描述，不等同于 KDIGO 2012 的 CKD G1–G5 分期（后者基于 eGFR）；「终末期肾病」为临床诊断，本页不下此结论。` : dead
- `tools/nephrology/edema-grading.html` : `水肿分级（按凹陷深度）：1+ 不超过2mm 轻度、2+ 2–4mm 中度、3+ 4–6mm 重度、4+ 不低于6mm 极重度；结合部位与是否对称评估病因。` : dead
- `tools/nephrology/manager-1.html` : `CKD诊断需满足：eGFR<60持续>3个月，或肾脏损伤标志（白蛋白尿等）持续>3个月` : dead
- `tools/nephrology/manager-1.html` : `：ACR <30 mg/g（正常至微量增加）` : dead
- `tools/nephrology/manager-1.html` : `：eGFR <15（肾衰竭）` : dead
- `tools/nephrology/proteinuria-24h.html` : `24 小时尿蛋白分级：小于0.15g 正常、0.15–0.5 轻度、0.5–3.5 中度、不低于3.5g 为肾病综合征范围蛋白尿。` : dead
- `tools/nephrology/proteinuria-24h.html` : `24h 尿蛋白 ≥3.5 g，属肾病综合征范围蛋白尿；但肾病综合征的诊断还需血清白蛋白 <30 g/L 与水肿，本页不能据此单独确诊。需评估血清白蛋白、血脂、肾功能，排查继发因素（糖尿病、系统性红斑狼疮、肿瘤等），建议肾内科评估是否肾活检。` : dead
- `tools/nephrology/proteinuria-24h.html` : `≥3.5g/24h 属肾病范围；是否诊断肾病综合征还需低白蛋白(<30g/L)与水肿，并由肾内科评估是否需病理检查。` : dead
- `tools/nephrology/proteinuria-24h.html` : `□ 查血清白蛋白是否 <30 g/L（肾病综合征必需条件之一）` : dead
- `tools/nephrology/renal-anemia-epo.html` : `HGB <100（个体化）` : dead
- `tools/nephrology/renal-tubular-acidosis.html` : `低钾(常<3.5)` : dead
- `tools/nephrology/renal-tubular-acidosis.html` : `提示：RTA核心特征为正常阴离子间隙型代谢性酸中毒(AG正常)。I型尿pH始终>5.5，II型酸中毒严重时尿pH可<5.5，IV型以高钾血症为特征。碳酸氢盐试验(FE-HCO₃⁻)有助于确诊。本工具仅供学习参考。` : dead
- `tools/nephrology/urine-electrolyte.html` : `<20肾外丢失，>20肾性丢失` : dead

  其它成因样例（共 27 条，仅列前 5）：
  - `tools/nephrology/ckd-staging.html` : `请填写有效的 eGFR 与 UACR 数值（UACR 不能留空）` : dynamic
  - `tools/nephrology/creatinine-clearance.html` : `内生肌酐清除率 Ccr(mL/min) = [尿肌酐(μmol/L) × 尿量(mL/min)] ÷ 血肌酐(μmol/L)；并用体表面积校正 Ccr × 1.73 ÷ BSA。` : fragment
  - `tools/nephrology/creatinine-clearance.html` : `Ccr ≥80（正常范围）` : dynamic
  - `tools/nephrology/creatinine-clearance.html` : `Ccr 50–79（轻度下降）` : dynamic
  - `tools/nephrology/creatinine-clearance.html` : `Ccr 25–49（中度下降）` : dynamic

### neurology（dead 6 / dynamic 41 / fragment 0 / harmless 0）

- `tools/neurology/alsfrs-r.html` : `球部 12+臂 12+躯干 4+腿 8+呼吸 12=48 分（满分，功能正常）。` : dead
- `tools/neurology/nihss.html` : `0 无神经功能缺损（不代表排除卒中）、1~4 轻、5~15 中、16~20 中重、≥21 重；上限 42。` : dead
- `tools/neurology/nihss.html` : `合计 18 分：中重度（16~20），需紧急评估取栓/溶栓并加强监护。` : dead
- `tools/neurology/nihss.html` : `总分 ≥16 分提示可能存在大血管闭塞` : dead
- `tools/neurology/rater-22.html` : `SARA 小脑共济失调量表总分 = 8 项检查（步态/站姿/坐姿/言语/指鼻/跟膝胫/轮替/跟-胫滑动）之和，满分 40；≤3 轻度、≤8 轻中度、≤15 中度、≤30 重度、>30 极重度。` : dead
- `tools/neurology/rater-22.html` : `SARA包含步态、站立、坐位、言语、追视、鼻指测试和交替轮替运动8项检查，总分0-40分，广泛用于遗传性共济失调的诊断分期、疗效评估和疾病进展监测。` : dead

  其它成因样例（共 41 条，仅列前 5）：
  - `tools/neurology/qmg.html` : `13.颈屈` : dynamic
  - `tools/neurology/rater-22.html` : `1.步态（0–8分）` : dynamic
  - `tools/neurology/rater-22.html` : `2.站立（0–6分）` : dynamic
  - `tools/neurology/rater-22.html` : `3.坐位（0–4分）` : dynamic
  - `tools/neurology/rater-22.html` : `4.言语障碍（0–6分）` : dynamic

### niche（dead 17 / dynamic 0 / fragment 0 / harmless 0）

- `tools/niche/index.html` : `在不同采样率（如 44.1k、48k）间换算，输入声道数与位深计算音频文件大小，并按奈奎斯特定理给出最高可记录频率。用于录音、混音格式选型。` : dead
- `tools/niche/index.html` : `在常见视频帧率（24/25/30/60fps）间换算并估算时长变化，用于剪辑与格式转换参考，纯前端换算不转码。` : dead
- `tools/niche/index.html` : `垂直工具工具集合收录了 16 个免费在线工具，覆盖垂直工具场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/niche/index.html` : `基于曝光三角（光圈、快门、ISO）计算曝光值 EV，并提供多组等效曝光组合，方便摄影师在保持曝光量不变下自由调整参数。` : dead
- `tools/niche/index.html` : `按低光、中光、高光三级对常见水草分类，输入鱼缸光照条件即可筛选适合养殖的品种并标注养护要点。用于水族造景选草，避免光照不足或藻类爆发。` : dead
- `tools/niche/index.html` : `按多肉品种管理浇水周期，内置常见科属浇水频率数据库，自动根据季节调整（夏休眠/冬减量），按紧急度排序生成浇水队列。` : dead
- `tools/niche/index.html` : `蜡烛燃烧时间估算工具按蜡烛重量与蜡材类型估算可持续燃烧时长，并给出首燃与烛芯修剪建议，适合香薰与应急照明规划。` : dead
- `tools/niche/index.html` : `输入猫或狗的实足年龄，按物种换算为对应的人类年龄阶段，帮助主人理解宠物的生命阶段与保健重点。用于宠物健康管理科普与兽医沟通。` : dead
- `tools/niche/index.html` : `输入蜂箱数量、花源面积与蜜源类型（油菜、椴树、荔枝等），估算年度可采蜜量并比较不同蜜源产量差异。用于养蜂场产能规划与收益预估。` : dead
- `tools/niche/index.html` : `输入视频时长与目标帧率（24/25/30/60 fps 等），换算总帧数并计算不同帧率间的关系，评估慢放/抽帧效果。用于视频剪辑、动画与帧率匹配。` : dead
- `tools/niche/index.html` : `输入鱼缸长×宽×高（或已有水量），计算实际装水体积与有效水量，并按每厘米鱼长需约 1 升水推荐可养鱼数量与过滤/加热设备配置。用于新手养鱼规划。` : dead
- `tools/niche/index.html` : `选择多肉品种与季节，推荐浇水频率并支持记录每次浇水时间、到期自动提醒，避免烂根或过度干旱。用于多肉爱好者规律养护。` : dead
- `tools/niche/index.html` : `选择植物类型（月季、果树、灌木等）与季节，推荐最佳修剪时间窗口与操作要点，帮助花园维持株型美观与开花结果。用于家庭园艺日程规划。` : dead
- `tools/niche/index.html` : `选择草种（如早熟禾、结缕草等 8 种）与季节，推荐最佳修剪留茬高度并给出不同季节的修剪频率与策略。用于庭院草坪养护，保持草皮健康浓密。` : dead
- `tools/niche/index.html` : `选择陶土类型（低温陶土、高温陶土、瓷土等），查看推荐的烧制温度区间、升温/保温/降温曲线与各阶段关键参数。用于陶艺工作者规划窑炉烧制方案。` : dead
- `tools/niche/index.html` : `陶艺烧制温度曲线推荐工具依据泥料与器型推荐升温、保温与冷却曲线，辅助电窑或气窑的烧成方案制定，适合陶艺创作。` : dead
- `tools/niche/index.html` : `音频采样率转换工具在 kHz 单位间换算采样频率，支持播放与录制参数的格式统一，适合音频处理、降采样与设备兼容。` : dead

### nuclear（dead 10 / dynamic 0 / fragment 0 / harmless 0）

- `tools/nuclear/activity-decay.html` : `A = A₀e^(−λt)。 活度衰减与核数同步。` : dead
- `tools/nuclear/age-from-activity.html` : `t = (1/λ)·ln(N₀/N)。 C-14 减半 → 约 5730 年。` : dead
- `tools/nuclear/carbon-dating-age.html` : `t = T½/ln2 · ln(N₀/N)。 剩 50% 即一个半衰期。` : dead
- `tools/nuclear/decay-fraction.html` : `已衰变份额 = 1 − e^(−λt)` : dead
- `tools/nuclear/mass-defect.html` : `Δm = Zm_p + Nm_n − M。 铁-56：Z=26,N=30。` : dead
- `tools/nuclear/q-value.html` : `Q>0 放能，Q<0 吸能。` : dead
- `tools/nuclear/radioactive-decay.html` : `N = N₀e^(−λt)。 一半衰期后剩约 50%。` : dead
- `tools/nuclear/reaction-rate.html` : `R = ΦσN。 示例 → 1×10⁵ /s。` : dead
- `tools/nuclear/specific-activity.html` : `a = λN_A/M。 碳-14 比活度较低。` : dead
- `tools/nuclear/specific-activity.html` : `碳-14 比活度较低。` : dead

### nutrition（dead 4 / dynamic 8 / fragment 12 / harmless 0）

- `tools/nutrition/generator-nutrition-label.html` : `复制结果` : dead
- `tools/nutrition/generator-nutrition-label.html` : `按 GB 28050 预包装食品营养标签通则：能量 8400 kJ、蛋白质 60g、脂肪 60g、碳水 300g、膳食纤维 25g、钠 2000mg。` : dead
- `tools/nutrition/generator-nutrition-label.html` : `某食品每 100g：蛋白质 10g、脂肪 20g、碳水 55g、膳食纤维 2g、钠 300mg。能量 = 10×17 + 20×37 + 55×17 + 2×8 = 1861 kJ（444.9 kcal）。NRV%：蛋白质 16.7%、脂肪 33.3%、碳水 18.3%、膳食纤维 8.0%、钠 15.0%、能量 22.…(+24字)` : dead
- `tools/nutrition/generator-nutrition-label.html` : `营养（表标签）一键生成。免费在线工具，纯前端处理，数据不上传，保护隐私安全。` : dead

  其它成因样例（共 20 条，仅列前 5）：
  - `tools/nutrition/generator-glucose-load.html` : `碳水` : fragment
  - `tools/nutrition/generator-glucose-load.html` : `每份` : dynamic
  - `tools/nutrition/generator-nutrition-label.html` : `表标签` : fragment
  - `tools/nutrition/generator-nutrition-label.html` : `请至少填写一项营养素含量（g/100g）。` : dynamic
  - `tools/nutrition/generator-nutrition-label.html` : `每 100 g` : fragment

### obstetrics（dead 15 / dynamic 1 / fragment 1 / harmless 0）

- `tools/obstetrics/afi-normal.html` : `羊水指数按四象限深度求和；AFI 5–24 cm 为正常，<5 cm 羊水过少，>24 cm 羊水过多；SDP 2–8 cm 正常。` : dead
- `tools/obstetrics/biyun-pearlzhishu-shibailv.html` : `指数 = （意外妊娠数 × 12 × 100` : dead
- `tools/obstetrics/cycle-8.html` : `：排卵前 <7mm 可能影响着床；>14mm 需警惕内膜病变` : dead
- `tools/obstetrics/down-screening.html` : `母血胎儿DNA，对21/18/13三体检出率>99%，假阳性<1%` : dead
- `tools/obstetrics/ectopic-hcg.html` : `hCG阳性+超声未见宫内孕囊(需排除hCG<2000的"鉴别区")` : dead
- `tools/obstetrics/ectopic-hcg.html` : `升高 < 53%` : dead
- `tools/obstetrics/ectopic-hcg.html` : `正常宮内孕婚 48h hCG 增幅≥ 66%（<1500）/≥ 53%（1500–3000）/≥ 30%（>3000）；≤ 正常下限需警惕异位孕婚。` : dead
- `tools/obstetrics/ectopic-hcg.html` : `注：hCG越高倍增越慢。初始hCG<1500时48h应升高≥66%为宫内妊娠；升高<53%高度怀疑异位妊娠或流产。` : dead
- `tools/obstetrics/fetal-movement-count.html` : `12 小时肾动数 = (早 + 中 + 晚 各段计数) × 4；≥ 30 正常，20–29 临界，< 20 偏少` : dead
- `tools/obstetrics/labor-curve.html` : `宫口扩张<1cm/h×4h为活跃期延长` : dead
- `tools/obstetrics/ovarian-reserve.html` : `AMH 分级：<0.5 极低、<1.0 低、<3.5 正常、<6.0 偏高、≥ 6.0 极高；FSH < 10 正常；AFC ≥ 8 正常` : dead
- `tools/obstetrics/postpartum-hemorrhage.html` : `失血量 ≥ 500 mL 为产后出血；SI < 0.9 正常、0.9–1.1 轻度、1.1–1.5 中度、> 1.5 重度伤克。` : dead
- `tools/obstetrics/preeclampsia-prediction.html` : `血管生成比值 = sFlt-1 / PlGF；< 38 排除（1周 NPV 99.3%），38–85(早发)/110(晚发) 灰色区，≥ 阈值 确诊` : dead
- `tools/obstetrics/yangshuizhishu-afi-zhengchangfanwei.html` : `AFI < 5 cm 羊水过少、5–8 cm 临界、8–25 cm 正常、> 25 cm 羊水过多；MVP < 2 过少、2–8 正常、> 8 过多。` : dead
- `tools/obstetrics/yangshuizhishu-afi-zhengchangfanwei.html` : `AFI = 四象限羊水池深度之和；MVP = 最大垂直羊水池深度` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/obstetrics/calc-50.html` : `出血量 = 血容量 × (Hct前 − Hct后) / Hct前` : fragment
  - `tools/obstetrics/rater-26.html` : `<3次/天 (1分)` : dynamic

### ophthalmology（dead 12 / dynamic 6 / fragment 1 / harmless 0）

- `tools/ophthalmology/convert-42.html` : `20 英尺（20/xx）与 6 米（6/xx）记法如何统一？` : dead
- `tools/ophthalmology/convert-42.html` : `两套分子只是检查距离不同：6/6 ≡ 20/20、6/12 ≡ 20/40。统一先转小数（分子/分母），再转 logMAR 或五分记录法，结果一致。` : dead
- `tools/ophthalmology/corneal-endothelium.html` : `CD ≥ 2500 正常、1500–2500 临界、< 1500 低密度；CV < 0.30 正常、0.30–0.40 临界、> 0.40 异常；六角形比例 ≥ 55% 正常、50%–55% 临界。` : dead
- `tools/ophthalmology/iol-power.html` : `SRK II：P = A′ − 0.9K − 2.5L（A′ 随眼轴分段校正）；SRK/T：P = 1336/(AL − ELP) − 1336/(1336/K − ELP)，ELP = pACD + H，pACD = 0.62467A − 68.747，R = 337.5/K，H = R − √(R² − (Cw/2…(+100字)` : dead
- `tools/ophthalmology/iop-correction.html` : `CCT 偏离均值越远、各经验系数差异越大；均值可减低单一公式偏差，但校正值仍不能替代直接眼压测量。` : dead
- `tools/ophthalmology/iop-correction.html` : `Ehlers=18+(520−550)×0.071=15.87；Doughty=18+(542−550)×0.02=17.84；Feltgen=18+(550−550)×0.03=18；三式均值≈17.2 mmHg（比值法=17.02，仅参考）。` : dead
- `tools/ophthalmology/iop-correction.html` : `三公式差异大说明什么？` : dead
- `tools/ophthalmology/iop-correction.html` : `同时给 Ehlers/Doughty/Feltgen 三种已发表公式并取均值；比值法仅作换算参考，不纳入均值。` : dead
- `tools/ophthalmology/iop-correction.html` : `眼压角膜厚度多公式校正：Ehlers = IOP +（520 − CCT）× 0.071；Doughty = IOP +（542 − CCT）× 0.020；Feltgen = IOP +（550 − CCT）× 0.030；比值法 = IOP × 520 ÷ CCT。取 Ehlers/Doughty/Feltgen …(+49字)` : dead
- `tools/ophthalmology/iop-correction.html` : `眼压角膜厚度多公式校正：Ehlers = IOP +（520 − CCT）× 0.071；Doughty = IOP +（542 − CCT）× 0.020；Feltgen = IOP +（550 − CCT）× 0.030；比值法 = IOP × 520 ÷ CCT；取四式均值与最值，CCT 小于500μm 读数偏低…(+2字)` : dead
- `tools/ophthalmology/osdi-scale.html` : `OSDI = (各题得分之和 × 100) / (已答题数 × 4)` : dead
- `tools/ophthalmology/visual-acuity-converter.html` : `每行 5 个字母、每字母 0.02 log 单位：logMAR = 1.10 &minus; 0.02 &times; 正确字母数；0–70 字母，20/20 = 55、20/10 = 70、&lt;20/200 计 0` : dead

  其它成因样例（共 7 条，仅列前 5）：
  - `tools/ophthalmology/convert-42.html` : `请输入有效数值：小数视力 0.01–2.0、logMAR −0.3–2.0、Snellen 分母 2–400（20/xx）；空值或越界不换算。` : dynamic
  - `tools/ophthalmology/iol-power.html` : `SRK II：P = A′ − 0.9K − 2.5L（A′ 随眼轴分段校正）；SRK/T：P = 1336/(AL − ELP) − 1336/(1336/K − ELP)，ELP = pACD + H，pACD = 0.62467A − 68.747，R = 337.5/K，H = R − √(R² − (Cw/2…(+3字)` : fragment
  - `tools/ophthalmology/iol-power.html` : `请输入有效参数：眼轴 15–36 mm、角膜曲率 30–60 D、A 常数 100–130；空值或越界不做计算。` : dynamic
  - `tools/ophthalmology/iop-correction.html` : `请输入有效眼压（1–80 mmHg）与角膜中央厚度（300–800 μm）；空值或越界不做校正。` : dynamic
  - `tools/ophthalmology/iop-correction.html` : `校正后眼压(三公式估算均值)：` : dynamic

### optical（dead 14 / dynamic 0 / fragment 1 / harmless 0）

- `tools/optical/checker-stress.html` : `光学元件双折射：精密级<10nm/cm，普通级<50nm/cm` : dead
- `tools/optical/checker-stress.html` : `钢化玻璃残余应力：表面压应力应>90MPa，中心张应力<45MPa` : dead
- `tools/optical/convergence-near-point.html` : `集合近点过远(>10cm)提示集合不足，常见于阅读疲劳、复视；过近(<3cm)可能集合过强。需结合聚散功能综合评估。` : dead
- `tools/optical/driving-lens.html` : `夜间驾驶严禁使用深色太阳镜（VLT<75%），会严重影响视野和反应速度。` : dead
- `tools/optical/gaussian-beam-waist.html` : `w₀ = 4λf/(πD) 计算束腰半径` : dead
- `tools/optical/lens-maker.html` : `符号约定：凸面 R>0、凹面 R<0（光线从左入射）。` : dead
- `tools/optical/lens-power-diopter.html` : `屈光度单位 D = m⁻¹；凸透镜 P>0（远视/老花），凹透镜 P<0（近视）。` : dead
- `tools/optical/mirror-imaging.html` : `凹面镜 f>0、凸面镜 f<0（此处曲率半径符号决定）。` : dead
- `tools/optical/peripheral-defocus.html` : `RPD>0 为近视性离焦，RPD<0 为远视性离焦；结合镜片类型评估近视防控效能。` : dead
- `tools/optical/peripheral-defocus.html` : `相对周边离焦 RPD = 周边屈光度 − 中央屈光度（D）` : dead
- `tools/optical/pupil-height.html` : `瞳高占 B 值比例 = 瞳高(mm) / 镜框 B 值(mm) × 100%` : dead
- `tools/optical/snell-refraction.html` : `n₁·sinθ₁ = n₂·sinθ₂ 计算折射角` : dead
- `tools/optical/thin-lens-imaging.html` : `1/f = 1/u + 1/v（实物距 u>0，凸透镜 f>0）。 像距 v>0 为实像（屏可接收），v` : dead
- `tools/optical/thin-lens-imaging.html` : `像距 v>0 为实像（屏可接收），v<0 为虚像；放大率 m<0 表示倒立。` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/optical/frame-pupillary.html` : `单眼移心量 = (A + DBL) / 2 − PD / 2` : fragment

### optics（dead 3 / dynamic 3 / fragment 0 / harmless 0）

- `tools/optics/magnification-optics.html` : `|M|>1 放大、<1 缩小。` : dead
- `tools/optics/mirror-equation.html` : `凹镜 f>0、凸镜 f<0。` : dead
- `tools/optics/single-slit-diffraction.html` : `sinθ = mλ。 第一暗纹 m=1。` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/optics/single-slit-diffraction.html` : `⚠ 缝宽 a 必须大于 0。` : dynamic
  - `tools/optics/single-slit-diffraction.html` : `⚠ 波长 λ 必须大于 0（λ=0 不会形成衍射条纹）。` : dynamic
  - `tools/optics/single-slit-diffraction.html` : `⚠ 暗纹级次 m 必须为非零整数（±1、±2、±3…）；0 级是中央亮纹，不是暗纹。` : dynamic

### pediatrics（dead 23 / dynamic 29 / fragment 3 / harmless 2）

- `tools/pediatrics/assessor-spo2.html` : `SpO2 <90%（任何部位）：CCHD筛查阳性，需紧急评估` : dead
- `tools/pediatrics/assessor-spo2.html` : `早产儿（<37周）` : dead
- `tools/pediatrics/diarrhea-dehydration.html` : `Plan C：静脉补液 100 mL/kg，3–6 小时；<12 月：30 mL/kg 1 小时内 + 70 mL/kg 5 小时；≥12 月：30 mL/kg 30 分钟内 + 70 mL/kg 2.5 小时` : dead
- `tools/pediatrics/diarrhea-dehydration.html` : `核心计算公式（按输入变量）：weight×deficit×1000；freq×10×weight÷10` : dead
- `tools/pediatrics/mchat-autism.html` : `提示：M-CHAT-R适用于16-30月龄儿童。关键题项(2,5,12)：若任何关键题未通过，即使总分<3也需随访。关键题：5(对呼名反应)、2(对兴趣指物)、12(模仿)。筛查阳性≠确诊ASD，需经ADOS/ADI-R等诊断评估确认。ASD核心症状：社交沟通障碍、刻板重复行为、兴趣狭窄。18月和24月是推荐筛查时间点…(+11字)` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `48 小时 TSB 10 mg/dL、胎龄 38 周：位于 p40–p75 之间（中低危险区）；低危足月儿 48–72h 光疗阈值 18 mg/dL，10<18 暂不需光疗，密切监测随访。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `48 小时 TSB 14 mg/dL、胎龄 38 周：Bhutani ≥95 百分位（P95≈12），属高危险区；本页 AAP 2004 低危光疗阈值 18，14<18 暂不需光疗，但需密切随访并按 AAP 2022 阈值复核。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `48h 同值 14：中危（≥38 周伴危险因素或 35–37 周无危险因素）阈值 15，未达；高危（35–37 周伴危险因素）阈值 13，已超过需光疗；<35 周应按 2022 AAP 早产儿曲线复核。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `光疗/换血阈值为 AAP 2004 小时胆红素曲线近似值（AAP 2022 已取代 2004，临床以 2022 版为准），需临床复核；胎龄 <35 周应按 2022 AAP/NICHD 早产儿曲线单独评估。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `光疗阈值(mg/dL)` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `同值若 35–37 周且无危险因素（本页中危 48–72 h 阈值 15），14<15 暂不达光疗；若伴危险因素（高危阈值 13），14≥13 需光疗；<35 周应按 2022 AAP 早产儿曲线复核。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `如 14` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `换血阈值(mg/dL)` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `表中为≥38 周、无神经毒性风险因素足月儿的 AAP 2004 小时胆红素曲线近似阈值（与本工具计算口径一致）。AAP 2022（Kemper et al., Pediatrics 2022;150(3):e2022060643）已取代 AAP 2004，临床应以 2022 版小时胆红素阈值图为准。35–37 周或存在…(+54字)` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `表中为≥38 周、无神经毒性风险因素足月儿的阈值（与本工具计算口径一致）。35–37 周或存在溶血/G6PD/败血症等风险因素时按中危下调约 2 mg/dL，<35 周按高危下调约 4–5 mg/dL。` : dead
- `tools/pediatrics/pediatric-anemia.html` : `1 岁属 6–23 月档，Hb 阈值 105；Hb 90 为中度贫血（70–99）；铁蛋白<12、MCV<70→缺铁性，铁剂 4mg/kg×10kg=40mg/日。` : dead
- `tools/pediatrics/pediatric-anemia.html` : `提示：缺铁性贫血(IDA)是最常见的儿童贫血类型。铁缺乏分三期：1.铁减少期(SF<12μg/L,Hb正常)；2.缺铁性红细胞生成(SF<12,MCV<正常,Hb正常)；3.缺铁性贫血(SF<12,MCV低,Hb低)。补铁首选口服二价铁(元素铁3-6mg/kg/日)，餐间服用+维C促吸收。治疗4周复查Hb，纠正后继续补…(+45字)` : dead
- `tools/pediatrics/pediatric-anemia.html` : `提示：铁缺乏分三期：1.铁减少期(SF<12μg/L,Hb正常)；2.缺铁性红细胞生成(SF<12,MCV<正常,Hb正常)；3.缺铁性贫血(SF<12,MCV低,Hb低)。补铁首选口服二价铁(元素铁3-6mg/kg/日)，餐间服用+维C促吸收。治疗4周复查Hb，纠正后继续补铁2-3月补足储存铁。早产儿2周龄起预防性补…(+23字)` : dead
- `tools/pediatrics/pediatric-asthma.html` : `提示：C-ACT适用于4-11岁儿童(7道题由儿童自答+家长答)，ACT适用于≥12岁。评估近4周情况。哮喘长期管理目标：达到并维持控制，预防急性发作，维持正常肺功能。ICS(吸入糖皮质激素)是长期控制首选。急性发作PEF<60%预计值需就医。本工具仅供临床参考，不替代专业医疗评估。` : dead
- `tools/pediatrics/pediatric-pneumonia.html` : `提示：呼吸增快是诊断肺炎最敏感的体征。胸凹陷(下胸壁内陷)提示重症。低氧血症(SpO2<90%)需氧疗。新生儿肺炎表现不典型(口吐白沫/呼吸暂停)。重度肺炎需排查并发症(脓胸/脓气胸/ARDS)。本工具仅供临床参考。` : dead
- `tools/pediatrics/rater-27.html` : `Z < -3：严重低于标准；Z < -2：中度低于标准；Z > 2：高于标准；Z > 3：严重高于标准` : dead
- `tools/pediatrics/xinshengerhuangdan-xiaoshidanhongsu-quxian.html` : `Bhutani ≥95 百分位（48h P95≈12）；低风险 AAP 2022 简化光疗阈值 13.5 mg/dL → 14≥13.5，需光疗。` : dead
- `tools/pediatrics/xinshengerhuangdan-xiaoshidanhongsu-quxian.html` : `胎龄<38 周或高危，48h 光疗阈值降至≈11 mg/dL，列线图整体左移。` : dead

  其它成因样例（共 34 条，仅列前 5）：
  - `tools/pediatrics/dehydration-assessment.html` : `请输入有效体重（0.5–100 kg）；空值或越界不做判读。` : dynamic
  - `tools/pediatrics/dehydration-assessment.html` : `按需口服补液，继续喂养；无需静脉补液。` : dynamic
  - `tools/pediatrics/diarrhea-dehydration.html` : `请输入有效年龄（0–60 月）、体重（0.5–100 kg）、腹泻次数（1–30 次/日）与病程（0–30 天）；空值或越界不做判读。` : dynamic
  - `tools/pediatrics/diarrhea-dehydration.html` : `补液方案（WHO 2005 Plan A/B/C）` : dynamic
  - `tools/pediatrics/diarrhea-dehydration.html` : `Plan A：每次稀便后补充 ORS，<2 岁 50–100 mL/次、≥2 岁 100–200 mL/次` : dynamic

### pet（dead 15 / dynamic 2 / fragment 3 / harmless 6）

- `tools/pet/checker-16.html` : `合规等级：≥90分优秀，75-89良好，60-74一般，<60不合格` : dead
- `tools/pet/index.html` : `宠物养护工具集合收录了 9 个免费在线工具，覆盖宠物养护场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/pet/index.html` : `宠物喂食量计算` : dead
- `tools/pet/index.html` : `宠物喂食量计算是一款免费的在线宠物养护工具，宠物喂食量计算是一款免费的在线宠物养护工具，输入参数即可实时得出结果；纯前端运行、数据不上传、无需注册，打开浏览器即可使用。纯前端运行、数据不上传、无需注…` : dead
- `tools/pet/pet-age-converter.html` : `犬种体型/猫龄类型` : dead
- `tools/pet/pet-age-converter.html` : `犬龄换算人类年龄：前 2 年每年折约 12 至 15 岁（1 岁约 15 岁、2 岁约 24 岁），其后按体型每年加 4 至 7 岁（小型犬 4、中型 5、大型 6、超大型 7）；猫龄前 2 年分别折 15 岁与 9 岁，其后每年加 4 岁；人类等效年龄超过 7 岁为成年后期、超过 10 岁为老年期，应加强关节、口腔与…(+7字)` : dead
- `tools/pet/pet-age-converter.html` : `狗狗猫咪年龄转换为人类等效年龄（仅近似参考）。` : dead
- `tools/pet/pet-feeding-calc.html` : `/ 宠物喂食量计算` : dead
- `tools/pet/pet-feeding-calc.html` : `中等活动` : dead
- `tools/pet/pet-feeding-calc.html` : `增重/增肌` : dead
- `tools/pet/pet-feeding-calc.html` : `按体重、年龄与活动度估算日均热量需求与日喂粮量（g）。` : dead
- `tools/pet/pet-feeding-calc.html` : `活动等级` : dead
- `tools/pet/pet-feeding-calc.html` : `静息能量需求 RER(kcal/天) = 70 × 体重(kg) 的 0.75 次方；每日能量需求 DER = RER × 系数（幼年 2.5 至 3.0、绝育成年 1.6、未绝育成年 1.8、老年 1.2 至 1.4、减重期 0.8 至 1.0、增重期 1.2 至 1.8）；每日喂食量(g) = DER ÷ 每克饲料…(+47字)` : dead
- `tools/pet/pet-feeding-calc.html` : `非常活跃` : dead
- `tools/pet/pet-feeding-calc.html` : `食物热量（kcal/100g）` : dead

  其它成因样例（共 11 条，仅列前 5）：
  - `tools/pet/aquarium-light.html` : `🎯 水草光照需求分类` : harmless
  - `tools/pet/pet-age-converter.html` : `🐾 宠物年龄换算` : harmless
  - `tools/pet/pet-age-converter.html` : `/ 宠物年龄换算` : fragment
  - `tools/pet/pet-age-converter.html` : `📖 查看「pet-age-converter 使用指南」` : harmless
  - `tools/pet/pet-age.html` : `🐾 宠物年龄换算` : harmless

### petrochem（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/petrochem/pipe-pressure.html` : `过渡流：流量 100 m³/h、管径 200 mm、管长 500 m、密度 900、黏度 50 mPa·s、粗糙度 0.1 mm。流速=0.884 m/s；Re=ρvD/μ=900×0.884×0.2/0.05≈3183(湍流区)；Swamee-Jain f≈0.0442；总压降=0.0442×(500/0.2)×(9…(+166字)` : dead

### photo（dead 23 / dynamic 0 / fragment 3 / harmless 0）

- `tools/photo/bracketing-plan.html` : `张数 = 范围/步进 + 1；覆盖 [基准−范围/2, 基准+范围/2]` : dead
- `tools/photo/card-capacity.html` : `张数 = 容量(GB)×1000 / 单张大小(MB)` : dead
- `tools/photo/convert-focal.html` : `千视场角换算` : dead
- `tools/photo/convert-focal.html` : `千镜头焦距` : dead
- `tools/photo/convert-focal.html` : `毫视场角换算` : dead
- `tools/photo/convert-focal.html` : `毫镜头焦距` : dead
- `tools/photo/depth-of-field.html` : `H = f²/(N·c) + f；近/远 = H·S/(H±(S−f))` : dead
- `tools/photo/dpi.html` : `DPI = 像素数 / 英寸长度` : dead
- `tools/photo/dpi.html` : `英寸 = 厘米 / 2.54` : dead
- `tools/photo/dynamic-range.html` : `DR = log₂(最亮/最暗)` : dead
- `tools/photo/flash-gn.html` : `光圈 = GN / 距离（ISO100）` : dead
- `tools/photo/golden-hour.html` : `日长 = 2·acos(−tanφ·tanδ)/15 小时` : dead
- `tools/photo/macro-magnification.html` : `放大率 m = f/(S−f)` : dead
- `tools/photo/nd-filter.html` : `新快门 = 基准 × 2^档数` : dead
- `tools/photo/photo-10.html` : `张数 = 2 × ceil(总范围 / 步长) + 1` : dead
- `tools/photo/photo-3.html` : `ISO 加倍，距离 ×√2` : dead
- `tools/photo/photo-5.html` : `对焦 H 时，景深从 H/2 到无穷远` : dead
- `tools/photo/photo-6.html` : `视角 = 2 · arctan(传感器边长 / (2 · 焦距))` : dead
- `tools/photo/photo-7.html` : `放大倍率 = 成像大小 / 实际大小` : dead
- `tools/photo/photo-8.html` : `压缩后 ≈ 未压缩 / 压缩比` : dead
- `tools/photo/photo-8.html` : `未压缩大小 = 像素数 × 位深 / 8` : dead
- `tools/photo/raw-size.html` : `大小 = 像素 × 位深 / 8` : dead
- `tools/photo/safe-shutter.html` : `安全快门 ≈ 1/(焦距 × 裁剪系数)` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/photo/convert-focal.html` : `镜头焦距` : fragment
  - `tools/photo/convert-focal.html` : `视场角换算` : fragment
  - `tools/photo/equivalent-focal.html` : `等效焦距 = 实际焦距 × 裁剪系数` : fragment

### photo2（dead 1 / dynamic 5 / fragment 0 / harmless 0）

- `tools/photo2/exposure-triangle.html` : `EV（曝光值）Formula:` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/photo2/exposure-triangle.html` : `调整档位` : dynamic
  - `tools/photo2/exposure-triangle.html` : `ISO（固定）` : dynamic
  - `tools/photo2/exposure-triangle.html` : `偏差` : dynamic
  - `tools/photo2/exposure-triangle.html` : `等量曝光：固定 ISO，光圈按 2^(s/2)、快门按 2^s 同时调整，保持 N²/t 不变，总进光量不变` : dynamic
  - `tools/photo2/exposure-triangle.html` : `请选择有效的光圈、快门与 ISO（ISO 不能为空）。` : dynamic

### plastic（dead 1 / dynamic 2 / fragment 1 / harmless 0）

- `tools/plastic/extrusion-rate.html` : `螺杆直径 10 mm、螺槽深 1 mm、螺距 5 mm、转速 10 rpm、密度 0.92、效率 90%。流道截面积 = π/4×(10²−(10−2)²) = π/4×36 ≈ 28.27 mm²；每转排量 28.27×5 ≈ 141.4 mm³；每分钟 1414 mm³、每秒 23.6 mm³；质量产量 = 23.…(+64字)` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/plastic/extrusion-rate.html` : `请输入有效参数：所有参数需大于 0，输送效率需在 0–100% 之间` : dynamic
  - `tools/plastic/extrusion-rate.html` : `请输入有效参数：螺槽深度过大，请检查` : dynamic
  - `tools/plastic/injection-cycle.html` : `注塑成型周期 = 注射 + 保压 + 冷却 + 开模 + 顶出 + 关模` : fragment

### pr（dead 1 / dynamic 2 / fragment 2 / harmless 0）

- `tools/pr/assessor-59.html` : `关键信息渗透率 = 包含核心传播信息的报道/总报道` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/pr/analysis-density-1.html` : `总词数 = 中文字符数 + 英文单词数` : fragment
  - `tools/pr/analysis-density-1.html` : `关键词密度 = 关键词出现次数 ÷ 总词数 × 100%` : fragment
  - `tools/pr/assessor-59.html` : `2-正面<40%` : dynamic
  - `tools/pr/assessor-59.html` : `1-<20%覆盖` : dynamic

### printing（dead 7 / dynamic 15 / fragment 6 / harmless 0）

- `tools/printing/analysis-7.html` : `平均亮度 L̄ = Σ Li ÷ n` : dead
- `tools/printing/convert-gsm.html` : `千厚度换算` : dead
- `tools/printing/convert-gsm.html` : `千纸张克重` : dead
- `tools/printing/convert-gsm.html` : `毫厚度换算` : dead
- `tools/printing/convert-gsm.html` : `毫纸张克重` : dead
- `tools/printing/estimate-ink.html` : `损耗墨量(5%)` : dead
- `tools/printing/sheet-calc.html` : `全张用纸量 = 印张 × 册数 × (1 + 加放率)` : dead

  其它成因样例（共 21 条，仅列前 5）：
  - `tools/printing/analysis-7.html` : `照度均匀度 U₁ = 最小亮度 ÷ 平均亮度` : fragment
  - `tools/printing/box-area.html` : `表面积 = 2×(L×W + L×H + W×H)` : fragment
  - `tools/printing/convert-gsm.html` : `纸张克重` : fragment
  - `tools/printing/convert-gsm.html` : `厚度换算` : fragment
  - `tools/printing/convert-gsm.html` : `定量 GSM 需填写大于 0 的数值（g/m²）` : dynamic

### process（dead 10 / dynamic 1 / fragment 0 / harmless 0）

- `tools/process/cp-index.html` : `σ=0.01 → Cp=1.667。 Cp≥1.33 通常视为合格。` : dead
- `tools/process/cpk-index.html` : `Cpk=Cp。 Cpk≥1.33 为过程能力充足。` : dead
- `tools/process/defect-probability.html` : `z=5 → 概率约 2.87e-7。 对称时总缺陷为两侧之和。` : dead
- `tools/process/dpmo-calc.html` : `20000×1e6 = 6200 DPMO。 机会数指可缺陷的特征数。` : dead
- `tools/process/first-pass-yield.html` : `FPY = 良品数 / 投入数` : dead
- `tools/process/measurement-uncertainty.html` : `√0.38≈0.616。 分量应相互独立。` : dead
- `tools/process/rolled-throughput-yield.html` : `98%×97%×99% ≈ 94.11%。 工序越多 RTY 越低。` : dead
- `tools/process/tolerance-rss.html` : `√0.0725≈0.269。 RSS 比最差情况宽松。` : dead
- `tools/process/tolerance-worst-case.html` : `0.2 = 0.45。 最差情况偏保守。` : dead
- `tools/process/xbar-control-limits.html` : `σ=2、n=5 → 界限 ±2.683。 σ/√n 为均值标准误。` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/process/cpk-index.html` : `⚠ 输入无效：过程标准差 σ 须大于 0，且上规格限 USL 须大于下规格限 LSL。` : dynamic

### procurement（dead 7 / dynamic 1 / fragment 0 / harmless 0）

- `tools/procurement/assessor-26.html` : `供应商准入分 = 指标加权` : dead
- `tools/procurement/assessor-26.html` : `分级标准：≥85分战略供应商，70-84优选，60-69合格，<60淘汰` : dead
- `tools/procurement/rater-price.html` : `供应商评分 = 综合加权` : dead
- `tools/procurement/stats-on-time-1.html` : `准时 255 批、合格 270 批、准时且合格 240 批。准时率=255/300=85.00%，良品率=270/300=90.00%，联合合格率=240/300=80.00%，准时不良率=(255−240)/300=5.00%，未达标率=(300−240)/300=20.00%。` : dead
- `tools/procurement/stats-on-time-1.html` : `输入当月交货总批次、准时批次、合格批次与「准时且合格」批次（取交集），自动计算准时率、良品率、联合合格率、准时但不良率与未达标率，用于供应商绩效考评。` : dead
- `tools/procurement/supplier-score.html` : `综合评分 = 质量×交期×价格×服务` : dead
- `tools/procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi.html` : `金额≥400 且 公开→公开招标；金额≥400 且 限定→邀请招标；金额<400→竞争性谈判` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi.html` : `💡 金额≥400 且公开→公开招标；限定→邀请招标；<400→竞争性谈判。` : dynamic

### project（dead 1 / dynamic 3 / fragment 6 / harmless 0）

- `tools/project/analysis-28.html` : `关注度 = 权力 × 利益；按「高/低权 × 高/低利」落入四象限` : dead

  其它成因样例（共 9 条，仅列前 5）：
  - `tools/project/assessor-risk-9.html` : `1-极低（<10%）` : dynamic
  - `tools/project/checker-training-hr-1.html` : `HSE 关键项存在 0 分项，触发一票否决规则：不得评为优秀或合格，本次评级降为不合格；请立即整改关键项后重新评估。` : dynamic
  - `tools/project/checker-training-hr-1.html` : `不达标关键项` : dynamic
  - `tools/project/checker-training-hr-1.html` : `安全培训档案` : fragment
  - `tools/project/checker-training-hr-1.html` : `特种作业持证` : fragment

### property（dead 11 / dynamic 0 / fragment 0 / harmless 0）

- `tools/property/calc-shared-property-fee.html` : `物业费 = 面积 × 单价` : dead
- `tools/property/checker-7.html` : `综合得分≥85分为优秀，70-84分为良好，55-69分为合格，<55分为不合格` : dead
- `tools/property/cleaning-allocation.html` : `保洁分配 = 区域/频次覆盖` : dead
- `tools/property/elevator-energy.html` : `电梯能耗 = 次数 × 单次能耗` : dead
- `tools/property/energy.html` : `运费 = 重量 × 运费率（元/kg）；吨均运费 = 运费率 × 1000` : dead
- `tools/property/fee-allocation.html` : `物业费分摊 = 面积比例` : dead
- `tools/property/irrigation-schedule.html` : `浇灌排程 = 需水量/流量` : dead
- `tools/property/rater-performance.html` : `绩效考核 = 指标加权评分` : dead
- `tools/property/rater-performance.html` : `💡 加权得分 = Σ(各维度得分 × 权重) / Σ权重。考核等级：A级(≥90)优秀 / B级(80-89)良好 / C级(70-79)合格 / D级(60-69)待改进 / E级(<60)不合格。维度得分参考：满意度调查均分、设施完好率、工单响应时间达标率、实际收费率、安全检查通过率、环境巡查合格率。` : dead
- `tools/property/stats-manager.html` : `临停位周转率 = 当日临停车次 ÷ 临停车位` : dead
- `tools/property/stats-manager.html` : `预计月收入 = 临停车次 × 时长 × 单价 × 30 + 包月车位 × 月租` : dead

### psychiatry（dead 2 / dynamic 0 / fragment 0 / harmless 0）

- `tools/psychiatry/eat26-eating.html` : `EAT-26总分 = Σ26个条目（含反向计分条目按REVERSE/NORMAL加权）；<20低风险、≥20提示进食障碍风险，需专业评估。` : dead
- `tools/psychiatry/rater-24.html` : `心理韧性总分 = Σ各条目（0-4），满分 = 题数×4；得分率 = 总分÷满分×100%；≥80高韧性、65-79中高、50-64中等、<50待提升。` : dead

### pulmonology（dead 11 / dynamic 25 / fragment 1 / harmless 0）

- `tools/pulmonology/lung-rads.html` : `实性结节 6mm→2 类，12 月低剂量 CT 随访。` : dead
- `tools/pulmonology/lung-rads.html` : `部分实性>10mm` : dead
- `tools/pulmonology/lung-rads.html` : `部分实性成分>10mm→4A/4B 类，建议 3 月复查或 PET-CT/活检。` : dead
- `tools/pulmonology/pneumothorax.html` : `气胸肺压缩比 ≈ 三处肋间测量平均距离 × 10（上限 100%）；压缩 小于20% 且无症状可观察并吸高浓度氧，继发性或张力性气胸需胸腔闭式引流或紧急排气。` : dead
- `tools/pulmonology/pulmonary-function.html` : `本工具 cutoff 可设(默认 0.7)，老年建议按 LLN。` : dead
- `tools/pulmonology/rater-13.html` : `三分类法：<2分低风险，2-6分中风险，>6分高风险` : dead
- `tools/pulmonology/respiratory-failure.html` : `氧合指数 P/F = PaO₂ / FiO₂` : dead
- `tools/pulmonology/tb-resistance.html` : `MDR/RR + 耐氟喹诺酮 + 耐至少一种二线注射剂` : dead
- `tools/pulmonology/tb-resistance.html` : `MDR/RR + 耐氟喹诺酮 或 二线注射剂` : dead
- `tools/pulmonology/tb-resistance.html` : `提示：涂片阳性提示传染性强，需呼吸道隔离。GeneXpert利福平耐药需经表型药敏确认。BPaL/BPaLM方案(贝达喹啉+普托马尼+利奈唑胺±莫西沙星)适用于≥6岁、无氟喹诺酮及注射剂耐药的MDR/RR-TB。仅供临床参考。` : dead
- `tools/pulmonology/tb-resistance.html` : `结核耐药分型：无利福平及异烟肼耐药为药物敏感结核 DS-TB（2HRZE/4HR）；耐利福平为 RR-TB、同时耐异烟肼为耐多药 MDR-TB、再加氟喹诺酮及二线注射剂耐药为广泛耐药 XDR-TB，据耐药谱选方案。` : dead

  其它成因样例（共 26 条，仅列前 5）：
  - `tools/pulmonology/niv-settings.html` : `压力支持 PS = IPAP − EPAP` : dynamic
  - `tools/pulmonology/pneumothorax.html` : `依据立位后前位胸片测量胸膜间距，采用 Rhea 法估算气胸肺压缩百分比` : dynamic
  - `tools/pulmonology/pneumothorax.html` : `请填写 A/B/C 三处胸膜间距（≥0 的有效数字）；空值或负值不会被当作 0 给出压缩比例。` : dynamic
  - `tools/pulmonology/pneumothorax.html` : `三处胸膜间距均为 0，无法估计气胸压缩比例；请核对测量值。` : dynamic
  - `tools/pulmonology/pneumothorax.html` : `创伤性气胸需先按 ATLS 评估合并伤，排查开放性/张力性气胸与血气胸；多数需胸腔闭式引流，由急诊/创伤团队复核。` : dynamic

### quality（dead 4 / dynamic 0 / fragment 1 / harmless 0）

- `tools/quality/convert-qualified-defect.html` : `千PPM换算` : dead
- `tools/quality/convert-qualified-defect.html` : `千不合格品率` : dead
- `tools/quality/convert-qualified-defect.html` : `毫PPM换算` : dead
- `tools/quality/convert-qualified-defect.html` : `毫不合格品率` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/quality/convert-qualified-defect.html` : `不合格品率` : fragment

### quantum（dead 5 / dynamic 9 / fragment 1 / harmless 0）

- `tools/quantum/cyclotron-frequency.html` : `ω = qB/m（与速度无关）。 用于回旋加速器设计。` : dead
- `tools/quantum/pair-production-threshold.html` : `光子产生正负电子对所需最小能量。` : dead
- `tools/quantum/pair-production-threshold.html` : `需 ≥ 两电子静能之和。` : dead
- `tools/quantum/photoelectric-effect.html` : `K_max = hf − φ。 f 需 > φ/h 才逸出。` : dead
- `tools/quantum/rydberg-wavelength.html` : `R≈1.097e7 m⁻¹。 n:3→2 为巴耳末 α 线 ≈ 656 nm。` : dead

  其它成因样例（共 10 条，仅列前 5）：
  - `tools/quantum/infinite-well-energy.html` : `⚠ 量子数 n 必须为正整数（1、2、3…），不能为 0、负数或小数。` : dynamic
  - `tools/quantum/infinite-well-energy.html` : `⚠ 粒子质量 m 必须大于 0。` : dynamic
  - `tools/quantum/infinite-well-energy.html` : `⚠ 阱宽 L 必须大于 0。` : dynamic
  - `tools/quantum/pair-production-threshold.html` : `⚠ 靶核质量数 A 须为 ≥0 的整数（0 表示不计反冲）。` : dynamic
  - `tools/quantum/pair-production-threshold.html` : `当前粒子对` : dynamic

### realestate（dead 41 / dynamic 1 / fragment 0 / harmless 0）

- `tools/realestate/analysis-24.html` : `未来价值 = 当前总价 × (1 + 年涨跌幅%)^持有年数` : dead
- `tools/realestate/assessor-23.html` : `成新率 = 1 − 已用年限/经济寿命` : dead
- `tools/realestate/assessor-38.html` : `按揭月供 = 等额本息公式` : dead
- `tools/realestate/assessor-39.html` : `计税评估值 = 计税依据 × 税率` : dead
- `tools/realestate/assessor-40.html` : `保险重置价值 = 重建成本` : dead
- `tools/realestate/assessor-42.html` : `征收补偿 = 区片价 × 面积` : dead
- `tools/realestate/assessor-43.html` : `企业价值 = 资产 − 负债（或收益法）` : dead
- `tools/realestate/assessor-44.html` : `无形资产评估 = 收益/市场/成本法` : dead
- `tools/realestate/assessor-45.html` : `涉税评估值` : dead
- `tools/realestate/assessor-return.html` : `V = NOI / 资本化率 R` : dead
- `tools/realestate/assessor-second-hand.html` : `评估值 = 可比实例价 × 修正系数` : dead
- `tools/realestate/calc-1.html` : `月供 = P·i·(1+i)^n/((1+i)^n−1)` : dead
- `tools/realestate/calc-2.html` : `租金回报率 = 年租金/总价 × 100%` : dead
- `tools/realestate/calc-70.html` : `楼面价 = 土地总价/总建筑面积` : dead
- `tools/realestate/calc-93.html` : `比较法：评估值 = 案例价 × Π修正` : dead
- `tools/realestate/calc-assessor.html` : `拆迁补偿 = 重置价 × 成新率 + 区位` : dead
- `tools/realestate/calc-cost.html` : `资本机会成本 = 替代投资收益` : dead
- `tools/realestate/calc-return.html` : `REITs 收益 = 分红/价格` : dead
- `tools/realestate/chiyou-qijianyunying-feiyong.html` : `持有费用 = 税费+维护+管理` : dead
- `tools/realestate/convert-area-shared.html` : `公摊面积 = 套内面积 × 公摊系数` : dead
- `tools/realestate/convert-area-shared.html` : `建筑面积 = 套内 + 公摊；得房率 = 套内 / 建筑面积 × 100%` : dead
- `tools/realestate/cost-depreciation.html` : `年折旧 = (重置−残值)/使用年限` : dead
- `tools/realestate/cost-depreciation-1.html` : `成本法：价值 = 重置成本 − 折旧 + 地价` : dead
- `tools/realestate/depreciation-2.html` : `房屋折旧 = (1−成新率)×重置成本` : dead
- `tools/realestate/down-payment.html` : `首付 = 总价 × 首付比例` : dead
- `tools/realestate/estimate-37.html` : `空置损失 = 潜在租金 × 空置率` : dead
- `tools/realestate/fangdichan-xintuo-jijinguzhi.html` : `REITs 估值 = 资产净值/份额` : dead
- `tools/realestate/fund-loan.html` : `公积金额度 = f(账户余额, 缴存)` : dead
- `tools/realestate/fund-loan-1.html` : `可贷额度 = 余额×倍数 或 缴存法` : dead
- `tools/realestate/layout-score.html` : `户型评分 = 综合指标加权` : dead
- `tools/realestate/market-valuation.html` : `市场比较法：评估值 = 可比价×修正` : dead
- `tools/realestate/paimai-baoliujia-qipaijia-sheding.html` : `起拍价 = 保留价×折扣` : dead
- `tools/realestate/price-discount-1.html` : `实售价 = 标价×(1−折扣率)` : dead
- `tools/realestate/rater-usable-layout.html` : `得房率 = 套内/建筑面积 × 100%` : dead
- `tools/realestate/rent-1.html` : `潜在毛收入 = 租金×面积×入住率` : dead
- `tools/realestate/return-1.html` : `净收益 = 经营收入 − 运营费用` : dead
- `tools/realestate/return-2.html` : `收益法：V = NOI / 资本化率` : dead
- `tools/realestate/shichang-bijiaofa-anlixiuzheng.html` : `案例修正 = 可比价×因素修正` : dead
- `tools/realestate/tudi-jizhundijia-luxianjia-xishuxiuzheng.html` : `路线价 = 基准价×深度×宽深修正` : dead
- `tools/realestate/xianjinliuyuce.html` : `现金流 = 经营现金流 − 资本支出` : dead
- `tools/realestate/yanglao-dichan-touzi-tuichu-jihui.html` : `投资回报 = 收益/投入` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/realestate/calc-93.html` : `💡 评估单价 = 案例单价 × 综合修正系数；修正额 = 案例单价 ×（系数 − 1）；系数 < 1 为向下修正。` : dynamic

### rehabilitation（dead 3 / dynamic 3 / fragment 0 / harmless 0）

- `tools/rehabilitation/asia-impairment-scale.html` : `损伤平面以下>半数关键肌肌力<3级` : dead
- `tools/rehabilitation/fim-scale.html` : `自己完成<25%，完全依赖他人` : dead
- `tools/rehabilitation/wheelchair-posture.html` : `核心计算公式（按输入变量）：ischialPressure ÷ 133.322；force ÷ (2 × 5)；hipW + 2` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/rehabilitation/tester-rater.html` : `1-<10秒` : dynamic
  - `tools/rehabilitation/tester-rater.html` : `1-<3秒` : dynamic
  - `tools/rehabilitation/tester-rater.html` : `4-每侧<3秒` : dynamic

### rental（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/rental/reminder-4.html` : `绿色=剩余>90天，黄色=30-90天，橙色=7-30天，红色=<7天` : dead

### reproductive-medicine（dead 11 / dynamic 0 / fragment 2 / harmless 0）

- `tools/reproductive-medicine/detector-9.html` : `判定标准：精液量 < 1.5ml 且 retroPct ≥ 50% 且 urTotal > 5×10⁶ → 显著逆行射精` : dead
- `tools/reproductive-medicine/detector-9.html` : `尿液总精子 urTotal = urVol × urConc` : dead
- `tools/reproductive-medicine/detector-9.html` : `精液总精子 ejTotal = ejVol × ejConc` : dead
- `tools/reproductive-medicine/detector-9.html` : `逆行射精诊断要点：精液量极少（常<1ml）+ 射精后尿液中发现大量精子` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `优质胚胎率 = 优质胚胎数 / 受精数 × 100%` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `卵裂率 = 卵裂数 / 受精数 × 100%` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `受精率 = 受精数 / 获卵数 × 100%` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `正常受精率 = 受精数 / MII卵数 × 100%` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `着床率 = 孕囊数 / 移植数 × 100%` : dead
- `tools/reproductive-medicine/sperm-morphology.html` : `正常形态(%) = 正常形态数 / 计数总数 × 100` : dead
- `tools/reproductive-medicine/testicular-volume.html` : `体积(mL) = 长 × 宽 × 高 × 0.71 ÷ 1000（单位 mm）` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/reproductive-medicine/epididymal-aspiration.html` : `获取精子总量(×10⁶) = 浓度(×10⁶/mL) × 体积(mL)` : fragment
  - `tools/reproductive-medicine/sperm-cryopreservation.html` : `复苏率 = 复苏后精子数 / 冻前精子数 ×100` : fragment

### research（dead 16 / dynamic 8 / fragment 5 / harmless 0）

- `tools/research/analysis-49.html` : `KMO 和 Bartlett 分别看什么？` : dead
- `tools/research/analysis-49.html` : `KMO 衡量条目间的共同方差是否足够，越接近 1 越适合做因子分析（常用 0.70 以上为可接受）；Bartlett 检验相关矩阵是否为单位阵，p<0.05 表示条目间存在相关、具备做因子分析的前提。两者都要看，KMO 低而 Bartlett 显著仍不宜直接做因子分析。` : dead
- `tools/research/analysis-49.html` : `α = k ÷ (k − 1) × (1 − Σ 条目方差 ÷ 总分方差)` : dead
- `tools/research/analysis-49.html` : `不会。本页只做可因子性检验与条目诊断，不运行主成分/主轴因子提取，也不输出载荷矩阵。需要因子结构和旋转结果时，请把数据导入统计软件（如 R、SPSS、JASP）继续分析。` : dead
- `tools/research/analysis-49.html` : `仍用上述 6×5 矩阵：相关矩阵行列式 |R| = 0.0001504，KMO = 0.553（按 Kaiser 1974 分档为「较差」）。Bartlett χ² = −[6 − 1 − (2×5+5) ÷ 6] × ln(0.0001504) = 22.006，df = 5×4 ÷ 2 = 10，p = 0.015…(+104字)` : dead
- `tools/research/analysis-49.html` : `准备做探索性因子分析前，先用 KMO 与 Bartlett 检验判断这批数据是否“值得”做因子分析。` : dead
- `tools/research/analysis-49.html` : `同一矩阵中，条目 1~5 的校正后条目-总分相关分别为 0.925、0.748、0.644、0.822、0.958；删除后的 α 分别为 0.8917、0.9268、0.9395、0.9083、0.8792。条目 3 的相关最低、删除后 α 最高（0.9395 > 0.9273），是优先复核的删题候选；条目 5 删除后…(+34字)` : dead
- `tools/research/analysis-49.html` : `同一组数据的 KMO 与 Bartlett` : dead
- `tools/research/analysis-49.html` : `总分方差按全部被试的合计得分计算` : dead
- `tools/research/analysis-49.html` : `把量表数据矩阵录入（每行一名被试、每列一个条目），计算克隆巴赫 α 系数，评估量表内部一致性信度。通常 α 达到 0.70 以上认为可靠，0.60 到 0.70 勉强可用，低于 0.60 需要修订条目。所有数据仅在浏览器本地处理，不上传。` : dead
- `tools/research/analysis-49.html` : `把量表数据矩阵录入（每行一名被试、每列一个条目），计算克隆巴赫 α 系数，评估量表内部一致性信度。通常 α 达到 0.70 以上认为可靠，0.60~0.70 勉强可用，低于 0.60 需修订条目。数据仅在浏览器本地处理，不会上传。` : dead
- `tools/research/analysis-49.html` : `本页会帮我提取因子吗？` : dead
- `tools/research/analysis-49.html` : `条目分析怎么用来删题` : dead
- `tools/research/analysis-49.html` : `量表（信度/效度/因子）分析。免费在线工具，纯前端处理，数据不上传，保护隐私安全。` : dead
- `tools/research/analysis-52.html` : `加权评分 = Σ(提及次数 × 评分) ÷ Σ提及次数` : dead
- `tools/research/analysis-54.html` : `近 5 条均含主题且未出现新主题，主题趋于饱和，可考虑停止抽样。` : dead

  其它成因样例（共 13 条，仅列前 5）：
  - `tools/research/analysis-49.html` : `结构效度（可因子性检验）` : dynamic
  - `tools/research/analysis-49.html` : `KMO 取样适切性：` : dynamic
  - `tools/research/analysis-49.html` : `Bartlett 球形检验：χ²=` : dynamic
  - `tools/research/analysis-49.html` : `条目分析（校正后条目-总分相关 / 删除该条目后的 α）` : dynamic
  - `tools/research/analysis-49.html` : `条目` : fragment

### restaurant（dead 9 / dynamic 0 / fragment 0 / harmless 4）

- `tools/restaurant/bbq-portion.html` : `关于「烧烤食材分量计算器」` : dead
- `tools/restaurant/bbq-portion.html` : `如何使用烧烤食材分量计算器？` : dead
- `tools/restaurant/bbq-portion.html` : `烧烤食材分量计算器是做什么的？` : dead
- `tools/restaurant/bbq-portion.html` : `烧烤食材分量计算器适合哪些场景？` : dead
- `tools/restaurant/hotpot-portion.html` : `关于「火锅食材分量计算器」` : dead
- `tools/restaurant/hotpot-portion.html` : `如何使用火锅食材分量计算器？` : dead
- `tools/restaurant/hotpot-portion.html` : `火锅食材分量计算器是做什么的？` : dead
- `tools/restaurant/hotpot-portion.html` : `火锅食材分量计算器适合哪些场景？` : dead
- `tools/restaurant/index.html` : `餐饮经营工具集合收录了 8 个免费在线工具，覆盖餐饮经营场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/restaurant/bbq-portion.html` : `📖 查看「烧烤食材分量计算器使用指南」` : harmless
  - `tools/restaurant/bbq-portion.html` : `📚 深度解析：烧烤食材分量计算器` : harmless
  - `tools/restaurant/hotpot-portion.html` : `📖 查看「火锅食材分量计算器使用指南」` : harmless
  - `tools/restaurant/hotpot-portion.html` : `📚 深度解析：火锅食材分量计算器` : harmless

### rheumatology（dead 9 / dynamic 1 / fragment 0 / harmless 0）

- `tools/rheumatology/basdai.html` : `CRP = 0.12×腰背痛 + 0.06×晨僵持续时间 + 0.07×患者总体 + 0.11×CRP(√)` : dead
- `tools/rheumatology/basdai.html` : `提示：BASDAI≥4是ASAS/EULAR推荐启动抗TNF生物制剂治疗的主要标准之一。BASDAI主观性较强，建议结合ASDAS(含CRP/ESR的客观指标)综合评估。ASDAS-CRP = 0.12×腰背痛 + 0.06×晨僵持续时间 + 0.07×患者总体 + 0.11×CRP(√)。仅供临床参考。` : dead
- `tools/rheumatology/essdai.html` : `高 — 肾小球肾炎/eGFR<30` : dead
- `tools/rheumatology/gout-uric-acid.html` : `提示：急性发作期不启动ULT，已用药者不停药。ULT启动初期(3-6月)需联合秋水仙碱(0.5mg 1-2次/日)预防发作。血尿酸不可降得过低(<180μmol/L)，可能与神经退行性疾病相关。每2-4周监测尿酸，达标后每6月复查。仅供临床参考。` : dead
- `tools/rheumatology/igg4-level.html` : `嗜酸性粒细胞 (×10⁹/L, 正常 <0.5)` : dead
- `tools/rheumatology/igg4-level.html` : `总IgE (IU/mL, 正常 <100)` : dead
- `tools/rheumatology/igg4-level.html` : `：IgG4+/IgG+比值>40%且>10个/HPF(+10分)；比值>40%但<10/HPF(+5分)` : dead
- `tools/rheumatology/lupus-anticoagulant.html` : `妊娠并发症：①≥10周不明原因死胎；②≥34周因子痫前期/胎盘功能不全早产；③连续3次<10周不明原因自然流产` : dead
- `tools/rheumatology/womac.html` : `标准化总分 = (原始分/96)×100` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/rheumatology/gout-uric-acid.html` : `5期 (GFR <15/透析)` : dynamic

### robotics（dead 15 / dynamic 6 / fragment 4 / harmless 0）

- `tools/robotics/battery-runtime.html` : `t = 容量(Wh) / 功耗(W)` : dead
- `tools/robotics/cable-tension-pulley.html` : `单侧绳张力 T = mg/2` : dead
- `tools/robotics/encoder-angle-resolution.html` : `四倍频后分辨率 = 360°/(4·CPR)。` : dead
- `tools/robotics/encoder-angle-resolution.html` : `输入每转脉冲数 CPR（四倍频后），求最小角度分辨率。` : dead
- `tools/robotics/encoder-angle-resolution.html` : `输入编码器每转单相脉冲数 PPR，工具按 θ_min=360°/(4·PPR)（正交四倍频）计算最小可分辨角度，说明高 PPR 提升定位精度，用于选型与运动控制分辨率评估。` : dead
- `tools/robotics/forward-kinematics-2r.html` : `θ₁=30°、θ₂=45°、L=1 → 约 (1.297, 1.207)。` : dead
- `tools/robotics/gravity-comp-torque.html` : `5kg、臂长 0.3m、水平` : dead
- `tools/robotics/gravity-comp-torque.html` : `τ = m·g·L·cosθ（水平时最大）。` : dead
- `tools/robotics/gravity-comp-torque.html` : `τ=m·g·L·cosθ=5×9.81×0.3×1=14.7 N·m（θ=0 水平最大）。` : dead
- `tools/robotics/gravity-comp-torque.html` : `水平臂重力平衡。` : dead
- `tools/robotics/gravity-comp-torque.html` : `臂与水平夹角；水平 θ=0 时重力矩最大。` : dead
- `tools/robotics/gravity-comp-torque.html` : `角度 θ (°)` : dead
- `tools/robotics/servo-pwm-angle.html` : `角度 = (脉宽−最小)/(最大−最小)×180°` : dead
- `tools/robotics/stepper-step-angle.html` : `步距角 = 360°/(步数/圈)` : dead
- `tools/robotics/wheel-odometry.html` : `ds=(1.0+1.2)/2=1.1m，dθ=(1.2−1.0)/0.4=0.5rad；前进 1.1m 并右转 0.5rad。` : dead

  其它成因样例（共 10 条，仅列前 5）：
  - `tools/robotics/encoder-angle-resolution.html` : `每转脉冲 PPR` : fragment
  - `tools/robotics/encoder-angle-resolution.html` : `⚠ 每转脉冲 PPR 必须为正整数（≥1），不能为 0、负数或小数。` : dynamic
  - `tools/robotics/inverse-kinematics-2r.html` : `θ₁ 肘下 (°)` : dynamic
  - `tools/robotics/inverse-kinematics-2r.html` : `θ₂ (°)` : dynamic
  - `tools/robotics/inverse-kinematics-2r.html` : `θ₂ 肘上 (°)` : dynamic

### sales（dead 2 / dynamic 0 / fragment 1 / harmless 0）

- `tools/sales/moving-average.html` : `SMA(3)：第3期 (100+120+110)/3 = 110；第4期 (120+110+130)/3 = 120；第5期 (110+130+140)/3 = 126.67。 ⏎ 下一期预测 = 最近窗口均值 = (110+130+140)/3 = 126.67。 ⏎ WMA(3) 权重 1/2/3，第5期 = (1…(+92字)` : dead
- `tools/sales/moving-average.html` : `核心计算公式（按输入变量）：2÷(n+1)；n×(n+1)÷2；n-1` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/sales/target-breakdown.html` : `个人目标 = 总目标 × (个人权重 ÷ 权重总和)` : fragment

