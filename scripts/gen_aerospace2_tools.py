# -*- coding: utf-8 -*-
"""Batch 70: 航空航天深化 II（14 个公式计算器）。industry=aerospace。"""
from tool_template import main

TOOLS = [
    {
        "slug": "dynamic-pressure",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "wind",
        "bg": "from-slate-500 to-gray-700",
        "title": "动压计算器",
        "h1": "q = ½·ρ·v²",
        "h2": "由空气密度与速度求动压",
        "intro": "输入空气密度 ρ 与速度 v，求动压。",
        "desc": "动压：输入 ρ、v，输出 q(帕)。",
        "inputs": [
            {"id": "rho", "label": "空气密度 ρ", "value": "1.225", "step": "0.025", "unit": "kg/m³"},
            {"id": "v", "label": "速度 v", "value": "100", "step": "5", "unit": "米/秒"},
        ],
        "calc": """
            const rho=num('rho'),v=num('v');
            const q=0.5*rho*v*v;
            ToolBox.setResult('result', dataGrid([
                [q.toFixed(2),'动压 q (Pa)']
            ]));
        """,
        "notes": ["动压是气动力基础。", "0.5×1.225×10000 → 6125 Pa。"],
    },
    {
        "slug": "drag-force",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "wind",
        "bg": "from-slate-500 to-gray-700",
        "title": "阻力计算器",
        "h1": "D = ½·ρ·v²·C_D·A",
        "h2": "由动压、阻力系数与面积求阻力",
        "intro": "输入空气密度 ρ、速度 v、阻力系数 C_D 与参考面积 A，求阻力。",
        "desc": "阻力：输入 ρ、v、CD、A，输出 D(牛)。",
        "inputs": [
            {"id": "rho", "label": "空气密度 ρ", "value": "1.225", "step": "0.025", "unit": "kg/m³"},
            {"id": "v", "label": "速度 v", "value": "100", "step": "5", "unit": "米/秒"},
            {"id": "CD", "label": "阻力系数 C_D", "value": "0.3", "step": "0.05", "unit": ""},
            {"id": "A", "label": "参考面积 A", "value": "20", "step": "1", "unit": "米²"},
        ],
        "calc": """
            const rho=num('rho'),v=num('v'),CD=num('CD'),A=num('A');
            const D=0.5*rho*v*v*CD*A;
            ToolBox.setResult('result', dataGrid([
                [D.toFixed(2),'阻力 D (N)']
            ]));
        """,
        "notes": ["阻力与速度平方成正比。", "0.5×1.225×10000×0.3×20 → 36750 N。"],
    },
    {
        "slug": "lift-equation",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "arrow-up",
        "bg": "from-slate-500 to-gray-700",
        "title": "升力方程计算器",
        "h1": "L = ½·ρ·v²·C_L·A",
        "h2": "由动压、升力系数与面积求升力",
        "intro": "输入空气密度 ρ、速度 v、升力系数 C_L 与机翼面积 A，求升力。",
        "desc": "升力：输入 ρ、v、CL、A，输出 L(牛)。",
        "inputs": [
            {"id": "rho", "label": "空气密度 ρ", "value": "1.225", "step": "0.025", "unit": "kg/m³"},
            {"id": "v", "label": "速度 v", "value": "100", "step": "5", "unit": "米/秒"},
            {"id": "CL", "label": "升力系数 C_L", "value": "0.5", "step": "0.05", "unit": ""},
            {"id": "A", "label": "机翼面积 A", "value": "20", "step": "1", "unit": "米²"},
        ],
        "calc": """
            const rho=num('rho'),v=num('v'),CL=num('CL'),A=num('A');
            const L=0.5*rho*v*v*CL*A;
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(2),'升力 L (N)']
            ]));
        """,
        "notes": ["升力平衡重力方可平飞。", "0.5×1.225×10000×0.5×20 → 61250 N。"],
    },
    {
        "slug": "thrust-to-weight",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "scale",
        "bg": "from-slate-500 to-gray-700",
        "title": "推重比计算器",
        "h1": "T/W = 推力 / 重量",
        "h2": "由推力与重量求推重比",
        "intro": "输入推力 T 与重量 W，求推重比。",
        "desc": "推重比：输入 T、W，输出 T/W。",
        "inputs": [
            {"id": "T", "label": "推力 T", "value": "50000", "step": "2000", "unit": "牛"},
            {"id": "W", "label": "重量 W", "value": "80000", "step": "2000", "unit": "牛"},
        ],
        "calc": """
            const T=num('T'),W=num('W');
            const tw=T/W;
            ToolBox.setResult('result', dataGrid([
                [tw.toFixed(3),'推重比 T/W']
            ]));
        """,
        "notes": ["T/W>1 才能垂直起降爬升。", "50000/80000 → 0.625。"],
    },
    {
        "slug": "orbital-velocity",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "orbit",
        "bg": "from-slate-500 to-gray-700",
        "title": "圆轨道速度计算器",
        "h1": "v = √(μ / r)",
        "h2": "由引力常数与轨道半径求速度",
        "intro": "输入引力参数 μ 与轨道半径 r，求圆轨道速度。",
        "desc": "圆轨道速度：输入 μ、r，输出 v(米/秒)。",
        "inputs": [
            {"id": "mu", "label": "引力参数 μ", "value": "3.986e14", "step": "1e13", "unit": "m³/s²"},
            {"id": "r", "label": "轨道半径 r", "value": "6.771e6", "step": "1e5", "unit": "米"},
        ],
        "calc": """
            const mu=num('mu'),r=num('r');
            const v=Math.sqrt(mu/r);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(1),'轨道速度 v (m/s)']
            ]));
        """,
        "notes": ["近地轨道约 7.7 km/s。", "√(3.986e14/6.771e6) → 7675 m/s。"],
    },
    {
        "slug": "escape-velocity",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "rocket",
        "bg": "from-slate-500 to-gray-700",
        "title": "逃逸速度计算器",
        "h1": "v = √(2μ / r)",
        "h2": "由引力常数与半径求逃逸速度",
        "intro": "输入引力参数 μ 与天体半径 r，求逃逸速度。",
        "desc": "逃逸速度：输入 μ、r，输出 v(米/秒)。",
        "inputs": [
            {"id": "mu", "label": "引力参数 μ", "value": "3.986e14", "step": "1e13", "unit": "m³/s²"},
            {"id": "r", "label": "半径 r", "value": "6.771e6", "step": "1e5", "unit": "米"},
        ],
        "calc": """
            const mu=num('mu'),r=num('r');
            const v=Math.sqrt(2*mu/r);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(1),'逃逸速度 v (m/s)']
            ]));
        """,
        "notes": ["逃逸速度为圆轨道速度的 √2 倍。", "√(2×3.986e14/6.771e6) → 10854 m/s。"],
    },
    {
        "slug": "centripetal-accel",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "rotate-cw",
        "bg": "from-slate-500 to-gray-700",
        "title": "向心加速度计算器",
        "h1": "a = v² / r",
        "h2": "由速度与转弯半径求向心加速度",
        "intro": "输入速度 v 与转弯半径 r，求向心加速度。",
        "desc": "向心加速度：输入 v、r，输出 a(米/秒²)。",
        "inputs": [
            {"id": "v", "label": "速度 v", "value": "200", "step": "10", "unit": "米/秒"},
            {"id": "r", "label": "半径 r", "value": "3000", "step": "100", "unit": "米"},
        ],
        "calc": """
            const v=num('v'),r=num('r');
            const a=v*v/r;
            ToolBox.setResult('result', dataGrid([
                [a.toFixed(3),'向心加速度 a (m/s²)']
            ]));
        """,
        "notes": ["机动飞行载荷来源。", "200²/3000 → 13.33 m/s²。"],
    },
    {
        "slug": "orbital-period",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "clock",
        "bg": "from-slate-500 to-gray-700",
        "title": "轨道周期计算器",
        "h1": "T = 2π·√(r³ / μ)",
        "h2": "由轨道半径求轨道周期",
        "intro": "输入引力参数 μ 与轨道半径 r，求轨道周期。",
        "desc": "轨道周期：输入 μ、r，输出 T(秒)。",
        "inputs": [
            {"id": "mu", "label": "引力参数 μ", "value": "3.986e14", "step": "1e13", "unit": "m³/s²"},
            {"id": "r", "label": "轨道半径 r", "value": "6.771e6", "step": "1e5", "unit": "米"},
        ],
        "calc": """
            const mu=num('mu'),r=num('r');
            const T=2*Math.PI*Math.sqrt(r*r*r/mu);
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(1),'轨道周期 T (s)']
            ]));
        """,
        "notes": ["近地轨道周期约 90 分钟。", "2π√(r³/μ) → 5543 s。"],
    },
    {
        "slug": "rocket-delta-v",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "rocket",
        "bg": "from-slate-500 to-gray-700",
        "title": "火箭速度增量计算器",
        "h1": "Δv = v_e·ln(m₀ / m_f)",
        "h2": "由比冲等效速度与质量比求 Δv",
        "intro": "输入有效排气速度 v_e、初始质量 m₀ 与末质量 m_f，求速度增量。",
        "desc": "火箭 Δv：输入 ve、m0、mf，输出 Δv(米/秒)。",
        "inputs": [
            {"id": "ve", "label": "排气速度 v_e", "value": "2500", "step": "100", "unit": "米/秒"},
            {"id": "m0", "label": "初始质量 m₀", "value": "100", "step": "5", "unit": "吨"},
            {"id": "mf", "label": "末质量 m_f", "value": "50", "step": "5", "unit": "吨"},
        ],
        "calc": """
            const ve=num('ve'),m0=num('m0'),mf=num('mf');
            const dv=ve*Math.log(m0/mf);
            ToolBox.setResult('result', dataGrid([
                [dv.toFixed(1),'速度增量 Δv (m/s)']
            ]));
        """,
        "notes": ["齐奥尔科夫斯基火箭方程。", "2500×ln2 → 1733 m/s。"],
    },
    {
        "slug": "payload-fraction",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "package",
        "bg": "from-slate-500 to-gray-700",
        "title": "载荷比计算器",
        "h1": "有效载荷比 = (m₀ − m_f) / m₀",
        "h2": "由初始与末质量求有效载荷占比",
        "intro": "输入初始质量 m₀ 与末质量 m_f，求有效载荷比。",
        "desc": "载荷比：输入 m0、mf，输出 (%)。",
        "inputs": [
            {"id": "m0", "label": "初始质量 m₀", "value": "100", "step": "5", "unit": "吨"},
            {"id": "mf", "label": "末质量 m_f", "value": "50", "step": "5", "unit": "吨"},
        ],
        "calc": """
            const m0=num('m0'),mf=num('mf');
            const pf=(m0-mf)/m0*100;
            ToolBox.setResult('result', dataGrid([
                [pf.toFixed(1),'有效载荷比 (%)']
            ]));
        """,
        "notes": ["载荷比越高运输效率越高。", "(100−50)/100 → 50%。"],
    },
    {
        "slug": "aspect-ratio",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "scale",
        "bg": "from-slate-500 to-gray-700",
        "title": "展弦比计算器",
        "h1": "AR = b² / S",
        "h2": "由翼展与机翼面积求展弦比",
        "intro": "输入翼展 b 与机翼面积 S，求展弦比。",
        "desc": "展弦比：输入 b、S，输出 AR。",
        "inputs": [
            {"id": "b", "label": "翼展 b", "value": "10", "step": "0.5", "unit": "米"},
            {"id": "S", "label": "机翼面积 S", "value": "20", "step": "1", "unit": "米²"},
        ],
        "calc": """
            const b=num('b'),S=num('S');
            const AR=b*b/S;
            ToolBox.setResult('result', dataGrid([
                [AR.toFixed(2),'展弦比 AR']
            ]));
        """,
        "notes": ["高展弦比利于滑翔省油。", "10²/20 → 5.0。"],
    },
    {
        "slug": "wing-area-from-loading",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "triangle",
        "bg": "from-slate-500 to-gray-700",
        "title": "翼载荷反算机翼面积计算器",
        "h1": "S = W / (W/S)",
        "h2": "由重量与翼载荷求所需机翼面积",
        "intro": "输入重量 W 与翼载荷 W/S，求机翼面积。",
        "desc": "翼载荷反算：输入 W、WL，输出 S(米²)。",
        "inputs": [
            {"id": "W", "label": "重量 W", "value": "80000", "step": "2000", "unit": "牛"},
            {"id": "WL", "label": "翼载荷 W/S", "value": "4000", "step": "200", "unit": "N/m²"},
        ],
        "calc": """
            const W=num('W'),WL=num('WL');
            const S=W/WL;
            ToolBox.setResult('result', dataGrid([
                [S.toFixed(2),'机翼面积 S (m²)']
            ]));
        """,
        "notes": ["翼载荷影响起降与机动。", "80000/4000 → 20 m²。"],
    },
    {
        "slug": "reynolds-number",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "waves",
        "bg": "from-slate-500 to-gray-700",
        "title": "雷诺数计算器",
        "h1": "Re = ρ·v·L / μ",
        "h2": "由密度、速度、特征长与黏度求雷诺数",
        "intro": "输入空气密度 ρ、速度 v、特征长度 L 与动力黏度 μ，求雷诺数。",
        "desc": "雷诺数：输入 ρ、v、L、μ，输出 Re。",
        "inputs": [
            {"id": "rho", "label": "密度 ρ", "value": "1.225", "step": "0.025", "unit": "kg/m³"},
            {"id": "v", "label": "速度 v", "value": "50", "step": "5", "unit": "米/秒"},
            {"id": "L", "label": "特征长 L", "value": "2", "step": "0.2", "unit": "米"},
            {"id": "mu", "label": "动力黏度 μ", "value": "1.81e-5", "step": "1e-6", "unit": "Pa·s"},
        ],
        "calc": """
            const rho=num('rho'),v=num('v'),L=num('L'),mu=num('mu');
            const Re=rho*v*L/mu;
            ToolBox.setResult('result', dataGrid([
                [Re.toExponential(3),'雷诺数 Re']
            ]));
        """,
        "notes": ["Re 决定层流/湍流状态。", "1.225×50×2/1.81e-5 → 6.77×10⁶。"],
    },
    {
        "slug": "bank-angle-load",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "rotate-cw",
        "bg": "from-slate-500 to-gray-700",
        "title": "坡度载荷因数计算器",
        "h1": "n = 1 / cos(φ)",
        "h2": "由坡度角求机动载荷因数",
        "intro": "输入坡度角 φ（度），求载荷因数。",
        "desc": "坡度载荷因数：输入 φ(度)，输出 n。",
        "inputs": [
            {"id": "phi", "label": "坡度角 φ", "value": "60", "step": "5", "unit": "度"},
        ],
        "calc": """
            const phi=num('phi')*Math.PI/180;
            const n=1/Math.cos(phi);
            ToolBox.setResult('result', dataGrid([
                [n.toFixed(3),'载荷因数 n']
            ]));
        """,
        "notes": ["坡度越大所需升力越大。", "1/cos60° → 2.0。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
