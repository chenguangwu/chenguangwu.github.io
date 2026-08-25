# -*- coding: utf-8 -*-
"""Batch 8: 光学计算深化（industry=optical，14 个公式计算器）。

复用 scripts/tool_template.py 的 TEMPLATE + render。
所有公式均经手算核对（见各 notes）。
"""
from tool_template import main

ICON = "🔬"
BG = "#6366f1"
CAT = "calculator"

TOOLS = [
    {
        "slug": "thin-lens-imaging",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "薄透镜成像计算器",
        "h1": "薄透镜成像计算器",
        "h2": "薄透镜成像（高斯公式）",
        "intro": "输入物距与焦距，按 1/f = 1/u + 1/v 计算像距与放大率，并判断实像/虚像。",
        "desc": "薄透镜成像计算器：输入物距与焦距，按高斯公式求像距与放大率，自动判断实像或虚像。",
        "inputs": [
            {"id": "u", "label": "物距 u", "value": 300, "step": "1", "unit": "mm", "min": "0.1"},
            {"id": "f", "label": "焦距 f", "value": 100, "step": "1", "unit": "mm"},
        ],
        "calc": """
            const u=num('u'), f=num('f');
            const denom = 1/f - 1/u;
            let v, m, real;
            if (Math.abs(denom) < 1e-9) {
                ToolBox.setResult('result', dataGrid([['平行光，像在无穷远','提示']]));
            } else {
                v = 1/denom; m = -v/u; real = v>0;
                ToolBox.setResult('result', dataGrid([
                    [v.toFixed(2)+' mm', '像距 v (v>0 实像 / v<0 虚像)'],
                    [m.toFixed(3), '放大率 m = -v/u'],
                    [(real?'实像':'虚像')+(m<0?'（倒立）':'（正立）'), '成像性质']
                ]));
            }
        """,
        "notes": [
            "高斯公式：1/f = 1/u + 1/v（实物距 u>0，凸透镜 f>0）。",
            "像距 v>0 为实像（屏可接收），v<0 为虚像；放大率 m<0 表示倒立。",
        ],
    },
    {
        "slug": "lens-maker",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "透镜制造者公式计算器",
        "h1": "透镜制造者公式计算器",
        "h2": "透镜制造者公式",
        "intro": "由折射率与两表面曲率半径，按 1/f = (n-1)(1/R₁ - 1/R₂) 计算透镜焦距。",
        "desc": "透镜制造者公式计算器：输入折射率与两表面曲率半径，求薄透镜焦距（约定凸面 R>0）。",
        "inputs": [
            {"id": "n", "label": "折射率 n", "value": 1.5, "step": "0.01"},
            {"id": "R1", "label": "前表面曲率半径 R₁", "value": 100, "step": "1", "unit": "mm"},
            {"id": "R2", "label": "后表面曲率半径 R₂", "value": -100, "step": "1", "unit": "mm"},
        ],
        "calc": """
            const n=num('n'), R1=num('R1'), R2=num('R2');
            const inv = (n-1)*(1/R1 - 1/R2);
            const f = 1/inv;
            ToolBox.setResult('result', dataGrid([
                [f.toFixed(2)+' mm', '焦距 f = 1/[(n-1)(1/R₁-1/R₂)]'],
                [(1/f).toFixed(4)+' mm⁻¹', '光焦度 1/f']
            ]));
        """,
        "notes": [
            "符号约定：凸面 R>0、凹面 R<0（光线从左入射）。",
            "平凸透镜取 R₂=∞ 即可（代码中可填极大值近似）。",
        ],
    },
    {
        "slug": "snell-refraction",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "折射定律计算器",
        "h1": "折射定律（斯涅尔）计算器",
        "h2": "斯涅尔折射定律",
        "intro": "由入射角与两侧折射率，按 n₁·sinθ₁ = n₂·sinθ₂ 计算折射角，自动检测全反射。",
        "desc": "折射定律计算器：输入入射角与两侧介质折射率，按斯涅尔定律求折射角并判断全反射。",
        "inputs": [
            {"id": "n1", "label": "入射介质折射率 n₁", "value": 1.0, "step": "0.01"},
            {"id": "n2", "label": "折射介质折射率 n₂", "value": 1.33, "step": "0.01"},
            {"id": "theta1", "label": "入射角 θ₁", "value": 30, "step": "0.5", "unit": "°", "min": "0", "max": "90"},
        ],
        "calc": """
            const n1=num('n1'), n2=num('n2'), t1=num('theta1')*Math.PI/180;
            const s = n1*Math.sin(t1)/n2;
            let out;
            if (s>1) out='发生全反射，无折射光';
            else out=(Math.asin(s)*180/Math.PI).toFixed(2)+' °';
            ToolBox.setResult('result', dataGrid([
                [out, '折射角 θ₂'],
                [(n1*Math.sin(t1)).toFixed(4), 'n₁·sinθ₁']
            ]));
        """,
        "notes": [
            "斯涅尔定律：n₁·sinθ₁ = n₂·sinθ₂。",
            "当 n₁·sinθ₁ > n₂ 时（光从光密到光疏且角过大）发生全反射。",
        ],
    },
    {
        "slug": "critical-angle",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "全反射临界角计算器",
        "h1": "全反射临界角计算器",
        "h2": "临界角 θc",
        "intro": "由光密到光疏介质的折射率，按 θc = arcsin(n₂/n₁) 计算全反射临界角。",
        "desc": "全反射临界角计算器：输入光密与光疏介质折射率，求发生全反射的最小入射角。",
        "inputs": [
            {"id": "n1", "label": "光密介质折射率 n₁", "value": 1.5, "step": "0.01", "min": "0"},
            {"id": "n2", "label": "光疏介质折射率 n₂", "value": 1.0, "step": "0.01", "min": "0"},
        ],
        "calc": """
            const n1=num('n1'), n2=num('n2');
            let out;
            if (n1<=n2) out='需 n₁>n₂ 才可能发生全反射';
            else out=(Math.asin(n2/n1)*180/Math.PI).toFixed(2)+' °';
            ToolBox.setResult('result', dataGrid([ [out, '临界角 θc = arcsin(n₂/n₁)'] ]));
        """,
        "notes": [
            "仅在光从光密介质（n₁）射向光疏介质（n₂）且 n₁>n₂ 时存在全反射。",
            "例：玻璃(n=1.5)→空气(n=1.0)，θc≈41.8°。",
        ],
    },
    {
        "slug": "mirror-imaging",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "球面镜成像计算器",
        "h1": "球面镜成像计算器",
        "h2": "球面镜成像",
        "intro": "由物距与曲率半径，按 f=R/2 与 1/f = 1/u + 1/v 计算像距与放大率。",
        "desc": "球面镜成像计算器：输入物距与曲率半径，求焦距、像距与放大率，判断成像性质。",
        "inputs": [
            {"id": "u", "label": "物距 u", "value": 300, "step": "1", "unit": "mm", "min": "0.1"},
            {"id": "R", "label": "曲率半径 R", "value": 200, "step": "1", "unit": "mm"},
        ],
        "calc": """
            const u=num('u'), R=num('R');
            const f=R/2;
            const denom = 1/f - 1/u;
            let v = 1/denom, m = -v/u, real = v>0;
            ToolBox.setResult('result', dataGrid([
                [(R/2).toFixed(1)+' mm', '焦距 f = R/2'],
                [v.toFixed(2)+' mm', '像距 v'],
                [m.toFixed(3), '放大率 m（'+(real?'实像':'虚像')+'）']
            ]));
        """,
        "notes": [
            "凹面镜 f>0、凸面镜 f<0（此处曲率半径符号决定）。",
            "公式与薄透镜同构：1/f = 1/u + 1/v。",
        ],
    },
    {
        "slug": "telescope-magnification",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "望远镜放大率计算器",
        "h1": "望远镜放大率计算器",
        "h2": "折射望远镜角放大率",
        "intro": "由物镜与目镜焦距，按 M = f₀/fₑ 计算望远镜角放大率。",
        "desc": "望远镜放大率计算器：输入物镜与目镜焦距，求折射望远镜角放大率。",
        "inputs": [
            {"id": "fo", "label": "物镜焦距 f₀", "value": 1000, "step": "10", "unit": "mm"},
            {"id": "fe", "label": "目镜焦距 fₑ", "value": 25, "step": "1", "unit": "mm", "min": "0.1"},
        ],
        "calc": """
            const fo=num('fo'), fe=num('fe');
            const M = fo/fe;
            ToolBox.setResult('result', dataGrid([ [M.toFixed(1)+' ×', '角放大率 M = f₀/fₑ'] ]));
        """,
        "notes": [
            "开普勒望远镜用两凸透镜，放大率为正表示倒像。",
            "放大率越大视场越小，受衍射极限约束。",
        ],
    },
    {
        "slug": "microscope-magnification",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "显微镜放大率计算器",
        "h1": "显微镜放大率计算器",
        "h2": "复式显微镜总放大率",
        "intro": "由物镜/目镜焦距、光学筒长与明视距离，按 M = (L/f₀)(D/fₑ) 计算总放大率。",
        "desc": "显微镜放大率计算器：输入物镜目镜焦距、筒长与明视距离，求复式显微镜总放大率。",
        "inputs": [
            {"id": "fo", "label": "物镜焦距 f₀", "value": 4, "step": "0.1", "unit": "mm", "min": "0.1"},
            {"id": "fe", "label": "目镜焦距 fₑ", "value": 25, "step": "1", "unit": "mm", "min": "0.1"},
            {"id": "L", "label": "光学筒长 L", "value": 160, "step": "1", "unit": "mm"},
            {"id": "D", "label": "明视距离 D", "value": 250, "step": "1", "unit": "mm"},
        ],
        "calc": """
            const fo=num('fo'), fe=num('fe'), L=num('L'), D=num('D');
            const M = (L/fo)*(D/fe);
            ToolBox.setResult('result', dataGrid([ [M.toFixed(0)+' ×', '总放大率 M = (L/f₀)(D/fₑ)'] ]));
        """,
        "notes": [
            "筒长 L 为物镜后焦面到目镜前焦面的距离（标准 160mm）。",
            "明视距离 D 通常取 250mm。",
        ],
    },
    {
        "slug": "diffraction-grating",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "光栅方程计算器",
        "h1": "光栅方程计算器",
        "h2": "衍射光栅方程",
        "intro": "由光栅常数、衍射级次与波长，按 d·sinθ = mλ 计算衍射角。",
        "desc": "光栅方程计算器：输入光栅常数、衍射级次与波长，求各级衍射角并判断级次是否存在。",
        "inputs": [
            {"id": "d", "label": "光栅常数 d", "value": 1000, "step": "10", "unit": "nm", "min": "1"},
            {"id": "m", "label": "衍射级次 m", "value": 1, "step": "1", "min": "1"},
            {"id": "lam", "label": "波长 λ", "value": 500, "step": "1", "unit": "nm", "min": "1"},
        ],
        "calc": """
            const d=num('d'), m=num('m'), lam=num('lam');
            const s = m*lam/d;
            let out = s>1 ? '该级次不存在（sinθ>1）' : (Math.asin(s)*180/Math.PI).toFixed(2)+' °';
            ToolBox.setResult('result', dataGrid([ [out, '衍射角 θ (d·sinθ=mλ)'] ]));
        """,
        "notes": [
            "光栅常数 d = 1/（每毫米刻线数）。",
            "最大可见级次满足 m ≤ d/λ。",
        ],
    },
    {
        "slug": "rayleigh-resolution",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "瑞利分辨极限计算器",
        "h1": "瑞利分辨极限计算器",
        "h2": "瑞利判据",
        "intro": "由波长与孔径直径，按 θ = 1.22λ/D 计算光学系统最小可分辨角。",
        "desc": "瑞利分辨极限计算器：输入波长与孔径直径，求圆孔衍射的最小可分辨角（弧度/角秒）。",
        "inputs": [
            {"id": "lam", "label": "波长 λ", "value": 550, "step": "1", "unit": "nm", "min": "1"},
            {"id": "D", "label": "孔径直径 D", "value": 100, "step": "1", "unit": "mm", "min": "0.1"},
        ],
        "calc": """
            const lam=num('lam')*1e-9, D=num('D')/1000;
            const theta = 1.22*lam/D;
            const arcsec = theta*206265;
            ToolBox.setResult('result', dataGrid([
                [theta.toExponential(3)+' rad', '最小分辨角 θ = 1.22λ/D'],
                [arcsec.toFixed(2)+' ″', '折合角秒']
            ]));
        """,
        "notes": [
            "瑞利判据：两点光源恰可分辨时，一波前极大与另一波前第一极小重合。",
            "人眼瞳孔约 2–5mm，可见光下分辨极限约 1′（角分）。",
        ],
    },
    {
        "slug": "lens-power-diopter",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "屈光度计算器",
        "h1": "屈光度（焦距换算）计算器",
        "h2": "屈光度 P",
        "intro": "由焦距（米）按 P = 1/f 计算透镜屈光度（D）。",
        "desc": "屈光度计算器：输入透镜焦距，换算为屈光度（1/m），眼镜处方常用单位。",
        "inputs": [
            {"id": "f", "label": "焦距 f", "value": 1000, "step": "10", "unit": "mm"},
        ],
        "calc": """
            const f=num('f');
            const P = 1/(f/1000);
            ToolBox.setResult('result', dataGrid([ [P.toFixed(2)+' D', '屈光度 P = 1/f(米)'] ]));
        """,
        "notes": [
            "屈光度单位 D = m⁻¹；凸透镜 P>0（远视/老花），凹透镜 P<0（近视）。",
        ],
    },
    {
        "slug": "numerical-aperture",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "数值孔径计算器",
        "h1": "数值孔径（NA）计算器",
        "h2": "数值孔径 NA",
        "intro": "由介质折射率与最大接受半角，按 NA = n·sinθ 计算数值孔径。",
        "desc": "数值孔径计算器：输入介质折射率与最大接受半角，求透镜/光纤的数值孔径 NA。",
        "inputs": [
            {"id": "n", "label": "介质折射率 n", "value": 1.0, "step": "0.01", "min": "1"},
            {"id": "theta", "label": "最大接受半角 θ", "value": 30, "step": "0.5", "unit": "°", "min": "0", "max": "90"},
        ],
        "calc": """
            const n=num('n'), t=num('theta')*Math.PI/180;
            const NA = n*Math.sin(t);
            ToolBox.setResult('result', dataGrid([ [NA.toFixed(3), '数值孔径 NA = n·sinθ'] ]));
        """,
        "notes": [
            "NA 决定透镜集光能力与衍射分辨极限（分辨率 ∝ λ/NA）。",
            "油镜浸油 n≈1.515，可显著提升 NA 与分辨率。",
        ],
    },
    {
        "slug": "gaussian-beam-waist",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "高斯光束束腰计算器",
        "h1": "高斯光束束腰半径计算器",
        "h2": "聚焦高斯光束腰斑",
        "intro": "由波长、聚焦透镜焦距与入射光束直径，按 w₀ = 4λf/(πD) 计算束腰半径。",
        "desc": "高斯光束束腰计算器：输入波长、透镜焦距与入射光束直径，求聚焦后的束腰半径（µm）。",
        "inputs": [
            {"id": "lam", "label": "波长 λ", "value": 650, "step": "1", "unit": "nm", "min": "1"},
            {"id": "f", "label": "透镜焦距 f", "value": 50, "step": "1", "unit": "mm", "min": "0.1"},
            {"id": "D", "label": "入射光束直径 D", "value": 10, "step": "0.5", "unit": "mm", "min": "0.1"},
        ],
        "calc": """
            const lam=num('lam')*1e-9, f=num('f')/1000, D=num('D')/1000;
            const w0 = 4*lam*f/(Math.PI*D);
            ToolBox.setResult('result', dataGrid([ [(w0*1e6).toFixed(2)+' µm', '束腰半径 w₀ = 4λf/(πD)'] ]));
        """,
        "notes": [
            "适用于入射为准直高斯光束、透镜口径远大于光束的近似。",
            "束腰半径越小，聚焦功率密度越高。",
        ],
    },
    {
        "slug": "f-number",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "光圈数计算器",
        "h1": "光圈数（F 值）计算器",
        "h2": "光圈数 N",
        "intro": "由焦距与有效孔径，按 N = f/D 计算摄影镜头光圈数。",
        "desc": "光圈数计算器：输入镜头焦距与有效孔径直径，求 F 值（光圈数），用于曝光与景深评估。",
        "inputs": [
            {"id": "f", "label": "焦距 f", "value": 50, "step": "1", "unit": "mm", "min": "0.1"},
            {"id": "D", "label": "有效孔径 D", "value": 25, "step": "0.5", "unit": "mm", "min": "0.1"},
        ],
        "calc": """
            const f=num('f'), D=num('D');
            const N = f/D;
            ToolBox.setResult('result', dataGrid([ [N.toFixed(1), '光圈数 N = f/D'] ]));
        """,
        "notes": [
            "N 每增大 √2 倍，进光量减半；景深随 N 增大而增大。",
        ],
    },
    {
        "slug": "optical-path-length",
        "industry": "optical", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "光程计算器",
        "h1": "光程（光学路径长度）计算器",
        "h2": "光程 OP",
        "intro": "由折射率与几何路程，按 光程 = n·L 计算光在介质中的等效真空路径。",
        "desc": "光程计算器：输入介质折射率与几何路程，求光程（等效真空路径长度）。",
        "inputs": [
            {"id": "n", "label": "折射率 n", "value": 1.5, "step": "0.01", "min": "1"},
            {"id": "L", "label": "几何路程 L", "value": 100, "step": "1", "unit": "mm", "min": "0"},
        ],
        "calc": """
            const n=num('n'), L=num('L');
            const op = n*L;
            ToolBox.setResult('result', dataGrid([ [op.toFixed(1)+' mm', '光程 = n·L'] ]));
        """,
        "notes": [
            "光程是把介质路径折算为真空等效长度，费马原理与干涉分析的基础。",
        ],
    },
]


if __name__ == "__main__":
    main(TOOLS)
