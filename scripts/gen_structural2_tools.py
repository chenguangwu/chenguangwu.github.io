# -*- coding: utf-8 -*-
"""Batch 49: 结构工程深化 II（14 个公式计算器）。industry=structural。"""
from tool_template import main

TOOLS = [
    {
        "slug": "moment-of-inertia-circle",
        "industry": "structural",
        "cat": "structural",
        "icon": "circle",
        "bg": "from-rose-500 to-red-600",
        "title": "圆截面惯性矩计算器",
        "h1": "I = πd⁴ / 64",
        "h2": "由直径求实心圆截面惯性矩",
        "intro": "输入圆截面直径 d，求截面惯性矩。", "desc": "圆截面惯性矩计算器：输入 d，输出 I(mm⁴)。",
        "inputs": [{"id": "d", "label": "直径 d", "value": "0.1", "step": "0.01", "unit": "m"}],
        "calc": """
            const d=num('d');
            const I=Math.PI*Math.pow(d,4)/64;
            ToolBox.setResult('result', dataGrid([
                [(I*1e12).toFixed(2),'惯性矩 I (mm⁴)'],
                [I.toExponential(3),'惯性矩 I (m⁴)']
            ]));
        """,
        "notes": ["I = πd⁴/64（实心圆）。", "d=0.1m → 4.91×10⁶ mm⁴。"],
    },
    {
        "slug": "polar-moment-circle",
        "industry": "structural",
        "cat": "structural",
        "icon": "circle",
        "bg": "from-rose-500 to-red-600",
        "title": "圆截面极惯性矩计算器",
        "h1": "J = πd⁴ / 32",
        "h2": "由直径求实心圆截面极惯性矩",
        "intro": "输入圆截面直径 d，求极惯性矩。", "desc": "圆截面极惯性矩计算器：输入 d，输出 J(mm⁴)。",
        "inputs": [{"id": "d", "label": "直径 d", "value": "0.1", "step": "0.01", "unit": "m"}],
        "calc": """
            const d=num('d');
            const J=Math.PI*Math.pow(d,4)/32;
            ToolBox.setResult('result', dataGrid([
                [(J*1e12).toFixed(2),'极惯性矩 J (mm⁴)'],
                [J.toExponential(3),'极惯性矩 J (m⁴)']
            ]));
        """,
        "notes": ["J = πd⁴/32（实心圆）。", "d=0.1m → 9.82×10⁶ mm⁴。"],
    },
    {
        "slug": "hoop-stress",
        "industry": "structural",
        "cat": "structural",
        "icon": "cylinder",
        "bg": "from-rose-500 to-red-600",
        "title": "薄壁圆筒环向应力计算器",
        "h1": "σ_h = p·r / t",
        "h2": "由内压求环向（周向）应力",
        "intro": "输入内压 p、半径 r、壁厚 t，求环向应力。", "desc": "薄壁圆筒环向应力计算器：输入 p、r、t，输出 σ_h(MPa)。",
        "inputs": [
            {"id": "p", "label": "内压 p", "value": "2e6", "step": "1e5", "unit": "Pa"},
            {"id": "r", "label": "半径 r", "value": "0.5", "step": "0.1", "unit": "m"},
            {"id": "t", "label": "壁厚 t", "value": "0.01", "step": "0.001", "unit": "m"},
        ],
        "calc": """
            const p=num('p'),r=num('r'),t=num('t');
            const sh=p*r/t;
            ToolBox.setResult('result', dataGrid([
                [(sh/1e6).toFixed(2),'环向应力 σ_h (MPa)']
            ]));
        """,
        "notes": ["薄壁假设 t/r < 0.1。", "p=2MPa,r=0.5,t=10mm → 100 MPa。"],
    },
    {
        "slug": "longitudinal-stress",
        "industry": "structural",
        "cat": "structural",
        "icon": "cylinder",
        "bg": "from-rose-500 to-red-600",
        "title": "薄壁圆筒纵向应力计算器",
        "h1": "σ_l = p·r / (2t)",
        "h2": "由内压求纵向应力",
        "intro": "输入内压 p、半径 r、壁厚 t，求纵向应力。", "desc": "薄壁圆筒纵向应力计算器：输入 p、r、t，输出 σ_l(MPa)。",
        "inputs": [
            {"id": "p", "label": "内压 p", "value": "2e6", "step": "1e5", "unit": "Pa"},
            {"id": "r", "label": "半径 r", "value": "0.5", "step": "0.1", "unit": "m"},
            {"id": "t", "label": "壁厚 t", "value": "0.01", "step": "0.001", "unit": "m"},
        ],
        "calc": """
            const p=num('p'),r=num('r'),t=num('t');
            const sl=p*r/(2*t);
            ToolBox.setResult('result', dataGrid([
                [(sl/1e6).toFixed(2),'纵向应力 σ_l (MPa)']
            ]));
        """,
        "notes": ["σ_l = σ_h/2。", "同上例 → 50 MPa。"],
    },
    {
        "slug": "axial-stress",
        "industry": "structural",
        "cat": "structural",
        "icon": "arrow-down",
        "bg": "from-rose-500 to-red-600",
        "title": "轴向应力计算器",
        "h1": "σ = F / A",
        "h2": "由轴力与截面积求正应力",
        "intro": "输入轴力 F 与截面积 A，求正应力。", "desc": "轴向应力计算器：输入 F、A，输出 σ(MPa)。",
        "inputs": [
            {"id": "F", "label": "轴力 F", "value": "1000", "step": "10", "unit": "N"},
            {"id": "A", "label": "截面积 A", "value": "0.01", "step": "0.001", "unit": "m²"},
        ],
        "calc": """
            const F=num('F'),A=num('A');
            const sig=F/A;
            ToolBox.setResult('result', dataGrid([
                [(sig/1e6).toFixed(3),'正应力 σ (MPa)']
            ]));
        """,
        "notes": ["σ = F/A（拉为正、压为负）。", "F=1000N,A=0.01m² → 0.1 MPa。"],
    },
    {
        "slug": "axial-strain",
        "industry": "structural",
        "cat": "structural",
        "icon": "move-vertical",
        "bg": "from-rose-500 to-red-600",
        "title": "轴向应变计算器",
        "h1": "ε = ΔL / L",
        "h2": "由伸长量与原长求应变",
        "intro": "输入伸长量 ΔL 与原长 L，求轴向应变。", "desc": "轴向应变计算器：输入 ΔL、L，输出 ε。",
        "inputs": [
            {"id": "dL", "label": "伸长量 ΔL", "value": "0.002", "step": "0.0001", "unit": "m"},
            {"id": "L", "label": "原长 L", "value": "2", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const dL=num('dL'),L=num('L');
            const eps=dL/L;
            ToolBox.setResult('result', dataGrid([
                [eps.toFixed(5),'轴向应变 ε']
            ]));
        """,
        "notes": ["ε 无量纲。", "ΔL=2mm,L=2m → 0.001。"],
    },
    {
        "slug": "shear-modulus",
        "industry": "structural",
        "cat": "structural",
        "icon": "shuffle",
        "bg": "from-rose-500 to-red-600",
        "title": "剪切模量计算器",
        "h1": "G = E / [2(1+ν)]",
        "h2": "由弹性模量与泊松比求剪切模量",
        "intro": "输入弹性模量 E 与泊松比 ν，求剪切模量 G。", "desc": "剪切模量计算器：输入 E、ν，输出 G(GPa)。",
        "inputs": [
            {"id": "E", "label": "弹性模量 E", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "nu", "label": "泊松比 ν", "value": "0.3", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const E=num('E'),nu=num('nu');
            const G=E/(2*(1+nu));
            ToolBox.setResult('result', dataGrid([
                [(G/1e9).toFixed(2),'剪切模量 G (GPa)']
            ]));
        """,
        "notes": ["G = E/[2(1+ν)]。", "钢 E=200GPa,ν=0.3 → G≈76.9 GPa。"],
    },
    {
        "slug": "thermal-strain",
        "industry": "structural",
        "cat": "structural",
        "icon": "thermometer",
        "bg": "from-rose-500 to-red-600",
        "title": "热应变计算器",
        "h1": "ε = α·ΔT",
        "h2": "由线膨胀系数与温差求热应变",
        "intro": "输入线膨胀系数 α 与温差 ΔT，求热应变。", "desc": "热应变计算器：输入 α、ΔT，输出 ε。",
        "inputs": [
            {"id": "a", "label": "线膨胀系数 α", "value": "1.2e-5", "step": "1e-6", "unit": "1/°C"},
            {"id": "dT", "label": "温差 ΔT", "value": "100", "step": "1", "unit": "°C"},
        ],
        "calc": """
            const a=num('a'),dT=num('dT');
            const eps=a*dT;
            ToolBox.setResult('result', dataGrid([
                [eps.toFixed(5),'热应变 ε']
            ]));
        """,
        "notes": ["ε = α·ΔT。", "钢 α=1.2e-5,ΔT=100°C → 0.0012。"],
    },
    {
        "slug": "von-mises-2d",
        "industry": "structural",
        "cat": "structural",
        "icon": "shield",
        "bg": "from-rose-500 to-red-600",
        "title": "冯·米塞斯等效应力计算器",
        "h1": "σ_vm = √(σₓ²−σₓσᵧ+σᵧ²+3τ²)",
        "h2": "由平面应力状态求等效应力",
        "intro": "输入平面应力 σx、σy 与剪应力 τ，求冯·米塞斯等效应力。", "desc": "冯·米塞斯应力计算器：输入 σx、σy、τ，输出 σ_vm(MPa)。",
        "inputs": [
            {"id": "sx", "label": "σₓ", "value": "100e6", "step": "1e6", "unit": "Pa"},
            {"id": "sy", "label": "σᵧ", "value": "50e6", "step": "1e6", "unit": "Pa"},
            {"id": "t", "label": "τ", "value": "30e6", "step": "1e6", "unit": "Pa"},
        ],
        "calc": """
            const sx=num('sx'),sy=num('sy'),t=num('t');
            const vm=Math.sqrt(sx*sx-sx*sy+sy*sy+3*t*t);
            ToolBox.setResult('result', dataGrid([
                [(vm/1e6).toFixed(2),'等效应力 σ_vm (MPa)']
            ]));
        """,
        "notes": ["平面应力 Von Mises 公式。", "示例 → 约 101 MPa。"],
    },
    {
        "slug": "torsional-shear-shaft",
        "industry": "structural",
        "cat": "structural",
        "icon": "rotate-cw",
        "bg": "from-rose-500 to-red-600",
        "title": "圆轴扭转剪应力计算器",
        "h1": "τ = T·r / J，J=πd⁴/32",
        "h2": "由扭矩与直径求轴表面剪应力",
        "intro": "输入扭矩 T 与轴直径 d，求表面最大剪应力。", "desc": "圆轴扭转剪应力计算器：输入 T、d，输出 τ(MPa)。",
        "inputs": [
            {"id": "T", "label": "扭矩 T", "value": "500", "step": "10", "unit": "N·m"},
            {"id": "d", "label": "直径 d", "value": "0.05", "step": "0.005", "unit": "m"},
        ],
        "calc": """
            const T=num('T'),d=num('d');
            const J=Math.PI*Math.pow(d,4)/32;
            const tau=T*(d/2)/J;
            ToolBox.setResult('result', dataGrid([
                [(tau/1e6).toFixed(2),'剪应力 τ (MPa)']
            ]));
        """,
        "notes": ["τ_max = T·r/J（圆轴）。", "T=500,d=50mm → 约 20.4 MPa。"],
    },
    {
        "slug": "angle-of-twist",
        "industry": "structural",
        "cat": "structural",
        "icon": "rotate-cw",
        "bg": "from-rose-500 to-red-600",
        "title": "圆轴扭转角计算器",
        "h1": "θ = T·L / (G·J)",
        "h2": "由扭矩、长度与刚度求扭转角",
        "intro": "输入扭矩 T、长度 L、剪切模量 G、直径 d，求扭转角。", "desc": "圆轴扭转角计算器：输入 T、L、G、d，输出 θ(rad)。",
        "inputs": [
            {"id": "T", "label": "扭矩 T", "value": "500", "step": "10", "unit": "N·m"},
            {"id": "L", "label": "长度 L", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "G", "label": "剪切模量 G", "value": "80e9", "step": "1e9", "unit": "Pa"},
            {"id": "d", "label": "直径 d", "value": "0.05", "step": "0.005", "unit": "m"},
        ],
        "calc": """
            const T=num('T'),L=num('L'),G=num('G'),d=num('d');
            const J=Math.PI*Math.pow(d,4)/32;
            const th=T*L/(G*J);
            ToolBox.setResult('result', dataGrid([
                [th.toFixed(5),'扭转角 θ (rad)'],
                [(th*180/Math.PI).toFixed(3),'扭转角 θ (°)']
            ]));
        """,
        "notes": ["θ = TL/(GJ)。", "示例 → 约 0.0102 rad。"],
    },
    {
        "slug": "deflection-cantilever-udl",
        "industry": "structural",
        "cat": "structural",
        "icon": "trending-down",
        "bg": "from-rose-500 to-red-600",
        "title": "悬臂梁均布载荷挠度计算器",
        "h1": "δ = wL⁴ / (8EI)",
        "h2": "由均布载荷求悬臂梁自由端挠度",
        "intro": "输入均布载荷 w、长度 L、弹性模量 E、圆截面直径 d，求挠度。", "desc": "悬臂梁均布挠度计算器：输入 w、L、E、d，输出 δ(mm)。",
        "inputs": [
            {"id": "w", "label": "均布载荷 w", "value": "1000", "step": "50", "unit": "N/m"},
            {"id": "L", "label": "长度 L", "value": "2", "step": "0.1", "unit": "m"},
            {"id": "E", "label": "弹性模量 E", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "d", "label": "直径 d", "value": "0.1", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const w=num('w'),L=num('L'),E=num('E'),d=num('d');
            const I=Math.PI*Math.pow(d,4)/64;
            const delta=w*Math.pow(L,4)/(8*E*I);
            ToolBox.setResult('result', dataGrid([
                [(delta*1000).toFixed(3),'挠度 δ (mm)']
            ]));
        """,
        "notes": ["δ = wL⁴/(8EI)（自由端）。", "示例 → 约 2.04 mm。"],
    },
    {
        "slug": "deflection-cantilever-point",
        "industry": "structural",
        "cat": "structural",
        "icon": "trending-down",
        "bg": "from-rose-500 to-red-600",
        "title": "悬臂梁端点载荷挠度计算器",
        "h1": "δ = FL³ / (3EI)",
        "h2": "由端点集中力求悬臂梁挠度",
        "intro": "输入端点力 F、长度 L、弹性模量 E、圆截面直径 d，求挠度。", "desc": "悬臂梁端点挠度计算器：输入 F、L、E、d，输出 δ(mm)。",
        "inputs": [
            {"id": "F", "label": "端点力 F", "value": "100", "step": "10", "unit": "N"},
            {"id": "L", "label": "长度 L", "value": "2", "step": "0.1", "unit": "m"},
            {"id": "E", "label": "弹性模量 E", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "d", "label": "直径 d", "value": "0.1", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const F=num('F'),L=num('L'),E=num('E'),d=num('d');
            const I=Math.PI*Math.pow(d,4)/64;
            const delta=F*Math.pow(L,3)/(3*E*I);
            ToolBox.setResult('result', dataGrid([
                [(delta*1000).toFixed(4),'挠度 δ (mm)']
            ]));
        """,
        "notes": ["δ = FL³/(3EI)（自由端）。", "示例 → 约 0.272 mm。"],
    },
    {
        "slug": "section-modulus-circle",
        "industry": "structural",
        "cat": "structural",
        "icon": "circle",
        "bg": "from-rose-500 to-red-600",
        "title": "圆截面抗弯截面模量计算器",
        "h1": "S = πd³ / 32",
        "h2": "由直径求圆截面抗弯模量",
        "intro": "输入圆截面直径 d，求抗弯截面模量。", "desc": "圆截面抗弯模量计算器：输入 d，输出 S(mm³)。",
        "inputs": [{"id": "d", "label": "直径 d", "value": "0.1", "step": "0.01", "unit": "m"}],
        "calc": """
            const d=num('d');
            const S=Math.PI*Math.pow(d,3)/32;
            ToolBox.setResult('result', dataGrid([
                [(S*1e9).toFixed(2),'抗弯模量 S (mm³)']
            ]));
        """,
        "notes": ["S = πd³/32（圆截面）。", "d=0.1m → 9.82×10⁴ mm³。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
