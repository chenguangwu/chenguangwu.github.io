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
    write('dividend-yield', build('dividend-yield', [
        "Dividend yield = annual dividend / share price",
        "The ratio of the dividend per share to the share price.",
        "Dividend Yield Calculator",
        "/ Dividend Yield",
        "Dividend Yield",
        "\U0001F4D6 Read the \"Dividend yield = annual dividend / share price\" guide",
        "Annual dividend per share",
        "Annual interest 3, share price 60 \u2192 5%.",
        "Unrelated to capital gains.",
        "\U0001F4DA In-depth analysis: dividend yield",
        "The annualized return of the dividend per share relative to the share price.",
        "Screen stocks for a high-dividend strategy.",
        "Compare dividend return levels across stocks with different prices.",
        "Annual dividend 3, share price 60",
        "Dividend yield = 3/60 = 5%. That is, the purchase price corresponds to a 5% annual dividend return.",
        "Annual dividend per share 2.5 CNY, share price 50 CNY",
        "Dividend yield=2.5/50=5.00%, equivalent to 5 CNY of cash dividend per year for every 100 CNY invested (before tax).",
        "Is a high dividend yield worth buying?",
        "A high yield may come with a sharp price drop or an unsustainable dividend; combine it with payout stability and fundamentals rather than looking at the number alone.",
        "Does the yield become distorted when the price crashes?",
        "Yes. The denominator is the share price, so a price crash mechanically inflates the yield, creating the so-called high-dividend trap. When judging, also check whether the total dividend is stable and whether there is a risk of future cuts; do not focus on the ratio alone.",
    ]))
    write('eps-calc', build('eps-calc', [
        "EPS = (net profit \u2212 preferred stock) / shares outstanding",
        "The earnings attributable to each common share.",
        "EPS Calculator",
        "/ Earnings Per Share (EPS)",
        "Earnings Per Share (EPS)",
        "\U0001F4D6 Read the \"EPS Calculator\" guide",
        "EPS = (net profit \u2212 preferred stock) / shares outstanding",
        "Preferred dividend",
        "Shares outstanding",
        "Net profit 10 million, 5 million shares \u2192 EPS 2.0.",
        "Preferred stock is deducted first.",
        "\U0001F4DA In-depth analysis: earnings per share (EPS)",
        "Compute earnings per share, the denominator of valuation.",
        "Compare profitability across companies with different share counts.",
        "Spread company earnings over each share so that firms with different share counts can be compared side by side.",
        "Net profit 10 million, preferred dividend 0, 5 million shares outstanding",
        "EPS = (10000000\u22120)/5000000 = 2 CNY per share. That is, earnings per share of 2 CNY.",
        "Net profit 300 million CNY, preferred dividend 0 CNY, share capital 100 million shares",
        "EPS=(300000000\u22120)/100000000=3.00 CNY per share, i.e. each share held corresponds to 3 CNY of annual earnings. If the company has preferred stock, the preferred dividend must be deducted from net profit before dividing by the common share capital.",
        "Why subtract preferred stock?",
        "Preferred dividends are paid first, so the profit attributable to common shareholders must exclude the preferred portion before dividing by the number of common shares outstanding.",
        "What is the difference between basic EPS and diluted EPS?",
        "Basic EPS uses the actual shares outstanding at period end; diluted EPS additionally assumes that convertible bonds, options and warrants are all converted into common shares, so the denominator is larger and the value lower. For conservative valuation, look at diluted EPS.",
    ]))
    write('future-value-inv', build('future-value-inv', [
        "Find the future value of an investment from the present value, interest rate and number of years",
        "Enter the present value PV, the annual interest rate r and the number of years n to obtain the future value.",
        "Compound Future Value Calculator",
        "/ Compound Future Value Calculator",
        "\U0001F4D6 Read the \"Find the future value of an investment from the present value, interest rate and number of years\" guide",
        "Present value PV (\u00a5)",
        "Compound future value of a one-off investment.",
        "10 thousand, 8%, 10 years \u2192 21589 CNY.",
        "\U0001F4DA In-depth analysis: investment future value (compound interest)",
        "Future value of a one-off principal at compound interest.",
        "Compare growth across different rates and terms.",
        "After a one-off investment, roll it up at compound interest to estimate total principal and interest at maturity.",
        "Principal 10 thousand, 8%, 10 years",
        "FV = 10000\u00d71.08\u00b9\u2070 = 10000\u00d72.1589 \u2248 21589 CNY. That is, 10 thousand at 8% compound interest for 10 years becomes about 21.6 thousand.",
        "Principal 50000 CNY, annual rate 6%, invested for 10 years",
        "FV=50000\u00d7(1.06)\u00b9\u2070\u224889542.38 CNY, of which 39542.38 CNY is interest, already more than 79% of the principal.",
        "How much do compound and simple interest differ?",
        "Simple interest over 10 years gives only 18 thousand; compound gives 21.6 thousand, and the gap from interest earning interest widens with the term.",
        "How do I switch from annual to monthly compounding?",
        "Divide the annual rate by the number of compounding periods and multiply the number of periods: with monthly compounding FV=PV(1+r/12)^(12n). The example above becomes about 90969.84 CNY with monthly compounding, 1427.46 CNY more than annual.",
    ]))
    write('geometric-mean-return', build('geometric-mean-return', [
        "Find the geometric mean return from a series of multi-period returns",
        "Enter the multi-period returns (comma or space separated) to obtain the geometric mean return.",
        "Geometric Mean Return Calculator",
        "/ Geometric Mean Return Calculator",
        "\U0001F4D6 Read the \"Find the geometric mean return from a series of multi-period returns\" guide",
        "Return series r",
        "The geometric mean accounts for compounding and is lower than the arithmetic mean.",
        "\U0001F4DA In-depth analysis: geometric mean return",
        "From a series of multi-period returns, compute the true annualized compound return.",
        "Avoid the arithmetic mean overstating volatile assets.",
        "When multi-period returns include both gains and losses, measure the true compound annualized level.",
        "Three years +10%, +20%, \u22125%",
        "G = (1.1\u00d71.2\u00d70.95)^(1/3) \u2212 1 = 1.254^0.333 \u2212 1 \u2248 7.83%. The true annualized return is about 7.8%, below the arithmetic mean of 8.3%.",
        "Three-year returns of +20%, \u221210%, +15%",
        "g=[1.20\u00d70.90\u00d71.15]^(1/3)\u22121\u22487.49%. The arithmetic mean gives 8.33%, clearly overstating the return actually received.",
        "Why is it lower than the arithmetic mean?",
        "Volatility drags compounding: a 20% gain followed by a 5% loss does not cancel out, so the geometric mean is always \u2264 the arithmetic mean, and the larger the volatility, the wider the gap.",
        "Why is the geometric mean always below the arithmetic mean?",
        "This is the volatility drag: up 10% then down 10% leaves net value at 0.99, so the arithmetic mean is 0% while you actually lost 1%. As long as returns fluctuate, the geometric mean is below the arithmetic mean, and the gap grows with volatility.",
    ]))
    write('holding-period-return', build('holding-period-return', [
        "Total return over the period including dividends.",
        "Holding Period Return Calculator",
        "/ Holding Period Return",
        "Holding Period Return",
        "\U0001F4D6 Read the \"Holding Period Return Calculator\" guide",
        "Purchase price P\u2080",
        "Sale price P\u2081",
        "Dividends during the period D",
        "100\u2192120 with dividend 4 \u2192 24%.",
        "Includes price and dividends.",
        "\U0001F4DA In-depth analysis: holding period return (HPR)",
        "Compute the total return over a holding period (including dividends).",
        "Compare real returns across different holding periods.",
        "Compute the complete return of a single investment over the holding period (including dividends received meanwhile).",
        "Buy at 100, sell at 120, dividend 4",
        "HPR = (120\u2212100+4)/100 = 24%. That is, total return of 24% over the holding period.",
        "Purchase price 50 CNY, sale price 62 CNY, dividends during the period 2 CNY",
        "HPR=(62\u221250+2)/50=28.00%, of which the price contributed 24 percentage points and dividends 4 percentage points.",
        "Must dividends be included?",
        "Yes. Total return = price change + interim cash flow (dividends/interest); counting only the price change understates the actual return.",
        "How do I annualize a holding period return?",
        "When held for t years, the annualized return = (1+HPR)^(1/t)\u22121. In the example, if held for 2 years, annualized = (1.28)^0.5\u22121\u224813.14%; simply dividing 28% by 2 to get 14% would overstate it.",
    ]))
    write('index', build('index', [
        "\U0001F4B9 Investment and Finance Tools",
        "Investment and Finance Tools",
        "Compound Future Value Calculator",
        "Find the future value of an investment from the present value, interest rate and number of years",
        "ROI Calculator",
        "ROI = (gain \u2212 cost) / cost",
        "Holding Period Return Calculator",
        "Holding Period Return Calculator. Enter the purchase price, sale price and dividends during the period to obtain the total return over the period including dividends, for the profit/loss and return assessment of a single investment.",
        "Bond Yield to Maturity (Approximate) Calculator",
        "Find the approximate YTM from the annual interest, face value, price and remaining term",
        "Geometric Mean Return Calculator",
        "Find the geometric mean return from a series of multi-period returns",
        "Real Rate of Return Calculator",
        "Find the real rate of return from the nominal return and the inflation rate",
        "Annuity Future Value Calculator",
        "Find the future value of an annuity from the periodic contribution, interest rate and number of periods",
        "Annuity Present Value Calculator",
        "Find the present value of an annuity from the periodic cash flow, interest rate and number of periods",
        "Profitability Index Calculator",
        "PI = present value of future cash flows / initial investment",
        "Dividend Payout Ratio Calculator",
        "Find the dividend payout ratio from dividend per share and earnings per share",
        "Payback Period Calculator",
        "Payback Period Calculator. Enter the cash flows of each period to find the year when cumulative cash flow turns from negative to positive, i.e. the number of years needed to recover the initial investment, for project liquidity and risk assessment.",
        "Investment Present Value Calculator",
        "Find the present value from the future value, discount rate and number of years",
        "Discounted Payback Period Calculator",
        "Discounted Payback Period Calculator. Enter the cash flows of each period and the discount rate to find the year when cumulative discounted cash flow turns from negative to positive: a payback assessment that accounts for the time value of money, for investment project evaluation.",
        "Retention Ratio Calculator",
        "Retention Ratio Calculator. Enter the dividend payout ratio DPR and compute the earnings retention ratio as b = 1 \u2212 DPR, for analyzing a company's reinvestment capacity and internal financing room.",
        "Sortino Ratio Calculator",
        "Sortino Ratio Calculator. Enter the portfolio return, risk-free rate and downside deviation to measure risk-adjusted return using downside risk only; it focuses more on losses than Sharpe, for fund performance evaluation.",
        "Bond Pricing Calculator",
        "Bond Pricing Calculator. Enter the face value, coupon rate, yield to maturity and term to obtain the bond price by discounting cash flows, for fixed-income valuation and trading reference.",
        "Sustainable Growth Rate Calculator",
        "Find the sustainable growth rate from return on equity and the retention ratio",
        "Net Present Value Calculator",
        "Net Present Value (NPV) Calculator. Enter the cash flows of each period and the discount rate to obtain the net present value by discounting; NPV>0 means the project is viable, for capital budgeting and project evaluation.",
        "Yield Spread Calculator",
        "Find the spread from the bond yield and the benchmark yield",
        "P/E Ratio Calculator",
        "Portfolio Beta Calculator",
        "Find the portfolio beta from the weights and betas of two assets",
        "Dividend Yield Calculator",
        "EPS Calculator",
        "EPS = (net profit \u2212 preferred stock) / shares outstanding",
        "Internal Rate of Return Calculator",
        "The discount rate at which NPV = 0",
        "About \"Investment and Finance Tools\"",
        "This collection of investment and finance tools includes 24 free online tools covering the common calculations, conversions and lookups needed in investment and wealth management. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. All tools run purely in the browser, data is not uploaded to any server, and your privacy and security are protected.",
        "The investment and finance tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common investment and finance tasks: no need to memorize complex formulas or convert manually, just enter values and get results.",
        "Do the investment and finance tools need to be downloaded or registered?",
        "No. All investment and finance tools on this page are pure front-end online tools: open the page and use them directly. No software to install, no account to register, and no data is uploaded.",
        "Are the calculation results accurate? Is the data secure?",
        "The tools compute locally in your browser based on public mathematical formulas and common industry standards, with instant results. All calculations are performed on your own device and data is never uploaded to a server, so your privacy and security are guaranteed.",
    ]))

if __name__ == '__main__':
    main()
