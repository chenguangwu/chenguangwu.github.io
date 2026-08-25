# -*- coding: utf-8 -*-
"""Batch 60: 计量学深化 II（14 个公式计算器）。industry=metrology。"""
from tool_template import main

TOOLS = [
    {
        "slug": "std-dev-type-a",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "sigma",
        "bg": "from-teal-500 to-cyan-600",
        "title": "A 类标准不确定度计算器",
        "h1": "u_A = s / √n",
        "h2": "由样本标准差与测量次数求 A 类标准不确定度",
        "intro": "输入样本标准差 s 与测量次数 n，求 A 类标准不确定度。",
        "desc": "A 类标准不确定度：输入 s、n，输出 u_A。",
        "inputs": [
            {"id": "s", "label": "样本标准差 s", "value": "2", "step": "0.1", "unit": ""},
            {"id": "n", "label": "测量次数 n", "value": "9", "step": "1", "unit": "次"},
        ],
        "calc": """
            const s=num('s'),n=num('n');
            const uA=s/Math.sqrt(n);
            ToolBox.setResult('result', dataGrid([
                [uA.toFixed(4),'A 类标准不确定度 u_A']
            ]));
        """,
        "notes": ["u_A = s/√n（多次重复测量）。", "s=2,n=9 → 0.6667。"],
    },
    {
        "slug": "relative-uncertainty",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "percent",
        "bg": "from-teal-500 to-cyan-600",
        "title": "相对不确定度计算器",
        "h1": "u_rel = u / |x|",
        "h2": "由标准不确定度与测得值求相对不确定度",
        "intro": "输入标准不确定度 u 与测得值 x，求相对不确定度。",
        "desc": "相对不确定度：输入 u、x，输出 u_rel(%)。",
        "inputs": [
            {"id": "u", "label": "标准不确定度 u", "value": "0.5", "step": "0.05", "unit": ""},
            {"id": "x", "label": "测得值 x", "value": "10", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const u=num('u'),x=num('x');
            const ur=u/Math.abs(x)*100;
            ToolBox.setResult('result', dataGrid([
                [ur.toFixed(3),'相对不确定度 u_rel (%)']
            ]));
        """,
        "notes": ["相对不确定度便于跨量纲比较。", "u=0.5,x=10 → 5%。"],
    },
    {
        "slug": "uncertainty-propagation-sum",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "plus",
        "bg": "from-teal-500 to-cyan-600",
        "title": "不确定度传播(线性)计算器",
        "h1": "u_c = √(Σ(c_i·u_i)²)",
        "h2": "由灵敏系数与分量标准不确定度求合成不确定度",
        "intro": "输入灵敏系数 c1、c2 与各分量标准不确定度 u1、u2，求合成不确定度。",
        "desc": "线性合成不确定度：输入 c1、u1、c2、u2，输出 u_c。",
        "inputs": [
            {"id": "c1", "label": "灵敏系数 c₁", "value": "1", "step": "0.1", "unit": ""},
            {"id": "u1", "label": "分量 u₁", "value": "0.3", "step": "0.05", "unit": ""},
            {"id": "c2", "label": "灵敏系数 c₂", "value": "1", "step": "0.1", "unit": ""},
            {"id": "u2", "label": "分量 u₂", "value": "0.4", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const c1=num('c1'),u1=num('u1'),c2=num('c2'),u2=num('u2');
            const uc=Math.sqrt(Math.pow(c1*u1,2)+Math.pow(c2*u2,2));
            ToolBox.setResult('result', dataGrid([
                [uc.toFixed(4),'合成标准不确定度 u_c']
            ]));
        """,
        "notes": ["线性函数不确定度传播公式。", "c=1,u1=0.3,u2=0.4 → 0.5。"],
    },
    {
        "slug": "uncertainty-propagation-product",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "x",
        "bg": "from-teal-500 to-cyan-600",
        "title": "不确定度传播(乘积)计算器",
        "h1": "u_y/|y| = √(Σ(u_i/x_i)²)",
        "h2": "由乘积型变量的相对不确定度求合成相对不确定度",
        "intro": "输入变量 x1、x2 及其标准不确定度 u1、u2，求相对合成不确定度。",
        "desc": "乘积相对不确定度：输入 x1、u1、x2、u2，输出 u_y/y(%)。",
        "inputs": [
            {"id": "x1", "label": "变量 x₁", "value": "10", "step": "0.5", "unit": ""},
            {"id": "u1", "label": "u₁", "value": "0.2", "step": "0.02", "unit": ""},
            {"id": "x2", "label": "变量 x₂", "value": "5", "step": "0.5", "unit": ""},
            {"id": "u2", "label": "u₂", "value": "0.1", "step": "0.02", "unit": ""},
        ],
        "calc": """
            const x1=num('x1'),u1=num('u1'),x2=num('x2'),u2=num('u2');
            const ur=Math.sqrt(Math.pow(u1/x1,2)+Math.pow(u2/x2,2))*100;
            ToolBox.setResult('result', dataGrid([
                [ur.toFixed(3),'相对合成不确定度 (%)']
            ]));
        """,
        "notes": ["乘积/商函数用相对不确定度 RSS。", "x1=10,u1=0.2,x2=5,u2=0.1 → 2.83%。"],
    },
    {
        "slug": "effective-dof-welch",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "divide",
        "bg": "from-teal-500 to-cyan-600",
        "title": "有效自由度(Welch)计算器",
        "h1": "ν_eff = (Σu_i²)² / Σ(u_i⁴/ν_i)",
        "h2": "由各分量不确定度与自由度求有效自由度",
        "intro": "输入两组分量不确定度 u、v 及自由度 ν，求有效自由度。",
        "desc": "Welch-Satterthwaite 有效自由度：输入 u1、v1、u2、v2，输出 ν_eff。",
        "inputs": [
            {"id": "u1", "label": "u₁", "value": "1", "step": "0.1", "unit": ""},
            {"id": "v1", "label": "自由度 ν₁", "value": "5", "step": "1", "unit": ""},
            {"id": "u2", "label": "u₂", "value": "2", "step": "0.1", "unit": ""},
            {"id": "v2", "label": "自由度 ν₂", "value": "10", "step": "1", "unit": ""},
        ],
        "calc": """
            const u1=num('u1'),v1=num('v1'),u2=num('u2'),v2=num('v2');
            const ucSum=Math.pow(u1*u1+u2*u2,2);
            const den=u1*u1*u1*u1/v1 + u2*u2*u2*u2/v2;
            const veff=ucSum/den;
            ToolBox.setResult('result', dataGrid([
                [veff.toFixed(2),'有效自由度 ν_eff']
            ]));
        """,
        "notes": ["用于查 t 表确定包含因子。", "u1=1,v1=5,u2=2,v2=10 → 13.9。"],
    },
    {
        "slug": "guard-band-95",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "shield",
        "bg": "from-teal-500 to-cyan-600",
        "title": "保护带(95%)计算器",
        "h1": "GB = 1.65·U",
        "h2": "由扩展不确定度求单侧 95% 保护带",
        "intro": "输入扩展不确定度 U，求 95% 单侧保护带值。",
        "desc": "保护带计算：输入 U，输出 GB。",
        "inputs": [
            {"id": "U", "label": "扩展不确定度 U", "value": "0.5", "step": "0.05", "unit": ""},
        ],
        "calc": """
            const U=num('U');
            const GB=1.65*U;
            ToolBox.setResult('result', dataGrid([
                [GB.toFixed(4),'保护带 GB']
            ]));
        """,
        "notes": ["保护带收窄合格判定限，降低错判风险。", "U=0.5 → 0.825。"],
    },
    {
        "slug": "measurement-cg",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "gauge",
        "bg": "from-teal-500 to-cyan-600",
        "title": "测量能力指数 Cg 计算器",
        "h1": "Cg = (USL − LSL) / (6·s)",
        "h2": "由公差带与测量标准差求测量能力指数",
        "intro": "输入上/下规格限与测量标准差 s，求 Cg。",
        "desc": "测量能力指数 Cg：输入 USL、LSL、s，输出 Cg。",
        "inputs": [
            {"id": "USL", "label": "上限 USL", "value": "10", "step": "0.5", "unit": ""},
            {"id": "LSL", "label": "下限 LSL", "value": "0", "step": "0.5", "unit": ""},
            {"id": "s", "label": "测量标准差 s", "value": "1", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const USL=num('USL'),LSL=num('LSL'),s=num('s');
            const Cg=(USL-LSL)/(6*s);
            ToolBox.setResult('result', dataGrid([
                [Cg.toFixed(3),'测量能力指数 Cg']
            ]));
        """,
        "notes": ["Cg≥1.33 通常表示测量系统合格。", "(10−0)/(6×1) → 1.667。"],
    },
    {
        "slug": "measurement-cgk",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "gauge",
        "bg": "from-teal-500 to-cyan-600",
        "title": "偏移修正能力指数 Cgk 计算器",
        "h1": "Cgk = min(USL−x̄, x̄−LSL) / (3·s)",
        "h2": "由偏倚与标准差求偏移修正能力指数",
        "intro": "输入上下规格限、测量均值与标准差，求 Cgk。",
        "desc": "测量能力指数 Cgk：输入 USL、LSL、x̄、s，输出 Cgk。",
        "inputs": [
            {"id": "USL", "label": "上限 USL", "value": "10", "step": "0.5", "unit": ""},
            {"id": "LSL", "label": "下限 LSL", "value": "0", "step": "0.5", "unit": ""},
            {"id": "xbar", "label": "测量均值 x̄", "value": "5", "step": "0.5", "unit": ""},
            {"id": "s", "label": "测量标准差 s", "value": "1", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const USL=num('USL'),LSL=num('LSL'),xbar=num('xbar'),s=num('s');
            const Cgk=Math.min(USL-xbar,xbar-LSL)/(3*s);
            ToolBox.setResult('result', dataGrid([
                [Cgk.toFixed(3),'偏移修正能力指数 Cgk']
            ]));
        """,
        "notes": ["Cgk 同时考虑偏倚与波动。", "min(5,5)/(3×1) → 1.667。"],
    },
    {
        "slug": "grr-percent",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "percent",
        "bg": "from-teal-500 to-cyan-600",
        "title": "量具重复再现性占比计算器",
        "h1": "%GRR = GRR / 公差 × 100%",
        "h2": "由测量系统误差与公差求 %GRR",
        "intro": "输入测量系统误差 GRR 与公差带，求 %GRR。",
        "desc": "%GRR：输入 GRR、公差，输出 (%)。",
        "inputs": [
            {"id": "GRR", "label": "GRR", "value": "2", "step": "0.1", "unit": ""},
            {"id": "Tol", "label": "公差带", "value": "10", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const GRR=num('GRR'),Tol=num('Tol');
            const p=GRR/Tol*100;
            ToolBox.setResult('result', dataGrid([
                [p.toFixed(1),'%GRR (%)']
            ]));
        """,
        "notes": ["%GRR<10% 测量系统可接受。", "2/10 → 20%。"],
    },
    {
        "slug": "bias-absolute",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "minus",
        "bg": "from-teal-500 to-cyan-600",
        "title": "绝对偏倚计算器",
        "h1": "Bias = x − x_ref",
        "h2": "由测得值与参考值求绝对偏倚",
        "intro": "输入测得值与参考标准值，求绝对偏倚。",
        "desc": "绝对偏倚：输入 x、x_ref，输出 Bias。",
        "inputs": [
            {"id": "x", "label": "测得值 x", "value": "10.2", "step": "0.1", "unit": ""},
            {"id": "xref", "label": "参考值 x_ref", "value": "10", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const x=num('x'),xref=num('xref');
            const bias=x-xref;
            ToolBox.setResult('result', dataGrid([
                [bias.toFixed(3),'绝对偏倚 Bias']
            ]));
        """,
        "notes": ["偏倚反映系统误差方向。", "10.2−10.0 → 0.2。"],
    },
    {
        "slug": "bias-percent",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "percent",
        "bg": "from-teal-500 to-cyan-600",
        "title": "相对偏倚计算器",
        "h1": "Bias% = (x − x_ref) / x_ref × 100%",
        "h2": "由测得值与参考值求相对偏倚",
        "intro": "输入测得值与参考标准值，求相对偏倚。",
        "desc": "相对偏倚：输入 x、x_ref，输出 (%)。",
        "inputs": [
            {"id": "x", "label": "测得值 x", "value": "10.2", "step": "0.1", "unit": ""},
            {"id": "xref", "label": "参考值 x_ref", "value": "10", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const x=num('x'),xref=num('xref');
            const biasp=(x-xref)/xref*100;
            ToolBox.setResult('result', dataGrid([
                [biasp.toFixed(2),'相对偏倚 (%)']
            ]));
        """,
        "notes": ["相对偏倚便于跨量程比较。", "(10.2−10)/10 → 2%。"],
    },
    {
        "slug": "ndc-number",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "hash",
        "bg": "from-teal-500 to-cyan-600",
        "title": "可区分类别数(NDC)计算器",
        "h1": "NDC = 1.41 × PV / GRR",
        "h2": "由零件变差与测量误差求可区分类别数",
        "intro": "输入零件间变差 PV 与测量系统误差 GRR，求 NDC。",
        "desc": "可区分类别数 NDC：输入 PV、GRR，输出 NDC。",
        "inputs": [
            {"id": "PV", "label": "零件变差 PV", "value": "5", "step": "0.5", "unit": ""},
            {"id": "GRR", "label": "GRR", "value": "1", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const PV=num('PV'),GRR=num('GRR');
            const NDC=1.41*PV/GRR;
            ToolBox.setResult('result', dataGrid([
                [NDC.toFixed(2),'可区分类别数 NDC']
            ]));
        """,
        "notes": ["NDC≥5 测量系统可区分零件。", "1.41×5 → 7.05。"],
    },
    {
        "slug": "drift-rate",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "trending-down",
        "bg": "from-teal-500 to-cyan-600",
        "title": "漂移率计算器",
        "h1": "Drift = (x₂ − x₁) / Δt",
        "h2": "由前后两次测得值与时间差求漂移率",
        "intro": "输入前后测得值与时间间隔，求漂移率。",
        "desc": "漂移率：输入 x1、x2、Δt，输出 漂移率。",
        "inputs": [
            {"id": "x1", "label": "初始值 x₁", "value": "10", "step": "0.5", "unit": ""},
            {"id": "x2", "label": "末次值 x₂", "value": "10.5", "step": "0.5", "unit": ""},
            {"id": "dt", "label": "时间间隔 Δt", "value": "30", "step": "1", "unit": "天"},
        ],
        "calc": """
            const x1=num('x1'),x2=num('x2'),dt=num('dt');
            const drift=(x2-x1)/dt;
            ToolBox.setResult('result', dataGrid([
                [drift.toFixed(4),'漂移率 (单位/Δt)']
            ]));
        """,
        "notes": ["正漂移表示测得值随时间增大。", "(10.5−10)/30 → 0.0167。"],
    },
    {
        "slug": "precision-tolerance-ratio",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "scale",
        "bg": "from-teal-500 to-cyan-600",
        "title": "精度公差比(PTR)计算器",
        "h1": "PTR = 6·s / Tol",
        "h2": "由测量标准差与公差带求精度公差比",
        "intro": "输入测量标准差 s 与公差带 Tol，求 PTR。",
        "desc": "精度公差比 PTR：输入 s、Tol，输出 PTR。",
        "inputs": [
            {"id": "s", "label": "测量标准差 s", "value": "0.5", "step": "0.05", "unit": ""},
            {"id": "Tol", "label": "公差带 Tol", "value": "10", "step": "0.5", "unit": ""},
        ],
        "calc": """
            const s=num('s'),Tol=num('Tol');
            const PTR=6*s/Tol;
            ToolBox.setResult('result', dataGrid([
                [PTR.toFixed(3),'精度公差比 PTR']
            ]));
        """,
        "notes": ["PTR<0.1 通常分辨率足够。", "6×0.5/10 → 0.3。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
