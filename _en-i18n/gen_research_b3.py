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
    write('calc-97', build('calc-97', [
        '🧮 Sample Size / Quota / Error Calculator',
        'Compute the minimum sample size needed for sampling, the actual sampling error at a given sample size, and support proportional quota allocation for stratified sampling.',
        'Core formula (by input variables): Math.round(n×s.size÷totalStrata); Math.ceil(n0÷(1+(n0-1)÷N)); Math.ceil(n0)',
        '📖 View the User Guide for Sample Size / Quota / Error Calculator',
        'Expected proportion p (%)',
        'Target error limit e (%, for required sample size)',
        'Actual sample size n (for actual error)',
        'Empty population size means infinite population',
        'Treat as infinite population',
        'Stratified quota (each row: stratum name, size)',
        'High income,2000\nMiddle income,5000\nLow income,3000',
        '💡 Required sample size n₀=Z²p(1−p)/e²; actual error e=Z·√[p(1−p)/n]·√[(N−n)/(N−1)]; stratification allocates by n_i=n·N_i/N proportional.',
        'The sum of stratum sizes should be close to N, otherwise allocate by the actual total',
        'Proportional allocation applies when stratum variances are similar; when variance differs greatly, consider Neyman allocation',
        'Do not apply the finite population correction (FPC) for infinite populations',
        'Actual error decreases as sample size grows, but with diminishing marginal returns',
        '📚 Deep Dive: Sample Size, Sampling Error and Stratified Quota',
        'At the survey design stage, infer the minimum from confidence level, expected proportion and allowed error',
        'When the actual sample size is known, back-calculate the sampling error to judge whether the conclusion supports the decision.',
        'Stratified sampling allocates quotas by each stratum size proportion, keeping the sample structure consistent with the population.',
        'How many samples for 95% confidence and ±5% error',
        'Confidence level 95% (z = 1.96), expected proportion p = 50% (most conservative), allowed error e = 5%, infinite population: n₀ = 1.96² × 0.5 × 0.5 ÷ 0.05² = 384.16 → at least 385 copies. If population N = 5,000 with finite population correction: n = 384.16 ÷ (1 + 383.16/5,000) = 356.8 → 357 copies, 28 fewer than the infinite case. Reverse check: at n = 385 the actual error = 1.96 × √(0.25/385) = 4.99%, consistent with the set 5%.',
        'Why is the expected proportion default 50%?',
        'p(1−p) reaches its maximum at p = 50%, giving the most conservative sample size. If you are sure the proportion is near 0 or 1 (e.g. a rare behavior 5%), using the actual proportion can significantly reduce the sample size.',
        'When should the finite population correction be used?',
        'When the sampling ratio n/N exceeds about 5%, the correction can noticeably reduce the required sample. After checking population size, the tool auto-applies the √((N−n)/(N−1)) factor; if the population is very large, check infinite population.',
        'About the Sample Size / Quota / Error Calculator',
        'A comprehensive survey sampling calculator that integrates sample-size requirement estimation, actual sampling-error calculation at a given sample, and stratified proportional quota allocation, supporting finite population correction.',
        'Bidirectional calculation of required sample size and actual error',
        'Stratified proportional quota allocation',
        'Error-meeting and gap hints',
        'Social survey sampling design',
        'Stratified sampling quota',
        'Quality inspection error evaluation',
        'Research sample-size justification',
        'High income,2000\nMiddle income,5000\nLow income,3000',
    ]))
    write('index', build('index', [
        '🎓 Research & Academic Tools',
        'Research & academic',
        'Research & academic tools',
        'Compute the minimum sample size needed for sampling, the actual sampling error at a given sample size, and support proportional quota allocation for stratified sampling.',
        'Qualitative research path analysis tool: supports coding of interview and observation materials, theme distillation and triangulation, helping researchers organize qualitative data by standard methods and form analytical conclusions.',
        'Focus group moderation analysis tool: structurally records focus group interview points, moderator outline and code categorization, assisting qualitative researchers in organizing interview materials and extracting key themes.',
        'Competitive intelligence analysis framework tool: based on standard data operations to organize competitive landscape, market share and benchmarking metrics, helping researchers systematically sort competitor intelligence and output structured analytical conclusions.',
        'Product (testing / pricing / concept) testing',
        'Four-dimensional product concept scoring + Van Westendorp price sensitivity test (PSM), automatically computing the optimal price range and concept feasibility.',
        'Advertising (effect / memory / attitude) assessment',
        'Enter ad delivery data (exposure effect / memory effect / attitude effect); the system computes the Advertising Effectiveness Index (AEI) and gives an effectiveness rating and optimization suggestions.',
        'Scale reliability/validity/factor analysis tool: enter each scale item score, compute Cronbach\'s α reliability coefficient and KMO and Bartlett sphericity test indicators, assisting questionnaire quality assessment and factor structure verification.',
        'Public Opinion (Monitoring / Analysis / Reporting) System',
        'Public opinion monitoring analysis system tool: integrates public-opinion volume statistics, sentiment distribution and communication trend metrics, assisting PR and communication researchers in quantitatively assessing event opinion evolution.',
        'About the Research & Academic Tools',
        'The research & academic tools collection includes 8 free online tools, covering common calculation, conversion and lookup needs in research and academic scenarios. Whether you are a practitioner, student or ordinary user in the field, you can find handy tools here that work instantly. All tools run entirely in the browser, upload no data to servers, and protect your privacy.',
        'The research & academic tools featured on this page include (representative tools):',
        'These tools help you quickly complete common research-academic tasks without memorizing complex formulas or manual conversion; just enter to get results.',
        'Do the research & academic tools need download or registration?',
        'No. All research & academic tools on this page are purely front-end online tools; open the web page to use them directly, with no software installation, no account registration, and no data upload.',
        'Are the research & academic tools accurate? Is the data safe?',
        'The tools compute locally in your browser based on public math formulas and general industry standards, with results available instantly. All calculations are done on your device locally, and data is never uploaded to servers, ensuring privacy and security.',
    ]))
    write('tester-17', build('tester-17', [
        '💰 Product Concept Assessment and Pricing Test',
        'Four-dimensional product concept scoring + Van Westendorp price sensitivity test (PSM), automatically computing the optimal price range and concept feasibility.',
        'Core formula (by input variables): (novelty+usefulness+feasibility+marketFit)÷4×10; (tooCheap+tooExpensive)÷2×0.6+tooCheap×0.4; tooExpensive×0.7+expensive×0.3',
        'Product (testing / pricing / concept) testing',
        '/ Product (testing / pricing / concept) testing',
        '📖 View the User Guide for Product Concept Assessment and Pricing Test',
        '1. Product concept assessment',
        'Novelty (1–10 points)',
        'Usefulness (1–10 points)',
        'Feasibility (1–10 points)',
        'Market fit (1–10 points)',
        '2. Price sensitivity test (PSM four questions)',
        'Enter the average feedback price of the research sample (CNY)',
        'Too cheap (suspect quality)',
        'Cheap (good value)',
        'Expensive (needs consideration)',
        'Too expensive (would not buy)',
        'Product cost (CNY)',
        'Research sample size (people)',
        'Comprehensive test',
        'Concept score: novelty/usefulness/feasibility/market fit each 25% weight',
        'The PSM model determines the optimal price range via the intersection of four price curves',
        'Optimal price = intersection of the cheap curve and the expensive curve (acceptable price point)',
        'Price lower bound = intersection of too-cheap and too-expensive, price upper bound = intersection of too-expensive and cheap',
        '📚 Deep Dive: Product Concept Scoring and PSM Price Test',
        'Before a new product is initiated, score the concept novelty, usefulness, feasibility and market fit to judge whether it is worth advancing.',
        'Use the Van Westendorp four questions (too cheap / cheap / expensive / too expensive) to get the acceptable price range and optimal price point.',
        'Look at the concept score and price range together: a strong concept but narrow price range means limited premium space.',
        'Concept 8/9/7/8 and PSM four prices',
        'Concept four dimensions: novelty 8, usefulness 9, feasibility 7, market fit 8 → (8+9+7+8)÷4×10 = 80 points → "excellent concept", weak link is feasibility (7 points), and technology and supply-chain justification should be done before advancing. PSM: too cheap 30 CNY, cheap 50 CNY, expensive 90 CNY, too expensive 130 CNY → optimal price point ≈ (50+90)÷2 = 70 CNY, price lower bound ≈ (30+130)÷2×0.6 + 30×0.4 = 60 CNY, price upper bound ≈ 130×0.7 + 90×0.3 = 118 CNY, acceptable range about 60–118 CNY.',
        'How are the concept score bands divided?',
        'Each dimension 1–10 points, average ×10 to a 100-point scale: ≥80 excellent concept, 65–79 good concept, 50–64 average concept, <50 weak concept. The per-dimension bar chart shows the specific weak link.',
        'How is the PSM price range approximated?',
        'The standard Van Westendorp requires the intersections of four cumulative curves. This tool uses a simplified approximation: the optimal price point takes the midpoint of "cheap" and "expensive", the lower bound is the midpoint of "too cheap/too expensive" weighted by "too cheap", and the upper bound is "too expensive" weighted by "expensive"; suitable for quick scoping, for formal pricing use the full curves.',
        'About the Product Concept Assessment and Pricing Test',
        'A product concept assessment and pricing test tool that combines the four-dimensional product concept scoring (novelty/usefulness/feasibility/market fit) with the Van Westendorp price sensitivity test (PSM), automatically computing the optimal price point (OPP), price range and gross margin, and giving concept feasibility judgment and pricing suggestions.',
        'Four-dimensional product concept scoring (10-point to 100-point scale)',
        'PSM four-question price sensitivity analysis',
        'Optimal price point (OPP) and acceptable price range calculation',
        'Gross margin and price elasticity space evaluation',
        'Concept rating and pricing suggestions auto-generated',
        'New product concept feasibility verification',
        'Product launch pricing strategy formulation',
        'Market research data analysis',
        'A/B concept test plan evaluation',
    ]))

if __name__ == '__main__':
    main()
