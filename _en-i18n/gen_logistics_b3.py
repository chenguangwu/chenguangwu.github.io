#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'logistics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'logistics')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {
    'analysis-75': {
        "品控（流程/标准/检测）机制 - 生鲜商品品质评估工具，输入外观、气味":
            "Quality control (process / standard / inspection) mechanism - a fresh produce quality assessment tool that takes appearance, odor",
    },
    'analysis-76': {
        "品控（流程/标准/检测）机制 - 生鲜商品品质评估工具，输入外观、气味":
            "Quality control (process / standard / inspection) mechanism - a fresh produce quality assessment tool that takes appearance, odor",
    },
}

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
    out = {'slug': slug, 'industry': 'logistics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('analysis-75', build('analysis-75', [
        "📉 Loss (Control / Prevention) Analysis by Category",
        "Enter inbound volume, loss volume and unit price by category to compute the loss rate, loss amount and the key loss sources.",
        "Loss management should look at both the rate and the amount: the loss rate measures how well loss is controlled and suits horizontal benchmarking, while the loss amount measures actual loss and sets remediation priority — a low-price category may have a high rate but limited amount, while a high-price category may be the biggest bleed even at a low rate. The overall loss rate is computed on the aggregate basis (Σloss ÷ Σinbound) so small-volume categories do not inflate the average. The tool also reports the item with the highest loss rate and the item with the highest loss amount, and sorts the table by amount descending. All computation happens locally in the browser and no data is uploaded.",
        "Loss (control / prevention / analysis) system",
        "/ Loss (control / prevention / analysis) system",
        "📖 Read the Fresh Produce Loss Descriptive Statistics user guide",
        "Single-item loss rate = loss volume ÷ inbound volume × 100%; single-item loss amount = loss volume × unit price; overall loss rate = Σloss volume ÷ Σinbound volume × 100%",
        "Enter \"category,inbound volume,loss volume,unit price\" per line, e.g. Fresh produce,1000,60,25",
        "Fresh produce,1000,60,25\nGeneral merchandise,2000,30,18\nCold chain,800,45,40",
        "📚 Deep dive: Loss Control Analysis by Category",
        "Monthly loss statistics for warehouses / stores",
        "Loss remediation priority ranking",
        "Category loss benchmarking and assessment",
        "Single-item loss rate = loss volume ÷ inbound volume × 100%; single-item loss amount = loss volume × unit price; overall loss rate = Σloss volume ÷ Σinbound volume × 100%.",
        "Produce 1200/90/12, meat 600/42/38, dry goods 1500/15/20 → inbound total 3300, loss total 147, overall loss rate = 147/3300 = 4.45%; loss amount 1080 + 1596 + 300 = 2976 CNY; the highest loss rate item is produce (7.50%), the highest loss amount item is meat (1596 CNY).",
        "Should I look at the loss rate or the loss amount?",
        "Both: the rate is used for horizontal benchmarking of control level, the amount for setting remediation priority. High-price categories are often the bulk of the amount even when the rate is not high.",
        "Why isn't the overall loss rate the average of each category?",
        "It is computed on the aggregate basis (Σloss ÷ Σinbound), which avoids inflating the average with the high loss rate of small-volume categories and stays closer to the real proportion of loss.",
        "Competition (analysis / strategy / differentiation)",
        "Quality control (process / standard / inspection) mechanism - a fresh produce quality assessment tool that takes appearance, odor",
        "About \"Loss (control / prevention / analysis) system\"",
        "Loss (control / prevention / analysis) system. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
        "e.g. Fresh produce,1000,60,25",
    ]))
    write('analysis-76', build('analysis-76', [
        "⚖️ Competition (Analysis / Strategy / Differentiation)",
        "Analysis / strategy / differentiation",
        "Competition (analysis / strategy / differentiation)",
        "/ Competition (analysis / strategy / differentiation)",
        "📖 Read the Competitor Price Descriptive Statistics user guide",
        "Normalize the range of each carrier's transit time, price and damage rate, then weight them (transit time 0.4 / price 0.3 / damage rate 0.3) to get a composite score and ranking, and combine the weak spots to give a differentiated position and improvement suggestions.",
        "Enter metrics for each carrier (one line per carrier: carrier,transit days,price,damage rate %,covered cities)",
        "Shunda,2,12,0.8,320\nYunyun,3,9,1.5,180\nAnjie,1,18,0.3,90",
        "📚 Deep dive: Competitor Price Descriptive Statistics",
        "Pricing benchmarking: enter the final delivered prices of N competitors in the same category, compute the mean and",
        "determine where your own price sits relative to them (high / middle / low).",
        "Price spread assessment: use the range and",
        "to look at competitor price dispersion; small dispersion means a price war is intense, large dispersion means there is room for tiered positioning.",
        "Promotion monitoring: enter competitor prices periodically to form a series and track mean drift to judge whether a rival has entered a price-cut cycle.",
        "Enter a numeric series separated by commas, spaces or newlines; outputs the count, sum, mean, median, minimum, maximum, range, variance and standard deviation. Mean = Σx/n; median = the middle value after sorting; variance = Σ(x−mean)²/n; standard deviation = √variance.",
        "Enter 5 competitor delivered prices: 12.5, 11.0, 13.2, 10.8, 12.0 (CNY). Count 5; sum 59.5; mean 11.9 CNY; median 12.0 CNY; range 13.2−10.8=2.4 CNY; variance 0.816; standard deviation 0.903 CNY. If your own price is 12.0 CNY, it sits exactly at the median, a middle position; the small competitor dispersion (σ<1) means a tight price band and limited room for differentiation.",
        "How many samples are needed to be meaningful?",
        "At least 5 to 10 samples on the same basis are needed to estimate the mean and standard deviation reliably; with too few samples the standard deviation is unreliable, so broaden competitor coverage or split by channel.",
        "Is a small standard deviation always good?",
        "For the buyer, small dispersion means transparent comparison and little room for a premium; for the seller it signals a price war. Decide based on volume and margin rather than dispersion alone.",
        "Loss (control / prevention / analysis) system",
        "Quality control (process / standard / inspection) mechanism - a fresh produce quality assessment tool that takes appearance, odor",
        "About \"Competition (analysis / strategy / differentiation)\"",
        "Competition (analysis / strategy / differentiation). Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
        "Shunda,2,12,0.8,320\nYunyun,3,9,1.5,180\nAnjie,1,18,0.3,90",
    ]))
    write('analysis-cycle-1', build('analysis-cycle-1', [
        "🏬 Cycle Count Variance Analysis (Book vs Physical)",
        "Enter the book quantity and counted quantity of each item line by line to compute the variance, variance rate and count accuracy.",
        "Cycle counting samples batches on a schedule, and the core metric is not total variance but count accuracy: total variance gets distorted because gains and losses offset each other, so dividing the sum of absolute variances by the total book quantity is what truly reflects how well books match physical stock. A positive variance is a gain (physical more than book), a negative variance is a loss. The tool also reports the item with the largest variance and the counts of gain and loss items, so you can sort by variance rate to arrange review and accountability. Data is computed only in your local browser and never uploaded.",
        "/ Stocktake (cycle / circulation / variance) analysis",
        "Variance = counted quantity − book quantity; variance rate = variance ÷ book quantity × 100%; count accuracy =(1 − Σ|variance| ÷ Σbook quantity)× 100%",
        "Enter \"material code,book quantity,counted quantity\" per line, e.g. A-001,100,97",
        "📚 Deep dive: Cycle Count Variance Analysis",
        "Cycle count book vs physical reconciliation",
        "Count accuracy assessment",
        "Review and accountability for gains and losses",
        "Variance = counted quantity − book quantity; variance rate = variance ÷ book quantity × 100%; count accuracy =(1 − Σ|variance| ÷ Σbook quantity)× 100%.",
        "M-01 500/485, M-02 320/320, M-03 150/168 → book total 970, counted total 973, total variance +3, sum of absolute variances 33, count accuracy = (1 − 33 ÷ 970)× 100% = 96.60%; the largest variance is M-03 (+18), with 1 gain item and 1 loss item.",
        "Does a total variance near 0 mean the count is accurate?",
        "No. Gains and losses offset each other, so you should judge by count accuracy, which is computed from the sum of absolute variances.",
        "At what accuracy level should a review be triggered?",
        "Warehouse management commonly uses 95%–98% as the assessment line; items below that line or with an absolute variance rate above 2% should be reviewed first.",
        "About \"Stocktake (cycle / circulation / variance) analysis\"",
        "Stocktake (cycle / circulation / variance) analysis. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
        "e.g. A-001,100,97",
    ]))
    write('analysis-report', build('analysis-report', [
        "📈 Finance (Profitability / Cash Flow / Statements) Analysis",
        "Profitability / cash flow / statements",
        "/ Finance (Profitability / Cash Flow / Statements) Analysis",
        "Net for each category = inflow for that category − outflow for that category; net cash flow = operating net + investing net + financing net.",
        "Cross-check: total inflow − total outflow should equal net cash flow; if they differ, a classification or sign is wrong.",
        "Look at operating net for health: only a positive operating net together with positive net cash flow is sustainable; covering an operating shortfall through financing needs a warning.",
        "Cash flow detail (one line per \"category,item,amount\", category is Operating/Investing/Financing, enter outflow as a negative number)",
        "Operating,sales collections,200000\nOperating,purchase payments,-120000\nOperating,labor expense,-30000\nInvesting,equipment purchase,-80000\nInvesting,asset disposal income,10000\nFinancing,bank loan,50000\nFinancing,interest payment,-10000",
        "Cash flow analysis",
        "📚 Deep dive: Cash Flow Structure and Net Amount Analysis",
        "Monthly cash flow review",
        "Structural analysis of cash flow across the three activity types",
        "Funding gap early warning",
        "Net for each category = inflow for that category − outflow for that category; net cash flow = operating net + investing net + financing net; total inflow − total outflow = net cash flow.",
        "Operating +120000, Investing −120000, Financing +120000 → net cash flow 120000.00, total inflow 730000.00, total outflow 610000.00, each of the three net amounts accounting for 33.33% in absolute share.",
        "Why is funding still tight when net cash flow is positive?",
        "If the operating net is negative and loans are used to cover it, positive net flow is not sustainable; focus on operating net and the schedule of maturing debt.",
        "Should outflows be negative or positive numbers?",
        "The tool requires outflows as negative numbers so sums and cross-checks work directly; you may also enter positive numbers and mark the direction in the item name.",
        "About \"Finance (Profitability / Cash Flow / Statements) Analysis\"",
        "Finance (profitability / cash flow / statements) analysis. Free online tool, pure front-end processing, data is not uploaded, privacy and security protected.",
        "Operating,sales collections,500000",
    ]))
    write('express-freight-calc', build('express-freight-calc', [
        "🚚 Express Freight Cost Calculator",
        "Estimate freight from first weight, additional weight and volumetric weight.",
        "/ Express Freight Cost Calculator",
        "Chargeable weight = max(actual weight, volumetric weight), volumetric ratio = volumetric weight ÷ actual weight; when it exceeds 1 billing uses volumetric weight; volumetric weight (kg) = length (cm) × width (cm) × height (cm) ÷ volumetric divisor (6000 is common for road freight, 5000 for air, 8000 for express); freight = first weight fee + (chargeable weight − first weight) × additional weight unit price (a fraction of 1 kg counts as 1 kg); total cost additionally includes insured value fee and remote area surcharge.",
        "First weight (kg)",
        "First weight freight (CNY)",
        "Additional weight unit price (CNY/kg)",
        "Actual weight (kg)",
        "Volumetric weight (kg)",
        "Compute freight",
        "📚 Deep dive: Express Freight (First Weight + Additional Weight) Calculation",
        "Before shipping, estimate freight by taking the larger of actual weight and volumetric weight, then compare prices across carriers.",
        "Work out the store's free-shipping cost: enter the first weight price and additional weight price for common destinations and batch-estimate order freight.",
        "Decide whether packaging needs to be compressed — compare volumetric weight before and after compression to see directly how much freight drops.",
        "Freight for a 2.4 kg parcel",
        "First weight 1 kg / first weight freight 12 CNY / additional weight 5 CNY per kg. A 30×20×15 cm package gives volumetric weight 1.5 kg via ÷6000; actual weight 2.4 kg is larger, so the chargeable weight is 2.4 kg. Excess over first weight = 2.4 − 1 = 1.4 kg, freight = 12 + 1.4 × 5 = 19.00 CNY. Switching to a 40×30×30 cm box (volumetric weight 6.0 kg) raises the chargeable weight to 6.0 kg, freight = 12 + 5 × 5 = 37.00 CNY, nearly double.",
        "How is volumetric weight computed?",
        "The common formula is length × width × height (cm) ÷ volumetric divisor, where the divisor is often 6000 or 8000 for domestic express and 5000 for international express. The tool lets you enter volumetric weight directly, so you can first compute it with the",
        "and then fill it in.",
        "Why is billing based on volumetric weight rather than actual weight?",
        "Light bulky goods take up carriage space but weigh little, so billing by actual weight would leave the carrier short of capacity. Taking the larger of actual and volumetric weight as the chargeable weight is standard industry practice.",
    ]))

if __name__ == '__main__':
    main()