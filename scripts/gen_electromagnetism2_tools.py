# -*- coding: utf-8 -*-
"""Batch 48: 电磁学深化 II（14 个公式计算器）。industry=electromagnetism。"""
from tool_template import main

TOOLS = [
    {
        "slug": "coulomb-force",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "zap",
        "bg": "from-amber-500 to-orange-600",
        "title": "库仑力计算器",
        "h1": "F = k·q₁q₂ / r²",
        "h2": "由两点电荷与距离求静电力",
        "intro": "输入两电荷 q1、q2（库仑）与距离 r（米），求库仑力大小。", "desc": "库仑力计算器：输入 q1、q2、r，输出 F(N)。",
        "inputs": [
            {"id": "q1", "label": "电荷 q₁", "value": "1e-6", "step": "1e-7", "unit": "C"},
            {"id": "q2", "label": "电荷 q₂", "value": "1e-6", "step": "1e-7", "unit": "C"},
            {"id": "r", "label": "距离 r", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const k=8.987551787e9;
            const q1=num('q1'),q2=num('q2'),r=num('r');
            const F=k*Math.abs(q1*q2)/(r*r);
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(4),'库仑力 F (N)']
            ]));
        """,
        "notes": ["F = k·|q1·q2|/r²，k≈8.99×10⁹。", "q=1µC,r=1m → F≈8.99 N。"],
    },
    {
        "slug": "electric-field-point",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "zap",
        "bg": "from-amber-500 to-orange-600",
        "title": "点电荷场强计算器",
        "h1": "E = k·q / r²",
        "h2": "由点电荷与距离求电场强度",
        "intro": "输入点电荷 q（库仑）与距离 r，求电场强度。", "desc": "点电荷场强计算器：输入 q、r，输出 E(N/C)。",
        "inputs": [
            {"id": "q", "label": "电荷 q", "value": "1e-6", "step": "1e-7", "unit": "C"},
            {"id": "r", "label": "距离 r", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const k=8.987551787e9;
            const q=num('q'),r=num('r');
            const E=k*Math.abs(q)/(r*r);
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(3),'电场强度 E (N/C)']
            ]));
        """,
        "notes": ["E = k·|q|/r²。", "q=1µC,r=1m → 8.99×10³ N/C。"],
    },
    {
        "slug": "electric-potential-point",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "zap",
        "bg": "from-amber-500 to-orange-600",
        "title": "点电荷电势计算器",
        "h1": "V = k·q / r",
        "h2": "由点电荷与距离求电势",
        "intro": "输入点电荷 q 与距离 r，求电势。", "desc": "点电荷电势计算器：输入 q、r，输出 V(V)。",
        "inputs": [
            {"id": "q", "label": "电荷 q", "value": "1e-6", "step": "1e-7", "unit": "C"},
            {"id": "r", "label": "距离 r", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const k=8.987551787e9;
            const q=num('q'),r=num('r');
            const V=k*q/r;
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(3),'电势 V (V)']
            ]));
        """,
        "notes": ["V = k·q/r（取无穷远为0）。", "q=1µC,r=1m → 8.99×10³ V。"],
    },
    {
        "slug": "capacitance-parallel-plate",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "layers",
        "bg": "from-amber-500 to-orange-600",
        "title": "平行板电容计算器",
        "h1": "C = ε₀εr·A / d",
        "h2": "由极板面积与间距求电容",
        "intro": "输入相对介电常数 εr、极板面积 A、间距 d，求电容。", "desc": "平行板电容计算器：输入 εr、A、d，输出 C(pF)。",
        "inputs": [
            {"id": "er", "label": "相对介电 εr", "value": "1", "step": "0.1", "unit": ""},
            {"id": "A", "label": "极板面积 A", "value": "0.01", "step": "0.001", "unit": "m²"},
            {"id": "d", "label": "间距 d", "value": "1e-3", "step": "1e-4", "unit": "m"},
        ],
        "calc": """
            const eps0=8.854187817e-12;
            const er=num('er'),A=num('A'),d=num('d');
            const C=eps0*er*A/d;
            ToolBox.setResult('result', dataGrid([
                [(C*1e12).toFixed(3),'电容 C (pF)']
            ]));
        """,
        "notes": ["C = ε₀εr·A/d，ε₀≈8.854×10⁻¹²。", "εr=1,A=0.01,d=1mm → 88.5 pF。"],
    },
    {
        "slug": "inductance-solenoid",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "wind",
        "bg": "from-amber-500 to-orange-600",
        "title": "螺线管电感计算器",
        "h1": "L = μ₀N²A / l",
        "h2": "由匝数、截面积与长度求电感",
        "intro": "输入匝数 N、截面积 A、长度 l，求螺线管电感。", "desc": "螺线管电感计算器：输入 N、A、l，输出 L(mH)。",
        "inputs": [
            {"id": "N", "label": "匝数 N", "value": "100", "step": "1", "unit": ""},
            {"id": "A", "label": "截面积 A", "value": "0.01", "step": "0.001", "unit": "m²"},
            {"id": "l", "label": "长度 l", "value": "0.2", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const mu0=4*Math.PI*1e-7;
            const N=num('N'),A=num('A'),l=num('l');
            const L=mu0*N*N*A/l;
            ToolBox.setResult('result', dataGrid([
                [(L*1e3).toFixed(4),'电感 L (mH)']
            ]));
        """,
        "notes": ["L = μ₀N²A/l，μ₀≈4π×10⁻⁷。", "N=100,A=0.01,l=0.2 → 0.628 mH。"],
    },
    {
        "slug": "energy-capacitor",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "battery-charging",
        "bg": "from-amber-500 to-orange-600",
        "title": "电容储能计算器",
        "h1": "E = ½CV²",
        "h2": "由电容与电压求储能",
        "intro": "输入电容 C（法拉）与电压 V，求电场储能。", "desc": "电容储能计算器：输入 C、V，输出 E(µJ)。",
        "inputs": [
            {"id": "C", "label": "电容 C", "value": "1e-6", "step": "1e-7", "unit": "F"},
            {"id": "V", "label": "电压 V", "value": "10", "step": "0.1", "unit": "V"},
        ],
        "calc": """
            const C=num('C'),V=num('V');
            const E=0.5*C*V*V;
            ToolBox.setResult('result', dataGrid([
                [(E*1e6).toFixed(3),'储能 E (µJ)'],
                [E.toExponential(3),'储能 E (J)']
            ]));
        """,
        "notes": ["E = ½CV²。", "C=1µF,V=10 → 50 µJ。"],
    },
    {
        "slug": "energy-inductor",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "battery-charging",
        "bg": "from-amber-500 to-orange-600",
        "title": "电感储能计算器",
        "h1": "E = ½LI²",
        "h2": "由电感与电流求储能",
        "intro": "输入电感 L（亨利）与电流 I，求磁场储能。", "desc": "电感储能计算器：输入 L、I，输出 E(J)。",
        "inputs": [
            {"id": "L", "label": "电感 L", "value": "0.1", "step": "0.01", "unit": "H"},
            {"id": "I", "label": "电流 I", "value": "2", "step": "0.1", "unit": "A"},
        ],
        "calc": """
            const L=num('L'),I=num('I');
            const E=0.5*L*I*I;
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(4),'储能 E (J)']
            ]));
        """,
        "notes": ["E = ½LI²。", "L=0.1H,I=2A → 0.2 J。"],
    },
    {
        "slug": "rl-time-constant",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "clock",
        "bg": "from-amber-500 to-orange-600",
        "title": "RL 时间常数计算器",
        "h1": "τ = L / R",
        "h2": "由电感与电阻求时间常数",
        "intro": "输入电感 L 与电阻 R，求 RL 电路时间常数。", "desc": "RL 时间常数计算器：输入 L、R，输出 τ(s)。",
        "inputs": [
            {"id": "L", "label": "电感 L", "value": "0.1", "step": "0.01", "unit": "H"},
            {"id": "R", "label": "电阻 R", "value": "10", "step": "0.1", "unit": "Ω"},
        ],
        "calc": """
            const L=num('L'),R=num('R');
            const tau=L/R;
            ToolBox.setResult('result', dataGrid([
                [tau.toFixed(4),'时间常数 τ (s)']
            ]));
        """,
        "notes": ["τ = L/R。", "L=0.1H,R=10Ω → 0.01 s。"],
    },
    {
        "slug": "free-space-impedance",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "waves",
        "bg": "from-amber-500 to-orange-600",
        "title": "自由空间波阻抗计算器",
        "h1": "Z₀ = √(μ₀/ε₀)",
        "h2": "求真空电磁波波阻抗",
        "intro": "基于真空磁导率与介电常数，求自由空间波阻抗。", "desc": "自由空间波阻抗计算器：输出 Z₀(Ω)。",
        "inputs": [{"id": "x", "label": "（无需输入）", "value": "0", "step": "1", "unit": ""}],
        "calc": """
            const mu0=4*Math.PI*1e-7, eps0=8.854187817e-12;
            const Z0=Math.sqrt(mu0/eps0);
            ToolBox.setResult('result', dataGrid([
                [Z0.toFixed(2),'波阻抗 Z₀ (Ω)']
            ]));
        """,
        "notes": ["Z₀ = √(μ₀/ε₀) ≈ 376.7 Ω。", "自由空间约 377 Ω。"],
    },
    {
        "slug": "drift-velocity",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "move-right",
        "bg": "from-amber-500 to-orange-600",
        "title": "电子漂移速度计算器",
        "h1": "v_d = I / (n·A·e)",
        "h2": "由电流与材料参数求漂移速度",
        "intro": "输入电流 I、载流子密度 n、截面积 A，求漂移速度。", "desc": "电子漂移速度计算器：输入 I、n、A，输出 v_d(m/s)。",
        "inputs": [
            {"id": "I", "label": "电流 I", "value": "1", "step": "0.1", "unit": "A"},
            {"id": "n", "label": "载流子密度 n", "value": "8.5e28", "step": "1e27", "unit": "m⁻³"},
            {"id": "A", "label": "截面积 A", "value": "1e-6", "step": "1e-7", "unit": "m²"},
        ],
        "calc": """
            const e=1.602176634e-19;
            const I=num('I'),n=num('n'),A=num('A');
            const vd=I/(n*A*e);
            ToolBox.setResult('result', dataGrid([
                [vd.toExponential(3),'漂移速度 v_d (m/s)']
            ]));
        """,
        "notes": ["v_d = I/(n·A·e)，铜 n≈8.5×10²⁸。", "铜导线中 v_d 极小（10⁻⁴ m/s 量级）。"],
    },
    {
        "slug": "resistivity-law",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "ruler",
        "bg": "from-amber-500 to-orange-600",
        "title": "电阻定律计算器",
        "h1": "R = ρL / A",
        "h2": "由电阻率、长度与截面积求电阻",
        "intro": "输入电阻率 ρ、长度 L、截面积 A，求导体电阻。", "desc": "电阻定律计算器：输入 ρ、L、A，输出 R(Ω)。",
        "inputs": [
            {"id": "rho", "label": "电阻率 ρ", "value": "1.68e-8", "step": "1e-9", "unit": "Ω·m"},
            {"id": "L", "label": "长度 L", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "A", "label": "截面积 A", "value": "1e-6", "step": "1e-7", "unit": "m²"},
        ],
        "calc": """
            const rho=num('rho'),L=num('L'),A=num('A');
            const R=rho*L/A;
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(5),'电阻 R (Ω)']
            ]));
        """,
        "notes": ["R = ρL/A。", "铜(ρ=1.68e-8),L=1m,A=1mm² → 0.0168 Ω。"],
    },
    {
        "slug": "current-density",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "activity",
        "bg": "from-amber-500 to-orange-600",
        "title": "电流密度计算器",
        "h1": "J = I / A",
        "h2": "由电流与截面积求电流密度",
        "intro": "输入电流 I 与导体截面积 A，求电流密度。", "desc": "电流密度计算器：输入 I、A，输出 J(A/m²)。",
        "inputs": [
            {"id": "I", "label": "电流 I", "value": "5", "step": "0.1", "unit": "A"},
            {"id": "A", "label": "截面积 A", "value": "1e-6", "step": "1e-7", "unit": "m²"},
        ],
        "calc": """
            const I=num('I'),A=num('A');
            const J=I/A;
            ToolBox.setResult('result', dataGrid([
                [J.toExponential(3),'电流密度 J (A/m²)']
            ]));
        """,
        "notes": ["J = I/A。", "I=5A,A=1mm² → 5×10⁶ A/m²。"],
    },
    {
        "slug": "force-wire-field",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "arrow-right",
        "bg": "from-amber-500 to-orange-600",
        "title": "载流导线安培力计算器",
        "h1": "F = BIL·sinθ",
        "h2": "由磁场、电流与长度求安培力",
        "intro": "输入磁感应强度 B、电流 I、导线长 L 与夹角 θ，求安培力。", "desc": "安培力计算器：输入 B、I、L、θ，输出 F(N)。",
        "inputs": [
            {"id": "B", "label": "磁感应 B", "value": "0.5", "step": "0.1", "unit": "T"},
            {"id": "I", "label": "电流 I", "value": "10", "step": "0.1", "unit": "A"},
            {"id": "L", "label": "导线长 L", "value": "0.2", "step": "0.1", "unit": "m"},
            {"id": "th", "label": "夹角 θ", "value": "90", "step": "1", "unit": "°"},
        ],
        "calc": """
            const B=num('B'),I=num('I'),L=num('L'),th=num('th');
            const F=B*I*L*Math.sin(th*Math.PI/180);
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(4),'安培力 F (N)']
            ]));
        """,
        "notes": ["F = BIL·sinθ，垂直时最大。", "B=0.5T,I=10A,L=0.2m,θ=90° → 1 N。"],
    },
    {
        "slug": "coil-torque",
        "industry": "electromagnetism",
        "cat": "electromagnetism",
        "icon": "rotate-cw",
        "bg": "from-amber-500 to-orange-600",
        "title": "线圈磁力矩计算器",
        "h1": "τ = N I A B·sinθ",
        "h2": "由匝数、电流、面积与磁场求磁力矩",
        "intro": "输入匝数 N、电流 I、面积 A、磁感应 B 与夹角 θ，求磁力矩。", "desc": "线圈磁力矩计算器：输入 N、I、A、B、θ，输出 τ(N·m)。",
        "inputs": [
            {"id": "N", "label": "匝数 N", "value": "200", "step": "1", "unit": ""},
            {"id": "I", "label": "电流 I", "value": "0.5", "step": "0.1", "unit": "A"},
            {"id": "A", "label": "面积 A", "value": "0.01", "step": "0.001", "unit": "m²"},
            {"id": "B", "label": "磁感应 B", "value": "0.1", "step": "0.01", "unit": "T"},
            {"id": "th", "label": "夹角 θ", "value": "90", "step": "1", "unit": "°"},
        ],
        "calc": """
            const N=num('N'),I=num('I'),A=num('A'),B=num('B'),th=num('th');
            const tau=N*I*A*B*Math.sin(th*Math.PI/180);
            ToolBox.setResult('result', dataGrid([
                [tau.toFixed(4),'磁力矩 τ (N·m)']
            ]));
        """,
        "notes": ["τ = N I A B·sinθ。", "N=200,I=0.5A,A=0.01,B=0.1T,θ=90° → 0.1 N·m。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
