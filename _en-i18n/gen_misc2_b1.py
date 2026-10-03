#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'misc2')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'misc2')
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
    out = {'slug': slug, 'industry': 'misc2', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('car-residual', build('car-residual', [
        "🧮 Used Car Residual Value Calculator",
        "Enter the new-car purchase price and years of use to estimate the used car's residual value",
        "Core formulas (by input variables): max(price - dep, price × 0.05); max(price - dep, salvageVal); (1 - residual ÷ price) × 100",
        "Used Car Residual Value Calculation",
        "/ Used Car Residual Value Calculation",
        "54321 Depreciation Method (first 5 years step-down)",
        "New Car Purchase Price (CNY)",
        "Depreciation Period (years)",
        "Residual Rate (%)",
        "📐 Depreciation Method Notes",
        "54321 Depreciation Method",
        "In the first 5 years depreciation is 15%, 12%, 10%, 8%, 6% respectively (total 51%); after year 5 about 5% per year. Commonly used for quick valuation of family cars.",
        "Annual depreciation = (original value − residual) ÷ depreciation period; depreciation is even, suitable for stable valuation.",
        "Annual depreciation rate = 2 ÷ depreciation period; faster early and slower later, closer to the real depreciation curve of a new car.",
        "The estimate is for reference only; the actual transaction price is affected by many factors such as vehicle condition, mileage, brand, and regional market.",
        "📚 In-Depth Analysis: Used Car Residual Value Calculator",
        "Before selling, estimate a car's current residual value, comparing the 54321 step-down, straight-line,",
        "double declining balance",
        "three methods",
        "result differences.",
        "Provide a residual-value baseline when assessing loans or insurance claims, helping judge payout amounts and trade-in subsidies.",
        "When buying, compare the residual-value decay speed of the same model at different ages to assess long-term ownership cost.",
        "Example: \"purchase price 200,000 CNY, age 5 years, 54321 step-down depreciation\"",
        "First 5 years depreciation rates are 15%/12%/10%/8%/6% respectively, cumulative 51%; from year 6 about 5% per year, with residual not below the 5% floor of the original value. Cumulative depreciation = 200,000 × 51% = 102,000, estimated residual = 200,000 − 102,000 = 98,000, cumulative depreciation rate 51%. If the age is only 3.5 years: first 3 years 37% + year 4 8% × 0.5 = 4% → cumulative 41%, residual about 118,000. If double declining balance is chosen (life 10 years, annual rate 20%): depreciation is faster early, early residual is lower but flattens later.",
        "What does 54321 step-down depreciation mean?",
        "Rule of thumb: \"year 1 15%, year 2 12%, year 3 10%, year 4 8%, year 5 6%\", total 51%, then about 5% per year; it reflects the real depreciation curve that is high early and low later, closer to the actual family car than the straight-line method. Residual is set at a 5% floor of original value to prevent zeroing.",
        "How does double declining balance differ from straight-line?",
        "Straight-line fixes the annual depreciation ((original − residual)/life), with higher early residual; double declining balance depreciates faster early (annual rate = 2/life) and switches to straight-line later, favoring accelerated depreciation scenarios (e.g. corporate tax). The tool gives three results; choose by use case.",
        "About \"Used Car Residual Value Calculation\"",
        "The used car residual value calculator provides three common depreciation methods to help you quickly estimate the remaining value of a vehicle after several years of use, offering a reference for buying and selling decisions.",
        "Supports 54321, straight-line, and double declining balance depreciation methods",
        "Customizable depreciation period and residual rate",
        "Automatically calculates cumulative depreciation rate and residual amount",
        "Used Car Residual Value Calculator. Travel tools, essential for trips, supports offline use.",
    ]))
    write('cigarette-tar', build('cigarette-tar', [
        "🫁 Nicotine and Tar Conversion",
        "Based on the tar/nicotine amount stated on cigarettes and smoking volume, estimate daily intake and exposure risk",
        "Daily tar intake = tar per cigarette (mg) × cigarettes per day; daily nicotine intake = nicotine per cigarette (mg) × cigarettes per day; relative exposure multiple can be approximated as cigarettes per day ÷ 20 × 1.5 (a 20-cigarette daily smoker's lung cancer risk is about 10 times that of a non-smoker); low-tar cigarettes are usually labeled under 8 mg/cigarette, but inhalation depth and method significantly change actual intake.",
        "Tar Content (mg/cigarette)",
        "Nicotine Content (mg/cigarette)",
        "Cigarettes per Day",
        "📊 Tar Grading Reference",
        "Health warning: smoking is harmful to health and can cause lung cancer, cardiovascular disease, and other illnesses. This tool is for risk reference only and does not constitute medical advice. Quitting smoking can significantly reduce health risks.",
        "📚 In-Depth Analysis: Nicotine and Tar Conversion",
        "Smokers quantify total daily tar/nicotine intake (mg/day) to see the smoking burden clearly.",
        "Compare long-term cumulative exposure (grams per month/year) of low/medium/high tar cigarettes.",
        "Track the decline in intake when quitting or cutting down, as a health-awareness reference.",
        "Example: \"tar 10 mg/cigarette, nicotine 1 mg/cigarette, 20 cigarettes per day\"",
        "Daily tar = 10 × 20 = 200 mg, nicotine = 1 × 20 = 20 mg; monthly tar = 200 × 30 = 6,000 mg (about 6 g), yearly = 200 × 365 = 73,000 mg (about 73 g); at about 25% actual inhalation rate, estimated true daily inhaled tar ≈ 50 mg. Tar grading: ≤5 mg/cigarette very low, ≤8 mg low, ≤12 mg medium, higher is high — in this example 10 mg is medium tar.",
        "Why multiply by 25% when calculating inhaled tar?",
        "Tar from burning cigarettes does not all enter the lungs; literature estimates actual inhalation at about 15%–30%, and the tool takes the median 25% as a conservative estimate of actual inhalation; this only reflects the exposure magnitude and does not represent a safe threshold.",
        "Which deserves more attention, tar or nicotine?",
        "Tar contains multiple carcinogens and is the main source of harm, while nicotine is mainly addictive. Lower tar does not mean harmless (deeper inhalation may compensate); the most reliable health benefit comes from reducing or quitting. This tool is for quantitative reference only and does not constitute medical advice.",
        "About \"Nicotine and Tar Conversion\"",
        "This tool estimates cumulative intake based on the tar and nicotine content labeled on cigarette packaging combined with daily smoking volume, helping understand smoking exposure risk. Smoking is harmful to health; this tool is for risk reference only.",
        "Calculate cumulative daily/monthly/yearly tar intake",
        "Estimate nicotine intake",
        "Tar Grading Reference",
        "Nicotine and Tar Converter - enter tar and nicotine amounts and number of cigarettes to estimate daily intake and equivalent exposure risk, smoking harm reference. Health metric calculation tool, based on authoritative medical standards, data processed locally to protect privacy.",
    ]))
    write('coin-grade', build('coin-grade', [
        "🪙 Commemorative Coin Grade Reference",
        "Coin grade rating chart: enter a grade to view detailed wear descriptions and collecting advice",
        "The Sheldon 70-point scale grades condition by wear: MS60 to MS70 Uncirculated (above MS65 called Gem grade), AU50 to AU58 About Uncirculated, XF40 to XF45 Extremely Fine, VF20 to VF35 Very Fine, F12 to F15 Fine, VG8 to VG10 Very Good, G4 to G6 Good, below AG3 About Good; for the same coin, each grade step up can differ in market value by 20% to 100%.",
        "Select Grade",
        "UNC - Uncirculated",
        "AU - About Uncirculated",
        "XF - Extremely Fine",
        "VF - Very Fine",
        "F - Fine",
        "VG - Very Good",
        "G - Good",
        "AG - About Good",
        "📋 Grade Rating Chart",
        "Tip: professional grading companies (such as NGC, PCGS) use a 70-point scale, with 70 being flawless. This table is a simplified international Sheldon grading reference.",
        "📚 In-Depth Analysis: Commemorative Coin Grade Reference",
        "Coin collectors use the Sheldon scale (Sheldon 1–70) to compare coin-surface wear and quickly determine the grade.",
        "Use a unified grading language before buying or selling to avoid price gaps from ambiguous condition descriptions.",
        "Assess a coin's collectible value-retention space and decide on graded encapsulation or raw coin holding.",
        "Example: \"About Uncirculated AU grade\"",
        "Code AU, score range AU50–AU58, wear characteristics: \"only the highest points of the coin surface (hairlines, drapery) show extremely slight wear, most luster retained\". Collecting advice: excellent grade, suitable for mid-to-high-end collecting. If it further reaches Uncirculated UNC (MS60–MS70), collection value is highest and professional encapsulation is recommended; if it drops to Very Fine VF (VF20–35), it suits ordinary handling.",
        "How do you read the Sheldon 1–70 scale?",
        "The larger the number, the better the condition: AG3→G4-6→VG8-10→F12-15→VF20-35→XF40-45→AU50-58→MS60-70. MS is Mint State (uncirculated); the closer to 70, the closer to factory-perfect.",
        "How does condition affect value?",
        "For the same coin, the price gap between uncirculated and circulated can be several times or even dozens of times; high-point wear, scratches, and stains all significantly lower the grade and price. High-value coins should be sent to authoritative graders like NGC/PCGS for encapsulation; low-value coins can be judged by eye against this table.",
        "About \"Commemorative Coin Grade Reference\"",
        "The commemorative coin grade reference table collects internationally used coin grade levels (Sheldon scale) to help collectors quickly understand the wear characteristics and collectible value of each grade.",
        "Full grade coverage from UNC to AG",
        "Detailed wear characteristic descriptions",
        "Provides collecting advice",
        "Commemorative Coin Grade Reference - coin grade rating chart, UNC/AU/XF/VF/F and other grade explanations, commemorative coin collecting grade rating reference. Daily life tools, close to life, practical and convenient.",
    ]))
    write('index', build('index', [
        "🛠️ Life Miscellaneous Tools",
        "Life Miscellaneous",
        "Life Miscellaneous Tools",
        "Screen Size Calculation",
        "The screen size calculator computes PPI pixel density from resolution width/height and diagonal inches, and converts actual display size, suitable for evaluating clarity when choosing monitors, phones, and projectors.",
        "Used Car Residual Value Calculation",
        "Enter the new-car purchase price and years of use, and estimate the used car's residual value by a curve that depreciates 15%, 12%, 10%, 8%, 6% in the first 5 years respectively, then about 5% per year thereafter. Used for quick family-car valuation, trade-in reference, and residual prediction.",
        "Express Insurance Fee Calculation",
        "The express insurance fee calculator estimates insurance cost from declared value and courier rates, supports comparing multiple couriers, and suits pre-shipping cost estimation and valuable-item protection decisions.",
        "Enter the tar/nicotine content labeled on cigarettes and daily cigarette count to estimate total daily tar and nicotine intake and relative exposure risk. Used for smokers to understand smoking burden; results are for health-awareness reference only.",
        "Lists shoe-size conversions for brands and countries (EU, US, UK, cm); enter a known size to look up the corresponding size, convenient for online shopping, pure front-end lookup.",
        "Enter overseas shopping amount, destination country tax rate, and live exchange rate to estimate the refundable tax and actual spending after refund. Used to estimate refund benefits and compare destinations before outbound shopping trips.",
        "Instrument Tuning Frequency Reference",
        "Generates a standard frequency reference table for each note name based on equal temperament, with default reference A4=440 Hz and support for custom reference pitch, for quick lookup in instrument tuning, choir pitch-setting, and acoustics teaching.",
        "Select or enter a coin grade (Sheldon scale 1–70) to view the corresponding wear description, scoring points, and collectible value-retention advice. Used by coin collectors to quickly compare grades and assess coin value.",
        "Look up the length/width/height and capacity specs of popular 18–30 inch luggage, and compare carry-on and checked baggage size/weight limits across airlines. Used to choose compliant luggage before travel and avoid boarding issues.",
        "About \"Life Miscellaneous Tools\"",
        "The Life Miscellaneous Tools collection includes 9 free online tools covering common calculation, conversion, and lookup needs in miscellaneous life scenarios. Whether you are a professional, student, or ordinary user in the field, you can find ready-to-use small tools here. All tools run purely front-end, data is not uploaded to servers, protecting privacy and security.",
        "The life miscellaneous tools on this page include (representative tools):",
        "These tools help you quickly complete common tasks related to miscellaneous life needs, without memorizing complex formulas or manual conversion; just input to get results.",
        "Do the life miscellaneous tools need to be downloaded or registered?",
        "No. All life miscellaneous tools on this page are pure front-end online tools; open the page to use them directly, no software installation, no account registration, and no data upload.",
        "Are the calculation results of the life miscellaneous tools accurate? Is the data safe?",
        "The tools compute locally in your browser based on public math formulas and general industry standards, with instant results. All calculations are completed locally on your device; data is not uploaded to servers, ensuring privacy and security.",
    ]))
if __name__ == '__main__':
    main()
