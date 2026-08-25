# -*- coding: utf-8 -*-
"""Batch 9: 流体力学计算深化（industry=hydraulic，14 个公式计算器）。

复用 scripts/tool_template.py。所有公式经手算核对。
"""
from tool_template import main

ICON = "💧"
BG = "#0ea5e9"
CAT = "calculator"

TOOLS = [
    {
        "slug": "reynolds-number",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "雷诺数计算器",
        "h1": "雷诺数（Re）计算器",
        "h2": "雷诺数 Re",
        "intro": "由密度、流速、特征管径与动力黏度，按 Re = ρvD/μ 计算流动雷诺数并判定流态。",
        "desc": "雷诺数计算器：输入密度、流速、管径与动力黏度，按 Re=ρvD/μ 判定层流/过渡/湍流。",
        "inputs": [
            {"id": "rho", "label": "流体密度 ρ", "value": 1000, "step": "1", "unit": "kg/m³", "min": "0"},
            {"id": "v", "label": "流速 v", "value": 1, "step": "0.1", "unit": "m/s", "min": "0"},
            {"id": "D", "label": "特征管径 D", "value": 0.1, "step": "0.01", "unit": "m", "min": "0"},
            {"id": "mu", "label": "动力黏度 μ", "value": 0.001, "step": "0.0001", "unit": "Pa·s", "min": "0"},
        ],
        "calc": """
            const rho=num('rho'), v=num('v'), D=num('D'), mu=num('mu');
            const Re = rho*v*D/mu;
            let state = Re<2300 ? '层流' : (Re<4000 ? '过渡流' : '湍流');
            ToolBox.setResult('result', dataGrid([
                [Re.toFixed(0), '雷诺数 Re = ρvD/μ'],
                [state, '流态判定']
            ]));
        """,
        "notes": [
            "圆管流：Re<2300 层流，2300–4000 过渡，>4000 湍流（近似经验值）。",
            "特征长度取水力直径；非圆管用 D=4A/P。",
        ],
    },
    {
        "slug": "bernoulli-velocity",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "伯努利方程流速计算器",
        "h1": "伯努利方程（求下游流速）计算器",
        "h2": "伯努利方程",
        "intro": "由上下游压强、流速、高程，按能量守恒求下游流速 v₂。",
        "desc": "伯努利方程计算器：输入上下游压强、流速与高程，求下游流速并判定是否可发生。",
        "inputs": [
            {"id": "P1", "label": "上游压强 P₁", "value": 200000, "step": "1000", "unit": "Pa"},
            {"id": "v1", "label": "上游流速 v₁", "value": 1, "step": "0.1", "unit": "m/s", "min": "0"},
            {"id": "z1", "label": "上游高程 z₁", "value": 0, "step": "0.5", "unit": "m"},
            {"id": "P2", "label": "下游压强 P₂", "value": 100000, "step": "1000", "unit": "Pa"},
            {"id": "z2", "label": "下游高程 z₂", "value": 5, "step": "0.5", "unit": "m"},
            {"id": "rho", "label": "流体密度 ρ", "value": 1000, "step": "1", "unit": "kg/m³", "min": "0"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const P1=num('P1'), v1=num('v1'), z1=num('z1'), P2=num('P2'), z2=num('z2'), rho=num('rho'), g=num('g');
            const v2sq = v1*v1 + 2*(P1-P2)/rho + 2*g*(z1-z2);
            if (v2sq < 0) {
                ToolBox.setResult('result', dataGrid([['给定条件下无解（能量不足）','提示']]));
            } else {
                ToolBox.setResult('result', dataGrid([ [Math.sqrt(v2sq).toFixed(2)+' m/s', '下游流速 v₂'] ]));
            }
        """,
        "notes": [
            "伯努利：P + ½ρv² + ρgz = 常数（忽略损失，理想不可压定常流）。",
        ],
    },
    {
        "slug": "darcy-head-loss",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "达西沿程水头损失计算器",
        "h1": "达西-魏斯巴赫沿程损失计算器",
        "h2": "达西-魏斯巴赫公式",
        "intro": "由摩擦系数、管长、管径、密度与流速，按 ΔP = f(L/D)(ρv²/2) 计算管道沿程压降。",
        "desc": "达西沿程损失计算器：输入摩擦系数、管长、管径、密度与流速，求管道沿程压降与水头损失。",
        "inputs": [
            {"id": "f", "label": "达西摩擦系数 f", "value": 0.02, "step": "0.001", "min": "0"},
            {"id": "L", "label": "管长 L", "value": 100, "step": "1", "unit": "m", "min": "0"},
            {"id": "D", "label": "管径 D", "value": 0.1, "step": "0.01", "unit": "m", "min": "0"},
            {"id": "rho", "label": "流体密度 ρ", "value": 1000, "step": "1", "unit": "kg/m³", "min": "0"},
            {"id": "v", "label": "流速 v", "value": 1, "step": "0.1", "unit": "m/s", "min": "0"},
        ],
        "calc": """
            const f=num('f'), L=num('L'), D=num('D'), rho=num('rho'), v=num('v');
            const dP = f*(L/D)*(rho*v*v/2);
            const h = dP/(rho*9.81);
            ToolBox.setResult('result', dataGrid([
                [dP.toFixed(0)+' Pa', '沿程压降 ΔP = f(L/D)(ρv²/2)'],
                [h.toFixed(3)+' m', '折合水头损失 h = ΔP/(ρg)']
            ]));
        """,
        "notes": [
            "f 可用 Moody 图或 Colebrook 公式由 Re 与相对粗糙度求得。",
        ],
    },
    {
        "slug": "hazen-williams-headloss",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "哈森-威廉姆斯水头损失计算器",
        "h1": "哈森-威廉姆斯水头损失计算器",
        "h2": "Hazen-Williams 公式",
        "intro": "由流量、管长、粗糙系数 C 与管径，按 h_f = 10.67·L·Q^1.852/(C^1.852·D^4.87) 计算水头损失（SI）。",
        "desc": "哈森-威廉姆斯水头损失计算器：输入流量、管长、C 值与管径，求给水管道水头损失。",
        "inputs": [
            {"id": "Q", "label": "流量 Q", "value": 0.01, "step": "0.001", "unit": "m³/s", "min": "0"},
            {"id": "L", "label": "管长 L", "value": 100, "step": "1", "unit": "m", "min": "0"},
            {"id": "C", "label": "粗糙系数 C", "value": 120, "step": "1", "min": "1"},
            {"id": "D", "label": "管径 D", "value": 0.1, "step": "0.01", "unit": "m", "min": "0"},
        ],
        "calc": """
            const Q=num('Q'), L=num('L'), C=num('C'), D=num('D');
            const hf = 10.67 * L * Math.pow(Q,1.852) / (Math.pow(C,1.852) * Math.pow(D,4.87));
            ToolBox.setResult('result', dataGrid([ [hf.toFixed(3)+' m', '水头损失 h_f (Hazen-Williams)'] ]));
        """,
        "notes": [
            "适用于水温约 4–25℃ 的给水管道；C 值：新钢管≈120–140，旧管≈80–100。",
            "单位为 SI（Q: m³/s，D: m，结果 m）。",
        ],
    },
    {
        "slug": "orifice-discharge",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "孔口出流计算器",
        "h1": "孔口出流流量计算器",
        "h2": "孔口自由出流",
        "intro": "由流量系数、孔径与水头，按 Q = Cd·A·√(2gh) 计算孔口出流流量。",
        "desc": "孔口出流计算器：输入流量系数、孔径与水头，求孔口自由出流流量。",
        "inputs": [
            {"id": "Cd", "label": "流量系数 Cd", "value": 0.62, "step": "0.01", "min": "0"},
            {"id": "d", "label": "孔径 d", "value": 0.05, "step": "0.005", "unit": "m", "min": "0"},
            {"id": "h", "label": "作用水头 h", "value": 2, "step": "0.1", "unit": "m", "min": "0"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const Cd=num('Cd'), d=num('d'), h=num('h'), g=num('g');
            const A = Math.PI*d*d/4;
            const Q = Cd*A*Math.sqrt(2*g*h);
            ToolBox.setResult('result', dataGrid([ [Q.toFixed(5)+' m³/s', '出流流量 Q = Cd·A·√(2gh)'] ]));
        """,
        "notes": [
            "薄壁小孔口 Cd≈0.61–0.62；大孔口或管嘴取值不同。",
        ],
    },
    {
        "slug": "manning-flow",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "曼宁明渠流量计算器",
        "h1": "曼宁公式明渠流量计算器",
        "h2": "曼宁公式",
        "intro": "由糙率 n、过水断面 A、水力半径 R 与底坡 S，按 Q=(1/n)A·R^(2/3)·√S 计算明渠均匀流流量。",
        "desc": "曼宁明渠流量计算器：输入糙率、断面面积、水力半径与底坡，求明渠均匀流流量。",
        "inputs": [
            {"id": "n", "label": "糙率 n", "value": 0.013, "step": "0.001", "min": "0"},
            {"id": "A", "label": "过水断面 A", "value": 1, "step": "0.1", "unit": "m²", "min": "0"},
            {"id": "R", "label": "水力半径 R", "value": 0.5, "step": "0.05", "unit": "m", "min": "0"},
            {"id": "S", "label": "底坡 S", "value": 0.001, "step": "0.0001", "min": "0"},
        ],
        "calc": """
            const n=num('n'), A=num('A'), R=num('R'), S=num('S');
            const Q = (1/n)*A*Math.pow(R,2/3)*Math.sqrt(S);
            ToolBox.setResult('result', dataGrid([ [Q.toFixed(3)+' m³/s', '明渠流量 Q = (1/n)A·R^(2/3)·√S'] ]));
        """,
        "notes": [
            "水力半径 R = A/P（P 为湿周）。",
            "适用均匀流；n 取值：混凝土 0.012–0.015，天然河道 0.025–0.035。",
        ],
    },
    {
        "slug": "hydrostatic-pressure",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "静水压强计算器",
        "h1": "静水压强计算器",
        "h2": "静水压强",
        "intro": "由液体密度、重力加速度与深度，按 P = ρgh 计算静水压强（相对压强）。",
        "desc": "静水压强计算器：输入液体密度、重力加速度与深度，求静水压强。",
        "inputs": [
            {"id": "rho", "label": "液体密度 ρ", "value": 1000, "step": "1", "unit": "kg/m³", "min": "0"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
            {"id": "h", "label": "深度 h", "value": 10, "step": "0.5", "unit": "m", "min": "0"},
        ],
        "calc": """
            const rho=num('rho'), g=num('g'), h=num('h');
            const P = rho*g*h;
            ToolBox.setResult('result', dataGrid([ [P.toFixed(0)+' Pa', '静水压强 P = ρgh'] ]));
        """,
        "notes": [
            "结果为相对压强（表压）；绝对压强需加大气压 ≈101325 Pa。",
        ],
    },
    {
        "slug": "buoyancy-force",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "浮力计算器",
        "h1": "阿基米德浮力计算器",
        "h2": "阿基米德原理",
        "intro": "由流体密度、重力加速度与排开体积，按 F = ρgV 计算浮力。",
        "desc": "浮力计算器：输入流体密度、重力加速度与排开体积，按阿基米德原理求浮力。",
        "inputs": [
            {"id": "rho", "label": "流体密度 ρ", "value": 1000, "step": "1", "unit": "kg/m³", "min": "0"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
            {"id": "V", "label": "排开体积 V", "value": 0.5, "step": "0.05", "unit": "m³", "min": "0"},
        ],
        "calc": """
            const rho=num('rho'), g=num('g'), V=num('V');
            const F = rho*g*V;
            ToolBox.setResult('result', dataGrid([ [F.toFixed(1)+' N', '浮力 F = ρgV'] ]));
        """,
        "notes": [
            "浮力等于排开流体的重量；物体密度小于流体则上浮。",
        ],
    },
    {
        "slug": "continuity-pipe",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "连续性方程流速计算器",
        "h1": "连续性方程（管道变径）计算器",
        "h2": "质量/体积连续性",
        "intro": "由入口断面、流速与出口断面，按 A₁v₁ = A₂v₂ 求变径后流速。",
        "desc": "连续性方程计算器：输入入口断面、流速与出口断面面积，求变径后流速。",
        "inputs": [
            {"id": "A1", "label": "入口断面 A₁", "value": 0.1, "step": "0.01", "unit": "m²", "min": "0"},
            {"id": "v1", "label": "入口流速 v₁", "value": 2, "step": "0.1", "unit": "m/s", "min": "0"},
            {"id": "A2", "label": "出口断面 A₂", "value": 0.05, "step": "0.01", "unit": "m²", "min": "0"},
        ],
        "calc": """
            const A1=num('A1'), v1=num('v1'), A2=num('A2');
            const v2 = A1*v1/A2;
            ToolBox.setResult('result', dataGrid([ [v2.toFixed(2)+' m/s', '出口流速 v₂ = A₁v₁/A₂'] ]));
        """,
        "notes": [
            "不可压定常流：体积流量守恒 Q=A·v = 常数。",
        ],
    },
    {
        "slug": "pump-power",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "水泵轴功率计算器",
        "h1": "水泵功率计算器",
        "h2": "泵功率",
        "intro": "由流量、扬程与效率，按 P = ρgQH/η 计算水泵轴功率（输入功率）。",
        "desc": "水泵轴功率计算器：输入流量、扬程、效率与流体密度，求水泵所需轴功率。",
        "inputs": [
            {"id": "rho", "label": "流体密度 ρ", "value": 1000, "step": "1", "unit": "kg/m³", "min": "0"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
            {"id": "Q", "label": "流量 Q", "value": 0.05, "step": "0.005", "unit": "m³/s", "min": "0"},
            {"id": "H", "label": "扬程 H", "value": 20, "step": "0.5", "unit": "m", "min": "0"},
            {"id": "eta", "label": "效率 η", "value": 0.75, "step": "0.01", "min": "0", "max": "1"},
        ],
        "calc": """
            const rho=num('rho'), g=num('g'), Q=num('Q'), H=num('H'), eta=num('eta');
            const P = rho*g*Q*H/eta;
            ToolBox.setResult('result', dataGrid([
                [(P/1000).toFixed(2)+' kW', '轴功率 P = ρgQH/η'],
                [(rho*g*Q*H/1000).toFixed(2)+' kW', '有效功率（水力功率）']
            ]));
        """,
        "notes": [
            "轴功率=水力功率/效率；η 越低成本越高。",
        ],
    },
    {
        "slug": "minor-head-loss",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "局部水头损失计算器",
        "h1": "局部水头损失计算器",
        "h2": "局部损失 h_L",
        "intro": "由局部阻力系数与流速，按 h_L = K·v²/(2g) 计算阀门、弯头等局部水头损失。",
        "desc": "局部水头损失计算器：输入局部阻力系数与流速，求管件局部水头损失。",
        "inputs": [
            {"id": "K", "label": "局部阻力系数 K", "value": 0.5, "step": "0.05", "min": "0"},
            {"id": "v", "label": "流速 v", "value": 3, "step": "0.1", "unit": "m/s", "min": "0"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const K=num('K'), v=num('v'), g=num('g');
            const hL = K*v*v/(2*g);
            ToolBox.setResult('result', dataGrid([ [hL.toFixed(3)+' m', '局部水头损失 h_L = K·v²/(2g)'] ]));
        """,
        "notes": [
            "K 典型值：90°弯头≈0.3–0.9，全开闸阀≈0.2，突然扩大按公式单独算。",
        ],
    },
    {
        "slug": "kinematic-viscosity",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "运动黏度计算器",
        "h1": "运动黏度计算器",
        "h2": "运动黏度 ν",
        "intro": "由动力黏度与密度，按 ν = μ/ρ 计算运动黏度。",
        "desc": "运动黏度计算器：输入动力黏度与密度，求运动黏度（常用于水力学与润滑油）。",
        "inputs": [
            {"id": "mu", "label": "动力黏度 μ", "value": 0.001, "step": "0.0001", "unit": "Pa·s", "min": "0"},
            {"id": "rho", "label": "密度 ρ", "value": 1000, "step": "1", "unit": "kg/m³", "min": "0"},
        ],
        "calc": """
            const mu=num('mu'), rho=num('rho');
            const nu = mu/rho;
            ToolBox.setResult('result', dataGrid([ [(nu*1e6).toFixed(2)+' ×10⁻⁶ m²/s', '运动黏度 ν = μ/ρ'] ]));
        """,
        "notes": [
            "20℃ 水的运动黏度约 1.0×10⁻⁶ m²/s，常作基准。",
        ],
    },
    {
        "slug": "rectangular-weir",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "矩形薄壁堰流量计算器",
        "h1": "矩形薄壁堰流量计算器",
        "h2": "矩形薄壁堰",
        "intro": "由流量系数、堰宽与堰上水头，按 Q=(2/3)Cd·b·√(2g)·H^1.5 计算堰流量。",
        "desc": "矩形薄壁堰流量计算器：输入流量系数、堰宽与堰上水头，求堰流流量。",
        "inputs": [
            {"id": "Cd", "label": "流量系数 Cd", "value": 0.62, "step": "0.01", "min": "0"},
            {"id": "b", "label": "堰宽 b", "value": 2, "step": "0.1", "unit": "m", "min": "0"},
            {"id": "H", "label": "堰上水头 H", "value": 0.3, "step": "0.05", "unit": "m", "min": "0"},
            {"id": "g", "label": "重力加速度 g", "value": 9.81, "step": "0.01", "unit": "m/s²"},
        ],
        "calc": """
            const Cd=num('Cd'), b=num('b'), H=num('H'), g=num('g');
            const Q = (2/3)*Cd*b*Math.sqrt(2*g)*Math.pow(H,1.5);
            ToolBox.setResult('result', dataGrid([ [Q.toFixed(4)+' m³/s', '堰流量 Q = (2/3)Cd·b·√(2g)·H^1.5'] ]));
        """,
        "notes": [
            "适用于无侧收缩、自由出流的矩形薄壁堰。",
        ],
    },
    {
        "slug": "velocity-from-flow",
        "industry": "hydraulic", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "流量换算流速计算器",
        "h1": "由流量求流速计算器",
        "h2": "流速 v = Q/A",
        "intro": "由体积流量与过流断面面积，按 v = Q/A 计算平均流速。",
        "desc": "流量换算流速计算器：输入体积流量与断面面积，求平均流速。",
        "inputs": [
            {"id": "Q", "label": "流量 Q", "value": 0.1, "step": "0.01", "unit": "m³/s", "min": "0"},
            {"id": "A", "label": "断面面积 A", "value": 0.05, "step": "0.005", "unit": "m²", "min": "0"},
        ],
        "calc": """
            const Q=num('Q'), A=num('A');
            const v = Q/A;
            ToolBox.setResult('result', dataGrid([ [v.toFixed(2)+' m/s', '平均流速 v = Q/A'] ]));
        """,
        "notes": [
            "Q=A·v 的逆向运算，常用于管道与明渠设计校核。",
        ],
    },
]


if __name__ == "__main__":
    main(TOOLS)
