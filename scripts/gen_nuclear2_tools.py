# -*- coding: utf-8 -*-
"""Batch 53: 核物理深化 II（14 个公式计算器）。industry=nuclear。"""
from tool_template import main

TOOLS = [
    {
        "slug": "decay-constant-from-halflife",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "hourglass",
        "bg": "from-yellow-500 to-orange-600",
        "title": "由半衰期求衰变常数",
        "h1": "λ = ln2 / t_{½}",
        "h2": "由半衰期求衰变常数",
        "intro": "输入半衰期 t½（秒），求衰变常数。", "desc": "由半衰期求衰变常数：输入 t½，输出 λ(1/s)。",
        "inputs": [{"id": "th", "label": "半衰期 t½", "value": "1.808e11", "step": "1e10", "unit": "s"}],
        "calc": """
            const th=num('th');
            const lam=Math.LN2/th;
            ToolBox.setResult('result', dataGrid([
                [lam.toExponential(3),'衰变常数 λ (1/s)']
            ]));
        """,
        "notes": ["λ = ln2/t½。", "C-14 (5730a) → 3.83×10⁻¹² /s。"],
    },
    {
        "slug": "activity-from-halflife",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "radio",
        "bg": "from-yellow-500 to-orange-600",
        "title": "由半衰期与核数求活度",
        "h1": "A = (ln2 / t_{½})·N",
        "h2": "由半衰期与原子核数求活度",
        "intro": "输入半衰期 t½ 与原子核数 N，求活度。", "desc": "由半衰期与核数求活度：输入 t½、N，输出 A(Bq)。",
        "inputs": [
            {"id": "th", "label": "半衰期 t½", "value": "1.808e11", "step": "1e10", "unit": "s"},
            {"id": "N", "label": "核数 N", "value": "1e20", "step": "1e19", "unit": ""},
        ],
        "calc": """
            const th=num('th'),N=num('N');
            const A=Math.LN2/th*N;
            ToolBox.setResult('result', dataGrid([
                [A.toExponential(3),'活度 A (Bq)']
            ]));
        """,
        "notes": ["A = λN = (ln2/t½)·N。", "示例 → 3.83×10⁸ Bq。"],
    },
    {
        "slug": "age-from-activity",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "history",
        "bg": "from-yellow-500 to-orange-600",
        "title": "放射性定年计算器",
        "h1": "t = (1/λ)·ln(N₀/N)",
        "h2": "由初始与现存活度求年龄",
        "intro": "输入衰变常数 λ、初始核数 N₀ 与现存核数 N，求年龄。", "desc": "放射性定年：输入 λ、N₀、N，输出 t(年)。",
        "inputs": [
            {"id": "lam", "label": "衰变常数 λ", "value": "3.833e-12", "step": "1e-13", "unit": "1/s"},
            {"id": "N0", "label": "初始核数 N₀", "value": "1e20", "step": "1e19", "unit": ""},
            {"id": "N", "label": "现存核数 N", "value": "5e19", "step": "1e19", "unit": ""},
        ],
        "calc": """
            const lam=num('lam'),N0=num('N0'),N=num('N');
            const t=(1/lam)*Math.log(N0/N);
            ToolBox.setResult('result', dataGrid([
                [(t/3.156e7).toFixed(0),'年龄 t (年)']
            ]));
        """,
        "notes": ["t = (1/λ)·ln(N₀/N)。", "C-14 减半 → 约 5730 年。"],
    },
    {
        "slug": "dose-equivalent",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "shield",
        "bg": "from-yellow-500 to-orange-600",
        "title": "剂量当量计算器",
        "h1": "H = D·Q",
        "h2": "由吸收剂量与品质因数求剂量当量",
        "intro": "输入吸收剂量 D 与辐射权重因子 Q，求剂量当量。", "desc": "剂量当量：输入 D、Q，输出 H(Sv)。",
        "inputs": [
            {"id": "D", "label": "吸收剂量 D", "value": "2", "step": "0.1", "unit": "Gy"},
            {"id": "Q", "label": "权重因子 Q", "value": "20", "step": "1", "unit": ""},
        ],
        "calc": """
            const D=num('D'),Q=num('Q');
            const H=D*Q;
            ToolBox.setResult('result', dataGrid([
                [H.toFixed(2),'剂量当量 H (Sv)']
            ]));
        """,
        "notes": ["H = D·Q；α 粒子 Q=20。", "D=2Gy,Q=20 → 40 Sv。"],
    },
    {
        "slug": "absorbed-dose",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "zap",
        "bg": "from-yellow-500 to-orange-600",
        "title": "吸收剂量计算器",
        "h1": "D = E / m",
        "h2": "由沉积能量与质量求吸收剂量",
        "intro": "输入沉积能量 E 与质量 m，求吸收剂量。", "desc": "吸收剂量：输入 E、m，输出 D(Gy)。",
        "inputs": [
            {"id": "E", "label": "能量 E", "value": "0.05", "step": "0.01", "unit": "J"},
            {"id": "m", "label": "质量 m", "value": "1", "step": "0.1", "unit": "kg"},
        ],
        "calc": """
            const E=num('E'),m=num('m');
            const D=E/m;
            ToolBox.setResult('result', dataGrid([
                [D.toFixed(4),'吸收剂量 D (Gy)']
            ]));
        """,
        "notes": ["D = E/m，1 Gy = 1 J/kg。", "E=0.05J,m=1kg → 0.05 Gy。"],
    },
    {
        "slug": "gamma-attenuation",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "shield",
        "bg": "from-yellow-500 to-orange-600",
        "title": "γ 射线衰减计算器",
        "h1": "I = I₀·e^{−μx}",
        "h2": "由线性衰减系数与厚度求透射强度",
        "intro": "输入初始强度 I₀、衰减系数 μ、厚度 x，求透射强度。", "desc": "γ 射线衰减：输入 I₀、μ、x，输出 I。",
        "inputs": [
            {"id": "I0", "label": "初始强度 I₀", "value": "100", "step": "1", "unit": ""},
            {"id": "mu", "label": "衰减系数 μ", "value": "0.1", "step": "0.01", "unit": "1/cm"},
            {"id": "x", "label": "厚度 x", "value": "5", "step": "0.5", "unit": "cm"},
        ],
        "calc": """
            const I0=num('I0'),mu=num('mu'),x=num('x');
            const I=I0*Math.exp(-mu*x);
            ToolBox.setResult('result', dataGrid([
                [I.toFixed(3),'透射强度 I']
            ]));
        """,
        "notes": ["I = I₀e^(−μx)。", "I₀=100,μ=0.1,x=5 → 60.65。"],
    },
    {
        "slug": "nuclear-radius",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "circle",
        "bg": "from-yellow-500 to-orange-600",
        "title": "原子核半径计算器",
        "h1": "R = r₀·A^{1/3}",
        "h2": "由质量数求核半径",
        "intro": "输入质量数 A，求原子核半径（r₀=1.2 fm）。", "desc": "原子核半径：输入 A，输出 R(fm)。",
        "inputs": [{"id": "A", "label": "质量数 A", "value": "56", "step": "1", "unit": ""}],
        "calc": """
            const r0=1.2e-15;
            const A=num('A');
            const R=r0*Math.cbrt(A);
            ToolBox.setResult('result', dataGrid([
                [(R*1e15).toFixed(3),'核半径 R (fm)']
            ]));
        """,
        "notes": ["R = r₀A^{1/3}，r₀≈1.2 fm。", "Fe-56 → 约 4.59 fm。"],
    },
    {
        "slug": "survival-probability",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "percent",
        "bg": "from-yellow-500 to-orange-600",
        "title": "核素存活概率计算器",
        "h1": "P = e^{−λt}",
        "h2": "由衰变常数与时间求存活概率",
        "intro": "输入衰变常数 λ 与时间 t，求核素存活概率。", "desc": "核素存活概率：输入 λ、t，输出 P。",
        "inputs": [
            {"id": "lam", "label": "衰变常数 λ", "value": "1e-9", "step": "1e-10", "unit": "1/s"},
            {"id": "t", "label": "时间 t", "value": "1e9", "step": "1e8", "unit": "s"},
        ],
        "calc": """
            const lam=num('lam'),t=num('t');
            const P=Math.exp(-lam*t);
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(4),'存活概率 P']
            ]));
        """,
        "notes": ["P = e^(−λt)。", "λt=1 → e⁻¹≈0.3679。"],
    },
    {
        "slug": "mean-life-from-halflife",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "hourglass",
        "bg": "from-yellow-500 to-orange-600",
        "title": "由半衰期求平均寿命",
        "h1": "τ = t_{½} / ln2",
        "h2": "由半衰期求平均寿命",
        "intro": "输入半衰期 t½（年），求平均寿命。", "desc": "由半衰期求平均寿命：输入 t½，输出 τ(年)。",
        "inputs": [{"id": "th", "label": "半衰期 t½", "value": "5730", "step": "100", "unit": "年"}],
        "calc": """
            const th=num('th');
            const tau=th/Math.LN2;
            ToolBox.setResult('result', dataGrid([
                [tau.toFixed(1),'平均寿命 τ (年)']
            ]));
        """,
        "notes": ["τ = t½/ln2 ≈ 1.443·t½。", "C-14 → 约 8267 年。"],
    },
    {
        "slug": "specific-activity-from-halflife",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "radio",
        "bg": "from-yellow-500 to-orange-600",
        "title": "比活度计算器",
        "h1": "a = (ln2 / t_{½})·N_A / M",
        "h2": "由半衰期与摩尔质量求比活度",
        "intro": "输入半衰期 t½（秒）与摩尔质量 M，求比活度。", "desc": "比活度：输入 t½、M，输出 a(Bq/g)。",
        "inputs": [
            {"id": "th", "label": "半衰期 t½", "value": "1.808e11", "step": "1e10", "unit": "s"},
            {"id": "M", "label": "摩尔质量 M", "value": "14", "step": "1", "unit": "g/mol"},
        ],
        "calc": """
            const NA=6.02214076e23;
            const th=num('th'),M=num('M');
            const a=Math.LN2/th*NA/M;
            ToolBox.setResult('result', dataGrid([
                [a.toExponential(3),'比活度 a (Bq/g)']
            ]));
        """,
        "notes": ["a = λ·N_A/M。", "C-14 → 约 1.65×10¹¹ Bq/g。"],
    },
    {
        "slug": "reaction-rate",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "atom",
        "bg": "from-yellow-500 to-orange-600",
        "title": "核反应率计算器",
        "h1": "R = Φ·σ·N",
        "h2": "由中子通量、截面与靶核数求反应率",
        "intro": "输入中子通量 Φ、微观截面 σ、靶核数 N，求反应率。", "desc": "核反应率：输入 Φ、σ、N，输出 R(1/s)。",
        "inputs": [
            {"id": "F", "label": "通量 Φ", "value": "1e13", "step": "1e12", "unit": "1/(m²·s)"},
            {"id": "s", "label": "截面 σ", "value": "1e-28", "step": "1e-29", "unit": "m²"},
            {"id": "N", "label": "靶核数 N", "value": "1e20", "step": "1e19", "unit": ""},
        ],
        "calc": """
            const F=num('F'),s=num('s'),N=num('N');
            const R=F*s*N;
            ToolBox.setResult('result', dataGrid([
                [R.toExponential(3),'反应率 R (1/s)']
            ]));
        """,
        "notes": ["R = ΦσN。", "示例 → 1×10⁵ /s。"],
    },
    {
        "slug": "half-life-from-activity-nuclei",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "hourglass",
        "bg": "from-yellow-500 to-orange-600",
        "title": "由活度与核数求半衰期",
        "h1": "t_{½} = N·ln2 / A",
        "h2": "由核数与活度反推半衰期",
        "intro": "输入核数 N 与活度 A，求半衰期。", "desc": "由活度与核数求半衰期：输入 N、A，输出 t½(年)。",
        "inputs": [
            {"id": "N", "label": "核数 N", "value": "1e20", "step": "1e19", "unit": ""},
            {"id": "A", "label": "活度 A", "value": "3.833e8", "step": "1e7", "unit": "Bq"},
        ],
        "calc": """
            const N=num('N'),A=num('A');
            const th=N*Math.LN2/A;
            ToolBox.setResult('result', dataGrid([
                [(th/3.156e7).toFixed(0),'半衰期 t½ (年)']
            ]));
        """,
        "notes": ["t½ = N·ln2/A。", "示例 → 约 5730 年。"],
    },
    {
        "slug": "effective-halflife",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "hourglass",
        "bg": "from-yellow-500 to-orange-600",
        "title": "有效半衰期计算器",
        "h1": "1/t_eff = 1/t_phys + 1/t_bio",
        "h2": "由物理与生物半衰期求有效半衰期",
        "intro": "输入物理半衰期 t_phys 与生物半衰期 t_bio，求有效半衰期。", "desc": "有效半衰期：输入 t_phys、t_bio，输出 t_eff(天)。",
        "inputs": [
            {"id": "tp", "label": "物理半衰期 t_phys", "value": "8", "step": "0.5", "unit": "天"},
            {"id": "tb", "label": "生物半衰期 t_bio", "value": "30", "step": "1", "unit": "天"},
        ],
        "calc": """
            const tp=num('tp'),tb=num('tb');
            const te=1/(1/tp+1/tb);
            ToolBox.setResult('result', dataGrid([
                [te.toFixed(2),'有效半衰期 t_eff (天)']
            ]));
        """,
        "notes": ["1/t_eff = 1/t_phys + 1/t_bio。", "8 天与 30 天 → 约 6.32 天。"],
    },
    {
        "slug": "decay-fraction",
        "industry": "nuclear",
        "cat": "nuclear",
        "icon": "percent",
        "bg": "from-yellow-500 to-orange-600",
        "title": "衰变份额计算器",
        "h1": "f = 1 − e^{−λt}",
        "h2": "由衰变常数与时间求已衰变份额",
        "intro": "输入衰变常数 λ 与时间 t，求已衰变份额。", "desc": "衰变份额：输入 λ、t，输出 f。",
        "inputs": [
            {"id": "lam", "label": "衰变常数 λ", "value": "1e-9", "step": "1e-10", "unit": "1/s"},
            {"id": "t", "label": "时间 t", "value": "1e9", "step": "1e8", "unit": "s"},
        ],
        "calc": """
            const lam=num('lam'),t=num('t');
            const f=1-Math.exp(-lam*t);
            ToolBox.setResult('result', dataGrid([
                [f.toFixed(4),'衰变份额 f']
            ]));
        """,
        "notes": ["f = 1−e^(−λt)。", "λt=1 → 1−e⁻¹≈0.6321。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
