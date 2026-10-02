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
    write('self-assess', build('self-assess', [
        "📋 Emotional Intelligence (EQ) Self-Report Questionnaire",
        "The Emotional Intelligence (EQ) self-report questionnaire is based on Goleman's five-element EQ model and assesses EQ across 5 dimensions — self-awareness, self-management, self-motivation, empathy and social skills — with 4 items per dimension for 20 items in total.",
        "This questionnaire is based on Goleman's five-element EQ model: self-awareness, self-management, self-motivation, empathy and social skills, with 4 items per dimension for 20 items in total. Each item is self-rated on 5 levels from \"never\" to \"always\", 1-5 points each, for a total of 0-100; the per-dimension levels and your weakest areas are also given. Everything runs in the browser and no answer is uploaded.",
        "Emotional Intelligence (EQ) Self-Assessment",
        "Question 1 / 20",
        "Loading...",
        "← Previous question",
        "Click the option text to answer; you can also use keys 1-5 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "Please answer based on your real behaviour over \"the past while\", not how you wish things were",
        "Each question has 5 levels from \"never\" to \"always\"; 4 questions per dimension, 20 questions in total",
        "This is a self-rating reference; a high score does not make you a \"winner at life\", it only characterizes one kind of emotional ability",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "The EQ assessment is based on Goleman's five-element model",
        "Please answer based on real behaviour, not on how you wish things were",
        "A total above 80 counts as high EQ, above 60 as fairly high",
        "EQ can be improved through deliberate training",
        "📚 Deep dive: Emotional Intelligence (EQ) Self-Report Questionnaire",
        "Workplace communication review: after friction with a colleague or client, use it to locate your weaker dimension (such as \"emotion regulation\" or \"empathy\").",
        "Intimate relationships: use the \"relationship management\" and \"self-awareness\" scores to understand your own reaction patterns in close interactions.",
        "Team management: managers can use the five dimensions to spot the weak spots in team atmosphere and improve them in a targeted way.",
        "Understanding the five dimensions",
        "This test splits EQ into self-awareness, emotion regulation, motivation, empathy and relationship management, 4 items each. The result section lists your total score and your weakest dimension, so you can work on the right thing.",
        "Is a low EQ a personality problem that cannot be changed?",
        "No. EQ is a skill rather than a fixed personality trait; both self-awareness and regulation improve through deliberate practice, and the scale simply helps you find where to start.",
        "What counts as a high total score?",
        "Each of the 20 questions is worth 1-5 points for a maximum of 100. 80 or above is high EQ, 60-79 fairly high, 40-59 moderate, below 40 leaves room to improve; these are self-rating reference bands.",
        "About \"Emotional Intelligence (EQ) Self-Report Questionnaire\"",
        "The Emotional Intelligence (EQ) self-report questionnaire is based on Goleman's five-element EQ model and assesses EQ level across 5 dimensions — self-awareness, self-management, self-motivation, empathy and social skills — with 20 items in total and a score from 0 to 100.",
        "20-item assessment across 5 dimensions",
        "Independent scoring per dimension",
        "Weakest dimension detection",
        "EQ self-assessment",
        "Leadership development reference",
        "Interpersonal communication self-test",
        "Personal growth planning",
    ]))

    write('calc-self-assess', build('calc-self-assess', [
        "📋 Optimism Index Calculator (Self-Rating Scale)",
        "Evaluates personal optimism based on a revised Life Orientation Test (LOT-R) with 6 core items (3 optimistic and 3 pessimistic), 1-5 points each, giving an optimism index. Pessimistic items are reverse-scored; the total runs from 6 to 30.",
        "This tool is based on the revised Life Orientation Test (LOT-R). The 6 items are self-rated on 5 levels from \"strongly disagree\" to \"strongly agree\", 1-5 points each; items 3 and 6 are pessimistic reverse items that the system flips automatically. Adding the 6 items gives a total of 6-30: higher means more optimistic, lower means more pessimistic. Everything runs in the browser and no answer is uploaded.",
        "Optimism Tendency Scale",
        "Question 1 / 6",
        "Loading...",
        "← Previous question",
        "Click the option text to answer; you can also use keys 1-5 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "Please answer with your genuine thoughts over \"the past while\"; there are no right answers",
        "Items 3 and 6 of the 6 are reverse items (they are worded pessimistically); the system flips the scoring automatically, so just pick what you truly feel",
        "Each question has 5 levels from \"strongly disagree\" to \"strongly agree\"",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "LOT-R is an internationally used scale for assessing optimistic and pessimistic tendencies",
        "Items 3 and 6 are reverse-scored (the more you disagree, the higher the score)",
        "Optimism is not blind optimism; moderate optimism supports physical and mental health",
        "Scores are for reference only and do not constitute a psychological diagnosis",
        "📚 Deep dive: Optimism Index Calculator (Self-Rating Scale)",
        "Mindset baseline: to find out whether you lean toward an optimistic or pessimistic explanatory style, locate it quickly with these 6 items.",
        "Stress readiness: measure once before a major change (new job, exam preparation); a higher optimism level usually recovers faster.",
        "Health behaviour reference: research links an optimistic tendency to better health behaviour, so this can serve as a starting point for self-awareness.",
        "Why items 3 and 6 are scored backwards",
        "Items 3 and 6 are worded pessimistically (for example \"I rarely expect good things to happen\"). If you \"agree\", that actually means you are more pessimistic, so they are reverse-scored to keep the logic that a higher total means more optimistic, avoiding a contradiction.",
        "Is optimism innate or trainable?",
        "Roughly 25% is heritable, but explanatory style can be adjusted. For example, viewing a setback as \"temporary and local\" is a trainable optimism technique.",
        "How should I read the total score?",
        "Each of the 6 items is worth 0-4 points, and after reversing the reverse items the total runs 0-24. 24 or above is highly optimistic, 18-23 moderate, 12-17 somewhat pessimistic, below 12 highly pessimistic; for reference only.",
        "About \"Optimism Index Calculator (Self-Rating Scale)\"",
        "The optimism index calculator is based on LOT-R (the revised Life Orientation Test) and assesses your optimistic or pessimistic tendency through 6 core items, with a total of 6-30 points, helping you understand your own optimism level.",
        "The standardized LOT-R scale",
        "Reverse scoring handled automatically",
        "4 levels of optimism tendency",
        "Interpreting the assessment result",
        "Self-test for optimistic and pessimistic tendency",
        "Positive psychology research",
    ]))

    write('assessor', build('assessor', [
        "📋 Procrastination Level Assessment",
        "The Procrastination Assessment Scale is adapted from the General Procrastination Scale (GPS) and quantifies procrastination through self-rating on 10 common procrastination scenarios. Please answer based on what actually happened in the last 2 weeks.",
        "This tool follows the approach of the General Procrastination Scale (GPS), using 10 common procrastination scenarios to assess your behavioural tendency over the \"past 2 weeks\". Each item is rated 0-4 by frequency (never → always). Adding the 10 items gives a total of 0-40: the higher the score, the heavier the procrastination. Everything runs in the browser and no answer is uploaded.",
        "Procrastination Behaviour Assessment",
        "Question 1 / 10",
        "Loading...",
        "← Previous question",
        "Click the option text to answer; you can also use keys 1-5 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "Look back at what really happened in the \"past 2 weeks\"; do not choose how you wish things were or how you behaved once in a while",
        "Each question has 5 levels from \"never\" to \"always\"; if unsure, pick the closest one",
        "This is a self-rating reference; a high score only means the procrastination tendency is clear and is not a clinical diagnosis",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "Please answer based on what actually happened in the last 2 weeks, not on how you wish things were",
        "The procrastination score is for reference only and is not a clinical diagnosis",
        "Below 10 no obvious procrastination, 11-20 mild, 21-30 moderate, 31-40 severe",
        "If severe procrastination is affecting daily functioning, consider seeking professional help",
        "📚 Deep dive: Procrastination Level Assessment",
        "Work procrastination self-check: when you keep pushing important tasks to the last minute and survive on deadlines, use it to quantify how often that happens.",
        "Study procrastination: students can use it to spot the \"I wanted to study but kept scrolling my phone\" pattern and find its trigger.",
        "Before and after comparison: after using time management or the Pomodoro technique, retest a month later and see whether the score drops.",
        "Procrastination is not laziness",
        "Procrastination usually stems from anxiety about the task, perfectionism or an unclear goal rather than plain laziness. These 10 items cover typical patterns such as \"avoidance, last-minute work and self-blame\", helping you tell an ability problem from an emotional one.",
        "Does a high score mean I definitely have procrastination disorder?",
        "This is a self-rating screen that flags a high procrastination frequency; real \"procrastination disorder\" that impairs functioning has to be judged together with how much your life is damaged, so do not force a label on yourself.",
        "How do I improve it?",
        "Breaking big tasks into small pieces, lowering the threshold to start, and using the \"just start for 5 minutes\" technique all work better than forcing yourself through sheer willpower.",
        "About \"Procrastination Level Assessment\"",
        "The Procrastination Assessment Scale is adapted from the General Procrastination Scale and quantifies procrastination through self-rating on 10 common procrastination scenarios, helping identify procrastinating behaviour and offering improvement advice.",
        "Standardized 10-item assessment",
        "4-level severity grading",
        "Procrastination behaviour self-assessment",
        "Time management ability self-test",
        "Psychological counseling aid",
    ]))

    write('analysis-2', build('analysis-2', [
        "🎨 Personality Color Analysis (Four-Color Model)",
        "Four-color model",
        "Personality color assessment",
        "Question 1 / 24",
        "Loading...",
        "← Previous question",
        "Pick the option closest to you for each question; you can also use keys 1-4 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "The 4 options of each question map to one personality color: red / blue / yellow / green. Choose the one closest to you",
        "There are no right answers; go with your first instinct and pick the most natural option instead of thinking about what you \"should\" choose",
        "Most people are a \"mix of colors\"; the result gives the share of all four colors and your dominant color",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "📚 Deep dive: Personality Color Analysis (Four-Color Model)",
        "Interpersonal communication: knowing whether you lean red (action) or blue (detail) lets you adjust how you speak and cut down friction.",
        "Team pairing: use members' dominant colors when forming teams — red + yellow suits charging ahead, blue + green suits holding steady and coordinating.",
        "Self-awareness: 24 scenario questions show your dominant and secondary colors, so you can understand the motives behind your behaviour.",
        "What each color stands for",
        "Red = forceful (result-oriented, direct); Blue = perfect (detail-oriented, rule-following); Yellow = lively (enthusiastic, people-oriented); Green = peaceful (stable, conflict-avoiding). The dominant color decides your main outward style, and the secondary color is the supplement.",
        "Do personality colors change?",
        "The dominant color is relatively stable, but the secondary color and the specific expression shift across life stages and environments. It is a thinking tool, not a fatalistic label.",
        "How is it different from MBTI or the Big Five?",
        "FPA uses four colors for an intuitive personality portrait and is easy for everyday use; MBTI gives 16 cognitive preference types and the Big Five gives continuous scores on 5 dimensions. They look at different angles and complement each other.",
        "About \"Personality Color Analysis (Four-Color Model)\"",
        "Personality Color Analysis (the FPA four-color model) uses 24 scenario multiple-choice questions to measure the share of your red, blue, yellow and green personality colors and gives your dominant color and core drive. It is widely used for self-awareness, team building and communication style optimization.",
        "24 scenario multiple-choice questions, answered one at a time",
        "Visualized share of the four colors red / blue / yellow / green",
        "Automatic detection of dominant and secondary color",
        "Progress saved locally, retest any time",
        "Self-awareness and personality exploration",
        "Teamwork and communication optimization",
        "Understanding differences in romance and parenting",
        "Training and corporate culture building",
    ]))

if __name__ == '__main__':
    main()
