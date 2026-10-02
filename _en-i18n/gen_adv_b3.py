#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'advertising')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'advertising')
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
    out = {'slug': slug, 'industry': 'advertising', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('analysis-27', build('analysis-27', [
        "📊 Competitor (Share / Positioning) Analysis",
        "Share / positioning",
        "📖 Read the Competitor (Share / Positioning) Analysis user guide",
        "Enter each competitor's market share (or sales share); the tool ranks them in descending order and computes the cumulative share, the head concentration CRn (the sum of the top n shares) and the HHI index (the sum of squared shares), then groups competitors into leader / challenger / niche tiers based on the largest competitor's share to support differentiation decisions. If the total entered is not 100%, it is automatically normalized for display.",
        "Enter competitors and shares line by line (format: competitor name,share% ; you may also enter numbers only)",
        "In-house,18\nCompetitor A,35\nCompetitor B,28\nCompetitor C,12\nCompetitor D,7",
        "Start analysis",
        "📚 Deep Dive: Competitor (Share / Positioning) Analysis",
        "Enter each competitor's market share (or sales share) to quickly get the ranking, the total and the head concentration (CRn), which reveals the competitive landscape.",
        "Paste share figures from multiple periods to compare and watch yourself and competitors gain or lose ground, to see whether you are being squeezed or expanding.",
        "Group competitors into leader / challenger / niche tiers by share to support differentiation positioning decisions.",
        "Share ranking and CR3 of five competitors",
        "Entered shares: 35, 28, 18, 12, 7 (%). Total 100%; after sorting, the top three total 35+28+18=81%, that is CR3=81%, so the market is highly concentrated; the largest competitor holds 35%, so at 18% you would be in the second tier.",
        "What if the shares do not add up to 100%?",
        "Usually because only the main competitors were entered and the long tail was missed, or because the data basis is inconsistent. You can first fill in the full set of regions or channels and then compute, or tick normalize by the entered values and let the tool rescale the shares. Any conclusion presumes complete data on a consistent basis.",
        "What is CRn?",
        "CRn (Concentration Ratio) is the sum of the shares of the top n companies in an industry, measuring concentration. CR3=81% means the top three control 80% of the market, so a new entrant faces a hard breakout and should take a differentiated or niche route.",
        "About Competitor (Share / Positioning) Analysis",
        "Competitor (share and positioning) analysis. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "In-house,18\nCompetitor A,35\nCompetitor B,28\nCompetitor C,12\nCompetitor D,7",
    ]))
    write('analysis-55', build('analysis-55', [
        "📣 Competitor (Ad / Campaign / Creative) Analysis",
        "Ad / campaign / creative",
        "📖 Read the Competitor (Ad / Campaign / Creative) Analysis user guide",
        "Enter each competitor's impressions, clicks, conversions and creative count line by line; the tool computes CTR (clicks / impressions), conversion rate (conversions / clicks), impression and conversion shares and creative density, ranks by conversion rate, and reports the impression concentration CR3 plus differentiation opportunities, supporting ad campaign review and creative optimization.",
        "Enter competitor campaign data line by line (format: competitor name,impressions,clicks,conversions,creative count)",
        "In-house,120000,3600,180,12\nCompetitor A,200000,5000,150,20\nCompetitor B,90000,2700,90,8\nCompetitor C,60000,1500,60,5",
        "Start analysis",
        "📚 Deep Dive: Competitor (Ad / Campaign / Creative) Analysis",
        "Enter each competitor's monthly ad spend (or creative count) to compare who has more voice and whose budget is more aggressive.",
        "Compare the click-through rate and conversion cost across competitors to find the industry benchmark and calibrate your own expectations.",
        "Combine it with share data to see whether high spend actually buys high share, and judge competitor campaign efficiency.",
        "Share of monthly spend across five competitors",
        "Entered monthly spend: 120, 90, 60, 40, 30 (in ten-thousands), totaling 3.4 million. The shares are 35.3%, 26.5%, 17.6%, 11.8% and 8.8%; the largest competitor spent a third of the total, so it clearly leads in voice.",
        "Where does this kind of campaign data come from?",
        "Public sources include media rate cards, industry reports and third-party monitoring (such as AppGrowing and the Ocean Engine analytics tool), all of which are estimates with differing definitions per platform. This tool only summarizes what you enter; for real decisions rely on authoritative monitoring and your own campaign backend data.",
        "Is it meaningful with only two or three competitors?",
        "A small sample only shows relative magnitude and cannot infer the whole industry. Cover at least the top 3-5 and note the data date, so that a temporary fluctuation is not mistaken for a trend.",
        "About Competitor (Ad / Campaign / Creative) Analysis",
        "Competitor (ad, campaign and creative) analysis. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "In-house,120000,3600,180,12\nCompetitor A,200000,5000,150,20\nCompetitor B,90000,2700,90,8\nCompetitor C,60000,1500,60,5",
    ]))


if __name__ == '__main__':
    main()
