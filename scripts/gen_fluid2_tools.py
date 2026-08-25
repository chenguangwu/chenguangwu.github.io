# -*- coding: utf-8 -*-
"""Batch 55: 流体力学深化 II（14 个公式计算器）。industry=fluid。"""
from tool_template import main

TOOLS = [
    {
        "slug": "hydraulic-diameter",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "circle",
        "bg": "from-sky-500 to-blue-600",
        "title": "水力直径计算器",
        "h1": "D_h = 4A / P",
        "h2": "由流通面积与湿周求水力直径",
        "intro": "输入流通面积 A 与湿周 P，求水力直径。", "desc": "水力直径：输入 A、P，输出 D_h(m)。",
        "inputs": [
            {"id": "A", "label": "面积 A", "value": "0.01", "step": "0.001", "unit": "m²"},
            {"id": "P", "label": "湿周 P", "value": "0.4", "step": "0.05", "unit": "m"},
        ],
        "calc": """
            const A=num('A'),P=num('P');
            const Dh=4*A/P;
            ToolBox.setResult('result', dataGrid([
                [Dh.toFixed(4),'水力直径 D_h (m)']
            ]));
        """,
        "notes": ["D_h = 4A/P；圆管 D_h=D。", "A=0.01,P=0.4 → 0.1 m。"],
    },
    {
        "slug": "pressure-drop-darcy",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "trending-down",
        "bg": "from-sky-500 to-blue-600",
        "title": "达西沿程压降计算器",
        "h1": "ΔP = f·(L/D)·(ρv²/2)",
        "h2": "由摩擦系数与流速求管道压降",
        "intro": "输入摩擦系数 f、管长 L、管径 D、密度 ρ、流速 v，求压降。", "desc": "达西沿程压降：输入 f、L、D、ρ、v，输出 ΔP(Pa)。",
        "inputs": [
            {"id": "f", "label": "摩擦系数 f", "value": "0.02", "step": "0.005", "unit": ""},
            {"id": "L", "label": "管长 L", "value": "10", "step": "0.5", "unit": "m"},
            {"id": "D", "label": "管径 D", "value": "0.1", "step": "0.01", "unit": "m"},
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
            {"id": "v", "label": "流速 v", "value": "2", "step": "0.1", "unit": "m/s"},
        ],
        "calc": """
            const f=num('f'),L=num('L'),D=num('D'),rho=num('rho'),v=num('v');
            const dP=f*(L/D)*(rho*v*v/2);
            ToolBox.setResult('result', dataGrid([
                [dP.toFixed(1),'压降 ΔP (Pa)']
            ]));
        """,
        "notes": ["达西-魏斯巴赫公式。", "示例 → 400 Pa。"],
    },
    {
        "slug": "froude-number",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "waves",
        "bg": "from-sky-500 to-blue-600",
        "title": "弗劳德数计算器",
        "h1": "Fr = v / √(gL)",
        "h2": "由流速与特征长度求弗劳德数",
        "intro": "输入流速 v、特征长度 L、g，求弗劳德数。", "desc": "弗劳德数：输入 v、L、g，输出 Fr。",
        "inputs": [
            {"id": "v", "label": "流速 v", "value": "3", "step": "0.1", "unit": "m/s"},
            {"id": "L", "label": "特征长度 L", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "g", "label": "重力加速度 g", "value": "9.81", "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const v=num('v'),L=num('L'),g=num('g');
            const Fr=v/Math.sqrt(g*L);
            ToolBox.setResult('result', dataGrid([
                [Fr.toFixed(3),'弗劳德数 Fr']
            ]));
        """,
        "notes": ["Fr>1 为急流，Fr<1 为缓流。", "v=3,L=1 → 0.958。"],
    },
    {
        "slug": "mach-number",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "zap",
        "bg": "from-sky-500 to-blue-600",
        "title": "马赫数计算器",
        "h1": "Ma = v / c",
        "h2": "由流速与声速求马赫数",
        "intro": "输入流速 v 与声速 c，求马赫数。", "desc": "马赫数：输入 v、c，输出 Ma。",
        "inputs": [
            {"id": "v", "label": "流速 v", "value": "340", "step": "10", "unit": "m/s"},
            {"id": "c", "label": "声速 c", "value": "340", "step": "10", "unit": "m/s"},
        ],
        "calc": """
            const v=num('v'),c=num('c');
            const Ma=v/c;
            ToolBox.setResult('result', dataGrid([
                [Ma.toFixed(3),'马赫数 Ma']
            ]));
        """,
        "notes": ["Ma=1 为音速；Ma>1 超声速。", "v=c=340 → Ma=1。"],
    },
    {
        "slug": "weber-number",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "droplet",
        "bg": "from-sky-500 to-blue-600",
        "title": "韦伯数计算器",
        "h1": "We = ρv²L / σ",
        "h2": "由流速、尺度与表面张力求韦伯数",
        "intro": "输入密度 ρ、流速 v、特征长度 L、表面张力 σ，求韦伯数。", "desc": "韦伯数：输入 ρ、v、L、σ，输出 We。",
        "inputs": [
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
            {"id": "v", "label": "流速 v", "value": "2", "step": "0.1", "unit": "m/s"},
            {"id": "L", "label": "特征长度 L", "value": "0.1", "step": "0.01", "unit": "m"},
            {"id": "sig", "label": "表面张力 σ", "value": "0.072", "step": "0.005", "unit": "N/m"},
        ],
        "calc": """
            const rho=num('rho'),v=num('v'),L=num('L'),sig=num('sig');
            const We=rho*v*v*L/sig;
            ToolBox.setResult('result', dataGrid([
                [We.toFixed(1),'韦伯数 We']
            ]));
        """,
        "notes": ["We 表征惯性力/表面张力。", "水,示例 → 5556。"],
    },
    {
        "slug": "kinematic-viscosity",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "wind",
        "bg": "from-sky-500 to-blue-600",
        "title": "运动黏度计算器",
        "h1": "ν = μ / ρ",
        "h2": "由动力黏度与密度求运动黏度",
        "intro": "输入动力黏度 μ 与密度 ρ，求运动黏度。", "desc": "运动黏度：输入 μ、ρ，输出 ν(m²/s)。",
        "inputs": [
            {"id": "mu", "label": "动力黏度 μ", "value": "0.001", "step": "0.0001", "unit": "Pa·s"},
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
        ],
        "calc": """
            const mu=num('mu'),rho=num('rho');
            const nu=mu/rho;
            ToolBox.setResult('result', dataGrid([
                [nu.toExponential(3),'运动黏度 ν (m²/s)']
            ]));
        """,
        "notes": ["ν = μ/ρ。", "水 20°C → 1.0×10⁻⁶ m²/s。"],
    },
    {
        "slug": "pitot-velocity",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "gauge",
        "bg": "from-sky-500 to-blue-600",
        "title": "皮托管流速计算器",
        "h1": "v = √(2ΔP / ρ)",
        "h2": "由动压差求流速",
        "intro": "输入动压差 ΔP 与密度 ρ，求流速。", "desc": "皮托管流速：输入 ΔP、ρ，输出 v(m/s)。",
        "inputs": [
            {"id": "dP", "label": "动压差 ΔP", "value": "500", "step": "10", "unit": "Pa"},
            {"id": "rho", "label": "密度 ρ", "value": "1.2", "step": "0.1", "unit": "kg/m³"},
        ],
        "calc": """
            const dP=num('dP'),rho=num('rho');
            const v=Math.sqrt(2*dP/rho);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(2),'流速 v (m/s)']
            ]));
        """,
        "notes": ["v = √(2ΔP/ρ)。", "ΔP=500,ρ=1.2 → 28.9 m/s。"],
    },
    {
        "slug": "stagnation-pressure",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "gauge",
        "bg": "from-sky-500 to-blue-600",
        "title": "驻点压力计算器",
        "h1": "p₀ = p + ½ρv²",
        "h2": "由静压与流速求驻点压力",
        "intro": "输入静压 p、密度 ρ、流速 v，求驻点压力。", "desc": "驻点压力：输入 p、ρ、v，输出 p₀(Pa)。",
        "inputs": [
            {"id": "p", "label": "静压 p", "value": "101325", "step": "100", "unit": "Pa"},
            {"id": "rho", "label": "密度 ρ", "value": "1.2", "step": "0.1", "unit": "kg/m³"},
            {"id": "v", "label": "流速 v", "value": "28.87", "step": "0.5", "unit": "m/s"},
        ],
        "calc": """
            const p=num('p'),rho=num('rho'),v=num('v');
            const p0=p+0.5*rho*v*v;
            ToolBox.setResult('result', dataGrid([
                [p0.toFixed(1),'驻点压力 p₀ (Pa)']
            ]));
        """,
        "notes": ["p₀ = p + ½ρv²（伯努利）。", "示例 → 约 101825 Pa。"],
    },
    {
        "slug": "chezy-velocity",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "waves",
        "bg": "from-sky-500 to-blue-600",
        "title": "谢才流速计算器",
        "h1": "v = C√(R·S)",
        "h2": "由谢才系数、水力半径与底坡求流速",
        "intro": "输入谢才系数 C、水力半径 R、底坡 S，求流速。", "desc": "谢才流速：输入 C、R、S，输出 v(m/s)。",
        "inputs": [
            {"id": "C", "label": "谢才系数 C", "value": "50", "step": "1", "unit": ""},
            {"id": "R", "label": "水力半径 R", "value": "0.5", "step": "0.05", "unit": "m"},
            {"id": "S", "label": "底坡 S", "value": "0.01", "step": "0.001", "unit": ""},
        ],
        "calc": """
            const C=num('C'),R=num('R'),S=num('S');
            const v=C*Math.sqrt(R*S);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(3),'流速 v (m/s)']
            ]));
        """,
        "notes": ["v = C√(RS)。", "C=50,R=0.5,S=0.01 → 3.54 m/s。"],
    },
    {
        "slug": "venturi-flow-rate",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "filter",
        "bg": "from-sky-500 to-blue-600",
        "title": "文丘里流量计计算器",
        "h1": "Q = A₂√(2ΔP / [ρ(1−(A₂/A₁)²)])",
        "h2": "由压差与截面积求体积流量",
        "intro": "输入入口/喉部面积 A1、A2 与压差 ΔP、密度 ρ，求流量。", "desc": "文丘里流量：输入 A1、A2、ΔP、ρ，输出 Q(m³/s)。",
        "inputs": [
            {"id": "A1", "label": "入口面积 A₁", "value": "0.01", "step": "0.001", "unit": "m²"},
            {"id": "A2", "label": "喉部面积 A₂", "value": "0.002", "step": "0.0005", "unit": "m²"},
            {"id": "dP", "label": "压差 ΔP", "value": "500", "step": "10", "unit": "Pa"},
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
        ],
        "calc": """
            const A1=num('A1'),A2=num('A2'),dP=num('dP'),rho=num('rho');
            const Q=A2*Math.sqrt(2*dP/(rho*(1-Math.pow(A2/A1,2))));
            ToolBox.setResult('result', dataGrid([
                [Q.toFixed(5),'体积流量 Q (m³/s)']
            ]));
        """,
        "notes": ["由伯努利+连续性推导。", "示例 → 约 0.00204 m³/s。"],
    },
    {
        "slug": "capillary-pressure",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "droplet",
        "bg": "from-sky-500 to-blue-600",
        "title": "毛细管压差计算器",
        "h1": "ΔP = 4γ / D",
        "h2": "由表面张力与管径求毛细压差",
        "intro": "输入表面张力 γ 与管内径 D，求毛细压差。", "desc": "毛细管压差：输入 γ、D，输出 ΔP(Pa)。",
        "inputs": [
            {"id": "g", "label": "表面张力 γ", "value": "0.072", "step": "0.005", "unit": "N/m"},
            {"id": "D", "label": "管内径 D", "value": "0.001", "step": "0.0001", "unit": "m"},
        ],
        "calc": """
            const g=num('g'),D=num('D');
            const dP=4*g/D;
            ToolBox.setResult('result', dataGrid([
                [dP.toFixed(1),'毛细压差 ΔP (Pa)']
            ]));
        """,
        "notes": ["ΔP = 4γ/D（完全润湿圆管）。", "水,D=1mm → 288 Pa。"],
    },
    {
        "slug": "cavitation-number",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "alert-triangle",
        "bg": "from-sky-500 to-blue-600",
        "title": "空化数计算器",
        "h1": "σ = (p − p_v) / (½ρv²)",
        "h2": "由压力与流速求空化数",
        "intro": "输入当地压力 p、饱和蒸气压 p_v、密度 ρ、流速 v，求空化数。", "desc": "空化数：输入 p、pv、ρ、v，输出 σ。",
        "inputs": [
            {"id": "p", "label": "当地压力 p", "value": "101325", "step": "100", "unit": "Pa"},
            {"id": "pv", "label": "蒸气压 p_v", "value": "2339", "step": "50", "unit": "Pa"},
            {"id": "rho", "label": "密度 ρ", "value": "1000", "step": "10", "unit": "kg/m³"},
            {"id": "v", "label": "流速 v", "value": "10", "step": "0.5", "unit": "m/s"},
        ],
        "calc": """
            const p=num('p'),pv=num('pv'),rho=num('rho'),v=num('v');
            const sig=(p-pv)/(0.5*rho*v*v);
            ToolBox.setResult('result', dataGrid([
                [sig.toFixed(3),'空化数 σ']
            ]));
        """,
        "notes": ["σ 越小越易空化（σ<1 危险）。", "水 20°C,v=10 → 约 1.98。"],
    },
    {
        "slug": "minor-loss-head",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "trending-down",
        "bg": "from-sky-500 to-blue-600",
        "title": "局部阻力损失计算器",
        "h1": "h = K·v² / (2g)",
        "h2": "由局部阻力系数与流速求水头损失",
        "intro": "输入局部阻力系数 K、流速 v、g，求水头损失。", "desc": "局部阻力损失：输入 K、v、g，输出 h(m)。",
        "inputs": [
            {"id": "K", "label": "阻力系数 K", "value": "0.5", "step": "0.1", "unit": ""},
            {"id": "v", "label": "流速 v", "value": "2", "step": "0.1", "unit": "m/s"},
            {"id": "g", "label": "重力加速度 g", "value": "9.81", "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const K=num('K'),v=num('v'),g=num('g');
            const h=K*v*v/(2*g);
            ToolBox.setResult('result', dataGrid([
                [h.toFixed(4),'水头损失 h (m)']
            ]));
        """,
        "notes": ["h = Kv²/(2g)。", "K=0.5,v=2 → 0.102 m。"],
    },
    {
        "slug": "laplace-sphere-pressure",
        "industry": "fluid",
        "cat": "fluid",
        "icon": "circle",
        "bg": "from-sky-500 to-blue-600",
        "title": "拉普拉斯球泡压差计算器",
        "h1": "ΔP = 2γ / R",
        "h2": "由表面张力与曲率半径求球泡内外压差",
        "intro": "输入表面张力 γ 与曲率半径 R，求内外压差。", "desc": "拉普拉斯球泡压差：输入 γ、R，输出 ΔP(Pa)。",
        "inputs": [
            {"id": "g", "label": "表面张力 γ", "value": "0.072", "step": "0.005", "unit": "N/m"},
            {"id": "R", "label": "曲率半径 R", "value": "0.001", "step": "0.0001", "unit": "m"},
        ],
        "calc": """
            const g=num('g'),R=num('R');
            const dP=2*g/R;
            ToolBox.setResult('result', dataGrid([
                [dP.toFixed(1),'内外压差 ΔP (Pa)']
            ]));
        """,
        "notes": ["ΔP = 2γ/R（球形液膜为 4γ/R）。", "水,R=1mm → 144 Pa。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
