# -*- coding: utf-8 -*-
"""Batch 46: 几何计算深化 II（14 个公式计算器）。industry=geometry。"""
from tool_template import main

TOOLS = [
    {
        "slug": "sphere-volume",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "circle",
        "bg": "from-indigo-500 to-purple-600",
        "title": "球体积计算器",
        "h1": "V = 4/3 · π · r³",
        "h2": "由半径求球的体积",
        "intro": "输入球半径，求体积。", "desc": "球体积计算器：输入半径 r，输出体积 V。",
        "inputs": [{"id": "r", "label": "半径 r", "value": "3", "step": "0.1", "unit": "m"}],
        "calc": """
            const r=num('r');
            ToolBox.setResult('result', dataGrid([
                [(4/3*Math.PI*r*r*r).toFixed(3),'球体体积 V (m³)']
            ]));
        """,
        "notes": ["V = 4πr³/3。", "r=3 → V≈113.1 m³。"],
    },
    {
        "slug": "sphere-surface-area",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "circle",
        "bg": "from-indigo-500 to-purple-600",
        "title": "球表面积计算器",
        "h1": "A = 4 · π · r²",
        "h2": "由半径求球的表面积",
        "intro": "输入球半径，求表面积。", "desc": "球表面积计算器：输入半径 r，输出表面积 A。",
        "inputs": [{"id": "r", "label": "半径 r", "value": "3", "step": "0.1", "unit": "m"}],
        "calc": """
            const r=num('r');
            ToolBox.setResult('result', dataGrid([
                [(4*Math.PI*r*r).toFixed(3),'表面积 A (m²)']
            ]));
        """,
        "notes": ["A = 4πr²。", "r=3 → A≈113.1 m²。"],
    },
    {
        "slug": "ellipsoid-volume",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "oval",
        "bg": "from-indigo-500 to-purple-600",
        "title": "椭球体积计算器",
        "h1": "V = 4/3 · π · a · b · c",
        "h2": "由三半轴求椭球体积",
        "intro": "输入三个半轴 a、b、c，求椭球体积。", "desc": "椭球体积计算器：输入 a、b、c，输出 V。",
        "inputs": [
            {"id": "a", "label": "半轴 a", "value": "3", "step": "0.1", "unit": "m"},
            {"id": "b", "label": "半轴 b", "value": "2", "step": "0.1", "unit": "m"},
            {"id": "c", "label": "半轴 c", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const a=num('a'),b=num('b'),c=num('c');
            ToolBox.setResult('result', dataGrid([
                [(4/3*Math.PI*a*b*c).toFixed(3),'椭球体积 V (m³)']
            ]));
        """,
        "notes": ["V = 4πabc/3。", "a=3,b=2,c=1 → V≈25.1 m³。"],
    },
    {
        "slug": "torus-volume",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "donut",
        "bg": "from-indigo-500 to-purple-600",
        "title": "环体（轮胎）体积计算器",
        "h1": "V = 2 · π² · R · r²",
        "h2": "由主半径与管半径求环体体积",
        "intro": "输入主半径 R（到管中心）与管半径 r，求环体体积。", "desc": "环体体积计算器：输入 R、r，输出 V。",
        "inputs": [
            {"id": "R", "label": "主半径 R", "value": "5", "step": "0.1", "unit": "m"},
            {"id": "r", "label": "管半径 r", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const R=num('R'),r=num('r');
            ToolBox.setResult('result', dataGrid([
                [(2*Math.PI*Math.PI*R*r*r).toFixed(3),'环体体积 V (m³)']
            ]));
        """,
        "notes": ["V = 2π²Rr²。", "R=5,r=1 → V≈98.7 m³。"],
    },
    {
        "slug": "cone-frustum-volume",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "triangle",
        "bg": "from-indigo-500 to-purple-600",
        "title": "圆台体积计算器",
        "h1": "V = πh/3 · (R² + Rr + r²)",
        "h2": "由上下底半径与高求圆台体积",
        "intro": "输入上半径 r、下半径 R 与高 h，求圆台体积。", "desc": "圆台体积计算器：输入 R、r、h，输出 V。",
        "inputs": [
            {"id": "R", "label": "下底半径 R", "value": "3", "step": "0.1", "unit": "m"},
            {"id": "r", "label": "上底半径 r", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "h", "label": "高 h", "value": "4", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const R=num('R'),r=num('r'),h=num('h');
            const V=Math.PI*h/3*(R*R+R*r+r*r);
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(3),'圆台体积 V (m³)']
            ]));
        """,
        "notes": ["V = πh(R²+Rr+r²)/3。", "R=3,r=1,h=4 → V≈43.98 m³。"],
    },
    {
        "slug": "cube-properties",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "box",
        "bg": "from-indigo-500 to-purple-600",
        "title": "立方体属性计算器",
        "h1": "V = a³，A = 6a²，d = a√3",
        "h2": "由边长求体积、表面积、体对角线",
        "intro": "输入立方体边长 a，求体积、表面积与体对角线。", "desc": "立方体属性计算器：输入 a，输出 V/A/d。",
        "inputs": [{"id": "a", "label": "边长 a", "value": "2", "step": "0.1", "unit": "m"}],
        "calc": """
            const a=num('a');
            ToolBox.setResult('result', dataGrid([
                [(a*a*a).toFixed(3),'体积 V (m³)'],
                [(6*a*a).toFixed(3),'表面积 A (m²)'],
                [(a*Math.sqrt(3)).toFixed(3),'体对角线 d (m)']
            ]));
        """,
        "notes": ["V=a³，A=6a²，d=a√3。", "a=2 → V=8，A=24，d≈3.464。"],
    },
    {
        "slug": "rectangular-prism-volume",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "box",
        "bg": "from-indigo-500 to-purple-600",
        "title": "长方体体积计算器",
        "h1": "V = l · w · h",
        "h2": "由长、宽、高求体积",
        "intro": "输入长、宽、高，求长方体体积与表面积。", "desc": "长方体体积计算器：输入 l、w、h，输出 V 与 A。",
        "inputs": [
            {"id": "l", "label": "长 l", "value": "4", "step": "0.1", "unit": "m"},
            {"id": "w", "label": "宽 w", "value": "3", "step": "0.1", "unit": "m"},
            {"id": "h", "label": "高 h", "value": "2", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const l=num('l'),w=num('w'),h=num('h');
            ToolBox.setResult('result', dataGrid([
                [(l*w*h).toFixed(3),'体积 V (m³)'],
                [(2*(l*w+w*h+h*l)).toFixed(3),'表面积 A (m²)']
            ]));
        """,
        "notes": ["V=lwh，A=2(lw+wh+hl)。", "4×3×2 → V=24，A=52。"],
    },
    {
        "slug": "pyramid-volume",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "triangle",
        "bg": "from-indigo-500 to-purple-600",
        "title": "棱锥体积计算器",
        "h1": "V = (1/3) · 底面积 · 高",
        "h2": "由底面积与高求棱锥体积",
        "intro": "输入底面积与高，求棱锥体积。", "desc": "棱锥体积计算器：输入底面积 A、高 h，输出 V。",
        "inputs": [
            {"id": "A", "label": "底面积 A", "value": "9", "step": "0.1", "unit": "m²"},
            {"id": "h", "label": "高 h", "value": "4", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const A=num('A'),h=num('h');
            ToolBox.setResult('result', dataGrid([
                [(A*h/3).toFixed(3),'棱锥体积 V (m³)']
            ]));
        """,
        "notes": ["V = Ah/3。", "底9、高4 → V=12。"],
    },
    {
        "slug": "distance-3d",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "move-3d",
        "bg": "from-indigo-500 to-purple-600",
        "title": "三维距离计算器",
        "h1": "d = √[(x₂−x₁)²+(y₂−y₁)²+(z₂−z₁)²]",
        "h2": "由两点坐标求空间距离",
        "intro": "输入两点 (x1,y1,z1) 与 (x2,y2,z2)，求三维距离。", "desc": "三维距离计算器：输入两组坐标，输出 d。",
        "inputs": [
            {"id": "x1", "label": "P1 x", "value": "0", "step": "0.1", "unit": ""},
            {"id": "y1", "label": "P1 y", "value": "0", "step": "0.1", "unit": ""},
            {"id": "z1", "label": "P1 z", "value": "0", "step": "0.1", "unit": ""},
            {"id": "x2", "label": "P2 x", "value": "3", "step": "0.1", "unit": ""},
            {"id": "y2", "label": "P2 y", "value": "4", "step": "0.1", "unit": ""},
            {"id": "z2", "label": "P2 z", "value": "12", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const x1=num('x1'),y1=num('y1'),z1=num('z1'),x2=num('x2'),y2=num('y2'),z2=num('z2');
            const d=Math.sqrt(Math.pow(x2-x1,2)+Math.pow(y2-y1,2)+Math.pow(z2-z1,2));
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(3),'三维距离 d']
            ]));
        """,
        "notes": ["d=√[(Δx)²+(Δy)²+(Δz)²]。", "3,4,12 → d=13。"],
    },
    {
        "slug": "midpoint-2d",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "map-pin",
        "bg": "from-indigo-500 to-purple-600",
        "title": "中点坐标计算器",
        "h1": "M = ((x₁+x₂)/2, (y₁+y₂)/2)",
        "h2": "由两点求线段中点",
        "intro": "输入两点坐标，求中点坐标。", "desc": "中点坐标计算器：输入两组坐标，输出中点。",
        "inputs": [
            {"id": "x1", "label": "P1 x", "value": "1", "step": "0.1", "unit": ""},
            {"id": "y1", "label": "P1 y", "value": "2", "step": "0.1", "unit": ""},
            {"id": "x2", "label": "P2 x", "value": "5", "step": "0.1", "unit": ""},
            {"id": "y2", "label": "P2 y", "value": "8", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const x1=num('x1'),y1=num('y1'),x2=num('x2'),y2=num('y2');
            ToolBox.setResult('result', dataGrid([
                [((x1+x2)/2).toFixed(3),'中点 x_M'],
                [((y1+y2)/2).toFixed(3),'中点 y_M']
            ]));
        """,
        "notes": ["中点 = 两端坐标算术平均。", "1,2 与 5,8 → (3,5)。"],
    },
    {
        "slug": "angle-between-vectors",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "compass",
        "bg": "from-indigo-500 to-purple-600",
        "title": "向量夹角计算器",
        "h1": "θ = arccos( a·b / (|a||b|) )",
        "h2": "由两向量求夹角",
        "intro": "输入两向量的分量，求夹角。", "desc": "向量夹角计算器：输入 a、b 分量，输出 θ。",
        "inputs": [
            {"id": "ax", "label": "a_x", "value": "1", "step": "0.1", "unit": ""},
            {"id": "ay", "label": "a_y", "value": "0", "step": "0.1", "unit": ""},
            {"id": "bx", "label": "b_x", "value": "0", "step": "0.1", "unit": ""},
            {"id": "by", "label": "b_y", "value": "1", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const ax=num('ax'),ay=num('ay'),bx=num('bx'),by=num('by');
            const dot=ax*bx+ay*by, na=Math.hypot(ax,ay), nb=Math.hypot(bx,by);
            const th=Math.acos(dot/(na*nb))*180/Math.PI;
            ToolBox.setResult('result', dataGrid([
                [th.toFixed(3),'夹角 θ (°)'],
                [dot.toFixed(3),'点积 a·b']
            ]));
        """,
        "notes": ["θ=arccos(a·b/(|a||b|))。", "x 轴与 y 轴单位向量 → 90°。"],
    },
    {
        "slug": "dot-product-2d",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "crosshair",
        "bg": "from-indigo-500 to-purple-600",
        "title": "二维点积计算器",
        "h1": "a·b = a_x b_x + a_y b_y",
        "h2": "由两向量求数量积与投影",
        "intro": "输入两向量分量，求点积与 a 在 b 上的投影长度。", "desc": "二维点积计算器：输入分量，输出点积与投影。",
        "inputs": [
            {"id": "ax", "label": "a_x", "value": "3", "step": "0.1", "unit": ""},
            {"id": "ay", "label": "a_y", "value": "4", "step": "0.1", "unit": ""},
            {"id": "bx", "label": "b_x", "value": "1", "step": "0.1", "unit": ""},
            {"id": "by", "label": "b_y", "value": "0", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const ax=num('ax'),ay=num('ay'),bx=num('bx'),by=num('by');
            const dot=ax*bx+ay*by, nb=Math.hypot(bx,by);
            ToolBox.setResult('result', dataGrid([
                [dot.toFixed(3),'点积 a·b'],
                [(dot/nb).toFixed(3),'a 在 b 上投影长度']
            ]));
        """,
        "notes": ["a·b = a_xb_x + a_yb_y。", "3,4·1,0 = 3。"],
    },
    {
        "slug": "ellipse-area",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "oval",
        "bg": "from-indigo-500 to-purple-600",
        "title": "椭圆面积计算器",
        "h1": "A = π · a · b",
        "h2": "由长短半轴求椭圆面积",
        "intro": "输入长半轴 a 与短半轴 b，求椭圆面积。", "desc": "椭圆面积计算器：输入 a、b，输出 A。",
        "inputs": [
            {"id": "a", "label": "长半轴 a", "value": "5", "step": "0.1", "unit": "m"},
            {"id": "b", "label": "短半轴 b", "value": "3", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const a=num('a'),b=num('b');
            ToolBox.setResult('result', dataGrid([
                [(Math.PI*a*b).toFixed(3),'椭圆面积 A (m²)']
            ]));
        """,
        "notes": ["A = πab。", "a=5,b=3 → A≈47.12 m²。"],
    },
    {
        "slug": "polygon-interior-angle",
        "industry": "geometry",
        "cat": "geometry",
        "icon": "hexagon",
        "bg": "from-indigo-500 to-purple-600",
        "title": "正多边形内角计算器",
        "h1": "θ = (n−2)·180° / n",
        "h2": "由边数求正多边形每个内角",
        "intro": "输入边数 n，求正多边形内角。", "desc": "正多边形内角计算器：输入 n，输出内角。",
        "inputs": [{"id": "n", "label": "边数 n", "value": "6", "step": "1", "unit": ""}],
        "calc": """
            const n=num('n');
            ToolBox.setResult('result', dataGrid([
                [((n-2)*180/n).toFixed(2),'每个内角 (°)'],
                [((n-2)*180).toFixed(0),'内角和 (°)']
            ]));
        """,
        "notes": ["内角=(n−2)·180°/n。", "六边形内角 120°。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
