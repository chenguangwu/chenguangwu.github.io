# -*- coding: utf-8 -*-
"""Batch 47: 信号与系统深化 II（14 个公式计算器）。industry=signal。"""
from tool_template import main

TOOLS = [
    {
        "slug": "snr-db",
        "industry": "signal",
        "cat": "signal",
        "icon": "activity",
        "bg": "from-teal-500 to-cyan-600",
        "title": "信噪比(SNR)计算器",
        "h1": "SNR = 10·log₁₀(Ps/Pn)",
        "h2": "由信号功率与噪声功率求信噪比",
        "intro": "输入信号功率 Ps 与噪声功率 Pn，求信噪比（dB）。", "desc": "信噪比计算器：输入 Ps、Pn，输出 SNR(dB)。",
        "inputs": [
            {"id": "ps", "label": "信号功率 Ps", "value": "10", "step": "0.1", "unit": "W"},
            {"id": "pn", "label": "噪声功率 Pn", "value": "0.1", "step": "0.1", "unit": "W"},
        ],
        "calc": """
            const ps=num('ps'),pn=num('pn');
            const snr=10*Math.log10(ps/pn);
            ToolBox.setResult('result', dataGrid([
                [snr.toFixed(3),'信噪比 SNR (dB)']
            ]));
        """,
        "notes": ["SNR_dB = 10·log10(Ps/Pn)。", "Ps=10,Pn=0.1 → 20 dB。"],
    },
    {
        "slug": "db-power-ratio",
        "industry": "signal",
        "cat": "signal",
        "icon": "gauge",
        "bg": "from-teal-500 to-cyan-600",
        "title": "功率比转分贝计算器",
        "h1": "L = 10·log₁₀(P₁/P₂)",
        "h2": "由两功率求分贝值",
        "intro": "输入功率 P1、P2，求分贝比值。", "desc": "功率比转分贝：输入 P1、P2，输出 L(dB)。",
        "inputs": [
            {"id": "p1", "label": "功率 P₁", "value": "100", "step": "0.1", "unit": "W"},
            {"id": "p2", "label": "功率 P₂", "value": "1", "step": "0.1", "unit": "W"},
        ],
        "calc": """
            const p1=num('p1'),p2=num('p2');
            const L=10*Math.log10(p1/p2);
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(3),'分贝值 L (dB)']
            ]));
        """,
        "notes": ["功率比 dB = 10·log10(P1/P2)。", "100/1 → 20 dB。"],
    },
    {
        "slug": "db-voltage-ratio",
        "industry": "signal",
        "cat": "signal",
        "icon": "gauge",
        "bg": "from-teal-500 to-cyan-600",
        "title": "电压比转分贝计算器",
        "h1": "L = 20·log₁₀(V₁/V₂)",
        "h2": "由两电压求分贝值",
        "intro": "输入电压 V1、V2，求分贝比值。", "desc": "电压比转分贝：输入 V1、V2，输出 L(dB)。",
        "inputs": [
            {"id": "v1", "label": "电压 V₁", "value": "10", "step": "0.1", "unit": "V"},
            {"id": "v2", "label": "电压 V₂", "value": "1", "step": "0.1", "unit": "V"},
        ],
        "calc": """
            const v1=num('v1'),v2=num('v2');
            const L=20*Math.log10(v1/v2);
            ToolBox.setResult('result', dataGrid([
                [L.toFixed(3),'分贝值 L (dB)']
            ]));
        """,
        "notes": ["电压比 dB = 20·log10(V1/V2)。", "10/1 → 20 dB。"],
    },
    {
        "slug": "cascade-gain-db",
        "industry": "signal",
        "cat": "signal",
        "icon": "git-merge",
        "bg": "from-teal-500 to-cyan-600",
        "title": "级联增益计算器",
        "h1": "G_total(dB) = Σ Gᵢ",
        "h2": "由各级增益(dB)求总增益",
        "intro": "输入三级增益（dB），求总增益与线性总增益。", "desc": "级联增益计算器：输入三级增益，输出总 dB 与线性增益。",
        "inputs": [
            {"id": "g1", "label": "第1级增益 G₁", "value": "10", "step": "0.1", "unit": "dB"},
            {"id": "g2", "label": "第2级增益 G₂", "value": "-3", "step": "0.1", "unit": "dB"},
            {"id": "g3", "label": "第3级增益 G₃", "value": "20", "step": "0.1", "unit": "dB"},
        ],
        "calc": """
            const g1=num('g1'),g2=num('g2'),g3=num('g3');
            const total=g1+g2+g3;
            const lin=Math.pow(10,total/10);
            ToolBox.setResult('result', dataGrid([
                [total.toFixed(3),'总增益 (dB)'],
                [lin.toFixed(3),'线性总增益']
            ]));
        """,
        "notes": ["级联总增益为各 dB 之和。", "10-3+20=27 dB → 线性≈501。"],
    },
    {
        "slug": "q-factor",
        "industry": "signal",
        "cat": "signal",
        "icon": "waves",
        "bg": "from-teal-500 to-cyan-600",
        "title": "品质因数 Q 计算器",
        "h1": "Q = f₀ / Δf",
        "h2": "由中心频率与带宽求品质因数",
        "intro": "输入中心频率 f0 与 -3dB 带宽 Δf，求品质因数 Q。", "desc": "品质因数计算器：输入 f0、Δf，输出 Q。",
        "inputs": [
            {"id": "f0", "label": "中心频率 f₀", "value": "1000", "step": "1", "unit": "Hz"},
            {"id": "bw", "label": "带宽 Δf", "value": "100", "step": "1", "unit": "Hz"},
        ],
        "calc": """
            const f0=num('f0'),bw=num('bw');
            const Q=f0/bw;
            ToolBox.setResult('result', dataGrid([
                [Q.toFixed(3),'品质因数 Q']
            ]));
        """,
        "notes": ["Q = f₀/Δf，越大选择性越好。", "1000/100 → Q=10。"],
    },
    {
        "slug": "bandwidth-q",
        "industry": "signal",
        "cat": "signal",
        "icon": "waves",
        "bg": "from-teal-500 to-cyan-600",
        "title": "谐振带宽计算器",
        "h1": "Δf = f₀ / Q",
        "h2": "由中心频率与品质因数求带宽",
        "intro": "输入中心频率 f0 与品质因数 Q，求 -3dB 带宽。", "desc": "谐振带宽计算器：输入 f0、Q，输出 Δf。",
        "inputs": [
            {"id": "f0", "label": "中心频率 f₀", "value": "1000", "step": "1", "unit": "Hz"},
            {"id": "Q", "label": "品质因数 Q", "value": "10", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const f0=num('f0'),Q=num('Q');
            const bw=f0/Q;
            ToolBox.setResult('result', dataGrid([
                [bw.toFixed(3),'带宽 Δf (Hz)']
            ]));
        """,
        "notes": ["Δf = f₀/Q。", "f0=1000,Q=10 → Δf=100 Hz。"],
    },
    {
        "slug": "bit-rate-nyquist",
        "industry": "signal",
        "cat": "signal",
        "icon": "binary",
        "bg": "from-teal-500 to-cyan-600",
        "title": "奈奎斯特最大码率计算器",
        "h1": "R_max = 2B·log₂(M)",
        "h2": "由带宽与电平数求最大码率",
        "intro": "输入带宽 B 与每个符号的电平数 M，求最大无码间串扰码率。", "desc": "奈奎斯特码率计算器：输入 B、M，输出 R_max。",
        "inputs": [
            {"id": "B", "label": "带宽 B", "value": "3000", "step": "1", "unit": "Hz"},
            {"id": "M", "label": "电平数 M", "value": "4", "step": "1", "unit": ""},
        ],
        "calc": """
            const B=num('B'),M=num('M');
            const R=2*B*Math.log2(M);
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(0),'最大码率 R_max (bps)']
            ]));
        """,
        "notes": ["R_max = 2B·log2(M)。", "B=3000,M=4 → 12000 bps。"],
    },
    {
        "slug": "duty-cycle",
        "industry": "signal",
        "cat": "signal",
        "icon": "clock",
        "bg": "from-teal-500 to-cyan-600",
        "title": "占空比计算器",
        "h1": "D = t_on / T × 100%",
        "h2": "由导通时间与周期求占空比",
        "intro": "输入导通时间 ton 与周期 T，求占空比。", "desc": "占空比计算器：输入 ton、T，输出 D(%)。",
        "inputs": [
            {"id": "ton", "label": "导通时间 t_on", "value": "2", "step": "0.1", "unit": "ms"},
            {"id": "T", "label": "周期 T", "value": "10", "step": "0.1", "unit": "ms"},
        ],
        "calc": """
            const ton=num('ton'),T=num('T');
            const D=ton/T*100;
            ToolBox.setResult('result', dataGrid([
                [D.toFixed(2),'占空比 D (%)']
            ]));
        """,
        "notes": ["D = t_on/T。", "2/10 → 20%。"],
    },
    {
        "slug": "signal-power",
        "industry": "signal",
        "cat": "signal",
        "icon": "zap",
        "bg": "from-teal-500 to-cyan-600",
        "title": "信号功率计算器",
        "h1": "P = V_rms² / R",
        "h2": "由有效值与负载求功率",
        "intro": "输入电压有效值 V 与电阻 R，求信号功率。", "desc": "信号功率计算器：输入 V、R，输出 P。",
        "inputs": [
            {"id": "v", "label": "电压有效值 V", "value": "5", "step": "0.1", "unit": "V"},
            {"id": "R", "label": "电阻 R", "value": "50", "step": "0.1", "unit": "Ω"},
        ],
        "calc": """
            const v=num('v'),R=num('R');
            const P=v*v/R;
            ToolBox.setResult('result', dataGrid([
                [P.toFixed(4),'功率 P (W)']
            ]));
        """,
        "notes": ["P = V_rms²/R。", "V=5,R=50 → 0.5 W。"],
    },
    {
        "slug": "mod-index-am",
        "industry": "signal",
        "cat": "signal",
        "icon": "radio",
        "bg": "from-teal-500 to-cyan-600",
        "title": "调幅调制指数计算器",
        "h1": "m = A_m / A_c",
        "h2": "由调制波与载波幅度求调幅指数",
        "intro": "输入调制波幅度 Am 与载波幅度 Ac，求调幅指数。", "desc": "AM 调制指数计算器：输入 Am、Ac，输出 m。",
        "inputs": [
            {"id": "am", "label": "调制波幅度 A_m", "value": "2", "step": "0.1", "unit": "V"},
            {"id": "ac", "label": "载波幅度 A_c", "value": "5", "step": "0.1", "unit": "V"},
        ],
        "calc": """
            const am=num('am'),ac=num('ac');
            const m=am/ac;
            ToolBox.setResult('result', dataGrid([
                [m.toFixed(3),'调制指数 m'],
            ]));
        """,
        "notes": ["m = A_m/A_c，m≤1 无过调制。", "2/5 → m=0.4。"],
    },
    {
        "slug": "mod-index-fm",
        "industry": "signal",
        "cat": "signal",
        "icon": "radio",
        "bg": "from-teal-500 to-cyan-600",
        "title": "调频调制指数计算器",
        "h1": "β = Δf / f_m",
        "h2": "由频偏与调制频率求调频指数",
        "intro": "输入最大频偏 Δf 与调制频率 fm，求调频指数。", "desc": "FM 调制指数计算器：输入 Δf、fm，输出 β。",
        "inputs": [
            {"id": "df", "label": "最大频偏 Δf", "value": "75", "step": "0.1", "unit": "kHz"},
            {"id": "fm", "label": "调制频率 f_m", "value": "15", "step": "0.1", "unit": "kHz"},
        ],
        "calc": """
            const df=num('df'),fm=num('fm');
            const beta=df/fm;
            ToolBox.setResult('result', dataGrid([
                [beta.toFixed(3),'调频指数 β']
            ]));
        """,
        "notes": ["β = Δf/f_m。", "75/15 → β=5。"],
    },
    {
        "slug": "energy-discrete",
        "industry": "signal",
        "cat": "signal",
        "icon": "bar-chart",
        "bg": "from-teal-500 to-cyan-600",
        "title": "离散信号能量计算器",
        "h1": "E = Σ x[n]²",
        "h2": "由采样序列求信号能量",
        "intro": "输入离散采样序列（空格或逗号分隔），求信号总能量。", "desc": "离散信号能量计算器：输入序列，输出能量 E。",
        "inputs": [{"id": "s", "label": "采样序列 x[n]", "value": "1 2 3 -1", "step": "0.1", "unit": ""}],
        "calc": """
            const s=document.getElementById('s').value.split(/[ ,]+/).filter(Boolean).map(Number);
            const E=s.reduce(function(a,b){return a+b*b;},0);
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(3),'信号能量 E'],
                [s.length,'采样点数 N']
            ]));
        """,
        "notes": ["E = Σ x[n]²。", "1,2,3,-1 → 1+4+9+1=15。"],
    },
    {
        "slug": "carrier-freq",
        "industry": "signal",
        "cat": "signal",
        "icon": "radio",
        "bg": "from-teal-500 to-cyan-600",
        "title": "载波频率计算器",
        "h1": "f_c = (f_upper + f_lower) / 2",
        "h2": "由上下边带求载波频率",
        "intro": "输入上边带与下边带频率，求载波频率。", "desc": "载波频率计算器：输入上下边带，输出 fc。",
        "inputs": [
            {"id": "fu", "label": "上边带 f_upper", "value": "1010", "step": "1", "unit": "kHz"},
            {"id": "fl", "label": "下边带 f_lower", "value": "990", "step": "1", "unit": "kHz"},
        ],
        "calc": """
            const fu=num('fu'),fl=num('fl');
            const fc=(fu+fl)/2;
            ToolBox.setResult('result', dataGrid([
                [fc.toFixed(3),'载波频率 f_c (kHz)']
            ]));
        """,
        "notes": ["f_c = (f_upper+f_lower)/2。", "(1010+990)/2 → 1000 kHz。"],
    },
    {
        "slug": "group-delay",
        "industry": "signal",
        "cat": "signal",
        "icon": "timer",
        "bg": "from-teal-500 to-cyan-600",
        "title": "群时延计算器",
        "h1": "τ_g = −dφ/dω",
        "h2": "由相位差与角频率差求群时延",
        "intro": "输入相位差 Δφ（度）与角频率差 Δω（rad/s），求群时延。", "desc": "群时延计算器：输入 Δφ、Δω，输出 τ_g。",
        "inputs": [
            {"id": "dp", "label": "相位差 Δφ", "value": "90", "step": "1", "unit": "°"},
            {"id": "dw", "label": "角频率差 Δω", "value": "1000", "step": "1", "unit": "rad/s"},
        ],
        "calc": """
            const dp=num('dp'),dw=num('dw');
            const tg=-(dp*Math.PI/180)/dw;
            ToolBox.setResult('result', dataGrid([
                [tg.toFixed(6),'群时延 τ_g (s)']
            ]));
        """,
        "notes": ["τ_g = −dφ/dω，相位以弧度计。", "Δφ=90°,Δω=1000 → τ_g≈−1.57 ms。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
