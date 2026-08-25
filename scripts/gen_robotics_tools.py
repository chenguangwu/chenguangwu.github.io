# -*- coding: utf-8 -*-
"""Batch 23: 机器人学计算深化（14 个公式计算器）。industry=robotics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "forward-kinematics-2r", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "二连杆正运动学", "h1": "二连杆正运动学计算器",
        "h2": "x = L₁cosθ₁ + L₂cos(θ₁+θ₂)",
        "intro": "由关节角求末端执行器坐标。",
        "desc": "二连杆正运动学：由 θ₁,θ₂,L₁,L₂ 求末端 (x,y)。",
        "inputs": [
            {"id": "t1", "label": "关节角 θ₁", "value": "30", "step": "1", "unit": "°"},
            {"id": "t2", "label": "关节角 θ₂", "value": "45", "step": "1", "unit": "°"},
            {"id": "L1", "label": "杆长 L₁", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "L2", "label": "杆长 L₂", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const t1 = num('t1') * Math.PI / 180, t2 = num('t2') * Math.PI / 180,
                  L1 = num('L1'), L2 = num('L2');
            const x = L1 * Math.cos(t1) + L2 * Math.cos(t1 + t2);
            const y = L1 * Math.sin(t1) + L2 * Math.sin(t1 + t2);
            ToolBox.setResult('result', dataGrid([
                [x.toFixed(4), '末端 x (m)'],
                [y.toFixed(4), '末端 y (m)']
            ]));
        """,
        "notes": ["x = L₁cosθ₁ + L₂cos(θ₁+θ₂)。", "θ₁=30°、θ₂=45°、L=1 → 约 (1.297, 1.207)。"],
    },
    {
        "slug": "inverse-kinematics-2r", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "二连杆逆运动学", "h1": "二连杆逆运动学计算器",
        "h2": "由 (x,y) 反解关节角 θ₁,θ₂",
        "intro": "平面二连杆逆解，含可达性判定。",
        "desc": "二连杆逆运动学：由 x,y,L₁,L₂ 反解 θ₁,θ₂。",
        "inputs": [
            {"id": "x", "label": "目标 x", "value": "1.3", "step": "0.05", "unit": "m"},
            {"id": "y", "label": "目标 y", "value": "1.2", "step": "0.05", "unit": "m"},
            {"id": "L1", "label": "杆长 L₁", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "L2", "label": "杆长 L₂", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const x = num('x'), y = num('y'), L1 = num('L1'), L2 = num('L2');
            const r2 = x * x + y * y, sum = L1 * L1 + L2 * L2;
            const c2 = (r2 - sum) / (2 * L1 * L2);
            if (c2 < -1 || c2 > 1) {
                ToolBox.setResult('result', dataGrid([['目标超出工作空间', '不可达']]));
            } else {
                const t2 = Math.acos(c2);
                const t1 = Math.atan2(y, x) - Math.atan2(L2 * Math.sin(t2), L1 + L2 * Math.cos(t2));
                ToolBox.setResult('result', dataGrid([
                    [(t1 * 180 / Math.PI).toFixed(2), 'θ₁ (°)'],
                    [(t2 * 180 / Math.PI).toFixed(2), 'θ₂ (°)']
                ]));
            }
        """,
        "notes": ["cosθ₂=(r²−L₁²−L₂²)/(2L₁L₂)。", "|L₁−L₂| ≤ √(x²+y²) ≤ L₁+L₂ 才可解。"],
    },
    {
        "slug": "diff-drive-velocity", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "差速驱动速度", "h1": "差速驱动线/角速度计算器",
        "h2": "v = (v_r + v_l)/2，ω = (v_r − v_l)/L",
        "intro": "由左右轮速度求机器人线速度与角速度。",
        "desc": "差速驱动：v=(v_r+v_l)/2，ω=(v_r−v_l)/L。",
        "inputs": [
            {"id": "vl", "label": "左轮速 v_l", "value": "0.5", "step": "0.05", "unit": "m/s"},
            {"id": "vr", "label": "右轮速 v_r", "value": "1.0", "step": "0.05", "unit": "m/s"},
            {"id": "L", "label": "轮距 L", "value": "0.4", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const vl = num('vl'), vr = num('vr'), L = num('L');
            const v = (vr + vl) / 2, w = (vr - vl) / L;
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(4), '线速度 v (m/s)'],
                [w.toFixed(4), '角速度 ω (rad/s)']
            ]));
        """,
        "notes": ["v=(v_r+v_l)/2。", "两轮不等速产生转向。"],
    },
    {
        "slug": "wheel-odometry", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "轮式里程计", "h1": "轮式里程计位移计算器",
        "h2": "Δs = (d_r + d_l)/2，Δθ = (d_r − d_l)/L",
        "intro": "由左右轮行进距离估计位姿变化。",
        "desc": "轮式里程计：Δs=(d_r+d_l)/2，Δθ=(d_r−d_l)/L。",
        "inputs": [
            {"id": "dl", "label": "左轮行距 d_l", "value": "1.0", "step": "0.05", "unit": "m"},
            {"id": "dr", "label": "右轮行距 d_r", "value": "1.2", "step": "0.05", "unit": "m"},
            {"id": "L", "label": "轮距 L", "value": "0.4", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const dl = num('dl'), dr = num('dr'), L = num('L');
            const ds = (dr + dl) / 2, dth = (dr - dl) / L;
            ToolBox.setResult('result', dataGrid([
                [ds.toFixed(4), '位移 Δs (m)'],
                [(dth * 180 / Math.PI).toFixed(2), '航向变化 (°)']
            ]));
        """,
        "notes": ["Δs=(d_r+d_l)/2。", "航向变化=两轮行距差/轮距。"],
    },
    {
        "slug": "pid-controller", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "PID 控制器输出", "h1": "PID 控制器输出计算器",
        "h2": "u = Kp·e + Ki·∫e + Kd·ė",
        "intro": "比例-积分-微分控制律输出。",
        "desc": "PID 输出：u = Kp·e + Ki·∫e + Kd·(e−eₚ)/dt。",
        "inputs": [
            {"id": "kp", "label": "比例 Kp", "value": "1.0", "step": "0.1"},
            {"id": "ki", "label": "积分 Ki", "value": "0.1", "step": "0.01"},
            {"id": "kd", "label": "微分 Kd", "value": "0.05", "step": "0.01"},
            {"id": "e", "label": "误差 e", "value": "2", "step": "0.1"},
            {"id": "ei", "label": "误差积分 ∫e", "value": "1", "step": "0.1"},
            {"id": "ep", "label": "上次误差 eₚ", "value": "0.5", "step": "0.1"},
            {"id": "dt", "label": "采样时间 dt", "value": "0.1", "step": "0.01", "unit": "s"},
        ],
        "calc": """
            const kp = num('kp'), ki = num('ki'), kd = num('kd'),
                  e = num('e'), ei = num('ei'), ep = num('ep'), dt = num('dt');
            const u = kp * e + ki * ei + kd * (e - ep) / dt;
            ToolBox.setResult('result', dataGrid([
                [(kp * e).toFixed(4), '比例项 Kp·e'],
                [(ki * ei).toFixed(4), '积分项 Ki·∫e'],
                [(kd * (e - ep) / dt).toFixed(4), '微分项 Kd·ė'],
                [u.toFixed(4), '总输出 u']
            ]));
        """,
        "notes": ["u = Kp·e + Ki·∫e + Kd·ė。", "积分项消除稳态误差。"],
    },
    {
        "slug": "motor-torque-current", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "电机转矩电流", "h1": "电机转矩电流计算器",
        "h2": "τ = Kt · I",
        "intro": "直流电机转矩与电流成正比。",
        "desc": "电机转矩：τ = Kt·I，输入转矩常数与电流。",
        "inputs": [
            {"id": "kt", "label": "转矩常数 Kt", "value": "0.05", "step": "0.005", "unit": "N·m/A"},
            {"id": "I", "label": "电流 I", "value": "10", "step": "0.5", "unit": "A"},
        ],
        "calc": """
            const kt = num('kt'), I = num('I');
            const t = kt * I;
            ToolBox.setResult('result', dataGrid([
                [t.toFixed(4), '转矩 τ (N·m)'],
                [(t * 1000).toFixed(1), 'τ (mN·m)']
            ]));
        """,
        "notes": ["τ = Kt·I。", "Kt=0.05、I=10A → 0.5 N·m。"],
    },
    {
        "slug": "servo-pwm-angle", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "舵机 PWM 转角度", "h1": "舵机 PWM 角度计算器",
        "h2": "角度 = (脉宽 − 最小) / (最大 − 最小) × 180°",
        "intro": "由 PWM 脉冲宽度求舵机转角。",
        "desc": "舵机角度：angle = (pwm−min)/(max−min)×180°。",
        "inputs": [
            {"id": "pwm", "label": "脉宽", "value": "1500", "step": "10", "unit": "µs"},
            {"id": "pmin", "label": "最小脉宽", "value": "500", "step": "10", "unit": "µs"},
            {"id": "pmax", "label": "最大脉宽", "value": "2500", "step": "10", "unit": "µs"},
        ],
        "calc": """
            const pwm = num('pwm'), pmin = num('pmin'), pmax = num('pmax');
            const ang = (pwm - pmin) / (pmax - pmin) * 180;
            ToolBox.setResult('result', dataGrid([
                [ang.toFixed(2), '转角 (°)']
            ]));
        """,
        "notes": ["1500µs（500–2500 范围）→ 90°。", "常见舵机 1000–2000µs。"],
    },
    {
        "slug": "gear-ratio-speed", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "减速比输出转速", "h1": "齿轮减速比转速计算器",
        "h2": "n_out = n_in / i，v = n_out·2πR/60",
        "intro": "由输入转速与减速比求输出转速及线速度。",
        "desc": "减速比：n_out=n_in/i，v=n_out·2πR/60。",
        "inputs": [
            {"id": "nin", "label": "输入转速 n_in", "value": "300", "step": "10", "unit": "rpm"},
            {"id": "i", "label": "减速比 i", "value": "30", "step": "1"},
            {"id": "R", "label": "输出轮半径 R", "value": "0.1", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const nin = num('nin'), i = num('i'), R = num('R');
            const nout = nin / i;
            const v = nout * 2 * Math.PI * R / 60;
            ToolBox.setResult('result', dataGrid([
                [nout.toFixed(2), '输出转速 (rpm)'],
                [(v * 3.6).toFixed(3), '线速度 (km/h)']
            ]));
        """,
        "notes": ["n_out = n_in/i。", "300rpm/30 = 10rpm，R=0.1 → 0.105 m/s。"],
    },
    {
        "slug": "gripper-force", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "夹爪夹持力", "h1": "夹爪夹持力计算器",
        "h2": "F = 2τ / L",
        "intro": "由驱动转矩与力臂估算两指总夹持力。",
        "desc": "夹爪力：F = 2τ/L，输入转矩与力臂。",
        "inputs": [
            {"id": "tau", "label": "驱动转矩 τ", "value": "5", "step": "0.5", "unit": "N·m"},
            {"id": "L", "label": "力臂 L", "value": "0.05", "step": "0.005", "unit": "m"},
        ],
        "calc": """
            const tau = num('tau'), L = num('L');
            const F = 2 * tau / L;
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(2), '夹持力 F (N)'],
                [(F / 9.81).toFixed(3), 'F (kgf)']
            ]));
        """,
        "notes": ["F = 2τ/L（双指）。", "τ=5、L=0.05 → 200 N。"],
    },
    {
        "slug": "lifting-torque", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "搬运关节转矩", "h1": "搬运负载关节转矩计算器",
        "h2": "τ = m · g · r",
        "intro": "竖直搬运负载时关节所需保持转矩。",
        "desc": "搬运转矩：τ = m·g·r，输入质量、力臂。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "2", "step": "0.1", "unit": "kg"},
            {"id": "r", "label": "力臂 r", "value": "0.5", "step": "0.05", "unit": "m"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const m = num('m'), r = num('r'), g = num('g');
            const tau = m * g * r;
            ToolBox.setResult('result', dataGrid([
                [tau.toFixed(3), '关节转矩 τ (N·m)']
            ]));
        """,
        "notes": ["τ = m·g·r。", "2kg×9.8×0.5 = 9.8 N·m。"],
    },
    {
        "slug": "centripetal-speed-limit", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "转弯限速", "h1": "机器人转弯最大速度计算器",
        "h2": "v_max = √(a_max · R)",
        "intro": "受最大向心加速度约束的转弯速度上限。",
        "desc": "转弯限速：v_max = √(a_max·R)，输入最大加速度与转弯半径。",
        "inputs": [
            {"id": "amax", "label": "最大加速度 a_max", "value": "2", "step": "0.1", "unit": "m/s²"},
            {"id": "R", "label": "转弯半径 R", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const amax = num('amax'), R = num('R');
            const v = Math.sqrt(amax * R);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(3), '最大速度 v_max (m/s)']
            ]));
        """,
        "notes": ["v_max = √(a_max·R)。", "a=2、R=1 → 1.414 m/s。"],
    },
    {
        "slug": "lead-screw-speed", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "丝杠线速度", "h1": "滚珠丝杠线速度计算器",
        "h2": "v = n · p / 60",
        "intro": "由转速与导程求螺母线速度。",
        "desc": "丝杠线速度：v = n·p/60，输入转速与导程。",
        "inputs": [
            {"id": "n", "label": "转速 n", "value": "300", "step": "10", "unit": "rpm"},
            {"id": "p", "label": "导程 p", "value": "0.005", "step": "0.001", "unit": "m/rev"},
        ],
        "calc": """
            const n = num('n'), p = num('p');
            const v = n * p / 60;
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(5), '线速度 v (m/s)'],
                [(v * 1000).toFixed(2), 'v (mm/s)']
            ]));
        """,
        "notes": ["v = n·p/60。", "300rpm×5mm → 25 mm/s。"],
    },
    {
        "slug": "belt-linear-speed", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "同步带线速度", "h1": "同步带线速度计算器",
        "h2": "v = π · D · n / 60",
        "intro": "由带轮直径与转速求带速。",
        "desc": "同步带线速度：v = π·D·n/60，输入直径与转速。",
        "inputs": [
            {"id": "D", "label": "带轮直径 D", "value": "0.06", "step": "0.005", "unit": "m"},
            {"id": "n", "label": "转速 n", "value": "300", "step": "10", "unit": "rpm"},
        ],
        "calc": """
            const D = num('D'), n = num('n');
            const v = Math.PI * D * n / 60;
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(4), '带速 v (m/s)']
            ]));
        """,
        "notes": ["v = π·D·n/60。", "D=0.06、300rpm → 0.942 m/s。"],
    },
    {
        "slug": "end-effector-reach", "industry": "robotics", "cat": "robotics", "icon": "🦾", "bg": "#eff6ff",
        "title": "工作空间可达半径", "h1": "二连杆工作空间计算器",
        "h2": "L₁−L₂ ≤ r ≤ L₁+L₂",
        "intro": "平面二连杆可到达的环形工作空间范围。",
        "desc": "工作空间：可达半径 |L₁−L₂| ≤ r ≤ L₁+L₂。",
        "inputs": [
            {"id": "L1", "label": "杆长 L₁", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "L2", "label": "杆长 L₂", "value": "0.8", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const L1 = num('L1'), L2 = num('L2');
            const rmin = Math.abs(L1 - L2), rmax = L1 + L2;
            ToolBox.setResult('result', dataGrid([
                [rmin.toFixed(3), '最小可达半径 (m)'],
                [rmax.toFixed(3), '最大可达半径 (m)']
            ]));
        """,
        "notes": ["可达半径介于 |L₁−L₂| 与 L₁+L₂ 之间。", "L=1、0.8 → 0.2~1.8 m。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
