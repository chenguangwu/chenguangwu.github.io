# -*- coding: utf-8 -*-
"""Batch 42: 计量学计算深化（14 个公式计算器）。industry=metrology。"""
from tool_template import main

TOOLS = [
    {
        "slug": "type-a-uncertainty",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "bar-chart",
        "bg": "from-cyan-600 to-blue-700",
        "title": "A 类标准不确定度",
        "h1": "A 类不确定度",
        "h2": "u_A = s / √n",
        "intro": "由重复观测统计，u_A = 样本标准差 / √n。",
        "desc": "输入重复测量值（逗号分隔），计算样本标准差与 A 类标准不确定度。",
        "inputs": [
            {"id": "vals", "label": "测量值 (逗号分隔)", "value": "10.02,10.04,9.98,10.01,10.03", "step": "", "unit": ""},
        ],
        "calc": """
            const v=document.getElementById('vals').value.split(',').map(Number);
            const n=v.length, m=v.reduce((a,b)=>a+b,0)/n;
            let s=0; for(let i=0;i<n;i++) s+=(v[i]-m)**2;
            s=Math.sqrt(s/(n-1));
            const uA=s/Math.sqrt(n);
            ToolBox.setResult('result', dataGrid([
                [m.toFixed(4),'平均值'],
                [s.toFixed(4),'样本标准差 s'],
                [uA.toFixed(4),'A类不确定度 u_A']
            ]));
        """,
        "notes": ["基于贝塞尔公式。", "n 越大不确定度越小。"],
    },
    {
        "slug": "type-b-uncertainty",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "shield",
        "bg": "from-cyan-600 to-blue-700",
        "title": "B 类标准不确定度",
        "h1": "B 类不确定度",
        "h2": "u_B = a / k",
        "intro": "由先验信息，u_B = 半宽 a / 包含因子 k。",
        "desc": "输入区间半宽与分布类型（矩形 k=√3、三角 k=√6、正态 k=2/3），计算 B 类不确定度。",
        "inputs": [
            {"id": "a", "label": "区间半宽 a", "value": "0.05", "step": "0.01", "unit": ""},
            {"id": "k", "label": "包含因子 k", "value": "1.732", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const a=num('a'),k=num('k');
            ToolBox.setResult('result', dataGrid([
                [(a/k).toFixed(5),'B类不确定度 u_B'],
                [((a/k)/a*100).toFixed(2),'占比 (%)']
            ]));
        """,
        "notes": ["矩形分布 k=√3≈1.732。", "正态 95% k=1.96/2。"],
    },
    {
        "slug": "combined-uncertainty",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "layers",
        "bg": "from-cyan-600 to-blue-700",
        "title": "合成标准不确定度",
        "h1": "合成不确定度",
        "h2": "u_c = √(Σu_i²)",
        "intro": "各独立分量平方和开方。",
        "desc": "输入各不确定度分量（逗号分隔），计算合成标准不确定度。",
        "inputs": [
            {"id": "us", "label": "分量 u_i (逗号分隔)", "value": "0.02,0.03,0.01", "step": "", "unit": ""},
        ],
        "calc": """
            const u=document.getElementById('us').value.split(',').map(Number);
            let s=0; for(let i=0;i<u.length;i++) s+=u[i]*u[i];
            const uc=Math.sqrt(s);
            ToolBox.setResult('result', dataGrid([
                [uc.toFixed(5),'合成不确定度 u_c'],
                [Math.sqrt(u[0]*u[0]+u[1]*u[1]).toFixed(5),'前两分量合成']
            ]));
        """,
        "notes": ["假设各分量独立。", "含相关系数需加权。"],
    },
    {
        "slug": "expanded-uncertainty",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "maximize",
        "bg": "from-cyan-600 to-blue-700",
        "title": "扩展不确定度",
        "h1": "扩展不确定度",
        "h2": "U = k · u_c",
        "intro": "U = 包含因子 k × 合成不确定度。",
        "desc": "输入合成不确定度与包含因子，计算扩展不确定度及置信水平。",
        "inputs": [
            {"id": "uc", "label": "合成不确定度 u_c", "value": "0.04", "step": "0.005", "unit": ""},
            {"id": "k", "label": "包含因子 k", "value": "2", "step": "0.5", "unit": ""},
            {"id": "meas", "label": "测得值", "value": "10.00", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const uc=num('uc'),k=num('k'),m=num('meas');
            const U=k*uc;
            ToolBox.setResult('result', dataGrid([
                [U.toFixed(4),'扩展不确定度 U'],
                [(m-U).toFixed(4),'下限'],
                [(m+U).toFixed(4),'上限']
            ]));
        """,
        "notes": ["k=2 约 95% 置信。", "报告形式：测得值 ±U。"],
    },
    {
        "slug": "resolution-uncertainty",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "ruler",
        "bg": "from-cyan-600 to-blue-700",
        "title": "分辨率不确定度",
        "h1": "分辨率不确定度",
        "h2": "u = a / (2√3)",
        "intro": "数字显示末位分辨力引入的不确定度。",
        "desc": "输入分辨率（末位步进），按矩形分布计算标准不确定度。",
        "inputs": [
            {"id": "a", "label": "分辨率 a", "value": "0.01", "step": "0.001", "unit": ""},
        ],
        "calc": """
            const a=num('a');
            const u=a/(2*Math.sqrt(3));
            ToolBox.setResult('result', dataGrid([
                [u.toFixed(6),'分辨率不确定度 u'],
                [(u/Math.sqrt(3)).toFixed(6),'半宽/√3 (对比)']
            ]));
        """,
        "notes": ["数字仪器典型处理。", "末位分辨率 a。"],
    },
    {
        "slug": "calibration-uncertainty",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "check-circle",
        "bg": "from-cyan-600 to-blue-700",
        "title": "校准不确定度合成",
        "h1": "校准不确定度",
        "h2": "标准器 + 重复性",
        "intro": "u_cal = √(u_std² + u_rep²)。",
        "desc": "输入标准器不确定度与本次重复性不确定度，合成校准不确定度。",
        "inputs": [
            {"id": "ustd", "label": "标准器不确定度", "value": "0.03", "step": "0.005", "unit": ""},
            {"id": "urep", "label": "重复性不确定度", "value": "0.02", "step": "0.005", "unit": ""},
        ],
        "calc": """
            const s=num('ustd'),r=num('urep');
            const uc=Math.sqrt(s*s+r*r);
            ToolBox.setResult('result', dataGrid([
                [uc.toFixed(5),'校准不确定度 u_c'],
                [(2*uc).toFixed(5),'扩展 U (k=2)']
            ]));
        """,
        "notes": ["校准证书常给出扩展不确定度，需先除以 k。", "各分量独立合成。"],
    },
    {
        "slug": "gauge-repeatability",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "repeat",
        "bg": "from-cyan-600 to-blue-700",
        "title": "量具重复性",
        "h1": "重复性 σ_r",
        "h2": "极差法 R̄/d₂",
        "intro": "重复性标准偏差 = 平均极差 / d₂。",
        "desc": "输入同一零件多次重复测量的极差与测量次数，估算重复性。",
        "inputs": [
            {"id": "r", "label": "极差 R", "value": "0.04", "step": "0.005", "unit": ""},
            {"id": "m", "label": "测量次数", "value": "3", "step": "1", "unit": "次"},
        ],
        "calc": """
            const R=num('r'),m=num('m');
            const d2={2:1.128,3:1.693,4:2.059,5:2.326}[m]||1.693;
            ToolBox.setResult('result', dataGrid([
                [(R/d2).toFixed(4),'重复性 σ_r'],
                [(5.15*R/d2).toFixed(4),'99% 过程带宽 (5.15σ)']
            ]));
        """,
        "notes": ["极差法快速估算。", "d₂ 随测量次数变化。"],
    },
    {
        "slug": "gauge-reproducibility",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "users",
        "bg": "from-cyan-600 to-blue-700",
        "title": "量具再现性",
        "h1": "再现性 σ_o",
        "h2": "不同操作者间差异",
        "intro": "再现性 = 操作者均值极差 / d₂*。",
        "desc": "输入不同操作者平均测量值的极差与操作者数，估算再现性。",
        "inputs": [
            {"id": "r", "label": "操作者均值极差 R₀", "value": "0.05", "step": "0.005", "unit": ""},
            {"id": "o", "label": "操作者数", "value": "3", "step": "1", "unit": "人"},
        ],
        "calc": """
            const R=num('r'),o=num('o');
            const d2s={2:1.128,3:1.693,4:2.059}[o]||1.693;
            ToolBox.setResult('result', dataGrid([
                [(R/d2s).toFixed(4),'再现性 σ_o']
            ]));
        """,
        "notes": ["反映人员间系统差。", "需大于重复性方有意义。"],
    },
    {
        "slug": "grr-study",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "percent",
        "bg": "from-cyan-600 to-blue-700",
        "title": "GRR 研究 (%GRR)",
        "h1": "量具重复再现分析",
        "h2": "%GRR = 6σ_R&R / T",
        "intro": "%GRR = 6√(σ_r²+σ_o²) / 公差 × 100。",
        "desc": "输入重复性与再现性标准偏差及公差，计算量具能力 %GRR。",
        "inputs": [
            {"id": "sr", "label": "重复性 σ_r", "value": "0.02", "step": "0.002", "unit": ""},
            {"id": "so", "label": "再现性 σ_o", "value": "0.015", "step": "0.002", "unit": ""},
            {"id": "tol", "label": "公差 T", "value": "1.0", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const sr=num('sr'),so=num('so'),tol=num('tol');
            const grr=6*Math.sqrt(sr*sr+so*so);
            const pct=grr/tol*100;
            const verdict=pct<10?'可接受':(pct<30?'临界':'不可接受');
            ToolBox.setResult('result', dataGrid([
                [pct.toFixed(1),'%GRR'],
                [grr.toFixed(4),'R&R 带宽 (6σ)'],
                [verdict,'判定']
            ]));
        """,
        "notes": ["%GRR<10% 良好。", "10%–30% 视情况。"],
    },
    {
        "slug": "dimensional-tolerance",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "move-horizontal",
        "bg": "from-cyan-600 to-blue-700",
        "title": "尺寸公差带",
        "h1": "尺寸公差带",
        "h2": "上偏差 − 下偏差",
        "intro": "公差 = 上偏差 − 下偏差，极限尺寸 = 基本尺寸 ± 偏差。",
        "desc": "输入基本尺寸、上偏差与下偏差，计算公差带与极限尺寸。",
        "inputs": [
            {"id": "nom", "label": "基本尺寸", "value": "50", "step": "1", "unit": "mm"},
            {"id": "es", "label": "上偏差 ES", "value": "0.025", "step": "0.005", "unit": "mm"},
            {"id": "ei", "label": "下偏差 EI", "value": "0.0", "step": "0.005", "unit": "mm"},
        ],
        "calc": """
            const n=num('nom'),es=num('es'),ei=num('ei');
            ToolBox.setResult('result', dataGrid([
                [(es-ei).toFixed(3),'公差 (mm)'],
                [(n+es).toFixed(3),'最大极限尺寸 (mm)'],
                [(n+ei).toFixed(3),'最小极限尺寸 (mm)']
            ]));
        """,
        "notes": ["偏差可正可负。", "配合性质由公差带决定。"],
    },
    {
        "slug": "roundness-deviation",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "circle",
        "bg": "from-cyan-600 to-blue-700",
        "title": "圆度误差",
        "h1": "圆度误差",
        "h2": "R_max − R_min",
        "intro": "圆度 = 最大半径 − 最小半径（最小区域法近似）。",
        "desc": "输入截面最大与最小半径，计算圆度误差。",
        "inputs": [
            {"id": "rmax", "label": "最大半径", "value": "25.02", "step": "0.01", "unit": "mm"},
            {"id": "rmin", "label": "最小半径", "value": "24.98", "step": "0.01", "unit": "mm"},
        ],
        "calc": """
            const rmax=num('rmax'),rmin=num('rmin');
            ToolBox.setResult('result', dataGrid([
                [(rmax-rmin).toFixed(3),'圆度误差 (mm)'],
                [((rmax-rmin)*1000).toFixed(1),'圆度误差 (μm)']
            ]));
        """,
        "notes": ["最小区域法为严格定义。", "此处为最大最小近似。"],
    },
    {
        "slug": "flatness-deviation",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "square",
        "bg": "from-cyan-600 to-blue-700",
        "title": "平面度误差",
        "h1": "平面度误差",
        "h2": "最高点 − 最低点",
        "intro": "平面度 = 最高测点 − 最低测点（最小区域法近似）。",
        "desc": "输入平面上最高与最低测点高度，计算平面度误差。",
        "inputs": [
            {"id": "hmax", "label": "最高点", "value": "0.05", "step": "0.005", "unit": "mm"},
            {"id": "hmin", "label": "最低点", "value": "-0.03", "step": "0.005", "unit": "mm"},
        ],
        "calc": """
            const hmax=num('hmax'),hmin=num('hmin');
            ToolBox.setResult('result', dataGrid([
                [(hmax-hmin).toFixed(3),'平面度误差 (mm)'],
                [((hmax-hmin)*1000).toFixed(1),'平面度误差 (μm)']
            ]));
        """,
        "notes": ["最小区域法为严格定义。", "实测需多点采样。"],
    },
    {
        "slug": "least-count-error",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "hash",
        "bg": "from-cyan-600 to-blue-700",
        "title": "分度值引致误差",
        "h1": "分度值误差",
        "h2": "±半分度值",
        "intro": "读数误差约 ± 分度值/2。",
        "desc": "输入量具分度值，估算单次读数极限误差。",
        "inputs": [
            {"id": "lc", "label": "分度值", "value": "0.02", "step": "0.001", "unit": "mm"},
        ],
        "calc": """
            const lc=num('lc');
            ToolBox.setResult('result', dataGrid([
                [(lc/2).toFixed(4),'读数极限误差 (±)'],
                [(-lc/2).toFixed(4),'下限']
            ]));
        """,
        "notes": ["目视估读通常 ±0.5 分度。", "数显量具无此误差。"],
    },
    {
        "slug": "tolerance-stackup-worst",
        "industry": "metrology",
        "cat": "metrology",
        "icon": "layers",
        "bg": "from-cyan-600 to-blue-700",
        "title": "尺寸链最坏情况",
        "h1": "最坏情况累积",
        "h2": "T_total = ΣT_i",
        "intro": "线性尺寸链最坏累积 = 各环公差绝对值之和。",
        "desc": "输入各组成环公差（逗号分隔），计算最坏情况总公差。",
        "inputs": [
            {"id": "ts", "label": "各环公差 (逗号分隔)", "value": "0.1,0.05,0.08,0.02", "step": "", "unit": ""},
        ],
        "calc": """
            const t=document.getElementById('ts').value.split(',').map(Number);
            let sum=0; for(let i=0;i<t.length;i++) sum+=Math.abs(t[i]);
            ToolBox.setResult('result', dataGrid([
                [sum.toFixed(3),'总公差 (最坏) (mm)'],
                [(sum/t.length).toFixed(3),'平均单环 (mm)']
            ]));
        """,
        "notes": ["最坏情况偏保守。", "统计法可用 RSS 替代。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
