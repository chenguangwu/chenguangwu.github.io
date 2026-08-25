# -*- coding: utf-8 -*-
"""Batch 41: 会计计算深化（14 个公式计算器）。industry=accounting。"""
from tool_template import main

TOOLS = [
    {
        "slug": "depreciation-straight",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "trending-down",
        "bg": "from-indigo-500 to-violet-600",
        "title": "直线折旧法",
        "h1": "直线折旧",
        "h2": "(原值 − 残值) / 年限",
        "intro": "年折旧 = (C − S) / n。",
        "desc": "输入原值、残值与使用年限，计算每年直线折旧额与折旧率。",
        "inputs": [
            {"id": "c", "label": "原值 C", "value": "100000", "step": "5000", "unit": "元"},
            {"id": "s", "label": "残值 S", "value": "10000", "step": "1000", "unit": "元"},
            {"id": "n", "label": "使用年限", "value": "10", "step": "1", "unit": "年"},
        ],
        "calc": """
            const c=num('c'),s=num('s'),n=num('n');
            const d=(c-s)/n;
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(2),'年折旧额 (元)'],
                [(d/c*100).toFixed(2),'年折旧率 (%)'],
                [(c-d).toFixed(2),'首年末账面值 (元)']
            ]));
        """,
        "notes": ["直线法各年折旧相同。", "残值不计提折旧。"],
    },
    {
        "slug": "depreciation-declining",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "arrow-down-right",
        "bg": "from-indigo-500 to-violet-600",
        "title": "双倍余额递减法",
        "h1": "双倍余额递减",
        "h2": "加速折旧",
        "intro": "年折旧 = 期初账面值 × 2/n（末年调至残值）。",
        "desc": "输入原值、残值、年限与指定年份，计算该年折旧额与期末账面值。",
        "inputs": [
            {"id": "c", "label": "原值 C", "value": "100000", "step": "5000", "unit": "元"},
            {"id": "s", "label": "残值 S", "value": "10000", "step": "1000", "unit": "元"},
            {"id": "n", "label": "使用年限", "value": "10", "step": "1", "unit": "年"},
            {"id": "yr", "label": "计算第几年", "value": "3", "step": "1", "unit": "年"},
        ],
        "calc": """
            const c=num('c'),s=num('s'),n=num('n'),yr=num('yr');
            const rate=2/n;
            let bv=c, accum=0, depYr=0;
            for(let k=1;k<=yr;k++){
                let d=bv*rate;
                if(k===n){ d=bv-s; }
                if(bv-d < s) d=bv-s;
                if(k===yr) depYr=d;
                accum+=d; bv-=d;
            }
            ToolBox.setResult('result', dataGrid([
                [depYr.toFixed(2),('第'+yr+'年折旧额 (元)')],
                [bv.toFixed(2),'期末账面值 (元)'],
                [(accum).toFixed(2),'累计折旧 (元)']
            ]));
        """,
        "notes": ["前期折旧多、后期少。", "最后两年通常改为直线调至残值。"],
    },
    {
        "slug": "depreciation-syd",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "layers",
        "bg": "from-indigo-500 to-violet-600",
        "title": "年数总和法",
        "h1": "年数总和法",
        "h2": "加速折旧",
        "intro": "年折旧 = (n−k+1)/SYD × (C−S)，SYD = n(n+1)/2。",
        "desc": "输入原值、残值、年限与指定年份，计算该年折旧额。",
        "inputs": [
            {"id": "c", "label": "原值 C", "value": "100000", "step": "5000", "unit": "元"},
            {"id": "s", "label": "残值 S", "value": "10000", "step": "1000", "unit": "元"},
            {"id": "n", "label": "使用年限", "value": "10", "step": "1", "unit": "年"},
            {"id": "yr", "label": "计算第几年", "value": "1", "step": "1", "unit": "年"},
        ],
        "calc": """
            const c=num('c'),s=num('s'),n=num('n'),yr=num('yr');
            const syd=n*(n+1)/2;
            const d=(n-yr+1)/syd*(c-s);
            ToolBox.setResult('result', dataGrid([
                [d.toFixed(2),('第'+yr+'年折旧额 (元)')],
                [(d/c*100).toFixed(2),'占原值比 (%)']
            ]));
        """,
        "notes": ["折旧额逐年递减。", "首年折旧最高。"],
    },
    {
        "slug": "amortization-intangible",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "clock",
        "bg": "from-indigo-500 to-violet-600",
        "title": "无形资产摊销",
        "h1": "无形资产摊销",
        "h2": "直线摊销",
        "intro": "年摊销 = (成本 − 残值) / 摊销年限。",
        "desc": "输入无形资产成本、残值与摊销年限，计算年摊销额。",
        "inputs": [
            {"id": "c", "label": "成本", "value": "600000", "step": "50000", "unit": "元"},
            {"id": "s", "label": "残值", "value": "0", "step": "1000", "unit": "元"},
            {"id": "n", "label": "摊销年限", "value": "10", "step": "1", "unit": "年"},
        ],
        "calc": """
            const c=num('c'),s=num('s'),n=num('n');
            ToolBox.setResult('result', dataGrid([
                [((c-s)/n).toFixed(2),'年摊销额 (元)'],
                [((c-s)/n/12).toFixed(2),'月摊销额 (元)']
            ]));
        """,
        "notes": ["使用寿命有限无形资产需摊销。", "与折旧本质相同。"],
    },
    {
        "slug": "gross-margin",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "percent",
        "bg": "from-indigo-500 to-violet-600",
        "title": "毛利率",
        "h1": "毛利率",
        "h2": "(收入 − 成本) / 收入",
        "intro": "毛利率 = (营收 − 营业成本) / 营收。",
        "desc": "输入营业收入与营业成本，计算毛利率。",
        "inputs": [
            {"id": "rev", "label": "营业收入", "value": "1000000", "step": "50000", "unit": "元"},
            {"id": "cost", "label": "营业成本", "value": "600000", "step": "50000", "unit": "元"},
        ],
        "calc": """
            const r=num('rev'),c=num('cost');
            ToolBox.setResult('result', dataGrid([
                [((r-c)/r*100).toFixed(2),'毛利率 (%)'],
                [(r-c).toFixed(0),'毛利额 (元)']
            ]));
        """,
        "notes": ["毛利率反映产品盈利能力。", "不同行业差异大。"],
    },
    {
        "slug": "net-profit-margin",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "trending-up",
        "bg": "from-indigo-500 to-violet-600",
        "title": "净利率",
        "h1": "净利率",
        "h2": "净利 / 收入",
        "intro": "净利率 = 净利润 / 营业收入。",
        "desc": "输入净利润与营业收入，计算净利率。",
        "inputs": [
            {"id": "np", "label": "净利润", "value": "150000", "step": "10000", "unit": "元"},
            {"id": "rev", "label": "营业收入", "value": "1000000", "step": "50000", "unit": "元"},
        ],
        "calc": """
            const np=num('np'),rev=num('rev');
            ToolBox.setResult('result', dataGrid([
                [(np/rev*100).toFixed(2),'净利率 (%)'],
                [(np/rev*100*12).toFixed(2),'年化 (%)']
            ]));
        """,
        "notes": ["净利率含全部费用与税。", "反映最终盈利水平。"],
    },
    {
        "slug": "break-even-units",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "scale",
        "bg": "from-indigo-500 to-violet-600",
        "title": "盈亏平衡产量",
        "h1": "盈亏平衡点",
        "h2": "FC / (P − VC)",
        "intro": "BEP = 固定成本 / (单价 − 单位变动成本)。",
        "desc": "输入固定成本、单价与单位变动成本，计算盈亏平衡产量与销售额。",
        "inputs": [
            {"id": "fc", "label": "固定成本", "value": "200000", "step": "10000", "unit": "元"},
            {"id": "p", "label": "单价 P", "value": "100", "step": "5", "unit": "元"},
            {"id": "vc", "label": "单位变动成本", "value": "60", "step": "5", "unit": "元"},
        ],
        "calc": """
            const fc=num('fc'),p=num('p'),vc=num('vc');
            const q=fc/(p-vc);
            ToolBox.setResult('result', dataGrid([
                [q.toFixed(1),'平衡产量 (件)'],
                [(q*p).toFixed(0),'平衡销售额 (元)'],
                [(p-vc).toFixed(2),'单位边际贡献 (元)']
            ]));
        """,
        "notes": ["销量超此点开始盈利。", "边际贡献=单价−单位变动。"],
    },
    {
        "slug": "contribution-margin",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "plus-circle",
        "bg": "from-indigo-500 to-violet-600",
        "title": "边际贡献",
        "h1": "边际贡献",
        "h2": "单价 − 单位变动成本",
        "intro": "单位边际贡献 = P − VC。",
        "desc": "输入单价、单位变动成本与销量，计算边际贡献总额与比率。",
        "inputs": [
            {"id": "p", "label": "单价 P", "value": "100", "step": "5", "unit": "元"},
            {"id": "vc", "label": "单位变动成本", "value": "60", "step": "5", "unit": "元"},
            {"id": "q", "label": "销量", "value": "10000", "step": "500", "unit": "件"},
        ],
        "calc": """
            const p=num('p'),vc=num('vc'),q=num('q');
            const cm=(p-vc)*q;
            const rev=p*q;
            ToolBox.setResult('result', dataGrid([
                [cm.toFixed(0),'边际贡献总额 (元)'],
                [(cm/rev*100).toFixed(2),'边际贡献率 (%)']
            ]));
        """,
        "notes": ["边际贡献先覆盖固定成本。", "再有余为利润。"],
    },
    {
        "slug": "roa-calc",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "bar-chart",
        "bg": "from-indigo-500 to-violet-600",
        "title": "总资产收益率 (ROA)",
        "h1": "ROA",
        "h2": "净利 / 总资产",
        "intro": "ROA = 净利润 / 平均总资产。",
        "desc": "输入净利润与总资产，计算资产收益率。",
        "inputs": [
            {"id": "np", "label": "净利润", "value": "200000", "step": "10000", "unit": "元"},
            {"id": "ta", "label": "总资产", "value": "5000000", "step": "100000", "unit": "元"},
        ],
        "calc": """
            const np=num('np'),ta=num('ta');
            ToolBox.setResult('result', dataGrid([
                [(np/ta*100).toFixed(2),'ROA (%)']
            ]));
        """,
        "notes": ["衡量资产使用效率。", "不同行业不可直接比。"],
    },
    {
        "slug": "roe-calc",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "award",
        "bg": "from-indigo-500 to-violet-600",
        "title": "净资产收益率 (ROE)",
        "h1": "ROE",
        "h2": "净利 / 净资产",
        "intro": "ROE = 净利润 / 平均净资产。",
        "desc": "输入净利润与净资产（所有者权益），计算权益收益率。",
        "inputs": [
            {"id": "np", "label": "净利润", "value": "200000", "step": "10000", "unit": "元"},
            {"id": "eq", "label": "净资产", "value": "2000000", "step": "100000", "unit": "元"},
        ],
        "calc": """
            const np=num('np'),eq=num('eq');
            ToolBox.setResult('result', dataGrid([
                [(np/eq*100).toFixed(2),'ROE (%)']
            ]));
        """,
        "notes": ["股东最关注的回报指标。", "高杠杆可放大 ROE。"],
    },
    {
        "slug": "current-ratio",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "droplet",
        "bg": "from-indigo-500 to-violet-600",
        "title": "流动比率",
        "h1": "流动比率",
        "h2": "流动资产 / 流动负债",
        "intro": "流动比率 = 流动资产 / 流动负债。",
        "desc": "输入流动资产与流动负债，计算短期偿债能力。",
        "inputs": [
            {"id": "ca", "label": "流动资产", "value": "3000000", "step": "100000", "unit": "元"},
            {"id": "cl", "label": "流动负债", "value": "1500000", "step": "100000", "unit": "元"},
        ],
        "calc": """
            const ca=num('ca'),cl=num('cl');
            ToolBox.setResult('result', dataGrid([
                [(ca/cl).toFixed(2),'流动比率'],
                [(cl/ca*100).toFixed(1),'流动负债占比 (%)']
            ]));
        """,
        "notes": [">2 较安全，但过高或闲置。", "需结合行业判断。"],
    },
    {
        "slug": "quick-ratio",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "zap",
        "bg": "from-indigo-500 to-violet-600",
        "title": "速动比率",
        "h1": "速动比率",
        "h2": "(流动资产 − 存货) / 流动负债",
        "intro": "速动比率剔除存货后的短期偿债能力。",
        "desc": "输入流动资产、存货与流动负债，计算速动比率。",
        "inputs": [
            {"id": "ca", "label": "流动资产", "value": "3000000", "step": "100000", "unit": "元"},
            {"id": "inv", "label": "存货", "value": "800000", "step": "50000", "unit": "元"},
            {"id": "cl", "label": "流动负债", "value": "1500000", "step": "100000", "unit": "元"},
        ],
        "calc": """
            const ca=num('ca'),inv=num('inv'),cl=num('cl');
            ToolBox.setResult('result', dataGrid([
                [((ca-inv)/cl).toFixed(2),'速动比率'],
                [(((ca-inv)/cl)>1?'达标(>1)':'偏低(<1)'),'评价']
            ]));
        """,
        "notes": ["剔除变现慢的存货。", "理想值约 1。"],
    },
    {
        "slug": "debt-to-asset",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "balance-scale",
        "bg": "from-indigo-500 to-violet-600",
        "title": "资产负债率",
        "h1": "资产负债率",
        "h2": "负债总额 / 资产总额",
        "intro": "资产负债率 = 总负债 / 总资产。",
        "desc": "输入总负债与总资产，计算杠杆水平。",
        "inputs": [
            {"id": "tl", "label": "总负债", "value": "3000000", "step": "100000", "unit": "元"},
            {"id": "ta", "label": "总资产", "value": "8000000", "step": "100000", "unit": "元"},
        ],
        "calc": """
            const tl=num('tl'),ta=num('ta');
            ToolBox.setResult('result', dataGrid([
                [(tl/ta*100).toFixed(2),'资产负债率 (%)'],
                [((1-tl/ta)*100).toFixed(2),'权益比率 (%)']
            ]));
        """,
        "notes": ["越高财务风险越大。", "行业资本结构差异大。"],
    },
    {
        "slug": "inventory-turnover",
        "industry": "accounting",
        "cat": "accounting",
        "icon": "refresh-cw",
        "bg": "from-indigo-500 to-violet-600",
        "title": "存货周转率",
        "h1": "存货周转率",
        "h2": "销售成本 / 平均存货",
        "intro": "周转率 = 营业成本 / 平均存货。",
        "desc": "输入销售成本与平均存货，计算存货周转率与周转天数。",
        "inputs": [
            {"id": "cogs", "label": "销售成本", "value": "4000000", "step": "100000", "unit": "元"},
            {"id": "inv", "label": "平均存货", "value": "800000", "step": "50000", "unit": "元"},
        ],
        "calc": """
            const cogs=num('cogs'),inv=num('inv');
            const turn=cogs/inv;
            ToolBox.setResult('result', dataGrid([
                [turn.toFixed(2),'存货周转率 (次/年)'],
                [(365/turn).toFixed(1),'周转天数 (天)']
            ]));
        """,
        "notes": ["周转率越高变现越快。", "天数 = 365 / 周转率。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
