# -*- coding: utf-8 -*-
"""Batch 43: 化学计算深化 II（14 个公式计算器）。industry=chemistry。"""
from tool_template import main

# 常数
R = 8.314          # 气体常数 J/(mol·K)
F = 96485          # 法拉第常数 C/mol

TOOLS = [
    {
        "slug": "limiting-reagent",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "flask-conical",
        "bg": "from-emerald-500 to-teal-600",
        "title": "限量反应物计算器",
        "h1": "限量反应物（限制试剂）",
        "h2": "根据投料量与化学计量比确定限量反应物与理论产量",
        "intro": "输入两种反应物的质量与摩尔质量，以及反应方程式系数，自动判定哪种是限量反应物。",
        "desc": "限量反应物计算器：输入质量、摩尔质量与化学计量系数，判定限制试剂并给出相对反应程度。",
        "inputs": [
            {"id": "mA", "label": "反应物 A 质量", "value": "10", "step": "0.1", "unit": "g"},
            {"id": "MA", "label": "A 摩尔质量", "value": "36.46", "step": "0.01", "unit": "g/mol"},
            {"id": "a", "label": "A 系数", "value": "1", "step": "1", "unit": ""},
            {"id": "mB", "label": "反应物 B 质量", "value": "8", "step": "0.1", "unit": "g"},
            {"id": "MB", "label": "B 摩尔质量", "value": "40.00", "step": "0.01", "unit": "g/mol"},
            {"id": "b", "label": "B 系数", "value": "2", "step": "1", "unit": ""},
            {"id": "MP", "label": "产物摩尔质量", "value": "58.44", "step": "0.01", "unit": "g/mol"},
            {"id": "c", "label": "产物系数", "value": "1", "step": "1", "unit": ""},
        ],
        "calc": """
            const mA=num('mA'),MA=num('MA'),a=num('a'),mB=num('mB'),MB=num('MB'),b=num('b'),MP=num('MP'),c=num('c');
            const nA=mA/MA, nB=mB/MB;
            const extA=nA/a, extB=nB/b;
            const limiting = extA<=extB ? 'A' : 'B';
            const ext = Math.min(extA, extB);
            const yieldMass = ext*c*MP;
            ToolBox.setResult('result', dataGrid([
                [(limiting==='A'?'A (反应物A)':'B (反应物B)'),'限量反应物'],
                [nA.toFixed(4),'A 物质的量 (mol)'],
                [nB.toFixed(4),'B 物质的量 (mol)'],
                [ext.toFixed(4),'反应程度 ξ (mol)'],
                [yieldMass.toFixed(3),'理论产量 (g)']
            ]));
        """,
        "notes": ["ξ = n_i/ν_i，取较小者对应的物质为限量反应物。", "示例：HCl(36.46) 10g 与 NaOH(40) 8g，A 限量。"],
    },
    {
        "slug": "mole-fraction",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "percent",
        "bg": "from-emerald-500 to-teal-600",
        "title": "摩尔分数计算器",
        "h1": "摩尔分数 x",
        "h2": "由各组分的物质的量求摩尔分数",
        "intro": "输入两种或多种组分的物质的量，自动归一化为摩尔分数。",
        "desc": "摩尔分数计算器：输入各组分物质的量，输出归一化摩尔分数与总和校验。",
        "inputs": [
            {"id": "n1", "label": "组分1 物质的量", "value": "2", "step": "0.1", "unit": "mol"},
            {"id": "n2", "label": "组分2 物质的量", "value": "3", "step": "0.1", "unit": "mol"},
            {"id": "n3", "label": "组分3 物质的量（可0）", "value": "0", "step": "0.1", "unit": "mol"},
        ],
        "calc": """
            const ns=[num('n1'),num('n2'),num('n3')].filter(v=>v>0);
            const tot=ns.reduce((s,v)=>s+v,0);
            const xs=ns.map(v=>(v/tot));
            const grid=xs.map((x,i)=>[(x*100).toFixed(2),'组分'+(i+1)+' 摩尔分数 (%)']);
            grid.push([tot.toFixed(4),'总物质的量 (mol)']);
            ToolBox.setResult('result', dataGrid(grid));
        """,
        "notes": ["x_i = n_i / Σn_i，所有 x_i 之和为 1。", "仅统计正数输入项。"],
    },
    {
        "slug": "mass-percent",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "scale",
        "bg": "from-emerald-500 to-teal-600",
        "title": "质量分数计算器",
        "h1": "质量分数 w",
        "h2": "由溶质与溶液质量求质量分数（浓度）",
        "intro": "输入溶质质量与溶液总质量，求质量分数（百分比浓度）。",
        "desc": "质量分数计算器：输入溶质质量与溶液质量，输出质量分数与百分数。",
        "inputs": [
            {"id": "ms", "label": "溶质质量", "value": "9", "step": "0.1", "unit": "g"},
            {"id": "msol", "label": "溶液质量", "value": "100", "step": "0.1", "unit": "g"},
        ],
        "calc": """
            const ms=num('ms'), msol=num('msol');
            const w=ms/msol;
            ToolBox.setResult('result', dataGrid([
                [w.toFixed(4),'质量分数 w'],
                [(w*100).toFixed(2),'质量分数 (%)'],
                [(msol-ms).toFixed(2),'溶剂质量 (g)']
            ]));
        """,
        "notes": ["w = m_溶质 / m_溶液。", "9 g NaCl 溶于 100 g 溶液 → 9%。"],
    },
    {
        "slug": "empirical-formula",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "atom",
        "bg": "from-emerald-500 to-teal-600",
        "title": "最简式（实验式）计算器",
        "h1": "由质量百分比求最简式",
        "h2": "将元素质量百分比换算为原子最简整数比",
        "intro": "输入最多三种元素的质量百分比与原子量，自动求原子数之比并约简。",
        "desc": "实验式计算器：输入元素质量百分比与原子量，输出原子数最简整数比。",
        "inputs": [
            {"id": "p1", "label": "元素1 质量%", "value": "40.0", "step": "0.1", "unit": "%"},
            {"id": "a1", "label": "元素1 原子量", "value": "12.01", "step": "0.01", "unit": "g/mol"},
            {"id": "p2", "label": "元素2 质量%", "value": "6.7", "step": "0.1", "unit": "%"},
            {"id": "a2", "label": "元素2 原子量", "value": "1.008", "step": "0.01", "unit": "g/mol"},
            {"id": "p3", "label": "元素3 质量%", "value": "53.3", "step": "0.1", "unit": "%"},
            {"id": "a3", "label": "元素3 原子量", "value": "16.00", "step": "0.01", "unit": "g/mol"},
        ],
        "calc": """
            const ps=[num('p1'),num('p2'),num('p3')];
            const as=[num('a1'),num('a2'),num('a3')];
            const moles=ps.map((p,i)=>p/as[i]);
            const min=Math.min(...moles.filter(v=>v>0));
            const ratios=moles.map(m=>(m/min));
            function near(x){return Math.round(x*100)/100;}
            const grid=ratios.map((r,i)=>[near(r).toFixed(2),'元素'+(i+1)+' 原子数比']);
            ToolBox.setResult('result', dataGrid(grid));
        """,
        "notes": ["n_i = w_i% / A_i，再除以最小值得到整数比。", "示例 C40% H6.7% O53.3% → CH₂O。"],
    },
    {
        "slug": "dilution-c1v1",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "droplets",
        "bg": "from-emerald-500 to-teal-600",
        "title": "溶液稀释计算器",
        "h1": "稀释公式 C₁V₁ = C₂V₂",
        "h2": "已知三者求第四者（浓度或体积）",
        "intro": "输入初始浓度与体积、目标浓度，求所需体积；或求目标体积。",
        "desc": "稀释计算器：输入 C1/V1/C2/V2 中任三项，求解缺失项。",
        "inputs": [
            {"id": "c1", "label": "初始浓度 C₁", "value": "1", "step": "0.01", "unit": "mol/L"},
            {"id": "v1", "label": "初始体积 V₁", "value": "100", "step": "1", "unit": "mL"},
            {"id": "c2", "label": "目标浓度 C₂", "value": "0.1", "step": "0.01", "unit": "mol/L"},
            {"id": "v2", "label": "目标体积 V₂（0=求此项）", "value": "0", "step": "1", "unit": "mL"},
        ],
        "calc": """
            const c1=num('c1'),v1=num('v1'),c2=num('c2'),v2=num('v2');
            let out;
            if(v2===0||v2===''){ const V=c1*v1/c2; out=[V.toFixed(2),'所需目标体积 V₂ (mL)']; }
            else { const V=c1*v1/c2; out=[V.toFixed(2),'由 C₁V₁=C₂V₂ 得 V₂ (mL)']; }
            ToolBox.setResult('result', dataGrid([
                out,
                [(c1*v1).toFixed(3),'溶质物质的量 (C·V)']
            ]));
        """,
        "notes": ["C₁V₁ = C₂V₂ 为稀释前后溶质量守恒。", "1 mol/L×100mL 稀释至 0.1 mol/L → 需 1000 mL。"],
    },
    {
        "slug": "ph-from-ka",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "test-tube",
        "bg": "from-emerald-500 to-teal-600",
        "title": "弱酸 pH 计算器",
        "h1": "一元弱酸 pH ≈ ½(pKₐ − log C)",
        "h2": "由酸解离常数与浓度估算 pH",
        "intro": "输入弱酸浓度与 Ka，用近似公式求氢离子浓度与 pH。",
        "desc": "弱酸 pH 计算器：输入浓度与 Ka，输出 [H⁺] 与 pH。",
        "inputs": [
            {"id": "C", "label": "弱酸浓度", "value": "0.1", "step": "0.01", "unit": "mol/L"},
            {"id": "Ka", "label": "酸解离常数 Ka", "value": "1.8e-5", "step": "1e-6", "unit": ""},
        ],
        "calc": """
            const C=num('C'), Ka=num('Ka');
            const h=Math.sqrt(Ka*C);
            const ph=-Math.log10(h);
            ToolBox.setResult('result', dataGrid([
                [h.toExponential(3),'[H⁺] (mol/L)'],
                [ph.toFixed(3),'pH']
            ]));
        """,
        "notes": ["近似 [H⁺]=√(Ka·C)，适用于 C/Ka>400。", "0.1 mol/L 醋酸(Ka=1.8e-5) → pH≈2.87。"],
    },
    {
        "slug": "buffer-ph",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "test-tube",
        "bg": "from-emerald-500 to-teal-600",
        "title": "缓冲溶液 pH 计算器",
        "h1": "Henderson–Hasselbalch 方程",
        "h2": "pH = pKₐ + log([A⁻]/[HA])",
        "intro": "输入 pKa 与共轭碱/酸浓度比，求缓冲溶液 pH。",
        "desc": "缓冲溶液 pH 计算器：输入 pKa、[A⁻]、[HA]，输出 pH。",
        "inputs": [
            {"id": "pKa", "label": "pKₐ", "value": "4.76", "step": "0.01", "unit": ""},
            {"id": "Abase", "label": "共轭碱浓度 [A⁻]", "value": "0.1", "step": "0.01", "unit": "mol/L"},
            {"id": "HA", "label": "弱酸浓度 [HA]", "value": "0.1", "step": "0.01", "unit": "mol/L"},
        ],
        "calc": """
            const pKa=num('pKa'),Ab=num('Abase'),HA=num('HA');
            const ph=pKa+Math.log10(Ab/HA);
            ToolBox.setResult('result', dataGrid([
                [ph.toFixed(3),'pH'],
                [(Ab/HA).toFixed(3),'[A⁻]/[HA] 比']
            ]));
        """,
        "notes": ["pH = pKₐ + log([A⁻]/[HA])。", "醋酸缓冲 pKa=4.76，等浓度 → pH=4.76。"],
    },
    {
        "slug": "poh-to-ph",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "test-tube",
        "bg": "from-emerald-500 to-teal-600",
        "title": "pOH 与 pH 换算器",
        "h1": "pH + pOH = 14（25℃）",
        "h2": "由 [OH⁻] 求 pOH 与 pH",
        "intro": "输入氢氧根浓度，求 pOH 与 pH。",
        "desc": "pOH/pH 换算器：输入 [OH⁻]，输出 pOH 与 pH。",
        "inputs": [
            {"id": "OH", "label": "氢氧根浓度 [OH⁻]", "value": "1e-3", "step": "1e-4", "unit": "mol/L"},
        ],
        "calc": """
            const OH=num('OH');
            const pOH=-Math.log10(OH);
            const ph=14-pOH;
            ToolBox.setResult('result', dataGrid([
                [pOH.toFixed(3),'pOH'],
                [ph.toFixed(3),'pH'],
                [(Math.pow(10,-ph)).toExponential(3),'[H⁺] (mol/L)']
            ]));
        """,
        "notes": ["pOH = -log[OH⁻]，pH = 14 - pOH（25℃）。", "[OH⁻]=1e-3 → pOH=3，pH=11。"],
    },
    {
        "slug": "kp-kc",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "scale",
        "bg": "from-emerald-500 to-teal-600",
        "title": "Kp 与 Kc 换算器",
        "h1": "Kp = Kc(RT)^Δn",
        "h2": "气体反应平衡常数换算",
        "intro": "输入 Kc、温度与气体摩尔数变化 Δn，求 Kp（R=8.314，T 为开尔文）。",
        "desc": "Kp/Kc 换算器：输入 Kc、T、Δn，输出 Kp。",
        "inputs": [
            {"id": "Kc", "label": "浓度平衡常数 Kc", "value": "0.5", "step": "0.01", "unit": ""},
            {"id": "T", "label": "温度 T", "value": "298", "step": "1", "unit": "K"},
            {"id": "dn", "label": "气体摩尔数变化 Δn", "value": "1", "step": "1", "unit": ""},
        ],
        "calc": """
            const Kc=num('Kc'),T=num('T'),dn=num('dn');
            const Kp=Kc*Math.pow(8.314*T, dn);
            ToolBox.setResult('result', dataGrid([
                [Kp.toExponential(3),'压力平衡常数 Kp'],
                [(8.314*T).toFixed(1),'RT (L·kPa/mol·K 等效)']
            ]));
        """,
        "notes": ["Kp = Kc(RT)^Δn，R=8.314。", "Δn=0 时 Kp=Kc。"],
    },
    {
        "slug": "gibbs-free-energy",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "zap",
        "bg": "from-emerald-500 to-teal-600",
        "title": "吉布斯自由能计算器",
        "h1": "ΔG = ΔH − TΔS",
        "h2": "判断反应自发性",
        "intro": "输入焓变、熵变与温度，求吉布斯自由能变并判断反应方向。",
        "desc": "吉布斯自由能计算器：输入 ΔH、ΔS、T，输出 ΔG 与自发性判定。",
        "inputs": [
            {"id": "dH", "label": "焓变 ΔH", "value": "-100", "step": "1", "unit": "kJ/mol"},
            {"id": "dS", "label": "熵变 ΔS", "value": "0.05", "step": "0.001", "unit": "kJ/(mol·K)"},
            {"id": "T", "label": "温度 T", "value": "298", "step": "1", "unit": "K"},
        ],
        "calc": """
            const dH=num('dH'),dS=num('dS'),T=num('T');
            const dG=dH - T*dS;
            const spon = dG<0 ? '自发 (ΔG<0)' : (dG>0 ? '非自发 (ΔG>0)' : '平衡');
            ToolBox.setResult('result', dataGrid([
                [dG.toFixed(3),'ΔG (kJ/mol)'],
                [spon,'反应方向']
            ]));
        """,
        "notes": ["ΔG = ΔH − TΔS，单位需一致（kJ）。", "ΔH=-100, ΔS=0.05, T=298 → ΔG≈-114.9，自发。"],
    },
    {
        "slug": "nernst-equation",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "zap",
        "bg": "from-emerald-500 to-teal-600",
        "title": "能斯特方程计算器",
        "h1": "E = E° − (RT/nF)·ln Q",
        "h2": "非标准状态下的电极电势",
        "intro": "输入标准电势、电子数 n、反应商 Q 与温度，求实际电极电势。",
        "desc": "能斯特方程计算器：输入 E°、n、Q、T，输出电极电势 E。",
        "inputs": [
            {"id": "E0", "label": "标准电极电势 E°", "value": "1.23", "step": "0.01", "unit": "V"},
            {"id": "n", "label": "电子转移数 n", "value": "2", "step": "1", "unit": ""},
            {"id": "Q", "label": "反应商 Q", "value": "1", "step": "0.1", "unit": ""},
            {"id": "T", "label": "温度 T", "value": "298", "step": "1", "unit": "K"},
        ],
        "calc": """
            const E0=num('E0'),n=num('n'),Q=num('Q'),T=num('T');
            const E=E0 - (8.314*T/(n*96485))*Math.log(Q);
            ToolBox.setResult('result', dataGrid([
                [E.toFixed(4),'电极电势 E (V)'],
                [((8.314*T/(n*96485))*Math.log(10)).toFixed(5),'(RT/nF)ln10 (V)']
            ]));
        """,
        "notes": ["E = E° − (RT/nF)lnQ。25℃ 时 2.303RT/F≈0.0592 V。", "Q=1 时 E=E°。"],
    },
    {
        "slug": "arrhenius",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "flame",
        "bg": "from-emerald-500 to-teal-600",
        "title": "阿伦尼乌斯公式计算器",
        "h1": "k = A·e^(−Ea/RT)",
        "h2": "温度对反应速率常数的影响",
        "intro": "输入指前因子 A、活化能 Ea 与温度，求速率常数 k。",
        "desc": "阿伦尼乌斯计算器：输入 A、Ea、T，输出速率常数 k。",
        "inputs": [
            {"id": "A", "label": "指前因子 A", "value": "1e13", "step": "1e12", "unit": "s⁻¹"},
            {"id": "Ea", "label": "活化能 Ea", "value": "50000", "step": "1000", "unit": "J/mol"},
            {"id": "T", "label": "温度 T", "value": "298", "step": "1", "unit": "K"},
        ],
        "calc": """
            const A=num('A'),Ea=num('Ea'),T=num('T');
            const k=A*Math.exp(-Ea/(8.314*T));
            ToolBox.setResult('result', dataGrid([
                [k.toExponential(3),'速率常数 k'],
                [(-Ea/(8.314*T)).toFixed(2),'指数项 (−Ea/RT)']
            ]));
        """,
        "notes": ["k = A·exp(−Ea/RT)。", "Ea=50 kJ/mol、298K、A=1e13 → k≈5.2e-5 s⁻¹。"],
    },
    {
        "slug": "solubility-product",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "droplets",
        "bg": "from-emerald-500 to-teal-600",
        "title": "溶度积 Ksp 计算器",
        "h1": "Ksp = [A]^m · [B]^n",
        "h2": "由离子浓度求溶度积或反之",
        "intro": "输入阴阳离子浓度与化学计量指数，求溶度积 Ksp。",
        "desc": "溶度积计算器：输入 [A]、[B] 与指数 m、n，输出 Ksp。",
        "inputs": [
            {"id": "cA", "label": "阳离子浓度 [A]", "value": "1e-5", "step": "1e-6", "unit": "mol/L"},
            {"id": "mA", "label": "阳离子指数 m", "value": "1", "step": "1", "unit": ""},
            {"id": "cB", "label": "阴离子浓度 [B]", "value": "1e-5", "step": "1e-6", "unit": "mol/L"},
            {"id": "mB", "label": "阴离子指数 n", "value": "1", "step": "1", "unit": ""},
        ],
        "calc": """
            const cA=num('cA'),mA=num('mA'),cB=num('cB'),mB=num('mB');
            const Ksp=Math.pow(cA,mA)*Math.pow(cB,mB);
            ToolBox.setResult('result', dataGrid([
                [Ksp.toExponential(3),'溶度积 Ksp'],
                [Math.sqrt(Ksp).toExponential(3),'若 1:1 则溶解度 s (mol/L)']
            ]));
        """,
        "notes": ["Ksp = [A]^m·[B]^n。", "AgCl: [Ag⁺]=[Cl⁻]=1e-5 → Ksp=1e-10。"],
    },
    {
        "slug": "reaction-quotient",
        "industry": "chemistry",
        "cat": "chemistry",
        "icon": "scale",
        "bg": "from-emerald-500 to-teal-600",
        "title": "反应商 Q 计算器",
        "h1": "Q = Π(浓度^系数)",
        "h2": "判断反应进行的方向",
        "intro": "输入反应物与生成物的浓度及系数，求反应商 Q 并与 K 比较。",
        "desc": "反应商 Q 计算器：输入浓度与系数，输出 Q 及与 K 的对比判定。",
        "inputs": [
            {"id": "rP", "label": "反应物浓度 [R]", "value": "1.0", "step": "0.1", "unit": "mol/L"},
            {"id": "rN", "label": "反应物系数 ν_R", "value": "1", "step": "1", "unit": ""},
            {"id": "pP", "label": "生成物浓度 [P]", "value": "0.5", "step": "0.1", "unit": "mol/L"},
            {"id": "pN", "label": "生成物系数 ν_P", "value": "1", "step": "1", "unit": ""},
            {"id": "K", "label": "平衡常数 K", "value": "2.0", "step": "0.1", "unit": ""},
        ],
        "calc": """
            const rP=num('rP'),rN=num('rN'),pP=num('pP'),pN=num('pN'),K=num('K');
            const Q=Math.pow(pP,pN)/Math.pow(rP,rN);
            let dir = Q<K ? '正向进行 (Q<K)' : (Q>K ? '逆向进行 (Q>K)' : '已达平衡');
            ToolBox.setResult('result', dataGrid([
                [Q.toFixed(4),'反应商 Q'],
                [dir,'反应方向']
            ]));
        """,
        "notes": ["Q = [P]^ν_P / [R]^ν_R（气相用分压）。", "Q<K 正向；Q>K 逆向。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
