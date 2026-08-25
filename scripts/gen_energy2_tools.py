# -*- coding: utf-8 -*-
"""Batch 69: 能源计算深化 II（14 个公式计算器）。industry=energy。"""
from tool_template import main

TOOLS = [
    {
        "slug": "kinetic-energy",
        "industry": "energy",
        "cat": "energy",
        "icon": "zap",
        "bg": "from-amber-500 to-yellow-600",
        "title": "动能计算器",
        "h1": "E_k = ½·m·v²",
        "h2": "由质量与速度求动能",
        "intro": "输入质量 m 与速度 v，求动能。",
        "desc": "动能：输入 m、v，输出 E_k(焦耳)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "1000", "step": "50", "unit": "千克"},
            {"id": "v", "label": "速度 v", "value": "20", "step": "1", "unit": "米/秒"},
        ],
        "calc": """
            const m=num('m'),v=num('v');
            const Ek=0.5*m*v*v;
            ToolBox.setResult('result', dataGrid([
                [Ek.toFixed(2),'动能 E_k (J)']
            ]));
        """,
        "notes": ["动能与速度平方成正比。", "1000×20²/2 → 200000 J。"],
    },
    {
        "slug": "gravitational-potential",
        "industry": "energy",
        "cat": "energy",
        "icon": "arrow-down",
        "bg": "from-amber-500 to-yellow-600",
        "title": "重力势能计算器",
        "h1": "E_p = m·g·h",
        "h2": "由质量、重力加速度与高度求势能",
        "intro": "输入质量 m、重力加速度 g 与高度 h，求重力势能。",
        "desc": "重力势能：输入 m、g、h，输出 E_p(焦耳)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "10", "step": "1", "unit": "千克"},
            {"id": "g", "label": "重力加速度 g", "value": "9.81", "step": "0.01", "unit": "米/秒²"},
            {"id": "h", "label": "高度 h", "value": "5", "step": "0.5", "unit": "米"},
        ],
        "calc": """
            const m=num('m'),g=num('g'),h=num('h');
            const Ep=m*g*h;
            ToolBox.setResult('result', dataGrid([
                [Ep.toFixed(2),'重力势能 E_p (J)']
            ]));
        """,
        "notes": ["以参考面为零势能面。", "10×9.81×5 → 490.5 J。"],
    },
    {
        "slug": "electrical-power",
        "industry": "energy",
        "cat": "energy",
        "icon": "zap",
        "bg": "from-amber-500 to-yellow-600",
        "title": "电功率计算器",
        "h1": "P = U·I",
        "h2": "由电压与电流求电功率",
        "intro": "输入电压 U 与电流 I，求电功率。",
        "desc": "电功率：输入 U、I，输出 P(瓦)。",
        "inputs": [
            {"id": "U", "label": "电压 U", "value": "12", "step": "1", "unit": "伏"},
            {"id": "I", "label": "电流 I", "value": "2", "step": "0.2", "unit": "安"},
        ],
        "calc": """
            const U=num('U'),I=num('I');
            const P=U*I;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2),'电功率 P (W)']
            ]));
        """,
        "notes": ["直流功率基本式。", "12×2 → 24 W。"],
    },
    {
        "slug": "joule-heating",
        "industry": "energy",
        "cat": "energy",
        "icon": "flame",
        "bg": "from-amber-500 to-yellow-600",
        "title": "焦耳热功率计算器",
        "h1": "P = I²·R",
        "h2": "由电流与电阻求热功率",
        "intro": "输入电流 I 与电阻 R，求焦耳热功率。",
        "desc": "焦耳热：输入 I、R，输出 P(瓦)。",
        "inputs": [
            {"id": "I", "label": "电流 I", "value": "2", "step": "0.2", "unit": "安"},
            {"id": "R", "label": "电阻 R", "value": "5", "step": "0.5", "unit": "欧"},
        ],
        "calc": """
            const I=num('I'),R=num('R');
            const P=I*I*R;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2),'热功率 P (W)']
            ]));
        """,
        "notes": ["电流热效应损耗。", "2²×5 → 20 W。"],
    },
    {
        "slug": "energy-from-power",
        "industry": "energy",
        "cat": "energy",
        "icon": "clock",
        "bg": "from-amber-500 to-yellow-600",
        "title": "电能(电量)计算器",
        "h1": "E = P·t",
        "h2": "由功率与用电时长求电能",
        "intro": "输入功率 P（瓦）与用电时长 t（小时），求电能（千瓦时）。",
        "desc": "电能：输入 P(W)、t(小时)，输出 E(kWh)。",
        "inputs": [
            {"id": "P", "label": "功率 P", "value": "1000", "step": "50", "unit": "瓦"},
            {"id": "t", "label": "时长 t", "value": "2", "step": "0.5", "unit": "小时"},
        ],
        "calc": """
            const P=num('P'),t=num('t');
            const E=P/1000*t;
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(3),'电能 E (kWh)']
            ]));
        """,
        "notes": ["1 kWh = 3.6×10⁶ J。", "1000W×2h → 2 kWh。"],
    },
    {
        "slug": "heat-energy-q",
        "industry": "energy",
        "cat": "energy",
        "icon": "thermometer",
        "bg": "from-amber-500 to-yellow-600",
        "title": "显热(比热)计算器",
        "h1": "Q = m·c·ΔT",
        "h2": "由质量、比热与温升求热量",
        "intro": "输入质量 m、比热 c 与温差 ΔT，求热量。",
        "desc": "显热：输入 m、c、ΔT，输出 Q(焦耳)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "1", "step": "0.1", "unit": "千克"},
            {"id": "c", "label": "比热 c", "value": "4186", "step": "100", "unit": "J/(kg·K)"},
            {"id": "dT", "label": "温差 ΔT", "value": "80", "step": "5", "unit": "K"},
        ],
        "calc": """
            const m=num('m'),c=num('c'),dT=num('dT');
            const Q=m*c*dT;
            ToolBox.setResult('result', dataGrid([
                [Q.toFixed(2),'热量 Q (J)']
            ]));
        """,
        "notes": ["水的比热约 4186 J/(kg·K)。", "1×4186×80 → 334880 J。"],
    },
    {
        "slug": "carnot-efficiency",
        "industry": "energy",
        "cat": "energy",
        "icon": "repeat",
        "bg": "from-amber-500 to-yellow-600",
        "title": "卡诺效率计算器",
        "h1": "η = 1 − T_c / T_h",
        "h2": "由冷热源温度求理论最高热效率",
        "intro": "输入低温热源温度 T_c 与高温热源温度 T_h（开尔文），求卡诺效率。",
        "desc": "卡诺效率：输入 Tc、Th(K)，输出 η(%)。",
        "inputs": [
            {"id": "Tc", "label": "低温 T_c", "value": "300", "step": "10", "unit": "K"},
            {"id": "Th", "label": "高温 T_h", "value": "600", "step": "10", "unit": "K"},
        ],
        "calc": """
            const Tc=num('Tc'),Th=num('Th');
            const eta=1-Tc/Th;
            ToolBox.setResult('result', dataGrid([
                [(eta*100).toFixed(2),'卡诺效率 η (%)']
            ]));
        """,
        "notes": ["实际热机效率低于卡诺极限。", "1−300/600 → 50%。"],
    },
    {
        "slug": "r-value-insulation",
        "industry": "energy",
        "cat": "energy",
        "icon": "layers",
        "bg": "from-amber-500 to-yellow-600",
        "title": "热阻(R值)计算器",
        "h1": "R = d / k",
        "h2": "由厚度与导热系数求热阻",
        "intro": "输入材料厚度 d 与导热系数 k，求热阻 R。",
        "desc": "热阻 R 值：输入 d、k，输出 R。",
        "inputs": [
            {"id": "d", "label": "厚度 d", "value": "0.2", "step": "0.01", "unit": "米"},
            {"id": "k", "label": "导热系数 k", "value": "0.04", "step": "0.005", "unit": "W/(m·K)"},
        ],
        "calc": """
            const d=num('d'),k=num('k');
            const R=d/k;
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(3),'热阻 R (m²·K/W)']
            ]));
        """,
        "notes": ["R 越大保温越好。", "0.2/0.04 → 5.0。"],
    },
    {
        "slug": "conductive-heat-rate",
        "industry": "energy",
        "cat": "energy",
        "icon": "arrow-right",
        "bg": "from-amber-500 to-yellow-600",
        "title": "导热热流率计算器",
        "h1": "Q̇ = k·A·ΔT / d",
        "h2": "由导热系数、面积、温差与厚度求热流率",
        "intro": "输入导热系数 k、面积 A、温差 ΔT 与厚度 d，求热流率。",
        "desc": "导热热流率：输入 k、A、ΔT、d，输出 Q̇(瓦)。",
        "inputs": [
            {"id": "k", "label": "导热系数 k", "value": "0.04", "step": "0.005", "unit": "W/(m·K)"},
            {"id": "A", "label": "面积 A", "value": "10", "step": "1", "unit": "米²"},
            {"id": "dT", "label": "温差 ΔT", "value": "20", "step": "2", "unit": "K"},
            {"id": "d", "label": "厚度 d", "value": "0.2", "step": "0.02", "unit": "米"},
        ],
        "calc": """
            const k=num('k'),A=num('A'),dT=num('dT'),d=num('d');
            const Qdot=k*A*dT/d;
            ToolBox.setResult('result', dataGrid([
                [Qdot.toFixed(2),'热流率 Q̇ (W)']
            ]));
        """,
        "notes": ["傅里叶导热定律。", "0.04×10×20/0.2 → 40 W。"],
    },
    {
        "slug": "wind-power-physics",
        "industry": "energy",
        "cat": "energy",
        "icon": "wind",
        "bg": "from-amber-500 to-yellow-600",
        "title": "风能功率密度计算器",
        "h1": "P = ½·ρ·A·v³",
        "h2": "由空气密度、扫风面积与风速求风能功率",
        "intro": "输入空气密度 ρ、扫风面积 A 与风速 v，求风能功率。",
        "desc": "风能功率：输入 ρ、A、v，输出 P(瓦)。",
        "inputs": [
            {"id": "rho", "label": "空气密度 ρ", "value": "1.225", "step": "0.025", "unit": "kg/m³"},
            {"id": "A", "label": "扫风面积 A", "value": "10", "step": "1", "unit": "米²"},
            {"id": "v", "label": "风速 v", "value": "10", "step": "1", "unit": "米/秒"},
        ],
        "calc": """
            const rho=num('rho'),A=num('A'),v=num('v');
            const P=0.5*rho*A*v*v*v;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2),'风能功率 P (W)']
            ]));
        """,
        "notes": ["功率与风速三次方成正比。", "0.5×1.225×10×1000 → 6125 W。"],
    },
    {
        "slug": "solar-output-physics",
        "industry": "energy",
        "cat": "energy",
        "icon": "sun",
        "bg": "from-amber-500 to-yellow-600",
        "title": "光伏输出功率计算器",
        "h1": "P = A·G·η",
        "h2": "由面积、辐照度与效率求光伏功率",
        "intro": "输入光伏面积 A、辐照度 G 与光电效率 η，求输出功率。",
        "desc": "光伏输出：输入 A、G、η，输出 P(瓦)。",
        "inputs": [
            {"id": "A", "label": "面积 A", "value": "10", "step": "1", "unit": "米²"},
            {"id": "G", "label": "辐照度 G", "value": "1000", "step": "50", "unit": "W/m²"},
            {"id": "eta", "label": "效率 η", "value": "0.2", "step": "0.02", "unit": ""},
        ],
        "calc": """
            const A=num('A'),G=num('G'),eta=num('eta');
            const P=A*G*eta;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2),'输出功率 P (W)']
            ]));
        """,
        "notes": ["标准测试条件辐照度 1000 W/m²。", "10×1000×0.2 → 2000 W。"],
    },
    {
        "slug": "specific-energy",
        "industry": "energy",
        "cat": "energy",
        "icon": "battery",
        "bg": "from-amber-500 to-yellow-600",
        "title": "比能量计算器",
        "h1": "比能量 = 能量 / 质量",
        "h2": "由能量与质量求比能量",
        "intro": "输入能量与质量，求比能量（质量能量密度）。",
        "desc": "比能量：输入 能量、质量，输出 比能量(J/kg)。",
        "inputs": [
            {"id": "E", "label": "能量 E", "value": "3600000", "step": "100000", "unit": "焦耳"},
            {"id": "m", "label": "质量 m", "value": "10", "step": "1", "unit": "千克"},
        ],
        "calc": """
            const E=num('E'),m=num('m');
            const se=E/m;
            ToolBox.setResult('result', dataGrid([
                [se.toFixed(0),'比能量 (J/kg)']
            ]));
        """,
        "notes": ["衡量储能系统质量效率。", "3600000/10 → 360000 J/kg。"],
    },
    {
        "slug": "rotational-power",
        "industry": "energy",
        "cat": "energy",
        "icon": "rotate-cw",
        "bg": "from-amber-500 to-yellow-600",
        "title": "旋转机械功率计算器",
        "h1": "P = τ·ω",
        "h2": "由扭矩与角速度求旋转功率",
        "intro": "输入扭矩 τ（牛·米）与转速（转/分），求功率。",
        "desc": "旋转功率：输入 τ(N·m)、rpm，输出 P(瓦)。",
        "inputs": [
            {"id": "tau", "label": "扭矩 τ", "value": "50", "step": "5", "unit": "N·m"},
            {"id": "rpm", "label": "转速", "value": "3000", "step": "100", "unit": "转/分"},
        ],
        "calc": """
            const tau=num('tau'),rpm=num('rpm');
            const w=rpm*2*Math.PI/60;
            const P=tau*w;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2),'旋转功率 P (W)']
            ]));
        """,
        "notes": ["角速度 ω=2π·rpm/60。", "50×314.16 → 15708 W。"],
    },
    {
        "slug": "energy-cost",
        "industry": "energy",
        "cat": "energy",
        "icon": "receipt",
        "bg": "from-amber-500 to-yellow-600",
        "title": "用电费用计算器",
        "h1": "费用 = P(kW)·h·单价",
        "h2": "由功率、时长与电价求电费",
        "intro": "输入功率 P（瓦）、用电时长 h（小时）与电价，求电费。",
        "desc": "用电费用：输入 P(W)、h、电价，输出 费用(元)。",
        "inputs": [
            {"id": "P", "label": "功率 P", "value": "1500", "step": "100", "unit": "瓦"},
            {"id": "h", "label": "时长 h", "value": "24", "step": "1", "unit": "小时"},
            {"id": "rate", "label": "电价", "value": "0.6", "step": "0.05", "unit": "元/kWh"},
        ],
        "calc": """
            const P=num('P'),h=num('h'),rate=num('rate');
            const cost=P/1000*h*rate;
            ToolBox.setResult('result', dataGrid([
                [cost.toFixed(2),'电费 (元)']
            ]));
        """,
        "notes": ["先换算为千瓦时再计费。", "1.5kW×24h×0.6 → 21.6 元。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
