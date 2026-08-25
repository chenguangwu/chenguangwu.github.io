# -*- coding: utf-8 -*-
"""Batch 31: 银行学计算深化（14 个公式计算器）。industry=banking（新干净目录）。"""
from tool_template import main

TOOLS = [
    {
        "slug": "simple-interest", "industry": "banking", "cat": "banking", "icon": "🏦", "bg": "#eff6ff",
        "title": "单利利息", "h1": "单利利息计算器",
        "h2": "I = P × r × t",
        "intro": "本金按固定利率、不滚利的单利利息。",
        "desc": "单利利息计算器：输入本金、年利率与年限求利息。",
        "inputs": [
            {"id": "p", "label": "本金 P", "value": "10000", "step": "100"},
            {"id": "r", "label": "年利率 r (%)", "value": "5", "step": "0.1"},
            {"id": "t", "label": "年限 t", "value": "3", "step": "0.5"},
        ],
        "calc": """
            const P = num('p'), r = num('r'), t = num('t');
            const I = P * r / 100 * t;
            ToolBox.setResult('result', dataGrid([
                [I.toFixed(2), '单利利息 I'],
                [(P + I).toFixed(2), '到期本利和']
            ]));
        """,
        "notes": ["10000、5%、3 年 → 利息 1500。", "单利不滚利。"],
    },
    {
        "slug": "effective-annual-rate", "industry": "banking", "cat": "banking", "icon": "📐", "bg": "#eff6ff",
        "title": "有效年利率 (EAR)", "h1": "有效年利率计算器",
        "h2": "EAR = (1 + r/n)^n − 1",
        "intro": "名义年利率按复利次数折算的真实年化收益率。",
        "desc": "有效年利率计算器：输入名义利率与复利次数求 EAR。",
        "inputs": [
            {"id": "r", "label": "名义年利率 r (%)", "value": "6", "step": "0.1"},
            {"id": "n", "label": "每年复利次数 n", "value": "12", "step": "1"},
        ],
        "calc": """
            const r = num('r') / 100, n = num('n');
            const ear = Math.pow(1 + r / n, n) - 1;
            ToolBox.setResult('result', dataGrid([
                [(ear * 100).toFixed(3), '有效年利率 EAR (%)'],
                [ear.toFixed(5), 'EAR (小数)']
            ]));
        """,
        "notes": ["6% 名义、月复利 → EAR≈6.168%。", "n 越大 EAR 越接近连续复利。"],
    },
    {
        "slug": "continuous-compounding", "industry": "banking", "cat": "banking", "icon": "♾️", "bg": "#eff6ff",
        "title": "连续复利终值", "h1": "连续复利终值计算器",
        "h2": "A = P·e^(rt)",
        "intro": "复利次数趋于无穷时的终值。",
        "desc": "连续复利计算器：输入本金、年利率与年限求终值。",
        "inputs": [
            {"id": "p", "label": "本金 P", "value": "10000", "step": "100"},
            {"id": "r", "label": "年利率 r (%)", "value": "5", "step": "0.1"},
            {"id": "t", "label": "年限 t", "value": "10", "step": "1"},
        ],
        "calc": """
            const P = num('p'), r = num('r') / 100, t = num('t');
            const A = P * Math.exp(r * t);
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(2), '连续复利终值 A'],
                [(A - P).toFixed(2), '利息总额']
            ]));
        """,
        "notes": ["10000、5%、10 年 → 约 16487.21。", "e 为自然常数。"],
    },
    {
        "slug": "emi-loan", "industry": "banking", "cat": "banking", "icon": "💳", "bg": "#eff6ff",
        "title": "等额本息月供 (EMI)", "h1": "贷款月供计算器",
        "h2": "EMI = P·i·(1+i)^N / [(1+i)^N − 1]",
        "intro": "按月等额本息还款的每月还款额。",
        "desc": "贷款月供计算器：输入贷款额、年利率与年限求月供。",
        "inputs": [
            {"id": "p", "label": "贷款本金 P", "value": "500000", "step": "1000"},
            {"id": "r", "label": "年利率 r (%)", "value": "4.9", "step": "0.1"},
            {"id": "y", "label": "年限 y", "value": "30", "step": "1"},
        ],
        "calc": """
            const P = num('p'), r = num('r') / 100 / 12, N = num('y') * 12;
            const emi = P * r * Math.pow(1 + r, N) / (Math.pow(1 + r, N) - 1);
            ToolBox.setResult('result', dataGrid([
                [emi.toFixed(2), '月供 EMI'],
                [(emi * N).toFixed(2), '还款总额']
            ]));
        """,
        "notes": ["50 万、4.9%、30 年 → 月供约 2653.63。", "r 为月利率。"],
    },
    {
        "slug": "loan-total-interest", "industry": "banking", "cat": "banking", "icon": "🧮", "bg": "#eff6ff",
        "title": "贷款总利息", "h1": "贷款总利息计算器",
        "h2": "总利息 = EMI×N − P",
        "intro": "等额本息下整个贷款周期支付的利息总额。",
        "desc": "贷款总利息计算器：输入贷款额、年利率与年限求总利息。",
        "inputs": [
            {"id": "p", "label": "贷款本金 P", "value": "500000", "step": "1000"},
            {"id": "r", "label": "年利率 r (%)", "value": "4.9", "step": "0.1"},
            {"id": "y", "label": "年限 y", "value": "30", "step": "1"},
        ],
        "calc": """
            const P = num('p'), r = num('r') / 100 / 12, N = num('y') * 12;
            const emi = P * r * Math.pow(1 + r, N) / (Math.pow(1 + r, N) - 1);
            const total = emi * N - P;
            ToolBox.setResult('result', dataGrid([
                [total.toFixed(2), '贷款总利息'],
                [emi.toFixed(2), '月供 EMI']
            ]));
        """,
        "notes": ["50 万、4.9%、30 年 → 总利息约 455307。", "总利息 = 还款总额 − 本金。"],
    },
    {
        "slug": "loan-remaining-balance", "industry": "banking", "cat": "banking", "icon": "📊", "bg": "#eff6ff",
        "title": "贷款剩余本金", "h1": "贷款剩余本金计算器",
        "h2": "B = P(1+i)^k − EMI·[(1+i)^k − 1]/i",
        "intro": "已还 k 期后尚未偿还的本金余额。",
        "desc": "贷款剩余本金计算器：输入贷款参数与已还期数求余额。",
        "inputs": [
            {"id": "p", "label": "贷款本金 P", "value": "500000", "step": "1000"},
            {"id": "r", "label": "年利率 r (%)", "value": "4.9", "step": "0.1"},
            {"id": "y", "label": "年限 y", "value": "30", "step": "1"},
            {"id": "k", "label": "已还期数 k", "value": "60", "step": "1"},
        ],
        "calc": """
            const P = num('p'), r = num('r') / 100 / 12, N = num('y') * 12, k = num('k');
            const emi = P * r * Math.pow(1 + r, N) / (Math.pow(1 + r, N) - 1);
            const B = P * Math.pow(1 + r, k) - emi * (Math.pow(1 + r, k) - 1) / r;
            ToolBox.setResult('result', dataGrid([
                [B.toFixed(2), '剩余本金 B'],
                [(P - B).toFixed(2), '已还本金']
            ]));
        """,
        "notes": ["50 万、4.9%、30 年、已还 60 期 → 余额约 45.1 万。", "k 不能超过总期数 N。"],
    },
    {
        "slug": "fd-quarterly", "industry": "banking", "cat": "banking", "icon": "🏧", "bg": "#eff6ff",
        "title": "定期存款（按季复利）", "h1": "定期存款到期计算器",
        "h2": "A = P(1 + r/4)^(4t)",
        "intro": "按季度复利计息的定期存款到期金额。",
        "desc": "定期存款计算器：输入本金、年利率与年限求到期金额。",
        "inputs": [
            {"id": "p", "label": "本金 P", "value": "100000", "step": "1000"},
            {"id": "r", "label": "年利率 r (%)", "value": "3", "step": "0.1"},
            {"id": "t", "label": "年限 t", "value": "5", "step": "1"},
        ],
        "calc": """
            const P = num('p'), r = num('r'), t = num('t');
            const A = P * Math.pow(1 + r / 4 / 100, 4 * t);
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(2), '到期金额 A'],
                [(A - P).toFixed(2), '利息总额']
            ]));
        """,
        "notes": ["10 万、3%、5 年（季复利）→ 约 116075。", "季度复利利滚利。"],
    },
    {
        "slug": "rd-maturity", "industry": "banking", "cat": "banking", "icon": "📆", "bg": "#eff6ff",
        "title": "零存整取（按月存、季复利）", "h1": "零存整取到期计算器",
        "h2": "M = P·[(1+i)^n − 1] / [1 − (1+i)^(−1/3)]",
        "intro": "每月固定存入、按季复利的零存整取到期金额。",
        "desc": "零存整取计算器：输入月存金额、年利率与年限求到期金额。",
        "inputs": [
            {"id": "p", "label": "每月存入 P", "value": "1000", "step": "100"},
            {"id": "r", "label": "年利率 r (%)", "value": "8", "step": "0.1"},
            {"id": "t", "label": "年限 t", "value": "1", "step": "1"},
        ],
        "calc": """
            const P = num('p'), i = num('r') / 4 / 100, n = num('t') * 4;
            const M = P * (Math.pow(1 + i, n) - 1) / (1 - Math.pow(1 + i, -1 / 3));
            ToolBox.setResult('result', dataGrid([
                [M.toFixed(2), '到期金额 M'],
                [(M - P * n * 3).toFixed(2), '利息总额']
            ]));
        """,
        "notes": ["月存 1000、8%、1 年 → 到期约 12531。", "分母含 (1+i)^(−1/3)。"],
    },
    {
        "slug": "savings-goal-monthly", "industry": "banking", "cat": "banking", "icon": "🎯", "bg": "#eff6ff",
        "title": "储蓄目标月存额", "h1": "储蓄目标月存额计算器",
        "h2": "PMT = FV·i / [(1+i)^N − 1]",
        "intro": "为在 N 期后达成目标金额，每期需存入的数额。",
        "desc": "储蓄目标计算器：输入目标金额、年利率与年限求每月应存。",
        "inputs": [
            {"id": "fv", "label": "目标金额 FV", "value": "200000", "step": "1000"},
            {"id": "r", "label": "年利率 r (%)", "value": "4", "step": "0.1"},
            {"id": "y", "label": "年限 y", "value": "10", "step": "1"},
        ],
        "calc": """
            const fv = num('fv'), i = num('r') / 100 / 12, N = num('y') * 12;
            const pmt = fv * i / (Math.pow(1 + i, N) - 1);
            ToolBox.setResult('result', dataGrid([
                [pmt.toFixed(2), '每月应存 PMT'],
                [(pmt * N).toFixed(2), '累计存入']
            ]));
        """,
        "notes": ["目标 20 万、4%、10 年 → 月存约 1361.37。", "i 为月利率。"],
    },
    {
        "slug": "discount-lump", "industry": "banking", "cat": "banking", "icon": "💵", "bg": "#eff6ff",
        "title": "未来金额折现", "h1": "未来金额折现计算器",
        "h2": "PV = FV / (1 + r)^t",
        "intro": "把未来某笔存款按贴现率折算为今天价值。",
        "desc": "折现计算器：输入未来金额、贴现率与年限求现值。",
        "inputs": [
            {"id": "fv", "label": "未来金额 FV", "value": "150000", "step": "1000"},
            {"id": "r", "label": "贴现率 r (%)", "value": "4", "step": "0.1"},
            {"id": "t", "label": "年限 t", "value": "10", "step": "1"},
        ],
        "calc": """
            const fv = num('fv'), r = num('r') / 100, t = num('t');
            const pv = fv / Math.pow(1 + r, t);
            ToolBox.setResult('result', dataGrid([
                [pv.toFixed(2), '现值 PV'],
                [(fv - pv).toFixed(2), '贴现额']
            ]));
        """,
        "notes": ["15 万、4%、10 年 → 现值约 101270。", "贴现率越高现值越低。"],
    },
    {
        "slug": "fisher-real-rate", "industry": "banking", "cat": "banking", "icon": "⚖️", "bg": "#eff6ff",
        "title": "费雪实际利率", "h1": "费雪实际利率计算器",
        "h2": "1 + r_real = (1 + r_nom) / (1 + π)",
        "intro": "用精确费雪方程由名义利率与通胀率求实际利率。",
        "desc": "实际利率计算器：输入名义利率与通胀率求实际利率。",
        "inputs": [
            {"id": "nom", "label": "名义利率 (%)", "value": "6", "step": "0.1"},
            {"id": "infl", "label": "通胀率 (%)", "value": "2", "step": "0.1"},
        ],
        "calc": """
            const nom = num('nom') / 100, infl = num('infl') / 100;
            const real = (1 + nom) / (1 + infl) - 1;
            ToolBox.setResult('result', dataGrid([
                [(real * 100).toFixed(3), '实际利率 (%)'],
                [((nom - infl) * 100).toFixed(3), '近似 (名义−通胀)']
            ]));
        """,
        "notes": ["名义 6%、通胀 2% → 实际约 3.922%。", "近似法为 nom−infl。"],
    },
    {
        "slug": "amortization-first-interest", "industry": "banking", "cat": "banking", "icon": "🔢", "bg": "#eff6ff",
        "title": "首月利息", "h1": "贷款首月利息计算器",
        "h2": "I₁ = P × (r/12)",
        "intro": "等额本息首期还款中的利息部分。",
        "desc": "首月利息计算器：输入贷款本金与年利率求首月利息。",
        "inputs": [
            {"id": "p", "label": "贷款本金 P", "value": "500000", "step": "1000"},
            {"id": "r", "label": "年利率 r (%)", "value": "4.9", "step": "0.1"},
        ],
        "calc": """
            const P = num('p'), r = num('r') / 100 / 12;
            const I1 = P * r;
            ToolBox.setResult('result', dataGrid([
                [I1.toFixed(2), '首月利息 I₁'],
                [(P - I1).toFixed(2), '首月还本金']
            ]));
        """,
        "notes": ["50 万、4.9% → 首月利息约 2041.67。", "等额本息前期利息占比高。"],
    },
    {
        "slug": "daily-interest", "industry": "banking", "cat": "banking", "icon": "📅", "bg": "#eff6ff",
        "title": "按日计息", "h1": "按日计息计算器",
        "h2": "I = P × r × 天数 / 365",
        "intro": "按实际天数、年利率计算的短期利息。",
        "desc": "按日计息计算器：输入本金、年利率与天数求利息。",
        "inputs": [
            {"id": "p", "label": "本金 P", "value": "100000", "step": "1000"},
            {"id": "r", "label": "年利率 r (%)", "value": "3.65", "step": "0.05"},
            {"id": "d", "label": "天数 d", "value": "100", "step": "1"},
        ],
        "calc": """
            const P = num('p'), r = num('r'), d = num('d');
            const I = P * r / 100 * d / 365;
            ToolBox.setResult('result', dataGrid([
                [I.toFixed(2), '按日利息 I'],
                [(P + I).toFixed(2), '本利和']
            ]));
        """,
        "notes": ["10 万、3.65%、100 天 → 利息约 1000。", "日利率 ≈ 年化/365。"],
    },
    {
        "slug": "break-even-savings", "industry": "banking", "cat": "banking", "icon": "⚖️", "bg": "#eff6ff",
        "title": "存贷利差平衡点", "h1": "存贷利差平衡点计算器",
        "h2": "存 X、贷 (1−X) 时净息为 0",
        "intro": "在存款利率 r_d、贷款利率 r_l 下，使整体净息差为零的存款占比。",
        "desc": "存贷平衡点计算器：输入存贷款利率求净息为零的存款占比。",
        "inputs": [
            {"id": "rd", "label": "存款利率 r_d (%)", "value": "2", "step": "0.1"},
            {"id": "rl", "label": "贷款利率 r_l (%)", "value": "5", "step": "0.1"},
        ],
        "calc": """
            const rd = num('rd'), rl = num('rl');
            const x = rl / (rd + rl);
            ToolBox.setResult('result', dataGrid([
                [(x * 100).toFixed(2), '存款占比 X (%)'],
                [((1 - x) * 100).toFixed(2), '贷款占比 (1−X) (%)']
            ]));
        """,
        "notes": ["存 2%、贷 5% → 存款占比 71.43% 时净息为 0。", "假设资产=负债规模相等。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
