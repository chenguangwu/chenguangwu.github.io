# -*- coding: utf-8 -*-
"""Batch 64: 证券分析深化 II（14 个公式计算器）。industry=securities。"""
from tool_template import main

TOOLS = [
    {
        "slug": "gordon-growth-price",
        "industry": "securities",
        "cat": "securities",
        "icon": "trending-up",
        "bg": "from-indigo-500 to-blue-600",
        "title": "戈登增长模型股价计算器",
        "h1": "P = D₁ / (r − g)",
        "h2": "由预期股利、要求收益率与增长率求股价",
        "intro": "输入预期每股股利 D₁、要求收益率 r 与股利增长率 g，求合理股价。",
        "desc": "戈登模型：输入 D1、r、g，输出 P。",
        "inputs": [
            {"id": "D1", "label": "预期股利 D₁", "value": "4", "step": "0.2", "unit": "元"},
            {"id": "r", "label": "要求收益率 r", "value": "0.1", "step": "0.005", "unit": ""},
            {"id": "g", "label": "增长率 g", "value": "0.04", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const D1=num('D1'),r=num('r'),g=num('g');
            const P=D1/(r-g);
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2),'合理股价 P (元)']
            ]));
        """,
        "notes": ["要求 r>g。", "4/(0.1−0.04) → 66.67 元。"],
    },
    {
        "slug": "earnings-yield",
        "industry": "securities",
        "cat": "securities",
        "icon": "percent",
        "bg": "from-indigo-500 to-blue-600",
        "title": "盈利收益率计算器",
        "h1": "盈利收益率 = EPS / P",
        "h2": "由每股收益与股价求盈利收益率",
        "intro": "输入每股收益 EPS 与股价 P，求盈利收益率。",
        "desc": "盈利收益率：输入 EPS、P，输出 (%)。",
        "inputs": [
            {"id": "EPS", "label": "每股收益 EPS", "value": "5", "step": "0.2", "unit": "元"},
            {"id": "P", "label": "股价 P", "value": "100", "step": "5", "unit": "元"},
        ],
        "calc": """
            const EPS=num('EPS'),P=num('P');
            const ey=EPS/P*100;
            ToolBox.setResult('result', dataGrid([
                [ey.toFixed(2),'盈利收益率 (%)']
            ]));
        """,
        "notes": ["市盈率的倒数。", "5/100 → 5%。"],
    },
    {
        "slug": "peg-ratio",
        "industry": "securities",
        "cat": "securities",
        "icon": "scale",
        "bg": "from-indigo-500 to-blue-600",
        "title": "PEG 估值指标计算器",
        "h1": "PEG = PE / (g × 100)",
        "h2": "由市盈率与盈利增长率求 PEG",
        "intro": "输入市盈率 PE 与盈利增长率 g（百分比），求 PEG。",
        "desc": "PEG：输入 PE、g(%)，输出 PEG。",
        "inputs": [
            {"id": "PE", "label": "市盈率 PE", "value": "20", "step": "1", "unit": ""},
            {"id": "g", "label": "增长率 g", "value": "10", "step": "1", "unit": "%"},
        ],
        "calc": """
            const PE=num('PE'),g=num('g');
            const PEG=PE/g;
            ToolBox.setResult('result', dataGrid([
                [PEG.toFixed(2),'PEG']
            ]));
        """,
        "notes": ["PEG<1 常被视为低估。", "20/10 → 2.0。"],
    },
    {
        "slug": "book-to-market",
        "industry": "securities",
        "cat": "securities",
        "icon": "book",
        "bg": "from-indigo-500 to-blue-600",
        "title": "账面市值比计算器",
        "h1": "B/M = BVPS / P",
        "h2": "由每股净资产与股价求账面市值比",
        "intro": "输入每股净资产 BVPS 与股价 P，求账面市值比。",
        "desc": "账面市值比：输入 BVPS、P，输出 B/M。",
        "inputs": [
            {"id": "BVPS", "label": "每股净资产 BVPS", "value": "30", "step": "1", "unit": "元"},
            {"id": "P", "label": "股价 P", "value": "100", "step": "5", "unit": "元"},
        ],
        "calc": """
            const BVPS=num('BVPS'),P=num('P');
            const BM=BVPS/P;
            ToolBox.setResult('result', dataGrid([
                [BM.toFixed(3),'账面市值比 B/M']
            ]));
        """,
        "notes": ["市净率的倒数，价值股常偏高。", "30/100 → 0.3。"],
    },
    {
        "slug": "enterprise-value",
        "industry": "securities",
        "cat": "securities",
        "icon": "building",
        "bg": "from-indigo-500 to-blue-600",
        "title": "企业价值(EV)计算器",
        "h1": "EV = 市值 + 债务 − 现金",
        "h2": "由市值、债务与现金求企业价值",
        "intro": "输入股票市值、总债务与现金及等价物，求企业价值。",
        "desc": "企业价值：输入 市值、债务、现金，输出 EV。",
        "inputs": [
            {"id": "MCap", "label": "股票市值", "value": "1000", "step": "50", "unit": "万元"},
            {"id": "Debt", "label": "总债务", "value": "200", "step": "20", "unit": "万元"},
            {"id": "Cash", "label": "现金及等价物", "value": "100", "step": "10", "unit": "万元"},
        ],
        "calc": """
            const MCap=num('MCap'),Debt=num('Debt'),Cash=num('Cash');
            const EV=MCap+Debt-Cash;
            ToolBox.setResult('result', dataGrid([
                [EV.toFixed(2),'企业价值 EV (万元)']
            ]));
        """,
        "notes": ["EV 反映整体收购成本。", "1000+200−100 → 1100 万。"],
    },
    {
        "slug": "fcf-yield",
        "industry": "securities",
        "cat": "securities",
        "icon": "droplets",
        "bg": "from-indigo-500 to-blue-600",
        "title": "自由现金流收益率计算器",
        "h1": "FCF 收益率 = FCF / 股价",
        "h2": "由每股自由现金流与股价求收益率",
        "intro": "输入每股自由现金流 FCF 与股价 P，求自由现金流收益率。",
        "desc": "自由现金流收益率：输入 FCF、P，输出 (%)。",
        "inputs": [
            {"id": "FCF", "label": "每股 FCF", "value": "8", "step": "0.5", "unit": "元"},
            {"id": "P", "label": "股价 P", "value": "100", "step": "5", "unit": "元"},
        ],
        "calc": """
            const FCF=num('FCF'),P=num('P');
            const y=FCF/P*100;
            ToolBox.setResult('result', dataGrid([
                [y.toFixed(2),'FCF 收益率 (%)']
            ]));
        """,
        "notes": ["比盈利收益率更难操纵。", "8/100 → 8%。"],
    },
    {
        "slug": "holding-return-stock",
        "industry": "securities",
        "cat": "securities",
        "icon": "repeat",
        "bg": "from-indigo-500 to-blue-600",
        "title": "股票持有期收益率计算器",
        "h1": "r = (P₁ − P₀ + D) / P₀",
        "h2": "由买卖价与股息求持有期收益率",
        "intro": "输入买入价、卖出价与期间股息，求持有期收益率。",
        "desc": "持有期收益：输入 P0、P1、D，输出 r(%)。",
        "inputs": [
            {"id": "P0", "label": "买入价 P₀", "value": "100", "step": "5", "unit": "元"},
            {"id": "P1", "label": "卖出价 P₁", "value": "110", "step": "5", "unit": "元"},
            {"id": "D", "label": "股息 D", "value": "2", "step": "0.2", "unit": "元"},
        ],
        "calc": """
            const P0=num('P0'),P1=num('P1'),D=num('D');
            const r=(P1-P0+D)/P0*100;
            ToolBox.setResult('result', dataGrid([
                [r.toFixed(2),'持有期收益率 (%)']
            ]));
        """,
        "notes": ["含股息的总回报。", "(110−100+2)/100 → 12%。"],
    },
    {
        "slug": "annualized-vol",
        "industry": "securities",
        "cat": "securities",
        "icon": "activity",
        "bg": "from-indigo-500 to-blue-600",
        "title": "年化波动率计算器",
        "h1": "σ_年 = σ_日 × √252",
        "h2": "由日波动率求年化波动率",
        "intro": "输入日波动率 σ_日，求年化波动率。",
        "desc": "年化波动率：输入 σ_日，输出 σ_年(%)。",
        "inputs": [
            {"id": "sd", "label": "日波动率 σ_日", "value": "0.01", "step": "0.001", "unit": ""},
        ],
        "calc": """
            const sd=num('sd');
            const sa=sd*Math.sqrt(252);
            ToolBox.setResult('result', dataGrid([
                [(sa*100).toFixed(2),'年化波动率 (%)']
            ]));
        """,
        "notes": ["252 为年化交易日数。", "0.01×√252 → 15.87%。"],
    },
    {
        "slug": "beta-covariance",
        "industry": "securities",
        "cat": "securities",
        "icon": "git-branch",
        "bg": "from-indigo-500 to-blue-600",
        "title": "协方差法 β 计算器",
        "h1": "β = Cov(r_i, r_m) / Var(r_m)",
        "h2": "由个股与市场收益率协方差与方差求 β",
        "intro": "输入个股与市场收益率协方差、市场收益率方差，求 β。",
        "desc": "协方差 β：输入 Cov、Var_m，输出 β。",
        "inputs": [
            {"id": "cov", "label": "协方差 Cov", "value": "0.002", "step": "0.0002", "unit": ""},
            {"id": "varm", "label": "市场方差 Var_m", "value": "0.0016", "step": "0.0002", "unit": ""},
        ],
        "calc": """
            const cov=num('cov'),varm=num('varm');
            const beta=cov/varm;
            ToolBox.setResult('result', dataGrid([
                [beta.toFixed(3),'β']
            ]));
        """,
        "notes": ["β 衡量个股相对市场系统性风险。", "0.002/0.0016 → 1.25。"],
    },
    {
        "slug": "tracking-error",
        "industry": "securities",
        "cat": "securities",
        "icon": "crosshair",
        "bg": "from-indigo-500 to-blue-600",
        "title": "跟踪误差计算器",
        "h1": "TE = std(r_p − r_b)",
        "h2": "由主动收益序列求跟踪误差",
        "intro": "输入组合与基准的超额收益序列（逗号或空格分隔），求跟踪误差。",
        "desc": "跟踪误差：输入 超额收益列表，输出 TE(%)。",
        "inputs": [
            {"id": "ex", "label": "超额收益序列", "value": "0.01, -0.005, 0.008, 0.002, -0.003", "step": "0.001", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('ex').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            const mean=raw.reduce((a,b)=>a+b,0)/raw.length;
            let v=0; for(const x of raw){ v+=Math.pow(x-mean,2); }
            const te=Math.sqrt(v/raw.length);
            ToolBox.setResult('result', dataGrid([
                [(te*100).toFixed(3),'跟踪误差 TE (%)']
            ]));
        """,
        "notes": ["TE 越小越贴近基准。", "示例序列 → 约 0.589%。"],
    },
    {
        "slug": "information-ratio",
        "industry": "securities",
        "cat": "securities",
        "icon": "bar-chart",
        "bg": "from-indigo-500 to-blue-600",
        "title": "信息比率计算器",
        "h1": "IR = 平均主动收益 / 跟踪误差",
        "h2": "由主动收益序列求信息比率",
        "intro": "输入组合与基准的超额收益序列（逗号或空格分隔），求信息比率。",
        "desc": "信息比率：输入 超额收益列表，输出 IR。",
        "inputs": [
            {"id": "ex", "label": "超额收益序列", "value": "0.01, -0.005, 0.008, 0.002, -0.003", "step": "0.001", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('ex').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            const mean=raw.reduce((a,b)=>a+b,0)/raw.length;
            let v=0; for(const x of raw){ v+=Math.pow(x-mean,2); }
            const te=Math.sqrt(v/raw.length);
            const ir=mean/te;
            ToolBox.setResult('result', dataGrid([
                [ir.toFixed(3),'信息比率 IR']
            ]));
        """,
        "notes": ["IR 衡量单位主动风险超额收益。", "示例序列 → 约 0.408。"],
    },
    {
        "slug": "max-drawdown",
        "industry": "securities",
        "cat": "securities",
        "icon": "trending-down",
        "bg": "from-indigo-500 to-blue-600",
        "title": "最大回撤计算器",
        "h1": "MD = (峰值 − 谷值) / 峰值",
        "h2": "由价格峰值与谷值求最大回撤",
        "intro": "输入区间价格峰值与谷值，求最大回撤。",
        "desc": "最大回撤：输入 峰值、谷值，输出 MD(%)。",
        "inputs": [
            {"id": "peak", "label": "峰值", "value": "100", "step": "5", "unit": ""},
            {"id": "trough", "label": "谷值", "value": "70", "step": "5", "unit": ""},
        ],
        "calc": """
            const peak=num('peak'),trough=num('trough');
            const md=(peak-trough)/peak*100;
            ToolBox.setResult('result', dataGrid([
                [md.toFixed(2),'最大回撤 MD (%)']
            ]));
        """,
        "notes": ["回撤越小风险承受越舒适。", "(100−70)/100 → 30%。"],
    },
    {
        "slug": "option-breakeven-put",
        "industry": "securities",
        "cat": "securities",
        "icon": "arrow-down-right",
        "bg": "from-indigo-500 to-blue-600",
        "title": "看跌期权盈亏平衡价计算器",
        "h1": "BE = 行权价 − 权利金",
        "h2": "由行权价与权利金求看跌期权盈亏平衡价",
        "intro": "输入行权价与权利金，求看跌期权盈亏平衡价。",
        "desc": "看跌期权平衡价：输入 行权价、权利金，输出 BE。",
        "inputs": [
            {"id": "K", "label": "行权价 K", "value": "50", "step": "1", "unit": "元"},
            {"id": "P", "label": "权利金 P", "value": "3", "step": "0.2", "unit": "元"},
        ],
        "calc": """
            const K=num('K'),P=num('P');
            const BE=K-P;
            ToolBox.setResult('result', dataGrid([
                [BE.toFixed(2),'盈亏平衡价 BE (元)']
            ]));
        """,
        "notes": ["标的跌破此价开始盈利。", "50−3 → 47 元。"],
    },
    {
        "slug": "margin-requirement",
        "industry": "securities",
        "cat": "securities",
        "icon": "shield",
        "bg": "from-indigo-500 to-blue-600",
        "title": "保证金比例计算器",
        "h1": "保证金比例 = 权益 / 持仓市值",
        "h2": "由账户权益与持仓市值求保证金比例",
        "intro": "输入账户权益与持仓市值，求保证金比例。",
        "desc": "保证金比例：输入 权益、持仓市值，输出 (%)。",
        "inputs": [
            {"id": "eq", "label": "账户权益", "value": "25000", "step": "1000", "unit": "元"},
            {"id": "pos", "label": "持仓市值", "value": "100000", "step": "5000", "unit": "元"},
        ],
        "calc": """
            const eq=num('eq'),pos=num('pos');
            const mr=eq/pos*100;
            ToolBox.setResult('result', dataGrid([
                [mr.toFixed(1),'保证金比例 (%)']
            ]));
        """,
        "notes": ["比例越低杠杆越高、强平风险越大。", "25000/100000 → 25%。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
