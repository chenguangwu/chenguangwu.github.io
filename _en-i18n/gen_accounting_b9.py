#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accounting 第9批：operating-cash-flow / quick-ratio / roa-calc / roe-calc / index"""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, '_en-i18n', 'work', 'accounting')
OUT = os.path.join(ROOT, 'i18n', 'tools', 'en', 'accounting')

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        for i, it in enumerate(items):
            print('   ', i, repr((it.get('zh') or '')[:50]))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'accounting', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))


# ---------------- operating-cash-flow (20) ----------------
write('operating-cash-flow', build('operating-cash-flow', [
    "Operating Cash Flow Calculator",
    "Compute operating cash flow from net income, depreciation and amortization and changes in working capital.",
    "OCF = Net Income + Depreciation & Amortisation − Change in Working Capital",
    "/ Operating Cash Flow Calculator",
    "Operating Cash Flow Calculator",
    '📖 View the "Operating Cash Flow Calculator Guide"',
    "Net income (10k CNY)",
    "Increase in working capital (10k CNY)",
    "The indirect method starts from net income.",
    "120+50−20 → 1,500,000 CNY.",
    "📚 In-Depth Analysis: Operating Cash Flow Calculator",
    "Uses the indirect method to convert net income into the true cash inflow from operating activities.",
    "Assesses the core business's ability to generate its own cash and whether operations can cover investment and debt service.",
    "Monitors divergence between accrual profit and cash flow to warn of deteriorating earnings quality.",
    "Computing Operating Cash Flow by the Indirect Method",
    "A company has net income of 200 (10k CNY) and adds back depreciation and amortisation of 80 (10k CNY); an increase in working capital (higher receivables and inventory, lower payables) ties up 50 (10k CNY), so operating cash flow = 200+80−50 = 230 (10k CNY).",
    "Why add back depreciation and amortisation?",
    "Depreciation and amortisation are non-cash expenses: they reduce net income without any cash outflow, so the indirect method adds them back to restore a cash basis.",
    "Why does an increase in working capital reduce cash?",
    "Rising receivables or inventory, or falling payables, means cash is tied up (funding first, collecting later), so it is deducted; conversely, cash released is added back.",
]))

# ---------------- quick-ratio (20) ----------------
write('quick-ratio', build('quick-ratio', [
    "Quick Ratio Calculator",
    "Compute the quick ratio from current assets, inventory and current liabilities to assess short-term solvency excluding inventory.",
    "Quick Ratio",
    "/ Quick Ratio",
    '📖 View the "Quick Ratio Calculator Guide"',
    "Quick Ratio = (Current Assets − Inventory) / Current Liabilities",
    "Inventory (CNY)",
    "Excludes slow-moving inventory.",
    "The ideal value is about 1.",
    "📚 In-Depth Analysis: Quick Ratio Calculator",
    "Beyond the ",
    ", the quick ratio strips out slower-moving inventory to gauge immediate solvency.",
    "For companies with a high inventory share (such as retail and real estate), the quick ratio matters more than the current ratio.",
    "When creditors review short-term positions, the quick ratio is the stricter baseline indicator.",
    "Computing the Quick Ratio",
    "A company has current assets of 800 (10k CNY) (including inventory of 300 (10k CNY)) and current liabilities of 400 (10k CNY), so the quick ratio = (800−300)/400 = 1.25, meaning quick assets excluding inventory still cover 1.25 times short-term liabilities.",
    "What do quick assets include?",
    "They usually include cash, trading financial assets, accounts receivable and other assets that convert to cash quickly; a conservative measure also excludes receivables whose collection is uncertain.",
    "Must the quick ratio be at least 1?",
    "A ratio of 1 or more means quick assets cover short-term liabilities and is relatively safe; but strong-cash-flow industries such as FMCG can run below 1 without worry, so judge it together with collection speed.",
]))

# ---------------- roa-calc (18) ----------------
write('roa-calc', build('roa-calc', [
    "Return on Assets (ROA) Calculator",
    "Compute return on assets from net income and average total assets to measure the profit generated per unit of assets.",
    "Return on Assets (ROA)",
    "/ Return on Assets (ROA)",
    '📖 View the "Return on Assets (ROA) Calculator Guide"',
    "ROA = Net Income / Total Assets × 100%",
    "Measures how efficiently assets are used.",
    "Not directly comparable across industries.",
    "📚 In-Depth Analysis: Return on Assets (ROA) Calculator",
    "Measures a company's ability to generate profit with all its assets and evaluates management's resource-allocation efficiency.",
    "Compare ROA with peers to judge whether asset expansion brings a corresponding return.",
    "Investors combine ROA with leverage to understand where ROE comes from.",
    "Computing Return on Assets",
    "A company has net income of 400 (10k CNY) and average total assets of 4000 (10k CNY), so ROA = 400/4000 = 10% - every 1 yuan of assets generates 0.1 yuan of net profit a year.",
    "What is the difference between ROA and ROE?",
    "ROA looks at the return on all assets (including those funded by debt), while ROE looks only at the return on shareholders' capital; ROE is amplified by leverage, whereas ROA better reflects the asset base's own profitability.",
    "What does a low ROA but high ROE indicate?",
    "It indicates that heavy use of debt amplifies shareholder returns but also accumulates financial risk; watch out for unsustainable leverage.",
]))

# ---------------- roe-calc (20) ----------------
write('roe-calc', build('roe-calc', [
    "Return on Equity (ROE) Calculator",
    "Compute return on equity from net income and average shareholders' equity to gauge the return on invested capital.",
    "Return on Equity (ROE)",
    "/ Return on Equity (ROE)",
    '📖 View the "Return on Equity (ROE) Calculator Guide"',
    "ROE = Net Income / Net Assets × 100%",
    "Net assets (CNY)",
    "The return metric shareholders watch most.",
    "High leverage can amplify ROE.",
    "📚 In-Depth Analysis: Return on Equity (ROE) Calculator",
    "The return metric shareholders care about most, measuring how efficiently their own capital grows.",
    "Compare ROE with peers to assess management's ability to create shareholder value.",
    "Combine with dividend and reinvestment policy to judge how efficiently retained earnings are used.",
    "Computing Return on Equity",
    "A company has net income of 400 (10k CNY) and average equity of 2000 (10k CNY), so ROE = 400/2000 = 20% - every 1 yuan invested by shareholders returns 0.2 yuan a year.",
    "Is a high ROE always good?",
    "A high ROE may come from high profitability or from high leverage (high risk). Break down its drivers to tell whether the return is from excellent operations or piled-up debt.",
    "ROE and earnings per share (",
    ") relationship?",
    "ROE = EPS ÷ book value per share; at the same ROE, a smaller equity base means a higher EPS; but relying too much on debt to lift ROE sacrifices financial safety.",
]))

# ---------------- index (74) ----------------
write('index', build('index', [
    "🧾 Accounting & Audit Tools",
    "Accounting & Audit",
    "Accounting & Audit Tools",
    "Cash Conversion Cycle Calculator",
    "Compute the cash cycle from receivable, inventory and payable days.",
    "Split Bill Calculator",
    "Split Bill Calculator is a free online accounting and audit tool: enter the parameters to get results in real time. It runs entirely in the front end, uploads no data, requires no registration and works right in your browser.",
    "VAT calculator: enter the tax-exclusive or tax-inclusive price and the applicable rate to quickly convert the tax-inclusive amount and compute the VAT payable, for general taxpayers' invoicing and tax calculation.",
    "Corporate income tax prepayment estimator: enter the quarterly total profit and the applicable rate to quickly estimate the quarterly prepayment, supporting quarterly filing and cash planning.",
    "Return on Equity (ROE)",
    "Enter net income and average shareholders' equity to compute ROE, reflecting the return on shareholders' investment, for investment analysis, management appraisal and capital return assessment.",
    "Return on Assets (ROA)",
    "Enter net income and average total assets to compute ROA, measuring profit generated per unit of assets, for profitability assessment and cross-period or cross-industry benchmarking.",
    "Build a corporate financial risk assessment model: enter leverage, cash flow and profitability metrics to get a risk grade and early-warning signals, for credit review, internal control checks and business risk screening.",
    "Enter net income and revenue to compute the net profit margin, reflecting final profit as a share of revenue, for earnings-quality assessment, operating benchmarking and investor analysis of financial statements.",
    "ROE = Net Profit Margin × Asset Turnover × Equity Multiplier",
    "DuPont ROE analysis calculator: enter the net profit margin, asset turnover and equity multiplier to break ROE = net margin × turnover × equity multiplier into its drivers.",
    "(Revenue − Cost) / Revenue",
    "Interest Coverage = EBIT / Interest Expense",
    "Interest coverage calculator: enter EBIT and interest expense to compute the interest coverage ratio = EBIT / interest expense as a solvency safety margin, for creditor risk assessment.",
    "DPO = Accounts Payable / Cost of Goods Sold × 365",
    "Days payable outstanding (DPO) calculator: enter the accounts payable balance and annual cost of goods sold to compute the payment cycle as DPO = AP / COGS × 365 for better cash flow planning.",
    "DSCR = Operating Cash Flow / Debt Service",
    "Debt service coverage ratio (DSCR) calculator: enter operating cash flow and annual debt service to compute DSCR = operating cash flow / debt service as a measure of debt capacity, for loan underwriting.",
    "DSO = Accounts Receivable / Revenue × 365",
    "Days sales outstanding (DSO) calculator: enter accounts receivable and annual revenue to compute the collection cycle as DSO = AR / revenue × 365, assessing collection efficiency and cash tie-up.",
    "OCF = Net Income + Depreciation & Amortisation − Change in Working Capital",
    "Operating cash flow (OCF) calculator: enter net income, depreciation and amortisation and the change in working capital to compute OCF = net income + depreciation − change in working capital for core-business cash inflow.",
    "Cost Accounting Method",
    "Aggregate and compute the full product cost, splitting fixed and variable costs to output unit cost and the break-even point, for manufacturing cost accounting, pricing analysis and cost control.",
    "Break-Even Point",
    "Break-even point calculator: enter fixed cost, unit price and unit variable cost to compute the break-even volume as BEP = fixed cost / (price − unit variable cost), supporting operating decisions.",
    "Financial Analysis, Decision and Forecasting Model",
    "An integrated model for financial analysis, decision-making and forecasting: enter historical financial data to get trend readouts and scenario estimates, for corporate budgeting, business review and financing decisions.",
    "Debt-to-Asset Ratio",
    "Enter total liabilities and total assets to compute the debt-to-asset ratio, measuring long-term solvency and leverage, for financial statement analysis, credit review and capital structure assessment.",
    "FCF = OCF − Capital Expenditure",
    "Compute free cash flow from operating cash flow and capital expenditure.",
    "DIO = Inventory / Cost of Goods Sold × 365",
    "Days inventory outstanding (DIO) calculator: enter the inventory balance and annual cost of goods sold to compute the inventory turnover cycle as DIO = inventory / COGS × 365, optimising stock management.",
    "WC = Current Assets − Current Liabilities",
    "Enter current assets and current liabilities to compute net working capital, measuring short-term funds available, for cash flow planning, liquidity management and working-capital gap diagnosis.",
    "Double Declining Balance",
    "Double declining balance depreciation calculator: enter cost, salvage value and useful life to charge accelerated depreciation as annual depreciation = beginning book value × 2/n (adjusted to salvage value in the final year), for accelerated depreciation accounting.",
    "Inventory Turnover",
    "Enter cost of sales and average inventory to compute inventory turnover and turnover days, measuring how fast inventory converts to cash, for warehouse management, supply-chain efficiency and slow-moving stock diagnosis.",
    "Amortisation of Intangible Assets",
    "Straight-line intangible asset amortisation calculator: enter cost, residual value and amortisation life to compute the annual amortisation as (cost − residual value) / life, for amortisation accounting and financial statement preparation.",
    "Current ratio calculator: enter current assets and current liabilities to compute the current ratio = current assets / current liabilities as a short-term solvency indicator, for financial health analysis and credit assessment.",
    "Bookkeeping and Financial Statement Preparation",
    "Supports the preparation of vouchers, ledgers and financial statements, automatically summarising account balances and the trial balance, for small-business bookkeeping, agency bookkeeping and period-end closing.",
    "Asset Turnover = Revenue / Total Assets",
    "Enter revenue and average total assets to compute total asset turnover as revenue ÷ total assets, measuring how efficiently assets generate revenue, for operating capability analysis and industry benchmarking.",
    "Contribution Margin",
    "Enter the unit price and unit variable cost to compute the unit contribution margin and contribution margin ratio, helping judge whether fixed costs are covered and profit is made, for cost-volume-profit analysis and product profitability assessment.",
    "Gross Profit = Revenue − Cost of Sales",
    "Enter revenue and cost of sales to compute gross profit and gross margin, directly reflecting the product's initial profit room, for sales accounting, pricing strategy and performance assessment.",
    "Sum-of-Years-Digits Method",
    "Quick Ratio",
    "(Current Assets − Inventory) / Current Liabilities",
    "Straight-Line Depreciation",
    "(Cost − Salvage Value) / Useful Life",
    "EBITDA = EBIT + Depreciation & Amortisation",
    "EBITDA calculator: enter EBIT and depreciation and amortisation to compute EBITDA = EBIT + D&A as earnings before interest, tax, depreciation and amortisation, assessing operating cash generation.",
    "EBIT = Revenue − Operating Cost − Operating Expenses",
    "EBIT calculator: enter revenue, operating cost and operating expenses to compute EBIT = revenue − cost − expenses for operating earnings, used for cross-company profit comparison.",
    'About "Accounting & Audit Tools"',
    "The Accounting & Audit Tools collection includes 35 free online tools covering common calculation, conversion and lookup needs in accounting and auditing. Whether you are a practitioner, a student or a general user, you will find handy tools here that are ready to use instantly. All tools run entirely in the front end, upload no data to any server and keep your privacy safe.",
    "The accounting and audit tools on this page include (a selection of representative tools):",
    "These tools help you complete common accounting and audit tasks quickly, with no need to memorise complex formulas or convert by hand - just enter your values and get results.",
    "Do the accounting and audit tools require downloading or registration?",
    "No. All the accounting and audit tools on this page are pure front-end online tools that work as soon as you open the page - no software to install, no account to register and no data uploaded.",
    "Are the results of the accounting and audit tools accurate? Is the data safe?",
    "The tools compute locally in your browser based on public mathematical formulas and common industry standards, with results available instantly. All calculations are performed on your device; no data is uploaded to any server, so your privacy is protected.",
]))
