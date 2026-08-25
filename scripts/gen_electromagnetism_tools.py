# -*- coding: utf-8 -*-
"""Batch 17: 电磁学计算深化（14 个公式计算器）。industry=electromagnetism。"""
from tool_template import main

TOOLS = [
    {
        "slug": "ohms-law", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "欧姆定律", "h1": "欧姆定律计算器",
        "h2": "欧姆定律（V = I·R）",
        "intro": "线性电阻两端电压等于电流乘电阻。",
        "desc": "欧姆定律计算器：V = I·R，输入电流与电阻得电压。",
        "inputs": [
            {"id": "I", "label": "电流", "value": "2", "step": "0.1", "unit": "A"},
            {"id": "R", "label": "电阻", "value": "10", "step": "0.1", "unit": "Ω"},
        ],
        "calc": """
            const I = num('I'), R = num('R');
            const V = I * R;
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(3), '电压 V (V)'],
                [(V / I).toFixed(3), '回算电阻 (Ω)']
            ]));
        """,
        "notes": ["V = I·R。", "2 A 通过 10 Ω 产生 20 V。"],
    },
    {
        "slug": "resistors-series", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "电阻串联", "h1": "电阻串联计算器",
        "h2": "串联等效（R = R₁ + R₂ + R₃）",
        "intro": "串联电阻总和即为等效电阻。",
        "desc": "电阻串联计算器：R_eq = ΣRi，输入三个电阻。",
        "inputs": [
            {"id": "R1", "label": "电阻 R₁", "value": "10", "step": "0.1", "unit": "Ω"},
            {"id": "R2", "label": "电阻 R₂", "value": "20", "step": "0.1", "unit": "Ω"},
            {"id": "R3", "label": "电阻 R₃", "value": "30", "step": "0.1", "unit": "Ω"},
        ],
        "calc": """
            const R1 = num('R1'), R2 = num('R2'), R3 = num('R3');
            const R = R1 + R2 + R3;
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(3), '等效电阻 R (Ω)'],
                [(1 / R).toFixed(5), '等效电导 (S)']
            ]));
        """,
        "notes": ["R_eq = R₁ + R₂ + R₃。", "10+20+30 = 60 Ω。"],
    },
    {
        "slug": "resistors-parallel", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "电阻并联", "h1": "电阻并联计算器",
        "h2": "并联等效（1/R = 1/R₁ + 1/R₂）",
        "intro": "并联电阻总电导为各电导之和。",
        "desc": "电阻并联计算器：1/R_eq = 1/R₁+1/R₂，输入两个电阻。",
        "inputs": [
            {"id": "R1", "label": "电阻 R₁", "value": "10", "step": "0.1", "unit": "Ω"},
            {"id": "R2", "label": "电阻 R₂", "value": "10", "step": "0.1", "unit": "Ω"},
        ],
        "calc": """
            const R1 = num('R1'), R2 = num('R2');
            const R = 1 / (1 / R1 + 1 / R2);
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(3), '等效电阻 R (Ω)'],
                [(1 / R).toFixed(4), '总电导 (S)']
            ]));
        """,
        "notes": ["1/R_eq = 1/R₁ + 1/R₂。", "两个 10 Ω 并联 = 5 Ω。"],
    },
    {
        "slug": "electric-power", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "电功率计算", "h1": "电功率计算器",
        "h2": "电功率（P = V·I = V²/R = I²R）",
        "intro": "由电压与电流求电功率。",
        "desc": "电功率计算器：P = V·I，输入电压与电流。",
        "inputs": [
            {"id": "V", "label": "电压", "value": "12", "step": "0.1", "unit": "V"},
            {"id": "I", "label": "电流", "value": "2", "step": "0.1", "unit": "A"},
        ],
        "calc": """
            const V = num('V'), I = num('I');
            const P = V * I;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(3), '功率 P (W)'],
                [(P / 1000).toFixed(4), '功率 (kW)']
            ]));
        """,
        "notes": ["P = V·I；也可 V²/R 或 I²R。", "12 V、2 A 为 24 W。"],
    },
    {
        "slug": "capacitors-series", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "电容串联", "h1": "电容串联计算器",
        "h2": "串联等效（1/C = 1/C₁ + 1/C₂）",
        "intro": "串联电容总电容减小。",
        "desc": "电容串联计算器：1/C_eq = 1/C₁+1/C₂，输入两个电容。",
        "inputs": [
            {"id": "C1", "label": "电容 C₁", "value": "2", "step": "0.1", "unit": "µF"},
            {"id": "C2", "label": "电容 C₂", "value": "2", "step": "0.1", "unit": "µF"},
        ],
        "calc": """
            const C1 = num('C1'), C2 = num('C2');
            const C = 1 / (1 / C1 + 1 / C2);
            ToolBox.setResult('result', dataGrid([
                [C.toFixed(4), '等效电容 C (µF)'],
                [(C1 + C2).toFixed(4), '并联等效 (µF)']
            ]));
        """,
        "notes": ["1/C_eq = 1/C₁ + 1/C₂。", "两个 2 µF 串联 = 1 µF。"],
    },
    {
        "slug": "capacitors-parallel", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "电容并联", "h1": "电容并联计算器",
        "h2": "并联等效（C = C₁ + C₂）",
        "intro": "并联电容总和即为等效电容。",
        "desc": "电容并联计算器：C_eq = C₁+C₂，输入两个电容。",
        "inputs": [
            {"id": "C1", "label": "电容 C₁", "value": "10", "step": "0.1", "unit": "µF"},
            {"id": "C2", "label": "电容 C₂", "value": "22", "step": "0.1", "unit": "µF"},
        ],
        "calc": """
            const C1 = num('C1'), C2 = num('C2');
            const C = C1 + C2;
            ToolBox.setResult('result', dataGrid([
                [C.toFixed(4), '等效电容 C (µF)'],
                [(1 / (1/C1 + 1/C2)).toFixed(4), '串联等效 (µF)']
            ]));
        """,
        "notes": ["C_eq = C₁ + C₂。", "10+22 = 32 µF。"],
    },
    {
        "slug": "inductors-series", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "电感串联", "h1": "电感串联计算器",
        "h2": "串联等效（L = L₁ + L₂）",
        "intro": "串联电感总和即为等效电感（忽略互感）。",
        "desc": "电感串联计算器：L_eq = L₁+L₂，输入两个电感。",
        "inputs": [
            {"id": "L1", "label": "电感 L₁", "value": "1", "step": "0.1", "unit": "mH"},
            {"id": "L2", "label": "电感 L₂", "value": "2", "step": "0.1", "unit": "mH"},
        ],
        "calc": """
            const L1 = num('L1'), L2 = num('L2');
            const L = L1 + L2;
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(4), '等效电感 L (mH)'],
                [(1 / (1/L1 + 1/L2)).toFixed(4), '并联等效 (mH)']
            ]));
        """,
        "notes": ["L_eq = L₁ + L₂（无互感）。", "1+2 = 3 mH。"],
    },
    {
        "slug": "inductors-parallel", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "电感并联", "h1": "电感并联计算器",
        "h2": "并联等效（1/L = 1/L₁ + 1/L₂）",
        "intro": "并联电感总电感减小。",
        "desc": "电感并联计算器：1/L_eq = 1/L₁+1/L₂，输入两个电感。",
        "inputs": [
            {"id": "L1", "label": "电感 L₁", "value": "2", "step": "0.1", "unit": "mH"},
            {"id": "L2", "label": "电感 L₂", "value": "2", "step": "0.1", "unit": "mH"},
        ],
        "calc": """
            const L1 = num('L1'), L2 = num('L2');
            const L = 1 / (1 / L1 + 1 / L2);
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(4), '等效电感 L (mH)'],
                [(1 / L).toFixed(4), '总倒感 (1/mH)']
            ]));
        """,
        "notes": ["1/L_eq = 1/L₁ + 1/L₂。", "两个 2 mH 并联 = 1 mH。"],
    },
    {
        "slug": "b-field-wire", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "直导线磁场", "h1": "长直导线磁场计算器",
        "h2": "安培定律（B = μ₀·I / (2π·r)）",
        "intro": "无限长直导线周围的环向磁感应强度。",
        "desc": "直导线磁场计算器：B = μ₀I/(2πr)，μ₀=4π×10⁻⁷，输出特斯拉。",
        "inputs": [
            {"id": "I", "label": "电流", "value": "10", "step": "0.1", "unit": "A"},
            {"id": "r", "label": "距离", "value": "0.01", "step": "0.001", "unit": "m"},
        ],
        "calc": """
            const I = num('I'), r = num('r');
            const mu0 = 4 * Math.PI * 1e-7;
            const B = mu0 * I / (2 * Math.PI * r);
            ToolBox.setResult('result', dataGrid([
                [B.toExponential(3), '磁感应强度 B (T)'],
                [(B * 1e6).toFixed(2), 'B (µT)']
            ]));
        """,
        "notes": ["B = μ₀I/(2πr)，μ₀ = 4π×10⁻⁷ H/m。", "10 A、1 cm 处约 2×10⁻⁴ T。"],
    },
    {
        "slug": "solenoid-field", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "螺线管磁场", "h1": "螺线管磁场计算器",
        "h2": "螺线管内部（B = μ₀·n·I）",
        "intro": "长螺线管内部磁场与单位长度匝数和电流成正比。",
        "desc": "螺线管磁场计算器：B = μ₀nI，n 为每米匝数，输出特斯拉。",
        "inputs": [
            {"id": "n", "label": "匝密度", "value": "1000", "step": "10", "unit": "匝/m"},
            {"id": "I", "label": "电流", "value": "1", "step": "0.1", "unit": "A"},
        ],
        "calc": """
            const n = num('n'), I = num('I');
            const mu0 = 4 * Math.PI * 1e-7;
            const B = mu0 * n * I;
            ToolBox.setResult('result', dataGrid([
                [B.toExponential(3), '磁感应强度 B (T)'],
                [(B * 1e3).toFixed(3), 'B (mT)']
            ]));
        """,
        "notes": ["B = μ₀·n·I；n 为每米匝数。", "1000 匝/m、1 A 时约 1.26 mT。"],
    },
    {
        "slug": "magnetic-flux", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "磁通量计算", "h1": "磁通量计算器",
        "h2": "磁通（Φ = B·A）",
        "intro": "匀强磁场垂直穿过面积的磁通量。",
        "desc": "磁通量计算器：Φ = B·A，输出韦伯。",
        "inputs": [
            {"id": "B", "label": "磁感应强度", "value": "0.001", "step": "0.0001", "unit": "T"},
            {"id": "A", "label": "面积", "value": "0.01", "step": "0.001", "unit": "m²"},
        ],
        "calc": """
            const B = num('B'), A = num('A');
            const Phi = B * A;
            ToolBox.setResult('result', dataGrid([
                [Phi.toExponential(3), '磁通 Φ (Wb)'],
                [(Phi * 1e6).toFixed(2), 'Φ (µWb)']
            ]));
        """,
        "notes": ["Φ = B·A（B 垂直 A）。", "1 mT、0.01 m² 得 1×10⁻⁵ Wb。"],
    },
    {
        "slug": "faraday-induction", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "法拉第电磁感应", "h1": "法拉第电磁感应计算器",
        "h2": "感应电动势（ε = N·|ΔΦ| / Δt）",
        "intro": "线圈磁通变化率产生感应电动势。",
        "desc": "法拉第电磁感应计算器：ε = N·|ΔΦ|/Δt，输入匝数、磁通变化与时间间隔。",
        "inputs": [
            {"id": "N", "label": "匝数", "value": "100", "step": "1"},
            {"id": "dPhi", "label": "磁通变化", "value": "0.001", "step": "0.0001", "unit": "Wb"},
            {"id": "dt", "label": "时间间隔", "value": "0.1", "step": "0.01", "unit": "s"},
        ],
        "calc": """
            const N = num('N'), dPhi = num('dPhi'), dt = num('dt');
            const eps = N * Math.abs(dPhi) / dt;
            ToolBox.setResult('result', dataGrid([
                [eps.toFixed(4), '感应电动势 ε (V)'],
                [(eps / N).toFixed(6), '每匝 (V)']
            ]));
        """,
        "notes": ["ε = N·|ΔΦ|/Δt（法拉第定律）。", "100 匝、0.001 Wb/0.1 s 得 1 V。"],
    },
    {
        "slug": "lc-resonance", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "LC 谐振频率", "h1": "LC 谐振频率计算器",
        "h2": "谐振频率（f = 1 / (2π·√(L·C))）",
        "intro": "无阻尼 LC 回路的固有谐振频率。",
        "desc": "LC 谐振频率计算器：f = 1/(2π√(LC))，L 用 mH、C 用 µF。",
        "inputs": [
            {"id": "L", "label": "电感", "value": "1", "step": "0.1", "unit": "mH"},
            {"id": "C", "label": "电容", "value": "1", "step": "0.1", "unit": "µF"},
        ],
        "calc": """
            const L = num('L') / 1000, C = num('C') / 1e6;
            const f = 1 / (2 * Math.PI * Math.sqrt(L * C));
            ToolBox.setResult('result', dataGrid([
                [f.toFixed(2), '谐振频率 f (Hz)'],
                [(f / 1000).toFixed(4), 'f (kHz)']
            ]));
        """,
        "notes": ["f = 1/(2π√(LC))。", "1 mH、1 µF 时约 5033 Hz。"],
    },
    {
        "slug": "capacitive-reactance", "industry": "electromagnetism", "cat": "electromagnetism", "icon": "⚡", "bg": "#fffbeb",
        "title": "容抗计算", "h1": "容抗计算器",
        "h2": "容抗（X_C = 1 / (2π·f·C)）",
        "intro": "电容对交流电的阻碍作用随频率升高而降低。",
        "desc": "容抗计算器：X_C = 1/(2πfC)，C 用 µF，输出欧姆。",
        "inputs": [
            {"id": "f", "label": "频率", "value": "60", "step": "1", "unit": "Hz"},
            {"id": "C", "label": "电容", "value": "1", "step": "0.1", "unit": "µF"},
        ],
        "calc": """
            const f = num('f'), C = num('C') / 1e6;
            const Xc = 1 / (2 * Math.PI * f * C);
            ToolBox.setResult('result', dataGrid([
                [Xc.toFixed(2), '容抗 X_C (Ω)'],
                [(-Xc).toFixed(2), '阻抗虚部 (Ω)']
            ]));
        """,
        "notes": ["X_C = 1/(2πfC)；容抗随频率升高而减小。", "60 Hz、1 µF 时约 2653 Ω。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
