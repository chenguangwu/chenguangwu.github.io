# -*- coding: utf-8 -*-
"""Batch 27: 动力学计算深化（14 个公式计算器）。industry=dynamics。"""
from tool_template import main

TOOLS = [
    {
        "slug": "newtons-second", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "牛顿第二定律", "h1": "牛顿第二定律计算器",
        "h2": "F = m·a",
        "intro": "合力等于质量乘以加速度。",
        "desc": "牛顿第二定律：F = ma，输入质量与加速度。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "1000", "step": "10", "unit": "kg"},
            {"id": "a", "label": "加速度 a", "value": "2", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const m = num('m'), a = num('a');
            ToolBox.setResult('result', dataGrid([
                [(m * a).toFixed(2), '合力 F (N)']
            ]));
        """,
        "notes": ["F = ma。", "1000 kg × 2 = 2000 N。"],
    },
    {
        "slug": "weight-force", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "重力", "h1": "重力计算器",
        "h2": "W = m·g",
        "intro": "物体所受地球引力。",
        "desc": "重力：W = mg，输入质量与重力加速度。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "70", "step": "1", "unit": "kg"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const m = num('m'), g = num('g');
            ToolBox.setResult('result', dataGrid([
                [(m * g).toFixed(2), '重力 W (N)'],
                [(m * g / 9.81).toFixed(2), 'W (kgf)']
            ]));
        """,
        "notes": ["W = mg。", "70 kg → 686 N。"],
    },
    {
        "slug": "kinetic-friction", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "动摩擦力", "h1": "动摩擦力计算器",
        "h2": "F_k = μ_k·N",
        "intro": "滑动摩擦力等于动摩擦系数乘正压力。",
        "desc": "动摩擦力：F_k = μ_k·N，输入动摩擦系数与正压力。",
        "inputs": [
            {"id": "mu", "label": "动摩擦系数 μ_k", "value": "0.3", "step": "0.01"},
            {"id": "N", "label": "正压力 N", "value": "100", "step": "5", "unit": "N"},
        ],
        "calc": """
            const mu = num('mu'), N = num('N');
            ToolBox.setResult('result', dataGrid([
                [(mu * N).toFixed(2), '动摩擦力 F_k (N)']
            ]));
        """,
        "notes": ["F_k = μ_k·N。", "与接触面积无关。"],
    },
    {
        "slug": "static-friction-max", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "最大静摩擦力", "h1": "最大静摩擦力计算器",
        "h2": "F_{s,max} = μ_s·N",
        "intro": "物体即将滑动时的静摩擦力上限。",
        "desc": "最大静摩擦力：F_s,max = μ_s·N，输入静摩擦系数与正压力。",
        "inputs": [
            {"id": "mu", "label": "静摩擦系数 μ_s", "value": "0.5", "step": "0.01"},
            {"id": "N", "label": "正压力 N", "value": "100", "step": "5", "unit": "N"},
        ],
        "calc": """
            const mu = num('mu'), N = num('N');
            ToolBox.setResult('result', dataGrid([
                [(mu * N).toFixed(2), '最大静摩擦 (N)']
            ]));
        """,
        "notes": ["F_s,max = μ_s·N。", "静摩擦系数通常 > 动摩擦。"],
    },
    {
        "slug": "work-done", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "做功", "h1": "做功计算器",
        "h2": "W = F·d·cosθ",
        "intro": "力在位移方向分量所做的功。",
        "desc": "做功：W = F·d·cosθ，输入力、位移与夹角。",
        "inputs": [
            {"id": "F", "label": "力 F", "value": "50", "step": "1", "unit": "N"},
            {"id": "d", "label": "位移 d", "value": "10", "step": "0.5", "unit": "m"},
            {"id": "th", "label": "夹角 θ", "value": "0", "step": "5", "unit": "°"},
        ],
        "calc": """
            const F = num('F'), d = num('d'), th = num('th') * Math.PI / 180;
            ToolBox.setResult('result', dataGrid([
                [(F * d * Math.cos(th)).toFixed(2), '做功 W (J)']
            ]));
        """,
        "notes": ["W = Fd cosθ。", "θ=90° 时不做功。"],
    },
    {
        "slug": "kinetic-energy", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "动能", "h1": "动能计算器",
        "h2": "KE = ½·m·v²",
        "intro": "物体由于运动具有的能量。",
        "desc": "动能：KE = ½mv²，输入质量与速度。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "1500", "step": "50", "unit": "kg"},
            {"id": "v", "label": "速度 v", "value": "20", "step": "1", "unit": "m/s"},
        ],
        "calc": """
            const m = num('m'), v = num('v');
            const ke = 0.5 * m * v * v;
            ToolBox.setResult('result', dataGrid([
                [ke.toFixed(1), '动能 KE (J)'],
                [(ke / 1000).toFixed(2), 'KE (kJ)']
            ]));
        """,
        "notes": ["KE = ½mv²。", "1500 kg × 20²/2 = 300 kJ。"],
    },
    {
        "slug": "gravitational-potential", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "重力势能", "h1": "重力势能计算器",
        "h2": "PE = m·g·h",
        "intro": "由高度决定的势能。",
        "desc": "重力势能：PE = mgh，输入质量、重力加速度、高度。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "10", "step": "0.5", "unit": "kg"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
            {"id": "h", "label": "高度 h", "value": "5", "step": "0.5", "unit": "m"},
        ],
        "calc": """
            const m = num('m'), g = num('g'), h = num('h');
            ToolBox.setResult('result', dataGrid([
                [(m * g * h).toFixed(2), '势能 PE (J)']
            ]));
        """,
        "notes": ["PE = mgh。", "相对参考面而定。"],
    },
    {
        "slug": "spring-potential", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "弹簧势能", "h1": "弹簧势能计算器",
        "h2": "U = ½·k·x²",
        "intro": "弹簧形变储存的弹性势能。",
        "desc": "弹簧势能：U = ½kx²，输入劲度系数与形变量。",
        "inputs": [
            {"id": "k", "label": "劲度系数 k", "value": "200", "step": "10", "unit": "N/m"},
            {"id": "x", "label": "形变量 x", "value": "0.1", "step": "0.01", "unit": "m"},
        ],
        "calc": """
            const k = num('k'), x = num('x');
            ToolBox.setResult('result', dataGrid([
                [(0.5 * k * x * x).toFixed(3), '弹性势能 U (J)']
            ]));
        """,
        "notes": ["U = ½kx²。", "k=200、x=0.1 → 1 J。"],
    },
    {
        "slug": "impulse", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "冲量", "h1": "冲量计算器",
        "h2": "J = F·Δt = Δp",
        "intro": "力在时间上的累积等于动量变化。",
        "desc": "冲量：J = F·Δt，输入力与作用时间。",
        "inputs": [
            {"id": "F", "label": "力 F", "value": "100", "step": "5", "unit": "N"},
            {"id": "dt", "label": "作用时间 Δt", "value": "0.5", "step": "0.05", "unit": "s"},
        ],
        "calc": """
            const F = num('F'), dt = num('dt');
            ToolBox.setResult('result', dataGrid([
                [(F * dt).toFixed(2), '冲量 J (N·s)']
            ]));
        """,
        "notes": ["J = FΔt = Δp。", "单位等效动量 kg·m/s。"],
    },
    {
        "slug": "momentum", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "动量", "h1": "动量计算器",
        "h2": "p = m·v",
        "intro": "物体质量与速度的乘积。",
        "desc": "动量：p = mv，输入质量与速度。",
        "inputs": [
            {"id": "m", "label": "质量 m", "value": "1000", "step": "50", "unit": "kg"},
            {"id": "v", "label": "速度 v", "value": "15", "step": "1", "unit": "m/s"},
        ],
        "calc": """
            const m = num('m'), v = num('v');
            ToolBox.setResult('result', dataGrid([
                [(m * v).toFixed(1), '动量 p (kg·m/s)']
            ]));
        """,
        "notes": ["p = mv。", "矢量，方向同速度。"],
    },
    {
        "slug": "momentum-conservation", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "一维动量守恒", "h1": "完全非弹性碰撞计算器",
        "h2": "m₁v₁ + m₂v₂ = (m₁+m₂)·v′",
        "intro": "碰撞后粘在一起的末速度。",
        "desc": "一维动量守恒：v′ = (m₁v₁+m₂v₂)/(m₁+m₂)。",
        "inputs": [
            {"id": "m1", "label": "质量 m₁", "value": "1000", "step": "50", "unit": "kg"},
            {"id": "v1", "label": "速度 v₁", "value": "20", "step": "1", "unit": "m/s"},
            {"id": "m2", "label": "质量 m₂", "value": "1500", "step": "50", "unit": "kg"},
            {"id": "v2", "label": "速度 v₂", "value": "0", "step": "1", "unit": "m/s"},
        ],
        "calc": """
            const m1 = num('m1'), v1 = num('v1'), m2 = num('m2'), v2 = num('v2');
            const vp = (m1 * v1 + m2 * v2) / (m1 + m2);
            ToolBox.setResult('result', dataGrid([
                [vp.toFixed(3), '末速度 v′ (m/s)']
            ]));
        """,
        "notes": ["完全非弹性碰撞末速。", "动量守恒、动能不守恒。"],
    },
    {
        "slug": "power-force", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "功率", "h1": "功率计算器",
        "h2": "P = F·v",
        "intro": "力与速度方向一致时的功率。",
        "desc": "功率：P = F·v，输入力与速度。",
        "inputs": [
            {"id": "F", "label": "力 F", "value": "2000", "step": "50", "unit": "N"},
            {"id": "v", "label": "速度 v", "value": "10", "step": "0.5", "unit": "m/s"},
        ],
        "calc": """
            const F = num('F'), v = num('v');
            ToolBox.setResult('result', dataGrid([
                [(F * v).toFixed(1), '功率 P (W)'],
                [(F * v / 1000).toFixed(2), 'P (kW)']
            ]));
        """,
        "notes": ["P = Fv。", "2000 N × 10 = 20 kW。"],
    },
    {
        "slug": "torque-force", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "力矩", "h1": "力矩计算器",
        "h2": "τ = r·F·sinθ",
        "intro": "力对转轴的转动效应。",
        "desc": "力矩：τ = rF sinθ，输入力臂、力与夹角。",
        "inputs": [
            {"id": "r", "label": "力臂 r", "value": "0.5", "step": "0.05", "unit": "m"},
            {"id": "F", "label": "力 F", "value": "100", "step": "5", "unit": "N"},
            {"id": "th", "label": "夹角 θ", "value": "90", "step": "5", "unit": "°"},
        ],
        "calc": """
            const r = num('r'), F = num('F'), th = num('th') * Math.PI / 180;
            ToolBox.setResult('result', dataGrid([
                [(r * F * Math.sin(th)).toFixed(2), '力矩 τ (N·m)']
            ]));
        """,
        "notes": ["τ = rF sinθ。", "垂直时 τ=rF 最大。"],
    },
    {
        "slug": "inclined-plane-accel", "industry": "dynamics", "cat": "dynamics", "icon": "💥", "bg": "#f0f9ff",
        "title": "斜面加速度", "h1": "斜面下滑加速度计算器",
        "h2": "a = g·(sinθ − μ·cosθ)",
        "intro": "考虑摩擦的斜面下滑加速度。",
        "desc": "斜面加速度：a = g(sinθ − μcosθ)，输入倾角、摩擦系数、重力。",
        "inputs": [
            {"id": "th", "label": "倾角 θ", "value": "30", "step": "1", "unit": "°"},
            {"id": "mu", "label": "摩擦系数 μ", "value": "0.1", "step": "0.01"},
            {"id": "g", "label": "重力加速度 g", "value": "9.8", "step": "0.1", "unit": "m/s²"},
        ],
        "calc": """
            const th = num('th') * Math.PI / 180, mu = num('mu'), g = num('g');
            const a = g * (Math.sin(th) - mu * Math.cos(th));
            ToolBox.setResult('result', dataGrid([
                [a.toFixed(3), '加速度 a (m/s²)'],
                [(a > 0 ? '向下滑' : '静止/需外力') , '状态']
            ]));
        """,
        "notes": ["a = g(sinθ − μcosθ)。", "θ 过小且 μ 大则不下溜。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
