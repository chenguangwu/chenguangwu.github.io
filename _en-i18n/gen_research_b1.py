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
    write('analysis-49', build('analysis-49', [
        '📋 Scale (Reliability / Validity / Factor) Analysis',
        'Reliability / validity / factor',
        'Enter the scale data matrix (one respondent per row, one item per column) to compute Cronbach alpha, assessing internal consistency reliability. Typically alpha ≥0.70 is considered reliable, 0.60–0.70 marginally usable, below 0.60 needs item revision. Data is processed locally in the browser only, never uploaded.',
        '📖 View the User Guide for Scale (Reliability / Validity / Factor) Analysis',
        'α = k ÷ (k − 1) × (1 − Σ item variance ÷ total score variance)',
        'Total score variance is computed from the sum scores of all respondents',
        'Enter the scale data matrix (one respondent per row, one item per column) to compute Cronbach alpha, assessing internal consistency reliability. Typically alpha ≥0.70 is considered reliable, 0.60 to 0.70 marginally usable, below 0.60 needs item revision. All data is processed locally in the browser only, not uploaded.',
        'Scale data (one respondent per row, comma-separated item scores)',
        'Calculate reliability',
        '📚 Deep Dive: Scale Reliability Analysis (Cronbach α)',
        'At the pre-survey stage, judge whether the self-designed scale items can stably measure the same concept, deciding whether to delete or add items.',
        'Before formal administration, run the existing scale once to confirm it still has acceptable internal consistency on this sample.',
        'Compute each dimension of the questionnaire separately, and check dimension by dimension whether all reach an acceptable α level.',
        'Five-item scale pilot test',
        '6 respondents, 5 items, total item variance 3.50, total score variance 13.56. α = 5 ÷ 4 × (1 − 3.50 ÷ 13.56) = 1.25 × 0.7418 = 0.927, judged as "excellent reliability".',
        'Ideas to fix low α',
        'If alpha = 0.58 is computed, the common cause is an item with opposite direction or not reverse-scored. First unify the direction of reverse items then recompute; if still low, delete items weakly correlated with others, or add synonymous items to raise inter-item covariance.',
        'Effect of item count on α',
        'Alpha rises with more items; an 8-item scale is often easier to reach 0.80 than a 3-item one. Thus in a short scale a slightly lower alpha (e.g. 0.65) is not necessarily unusable; report the item count alongside so readers can judge.',
        'How much alpha is acceptable?',
        'The common academic threshold: ≥0.70 acceptable, ≥0.80 good, ≥0.90 excellent; in exploratory research or with very few items, 0.60 can be marginally used. Excessively high alpha (e.g. above 0.95) instead signals item redundancy, possibly near-duplicate items.',
        'Does high α mean the scale is valid?',
        'No. Alpha only reflects inter-item consistency, which is reliability, and does not prove the scale measures the construct. Validity needs separate evidence of content validity, construct validity (e.g. factor analysis) and criterion-related validity.',
        'What if data entry errors out?',
        'Requires one respondent per row, same column count per row and at least 2 columns. If a row column count differs from the first, the tool prompts and refuses to calculate; for missing data, first handle per the scale manual (e.g. series mean substitution or whole-record removal), do not leave blanks.',
        'About the Scale (Reliability / Validity / Factor) Analysis',
        'Scale (Reliability / Validity / Factor) Analysis. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))
    write('analysis-50', build('analysis-50', [
        '🎓 Competitive (Intelligence / Analysis / Strategy) Framework',
        'Competitive landscape and market share estimation',
        '📖 View the User Guide for Competitive (Intelligence / Analysis / Strategy) Framework',
        'Enter one line per "company,revenue". Share = company revenue ÷ total market size × 100%; CRn = sum of top n companies shares; HHI = Σ (each company share percentage squared). HHI>2500 is highly concentrated, 1500–2500 moderately concentrated, below 1500 competitively fragmented.',
        'Competitor data (one line per "company,revenue")',
        'Company A,300\nCompany B,200\nCompany C,100',
        'Estimate landscape',
        '📚 Deep Dive: Competitive Landscape and Market Share Estimation',
        'Industry researchers organize major competitors revenue data, estimate CR3, CR5 and HHI, and judge industry concentration and entry barriers.',
        'Before formulating strategy, companies use this tool to quantify their own share gap with leading rivals, positioning as challenger or follower.',
        'In investment due diligence, quickly verify the claimed "market position" of a target, cross-checking with share and concentration data.',
        'Five-company landscape trial calculation',
        'Input "A Co.,520; B Co.,380; C Co.,260; D Co.,150; E Co.,90", total market size 1400.00, leading company A Co. (37.14%), CR3 82.86%, CR5 100.00%, HHI 2617.35, judged as a highly concentrated landscape.',
        'What HHI counts as highly concentrated?',
        'Common standard: HHI above 2500 is highly concentrated, 1500–2500 moderately concentrated, below 1500 competitively fragmented; thresholds vary slightly by regulatory standard.',
        'What is the difference between CR3 and HHI?',
        'CR3 only looks at the combined share of the top three, easily overlooking gaps among the leaders; HHI sums squared shares, more sensitive to the relative scale of leading firms.',
        'What if revenue units are inconsistent?',
        'This tool only does relative share calculation; units do not affect the result, but the same input must use unified units (e.g. all in 100 million CNY or all in 10,000 CNY).',
        'About the Competitive (Intelligence / Analysis / Strategy) Framework',
        'Competitive (Intelligence / Analysis / Strategy) Framework. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
        'A Co.,520',
    ]))
    write('analysis-51', build('analysis-51', [
        '🎓 Public Opinion (Monitoring / Analysis / Reporting) System',
        'Public opinion volume and sentiment distribution monitoring',
        '📖 View the User Guide for Public Opinion (Monitoring / Analysis / Reporting) System',
        'Enter one line per "period,positive,neutral,negative" volume. Total volume is the sum of the three; each sentiment ratio = that sentiment volume ÷ total volume × 100%. The tool outputs the negative rate, the peak-volume period and the highest-negative-rate period, and gives a public-opinion attention level by negative rate.',
        'Public opinion data (one line per "period,positive,neutral,negative")',
        'Monitoring analysis',
        '📚 Deep Dive: Public Opinion Volume and Sentiment Distribution Monitoring',
        'PR and brand teams summarize daily public-opinion volume, observe negative-rate changes, and judge whether incident handling needs escalation.',
        'Communication researchers compare total volume and sentiment structure across periods, locating the peak-volume and highest-negative-rate time points.',
        'At project closure, use the three metrics of total volume, positive ratio and negative rate to quantify communication effect.',
        'Three-day public-opinion monitoring trial',
        'Input "D1,120,60,20; D2,90,50,60; D3,150,40,30", total volume 620, positive 58.06%, neutral 24.19%, negative 17.74%; peak-volume period is D3, highest-negative-rate period is D2 (30.00%).',
        'How high a negative rate needs an alert?',
        'The tool uses two tiers, 15% and 25%: below 15% is controllable, 15%–25% needs attention, reaching above 25% needs key handling; specific thresholds can be adjusted by industry.',
        'How are sentiment categories determined?',
        'This tool does not judge text sentiment; it only summarizes and computes ratios for the positive, neutral and negative volumes you have already categorized; the classification standard is up to you.',
        'Can the period be any granularity?',
        'Yes, day, week or hour all work, as long as each row is filled in period order and the sentiment volumes are non-negative numbers.',
        'About the Public Opinion (Monitoring / Analysis / Reporting) System',
        'Public Opinion (Monitoring / Analysis / Reporting) System. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.',
    ]))

if __name__ == '__main__':
    main()
