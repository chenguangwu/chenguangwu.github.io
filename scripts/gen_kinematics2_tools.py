# -*- coding: utf-8 -*-
"""Batch 51: 运动学深化 II（14 个公式计算器）。industry=kinematics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "angular-displacement",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "rotate-cw",
        "bg": "from-blue-500 to-indigo-600",
        "title": "角位移计算器",
        "h1": "θ = ω₀t + ½αt²",
        "h2": "由初角速度、角加速度与时间求角位移",
        "intro": "输入初角速度 ω₀、角加速度 α、时间 t，求角位移。", "desc": "角位移计算器：输入 ω₀、α、t，输出 θ(rad)。",
        "inputs": [
            {"id": "w0", "label": "初角速度 ω₀", "value": "2", "step": "0.1", "unit": "rad/s"},
            {"id": "a", "label": "角加速度 α", "value": "1", "step": "0.1", "unit": "rad/s²"},
            {"id": "t", "label": "时间 t", "value": "3", "step": "0.1", "unit": "s"},
        ],
        "calc": """
            const w0=num('w0'),a=num('a'),t=num('t');
            const th=w0*t+0.5*a*t*t;
            ToolBox.setResult('result', dataGrid([
                [th.toFixed(3),'角位移 θ (rad)']
            ]));
        """,
        "notes": ["θ = ω₀t + ½αt²。", "ω₀=2,α=1,t=3 → 10.5 rad。"],
    },
    {
        "slug": "angular-final-velocity",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "rotate-cw",
        "bg": "from-blue-500 to-indigo-600",
        "title": "末角速度计算器",
        "h1": "ω = ω₀ + αt",
        "h2": "由初角速度、角加速度与时间求末角速度",
        "intro": "输入初角速度 ω₀、角加速度 α、时间 t，求末角速度。", "desc": "末角速度计算器：输入 ω₀、α、t，输出 ω(rad/s)。",
        "inputs": [
            {"id": "w0", "label": "初角速度 ω₀", "value": "2", "step": "0.1", "unit": "rad/s"},
            {"id": "a", "label": "角加速度 α", "value": "1", "step": "0.1", "unit": "rad/s²"},
            {"id": "t", "label": "时间 t", "value": "3", "step": "0.1", "unit": "s"},
        ],
        "calc": """
            const w0=num('w0'),a=num('a'),t=num('t');
            const w=w0+a*t;
            ToolBox.setResult('result', dataGrid([
                [w.toFixed(3),'末角速度 ω (rad/s)']
            ]));
        """,
        "notes": ["ω = ω₀ + αt。", "ω₀=2,α=1,t=3 → 5 rad/s。"],
    },
    {
        "slug": "rpm-to-radps",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "gauge",
        "bg": "from-blue-500 to-indigo-600",
        "title": "转速转角速度计算器",
        "h1": "ω = 2π·n / 60",
        "h2": "由每分钟转数求角速度",
        "intro": "输入转速 n（rpm），求角速度 ω（rad/s）。", "desc": "转速转角速度：输入 n(rpm)，输出 ω(rad/s)。",
        "inputs": [{"id": "n", "label": "转速 n", "value": "3000", "step": "100", "unit": "rpm"}],
        "calc": """
            const n=num('n');
            const w=2*Math.PI*n/60;
            ToolBox.setResult('result', dataGrid([
                [w.toFixed(3),'角速度 ω (rad/s)']
            ]));
        """,
        "notes": ["ω = 2πn/60。", "3000 rpm → 314.16 rad/s。"],
    },
    {
        "slug": "tangential-velocity",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "move-right",
        "bg": "from-blue-500 to-indigo-600",
        "title": "切向速度计算器",
        "h1": "v = ω·r",
        "h2": "由角速度与半径求切向速度",
        "intro": "输入角速度 ω 与半径 r，求切向速度。", "desc": "切向速度计算器：输入 ω、r，输出 v(m/s)。",
        "inputs": [
            {"id": "w", "label": "角速度 ω", "value": "10", "step": "0.1", "unit": "rad/s"},
            {"id": "r", "label": "半径 r", "value": "0.5", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const w=num('w'),r=num('r');
            const v=w*r;
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(3),'切向速度 v (m/s)']
            ]));
        """,
        "notes": ["v = ωr。", "ω=10,r=0.5 → 5 m/s。"],
    },
    {
        "slug": "tangential-accel",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "move-right",
        "bg": "from-blue-500 to-indigo-600",
        "title": "切向加速度计算器",
        "h1": "a_t = α·r",
        "h2": "由角加速度与半径求切向加速度",
        "intro": "输入角加速度 α 与半径 r，求切向加速度。", "desc": "切向加速度计算器：输入 α、r，输出 a_t(m/s²)。",
        "inputs": [
            {"id": "a", "label": "角加速度 α", "value": "2", "step": "0.1", "unit": "rad/s²"},
            {"id": "r", "label": "半径 r", "value": "0.5", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const a=num('a'),r=num('r');
            const at=a*r;
            ToolBox.setResult('result', dataGrid([
                [at.toFixed(3),'切向加速度 a_t (m/s²)']
            ]));
        """,
        "notes": ["a_t = αr。", "α=2,r=0.5 → 1 m/s²。"],
    },
    {
        "slug": "period-from-omega",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "clock",
        "bg": "from-blue-500 to-indigo-600",
        "title": "周期计算器",
        "h1": "T = 2π / ω",
        "h2": "由角速度求旋转周期",
        "intro": "输入角速度 ω，求周期 T。", "desc": "周期计算器：输入 ω，输出 T(s)。",
        "inputs": [{"id": "w", "label": "角速度 ω", "value": "6.283", "step": "0.1", "unit": "rad/s"}],
        "calc": """
            const w=num('w');
            const T=2*Math.PI/w;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(4),'周期 T (s)']
            ]));
        """,
        "notes": ["T = 2π/ω。", "ω=2π → T=1 s。"],
    },
    {
        "slug": "freq-from-omega",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "activity",
        "bg": "from-blue-500 to-indigo-600",
        "title": "频率计算器",
        "h1": "f = ω / (2π)",
        "h2": "由角速度求频率",
        "intro": "输入角速度 ω，求频率 f。", "desc": "频率计算器：输入 ω，输出 f(Hz)。",
        "inputs": [{"id": "w", "label": "角速度 ω", "value": "6.283", "step": "0.1", "unit": "rad/s"}],
        "calc": """
            const w=num('w');
            const f=w/(2*Math.PI);
            ToolBox.setResult('result', dataGrid([
                [f.toFixed(4),'频率 f (Hz)']
            ]));
        """,
        "notes": ["f = ω/(2π)。", "ω=2π → f=1 Hz。"],
    },
    {
        "slug": "avg-acceleration",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "trending-up",
        "bg": "from-blue-500 to-indigo-600",
        "title": "平均加速度计算器",
        "h1": "a = (v − v₀) / t",
        "h2": "由速度变化与时间求平均加速度",
        "intro": "输入末速度 v、初速度 v₀、时间 t，求平均加速度。", "desc": "平均加速度计算器：输入 v、v₀、t，输出 a(m/s²)。",
        "inputs": [
            {"id": "v", "label": "末速度 v", "value": "20", "step": "0.5", "unit": "m/s"},
            {"id": "v0", "label": "初速度 v₀", "value": "10", "step": "0.5", "unit": "m/s"},
            {"id": "t", "label": "时间 t", "value": "2", "step": "0.1", "unit": "s"},
        ],
        "calc": """
            const v=num('v'),v0=num('v0'),t=num('t');
            const a=(v-v0)/t;
            ToolBox.setResult('result', dataGrid([
                [a.toFixed(3),'平均加速度 a (m/s²)']
            ]));
        """,
        "notes": ["a = (v−v₀)/t。", "20,10,2s → 5 m/s²。"],
    },
    {
        "slug": "uniform-displacement",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "ruler",
        "bg": "from-blue-500 to-indigo-600",
        "title": "匀速位移计算器",
        "h1": "s = v·t",
        "h2": "由匀速与时间求位移",
        "intro": "输入速度 v 与时间 t，求位移。", "desc": "匀速位移计算器：输入 v、t，输出 s(m)。",
        "inputs": [
            {"id": "v", "label": "速度 v", "value": "5", "step": "0.1", "unit": "m/s"},
            {"id": "t", "label": "时间 t", "value": "10", "step": "0.5", "unit": "s"},
        ],
        "calc": """
            const v=num('v'),t=num('t');
            const s=v*t;
            ToolBox.setResult('result', dataGrid([
                [s.toFixed(3),'位移 s (m)']
            ]));
        """,
        "notes": ["s = v·t（匀速）。", "5×10 → 50 m。"],
    },
    {
        "slug": "stopping-time",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "timer",
        "bg": "from-blue-500 to-indigo-600",
        "title": "制动时间计算器",
        "h1": "t = v₀ / a",
        "h2": "由初速度与减速度求制动时间",
        "intro": "输入初速度 v₀ 与减速度 a，求制动时间。", "desc": "制动时间计算器：输入 v₀、a，输出 t(s)。",
        "inputs": [
            {"id": "v0", "label": "初速度 v₀", "value": "20", "step": "0.5", "unit": "m/s"},
            {"id": "a", "label": "减速度 a", "value": "5", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const v0=num('v0'),a=num('a');
            const t=v0/a;
            ToolBox.setResult('result', dataGrid([
                [t.toFixed(3),'制动时间 t (s)']
            ]));
        """,
        "notes": ["t = v₀/a。", "20/5 → 4 s。"],
    },
    {
        "slug": "displacement-va",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "ruler",
        "bg": "from-blue-500 to-indigo-600",
        "title": "匀变速位移(已知v,v₀,a)计算器",
        "h1": "s = (v² − v₀²) / (2a)",
        "h2": "由速度变化与加速度求位移",
        "intro": "输入末速度 v、初速度 v₀、加速度 a，求位移。", "desc": "匀变速位移计算器：输入 v、v₀、a，输出 s(m)。",
        "inputs": [
            {"id": "v", "label": "末速度 v", "value": "20", "step": "0.5", "unit": "m/s"},
            {"id": "v0", "label": "初速度 v₀", "value": "10", "step": "0.5", "unit": "m/s"},
            {"id": "a", "label": "加速度 a", "value": "5", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const v=num('v'),v0=num('v0'),a=num('a');
            const s=(v*v-v0*v0)/(2*a);
            ToolBox.setResult('result', dataGrid([
                [s.toFixed(3),'位移 s (m)']
            ]));
        """,
        "notes": ["s = (v²−v₀²)/(2a)。", "20,10,5 → 30 m。"],
    },
    {
        "slug": "relative-velocity-1d",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "move-right",
        "bg": "from-blue-500 to-indigo-600",
        "title": "一维相对速度计算器",
        "h1": "v_rel = v₁ − v₂",
        "h2": "由两物体速度求相对速度",
        "intro": "输入两物体速度 v₁、v₂，求相对速度。", "desc": "相对速度计算器：输入 v₁、v₂，输出 v_rel(m/s)。",
        "inputs": [
            {"id": "v1", "label": "速度 v₁", "value": "30", "step": "1", "unit": "m/s"},
            {"id": "v2", "label": "速度 v₂", "value": "20", "step": "1", "unit": "m/s"},
        ],
        "calc": """
            const v1=num('v1'),v2=num('v2');
            const vr=v1-v2;
            ToolBox.setResult('result', dataGrid([
                [vr.toFixed(3),'相对速度 v_rel (m/s)']
            ]));
        """,
        "notes": ["v_rel = v₁−v₂（同方向）。", "30−20 → 10 m/s。"],
    },
    {
        "slug": "projectile-velocity-components",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "crosshair",
        "bg": "from-blue-500 to-indigo-600",
        "title": "抛射速度分量计算器",
        "h1": "vₓ = v·cosθ, vᵧ = v·sinθ",
        "h2": "由初速与仰角求水平竖直分量",
        "intro": "输入初速度 v 与仰角 θ，求水平与竖直分量。", "desc": "抛射速度分量计算器：输入 v、θ，输出 vₓ、vᵧ。",
        "inputs": [
            {"id": "v", "label": "初速度 v", "value": "20", "step": "0.5", "unit": "m/s"},
            {"id": "th", "label": "仰角 θ", "value": "30", "step": "1", "unit": "°"},
        ],
        "calc": """
            const v=num('v'),th=num('th');
            const vx=v*Math.cos(th*Math.PI/180), vy=v*Math.sin(th*Math.PI/180);
            ToolBox.setResult('result', dataGrid([
                [vx.toFixed(3),'水平分量 vₓ (m/s)'],
                [vy.toFixed(3),'竖直分量 vᵧ (m/s)']
            ]));
        """,
        "notes": ["vₓ=v·cosθ, vᵧ=v·sinθ。", "v=20,θ=30° → 17.32 / 10。"],
    },
    {
        "slug": "height-fall-distance",
        "industry": "kinematics",
        "cat": "kinematics",
        "icon": "arrow-down",
        "bg": "from-blue-500 to-indigo-600",
        "title": "自由落体下落距离计算器",
        "h1": "h = ½gt²",
        "h2": "由下落时间求下落距离",
        "intro": "输入下落时间 t 与重力加速度 g，求下落距离。", "desc": "自由落体下落距离：输入 t、g，输出 h(m)。",
        "inputs": [
            {"id": "t", "label": "时间 t", "value": "2", "step": "0.1", "unit": "s"},
            {"id": "g", "label": "重力加速度 g", "value": "9.81", "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const t=num('t'),g=num('g');
            const h=0.5*g*t*t;
            ToolBox.setResult('result', dataGrid([
                [h.toFixed(3),'下落距离 h (m)']
            ]));
        """,
        "notes": ["h = ½gt²（无初速）。", "t=2,g=9.81 → 19.62 m。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
