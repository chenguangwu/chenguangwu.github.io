# -*- coding: utf-8 -*-
"""Batch 54: 动力学深化 II（14 个公式计算器）。industry=dynamics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "angular-momentum",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "rotate-cw",
        "bg": "from-cyan-500 to-blue-600",
        "title": "角动量计算器",
        "h1": "L = I·ω",
        "h2": "由转动惯量与角速度求角动量",
        "intro": "输入转动惯量 I 与角速度 ω，求角动量。", "desc": "角动量计算器：输入 I、ω，输出 L(kg·m²/s)。",
        "inputs": [
            {"id": "I", "label": "转动惯量 I", "value": "0.5", "step": "0.1", "unit": "kg·m²"},
            {"id": "w", "label": "角速度 ω", "value": "10", "step": "0.5", "unit": "rad/s"},
        ],
        "calc": """
            const I=num('I'),w=num('w');
            const L=I*w;
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(3),'角动量 L (kg·m²/s)']
            ]));
        """,
        "notes": ["L = I·ω。", "I=0.5,ω=10 → 5 kg·m²/s。"],
    },
    {
        "slug": "rotational-kinetic-energy",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "zap",
        "bg": "from-cyan-500 to-blue-600",
        "title": "转动动能计算器",
        "h1": "E = ½Iω²",
        "h2": "由转动惯量与角速度求转动动能",
        "intro": "输入转动惯量 I 与角速度 ω，求转动动能。", "desc": "转动动能计算器：输入 I、ω，输出 E(J)。",
        "inputs": [
            {"id": "I", "label": "转动惯量 I", "value": "0.5", "step": "0.1", "unit": "kg·m²"},
            {"id": "w", "label": "角速度 ω", "value": "10", "step": "0.5", "unit": "rad/s"},
        ],
        "calc": """
            const I=num('I'),w=num('w');
            const E=0.5*I*w*w;
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(3),'转动动能 E (J)']
            ]));
        """,
        "notes": ["E = ½Iω²。", "I=0.5,ω=10 → 25 J。"],
    },
    {
        "slug": "moment-of-inertia-point",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "circle",
        "bg": "from-cyan-500 to-blue-600",
        "title": "质点转动惯量计算器",
        "h1": "I = m·r²",
        "h2": "由质量与半径求质点转动惯量",
        "intro": "输入质量 m 与回转半径 r，求转动惯量。", "desc": "质点转动惯量：输入 m、r，输出 I(kg·m²)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "2", "step": "0.1", "unit": "kg"},
            {"id": "r", "label": "半径 r", "value": "0.5", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const m=num('m'),r=num('r');
            const I=m*r*r;
            ToolBox.setResult('result', dataGrid([
                [I.toFixed(3),'转动惯量 I (kg·m²)']
            ]));
        """,
        "notes": ["I = mr²。", "m=2,r=0.5 → 0.5 kg·m²。"],
    },
    {
        "slug": "drag-force",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "wind",
        "bg": "from-cyan-500 to-blue-600",
        "title": "空气阻力计算器",
        "h1": "F_d = ½ρv²C_dA",
        "h2": "由流体密度、速度与迎风面积求阻力",
        "intro": "输入空气密度 ρ、速度 v、阻力系数 Cd、面积 A，求阻力。", "desc": "空气阻力：输入 ρ、v、Cd、A，输出 F_d(N)。",
        "inputs": [
            {"id": "rho", "label": "密度 ρ", "value": "1.2", "step": "0.1", "unit": "kg/m³"},
            {"id": "v", "label": "速度 v", "value": "30", "step": "1", "unit": "m/s"},
            {"id": "cd", "label": "阻力系数 Cd", "value": "0.3", "step": "0.05", "unit": ""},
            {"id": "A", "label": "面积 A", "value": "0.5", "step": "0.1", "unit": "m²"},
        ],
        "calc": """
            const rho=num('rho'),v=num('v'),cd=num('cd'),A=num('A');
            const Fd=0.5*rho*v*v*cd*A;
            ToolBox.setResult('result', dataGrid([
                [Fd.toFixed(2),'阻力 F_d (N)']
            ]));
        """,
        "notes": ["F_d = ½ρv²C_dA。", "示例 → 81 N。"],
    },
    {
        "slug": "terminal-velocity",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "arrow-down",
        "bg": "from-cyan-500 to-blue-600",
        "title": "终端速度计算器",
        "h1": "v_t = √(2mg / (ρC_dA))",
        "h2": "由重力与阻力平衡求终端速度",
        "intro": "输入质量 m、g、ρ、Cd、A，求终端速度。", "desc": "终端速度：输入 m、g、ρ、Cd、A，输出 v_t(m/s)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "80", "step": "1", "unit": "kg"},
            {"id": "g", "label": "重力加速度 g", "value": "9.81", "step": "0.01", "unit": "m/s²"},
            {"id": "rho", "label": "密度 ρ", "value": "1.2", "step": "0.1", "unit": "kg/m³"},
            {"id": "cd", "label": "阻力系数 Cd", "value": "1.0", "step": "0.1", "unit": ""},
            {"id": "A", "label": "面积 A", "value": "0.7", "step": "0.1", "unit": "m²"},
        ],
        "calc": """
            const m=num('m'),g=num('g'),rho=num('rho'),cd=num('cd'),A=num('A');
            const vt=Math.sqrt(2*m*g/(rho*cd*A));
            ToolBox.setResult('result', dataGrid([
                [vt.toFixed(2),'终端速度 v_t (m/s)']
            ]));
        """,
        "notes": ["mg = ½ρv²C_dA 时达到终端速度。", "示例 → 约 43.2 m/s。"],
    },
    {
        "slug": "coefficient-restitution",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "repeat",
        "bg": "from-cyan-500 to-blue-600",
        "title": "恢复系数计算器",
        "h1": "e = (v₂′−v₁′) / (v₁−v₂)",
        "h2": "由碰撞前后速度求恢复系数",
        "intro": "输入碰撞前后两物体速度，求恢复系数。", "desc": "恢复系数：输入 v₁、v₂、v₁′、v₂′，输出 e。",
        "inputs": [
            {"id": "v1", "label": "碰前 v₁", "value": "5", "step": "0.5", "unit": "m/s"},
            {"id": "v2", "label": "碰前 v₂", "value": "0", "step": "0.5", "unit": "m/s"},
            {"id": "v1p", "label": "碰后 v₁′", "value": "2", "step": "0.5", "unit": "m/s"},
            {"id": "v2p", "label": "碰后 v₂′", "value": "3", "step": "0.5", "unit": "m/s"},
        ],
        "calc": """
            const v1=num('v1'),v2=num('v2'),v1p=num('v1p'),v2p=num('v2p');
            const e=(v2p-v1p)/(v1-v2);
            ToolBox.setResult('result', dataGrid([
                [e.toFixed(3),'恢复系数 e']
            ]));
        """,
        "notes": ["e=1 完全弹性，e=0 完全非弹性。", "5,0→2,3 → e=0.2。"],
    },
    {
        "slug": "elastic-collision-1d",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "repeat",
        "bg": "from-cyan-500 to-blue-600",
        "title": "一维弹性碰撞计算器",
        "h1": "v₁′=(m₁−m₂)v₁/(m₁+m₂)+2m₂v₂/(m₁+m₂)",
        "h2": "由质量与碰前速度求碰后速度",
        "intro": "输入两质量与碰前速度，求碰后速度。", "desc": "一维弹性碰撞：输入 m₁、m₂、v₁、v₂，输出 v₁′、v₂′。",
        "inputs": [
            {"id": "m1", "label": "质量 m₁", "value": "2", "step": "0.1", "unit": "kg"},
            {"id": "m2", "label": "质量 m₂", "value": "1", "step": "0.1", "unit": "kg"},
            {"id": "v1", "label": "碰前 v₁", "value": "4", "step": "0.5", "unit": "m/s"},
            {"id": "v2", "label": "碰前 v₂", "value": "0", "step": "0.5", "unit": "m/s"},
        ],
        "calc": """
            const m1=num('m1'),m2=num('m2'),v1=num('v1'),v2=num('v2');
            const s=m1+m2;
            const v1p=(m1-m2)*v1/s+2*m2*v2/s;
            const v2p=2*m1*v1/s-(m1-m2)*v2/s;
            ToolBox.setResult('result', dataGrid([
                [v1p.toFixed(3),'碰后速度 v₁′ (m/s)'],
                [v2p.toFixed(3),'碰后速度 v₂′ (m/s)']
            ]));
        """,
        "notes": ["动量、动能均守恒。", "2kg,4m/s 撞 1kg 静止 → v₁′=1.33, v₂′=5.33 m/s。"],
    },
    {
        "slug": "banked-curve",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "curve",
        "bg": "from-cyan-500 to-blue-600",
        "title": "弯道设计速度计算器",
        "h1": "v = √(r·g·tanθ)",
        "h2": "由弯道半径与倾角求无摩擦设计速度",
        "intro": "输入弯道半径 r、倾角 θ、g，求设计速度。", "desc": "弯道设计速度：输入 r、θ、g，输出 v(m/s)。",
        "inputs": [
            {"id": "r", "label": "半径 r", "value": "50", "step": "1", "unit": "m"},
            {"id": "th", "label": "倾角 θ", "value": "30", "step": "1", "unit": "°"},
            {"id": "g", "label": "重力加速度 g", "value": "9.81", "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const r=num('r'),th=num('th'),g=num('g');
            const v=Math.sqrt(r*g*Math.tan(th*Math.PI/180));
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(2),'设计速度 v (m/s)']
            ]));
        """,
        "notes": ["v = √(rg·tanθ)（无侧滑）。", "r=50,θ=30° → 约 16.8 m/s。"],
    },
    {
        "slug": "period-pendulum",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "clock",
        "bg": "from-cyan-500 to-blue-600",
        "title": "单摆周期计算器",
        "h1": "T = 2π√(L/g)",
        "h2": "由摆长求单摆周期",
        "intro": "输入摆长 L 与重力加速度 g，求周期。", "desc": "单摆周期：输入 L、g，输出 T(s)。",
        "inputs": [
            {"id": "L", "label": "摆长 L", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "g", "label": "重力加速度 g", "value": "9.81", "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const L=num('L'),g=num('g');
            const T=2*Math.PI*Math.sqrt(L/g);
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(3),'周期 T (s)']
            ]));
        """,
        "notes": ["T = 2π√(L/g)（小角度）。", "L=1m,g=9.81 → 约 2.01 s。"],
    },
    {
        "slug": "power-rotational",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "zap",
        "bg": "from-cyan-500 to-blue-600",
        "title": "旋转功率计算器",
        "h1": "P = τ·ω",
        "h2": "由扭矩与角速度求旋转功率",
        "intro": "输入扭矩 τ 与角速度 ω，求旋转功率。", "desc": "旋转功率：输入 τ、ω，输出 P(W)。",
        "inputs": [
            {"id": "tau", "label": "扭矩 τ", "value": "10", "step": "0.5", "unit": "N·m"},
            {"id": "w", "label": "角速度 ω", "value": "5", "step": "0.5", "unit": "rad/s"},
        ],
        "calc": """
            const tau=num('tau'),w=num('w');
            const P=tau*w;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2),'旋转功率 P (W)']
            ]));
        """,
        "notes": ["P = τ·ω。", "τ=10,ω=5 → 50 W。"],
    },
    {
        "slug": "angular-momentum-conservation",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "rotate-cw",
        "bg": "from-cyan-500 to-blue-600",
        "title": "角动量守恒计算器",
        "h1": "I₁ω₁ = I₂ω₂",
        "h2": "由初态求末态角速度",
        "intro": "输入初末转动惯量与初角速度，求末角速度。", "desc": "角动量守恒：输入 I₁、ω₁、I₂，输出 ω₂(rad/s)。",
        "inputs": [
            {"id": "I1", "label": "初惯量 I₁", "value": "2", "step": "0.1", "unit": "kg·m²"},
            {"id": "w1", "label": "初角速度 ω₁", "value": "10", "step": "0.5", "unit": "rad/s"},
            {"id": "I2", "label": "末惯量 I₂", "value": "1", "step": "0.1", "unit": "kg·m²"},
        ],
        "calc": """
            const I1=num('I1'),w1=num('w1'),I2=num('I2');
            const w2=I1*w1/I2;
            ToolBox.setResult('result', dataGrid([
                [w2.toFixed(3),'末角速度 ω₂ (rad/s)']
            ]));
        """,
        "notes": ["I₁ω₁ = I₂ω₂。", "I:2→1,ω₁=10 → ω₂=20。"],
    },
    {
        "slug": "hooke-force",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "minimize",
        "bg": "from-cyan-500 to-blue-600",
        "title": "弹簧力计算器",
        "h1": "F = k·x",
        "h2": "由劲度系数与形变量求弹力",
        "intro": "输入劲度系数 k 与形变量 x，求弹力大小。", "desc": "弹簧力：输入 k、x，输出 F(N)。",
        "inputs": [
            {"id": "k", "label": "劲度系数 k", "value": "200", "step": "10", "unit": "N/m"},
            {"id": "x", "label": "形变量 x", "value": "0.1", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const k=num('k'),x=num('x');
            const F=k*x;
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(2),'弹力 F (N)']
            ]));
        """,
        "notes": ["F = k·x（大小，方向反向形变）。", "k=200,x=0.1 → 20 N。"],
    },
    {
        "slug": "work-energy-theorem",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "trending-up",
        "bg": "from-cyan-500 to-blue-600",
        "title": "动能定理计算器",
        "h1": "W = ½m(v₂² − v₁²)",
        "h2": "由速度变化求合外力做功",
        "intro": "输入质量与初末速度，求动能变化（合外力功）。", "desc": "动能定理：输入 m、v₁、v₂，输出 W(J)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "2", "step": "0.1", "unit": "kg"},
            {"id": "v1", "label": "初速度 v₁", "value": "0", "step": "0.5", "unit": "m/s"},
            {"id": "v2", "label": "末速度 v₂", "value": "10", "step": "0.5", "unit": "m/s"},
        ],
        "calc": """
            const m=num('m'),v1=num('v1'),v2=num('v2');
            const W=0.5*m*(v2*v2-v1*v1);
            ToolBox.setResult('result', dataGrid([
                [W.toFixed(2),'合外力功 W (J)']
            ]));
        """,
        "notes": ["W = ΔK = ½m(v₂²−v₁²)。", "2kg,0→10 → 100 J。"],
    },
    {
        "slug": "inelastic-collision",
        "industry": "dynamics",
        "cat": "dynamics",
        "icon": "merge",
        "bg": "from-cyan-500 to-blue-600",
        "title": "完全非弹性碰撞计算器",
        "h1": "v = (m₁v₁ + m₂v₂) / (m₁ + m₂)",
        "h2": "由质量与碰前速度求共同速度",
        "intro": "输入两质量与碰前速度，求粘连共同速度。", "desc": "完全非弹性碰撞：输入 m₁、m₂、v₁、v₂，输出 v(m/s)。",
        "inputs": [
            {"id": "m1", "label": "质量 m₁", "value": "2", "step": "0.1", "unit": "kg"},
            {"id": "m2", "label": "质量 m₂", "value": "1", "step": "0.1", "unit": "kg"},
            {"id": "v1", "label": "碰前 v₁", "value": "4", "step": "0.5", "unit": "m/s"},
            {"id": "v2", "label": "碰前 v₂", "value": "0", "step": "0.5", "unit": "m/s"},
        ],
        "calc": """
            const m1=num('m1'),m2=num('m2'),v1=num('v1'),v2=num('v2');
            const v=(m1*v1+m2*v2)/(m1+m2);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(3),'共同速度 v (m/s)']
            ]));
        """,
        "notes": ["动量守恒、动能不守恒。", "2kg·4 + 1kg·0 → 2.67 m/s。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
