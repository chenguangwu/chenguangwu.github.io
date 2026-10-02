#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'gastroenterology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'gastroenterology')
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
    out = {'slug': slug, 'industry': 'gastroenterology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('intestinal-metaplasia', build('intestinal-metaplasia', [
        "\U0001F4CB Intestinal Metaplasia (Atrophy Extent) Assessor",
        "Based on the OLGIM staging system, assess the extent of gastric mucosal intestinal metaplasia and stratify gastric cancer risk.",
        "Intestinal Metaplasia Atrophy Extent Assessor",
        "/ Intestinal Metaplasia Assessment",
        "Gastric intestinal metaplasia OLGIM staging: determine stage 0 to IV from antral and body IM grades via a matrix lookup; OLGA is based on atrophy grading; stages III\u2013IV are high risk requiring endoscopic follow-up.",
        "Antral intestinal metaplasia degree (biopsy pathology)",
        "Antral intestinal metaplasia",
        "None (grade 0)",
        "Mild (grade 1)",
        "Moderate (grade 2)",
        "Severe (grade 3)",
        "Body intestinal metaplasia",
        "Atrophy degree (OLGA reference)",
        "Antral atrophy",
        "Body atrophy",
        "\U0001F4CB OLGIM staging matrix",
        "Antrum \\ Body",
        "None(0)",
        "Mild(1)",
        "Moderate(2)",
        "Severe(3)",
        "OLGIM is based on the degree of intestinal metaplasia and has better reproducibility than OLGA (which is based on atrophy degree). Both share the same staging matrix structure.",
        "\U0001F4CA Gastric cancer risk stratification",
        "OLGIM stage 0",
        ": no IM, gastric cancer risk extremely low, no special follow-up needed",
        "OLGIM stages I\u2013II",
        ": low risk, follow-up gastroscopy every 3 years",
        "OLGIM stage III",
        ": moderate risk, gastroscopy every 1-2 years recommended",
        "OLGIM stage IV",
        ": high risk (whole-stomach IM), annual gastroscopy recommended",
        "Note: OLGIM staging must be based on standard 5-point biopsy (antral lesser curvature, antral greater curvature, angle, body lesser curvature, body greater curvature). H. pylori positive patients should undergo eradication first. For clinical reference only.",
        "\U0001F4DA Deep Dive: Intestinal Metaplasia (Atrophy) OLGIM/OLGA Staging and Gastric Cancer Risk",
        "Atrophy staging: determine OLGIM stage from antral/body intestinal metaplasia and atrophy extent",
        "Risk stratification: gastric cancer risk rises markedly at stages III-IV, strengthening follow-up",
        "Follow-up decision: set gastroscopy intervals by stage (3 years / 1~2 years / annually)",
        "Algorithm: OLGIM matrix = [[0,1,1,2],[1,1,2,2],[1,2,2,3],[2,2,3,3]] (rows = antral IM 0~3, columns = body IM 0~3); the homologous OLGA matrix follows atrophy extent. Stage 0 extremely low risk, I low (3 years), II moderate (1~2 years), III-IV high (annually); H. pylori eradication is advised in all cases.",
        "Example: antral IM grade 2, body IM grade 3 \u2192 OLGIM[2][3] = stage III, high risk; annual gastroscopy plus biopsy after H. pylori eradication is advised. If antrum and body both show no IM or atrophy (0,0) \u2192 OLGIM[0][0] = stage 0, extremely low risk, needing only health maintenance follow-up and H. pylori eradication (if positive).",
        "What is the difference between OLGIM and OLGA?",
        "OLGIM is based on metaplasia extent and OLGA on atrophy extent; both share the same staging matrix structure. Clinically they are often combined: OLGA more sensitively reflects atrophy, while OLGIM relates more directly to gastric cancer risk, with stages III-IV marking high risk.",
        "Can intestinal metaplasia be reversed?",
        "Mild intestinal metaplasia can partly regress after H. pylori eradication, but moderate-to-severe is mostly irreversible. The point is not reversal but surveillance \u2014 high-risk stages need periodic gastroscopy plus biopsy to detect dysplasia and early cancer in time.",
        "About the Intestinal Metaplasia Atrophy Extent Assessor",
        "The Intestinal Metaplasia (atrophy extent) assessor, based on the OLGIM and OLGA staging systems, stratifies gastric cancer risk from the degree of atrophy and intestinal metaplasia in antral and body biopsies." + DISCL_M,
    ]))
    write('mayo-score', build('mayo-score', [
        "\U0001FA7B Ulcerative Colitis Mayo Score Tool",
        "Mayo scoring system assessing ulcerative colitis (UC) disease activity, total 0-12 points.",
        "Ulcerative Colitis Mayo Score Tool",
        "/ Mayo Score",
        "\U0001F4D6 View the Ulcerative Colitis Mayo Score Usage Guide",
        "Mayo score = sum of stool frequency + rectal bleeding + endoscopic findings + physician assessment (each 0 to 3), max 12; the partial Mayo score excludes endoscopy (0 to 9); <2 remission, 3\u20135 mild, 6\u201310 moderate, 11\u201312 severe.",
        "Stool frequency (increase over normal)",
        "1-2 more per day than normal",
        "3-4 more per day than normal",
        "5 or more per day than normal",
        "Rectal bleeding",
        "Trace blood streaks in stool",
        "Obvious bloody stool",
        "Predominantly blood",
        "Endoscopic findings",
        "Normal or no activity",
        "Mild inflammation (erythema, reduced vascular pattern)",
        "Moderate inflammation (marked erythema, absent vascular pattern, erosions)",
        "Severe inflammation (spontaneous bleeding, ulcer formation)",
        "Physician global assessment",
        "\U0001F4CB Mayo scoring criteria",
        "Stool frequency",
        "+1~2/day",
        "+3~4/day",
        "+\u22655/day",
        "Trace blood streaks",
        "Mild inflammation",
        "Moderate inflammation",
        "Severe inflammation",
        "Mayo score = sum of the 4 items (0-12 points). Mayo endoscopic subscore = endoscopic findings alone (0-3 points).",
        "Remission (\u22642 points)",
        ": clinical remission, maintenance therapy, periodic monitoring",
        "Mild (3-5 points)",
        ": oral 5-ASA plus topical therapy may suffice",
        "Moderate (6-10 points)",
        ": active treatment needed, consider steroids or biologics",
        "Severe (11-12 points)",
        ": may need hospitalization, IV steroids, biologics, or surgical evaluation",
        "Endoscopic remission definition: Mayo endoscopic subscore = 0. Deep remission definition: clinical remission + endoscopic remission.",
        "Note: The modified Mayo score (excluding physician global assessment, 0-9 points) is commonly used for clinical trial endpoint assessment. The Mayo score can also monitor treatment response, with clinical response defined as a score drop \u22653 points and \u226530% reduction. For clinical reference only.",
        "\U0001F4DA Deep Dive: Ulcerative Colitis Mayo Score",
        "Activity assessment: compute 0~12 points from the 4 items of stool frequency, rectal bleeding, endoscopy, and physician assessment",
        "Treatment stratification: remission/mild/moderate/severe correspond to 5-ASA/steroids/biologics/hospitalization",
        "Remainder definition: endoscopic remission and deep remission are near-term treatment goals",
        "Algorithm: stool frequency (normal/+/1~2/+/3~4/+\u22655 counts 0~3), rectal bleeding (none/trace/obvious/predominantly blood 0~3), endoscopy (normal/mild/moderate/severe 0~3), physician assessment (normal/mild/moderate/severe 0~3), summed to a Mayo total of 0~12; partial Mayo = stool frequency + rectal bleeding + physician assessment. \u22642 remission, 3~5 mild, 6~10 moderate, >10 severe.",
        "Example: stool frequency 2, rectal bleeding 2, endoscopy 2, physician 2 \u2192 total 8, moderate activity (\u226410); systemic steroids or biologic evaluation is advised. If all items score 1 \u2192 total 4, mild activity (\u22645), oral 5-ASA plus topical suffices. If all score 3 \u2192 total 12, severe activity (>10); hospitalization, IV steroids, and switching to cyclosporine/infliximab if no response in 48~72h are advised.",
        "What is the partial Mayo score used for?",
        "The partial Mayo excludes the endoscopy item, enabling quick outpatient assessment and avoiding frequent colonoscopy, and is often used in clinical trials and remote follow-up; but determining endoscopic remission must rely on the complete Mayo (with endoscopy).",
        "Does Mayo \u22642 mean cured?",
        "Mayo \u22642 with each item \u22641 is traditionally defined as clinical remission, but deep remission additionally requires no endoscopic activity (endoscopic subscore 0). Symptom-only remission with ongoing endoscopic inflammation has a high relapse rate, so treatment targets should point to endoscopic/histologic remission.",
        "About the Ulcerative Colitis Mayo Score Tool",
        "The Ulcerative Colitis Mayo Score Tool computes the Mayo score from four indicators \u2014 stool frequency, rectal bleeding, endoscopic findings, and physician global assessment \u2014 to assess UC disease activity." + DISCL_M,
        "How to use the Ulcerative Colitis Mayo Score Tool",
        "What does the Ulcerative Colitis Mayo Score Tool do?",
        "The Ulcerative Colitis Mayo Score Tool. Enter the 4 clinical and endoscopic subscores to aggregate a 0\u201312 point Mayo score, determine activity, and define endoscopic/deep remission, for IBD assessment, for medical reference only.",
        "How to use the Ulcerative Colitis Mayo Score Tool?",
        "Which scenarios suit the Ulcerative Colitis Mayo Score Tool?",
    ]))

if __name__ == '__main__':
    main()
