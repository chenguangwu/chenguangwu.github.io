#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'ecommerce')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'ecommerce')
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
    out = {'slug': slug, 'industry': 'ecommerce', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

DISCL_E = "Results are for e-commerce operations estimates, product selection and decision reference only; they are not financial or tax advice and do not replace the latest platform rules or formal reconciliation \u2014 the platform's official rules and actual accounts prevail."


def main():
    write('calc-79', build('calc-79', [
        "\U0001F9EE Growth Rate (YoY / MoM) Calculation",
        "Enter the current and comparison period values to compute the year-over-year growth rate, the growth amount and the multiple.",
        "\U0001F4D6 View the \"Growth Rate (YoY / MoM) Calculation Guide\"",
        "Growth rate = (current \u2212 comparison) / comparison \u00d7 100%",
        "This tool computes year-over-year and period-over-period growth rates from the current and base period values, handling a zero base period and cross-period comparisons automatically, and outputs both the percentage and the absolute change.",
        "Current value",
        "Comparison value",
        "\U0001F4A1 Growth rate = (current \u2212 comparison) \u00f7 comparison \u00d7 100%; growth contribution = growth amount \u00f7 current \u00d7 100%.",
        "\U0001F4DA In-depth Analysis: Growth Rate (YoY / MoM) Calculation",
        "Year over year: enter this year and the same month last year to compute YoY and strip out seasonal effects.",
        "Period over period: enter this month and last month to compute MoM and see the short-term trend.",
        "Classroom demo: when the base period is 0 the growth rate is undefined and needs special handling.",
        "Example: this month 120, last month 100, MoM=(120\u2212100)/100=20%; this year 120, same month last year 90, YoY=33.3%.",
        "What is the difference between YoY and MoM?",
        "YoY compares with the same period last year (removing seasonality), MoM with the previous period (a short-term view); they serve different purposes and must not be mixed. " + DISCL_E,
        "What if the base period is 0?",
        "With a base of 0 the formula is meaningless, so mark it as \"starting from 0\" or use the absolute increment to avoid infinity. " + DISCL_E,
        "What about a negative growth rate?",
        "If the current period is below the base period that is negative growth; just express the decline as a percentage. " + DISCL_E,
        "About \"Growth Rate (YoY / MoM) Calculation\"",
        "Growth Rate (YoY / MoM) Calculation.",
        "Enter the current and base periods to compute YoY and MoM automatically",
        "Year-over-year growth accounting for monthly business reports",
        "Tracking short-term trends period over period",
        "Special handling when the base period is 0",
        "Trend comparison across multiple metrics",
        "YoY",
        "MoM",
    ]))

    write('calc-commission-2', build('calc-commission-2', [
        "\U0001F9EE Commission (Platform / Service Fee) Calculation",
        "Compute commission and net proceeds from the transaction amount and the platform or service fee rate.",
        "\U0001F4D6 View the \"Commission (Platform / Service Fee) Calculation Guide\"",
        "Commission = transaction amount \u00d7 rate",
        "This tool computes platform commission, service fees and the amount received from the transaction value and commission rate (including tiered rates and caps), and supports trial calculations across several rate tiers.",
        "Transaction amount (\u00a5)",
        "Combined rate (%)",
        "\U0001F4A1 Commission = transaction amount \u00d7 rate; net proceeds = transaction amount \u2212 commission; a rate above 10% is on the high side.",
        "\U0001F4DA In-depth Analysis: Commission (Platform / Service Fee) Calculation",
        "Settlement trial: enter the transaction amount and rate to get the commission and the amount received.",
        "Tier comparison: enter rates for different tiers to see where commission jumps on large orders.",
        "Classroom demo: show how a cap affects high-value orders.",
        "Example: a transaction of 1000 at a 5% rate gives commission 50 and 950 received; with a cap of 30 the commission is 30.",
        "Does the commission base include shipping?",
        "Platform rules differ: some charge on the transaction amount, others exclude shipping, so follow the platform's settlement rules. " + DISCL_E,
        "How are tiered rates calculated?",
        "Commission is charged per segment at that tier's rate; watch for jumps at the breakpoints and check whether large orders trigger a higher tier. " + DISCL_E,
        "Do refunds affect the amount received?",
        "Refunds usually reduce both commission and the amount received; the platform statement is final and this tool is for estimation. " + DISCL_E,
        "About \"Commission (Platform / Service Fee) Calculation\"",
        "Commission (Platform / Service Fee) Calculation.",
        "Compute commission and proceeds from the rate and cap",
        "Commission estimation for transaction settlement",
        "Comparison of tiered rate jumps",
        "Commission cap estimation for large orders",
        "Comparing commission costs across platforms",
        "Platform",
        "Service fee",
    ]))

    write('conversion-4', build('conversion-4', [
        "\U0001F6CD\uFE0F Livestream (Views / Orders) Conversion",
        "Compute the livestream conversion rate and orders per thousand views from view and order counts.",
        "\U0001F4D6 View the \"Livestream (Views / Orders) Conversion Guide\"",
        "Conversion rate = orders / views",
        "This tool computes view-to-order conversion, orders per thousand views (GPM) and traffic monetisation efficiency from livestream viewers, interactions and orders.",
        "Views",
        "Orders",
        "\U0001F4A1 Conversion rate = orders \u00f7 views \u00d7 100%; orders per thousand views = orders \u00f7 views \u00d7 1000.",
        "\U0001F4DA In-depth Analysis: Livestream (Views / Orders) Conversion",
        "Conversion assessment: enter the view UVs and orders to compute the livestream room's",
        "conversion rate",
        "GPM comparison: enter the order amount and the per-thousand views to compute GPM and compare it across hosts or sessions.",
        "Classroom demo: a low conversion rate with a high order value can still produce a high GPM.",
        "Example: 10000 views and 200 orders gives a 2% conversion rate; 40000 yuan of orders gives GPM = 4000 yuan per thousand views.",
        "What is GPM?",
        "Gross merchandise volume per thousand views \u2014 the core metric for traffic monetisation efficiency. " + DISCL_E,
        "Should I look at conversion or GPM?",
        "Conversion shows how well traffic is captured and GPM how well it is monetised, so use both: high-ticket categories convert lower but may still score a higher GPM. " + DISCL_E,
        "Does interaction affect conversion?",
        "Interaction raises dwell time and trust, indirectly lifting conversion, but the relationship is not linear and depends on the products and the pitch. " + DISCL_E,
        "About \"Livestream (Views / Orders) Conversion\"",
        "Livestream (Views / Orders) Conversion.",
        "Compute conversion rate and GPM from views and orders",
        "Assessing livestream view-to-order conversion",
        "Comparing orders per thousand views (GPM)",
        "Ranking monetisation efficiency by host or session",
        "Observing the relationship between interaction and conversion",
        "Views",
        "Orders",
    ]))

    write('cycle-15', build('cycle-15', [
        "\U0001F52E Repurchase (Cycle / Frequency) Forecast",
        "Record a customer's purchase history, compute the average repurchase cycle and purchase frequency, forecast the next purchase date, and segment customers automatically (one-time / regular / VIP / churned).",
        "\"Record a customer's purchase history, compute the average repurchase cycle and purchase frequency, forecast the next purchase date, and segment customers automatically (one-time / regular / VIP / churned).\" It performs a professional calculation from the input parameters and outputs the result.",
        "\U0001F4D6 View the \"Repurchase (Cycle / Frequency) Forecast Guide\"",
        "Add customer",
        "Customer name / ID",
        "Churn threshold (days)",
        "Customer overview",
        "Close",
        "Purchase records",
        "Add purchase record",
        "Analyze and forecast",
        "\U0001F4DA In-depth Analysis: Repurchase (Cycle / Frequency) Forecast",
        "Repurchase forecasting: enter past purchase dates to get the average interval and predict the next purchase window.",
        "Customer segmentation: segment RFM-style by frequency and recency to identify VIPs and churned customers.",
        "Classroom demo: repurchase rate = repeat customers / total customers.",
        "Example: customer A's three purchases are 30 and 34 days apart, averaging 32 days, so the next repurchase is forecast about 32 days out; more than 90 days without a purchase is flagged as churn.",
        "How is the repurchase rate calculated?",
        "Repeat customers divided by the total customers with a purchase; be careful to remove the bias introduced by one-off necessity purchases. " + DISCL_E,
        "Is the forecast accurate?",
        "It is a statistical forecast based on past intervals and is affected by promotions and seasonality, so treat it as a range rather than an exact date. " + DISCL_E,
        "What about the churn threshold?",
        "Set it from the category's repurchase cycle (for example three times the average cycle without a purchase); the threshold differs by category. " + DISCL_E,
        "Average repurchase cycle = the mean of the intervals between adjacent purchase dates",
        "Forecast next purchase date = last purchase date + average repurchase cycle",
        "Customer segmentation: VIP (\u22655 purchases) / regular (2-4) / one-time (1) / churned (no repurchase beyond the threshold)",
        "Repurchase rate = customers with 2 or more purchases / total customers",
        "About \"Repurchase (Cycle / Frequency) Forecast\"",
        "A tool for analysing and forecasting customer repurchase behaviour. It records purchase history, computes the average repurchase cycle, purchase frequency and repurchase rate, forecasts the next purchase time, and segments customers automatically (VIP / regular / one-time / churned).",
        "Average repurchase cycle and purchase frequency calculation",
        "Next purchase date forecast with confidence",
        "Four segments: VIP / regular / one-time / churned",
        "Purchase timeline visualisation",
        "Repurchase rate and spending statistics",
        "E-commerce customer repurchase analysis",
        "Customer lifecycle management",
        "Timing for precision marketing outreach",
        "Churn warning and win-back",
        "e.g. Customer A or user_001",
    ]))

    write('discount', build('discount', [
        "\U0001F4D0 Promotion (Discount / Threshold / Coupon) Design",
        "Compute the amount paid, the amount saved and the discount level from the list price and discount rate.",
        "\U0001F4D6 View the \"Promotion (Discount / Threshold / Coupon) Design Guide\"",
        "Amount paid = list price \u00d7 (1 \u2212 discount rate)",
        "This tool computes the final price and discount strength from the discount rate, spend thresholds and coupon stacking rules, and supports comparing several schemes.",
        "List price (\u00a5)",
        "Discount rate (%)",
        "\U0001F4A1 Amount paid = list price \u00d7 (1 \u2212 discount rate); discount level = (1 \u2212 discount rate) \u00d7 10; a discount rate above 50% needs a gross margin review.",
        "\U0001F4DA In-depth Analysis: Promotion (Discount / Threshold / Coupon) Design",
        "Final price: enter the list price, discount and threshold offer to get the final price and the amount saved.",
        "Scheme comparison: compare \"spend 300, get 50 off\" with \"15% off\" to see which is better for the customer and cheaper for the store.",
        "Classroom demo: show the order in which coupons stack and the mutual exclusion rules.",
        "Example: list price 400, spend 300 get 50 off, then a further 10% off gives (400\u221250)\u00d70.9=315, saving 85 yuan.",
        "Do threshold offers and percentage discounts stack?",
        "Usually the threshold offer applies first and then the percentage discount; a different order gives a different final price, so the campaign rules decide. " + DISCL_E,
        "How do I compare discount strength?",
        "Use the",
        "discount rate",
        "(1 \u2212 final price / list price) for a uniform comparison, so that \"50 off\" and \"10% off\" are not judged on different bases. " + DISCL_E,
        "Is there a limit on stacking?",
        "Platforms often cap how many coupons can stack and the excess does not apply, so campaigns must state this clearly. " + DISCL_E,
        "About \"Promotion (Discount / Threshold / Coupon) Design\"",
        "Promotion (Discount / Threshold / Coupon) Design.",
        "Compute the final price from stacked discounts, threshold offers and coupons",
        "Comparing final prices for threshold offers and percentage discounts",
        "Estimating the order in which coupons stack",
        "Uniform comparison of campaign discount strength",
        "Balancing profit against discount depth",
        "Discount",
        "Threshold offer",
    ]))


if __name__ == '__main__':
    main()
