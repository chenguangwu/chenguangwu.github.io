#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'psychology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'psychology')
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
    out = {'slug': slug, 'industry': 'psychology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('index', build('index', [
        "💭 Psychological Counseling Tools",
        "Psychological counseling",
        "Psychological counseling tools",
        "Generates a keyword word cloud by philosophical school with a list of representative works, with adjustable font size and color scheme, useful for teaching guided tours and reading notes, generated entirely in the browser.",
        "Optimism Index Calculator (Self-Rating Scale)",
        "Evaluates personal optimism based on a revised Life Orientation Test (LOT-R) with 6 core items (3 optimistic and 3 pessimistic), 1-5 points each, giving an optimism index. Pessimistic items are reverse-scored; the total runs from 6 to 30.",
        "Rate yourself 0-10 on each of the 10 life dimensions to get a total happiness score and grade, with a radar chart of the dimensions.",
        "Cognitive Bias Cards Random Display randomly draws and presents the definition and case of a common cognitive bias (such as anchoring and confirmation bias), suitable for psychology study and bias self-checking.",
        "SCL-90 Mental Health Self-Rating Scale",
        "A complete 90-item online SCL-90 symptom self-rating tool. It uses the 5-level scale 1 none / 2 very mild / 3 moderate / 4 fairly severe / 5 severe and automatically computes the total score, mean score, number of positive items, number of negative items and the mean positive symptom score, ...",
        "Adult Attachment Style Test (ECR)",
        "Adult attachment describes the pattern of emotional bonding an individual forms in intimate relationships. The ECR (Experiences in Close Relationships) scale characterizes this on two orthogonal dimensions: anxiety (worry about being ...",
        "Big Five Personality Test (15 facets, 28 types)",
        "A 60-item online Big Five (Big Five / OCEAN) assessment. The five main dimensions have 12 items each and the 15 facets have 4 items each; reverse scoring is handled automatically and converted to T scores with mean 50 and standard deviation 10; weighted Euclidean distance is used in a 2...",
        "Holland Career Interest Test (RIASEC)",
        "John Holland's career interest theory groups personality and work environment into six types: Realistic R, Investigative I, Artistic A, Social S, Enterprising E and Conventional C. This assessment has 60 items (10 per type) and rates each as \"like / ...",
        "The Perceived Stress Scale (PSS-10) is an internationally used stress assessment tool. Its 10 items evaluate how stressful life has felt over the past month, 0-4 points each, for a total of 0-40.",
        "The Emotional Intelligence (EQ) self-report questionnaire is based on Goleman's five-element EQ model and assesses emotional intelligence across 5 dimensions: self-awareness, self-management, self-motivation, empathy and social skills, with 4 items per dimension for 20 items in total.",
        "Enneagram Personality Test",
        "Each group has two descriptions; pick the one closer to you. It reveals your dominant type, wing, tri-center and the dynamic shift under stress versus security, and draws a nine-pointed star chart.",
        "MBTI Personality Type Test",
        "A full MBTI (Myers-Briggs Type Indicator) test: 60 questions across 4 dimensions (E/I extraversion-introversion, S/N sensing-intuition, T/F thinking-feeling, J/P judging-perceiving), 5 options per question (strongly agree / somewhat agree / neutral / ...",
        "The VARK learning style test uses 12 scenario questions to assess your learning preference: Visual (V), Auditory (A), Read/Write (R) and Kinesthetic (K), helping you find the way of learning that suits you best.",
        "The Procrastination Assessment Scale is adapted from the General Procrastination Scale (GPS) and quantifies procrastination through self-rating on 10 common procrastination scenarios. Please answer based on what actually happened in the last 2 weeks.",
        "A simplified Pittsburgh Sleep Quality Index (PSQI) assessing sleep quality over the past month, 0-3 points for each of 7 dimensions, 0-21 total, where a higher score means worse sleep quality.",
        "The Personality Color Analysis (four-color model) tool computes the red, blue, yellow and green shares and the dominant personality from your answers, suitable for team building, self-awareness and communication style assessment.",
        "Which Milk Tea Are You",
        "12 situational multiple-choice questions spanning four hidden dimensions of sweetness, strength, ice level and toppings, matching you with the cup that fits you best and generating a shareable result card.",
        "PHQ-9 Depression Self-Assessment",
        "The PHQ-9 (Patient Health Questionnaire depression scale, Kroenke et al. 2001) has 9 items that assess how often you have been bothered by the following feelings over the \"past two weeks\". Each item scores 0-3 (0 = not at all, 1 = several days, 2 = more than half the days, 3 = nearly every day), 9...",
        "PSQI Sleep Self-Assessment",
        "The PSQI assesses sleep over the \"past month\" through 7 components, each 0-3 points: (1) subjective sleep quality, (2) sleep latency (take the higher of the frequency and the minute score), (3) actual sleep duration, (4) sleep efficiency (actual sleep ÷ time in bed), (5) sleep disturbance (sum of 7 interference types) ...",
        "SAS Anxiety Self-Assessment",
        "Rate each item 1-4 by how often the symptom appears: 1 = never or rarely, 2 = a small part of the time, 3 = a considerable part of the time, 4 = most or all of the time. Items 5, 9, 13, 17 and 19 are reverse-scored (choosing 1 records 4 points, choosing 2 records 3 ...",
        "About \"Psychological Counseling Tools\"",
        "This collection gathers 20 free online tools covering the common calculations, conversions and lookups that come up in psychological counseling. Whether you are a practitioner, a student or an ordinary user, you will find practical ready-to-use mini tools here. Every tool runs entirely in the browser, no data is uploaded to a server, and your privacy is protected.",
        "The psychological counseling tools collected on this page include (a few representative ones):",
        "These tools help you finish common psychological-counseling tasks quickly, with no need to memorize complex formulas or convert anything by hand — type and you get the result.",
        "Do the psychological counseling tools need a download or registration?",
        "No. Every tool on this page is a pure front-end online tool: open the page and start using it. No software to install, no account to register, and no data is uploaded.",
        "Are the results accurate? Is the data safe?",
        "The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are instant. All computation happens on your own device, no data is uploaded to a server, and your privacy is fully protected.",
    ]))

    write('self-test-pressure', build('self-test-pressure', [
        "🎚️ Perceived Stress Self-Rating Scale (PSS)",
        "The Perceived Stress Scale (PSS-10) is an internationally used stress assessment tool. Its 10 items evaluate how stressful life has felt over the past month, 0-4 points each, for a total of 0-40.",
        "PSS-10 (Perceived Stress Scale) has 10 items assessing perceived stress over the \"past 1 month\". Each item is rated 0-4 by frequency (0 = never, 1 = occasionally, 2 = sometimes, 3 = fairly often, 4 = very often). Items 4, 5, 7 and 8 are reverse-scored (choosing 4 records 0, 3 records 1, 2 records 2, 1 records 3, 0 records 4, flipped automatically). Adding the 10 items gives a total of 0-40: 0-13 low stress, 14-19 moderate/normal, 20-26 fairly high, 27-40 high stress. Everything runs in the browser and no answer is uploaded.",
        "Perceived Stress Scale",
        "Question 1 / 10",
        "Loading...",
        "← Previous question",
        "Click the option text to answer; you can also use keys 1-5 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "PSS assesses your perceived stress over the \"past 1 month\", not a single day or your whole life",
        "Items 4, 5, 7 and 8 of the 10 are reverse-scored and the system flips them for you, so answer with your genuine feeling",
        "Each question has 5 levels from \"never\" to \"very often\"; if unsure, pick the closest one",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "PSS-10 is an internationally used perceived stress scale",
        "Items 4, 5, 7 and 8 are reverse-scored",
        "0-13 low stress, 14-19 moderate, 20-26 fairly high, 27-40 high stress",
        "A high score suggests psychological stress may be present, but it does not mean a mental illness",
        "📚 Deep dive: Perceived Stress Self-Rating Scale (PSS)",
        "Workload self-check: when overtime runs back to back and deadlines pile up, use this to confirm whether your sense of loss of control has climbed and plan rest ahead of time.",
        "Before an exam or project: measure once before a big exam or during a project sprint to tell \"healthy tension\" apart from \"sustained high pressure\" instead of pushing through blindly.",
        "Chronic stress tracking: run it at a fixed time each month and watch the trend of the total to judge whether your life rhythm is out of balance.",
        "Understanding reverse-scored items",
        "Items 4, 5, 7 and 8 are reverse-scored: the more you feel you \"can stay in control and cope calmly\", the lower the score. This cancels out blind optimism so the total reflects your real stress more closely.",
        "Does PSS measure stressful events or the feeling of stress?",
        "It measures \"your subjective sense of stress and loss of control over the past month, not the number of objective events\". The same event feels very different to different people.",
        "Does a high score always mean I need medical help?",
        "Not necessarily. A high score means stress is on the high side and needs managing; but if it comes with persistent insomnia, emotional breakdown or physical discomfort, seek professional help.",
        "How do I choose between the 10-item and 14-item versions?",
        "This test uses the most widely used 10-item version (PSS-10), which covers both the sense of loss of control and coping efficacy and is already enough for self-screening.",
        "About \"Perceived Stress Self-Rating Scale (PSS)\"",
        "PSS-10 (Perceived Stress Scale) is an internationally used stress assessment tool. Ten questions assess how stressful life has felt over the past month, with a total of 0-40 points, helping identify your stress level and offering stress-relief advice.",
        "The PSS-10 standard scale",
        "Reverse items handled automatically",
        "4-level stress grading",
        "Stress-relief suggestions generated",
        "Self-assessment of stress level",
        "Evaluating stress management effectiveness",
        "Workplace health monitoring",
    ]))

    write('rater', build('rater', [
        "⚖️ Sleep Quality Rating (Simplified PSQI)",
        "A simplified Pittsburgh Sleep Quality Index (PSQI) assessing sleep quality over the past month, 0-3 points for each of 7 dimensions, 0-21 total, where a higher score means worse sleep quality.",
        "This tool is a simplified version of the Pittsburgh Sleep Quality Index (PSQI) that evaluates sleep over the \"past 1 month\" across 7 dimensions: subjective quality, sleep latency, actual sleep, sleep efficiency, sleep disturbance, hypnotic medication and daytime function. Each dimension scores 0-3 for a total of 0-21, and a higher score means worse sleep quality (5 or more suggests a sleep deviation). Everything runs in the browser and no answer is uploaded.",
        "Total 0-5 good sleep quality, 6-10 average, 11-15 fairly poor, 16-21 very poor",
        "Sleep Quality Brief Rating (Simplified PSQI)",
        "Question 1 / 7",
        "Loading...",
        "← Previous question",
        "Click the option text to answer; you can also use keys 1-4 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "Please answer based on your real sleep over the \"past 1 month\", not a single day or your whole life",
        "The 7 dimensions score 0-3 each, 0-21 in total; a higher score means worse sleep quality",
        "This is a self-rating reference; 5 or more suggests a sleep deviation, but it is not a medical diagnosis",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "PSQI assesses sleep over the past month",
        "A total above 7 points is usually treated as the boundary for poor sleep quality",
        "A hypnotic medication score above 0 calls for attention to the risk of dependence",
        "This scale is for reference only and does not replace a professional sleep medicine diagnosis",
        "📚 Deep dive: Sleep Quality Rating (Simplified PSQI)",
        "Everyday sleep self-check: instead of filling in the full 19 items, use these 7 key dimensions to get a quick idea of roughly where your sleep quality sits.",
        "Evaluating sleep aids: after trying exercise, meditation or a schedule change, measure every other week and see whether the total drops.",
        "Shift workers and jet-lagged travelers: use it to monitor whether sleep has been drifting away from normal over the long term when your schedule is irregular.",
        "What are the 7 dimensions",
        "This test covers subjective quality, sleep latency, sleep duration, efficiency, disturbance, sleep medication and daytime function, 0-3 points each for 0-21 total. The closer to 0 the better; 5 or more suggests poor sleep quality and it is worth running the full PSQI.",
        "How does the simplified version differ from the full PSQI?",
        "The full version (psqi-assessment) has 19 items and 7 component scores; this simplified version asks about the 7 dimensions directly, which is faster but less detailed, so it suits everyday tracking.",
        "At what score should I see a doctor?",
        "A total of 5 or more usually suggests a deviation in sleep quality; if it comes with severe daytime sleepiness or mood impact, consider a sleep clinic or psychiatry visit.",
        "About \"Sleep Quality Rating (Simplified PSQI)\"",
        "PSQI (Pittsburgh Sleep Quality Index) is the international standard scale for assessing sleep quality. It evaluates 7 dimensions — subjective sleep quality, sleep latency, sleep duration, sleep efficiency, sleep disturbance, hypnotic medication and daytime function — for a total of 0-21 points.",
        "Standardized 7-dimension assessment",
        "4-level sleep quality grading",
        "Per-dimension score breakdown",
        "Sleep improvement suggestions",
        "Sleep quality self-test",
        "Insomnia screening",
        "Evaluating sleep treatment effectiveness",
        "Sleep hygiene education",
    ]))

if __name__ == '__main__':
    main()
