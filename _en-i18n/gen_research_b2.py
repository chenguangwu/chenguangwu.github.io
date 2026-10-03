#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'research')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'research')
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
    out = {'slug': slug, 'industry': 'research', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('analysis-52', build('analysis-52', [
        '📊 Focus Group (Moderation / Analysis) Techniques',
        'Group / moderation / analysis',
        '📖 View the User Guide for Focus Group (Moderation / Analysis) Techniques',
        'Mention ratio = mention count of that code ÷ total mention count × 100%',
        'Weighted score = Σ(mention count × rating) ÷ Σ mention count',
        'Coding sheet (each row: code name, mention count, rating 1–5)',
        'Price sensitivity,12,4\nTaste preference,9,5\nBrand awareness,7,3\nPurchase channel,5,2\nAfter-sales concern,3,4',
        'Statistics coding',
        '📚 Deep Dive: Focus Group Code Frequency and Rating Statistics',
        'After the discussion, enter the organized coding sheet row by row; the three columns "code name, mention count, rating" are entered at once, directly yielding each theme mention ratio.',
        'Use CR3 (sum of top three mention ratios) to judge whether opinions are concentrated: a high value means a few dominant topics occupied most of the discussion.',
        'Combine rating with mention count: themes mentioned often but rated low are usually common pains that are not severe, while those mentioned little but rated high may be key minorities.',
        'Dominant themes and concentration',
        'Enter "Price sensitivity,12,4" "Taste preference,9,5" "Brand awareness,7,3" "Purchase channel,5,2" "After-sales concern,3,4"; total mentions 36. Price sensitivity 33.3%, taste preference 25.0%, brand awareness 19.4%, CR3 = 77.8%, indicating the discussion is highly concentrated on the top three themes, usable as the top-level categories of the codebook.',
        'Why do the mean and weighted mean differ',
        'The arithmetic mean of the five ratings is 3.60, while the mention-weighted mean is 3.78. The difference comes from "taste preference" being mentioned 9 times and rated 5: it appeared a lot in discussion and deserves more weight after weighting. If the gap is obvious, use the weighted value as the decision basis and state the standard.',
        'Themes appearing only among a few',
        'A theme mentioned only 2 times but rated 5, with a mere 5.6% share, ranks last. Such "low-frequency high-rating" cases should not be ignored directly:',
        'In a small focus group, it may represent a latent need not yet recognized by most, worth verifying separately in follow-up surveys.',
        'Can the tool do qualitative coding for me?',
        'No. It only does statistics after you finish open coding and organize themes into "code name + mention count + rating". Axial coding, theme distillation and theoretical saturation judgment still require manual work.',
        'What are the entry format requirements?',
        'One per row, separated by comma, enumeration comma, semicolon or space; at least the code name and mention count two columns, the third is rating (suggest 1–5). Rows missing mention count are skipped with a note in the result, not counted as 0 to mix into statistics.',
        'With few participants, are the statistics meaningful?',
        'Focus groups usually have only 8–12 people, so the mean representativeness is limited. It is suggested to focus on mention-count ranking, ratio and CR3, treating the results as organizing clues and hypothesis sources for follow-up surveys, rather than directly generalizable conclusions.',
        'About the Focus Group (Moderation / Analysis) Techniques',
        'Focus Group (Moderation / Analysis) Techniques. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
        'E.g.: Price sensitivity,12,4',
    ]))
    write('analysis-54', build('analysis-54', [
        '📊 Qualitative (Research / Method / Analysis) Path',
        'Research / method / analysis',
        '📖 View the User Guide for Qualitative (Research / Method / Analysis) Path',
        'The qualitative research path tool helps systematic coding and theme distillation of interview/observation materials:',
        'The first field of each row is the material text, followed by comma-separated theme tags; count each theme frequency, coverage = coded entries ÷ total entries, stability judged by appearing ≥3 times.',
        'Saturation hint: when several consecutive entries (default 5) show no new theme, it hints sampling can stop. This tool only does frequency and coverage statistics; theme distillation still requires the researcher to judge with context.',
        'Material entries (each row: material text, theme1, theme2, …; comma-separated, first is text, rest are themes)',
        'Interview1,Price sensitivity,Insufficient service\nInterview2,Price sensitivity,Inconvenient transport\nObserve3,Insufficient service,Good environment\nInterview4,Price sensitivity,Good environment\nObserve5,Inconvenient transport,Insufficient service',
        'Start calculation',
        '📚 Deep Dive: Descriptive Statistics of Qualitative Coding Results',
        'Paste in a set of occurrence frequencies for each coding category; first look at',
        'and total to confirm no missed or extra entries, then look at the mean and',
        'to judge central tendency.',
        'Use range and',
        'to judge the dispersion of each coding category occurrence frequency; a persistently large standard deviation indicates inconsistent data standards or outliers.',
        'Run each of two batches (e.g. pre-post test, two groups of subjects) once, comparing mean and standard deviation for a preliminary difference judgment.',
        'Example of occurrence frequency per coding category',
        'Input occurrence frequencies per category: 12,9,8,6,5,5,3,2. Sample size 8, total 50, mean 6.25, median 5.50, range 10, standard deviation 3.15. The first three categories total 29 (58%), forming the main structure of the material; the last three total only 10, and in triangulation should be prioritized for re-interview of these low-frequency themes.',
        'Can triangulation be done automatically?',
        'No. The tool only does',
        'descriptive statistics',
        ', and triangulation requires you to judge against the three sources of interview, observation and document by yourself.',
        'Should categories with very low frequency be merged?',
        'Categories appearing 1–2 times can be kept and noted in a memo first, and merged or deleted after the second batch is entered, avoiding prematurely erasing abnormal clues.',
        'About the Qualitative (Research / Method / Analysis) Path',
        'Qualitative (Research / Method / Analysis) Path. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
        'E.g.: Interview1,Price sensitivity,Insufficient service',
    ]))
    write('assessor-50', build('assessor-50', [
        '📣 Comprehensive Advertising Effectiveness Assessment',
        'Enter ad delivery data (exposure effect / memory effect / attitude effect); the system computes the Advertising Effectiveness Index (AEI) and gives an effectiveness rating and optimization suggestions.',
        'Core formula (by input variables): Math.round(min(aidedRecall,100)×0.35+min(unaidedRecall,100)×0.40+min(recognition,100)×0.25); Math.round(min(favorability,50)×0.7+min(purchaseIntent,50)×0.7+((nps+100)÷200)×36); Math.round(exposureScore×0.30+memoryScore×0.35+attitudeScore×0.35)',
        'Advertising (effect / memory / attitude) assessment',
        '/ Advertising (effect / memory / attitude) assessment',
        '📖 View the User Guide for Comprehensive Advertising Effectiveness Assessment',
        '1. Exposure effect (weight 30%)',
        'Ad reach count',
        'Average exposure frequency',
        'Click-through rate CTR (%)',
        '2. Memory effect (weight 35%)',
        'Aided recall rate (%)',
        'Unaided recall rate (%)',
        'Brand recognition rate (%)',
        '3. Attitude effect (weight 35%)',
        'Brand favorability lift (%)',
        'Purchase intention lift (%)',
        'Recommendation willingness NPS',
        'Ad investment (10,000 CNY)',
        'Reach rate = reach count ÷ target audience × 100%',
        'Effective frequency: 3–7 times is best; too low means insufficient memory, too high wastes budget',
        'Aided recall >40% is good, unaided recall >20% is excellent',
        'NPS (net promoter score): promoters% − detractors%, >30 good, >50 excellent',
        '📚 Deep Dive: Advertising Effectiveness Index (AEI) Assessment',
        'After a campaign ends, aggregate reach, frequency, CTR and recall/favorability data, compute AEI to judge overall effect.',
        'Compare the AEI and sub-scores of two creatives or two media mixes to locate whether exposure is insufficient or memory/attitude is weak.',
        'Combine investment to compute cost per reach and cost per recalled user, for cross-channel cost-performance comparison.',
        'AEI calculation for a 500,000 CNY campaign',
        'Reach 400,000 / target audience 800,000 (reach rate 50% → 15 pts), average frequency 4 (within 3–7 → 40 pts), CTR 2.0% (2/5×30 = 12 pts) → exposure 67 pts. Aided recall 60%, unaided recall 35%, brand recognition 70% → memory = 60×0.35 + 35×0.40 + 70×0.25 = 53 pts. Favorability lift 20%, purchase intention lift 15%, NPS 30 → attitude = 20×0.7 + 15×0.7 + (130/200)×36 = 48 pts. AEI = 67×0.30 + 53×0.35 + 48×0.35 ≈ 55 → "average effect", weak link in memory (only 35% unaided recall). At investment 500,000 CNY, cost per reach = 500,000 ÷ 400,000 = 1.25 CNY, cost per recalled user = 500,000 ÷ 140,000 ≈ 3.57 CNY.',
        'Why do the three AEI dimensions have different weights?',
        'Exposure 30%, memory 35%, attitude 35%. Exposure is only a prerequisite; what truly drives conversion is whether consumers remember and form preference, so the latter two each take 35%.',
        'How are the rating bands divided?',
        'AEI ≥80 excellent, 65–79 good, 50–64 average, <50 poor. Below 65, locate the weak link by the three sub-scores rather than simply adding budget.',
        'About the Comprehensive Advertising Effectiveness Assessment',
        'A comprehensive advertising effectiveness assessment tool that computes the Advertising Effectiveness Index AEI from three dimensions: exposure effect (reach/frequency/CTR), memory effect (aided/unaided recall, brand recognition) and attitude effect (favorability/purchase intention/NPS), auto-rates and gives targeted optimization suggestions.',
        'Three-dimension weighted Advertising Effectiveness Index AEI',
        'Exposure/memory/attitude item-by-item diagnosis',
        'CPM and cost per recalled user calculation',
        'Smart optimization suggestions based on weak links',
        'Four-level effectiveness rating (excellent/good/average/poor)',
        'Post-campaign effectiveness review',
        'A/B test plan effect comparison',
        'Annual ad budget allocation reference',
        'Brand and performance ad assessment',
        'How to use the Comprehensive Advertising Effectiveness Assessment',
        'What does the Comprehensive Advertising Effectiveness Assessment do?',
        'How to use the Comprehensive Advertising Effectiveness Assessment?',
        'Which scenarios is the Comprehensive Advertising Effectiveness Assessment suitable for?',
    ]))

if __name__ == '__main__':
    main()
