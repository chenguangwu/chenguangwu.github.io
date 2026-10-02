#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pediatrics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pediatrics')
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
    out = {'slug': slug, 'industry': 'pediatrics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
# body for pediatrics b3: hfmd-course / hirschberg-test / mchat-autism / neonatal-jaundice / pediatric-anemia

def main():
    # hfmd-course (42)
    write('hfmd-course', build('hfmd-course', [
"Hand-Foot-Mouth Disease (Rash/Oral) Course Assessor",
"Assess HFMD severity and isolation period from rash distribution, oral lesions and neuro/respiratory signs",
"Core formula (by input): max(14-day,0)",
" / HFMD Course Assessor",
"Day of illness",
"Temperature (°C)",
"Rash distribution",
"Hand rash",
"Foot rash",
"Oral vesicles/ulcers",
"Buttock rash",
"Generalized rash",
"Severe warning signs (check present)",
"Assess condition",
"HFMD Staging (Health Ministry Guideline)",
"Stage 1 (rash stage)",
"Fever + hand/foot/mouth/buttock rash",
"Outpatient symptomatic care",
"Stage 2 (nervous-system involvement)",
"Poor spirits/lethargy/startle/limb tremor/weakness",
"Admit for observation, reduce intracranial pressure",
"Stage 3 (pre-cardiopulmonary failure)",
"Tachycardia/tachypnea/abnormal BP/clammy sweating",
"ICU, vasoactive drugs",
"Stage 4 (cardiopulmonary failure)",
"Pulmonary edema/hemorrhage/shock/heart failure",
"PICU, respiratory-circulatory support",
"Note: HFMD is caused by enteroviruses (EV71/CoxA16 etc.), most common under 5 years. EV71 infection tends to be severe. Days 1-4 are the key progression window; monitor warning signs closely. Isolation: 1 week after symptoms resolve (usually 2 weeks total). Non-itchy/painless rash needs no treatment; painful oral ulcers affecting feeding can use topical medication. EV71 vaccine effectively prevents severe disease. This tool is for clinical reference only.",
"In-Depth: HFMD Course",
"Typical rash",
"Neuro/cardiopulmonary warning",
"Isolation days",
"3 yo, day 2 rash",
"HFMD + buttock rash ≥2 sites, oral rash -> typical HFMD, day-2 rash peak, symptomatic care suffices.",
"Warning signs",
"Persistent high fever, startle, limb tremor, fast breathing/heart rate -> suspect severe (encephalitis/pulmonary edema), seek care immediately.",
"How long isolation?",
"About 1 week after symptoms resolve; usually infectious within 14 days of onset.",
"When to hospitalize?",
"Neuro or cardiorespiratory symptoms mean severe disease, need ICU monitoring.",
"About the Hand-Foot-Mouth Disease (Rash/Oral) Course Assessor",
"The HFMD (rash/oral) course assessor evaluates severity and isolation period from rash distribution, oral lesions and systemic symptoms. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # hirschberg-test (36)
    write('hirschberg-test', build('hirschberg-test', [
"Vision (Hirschberg) Eye-Alignment Assessor",
"Hirschberg (corneal light reflex) test judges deviation direction/angle to screen pediatric strabismus",
"Core formula (by input): offset×15",
" / Hirschberg Eye-Alignment Assessor",
"Fixating eye",
"Right eye",
"Left eye",
"Non-fixating eye reflex position",
"Centered (pupil center)",
"Toward nose",
"Toward temple",
"Upward",
"Downward",
"Reflex offset distance (mm)",
"Assess alignment",
"Hirschberg Corneal Light-Reflex Standard",
"Reflex offset",
"Deviation angle",
"Deviation type",
"Orthophoria (no strabismus)",
"Mild strabismus",
"Moderate strabismus",
"Severe strabismus",
"Very severe strabismus",
"Note: Hirschberg is a rough screen; exact angle needs prism + alternate cover test. Reflex toward nose = exotropia (outward turn); toward temple = esotropia (inward turn). Pediatric strabismus needs early detection/treatment; 3-6 years is the key window for amblyopia therapy. Types to rule out: congenital (within 6 months), accommodative esotropia (from hyperopia), intermittent exotropia. All strabismus children need cycloplegic refraction. This tool is for screening reference only.",
"In-Depth: Hirschberg Alignment",
"Corneal reflex deviation",
"Esotropia/exotropia",
"Reflex offset 2 mm ×15°/mm = 30°; toward temple -> esotropia, toward nose -> exotropia (moderate).",
"Offset <1.5 mm (<22.5°) -> mild, observe or optometric training.",
"Source of 15°/mm?",
"Corneal diameter ~11 mm corresponds to 22.5°; each mm offset ≈15° deviation, a rough estimate.",
"Confirm diagnosis?",
"Hirschberg is screening; exact angle relies on prism-cover/synoptophore.",
"About the Vision (Hirschberg) Eye-Alignment Assessor",
"The Hirschberg eye-alignment assessor judges deviation direction/degree by corneal light reflex to screen strabismus. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # mchat-autism (23)
    write('mchat-autism', build('mchat-autism', [
"Autism (M-CHAT) Screening Tool",
"M-CHAT-R/F screens autism spectrum disorder (ASD) risk in 16-30 month toddlers",
" / M-CHAT Autism Screener",
"Compute screening result",
"M-CHAT-R Scoring Criteria",
"No further assessment needed",
"Needs M-CHAT-R/F follow-up interview",
"Refer immediately for ASD diagnostic assessment",
"Note: M-CHAT-R is for 16-30 month toddlers. Critical items (2,5,12): if any fails, follow up even if total <3. Critical: 5 (responds to name), 2 (points to interest), 12 (imitates). Positive screen ≠ ASD diagnosis; confirm via ADOS/ADI-R. ASD core: social-communication deficit, stereotyped repetitive behavior, restricted interests. 18 and 24 months are recommended screening points. This tool is for screening reference only.",
"In-Depth: M-CHAT Autism Screening",
"20-item parent version",
"Critical items",
"Age adaptation",
"fail ≤2, no critical",
"≤2 of 20 failed and all critical items (eye contact/pointing etc.) passed -> low risk, routine follow-up.",
"Critical item failed",
"Any critical item failed or ≥3 failed -> moderate-high risk, refer for ADOS diagnostic assessment.",
"Critical items?",
"Includes eye contact, pointing, response to name; a single failure raises risk.",
"Screening is not diagnosis",
"M-CHAT is screening; positive needs professional diagnostic interview.",
"About the Autism (M-CHAT) Screening Tool",
"The M-CHAT-R/F screener, a modified checklist for toddlers, assesses ASD risk in 16-30 month children. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # neonatal-jaundice (40)
    write('neonatal-jaundice', build('neonatal-jaundice', [
"Newborn Jaundice (Hour-Specific Bilirubin) Curve Tool",
"Bhutani hour-specific bilirubin percentile curve: assess neonatal hyperbilirubinemia risk zones and phototherapy/exchange thresholds",
"Core formula (by input): min(100,(tsb÷(pct.p95×1.2))×100)",
" / Newborn Jaundice Curve Tool",
"Hours of life (h)",
"Total serum bilirubin TSB (mg/dL)",
"Birth weight (g)",
"High-risk factors (hemolysis/G6PD/sepsis)",
"Gestational age <38 weeks",
"Assess risk zone",
"Bhutani Risk-Zone Explanation",
"Clinical management",
"Low-risk zone",
"<40th percentile",
"No intervention, monitor follow-up",
"Low-intermediate zone",
"40th-75th percentile",
"Close monitoring",
"High-intermediate zone",
"75th-95th percentile",
"Consider phototherapy",
"High-risk zone",
">95th percentile",
"Phototherapy/exchange",
"Phototherapy & Exchange Indications (AAP 2022)",
"Hours of life",
"Phototherapy threshold (mg/dL)",
"Exchange threshold (mg/dL)",
"Note: high-risk factors include isoimmune hemolysis, G6PD deficiency, sepsis, cephalohematoma, breast-milk jaundice etc. Smaller gestation/weight -> lower phototherapy threshold. Kernicterus warning: lethargy, hypotonia, weak suck, high-pitched cry, opisthotonos. This tool is for clinical reference only.",
"In-Depth: Newborn Hour-Specific Bilirubin",
"Bhutani nomogram",
"Phototherapy/exchange thresholds",
"High-risk factors",
"48 h TSB 14 mg/dL, GA 38 wk: in 40-75 percentile; low-risk phototherapy threshold ≈12, needs phototherapy (14≥12).",
"High-risk threshold lower",
"Same value with GA <38 or high-risk: phototherapy threshold ≈10 mg/dL, intervene earlier.",
"When to exchange?",
"TSB exceeds exchange threshold (by hour/GA) or rises too fast; watch for kernicterus.",
"About the Newborn Jaundice (Hour-Specific Bilirubin) Curve Tool",
"The newborn hour-specific bilirubin (Bhutani) curve assessor uses hours of life and serum bilirubin to assign risk zones and guide phototherapy/exchange. A medical professional tool based on authoritative standards, for reference only.",
    ]))

    # pediatric-anemia (31)
    write('pediatric-anemia', build('pediatric-anemia', [
"Iron-Deficiency Anemia (Hb/Serum Ferritin) Assessor",
"By hemoglobin, serum ferritin, MCV etc., stratify by age to assess IDA severity and iron-supplement plan",
"Core formula (by input): weight×4; weight×2",
" / Iron-Deficiency Anemia Assessor",
"Hemoglobin Hb (g/L)",
"Serum ferritin SF (μg/L)",
"Preterm infant",
"Exclusive breastfeeding >6 mo without iron",
"Assess anemia severity",
"Pediatric Anemia Criteria (WHO, age-based Hb thresholds)",
"Normal Hb",
"Mild anemia",
"Moderate anemia",
"Severe anemia",
"6-59 months",
"5-11 years",
"12-14 years",
"Note: iron-deficiency anemia (IDA) is the most common pediatric anemia. Iron deficiency has 3 stages: 1. iron depletion (SF<12 μg/L, normal Hb); 2. iron-deficient erythropoiesis (SF<12, low MCV, normal Hb); 3. IDA (SF<12, low MCV, low Hb). First-line oral ferrous iron (elemental iron 3-6 mg/kg/day), between meals + vitamin C for absorption. Recheck Hb at 4 weeks; continue iron 2-3 months after correction to refill stores. Preterm infants: preventive iron 2 mg/kg/day from 2 weeks to 1 year. This tool is for clinical reference only.",
"In-Depth: Iron-Deficiency Anemia Assessment",
"Hb and age thresholds",
"Ferritin/MCV",
"Iron dose",
"1 yo Hb 90 ferritin 8",
"1 yo Hb threshold 110, 90 is moderate; ferritin<12, MCV<70 -> iron-deficient, iron 4 mg/kg×10 kg = 40 mg/day.",
"Hb<70 or heart-failure signs -> consider transfusion; then iron + diet after stabilization.",
"Iron dose?",
"Treatment 3-6 mg/kg/d elemental iron, prevention 1-2 mg/kg/d; vitamin C between meals aids absorption.",
"Why check MCV?",
"Microcytic hypochromic (low MCV) supports iron deficiency; in thalassemia ferritin is not low.",
"About the Iron-Deficiency Anemia (Hb/Serum Ferritin) Assessor",
"The pediatric IDA (Hb/serum ferritin) assessor uses age-stratified Hb thresholds to assess iron-deficiency degree and iron plan. A medical professional tool based on authoritative standards, for reference only.",
    ]))

if __name__ == '__main__':
    main()
