# -*- coding: utf-8 -*-
"""Batch 13: 声学/振动计算深化（14 个公式计算器）。industry=acoustics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "sound-speed-air", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "空气中声速", "h1": "空气中声速计算器",
        "h2": "空气中声速（v = 331.4 + 0.6·T）",
        "intro": "干空气中声速随温度近似线性增加。",
        "desc": "空气中声速计算器：v = 331.4 + 0.6·T(℃)，输出 m/s。",
        "inputs": [{"id": "T", "label": "温度", "value": "20", "step": "0.1", "unit": "℃"}],
        "calc": """
            const T = num('T');
            const v = 331.4 + 0.6 * T;
            ToolBox.setResult('result', dataGrid([
                [v.toFixed(2), '声速 v (m/s)'],
                [(v / 3.6).toFixed(2), '约 (km/h)']
            ]));
        """,
        "notes": ["v = 331.4 + 0.6·T（℃），适用于干空气近似。", "20℃ 时声速约 343 m/s。"],
    },
    {
        "slug": "wavelength-frequency", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "波长频率换算", "h1": "波长与频率换算器",
        "h2": "波长频率（λ = v / f）",
        "intro": "已知波速与频率，求声波波长。",
        "desc": "波长频率换算：λ = v/f，输入声速与频率得波长。",
        "inputs": [
            {"id": "v", "label": "波速", "value": "343", "step": "1", "unit": "m/s"},
            {"id": "f", "label": "频率", "value": "440", "step": "1", "unit": "Hz"},
        ],
        "calc": """
            const v = num('v'), f = num('f');
            const lam = v / f;
            ToolBox.setResult('result', dataGrid([
                [lam.toFixed(4), '波长 λ (m)'],
                [(lam * 100).toFixed(2), '波长 (cm)']
            ]));
        """,
        "notes": ["λ = v / f。", "343 m/s、440 Hz 对应波长约 0.78 m（A4 音）。"],
    },
    {
        "slug": "doppler-acoustic", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "声学多普勒", "h1": "声学多普勒效应计算器",
        "h2": "声源趋近（f' = f·v / (v − v_s)）",
        "intro": "声源以速度 v_s 朝向静止观察者运动时，观测频率升高。",
        "desc": "声学多普勒计算器：f' = f·v/(v−v_s)，输入频率、声速与声源速度。",
        "inputs": [
            {"id": "f", "label": "原频率", "value": "440", "step": "1", "unit": "Hz"},
            {"id": "v", "label": "声速", "value": "343", "step": "1", "unit": "m/s"},
            {"id": "vs", "label": "声源速度", "value": "34.3", "step": "0.1", "unit": "m/s"},
        ],
        "calc": """
            const f = num('f'), v = num('v'), vs = num('vs');
            const fp = f * v / (v - vs);
            ToolBox.setResult('result', dataGrid([
                [fp.toFixed(2), '观测频率 f′ (Hz)'],
                [(fp - f).toFixed(2), '频率偏移 (Hz)']
            ]));
        """,
        "notes": ["f' = f·v / (v − v_s)，声源朝向观察者；远离时分母取 v + v_s。", "声源速度 34.3 m/s 时偏移约 +49 Hz。"],
    },
    {
        "slug": "spl-add", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "声压级叠加", "h1": "声压级叠加计算器",
        "h2": "两声压级叠加（L = 10·log₁₀(10^(L₁/10)+10^(L₂/10))）",
        "intro": "两个声压级不能直接相加，需按能量叠加。",
        "desc": "声压级叠加计算器：按能量叠加两个 SPL 得总声压级。",
        "inputs": [
            {"id": "L1", "label": "声压级 1", "value": "80", "step": "0.1", "unit": "dB"},
            {"id": "L2", "label": "声压级 2", "value": "80", "step": "0.1", "unit": "dB"},
        ],
        "calc": """
            const L1 = num('L1'), L2 = num('L2');
            const Lt = 10 * Math.log10(Math.pow(10, L1/10) + Math.pow(10, L2/10));
            ToolBox.setResult('result', dataGrid([
                [Lt.toFixed(2), '总声压级 L (dB)'],
                [(Lt - Math.max(L1, L2)).toFixed(2), '增量 (dB)']
            ]));
        """,
        "notes": ["按能量叠加：L = 10·log₁₀(10^(L₁/10)+10^(L₂/10))。", "两个相同 80 dB 叠加为 83 dB（非 160）。"],
    },
    {
        "slug": "sound-intensity-level", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "声强级计算", "h1": "声强级计算器",
        "h2": "声强级（L_I = 10·log₁₀(I / I₀)）",
        "intro": "声强级以参考声强 I₀ = 1×10⁻¹² W/m² 计。",
        "desc": "声强级计算器：L_I = 10·log10(I/I₀)，I₀=1e-12。",
        "inputs": [{"id": "I", "label": "声强", "value": "1e-6", "step": "1e-6", "unit": "W/m²"}],
        "calc": """
            const I = num('I');
            const I0 = 1e-12;
            const L = 10 * Math.log10(I / I0);
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(2), '声强级 L_I (dB)'],
                [(Math.pow(10, L/10) * I0).toExponential(3), '回算声强 (W/m²)']
            ]));
        """,
        "notes": ["L_I = 10·log₁₀(I / I₀)，I₀ = 1×10⁻¹² W/m²。", "1×10⁻⁶ W/m² 对应 60 dB。"],
    },
    {
        "slug": "decibel-power", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "功率分贝换算", "h1": "功率分贝换算器",
        "h2": "功率分贝（L = 10·log₁₀(P / P₀)）",
        "intro": "功率比用 10 倍对数表达为分贝。",
        "desc": "功率分贝换算：L = 10·log10(P/P₀)，输入功率与参考功率。",
        "inputs": [
            {"id": "P", "label": "功率", "value": "10", "step": "0.1", "unit": "W"},
            {"id": "P0", "label": "参考功率", "value": "1", "step": "0.1", "unit": "W"},
        ],
        "calc": """
            const P = num('P'), P0 = num('P0');
            const L = 10 * Math.log10(P / P0);
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(2), '电平 L (dB)'],
                [Math.pow(10, L/10).toFixed(3), '功率比 P/P₀']
            ]));
        """,
        "notes": ["L = 10·log₁₀(P / P₀)（功率量）。", "功率 10 倍 = 10 dB。"],
    },
    {
        "slug": "string-fundamental", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "弦基频计算", "h1": "弦基频计算器",
        "h2": "弦基频（f₁ = (1/2L)·√(T/μ)）",
        "intro": "两端固定弦的基频由张力、线密度与长度决定。",
        "desc": "弦基频计算器：f₁ = (1/2L)·√(T/μ)，输入长度、张力、线密度。",
        "inputs": [
            {"id": "L", "label": "弦长", "value": "0.65", "step": "0.01", "unit": "m"},
            {"id": "T", "label": "张力", "value": "80", "step": "1", "unit": "N"},
            {"id": "mu", "label": "线密度", "value": "0.01", "step": "0.001", "unit": "kg/m"},
        ],
        "calc": """
            const L = num('L'), T = num('T'), mu = num('mu');
            const f1 = (1 / (2 * L)) * Math.sqrt(T / mu);
            ToolBox.setResult('result', dataGrid([
                [f1.toFixed(2), '基频 f₁ (Hz)'],
                [(f1 * 2).toFixed(2), '二次谐波 (Hz)']
            ]));
        """,
        "notes": ["f₁ = (1/2L)·√(T/μ)；μ 为线密度(kg/m)。", "L=0.65m、T=80N、μ=0.01 时约 68.8 Hz。"],
    },
    {
        "slug": "pipe-closed", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "闭管基频", "h1": "闭管基频计算器",
        "h2": "一端闭口管基频（f₁ = v / 4L）",
        "intro": "一端闭口、一端开口的管，基频波长为管长 4 倍。",
        "desc": "闭管基频计算器：f₁ = v/(4L)，输入声速与管长。",
        "inputs": [
            {"id": "v", "label": "声速", "value": "343", "step": "1", "unit": "m/s"},
            {"id": "L", "label": "管长", "value": "0.5", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const v = num('v'), L = num('L');
            const f1 = v / (4 * L);
            ToolBox.setResult('result', dataGrid([
                [f1.toFixed(2), '基频 f₁ (Hz)'],
                [(f1 * 3).toFixed(2), '三次谐波 (Hz)']
            ]));
        """,
        "notes": ["一端闭口管 f₁ = v/4L，仅含奇次谐波。", "343 m/s、0.5 m 管约 171.5 Hz。"],
    },
    {
        "slug": "pipe-open", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "开管基频", "h1": "开管基频计算器",
        "h2": "两端开口管基频（f₁ = v / 2L）",
        "intro": "两端开口管的基频波长为管长 2 倍。",
        "desc": "开管基频计算器：f₁ = v/(2L)，输入声速与管长。",
        "inputs": [
            {"id": "v", "label": "声速", "value": "343", "step": "1", "unit": "m/s"},
            {"id": "L", "label": "管长", "value": "0.5", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const v = num('v'), L = num('L');
            const f1 = v / (2 * L);
            ToolBox.setResult('result', dataGrid([
                [f1.toFixed(2), '基频 f₁ (Hz)'],
                [(f1 * 2).toFixed(2), '二次谐波 (Hz)']
            ]));
        """,
        "notes": ["两端开口管 f₁ = v/2L，含全部谐波。", "343 m/s、0.5 m 管约 343 Hz。"],
    },
    {
        "slug": "spring-natural-freq", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "弹簧固有频率", "h1": "弹簧-质量系统固有频率计算器",
        "h2": "固有频率（f = (1/2π)·√(k/m)）",
        "intro": "无阻尼弹簧-质量系统的固有频率由刚度与质量决定。",
        "desc": "弹簧固有频率计算器：f = (1/2π)·√(k/m)，输入刚度与质量。",
        "inputs": [
            {"id": "k", "label": "刚度", "value": "100", "step": "1", "unit": "N/m"},
            {"id": "m", "label": "质量", "value": "1", "step": "0.01", "unit": "kg"},
        ],
        "calc": """
            const k = num('k'), m = num('m');
            const f = (1 / (2 * Math.PI)) * Math.sqrt(k / m);
            ToolBox.setResult('result', dataGrid([
                [f.toFixed(4), '固有频率 f (Hz)'],
                [(2 * Math.PI * f).toFixed(4), '角频率 ω (rad/s)']
            ]));
        """,
        "notes": ["f = (1/2π)·√(k/m)。", "k=100 N/m、m=1 kg 时约 1.59 Hz。"],
    },
    {
        "slug": "beat-frequency", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "拍频计算", "h1": "拍频计算器",
        "h2": "拍频（f_beat = |f₁ − f₂|）",
        "intro": "两个相近频率叠加产生拍，拍频为二者之差。",
        "desc": "拍频计算器：f_beat = |f₁ − f₂|，输入两频率。",
        "inputs": [
            {"id": "f1", "label": "频率 1", "value": "440", "step": "1", "unit": "Hz"},
            {"id": "f2", "label": "频率 2", "value": "444", "step": "1", "unit": "Hz"},
        ],
        "calc": """
            const f1 = num('f1'), f2 = num('f2');
            const fb = Math.abs(f1 - f2);
            ToolBox.setResult('result', dataGrid([
                [fb.toFixed(2), '拍频 f_beat (Hz)'],
                [((f1 + f2) / 2).toFixed(2), '平均频率 (Hz)']
            ]));
        """,
        "notes": ["f_beat = |f₁ − f₂|。", "440 与 444 Hz 叠加产生 4 Hz 拍。"],
    },
    {
        "slug": "intensity-inverse-square", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "声强平方反比", "h1": "声强距离平方反比计算器",
        "h2": "声强衰减（I₂ = I₁·(r₁/r₂)²）",
        "intro": "点声源声强随距离平方衰减。",
        "desc": "声强平方反比计算器：I₂ = I₁·(r₁/r₂)²，输入声强与两距离。",
        "inputs": [
            {"id": "I1", "label": "初始声强", "value": "100", "step": "1", "unit": "W/m²"},
            {"id": "r1", "label": "初始距离", "value": "1", "step": "0.1", "unit": "m"},
            {"id": "r2", "label": "目标距离", "value": "2", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const I1 = num('I1'), r1 = num('r1'), r2 = num('r2');
            const I2 = I1 * Math.pow(r1 / r2, 2);
            ToolBox.setResult('result', dataGrid([
                [I2.toFixed(2), '目标声强 I₂ (W/m²)'],
                [(10 * Math.log10(I2 / 1e-12)).toFixed(2), '声强级 (dB)']
            ]));
        """,
        "notes": ["I₂ = I₁·(r₁/r₂)²；点源球面扩散。", "距离加倍，声强降为 1/4。"],
    },
    {
        "slug": "reverberation-time", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "混响时间", "h1": "混响时间（Sabine）计算器",
        "h2": "混响时间（T₆₀ = 0.161·V / A）",
        "intro": "Sabine 公式估算房间混响时间，A 为总吸声量（赛宾）。",
        "desc": "混响时间计算器：T = 0.161·V/A，输入体积与总吸声量。",
        "inputs": [
            {"id": "V", "label": "房间体积", "value": "100", "step": "1", "unit": "m³"},
            {"id": "A", "label": "总吸声量", "value": "10", "step": "0.1", "unit": "sabin"},
        ],
        "calc": """
            const V = num('V'), A = num('A');
            const T = 0.161 * V / A;
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(3), '混响时间 T₆₀ (s)'],
                [(A / V).toFixed(4), '吸声面密度 (1/m)']
            ]));
        """,
        "notes": ["T₆₀ = 0.161·V/A（A 单位为赛宾 sabin）。", "100 m³、10 sabin 约 1.61 s。"],
    },
    {
        "slug": "decibel-voltage", "industry": "acoustics", "cat": "acoustics", "icon": "🔊", "bg": "#eef2ff",
        "title": "电压分贝换算", "h1": "电压分贝换算器",
        "h2": "电压分贝（L = 20·log₁₀(V / V₀)）",
        "intro": "电压、声压等场量用 20 倍对数表达为分贝。",
        "desc": "电压分贝换算：L = 20·log10(V/V₀)，输入电压与参考电压。",
        "inputs": [
            {"id": "V", "label": "电压", "value": "10", "step": "0.1", "unit": "V"},
            {"id": "V0", "label": "参考电压", "value": "1", "step": "0.1", "unit": "V"},
        ],
        "calc": """
            const V = num('V'), V0 = num('V0');
            const L = 20 * Math.log10(V / V0);
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(2), '电平 L (dB)'],
                [Math.pow(10, L/20).toFixed(3), '电压比 V/V₀']
            ]));
        """,
        "notes": ["L = 20·log₁₀(V / V₀)（场量）。", "电压 10 倍 = 20 dB。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
