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
    write('esophageal-varices', build('esophageal-varices', [
        "\U0001FA7B Esophageal Varices Grading and Bleeding Risk Assessor",
        "Assess first-bleeding risk (NIEC index) based on varix size, red wale signs, and Child-Pugh grade.",
        "Esophageal Varices Bleeding Risk Assessor",
        "/ Esophageal Varices Assessment",
        "\U0001F4D6 View the Esophageal Varices Bleeding Risk (Modified NIEC) Assessment Usage Guide",
        "Esophageal varices grading: assess rupture risk and prevention strategy from varix size (D1\u2013D3) + red wale signs + Child-Pugh grade + prior bleeding.",
        "Varix size",
        "Mild (D1, diameter <3mm)",
        "Moderate (D2, diameter 3-6mm)",
        "Severe (D3, diameter >6mm)",
        "Red wale signs (RC sign)",
        "Child-Pugh grade",
        "Any prior bleeding",
        "No bleeding history",
        "With bleeding history",
        "\U0001F4CB Esophageal varices grading criteria",
        "Varix diameter",
        "Mild (G1)",
        "Straight or tortuous",
        "Lower esophagus",
        "Moderate (G2)",
        "Tortuous elevation",
        "May reach middle esophagus",
        "Severe (G3)",
        "Beaded/nodular",
        "May reach upper esophagus",
        "Domestic grading (LDRf): records location (L), diameter (D), red wale sign (R), risk factor (f).",
        "\U0001F4CA Bleeding risk factors",
        ": D3 carries markedly higher bleeding risk than D1",
        ": red stripes, cherry-red spots, cystic red spots, etc., indicating high bleeding risk",
        ": grade C carries the highest bleeding risk",
        ": hepatic venous pressure gradient >12 mmHg is the bleeding threshold, >20 mmHg indicates high rebleeding risk",
        "Prior bleeding history",
        ": rebleeding risk within 1 year reaches 60-70%",
        "\U0001F4CA Prevention strategies",
        "Primary prophylaxis",
        ": moderate-severe varices + high-risk factors (Child B/C or positive RC sign) \u2192 non-selective beta blocker (NSBB) or endoscopic variceal ligation (EVL)",
        "Secondary prophylaxis",
        ": after bleeding \u2192 NSBB + EVL combination therapy",
        "High-risk patients",
        ": TIPS or surgical shunt surgery",
        "Note: Acute variceal bleeding is a lethal complication of cirrhosis, with 6-week mortality around 15-25%. Bleeding risk rises as varices enlarge, RC signs worsen, and liver function deteriorates. HVPG measurement is the gold standard. For clinical reference only.",
        "\U0001F4DA Deep Dive: Esophageal Varices Bleeding Risk (Modified NIEC) Assessment",
        "Primary prophylaxis: estimate first-bleeding risk from varix degree, red wale signs, and Child-Pugh",
        "Emergency bleeding control: very high-risk patients need immediate NSBB/EVL combination plus TIPS evaluation",
        "Follow-up stratification: set gastroscopy recheck intervals by risk level",
        "Algorithm: risk score = size (mild/moderate/severe 1/2/3) + red wale sign (none/mild/moderate/severe 0~3) + Child-Pugh (A/B/C 1/2/3) + bleeding history (yes +2). Grading: \u22659 very high risk (1-year bleeding >50%), 6~8 high risk (25~35%), 4~5 moderate risk (10~15%), <4 low risk (<5%).",
        "Example: moderate varices (D2), moderate red wale sign, Child-Pugh grade B, no bleeding history \u2192 2+2+2+0 = 6 points, high risk (1-year bleeding 25~35%), NSBB or EVL primary prophylaxis plus gastroscopy follow-up every 1~2 years is advised. If severe varices (D3), severe red wale sign, grade C, bleeding history \u2192 3+3+3+2 = 11 points, very high risk (>50%); immediate NSBB+EVL combination and TIPS indication evaluation are advised.",
        "What are red wale signs?",
        "Red wale signs are red markings on the varix surface under endoscopy (red stripes, blood blister-like, cherry-red dots, etc.), indicating high wall tension and high near-term bleeding risk. They are an independent bleeding predictor and are more sensitive than size alone.",
        "How to choose between NSBB and EVL?",
        "For moderate-to-high risk patients without bleeding history, either NSBB (propranolol/carvedilol) or EVL alone can serve as primary prophylaxis; for high/very high risk or those with bleeding history, NSBB+EVL combination is recommended. NSBB also reduces the risk of hepatic encephalopathy and portal hypertensive gastropathy, but heart rate and blood pressure must be monitored.",
        "About the Esophageal Varices Bleeding Risk Assessor",
        "The Esophageal Varices Grading and Bleeding Risk Assessor evaluates first-bleeding risk from varix size, red wale signs, and Child-Pugh grade." + DISCL_M,
    ]))
    write('gastric-emptying', build('gastric-emptying', [
        "\U0001FA7B Gastrointestinal Motility (Gastric Emptying) Tester",
        "Compute gastric emptying rate and half-emptying time from radionuclide gastric emptying scan data to assess gastric motility function.",
        "Compute gastric emptying rate and half-emptying time from radionuclide gastric emptying scan data to assess gastric motility function. Computes professionally from the input parameters and outputs the result.",
        "Gastrointestinal Motility Gastric Emptying Tester",
        "/ Gastric Emptying Measurement",
        "Radionuclide gastric emptying scan (gold standard)",
        "\u00B9\u00B3C-octanoic acid breath test",
        "Test meal type",
        "Solid test meal",
        "Liquid test meal",
        "Radionuclide retention rate (at different time points)",
        "2-hour retention rate (%)",
        "4-hour retention rate (%)",
        "Initial retention rate (%)",
        "Half-emptying time T\u00BD (minutes)",
        "Analyze results",
        "\U0001F4CB Normal gastric emptying reference values (radionuclide solid meal)",
        "Too rapid emptying",
        "1-hour retention rate",
        "2-hour retention rate",
        "4-hour retention rate",
        "Half-emptying time T\u00BD",
        "<90 minutes",
        ">90 minutes",
        "<30 minutes",
        "Standard test meal: \u00B9\u00B3\u2079Tc-colloid-labeled egg sandwich (255 kcal). Reference values vary by test meal and laboratory.",
        "\U0001F4CA Clinical meaning of abnormal gastric emptying",
        "Delayed gastric emptying (gastroparesis)",
        "Diabetic autonomic neuropathy (most common)",
        "Idiopathic gastroparesis (possibly related to post-viral infection)",
        "Postoperative gastroparesis (after vagotomy)",
        "Drugs: opioids, anticholinergics, GLP-1 agonists",
        "Neurologic disease: Parkinson disease, multiple sclerosis",
        "Connective tissue disease: scleroderma, systemic lupus erythematosus",
        "Too rapid gastric emptying (dumping syndrome)",
        "After gastric surgery (Billroth II, Roux-en-Y)",
        "Post-vagotomy",
        "Zollinger-Ellison syndrome",
        "Early dumping (within 30 min of meals, vasomotor symptoms)",
        "Late dumping (1-3 hours after meals, hypoglycemic symptoms)",
        "Note: Radionuclide gastric emptying scan is the gold standard for assessing gastric motility. Before testing, drugs affecting gastric motility must be stopped (prokinetics 3 days, opioids 48 hours, anticholinergics 48 hours). Blood glucose control matters (>278 mg/dL can delay emptying). The wireless motility capsule (WMC) can simultaneously assess whole-GI transit time. For clinical reference only.",
        "\U0001F4DA Deep Dive: Gastric Emptying (Radionuclide Method) Measurement and Gastroparesis Judgment",
        "Finding the cause of dyspepsia: compute T\u00BD and emptying rate from radionuclide gastric emptying scan retention rates",
        "Gastroparesis diagnosis: 4h retention >10% or T\u00BD >90 min indicates delay",
        "Dumping syndrome: 2h retention <30% or T\u00BD <30 min indicates too-rapid emptying",
        "Algorithm: 2h emptying rate = initial retention \u2212 2h retention; the same for 4h. 2h retention >60% delayed, 30%~60% normal, <30% on the fast side; 4h retention >10% delayed, \u226410% normal; half-emptying T\u00BD >90 min prolonged, 30~90 min normal, <30 min shortened. Combined: 4h retention >10% or T\u00BD >90 min \u2192 delayed gastric emptying (gastroparesis); 2h retention <30% or T\u00BD <30 min \u2192 possible dumping syndrome; otherwise normal.",
        "Example: initial 100%, 2h retention 65%, 4h retention 30%, T\u00BD 90 min \u2192 2h emptying 35%, 4h emptying 70%, 4h retention 30%>10% judged delayed gastric emptying (gastroparesis); screening for mechanical obstruction, optimizing glucose, and prokinetics are advised. If 2h retention 40%, 4h retention 5%, T\u00BD 60 min \u2192 4h retention \u226410% and T\u00BD normal, judged normal gastric emptying.",
        "Is radionuclide gastric emptying the gold standard?",
        "Radionuclide scintigraphy is currently the first-choice physiological test for gastroparesis diagnosis (4h retention >10% indicates delay), but it is affected by test meal type (solid/liquid), equipment, and operation. The \u00B9\u00B3C-octanoic acid breath test can serve as a non-invasive alternative, while electrogastrography and ultrasound have limited reference value.",
        "Which matters more, T\u00BD or 4h retention?",
        "The two complement each other: the 4h retention rate directly reflects the degree of delay, while T\u00BD reflects the emptying speed. Clinically 4h retention >10% is used as the main gastroparesis criterion; prolonged T\u00BD (>90 min) supports the diagnosis, while shortened T\u00BD (<30 min) suggests dumping syndrome.",
        "About the Gastrointestinal Motility Gastric Emptying Tester",
        "The Gastrointestinal Motility Gastric Emptying Tester computes the gastric emptying half-time (T1/2) and emptying rate from radionuclide gastric emptying or breath test data to assess gastric motility function." + DISCL_M,
    ]))

if __name__ == '__main__':
    main()
