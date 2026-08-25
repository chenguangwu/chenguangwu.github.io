# -*- coding: utf-8 -*-
"""Batch 58: 银行学深化 II（14 个公式计算器）。industry=banking。"""
from tool_template import main

TOOLS = [
    {
        "slug": "compound-interest",
        "industry": "banking",
        "cat": "banking",
        "icon": "trending-up",
        "bg": "from-green-500 to-emerald-600",
        "title": "复利终值计算器",
        "h1": "A = P(1 + r/n)^{nt}",
        "h2": "由本金、利率与复利频率求终值",
        "intro": "输入本金 P、名义年利率 r、每年复利次数 n、年数 t，求终值。",
        "desc": "复利终值计算器：输入 P、r、n、t，输出 A。",
        "inputs": [
            {"id": "P", "label": "本金 P", "value": "1000", "step": "50", "unit": "元"},
            {"id": "r", "label": "年利率 r", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "n", "label": "年复利次数 n", "value": "12", "step": "1", "unit": "次/年"},
            {"id": "t", "label": "年数 t", "value": "10", "step": "1", "unit": "年"},
        ],
        "calc": """
            const P=num('P'),r=num('r'),n=num('n'),t=num('t');
            const A=P*Math.pow(1+r/n,n*t);
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(2),'终值 A (元)']
            ]));
        """,
        "notes": ["A = P(1+r/n)^{nt}。", "1000 元,5%,月复利,10 年 → 约 1647 元。"],
    },
    {
        "slug": "perpetuity-pv",
        "industry": "banking",
        "cat": "banking",
        "icon": "infinity",
        "bg": "from-green-500 to-emerald-600",
        "title": "永续年金现值计算器",
        "h1": "PV = C / r",
        "h2": "由每期现金流与贴现率求永续年金现值",
        "intro": "输入每期现金流 C 与贴现率 r，求永续年金现值。",
        "desc": "永续年金现值：输入 C、r，输出 PV。",
        "inputs": [
            {"id": "C", "label": "每期现金流 C", "value": "100", "step": "5", "unit": "元"},
            {"id": "r", "label": "贴现率 r", "value": "0.05", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const C=num('C'),r=num('r');
            const PV=C/r;
            ToolBox.setResult('result', dataGrid([
                [PV.toFixed(2),'现值 PV (元)']
            ]));
        """,
        "notes": ["PV = C/r（永续）。", "C=100,r=5% → 2000 元。"],
    },
    {
        "slug": "apy-calculator",
        "industry": "banking",
        "cat": "banking",
        "icon": "percent",
        "bg": "from-green-500 to-emerald-600",
        "title": "年化收益率(APY)计算器",
        "h1": "APY = (1 + r/n)^n − 1",
        "h2": "由名义利率与复利频率求实际年化收益率",
        "intro": "输入名义年利率 r 与每年复利次数 n，求 APY。",
        "desc": "年化收益率 APY：输入 r、n，输出 APY(%)。",
        "inputs": [
            {"id": "r", "label": "名义年利率 r", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "n", "label": "年复利次数 n", "value": "12", "step": "1", "unit": "次/年"},
        ],
        "calc": """
            const r=num('r'),n=num('n');
            const APY=Math.pow(1+r/n,n)-1;
            ToolBox.setResult('result', dataGrid([
                [(APY*100).toFixed(3),'年化收益率 APY (%)']
            ]));
        """,
        "notes": ["APY = (1+r/n)^n−1。", "5%,月复利 → 约 5.116%。"],
    },
    {
        "slug": "nominal-from-effective",
        "industry": "banking",
        "cat": "banking",
        "icon": "percent",
        "bg": "from-green-500 to-emerald-600",
        "title": "由实际利率反推名义利率",
        "h1": "r = n[(1+EAR)^{1/n} − 1]",
        "h2": "由实际年化利率与复利频率求名义利率",
        "intro": "输入实际年化利率 EAR 与每年复利次数 n，求名义年利率。",
        "desc": "由实际利率反推名义利率：输入 EAR、n，输出 r(%)。",
        "inputs": [
            {"id": "EAR", "label": "实际年利率 EAR", "value": "0.05116", "step": "0.001", "unit": ""},
            {"id": "n", "label": "年复利次数 n", "value": "12", "step": "1", "unit": "次/年"},
        ],
        "calc": """
            const EAR=num('EAR'),n=num('n');
            const r=n*(Math.pow(1+EAR,1/n)-1);
            ToolBox.setResult('result', dataGrid([
                [(r*100).toFixed(3),'名义年利率 r (%)']
            ]));
        """,
        "notes": ["r = n[(1+EAR)^{1/n}−1]。", "EAR=5.116%,月复利 → 5.0%。"],
    },
    {
        "slug": "growing-annuity-pv",
        "industry": "banking",
        "cat": "banking",
        "icon": "trending-up",
        "bg": "from-green-500 to-emerald-600",
        "title": "增长年金现值计算器",
        "h1": "PV = C/(r−g)·[1−((1+g)/(1+r))^n]",
        "h2": "由首期现金流、增长率与贴现率求现值",
        "intro": "输入首期现金流 C、贴现率 r、增长率 g、期数 n，求增长年金现值。",
        "desc": "增长年金现值：输入 C、r、g、n，输出 PV。",
        "inputs": [
            {"id": "C", "label": "首期现金流 C", "value": "100", "step": "5", "unit": "元"},
            {"id": "r", "label": "贴现率 r", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "g", "label": "增长率 g", "value": "0.02", "step": "0.005", "unit": ""},
            {"id": "n", "label": "期数 n", "value": "10", "step": "1", "unit": ""},
        ],
        "calc": """
            const C=num('C'),r=num('r'),g=num('g'),n=num('n');
            const PV=C/(r-g)*(1-Math.pow((1+g)/(1+r),n));
            ToolBox.setResult('result', dataGrid([
                [PV.toFixed(2),'现值 PV (元)']
            ]));
        """,
        "notes": ["要求 r>g。", "C=100,r=5%,g=2%,n=10 → 约 840 元。"],
    },
    {
        "slug": "present-value-annuity-due",
        "industry": "banking",
        "cat": "banking",
        "icon": "arrow-left",
        "bg": "from-green-500 to-emerald-600",
        "title": "期初年金现值计算器",
        "h1": "PV = PMT·[1−(1+r)^{−n}]/r·(1+r)",
        "h2": "由每期付款、利率与期数求期初年金现值",
        "intro": "输入每期付款 PMT、每期利率 r、期数 n，求期初年金现值。",
        "desc": "期初年金现值：输入 PMT、r、n，输出 PV。",
        "inputs": [
            {"id": "PMT", "label": "每期付款 PMT", "value": "100", "step": "10", "unit": "元"},
            {"id": "r", "label": "每期利率 r", "value": "0.005", "step": "0.001", "unit": ""},
            {"id": "n", "label": "期数 n", "value": "12", "step": "1", "unit": ""},
        ],
        "calc": """
            const PMT=num('PMT'),r=num('r'),n=num('n');
            const PV=PMT*(1-Math.pow(1+r,-n))/r*(1+r);
            ToolBox.setResult('result', dataGrid([
                [PV.toFixed(2),'现值 PV (元)']
            ]));
        """,
        "notes": ["期初年金每期期初收付。", "100 元,0.5%/期,12 期 → 约 1168 元。"],
    },
    {
        "slug": "future-value-annuity-due",
        "industry": "banking",
        "cat": "banking",
        "icon": "arrow-right",
        "bg": "from-green-500 to-emerald-600",
        "title": "期初年金终值计算器",
        "h1": "FV = PMT·[(1+r)^n−1]/r·(1+r)",
        "h2": "由每期付款、利率与期数求期初年金终值",
        "intro": "输入每期付款 PMT、每期利率 r、期数 n，求期初年金终值。",
        "desc": "期初年金终值：输入 PMT、r、n，输出 FV。",
        "inputs": [
            {"id": "PMT", "label": "每期付款 PMT", "value": "100", "step": "10", "unit": "元"},
            {"id": "r", "label": "每期利率 r", "value": "0.005", "step": "0.001", "unit": ""},
            {"id": "n", "label": "期数 n", "value": "12", "step": "1", "unit": ""},
        ],
        "calc": """
            const PMT=num('PMT'),r=num('r'),n=num('n');
            const FV=PMT*(Math.pow(1+r,n)-1)/r*(1+r);
            ToolBox.setResult('result', dataGrid([
                [FV.toFixed(2),'终值 FV (元)']
            ]));
        """,
        "notes": ["期初年金每期期初收付。", "100 元,0.5%/期,12 期 → 约 1240 元。"],
    },
    {
        "slug": "loan-tenure",
        "industry": "banking",
        "cat": "banking",
        "icon": "clock",
        "bg": "from-green-500 to-emerald-600",
        "title": "贷款期限计算器",
        "h1": "n = −ln(1 − Pr/PMT) / ln(1+r)",
        "h2": "由贷款额、利率与月供反推还款期数",
        "intro": "输入贷款本金 P、每期利率 r、每期还款 PMT，求还款期数。",
        "desc": "贷款期限：输入 P、r、PMT，输出 n(期)。",
        "inputs": [
            {"id": "P", "label": "贷款本金 P", "value": "10000", "step": "500", "unit": "元"},
            {"id": "r", "label": "每期利率 r", "value": "0.005", "step": "0.001", "unit": ""},
            {"id": "PMT", "label": "每期还款 PMT", "value": "200", "step": "10", "unit": "元"},
        ],
        "calc": """
            const P=num('P'),r=num('r'),PMT=num('PMT');
            const n=-Math.log(1-P*r/PMT)/Math.log(1+r);
            ToolBox.setResult('result', dataGrid([
                [n.toFixed(1),'还款期数 n (期)']
            ]));
        """,
        "notes": ["由年金现值公式反解 n。", "1万,0.5%/期,200/期 → 约 57.7 期。"],
    },
    {
        "slug": "credit-card-interest-monthly",
        "industry": "banking",
        "cat": "banking",
        "icon": "credit-card",
        "bg": "from-green-500 to-emerald-600",
        "title": "信用卡循环利息计算器",
        "h1": "I = 余额 × 日利率 × 天数",
        "h2": "由欠款余额与日利率求月利息",
        "intro": "输入欠款余额、日利率、计息天数，求利息。",
        "desc": "信用卡循环利息：输入 余额、日利率、天数，输出 I。",
        "inputs": [
            {"id": "bal", "label": "欠款余额", "value": "1000", "step": "50", "unit": "元"},
            {"id": "dr", "label": "日利率", "value": "0.0005", "step": "0.0001", "unit": ""},
            {"id": "days", "label": "计息天数", "value": "30", "step": "1", "unit": "天"},
        ],
        "calc": """
            const bal=num('bal'),dr=num('dr'),days=num('days');
            const I=bal*dr*days;
            ToolBox.setResult('result', dataGrid([
                [I.toFixed(2),'利息 I (元)']
            ]));
        """,
        "notes": ["I = 余额×日利率×天数。", "1000 元,0.05%/天,30 天 → 15 元。"],
    },
    {
        "slug": "bond-current-yield",
        "industry": "banking",
        "cat": "banking",
        "icon": "line-chart",
        "bg": "from-green-500 to-emerald-600",
        "title": "债券当前收益率计算器",
        "h1": "CY = 年息 / 市价",
        "h2": "由年利息与债券价格求当前收益率",
        "intro": "输入年利息（票息）与债券市场价格，求当前收益率。",
        "desc": "债券当前收益率：输入 年息、市价，输出 CY(%)。",
        "inputs": [
            {"id": "c", "label": "年利息", "value": "50", "step": "2", "unit": "元"},
            {"id": "p", "label": "债券市价", "value": "980", "step": "10", "unit": "元"},
        ],
        "calc": """
            const c=num('c'),p=num('p');
            const CY=c/p;
            ToolBox.setResult('result', dataGrid([
                [(CY*100).toFixed(3),'当前收益率 CY (%)']
            ]));
        """,
        "notes": ["CY = 年息/市价。", "年息 50,市价 980 → 5.10%。"],
    },
    {
        "slug": "loan-to-value",
        "industry": "banking",
        "cat": "banking",
        "icon": "scale",
        "bg": "from-green-500 to-emerald-600",
        "title": "贷款价值比(LTV)计算器",
        "h1": "LTV = 贷款额 / 抵押物价值",
        "h2": "由贷款额与抵押物价值求 LTV",
        "intro": "输入贷款额与抵押物评估价值，求贷款价值比。",
        "desc": "贷款价值比 LTV：输入 贷款额、价值，输出 LTV(%)。",
        "inputs": [
            {"id": "loan", "label": "贷款额", "value": "800000", "step": "10000", "unit": "元"},
            {"id": "val", "label": "抵押物价值", "value": "1000000", "step": "10000", "unit": "元"},
        ],
        "calc": """
            const loan=num('loan'),val=num('val');
            const LTV=loan/val*100;
            ToolBox.setResult('result', dataGrid([
                [LTV.toFixed(1),'贷款价值比 LTV (%)']
            ]));
        """,
        "notes": ["LTV 越低风险越小。", "80 万/100 万 → 80%。"],
    },
    {
        "slug": "debt-to-income",
        "industry": "banking",
        "cat": "banking",
        "icon": "scale",
        "bg": "from-green-500 to-emerald-600",
        "title": "债务收入比(DTI)计算器",
        "h1": "DTI = 月债务支出 / 月收入",
        "h2": "由月债务与月收入求债务收入比",
        "intro": "输入月债务支出与月收入，求债务收入比。",
        "desc": "债务收入比 DTI：输入 月债务、月收入，输出 DTI(%)。",
        "inputs": [
            {"id": "debt", "label": "月债务支出", "value": "3000", "step": "100", "unit": "元"},
            {"id": "inc", "label": "月收入", "value": "10000", "step": "500", "unit": "元"},
        ],
        "calc": """
            const debt=num('debt'),inc=num('inc');
            const DTI=debt/inc*100;
            ToolBox.setResult('result', dataGrid([
                [DTI.toFixed(1),'债务收入比 DTI (%)']
            ]));
        """,
        "notes": ["DTI 一般建议 <43%。", "3000/10000 → 30%。"],
    },
    {
        "slug": "net-worth",
        "industry": "banking",
        "cat": "banking",
        "icon": "wallet",
        "bg": "from-green-500 to-emerald-600",
        "title": "净资产计算器",
        "h1": "NW = 总资产 − 总负债",
        "h2": "由资产与负债求净资产",
        "intro": "输入总资产与总负债，求净资产。",
        "desc": "净资产：输入 资产、负债，输出 NW。",
        "inputs": [
            {"id": "assets", "label": "总资产", "value": "500000", "step": "10000", "unit": "元"},
            {"id": "liab", "label": "总负债", "value": "200000", "step": "10000", "unit": "元"},
        ],
        "calc": """
            const assets=num('assets'),liab=num('liab');
            const NW=assets-liab;
            ToolBox.setResult('result', dataGrid([
                [NW.toFixed(0),'净资产 NW (元)']
            ]));
        """,
        "notes": ["NW = 资产 − 负债。", "50 万 − 20 万 → 30 万。"],
    },
    {
        "slug": "tax-equivalent-yield",
        "industry": "banking",
        "cat": "banking",
        "icon": "percent",
        "bg": "from-green-500 to-emerald-600",
        "title": "税后等效收益率计算器",
        "h1": "TEY = 免税收益率 / (1 − 税率)",
        "h2": "由免税品种收益率与税率求税后等效收益率",
        "intro": "输入免税品种收益率与边际税率，求税后等效应税收益率。",
        "desc": "税后等效收益率：输入 免税收益率、税率，输出 TEY(%)。",
        "inputs": [
            {"id": "muni", "label": "免税收益率", "value": "0.03", "step": "0.005", "unit": ""},
            {"id": "tax", "label": "边际税率", "value": "0.25", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const muni=num('muni'),tax=num('tax');
            const TEY=muni/(1-tax);
            ToolBox.setResult('result', dataGrid([
                [(TEY*100).toFixed(3),'税后等效收益率 TEY (%)']
            ]));
        """,
        "notes": ["TEY = 免税收益率/(1−税率)。", "3%/(1−25%) → 4%。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
