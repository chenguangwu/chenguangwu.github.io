# -*- coding: utf-8 -*-
"""Batch 16: 几何/测量计算深化（14 个公式计算器）。industry=geometry。"""
from tool_template import main
import math

TOOLS = [
    {
        "slug": "circle-area", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "圆面积计算", "h1": "圆面积计算器",
        "h2": "圆面积（A = π·r²）",
        "intro": "由半径求圆面积。",
        "desc": "圆面积计算器：A = π·r²，输入半径得面积。",
        "inputs": [{"id": "r", "label": "半径", "value": "5", "step": "0.1", "unit": "m"}],
        "calc": """
            const r = num('r');
            const A = Math.PI * r * r;
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(4), '圆面积 A (m²)'],
                [(2 * Math.PI * r).toFixed(4), '圆周长 (m)']
            ]));
        """,
        "notes": ["A = π·r²。", "r=5 时面积约 78.54。"],
    },
    {
        "slug": "circle-circumference", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "圆周长计算", "h1": "圆周长计算器",
        "h2": "圆周长（C = 2π·r）",
        "intro": "由半径求圆周长。",
        "desc": "圆周长计算器：C = 2π·r，输入半径得周长。",
        "inputs": [{"id": "r", "label": "半径", "value": "5", "step": "0.1", "unit": "m"}],
        "calc": """
            const r = num('r');
            const C = 2 * Math.PI * r;
            ToolBox.setResult('result', dataGrid([
                [C.toFixed(4), '圆周长 C (m)'],
                [((C / Math.PI).toFixed(4)), '直径 (m)']
            ]));
        """,
        "notes": ["C = 2π·r，直径 d = 2r。", "r=5 时周长约 31.42。"],
    },
    {
        "slug": "triangle-heron", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "三角形面积(Heron)", "h1": "三角形面积计算器（海伦公式）",
        "h2": "海伦公式（A = √(s(s−a)(s−b)(s−c))）",
        "intro": "已知三边长，用半周长求三角形面积。",
        "desc": "三角形面积计算器：海伦公式 A=√[s(s−a)(s−b)(s−c)]，s=(a+b+c)/2。",
        "inputs": [
            {"id": "a", "label": "边 a", "value": "3", "step": "0.1", "unit": "m"},
            {"id": "b", "label": "边 b", "value": "4", "step": "0.1", "unit": "m"},
            {"id": "c", "label": "边 c", "value": "5", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const a = num('a'), b = num('b'), c = num('c');
            const s = (a + b + c) / 2;
            const A = Math.sqrt(s * (s - a) * (s - b) * (s - c));
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(4), '三角形面积 A (m²)'],
                [s.toFixed(4), '半周长 s (m)']
            ]));
        """,
        "notes": ["A = √[s(s−a)(s−b)(s−c)]，s = (a+b+c)/2。", "3-4-5 直角三角形面积 6。"],
    },
    {
        "slug": "pythagorean", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "勾股定理斜边", "h1": "勾股定理计算器",
        "h2": "斜边（c = √(a² + b²)）",
        "intro": "直角三角形斜边长度。",
        "desc": "勾股定理计算器：c = √(a²+b²)，输入两直角边。",
        "inputs": [
            {"id": "a", "label": "直角边 a", "value": "3", "step": "0.1", "unit": "m"},
            {"id": "b", "label": "直角边 b", "value": "4", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const a = num('a'), b = num('b');
            const c = Math.sqrt(a * a + b * b);
            const angA = Math.atan2(b, a) * 180 / Math.PI;
            ToolBox.setResult('result', dataGrid([
                [c.toFixed(4), '斜边 c (m)'],
                [angA.toFixed(2), '∠A (°)']
            ]));
        """,
        "notes": ["c = √(a² + b²)。", "3-4 对应斜边 5。"],
    },
    {
        "slug": "rectangle-diagonal", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "矩形对角线", "h1": "矩形对角线计算器",
        "h2": "对角线（d = √(w² + h²)）",
        "intro": "矩形对角线长度。",
        "desc": "矩形对角线计算器：d = √(w²+h²)，输入宽与高。",
        "inputs": [
            {"id": "w", "label": "宽", "value": "3", "step": "0.1", "unit": "m"},
            {"id": "h", "label": "高", "value": "4", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const w = num('w'), h = num('h');
            const d = Math.sqrt(w * w + h * h);
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(4), '对角线 d (m)'],
                [(w * h).toFixed(4), '矩形面积 (m²)']
            ]));
        """,
        "notes": ["d = √(w² + h²)。", "3×4 矩形对角线 5。"],
    },
    {
        "slug": "cylinder-volume", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "圆柱体积", "h1": "圆柱体积计算器",
        "h2": "圆柱体积（V = π·r²·h）",
        "intro": "由底面半径与高求圆柱体积。",
        "desc": "圆柱体积计算器：V = π·r²·h，输入半径与高。",
        "inputs": [
            {"id": "r", "label": "底面半径", "value": "2", "step": "0.1", "unit": "m"},
            {"id": "h", "label": "高", "value": "5", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const r = num('r'), h = num('h');
            const V = Math.PI * r * r * h;
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(4), '体积 V (m³)'],
                [(2 * Math.PI * r * h).toFixed(4), '侧面积 (m²)']
            ]));
        """,
        "notes": ["V = π·r²·h。", "r=2、h=5 时约 62.83 m³。"],
    },
    {
        "slug": "cone-volume", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "圆锥体积", "h1": "圆锥体积计算器",
        "h2": "圆锥体积（V = π·r²·h / 3）",
        "intro": "由底面半径与高求圆锥体积。",
        "desc": "圆锥体积计算器：V = π·r²·h/3，输入半径与高。",
        "inputs": [
            {"id": "r", "label": "底面半径", "value": "3", "step": "0.1", "unit": "m"},
            {"id": "h", "label": "高", "value": "4", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const r = num('r'), h = num('h');
            const V = Math.PI * r * r * h / 3;
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(4), '体积 V (m³)'],
                [(Math.PI * r * r).toFixed(4), '底面积 (m²)']
            ]));
        """,
        "notes": ["V = π·r²·h/3（同底等高圆柱的 1/3）。", "r=3、h=4 时约 37.70 m³。"],
    },
    {
        "slug": "trapezoid-area", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "梯形面积", "h1": "梯形面积计算器",
        "h2": "梯形面积（A = (a + b)·h / 2）",
        "intro": "由上下底与高求梯形面积。",
        "desc": "梯形面积计算器：A = (a+b)·h/2，输入两底与高。",
        "inputs": [
            {"id": "a", "label": "上底", "value": "3", "step": "0.1", "unit": "m"},
            {"id": "b", "label": "下底", "value": "5", "step": "0.1", "unit": "m"},
            {"id": "h", "label": "高", "value": "4", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const a = num('a'), b = num('b'), h = num('h');
            const A = (a + b) * h / 2;
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(4), '梯形面积 A (m²)'],
                [((a + b) * 2).toFixed(4), '中位线×2 (m)']
            ]));
        """,
        "notes": ["A = (a+b)·h/2。", "3/5 底、高 4 的梯形面积 16。"],
    },
    {
        "slug": "regular-polygon-area", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "正多边形面积", "h1": "正多边形面积计算器",
        "h2": "正多边形面积（A = n·s² / (4·tan(π/n))）",
        "intro": "由边数与边长求正多边形面积（n≥3）。",
        "desc": "正多边形面积计算器：A = n·s²/(4·tan(π/n))，输入边数与边长。",
        "inputs": [
            {"id": "n", "label": "边数 n", "value": "6", "step": "1"},
            {"id": "s", "label": "边长", "value": "1", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const n = num('n'), s = num('s');
            const A = n * s * s / (4 * Math.tan(Math.PI / n));
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(4), '正多边形面积 A (m²)'],
                [(s / (2 * Math.tan(Math.PI / n))).toFixed(4), '内切圆半径 (m)']
            ]));
        """,
        "notes": ["A = n·s² / (4·tan(π/n))。", "正六边形(s=1)面积约 2.598。"],
    },
    {
        "slug": "arc-length", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "弧长计算", "h1": "弧长计算器",
        "h2": "弧长（L = r·θ，θ 为弧度）",
        "intro": "圆弧长等于半径乘圆心角（弧度）。",
        "desc": "弧长计算器：L = r·θ，θ 以度输入自动转弧度。",
        "inputs": [
            {"id": "r", "label": "半径", "value": "10", "step": "0.1", "unit": "m"},
            {"id": "deg", "label": "圆心角", "value": "90", "step": "1", "unit": "°"},
        ],
        "calc": """
            const r = num('r'), deg = num('deg');
            const th = deg * Math.PI / 180;
            const L = r * th;
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(4), '弧长 L (m)'],
                [(th.toFixed(4)), '圆心角 (rad)']
            ]));
        """,
        "notes": ["L = r·θ（θ 弧度）；90° 弧长 = r·π/2。", "r=10、90° 时约 15.71 m。"],
    },
    {
        "slug": "sector-area", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "扇形面积", "h1": "扇形面积计算器",
        "h2": "扇形面积（A = r²·θ / 2，θ 为弧度）",
        "intro": "由半径与圆心角（弧度）求扇形面积。",
        "desc": "扇形面积计算器：A = r²·θ/2，θ 以度输入。",
        "inputs": [
            {"id": "r", "label": "半径", "value": "10", "step": "0.1", "unit": "m"},
            {"id": "deg", "label": "圆心角", "value": "90", "step": "1", "unit": "°"},
        ],
        "calc": """
            const r = num('r'), deg = num('deg');
            const th = deg * Math.PI / 180;
            const A = r * r * th / 2;
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(4), '扇形面积 A (m²)'],
                [(Math.PI * r * r * deg / 360).toFixed(4), '占整圆比 (%)×面积']
            ]));
        """,
        "notes": ["A = r²·θ/2（θ 弧度）；也等于 πr²·(θ°/360)。", "r=10、90° 时约 78.54 m²。"],
    },
    {
        "slug": "chord-length", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "弦长计算", "h1": "弦长计算器",
        "h2": "弦长（c = 2r·sin(θ/2)）",
        "intro": "由半径与圆心角（弧度）求弦长。",
        "desc": "弦长计算器：c = 2r·sin(θ/2)，θ 以度输入。",
        "inputs": [
            {"id": "r", "label": "半径", "value": "10", "step": "0.1", "unit": "m"},
            {"id": "deg", "label": "圆心角", "value": "90", "step": "1", "unit": "°"},
        ],
        "calc": """
            const r = num('r'), deg = num('deg');
            const th = deg * Math.PI / 180;
            const c = 2 * r * Math.sin(th / 2);
            ToolBox.setResult('result', dataGrid([
                [c.toFixed(4), '弦长 c (m)'],
                [(c / 2).toFixed(4), '半弦长 (m)']
            ]));
        """,
        "notes": ["c = 2r·sin(θ/2)；90°、r=10 时约 14.14 m。"],
    },
    {
        "slug": "parabola-vertex", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "抛物线顶点", "h1": "抛物线顶点计算器",
        "h2": "顶点（x_v = −b/2a，y_v = f(x_v)）",
        "intro": "二次函数 y = ax² + bx + c 的顶点坐标。",
        "desc": "抛物线顶点计算器：x_v=−b/2a，y_v=f(x_v)，输入 a、b、c。",
        "inputs": [
            {"id": "a", "label": "系数 a", "value": "1", "step": "0.1"},
            {"id": "b", "label": "系数 b", "value": "-4", "step": "0.1"},
            {"id": "c", "label": "系数 c", "value": "3", "step": "0.1"},
        ],
        "calc": """
            const a = num('a'), b = num('b'), c = num('c');
            const xv = -b / (2 * a);
            const yv = a * xv * xv + b * xv + c;
            ToolBox.setResult('result', dataGrid([
                [xv.toFixed(4), '顶点 x_v'],
                [yv.toFixed(4), '顶点 y_v']
            ]));
        """,
        "notes": ["顶点 x_v = −b/(2a)，y_v = a·x_v²+b·x_v+c。", "y=x²−4x+3 顶点 (2, −1)。"],
    },
    {
        "slug": "point-line-distance", "industry": "geometry", "cat": "geometry", "icon": "📐", "bg": "#f5f3ff",
        "title": "点到直线距离", "h1": "点到直线距离计算器",
        "h2": "距离（d = |Ax₀+By₀+C| / √(A²+B²)）",
        "intro": "点 (x₀,y₀) 到直线 Ax+By+C=0 的最短距离。",
        "desc": "点到直线距离计算器：d=|Ax₀+By₀+C|/√(A²+B²)，输入系数与点坐标。",
        "inputs": [
            {"id": "A", "label": "A", "value": "1", "step": "0.1"},
            {"id": "B", "label": "B", "value": "1", "step": "0.1"},
            {"id": "C", "label": "C", "value": "-1", "step": "0.1"},
            {"id": "x0", "label": "点 x₀", "value": "0", "step": "0.1"},
            {"id": "y0", "label": "点 y₀", "value": "0", "step": "0.1"},
        ],
        "calc": """
            const A = num('A'), B = num('B'), C = num('C'), x0 = num('x0'), y0 = num('y0');
            const d = Math.abs(A * x0 + B * y0 + C) / Math.sqrt(A * A + B * B);
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(4), '距离 d (m)'],
                [(Math.sqrt(A*A+B*B)).toFixed(4), '法向量模 √A²+B²']
            ]));
        """,
        "notes": ["d = |Ax₀+By₀+C| / √(A²+B²)。", "原点到 x+y−1=0 距离为 0.7071。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
