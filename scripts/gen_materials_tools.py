# -*- coding: utf-8 -*-
"""Batch 20: 材料科学计算深化（14 个公式计算器）。industry=materials。"""
from tool_template import main

TOOLS = [
    {
        "slug": "hooke-strain", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "胡克定律应变", "h1": "胡克定律应变计算器",
        "h2": "轴向应变（ε = σ / E）",
        "intro": "线弹性范围内，应变等于应力除以弹性模量。",
        "desc": "胡克定律应变计算器：ε = σ/E，输入应力与弹性模量。",
        "inputs": [
            {"id": "s", "label": "应力", "value": "200e6", "step": "1e6", "unit": "Pa"},
            {"id": "E", "label": "弹性模量", "value": "200e9", "step": "1e9", "unit": "Pa"},
        ],
        "calc": """
            const s = num('s'), E = num('E');
            const eps = s / E;
            ToolBox.setResult('result', dataGrid([
                [eps.toFixed(5), '应变 ε'],
                [(eps * 100).toFixed(3), 'ε (%)']
            ]));
        """,
        "notes": ["ε = σ/E（单向应力）。", "200 MPa、200 GPa 钢 → ε=0.001。"],
    },
    {
        "slug": "youngs-modulus", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "弹性模量", "h1": "弹性模量计算器",
        "h2": "杨氏模量（E = σ / ε）",
        "intro": "由应力与应变之比求弹性模量。",
        "desc": "弹性模量计算器：E = σ/ε，输入应力与应变。",
        "inputs": [
            {"id": "s", "label": "应力", "value": "200e6", "step": "1e6", "unit": "Pa"},
            {"id": "eps", "label": "应变", "value": "0.001", "step": "0.0001"},
        ],
        "calc": """
            const s = num('s'), eps = num('eps');
            const E = s / eps;
            ToolBox.setResult('result', dataGrid([
                [E.toExponential(3), '弹性模量 E (Pa)'],
                [(E / 1e9).toFixed(1), 'E (GPa)']
            ]));
        """,
        "notes": ["E = σ/ε。", "200 MPa / 0.001 = 200 GPa（钢）。"],
    },
    {
        "slug": "poisson-lateral", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "泊松比横向应变", "h1": "泊松比横向应变计算器",
        "h2": "横向应变（ε_lat = −ν·ε_long）",
        "intro": "纵向受拉时横向收缩，比例系数为泊松比。",
        "desc": "泊松比横向应变计算器：ε_lat = −ν·ε_long，输入泊松比与纵向应变。",
        "inputs": [
            {"id": "nu", "label": "泊松比 ν", "value": "0.3", "step": "0.01"},
            {"id": "el", "label": "纵向应变", "value": "0.001", "step": "0.0001"},
        ],
        "calc": """
            const nu = num('nu'), el = num('el');
            const elat = -nu * el;
            ToolBox.setResult('result', dataGrid([
                [elat.toFixed(6), '横向应变 ε_lat'],
                [(-elat / el).toFixed(3), '回算 ν']
            ]));
        """,
        "notes": ["ε_lat = −ν·ε_long。", "ν=0.3、纵向 0.001 → 横向 −0.0003。"],
    },
    {
        "slug": "shear-modulus", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "剪切模量", "h1": "剪切模量计算器",
        "h2": "剪切模量（G = E / (2(1+ν))）",
        "intro": "剪切模量与弹性模量、泊松比的关系。",
        "desc": "剪切模量计算器：G = E/(2(1+ν))，输入弹性模量与泊松比。",
        "inputs": [
            {"id": "E", "label": "弹性模量", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "nu", "label": "泊松比 ν", "value": "0.3", "step": "0.01"},
        ],
        "calc": """
            const E = num('E'), nu = num('nu');
            const G = E / (2 * (1 + nu));
            ToolBox.setResult('result', dataGrid([
                [G.toExponential(3), '剪切模量 G (Pa)'],
                [(G / 1e9).toFixed(2), 'G (GPa)']
            ]));
        """,
        "notes": ["G = E/(2(1+ν))。", "200 GPa、ν=0.3 → G≈76.9 GPa。"],
    },
    {
        "slug": "bulk-modulus", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "体积模量", "h1": "体积模量计算器",
        "h2": "体积模量（K = E / (3(1−2ν))）",
        "intro": "体积模量表征材料抗均匀压缩能力。",
        "desc": "体积模量计算器：K = E/(3(1−2ν))，输入弹性模量与泊松比。",
        "inputs": [
            {"id": "E", "label": "弹性模量", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "nu", "label": "泊松比 ν", "value": "0.3", "step": "0.01"},
        ],
        "calc": """
            const E = num('E'), nu = num('nu');
            const K = E / (3 * (1 - 2 * nu));
            ToolBox.setResult('result', dataGrid([
                [K.toExponential(3), '体积模量 K (Pa)'],
                [(K / 1e9).toFixed(2), 'K (GPa)']
            ]));
        """,
        "notes": ["K = E/(3(1−2ν))。", "200 GPa、ν=0.3 → K≈166.7 GPa。"],
    },
    {
        "slug": "density-basic", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "密度计算", "h1": "密度计算器",
        "h2": "密度（ρ = m / V）",
        "intro": "由质量与体积求密度。",
        "desc": "密度计算器：ρ = m/V，输入质量与体积。",
        "inputs": [
            {"id": "m", "label": "质量", "value": "7.85", "step": "0.01", "unit": "kg"},
            {"id": "V", "label": "体积", "value": "0.001", "step": "0.0001", "unit": "m³"},
        ],
        "calc": """
            const m = num('m'), V = num('V');
            const rho = m / V;
            ToolBox.setResult('result', dataGrid([
                [rho.toFixed(1), '密度 ρ (kg/m³)'],
                [(rho / 1000).toFixed(4), 'ρ (g/cm³)']
            ]));
        """,
        "notes": ["ρ = m/V。", "7.85 kg、0.001 m³ → 7850 kg/m³（钢）。"],
    },
    {
        "slug": "specific-weight", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "重度计算", "h1": "重度计算器",
        "h2": "重度（γ = ρ·g）",
        "intro": "单位体积的重量（重度）。",
        "desc": "重度计算器：γ = ρ·g，输入密度。",
        "inputs": [{"id": "rho", "label": "密度", "value": "7850", "step": "10", "unit": "kg/m³"}],
        "calc": """
            const rho = num('rho');
            const g = 9.81;
            const gamma = rho * g;
            ToolBox.setResult('result', dataGrid([
                [gamma.toFixed(1), '重度 γ (N/m³)'],
                [(gamma / 1000).toFixed(2), 'γ (kN/m³)']
            ]));
        """,
        "notes": ["γ = ρ·g。", "钢重度约 77 kN/m³。"],
    },
    {
        "slug": "mass-from-density", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "质量计算(密度)", "h1": "质量计算器（密度法）",
        "h2": "质量（m = ρ·V）",
        "intro": "由密度与体积求质量。",
        "desc": "质量计算器：m = ρ·V，输入密度与体积。",
        "inputs": [
            {"id": "rho", "label": "密度", "value": "7850", "step": "10", "unit": "kg/m³"},
            {"id": "V", "label": "体积", "value": "0.002", "step": "0.0001", "unit": "m³"},
        ],
        "calc": """
            const rho = num('rho'), V = num('V');
            const m = rho * V;
            ToolBox.setResult('result', dataGrid([
                [m.toFixed(3), '质量 m (kg)'],
                [(m * 1000).toFixed(1), 'm (g)']
            ]));
        """,
        "notes": ["m = ρ·V。", "7850 kg/m³、0.002 m³ → 15.7 kg。"],
    },
    {
        "slug": "modulus-resilience", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "回弹模量", "h1": "回弹模量计算器",
        "h2": "回弹能（U_r = σ_y² / (2E)）",
        "intro": "材料在弹性范围内单位体积吸收的能量。",
        "desc": "回弹模量计算器：U_r = σ_y²/(2E)，输入屈服强度与弹性模量。",
        "inputs": [
            {"id": "sy", "label": "屈服强度", "value": "250e6", "step": "1e6", "unit": "Pa"},
            {"id": "E", "label": "弹性模量", "value": "200e9", "step": "1e9", "unit": "Pa"},
        ],
        "calc": """
            const sy = num('sy'), E = num('E');
            const Ur = sy * sy / (2 * E);
            ToolBox.setResult('result', dataGrid([
                [Ur.toFixed(1), '回弹能 U_r (J/m³)'],
                [(Ur / 1000).toFixed(3), 'U_r (kJ/m³)']
            ]));
        """,
        "notes": ["U_r = σ_y²/(2E)。", "250 MPa、200 GPa → 约 156 kJ/m³。"],
    },
    {
        "slug": "tensile-force-area", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "拉伸载荷", "h1": "截面拉伸载荷计算器",
        "h2": "拉伸力（F = σ·A）",
        "intro": "给定应力与截面积求可承受的拉力。",
        "desc": "拉伸载荷计算器：F = σ·A，输入应力与截面积。",
        "inputs": [
            {"id": "s", "label": "应力", "value": "250e6", "step": "1e6", "unit": "Pa"},
            {"id": "A", "label": "截面积", "value": "1e-4", "step": "1e-5", "unit": "m²"},
        ],
        "calc": """
            const s = num('s'), A = num('A');
            const F = s * A;
            ToolBox.setResult('result', dataGrid([
                [(F).toFixed(1), '拉力 F (N)'],
                [(F / 1000).toFixed(2), 'F (kN)']
            ]));
        """,
        "notes": ["F = σ·A。", "250 MPa、100 mm² → 25 kN。"],
    },
    {
        "slug": "engineering-strain", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "工程应变", "h1": "工程应变计算器",
        "h2": "工程应变（ε = (L − L₀) / L₀）",
        "intro": "标距长度的相对变化。",
        "desc": "工程应变计算器：ε = (L−L₀)/L₀，输入变形后与原始长度。",
        "inputs": [
            {"id": "L", "label": "变形后长度", "value": "101", "step": "0.1", "unit": "mm"},
            {"id": "L0", "label": "原始长度", "value": "100", "step": "0.1", "unit": "mm"},
        ],
        "calc": """
            const L = num('L'), L0 = num('L0');
            const eps = (L - L0) / L0;
            ToolBox.setResult('result', dataGrid([
                [eps.toFixed(5), '工程应变 ε'],
                [(eps * 100).toFixed(3), '伸长率 (%)']
            ]));
        """,
        "notes": ["ε = (L−L₀)/L₀。", "101/100 → ε=0.01（1%）。"],
    },
    {
        "slug": "true-strain", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "真实应变", "h1": "真实应变计算器",
        "h2": "真实应变（ε_t = ln(L / L₀)）",
        "intro": "大变形下用自然对数定义的应变。",
        "desc": "真实应变计算器：ε_t = ln(L/L₀)，输入变形后与原始长度。",
        "inputs": [
            {"id": "L", "label": "变形后长度", "value": "101", "step": "0.1", "unit": "mm"},
            {"id": "L0", "label": "原始长度", "value": "100", "step": "0.1", "unit": "mm"},
        ],
        "calc": """
            const L = num('L'), L0 = num('L0');
            const et = Math.log(L / L0);
            ToolBox.setResult('result', dataGrid([
                [et.toFixed(6), '真实应变 ε_t'],
                [(et * 100).toFixed(4), 'ε_t (%)']
            ]));
        """,
        "notes": ["ε_t = ln(L/L₀)；101/100 → 0.00995。"],
    },
    {
        "slug": "vickers-hardness", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "维氏硬度", "h1": "维氏硬度计算器",
        "h2": "维氏硬度（HV = 1.854·F / d²）",
        "intro": "维氏硬度由压痕对角线长度与试验力求得（F 换算为 kgf）。",
        "desc": "维氏硬度计算器：HV = 1.854·(F/9.80665)/d²，F 用 N，d 用 mm。",
        "inputs": [
            {"id": "F", "label": "试验力", "value": "98.07", "step": "1", "unit": "N"},
            {"id": "d", "label": "压痕对角线", "value": "0.5", "step": "0.01", "unit": "mm"},
        ],
        "calc": """
            const F = num('F'), d = num('d');
            const HV = 1.854 * (F / 9.80665) / (d * d);
            ToolBox.setResult('result', dataGrid([
                [HV.toFixed(2), '维氏硬度 HV'],
                [(HV / 9.80665).toFixed(4), '对比 kgf 基准']
            ]));
        """,
        "notes": ["HV = 1.854·F_kgf/d²；F 以 kgf 计。", "10 kgf、d=0.5mm → HV≈74.2。"],
    },
    {
        "slug": "rule-of-mixtures", "industry": "materials", "cat": "materials", "icon": "🧪", "bg": "#fdf4ff",
        "title": "混合法则模量", "h1": "复合材料混合法则计算器",
        "h2": "纵向模量（E_c = V_f·E_f + V_m·E_m）",
        "intro": "纤维增强复合材料纵向弹性模量近似为体积加权。",
        "desc": "混合法则计算器：E_c = V_f·E_f + (1−V_f)·E_m，输入纤维体积分数与两者模量。",
        "inputs": [
            {"id": "Vf", "label": "纤维体积分数", "value": "0.5", "step": "0.01"},
            {"id": "Ef", "label": "纤维模量", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "Em", "label": "基体模量", "value": "3e9", "step": "1e8", "unit": "Pa"},
        ],
        "calc": """
            const Vf = num('Vf'), Ef = num('Ef'), Em = num('Em');
            const Ec = Vf * Ef + (1 - Vf) * Em;
            ToolBox.setResult('result', dataGrid([
                [(Ec / 1e9).toFixed(2), '复合模量 E_c (GPa)'],
                [(Ec).toExponential(3), 'E_c (Pa)']
            ]));
        """,
        "notes": ["E_c = V_f·E_f + V_m·E_m（V_m=1−V_f）。", "V_f=0.5、200/3 GPa → 101.5 GPa。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
