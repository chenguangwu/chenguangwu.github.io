#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch 6 — 工程建造计算深化
批量生成 civil(土木) + engineering(工程) A 级专业计算工具页。

每个工具基于现有工具页模板（tools/civil/calc-1.html）生成，包含：
  - 正确的 <meta name="toolbox">（cat/industry/icon/bg），供 _build.py 自动索引
  - 唯一的 id="result"（避免 id 冲突历史 bug）
  - 真实工程计算公式（独立 JS 计算逻辑，达 A 级专业标准）

用法：python3 scripts/gen_civil_eng_tools.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools")

CAT_ZH = {"civil": "土木工程", "engineering": "工程计算"}

# 工具定义列表
TOOLS = [
    # ===================== civil（土木） =====================
    {
        "slug": "beam-udl", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "简支梁均布荷载内力计算（土木）",
        "h1": "简支梁均布荷载内力计算",
        "h2": "🏗️ 简支梁均布荷载内力计算（土木）",
        "intro": "计算受均布荷载简支梁的最大弯矩、剪力、跨中挠度与跨中弯曲应力。",
        "desc": "简支梁均布荷载内力计算 - 按材料力学公式计算最大弯矩、剪力、跨中挠度与弯曲应力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "L", "label": "跨度 L (m)", "value": "6", "step": "0.1", "min": "0.1"},
            {"id": "q", "label": "均布荷载 q (kN/m)", "value": "20", "step": "0.5", "min": "0"},
            {"id": "E", "label": "弹性模量 E (GPa)", "value": "30", "step": "1", "min": "1"},
            {"id": "I", "label": "截面惯性矩 I (cm⁴)", "value": "8000", "step": "100", "min": "1"},
            {"id": "b", "label": "截面宽 b (mm)", "value": "200", "step": "5", "min": "1"},
            {"id": "h", "label": "截面高 h (mm)", "value": "400", "step": "5", "min": "1"},
        ],
        "calc": r"""
            const L=num('L'), q=num('q'), E=num('E')*1e9, I=num('I')*1e-8, b=num('b'), h=num('h');
            if(L<=0||q<0||E<=0||I<=0||b<=0||h<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的梁参数。</p>');return;}
            const Mmax = q*L*L/8;               // kN·m
            const Vmax = q*L/2;                 // kN
            const delta = 5*q*1000*Math.pow(L,4)/(384*E*I)*1000; // m -> mm (q 转 N/m)
            const W = b*Math.pow(h,2)/6;        // mm^3 截面模量 W = bh²/6
            const sigma = Mmax*1e6/W;           // MPa (M:kN·m -> N·mm = ×1e6)
            const html = dataGrid([
                [Mmax.toFixed(2),'最大弯矩 (kN·m)'],
                [Vmax.toFixed(2),'最大剪力 (kN)'],
                [delta.toFixed(2),'跨中挠度 (mm)'],
                [sigma.toFixed(2),'跨中弯曲应力 (MPa)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "最大弯矩 M<sub>max</sub> = qL²/8（跨中）",
            "最大剪力 V<sub>max</sub> = qL/2（支座处）",
            "跨中挠度 δ = 5qL⁴/(384EI)（单位统一为 N、m）",
            "弯曲应力 σ = M/W，W = bh²/6 为截面模量",
        ],
    },
    {
        "slug": "rc-beam-rebar", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "矩形截面梁受弯配筋计算（土木）",
        "h1": "矩形截面梁受弯配筋计算",
        "h2": "🏗️ 矩形截面梁受弯配筋计算（土木）",
        "intro": "按单筋矩形截面受弯构件，由弯矩设计值计算所需受拉钢筋面积。",
        "desc": "矩形截面梁受弯配筋计算 - 依据混凝土结构设计原理，由弯矩计算所需受拉钢筋面积。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "M", "label": "弯矩设计值 M (kN·m)", "value": "150", "step": "1", "min": "0"},
            {"id": "b", "label": "截面宽 b (mm)", "value": "250", "step": "5", "min": "1"},
            {"id": "h", "label": "截面高 h (mm)", "value": "500", "step": "5", "min": "1"},
            {"id": "fc", "label": "混凝土强度 f_c (MPa)", "value": "14.3", "step": "0.1", "min": "1"},
            {"id": "fy", "label": "钢筋强度 f_y (MPa)", "value": "360", "step": "5", "min": "1"},
            {"id": "as", "label": "保护层 a_s (mm)", "value": "40", "step": "5", "min": "10"},
        ],
        "calc": r"""
            const M=num('M')*1e6, b=num('b'), h=num('h'), fc=num('fc'), fy=num('fy'), as_=num('as');
            const a1=1.0; const h0=h-as_;
            if(M<=0||b<=0||h0<=0||fc<=0||fy<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的截面与内力参数。</p>');return;}
            const alphaS = M/(a1*fc*b*h0*h0);
            if(alphaS>0.44){ToolBox.setResult('result','<p class="tip-error">α_s 超限，需增大截面或改为双筋截面。</p>');return;}
            const xi = 1-Math.sqrt(1-2*alphaS);
            const As = xi*a1*fc*b*h0/fy;
            const html = dataGrid([
                [alphaS.toFixed(4),'α_s'],
                [xi.toFixed(4),'相对受压区高度 ξ'],
                [As.toFixed(0),'受拉钢筋面积 A_s (mm²)'],
                [(As/(b*h0)*100).toFixed(2),'配筋率 ρ (%)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "α_s = M / (α₁·f_c·b·h₀²)，h₀ = h − a_s",
            "ξ = 1 − √(1 − 2α_s)，单筋适筋上限 ξ_b ≈ 0.44（HRB400）",
            "A_s = ξ·α₁·f_c·b·h₀ / f_y",
            "结果仅供初步估算，实际设计按规范并考虑构造要求",
        ],
    },
    {
        "slug": "isolated-footing", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "独立基础底面积计算（土木）",
        "h1": "独立基础底面积计算",
        "h2": "🏗️ 独立基础底面积计算（土木）",
        "intro": "由柱底轴力与弯矩，按地基承载力计算独立基础底面尺寸并验算基底压力。",
        "desc": "独立基础底面积计算 - 根据轴力、弯矩与地基承载力计算基础底面积并验算基底压力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "N", "label": "柱底轴力 N (kN)", "value": "800", "step": "10", "min": "0"},
            {"id": "M", "label": "弯矩 M (kN·m)", "value": "80", "step": "5", "min": "0"},
            {"id": "fa", "label": "地基承载力 f_a (kPa)", "value": "200", "step": "5", "min": "1"},
            {"id": "gamma", "label": "基础及土平均重度 (kN/m³)", "value": "20", "step": "1", "min": "1"},
            {"id": "d", "label": "基础埋深 d (m)", "value": "1.5", "step": "0.1", "min": "0.1"},
            {"id": "B", "label": "基础边长 B (m)", "value": "2.5", "step": "0.1", "min": "0.5"},
        ],
        "calc": r"""
            const N=num('N'), M=num('M'), fa=num('fa'), gamma=num('gamma'), d=num('d'), B=num('B');
            if(N<0||fa<=0||gamma<=0||d<=0||B<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的荷载与地基参数。</p>');return;}
            const A = B*B;
            const pmax = (N + gamma*A*d)/A + M/(B*Math.pow(B,2)/6);
            const pmin = (N + gamma*A*d)/A - M/(B*Math.pow(B,2)/6);
            const pavg = (N + gamma*A*d)/A;
            const ok = (pmax<=1.2*fa) && (pmin>=0);
            const html = dataGrid([
                [A.toFixed(2),'基础底面积 A (m²)'],
                [pavg.toFixed(1),'平均基底压力 p (kPa)'],
                [pmax.toFixed(1),'最大基底压力 p_max (kPa)'],
                [pmin.toFixed(1),'最小基底压力 p_min (kPa)']
            ]) + (ok?'<p style="color:var(--ok,#16a34a);margin-top:10px;">✅ 基底压力满足要求（p_max ≤ 1.2f_a 且 p_min ≥ 0）</p>'
                    :'<p class="tip-error">⚠️ 基底压力不满足，建议增大基础尺寸或提高地基承载力。</p>');
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "基底平均压力 p = (N + γ·A·d) / A",
            "偏心时 p_max/min = p ± M / W，W = B³/6（方形基础）",
            "验算条件：p_max ≤ 1.2f_a 且 p_min ≥ 0",
            "本工具按方形基础估算，矩形基础请另行计算",
        ],
    },
    {
        "slug": "pile-capacity", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "单桩竖向承载力计算（土木）",
        "h1": "单桩竖向承载力计算",
        "h2": "🏗️ 单桩竖向承载力计算（土木）",
        "intro": "按桩侧摩阻力与桩端阻力经验公式估算单桩竖向承载力特征值。",
        "desc": "单桩竖向承载力计算 - 依据桩侧摩阻与桩端阻力经验公式估算单桩竖向承载力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "d", "label": "桩径 d (m)", "value": "0.6", "step": "0.05", "min": "0.1"},
            {"id": "L", "label": "桩长 L (m)", "value": "15", "step": "0.5", "min": "1"},
            {"id": "qs", "label": "平均侧阻 q_s (kPa)", "value": "40", "step": "2", "min": "0"},
            {"id": "qp", "label": "端阻 q_p (kPa)", "value": "2000", "step": "50", "min": "0"},
            {"id": "K", "label": "安全系数 K", "value": "2", "step": "0.1", "min": "1"},
        ],
        "calc": r"""
            const d=num('d'), L=num('L'), qs=num('qs'), qp=num('qp'), K=num('K');
            if(d<=0||L<=0||K<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的桩参数。</p>');return;}
            const Ap = Math.PI*d*d/4;       // m²
            const u = Math.PI*d;            // m
            const Ra = (qp*Ap + u*qs*L)/K;  // kN
            const html = dataGrid([
                [Ap.toFixed(3),'桩端面积 A_p (m²)'],
                [(u*qs*L).toFixed(0),'总侧阻 (kN)'],
                [(qp*Ap).toFixed(0),'端阻 (kN)'],
                [Ra.toFixed(0),'单桩承载力特征值 R_a (kN)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "R_a = (q_pa·A_p + u·Σ q_sia·l_i) / K",
            "A_p = πd²/4 为桩端面积，u = πd 为桩周长",
            "安全系数 K 通常取 2（以标准值求特征值）",
            "侧阻/端阻应按地质报告取值，本工具为经验估算",
        ],
    },
    {
        "slug": "active-earth-rankine", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "朗金主动土压力计算（土木）",
        "h1": "朗金主动土压力计算",
        "h2": "🏗️ 朗金主动土压力计算（土木）",
        "intro": "按朗金土压力理论计算无黏性/黏性填土作用于竖直墙背的主动土压力合力与临界深度。",
        "desc": "朗金主动土压力计算 - 依据朗金土压力理论计算主动土压力合力、临界深度与土压力分布。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "gamma", "label": "土的重度 γ (kN/m³)", "value": "18", "step": "0.5", "min": "1"},
            {"id": "H", "label": "填土高度 H (m)", "value": "5", "step": "0.1", "min": "0.1"},
            {"id": "phi", "label": "内摩擦角 φ (°)", "value": "30", "step": "1", "min": "0", "max": "45"},
            {"id": "c", "label": "黏聚力 c (kPa)", "value": "0", "step": "1", "min": "0"},
        ],
        "calc": r"""
            const g=num('gamma'), H=num('H'), phi=num('phi')*Math.PI/180, c=num('c');
            if(g<=0||H<=0||phi<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的土体参数。</p>');return;}
            const Ka = Math.pow(Math.tan(Math.PI/4 - phi/2),2);
            let z0 = 0;
            if(c>0) z0 = 2*c/Math.sqrt(Ka)/g;
            let Ea;
            if(c>0 && z0>=H){ Ea=0; }
            else { Ea = 0.5*g*H*H*Ka - 2*c*H*Math.sqrt(Ka); if(Ea<0) Ea=0; }
            const pa_bottom = g*H*Ka - 2*c*Math.sqrt(Ka);
            const html = dataGrid([
                [Ka.toFixed(3),'主动土压力系数 K_a'],
                [z0.toFixed(2),'临界深度 z_0 (m)'],
                [Math.max(pa_bottom,0).toFixed(1),'墙底土压力 (kPa)'],
                [Ea.toFixed(1),'主动土压力合力 E_a (kN/m)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "K_a = tan²(45° − φ/2)",
            "黏性土临界深度 z₀ = 2c/(γ√K_a)",
            "主动土压力合力 E_a = ½γH²K_a − 2cH√K_a（当为正时）",
            "本工具按水平填土、无超载的朗金理论估算",
        ],
    },
    {
        "slug": "rebar-weight", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "钢筋理论重量计算（土木）",
        "h1": "钢筋理论重量计算",
        "h2": "🏗️ 钢筋理论重量计算（土木）",
        "intro": "按钢筋直径、长度与根数计算理论重量（采用 ρ=7850 kg/m³ 密度公式）。",
        "desc": "钢筋理论重量计算 - 依据钢筋密度公式按直径、长度与根数计算理论重量。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "d", "label": "钢筋直径 d (mm)", "value": "20", "step": "1", "min": "1"},
            {"id": "L", "label": "单根长度 L (m)", "value": "9", "step": "0.5", "min": "0.1"},
            {"id": "n", "label": "根数 n", "value": "10", "step": "1", "min": "1"},
        ],
        "calc": r"""
            const d=num('d'), L=num('L'), n=num('n');
            if(d<=0||L<=0||n<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的钢筋参数。</p>');return;}
            const perM = 0.00617*d*d;     // kg/m 经验式 = π/4*d²*7.85e-6*1000
            const total = perM*L*n;
            const html = dataGrid([
                [perM.toFixed(3),'每米理论重 (kg/m)'],
                [(perM*L).toFixed(2),'单根重量 (kg)'],
                [total.toFixed(1),'总重 (kg)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "每米重 = 0.00617 × d² (kg/m)，等价于 π/4·d²·ρ（ρ=7850 kg/m³）",
            "总重 = 每米重 × 长度 × 根数",
            "结果为理论重量，实际重量允许偏差见相关标准",
        ],
    },
    {
        "slug": "concrete-volume", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "混凝土构件方量计算（土木）",
        "h1": "混凝土构件方量计算",
        "h2": "🏗️ 混凝土构件方量计算（土木）",
        "intro": "按构件尺寸（长×宽×高或截面积×长度）计算混凝土体积与重量。",
        "desc": "混凝土构件方量计算 - 按尺寸计算混凝土体积并换算为重量，便于工程量估算。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "a", "label": "长度 a (m)", "value": "4", "step": "0.1", "min": "0"},
            {"id": "b", "label": "宽度 b (m)", "value": "0.4", "step": "0.05", "min": "0"},
            {"id": "c", "label": "高度/厚度 c (m)", "value": "0.5", "step": "0.05", "min": "0"},
            {"id": "rho", "label": "混凝土容重 (kg/m³)", "value": "2400", "step": "50", "min": "1000"},
        ],
        "calc": r"""
            const a=num('a'), b=num('b'), c=num('c'), rho=num('rho');
            if(a<0||b<0||c<0||rho<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的构件尺寸。</p>');return;}
            const V=a*b*c;
            const html = dataGrid([
                [V.toFixed(3),'混凝土体积 (m³)'],
                [(V*rho/1000).toFixed(2),'重量 (t)'],
                [(V*rho).toFixed(0),'重量 (kg)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "体积 V = a × b × c",
            "普通混凝土容重约 2400 kg/m³（C20~C40 区间）",
            "结果用于工程量估算，实际以图纸与计量规则为准",
        ],
    },
    {
        "slug": "slope-stability-fos", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "无限边坡稳定安全系数计算（土木）",
        "h1": "无限边坡稳定安全系数计算",
        "h2": "🏗️ 无限边坡稳定安全系数计算（土木）",
        "intro": "按无限边坡（长直斜坡）简化条分法估算安全系数 Fs。",
        "desc": "无限边坡稳定安全系数计算 - 依据无限边坡简化条分法估算边坡稳定安全系数。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "gamma", "label": "土体重度 γ (kN/m³)", "value": "19", "step": "0.5", "min": "1"},
            {"id": "z", "label": "滑动面深度 z (m)", "value": "3", "step": "0.1", "min": "0.1"},
            {"id": "alpha", "label": "坡角 α (°)", "value": "30", "step": "1", "min": "1", "max": "60"},
            {"id": "c", "label": "黏聚力 c (kPa)", "value": "10", "step": "1", "min": "0"},
            {"id": "phi", "label": "内摩擦角 φ (°)", "value": "28", "step": "1", "min": "0", "max": "45"},
        ],
        "calc": r"""
            const g=num('gamma'), z=num('z'), al=num('alpha')*Math.PI/180, c=num('c'), phi=num('phi')*Math.PI/180;
            if(g<=0||z<=0||al<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的边坡参数。</p>');return;}
            const ca=Math.cos(al), sa=Math.sin(al);
            const numF = c + g*z*ca*ca*Math.tan(phi);
            const denF = g*z*sa*ca;
            const Fs = denF>0 ? numF/denF : 999;
            const ok = Fs>=1.3;
            const html = dataGrid([
                [Fs.toFixed(2),'安全系数 F_s'],
                [(Fs*denF).toFixed(1),'抗滑力 (kN/m²)'],
                [denF.toFixed(1),'滑动力 (kN/m²)']
            ]) + (ok?'<p style="color:var(--ok,#16a34a);margin-top:10px;">✅ F_s ≥ 1.3，边坡稳定满足一般要求</p>'
                    :'<p class="tip-error">⚠️ F_s < 1.3，边坡欠稳定，需放缓坡度或加固。</p>');
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "无限边坡：F_s = (c + γz·cos²α·tanφ) / (γz·sinα·cosα)",
            "一般工程要求 F_s ≥ 1.3（永久边坡）",
            "适用于均质、长直斜坡的初步估算",
        ],
    },
    # ===================== engineering（工程） =====================
    {
        "slug": "axial-stress", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "轴向拉压应力与应变计算（工程）",
        "h1": "轴向拉压应力与应变计算",
        "h2": "🏗️ 轴向拉压应力与应变计算（工程）",
        "intro": "按轴向荷载与截面积计算正应力、线应变与轴向变形。",
        "desc": "轴向拉压应力与应变计算 - 依据胡克定律计算轴向荷载下的应力、应变与变形。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "F", "label": "轴向力 F (kN)", "value": "50", "step": "1", "min": "0"},
            {"id": "A", "label": "截面积 A (mm²)", "value": "500", "step": "10", "min": "1"},
            {"id": "E", "label": "弹性模量 E (GPa)", "value": "200", "step": "5", "min": "1"},
            {"id": "L", "label": "原长 L (m)", "value": "2", "step": "0.1", "min": "0.01"},
        ],
        "calc": r"""
            const F=num('F')*1000, A=num('A'), E=num('E')*1e9, L=num('L');
            if(A<=0||E<=0||L<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的材料与几何参数。</p>');return;}
            const sigma=F/A;            // N/mm² = MPa (F in N, A in mm²)
            const eps=sigma*1e6/E;      // MPa -> Pa, 除以 E(Pa) 得应变
            const dL=eps*L*1000;        // mm
            const html=dataGrid([
                [sigma.toFixed(2),'正应力 σ (MPa)'],
                [eps.toExponential(3),'线应变 ε'],
                [dL.toFixed(3),'轴向变形 ΔL (mm)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "应力 σ = F / A",
            "应变 ε = σ / E（胡克定律）",
            "变形 ΔL = ε · L",
        ],
    },
    {
        "slug": "shaft-torsion", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "圆轴扭转剪应力计算（工程）",
        "h1": "圆轴扭转剪应力计算",
        "h2": "🏗️ 圆轴扭转剪应力计算（工程）",
        "intro": "计算受扭圆轴的最大剪应力与单位扭转角。",
        "desc": "圆轴扭转剪应力计算 - 依据材料力学扭转理论计算圆轴最大剪应力与扭转角。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "T", "label": "扭矩 T (kN·m)", "value": "2", "step": "0.1", "min": "0"},
            {"id": "d", "label": "轴径 d (mm)", "value": "50", "step": "1", "min": "1"},
            {"id": "G", "label": "剪切模量 G (GPa)", "value": "80", "step": "2", "min": "1"},
            {"id": "L", "label": "轴长 L (m)", "value": "1", "step": "0.1", "min": "0.01"},
        ],
        "calc": r"""
            const T=num('T')*1000, d=num('d')/1000, G=num('G')*1e9, L=num('L');
            if(d<=0||G<=0||L<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的轴参数。</p>');return;}
            const J=Math.PI*Math.pow(d,4)/32;
            const tau=T*d/2/J/1e6;     // Pa -> MPa
            const theta=T*L/(G*J);     // rad
            const html=dataGrid([
                [(J*1e12).toFixed(3),'极惯性矩 J (mm⁴)'],
                [tau.toFixed(2),'最大剪应力 τ_max (MPa)'],
                [(theta*180/Math.PI).toFixed(3),'扭转角 θ (°)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "极惯性矩 J = πd⁴/32",
            "最大剪应力 τ_max = T·r / J（r = d/2）",
            "扭转角 θ = T·L / (G·J)",
        ],
    },
    {
        "slug": "section-inertia", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "截面惯性矩计算（工程）",
        "h1": "截面惯性矩计算",
        "h2": "🏗️ 截面惯性矩计算（工程）",
        "intro": "计算矩形或圆形截面对中性轴的惯性矩 I 与截面模量 W。",
        "desc": "截面惯性矩计算 - 计算矩形或圆形截面的惯性矩与截面模量。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "shape", "label": "形状(1=矩形,2=圆)", "value": "1", "step": "1", "min": "1", "max": "2"},
            {"id": "b", "label": "矩形宽 b (mm)", "value": "200", "step": "5", "min": "1"},
            {"id": "h", "label": "矩形高 h / 圆径 D (mm)", "value": "400", "step": "5", "min": "1"},
        ],
        "calc": r"""
            const shape=num('shape'), b=num('b'), h=num('h');
            if(b<=0||h<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的截面尺寸。</p>');return;}
            let I, W, desc;
            if(shape===1){ I=b*Math.pow(h,3)/12; W=I/(h/2); desc='矩形 I = bh³/12'; }
            else { I=Math.PI*Math.pow(h,4)/64; W=I/(h/2); desc='圆 I = πD⁴/64'; }
            const html=dataGrid([
                [(I).toFixed(0),'惯性矩 I (mm⁴)'],
                [(W).toFixed(0),'截面模量 W (mm³)'],
            ]) + '<p style="margin-top:10px;font-size:13px;color:var(--text-muted)">'+desc+'</p>';
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "矩形：I = bh³/12，W = I / (h/2)",
            "圆形：I = πD⁴/64，W = I / (D/2)",
            "惯性矩是抗弯刚度 EI 的核心参数",
        ],
    },
    {
        "slug": "thermal-expansion", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "线膨胀量计算（工程）",
        "h1": "线膨胀量计算",
        "h2": "🏗️ 线膨胀量计算（工程）",
        "intro": "按线膨胀系数、原长与温差计算构件的伸长量。",
        "desc": "线膨胀量计算 - 依据线膨胀公式计算温度变化时构件的伸长或缩短量。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "alpha", "label": "线膨胀系数 α (×10⁻⁶/°C)", "value": "12", "step": "0.5", "min": "0"},
            {"id": "L0", "label": "原长 L₀ (m)", "value": "10", "step": "0.5", "min": "0.01"},
            {"id": "dT", "label": "温差 ΔT (°C)", "value": "40", "step": "1", "min": "-200", "max": "1000"},
        ],
        "calc": r"""
            const a=num('alpha')*1e-6, L0=num('L0'), dT=num('dT');
            if(L0<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的原长。</p>');return;}
            const dL=a*L0*dT*1000;   // mm
            const html=dataGrid([
                [dL.toFixed(3),'膨胀量 ΔL (mm)'],
                [(dL/1000).toFixed(4),'膨胀量 ΔL (m)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "ΔL = α · L₀ · ΔT",
            "钢材 α ≈ 12×10⁻⁶/°C，混凝土 ≈ 10×10⁻⁶/°C，铝 ≈ 23×10⁻⁶/°C",
            "升温为正（伸长），降温为负（缩短）",
        ],
    },
    {
        "slug": "cantilever-deflection", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "悬臂梁端部集中荷载挠度（工程）",
        "h1": "悬臂梁端部集中荷载挠度",
        "h2": "🏗️ 悬臂梁端部集中荷载挠度（工程）",
        "intro": "计算自由端受集中力的悬臂梁端部挠度与自由端转角。",
        "desc": "悬臂梁端部集中荷载挠度 - 依据材料力学公式计算悬臂梁端部挠度与转角。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "P", "label": "端部荷载 P (kN)", "value": "5", "step": "0.5", "min": "0"},
            {"id": "L", "label": "梁长 L (m)", "value": "3", "step": "0.1", "min": "0.1"},
            {"id": "E", "label": "弹性模量 E (GPa)", "value": "30", "step": "1", "min": "1"},
            {"id": "I", "label": "惯性矩 I (cm⁴)", "value": "5000", "step": "100", "min": "1"},
        ],
        "calc": r"""
            const P=num('P')*1000, L=num('L'), E=num('E')*1e9, I=num('I')*1e-8;
            if(L<=0||E<=0||I<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的梁参数。</p>');return;}
            const delta=P*Math.pow(L,3)/(3*E*I)*1000;  // m->mm
            const theta=P*L*L/(2*E*I)*180/Math.PI;     // rad->deg
            const html=dataGrid([
                [delta.toFixed(2),'端部挠度 δ (mm)'],
                [theta.toFixed(3),'自由端转角 θ (°)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "端部挠度 δ = P·L³ / (3EI)",
            "自由端转角 θ = P·L² / (2EI)",
            "单位需统一为 N、m",
        ],
    },
    {
        "slug": "bolt-preload", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "螺栓预紧力计算（工程）",
        "h1": "螺栓预紧力计算",
        "h2": "🏗️ 螺栓预紧力计算（工程）",
        "intro": "按拧紧扭矩与扭矩系数估算螺栓轴向预紧力。",
        "desc": "螺栓预紧力计算 - 依据扭矩-预紧力关系估算螺栓轴向预紧力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "T", "label": "拧紧扭矩 T (N·m)", "value": "100", "step": "5", "min": "0"},
            {"id": "d", "label": "螺纹公称直径 d (mm)", "value": "12", "step": "1", "min": "1"},
            {"id": "K", "label": "扭矩系数 K", "value": "0.2", "step": "0.01", "min": "0.05", "max": "0.4"},
        ],
        "calc": r"""
            const T=num('T'), d=num('d')/1000, K=num('K');
            if(d<=0||K<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效的螺栓参数。</p>');return;}
            const F=T/(K*d);   // N
            const html=dataGrid([
                [(F/1000).toFixed(2),'预紧力 F (kN)'],
                [(F).toFixed(0),'预紧力 F (N)']
            ]);
            ToolBox.setResult('result', html);
        """,
        "notes": [
            "F = T / (K · d)，d 取公称直径（m）",
            "扭矩系数 K 通常 0.1~0.25（有润滑取小值）",
            "实际预紧力受摩擦影响，建议配合拉伸法校核",
        ],
    },
    # ===================== civil v2（补齐至 22） =====================
    {
        "slug": "one-way-slab", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "单向板配筋计算（土木）",
        "h1": "单向板配筋计算",
        "h2": "🏗️ 单向板配筋计算（土木）",
        "intro": "按单位宽度单向板，由弯矩计算受拉钢筋面积。",
        "desc": "单向板配筋计算 - 依据混凝土结构原理按单位宽板带计算受拉钢筋面积。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "M", "label": "每延米弯矩 M (kN·m/m)", "value": "8", "step": "0.5", "min": "0"},
            {"id": "h", "label": "板厚 h (mm)", "value": "120", "step": "5", "min": "1"},
            {"id": "fc", "label": "混凝土强度 f_c (MPa)", "value": "14.3", "step": "0.1", "min": "1"},
            {"id": "fy", "label": "钢筋强度 f_y (MPa)", "value": "360", "step": "5", "min": "1"},
            {"id": "as", "label": "保护层 a_s (mm)", "value": "20", "step": "2", "min": "10"},
        ],
        "calc": r"""
            const M=num('M')*1e6, b=1000, h=num('h'), fc=num('fc'), fy=num('fy'), as_=num('as');
            const a1=1.0, h0=h-as_;
            if(M<=0||h0<=0||fc<=0||fy<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const aS=M/(a1*fc*b*h0*h0);
            if(aS>0.44){ToolBox.setResult('result','<p class="tip-error">α_s 超限，需增大板厚。</p>');return;}
            const xi=1-Math.sqrt(1-2*aS);
            const As=xi*a1*fc*b*h0/fy;
            ToolBox.setResult('result', dataGrid([
                [aS.toFixed(4),'α_s'],
                [xi.toFixed(4),'ξ'],
                [As.toFixed(0),'每米配筋 A_s (mm²/m)']
            ]));
        """,
        "notes": [
            "α_s = M/(α₁·f_c·b·h₀²)，b 取 1000mm（单位宽板带）",
            "ξ = 1−√(1−2α_s)，单筋适筋上限 ξ_b ≈ 0.44",
            "A_s = ξ·α₁·f_c·b·h₀ / f_y",
        ],
    },
    {
        "slug": "two-way-slab", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "双向板弯矩估算（土木）",
        "h1": "双向板弯矩估算",
        "h2": "🏗️ 双向板弯矩估算（土木）",
        "intro": "按弹性理论经验系数法估算双向板短跨与长跨方向弯矩。",
        "desc": "双向板弯矩估算 - 依据经验系数法估算双向板两向弯矩。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "q", "label": "均布荷载 q (kN/m²)", "value": "10", "step": "0.5", "min": "0"},
            {"id": "lx", "label": "短跨 l_x (m)", "value": "4", "step": "0.1", "min": "0.5"},
            {"id": "ly", "label": "长跨 l_y (m)", "value": "5", "step": "0.1", "min": "0.5"},
        ],
        "calc": r"""
            const q=num('q'), lx=num('lx'), ly=num('ly');
            if(q<=0||lx<=0||ly<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const ax = lx<=ly ? 0.10 : 0.08;
            const ay = 0.06;
            const Mx=ax*q*lx*lx, My=ay*q*ly*ly;
            ToolBox.setResult('result', dataGrid([
                [Mx.toFixed(2),'短跨方向弯矩 M_x (kN·m/m)'],
                [My.toFixed(2),'长跨方向弯矩 M_y (kN·m/m)'],
                [(Mx/My).toFixed(2),'M_x / M_y 比值']
            ]));
        """,
        "notes": [
            "采用弹性理论经验系数法（简化）",
            "短跨系数 αx≈0.10，长跨系数 αy≈0.06",
            "M = α·q·l²，实际设计应查双向板系数表",
        ],
    },
    {
        "slug": "masonry-bearing", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "砌体墙抗压承载力计算（土木）",
        "h1": "砌体墙抗压承载力计算",
        "h2": "🏗️ 砌体墙抗压承载力计算（土木）",
        "intro": "按砌体抗压强度与截面面积估算轴心受压承载力（含高厚比稳定系数）。",
        "desc": "砌体墙抗压承载力计算 - 依据砌体结构原理估算轴心受压承载力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "f", "label": "砌体抗压强度 f (MPa)", "value": "2.5", "step": "0.1", "min": "0.5"},
            {"id": "b", "label": "墙厚 b (mm)", "value": "240", "step": "10", "min": "50"},
            {"id": "L", "label": "墙长 L (mm)", "value": "3000", "step": "50", "min": "100"},
            {"id": "phi", "label": "稳定系数 φ", "value": "1.0", "step": "0.05", "min": "0.1", "max": "1"},
        ],
        "calc": r"""
            const f=num('f'), b=num('b'), L=num('L'), phi=num('phi');
            if(f<=0||b<=0||L<=0||phi<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const A=b*L;            // mm²
            const N=phi*f*A/1000;   // kN (f MPa=N/mm²)
            ToolBox.setResult('result', dataGrid([
                [(A/1e6).toFixed(3),'截面面积 A (m²)'],
                [N.toFixed(0),'承载力 N (kN)'],
                [(f*A/1000).toFixed(0),'材料抗力 (kN, φ=1)']
            ]));
        """,
        "notes": [
            "N = φ·f·A（f 单位 N/mm²，A 单位 mm² → N）",
            "稳定系数 φ 由高厚比查表确定",
            "开洞墙应按净面积计算",
        ],
    },
    {
        "slug": "concrete-wb-ratio", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "混凝土水胶比计算（土木）",
        "h1": "混凝土水胶比计算",
        "h2": "🏗️ 混凝土水胶比计算（土木）",
        "intro": "按保罗米公式由配制强度与胶凝材料强度计算水胶比 W/B。",
        "desc": "混凝土水胶比计算 - 依据保罗米公式由配制强度计算水胶比。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "fcu", "label": "配制强度 f_cu,0 (MPa)", "value": "38.2", "step": "0.1", "min": "5"},
            {"id": "fb", "label": "胶凝材料 28d 强度 f_b (MPa)", "value": "45", "step": "1", "min": "10"},
            {"id": "aa", "label": "系数 α_a", "value": "0.53", "step": "0.01", "min": "0"},
            {"id": "ab", "label": "系数 α_b", "value": "0.20", "step": "0.01", "min": "0"},
        ],
        "calc": r"""
            const fcu=num('fcu'), fb=num('fb'), aa=num('aa'), ab=num('ab');
            if(fcu<=0||fb<=0||aa<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const wb = aa*fb/(fcu + aa*ab*fb);
            ToolBox.setResult('result', dataGrid([
                [wb.toFixed(3),'水胶比 W/B'],
                [(1/wb).toFixed(2),'胶水比 B/W']
            ]));
        """,
        "notes": [
            "保罗米公式：W/B = α_a·f_b / (f_cu,0 + α_a·α_b·f_b)",
            "普通硅酸盐水泥 α_a≈0.53，α_b≈0.20",
            "结果为理论水胶比，还需满足耐久性最大水胶比限值",
        ],
    },
    {
        "slug": "rebar-anchorage", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "钢筋锚固长度计算（土木）",
        "h1": "钢筋锚固长度计算",
        "h2": "🏗️ 钢筋锚固长度计算（土木）",
        "intro": "按基本锚固长度公式由钢筋与混凝土强度计算锚固长度。",
        "desc": "钢筋锚固长度计算 - 依据混凝土结构设计原理计算受拉钢筋锚固长度。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "fy", "label": "钢筋强度 f_y (MPa)", "value": "360", "step": "5", "min": "1"},
            {"id": "ft", "label": "混凝土抗拉强度 f_t (MPa)", "value": "1.43", "step": "0.05", "min": "0.1"},
            {"id": "d", "label": "钢筋直径 d (mm)", "value": "20", "step": "1", "min": "1"},
            {"id": "za", "label": "锚固长度修正系数 ζ_a", "value": "1.0", "step": "0.05", "min": "0.5", "max": "2"},
        ],
        "calc": r"""
            const fy=num('fy'), ft=num('ft'), d=num('d'), za=num('za');
            if(fy<=0||ft<=0||d<=0||za<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const lab = 0.14*za*(fy/ft)*d; // mm (α=0.14 带肋钢筋锚固外形系数)
            ToolBox.setResult('result', dataGrid([
                [lab.toFixed(0),'基本锚固长度 l_ab (mm)'],
                [(lab/1000).toFixed(2),'l_ab (m)']
            ]));
        """,
        "notes": [
            "l_ab = α·ζ_a·(f_y/f_t)·d，α=0.14（带肋钢筋外形系数）",
            "d>25mm 时 ζ_a 取 1.1，环氧涂层钢筋取 1.25 等",
            "受拉锚固长度 l_a = ζ·l_ab，按锚固区保护层等修正",
        ],
    },
    {
        "slug": "cft-capacity", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "钢管混凝土轴压承载力估算（土木）",
        "h1": "钢管混凝土轴压承载力估算",
        "h2": "🏗️ 钢管混凝土轴压承载力估算（土木）",
        "intro": "按简化叠加模型估算圆钢管混凝土短柱轴心受压承载力。",
        "desc": "钢管混凝土轴压承载力估算 - 依据简化叠加模型估算轴心受压承载力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "D", "label": "钢管外径 D (mm)", "value": "400", "step": "10", "min": "50"},
            {"id": "t", "label": "钢管壁厚 t (mm)", "value": "10", "step": "1", "min": "2"},
            {"id": "fc", "label": "核心混凝土 f_c (MPa)", "value": "40", "step": "1", "min": "1"},
            {"id": "fy", "label": "钢材 f_y (MPa)", "value": "345", "step": "5", "min": "1"},
        ],
        "calc": r"""
            const D=num('D'), t=num('t'), fc=num('fc'), fy=num('fy');
            if(D<=0||t<=0||t>=D/2||fc<=0||fy<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const Ac=Math.PI*(D-2*t)*(D-2*t)/4; // mm²
            const As=Math.PI*(D*D-(D-2*t)*(D-2*t))/4; // mm²
            const N=As*fy + 1.2*Ac*fc; // N (简化，含约束增强系数1.2)
            ToolBox.setResult('result', dataGrid([
                [Ac.toFixed(0),'核心混凝土面积 A_c (mm²)'],
                [As.toFixed(0),'钢管面积 A_s (mm²)'],
                [(N/1000).toFixed(0),'承载力 N (kN)']
            ]));
        """,
        "notes": [
            "A_c、A_s 分别为核心混凝土与钢管截面面积",
            "承载力取 N = A_s·f_y + 1.2·A_c·f_c（含约束增强，保守估）",
            "实际应按规范约束混凝土本构计算",
        ],
    },
    {
        "slug": "excavation-earth", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "基坑主动土压力估算（土木）",
        "h1": "基坑主动土压力估算",
        "h2": "🏗️ 基坑主动土压力估算（土木）",
        "intro": "按朗金理论估算基坑直立边坡的主动土压力合力。",
        "desc": "基坑主动土压力估算 - 依据朗金土压力理论估算基坑主动土压力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "gamma", "label": "土体重度 γ (kN/m³)", "value": "19", "step": "0.5", "min": "1"},
            {"id": "H", "label": "基坑深度 H (m)", "value": "8", "step": "0.5", "min": "0.5"},
            {"id": "phi", "label": "内摩擦角 φ (°)", "value": "30", "step": "1", "min": "0", "max": "45"},
            {"id": "q", "label": "地面超载 q (kPa)", "value": "10", "step": "1", "min": "0"},
        ],
        "calc": r"""
            const g=num('gamma'), H=num('H'), phi=num('phi')*Math.PI/180, q=num('q');
            if(g<=0||H<=0||phi<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const Ka=Math.pow(Math.tan(Math.PI/4-phi/2),2);
            const Ea=0.5*g*H*H*Ka + q*H*Ka;
            ToolBox.setResult('result', dataGrid([
                [Ka.toFixed(3),'主动土压力系数 K_a'],
                [(g*H*Ka+q*Ka).toFixed(1),'墙顶土压力 (kPa)'],
                [Ea.toFixed(1),'主动土压力合力 E_a (kN/m)']
            ]));
        """,
        "notes": [
            "K_a = tan²(45°−φ/2)",
            "含地面超载 q 时 E_a = ½γH²K_a + qHK_a",
            "支护结构内力应按此土压力设计",
        ],
    },
    {
        "slug": "rock-mass-rating", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "围岩分级评分 RMR 计算（土木）",
        "h1": "围岩分级评分 RMR 计算",
        "h2": "🏗️ 围岩分级评分 RMR 计算（土木）",
        "intro": "按 Bieniawski 岩体质量评分法（RMR）计算围岩分级总分。",
        "desc": "围岩分级评分 RMR 计算 - 依据 RMR 体系计算岩体质量评分与级别。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "s1", "label": "岩石强度评分 (0-15)", "value": "12", "step": "1", "min": "0", "max": "15"},
            {"id": "s2", "label": "RQD 评分 (0-20)", "value": "13", "step": "1", "min": "0", "max": "20"},
            {"id": "s3", "label": "节理间距评分 (0-20)", "value": "10", "step": "1", "min": "0", "max": "20"},
            {"id": "s4", "label": "节理条件评分 (0-25)", "value": "20", "step": "1", "min": "0", "max": "25"},
            {"id": "s5", "label": "地下水评分 (0-15)", "value": "10", "step": "1", "min": "0", "max": "15"},
        ],
        "calc": r"""
            const s1=num('s1'),s2=num('s2'),s3=num('s3'),s4=num('s4'),s5=num('s5');
            const RMR=s1+s2+s3+s4+s5;
            let grade = RMR>=81?'I 级（极好）':RMR>=61?'II 级（好）':RMR>=41?'III 级（中等）':RMR>=21?'IV 级（差）':'V 级（极差）';
            ToolBox.setResult('result', dataGrid([
                [RMR.toFixed(0),'RMR 总分'],
                [grade,'围岩级别']
            ]));
        """,
        "notes": [
            "RMR = 5 项评分之和（满分 100）",
            "评分项：岩石强度(15)+RQD(20)+节理间距(20)+节理条件(25)+地下水(15)",
            "RMR≥81 为 I 级，逐级递减",
        ],
    },
    {
        "slug": "wind-load", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "风荷载标准值计算（土木）",
        "h1": "风荷载标准值计算",
        "h2": "🏗️ 风荷载标准值计算（土木）",
        "intro": "按荷载规范计算垂直于建筑物表面的风荷载标准值。",
        "desc": "风荷载标准值计算 - 依据荷载规范计算风荷载标准值。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "w0", "label": "基本风压 ω0 (kN/m²)", "value": "0.5", "step": "0.05", "min": "0.1"},
            {"id": "mz", "label": "风压高度系数 μ_z", "value": "1.0", "step": "0.05", "min": "0.3"},
            {"id": "ms", "label": "体型系数 μ_s", "value": "1.3", "step": "0.1", "min": "0.5"},
            {"id": "bz", "label": "阵风系数 β_z", "value": "1.5", "step": "0.05", "min": "1"},
        ],
        "calc": r"""
            const w0=num('w0'), mz=num('mz'), ms=num('ms'), bz=num('bz');
            if(w0<=0||mz<=0||ms<=0||bz<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const wk=bz*mz*ms*w0;
            ToolBox.setResult('result', dataGrid([
                [wk.toFixed(3),'风荷载标准值 w_k (kN/m²)']
            ]));
        """,
        "notes": [
            "w_k = β_z·μ_z·μ_s·ω_0",
            "ω_0 按重现期与地区查基本风压",
            "μ_z、μ_s 按规范表格取值",
        ],
    },
    {
        "slug": "load-combination", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "荷载基本组合计算（土木）",
        "h1": "荷载基本组合计算",
        "h2": "🏗️ 荷载基本组合计算（土木）",
        "intro": "按承载能力极限状态基本组合计算组合效应设计值。",
        "desc": "荷载基本组合计算 - 依据荷载规范计算基本组合效应设计值。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "Sg", "label": "永久荷载效应 S_Gk", "value": "50", "step": "1", "min": "0"},
            {"id": "Sq", "label": "可变荷载效应 S_Qk", "value": "30", "step": "1", "min": "0"},
            {"id": "gG", "label": "永久荷载分项系数 γ_G", "value": "1.3", "step": "0.05", "min": "1"},
            {"id": "gQ", "label": "可变荷载分项系数 γ_Q", "value": "1.5", "step": "0.05", "min": "1"},
        ],
        "calc": r"""
            const Sg=num('Sg'), Sq=num('Sq'), gG=num('gG'), gQ=num('gQ');
            const S=gG*Sg+gQ*Sq;
            ToolBox.setResult('result', dataGrid([
                [(gG*Sg).toFixed(1),'γ_G·S_Gk'],
                [(gQ*Sq).toFixed(1),'γ_Q·S_Qk'],
                [S.toFixed(1),'组合效应 S (kN·m)']
            ]));
        """,
        "notes": [
            "S = γ_G·S_Gk + γ_Q·S_Qk（基本组合）",
            "γ_G 通常 1.2~1.3，γ_Q 通常 1.4~1.5",
            "有多个可变荷载时取效应最大的为主导",
        ],
    },
    {
        "slug": "carbonation-depth", "industry": "civil", "cat": "engineer",
        "icon": "🏗️", "bg": "#fef3c7",
        "title": "混凝土碳化深度估算（土木）",
        "h1": "混凝土碳化深度估算",
        "h2": "🏗️ 混凝土碳化深度估算（土木）",
        "intro": "按平方扩散规律估算给定使用年限下的混凝土碳化深度。",
        "desc": "混凝土碳化深度估算 - 依据碳化扩散模型估算碳化深度。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "K", "label": "碳化系数 K (mm/√a)", "value": "2.0", "step": "0.1", "min": "0.5"},
            {"id": "t", "label": "使用年限 t (年)", "value": "30", "step": "1", "min": "1"},
        ],
        "calc": r"""
            const K=num('K'), t=num('t');
            if(K<=0||t<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const x=2.56*K*Math.sqrt(t);
            ToolBox.setResult('result', dataGrid([
                [x.toFixed(1),'碳化深度 x (mm)'],
                [(x/10).toFixed(2),'碳化深度 (cm)']
            ]));
        """,
        "notes": [
            "常用模型：x = 2.56·K·√t（K 为碳化速度系数）",
            "K 受混凝土强度、养护、环境湿度影响",
            "碳化达到保护层厚度时钢筋开始锈蚀",
        ],
    },
    # ===================== engineering v2（补齐至 15） =====================
    {
        "slug": "bending-stress", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "梁受弯最大弯曲应力计算（工程）",
        "h1": "梁受弯最大弯曲应力计算",
        "h2": "🏗️ 梁受弯最大弯曲应力计算（工程）",
        "intro": "由弯矩与截面模量计算梁的最大弯曲正应力。",
        "desc": "梁受弯最大弯曲应力计算 - 依据材料力学公式计算梁的最大弯曲正应力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "M", "label": "弯矩 M (kN·m)", "value": "20", "step": "0.5", "min": "0"},
            {"id": "b", "label": "截面宽 b (mm)", "value": "150", "step": "5", "min": "1"},
            {"id": "h", "label": "截面高 h (mm)", "value": "300", "step": "5", "min": "1"},
        ],
        "calc": r"""
            const M=num('M')*1e6, b=num('b'), h=num('h');
            if(M<=0||b<=0||h<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const W=b*h*h/6; // mm³
            const sigma=M/W; // MPa
            ToolBox.setResult('result', dataGrid([
                [W.toFixed(0),'截面模量 W (mm³)'],
                [sigma.toFixed(2),'最大弯曲应力 σ (MPa)']
            ]));
        """,
        "notes": [
            "σ_max = M / W",
            "W = bh²/6（矩形截面）",
            "拉应力在受拉边，压应力在受压边",
        ],
    },
    {
        "slug": "poisson-strain", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "泊松比横向应变计算（工程）",
        "h1": "泊松比横向应变计算",
        "h2": "🏗️ 泊松比横向应变计算（工程）",
        "intro": "由轴向应变与泊松比计算横向应变。",
        "desc": "泊松比横向应变计算 - 依据泊松效应计算横向应变。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "ex", "label": "轴向应变 ε_x", "value": "0.001", "step": "0.0001", "min": "-1"},
            {"id": "nu", "label": "泊松比 ν", "value": "0.3", "step": "0.01", "min": "-1", "max": "0.5"},
        ],
        "calc": r"""
            const ex=num('ex'), nu=num('nu');
            const ey=-nu*ex;
            ToolBox.setResult('result', dataGrid([
                [ex.toExponential(3),'轴向应变 ε_x'],
                [ey.toExponential(3),'横向应变 ε_y'],
                [nu.toFixed(3),'泊松比 ν']
            ]));
        """,
        "notes": [
            "ε_y = −ν·ε_x（横向与轴向反向）",
            "钢材 ν≈0.3，混凝土 ν≈0.2，橡胶 ν≈0.5",
            "泊松比是材料固有弹性常数",
        ],
    },
    {
        "slug": "pressure-vessel", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "薄壁圆筒容器壁厚计算（工程）",
        "h1": "薄壁圆筒容器壁厚计算",
        "h2": "🏗️ 薄壁圆筒容器壁厚计算（工程）",
        "intro": "按薄壁圆筒环向应力公式由内压计算所需壁厚。",
        "desc": "薄壁圆筒容器壁厚计算 - 依据薄壁应力公式计算容器壁厚。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "P", "label": "设计内压 P (MPa)", "value": "1.6", "step": "0.1", "min": "0"},
            {"id": "D", "label": "容器内径 D (mm)", "value": "1000", "step": "10", "min": "10"},
            {"id": "sigma", "label": "许用应力 [σ] (MPa)", "value": "130", "step": "5", "min": "1"},
            {"id": "phi", "label": "焊缝系数 φ", "value": "0.85", "step": "0.05", "min": "0.1", "max": "1"},
        ],
        "calc": r"""
            const P=num('P'), D=num('D'), sig=num('sigma'), phi=num('phi');
            if(P<=0||D<=0||sig<=0||phi<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const t=P*D/(2*sig*phi); // mm (薄壁环向应力公式)
            ToolBox.setResult('result', dataGrid([
                [t.toFixed(2),'所需壁厚 t (mm)'],
                [(t+2).toFixed(2),'计入腐蚀裕量后 (~+2mm)']
            ]));
        """,
        "notes": [
            "t = P·D / (2[σ]·φ)（环向应力控制）",
            "适用于 D/t ≥ 20 的薄壁圆筒",
            "实际设计还应校核轴向应力与稳定",
        ],
    },
    {
        "slug": "weld-strength", "industry": "engineering", "cat": "calculator",
        "icon": "🏗️", "bg": "#475569",
        "title": "角焊缝强度计算（工程）",
        "h1": "角焊缝强度计算",
        "h2": "🏗️ 角焊缝强度计算（工程）",
        "intro": "由焊缝尺寸与作用力计算角焊缝的平均剪应力。",
        "desc": "角焊缝强度计算 - 依据角焊缝有效截面计算剪应力。免费在线工具，纯前端本地处理，数据不上传。",
        "inputs": [
            {"id": "F", "label": "作用力 F (kN)", "value": "50", "step": "1", "min": "0"},
            {"id": "hf", "label": "焊脚尺寸 h_f (mm)", "value": "6", "step": "0.5", "min": "1"},
            {"id": "lw", "label": "焊缝计算长度 l_w (mm)", "value": "200", "step": "10", "min": "10"},
        ],
        "calc": r"""
            const F=num('F')*1000, hf=num('hf'), lw=num('lw');
            if(F<=0||hf<=0||lw<=0){ToolBox.setResult('result','<p class="tip-error">请输入有效参数。</p>');return;}
            const A=0.7*hf*lw; // mm² 有效截面
            const tau=F/A; // MPa
            ToolBox.setResult('result', dataGrid([
                [A.toFixed(0),'焊缝有效截面 A_e (mm²)'],
                [tau.toFixed(2),'焊缝剪应力 τ (MPa)']
            ]));
        """,
        "notes": [
            "A_e = 0.7·h_f·l_w（角焊缝有效截面）",
            "τ = F / A_e，应 ≤ 角焊缝强度设计值",
            "l_w 应扣除起灭弧缺陷（通常减 2h_f）",
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
<script>window.__tbq=window.__tbq||[];window.ToolBox=window.ToolBox||{};['initToolTheme','addToolStyles','showToast','toast','copyText','copyToClipboard','copyFromElement','downloadText','injectPrivacyBadge','toggleFavTool','addToRecentTool','toggleToolTheme','applyTheme'].forEach(function(k){if(typeof window.ToolBox[k]!=='function')window.ToolBox[k]=function(){window.__tbq.push([k,[].slice.call(arguments)]);};});</script><!-- TOOLBOX-API-STUB -->
<script src="../../js/common.js" defer></script>

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首页","item":"https://chenguangwu.github.io/"},{"@type":"ListItem","position":2,"name":"__CATZH__","item":"https://chenguangwu.github.io/tools/__INDUSTRY__/index.html"},{"@type":"ListItem","position":3,"name":"__TITLE__","item":"https://chenguangwu.github.io/tools/__INDUSTRY__/__SLUG__.html"}]}
</script>

<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 5000+免费在线工具">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 5000+免费在线工具">
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
