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
    write('sas-assessment', build('sas-assessment', [
        "💭 SAS Anxiety Self-Assessment",
        "The SAS (Self-Rating Anxiety Scale, Zung 1971) has 20 items. Please answer based on your actual feelings over the \"past week\". The result is for self-understanding and reference only and is not a medical diagnosis.",
        "/ SAS Anxiety Self-Assessment",
        "📐 Scoring principle",
        "Rate each item 1-4 by how often the symptom appears: 1 = never or rarely, 2 = a small part of the time, 3 = a considerable part of the time, 4 = most or all of the time. Items 5, 9, 13, 17 and 19 are",
        "reverse-scored items",
        "(choosing 1 records 4 points, 2 records 3, 3 records 2, 4 records 1). Adding the 20 items gives a raw score of 20-80, and the standard score = raw score × 1.25 (rounded to an integer). Chinese norm reference: below 50 normal, 50-59 mild anxiety, 60-69 moderate anxiety, 70 or above severe anxiety.",
        "Self-Rating Anxiety Scale",
        "Question 1 / 20",
        "Loading...",
        "← Previous question",
        "Click the option text to answer; you can also use keys 1-4 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "SAS assesses your actual feelings over the \"past week\", not a single day or your whole life",
        "Items 5, 9, 13, 17 and 19 of the 20 are reverse-scored items (they are worded as a \"no anxiety\" state); the system flips them for you, so answer with your genuine feeling",
        "Each question has 4 levels from \"rarely\" to \"almost always\"; if unsure, pick the closest one",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "📚 Deep dive: SAS Anxiety Self-Assessment",
        "Anxiety tendency self-check: when you often feel inexplicably nervous, sweaty or restless, use it to judge whether your anxiety level has reached a range worth watching.",
        "Use it together with PHQ-9: anxiety and depression often appear together, and measuring both scales together reflects your recent mood state more completely.",
        "Before and after medication or counseling: retest the standard score after a period of intervention and see whether it has dropped.",
        "How the standard score is computed",
        "The 20 items give a raw score of 20-80, which multiplied by 1.25 and rounded yields a standard score of 25-100. Items 5, 9, 13, 17 and 19 are reverse items (the more \"never\" you experience the symptom, the higher the score recorded), which prevents habitual denial.",
        "Does a standard score above 50 mean I have an anxiety disorder?",
        "It is not a diagnosis. Chinese norms use 50 as the cutoff: 50-59 mild, 60-69 moderate, 70 or above severe. It only flags that the anxiety level is high; whether it amounts to a disorder has to be judged by a physician.",
        "Why is my score not low even though I \"rarely have symptoms\"?",
        "Most likely the reverse items were reverse-scored — this is how the scale is designed: people who are \"never\" nervous score high on reverse items, which is normal arithmetic.",
    ]))

    write('phq9-assessment', build('phq9-assessment', [
        "💭 PHQ-9 Depression Self-Assessment",
        "The PHQ-9 reference questionnaire scores 0-27. It is not a diagnostic scale; if the result is abnormal, please consult a professional.",
        "/ PHQ-9 Depression Self-Assessment",
        "The PHQ-9 (Patient Health Questionnaire depression scale, Kroenke et al. 2001) has 9 items that assess how often you have been bothered by the following feelings over the \"past two weeks\". Each item scores 0-3 (0 = not at all, 1 = several days, 2 = more than half the days, 3 = nearly every day), and adding the 9 items gives a total of 0-27. Reference bands: 0-4 none or very mild, 5-9 mild, 10-14 moderate, 15-19 moderately severe, 20-27 severe. Item 9 concerns thoughts of self-harm; if it scores 1 or more, a safety notice appears. Everything runs in the browser and no answer is uploaded.",
        "Depression Screening Scale",
        "Question 1 / 9",
        "Loading...",
        "← Previous question",
        "Click the option text to answer; you can also use keys 1-4 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "The PHQ-9 asks about the \"past two weeks\", not a single day or your whole life",
        "For each item pick one level by how often you were bothered, from \"not at all\" to \"nearly every day\"",
        "Item 9 concerns thoughts of self-harm; if you genuinely have such thoughts, be sure to read the safety notice in the result",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "📚 Deep dive: PHQ-9 Depression Self-Assessment",
        "Two-week mood screen: when you or someone close to you has had low mood, lost interest, or clear changes in sleep or appetite for more than two weeks, use it to judge the severity quickly.",
        "Follow-up during treatment: while you are in counseling or on medication, test yourself every few weeks and watch the trend of the total and of items 1 to 8.",
        "Self-awareness: when you cannot tell \"just feeling down\" apart from \"possibly depressed\", scoring the frequency 0-3 turns a vague feeling into a comparable number.",
        "A quick look at item 9 (self-harm) on its own",
        "Item 9 does not count toward the 0-27 total banding, but a score of 1 or more means thoughts of self-harm or of ending your life have appeared recently. The result section pops up an extra red notice, so please take it seriously and contact a professional or a helpline as soon as possible.",
        "Can the PHQ-9 replace a hospital diagnosis?",
        "No. It is an internationally used screening scale for flagging risk and tracking change; whether you meet the diagnostic criteria for depression requires a psychiatrist or psychologist to judge through a clinical interview.",
        "What total counts as \"severe\"?",
        "0-4 none or very mild, 5-9 mild, 10-14 moderate, 15-19 moderately severe, 20-27 severe. The higher the score, the denser the depressive symptoms over the past two weeks.",
        "How is it different from SAS (anxiety)?",
        "The PHQ-9 measures core \"depressive\" symptoms (low mood, interest, energy) while SAS measures core \"anxiety\" symptoms (tension, worry, physical restlessness). The two often co-occur, so testing them together makes sense.",
    ]))

    write('calc-12', build('calc-12', [
        "📋 Happiness Index Calculator",
        "Rate yourself 0-10 on each of the 10 life dimensions below to get a total happiness score and grade, with a radar chart of the dimensions.",
        "This tool uses a multidimensional subjective well-being self-rating framework: rate 10 dimensions — life, health, relationships, work, finances and so on — each 0-10, and add them up to a total of 0-100. A radar chart shows the distribution across dimensions, and the result is compared against a norm of about 62 points to judge your relative level and locate your weakest dimension. It is for self-awareness and trend tracking only, not a clinical diagnosis.",
        "💡 Total score 0-100 points; norm reference: 60 is moderate, 70+ is good, 80+ is fairly high. The radar chart makes weak dimensions easy to spot.",
        "This scale is a self-rated subjective well-being reference tool, not a clinical diagnosis",
        "0 means extremely dissatisfied or very poor, 10 means extremely satisfied or excellent",
        "Scores are affected by recent mood and events, so retest regularly to observe the trend",
        "A persistently low score, or any dimension below 4, is a sign to seek professional support",
        "📚 Deep dive: Happiness Index Calculator",
        "Life satisfaction review: score your current life across ten dimensions (such as positive mood, relationships, health and finances) to find what is dragging you down the most.",
        "Compare with the norm: the result section gives the norm mean as a reference so you can see whether you are above or below average, avoiding the illusion that \"everyone else is doing better than me\".",
        "Goal setting: take the two or three lowest-scoring dimensions as next quarter's priorities, then retest in six months to see the change.",
        "How to read the radar chart",
        "Each dimension is 0-10, and the fuller the ten-sided radar chart, the more balanced your overall well-being. The norm of 62 points is the overall reference line; sitting clearly below it with one dimension collapsed usually marks the weak spot worth fixing first.",
        "How is happiness different from mood?",
        "Mood is a momentary emotion, while happiness is a relatively stable subjective evaluation of life shaped by several long-term dimensions, so this test measures it across all ten dimensions together.",
        "Does a low score mean my life has failed?",
        "No. It is only a snapshot of how you feel right now and is strongly influenced by recent events. Treat it as a dashboard for adjusting your life, not as a judgement.",
        "About \"Happiness Index Calculator\"",
        "The subjective well-being index assessment tool covers 10 dimensions — life, health, relationships, work, finances and more — computing a total score and a happiness grade, comparing them with the norm and visualizing each dimension with a radar chart.",
        "Self-rating 0-10 across 10 dimensions",
        "Total score and happiness grade",
        "Norm comparison",
        "Radar chart visualizing weak spots",
        "Personal well-being self-assessment",
        "Periodic tracking of psychological state",
        "Team or organizational happiness survey",
        "Reference for improving quality of life",
    ]))

    write('psqi-assessment', build('psqi-assessment', [
        "😴 Sleep Quality Self-Assessment (PSQI)",
        "19 scored items on a 0-3 scale, where a higher score means worse sleep quality, on a 0-21 scale.",
        "PSQI sleep self-assessment",
        "/ Sleep Quality Self-Assessment",
        "The PSQI assesses sleep over the \"past month\" through 7 components, each scored 0-3: (1) subjective sleep quality, (2) sleep latency (take the higher of the frequency and the minute score), (3) actual sleep duration, (4) sleep efficiency (actual sleep ÷ time in bed), (5) sleep disturbance (sum of 7 interference types), (6) hypnotic medication, (7) daytime functioning. Adding the 7 gives a global score of 0-21: 5 or below is fairly good sleep, 6-10 a mild to moderate problem, 11-15 a clear problem, 16-21 a serious problem. Everything runs in the browser and no data is uploaded.",
        "Pittsburgh Sleep Quality Index",
        "Question 1 / 17",
        "Loading...",
        "← Previous question",
        "Answer based on your real situation by clicking an option or filling in a value; you can also use keys 1-4 / ← →",
        "Question number overview (click any number to go back and change that answer)",
        "⚠️ Before you start",
        "The PSQI assesses your overall sleep over the \"past month\", not a single night",
        "Answer the time-related items based on your usual routine; for the frequency items pick one level from \"none\" to \"3 or more nights a week\"",
        "Item 13 (other reasons) is recorded only and is not scored",
        "Your progress is stored only in this local browser. Click \"Restart test\" to clear it; no data is uploaded",
        "Restart test",
        "📚 Deep dive: PSQI Sleep Self-Assessment",
        "Full sleep assessment: when you \"sleep badly\" but cannot say what is wrong, use the 7 components to locate whether it is slow sleep onset, frequent waking or low efficiency.",
        "Preparing for an insomnia clinic visit: bring your PSQI result for the past month to the appointment so the doctor can judge your sleep structure quickly.",
        "Evaluating medication or behavioural treatment: measure once before and once after the intervention and compare the change in the global score and in individual components.",
        "What each of the 7 components means",
        "Component 1 subjective quality, 2 sleep latency, 3 sleep duration, 4 sleep efficiency (actual sleep ÷ time in bed), 5 sleep disturbance, 6 sleep medication, 7 daytime function, each 0-3 for a total of 0-21. A score of 5 or more suggests poor sleep quality.",
        "How is sleep efficiency computed?",
        "Use \"actual hours asleep ÷ total hours in bed × 100%\". For example, lying in bed for 8 hours and sleeping only 6 gives an efficiency of 75%, which lowers the score of component 4.",
        "Why can a long time in bed cost you points?",
        "Because lying a long time without falling asleep lowers sleep efficiency. It is a reminder that when you cannot sleep you are better off getting up than staying in bed.",
    ]))

if __name__ == '__main__':
    main()
