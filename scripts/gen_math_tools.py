# -*- coding: utf-8 -*-
"""Batch 22: 数学计算深化（14 个公式计算器）。industry=math。避开已有 slug。"""
from tool_template import main

TOOLS = [
    {
        "slug": "quadratic-solver", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "一元二次方程求根", "h1": "一元二次方程求根计算器",
        "h2": "ax² + bx + c = 0",
        "intro": "用判别式求解一元二次方程的两个根。",
        "desc": "一元二次方程求根计算器：输入 a,b,c 求 x₁,x₂。",
        "inputs": [
            {"id": "a", "label": "系数 a", "value": "1", "step": "0.1"},
            {"id": "b", "label": "系数 b", "value": "-3", "step": "0.1"},
            {"id": "c", "label": "系数 c", "value": "2", "step": "0.1"},
        ],
        "calc": """
            const a = num('a'), b = num('b'), c = num('c');
            const d = b * b - 4 * a * c;
            if (d < 0) {
                ToolBox.setResult('result', dataGrid([['无实根（Δ<0）', '判别式 Δ']]));
            } else {
                const x1 = (-b + Math.sqrt(d)) / (2 * a);
                const x2 = (-b - Math.sqrt(d)) / (2 * a);
                ToolBox.setResult('result', dataGrid([
                    [d.toFixed(4), '判别式 Δ'],
                    [x1.toFixed(4), '根 x₁'],
                    [x2.toFixed(4), '根 x₂']
                ]));
            }
        """,
        "notes": ["Δ = b²−4ac。", "x²−3x+2=0 → 根 2、1。"],
    },
    {
        "slug": "factorial-calc", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "阶乘计算", "h1": "阶乘计算器",
        "h2": "n! = n × (n−1) × … × 1",
        "intro": "非负整数的阶乘，0! = 1。",
        "desc": "阶乘计算器：输入非负整数 n 求 n!。",
        "inputs": [
            {"id": "n", "label": "整数 n", "value": "10", "step": "1"},
        ],
        "calc": """
            let n = Math.round(num('n'));
            if (n < 0) n = 0;
            let f = 1; for (let i = 2; i <= n; i++) f *= i;
            ToolBox.setResult('result', dataGrid([
                [f.toExponential(4), n + '! (科学计数)'],
                [f.toLocaleString('en-US'), n + '!']
            ]));
        """,
        "notes": ["0! = 1。", "10! = 3,628,800。"],
    },
    {
        "slug": "gcd-lcm", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "最大公约数与最小公倍数", "h1": "GCD / LCM 计算器",
        "h2": "gcd(a,b) · lcm(a,b) = |a·b|",
        "intro": "辗转相除法求最大公约数，再求最小公倍数。",
        "desc": "GCD/LCM 计算器：输入两整数求最大公约数与最小公倍数。",
        "inputs": [
            {"id": "a", "label": "整数 a", "value": "48", "step": "1"},
            {"id": "b", "label": "整数 b", "value": "36", "step": "1"},
        ],
        "calc": """
            let a = Math.round(num('a')), b = Math.round(num('b'));
            const prod = Math.abs(a * b);
            while (b) { const t = b; b = a % b; a = t; }
            const g = Math.abs(a);
            ToolBox.setResult('result', dataGrid([
                [g, '最大公约数 gcd'],
                [prod / g, '最小公倍数 lcm']
            ]));
        """,
        "notes": ["gcd(48,36)=12。", "lcm = |ab|/gcd = 144。"],
    },
    {
        "slug": "prime-check", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "质数判定", "h1": "质数判定计算器",
        "h2": "试除法判定素数",
        "intro": "判断给定正整数是否为质数。",
        "desc": "质数判定计算器：输入正整数判断是否为质数。",
        "inputs": [
            {"id": "n", "label": "整数 n", "value": "97", "step": "1"},
        ],
        "calc": """
            let n = Math.round(num('n'));
            let prime = n >= 2;
            for (let i = 2; i * i <= n; i++) { if (n % i === 0) { prime = false; break; } }
            ToolBox.setResult('result', dataGrid([
                [prime ? '是质数' : '不是质数', n + ' 的判定']
            ]));
        """,
        "notes": ["97 是质数。", "试除法到 √n 即可。"],
    },
    {
        "slug": "fibonacci-n", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "斐波那契数列", "h1": "斐波那契第 n 项计算器",
        "h2": "F(n) = F(n−1) + F(n−2)",
        "intro": "迭代计算斐波那契数列第 n 项。",
        "desc": "斐波那契计算器：输入 n 求第 n 项。",
        "inputs": [
            {"id": "n", "label": "项数 n", "value": "20", "step": "1"},
        ],
        "calc": """
            let n = Math.round(num('n'));
            if (n < 0) n = 0;
            let a = 0, b = 1;
            for (let i = 0; i < n; i++) { const t = a + b; a = b; b = t; }
            ToolBox.setResult('result', dataGrid([
                [a.toLocaleString('en-US'), 'F(' + n + ')']
            ]));
        """,
        "notes": ["F(0)=0, F(1)=1。", "F(20) = 6765。"],
    },
    {
        "slug": "log-base", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "任意底数对数", "h1": "任意底数对数计算器",
        "h2": "log_b(x) = ln(x) / ln(b)",
        "intro": "换底公式求任意底数的对数。",
        "desc": "任意底数对数计算器：log_b(x) = ln x / ln b。",
        "inputs": [
            {"id": "x", "label": "真数 x", "value": "1000", "step": "1"},
            {"id": "b", "label": "底数 b", "value": "10", "step": "0.1"},
        ],
        "calc": """
            const x = num('x'), b = num('b');
            const r = Math.log(x) / Math.log(b);
            ToolBox.setResult('result', dataGrid([
                [r.toFixed(6), 'log_' + b + '(' + x + ')']
            ]));
        """,
        "notes": ["log_10(1000)=3。", "换底公式：ln x/ln b。"],
    },
    {
        "slug": "power-calc", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "幂运算", "h1": "幂运算计算器",
        "h2": "x^y",
        "intro": "计算底数 x 的 y 次幂。",
        "desc": "幂运算计算器：计算 x 的 y 次方。",
        "inputs": [
            {"id": "x", "label": "底数 x", "value": "2", "step": "0.1"},
            {"id": "y", "label": "指数 y", "value": "10", "step": "0.1"},
        ],
        "calc": """
            const x = num('x'), y = num('y');
            const r = Math.pow(x, y);
            ToolBox.setResult('result', dataGrid([
                [r.toExponential(4), x + '^' + y + ' (科学)'],
                [r.toLocaleString('en-US'), x + '^' + y]
            ]));
        """,
        "notes": ["2^10 = 1024。", "支持小数指数（开方即 y=0.5）。"],
    },
    {
        "slug": "root-calc", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "开方计算", "h1": "开方计算器",
        "h2": "√x 与 ∛x",
        "intro": "计算平方根与立方根。",
        "desc": "开方计算器：计算平方根与立方根。",
        "inputs": [
            {"id": "x", "label": "被开方数 x", "value": "2", "step": "0.1"},
        ],
        "calc": """
            const x = num('x');
            ToolBox.setResult('result', dataGrid([
                [Math.sqrt(x).toFixed(6), '平方根 √x'],
                [Math.cbrt(x).toFixed(6), '立方根 ∛x']
            ]));
        """,
        "notes": ["√2 ≈ 1.414214。", "∛8 = 2。"],
    },
    {
        "slug": "permutation", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "排列数", "h1": "排列数计算器",
        "h2": "P(n,r) = n! / (n−r)!",
        "intro": "从 n 个元素取 r 个的排列数。",
        "desc": "排列数计算器：P(n,r) = n!/(n−r)!。",
        "inputs": [
            {"id": "n", "label": "总数 n", "value": "10", "step": "1"},
            {"id": "r", "label": "选取 r", "value": "3", "step": "1"},
        ],
        "calc": """
            let n = Math.round(num('n')), r = Math.round(num('r'));
            if (r > n) r = n;
            let p = 1; for (let i = n - r + 1; i <= n; i++) p *= i;
            ToolBox.setResult('result', dataGrid([
                [p.toLocaleString('en-US'), 'P(' + n + ',' + r + ')']
            ]));
        """,
        "notes": ["P(10,3) = 720。", "与顺序有关。"],
    },
    {
        "slug": "combination", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "组合数", "h1": "组合数计算器",
        "h2": "C(n,r) = n! / (r!(n−r)!)",
        "intro": "从 n 个元素取 r 个的组合数。",
        "desc": "组合数计算器：C(n,r) = n!/(r!(n−r)!)。",
        "inputs": [
            {"id": "n", "label": "总数 n", "value": "10", "step": "1"},
            {"id": "r", "label": "选取 r", "value": "3", "step": "1"},
        ],
        "calc": """
            let n = Math.round(num('n')), r = Math.round(num('r'));
            if (r > n) r = n;
            let c = 1;
            for (let i = 1; i <= r; i++) c = c * (n - i + 1) / i;
            ToolBox.setResult('result', dataGrid([
                [c.toLocaleString('en-US'), 'C(' + n + ',' + r + ')']
            ]));
        """,
        "notes": ["C(10,3) = 120。", "与顺序无关。"],
    },
    {
        "slug": "modulo-calc", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "取模运算", "h1": "取模运算计算器",
        "h2": "a mod b",
        "intro": "求 a 除以 b 的余数。",
        "desc": "取模运算计算器：计算 a mod b。",
        "inputs": [
            {"id": "a", "label": "被除数 a", "value": "17", "step": "1"},
            {"id": "b", "label": "除数 b", "value": "5", "step": "1"},
        ],
        "calc": """
            const a = num('a'), b = num('b');
            ToolBox.setResult('result', dataGrid([
                [(a % b).toFixed(4), 'a mod b']
            ]));
        """,
        "notes": ["17 mod 5 = 2。", "用于周期与同余。"],
    },
    {
        "slug": "percent-change", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "百分比变化", "h1": "百分比变化计算器",
        "h2": "Δ% = (新 − 旧) / 旧 × 100%",
        "intro": "计算数值变化的百分比。",
        "desc": "百分比变化计算器：Δ% = (新−旧)/旧×100%。",
        "inputs": [
            {"id": "old", "label": "原值", "value": "80", "step": "1"},
            {"id": "new", "label": "新值", "value": "100", "step": "1"},
        ],
        "calc": """
            const old = num('old'), nw = num('new');
            const pct = (nw - old) / old * 100;
            ToolBox.setResult('result', dataGrid([
                [pct.toFixed(2), '变化百分比 (%)'],
                [(nw - old).toFixed(2), '绝对变化']
            ]));
        """,
        "notes": ["80→100 为 +25%。", "负值表示下降。"],
    },
    {
        "slug": "slope-line", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "直线斜率", "h1": "直线斜率计算器",
        "h2": "k = (y₂ − y₁) / (x₂ − x₁)",
        "intro": "由两点坐标求直线斜率。",
        "desc": "直线斜率计算器：k = (y₂−y₁)/(x₂−x₁)。",
        "inputs": [
            {"id": "x1", "label": "x₁", "value": "1", "step": "0.5"},
            {"id": "y1", "label": "y₁", "value": "2", "step": "0.5"},
            {"id": "x2", "label": "x₂", "value": "4", "step": "0.5"},
            {"id": "y2", "label": "y₂", "value": "8", "step": "0.5"},
        ],
        "calc": """
            const x1 = num('x1'), y1 = num('y1'), x2 = num('x2'), y2 = num('y2');
            const dx = x2 - x1;
            if (Math.abs(dx) < 1e-12) {
                ToolBox.setResult('result', dataGrid([['斜率不存在（竖直线）', 'k']]));
            } else {
                const k = (y2 - y1) / dx;
                ToolBox.setResult('result', dataGrid([
                    [k.toFixed(4), '斜率 k'],
                    [Math.atan(k) * 180 / Math.PI, '倾角 (°)']
                ]));
            }
        """,
        "notes": ["(1,2)→(4,8) 斜率 2。", "分母为零为竖直线。"],
    },
    {
        "slug": "distance-2d", "industry": "math", "cat": "math", "icon": "🧮", "bg": "#f0fdf4",
        "title": "两点距离", "h1": "平面两点距离计算器",
        "h2": "d = √((x₂−x₁)² + (y₂−y₁)²)",
        "intro": "计算二维平面上两点的距离。",
        "desc": "两点距离计算器：欧几里得距离。",
        "inputs": [
            {"id": "x1", "label": "x₁", "value": "0", "step": "0.5"},
            {"id": "y1", "label": "y₁", "value": "0", "step": "0.5"},
            {"id": "x2", "label": "x₂", "value": "3", "step": "0.5"},
            {"id": "y2", "label": "y₂", "value": "4", "step": "0.5"},
        ],
        "calc": """
            const x1 = num('x1'), y1 = num('y1'), x2 = num('x2'), y2 = num('y2');
            const d = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(4), '距离 d']
            ]));
        """,
        "notes": ["(0,0)→(3,4) 距离 5。", "勾股数 3-4-5。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
