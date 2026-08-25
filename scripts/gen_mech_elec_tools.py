#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch 7 — 机械/电气工程计算深化
批量生成 mechanical(机械) + electrical(电气) A 级专业计算工具页（填补现有行业内的空白主题）。

复用 Batch 6 的成熟模板（TEMPLATE 占位符 + TOOLS 字典 + render 系列），
每个工具含正确 <meta name="toolbox">、唯一 id="result"、真实工程计算公式（达 A 级）。

用法：python3 scripts/gen_mech_elec_tools.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")

CAT_ZH = {"mechanical": "机械工程", "electrical": "电气工程"}

# 工具定义列表（slug 均不与现有 mechanical/electrical 工具冲突）
TOOLS = [
    # ===================== mechanical（机械） =====================
    {
        "slug": "spring-rate", "industry": "mechanical", "cat": "engineer",
        "icon": "⚙️", "bg": "#dbeafe",
        "title": "圆柱螺旋弹簧刚度计算（机械）",
        "h1": "圆柱螺旋弹簧刚度计算",
        "h2": "⚙️ 圆柱螺旋弹簧刚度计算（机械）",
        "intro": "按材料力学公式由线径、中径、有效圈数计算圆柱螺旋压缩弹簧的轴向刚度。",
        "desc": "圆柱螺旋弹簧刚度计算 - 依据弹簧刚度公式 k=G·d⁴/(8D³n) 计算轴向刚度。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "d", "label": "弹簧线径 d (mm)", "value": "5", "step": "0.5", "min": "0.1"},
            {"id": "D", "label": "弹簧中径 D (mm)", "value": "30", "step": "1", "min": "1"},
            {"id": "n", "label": "有效圈数 n", "value": "6", "step": "0.5", "min": "1"},
            {"id": "G", "label": "剪切模量 G (GPa)", "value": "79", "step": "1", "min": "1"},
        ],
        "calc": r"""
            const d=num('d'), D=num('D'), n=num('n'), G=num('G')*1000; // G: GPa->N/mm²
            if(d<=0||D<=0||n<=0||G<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的弹簧参数。</p>');return;}
            const k=G*Math.pow(d,4)/(8*Math.pow(D,3)*n); // N/mm
            ToolBox.setResult('result', dataGrid([
                [k.toFixed(2),'弹簧刚度 k (N/mm)'],
                [(k*1000).toFixed(0),'弹簧刚度 k (N/m)']
            ]));
        """,
        "notes": [
            "k = G·d⁴ / (8·D³·n)（圆柱螺旋弹簧轴向刚度）",
            "G 取材料剪切模量：钢 ≈79 GPa，不锈钢 ≈73 GPa",
            "d 为线径、D 为中径、n 为有效圈数",
        ],
    },
    {
        "slug": "centrifugal-force", "industry": "mechanical", "cat": "engineer",
        "icon": "⚙️", "bg": "#dbeafe",
        "title": "离心力计算（机械）",
        "h1": "离心力计算",
        "h2": "⚙️ 离心力计算（机械）",
        "intro": "由质量、旋转半径与转速计算旋转体的离心力（惯性力）。",
        "desc": "离心力计算 - 依据 F=m·ω²·r 由质量、半径与转速计算离心力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "m", "label": "质量 m (kg)", "value": "10", "step": "0.5", "min": "0"},
            {"id": "r", "label": "旋转半径 r (m)", "value": "0.5", "step": "0.05", "min": "0"},
            {"id": "rpm", "label": "转速 n (rpm)", "value": "600", "step": "10", "min": "0"},
        ],
        "calc": r"""
            const m=num('m'), r=num('r'), rpm=num('rpm');
            if(m<0||r<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数（半径须>0）。</p>');return;}
            const w=2*Math.PI*rpm/60; // rad/s
            const F=m*w*w*r; // N
            ToolBox.setResult('result', dataGrid([
                [F.toFixed(1),'离心力 F (N)'],
                [(F/1000).toFixed(2),'离心力 F (kN)'],
                [w.toFixed(2),'角速度 ω (rad/s)']
            ]));
        """,
        "notes": [
            "F = m·ω²·r，ω = 2πn/60（n 为 rpm）",
            "离心力与转速平方成正比，高速旋转时迅速增大",
            "常用于转子动平衡、离心机设计",
        ],
    },
    {
        "slug": "flywheel-energy", "industry": "mechanical", "cat": "engineer",
        "icon": "⚙️", "bg": "#dbeafe",
        "title": "飞轮转动动能计算（机械）",
        "h1": "飞轮转动动能计算",
        "h2": "⚙️ 飞轮转动动能计算（机械）",
        "intro": "由飞轮质量、半径与转速估算其储存的转动动能（实心圆盘模型）。",
        "desc": "飞轮转动动能计算 - 依据 E=½Iω² 估算飞轮储能。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "m", "label": "质量 m (kg)", "value": "50", "step": "1", "min": "0"},
            {"id": "r", "label": "半径 r (m)", "value": "0.3", "step": "0.05", "min": "0"},
            {"id": "rpm", "label": "转速 n (rpm)", "value": "1000", "step": "10", "min": "0"},
        ],
        "calc": r"""
            const m=num('m'), r=num('r'), rpm=num('rpm');
            if(m<0||r<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数（半径须>0）。</p>');return;}
            const I=0.5*m*r*r; // kg·m² (实心圆盘)
            const w=2*Math.PI*rpm/60;
            const E=0.5*I*w*w; // J
            ToolBox.setResult('result', dataGrid([
                [I.toFixed(3),'转动惯量 I (kg·m²)'],
                [E.toFixed(1),'转动动能 E (J)'],
                [(E/1000).toFixed(2),'转动动能 E (kJ)']
            ]));
        """,
        "notes": [
            "E = ½·I·ω²（实心圆盘 I = ½mr²）",
            "飞轮用于平滑转速波动、回收制动能量",
            "储能与转速平方成正比",
        ],
    },
    {
        "slug": "gear-ratio", "industry": "mechanical", "cat": "engineer",
        "icon": "⚙️", "bg": "#dbeafe",
        "title": "齿轮传动比计算（机械）",
        "h1": "齿轮传动比计算",
        "h2": "⚙️ 齿轮传动比计算（机械）",
        "intro": "由主从动齿轮齿数计算传动比，并推算输出转速与转矩。",
        "desc": "齿轮传动比计算 - 依据 i=z₂/z₁ 计算传动比及输出转速、转矩。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "z1", "label": "主动轮齿数 z₁", "value": "20", "step": "1", "min": "1"},
            {"id": "z2", "label": "从动轮齿数 z₂", "value": "40", "step": "1", "min": "1"},
            {"id": "n1", "label": "主动轮转速 n₁ (rpm)", "value": "1500", "step": "10", "min": "0"},
            {"id": "T1", "label": "主动轮转矩 T₁ (N·m)", "value": "100", "step": "1", "min": "0"},
            {"id": "eta", "label": "传动效率 η", "value": "0.97", "step": "0.01", "min": "0", "max": "1"},
        ],
        "calc": r"""
            const z1=num('z1'), z2=num('z2'), n1=num('n1'), T1=num('T1'), eta=num('eta');
            if(z1<=0||z2<=0){ToolBox.setResult('result','<p class="tip-error">齿数须>0。</p>');return;}
            const i=z2/z1;
            const n2=n1/i;
            const T2=T1*i*eta;
            ToolBox.setResult('result', dataGrid([
                [i.toFixed(3),'传动比 i (=z₂/z₁)'],
                [n2.toFixed(1),'输出转速 n₂ (rpm)'],
                [T2.toFixed(1),'输出转矩 T₂ (N·m)']
            ]));
        """,
        "notes": [
            "i = z₂/z₁；减速时 z₂>z₁（i>1），增速时相反",
            "n₂ = n₁/i，T₂ = T₁·i·η",
            "η 取齿轮传动效率（单级约 0.95~0.98）",
        ],
    },
    {
        "slug": "lever-advantage", "industry": "mechanical", "cat": "engineer",
        "icon": "⚙️", "bg": "#dbeafe",
        "title": "杠杆机械增益计算（机械）",
        "h1": "杠杆机械增益计算",
        "h2": "⚙️ 杠杆机械增益计算（机械）",
        "intro": "由动力臂与阻力臂长度计算杠杆的机械增益（省力倍数）。",
        "desc": "杠杆机械增益计算 - 依据 MA=L_动力/L_阻力 计算机械增益。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "Lin", "label": "动力臂 L₁ (m)", "value": "1.0", "step": "0.05", "min": "0"},
            {"id": "Lout", "label": "阻力臂 L₂ (m)", "value": "0.2", "step": "0.05", "min": "0"},
        ],
        "calc": r"""
            const Lin=num('Lin'), Lout=num('Lout');
            if(Lin<=0||Lout<=0){ToolBox.setResult('result','<p class="tip-error">臂长须>0。</p>');return;}
            const MA=Lin/Lout;
            ToolBox.setResult('result', dataGrid([
                [MA.toFixed(2),'机械增益 MA (=L₁/L₂)'],
                [(1/MA).toFixed(2),'所需动力 / 阻力']
            ]));
        """,
        "notes": [
            "MA = L₁/L₂（动力臂/阻力臂）",
            "MA>1 省力，代价是动力端位移更大",
            "滑轮组机械增益约等于承重绳段数 n",
        ],
    },
    {
        "slug": "beam-point-load", "industry": "mechanical", "cat": "engineer",
        "icon": "⚙️", "bg": "#dbeafe",
        "title": "简支梁跨中集中力计算（机械）",
        "h1": "简支梁跨中集中力计算",
        "h2": "⚙️ 简支梁跨中集中力计算（机械）",
        "intro": "计算受跨中集中力的简支梁的最大弯矩、跨中挠度与弯曲应力。",
        "desc": "简支梁跨中集中力计算 - 依据材料力学公式计算最大弯矩、跨中挠度与弯曲应力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "L", "label": "跨度 L (m)", "value": "4", "step": "0.1", "min": "0.1"},
            {"id": "F", "label": "集中力 F (kN)", "value": "10", "step": "0.5", "min": "0"},
            {"id": "E", "label": "弹性模量 E (GPa)", "value": "30", "step": "1", "min": "1"},
            {"id": "I", "label": "截面惯性矩 I (cm⁴)", "value": "5000", "step": "100", "min": "1"},
            {"id": "b", "label": "截面宽 b (mm)", "value": "150", "step": "5", "min": "1"},
            {"id": "h", "label": "截面高 h (mm)", "value": "300", "step": "5", "min": "1"},
        ],
        "calc": r"""
            const L=num('L'), F=num('F'), E=num('E')*1000, I=num('I')*1e4, b=num('b'), h=num('h');
            if(L<=0||E<=0||I<=0||b<=0||h<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的梁参数。</p>');return;}
            const Mmax=F*L/4;                                  // kN·m
            const delta=F*1000*Math.pow(L*1000,3)/(48*E*I);    // mm (统一 N/mm)
            const W=b*h*h/6;                                   // mm³
            const sigma=Mmax*1e6/W;                            // MPa
            ToolBox.setResult('result', dataGrid([
                [Mmax.toFixed(2),'最大弯矩 M (kN·m)'],
                [delta.toFixed(2),'跨中挠度 δ (mm)'],
                [sigma.toFixed(2),'跨中弯曲应力 σ (MPa)']
            ]));
        """,
        "notes": [
            "跨中集中力：M_max = FL/4，δ = FL³/(48EI)",
            "单位统一为 N、mm、N/mm²（E: GPa→×1000，I: cm⁴→×1e4）",
            "σ = M/W，W = bh²/6 为矩形截面模量",
        ],
    },
    {
        "slug": "torque-power", "industry": "mechanical", "cat": "engineer",
        "icon": "⚙️", "bg": "#dbeafe",
        "title": "转矩-功率-转速换算（机械）",
        "h1": "转矩-功率-转速换算",
        "h2": "⚙️ 转矩-功率-转速换算（机械）",
        "intro": "由功率与转速换算旋转轴的输出转矩（及角速度）。",
        "desc": "转矩-功率-转速换算 - 依据 T=9550·P/n 由功率与转速计算转矩。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "P", "label": "功率 P (kW)", "value": "7.5", "step": "0.1", "min": "0"},
            {"id": "n", "label": "转速 n (rpm)", "value": "1450", "step": "10", "min": "0"},
        ],
        "calc": r"""
            const P=num('P'), n=num('n');
            if(n<=0){ToolBox.setResult('result','<p class="tip-error">转速须>0。</p>');return;}
            const T=9550*P/n;               // N·m
            const w=2*Math.PI*n/60;         // rad/s
            ToolBox.setResult('result', dataGrid([
                [T.toFixed(1),'转矩 T (N·m)'],
                [w.toFixed(2),'角速度 ω (rad/s)'],
                [(T*w/1000).toFixed(1),'校验功率 P (kW)']
            ]));
        """,
        "notes": [
            "T = 9550·P/n（P:kW，n:rpm，T:N·m）",
            "亦可用 T = P/ω（P:W，ω:rad/s）",
            "校验行 P=T·ω/1000 应回等于输入功率",
        ],
    },
    # ===================== electrical（电气） =====================
    {
        "slug": "voltage-divider", "industry": "electrical", "cat": "calculator",
        "icon": "🔌", "bg": "#fef9c3",
        "title": "电阻分压器计算（电气）",
        "h1": "电阻分压器计算",
        "h2": "🔌 电阻分压器计算（电气）",
        "intro": "计算由两个串联电阻构成的分压器输出电压。",
        "desc": "电阻分压器计算 - 依据 Vout=Vin·R₂/(R₁+R₂) 计算分压输出。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "Vin", "label": "输入电压 V_in (V)", "value": "12", "step": "0.5", "min": "0"},
            {"id": "R1", "label": "上电阻 R₁ (Ω)", "value": "1000", "step": "10", "min": "0"},
            {"id": "R2", "label": "下电阻 R₂ (Ω)", "value": "2000", "step": "10", "min": "0"},
        ],
        "calc": r"""
            const Vin=num('Vin'), R1=num('R1'), R2=num('R2');
            if(R1+R2<=0){ToolBox.setResult('result','<p class="tip-error">电阻和须>0。</p>');return;}
            const Vout=Vin*R2/(R1+R2);
            ToolBox.setResult('result', dataGrid([
                [Vout.toFixed(2),'输出电压 V_out (V)'],
                [(Vout/Vin*100).toFixed(1),'分压比 (%)']
            ]));
        """,
        "notes": [
            "V_out = V_in·R₂/(R₁+R₂)",
            "空载理想分压；带负载时输出会下降",
            "常用作传感器信号调理、基准偏置",
        ],
    },
    {
        "slug": "current-divider", "industry": "electrical", "cat": "calculator",
        "icon": "🔌", "bg": "#fef9c3",
        "title": "电流分流器计算（电气）",
        "h1": "电流分流器计算",
        "h2": "🔌 电流分流器计算（电气）",
        "intro": "计算两个并联电阻各自分得的电流。",
        "desc": "电流分流器计算 - 依据并联分流公式 I_x=I·R_总/R_x 计算各支路电流。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "It", "label": "总电流 I_t (mA)", "value": "100", "step": "1", "min": "0"},
            {"id": "R1", "label": "支路电阻 R₁ (Ω)", "value": "1000", "step": "10", "min": "0"},
            {"id": "R2", "label": "支路电阻 R₂ (Ω)", "value": "2000", "step": "10", "min": "0"},
        ],
        "calc": r"""
            const It=num('It'), R1=num('R1'), R2=num('R2');
            if(R1<=0||R2<=0){ToolBox.setResult('result','<p class="tip-error">电阻须>0。</p>');return;}
            const I1=It*R2/(R1+R2); // 流经 R1
            const I2=It*R1/(R1+R2); // 流经 R2
            ToolBox.setResult('result', dataGrid([
                [I1.toFixed(2),'支路 R₁ 电流 I₁ (mA)'],
                [I2.toFixed(2),'支路 R₂ 电流 I₂ (mA)'],
                [(I1+I2).toFixed(2),'电流合计 (mA)']
            ]));
        """,
        "notes": [
            "并联分流：I₁ = I_t·R₂/(R₁+R₂)，I₂ = I_t·R₁/(R₁+R₂)",
            "电阻越小，分流越大",
            "合计应等于输入总电流（校验用）",
        ],
    },
    {
        "slug": "rc-filter", "industry": "electrical", "cat": "calculator",
        "icon": "🔌", "bg": "#fef9c3",
        "title": "RC 低通滤波截止频率计算（电气）",
        "h1": "RC 低通滤波截止频率计算",
        "h2": "🔌 RC 低通滤波截止频率计算（电气）",
        "intro": "由电阻与电容计算一阶 RC 低通滤波器的截止频率。",
        "desc": "RC 低通滤波截止频率计算 - 依据 fc=1/(2πRC) 计算截止频率。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "R", "label": "电阻 R (kΩ)", "value": "10", "step": "0.5", "min": "0"},
            {"id": "C", "label": "电容 C (µF)", "value": "0.1", "step": "0.01", "min": "0"},
        ],
        "calc": r"""
            const R=num('R')*1000, C=num('C')*1e-6; // Ω, F
            if(R<=0||C<=0){ToolBox.setResult('result','<p class="tip-error">R、C 须>0。</p>');return;}
            const fc=1/(2*Math.PI*R*C);
            ToolBox.setResult('result', dataGrid([
                [fc.toFixed(1),'截止频率 f_c (Hz)'],
                [(fc/1000).toFixed(3),'截止频率 f_c (kHz)']
            ]));
        """,
        "notes": [
            "f_c = 1/(2πRC)",
            "高于 f_c 的信号按 -20dB/十倍频衰减",
            "常用于电源去耦、抗混叠前置滤波",
        ],
    },
    {
        "slug": "led-resistor", "industry": "electrical", "cat": "calculator",
        "icon": "🔌", "bg": "#fef9c3",
        "title": "LED 限流电阻计算（电气）",
        "h1": "LED 限流电阻计算",
        "h2": "🔌 LED 限流电阻计算（电气）",
        "intro": "由电源电压、LED 正向压降与额定电流计算所需限流电阻及功耗。",
        "desc": "LED 限流电阻计算 - 依据 R=(V_s−V_f)/I_f 计算限流电阻。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "Vs", "label": "电源电压 V_s (V)", "value": "5", "step": "0.5", "min": "0"},
            {"id": "Vf", "label": "LED 正向压降 V_f (V)", "value": "2.0", "step": "0.1", "min": "0"},
            {"id": "If", "label": "正向电流 I_f (mA)", "value": "20", "step": "1", "min": "0"},
        ],
        "calc": r"""
            const Vs=num('Vs'), Vf=num('Vf'), If=num('If')/1000; // A
            if(If<=0){ToolBox.setResult('result','<p class="tip-error">电流须>0。</p>');return;}
            if(Vs<=Vf){ToolBox.setResult('result','<p class="tip-error">电源电压须大于 LED 压降。</p>');return;}
            const R=(Vs-Vf)/If;          // Ω
            const P=Math.pow(If,2)*R;     // W
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(0),'限流电阻 R (Ω)'],
                [(R*1.5).toFixed(0),'建议标称值 (~1.5×) (Ω)'],
                [(P*1000).toFixed(1),'电阻功耗 P (mW)']
            ]));
        """,
        "notes": [
            "R = (V_s−V_f)/I_f",
            "实际选阻值应 ≥ 计算值并留余量（防过流）",
            "功耗 P = I_f²·R，据此选电阻功率档",
        ],
    },
    {
        "slug": "opamp-gain", "industry": "electrical", "cat": "calculator",
        "icon": "🔌", "bg": "#fef9c3",
        "title": "运算放大器增益计算（电气）",
        "h1": "运算放大器增益计算",
        "h2": "🔌 运算放大器增益计算（电气）",
        "intro": "计算反相与同相放大电路的闭环电压增益。",
        "desc": "运算放大器增益计算 - 依据反相 A_v=−R_f/R_in、同相 A_v=1+R_f/R_in 计算增益。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "Rin", "label": "输入电阻 R_in (Ω)", "value": "1000", "step": "10", "min": "0"},
            {"id": "Rf", "label": "反馈电阻 R_f (Ω)", "value": "10000", "step": "100", "min": "0"},
        ],
        "calc": r"""
            const Rin=num('Rin'), Rf=num('Rf');
            if(Rin<=0||Rf<0){ToolBox.setResult('result','<p class="tip-error">R_in 须>0。</p>');return;}
            const Av_inv=-Rf/Rin;
            const Av_non=1+Rf/Rin;
            ToolBox.setResult('result', dataGrid([
                [Av_inv.toFixed(2),'反相增益 A_v (=−R_f/R_in)'],
                [Av_non.toFixed(2),'同相增益 A_v (=1+R_f/R_in)']
            ]));
        """,
        "notes": [
            "反相：A_v = −R_f/R_in",
            "同相：A_v = 1+R_f/R_in",
            "理想运放、深度负反馈近似；实际受带宽/摆率限制",
        ],
    },
    {
        "slug": "rlc-resonance", "industry": "electrical", "cat": "calculator",
        "icon": "🔌", "bg": "#fef9c3",
        "title": "RLC 串联谐振频率计算（电气）",
        "h1": "RLC 串联谐振频率计算",
        "h2": "🔌 RLC 串联谐振频率计算（电气）",
        "intro": "由电感与电容计算 RLC 串联电路的谐振频率。",
        "desc": "RLC 串联谐振频率计算 - 依据 f₀=1/(2π√LC) 计算谐振频率。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "L", "label": "电感 L (mH)", "value": "10", "step": "0.5", "min": "0"},
            {"id": "C", "label": "电容 C (µF)", "value": "0.1", "step": "0.01", "min": "0"},
        ],
        "calc": r"""
            const L=num('L')/1000, C=num('C')*1e-6; // H, F
            if(L<=0||C<=0){ToolBox.setResult('result','<p class="tip-error">L、C 须>0。</p>');return;}
            const f0=1/(2*Math.PI*Math.sqrt(L*C));
            ToolBox.setResult('result', dataGrid([
                [f0.toFixed(1),'谐振频率 f₀ (Hz)'],
                [(f0/1000).toFixed(3),'谐振频率 f₀ (kHz)']
            ]));
        """,
        "notes": [
            "f₀ = 1/(2π√LC)",
            "谐振时感抗与容抗相等，回路阻抗最小",
            "用于选频、滤波、振荡电路设计",
        ],
    },
    {
        "slug": "wire-resistance", "industry": "electrical", "cat": "calculator",
        "icon": "🔌", "bg": "#fef9c3",
        "title": "导线电阻计算（电气）",
        "h1": "导线电阻计算",
        "h2": "🔌 导线电阻计算（电气）",
        "intro": "由材料电阻率、长度与截面积计算导线直流电阻。",
        "desc": "导线电阻计算 - 依据 R=ρL/A 计算导线电阻。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "rho", "label": "电阻率 ρ (Ω·mm²/m)", "value": "0.0172", "step": "0.001", "min": "0"},
            {"id": "L", "label": "长度 L (m)", "value": "100", "step": "1", "min": "0"},
            {"id": "A", "label": "截面积 A (mm²)", "value": "2.5", "step": "0.1", "min": "0"},
        ],
        "calc": r"""
            const rho=num('rho'), L=num('L'), A=num('A');
            if(A<=0||L<0||rho<0){ToolBox.setResult('result','<p class="tip-error">参数须有效。</p>');return;}
            const R=rho*L/A;
            ToolBox.setResult('result', dataGrid([
                [R.toFixed(3),'导线电阻 R (Ω)'],
                [(R*1000/L).toFixed(2),'每千米电阻 (Ω/km)']
            ]));
        """,
        "notes": [
            "R = ρ·L/A（铜 ρ≈0.0172，铝 ≈0.0283 Ω·mm²/m）",
            "电阻随温度升高而增大",
            "长距离输电需校核压降与发热",
        ],
    },
]


TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<!-- toolbox-theme-bootstrap -->
<!-- toolbox-sw-register --><script>if("serviceWorker"in navigator){window.addEventListener("load",function(){navigator.serviceWorker.register("/sw.js").catch(function(){});});}</script><script>(function(){try{var t=localStorage.getItem("theme");if(!t&&window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches){t="dark";}if(t==="dark"){document.documentElement.setAttribute("data-theme","dark");}}catch(e){}})();</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="toolbox" content="cat=__CAT__,industry=__INDUSTRY__,icon=__ICON__,bg=__BG__">
<title>__TITLE__ - ToolBox</title>
<link rel="canonical" href="https://chenguangwu.github.io/tools/__INDUSTRY__/__SLUG__.html">
<meta property="og:title" content="__TITLE__">
<meta property="og:description" content="__DESC__">
<meta property="og:url" content="https://chenguangwu.github.io/tools/__INDUSTRY__/__SLUG__.html">
<meta name="twitter:card" content="summary">
<meta name="description" content="__DESC__">
<link rel="stylesheet" href="../../css/common.css">
<script src="../../js/common.js"></script>

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://chenguangwu.github.io/"},{"@type":"ListItem","position":2,"name":"__CATZH__","item":"https://chenguangwu.github.io/tools/__INDUSTRY__/index.html"},{"@type":"ListItem","position":3,"name":"__TITLE__","item":"https://chenguangwu.github.io/tools/__INDUSTRY__/__SLUG__.html"}]}
</script>

<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 6000+免费在线工具">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 6000+免费在线工具">
    <meta property="og:type" content="website">
    <meta name="twitter:title" content="__TITLE__">
    <meta name="twitter:description" content="__DESC__">

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"__TITLE__","url":"https://chenguangwu.github.io/tools/__INDUSTRY__/__SLUG__.html","applicationCategory":"UtilitiesApplication","operatingSystem":"Any","browserRequirements":"Requires JavaScript","description":"__TITLE__","image":"https://chenguangwu.github.io/og-image.png","offers":{"@type":"Offer","price":"0","priceCurrency":"CNY"}}
</script>

<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">
<!-- TOOLBOX-SECURITY -->

<script src="/js/privacy.js" defer></script>
<!-- TOOLBOX-PRIVACY-SCRIPT -->

<script src="/js/metrics.js" defer></script>
<!-- TOOLBOX-METRICS-SCRIPT -->
</head>
<body>

<h1 class="sr-only">__H1__</h1>

<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ __TITLE__</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>



<nav class="breadcrumb" aria-label="面包屑导航" data-breadcrumb="1">
  <a href="../../index.html">首页</a>
  <span class="bc-sep">‹</span>
  <a href="index.html">🔧 __CATZH__</a>
  <span class="bc-sep">‹</span>
  <span class="bc-current">__TITLE__ | ToolBox免费在线工具箱</span>
</nav>
<div class="container">
  <div class="card">
    <h2>__H2__</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">__INTRO__</p>

__INPUTS__

    <div class="toolbar">
      <button class="btn primary" onclick="calcTool()">计算</button>
      <button class="btn" onclick="resetForm()">重置</button>
    </div>

    <div class="result-box" id="result"></div>

    <div class="tool-notes">
      <div class="tool-notes-title">📌 计算说明</div>
      <ul>
__NOTES__
      </ul>
    </div>
  </div>
</div>

<script>
function num(id){const v=parseFloat(document.getElementById(id).value);return isNaN(v)?0:v;}
function dataGrid(rows){let h='<div class="data-grid">';for(const r of rows){h+='<div class="data-card"><div class="num">'+r[0]+'</div><div class="label">'+r[1]+'</div></div>';}return h+'</div>';}
function calcTool(){__CALC__}
function resetForm(){__RESET__}
calcTool();
</script>
</body>
</html>
"""


def render_inputs(tool):
    rows = []
    ins = tool["inputs"]
    for i in range(0, len(ins), 3):
        chunk = ins[i:i + 3]
        cells = []
        for f in chunk:
            unit = (" (" + f.get("unit", "") + ")") if f.get("unit") else ""
            minv = f.get("min", "")
            maxv = f.get("max", "")
            extra = ""
            if minv != "":
                extra += ' min="%s"' % minv
            if maxv != "":
                extra += ' max="%s"' % maxv
            cells.append(
                '      <div>\n'
                '        <label for="%s">%s%s</label>\n'
                '        <input type="number" id="%s" value="%s" step="%s"%s>\n'
                '      </div>' % (f["id"], f["label"], unit, f["id"], f["value"], f["step"], extra)
            )
        rows.append('    <div class="input-row">\n' + "\n".join(cells) + '\n    </div>')
    return "\n".join(rows)


def render_reset(tool):
    lines = []
    for f in tool["inputs"]:
        lines.append("document.getElementById('%s').value = %s;" % (f["id"], repr(f["value"])))
    lines.append("calcTool();")
    return "\n      ".join(lines)


def render_notes(tool):
    return "\n".join("        <li>%s</li>" % n for n in tool["notes"])


def render(tool):
    return (TEMPLATE
            .replace("__CAT__", tool["cat"])
            .replace("__INDUSTRY__", tool["industry"])
            .replace("__ICON__", tool["icon"])
            .replace("__BG__", tool["bg"])
            .replace("__SLUG__", tool["slug"])
            .replace("__TITLE__", tool["title"])
            .replace("__H1__", tool["h1"])
            .replace("__H2__", tool["h2"])
            .replace("__INTRO__", tool["intro"])
            .replace("__DESC__", tool["desc"])
            .replace("__CATZH__", CAT_ZH[tool["industry"]])
            .replace("__INPUTS__", render_inputs(tool))
            .replace("__CALC__", tool["calc"])
            .replace("__RESET__", render_reset(tool))
            .replace("__NOTES__", render_notes(tool)))


def main():
    count = 0
    for tool in TOOLS:
        out_dir = os.path.join(TOOLS_DIR, tool["industry"])
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, tool["slug"] + ".html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(render(tool))
        count += 1
        print("  + tools/%s/%s.html" % (tool["industry"], tool["slug"]))
    print("共生成 %d 个工具页" % count)


if __name__ == "__main__":
    main()
