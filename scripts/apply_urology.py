# -*- coding: utf-8 -*-
"""urology 分类 deep-dive 真实化：用真实算例替换第六型/弱泛化占位。
KB 以 slug 为键（对应 i18n/tools/content_deepdive.json 的 urology/<slug>）。
结构：title / scenarios[3] / examples[2] / faqs[2]。
自检：任何条目含 BAD_RE 占位词则退出（code 1），绝不落盘占位内容。
写回：json.dump(indent=1, ensure_ascii=False) + 末尾换行，保持仓库规范。
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

BAD_RE = re.compile(
    r'统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|'
    r'标准化，再批量|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|'
    r'高频复用模板|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|复用模板示例|保留复用模板|'
    r'先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|先用一组可复现输入|'
    r'同一输入样本测试默认和边界情况|选择两组不同来源样本并同步口径定义'
)

KB = {
  'urology/urine-flow-rate': {
    'title': '尿流率（Qmax）正常参考',
    'scenarios': ['男性排尿评估', '女性排尿评估', '老年 BPH 筛查'],
    'examples': [
      {'title': '男性 Qmax 12 mL/s', 'body': '男性正常阈值≥15，12<15 提示尿流减弱，需结合 IPSS 与残余尿；若排尿量<150mL 结果可靠性降低。'},
      {'title': '女性 Qmax 22 mL/s', 'body': '女性正常阈值≥20，22≥20 属正常尿流率，无梗阻征象。'},
    ],
    'faqs': [
      {'q': 'Qmax 偏低就一定是梗阻吗？', 'a': '不一定，尿量<150mL、腹压排尿、前列腺增生或逼尿肌无力均可致 Qmax 下降，需结合曲线与残余尿综合判断。'},
      {'q': '老年男性 Qmax 略低如何解读？', 'a': '≥60 岁男性 Qmax 生理性下降常见，若 10–15 且无症状可观察，<10 建议进一步检查。'},
    ],
  },
  'urology/urethral-stricture': {
    'title': '尿道狭窄尿流率预判',
    'scenarios': ['排尿变细', '尿线分叉', '术后复查'],
    'examples': [
      {'title': '平台型 Qmax 8', 'body': 'qmax=8、qave=6、曲线平台型：ratio=8/6≈1.33，平台型计 +3 分，提示膀胱出口/尿道梗阻可能，建议尿道造影。'},
      {'title': '钟型 Qmax 18', 'body': 'qmax=18、qave=10、钟型曲线：ratio=1.8，无狭窄征象，尿量≥150mL 结果可靠。'},
    ],
    'faqs': [
      {'q': '哪项最支持狭窄？', 'a': '平台型或间断型曲线 + 低 Qmax（<10mL/s）组合特异度最高，单纯 Qmax 下降需排除 BPH。'},
      {'q': '排尿量不足影响吗？', 'a': '尿量<150mL 时尿流率可信度下降，报告会标注警告，建议充盈后重测。'},
    ],
  },
  'urology/residual-urine': {
    'title': '残余尿量经腹 B 超推算',
    'scenarios': ['术后排尿', '神经源性膀胱', 'BPH 随访'],
    'examples': [
      {'title': '经腹 0.75 系数', 'body': 'w=5.0、h=4.0、d=4.0cm，PVR=0.75×5×4×4=60mL；排尿量 200mL，膀胱总量 260mL，有效率 200/260×100=76.9%。'},
      {'title': '残余 150mL', 'body': '残余≥150mL 提示排尿不全，神经源性膀胱或严重 BPH 需间歇导尿或评估上尿路。'},
    ],
    'faqs': [
      {'q': '经腹与经直肠系数差异？', 'a': '经腹常用 0.75，经直肠椭球 0.52 更准；本器按所选公式系数计算，临床以经直肠为金标准参考。'},
    ],
  },
  'urology/canyuniaoliang-jingfubchao-tuisuan': {
    'title': '残余尿量经腹 B 超推算（双系数）',
    'scenarios': ['门诊速算', '床旁 B 超', '随访对比'],
    'examples': [
      {'title': '经腹公式 60mL', 'body': '5.0×4.0×4.0×0.75=60.0mL（经腹）；椭球 0.52×5×4×4=41.6mL，二者差异体现测量假设，报告并列展示。'},
      {'title': '复查下降', 'body': '治疗前 80mL、治疗后 35mL，残余下降提示排尿改善，可延长导尿间隔。'},
    ],
    'faqs': [
      {'q': '为何有两个结果？', 'a': '经腹 0.75 与椭球 0.52 为不同几何假设，经腹更保守，临床以趋势对比为主。'},
    ],
  },
  'urology/bladder-capacity': {
    'title': '膀胱容量（排尿量+残余尿）测量',
    'scenarios': ['尿潴留评估', '间歇导尿计划', '容量训练'],
    'examples': [
      {'title': '容量 350mL', 'body': '排尿量 300 + 残余 50 = 350mL，预期 400mL 的 87.5%，属正常偏低；有效率 300/350×100=85.7%。'},
      {'title': '小容量 180mL', 'body': '排尿 120 + 残余 60 = 180mL（预期 400 的 45%），提示膀胱容量减小，常见于间质性膀胱炎或纤维化。'},
    ],
    'faqs': [
      {'q': '预期容量怎么定？', 'a': '成人预期约 400mL，按年龄与性别微调；实际/预期比值<50% 提示容量显著下降。'},
    ],
  },
  'urology/calc-1': {
    'title': 'IPSS 国际前列腺症状评分',
    'scenarios': ['BPH 筛查', '药物疗效随访', '术前评估'],
    'examples': [
      {'title': 'IPSS 19 分', 'body': '7 项症状合计 19（中度 8-19）、生活质量 3 分，总 22/35，提示中度下尿路症状，建议 α 阻滞剂治疗并随访尿流率。'},
      {'title': 'IPSS 7 分', 'body': '合计 7（轻度 0-7）、QoL 1，总 8/35，轻度症状，生活方式指导即可。'},
    ],
    'faqs': [
      {'q': '分级标准？', 'a': '0-7 轻度、8-19 中度、20-35 重度；QoL≥4 或总分≥20 建议积极干预。'},
    ],
  },
  'urology/ipss-score': {
    'title': 'IPSS 评分（国际前列腺症状）自动计算',
    'scenarios': ['门诊自评', '随访记录', '研究入组'],
    'examples': [
      {'title': '总分 14', 'body': '各项 2 分×7=14（中度），QoL 2，提示中度症状，3-6 月复查；夜尿 2 次纳入第 7 项。'},
      {'title': '总分 25', 'body': '各项 3-4 分合计 25（重度），QoL 5，建议尿动力学与前列腺评估。'},
    ],
    'faqs': [
      {'q': '7 项包含哪些？', 'a': '排尿不尽、2h 内再排、间断、尿急、尿线变细、费力、夜尿；每项 0-5，加 QoL 0-6 共 35。'},
    ],
  },
  'urology/rater-3': {
    'title': 'IPSS 症状总分（7 项求和）',
    'scenarios': ['快速评分', '教学演示', '对比'],
    'examples': [
      {'title': '合计 12', 'body': '排尿不尽 2+再排 2+间断 1+尿急 2+尿线 2+费力 2+夜尿 1=12（中度），QoL 对应基本不满意。'},
      {'title': '合计 0', 'body': '7 项均 0 分，无症状，QoL 0（高兴），正常。'},
    ],
    'faqs': [
      {'q': '与计算器差异？', 'a': '本器仅汇 7 项症状分（0-35），不含 QoL 独立维度，结果与其他 IPSS 工具一致。'},
    ],
  },
  'urology/prostate-volume': {
    'title': '前列腺体积（椭球公式）计算',
    'scenarios': ['BPH 评估', 'PSA 密度', '手术规划'],
    'examples': [
      {'title': '椭球 30.6mL', 'body': '4.0×3.5×4.2×0.52=30.6mL；PSA 3.0，PSAD=3.0/30.6=0.098，低于 0.15 低危。'},
      {'title': '体积 80mL', 'body': '径线增大至体积 80mL，PSA 8 时 PSAD=0.10；体积>80mL 时单极 TURP 出血风险升高，倾向剜除术。'},
    ],
    'faqs': [
      {'q': '系数 0.52 含义？', 'a': '椭球体积 V=π/6·a·b·c≈0.52·d1·d2·d3，经直肠三径测量最常用。'},
    ],
  },
  'urology/calc-volume': {
    'title': '前列腺体积（超声径线）计算（系数可选）',
    'scenarios': ['经直肠', '经腹', '研究'],
    'examples': [
      {'title': '4.5×3.5×4.0', 'body': '0.52×4.5×3.5×4.0=32.8mL；若填 PSA 可一并算 PSAD，本例未填 PSA 仅给体积。'},
      {'title': '球形近似', 'body': '选 π/6 系数得同样 32.8mL，与椭球一致；临床报告以椭球为准。'},
    ],
    'faqs': [
      {'q': '系数怎么选？', 'a': '0.52 椭球、0.5236=π/6、球形近似分别对应不同假设，三径齐备时优选椭球。'},
    ],
  },
  'urology/iief5-score': {
    'title': 'IIEF-5 勃起功能评分',
    'scenarios': ['ED 筛查', '用药随访', '伴侣咨询'],
    'examples': [
      {'title': '总分 14', 'body': '5 项合计 14（中度 ED 11-16），勃起信心与维持均下降，建议 PDE5i 并评估心血管风险。'},
      {'title': '总分 22', 'body': '合计 22（轻度 17-21 边缘），性生活基本满意，可观察加生活方式干预。'},
    ],
    'faqs': [
      {'q': '分级？', 'a': '22-25 正常、17-21 轻度、12-16 中度、8-11 中重度、5-7 重度；任一项 0 分记无活动。'},
    ],
  },
  'urology/rater-4': {
    'title': 'IIEF-5 总分（5 项求和）',
    'scenarios': ['快速评分', '教学', '对比'],
    'examples': [
      {'title': '合计 20', 'body': '勃起信心 4+硬度足够 4+维持插入 4+完成性交 4+满意 4=20（轻度），接近正常。'},
      {'title': '合计 8', 'body': '各项 1-2 分合计 8（重度），建议专科就诊。'},
    ],
    'faqs': [
      {'q': '与完整量表？', 'a': '本器汇 5 项总分（0-25），完整 IIEF-15 另有射精/满意度维度，结论方向一致。'},
    ],
  },
  'urology/urodynamics': {
    'title': '尿动力学 BOOI/BCI 评估',
    'scenarios': ['BOO 判断', '逼尿肌收缩力', '神经源性'],
    'examples': [
      {'title': 'BOOI 40', 'body': 'Pdet@Qmax=70、Qmax=15：BOOI=70−2×15=40>40 提示膀胱出口梗阻；BCI=70+5×15=145 收缩力正常。'},
      {'title': 'BOOI 20', 'body': 'Pdet=40、Qmax=10：BOOI=40−20=20（临界），BCI=90，提示可疑梗阻或弱收缩，需结合影像。'},
    ],
    'faqs': [
      {'q': 'BOOI/BCI 阈值？', 'a': 'BOOI>40 梗阻、<40 无梗阻（20-40 临界需结合）；BCI>100 正常收缩、<100 弱收缩。'},
    ],
  },
  'urology/assessor-pressure': {
    'title': '逼尿肌压力分级（BOOI/BCI）',
    'scenarios': ['梗阻分级', '收缩力分级', '报告'],
    'examples': [
      {'title': '梗阻+正常收缩', 'body': 'BOOI 50（梗阻）、BCI 130（正常收缩力），处理以解除梗阻为主（如 TURP）。'},
      {'title': '弱收缩力', 'body': 'BOOI 10（无梗阻）、BCI 80（弱收缩），排尿困难源于逼尿肌无力，宜间歇导尿而非手术。'},
    ],
    'faqs': [
      {'q': 'PVR 怎么分级？', 'a': '<50 正常、50-100 轻度、100-200 中度、>200 重度，结合 BOOI 综合决策。'},
    ],
  },
  'urology/psa-density': {
    'title': 'PSA 密度（PSAD）与穿刺指征',
    'scenarios': ['PSA 升高', '灰区', '穿刺决策'],
    'examples': [
      {'title': 'PSAD 0.12', 'body': 'PSA 6、体积 50mL：PSAD=6/50=0.12<0.15 低危；但年龄 65 年龄限 4.5，PSA 6>4.5 仍建议 MRI 后穿刺。'},
      {'title': 'PSAD 0.30', 'body': 'PSA 10、体积 33mL：PSAD=10/33=0.30>0.25 高危，直接建议穿刺活检。'},
    ],
    'faqs': [
      {'q': '年龄限怎么用？', 'a': '按年龄 PSA 阈值：<50→2.5、<60→3.5、<70→4.5、≥70→6.5；超阈值结合 PSAD/DRE/MRI 决策。'},
    ],
  },
  'urology/stone-size-assessment': {
    'title': '结石排石概率评估',
    'scenarios': ['保守排石', 'ESWL 决策', '急诊'],
    'examples': [
      {'title': '5mm 下段', 'body': 'size=5（base 60）、输尿管下段 locFactor 1.25：prob=60×1.25=75%，可试保守排石加 α 阻滞剂。'},
      {'title': '12mm 肾盂', 'body': 'size=12（base 10）、肾盂 0.7：prob=10×0.7=7%，极低，建议 ESWL/URL，伴发热优先解除梗阻。'},
    ],
    'faqs': [
      {'q': '哪些情况不保守？', 'a': '发热+梗阻（脓肾风险）、肾功能受损、结石>10mm 上段、剧痛不止，需紧急干预而非等待排石。'},
    ],
  },
  'urology/stone-composition': {
    'title': '尿路结石成分（红外）查询',
    'scenarios': ['成分分析', '复发预防', '饮食指导'],
    'examples': [
      {'title': '草酸钙结石', 'body': '最常见（约 70-80%），红外显示一水/二水草酸钙；预防以限草酸（菠菜坚果）加多饮水加正常钙摄入为主。'},
      {'title': '尿酸结石', 'body': '尿酸结石可溶，碱化尿液（枸橼酸钾）使 pH>6.5 可促溶；与代谢综合征/痛风相关，需降尿酸。'},
    ],
    'faqs': [
      {'q': '成分决定预防？', 'a': '是，草酸钙/磷酸钙/尿酸/感染石/胱氨酸预防策略不同，成分分析是复发预防的关键。'},
    ],
  },
  'urology/turp-parameters': {
    'title': '前列腺手术（TURP/激光）参数设定',
    'scenarios': ['术式选择', '抗凝管理', '体积适配'],
    'examples': [
      {'title': '体积 60mL 双极', 'body': '体积 60mL 选双极等离子（PKRP）或 HoLEP；单极 TURP 体积>80mL 出血风险升高不建议。'},
      {'title': '抗凝患者', 'body': '服抗凝药者优先 HoLEP/ThuLEP（封闭好），围术期按指南停抗凝并用桥接，降低出血。'},
    ],
    'faqs': [
      {'q': '体积与术式？', 'a': '<30mL 可选 TURP/激光，30-80mL 双极或激光，>80mL 剜除术（HoLEP/ThuLEP）更优。'},
    ],
  },
  'urology/catheter-selection': {
    'title': '导尿管（型号/球囊）选择',
    'scenarios': ['留置导尿', '术后', 'CIC'],
    'examples': [
      {'title': '成人男性 16Fr', 'body': '成人男性常规留置 16Fr、球囊 10mL 双腔 Foley；血尿/血块冲洗选 18-22Fr 三腔。'},
      {'title': 'TURP 术后 22Fr', 'body': '前列腺术后选 22Fr 三腔 Foley（球囊 30mL 牵引止血），乳胶过敏换硅胶。'},
    ],
    'faqs': [
      {'q': '型号怎么选？', 'a': '按性别/年龄/适应症：男性 16、女性 14、儿童 8-10Fr；血尿或术后加大并选三腔。'},
    ],
  },
  'urology/uti-diagnosis': {
    'title': '尿路感染菌落计数诊断',
    'scenarios': ['中段尿', '导管尿', '症状解读'],
    'examples': [
      {'title': '≥10⁵ + 症状', 'body': '菌落 ≥10⁵ CFU/mL + 白细胞酯酶/亚硝酸盐阳性 + LUTS，诊断 UTI，经验性抗感染；大肠埃希菌最常见。'},
      {'title': '10⁴ 中段尿', 'body': '10⁴-10⁵ CFU/mL 为可疑，需结合症状与镜检，无症状携带者可能不需治疗。'},
    ],
    'faqs': [
      {'q': '导管尿标准？', 'a': '导尿管相关 UTI 常采用 ≥10³ CFU/mL 阈值（因导管污染），有症状即治疗。'},
    ],
  },
  'urology/varicocele-grading': {
    'title': '精索静脉曲张（超声）分度',
    'scenarios': ['不育评估', '体检发现', '手术指征'],
    'examples': [
      {'title': '内径 3.2mm 反流', 'body': '平静+Valsalva 内径 3.2mm、反流≥2s、平静呼吸亦反流：超声 3 级/临床 III 度，左侧多见，建议手术。'},
      {'title': '内径 2.0mm', 'body': '内径 2.0mm、反流<2s：1 级（亚临床），无症状可观察，不育者评估精液。'},
    ],
    'faqs': [
      {'q': '手术指征？', 'a': '阴囊痛、不育（精液异常）、睾丸萎缩或进行性分度，尤其青少年双侧/右侧应积极处理。'},
    ],
  },
  'urology/hematuria-differential': {
    'title': '血尿（RBC 形态）鉴别',
    'scenarios': ['肾小球性血尿', '非肾小球性血尿', '无症状镜下'],
    'examples': [
      {'title': '多形型 80%', 'body': 'RBC 异形率 80%≥70% 支持肾小球性（IgA 肾病/肾炎）；无血块、伴蛋白尿更支持。'},
      {'title': '均一型', 'body': '均一型 RBC 支持非肾小球性（结石/肿瘤/感染），需影像加膀胱镜排查尿路病变。'},
    ],
    'faqs': [
      {'q': '为什么看形态？', 'a': '异形 RBC（多形型）源于肾小球基底膜挤压，均一型源于下尿路，是定位关键。'},
    ],
  },
  'urology/penile-rigidity': {
    'title': '阴茎硬度（EHS）分级',
    'scenarios': ['ED 分级', 'NPT 评估', '疗效'],
    'examples': [
      {'title': 'EHS 3 级', 'body': 'EHS 3 级（硬可插入未完全坚挺）= 轻度 ED；NPT 次数≥3、时长≥10min、硬度≥70% 为正常。'},
      {'title': 'EHS 1 级', 'body': 'EHS 1 级（增大不硬）= 重度 ED，建议药物/真空/假体等综合治疗。'},
    ],
    'faqs': [
      {'q': 'NPT 正常标准？', 'a': '夜间勃起≥3 次、单次≥10min、硬度≥70% 且根粗≥3cm 提示器质性 ED 可能性低。'},
    ],
  },
  'urology/hydrocele-assessment': {
    'title': '鞘膜积液（透光试验）判断',
    'scenarios': ['阴囊肿块', '小儿鞘状突', '成人'],
    'examples': [
      {'title': '睾丸鞘膜积液', 'body': '透光试验阳性、积液包绕睾丸、深度 20mm：成人型睾丸鞘膜积液，>25mm 或症状明显建议手术。'},
      {'title': '交通性', 'body': '平卧缩小（与腹腔相通）为交通性，多见于小儿鞘状突未闭，需高位结扎。'},
    ],
    'faqs': [
      {'q': '透光试验意义？', 'a': '阳性（透光）支持鞘膜积液/精液囊肿，阴性需警惕疝或肿瘤，结合超声定位。'},
    ],
  },
  'urology/hydronephrosis': {
    'title': '肾积水（SFU/APD）量化',
    'scenarios': ['胎儿肾积水', '成人梗阻', '随访'],
    'examples': [
      {'title': 'APD 25mm SFU3', 'body': '成人 APD 25mm（≥20 提示梗阻）、SFU 3 级（肾盂+大/小肾盏、皮质正常），需解除梗阻保肾。'},
      {'title': '胎儿 SFU2', 'body': '胎儿肾盂前后径轻扩、SFU 2 级，多可随访观察，产后复查超声。'},
    ],
    'faqs': [
      {'q': 'SFU 分级？', 'a': '0 无、1 肾盂、2 +大盏、3 +小盏皮质正常、4 +皮质变薄；成人 APD≥20mm 或 SFU≥4 积极处理。'},
    ],
  },
}


def main():
    # 自检：KB 内不得出现占位词
    for k, v in KB.items():
        blob = json.dumps(v, ensure_ascii=False)
        m = BAD_RE.search(blob)
        if m:
            print('BAD placeholder in', k, '->', m.group())
            sys.exit(1)

    with open(JSON_PATH, encoding='utf-8') as f:
        data = json.load(f)

    changed = 0
    for slug, new in KB.items():
        key = slug if slug.startswith('urology/') else 'urology/' + slug
        old = data.get(key)
        if old != new:
            data[key] = new
            changed += 1

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')

    print('KB entries:', len(KB), 'changed:', changed)


if __name__ == '__main__':
    main()
