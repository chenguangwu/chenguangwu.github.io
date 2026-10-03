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
    write('sales-forecast', build('sales-forecast', [
        "Sales Forecast",
        "Forecasts future sales from historical monthly data using moving average, weighted moving average, linear regression, or seasonal methods.",
        "Forecasts future sales from historical monthly data using moving average, weighted moving average, linear regression, or seasonal methods, and computes and outputs results from the input parameters.",
        "📖 View the Sales Forecast Guide",
        "Historical sales data (one value per line, in time order, at least 3 periods)",
        "Linear regression",
        "Seasonal (YoY/MoM)",
        "Moving average periods N",
        "Clear saved",
        "Forecast visualization",
        "Historical data",
        "Forecast data",
        "Trend line",
        "Forecast method notes",
        "Use the arithmetic mean of the last N periods as the next-period forecast",
        "Stationary data, no obvious trend/season",
        "Higher weight on recent periods (weights N,N-1,...,1)",
        "Recent data is more representative",
        "Least-squares fit y = a·x + b",
        "Obvious linear trend exists",
        "Seasonal",
        "Extrapolate by same-period growth rate (needs at least one cycle)",
        "Has periodic fluctuation (e.g. seasonality)",
        "Confidence interval:",
        "Approximate 95% confidence interval from historical residual standard deviation (forecast ± 1.96σ). For reference only; actual forecast error is affected by many factors.",
        "📚 In-depth: Sales Forecast",
        "Moving-average forecast: extrapolate from the mean of the last N periods, suitable for stationary series with no strong trend.",
        "Forecast: fit the historical trend line y=a+bx and extrapolate, suitable for sustained growth/decline series.",
        "Seasonal forecast: extrapolate by cycle-length YoY/MoM growth rate, suitable for monthly/quarterly strongly cyclical business.",
        "Example: series [100,120,110,130,140], moving average N=3 forecasting 2 periods",
        "Period 1 forecast = mean of last 3 (110+130+140)/3 = 126.67; add it to the series then forecast period 2 = (130+140+126.67)/3 ≈ 132.22.\nWith linear regression, fit the trend then extrapolate periods 6 and 7 (x=6,7), better for monotonic trends; the seasonal pattern extrapolates by the 'same period last year → this year' growth rate.",
        "How to choose among the four forecast methods?",
        "Use MA/WMA for stationary series; linear regression for obvious linear trends; seasonal for strong cycles (e.g. Double 11, summer); EMA for streaming updates. No method is absolutely better; compare several and look at",
        "How to interpret the confidence interval?",
        "The tool uses historical",
        "σ to give a ±1.96σ interval, meaning about 95% probability falls in this range. The larger σ and the more volatile history, the wider the interval and the less reliable the forecast; judge with business context.",
        "About Sales Forecast",
        "Sales Forecast is an online tool in sales management. Sales management tools help quantify performance and commission calculation.",
        "Example:\n120000\n135000\n150000\n142000\n168000",
    ]))
    write('stacked-discount', build('stacked-discount', [
        "Stacked Discount Calculator",
        "Applied top to bottom in order; stacking is not simply adding the discount rates.",
        "📖 View the Stacked Discount Calculator Guide",
        "Coupon: current price → current price ×(discount÷100); threshold coupon: once the threshold is met, current price - fixed amount",
        "Final price after multiple stacked discounts, supporting coupon and threshold-coupon combinations",
        "Stack discounts",
        "+ discount",
        "+ threshold coupon",
        "Final price",
        "Stacking order: applied top to bottom. Coupon = current price × discount; threshold coupon = subtract fixed amount once threshold met. Stacking is not simply adding discount rates.",
        "📚 In-depth: Stacked Discount Calculator",
        "Design promotional stacking: combine coupons (by percentage) and threshold coupons (amount off at threshold), computing the final price in the set order.",
        "Compare stacking order: verify the difference between 'discount then threshold' and 'threshold then discount' to prevent over-discounting.",
        "Measure actual discount depth: derive the equivalent",
        "discount rate",
        "(effective discount), for external promotional wording.",
        "Example: original price 500 CNY, first 20% off then 300-50 threshold",
        "Layer 1 20% off: 500 × 80% = 400 CNY; Layer 2 300-50 threshold (400≥300 hit): 400 - 50 = 350 CNY.\nFinal price 350 CNY, total saved 150 CNY (equivalent to 30% off the original; the tool shows 'save 30%' as the discount share). If reversed to threshold then discount: 500-50=450 then 20% off = 360 CNY; order changes the result.",
        "Does stacking order affect the final price?",
        "Yes. When percentage discount and threshold coupon combine, 'percentage first then threshold' is usually better (threshold easier to hit); 'threshold first then percentage' also discounts the threshold amount. Define the order and measure cost when designing campaigns.",
        "What if the threshold is not met?",
        "If the current price is below the threshold, that layer does not apply (shows 'threshold not met'), and only previously applied discounts accumulate. You can adjust the threshold or order in the config.",
        "About the Stacked Discount Calculator",
        "Stacked Discount Calculator - final price after multiple stacked discounts, supporting threshold-coupon and discount combinations. Free online sales tool. Business productivity tool, boosting work efficiency, with data processed locally for privacy.",
    ]))
    write('target-breakdown', build('target-breakdown', [
        "Sales Target Breakdown",
        "Break down team targets bottom-up, supporting weighted or equal split",
        "📖 View the Sales Target Breakdown Guide",
        "Individual target = total target × (individual weight ÷ total weight)",
        "Team total target",
        "Breakdown method",
        "By weight",
        "single",
        "Team members",
        "+ add member",
        "📈 Re-breakdown",
        "Weighted mode: individual target = total target × (individual weight ÷ total weight). Weights can be set by historical performance, customer resources, or rank.",
        "📚 In-depth: Sales Target Breakdown",
        "Weighted breakdown: allocate annual/quarterly total targets by region, person, or channel weight (e.g. historical share, capacity).",
        "Equal breakdown: when members have equal weight, split evenly, simple and transparent.",
        "Verify totals match: the post-breakdown sum should equal the total target, used for plan review and accountability.",
        "Example: annual target 1,000,000 CNY, 4 people weights 30/25/20/25",
        "Total weight 100. Zhang San = 1,000,000 × 30/100 = 300,000 CNY; Li Si = 250,000; Wang Wu = 200,000; Zhao Liu = 250,000.\nSum = 30+25+20+25 = 1,000,000 CNY, matching the total. If a member's weight is 0 or negative, the tool normalizes by the remaining weight to avoid allocation errors.",
        "How to choose weighted vs equal breakdown?",
        "Use weight when members differ greatly in ability/resources (e.g. by historical share); use equal when evenly matched or fairness is emphasized. Total weight is best = 100 for easy checking; if not 100, the tool normalizes by actual share.",
        "What if the post-breakdown sum does not match the total?",
        "First check whether the weight total is as expected and whether any member was missed. In weighted mode the tool uses (individual weight ÷ total weight) × total target; as long as total weight > 0 and the total target is correct, the sum must equal the total.",
        "About Sales Target Breakdown",
        "Sales Target Breakdown - breaks down team targets bottom-up by member weight or equal split. Free online management tool. Business productivity tool, boosting work efficiency, with data processed locally for privacy.",
    ]))

if __name__ == '__main__':
    main()
