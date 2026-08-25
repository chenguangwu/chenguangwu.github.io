# -*- coding: utf-8 -*-
"""Batch 63: 保险学深化 II（14 个公式计算器）。industry=insurance。"""
from tool_template import main

TOOLS = [
    {
        "slug": "expected-claim-loss",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "alert-triangle",
        "bg": "from-rose-500 to-red-600",
        "title": "期望赔付损失计算器",
        "h1": "ECL = 索赔频率 × 平均赔付额",
        "h2": "由索赔频率与平均赔付额求期望损失",
        "intro": "输入单位风险索赔频率与平均赔付额，求期望损失成本。",
        "desc": "期望赔付损失：输入 频率、平均赔付，输出 ECL。",
        "inputs": [
            {"id": "freq", "label": "索赔频率", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "sev", "label": "平均赔付额", "value": "20000", "step": "1000", "unit": "元"},
        ],
        "calc": """
            const freq=num('freq'),sev=num('sev');
            const ECL=freq*sev;
            ToolBox.setResult('result', dataGrid([
                [ECL.toFixed(2),'期望损失 ECL (元)']
            ]));
        """,
        "notes": ["频率×严重度是纯保费基础。", "0.05×20000 → 1000 元。"],
    },
    {
        "slug": "loss-ratio-ins",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "bar-chart",
        "bg": "from-rose-500 to-red-600",
        "title": "赔付率计算器",
        "h1": "LR = 赔款 / 保费",
        "h2": "由赔款支出与保费收入求赔付率",
        "intro": "输入赔款支出与保费收入，求赔付率。",
        "desc": "赔付率：输入 赔款、保费，输出 LR(%)。",
        "inputs": [
            {"id": "loss", "label": "赔款支出", "value": "600", "step": "20", "unit": "元"},
            {"id": "prem", "label": "保费收入", "value": "1000", "step": "50", "unit": "元"},
        ],
        "calc": """
            const loss=num('loss'),prem=num('prem');
            const LR=loss/prem*100;
            ToolBox.setResult('result', dataGrid([
                [LR.toFixed(1),'赔付率 LR (%)']
            ]));
        """,
        "notes": ["赔付率越低承保越盈利。", "600/1000 → 60%。"],
    },
    {
        "slug": "expense-ratio-ins",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "bar-chart",
        "bg": "from-rose-500 to-red-600",
        "title": "费用率计算器",
        "h1": "ER = 费用 / 保费",
        "h2": "由运营费用与保费收入求费用率",
        "intro": "输入运营费用与保费收入，求费用率。",
        "desc": "费用率：输入 费用、保费，输出 ER(%)。",
        "inputs": [
            {"id": "exp", "label": "运营费用", "value": "250", "step": "10", "unit": "元"},
            {"id": "prem", "label": "保费收入", "value": "1000", "step": "50", "unit": "元"},
        ],
        "calc": """
            const exp=num('exp'),prem=num('prem');
            const ER=exp/prem*100;
            ToolBox.setResult('result', dataGrid([
                [ER.toFixed(1),'费用率 ER (%)']
            ]));
        """,
        "notes": ["费用率含佣金与管理费。", "250/1000 → 25%。"],
    },
    {
        "slug": "uw-margin",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "trending-up",
        "bg": "from-rose-500 to-red-600",
        "title": "承保利润率计算器",
        "h1": "承保利润率 = 1 − (赔付率 + 费用率)",
        "h2": "由综合成本率反推承保利润",
        "intro": "输入赔付率与费用率，求承保利润率。",
        "desc": "承保利润率：输入 LR(%)、ER(%)，输出 (%)。",
        "inputs": [
            {"id": "LR", "label": "赔付率 LR", "value": "60", "step": "2", "unit": "%"},
            {"id": "ER", "label": "费用率 ER", "value": "25", "step": "2", "unit": "%"},
        ],
        "calc": """
            const LR=num('LR'),ER=num('ER');
            const m=100-(LR+ER);
            ToolBox.setResult('result', dataGrid([
                [m.toFixed(1),'承保利润率 (%)']
            ]));
        """,
        "notes": ["综合成本率<100% 才承保盈利。", "1−(60+25)% → 15%。"],
    },
    {
        "slug": "pure-premium-rate",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "tag",
        "bg": "from-rose-500 to-red-600",
        "title": "纯费率计算器",
        "h1": "纯费率 = 期望损失 / 风险暴露",
        "h2": "由期望损失与暴露单位求纯费率",
        "intro": "输入期望损失与风险暴露单位数，求纯费率。",
        "desc": "纯费率：输入 期望损失、暴露，输出 纯费率。",
        "inputs": [
            {"id": "el", "label": "期望损失", "value": "1000", "step": "50", "unit": "元"},
            {"id": "exp", "label": "风险暴露", "value": "100", "step": "5", "unit": "单位"},
        ],
        "calc": """
            const el=num('el'),exp=num('exp');
            const ppr=el/exp;
            ToolBox.setResult('result', dataGrid([
                [ppr.toFixed(2),'纯费率 (元/单位)']
            ]));
        """,
        "notes": ["纯费率为风险对价基础。", "1000/100 → 10 元/单位。"],
    },
    {
        "slug": "gross-premium-loading",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "plus",
        "bg": "from-rose-500 to-red-600",
        "title": "毛保费附加计算器",
        "h1": "毛保费 = 纯保费 × (1 + 附加费率)",
        "h2": "由纯保费与附加费率求毛保费",
        "intro": "输入纯保费与附加费率，求毛保费。",
        "desc": "毛保费：输入 纯保费、附加费率，输出 毛保费。",
        "inputs": [
            {"id": "pp", "label": "纯保费", "value": "10", "step": "0.5", "unit": "元"},
            {"id": "load", "label": "附加费率", "value": "0.4", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const pp=num('pp'),load=num('load');
            const gp=pp*(1+load);
            ToolBox.setResult('result', dataGrid([
                [gp.toFixed(2),'毛保费 (元)']
            ]));
        """,
        "notes": ["附加覆盖费用与利润。", "10×1.4 → 14 元。"],
    },
    {
        "slug": "annuity-nsp",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "clock",
        "bg": "from-rose-500 to-red-600",
        "title": "年金净单保费计算器",
        "h1": "NSP = 年给付 × 年金现值因子 a_x",
        "h2": "由年给付与年金因子求净单保费",
        "intro": "输入年给付额与年金现值因子 a_x，求净单保费。",
        "desc": "年金净单保费：输入 年给付、a_x，输出 NSP。",
        "inputs": [
            {"id": "b", "label": "年给付额", "value": "1000", "step": "50", "unit": "元"},
            {"id": "ax", "label": "年金因子 a_x", "value": "15", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const b=num('b'),ax=num('ax');
            const NSP=b*ax;
            ToolBox.setResult('result', dataGrid([
                [NSP.toFixed(2),'净单保费 NSP (元)']
            ]));
        """,
        "notes": ["a_x 由生命表贴现求得。", "1000×15 → 15000 元。"],
    },
    {
        "slug": "force-of-mortality",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "activity",
        "bg": "from-rose-500 to-red-600",
        "title": "死亡力(中心死亡率)计算器",
        "h1": "μ_x = −ln(p_x)",
        "h2": "由一年生存概率求死亡力",
        "intro": "输入一年生存概率 p_x，求死亡力 μ。",
        "desc": "死亡力：输入 p_x，输出 μ。",
        "inputs": [
            {"id": "px", "label": "生存概率 p_x", "value": "0.99", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const px=num('px');
            const mu=-Math.log(px);
            ToolBox.setResult('result', dataGrid([
                [mu.toFixed(5),'死亡力 μ']
            ]));
        """,
        "notes": ["死亡力为瞬时死亡率。", "p_x=0.99 → μ≈0.01005。"],
    },
    {
        "slug": "survival-prob-t",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "heart",
        "bg": "from-rose-500 to-red-600",
        "title": "t 年生存概率计算器",
        "h1": "ₜp_x = l_{x+t} / l_x",
        "h2": "由生存人数求 t 年生存概率",
        "intro": "输入 x+t 岁与 x 岁生存人数，求 t 年生存概率。",
        "desc": "t 年生存概率：输入 l_xt、l_x，输出 ₜp_x。",
        "inputs": [
            {"id": "lxt", "label": "l_{x+t}", "value": "950", "step": "10", "unit": "人"},
            {"id": "lx", "label": "l_x", "value": "1000", "step": "10", "unit": "人"},
        ],
        "calc": """
            const lxt=num('lxt'),lx=num('lx');
            const tpx=lxt/lx;
            ToolBox.setResult('result', dataGrid([
                [tpx.toFixed(4),'t 年生存概率 ₜp_x']
            ]));
        """,
        "notes": ["生命表核心列。", "950/1000 → 0.95。"],
    },
    {
        "slug": "complete-life-expectancy",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "hourglass",
        "bg": "from-rose-500 to-red-600",
        "title": "完全生命期望计算器",
        "h1": "e_x = Σ ₜp_x",
        "h2": "由逐年生存概率序列求完全期望寿命",
        "intro": "输入逐年生存概率序列（逗号或空格分隔），求期望余命。",
        "desc": "完全期望寿命：输入 ₜp_x 列表，输出 e_x。",
        "inputs": [
            {"id": "tpx", "label": "生存概率序列 ₜp_x", "value": "0.95, 0.9, 0.85, 0.8, 0.75", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const raw=document.getElementById('tpx').value.split(/[ ,]+/).filter(Boolean).map(parseFloat);
            let s=0;
            for(const x of raw){ s+=x; }
            ToolBox.setResult('result', dataGrid([
                [s.toFixed(3),'完全期望寿命 e_x']
            ]));
        """,
        "notes": ["近似为生存概率累加。", "0.95+0.9+0.85+0.8+0.75 → 4.25。"],
    },
    {
        "slug": "average-severity",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "divide",
        "bg": "from-rose-500 to-red-600",
        "title": "平均赔付额计算器",
        "h1": "严重度 = 总赔款 / 索赔件数",
        "h2": "由总赔款与索赔件数求平均赔付额",
        "intro": "输入总赔款与索赔件数，求平均赔付额。",
        "desc": "平均赔付额：输入 总赔款、件数，输出 严重度。",
        "inputs": [
            {"id": "tot", "label": "总赔款", "value": "500000", "step": "10000", "unit": "元"},
            {"id": "n", "label": "索赔件数", "value": "25", "step": "1", "unit": "件"},
        ],
        "calc": """
            const tot=num('tot'),n=num('n');
            const sev=tot/n;
            ToolBox.setResult('result', dataGrid([
                [sev.toFixed(2),'平均赔付额 (元)']
            ]));
        """,
        "notes": ["平均赔付额衡量严重度。", "50万/25 → 2 万元。"],
    },
    {
        "slug": "ibnr-estimate",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "clock",
        "bg": "from-rose-500 to-red-600",
        "title": "IBNR 准备金估算器",
        "h1": "IBNR = 终极赔款 × (1 − 已付比例)",
        "h2": "由终极赔款与已付比例估算未决赔款",
        "intro": "输入终极赔款与已付比例，求 IBNR 准备金。",
        "desc": "IBNR 估算：输入 终极赔款、已付比例，输出 IBNR。",
        "inputs": [
            {"id": "ult", "label": "终极赔款", "value": "100000", "step": "5000", "unit": "元"},
            {"id": "paid", "label": "已付比例", "value": "0.7", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const ult=num('ult'),paid=num('paid');
            const ibnr=ult*(1-paid);
            ToolBox.setResult('result', dataGrid([
                [ibnr.toFixed(2),'IBNR 准备金 (元)']
            ]));
        """,
        "notes": ["IBNR 为已发生未报案赔款。", "10万×(1−0.7) → 3 万。"],
    },
    {
        "slug": "surrender-value",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "wallet",
        "bg": "from-rose-500 to-red-600",
        "title": "退保现金价值计算器",
        "h1": "现金价值 = 准备金 × 退保比例",
        "h2": "由保单准备金与退保比例求现金价值",
        "intro": "输入保单准备金与退保比例，求退保现金价值。",
        "desc": "退保现金价值：输入 准备金、退保比例，输出 现金价值。",
        "inputs": [
            {"id": "res", "label": "保单准备金", "value": "50000", "step": "2000", "unit": "元"},
            {"id": "rate", "label": "退保比例", "value": "0.8", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const res=num('res'),rate=num('rate');
            const cv=res*rate;
            ToolBox.setResult('result', dataGrid([
                [cv.toFixed(2),'现金价值 (元)']
            ]));
        """,
        "notes": ["早期退保比例通常较低。", "5万×0.8 → 4 万。"],
    },
    {
        "slug": "premium-elasticity",
        "industry": "insurance",
        "cat": "insurance",
        "icon": "git-compare",
        "bg": "from-rose-500 to-red-600",
        "title": "保费需求弹性计算器",
        "h1": "弹性 = (%Δ需求) / (%Δ保费)",
        "h2": "由需求与保费变动率求弹性",
        "intro": "输入需求量变动率与保费变动率，求需求弹性。",
        "desc": "保费需求弹性：输入 %Δ需求、%Δ保费，输出 弹性。",
        "inputs": [
            {"id": "dq", "label": "需求量变动率", "value": "0.1", "step": "0.01", "unit": ""},
            {"id": "dp", "label": "保费变动率", "value": "0.2", "step": "0.01", "unit": ""},
        ],
        "calc": """
            const dq=num('dq'),dp=num('dp');
            const e=dq/dp;
            ToolBox.setResult('result', dataGrid([
                [e.toFixed(2),'需求弹性']
            ]));
        """,
        "notes": ["弹性<1 为缺乏弹性（刚需）。", "0.1/0.2 → 0.5。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
