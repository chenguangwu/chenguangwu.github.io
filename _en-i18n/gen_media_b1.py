#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'media')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'media')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'media', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- analysis-26 (22) ----------------
    write('analysis-26', build('analysis-26', [
        "📊 Sentiment / Word-Frequency Analysis",
        "Sentiment / Word Frequency",
        "📖 Read the \"Sentiment / Word-Frequency Analysis User Guide\"",
        "A built-in positive/negative dictionary scores word-frequency hits for every text and classifies sentiment (positive/negative/neutral), then aggregates a sentiment tendency index = (positive - negative) / (positive + negative) x 100. It also counts high-frequency Chinese characters after stop-word removal to reveal the focus of public opinion.",
        "Input the text to analyze (one comment or post per line)",
        "The service at this store is great and shipping was fast, very satisfied\nThe item I received had scratches, disappointing experience and I want to return\nGood value for money, recommended",
        "Analyze Sentiment",
        "📚 Deep dive: Sentiment / Word-Frequency Analysis",
        "Batch sentiment scoring: enter the sentiment scores (1-5) of a whole batch of comments or posts at once, use the mean to see the overall reputation level, and",
        "inspect typical reviews instead of judging from a single comment.",
        "Keyword frequency dispersion: count how often a keyword appears across channels, then use the",
        "/range to judge whether the distribution is balanced or concentrated in a few channels.",
        "Outlier sample location: use min/max/range to quickly lock onto extremely positive or negative samples, which supports crisis alerting and reputation repair.",
        "Worked example (sentiment scores of 10 comments: 3,4,2,5,4,3,5,2,4,3)",
        "Sample size n=10, sum=35, mean=35/10=3.50, median after sorting=3.50, min/max=2/5, range=5-2=3, variance~1.05, standard deviation~1.02. Interpretation: the mean equals the median (3.5), so the reputation distribution is symmetric; the standard deviation of 1.02 is small, meaning ratings are tightly clustered with no clear polarization. The tool outputs each step in the order \"sample size -> sum -> mean -> median -> min/max -> range -> variance -> standard deviation\".",
        "Which is more trustworthy, the mean or the median?",
        "The mean is sensitive to outliers while the median is not affected by extreme values. When sentiment scores contain no extreme outliers the two are close (here mean = median = 3.5) and the mean can be used directly; if there are rating-brigade or spam outliers, rely on the median instead.",
        "What does the standard deviation really mean?",
        "The standard deviation measures how spread out the scores are: the larger it is, the more polarized the ratings; the smaller it is, the more consistent the opinions. The range shows the span between the two ends, the standard deviation shows the overall spread, and the two complement each other.",
        "About \"Sentiment / Word-Frequency Analysis\"",
        "Sentiment / Word-Frequency Analysis. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "The service at this store is great and shipping was fast, very satisfied\nThe item I received had scratches, disappointing experience and I want to return\nGood value for money, recommended",
    ]))

    # ---------------- analysis-funnel (22) ----------------
    write('analysis-funnel', build('analysis-funnel', [
        "🎯 Data Analysis (Funnel / Heatmap)",
        "Funnel / Heatmap",
        "📖 Read the \"Data Analysis (Funnel / Heatmap) User Guide\"",
        "Conversion funnel analysis: enter the user count for each step from top to bottom, then compute the step-to-step conversion rate, the lost user count and loss rate per step, plus the overall conversion rate of the last step relative to the first, to pinpoint the bottleneck step.",
        "User count for each funnel step (top to bottom, separated by commas or newlines)",
        "Analyze Funnel",
        "📚 Deep dive: Conversion Funnel and Heatmap Analysis",
        "E-commerce",
        "conversion funnel",
        ": enter the user counts for each step of impression -> click -> add to cart -> order, and use the step",
        "conversion rate",
        "to locate the step with the largest drop-off and optimize it.",
        "Landing page A/B testing: compute the overall conversion rate for two groups of the same steps and compare which funnel version performs better.",
        "Worked example (4-step funnel: 2000->1000->400->120)",
        "The step conversion rates are 50.00%, 40.00% and 30.00%; the overall conversion rate = last/first = 120/2000 = 6.00%; the largest loss is at step 1->2 (1000 users lost, 50% loss rate). The tool outputs every step from the formulas to pinpoint the bottleneck step.",
        "Why is the overall conversion rate so much smaller than the step conversion rates?",
        "The overall conversion rate = last-step users / first-step users, which is the product of all step rates (here 0.5 x 0.4 x 0.3 = 0.06). Every stage eliminates a portion of users, so the cumulative decay is fast and ends up far below any single-step rate.",
        "How should step conversion rate and loss rate be read?",
        "Step conversion rate = current-step users / previous-step users, reflecting the pass efficiency of that step; lost users = previous step - current step, and loss rate = lost / previous step. The step with the highest loss rate is the bottleneck to optimize first.",
        "About \"Data Analysis (Funnel / Heatmap)\"",
        "Data Analysis (Funnel / Heatmap). Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "For example: 1000,600,300,150,80",
    ]))

    # ---------------- assessor-25 (26) ----------------
    write('assessor-25', build('assessor-25', [
        "📋 Reading (Open Rate / Completion) Assessment",
        "Open Rate / Completion",
        "📖 Read the \"Reading (Open Rate / Completion) Assessment User Guide\"",
        "Open rate = opens / delivered x 100%; completion rate = completions / opens x 100%; interaction rate = interactions / opens x 100%; average reading time = total reading time / opens; reading speed is about word count / average reading time (words per minute). The composite score is a weighted 100-point scale of open rate 30%, completion rate 40% and interaction rate 30%, where 80 or above is excellent, 60 to 79 is good, and below 60 needs optimization.",
        "Content reading performance assessment (open rate / completion rate / interaction rate)",
        "Total pushes or sends",
        "Number opened and read",
        "Number completed (read to the end)",
        "Number of interactions (likes / comments / shares)",
        "Average reading time (seconds)",
        "Total word count of the content",
        "Assess Reading Performance",
        "📚 Deep dive: Reading (Open Rate / Completion) Assessment",
        "Campaign performance review: enter sends, opens, completions, interactions and reading time, then use the open rate to judge title and cover, the completion rate to judge content quality, and the interaction rate to judge resonance.",
        "Reading completion diagnosis: use actual reading time / expected time (word count / 5) to see whether users really finished, and locate low-quality traffic that \"opens and leaves\".",
        "Composite score: each of the three rates is scored 0-3 by threshold (9 points total); >=75% excellent, 50-75% good, 25-50% average, <25% poor, giving a quick grade.",
        "Worked example (8000 sent / 2400 opened / 1440 completed / 300 interactions / 120 s reading / 800 words)",
        "Open rate = 2400/8000 x 100% = 30.0%; completion rate = 1440/2400 x 100% = 60.0%; interaction rate = 300/2400 x 100% = 12.5%; expected time = 800/5 = 160 s; reading completion = 120/160 x 100% = 75.0%. All three rates pass the threshold -> composite 9/9 = 100% \"Excellent reading performance\". The tool outputs four dimensions and gives the composite score plus optimization advice.",
        "What open rate / completion rate counts as normal?",
        "Open rates are usually 5-30% (depending on follower quality and title) and completion rates 20-60%; all three being high means the content matches the audience well. Here open 30% / completion 60% / interaction 12.5% are all in the upper-middle range.",
        "How should reading completion be understood?",
        "Expected time = word count / 5 (at about 5 words per second of",
        "reading speed",
        "), and reading completion = actual time / expected time. A low value (e.g. <60%) means users did not finish, which may be caused by a weak opening, excessive length, or mismatched expectations.",
        "About \"Reading (Open Rate / Completion) Assessment\"",
        "Reading (Open Rate / Completion) Assessment. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))


if __name__ == '__main__':
    main()
