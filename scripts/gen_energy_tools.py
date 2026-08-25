# -*- coding: utf-8 -*-
"""Batch 39: 能源计算深化（14 个公式计算器）。industry=energy。"""
from tool_template import main

TOOLS = [
    {
        "slug": "solar-panel-power",
        "industry": "energy",
        "cat": "energy",
        "icon": "sun",
        "bg": "from-yellow-500 to-amber-600",
        "title": "光伏阵列功率",
        "h1": "光伏阵列功率",
        "h2": "面积 × 辐照度 × 效率",
        "intro": "P = A × G × η。",
        "desc": "输入阵列面积、峰值辐照度与组件效率，计算输出功率。",
        "inputs": [
            {"id": "a", "label": "阵列面积 A", "value": "20", "step": "1", "unit": "m²"},
            {"id": "g", "label": "辐照度 G", "value": "1000", "step": "50", "unit": "W/m²"},
            {"id": "eta", "label": "效率 η", "value": "0.2", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const A=num('a'),G=num('g'),e=num('eta');
            const P=A*G*e;
            ToolBox.setResult('result', dataGrid([
                [(P/1000).toFixed(2),'输出功率 (kW)'],
                [P.toFixed(0),'输出功率 (W)']
            ]));
        """,
        "notes": ["标准测试条件 G=1000 W/m²。", "实际受温度与遮挡影响。"],
    },
    {
        "slug": "battery-capacity-wh",
        "industry": "energy",
        "cat": "energy",
        "icon": "battery",
        "bg": "from-yellow-500 to-amber-600",
        "title": "电池容量换算",
        "h1": "电池容量换算",
        "h2": "Ah ↔ Wh",
        "intro": "能量 (Wh) = 容量 (Ah) × 电压 (V)。",
        "desc": "输入容量与电压，计算电池能量；并可估算续航。",
        "inputs": [
            {"id": "ah", "label": "容量 (Ah)", "value": "50", "step": "5", "unit": "Ah"},
            {"id": "v", "label": "电压 (V)", "value": "12", "step": "1", "unit": "V"},
            {"id": "load", "label": "负载功率", "value": "100", "step": "10", "unit": "W"},
        ],
        "calc": """
            const ah=num('ah'),v=num('v'),L=num('load');
            const wh=ah*v;
            const hrs=wh/L;
            ToolBox.setResult('result', dataGrid([
                [wh.toFixed(0),'能量 (Wh)'],
                [hrs.toFixed(2),'续航 (h)'],
                [(hrs*60).toFixed(0),'续航 (min)']
            ]));
        """,
        "notes": ["Wh = Ah × V。", "续航 = 能量/负载功率。"],
    },
    {
        "slug": "energy-consumption",
        "industry": "energy",
        "cat": "energy",
        "icon": "zap",
        "bg": "from-yellow-500 to-amber-600",
        "title": "能耗计算",
        "h1": "能耗计算",
        "h2": "功率 × 时间",
        "intro": "E = P × t。",
        "desc": "输入功率与运行时间，计算消耗电能与电费。",
        "inputs": [
            {"id": "p", "label": "功率 P", "value": "1500", "step": "100", "unit": "W"},
            {"id": "t", "label": "时间 t", "value": "3", "step": "0.5", "unit": "h"},
            {"id": "price", "label": "电价", "value": "0.6", "step": "0.05", "unit": "元/kWh"},
        ],
        "calc": """
            const p=num('p'),t=num('t'),pr=num('price');
            const kwh=p*t/1000;
            ToolBox.setResult('result', dataGrid([
                [kwh.toFixed(2),'耗电量 (kWh)'],
                [(kwh*pr).toFixed(2),'电费 (元)']
            ]));
        """,
        "notes": ["注意 W→kW 除以 1000。", "峰谷电价不同。"],
    },
    {
        "slug": "fuel-heat-value",
        "industry": "energy",
        "cat": "energy",
        "icon": "flame",
        "bg": "from-yellow-500 to-amber-600",
        "title": "燃料热值能量",
        "h1": "燃料热值能量",
        "h2": "质量 × 低位热值",
        "intro": "Q = m × H。",
        "desc": "输入燃料质量与低位热值，计算释放能量。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "1000", "step": "100", "unit": "kg"},
            {"id": "h", "label": "低位热值", "value": "42000", "step": "1000", "unit": "kJ/kg"},
        ],
        "calc": """
            const m=num('m'),h=num('h');
            const Q=m*h;
            ToolBox.setResult('result', dataGrid([
                [(Q/1000).toFixed(1),'能量 (MJ)'],
                [(Q/3.6e6).toFixed(3),'能量 (kWh)']
            ]));
        """,
        "notes": ["1 kWh = 3.6 MJ。", "标煤热值约 29307 kJ/kg。"],
    },
    {
        "slug": "cop-heatpump",
        "industry": "energy",
        "cat": "energy",
        "icon": "thermometer",
        "bg": "from-yellow-500 to-amber-600",
        "title": "热泵 COP",
        "h1": "热泵能效比 COP",
        "h2": "制热量 / 耗电量",
        "intro": "COP = Q / W。",
        "desc": "输入制热量与耗电功率，计算能效比。",
        "inputs": [
            {"id": "q", "label": "制热量", "value": "4000", "step": "200", "unit": "W"},
            {"id": "w", "label": "耗电功率", "value": "1000", "step": "100", "unit": "W"},
        ],
        "calc": """
            const q=num('q'),w=num('w');
            ToolBox.setResult('result', dataGrid([
                [(q/w).toFixed(2),'COP'],
                [((q-w)/q*100).toFixed(1),'节电率 (%)']
            ]));
        """,
        "notes": ["COP 越高越省电。", "COP>1 因吸收环境热量。"],
    },
    {
        "slug": "lcoe",
        "industry": "energy",
        "cat": "energy",
        "icon": "trending-down",
        "bg": "from-yellow-500 to-amber-600",
        "title": "平准化度电成本 (LCOE)",
        "h1": "LCOE",
        "h2": "生命周期成本 / 发电量",
        "intro": "LCOE = (CAPEX·CRF + O&M) / 年发电量。",
        "desc": "输入初投资、年限、折现率、年运维与年发电量，计算度电成本。",
        "inputs": [
            {"id": "capex", "label": "初投资", "value": "5000000", "step": "500000", "unit": "元"},
            {"id": "n", "label": "年限", "value": "20", "step": "1", "unit": "年"},
            {"id": "r", "label": "折现率 r", "value": "0.06", "step": "0.005", "unit": ""},
            {"id": "om", "label": "年运维", "value": "100000", "step": "10000", "unit": "元"},
            {"id": "e", "label": "年发电量", "value": "1200000", "step": "100000", "unit": "kWh"},
        ],
        "calc": """
            const C=num('capex'),n=num('n'),r=num('r'),om=num('om'),E=num('e');
            const crf=r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1);
            const lcoe=(C*crf+om)/E;
            ToolBox.setResult('result', dataGrid([
                [lcoe.toFixed(3),'LCOE (元/kWh)'],
                [crf.toFixed(4),'资本回收因子 CRF']
            ]));
        """,
        "notes": ["CRF = r(1+r)^n/((1+r)^n−1)。", "LCOE 越低竞争力越强。"],
    },
    {
        "slug": "power-factor",
        "industry": "energy",
        "cat": "energy",
        "icon": "gauge",
        "bg": "from-yellow-500 to-amber-600",
        "title": "功率因数",
        "h1": "功率因数",
        "h2": "有功 / 视在",
        "intro": "PF = P / S = cos φ。",
        "desc": "输入有功功率与视在功率，计算功率因数。",
        "inputs": [
            {"id": "p", "label": "有功功率 P", "value": "800", "step": "50", "unit": "kW"},
            {"id": "s", "label": "视在功率 S", "value": "1000", "step": "50", "unit": "kVA"},
        ],
        "calc": """
            const p=num('p'),s=num('s');
            const pf=p/s;
            ToolBox.setResult('result', dataGrid([
                [pf.toFixed(3),'功率因数 PF'],
                [(Math.acos(pf)*180/Math.PI).toFixed(2),'相位角 φ (°)']
            ]));
        """,
        "notes": ["PF 低需无功补偿。", "PF=cos φ。"],
    },
    {
        "slug": "three-phase-power",
        "industry": "energy",
        "cat": "energy",
        "icon": "plug",
        "bg": "from-yellow-500 to-amber-600",
        "title": "三相有功功率",
        "h1": "三相功率",
        "h2": "P = √3·U·I·cosφ",
        "intro": "三相 P = √3 × 线电压 × 线电流 × 功率因数。",
        "desc": "输入线电压、线电流与功率因数，计算三相有功功率。",
        "inputs": [
            {"id": "u", "label": "线电压 U", "value": "380", "step": "10", "unit": "V"},
            {"id": "i", "label": "线电流 I", "value": "100", "step": "10", "unit": "A"},
            {"id": "pf", "label": "功率因数", "value": "0.9", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const u=num('u'),i=num('i'),pf=num('pf');
            const P=Math.sqrt(3)*u*i*pf;
            ToolBox.setResult('result', dataGrid([
                [(P/1000).toFixed(2),'有功功率 (kW)']
            ]));
        """,
        "notes": ["线电压 380 V 为常见低压。", "忽略线损。"],
    },
    {
        "slug": "energy-payback",
        "industry": "energy",
        "cat": "energy",
        "icon": "clock",
        "bg": "from-yellow-500 to-amber-600",
        "title": "节能投资回收期",
        "h1": "投资回收期",
        "h2": "投资 / 年节约",
        "intro": "回收期 = 初投资 / 年节约。",
        "desc": "输入项目初投资与年节约金额，计算静态回收期。",
        "inputs": [
            {"id": "inv", "label": "初投资", "value": "30000", "step": "1000", "unit": "元"},
            {"id": "save", "label": "年节约", "value": "6000", "step": "500", "unit": "元/年"},
        ],
        "calc": """
            const inv=num('inv'),s=num('save');
            ToolBox.setResult('result', dataGrid([
                [(inv/s).toFixed(2),'回收期 (年)'],
                [(s/inv*100).toFixed(1),'年回报率 (%)']
            ]));
        """,
        "notes": ["静态回收忽略折现。", "含折现需用动态回收期。"],
    },
    {
        "slug": "energy-density",
        "industry": "energy",
        "cat": "energy",
        "icon": "box",
        "bg": "from-yellow-500 to-amber-600",
        "title": "能量密度",
        "h1": "能量密度",
        "h2": "能量 / 质量",
        "intro": "ρ_E = E / m。",
        "desc": "输入能量与质量，计算质量能量密度。",
        "inputs": [
            {"id": "e", "label": "能量 E", "value": "3600000", "step": "100000", "unit": "J"},
            {"id": "m", "label": "质量 m", "value": "10", "step": "1", "unit": "kg"},
        ],
        "calc": """
            const e=num('e'),m=num('m');
            ToolBox.setResult('result', dataGrid([
                [(e/m/1000).toFixed(1),'能量密度 (kJ/kg)'],
                [(e/m/3.6e6).toFixed(4),'能量密度 (kWh/kg)']
            ]));
        """,
        "notes": ["锂电约 0.1–0.3 kWh/kg。", "汽油约 12 kWh/kg。"],
    },
    {
        "slug": "daily-irradiation",
        "industry": "energy",
        "cat": "energy",
        "icon": "sunrise",
        "bg": "from-yellow-500 to-amber-600",
        "title": "日辐照量估算",
        "h1": "日辐照量",
        "h2": "峰值 × 等效日照时数",
        "intro": "H = G_peak × t_equiv。",
        "desc": "输入峰值辐照度与等效满发小时数，估算日均辐照量。",
        "inputs": [
            {"id": "g", "label": "峰值辐照度", "value": "1000", "step": "50", "unit": "W/m²"},
            {"id": "t", "label": "等效满发时长", "value": "4.5", "step": "0.5", "unit": "h"},
        ],
        "calc": """
            const g=num('g'),t=num('t');
            ToolBox.setResult('result', dataGrid([
                [(g*t/1000).toFixed(2),'日辐照量 (kWh/m²)']
            ]));
        """,
        "notes": ["我国一类资源区等效时数约 1600 h/年。", "等效时数含天气折减。"],
    },
    {
        "slug": "wind-power",
        "industry": "energy",
        "cat": "energy",
        "icon": "wind",
        "bg": "from-yellow-500 to-amber-600",
        "title": "风力发电功率",
        "h1": "风功率",
        "h2": "P = ½ρA v³ Cp",
        "intro": "P = ½·ρ·A·v³·Cp。",
        "desc": "输入空气密度、风轮半径、风速与功率系数，计算风能捕获功率。",
        "inputs": [
            {"id": "rho", "label": "空气密度 ρ", "value": "1.225", "step": "0.01", "unit": "kg/m³"},
            {"id": "r", "label": "风轮半径", "value": "40", "step": "5", "unit": "m"},
            {"id": "v", "label": "风速 v", "value": "10", "step": "1", "unit": "m/s"},
            {"id": "cp", "label": "功率系数 Cp", "value": "0.4", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const rho=num('rho'),r=num('r'),v=num('v'),cp=num('cp');
            const A=Math.PI*r*r;
            const P=0.5*rho*A*Math.pow(v,3)*cp;
            ToolBox.setResult('result', dataGrid([
                [(P/1000).toFixed(2),'捕获功率 (kW)'],
                [A.toFixed(1),'扫风面积 (m²)']
            ]));
        """,
        "notes": ["贝兹极限 Cp≤0.593。", "功率与风速立方成正比。"],
    },
    {
        "slug": "fuel-cost",
        "industry": "energy",
        "cat": "energy",
        "icon": "coins",
        "bg": "from-yellow-500 to-amber-600",
        "title": "燃料费用计算",
        "h1": "燃料费用",
        "h2": "用量 × 单价",
        "intro": "费用 = 用量 × 单价。",
        "desc": "输入燃料用量与单价，计算费用；可换算单位里程成本。",
        "inputs": [
            {"id": "q", "label": "燃料用量", "value": "50", "step": "5", "unit": "L"},
            {"id": "price", "label": "单价", "value": "8", "step": "0.2", "unit": "元/L"},
            {"id": "dist", "label": "行驶里程", "value": "600", "step": "50", "unit": "km"},
        ],
        "calc": """
            const q=num('q'),p=num('price'),d=num('dist');
            const cost=q*p;
            ToolBox.setResult('result', dataGrid([
                [cost.toFixed(2),'燃料费 (元)'],
                [(cost/d).toFixed(2),'单位里程 (元/km)']
            ]));
        """,
        "notes": ["百公里成本 = 10×单位里程。", "电/气同理替换单位。"],
    },
    {
        "slug": "thermal-efficiency",
        "industry": "energy",
        "cat": "energy",
        "icon": "percent",
        "bg": "from-yellow-500 to-amber-600",
        "title": "热效率",
        "h1": "热效率",
        "h2": "输出 / 输入",
        "intro": "η = 有效输出 / 能量输入。",
        "desc": "输入输出能量与输入能量，计算热效率。",
        "inputs": [
            {"id": "out", "label": "有效输出", "value": "300", "step": "10", "unit": "kJ"},
            {"id": "in", "label": "能量输入", "value": "1000", "step": "50", "unit": "kJ"},
        ],
        "calc": """
            const o=num('out'),i=num('in');
            ToolBox.setResult('result', dataGrid([
                [(o/i*100).toFixed(2),'热效率 (%)'],
                [((1-o/i)*100).toFixed(2),'损失率 (%)']
            ]));
        """,
        "notes": ["受卡诺效率上限约束。", "提高 η 是节能关键。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
