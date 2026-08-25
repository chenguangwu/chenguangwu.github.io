# -*- coding: utf-8 -*-
"""Batch 67: 统计计算深化 II（14 个公式计算器）。industry=statistics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "variance-list",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "bar-chart",
        "bg": "from-violet-500 to-purple-600",
        "title": "样本方差计算器",
        "h1": "s² = Σ(xᵢ − x̄)² / (n − 1)",
        "h2": "由数值序列求样本方差",
        "intro": "输入多个数值（逗号或空格分隔），求样本方差。",
        "desc": "样本方差：输入 数值列表，输出 s²。",
        "inputs": [
            {"id": "xs", "label": "数值序列", "value": "2, 4, 4, 4, 5, 5, 7, 9", "step": "1", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('xs').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            const mean=raw.reduce((a,b)=>a+b,0)/raw.length;
            let ss=0; for(const x of raw){ ss+=Math.pow(x-mean,2); }
            const v=ss/(raw.length-1);
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(4),'样本方差 s²']
            ]));
        """,
        "notes": ["样本方差分母为 n−1（无偏）。", "2,4,4,4,5,5,7,9 → 4.571。"],
    },
    {
        "slug": "stddev-list",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "bar-chart",
        "bg": "from-violet-500 to-purple-600",
        "title": "样本标准差计算器",
        "h1": "s = √[Σ(xᵢ − x̄)² / (n − 1)]",
        "h2": "由数值序列求样本标准差",
        "intro": "输入多个数值（逗号或空格分隔），求样本标准差。",
        "desc": "样本标准差：输入 数值列表，输出 s。",
        "inputs": [
            {"id": "xs", "label": "数值序列", "value": "2, 4, 4, 4, 5, 5, 7, 9", "step": "1", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('xs').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            const mean=raw.reduce((a,b)=>a+b,0)/raw.length;
            let ss=0; for(const x of raw){ ss+=Math.pow(x-mean,2); }
            const s=Math.sqrt(ss/(raw.length-1));
            ToolBox.setResult('result', dataGrid([
                [s.toFixed(4),'样本标准差 s']
            ]));
        """,
        "notes": ["标准差与原始数据同量纲。", "√4.571 → 2.138。"],
    },
    {
        "slug": "coefficient-of-variation",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "percent",
        "bg": "from-violet-500 to-purple-600",
        "title": "变异系数计算器",
        "h1": "CV = σ / μ × 100%",
        "h2": "由均值与标准差求变异系数",
        "intro": "输入均值 μ 与标准差 σ，求变异系数。",
        "desc": "变异系数：输入 μ、σ，输出 CV(%)。",
        "inputs": [
            {"id": "mu", "label": "均值 μ", "value": "5", "step": "0.5", "unit": ""},
            {"id": "sigma", "label": "标准差 σ", "value": "2", "step": "0.2", "unit": ""},
        ],
        "calc": """
            const mu=num('mu'),sigma=num('sigma');
            const CV=sigma/mu*100;
            ToolBox.setResult('result', dataGrid([
                [CV.toFixed(2),'变异系数 CV (%)']
            ]));
        """,
        "notes": ["无量纲，便于跨量纲比较离散度。", "2/5 → 40%。"],
    },
    {
        "slug": "mean-absolute-deviation",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "bar-chart",
        "bg": "from-violet-500 to-purple-600",
        "title": "平均绝对偏差计算器",
        "h1": "MAD = Σ|xᵢ − x̄| / n",
        "h2": "由数值序列求平均绝对偏差",
        "intro": "输入多个数值（逗号或空格分隔），求平均绝对偏差。",
        "desc": "平均绝对偏差：输入 数值列表，输出 MAD。",
        "inputs": [
            {"id": "xs", "label": "数值序列", "value": "2, 4, 4, 4, 5, 5, 7, 9", "step": "1", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('xs').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            const mean=raw.reduce((a,b)=>a+b,0)/raw.length;
            let s=0; for(const x of raw){ s+=Math.abs(x-mean); }
            const mad=s/raw.length;
            ToolBox.setResult('result', dataGrid([
                [mad.toFixed(4),'平均绝对偏差 MAD']
            ]));
        """,
        "notes": ["比方差对异常值更稳健。", "2,4,4,4,5,5,7,9 → 1.5。"],
    },
    {
        "slug": "range-stat",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "git-horizontal",
        "bg": "from-violet-500 to-purple-600",
        "title": "极差计算器",
        "h1": "R = max − min",
        "h2": "由数值序列求极差",
        "intro": "输入多个数值（逗号或空格分隔），求极差。",
        "desc": "极差：输入 数值列表，输出 R。",
        "inputs": [
            {"id": "xs", "label": "数值序列", "value": "2, 4, 4, 4, 5, 5, 7, 9", "step": "1", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('xs').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            const R=Math.max.apply(null,raw)-Math.min.apply(null,raw);
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(2),'极差 R']
            ]));
        """,
        "notes": ["极差最易算但易受极值影响。", "9−2 → 7。"],
    },
    {
        "slug": "skewness-sample",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "activity",
        "bg": "from-violet-500 to-purple-600",
        "title": "样本偏度计算器",
        "h1": "g₁ = [n/((n−1)(n−2))]·Σ((x−x̄)/s)³",
        "h2": "由数值序列求样本偏度",
        "intro": "输入多个数值（逗号或空格分隔），求样本偏度。",
        "desc": "样本偏度：输入 数值列表，输出 g₁。",
        "inputs": [
            {"id": "xs", "label": "数值序列", "value": "2, 4, 4, 4, 5, 5, 7, 9", "step": "1", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('xs').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            const n=raw.length;
            const mean=raw.reduce((a,b)=>a+b,0)/n;
            let ss=0; for(const x of raw){ ss+=Math.pow(x-mean,2); }
            const s=Math.sqrt(ss/(n-1));
            let cu=0; for(const x of raw){ cu+=Math.pow((x-mean)/s,3); }
            const g1=n/((n-1)*(n-2))*cu;
            ToolBox.setResult('result', dataGrid([
                [g1.toFixed(4),'样本偏度 g₁']
            ]));
        """,
        "notes": ["正偏度表示右尾更长。", "示例 → 约 0.82。"],
    },
    {
        "slug": "t-score",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "hash",
        "bg": "from-violet-500 to-purple-600",
        "title": "t 统计量计算器",
        "h1": "t = (x̄ − μ) / (s / √n)",
        "h2": "由样本均值、假设均值与标准差求 t 值",
        "intro": "输入样本均值 x̄、假设均值 μ、标准差 s 与样本量 n，求 t 统计量。",
        "desc": "t 统计量：输入 xbar、mu、s、n，输出 t。",
        "inputs": [
            {"id": "xbar", "label": "样本均值 x̄", "value": "105", "step": "1", "unit": ""},
            {"id": "mu", "label": "假设均值 μ", "value": "100", "step": "1", "unit": ""},
            {"id": "s", "label": "标准差 s", "value": "10", "step": "0.5", "unit": ""},
            {"id": "n", "label": "样本量 n", "value": "25", "step": "1", "unit": ""},
        ],
        "calc": """
            const xbar=num('xbar'),mu=num('mu'),s=num('s'),n=num('n');
            const t=(xbar-mu)/(s/Math.sqrt(n));
            ToolBox.setResult('result', dataGrid([
                [t.toFixed(3),'t 统计量']
            ]));
        """,
        "notes": ["单样本 t 检验的核心量。", "(105−100)/(10/5) → 2.5。"],
    },
    {
        "slug": "pooled-variance",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "layers",
        "bg": "from-violet-500 to-purple-600",
        "title": "合并方差计算器",
        "h1": "s_p² = [(n₁−1)s₁² + (n₂−1)s₂²] / (n₁+n₂−2)",
        "h2": "由两组样本量方差求合并方差",
        "intro": "输入两组样本量 n₁、n₂ 与方差 s₁²、s₂²，求合并方差。",
        "desc": "合并方差：输入 n1、s1、n2、s2，输出 s_p²。",
        "inputs": [
            {"id": "n1", "label": "样本量 n₁", "value": "10", "step": "1", "unit": ""},
            {"id": "s1", "label": "标准差 s₁", "value": "2", "step": "0.2", "unit": ""},
            {"id": "n2", "label": "样本量 n₂", "value": "12", "step": "1", "unit": ""},
            {"id": "s2", "label": "标准差 s₂", "value": "3", "step": "0.2", "unit": ""},
        ],
        "calc": """
            const n1=num('n1'),s1=num('s1'),n2=num('n2'),s2=num('s2');
            const sp2=((n1-1)*s1*s1+(n2-1)*s2*s2)/(n1+n2-2);
            ToolBox.setResult('result', dataGrid([
                [sp2.toFixed(3),'合并方差 s_p²']
            ]));
        """,
        "notes": ["两样本 t 检验假定等方差时使用。", "(9·4+11·9)/20 → 6.75。"],
    },
    {
        "slug": "standard-error-proportion",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "percent",
        "bg": "from-violet-500 to-purple-600",
        "title": "比例标准误计算器",
        "h1": "SE = √[p(1−p) / n]",
        "h2": "由样本比例与样本量求标准误",
        "intro": "输入样本比例 p 与样本量 n，求比例标准误。",
        "desc": "比例标准误：输入 p、n，输出 SE。",
        "inputs": [
            {"id": "p", "label": "比例 p", "value": "0.5", "step": "0.05", "unit": ""},
            {"id": "n", "label": "样本量 n", "value": "100", "step": "5", "unit": ""},
        ],
        "calc": """
            const p=num('p'),n=num('n');
            const SE=Math.sqrt(p*(1-p)/n);
            ToolBox.setResult('result', dataGrid([
                [SE.toFixed(4),'比例标准误 SE']
            ]));
        """,
        "notes": ["比例置信区间的基础。", "√(0.25/100) → 0.05。"],
    },
    {
        "slug": "margin-of-error",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "move-horizontal",
        "bg": "from-violet-500 to-purple-600",
        "title": "误差幅度计算器",
        "h1": "ME = z × SE",
        "h2": "由临界值与标准误求误差幅度",
        "intro": "输入临界值 z 与标准误 SE，求误差幅度。",
        "desc": "误差幅度：输入 z、SE，输出 ME。",
        "inputs": [
            {"id": "z", "label": "临界值 z", "value": "1.96", "step": "0.05", "unit": ""},
            {"id": "SE", "label": "标准误 SE", "value": "0.05", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const z=num('z'),SE=num('SE');
            const ME=z*SE;
            ToolBox.setResult('result', dataGrid([
                [ME.toFixed(4),'误差幅度 ME']
            ]));
        """,
        "notes": ["95% 置信常取 z=1.96。", "1.96×0.05 → 0.098。"],
    },
    {
        "slug": "odds-to-probability",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "shuffle",
        "bg": "from-violet-500 to-purple-600",
        "title": "赔率转概率计算器",
        "h1": "p = o / (1 + o)",
        "h2": "由赔率求对应概率",
        "intro": "输入赔率 o，求概率。",
        "desc": "赔率转概率：输入 赔率，输出 p。",
        "inputs": [
            {"id": "o", "label": "赔率 o", "value": "2", "step": "0.2", "unit": ""},
        ],
        "calc": """
            const o=num('o');
            const p=o/(1+o);
            ToolBox.setResult('result', dataGrid([
                [p.toFixed(4),'概率 p']
            ]));
        """,
        "notes": ["赔率 1:1 对应概率 0.5。", "o=2 → 2/3 ≈ 0.667。"],
    },
    {
        "slug": "probability-complement",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "minus",
        "bg": "from-violet-500 to-purple-600",
        "title": "对立事件概率计算器",
        "h1": "P(Aᶜ) = 1 − P(A)",
        "h2": "由事件概率求其补事件概率",
        "intro": "输入事件概率 p，求对立事件概率。",
        "desc": "对立事件：输入 p，输出 1−p。",
        "inputs": [
            {"id": "p", "label": "概率 P(A)", "value": "0.3", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const p=num('p');
            const pc=1-p;
            ToolBox.setResult('result', dataGrid([
                [pc.toFixed(4),'补事件概率 P(Aᶜ)']
            ]));
        """,
        "notes": ["所有可能事件概率之和为 1。", "1−0.3 → 0.7。"],
    },
    {
        "slug": "binomial-cdf",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "sigma",
        "bg": "from-violet-500 to-purple-600",
        "title": "二项累积分布计算器",
        "h1": "P(X ≤ x) = Σ C(n,k)pᵏ(1−p)^{n−k}",
        "h2": "由试验数、成功概率与上限求累积概率",
        "intro": "输入试验数 n、成功概率 p 与上限 x，求 P(X≤x)。",
        "desc": "二项 CDF：输入 n、p、x，输出 P(X≤x)。",
        "inputs": [
            {"id": "n", "label": "试验数 n", "value": "5", "step": "1", "unit": ""},
            {"id": "p", "label": "成功概率 p", "value": "0.5", "step": "0.05", "unit": ""},
            {"id": "x", "label": "上限 x", "value": "2", "step": "1", "unit": ""},
        ],
        "calc": """
            function factN(k){let v=1;for(let i=2;i<=k;i++)v*=i;return v;}
            const n=num('n'),p=num('p'),xx=num('x');
            let cdf=0;
            for(let k=0;k<=xx;k++){
                const comb=factN(n)/(factN(k)*factN(n-k));
                cdf+=comb*Math.pow(p,k)*Math.pow(1-p,n-k);
            }
            ToolBox.setResult('result', dataGrid([
                [cdf.toFixed(4),'累积概率 P(X≤x)']
            ]));
        """,
        "notes": ["二项分布的左尾概率。", "n=5,p=0.5,x=2 → 0.5。"],
    },
    {
        "slug": "correlation-r-squared",
        "industry": "statistics",
        "cat": "statistics",
        "icon": "square",
        "bg": "from-violet-500 to-purple-600",
        "title": "决定系数 R² 计算器",
        "h1": "R² = r²",
        "h2": "由相关系数求决定系数",
        "intro": "输入相关系数 r，求决定系数 R²。",
        "desc": "决定系数：输入 r，输出 R²。",
        "inputs": [
            {"id": "r", "label": "相关系数 r", "value": "0.8", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const r=num('r');
            const R2=r*r;
            ToolBox.setResult('result', dataGrid([
                [R2.toFixed(4),'决定系数 R²']
            ]));
        """,
        "notes": ["R² 表示被解释的变异比例。", "0.8² → 0.64。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
