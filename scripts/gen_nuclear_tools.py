# -*- coding: utf-8 -*-
"""Batch 26: 核物理计算深化（14 个公式计算器）。industry=nuclear。"""
from tool_template import main

# 物理常数（注入到每页 calc JS）
CONSTS = ("const MP=1.6726219e-27,MN=1.6749275e-27,ME=9.10938356e-31,"
          "U=1.66053906660e-27,C=299792458,NA=6.02214076e23,EV=1.602176634e-19,LN2=0.69314718056;")

TOOLS = [
    {
        "slug": "decay-constant", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "衰变常数", "h1": "衰变常数计算器",
        "h2": "λ = ln2 / T_{1/2}",
        "intro": "由半衰期求衰变常数。",
        "desc": "衰变常数：λ = ln2/T½，输入半衰期。",
        "inputs": [
            {"id": "th", "label": "半衰期 T½", "value": "5730", "step": "100", "unit": "年"},
        ],
        "calc": """
            const th = num('th');
            const lam = LN2 / th;
            ToolBox.setResult('result', dataGrid([
                [lam.toExponential(4), '衰变常数 λ (年⁻¹)']
            ]));
        """,
        "notes": ["λ = ln2/T½。", "碳-14 半衰期 5730 年。"],
    },
    {
        "slug": "half-life-from-lambda", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "半衰期（由衰变常数）", "h1": "半衰期计算器",
        "h2": "T_{1/2} = ln2 / λ",
        "intro": "由衰变常数求半衰期。",
        "desc": "半衰期：T½ = ln2/λ，输入衰变常数。",
        "inputs": [
            {"id": "lam", "label": "衰变常数 λ", "value": "1.21e-4", "step": "1e-5", "unit": "年⁻¹"},
        ],
        "calc": """
            const lam = num('lam');
            ToolBox.setResult('result', dataGrid([
                [(LN2 / lam).toFixed(2), '半衰期 T½ (年)']
            ]));
        """,
        "notes": ["T½ = ln2/λ。", "与衰变常数互为倒数关系。"],
    },
    {
        "slug": "mean-life", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "平均寿命", "h1": "平均寿命计算器",
        "h2": "τ = 1 / λ = T_{1/2} / ln2",
        "intro": "放射性核素的平均存活时间。",
        "desc": "平均寿命：τ = T½/ln2，输入半衰期。",
        "inputs": [
            {"id": "th", "label": "半衰期 T½", "value": "5730", "step": "100", "unit": "年"},
        ],
        "calc": """
            const th = num('th');
            ToolBox.setResult('result', dataGrid([
                [(th / LN2).toFixed(2), '平均寿命 τ (年)']
            ]));
        """,
        "notes": ["τ = T½/ln2 ≈ 1.44·T½。"],
    },
    {
        "slug": "radioactive-decay", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "放射性衰变", "h1": "放射性衰变计算器",
        "h2": "N = N₀·e^(−λt)",
        "intro": "随时间衰减的原子核数目。",
        "desc": "衰变规律：N = N₀·e^(−λt)，输入初值、衰变常数、时间。",
        "inputs": [
            {"id": "n0", "label": "初始核数 N₀", "value": "1000", "step": "10"},
            {"id": "lam", "label": "衰变常数 λ", "value": "0.001", "step": "0.0001", "unit": "年⁻¹"},
            {"id": "t", "label": "时间 t", "value": "1000", "step": "10", "unit": "年"},
        ],
        "calc": """
            const n0 = num('n0'), lam = num('lam'), t = num('t');
            const n = n0 * Math.exp(-lam * t);
            ToolBox.setResult('result', dataGrid([
                [n.toFixed(2), '剩余核数 N'],
                [(n / n0 * 100).toFixed(2), '剩余比例 (%)']
            ]));
        """,
        "notes": ["N = N₀e^(−λt)。", "一半衰期后剩约 50%。"],
    },
    {
        "slug": "activity", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "放射性活度", "h1": "放射性活度计算器",
        "h2": "A = λ·N",
        "intro": "单位时间衰变数（贝可勒尔）。",
        "desc": "活度：A = λ·N，输入衰变常数与核数。",
        "inputs": [
            {"id": "lam", "label": "衰变常数 λ", "value": "1e-9", "step": "1e-10", "unit": "s⁻¹"},
            {"id": "n", "label": "核数 N", "value": "1e20", "step": "1e19"},
        ],
        "calc": """
            const lam = num('lam'), n = num('n');
            const A = lam * n;
            ToolBox.setResult('result', dataGrid([
                [A.toExponential(3), '活度 A (Bq)'],
                [(A / 3.7e10).toExponential(3), 'A (Ci)']
            ]));
        """,
        "notes": ["A = λN。", "1 Ci = 3.7e10 Bq。"],
    },
    {
        "slug": "activity-decay", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "活度随时间衰减", "h1": "活度衰减计算器",
        "h2": "A = A₀·e^(−λt)",
        "intro": "初始活度随时间衰减。",
        "desc": "活度衰减：A = A₀·e^(−λt)，输入初活度、衰变常数、时间。",
        "inputs": [
            {"id": "a0", "label": "初始活度 A₀", "value": "100", "step": "1", "unit": "Bq"},
            {"id": "lam", "label": "衰变常数 λ", "value": "0.001", "step": "0.0001", "unit": "年⁻¹"},
            {"id": "t", "label": "时间 t", "value": "1000", "step": "10", "unit": "年"},
        ],
        "calc": """
            const a0 = num('a0'), lam = num('lam'), t = num('t');
            const A = a0 * Math.exp(-lam * t);
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(3), '活度 A (Bq)']
            ]));
        """,
        "notes": ["A = A₀e^(−λt)。", "活度衰减与核数同步。"],
    },
    {
        "slug": "mass-defect", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "质量亏损", "h1": "质量亏损计算器",
        "h2": "Δm = Z·m_p + N·m_n − M",
        "intro": "核子质量之和与原子核质量之差。",
        "desc": "质量亏损：Δm = Z·m_p + N·m_n − M，输入质子数、中子数、核质量。",
        "inputs": [
            {"id": "z", "label": "质子数 Z", "value": "26", "step": "1"},
            {"id": "nn", "label": "中子数 N", "value": "30", "step": "1"},
            {"id": "M", "label": "原子核质量 M", "value": "55.9349", "step": "0.001", "unit": "u"},
        ],
        "calc": """
            const z = num('z'), nn = num('nn'), M = num('M');
            const dm = (z * MP + nn * MN - M * U) / U;
            ToolBox.setResult('result', dataGrid([
                [dm.toFixed(5), '质量亏损 Δm (u)'],
                [(dm * U * C * C / EV / 1e6).toFixed(3), '对应能量 (MeV)']
            ]));
        """,
        "notes": ["Δm = Zm_p + Nm_n − M。", "铁-56：Z=26,N=30。"],
    },
    {
        "slug": "binding-energy", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "结合能", "h1": "原子核结合能计算器",
        "h2": "BE = Δm·c²",
        "intro": "将核子束缚成核所释放的能量。",
        "desc": "结合能：BE = Δm·c²，输入质量亏损（u）。",
        "inputs": [
            {"id": "dm", "label": "质量亏损 Δm", "value": "0.528", "step": "0.01", "unit": "u"},
        ],
        "calc": """
            const dm = num('dm');
            const BE = dm * U * C * C;
            ToolBox.setResult('result', dataGrid([
                [BE.toExponential(3), '结合能 BE (J)'],
                [(BE / EV / 1e6).toFixed(3), 'BE (MeV)']
            ]));
        """,
        "notes": ["1 u·c² ≈ 931.5 MeV。", "铁-56 总结合能约 492 MeV。"],
    },
    {
        "slug": "binding-energy-per-nucleon", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "比结合能", "h1": "比结合能计算器",
        "h2": "BE/A = Δm·c² / A",
        "intro": "每核子的平均结合能，反映核稳定性。",
        "desc": "比结合能：BE/A，输入质量亏损与核子数。",
        "inputs": [
            {"id": "dm", "label": "质量亏损 Δm", "value": "0.528", "step": "0.01", "unit": "u"},
            {"id": "a", "label": "核子数 A", "value": "56", "step": "1"},
        ],
        "calc": """
            const dm = num('dm'), a = num('a');
            const be = dm * U * C * C / EV / 1e6;
            ToolBox.setResult('result', dataGrid([
                [(be / a).toFixed(3), '比结合能 (MeV/核子)']
            ]));
        """,
        "notes": ["铁峰约 8.8 MeV/核子。", "比结合能越大越稳定。"],
    },
    {
        "slug": "q-value", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "核反应 Q 值", "h1": "核反应 Q 值计算器",
        "h2": "Q = (m_i − m_f)·c²",
        "intro": "反应前后质量差对应的能量释放。",
        "desc": "Q 值：Q = (m_i − m_f)c²，输入初末态质量（u）。",
        "inputs": [
            {"id": "mi", "label": "初态总质量 m_i", "value": "4.0026", "step": "0.001", "unit": "u"},
            {"id": "mf", "label": "末态总质量 m_f", "value": "4.0015", "step": "0.001", "unit": "u"},
        ],
        "calc": """
            const mi = num('mi'), mf = num('mf');
            const Q = (mi - mf) * U * C * C / EV / 1e6;
            ToolBox.setResult('result', dataGrid([
                [Q.toFixed(4), 'Q 值 (MeV)'],
                [Q > 0 ? '放能反应' : '吸能反应', '类型']
            ]));
        """,
        "notes": ["Q>0 放能，Q<0 吸能。", "单位换算 1u≈931.5 MeV。"],
    },
    {
        "slug": "carbon-dating-age", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "碳十四测年", "h1": "碳十四测年计算器",
        "h2": "t = (T_{1/2}/ln2)·ln(N₀/N)",
        "intro": "由剩余碳-14 比例推算样品年代。",
        "desc": "碳十四测年：t = T½/ln2 · ln(N₀/N)，输入半衰期与剩余比例。",
        "inputs": [
            {"id": "th", "label": "半衰期 T½", "value": "5730", "step": "100", "unit": "年"},
            {"id": "frac", "label": "剩余比例 N/N₀", "value": "0.5", "step": "0.05"},
        ],
        "calc": """
            const th = num('th'), frac = num('frac');
            const t = (th / LN2) * Math.log(1 / frac);
            ToolBox.setResult('result', dataGrid([
                [t.toFixed(0), '年代 t (年)']
            ]));
        """,
        "notes": ["t = T½/ln2 · ln(N₀/N)。", "剩 50% 即一个半衰期。"],
    },
    {
        "slug": "specific-activity", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "比活度", "h1": "比活度计算器",
        "h2": "a = λ·N_A / M",
        "intro": "单位质量的放射性活度。",
        "desc": "比活度：a = λ·N_A/M，输入半衰期与摩尔质量。",
        "inputs": [
            {"id": "th", "label": "半衰期 T½", "value": "5730", "step": "100", "unit": "年"},
            {"id": "M", "label": "摩尔质量 M", "value": "14", "step": "1", "unit": "g/mol"},
        ],
        "calc": """
            const th = num('th'), M = num('M');
            const lam = LN2 / (th * 365.25 * 24 * 3600); // 转 s⁻¹
            const a = lam * NA / (M / 1000); // 每 kg
            ToolBox.setResult('result', dataGrid([
                [a.toExponential(3), '比活度 (Bq/kg)']
            ]));
        """,
        "notes": ["a = λN_A/M。", "碳-14 比活度较低。"],
    },
    {
        "slug": "fission-energy-yield", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "裂变能产额", "h1": "核裂变总能产额计算器",
        "h2": "E = N·E_f",
        "intro": "由裂变原子数与每次裂变能量求总能。",
        "desc": "裂变能：E = N·E_f，输入原子数与每次裂变能量。",
        "inputs": [
            {"id": "n", "label": "裂变原子数 N", "value": "1e20", "step": "1e19"},
            {"id": "ef", "label": "每次裂变能量 E_f", "value": "200", "step": "10", "unit": "MeV"},
        ],
        "calc": """
            const n = num('n'), ef = num('ef');
            const E = n * ef * 1e6 * EV;
            ToolBox.setResult('result', dataGrid([
                [E.toExponential(3), '总能量 E (J)'],
                [(E / 3.6e9).toFixed(3), 'E (kWh)']
            ]));
        """,
        "notes": ["U-235 每次裂变约 200 MeV。", "1 g 铀-235 释能巨大。"],
    },
    {
        "slug": "pair-annihilation", "industry": "nuclear", "cat": "nuclear", "icon": "☢️", "bg": "#fef2f2",
        "title": "正负电子湮灭", "h1": "电子湮灭光子能量计算器",
        "h2": "E_γ = m_e·c² = 511 keV",
        "intro": "电子对湮灭产生两个 511 keV 光子。",
        "desc": "湮灭光子能量：E_γ = m_e·c²。",
        "inputs": [
            {"id": "dummy", "label": "（常量计算）", "value": "1", "step": "1"},
        ],
        "calc": """
            const E = ME * C * C / EV / 1e3; // keV
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(1), '每个光子能量 (keV)'],
                [(2 * E).toFixed(1), '总能量 (keV)']
            ]));
        """,
        "notes": ["每个光子 511 keV。", "双光子各带 511 keV。"],
    },
]

for _t in TOOLS:
    _t["calc"] = "\n            " + CONSTS + _t["calc"]

if __name__ == "__main__":
    main(TOOLS)
