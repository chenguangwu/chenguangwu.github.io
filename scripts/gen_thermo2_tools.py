# -*- coding: utf-8 -*-
"""Batch 45: 热力学计算深化 II（14 个公式计算器）。industry=thermodynamics。"""
from tool_template import main

R = 8.314  # 气体常数 J/(mol·K)

TOOLS = [
    {
        "slug": "adiabatic-tv",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "thermometer",
        "bg": "from-orange-500 to-red-600",
        "title": "绝热过程温度计算器",
        "h1": "T·V^(γ−1) = 常数",
        "h2": "理想气体可逆绝热过程温度-体积关系",
        "intro": "输入初态温度/体积、末态体积与比热比 γ，求末态温度。",
        "desc": "绝热过程温度计算器：输入 T1、V1、V2、γ，输出 T2。",
        "inputs": [
            {"id": "T1", "label": "初态温度 T₁", "value": "300", "step": "1", "unit": "K"},
            {"id": "V1", "label": "初态体积 V₁", "value": "1", "step": "0.1", "unit": "L"},
            {"id": "V2", "label": "末态体积 V₂", "value": "2", "step": "0.1", "unit": "L"},
            {"id": "gamma", "label": "比热比 γ", "value": "1.4", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const T1=num('T1'),V1=num('V1'),V2=num('V2'),g=num('gamma');
            const T2=T1*Math.pow(V1/V2, g-1);
            ToolBox.setResult('result', dataGrid([
                [T2.toFixed(2),'末态温度 T₂ (K)'],
                [(T2-273.15).toFixed(2),'末态温度 (℃)']
            ]));
        """,
        "notes": ["T₁V₁^(γ−1)=T₂V₂^(γ−1)。", "300K 体积翻倍(γ=1.4) → T₂≈227.4 K。"],
    },
    {
        "slug": "polytropic-work",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "calculator",
        "bg": "from-orange-500 to-red-600",
        "title": "多变过程功计算器",
        "h1": "W = (P₂V₂ − P₁V₁) / (1 − n)",
        "h2": "多方指数 n 过程的体积功",
        "intro": "输入初末态压力与体积及多方指数 n，求过程功。",
        "desc": "多变过程功计算器：输入 P1、V1、P2、V2、n，输出 W。",
        "inputs": [
            {"id": "p1", "label": "初压 P₁", "value": "100", "step": "1", "unit": "kPa"},
            {"id": "v1", "label": "初容 V₁", "value": "1", "step": "0.1", "unit": "m³"},
            {"id": "p2", "label": "末压 P₂", "value": "50", "step": "1", "unit": "kPa"},
            {"id": "v2", "label": "末容 V₂", "value": "2", "step": "0.1", "unit": "m³"},
            {"id": "n", "label": "多方指数 n", "value": "1.3", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const p1=num('p1')*1000, v1=num('v1'), p2=num('p2')*1000, v2=num('v2'), n=num('n');
            const W=(p2*v2 - p1*v1)/(1-n);
            ToolBox.setResult('result', dataGrid([
                [(W/1000).toFixed(2),'过程功 W (kJ)']
            ]));
        """,
        "notes": ["W=(P₂V₂−P₁V₁)/(1−n)（SI 单位）。", "n=1 时退化为等温，需另用 ln 式。"],
    },
    {
        "slug": "thermal-resistance-series",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "layers",
        "bg": "from-orange-500 to-red-600",
        "title": "多层平壁热阻计算器",
        "h1": "R = L / (k·A)（串联相加）",
        "h2": "双层复合壁总热阻与热流",
        "intro": "输入两层的厚度、导热系数与面积，求总热阻、总温差热流。",
        "desc": "多层平壁热阻计算器：输入 L/k/A 各层，输出总热阻与热流。",
        "inputs": [
            {"id": "L1", "label": "层1 厚度 L₁", "value": "0.1", "step": "0.01", "unit": "m"},
            {"id": "k1", "label": "层1 导热系数 k₁", "value": "0.04", "step": "0.01", "unit": "W/(m·K)"},
            {"id": "L2", "label": "层2 厚度 L₂", "value": "0.2", "step": "0.01", "unit": "m"},
            {"id": "k2", "label": "层2 导热系数 k₂", "value": "1.0", "step": "0.1", "unit": "W/(m·K)"},
            {"id": "A", "label": "面积 A", "value": "1", "step": "0.1", "unit": "m²"},
        ],
        "calc": """
            const L1=num('L1'),k1=num('k1'),L2=num('L2'),k2=num('k2'),A=num('A');
            const R1=L1/(k1*A), R2=L2/(k2*A);
            ToolBox.setResult('result', dataGrid([
                [(R1+R2).toFixed(4),'总热阻 R (K/W)'],
                [(1/(R1+R2)).toFixed(2),'总传热系数 U (W/(m²·K))']
            ]));
        """,
        "notes": ["串联 R=R1+R2，U=1/R_total。", "保温层+砖墙示例可得低 U 值。"],
    },
    {
        "slug": "convective-heat-rate",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "wind",
        "bg": "from-orange-500 to-red-600",
        "title": "对流换热率计算器",
        "h1": "Q̇ = h·A·ΔT",
        "h2": "牛顿冷却定律的热流密度",
        "intro": "输入表面传热系数、面积与温差，求对流换热功率。",
        "desc": "对流换热率计算器：输入 h、A、ΔT，输出 Q̇。",
        "inputs": [
            {"id": "h", "label": "传热系数 h", "value": "10", "step": "1", "unit": "W/(m²·K)"},
            {"id": "A", "label": "面积 A", "value": "2", "step": "0.1", "unit": "m²"},
            {"id": "dT", "label": "温差 ΔT", "value": "20", "step": "1", "unit": "K"},
        ],
        "calc": """
            const h=num('h'),A=num('A'),dT=num('dT');
            ToolBox.setResult('result', dataGrid([
                [(h*A*dT).toFixed(2),'换热率 Q̇ (W)']
            ]));
        """,
        "notes": ["Q̇ = h·A·ΔT。", "h=10、A=2、ΔT=20 → 400 W。"],
    },
    {
        "slug": "biot-number",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "grid",
        "bg": "from-orange-500 to-red-600",
        "title": "毕渥数计算器",
        "h1": "Bi = h·L / k",
        "h2": "判断是否满足集总参数法",
        "intro": "输入传热系数、特征长度与导热系数，求毕渥数 Bi。",
        "desc": "毕渥数计算器：输入 h、L、k，输出 Bi 及集总判据。",
        "inputs": [
            {"id": "h", "label": "传热系数 h", "value": "50", "step": "1", "unit": "W/(m²·K)"},
            {"id": "L", "label": "特征长度 L", "value": "0.05", "step": "0.01", "unit": "m"},
            {"id": "k", "label": "导热系数 k", "value": "400", "step": "1", "unit": "W/(m·K)"},
        ],
        "calc": """
            const h=num('h'),L=num('L'),k=num('k');
            const Bi=h*L/k;
            const lump = Bi<0.1 ? '可用集总参数法 (Bi<0.1)' : '内部温度梯度不可忽略';
            ToolBox.setResult('result', dataGrid([
                [Bi.toFixed(4),'毕渥数 Bi'],
                [lump,'判据']
            ]));
        """,
        "notes": ["Bi = hL/k。Bi<0.1 时可用集总参数法。", "金属小件常满足 Bi<<1。"],
    },
    {
        "slug": "fourier-number",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "clock",
        "bg": "from-orange-500 to-red-600",
        "title": "傅里叶数计算器",
        "h1": "Fo = α·t / L²",
        "h2": "无量纲瞬态导热时间尺度",
        "intro": "输入热扩散率、时间与特征长度，求傅里叶数 Fo。",
        "desc": "傅里叶数计算器：输入 α、t、L，输出 Fo。",
        "inputs": [
            {"id": "alpha", "label": "热扩散率 α", "value": "1e-5", "step": "1e-6", "unit": "m²/s"},
            {"id": "t", "label": "时间 t", "value": "100", "step": "1", "unit": "s"},
            {"id": "L", "label": "特征长度 L", "value": "0.01", "step": "0.001", "unit": "m"},
        ],
        "calc": """
            const alpha=num('alpha'),t=num('t'),L=num('L');
            ToolBox.setResult('result', dataGrid([
                [(alpha*t/(L*L)).toFixed(3),'傅里叶数 Fo']
            ]));
        """,
        "notes": ["Fo = αt/L²。Fo≥0.2 后温度分布趋于正则。"],
    },
    {
        "slug": "grashof-number",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "arrows-up-down",
        "bg": "from-orange-500 to-red-600",
        "title": "格拉晓夫数计算器",
        "h1": "Gr = g·β·ΔT·L³ / ν²",
        "h2": "自然对流驱动力无量纲数",
        "intro": "输入重力加速度、体膨胀系数、温差、特征长度与运动黏度，求 Gr。",
        "desc": "格拉晓夫数计算器：输入 g、β、ΔT、L、ν，输出 Gr。",
        "inputs": [
            {"id": "g", "label": "重力加速度 g", "value": "9.81", "step": "0.01", "unit": "m/s²"},
            {"id": "beta", "label": "体膨胀系数 β", "value": "0.003", "step": "0.0005", "unit": "1/K"},
            {"id": "dT", "label": "温差 ΔT", "value": "10", "step": "1", "unit": "K"},
            {"id": "L", "label": "特征长度 L", "value": "0.1", "step": "0.01", "unit": "m"},
            {"id": "nu", "label": "运动黏度 ν", "value": "1.5e-5", "step": "1e-6", "unit": "m²/s"},
        ],
        "calc": """
            const g=num('g'),beta=num('beta'),dT=num('dT'),L=num('L'),nu=num('nu');
            const Gr=g*beta*dT*L*L*L/(nu*nu);
            ToolBox.setResult('result', dataGrid([
                [Gr.toExponential(3),'格拉晓夫数 Gr']
            ]));
        """,
        "notes": ["Gr = gβΔTL³/ν²。与 Re² 比决定自然/强制对流主导。"],
    },
    {
        "slug": "newton-cooling",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "thermometer",
        "bg": "from-orange-500 to-red-600",
        "title": "牛顿冷却时间计算器",
        "h1": "T(t) = T∞ + (T₀−T∞)·e^(−kt)",
        "h2": "集总参数法的温度衰减",
        "intro": "输入初温、环境温、时间常数 k 与时间，求当前温度。",
        "desc": "牛顿冷却计算器：输入 T0、T∞、k、t，输出 T(t)。",
        "inputs": [
            {"id": "T0", "label": "初温 T₀", "value": "100", "step": "1", "unit": "℃"},
            {"id": "Tinf", "label": "环境温度 T∞", "value": "20", "step": "1", "unit": "℃"},
            {"id": "k", "label": "冷却常数 k", "value": "0.05", "step": "0.005", "unit": "1/min"},
            {"id": "t", "label": "时间 t", "value": "30", "step": "1", "unit": "min"},
        ],
        "calc": """
            const T0=num('T0'),Ti=num('Tinf'),k=num('k'),t=num('t');
            const T=Ti+(T0-Ti)*Math.exp(-k*t);
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'t 时刻温度 (℃)']
            ]));
        """,
        "notes": ["T(t)=T∞+(T₀−T∞)e^(−kt)。", "k=0.05/min、30min → 约 40℃。"],
    },
    {
        "slug": "otto-efficiency",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "gauge",
        "bg": "from-orange-500 to-red-600",
        "title": "奥托循环效率计算器",
        "h1": "η = 1 − 1 / r^(γ−1)",
        "h2": "理想汽油机（定容加热）热效率",
        "intro": "输入压缩比 r 与比热比 γ，求奥托循环热效率。",
        "desc": "奥托循环效率计算器：输入 r、γ，输出 η。",
        "inputs": [
            {"id": "r", "label": "压缩比 r", "value": "10", "step": "0.5", "unit": ""},
            {"id": "g", "label": "比热比 γ", "value": "1.4", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const r=num('r'),g=num('g');
            const eff=1-1/Math.pow(r, g-1);
            ToolBox.setResult('result', dataGrid([
                [(eff*100).toFixed(2),'热效率 η (%)']
            ]));
        """,
        "notes": ["η_otto = 1 − 1/r^(γ−1)。", "r=10、γ=1.4 → η≈60.2%。"],
    },
    {
        "slug": "diesel-efficiency",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "gauge",
        "bg": "from-orange-500 to-red-600",
        "title": "狄塞尔循环效率计算器",
        "h1": "η = 1 − (1/r^(γ−1))·(ρ^γ−1)/(γ(ρ−1))",
        "h2": "理想柴油机（定压加热）热效率",
        "intro": "输入压缩比 r、截止比 ρ 与比热比 γ，求狄塞尔循环效率。",
        "desc": "狄塞尔循环效率计算器：输入 r、ρ、γ，输出 η。",
        "inputs": [
            {"id": "r", "label": "压缩比 r", "value": "18", "step": "0.5", "unit": ""},
            {"id": "rho", "label": "截止比 ρ", "value": "2", "step": "0.1", "unit": ""},
            {"id": "g", "label": "比热比 γ", "value": "1.4", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const r=num('r'),rho=num('rho'),g=num('g');
            const eff=1-(1/Math.pow(r,g-1))*(Math.pow(rho,g)-1)/(g*(rho-1));
            ToolBox.setResult('result', dataGrid([
                [(eff*100).toFixed(2),'热效率 η (%)']
            ]));
        """,
        "notes": ["η_diesel = 1 − (1/r^(γ−1))·(ρ^γ−1)/(γ(ρ−1))。", "r=18、ρ=2、γ=1.4 → η≈63%。"],
    },
    {
        "slug": "compressor-isentropic-work",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "compress",
        "bg": "from-orange-500 to-red-600",
        "title": "等熵压缩功计算器",
        "h1": "w = (γ/(γ−1))·R·T₁·[(P₂/P₁)^((γ−1)/γ) − 1]",
        "h2": "理想气体单位质量等熵压缩功",
        "intro": "输入初温、压比、比热比与气体常数，求单位质量压缩功。",
        "desc": "等熵压缩功计算器：输入 T1、PR、γ、R，输出 w。",
        "inputs": [
            {"id": "T1", "label": "进气温度 T₁", "value": "300", "step": "1", "unit": "K"},
            {"id": "PR", "label": "压比 P₂/P₁", "value": "8", "step": "0.5", "unit": ""},
            {"id": "g", "label": "比热比 γ", "value": "1.4", "step": "0.01", "unit": ""},
            {"id": "Rgas", "label": "气体常数 R", "value": "287", "step": "1", "unit": "J/(kg·K)"},
        ],
        "calc": """
            const T1=num('T1'),PR=num('PR'),g=num('g'),Rg=num('Rgas');
            const w=(g/(g-1))*Rg*T1*(Math.pow(PR,(g-1)/g)-1);
            ToolBox.setResult('result', dataGrid([
                [w.toFixed(1),'单位质量压缩功 w (J/kg)']
            ]));
        """,
        "notes": ["w = γ/(γ−1)·R·T₁·[(P₂/P₁)^((γ−1)/γ)−1]。", "空气 300K、压比8 → 约 234 kJ/kg。"],
    },
    {
        "slug": "lmtd-heat-exchanger",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "arrow-left-right",
        "bg": "from-orange-500 to-red-600",
        "title": "对数平均温差计算器",
        "h1": "LMTD = (ΔT₁ − ΔT₂) / ln(ΔT₁/ΔT₂)",
        "h2": "换热器平均传热温差",
        "intro": "输入两端温差 ΔT₁、ΔT₂，求对数平均温差。",
        "desc": "对数平均温差计算器：输入 ΔT1、ΔT2，输出 LMTD。",
        "inputs": [
            {"id": "dt1", "label": "端1 温差 ΔT₁", "value": "60", "step": "1", "unit": "K"},
            {"id": "dt2", "label": "端2 温差 ΔT₂", "value": "30", "step": "1", "unit": "K"},
        ],
        "calc": """
            const a=num('dt1'),b=num('dt2');
            const lmtd=(a-b)/Math.log(a/b);
            ToolBox.setResult('result', dataGrid([
                [lmtd.toFixed(2),'对数平均温差 LMTD (K)']
            ]));
        """,
        "notes": ["LMTD=(ΔT₁−ΔT₂)/ln(ΔT₁/ΔT₂)。", "60 与 30 → 43.3 K。"],
    },
    {
        "slug": "entropy-generation",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "shuffle",
        "bg": "from-orange-500 to-red-600",
        "title": "熵产计算器",
        "h1": "S_gen = ΔS_sys + ΔS_surr ≥ 0",
        "h2": "由系统与外界熵变求熵产",
        "intro": "输入系统熵变与热源熵变，求熵产（应 ≥0）。",
        "desc": "熵产计算器：输入 ΔS_sys、ΔS_surr，输出 S_gen。",
        "inputs": [
            {"id": "dsSys", "label": "系统熵变 ΔS_sys", "value": "10", "step": "0.1", "unit": "J/K"},
            {"id": "dsSurr", "label": "环境熵变 ΔS_surr", "value": "-9", "step": "0.1", "unit": "J/K"},
        ],
        "calc": """
            const a=num('dsSys'),b=num('dsSurr');
            const sgen=a+b;
            const ok = sgen>=0 ? '满足第二定律 (S_gen≥0)' : '违反第二定律!';
            ToolBox.setResult('result', dataGrid([
                [sgen.toFixed(3),'熵产 S_gen (J/K)'],
                [ok,'判定']
            ]));
        """,
        "notes": ["S_gen = ΔS_sys + ΔS_surr ≥ 0。", "系统 +10、环境 −9 → S_gen=+1。"],
    },
    {
        "slug": "cp-cv-ratio",
        "industry": "thermodynamics",
        "cat": "thermodynamics",
        "icon": "divide",
        "bg": "from-orange-500 to-red-600",
        "title": "比热比 γ 计算器",
        "h1": "γ = c_p / c_v，c_v = c_p − R",
        "h2": "由定压比热求比热比",
        "intro": "输入定压比热 c_p 与气体常数，求定容比热与比热比 γ。",
        "desc": "比热比计算器：输入 cp、R，输出 cv 与 γ。",
        "inputs": [
            {"id": "cp", "label": "定压比热 c_p", "value": "1005", "step": "1", "unit": "J/(kg·K)"},
            {"id": "Rgas", "label": "气体常数 R", "value": "287", "step": "1", "unit": "J/(kg·K)"},
        ],
        "calc": """
            const cp=num('cp'),Rg=num('Rgas');
            const cv=cp-Rg;
            ToolBox.setResult('result', dataGrid([
                [cv.toFixed(1),'定容比热 c_v (J/(kg·K))'],
                [(cp/cv).toFixed(3),'比热比 γ']
            ]));
        """,
        "notes": ["γ = c_p/c_v，c_v = c_p − R。", "空气 cp=1005、R=287 → γ≈1.40。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
