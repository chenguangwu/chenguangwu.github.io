# -*- coding: utf-8 -*-
"""Batch 29: 统计学深化（14 个公式计算器）。industry=statistics。避开已有 slug。"""
from tool_template import main

TOOLS = [
    {
        "slug": "normal-cdf", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "正态分布累积概率", "h1": "正态分布 CDF 计算器",
        "h2": "Φ(z) = P(Z ≤ z)",
        "intro": "标准正态累积分布函数（erf 近似）。",
        "desc": "正态分布 CDF：输入 z 求 Φ(z)。",
        "inputs": [
            {"id": "z", "label": "标准分 z", "value": "1.96", "step": "0.1"},
        ],
        "calc": """
            function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+0.3275911*x);
                const tt=t*t, t3=tt*t, t4=tt*tt, t5=t4*t;
                const poly=0.254829592*t-0.284496736*tt+1.421413741*t3-1.453152027*t4+1.061405429*t5;
                const y=1-poly*Math.exp(-x*x);
                return s*y;}
            const z = num('z');
            const phi = 0.5 * (1 + erf(z / Math.SQRT2));
            ToolBox.setResult('result', dataGrid([
                [phi.toFixed(5), 'Φ(z) = P(Z≤z)'],
                [((1 - phi) * 100).toFixed(3), '右尾 (%)']
            ]));
        """,
        "notes": ["Φ(1.96)≈0.975。", "erf 近似精度约 1e-7。"],
    },
    {
        "slug": "z-score-calc", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "标准分 Z", "h1": "标准分 Z 值计算器",
        "h2": "z = (x − μ) / σ",
        "intro": "数据偏离均值的标准差倍数。",
        "desc": "标准分：z = (x−μ)/σ，输入数值、均值、标准差。",
        "inputs": [
            {"id": "x", "label": "数值 x", "value": "115", "step": "1"},
            {"id": "mu", "label": "均值 μ", "value": "100", "step": "1"},
            {"id": "sigma", "label": "标准差 σ", "value": "15", "step": "1"},
        ],
        "calc": """
            const x = num('x'), mu = num('mu'), sigma = num('sigma');
            ToolBox.setResult('result', dataGrid([
                [((x - mu) / sigma).toFixed(3), '标准分 z']
            ]));
        """,
        "notes": ["z = (x−μ)/σ。", "IQ 115（μ100,σ15）→ z≈1。"],
    },
    {
        "slug": "binomial-pmf", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "二项分布概率", "h1": "二项分布概率计算器",
        "h2": "P(X=k) = C(n,k)·p^k·(1−p)^(n−k)",
        "intro": "n 次独立试验恰好 k 次成功的概率。",
        "desc": "二项分布：P(X=k)=C(n,k)p^k(1−p)^(n−k)。",
        "inputs": [
            {"id": "n", "label": "试验数 n", "value": "10", "step": "1"},
            {"id": "k", "label": "成功数 k", "value": "3", "step": "1"},
            {"id": "p", "label": "成功概率 p", "value": "0.5", "step": "0.05"},
        ],
        "calc": """
            const n = Math.round(num('n')), k = Math.round(num('k')), p = num('p');
            function fact(m){let f=1;for(let i=2;i<=m;i++)f*=i;return f;}
            const C = fact(n) / (fact(k) * fact(n - k));
            const P = C * Math.pow(p, k) * Math.pow(1 - p, n - k);
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(5), 'P(X=' + k + ')'],
                [C.toFixed(0), '组合数 C(' + n + ',' + k + ')']
            ]));
        """,
        "notes": ["P(X=k)=C(n,k)p^k(1−p)^(n−k)。", "10 投 3 中、p=0.5 → 0.1172。"],
    },
    {
        "slug": "poisson-pmf", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "泊松分布概率", "h1": "泊松分布概率计算器",
        "h2": "P(X=k) = λ^k·e^(−λ) / k!",
        "intro": "单位时间/空间内发生 k 次事件的概率。",
        "desc": "泊松分布：P(X=k)=λ^k e^−λ/k!，输入均值 λ 与次数 k。",
        "inputs": [
            {"id": "lam", "label": "均值 λ", "value": "4", "step": "0.5"},
            {"id": "k", "label": "事件数 k", "value": "2", "step": "1"},
        ],
        "calc": """
            const lam = num('lam'), k = Math.round(num('k'));
            function fact(m){let f=1;for(let i=2;i<=m;i++)f*=i;return f;}
            const P = Math.pow(lam, k) * Math.exp(-lam) / fact(k);
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(5), 'P(X=' + k + ')']
            ]));
        """,
        "notes": ["P(X=k)=λ^k e^−λ/k!。", "λ=4、k=2 → 0.1465。"],
    },
    {
        "slug": "confidence-interval", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "置信区间", "h1": "均值置信区间计算器",
        "h2": "CI = x̄ ± z·σ/√n",
        "intro": "已知总体标准差时均值的置信区间。",
        "desc": "置信区间：x̄ ± z·σ/√n，输入均值、z、标准差、样本量。",
        "inputs": [
            {"id": "xbar", "label": "样本均值 x̄", "value": "100", "step": "1"},
            {"id": "z", "label": "z 值", "value": "1.96", "step": "0.05"},
            {"id": "sigma", "label": "标准差 σ", "value": "15", "step": "1"},
            {"id": "n", "label": "样本量 n", "value": "36", "step": "1"},
        ],
        "calc": """
            const xbar = num('xbar'), z = num('z'), sigma = num('sigma'), n = num('n');
            const m = z * sigma / Math.sqrt(n);
            ToolBox.setResult('result', dataGrid([
                [(xbar - m).toFixed(3), '下限'],
                [(xbar + m).toFixed(3), '上限'],
                [(2 * m).toFixed(3), '区间宽度']
            ]));
        """,
        "notes": ["CI = x̄ ± zσ/√n。", "95% 置信常用 z=1.96。"],
    },
    {
        "slug": "sample-variance", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "样本方差", "h1": "样本方差计算器",
        "h2": "s² = Σ(xᵢ − x̄)² / (n − 1)",
        "intro": "用 n−1 自由度的样本方差。",
        "desc": "样本方差：s² = Σ(xᵢ−x̄)²/(n−1)，输入逗号分隔数据。",
        "inputs": [
            {"id": "data", "label": "数据（逗号分隔）", "value": "2,4,4,4,5,5,7,9", "step": "1"},
        ],
        "calc": """
            const arr = document.getElementById('data').value.split(',').map(s => parseFloat(s.trim())).filter(v => !isNaN(v));
            const n = arr.length, mean = arr.reduce((a, b) => a + b, 0) / n;
            const ss = arr.reduce((a, b) => a + (b - mean) * (b - mean), 0);
            ToolBox.setResult('result', dataGrid([
                [mean.toFixed(4), '均值 x̄'],
                [(ss / (n - 1)).toFixed(4), '样本方差 s²'],
                [Math.sqrt(ss / (n - 1)).toFixed(4), '样本标准差 s']
            ]));
        """,
        "notes": ["s² = Σ(xᵢ−x̄)²/(n−1)。", "分母为 n−1（无偏）。"],
    },
    {
        "slug": "population-variance", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "总体方差", "h1": "总体方差计算器",
        "h2": "σ² = Σ(xᵢ − μ)² / N",
        "intro": "以总体规模 N 为分母的方差。",
        "desc": "总体方差：σ² = Σ(xᵢ−μ)²/N，输入逗号分隔数据。",
        "inputs": [
            {"id": "data", "label": "数据（逗号分隔）", "value": "2,4,4,4,5,5,7,9", "step": "1"},
        ],
        "calc": """
            const arr = document.getElementById('data').value.split(',').map(s => parseFloat(s.trim())).filter(v => !isNaN(v));
            const n = arr.length, mean = arr.reduce((a, b) => a + b, 0) / n;
            const ss = arr.reduce((a, b) => a + (b - mean) * (b - mean), 0);
            ToolBox.setResult('result', dataGrid([
                [mean.toFixed(4), '均值 μ'],
                [(ss / n).toFixed(4), '总体方差 σ²'],
                [Math.sqrt(ss / n).toFixed(4), '总体标准差 σ']
            ]));
        """,
        "notes": ["σ² = Σ(xᵢ−μ)²/N。", "分母为 N（总体）。"],
    },
    {
        "slug": "correlation-coefficient", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "皮尔逊相关系数", "h1": "皮尔逊相关系数计算器",
        "h2": "r = Σ(xᵢ−x̄)(yᵢ−ȳ) / √(Σ(xᵢ−x̄)²·Σ(yᵢ−ȳ)²)",
        "intro": "两变量线性相关强度。",
        "desc": "皮尔逊 r：输入两组逗号分隔数据。",
        "inputs": [
            {"id": "x", "label": "X 数据（逗号分隔）", "value": "1,2,3,4,5", "step": "1"},
            {"id": "y", "label": "Y 数据（逗号分隔）", "value": "2,4,5,4,5", "step": "1"},
        ],
        "calc": """
            const xa = document.getElementById('x').value.split(',').map(s=>parseFloat(s.trim()));
            const ya = document.getElementById('y').value.split(',').map(s=>parseFloat(s.trim()));
            const n = Math.min(xa.length, ya.length);
            const mx = xa.slice(0,n).reduce((a,b)=>a+b,0)/n, my = ya.slice(0,n).reduce((a,b)=>a+b,0)/n;
            let num_=0, dx=0, dy=0;
            for(let i=0;i<n;i++){num_+=(xa[i]-mx)*(ya[i]-my);dx+=Math.pow(xa[i]-mx,2);dy+=Math.pow(ya[i]-my,2);}
            const r = num_ / Math.sqrt(dx*dy);
            ToolBox.setResult('result', dataGrid([
                [r.toFixed(4), '相关系数 r'],
                [(r*r).toFixed(4), '决定系数 r²']
            ]));
        """,
        "notes": ["r∈[−1,1]。", "|r|越接近 1 线性相关越强。"],
    },
    {
        "slug": "linear-regression", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "一元线性回归", "h1": "最小二乘回归计算器",
        "h2": "y = a + b·x（最小二乘）",
        "intro": "由数据拟合最佳直线。",
        "desc": "一元线性回归：输入两组逗号分隔数据，求斜率与截距。",
        "inputs": [
            {"id": "x", "label": "X 数据（逗号分隔）", "value": "1,2,3,4,5", "step": "1"},
            {"id": "y", "label": "Y 数据（逗号分隔）", "value": "2,4,5,4,5", "step": "1"},
        ],
        "calc": """
            const xa = document.getElementById('x').value.split(',').map(s=>parseFloat(s.trim()));
            const ya = document.getElementById('y').value.split(',').map(s=>parseFloat(s.trim()));
            const n = Math.min(xa.length, ya.length);
            const mx = xa.slice(0,n).reduce((a,b)=>a+b,0)/n, my = ya.slice(0,n).reduce((a,b)=>a+b,0)/n;
            let num_=0, den=0;
            for(let i=0;i<n;i++){num_+=(xa[i]-mx)*(ya[i]-my);den+=Math.pow(xa[i]-mx,2);}
            const b = num_/den, a = my - b*mx;
            ToolBox.setResult('result', dataGrid([
                [a.toFixed(4), '截距 a'],
                [b.toFixed(4), '斜率 b'],
                [(a + b*3).toFixed(3), 'x=3 预测 y']
            ]));
        """,
        "notes": ["最小二乘：b=Σ(x−x̄)(y−ȳ)/Σ(x−x̄)²。", "a = ȳ − b x̄。"],
    },
    {
        "slug": "chi-square-test", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "卡方拟合优度", "h1": "卡方检验计算器",
        "h2": "χ² = Σ (Oᵢ − Eᵢ)² / Eᵢ",
        "intro": "观测值与期望值偏离程度。",
        "desc": "卡方统计量：χ² = Σ(O−E)²/E，输入两组逗号分隔数据。",
        "inputs": [
            {"id": "o", "label": "观测值 O（逗号分隔）", "value": "50,30,20", "step": "1"},
            {"id": "e", "label": "期望值 E（逗号分隔）", "value": "40,40,20", "step": "1"},
        ],
        "calc": """
            const oa = document.getElementById('o').value.split(',').map(s=>parseFloat(s.trim()));
            const ea = document.getElementById('e').value.split(',').map(s=>parseFloat(s.trim()));
            const n = Math.min(oa.length, ea.length);
            let chi=0;
            for(let i=0;i<n;i++) chi += Math.pow(oa[i]-ea[i], 2) / ea[i];
            ToolBox.setResult('result', dataGrid([
                [chi.toFixed(4), '卡方统计量 χ²'],
                [n - 1, '自由度 df']
            ]));
        """,
        "notes": ["χ² = Σ(O−E)²/E。", "df = 类别数 − 1。"],
    },
    {
        "slug": "geometric-mean", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "几何平均数", "h1": "几何平均数计算器",
        "h2": "G = (∏xᵢ)^(1/n)",
        "intro": "乘积的 n 次根，适合比率数据。",
        "desc": "几何平均：G = (∏xᵢ)^(1/n)，输入逗号分隔数据。",
        "inputs": [
            {"id": "data", "label": "数据（逗号分隔）", "value": "1.1,1.2,0.9,1.05", "step": "0.1"},
        ],
        "calc": """
            const arr = document.getElementById('data').value.split(',').map(s=>parseFloat(s.trim())).filter(v=>v>0);
            const n = arr.length;
            const g = Math.pow(arr.reduce((a,b)=>a*b,1), 1/n);
            ToolBox.setResult('result', dataGrid([
                [g.toFixed(5), '几何平均 G']
            ]));
        """,
        "notes": ["G = (∏xᵢ)^(1/n)。", "适合增长率平均。"],
    },
    {
        "slug": "harmonic-mean", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "调和平均数", "h1": "调和平均数计算器",
        "h2": "H = n / Σ(1/xᵢ)",
        "intro": "倒数的算术平均之倒数，适合速率。",
        "desc": "调和平均：H = n/Σ(1/xᵢ)，输入逗号分隔数据。",
        "inputs": [
            {"id": "data", "label": "数据（逗号分隔）", "value": "60,40,30", "step": "1"},
        ],
        "calc": """
            const arr = document.getElementById('data').value.split(',').map(s=>parseFloat(s.trim())).filter(v=>v>0);
            const n = arr.length;
            const H = n / arr.reduce((a,b)=>a+1/b,0);
            ToolBox.setResult('result', dataGrid([
                [H.toFixed(4), '调和平均 H']
            ]));
        """,
        "notes": ["H = n/Σ(1/xᵢ)。", "往返平均速度用调和平均。"],
    },
    {
        "slug": "percentile-rank", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "百分等级", "h1": "百分等级计算器",
        "h2": "PR = (Below + 0.5·Equal) / N × 100",
        "intro": "某值低于总体中多少比例的数据。",
        "desc": "百分等级：输入数据集与该值，求 PR。",
        "inputs": [
            {"id": "data", "label": "数据（逗号分隔）", "value": "55,60,65,70,75,80,85,90", "step": "1"},
            {"id": "val", "label": "目标值", "value": "70", "step": "1"},
        ],
        "calc": """
            const arr = document.getElementById('data').value.split(',').map(s=>parseFloat(s.trim()));
            const v = num('val'), N = arr.length;
            let below = 0, equal = 0;
            arr.forEach(x => { if (x < v) below++; else if (x === v) equal++; });
            const pr = (below + 0.5 * equal) / N * 100;
            ToolBox.setResult('result', dataGrid([
                [pr.toFixed(2), '百分等级 PR (%)']
            ]));
        """,
        "notes": ["PR = (Below+0.5·Equal)/N×100。", "描述相对位置。"],
    },
    {
        "slug": "standard-error", "industry": "statistics", "cat": "math", "icon": "📊", "bg": "#f0fdf4",
        "title": "标准误", "h1": "均值标准误计算器",
        "h2": "SE = σ / √n",
        "intro": "样本均值分布的标准差。",
        "desc": "标准误：SE = σ/√n，输入标准差与样本量。",
        "inputs": [
            {"id": "sigma", "label": "标准差 σ", "value": "15", "step": "1"},
            {"id": "n", "label": "样本量 n", "value": "36", "step": "1"},
        ],
        "calc": """
            const sigma = num('sigma'), n = num('n');
            ToolBox.setResult('result', dataGrid([
                [(sigma / Math.sqrt(n)).toFixed(4), '标准误 SE']
            ]));
        """,
        "notes": ["SE = σ/√n。", "样本越大标准误越小。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
