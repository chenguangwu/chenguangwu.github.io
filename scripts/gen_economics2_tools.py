# -*- coding: utf-8 -*-
"""Batch 57: 经济学深化 II（14 个公式计算器）。industry=economics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "gdp-growth-rate",
        "industry": "economics",
        "cat": "economics",
        "icon": "trending-up",
        "bg": "from-indigo-500 to-blue-600",
        "title": "GDP 增长率计算器",
        "h1": "g = (GDP_t − GDP_{t−1}) / GDP_{t−1}",
        "h2": "由两期 GDP 求增长率",
        "intro": "输入本期与基期 GDP，求增长率。", "desc": "GDP 增长率：输入 GDP_t、GDP_{t−1}，输出 g(%)。",
        "inputs": [
            {"id": "gt", "label": "本期 GDP_t", "value": "1050", "step": "10", "unit": "亿元"},
            {"id": "gp", "label": "基期 GDP", "value": "1000", "step": "10", "unit": "亿元"},
        ],
        "calc": """
            const gt=num('gt'),gp=num('gp');
            const g=(gt-gp)/gp*100;
            ToolBox.setResult('result', dataGrid([
                [g.toFixed(2),'GDP 增长率 g (%)']
            ]));
        """,
        "notes": ["g = (GDP_t−GDP_{t−1})/GDP_{t−1}。", "1050/1000 → 5.0%。"],
    },
    {
        "slug": "nominal-to-real",
        "industry": "economics",
        "cat": "economics",
        "icon": "scale",
        "bg": "from-indigo-500 to-blue-600",
        "title": "名义转实际值计算器",
        "h1": "Real = Nominal / (1+π)",
        "h2": "由名义值与通胀率求实际值",
        "intro": "输入名义值 Nominal 与通胀率 π，求实际值。", "desc": "名义转实际值：输入 Nominal、π，输出 Real。",
        "inputs": [
            {"id": "nom", "label": "名义值 Nominal", "value": "110", "step": "1", "unit": ""},
            {"id": "pi", "label": "通胀率 π", "value": "0.10", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const nom=num('nom'),pi=num('pi');
            const real=nom/(1+pi);
            ToolBox.setResult('result', dataGrid([
                [real.toFixed(2),'实际值 Real']
            ]));
        """,
        "notes": ["Real = Nominal/(1+π)。", "110,π=10% → 100。"],
    },
    {
        "slug": "velocity-of-money",
        "industry": "economics",
        "cat": "economics",
        "icon": "zap",
        "bg": "from-indigo-500 to-blue-600",
        "title": "货币流通速度计算器",
        "h1": "V = P·Y / M",
        "h2": "由价格水平、产出与货币量求流通速度",
        "intro": "输入价格水平 P、实际产出 Y、货币量 M，求货币流通速度。", "desc": "货币流通速度：输入 P、Y、M，输出 V。",
        "inputs": [
            {"id": "P", "label": "价格水平 P", "value": "1", "step": "0.05", "unit": ""},
            {"id": "Y", "label": "实际产出 Y", "value": "2000", "step": "50", "unit": "亿元"},
            {"id": "M", "label": "货币量 M", "value": "500", "step": "10", "unit": "亿元"},
        ],
        "calc": """
            const P=num('P'),Y=num('Y'),M=num('M');
            const V=P*Y/M;
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(2),'流通速度 V']
            ]));
        """,
        "notes": ["MV = PY（交易方程）。", "P=1,Y=2000,M=500 → 4。"],
    },
    {
        "slug": "marginal-propensity-consume",
        "industry": "economics",
        "cat": "economics",
        "icon": "trending-up",
        "bg": "from-indigo-500 to-blue-600",
        "title": "边际消费倾向计算器",
        "h1": "MPC = ΔC / ΔY",
        "h2": "由消费与收入增量求边际消费倾向",
        "intro": "输入消费增量 ΔC 与收入增量 ΔY，求 MPC。", "desc": "边际消费倾向：输入 ΔC、ΔY，输出 MPC。",
        "inputs": [
            {"id": "dc", "label": "消费增量 ΔC", "value": "80", "step": "5", "unit": ""},
            {"id": "dy", "label": "收入增量 ΔY", "value": "100", "step": "5", "unit": ""},
        ],
        "calc": """
            const dc=num('dc'),dy=num('dy');
            const mpc=dc/dy;
            ToolBox.setResult('result', dataGrid([
                [mpc.toFixed(3),'边际消费倾向 MPC']
            ]));
        """,
        "notes": ["MPC = ΔC/ΔY，0<MPC<1。", "80/100 → 0.8。"],
    },
    {
        "slug": "mpc-from-multiplier",
        "industry": "economics",
        "cat": "economics",
        "icon": "trending-up",
        "bg": "from-indigo-500 to-blue-600",
        "title": "由乘数反推 MPC 计算器",
        "h1": "MPC = 1 − 1/k",
        "h2": "由支出乘数反推边际消费倾向",
        "intro": "输入支出乘数 k，求边际消费倾向。", "desc": "由乘数反推 MPC：输入 k，输出 MPC。",
        "inputs": [{"id": "k", "label": "支出乘数 k", "value": "5", "step": "0.5", "unit": ""}],
        "calc": """
            const k=num('k');
            const mpc=1-1/k;
            ToolBox.setResult('result', dataGrid([
                [mpc.toFixed(3),'边际消费倾向 MPC']
            ]));
        """,
        "notes": ["k = 1/(1−MPC)。", "k=5 → MPC=0.8。"],
    },
    {
        "slug": "fisher-equation",
        "industry": "economics",
        "cat": "economics",
        "icon": "percent",
        "bg": "from-indigo-500 to-blue-600",
        "title": "费雪方程计算器",
        "h1": "i ≈ r + π",
        "h2": "由实际利率与通胀求名义利率",
        "intro": "输入实际利率 r 与通胀率 π，求名义利率。", "desc": "费雪方程：输入 r、π，输出 i(%)。",
        "inputs": [
            {"id": "r", "label": "实际利率 r", "value": "2", "step": "0.1", "unit": "%"},
            {"id": "pi", "label": "通胀率 π", "value": "3", "step": "0.1", "unit": "%"},
        ],
        "calc": """
            const r=num('r'),pi=num('pi');
            const i=r+pi;
            ToolBox.setResult('result', dataGrid([
                [i.toFixed(2),'名义利率 i (%)']
            ]));
        """,
        "notes": ["i ≈ r + π（近似）。", "r=2,π=3 → i=5%。"],
    },
    {
        "slug": "tax-multiplier",
        "industry": "economics",
        "cat": "economics",
        "icon": "trending-down",
        "bg": "from-indigo-500 to-blue-600",
        "title": "税收乘数计算器",
        "h1": "k_t = −MPC / (1−MPC)",
        "h2": "由边际消费倾向求税收乘数",
        "intro": "输入边际消费倾向 MPC，求税收乘数。", "desc": "税收乘数：输入 MPC，输出 k_t。",
        "inputs": [{"id": "mpc", "label": "边际消费倾向 MPC", "value": "0.8", "step": "0.05", "unit": ""}],
        "calc": """
            const mpc=num('mpc');
            const kt=-mpc/(1-mpc);
            ToolBox.setResult('result', dataGrid([
                [kt.toFixed(2),'税收乘数 k_t']
            ]));
        """,
        "notes": ["k_t = −MPC/(1−MPC)，负号表示反向。", "MPC=0.8 → −4。"],
    },
    {
        "slug": "gdp-expenditure",
        "industry": "economics",
        "cat": "economics",
        "icon": "bar-chart",
        "bg": "from-indigo-500 to-blue-600",
        "title": "支出法 GDP 计算器",
        "h1": "Y = C + I + G + (X−M)",
        "h2": "由支出分项求 GDP",
        "intro": "输入消费 C、投资 I、政府支出 G、净出口 NX，求 GDP。", "desc": "支出法 GDP：输入 C、I、G、NX，输出 Y。",
        "inputs": [
            {"id": "C", "label": "消费 C", "value": "1000", "step": "10", "unit": "亿元"},
            {"id": "I", "label": "投资 I", "value": "300", "step": "10", "unit": "亿元"},
            {"id": "G", "label": "政府支出 G", "value": "200", "step": "10", "unit": "亿元"},
            {"id": "NX", "label": "净出口 NX", "value": "50", "step": "10", "unit": "亿元"},
        ],
        "calc": """
            const C=num('C'),I=num('I'),G=num('G'),NX=num('NX');
            const Y=C+I+G+NX;
            ToolBox.setResult('result', dataGrid([
                [Y.toFixed(0),'GDP Y']
            ]));
        """,
        "notes": ["Y = C+I+G+(X−M)。", "1000+300+200+50 → 1550。"],
    },
    {
        "slug": "labor-force-participation",
        "industry": "economics",
        "cat": "economics",
        "icon": "users",
        "bg": "from-indigo-500 to-blue-600",
        "title": "劳动参与率计算器",
        "h1": "LFP = LF / POP",
        "h2": "由劳动力与总人口求劳动参与率",
        "intro": "输入劳动力 LF 与适龄人口 POP，求劳动参与率。", "desc": "劳动参与率：输入 LF、POP，输出 LFP(%)。",
        "inputs": [
            {"id": "lf", "label": "劳动力 LF", "value": "150", "step": "5", "unit": "万人"},
            {"id": "pop", "label": "适龄人口 POP", "value": "250", "step": "5", "unit": "万人"},
        ],
        "calc": """
            const lf=num('lf'),pop=num('pop');
            const lfp=lf/pop*100;
            ToolBox.setResult('result', dataGrid([
                [lfp.toFixed(1),'劳动参与率 LFP (%)']
            ]));
        """,
        "notes": ["LFP = LF/POP。", "150/250 → 60%。"],
    },
    {
        "slug": "labor-force",
        "industry": "economics",
        "cat": "economics",
        "icon": "users",
        "bg": "from-indigo-500 to-blue-600",
        "title": "劳动力规模计算器",
        "h1": "LF = E + U",
        "h2": "由就业与失业人数求劳动力",
        "intro": "输入就业人数 E 与失业人数 U，求劳动力规模。", "desc": "劳动力规模：输入 E、U，输出 LF。",
        "inputs": [
            {"id": "E", "label": "就业 E", "value": "140", "step": "5", "unit": "万人"},
            {"id": "U", "label": "失业 U", "value": "10", "step": "1", "unit": "万人"},
        ],
        "calc": """
            const E=num('E'),U=num('U');
            const LF=E+U;
            ToolBox.setResult('result', dataGrid([
                [LF.toFixed(0),'劳动力 LF']
            ]));
        """,
        "notes": ["LF = 就业 + 失业。", "140+10 → 150 万人。"],
    },
    {
        "slug": "balance-of-trade",
        "industry": "economics",
        "cat": "economics",
        "icon": "scale",
        "bg": "from-indigo-500 to-blue-600",
        "title": "贸易差额计算器",
        "h1": "BoT = X − M",
        "h2": "由出口与进口求贸易差额",
        "intro": "输入出口 X 与进口 M，求贸易差额。", "desc": "贸易差额：输入 X、M，输出 BoT。",
        "inputs": [
            {"id": "X", "label": "出口 X", "value": "200", "step": "10", "unit": "亿元"},
            {"id": "M", "label": "进口 M", "value": "180", "step": "10", "unit": "亿元"},
        ],
        "calc": """
            const X=num('X'),M=num('M');
            const bot=X-M;
            ToolBox.setResult('result', dataGrid([
                [bot.toFixed(0),'贸易差额 BoT']
            ]));
        """,
        "notes": ["BoT = X−M；正为顺差。", "200−180 → 20 亿元顺差。"],
    },
    {
        "slug": "marginal-product-labor",
        "industry": "economics",
        "cat": "economics",
        "icon": "factory",
        "bg": "from-indigo-500 to-blue-600",
        "title": "劳动边际产量计算器",
        "h1": "MPL = ΔQ / ΔL",
        "h2": "由产量与劳动增量求边际产量",
        "intro": "输入产量增量 ΔQ 与劳动增量 ΔL，求劳动边际产量。", "desc": "劳动边际产量：输入 ΔQ、ΔL，输出 MPL。",
        "inputs": [
            {"id": "dq", "label": "产量增量 ΔQ", "value": "50", "step": "5", "unit": ""},
            {"id": "dl", "label": "劳动增量 ΔL", "value": "10", "step": "1", "unit": ""},
        ],
        "calc": """
            const dq=num('dq'),dl=num('dl');
            const mpl=dq/dl;
            ToolBox.setResult('result', dataGrid([
                [mpl.toFixed(2),'劳动边际产量 MPL']
            ]));
        """,
        "notes": ["MPL = ΔQ/ΔL。", "50/10 → 5。"],
    },
    {
        "slug": "cobb-douglas",
        "industry": "economics",
        "cat": "economics",
        "icon": "function-square",
        "bg": "from-indigo-500 to-blue-600",
        "title": "Cobb-Douglas 生产函数计算器",
        "h1": "Y = A·K^α·L^{(1−α)}",
        "h2": "由资本、劳动与技术求产出",
        "intro": "输入全要素生产率 A、资本 K、资本弹性 α、劳动 L，求产出。", "desc": "Cobb-Douglas 生产函数：输入 A、K、α、L，输出 Y。",
        "inputs": [
            {"id": "A", "label": "技术水平 A", "value": "1", "step": "0.1", "unit": ""},
            {"id": "K", "label": "资本 K", "value": "200", "step": "10", "unit": ""},
            {"id": "al", "label": "资本弹性 α", "value": "0.3", "step": "0.05", "unit": ""},
            {"id": "L", "label": "劳动 L", "value": "100", "step": "10", "unit": ""},
        ],
        "calc": """
            const A=num('A'),K=num('K'),al=num('al'),L=num('L');
            const Y=A*Math.pow(K,al)*Math.pow(L,1-al);
            ToolBox.setResult('result', dataGrid([
                [Y.toFixed(2),'产出 Y']
            ]));
        """,
        "notes": ["Y = A·K^α·L^(1−α)（规模报酬不变）。", "A=1,K=200,α=0.3,L=100 → 约 123.3。"],
    },
    {
        "slug": "average-propensity-consume",
        "industry": "economics",
        "cat": "economics",
        "icon": "pie-chart",
        "bg": "from-indigo-500 to-blue-600",
        "title": "平均消费倾向计算器",
        "h1": "APC = C / Y",
        "h2": "由消费与收入求平均消费倾向",
        "intro": "输入消费 C 与收入 Y，求平均消费倾向。", "desc": "平均消费倾向：输入 C、Y，输出 APC。",
        "inputs": [
            {"id": "C", "label": "消费 C", "value": "800", "step": "10", "unit": ""},
            {"id": "Y", "label": "收入 Y", "value": "1000", "step": "10", "unit": ""},
        ],
        "calc": """
            const C=num('C'),Y=num('Y');
            const apc=C/Y;
            ToolBox.setResult('result', dataGrid([
                [apc.toFixed(3),'平均消费倾向 APC']
            ]));
        """,
        "notes": ["APC = C/Y。", "800/1000 → 0.8。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
