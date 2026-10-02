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
    write('irr-calc', build('irr-calc', [
        "The discount rate at which NPV = 0",
        "The project's own cash return rate, solved numerically by bisection.",
        "Internal Rate of Return Calculator",
        "/ Internal Rate of Return (IRR)",
        "\U0001F4D6 Read the \"The discount rate at which NPV = 0\" guide",
        "IRR > required return means the project is viable.",
        "When there are multiple positive roots, the conventional solution is used.",
        "\U0001F4DA In-depth analysis: internal rate of return (IRR)",
        "The discount rate that makes NPV=0, measuring the project's true return.",
        "Compare the returns of mutually exclusive projects.",
        "Set the present value of cash inflows equal to that of outflows to solve for the project's own rate of return.",
        "Invest 1000, cash back 300/400/500",
        "Solving NPV=\u22121000+300/(1+r)+400/(1+r)\u00b2+500/(1+r)\u00b3=0 gives r\u22489.7%. That is, the project's internal rate of return is about 9.7%.",
        "Cash flows \u22121000, 300, 400, 500, 200 (5 periods in total)",
        "Solving for the discount rate at which NPV=0 by bisection gives IRR\u224815.32%. Although period 5 is only 200 CNY, it participates in the ",
        "equation solution",
        "; if that period is entered as 0, the IRR falls to about 8.90%.",
        "How do you choose between IRR and NPV?",
        "IRR shows the return rate directly, but unconventional cash flows may produce multiple solutions; NPV looks at absolute value added and is more reliable for scale decisions.",
        "When can IRR not be computed?",
        "When the cash flow sign changes more than once (for example additional investment midway), multiple IRR solutions may appear; if all cash flows are positive or all negative there is no solution at all. For such projects look at NPV directly rather than relying on IRR.",
    ]))
    write('npv-calc', build('npv-calc', [
        "Discount the cash flows of each period at the discount rate to obtain the net present value.",
        "Net Present Value Calculator",
        "/ Net Present Value (NPV)",
        "\U0001F4D6 Read the \"Net Present Value Calculator\" guide",
        "NPV>0 usually means the project is viable.",
        "CF\u2080 is usually negative (initial investment).",
        "\U0001F4DA In-depth analysis: net present value (NPV)",
        "Discount all cash flows to see the net value added by the project; >0 is acceptable.",
        "Make investment decisions given a discount rate.",
        "Convert all future cash flows into today's value to judge whether the project is worthwhile.",
        "Invest 1000, cash back 300/400/500, discount 10%",
        "NPV = \u22121000+300/1.1+400/1.21+500/1.331 \u2248 \u221220.9. Slightly negative, meaning it is marginally not worthwhile at a 10% discount rate; the critical IRR is about 9.7%.",
        "Cash flows \u22121000, 500, 500, 500, 200, discount rate 10%",
        "NPV=\u22121000+500/1.1+500/1.21+500/1.331+200/1.4641\u2248380.03 CNY. The result is greater than 0, meaning the return exceeds the cost of capital and the project is viable.",
        "How should the discount rate be set?",
        "Use the required rate of return or the cost of capital (WACC); the higher it is, the lower the NPV, making it the key sensitivity variable.",
        "Why do NPV and IRR sometimes give opposite conclusions?",
        "Their reinvestment assumptions differ: NPV assumes interim cash flows are reinvested at the discount rate, IRR assumes reinvestment at the IRR itself. Conclusions may conflict for mutually exclusive projects or when the timing of cash flows differs greatly; NPV is usually the tie-breaker.",
    ]))
    write('payback-period', build('payback-period', [
        "Years until cumulative cash flow turns from negative to positive",
        "The number of years needed to recover the initial investment.",
        "Payback Period Calculator",
        "/ Static Payback Period",
        "Static Payback Period",
        "\U0001F4D6 Read the \"Years until cumulative cash flow turns from negative to positive\" guide",
        "Payback period = years until cumulative cash flow turns from negative to positive",
        "-1000+300+400+500 \u2192 break-even early in year 3, about 2.6 years.",
        "\U0001F4DA In-depth analysis: static payback period",
        "See how long it takes to break even without discounting, to screen projects quickly.",
        "Compare it with the ",
        "discounted payback period",
        " to see the effect of the time value of money.",
        "Roughly estimate how many years are needed to recover the initial outlay, measuring how long capital is tied up.",
        "Invest 1000, cash back 300/400/500",
        "Cumulative \u22121000\u2192\u2212700\u2192\u2212300\u2192+200, turning positive in year 3; payback period = 2+300/500 = 2.6 years.",
        "Cash flows \u22121000, 400, 400, 400, 200",
        "Cumulative cash flows are \u22121000, \u2212600, \u2212200, +200, +400, turning positive between periods 2\u21923; the interpolated payback period =2+200/400=2.50 years, and the 200 CNY in period 5 does not affect the payback point.",
        "Is a short payback period always good?",
        "A short payback reduces risk but ignores cash flows after break-even; high-return long-cycle projects may be wrongly screened out, so combine it with NPV.",
        "Why can the payback period not be used for decisions on its own?",
        "It ignores both cash flows after the payback point and the time value of money. A project that pays back in 2.5 years but earns nothing afterwards may be worse than one that pays back in 4 years yet has rich long-term cash flows, so it must be used together with NPV and IRR.",
    ]))
    write('pe-ratio', build('pe-ratio', [
        "P/E = share price / earnings per share",
        "The valuation multiple of the share price relative to earnings.",
        "P/E Ratio Calculator",
        "/ P/E Ratio (P/E)",
        "P/E Ratio (P/E)",
        "\U0001F4D6 Read the \"P/E Ratio Calculator\" guide",
        "Earnings per share EPS",
        "Share price 60, EPS 3 \u2192 P/E 20.",
        "The higher the multiple, the more expensive the valuation.",
        "\U0001F4DA In-depth analysis: P/E ratio",
        "See whether the price is cheap or expensive relative to earnings.",
        "Compare valuation levels with peers.",
        "Divide the market price per share by earnings per share to quickly judge whether the valuation is cheap or expensive.",
        "Share price 60, ",
        "P/E = 60/3 = 20x. That is, at current earnings it takes 20 years to recover the cost (undiscounted).",
        "Share price 45 CNY, earnings per share EPS 3 CNY",
        "PE=45/3=15.00x, meaning that on a static projection of current earnings it takes about 15 years of total profit to recover the cost (without counting earnings growth).",
        "Is a low P/E always cheap?",
        "A low P/E may mean earnings are about to fall or a cyclical peak; a high P/E may mean high growth. Judge it together with growth (PEG) and quality.",
        "What does a negative P/E mean?",
        "When a company is loss-making, EPS is negative and the P/E also turns negative and loses valuation reference value; in that case use the price-to-sales ratio PS or the ",
        "price-to-book ratio",
        " PB instead. Cyclical stocks also show an inflated P/E at the earnings trough, a classic valuation trap.",
    ]))
    write('portfolio-beta', build('portfolio-beta', [
        "Find the portfolio beta from the weights and betas of two assets",
        "Enter the weights w\u2081, w\u2082 and betas \u03b2\u2081, \u03b2\u2082 of two assets (w\u2081+w\u2082=1) to obtain the portfolio beta.",
        "Portfolio Beta Calculator",
        "/ Portfolio Beta Calculator",
        "\U0001F4D6 Read the \"Find the portfolio beta from the weights and betas of two assets\" guide",
        "Weight w\u2081",
        "Weight w\u2082",
        "The portfolio beta is a weighted average.",
        "\U0001F4DA In-depth analysis: portfolio beta (weighted average)",
        "Find the portfolio's systematic risk from the weights and betas of two assets.",
        "Manage risk exposure.",
        "Estimate the portfolio's systematic risk exposure relative to the market.",
        "50% each: \u03b2 1.0 and 1.4",
        "\u03b2p = 0.5\u00d71.0 + 0.5\u00d71.4 = 1.2. That is, a portfolio beta of 1.2, slightly more volatile than the market.",
        "Asset one weight 0.6, \u03b2=1.2; asset two weight 0.4, \u03b2=0.8",
        "\u03b2p=0.6\u00d71.2+0.4\u00d70.8=1.040, i.e. when the market rises 1%, the portfolio moves about 1.04% on average.",
        "How is it computed for more than two assets?",
        "The same weighting applies: \u03b2p = \u03a3 w\u1d62\u03b2\u1d62. Diversifying into low-correlation assets can lower the portfolio beta and reduce systematic risk.",
        "What if the weights do not add up to 1?",
        "The portfolio beta is a weighted average, so the weights must first be normalized. Cash holdings should also be included (cash \u03b2\u22480): for example 70% stocks with \u03b2=1.1 and 30% cash gives \u03b2p=0.7\u00d71.1+0.3\u00d70=0.77.",
    ]))
    write('present-value-inv', build('present-value-inv', [
        "Find the present value from the future value, discount rate and number of years",
        "Enter the future value FV, the discount rate r and the number of years n to obtain the present value.",
        "Investment Present Value Calculator",
        "/ Investment Present Value Calculator",
        "\U0001F4D6 Read the \"Find the present value from the future value, discount rate and number of years\" guide",
        "Future value FV (\u00a5)",
        "Present value is the future cash flow discounted at the interest rate.",
        "21589, 8%, 10 years \u2192 10000 CNY.",
        "\U0001F4DA In-depth analysis: present value (discounting a future value)",
        "Discount a future sum of money to today at the discount rate.",
        "Cross-check as the inverse of future value.",
        "Given the amount due in future, work backwards to the price you would pay today.",
        "Future 21589, 8%, 10 years",
        "PV = 21589/1.08\u00b9\u2070 = 21589/2.1589 = 10000 CNY. That is, 21589 in 10 years discounted at 8% has a present value of 10 thousand (mutually inverse with the ",
        "compound future value",
        ").",
        "100000 CNY received 7 years from now, discount rate 8%",
        "PV=100000/(1.08)\u2077\u224858349.04 CNY, i.e. paying 58349.04 CNY today is equivalent to 100000 CNY seven years later.",
        "How does it differ from the ",
        "annuity present value",
        "?",
        "This tool discounts a single future value; the annuity present value discounts multiple periodic cash flows, so the applicable scenarios differ.",
        "How should the discount rate be chosen?",
        "Usually take the opportunity cost of capital: your own investment return, the bank loan rate or the industry benchmark yield. Each 1 percentage point rise in the discount rate noticeably lowers the present value of long-term cash flows, so sensitivity analysis is essential.",
    ]))

if __name__ == '__main__':
    main()
