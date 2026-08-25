# -*- coding: utf-8 -*-
"""Batch 19: 天文/地球物理计算深化（14 个公式计算器）。industry=astronomy。"""
from tool_template import main

G = 6.674e-11
C = 299792458.0
AU = 1.496e11
DAY = 86400.0

TOOLS = [
    {
        "slug": "kepler-third-period", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "轨道周期(开普勒三)", "h1": "开普勒第三定律轨道周期计算器",
        "h2": "轨道周期（T = 2π·√(a³ / (G·M))）",
        "intro": "圆轨道绕中心天体运行的周期由半长轴与中心质量决定。",
        "desc": "开普勒第三定律计算器：T = 2π√(a³/GM)，输出秒与天。",
        "inputs": [
            {"id": "a", "label": "半长轴", "value": "1.496e11", "step": "1e9", "unit": "m"},
            {"id": "M", "label": "中心质量", "value": "1.989e30", "step": "1e28", "unit": "kg"},
        ],
        "calc": """
            const a = num('a'), M = num('M');
            const Gc = 6.674e-11;
            const T = 2 * Math.PI * Math.sqrt(a * a * a / (Gc * M));
            ToolBox.setResult('result', dataGrid([
                [(T / 86400).toFixed(2), '轨道周期 T (天)'],
                [(T).toExponential(3), 'T (s)']
            ]));
        """,
        "notes": ["T = 2π√(a³/GM)；地球绕日约 365.2 天。", "a 取 1 AU、M 取太阳质量即得一年。"],
    },
    {
        "slug": "orbital-velocity", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "圆轨道速度", "h1": "圆轨道速度计算器",
        "h2": "轨道速度（v = √(G·M / r)）",
        "intro": "维持圆轨道所需的第一宇宙速度。",
        "desc": "圆轨道速度计算器：v = √(GM/r)，输出 m/s 与 km/s。",
        "inputs": [
            {"id": "r", "label": "轨道半径", "value": "1.496e11", "step": "1e9", "unit": "m"},
            {"id": "M", "label": "中心质量", "value": "1.989e30", "step": "1e28", "unit": "kg"},
        ],
        "calc": """
            const r = num('r'), M = num('M');
            const Gc = 6.674e-11;
            const v = Math.sqrt(Gc * M / r);
            ToolBox.setResult('result', dataGrid([
                [(v / 1000).toFixed(3), '轨道速度 v (km/s)'],
                [(v).toFixed(1), 'v (m/s)']
            ]));
        """,
        "notes": ["v = √(GM/r)；地球公转约 29.8 km/s。"],
    },
    {
        "slug": "gravitational-force", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "万有引力", "h1": "万有引力计算器",
        "h2": "引力（F = G·m₁·m₂ / r²）",
        "intro": "两质点间的万有引力。",
        "desc": "万有引力计算器：F = G·m₁·m₂/r²，默认地月参数。",
        "inputs": [
            {"id": "m1", "label": "质量 m₁", "value": "5.97e24", "step": "1e23", "unit": "kg"},
            {"id": "m2", "label": "质量 m₂", "value": "7.35e22", "step": "1e21", "unit": "kg"},
            {"id": "r", "label": "距离", "value": "3.84e8", "step": "1e7", "unit": "m"},
        ],
        "calc": """
            const m1 = num('m1'), m2 = num('m2'), r = num('r');
            const Gc = 6.674e-11;
            const F = Gc * m1 * m2 / (r * r);
            ToolBox.setResult('result', dataGrid([
                [F.toExponential(3), '引力 F (N)'],
                [(F / 1e20).toFixed(3), 'F (×10²⁰ N)']
            ]));
        """,
        "notes": ["F = G·m₁·m₂/r²；地月引力约 1.98×10²⁰ N。"],
    },
    {
        "slug": "apparent-magnitude-distance", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "视星等求距离", "h1": "视星等距离计算器",
        "h2": "距离模数（d = 10^(1 + (m−M)/5) pc）",
        "intro": "由视星等与绝对星等差求天体距离。",
        "desc": "视星等距离计算器：d = 10^(1+(m−M)/5)，输出秒差距。",
        "inputs": [
            {"id": "m", "label": "视星等 m", "value": "1", "step": "0.1"},
            {"id": "M", "label": "绝对星等 M", "value": "1", "step": "0.1"},
        ],
        "calc": """
            const m = num('m'), M = num('M');
            const d = Math.pow(10, 1 + (m - M) / 5);
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(3), '距离 d (pc)'],
                [(d * 3.262).toFixed(3), 'd (光年)']
            ]));
        """,
        "notes": ["m − M = 5·log₁₀(d) − 5；d 以秒差距计。", "m=M 时 d=10 pc。"],
    },
    {
        "slug": "hubble-redshift-distance", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "哈勃红移距离", "h1": "哈勃红移距离计算器",
        "h2": "近似距离（d = c·z / H₀）",
        "intro": "低红移下，退行速度与距离成线性关系。",
        "desc": "哈勃红移距离计算器：d = c·z/H₀，H₀=70 km/s/Mpc。",
        "inputs": [{"id": "z", "label": "红移 z", "value": "0.01", "step": "0.001"}],
        "calc": """
            const z = num('z');
            const c = 299792.458; // km/s
            const H0 = 70; // km/s/Mpc
            const d = c * z / H0;
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(2), '距离 d (Mpc)'],
                [(d * 3.262).toFixed(2), 'd (百万光年)']
            ]));
        """,
        "notes": ["d ≈ c·z/H₀（低红移近似）；H₀=70 km/s/Mpc。", "z=0.01 约 42.8 Mpc。"],
    },
    {
        "slug": "light-travel-time", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "光行时", "h1": "光行时计算器",
        "h2": "传播时间（t = d / c）",
        "intro": "光在真空中走过某段距离所需时间。",
        "desc": "光行时计算器：t = d/c，输入距离（米），输出秒与分。",
        "inputs": [{"id": "d", "label": "距离", "value": "1.496e11", "step": "1e9", "unit": "m"}],
        "calc": """
            const d = num('d');
            const c = 299792458;
            const t = d / c;
            ToolBox.setResult('result', dataGrid([
                [(t / 60).toFixed(3), '传播时间 t (min)'],
                [(t).toFixed(1), 't (s)']
            ]));
        """,
        "notes": ["t = d/c；1 AU 光行时约 8.32 分钟。"],
    },
    {
        "slug": "horizon-distance", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "地平线距离", "h1": "地平线视线距离计算器",
        "h2": "视距（d = √(2·R·h)）",
        "intro": "观察者眼高 h 能看到的地平线距离（忽略大气折射）。",
        "desc": "地平线距离计算器：d = √(2Rh)，R=6371 km，输出 km。",
        "inputs": [{"id": "h", "label": "眼高", "value": "1.7", "step": "0.1", "unit": "m"}],
        "calc": """
            const h = num('h');
            const R = 6371000;
            const d = Math.sqrt(2 * R * h);
            ToolBox.setResult('result', dataGrid([
                [(d / 1000).toFixed(3), '地平线距离 d (km)'],
                [(d).toFixed(1), 'd (m)']
            ]));
        """,
        "notes": ["d = √(2Rh)；眼高 1.7 m 约见 4.65 km 外地平线。"],
    },
    {
        "slug": "moon-illumination", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "月相照明比例", "h1": "月相照明比例计算器",
        "h2": "照明比例（k = (1 − cos(2π·D/29.53)) / 2）",
        "intro": "由农历周期中的天数估算月球被照亮的比例。",
        "desc": "月相照明计算器：k=(1−cos(2πD/29.53))/2，D 为朔后天数。",
        "inputs": [{"id": "D", "label": "朔后天数", "value": "0", "step": "0.5", "unit": "天"}],
        "calc": """
            const D = num('D');
            const k = (1 - Math.cos(2 * Math.PI * D / 29.53)) / 2;
            ToolBox.setResult('result', dataGrid([
                [(k * 100).toFixed(1), '照明比例 k (%)'],
                [(k < 0.02 ? '新月' : k > 0.98 ? '满月' : k > 0.48 && k < 0.52 ? '上/下弦' : '过渡'), '相位']
            ]));
        """,
        "notes": ["k=(1−cos(2πD/29.53))/2；D=0 新月、14.77 满月。", "D≈7.4 时约半亮（弦月）。"],
    },
    {
        "slug": "escape-velocity", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "逃逸速度", "h1": "逃逸速度计算器",
        "h2": "逃逸速度（v = √(2·G·M / R)）",
        "intro": "摆脱天体引力束缚所需最小速度。",
        "desc": "逃逸速度计算器：v = √(2GM/R)，默认地球参数。",
        "inputs": [
            {"id": "M", "label": "天体质量", "value": "5.97e24", "step": "1e23", "unit": "kg"},
            {"id": "R", "label": "天体半径", "value": "6.371e6", "step": "1e5", "unit": "m"},
        ],
        "calc": """
            const M = num('M'), R = num('R');
            const Gc = 6.674e-11;
            const v = Math.sqrt(2 * Gc * M / R);
            ToolBox.setResult('result', dataGrid([
                [(v / 1000).toFixed(3), '逃逸速度 v (km/s)'],
                [(v).toFixed(1), 'v (m/s)']
            ]));
        """,
        "notes": ["v = √(2GM/R)；地球约 11.2 km/s。"],
    },
    {
        "slug": "solar-declination", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "太阳赤纬", "h1": "太阳赤纬近似计算器",
        "h2": "赤纬（δ ≈ 23.44°·sin(360°·(284+N)/365)）",
        "intro": "由年内第 N 天估算太阳赤纬（Cooper 近似）。",
        "desc": "太阳赤纬计算器：δ ≈ 23.44°·sin(360°(284+N)/365)，输入年积日。",
        "inputs": [{"id": "N", "label": "年积日 N", "value": "172", "step": "1"}],
        "calc": """
            const N = num('N');
            const d = 23.44 * Math.sin(360 * (284 + N) / 365 * Math.PI / 180);
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(3), '太阳赤纬 δ (°)'],
                [(d > 0 ? '北半球夏半年' : '冬半年'), '半球']
            ]));
        """,
        "notes": ["δ ≈ 23.44°·sin(360°(284+N)/365)；N=172(夏至)≈+23.44°。", "N=355(冬至)≈−23.44°。"],
    },
    {
        "slug": "atmospheric-refraction", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "大气折射", "h1": "大气折射计算器",
        "h2": "折射量（R = 1.02 / tan(h + 10.3/(h+5.11)) ′）",
        "intro": "近地面大气使天体视高度抬升（Bennett 近似，单位角分）。",
        "desc": "大气折射计算器：Bennett 公式 R(角分)，输入真高度角。",
        "inputs": [{"id": "h", "label": "真高度角", "value": "30", "step": "1", "unit": "°"}],
        "calc": """
            const h = num('h');
            const R = 1.02 / Math.tan((h + 10.3 / (h + 5.11)) * Math.PI / 180);
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(3), '大气折射 R (′)'],
                [(R / 60).toFixed(4), 'R (°)']
            ]));
        """,
        "notes": ["R = 1.02 / tan(h + 10.3/(h+5.11)) 角分（Bennett 近似）。", "高度越低折射越大，天顶处趋近 0。"],
    },
    {
        "slug": "stellar-parallax", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "恒星视差测距", "h1": "恒星视差距离计算器",
        "h2": "视差距离（d = 1 / p pc）",
        "intro": "周年视差 p（角秒）与距离（秒差距）互为倒数。",
        "desc": "恒星视差测距计算器：d = 1/p，p 单位角秒，输出秒差距与光年。",
        "inputs": [{"id": "p", "label": "视差 p", "value": "0.1", "step": "0.001", "unit": "″"}],
        "calc": """
            const p = num('p');
            const d = 1 / p;
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(3), '距离 d (pc)'],
                [(d * 3.262).toFixed(3), 'd (光年)']
            ]));
        """,
        "notes": ["d(pc) = 1/p(″)；p=0.1″ 对应 10 pc。"],
    },
    {
        "slug": "kepler-equation", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "开普勒方程", "h1": "开普勒方程求解器",
        "h2": "M = E − e·sinE（牛顿迭代求 E）",
        "intro": "由平近点角 M 与偏心率 e 数值求解偏近点角 E。",
        "desc": "开普勒方程计算器：牛顿迭代解 E，输入 M(°) 与 e。",
        "inputs": [
            {"id": "Mdeg", "label": "平近点角 M", "value": "90", "step": "1", "unit": "°"},
            {"id": "e", "label": "偏心率 e", "value": "0.1", "step": "0.01"},
        ],
        "calc": """
            const M = num('Mdeg') * Math.PI / 180;
            const e = num('e');
            let E = M;
            for (let i = 0; i < 50; i++) {
                const f = E - e * Math.sin(E) - M;
                const fp = 1 - e * Math.cos(E);
                E = E - f / fp;
            }
            ToolBox.setResult('result', dataGrid([
                [(E * 180 / Math.PI).toFixed(3), '偏近点角 E (°)'],
                [(E).toFixed(5), 'E (rad)']
            ]));
        """,
        "notes": ["M = E − e·sinE；牛顿迭代收敛快。", "e=0.1、M=90° 时 E≈95.7°。"],
    },
    {
        "slug": "schwarzschild-radius", "industry": "astronomy", "cat": "astronomy", "icon": "🔭", "bg": "#e0f2fe",
        "title": "史瓦西半径", "h1": "史瓦西半径计算器",
        "h2": "事件视界（r_s = 2·G·M / c²）",
        "intro": "质量 M 坍缩成黑洞的事件视界半径。",
        "desc": "史瓦西半径计算器：r_s = 2GM/c²，默认太阳质量。",
        "inputs": [{"id": "M", "label": "质量 M", "value": "1.989e30", "step": "1e28", "unit": "kg"}],
        "calc": """
            const M = num('M');
            const Gc = 6.674e-11, c = 299792458;
            const rs = 2 * Gc * M / (c * c);
            ToolBox.setResult('result', dataGrid([
                [(rs / 1000).toFixed(3), '史瓦西半径 r_s (km)'],
                [(rs).toFixed(1), 'r_s (m)']
            ]));
        """,
        "notes": ["r_s = 2GM/c²；太阳质量约 2.95 km。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
