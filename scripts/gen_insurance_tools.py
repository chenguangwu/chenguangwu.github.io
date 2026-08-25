# -*- coding: utf-8 -*-
"""Batch 36: 保险精算计算深化（14 个公式计算器）。industry=insurance。"""
from tool_template import main

TOOLS = [
    {
        "slug": "life-cover-need",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "shield",
        "bg": "from-rose-500 to-red-600",
        "title": "寿险保额需求计算器",
        "h1": "寿险保额需求",
        "h2": "收入替代法估算所需寿险保额",
        "intro": "按收入替代与负债估算家庭所需寿险保额。",
        "desc": "输入年收入、需保障年数、现有资产与负债，计算建议保额 = 年收入×年数 + 负债 − 资产。",
        "inputs": [
            {"id": "income", "label": "年收入", "value": "300000", "step": "10000", "unit": "元"},
            {"id": "years", "label": "保障年数", "value": "10", "step": "1", "unit": "年"},
            {"id": "debt", "label": "现有负债", "value": "1000000", "step": "50000", "unit": "元"},
            {"id": "asset", "label": "可动用资产", "value": "500000", "step": "50000", "unit": "元"},
        ],
        "calc": """
            const inc=num('income'),y=num('years'),d=num('debt'),a=num('asset');
            const cover=inc*y + d - a;
            ToolBox.setResult('result', dataGrid([
                [fmt(cover),'建议保额 (元)'],
                [fmt(inc*y),'收入替代部分 (元)'],
                [fmt(Math.max(cover,0)),'保额下限 (元)']
            ]));
        """,
        "notes": ["保额 = 年收入×保障年数 + 负债 − 资产。", "仅作粗略估算，实际需求应结合具体家庭结构。"],
    },
    {
        "slug": "mortality-prob",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "activity",
        "bg": "from-rose-500 to-red-600",
        "title": "死亡率与生存率换算",
        "h1": "死亡率 / 生存率换算",
        "h2": "由生存率推算死亡率",
        "intro": "已知年生存率 p，死亡率 q = 1 − p。",
        "desc": "输入年生存率（0–1），计算年死亡率、n 年生存概率及 n 年内死亡概率。",
        "inputs": [
            {"id": "p", "label": "年生存率 p", "value": "0.99", "step": "0.001", "unit": ""},
            {"id": "n", "label": "年数 n", "value": "10", "step": "1", "unit": "年"},
        ],
        "calc": """
            const p=num('p'),n=num('n');
            const q=1-p;
            const sp=Math.pow(p,n);
            ToolBox.setResult('result', dataGrid([
                [(q*100).toFixed(3),'年死亡率 q (%)'],
                [(sp*100).toFixed(3),'n 年生存概率 (%)'],
                [((1-sp)*100).toFixed(3),'n 年内死亡概率 (%)']
            ]));
        """,
        "notes": ["q = 1 − p。", "n 年生存概率 = p^n。"],
    },
    {
        "slug": "net-single-premium",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "credit-card",
        "bg": "from-rose-500 to-red-600",
        "title": "净趸缴保费计算器",
        "h1": "净趸缴保费 (NSP)",
        "h2": "一次性缴清的纯保费",
        "intro": "在给定死亡率与利率下，死亡给付的现值即净趸缴保费。",
        "desc": "输入保额、年死亡率、利率与保障年数，用 NSP = Σ B·v^(t+1)·t_p_x·q 近似（简化为等额死亡率）计算。",
        "inputs": [
            {"id": "B", "label": "保额", "value": "1000000", "step": "50000", "unit": "元"},
            {"id": "q", "label": "年死亡率 q", "value": "0.01", "step": "0.001", "unit": ""},
            {"id": "i", "label": "年利率 i", "value": "0.03", "step": "0.005", "unit": ""},
            {"id": "n", "label": "保障年数", "value": "10", "step": "1", "unit": "年"},
        ],
        "calc": """
            const B=num('B'),q=num('q'),i=num('i'),n=num('n');
            const v=1/(1+i);
            let nsp=0, sp=1;
            for(let t=1;t<=n;t++){ const prob=sp*q; nsp += B*Math.pow(v,t)*prob; sp*=(1-q); }
            ToolBox.setResult('result', dataGrid([
                [fmt(nsp),'净趸缴保费 (元)'],
                [fmt(nsp/B*100),'占保额比例 (%)']
            ]));
        """,
        "notes": ["NSP 为未来死亡给付按利率贴现的期望值。", "简化假设各年死亡率相同。"],
    },
    {
        "slug": "level-premium-life",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "repeat",
        "bg": "from-rose-500 to-red-600",
        "title": "均衡年保费计算器",
        "h1": "均衡年保费",
        "h2": "将趸缴保费分摊为每年缴费",
        "intro": "均衡年保费 = 净趸缴保费 ÷ 年金现值系数。",
        "desc": "输入趸缴保费、年利率与缴费年数，按 a_n| = (1−v^n)/i 计算年缴保费。",
        "inputs": [
            {"id": "nsp", "label": "净趸缴保费", "value": "85000", "step": "1000", "unit": "元"},
            {"id": "i", "label": "年利率 i", "value": "0.03", "step": "0.005", "unit": ""},
            {"id": "n", "label": "缴费年数", "value": "20", "step": "1", "unit": "年"},
        ],
        "calc": """
            const nsp=num('nsp'),i=num('i'),n=num('n');
            const v=1/(1+i);
            const a=(1-Math.pow(v,n))/i;
            const P=nsp/a;
            ToolBox.setResult('result', dataGrid([
                [fmt(P),'均衡年保费 (元)'],
                [fmt(a),'年金现值系数 a_n|'],
                [fmt(P*n),'总缴费 (元)']
            ]));
        """,
        "notes": ["a_n| = (1 − v^n) / i。", "年保费随利率上升而下降。"],
    },
    {
        "slug": "endowment-premium",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "gift",
        "bg": "from-rose-500 to-red-600",
        "title": "两全保险保费计算器",
        "h1": "两全保险保费",
        "h2": "身故与满期给付组合",
        "intro": "两全保险 = 定期寿险 + 满期生存给付的现值。",
        "desc": "输入保额、年死亡率、利率、年数，计算含满期返还的均衡年保费。",
        "inputs": [
            {"id": "B", "label": "保额", "value": "1000000", "step": "50000", "unit": "元"},
            {"id": "q", "label": "年死亡率 q", "value": "0.01", "step": "0.001", "unit": ""},
            {"id": "i", "label": "年利率 i", "value": "0.03", "step": "0.005", "unit": ""},
            {"id": "n", "label": "保险年数", "value": "20", "step": "1", "unit": "年"},
        ],
        "calc": """
            const B=num('B'),q=num('q'),i=num('i'),n=num('n');
            const v=1/(1+i);
            let death=0, sp=1;
            for(let t=1;t<=n;t++){ death += B*Math.pow(v,t)*sp*q; sp*=(1-q); }
            const survival=B*Math.pow(v,n)*sp;
            const a=(1-Math.pow(v,n))/i;
            const P=(death+survival)/a;
            ToolBox.setResult('result', dataGrid([
                [fmt(P),'两全年保费 (元)'],
                [fmt(death),'身故给付现值 (元)'],
                [fmt(survival),'满期给付现值 (元)']
            ]));
        """,
        "notes": ["两全 = 死亡给付现值 + 生存给付现值。", "均衡保费再除以年金现值系数。"],
    },
    {
        "slug": "surrender-value",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "wallet",
        "bg": "from-rose-500 to-red-600",
        "title": "保单现金价值估算",
        "h1": "现金价值估算",
        "h2": "退保可领取金额",
        "intro": "现金价值 ≈ 已缴保费终值 − 退保手续费。",
        "desc": "输入年保费、已缴年数、年利率与退保费率，估算退保现金价值。",
        "inputs": [
            {"id": "P", "label": "年保费", "value": "5000", "step": "500", "unit": "元"},
            {"id": "y", "label": "已缴年数", "value": "5", "step": "1", "unit": "年"},
            {"id": "i", "label": "年利率 i", "value": "0.03", "step": "0.005", "unit": ""},
            {"id": "fee", "label": "退保费率", "value": "0.1", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const P=num('P'),y=num('y'),i=num('i'),fee=num('fee');
            const fv=P*((Math.pow(1+i,y)-1)/i);
            const cv=fv*(1-fee);
            ToolBox.setResult('result', dataGrid([
                [fmt(cv),'现金价值 (元)'],
                [fmt(fv),'已缴保费终值 (元)'],
                [fmt(fv*fee),'退保手续费 (元)']
            ]));
        """,
        "notes": ["近似按保费年金终值扣除退保费用。", "实际现金价值以保单现金价值表为准。"],
    },
    {
        "slug": "claim-frequency",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "hash",
        "bg": "from-rose-500 to-red-600",
        "title": "理赔频率计算器",
        "h1": "理赔频率",
        "h2": "每单位风险暴露的理赔次数",
        "intro": "理赔频率 = 理赔件数 ÷ 风险暴露单位。",
        "desc": "输入理赔件数与风险暴露（车年/人年等），计算理赔频率。",
        "inputs": [
            {"id": "claims", "label": "理赔件数", "value": "120", "step": "1", "unit": "件"},
            {"id": "exposure", "label": "风险暴露", "value": "1000", "step": "10", "unit": "车年"},
        ],
        "calc": """
            const c=num('claims'),e=num('exposure');
            const f=c/e;
            ToolBox.setResult('result', dataGrid([
                [f.toFixed(4),'理赔频率 (次/暴露单位)'],
                [(f*100).toFixed(2),'出险率 (%)']
            ]));
        """,
        "notes": ["频率 = 理赔件数 / 暴露单位。", "常用于车险定价基础。"],
    },
    {
        "slug": "pure-premium",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "calculator",
        "bg": "from-rose-500 to-red-600",
        "title": "纯保费计算器",
        "h1": "纯保费 (风险保费)",
        "h2": "期望损失 = 频率 × 严重度",
        "intro": "纯保费 = 理赔频率 × 平均赔付额。",
        "desc": "输入理赔频率与平均赔付金额，计算每风险单位的纯保费。",
        "inputs": [
            {"id": "freq", "label": "理赔频率", "value": "0.12", "step": "0.01", "unit": "次/单位"},
            {"id": "sev", "label": "平均赔付额", "value": "30000", "step": "1000", "unit": "元"},
        ],
        "calc": """
            const f=num('freq'),s=num('sev');
            const pp=f*s;
            ToolBox.setResult('result', dataGrid([
                [fmt(pp),'纯保费 (元/单位)'],
                [fmt(pp*1.1),'含10%安全边际 (元)']
            ]));
        """,
        "notes": ["纯保费 = 频率 × 严重度。", "实际保费还需加费用与利润附加。"],
    },
    {
        "slug": "loss-ratio",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "trending-down",
        "bg": "from-rose-500 to-red-600",
        "title": "赔付率计算器",
        "h1": "赔付率",
        "h2": "已决赔款与保费之比",
        "intro": "赔付率 = 赔款支出 ÷ 保费收入。",
        "desc": "输入赔款与保费收入，计算赔付率。",
        "inputs": [
            {"id": "claims", "label": "赔款支出", "value": "6500000", "step": "100000", "unit": "元"},
            {"id": "premium", "label": "保费收入", "value": "10000000", "step": "100000", "unit": "元"},
        ],
        "calc": """
            const c=num('claims'),p=num('premium');
            const lr=c/p*100;
            ToolBox.setResult('result', dataGrid([
                [lr.toFixed(2),'赔付率 (%)'],
                [(100-lr).toFixed(2),'承保边际 (%)']
            ]));
        """,
        "notes": ["赔付率越低盈利空间越大。", "综合成本率还需计入费用率。"],
    },
    {
        "slug": "expense-ratio",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "receipt",
        "bg": "from-rose-500 to-red-600",
        "title": "费用率计算器",
        "h1": "费用率",
        "h2": "营运费用与保费之比",
        "intro": "费用率 = 营运费用 ÷ 保费收入。",
        "desc": "输入费用与保费收入，计算费用率。",
        "inputs": [
            {"id": "exp", "label": "营运费用", "value": "2500000", "step": "100000", "unit": "元"},
            {"id": "premium", "label": "保费收入", "value": "10000000", "step": "100000", "unit": "元"},
        ],
        "calc": """
            const e=num('exp'),p=num('premium');
            ToolBox.setResult('result', dataGrid([
                [(e/p*100).toFixed(2),'费用率 (%)']
            ]));
        """,
        "notes": ["费用率 = 费用 / 保费。", "与赔付率相加得综合成本率。"],
    },
    {
        "slug": "combined-ratio",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "scale",
        "bg": "from-rose-500 to-red-600",
        "title": "综合成本率计算器",
        "h1": "综合成本率",
        "h2": "承保盈亏的核心指标",
        "intro": "综合成本率 = 赔付率 + 费用率。",
        "desc": "输入赔款、费用与保费，计算综合成本率（<100% 承保盈利）。",
        "inputs": [
            {"id": "claims", "label": "赔款支出", "value": "6500000", "step": "100000", "unit": "元"},
            {"id": "exp", "label": "营运费用", "value": "2500000", "step": "100000", "unit": "元"},
            {"id": "premium", "label": "保费收入", "value": "10000000", "step": "100000", "unit": "元"},
        ],
        "calc": """
            const c=num('claims'),e=num('exp'),p=num('premium');
            const cr=(c+e)/p*100;
            ToolBox.setResult('result', dataGrid([
                [cr.toFixed(2),'综合成本率 (%)'],
                [(cr<100?'承保盈利':'承保亏损'),'承保结论'],
                [(100-cr).toFixed(2),'承保利润率 (%)']
            ]));
        """,
        "notes": ["综合成本率 < 100% 表示承保盈利。", "含投资收益后总体仍可能盈利。"],
    },
    {
        "slug": "ibnr-reserve",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "archive",
        "bg": "from-rose-500 to-red-600",
        "title": "IBNR 准备金估算",
        "h1": "IBNR 准备金",
        "h2": "已发生未报案赔款",
        "intro": "IBNR 常用已报案赔款乘以发展因子推算。",
        "desc": "输入已报案赔款与发展因子（>1），估算 IBNR 与总准备金。",
        "inputs": [
            {"id": "reported", "label": "已报案赔款", "value": "4000000", "step": "100000", "unit": "元"},
            {"id": "factor", "label": "发展因子", "value": "1.25", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const r=num('reported'),f=num('factor');
            const ibnr=r*(f-1);
            ToolBox.setResult('result', dataGrid([
                [fmt(ibnr),'IBNR 准备金 (元)'],
                [fmt(r*f),'最终赔款估计 (元)']
            ]));
        """,
        "notes": ["IBNR ≈ 已报案 × (发展因子 − 1)。", "发展因子由历史赔付进展经验确定。"],
    },
    {
        "slug": "uw-profit",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "line-chart",
        "bg": "from-rose-500 to-red-600",
        "title": "承保利润计算器",
        "h1": "承保利润",
        "h2": "保费减赔款减费用",
        "intro": "承保利润 = 保费 − 赔款 − 费用。",
        "desc": "输入保费、赔款与费用，计算承保利润与利润率。",
        "inputs": [
            {"id": "premium", "label": "保费收入", "value": "10000000", "step": "100000", "unit": "元"},
            {"id": "claims", "label": "赔款支出", "value": "6500000", "step": "100000", "unit": "元"},
            {"id": "exp", "label": "营运费用", "value": "2500000", "step": "100000", "unit": "元"},
        ],
        "calc": """
            const p=num('premium'),c=num('claims'),e=num('exp');
            const profit=p-c-e;
            ToolBox.setResult('result', dataGrid([
                [fmt(profit),'承保利润 (元)'],
                [(profit/p*100).toFixed(2),'承保利润率 (%)']
            ]));
        """,
        "notes": ["承保利润 = 保费 − 赔款 − 费用。", "与综合成本率互补验证。"],
    },
    {
        "slug": "annuity-certain-pv",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "calendar-clock",
        "bg": "from-rose-500 to-red-600",
        "title": "确定年金现值计算器",
        "h1": "确定年金现值",
        "h2": "保险年金定价基础",
        "intro": "确定年金现值 a_n| = (1 − v^n) / i。",
        "desc": "输入年金额、年利率与年数，计算期初/期末付年金现值。",
        "inputs": [
            {"id": "P", "label": "年金额", "value": "12000", "step": "1000", "unit": "元"},
            {"id": "i", "label": "年利率 i", "value": "0.03", "step": "0.005", "unit": ""},
            {"id": "n", "label": "年数", "value": "15", "step": "1", "unit": "年"},
        ],
        "calc": """
            const P=num('P'),i=num('i'),n=num('n');
            const v=1/(1+i);
            const aEnd=(1-Math.pow(v,n))/i;
            const aBeg=aEnd*(1+i);
            ToolBox.setResult('result', dataGrid([
                [fmt(P*aEnd),'期末付现值 (元)'],
                [fmt(P*aBeg),'期初付现值 (元)'],
                [fmt(aEnd),'年金现值系数 a_n|']
            ]));
        """,
        "notes": ["期末付 a_n| = (1 − v^n) / i。", "期初付 = 期末付 × (1+i)。"],
    },
]

FMT_DEF = "function fmt(v){const neg=v<0?'-':'';v=Math.abs(v);let s=v.toFixed(2);let p=s.split('.');p[0]=p[0].replace(/\\B(?=(\\d{3})+(?!\\d))/g,',');return neg+p.join('.');}"

for _t in TOOLS:
    if "fmt(" in _t["calc"]:
        _t["calc"] = FMT_DEF + "\n            " + _t["calc"].lstrip()

if __name__ == "__main__":
    main(TOOLS)
