# -*- coding: utf-8 -*-
"""Real-ize pulmonology deep-dive content: replace template/placeholder text with real clinical examples."""
import json, os, re

PATH = 'i18n/tools/content_deepdive.json'
BAD_RE = re.compile(
    r'统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|标准化，再批量'
    r'|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|高频复用模板'
    r'|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|复用模板示例|保留复用模板'
    r'|先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|先用一组可复现输入'
    r'|同一输入样本测试默认和边界情况|选择两组不同来源样本并同步口径定义'
)

KB = {
'pulmonology/analysis-14': {
  'title': '结核涂片/培养耐药分析',
  'scenarios': ['门诊痰涂片阳性初诊患者', '培养阳性需判定传染性与耐药', '耐药结果回报后调整方案'],
  'examples': [
    {'title': '涂片阳+培养阳', 'body': '涂片阳性、培养阳性：具有传染性，须呼吸道隔离；提示活动肺结核。'},
    {'title': '耐多药判定', 'body': '同时耐异烟肼与利福平（MDR-TB）：归为耐药结核，按方案换用二线药，传染期延长。'}],
  'faqs': [
    {'q': '涂片阴性能否排除传染？', 'a': '涂片阴性、培养阳性仍有低度传染；涂片阴性不等于无传染性，结合培养与症状综合判断。'},
    {'q': 'Xpert 作用？', 'a': 'Xpert MTB/RIF 可 2 小时内同时报结核与利福平耐药，阳性即按耐药流程处置。'}]},
'pulmonology/anti-tb-dosing': {
  'title': '抗结核四联剂量与肝毒性',
  'scenarios': ['初治肺结核体重 55kg', '基础肝病需评估肝毒性', '治疗中监测肝功能'],
  'examples': [
    {'title': '55kg 标准剂量', 'body': 'INH=min(55×5,300)=275mg；RIF(≥50kg)=600mg；PZA(50–75kg)=1750mg；EMB(50–75kg)=1000mg。'},
    {'title': '高危肝毒性', 'body': '基础肝功异常+长期饮酒+HCV 三项风险因素：高危，每 1–2 周复查肝功，必要时减 Z 或换肝毒性低方案(HRE+氟喹诺酮)。'}],
  'faqs': [
    {'q': '为什么 INH 封顶 300？', 'a': 'INH 按体重 5mg/kg 但封顶 300mg，超量不增疗效且肝毒性上升。'},
    {'q': '肝功异常如何处理？', 'a': '明显异常(ALT 显著升高/黄疸)先停肝毒性药，保肝并请专科，稳定后逐步重建方案。'}]},
'pulmonology/assessor-8': {
  'title': '哮喘 GINA 控制评估',
  'scenarios': ['四问症状控制评分', '合并风险因素评估', '阶梯治疗调整'],
  'examples': [
    {'title': '控制项 0 分', 'body': '四项症状均为阴性→控制分 0，控制良好；当前方案有效。'},
    {'title': '控制良好但有风险', 'body': '控制分 0、风险项 1 项阳性→整体"良好控制但伴风险因素"，维持治疗并加强诱因管理。'}],
  'faqs': [
    {'q': '控制与风险区别？', 'a': '控制反映当前症状，风险反映急性发作/肺功能下降倾向；二者均需管理。'},
    {'q': '多久复评？', 'a': '每 1–3 月评估控制，稳定后可谨慎考虑降阶梯。'}]},
'pulmonology/bronchoscopy-grading': {
  'title': '支气管镜镜下分级',
  'scenarios': ['中央型肺癌镜下分型', '气道炎症分级', '狭窄程度评估'],
  'examples': [
    {'title': '肿瘤型增生', 'body': '肿瘤型：管内增殖/管壁浸润/管外压迫三型，决定活检与支架策略。'},
    {'title': '狭窄分级', 'body': '狭窄按程度分轻/中/重，重度(闭塞)>75% 需球囊或支架开通。'}],
  'faqs': [
    {'q': '分级有何用？', 'a': '分型指导活检部位与通气重建方式，并用于随访比较。'},
    {'q': '炎症与肿瘤如何区分？', 'a': '结合充血水肿、坏死、新生物形态与病理，单凭肉眼不确诊。'}]},
'pulmonology/calc-48': {
  'title': '氧合指数 PaO₂/FiO₂',
  'scenarios': ['ARDS 严重程度分层', '机械通气氧合监测', '含 PEEP 时算 OI'],
  'examples': [
    {'title': 'PaO₂ 80 / FiO₂ 40%', 'body': 'PF=80/0.40=200 mmHg：属中度 ARDS(100–200)。'},
    {'title': '含 MAP 算 OI', 'body': 'MAP 13、FiO₂ 0.40、PaO₂ 80：OI=(13×40)/80=6.5，OI>10 提示重度。'}],
  'faqs': [
    {'q': 'ARDS 分级切点？', 'a': 'PF<100 重度、100–200 中度、200–300 轻度(需 PEEP≥5)。'},
    {'q': 'SF 比值？', 'a': '无创时以 SpO₂/FiO₂ 替代，SF<315 近似 PF<300。'}]},
'pulmonology/copd-cat': {
  'title': 'COPD CAT 问卷',
  'scenarios': ['慢阻肺症状负荷评估', '指导药物强度', '随访疗效比较'],
  'examples': [
    {'title': '8 题各 2 分', 'body': '总分=8×2=16 分：10–20 为中度影响，建议含长效支扩剂治疗。'},
    {'title': '重度影响', 'body': '总分≥20：症状重度，考虑 LAMA+LABA 或联合 ICS。'}],
  'faqs': [
    {'q': 'CAT 与 mMRC 区别？', 'a': 'CAT 全面评估症状/活动/心理，mMRC 仅呼吸困难；二者互补。'},
    {'q': '多少分需随访？', 'a': '每 3 月复评，变化≥2 分有临床意义。'}]},
'pulmonology/curb65': {
  'title': '肺炎 CURB-65 评分',
  'scenarios': ['社区肺炎严重度', '住院与否决策', 'ICU 评估'],
  'examples': [
    {'title': '3 分项阳性', 'body': '意识+尿素+年龄≥65 三项阳性→3 分，死亡率约 15%，建议住院/ICU 评估。'},
    {'title': '0–1 分低危', 'body': '0–1 分死亡率<3%，可门急诊抗感染随访。'}],
  'faqs': [
    {'q': '各项含义？', 'a': 'C 意识、U 尿素>7mmol/L、R 呼吸≥30、B 收缩压<90 或舒张压≤60、年龄≥65。'},
    {'q': '2 分如何处理？', 'a': '2 分中危(约 9%)，住院治疗、静脉抗生素。'}]},
'pulmonology/feigongneng-fev1-fvc-fenji': {
  'title': '肺功能 FEV₁/FVC 分级',
  'scenarios': ['慢阻肺气流受限判定', 'GOLD 分级', '结合 FVC 鉴限制'],
  'examples': [
    {'title': 'FEV₁ 2.1 / FVC 3.5', 'body': '比值=2.1/3.5=60%，<60 岁 LLN 0.70→阻塞性；FEV₁%pred=2.1/3.0=70%→GOLD 2 中度。'},
    {'title': '限制性提示', 'body': '若 FVC<预计值 80%：比值低且 FVC 低→混合性或限制性，需查 TLC/DLCO。'}],
  'faqs': [
    {'q': 'LLN 与 0.70 切点？', 'a': '年轻用 LLN 更准，老年常用 0.70；本工具按年龄取 LLN，≥65 用 0.66。'},
    {'q': 'GOLD 分期？', 'a': 'GOLD 1≥80%、2 50–79%、3 30–49%、4<30%(均基于 FEV₁%pred)。'}]},
'pulmonology/gina-asthma': {
  'title': '哮喘 GINA/ACT 控制',
  'scenarios': ['GINA 四问控制', 'ACT 5 题评分', '阶梯调整'],
  'examples': [
    {'title': 'GINA 四项阴性', 'body': 'GINA 四问全阴性→控制良好，维持当前阶梯，每 3–6 月复评。'},
    {'title': 'ACT 20 分', 'body': 'ACT 5 题总分 20/25→部分控制，需升级治疗并随访。'}],
  'faqs': [
    {'q': 'GINA 与 ACT 选谁？', 'a': 'GINA 为控制问卷、ACT 为症状+活动量表；联合更全面。'},
    {'q': '部分控制怎么办？', 'a': '部分控制提示需升阶梯或更换吸入技术，2–4 周后复评。'}]},
'pulmonology/light-criteria': {
  'title': '胸水 Light 标准',
  'scenarios': ['胸水渗出/漏出鉴别', '蛋白与 LDH 比值', '结合血清上限'],
  'examples': [
    {'title': '蛋白比 0.583', 'body': '胸水蛋白 3.5/血清 6.0=0.583>0.5→满足一条，判渗出液。'},
    {'title': 'LDH 比超标', 'body': '胸水 LDH 250/血清 LDH 200=1.25>0.6，或胸水 LDH>血清上限 2/3→渗出。'}],
  'faqs': [
    {'q': '三条满足几条？', 'a': '满足任一条即渗出；漏出液三条均不满足。'},
    {'q': '假性渗出？', 'a': '心衰/低蛋白时可出现"假性渗出"，需结合临床与 NT-proBNP。'}]},
'pulmonology/lung-cancer-tnm': {
  'title': '肺癌 TNM 分期',
  'scenarios': ['非小细胞肺癌分期', 'T/N/M 组合', '治疗路径提示'],
  'examples': [
    {'title': 'T2a N0 M0', 'body': 'T2a(3–4cm)+N0+M0→ⅠB 期，首选手术切除+淋巴结清扫。'},
    {'title': 'N3 局部晚期', 'body': 'N3 无论 T→ⅢC 期，不可切除行同步放化疗+免疫巩固。'}],
  'faqs': [
    {'q': 'M1 如何分期？', 'a': 'M1a/M1b→ⅣA、M1c→ⅣB，以全身治疗为主。'},
    {'q': '分期决定什么？', 'a': '分期驱动可切除性评估与辅助/新辅助策略。'}]},
'pulmonology/lung-rads': {
  'title': '肺结节 Lung-RADS',
  'scenarios': ['低剂量 CT 随访', '实性/部分实性分层', '恶性风险评估'],
  'examples': [
    {'title': '实性 6mm', 'body': '实性结节 6mm→2 类，12 月低剂量 CT 随访。'},
    {'title': '部分实性>10mm', 'body': '部分实性成分>10mm→4A/4B 类，建议 3 月复查或 PET-CT/活检。'}],
  'faqs': [
    {'q': '4 类是癌吗？', 'a': '4 类为可疑恶性需积极处理，并非确诊；最终靠病理。'},
    {'q': '随访间隔？', 'a': '按类别 3–12 月不等，新发/增大提示升级。'}]},
'pulmonology/niv-settings': {
  'title': '无创通气设定',
  'scenarios': ['COPD 呼衰', '心源性肺水肿', 'OSA/神经肌肉'],
  'examples': [
    {'title': 'COPD 伴高碳酸', 'body': 'PaCO₂ 7.2(<7.25)：EPAP 4、PS 10、IPAP=14 cmH₂O。'},
    {'title': '心源性肺水肿', 'body': 'EPAP 8、PS 5、IPAP=13 cmH₂O，高 EPAP 利于复张肺泡。'}],
  'faqs': [
    {'q': 'IPAP 怎么来？', 'a': 'IPAP=EPAP+PS；PS 随指征与血气调整，目标 PaCO₂ 下降。'},
    {'q': '为什么要 PEEP？', 'a': 'EPAP 维持气道开放、对抗内源性 PEEP，尤其 COPD/肺水肿。'}]},
'pulmonology/oxygenation-index': {
  'title': 'PaO₂/FiO₂ 与 SF',
  'scenarios': ['氧合监测', 'ARDS 分层', '无创 SF 替代'],
  'examples': [
    {'title': 'PaO₂ 80 / FiO₂ 40%', 'body': 'PF=80/0.40=200 mmHg：中度 ARDS。'},
    {'title': 'SF 比值', 'body': 'SpO₂ 90 / FiO₂ 40%：SF=90/0.40=225，近似 PF 轻-中度。'}],
  'faqs': [
    {'q': 'PF 与 OI 区别？', 'a': 'PF 不用 PEEP，OI 含 MAP，OI 对小儿/高 PEEP 更敏感。'},
    {'q': 'SF 可靠吗？', 'a': 'SF 受脉搏血氧误差影响，仅作无创筛查。'}]},
'pulmonology/pneumothorax': {
  'title': '气胸肺压缩%',
  'scenarios': ['原发性气胸', '继发性气胸', '症状与压缩度决策'],
  'examples': [
    {'title': '三径均值 2', 'body': 'a=b=c=2cm，均值 2，压缩≈2×10=20%：临界，观察或细管引流。'},
    {'title': '重度症状', 'body': '压缩>20% 且呼吸困难→优先胸腔闭式引流。'}],
  'faqs': [
    {'q': '估算准确吗？', 'a': '径线法为粗略估计，CT 体积法更准；临床以症状为先。'},
    {'q': '20% 怎么处理？', 'a': '无症状原发性可观察，继发性/症状者引流。'}]},
'pulmonology/pulmonary-function': {
  'title': 'FEV₁/FVC 分级',
  'scenarios': ['阻塞性判定', '限制性判定', '自定义切点'],
  'examples': [
    {'title': 'FEV₁ 1.5 / FVC 3.0', 'body': '比值=1.5/3.0=50%<0.7→阻塞性；FVC%pred≥80 不支持限制。'},
    {'title': '限制性', 'body': '比值正常但 FVC%pred<80→限制性通气障碍，查 TLC。'}],
  'faqs': [
    {'q': '切点可调？', 'a': '本工具 cutoff 可设(默认 0.7)，老年建议按 LLN。'},
    {'q': '阻塞性+限制？', 'a': '比值低且 FVC 低为混合性，需 TLC/DLCO 确认。'}]},
'pulmonology/pulmonary-rehab': {
  'title': '呼吸肌训练强度',
  'scenarios': ['COPD 呼吸肌无力', '力量 vs 耐力目标', 'MIP/MEP 弱'],
  'examples': [
    {'title': '男 60 MIP 60', 'body': '下限=75−0.5×60=45；MIP 60>45 不弱；力量目标训练=60×0.35≈21 cmH₂O。'},
    {'title': '呼吸肌弱', 'body': 'MIP<下限→吸气肌薄弱，从 30–50% MIP 起渐进负荷。'}],
  'faqs': [
    {'q': '力量与耐力强度？', 'a': '力量 30–50% MIP、耐力 20–30% MIP，每日分次训练。'},
    {'q': '为什么要测 MIP？', 'a': 'MIP/MEP 反映吸气/呼气肌，低于年龄下限提示易疲劳。'}]},
'pulmonology/rater-13': {
  'title': 'Wells 肺栓塞评分',
  'scenarios': ['疑似肺栓塞', '临床概率分层', 'D-二聚体策略'],
  'examples': [
    {'title': 'DVT 症状+3', 'body': '下肢 DVT 症状体征 +3，合并其他项总分>6→高可能，直接 CTPA。'},
    {'title': '低可能', 'body': '总分≤4 且 D-二聚体阴性→排除肺栓塞，不必影像。'}],
  'faqs': [
    {'q': '高分怎么走？', 'a': '>6 高可能直接影像；4–6 中可能查 D-二聚体或 CTPA。'},
    {'q': '与简化 Wells 区别？', 'a': '本版加权计分，简化版以 1 项阳性即中/高可能。'}]},
'pulmonology/respiratory-failure': {
  'title': '呼吸衰竭血气鉴别',
  'scenarios': ['Ⅰ型/Ⅱ型呼衰', '肺泡-动脉梯度', '吸氧下判读'],
  'examples': [
    {'title': 'PaO₂ 50 / PaCO₂ 60', 'body': 'FiO₂ 0.21：PAO₂=0.21×713=149.7；A-a=149.7−60/0.8−50=24.7>15.1→Ⅱ型呼衰且梯度增大。'},
    {'title': '单纯低氧', 'body': 'PaO₂<60 而 PaCO₂ 正常→Ⅰ型呼衰，提高吸氧浓度。'}],
  'faqs': [
    {'q': 'Ⅰ型与Ⅱ型？', 'a': 'PaO₂<60 即可诊断；伴 PaCO₂>50 为Ⅱ型(通气不足)。'},
    {'q': 'A-a 梯度公式？', 'a': 'PAO₂=FiO₂×(760−47)−PaCO₂/0.8；梯度随年龄增大。'}]},
'pulmonology/self-assess-3': {
  'title': 'FTND 尼古丁依赖',
  'scenarios': ['戒烟前评估', '依赖程度分层', '制定干预强度'],
  'examples': [
    {'title': '总分 5 分', 'body': 'FTND 5 分→中度依赖，建议药物(伐尼克兰/贴剂)+行为支持。'},
    {'title': '重度依赖', 'body': '≥7 分重度，单靠意志力难戒，需强化药物与随访。'}],
  'faqs': [
    {'q': 'FTND 几分？', 'a': '6 题 0–10 分，≤3 低、4–6 中、≥7 高依赖。'},
    {'q': '评分用途？', 'a': '依赖越高越需药物辅助与高频随访。'}]},
'pulmonology/smoking-cessation': {
  'title': 'FTND 依赖自评',
  'scenarios': ['戒烟门诊初筛', '依赖分级', '随访复评'],
  'examples': [
    {'title': '6 题合计', 'body': '6 题各取分值求和；如 4+1+0+0+0+0=5 分→中度依赖。'},
    {'title': '低依赖', 'body': '≤3 分低依赖，可先行为干预+简短随访。'}],
  'faqs': [
    {'q': '和 self-assess-3 区别？', 'a': '同为 FTND，本工具为简化自评版，用于快速分层。'},
    {'q': '多久复评？', 'a': '戒烟后 2 周、1 月复评依赖与戒断症状。'}]},
'pulmonology/sputum-analysis': {
  'title': '痰液性状临床意义',
  'scenarios': ['痰色性状判读', '急症警示', '病原方向提示'],
  'examples': [
    {'title': '铁锈色痰', 'body': '铁锈色痰高度提示大叶性肺炎(肺炎链球菌)，结合高热胸痛经验性抗感染。'},
    {'title': '粉红色泡沫痰', 'body': '粉红色泡沫痰为急性肺水肿急症，立即坐位吸氧利尿扩血管。'}],
  'faqs': [
    {'q': '恶臭痰意义？', 'a': '恶臭提示厌氧菌(肺脓肿/支扩)，需覆盖甲硝唑/克林霉素。'},
    {'q': '血性痰排查？', 'a': '中老年咯血查胸部 CT 与支气管镜，排外结核/肺癌。'}]},
'pulmonology/stop-bang': {
  'title': 'STOP-BANG 筛查',
  'scenarios': ['OSA 高危筛查', '术前评估', '打鼾人群'],
  'examples': [
    {'title': '8 项全中', 'body': '打鼾+倦+呼吸暂停+高血压+BMI>35+年龄>50+颈粗+性别男=8 分→高危 OSA。'},
    {'title': '低危', 'body': '0–2 分低危；3–4 分中危，建议睡眠监测。'}],
  'faqs': [
    {'q': '几分做监测？', 'a': '中高危(≥3)建议多导睡眠图确认。'},
    {'q': '灵敏度高吗？', 'a': 'STOP-BANG 对中重度 OSA 灵敏度高，阴性可较放心排除。'}]},
'pulmonology/tb-resistance': {
  'title': '结核耐药分析',
  'scenarios': ['涂片培养+Xpert', '耐药药物勾选', '传染与隔离'],
  'examples': [
    {'title': '涂片阳+Xpert rif_r', 'body': '涂片阳性且有传染；Xpert 报利福平耐药→RR-TB，按耐药流程隔离治疗。'},
    {'title': '低传染', 'body': '涂片阴性+培养阴性→传染性低，仍完成疗程并复查。'}],
  'faqs': [
    {'q': 'RR-TB 与 MDR？', 'a': 'RR-TB 含利福平耐药(含 MDR)，治疗以全口服短程方案为主。'},
    {'q': '隔离到何时？', 'a': '涂片阴转并治疗 2 周后传染性大幅下降，遵医嘱解隔。'}]},
'pulmonology/vibration-percussion': {
  'title': '振动排痰指导',
  'scenarios': ['慢支/支扩排痰', '肺叶体位', '频率选择'],
  'examples': [
    {'title': '下叶 20Hz', 'body': '下叶病变取头低俯卧位，频率 20Hz 中频常规排痰。'},
    {'title': '高频黏稠痰', 'body': '痰黏稠选>25Hz 高频促进排出，注意耐受与心率。'}],
  'faqs': [
    {'q': '频率怎么选？', 'a': '≤15 低频松痰栓、15–25 中频常规、>25 高频促排，按耐受调整。'},
    {'q': '禁忌？', 'a': '咯血、气胸、骨质疏松、不稳定心血管者慎用。'}]},
'pulmonology/wells-pe': {
  'title': 'Wells 肺栓塞评分',
  'scenarios': ['门急诊疑诊 PE', '概率分层', '影像决策'],
  'examples': [
    {'title': '临床中可能', 'body': '无 DVT 症状但 D-二聚体高、心率快等→总分 4–6 中可能，查 CTPA。'},
    {'title': '低可能排除', 'body': '≤4 且 D-二聚体阴性→可排除，不必影像。'}],
  'faqs': [
    {'q': '与 rater-13 区别？', 'a': '同属 Wells PE 评分，本工具为临床决策版；总分>6 高可能直接影像。'},
    {'q': '妊娠/肿瘤？', 'a': '活动性肿瘤、近期手术均计入加分项，提高先验概率。'}]},
}

def main():
    data = json.load(open(PATH, encoding='utf-8'))
    # self-check: reject any placeholder text in KB
    for slug, info in KB.items():
        blob = json.dumps(info, ensure_ascii=False)
        if BAD_RE.search(blob):
            raise SystemExit('BAD placeholder in KB slug=%s -> %s' % (slug, BAD_RE.search(blob).group()))
    changed = 0
    for slug, info in KB.items():
        if slug not in data:
            print('WARN missing key:', slug); continue
        if data[slug] != info:
            data[slug] = info; changed += 1
    json.dump(data, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(PATH, 'a').write('\n')
    print('KB entries:', len(KB), 'changed:', changed)

if __name__ == '__main__':
    main()
