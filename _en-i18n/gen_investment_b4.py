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
    write('profitability-index', build('profitability-index', [
        "PI = present value of future cash flows / initial investment",
        "The present value return per unit of investment.",
        "Profitability Index Calculator",
        "/ Profitability Index (PI)",
        "\U0001F4D6 Read the \"Profitability Index Calculator\" guide",
        "PI = present value / initial investment",
        "PI>1 means the project adds value.",
        "\U0001F4DA In-depth analysis: profitability index PI (present value / initial investment)",
        "Divide the present value of future cash flows by the initial investment to get PI; only PI>1 is viable.",
        "Complementary to NPV: PI looks at present value return per unit invested.",
        "Compare the output efficiency per unit of investment among mutually exclusive projects when capital is constrained.",
        "Initial 1000, cash back 300/400/500, 10%",
        "Present value of future cash flows = 300/1.1+400/1.21+500/1.331 \u2248 979, PI = 979/1000 = 0.979 < 1, marginally not viable at a 10% discount rate (consistent with NPV\u2248\u221221). If the present value reached 1200 then PI=1.2 and it would be viable.",
        "Cash flows \u22121000, 500, 500, 500, discount rate 10%",
        "First discount and sum periods 1~3: 500/1.1+500/1.21+500/1.331\u22481243.43 CNY; PI=1243.43/1000\u22481.243, i.e. every 1 CNY invested brings about 1.243 CNY of present value return.",
        "What is the relationship between PI and NPV?",
        "PI>1 is equivalent to NPV>0; PI is a relative measure that compares efficiency across projects of different sizes, while NPV is the absolute value added.",
        "Are PI>1 and NPV>0 equivalent?",
        "For a single independent project they are exactly equivalent: PI = present value of future cash flows \u00f7 initial investment, so PI>1 means NPV>0. In the example, an initial investment of 1000 CNY and a present value of 1243.43 CNY correspond to NPV\u2248243.43 CNY. But when ranking mutually exclusive projects under a capital constraint, PI ranks by efficiency and NPV by absolute value added, so the two may select different projects.",
    ]))
    write('real-rate-return', build('real-rate-return', [
        "Find the real rate of return from the nominal return and the inflation rate",
        "Enter the nominal return r_nom and the inflation rate i to obtain the real rate of return.",
        "Real Rate of Return Calculator",
        "/ Real Rate of Return Calculator",
        "\U0001F4D6 Read the \"Find the real rate of return from the nominal return and the inflation rate\" guide",
        "Real = (1+nominal)/(1+inflation) \u2212 1",
        "Nominal return",
        "Inflation rate i",
        "Fisher approximation: r_real \u2248 r_nom \u2212 i.",
        "\U0001F4DA In-depth analysis: real rate of return (excluding inflation)",
        "Subtract inflation from the nominal return to see the growth in real purchasing power.",
        "Calibrate long-term savings targets.",
        "Strip out ",
        "inflation",
        " and see whether purchasing power really grew.",
        "Nominal 8%, inflation 3%",
        "Real = (1.08/1.03) \u2212 1 = 4.85%. That is, real purchasing power grows about 4.85% a year, not the 8% on paper.",
        "Set the nominal return to 0.07 and the ",
        "inflation rate",
        " to 0.03",
        "The exact value is r_real=1.07/1.03\u22121\u22483.88% (the page displays two decimals); using 7%\u22123%=4.00% directly slightly overstates the real return.",
        "Why can't you use 8%\u22123%=5%?",
        "The 5% approximation has an acceptable small error, but the exact formula (1+n)/(1+i)\u22121 is correct, and the gap becomes clear when inflation is high.",
        "Why can't the subtraction approximation be used?",
        "Because nominal return and inflation combine multiplicatively, not additively. The two are close when inflation is low, but the deviation grows with inflation: with a nominal 10% and inflation 20%, the exact real return is 1.10/1.20\u22121\u2248\u22128.33%, while subtraction gives \u221210%, clearly too pessimistic.",
    ]))
    write('retention-ratio', build('retention-ratio', [
        "Find the retention ratio from the dividend payout ratio",
        "Enter the dividend payout ratio DPR to obtain the retention ratio.",
        "Retention Ratio Calculator",
        "/ Retention Ratio Calculator",
        "\U0001F4D6 Read the \"Find the retention ratio from the dividend payout ratio\" guide",
        "Retention ratio = 1 \u2212 dividend payout ratio",
        "Dividend payout ratio DPR (%)",
        "Retained earnings are used for corporate reinvestment.",
        "\U0001F4DA In-depth analysis: retention ratio",
        "Derive from the ",
        "dividend payout ratio",
        " the proportion retained in the company.",
        "Combine with ROE to compute sustainable growth.",
        "See how much profit the company retains for reinvestment.",
        "Payout ratio 40%",
        "Retention ratio = 1 \u2212 40% = 60%. That is, 60% of earnings is retained for reinvestment.",
        "Dividend payout ratio DPR of 40%",
        "b=1\u221240%=60.00%, i.e. 0.6 CNY of every 1 CNY of earnings is retained in the business and the remaining 0.4 CNY is paid to shareholders.",
        "Is retaining earnings in the company always good?",
        "The premise is that the return on retained reinvestment ",
        "exceeds what shareholders could earn by investing themselves; inefficient retention destroys value, so check ROE and investment opportunities.",
        "Is a higher retention ratio always better?",
        "Not necessarily. A high retention ratio means abundant internal funds, but value is created only when the return on new capital exceeds the return shareholders require; otherwise distributing profit to shareholders is better, and blind retention only brings inefficient expansion.",
    ]))
    write('roi-calc', build('roi-calc', [
        "ROI = (gain \u2212 cost) / cost",
        "A simple ratio measuring the profitability of an investment.",
        "ROI Calculator",
        "/ Return on Investment (ROI)",
        "\U0001F4D6 Read the \"ROI Calculator\" guide",
        "ROI = (gain \u2212 cost)/cost",
        "\U0001F4DA In-depth analysis: return on investment (ROI)",
        "Compute the input-output ratio to quickly see whether a project pays off.",
        "Compare efficiency across projects.",
        "Use a single ratio to quickly measure the output efficiency of an investment.",
        "Gain 1300, cost 1000",
        "= (1300\u22121000)/1000 = 30%. That is, this ",
        "investment return",
        "Recovering 4800 CNY, investment cost 6000 CNY",
        "ROI=(4800\u22126000)/6000=\u221220.00%, the minus sign meaning the investment actually lost money.",
        "Does ROI ignore time?",
        "Yes. ROI carries no term, so a long-term low ROI may be worse than a short-term high ROI; combine it with the payback period or IRR.",
        "Which costs should be included for accuracy?",
        "All outlays needed to acquire the asset: purchase price, fees, taxes and subsequent required investment. Counting only the purchase price overstates the return: for example buying at 100 and selling at 110 looks like a 10% gain, but if 5 CNY of trading cost is omitted the true ROI is only about 4.76%.",
    ]))
    write('sortino-ratio', build('sortino-ratio', [
        "Measure risk-adjusted return using downside deviation only.",
        "Sortino Ratio Calculator",
        "/ Sortino Ratio",
        "\U0001F4D6 Read the \"Sortino Ratio Calculator\" guide",
        "Downside standard deviation (%)",
        "Weights downside risk more heavily than Sharpe.",
        "The denominator uses the downside standard deviation.",
        "\U0001F4DA In-depth analysis: Sortino ratio",
        "Punishes only downside volatility, focusing more than Sharpe on harmful risk.",
        "More suitable for strategies with large downside risk.",
        "Evaluate risk-adjusted return by penalizing downside volatility only.",
        "Portfolio 15%, risk-free 3%, downside \u03c3 6%",
        "Sortino = (15%\u22123%)/6% = 2.0. With smaller downside volatility, the ratio is above Sharpe (1.2), showing a better risk-adjusted result.",
        "Portfolio return 12%, risk-free rate 3%, downside deviation 8%",
        "Sortino ratio=(12%\u22123%)/8%=1.1250, i.e. 1.125 units of excess return per unit of downside risk borne.",
        "How does it differ from Sharpe?",
        "Sharpe uses total \u03c3 and penalizes all volatility, while Sortino uses only downside \u03c3 and penalizes loss volatility; Sortino fits asymmetric distributions better.",
        "How should this be chosen against the ",
        "Sharpe ratio?",
        "The Sharpe ratio uses total volatility, counting gains as risk too; Sortino uses only downside volatility, closer to an investor's real feeling about losses. For products whose return distribution is clearly right-skewed (frequent excess gains), Sortino is usually well above Sharpe.",
    ]))
    write('sustainable-growth', build('sustainable-growth', [
        "Find the sustainable growth rate from return on equity and the retention ratio",
        "Enter return on equity ROE and the retention ratio b to obtain the sustainable growth rate.",
        "Sustainable Growth Rate Calculator",
        "/ Sustainable Growth Rate Calculator",
        "\U0001F4D6 Read the \"Find the sustainable growth rate from return on equity and the retention ratio\" guide",
        "g = ROE \u00d7 retention ratio",
        "Return on equity ROE (%)",
        "Retention ratio b (%)",
        "Maximum growth rate without new issuance or new debt.",
        "\U0001F4DA In-depth analysis: sustainable growth rate g",
        "Compute the internal growth rate from ROE and the retention ratio without new issuance or debt.",
        "See how fast the company can grow on its own.",
        "Estimate the profit growth rate the company can sustain without adding new share capital.",
        "ROE 15%, retention ratio 60%",
        "g = 15%\u00d760% = 9%. That is, on retained profit alone, revenue/profit can grow sustainably by about 9%.",
        "Return on equity ROE 15%, ",
        "retention ratio",
        " 60%: g=15%\u00d760%=9.00%, meaning that without raising leverage or issuing new shares, earnings can keep growing at about 9% a year.",
        "What happens if growth exceeds g?",
        "Growing faster requires external financing (new issuance/debt) or higher ROE/retention; otherwise it is unsustainable and strains the finances.",
        "What assumptions does this formula make?",
        "It assumes an unchanged capital structure, a stable ROE and no new share issuance. In reality ROE often falls as scale grows, so actual growth is usually below the theoretical value; also note that if ROE is below the return shareholders require, high book growth is actually destroying value.",
    ]))
    write('yield-spread', build('yield-spread', [
        "Find the spread from the bond yield and the benchmark yield",
        "Enter the bond yield and the benchmark yield to obtain the spread.",
        "Yield Spread Calculator",
        "/ Yield Spread Calculator",
        "\U0001F4D6 Read the \"Find the spread from the bond yield and the benchmark yield\" guide",
        "Spread = bond yield \u2212 benchmark yield",
        "Bond yield",
        "Benchmark yield",
        "The spread reflects credit risk and liquidity.",
        "\U0001F4DA In-depth analysis: credit spread (bond yield \u2212 benchmark)",
        "Compute the excess return of a bond relative to a benchmark such as government bonds.",
        "Measure the credit risk premium.",
        "Judge whether the excess compensation of a bond relative to the benchmark is sufficient.",
        "Bond yield 5%, benchmark 3%",
        "Spread = 5% \u2212 3% = 2%. That is, bearing credit risk earns 200bp of excess return.",
        "0.058, benchmark yield 0.025",
        "Spread=(0.058\u22120.025)\u00d710000=330 basis points (1bp=0.01%, i.e. 3.30%), representing compensation for credit and liquidity risk.",
        "What does a widening spread mean?",
        "A widening spread usually reflects rising credit concerns or deteriorating liquidity; a narrowing one means improving risk appetite, a signal of the credit cycle.",
        "Why are quotes given in basis points rather than percentages? ",
        "Bond spread moves are usually only a few to a few dozen bp; basis points avoid decimal ambiguity and make it quick to say the spread narrowed 5bp. If you have percentage data (such as 5.80% and 2.50%), convert them to decimals 0.058 and 0.025 before entering.",
    ]))

if __name__ == '__main__':
    main()
