# -*- coding: utf-8 -*-
"""Batch 14: 热力学计算深化（14 个公式计算器）。industry=thermodynamics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "ideal-gas-pressure", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "理想气体压强", "h1": "理想气体压强计算器",
        "h2": "理想气体压强（P = nRT / V）",
        "intro": "由理想气体状态方程求给定体积下的气体压强。",
        "desc": "理想气体压强计算器：P = nRT/V，R=8.314 kPa·L/(mol·K)。",
        "inputs": [
            {"id": "n", "label": "物质的量", "value": "1", "step": "0.001", "unit": "mol"},
            {"id": "T", "label": "温度", "value": "273.15", "step": "0.01", "unit": "K"},
            {"id": "V", "label": "体积", "value": "22.414", "step": "0.001", "unit": "L"},
        ],
        "calc": """
            const n = num('n'), T = num('T'), V = num('V');
            const R = 8.314;
            const P = n * R * T / V;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(3), '压强 P (kPa)'],
                [(P * 1000).toFixed(1), '压强 (Pa)']
            ]));
        """,
        "notes": ["P = nRT / V，R = 8.314 kPa·L/(mol·K)。", "1 mol 在 STP(22.414 L) 下约 101.3 kPa。"],
    },
    {
        "slug": "charles-law", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "查尔斯定律", "h1": "查尔斯定律计算器",
        "h2": "等压体积-温度（V₂ = V₁·T₂ / T₁）",
        "intro": "压强不变时，理想气体体积与热力学温度成正比。",
        "desc": "查尔斯定律计算器：V₂ = V₁·T₂/T₁，温度须用开尔文。",
        "inputs": [
            {"id": "V1", "label": "初体积", "value": "1", "step": "0.01", "unit": "L"},
            {"id": "T1", "label": "初温度", "value": "273.15", "step": "0.01", "unit": "K"},
            {"id": "T2", "label": "末温度", "value": "373.15", "step": "0.01", "unit": "K"},
        ],
        "calc": """
            const V1 = num('V1'), T1 = num('T1'), T2 = num('T2');
            const V2 = V1 * T2 / T1;
            ToolBox.setResult('result', dataGrid([
                [V2.toFixed(4), '末体积 V₂ (L)'],
                [((T2 / T1)).toFixed(4), '体积放大倍数']
            ]));
        """,
        "notes": ["V₁/T₁ = V₂/T₂，温度须为开尔文。", "0℃→100℃(等压)体积约增 36.6%。"],
    },
    {
        "slug": "gay-lussac-law", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "盖-吕萨克定律", "h1": "盖-吕萨克定律计算器",
        "h2": "等容压强-温度（P₂ = P₁·T₂ / T₁）",
        "intro": "体积不变时，理想气体压强与热力学温度成正比。",
        "desc": "盖-吕萨克定律计算器：P₂ = P₁·T₂/T₁，温度须用开尔文。",
        "inputs": [
            {"id": "P1", "label": "初压强", "value": "100", "step": "0.1", "unit": "kPa"},
            {"id": "T1", "label": "初温度", "value": "300", "step": "0.1", "unit": "K"},
            {"id": "T2", "label": "末温度", "value": "400", "step": "0.1", "unit": "K"},
        ],
        "calc": """
            const P1 = num('P1'), T1 = num('T1'), T2 = num('T2');
            const P2 = P1 * T2 / T1;
            ToolBox.setResult('result', dataGrid([
                [P2.toFixed(3), '末压强 P₂ (kPa)'],
                [((P2 / P1)).toFixed(4), '压强放大倍数']
            ]));
        """,
        "notes": ["P₁/T₁ = P₂/T₂，温度须为开尔文。", "300 K→400 K 压强升约 33.3%。"],
    },
    {
        "slug": "boyles-law", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "玻意耳定律", "h1": "玻意耳定律计算器",
        "h2": "等温压强-体积（P₁V₁ = P₂V₂）",
        "intro": "温度不变时，理想气体压强与体积成反比。",
        "desc": "玻意耳定律计算器：V₂ = P₁V₁/P₂，输入初末压强与初体积。",
        "inputs": [
            {"id": "P1", "label": "初压强", "value": "100", "step": "0.1", "unit": "kPa"},
            {"id": "V1", "label": "初体积", "value": "2", "step": "0.01", "unit": "L"},
            {"id": "P2", "label": "末压强", "value": "50", "step": "0.1", "unit": "kPa"},
        ],
        "calc": """
            const P1 = num('P1'), V1 = num('V1'), P2 = num('P2');
            const V2 = P1 * V1 / P2;
            ToolBox.setResult('result', dataGrid([
                [V2.toFixed(4), '末体积 V₂ (L)'],
                [((P1 / P2)).toFixed(4), '体积放大倍数']
            ]));
        """,
        "notes": ["P₁V₁ = P₂V₂（等温）。", "压强减半，体积加倍。"],
    },
    {
        "slug": "specific-heat-q", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "比热容热量", "h1": "比热容热量计算器",
        "h2": "显热（Q = m·c·ΔT）",
        "intro": "物体升温所需热量等于质量 × 比热容 × 温升。",
        "desc": "比热容热量计算器：Q = m·c·(T2−T1)，输出焦耳。",
        "inputs": [
            {"id": "m", "label": "质量", "value": "1", "step": "0.01", "unit": "kg"},
            {"id": "c", "label": "比热容", "value": "4186", "step": "1", "unit": "J/(kg·K)"},
            {"id": "T1", "label": "初温", "value": "20", "step": "0.1", "unit": "℃"},
            {"id": "T2", "label": "末温", "value": "30", "step": "0.1", "unit": "℃"},
        ],
        "calc": """
            const m = num('m'), c = num('c'), T1 = num('T1'), T2 = num('T2');
            const Q = m * c * (T2 - T1);
            ToolBox.setResult('result', dataGrid([
                [Q.toFixed(1), '热量 Q (J)'],
                [(Q / 1000).toFixed(3), '热量 (kJ)']
            ]));
        """,
        "notes": ["Q = m·c·ΔT；水的比热容约 4186 J/(kg·K)。", "1 kg 水升温 10℃ 需 41.86 kJ。"],
    },
    {
        "slug": "latent-heat", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "相变潜热", "h1": "相变潜热计算器",
        "h2": "潜热（Q = m·L）",
        "intro": "相变（熔化/汽化）过程吸收或释放的热量。",
        "desc": "相变潜热计算器：Q = m·L，输入质量与潜热。",
        "inputs": [
            {"id": "m", "label": "质量", "value": "1", "step": "0.01", "unit": "kg"},
            {"id": "L", "label": "潜热", "value": "334000", "step": "1000", "unit": "J/kg"},
        ],
        "calc": """
            const m = num('m'), L = num('L');
            const Q = m * L;
            ToolBox.setResult('result', dataGrid([
                [Q.toFixed(0), '相变热量 Q (J)'],
                [(Q / 1e6).toFixed(3), '热量 (MJ)']
            ]));
        """,
        "notes": ["Q = m·L；冰的熔解潜热 3.34×10⁵ J/kg。", "1 kg 冰融化需 334 kJ。"],
    },
    {
        "slug": "heat-conduction", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "傅里叶导热", "h1": "傅里叶导热计算器",
        "h2": "导热速率（q = k·A·ΔT / L）",
        "intro": "稳态一维导热热流与温差、截面积成正比，与厚度成反比。",
        "desc": "傅里叶导热计算器：q = k·A·ΔT/L，输出瓦特。",
        "inputs": [
            {"id": "k", "label": "导热系数", "value": "400", "step": "1", "unit": "W/(m·K)"},
            {"id": "A", "label": "截面积", "value": "0.01", "step": "0.001", "unit": "m²"},
            {"id": "dT", "label": "温差", "value": "100", "step": "1", "unit": "K"},
            {"id": "L", "label": "厚度", "value": "0.1", "step": "0.001", "unit": "m"},
        ],
        "calc": """
            const k = num('k'), A = num('A'), dT = num('dT'), L = num('L');
            const q = k * A * dT / L;
            ToolBox.setResult('result', dataGrid([
                [q.toFixed(1), '导热热流 q (W)'],
                [(q / A).toFixed(1), '热流密度 (W/m²)']
            ]));
        """,
        "notes": ["q = k·A·ΔT / L；铝导热系数约 400 W/(m·K)。", "示例热流 4000 W。"],
    },
    {
        "slug": "stefan-boltzmann", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "黑体辐射功率", "h1": "斯特藩-玻尔兹曼辐射计算器",
        "h2": "辐射功率（P = ε·σ·A·T⁴）",
        "intro": "黑体辐射总功率与绝对温度四次方成正比。",
        "desc": "黑体辐射计算器：P = ε·σ·A·T⁴，σ=5.67×10⁻⁸。",
        "inputs": [
            {"id": "eps", "label": "发射率", "value": "1", "step": "0.01"},
            {"id": "A", "label": "表面积", "value": "1", "step": "0.01", "unit": "m²"},
            {"id": "T", "label": "温度", "value": "300", "step": "1", "unit": "K"},
        ],
        "calc": """
            const eps = num('eps'), A = num('A'), T = num('T');
            const sigma = 5.67e-8;
            const P = eps * sigma * A * Math.pow(T, 4);
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2), '辐射功率 P (W)'],
                [(P / A).toFixed(2), '辐射出射度 (W/m²)']
            ]));
        """,
        "notes": ["P = ε·σ·A·T⁴，σ = 5.67×10⁻⁸ W/(m²·K⁴)。", "300 K 黑体约 459 W/m²。"],
    },
    {
        "slug": "carnot-efficiency", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "卡诺效率", "h1": "卡诺热机效率计算器",
        "h2": "卡诺效率（η = 1 − T_c / T_h）",
        "intro": "工作于两热源间的理想热机最大效率。",
        "desc": "卡诺效率计算器：η = 1 − Tc/Th，温度用开尔文。",
        "inputs": [
            {"id": "Tc", "label": "冷源温度", "value": "300", "step": "1", "unit": "K"},
            {"id": "Th", "label": "热源温度", "value": "600", "step": "1", "unit": "K"},
        ],
        "calc": """
            const Tc = num('Tc'), Th = num('Th');
            const eta = 1 - Tc / Th;
            ToolBox.setResult('result', dataGrid([
                [(eta * 100).toFixed(2), '卡诺效率 η (%)'],
                [(Tc / Th).toFixed(4), 'T_c/T_h']
            ]));
        """,
        "notes": ["η = 1 − T_c/T_h，温度须为开尔文。", "600 K/300 K 间理想效率 50%。"],
    },
    {
        "slug": "linear-expansion", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "线性热膨胀", "h1": "线性热膨胀计算器",
        "h2": "线膨胀（ΔL = α·L₀·ΔT）",
        "intro": "固体受热沿长度方向伸长，与线膨胀系数、原长和温升有关。",
        "desc": "线性热膨胀计算器：ΔL = α·L₀·ΔT，输入膨胀系数、原长与温升。",
        "inputs": [
            {"id": "alpha", "label": "线膨胀系数", "value": "1.2e-5", "step": "1e-6", "unit": "1/K"},
            {"id": "L0", "label": "原长", "value": "1000", "step": "1", "unit": "mm"},
            {"id": "dT", "label": "温升", "value": "50", "step": "1", "unit": "K"},
        ],
        "calc": """
            const alpha = num('alpha'), L0 = num('L0'), dT = num('dT');
            const dL = alpha * L0 * dT;
            ToolBox.setResult('result', dataGrid([
                [dL.toFixed(4), '伸长量 ΔL (mm)'],
                [((L0 + dL)).toFixed(3), '末长 (mm)']
            ]));
        """,
        "notes": ["ΔL = α·L₀·ΔT；钢 α≈1.2×10⁻⁵ /K。", "1 m 钢升温 50℃ 伸长约 0.6 mm。"],
    },
    {
        "slug": "isothermal-work", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "等温膨胀功", "h1": "等温膨胀功计算器",
        "h2": "等温膨胀功（W = nRT·ln(V₂/V₁)）",
        "intro": "理想气体等温可逆膨胀对外做功。",
        "desc": "等温膨胀功计算器：W = nRT·ln(V₂/V₁)，输出焦耳。",
        "inputs": [
            {"id": "n", "label": "物质的量", "value": "1", "step": "0.01", "unit": "mol"},
            {"id": "T", "label": "温度", "value": "300", "step": "1", "unit": "K"},
            {"id": "V1", "label": "初体积", "value": "1", "step": "0.01", "unit": "L"},
            {"id": "V2", "label": "末体积", "value": "2", "step": "0.01", "unit": "L"},
        ],
        "calc": """
            const n = num('n'), T = num('T'), V1 = num('V1'), V2 = num('V2');
            const R = 8.314;
            const W = n * R * T * Math.log(V2 / V1);
            ToolBox.setResult('result', dataGrid([
                [W.toFixed(1), '膨胀功 W (J)'],
                [(W / 1000).toFixed(3), '功 (kJ)']
            ]));
        """,
        "notes": ["W = nRT·ln(V₂/V₁)；体积加倍功 = nRT·ln2。", "示例约 1.73 kJ。"],
    },
    {
        "slug": "first-law", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "热力学第一定律", "h1": "热力学第一定律计算器",
        "h2": "内能变化（ΔU = Q − W）",
        "intro": "系统内能变化等于吸热量减去对外做功。",
        "desc": "热力学第一定律计算器：ΔU = Q − W，输入热量与功。",
        "inputs": [
            {"id": "Q", "label": "吸热量", "value": "1000", "step": "1", "unit": "J"},
            {"id": "W", "label": "对外做功", "value": "400", "step": "1", "unit": "J"},
        ],
        "calc": """
            const Q = num('Q'), W = num('W');
            const dU = Q - W;
            ToolBox.setResult('result', dataGrid([
                [dU.toFixed(1), '内能变化 ΔU (J)'],
                [((dU / Q) * 100).toFixed(2), '占吸热比 (%)']
            ]));
        """,
        "notes": ["ΔU = Q − W（系统吸热为正、对外做功为正）。", "吸热 1000 J、做功 400 J → ΔU=600 J。"],
    },
    {
        "slug": "entropy-change", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "熵变计算", "h1": "可逆熵变计算器",
        "h2": "熵变（ΔS = Q_rev / T）",
        "intro": "可逆相变或传热过程的熵变等于可逆热量除以温度。",
        "desc": "熵变计算器：ΔS = Q_rev/T，输入可逆热量与温度。",
        "inputs": [
            {"id": "Q", "label": "可逆热量", "value": "4186", "step": "1", "unit": "J"},
            {"id": "T", "label": "温度", "value": "373.15", "step": "0.01", "unit": "K"},
        ],
        "calc": """
            const Q = num('Q'), T = num('T');
            const dS = Q / T;
            ToolBox.setResult('result', dataGrid([
                [dS.toFixed(3), '熵变 ΔS (J/K)'],
                [(dS / Q).toFixed(6), '1/T (1/K)']
            ]));
        """,
        "notes": ["ΔS = Q_rev / T；水沸点 373.15 K 汽化熵约 11.2 J/K。"],
    },
    {
        "slug": "humid-air-enthalpy", "industry": "thermodynamics", "cat": "thermodynamics", "icon": "🌡️", "bg": "#fff7ed",
        "title": "湿空气焓", "h1": "湿空气焓计算器",
        "h2": "湿空气焓（h = 1.006t + w(2501 + 1.86t)）",
        "intro": "湿空气的比焓由干球温度与含湿量决定。",
        "desc": "湿空气焓计算器：h = 1.006t + w(2501+1.86t)，输出 kJ/kg 干空气。",
        "inputs": [
            {"id": "t", "label": "干球温度", "value": "25", "step": "0.1", "unit": "℃"},
            {"id": "w", "label": "含湿量", "value": "0.01", "step": "0.001", "unit": "kg/kg"},
        ],
        "calc": """
            const t = num('t'), w = num('w');
            const h = 1.006 * t + w * (2501 + 1.86 * t);
            ToolBox.setResult('result', dataGrid([
                [h.toFixed(3), '湿空气焓 h (kJ/kg)'],
                [(1.006 * t).toFixed(3), '干空气部分 (kJ/kg)']
            ]));
        """,
        "notes": ["h = 1.006t + w(2501 + 1.86t)，w 为含湿量 kg/kg 干空气。", "25℃、w=0.01 时约 50.6 kJ/kg。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
