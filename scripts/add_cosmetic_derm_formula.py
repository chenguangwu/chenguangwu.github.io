#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cosmetic-derm 分类公式框补充（收口批次 C）：为 13 个缺框的计算类工具注入真实公式框。

缺框页：area-12 / chemical-peel / concentration / formula-1 / length-spacing /
        mesotherapy / microneedle / ratio-composition-injection / rf-tightening /
        sebumeter / spf-pa-calculator / temp-time-4 / thread-lift
（其余 21 页或已有框、或为无数值输入的豁免页。）

用法：python3 scripts/add_cosmetic_derm_formula.py [--apply]
与 scripts/add_eco_formula.py 同构：在首个 markup 锚点前插入 formula-box。
锚点搜索严格排除 <script>/<style> 区间（防把框插进 JS 模板串，历史 P0 坑）。
所有公式逐条对照页面 calc() 实现撰写，不写套话。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "cosmetic-derm")

ANCHORS = [
    "tip-box", "tabs", "scale-row", "set-row", "tool-result", "input-row", "subject-row",
]

FORMULAS = {
    "area-12": (
        "严重程度按红斑面积占比分级；血管直径按 μm 分型",
        "面积占比分级：<5% 轻度（毛细血管扩张 I 级）、5–15% 中度（II 级）、"
        "15–30% 重度（III 级）、≥30% 极重度（IV 级）；占比上限截断至 100%。"
        "血管直径分型：<0.2 μm 细血管（毛细血管扩张）、<1 μm 中等血管（小静脉扩张）、"
        "≥1 μm 粗血管（静脉扩张）。用于面部毛细血管扩张（红血丝）程度评估与治疗决策参考。",
    ),
    "chemical-peel": (
        "游离酸比例 = 1 / (1 + 10^(pH − pKa))；"
        "渗透深度指数 = 游离酸浓度 × 时间 × (76/MW) × 敏感度 × 首次因子 / 100",
        "游离酸比例由酸型 pKa 与实测 pH 决定：pKa 取甘醇酸 3.83、乳酸 3.86、杏仁酸 3.41、"
        "水杨酸 2.97、TCA 0.26、Jessner 3.0；游离酸浓度 = 输入浓度 × 游离酸比例。"
        "分子量因子以甘醇酸（MW 76）为基准 1.0，其余按 76/MW 折算（乳酸 90、杏仁酸 152、"
        "水杨酸 138、TCA 163、Jessner 100），越小渗透越快。首次刷酸乘 0.7 折减。"
        "深度指数越大提示剥脱越深，用于选择酸型/浓度/pH 组合与恢复期预估。",
    ),
    "concentration": (
        "游离酸比例 = 10^(pH − pKa) / (1 + 10^(pH − pKa))；"
        "游离酸浓度 = 输入浓度 × 游离酸比例",
        "pKa 常数：AHA（甘醇酸）3.83、BHA（水杨酸）2.97、TCA 0.66。"
        "pH 越低游离酸比例越高、剥脱力越强；pH 提示：<2.0 刺激性大、<3.0 剥脱力强、"
        "<3.5 适中、≥3.5 温和。剥脱深度判定：AHA 按浓度与 pH 组合分极浅表（≤20% 且 pH≥3.5）"
        "／浅表／中度／深度；BHA 按 ≤10%／≤20%／>20% 分浅表／中度／深度；"
        "TCA 按 ≤15%／≤35%／>35% 分浅表／中度／深度。用于刷酸方案浓度与 pH 的量化评估。",
    ),
    "formula-1": (
        "折算配比 = 各成分配比 / 配比合计；体积 = 总量 × 折算配比；含量 = 体积 × 浓度",
        "当配比合计偏离 100%（±0.5% 容差）时按比例折算至 100% 并给出提示。"
        "成分含量：玻尿酸 = 体积 × 输入浓度（mg/ml）、维生素C = 体积 × 输入浓度（mg/ml）、"
        "肽类/辅酶按 2 mg/ml 估算。输出各成分体积、折算配比、浓度与含量及合计，"
        "用于水光/中胚层配方（如 HA+VC+肽）的配比折算与投料量核算。",
    ),
    "length-spacing": (
        "针密度 = 1 / (间距_cm)²（间距 μm ÷ 10000 转 cm）；"
        "实际穿透深度 = 针长 × 0.8；渗透面积占比 = 针密度 × π(d/2)² × 100%",
        "针长以 mm 计，实际穿透深度按皮肤弹性回缩取 0.8 折减。"
        "单点通道面积 = π × (直径 μm/10000 ÷ 2)² cm²。"
        "作用层次判定：<0.3 mm 角质层、<0.5 mm 表皮层、<1.0 mm 真皮乳头层、"
        "<1.5 mm 真皮网状层、≥1.5 mm 深层真皮/皮下。用于微针针长与间距组合的层次覆盖评估。",
    ),
    "mesotherapy": (
        "各成分体积 = 总量 × 成分比例；含量 = 体积 × 参考浓度；生理盐水补足余量",
        "配比逻辑：非交联透明质酸为基底（占 50%，若含 PRP 则降为 30%）；PRP 30%、"
        "维生素C 10%（10%）、肽类/生长因子 5%（0.5%）、微量肉毒素 2%（约 5 U/ml，全脸≤30 U）、"
        "PDRN 15%（上限 2 ml）、谷胱甘肽 3%（600 mg/4 ml）。"
        "生理盐水 = 总量 − 各成分体积和，用于补足总体积（>0.1 ml 时计入）。"
        "要求至少选择透明质酸或 PRP 作为基础成分。用于水光注射配方成分与用量核算。",
    ),
    "microneedle": (
        "微孔密度 = (1 / 间距_mm²) × 100 孔/cm²；单孔体积 = π r² h / 3（圆锥）；"
        "有效递送量 = 总孔体积 × 分子量因子 × 浓度 / 100",
        "有效深度 = 针长 × 0.75（皮肤回缩折减）；单孔半径 r = 直径 μm ÷ 2 ÷ 1000（mm）；"
        "总孔体积 = 密度 × 面积 × 单孔体积 × 遍数（mm³ ≈ μL）。"
        "分子量因子：<1 kDa 0.95、<10 kDa 0.85、<100 kDa 0.65、<500 kDa 0.45、否则 0.30。"
        "单次递送量 = 有效体积 × 浓度/100（1 μL 的 1% ≈ 10 μg）。"
        "用于药物/有效成分经皮微针递送的通量与剂量估算。",
    ),
    "ratio-composition-injection": (
        "折算配比 = 各成分配比 / 配比合计；体积 = 总量 × 折算配比；含量 = 体积 × 参考浓度",
        "配比合计偏离 100%（±0.5%）时按比例折算并提示。成分含量："
        "玻尿酸 = 体积 × 输入浓度（mg/ml）；维生素C、谷胱甘肽、其他/PRP 分别按参考浓度 "
        "50 / 30 / 5 mg/ml 折算。输出各成分折算配比、体积、含量及合计，"
        "并以条形图展示配比结构，用于复合注射（HA+VC+谷胱甘肽）配方核算。",
    ),
    "rf-tightening": (
        "有效温度区（42–50 ℃）效果 = (温度 − 42) × 时间 / 180；"
        "高温区（>50 ℃ 至安全上限）= 4 × 时间 / 180 × 1.2；效果上限 10",
        "安全温度上限：有冷却 52 ℃、无冷却 48 ℃；有效区间为 40–上限。"
        "低温区（40–42 ℃）= (温度 − 40) × 时间 / 360 × 0.5。"
        "频率对应穿透深度：1 MHz 3–5 mm、2 MHz 2–3 mm、3 MHz 1–2 mm、6 MHz 0.5–1 mm、"
        "双极多层交替（1–5 mm）。多次疗程按每次累积并递减计算累计效应。"
        "用于射频紧肤温度/时间参数的安全性与胶原刺激效果评估。",
    ),
    "sebumeter": (
        "T区 = (前额 + 鼻部) / 2；U区 = (颊部 + 下颌) / 2；"
        "温度校正均值 = 整体均值 × (1 − (温度 − 25) × 0.01)",
        "温度每升高 1 ℃ 皮脂分泌约增 10%，故按标准 25 ℃ 作反向校正。"
        "混合型判定：|T区 − U区| > 60 μg/cm² 即为混合型，并按 T/U 区分别定性。"
        "肤质分级：<70 干性、<120 中性、<180 偏油、≥180 油性。"
        "用于皮脂仪（Sebumeter）多部位读数换算与肤质判定。",
    ),
    "spf-pa-calculator": (
        "有效 MED = MED × 5 / UVI；理论保护时间 = 有效 MED × SPF；"
        "实际保护时间 = 理论 × 活动系数；所需 SPF = ⌈户外时间 / (有效 MED × 活动系数)⌉",
        "UVI 以 5 为基准校正（UVI 越高有效 MED 越短）。活动系数反映出汗/水洗对防晒的削弱。"
        "UVA 保护时间 = 有效 MED × PPD × 活动系数，PPD 按 PA 等级取 PA+ 3、PA++ 6、"
        "PA+++ 12、PA++++ 20。推荐 SPF：需 ≤15 为 SPF 15+、≤30 为 SPF 30+、"
        "≤50 为 SPF 50+，否则 SPF 50+（需物理遮盖 + 补涂）；推荐 PA：UVI ≤2 为 PA++、"
        "≤5 为 PA+++、>5 为 PA++++。用于户外防晒规格与补涂间隔评估。",
    ),
    "temp-time-4": (
        "胶原收缩率按真皮温度分段；收缩率 = min(分段值 × 时间因子, 55%)；"
        "时间因子 = min(1 + 0.3 × ln(时间), 1.8)",
        "收缩率分段：<45 ℃ 为 0；45–55 ℃ 为 (T − 45)/10 × 10；55–60 ℃ 为 10 + (T − 55)/5 × 10；"
        "60–70 ℃ 为 20 + (T − 60)/10 × 25；70–75 ℃ 为 45 + (T − 70)/5 × 5；≥75 ℃ 封顶 50%。"
        "效果分级：<45 无效、<55 轻微、<65 良好、<75 显著、≥75 风险区。"
        "用于射频/热作用胶原收缩与紧肤效果的量化估算。",
    ),
    "thread-lift": (
        "单线提拉力 = 锚定力 × 线材系数 × cos(进针角偏差) × cos(提拉角偏差)；"
        "总有效提拉力 = 单线力 × 数量 × 松弛度修正",
        "线材系数：平滑线 0、PDO 0.5、双向锯齿 0.6、PLA 0.7、PCLA 0.8、单向锯齿 0.85、"
        "360° 锯齿 1.0。角度偏差 = |输入角度 − 区域最佳角度|；"
        "区域最佳进针/提拉角：中面部 50/45°、下面部 40/35°、下颌线 55/50°、颈部 35/30°、眉部 20/15°。"
        "松弛度修正：轻度 1.2、中度 1.0、重度 0.7。效果分级：<100 轻度、<300 中度、"
        "<600 显著、≥600 强力提拉（g）。用于埋线提升方案提拉力与角度质量评估。",
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


def has_formula_box(s):
    """按 class 属性匹配（兼容 card formula-box 等复合类名），避免重复注入。"""
    return bool(re.search(r'class="[^"]*\bformula-box\b[^"]*"', s))


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
        if has_formula_box(s):
            skipped += 1
            continue
        pos = find_anchor(s)
        if pos < 0:
            print("  无锚点(跳过): %s" % slug)
            continue
        box = build_box(eq, desc)
        s2 = s[:pos] + box + s[pos:]
        # 自检：插入后公式框不得落在 script/style 内
        spans2 = script_or_style_spans(s2)
        i2 = s2.find('class="card formula-box"')
        assert i2 > 0 and not any(x <= i2 < y for x, y in spans2), "%s 插入位置异常" % slug
        if a.apply:
            open(fp, "w", encoding="utf-8").write(s2)
        done += 1
        print("  补框: %s" % slug)
    print("公式框：已补 %d / 缺框 0 / 跳过(已有) %d（共 %d）" % (done, skipped, total))


if __name__ == "__main__":
    main()
