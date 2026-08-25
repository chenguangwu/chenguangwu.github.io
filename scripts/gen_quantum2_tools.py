# -*- coding: utf-8 -*-
"""Batch 52: 量子物理深化 II（14 个公式计算器）。industry=quantum。"""
from tool_template import main

TOOLS = [
    {
        "slug": "compton-wavelength",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "waves",
        "bg": "from-violet-500 to-purple-600",
        "title": "康普顿波长计算器",
        "h1": "λ_c = h / (m·c)",
        "h2": "由粒子质量求康普顿波长",
        "intro": "输入粒子质量 m，求康普顿波长。", "desc": "康普顿波长计算器：输入 m，输出 λ_c(pm)。",
        "inputs": [{"id": "m", "label": "质量 m", "value": "9.109e-31", "step": "1e-31", "unit": "kg"}],
        "calc": """
            const h=6.62607015e-34, c=2.99792458e8;
            const m=num('m');
            const lc=h/(m*c);
            ToolBox.setResult('result', dataGrid([
                [(lc*1e12).toFixed(3),'康普顿波长 λ_c (pm)']
            ]));
        """,
        "notes": ["λ_c = h/(mc)。", "电子 m=9.109e-31 → 2.426 pm。"],
    },
    {
        "slug": "energy-time-uncertainty",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "clock",
        "bg": "from-violet-500 to-purple-600",
        "title": "能量-时间不确定关系计算器",
        "h1": "ΔE ≥ ℏ / (2Δt)",
        "h2": "由时间不确定度求能量展宽",
        "intro": "输入时间不确定度 Δt，求最小能量展宽。", "desc": "能量-时间不确定关系：输入 Δt，输出 ΔE(eV)。",
        "inputs": [{"id": "dt", "label": "时间不确定度 Δt", "value": "1e-9", "step": "1e-10", "unit": "s"}],
        "calc": """
            const hbar=1.054571817e-34, e=1.602176634e-19;
            const dt=num('dt');
            const dE=hbar/(2*dt);
            ToolBox.setResult('result', dataGrid([
                [(dE/e).toExponential(3),'能量展宽 ΔE (eV)']
            ]));
        """,
        "notes": ["ΔE·Δt ≥ ℏ/2。", "Δt=1ns → ΔE≈3.3×10⁻⁷ eV。"],
    },
    {
        "slug": "angular-momentum-quant",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "rotate-cw",
        "bg": "from-violet-500 to-purple-600",
        "title": "角动量量子化计算器",
        "h1": "L = n·ℏ",
        "h2": "由主量子数求角动量",
        "intro": "输入量子数 n，求轨道角动量。", "desc": "角动量量子化：输入 n，输出 L(10⁻³⁴ J·s)。",
        "inputs": [{"id": "n", "label": "量子数 n", "value": "3", "step": "1", "unit": ""}],
        "calc": """
            const hbar=1.054571817e-34;
            const n=num('n');
            const L=n*hbar;
            ToolBox.setResult('result', dataGrid([
                [(L*1e34).toFixed(4),'角动量 L (10⁻³⁴ J·s)']
            ]));
        """,
        "notes": ["L = n·ℏ。", "n=3 → 3ℏ。"],
    },
    {
        "slug": "quantum-oscillator-energy",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "activity",
        "bg": "from-violet-500 to-purple-600",
        "title": "量子谐振子能级计算器",
        "h1": "E_n = ℏω(n + ½)",
        "h2": "由能级与频率求能量",
        "intro": "输入能级 n 与频率 f，求谐振子能量。", "desc": "量子谐振子能级：输入 n、f，输出 E(eV)。",
        "inputs": [
            {"id": "n", "label": "能级 n", "value": "2", "step": "1", "unit": ""},
            {"id": "f", "label": "频率 f", "value": "1e14", "step": "1e13", "unit": "Hz"},
        ],
        "calc": """
            const hbar=1.054571817e-34, e=1.602176634e-19;
            const n=num('n'),f=num('f');
            const E=hbar*2*Math.PI*f*(n+0.5);
            ToolBox.setResult('result', dataGrid([
                [(E/e).toFixed(4),'能量 E (eV)']
            ]));
        """,
        "notes": ["E_n = ℏω(n+½)。", "n=2,f=1e14Hz → 约 1.035 eV。"],
    },
    {
        "slug": "stefan-boltzmann-power",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "flame",
        "bg": "from-violet-500 to-purple-600",
        "title": "黑体辐射功率计算器",
        "h1": "P = σ·A·T⁴",
        "h2": "由面积与温度求辐射功率",
        "intro": "输入面积 A 与绝对温度 T，求黑体辐射功率。", "desc": "黑体辐射功率：输入 A、T，输出 P(W)。",
        "inputs": [
            {"id": "A", "label": "面积 A", "value": "0.01", "step": "0.001", "unit": "m²"},
            {"id": "T", "label": "温度 T", "value": "300", "step": "10", "unit": "K"},
        ],
        "calc": """
            const sig=5.670374419e-8;
            const A=num('A'),T=num('T');
            const P=sig*A*Math.pow(T,4);
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(3),'辐射功率 P (W)']
            ]));
        """,
        "notes": ["P = σAT⁴。", "A=0.01,T=300K → 约 4.59 W。"],
    },
    {
        "slug": "fermi-energy-3d",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "box",
        "bg": "from-violet-500 to-purple-600",
        "title": "三维费米能计算器",
        "h1": "E_F = (ℏ²/2m)(3π²n)^{2/3}",
        "h2": "由自由电子密度求费米能",
        "intro": "输入自由电子数密度 n 与有效质量 m，求费米能。", "desc": "三维费米能：输入 n、m，输出 E_F(eV)。",
        "inputs": [
            {"id": "n", "label": "电子密度 n", "value": "8.5e28", "step": "1e27", "unit": "m⁻³"},
            {"id": "m", "label": "有效质量 m", "value": "9.109e-31", "step": "1e-31", "unit": "kg"},
        ],
        "calc": """
            const hbar=1.054571817e-34, e=1.602176634e-19;
            const n=num('n'),m=num('m');
            const EF=Math.pow(hbar,2)/(2*m)*Math.pow(3*Math.PI*Math.PI*n,2/3);
            ToolBox.setResult('result', dataGrid([
                [(EF/e).toFixed(3),'费米能 E_F (eV)']
            ]));
        """,
        "notes": ["E_F = (ℏ²/2m)(3π²n)^{2/3}。", "铜约 7.0 eV。"],
    },
    {
        "slug": "band-gap-photon",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "zap",
        "bg": "from-violet-500 to-purple-600",
        "title": "带隙对应波长计算器",
        "h1": "λ = hc / E_g",
        "h2": "由带隙能量求吸收/发射波长",
        "intro": "输入带隙能量 E_g（eV），求对应光子波长。", "desc": "带隙对应波长：输入 E_g，输出 λ(nm)。",
        "inputs": [{"id": "Eg", "label": "带隙 E_g", "value": "1.12", "step": "0.01", "unit": "eV"}],
        "calc": """
            const h=6.62607015e-34, c=2.99792458e8, e=1.602176634e-19;
            const Eg=num('Eg')*e;
            const lam=h*c/Eg;
            ToolBox.setResult('result', dataGrid([
                [(lam*1e9).toFixed(1),'波长 λ (nm)']
            ]));
        """,
        "notes": ["λ = hc/E_g。", "Si 带隙 1.12eV → 约 1107 nm（红外）。"],
    },
    {
        "slug": "zeeman-splitting",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "split",
        "bg": "from-violet-500 to-purple-600",
        "title": "塞曼分裂能计算器",
        "h1": "ΔE = μ_B·B",
        "h2": "由磁场求相邻能级分裂",
        "intro": "输入磁感应强度 B，求相邻塞曼能级能量差。", "desc": "塞曼分裂能：输入 B，输出 ΔE(eV)。",
        "inputs": [{"id": "B", "label": "磁感应 B", "value": "1", "step": "0.1", "unit": "T"}],
        "calc": """
            const muB=9.2740100783e-24, e=1.602176634e-19;
            const B=num('B');
            const dE=muB*B;
            ToolBox.setResult('result', dataGrid([
                [(dE/e).toExponential(3),'能级分裂 ΔE (eV)']
            ]));
        """,
        "notes": ["ΔE = μ_B·B（Δm_l=±1）。", "B=1T → 约 5.79×10⁻⁵ eV。"],
    },
    {
        "slug": "photoelectric-threshold",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "sun",
        "bg": "from-violet-500 to-purple-600",
        "title": "光电阈频计算器",
        "h1": "f₀ = φ / h",
        "h2": "由逸出功求截止频率",
        "intro": "输入逸出功 φ（eV），求截止频率。", "desc": "光电阈频：输入 φ，输出 f₀(Hz)。",
        "inputs": [{"id": "phi", "label": "逸出功 φ", "value": "4.5", "step": "0.1", "unit": "eV"}],
        "calc": """
            const h=6.62607015e-34, e=1.602176634e-19;
            const phi=num('phi')*e;
            const f0=phi/h;
            ToolBox.setResult('result', dataGrid([
                [f0.toExponential(3),'截止频率 f₀ (Hz)']
            ]));
        """,
        "notes": ["f₀ = φ/h。", "φ=4.5eV → 约 1.09×10¹⁵ Hz。"],
    },
    {
        "slug": "spin-magnetic-moment",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "magnet",
        "bg": "from-violet-500 to-purple-600",
        "title": "电子自旋磁矩计算器",
        "h1": "μ = μ_B · m_l",
        "h2": "由磁量子数求磁矩",
        "intro": "输入磁量子数 m_l，求轨道磁矩（以 μ_B 为单位）。", "desc": "电子自旋磁矩：输入 m_l，输出 μ(μ_B)。",
        "inputs": [{"id": "ml", "label": "磁量子数 m_l", "value": "1", "step": "1", "unit": ""}],
        "calc": """
            const muB=9.2740100783e-24;
            const ml=num('ml');
            const mu=muB*ml;
            ToolBox.setResult('result', dataGrid([
                [ml.toFixed(0),'磁矩 μ (μ_B)'],
                [mu.toExponential(3),'磁矩 μ (J/T)']
            ]));
        """,
        "notes": ["μ = μ_B·m_l，μ_B≈9.274×10⁻²⁴ J/T。", "m_l=1 → 1 μ_B。"],
    },
    {
        "slug": "thermal-de-broglie",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "thermometer",
        "bg": "from-violet-500 to-purple-600",
        "title": "热德布罗意波长计算器",
        "h1": "λ = h / √(2πmkT)",
        "h2": "由温度与质量求热德布罗意波长",
        "intro": "输入质量 m、温度 T，求热德布罗意波长。", "desc": "热德布罗意波长：输入 m、T，输出 λ(nm)。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "9.109e-31", "step": "1e-31", "unit": "kg"},
            {"id": "T", "label": "温度 T", "value": "300", "step": "10", "unit": "K"},
        ],
        "calc": """
            const h=6.62607015e-34, kB=1.380649e-23;
            const m=num('m'),T=num('T');
            const lam=h/Math.sqrt(2*Math.PI*m*kB*T);
            ToolBox.setResult('result', dataGrid([
                [(lam*1e9).toFixed(3),'热德布罗意波长 λ (nm)']
            ]));
        """,
        "notes": ["λ = h/√(2πmkT)。", "电子 300K → 约 4.3 nm。"],
    },
    {
        "slug": "photon-flux",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "zap",
        "bg": "from-violet-500 to-purple-600",
        "title": "光子通量计算器",
        "h1": "N = P·λ / (hc)",
        "h2": "由功率与波长求每秒光子数",
        "intro": "输入光功率 P 与波长 λ，求光子通量。", "desc": "光子通量：输入 P、λ，输出 N(1/s)。",
        "inputs": [
            {"id": "P", "label": "功率 P", "value": "1", "step": "0.1", "unit": "W"},
            {"id": "lam", "label": "波长 λ", "value": "500e-9", "step": "1e-9", "unit": "m"},
        ],
        "calc": """
            const h=6.62607015e-34, c=2.99792458e8;
            const P=num('P'),lam=num('lam');
            const N=P*lam/(h*c);
            ToolBox.setResult('result', dataGrid([
                [N.toExponential(3),'光子通量 N (1/s)']
            ]));
        """,
        "notes": ["N = Pλ/(hc)。", "P=1W,λ=500nm → 2.5×10¹⁸ /s。"],
    },
    {
        "slug": "wavelength-frequency",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "radio",
        "bg": "from-violet-500 to-purple-600",
        "title": "波长-频率换算计算器",
        "h1": "λ = c / f",
        "h2": "由频率求电磁波波长",
        "intro": "输入频率 f，求波长。", "desc": "波长-频率换算：输入 f，输出 λ(nm)。",
        "inputs": [{"id": "f", "label": "频率 f", "value": "5e14", "step": "1e13", "unit": "Hz"}],
        "calc": """
            const c=2.99792458e8;
            const f=num('f');
            const lam=c/f;
            ToolBox.setResult('result', dataGrid([
                [(lam*1e9).toFixed(1),'波长 λ (nm)']
            ]));
        """,
        "notes": ["λ = c/f。", "f=5×10¹⁴Hz → 600 nm（可见光）。"],
    },
    {
        "slug": "boltzmann-population",
        "industry": "quantum",
        "cat": "quantum",
        "icon": "bar-chart",
        "bg": "from-violet-500 to-purple-600",
        "title": "玻尔兹曼布居比计算器",
        "h1": "N₂/N₁ = exp(−ΔE/kT)",
        "h2": "由能级差与温度求粒子数之比",
        "intro": "输入能级差 ΔE（eV）与温度 T，求两能级粒子数比。", "desc": "玻尔兹曼布居比：输入 ΔE、T，输出 N₂/N₁。",
        "inputs": [
            {"id": "dE", "label": "能级差 ΔE", "value": "1", "step": "0.1", "unit": "eV"},
            {"id": "T", "label": "温度 T", "value": "300", "step": "10", "unit": "K"},
        ],
        "calc": """
            const e=1.602176634e-19, kB=1.380649e-23;
            const dE=num('dE')*e, T=num('T');
            const ratio=Math.exp(-dE/(kB*T));
            ToolBox.setResult('result', dataGrid([
                [ratio.toExponential(3),'布居比 N₂/N₁']
            ]));
        """,
        "notes": ["N₂/N₁ = e^(−ΔE/kT)。", "ΔE=1eV,T=300K → 1.6×10⁻¹⁷。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
