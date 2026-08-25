# -*- coding: utf-8 -*-
"""Batch 25: 光学计算深化（14 个公式计算器）。industry=optics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "snells-law", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "斯涅尔定律", "h1": "斯涅尔定律折射计算器",
        "h2": "n₁·sinθ₁ = n₂·sinθ₂",
        "intro": "由入射角与折射率求折射角。",
        "desc": "斯涅尔定律：n₁sinθ₁ = n₂sinθ₂，输入两折射率与入射角。",
        "inputs": [
            {"id": "n1", "label": "折射率 n₁", "value": "1.0", "step": "0.01"},
            {"id": "n2", "label": "折射率 n₂", "value": "1.5", "step": "0.01"},
            {"id": "t1", "label": "入射角 θ₁", "value": "30", "step": "1", "unit": "°"},
        ],
        "calc": """
            const n1 = num('n1'), n2 = num('n2'), t1 = num('t1') * Math.PI / 180;
            const s = n1 * Math.sin(t1) / n2;
            if (s > 1) {
                ToolBox.setResult('result', dataGrid([['发生全反射（无折射）', '']]));
            } else {
                const t2 = Math.asin(s) * 180 / Math.PI;
                ToolBox.setResult('result', dataGrid([
                    [t2.toFixed(3), '折射角 θ₂ (°)']
                ]));
            }
        """,
        "notes": ["n₁sinθ₁ = n₂sinθ₂。", "光从空气入玻璃会向法线偏折。"],
    },
    {
        "slug": "critical-angle", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "临界角", "h1": "全反射临界角计算器",
        "h2": "θ_c = arcsin(n₂ / n₁)",
        "intro": "光从光密到光疏介质发生全反射的最小角。",
        "desc": "临界角：θ_c = arcsin(n₂/n₁)，输入两折射率（n₁>n₂）。",
        "inputs": [
            {"id": "n1", "label": "折射率 n₁（密）", "value": "1.5", "step": "0.01"},
            {"id": "n2", "label": "折射率 n₂（疏）", "value": "1.0", "step": "0.01"},
        ],
        "calc": """
            const n1 = num('n1'), n2 = num('n2');
            const s = n2 / n1;
            if (s > 1) {
                ToolBox.setResult('result', dataGrid([['无全反射（n₁ 须 > n₂）', '']]));
            } else {
                const tc = Math.asin(s) * 180 / Math.PI;
                ToolBox.setResult('result', dataGrid([
                    [tc.toFixed(3), '临界角 θ_c (°)']
                ]));
            }
        """,
        "notes": ["θ_c = arcsin(n₂/n₁)。", "玻璃→空气 ≈ 41.8°。"],
    },
    {
        "slug": "refractive-index", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "折射率", "h1": "折射率计算器",
        "h2": "n = c / v",
        "intro": "由光在介质中的速度求折射率。",
        "desc": "折射率：n = c/v，输入介质中光速。",
        "inputs": [
            {"id": "v", "label": "介质光速 v", "value": "2e8", "step": "1e7", "unit": "m/s"},
            {"id": "c", "label": "真空中光速 c", "value": "3e8", "step": "1e7", "unit": "m/s"},
        ],
        "calc": """
            const v = num('v'), c = num('c');
            ToolBox.setResult('result', dataGrid([
                [(c / v).toFixed(4), '折射率 n']
            ]));
        """,
        "notes": ["n = c/v。", "水 n≈1.33，玻璃 n≈1.5。"],
    },
    {
        "slug": "lens-maker", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "磨镜者公式", "h1": "磨镜者公式计算器",
        "h2": "1/f = (n−1)·(1/R₁ − 1/R₂)",
        "intro": "由曲率半径与折射率求薄透镜焦距。",
        "desc": "磨镜者公式：1/f = (n−1)(1/R₁−1/R₂)，输入折射率与两曲率半径。",
        "inputs": [
            {"id": "n", "label": "折射率 n", "value": "1.5", "step": "0.01"},
            {"id": "r1", "label": "曲率半径 R₁", "value": "0.2", "step": "0.01", "unit": "m"},
            {"id": "r2", "label": "曲率半径 R₂", "value": "-0.2", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const n = num('n'), r1 = num('r1'), r2 = num('r2');
            const f = 1 / ((n - 1) * (1 / r1 - 1 / r2));
            ToolBox.setResult('result', dataGrid([
                [f.toFixed(4), '焦距 f (m)'],
                [(f * 100).toFixed(2), 'f (cm)']
            ]));
        """,
        "notes": ["1/f = (n−1)(1/R₁−1/R₂)。", "双凸 n=1.5、R=±0.2 → f=0.2 m。"],
    },
    {
        "slug": "thin-lens-equation", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "薄透镜成像", "h1": "薄透镜成像公式计算器",
        "h2": "1/f = 1/d_o + 1/d_i",
        "intro": "由物距与焦距求像距。",
        "desc": "薄透镜：1/f = 1/d_o + 1/d_i，输入焦距与物距。",
        "inputs": [
            {"id": "f", "label": "焦距 f", "value": "0.1", "step": "0.005", "unit": "m"},
            {"id": "do", "label": "物距 d_o", "value": "0.3", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const f = num('f'), do_ = num('do');
            const di = 1 / (1 / f - 1 / do_);
            ToolBox.setResult('result', dataGrid([
                [di.toFixed(4), '像距 d_i (m)'],
                [(di > 0 ? '实像' : '虚像'), '像性质']
            ]));
        """,
        "notes": ["1/f = 1/d_o + 1/d_i。", "f=0.1、d_o=0.3 → d_i=0.15 m（实像）。"],
    },
    {
        "slug": "mirror-equation", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "球面镜成像", "h1": "球面镜成像公式计算器",
        "h2": "1/f = 1/d_o + 1/d_i",
        "intro": "凹/凸面镜的成像公式（符号约定同薄透镜）。",
        "desc": "球面镜：1/f = 1/d_o + 1/d_i，输入焦距与物距。",
        "inputs": [
            {"id": "f", "label": "焦距 f（凹正凸负）", "value": "0.2", "step": "0.01", "unit": "m"},
            {"id": "do", "label": "物距 d_o", "value": "0.5", "step": "0.02", "unit": "m"},
        ],
        "calc": """
            const f = num('f'), do_ = num('do');
            const di = 1 / (1 / f - 1 / do_);
            ToolBox.setResult('result', dataGrid([
                [di.toFixed(4), '像距 d_i (m)']
            ]));
        """,
        "notes": ["凹镜 f>0、凸镜 f<0。", "f=0.2、d_o=0.5 → d_i≈0.333 m。"],
    },
    {
        "slug": "magnification-optics", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "光学放大率", "h1": "光学放大率计算器",
        "h2": "M = −d_i / d_o",
        "intro": "横向放大率（负号表示倒立）。",
        "desc": "放大率：M = −d_i/d_o，输入物距与像距。",
        "inputs": [
            {"id": "do", "label": "物距 d_o", "value": "0.3", "step": "0.01", "unit": "m"},
            {"id": "di", "label": "像距 d_i", "value": "0.15", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const do_ = num('do'), di = num('di');
            const M = -di / do_;
            ToolBox.setResult('result', dataGrid([
                [M.toFixed(3), '放大率 M'],
                [(M < 0 ? '倒立' : '正立'), '取向']
            ]));
        """,
        "notes": ["M = −d_i/d_o。", "|M|>1 放大、<1 缩小。"],
    },
    {
        "slug": "brewster-angle", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "布儒斯特角", "h1": "布儒斯特角计算器",
        "h2": "θ_B = arctan(n₂ / n₁)",
        "intro": "反射光完全偏振时的入射角。",
        "desc": "布儒斯特角：θ_B = arctan(n₂/n₁)，输入两折射率。",
        "inputs": [
            {"id": "n1", "label": "折射率 n₁（入射侧）", "value": "1.0", "step": "0.01"},
            {"id": "n2", "label": "折射率 n₂（介质）", "value": "1.5", "step": "0.01"},
        ],
        "calc": """
            const n1 = num('n1'), n2 = num('n2');
            const tb = Math.atan(n2 / n1) * 180 / Math.PI;
            ToolBox.setResult('result', dataGrid([
                [tb.toFixed(3), '布儒斯特角 θ_B (°)']
            ]));
        """,
        "notes": ["θ_B = arctan(n₂/n₁)。", "空气→玻璃 ≈ 56.3°。"],
    },
    {
        "slug": "fresnel-reflectance", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "菲涅尔正入射反射率", "h1": "菲涅尔反射率计算器",
        "h2": "R = ((n₁−n₂)/(n₁+n₂))²",
        "intro": "正入射时界面反射能量比例。",
        "desc": "正入射反射率：R = ((n₁−n₂)/(n₁+n₂))²，输入两折射率。",
        "inputs": [
            {"id": "n1", "label": "折射率 n₁", "value": "1.0", "step": "0.01"},
            {"id": "n2", "label": "折射率 n₂", "value": "1.5", "step": "0.01"},
        ],
        "calc": """
            const n1 = num('n1'), n2 = num('n2');
            const R = Math.pow((n1 - n2) / (n1 + n2), 2);
            ToolBox.setResult('result', dataGrid([
                [(R * 100).toFixed(2), '反射率 R (%)'],
                [((1 - R) * 100).toFixed(2), '透射率 (%)']
            ]));
        """,
        "notes": ["R = ((n₁−n₂)/(n₁+n₂))²。", "空气→玻璃约 4% 反射。"],
    },
    {
        "slug": "diffraction-grating", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "光栅衍射", "h1": "光栅衍射角计算器",
        "h2": "d·sinθ = m·λ",
        "intro": "由光栅常数与波长求第 m 级衍射角。",
        "desc": "光栅方程：d·sinθ = m·λ，输入光栅常数、波长、级次。",
        "inputs": [
            {"id": "d", "label": "光栅常数 d", "value": "1e-6", "step": "1e-7", "unit": "m"},
            {"id": "lam", "label": "波长 λ", "value": "500e-9", "step": "10e-9", "unit": "m"},
            {"id": "m", "label": "级次 m", "value": "1", "step": "1"},
        ],
        "calc": """
            const d = num('d'), lam = num('lam'), m = Math.round(num('m'));
            const s = m * lam / d;
            if (s > 1) {
                ToolBox.setResult('result', dataGrid([['该级次不存在（|sinθ|>1）', '']]));
            } else {
                const th = Math.asin(s) * 180 / Math.PI;
                ToolBox.setResult('result', dataGrid([
                    [th.toFixed(3), '衍射角 θ (°)']
                ]));
            }
        """,
        "notes": ["d·sinθ = mλ。", "1000 线/mm 的 d=1µm。"],
    },
    {
        "slug": "single-slit-diffraction", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "单缝衍射", "h1": "单缝衍射暗纹计算器",
        "h2": "a·sinθ = m·λ（m=1,2,…）",
        "intro": "单缝夫琅禾费衍射第一暗纹角。",
        "desc": "单缝衍射：a·sinθ = mλ，输入缝宽、波长、级次。",
        "inputs": [
            {"id": "a", "label": "缝宽 a", "value": "1e-4", "step": "1e-5", "unit": "m"},
            {"id": "lam", "label": "波长 λ", "value": "500e-9", "step": "10e-9", "unit": "m"},
            {"id": "m", "label": "暗纹级次 m", "value": "1", "step": "1"},
        ],
        "calc": """
            const a = num('a'), lam = num('lam'), m = Math.round(num('m'));
            const s = m * lam / a;
            const th = Math.asin(s) * 180 / Math.PI;
            ToolBox.setResult('result', dataGrid([
                [th.toFixed(4), '暗纹角 θ (°)']
            ]));
        """,
        "notes": ["a·sinθ = mλ。", "第一暗纹 m=1。"],
    },
    {
        "slug": "rayleigh-criterion", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "瑞利判据", "h1": "瑞利分辨极限计算器",
        "h2": "θ_min = 1.22·λ / D",
        "intro": "圆孔衍射的最小可分辨角。",
        "desc": "瑞利判据：θ_min = 1.22λ/D，输入波长与孔径。",
        "inputs": [
            {"id": "lam", "label": "波长 λ", "value": "550e-9", "step": "10e-9", "unit": "m"},
            {"id": "D", "label": "孔径 D", "value": "0.1", "step": "0.005", "unit": "m"},
        ],
        "calc": """
            const lam = num('lam'), D = num('D');
            const th = 1.22 * lam / D;
            ToolBox.setResult('result', dataGrid([
                [(th * 1e6).toFixed(4), '最小分辨角 (µrad)'],
                [(th * 180 / Math.PI * 3600).toExponential(3), 'θ (角秒)']
            ]));
        """,
        "notes": ["θ_min = 1.22λ/D。", "人眼瞳孔 ~2mm 分辨约 1′。"],
    },
    {
        "slug": "numerical-aperture", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "数值孔径分辨率", "h1": "数值孔径分辨率计算器",
        "h2": "d_min = 0.61·λ / NA",
        "intro": "显微镜由数值孔径决定的最小分辨距离。",
        "desc": "NA 分辨率：d_min = 0.61λ/NA，输入波长与数值孔径。",
        "inputs": [
            {"id": "lam", "label": "波长 λ", "value": "550e-9", "step": "10e-9", "unit": "m"},
            {"id": "na", "label": "数值孔径 NA", "value": "1.3", "step": "0.05"},
        ],
        "calc": """
            const lam = num('lam'), na = num('na');
            const d = 0.61 * lam / na;
            ToolBox.setResult('result', dataGrid([
                [(d * 1e9).toFixed(3), '最小分辨距离 (nm)']
            ]));
        """,
        "notes": ["d_min = 0.61λ/NA。", "油镜 NA≈1.4 可分辨 ~240 nm。"],
    },
    {
        "slug": "combined-lens-focal", "industry": "optics", "cat": "optics", "icon": "🔆", "bg": "#fffbeb",
        "title": "组合透镜焦距", "h1": "组合透镜焦距计算器",
        "h2": "1/F = 1/f₁ + 1/f₂",
        "intro": "密接双透镜的等效焦距。",
        "desc": "组合透镜：1/F = 1/f₁ + 1/f₂，输入两透镜焦距。",
        "inputs": [
            {"id": "f1", "label": "焦距 f₁", "value": "0.1", "step": "0.005", "unit": "m"},
            {"id": "f2", "label": "焦距 f₂", "value": "0.2", "step": "0.005", "unit": "m"},
        ],
        "calc": """
            const f1 = num('f1'), f2 = num('f2');
            const F = 1 / (1 / f1 + 1 / f2);
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(4), '等效焦距 F (m)']
            ]));
        """,
        "notes": ["1/F = 1/f₁ + 1/f₂。", "0.1 与 0.2 组合 → 0.0667 m。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
