# -*- coding: utf-8 -*-
"""Real-ize pediatrics deep-dive content: replace template/placeholder text with real clinical examples."""
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
'pediatrics/neonatal-jaundice': {
  'title': '新生儿黄疸小时胆红素',
  'scenarios': ['Bhutani 列线图', '光疗/换血阈值', '高危因素'],
  'examples': [
    {'title': '48h TSB 14', 'body': '48 小时 TSB 14 mg/dL、胎龄 38 周：位于 40–75 分位；低风险光疗阈值≈12、需光疗(14≥12)。'},
    {'title': '高危阈值更低', 'body': '同值若胎龄<38 或高危，光疗阈值≈10 mg/dL，更早干预。'}],
  'faqs': [
    {'q': '单位换算？', 'a': 'mg/dL×17.1=µmol/L；14 mg/dL≈239 µmol/L。'},
    {'q': '何时换血？', 'a': 'TSB 超过换血阈值(随小时/胎龄)或上升过快，警惕胆红素脑病。'}]},
'pediatrics/xinshengerhuangdan-xiaoshidanhongsu-quxian': {
  'title': '新生儿黄疸小时胆红素曲线',
  'scenarios': ['Bhutani 百分位', 'AAP 2022 阈值', '单位切换'],
  'examples': [
    {'title': '48h 14 mg/dL', 'body': 'Bhutani 约 40–75 分位；低风险光疗阈值≈12 mg/dL → 超标需光疗。'},
    {'title': '高危更严', 'body': '胎龄<38 周或高危，光疗阈值降至≈10 mg/dL，列线图整体左移。'}],
  'faqs': [
    {'q': '与 neonatal-jaundice 关系？', 'a': '同属小时胆红素曲线，本键为旧 slug，算法一致。'},
    {'q': '百分位含义？', 'a': '同小时龄 TSB 在人群分布位置，越高越接近光疗线。'}]},
'pediatrics/dehydration-assessment': {
  'title': '脱水 Gorelick 评估',
  'scenarios': ['Gorelick 评分', '累计丢失量', '口服/静脉'],
  'examples': [
    {'title': '10kg 评分 4', 'body': 'Gorelick 4 分→缺失约 7.5%：累计丢失=10×0.075=750 mL，需补充。'},
    {'title': '轻中重', 'body': '评分≤2 约 4%、3–6 约 7.5%、≥7 约 12% 体液缺失。'}],
  'faqs': [
    {'q': 'Gorelick 适用？', 'a': '适用于 1 月–5 岁腹泻患儿快速分度，结合体重变化更准。'},
    {'q': '补液原则？', 'a': '先补累计丢失、再给维持量(100mL/kg 前 10kg)，口服不耐受则静脉。'}]},
'pediatrics/diarrhea-dehydration': {
  'title': '腹泻脱水分度',
  'scenarios': ['体征分度', '维持量计算', '血便警示'],
  'examples': [
    {'title': '10kg 水样便', 'body': '维持量=1000 mL/日(前 10kg×100)；中重度按缺失补累计量。'},
    {'title': '血便', 'body': '血便提示细菌性肠炎，需培养；EHEC 慎用抗生素以防 HUS。'}],
  'faqs': [
    {'q': '维持量公式？', 'a': '前 10kg×100、10–20kg 部分×50、>20kg 部分×20 mL/日。'},
    {'q': '霍乱？', 'a': '米泔水样便按甲类管理，大量快速口服/静脉补液。'}]},
'pediatrics/chd-assessment': {
  'title': '先心病杂音血氧评估',
  'scenarios': ['粗糙杂音', '上下肢血氧差', '发给/气促'],
  'examples': [
    {'title': '粗糙杂音+差', 'body': '粗糙病理性杂音 + 上下肢 SpO₂ 差>3% → 高危先心，急查心超。'},
    {'title': '单纯柔和', 'body': '柔和杂音、血氧正常、无发给→低危，随访鉴别良性杂音。'}],
  'faqs': [
    {'q': '血氧差意义？', 'a': '导管前(右臂)与导管后(下肢)差>3% 提示主动脉缩窄/导管依赖先心。'},
    {'q': '何为急症？', 'a': '发给+气促+喂养困难+粗糙杂音，需在新生儿期干预。'}]},
'pediatrics/assessor-spo2': {
  'title': '先心病筛查(SpO₂)',
  'scenarios': ['右上肢/足血氧', '差值判定', '重复确认'],
  'examples': [
    {'title': '右手 95 足 90', 'body': '差=5%>3% 且最低 90 → 高危，需心超排除导管依赖先心。'},
    {'title': '均≥95', 'body': '双手足≥95 且差<3%→筛查阴性，仍随访喂养与发给。'}],
  'faqs': [
    {'q': '筛查时机？', 'a': '生后 24–48h、安静状态下测，哭闹会假性偏低。'},
    {'q': '与 chd-assessment 区别？', 'a': '本工具聚焦脉搏血氧差值，chd-assessment 含杂音与症状综合。'}]},
'pediatrics/ddst-screening': {
  'title': 'DDST 发育筛查',
  'scenarios': ['4 能区', '月龄适配', '异常/可疑'],
  'examples': [
    {'title': '18 月 2 能区延迟', 'body': '个人-社交/精细等 2 能区未通过→异常，2–3 周复查仍异常转诊。'},
    {'title': '正常', 'body': '各能区通过≥80%→正常，定期体检随访。'}],
  'faqs': [
    {'q': '能区有哪些？', 'a': '个人-社交、精细动作、语言、大运动；任 2 能区延迟为异常。'},
    {'q': '筛查非诊断', 'a': 'DDST 为筛查，异常需小儿神经/发育专科进一步评估。'}]},
'pediatrics/developmental-milestones': {
  'title': '发育里程碑评估',
  'scenarios': ['粗细动作言语社交', '月龄参照', '达成率'],
  'examples': [
    {'title': '18 月达成率', 'body': '18 月应独走、说单词、指认；达成率≥80% 为正常，<50% 明显落后。'},
    {'title': '明显落后', 'body': '单能区达成率<50%→明显落后，尽早早期干预。'}],
  'faqs': [
    {'q': '里程碑范围？', 'a': '按语/运/社交逐月龄列出，慢 2 个月以上需警惕。'},
    {'q': '早产校正？', 'a': '矫正月龄(减早产周数)评估至 2 岁。'}]},
'pediatrics/enuresis-age': {
  'title': '遗尿年龄评估',
  'scenarios': ['≥5 岁诊断', '单/非单症状', '自发缓解率'],
  'examples': [
    {'title': '7 岁频发', 'body': '7 岁、≥2 次/周→符合遗尿诊断；原发(自幼)单症状性，自发缓解约 90%。'},
    {'title': '继发性', 'body': '已戒后又发+日间症状→继发性，查 UTI/便秘/糖尿等原发病。'}],
  'faqs': [
    {'q': '几岁诊断？', 'a': '≥5 岁、每周≥2 次方可诊断遗尿，此前多为发育未成熟。'},
    {'q': '治疗？', 'a': '基础为遗尿闹钟+限晚水，药物(去氨加压素)备用，伴日间症状需综合治疗。'}]},
'pediatrics/growth-curve-zscore': {
  'title': '生长曲线 Z 评分',
  'scenarios': ['WHO 中位/SD', '身高体重头围', 'Z<-2 提示'],
  'examples': [
    {'title': '男 18 月 身高 76', 'body': 'WHO 中位 82.3、SD≈3.2：Z=(76−82.3)/3.2≈−2.0→生长迟缓临界，需追查营养。'},
    {'title': '正常', 'body': '身高 80、体重 11：Z≈−0.7/−0.3，均在 ±2 内生长发育良好。'}],
  'faqs': [
    {'q': 'Z 含义？', 'a': 'Z=(实测−中位)/SD；|Z|>2 为异常低/高。'},
    {'q': '头围？', 'a': '头围 Z 反映脑发育，过小查小头/过大查积水。'}]},
'pediatrics/hearing-screening': {
  'title': '听力筛查 OAE/AABR',
  'scenarios': ['OAE 与 AABR', '双耳 pass/refer', '高危因素'],
  'examples': [
    {'title': 'OAE 双耳 pass', 'body': 'OAE 左右均 pass→通过，常规随访；有高危因素建议 AABR。'},
    {'title': 'refer', 'body': '任一耳 refer→复查，仍 refer 转诊断性 ABR 与耳鼻喉。'}],
  'faqs': [
    {'q': 'OAE vs AABR？', 'a': 'OAE 查耳蜗、AABR 查听神经脑干部；高危儿首选 AABR。'},
    {'q': '未通过慌吗？', 'a': '新生儿耳道胎脂可假 refer，42 天内复筛即可。'}]},
'pediatrics/hfmd-course': {
  'title': '手足口病病程',
  'scenarios': ['典型皮疹', '神经/心肺警示', '隔离天数'],
  'examples': [
    {'title': '3 岁第 2 天皮疹', 'body': '手足口+臀疹≥2 处、口腔疹→典型 HFMD，第 2 天出疹高峰，对症即可。'},
    {'title': '警示征', 'body': '持续高热、惊跳、肢体抖、呼吸心率快→警惕重症(脑炎/肺水肿)，立即就医。'}],
  'faqs': [
    {'q': '隔离多久？', 'a': '症状消失后约 1 周，通常发病 14 天内具传染性。'},
    {'q': '何须住院？', 'a': '出现神经或心肺症状属重症，需 ICU 监护。'}]},
'pediatrics/hirschberg-test': {
  'title': 'Hirschberg 眼位',
  'scenarios': ['角膜光反射偏位', '偏斜角度', '内/外斜'],
  'examples': [
    {'title': '偏移 2mm', 'body': '光反射偏位 2mm×15°/mm=30°；偏颞侧→内斜视、偏鼻侧→外斜视(中度)。'},
    {'title': '轻度', 'body': '偏移<1.5mm(<22.5°)→轻度，可观察或视光训练。'}],
  'faqs': [
    {'q': '15°/mm 来源？', 'a': '角膜直径约 11mm 对应 22.5°，每 mm 偏移≈15°偏斜的粗略估算。'},
    {'q': '确诊？', 'a': 'Hirschberg 为筛查，精确角度靠棱镜遮盖/同视机。'}]},
'pediatrics/mchat-autism': {
  'title': 'M-CHAT 自闭症筛查',
  'scenarios': ['20 题家长版', '关键项', '年龄适配'],
  'examples': [
    {'title': 'fail≤2 无关键', 'body': '20 题未通过≤2 项且关键项(眼神/指向等)全过→低危，常规随访。'},
    {'title': '关键项失败', 'body': '任一关键项失败或失败≥3→中高危，转 ADOS 诊断评估。'}],
  'faqs': [
    {'q': '关键项？', 'a': '含目光、指物、听名应答等，单条失败即提升风险。'},
    {'q': '筛查非诊断', 'a': 'M-CHAT 为筛查，阳性需专业诊断访谈确认。'}]},
'pediatrics/pediatric-anemia': {
  'title': '缺铁性贫血评估',
  'scenarios': ['Hb 与年龄阈值', '铁蛋白/MCV', '铁剂剂量'],
  'examples': [
    {'title': '1 岁 Hb 90 铁蛋白 8', 'body': '1 岁 Hb 阈值 110，90 为中度；铁蛋白<12、MCV<70→缺铁性，铁剂 4mg/kg×10kg=40mg/日。'},
    {'title': '重度', 'body': 'Hb<70 或心衰表现→考虑输血，稳定后铁剂+饮食干预。'}],
  'faqs': [
    {'q': '铁剂量？', 'a': '治疗 3–6mg/kg/d 元素铁，预防 1–2mg/kg/d；餐间维 C 助吸收。'},
    {'q': '为何查 MCV？', 'a': '小细胞低色素(低 MCV)支持缺铁，地贫则铁蛋白不低。'}]},
'pediatrics/pediatric-asthma': {
  'title': '儿童哮喘控制(C-ACT)',
  'scenarios': ['C-ACT 7 题', '儿童+家长', '控制分级'],
  'examples': [
    {'title': 'C-ACT 25 分', 'body': '满分 25→控制良好，维持当前阶梯，3 月复评。'},
    {'title': '部分控制', 'body': '19–22 分→部分控制，升阶梯并查吸入技术。'}],
  'faqs': [
    {'q': 'C-ACT 适用？', 'a': '4–11 岁，儿童自答+家长观察结合，更敏感。'},
    {'q': '分值意义？', 'a': '≥20 控制、13–19 部分、≤12 未控制，指导升降级。'}]},
'pediatrics/pediatric-fever': {
  'title': '儿童发热护理',
  'scenarios': ['腋/口/肛温校正', '危险征', '退热与补水'],
  'examples': [
    {'title': '腋温 38.5', 'body': '腋温 38.5°C 即发热(肛温校正 +0.5=39.0)；精神好可观察补水。'},
    {'title': '危险征', 'body': '月龄小、热>3–5 天、精神差、惊厥→及时就医，不盲目退热。'}],
  'faqs': [
    {'q': '不同部位差？', 'a': '肛/耳比腋高约 0.5°C、口高 0.3°C，统一换算再判发热。'},
    {'q': '何时用药？', 'a': '≥38.5°C 或明显不适用退热药，重点在饮水与观察精神。'}]},
'pediatrics/pediatric-fracture': {
  'title': '儿童骨折骨骺',
  'scenarios': ['Salter-Harris 型', '部位生长风险', '开放/血管'],
  'examples': [
    {'title': '股骨远端', 'body': '股骨远端骺板占下肢生长 70%，Salter IV 型几乎必致生长障碍，需解剖复位。'},
    {'title': '胫骨远端', 'body': '青少年三平面(Tillaux)骨折累及骺线，CT 评估关节面后固定。'}],
  'faqs': [
    {'q': '为何重骨骺？', 'a': '骺板关系日后身高与力线，损伤可致长短腿/内翻。'},
    {'q': '急症？', 'a': '开放、血管神经受损、明显移位需急诊处理。'}]},
'pediatrics/pediatric-pneumonia': {
  'title': '儿童肺炎严重度',
  'scenarios': ['呼吸急促阈值', 'SpO₂ 分级', '凹陷征'],
  'examples': [
    {'title': 'RR 50 SpO₂ 88', 'body': '2 月儿 RR≥60 为促、本例 50 超标且 SpO₂ 88<90→重症肺炎，住院吸氧。'},
    {'title': '轻度', 'body': '无气促、SpO₂≥95、进食可→社区口服抗生素随访。'}],
  'faqs': [
    {'q': 'RR 阈值？', 'a': '<2 月≥60、2–12 月≥50、1–5 岁≥40 次/分为呼吸急促。'},
    {'q': '重症标准？', 'a': 'SpO₂<90、胸陷、拒食、发绀、嗜睡任一项即重症。'}]},
'pediatrics/rater-27': {
  'title': '生长曲线 Z 评分',
  'scenarios': ['WHO 数据', '月龄插值', '百分位'],
  'examples': [
    {'title': '男 18 月 身高 76', 'body': '插值 WHO 中位 82.3、SD≈3.2：Z=(76−82.3)/3.2≈−2.0→生长迟缓临界，需营养评估。'},
    {'title': '正常区间', 'body': 'Z 在 −2~+2 为正常，<-2 生长迟缓、>2 超重/肥胖。'}],
  'faqs': [
    {'q': '与 growth-curve-zscore 关系？', 'a': '同属生长 Z 评分，本键为旧 slug，算法一致。'},
    {'q': '百分位换算？', 'a': 'Z 经误差函数转百分位，便于家长理解(如 Z−2≈2.3%)。'}]},
'pediatrics/seizure-classification': {
  'title': '惊厥分类(热性/无热)',
  'scenarios': ['发热与否', '持续/单次', '局灶/全面'],
  'examples': [
    {'title': '单纯热性惊厥', 'body': '发热+短暂(<15min)+全面+单次→单纯热性惊厥，低危，家长宣教。'},
    {'title': '复杂/无热', 'body': '>15min 或局灶或反复，或无热→警惕癫痫/脑炎，神经评估。'}],
  'faqs': [
    {'q': '热性惊厥线？', 'a': '6 月–5 岁发热伴惊厥，短期复发率约 30%，多良性。'},
    {'q': '何时查因？', 'a': '无热、复杂、<6 月或>5 岁、神经体征异常需详查。'}]},
'pediatrics/tester-6': {
  'title': '儿童哮喘控制测试',
  'scenarios': ['C-ACT 儿童+家长', '总分 27', '控制判定'],
  'examples': [
    {'title': '满分 27', 'body': '儿童(12 分)+家长(15 分)合计 27→控制良好，维持治疗。'},
    {'title': '部分控制', 'body': '合计<20→未控制，升阶梯并复查吸入技术。'}],
  'faqs': [
    {'q': '与 pediatric-asthma 区别？', 'a': '同属 C-ACT 控制测试，本键为旧 slug，算法一致。'},
    {'q': '合计满分？', 'a': '儿童 4+3+3+3=13? 实际儿童 12+家长 15=27 满分(各版题权重和)。'}]},
'pediatrics/vaccine-schedule': {
  'title': '疫苗接种程序',
  'scenarios': ['国家计划免疫', '按出生日期', '逾期提醒'],
  'examples': [
    {'title': '出生满 2 月', 'body': '当前月龄推算：乙肝(0/1/6)、脊灰(2/3/4)、百白破(3/4/5)等，满 2 月应种脊灰+百白破首剂。'},
    {'title': '逾期', 'body': '红色=逾期未种，按补种原则尽快完成，不影响后续间隔。'}],
  'faqs': [
    {'q': '程序依据？', 'a': '按国家免疫规划，以出生日期算月龄匹配剂次。'},
    {'q': '早产/低体重？', 'a': '按实际出生日期计，乙肝首剂体重<2kg 暂缓(母亲抗原阴性时)。'}]},
'pediatrics/vanderbilt-adhd': {
  'title': 'Vanderbilt 多动症',
  'scenarios': ['注意/多动', '行为/焦虑', '跨场景'],
  'examples': [
    {'title': '注意 9 题≥2 共 7', 'body': '注意缺陷维度≥6 项阳性(0–4 分制≥2)→注意缺陷型阳性，需教师版交叉。'},
    {'title': '共病', 'body': '行为≥3 或焦虑≥3→对立违抗/焦虑共病，综合干预。'}],
  'faqs': [
    {'q': '诊断门槛？', 'a': '注意或多动维度≥6 项阳性、跨场景(家长+教师)、≥6 岁方可疑 ADHD。'},
    {'q': '为何跨场景？', 'a': 'ADHD 需多场景表现，单场景阳性可能为情境性行为。'}]},
'pediatrics/assessor-13': {
  'title': '脱水评估(体征)',
  'scenarios': ['体征评分', '轻中重度', '补液量'],
  'examples': [
    {'title': '10kg 中度', 'body': '体征评分对应中度缺失约 6%：累计丢失=10×0.06=600 mL，静脉/口服补充。'},
    {'title': '重度', 'body': '嗜睡、肢冷、再充盈>3s→重度(约 10%)，紧急静脉扩容。'}],
  'faqs': [
    {'q': '与 dehydration-assessment？', 'a': '同属脱水评估，本工具按体征条目打分，算法一致。'},
    {'q': '金标准？', 'a': '体重前后变化最准，体征用于现场快速分度。'}]},
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
