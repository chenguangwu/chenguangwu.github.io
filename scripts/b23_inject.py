#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# B-OPT23 注入脚本：为 26 个"会算·无 formula-box·公式已核对一致"的 B 级工具，
# 在首个 <h2> 之后注入规范 formula-box（升 A）。
# 公式文本已逐个人工核对与 calc 逻辑一致（见 _b23_audit.txt）。
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

# path -> (eq, desc)  —— 公式文本均经人工核对与 calc 一致
FORMS = {
 "advertising/assessor-54.html": (
   "OTS（接触机会）= 日均流量 × 广告牌数 × 天数；Reach（到达率）= 注意到的人数 / 目标人群 × 100%；GRP（总收视点）= Reach × 平均频次",
   "OTS 为广告总曝光机会，Reach 为覆盖人群比例，GRP 为到达率与频次之积。"),
 "agriculture/calc-11.html": (
   "小时作业量（公顷/小时）= 幅宽(m) × 速度(km/h) × 效率系数 ÷ 10",
   "农机单位时间作业面积；效率系数反映转弯与地头损耗。"),
 "agriculture/calc-12.html": (
   "毛用水量（m³）= 面积(亩) × 666.67 × 深度(mm) ÷ 1000 ÷ 利用系数",
   "1 亩≈666.67 m²，深度按 mm 计；利用系数=有效水量/毛用水量。"),
 "agriculture/calc-13.html": (
   "小时油耗（L/h）= 功率(kW) × 负荷系数 × 比油耗(g/kWh) ÷ 1000 ÷ 密度(kg/L)",
   "负荷系数取小数（百分比÷100）；比油耗为每 kWh 耗油克数。"),
 "agriculture/calc-37.html": (
   "DLI（每日光积分, mol/m²/日）= PAR × 光照时长(h) × 3.6 ÷ 1000",
   "PAR 单位 μmol/m²/s；3.6÷1000 为 μmol→mol 的小时积分换算。"),
 "agriculture/calc-5.html": (
   "所需通风量 Q = 太阳辐射得热 ÷（空气密度 × 比热容 × 允许温差）",
   "显热平衡简化式，ρ=1.2 kg/m³、c=1005 J/(kg·K)；得热=辐射×面积×透射率。"),
 "agriculture/calc-7.html": (
   "纯养分(kg) = 总灌水量(m³) × 目标浓度(mg/L) ÷ 1000；肥料商品(kg) = 纯养分 ÷（养分含量 ÷ 100）",
   "目标浓度按纯元素计；养分含量为肥料质量百分比。"),
 "agriculture/calc-8.html": (
   "石灰用量(kg) =（目标 pH − 当前 pH）× 缓冲系数 × 面积",
   "适用于需调高 pH 的酸性土壤；缓冲系数随土质变化。"),
 "beekeeping/detector-13.html": (
   "蜂螨寄生率(%) = 检出螨数 ÷ 样本蜂数 × 100",
   "糖粉法检测，即每百只蜂寄生螨数；达阈值需防治。"),
 "clinical-nursing/iv-drip-rate.html": (
   "滴速(滴/分) = 总量(mL) × 滴系数(滴/mL) ÷ 总时间(分钟)；泵速(mL/h) = 总量(mL) ÷ 总时间(h)",
   "滴系数常见 15/20 滴/mL；总分钟=小时×60+分钟。"),
 "clinical-nursing/oxygen-concentration.html": (
   "鼻导管 FiO₂(%) ≈ 21 + 4 × 流量(L/min)（上限约 44%）",
   "经验估算式；普通面罩/储氧面罩另按分段换算，详见工具说明。"),
 "electronics/capacitance.html": (
   "当 C₁=C₂=C 时：C_L = C ÷ 2 + C_s，故 C = 2 × (C_L − C_s)",
   "两等值电容串联加杂散电容 C_s，求匹配标准容值 C。"),
 "food-processing/freeze-thaw-loss.html": (
   "解冻失水率(%) = (冷冻前重 − 解冻后重) ÷ 冷冻前重 × 100%",
   "基础汁液流失率；多次冻融按循环累积（见结果表）。"),
 "food-testing/protein-kjeldahl.html": (
   "氮含量(%) = |V₁−V₀| × c × 0.014 / m × 100；蛋白质(%) = 氮含量 × F",
   "V 为滴定体积(mL)、c 为酸浓度(mol/L)、m 为样品质量(g)；F 为氮→蛋白换算系数（小麦 5.70、玉米 6.25 等）。"),
 "leather/colorfast.html": (
   "累积辐照量(kJ/m²) = 照射时间(h) × 3600 × 辐照度(W/m²) ÷ 1000",
   "按累积能量对照蓝标 1–8 级评估耐光色牢度。"),
 "optical/blue-light-filter.html": (
   "透射比模型 T(λ) = 1 / [1 + e^(k×(λc−λ)/λc)]（λc 处 T≈50%）",
   "sigmoid 截止模型，k 为陡度、λc 为截止波长。"),
 "pulmonology/niv-settings.html": (
   "压力支持 PS = IPAP − EPAP",
   "无创通气压力参数关系；IPAP/EPAP 按病种滴定。"),
 "pulmonology/respiratory-failure.html": (
   "氧合指数 P/F = PaO₂ / FiO₂",
   "评价氧合障碍；<300 提示 ALI，<200（新标准<100）提示重度 ARDS。"),
 "reproductive-medicine/epididymal-aspiration.html": (
   "获取精子总量(×10⁶) = 浓度(×10⁶/mL) × 体积(mL)",
   "附睾穿刺/抽吸取精总量估算；可活动量另计 motility%。"),
 "reproductive-medicine/rater-30.html": (
   "MJS = Σ(各曲细精管评分) ÷ 曲细精管数量",
   "每管 1–10 分取均值，评估生精功能。"),
 "reproductive-medicine/sperm-concentration.html": (
   "浓度(×10⁶/mL) = (计数精子数 / 大方格数) × 稀释倍数 × 0.01",
   "改良 Neubauer 计数板公式（每大格体积 0.1 mm³ = 10⁻⁴ mL）。"),
 "reproductive-medicine/sperm-morphology.html": (
   "正常形态(%) = 正常形态数 / 计数总数 × 100",
   "WHO 严格形态标准，参考下限 4%。"),
 "reproductive-medicine/testicular-volume.html": (
   "体积(mL) = 长 × 宽 × 高 × 0.71 ÷ 1000（单位 mm）",
   "椭球近似（Lambert 公式），结果单位 mL。"),
 "rheumatology/essdai.html": (
   "ESSDAI = Σ(各脏器域活动度得分 × 域权重)（域活动度 0/1/2/高=权重值，共 12 域）",
   "原发性干燥综合征脏器受累活动度金标准评分，≥14 提示高活动度。"),
 "sales/stacked-discount.html": (
   "折扣券：当前价 → 当前价 ×(折扣÷100)；满减券：达门槛后 当前价 − 固定金额",
   "按从上到下依次应用；叠加不等于折扣率简单相加。"),
 "telecom/path-loss.html": (
   "FSPL(dB) = 20·log₁₀(d) + 20·log₁₀(f) + 32.44；Pr(dBm) = Pt + Gt + Gr − FSPL",
   "d、f 取 km、MHz；FSPL 为自由空间路径损耗，Pr 为接收功率。"),
}

def build_box(eq, desc):
    return (
        '<div class="formula-box">\n'
        '  <div class="formula-title">计算公式</div>\n'
        f'  <div class="formula-eq">{eq}</div>\n'
        f'  <p class="formula-desc">{desc}</p>\n'
        '</div>'
    )

def inject(path, dry=True):
    fp = os.path.join(TOOLS, path)
    if not os.path.exists(fp):
        return f"[缺失] {path}"
    h = open(fp, encoding="utf-8").read()
    if "formula-box" in h:
        return f"[已含formula-box·跳过] {path}"
    m = re.search(r'<h2[^>]*>.*?</h2>', h, re.S)
    if not m:
        return f"[无h2·跳过] {path}"
    if dry:
        snippet = m.group(0).replace("\n", " ")[:90]
        return f"[dry] {path}  (首个h2: {snippet})"
    box = build_box(*FORMS[path])
    end = m.end()
    new = h[:end] + "\n\n" + box + "\n" + h[end:]
    open(fp, "w", encoding="utf-8").write(new)
    return f"[已注入] {path}"

if __name__ == "__main__":
    dry = "--apply" not in sys.argv
    print(f"模式: {'DRY-RUN' if dry else 'APPLY'}，共 {len(FORMS)} 个\n")
    for p in sorted(FORMS):
        print(inject(p, dry=dry))
