#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""health 分类 formula 补框（C 批次）。

用法: python3 scripts/add_health_formula.py [--apply]

幂等：已存在 formula-eq 的页面跳过。公式文本来自各页 calc() 的真实实现。
插入位置：首个 </h2> 之后，与既有公式框（如 insulin-dose）结构一致。
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'health')
APPLY = '--apply' in sys.argv

# slug -> 公式（一行，若有第二行则用 \n 分隔展示为两段）
F = {
 'alcohol-units': '酒精量(g) = 酒精度(%ABV) × 体积(mL) × 0.789 ÷ 100 × 杯数\nBAC = 酒精量 ÷ (体重 × 性别分布系数 × 10) × 空腹系数 − 0.015 × 经过小时',
 'blood-pressure-classifier': '脉压 = 收缩压 − 舒张压　　MAP = 舒张压 + 脉压 ÷ 3\n分级：正常 <120/80，升高 120–129，1级 130–139/80–89，2级 ≥140/90（按 ACC/AHA 2017）',
 'blood-type-calculator': '子代 ABO 血型 = 父母基因型组合（A、B 为显性，O 为隐性）\nRh：(++ 或 +−) 子女 Rh 阳性；(−−) 子女 Rh 阴性',
 'body-surface-area': 'Mosteller：BSA(m²) = √(身高cm × 体重kg ÷ 3600)\nDu Bois：0.007184 × 体重^0.425 × 身高^0.725　　Haycock：0.024265 × 体重^0.5378 × 身高^0.3964',
 'breath-timer': '单周期(s) = 吸气 + 屏气 + 呼气 (+ 呼气后屏息)\n总时长 = 单周期 × 目标周期数（4-7-8 法：吸 4s、屏 7s、呼 8s）',
 'caffeine-limit': '安全上限(mg) = 体重(kg) × 人群系数(mg/kg)\n中等摄入 = 体重 × 3　高风险 = 体重 × 6　咖啡杯数 = 安全上限 ÷ 95',
 'calc-1': '基础量(ml) = 体重(kg) × 系数；运动补充 = ⌊运动分钟 ÷ 30⌋ × 250 ml\n总量 = 基础 + 运动补充 + 环境调整（炎热 +500 / 干燥 +300 / 寒冷 −200 ml）；杯数 = 总量 ÷ 250',
 'calc-2': '总分 = 睡眠时长 + 入睡潜伏期 + 夜间觉醒 + 睡眠深度 + 日间警觉 + 呼吸 六项评分之和\n时长 7–9h 记 20 分，6–7h 记 15 分，5–6h 记 8 分，<5h 记 0 分',
 'calc-3': '总时长(h) = 手机 + 电脑 + 电视 + 平板\n评级：≤ 推荐值「控制良好」，≤ 上限「略偏高」，> 上限「明显超标」（按人群分档）',
 'calorie-needs': 'Mifflin-St Jeor：男 BMR = 10W + 6.25H − 5A + 5；女 = 10W + 6.25H − 5A − 161\nKatch-McArdle（有体脂时）：370 + 21.6 × 瘦体重；TDEE = BMR × 活动系数；目标热量 = TDEE ± 周变化(kg) × 7700 ÷ 7',
 'child-bmi-calculator': 'BMI = 体重(kg) ÷ 身高(m)²\n按年龄、性别的 BMI 百分位与 Z 值分级（2–20 岁）：超重 ≥ P85，肥胖 ≥ P95',
 'child-height-predictor': '男孩靶身高(cm) = (父身高 + 母身高 + 13) ÷ 2\n女孩靶身高(cm) = (父身高 + 母身高 − 13) ÷ 2；预期范围 = 靶身高 ± 5 cm',
 'child-medication-dose': 'Clark 公式：剂量 = 体重(kg) × 成人剂量 ÷ 70\nYoung 公式：剂量 = 年龄 × 成人剂量 ÷ (年龄 + 12)；标准范围 = mg/kg 单位剂量 × 体重',
 'cholesterol-ratio': '总胆固醇/HDL = TC ÷ HDL　　LDL/HDL = LDL ÷ HDL　　TG/HDL = TG ÷ HDL\n非 HDL = TC − HDL；心血管风险随 TC/HDL 升高递增',
 'dumbbell-weight-calculator': '每侧配重(kg) = (目标总重量 − 杆重) ÷ 2\n按所选片规格从大到小贪心组合，余数无对应片时给出最接近方案',
 'gfr-calculator': 'MDRD：186 × 肌酐^(−1.154) × 年龄^(−0.203) × (女 0.742) × (非裔 1.212)\nCKD-EPI：142 × min(Scr/κ,1)^α × max(Scr/κ,1)^(−1.2) × 0.9938^年龄 × (女 1.012)；Cockcroft-Gault：(140−年龄) × 体重 × (女 0.85) ÷ (72 × 肌酐)',
 'milk-tea-calories': '总热量(kcal) = (茶底 + 奶类) + 糖热量 + 加料热量\n糖热量 ≈ 容量(mL) ÷ 100 × 糖度 × 10；加料按所选（珍珠 +80 / 椰果 +40 / 布丁 +60 / 奶盖 +70 / 红豆 +50）累加',
 'one-rep-max': 'Epley：1RM = W × (1 + R ÷ 30)　　Brzycki：W × 36 ÷ (37 − R)\nLombardi：W × R^0.10　　O\'Conner：W × (1 + R ÷ 40)　　Mayhew：W × 100 ÷ (52.2 + 41.9e^(−0.055R))',
 'ovulation-calculator': '排卵日 = 末次月经 + 周期天数 − 14\n易孕期 = 排卵日前 5 天 ~ 后 1 天；下次月经 = 末次月经 + 周期天数',
 'pace-calculator': '配速 = 总时间 ÷ 距离　　时间 = 配速 × 距离　　距离 = 时间 ÷ 配速\n速度(km/h) = 3600 ÷ 每公里秒数（英制按 1 英里 = 1.60934 km 换算）',
 'pregnancy-due-date': 'Naegele 规则：预产期 = 末次月经 + 280 天\n或 排卵日 + 266 天；B 超法按检查日孕周回推校正',
 'pregnancy-weight-gain': '孕前 BMI = 体重(kg) ÷ 身高(m)²\n按 IOM 2009：偏瘦 12.5–18 kg、正常 11.5–16 kg、超重 7–11.5 kg、肥胖 5–9 kg（并给孕中晚期周增重区间）',
 'premature-age-calculator': '早产天数 = (40 − 出生孕周) × 7 − 孕天；预产期 = 出生日 + 早产天数\n矫正月龄 = (今天 − 预产期天数) ÷ 30.44；矫正周龄 = 矫正天数 ÷ 7',
 'protein-needs': '需求量(g) = 体重(kg) × 活动系数（目标取下限：增肌 ≥1.6、减脂 ≥1.8、康复 ≥1.5、老年 ≥1.2）\n年龄 ≥ 65 岁再按老年下限取高值',
 'rehab-timer': '单组时长 = 动作时长(s)；总时长 = 组数 × 动作时长 + (组数 − 1) × 组间休息',
 'running-calories': '热量(kcal) = MET × 体重(kg) × 时间(h)\nMET 由配速查表得到；心率法按平均心率、静息心率与年龄另行估算',
 'safe-period-calculator': '排卵日 = 末次月经 + 周期天数 − 14\n易孕期 = 排卵日 −5 ~ +4；安全期 = 周期其余日期（日历法，仅适用于周期规律者）',
 'sleep-cycle-calculator': '入睡时刻 = 起床时刻 − (周期数 × 90 分钟 + 入睡耗时)\n以 90 分钟为一个完整睡眠周期，从起床时刻向前倒推 3–6 个周期',
 'smoking-cost-calculator': '日花费 = 每日支数 ÷ 每包支数 × 每包价格；年花费 = 日花费 × 365；总花费 = 年花费 × 年数\n总吸烟量 = 每日支数 × 365 × 年数；累计寿命损失 ≈ 总支数 × 11 分钟',
 'vo2-max-calculator': 'Cooper 12 分钟跑：VO₂max = (距离m − 504.9) ÷ 44.73\n1.5 英里走跑：3.5 + 483 ÷ 时间(分)；Bruce 方案按运动总时间代入分级方程',
 'waist-hip-ratio': 'WHR = 腰围 ÷ 臀围\n中心性肥胖切点：男性 ≥ 0.90，女性 ≥ 0.85',
 'water-intake-calculator': '基础量(ml) = 体重(kg) × 年龄分段系数（≤1岁 120、≤3岁 110、≤6岁 100、≤10岁 80、≤14岁 60；成年男 35、女 30）\n总量 = 基础 × 活动系数 × 天气系数 × 特殊情况系数',
}

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

n_skip = n_add = 0
for slug in sorted(F):
    fp = os.path.join(TOOLS, slug + '.html')
    if not os.path.isfile(fp):
        print('  !! 页面不存在:', slug)
        continue
    s = open(fp, encoding='utf-8').read()
    if re.search(r'<div class="formula-eq">', s):
        n_skip += 1
        continue
    m = re.search(r'</h2>', s)
    if not m:
        print('  !! 无 h2:', slug)
        continue
    lines = [esc(x) for x in F[slug].split('\n')]
    eq = '<br>'.join(lines)
    box = ('\n    <div class="formula-box">\n'
           '      <div class="formula-title">📐 计算公式</div>\n'
           '      <div class="formula-eq">%s</div>\n'
           '    </div>' % eq)
    s = s[:m.end()] + box + s[m.end():]
    if APPLY:
        open(fp, 'w', encoding='utf-8').write(s)
    n_add += 1

print('补框 %d 页，已有框跳过 %d 页' % (n_add, n_skip))
print('DRY-RUN，未写文件（加 --apply 落盘）' if not APPLY else '已落盘')
