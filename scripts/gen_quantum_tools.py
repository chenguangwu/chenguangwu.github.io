# -*- coding: utf-8 -*-
"""Batch 24: 量子物理计算深化（14 个公式计算器）。industry=quantum。"""
from tool_template import main

# 物理常数（注入到每页 calc JS 中，浏览器端可用）
CONSTS = ("const H=6.62607015e-34,C=299792458,ME=9.10938356e-31,EV=1.602176634e-19,"
          "A0=5.291772109e-11,RY=1.0973731568e7,B_WIEN=2.897771955e-3;")

TOOLS = [
    {
        "slug": "photon-energy", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "光子能量", "h1": "光子能量计算器",
        "h2": "E = h·f = h·c / λ",
        "intro": "由频率或波长求光子能量。",
        "desc": "光子能量计算器：E = h·c/λ，输入波长。",
        "inputs": [
            {"id": "lam", "label": "波长 λ", "value": "500e-9", "step": "10e-9", "unit": "m"},
        ],
        "calc": """
            const lam = num('lam');
            const E = H * C / lam;
            ToolBox.setResult('result', dataGrid([
                [E.toExponential(3), '能量 E (J)'],
                [(E / EV).toFixed(3), 'E (eV)']
            ]));
        """,
        "notes": ["E = hc/λ。", "500 nm 可见光 ≈ 2.48 eV。"],
    },
    {
        "slug": "photon-momentum", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "光子动量", "h1": "光子动量计算器",
        "h2": "p = h / λ",
        "intro": "光子的相对论动量。",
        "desc": "光子动量计算器：p = h/λ，输入波长。",
        "inputs": [
            {"id": "lam", "label": "波长 λ", "value": "500e-9", "step": "10e-9", "unit": "m"},
        ],
        "calc": """
            const lam = num('lam');
            const p = H / lam;
            ToolBox.setResult('result', dataGrid([
                [p.toExponential(3), '动量 p (kg·m/s)']
            ]));
        """,
        "notes": ["p = h/λ。", "光子静质量为零但具动量。"],
    },
    {
        "slug": "de-broglie-wavelength", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "德布罗意波长", "h1": "德布罗意波长计算器",
        "h2": "λ = h / (m·v)",
        "intro": "物质波的波长与动量关系。",
        "desc": "德布罗意波长计算器：λ = h/(mv)，输入质量与速度。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "9.11e-31", "step": "1e-31", "unit": "kg"},
            {"id": "v", "label": "速度 v", "value": "1e6", "step": "1e5", "unit": "m/s"},
        ],
        "calc": """
            const m = num('m'), v = num('v');
            const lam = H / (m * v);
            ToolBox.setResult('result', dataGrid([
                [lam.toExponential(3), '波长 λ (m)'],
                [(lam * 1e9).toFixed(4), 'λ (nm)']
            ]));
        """,
        "notes": ["λ = h/(mv)。", "电子 1e6 m/s → λ ≈ 0.73 nm。"],
    },
    {
        "slug": "photoelectric-effect", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "光电效应", "h1": "光电效应计算器",
        "h2": "K_max = h·f − φ",
        "intro": "光电子最大初动能等于光子能量减功函数。",
        "desc": "光电效应计算器：K_max = hf − φ。",
        "inputs": [
            {"id": "f", "label": "频率 f", "value": "1.0e15", "step": "1e14", "unit": "Hz"},
            {"id": "phi", "label": "功函数 φ", "value": "2.0", "step": "0.1", "unit": "eV"},
        ],
        "calc": """
            const f = num('f'), phi = num('phi') * EV;
            const K = H * f - phi;
            ToolBox.setResult('result', dataGrid([
                [K.toExponential(3), '最大动能 K (J)'],
                [(K / EV).toFixed(3), 'K (eV)'],
                [K > 0 ? '能逸出' : '不能逸出（hf<φ）', '判定']
            ]));
        """,
        "notes": ["K_max = hf − φ。", "f 需 > φ/h 才逸出。"],
    },
    {
        "slug": "compton-shift", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "康普顿散射位移", "h1": "康普顿散射位移计算器",
        "h2": "Δλ = (h / m_e·c)·(1 − cosθ)",
        "intro": "X 射线散射后波长改变量。",
        "desc": "康普顿位移：Δλ = h/(m_e c)(1−cosθ)，输入散射角。",
        "inputs": [
            {"id": "th", "label": "散射角 θ", "value": "90", "step": "5", "unit": "°"},
        ],
        "calc": """
            const th = num('th') * Math.PI / 180;
            const dl = (H / (ME * C)) * (1 - Math.cos(th));
            ToolBox.setResult('result', dataGrid([
                [(dl * 1e12).toFixed(4), 'Δλ (pm)'],
                [(dl * 1e9).toFixed(5), 'Δλ (nm)']
            ]));
        """,
        "notes": ["λ_C = h/(m_e c) ≈ 2.43 pm。", "90° 散射 Δλ ≈ 2.43 pm。"],
    },
    {
        "slug": "rydberg-wavelength", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "里德伯公式", "h1": "里德伯波长计算器",
        "h2": "1/λ = R·(1/n₁² − 1/n₂²)",
        "intro": "氢原子谱线波长。",
        "desc": "里德伯公式：1/λ = R(1/n₁²−1/n₂²)，输入能级 n₁,n₂。",
        "inputs": [
            {"id": "n1", "label": "低能级 n₁", "value": "2", "step": "1"},
            {"id": "n2", "label": "高能级 n₂", "value": "3", "step": "1"},
        ],
        "calc": """
            let n1 = Math.round(num('n1')), n2 = Math.round(num('n2'));
            if (n1 > n2) { const t = n1; n1 = n2; n2 = t; }
            const inv = RY * (1/(n1*n1) - 1/(n2*n2));
            ToolBox.setResult('result', dataGrid([
                [inv.toExponential(3), '波数 1/λ (m⁻¹)'],
                [((1/inv) * 1e9).toFixed(2), '波长 λ (nm)']
            ]));
        """,
        "notes": ["里德伯常量 R≈1.097e7 m⁻¹。", "n:3→2 为巴耳末 α 线 ≈ 656 nm。"],
    },
    {
        "slug": "hydrogen-energy-level", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "氢原子能级", "h1": "氢原子能级计算器",
        "h2": "E_n = −13.6 eV / n²",
        "intro": "氢原子第 n 能级能量。",
        "desc": "氢原子能级：E_n = −13.6/n² eV，输入主量子数 n。",
        "inputs": [
            {"id": "n", "label": "主量子数 n", "value": "2", "step": "1"},
        ],
        "calc": """
            const n = Math.round(num('n'));
            const E = -13.6 / (n * n);
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(4), '能级 E_n (eV)']
            ]));
        """,
        "notes": ["E_n = −13.6/n² eV。", "基态 n=1 → −13.6 eV。"],
    },
    {
        "slug": "bohr-orbit-radius", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "玻尔轨道半径", "h1": "玻尔轨道半径计算器",
        "h2": "r_n = a₀ · n²",
        "intro": "氢原子第 n 轨道半径。",
        "desc": "玻尔半径：r_n = a₀·n²，输入主量子数 n。",
        "inputs": [
            {"id": "n", "label": "主量子数 n", "value": "1", "step": "1"},
        ],
        "calc": """
            const n = Math.round(num('n'));
            const r = A0 * n * n;
            ToolBox.setResult('result', dataGrid([
                [(r * 1e10).toFixed(4), '轨道半径 r_n (Å)'],
                [(r * 1e9).toFixed(4), 'r_n (nm)']
            ]));
        """,
        "notes": ["a₀ ≈ 0.529 Å。", "n=1 基态半径 0.529 Å。"],
    },
    {
        "slug": "heisenberg-uncertainty", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "海森堡不确定性", "h1": "海森堡不确定性计算器",
        "h2": "Δx·Δp ≥ ħ / 2",
        "intro": "位置与动量不确定度的乘积下限。",
        "desc": "不确定性原理：Δx·Δp ≥ ħ/2，输入位置不确定度求动量下限。",
        "inputs": [
            {"id": "dx", "label": "位置不确定度 Δx", "value": "1e-10", "step": "1e-11", "unit": "m"},
        ],
        "calc": """
            const dx = num('dx');
            const hbar = H / (2 * Math.PI);
            const dp = hbar / (2 * dx);
            ToolBox.setResult('result', dataGrid([
                [dp.toExponential(3), '动量不确定度 Δp (kg·m/s)'],
                [(dp / ME).toExponential(3), '等效速度不确定 (m/s)']
            ]));
        """,
        "notes": ["Δx·Δp ≥ ħ/2。", "ħ = h/(2π)。"],
    },
    {
        "slug": "mass-energy-equivalence", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "质能等价", "h1": "质能等价计算器",
        "h2": "E = m·c²",
        "intro": "质量对应的能量。",
        "desc": "质能等价：E = mc²，输入质量。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "1", "step": "0.1", "unit": "kg"},
        ],
        "calc": """
            const m = num('m');
            const E = m * C * C;
            ToolBox.setResult('result', dataGrid([
                [E.toExponential(3), '能量 E (J)'],
                [(E / EV / 1e6).toExponential(3), 'E (MeV)']
            ]));
        """,
        "notes": ["E = mc²。", "1 kg 对应 9e16 J。"],
    },
    {
        "slug": "infinite-well-energy", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "一维无限深势阱", "h1": "无限深势阱能级计算器",
        "h2": "E_n = n²·h² / (8·m·L²)",
        "intro": "粒子在一维势阱中的能级。",
        "desc": "无限深势阱：E_n = n²h²/(8mL²)，输入质量、阱宽、量子数。",
        "inputs": [
            {"id": "n", "label": "量子数 n", "value": "1", "step": "1"},
            {"id": "m", "label": "粒子质量 m", "value": "9.11e-31", "step": "1e-31", "unit": "kg"},
            {"id": "L", "label": "阱宽 L", "value": "1e-9", "step": "1e-10", "unit": "m"},
        ],
        "calc": """
            const n = Math.round(num('n')), m = num('m'), L = num('L');
            const E = n * n * H * H / (8 * m * L * L);
            ToolBox.setResult('result', dataGrid([
                [E.toExponential(3), '能级 E_n (J)'],
                [(E / EV).toFixed(4), 'E_n (eV)']
            ]));
        """,
        "notes": ["E_n = n²h²/(8mL²)。", "电子 1 nm 阱基态 ≈ 0.376 eV。"],
    },
    {
        "slug": "wien-displacement", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "维恩位移定律", "h1": "维恩位移定律计算器",
        "h2": "λ_max = b / T",
        "intro": "黑体辐射峰值波长与温度关系。",
        "desc": "维恩位移：λ_max = b/T，输入温度。",
        "inputs": [
            {"id": "T", "label": "温度 T", "value": "5778", "step": "100", "unit": "K"},
        ],
        "calc": """
            const T = num('T');
            const lam = B_WIEN / T;
            ToolBox.setResult('result', dataGrid([
                [(lam * 1e9).toFixed(2), '峰值波长 λ_max (nm)']
            ]));
        """,
        "notes": ["λ_max = b/T。", "太阳 5778 K → 峰 ≈ 502 nm（绿光）。"],
    },
    {
        "slug": "pair-production-threshold", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "电子对产生阈能", "h1": "电子对产生阈能计算器",
        "h2": "E_min = 2·m_e·c²",
        "intro": "光子产生正负电子对所需最小能量。",
        "desc": "电子对产生阈能：E_min = 2m_e c²。",
        "inputs": [
            {"id": "dummy", "label": "（常量计算）", "value": "1", "step": "1"},
        ],
        "calc": """
            const Emin = 2 * ME * C * C;
            ToolBox.setResult('result', dataGrid([
                [Emin.toExponential(3), '最小能量 (J)'],
                [(Emin / EV / 1e6).toFixed(4), '阈值 (MeV)']
            ]));
        """,
        "notes": ["E_min = 2m_e c² ≈ 1.022 MeV。", "需 ≥ 两电子静能之和。"],
    },
    {
        "slug": "cyclotron-frequency", "industry": "quantum", "cat": "quantum", "icon": "⚛️", "bg": "#faf5ff",
        "title": "回旋频率", "h1": "回旋频率计算器",
        "h2": "ω = q·B / m",
        "intro": "带电粒子在磁场中的回旋角频率。",
        "desc": "回旋频率：ω = qB/m，输入电荷、磁场、质量。",
        "inputs": [
            {"id": "q", "label": "电荷 q", "value": "1.602e-19", "step": "1e-19", "unit": "C"},
            {"id": "B", "label": "磁感应强度 B", "value": "1", "step": "0.1", "unit": "T"},
            {"id": "m", "label": "质量 m", "value": "9.11e-31", "step": "1e-31", "unit": "kg"},
        ],
        "calc": """
            const q = num('q'), B = num('B'), m = num('m');
            const w = q * B / m;
            ToolBox.setResult('result', dataGrid([
                [w.toExponential(3), '角频率 ω (rad/s)'],
                [(w / (2 * Math.PI)).toExponential(3), '频率 f (Hz)']
            ]));
        """,
        "notes": ["ω = qB/m（与速度无关）。", "用于回旋加速器设计。"],
    },
]

# 将物理常数声明前置注入每个 calc 字符串（浏览器端执行）
for _t in TOOLS:
    _t["calc"] = "\n            " + CONSTS + _t["calc"]

if __name__ == "__main__":
    main(TOOLS)
