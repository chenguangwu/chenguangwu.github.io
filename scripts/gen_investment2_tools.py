# -*- coding: utf-8 -*-
"""Batch 62: 投资分析深化 II（14 个公式计算器）。industry=investment。"""
from tool_template import main

TOOLS = [
    {
        "slug": "cagr",
        "industry": "investment",
        "cat": "investment",
        "icon": "trending-up",
        "bg": "from-orange-500 to-amber-600",
        "title": "复合年增长率(CAGR)计算器",
        "h1": "CAGR = (EV/BV)^{1/n} − 1",
        "h2": "由期初与期末价值及年数求复合年增长率",
        "intro": "输入期初价值 BV、期末价值 EV 与年数 n，求 CAGR。",
        "desc": "复合年增长率：输入 BV、EV、n，输出 CAGR(%)。",
        "inputs": [
            {"id": "BV", "label": "期初价值 BV", "value": "100000", "step": "5000", "unit": "元"},
            {"id": "EV", "label": "期末价值 EV", "value": "200000", "step": "5000", "unit": "元"},
            {"id": "n", "label": "年数 n", "value": "5", "step": "1", "unit": "年"},
        ],
        "calc": """
            const BV=num('BV'),EV=num('EV'),n=num('n');
            const cagr=Math.pow(EV/BV,1/n)-1;
            ToolBox.setResult('result', dataGrid([
                [(cagr*100).toFixed(2),'复合年增长率 CAGR (%)']
            ]));
        """,
        "notes": ["CAGR 平滑了期间波动。", "10 万→20 万,5 年 → 14.87%。"],
    },
    {
        "slug": "future-value-inv",
        "industry": "investment",
        "cat": "investment",
        "icon": "arrow-up-right",
        "bg": "from-orange-500 to-amber-600",
        "title": "复利未来值计算器",
        "h1": "FV = PV·(1+r)^n",
        "h2": "由现值、利率与年数求投资未来值",
        "intro": "输入现值 PV、年利率 r 与年数 n，求未来值。",
        "desc": "复利未来值：输入 PV、r、n，输出 FV。",
        "inputs": [
            {"id": "PV", "label": "现值 PV", "value": "10000", "step": "500", "unit": "元"},
            {"id": "r", "label": "年利率 r", "value": "0.08", "step": "0.005", "unit": ""},
            {"id": "n", "label": "年数 n", "value": "10", "step": "1", "unit": "年"},
        ],
        "calc": """
            const PV=num('PV'),r=num('r'),n=num('n');
            const FV=PV*Math.pow(1+r,n);
            ToolBox.setResult('result', dataGrid([
                [FV.toFixed(2),'未来值 FV (元)']
            ]));
        """,
        "notes": ["一次性投入的复利终值。", "1 万,8%,10 年 → 21589 元。"],
    },
    {
        "slug": "present-value-inv",
        "industry": "investment",
        "cat": "investment",
        "icon": "arrow-down-right",
        "bg": "from-orange-500 to-amber-600",
        "title": "投资现值计算器",
        "h1": "PV = FV / (1+r)^n",
        "h2": "由未来值、贴现率与年数求现值",
        "intro": "输入未来值 FV、贴现率 r 与年数 n，求现值。",
        "desc": "投资现值：输入 FV、r、n，输出 PV。",
        "inputs": [
            {"id": "FV", "label": "未来值 FV", "value": "21589", "step": "500", "unit": "元"},
            {"id": "r", "label": "贴现率 r", "value": "0.08", "step": "0.005", "unit": ""},
            {"id": "n", "label": "年数 n", "value": "10", "step": "1", "unit": "年"},
        ],
        "calc": """
            const FV=num('FV'),r=num('r'),n=num('n');
            const PV=FV/Math.pow(1+r,n);
            ToolBox.setResult('result', dataGrid([
                [PV.toFixed(2),'现值 PV (元)']
            ]));
        """,
        "notes": ["现值为未来现金流按利率贴现。", "21589,8%,10 年 → 10000 元。"],
    },
    {
        "slug": "annuity-fv-inv",
        "industry": "investment",
        "cat": "investment",
        "icon": "repeat",
        "bg": "from-orange-500 to-amber-600",
        "title": "年金未来值计算器",
        "h1": "FV = PMT·[(1+r)^n − 1] / r",
        "h2": "由每期定投、利率与期数求年金终值",
        "intro": "输入每期定投 PMT、每期利率 r 与期数 n，求年金终值。",
        "desc": "年金未来值：输入 PMT、r、n，输出 FV。",
        "inputs": [
            {"id": "PMT", "label": "每期定投 PMT", "value": "1000", "step": "50", "unit": "元"},
            {"id": "r", "label": "每期利率 r", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "n", "label": "期数 n", "value": "10", "step": "1", "unit": ""},
        ],
        "calc": """
            const PMT=num('PMT'),r=num('r'),n=num('n');
            const FV=PMT*(Math.pow(1+r,n)-1)/r;
            ToolBox.setResult('result', dataGrid([
                [FV.toFixed(2),'年金终值 FV (元)']
            ]));
        """,
        "notes": ["适用于定期定额投资。", "1000,5%,10 期 → 12578 元。"],
    },
    {
        "slug": "annuity-pv-inv",
        "industry": "investment",
        "cat": "investment",
        "icon": "repeat",
        "bg": "from-orange-500 to-amber-600",
        "title": "年金现值计算器",
        "h1": "PV = PMT·[1 − (1+r)^{−n}] / r",
        "h2": "由每期现金流、利率与期数求年金现值",
        "intro": "输入每期现金流 PMT、每期利率 r 与期数 n，求年金现值。",
        "desc": "年金现值：输入 PMT、r、n，输出 PV。",
        "inputs": [
            {"id": "PMT", "label": "每期现金流 PMT", "value": "1000", "step": "50", "unit": "元"},
            {"id": "r", "label": "每期利率 r", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "n", "label": "期数 n", "value": "10", "step": "1", "unit": ""},
        ],
        "calc": """
            const PMT=num('PMT'),r=num('r'),n=num('n');
            const PV=PMT*(1-Math.pow(1+r,-n))/r;
            ToolBox.setResult('result', dataGrid([
                [PV.toFixed(2),'年金现值 PV (元)']
            ]));
        """,
        "notes": ["r=0 时现值退化为 PMT·n。", "1000,5%,10 期 → 7722 元。"],
    },
    {
        "slug": "dividend-payout-ratio",
        "industry": "investment",
        "cat": "investment",
        "icon": "pie-chart",
        "bg": "from-orange-500 to-amber-600",
        "title": "股利支付率计算器",
        "h1": "DPR = DPS / EPS",
        "h2": "由每股股利与每股收益求股利支付率",
        "intro": "输入每股股利 DPS 与每股收益 EPS，求股利支付率。",
        "desc": "股利支付率：输入 DPS、EPS，输出 DPR(%)。",
        "inputs": [
            {"id": "DPS", "label": "每股股利 DPS", "value": "2", "step": "0.1", "unit": "元"},
            {"id": "EPS", "label": "每股收益 EPS", "value": "5", "step": "0.2", "unit": "元"},
        ],
        "calc": """
            const DPS=num('DPS'),EPS=num('EPS');
            const DPR=DPS/EPS*100;
            ToolBox.setResult('result', dataGrid([
                [DPR.toFixed(1),'股利支付率 DPR (%)']
            ]));
        """,
        "notes": ["DPR 低则再投资比例高。", "2/5 → 40%。"],
    },
    {
        "slug": "retention-ratio",
        "industry": "investment",
        "cat": "investment",
        "icon": "pie-chart",
        "bg": "from-orange-500 to-amber-600",
        "title": "留存收益率计算器",
        "h1": "b = 1 − DPR",
        "h2": "由股利支付率求留存收益率",
        "intro": "输入股利支付率 DPR，求留存收益率。",
        "desc": "留存收益率：输入 DPR(%)，输出 b(%)。",
        "inputs": [
            {"id": "DPR", "label": "股利支付率 DPR", "value": "40", "step": "5", "unit": "%"},
        ],
        "calc": """
            const DPR=num('DPR');
            const b=100-DPR;
            ToolBox.setResult('result', dataGrid([
                [b.toFixed(1),'留存收益率 b (%)']
            ]));
        """,
        "notes": ["留存收益用于企业再投资。", "DPR=40% → b=60%。"],
    },
    {
        "slug": "sustainable-growth",
        "industry": "investment",
        "cat": "investment",
        "icon": "trending-up",
        "bg": "from-orange-500 to-amber-600",
        "title": "可持续增长率计算器",
        "h1": "g = ROE × b",
        "h2": "由净资产收益率与留存收益率求可持续增长率",
        "intro": "输入净资产收益率 ROE 与留存收益率 b，求可持续增长率。",
        "desc": "可持续增长率：输入 ROE(%)、b(%)，输出 g(%)。",
        "inputs": [
            {"id": "ROE", "label": "净资产收益率 ROE", "value": "15", "step": "1", "unit": "%"},
            {"id": "b", "label": "留存收益率 b", "value": "60", "step": "5", "unit": "%"},
        ],
        "calc": """
            const ROE=num('ROE')/100,b=num('b')/100;
            const g=ROE*b*100;
            ToolBox.setResult('result', dataGrid([
                [g.toFixed(2),'可持续增长率 g (%)']
            ]));
        """,
        "notes": ["不增发不举债时的最高增速。", "15%×60% → 9%。"],
    },
    {
        "slug": "capm-return",
        "industry": "investment",
        "cat": "investment",
        "icon": "line-chart",
        "bg": "from-orange-500 to-amber-600",
        "title": "CAPM 预期收益率计算器",
        "h1": "E(r) = r_f + β(r_m − r_f)",
        "h2": "由无风险利率、β与市场溢价求预期收益率",
        "intro": "输入无风险利率 r_f、β 与市场收益率 r_m，求预期收益率。",
        "desc": "CAPM 预期收益：输入 rf、beta、rm，输出 E(r)(%)。",
        "inputs": [
            {"id": "rf", "label": "无风险利率 r_f", "value": "0.03", "step": "0.005", "unit": ""},
            {"id": "beta", "label": "β", "value": "1.2", "step": "0.1", "unit": ""},
            {"id": "rm", "label": "市场收益率 r_m", "value": "0.08", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const rf=num('rf'),beta=num('beta'),rm=num('rm');
            const er=rf+beta*(rm-rf);
            ToolBox.setResult('result', dataGrid([
                [(er*100).toFixed(2),'预期收益率 E(r) (%)']
            ]));
        """,
        "notes": ["β 衡量系统性风险。", "3%+1.2×(8%−3%) → 9%。"],
    },
    {
        "slug": "portfolio-beta",
        "industry": "investment",
        "cat": "investment",
        "icon": "layers",
        "bg": "from-orange-500 to-amber-600",
        "title": "投资组合 β 计算器",
        "h1": "β_p = Σ w_i·β_i",
        "h2": "由两资产权重与 β 求组合 β",
        "intro": "输入两资产权重 w₁、w₂ 与 β₁、β₂（w₁+w₂=1），求组合 β。",
        "desc": "组合 β：输入 w1、beta1、w2、beta2，输出 β_p。",
        "inputs": [
            {"id": "w1", "label": "权重 w₁", "value": "0.5", "step": "0.05", "unit": ""},
            {"id": "b1", "label": "β₁", "value": "1.0", "step": "0.1", "unit": ""},
            {"id": "w2", "label": "权重 w₂", "value": "0.5", "step": "0.05", "unit": ""},
            {"id": "b2", "label": "β₂", "value": "1.4", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const w1=num('w1'),b1=num('b1'),w2=num('w2'),b2=num('b2');
            const bp=w1*b1+w2*b2;
            ToolBox.setResult('result', dataGrid([
                [bp.toFixed(3),'组合 β_p']
            ]));
        """,
        "notes": ["组合 β 为加权平均。", "0.5×1.0+0.5×1.4 → 1.2。"],
    },
    {
        "slug": "geometric-mean-return",
        "industry": "investment",
        "cat": "investment",
        "icon": "percent",
        "bg": "from-orange-500 to-amber-600",
        "title": "几何平均收益率计算器",
        "h1": "g = (Π(1+r_i))^{1/n} − 1",
        "h2": "由多期收益率序列求几何平均收益率",
        "intro": "输入多期收益率（逗号或空格分隔），求几何平均收益率。",
        "desc": "几何平均收益率：输入 r(列表)，输出 g(%)。",
        "inputs": [
            {"id": "r", "label": "收益率序列 r", "value": "0.1, 0.2, -0.05", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('r').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            let prod=1;
            for(const x of raw){ prod*= (1+x); }
            const g=Math.pow(prod, 1/raw.length)-1;
            ToolBox.setResult('result', dataGrid([
                [(g*100).toFixed(2),'几何平均收益率 g (%)']
            ]));
        """,
        "notes": ["几何平均考虑复利，低于算术平均。", "0.1,0.2,−0.05 → 7.83%。"],
    },
    {
        "slug": "real-rate-return",
        "industry": "investment",
        "cat": "investment",
        "icon": "scale",
        "bg": "from-orange-500 to-amber-600",
        "title": "实际收益率计算器",
        "h1": "r_real = (1+r_nom)/(1+i) − 1",
        "h2": "由名义收益率与通胀率求实际收益率",
        "intro": "输入名义收益率 r_nom 与通货膨胀率 i，求实际收益率。",
        "desc": "实际收益率：输入 nom、inf，输出 r_real(%)。",
        "inputs": [
            {"id": "nom", "label": "名义收益率", "value": "0.08", "step": "0.005", "unit": ""},
            {"id": "inf", "label": "通胀率 i", "value": "0.03", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const nom=num('nom'),inf=num('inf');
            const rr=(1+nom)/(1+inf)-1;
            ToolBox.setResult('result', dataGrid([
                [(rr*100).toFixed(2),'实际收益率 (%)']
            ]));
        """,
        "notes": ["费雪近似：r_real ≈ r_nom − i。", "(1.08/1.03)−1 → 4.85%。"],
    },
    {
        "slug": "bond-ytm-approx",
        "industry": "investment",
        "cat": "investment",
        "icon": "line-chart",
        "bg": "from-orange-500 to-amber-600",
        "title": "债券到期收益率(近似)计算器",
        "h1": "YTM ≈ [C + (F−P)/n] / [(F+P)/2]",
        "h2": "由年息、面值、价格与剩余年限求近似 YTM",
        "intro": "输入年利息 C、面值 F、价格 P 与剩余年限 n，求近似 YTM。",
        "desc": "债券近似 YTM：输入 C、F、P、n，输出 YTM(%)。",
        "inputs": [
            {"id": "C", "label": "年利息 C", "value": "50", "step": "2", "unit": "元"},
            {"id": "F", "label": "面值 F", "value": "1000", "step": "10", "unit": "元"},
            {"id": "P", "label": "价格 P", "value": "950", "step": "10", "unit": "元"},
            {"id": "n", "label": "剩余年限 n", "value": "10", "step": "1", "unit": "年"},
        ],
        "calc": """
            const C=num('C'),F=num('F'),P=num('P'),n=num('n');
            const YTM=(C+(F-P)/n)/((F+P)/2);
            ToolBox.setResult('result', dataGrid([
                [(YTM*100).toFixed(2),'近似到期收益率 YTM (%)']
            ]));
        """,
        "notes": ["近似式忽略现金流时间结构。", "50,(1000−950)/10,均价 975 → 5.64%。"],
    },
    {
        "slug": "yield-spread",
        "industry": "investment",
        "cat": "investment",
        "icon": "git-compare",
        "bg": "from-orange-500 to-amber-600",
        "title": "利差计算器",
        "h1": "Spread = y_bond − y_bench",
        "h2": "由债券收益率与基准收益率求利差",
        "intro": "输入债券收益率与基准收益率，求利差。",
        "desc": "利差：输入 y_bond、y_bench，输出 Spread(基点 bps)。",
        "inputs": [
            {"id": "yb", "label": "债券收益率", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "ybm", "label": "基准收益率", "value": "0.03", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const yb=num('yb'),ybm=num('ybm');
            const sp=(yb-ybm)*10000;
            ToolBox.setResult('result', dataGrid([
                [sp.toFixed(0),'利差 Spread (bps)']
            ]));
        """,
        "notes": ["利差反映信用风险与流动性。", "5%−3% → 200 bps。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
