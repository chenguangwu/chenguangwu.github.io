# -*- coding: utf-8 -*-
"""Batch 61: 光学深化 II（14 个公式计算器）。industry=optics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "optical-power-diopter",
        "industry": "optics",
        "cat": "optics",
        "icon": "zap",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "透镜光焦度(屈光度)计算器",
        "h1": "P = 1 / f",
        "h2": "由焦距求透镜光焦度（屈光度）",
        "intro": "输入焦距 f（米），求光焦度。",
        "desc": "光焦度：输入 f(米)，输出 P(屈光度 D)。",
        "inputs": [
            {"id": "f", "label": "焦距 f", "value": "0.5", "step": "0.05", "unit": "米"},
        ],
        "calc": """
            const f=num('f');
            const P=1/f;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(2),'光焦度 P (D)']
            ]));
        """,
        "notes": ["P 为正为会聚、负为发散。", "f=0.5 m → 2.00 D。"],
    },
    {
        "slug": "angular-magnification",
        "industry": "optics",
        "cat": "optics",
        "icon": "search",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "放大镜角放大率计算器",
        "h1": "M = N / f",
        "h2": "由明视距离与焦距求简单放大镜角放大率",
        "intro": "输入明视距离 N 与放大镜焦距 f，求角放大率。",
        "desc": "放大镜角放大率：输入 N、f，输出 M。",
        "inputs": [
            {"id": "N", "label": "明视距离 N", "value": "250", "step": "10", "unit": "毫米"},
            {"id": "f", "label": "焦距 f", "value": "25", "step": "1", "unit": "毫米"},
        ],
        "calc": """
            const N=num('N'),f=num('f');
            const M=N/f;
            ToolBox.setResult('result', dataGrid([
                [M.toFixed(2),'角放大率 M']
            ]));
        """,
        "notes": ["明视距离通常取 250 mm。", "250/25 → 10×。"],
    },
    {
        "slug": "focal-length-mirror",
        "industry": "optics",
        "cat": "optics",
        "icon": "circle",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "球面镜焦距计算器",
        "h1": "f = R / 2",
        "h2": "由曲率半径求球面镜焦距",
        "intro": "输入球面镜曲率半径 R，求焦距。",
        "desc": "球面镜焦距：输入 R，输出 f。",
        "inputs": [
            {"id": "R", "label": "曲率半径 R", "value": "20", "step": "1", "unit": "厘米"},
        ],
        "calc": """
            const R=num('R');
            const f=R/2;
            ToolBox.setResult('result', dataGrid([
                [f.toFixed(2),'焦距 f (厘米)']
            ]));
        """,
        "notes": ["凹面镜 R、f 取正，凸面镜取负。", "R=20 → f=10。"],
    },
    {
        "slug": "telescope-magnification",
        "industry": "optics",
        "cat": "optics",
        "icon": "telescope",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "望远镜放大率计算器",
        "h1": "M = f_o / f_e",
        "h2": "由物镜与目镜焦距求望远镜放大率",
        "intro": "输入物镜焦距 f_o 与目镜焦距 f_e，求放大率。",
        "desc": "望远镜放大率：输入 f_o、f_e，输出 M。",
        "inputs": [
            {"id": "fo", "label": "物镜焦距 f_o", "value": "1000", "step": "50", "unit": "毫米"},
            {"id": "fe", "label": "目镜焦距 f_e", "value": "25", "step": "1", "unit": "毫米"},
        ],
        "calc": """
            const fo=num('fo'),fe=num('fe');
            const M=fo/fe;
            ToolBox.setResult('result', dataGrid([
                [M.toFixed(2),'放大率 M']
            ]));
        """,
        "notes": ["放大率等于两焦距之比。", "1000/25 → 40×。"],
    },
    {
        "slug": "microscope-magnification",
        "industry": "optics",
        "cat": "optics",
        "icon": "microscope",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "显微镜总放大率计算器",
        "h1": "M = (L · N) / (f_o · f_e)",
        "h2": "由镜筒长、明视距离与两焦距求总放大率",
        "intro": "输入光学筒长 L、明视距离 N、物镜焦距 f_o、目镜焦距 f_e，求总放大率。",
        "desc": "显微镜总放大率：输入 L、N、f_o、f_e，输出 M。",
        "inputs": [
            {"id": "L", "label": "光学筒长 L", "value": "160", "step": "10", "unit": "毫米"},
            {"id": "N", "label": "明视距离 N", "value": "250", "step": "10", "unit": "毫米"},
            {"id": "fo", "label": "物镜焦距 f_o", "value": "10", "step": "1", "unit": "毫米"},
            {"id": "fe", "label": "目镜焦距 f_e", "value": "25", "step": "1", "unit": "毫米"},
        ],
        "calc": """
            const L=num('L'),N=num('N'),fo=num('fo'),fe=num('fe');
            const M=L*N/(fo*fe);
            ToolBox.setResult('result', dataGrid([
                [M.toFixed(1),'总放大率 M']
            ]));
        """,
        "notes": ["近似公式适用于薄透镜组合。", "160×250/(10×25) → 160×。"],
    },
    {
        "slug": "resolving-power",
        "industry": "optics",
        "cat": "optics",
        "icon": "crosshair",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "分辨本领计算器",
        "h1": "R = D / (1.22·λ)",
        "h2": "由孔径与波长求圆形孔径分辨本领",
        "intro": "输入孔径直径 D 与波长 λ（纳米），求分辨本领。",
        "desc": "分辨本领：输入 D(米)、λ(纳米)，输出 R(1/米)。",
        "inputs": [
            {"id": "D", "label": "孔径 D", "value": "0.1", "step": "0.01", "unit": "米"},
            {"id": "lam", "label": "波长 λ", "value": "550", "step": "10", "unit": "纳米"},
        ],
        "calc": """
            const D=num('D'),lam=num('lam')*1e-9;
            const R=D/(1.22*lam);
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(0),'分辨本领 R (1/m)']
            ]));
        """,
        "notes": ["R 越大分辨越细。", "0.1 m,550 nm → 约 1.49×10⁵。"],
    },
    {
        "slug": "prism-deviation",
        "industry": "optics",
        "cat": "optics",
        "icon": "triangle",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "棱镜最小偏向角计算器",
        "h1": "δ ≈ (n − 1)·A",
        "h2": "由折射率与顶角求小角度棱镜偏向角",
        "intro": "输入折射率 n 与棱镜顶角 A（度），求偏向角。",
        "desc": "棱镜偏向角：输入 n、A(度)，输出 δ(度)。",
        "inputs": [
            {"id": "n", "label": "折射率 n", "value": "1.5", "step": "0.01", "unit": ""},
            {"id": "A", "label": "顶角 A", "value": "10", "step": "1", "unit": "度"},
        ],
        "calc": """
            const n=num('n'),A=num('A');
            const delta=(n-1)*A;
            ToolBox.setResult('result', dataGrid([
                [delta.toFixed(2),'偏向角 δ (°)']
            ]));
        """,
        "notes": ["近似式适用于小顶角棱镜。", "(1.5−1)×10 → 5°。"],
    },
    {
        "slug": "separated-lenses-focal",
        "industry": "optics",
        "cat": "optics",
        "icon": "layers",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "分离双透镜组合焦距计算器",
        "h1": "1/F = 1/f₁ + 1/f₂ − d/(f₁f₂)",
        "h2": "由两透镜焦距与间距求组合焦距",
        "intro": "输入两透镜焦距 f₁、f₂ 与间距 d，求组合焦距。",
        "desc": "分离双透镜组合焦距：输入 f1、f2、d，输出 F。",
        "inputs": [
            {"id": "f1", "label": "焦距 f₁", "value": "10", "step": "1", "unit": "厘米"},
            {"id": "f2", "label": "焦距 f₂", "value": "10", "step": "1", "unit": "厘米"},
            {"id": "d", "label": "间距 d", "value": "2", "step": "0.5", "unit": "厘米"},
        ],
        "calc": """
            const f1=num('f1'),f2=num('f2'),d=num('d');
            const invF=1/f1+1/f2-d/(f1*f2);
            const F=1/invF;
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(3),'组合焦距 F (厘米)']
            ]));
        """,
        "notes": ["d→0 退化为密接透镜。", "10,10,2 → 5.556 cm。"],
    },
    {
        "slug": "f-number",
        "industry": "optics",
        "cat": "optics",
        "icon": "aperture",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "光圈数(F 数)计算器",
        "h1": "N = f / D",
        "h2": "由焦距与入瞳直径求光圈数",
        "intro": "输入焦距 f 与入瞳直径 D，求光圈数。",
        "desc": "光圈数 F：输入 f、D，输出 N。",
        "inputs": [
            {"id": "f", "label": "焦距 f", "value": "50", "step": "5", "unit": "毫米"},
            {"id": "D", "label": "入瞳直径 D", "value": "25", "step": "1", "unit": "毫米"},
        ],
        "calc": """
            const f=num('f'),D=num('D');
            const N=f/D;
            ToolBox.setResult('result', dataGrid([
                [N.toFixed(2),'光圈数 N (f/)']
            ]));
        """,
        "notes": ["N 越小进光越多、景深越浅。", "50/25 → f/2.0。"],
    },
    {
        "slug": "thin-film-max",
        "industry": "optics",
        "cat": "optics",
        "icon": "waves",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "薄膜相长干涉波长计算器",
        "h1": "2nt = mλ（垂直入射）",
        "h2": "由膜厚、折射率与级次求相长波长",
        "intro": "输入膜折射率 n、厚度 t（纳米）与级次 m，求相长干涉波长。",
        "desc": "薄膜相长波长：输入 n、t(纳米)、m，输出 λ(纳米)。",
        "inputs": [
            {"id": "n", "label": "膜折射率 n", "value": "1.33", "step": "0.01", "unit": ""},
            {"id": "t", "label": "膜厚 t", "value": "500", "step": "10", "unit": "纳米"},
            {"id": "m", "label": "级次 m", "value": "1", "step": "1", "unit": ""},
        ],
        "calc": """
            const n=num('n'),t=num('t'),m=num('m');
            const lam=2*n*t/m;
            ToolBox.setResult('result', dataGrid([
                [lam.toFixed(1),'相长波长 λ (nm)']
            ]));
        """,
        "notes": ["垂直入射、两相长条件近似。", "n=1.33,t=500,m=1 → 1330 nm。"],
    },
    {
        "slug": "thin-film-min",
        "industry": "optics",
        "cat": "optics",
        "icon": "waves",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "薄膜相消干涉波长计算器",
        "h1": "2nt = (m+½)λ（垂直入射）",
        "h2": "由膜厚、折射率与级次求相消波长",
        "intro": "输入膜折射率 n、厚度 t（纳米）与级次 m，求相消干涉波长。",
        "desc": "薄膜相消波长：输入 n、t(纳米)、m，输出 λ(纳米)。",
        "inputs": [
            {"id": "n", "label": "膜折射率 n", "value": "1.33", "step": "0.01", "unit": ""},
            {"id": "t", "label": "膜厚 t", "value": "500", "step": "10", "unit": "纳米"},
            {"id": "m", "label": "级次 m", "value": "1", "step": "1", "unit": ""},
        ],
        "calc": """
            const n=num('n'),t=num('t'),m=num('m');
            const lam=2*n*t/(m+0.5);
            ToolBox.setResult('result', dataGrid([
                [lam.toFixed(1),'相消波长 λ (nm)']
            ]));
        """,
        "notes": ["肥皂膜呈彩色即薄膜干涉。", "n=1.33,t=500,m=1 → 886.7 nm。"],
    },
    {
        "slug": "young-fringe",
        "industry": "optics",
        "cat": "optics",
        "icon": "align-horizontal-space-between",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "杨氏双缝条纹间距计算器",
        "h1": "Δy = λL / d",
        "h2": "由波长、屏距与缝距求条纹间距",
        "intro": "输入波长 λ（纳米）、屏距 L（米）与缝距 d（毫米），求条纹间距。",
        "desc": "双缝条纹间距：输入 λ(nm)、L(m)、d(mm)，输出 Δy(mm)。",
        "inputs": [
            {"id": "lam", "label": "波长 λ", "value": "550", "step": "10", "unit": "纳米"},
            {"id": "L", "label": "屏距 L", "value": "1", "step": "0.1", "unit": "米"},
            {"id": "d", "label": "缝距 d", "value": "0.5", "step": "0.05", "unit": "毫米"},
        ],
        "calc": """
            const lam=num('lam')*1e-9, L=num('L'), d=num('d')*1e-3;
            const dy=lam*L/d*1000;
            ToolBox.setResult('result', dataGrid([
                [dy.toFixed(3),'条纹间距 Δy (mm)']
            ]));
        """,
        "notes": ["间距与波长成正比、与缝距成反比。", "550 nm,1 m,0.5 mm → 1.1 mm。"],
    },
    {
        "slug": "malus-law",
        "industry": "optics",
        "cat": "optics",
        "icon": "sun",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "马吕斯定律计算器",
        "h1": "I = I₀·cos²θ",
        "h2": "由起偏光强与偏振片夹角求透射光强",
        "intro": "输入入射光强 I₀ 与偏振片夹角 θ（度），求透射光强。",
        "desc": "马吕斯定律：输入 I0、θ(度)，输出 I。",
        "inputs": [
            {"id": "I0", "label": "入射光强 I₀", "value": "100", "step": "5", "unit": ""},
            {"id": "th", "label": "夹角 θ", "value": "60", "step": "5", "unit": "度"},
        ],
        "calc": """
            const I0=num('I0'),th=num('th')*Math.PI/180;
            const I=I0*Math.pow(Math.cos(th),2);
            ToolBox.setResult('result', dataGrid([
                [I.toFixed(2),'透射光强 I']
            ]));
        """,
        "notes": ["θ=90° 时完全消光。", "100,60° → 25.0。"],
    },
    {
        "slug": "doppler-optical",
        "industry": "optics",
        "cat": "optics",
        "icon": "activity",
        "bg": "from-purple-500 to-fuchsia-600",
        "title": "光多普勒频移计算器",
        "h1": "f′ = f·(1 + v/c)",
        "h2": "由源频率、相对速度与光速求观测频率",
        "intro": "输入源频率 f、相对速度 v 与光速 c，求观测频率（近似非相对论）。",
        "desc": "光多普勒：输入 f、v、c，输出 f′。",
        "inputs": [
            {"id": "f", "label": "源频率 f", "value": "5e14", "step": "1e13", "unit": "Hz"},
            {"id": "v", "label": "相对速度 v", "value": "300000", "step": "10000", "unit": "米/秒"},
            {"id": "c", "label": "光速 c", "value": "3e8", "step": "1e7", "unit": "米/秒"},
        ],
        "calc": """
            const f=num('f'),v=num('v'),c=num('c');
            const fp=f*(1+v/c);
            ToolBox.setResult('result', dataGrid([
                [fp.toExponential(3),'观测频率 f′ (Hz)']
            ]));
        """,
        "notes": ["v 取正为靠近（蓝移）。", "5×10¹⁴,3×10⁵,3×10⁸ → 5.005×10¹⁴。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
