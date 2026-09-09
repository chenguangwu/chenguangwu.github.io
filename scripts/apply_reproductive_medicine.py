#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reproductive-medicine 分类 deep-dive 真实化：用真实生殖医学算例替换占位/弱泛化内容。"""
import json, re, os

F = 'i18n/tools/content_deepdive.json'
BAD_RE = re.compile(
    r'统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|'
    r'标准化，再批量|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|'
    r'高频复用模板|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|复用模板示例|'
    r'保留复用模板|先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|'
    r'先用一组可复现输入|同一输入样本测试默认和边界情况|选择两组不同来源样本并同步口径定义'
)

KB = {
'reproductive-medicine/anti-sperm-antibody': {
  'title': '抗精子抗体（ASA）判读',
  'scenarios': [
    '免疫性不育的抗体滴度评估。',
    'IgA/IgM 分型与临床意义。',
    '宫颈粘液穿透能力关联。'],
  'examples': [
    {'title': 'IgA 60% 阳性', 'body': 'IgA≥50% 判为阳性，与精子穿透宫颈粘液能力下降密切相关，建议结合配偶情况考虑免疫抑制剂或辅助生殖。'},
    {'title': 'IgM 15%', 'body': 'IgM≥10% 提示近期感染或局部免疫反应活跃，需排查生殖道炎症。'}],
  'faqs': [
    {'q': 'IgG 与 IgA 区别？', 'a': 'IgA 直接干扰精子-粘液相互作用更具临床意义；IgG 多为血清型，意义相对次要。'},
    {'q': '参考阈值？', 'a': '常用混合抗球蛋白反应（MAR）或免疫珠试验：IgA≥50%、IgM≥10% 为阳性界值。'}]},

'reproductive-medicine/assessor-15': {
  'title': '输精管造影通畅度评估',
  'scenarios': [
    '无精子症病因定位。',
    '梗阻性 vs 非梗阻性鉴别。',
    '显微外科重建术前评估。'],
  'examples': [
    {'title': '双侧各段均 2 分', 'body': '评分 0=梗阻、1=部分、2=通畅；双侧全部 2 → 双侧通畅，不支持梗阻性无精子症。'},
    {'title': '左段一处 0 分', 'body': '左某段评 0 → 左侧梗阻；若仅单侧且对侧通畅，仍有自然受孕可能，可先观察。'}],
  'faqs': [
    {'q': '评分怎么用？', 'a': '逐段（腹股沟/盆段/壶腹等）评 0–2，任一段 0 即该侧梗阻，双侧 0 为梗阻性无精子症。'},
    {'q': '下一步？', 'a': '双侧梗阻常选 PESA+ICSI；单侧可据精液参数决定是否手术探查。'}]},

'reproductive-medicine/baifenbijisuanqi': {
  'title': '百分比计算器',
  'scenarios': [
    '精液参数占比换算。',
    '活率/形态正常率百分比。',
    '通用比例计算。'],
  'examples': [
    {'title': 'PR 40 / 总 100', 'body': '前向运动占比 = 40/100×100% = 40%，高于 WHO PR≥32% 参考。'},
    {'title': '正常形态 8 / 200', 'body': '正常形态率 = 8/200×100% = 4%，达 WHO 严格标准 ≥4% 临界。'}],
  'faqs': [
    {'q': '和专用计算器区别？', 'a': '本器做通用占比；专用器按 WHO 字段自动套阈值与判读。'},
    {'q': '分母为零？', 'a': '总数须>0，否则无法计算占比。'}]},

'reproductive-medicine/calc-volume-concentration': {
  'title': '精子总数（浓度×体积）',
  'scenarios': [
    '精液常规总精子数估算。',
    '少精子症判定。',
    '辅助生殖取精规划。'],
  'examples': [
    {'title': '浓度 40×10⁶/ml、体积 3.0ml', 'body': '总数 = 40×3.0 = 120×10⁶；浓度≥16、体积≥1.4 均正常，总数远高于 WHO ≥39×10⁶。'},
    {'title': '浓度 10、体积 1.2', 'body': '总数=12×10⁶ <39，且浓度、体积均低于参考，提示少精子症。'}],
  'faqs': [
    {'q': 'WHO 第 6 版阈值？', 'a': '浓度≥16×10⁶/ml、体积≥1.4ml、总数≥39×10⁶ 为参考下限。'},
    {'q': '单位', 'a': '浓度为 ×10⁶/ml（即百万/毫升），总数为 ×10⁶（百万）。'}]},

'reproductive-medicine/detector-9': {
  'title': '逆行射精检测',
  'scenarios': [
    '射精后尿液中精子的比例。',
    '逆行射精程度判定。',
    '不育病因筛查。'],
  'examples': [
    {'title': '精液 1.0ml×20、尿液 30ml×2', 'body': 'ejTotal=20、urTotal=60、合计 80×10⁶；尿液占比=60/80×100%=75% ≥50% 且>5百万 → 显著逆行射精。'},
    {'title': '尿液无精子', 'body': 'urConc=0 → 尿液占比 0%，不支持逆行射精，需查其他原因。'}],
  'faqs': [
    {'q': '显著标准？', 'a': '尿液中精子占比≥50% 且总量>5×10⁶ 判为显著逆行，常伴射精量少。'},
    {'q': '处理？', 'a': '可碱化尿液后回收尿精子行 IUI/ICSI，或药物（拟交感）改善。'}]},

'reproductive-medicine/embryo-grading': {
  'title': '囊胚 Gardner 评分',
  'scenarios': [
    '第 5–6 天囊胚分级。',
 'ICM 与 TE 质量评估。',
    '移植优先级排序。'],
  'examples': [
    {'title': '扩张 4、ICM A、TE A', 'body': '编码 4AA：ICM 与 TE 均 A 级，优质囊胚，优先移植/冷冻。'},
    {'title': '扩张 3、ICM B、TE B', 'body': '3BB：可用胚胎，着床潜能中等，可作次选。'}],
  'faqs': [
    {'q': '三部分含义？', 'a': '扩张度(1–6)＋内细胞团(A–C)＋滋养层(A–C)；数字越大越扩张、字母越前越优。'},
    {'q': '哪种最优先？', 'a': '扩张≥4 且 ICM/TE 为 A 或 B 的囊胚着床率最高。'}]},

'reproductive-medicine/endometrial-receptivity': {
  'title': '子宫内膜容受性评估',
  'scenarios': [
    '移植窗口内膜条件判定。',
    '三线征与厚度关联。',
    '冻胚/鲜胚移植前筛查。'],
  'examples': [
    {'title': '厚度 9mm、A 型、周期日 12', 'body': '增殖期 A 型三线征且厚度 7–14mm → 良好容受，适宜移植窗口。'},
    {'title': '厚度 5mm、C 型', 'body': '偏薄且分泌期 C 型过早出现，容受欠佳，建议调整方案或宫腔评估。'}],
  'faqs': [
    {'q': '理想厚度？', 'a': '通常 7–14mm 且 A 型三线征最佳；<7mm 容受下降。'},
    {'q': 'A/B/C 型？', 'a': 'A 增殖期三线、B 过渡、C 分泌期均质高回声，需结合周期日判读。'}]},

'reproductive-medicine/epididymal-aspiration': {
  'title': '附睾穿刺取精产量',
  'scenarios': [
    'PESA/MESA 获精量估算。',
    '每卵可分配活动精子。',
    'ICSI 取材规划。'],
  'examples': [
    {'title': '0.5ml×50×10⁶/ml、活力 40%、卵 8', 'body': '总量=0.5×50=25×10⁶；活动=25×40%=10×10⁶；每卵=10/8=1.25×10⁶，足够 ICSI。'},
    {'title': '量少活力低', 'body': '总量 5×10⁶、活动 1×10⁶、卵 10 → 每卵仅 0.1×10⁶，偏紧，考虑重复穿刺或 TESE。'}],
  'faqs': [
    {'q': 'PESA 与 MESA？', 'a': 'PESA 经皮粗针、MESA 显微直视，后者更精准但创伤大。'},
    {'q': '每卵多少够？', 'a': 'ICSI 单卵仅需数个活动精子，常规获精远大于需求。'}]},

'reproductive-medicine/icsi-success': {
  'title': 'ICSI 活产率预估',
  'scenarios': [
    '按女方年龄估算预期活产。',
    '受精/存活/优质率测算。',
    '方案沟通参考。'],
  'examples': [
    {'title': '年龄 35–37，MII 10/注射 8/存活 7/受精 6/优质 4', 'body': '存活率 7/8=87.5%、受精率 6/8=75%、优质率 4/6=66.7%；该年龄预期活产 35–50%。'},
    {'title': '年龄 >42', 'body': '预期活产降至 5–15%，建议充分知情并考虑供卵。'}],
  'faqs': [
    {'q': '年龄分界？', 'a': '常用 <30:50–65%、30–34:45–60%、35–37:35–50%、38–40:25–40%、41–42:15–25%、>42:5–15%。'},
    {'q': '仅参考？', 'a': '为统计区间，实际受卵巢储备、胚胎质量等多因素影响。'}]},

'reproductive-medicine/ivf-statistics': {
  'title': 'IVF 实验室指标统计',
  'scenarios': [
    '受精/卵裂/优质/着床率测算。',
    '周期质量评估。',
    '质控与改进依据。'],
  'examples': [
    {'title': '卵 12/MII 10/受精 8/卵裂 8/优质 5/可用 5/移植 2/囊胚 1', 'body': '受精率 8/12=66.7%、正常受精 8/10=80%、卵裂 100%、优质 5/8=62.5%、着床 1/2=50%，实验室阶段达标。'},
    {'title': '受精率偏低', 'body': '受精率<60% 提示受精障碍，可改 ICSI 或评估精液。'}],
  'faqs': [
    {'q': '各率分母？', 'a': '受精率/卵裂率/优质率分母取受精卵数；正常受精率分母为 MII 数；着床率分母为移植数。'},
    {'q': '达标线？', 'a': '受精率≥60%、着床率≥30% 常作质控参考。'}]},

'reproductive-medicine/jingzidnasuipian-dfi-zhishu': {
  'title': '精子 DNA 碎片指数（DFI/HDS）',
  'scenarios': [
    'DFI 与 HDS 联合判读。',
    '反复流产/受精失败评估。',
    '抗氧化治疗随访。'],
  'examples': [
    {'title': 'DFI 18%、HDS 8%', 'body': 'DFI<30%（部分实验室<15% 更优）、HDS<15% → 均正常，DNA 完整性与染色质结构良好。'},
    {'title': 'DFI 35%', 'body': 'DFI≥30% 提示碎片升高，反复不良妊娠风险增加，建议抗氧化与生活方式干预后复查。'}],
  'faqs': [
    {'q': 'DFI 与 HDS 区别？', 'a': 'DFI 反映 DNA 断裂碎片比例，HDS 反映未成熟染色质（高可染性）比例。'},
    {'q': '阈值？', 'a': '常用 DFI<15–30%、HDS<15% 为正常区间，越高越差。'}]},

'reproductive-medicine/liquefaction-time': {
  'title': '精液液化时间',
  'scenarios': [
    '正常液化判定。',
    '液化延迟/不液化评估。',
    '粘稠度异常提示。'],
  'examples': [
    {'title': '30 分钟完全液化', 'body': 'WHO 参考：室温下 ≤60 分钟完全液化；30 分钟液化属正常。'},
    {'title': '>60 分钟仍胶冻状', 'body': '超过 60 分钟未液化或粘稠拉丝>2cm，提示液化异常，可影响计数与受孕。'}],
  'faqs': [
    {'q': '正常多久？', 'a': '射精后 15–30 分钟逐渐液化，参考上限 60 分钟。'},
    {'q': '不液化原因？', 'a': '常与前列腺分泌酶不足、炎症相关，可酶处理助检。'}]},

'reproductive-medicine/pgt-indication': {
  'title': 'PGT 适应症筛查',
  'scenarios': [
    'PGT-A/PGT-M/PGT-SR 指征判断。',
    '高龄/反复流产/染色体易位。',
    '遗传咨询前置评估。'],
  'examples': [
    {'title': '年龄 39 + 反复流产 3 次', 'body': '高龄(≥38)且 RPL≥2 次 → 符合 PGT-A 指征，建议行胚胎非整倍体筛查。'},
    {'title': '平衡易位携带', 'body': '染色体易位 → PGT-SR 指征，筛选正常/平衡胚胎降低流产。'}],
  'faqs': [
    {'q': '三种 PGT？', 'a': 'PGT-A 非整倍体、PGT-M 单基因病、PGT-SR 结构重排，按指征选择。'},
    {'q': '必须做吗？', 'a': '仅当存在明确指征；需遗传咨询与伦理审批。'}]},

'reproductive-medicine/progressive-motility': {
  'title': '精子活动力分级',
  'scenarios': [
    'PR/NP/IM 三级占比。',
    '弱精子症判定。',
    '精液常规核心指标。'],
  'examples': [
    {'title': 'PR 40、NP 10、IM 50', 'body': '总数 100；PR%=40%、总活动(PR+NP)=50%；PR≥32% 正常，前向运动良好。'},
    {'title': 'PR 20、IM 80', 'body': 'PR=20%<32% → 弱精子症（asthenozoospermia），建议复查与病因排查。'}],
  'faqs': [
    {'q': '三级含义？', 'a': 'PR 前向运动、NP 非前向、IM 不活动；WHO 以 PR≥32% 为参考。'},
    {'q': '活动力低怎么办？', 'a': '排查精索静脉曲张/感染/氧化应激，必要时 IUI/ICSI。'}]},

'reproductive-medicine/rater-30': {
  'title': 'Johnsen 评分（生精细管）',
  'scenarios': [
    '睾丸活检生精评分。',
    '10 条小管平均评分。',
    '生精功能分级。'],
  'examples': [
    {'title': '10 条小管评分均 8', 'body': '平均 8 分（满分 10）→ 生精功能良好，可见多量各级生精细胞。'},
    {'title': '平均 5 分', 'body': '平均 5 分 → 生精减低下，仅见少量精母/精子细胞，提示生精障碍。'}],
  'faqs': [
    {'q': '评分范围？', 'a': '每小管 1（无生精）至 10（完整生精）分，取多条平均。'},
    {'q': '与精液关系？', 'a': '评分低常对应非梗阻性无/少精子症，指导取精方式。'}]},

'reproductive-medicine/rater-31': {
  'title': 'Gardner 囊胚批量评分',
  'scenarios': [
    '多枚囊胚统一分级。',
    '优质/良好/一般/较差分布。',
    '移植与冷冻决策。'],
  'examples': [
    {'title': '3 枚：4AA、3BB、3BC', 'body': '评分=ICM级×3+TE级×2+min(扩张,4)：4AA=3×3+2×3+4=19（优质）；3BB=2×3+2×2+3=13（良好）；3BC 一般。'},
    {'title': '优选', 'body': '首选 4AA 移植，3BB 次之，3BC 作备选或囊胚培养观察。'}],
  'faqs': [
    {'q': '评分公式？', 'a': 'gradeLetter(A/B/C)=3/2/1；score=ICM分×3+TE分×2+min(扩张度,4)。'},
    {'q': '多少枚算好？', 'a': '依周期而定，有≥1 枚优质/良好即可移植，余冷冻。'}]},

'reproductive-medicine/reproductive-hormones': {
  'title': '生殖激素谱判读',
  'scenarios': [
    'FSH/LH/E2/T/PRL 联合分析。',
    '卵巢储备与排卵评估。',
    '高泌乳素/高雄鉴别。'],
  'examples': [
    {'title': 'FSH 12、LH 6、E2 40、T 3', 'body': 'FSH 升高伴 E2 不低 → 卵巢储备减退（DOR）倾向，建议 AMH 与 AFC 复核。'},
    {'title': 'PRL 80、余正常', 'body': '泌乳素显著升高（正常<25） → 高泌乳素血症，抑制排卵，需查垂体 MRI。'}],
  'faqs': [
    {'q': '基础 FSH 阈值？', 'a': '卵泡期 FSH>10 提示储备下降、>20 明显减退、>25 反应极差。'},
    {'q': 'LH/FSH 比值？', 'a': 'PCOS 常 LH/FSH≥2 伴 T 升高；需结合超声。'}]},

'reproductive-medicine/retrograde-ejaculation': {
  'title': '逆行射精程度',
  'scenarios': [
    '射精后尿液精子占比。',
    '完全/部分性逆行判定。',
    '取精策略选择。'],
  'examples': [
    {'title': '精液 0.5ml×10、尿液 40ml×3', 'body': 'semenTotal=5、urineTotal=120、合计 125×10⁶；尿液占比=120/125×100%=96% → 近乎完全逆行。'},
    {'title': '尿液占比 20%', 'body': '尿液 20% → 部分逆行，前向精液仍可自然受孕，必要时回收尿精子。'}],
  'faqs': [
    {'q': '与 detector-9 关系？', 'a': '两者同一算法（尿液精子占比），本器侧重程度分级与处理建议。'},
    {'q': '能否生育？', 'a': '完全逆行仍可经尿回收精子行 IUI/ICSI 助孕。'}]},

'reproductive-medicine/semen-volume': {
  'title': '精液量评估',
  'scenarios': [
    '禁欲天数与体积关系。',
    '少精液症判定。',
    '采集规范性核查。'],
  'examples': [
    {'title': '体积 2.5ml、禁欲 4 天', 'body': '禁欲 2–7 天采集合格，体积 2.5ml≥1.4ml 正常。'},
    {'title': '体积 0.8ml', 'body': '0.8ml<1.4ml → 少精液症，需排除逆行射精与附属腺分泌不足。'}],
  'faqs': [
    {'q': 'WHO 量下限？', 'a': '≥1.4ml；低于此提示采集不全或分泌减少。'},
    {'q': '禁欲多久准？', 'a': '推荐禁欲 2–7 天，过短量低、过长活力降。'}]},

'reproductive-medicine/sperm-concentration': {
  'title': '精子浓度（计数板法）',
  'scenarios': [
    '血细胞计数板浓度计算。',
    '稀释倍数校正。',
    '少/无精子症量化。'],
  'examples': [
    {'title': '2 格计 200、稀释 10×', 'body': '浓度=(C/n)×D×0.01=(200/2)×10×0.01=10×10⁶/ml，达参考下限附近。'},
    {'title': '2 格计 600、稀释 10×', 'body': '浓度=(600/2)×10×0.01=30×10⁶/ml，高于 ≥16 参考。'}],
  'faqs': [
    {'q': '公式含义？', 'a': 'C 为计数格内精子数、n 为格数、D 稀释倍数；×0.01 为板常数换算。'},
    {'q': '无精子？', 'a': '计数 0 需离心沉渣复检，仍无则报无精子症并进一步区分。'}]},

'reproductive-medicine/sperm-cryopreservation': {
  'title': '精子冷冻复苏率',
  'scenarios': [
    '冻融前后总数对比。',
    '活动精子回收率。',
    '生育力保存评估。'],
  'examples': [
    {'title': '冻前 60×3ml/50%、冻后 45×3ml/40%', 'body': '冻前总数 180、活动 90×10⁶；冻后总数 135、活动 54×10⁶；复苏率 75%、活动回收率 60%，属良好。'},
    {'title': '活动回收率偏低', 'body': '活动回收<50% 提示冷冻损伤偏大，可优化程序或分装。'}],
  'faqs': [
    {'q': '怎么算回收率？', 'a': '复苏率=冻后总数/冻前总数；活动回收率=冻后活动/冻前活动×100%。'},
    {'q': '正常水平？', 'a': '活动回收率常 40–70%，受方法与保护剂影响。'}]},

'reproductive-medicine/sperm-dfi': {
  'title': '精子 DNA 碎片（DFI）',
  'scenarios': [
    'DFI 单一指标判读。',
    '不育/流产风险分层。',
    '治疗随访监测。'],
  'examples': [
    {'title': 'DFI 25%', 'body': 'DFI<30%（更严实验室<15% 最优）属正常，DNA 完整性尚可。'},
    {'title': 'DFI 40%', 'body': 'DFI≥30–40% 升高，与受精失败、反复流产相关，建议抗氧化+复查。'}],
  'faqs': [
    {'q': 'DFI 与活力关系？', 'a': '二者不完全相关；DNA 损伤高但活力可正常，需专项检测。'},
    {'q': '能改善吗？', 'a': '戒烟酒、抗氧化（维 C/E、辅酶 Q10）、控热与感染可降 DFI。'}]},

'reproductive-medicine/sperm-morphology': {
  'title': '精子正常形态率',
  'scenarios': [
    '严格标准形态计数。',
    '畸精子症判定。',
    'IVF/ICSI 决策参考。'],
  'examples': [
    {'title': '正常 8 / 总数 200', 'body': '正常率=8/200×100%=4%，达 WHO 严格标准 ≥4% 临界正常。'},
    {'title': '正常 2 / 200', 'body': '正常率=1%<4% → 畸精子症，自然妊娠下降，ICSI 可 bypass 形态问题。'}],
  'faqs': [
    {'q': '严格标准？', 'a': 'WHO 第 5/6 版严格标准正常形态≥4% 为参考下限（Tygerberg 法）。'},
    {'q': '形态差必须 ICSI？', 'a': '非必须；仅当合并少弱精或反复失败才倾向 ICSI。'}]},

'reproductive-medicine/stats-6': {
  'title': '生殖统计汇总',
  'scenarios': [
    '周期级数据统计。',
    '多指标占比汇总。',
    '报表辅助计算。'],
  'examples': [
    {'title': '受精 8/12、卵裂 8/8', 'body': '受精率 66.7%、卵裂率 100%，汇总为实验室质控基线。'},
    {'title': '移植 2 着床 1', 'body': '着床率 50%，高于 ≥30% 参考，周期质量良好。'}],
  'faqs': [
    {'q': '用途？', 'a': '对若干关键率做快速汇总，便于周期复盘与上报。'},
    {'q': '与 ivf-statistics 区别？', 'a': '本器更通用，ivf-statistics 按固定字段输出全套率。'}]},

'reproductive-medicine/testicular-biopsy': {
  'title': '睾丸活检分级',
  'scenarios': [
    'Johnsen/Silber 分级。',
    '生精状态定性。',
    '取精方式指导。'],
  'examples': [
    {'title': '10 条小管评分合计均值 7', 'body': '平均 7 分 → 生精减低下但有精子，可尝试显微取精（micro-TESE）。'},
    {'title': '平均 2 分', 'body': '仅支持细胞/精原，生精严重障碍，取精成功率低，需充分告知。'}],
  'faqs': [
    {'q': 'Johnsen 与 Silber？', 'a': '均 1–10 分系统，Silber 更简；本器支持两式并给出分级描述。'},
    {'q': '活检后取精？', 'a': '非梗阻性无精子症靠 micro-TESE 找局灶生精，评分高成功率更高。'}]},

'reproductive-medicine/testicular-volume': {
  'title': '睾丸体积测算',
  'scenarios': [
    '椭球体积公式估算。',
    '左右不对称评估。',
    '青春期/萎缩监测。'],
  'examples': [
    {'title': '左 40×30×20mm、右 38×28×19mm', 'body': '左=(4×3×2×0.71)=17.0ml、右=(3.8×2.8×1.9×0.71)=14.3ml，均正常（15–25ml）；差 2.7ml 略超 2ml 注意随访。'},
    {'title': '单侧 8ml', 'body': '体积<12–15ml 提示发育不良/萎缩，伴生精下降。'}],
  'faqs': [
    {'q': '公式？', 'a': '体积=(长×宽×高×0.71)/1000（长宽高取 mm、结果 ml），0.71 为椭球系数。'},
    {'q': '正常多大？', 'a': '成人单侧约 15–25ml，相差>2ml 或单侧偏小需排查。'}]},

'reproductive-medicine/total-sperm-count': {
  'title': '总精子数',
  'scenarios': [
    '浓度×体积总数。',
    '少精子症量化。',
    '生育力初筛。'],
  'examples': [
    {'title': '浓度 40×10⁶/ml、体积 3.0ml', 'body': '总数=40×3.0=120×10⁶，远高于 WHO ≥39×10⁶ 下限，正常。'},
    {'title': '浓度 12、体积 1.5', 'body': '总数=18×10⁶<39 → 少精子症，建议复查与评估。'}],
  'faqs': [
    {'q': 'WHO 下限？', 'a': '总数 ≥39×10⁶ 为参考下限（浓度×体积）。'},
    {'q': '与浓度关系？', 'a': '总数同时受浓度与体积影响，体积少也会拉低总数。'}]},

'reproductive-medicine/vasography': {
  'title': '精道造影梗阻定位',
  'scenarios': [
    '输精管/精囊/射精管通畅判定。',
    '梗阻部位定位。',
    'TURED 等手术指征。'],
  'examples': [
    {'title': '全段通畅', 'body': '输精管、精囊、射精管均勾选通畅、部位 none → 精道通畅，不支持梗阻性无精子症。'},
    {'title': '部位=射精管、精囊明显扩张', 'body': '射精管梗阻 + 精囊扩张 → 建议 TURED（经尿道射精管切开）评估。'}],
  'faqs': [
    {'q': '常见梗阻点？', 'a': '腹股沟段、盆段、射精管；射精管梗阻常伴精囊扩张、精液量少。'},
    {'q': '下一步？', 'a': '定位明确后行显微/内镜重建或直取精+ICSI。'}]},
}

def main():
    data = json.load(open(F, encoding='utf-8'))
    for slug, info in KB.items():
        blob = json.dumps(info, ensure_ascii=False)
        if BAD_RE.search(blob):
            raise SystemExit(f'BAD placeholder in KB {slug}: {BAD_RE.search(blob).group()}')
    changed = 0
    for slug, info in KB.items():
        if slug not in data:
            data[slug] = info
            changed += 1
            continue
        if data[slug] != info:
            data[slug] = info
            changed += 1
    json.dump(data, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(F, 'a').write('\n')
    print(f'KB entries: {len(KB)} changed: {changed}')

if __name__ == '__main__':
    main()
