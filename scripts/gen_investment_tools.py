# -*- coding: utf-8 -*-
"""Batch 35: 投资分析计算深化（14 个公式计算器）。industry=investment（新干净目录）。"""
from tool_template import main

JS = """
function npv(rate, cfs){let s=0; for(let i=0;i<cfs.length;i++) s+=cfs[i]/Math.pow(1+rate,i); return s;}
function irr(cfs){let lo=-0.99, hi=10;
  for(let k=0;k<200;k++){const mid=(lo+hi)/2; if(npv(mid,cfs)>0) lo=mid; else hi=mid;}
  return (lo+hi)/2;}
"""

TOOLS = [
    {
        "slug": "npv-calc", "industry": "investment", "cat": "investment", "icon": "💼", "bg": "#f0fdfa",
        "title": "净现值 (NPV)", "h1": "净现值计算器", "h2": "NPV = Σ CFₜ / (1+r)ᵗ", "intro": "按贴现率折算各期现金流的净现值。",
        "desc": "NPV：输入期初与逐年现金流及贴现率求净现值。",
        "inputs": [
            {"id": "cf0", "label": "期初现金流 CF₀", "value": "-1000", "step": "100"},
            {"id": "cf1", "label": "第1年 CF₁", "value": "300", "step": "50"},
            {"id": "cf2", "label": "第2年 CF₂", "value": "400", "step": "50"},
            {"id": "cf3", "label": "第3年 CF₃", "value": "500", "step": "50"},
            {"id": "cf4", "label": "第4年 CF₄", "value": "200", "step": "50"},
            {"id": "r", "label": "贴现率 r (%)", "value": "10", "step": "0.5"},
        ],
        "calc": JS + """
            const cfs=[num('cf0'),num('cf1'),num('cf2'),num('cf3'),num('cf4')];
            const r=num('r')/100;
            ToolBox.setResult('result', dataGrid([
                [npv(r,cfs).toFixed(2),'净现值 NPV']
            ]));
        """,
        "notes": ["NPV>0 通常可行。", "CF₀ 多为负（初始投资）。"],
    },
    {
        "slug": "irr-calc", "industry": "investment", "cat": "investment", "icon": "📈", "bg": "#f0fdfa",
        "title": "内部收益率 (IRR)", "h1": "内部收益率计算器", "h2": "使 NPV = 0 的贴现率", "intro": "项目自身现金收益率，二分法数值求解。",
        "desc": "IRR：输入期初与逐年现金流求内部收益率。",
        "inputs": [
            {"id": "cf0", "label": "期初现金流 CF₀", "value": "-1000", "step": "100"},
            {"id": "cf1", "label": "第1年 CF₁", "value": "300", "step": "50"},
            {"id": "cf2", "label": "第2年 CF₂", "value": "400", "step": "50"},
            {"id": "cf3", "label": "第3年 CF₃", "value": "500", "step": "50"},
            {"id": "cf4", "label": "第4年 CF₄", "value": "200", "step": "50"},
        ],
        "calc": JS + """
            const cfs=[num('cf0'),num('cf1'),num('cf2'),num('cf3'),num('cf4')];
            ToolBox.setResult('result', dataGrid([
                [(irr(cfs)*100).toFixed(2),'内部收益率 IRR (%)']
            ]));
        """,
        "notes": ["IRR>要求收益率则可行。", "多正根时取常规解。"],
    },
    {
        "slug": "roi-calc", "industry": "investment", "cat": "investment", "icon": "🏆", "bg": "#f0fdfa",
        "title": "投资回报率 (ROI)", "h1": "ROI 计算器", "h2": "ROI = (收益 − 成本) / 成本", "intro": "衡量投资盈利水平的简单比率。",
        "desc": "ROI：输入收益与成本求投资回报率。",
        "inputs": [
            {"id": "gain", "label": "总收益", "value": "1300", "step": "10"},
            {"id": "cost", "label": "总成本", "value": "1000", "step": "10"},
        ],
        "calc": """
            const g=num('gain'),c=num('cost');
            ToolBox.setResult('result', dataGrid([
                [((g-c)/c*100).toFixed(2),'ROI (%)'],
                [(g-c).toFixed(2),'净收益']
            ]));
        """,
        "notes": ["1300/1000 → ROI 30%。", "未考虑时间价值。"],
    },
    {
        "slug": "payback-period", "industry": "investment", "cat": "investment", "icon": "⏱️", "bg": "#f0fdfa",
        "title": "静态投资回收期", "h1": "投资回收期计算器", "h2": "累计现金流由负转正的年限", "intro": "收回初始投资所需的年数。",
        "desc": "回收期：输入期初与逐年现金流求回收期。",
        "inputs": [
            {"id": "cf0", "label": "期初现金流 CF₀", "value": "-1000", "step": "100"},
            {"id": "cf1", "label": "第1年 CF₁", "value": "300", "step": "50"},
            {"id": "cf2", "label": "第2年 CF₂", "value": "400", "step": "50"},
            {"id": "cf3", "label": "第3年 CF₃", "value": "500", "step": "50"},
            {"id": "cf4", "label": "第4年 CF₄", "value": "200", "step": "50"},
        ],
        "calc": """
            const cfs=[num('cf0'),num('cf1'),num('cf2'),num('cf3'),num('cf4')];
            let cum=0, yr=-1;
            for(let i=0;i<cfs.length;i++){cum+=cfs[i]; if(cum>=0 && yr<0){ if(i===0){yr=0;} else {const prev=cum-cfs[i]; yr=i-1+(-prev/cfs[i]);} } }
            ToolBox.setResult('result', dataGrid([
                [yr>=0?yr.toFixed(2)+' 年':'未回收', '静态回收期']
            ]));
        """,
        "notes": ["-1000+300+400+500 → 第3年初回本，约 2.6 年。", "未考虑时间价值。"],
    },
    {
        "slug": "discounted-payback", "industry": "investment", "cat": "investment", "icon": "📉", "bg": "#f0fdfa",
        "title": "动态回收期", "h1": "折现回收期计算器",
        "h2": "累计折现现金流回正年限", "intro": "考虑时间价值的回收期。",
        "desc": "折现回收期：输入现金流与贴现率求折现回收期。",
        "inputs": [
            {"id": "cf0", "label": "期初现金流 CF₀", "value": "-1000", "step": "100"},
            {"id": "cf1", "label": "第1年 CF₁", "value": "300", "step": "50"},
            {"id": "cf2", "label": "第2年 CF₂", "value": "400", "step": "50"},
            {"id": "cf3", "label": "第3年 CF₃", "value": "500", "step": "50"},
            {"id": "r", "label": "贴现率 r (%)", "value": "10", "step": "0.5"},
        ],
        "calc": """
            const cfs=[num('cf0'),num('cf1'),num('cf2'),num('cf3')];
            const r=num('r')/100; let cum=0, yr=-1;
            for(let i=0;i<cfs.length;i++){cum+=cfs[i]/Math.pow(1+r,i); if(cum>=0 && yr<0){ if(i===0)yr=0; else {const prev=cum-cfs[i]/Math.pow(1+r,i); yr=i-1+(-prev/(cfs[i]/Math.pow(1+r,i)));} } }
            ToolBox.setResult('result', dataGrid([
                [yr>=0?yr.toFixed(2)+' 年':'未回收', '折现回收期']
            ]));
        """,
        "notes": ["折现后回收更慢。", "比静态回收期保守。"],
    },
    {
        "slug": "profitability-index", "industry": "investment", "cat": "investment", "icon": "📊", "bg": "#f0fdfa",
        "title": "盈利指数 (PI)", "h1": "盈利指数计算器",
        "h2": "PI = 未来现金流现值 / 初始投资", "intro": "单位投资带来的现值收益。",
        "desc": "盈利指数：输入现金流与贴现率求 PI。",
        "inputs": [
            {"id": "cf0", "label": "期初现金流 CF₀", "value": "-1000", "step": "100"},
            {"id": "cf1", "label": "第1年 CF₁", "value": "300", "step": "50"},
            {"id": "cf2", "label": "第2年 CF₂", "value": "400", "step": "50"},
            {"id": "cf3", "label": "第3年 CF₃", "value": "500", "step": "50"},
            {"id": "r", "label": "贴现率 r (%)", "value": "10", "step": "0.5"},
        ],
        "calc": """
            const cfs=[num('cf0'),num('cf1'),num('cf2'),num('cf3')];
            const r=num('r')/100;
            let pv=0; for(let i=1;i<cfs.length;i++) pv+=cfs[i]/Math.pow(1+r,i);
            const pi=pv/(-cfs[0]);
            ToolBox.setResult('result', dataGrid([
                [pi.toFixed(3),'盈利指数 PI'],
                [(pv).toFixed(2),'未来现金流现值']
            ]));
        """,
        "notes": ["PI>1 项目增值。", "=-PV(of future)/initial。"],
    },
    {
        "slug": "sharpe-ratio", "industry": "investment", "cat": "investment", "icon": "⚖️", "bg": "#f0fdfa",
        "title": "夏普比率", "h1": "夏普比率计算器",
        "h2": "Sharpe = (Rp − Rf) / σp", "intro": "每单位总风险的超额收益。",
        "desc": "夏普比率：输入组合收益、无风险利率与波动率求夏普。",
        "inputs": [
            {"id": "rp", "label": "组合收益率 (%)", "value": "15", "step": "0.5"},
            {"id": "rf", "label": "无风险利率 (%)", "value": "3", "step": "0.5"},
            {"id": "sd", "label": "组合波动率 σ (%)", "value": "10", "step": "0.5"},
        ],
        "calc": """
            const rp=num('rp'),rf=num('rf'),sd=num('sd');
            ToolBox.setResult('result', dataGrid([
                [((rp-rf)/sd).toFixed(3),'夏普比率']
            ]));
        """,
        "notes": ["15%、3%、σ10% → 夏普 1.2。", "越高风险调整后收益越好。"],
    },
    {
        "slug": "sortino-ratio", "industry": "investment", "cat": "investment", "icon": "📉", "bg": "#f0fdfa",
        "title": "索提诺比率", "h1": "索提诺比率计算器",
        "h2": "Sortino = (Rp − Rf) / σd", "intro": "仅用下行波动衡量风险调整收益。",
        "desc": "索提诺比率：输入组合收益、无风险利率与下行标准差求索提诺。",
        "inputs": [
            {"id": "rp", "label": "组合收益率 (%)", "value": "15", "step": "0.5"},
            {"id": "rf", "label": "无风险利率 (%)", "value": "3", "step": "0.5"},
            {"id": "dd", "label": "下行标准差 (%)", "value": "6", "step": "0.5"},
        ],
        "calc": """
            const rp=num('rp'),rf=num('rf'),dd=num('dd');
            ToolBox.setResult('result', dataGrid([
                [((rp-rf)/dd).toFixed(3),'索提诺比率']
            ]));
        """,
        "notes": ["比夏普更看重下行风险。", "分母用下行标准差。"],
    },
    {
        "slug": "holding-period-return", "industry": "investment", "cat": "investment", "icon": "🔁", "bg": "#f0fdfa",
        "title": "持有期收益率", "h1": "持有期收益率计算器",
        "h2": "HPR = (P₁ − P₀ + D) / P₀", "intro": "含股息的期间总回报。",
        "desc": "持有期收益：输入买入价、卖出价与期间股息求收益率。",
        "inputs": [
            {"id": "p0", "label": "买入价 P₀", "value": "100", "step": "1"},
            {"id": "p1", "label": "卖出价 P₁", "value": "120", "step": "1"},
            {"id": "d", "label": "期间股息 D", "value": "4", "step": "0.5"},
        ],
        "calc": """
            const p0=num('p0'),p1=num('p1'),d=num('d');
            ToolBox.setResult('result', dataGrid([
                [((p1-p0+d)/p0*100).toFixed(2),'持有期收益率 (%)'],
                [(p1-p0+d).toFixed(2),'总收益']
            ]));
        """,
        "notes": ["100→120 含息 4 → 24%。", "含价格与分红。"],
    },
    {
        "slug": "dividend-yield", "industry": "investment", "cat": "investment", "icon": "💰", "bg": "#f0fdfa",
        "title": "股息率", "h1": "股息率计算器",
        "h2": "股息率 = 年股息 / 股价", "intro": "每股分红相对于股价的比率。",
        "desc": "股息率：输入年股息与股价求股息率。",
        "inputs": [
            {"id": "dps", "label": "年每股股息", "value": "3", "step": "0.1"},
            {"id": "price", "label": "股价", "value": "60", "step": "1"},
        ],
        "calc": """
            const d=num('dps'),p=num('price');
            ToolBox.setResult('result', dataGrid([
                [(d/p*100).toFixed(2),'股息率 (%)']
            ]));
        """,
        "notes": ["年息 3、股价 60 → 5%。", "与资本利得无关。"],
    },
    {
        "slug": "eps-calc", "industry": "investment", "cat": "investment", "icon": "🧮", "bg": "#f0fdfa",
        "title": "每股收益 (EPS)", "h1": "EPS 计算器",
        "h2": "EPS = (净利润 − 优先股) / 流通股数", "intro": "普通股股东每股享有的盈利。",
        "desc": "EPS：输入净利润、优先股股利与股数求每股收益。",
        "inputs": [
            {"id": "ni", "label": "净利润", "value": "10000000", "step": "100000"},
            {"id": "pref", "label": "优先股股利", "value": "0", "step": "100000"},
            {"id": "shares", "label": "流通股数", "value": "5000000", "step": "100000"},
        ],
        "calc": """
            const ni=num('ni'),pref=num('pref'),s=num('shares');
            ToolBox.setResult('result', dataGrid([
                [((ni-pref)/s).toFixed(2),'每股收益 EPS']
            ]));
        """,
        "notes": ["净利 1000 万、500 万股 → EPS 2.0。", "优先股优先扣除。"],
    },
    {
        "slug": "pe-ratio", "industry": "investment", "cat": "investment", "icon": "📐", "bg": "#f0fdfa",
        "title": "市盈率 (P/E)", "h1": "市盈率计算器",
        "h2": "P/E = 股价 / 每股收益", "intro": "股价相对于盈利的估值倍数。",
        "desc": "市盈率：输入股价与每股收益求 P/E。",
        "inputs": [
            {"id": "price", "label": "股价", "value": "60", "step": "1"},
            {"id": "eps", "label": "每股收益 EPS", "value": "3", "step": "0.1"},
        ],
        "calc": """
            const p=num('price'),e=num('eps');
            ToolBox.setResult('result', dataGrid([
                [(p/e).toFixed(2),'市盈率 P/E']
            ]));
        """,
        "notes": ["股价 60、EPS 3 → P/E 20。", "倍数越高估值越贵。"],
    },
    {
        "slug": "bond-price", "industry": "investment", "cat": "investment", "icon": "📜", "bg": "#f0fdfa",
        "title": "债券定价", "h1": "债券定价计算器",
        "h2": "P = Σ C/(1+y)ᵗ + F/(1+y)ⁿ", "intro": "按到期收益率折现票息与面值。",
        "desc": "债券定价：输入面值、票息率、YTM、年限与付息频率求价格。",
        "inputs": [
            {"id": "face", "label": "面值 F", "value": "1000", "step": "10"},
            {"id": "cr", "label": "票息率 (%)", "value": "5", "step": "0.5"},
            {"id": "ytm", "label": "到期收益率 (%)", "value": "6", "step": "0.5"},
            {"id": "n", "label": "年限 n", "value": "10", "step": "1"},
            {"id": "freq", "label": "年付息次数", "value": "2", "step": "1"},
        ],
        "calc": """
            const F=num('face'),cr=num('cr')/100,ytm=num('ytm')/100,N=num('n'),freq=num('freq');
            const c=F*cr/freq, y=ytm/freq, T=N*freq;
            let p=0; for(let t=1;t<=T;t++) p+=c/Math.pow(1+y,t); p+=F/Math.pow(1+y,T);
            ToolBox.setResult('result', dataGrid([
                [p.toFixed(2),'债券价格 P'],
                [(p>F? '溢价':'折价'),'状态']
            ]));
        """,
        "notes": ["YTM>票息 → 折价。", "半年付息为常见。"],
    },
    {
        "slug": "portfolio-return", "industry": "investment", "cat": "investment", "icon": "🧩", "bg": "#f0fdfa",
        "title": "组合预期收益", "h1": "组合预期收益计算器",
        "h2": "E(Rp) = Σ wᵢ·Rᵢ", "intro": "按权重加总的组合期望收益。",
        "desc": "组合预期收益：输入各资产权重与预期收益求组合收益。",
        "inputs": [
            {"id": "w1", "label": "资产1权重 (%)", "value": "60", "step": "5"},
            {"id": "r1", "label": "资产1收益 (%)", "value": "12", "step": "0.5"},
            {"id": "w2", "label": "资产2权重 (%)", "value": "40", "step": "5"},
            {"id": "r2", "label": "资产2收益 (%)", "value": "8", "step": "0.5"},
        ],
        "calc": """
            const w1=num('w1')/100,w2=num('w2')/100,r1=num('r1'),r2=num('r2');
            const rp=w1*r1+w2*r2;
            ToolBox.setResult('result', dataGrid([
                [rp.toFixed(2),'组合预期收益 (%)'],
                [(w1+w2).toFixed(2),'权重合计']
            ]));
        """,
        "notes": ["60%×12%+40%×8% = 10.4%。", "权重应合计 100%。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
