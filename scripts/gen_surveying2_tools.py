# -*- coding: utf-8 -*-
"""Batch 68: 测绘学深化 II（14 个公式计算器）。industry=surveying。"""
from tool_template import main

TOOLS = [
    {
        "slug": "coordinate-distance-2d",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "map-pin",
        "bg": "from-lime-500 to-green-600",
        "title": "坐标距离(平面)计算器",
        "h1": "D = √[(x₂−x₁)² + (y₂−y₁)²]",
        "h2": "由两点平面坐标求水平距离",
        "intro": "输入两点平面坐标 (x₁,y₁) 与 (x₂,y₂)，求水平距离。",
        "desc": "平面坐标距离：输入 x1、y1、x2、y2，输出 D。",
        "inputs": [
            {"id": "x1", "label": "x₁", "value": "0", "step": "1", "unit": "米"},
            {"id": "y1", "label": "y₁", "value": "0", "step": "1", "unit": "米"},
            {"id": "x2", "label": "x₂", "value": "3", "step": "1", "unit": "米"},
            {"id": "y2", "label": "y₂", "value": "4", "step": "1", "unit": "米"},
        ],
        "calc": """
            const x1=num('x1'),y1=num('y1'),x2=num('x2'),y2=num('y2');
            const D=Math.sqrt(Math.pow(x2-x1,2)+Math.pow(y2-y1,2));
            ToolBox.setResult('result', dataGrid([
                [D.toFixed(3),'水平距离 D (米)']
            ]));
        """,
        "notes": ["平面直角坐标系中两点距离。", "(0,0)→(3,4) → 5 米。"],
    },
    {
        "slug": "bearing-from-coordinates",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "compass",
        "bg": "from-lime-500 to-green-600",
        "title": "坐标方位角计算器",
        "h1": "α = atan2(ΔE, ΔN)",
        "h2": "由坐标增量求方位角",
        "intro": "输入北向增量 ΔN 与东向增量 ΔE，求方位角（0–360°）。",
        "desc": "坐标方位角：输入 ΔN、ΔE，输出 α(度)。",
        "inputs": [
            {"id": "dN", "label": "北向增量 ΔN", "value": "100", "step": "5", "unit": "米"},
            {"id": "dE", "label": "东向增量 ΔE", "value": "100", "step": "5", "unit": "米"},
        ],
        "calc": """
            const dN=num('dN'),dE=num('dE');
            let a=Math.atan2(dE,dN)*180/Math.PI;
            if(a<0)a+=360;
            ToolBox.setResult('result', dataGrid([
                [a.toFixed(2),'方位角 α (°)']
            ]));
        """,
        "notes": ["atan2(东,北) 保证象限正确。", "ΔN=ΔE=100 → 45°。"],
    },
    {
        "slug": "bearing-to-offset",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "crosshair",
        "bg": "from-lime-500 to-green-600",
        "title": "方位角推坐标计算器",
        "h1": "N = D·cosα, E = D·sinα",
        "h2": "由距离与方位角求坐标增量",
        "intro": "输入距离 D 与方位角 α（度），求北向与东向增量。",
        "desc": "方位推坐标：输入 D、α(度)，输出 ΔN、ΔE。",
        "inputs": [
            {"id": "D", "label": "距离 D", "value": "100", "step": "5", "unit": "米"},
            {"id": "a", "label": "方位角 α", "value": "30", "step": "1", "unit": "度"},
        ],
        "calc": """
            const D=num('D'),a=num('a')*Math.PI/180;
            const dN=D*Math.cos(a), dE=D*Math.sin(a);
            ToolBox.setResult('result', dataGrid([
                [dN.toFixed(3),'北向增量 ΔN (米)'],
                [dE.toFixed(3),'东向增量 ΔE (米)']
            ]));
        """,
        "notes": ["极坐标到直角坐标换算。", "D=100,α=30° → ΔN≈86.6,ΔE=50。"],
    },
    {
        "slug": "reduced-level-bsfs",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "ruler",
        "bg": "from-lime-500 to-green-600",
        "title": "水准仪高差法高程计算器",
        "h1": " RL = BM + ΣBS − ΣFS",
        "h2": "由后视前视累计求待定点高程",
        "intro": "输入已知点高程 BM、后视累计 BS 与前视累计 FS，求高程。",
        "desc": "水准高差法：输入 BM、BS、FS，输出 RL。",
        "inputs": [
            {"id": "BM", "label": "已知点高程 BM", "value": "100", "step": "1", "unit": "米"},
            {"id": "BS", "label": "后视累计 BS", "value": "1.5", "step": "0.1", "unit": "米"},
            {"id": "FS", "label": "前视累计 FS", "value": "0.5", "step": "0.1", "unit": "米"},
        ],
        "calc": """
            const BM=num('BM'),BS=num('BS'),FS=num('FS');
            const RL=BM+BS-FS;
            ToolBox.setResult('result', dataGrid([
                [RL.toFixed(3),'待定点高程 RL (米)']
            ]));
        """,
        "notes": ["BS 升、FS 降。", "100+1.5−0.5 → 101.0 米。"],
    },
    {
        "slug": "horizontal-from-slope",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "minimize",
        "bg": "from-lime-500 to-green-600",
        "title": "斜距化平距计算器",
        "h1": "H = S·cos(v)",
        "h2": "由斜距与垂直角求水平距",
        "intro": "输入斜距 S 与垂直角 v（度），求水平距离。",
        "desc": "斜距化平距：输入 S、v(度)，输出 H。",
        "inputs": [
            {"id": "S", "label": "斜距 S", "value": "100", "step": "5", "unit": "米"},
            {"id": "v", "label": "垂直角 v", "value": "10", "step": "1", "unit": "度"},
        ],
        "calc": """
            const S=num('S'),v=num('v')*Math.PI/180;
            const H=S*Math.cos(v);
            ToolBox.setResult('result', dataGrid([
                [H.toFixed(3),'水平距离 H (米)']
            ]));
        """,
        "notes": ["垂直角越大平距越短。", "100·cos10° → 98.48 米。"],
    },
    {
        "slug": "grade-intersection-elev",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "trending-up",
        "bg": "from-lime-500 to-green-600",
        "title": "竖曲线高程计算器",
        "h1": "y = g₁x + (g₂−g₁)/(2L)·x²",
        "h2": "由坡度与曲线长求竖曲线上任一点高程",
        "intro": "输入前坡 g₁、后坡 g₂、曲线长 L 与距起点距离 x，求相对高程 y。",
        "desc": "竖曲线高程：输入 g1、g2、L、x，输出 y。",
        "inputs": [
            {"id": "g1", "label": "前坡 g₁", "value": "0.02", "step": "0.005", "unit": ""},
            {"id": "g2", "label": "后坡 g₂", "value": "-0.01", "step": "0.005", "unit": ""},
            {"id": "L", "label": "曲线长 L", "value": "200", "step": "10", "unit": "米"},
            {"id": "x", "label": "距起点 x", "value": "100", "step": "10", "unit": "米"},
        ],
        "calc": """
            const g1=num('g1'),g2=num('g2'),L=num('L'),x=num('x');
            const y=g1*x+(g2-g1)/(2*L)*x*x;
            ToolBox.setResult('result', dataGrid([
                [y.toFixed(4),'相对高程 y (米)']
            ]));
        """,
        "notes": ["抛物线型竖曲线常用公式。", "g1=2%,g2=−1%,L=200,x=100 → 1.25 米。"],
    },
    {
        "slug": "end-area-volume",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "box",
        "bg": "from-lime-500 to-green-600",
        "title": "平均断面法土方量计算器",
        "h1": "V = (A₁ + A₂)/2 · L",
        "h2": "由两端断面面积与间距求土方量",
        "intro": "输入两端断面面积 A₁、A₂ 与间距 L，求体积。",
        "desc": "平均断面法：输入 A1、A2、L，输出 V。",
        "inputs": [
            {"id": "A1", "label": "断面面积 A₁", "value": "10", "step": "1", "unit": "米²"},
            {"id": "A2", "label": "断面面积 A₂", "value": "20", "step": "1", "unit": "米²"},
            {"id": "L", "label": "间距 L", "value": "50", "step": "5", "unit": "米"},
        ],
        "calc": """
            const A1=num('A1'),A2=num('A2'),L=num('L');
            const V=(A1+A2)/2*L;
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(2),'土方体积 V (米³)']
            ]));
        """,
        "notes": ["相邻断面取平均乘间距。", "(10+20)/2×50 → 750 米³。"],
    },
    {
        "slug": "prismoidal-volume",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "box",
        "bg": "from-lime-500 to-green-600",
        "title": "棱台体积(辛普森)计算器",
        "h1": "V = L/6 · (A₁ + 4A_m + A₂)",
        "h2": "由两端与中截面面积求棱台体积",
        "intro": "输入两端面积 A₁、A₂、中截面 A_m 与间距 L，求体积。",
        "desc": "棱台体积：输入 A1、Am、A2、L，输出 V。",
        "inputs": [
            {"id": "A1", "label": "端面积 A₁", "value": "10", "step": "1", "unit": "米²"},
            {"id": "Am", "label": "中截面 A_m", "value": "15", "step": "1", "unit": "米²"},
            {"id": "A2", "label": "端面积 A₂", "value": "20", "step": "1", "unit": "米²"},
            {"id": "L", "label": "间距 L", "value": "50", "step": "5", "unit": "米"},
        ],
        "calc": """
            const A1=num('A1'),Am=num('Am'),A2=num('A2'),L=num('L');
            const V=L/6*(A1+4*Am+A2);
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(2),'棱台体积 V (米³)']
            ]));
        """,
        "notes": ["辛普森法，比平均断面更精确。", "50/6×(10+60+20) → 750 米³。"],
    },
    {
        "slug": "subtense-distance",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "ruler",
        "bg": "from-lime-500 to-green-600",
        "title": "视距丝(横基尺)测距计算器",
        "h1": "D = c / tan(θ)",
        "h2": "由横基尺长度与夹角求距离",
        "intro": "输入横基尺长度 c 与所对夹角 θ（度），求距离。",
        "desc": "横基尺测距：输入 c、θ(度)，输出 D。",
        "inputs": [
            {"id": "c", "label": "横基尺长 c", "value": "2", "step": "0.1", "unit": "米"},
            {"id": "th", "label": "夹角 θ", "value": "0.0573", "step": "0.001", "unit": "度"},
        ],
        "calc": """
            const c=num('c'),th=num('th')*Math.PI/180;
            const D=c/Math.tan(th);
            ToolBox.setResult('result', dataGrid([
                [D.toFixed(2),'距离 D (米)']
            ]));
        """,
        "notes": ["小角下 tanθ≈θ(弧度)。", "2/tan(0.001 rad) → 2000 米。"],
    },
    {
        "slug": "tangent-length-curve",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "arc",
        "bg": "from-lime-500 to-green-600",
        "title": "圆曲线切线长计算器",
        "h1": "T = R·tan(Δ/2)",
        "h2": "由半径与转角求切线长",
        "intro": "输入圆曲线半径 R 与转角 Δ（度），求切线长。",
        "desc": "圆曲线切线长：输入 R、Δ(度)，输出 T。",
        "inputs": [
            {"id": "R", "label": "半径 R", "value": "100", "step": "5", "unit": "米"},
            {"id": "D", "label": "转角 Δ", "value": "60", "step": "2", "unit": "度"},
        ],
        "calc": """
            const R=num('R'),D=num('D')*Math.PI/180;
            const T=R*Math.tan(D/2);
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(3),'切线长 T (米)']
            ]));
        """,
        "notes": ["切线长为曲线主点间距。", "100·tan30° → 57.74 米。"],
    },
    {
        "slug": "external-distance-curve",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "arc",
        "bg": "from-lime-500 to-green-600",
        "title": "圆曲线外距计算器",
        "h1": "E = R·(sec(Δ/2) − 1)",
        "h2": "由半径与转角求外距",
        "intro": "输入圆曲线半径 R 与转角 Δ（度），求外距。",
        "desc": "圆曲线外距：输入 R、Δ(度)，输出 E。",
        "inputs": [
            {"id": "R", "label": "半径 R", "value": "100", "step": "5", "unit": "米"},
            {"id": "D", "label": "转角 Δ", "value": "60", "step": "2", "unit": "度"},
        ],
        "calc": """
            const R=num('R'),D=num('D')*Math.PI/180;
            const E=R*(1/Math.cos(D/2)-1);
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(3),'外距 E (米)']
            ]));
        """,
        "notes": ["外距为切曲中点至交点距离。", "100×(sec30°−1) → 15.47 米。"],
    },
    {
        "slug": "middle-ordinate-curve",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "arc",
        "bg": "from-lime-500 to-green-600",
        "title": "圆曲线中点弦垂距计算器",
        "h1": "M = R·(1 − cos(Δ/2))",
        "h2": "由半径与转角求中弦垂距",
        "intro": "输入圆曲线半径 R 与转角 Δ（度），求中点垂距。",
        "desc": "圆曲线中点垂距：输入 R、Δ(度)，输出 M。",
        "inputs": [
            {"id": "R", "label": "半径 R", "value": "100", "step": "5", "unit": "米"},
            {"id": "D", "label": "转角 Δ", "value": "60", "step": "2", "unit": "度"},
        ],
        "calc": """
            const R=num('R'),D=num('D')*Math.PI/180;
            const M=R*(1-Math.cos(D/2));
            ToolBox.setResult('result', dataGrid([
                [M.toFixed(3),'中点垂距 M (米)']
            ]));
        """,
        "notes": ["用于曲线偏角法放样。", "100×(1−cos30°) → 13.40 米。"],
    },
    {
        "slug": "chord-length-curve",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "arc",
        "bg": "from-lime-500 to-green-600",
        "title": "圆曲线弦长计算器",
        "h1": "C = 2R·sin(Δ/2)",
        "h2": "由半径与转角求曲线弦长",
        "intro": "输入圆曲线半径 R 与转角 Δ（度），求弦长。",
        "desc": "圆曲线弦长：输入 R、Δ(度)，输出 C。",
        "inputs": [
            {"id": "R", "label": "半径 R", "value": "100", "step": "5", "unit": "米"},
            {"id": "D", "label": "转角 Δ", "value": "60", "step": "2", "unit": "度"},
        ],
        "calc": """
            const R=num('R'),D=num('D')*Math.PI/180;
            const C=2*R*Math.sin(D/2);
            ToolBox.setResult('result', dataGrid([
                [C.toFixed(3),'弦长 C (米)']
            ]));
        """,
        "notes": ["弦长小于弧长。", "200·sin30° → 100 米。"],
    },
    {
        "slug": "earthwork-pyramid-volume",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "mountain",
        "bg": "from-lime-500 to-green-600",
        "title": "锥体(路堤/基坑)土方计算器",
        "h1": "V = A·h / 3",
        "h2": "由底面积与高求锥体体积",
        "intro": "输入底面积 A 与高 h，求锥体体积。",
        "desc": "锥体土方：输入 A、h，输出 V。",
        "inputs": [
            {"id": "A", "label": "底面积 A", "value": "100", "step": "5", "unit": "米²"},
            {"id": "h", "label": "高 h", "value": "3", "step": "0.5", "unit": "米"},
        ],
        "calc": """
            const A=num('A'),h=num('h');
            const V=A*h/3;
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(2),'锥体体积 V (米³)']
            ]));
        """,
        "notes": ["棱锥/圆锥通用。", "100×3/3 → 100 米³。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
