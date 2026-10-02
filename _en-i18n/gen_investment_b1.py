#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'investment')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'investment')
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
    out = {'slug': slug, 'industry': 'investment', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('annuity-fv-inv', build('annuity-fv-inv', [
        "Find the future value of an annuity from the periodic contribution, interest rate and number of periods",
        "Enter the periodic contribution PMT, the periodic interest rate r and the number of periods n to obtain the future value of the annuity.",
        "Annuity Future Value Calculator",
        "/ Annuity Future Value Calculator",
        "\U0001F4D6 Read the \"Find the future value of an annuity from the periodic contribution, interest rate and number of periods\" guide",
        "Periodic contribution PMT (\u00a5)",
        "Suitable for fixed-amount periodic investing.",
        "1000, 5%, 10 periods \u2192 12578 CNY.",
        "\U0001F4DA In-depth analysis: annuity future value (accumulation of periodic contributions)",
        "Monthly or annual contributions: compute how much you will have accumulated after n years, for retirement or education fund planning.",
        "Compare how the ",
        "annuity future value",
        " differs across interest rates.",
        "Estimate ",
        "fund auto-invest (SIP) plans",
        " and installment deposits: total principal and interest after several periods (including reinvestment returns).",
        "Annual 1000, 5%, 10 years",
        "FV = 1000\u00d7((1.05\u00b9\u2070\u22121)/0.05) = 1000\u00d712.5779 \u2248 12578 CNY. That is, investing 1000 each year at 5% compound interest for 10 years gives about 12.6 thousand.",
        "Monthly 1000 CNY, monthly rate 0.5%, 60 periods in total",
        "FV=1000\u00d7[(1.005\u2076\u2070\u22121)/0.005]\u224869770.03 CNY; total contributions over the same period are only 60000 CNY, and the extra 9770.03 CNY comes from compounding.",
        "How does it differ from the ",
        "compound future value",
        "?",
        "Compound future value is a one-off principal earning interest; annuity future value accumulates a cash flow added each period, adding the dimension of the number of periods.",
        "How much does the result differ between end-of-period and beginning-of-period payments?",
        "This tool uses an ordinary annuity (contribution at the end of each period). If contributions are made at the beginning of each period, the future value must be multiplied by (1+r): in the example above 69770.03\u00d71.005\u224870118.88 CNY.",
    ]))
    write('annuity-pv-inv', build('annuity-pv-inv', [
        "Find the present value of an annuity from the periodic cash flow, interest rate and number of periods",
        "Enter the periodic cash flow PMT, the periodic interest rate r and the number of periods n to obtain the present value of the annuity.",
        "Annuity Present Value Calculator",
        "/ Annuity Present Value Calculator",
        "\U0001F4D6 Read the \"Find the present value of an annuity from the periodic cash flow, interest rate and number of periods\" guide",
        "Periodic cash flow PMT (\u00a5)",
        "When r=0 the present value degenerates to PMT\u00b7n.",
        "1000, 5%, 10 periods \u2192 7722 CNY.",
        "\U0001F4DA In-depth analysis: annuity present value (discounting periodic cash flows)",
        "A steady annual cash flow for n years: what is it worth today.",
        "Compare the present-value cost of a loan or an annuity product.",
        "Convert a series of cash flows such as installment receipts or a pension into one comparable lump-sum value today.",
        "Annual 1000, 5%, 10 years",
        "PV = 1000\u00d7(1\u22121.05\u207b\u00b9\u2070)/0.05 = 1000\u00d77.7217 \u2248 7722 CNY. That is, 1000 per year for the next 10 years discounted at 5% is worth about 7722 today.",
        "2000 CNY per period, period rate 1%, 36 periods in total",
        "PV=2000\u00d7[1\u2212(1.01)\u207b\u00b3\u2076]/0.01\u224860215.01 CNY; nominally 72000 CNY will be received in future, and the 11784.99 CNY difference is the time value of money.",
        "Are this and the ",
        "annuity future value",
        " inverses of each other?",
        "Yes. For the same set of cash flows, the future value is the value at a future date and the present value is the value today; they differ by a factor of (1+i)^n.",
        "Should 36 periods use a monthly rate or an annual rate?",
        "n and r must share the same unit: use a monthly rate for monthly receipts and an annual rate for annual receipts. 36 periods with a 1% monthly rate means a 3-year term; if you mistakenly use a 1% annual rate (roughly 12% annualized), the present value will be significantly understated.",
    ]))
    write('bond-price', build('bond-price', [
        "Discount the coupons and face value at the yield to maturity.",
        "Bond Pricing Calculator",
        "/ Bond Pricing",
        "Bond Pricing",
        "\U0001F4D6 Read the \"Bond Pricing Calculator\" guide",
        "Face value F",
        "Coupon rate (%)",
        "Term n (years)",
        "Payments per year",
        "YTM > coupon \u2192 traded at a discount.",
        "Semiannual payments are the most common.",
        "\U0001F4DA In-depth analysis: bond pricing (discounting coupons + face value)",
        "Given the coupon, yield to maturity and term, compute the fair price of the bond.",
        "See how the price falls when the yield rises (interest rate risk).",
        "Given the yield to maturity demanded by the market, work backwards to the fair trading price of the bond.",
        "Face value 1000, coupon 5%, YTM 6%, 10 years",
        "P = 50\u00d7\u00e4\u2081\u2080@6% (\u22487.360) + 1000\u00d7v\u00b9\u2070 (0.558) = 368 + 558 = 926 CNY. Since YTM > coupon, it trades at a discount.",
        "Face value 1000, coupon rate 5%, YTM 6%, term 5 years (semiannual payments)",
        "The page defaults to freq=2, i.e. two payments per year: each coupon c=1000\u00d75%/2=25 CNY, each discount rate y=6%/2=3%, with T=5\u00d72=10 periods. P=\u03a325/(1.03)^t (t=1\u202610)+1000/(1.03)\u00b9\u2070\u2248957.35 CNY. The coupon rate is below YTM, so it is issued at a discount.",
        "Why is the price below face value?",
        "The market yield of 6% is higher than the 5% coupon rate, so the old bond must be discounted to attract buyers; premium or discount is determined by the gap between YTM and coupon.",
        "How does the relationship between the coupon rate and YTM determine the price?",
        "Coupon rate > YTM means a premium (price above face value), equality means par, and lower means a discount. In the example the 5% coupon < 6% YTM, so the theoretical price of 957.35 CNY is below the 1000 CNY face value. Changing freq to 1 (annual payments) gives a price of about 957.88 CNY, showing that payment frequency also affects pricing.",
    ]))
    write('bond-ytm-approx', build('bond-ytm-approx', [
        "Find the approximate YTM from the annual interest, face value, price and remaining term",
        "Enter the annual interest C, face value F, price P and remaining term n to obtain the approximate YTM.",
        "Bond Yield to Maturity (Approximate) Calculator",
        "/ Bond Yield to Maturity (Approximate) Calculator",
        "\U0001F4D6 Read the \"Find the approximate YTM from the annual interest, face value, price and remaining term\" guide",
        "Price P (\u00a5)",
        "Remaining term n (years)",
        "The approximation ignores the timing structure of the cash flows.",
        "50, (1000\u2212950)/10, average price 975 \u2192 5.64%.",
        "\U0001F4DA In-depth analysis: approximate yield to maturity (YTM)",
        "Given the bond price, coupon, face value and term, quickly estimate the YTM.",
        "Compare the approximate holding return of different bonds.",
        "Without a financial calculator at hand, quickly estimate the annualized return of holding to maturity.",
        "Coupon 50, face value 1000, price 950, 10 years",
        "YTM \u2248 (50+(1000\u2212950)/10)/((1000+950)/2) = (50+5)/975 = 5.64%. Buying at a discount makes YTM higher than the 5% coupon rate.",
        "Annual interest 50 CNY, face value 1000 CNY, current price 950 CNY, 5 years remaining",
        "YTM\u2248[50+(1000\u2212950)/5]/[(1000+950)/2]=60/975\u22486.15% (the page displays two decimals). Besides the 50 CNY annual coupon, it also implies a 10 CNY annual accretion to face value.",
        "How much do the approximate and exact values differ?",
        "The approximate formula ignores the timing structure of cash flows, so the error grows slightly with longer terms; the exact YTM requires solving an equation, while the approximation is sufficient for quick comparisons.",
        "When is the error of the approximation largest?",
        "The longer the term and the further the price deviates from face value, the larger the error. It substitutes the average book amount for the true present value of cash flows and ignores coupon reinvestment; when an exact value is needed, use the ",
        "bond pricing",
        " tool to work backwards or compute the IRR of the cash flows.",
    ]))
    write('discounted-payback', build('discounted-payback', [
        "Years until cumulative discounted cash flow turns positive",
        "A payback period that accounts for the time value of money.",
        "Discounted Payback Period Calculator",
        "/ Dynamic Payback Period",
        "Dynamic Payback Period",
        "\U0001F4D6 Read the \"Years until cumulative discounted cash flow turns positive\" guide",
        "Discounted payback period = years until cumulative discounted cash flow turns positive",
        "Payback is slower after discounting.",
        "More conservative than the static payback period.",
        "\U0001F4DA In-depth analysis: discounted payback period",
        "Accounting for the time value of money, see how long it takes for the investment to pay back.",
        "More conservative than the static payback period.",
        "After accounting for the cost of capital, judge how long it truly takes to recover the investment.",
        "Invest 1000, cash flows 300/400/500, 10%",
        "After discounting 272.7/330.6/375.7, cumulative \u22121000\u2192\u2212727.3\u2192\u2212396.7\u2192\u221221.0, turning positive at about 3.07 years. Longer than the static payback period (2.6 years).",
        "Initial 5000 CNY, then 2500 CNY in each of the next 3 periods, discount rate 10%",
        "Cumulative discounted values are \u22125000, \u22122727.27, \u2212661.16, +1217.13 respectively, turning positive between periods 2\u21923; the interpolated payback period \u22482+661.16/1878.29\u22482.35 years.",
        "Why not rely only on the static payback period?",
        "The static measure ignores discounting, yet early cash is worth more; the discounted payback period is more realistic but still has the drawback of ignoring cash flows after the payback point.",
        "How much does it differ from the ordinary payback period?",
        "With the same cash flows undiscounted, cumulative values are \u22125000, \u22122500, 0, +2500, so it pays back in exactly 2 years; after discounting about 2.35 years. The extra 0.35 years is the cost of tying up capital over that period, and the gap widens as the discount rate rises.",
    ]))
    write('dividend-payout-ratio', build('dividend-payout-ratio', [
        "Find the dividend payout ratio from dividend per share and earnings per share",
        "Enter dividend per share DPS and earnings per share EPS to obtain the dividend payout ratio.",
        "Dividend Payout Ratio Calculator",
        "/ Dividend Payout Ratio Calculator",
        "\U0001F4D6 Read the \"Find the dividend payout ratio from dividend per share and earnings per share\" guide",
        "A low DPR means a high proportion is reinvested.",
        "\U0001F4DA In-depth analysis: dividend payout ratio",
        "See how much of the company's earnings is distributed to shareholders and assess the dividend policy.",
        "Compare dividend stability with peers or with the company's own history.",
        "Judge what proportion of current-period profit the company pays directly to shareholders.",
        "Payout ratio = 2/5 = 40%. That is, 40% of earnings is paid out as dividends and 60% is retained for reinvestment.",
        "Dividend per share DPS 1.2 CNY, earnings per share EPS 3 CNY",
        "DPR=1.2/3=40.00%, i.e. 0.4 CNY of every 1 CNY of earnings is paid out, with the remaining 60% retained in the company.",
        "Is a high payout ratio good?",
        "High dividends mean stable cash returns but less investment in growth; a low payout with high retention favors expansion. It depends on the company's stage: mature firms are usually high, growth firms usually low.",
        "What does a DPR above 100% mean?",
        "It means dividends exceed current-period earnings: the company has drawn on prior retained earnings or even borrowed to pay, which is usually not sustainable. It is common with one-off special dividends, or when a mature company strains to maintain a set dividend policy; operating cash flow should be checked at the same time.",
    ]))

if __name__ == '__main__':
    main()
