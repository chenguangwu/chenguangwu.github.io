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
    write('conversion-funnel', build('conversion-funnel', [
        "Conversion Funnel Analysis",
        "Analyze conversion rates at each stage, visualizing every step's conversion and drop-off",
        "📖 View the Conversion Funnel Analysis Guide",
        "Funnel scenarios",
        "E-commerce shopping",
        "Customer acquisition",
        "Sales closing",
        "Funnel stages",
        "Conversion rate = current stage count ÷ previous stage count; overall conversion = last stage ÷ first stage. Drop-off rate = 1 - conversion rate.",
        "📚 In-depth: Conversion Funnel Analysis",
        "Locate the conversion bottleneck: enter visitor→add-to-cart→order→payment counts per stage and compute each step's",
        "conversion rate",
        "and drop-off rate to find the stage with the largest loss.",
        "Evaluate operational changes: after launching a new page or campaign, compare before/after step conversion rates to quantify improvement.",
        "Compare channel quality: route traffic from different sources into the same funnel and compare retention differences at key steps.",
        "Example: visits 10000 → add-to-cart 3000 → order 1200 → payment 800",
        "Add-to-cart rate = 3000/10000 = 30.00%; order rate = 1200/3000 = 40.00%; payment rate = 800/1200 = 66.67%.\nOverall conversion = payment/visits = 800/10000 = 8.0%. The biggest drop is 'visit→add-to-cart' (70% lost), so prioritize optimizing the landing page and first-screen hook.",
        "Which step should be optimized first?",
        "Prioritize both 'absolute lost count' and 'relative drop-off rate'. Here visit→add-to-cart loses 7,000 (70%), the largest magnitude; although order→payment loses only 33%, payment has high order value, so both deserve scheduling, starting with the largest bottleneck.",
        "What baseline for funnel comparison?",
        "Use a same-window time period or same batch of traffic for A/B comparison to avoid seasonal noise; focus on 'relative conversion rate' rather than absolute counts to prevent misjudging traffic structure changes.",
        "About Conversion Funnel Analysis",
        "Conversion Funnel Analysis - analyzes conversion rates at each stage, visualizing every step's conversion and drop-off in the sales/marketing funnel. Free online tool. Business productivity tool, boosting work efficiency, with data processed locally for privacy.",
    ]))
    write('moving-average', build('moving-average', [
        "Sales Trend Forecast",
        "Moving-average forecasting, supporting Simple Moving Average (SMA), Weighted Moving Average (WMA), and Exponential Smoothing (EMA)",
        "Core formula (by input variable): 2÷(n+1); n×(n+1)÷2; n-1",
        "📖 View the Sales Trend Forecast Guide",
        "Historical sales data (one value per line, in time order)",
        "Moving window N",
        "Simple Moving Average",
        "Weighted Moving Average",
        "Exponential Smoothing",
        "🔮 Forecast",
        "Next-period forecast",
        ": arithmetic mean of the last N periods;",
        ": more weight on recent periods;",
        ": α=2/(N+1), the more recent, the greater the influence. Moving average suits stationary series with no obvious seasonal fluctuation.",
        "📚 In-depth: Sales Trend Forecast (Moving Average)",
        "Smooth short-term fluctuation: use SMA to remove daily/weekly noise and see the sales trend.",
        "Emphasize recent weight: use WMA to give recent periods higher weight, more sensitive to trend reversal.",
        "Apply exponential smoothing: use EMA with smoothing factor α=2/(N+1) recursively, balancing history and latest, suitable for continuous forecasting.",
        "Example: series [100,120,110,130,140], window N=3",
        "SMA(3): period 3 (100+120+110)/3 = 110; period 4 (120+110+130)/3 = 120; period 5 (110+130+140)/3 = 126.67.\nNext-period forecast = recent window mean = (110+130+140)/3 = 126.67.\nWMA(3) weights 1/2/3, period 5 = (110×1+130×2+140×3)/6 = 133.33, more sensitive to recent; EMA smoothing factor α=2/(3+1)=0.5.",
        "How to choose SMA, WMA, EMA?",
        "SMA is smoothest but lags; WMA gives recent higher weight and is more sensitive to turning points; EMA uses α recursively, needs only the previous result, and suits streaming forecasts. Use SMA for noisy data, WMA/EMA for strong trends you want to track closely.",
        "Is a larger window N always better?",
        "Larger N is smoother but lags more and ignores recent data; smaller N is more sensitive but prone to noise. Typically 3-6; for obvious seasonality use the cycle length (e.g. 12).",
        "About Sales Trend Forecast",
        "Sales Trend Forecast - moving-average forecasting, supporting SMA, WMA, and EMA. Free online tool. Business productivity tool, boosting work efficiency, with data processed locally for privacy.",
    ]))
    write('price-calculator', build('price-calculator', [
        "Pricing Calculator",
        "Supports four strategies - cost-plus, target-profit, competitor-reference, and value pricing - outputting suggested price, gross margin, and break-even volume.",
        "Core formula (by input variable): max(0, min(100, r.cost ÷ r.price × 100))",
        "📖 View the Pricing Calculator Guide",
        "Cost-plus",
        "Target profit",
        "Competitor reference",
        "Value pricing",
        "Unit cost (CNY)*",
        "Fixed cost (CNY, optional)",
        "Markup rate (%)",
        "Target profit (CNY)",
        "Expected volume (units)",
        "Competitor price (CNY)",
        "Deviation (%, positive = above competitor, negative = below)",
        "Customer perceived value (CNY)",
        "Value capture rate (%)",
        "Pricing strategy comparison",
        "Pricing strategy reference",
        "Pros and cons",
        "Price = cost × (1 + markup rate)",
        "Manufacturing, retail, stable costs",
        "Simple and easy, but ignores market and customer value",
        "Price = (cost + target profit/volume)",
        "Projects with a clear profit target",
        "Secures profit, but volume forecast must be accurate",
        "Price = competitor price × (1 ± deviation%)",
        "Fierce competition, homogeneous products",
        "Responds to market, but risks price wars",
        "Price = customer value × capture rate",
        "Differentiated products, SaaS, premium services",
        "Large profit margin, but requires quantifying customer value",
        "Break-even volume:",
        "= fixed cost ÷ (price - unit cost). When price ≤ unit cost, volume alone cannot turn a profit.",
        "📚 In-depth: Pricing Calculator",
        "Cost-plus pricing: add a target markup rate on cost to quickly get the suggested price and",
        "Target-profit pricing: given fixed cost, target total profit, and expected volume, reverse-engineer the required unit price.",
        "Competitor/value pricing: multiply competitor price or perceived customer value by deviation/capture rate for differentiated pricing.",
        "Example: cost 80 CNY, markup 25%, monthly fixed cost 2,000 CNY",
        "Price = 80 × (1 + 25%) = 100 CNY; unit gross profit = 100 - 80 = 20 CNY; gross margin = 20/100 = 20.0%.",
        "Break-even",
        "Volume = fixed cost ÷ unit gross profit = 2,000 ÷ 20 = 100 units (must sell 100 to cover fixed cost).\nSwitching to 'target profit' mode with target profit 2,000 and volume 100 gives price = 80 + (2,000+2,000)/100 = 120 CNY.",
        "How to use the four pricing strategies?",
        "Cost-plus is safest; target-profit guarantees payback; competitor-reference suits red oceans; value pricing suits differentiated/high-perceived-value products. Compare suggested price and margin on the same screen.",
        "Where does break-even volume come from?",
        "Break-even volume = monthly fixed cost ÷ unit gross profit. In the example, unit gross profit 20 CNY and fixed 2,000 CNY, so 100 units cover fixed cost; only the excess contributes net profit.",
        "About the Pricing Calculator",
        "The Pricing Calculator is an online tool in sales management. Sales management tools help quantify performance and commission calculation.",
    ]))

if __name__ == '__main__':
    main()
