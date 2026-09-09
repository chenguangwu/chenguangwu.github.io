# -*- coding: utf-8 -*-
"""real-ize rheumatology deep-dive: replace template/boilerplate with real examples."""
import json, re, sys, os

JSON_PATH = 'i18n/tools/content_deepdive.json'
BAD_RE = re.compile(
    r'统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|标准化，再批量'
    r'|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|高频复用模板'
    r'|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|复用模板示例|保留复用模板'
    r'|先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|先用一组可复现输入'
    r'|同一输入样本测试默认和边界情况|选择两组不同来源样本并同步口径定义'
)

KB = {
'psychiatry_placeholder': {},  # noqa
'rheumatology/gout-uric-acid': {
  'title': '痛风血尿酸达标治疗',
  'scenarios': ['无石痛风', '痛风石/慢性', '肾结石/CKD'],
  'examples': [
    {'title': '慢性痛风石未达标', 'body': '血尿酸 520 μmol/L，慢性痛风石期目标 <300 μmol/L → 差 220，未达标；启动别嘌醇/非布司他并联合小剂量秋水仙碱 3–6 月预防发作，3 月复测。'},
    {'title': '无石已达标', 'body': '血尿酸 340 μmol/L，无石期目标 <360 → 达标，维持 ULT 并随访肾功能。'}],
  'faqs': [
    {'q': '目标为何分档？', 'a': '无石 <360、有石/慢性/反复 <300 μmol/L；达标可溶解尿酸盐结晶、减少发作。'},
    {'q': '急性期能加药吗？', 'a': '急性发作期不停已有 ULT，但不新启动；新启动应等炎症消退后。'}]},
'rheumatology/das28': {
  'title': 'DAS28 类风湿活动度',
  'scenarios': ['ESR 版', 'CRP 版', '疗效随访'],
  'examples': [
    {'title': '高活动 6.54', 'body': 'ESR 版：压痛关节 TJC=6、肿胀 SJC=8、ESR 40、GH 60 → DAS28=0.56√6+0.28√8+0.70·ln40+0.014×60+0.96≈1.37+0.79+2.58+0.84+0.96=6.54，高活动，需强化治疗。'},
    {'title': '低活动 2.6', 'body': 'TJC=2、SJC=1、ESR 18、GH 30 → 约 2.6，低活动/缓解附近，维持并监测。'}],
  'faqs': [
    {'q': '分级？', 'a': '≤2.6 缓解(ESR 版)、>5.1 高活动、3.2–5.1 中、2.6–3.2 低；CRP 版阈值略不同。'},
    {'q': '关节数怎么数？', 'a': '28 个指定关节（肘腕以下+肩膝），TJC/SJC 由查体计，GH 为 0–100 视觉模拟。'}]},
'rheumatology/essdai': {
  'title': 'ESSDAI 干燥综合征活动度',
  'scenarios': ['全身/淋巴结', '肺部/肾', '血液/外周神经'],
  'examples': [
    {'title': '总分 14', 'body': '12 系统分级：淋巴结中(2)+肺部中(2)+肾高(权重4)+血液低(1)+关节低(1)+皮肤低(1)+外周神经低(1)+中枢低(1)+腺体(1) → 合计 14，中高活动，需系统治疗。'},
    {'title': '无活动 0', 'body': '各系统 0 分 → 无系统活动，以口眼干对症为主并淋巴瘤筛查。'}],
  'faqs': [
    {'q': '怎么计分？', 'a': '9 大系统按低/中/高(或权重)赋 1/2/权重分；总分 0 无活动、1–4 低、5–13 中、≥14 高。'},
    {'q': '与 pSS 关系？', 'a': 'ESSDAI 评价系统性脏器活动，不反映口干眼干症状（症状用 ESSPRI）。'}]},
'rheumatology/basdai': {
  'title': 'BASDAI 强直活动度',
  'scenarios': ['疲劳', '脊柱痛', '晨僵'],
  'examples': [
    {'title': '高活动 4.8', 'body': '6 题 0–10：疲劳6、脊柱痛4、关节肿痛5、肌腱炎3、晨僵两题 7 与 5 → 晨僵均值 6；BASDAI=(6+4+5+3+6)/5=4.8 >4，高活动。'},
    {'title': '低活动 2.0', 'body': '各症状约 2 → 2.0，低活动，维持 TNF/IL-17 抑制剂。'}],
  'faqs': [
    {'q': '判读？', 'a': '0–4 低活动、>4 高活动；>4 常提示需调整生物制剂。晨僵取两题均值后与前 4 题平均。'},
    {'q': '自评局限？', 'a': 'BASDAI 含主观症状，需结合 CRP/影像与功能指标(BASFI)综合判效。'}]},
'rheumatology/mrss': {
  'title': 'mRSS 硬皮病皮肤硬化',
  'scenarios': ['上肢/面部', '躯干', '下肢'],
  'examples': [
    {'title': '总分 24', 'body': '17 区块 0–3：面部2+左手指3+左手掌2+左前臂2+右手指3+右手掌2+右前臂2+胸腹壁2+左大腿1+左小腿1+左足1+右大腿1+右小腿1+右足1 = 24，中重度皮肤受累。'},
    {'title': '轻度 9', 'body': '面部1+手指合计4+前臂2+躯干2 = 9，轻度，随访指端溃疡与肺纤维化。'}],
  'faqs': [
    {'q': '范围？', 'a': '17 区 0–3 分，0 正常、1 轻度、2 中度、3 重度，总分 0–51；用于弥漫型 SSc 活动与预后。'},
    {'q': '分部意义？', 'a': '上肢/下肢高提示外周缺血与指端溃疡风险，躯干高提示内脏受累可能。'}]},
'rheumatology/sledai': {
  'title': 'SLEDAI-2K 狼疮活动',
  'scenarios': ['肾脏/补体', '皮肤黏膜', '神经/血液'],
  'examples': [
    {'title': '中重度 12', 'body': '关节炎2+新发皮疹2+蛋白尿4+补体降低2+抗dsDNA升高2 = 12，中重度活动，需免疫抑制；肾型权重高需查尿蛋白定量。'},
    {'title': '无活动 0', 'body': '近 10 天无活动项 → 0，维持治疗并监测补体/dsDNA。'}],
  'faqs': [
    {'q': '权重？', 'a': '癫痫发作/精神病 8，血管炎/肾炎 6，关节炎/肌炎/管型/血尿/蛋白尿/脓尿 4，皮疹/胸膜炎/心包炎/补体降/dsDNA 2，发热/血小板/白细胞 1。'},
    {'q': '评估窗？', 'a': 'SLEDAI-2K 看近 10 天表现，发作频率按是否新发或复发计。'}]},
'rheumatology/bvas': {
  'title': 'BVAS 血管炎活动',
  'scenarios': ['全身/皮肤', '肾/肺', '神经/五官'],
  'examples': [
    {'title': '中重度 18', 'body': '分组计分：全身发热3+皮肤紫癜3+肾血尿/蛋白尿6+肺出血/浸润4+神经2 = 18，中重度活动，诱导期需大剂量激素+环磷酰胺/利妥昔。'},
    {'title': '无活动 0', 'body': '近 4 周无活动项 → 0，缓解期维持，监测 ANCA 滴度。'}],
  'faqs': [
    {'q': '版本？', 'a': 'BVAS v3 覆盖 9 系统并按严重度封顶；总分 0 无活动、1–14 轻中、≥15 重（含诱导期）。'},
    {'q': '与缓解关系？', 'a': 'BVAS 降 50% 且达 0 常作缓解定义之一，用于临床试验终点。'}]},
'rheumatology/womac': {
  'title': 'WOMAC 骨关节炎指数',
  'scenarios': ['疼痛', '僵硬', '功能'],
  'examples': [
    {'title': '总分 48（约50%）', 'body': '疼痛 5 项各 2 = 10、僵硬 2 项各 2 = 4、功能 17 项各 2 = 34 → 总分 48/96；疼痛/僵硬/功能标化分别 50%/50%/50%，中重度。'},
    {'title': '轻度 12', 'body': '各题多 1 → 12/96，轻度，建议运动疗法与减重。'}],
  'faqs': [
    {'q': '三个分量？', 'a': '疼痛 0–20、僵硬 0–8、功能 0–68，总分 0–96；标化 = 各项/满分×100% 便于比较。'},
    {'q': '与 guguanjieyan-womac 区别？', 'a': '后者为中文版同算法实现，本页为英文版，评分规则一致。'}]},
'rheumatology/guguanjieyan-womac-zhishu': {
  'title': '骨关节炎 WOMAC 指数（中文版）',
  'scenarios': ['疼痛', '僵硬', '日常生活功能'],
  'examples': [
    {'title': '总分 48', 'body': '中文版 24 条目：疼痛 5 题、僵硬 2 题、功能 17 题各 0–4；假设均选 2 → 疼痛10/僵硬4/功能34，合计 48/96，属中重度骨关节炎。'},
    {'title': '轻度 16', 'body': '各题多 1 分 → 16/96，轻度，推荐股四头肌训练与减重。'}],
  'faqs': [
    {'q': '与 womac 区别？', 'a': '同一量表中文实现，条目与权重一致；用于膝/髋 OA 症状与功能随访。'},
    {'q': '怎么用？', 'a': '治疗前后复测总分与标化百分比，下降 ≥10–15% 常视为有临床意义改善。'}]},
'rheumatology/assessor-10': {
  'title': 'ESSDAI 系统评估（评分式）',
  'scenarios': ['逐项分级', '权重合计', '活动分层'],
  'examples': [
    {'title': '总分 14', 'body': '12 系统下拉逐项：淋巴结2+肺2+肾(权重4)+血液1+关节1+皮肤1+外周神经1+中枢1+腺体1 = 14，≥14 为高活动，提示需系统免疫治疗。'},
    {'title': '低 3', 'body': '合计 3（如关节1+皮肤1+腺体1）→ 低活动，对症为主。'}],
  'faqs': [
    {'q': '与 essdai 区别？', 'a': '本页为评分式（assessor），essdai 为展示式，计分规则一致。'},
    {'q': '权重项？', 'a': '肾、肺、神经等系统「高」级取该域权重分（如肾权重 4），其余低/中/高=1/2/权重。'}]},
'rheumatology/detector-8': {
  'title': 'dRVVT 狼疮抗凝物检测',
  'scenarios': ['筛查/确认', '混合试验', '三步法判读'],
  'examples': [
    {'title': '三步法 3/3 阳性', 'body': 'screen 45s、confirm 38s、正常 35s：延长率 screen%=128.6%>110，比值 45/38=1.18>1.2?临界(1.1–1.2)；混合不纠正 + 比值阳性 → 三步法符合 3/3，LA 阳性。'},
    {'title': '阴性', 'body': 'screen/confirm 均正常、比值 <1.1、混合纠正 → 不符合 LA 标准。'}],
  'faqs': [
    {'q': '三步法？', 'a': '①筛查延长>110% ②混合血浆不纠正 ③比值( screen/confirm )>1.2 阳性；三项全符即 LA 阳性。'},
    {'q': '与 lupus-anticoagulant 区别？', 'a': '本页为 dRVVT 单项检测实现，lupus-anticoagulant 为 dRVVT+sTA 综合判读，互补。'}]},
'rheumatology/rater-16': {
  'title': 'SLEDAI 评分（评分式）',
  'scenarios': ['逐项勾选', '器官分项', '活动分层'],
  'examples': [
    {'title': '总分 12', 'body': '逐项勾选：关节炎2+皮疹2+蛋白尿4+补体降2+dsDNA升2 = 12；器官分项见肾4/皮肤2/免疫4，中重度狼疮活动。'},
    {'title': '无活动 0', 'body': '无项勾选 → 0，缓解期维持治疗。'}],
  'faqs': [
    {'q': '与 sledai 区别？', 'a': '本页为评分式（rater），sledai 为量表展示式，均按 SLEDAI-2K 权重。'},
    {'q': '权重最高项？', 'a': '神经精神 8 分、肾/血管炎 6 分最重，直接影响活动分级与治疗强度。'}]},
'rheumatology/rater-17': {
  'title': 'BVAS 评分（评分式）',
  'scenarios': ['系统分组', '严重度封顶', '活动分层'],
  'examples': [
    {'title': '总分 18', 'body': '分组勾选：全身3+皮肤3+肾6+肺4+神经2 = 18（各系统按 max 封顶）；≥15 重度，诱导缓解治疗。'},
    {'title': '低 6', 'body': '合计 6（皮肤3+关节3）→ 轻中活动，门诊随访。'}],
  'faqs': [
    {'q': '与 bvas 区别？', 'a': '本页为评分式（rater），bvas 为展示式，均用 BVAS v3 分组封顶规则。'},
    {'q': '封顶意义？', 'a': '每系统最高按 max 计（如肾最高 6），避免单系统过度拉高总分、更反映多系统受累。'}]},
'rheumatology/anca-classification': {
  'title': 'ANCA 分型（GPA/MPA/EGPA）',
  'scenarios': ['PR3/cANCA', 'MPO/pANCA', '滴度与器官'],
  'examples': [
    {'title': 'GPA 型', 'body': 'PR3 阳性、MPO 阴性、IIF cANCA、高滴度(≥1:320)，伴肾+肺受累 → 支持肉芽肿性多血管炎(GPA)，需诱导缓解治疗。'},
    {'title': 'MPA 型', 'body': 'MPO 阳性、PR3 阴性、pANCA → microscopic polyangiitis，以肾/肺小血管炎为主。'}],
  'faqs': [
    {'q': 'PR3/MPO 意义？', 'a': 'PR3-ANCA 多对应 GPA，MPO-ANCA 多对应 MPA/EGPA；滴度高低提示活动与复发风险。'},
    {'q': 'IIF 模式？', 'a': 'cANCA 多与 PR3 相关、pANCA 多与 MPO 相关，但确诊以抗原特异性 ELISA 为准。'}]},
'rheumatology/il6-inflammation': {
  'title': 'IL-6 与炎症评估',
  'scenarios': ['CRS/AAS', 'RA/脊柱炎', '感染/败血症'],
  'examples': [
    {'title': '重度炎症', 'body': 'IL-6 85 pg/mL、CRP 120、ESR 90、铁蛋白 800、血小板 450 → 预期 CRP=min(85×1.5,200)=127.5 与实际 120 一致，炎症评分高，提示 IL-6 通路驱动，可考虑托珠单抗。'},
    {'title': '轻度', 'body': 'IL-6 5、CRP 8、ESR 20 → 轻/无炎症，随访即可。'}],
  'faqs': [
    {'q': '预期 CRP 怎么来？', 'a': '工具按 IL-6>7 时 crpExpected=min(IL6×1.5,200) 估算，与实际比对判断一致性。'},
    {'q': '哪些病用IL-6抑制剂？', 'a': ' Castleman、AAS、RA、CRS 等；用药前需排除活动性感染。'}]},
'rheumatology/sapho-syndrome': {
  'title': 'SAPHO 综合征评估',
  'scenarios': ['骨关节', '痤疮/脓疱', '炎症指标'],
  'examples': [
    {'title': '诊断评分高', 'body': '中轴+外周关节炎+胸壁+掌跖脓疱病+银屑病样皮损+CRP/ESR 升高+HLA-B27+ → 多系统特征齐全，SAPHO 诊断评分高，活动度中高。'},
    {'title': '低活动', 'body': '仅慢性痤疮+轻度胸壁痛、炎症指标阴性 → 低活动，对症与 NSAIDs。'}],
  'faqs': [
    {'q': '诊断要点？', 'a': '骨炎/骨髓炎+痤疮/掌跖脓疱/银屑病皮肤表现+无菌性炎症，满足典型组合即可拟诊，需排感染。'},
    {'q': '治疗阶梯？', 'a': 'NSAIDs→柳氮/甲氨蝶呤→TNF/IL-17 抑制剂；骨病与皮肤可分别处理。'}]},
'rheumatology/igg4-level': {
  'title': 'IgG4 相关性疾病评估',
  'scenarios': ['血清 IgG4', 'IgG4/IgG 比值', '器官受累'],
  'examples': [
    {'title': '升高伴多发器官', 'body': 'IgG4 2800 mg/dL（>135）、IgG 1600 → 比值 175%>10%；伴胰腺+涎腺+腹膜后受累 → 符合 IgG4-RD，需激素诱导。'},
    {'title': '轻度升高', 'body': 'IgG4 320、比值 12% 单一淋巴结 → 临界，结合病理（席纹状纤维化/闭塞性静脉炎）确认。'}],
  'faqs': [
    {'q': '诊断标准？', 'a': '典型器官表现+血清 IgG4 升高+病理（IgG4+浆细胞/席纹）+激素敏感综合判；比值>10% 支持但不单独确诊。'},
    {'q': '需鉴别？', 'a': '与淋巴瘤、Castleman、感染、ANCA 相关病鉴别；激素反应好但易复发。'}]},
'rheumatology/mctd-diagnosis': {
  'title': 'MCTD 混合结缔组织病诊断',
  'scenarios': ['高滴度 RNP', '雷诺/指肿', '食管/肌炎'],
  'examples': [
    {'title': '符合 MCTD', 'body': '抗 RNP 高滴度 + 雷诺现象 + 手指肿胀 + 食管蠕动障碍 + 肌炎/关节炎 → 满足血清学+临床标准，符合 MCTD，需随访肺动脉高压。'},
    {'title': '更似 SSc', 'body': 'RNP 非高滴度 + 弥漫皮肤硬化为主 → 更符合系统性硬化，而非 MCTD。'}],
  'faqs': [
    {'q': '核心标准？', 'a': '高滴度抗 U1-RNP 是必备；叠加 SLE/SSc/PM 临床特征但 dsDNA/Sm 多阴性，是 MCTD 特点。'},
    {'q': '为何监测 PAH？', 'a': 'MCTD 可进展为肺动脉高压，是主要预后决定因素，需定期超声与右心评估。'}]},
'rheumatology/behcet-hla': {
  'title': '白塞病 HLA-B51 评估',
  'scenarios': ['口腔/生殖溃疡', '眼/皮肤', '血管/神经'],
  'examples': [
    {'title': '诊断评分高', 'body': '反复口腔溃疡+生殖器溃疡+眼葡萄膜炎+皮肤结节红斑+针刺反应+ HLA-B51 阳性+男性 → 满足国际标准且预后因素多，白塞诊断明确、易内脏受累。'},
    {'title': '不完全型', 'body': '仅口腔+皮肤表现、HLA-B51 阴性 → 不完全型，随访眼/血管并发症。'}],
  'faqs': [
    {'q': '诊断标准？', 'a': '反复口腔溃疡+任意 2 项（生殖器溃疡/眼炎/皮肤/针刺反应）即拟诊；HLA-B51 与血管/神经型相关。'},
    {'q': '预后因素？', 'a': '男性、早发、眼/血管/神经受累提示更重，需积极免疫抑制防失明与卒中。'}]},
'rheumatology/mda5-antibody': {
  'title': '抗 MDA5 皮肌炎评估',
  'scenarios': ['CADM/DM', '快速进展ILD', '溃疡/丘疹'],
  'examples': [
    {'title': '高风险', 'body': 'MDA5 阳性 + 临床无肌病型(CADM) + 快速进展性肺间质病变(rpILD) + 皮肤溃疡/手掌丘疹 + 铁蛋白 1200 → 风险评分高，致死性 ILD 风险大，需积极免疫抑制。'},
    {'title': '中风险', 'body': 'MDA5 阳性 + 典型皮疹但无 rpILD、CK 正常 → 中风险，密切随访肺功能。'}],
  'faqs': [
    {'q': '为何警惕 rpILD？', 'a': '抗 MDA5 阳性尤其 CADM 易伴快速进展 ILD，短期内可致呼吸衰竭，是皮肌炎最危重亚型。'},
    {'q': 'CK 正常有意义吗？', 'a': 'CADM 可肌酶正常但肺损伤重，CK 正常不除外高危，需以影像与铁蛋白判。'}]},
'rheumatology/itp-immune': {
  'title': 'ITP 血小板减少评估',
  'scenarios': ['新发/慢性', '出血分级', '危险分层'],
  'examples': [
    {'title': '极高风险', 'body': '血小板 15×10⁹/L + 黏膜出血 + 老年 + 无感染/药因 → 出血风险极高，需住院、静脉免疫球蛋白/激素，警惕颅内出血。'},
    {'title': '观察', 'body': '血小板 45×10⁹/L、无症状、成人 → 低风险，门诊观察，避免抗凝并教育出血征兆。'}],
  'faqs': [
    {'q': '治疗阈值？', 'a': '成人 <30×10⁹/L 或有出血/高危因素启动治疗；>30 且无症状可观察，儿童新发多自限。'},
    {'q': '危险分层？', 'a': '按血小板计数+出血部位（黏膜/消化道/中枢）+年龄综合；CNS 出血无论计数均急症。'}]},
'rheumatology/complement-level': {
  'title': '补体 C3/C4 与活动评估',
  'scenarios': ['SLE 活动', '冷球蛋白血症', '感染后降低'],
  'examples': [
    {'title': 'SLE 活动', 'body': 'C3 0.5(低)、C4 0.05(低)、dsDNA 强阳、蛋白尿+关节炎 → 活动评分高，提示狼疮活动尤其肾炎，需免疫抑制。'},
    {'title': '感染后一过低', 'body': 'C3 0.7、C4 0.08、dsDNA 阴性、急性感染 → 感染相关补体消耗，抗感染后复查。'}],
  'faqs': [
    {'q': '怎么判活动？', 'a': 'C3/C4 降低+dsDNA 升高+临床（肾/皮疹/浆膜）组合算活动分；补体回升常预示缓解。'},
    {'q': '需排除？', 'a': '感染、冷球蛋白血症、先天缺陷也可低补体，结合背景与动态变化解读。'}]},
'rheumatology/lupus-anticoagulant': {
  'title': '狼疮抗凝物(dRVVT+sTA)判读',
  'scenarios': ['dRVVT', 'sTA 蛇毒试验', 'APS 标准'],
  'examples': [
    {'title': '中阳性+血栓APS', 'body': 'dNR=1.25、sNR=1.15（均>1.1）、ACL 阳性 → LA 中阳性；合并 VTE 史 → 满足实验室+临床标准，诊断抗磷脂综合征，需抗凝。'},
    {'title': '阴性', 'body': '两试验比值均 <1.1 且 ACL/β2GPI 阴性 → 不符 LA，排查其他血栓因。'}],
  'faqs': [
    {'q': '实验室标准？', 'a': 'LA 阳性（dRVVT/sTA 之一）+中高滴度 ACL 或 β2GPI 任一阳性即满足血清学标准。'},
    {'q': '临床标准？', 'a': '动脉/静脉血栓或病理妊娠（≥1 次）满足临床标准；两标准同具即 APS。'}]},
'rheumatology/ssa-ssb': {
  'title': '抗 SSA/SSB 干燥综合征评估',
  'scenarios': ['pSS 诊断', '肾小管/淋巴瘤', '妊娠与新生儿狼疮'],
  'examples': [
    {'title': '妊娠风险', 'body': 'SSA Ro60+ 且 SSB 阳性、补体低、口干眼干+关节痛 → 支持 pSS；若妊娠且 SSA+ 须监测胎儿心脏传导阻滞（新生儿狼疮风险），母用羟氯喹。'},
    {'title': '典型 pSS', 'body': 'ANA 高+RF+SSA/SSB 双阳+口眼干 → 符合原发性干燥综合征分类，查 Schirmer 与唇腺活检。'}],
  'faqs': [
    {'q': 'SSA 亚型？', 'a': 'Ro60 与 Ro52 意义不同，Ro52 更关联肌炎/间质肺；双阳(pSS) 淋巴淋巴瘤与新生儿狼疮风险增。'},
    {'q': '妊娠为何监测？', 'a': '母体 SSA 可经胎盘致胎儿心脏传导阻滞，孕 16–24 周胎心监护，必要时羟氯喹预防。'}]},
'rheumatology/anti-ccp': {
  'title': '抗 CCP/RF 类风湿关节炎评估',
  'scenarios': ['高滴度抗体', '小关节对称', '侵蚀与预后'],
  'examples': [
    {'title': 'RA 高预后不良', 'body': '抗 CCP 200(≥160)、RF 120(≥60)、双手小关节对称肿痛≥6周、晨僵、X 线骨侵蚀 → RA 评分高且预后不良，尽早 DMARD+生物制剂防残。'},
    {'title': '早期未侵蚀', 'body': 'CCP 80、RF 40、小关节肿但无侵蚀 → 早期 RA，积极 csDMARD 争取达标。'}],
  'faqs': [
    {'q': '评分？', 'a': '高滴度自身抗体(+3)+病程≥6周(+1)+小关节/对称/晨僵/侵蚀等组合计；2010 ACR 标准 ≥6 分类 RA。'},
    {'q': '预后？', 'a': '高滴度 CCP/RF、早期侵蚀、多关节、急性相同时→预后差，需强化治疗与严密随访。'}]},
}

def main():
    data = json.load(open(JSON_PATH, encoding='utf-8'))
    changed = 0
    for slug, info in KB.items():
        if slug == 'psychiatry_placeholder':
            continue
        blob = json.dumps(info, ensure_ascii=False)
        if BAD_RE.search(blob):
            print('SELF-CHECK FAIL placeholder in', slug); sys.exit(1)
        if slug not in data:
            print('WARN slug missing in JSON:', slug); continue
        if data[slug] != info:
            data[slug] = info; changed += 1
    json.dump(data, open(JSON_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(JSON_PATH, 'a').write('\n')
    print('KB entries:', len(KB)-1, 'changed:', changed)

if __name__ == '__main__':
    main()
