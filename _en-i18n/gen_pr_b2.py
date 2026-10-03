#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pr')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pr')
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
    out = {'slug': slug, 'industry': 'pr', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('assessor-58', build('assessor-58', [
        "🔎 KOL (Screening/Collaboration/Evaluation) Mechanism",
        "A full-chain assessment of KOL (key opinion leader) collaboration, covering five dimensions: follower scale and quality, content creation ability, brand fit, interaction performance and return on investment.",
        "📖 View the usage guide for 'KOL (Screening/Collaboration/Evaluation) Mechanism'",
        "KOL quality score = follower quality + content creation ability + brand fit + interaction performance (0 to 5 points each, 20 in total); 17 or above is preferred, 13 to 16 is workable, 9 to 12 needs caution, and below 9 is not recommended; ROI = impressions ÷ collaboration fee (or real followers ÷ quoted price), used for horizontal comparison.",
        "1. Follower scale (10k)",
        "2. Follower quality (activity/authenticity)",
        "5-High quality and high activity",
        "4-Fairly good quality",
        "3-Average quality",
        "2-Low quality",
        "1-Suspected bot traffic",
        "3. Content creation ability",
        "5-Original high-quality content",
        "4-Fairly good content",
        "3-Average content",
        "1-Poor content",
        "4. Brand fit",
        "5-Highly aligned",
        "4-Fairly aligned",
        "3-Basically aligned",
        "2-Low fit",
        "1-Not aligned",
        "5. Interaction performance (comments/shares/likes)",
        "5-High interaction rate",
        "4-Fairly good interaction",
        "3-Average interaction",
        "2-Low interaction",
        "1-Extremely low interaction",
        "6. Collaboration fee (10k CNY)",
        "7. Estimated impressions (10k)",
        "Follower scale is only a reference; follower quality and interaction rate matter more",
        "A CPM (cost per mille impressions) below 50 CNY is excellent, above 200 CNY is on the high side",
        "Brand fit is the key factor in successful KOL collaboration",
        "Check whether the KOL's historical data shows artificial inflation",
        "📚 Deep Dive: KOL (Screening/Collaboration/Evaluation) Mechanism",
        "When screening KOLs commercially, score 0-5 on each of the four items - follower quality, content creation, brand fit and interaction performance - then combine follower count, fee and impressions to compute CPM/CPE and grade them together.",
        "Under the same budget, compare two KOL types (head vs vertical) and use CPM/CPE to see which offers better value.",
        "After the collaboration, review the actual interactions and compare them with the pre-signing scores, accumulating early warning features for 'high score but flop'.",
        "Scoring criteria",
        "Composite score = follower quality + content creation + brand fit + interaction performance (0-5 each, 20 in total); grades: ≥17 preferred KOL, ≥13 workable KOL, ≥9 assess with caution, <9 not recommended. Cost metrics: CPM (cost per mille impressions) = collaboration fee ÷ estimated impressions × 10000 (both fee and impressions in units of 10k); cost per follower CPE = collaboration fee ÷ follower count.",
        "A tech KOL: 5 million followers, quality 5 + content 5 + fit 4 + interaction 4 = 18 points, judged a preferred KOL; fee 200k CNY, impressions 30 million → CPM = 20÷3000×10000 = 66.67 CNY, CPE = 20÷500 = 0.04 CNY. By contrast, a low-quality account: quality 2 + content 2 + fit 1 + interaction 2 = 7 points, judged not recommended; even with a fee of only 50k CNY and 1 million impressions, CPM is as high as 500 CNY (7.5 times that of the preferred KOL), so the value is extremely poor.",
        "Does a low CPM mean it is worth investing?",
        "Not necessarily. CPM only looks at the unit price of impressions and ignores follower quality and fit - an account with an extremely low CPM but fake followers or a mismatched tone will not convert no matter how many impressions it gets. This tool puts CPM/CPE alongside the four-dimension score; accounts with a composite score below 9 are not recommended however low the CPM.",
        "The composite score excludes follower count - does it miss head KOLs?",
        "The score measures 'quality', while follower count/impressions/fee measure 'volume and price' - two separate lines. Head KOLs usually have large followings but their quality/fit may not be full marks; in the end you have to weigh across dimensions with CPM/CPE between 'high-score small accounts' and 'low-score large accounts'. This tool exists precisely to provide a unified panel for that trade-off.",
        "About 'KOL (Screening/Collaboration/Evaluation) Mechanism'",
        "The KOL collaboration assessment tool scores across four dimensions - follower quality, content creation, brand fit and interaction performance - and combines follower scale, collaboration fee and estimated impressions to compute cost metrics such as CPM, helping PR teams screen and evaluate the value of KOL collaborations scientifically.",
        "4-dimension KOL quality score",
        "CPM cost analysis",
        "Cost per follower calculation",
        "KOL screening and evaluation",
        "Collaboration value-for-money analysis",
        "KOL campaign effect review",
        "Budget allocation reference",
    ]))

    write('assessor-59', build('assessor-59', [
        "📢 PR (Effect/Evaluation/Reporting) System",
        "A systematic quantified assessment of PR communication effect covering five dimensions - media coverage, communication volume, sentiment tendency, key message penetration and crisis response - to help produce a PR effect evaluation report.",
        "📖 View the usage guide for 'PR (Effect/Evaluation/Reporting) System'",
        "Key message penetration rate = reports containing the core message / total reports",
        "1. Total number of media reports",
        "2. Of which, core media reports",
        "3. Estimated total impressions (10k person-times)",
        "4. Sentiment tendency (positive/neutral/negative ratio)",
        "5-Positive >80%",
        "4-Positive 60-80%",
        "3-Positive 40-60%",
        "2-Positive <40%",
        "1-Mainly negative",
        "5. Key message penetration rate",
        "5-Key message >80% coverage",
        "4-60-80% coverage",
        "3-40-60% coverage",
        "2-20-40% coverage",
        "1-<20% coverage",
        "6. Crisis response performance",
        "5-Excellent response",
        "4-Fairly good response",
        "3-Average response",
        "2-Insufficient response",
        "1-Response failure",
        "Core media means industry-leading media and authoritative media",
        "Sentiment tendency analysis needs the support of public opinion monitoring tools",
        "Key message penetration rate = reports containing the core message / total reports",
        "An effect score of 13 or above is excellent, and 10 or above is good",
        "📚 Deep Dive: PR (Effect/Evaluation/Reporting) System",
        "After a brand campaign wraps up, tally the number of reports, core media count and impressions, and score 0-5 on sentiment tendency, message penetration and crisis response to quantify the communication effect.",
        "Compare against the KPIs set before the campaign (core media share target, impression target) to see the attainment.",
        "Plot the effect scores of multiple campaigns as a time series to identify 'high volume but low penetration' inflated campaigns.",
        "Scoring criteria",
        "Displayed metrics: total number of reports, number of core media reports, core media share = core media count ÷ total reports × 100%, estimated impressions (10k person-times). Effect score = sentiment tendency + key message penetration + crisis response (0-5 each, 15 in total); grades: ≥13 excellent, ≥10 good, ≥7 qualified, <7 insufficient. Note: report count and impressions are only for display and do not count toward the effect total.",
        "One campaign: 50 reports, 20 core media → core share 40%; impressions 20 million person-times; sentiment 5 + penetration 5 + crisis 4 = 14 points, judged excellent (≥13). By contrast, another campaign: 50 reports, 20 core (share still 40%), impressions 20 million, but sentiment 3 + penetration 3 + crisis 2 = 8 points, judged only qualified - showing that although the latter 'published a lot', positive sentiment and key message reach are weak, a typical 'high volume, low penetration' case.",
        "Why is the report count not counted in the effect score?",
        "Count is 'quantity', while sentiment/penetration/crisis are 'quality'; mixing them lets inflation interfere. Keeping count and impressions as separate display metrics, the effect score only judges 'was it said right, did it get through, did anything go wrong', which is closer to the essence of PR - influencing awareness rather than piling up column inches.",
        "Is a 40% core media share high?",
        "It depends on the industry and the campaign goal. 40% is a healthy range (meaning nearly half the reports come from authoritative sources, giving strong endorsement); below 20% is mostly long-tail self-published media, whose credibility and secondary spread are markedly reduced. This tool only gives the share figure; the target value must be set against your own media matrix.",
        "About 'PR (Effect/Evaluation/Reporting) System'",
        "The PR effect evaluation system quantifies PR communication effect across five dimensions - media coverage, communication volume, sentiment tendency, key message penetration and crisis response - helping PR teams produce professional effect evaluation reports.",
        "Quantified media coverage analysis",
        "Sentiment tendency assessment",
        "Key message penetration rate",
        "Core media share calculation",
        "PR communication effect assessment",
        "Public opinion monitoring report",
        "Annual PR summary",
        "Brand communication strategy optimisation",
    ]))

    write('assessor-risk', build('assessor-risk', [
        "🎲 Event Risk Assessment (Probability/Impact)",
        "A quantified assessment of event risk based on a risk matrix (probability x impact), covering five categories - safety, financial, reputation, operational and legal compliance risk - automatically computing the risk level and giving response suggestions.",
        "📖 View the usage guide for 'Event Risk Assessment (Probability/Impact)'",
        "Single event risk value = probability of occurrence (1 to 5 points) × degree of impact (1 to 5 points), ranging 1 to 25; the risk level is determined by the highest risk value: 16 or above is extreme risk, 10 to 15 is high risk, 5 to 9 is medium risk, and below 5 is low risk; items with a risk value of 10 or above must be included in the high-priority contingency plan list.",
        "Risk matrix standard",
        "Probability: 1=very low 2=low 3=medium 4=high 5=very high",
        "Impact: 1=minimal 2=minor 3=medium 4=major 5=severe",
        "Risk value = probability x impact, 1-4 low risk 5-9 medium risk 10-15 high risk 16-25 extreme risk",
        "1. Safety risk - probability of occurrence",
        "1. Safety risk - degree of impact",
        "1-Minimal",
        "2-Minor",
        "4-Major",
        "5-Severe",
        "2. Financial risk - probability of occurrence",
        "2. Financial risk - degree of impact",
        "3. Reputation risk - probability of occurrence",
        "3. Reputation risk - degree of impact",
        "4. Operational risk - probability of occurrence",
        "4. Operational risk - degree of impact",
        "5. Legal compliance risk - probability of occurrence",
        "5. Legal compliance risk - degree of impact",
        "Risk value = probability x impact, the higher the value the greater the risk",
        "Risk items scoring above 10 require a dedicated contingency plan",
        "Safety risk and legal compliance risk need focused attention regardless of the score",
        "Complete the risk assessment 2 weeks before the event and submit it for management approval",
        "📚 Deep Dive: Event Risk Assessment (Probability/Impact)",
        "When planning a large event, estimate the probability (1-5) and impact (1-5) for each of the five risk categories - safety, financial, reputation, operational and legal compliance - and rank them by probability × impact.",
        "Compare the five risk categories horizontally to lock onto the one with the highest risk value and write its contingency plan first.",
        "Count items with a risk value ≥10 as 'high-risk items', which are the red lines for mandatory insurance and emergency posts.",
        "Scoring criteria",
        "5 risk categories (safety risk, financial risk, reputation risk, operational risk, legal compliance risk), each filled with a probability (1-5) and an impact (1-5); risk value = probability × impact; the highest risk value takes the maximum of the five. Levels: highest risk value ≥16 extreme risk, ≥10 high risk, ≥5 medium risk, <5 low risk; items with a risk value ≥10 count as 'high-risk items'.",
        "A music festival: safety(5,5)=25, financial(4,3)=12, reputation(3,4)=12, operational(4,3)=12, legal(2,3)=6 → the highest 25 is judged extreme risk, with 4 high-risk items (safety/financial/reputation/operational), requiring cancellation or major adjustment. By contrast, an internal training session: safety(3,3)=9, financial(2,2)=4, reputation(3,2)=6, operational(2,3)=6, legal(2,2)=4 → the highest 9 is judged medium risk, with 0 high-risk items, so a standard contingency plan suffices.",
        "If both probability and impact are 5 giving a risk value of 25, should the event be cancelled outright?",
        "A risk value of 25 triggers the 'extreme risk, cancellation or major adjustment recommended' notice, but whether to cancel also depends on whether the risk can be mitigated - for example a safety risk (5,5) can have its probability pushed down to 2 through capacity limits, security screening and on-site medical staff, bringing the risk value down to 10. This tool gives the 'risk level without intervention', which drives the contingency plan rather than acting as a single veto.",
        "Why multiply probability × impact instead of adding them?",
        "Multiplication distinguishes 'high probability low impact' from 'low probability high impact' - the two may be equal when added, but the latter has severe consequences once triggered. Multiplication gives 'extreme impact' inherently higher weight, which is closer to risk management common sense (such as tail catastrophe events). If your system prefers addition, you can use the result as a reference and compute separately.",
        "About 'Event Risk Assessment (Probability/Impact)'",
        "The event risk assessment tool quantifies the five categories of event risk based on a risk matrix (probability x impact), automatically computing the risk value and level of each item, helping event teams identify high-risk items and formulate contingency plans.",
        "Full coverage of 5 risk categories",
        "Probability x impact risk matrix",
        "Automatic risk level determination",
        "Risk response suggestions",
        "Large event risk assessment",
        "Event scheme approval",
        "Insurance underwriting reference",
    ]))


if __name__ == '__main__':
    main()
