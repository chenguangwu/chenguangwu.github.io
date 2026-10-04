#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'service')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'service')
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
    out = {'slug': slug, 'industry': 'service', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('complaint-analysis', build('complaint-analysis', [
        '📊 Complaint Classification Analysis',
        'Enter complaint text and classify it, automatically counting the issue type distribution, word frequency and handling priority',
        '/ Complaint Analysis',
        '📖 View the Complaint Classification Analysis user guide',
        'Complaint classification: each line of complaint text is matched to a category by the keyword library of quality, logistics, service and returns; the category share = the number of items in that category ÷ total items × 100%; frequent words are taken in descending order of frequency, top N; handling priority is sorted by share × severity weight, for customer service review and process improvement.',
        'Count',
        '📚 In-depth analysis: Complaint Classification Analysis',
        'Complaint categorisation: paste several lines of complaint text and the tool matches each line against preset keywords for logistics, quality, service, price and after-sales, automatically categorising them and counting the number and share of each type.',
        'Improvement focus: the classification coverage indicator identifies uncategorised other complaints, and frequent words with stop words removed reveal new pain points, so the keyword library can be iterated.',
        'Daily report generation: output the number and share of each complaint type plus the top 20 word frequencies, ready for quality meetings and supplier or logistics accountability.',
        'Worked example: classifying 6 complaint texts',
        'Default word library: logistics covers delivery, express, dispatch, slow, delay and arrival; quality covers quality, broken, damaged, defect and faulty; service covers attitude, agent and ignored; price covers expensive, price increase, price and charge; after-sales covers refund, return and repair. Entering 6 lines: the express is too slow and the logistics information is not updated, giving logistics; the product quality has flaws, giving quality; the agent attitude is poor and nobody responds, giving service; the price is too expensive, giving price; the refund process is troublesome and a return is requested, giving after-sales; and feeling down today, giving other. Result: logistics 1, quality 1, service 1, price 1, after-sales 1, other 1, so classification coverage = (6-1)/6 ≈ 83%, meaning 5 of 6 complaints were categorised effectively.',
        'Can the classification keywords be customised?',
        'Yes. The page provides a keyword input box; fill it in the format category:word1,word2;category2:word… to override the default library, adapting to different business scenarios such as e-commerce, SaaS or physical stores.',
        'What does a low classification coverage mean?',
        'Coverage = (total complaints − the number of uncategorised other items) ÷ total complaints. A low value means many complaints did not hit any keyword, so the library should be extended or frequent other samples distilled into a new category, continuously improving automatic classification.',
        'About Complaint Analysis',
        'Enter one complaint per line\ne.g. delivery was too slow, it took three days to arrive',
    ]))

    write('csat-score', build('csat-score', [
        '📋 CSAT Customer Satisfaction Score',
        'Enter the number of ratings at each star level to calculate the CSAT score, satisfaction distribution and NPS trend reference automatically',
        'Core formulas (by input variables): s.count÷maxCount×100; s.count÷total×100',
        '/ CSAT Score',
        '📖 View the CSAT Customer Satisfaction Score user guide',
        '📚 In-depth analysis: CSAT Customer Satisfaction Score',
        'Satisfaction accounting: enter the number of ratings at each star level from 1 to 5 and the tool works out CSAT, the share of 4 and 5 stars, NPS, promoters minus detractors, the average star rating and the grade.',
        'Service rating: a grade is given by the CSAT thresholds of 90 or above excellent, 75 or above good, 50 or above pass and otherwise needs improvement, combined with the detractor share to judge whether rectification should be triggered.',
        'Trend comparison: compute the star distribution of different periods, this month versus last month, separately to quantify the improvement in service, supporting KPI appraisal and team incentives.',
        'Worked example: 100 ratings, 5 stars 50, 4 stars 30, 3 stars 12, 2 stars 5, 1 star 3',
        'Total ratings 100; satisfied, 4 plus 5 stars, = 80 → CSAT = 80.0%, good; promoters at 5 stars = 50% → NPS = 50% − detractors at 1 plus 2 stars, 8%, = 42; average star rating = (3×1 + 5×2 + 12×3 + 30×4 + 50×5)/100 = 4.19; detractor share 8.0%. Conclusion: satisfaction is good, but 8% detractors remain, so a root cause analysis of the negative tickets is recommended.',
        'What is the difference between CSAT and NPS?',
        'CSAT measures satisfaction, the share of 4 and 5 stars, and looks at the overall experience; NPS measures loyalty, promoters minus detractors, and looks at repeat purchase and word of mouth. This tool shows both on the same screen: in the example above CSAT = 80% and NPS = 42.',
        'What thresholds is the grade based on?',
        'CSAT of 90 or above is excellent, 75 or above good, 50 or above pass and below 50 needs improvement. The example at 80% falls in the good band; if the detractor share exceeds 20%, an additional warning of negative word-of-mouth risk appears.',
        'About CSAT Score',
    ]))

    write('response-time', build('response-time', [
        '🎧 Customer Service Response Time Statistics',
        'Enter ticket response and resolution times to calculate the average response time, resolution rate and key SLA indicators such as P50, P90 and P99 automatically',
        'Core formulas (by input variables): Math.max.apply(null,counts)||1; counts[i]÷maxCount×100',
        '/ Response Time',
        '📖 View the Customer Service Response Time Statistics user guide',
        '📚 In-depth analysis: Customer Service Response Time Statistics',
        'Routine service quality monitoring: paste or import the response durations in minutes of N tickets, set the SLA target of 30 minutes by default, and the tool automatically works out the average response, the SLA compliance rate and the P50, P90 and P99 percentiles.',
        'Weekly and monthly reports: combined with resolution durations, work out the average resolution time and resolution rate, and show the response distribution intuitively with a histogram binned at 0-5, 5-15, 15-30, 30-60 and 60+ minutes, ready for reporting upwards.',
        'Exception troubleshooting: when P90 far exceeds the SLA, locate the long-tail tickets, for example responses of 35 and 45 minutes against the 30-minute threshold, and optimise shift scheduling or the escalation mechanism to raise the overall compliance rate.',
        'Worked example: 8 built-in tickets with an SLA of 30 minutes',
        'Ticket response durations of 5, 12, 25, 3, 45, 8, 35 and 15 minutes, one of them unresolved. Calculated: 8 tickets in total, 7 resolved, resolution rate 87.5%; average response 18.5 minutes; 6 tickets responded to within 30 minutes, giving an SLA compliance rate of 75.0%; percentiles P50 = 13.5 minutes, P90 = 38.0 minutes, P99 = 44.3 minutes; average resolution time 115.7 minutes. Conclusion: most tickets meet the target, but the P90 and P99 long tail of 35 and 45 minutes drags the compliance rate down, so overdue tickets need priority attention.',
        'How is the SLA compliance rate calculated?',
        'Compliance rate = the number of tickets whose response time is at or below the SLA target ÷ total tickets. In this example the SLA is 30 minutes and 6 of 8 tickets are within 30 minutes, with 45 and 35 minutes over, so the rate is 75.0%.',
        'What are the P90 and P99 response percentiles for?',
        'P90 means 90% of tickets are responded to faster than that value, and P99 means 99% are faster than that value. They measure the long-tail experience and expose a few extremely slow responses better than the average, making them key indicators for SLA governance.',
        'About Response Time',
    ]))

    write('script-template', build('script-template', [
        '🎧 Customer Service Script Template Picker',
        'Draw standard customer service scripts at random by scenario, ready to copy and use, covering common service scenarios',
        '/ Script Template',
        '📖 View the Customer Service Script Template Picker user guide',
        'Script template structure: scenario, covering pre-sales enquiry, return or exchange and complaint handling, times stage, from greeting to confirming the problem, explaining the solution, handling objections and closing; the variables to fill in are the order number, product name and time frame; the response must empathise before giving a solution and promising unauthorised terms is forbidden; used for new-hire training and response standards.',
        '📚 In-depth analysis: Customer Service Script Template Picker',
        'New agent training: copy the standard opening greeting script with one click, for example "Hello, welcome to customer service, how may I help you?", quickly establishing a professional first impression and avoiding being lost for words.',
        'Complaint soothing: when a customer is upset, use the apology and reassurance category, for example "We are very sorry for the bad experience; we completely understand how you feel and will do our utmost to solve the problem for you", empathising first and then handling, to reduce confrontation.',
        'Refunds and after-sales: after confirming a refund, use the refund and after-sales category, for example "Your refund request has been accepted and the money will be returned to your payment account within 3-5 ',
        'working days',
        '", stating the time frame clearly to reduce follow-up questions and chasing.',
        'Example: filtering scripts by category',
        'The tool has 18 built-in scripts in 6 categories with 3 in each: opening greeting, apology and reassurance, problem handling, refunds and after-sales, information confirmation and closing farewell. Selecting the apology and reassurance category returns 3 scripts, such as "We deeply apologise for the trouble caused…" and "So sorry to have kept you waiting…", and clicking any one copies it; switching to the refunds and after-sales category shows the corresponding refund timing scripts, covering every node of the service process.',
        'What categories are the scripts divided into?',
        'Six categories with 18 scripts: opening greeting, apology and reassurance, problem handling, refunds and after-sales, information confirmation and closing farewell, covering every node from reception to wrap-up, and you can switch categories by key or drop-down to locate them quickly.',
        'Can the scripts be customised?',
        'This tool provides generic script templates that you can copy and then fine-tune to your business; if you want to build a proprietary script library over the long term, maintain it in your internal knowledge base, since applying scripts rigidly can irritate customers.',
        'About Script Template',
    ]))

    write('ticket-priority', build('ticket-priority', [
        '📋 Ticket Priority Sorting',
        'Build a priority matrix from urgency and importance, sort automatically and visualise the distribution',
        '/ Ticket Priority',
        '📖 View the Ticket Priority Sorting user guide',
        '📚 In-depth analysis: Ticket Priority Sorting',
        'Inbound triage: enter urgency from 1 to 5 and importance from 1 to 5 for a new ticket, and the tool computes the priority score as urgency × importance; the higher the score, the sooner the ticket is handled.',
        'Shift scheduling: sort pending tickets in descending order of score and assign them to online agents first, so that high-urgency, high-importance tickets are not buried in a low-score queue.',
        'Escalation decision: tickets reaching a threshold, for example 20 or above, are flagged automatically as high priority, triggering supervisor involvement or dedicated follow-up to protect the experience of core customers.',
        'Worked example: scoring three types of ticket',
        'Priority score = urgency × importance, both integers from 1 to 5. General enquiry: urgency 3 × importance 4 = 12 points; core customer outage: urgency 5 × importance 5 = 25 points, the highest; low-priority feedback: urgency 1 × importance 2 = 2 points, the lowest. Handle them in descending order from 25 to 12 to 2, to make sure the most critical ticket is answered first.',
        'How is the priority score calculated?',
        'Priority score = urgency × importance on a 1-5 scale. The product makes tickets that are both high urgency and high importance score clearly higher than those high on a single dimension: for example 5×5 = 25 is far above 5×1 = 5, giving stronger sorting discrimination.',
        'How should urgency and importance be valued?',
        'Urgency reflects how pressing the problem is for the customer, so an outage ranks above an enquiry; importance reflects the business impact, so a core customer ranks above a long-tail one. The team should agree on one scoring standard, so that subjective bias does not distort the ordering.',
        'About Ticket Priority',
    ]))


if __name__ == '__main__':
    main()
