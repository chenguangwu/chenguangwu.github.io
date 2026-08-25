# -*- coding: utf-8 -*-
"""Batch 50: 材料科学深化 II（14 个公式计算器）。industry=materials。"""
from tool_template import main

TOOLS = [
    {
        "slug": "brinell-hardness",
        "industry": "materials",
        "cat": "materials",
        "icon": "disc",
        "bg": "from-emerald-500 to-green-600",
        "title": "布氏硬度计算器",
        "h1": "BHN = 2F / [πD(D−√(D²−d²))]",
        "h2": "由压痕载荷与直径求布氏硬度",
        "intro": "输入载荷 F、压头直径 D 与压痕直径 d，求布氏硬度。", "desc": "布氏硬度计算器：输入 F、D、d，输出 BHN。",
        "inputs": [
            {"id": "F", "label": "载荷 F", "value": "3000", "step": "100", "unit": "N"},
            {"id": "D", "label": "压头直径 D", "value": "10", "step": "0.5", "unit": "mm"},
            {"id": "d", "label": "压痕直径 d", "value": "4.2", "step": "0.1", "unit": "mm"},
        ],
        "calc": """
            const F=num('F'),D=num('D'),d=num('d');
            const BHN=2*F/(Math.PI*D*(D-Math.sqrt(D*D-d*d)));
            ToolBox.setResult('result', dataGrid([
                [BHN.toFixed(2),'布氏硬度 BHN']
            ]));
        """,
        "notes": ["单位一致（mm/N）即可。", "F=3000N,D=10,d=4.2mm → 约 202 BHN。"],
    },
    {
        "slug": "fourier-conduction",
        "industry": "materials",
        "cat": "materials",
        "icon": "flame",
        "bg": "from-emerald-500 to-green-600",
        "title": "一维热传导计算器",
        "h1": "q = k·A·ΔT / L",
        "h2": "由傅里叶定律求热流率",
        "intro": "输入导热系数 k、面积 A、温差 ΔT、厚度 L，求热流率。", "desc": "一维热传导计算器：输入 k、A、ΔT、L，输出 q(W)。",
        "inputs": [
            {"id": "k", "label": "导热系数 k", "value": "50", "step": "1", "unit": "W/(m·K)"},
            {"id": "A", "label": "面积 A", "value": "0.01", "step": "0.001", "unit": "m²"},
            {"id": "dT", "label": "温差 ΔT", "value": "100", "step": "1", "unit": "K"},
            {"id": "L", "label": "厚度 L", "value": "0.05", "step": "0.005", "unit": "m"},
        ],
        "calc": """
            const k=num('k'),A=num('A'),dT=num('dT'),L=num('L');
            const q=k*A*dT/L;
            ToolBox.setResult('result', dataGrid([
                [q.toFixed(1),'热流率 q (W)']
            ]));
        """,
        "notes": ["q = k·A·ΔT/L。", "钢 k=50，示例 → 1000 W。"],
    },
    {
        "slug": "specific-heat-capacity",
        "industry": "materials",
        "cat": "materials",
        "icon": "thermometer",
        "bg": "from-emerald-500 to-green-600",
        "title": "热容计算器",
        "h1": "C = m·c",
        "h2": "由质量与比热容求热容",
        "intro": "输入质量 m 与比热容 c，求热容。", "desc": "热容计算器：输入 m、c，输出 C(J/K)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "2", "step": "0.1", "unit": "kg"},
            {"id": "c", "label": "比热容 c", "value": "4200", "step": "50", "unit": "J/(kg·K)"},
        ],
        "calc": """
            const m=num('m'),c=num('c');
            const C=m*c;
            ToolBox.setResult('result', dataGrid([
                [C.toFixed(0),'热容 C (J/K)']
            ]));
        """,
        "notes": ["C = m·c。", "水 m=2kg,c=4200 → 8400 J/K。"],
    },
    {
        "slug": "linear-thermal-expansion",
        "industry": "materials",
        "cat": "materials",
        "icon": "move-vertical",
        "bg": "from-emerald-500 to-green-600",
        "title": "线膨胀量计算器",
        "h1": "ΔL = α·L·ΔT",
        "h2": "由线膨胀系数求伸长量",
        "intro": "输入线膨胀系数 α、原长 L、温差 ΔT，求伸长量。", "desc": "线膨胀量计算器：输入 α、L、ΔT，输出 ΔL(mm)。",
        "inputs": [
            {"id": "a", "label": "线膨胀系数 α", "value": "1.2e-5", "step": "1e-6", "unit": "1/K"},
            {"id": "L", "label": "原长 L", "value": "2", "step": "0.1", "unit": "m"},
            {"id": "dT", "label": "温差 ΔT", "value": "100", "step": "1", "unit": "K"},
        ],
        "calc": """
            const a=num('a'),L=num('L'),dT=num('dT');
            const dL=a*L*dT;
            ToolBox.setResult('result', dataGrid([
                [(dL*1000).toFixed(3),'伸长量 ΔL (mm)']
            ]));
        """,
        "notes": ["ΔL = α·L·ΔT。", "钢 α=1.2e-5,L=2m,ΔT=100 → 2.4 mm。"],
    },
    {
        "slug": "poisson-ratio-calc",
        "industry": "materials",
        "cat": "materials",
        "icon": "shuffle",
        "bg": "from-emerald-500 to-green-600",
        "title": "泊松比计算器",
        "h1": "ν = −ε_lat / ε_ax",
        "h2": "由横向与轴向应变求泊松比",
        "intro": "输入横向应变 ε_lat 与轴向应变 ε_ax，求泊松比。", "desc": "泊松比计算器：输入 ε_lat、ε_ax，输出 ν。",
        "inputs": [
            {"id": "el", "label": "横向应变 ε_lat", "value": "-0.003", "step": "0.0001", "unit": ""},
            {"id": "ea", "label": "轴向应变 ε_ax", "value": "0.01", "step": "0.0001", "unit": ""},
        ],
        "calc": """
            const el=num('el'),ea=num('ea');
            const nu=-el/ea;
            ToolBox.setResult('result', dataGrid([
                [nu.toFixed(3),'泊松比 ν']
            ]));
        """,
        "notes": ["ν = −ε_lat/ε_ax。", "ε_lat=−0.003,ε_ax=0.01 → ν=0.3。"],
    },
    {
        "slug": "lame-lambda",
        "industry": "materials",
        "cat": "materials",
        "icon": "sigma",
        "bg": "from-emerald-500 to-green-600",
        "title": "拉梅常数 λ 计算器",
        "h1": "λ = Eν / [(1+ν)(1−2ν)]",
        "h2": "由弹性模量与泊松比求拉梅常数",
        "intro": "输入弹性模量 E 与泊松比 ν，求拉梅常数 λ。", "desc": "拉梅常数 λ 计算器：输入 E、ν，输出 λ(GPa)。",
        "inputs": [
            {"id": "E", "label": "弹性模量 E", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "nu", "label": "泊松比 ν", "value": "0.3", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const E=num('E'),nu=num('nu');
            const lam=E*nu/((1+nu)*(1-2*nu));
            ToolBox.setResult('result', dataGrid([
                [(lam/1e9).toFixed(2),'拉梅常数 λ (GPa)']
            ]));
        """,
        "notes": ["λ = Eν/[(1+ν)(1−2ν)]。", "钢 E=200GPa,ν=0.3 → 约 115 GPa。"],
    },
    {
        "slug": "bulk-modulus-e-nu",
        "industry": "materials",
        "cat": "materials",
        "icon": "compress",
        "bg": "from-emerald-500 to-green-600",
        "title": "体积模量(由E,ν)计算器",
        "h1": "K = E / [3(1−2ν)]",
        "h2": "由弹性模量与泊松比求体积模量",
        "intro": "输入弹性模量 E 与泊松比 ν，求体积模量。", "desc": "体积模量计算器：输入 E、ν，输出 K(GPa)。",
        "inputs": [
            {"id": "E", "label": "弹性模量 E", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "nu", "label": "泊松比 ν", "value": "0.3", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const E=num('E'),nu=num('nu');
            const K=E/(3*(1-2*nu));
            ToolBox.setResult('result', dataGrid([
                [(K/1e9).toFixed(2),'体积模量 K (GPa)']
            ]));
        """,
        "notes": ["K = E/[3(1−2ν)]。", "钢 → 约 166.7 GPa。"],
    },
    {
        "slug": "thermal-diffusivity",
        "industry": "materials",
        "cat": "materials",
        "icon": "wind",
        "bg": "from-emerald-500 to-green-600",
        "title": "热扩散率计算器",
        "h1": "α = k / (ρ·c)",
        "h2": "由导热系数、密度与比热求热扩散率",
        "intro": "输入导热系数 k、密度 ρ、比热容 c，求热扩散率。", "desc": "热扩散率计算器：输入 k、ρ、c，输出 α(m²/s)。",
        "inputs": [
            {"id": "k", "label": "导热系数 k", "value": "50", "step": "1", "unit": "W/(m·K)"},
            {"id": "rho", "label": "密度 ρ", "value": "7850", "step": "50", "unit": "kg/m³"},
            {"id": "c", "label": "比热容 c", "value": "460", "step": "10", "unit": "J/(kg·K)"},
        ],
        "calc": """
            const k=num('k'),rho=num('rho'),c=num('c');
            const alpha=k/(rho*c);
            ToolBox.setResult('result', dataGrid([
                [alpha.toExponential(3),'热扩散率 α (m²/s)']
            ]));
        """,
        "notes": ["α = k/(ρ·c)。", "钢 ≈ 1.4×10⁻⁵ m²/s。"],
    },
    {
        "slug": "volumetric-strain",
        "industry": "materials",
        "cat": "materials",
        "icon": "box",
        "bg": "from-emerald-500 to-green-600",
        "title": "体积应变计算器",
        "h1": "ε_v = ε_x + ε_y + ε_z",
        "h2": "由三向主应变求和体积应变",
        "intro": "输入三个正交方向应变，求体积应变。", "desc": "体积应变计算器：输入 εx、εy、εz，输出 ε_v。",
        "inputs": [
            {"id": "ex", "label": "ε_x", "value": "0.01", "step": "0.001", "unit": ""},
            {"id": "ey", "label": "ε_y", "value": "-0.003", "step": "0.001", "unit": ""},
            {"id": "ez", "label": "ε_z", "value": "-0.003", "step": "0.001", "unit": ""},
        ],
        "calc": """
            const ex=num('ex'),ey=num('ey'),ez=num('ez');
            const ev=ex+ey+ez;
            ToolBox.setResult('result', dataGrid([
                [ev.toFixed(5),'体积应变 ε_v']
            ]));
        """,
        "notes": ["ε_v = ε_x+ε_y+ε_z。", "0.01−0.003−0.003 → 0.004。"],
    },
    {
        "slug": "fracture-toughness",
        "industry": "materials",
        "cat": "materials",
        "icon": "crack",
        "bg": "from-emerald-500 to-green-600",
        "title": "断裂韧度计算器",
        "h1": "K_IC = Y·σ·√(πa)",
        "h2": "由应力强度因子求断裂韧度",
        "intro": "输入几何因子 Y、应力 σ、裂纹半长 a，求应力强度因子。", "desc": "断裂韧度计算器：输入 Y、σ、a，输出 K(MPa√m)。",
        "inputs": [
            {"id": "Y", "label": "几何因子 Y", "value": "1.12", "step": "0.01", "unit": ""},
            {"id": "sig", "label": "应力 σ", "value": "100e6", "step": "1e6", "unit": "Pa"},
            {"id": "a", "label": "裂纹半长 a", "value": "0.01", "step": "0.001", "unit": "m"},
        ],
        "calc": """
            const Y=num('Y'),sig=num('sig'),a=num('a');
            const K=Y*sig*Math.sqrt(Math.PI*a);
            ToolBox.setResult('result', dataGrid([
                [(K/1e6).toFixed(2),'应力强度因子 K (MPa√m)']
            ]));
        """,
        "notes": ["K = Y·σ·√(πa)；K≥K_IC 时失稳。", "示例 → 约 19.9 MPa√m。"],
    },
    {
        "slug": "shear-strain",
        "industry": "materials",
        "cat": "materials",
        "icon": "shuffle",
        "bg": "from-emerald-500 to-green-600",
        "title": "剪应变计算器",
        "h1": "γ = τ / G",
        "h2": "由剪应力与剪切模量求剪应变",
        "intro": "输入剪应力 τ 与剪切模量 G，求剪应变。", "desc": "剪应变计算器：输入 τ、G，输出 γ。",
        "inputs": [
            {"id": "tau", "label": "剪应力 τ", "value": "50e6", "step": "1e6", "unit": "Pa"},
            {"id": "G", "label": "剪切模量 G", "value": "80e9", "step": "1e9", "unit": "Pa"},
        ],
        "calc": """
            const tau=num('tau'),G=num('G');
            const g=tau/G;
            ToolBox.setResult('result', dataGrid([
                [g.toExponential(3),'剪应变 γ']
            ]));
        """,
        "notes": ["γ = τ/G。", "τ=50MPa,G=80GPa → 6.25×10⁻⁴。"],
    },
    {
        "slug": "elastic-energy-density",
        "industry": "materials",
        "cat": "materials",
        "icon": "battery-charging",
        "bg": "from-emerald-500 to-green-600",
        "title": "弹性应变能密度计算器",
        "h1": "u = σ² / (2E)",
        "h2": "由应力与弹性模量求应变能密度",
        "intro": "输入应力 σ 与弹性模量 E，求单位体积应变能。", "desc": "弹性应变能密度计算器：输入 σ、E，输出 u(kJ/m³)。",
        "inputs": [
            {"id": "sig", "label": "应力 σ", "value": "200e6", "step": "1e6", "unit": "Pa"},
            {"id": "E", "label": "弹性模量 E", "value": "200e9", "step": "1e9", "unit": "Pa"},
        ],
        "calc": """
            const sig=num('sig'),E=num('E');
            const u=sig*sig/(2*E);
            ToolBox.setResult('result', dataGrid([
                [(u/1e3).toFixed(1),'应变能密度 u (kJ/m³)']
            ]));
        """,
        "notes": ["u = σ²/(2E)。", "σ=200MPa,E=200GPa → 100 kJ/m³。"],
    },
    {
        "slug": "thermal-resistance",
        "industry": "materials",
        "cat": "materials",
        "icon": "thermometer",
        "bg": "from-emerald-500 to-green-600",
        "title": "热阻计算器",
        "h1": "R_th = L / (k·A)",
        "h2": "由厚度、导热系数与面积求热阻",
        "intro": "输入厚度 L、导热系数 k、面积 A，求热阻。", "desc": "热阻计算器：输入 L、k、A，输出 R_th(K/W)。",
        "inputs": [
            {"id": "L", "label": "厚度 L", "value": "0.05", "step": "0.005", "unit": "m"},
            {"id": "k", "label": "导热系数 k", "value": "50", "step": "1", "unit": "W/(m·K)"},
            {"id": "A", "label": "面积 A", "value": "0.01", "step": "0.001", "unit": "m²"},
        ],
        "calc": """
            const L=num('L'),k=num('k'),A=num('A');
            const R=L/(k*A);
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(4),'热阻 R_th (K/W)']
            ]));
        """,
        "notes": ["R_th = L/(k·A)。", "示例 → 0.1 K/W。"],
    },
    {
        "slug": "young-from-kg",
        "industry": "materials",
        "cat": "materials",
        "icon": "sigma",
        "bg": "from-emerald-500 to-green-600",
        "title": "由体积与剪切模量求弹性模量",
        "h1": "E = 9KG / (3K+G)",
        "h2": "由 K 与 G 反推弹性模量",
        "intro": "输入体积模量 K 与剪切模量 G，求弹性模量 E。", "desc": "由 K、G 求弹性模量：输入 K、G，输出 E(GPa)。",
        "inputs": [
            {"id": "K", "label": "体积模量 K", "value": "166.7e9", "step": "1e9", "unit": "Pa"},
            {"id": "G", "label": "剪切模量 G", "value": "76.9e9", "step": "1e9", "unit": "Pa"},
        ],
        "calc": """
            const K=num('K'),G=num('G');
            const E=9*K*G/(3*K+G);
            ToolBox.setResult('result', dataGrid([
                [(E/1e9).toFixed(2),'弹性模量 E (GPa)']
            ]));
        """,
        "notes": ["E = 9KG/(3K+G)。", "K=166.7,G=76.9 GPa → 约 200 GPa。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
