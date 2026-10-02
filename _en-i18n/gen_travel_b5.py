#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'travel')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'travel')
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
    out = {'slug': slug, 'industry': 'travel', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('currency-cheat-sheet', build('currency-cheat-sheet', [
        "\U0001F4B1 Currency Cheat Sheet Generator",
        "Generate quick reference tables for common amounts so you can convert in your head while shopping. Exchange rates are for reference only.",
        "Currency Cheat Sheet",
        "/ Currency Cheat Sheet",
        "\U0001F4CB Cheat Sheet",
        "\U0001F30D Currency List",
        "\U0001F4A1 Exchange Tips",
        "Select Currency",
        "US Dollar USD ($)",
        "Euro EUR (\u20ac)",
        "Japanese Yen JPY (\u00a5)",
        "British Pound GBP (\u00a3)",
        "South Korean Won KRW (\u20a9)",
        "Hong Kong Dollar HKD",
        "New Taiwan Dollar TWD",
        "Singapore Dollar SGD",
        "Thai Baht THB (\u0e3f)",
        "Australian Dollar AUD",
        "Canadian Dollar CAD",
        "Malaysian Ringgit MYR",
        "Vietnamese Dong VND",
        "Indonesian Rupiah IDR",
        "Indian Rupee INR",
        "Swiss Franc CHF",
        "New Zealand Dollar NZD",
        "Russian Ruble RUB",
        "Macanese Pataca MOP",
        "Philippine Peso PHP",
        "Exchange Rate (1 unit of foreign currency = ? CNY)",
        "Amount Preset",
        "Standard Amounts",
        "Small Purchases",
        "Large Purchases",
        "Custom Amounts (comma-separated)",
        "\U0001F504 Reverse Conversion",
        "Search Currency",
        "\U0001F4B3 Exchange Method Comparison",
        "Convenience",
        "Domestic Bank Exchange",
        "Good",
        "ATM Withdrawal",
        "Fair",
        "Credit Card Spending",
        "Currency Conversion Fee",
        "Airport Exchange Counter",
        "Local Exchange Shop",
        "\U0001F9EE Fast Mental Math Tips",
        "Simplify the rate:",
        "Round the rate to an integer or a simple decimal for a quick estimate",
        "Remember key amounts:",
        "Memorize the CNY equivalent of common amounts such as 10, 50, 100 and 500",
        "Price anchor method:",
        "Use familiar item prices as reference (a bottle of water, a meal)",
        "Divide by a round number:",
        "If the USD rate is 7, roughly divide by 7 and multiply by 10",
        "Allow for fees:",
        "Credit card spending abroad usually carries a 1 to 2% currency conversion fee",
        "\U0001F4A1 Money-saving Tips",
        "Get a credit card with no foreign transaction fee:",
        "Many all-currency cards waive the 1.5% currency conversion fee",
        "Watch exchange rate trends:",
        "Exchange at rate lows; for long trips, exchange in batches",
        "Prefer cash in the local currency:",
        "Small shops may not accept credit cards or charge a fee",
        "Use a debit card for ATM withdrawals:",
        "Credit card cash advances carry high interest, so use a savings debit card",
        "Keep some small denominations:",
        "For tips, short trips and emergencies",
        "\u26a0\ufe0f The rates above are for reference only; actual rates follow the bank. Check the latest rate before travelling abroad.",
        "\U0001F4DA In-Depth Analysis: Currency Cheat Sheet Conversion",
        "Cash Conversion Abroad",
        "Estimating Small Foreign Amounts",
        "Rates at Your Fingertips",
        "100 USD in CNY",
        "Choose USD (rate about 7.2) and enter 100 \u2192 100 \u00f7 7.2 \u2248 13.89; in other words 100 CNY corresponds to about 13.89 USD, and in reverse 100 USD \u00d7 7.2 \u2248 CNY 720.",
        "Small Denomination Examples",
        "Choose the small-denomination set [1, 5, 10, 20, 50, 100] to list the CNY equivalent of each denomination by rate, which sets expectations for change at the airport.",
        "Where does the rate come from?",
        "A built-in reference rate is used by default; you can overwrite it in the rate field with the live quote and the results update accordingly.",
        "Can I save history?",
        "Switch to the history tab to see the 20 most recent conversions, stored locally.",
        "About \"Currency Cheat Sheet\"",
        "Currency Cheat Sheet is an online tool in the travel domain. A travel tool that is essential for trips and works offline.",
        "Enter a currency name or code...",
    ]))


if __name__ == '__main__':
    main()