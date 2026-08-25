# -*- coding: utf-8 -*-
"""Batch 33: 税务计算深化（14 个通用税费公式计算器）。industry=tax（新干净目录）。"""
from tool_template import main

TOOLS = [
    {
        "slug": "vat-inclusive-to-exclusive", "industry": "tax", "cat": "tax", "icon": "🧾", "bg": "#fef2f2",
        "title": "含税价转不含税价（增值税）", "h1": "含税转不含税计算器",
        "h2": "不含税 = 含税 ÷ (1 + 税率)", "intro": "把含税金额按增值税率拆出不含税销售额与税额。",
        "desc": "增值税含税转不含税：输入含税金额与税率求不含税额与税额。",
        "inputs": [
            {"id": "inc", "label": "含税金额", "value": "113", "step": "1"},
            {"id": "r", "label": "增值税率 (%)", "value": "13", "step": "1"},
        ],
        "calc": """
            const inc = num('inc'), r = num('r') / 100;
            const ex = inc / (1 + r);
            ToolBox.setResult('result', dataGrid([
                [ex.toFixed(2), '不含税金额'],
                [(inc - ex).toFixed(2), '增值税额']
            ]));
        """,
        "notes": ["含税 113、13% → 不含税 100、税额 13。", "税额 = 含税 − 不含税。"],
    },
    {
        "slug": "vat-from-exclusive", "industry": "tax", "cat": "tax", "icon": "📋", "bg": "#fef2f2",
        "title": "不含税价算增值税", "h1": "不含税算增值税计算器",
        "h2": "税额 = 不含税 × 税率", "intro": "由不含税销售额直接计算增值税额与含税价。",
        "desc": "增值税由不含税计算：输入不含税金额与税率求税额与含税价。",
        "inputs": [
            {"id": "ex", "label": "不含税金额", "value": "100", "step": "1"},
            {"id": "r", "label": "增值税率 (%)", "value": "13", "step": "1"},
        ],
        "calc": """
            const ex = num('ex'), r = num('r') / 100;
            const tax = ex * r;
            ToolBox.setResult('result', dataGrid([
                [tax.toFixed(2), '增值税额'],
                [(ex + tax).toFixed(2), '含税金额']
            ]));
        """,
        "notes": ["不含税 100、13% → 税额 13、含税 113。", "含税 = 不含税 ×(1+税率)。"],
    },
    {
        "slug": "progressive-income-tax", "industry": "tax", "cat": "tax", "icon": "🪜", "bg": "#fef2f2",
        "title": "累进所得税", "h1": "累进所得税计算器",
        "h2": "分档累加：各档 (应税−下限) × 档率", "intro": "三档累进税率下的所得税（可自定义档位与税率）。",
        "desc": "累进所得税：输入应税所得与三档下限/税率求总税额。",
        "inputs": [
            {"id": "income", "label": "应税所得", "value": "30000", "step": "1000"},
            {"id": "l1", "label": "第1档上限", "value": "10000", "step": "1000"},
            {"id": "r1", "label": "第1档税率 (%)", "value": "10", "step": "1"},
            {"id": "l2", "label": "第2档上限", "value": "20000", "step": "1000"},
            {"id": "r2", "label": "第2档税率 (%)", "value": "20", "step": "1"},
            {"id": "r3", "label": "第3档税率 (%)", "value": "30", "step": "1"},
        ],
        "calc": """
            const I = num('income'), l1 = num('l1'), r1 = num('r1') / 100, l2 = num('l2'), r2 = num('r2') / 100, r3 = num('r3') / 100;
            let tax = 0;
            if (I > 0) tax += Math.min(I, l1) * r1;
            if (I > l1) tax += Math.min(I - l1, l2 - l1) * r2;
            if (I > l2) tax += (I - l2) * r3;
            ToolBox.setResult('result', dataGrid([
                [tax.toFixed(2), '应纳税额'],
                [(tax / I * 100).toFixed(2), '实际税率 (%)']
            ]));
        """,
        "notes": ["30000、10/20/30 三档 → 1000+2000+3000=6000。", "可改档位模拟个税/企税。"],
    },
    {
        "slug": "corporate-income-tax", "industry": "tax", "cat": "tax", "icon": "🏢", "bg": "#fef2f2",
        "title": "企业所得税", "h1": "企业所得税计算器",
        "h2": "税额 = 应纳税所得额 × 税率", "intro": "由应纳税所得额与适用税率求企业所得税。",
        "desc": "企业所得税：输入应纳税所得额与税率求税额。",
        "inputs": [
            {"id": "profit", "label": "应纳税所得额", "value": "1000000", "step": "10000"},
            {"id": "r", "label": "税率 (%)", "value": "25", "step": "1"},
        ],
        "calc": """
            const p = num('profit'), r = num('r') / 100;
            ToolBox.setResult('result', dataGrid([
                [(p * r).toFixed(2), '企业所得税额'],
                [(p * (1 - r)).toFixed(2), '税后利润']
            ]));
        """,
        "notes": ["100 万、25% → 税额 25 万。", "小型微利企业有优惠税率。"],
    },
    {
        "slug": "capital-gains-tax", "industry": "tax", "cat": "tax", "icon": "📈", "bg": "#fef2f2",
        "title": "资本利得税", "h1": "资本利得税计算器",
        "h2": "税额 = (售价 − 成本) × 税率", "intro": "由资产转让价差与税率计算资本利得税。",
        "desc": "资本利得税：输入售价、成本与税率求税额与净收益。",
        "inputs": [
            {"id": "sell", "label": "售价", "value": "150000", "step": "1000"},
            {"id": "cost", "label": "成本", "value": "100000", "step": "1000"},
            {"id": "r", "label": "税率 (%)", "value": "20", "step": "1"},
        ],
        "calc": """
            const sell = num('sell'), cost = num('cost'), r = num('r') / 100;
            const gain = sell - cost;
            const tax = Math.max(0, gain) * r;
            ToolBox.setResult('result', dataGrid([
                [gain.toFixed(2), '资本利得'],
                [tax.toFixed(2), '资本利得税'],
                [(sell - tax).toFixed(2), '税后到手']
            ]));
        """,
        "notes": ["价差 5 万、20% → 税 1 万。", "亏损通常免税（取 max(0,利得)）。"],
    },
    {
        "slug": "effective-tax-rate", "industry": "tax", "cat": "tax", "icon": "⚖️", "bg": "#fef2f2",
        "title": "实际税率", "h1": "实际税率计算器",
        "h2": "实际税率 = 总税额 ÷ 税前所得", "intro": "综合衡量实际承担的税负水平。",
        "desc": "实际税率：输入总税额与税前所得求实际税率。",
        "inputs": [
            {"id": "tax", "label": "总税额", "value": "250000", "step": "1000"},
            {"id": "pretax", "label": "税前所得", "value": "1000000", "step": "10000"},
        ],
        "calc": """
            const t = num('tax'), p = num('pretax');
            ToolBox.setResult('result', dataGrid([
                [(t / p * 100).toFixed(2), '实际税率 (%)'],
                [(p - t).toFixed(2), '税后所得']
            ]));
        """,
        "notes": ["25 万 / 100 万 = 25%。", "低于名义税率说明有减免。"],
    },
    {
        "slug": "customs-duty", "industry": "tax", "cat": "tax", "icon": "🌐", "bg": "#fef2f2",
        "title": "进口关税", "h1": "进口关税计算器",
        "h2": "关税 = 完税价格 × 关税率", "intro": "由审定完税价格与关税率计算进口关税。",
        "desc": "进口关税：输入完税价格与关税率求关税。",
        "inputs": [
            {"id": "value", "label": "完税价格", "value": "50000", "step": "500"},
            {"id": "r", "label": "关税率 (%)", "value": "10", "step": "0.5"},
        ],
        "calc": """
            const v = num('value'), r = num('r') / 100;
            ToolBox.setResult('result', dataGrid([
                [(v * r).toFixed(2), '进口关税'],
                [(v * (1 + r)).toFixed(2), '含税成本']
            ]));
        """,
        "notes": ["5 万、10% → 关税 5 千。", "完税价格含运费保险费(CIF)。"],
    },
    {
        "slug": "sales-tax-addon", "industry": "tax", "cat": "tax", "icon": "🛒", "bg": "#fef2f2",
        "title": "价外税（消费税）", "h1": "价外税计算器",
        "h2": "含税 = 价格 × (1 + 税率)", "intro": "在价格之外按比例附加的消费税。",
        "desc": "价外税：输入不含税价格与税率求税额与含税价。",
        "inputs": [
            {"id": "price", "label": "不含税价格", "value": "100", "step": "1"},
            {"id": "r", "label": "税率 (%)", "value": "5", "step": "0.5"},
        ],
        "calc": """
            const p = num('price'), r = num('r') / 100;
            ToolBox.setResult('result', dataGrid([
                [(p * r).toFixed(2), '消费税额'],
                [(p * (1 + r)).toFixed(2), '含税价']
            ]));
        """,
        "notes": ["100、5% → 税额 5、含税 105。", "与增值税同为价外税。"],
    },
    {
        "slug": "stamp-duty", "industry": "tax", "cat": "tax", "icon": "✒️", "bg": "#fef2f2",
        "title": "印花税", "h1": "印花税计算器",
        "h2": "税额 = 凭证金额 × 印花税率", "intro": "由应税凭证金额与适用印花税率计算。",
        "desc": "印花税：输入凭证金额与税率求印花税额。",
        "inputs": [
            {"id": "amount", "label": "凭证金额", "value": "1000000", "step": "10000"},
            {"id": "r", "label": "印花税率 (%)", "value": "0.05", "step": "0.01"},
        ],
        "calc": """
            const a = num('amount'), r = num('r') / 100;
            ToolBox.setResult('result', dataGrid([
                [(a * r).toFixed(2), '印花税额']
            ]));
        """,
        "notes": ["100 万、0.05% → 税额 500。", "不同凭证税率不同。"],
    },
    {
        "slug": "property-tax", "industry": "tax", "cat": "tax", "icon": "🏠", "bg": "#fef2f2",
        "title": "房产税", "h1": "房产税计算器",
        "h2": "税额 = 计税余值 × 税率", "intro": "按房产原值扣除比例后的余值计征（或从租计征）。",
        "desc": "房产税：输入计税余值与税率求年税额。",
        "inputs": [
            {"id": "base", "label": "计税余值", "value": "800000", "step": "10000"},
            {"id": "r", "label": "税率 (%)", "value": "1.2", "step": "0.1"},
        ],
        "calc": """
            const b = num('base'), r = num('r') / 100;
            ToolBox.setResult('result', dataGrid([
                [(b * r).toFixed(2), '年房产税额']
            ]));
        """,
        "notes": ["余值 80 万、1.2% → 年税 9600。", "从租计征按租金比例。"],
    },
    {
        "slug": "interest-income-tax", "industry": "tax", "cat": "tax", "icon": "💰", "bg": "#fef2f2",
        "title": "利息所得税", "h1": "利息所得税计算器",
        "h2": "税额 = 利息 × 税率", "intro": "由利息所得与适用税率计算代扣税。",
        "desc": "利息所得税：输入利息金额与税率求税额与到手利息。",
        "inputs": [
            {"id": "interest", "label": "利息金额", "value": "5000", "step": "100"},
            {"id": "r", "label": "税率 (%)", "value": "20", "step": "1"},
        ],
        "calc": """
            const i = num('interest'), r = num('r') / 100;
            ToolBox.setResult('result', dataGrid([
                [(i * r).toFixed(2), '利息所得税'],
                [(i * (1 - r)).toFixed(2), '税后利息']
            ]));
        """,
        "notes": ["利息 5000、20% → 税 1000。", "部分国债利息免税。"],
    },
    {
        "slug": "withholding-tax", "industry": "tax", "cat": "tax", "icon": "✂️", "bg": "#fef2f2",
        "title": "预提所得税", "h1": "预提所得税计算器",
        "h2": "税额 = 支付额 × 预提税率", "intro": "对非居民企业取得的所得源泉扣缴。",
        "desc": "预提所得税：输入支付额与预提税率求扣缴税额。",
        "inputs": [
            {"id": "payment", "label": "支付额", "value": "100000", "step": "1000"},
            {"id": "r", "label": "预提税率 (%)", "value": "10", "step": "0.5"},
        ],
        "calc": """
            const p = num('payment'), r = num('r') / 100;
            ToolBox.setResult('result', dataGrid([
                [(p * r).toFixed(2), '预提税额'],
                [(p * (1 - r)).toFixed(2), '实际支付净额']
            ]));
        """,
        "notes": ["支付 10 万、10% → 预提 1 万。", "税收协定可降率。"],
    },
    {
        "slug": "tax-on-discount", "industry": "tax", "cat": "tax", "icon": "🏷️", "bg": "#fef2f2",
        "title": "折扣后计税", "h1": "折扣后计税计算器",
        "h2": "税额 = 折后价 × 税率", "intro": "按折扣后净额计征税额。",
        "desc": "折扣后计税：输入原价、折扣率与税率求折后价与税额。",
        "inputs": [
            {"id": "price", "label": "原价", "value": "200", "step": "1"},
            {"id": "disc", "label": "折扣率 (%)", "value": "20", "step": "1"},
            {"id": "r", "label": "税率 (%)", "value": "13", "step": "1"},
        ],
        "calc": """
            const p = num('price'), d = num('disc') / 100, r = num('r') / 100;
            const net = p * (1 - d);
            ToolBox.setResult('result', dataGrid([
                [net.toFixed(2), '折后价'],
                [(net * r).toFixed(2), '税额']
            ]));
        """,
        "notes": ["200、20 折、13% → 折后 160、税 20.8。", "视同销售按公允价。"],
    },
    {
        "slug": "break-even-taxable", "industry": "tax", "cat": "tax", "icon": "📊", "bg": "#fef2f2",
        "title": "盈亏平衡应税额", "h1": "盈亏平衡应税额计算器",
        "h2": "应税所得 = 固定扣除 / 边际税率", "intro": "估算达到税后目标所需的应税所得。",
        "desc": "盈亏平衡应税：输入目标税后所得、税率与扣除求应税所得。",
        "inputs": [
            {"id": "target", "label": "目标税后所得", "value": "750000", "step": "10000"},
            {"id": "deduct", "label": "免税/扣除额", "value": "0", "step": "1000"},
            {"id": "r", "label": "税率 (%)", "value": "25", "step": "1"},
        ],
        "calc": """
            const t = num('target'), d = num('deduct'), r = num('r') / 100;
            const taxable = (t + d) / (1 - r);
            ToolBox.setResult('result', dataGrid([
                [taxable.toFixed(2), '所需应税所得'],
                [(taxable * r).toFixed(2), '应纳税额']
            ]));
        """,
        "notes": ["税后 75 万、25% → 应税 100 万。", "税前沿 = 税后/(1−r)。"],
    },
]

if __name__ == "__main__":
    main(TOOLS)
