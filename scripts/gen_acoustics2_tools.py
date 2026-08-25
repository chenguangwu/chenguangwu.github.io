# -*- coding: utf-8 -*-
"""Batch 44: 声学计算深化 II（14 个公式计算器）。industry=acoustics。"""
from tool_template import main

C_AIR = 343.0  # 空气中声速 m/s（近似）

TOOLS = [
    {
        "slug": "sound-intensity-spherical",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "radio",
        "bg": "from-sky-500 to-blue-600",
        "title": "球面声强计算器",
        "h1": "自由场声强 I = P / (4πr²)",
        "h2": "点声源在距离 r 处的声强",
        "intro": "输入声功率与距离，求球面扩散后的声强。",
        "desc": "球面声强计算器：输入声功率 P 与距离 r，输出声强 I。",
        "inputs": [
            {"id": "P", "label": "声功率 P", "value": "1", "step": "0.1", "unit": "W"},
            {"id": "r", "label": "距离 r", "value": "2", "step": "0.1", "unit": "m"},
        ],
        "calc": """
            const P=num('P'),r=num('r');
            const I=P/(4*Math.PI*r*r);
            ToolBox.setResult('result', dataGrid([
                [I.toExponential(3),'声强 I (W/m²)'],
                [(10*Math.log10(I/1e-12)).toFixed(2),'对应声强级 (dB)']
            ]));
        """,
        "notes": ["I = P/(4πr²)（球面自由场）。", "1 W 在 2 m 处 → I≈0.0199 W/m²。"],
    },
    {
        "slug": "sound-pressure-level",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "volume-2",
        "bg": "from-sky-500 to-blue-600",
        "title": "声压级计算器",
        "h1": "SPL = 20·log₁₀(p / p₀)",
        "h2": "由声压求声压级（p₀=20 µPa）",
        "intro": "输入声压（有效值），求声压级 SPL。",
        "desc": "声压级计算器：输入声压 p，输出 SPL(dB)。",
        "inputs": [
            {"id": "p", "label": "声压 p (有效值)", "value": "0.632", "step": "0.001", "unit": "Pa"},
        ],
        "calc": """
            const p=num('p'), p0=20e-6;
            const spl=20*Math.log10(p/p0);
            ToolBox.setResult('result', dataGrid([
                [spl.toFixed(2),'声压级 SPL (dB)'],
                [p0,'参考声压 p₀ (Pa)']
            ]));
        """,
        "notes": ["SPL = 20log₁₀(p/p₀)，p₀=20 µPa。", "p=0.632 Pa → 约 90 dB（≈痛阈附近）。"],
    },
    {
        "slug": "intensity-level",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "activity",
        "bg": "from-sky-500 to-blue-600",
        "title": "声强级计算器",
        "h1": "L_I = 10·log₁₀(I / I₀)",
        "h2": "由声强求声强级（I₀=10⁻¹² W/m²）",
        "intro": "输入声强，求声强级。",
        "desc": "声强级计算器：输入声强 I，输出声强级 L_I(dB)。",
        "inputs": [
            {"id": "I", "label": "声强 I", "value": "1e-6", "step": "1e-7", "unit": "W/m²"},
        ],
        "calc": """
            const I=num('I'), I0=1e-12;
            const LI=10*Math.log10(I/I0);
            ToolBox.setResult('result', dataGrid([
                [LI.toFixed(2),'声强级 L_I (dB)'],
                [I0,'参考声强 I₀ (W/m²)']
            ]));
        """,
        "notes": ["L_I = 10log₁₀(I/I₀)，I₀=10⁻¹² W/m²。", "I=1e-6 → 60 dB。"],
    },
    {
        "slug": "acoustic-impedance",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "waves",
        "bg": "from-sky-500 to-blue-600",
        "title": "声阻抗计算器",
        "h1": "特性声阻抗 Z = ρ·c",
        "h2": "介质密度与声速之积",
        "intro": "输入介质密度与声速，求特性声阻抗。",
        "desc": "声阻抗计算器：输入密度 ρ 与声速 c，输出 Z。",
        "inputs": [
            {"id": "rho", "label": "介质密度 ρ", "value": "1.2", "step": "0.1", "unit": "kg/m³"},
            {"id": "c", "label": "声速 c", "value": "343", "step": "1", "unit": "m/s"},
        ],
        "calc": """
            const rho=num('rho'),c=num('c');
            ToolBox.setResult('result', dataGrid([
                [(rho*c).toFixed(1),'特性声阻抗 Z (Pa·s/m)'],
                [(rho*c).toFixed(1),'瑞利 (Rayl)']
            ]));
        """,
        "notes": ["Z = ρ·c。空气约 415 Rayl，水约 1.48e6 Rayl。", "1.2×343 ≈ 412 Rayl。"],
    },
    {
        "slug": "wavelength-from-freq",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "ruler",
        "bg": "from-sky-500 to-blue-600",
        "title": "波长计算器（由频率）",
        "h1": "λ = c / f",
        "h2": "由频率求波长",
        "intro": "输入频率（与声速），求波长。",
        "desc": "波长计算器：输入频率 f，输出波长 λ。",
        "inputs": [
            {"id": "f", "label": "频率 f", "value": "1000", "step": "10", "unit": "Hz"},
            {"id": "c", "label": "声速 c", "value": "343", "step": "1", "unit": "m/s"},
        ],
        "calc": """
            const f=num('f'),c=num('c');
            ToolBox.setResult('result', dataGrid([
                [(c/f).toFixed(4),'波长 λ (m)'],
                [((c/f)*100).toFixed(2),'波长 (cm)']
            ]));
        """,
        "notes": ["λ = c/f。", "1 kHz 在空气中 λ=0.343 m。"],
    },
    {
        "slug": "room-axial-mode",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "box",
        "bg": "from-sky-500 to-blue-600",
        "title": "房间轴向简正模式计算器",
        "h1": "f = n·c / (2L)",
        "h2": "矩形房间轴向共振频率",
        "intro": "输入房间尺寸与模式阶数 n，求轴向共振频率。",
        "desc": "房间轴向模式计算器：输入尺寸 L 与阶数 n，输出共振频率。",
        "inputs": [
            {"id": "L", "label": "房间尺寸 L", "value": "5", "step": "0.1", "unit": "m"},
            {"id": "n", "label": "模式阶数 n", "value": "1", "step": "1", "unit": ""},
            {"id": "c", "label": "声速 c", "value": "343", "step": "1", "unit": "m/s"},
        ],
        "calc": """
            const L=num('L'),n=num('n'),c=num('c');
            ToolBox.setResult('result', dataGrid([
                [(n*c/(2*L)).toFixed(2),'轴向共振频率 (Hz)']
            ]));
        """,
        "notes": ["f_n = n·c/(2L)。", "5 m 房间基模 ≈ 34.3 Hz。"],
    },
    {
        "slug": "mass-law-tl",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "shield",
        "bg": "from-sky-500 to-blue-600",
        "title": "质量定律隔声量计算器",
        "h1": "TL ≈ 20·log₁₀(f·m) − 48",
        "h2": "单层均质墙的场隔声量",
        "intro": "输入频率与面密度，用质量定律估算隔声量 TL。",
        "desc": "质量定律隔声计算器：输入 f 与面密度 m，输出 TL。",
        "inputs": [
            {"id": "f", "label": "频率 f", "value": "500", "step": "10", "unit": "Hz"},
            {"id": "m", "label": "面密度 m", "value": "10", "step": "0.5", "unit": "kg/m²"},
        ],
        "calc": """
            const f=num('f'),m=num('m');
            const TL=20*Math.log10(f*m)-48;
            ToolBox.setResult('result', dataGrid([
                [TL.toFixed(2),'隔声量 TL (dB)']
            ]));
        """,
        "notes": ["TL ≈ 20log₁₀(f·m) − 48（f Hz，m kg/m²）。", "10 kg/m²、500 Hz → TL≈26 dB。"],
    },
    {
        "slug": "sound-power-level",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "zap",
        "bg": "from-sky-500 to-blue-600",
        "title": "声功率级计算器",
        "h1": "L_W = 10·log₁₀(W / W₀)",
        "h2": "由声功率求声功率级（W₀=10⁻¹² W）",
        "intro": "输入声功率，求声功率级。",
        "desc": "声功率级计算器：输入声功率 W，输出 L_W(dB)。",
        "inputs": [
            {"id": "W", "label": "声功率 W", "value": "0.01", "step": "0.001", "unit": "W"},
        ],
        "calc": """
            const W=num('W'), W0=1e-12;
            ToolBox.setResult('result', dataGrid([
                [(10*Math.log10(W/W0)).toFixed(2),'声功率级 L_W (dB)']
            ]));
        """,
        "notes": ["L_W = 10log₁₀(W/W₀)，W₀=10⁻¹² W。", "0.01 W → 100 dB。"],
    },
    {
        "slug": "absorption-coeff-sabine",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "percent",
        "bg": "from-sky-500 to-blue-600",
        "title": "平均吸声系数计算器",
        "h1": "ᾱ = 0.161·V / (S·RT60)",
        "h2": "由赛宾公式反推平均吸声系数",
        "intro": "输入房间体积、表面积与混响时间，反推平均吸声系数。",
        "desc": "平均吸声系数计算器：输入 V、S、RT60，输出 ᾱ。",
        "inputs": [
            {"id": "V", "label": "房间体积 V", "value": "100", "step": "1", "unit": "m³"},
            {"id": "S", "label": "表面积 S", "value": "130", "step": "1", "unit": "m²"},
            {"id": "rt", "label": "混响时间 RT60", "value": "0.8", "step": "0.1", "unit": "s"},
        ],
        "calc": """
            const V=num('V'),S=num('S'),rt=num('rt');
            const aBar=0.161*V/(S*rt);
            ToolBox.setResult('result', dataGrid([
                [aBar.toFixed(3),'平均吸声系数 ᾱ'],
                [(aBar*S).toFixed(2),'总吸声量 A (m²·sab)']
            ]));
        """,
        "notes": ["ᾱ = 0.161·V/(S·RT60)（公制）。", "V=100、S=130、RT60=0.8 → ᾱ≈0.155。"],
    },
    {
        "slug": "decibel-power-ratio",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "bar-chart",
        "bg": "from-sky-500 to-blue-600",
        "title": "功率比分贝换算器",
        "h1": "L = 10·log₁₀(P₂ / P₁)",
        "h2": "功率量之比转分贝",
        "intro": "输入两个功率值，求其比值的分贝数。",
        "desc": "功率比分贝换算器：输入 P1、P2，输出 dB。",
        "inputs": [
            {"id": "p1", "label": "参考功率 P₁", "value": "1", "step": "0.1", "unit": "W"},
            {"id": "p2", "label": "比较功率 P₂", "value": "10", "step": "0.1", "unit": "W"},
        ],
        "calc": """
            const p1=num('p1'),p2=num('p2');
            ToolBox.setResult('result', dataGrid([
                [(10*Math.log10(p2/p1)).toFixed(2),'功率比 (dB)'],
                [(p2/p1).toFixed(3),'线性比 P₂/P₁']
            ]));
        """,
        "notes": ["功率量：dB = 10log₁₀(P₂/P₁)。", "10× → 10 dB。"],
    },
    {
        "slug": "decibel-voltage-ratio",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "bar-chart",
        "bg": "from-sky-500 to-blue-600",
        "title": "电压比分贝换算器",
        "h1": "L = 20·log₁₀(V₂ / V₁)",
        "h2": "场量（电压/声压）之比转分贝",
        "intro": "输入两个电压（或声压）值，求其比值的分贝数。",
        "desc": "电压比分贝换算器：输入 V1、V2，输出 dB。",
        "inputs": [
            {"id": "v1", "label": "参考电压 V₁", "value": "1", "step": "0.1", "unit": "V"},
            {"id": "v2", "label": "比较电压 V₂", "value": "3.16", "step": "0.1", "unit": "V"},
        ],
        "calc": """
            const v1=num('v1'),v2=num('v2');
            ToolBox.setResult('result', dataGrid([
                [(20*Math.log10(v2/v1)).toFixed(2),'电压比 (dB)'],
                [(v2/v1).toFixed(3),'线性比 V₂/V₁']
            ]));
        """,
        "notes": ["场量：dB = 20log₁₀(V₂/V₁)。", "√10× → 10 dB。"],
    },
    {
        "slug": "combine-two-spl",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "plus",
        "bg": "from-sky-500 to-blue-600",
        "title": "两声压级叠加计算器",
        "h1": "L = 10·log₁₀(10^(L₁/₁₀)+10^(L₂/₁₀))",
        "h2": "两个不相干声源的总声级",
        "intro": "输入两个声压级，求能量叠加后的总声级。",
        "desc": "两声压级叠加计算器：输入 L1、L2，输出总声级。",
        "inputs": [
            {"id": "l1", "label": "声压级 L₁", "value": "80", "step": "1", "unit": "dB"},
            {"id": "l2", "label": "声压级 L₂", "value": "80", "step": "1", "unit": "dB"},
        ],
        "calc": """
            const l1=num('l1'),l2=num('l2');
            const L=10*Math.log10(Math.pow(10,l1/10)+Math.pow(10,l2/10));
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(2),'总声压级 (dB)'],
                [(L-Math.max(l1,l2)).toFixed(2),'比响者高出 (dB)']
            ]));
        """,
        "notes": ["能量叠加：L=10log₁₀(10^(L1/10)+10^(L2/10))。", "80+80 → 83.01 dB。"],
    },
    {
        "slug": "critical-distance",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "crosshair",
        "bg": "from-sky-500 to-blue-600",
        "title": "临界距离（混响声场）计算器",
        "h1": "r_c ≈ 0.141·√(Q·V / RT60)",
        "h2": "直达声与混响声相等的临界距离",
        "intro": "输入房间体积、混响时间与指向性因子，估算临界距离。",
        "desc": "临界距离计算器：输入 V、RT60、Q，输出 r_c。",
        "inputs": [
            {"id": "V", "label": "房间体积 V", "value": "200", "step": "1", "unit": "m³"},
            {"id": "rt", "label": "混响时间 RT60", "value": "1.0", "step": "0.1", "unit": "s"},
            {"id": "Q", "label": "指向性因子 Q", "value": "1", "step": "1", "unit": ""},
        ],
        "calc": """
            const V=num('V'),rt=num('rt'),Q=num('Q');
            const rc=0.141*Math.sqrt(Q*V/rt);
            ToolBox.setResult('result', dataGrid([
                [rc.toFixed(2),'临界距离 r_c (m)']
            ]));
        """,
        "notes": ["r_c ≈ 0.141·√(Q·V/RT60)（公制近似）。", "V=200、RT60=1、Q=1 → r_c≈2 m。"],
    },
    {
        "slug": "freq-to-note",
        "industry": "acoustics",
        "cat": "acoustics",
        "icon": "music",
        "bg": "from-sky-500 to-blue-600",
        "title": "频率转音名计算器",
        "h1": "n = 69 + 12·log₂(f/440)",
        "h2": "将频率映射到最近的十二平均律音名",
        "intro": "输入频率，求最接近的标准音名（A4=440 Hz）及音分偏差。", "desc": "频率转音名计算器：输入频率 f，输出音名与偏差。",
        "inputs": [
            {"id": "f", "label": "频率 f", "value": "440", "step": "1", "unit": "Hz"},
        ],
        "calc": """
            const f=num('f');
            const NAMES=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
            const midi=69+12*Math.log2(f/440);
            const near=Math.round(midi);
            const cents=Math.round((midi-near)*100);
            const octave=Math.floor(near/12)-1;
            const name=NAMES[((near%12)+12)%12]+octave;
            ToolBox.setResult('result', dataGrid([
                [name,'最接近音名'],
                [near,'MIDI 音高编号'],
                [(cents>=0?'+':'')+cents,'与标准音分偏差']
            ]));
        """,
        "notes": ["A4=440 Hz 为基准，十二平均律。", "442 Hz → A4 +约 +8 音分。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
