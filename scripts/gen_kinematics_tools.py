# -*- coding: utf-8 -*-
"""Batch 21: 运动学计算深化（14 个公式计算器）。industry=kinematics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "avg-velocity", "industry": "kinematics", "cat": "kinematics", "icon": "🏃", "bg": "#ecfeff",
        "title": "平均速度", "h1": "平均速度计算器",
        "h2": "平均速度（v̄ = Δx / Δt）",
        "intro": "位移变化量与所用时间之比。",
        "desc": "平均速度计算器：v̄ = Δx/Δt，输入位移与时间。",
        "inputs": [
            {"id": "dx", "label": "位移 Δx", "value": "100", "step": "1", "unit": "m"},
            {"id": "dt", "label": "时间 Δt", "value": "10", "step": "0.1", "unit": "s"},
        ],
        "calc": """
            const dx = num('dx'), dt = num('dt');
            const v = dx / dt;
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(3), '平均速度 v̄ (m/s)'],
                [(v * 3.6).toFixed(3), 'v̄ (km/h)']
            ]));
        """,
        "notes": ["v̄ = Δx/Δt。", "100 m / 10 s = 10 m/s = 36 km/h。"],
    },
    {
        "slug": "final-velocity-accel", "industry": "kinematics", "cat": "kinematics", "icon": "🏃", "bg": "#ecfeff",
        "title": "匀加速末速度", "h1": "匀加速末速度计算器",
        "h2": "速度公式（v = v₀ + a·t）",
        "intro": "初速度叠加加速度在时间上的累积。",
        "desc": "匀加速末速度计算器：v = v₀ + a·t，输入初速度、加速度、时间。",
        "inputs": [
            {"id": "v0", "label": "初速度 v₀", "value": "0", "step": "1", "unit": "m/s"},
            {"id": "a", "label": "加速度 a", "value": "9.8", "step": "0.1", "unit": "m/s²"},
            {"id": "t", "label": "时间 t", "value": "5", "step": "0.1", "unit": "s"},
        ],
        "calc": """
            const v0 = num('v0'), a = num('a'), t = num('t');
            const v = v0 + a * t;
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(3), '末速度 v (m/s)'],
                [(v * 3.6).toFixed(3), 'v (km/h)']
            ]));
        """,
        "notes": ["v = v₀ + a·t。", "自由落体 5 s：v = 9.8×5 = 49 m/s。"],
    },
    {
        "slug": "displacement-accel", "industry": "kinematics", "cat": "kinematics", "icon": "🏃", "bg": "#ecfeff",
        "title": "匀加速位移", "h1": "匀加速位移计算器",
        "h2": "位移公式（x = v₀·t + ½·a·t²）",
        "intro": "初速度位移与匀加速位移之和。",
        "desc": "匀加速位移计算器：x = v₀t + ½at²，输入初速度、加速度、时间。",
        "inputs": [
            {"id": "v0", "label": "初速度 v₀", "value": "10", "step": "1", "unit": "m/s"},
            {"id": "a", "label": "加速度 a", "value": "2", "step": "0.1", "unit": "m/s²"},
            {"id": "t", "label": "时间 t", "value": "5", "step": "0.1", "unit": "s"},
        ],
        "calc": """
            const v0 = num('v0'), a = num('a'), t = num('t');
            const x = v0 * t + 0.5 * a * t * t;
            ToolBox.setResult('result', dataGrid([
                [x.toFixed(3), '位移 x (m)']
            ]));
        """,
        "notes": ["x = v₀t + ½at²。", "10×5 + 0.5×2×25 = 75 m。"],
    },
    {
        "slug": "velocity-squared", "industry": "kinematics", "cat": "kinematics", "icon": "🏃", "bg": "#ecfeff",
        "title": "速度位移公式", "h1": "速度位移关系计算器",
        "h2": "v² = v₀² + 2·a·Δx",
        "intro": "不含时间的速度与位移关系。",
        "desc": "速度位移关系计算器：v² = v₀² + 2aΔx，输入初速度、加速度、位移。",
        "inputs": [
            {"id": "v0", "label": "初速度 v₀", "value": "0", "step": "1", "unit": "m/s"},
            {"id": "a", "label": "加速度 a", "value": "9.8", "step": "0.1", "unit": "m/s²"},
            {"id": "dx", "label": "位移 Δx", "value": "100", "step": "1", "unit": "m"},
        ],
        "calc": """
            const v0 = num('v0'), a = num('a'), dx = num('dx');
            const v = Math.sqrt(v0 * v0 + 2 * a * dx);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(3), '末速度 v (m/s)']
            ]));
        """,
        "notes": ["v² = v₀² + 2aΔx。", "0 + 2×9.8×100 → v≈44.27 m/s。"],
    },
    {
        "slug": "free-fall-time", "industry": "kinematics", "cat": "kinematics", "icon": "🍎", "bg": "#ecfeff",
        "title": "自由落体时间", "h1": "自由落体时间计算器",
        "h2": "t = √(2h / g)",
        "intro": "由高度求无初速自由下落时间。",
        "desc": "自由落体时间计算器：t = √(2h/g)，输入高度与重力加速度。",
        "inputs": [
            {"id": "h", "label": "高度 h", "value": "100", "step": "1", "unit": "m"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const h = num('h'), g = num('g');
            const t = Math.sqrt(2 * h / g);
            ToolBox.setResult('result', dataGrid([
                [t.toFixed(3), '下落时间 t (s)'],
                [(g * t).toFixed(3), '触地速度 (m/s)']
            ]));
        """,
        "notes": ["t = √(2h/g)。", "100 m 下落约 4.52 s。"],
    },
    {
        "slug": "projectile-range", "industry": "kinematics", "cat": "kinematics", "icon": "🎯", "bg": "#ecfeff",
        "title": "抛射射程", "h1": "抛射运动射程计算器",
        "h2": "R = v²·sin(2θ) / g",
        "intro": "以倾角 θ 斜抛的水平射程。",
        "desc": "抛射射程计算器：R = v²sin(2θ)/g，输入初速度、角度、重力加速度。",
        "inputs": [
            {"id": "v", "label": "初速度 v", "value": "30", "step": "1", "unit": "m/s"},
            {"id": "deg", "label": "抛射角 θ", "value": "45", "step": "1", "unit": "°"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const v = num('v'), deg = num('deg'), g = num('g');
            const th = deg * Math.PI / 180;
            const R = v * v * Math.sin(2 * th) / g;
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(3), '射程 R (m)']
            ]));
        """,
        "notes": ["R = v²sin(2θ)/g。", "45° 时射程最大：30²/9.8 ≈ 91.84 m。"],
    },
    {
        "slug": "projectile-max-height", "industry": "kinematics", "cat": "kinematics", "icon": "🎯", "bg": "#ecfeff",
        "title": "抛射最大高度", "h1": "抛射最大高度计算器",
        "h2": "H = v²·sin²θ / (2g)",
        "intro": "斜抛达到的竖直最大高度。",
        "desc": "抛射最大高度计算器：H = v²sin²θ/(2g)，输入初速度、角度、重力加速度。",
        "inputs": [
            {"id": "v", "label": "初速度 v", "value": "30", "step": "1", "unit": "m/s"},
            {"id": "deg", "label": "抛射角 θ", "value": "60", "step": "1", "unit": "°"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const v = num('v'), deg = num('deg'), g = num('g');
            const th = deg * Math.PI / 180;
            const H = v * v * Math.sin(th) * Math.sin(th) / (2 * g);
            ToolBox.setResult('result', dataGrid([
                [H.toFixed(3), '最大高度 H (m)']
            ]));
        """,
        "notes": ["H = v²sin²θ/(2g)。", "30 m/s、60° → H ≈ 34.4 m。"],
    },
    {
        "slug": "projectile-time-flight", "industry": "kinematics", "cat": "kinematics", "icon": "🎯", "bg": "#ecfeff",
        "title": "抛射飞行时间", "h1": "抛射飞行时间计算器",
        "h2": "T = 2v·sinθ / g",
        "intro": "回到同一水平面的总飞行时间。",
        "desc": "抛射飞行时间计算器：T = 2v·sinθ/g，输入初速度、角度、重力加速度。",
        "inputs": [
            {"id": "v", "label": "初速度 v", "value": "30", "step": "1", "unit": "m/s"},
            {"id": "deg", "label": "抛射角 θ", "value": "45", "step": "1", "unit": "°"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const v = num('v'), deg = num('deg'), g = num('g');
            const th = deg * Math.PI / 180;
            const T = 2 * v * Math.sin(th) / g;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(3), '飞行时间 T (s)']
            ]));
        """,
        "notes": ["T = 2v·sinθ/g。", "30 m/s、45° → T ≈ 4.33 s。"],
    },
    {
        "slug": "centripetal-accel", "industry": "kinematics", "cat": "kinematics", "icon": "🔄", "bg": "#ecfeff",
        "title": "向心加速度", "h1": "向心加速度计算器",
        "h2": "a = v² / r",
        "intro": "匀速圆周运动指向圆心的加速度。",
        "desc": "向心加速度计算器：a = v²/r，输入线速度与半径。",
        "inputs": [
            {"id": "v", "label": "线速度 v", "value": "20", "step": "1", "unit": "m/s"},
            {"id": "r", "label": "半径 r", "value": "50", "step": "1", "unit": "m"},
        ],
        "calc": """
            const v = num('v'), r = num('r');
            const a = v * v / r;
            ToolBox.setResult('result', dataGrid([
                [a.toFixed(3), '向心加速度 a (m/s²)']
            ]));
        """,
        "notes": ["a = v²/r。", "20²/50 = 8 m/s²。"],
    },
    {
        "slug": "angular-velocity", "industry": "kinematics", "cat": "kinematics", "icon": "🔄", "bg": "#ecfeff",
        "title": "角速度", "h1": "角速度计算器",
        "h2": "ω = v / r",
        "intro": "线速度与半径之比即角速度。",
        "desc": "角速度计算器：ω = v/r，输入线速度与半径。",
        "inputs": [
            {"id": "v", "label": "线速度 v", "value": "10", "step": "0.5", "unit": "m/s"},
            {"id": "r", "label": "半径 r", "value": "2", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const v = num('v'), r = num('r');
            const w = v / r;
            ToolBox.setResult('result', dataGrid([
                [w.toFixed(3), '角速度 ω (rad/s)'],
                [(w * 60 / (2 * Math.PI)).toFixed(3), '转速 (rpm)']
            ]));
        """,
        "notes": ["ω = v/r。", "10/2 = 5 rad/s ≈ 47.7 rpm。"],
    },
    {
        "slug": "angular-accel", "industry": "kinematics", "cat": "kinematics", "icon": "🔄", "bg": "#ecfeff",
        "title": "角加速度", "h1": "角加速度计算器",
        "h2": "α = Δω / Δt",
        "intro": "角速度变化率。",
        "desc": "角加速度计算器：α = Δω/Δt，输入角速度变化与时间。",
        "inputs": [
            {"id": "dw", "label": "角速度变化 Δω", "value": "10", "step": "0.5", "unit": "rad/s"},
            {"id": "dt", "label": "时间 Δt", "value": "2", "step": "0.1", "unit": "s"},
        ],
        "calc": """
            const dw = num('dw'), dt = num('dt');
            const a = dw / dt;
            ToolBox.setResult('result', dataGrid([
                [a.toFixed(3), '角加速度 α (rad/s²)']
            ]));
        """,
        "notes": ["α = Δω/Δt。", "10/2 = 5 rad/s²。"],
    },
    {
        "slug": "centripetal-force", "industry": "kinematics", "cat": "kinematics", "icon": "🔄", "bg": "#ecfeff",
        "title": "向心力", "h1": "向心力计算器",
        "h2": "F = m·v² / r",
        "intro": "维持圆周运动所需的向心力。",
        "desc": "向心力计算器：F = mv²/r，输入质量、线速度、半径。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "1000", "step": "10", "unit": "kg"},
            {"id": "v", "label": "线速度 v", "value": "20", "step": "1", "unit": "m/s"},
            {"id": "r", "label": "半径 r", "value": "50", "step": "1", "unit": "m"},
        ],
        "calc": """
            const m = num('m'), v = num('v'), r = num('r');
            const F = m * v * v / r;
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(3), '向心力 F (N)'],
                [(F / 1000).toFixed(3), 'F (kN)']
            ]));
        """,
        "notes": ["F = mv²/r。", "1000×20²/50 = 8000 N = 8 kN。"],
    },
    {
        "slug": "relativistic-velocity-add", "industry": "kinematics", "cat": "kinematics", "icon": "🚀", "bg": "#ecfeff",
        "title": "相对论速度叠加", "h1": "相对论速度叠加计算器",
        "h2": "u = (u′ + v) / (1 + u′v/c²)",
        "intro": "高速参考系下的速度合成，永不超光速。",
        "desc": "相对论速度叠加计算器：u = (u′+v)/(1+u′v/c²)，输入两参考系速度与光速。",
        "inputs": [
            {"id": "up", "label": "物体相对速度 u′", "value": "0.6", "step": "0.01", "unit": "c"},
            {"id": "v", "label": "参考系速度 v", "value": "0.6", "step": "0.01", "unit": "c"},
            {"id": "c", "label": "光速 c", "value": "3e8", "step": "1e7", "unit": "m/s"},
        ],
        "calc": """
            const up = num('up'), v = num('v'), c = num('c');
            const u = (up + v) / (1 + up * v);  // 以 c 为单位
            ToolBox.setResult('result', dataGrid([
                [u.toFixed(6), '合成速度 u (c)'],
                [(u * c).toExponential(3), 'u (m/s)']
            ]));
        """,
        "notes": ["u = (u′+v)/(1+u′v/c²)。", "0.6c+0.6c → 0.882c（亚光速）。"],
    },
    {
        "slug": "stopping-distance", "industry": "kinematics", "cat": "kinematics", "icon": "🛑", "bg": "#ecfeff",
        "title": "刹车制动距离", "h1": "刹车制动距离计算器",
        "h2": "d = v₀·t_r + v₀² / (2a)",
        "intro": "反应距离叠加减速制动距离。",
        "desc": "刹车制动距离计算器：d = v₀·t_r + v₀²/(2a)，输入初速度、反应时间、减速度。",
        "inputs": [
            {"id": "v0", "label": "初速度 v₀", "value": "27.78", "step": "1", "unit": "m/s"},
            {"id": "tr", "label": "反应时间 t_r", "value": "1", "step": "0.1", "unit": "s"},
            {"id": "a", "label": "减速度 a", "value": "7", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const v0 = num('v0'), tr = num('tr'), a = num('a');
            const d = v0 * tr + v0 * v0 / (2 * a);
            ToolBox.setResult('result', dataGrid([
                [(v0 * tr).toFixed(2), '反应距离 (m)'],
                [(v0 * v0 / (2 * a)).toFixed(2), '制动距离 (m)'],
                [d.toFixed(2), '总停车距离 (m)']
            ]));
        """,
        "notes": ["d = v₀t_r + v₀²/(2a)。", "100 km/h≈27.8 m/s、反应1s、减速度7 → 约 83 m。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
