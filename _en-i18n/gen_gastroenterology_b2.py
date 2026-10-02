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
    write('capsule-endoscopy', build('capsule-endoscopy', [
        "\u26A1 Capsule Endoscopy (Intestinal Transit Time) Calculator",
        "Compute gastric transit time and small-bowel transit time to assess intestinal motility function.",
        "Capsule Endoscopy Bowel Transit Time Calculator",
        "/ Capsule Endoscopy Transit Time",
        "Capsule swallow time",
        "Time of reaching duodenum",
        "Time of reaching ileocecal valve",
        "Capsule expulsion time",
        "Capsule already expelled",
        "Using prokinetic (metoclopramide)",
        "Compute transit time",
        "\U0001F4CB Normal reference ranges",
        "Gastric transit time (GTT)",
        "<60 minutes",
        "Prolongation indicates delayed gastric emptying",
        "Small-bowel transit time (SBTT)",
        "180-360 minutes",
        "Prolonged/shortened indicates dysmotility",
        "Total bowel transit time",
        "<8 hours (usually expelled)",
        ">8 hours suggests possible constipation",
        "Examination completion rate",
        "Reaching the ileocecal valve counts as complete",
        "Failure to reach the ileocecal valve counts as incomplete",
        "An overly short SBTT may lower the detection rate of small-bowel lesions. Studies show SBTT is inversely correlated with capsule completion rate.",
        "\U0001F4CA Influencing factors",
        "Factors prolonging gastric transit time",
        "Diabetes (autonomic neuropathy)",
        "Scleroderma / systemic lupus erythematosus",
        "Hypothyroidism",
        "Opioids, anticholinergic drugs",
        "Parkinson disease",
        "Strategies to raise the completion rate",
        "Adequate bowel preparation (polyethylene glycol + simethicone)",
        "Swallow the capsule lying on the right side",
        "Prokinetics (metoclopramide) can shorten GTT",
        "Real-time monitoring, use a magnet-guided capsule if needed",
        "New-generation capsules with longer battery life",
        "Note: Capsule endoscopy completion rate is about 80-90%. A prolonged GTT shortens the available SBTT window and affects distal small-bowel examination. An unexpelled capsule needs abdominal X-ray confirmation; retention beyond 2 weeks requires evaluation for surgical retrieval. For clinical reference only.",
        "\U0001F4DA Deep Dive: Capsule Endoscopy Gastric/Small-Bowel Transit Time Assessment",
        "Small-bowel examination quality: derive GTT and SBTT from swallow, duodenal arrival, and ileocecal arrival times",
        "Gastroparesis screening: a prolonged GTT indicates impaired gastric emptying",
        "Lesion detection rate assessment: an overly short SBTT may affect distal small-bowel reading",
        "Algorithm: convert times to minutes (HH:MM); gastric transit time GTT = duodenal arrival \u2212 swallow; small-bowel transit time SBTT = ileocecal arrival \u2212 duodenal arrival. GTT \u226460 min normal, 61~90 min mildly prolonged, >90 min clearly prolonged (gastroparesis); SBTT 180~360 min normal, <180 min too short (affects detection), 361~480 min prolonged, >480 min clearly prolonged; total bowel transit >480 min suggests possible constipation.",
        "Example: swallow at 08:00, duodenum at 08:25, ileocecal valve at 11:30 \u2192 GTT 25 min (normal), SBTT 185 min (normal, good detection rate). If swallowed at 08:00, duodenum only at 10:00, ileocecal valve at 14:00 \u2192 GTT 120 min (clearly prolonged, suggesting gastroparesis), SBTT 240 min (normal); gastric emptying function should be evaluated and a prokinetic used.",
        "Why is a too-short SBTT actually undesirable?",
        "An SBTT that is too short (<180 min) means the capsule did not dwell in the small bowel long enough, so the distal small bowel, especially the terminal ileum, is under-imaged and small ulcers, vascular malformations, or early tumors may be missed. Reading must be especially careful; repeat examination or switch to enteroscopy if necessary.",
        "Is it a problem if the capsule is never expelled?",
        "If expulsion is still unconfirmed after 48~72 hours, an abdominal X-ray should confirm whether it is retained. The vast majority pass in stool; with known small-bowel stricture or a history of retention there is a risk of capsule impaction requiring preoperative evaluation.",
        "About the Capsule Endoscopy Bowel Transit Time Calculator",
        "The Capsule Endoscopy Bowel Transit Time Calculator computes gastric and small-bowel transit times from the capsule swallow time, duodenal arrival time, and expulsion time, aiding assessment of bowel motility." + DISCL_M,
    ]))
    write('cdai', build('cdai', [
        "\U0001F9EE Crohn's Disease CDAI Activity Index Calculator",
        "Crohn's Disease Activity Index, computed from a 7-day diary record to assess Crohn's disease activity.",
        "Crohn's Disease CDAI Activity Index Calculator",
        "/ CDAI Calculator",
        "\U0001F4D6 View the CDAI Usage Guide",
        "Crohn's disease activity index CDAI = weighted sum of clinical variables (stool frequency, abdominal pain, general well-being, complications, antidiarrheal use, abdominal mass, hematocrit, weight); <150 remission, 150\u2013220 mild, 220\u2013450 moderate, >450 severe.",
        "Loose stool count (7-day total)",
        "Abdominal pain total score (7 days, 0-3/day)",
        "General well-being total score (7 days, 0-4/day)",
        "Number of complications (0-4 items)",
        "Days on antidiarrheals (0-1)",
        "Abdominal mass (0=none, 2=questionable, 5=definite)",
        "Hematocrit Hct (male %, female %)",
        "Male (standard 42%)",
        "Female (standard 37%)",
        "Weight deviation from standard (%)",
        "Compute CDAI",
        "\U0001F4CB CDAI composition",
        "7-day loose stool count",
        "Recorded daily, 7-day total",
        "7-day abdominal pain score total",
        "0=none, 1=mild, 2=moderate, 3=severe",
        "7-day general well-being score total",
        "0=good, 1=slightly below par, 2=poor, 3=very poor, 4=extremely poor",
        "Number of complications",
        "Arthritis, erythema nodosum, oral ulcers, iritis, etc.",
        "Antidiarrheal use",
        "0 or 1 (used within 7 days)",
        "Abdominal mass",
        "0=none, 2=questionable, 5=definite",
        "Hct deviation",
        "Male: 42-Hct, Female: 37-Hct",
        "Weight deviation",
        "(standard weight - actual)/standard weight \u00d7 100",
        "CDAI = sum of all weighted products. Data is based on the 7-day diary card record.",
        ": clinical remission",
        ": mild activity",
        ": moderate activity",
        ": severe activity",
        "Clinical response definition: CDAI decrease \u226570 points (or \u226525% reduction while the absolute value remains <150). CDAI <150 is one of the criteria for clinical remission.",
        "Note: CDAI is the classic activity assessment tool for Crohn's disease but has a substantial subjective component. It is best judged together with endoscopy (SES-CD), imaging (MRE), and biomarkers (CRP, fecal calprotectin). For clinical reference only.",
        "\U0001F4DA Deep Dive: Crohn's Disease CDAI Activity Index",
        "Activity assessment: compute CDAI from the 7-day diary to separate remission / mild / moderate / severe activity",
        "Treatment response: recompute the score before and after treatment to judge whether induction of remission succeeded",
        "Follow-up stratification: promptly escalate therapy for moderate-to-severe activity (steroids / immunosuppressants / biologics)",
        "Algorithm: CDAI = loose stools\u00d72 + abdominal pain (0~10)\u00d75 + general well-being (0~10)\u00d77 + complications\u00d720 + antidiarrheal (>0 counts as 1)\u00d730 + abdominal mass (0/2/5)\u00d710 + (standard Hct \u2212 measured Hct)\u00d76 + weight deviation%\u00d71; standard Hct is 42 for men and 37 for women. Grading: <150 remission, 150~219 mild, 220~450 moderate, >450 severe.",
        "Example: female, 14 loose stools, abdominal pain 10, well-being 7, 1 complication, no antidiarrheal, no mass, Hct 35%, weight \u22125% \u2192 (37\u221235)=2 \u2192 CDAI = 28+50+49+20+0+0+12\u22125 = 154, mild activity. If male, 20 loose stools, abdominal pain 30, well-being 10, 2 complications, antidiarrheal used, mass 5, Hct 25%, weight 0% \u2192 (42\u221225)=17 \u2192 CDAI = 40+150+70+40+30+50+102 = 482, severe activity; hospitalization with active induction therapy is advised.",
        "Does CDAI <150 mean remission?",
        "CDAI<150 is traditionally defined as clinical remission, but it must be judged together with endoscopic mucosal healing (the current treatment target). Some patients develop fistulas or perianal disease while CDAI stays low and still need specialist evaluation, so follow-up must not be relaxed based on the score alone.",
        "Why use a 7-day diary?",
        "CDAI was designed around symptom frequency over 7 days (loose stool count, abdominal pain, etc.) to smooth single-day fluctuation and reflect overall activity. The more accurate the diary, the more reliable the score; short-term recall bias can overestimate or underestimate it.",
        "About the Crohn's Disease CDAI Activity Index Calculator",
        "The Crohn's Disease CDAI Activity Index Calculator computes the CDAI score from eight indicators: stool frequency, abdominal pain, general well-being, complications, antidiarrheal use, abdominal mass, hematocrit, and weight." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()
