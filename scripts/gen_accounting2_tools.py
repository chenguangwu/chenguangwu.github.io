# -*- coding: utf-8 -*-
"""Batch 65: 会计分析深化 II（14 个公式计算器）。industry=accounting。"""
from tool_template import main

TOOLS = [
    {
        "slug": "ebitda",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "calculator",
        "bg": "from-emerald-500 to-green-600",
        "title": "EBITDA 计算器",
        "h1": "EBITDA = EBIT + 折旧摊销",
        "h2": "由息税前利润与折旧摊销求 EBITDA",
        "intro": "输入 EBIT 与折旧摊销，求 EBITDA。",
        "desc": "EBITDA：输入 EBIT、折旧摊销，输出 EBITDA。",
        "inputs": [
            {"id": "EBIT", "label": "息税前利润 EBIT", "value": "200", "step": "10", "unit": "万元"},
            {"id": "DA", "label": "折旧摊销", "value": "50", "step": "5", "unit": "万元"},
        ],
        "calc": """
            const EBIT=num('EBIT'),DA=num('DA');
            const ebitda=EBIT+DA;
            ToolBox.setResult('result', dataGrid([
                [ebitda.toFixed(2),'EBITDA (万元)']
            ]));
        """,
        "notes": ["EBITDA 近似经营现金流。", "200+50 → 250 万。"],
    },
    {
        "slug": "ebit",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "calculator",
        "bg": "from-emerald-500 to-green-600",
        "title": "EBIT 息税前利润计算器",
        "h1": "EBIT = 营收 − 营业成本 − 营业费用",
        "h2": "由营收、营业成本与费用求 EBIT",
        "intro": "输入营业收入、营业成本与营业费用，求 EBIT。",
        "desc": "EBIT：输入 营收、成本、费用，输出 EBIT。",
        "inputs": [
            {"id": "rev", "label": "营业收入", "value": "1000", "step": "50", "unit": "万元"},
            {"id": "cogs", "label": "营业成本", "value": "600", "step": "30", "unit": "万元"},
            {"id": "opex", "label": "营业费用", "value": "200", "step": "10", "unit": "万元"},
        ],
        "calc": """
            const rev=num('rev'),cogs=num('cogs'),opex=num('opex');
            const ebit=rev-cogs-opex;
            ToolBox.setResult('result', dataGrid([
                [ebit.toFixed(2),'EBIT (万元)']
            ]));
        """,
        "notes": ["剔除利息与税的经营利润。", "1000−600−200 → 200 万。"],
    },
    {
        "slug": "operating-cash-flow",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "droplets",
        "bg": "from-emerald-500 to-green-600",
        "title": "经营活动现金流计算器",
        "h1": "OCF = 净利润 + 折旧摊销 − 营运资本变动",
        "h2": "由净利润、折旧摊销与营运资本变动求 OCF",
        "intro": "输入净利润、折旧摊销与营运资本增加额，求经营现金流。",
        "desc": "经营现金流：输入 净利、折旧、ΔWC，输出 OCF。",
        "inputs": [
            {"id": "NI", "label": "净利润", "value": "120", "step": "10", "unit": "万元"},
            {"id": "DA", "label": "折旧摊销", "value": "50", "step": "5", "unit": "万元"},
            {"id": "dWC", "label": "营运资本增加", "value": "20", "step": "5", "unit": "万元"},
        ],
        "calc": """
            const NI=num('NI'),DA=num('DA'),dWC=num('dWC');
            const OCF=NI+DA-dWC;
            ToolBox.setResult('result', dataGrid([
                [OCF.toFixed(2),'经营现金流 OCF (万元)']
            ]));
        """,
        "notes": ["间接法起点为净利润。", "120+50−20 → 150 万。"],
    },
    {
        "slug": "free-cash-flow",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "droplets",
        "bg": "from-emerald-500 to-green-600",
        "title": "自由现金流计算器",
        "h1": "FCF = OCF − 资本支出",
        "h2": "由经营现金流与资本支出求自由现金流",
        "intro": "输入经营现金流与资本支出，求自由现金流。",
        "desc": "自由现金流：输入 OCF、资本支出，输出 FCF。",
        "inputs": [
            {"id": "OCF", "label": "经营现金流 OCF", "value": "150", "step": "10", "unit": "万元"},
            {"id": "capex", "label": "资本支出", "value": "80", "step": "5", "unit": "万元"},
        ],
        "calc": """
            const OCF=num('OCF'),capex=num('capex');
            const FCF=OCF-capex;
            ToolBox.setResult('result', dataGrid([
                [FCF.toFixed(2),'自由现金流 FCF (万元)']
            ]));
        """,
        "notes": ["FCF 可分配于偿债与分红。", "150−80 → 70 万。"],
    },
    {
        "slug": "working-capital",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "layers",
        "bg": "from-emerald-500 to-green-600",
        "title": "营运资金计算器",
        "h1": "WC = 流动资产 − 流动负债",
        "h2": "由流动资产与流动负债求营运资金",
        "intro": "输入流动资产与流动负债，求营运资金。",
        "desc": "营运资金：输入 流动资产、流动负债，输出 WC。",
        "inputs": [
            {"id": "CA", "label": "流动资产", "value": "500", "step": "20", "unit": "万元"},
            {"id": "CL", "label": "流动负债", "value": "300", "step": "20", "unit": "万元"},
        ],
        "calc": """
            const CA=num('CA'),CL=num('CL');
            const WC=CA-CL;
            ToolBox.setResult('result', dataGrid([
                [WC.toFixed(2),'营运资金 WC (万元)']
            ]));
        """,
        "notes": ["WC>0 通常表示短期偿债能力良好。", "500−300 → 200 万。"],
    },
    {
        "slug": "days-sales-outstanding",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "clock",
        "bg": "from-emerald-500 to-green-600",
        "title": "应收账款周转天数计算器",
        "h1": "DSO = 应收账款 / 营收 × 365",
        "h2": "由应收账款与营收求收款天数",
        "intro": "输入应收账款与年营业收入，求 DSO。",
        "desc": "应收账款天数：输入 应收、营收，输出 DSO(天)。",
        "inputs": [
            {"id": "AR", "label": "应收账款", "value": "100", "step": "10", "unit": "万元"},
            {"id": "rev", "label": "营业收入", "value": "1000", "step": "50", "unit": "万元"},
        ],
        "calc": """
            const AR=num('AR'),rev=num('rev');
            const DSO=AR/rev*365;
            ToolBox.setResult('result', dataGrid([
                [DSO.toFixed(1),'应收账款天数 DSO (天)']
            ]));
        """,
        "notes": ["DSO 越短回款越快。", "100/1000×365 → 36.5 天。"],
    },
    {
        "slug": "days-payable-outstanding",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "clock",
        "bg": "from-emerald-500 to-green-600",
        "title": "应付账款周转天数计算器",
        "h1": "DPO = 应付账款 / 营业成本 × 365",
        "h2": "由应付账款与营业成本求付款天数",
        "intro": "输入应付账款与年营业成本，求 DPO。",
        "desc": "应付账款天数：输入 应付、成本，输出 DPO(天)。",
        "inputs": [
            {"id": "AP", "label": "应付账款", "value": "80", "step": "10", "unit": "万元"},
            {"id": "cogs", "label": "营业成本", "value": "600", "step": "30", "unit": "万元"},
        ],
        "calc": """
            const AP=num('AP'),cogs=num('cogs');
            const DPO=AP/cogs*365;
            ToolBox.setResult('result', dataGrid([
                [DPO.toFixed(1),'应付账款天数 DPO (天)']
            ]));
        """,
        "notes": ["DPO 越长占用供应商资金越久。", "80/600×365 → 48.7 天。"],
    },
    {
        "slug": "cash-conversion-cycle",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "refresh-cw",
        "bg": "from-emerald-500 to-green-600",
        "title": "现金转换周期计算器",
        "h1": "CCC = DSO + DIO − DPO",
        "h2": "由应收、存货与应付天数求现金周期",
        "intro": "输入应收账款天数、存货天数与应付账款天数，求现金转换周期。",
        "desc": "现金转换周期：输入 DSO、DIO、DPO，输出 CCC(天)。",
        "inputs": [
            {"id": "DSO", "label": "应收天数 DSO", "value": "36.5", "step": "2", "unit": "天"},
            {"id": "DIO", "label": "存货天数 DIO", "value": "91.25", "step": "2", "unit": "天"},
            {"id": "DPO", "label": "应付天数 DPO", "value": "48.67", "step": "2", "unit": "天"},
        ],
        "calc": """
            const DSO=num('DSO'),DIO=num('DIO'),DPO=num('DPO');
            const CCC=DSO+DIO-DPO;
            ToolBox.setResult('result', dataGrid([
                [CCC.toFixed(2),'现金转换周期 CCC (天)']
            ]));
        """,
        "notes": ["CCC 越短资金效率越高。", "36.5+91.25−48.67 → 79.08 天。"],
    },
    {
        "slug": "roe-dupont",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "pie-chart",
        "bg": "from-emerald-500 to-green-600",
        "title": "杜邦分析 ROE 计算器",
        "h1": "ROE = 净利率 × 资产周转率 × 权益乘数",
        "h2": "由三因子求净资产收益率",
        "intro": "输入净利率、资产周转率与权益乘数，求 ROE。",
        "desc": "杜邦 ROE：输入 净利率(%)、资产周转率、权益乘数，输出 ROE(%)。",
        "inputs": [
            {"id": "nm", "label": "净利率", "value": "12", "step": "1", "unit": "%"},
            {"id": "at", "label": "资产周转率", "value": "1.5", "step": "0.1", "unit": ""},
            {"id": "em", "label": "权益乘数", "value": "2.0", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const nm=num('nm')/100,at=num('at'),em=num('em');
            const roe=nm*at*em*100;
            ToolBox.setResult('result', dataGrid([
                [roe.toFixed(2),'净资产收益率 ROE (%)']
            ]));
        """,
        "notes": ["杜邦分解揭示 ROE 驱动。", "12%×1.5×2.0 → 36%。"],
    },
    {
        "slug": "asset-turnover",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "repeat",
        "bg": "from-emerald-500 to-green-600",
        "title": "资产周转率计算器",
        "h1": "资产周转率 = 营收 / 总资产",
        "h2": "由营收与总资产求资产周转率",
        "intro": "输入营业收入与总资产，求资产周转率。",
        "desc": "资产周转率：输入 营收、总资产，输出 周转率。",
        "inputs": [
            {"id": "rev", "label": "营业收入", "value": "1000", "step": "50", "unit": "万元"},
            {"id": "assets", "label": "总资产", "value": "500", "step": "20", "unit": "万元"},
        ],
        "calc": """
            const rev=num('rev'),assets=num('assets');
            const at=rev/assets;
            ToolBox.setResult('result', dataGrid([
                [at.toFixed(2),'资产周转率']
            ]));
        """,
        "notes": ["衡量资产创收效率。", "1000/500 → 2.0。"],
    },
    {
        "slug": "inventory-days",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "box",
        "bg": "from-emerald-500 to-green-600",
        "title": "存货周转天数计算器",
        "h1": "DIO = 存货 / 营业成本 × 365",
        "h2": "由存货与营业成本求存货天数",
        "intro": "输入存货余额与年营业成本，求存货周转天数。",
        "desc": "存货天数：输入 存货、成本，输出 DIO(天)。",
        "inputs": [
            {"id": "inv", "label": "存货余额", "value": "150", "step": "10", "unit": "万元"},
            {"id": "cogs", "label": "营业成本", "value": "600", "step": "30", "unit": "万元"},
        ],
        "calc": """
            const inv=num('inv'),cogs=num('cogs');
            const DIO=inv/cogs*365;
            ToolBox.setResult('result', dataGrid([
                [DIO.toFixed(1),'存货天数 DIO (天)']
            ]));
        """,
        "notes": ["DIO 越短变现越快。", "150/600×365 → 91.25 天。"],
    },
    {
        "slug": "debt-service-coverage",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "shield",
        "bg": "from-emerald-500 to-green-600",
        "title": "偿债保障倍数计算器",
        "h1": "DSCR = 经营现金流 / 债务偿付",
        "h2": "由经营现金流与债务偿付额求保障倍数",
        "intro": "输入经营现金流与年度债务偿付额，求 DSCR。",
        "desc": "偿债保障倍数：输入 OCF、债务偿付，输出 DSCR。",
        "inputs": [
            {"id": "OCF", "label": "经营现金流 OCF", "value": "150", "step": "10", "unit": "万元"},
            {"id": "ds", "label": "债务偿付额", "value": "60", "step": "5", "unit": "万元"},
        ],
        "calc": """
            const OCF=num('OCF'),ds=num('ds');
            const DSCR=OCF/ds;
            ToolBox.setResult('result', dataGrid([
                [DSCR.toFixed(2),'偿债保障倍数 DSCR']
            ]));
        """,
        "notes": ["DSCR>1 才足以覆盖债务。", "150/60 → 2.5。"],
    },
    {
        "slug": "interest-coverage",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "shield",
        "bg": "from-emerald-500 to-green-600",
        "title": "利息保障倍数计算器",
        "h1": "利息保障倍数 = EBIT / 利息费用",
        "h2": "由 EBIT 与利息费用求保障倍数",
        "intro": "输入 EBIT 与利息费用，求利息保障倍数。",
        "desc": "利息保障倍数：输入 EBIT、利息，输出 倍数。",
        "inputs": [
            {"id": "EBIT", "label": "EBIT", "value": "200", "step": "10", "unit": "万元"},
            {"id": "int", "label": "利息费用", "value": "40", "step": "5", "unit": "万元"},
        ],
        "calc": """
            const EBIT=num('EBIT'),int=num('int');
            const ic=EBIT/int;
            ToolBox.setResult('result', dataGrid([
                [ic.toFixed(2),'利息保障倍数']
            ]));
        """,
        "notes": ["倍数越高付息越安全。", "200/40 → 5.0。"],
    },
    {
        "slug": "gross-profit",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "trending-up",
        "bg": "from-emerald-500 to-green-600",
        "title": "毛利计算器",
        "h1": "毛利 = 营业收入 − 营业成本",
        "h2": "由营收与营业成本求毛利",
        "intro": "输入营业收入与营业成本，求毛利。",
        "desc": "毛利：输入 营收、成本，输出 毛利。",
        "inputs": [
            {"id": "rev", "label": "营业收入", "value": "1000", "step": "50", "unit": "万元"},
            {"id": "cogs", "label": "营业成本", "value": "600", "step": "30", "unit": "万元"},
        ],
        "calc": """
            const rev=num('rev'),cogs=num('cogs');
            const gp=rev-cogs;
            ToolBox.setResult('result', dataGrid([
                [gp.toFixed(2),'毛利 (万元)']
            ]));
        """,
        "notes": ["毛利为营收减直接成本。", "1000−600 → 400 万。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
