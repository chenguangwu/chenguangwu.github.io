#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fitness 分类公式框补充（收口批次 C）：为 19 个缺框的计算类工具注入真实公式框。

用法：python3 scripts/add_fitness_formula.py [--apply]
与 scripts/add_math_formula.py 同构：在首个锚点前插入 formula-box。
所有公式逐条对照页面 calc() 实现撰写，不写套话。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "fitness")

ANCHORS = [
    "tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row",
]

FORMULAS = {
    "angle-motion": (
        "关节力矩 τ = F × r × sinθ（F = m·g）；肌力需求 F<sub>肌</sub> = τ / r<sub>内</sub>；力学优势 = r<sub>内</sub> / r",
        "F 为负荷重力（m 为质量、g = 9.81 m/s²），r 为外力臂（cm 折算为 m），θ 为关节角度。"
        "力矩随角度正弦变化：θ = 90° 时力臂最大、力矩最大，θ 趋近 0° 或 180° 时力矩趋零。"
        "肌肉需在 5 cm 等效内力臂上产生 F 肌 = τ / 0.05 的力才能对抗该力矩，力学优势 r 内 / r 越小说明该角度越费力。",
    ),
    "assessor-64": (
        "综合评分 = 师资×0.25 + 课程内容×0.25 + 教学环境×0.20 + 学员效果×0.30",
        "师资力量 = 认证系数×0.6 + min(从业年限/10, 1)×4（上限 10）；课程内容 = 三项评分均值；"
        "教学环境 = 室温×0.3 + 湿度×0.2 + 班级人数×0.25 + 人均面积×0.25（达标记 10、不达标记 5–6）；"
        "学员效果 = (满意度×0.3 + 留存×0.3 + 续费×0.2 + 进度×0.2)/10。"
        "等级：≥8.5 卓越 S、≥7.5 优秀 A、≥6.0 良好 B、≥4.5 合格 C，其余不合格 D；单项 < 7 判「待提升」。",
    ),
    "bodyfat-caliper": (
        "体脂率 = 495 / D − 450（Siri）；D 为身体密度，按性别与测量点数取 Jackson-Pollock 回归式",
        "三点法（男）D = 1.10938 − 0.0008267Σ + 0.0000016Σ² − 0.0002574×年龄；"
        "三点法（女）D = 1.0994921 − 0.0009929Σ + 0.0000023Σ² − 0.0001392×年龄；"
        "七点法男 D = 1.112 − 0.00043499Σ + 0.00000055Σ² − 0.00028826×年龄、女 D = 1.097 − 0.00046971Σ + 0.00000056Σ² − 0.00012828×年龄；"
        "Σ 为各测量点皮褶厚度之和（mm）。测得身体密度后用 Siri 公式换算体脂率。",
    ),
    "calc": (
        "BMR = 10×体重 + 6.25×身高 − 5×年龄 + 性别常数；TDEE = BMR × 活动系数",
        "采用 Mifflin-St Jeor 公式：男性性别常数 +5、女性 −161（体重 kg、身高 cm、年龄岁）。"
        "TDEE（每日总能量消耗）= BMR × 活动系数（久坐 1.2 至高强度 1.9）。"
        "目标热量：减脂 = TDEE − 500 kcal/天，维持 = TDEE，增肌 = TDEE + 300 kcal/天。",
    ),
    "calc-3": (
        "男 体脂% = 86.010×log₁₀(腰围−颈围) − 70.041×log₁₀(身高) + 36.76；"
        "女 体脂% = 163.205×log₁₀(腰围+臀围−颈围) − 97.684×log₁₀(身高) − 78.387",
        "美国海军围度法（US Navy），单位 cm。男性仅需颈围与腰围，女性需增加臀围项。"
        "结果截断在 2%–60% 区间后，按性别分档给出「必需脂肪 / 健康 / 可接受 / 偏高 / 肥胖」评级。",
    ),
    "calculator-calc-13": (
        "体脂% = 495 / D − 450（Siri）；Σ₃ = s₁ + s₂ + s₃；"
        "男 D = 1.109380 − 0.0008267Σ + 0.0000016Σ² − 0.0002574×年龄；"
        "女 D = 1.0994921 − 0.0009929Σ + 0.0000023Σ² − 0.0001392×年龄",
        "Jackson-Pollock 三点皮褶法：男性取胸、腹、大腿，女性取三头肌、髂上、大腿（单位 mm）。"
        "先由 Σ 求身体密度 D，再用 Siri 公式换算体脂率；结合体重进一步给出脂肪重量与去脂体重。",
    ),
    "calculator-calc-metabolism": (
        "Mifflin-St Jeor：BMR = 10W + 6.25H − 5A + (男 +5 / 女 −161)；"
        "Harris-Benedict：男 88.362 + 13.397W + 4.799H − 5.677A，女 447.593 + 9.247W + 3.098H − 4.330A",
        "W 为体重（kg）、H 为身高（cm）、A 为年龄（岁）。两种经典公式给出的 BMR 取平均值作为推荐值，"
        "再乘活动系数（1.2 / 1.375 / 1.55 / 1.725）得到各活动水平下的每日所需热量。",
    ),
    "circuit-timer": (
        "单轮时长 = 训练时长 + 休息时长；训练总时长 = (训练时长 + 休息时长) × 轮数；"
        "含准备总时长 = 训练总时长 + 准备时长",
        "例如训练 40 秒、休息 20 秒、8 轮、准备 10 秒：单轮 60 秒，训练总时长 60×8 = 480 秒（8 分钟），"
        "含准备 490 秒。计时器按各段时长自动切换训练/休息并统计累计训练分钟数。",
    ),
    "estimate-2": (
        "消耗热量 kcal = MET × 3.5 × 体重(kg) / 200 × 时长(min)；kJ = kcal × 4.184；每分钟消耗 = kcal / 时长",
        "基于代谢当量（MET）法：MET = 1 约等于静息代谢（3.5 ml O₂/kg/min）。"
        "MET 越高强度越大（<3 低强度、<6 中等、<9 高强度，≥9 极高强度）。"
        "米饭当量按每碗约 230 kcal 折算，便于直观理解消耗量。",
    ),
    "jianzhinengliangquekoujisuan": (
        "每日热量缺口 = 目标减脂(kg) × 7700 / (周数 × 7)；每周减脂 = 目标 / 周数；"
        "减重速率% = 每周减脂 / 体重 × 100；饮食缺口 = 每日缺口 × 饮食比例，运动缺口 = 每日缺口 × (1 − 比例)",
        "按 1 kg 脂肪 ≈ 7700 kcal 的能量守恒推算：先由总能耗除以天数得每日缺口，"
        "再按设定比例拆分为饮食减少与运动消耗两部分，并依减重速率给出安全性与建议。",
    ),
    "load": (
        "非减载周 w_k = w_(k−1) × 1.025；每 4 周减载 w = w_(k−1) × 0.9；单周容量 = w × 组数 × 次数",
        "按每周 +2.5% 的渐进超负荷递增，每第 4 周安排减载周（重量降为原 90%）以促进恢复。"
        "训练总容量仅累计非减载周；总增益 = 末周重量 − 起始重量，增益% = 增益 / 起始重量 × 100。",
    ),
    "rater-time": (
        "推荐时长 = 60 s（压痛 0–2）/ 90 s（3–5）/ 120 s（6–7）/ 60 s（≥8）；"
        "判定：实际 < 0.6×推荐 偏短，0.6–1.5×推荐 适中，> 1.5×推荐 偏长",
        "按压痛 VAS 分档给出单次泡沫轴放松的推荐时长，再用实际时长与推荐区间的比值判定是否充分。"
        "压痛 ≥6 时提示减轻力度、优先处理痛点周边；≥8 时提示停止重压并视情况就医。",
    ),
    "ratio-19": (
        "平均围度 = (左 + 右) / 2；差异 = |左 − 右|；差异% = 差异 / 平均 × 100；"
        "对称分 = max(0, 100 − 差异%)；综合评分 = 各部位对称分均值",
        "对上臂、大腿、小腿左右围度逐项计算差异百分比并换算为对称分（差异越大分越低）。"
        "差异 > 5% 标记提示、> 10% 标记警示；综合评分 ≥98 优秀、≥95 良好、≥90 一般，其余需改善。",
    ),
    "reminder": (
        "完成率% = min(100, round(当日累计饮水量 / 每日目标 × 100))；剩余量 = 目标 − 累计",
        "当日目标水量可调（默认 2000 ml），每次记录饮水量后累加并计算完成进度，环形进度条按完成率着色，"
        "并按设定间隔（默认 60 分钟）提醒补水。全部记录保存在浏览器本地。",
    ),
    "resistance": (
        "阻抗指数 = 身高² / 阻抗 Z；总体水 TBW = 1.20 + 0.45×指数 + 0.18×体重；"
        "去脂体重 FFM = TBW / 0.732（上限 0.95×体重）；体脂% = (体重 − FFM) / 体重 × 100",
        "生物电阻抗分析法（BIA）：用身高平方与阻抗值算阻抗指数，再按回归式估算总体水，"
        "以去脂组织中约 73.2% 的含水率反推去脂体重（FFM），最终得到体脂率与脂肪重量。"
        "结果按性别分档评级，测量前应避免剧烈运动与大量饮水以减小误差。",
    ),
    "training-volume": (
        "单次训练容量 = Σ(重量 × 组数 × 次数)；估算 1RM ≈ 重量 × (1 + 次数 / 30)（Epley）",
        "按动作记录每次训练的组数与次数，单次容量为各组重量×次数之和，累加后绘制容量进度曲线。"
        "由当次重量与次数用 Epley 公式估算 1RM，用于纵向比较力量增长；容量上升且 1RM 提升说明训练有效。",
    ),
    "vo2max-12min": (
        "VO₂max = (跑动距离(m) − 504.9) / 44.73（Cooper 12 分钟跑）；平均配速 = 12 分钟 / 距离",
        "Cooper 12 分钟跑测试常用于场地与跑步机：记录 12 分钟内完成的最大距离，"
        "代入上式得到最大摄氧量（ml/kg/min）；另一模式由完成时间反推（VO₂max = 483 / 时间 + 3.5）。"
        "结果按性别与年龄分段给出耐力等级。",
    ),
    "weight-capacity-training": (
        "训练总容量 = 重量 × 组数 × 次数；估算 1RM ≈ 重量 × (1 + 次数 / 30)（Epley）；"
        "强度% = 当前重量 / 1RM × 100",
        "容量（tonnage）反映一次训练的总负荷；相对强度由当前重量与 1RM 的比值决定，"
        "据强度区间判定训练目标（力量 / 增肌 / 耐力）。热身递增组取 1RM 的 50% / 70% / 80% / 90% 作为参考重量。",
    ),
    "zuidasheyanglianggusuan": (
        "VO₂max = (距离(m) − 504.9) / 44.73；绝对摄氧量 = VO₂max × 体重 / 1000 (L/min)；"
        "平均速度 = 距离 / 12 (m/min)；等效距离 = VO₂max × 44.73 + 504.9",
        "由 Cooper 12 分钟跑距离估算最大摄氧量，再乘体重得每分钟绝对摄氧量（升）。"
        "等效距离用于换算「提升若干 ml/kg/min 需多跑的米数」，便于设定阶段目标；"
        "结果按性别与年龄评级，并给出相对优秀线（70 ml/kg/min）的百分比。",
    ),
}


def build_box(eq, desc):
    return (
        '<div class="card formula-box">\n'
        '  <h3>📐 计算公式</h3>\n'
        '  <div class="formula-eq">%s</div>\n'
        '  <p class="formula-desc">%s</p>\n'
        '</div>\n'
    ) % (eq, desc)


def script_or_style_spans(s):
    """<script>/<style> 区间：锚点搜索必须排除，否则会命中 JS 模板串里的 input-row/tip-box。"""
    spans = []
    for pat in (r'<script\b[\s\S]*?</script>', r'<style\b[\s\S]*?</style>'):
        spans += [(m.start(), m.end()) for m in re.finditer(pat, s, re.I)]
    return spans


def find_anchor(s):
    spans = script_or_style_spans(s)
    for a in ANCHORS:
        for m in re.finditer(
            r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), s):
            if any(x <= m.start() < y for x, y in spans):
                continue
            return m.start()
    return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    total = len(FORMULAS)
    done = skipped = 0
    for slug, (eq, desc) in FORMULAS.items():
        fp = os.path.join(TOOLS_DIR, slug + ".html")
        if not os.path.isfile(fp):
            print("  缺失: %s" % slug)
            continue
        s = open(fp, encoding="utf-8").read()
        if 'class="formula-box"' in s:
            skipped += 1
            continue
        pos = find_anchor(s)
        if pos < 0:
            print("  无锚点(跳过): %s" % slug)
            continue
        box = build_box(eq, desc)
        s2 = s[:pos] + box + s[pos:]
        if a.apply:
            open(fp, "w", encoding="utf-8").write(s2)
        done += 1
        print("  补框: %s" % slug)
    print("公式框：已补 %d / 缺框 0 / 跳过(已有) %d（共 %d）" % (done, skipped, total))


if __name__ == "__main__":
    main()
