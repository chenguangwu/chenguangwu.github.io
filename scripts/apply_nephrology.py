# -*- coding: utf-8 -*-
"""Real-ize nephrology deep-dive content: replace template/placeholder text with real clinical examples."""
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
'nephrology/aki-kdigo': {
  'title': '急性肾损伤 KDIGO 分期',
  'scenarios': ['肌酐较基线升高', '尿量持续偏低', '需 RRT 评估'],
  'examples': [
    {'title': '基线 80 升至 180', 'body': '比值=180/80=2.25(≥2.0)→AKI 2 期；同时增量 100µmol/L>26.5，取较重分期。'},
    {'title': '比值 1.8 倍', 'body': '基线 80、当前 144：比值 1.8(1.5–1.9)→1 期，监测尿量避免肾毒性药。'}],
  'faqs': [
    {'q': '分期取什么？', 'a': '肌酐分期与尿量分期取较重者；RRT 即归 3 期。'},
    {'q': '肌酐单位？', 'a': '与基线同单位比较，注意 µmol/L 与 mg/dL 换算(×88.4)。'}]},
'nephrology/ca-p-product': {
  'title': '钙磷乘积评估',
  'scenarios': ['CKD 矿物质评估', '透析患者靶目标', 'iPTH 联动'],
  'examples': [
    {'title': 'Ca 2.2 / P 1.6', 'body': '校正钙 2.2(白蛋白 40)，Ca×P=3.52 mmol²/L²×12.4=43.6 mg²/dL²：<55 达标(透析目标)。'},
    {'title': '高磷超靶', 'body': '血磷>1.78(透析)或>1.45(非透析)：需限磷饮食+磷结合剂，iPTH 同步评估。'}],
  'faqs': [
    {'q': '为何校正钙？', 'a': '低白蛋白时测钙偏低，按 40−白蛋白 校正更接近游离钙。'},
    {'q': '乘积上限？', 'a': '透析患者 Ca×P<55 mg²/dL²，降低血管钙化风险。'}]},
'nephrology/calc-1': {
  'title': 'eGFR (CKD-EPI) 计算',
  'scenarios': ['估算肾小球滤过率', 'CKD 分期', '随访比较'],
  'examples': [
    {'title': '男 60 岁 Scr 133', 'body': 'Scr 133µmol/L=1.5mg/dL：eGFR≈50.7 mL/min/1.73m²→G3a 期。'},
    {'title': '女性示例', 'body': '女 55 岁 Scr 106µmol/L：CKD-EPI 2021 得 eGFR≈53.5→G3a。'}],
  'faqs': [
    {'q': 'CKD-EPI 与 MDRD？', 'a': 'CKD-EPI 在较高 eGFR 更准确，现为标准；种族系数已去除。'},
    {'q': '单位换算？', 'a': 'Scr µmol/L÷88.4=mg/dL 后再代入。'}]},
'nephrology/ckd-staging': {
  'title': 'CKD CGA 分期',
  'scenarios': ['G 分期 + A 分期', '风险分层', '随访转诊'],
  'examples': [
    {'title': 'eGFR 45 / UACR 30', 'body': 'G3a+A2→中风险，年度随访，必要时转诊肾科。'},
    {'title': 'G4 A3', 'body': 'G4(15–29)+A3→高风险，积极管理并发症，准备肾脏替代。'}],
  'faqs': [
    {'q': 'CGA 含义？', 'a': 'G 按 eGFR、A 按白蛋白尿；二者联合定风险与转诊时机。'},
    {'q': '何时转肾科？', 'a': 'G3 起建议评估，G4/G5 或 A3 尽早专科。'}]},
'nephrology/creatinine-clearance': {
  'title': '24h 肌酐清除率 Ccr',
  'scenarios': ['留尿法测清除率', '体表面积校正', '对比 eGFR'],
  'examples': [
    {'title': 'uCr 8.8 / vol 1500', 'body': '尿 Cr 8.8mmol/L、尿量 1500mL、Scr 80：尿率 1.042mL/min，Ccr=8800×1.042/80≈114.6 mL/min；BSA 1.73 免校正。'},
    {'title': '小体型校正', 'body': 'BSA<1.73 时 Ccr×(1.73/BSA) 校正，消除体型偏倚。'}],
  'faqs': [
    {'q': 'Ccr 与 eGFR？', 'a': 'Ccr 受年龄/肌肉影响偏高，eGFR 更稳；二者结合判读。'},
    {'q': '留尿不准？', 'a': '留尿不全会低估，建议复查或改用血公式。'}]},
'nephrology/dialysis-ktv': {
  'title': '透析充分性 Kt/V',
  'scenarios': ['血透单室 Kt/V', '目标值判定', '透析频率影响'],
  'examples': [
    {'title': 'pre 25 / post 10', 'body': 'R=0.4、4h、UF 2L、透后 70kg：spKt/V≈1.07；3 次/周目标 1.2，略不足需增量或延长时间。'},
    {'title': '达标', 'body': 'spKt/V≥1.2(3 次/周)或 eKt/V≥1.2 为充分，过低提示剂量不够。'}],
  'faqs': [
    {'q': 'spKt/V 与 eKt/V？', 'a': 'spKt/V 单室、eKt/V  equilibrated 校正再分布，后者更准。'},
    {'q': '频率影响目标？', 'a': '3 次/周 1.2、2 次/周 1.8、1 次/周 3.0 为标准最低值。'}]},
'nephrology/diuretic-conversion': {
  'title': '利尿剂等效换算',
  'scenarios': ['袢利尿剂互换', '噻嗪类转换', '静脉改口服'],
  'examples': [
    {'title': '呋塞米 40mg', 'body': '等效托拉塞米 20mg 或布美他尼 1mg（呋:托=2:1，呋:布=40:1）。'},
    {'title': '托拉塞米改呋', 'body': '托拉塞米 20mg→呋塞米 40mg，注意口服生物利用度差异。'}],
  'faqs': [
    {'q': '为何换算？', 'a': '不同袢利尿剂效价不同，换药按等效剂量避免过量或不足。'},
    {'q': '肾功能影响？', 'a': '呋塞米在肾衰仍可用，托拉塞米肝代谢受肝功能影响。'}]},
'nephrology/edema-grading': {
  'title': '凹陷性水肿分级',
  'scenarios': ['下肢水肿评估', '凹陷深度与恢复', '双侧对称性'],
  'examples': [
    {'title': '凹陷 2mm', 'body': '压陷 2mm、1 分钟恢复→1 度（轻度）水肿。'},
    {'title': '重度', 'body': '凹陷>4mm、恢复>2 分钟→2–3 度，提示低蛋白或心肾源性。'}],
  'faqs': [
    {'q': '分级标准？', 'a': '按凹陷深度 mm 与恢复秒数分 1–3 度(或 1–4 度)。'},
    {'q': '单侧水肿？', 'a': '单侧警惕静脉/淋巴回流障碍，非全身性疾病。'}]},
'nephrology/egfr': {
  'title': 'eGFR 估算器',
  'scenarios': ['CKD-EPI 2021', '肌酐/胱抑氨酸', '性别年龄校正'],
  'examples': [
    {'title': '女 55 Scr 106', 'body': 'CKD-EPI 2021：eGFR≈53.5 mL/min/1.73m²→G3a 期。'},
    {'title': '胱抑氨酸公式', 'body': '仅胱抑氨酸时 133×比值公式，联合公式更准，适用于肌少/肥胖者。'}],
  'faqs': [
    {'q': '2021 改了什么？', 'a': '去除种族系数，黑人不再乘 1.159，避免低估。'},
    {'q': '何时用胱抑氨酸？', 'a': '肌肉量异常(截瘫/肌少)时血肌酐不可靠，改用 Cystatin C。'}]},
'nephrology/hematuria-source': {
  'title': '血尿来源判断',
  'scenarios': ['畸形红细胞比例', '管型与蛋白', '肾外征象'],
  'examples': [
    {'title': '畸形红细胞 80%', 'body': '畸形(棘形)红细胞≥80%→肾小球性血尿，提示肾炎。'},
    {'title': '血块+疼痛', 'body': '肉眼血尿伴血块、腰痛→多为尿路(结石/肿瘤)非肾小球。'}],
  'faqs': [
    {'q': '畸形红细胞意义？', 'a': '通过肾小球基底膜挤压变形，提示肾源性。'},
    {'q': '需做哪些检查？', 'a': '尿红细胞位相、尿蛋白/管型、影像与膀胱镜按年龄分层。'}]},
'nephrology/jixingshensunshang-kdigo-fenqi': {
  'title': '急性肾损伤 KDIGO 分期',
  'scenarios': ['肌酐较基线升高', '6/12/24h 尿量', 'RRT 指征'],
  'examples': [
    {'title': '基线 80 当前 180', 'body': '比值 2.25(≥2.0)→AKI 2 期；近 12h 尿量<0.5mL/kg/h 也支持。'},
    {'title': '6h 尿量少', 'body': '70kg 近 6h 尿 150mL(0.36mL/kg/h<0.5)持续 6–12h→1 期。'}],
  'faqs': [
    {'q': '与 aki-kdigo 区别？', 'a': '同属 KDIGO AKI 分期，本工具含 6/12/24h 尿量分项输入。'},
    {'q': '3 期定义？', 'a': '比值≥3.0 或升高≥354µmol/L 或 RRT 或<18 且急性降 50%→3 期。'}]},
'nephrology/manager-1': {
  'title': 'CKD 分期管理',
  'scenarios': ['多公式 eGFR', '患者档案留存', '风险与随访'],
  'examples': [
    {'title': 'eGFR 45 + ACR 30', 'body': 'CKD-EPI 2021 得 G3a、ACR 30→A2，中风险年度随访。'},
    {'title': '联合公式', 'body': '肌酐+胱抑氨酸联合 eGFR 更准，尤适用于肌肉量异常患者。'}],
  'faqs': [
    {'q': '管理工具有何用？', 'a': '可存多患者 Scr/胱抑氨酸/ACR，自动分期与随访建议。'},
    {'q': 'ACR 分期？', 'a': 'A1<30、A2 30–300、A3>300 mg/g(白蛋白尿)。'}]},
'nephrology/microalbuminuria': {
  'title': '微量白蛋白尿评估',
  'scenarios': ['糖尿病肾病筛查', '高血压肾损害', '晨尿 UACR'],
  'examples': [
    {'title': 'UACR 50 mg/g', 'body': '30–300 为微量白蛋白尿→糖尿病肾病 III 期，启动 ACEI/ARB、控糖压。'},
    {'title': '正常', 'body': 'UACR<30 正常，糖尿病/高血压者每年复查。'}],
  'faqs': [
    {'q': '为何查微量？', 'a': '早于大量蛋白尿出现，是早期肾损伤的敏感标志。'},
    {'q': '影响因素？', 'a': '运动/感染/血尿可假阳性，需晨尿或重复确认。'}]},
'nephrology/nephrotic-syndrome': {
  'title': '肾病综合征病理分型',
  'scenarios': ['年龄与起病', '光镜/免疫荧光', '电镜足突'],
  'examples': [
    {'title': '中老年膜性肾病', 'body': '中老年+膜性改变+IgG 颗粒沉积+上皮下钉突→膜性肾病，匹配度约 85%。'},
    {'title': '儿童微小病变', 'body': '儿童+光镜近正常+足突融合+免疫阴性→微小病变，激素敏感。'}],
  'faqs': [
    {'q': '分型靠什么？', 'a': '光镜+免疫荧光+电镜三联，结合年龄与起病急缓。'},
    {'q': '为何要分型？', 'a': '不同病理治疗与预后各异，指导免疫抑制策略。'}]},
'nephrology/peritoneal-equilibrium': {
  'title': '腹膜平衡试验 PET',
  'scenarios': ['腹透液/血浆肌酐比', '葡萄糖吸收', '转运分型'],
  'examples': [
    {'title': 'D/P Cr 0.65', 'body': '4h 腹透液/血浆肌酐比 0.65→高平均转运，选短留腹处方。'},
    {'title': '高糖吸收', 'body': 'D/D0 葡萄糖低→高转运，超滤依赖短 dwell，防糖负荷。'}],
  'faqs': [
    {'q': '高转运意义？', 'a': '溶质快清除但超滤易失，需调整留腹时间与浓度。'},
    {'q': '多久做一次？', 'a': '病情/处方变化或超滤下降时复查 PET。'}]},
'nephrology/proteinuria-24h': {
  'title': '24h 蛋白尿定量',
  'scenarios': ['定量严重度', '浓度换算', '肾病范围判定'],
  'examples': [
    {'title': '1.5g / 1500mL', 'body': '24h 蛋白 1.5g、尿量 1500mL→浓度约 1.0g/L，未达肾病范围(<3.5g)。'},
    {'title': '肾病范围', 'body': '≥3.5g/24h 伴低白蛋白→肾病综合征标准，需病理评估。'}],
  'faqs': [
    {'q': '留尿不全？', 'a': '留尿天数不足会低估，建议完整 24h 并记录总量。'},
    {'q': '与 UPCR 关系？', 'a': 'UPCR≈0.7×24h g/24h，可作筛查替代。'}]},
'nephrology/renal-anemia-epo': {
  'title': '肾性贫血 EPO 剂量',
  'scenarios': ['血透起始量', '腹透维持量', '铁状态联动'],
  'examples': [
    {'title': 'Hgb 85 体重 60 血透', 'body': '起始 50 IU/kg×60=3000 IU/次，每周 3 次=9000 IU；铁充足( ferritin≥200、TSAT≥20)才有效。'},
    {'title': '维持量', 'body': 'Hgb 接近靶(100–110)后减量至 30 IU/kg 维持，防过高。'}],
  'faqs': [
    {'q': '靶 Hgb？', 'a': '非透析/透析均建议 100–110 g/L，避免>130 增血栓风险。'},
    {'q': '铁为何重要？', 'a': '铁缺乏时 EPO 效差，先补铁达标再调 EPO。'}]},
'nephrology/renal-biopsy': {
  'title': '肾活检解读',
  'scenarios': ['光镜+免疫荧光', '电镜足突', '狼疮分型'],
  'examples': [
    {'title': '微小病变', 'body': '光镜近正常+免疫阴性+足突消失→微小病变，儿童激素敏感。'},
    {'title': '狼疮 IV 型', 'body': '弥漫增生+满堂亮(full-house)→狼疮性肾炎 IV 型，需免疫抑制。'}],
  'faqs': [
    {'q': '三联缺一不可？', 'a': '光镜定位、免疫定抗原、电镜看沉积部位，三者互补。'},
    {'q': '禁忌？', 'a': '孤立肾、出血倾向、未控高血压慎用，权衡获益。'}]},
'nephrology/renal-tubular-acidosis': {
  'title': '肾小管酸中毒分型',
  'scenarios': ['代酸+高氯', '尿 pH 与钾', '阴离子隙'],
  'examples': [
    {'title': '远端Ⅰ型 RTA', 'body': 'pH 7.3、HCO₃ 16、尿 pH 6.5(不酸化)、低钾→远端(Ⅰ型)RTA。'},
    {'title': '近端Ⅱ型', 'body': 'HCO₃ 低、尿 pH 可<5.5、FE-HCO₃ 高→近端(Ⅱ型)，常伴其他肾小管病。'}],
  'faqs': [
    {'q': 'Ⅰ与Ⅱ区别？', 'a': 'Ⅰ型不能酸化尿(pH>5.5)，Ⅱ型碳酸氢盐重吸收障碍(FE-HCO₃ 高)。'},
    {'q': '补碱注意？', 'a': '补枸橼酸/碳酸氢钠纠酸，Ⅰ型常需补钾，监测血钙。'}]},
'nephrology/shenxiaoqiulvguolv-24h-jiganqingchu-ccr': {
  'title': '24h 肌酐清除 Ccr',
  'scenarios': ['留尿法测 GFR', 'Cockcroft-Gault', 'BSA 校正'],
  'examples': [
    {'title': 'Scr 80 / uCr 8.8 / vol 1500', 'body': 'Ccr=(8.8×11.312×1500/1000)/(80×1440)=114.6 mL/min；CG=(140−40)×65/(72×0.905)=... 校正 BSA 1.73。'},
    {'title': 'CG 公式', 'body': 'CG=((140−age)×kg)/(72×Scr)，女×0.85；粗略估剂量但偏高。'}],
  'faqs': [
    {'q': '与肌酐清除区别？', 'a': '本工具同时给 Ccr 与 Cockcroft-Gault，后者常用于药量调整。'},
    {'q': 'BSA 校正？', 'a': 'Ccr×(1.73/BSA) 消除体型影响，标准体表面积 1.73。'}]},
'nephrology/uacr': {
  'title': 'UACR 尿白蛋白肌酐比',
  'scenarios': ['随机尿评估', '单位换算', 'A1/A2/A3'],
  'examples': [
    {'title': '白蛋白 30 / 尿肌酐 8.8', 'body': '尿肌酐 8.8mmol/L×0.113=0.994g/L；UACR=30/0.994≈30.2 mg/g→A2(微量)。'},
    {'title': 'A3 大量', 'body': 'UACR>300 mg/g→A3 大量白蛋白尿，提示显著肾损伤。'}],
  'faqs': [
    {'q': '为何比肌酐？', 'a': '校正尿浓度波动，随机尿即可反映排泄率。'},
    {'q': '单位换算？', 'a': '尿肌酐 mmol/L×0.113、mg/dL×0.01 得 g/L 再比。'}]},
'nephrology/urine-electrolyte': {
  'title': '尿电解质排泄',
  'scenarios': ['FE-Na 鉴别', '尿阴离子隙', '肾前/肾性'],
  'examples': [
    {'title': 'FE-Na 0.29%', 'body': 'uNa 40、sNa 140、sCr 80、uCr 8000：FE-Na=(40×80)/(140×8000)×100=0.29%<1→肾前性(容量不足)。'},
    {'title': 'UAG 负值', 'body': 'UAG=uNa+uK−uCl<0→提示代谢性酸中毒时尿可酸化(远端功能在)。'}],
  'faqs': [
    {'q': 'FE-Na 切点？', 'a': '<1% 肾前性、1–2% 灰区、>2% 急性肾小管坏死。'},
    {'q': 'UAG 用途？', 'a': '代酸时 UAG<0 提示远端酸化正常，>0 提示远端 RTA。'}]},
'nephrology/urine-osmolality': {
  'title': '尿渗透压与浓缩',
  'scenarios': ['随机/晨尿', '自由水清除', '浓缩功能'],
  'examples': [
    {'title': '400 / 300 随机', 'body': '尿渗透 400、血 300、随机>300→浓缩功能正常。'},
    {'title': '低渗尿', 'body': '尿渗透接近血(比值≈1)且多尿→尿崩症可能，查禁水试验。'}],
  'faqs': [
    {'q': '晨尿标准？', 'a': '晨尿应>600 mOsm/kg，随机>300 为正常低限。'},
    {'q': '自由水清除？', 'a': 'CH₂O=尿率×(1−尿/血渗透)，负值表示浓缩。'}]},
'nephrology/vascular-calcification': {
  'title': '血管钙化评分',
  'scenarios': ['腹主动脉 X 线', 'L1–L4 分段', '总分评估'],
  'examples': [
    {'title': '四段各 1.5 分', 'body': 'L1–L4 前/后壁各 0–3 分；示例每段 1.5 合计 6 分→中度钙化。'},
    {'title': '重度', 'body': '总分接近 24→重度腹主动脉钙化，心血管事件风险高。'}],
  'faqs': [
    {'q': '评分部位？', 'a': '腹主动脉 L1–L4 水平前/后壁，各段 0–3 分。'},
    {'q': '临床意义？', 'a': '钙化积分越高，透析者心血管死亡率越高，指导干预。'}]},
'nephrology/rater-15': {
  'title': '血管钙化评分',
  'scenarios': ['腹主动脉 X 线', 'L1–L4 分段', '总分评估'],
  'examples': [
    {'title': '四段各 1.5 分', 'body': 'L1–L4 前/后壁各 0–3 分；示例合计 6 分→中度钙化。'},
    {'title': '重度', 'body': '总分近 24→重度腹主动脉钙化，提示高心血管风险。'}],
  'faqs': [
    {'q': '与 vascular-calcification 关系？', 'a': '同属腹主动脉钙化评分，本键为旧 slug，算法一致。'},
    {'q': '怎么用？', 'a': '按 L1–L4 水平前/后壁评分求和，分级干预。'}]},
}

def main():
    data = json.load(open(PATH, encoding='utf-8'))
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
