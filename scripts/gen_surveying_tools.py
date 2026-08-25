# -*- coding: utf-8 -*-
"""Batch 38: 测绘计算深化（14 个公式计算器）。industry=surveying。"""
from tool_template import main

TOOLS = [
    {
        "slug": "coordinate-distance-3d",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "move",
        "bg": "from-emerald-500 to-teal-600",
        "title": "三维坐标距离",
        "h1": "三维坐标距离",
        "h2": "两点空间距离",
        "intro": "d = √[(Δx)²+(Δy)²+(Δz)²]。",
        "desc": "输入两点的三维坐标，计算空间直线距离。",
        "inputs": [
            {"id": "x1", "label": "点1 X", "value": "0", "step": "1", "unit": "m"},
            {"id": "y1", "label": "点1 Y", "value": "0", "step": "1", "unit": "m"},
            {"id": "z1", "label": "点1 Z", "value": "0", "step": "1", "unit": "m"},
            {"id": "x2", "label": "点2 X", "value": "100", "step": "1", "unit": "m"},
            {"id": "y2", "label": "点2 Y", "value": "100", "step": "1", "unit": "m"},
            {"id": "z2", "label": "点2 Z", "value": "50", "step": "1", "unit": "m"},
        ],
        "calc": """
            const x1=num('x1'),y1=num('y1'),z1=num('z1'),x2=num('x2'),y2=num('y2'),z2=num('z2');
            const d=Math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2);
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(3),'空间距离 (m)']
            ]));
        """,
        "notes": ["三维欧氏距离。", "坐标需同一基准。"],
    },
    {
        "slug": "horizontal-distance",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "ruler",
        "bg": "from-emerald-500 to-teal-600",
        "title": "斜距化平距",
        "h1": "斜距化平距",
        "h2": "测距仪斜距 → 水平距离",
        "intro": "D = L·cos(α)，α 为竖直角。",
        "desc": "输入斜距与竖直角，计算水平距离。",
        "inputs": [
            {"id": "l", "label": "斜距 L", "value": "150", "step": "1", "unit": "m"},
            {"id": "a", "label": "竖直角 α", "value": "10", "step": "0.5", "unit": "°"},
        ],
        "calc": """
            const l=num('l'),a=num('a')*Math.PI/180;
            const d=l*Math.cos(a);
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(3),'水平距离 (m)'],
                [(l*Math.sin(a)).toFixed(3),'高差 (m)']
            ]));
        """,
        "notes": ["α 为相对水平面的倾角。", "高差 = L·sin(α)。"],
    },
    {
        "slug": "slope-percent",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "trending-up",
        "bg": "from-emerald-500 to-teal-600",
        "title": "坡度百分比",
        "h1": "坡度百分比",
        "h2": "纵坡 = 高差 / 平距",
        "intro": "坡度% = (h / d) × 100。",
        "desc": "输入高差与水平距离，计算坡度百分比。",
        "inputs": [
            {"id": "h", "label": "高差 h", "value": "5", "step": "0.5", "unit": "m"},
            {"id": "d", "label": "水平距离 d", "value": "100", "step": "5", "unit": "m"},
        ],
        "calc": """
            const h=num('h'),d=num('d');
            ToolBox.setResult('result', dataGrid([
                [(h/d*100).toFixed(2),'坡度 (%)'],
                [(Math.atan(h/d)*180/Math.PI).toFixed(2),'坡度角 (°)']
            ]));
        """,
        "notes": ["坡度% = 高差/平距×100。", "坡度角 = arctan(h/d)。"],
    },
    {
        "slug": "grade-angle",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "compass",
        "bg": "from-emerald-500 to-teal-600",
        "title": "坡度角换算",
        "h1": "坡度角",
        "h2": "角度 ↔ 百分比",
        "intro": "百分比 = tan(θ)×100。",
        "desc": "输入坡度角（度），换算为坡度百分比。",
        "inputs": [
            {"id": "a", "label": "坡度角 θ", "value": "5", "step": "0.5", "unit": "°"},
        ],
        "calc": """
            const a=num('a')*Math.PI/180;
            ToolBox.setResult('result', dataGrid([
                [(Math.tan(a)*100).toFixed(2),'坡度 (%)'],
                [(1/Math.tan(a)).toFixed(3),'坡比 (1:n)']
            ]));
        """,
        "notes": ["坡比 1:n 中 n = 1/tan(θ)。", "常见道路坡度 3%–8%。"],
    },
    {
        "slug": "area-coordinates",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "hexagon",
        "bg": "from-emerald-500 to-teal-600",
        "title": "坐标法面积（鞋带公式）",
        "h1": "坐标法面积",
        "h2": "多边形闭合面积",
        "intro": "A = ½|Σ(xᵢyᵢ₊₁ − xᵢ₊₁yᵢ)|。",
        "desc": "输入顶点 X、Y 坐标（逗号分隔，首尾可不重复），计算多边形面积。",
        "inputs": [
            {"id": "xs", "label": "X 坐标 (逗号分隔)", "value": "0,100,100,0", "step": "", "unit": ""},
            {"id": "ys", "label": "Y 坐标 (逗号分隔)", "value": "0,0,100,100", "step": "", "unit": ""},
        ],
        "calc": """
            const xs=document.getElementById('xs').value.split(',').map(Number);
            const ys=document.getElementById('ys').value.split(',').map(Number);
            const n=xs.length;
            let s=0;
            for(let i=0;i<n;i++){const j=(i+1)%n;s+=xs[i]*ys[j]-xs[j]*ys[i];}
            ToolBox.setResult('result', dataGrid([
                [(Math.abs(s)/2).toFixed(2),'面积 (m²)'],
                [(Math.abs(s)/2/666.67).toFixed(4),'面积 (亩)']
            ]));
        """,
        "notes": ["鞋带公式自动闭合多边形。", "1 亩 ≈ 666.67 m²。"],
    },
    {
        "slug": "bearing-azimuth",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "navigation",
        "bg": "from-emerald-500 to-teal-600",
        "title": "坐标反算方位角",
        "h1": "坐标反算方位角",
        "h2": "由坐标增量求方位角",
        "intro": "α = atan2(ΔE, ΔN)，归算至 0–360°。",
        "desc": "输入两点的北向/东向坐标差，计算方位角与水平距离。",
        "inputs": [
            {"id": "dn", "label": "北向差 ΔN", "value": "100", "step": "1", "unit": "m"},
            {"id": "de", "label": "东向差 ΔE", "value": "100", "step": "1", "unit": "m"},
        ],
        "calc": """
            const dn=num('dn'),de=num('de');
            let az=Math.atan2(de,dn)*180/Math.PI;
            if(az<0)az+=360;
            const d=Math.sqrt(dn*dn+de*de);
            ToolBox.setResult('result', dataGrid([
                [az.toFixed(2),'方位角 (°)'],
                [d.toFixed(3),'水平距离 (m)']
            ]));
        """,
        "notes": ["方位角自正北顺时针。", "坐标差需同基准。"],
    },
    {
        "slug": "elevation-diff",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "arrow-up-down",
        "bg": "from-emerald-500 to-teal-600",
        "title": "水准高差累积",
        "h1": "水准高差累积",
        "h2": "闭合水准路线",
        "intro": "Σh = Σ(后视 − 前视)。",
        "desc": "输入后视与前视读数（逗号分隔，成对），计算总高差。",
        "inputs": [
            {"id": "bs", "label": "后视读数 (逗号分隔)", "value": "1.5,1.2,1.0", "step": "", "unit": "m"},
            {"id": "fs", "label": "前视读数 (逗号分隔)", "value": "1.3,1.4,0.9", "step": "", "unit": "m"},
        ],
        "calc": """
            const bs=document.getElementById('bs').value.split(',').map(Number);
            const fs=document.getElementById('fs').value.split(',').map(Number);
            let h=0;
            for(let i=0;i<bs.length;i++){h+=bs[i]-(fs[i]||0);}
            ToolBox.setResult('result', dataGrid([
                [h.toFixed(3),'总高差 (m)'],
                [(h/bs.length).toFixed(4),'平均站差 (m)']
            ]));
        """,
        "notes": ["高差 = 后视 − 前视，逐站累加。", "闭合差应限差内。"],
    },
    {
        "slug": "stadia-distance",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "crosshair",
        "bg": "from-emerald-500 to-teal-600",
        "title": "视距测量距离",
        "h1": "视距测量距离",
        "h2": "视距丝间隔法",
        "intro": "D = k·s·cos²θ（k=100）。",
        "desc": "输入视距间隔 s 与竖直角 θ，计算水平视距。",
        "inputs": [
            {"id": "s", "label": "视距间隔 s", "value": "1.2", "step": "0.1", "unit": "m"},
            {"id": "a", "label": "竖直角 θ", "value": "5", "step": "0.5", "unit": "°"},
        ],
        "calc": """
            const s=num('s'),a=num('a')*Math.PI/180;
            const D=100*s*Math.cos(a)*Math.cos(a);
            ToolBox.setResult('result', dataGrid([
                [D.toFixed(3),'水平视距 (m)'],
                [(100*s*Math.sin(a)*Math.cos(a)).toFixed(3),'高差 (m)']
            ]));
        """,
        "notes": ["视距常数 k=100。", "高差 = ½k·s·sin(2θ)。"],
    },
    {
        "slug": "vertical-curve-elev",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "activity",
        "bg": "from-emerald-500 to-teal-600",
        "title": "竖曲线高程",
        "h1": "竖曲线高程",
        "h2": "抛物线形竖曲线",
        "intro": "y = y₀ + g₁x + (g₂−g₁)x²/(2L)。",
        "desc": "输入变坡点高程、两坡比、曲线长与桩距，计算竖曲线上高程。",
        "inputs": [
            {"id": "y0", "label": "变坡点高程", "value": "100", "step": "1", "unit": "m"},
            {"id": "g1", "label": "前坡比 g₁ (%)", "value": "3", "step": "0.5", "unit": "%"},
            {"id": "g2", "label": "后坡比 g₂ (%)", "value": "-2", "step": "0.5", "unit": "%"},
            {"id": "L", "label": "曲线长 L", "value": "60", "step": "5", "unit": "m"},
            {"id": "x", "label": "桩距 x", "value": "20", "step": "5", "unit": "m"},
        ],
        "calc": """
            const y0=num('y0'),g1=num('g1')/100,g2=num('g2')/100,L=num('L'),x=num('x');
            const y=y0+g1*x+(g2-g1)*x*x/(2*L);
            ToolBox.setResult('result', dataGrid([
                [y.toFixed(3),'该桩高程 (m)'],
                [(y-y0).toFixed(3),'相对变坡点高差 (m)']
            ]));
        """,
        "notes": ["x 自变坡点起算。", "凹/凸曲线由 g₁、g₂ 符号决定。"],
    },
    {
        "slug": "circular-curve",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "circle",
        "bg": "from-emerald-500 to-teal-600",
        "title": "圆曲线要素",
        "h1": "圆曲线要素",
        "h2": "T / L / E / M",
        "intro": "T=R·tan(Δ/2)，L=R·Δ，E=R(sec Δ/2 −1)，M=R(1−cos Δ/2)。",
        "desc": "输入半径与转角，计算切线长、曲线长、外距、中点弦距。",
        "inputs": [
            {"id": "R", "label": "半径 R", "value": "200", "step": "10", "unit": "m"},
            {"id": "d", "label": "转角 Δ", "value": "60", "step": "1", "unit": "°"},
        ],
        "calc": """
            const R=num('R'),d=num('d')*Math.PI/180,h=d/2;
            const T=R*Math.tan(h),L=R*d,E=R*(1/Math.cos(h)-1),M=R*(1-Math.cos(h));
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(3),'切线长 T (m)'],
                [L.toFixed(3),'曲线长 L (m)'],
                [E.toFixed(3),'外距 E (m)'],
                [M.toFixed(3),'中点弦距 M (m)']
            ]));
        """,
        "notes": ["Δ 为路线转角（圆心角）。", "单位统一为米。"],
    },
    {
        "slug": "triangulation-side",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "triangle",
        "bg": "from-emerald-500 to-teal-600",
        "title": "三角测量边长",
        "h1": "三角测量边长",
        "h2": "正弦定理",
        "intro": "a / sin A = b / sin B。",
        "desc": "输入已知边长及其对角、待求边对角，计算待求边长。",
        "inputs": [
            {"id": "a", "label": "已知边 a", "value": "100", "step": "5", "unit": "m"},
            {"id": "A", "label": "已知边对角 A", "value": "45", "step": "1", "unit": "°"},
            {"id": "B", "label": "待求边对角 B", "value": "60", "step": "1", "unit": "°"},
        ],
        "calc": """
            const a=num('a'),A=num('A')*Math.PI/180,B=num('B')*Math.PI/180;
            const b=a*Math.sin(B)/Math.sin(A);
            ToolBox.setResult('result', dataGrid([
                [b.toFixed(3),'待求边长 b (m)']
            ]));
        """,
        "notes": ["正弦定理适用于三角形。", "角度需为对边对角。"],
    },
    {
        "slug": "cut-fill-volume",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "layers",
        "bg": "from-emerald-500 to-teal-600",
        "title": "平均断面法土方",
        "h1": "平均断面法土方",
        "h2": "相邻断面体积",
        "intro": "V = (A₁ + A₂) / 2 × L。",
        "desc": "输入相邻两断面面积与间距，估算土石方量。",
        "inputs": [
            {"id": "a1", "label": "断面1面积", "value": "120", "step": "10", "unit": "m²"},
            {"id": "a2", "label": "断面2面积", "value": "180", "step": "10", "unit": "m²"},
            {"id": "l", "label": "间距 L", "value": "20", "step": "2", "unit": "m"},
        ],
        "calc": """
            const a1=num('a1'),a2=num('a2'),l=num('l');
            const v=(a1+a2)/2*l;
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(2),'体积 (m³)'],
                [(v/1000).toFixed(3),'体积 (千m³)']
            ]));
        """,
        "notes": ["平均断面法为近似。", "断面面积需同基准面。"],
    },
    {
        "slug": "map-scale",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "maximize",
        "bg": "from-emerald-500 to-teal-600",
        "title": "比例尺换算",
        "h1": "比例尺换算",
        "h2": "图上 ↔ 实地",
        "intro": "实地距 = 图上距 × 分母。",
        "desc": "输入图上距离与比例尺分母（如图 1:1000 输 1000），换算实地距离（米）。",
        "inputs": [
            {"id": "d", "label": "图上距离", "value": "5", "step": "0.5", "unit": "cm"},
            {"id": "m", "label": "比例尺分母", "value": "1000", "step": "100", "unit": ""},
        ],
        "calc": """
            const d=num('d'),m=num('m');
            const ground=d*m/100;
            ToolBox.setResult('result', dataGrid([
                [ground.toFixed(2),'实地距离 (m)'],
                [ground/1000, '实地距离 (km)']
            ]));
        """,
        "notes": ["图上 cm × 分母 ÷ 100 = 米。", "注意单位换算。"],
    },
    {
        "slug": "coordinate-rotation",
        "industry": "surveying",
        "cat": "surveying",
        "icon": "rotate-cw",
        "bg": "from-emerald-500 to-teal-600",
        "title": "坐标旋转",
        "h1": "坐标旋转",
        "h2": "平面点绕原点旋转",
        "intro": "x' = x·cosθ − y·sinθ，y' = x·sinθ + y·cosθ。",
        "desc": "输入点坐标与旋转角，计算旋转后坐标。",
        "inputs": [
            {"id": "x", "label": "点 X", "value": "10", "step": "1", "unit": "m"},
            {"id": "y", "label": "点 Y", "value": "0", "step": "1", "unit": "m"},
            {"id": "t", "label": "旋转角 θ", "value": "30", "step": "1", "unit": "°"},
        ],
        "calc": """
            const x=num('x'),y=num('y'),t=num('t')*Math.PI/180;
            const xp=x*Math.cos(t)-y*Math.sin(t);
            const yp=x*Math.sin(t)+y*Math.cos(t);
            ToolBox.setResult('result', dataGrid([
                [xp.toFixed(3),'旋转后 X (m)'],
                [yp.toFixed(3),'旋转后 Y (m)']
            ]));
        """,
        "notes": ["逆时针为正。", "常用于坐标转换。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
