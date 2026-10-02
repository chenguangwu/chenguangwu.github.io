#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'tcm-diagnosis')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'tcm-diagnosis')
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
    out = {'slug': slug, 'industry': 'tcm-diagnosis', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('tcm-medical-record', build('tcm-medical-record', [
        "\U0001F33F TCM Medical Record Template Generator",
        "Fill in the four diagnostic findings per TCM record standards to auto-generate a standardized TCM medical record",
        "Record Entry",
        "Entry Guide",
        "Visit Date",
        "Occupation",
        "Native Place",
        "Visit Type",
        "First Visit",
        "Follow-up Visit",
        "II. Chief Complaint and History",
        "Chief Complaint (main symptoms + duration)",
        "History of Present Illness (onset, course, treatment)",
        "Past History",
        "Allergy History",
        "Personal History",
        "Family History",
        "III. Inspection",
        "Mental State",
        "Listless spirit",
        "Absent spirit",
        "Agitated spirit",
        "Complexion",
        "Normal (rosy with faint yellow)",
        "Sallow yellow",
        "Flushed red",
        "Dark black",
        "Dusky",
        "Body Build",
        "Emaciated",
        "Swollen with teeth marks",
        "Fissured",
        "Swollen",
        "Teeth marks present",
        "Prickles present",
        "Peeling",
        "Sublingual Veins",
        "Tortuous",
        "Purplish dark",
        "Engorged",
        "Other Inspection Findings (discharges, index-finger vein pattern in children, etc.)",
        "IV. Auscultation and Olfaction",
        "Voice",
        "Hoarse",
        "Heavy and turbid",
        "Coarse breathing",
        "Weak breathing",
        "Panting",
        "Low breath volume",
        "Cough (sound without sputum)",
        "Cough with sputum (no sound)",
        "Paroxysmal",
        "No abnormal odor",
        "Sour or foul odor",
        "Fishy or fetid odor",
        "Urine-like odor",
        "V. Inquiry (Ten Questions)",
        "Perspiration",
        "Head and Body",
        "Chest and Abdomen",
        "Ears, Eyes, Nose and Throat",
        "Diet and Taste",
        "Bowel and Urine",
        "Menstruation and Discharge",
        "Pediatric Questions",
        "VI. Palpation",
        "Surge pulse",
        "Tight pulse",
        "Soggy pulse",
        "Palpation Examination",
        "VII. Pattern Differentiation and Treatment",
        "Pattern Analysis (location + nature + mechanism)",
        "TCM Diagnosis (pattern)",
        "Western Diagnosis (optional)",
        "Formula and Herbs",
        "Doctor's Advice (care instructions)",
        "Generate Record",
        "Copy Record",
        "Download Record",
        "Clear Form",
        "External contraction of wind-cold",
        "Spleen-stomach deficiency-cold",
        "Liver qi stagnation",
        "Kidney yin deficiency",
        "Key Points for Writing TCM Medical Records",
        "Chief complaint:",
        "The patient's main suffering and its duration, concise and usually within 20 characters. Format: main symptoms + duration.",
        "History of present illness:",
        "Record in detail around the chief complaint how the disease arose, developed, changed, and was treated, including cause, initial symptoms, course, prior treatment and its effects.",
        "Inspection:",
        "Focus on spirit, complexion, body form and tongue findings. Tongue findings include the tongue body (pale red / pale white / red / crimson / purple, etc.), tongue shape (swollen / thin / teeth marks / fissures, etc.), coating (thin white / thick white / yellow greasy / thin or absent, etc.), and sublingual veins.",
        "Auscultation and olfaction:",
        "Listen to the voice (speech, breathing, cough) and smell odors (breath, body, discharges).",
        "Inquiry:",
        "Ask in the order of the Ten Questions: first cold and heat, second perspiration; third head and body, fourth stool and urine; fifth diet, sixth chest; seventh hearing and thirst must be judged; eighth and ninth old illnesses, tenth causes; also weigh medication changes. For women always ask about menstruation, noting whether it is early, late, closed or flooding.",
        "Palpation:",
        "Pulse diagnosis (cun, guan, chi; floating, middle, deep) and palpation (skin, extremities, epigastrium and abdomen, back-shu points).",
        "Pattern analysis:",
        "Synthesize the four diagnostic findings and apply eight-principle, zang-fu and other methods to analyze the location, nature, and mechanism of disease.",
        "Treatment principle:",
        "Establish the governing treatment principle from the pattern, such as tonifying qi and strengthening the spleen, activating blood and resolving stasis, or calming the liver and extinguishing wind.",
        "Formula and herbs:",
        "Name the formula and list the herb composition with doses for each herb, and note any modifications.",
        "This tool generates standardized TCM record templates for study and reference; clinical records must follow the standards of the medical institution. All data is processed locally in your browser and is never uploaded to any server.",
        "\U0001F4DA In-Depth Analysis: Generating TCM Medical Record Templates",
        "Outpatient Record Writing",
        "Fill Templates Fast",
        "Archive the Four Examinations",
        "Spleen Deficiency Template",
        "Select the \"Spleen Deficiency\" template to auto-fill: female, age 45, chief complaint \"poor appetite with loose stools and fatigue\", present illness, pale tongue with white coating, weak pulse, diagnosis \"spleen deficiency pattern\", principle \"strengthen the spleen and tonify qi\", formula such as Four Gentlemen Decoction.",
        "Kidney Deficiency Template",
        "Select the \"Kidney Deficiency\" template with age prefilled as 52, chief complaint \"aching lower back and knees with aversion to cold\", deep and thin pulse, diagnosis \"kidney yang deficiency\", formula such as Golden Cabinet Kidney Qi Pill.",
        "Can I edit the template?",
        "After generation you can revise the chief complaint, tongue and pulse, and diagnosis item by item, then copy or export the text in one click.",
        "Does it include Western medicine fields?",
        "It uses a pure TCM structure (four examinations + pattern + principle + formula) and does not write a Western diagnosis for you.",
        "About \"TCM Medical Record Template Generator\"",
        "TCM Medical Record Template Generator - Generate standardized TCM inpatient and outpatient records including chief complaint, present history, the four examinations, pattern differentiation and treatment. Professional medical tool based on authoritative medical standards, for reference only.",
        "Patient Name",
        "years",
        "Occupation",
        "Native Place",
        "e.g., recurrent epigastric pain for 3 years, worse for 1 week",
        "Record how the disease arose, developed, changed, and was treated",
        "Previous health status and disease history",
        "Drug and food allergy history",
        "Lifestyle habits and preferences",
        "Family and hereditary disease history",
        "e.g., thick yellow sputum in large amounts",
        "e.g., chills with fever / fever without chills / chills without fever",
        "e.g., no sweating / spontaneous sweating / night sweats",
        "e.g., headache and body aches / dizziness",
        "e.g., chest oppression with abdominal distension / hypochondriac pain",
        "e.g., tinnitus and blurred vision",
        "e.g., poor appetite with bitter taste / dry mouth with thirst",
        "e.g., dry hard stool / scanty dark urine",
        "e.g., insomnia with many dreams / somnolence",
        "Menstruation and vaginal discharge",
        "Birth history / vaccinations and so on",
        "e.g., soft abdomen without tenderness / mass below the hypochondrium",
        "Synthesize the four examinations to perform pattern analysis and clarify location, nature, and mechanism",
        "e.g., spleen-stomach deficiency-cold pattern",
        "e.g., chronic gastritis",
        "e.g., warm the middle and strengthen the spleen, disperse cold and relieve pain",
        "Formula name and composition, e.g., Regulating Middle Pill modified: ginseng, atractylodes, dried ginger...",
        "e.g., avoid raw and cold foods, keep warm, eat regular meals",
    ]))


if __name__ == '__main__':
    main()