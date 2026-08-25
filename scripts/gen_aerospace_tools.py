# -*- coding: utf-8 -*-
"""Batch 40: 航空航天计算深化（14 个公式计算器）。industry=aerospace。"""
from tool_template import main

TOOLS = [
    {
        "slug": "lift-force",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "plane",
        "bg": "from-sky-500 to-blue-600",
        "title": "升力计算",
        "h1": "机翼升力",
        "h2": "L = ½ρV²S·C_L",
        "intro": "L = ½·ρ·V²·S·C_L。",
        "desc": "输入空气密度、速度、机翼面积与升力系数，计算升力。",
        "inputs": [
            {"id": "rho", "label": "空气密度 ρ", "value": "1.225", "step": "0.01", "unit": "kg/m³"},
            {"id": "v", "label": "空速 V", "value": "80", "step": "5", "unit": "m/s"},
            {"id": "s", "label": "机翼面积 S", "value": "16", "step": "1", "unit": "m²"},
            {"id": "cl", "label": "升力系数 C_L", "value": "1.2", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const rho=num('rho'),v=num('v'),S=num('s'),cl=num('cl');
            const L=0.5*rho*v*v*S*cl;
            ToolBox.setResult('result', dataGrid([
                [(L/1000).toFixed(2),'升力 L (kN)'],
                [(L/9.81).toFixed(1),'升力 (kgf)']
            ]));
        """,
        "notes": ["低速近似不可压。", "C_L 随迎角变化。"],
    },
    {
        "slug": "lift-to-drag-ratio",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "scale",
        "bg": "from-sky-500 to-blue-600",
        "title": "升阻比",
        "h1": "升阻比 L/D",
        "h2": "气动效率",
        "intro": "(L/D) = C_L / C_D。",
        "desc": "输入升力与阻力系数，计算升阻比。",
        "inputs": [
            {"id": "cl", "label": "升力系数 C_L", "value": "1.0", "step": "0.1", "unit": ""},
            {"id": "cd", "label": "阻力系数 C_D", "value": "0.05", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const cl=num('cl'),cd=num('cd');
            ToolBox.setResult('result', dataGrid([
                [(cl/cd).toFixed(2),'升阻比 L/D'],
                [(cd/cl*100).toFixed(2),'阻力占比 (%)']
            ]));
        """,
        "notes": ["升阻比越高越省油。", "滑翔机可达 40+。"],
    },
    {
        "slug": "mach-number",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "zap",
        "bg": "from-sky-500 to-blue-600",
        "title": "马赫数",
        "h1": "马赫数",
        "h2": "M = V / a",
        "intro": "a = √(γRT)，M = V/a。",
        "desc": "输入速度、温度（℃）与比热比，计算声速与马赫数。",
        "inputs": [
            {"id": "v", "label": "速度 V", "value": "340", "step": "10", "unit": "m/s"},
            {"id": "t", "label": "温度 T", "value": "15", "step": "1", "unit": "°C"},
            {"id": "g", "label": "比热比 γ", "value": "1.4", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const v=num('v'),T=num('t')+273.15,gamma=num('g');
            const a=Math.sqrt(gamma*287*T);
            ToolBox.setResult('result', dataGrid([
                [(v/a).toFixed(3),'马赫数 M'],
                [a.toFixed(1),'声速 a (m/s)']
            ]));
        """,
        "notes": ["15°C 海平面声速约 340 m/s。", "M>1 为超声速。"],
    },
    {
        "slug": "thrust-required",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "rocket",
        "bg": "from-sky-500 to-blue-600",
        "title": "所需推力",
        "h1": "所需推力",
        "h2": "平飞 T = D",
        "intro": "T = ½ρV²S·C_D。",
        "desc": "输入空气密度、速度、面积与阻力系数，计算平飞所需推力。",
        "inputs": [
            {"id": "rho", "label": "空气密度 ρ", "value": "1.225", "step": "0.01", "unit": "kg/m³"},
            {"id": "v", "label": "速度 V", "value": "80", "step": "5", "unit": "m/s"},
            {"id": "s", "label": "参考面积 S", "value": "16", "step": "1", "unit": "m²"},
            {"id": "cd", "label": "阻力系数 C_D", "value": "0.05", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const rho=num('rho'),v=num('v'),S=num('s'),cd=num('cd');
            const T=0.5*rho*v*v*S*cd;
            ToolBox.setResult('result', dataGrid([
                [(T/1000).toFixed(3),'所需推力 (kN)']
            ]));
        """,
        "notes": ["平飞时推力等于阻力。", "与升力共用动压项。"],
    },
    {
        "slug": "stall-speed",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "alert-triangle",
        "bg": "from-sky-500 to-blue-600",
        "title": "失速速度",
        "h1": "失速速度",
        "h2": "V_s = √(2W/(ρS·C_Lmax))",
        "intro": "失速速度由最大升力系数决定。",
        "desc": "输入重量、密度、面积与最大升力系数，计算失速速度。",
        "inputs": [
            {"id": "w", "label": "重量 W", "value": "10000", "step": "500", "unit": "N"},
            {"id": "rho", "label": "密度 ρ", "value": "1.225", "step": "0.01", "unit": "kg/m³"},
            {"id": "s", "label": "面积 S", "value": "16", "step": "1", "unit": "m²"},
            {"id": "cl", "label": "C_Lmax", "value": "1.5", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const W=num('w'),rho=num('rho'),S=num('s'),cl=num('cl');
            const vs=Math.sqrt(2*W/(rho*S*cl));
            ToolBox.setResult('result', dataGrid([
                [vs.toFixed(2),'失速速度 (m/s)'],
                [(vs*3.6).toFixed(1),'失速速度 (km/h)']
            ]));
        """,
        "notes": ["重量越大失速越快。", "增升装置提高 C_Lmax 降低 V_s。"],
    },
    {
        "slug": "turn-radius",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "refresh-cw",
        "bg": "from-sky-500 to-blue-600",
        "title": "转弯半径",
        "h1": "协调转弯半径",
        "h2": "R = V² / (g·tan φ)",
        "intro": "R = V² / (g·tan φ)。",
        "desc": "输入速度与坡度角，计算协调转弯半径。",
        "inputs": [
            {"id": "v", "label": "速度 V", "value": "100", "step": "5", "unit": "m/s"},
            {"id": "phi", "label": "坡度角 φ", "value": "30", "step": "2", "unit": "°"},
        ],
        "calc": """
            const v=num('v'),phi=num('phi')*Math.PI/180;
            const R=v*v/(9.81*Math.tan(phi));
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(1),'转弯半径 (m)']
            ]));
        """,
        "notes": ["坡度越大半径越小。", "大坡度需更高速度维持升力的水平分量。"],
    },
    {
        "slug": "turn-rate",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "rotate-cw",
        "bg": "from-sky-500 to-blue-600",
        "title": "转弯角速度",
        "h1": "转弯角速度",
        "h2": "ω = g·tan φ / V",
        "intro": "ω = g·tan φ / V。",
        "desc": "输入速度与坡度角，计算转弯角速度（°/s）。",
        "inputs": [
            {"id": "v", "label": "速度 V", "value": "100", "step": "5", "unit": "m/s"},
            {"id": "phi", "label": "坡度角 φ", "value": "30", "step": "2", "unit": "°"},
        ],
        "calc": """
            const v=num('v'),phi=num('phi')*Math.PI/180;
            const w=9.81*Math.tan(phi)/v;
            ToolBox.setResult('result', dataGrid([
                [(w*180/Math.PI).toFixed(2),'角速度 (°/s)'],
                [(60*w*180/Math.PI).toFixed(1),'转弯率 (°/min)']
            ]));
        """,
        "notes": ["与转弯半径互为倒易。", "战斗机追求高转弯率。"],
    },
    {
        "slug": "load-factor",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "weight",
        "bg": "from-sky-500 to-blue-600",
        "title": "载荷因子",
        "h1": "载荷因子 n",
        "h2": "n = 1 / cos φ",
        "intro": "协调转弯载荷因子 n = 1/cos φ。",
        "desc": "输入坡度角，计算载荷因子及等效过载。",
        "inputs": [
            {"id": "phi", "label": "坡度角 φ", "value": "60", "step": "2", "unit": "°"},
        ],
        "calc": """
            const phi=num('phi')*Math.PI/180;
            const n=1/Math.cos(phi);
            ToolBox.setResult('result', dataGrid([
                [n.toFixed(2),'载荷因子 n'],
                [(n).toFixed(2),'等效 g']
            ]));
        """,
        "notes": ["坡度 60° 时 n=2。", "结构需承受相应过载。"],
    },
    {
        "slug": "breguet-range",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "map",
        "bg": "from-sky-500 to-blue-600",
        "title": "布雷盖航程",
        "h1": "布雷盖航程",
        "h2": "R = (V·L/D / g)·ln(W_i/W_f)",
        "intro": "螺旋桨飞机航程公式。",
        "desc": "输入速度、升阻比、初重与终重，计算航程。",
        "inputs": [
            {"id": "v", "label": "速度 V", "value": "120", "step": "5", "unit": "m/s"},
            {"id": "ld", "label": "升阻比 L/D", "value": "12", "step": "1", "unit": ""},
            {"id": "wi", "label": "起飞重量", "value": "12000", "step": "500", "unit": "N"},
            {"id": "wf", "label": "着陆重量", "value": "8000", "step": "500", "unit": "N"},
        ],
        "calc": """
            const v=num('v'),ld=num('ld'),wi=num('wi'),wf=num('wf');
            const R=v*ld/9.81*Math.log(wi/wf);
            ToolBox.setResult('result', dataGrid([
                [(R/1000).toFixed(1),'航程 (km)'],
                [(R/1852).toFixed(1),'航程 (n mile)']
            ]));
        """,
        "notes": ["航程随升阻比对数增长。", "喷气式用燃油消耗率形式。"],
    },
    {
        "slug": "climb-rate",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "trending-up",
        "bg": "from-sky-500 to-blue-600",
        "title": "爬升率",
        "h1": "爬升率 (ROC)",
        "h2": "ROC = (P_av − P_req) / W",
        "intro": "多余功率决定爬升率。",
        "desc": "输入可用功率、所需功率与重量，计算爬升率。",
        "inputs": [
            {"id": "pav", "label": "可用功率", "value": "200000", "step": "10000", "unit": "W"},
            {"id": "preq", "label": "所需功率", "value": "120000", "step": "10000", "unit": "W"},
            {"id": "w", "label": "重量 W", "value": "10000", "step": "500", "unit": "N"},
        ],
        "calc": """
            const pav=num('pav'),preq=num('preq'),w=num('w');
            const roc=(pav-preq)/w;
            ToolBox.setResult('result', dataGrid([
                [roc.toFixed(2),'爬升率 (m/s)'],
                [(roc*60).toFixed(1),'爬升率 (m/min)']
            ]));
        """,
        "notes": ["多余功率越大爬升越快。", "静止时 ROC=0（平飞极限）。"],
    },
    {
        "slug": "wing-loading",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "layout",
        "bg": "from-sky-500 to-blue-600",
        "title": "翼载荷",
        "h1": "翼载荷 W/S",
        "h2": "重量 / 机翼面积",
        "intro": "翼载荷 = W / S。",
        "desc": "输入重量与机翼面积，计算翼载荷（N/m²）。",
        "inputs": [
            {"id": "w", "label": "重量 W", "value": "10000", "step": "500", "unit": "N"},
            {"id": "s", "label": "机翼面积 S", "value": "16", "step": "1", "unit": "m²"},
        ],
        "calc": """
            const w=num('w'),s=num('s');
            ToolBox.setResult('result', dataGrid([
                [(w/s).toFixed(1),'翼载荷 (N/m²)'],
                [(w/s/9.81).toFixed(2),'翼载荷 (kgf/m²)']
            ]));
        """,
        "notes": ["高翼载荷→高速低机动。", "战斗机翼载荷高于滑翔机。"],
    },
    {
        "slug": "specific-impulse",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "gauge",
        "bg": "from-sky-500 to-blue-600",
        "title": "火箭比冲",
        "h1": "比冲 Isp",
        "h2": "Isp = F / (ṁ·g₀)",
        "intro": "比冲 = 推力 / (质量流率×g₀)。",
        "desc": "输入推力与质量流率，计算比冲（秒）。",
        "inputs": [
            {"id": "f", "label": "推力 F", "value": "100000", "step": "5000", "unit": "N"},
            {"id": "mdot", "label": "质量流率 ṁ", "value": "40", "step": "2", "unit": "kg/s"},
        ],
        "calc": """
            const f=num('f'),md=num('mdot');
            const isp=f/(md*9.81);
            ToolBox.setResult('result', dataGrid([
                [isp.toFixed(1),'比冲 Isp (s)']
            ]));
        """,
        "notes": ["比冲越高推进效率越高。", "液氢氧可达 450 s。"],
    },
    {
        "slug": "delta-v-rocket",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "rocket",
        "bg": "from-sky-500 to-blue-600",
        "title": "火箭速度增量",
        "h1": "齐奥尔科夫斯基公式",
        "h2": "Δv = Isp·g₀·ln(m₀/m_f)",
        "intro": "Δv = Isp·g₀·ln(m₀/m_f)。",
        "desc": "输入比冲、初重与终重，计算速度增量。",
        "inputs": [
            {"id": "isp", "label": "比冲 Isp", "value": "300", "step": "10", "unit": "s"},
            {"id": "m0", "label": "初始质量", "value": "500000", "step": "10000", "unit": "kg"},
            {"id": "mf", "label": "最终质量", "value": "100000", "step": "10000", "unit": "kg"},
        ],
        "calc": """
            const isp=num('isp'),m0=num('m0'),mf=num('mf');
            const dv=isp*9.81*Math.log(m0/mf);
            ToolBox.setResult('result', dataGrid([
                [(dv/1000).toFixed(2),'速度增量 Δv (km/s)'],
                [dv.toFixed(0),'Δv (m/s)']
            ]));
        """,
        "notes": ["质量比越大 Δv 越大。", "多级火箭提高有效质量比。"],
    },
    {
        "slug": "descent-rate",
        "industry": "aerospace",
        "cat": "aerospace",
        "icon": "arrow-down",
        "bg": "from-sky-500 to-blue-600",
        "title": "下降率",
        "h1": "下降率",
        "h2": "Sink = V·sin γ",
        "intro": "下降率 = 真空速 × sin(航迹角)。",
        "desc": "输入真空速与航迹角（下降为负），计算下降率。",
        "inputs": [
            {"id": "v", "label": "真空速 V", "value": "70", "step": "5", "unit": "m/s"},
            {"id": "g", "label": "航迹角 γ", "value": "-3", "step": "0.5", "unit": "°"},
        ],
        "calc": """
            const v=num('v'),gamma=num('g')*Math.PI/180;
            const sink=v*Math.sin(gamma);
            ToolBox.setResult('result', dataGrid([
                [(sink*60).toFixed(1),'下降率 (m/min)'],
                [sink.toFixed(2),'下降率 (m/s)']
            ]));
        """,
        "notes": ["负角表示下降。", "进近常用 3° 下滑角。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
