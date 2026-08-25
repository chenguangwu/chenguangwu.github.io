# -*- coding: utf-8 -*-
"""Batch 56: 机器人学深化 II（14 个公式计算器）。industry=robotics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "stepper-step-angle",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "rotate-cw",
        "bg": "from-teal-500 to-emerald-600",
        "title": "步进电机步距角计算器",
        "h1": "θ = 360° / N",
        "h2": "由每转步数求步距角",
        "intro": "输入每转步数 N，求步距角。", "desc": "步进电机步距角：输入 N，输出 θ(°)。",
        "inputs": [{"id": "N", "label": "每转步数 N", "value": "200", "step": "1", "unit": "步/转"}],
        "calc": """
            const N=num('N');
            const th=360/N;
            ToolBox.setResult('result', dataGrid([
                [th.toFixed(3),'步距角 θ (°)']
            ]));
        """,
        "notes": ["θ = 360°/N。", "N=200 → 1.8°（常见）。"],
    },
    {
        "slug": "encoder-angle-resolution",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "target",
        "bg": "from-teal-500 to-emerald-600",
        "title": "编码器角分辨率计算器",
        "h1": "θ_min = 360° / (4·CPR)",
        "h2": "由每转脉冲数求最小角度分辨率",
        "intro": "输入每转脉冲数 CPR（四倍频后），求最小角度分辨率。", "desc": "编码器角分辨率：输入 CPR，输出 θ_min(°)。",
        "inputs": [{"id": "cpr", "label": "每转脉冲 CPR", "value": "1000", "step": "50", "unit": "PPR"}],
        "calc": """
            const cpr=num('cpr');
            const th=360/(4*cpr);
            ToolBox.setResult('result', dataGrid([
                [th.toFixed(4),'角分辨率 θ_min (°)']
            ]));
        """,
        "notes": ["四倍频后分辨率 = 360°/(4·CPR)。", "CPR=1000 → 0.09°。"],
    },
    {
        "slug": "rotational-inertia-torque",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "rotate-cw",
        "bg": "from-teal-500 to-emerald-600",
        "title": "转动惯量加速扭矩计算器",
        "h1": "τ = I·α",
        "h2": "由转动惯量与角加速度求所需扭矩",
        "intro": "输入转动惯量 I 与角加速度 α，求所需扭矩。", "desc": "转动惯量加速扭矩：输入 I、α，输出 τ(N·m)。",
        "inputs": [
            {"id": "I", "label": "转动惯量 I", "value": "0.5", "step": "0.1", "unit": "kg·m²"},
            {"id": "a", "label": "角加速度 α", "value": "4", "step": "0.5", "unit": "rad/s²"},
        ],
        "calc": """
            const I=num('I'),a=num('a');
            const tau=I*a;
            ToolBox.setResult('result', dataGrid([
                [tau.toFixed(2),'所需扭矩 τ (N·m)']
            ]));
        """,
        "notes": ["τ = I·α。", "I=0.5,α=4 → 2 N·m。"],
    },
    {
        "slug": "linear-accel-force",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "move-right",
        "bg": "from-teal-500 to-emerald-600",
        "title": "直线运动加速力计算器",
        "h1": "F = m·a",
        "h2": "由质量与加速度求驱动力",
        "intro": "输入质量 m 与加速度 a，求驱动力。", "desc": "直线运动加速力：输入 m、a，输出 F(N)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "10", "step": "0.5", "unit": "kg"},
            {"id": "a", "label": "加速度 a", "value": "2", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const m=num('m'),a=num('a');
            const F=m*a;
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(2),'驱动力 F (N)']
            ]));
        """,
        "notes": ["F = m·a。", "m=10,a=2 → 20 N。"],
    },
    {
        "slug": "gear-ratio-torque",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "settings",
        "bg": "from-teal-500 to-emerald-600",
        "title": "减速比扭矩放大计算器",
        "h1": "τ_out = τ_in·GR·η",
        "h2": "由输入扭矩与减速比求输出扭矩",
        "intro": "输入输入扭矩 τ_in、减速比 GR、效率 η，求输出扭矩。", "desc": "减速比扭矩放大：输入 τ_in、GR、η，输出 τ_out(N·m)。",
        "inputs": [
            {"id": "ti", "label": "输入扭矩 τ_in", "value": "1", "step": "0.1", "unit": "N·m"},
            {"id": "gr", "label": "减速比 GR", "value": "10", "step": "0.5", "unit": ""},
            {"id": "eta", "label": "效率 η", "value": "0.9", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const ti=num('ti'),gr=num('gr'),eta=num('eta');
            const to=ti*gr*eta;
            ToolBox.setResult('result', dataGrid([
                [to.toFixed(2),'输出扭矩 τ_out (N·m)']
            ]));
        """,
        "notes": ["τ_out = τ_in·GR·η。", "τ_in=1,GR=10,η=0.9 → 9 N·m。"],
    },
    {
        "slug": "gravity-comp-torque",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "rotate-cw",
        "bg": "from-teal-500 to-emerald-600",
        "title": "关节重力补偿扭矩计算器",
        "h1": "τ = m·g·L·cosθ",
        "h2": "由连杆质量、长度与角度求重力扭矩",
        "intro": "输入质量 m、臂长 L、角度 θ、g，求关节重力扭矩。", "desc": "关节重力补偿扭矩：输入 m、L、θ、g，输出 τ(N·m)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "5", "step": "0.5", "unit": "kg"},
            {"id": "L", "label": "臂长 L", "value": "0.3", "step": "0.05", "unit": "m"},
            {"id": "th", "label": "角度 θ", "value": "0", "step": "5", "unit": "°"},
            {"id": "g", "label": "重力加速度 g", "value": "9.81", "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const m=num('m'),L=num('L'),th=num('th'),g=num('g');
            const tau=m*g*L*Math.cos(th*Math.PI/180);
            ToolBox.setResult('result', dataGrid([
                [tau.toFixed(3),'重力扭矩 τ (N·m)']
            ]));
        """,
        "notes": ["τ = m·g·L·cosθ（水平时最大）。", "m=5,L=0.3,θ=0 → 14.7 N·m。"],
    },
    {
        "slug": "trajectory-time-linear",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "timer",
        "bg": "from-teal-500 to-emerald-600",
        "title": "直线运动时间计算器",
        "h1": "t = d / v",
        "h2": "由位移与速度求运动时间",
        "intro": "输入位移 d 与速度 v，求运动时间。", "desc": "直线运动时间：输入 d、v，输出 t(s)。",
        "inputs": [
            {"id": "d", "label": "位移 d", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "v", "label": "速度 v", "value": "0.2", "step": "0.05", "unit": "m/s"},
        ],
        "calc": """
            const d=num('d'),v=num('v');
            const t=d/v;
            ToolBox.setResult('result', dataGrid([
                [t.toFixed(2),'运动时间 t (s)']
            ]));
        """,
        "notes": ["t = d/v（匀速）。", "d=1m,v=0.2m/s → 5 s。"],
    },
    {
        "slug": "cable-tension-pulley",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "minimize",
        "bg": "from-teal-500 to-emerald-600",
        "title": "理想滑轮绳张力计算器",
        "h1": "T = F / 2",
        "h2": "由负载求单侧绳张力",
        "intro": "输入被提升负载 F，求理想定滑轮单侧绳张力。", "desc": "理想滑轮绳张力：输入 F，输出 T(N)。",
        "inputs": [{"id": "F", "label": "负载 F", "value": "100", "step": "5", "unit": "N"}],
        "calc": """
            const F=num('F');
            const T=F/2;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'绳张力 T (N)']
            ]));
        """,
        "notes": ["理想滑轮 T = F/2（两侧均分）。", "F=100N → 50 N。"],
    },
    {
        "slug": "stereo-depth",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "eye",
        "bg": "from-teal-500 to-emerald-600",
        "title": "双目视觉深度计算器",
        "h1": "Z = f·B / d",
        "h2": "由视差求物体深度",
        "intro": "输入焦距 f（像素）、基线 B、视差 d（像素），求深度。", "desc": "双目视觉深度：输入 f、B、d，输出 Z(m)。",
        "inputs": [
            {"id": "f", "label": "焦距 f", "value": "500", "step": "10", "unit": "px"},
            {"id": "B", "label": "基线 B", "value": "0.1", "step": "0.01", "unit": "m"},
            {"id": "d", "label": "视差 d", "value": "25", "step": "1", "unit": "px"},
        ],
        "calc": """
            const f=num('f'),B=num('B'),d=num('d');
            const Z=f*B/d;
            ToolBox.setResult('result', dataGrid([
                [Z.toFixed(3),'深度 Z (m)']
            ]));
        """,
        "notes": ["Z = fB/d（小孔模型）。", "f=500,B=0.1,d=25 → 2 m。"],
    },
    {
        "slug": "motor-power",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "zap",
        "bg": "from-teal-500 to-emerald-600",
        "title": "电机功率计算器",
        "h1": "P = τ·ω",
        "h2": "由扭矩与角速度求机械功率",
        "intro": "输入扭矩 τ 与角速度 ω，求机械功率。", "desc": "电机功率：输入 τ、ω，输出 P(W)。",
        "inputs": [
            {"id": "tau", "label": "扭矩 τ", "value": "2", "step": "0.1", "unit": "N·m"},
            {"id": "w", "label": "角速度 ω", "value": "10", "step": "0.5", "unit": "rad/s"},
        ],
        "calc": """
            const tau=num('tau'),w=num('w');
            const P=tau*w;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2),'机械功率 P (W)']
            ]));
        """,
        "notes": ["P = τ·ω。", "τ=2,ω=10 → 20 W。"],
    },
    {
        "slug": "joint-angular-velocity",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "rotate-cw",
        "bg": "from-teal-500 to-emerald-600",
        "title": "关节角速度计算器",
        "h1": "ω = v / L",
        "h2": "由末端线速度与臂长求关节角速度",
        "intro": "输入末端线速度 v 与臂长 L，求关节角速度。", "desc": "关节角速度：输入 v、L，输出 ω(rad/s)。",
        "inputs": [
            {"id": "v", "label": "末端线速度 v", "value": "0.5", "step": "0.05", "unit": "m/s"},
            {"id": "L", "label": "臂长 L", "value": "0.3", "step": "0.05", "unit": "m"},
        ],
        "calc": """
            const v=num('v'),L=num('L');
            const w=v/L;
            ToolBox.setResult('result', dataGrid([
                [w.toFixed(3),'角速度 ω (rad/s)']
            ]));
        """,
        "notes": ["ω = v/L。", "v=0.5,L=0.3 → 1.667 rad/s。"],
    },
    {
        "slug": "dc-motor-back-emf",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "zap",
        "bg": "from-teal-500 to-emerald-600",
        "title": "直流电机反电动势计算器",
        "h1": "E = k_e·ω",
        "h2": "由反电动势常数与角速度求反电动势",
        "intro": "输入反电动势常数 k_e 与角速度 ω，求反电动势。", "desc": "直流电机反电动势：输入 k_e、ω，输出 E(V)。",
        "inputs": [
            {"id": "ke", "label": "反电动势常数 k_e", "value": "0.05", "step": "0.005", "unit": "V·s/rad"},
            {"id": "w", "label": "角速度 ω", "value": "100", "step": "5", "unit": "rad/s"},
        ],
        "calc": """
            const ke=num('ke'),w=num('w');
            const E=ke*w;
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(2),'反电动势 E (V)']
            ]));
        """,
        "notes": ["E = k_e·ω。", "k_e=0.05,ω=100 → 5 V。"],
    },
    {
        "slug": "battery-runtime",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "battery",
        "bg": "from-teal-500 to-emerald-600",
        "title": "电池续航时间计算器",
        "h1": "t = (Ah·V) / P",
        "h2": "由容量与功耗求续航时间",
        "intro": "输入电池容量 Ah、电压 V、负载功率 P，求续航时间。", "desc": "电池续航时间：输入 Ah、V、P，输出 t(h)。",
        "inputs": [
            {"id": "ah", "label": "容量 Ah", "value": "2", "step": "0.1", "unit": "Ah"},
            {"id": "V", "label": "电压 V", "value": "12", "step": "0.5", "unit": "V"},
            {"id": "P", "label": "功率 P", "value": "24", "step": "1", "unit": "W"},
        ],
        "calc": """
            const ah=num('ah'),V=num('V'),P=num('P');
            const t=ah*V/P;
            ToolBox.setResult('result', dataGrid([
                [t.toFixed(2),'续航时间 t (h)']
            ]));
        """,
        "notes": ["t = (Ah·V)/P = Wh/P。", "2Ah·12V / 24W → 1 h。"],
    },
    {
        "slug": "accel-distance",
        "industry": "robotics",
        "cat": "robotics",
        "icon": "ruler",
        "bg": "from-teal-500 to-emerald-600",
        "title": "匀加速距离计算器",
        "h1": "d = v² / (2a)",
        "h2": "由末速度与加速度求加速距离",
        "intro": "输入末速度 v 与加速度 a，求匀加速距离。", "desc": "匀加速距离：输入 v、a，输出 d(m)。",
        "inputs": [
            {"id": "v", "label": "末速度 v", "value": "2", "step": "0.1", "unit": "m/s"},
            {"id": "a", "label": "加速度 a", "value": "1", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const v=num('v'),a=num('a');
            const d=v*v/(2*a);
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(3),'加速距离 d (m)']
            ]));
        """,
        "notes": ["d = v²/(2a)（从静止）。", "v=2,a=1 → 2 m。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
