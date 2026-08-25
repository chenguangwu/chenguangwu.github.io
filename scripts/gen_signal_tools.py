# -*- coding: utf-8 -*-
"""Batch 15: 信号与系统/控制计算深化（14 个公式计算器）。industry=signal。"""
from tool_template import main

TOOLS = [
    {
        "slug": "nyquist-rate", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "奈奎斯特采样率", "h1": "奈奎斯特采样率计算器",
        "h2": "奈奎斯特采样（f_s ≥ 2·f_max）",
        "intro": "无失真重建连续信号所需最小采样率为信号最高频率的两倍。",
        "desc": "奈奎斯特采样率计算器：f_s_min = 2·f_max，输入最高频率。",
        "inputs": [{"id": "fmax", "label": "最高频率", "value": "20000", "step": "100", "unit": "Hz"}],
        "calc": """
            const fmax = num('fmax');
            const fs = 2 * fmax;
            ToolBox.setResult('result', dataGrid([
                [fs.toLocaleString(), '最小采样率 f_s (Hz)'],
                [(fs / 1000).toFixed(1), '采样率 (kHz)']
            ]));
        """,
        "notes": ["f_s_min = 2·f_max（奈奎斯特率）。", "20 kHz 音频需 ≥40 kHz 采样（CD 为 44.1 kHz）。"],
    },
    {
        "slug": "rc-time-constant", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "RC 时间常数", "h1": "RC 时间常数计算器",
        "h2": "时间常数（τ = R·C）",
        "intro": "RC 电路的时间常数决定充放电快慢。",
        "desc": "RC 时间常数计算器：τ = R·C，输出秒。",
        "inputs": [
            {"id": "R", "label": "电阻", "value": "1000", "step": "1", "unit": "Ω"},
            {"id": "C", "label": "电容", "value": "1e-6", "step": "1e-7", "unit": "F"},
        ],
        "calc": """
            const R = num('R'), C = num('C');
            const tau = R * C;
            ToolBox.setResult('result', dataGrid([
                [tau.toExponential(3), '时间常数 τ (s)'],
                [(tau * 1000).toExponential(3), 'τ (ms)']
            ]));
        """,
        "notes": ["τ = R·C。", "1 kΩ 配 1 µF 得 τ = 1 ms。"],
    },
    {
        "slug": "first-order-rise", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "一阶上升时间", "h1": "一阶系统上升时间计算器",
        "h2": "上升时间（t_r ≈ 2.2·τ）",
        "intro": "一阶系统从 10% 升到 90% 约需 2.2 个时间常数。",
        "desc": "一阶上升时间计算器：t_r ≈ 2.2·τ，输入时间常数。",
        "inputs": [{"id": "tau", "label": "时间常数", "value": "0.001", "step": "1e-4", "unit": "s"}],
        "calc": """
            const tau = num('tau');
            const tr = 2.2 * tau;
            ToolBox.setResult('result', dataGrid([
                [tr.toExponential(3), '上升时间 t_r (s)'],
                [(tr * 1000).toExponential(3), 't_r (ms)']
            ]));
        """,
        "notes": ["t_r ≈ 2.2·τ（10%–90%）。", "τ=1 ms 时上升约 2.2 ms。"],
    },
    {
        "slug": "rc-cutoff", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "RC 截止频率", "h1": "RC 截止频率计算器",
        "h2": "−3dB 截止（f_c = 1 / (2π·R·C)）",
        "intro": "一阶 RC 低通/高通滤波器的 −3dB 转折频率。",
        "desc": "RC 截止频率计算器：f_c = 1/(2π·R·C)，输出 Hz。",
        "inputs": [
            {"id": "R", "label": "电阻", "value": "1000", "step": "1", "unit": "Ω"},
            {"id": "C", "label": "电容", "value": "1e-6", "step": "1e-7", "unit": "F"},
        ],
        "calc": """
            const R = num('R'), C = num('C');
            const fc = 1 / (2 * Math.PI * R * C);
            ToolBox.setResult('result', dataGrid([
                [fc.toFixed(2), '截止频率 f_c (Hz)'],
                [(fc / 1000).toFixed(4), 'f_c (kHz)']
            ]));
        """,
        "notes": ["f_c = 1 / (2π·R·C)。", "1 kΩ、1 µF 对应约 159 Hz。"],
    },
    {
        "slug": "sine-rms", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "正弦有效值", "h1": "正弦波有效值计算器",
        "h2": "有效值（V_rms = V_pk / √2）",
        "intro": "正弦波的 RMS（有效值）为峰值的 1/√2。",
        "desc": "正弦有效值计算器：V_rms = V_pk/√2，输入峰值电压。",
        "inputs": [{"id": "Vpk", "label": "峰值电压", "value": "10", "step": "0.1", "unit": "V"}],
        "calc": """
            const Vpk = num('Vpk');
            const Vrms = Vpk / Math.SQRT2;
            ToolBox.setResult('result', dataGrid([
                [Vrms.toFixed(4), '有效值 V_rms (V)'],
                [(Vrms * Vrms / (Vpk * Vpk)).toFixed(4), 'V_rms²/V_pk²']
            ]));
        """,
        "notes": ["V_rms = V_pk / √2；市电 220 V 即有效值，峰值约 311 V。"],
    },
    {
        "slug": "fourier-base", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "傅里叶基频", "h1": "傅里叶级数基频计算器",
        "h2": "基频（f₀ = 1 / T）",
        "intro": "周期信号的基频为其周期的倒数。",
        "desc": "傅里叶基频计算器：f₀ = 1/T，输入周期。",
        "inputs": [{"id": "T", "label": "周期", "value": "0.02", "step": "0.001", "unit": "s"}],
        "calc": """
            const T = num('T');
            const f0 = 1 / T;
            ToolBox.setResult('result', dataGrid([
                [f0.toFixed(2), '基频 f₀ (Hz)'],
                [(1 / f0).toFixed(4), '周期 T (s)']
            ]));
        """,
        "notes": ["f₀ = 1 / T。", "周期 20 ms 对应 50 Hz 基频。"],
    },
    {
        "slug": "damping-ratio", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "阻尼比计算", "h1": "二阶系统阻尼比计算器",
        "h2": "阻尼比（ζ = c / (2√(k·m))）",
        "intro": "阻尼比描述二阶系统振荡衰减程度。",
        "desc": "阻尼比计算器：ζ = c/(2√(km))，输入阻尼系数、刚度、质量。",
        "inputs": [
            {"id": "c", "label": "阻尼系数", "value": "2", "step": "0.1", "unit": "N·s/m"},
            {"id": "k", "label": "刚度", "value": "100", "step": "1", "unit": "N/m"},
            {"id": "m", "label": "质量", "value": "1", "step": "0.01", "unit": "kg"},
        ],
        "calc": """
            const c = num('c'), k = num('k'), m = num('m');
            const zeta = c / (2 * Math.sqrt(k * m));
            ToolBox.setResult('result', dataGrid([
                [zeta.toFixed(4), '阻尼比 ζ'],
                [(zeta < 1 ? '欠阻尼' : zeta > 1 ? '过阻尼' : '临界阻尼'), '状态']
            ]));
        """,
        "notes": ["ζ = c/(2√(km))；ζ<1 振荡，ζ=1 临界，ζ>1 过阻尼。", "示例 ζ=0.1（欠阻尼振荡）。"],
    },
    {
        "slug": "natural-frequency-2nd", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "二阶固有频率", "h1": "二阶系统固有频率计算器",
        "h2": "固有频率（ω_n = √(k/m)）",
        "intro": "二阶系统的无阻尼固有角频率。",
        "desc": "二阶固有频率计算器：ω_n = √(k/m)，同时给 fn。",
        "inputs": [
            {"id": "k", "label": "刚度", "value": "100", "step": "1", "unit": "N/m"},
            {"id": "m", "label": "质量", "value": "1", "step": "0.01", "unit": "kg"},
        ],
        "calc": """
            const k = num('k'), m = num('m');
            const wn = Math.sqrt(k / m);
            const fn = wn / (2 * Math.PI);
            ToolBox.setResult('result', dataGrid([
                [wn.toFixed(4), '固有角频率 ω_n (rad/s)'],
                [fn.toFixed(4), '固有频率 f_n (Hz)']
            ]));
        """,
        "notes": ["ω_n = √(k/m)，f_n = ω_n/2π。", "k=100、m=1 时 ω_n=10 rad/s、f_n≈1.59 Hz。"],
    },
    {
        "slug": "peak-time-2nd", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "二阶峰值时间", "h1": "二阶系统峰值时间计算器",
        "h2": "峰值时间（t_p = π / (ω_n√(1−ζ²))）",
        "intro": "欠阻尼二阶系统首次到达峰值的时间。",
        "desc": "二阶峰值时间计算器：t_p = π/(ω_n√(1−ζ²))，输入 ω_n 与 ζ。",
        "inputs": [
            {"id": "wn", "label": "固有角频率", "value": "10", "step": "0.1", "unit": "rad/s"},
            {"id": "zeta", "label": "阻尼比", "value": "0.1", "step": "0.01"},
        ],
        "calc": """
            const wn = num('wn'), zeta = num('zeta');
            const tp = Math.PI / (wn * Math.sqrt(1 - zeta * zeta));
            ToolBox.setResult('result', dataGrid([
                [tp.toFixed(4), '峰值时间 t_p (s)'],
                [(Math.exp(-zeta * Math.PI / Math.sqrt(1 - zeta * zeta)) * 100).toFixed(2), '超调量 (%)']
            ]));
        """,
        "notes": ["t_p = π/(ω_n√(1−ζ²))；超调量 = exp(−ζπ/√(1−ζ²))。", "ω_n=10、ζ=0.1 时 t_p≈0.316 s、超调约 73%。"],
    },
    {
        "slug": "steady-state-error", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "稳态误差", "h1": "单位反馈稳态误差计算器",
        "h2": "阶跃稳态误差（e_ss = 1 / (1 + K_p)）",
        "intro": "0 型单位反馈系统在单位阶跃输入下的稳态误差。",
        "desc": "稳态误差计算器：e_ss = 1/(1+K_p)，输入比例增益 K_p。",
        "inputs": [{"id": "Kp", "label": "比例增益 K_p", "value": "9", "step": "0.1"}],
        "calc": """
            const Kp = num('Kp');
            const ess = 1 / (1 + Kp);
            ToolBox.setResult('result', dataGrid([
                [ess.toFixed(4), '稳态误差 e_ss'],
                [(ess * 100).toFixed(2), '误差 (%)']
            ]));
        """,
        "notes": ["e_ss = 1/(1+K_p)（0 型系统、单位阶跃）。", "K_p=9 时 e_ss=0.1（10%）。"],
    },
    {
        "slug": "gain-db", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "增益分贝", "h1": "电压增益分贝计算器",
        "h2": "增益（G = 20·log₁₀(V_out / V_in)）",
        "intro": "放大器或网络的电压增益用分贝表示。",
        "desc": "增益分贝计算器：G = 20·log10(Vout/Vin)。",
        "inputs": [
            {"id": "vout", "label": "输出幅度", "value": "10", "step": "0.1", "unit": "V"},
            {"id": "vin", "label": "输入幅度", "value": "1", "step": "0.1", "unit": "V"},
        ],
        "calc": """
            const vout = num('vout'), vin = num('vin');
            const G = 20 * Math.log10(vout / vin);
            ToolBox.setResult('result', dataGrid([
                [G.toFixed(2), '增益 G (dB)'],
                [Math.pow(10, G / 20).toFixed(3), '电压比 V_out/V_in']
            ]));
        """,
        "notes": ["G = 20·log₁₀(V_out/V_in)。", "10 倍电压增益 = 20 dB。"],
    },
    {
        "slug": "pll-lock-range", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "PLL 锁定范围", "h1": "PLL 锁定范围计算器",
        "h2": "锁定范围（Δf = K_v · V_max）",
        "intro": "锁相环中压控振荡器的频率牵引范围由增益与控制电压决定。",
        "desc": "PLL 锁定范围计算器：Δf = K_v·V_max，输入 VCO 增益与最大控制电压。",
        "inputs": [
            {"id": "Kv", "label": "VCO 增益", "value": "1e6", "step": "1e4", "unit": "Hz/V"},
            {"id": "Vmax", "label": "最大控制电压", "value": "5", "step": "0.1", "unit": "V"},
        ],
        "calc": """
            const Kv = num('Kv'), Vmax = num('Vmax');
            const df = Kv * Vmax;
            ToolBox.setResult('result', dataGrid([
                [df.toLocaleString(), '锁定范围 Δf (Hz)'],
                [(df / 1e6).toFixed(3), 'Δf (MHz)']
            ]));
        """,
        "notes": ["Δf = K_v·V_max；VCO 增益 K_v 单位 Hz/V。", "K_v=1 MHz/V、V_max=5V 时范围 ±5 MHz。"],
    },
    {
        "slug": "fft-resolution", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "FFT 频率分辨率", "h1": "FFT 频率分辨率计算器",
        "h2": "频率分辨率（Δf = f_s / N）",
        "intro": "N 点 FFT 的频率分辨率为采样率除以点数。",
        "desc": "FFT 频率分辨率计算器：Δf = f_s/N，输入采样率与 FFT 点数。",
        "inputs": [
            {"id": "fs", "label": "采样率", "value": "1000", "step": "1", "unit": "Hz"},
            {"id": "N", "label": "FFT 点数", "value": "1024", "step": "1"},
        ],
        "calc": """
            const fs = num('fs'), N = num('N');
            const df = fs / N;
            ToolBox.setResult('result', dataGrid([
                [df.toFixed(4), '频率分辨率 Δf (Hz)'],
                [(1 / df).toFixed(1), '可分辨最大周期 (s)']
            ]));
        """,
        "notes": ["Δf = f_s / N；N 越大分辨率越高。", "1 kHz 采样、1024 点 → 约 0.977 Hz。"],
    },
    {
        "slug": "pwm-average", "industry": "signal", "cat": "signal", "icon": "📡", "bg": "#f0f9ff",
        "title": "PWM 平均电压", "h1": "PWM 平均电压计算器",
        "h2": "平均电压（V_avg = D · V_cc）",
        "intro": "脉宽调制输出经低通滤波后的平均电压等于占空比乘电源电压。",
        "desc": "PWM 平均电压计算器：V_avg = D·V_cc，输入占空比与电源电压。",
        "inputs": [
            {"id": "D", "label": "占空比", "value": "50", "step": "1", "unit": "%"},
            {"id": "Vcc", "label": "电源电压", "value": "5", "step": "0.1", "unit": "V"},
        ],
        "calc": """
            const D = num('D'), Vcc = num('Vcc');
            const Vavg = (D / 100) * Vcc;
            ToolBox.setResult('result', dataGrid([
                [Vavg.toFixed(3), '平均电压 V_avg (V)'],
                [(Vavg / Vcc * 100).toFixed(1), '等效占空比 (%)']
            ]));
        """,
        "notes": ["V_avg = D·V_cc，D 为 0–100% 占空比。", "50% 占空比、5 V 电源 → 2.5 V。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
