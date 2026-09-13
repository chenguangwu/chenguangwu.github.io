#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""healthcare 分类 formula 补框（C 批次）。

用法: python3 scripts/add_healthcare_formula.py [--apply]

幂等：已存在 formula-eq 的页面跳过。公式文本来自各页 calc() 的真实实现。
插入位置：首个 </h2> 之后，与既有公式框结构一致。
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'healthcare')
APPLY = '--apply' in sys.argv

F = {
 'analysis-report-cost': '均值 x̄ = Σx ÷ n　　中位数 = 排序后中间值（偶数取中间两项均值）\n方差 σ² = Σ(x − x̄)² ÷ n　　标准差 σ = √σ²　　极差 = 最大值 − 最小值',
 'antipyretic-dose': '单次液量(mL) = 体重(kg) × 单位剂量(mg/kg) ÷ 混悬液浓度(mg/mL)\n每日最多次数 = ⌊体重 × 75 ÷ 浓度 ÷ 单次液量⌋（按每日最大 75 mg/kg 折算）',
 'apgar': 'Apgar 总分 = 肤色 + 心率 + 反射 + 肌张力 + 呼吸（每项 0–2 分，满分 10）\n判读：7–10 正常，4–6 轻度窒息，0–3 重度窒息',
 'bac-calculator': 'BAC(‰) = 体积(mL) × 酒精度(%) × 0.789 ÷ (分布系数 × 体重kg) − 0.015 × 经过小时\n分布系数：男 0.68，女 0.55；代谢消除按每小时 0.015 递减',
 'blood-pressure-grade': '脉压 = 收缩压 − 舒张压　　分级：≥180/120 为 5 级，≥140/90 为 4 级，≥130/80 为 3 级，≥120 为 2 级，其余 1 级',
 'bmi-2': 'Z 分数 ≈ (BMI − 基线 − 年龄 × 0.35) ÷ 2.2（基线：男 16.5，女 16.2）\n百分位 = Φ(Z) × 100，其中 Φ 为标准正态分布函数；Z < −2 偏瘦，Z > 2 超重',
 'bmi-calculator': 'BMI = 体重(kg) ÷ 身高(m)²\nDevine 理想体重 = (男 50 / 女 45.5) + 2.3 × (身高in − 60)；Robinson = (男 52 / 女 49) + (男 1.9 / 女 1.7) × (身高in − 60)',
 'bmr-calculator': 'Mifflin-St Jeor：男 BMR = 10W + 6.25H − 5A + 5；女 BMR = 10W + 6.25H − 5A − 161\nW 体重(kg)、H 身高(cm)、A 年龄(岁)，结果单位为 kcal/天',
 'body-fat-estimator': 'BMI = 体重(kg) ÷ 身高(m)²\n体脂率(%) = 1.2 × BMI + 0.23 × 年龄 − 10.8 × 性别系数(男 1 / 女 0) − 5.4',
 'bsa-calculator': 'Du Bois：BSA(m²) = 0.007184 × 体重(kg)^0.425 × 身高(cm)^0.725\n用于化疗剂量、烧伤补液与儿童给药的体表面积换算',
 'chads-vasc': 'CHA₂DS₂-VASc = 心衰 + 高血压 + 年龄 65–74 + 糖尿病 + 卒中/血栓 × 2 + 血管病 + 女性\n分层：0 分低危、1 分低中危、2 分中危、≥3 分高危（按年卒中风险）',
 'checker-manager': '总分 = 八项检查得分之和（每项 0–10，满分 80）\n达标率(%) = 总分 ÷ 80 × 100，并结合记录的温度与湿度给出综合评级',
 'due-date-calc': '当前孕周 = 已孕天数 ÷ 7　　距预产期(天) = 280 − 已孕天数\n孕天数 = 已孕天数 − 排卵日偏移；Naegele 规则总孕期按 280 天计',
 'egfr': 'CKD-EPI：eGFR = 141 × min(Scr/κ, 1)^α × max(Scr/κ, 1)^(−1.209) × 0.993^年龄 × 性别系数 × 种族系数\nκ：女 0.7、男 0.9；α：女 −0.329、男 −0.411；Scr 单位 μmol/L（本页按 88.4 换算为 mg/dL）',
 'egfr-calculator': 'MDRD 简化式：eGFR = 175 × 肌酐^(−1.154) × 年龄^(−0.203) × 性别系数（女 0.742）\n结果单位 mL/min/1.73m²，用于慢性肾病分期参考',
 'fat-loss-deficit': '总热量缺口(kcal) = 目标减重(kg) × 7700\n每日缺口 = 总缺口 ÷ 计划天数；目标体重 = 当前体重 + 减重量（每公斤脂肪约合 7700 kcal）',
 'gfr-cockcroft': 'Cockcroft-Gault：CrCl(mL/min) = (140 − 年龄) × 体重(kg) ÷ (肌酐 μmol/L ÷ 88.4) × 性别系数（女 0.85）\n按体表面积校正值 = CrCl × 1.73 ÷ BSA（BSA 用 Du Bois 公式按身高 170 cm 估算）',
 'healthcare': '按体重：儿童剂量 = 成人剂量 × (儿童体重 ÷ 成人体重)\n上限校验：实际剂量 = min(按体重剂量, 成人剂量 × 最大系数)；给药比(%) = 儿童体重 ÷ 成人体重 × 100',
 'healthcare-2': '总滴数 = 输液体积(mL) × 滴系数(滴/mL)\n滴速(滴/分) = 总滴数 ÷ 输注时间(分)　　每滴间隔(s) = 60 ÷ 滴速',
 'healthcare-3': '预期升幅(mmol/L) = (输注液钠浓度 − 当前血钠) ÷ (总体水 + 1)\n需提升幅度 = 目标血钠 − 当前血钠；24 小时血钠纠正不超过 8–10 mmol/L',
 'healthcare-4': 'NYHA 分级：静息有症状为 Ⅳ 级；无呼吸困难为 Ⅰ 级；活动明显受限为 Ⅲ 级；轻度受限为 Ⅱ 级\n对应描述：Ⅰ 无症状、Ⅱ 轻度受限、Ⅲ 明显受限、Ⅳ 静息症状',
 'healthcare-5': '维持需求(g) = 体重(kg) × 0.8 × 活动系数\n目标需求(g) = 维持需求 × 目标系数（增肌/减脂/康复按目标取值）；餐次分配 = 目标需求 ÷ 4',
 'heart-rate-zones': '最大心率 = 220 − 年龄　　心率储备 HRR = 最大心率 − 静息心率\n最大心率法区间 Z1–Z5 = 最大心率 × 50%/60%/70%/80%/90% 起；Karvonen 法区间 = 静息心率 + HRR × 系数',
 'ibw': 'Devine：IBW(kg) = (男 50 / 女 45.5) + 0.91 × (身高cm − 152.4)\n上限 = IBW × 1.1　　下限 = IBW × 0.9（给出理想体重可接受区间）',
 'ideal-weight': 'Devine：理想体重(kg) = (男 50 / 女 45.5) + 2.3 × (身高in − 60)\n身高换算：1 in = 2.54 cm；结果与 Hamwi、Miller、Robinson 等公式并列比较',
 'map': 'MAP(mmHg) = 舒张压 + (收缩压 − 舒张压) ÷ 3\n脉压 = 收缩压 − 舒张压；判读：MAP ≥ 70 正常，≥ 65 临界，< 65 偏低',
 'morse': 'Morse 总分 = 跌倒史 + 次要诊断 + 助行器 + 静脉输液 + 步态 + 精神状态\n风险分级：≤ 24 分低风险，25–50 分中风险，> 50 分高风险',
 'nrs2002': '营养受损评分 = BMI 评分 + 体重丢失评分 + 摄入减少评分\n总分 = 营养受损评分 + 疾病严重程度评分 + 年龄 ≥ 70 加分；总分 ≥ 3 判为存在营养风险',
 'parkland': 'Parkland：24h 补液量(mL) = 4 × 体重(kg) × 烧伤面积(%TBSA)\n前 8 小时 = 总量 × 0.5（即 2 × 体重 × 面积）；后 16 小时 = 剩余 0.5；已输量 = 总量 × 已过小时 ÷ 24',
 'qtc': 'Bazett：QTc = QT ÷ √(60 ÷ HR)　　Fridericia：QTc = QT ÷ ³√(60 ÷ HR)\n延长阈值：男性 440 ms，女性 450 ms（所选公式法对应阈值）',
 'resp-rate': '判读：< 12 或 > 20 次/分 为异常（等级 3），12–20 次/分为正常（等级 1）\n偏离正常 = |呼吸频率 − 16|；运动上限参考：安静状态 20 次/分，活动状态 40 次/分',
 'tdee-calculator': 'BMR（Mifflin-St Jeor）= 10W + 6.25H − 5A + (男 +5 / 女 −161)\nTDEE = BMR × 活动系数；减脂目标 = TDEE − 500，增肌目标 = TDEE + 300；食物热效应 TEF = TDEE × 0.1',
 'water-intake': '推荐饮水量(mL) = 体重(kg) × 35 × 活动系数 × 气候系数\n杯数 = 推荐饮水量 ÷ 250（按每杯 250 mL 折算）',
 'weight-dosage': '日剂量(mg/天) = 体重(kg) × 单位剂量(mg/kg)\n单次剂量 = 日剂量 ÷ 每日给药次数',
 'wells': 'Wells 总分 = DVT 体征 + PE 可能性 + 心率 > 100 + 制动/手术 + DVT/PE 史 + 咯血 + 恶性肿瘤\n临床概率：≤ 1 分低度，2–6 分中度，> 6 分高度',
}


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def build_html(text):
    parts = [esc(p) for p in text.split('\n')]
    inner = ''.join('<div class="formula-line">%s</div>' % p for p in parts)
    return ('<div class="formula-box">\n'
            '<div class="formula-title">计算公式</div>\n'
            '<div class="formula-eq">%s</div>\n'
            '</div>\n' % inner)


n_skip = n_add = 0
missing = []
for slug in sorted(F):
    fp = os.path.join(TOOLS, slug + '.html')
    if not os.path.isfile(fp):
        missing.append(slug)
        continue
    s = open(fp, encoding='utf-8').read()
    if 'formula-eq' in s:
        n_skip += 1
        continue
    m = re.search(r'</h2>', s)
    if not m:
        missing.append(slug + '(no-h2)')
        continue
    s = s[:m.end()] + '\n' + build_html(F[slug]) + s[m.end():]
    if APPLY:
        open(fp, 'w', encoding='utf-8').write(s)
    n_add += 1

print('healthcare formula 补框：新增 %d，已存在跳过 %d，异常 %s'
      % (n_add, n_skip, missing if missing else '无'))
print(('已落盘（--apply）' if APPLY else 'DRY-RUN：未写文件'))
