#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 general 分类无 formula-box 的工具页补写规范的「📐 计算公式」块。

设计要点（与 fix_general_en_p.py 同构，可复用 / 幂等 / dry-run）：
- FORMULA_MAP: slug -> {"eq": 公式表达式(可空), "desc": 依据/计算逻辑说明}
- 在 <div class="tool-card-accent"> 容器内、第一个 <div class="input-row"> 之前插入 formula-box
- 若 eq 为空，则只写 formula-title + formula-desc（避免出现空公式框）
- 若页面已有 formula-box 则跳过（幂等）
- --dry-run 仅报告，不落盘；--apply 落盘

注意：formula-desc 写「计算依据 / 标准 / 方法」，formula-eq 写可确定的表达式；
无法写准具体系数时，eq 留空、desc 写定性依据，绝不臆造误导公式。
"""
import os
import re
import sys

TOOLS_DIR = "tools/general"
PLACEHOLDER = "is available directly in your browser"  # 仅用于排除占位（本批不处理占位）

# 键为 slug（不含 .html），值为 {"eq":..., "desc":...}
FORMULA_MAP = {
    # ---- 复用正文已有清晰公式（零风险）----
    "calc-flow": {
        "eq": "Q = q × N；药液量/亩 = 40 × Q ÷ (W × v)；效率 = W × v × 1.5",
        "desc": "总流量 Q 为单喷头流量 q 与喷头数 N 之积；按喷幅 W 与作业速度 v 折算每亩药液用量与作业效率（1 亩 ≈ 666.7 m²）。",
    },
    "calc-speed-capacity": {
        "eq": "Wh = mAh ÷ 1000 × V；t = Ah ÷ I；航程 = t × v",
        "desc": "由电池容量(mAh)与电压(V)得能量 Wh；续航 t 为容量(Ah)除以平均电流(A)；最大航程为续航乘飞行速度，实际需预留安全裕量。",
    },
    "color-temp-2": {
        "eq": "Φ = E × A ÷ 0.6 ÷ 0.8；N = Φ ÷ Φ₁（向上取整）",
        "desc": "所需总光通量 Φ 由推荐照度 E 与面积 A 并计利用系数 0.6、维护系数 0.8 得到；灯具数量 N 为总光通量除以单灯光通量 Φ₁（1 lux = 1 lm/m²）。",
    },
    "estimate-15": {
        "eq": "退税 = 金额 × 退税率；手续费 = 退税 × 费率；到手 = 退税 − 手续费",
        "desc": "按购物金额与退税率计算应退税额，扣除手续费后为实际到手；未达起退点不予退税，外币按给定汇率折算。",
    },
    "gongchengzaojiazhishujisuan": {
        "eq": "Iᵢ = P₁ᵢ/P₀ᵢ × 100；综合指数 = Σ(Iᵢ×wᵢ)/Σwᵢ",
        "desc": "单项指数 Iᵢ 为报告期价 P₁ᵢ 与基期价 P₀ᵢ 之比；综合造价指数按各费用项权重 wᵢ 加权，涨跌幅度 = 综合指数 − 100（%），权重建议合计 100%。",
    },
    "jienengfanganjisuan": {
        "eq": "W = P×t×d；ΔW = W×η/100；节费 = ΔW×c；碳减排 = ΔW×0.785；回收期 = I/节费",
        "desc": "年用电量 W 由功率 P、日均运行 t 与年运行天数 d 计算；按节能率 η 得年节电量 ΔW，乘以电价 c 得年节约电费，乘以 0.785 kgCO₂/kWh 得碳减排，回收期 = 改造投资 I / 年节约电费。",
    },
    "jiguanghanjieguangbanjisuan": {
        "eq": "d₀ = 4λf/(πD)；d = M²·d₀；z_R = πw₀²/λ；d_z = d·√(1+(z/z_R)²)；I = P/(π(d_z/2)²)",
        "desc": "衍射极限光斑 d₀ 由波长 λ、焦距 f 与入射光束直径 D 计算；实际焦点受光束质量 M² 放大；瑞利长度 z_R 描述离焦光斑 d_z 随离焦量 z 的演化；功率密度 I 为功率 P 除以光斑面积。",
    },
    "jiguangrongfuhoudujisuan": {
        "eq": "质量/长度 = 流量×效率/速度；A = 质量长度×1000/ρ；宽 ≈ 光斑+0.0003·P；高 = A/(0.74×宽)",
        "desc": "由粉末流量、扫描速度与送粉效率得单位长度沉积质量；截面积 A 由密度 ρ 换算；单道宽随功率 P 增大，单道高由截面积与宽推算，搭接步距 = 宽×(1−搭接率)。",
    },
    "lizishujianshejisuan": {
        "eq": "Y ≈ 0.0006·E·√Z / cosθ；Φ = J/e；刻蚀速率 = Y·Φ·M/(ρ·Nₐ)·1e7·60",
        "desc": "溅射产额 Y 随离子能量 E、靶材原子序数 Z 与入射角 θ 变化；离子通量 Φ 由电流密度 J 与元电荷 e 计算；刻蚀速率由产额、通量、摩尔质量 M、密度 ρ 与阿伏伽德罗常数 Nₐ 换算（nm/min）。",
    },
    # ---- 标准工程公式（高信心）----
    "calc-197": {
        "eq": "LMTD = (ΔT₁−ΔT₂) / ln(ΔT₁/ΔT₂)；A = Q / (K · LMTD)",
        "desc": "依据对数平均温差（LMTD）法，对逆流或顺流布置分别计算 LMTD，再按热流量 Q 与总传热系数 K 求所需换热面积 A。",
    },
    "calc-203": {
        "eq": "依据 ISO 286：上偏差 ES/ei、下偏差 EI/es 由基本尺寸与公差等级查表/计算",
        "desc": "依据 ISO 286 公差体系，按基本尺寸与配合代号（如 H7/g6）计算孔、轴上下偏差及配合间隙或过盈，给出极限尺寸。",
    },
    "calc-204": {
        "eq": "承载面积法：间距 s = √(容许荷载 / 侧压力)；根数 n = 理论布置数",
        "desc": "依据承载面积法，按模板尺寸、混凝土侧压力 q 与单根支撑容许荷载，计算理论支撑间距、实际布置根数与单根利用率。",
    },
    "calc-205": {
        "eq": "用钢量 = Σ(杆件长度 × 钢管线密度) + 扣件/连接件",
        "desc": "按搭设高度、长度、步距与立杆间距，依据标准钢管线密度逐项统计立杆、水平杆、剪刀撑等用钢量，输入校验后结果可复制。",
    },
    "calc-206": {
        "eq": "立杆稳定性 K = N / (φ·A·f)（按 JGJ130 轴压稳定）",
        "desc": "按施工荷载、风压、立杆间距与步距校核立杆稳定承载力；K 仅作快速校核，正式设计须按 JGJ130 验算并考虑初弯曲、节点松动等构造要求。",
    },
    "calc-strength-ratio": {
        "eq": "Bolomey：W/C = (α·f_c × γ_c)/(f_c + α·γ_c × γ_w)；体积比由 W/C 与砂率推导",
        "desc": "依据 Bolomey 公式，按强度等级、水泥标号与骨料类型计算水灰比，再据用水量、砂率求得每立方米混凝土的水泥、水、砂、石用量。",
    },
    "calc-196": {
        "eq": "圆管散热 q = 2πλ(Tw−Ta)/ln(Do/Di)；临界保温厚度 δ_c = λ/h",
        "desc": "依据圆管一维稳态导热计算散热热流，并校核临界保温厚度与表面温度须低于规范限值、散热可控后确定外包厚度。",
    },
    "flow-14": {
        "eq": "轴功率 P_s = ρ·g·Q·H / (η·1000)；配电机 P = P_s × K",
        "desc": "由流量 Q、扬程 H、介质密度 ρ 与泵效率 η 计算轴功率，乘以安全系数 K 并依据标准电机功率等级推荐匹配电机；按比转速推荐泵型。",
    },
    "flow-itinerary": {
        "eq": "推力 F = P × π·D²/4；拉力 F_t = P × π(D²−d²)/4",
        "desc": "按缸径 D、活塞杆径 d 与系统压力 P 计算无杆腔/有杆腔输出力，结合行程 S 与行程时间 t 选型，并据速比推荐杆型。",
    },
    "fabric-1": {
        "eq": "tex = 590.5 / Ne；面密度 = Σ(Tᵢ × nᵢ) / (1 − 织缩率) ÷ 100",
        "desc": "英制纱支 Ne 转国际标准线密度 tex：tex = 590.5/Ne；由经纬纱线密度、经纬密与织缩率、幅宽计算织物平方米克重。",
    },
    "gravity": {
        "eq": "重心 x = Σ(Wᵢ·xᵢ) / ΣWᵢ；力矩 Mᵢ = Wᵢ·xᵢ",
        "desc": "基于力矩平衡原理，输入相机机身、镜头、配重、附件等部件重量与距云台轴的力臂，计算合成重心位置与各部件力矩，并给出配平建议。",
    },
    "nianjieqiangdujisuan": {
        "eq": "τ = F / A；许用载荷 F = τ·A / n",
        "desc": "按粘结面积 A 与胶水剪切强度 τ 计算可承受载荷，除以安全系数 n（建议 2~4，动载荷取大值）得许用载荷；剪切强度为胶水标准条件下典型值，实际受温度与老化影响。",
    },
    "power-7": {
        "eq": "I = P / (√3 · U · cosφ · Kd)",
        "desc": "由电器总功率 P、同时使用系数 Kd、功率因数 cosφ 与电压 U 计算计算电流，依据断路器标准规格与铜芯导线载流量表推荐匹配断路器与导线截面积。",
    },
    "power-voltage-1": {
        "eq": "S = P / cosφ；I = S / (√3 · U)",
        "desc": "由负载总功率 P 与功率因数 cosφ 计算视在功率 S，求计算电流 I，依据目标负载率推荐标准变压器容量并评估实际负载率是否合理。",
    },
    "power-voltage": {
        "eq": "P = F · v / η；推荐标准电机功率等级与极数",
        "desc": "由负载力 F、运动速度 v 与传动效率 η 计算所需功率，推荐标准电机功率等级、极数与电机系列型号。",
    },
    "gongyebengxuanxing": {
        "eq": "P_s = ρ·g·Q·H / (η·1000)；配电机 P = P_s × K",
        "desc": "由流量 Q、扬程 H、介质密度 ρ 与泵效率 η 计算轴功率，乘以安全系数并依据标准序列推荐泵型、材质与转速，用于工业泵选型。",
    },
    "gongyeshebeigonglvpipei": {
        "eq": "P = F · v / η；T = 9550 · P / n",
        "desc": "由负载力 F、运动速度 v 与传动效率 η 计算所需功率，从标准电机功率序列推荐电机规格，并估算额定扭矩 T 与电流，用于机械传动系统电机选型。",
    },
    "fengjixuanxingjisuan": {
        "eq": "风量 Q (m³/h)、全压 p (Pa) 定工况；选型匹配性能曲线",
        "desc": "依据所需风量 Q 与风压 p 选型，风量为标准工况值，实际需考虑温度与海拔修正；结果仅供参考，正式选型须参照风机性能曲线。",
    },
    "dianhuaxuedunhuakongzhi": {
        "eq": "依据 Pourbaix 图：电位 E 与 pH 判定免蚀/活化/钝化/过钝化",
        "desc": "由电位 E（vs SHE）、电流密度 i 与 pH 值，依据铁的 Pourbaix 图判断所处区间（免蚀/活化/钝化/过钝化）并估算腐蚀速率。",
    },
    "hardness-14": {
        "eq": "HRC→HV 查标准换算表（如 HRC30≈HV303）",
        "desc": "按硬度数值与制式（HRC/HV/HB 等）及加工类型推荐磨料硬度，HRC 与 HV 之间按标准换算表关键点查值。",
    },
    "fabric-3": {
        "eq": "依据 GB 色牢度 1~5 级（4 级为良好）等质量指标综合评估",
        "desc": "依据经纬纱支数、经纬密、缩水率与 GB 色牢度（1~5 级，4 级为良好，贴身与深色面料常要求 ≥4 级）等指标对面料质量进行综合评估。",
    },
    "bearing": {
        "eq": "轴承补油/换油周期依据 dn 值（d×n）与润滑方式估算",
        "desc": "依据速度因数 dn 值（内径 d × 转速 n）与润滑方式，估算轴承补油（补脂/换油）周期与整体更换周期。",
    },
    "naimoxingpinggujisuan": {
        "eq": "磨损系数 k ≈ a·μ²（摩擦越大磨损越剧烈的经验简化式）",
        "desc": "由材料硬度、摩擦系数、接触压力与滑动速度，依据磨损系数与摩擦系数关联的经验简化式综合评估耐磨性。",
    },
    "pidaizhangjinjisuan": {
        "eq": "张紧力依据传递功率、带速与包角；F = 2·P/(v·(1−1/e^μθ))",
        "desc": "依据皮带型号、中心距、小带轮转速、传动功率与小带轮节径，计算所需张紧力并为试车与张力调整提供数据依据。",
    },
    "power-16": {
        "eq": "依据传递功率 P、主动轮转速 n₁ 与传动比 i 选带型与带轮直径",
        "desc": "由传递功率 P、主动轮转速 n₁ 与传动比 i 选型，依据标准带轮直径系列计算带速、根数与中心距，并给出张紧与校验建议。",
    },
    "hanjiegongyicanshu": {
        "eq": "焊接电流/电压依据材料厚度与焊接方法（经验区间）",
        "desc": "依据材料厚度与焊接方法推荐焊接电流、电压、速度与热输入等工艺参数，给出工艺窗口与注意事项。",
    },
    "kongtiaolengfuhejisuan": {
        "eq": "冷负荷 ≈ 围护传热 + 人员显热 + 设备散热 + 新风负荷（经验估算法）",
        "desc": "按房间面积、层高、朝向、人数、设备与照明功率，采用经验估算法汇总围护传热、人员、设备与新风的冷负荷，用于空调选型参考。",
    },
    "power-focal": {
        "eq": "切割深度随功率 P 增大、随速度 v 增大而减小；fEff 以 100mm 为峰值",
        "desc": "依据激光功率、焦距、切割速度与材料类型估算切割深度；光斑随焦距增大而变大，以 100mm 为效率峰值（fEff=1），偏离按 0.2%/mm 衰减。",
    },
    "frequency-15": {
        "eq": "超声加工参数（频率 f、振幅 A、工具直径 D、静压力 F）按材料匹配",
        "desc": "依据频率 f、振幅 A、工具直径 D 与静压力 F 及工件材料推荐超声加工参数，给出工艺匹配建议。",
    },
    "jingmishebeixuanxing": {
        "eq": "依据定位精度、负载、行程、移动速度选直线导轨(HGR)与滚珠丝杠",
        "desc": "依据定位精度、负载、行程与移动速度等要求，推荐合适的直线导轨规格（HGR 系列）和滚珠丝杠参数（直径、导程、精度等级）。",
    },
    # ---- lifespan 系列（有清晰标准模型）----
    "lifespan-20": {
        "eq": "L₁₀ = (C/P)^p（ISO 281），并计精度因子与润滑因子",
        "desc": "基于 ISO 281 的 L10 额定寿命公式，结合精度等级因子（P0–P2）与润滑方式因子，计算精密轴承的疲劳寿命与精度保持期。",
    },
    "lifespan-23": {
        "eq": "氧化速率 ≈ 2^(ΔT/10)（Arrhenius 工程近似，每升 10℃ 翻倍）",
        "desc": "依据 Arrhenius 方程对油品氧化反应速率的工程近似（温度每升 10℃ 速率约翻倍），结合油品类型、工作温度与转速估算低油雾寿命。",
    },
    "lifespan-25": {
        "eq": "Coffin–Manson：Δε_p ∝ (2N_f)^c（本工具用等效 ΔT 简化替代）",
        "desc": "依据 Coffin–Manson 关系（以塑性应变幅值为自变量），本工具用等效温度幅值 ΔT 作简化替代，快速比较不同快冷方案的热疲劳寿命，仅供相对比较。",
    },
    "lifespan-6": {
        "eq": "剩余寿命 = (涂层厚度 − 已腐蚀量 − 安全裕量) / 腐蚀速率（ISO 12944）",
        "desc": "依据 ISO 12944 标准，输入涂层厚度、腐蚀速率、环境等级（C1–C5）与已使用年限，计算防腐涂层剩余寿命与健康度并给出维护建议。",
    },
    "lifespan-4": {
        "eq": "Goodman/S-N：σ_a' = σ_a / (1 − σ_m/σ_b)（或 Gerber 修正）",
        "desc": "依据疲劳 S–N 曲线与 Goodman（或 Gerber）平均应力修正，由应力幅 σa、平均应力 σm 与抗拉强度 σb、疲劳强度系数/指数估算材料疲劳寿命。",
    },
    "lifespan-corrosion": {
        "eq": "剩余寿命 = (初始壁厚 − 已用量 − 腐蚀裕量) / 腐蚀速率",
        "desc": "依据腐蚀速率、初始壁厚、腐蚀裕量与已使用年限，结合环境等级估算耐腐蚀剩余寿命，为检修与更换计划提供决策依据。",
    },
}


def build_box(eq, desc):
    lines = ['    <div class="formula-box">', '      <div class="formula-title">📐 计算公式</div>']
    if eq and eq.strip():
        lines.append('      <div class="formula-eq">%s</div>' % eq.strip())
    lines.append('      <p class="formula-desc">%s</p>' % desc.strip())
    lines.append('    </div>')
    return "\n".join(lines)


def process_file(slug, apply):
    path = os.path.join(TOOLS_DIR, slug + ".html")
    if not os.path.exists(path):
        return ("MISSING", path)
    s = open(path, encoding="utf-8").read()
    if "formula-box" in s:
        return ("SKIP_HAS_BOX", path)
    anchor = '<div class="input-row">'
    idx = s.find(anchor)
    if idx < 0:
        return ("NO_INPUT", path)
    box = build_box(FORMULA_MAP[slug]["eq"], FORMULA_MAP[slug]["desc"])
    new_s = s[:idx] + box + "\n" + s[idx:]
    if apply:
        open(path, "w", encoding="utf-8").write(new_s)
    return ("OK", path)


def main():
    mode = "--apply" if "--apply" in sys.argv else "--dry-run"
    apply = mode == "--apply"
    targets = list(FORMULA_MAP.keys())
    done, skip, err = 0, 0, 0
    for slug in targets:
        if slug not in FORMULA_MAP:
            continue
        status, path = process_file(slug, apply)
        if status == "OK":
            done += 1
            if apply:
                print("  [应用] %s" % slug)
        elif status == "SKIP_HAS_BOX":
            skip += 1
            print("  [跳过-已有box] %s" % slug)
        elif status == "MISSING":
            err += 1
            print("  [缺失文件] %s" % slug)
        elif status == "NO_INPUT":
            err += 1
            print("  [无input-row] %s" % slug)
    print("\n模式: %s | 处理 %d | 跳过 %d | 异常 %d | 字典条目 %d" % (mode, done, skip, err, len(targets)))


if __name__ == "__main__":
    main()
