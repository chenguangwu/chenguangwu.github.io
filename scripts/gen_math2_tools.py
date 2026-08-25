# -*- coding: utf-8 -*-
"""Batch 66: 数学计算深化 II（14 个公式计算器）。industry=math。"""
from tool_template import main

TOOLS = [
    {
        "slug": "arithmetic-mean-math",
        "industry": "math",
        "cat": "math",
        "icon": "divide",
        "bg": "from-cyan-500 to-sky-600",
        "title": "算术平均数计算器",
        "h1": "x̄ = Σx / n",
        "h2": "由数值序列求算术平均数",
        "intro": "输入多个数值（逗号或空格分隔），求算术平均数。",
        "desc": "算术平均数：输入 数值列表，输出 x̄。",
        "inputs": [
            {"id": "xs", "label": "数值序列", "value": "1, 2, 3, 4, 5", "step": "1", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('xs').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            const mean=raw.reduce((a,b)=>a+b,0)/raw.length;
            ToolBox.setResult('result', dataGrid([
                [mean.toFixed(4),'算术平均数 x̄']
            ]));
        """,
        "notes": ["最常用的集中趋势度量。", "1,2,3,4,5 → 3。"],
    },
    {
        "slug": "geometric-series-sum",
        "industry": "math",
        "cat": "math",
        "icon": "trending-up",
        "bg": "from-cyan-500 to-sky-600",
        "title": "等比数列求和计算器",
        "h1": "S_n = a(1 − rⁿ) / (1 − r)",
        "h2": "由首项、公比与项数求等比级数和",
        "intro": "输入首项 a、公比 r 与项数 n，求前 n 项和。",
        "desc": "等比数列求和：输入 a、r、n，输出 S_n。",
        "inputs": [
            {"id": "a", "label": "首项 a", "value": "1", "step": "0.5", "unit": ""},
            {"id": "r", "label": "公比 r", "value": "0.5", "step": "0.05", "unit": ""},
            {"id": "n", "label": "项数 n", "value": "4", "step": "1", "unit": ""},
        ],
        "calc": """
            const a=num('a'),r=num('r'),n=num('n');
            const Sn=a*(1-Math.pow(r,n))/(1-r);
            ToolBox.setResult('result', dataGrid([
                [Sn.toFixed(4),'前 n 项和 S_n']
            ]));
        """,
        "notes": ["|r|<1 时数列收敛。", "1,0.5,4 → 1.875。"],
    },
    {
        "slug": "arithmetic-series-sum",
        "industry": "math",
        "cat": "math",
        "icon": "trending-up",
        "bg": "from-cyan-500 to-sky-600",
        "title": "等差数列求和计算器",
        "h1": "S_n = n(a₁ + aₙ) / 2",
        "h2": "由项数、首末项求等差级数和",
        "intro": "输入项数 n、首项 a₁ 与末项 aₙ，求前 n 项和。",
        "desc": "等差数列求和：输入 n、a1、an，输出 S_n。",
        "inputs": [
            {"id": "n", "label": "项数 n", "value": "10", "step": "1", "unit": ""},
            {"id": "a1", "label": "首项 a₁", "value": "1", "step": "0.5", "unit": ""},
            {"id": "an", "label": "末项 aₙ", "value": "10", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const n=num('n'),a1=num('a1'),an=num('an');
            const Sn=n*(a1+an)/2;
            ToolBox.setResult('result', dataGrid([
                [Sn.toFixed(2),'前 n 项和 S_n']
            ]));
        """,
        "notes": ["高斯求和公式。", "10×(1+10)/2 → 55。"],
    },
    {
        "slug": "nth-term-geometric",
        "industry": "math",
        "cat": "math",
        "icon": "hash",
        "bg": "from-cyan-500 to-sky-600",
        "title": "等比数列通项计算器",
        "h1": "aₙ = a₁·r^{(n−1)}",
        "h2": "由首项、公比与项数求通项",
        "intro": "输入首项 a₁、公比 r 与项数 n，求第 n 项。",
        "desc": "等比数列通项：输入 a1、r、n，输出 aₙ。",
        "inputs": [
            {"id": "a1", "label": "首项 a₁", "value": "2", "step": "0.5", "unit": ""},
            {"id": "r", "label": "公比 r", "value": "3", "step": "0.5", "unit": ""},
            {"id": "n", "label": "项数 n", "value": "4", "step": "1", "unit": ""},
        ],
        "calc": """
            const a1=num('a1'),r=num('r'),n=num('n');
            const an=a1*Math.pow(r,n-1);
            ToolBox.setResult('result', dataGrid([
                [an.toFixed(3),'第 n 项 aₙ']
            ]));
        """,
        "notes": ["指数增长基础公式。", "2·3³ → 54。"],
    },
    {
        "slug": "circular-permutation",
        "industry": "math",
        "cat": "math",
        "icon": "rotate-cw",
        "bg": "from-cyan-500 to-sky-600",
        "title": "圆排列数计算器",
        "h1": "P = (n − 1)!",
        "h2": "由元素个数求环形排列数",
        "intro": "输入元素个数 n，求圆排列数。",
        "desc": "圆排列数：输入 n，输出 (n−1)!。",
        "inputs": [
            {"id": "n", "label": "元素个数 n", "value": "5", "step": "1", "unit": ""},
        ],
        "calc": """
            function factN(k){let r=1;for(let i=2;i<=k;i++)r*=i;return r;}
            const n=num('n');
            const P=factN(n-1);
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(0),'圆排列数 (n−1)!']
            ]));
        """,
        "notes": ["环形排列比线性少一个自由度。", "n=5 → 4! = 24。"],
    },
    {
        "slug": "combination-repetition",
        "industry": "math",
        "cat": "math",
        "icon": "repeat",
        "bg": "from-cyan-500 to-sky-600",
        "title": "可重复组合数计算器",
        "h1": "C(n+r−1, r)",
        "h2": "由类型数与选取数求可重复组合数",
        "intro": "输入类型数 n 与选取数 r，求可重复组合数。",
        "desc": "可重复组合：输入 n、r，输出 C(n+r−1,r)。",
        "inputs": [
            {"id": "n", "label": "类型数 n", "value": "5", "step": "1", "unit": ""},
            {"id": "r", "label": "选取数 r", "value": "3", "step": "1", "unit": ""},
        ],
        "calc": """
            function factN(k){let v=1;for(let i=2;i<=k;i++)v*=i;return v;}
            const n=num('n'),r=num('r');
            const C=factN(n+r-1)/(factN(r)*factN(n-1));
            ToolBox.setResult('result', dataGrid([
                [C.toFixed(0),'可重复组合数 C']
            ]));
        """,
        "notes": ["星棒法经典计数。", "n=5,r=3 → 35。"],
    },
    {
        "slug": "multinomial-coefficient",
        "industry": "math",
        "cat": "math",
        "icon": "grid",
        "bg": "from-cyan-500 to-sky-600",
        "title": "多项式系数计算器",
        "h1": "n! / (k₁!·k₂!·k₃!)",
        "h2": "由总数与各类别数求多项式系数",
        "intro": "输入总数 n 与三个类别数 k₁、k₂、k₃（和为 n），求多项式系数。",
        "desc": "多项式系数：输入 n、k1、k2、k3，输出 系数。",
        "inputs": [
            {"id": "n", "label": "总数 n", "value": "6", "step": "1", "unit": ""},
            {"id": "k1", "label": "类别 k₁", "value": "3", "step": "1", "unit": ""},
            {"id": "k2", "label": "类别 k₂", "value": "2", "step": "1", "unit": ""},
            {"id": "k3", "label": "类别 k₃", "value": "1", "step": "1", "unit": ""},
        ],
        "calc": """
            function factN(k){let v=1;for(let i=2;i<=k;i++)v*=i;return v;}
            const n=num('n'),k1=num('k1'),k2=num('k2'),k3=num('k3');
            const C=factN(n)/(factN(k1)*factN(k2)*factN(k3));
            ToolBox.setResult('result', dataGrid([
                [C.toFixed(0),'多项式系数']
            ]));
        """,
        "notes": ["多项展开项的系数。", "6!/(3!2!1!) → 60。"],
    },
    {
        "slug": "law-of-sines",
        "industry": "math",
        "cat": "math",
        "icon": "triangle",
        "bg": "from-cyan-500 to-sky-600",
        "title": "正弦定理求边计算器",
        "h1": "a = b·sinA / sinB",
        "h2": "由已知边角与对角求未知边长",
        "intro": "输入已知边 b、其对角 B 与待求边对角 A（度），求边长 a。",
        "desc": "正弦定理：输入 b、A(度)、B(度)，输出 a。",
        "inputs": [
            {"id": "b", "label": "已知边 b", "value": "10", "step": "0.5", "unit": ""},
            {"id": "A", "label": "角 A", "value": "30", "step": "1", "unit": "度"},
            {"id": "B", "label": "角 B", "value": "45", "step": "1", "unit": "度"},
        ],
        "calc": """
            const b=num('b'),A=num('A')*Math.PI/180,B=num('B')*Math.PI/180;
            const a=b*Math.sin(A)/Math.sin(B);
            ToolBox.setResult('result', dataGrid([
                [a.toFixed(3),'边长 a']
            ]));
        """,
        "notes": ["正弦定理用于解斜三角形。", "10·sin30/sin45 → 7.071。"],
    },
    {
        "slug": "law-of-cosines",
        "industry": "math",
        "cat": "math",
        "icon": "triangle",
        "bg": "from-cyan-500 to-sky-600",
        "title": "余弦定理求边计算器",
        "h1": "c = √(a² + b² − 2ab·cosC)",
        "h2": "由两边及夹角求第三边",
        "intro": "输入两边 a、b 及其夹角 C（度），求第三边 c。",
        "desc": "余弦定理：输入 a、b、C(度)，输出 c。",
        "inputs": [
            {"id": "a", "label": "边 a", "value": "3", "step": "0.5", "unit": ""},
            {"id": "b", "label": "边 b", "value": "4", "step": "0.5", "unit": ""},
            {"id": "C", "label": "夹角 C", "value": "90", "step": "5", "unit": "度"},
        ],
        "calc": """
            const a=num('a'),b=num('b'),C=num('C')*Math.PI/180;
            const c=Math.sqrt(a*a+b*b-2*a*b*Math.cos(C));
            ToolBox.setResult('result', dataGrid([
                [c.toFixed(3),'边长 c']
            ]));
        """,
        "notes": ["C=90° 退化为勾股定理。", "3,4,90° → 5。"],
    },
    {
        "slug": "herons-area",
        "industry": "math",
        "cat": "math",
        "icon": "triangle",
        "bg": "from-cyan-500 to-sky-600",
        "title": "海伦公式面积计算器",
        "h1": "A = √[s(s−a)(s−b)(s−c)]",
        "h2": "由三边长求三角形面积",
        "intro": "输入三角形三边长 a、b、c，求面积。",
        "desc": "海伦公式：输入 a、b、c，输出 面积。",
        "inputs": [
            {"id": "a", "label": "边 a", "value": "3", "step": "0.5", "unit": ""},
            {"id": "b", "label": "边 b", "value": "4", "step": "0.5", "unit": ""},
            {"id": "c", "label": "边 c", "value": "5", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const a=num('a'),b=num('b'),c=num('c');
            const s=(a+b+c)/2;
            const A=Math.sqrt(s*(s-a)*(s-b)*(s-c));
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(3),'三角形面积 A']
            ]));
        """,
        "notes": ["仅需三边即可求面积。", "3,4,5 → 面积 6。"],
    },
    {
        "slug": "exponent-solve",
        "industry": "math",
        "cat": "math",
        "icon": "superscript",
        "bg": "from-cyan-500 to-sky-600",
        "title": "指数方程求解计算器",
        "h1": "a^x = b → x = ln b / ln a",
        "h2": "由底数与结果求指数",
        "intro": "输入底数 a 与结果 b，求指数 x。",
        "desc": "指数方程：输入 a、b，输出 x。",
        "inputs": [
            {"id": "a", "label": "底数 a", "value": "2", "step": "0.5", "unit": ""},
            {"id": "b", "label": "结果 b", "value": "8", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const a=num('a'),b=num('b');
            const x=Math.log(b)/Math.log(a);
            ToolBox.setResult('result', dataGrid([
                [x.toFixed(4),'指数 x']
            ]));
        """,
        "notes": ["以 a 为底 b 的对数。", "2^x=8 → x=3。"],
    },
    {
        "slug": "dot-product",
        "industry": "math",
        "cat": "math",
        "icon": "boxes",
        "bg": "from-cyan-500 to-sky-600",
        "title": "向量点积计算器",
        "h1": "A·B = Σ aᵢ·bᵢ",
        "h2": "由两三维向量求点积",
        "intro": "输入两向量各分量，求点积。",
        "desc": "向量点积：输入 三组分量，输出 A·B。",
        "inputs": [
            {"id": "ax", "label": "A_x", "value": "1", "step": "0.5", "unit": ""},
            {"id": "ay", "label": "A_y", "value": "2", "step": "0.5", "unit": ""},
            {"id": "az", "label": "A_z", "value": "3", "step": "0.5", "unit": ""},
            {"id": "bx", "label": "B_x", "value": "4", "step": "0.5", "unit": ""},
            {"id": "by", "label": "B_y", "value": "5", "step": "0.5", "unit": ""},
            {"id": "bz", "label": "B_z", "value": "6", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const ax=num('ax'),ay=num('ay'),az=num('az'),bx=num('bx'),by=num('by'),bz=num('bz');
            const dp=ax*bx+ay*by+az*bz;
            ToolBox.setResult('result', dataGrid([
                [dp.toFixed(2),'点积 A·B']
            ]));
        """,
        "notes": ["点积为零则两向量正交。", "(1,2,3)·(4,5,6) → 32。"],
    },
    {
        "slug": "determinant-2x2",
        "industry": "math",
        "cat": "math",
        "icon": "grid",
        "bg": "from-cyan-500 to-sky-600",
        "title": "二阶行列式计算器",
        "h1": "|A| = ad − bc",
        "h2": "由二阶矩阵四元素求行列式",
        "intro": "输入二阶矩阵元素 a、b、c、d，求行列式。",
        "desc": "二阶行列式：输入 a、b、c、d，输出 |A|。",
        "inputs": [
            {"id": "a", "label": "a", "value": "1", "step": "0.5", "unit": ""},
            {"id": "b", "label": "b", "value": "2", "step": "0.5", "unit": ""},
            {"id": "c", "label": "c", "value": "3", "step": "0.5", "unit": ""},
            {"id": "d", "label": "d", "value": "4", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const a=num('a'),b=num('b'),c=num('c'),d=num('d');
            const det=a*d-b*c;
            ToolBox.setResult('result', dataGrid([
                [det.toFixed(2),'行列式 |A|']
            ]));
        """,
        "notes": ["行列式为零则矩阵奇异。", "1·4−2·3 → −2。"],
    },
    {
        "slug": "quadratic-discriminant",
        "industry": "math",
        "cat": "math",
        "icon": "function-square",
        "bg": "from-cyan-500 to-sky-600",
        "title": "二次方程判别式计算器",
        "h1": "Δ = b² − 4ac",
        "h2": "由二次项系数求判别式",
        "intro": "输入二次项系数 a、b、c，求判别式。",
        "desc": "判别式：输入 a、b、c，输出 Δ。",
        "inputs": [
            {"id": "a", "label": "a", "value": "1", "step": "0.5", "unit": ""},
            {"id": "b", "label": "b", "value": "-3", "step": "0.5", "unit": ""},
            {"id": "c", "label": "c", "value": "2", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const a=num('a'),b=num('b'),c=num('c');
            const D=b*b-4*a*c;
            ToolBox.setResult('result', dataGrid([
                [D.toFixed(2),'判别式 Δ']
            ]));
        """,
        "notes": ["Δ>0 两实根，Δ=0 重根，Δ<0 复根。", "(−3)²−8 → 1。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
