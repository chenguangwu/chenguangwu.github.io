# -*- coding: utf-8 -*-
"""Batch 28: 流体力学计算深化（14 个公式计算器）。industry=fluid。"""
from tool_template import main

TOOLS = [
    {
        "slug": "reynolds-number", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "雷诺数", "h1": "雷诺数计算器",
        "h2": "Re = ρ·v·D / μ",
        "intro": "判断流动层流或湍流的无量纲数。",
        "desc": "雷诺数：Re = ρvD/μ，输入密度、速度、特征尺度、动力黏度。",
        "inputs": [
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
            {"id": "v", "label": "速度 v", "value": "1", "step": "0.1", "unit": "m/s"},
            {"id": "D", "label": "特征尺度 D", "value": "0.05", "step": "0.005", "unit": "m"},
            {"id": "mu", "label": "动力黏度 μ", "value": "0.001", "step": "0.0001", "unit": "Pa·s"},
        ],
        "calc": """
            const rho = num('rho'), v = num('v'), D = num('D'), mu = num('mu');
            const Re = rho * v * D / mu;
            ToolBox.setResult('result', dataGrid([
                [Re.toFixed(1), '雷诺数 Re'],
                [Re < 2300 ? '层流' : (Re > 4000 ? '湍流' : '过渡区'), '流态']
            ]));
        """,
        "notes": ["Re = ρvD/μ。", "Re<2300 层流，>4000 湍流。"],
    },
    {
        "slug": "bernoulli-pressure", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "伯努利方程", "h1": "伯努利压力计算器",
        "h2": "P₁ + ½ρv₁² = P₂ + ½ρv₂²",
        "intro": "理想流体沿流线速度与压力关系。",
        "desc": "伯努利：P₂ = P₁ + ½ρ(v₁²−v₂²)，输入两截面速度、密度、压力 1。",
        "inputs": [
            {"id": "p1", "label": "压力 P₁", "value": "101325", "step": "1000", "unit": "Pa"},
            {"id": "v1", "label": "速度 v₁", "value": "1", "step": "0.1", "unit": "m/s"},
            {"id": "v2", "label": "速度 v₂", "value": "3", "step": "0.1", "unit": "m/s"},
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
        ],
        "calc": """
            const p1 = num('p1'), v1 = num('v1'), v2 = num('v2'), rho = num('rho');
            const p2 = p1 + 0.5 * rho * (v1 * v1 - v2 * v2);
            ToolBox.setResult('result', dataGrid([
                [p2.toFixed(1), '压力 P₂ (Pa)'],
                [((p1 - p2) / 1000).toFixed(2), '压差 (kPa)']
            ]));
        """,
        "notes": ["P₂ = P₁ + ½ρ(v₁²−v₂²)。", "管细处流速大、压力低。"],
    },
    {
        "slug": "continuity-equation", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "连续性方程", "h1": "连续性方程计算器",
        "h2": "A₁·v₁ = A₂·v₂",
        "intro": "不可压缩流体质量守恒。",
        "desc": "连续性：v₂ = A₁v₁/A₂，输入两截面面积与速度 1。",
        "inputs": [
            {"id": "a1", "label": "面积 A₁", "value": "0.01", "step": "0.001", "unit": "m²"},
            {"id": "v1", "label": "速度 v₁", "value": "2", "step": "0.1", "unit": "m/s"},
            {"id": "a2", "label": "面积 A₂", "value": "0.005", "step": "0.0005", "unit": "m²"},
        ],
        "calc": """
            const a1 = num('a1'), v1 = num('v1'), a2 = num('a2');
            const v2 = a1 * v1 / a2;
            ToolBox.setResult('result', dataGrid([
                [v2.toFixed(3), '速度 v₂ (m/s)']
            ]));
        """,
        "notes": ["A₁v₁ = A₂v₂。", "截面减小则流速增大。"],
    },
    {
        "slug": "drag-force", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "阻力", "h1": "流体阻力计算器",
        "h2": "F_d = ½·ρ·v²·C_d·A",
        "intro": "物体在流体中运动所受阻力。",
        "desc": "阻力：F_d = ½ρv²C_dA，输入密度、速度、阻力系数、迎风面积。",
        "inputs": [
            {"id": "rho", "label": "密度 ρ", "value": "1.225", "step": "0.01", "unit": "kg/m³"},
            {"id": "v", "label": "速度 v", "value": "30", "step": "1", "unit": "m/s"},
            {"id": "cd", "label": "阻力系数 C_d", "value": "0.47", "step": "0.01"},
            {"id": "a", "label": "迎风面积 A", "value": "0.5", "step": "0.05", "unit": "m²"},
        ],
        "calc": """
            const rho = num('rho'), v = num('v'), cd = num('cd'), a = num('a');
            const F = 0.5 * rho * v * v * cd * a;
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(2), '阻力 F_d (N)']
            ]));
        """,
        "notes": ["F_d = ½ρv²C_dA。", "球体 C_d≈0.47。"],
    },
    {
        "slug": "buoyancy-force", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "浮力", "h1": "阿基米德浮力计算器",
        "h2": "F_b = ρ_f·g·V",
        "intro": "排开流体重量等于浮力。",
        "desc": "浮力：F_b = ρ_f·g·V，输入流体密度、体积、重力加速度。",
        "inputs": [
            {"id": "rho", "label": "流体密度 ρ_f", "value": "1000", "step": "10", "unit": "kg/m³"},
            {"id": "V", "label": "排开体积 V", "value": "0.05", "step": "0.005", "unit": "m³"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const rho = num('rho'), V = num('V'), g = num('g');
            ToolBox.setResult('result', dataGrid([
                [(rho * V * g).toFixed(2), '浮力 F_b (N)']
            ]));
        """,
        "notes": ["F_b = ρ_f g V。", "浮力等于排开液重。"],
    },
    {
        "slug": "hydrostatic-pressure", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "静水压力", "h1": "静水压力计算器",
        "h2": "P = ρ·g·h",
        "intro": "液体内部由深度产生的压强。",
        "desc": "静水压力：P = ρgh，输入密度、深度、重力加速度。",
        "inputs": [
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
            {"id": "h", "label": "深度 h", "value": "10", "step": "0.5", "unit": "m"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const rho = num('rho'), h = num('h'), g = num('g');
            ToolBox.setResult('result', dataGrid([
                [(rho * g * h).toFixed(1), '压强 P (Pa)'],
                [(rho * g * h / 1000).toFixed(2), 'P (kPa)']
            ]));
        """,
        "notes": ["P = ρgh。", "10 m 水柱 ≈ 98 kPa。"],
    },
    {
        "slug": "poiseuille-flow", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "泊肃叶流量", "h1": "泊肃叶流量计算器",
        "h2": "Q = π·ΔP·r⁴ / (8·μ·L)",
        "intro": "圆管层流体积流量。",
        "desc": "泊肃叶：Q = πΔP r⁴/(8μL)，输入压差、半径、黏度、管长。",
        "inputs": [
            {"id": "dp", "label": "压差 ΔP", "value": "1000", "step": "50", "unit": "Pa"},
            {"id": "r", "label": "管半径 r", "value": "0.01", "step": "0.001", "unit": "m"},
            {"id": "mu", "label": "黏度 μ", "value": "0.001", "step": "0.0001", "unit": "Pa·s"},
            {"id": "L", "label": "管长 L", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const dp = num('dp'), r = num('r'), mu = num('mu'), L = num('L');
            const Q = Math.PI * dp * Math.pow(r, 4) / (8 * mu * L);
            ToolBox.setResult('result', dataGrid([
                [Q.toExponential(3), '流量 Q (m³/s)'],
                [(Q * 1e6).toFixed(3), 'Q (mL/s)']
            ]));
        """,
        "notes": ["Q = πΔP r⁴/(8μL)。", "流量对半径极敏感（四次方）。"],
    },
    {
        "slug": "terminal-velocity", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "终端速度", "h1": "终端速度计算器",
        "h2": "v_t = √(2mg / (ρ·A·C_d))",
        "intro": "阻力与重力平衡时的匀速下落速度。",
        "desc": "终端速度：v_t = √(2mg/(ρAC_d))，输入质量、密度、面积、阻力系数。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "0.1", "step": "0.01", "unit": "kg"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
            {"id": "rho", "label": "流体密度 ρ", "value": "1.225", "step": "0.01", "unit": "kg/m³"},
            {"id": "a", "label": "迎风面积 A", "value": "0.05", "step": "0.005", "unit": "m²"},
            {"id": "cd", "label": "阻力系数 C_d", "value": "0.47", "step": "0.01"},
        ],
        "calc": """
            const m = num('m'), g = num('g'), rho = num('rho'), a = num('a'), cd = num('cd');
            const vt = Math.sqrt(2 * m * g / (rho * a * cd));
            ToolBox.setResult('result', dataGrid([
                [vt.toFixed(3), '终端速度 v_t (m/s)']
            ]));
        """,
        "notes": ["v_t = √(2mg/(ρAC_d))。", "雨滴约 9 m/s。"],
    },
    {
        "slug": "orifice-discharge", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "孔口出流", "h1": "孔口出流流量计算器",
        "h2": "Q = C_d·A·√(2·ΔP/ρ)",
        "intro": "薄壁孔口自由出流流量。",
        "desc": "孔口出流：Q = C_d A√(2ΔP/ρ)，输入流量系数、面积、压差、密度。",
        "inputs": [
            {"id": "cd", "label": "流量系数 C_d", "value": "0.62", "step": "0.01"},
            {"id": "a", "label": "孔口面积 A", "value": "0.001", "step": "0.0001", "unit": "m²"},
            {"id": "dp", "label": "压差 ΔP", "value": "5000", "step": "100", "unit": "Pa"},
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
        ],
        "calc": """
            const cd = num('cd'), a = num('a'), dp = num('dp'), rho = num('rho');
            const Q = cd * a * Math.sqrt(2 * dp / rho);
            ToolBox.setResult('result', dataGrid([
                [Q.toExponential(3), '流量 Q (m³/s)']
            ]));
        """,
        "notes": ["Q = C_d A√(2ΔP/ρ)。", "重力出流时 ΔP=ρgh。"],
    },
    {
        "slug": "manning-velocity", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "曼宁公式", "h1": "曼宁公式流速计算器",
        "h2": "v = (1/n)·R^(2/3)·S^(1/2)",
        "intro": "明渠均匀流平均速度。",
        "desc": "曼宁公式：v = (1/n)R^(2/3)S^(1/2)，输入糙率、水力半径、底坡。",
        "inputs": [
            {"id": "n", "label": "糙率 n", "value": "0.013", "step": "0.001"},
            {"id": "R", "label": "水力半径 R", "value": "0.5", "step": "0.05", "unit": "m"},
            {"id": "S", "label": "底坡 S", "value": "0.001", "step": "0.0001"},
        ],
        "calc": """
            const n = num('n'), R = num('R'), S = num('S');
            const v = (1 / n) * Math.pow(R, 2/3) * Math.sqrt(S);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(4), '流速 v (m/s)']
            ]));
        """,
        "notes": ["v = (1/n)R^(2/3)S^(1/2)。", "混凝土渠 n≈0.013。"],
    },
    {
        "slug": "capillary-rise", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "毛细上升高度", "h1": "毛细上升高度计算器",
        "h2": "h = 2γ·cosθ / (ρ·g·r)",
        "intro": "液体在细管中因表面张力上升。",
        "desc": "毛细上升：h = 2γcosθ/(ρgr)，输入表面张力、接触角、密度、管半径。",
        "inputs": [
            {"id": "gamma", "label": "表面张力 γ", "value": "0.0728", "step": "0.001", "unit": "N/m"},
            {"id": "th", "label": "接触角 θ", "value": "0", "step": "5", "unit": "°"},
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
            {"id": "r", "label": "管半径 r", "value": "0.0005", "step": "0.0001", "unit": "m"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const gamma = num('gamma'), th = num('th') * Math.PI / 180,
                  rho = num('rho'), r = num('r'), g = num('g');
            const h = 2 * gamma * Math.cos(th) / (rho * g * r);
            ToolBox.setResult('result', dataGrid([
                [(h * 1000).toFixed(2), '上升高度 h (mm)']
            ]));
        """,
        "notes": ["h = 2γcosθ/(ρgr)。", "水在细玻管中明显上升。"],
    },
    {
        "slug": "dynamic-pressure", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "动压", "h1": "动压计算器",
        "h2": "q = ½·ρ·v²",
        "intro": "流体单位体积动能。",
        "desc": "动压：q = ½ρv²，输入密度与速度。",
        "inputs": [
            {"id": "rho", "label": "密度 ρ", "value": "1.225", "step": "0.01", "unit": "kg/m³"},
            {"id": "v", "label": "速度 v", "value": "50", "step": "1", "unit": "m/s"},
        ],
        "calc": """
            const rho = num('rho'), v = num('v');
            ToolBox.setResult('result', dataGrid([
                [(0.5 * rho * v * v).toFixed(1), '动压 q (Pa)']
            ]));
        """,
        "notes": ["q = ½ρv²。", "皮托管测速基础。"],
    },
    {
        "slug": "volume-flow-rate", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "体积流量", "h1": "体积流量计算器",
        "h2": "Q = A·v",
        "intro": "截面积与流速之积。",
        "desc": "体积流量：Q = A·v，输入截面积与流速。",
        "inputs": [
            {"id": "a", "label": "截面积 A", "value": "0.2", "step": "0.01", "unit": "m²"},
            {"id": "v", "label": "流速 v", "value": "3", "step": "0.1", "unit": "m/s"},
        ],
        "calc": """
            const a = num('a'), v = num('v');
            const Q = a * v;
            ToolBox.setResult('result', dataGrid([
                [Q.toFixed(3), '流量 Q (m³/s)'],
                [(Q * 1000).toFixed(1), 'Q (L/s)']
            ]));
        """,
        "notes": ["Q = A·v。", "管道流量直接估算。"],
    },
    {
        "slug": "stokes-settling", "industry": "fluid", "cat": "fluid", "icon": "💧", "bg": "#eff6ff",
        "title": "斯托克斯沉降速度", "h1": "斯托克斯沉降速度计算器",
        "h2": "v = 2r²(ρ_p−ρ_f)g / (9μ)",
        "intro": "小颗粒在低雷诺数下的匀速沉降速度。",
        "desc": "斯托克斯沉降：v = 2r²(ρ_p−ρ_f)g/(9μ)，输入颗粒半径、密度差、黏度。",
        "inputs": [
            {"id": "r", "label": "颗粒半径 r", "value": "1e-4", "step": "1e-5", "unit": "m"},
            {"id": "rhop", "label": "颗粒密度 ρ_p", "value": "2500", "step": "50", "unit": "kg/m³"},
            {"id": "rhof", "label": "流体密度 ρ_f", "value": "1000", "step": "10", "unit": "kg/m³"},
            {"id": "mu", "label": "黏度 μ", "value": "0.001", "step": "0.0001", "unit": "Pa·s"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const r = num('r'), rhop = num('rhop'), rhof = num('rhof'),
                  mu = num('mu'), g = num('g');
            const v = 2 * r * r * (rhop - rhof) * g / (9 * mu);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(6), '沉降速度 v (m/s)']
            ]));
        """,
        "notes": ["v = 2r²(ρ_p−ρ_f)g/(9μ)。", "适用低雷诺数小球。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
