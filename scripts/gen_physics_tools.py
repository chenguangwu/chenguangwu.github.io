# -*- coding: utf-8 -*-
"""Batch 10: 物理通用计算深化（industry=science，14 个公式计算器）。

复用 scripts/tool_template.py。所有公式经手算核对。
"""
from tool_template import main

ICON = "⚛️"
BG = "#10b981"
CAT = "calculator"

TOOLS = [
    {
        "slug": "kinetic-energy",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "动能计算器",
        "h1": "动能计算器",
        "h2": "动能 E_k",
        "intro": "由质量与速度，按 E_k = ½mv² 计算物体动能。",
        "desc": "动能计算器：输入质量与速度，按 E=½mv² 求物体动能（焦耳）。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": 10, "step": "0.5", "unit": "kg", "min": "0"},
            {"id": "v", "label": "速度 v", "value": 5, "step": "0.5", "unit": "m/s", "min": "0"},
        ],
        "calc": """
            const m=num('m'), v=num('v');
            const E = 0.5*m*v*v;
            ToolBox.setResult('result', dataGrid([ [E.toFixed(1)+' J', '动能 E_k = ½mv²'] ]));
        """,
        "notes": ["动能与速度平方成正比；参考系依赖。"],
    },
    {
        "slug": "gravitational-potential",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "重力势能计算器",
        "h1": "重力势能计算器",
        "h2": "重力势能 E_p",
        "intro": "由质量、重力加速度与高度，按 E_p = mgh 计算重力势能。",
        "desc": "重力势能计算器：输入质量、重力加速度与高度，按 E=mgh 求重力势能。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": 10, "step": "0.5", "unit": "kg", "min": "0"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
            {"id": "h", "label": "高度 h", "value": 5, "step": "0.5", "unit": "m", "min": "0"},
        ],
        "calc": """
            const m=num('m'), g=num('g'), h=num('h');
            const U = m*g*h;
            ToolBox.setResult('result', dataGrid([ [U.toFixed(1)+' J', '重力势能 E_p = mgh'] ]));
        """,
        "notes": ["势能零点是人为选取的基准面。"],
    },
    {
        "slug": "projectile-range",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "斜抛运动计算器",
        "h1": "斜抛运动计算器",
        "h2": "斜抛射程与最大高度",
        "intro": "由初速度与抛射角，按 R=v²sin(2θ)/g、H=v²sin²θ/(2g) 计算水平射程与最大高度。",
        "desc": "斜抛运动计算器：输入初速度与抛射角，求水平射程与最大高度（忽略空气阻力）。",
        "inputs": [
            {"id": "v", "label": "初速度 v", "value": 20, "step": "1", "unit": "m/s", "min": "0"},
            {"id": "theta", "label": "抛射角 θ", "value": 45, "step": "1", "unit": "°", "min": "0", "max": "90"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const v=num('v'), th=num('theta')*Math.PI/180, g=num('g');
            const R = v*v*Math.sin(2*th)/g;
            const H = v*v*Math.sin(th)*Math.sin(th)/(2*g);
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(2)+' m', '水平射程 R = v²sin(2θ)/g'],
                [H.toFixed(2)+' m', '最大高度 H = v²sin²θ/(2g)']
            ]));
        """,
        "notes": ["45° 抛射角射程最大（同一初速、同高度）。", "忽略空气阻力，实战需修正。"],
    },
    {
        "slug": "centripetal-force",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "向心力计算器",
        "h1": "向心力计算器",
        "h2": "向心力 F_c",
        "intro": "由质量、线速度与曲率半径，按 F = mv²/r 计算匀速圆周运动所需向心力。",
        "desc": "向心力计算器：输入质量、线速度与半径，按 F=mv²/r 求向心力。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": 2, "step": "0.1", "unit": "kg", "min": "0"},
            {"id": "v", "label": "线速度 v", "value": 10, "step": "0.5", "unit": "m/s", "min": "0"},
            {"id": "r", "label": "半径 r", "value": 5, "step": "0.5", "unit": "m", "min": "0"},
        ],
        "calc": """
            const m=num('m'), v=num('v'), r=num('r');
            const F = m*v*v/r;
            ToolBox.setResult('result', dataGrid([ [F.toFixed(1)+' N', '向心力 F = mv²/r'] ]));
        """,
        "notes": ["向心力指向圆心，由合外力提供；并非独立新力。"],
    },
    {
        "slug": "hookes-law",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "胡克定律计算器",
        "h1": "胡克定律计算器",
        "h2": "胡克定律 F = kx",
        "intro": "由弹簧刚度与形变量，按 F = kx 计算弹簧恢复力（弹性力）。",
        "desc": "胡克定律计算器：输入弹簧刚度系数与伸长量，按 F=kx 求弹簧力。",
        "inputs": [
            {"id": "k", "label": "刚度系数 k", "value": 100, "step": "5", "unit": "N/m", "min": "0"},
            {"id": "x", "label": "形变量 x", "value": 0.2, "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const k=num('k'), x=num('x');
            const F = k*x;
            ToolBox.setResult('result', dataGrid([ [F.toFixed(1)+' N', '弹簧力 F = k·x'] ]));
        """,
        "notes": ["仅在弹性限度内成立；超出后非线性。"],
    },
    {
        "slug": "pendulum-period",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "单摆周期计算器",
        "h1": "单摆周期计算器",
        "h2": "单摆周期 T",
        "intro": "由摆长与重力加速度，按 T = 2π√(L/g) 计算小角度单摆周期。",
        "desc": "单摆周期计算器：输入摆长与重力加速度，按 T=2π√(L/g) 求单摆周期。",
        "inputs": [
            {"id": "L", "label": "摆长 L", "value": 1, "step": "0.05", "unit": "m", "min": "0"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const L=num('L'), g=num('g');
            const T = 2*Math.PI*Math.sqrt(L/g);
            ToolBox.setResult('result', dataGrid([ [T.toFixed(3)+' s', '周期 T = 2π√(L/g)'] ]));
        """,
        "notes": ["适用条件：小角度（θ<5°~10°）；与摆球质量无关。"],
    },
    {
        "slug": "spring-oscillation-period",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "弹簧振子周期计算器",
        "h1": "弹簧振子周期计算器",
        "h2": "简谐振动周期 T",
        "intro": "由质量与弹簧刚度，按 T = 2π√(m/k) 计算弹簧振子周期。",
        "desc": "弹簧振子周期计算器：输入质量与弹簧刚度，按 T=2π√(m/k) 求简谐振动周期。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": 0.5, "step": "0.05", "unit": "kg", "min": "0"},
            {"id": "k", "label": "刚度系数 k", "value": 50, "step": "2", "unit": "N/m", "min": "0"},
        ],
        "calc": """
            const m=num('m'), k=num('k');
            const T = 2*Math.PI*Math.sqrt(m/k);
            ToolBox.setResult('result', dataGrid([ [T.toFixed(3)+' s', '周期 T = 2π√(m/k)'] ]));
        """,
        "notes": ["频率 f = 1/T；与圆频率 ω=√(k/m) 关系为 T=2π/ω。"],
    },
    {
        "slug": "doppler-effect",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "多普勒效应计算器",
        "h1": "多普勒效应计算器",
        "h2": "声波多普勒频移",
        "intro": "由波速、源频率、观察者速度与波源速度，按 f' = f(v+v_o)/(v-v_s) 计算接近时的观测频率。",
        "desc": "多普勒效应计算器：输入波速、源频率、观察者速度与波源速度，求接近时的观测频率。",
        "inputs": [
            {"id": "f", "label": "源频率 f", "value": 1000, "step": "10", "unit": "Hz", "min": "0"},
            {"id": "v", "label": "波速 v", "value": 343, "step": "1", "unit": "m/s", "min": "0"},
            {"id": "vo", "label": "观察者速度 v₀（朝向源为正）", "value": 0, "step": "1", "unit": "m/s"},
            {"id": "vs", "label": "波源速度 v_s（朝向观察者为正）", "value": 20, "step": "1", "unit": "m/s"},
        ],
        "calc": """
            const f=num('f'), v=num('v'), vo=num('vo'), vs=num('vs');
            const fp = f*(v+vo)/(v-vs);
            ToolBox.setResult('result', dataGrid([ [fp.toFixed(1)+' Hz', "观测频率 f' = f(v+v₀)/(v-v_s)"] ]));
        """,
        "notes": ["声速约 343 m/s（20℃空气）；波源靠近观察者时频率升高。"],
    },
    {
        "slug": "coulomb-force",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "库仑力计算器",
        "h1": "库仑力（静电力）计算器",
        "h2": "库仑定律",
        "intro": "由两电荷量与距离，按 F = k·q₁q₂/r²（k=8.988×10⁹）计算真空中两点电荷间静电力大小。",
        "desc": "库仑力计算器：输入两电荷量与距离，按库仑定律求真空中静电力大小。",
        "inputs": [
            {"id": "q1", "label": "电荷 q₁", "value": 1, "step": "0.1", "unit": "µC"},
            {"id": "q2", "label": "电荷 q₂", "value": 1, "step": "0.1", "unit": "µC"},
            {"id": "r", "label": "距离 r", "value": 0.1, "step": "0.01", "unit": "m", "min": "0"},
        ],
        "calc": """
            const k=8.988e9, q1=num('q1')*1e-6, q2=num('q2')*1e-6, r=num('r');
            const F = k*q1*q2/(r*r);
            ToolBox.setResult('result', dataGrid([ [F.toFixed(4)+' N', '静电力 F = k·q₁q₂/r²'] ]));
        """,
        "notes": ["k≈8.988×10⁹ N·m²/C²；同号排斥、异号吸引。输入单位为微库仑(µC)。"],
    },
    {
        "slug": "electric-field-point",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "点电荷电场强度计算器",
        "h1": "点电荷电场强度计算器",
        "h2": "电场强度 E",
        "intro": "由点电荷与距离，按 E = k·q/r²（k=8.988×10⁹）计算真空中该点电场强度。",
        "desc": "点电荷电场强度计算器：输入电荷量与距离，求点电荷在真空中的电场强度。",
        "inputs": [
            {"id": "q", "label": "电荷 q", "value": 1, "step": "0.1", "unit": "µC"},
            {"id": "r", "label": "距离 r", "value": 0.1, "step": "0.01", "unit": "m", "min": "0"},
        ],
        "calc": """
            const k=8.988e9, q=num('q')*1e-6, r=num('r');
            const E = k*q/(r*r);
            ToolBox.setResult('result', dataGrid([ [E.toFixed(1)+' N/C', '电场强度 E = k·q/r²'] ]));
        """,
        "notes": ["电场方向沿径向：正电荷向外、负电荷向内。输入单位为微库仑(µC)。"],
    },
    {
        "slug": "newtons-second",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "牛顿第二定律计算器",
        "h1": "牛顿第二定律计算器",
        "h2": "牛顿第二定律 F = ma",
        "intro": "由质量与加速度，按 F = ma 计算合外力。",
        "desc": "牛顿第二定律计算器：输入质量与加速度，按 F=ma 求物体所受合外力。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": 10, "step": "0.5", "unit": "kg", "min": "0"},
            {"id": "a", "label": "加速度 a", "value": 3, "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const m=num('m'), a=num('a');
            const F = m*a;
            ToolBox.setResult('result', dataGrid([ [F.toFixed(1)+' N', '合外力 F = m·a'] ]));
        """,
        "notes": ["a 与合外力同向；质量单位为 kg、加速度 m/s² 时结果单位为 N。"],
    },
    {
        "slug": "work-done",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "做功计算器",
        "h1": "恒力做功计算器",
        "h2": "功 W = F·d·cosθ",
        "intro": "由力的大小、位移与夹角，按 W = F·d·cosθ 计算恒力所做的功。",
        "desc": "做功计算器：输入力、位移与力和位移夹角，按 W=Fdcosθ 求功。",
        "inputs": [
            {"id": "F", "label": "力 F", "value": 50, "step": "1", "unit": "N", "min": "0"},
            {"id": "d", "label": "位移 d", "value": 10, "step": "0.5", "unit": "m", "min": "0"},
            {"id": "theta", "label": "夹角 θ", "value": 0, "step": "1", "unit": "°", "min": "0", "max": "180"},
        ],
        "calc": """
            const F=num('F'), d=num('d'), th=num('theta')*Math.PI/180;
            const W = F*d*Math.cos(th);
            ToolBox.setResult('result', dataGrid([ [W.toFixed(1)+' J', '功 W = F·d·cosθ'] ]));
        """,
        "notes": ["θ=90° 时力不做功；力与位移反向（θ=180°）时做功为负。"],
    },
    {
        "slug": "mechanical-power",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "机械功率计算器",
        "h1": "机械功率计算器",
        "h2": "功率 P = F·v",
        "intro": "由力与速度（同向），按 P = F·v 计算机械功率。",
        "desc": "机械功率计算器：输入力与速度，按 P=Fv 求机械功率（瓦特）。",
        "inputs": [
            {"id": "F", "label": "力 F", "value": 100, "step": "5", "unit": "N", "min": "0"},
            {"id": "v", "label": "速度 v", "value": 5, "step": "0.5", "unit": "m/s", "min": "0"},
        ],
        "calc": """
            const F=num('F'), v=num('v');
            const P = F*v;
            ToolBox.setResult('result', dataGrid([ [P.toFixed(0)+' W', '功率 P = F·v'] ]));
        """,
        "notes": ["亦可用 P = W/t；单位 W = J/s。"],
    },
    {
        "slug": "density-physics",
        "industry": "science", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "密度计算器",
        "h1": "密度计算器",
        "h2": "密度 ρ = m/V",
        "intro": "由质量与体积，按 ρ = m/V 计算物质密度。",
        "desc": "密度计算器：输入质量与体积，按 ρ=m/V 求物质密度（kg/m³）。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": 2, "step": "0.1", "unit": "kg", "min": "0"},
            {"id": "V", "label": "体积 V", "value": 0.001, "step": "0.0001", "unit": "m³", "min": "0"},
        ],
        "calc": """
            const m=num('m'), V=num('V');
            const rho = m/V;
            ToolBox.setResult('result', dataGrid([ [rho.toFixed(0)+' kg/m³', '密度 ρ = m/V'] ]));
        """,
        "notes": ["水的密度约 1000 kg/m³；可用作物质识别参考。"],
    },
]


if __name__ == "__main__":
    main(TOOLS)
