# -*- coding: utf-8 -*-
"""Batch 12: 化学/化工计算深化（14 个公式计算器）。industry=chemistry。"""
from tool_template import main

TOOLS = [
    {
        "slug": "mass-to-moles", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "质量转物质的量", "h1": "质量转物质的量计算器",
        "h2": "质量转物质的量（n = m / M）",
        "intro": "已知物质的质量与摩尔质量，求物质的量（摩尔数）。",
        "desc": "质量转物质的量计算器：n = m / M，输入质量与摩尔质量即得摩尔数。",
        "inputs": [
            {"id": "m", "label": "质量", "value": "18", "step": "0.01", "unit": "g"},
            {"id": "M", "label": "摩尔质量", "value": "18.015", "step": "0.001", "unit": "g/mol"},
        ],
        "calc": """
            const m = num('m'), M = num('M');
            const n = m / M;
            ToolBox.setResult('result', dataGrid([
                [n.toFixed(4), '物质的量 n (mol)'],
                [(M/m).toFixed(4), '摩尔质量倒数 (mol/g)']
            ]));
        """,
        "notes": ["n = m / M；m 为质量(g)，M 为摩尔质量(g/mol)。", "18 g 水(H₂O, M=18.015) 约等于 1 mol。"],
    },
    {
        "slug": "ideal-gas-volume", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "理想气体体积", "h1": "理想气体状态方程计算器",
        "h2": "理想气体体积（V = nRT / P）",
        "intro": "根据理想气体状态方程 PV = nRT 计算在给定压强、温度、物质的量下的气体体积。",
        "desc": "理想气体状态方程计算器：V = nRT/P，R=8.314 kPa·L/(mol·K)。",
        "inputs": [
            {"id": "n", "label": "物质的量", "value": "1", "step": "0.001", "unit": "mol"},
            {"id": "P", "label": "压强", "value": "101.325", "step": "0.001", "unit": "kPa"},
            {"id": "T", "label": "温度", "value": "273.15", "step": "0.01", "unit": "K"},
        ],
        "calc": """
            const n = num('n'), P = num('P'), T = num('T');
            const R = 8.314; // kPa·L/(mol·K)
            const V = n * R * T / P;
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(3), '体积 V (L)'],
                [(P * V / (n * R)).toFixed(2), '回算温度 T (K)']
            ]));
        """,
        "notes": ["V = nRT / P，R = 8.314 kPa·L/(mol·K)。", "标准状况(0℃,101.325kPa)下 1 mol 理想气体体积约 22.4 L。"],
    },
    {
        "slug": "solution-dilution", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "溶液稀释计算", "h1": "溶液稀释计算器",
        "h2": "溶液稀释（C₁V₁ = C₂V₂）",
        "intro": "稀释前后溶质量守恒：C₁V₁ = C₂V₂，求稀释后所需体积 V₂。",
        "desc": "溶液稀释计算器：C₁V₁=C₂V₂，输入原浓度/体积与目标浓度得稀释体积。",
        "inputs": [
            {"id": "C1", "label": "原浓度", "value": "10", "step": "0.1", "unit": "mol/L"},
            {"id": "V1", "label": "原体积", "value": "100", "step": "1", "unit": "mL"},
            {"id": "C2", "label": "目标浓度", "value": "2", "step": "0.1", "unit": "mol/L"},
        ],
        "calc": """
            const C1 = num('C1'), V1 = num('V1'), C2 = num('C2');
            const V2 = C1 * V1 / C2;
            ToolBox.setResult('result', dataGrid([
                [V2.toFixed(2), '稀释后体积 V₂ (mL)'],
                [(V2 - V1).toFixed(2), '需加溶剂量 (mL)']
            ]));
        """,
        "notes": ["C₁V₁ = C₂V₂，稀释前后溶质的量不变。", "10 mol/L、100 mL 稀释至 2 mol/L 需加至 500 mL。"],
    },
    {
        "slug": "mass-fraction", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "质量分数计算", "h1": "质量分数计算器",
        "h2": "质量分数（w = m_溶质 / m_总 × 100%）",
        "intro": "计算溶液中溶质的质量分数。",
        "desc": "质量分数计算器：w = m溶质 / m总 ×100%，输入溶质与总质量得质量分数。",
        "inputs": [
            {"id": "ms", "label": "溶质质量", "value": "20", "step": "0.1", "unit": "g"},
            {"id": "mt", "label": "溶液总质量", "value": "100", "step": "0.1", "unit": "g"},
        ],
        "calc": """
            const ms = num('ms'), mt = num('mt');
            const w = ms / mt * 100;
            ToolBox.setResult('result', dataGrid([
                [w.toFixed(2), '质量分数 w (%)'],
                [(mt - ms).toFixed(2), '溶剂质量 (g)']
            ]));
        """,
        "notes": ["w = m_溶质 / m_总 × 100%。", "20 g 溶质溶于 100 g 溶液，质量分数 20%。"],
    },
    {
        "slug": "molarity", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "摩尔浓度计算", "h1": "摩尔浓度计算器",
        "h2": "摩尔浓度（c = n / V）",
        "intro": "由物质的量与溶液体积计算物质的量浓度。",
        "desc": "摩尔浓度计算器：c = n/V，输入物质的量与体积得 mol/L。",
        "inputs": [
            {"id": "n", "label": "物质的量", "value": "2", "step": "0.01", "unit": "mol"},
            {"id": "V", "label": "溶液体积", "value": "1", "step": "0.01", "unit": "L"},
        ],
        "calc": """
            const n = num('n'), V = num('V');
            const c = n / V;
            ToolBox.setResult('result', dataGrid([
                [c.toFixed(4), '摩尔浓度 c (mol/L)'],
                [(c * 1000).toFixed(2), '毫摩尔浓度 (mmol/L)']
            ]));
        """,
        "notes": ["c = n / V；V 为溶液体积(L)。", "2 mol 溶于 1 L 得 2 mol/L。"],
    },
    {
        "slug": "normality", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "当量浓度计算", "h1": "当量浓度计算器",
        "h2": "当量浓度（N = n·z / V）",
        "intro": "当量浓度 = 物质的量 × 当量数 / 体积，常用于酸碱氧化还原滴定。",
        "desc": "当量浓度计算器：N = n·z / V，输入物质的量、当量数与体积。",
        "inputs": [
            {"id": "n", "label": "物质的量", "value": "1", "step": "0.01", "unit": "mol"},
            {"id": "z", "label": "当量数 z", "value": "2", "step": "1", "unit": "eq/mol"},
            {"id": "V", "label": "体积", "value": "1", "step": "0.01", "unit": "L"},
        ],
        "calc": """
            const n = num('n'), z = num('z'), V = num('V');
            const N = n * z / V;
            ToolBox.setResult('result', dataGrid([
                [N.toFixed(4), '当量浓度 N (eq/L)'],
                [(N).toFixed(4), '等价摩尔浓度 (mol/L × z)']
            ]));
        """,
        "notes": ["N = n·z / V；z 为每摩尔的当量数。", "1 mol H₂SO₄(z=2) 配 1 L 得 2 N。"],
    },
    {
        "slug": "ph-to-h", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "pH 与氢离子浓度", "h1": "pH 与氢离子浓度换算器",
        "h2": "pH 与 [H⁺]（[H⁺] = 10⁻ᴾᴴ）",
        "intro": "pH = -log₁₀[H⁺]，本工具由 pH 求氢离子浓度，反之亦然。",
        "desc": "pH 与氢离子浓度换算：输入 pH 得 [H⁺] = 10^(-pH)。",
        "inputs": [
            {"id": "pH", "label": "pH 值", "value": "7", "step": "0.01"},
        ],
        "calc": """
            const pH = num('pH');
            const H = Math.pow(10, -pH);
            ToolBox.setResult('result', dataGrid([
                [H.toExponential(3), '氢离子浓度 [H⁺] (mol/L)'],
                [(-Math.log10(H)).toFixed(3), '回算 pH']
            ]));
        """,
        "notes": ["[H⁺] = 10^(-pH)；pH = 7 时 [H⁺] = 1×10⁻⁷ mol/L。", "pH < 7 酸性，> 7 碱性。"],
    },
    {
        "slug": "reaction-yield", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "反应产率计算", "h1": "化学反应产率计算器",
        "h2": "反应产率（产率 = 实际 / 理论 × 100%）",
        "intro": "由实际产量与理论产量计算反应产率。",
        "desc": "反应产率计算器：产率 = 实际产量 / 理论产量 × 100%。",
        "inputs": [
            {"id": "act", "label": "实际产量", "value": "8", "step": "0.1", "unit": "g"},
            {"id": "theo", "label": "理论产量", "value": "10", "step": "0.1", "unit": "g"},
        ],
        "calc": """
            const act = num('act'), theo = num('theo');
            const y = act / theo * 100;
            ToolBox.setResult('result', dataGrid([
                [y.toFixed(2), '产率 (%)'],
                [(theo - act).toFixed(2), '损失量 (g)']
            ]));
        """,
        "notes": ["产率 = 实际产量 / 理论产量 × 100%。", "实际 8 g、理论 10 g 时产率 80%。"],
    },
    {
        "slug": "gas-density", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "气体密度计算", "h1": "气体密度计算器",
        "h2": "理想气体密度（ρ = PM / RT）",
        "intro": "由压强、摩尔质量与温度估算理想气体密度。",
        "desc": "气体密度计算器：ρ = PM/RT，输出 g/L。",
        "inputs": [
            {"id": "P", "label": "压强", "value": "101.325", "step": "0.001", "unit": "kPa"},
            {"id": "M", "label": "摩尔质量", "value": "28.97", "step": "0.001", "unit": "g/mol"},
            {"id": "T", "label": "温度", "value": "273.15", "step": "0.01", "unit": "K"},
        ],
        "calc": """
            const P = num('P'), M = num('M'), T = num('T');
            const R = 8.314;
            const rho = P * M / (R * T);
            ToolBox.setResult('result', dataGrid([
                [rho.toFixed(4), '气体密度 ρ (g/L)'],
                [(rho / 1000).toFixed(6), '密度 (kg/m³)']
            ]));
        """,
        "notes": ["ρ = PM / RT，R = 8.314；结果单位为 g/L。", "空气(28.97)在 STP 下约 1.29 g/L。"],
    },
    {
        "slug": "partial-pressure", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "道尔顿分压", "h1": "道尔顿分压定律计算器",
        "h2": "道尔顿分压（Pᵢ = xᵢ · P_总）",
        "intro": "混合气体中某组分的分压等于其摩尔分数乘以总压。",
        "desc": "道尔顿分压计算器：Pᵢ = xᵢ·P总，输入摩尔分数与总压。",
        "inputs": [
            {"id": "x", "label": "摩尔分数", "value": "0.2", "step": "0.01"},
            {"id": "Pt", "label": "总压", "value": "100", "step": "0.1", "unit": "kPa"},
        ],
        "calc": """
            const x = num('x'), Pt = num('Pt');
            const Pi = x * Pt;
            ToolBox.setResult('result', dataGrid([
                [Pi.toFixed(2), '分压 Pᵢ (kPa)'],
                [(Pt - Pi).toFixed(2), '其余组分分压 (kPa)']
            ]));
        """,
        "notes": ["Pᵢ = xᵢ · P_总；xᵢ 为组分摩尔分数。", "摩尔分数 0.2、总压 100 kPa 时分压 20 kPa。"],
    },
    {
        "slug": "molality", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "质量摩尔浓度", "h1": "质量摩尔浓度计算器",
        "h2": "质量摩尔浓度（b = n / m_溶剂）",
        "intro": "质量摩尔浓度 = 溶质物质的量 / 溶剂质量(kg)，不受温度影响。",
        "desc": "质量摩尔浓度计算器：b = n/m溶剂，输入物质的量与溶剂质量(kg)。",
        "inputs": [
            {"id": "n", "label": "物质的量", "value": "1", "step": "0.01", "unit": "mol"},
            {"id": "ms", "label": "溶剂质量", "value": "0.5", "step": "0.01", "unit": "kg"},
        ],
        "calc": """
            const n = num('n'), ms = num('ms');
            const b = n / ms;
            ToolBox.setResult('result', dataGrid([
                [b.toFixed(4), '质量摩尔浓度 b (mol/kg)'],
                [(b * 1000).toFixed(2), '毫摩尔每千克 (mmol/kg)']
            ]));
        """,
        "notes": ["b = n_溶质 / m_溶剂(kg)。", "1 mol 溶于 0.5 kg 溶剂得 2 mol/kg。"],
    },
    {
        "slug": "resistivity-from-r", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "电阻率计算", "h1": "电阻率计算器",
        "h2": "电阻率（ρ = R·A / L）",
        "intro": "由测得的电阻、截面积与长度计算材料电阻率（电导率倒数）。",
        "desc": "电阻率计算器：ρ = R·A/L，输出 Ω·m。",
        "inputs": [
            {"id": "R", "label": "电阻", "value": "10", "step": "0.1", "unit": "Ω"},
            {"id": "A", "label": "截面积", "value": "1", "step": "0.01", "unit": "mm²"},
            {"id": "L", "label": "长度", "value": "1", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const R = num('R'), A = num('A'), L = num('L');
            const rho = R * (A / 1e6) / L; // A mm² -> m²
            ToolBox.setResult('result', dataGrid([
                [rho.toExponential(3), '电阻率 ρ (Ω·m)'],
                [(1 / rho).toExponential(3), '电导率 κ (S/m)']
            ]));
        """,
        "notes": ["ρ = R·A / L；A 由 mm² 换算为 m²。", "铜电阻率约 1.7×10⁻⁸ Ω·m。"],
    },
    {
        "slug": "acid-base-titration", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "酸碱中和滴定", "h1": "酸碱中和滴定计算器",
        "h2": "中和所需碱体积（V_b = C_a·V_a·n_a / (C_b·n_b)）",
        "intro": "根据酸碱的当量关系计算达到中和所需的另一种溶液体积。",
        "desc": "酸碱中和滴定计算器：V_b = C_a·V_a·n_a/(C_b·n_b)。",
        "inputs": [
            {"id": "Ca", "label": "酸浓度", "value": "0.1", "step": "0.001", "unit": "mol/L"},
            {"id": "Va", "label": "酸体积", "value": "25", "step": "0.1", "unit": "mL"},
            {"id": "na", "label": "酸元数 n_a", "value": "1", "step": "1"},
            {"id": "Cb", "label": "碱浓度", "value": "0.1", "step": "0.001", "unit": "mol/L"},
            {"id": "nb", "label": "碱元数 n_b", "value": "1", "step": "1"},
        ],
        "calc": """
            const Ca = num('Ca'), Va = num('Va'), na = num('na'), Cb = num('Cb'), nb = num('nb');
            const Vb = Ca * Va * na / (Cb * nb);
            ToolBox.setResult('result', dataGrid([
                [Vb.toFixed(2), '所需碱体积 V_b (mL)'],
                [(Cb * Vb * nb / (Va * na)).toFixed(4), '回算酸浓度 (mol/L)']
            ]));
        """,
        "notes": ["V_b = C_a·V_a·n_a / (C_b·n_b)，n 为可电离 H⁺/OH⁻ 数。", "一元酸一元碱等浓度等体积中和。"],
    },
    {
        "slug": "boiling-point-elevation", "industry": "chemistry", "cat": "chemistry", "icon": "⚗️", "bg": "#ecfdf5",
        "title": "沸点升高计算", "h1": "沸点升高计算器",
        "h2": "沸点升高（ΔT_b = K_b · m · i）",
        "intro": "难挥发非电解质稀溶液的沸点升高与质量摩尔浓度成正比。",
        "desc": "沸点升高计算器：ΔT_b = K_b·m·i，输入沸点升高常数、质量摩尔浓度与范特霍夫因子。",
        "inputs": [
            {"id": "Kb", "label": "沸点升高常数", "value": "0.512", "step": "0.001", "unit": "°C·kg/mol"},
            {"id": "m", "label": "质量摩尔浓度", "value": "1", "step": "0.01", "unit": "mol/kg"},
            {"id": "i", "label": "范特霍夫因子", "value": "1", "step": "0.1"},
        ],
        "calc": """
            const Kb = num('Kb'), m = num('m'), i = num('i');
            const dT = Kb * m * i;
            ToolBox.setResult('result', dataGrid([
                [dT.toFixed(4), '沸点升高 ΔT_b (°C)'],
                [(100 + dT).toFixed(4), '溶液沸点 (°C, 以水为基准)']
            ]));
        """,
        "notes": ["ΔT_b = K_b·m·i；水的 K_b = 0.512 °C·kg/mol。", "1 mol/kg 非电解质使水沸点升高约 0.512°C。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
