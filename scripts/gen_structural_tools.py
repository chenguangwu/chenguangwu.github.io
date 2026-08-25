# -*- coding: utf-8 -*-
"""Batch 18: 结构工程计算深化（14 个公式计算器）。industry=structural。"""
from tool_template import main

TOOLS = [
    {
        "slug": "ss-udl-moment", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "简支梁均布弯矩", "h1": "简支梁均布荷载弯矩计算器",
        "h2": "最大弯矩（M_max = w·L² / 8）",
        "intro": "均布荷载简支梁跨中弯矩最大。",
        "desc": "简支梁均布弯矩计算器：M=wL²/8，输入均布荷载与跨度。",
        "inputs": [
            {"id": "w", "label": "均布荷载", "value": "10", "step": "0.1", "unit": "kN/m"},
            {"id": "L", "label": "跨度", "value": "4", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const w = num('w'), L = num('L');
            const M = w * L * L / 8;
            ToolBox.setResult('result', dataGrid([
                [M.toFixed(3), '最大弯矩 M (kN·m)'],
                [(w * L).toFixed(2), '总荷载 (kN)']
            ]));
        """,
        "notes": ["M_max = w·L²/8（均布 w，简支）。", "10 kN/m、4 m 跨中弯矩 20 kN·m。"],
    },
    {
        "slug": "cantilever-end-moment", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "悬臂端弯矩", "h1": "悬臂梁端部弯矩计算器",
        "h2": "端部弯矩（M = F·L）",
        "intro": "悬臂梁自由端集中力在固定端产生最大弯矩。",
        "desc": "悬臂端弯矩计算器：M = F·L，输入端部力与悬臂长度。",
        "inputs": [
            {"id": "F", "label": "端部力", "value": "5", "step": "0.1", "unit": "kN"},
            {"id": "L", "label": "悬臂长度", "value": "2", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const F = num('F'), L = num('L');
            const M = F * L;
            ToolBox.setResult('result', dataGrid([
                [M.toFixed(3), '固定端弯矩 M (kN·m)'],
                [(F / L).toFixed(3), '等效均布 (kN/m)']
            ]));
        """,
        "notes": ["M = F·L（悬臂固定端）。", "5 kN、2 m 悬臂 → 10 kN·m。"],
    },
    {
        "slug": "euler-buckling", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "欧拉临界载荷", "h1": "压杆欧拉临界载荷计算器",
        "h2": "欧拉临界（P_cr = π²·E·I / L²）",
        "intro": "两端铰支细长压杆的屈曲临界载荷。",
        "desc": "欧拉临界载荷计算器：P_cr = π²EI/L²，输出牛顿。",
        "inputs": [
            {"id": "E", "label": "弹性模量", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "I", "label": "截面惯性矩", "value": "1e-6", "step": "1e-7", "unit": "m⁴"},
            {"id": "L", "label": "长度", "value": "2", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const E = num('E'), I = num('I'), L = num('L');
            const Pcr = Math.PI * Math.PI * E * I / (L * L);
            ToolBox.setResult('result', dataGrid([
                [(Pcr).toFixed(1), '临界载荷 P_cr (N)'],
                [(Pcr / 1000).toFixed(2), 'P_cr (kN)']
            ]));
        """,
        "notes": ["P_cr = π²EI/L²（两端铰支）。", "200 GPa 钢、I=1e-6、L=2m → 约 493 kN。"],
    },
    {
        "slug": "radius-of-gyration", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "回转半径", "h1": "截面回转半径计算器",
        "h2": "回转半径（r = √(I / A)）",
        "intro": "回转半径反映截面面积分布离形心的远近。",
        "desc": "回转半径计算器：r = √(I/A)，输入惯性矩与面积。",
        "inputs": [
            {"id": "I", "label": "惯性矩", "value": "1e-6", "step": "1e-7", "unit": "m⁴"},
            {"id": "A", "label": "截面积", "value": "1e-3", "step": "1e-4", "unit": "m²"},
        ],
        "calc": """
            const I = num('I'), A = num('A');
            const r = Math.sqrt(I / A);
            ToolBox.setResult('result', dataGrid([
                [r.toFixed(5), '回转半径 r (m)'],
                [(r * 1000).toFixed(2), 'r (mm)']
            ]));
        """,
        "notes": ["r = √(I/A)。", "I=1e-6、A=1e-3 时 r≈31.6 mm。"],
    },
    {
        "slug": "slenderness-ratio", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "长细比", "h1": "压杆长细比计算器",
        "h2": "长细比（λ = L / r）",
        "intro": "长细比越大越易失稳。",
        "desc": "长细比计算器：λ = L/r，输入长度与回转半径。",
        "inputs": [
            {"id": "L", "label": "长度", "value": "2", "step": "0.1", "unit": "m"},
            {"id": "r", "label": "回转半径", "value": "0.03162", "step": "0.001", "unit": "m"},
        ],
        "calc": """
            const L = num('L'), r = num('r');
            const lam = L / r;
            ToolBox.setResult('result', dataGrid([
                [lam.toFixed(2), '长细比 λ'],
                [(lam < 100 ? '稳定' : '易失稳'), '评估']
            ]));
        """,
        "notes": ["λ = L/r；λ 越大越易失稳。", "L=2、r=0.0316 时 λ≈63。"],
    },
    {
        "slug": "beam-shear-center", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "简支梁支座剪力", "h1": "简支梁跨中集中力剪力计算器",
        "h2": "支座剪力（V = P / 2）",
        "intro": "简支梁跨中一个集中力时，两支座各承担一半。",
        "desc": "简支梁剪力计算器：V = P/2，输入集中力。",
        "inputs": [{"id": "P", "label": "集中力", "value": "10", "step": "0.1", "unit": "kN"}],
        "calc": """
            const P = num('P');
            const V = P / 2;
            ToolBox.setResult('result', dataGrid([
                [V.toFixed(3), '支座剪力 V (kN)'],
                [(V * 1000).toFixed(1), 'V (N)']
            ]));
        """,
        "notes": ["跨中集中力 P 时，V = P/2。", "10 kN 力 → 每支座 5 kN。"],
    },
    {
        "slug": "ss-point-deflection", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "简支梁跨中挠度", "h1": "简支梁集中力挠度计算器",
        "h2": "跨中挠度（δ = P·L³ / (48·E·I)）",
        "intro": "简支梁跨中受集中力的最大挠度。",
        "desc": "简支梁挠度计算器：δ = PL³/(48EI)，输入力、跨度、E、I。",
        "inputs": [
            {"id": "P", "label": "集中力", "value": "10", "step": "0.1", "unit": "kN"},
            {"id": "L", "label": "跨度", "value": "2", "step": "0.1", "unit": "m"},
            {"id": "E", "label": "弹性模量", "value": "200e9", "step": "1e9", "unit": "Pa"},
            {"id": "I", "label": "惯性矩", "value": "1e-6", "step": "1e-7", "unit": "m⁴"},
        ],
        "calc": """
            const P = num('P') * 1000, L = num('L'), E = num('E'), I = num('I');
            const d = P * L * L * L / (48 * E * I);
            ToolBox.setResult('result', dataGrid([
                [(d * 1000).toFixed(3), '挠度 δ (mm)'],
                [(d).toFixed(6), 'δ (m)']
            ]));
        """,
        "notes": ["δ = PL³/(48EI)（跨中集中力）。", "示例约 8.33 mm。"],
    },
    {
        "slug": "torsion-polar-j", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "圆截面极惯性矩", "h1": "实心圆截面极惯性矩计算器",
        "h2": "极惯性矩（J = π·d⁴ / 32）",
        "intro": "圆截面抗扭的几何参数。",
        "desc": "圆截面极惯性矩计算器：J = πd⁴/32，输入直径。",
        "inputs": [{"id": "d", "label": "直径", "value": "0.1", "step": "0.001", "unit": "m"}],
        "calc": """
            const d = num('d');
            const J = Math.PI * Math.pow(d, 4) / 32;
            ToolBox.setResult('result', dataGrid([
                [J.toExponential(3), '极惯性矩 J (m⁴)'],
                [(Math.PI * Math.pow(d, 4) / 64).toExponential(3), '极截面模量 (m³)']
            ]));
        """,
        "notes": ["J = πd⁴/32（实心圆）。", "d=0.1 m 时 J≈9.82×10⁻⁶ m⁴。"],
    },
    {
        "slug": "stress-concentration", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "应力集中", "h1": "应力集中计算器",
        "h2": "最大应力（σ_max = K_t · σ_nom）",
        "intro": "几何不连续处（孔、缺口）应力被放大。",
        "desc": "应力集中计算器：σ_max = K_t·σ_nom，输入应力集中系数与名义应力。",
        "inputs": [
            {"id": "Kt", "label": "应力集中系数", "value": "2", "step": "0.1"},
            {"id": "snom", "label": "名义应力", "value": "100", "step": "1", "unit": "MPa"},
        ],
        "calc": """
            const Kt = num('Kt'), snom = num('snom');
            const smax = Kt * snom;
            ToolBox.setResult('result', dataGrid([
                [smax.toFixed(2), '最大应力 σ_max (MPa)'],
                [((smax / snom)).toFixed(2), '放大倍数']
            ]));
        """,
        "notes": ["σ_max = K_t·σ_nom；K_t 由几何查表。", "K_t=2 时名义应力放大一倍。"],
    },
    {
        "slug": "allowable-stress", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "许用应力", "h1": "许用应力计算器",
        "h2": "许用应力（σ_allow = σ_yield / n）",
        "intro": "以屈服强度和安全系数确定许用应力。",
        "desc": "许用应力计算器：σ_allow = σ_yield/n，输入屈服强度与安全系数。",
        "inputs": [
            {"id": "sy", "label": "屈服强度", "value": "250", "step": "1", "unit": "MPa"},
            {"id": "n", "label": "安全系数", "value": "1.5", "step": "0.1"},
        ],
        "calc": """
            const sy = num('sy'), n = num('n');
            const sa = sy / n;
            ToolBox.setResult('result', dataGrid([
                [sa.toFixed(2), '许用应力 σ_allow (MPa)'],
                [(sa * n).toFixed(2), '回算屈服 (MPa)']
            ]));
        """,
        "notes": ["σ_allow = σ_yield / n。", "250 MPa、n=1.5 → 约 167 MPa。"],
    },
    {
        "slug": "bearing-pressure", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "基底平均压力", "h1": "基底平均压力计算器",
        "h2": "基底压力（p = N / A）",
        "intro": "基础底面平均接触压应力。",
        "desc": "基底压力计算器：p = N/A，输入竖向力与底面积。",
        "inputs": [
            {"id": "N", "label": "竖向力", "value": "100", "step": "1", "unit": "kN"},
            {"id": "A", "label": "底面积", "value": "10", "step": "0.1", "unit": "m²"},
        ],
        "calc": """
            const N = num('N'), A = num('A');
            const p = N / A;
            ToolBox.setResult('result', dataGrid([
                [p.toFixed(3), '基底压力 p (kPa)'],
                [(p * 1000).toFixed(1), 'p (Pa)']
            ]));
        """,
        "notes": ["p = N/A；N 用 kN、A 用 m² 得 kPa。", "100 kN、10 m² → 10 kPa。"],
    },
    {
        "slug": "beam-shear-stress", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "矩形梁最大剪应力", "h1": "矩形截面梁剪应力计算器",
        "h2": "最大剪应力（τ_max = 1.5·V / A）",
        "intro": "矩形截面梁中性轴处剪应力最大，为平均剪应力的 1.5 倍。",
        "desc": "矩形梁剪应力计算器：τ_max = 1.5V/A，输入剪力与截面积。",
        "inputs": [
            {"id": "V", "label": "剪力", "value": "5", "step": "0.1", "unit": "kN"},
            {"id": "A", "label": "截面积", "value": "0.1", "step": "0.001", "unit": "m²"},
        ],
        "calc": """
            const V = num('V') * 1000, A = num('A');
            const t = 1.5 * V / A;
            ToolBox.setResult('result', dataGrid([
                [(t / 1e6).toFixed(3), '最大剪应力 τ (MPa)'],
                [(t / 1e3).toFixed(2), 'τ (kPa)']
            ]));
        """,
        "notes": ["τ_max = 1.5·V/A（矩形截面）。", "5 kN、0.1 m² → 75 kPa。"],
    },
    {
        "slug": "section-modulus-rect", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "矩形截面模量", "h1": "矩形截面模量计算器",
        "h2": "截面模量（W = b·h² / 6）",
        "intro": "截面模量用于弯曲正应力 σ = M/W。",
        "desc": "矩形截面模量计算器：W = bh²/6，输入宽与高。",
        "inputs": [
            {"id": "b", "label": "宽", "value": "0.1", "step": "0.01", "unit": "m"},
            {"id": "h", "label": "高", "value": "0.2", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const b = num('b'), h = num('h');
            const W = b * h * h / 6;
            ToolBox.setResult('result', dataGrid([
                [W.toExponential(3), '截面模量 W (m³)'],
                [(b * Math.pow(h, 3) / 12).toExponential(3), '惯性矩 I (m⁴)']
            ]));
        """,
        "notes": ["W = b·h²/6（绕强轴）。", "0.1×0.2 m 矩形 W≈6.67×10⁻⁴ m³。"],
    },
    {
        "slug": "moment-of-inertia-rect", "industry": "structural", "cat": "structural", "icon": "🏗️", "bg": "#fef3c7",
        "title": "矩形惯性矩", "h1": "矩形截面惯性矩计算器",
        "h2": "惯性矩（I = b·h³ / 12）",
        "intro": "矩形截面绕中性轴的惯性矩。",
        "desc": "矩形惯性矩计算器：I = bh³/12，输入宽与高。",
        "inputs": [
            {"id": "b", "label": "宽", "value": "0.1", "step": "0.01", "unit": "m"},
            {"id": "h", "label": "高", "value": "0.2", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const b = num('b'), h = num('h');
            const I = b * Math.pow(h, 3) / 12;
            ToolBox.setResult('result', dataGrid([
                [I.toExponential(3), '惯性矩 I (m⁴)'],
                [(b * h * h / 6).toExponential(3), '截面模量 W (m³)']
            ]));
        """,
        "notes": ["I = b·h³/12（绕强轴）。", "0.1×0.2 m 矩形 I≈6.67×10⁻⁵ m⁴。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
