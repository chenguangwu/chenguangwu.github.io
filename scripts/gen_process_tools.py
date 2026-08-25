# -*- coding: utf-8 -*-
"""Batch 34: 过程能力/质量计算深化（14 个公式计算器）。industry=process（新干净目录）。"""
from tool_template import main

INV = """
function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+0.3275911*x);
  const y=1-(((((1.061405429*t-1.453152027)*t+1.421413741)*t-0.284496736)*t+0.254829592)*t)*Math.exp(-x*x);
  return s*y;}
function invNorm(p){const a=[-3.969683028665376e+01,2.209460984245205e+02,-2.759285104469687e+02,1.383577518672690e+02,-3.066479806614716e+01,2.506628277459239e+00];
  const b=[-5.447609879822406e+01,1.615858368580409e+02,-1.556989798598866e+02,6.680131188771972e+01,-1.328068155288572e+01];
  const c=[-7.784894002430293e-03,-3.223964580411365e-01,-2.400758277161838e+00,-2.549732539343734e+00,4.374664141464968e+00,2.938163982698783e+00];
  const d=[7.784695709041462e-03,3.224671290700398e-01,2.445134137142996e+00,3.754408661907416e+00];
  const plow=0.02425,phigh=1-plow;let q,r;
  if(p<plow){q=Math.sqrt(-2*Math.log(p));return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);}
  else if(p<=phigh){q=p-0.5;r=q*q;return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q/(((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1);}
  else{q=Math.sqrt(-2*Math.log(1-p));return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5])/((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1);}}
"""

TOOLS = [
    {
        "slug": "cp-index", "industry": "process", "cat": "process", "icon": "📏", "bg": "#ecfeff",
        "title": "过程能力指数 Cp", "h1": "Cp 过程能力计算器",
        "h2": "Cp = (USL − LSL) / (6σ)", "intro": "衡量规格宽度与过程离散程度的比值（不考虑偏移）。",
        "desc": "Cp 计算器：输入上下规格限与过程标准差求 Cp。",
        "inputs": [
            {"id": "usl", "label": "上规格限 USL", "value": "10.05", "step": "0.01"},
            {"id": "lsl", "label": "下规格限 LSL", "value": "9.95", "step": "0.01"},
            {"id": "sigma", "label": "过程标准差 σ", "value": "0.01", "step": "0.001"},
        ],
        "calc": """
            const usl=num('usl'),lsl=num('lsl'),s=num('sigma');
            ToolBox.setResult('result', dataGrid([
                [((usl-lsl)/(6*s)).toFixed(3),'Cp']
            ]));
        """,
        "notes": ["规格 9.95–10.05、σ=0.01 → Cp=1.667。", "Cp≥1.33 通常视为合格。"],
    },
    {
        "slug": "cpk-index", "industry": "process", "cat": "process", "icon": "🎯", "bg": "#ecfeff",
        "title": "过程能力指数 Cpk", "h1": "Cpk 过程能力计算器",
        "h2": "Cpk = min((USL−μ),(μ−LSL)) / (3σ)", "intro": "同时考虑过程中心偏移的能力指数。",
        "desc": "Cpk 计算器：输入规格限、均值与标准差求 Cpk。",
        "inputs": [
            {"id": "usl", "label": "上规格限 USL", "value": "10.05", "step": "0.01"},
            {"id": "lsl", "label": "下规格限 LSL", "value": "9.95", "step": "0.01"},
            {"id": "mu", "label": "过程均值 μ", "value": "10.0", "step": "0.01"},
            {"id": "sigma", "label": "过程标准差 σ", "value": "0.01", "step": "0.001"},
        ],
        "calc": """
            const usl=num('usl'),lsl=num('lsl'),m=num('mu'),s=num('sigma');
            const cpk=Math.min((usl-m)/(3*s),(m-lsl)/(3*s));
            ToolBox.setResult('result', dataGrid([
                [cpk.toFixed(3),'Cpk']
            ]));
        """,
        "notes": ["中心无偏移时 Cpk=Cp。", "Cpk≥1.33 为过程能力充足。"],
    },
    {
        "slug": "pp-index", "industry": "process", "cat": "process", "icon": "📐", "bg": "#ecfeff",
        "title": "过程性能指数 Pp", "h1": "Pp 过程性能计算器",
        "h2": "Pp = (USL − LSL) / (6σ_lt)", "intro": "用长期（总）标准差衡量的性能指数。",
        "desc": "Pp 计算器：输入规格限与长期标准差求 Pp。",
        "inputs": [
            {"id": "usl", "label": "上规格限 USL", "value": "10.05", "step": "0.01"},
            {"id": "lsl", "label": "下规格限 LSL", "value": "9.95", "step": "0.01"},
            {"id": "slt", "label": "长期标准差 σ_lt", "value": "0.015", "step": "0.001"},
        ],
        "calc": """
            const usl=num('usl'),lsl=num('lsl'),s=num('slt');
            ToolBox.setResult('result', dataGrid([
                [((usl-lsl)/(6*s)).toFixed(3),'Pp']
            ]));
        """,
        "notes": ["Pp 用整体标准差，含特殊原因。", "Pp 常低于 Cp。"],
    },
    {
        "slug": "ppk-index", "industry": "process", "cat": "process", "icon": "📊", "bg": "#ecfeff",
        "title": "过程性能指数 Ppk", "h1": "Ppk 过程性能计算器",
        "h2": "Ppk = min((USL−μ),(μ−LSL)) / (3σ_lt)", "intro": "考虑偏移的长期过程性能指数。",
        "desc": "Ppk 计算器：输入规格限、均值与长期标准差求 Ppk。",
        "inputs": [
            {"id": "usl", "label": "上规格限 USL", "value": "10.05", "step": "0.01"},
            {"id": "lsl", "label": "下规格限 LSL", "value": "9.95", "step": "0.01"},
            {"id": "mu", "label": "过程均值 μ", "value": "10.0", "step": "0.01"},
            {"id": "slt", "label": "长期标准差 σ_lt", "value": "0.015", "step": "0.001"},
        ],
        "calc": """
            const usl=num('usl'),lsl=num('lsl'),m=num('mu'),s=num('slt');
            ToolBox.setResult('result', dataGrid([
                [Math.min((usl-m)/(3*s),(m-lsl)/(3*s)).toFixed(3),'Ppk']
            ]));
        """,
        "notes": ["Ppk 含长期变异与偏移。", "Ppk≥1.33 视为性能充足。"],
    },
    {
        "slug": "sigma-level", "industry": "process", "cat": "process", "icon": "🏅", "bg": "#ecfeff",
        "title": "西格玛水平", "h1": "西格玛水平计算器",
        "h2": "Z_bench = Φ⁻¹(1 − DPMO/10⁶) + 1.5", "intro": "由百万缺陷机会数换算长期西格玛水平。",
        "desc": "西格玛水平：输入 DPMO 求 Z 基准与西格玛水平。",
        "inputs": [
            {"id": "dpmo", "label": "DPMO", "value": "6210", "step": "10"},
        ],
        "calc": INV + """
            const d=num('dpmo');
            const y=1-d/1e6;
            const zb=invNorm(y);
            ToolBox.setResult('result', dataGrid([
                [zb.toFixed(3),'Z_bench'],
                [(zb+1.5).toFixed(2),'西格玛水平 (1.5σ 偏移)']
            ]));
        """,
        "notes": ["6σ 对应 DPMO≈3.4。", "DPMO 6210 ≈ 4σ。"],
    },
    {
        "slug": "dpmo-calc", "industry": "process", "cat": "process", "icon": "🔢", "bg": "#ecfeff",
        "title": "DPMO 计算", "h1": "DPMO 计算器",
        "h2": "DPMO = 缺陷数 / (单位数 × 机会数) × 10⁶", "intro": "每百万机会缺陷数，过程质量通用度量。",
        "desc": "DPMO：输入缺陷数、单位数与每单位机会数求 DPMO。",
        "inputs": [
            {"id": "def", "label": "缺陷数", "value": "124", "step": "1"},
            {"id": "units", "label": "单位数", "value": "2000", "step": "10"},
            {"id": "opp", "label": "每单位机会数", "value": "10", "step": "1"},
        ],
        "calc": """
            const d=num('def'),u=num('units'),o=num('opp');
            ToolBox.setResult('result', dataGrid([
                [(d/(u*o)*1e6).toFixed(1),'DPMO']
            ]));
        """,
        "notes": ["124/20000×1e6 = 6200 DPMO。", "机会数指可缺陷的特征数。"],
    },
    {
        "slug": "first-pass-yield", "industry": "process", "cat": "process", "icon": "✅", "bg": "#ecfeff",
        "title": "一次通过率 (FPY)", "h1": "一次通过率计算器",
        "h2": "FPY = 良品数 / 投入数 × 100%", "intro": "未经返修首次即合格的比例。",
        "desc": "一次通过率：输入良品数与投入数求 FPY。",
        "inputs": [
            {"id": "good", "label": "良品数", "value": "950", "step": "1"},
            {"id": "total", "label": "投入数", "value": "1000", "step": "1"},
        ],
        "calc": """
            const g=num('good'),t=num('total');
            ToolBox.setResult('result', dataGrid([
                [(g/t*100).toFixed(2),'一次通过率 (%)']
            ]));
        """,
        "notes": ["950/1000 = 95% FPY。", "返修后合格不计入 FPY。"],
    },
    {
        "slug": "rolled-throughput-yield", "industry": "process", "cat": "process", "icon": "🔗", "bg": "#ecfeff",
        "title": "流通合格率 (RTY)", "h1": "流通合格率计算器",
        "h2": "RTY = Y₁ × Y₂ × … × Yₙ", "intro": "多工序串联时整体一次合格率。",
        "desc": "流通合格率：输入各工序合格率求整体 RTY。",
        "inputs": [
            {"id": "y1", "label": "工序1良率 (%)", "value": "98", "step": "0.5"},
            {"id": "y2", "label": "工序2良率 (%)", "value": "97", "step": "0.5"},
            {"id": "y3", "label": "工序3良率 (%)", "value": "99", "step": "0.5"},
        ],
        "calc": """
            const y1=num('y1')/100,y2=num('y2')/100,y3=num('y3')/100;
            ToolBox.setResult('result', dataGrid([
                [(y1*y2*y3*100).toFixed(2),'RTY (%)'],
                [(y1*y2*y3).toFixed(4),'RTY (小数)']
            ]));
        """,
        "notes": ["98%×97%×99% ≈ 94.11%。", "工序越多 RTY 越低。"],
    },
    {
        "slug": "xbar-control-limits", "industry": "process", "cat": "process", "icon": "📈", "bg": "#ecfeff",
        "title": "均值控制图界限", "h1": "X̄ 控制图界限计算器",
        "h2": "UCL/LCL = x̄̄ ± 3σ/√n", "intro": "子组均值控制图的 3σ 控制界限。",
        "desc": "均值控制限：输入总均值、标准差与子组大小求上下限。",
        "inputs": [
            {"id": "mean", "label": "总均值 x̄̄", "value": "50", "step": "0.1"},
            {"id": "sigma", "label": "标准差 σ", "value": "2", "step": "0.1"},
            {"id": "n", "label": "子组大小 n", "value": "5", "step": "1"},
        ],
        "calc": """
            const m=num('mean'),s=num('sigma'),n=num('n');
            const se=s/Math.sqrt(n);
            ToolBox.setResult('result', dataGrid([
                [(m+3*se).toFixed(3),'UCL'],
                [(m-3*se).toFixed(3),'LCL'],
                [m.toFixed(3),'中心线 CL']
            ]));
        """,
        "notes": ["50、σ=2、n=5 → 界限 ±2.683。", "σ/√n 为均值标准误。"],
    },
    {
        "slug": "cpk-with-shift", "industry": "process", "cat": "process", "icon": "↔️", "bg": "#ecfeff",
        "title": "偏移后 Cpk", "h1": "偏移后 Cpk 计算器",
        "h2": "Cpk = min((USL−(μ+δ)),((μ+δ)−LSL)) / (3σ)", "intro": "过程均值相对中心偏移 δ 后的能力。",
        "desc": "偏移后 Cpk：输入规格限、标称中心、偏移量与 σ 求 Cpk。",
        "inputs": [
            {"id": "usl", "label": "上规格限 USL", "value": "10.05", "step": "0.01"},
            {"id": "lsl", "label": "下规格限 LSL", "value": "9.95", "step": "0.01"},
            {"id": "nominal", "label": "标称中心", "value": "10.0", "step": "0.01"},
            {"id": "shift", "label": "偏移量 δ", "value": "0.02", "step": "0.005"},
            {"id": "sigma", "label": "过程标准差 σ", "value": "0.01", "step": "0.001"},
        ],
        "calc": """
            const usl=num('usl'),lsl=num('lsl'),nom=num('nominal'),d=num('shift'),s=num('sigma');
            const mu=nom+d;
            ToolBox.setResult('result', dataGrid([
                [Math.min((usl-mu)/(3*s),(mu-lsl)/(3*s)).toFixed(3),'Cpk (偏移后)'],
                [mu.toFixed(4),'实际均值 μ']
            ]));
        """,
        "notes": ["偏移使 Cpk 下降。", "δ=0 时回到原 Cpk。"],
    },
    {
        "slug": "tolerance-worst-case", "industry": "process", "cat": "process", "icon": "🧩", "bg": "#ecfeff",
        "title": "公差叠加（最差情况）", "h1": "公差叠加计算器（最差）",
        "h2": "T_total = Σ |tᵢ|", "intro": "线性尺寸链在最差情况下的总公差。",
        "desc": "公差最差叠加：输入各零件公差求总公差。",
        "inputs": [
            {"id": "t1", "label": "公差1 t₁", "value": "0.1", "step": "0.01"},
            {"id": "t2", "label": "公差2 t₂", "value": "0.15", "step": "0.01"},
            {"id": "t3", "label": "公差3 t₃", "value": "0.2", "step": "0.01"},
        ],
        "calc": """
            const t1=num('t1'),t2=num('t2'),t3=num('t3');
            ToolBox.setResult('result', dataGrid([
                [(t1+t2+t3).toFixed(3),'总公差 (最差)']
            ]));
        """,
        "notes": ["0.1+0.15+0.2 = 0.45。", "最差情况偏保守。"],
    },
    {
        "slug": "tolerance-rss", "industry": "process", "cat": "process", "icon": "📐", "bg": "#ecfeff",
        "title": "公差叠加（统计 RSS）", "h1": "公差叠加计算器（RSS）",
        "h2": "T = √(Σ tᵢ²)", "intro": "用均方根法估计线性尺寸链的统计总公差。",
        "desc": "公差 RSS 叠加：输入各零件公差求统计总公差。",
        "inputs": [
            {"id": "t1", "label": "公差1 t₁", "value": "0.1", "step": "0.01"},
            {"id": "t2", "label": "公差2 t₂", "value": "0.15", "step": "0.01"},
            {"id": "t3", "label": "公差3 t₃", "value": "0.2", "step": "0.01"},
        ],
        "calc": """
            const t1=num('t1'),t2=num('t2'),t3=num('t3');
            ToolBox.setResult('result', dataGrid([
                [Math.sqrt(t1*t1+t2*t2+t3*t3).toFixed(3),'总公差 (RSS)']
            ]));
        """,
        "notes": ["√(0.01+0.0225+0.04)=√0.0725≈0.269。", "RSS 比最差情况宽松。"],
    },
    {
        "slug": "defect-probability", "industry": "process", "cat": "process", "icon": "⚠️", "bg": "#ecfeff",
        "title": "超规格概率", "h1": "超规格概率计算器",
        "h2": "P(X>USL) = 1 − Φ((USL−μ)/σ)", "intro": "正态假设下超出上规格限的概率。",
        "desc": "超规格概率：输入规格限、均值与 σ 求缺陷概率。",
        "inputs": [
            {"id": "usl", "label": "上规格限 USL", "value": "10.05", "step": "0.01"},
            {"id": "mu", "label": "过程均值 μ", "value": "10.0", "step": "0.01"},
            {"id": "sigma", "label": "过程标准差 σ", "value": "0.01", "step": "0.001"},
        ],
        "calc": """
            function erf(x){const s=x<0?-1:1;x=Math.abs(x);const t=1/(1+0.3275911*x);
              const y=1-(((((1.061405429*t-1.453152027)*t+1.421413741)*t-0.284496736)*t+0.254829592)*t)*Math.exp(-x*x);
              return s*y;}
            const usl=num('usl'),m=num('mu'),s=num('sigma');
            const z=(usl-m)/s;
            const p=1-0.5*(1+erf(z/Math.SQRT2));
            ToolBox.setResult('result', dataGrid([
                [(p*100).toFixed(4),'超上规格概率 (%)'],
                [(p*1e6).toFixed(1),'对应 DPMO']
            ]));
        """,
        "notes": ["z=5 → 概率约 2.87e-7。", "对称时总缺陷为两侧之和。"],
    },
    {
        "slug": "measurement-uncertainty", "industry": "process", "cat": "process", "icon": "🔬", "bg": "#ecfeff",
        "title": "合成测量不确定度", "h1": "合成不确定度计算器",
        "h2": "u_c = √(u₁² + u₂² + …)", "intro": "多个独立不确定度分量的合成（RSS）。",
        "desc": "合成不确定度：输入各分量求合成标准不确定度。",
        "inputs": [
            {"id": "u1", "label": "分量1 u₁", "value": "0.5", "step": "0.05"},
            {"id": "u2", "label": "分量2 u₂", "value": "0.3", "step": "0.05"},
            {"id": "u3", "label": "分量3 u₃", "value": "0.2", "step": "0.05"},
        ],
        "calc": """
            const u1=num('u1'),u2=num('u2'),u3=num('u3');
            ToolBox.setResult('result', dataGrid([
                [Math.sqrt(u1*u1+u2*u2+u3*u3).toFixed(4),'合成不确定度 u_c']
            ]));
        """,
        "notes": ["√(0.25+0.09+0.04)=√0.38≈0.616。", "分量应相互独立。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
