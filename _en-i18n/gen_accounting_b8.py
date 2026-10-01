#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""accounting 第8批：interest-coverage / inventory-days / inventory-turnover / net-profit-margin"""
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


# ---------------- interest-coverage (20) ----------------
write('interest-coverage', build('interest-coverage', [
    "Interest Coverage Ratio Calculator",
    "Compute the interest coverage ratio as EBIT divided by interest expense to measure the margin of safety for creditors.",
    "Interest Coverage Ratio = EBIT / Interest Expense",
    "/ Interest Coverage Ratio Calculator",
    "Interest Coverage Ratio Calculator",
    '📖 View the "Interest Coverage Ratio Calculator Guide"',
    "Interest Coverage Ratio = EBIT / Interest Expense",
    "EBIT (10k CNY)",
    "Interest expense (10k CNY)",
    "The higher the ratio, the safer the interest payments.",
    "📚 In-Depth Analysis: Interest Coverage Ratio Calculator",
    "Creditors assess a company's ability to pay interest from operating profit; it is an important lending threshold.",
    "Monitor a falling interest coverage ratio to warn of excessive leverage or deteriorating earnings.",
    "In bond pricing, a higher ratio means lower default risk and financing cost.",
    "Computing the Interest Coverage Ratio",
    "A company has EBIT of 200 (10k CNY) and interest expense of 40 (10k CNY), so the interest coverage ratio = 200/40 = 5 times, meaning operating profit is five times the interest expense - a comfortable margin of safety for interest payments.",
    "Below what level is the interest coverage ratio dangerous?",
    "A ratio below 1.5 is generally seen as a clear rise in risk, and below 1 operating profit no longer covers interest; but cyclical industries swing widely, so look at the long-term average.",
    "Should the numerator be EBIT or EBITDA?",
    "EBIT is more conservative (it already includes the cash pressure of depreciation and amortisation); some industries use EBITDA coverage (since depreciation is non-cash), but that overstates the ability to pay interest.",
]))

# ---------------- inventory-days (20) ----------------
write('inventory-days', build('inventory-days', [
    "Inventory Days (DIO) Calculator",
    "Compute days inventory outstanding from inventory balance and annual cost of goods sold to optimize stock management.",
    "DIO = Inventory / Cost of Goods Sold × 365",
    "/ Inventory Days Calculator",
    "Inventory Days Calculator",
    '📖 View the "Inventory Days Calculator Guide"',
    "DIO = Inventory / Cost of Goods Sold × 365",
    "Inventory balance (10k CNY)",
    "The shorter the DIO, the faster inventory is converted to cash.",
    "150/600×365 → 91.25 days.",
    "📚 In-Depth Analysis: Inventory Days Calculator",
    "Measures the average days inventory is held from receipt to sale to assess stock efficiency.",
    "For seasonal stockpiling, estimate inventory days to avoid overstock or stockouts.",
    "Compare with peers to identify strengths and weaknesses in supply-chain management.",
    "Computing Days Inventory Outstanding",
    "A company has ending inventory of 300 (10k CNY) and annual cost of goods sold of 3600 (10k CNY), so inventory days = 300 ÷ (3600/365) = 300 ÷ 9.863 ≈ 30.4 days, meaning inventory turns over about every 30 days.",
    "Is a shorter inventory days always better?",
    "Usually the shorter, the less capital tied up and the lower the risk of price declines, but too short can mean frequent stockouts and lost sales; balance it against safety stock and the replenishment cycle.",
    "Use cost of goods sold or revenue?",
    "Inventory corresponds to the cost of goods sold, so using cost of goods sold (COGS) matches better; using revenue would mix in gross profit and overstate turnover efficiency.",
]))

# ---------------- inventory-turnover (20) ----------------
write('inventory-turnover', build('inventory-turnover', [
    "Inventory Turnover Calculator",
    "Compute inventory turnover and turnover days from cost of goods sold and average inventory balance.",
    "Inventory Turnover",
    "/ Inventory Turnover",
    '📖 View the "Inventory Turnover Calculator Guide"',
    "Inventory Turnover = Cost of Sales / Average Inventory",
    "Cost of sales (CNY)",
    "Average inventory (CNY)",
    "The higher the turnover, the faster inventory is converted to cash.",
    "Days = 365 / Turnover.",
    "📚 In-Depth Analysis: Inventory Turnover Calculator",
    "Measures how many times inventory is sold and replenished in a year, reflecting operating efficiency.",
    "Retail, manufacturing and other industries use turnover to assess whether purchasing and sales are in step.",
    "Compare with the industry to spot slow-moving goods or overstocking.",
    "Computing Inventory Turnover",
    "A company has annual cost of sales of 3600 (10k CNY), beginning inventory of 250 (10k CNY) and ending inventory of 350 (10k CNY), so average inventory = 300 (10k CNY) and inventory turnover = 3600/300 = 12 times per year, turning over about every 30 days.",
    "How does inventory turnover relate to inventory days?",
    "The two are reciprocals (days = 365 ÷ turnover); a high turnover corresponds to few days, and both measure inventory operating efficiency from different angles.",
    "Is a high turnover always good?",
    "High turnover usually means strong sales and efficient use of capital, but it may also mean understocking and missed sales; fresh-goods industries turn over naturally fast while durable goods are slower, so compare within the same industry.",
]))

# ---------------- net-profit-margin (19) ----------------
write('net-profit-margin', build('net-profit-margin', [
    "Net Profit Margin Calculator",
    "Compute the net profit margin from net income and revenue to assess final profitability and earnings quality.",
    "/ Net Profit Margin",
    '📖 View the "Net Profit Margin Calculator Guide"',
    "Net Profit Margin = Net Income / Revenue × 100%",
    "Net profit margin includes all expenses and taxes.",
    "It reflects the final level of profitability.",
    "📚 In-Depth Analysis: Net Profit Margin Calculator",
    "Measures a company's final profitability and how efficiently revenue converts into net income.",
    "Compare with peers to assess operating efficiency and cost control.",
    "Investors use the net margin trend to judge the direction of a company's profitability.",
    "Computing the Net Profit Margin",
    "A company has net income of 150 (10k CNY) and revenue of 1000 (10k CNY), so the net profit margin = 150/1000 = 15% - for every 1 yuan of revenue, 0.15 yuan remains as net profit.",
    "Which factors affect the net profit margin the most?",
    " determines the room, while period ",
    "expense ratio",
    " (selling/administrative/R&D), interest and tax burden determine how much is eroded; cost reduction and efficiency gains plus reasonable tax planning can all improve the net profit margin.",
    "Is it normal for the net profit margin to swing?",
    "One-off gains and losses (asset disposals, government subsidies, impairments) make the margin fluctuate; the non-recurring adjusted net margin better reflects the core business's sustainable profitability.",
]))
