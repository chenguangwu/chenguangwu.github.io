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
    write('analysis-density-1', build('analysis-density-1', [
        "📊 Press Release Keyword Density Analysis",
        "An online press release keyword density analysis tool",
        "Paste the article body and give the keywords to check; the tool computes the true density as 'occurrences ÷ total word count'. Space characters are not counted in Chinese, while English is counted as one word per run of consecutive letters, so mixed Chinese-English articles also get a stable measure. A density below 1% means the topic is not prominent enough, 1%~3% is the common suitable range, 3%~5% is on the dense side, and above 5% is usually judged by readers as keyword stuffing and may also be downweighted by search engines. Multiple synonymous keywords in the same passage should each be counted separately. All content is processed only in the local browser and is never uploaded.",
        "📖 View the usage guide for 'Press Release Keyword Density Analysis'",
        "Total word count = number of Chinese characters + number of English words",
        "Keyword density = keyword occurrences ÷ total word count × 100%",
        "Article body",
        "Green and low-carbon was a hot topic at this year's Two Sessions. Many manufacturing companies said the green and low-carbon transition has already become a source of competitiveness rather than a cost item. Industry experts believe the large-scale application of green and low-carbon technology will significantly reshape the supply chain in the next three years. Smart Manufacturing and digital factory are also mentioned frequently.",
        "Keywords (separate multiple with commas)",
        "Analyse density",
        "📚 Deep Dive: Press Release Keyword Density Analysis",
        "Before publishing, enter the body text and the core keywords to compute the actual occurrence count and density, and judge whether there is keyword stuffing.",
        "Put several synonymous keywords in the same article and count them separately to see whether the topic words are evenly distributed or whether one word is repeatedly stuffed in.",
        "Paste a competitor's press release and run the same statistics to compare",
        "the measure on both sides as a self-check reference before publishing.",
        "Where to fix an elevated density",
        "In a short item of 68 Chinese characters, 'intelligent manufacturing' appears 3 times; with a total word count of 68, the density = 3 ÷ 68 = 4.41%, which falls in the 3%~5% band and is judged on the dense side. Short items are especially prone to crossing the line, so one occurrence can be replaced with a synonymous expression or a pronoun.",
        "How is mixed Chinese-English text counted?",
        "In 128 characters of body text there are 83 Chinese characters and 4 English words, so the total word count by 'Chinese characters + English words' is 87. This algorithm keeps the same measure for mixed Chinese-English articles and does not become unbalanced because English is split by spaces while Chinese is counted by character.",
        "Keywords that never appear",
        "If a keyword never appears, the tool marks it as 'not present' rather than giving it a 0.00% density rating. At that point check whether the keyword was wrapped in full-width Chinese parentheses, or whether the keyword itself was written as an alias.",
        "What density is appropriate?",
        "The common reference is 1%~3% suitable, below 1% the topic is not prominent enough, 3%~5% is on the dense side, and above 5% is usually judged by readers as keyword stuffing and may also be downweighted by search engines. The reasonable density of a press release is generally lower than that of an SEO landing page, so do not copy the figures from page optimisation practice.",
        "Is the density here computed by the same algorithm as SEO density?",
        "The measure is consistent but the object differs. Search engines usually compute it from the word segmentation result of the full web page, while this tool computes it in real time from the text you paste; both follow 'occurrences ÷ total word count', but this tool neither crawls the web nor does dictionary-based word segmentation, and long phrases are counted as exact whole-string matches.",
        "English keywords",
        "Do case differences count as the same word?",
        "Yes. The tool first matches the original text exactly; if it misses, it lowercases and matches once more, so 'Smart Manufacturing' and 'smart manufacturing' are counted as the same keyword and nothing is missed.",
        "About 'Press Release Keyword Density Analysis'",
        "Press Release Keyword Density Analysis. A free online tool processed entirely in the browser, no data uploaded, privacy and security protected.",
        "Paste the press release body text",
    ]))

    write('analysis-6', build('analysis-6', [
        "📊 Sentiment Polarity Analysis by Word Frequency",
        "Word frequency",
        "The body text is counted by Chinese characters and English words to obtain the total word count, then the built-in sentiment word list counts the occurrences of positive and negative words separately; the ratio of their difference to their sum is the polarity index, ranging between -100% (all negative) and +100% (all positive) — the larger the absolute value, the stronger the emotion. This is only a coarse tendency judgement based on a word list; it does not handle irony, negation or contextual semantics, so it is suitable for first-pass screening of batches of articles rather than a verdict on a single item. Both the text and the results stay in the local browser and are never uploaded.",
        "📖 View the usage guide for 'Simple Sentiment Polarity Analysis (Word Frequency)'",
        "Polarity index = (positive hits - negative hits) ÷ (positive hits + negative hits) × 100%",
        "Text to analyse (paste news, posts or comments)",
        "The experience of this newly launched product is very good, the performance is stable, the price is affordable, the customer service attitude is professional, the logistics is fast, and it is worth recommending.",
        "Analyse sentiment tendency",
        "📚 Deep Dive: Dictionary-Based Analysis of Sentiment Polarity",
        "Paste a batch of posts, comments or short news items and use the built-in word list to count positive and negative word hits, yielding the overall polarity index first.",
        "During crisis handling, paste the text for each time window separately and compare the polarity index and negative word composition of the two to judge whether public opinion is easing or worsening.",
        "When first-screening a batch of articles, look only at the negative word list: samples with dense negatives concentrated on words such as 'refund', 'delay' and 'perfunctory' should be prioritised for manual review.",
        "Reading of a positive article",
        "A 36-character experience comment 'the experience is very good, the performance is stable, the price is affordable, the customer service attitude is professional, the logistics is fast, worth recommending' hits positive words 6 times and negative words 0 times, so the polarity index = (6 - 0) ÷ (6 + 0) = 100.00%, with a sentiment word density of 16.67%, judged as a positive tendency.",
        "Negative word composition in a complaint post",
        "A 45-character complaint 'lagging and malfunctions, the customer service attitude is perfunctory, the logistics was delayed by two days, the refund was also slow, the experience is very poor, not worth it at all' hits negative words 8 times distributed across different aspects (quality, service, logistics, after-sales, value for money), giving a polarity index of -100.00%. Such samples negative across multiple dimensions deserve higher priority than single-point complaints.",
        "Why not look only at the polarity index",
        "Two texts may both have a polarity index close to 0, but in one the positive and negative words each hit 5 times (controversial content with two opposing sides), while in the other nothing is hit at all (a neutral statement with no emotion). So the sentiment word density must be examined together; when the density is very close to 0 the conclusion is unreliable and the text should be read manually or analysed with a more complete model.",
        "Can this method replace a professional",
        "model?",
        "No. The dictionary method does no word segmentation or syntactic analysis, cannot handle negation (such as 'not good'), irony or contextual semantics, and cannot recognise new internet words outside the dictionary. Its value lies in zero dependency, offline operation and results in seconds, making it suitable for coarse screening of large sample batches and for ranking before manual review; the final verdict must still consider context.",
        "Does a polarity index of 0 mean neutral?",
        "Not necessarily. It only means the positive and negative word hits are equal. If both are large the content is controversial; if both are 0 then no sentiment word was matched and the conclusion is untrustworthy. In that case read it together with the 'sentiment word density' and, when the density is too low, recommend manual review.",
        "What about domain words not in the dictionary?",
        "This tool uses a fixed word list and does not support customisation. Industry-specific expressions (such as 'claim rejection' in insurance clauses) are missed if they are not in the list. In that case treat the result as a reference, manually re-check against your own business word list, or choose a professional tool that supports custom dictionaries.",
        "Can English content be used?",
        "The total word count adds Chinese characters and English words, but the built-in word list only covers Chinese, so sentiment words in English are not counted. For pure English or mixed Chinese-English text where the emotion is mainly expressed in English, the result will be clearly low; it is recommended to translate to Chinese first and then count.",
        "About 'Simple Sentiment Polarity Analysis (Word Frequency)'",
        "Simple Sentiment Polarity Analysis (Word Frequency). A free online tool processed entirely in the browser, no data uploaded, privacy and security protected.",
        "Paste the text whose sentiment tendency you want to judge",
    ]))

    write('media-invite', build('media-invite', [
        "📚 Media Invitation Tracking",
        "Media invitation list management and status tracking",
        "📖 View the usage guide for 'Media Invitation Tracking'",
        "Add media",
        "Media name",
        "Media type",
        "Newspaper/magazine",
        "Online media",
        "Radio",
        "Contact",
        "Export list",
        "📚 Deep Dive: Media Invitation Tracking",
        "Before a launch or an event, build a media list (TV/online/print/radio/self-published) and track the status of each (invited/confirmed/attended/declined).",
        "Close to the event date, check whether the 'confirmation rate' meets the target and follow up a second time with media stuck at 'invited' for a long time.",
        "After the event, tally the 'attendance rate' to accumulate the arrival quality of each media type and optimise the list structure next time.",
        "Tracking criteria",
        "Each media record contains: name, contact, type (TV/online/print/radio/self-published), status (invited / confirmed / attended / declined). Entries can be dynamically added, removed and re-statused; progress is summarised in real time from the status distribution.",
        "The loaded sample list has 10 entries: 4 confirmed (CCTV, Xinhua, Sina Finance, Tencent News), 2 attended (People's Daily, Economic Observer), 3 invited (Phoenix TV, CBN, Jiemian News), 1 declined (CNR). Confirmation rate = 4÷10 = 40%, attendance rate = 2÷10 = 20%. If the target confirmation rate is ≥60%, the current gap is clear and the 3 'invited' media need chasing; the declined broadcast entry can be backfilled with a replacement.",
        "Is a large gap between confirmation rate and attendance rate normal?",
        "Common. Media that 'confirm attendance' often drop out at the last minute due to sudden assignments, so the attendance rate is usually below the confirmation rate. This tool separates the two precisely to expose this funnel — if the confirmation rate is 40% but the attendance rate only 20%, then even confirmations are unreliable and replacements plus an online live stream backup are needed.",
        "Can statuses be customised, e.g. 'rescheduled' or 'pending editor approval'?",
        "The four built-in statuses (invited/confirmed/attended/declined) cover the mainstream funnel. If you need finer statuses (such as under approval or rescheduled), you can extend the status enumeration on the data yourself; the summary logic of this tool counts by enumeration value, so it keeps working after extension.",
        "About 'Media Invitation Tracking'",
        "Media Invitation Tracking is an online tool in the marketing and promotion field. A marketing analysis tool that helps quantify and evaluate marketing effect and ROI.",
        "e.g. Xinhua Net",
        "Reporter name",
    ]))

    write('risk-assessment', build('risk-assessment', [
        "📋 Risk Assessment",
        "PR event risk assessment, probability x impact matrix analysis",
        "'PR event risk assessment, probability x impact matrix analysis' performs a professional calculation from the input parameters and outputs the result.",
        "📖 View the usage guide for 'Risk Assessment'",
        "Add risk item",
        "Risk description",
        "Probability of occurrence (1-5)",
        "Degree of impact (1-5)",
        "Risk matrix",
        "Risk list",
        "Risk assessment method:",
        "Risk value = probability (1-5) × impact (1-5). 1-6 is low risk, 7-12 is medium risk, 13-19 is high risk, and 20-25 is extreme risk. Contingency plans are recommended for items above high risk.",
        "📚 Deep Dive: Risk Assessment",
        "For a single risk point (such as a project delay or a compliance gap), estimate the probability (1~5) and the impact (1~5) separately, and derive and grade the risk value by probability × impact.",
        "Assess the same risk once before and once after measures are taken, to see how the intervention pushes the risk value down from 'extreme' to 'medium'.",
        "Arrange multiple risk points into a list and sort them by risk value descending, so the top ones are handled first.",
        "Scoring criteria",
        "Probability (1~5, 1 extremely unlikely, 5 extremely likely) × impact (1~5, 1 minor, 5 catastrophic); risk value = probability × impact. Levels: ≤6 low, ≤12 medium, ≤19 high, >19 extreme. Defaults are probability 3 and impact 3 (i.e. 9, medium risk).",
        "By default 3 × 3 = 9, judged medium risk. If both probability and impact rise to 5: 5 × 5 = 25, judged extreme and requiring immediate handling or escalation. If it is only low probability and low impact: 1 × 2 = 2, judged low risk, which can be folded into routine monitoring without a separate plan. The three tiers (2/9/25) cover exactly the low/medium/extreme tiers, making it easy to demonstrate the non-linear amplification of risk as both dimensions rise together.",
        "If both probability and impact are 5 giving a risk value of 25, does it definitely happen?",
        "No. 25 only represents the risk level when 'probability and impact are both judged as the highest' — a reminder that 'the consequence is severe and very likely', not a prediction that it will definitely occur. Whether it happens also depends on whether you intervene afterwards; this tool exists precisely to quantify the 'high level before intervention' and drive you to push it down.",
        "What is the difference from the 'Event Risk Assessment' tool?",
        "This tool provides a general qualitative and quantitative probability × impact assessment for single or multiple discrete risk points; the scoring dimensions are simple and it suits a quick list. 'Event Risk Assessment' specifically batch-builds a matrix for the 5 event risk categories (safety/financial/reputation/operational/legal). The former is general, the latter is scenario-specific, and they can be used together: first grade each point with this tool, then run the event version for the specific scenario.",
        "About 'Risk Assessment'",
        "Risk Assessment is an online tool in the marketing and promotion field. A marketing analysis tool that helps quantify and evaluate marketing effect and ROI.",
        "e.g. guest cancels at the last minute",
    ]))

    write('analysis-assessor', build('analysis-assessor', [
        "📋 Sponsorship (Project/Evaluation/Return) Analysis",
        "Sponsorship project evaluation and return estimation",
        "📖 View the usage guide for 'Sponsorship (Project/Evaluation/Return) Analysis'",
        "Enter one 'benefit item, media valuation, actual investment' per line. Sponsorship ROI = (total media value - total investment) ÷ total investment × 100%; the single-item ROI is computed item by item on the same basis. It also gives the net return and the highest-value benefit item, for sponsorship decisions and closing reviews.",
        "Sponsorship benefit data (one line per 'benefit item, media valuation, actual investment')",
        "Naming rights,300000,150000\nOn-site booth,100000,60000",
        "Evaluate return",
        "📚 Deep Dive: Sponsorship Project Evaluation and Return Estimation",
        "Before approving a sponsorship, the brand side estimates the media valuation and investment of each benefit item,",
        "to judge whether it is worth investing.",
        "At sponsorship closing, tally the actual media value and investment, output the net return and single-item ROI for review and renewal negotiation.",
        "Compare the ROI of several sponsorship schemes to select the benefit combination with the highest return.",
        "Worked example: return of four benefit items",
        "Entering 'naming rights,800000,300000; on-site booth,250000,120000; media exposure,420000,150000; social communication,180000,60000', the total media value is 1650000.00, total investment 630000.00, net return 1020000.00, sponsorship ROI 161.90%, judged as a high return.",
        "Where does the media valuation come from?",
        "It is usually estimated from the equivalent advertising list price, CPM converted from impressions, or a third-party monitoring report; this tool only does the aggregation and the",
        "ROI calculation",
        ", so the valuation basis must be determined by you.",
        "What ROI counts as good?",
        "The tool splits it into three tiers of 100%, 50% and 0%: ≥100% is a high return, 50%~100% is a good return, 0%~50% is basically break-even, and below 0 is not break-even.",
        "How is a benefit item with zero investment handled?",
        "The single-item ROI requires division by the investment; when the investment is 0 that item's ROI shows as 0.00%, so please fill in the real investment amount.",
        "About 'Sponsorship (Project/Evaluation/Return) Analysis'",
        "Sponsorship (Project/Evaluation/Return) Analysis. A free online tool processed entirely in the browser, no data uploaded, privacy and security protected.",
        "Naming rights,800000,300000",
    ]))

    write('press-conference', build('press-conference', [
        "📢 Press Conference Run of Show",
        "Automatic generation of a press conference run-of-show timetable",
        "📖 View the usage guide for 'Press Conference Run of Show'",
        "Press conference start time",
        "Press conference type",
        "Product launch",
        "Press briefing",
        "Annual summary meeting",
        "📢 Generate run of show",
        "+ Add segment",
        "Export run of show",
        "📚 Deep Dive: Press Conference Run of Show",
        "When preparing a press conference, choose a template (product/media/annual meeting) or customise it, and fill in the name, duration (minutes), content and owner for each segment to generate the run of show.",
        "Back-calculate the start time from the total duration: when the end deadline is known, use the total duration to work out what time each segment should start.",
        "When reusing the same template for multiple events, fine-tune a segment duration to see whether the total still fits the venue's time slot.",
        "Scheduling criteria",
        "The run of show = a number of segments, each containing name / duration (minutes) / content description / owner; total duration = the sum of the segment durations; default start time 14:00. Segments can be moved up/down, deleted, or loaded from a template (product contains 10 segments: sign-in 30, warm-up 5, hosting 5, leader remarks 10, product launch 20, product demo 15, guest speech 15, media Q&A 20, group photo 5, tea break 30).",
        "Applying the product launch template: the ten segment durations sum to 30+5+5+10+20+15+15+20+5+30 = 155 minutes (about 2 hours 35 minutes). Starting at the default 14:00, it ends at an expected 16:35, which falls within a conventional half-day venue slot. If it needs to be compressed to within 2 hours, the tea break 30 and the guest speech 15 can be cut (saving 45 minutes → 110 minutes), but that sacrifices the interaction and media lead-capture segments, so a trade-off is needed.",
        "Are the durations in the template hard standards?",
        "No. The template gives reference values for common industry pacing; in practice it should be adjusted for guest schedules, venue transitions, live stream signal switching and so on. The value of this tool is to structure 'segment - duration - owner', so the total duration is summed in real time and the start time can be back-calculated, avoiding overruns caused by scheduling from experience alone.",
        "Why look at the total duration separately instead of only the segment count?",
        "The number of segments can be the same while the durations differ greatly (e.g. ten 5-minute segments versus ten 20-minute segments). Media Q&A, tea breaks and demos are often duration black holes; this tool lists the durations explicitly and sums them precisely to expose these 'invisible big items', making it easier to cut or parallelise them.",
        "About 'Press Conference Run of Show'",
        "Press Conference Run of Show is an online tool in the marketing and promotion field. A marketing analysis tool that helps quantify and evaluate marketing effect and ROI.",
    ]))

    write('index', build('index', [
        "📢 PR and Communication Tools",
        "PR and Communication",
        "PR and Communication Tools",
        "Sponsorship (Project/Evaluation/Return) Analysis",
        "The sponsorship project evaluation and return analysis tool quantifies sponsorship effect across project influence, media value and return dimensions, suitable for brand sponsorship decisions and ROI estimation.",
        "The sentiment polarity word frequency analysis tool performs word frequency statistics and simple positive/negative sentiment discrimination on text, outputting high-frequency words and tendency, suitable for public opinion monitoring and preliminary judgement of communication effect.",
        "The press conference run-of-show tool automatically generates the timetable and segment arrangement of a press conference by type, supports custom addition and deletion, and suits event planning and on-site execution checklists.",
        "The event risk assessment tool quantifies event risk levels with a probability (1-5) x impact (1-5) matrix and outputs high-priority items, suitable for contingency planning for launches, roadshows and similar events.",
        "A full-chain score of corporate social responsibility (CSR) projects from project design and communication strategy through to effect evaluation, covering five dimensions: social value, stakeholders, communication strategy, sustainability and the evaluation system.",
        "A full-chain assessment of KOL (key opinion leader) collaboration, covering five dimensions: follower scale and quality, content creation ability, brand fit, interaction performance and return on investment.",
        "The PR effect evaluation system quantifies communication effect across five dimensions - media coverage, volume, sentiment tendency, key message penetration and crisis response - producing a professional evaluation report.",
        "A systematic assessment of corporate brand reputation covering five dimensions - brand awareness, public trust, crisis resilience, stakeholder relations and online reputation - helping formulate reputation improvement strategies.",
        "A structured score of the whole PR event process from planning through execution to evaluation, covering six dimensions: goal setting, budget management, audience analysis, channel strategy, execution quality and effect evaluation.",
        "The risk assessment tool scores multiple PR event risks with a probability x impact matrix and derives the average risk value and level, suitable for quantifying event contingency plans and crisis management.",
        "The media invitation tracking tool manages media lists and invitation status (sent/replied/attended), supports loading samples and progress statistics, and suits invitation coordination for launches and media events.",
        "The press release keyword density analysis tool counts keyword frequency and distribution in the article, flags stuffing risk, and suits PR copywriting SEO and readability optimisation.",
        "About 'PR and Communication Tools'",
        "This PR and Communication Tools collection includes 12 free online tools covering the common calculation, conversion and lookup needs of PR and communication scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find ready-to-use practical tools here. All tools run purely in the front end, data is not uploaded to the server, and privacy and security are protected.",
        "The PR and communication tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common PR and communication tasks without memorising complex formulas or converting manually; just input and you get the result.",
        "Do the PR and Communication Tools need a download or registration?",
        "No. All PR and Communication Tools on this page are pure front-end online tools. Open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
        "Are the calculation results of the PR and Communication Tools accurate? Is the data secure?",
        "The tools compute locally in your browser from public mathematical formulas and common industry standards, so results are available instantly. All computation happens locally on your device, data is never uploaded to the server, and privacy is well protected.",
    ]))


if __name__ == '__main__':
    main()
