# -*- coding: utf-8 -*-
"""Batch 59: 税务学深化 II（14 个公式计算器）。industry=tax。"""
from tool_template import main

TOOLS = [
    {
        "slug": "marginal-tax-rate",
        "industry": "tax",
        "cat": "tax",
        "icon": "percent",
        "bg": "from-blue-500 to-indigo-600",
        "title": "边际税率计算器",
        "h1": "MTR = (T₂ − T₁) / (Y₂ − Y₁)",
        "h2": "由相邻级距税额差与收入差求边际税率",
        "intro": "输入两级收入及对应应纳税额，求边际税率。",
        "desc": "边际税率：输入 Y1、T1、Y2、T2，输出 MTR(%)。",
        "inputs": [
            {"id": "Y1", "label": "收入1 Y₁", "value": "100000", "step": "1000", "unit": "元"},
            {"id": "T1", "label": "税额1 T₁", "value": "20000", "step": "500", "unit": "元"},
            {"id": "Y2", "label": "收入2 Y₂", "value": "150000", "step": "1000", "unit": "元"},
            {"id": "T2", "label": "税额2 T₂", "value": "35000", "step": "500", "unit": "元"},
        ],
        "calc": """
            const Y1=num('Y1'),T1=num('T1'),Y2=num('Y2'),T2=num('T2');
            const MTR=(T2-T1)/(Y2-Y1);
            ToolBox.setResult('result', dataGrid([
                [(MTR*100).toFixed(2),'边际税率 MTR (%)']
            ]));
        """,
        "notes": ["MTR = Δ税额/Δ收入。", "收入增 5 万、税额增 1.5 万 → 30%。"],
    },
    {
        "slug": "average-tax-rate",
        "industry": "tax",
        "cat": "tax",
        "icon": "percent",
        "bg": "from-blue-500 to-indigo-600",
        "title": "平均税率计算器",
        "h1": "ATR = T / Y",
        "h2": "由总税额与总收入求平均税率",
        "intro": "输入总税额与总收入，求平均税率。",
        "desc": "平均税率：输入 T、Y，输出 ATR(%)。",
        "inputs": [
            {"id": "T", "label": "总税额 T", "value": "30000", "step": "1000", "unit": "元"},
            {"id": "Y", "label": "总收入 Y", "value": "100000", "step": "1000", "unit": "元"},
        ],
        "calc": """
            const T=num('T'),Y=num('Y');
            const ATR=T/Y;
            ToolBox.setResult('result', dataGrid([
                [(ATR*100).toFixed(2),'平均税率 ATR (%)']
            ]));
        """,
        "notes": ["ATR = 总税额/总收入。", "3 万/10 万 → 30%。"],
    },
    {
        "slug": "tax-to-gdp",
        "industry": "tax",
        "cat": "tax",
        "icon": "bar-chart",
        "bg": "from-blue-500 to-indigo-600",
        "title": "宏观税负计算器",
        "h1": "宏观税负 = 税收总额 / GDP",
        "h2": "由税收总额与 GDP 求宏观税负",
        "intro": "输入税收总额与 GDP，求宏观税负。",
        "desc": "宏观税负：输入 税收、GDP，输出 (%)。",
        "inputs": [
            {"id": "tax", "label": "税收总额", "value": "18", "step": "1", "unit": "万亿"},
            {"id": "gdp", "label": "GDP", "value": "100", "step": "1", "unit": "万亿"},
        ],
        "calc": """
            const tax=num('tax'),gdp=num('gdp');
            const r=tax/gdp*100;
            ToolBox.setResult('result', dataGrid([
                [r.toFixed(2),'宏观税负 (%)']
            ]));
        """,
        "notes": ["宏观税负 = 税收/GDP。", "18 万亿/100 万亿 → 18%。"],
    },
    {
        "slug": "ad-valorem-duty",
        "industry": "tax",
        "cat": "tax",
        "icon": "package",
        "bg": "from-blue-500 to-indigo-600",
        "title": "从价税计算器",
        "h1": "T = 计税价格 × 税率",
        "h2": "由计税价格与从价税率求从价税",
        "intro": "输入计税价格与从价税率，求从价税。",
        "desc": "从价税：输入 价格、税率，输出 T。",
        "inputs": [
            {"id": "p", "label": "计税价格", "value": "1000", "step": "50", "unit": "元"},
            {"id": "r", "label": "税率", "value": "0.1", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const p=num('p'),r=num('r');
            const T=p*r;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'从价税 T (元)']
            ]));
        """,
        "notes": ["从价税按价格比例征收。", "1000 元×10% → 100 元。"],
    },
    {
        "slug": "specific-duty",
        "industry": "tax",
        "cat": "tax",
        "icon": "package",
        "bg": "from-blue-500 to-indigo-600",
        "title": "从量税计算器",
        "h1": "T = 数量 × 单位税额",
        "h2": "由应税数量与单位税额求从量税",
        "intro": "输入应税数量与单位税额，求从量税。",
        "desc": "从量税：输入 数量、单位税额，输出 T。",
        "inputs": [
            {"id": "q", "label": "应税数量", "value": "100", "step": "10", "unit": "件"},
            {"id": "u", "label": "单位税额", "value": "5", "step": "0.5", "unit": "元/件"},
        ],
        "calc": """
            const q=num('q'),u=num('u');
            const T=q*u;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'从量税 T (元)']
            ]));
        """,
        "notes": ["从量税按数量固定额度征收。", "100 件×5 元 → 500 元。"],
    },
    {
        "slug": "excise-tax",
        "industry": "tax",
        "cat": "tax",
        "icon": "percent",
        "bg": "from-blue-500 to-indigo-600",
        "title": "消费税(从价)计算器",
        "h1": "T = 出厂价 × 数量 × 税率",
        "h2": "由出厂单价、数量与消费税率求消费税",
        "intro": "输入出厂单价、数量与消费税率，求消费税。",
        "desc": "消费税从价计征：输入 单价、数量、税率，输出 T。",
        "inputs": [
            {"id": "p", "label": "出厂单价", "value": "10", "step": "1", "unit": "元"},
            {"id": "q", "label": "数量", "value": "100", "step": "10", "unit": "件"},
            {"id": "r", "label": "消费税率", "value": "0.2", "step": "0.02", "unit": ""},
        ],
        "calc": """
            const p=num('p'),q=num('q'),r=num('r');
            const T=p*q*r;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'消费税 T (元)']
            ]));
        """,
        "notes": ["从价消费税 = 计税价×数量×税率。", "10×100×20% → 200 元。"],
    },
    {
        "slug": "payroll-tax",
        "industry": "tax",
        "cat": "tax",
        "icon": "users",
        "bg": "from-blue-500 to-indigo-600",
        "title": "工薪税计算器",
        "h1": "T = 工资 × (雇主率 + 雇员率)",
        "h2": "由工资金额与双方费率求工薪税合计",
        "intro": "输入工资总额、雇主费率与雇员费率，求工薪税。",
        "desc": "工薪税：输入 工资、雇主率、雇员率，输出 T。",
        "inputs": [
            {"id": "w", "label": "工资总额", "value": "10000", "step": "500", "unit": "元"},
            {"id": "er", "label": "雇主费率", "value": "0.2", "step": "0.01", "unit": ""},
            {"id": "ee", "label": "雇员费率", "value": "0.08", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const w=num('w'),er=num('er'),ee=num('ee');
            const T=w*(er+ee);
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'工薪税 T (元)']
            ]));
        """,
        "notes": ["工薪税 = 工资×(雇主率+雇员率)。", "1 万×(0.2+0.08) → 2800 元。"],
    },
    {
        "slug": "capital-gains-effective",
        "industry": "tax",
        "cat": "tax",
        "icon": "trending-up",
        "bg": "from-blue-500 to-indigo-600",
        "title": "优惠资本利得税计算器",
        "h1": "T = 收益 × 优惠税率",
        "h2": "由资本收益与优惠税率求应缴税",
        "intro": "输入资本收益与适用优惠税率，求资本利得税。",
        "desc": "优惠资本利得税：输入 收益、税率，输出 T。",
        "inputs": [
            {"id": "g", "label": "资本收益", "value": "100000", "step": "5000", "unit": "元"},
            {"id": "r", "label": "优惠税率", "value": "0.1", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const g=num('g'),r=num('r');
            const T=g*r;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'资本利得税 T (元)']
            ]));
        """,
        "notes": ["长期持有常享优惠税率。", "10 万×10% → 1 万元。"],
    },
    {
        "slug": "gift-tax",
        "industry": "tax",
        "cat": "tax",
        "icon": "gift",
        "bg": "from-blue-500 to-indigo-600",
        "title": "赠与税计算器",
        "h1": "T = max(赠与额 − 免税额, 0) × 税率",
        "h2": "由赠与额、免税额与税率求赠与税",
        "intro": "输入赠与额、免税额与税率，求赠与税。",
        "desc": "赠与税：输入 赠与额、免税额、税率，输出 T。",
        "inputs": [
            {"id": "a", "label": "赠与额", "value": "1000000", "step": "50000", "unit": "元"},
            {"id": "e", "label": "免税额", "value": "200000", "step": "10000", "unit": "元"},
            {"id": "r", "label": "税率", "value": "0.2", "step": "0.02", "unit": ""},
        ],
        "calc": """
            const a=num('a'),e=num('e'),r=num('r');
            const T=Math.max(a-e,0)*r;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'赠与税 T (元)']
            ]));
        """,
        "notes": ["超出免税额部分计税。", "(100万−20万)×20% → 16 万。"],
    },
    {
        "slug": "tax-credit",
        "industry": "tax",
        "cat": "tax",
        "icon": "minus-circle",
        "bg": "from-blue-500 to-indigo-600",
        "title": "税收抵免后应纳税额计算器",
        "h1": "T' = 应纳税额 − 抵免额",
        "h2": "由应纳税额与税收抵免额求实缴税额",
        "intro": "输入应纳税额与可抵免金额，求抵免后实缴。",
        "desc": "税收抵免：输入 应纳税额、抵免额，输出 T'。",
        "inputs": [
            {"id": "t", "label": "应纳税额", "value": "5000", "step": "200", "unit": "元"},
            {"id": "c", "label": "抵免额", "value": "1000", "step": "100", "unit": "元"},
        ],
        "calc": """
            const t=num('t'),c=num('c');
            const Tp=Math.max(t-c,0);
            ToolBox.setResult('result', dataGrid([
                [Tp.toFixed(2),'抵免后税额 T′ (元)']
            ]));
        """,
        "notes": ["抵免直接减税额（非减所得）。", "5000−1000 → 4000 元。"],
    },
    {
        "slug": "foreign-tax-credit",
        "industry": "tax",
        "cat": "tax",
        "icon": "globe",
        "bg": "from-blue-500 to-indigo-600",
        "title": "境外税收抵免限额计算器",
        "h1": "抵扣额 = min(境外已纳税, 抵免限额)",
        "h2": "由境外已纳税与抵免限额求可抵扣额",
        "intro": "输入境外已纳税额与抵免限额，求可抵扣金额。",
        "desc": "境外税收抵免：输入 境外税、限额，输出 抵扣额。",
        "inputs": [
            {"id": "ft", "label": "境外已纳税", "value": "2000", "step": "100", "unit": "元"},
            {"id": "lim", "label": "抵免限额", "value": "1500", "step": "100", "unit": "元"},
        ],
        "calc": """
            const ft=num('ft'),lim=num('lim');
            const cr=Math.min(ft,lim);
            ToolBox.setResult('result', dataGrid([
                [cr.toFixed(2),'可抵扣额 (元)']
            ]));
        """,
        "notes": ["抵免不超过限额（分国/综合）。", "min(2000,1500) → 1500 元。"],
    },
    {
        "slug": "social-security-tax",
        "industry": "tax",
        "cat": "tax",
        "icon": "shield",
        "bg": "from-blue-500 to-indigo-600",
        "title": "社会保险费计算器",
        "h1": "T = 缴费基数 × 费率",
        "h2": "由缴费基数与社保费率求社保费",
        "intro": "输入缴费基数与社保综合费率，求社保费。",
        "desc": "社会保险费：输入 基数、费率，输出 T。",
        "inputs": [
            {"id": "b", "label": "缴费基数", "value": "10000", "step": "500", "unit": "元"},
            {"id": "r", "label": "费率", "value": "0.18", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const b=num('b'),r=num('r');
            const T=b*r;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'社保费 T (元)']
            ]));
        """,
        "notes": ["含养老/医疗/失业等综合费率。", "1 万×18% → 1800 元。"],
    },
    {
        "slug": "vat-output",
        "industry": "tax",
        "cat": "tax",
        "icon": "receipt",
        "bg": "from-blue-500 to-indigo-600",
        "title": "增值税销项税额计算器",
        "h1": "T = 销售额 × 税率",
        "h2": "由销售额与增值税率求销项税额",
        "intro": "输入销售额与增值税率，求销项税额。",
        "desc": "增值税销项：输入 销售额、税率，输出 T。",
        "inputs": [
            {"id": "s", "label": "销售额", "value": "10000", "step": "500", "unit": "元"},
            {"id": "r", "label": "增值税率", "value": "0.13", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const s=num('s'),r=num('r');
            const T=s*r;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'销项税额 T (元)']
            ]));
        """,
        "notes": ["销项税额 = 不含税销售额×税率。", "1 万×13% → 1300 元。"],
    },
    {
        "slug": "reverse-charge",
        "industry": "tax",
        "cat": "tax",
        "icon": "refresh-cw",
        "bg": "from-blue-500 to-indigo-600",
        "title": "代扣代缴税额计算器",
        "h1": "T = 金额 × 征收率",
        "h2": "由代扣金额与征收率求代扣代缴税额",
        "intro": "输入代扣金额与征收率，求代扣代缴税额。",
        "desc": "代扣代缴：输入 金额、征收率，输出 T。",
        "inputs": [
            {"id": "a", "label": "代扣金额", "value": "5000", "step": "200", "unit": "元"},
            {"id": "r", "label": "征收率", "value": "0.03", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const a=num('a'),r=num('r');
            const T=a*r;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(2),'代扣代缴 T (元)']
            ]));
        """,
        "notes": ["常用于代扣代缴小额劳务。", "5000×3% → 150 元。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
