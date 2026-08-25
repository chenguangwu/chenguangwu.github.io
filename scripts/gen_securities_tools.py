# -*- coding: utf-8 -*-
"""Batch 37: 证券分析计算深化（14 个公式计算器）。industry=securities。"""
from tool_template import main

TOOLS = [
    {
        "slug": "ddm-price",
        "industry": "securities",
        "cat": "securities",
        "icon": "trending-up",
        "bg": "from-amber-500 to-orange-600",
        "title": "股利贴现模型 (DDM)",
        "h1": "股利贴现模型",
        "h2": "戈登增长模型估值",
        "intro": "P = D₁ / (r − g)，适用于稳定增长股票。",
        "desc": "输入预期每股股利、要求回报率与股利增长率，估算股票内在价值。",
        "inputs": [
            {"id": "d1", "label": "预期股利 D₁", "value": "4", "step": "0.5", "unit": "元"},
            {"id": "r", "label": "要求回报率 r", "value": "0.1", "step": "0.005", "unit": ""},
            {"id": "g", "label": "股利增长率 g", "value": "0.04", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const d1=num('d1'),r=num('r'),g=num('g');
            const p=d1/(r-g);
            ToolBox.setResult('result', dataGrid([
                [p.toFixed(2),'股票内在价值 (元)'],
                [(r-g).toFixed(4),'贴水率 (r-g)']
            ]));
        """,
        "notes": ["戈登模型 P = D₁ / (r − g)。", "仅适用于 r > g 且增长稳定的股票。"],
    },
    {
        "slug": "capm-return",
        "industry": "securities",
        "cat": "securities",
        "icon": "percent",
        "bg": "from-amber-500 to-orange-600",
        "title": "CAPM 期望收益",
        "h1": "CAPM 期望收益率",
        "h2": "资本资产定价模型",
        "intro": "E(r) = r_f + β·(r_m − r_f)。",
        "desc": "输入无风险利率、β 系数与市场风险溢价，计算股票期望收益率。",
        "inputs": [
            {"id": "rf", "label": "无风险利率 r_f", "value": "0.025", "step": "0.005", "unit": ""},
            {"id": "beta", "label": "β 系数", "value": "1.2", "step": "0.1", "unit": ""},
            {"id": "rm", "label": "市场收益率 r_m", "value": "0.08", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const rf=num('rf'),b=num('beta'),rm=num('rm');
            const er=rf+b*(rm-rf);
            ToolBox.setResult('result', dataGrid([
                [(er*100).toFixed(2),'期望收益率 (%)'],
                [((rm-rf)*100).toFixed(2),'市场风险溢价 (%)']
            ]));
        """,
        "notes": ["CAPM: E(r) = r_f + β(r_m − r_f)。", "β>1 波动大于市场，β<1 小于市场。"],
    },
    {
        "slug": "capm-beta",
        "industry": "securities",
        "cat": "securities",
        "icon": "grid",
        "bg": "from-amber-500 to-orange-600",
        "title": "β 系数计算",
        "h1": "β 系数",
        "h2": "协方差 / 市场方差",
        "intro": "β = Cov(r_i, r_m) / Var(r_m)。",
        "desc": "输入股票与市场的收益率样本，计算 β 系数。",
        "inputs": [
            {"id": "ri", "label": "股票收益率 (逗号分隔)", "value": "0.02,0.03,-0.01,0.04,0.01", "step": "", "unit": ""},
            {"id": "rm", "label": "市场收益率 (逗号分隔)", "value": "0.01,0.02,0.00,0.03,0.01", "step": "", "unit": ""},
        ],
        "calc": """
            const ri=document.getElementById('ri').value.split(',').map(Number);
            const rm=document.getElementById('rm').value.split(',').map(Number);
            const n=ri.length;
            const mi=ri.reduce((a,b)=>a+b,0)/n, mm=rm.reduce((a,b)=>a+b,0)/n;
            let cov=0,varM=0;
            for(let i=0;i<n;i++){cov+=(ri[i]-mi)*(rm[i]-mm);varM+=(rm[i]-mm)**2;}
            cov/=n;varM/=n;
            const b=cov/varM;
            ToolBox.setResult('result', dataGrid([
                [b.toFixed(3),'β 系数'],
                [cov.toFixed(5),'协方差'],
                [varM.toFixed(5),'市场方差']
            ]));
        """,
        "notes": ["β = 协方差 / 市场方差。", "样本需等长。"],
    },
    {
        "slug": "ytm-approx",
        "industry": "securities",
        "cat": "securities",
        "icon": "banknote",
        "bg": "from-amber-500 to-orange-600",
        "title": "债券到期收益率 (近似)",
        "h1": "YTM 近似",
        "h2": "债券收益率估算",
        "intro": "YTM ≈ [C + (F−P)/n] / [(F+P)/2]。",
        "desc": "输入票面利息、面值、现价与剩余年限，近似计算到期收益率。",
        "inputs": [
            {"id": "c", "label": "年利息 C", "value": "50", "step": "5", "unit": "元"},
            {"id": "f", "label": "面值 F", "value": "1000", "step": "100", "unit": "元"},
            {"id": "p", "label": "现价 P", "value": "950", "step": "10", "unit": "元"},
            {"id": "n", "label": "剩余年限", "value": "10", "step": "1", "unit": "年"},
        ],
        "calc": """
            const c=num('c'),f=num('f'),p=num('p'),n=num('n');
            const ytm=(c+(f-p)/n)/((f+p)/2);
            ToolBox.setResult('result', dataGrid([
                [(ytm*100).toFixed(2),'到期收益率 (%)'],
                [((c/p)*100).toFixed(2),'当前收益率 (%)']
            ]));
        """,
        "notes": ["近似公式适用于平价附近债券。", "精确 YTM 需迭代求解。"],
    },
    {
        "slug": "current-yield",
        "industry": "securities",
        "cat": "securities",
        "icon": "receipt",
        "bg": "from-amber-500 to-orange-600",
        "title": "债券当前收益率",
        "h1": "当前收益率",
        "h2": "年息 / 现价",
        "intro": "当前收益率 = 年利息 / 债券现价。",
        "desc": "输入年利息与债券现价，计算当前收益率。",
        "inputs": [
            {"id": "c", "label": "年利息", "value": "50", "step": "5", "unit": "元"},
            {"id": "p", "label": "债券现价", "value": "950", "step": "10", "unit": "元"},
        ],
        "calc": """
            const c=num('c'),p=num('p');
            ToolBox.setResult('result', dataGrid([
                [(c/p*100).toFixed(2),'当前收益率 (%)']
            ]));
        """,
        "notes": ["当前收益率忽略资本利得与期限。", "与 YTM 不同，不含价格回归面值。"],
    },
    {
        "slug": "dividend-payout",
        "industry": "securities",
        "cat": "securities",
        "icon": "pie-chart",
        "bg": "from-amber-500 to-orange-600",
        "title": "股利支付率",
        "h1": "股利支付率",
        "h2": "每股股利 / 每股收益",
        "intro": "支付率 = DPS / EPS。",
        "desc": "输入每股股利与每股收益，计算股利支付率。",
        "inputs": [
            {"id": "dps", "label": "每股股利 DPS", "value": "2", "step": "0.1", "unit": "元"},
            {"id": "eps", "label": "每股收益 EPS", "value": "5", "step": "0.1", "unit": "元"},
        ],
        "calc": """
            const d=num('dps'),e=num('eps');
            ToolBox.setResult('result', dataGrid([
                [(d/e*100).toFixed(2),'股利支付率 (%)'],
                [((1-d/e)*100).toFixed(2),'留存收益率 (%)']
            ]));
        """,
        "notes": ["支付率高代表分红慷慨，留存少。", "成长股通常支付率较低。"],
    },
    {
        "slug": "book-value-per-share",
        "industry": "securities",
        "cat": "securities",
        "icon": "book",
        "bg": "from-amber-500 to-orange-600",
        "title": "每股账面价值",
        "h1": "每股账面价值 (BVPS)",
        "h2": "(净资产 − 优先股) / 流通股",
        "intro": "BVPS = 股东权益 / 流通股数。",
        "desc": "输入净资产、优先股与流通股数，计算每股账面价值。",
        "inputs": [
            {"id": "eq", "label": "股东权益", "value": "500000000", "step": "10000000", "unit": "元"},
            {"id": "pref", "label": "优先股权益", "value": "0", "step": "1000000", "unit": "元"},
            {"id": "sh", "label": "流通股数", "value": "100000000", "step": "1000000", "unit": "股"},
        ],
        "calc": """
            const eq=num('eq'),pref=num('pref'),sh=num('sh');
            const bv=(eq-pref)/sh;
            ToolBox.setResult('result', dataGrid([
                [bv.toFixed(2),'每股账面价值 (元)']
            ]));
        """,
        "notes": ["BVPS 反映账面净资产支撑。", "与市价之比即市净率倒数。"],
    },
    {
        "slug": "price-to-book",
        "industry": "securities",
        "cat": "securities",
        "icon": "scale",
        "bg": "from-amber-500 to-orange-600",
        "title": "市净率 (P/B)",
        "h1": "市净率",
        "h2": "股价 / 每股账面价值",
        "intro": "P/B = 股价 ÷ BVPS。",
        "desc": "输入股价与每股账面价值，计算市净率。",
        "inputs": [
            {"id": "price", "label": "股价", "value": "30", "step": "1", "unit": "元"},
            {"id": "bv", "label": "每股账面价值", "value": "10", "step": "0.5", "unit": "元"},
        ],
        "calc": """
            const p=num('price'),b=num('bv');
            ToolBox.setResult('result', dataGrid([
                [(p/b).toFixed(2),'市净率 P/B'],
                [(b/p).toFixed(3),'账面市值比']
            ]));
        """,
        "notes": ["P/B<1 可能被低估（需结合资产质量）。", "重资产行业常用此指标。"],
    },
    {
        "slug": "market-cap",
        "industry": "securities",
        "cat": "securities",
        "icon": "building",
        "bg": "from-amber-500 to-orange-600",
        "title": "总市值计算",
        "h1": "总市值",
        "h2": "股价 × 总股本",
        "intro": "市值 = 股价 × 总股本。",
        "desc": "输入股价与总股本，计算公司总市值。",
        "inputs": [
            {"id": "price", "label": "股价", "value": "50", "step": "1", "unit": "元"},
            {"id": "shares", "label": "总股本", "value": "2000000000", "step": "100000000", "unit": "股"},
        ],
        "calc": """
            const p=num('price'),s=num('shares');
            ToolBox.setResult('result', dataGrid([
                [(p*s/1e8).toFixed(2),'总市值 (亿元)'],
                [(p*s).toFixed(0),'总市值 (元)']
            ]));
        """,
        "notes": ["市值随股价实时变动。", "流通市值仅计流通股。"],
    },
    {
        "slug": "market-risk-premium",
        "industry": "securities",
        "cat": "securities",
        "icon": "trending-up",
        "bg": "from-amber-500 to-orange-600",
        "title": "市场风险溢价",
        "h1": "市场风险溢价",
        "h2": "市场收益 − 无风险利率",
        "intro": "MRP = r_m − r_f。",
        "desc": "输入市场预期收益率与无风险利率，计算风险溢价。",
        "inputs": [
            {"id": "rm", "label": "市场预期收益", "value": "0.08", "step": "0.005", "unit": ""},
            {"id": "rf", "label": "无风险利率", "value": "0.025", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const rm=num('rm'),rf=num('rf');
            ToolBox.setResult('result', dataGrid([
                [((rm-rf)*100).toFixed(2),'市场风险溢价 (%)']
            ]));
        """,
        "notes": ["风险溢价是 CAPM 核心输入。", "长期历史约 4%–6%。"],
    },
    {
        "slug": "black-scholes-call",
        "industry": "securities",
        "cat": "securities",
        "icon": "phone-call",
        "bg": "from-amber-500 to-orange-600",
        "title": "布莱克-斯科尔斯看涨期权",
        "h1": "Black-Scholes 看涨",
        "h2": "欧式看涨期权定价",
        "intro": "C = S·N(d₁) − K·e^(−rT)·N(d₂)。",
        "desc": "输入标的价、行权价、无风险利率、波动率和期限，计算欧式看涨期权价格。",
        "inputs": [
            {"id": "s", "label": "标的价格 S", "value": "100", "step": "5", "unit": "元"},
            {"id": "k", "label": "行权价 K", "value": "100", "step": "5", "unit": "元"},
            {"id": "r", "label": "无风险利率 r", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "v", "label": "波动率 σ", "value": "0.2", "step": "0.01", "unit": ""},
            {"id": "t", "label": "期限 T", "value": "1", "step": "0.25", "unit": "年"},
        ],
        "calc": """
            function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+0.3275911*x);
                const y=1-(((((1.061405429*t-1.453152027)*t+1.421413741)*t-0.284496736)*t+0.254829592)*t)*Math.exp(-x*x);
                return s*y;}
            function N(x){return 0.5*(1+erf(x/Math.SQRT2));}
            const S=num('s'),K=num('k'),r=num('r'),sig=num('v'),T=num('t');
            const d1=(Math.log(S/K)+(r+sig*sig/2)*T)/(sig*Math.sqrt(T));
            const d2=d1-sig*Math.sqrt(T);
            const c=S*N(d1)-K*Math.exp(-r*T)*N(d2);
            ToolBox.setResult('result', dataGrid([
                [c.toFixed(4),'看涨期权价格 C'],
                [d1.toFixed(4),'d1'],
                [d2.toFixed(4),'d2']
            ]));
        """,
        "notes": ["欧式期权，无股息假设。", "N(x) 为标准正态分布函数。"],
    },
    {
        "slug": "black-scholes-put",
        "industry": "securities",
        "cat": "securities",
        "icon": "phone-outgoing",
        "bg": "from-amber-500 to-orange-600",
        "title": "布莱克-斯科尔斯看跌期权",
        "h1": "Black-Scholes 看跌",
        "h2": "欧式看跌期权定价",
        "intro": "P = K·e^(−rT)·N(−d₂) − S·N(−d₁)。",
        "desc": "输入标的价、行权价、无风险利率、波动率和期限，计算欧式看跌期权价格。",
        "inputs": [
            {"id": "s", "label": "标的价格 S", "value": "100", "step": "5", "unit": "元"},
            {"id": "k", "label": "行权价 K", "value": "100", "step": "5", "unit": "元"},
            {"id": "r", "label": "无风险利率 r", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "v", "label": "波动率 σ", "value": "0.2", "step": "0.01", "unit": ""},
            {"id": "t", "label": "期限 T", "value": "1", "step": "0.25", "unit": "年"},
        ],
        "calc": """
            function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+0.3275911*x);
                const y=1-(((((1.061405429*t-1.453152027)*t+1.421413741)*t-0.284496736)*t+0.254829592)*t)*Math.exp(-x*x);
                return s*y;}
            function N(x){return 0.5*(1+erf(x/Math.SQRT2));}
            const S=num('s'),K=num('k'),r=num('r'),sig=num('v'),T=num('t');
            const d1=(Math.log(S/K)+(r+sig*sig/2)*T)/(sig*Math.sqrt(T));
            const d2=d1-sig*Math.sqrt(T);
            const p=K*Math.exp(-r*T)*N(-d2)-S*N(-d1);
            ToolBox.setResult('result', dataGrid([
                [p.toFixed(4),'看跌期权价格 P'],
                [d1.toFixed(4),'d1'],
                [d2.toFixed(4),'d2']
            ]));
        """,
        "notes": ["与看涨满足看跌-看涨平价。", "无股息假设。"],
    },
    {
        "slug": "option-breakeven-call",
        "industry": "securities",
        "cat": "securities",
        "icon": "crosshair",
        "bg": "from-amber-500 to-orange-600",
        "title": "看涨期权盈亏平衡",
        "h1": "看涨期权盈亏平衡",
        "h2": "行权价 + 权利金",
        "intro": "盈亏平衡 = 行权价 + 权利金。",
        "desc": "输入行权价与权利金，计算看涨期权到期盈亏平衡股价。",
        "inputs": [
            {"id": "k", "label": "行权价 K", "value": "100", "step": "5", "unit": "元"},
            {"id": "prem", "label": "权利金", "value": "8", "step": "1", "unit": "元"},
        ],
        "calc": """
            const k=num('k'),pr=num('prem');
            ToolBox.setResult('result', dataGrid([
                [(k+pr).toFixed(2),'盈亏平衡股价 (元)']
            ]));
        """,
        "notes": ["股价高于此点买方盈利。", "卖方盈亏平衡相同但方向相反。"],
    },
    {
        "slug": "annualized-volatility",
        "industry": "securities",
        "cat": "securities",
        "icon": "activity",
        "bg": "from-amber-500 to-orange-600",
        "title": "年化波动率",
        "h1": "年化波动率",
        "h2": "日波动率 × √252",
        "intro": "年化波动率 = 日波动率 × √交易日数。",
        "desc": "输入日波动率（标准差）与年交易日数，计算年化波动率。",
        "inputs": [
            {"id": "dv", "label": "日波动率", "value": "0.015", "step": "0.001", "unit": ""},
            {"id": "d", "label": "年交易日数", "value": "252", "step": "1", "unit": "日"},
        ],
        "calc": """
            const dv=num('dv'),d=num('d');
            const av=dv*Math.sqrt(d);
            ToolBox.setResult('result', dataGrid([
                [(av*100).toFixed(2),'年化波动率 (%)'],
                [(av/Math.sqrt(d)*100).toFixed(3),'日波动率 (%)']
            ]));
        """,
        "notes": ["常用 √252 年化。", "波动率随时间聚合。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
