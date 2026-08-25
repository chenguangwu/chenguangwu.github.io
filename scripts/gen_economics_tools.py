# -*- coding: utf-8 -*-
"""Batch 30: 经济学计算深化（14 个公式计算器）。industry=economics（新干净目录）。"""
from tool_template import main

TOOLS = [
    {
        "slug": "inflation-rate", "industry": "economics", "cat": "economics", "icon": "📈", "bg": "#fff7ed",
        "title": "通货膨胀率（CPI）", "h1": "通货膨胀率计算器",
        "h2": "π = (CPI₁ − CPI₀) / CPI₀ × 100%",
        "intro": "基于消费者价格指数的时期通货膨胀率。",
        "desc": "通货膨胀率计算器：输入基期与报告期 CPI 求通胀率。",
        "inputs": [
            {"id": "cpi0", "label": "基期 CPI", "value": "100", "step": "0.1"},
            {"id": "cpi1", "label": "报告期 CPI", "value": "105", "step": "0.1"},
        ],
        "calc": """
            const c0 = num('cpi0'), c1 = num('cpi1');
            const p = (c1 - c0) / c0 * 100;
            ToolBox.setResult('result', dataGrid([
                [p.toFixed(2), '通货膨胀率 (%)'],
                [((c1 - c0)).toFixed(2), 'CPI 变化']
            ]));
        """,
        "notes": ["CPI 100→105 对应通胀 5%。", "分母为基期 CPI。"],
    },
    {
        "slug": "real-gdp", "industry": "economics", "cat": "economics", "icon": "🏦", "bg": "#fff7ed",
        "title": "实际 GDP", "h1": "实际 GDP 计算器",
        "h2": "实际 GDP = 名义 GDP / (1 + 平减指数%)",
        "intro": "用 GDP 平减指数剔除价格变化，得到实际产出。",
        "desc": "实际 GDP 计算器：输入名义 GDP 与平减指数求实际 GDP。",
        "inputs": [
            {"id": "nominal", "label": "名义 GDP", "value": "1100", "step": "1"},
            {"id": "defl", "label": "GDP 平减指数 (%)", "value": "10", "step": "0.1"},
        ],
        "calc": """
            const nom = num('nominal'), d = num('defl');
            const real = nom / (1 + d / 100);
            ToolBox.setResult('result', dataGrid([
                [real.toFixed(2), '实际 GDP'],
                [(nom - real).toFixed(2), '价格扭曲部分']
            ]));
        """,
        "notes": ["实际 GDP 剔除了通胀影响。", "平减指数 10% 时 1100→1000。"],
    },
    {
        "slug": "cagr", "industry": "economics", "cat": "economics", "icon": "📊", "bg": "#fff7ed",
        "title": "复合年均增长率", "h1": "CAGR 计算器",
        "h2": "CAGR = (终值 / 初值)^(1/n) − 1",
        "intro": "多期复合年均增长率。",
        "desc": "复合年均增长率计算器：输入初值、终值与年数求 CAGR。",
        "inputs": [
            {"id": "start", "label": "初值", "value": "100", "step": "1"},
            {"id": "end", "label": "终值", "value": "200", "step": "1"},
            {"id": "years", "label": "年数 n", "value": "7", "step": "0.5"},
        ],
        "calc": """
            const s = num('start'), e = num('end'), n = num('years');
            const g = Math.pow(e / s, 1 / n) - 1;
            ToolBox.setResult('result', dataGrid([
                [(g * 100).toFixed(2), 'CAGR (%)'],
                [g.toFixed(4), '增长率 (小数)']
            ]));
        """,
        "notes": ["100→200 经 7 年，CAGR ≈ 10.41%。", "几何平均而非算术平均。"],
    },
    {
        "slug": "rule-of-72", "industry": "economics", "cat": "economics", "icon": "⏱️", "bg": "#fff7ed",
        "title": "72 法则（翻倍时间）", "h1": "72 法则计算器",
        "h2": "t ≈ 72 / r",
        "intro": "估算投资翻倍所需年数的经验法则。",
        "desc": "72 法则计算器：输入年增长率求翻倍时间。",
        "inputs": [
            {"id": "rate", "label": "年增长率 r (%)", "value": "6", "step": "0.1"},
        ],
        "calc": """
            const r = num('rate');
            const t = 72 / r;
            const exact = Math.log(2) / Math.log(1 + r / 100);
            ToolBox.setResult('result', dataGrid([
                [t.toFixed(2), '72 法则估计 (年)'],
                [exact.toFixed(2), '精确翻倍 (年)']
            ]));
        """,
        "notes": ["r=6% → 约 12 年翻倍。", "利率越高估计越偏，精确值用 ln2/ln(1+r)。"],
    },
    {
        "slug": "compound-amount", "industry": "economics", "cat": "economics", "icon": "💰", "bg": "#fff7ed",
        "title": "复利终值", "h1": "复利终值计算器",
        "h2": "F = P(1 + r/n)^(nt)",
        "intro": "本金按年利率 r、每年 n 次复利、t 年后的终值。",
        "desc": "复利终值计算器：输入本金、利率、年期与复利次数求终值。",
        "inputs": [
            {"id": "p", "label": "本金 P", "value": "10000", "step": "100"},
            {"id": "r", "label": "年利率 r (%)", "value": "5", "step": "0.1"},
            {"id": "t", "label": "年数 t", "value": "10", "step": "1"},
            {"id": "n", "label": "每年复利次数 n", "value": "1", "step": "1"},
        ],
        "calc": """
            const P = num('p'), r = num('r'), t = num('t'), n = num('n');
            const f = P * Math.pow(1 + r / 100 / n, n * t);
            ToolBox.setResult('result', dataGrid([
                [f.toFixed(2), '复利终值 F'],
                [(f - P).toFixed(2), '利息总额']
            ]));
        """,
        "notes": ["10000 元、5%、10 年、年复利 → 16288.95。", "n=12 为月复利。"],
    },
    {
        "slug": "present-value", "industry": "economics", "cat": "economics", "icon": "💵", "bg": "#fff7ed",
        "title": "现值（折现）", "h1": "现值计算器",
        "h2": "PV = FV / (1 + r)^t",
        "intro": "未来一笔现金流按贴现率折算为今天的价值。",
        "desc": "现值计算器：输入未来值、贴现率与年数求现值。",
        "inputs": [
            {"id": "fv", "label": "未来值 FV", "value": "20000", "step": "100"},
            {"id": "r", "label": "贴现率 r (%)", "value": "5", "step": "0.1"},
            {"id": "t", "label": "年数 t", "value": "10", "step": "1"},
        ],
        "calc": """
            const fv = num('fv'), r = num('r'), t = num('t');
            const pv = fv / Math.pow(1 + r / 100, t);
            ToolBox.setResult('result', dataGrid([
                [pv.toFixed(2), '现值 PV'],
                [(fv - pv).toFixed(2), '贴现额']
            ]));
        """,
        "notes": ["20000 元、5%、10 年 → 现值约 12278.27。", "贴现率越高现值越低。"],
    },
    {
        "slug": "fv-annuity", "industry": "economics", "cat": "economics", "icon": "📅", "bg": "#fff7ed",
        "title": "年金终值", "h1": "年金终值计算器",
        "h2": "FV = PMT·[(1+i)^N − 1]/i",
        "intro": "每期期末等额存入 PMT、共 N 期、每期利率 i 的年金终值。",
        "desc": "年金终值计算器：输入每期金额、期利率与期数求年金终值。",
        "inputs": [
            {"id": "pmt", "label": "每期金额 PMT", "value": "1000", "step": "50"},
            {"id": "i", "label": "每期利率 i (%)", "value": "1", "step": "0.1"},
            {"id": "n", "label": "期数 N", "value": "12", "step": "1"},
        ],
        "calc": """
            const pmt = num('pmt'), i = num('i') / 100, n = num('n');
            const fv = i === 0 ? pmt * n : pmt * (Math.pow(1 + i, n) - 1) / i;
            ToolBox.setResult('result', dataGrid([
                [fv.toFixed(2), '年金终值 FV'],
                [(fv - pmt * n).toFixed(2), '利息总额']
            ]));
        """,
        "notes": ["每期 1000、1%、12 期 → 约 12682.50。", "i=0 时退化为 PMT×N。"],
    },
    {
        "slug": "pv-annuity", "industry": "economics", "cat": "economics", "icon": "🧾", "bg": "#fff7ed",
        "title": "年金现值", "h1": "年金现值计算器",
        "h2": "PV = PMT·[1 − (1+i)^−N]/i",
        "intro": "每期期末等额收款 PMT、共 N 期、每期利率 i 的年金现值。",
        "desc": "年金现值计算器：输入每期金额、期利率与期数求年金现值。",
        "inputs": [
            {"id": "pmt", "label": "每期金额 PMT", "value": "1000", "step": "50"},
            {"id": "i", "label": "每期利率 i (%)", "value": "1", "step": "0.1"},
            {"id": "n", "label": "期数 N", "value": "12", "step": "1"},
        ],
        "calc": """
            const pmt = num('pmt'), i = num('i') / 100, n = num('n');
            const pv = i === 0 ? pmt * n : pmt * (1 - Math.pow(1 + i, -n)) / i;
            ToolBox.setResult('result', dataGrid([
                [pv.toFixed(2), '年金现值 PV'],
                [(pmt * n - pv).toFixed(2), '贴现总额']
            ]));
        """,
        "notes": ["每期 1000、1%、12 期 → 现值约 11255.08。", "i=0 时退化为 PMT×N。"],
    },
    {
        "slug": "unemployment-rate", "industry": "economics", "cat": "economics", "icon": "👥", "bg": "#fff7ed",
        "title": "失业率", "h1": "失业率计算器",
        "h2": "u = 失业人数 / 劳动力 × 100%",
        "intro": "劳动力中失业者所占比例。",
        "desc": "失业率计算器：输入失业人数与劳动力总数求失业率。",
        "inputs": [
            {"id": "unemp", "label": "失业人数", "value": "600", "step": "10"},
            {"id": "lf", "label": "劳动力总数", "value": "10000", "step": "100"},
        ],
        "calc": """
            const u = num('unemp'), lf = num('lf');
            const rate = u / lf * 100;
            ToolBox.setResult('result', dataGrid([
                [rate.toFixed(2), '失业率 (%)'],
                [(lf - u).toFixed(0), '就业人数']
            ]));
        """,
        "notes": ["600/10000 = 6% 失业率。", "劳动力 = 就业 + 失业。"],
    },
    {
        "slug": "elasticity-demand", "industry": "economics", "cat": "economics", "icon": "🔁", "bg": "#fff7ed",
        "title": "需求价格弹性（中点法）", "h1": "需求价格弹性计算器",
        "h2": "E_d = (%ΔQ) / (%ΔP)",
        "intro": "用中点法计算需求对价格的弹性，避免端点依赖。",
        "desc": "需求价格弹性计算器：输入价格与数量变动求弹性。",
        "inputs": [
            {"id": "q1", "label": "原数量 Q₁", "value": "100", "step": "1"},
            {"id": "q2", "label": "新数量 Q₂", "value": "80", "step": "1"},
            {"id": "p1", "label": "原价格 P₁", "value": "10", "step": "0.5"},
            {"id": "p2", "label": "新价格 P₂", "value": "12", "step": "0.5"},
        ],
        "calc": """
            const q1 = num('q1'), q2 = num('q2'), p1 = num('p1'), p2 = num('p2');
            const dQ = (q2 - q1) / ((q1 + q2) / 2);
            const dP = (p2 - p1) / ((p1 + p2) / 2);
            const e = dQ / dP;
            const type = Math.abs(e) > 1 ? '富有弹性' : (Math.abs(e) < 1 ? '缺乏弹性' : '单位弹性');
            ToolBox.setResult('result', dataGrid([
                [e.toFixed(3), '需求价格弹性 E_d'],
                [type, '弹性类型']
            ]));
        """,
        "notes": ["价格 10→12、数量 100→80 → E_d ≈ −1.22（富有弹性）。", "绝对值>1 为富有弹性。"],
    },
    {
        "slug": "cross-elasticity", "industry": "economics", "cat": "economics", "icon": "🔗", "bg": "#fff7ed",
        "title": "交叉价格弹性", "h1": "交叉价格弹性计算器",
        "h2": "E_xy = (%ΔQ_x) / (%ΔP_y)",
        "intro": "商品 y 价格变动对商品 x 需求量的影响。正为替代品，负为互补品。",
        "desc": "交叉价格弹性计算器：输入两商品数量与价格变动求交叉弹性。",
        "inputs": [
            {"id": "qx1", "label": "商品 x 原数量", "value": "100", "step": "1"},
            {"id": "qx2", "label": "商品 x 新数量", "value": "110", "step": "1"},
            {"id": "py1", "label": "商品 y 原价格", "value": "10", "step": "0.5"},
            {"id": "py2", "label": "商品 y 新价格", "value": "12", "step": "0.5"},
        ],
        "calc": """
            const q1 = num('qx1'), q2 = num('qx2'), p1 = num('py1'), p2 = num('py2');
            const dQ = (q2 - q1) / ((q1 + q2) / 2);
            const dP = (p2 - p1) / ((p1 + p2) / 2);
            const e = dQ / dP;
            const type = e > 0 ? '替代品' : (e < 0 ? '互补品' : '无关');
            ToolBox.setResult('result', dataGrid([
                [e.toFixed(3), '交叉价格弹性 E_xy'],
                [type, '关系']
            ]));
        """,
        "notes": ["y 涨价、x 需求上升 → 替代品（正）。", "负则为互补品。"],
    },
    {
        "slug": "income-elasticity", "industry": "economics", "cat": "economics", "icon": "💼", "bg": "#fff7ed",
        "title": "收入弹性", "h1": "收入弹性计算器",
        "h2": "E_i = (%ΔQ) / (%ΔI)",
        "intro": "收入变动对需求量的影响。正常品为正，劣等品为负。",
        "desc": "收入弹性计算器：输入数量与收入变动求收入弹性。",
        "inputs": [
            {"id": "q1", "label": "原数量 Q₁", "value": "100", "step": "1"},
            {"id": "q2", "label": "新数量 Q₂", "value": "115", "step": "1"},
            {"id": "i1", "label": "原收入 I₁", "value": "1000", "step": "10"},
            {"id": "i2", "label": "新收入 I₂", "value": "1100", "step": "10"},
        ],
        "calc": """
            const q1 = num('q1'), q2 = num('q2'), i1 = num('i1'), i2 = num('i2');
            const dQ = (q2 - q1) / ((q1 + q2) / 2);
            const dI = (i2 - i1) / ((i1 + i2) / 2);
            const e = dQ / dI;
            const type = e > 0 ? '正常品' : '劣等品';
            ToolBox.setResult('result', dataGrid([
                [e.toFixed(3), '收入弹性 E_i'],
                [type, '商品类型']
            ]));
        """,
        "notes": ["收入上升需求上升 → 正常品（正）。", "负值为劣等品。"],
    },
    {
        "slug": "okuns-law", "industry": "economics", "cat": "economics", "icon": "📉", "bg": "#fff7ed",
        "title": "奥肯定律", "h1": "奥肯定律计算器",
        "h2": "Δu ≈ −½(实际增长 − 潜在增长)",
        "intro": "实际 GDP 增长率与潜在增长率之差对失业率变化的影响。",
        "desc": "奥肯定律计算器：输入实际与潜在增长率求失业率变化。",
        "inputs": [
            {"id": "g", "label": "实际 GDP 增长率 (%)", "value": "4", "step": "0.1"},
            {"id": "gp", "label": "潜在增长率 (%)", "value": "3", "step": "0.1"},
        ],
        "calc": """
            const g = num('g'), gp = num('gp');
            const du = -0.5 * (g - gp);
            ToolBox.setResult('result', dataGrid([
                [du.toFixed(2), '失业率变化 Δu (百分点)'],
                [(g - gp).toFixed(2), '增长缺口']
            ]));
        """,
        "notes": ["实际 4%、潜在 3% → 失业率下降约 0.5 点。", "系数为 −½（常用近似）。"],
    },
    {
        "slug": "spending-multiplier", "industry": "economics", "cat": "economics", "icon": "🔄", "bg": "#fff7ed",
        "title": "支出乘数", "h1": "政府支出乘数计算器",
        "h2": "k = 1 / (1 − MPC)",
        "intro": "边际消费倾向 MPC 决定的政府购买乘数。",
        "desc": "支出乘数计算器：输入边际消费倾向求乘数。",
        "inputs": [
            {"id": "mpc", "label": "边际消费倾向 MPC", "value": "0.8", "step": "0.05"},
        ],
        "calc": """
            const mpc = num('mpc');
            const k = 1 / (1 - mpc);
            const kt = -mpc / (1 - mpc);
            ToolBox.setResult('result', dataGrid([
                [k.toFixed(2), '政府购买乘数 k'],
                [kt.toFixed(2), '税收乘数 k_t']
            ]));
        """,
        "notes": ["MPC=0.8 → 乘数 5。", "税收乘数为 −MPC/(1−MPC)。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
