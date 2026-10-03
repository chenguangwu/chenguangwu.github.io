#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'sales')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'sales')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp
def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'sales', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('commission-calc', build('commission-calc', [
        "Commission Calculator",
        "Automatic tiered commission calculation, supporting excess-progressive and full-progressive methods",
        "Core calculation formula (by input variables): min(sales, upper) - lower; max(total - taxThr, 0); sales×useRate÷100",
        "📖 View the Commission Calculator Guide",
        "Excess-progressive",
        "Full-progressive",
        "Base salary (optional)",
        "Personal income tax threshold",
        "Commission tiers",
        "Load common template",
        "💵 Calculate commission",
        "Commission payable",
        "Each tier is calculated separately at its own rate and then summed;",
        "All sales are calculated at the highest tier rate reached.",
        "📚 In-depth: Commission Calculator",
        "Design a tiered commission policy: enter multiple sales thresholds and rates, and the tool automatically calculates commissions by tier using excess- or full-progressive methods, with a cap option.",
        "Verify a large single-order commission: when a big order spans multiple tiers, confirm each tier boundary and rate to avoid missing the higher tiers.",
        "Build a team commission budget: given total performance and tiers, estimate total commission and control the sales-expense ratio.",
        "Example: tiers 3%/5%/8% (excess-progressive) on 500,000 CNY",
        "Tiers: 0-100,000 at 3%, 100,000-300,000 at 5%, above 300,000 at 8%.\nTier 1: 100,000×3% = 3,000 CNY; Tier 2: 200,000×5% = 10,000 CNY; Tier 3: 200,000×8% = 16,000 CNY.\nTotal commission = 29,000 CNY. If 'full-progressive' is chosen, all 500,000 CNY is at 8% = 40,000 CNY; the gap is significant, so choose based on incentive goals.",
        "How much do excess- and full-progressive differ?",
        "For the same 500,000 CNY performance, excess-progressive gives 29,000 CNY and full-progressive 40,000 CNY; the higher the performance and the larger the tier gap, the bigger the difference. Excess-progressive is smoother and more common.",
        "How are the cap and tax exemption handled?",
        "You can set a cap (no further accrual beyond it) and a personal-tax exemption (default 0 or 5000) in the parameters; the tool estimates personal tax after totalling. The cap prevents a single abnormal order from inflating cost.",
        "About the Commission Calculator",
        "Commission Calculator - automatic tiered commission calculation, supporting custom tiers and excess-progressive. Free online sales tool. Business productivity tool, boosting work efficiency, with data processed locally for privacy.",
    ]))
    write('commission-calculator', build('commission-calculator', [
        "Sales Commission Calculator",
        "Supports four modes: fixed-rate, tiered, base-salary-plus-commission, and team commission, with automatic personal-tax estimation.",
        "📖 View the Sales Commission Calculator Guide",
        "Supports four commission models:",
        "Fixed rate",
        "(sales×r);",
        "Tiered commission",
        "(progressive by tier; the excess over the threshold uses the higher rate);",
        "Base salary + commission",
        "(base salary added);",
        "Team commission",
        "(total split by member share). Personal tax is estimated by the cumulative withholding method.",
        "Tier thresholds and rates follow company policy; note the difference between 'excess-progressive' and 'full-progressive'.",
        "Pre-/post-tax toggle affects net pay; the personal tax is an approximation, not a filing basis.",
        "This month's sales (CNY)",
        "Commission rate (%)",
        "Tier config (upper bound & rate %)",
        "Restore default",
        "Base salary (CNY)",
        "Excess portion rate (%)",
        "Team total sales (CNY)",
        "Team commission rate (%)",
        "Individual allocation factor (0-1)",
        "Personal tax estimation note:",
        "Uses the annual progressive tax table for comprehensive income, converted to monthly withholding (threshold 5,000 CNY/month including the basic deduction). It estimates only the approximate tax on the commission portion; the actual amount is subject to tax law.",
        "Commission model formulas",
        "Fixed rate: commission = sales × rate",
        "Tiered: each bracket is accumulated separately (excess portion at its corresponding rate)",
        "Base + commission: pre-tax income = base + max(0, sales - threshold) × rate",
        "Team: individual commission = team total × team rate × individual factor",
        "📚 In-depth: Sales Commission Calculator",
        "Fixed-rate commission: directly sales × fixed rate, suitable for stable unit prices and low volatility.",
        "Base plus commission: set a threshold, accrue only on the excess over it, balancing security and incentive.",
        "Team split: allocate by team total × team rate × individual share, suitable for channel/key-account teams.",
        "Example: fixed mode 500,000 CNY × 5%",
        "Choose 'Fixed rate' mode, sales 500,000 CNY, rate 5%.\nCommission = 500,000 × 5% = 25,000 CNY. Pre-tax income = base + 25,000; if base is 0, pre-tax is 25,000, and personal tax is estimated as 'taxable income = 25,000 - 5,000 = 20,000'.",
        "Which scenario suits each of the four modes?",
        "Fixed rate suits stable business; tiered progressive suits pushing for high performance; base plus commission suits newcomer protection; team split suits collaborative large deals. You can switch and compare on the same screen.",
        "Why is the tax threshold 5000 by default?",
        "The tool approximates with the monthly wage exemption of 5,000 CNY (merging commission into monthly wage tax is more complex; this is only a reference). Please follow your company's payroll system and tax filing.",
        "About the Sales Commission Calculator",
        "Sales Commission Calculator. A sales management tool that helps quantify performance and commission calculation.",
    ]))
    write('cost-price-margin', build('cost-price-margin', [
        "Cost Price Margin computes and outputs results based on the input parameters.",
        "/ Cost-Price / Selling-Price / Profit Converter",
        "📖 View the Cost-Price-Margin Guide",
        "💰 Cost / Selling Price / Profit Converter",
        "In business you often need reverse pricing: given cost and target margin to find selling price, or given price and cost to find margin. This tool cross-computes five variables; enter any two.",
        "Known cost + margin → find selling price",
        "Known price + margin → find cost",
        "Known cost + price → find margin",
        "Cost price (CNY)",
        "Selling price (CNY)",
        "📚 In-depth: Cost / Price / Margin Converter",
        "Reverse pricing: given cost and target",
        "margin",
        ", find the selling price to avoid arbitrary pricing that misses the gross-margin target.",
        "Back-calculate cost: given price and margin, derive the maximum acceptable cost for procurement negotiation.",
        "Check the margin basis: convert between 'margin (profit/selling price)' and 'markup (profit/cost)' to avoid mixing bases.",
        "Example: cost 100 CNY, target margin 25% → selling price",
        "Selling price = cost × (1 + margin) = 100 × (1 + 25%) = 125 CNY.\nProfit = 125 - 100 = 25 CNY; margin = 25/125 = 20.0% (note: 'margin 25%' here means 25% cost markup, corresponding to 20% selling-price margin).\nConversely, if price is 125 and cost 100, margin = 20.0%, markup = 25.0%.",
        "Aren't margin and markup the same thing?",
        "No. Margin = profit÷price (common in e-commerce), markup = profit÷cost (common in physical retail). At cost 100, price 125, margin is 20%, markup 25%; do not mix them. The tool has a built-in table (e.g. 50% margin = 100% markup) for quick lookup.",
        "How to use the five-variable cross-calculation?",
        "Enter any two to get the third: cost+margin→price; price+margin→cost; cost+price→margin/markup. Good for pricing sensitivity tests.",
        "(Gross) margin = (price - cost) ÷ price",
        "Markup = (price - cost) ÷ cost, a different basis from margin",
        "Enter any two to derive the rest, supporting both cost→price and price→cost directions",
        "Results are for reference only; set prices based on cost structure and market conditions",
    ]))
    write('index', build('index', [
        "Sales Management Tools",
        "Sales Management",
        "Sales Management Tools",
        "Supports four commission modes - fixed-rate, tiered progressive, base-plus-commission, and team split - and automatically computes commission from performance with cumulative-withholding tax estimation, simplifying sales compensation.",
        "Pricing Calculator",
        "Supports four strategies - cost-plus, target-profit, competitor-reference, and value pricing - outputting suggested price, gross margin, and break-even volume.",
        "Enter multiple discounts (coupon, threshold coupon, percentage offer) and stacking order; the tool computes final price and total savings, highlighting differences between stacking methods, helping e-commerce and stores design promotions.",
        "Enter sales and custom commission tiers (excess- or full-progressive); the tool calculates each tier's commission and totals it, supporting multi-tier rates and caps, simplifying team compensation.",
        "Cost / Selling Price / Profit Converter",
        "The Cost/Price/Profit Converter is a free online sales-management tool. In business you often reverse price: given cost and target margin to find price, or given price and cost to find margin. It cross-computes five variables; enter any two. Runs entirely in the browser, no data upload, no registration...",
        "Enter traffic at each marketing stage (visit, add-to-cart, order, payment); the tool computes each step's conversion and drop-off and visualizes the funnel, locating bottlenecks to optimize spend and pages.",
        "Split annual targets by region, month, or person and total them, verifying consistency, for sales planning; the pure-front-end split can export a table.",
        "Moving-average forecasting, supporting Simple Moving Average (SMA), Weighted Moving Average (WMA), and Exponential Smoothing (EMA)",
        "Forecasts future sales from historical monthly data using moving average, weighted moving average, linear regression, or seasonal methods.",
        "About Sales Management Tools",
        "The Sales Management Tools collection includes 9 free online tools covering common calculations, conversions, and lookups in sales management. Whether you are a professional, student, or general user, you will find ready-to-use mini tools here. All tools run purely in the browser, with no data uploaded to servers, protecting your privacy.",
        "The sales management tools on this page include (representative tools):",
        "These tools help you quickly complete common sales-management tasks without memorizing complex formulas or manual conversions; just enter to get results.",
        "Do the sales management tools need download or registration?",
        "No. All tools here are pure-front-end online tools; open the page and use them directly, no software install, no account registration, and no data upload.",
        "Are the calculation results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public math formulas and common industry standards, with instant results. All operations run on your device; data is never uploaded to servers, ensuring privacy and security.",
    ]))

if __name__ == '__main__':
    main()
