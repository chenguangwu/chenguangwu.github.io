#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'rehabilitation')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'rehabilitation')
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
    out = {'slug': slug, 'industry': 'rehabilitation', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."

def main():
    write('assistive-device-fitting', build('assistive-device-fitting', [
        "\u2696\ufe0f Assistive Device Fitting (Size/Weight) Calculator",
        "Calculates the fitting dimensions, load capacity and usage recommendations for various assistive devices from patient parameters",
        "Computes the fitting dimensions, load capacity and usage recommendations for each assistive device from the entered parameters.",
        "Wheelchair fitting",
        "Orthosis fitting",
        "Prosthesis fitting",
        "Lower-leg length (cm, popliteal fossa to sole)",
        "Enter parameters to calculate the wheelchair size",
        "Orthosis selection",
        "Orthosis body part",
        "Ankle-foot orthosis (AFO)",
        "Knee-ankle-foot orthosis (KAFO)",
        "Hip-knee-ankle-foot orthosis (HKAFO)",
        "Wrist-hand orthosis (WHO)",
        "Elbow-wrist-hand orthosis (EWHO)",
        "Cervical orthosis",
        "Thoracolumbosacral orthosis (TLSO)",
        "Mild (muscle grade 3 or better)",
        "Moderate (muscle grade 2-3)",
        "Severe (muscle grade 0-2)",
        "Calf circumference (cm, for AFO)",
        "Thigh circumference (cm, for KAFO)",
        "Select parameters to see fitting recommendations",
        "Prosthesis parameters",
        "Amputation level",
        "Below-knee amputation",
        "Above-knee amputation",
        "Syme amputation (ankle)",
        "Below-elbow amputation",
        "Above-elbow amputation",
        "Patient activity grade",
        "K0 (cannot walk)",
        "K1 (indoor walking)",
        "K2 (limited outdoor walking)",
        "K3 (community walking)",
        "K4 (high activity)",
        "Enter parameters to see prosthesis fitting recommendations",
        "\U0001F4D6 Fitting principle reference",
        "Wheelchair fitting principles",
        "Seat width = hip width + 2 cm",
        "Seat depth = sitting depth - 2 to 5 cm (2-5 cm between the popliteal fossa and the seat front edge)",
        "Seat height = lower-leg length + 5 cm (footplate 5 cm off the floor)",
        "Backrest height = sitting height - seat height (raise it for high-level paraplegia)",
        "Armrest height = forearm height when resting flat while seated",
        "Load capacity selection: body weight x 1.5 safety factor",
        "Orthosis fitting principles",
        "AFO: calf circumference + 2 cm allowance",
        "KAFO: thigh circumference + 2-3 cm allowance",
        "Align the joint hinge with the anatomical joint axis",
        "Distribute pressure evenly to avoid pressure ulcers",
        "Keep the weight within the weight-bearing capacity of the affected limb",
        "Prosthesis fitting principles",
        "Full contact in the socket with even weight bearing",
        "The K grade determines component selection",
        "Prosthesis weight <= 80% of the weight of the sound limb",
        "Residual limb length affects suspension and control",
        "Refit periodically as the residual limb changes",
        "\U0001F4CCB Fitting record",
        "\U0001F4DDA In-depth analysis: assistive device fitting (wheelchair / brace / prosthesis)",
        "Wheelchair selection",
        "Prosthesis components",
        "Wheelchair seat width 38 cm",
        "Hip width 36 cm \u2192 seat width 36+2 = 38 cm; lower-leg length 40 \u2192 seat depth 37 cm; load = ceil(70x1.5) = 105 kg; prosthesis weight <= 70x4% = 2.8 kg.",
        "AFO selection",
        "For mild foot drop choose a posterior-leaf elastic AFO (carbon fiber); for moderate drop choose a hinged AFO with adjustable ankle angle; calf circumference 35 \u2192 add 2 cm at the gastrocnemius.",
        "Is there a limit on prosthesis weight?",
        "A prosthesis below the socket should not exceed 4% of body weight, otherwise energy expenditure rises and gait becomes abnormal; high-activity users should prioritize lightweight components.",
        "How is wheelchair seat width determined?",
        "While the patient is seated, add 2.5 cm (about one finger width) to each side of the widest point of the hips: too wide allows side-to-side sliding and raises the risk of spinal curvature; too narrow compresses the greater trochanters and ischial tuberosities and causes pressure ulcers. Seat depth leaves 2-3 fingers (about 5 cm) between the popliteal fossa and the seat edge so the popliteal fossa is not compressed and venous return is not affected. Take these measurements while the patient wears everyday clothing.",
        "About the Assistive Device Fitting (Size/Weight) Calculator",
        "Assistive Device Fitting (Size/Weight) Calculator." + DISCL_M,
        "How to use the Assistive Device Fitting (Size/Weight) Calculator",
        "What does the Assistive Device Fitting (Size/Weight) Calculator do?",
        "Enter patient height, weight and limb measurements, and the tool calculates fitting dimensions and load recommendations for assistive devices such as wheelchair seat width and depth, crutch and walker height, helping therapists select a safe, well-fitting device for the user.",
        "How do I use the Assistive Device Fitting (Size/Weight) Calculator?",
        "Which scenarios suit the Assistive Device Fitting (Size/Weight) Calculator?",
        "e.g. 170",
        "e.g. 65",
        "e.g. 85",
        "e.g. 40",
        "e.g. 45",
        "e.g. 35",
        "e.g. 50",
        "e.g. 15",
    ]))
    write('boston-aphasia', build('boston-aphasia', [
        "\U0001F4CCB Aphasia (Boston) Severity Assessor",
        "Boston Diagnostic Aphasia Examination (BDAE) severity grading (0-5) for evaluating language function in aphasia patients",
        "BDAE aphasia severity is rated from grade 0 to 5: grade 0 has no usable speech or auditory comprehension; grade 1 has severely limited, mostly fragmentary speech; grade 2 can hold everyday conversation with assistance; grade 3 can discuss familiar topics with help or prompting; grade 4 has fluent speech but reduced comprehension and limited concept expression; grade 5 is the mildest detectable speech impairment. Grading is based on the combined picture of speech fluency, auditory comprehension, repetition and naming.",
        "Choose the best matching grade",
        "Select a grade to see the detailed description",
        "\U0001F4CCA Boston aphasia classification",
        "Aphasia type",
        "Fluency",
        "Comprehension",
        "Repetition",
        "Naming",
        "Lesion site",
        "Broca aphasia",
        "Non-fluent",
        "Inferior frontal gyrus (Broca area)",
        "Wernicke aphasia",
        "Fluent",
        "Superior temporal gyrus (Wernicke area)",
        "Conduction aphasia",
        "Arcuate fasciculus / angular gyrus",
        "Global aphasia",
        "Extensive dominant hemisphere",
        "Anomic aphasia",
        "Good",
        "Middle temporal gyrus / angular gyrus",
        "Transcortical motor",
        "Frontal watershed region",
        "Transcortical sensory",
        "Temporoparietal watershed region",
        "Transcortical mixed",
        "Extensive watershed region",
        "\U0001F4CCB Assessment record",
        "\U0001F4DDA In-depth analysis: aphasia (Boston) severity grading",
        "Expressive aphasia",
        "Recovery prediction",
        "Communication strategies",
        "Boston grade 2: only fragmentary speech with limited comprehension, communication board plus gestures are the mainstay, prognosis is worse than for grades 4-5, and intensive speech therapy is needed.",
        "Grade 4: everyday conversation is basically fluent while complex sentences are weaker, so social re-entry is feasible, with emphasis on naming and precise reading and writing training.",
        "How does it compare with the assessor?",
        "This tool rates severity on the 0-5 scale, consistent with the Boston Diagnostic Aphasia Examination: the higher the grade, the better the function.",
        "Do the grades change over time?",
        "Yes, and that is exactly what it is for: the first 3-6 months after stroke are the fastest window of spontaneous recovery, and grades often improve markedly during that period; after 6 months the curve plateaus. Grades should therefore record the assessment date and disease stage, and a single grade cannot judge long-term prognosis. Still grade 0-1 after 6 months suggests a poor prognosis, so rehabilitation goals should shift toward compensatory communication strategies (gestures, communication boards) rather than restoring spoken language.",
        "About the Aphasia (Boston) Severity Assessor",
        "Aphasia (Boston) Severity Assessor." + DISCL_M,
    ]))
    write('fim-scale', build('fim-scale', [
        "\U0001FABF Functional Independence Measure (FIM) Total Score Calculator",
        "FIM functional independence rating of 18 items (13 motor + 5 cognitive), 1-7 points each, 18-126 total",
        "Complete all item scores to see the result",
        "\U0001F4CCA FIM scoring standard",
        "Level of independence",
        "Complete independence",
        "Completes safely without assistance and within reasonable time",
        "Modified independence",
        "Completes independently with assistive devices or extra time",
        "Supervision",
        "Needs supervision, prompting or setup from another person but no physical contact",
        "Minimal assistance",
        "Needs physical contact from another person and completes 75% or more by itself",
        "Moderate assistance",
        "Needs help from another person and completes 50-74% by itself",
        "Maximal assistance",
        "Needs help from another person and completes 25-49% by itself",
        "Complete assistance",
        "Completes less than 25% by itself and depends fully on others",
        "Total score interpretation:",
        "126 = complete independence; 108-125 = basically independent; 90-107 = very mild dependence; 72-89 = mild dependence; 54-71 = moderate dependence; 36-53 = severe dependence; 19-35 = very severe dependence; 18 = complete dependence.",
        "\U0001F4CCB Assessment record",
        "\U0001F4DDA In-depth analysis: Functional Independence Measure (FIM) total score",
        "Admission baseline",
        "Discharge comparison",
        "Insurance assessment",
        "Total 126",
        "13 motor items + 5 cognitive items across 18 items x 1-7: motor 91 + cognitive 35 = 126, complete independence (>=108).",
        "Total 60",
        "Total 60 (54-71 orange zone), moderate dependence needing substantial assistance; if admission is <80, expected gain \u224820 + (80 - total) x 0.3.",
        "What do the grades mean?",
        ">=126 complete independence; 108-125 basically independent; 72-107 moderate dependence; 54-71 severe dependence; 18-53 very severe dependence (18 items, maximum 126).",
        "Why assess on both admission and discharge?",
        "The core value of the FIM lies in the difference rather than a single number: FIM efficiency = (discharge FIM - admission FIM) / length of stay, or FIM gain = (discharge - admission) / (maximum possible score - admission score). The admission score alone only shows the care burden and not how fast recovery happens. Scoring must record actual performance rather than potential, and the cognitive and motor subscales should be read separately, since slow cognitive improvement often signals a poorer prognosis.",
        "About the Functional Independence Measure (FIM) Total Score Calculator",
        "Functional Independence Measure (FIM) Total Score Calculator." + DISCL_M,
        "How to use the Functional Independence Measure (FIM) Total Score Calculator",
        "What does the Functional Independence Measure (FIM) Total Score Calculator do?",
        "How do I use the Functional Independence Measure (FIM) Total Score Calculator?",
        "Which scenarios suit the Functional Independence Measure (FIM) Total Score Calculator?",
        "Score range",
        "The Functional Independence Measure (FIM) has 18 items (self-care, sphincter, transfer, walking, communication, social cognition), 1-7 points each, total",
        "Complete independence;",
        "Basically independent (some needs assistive devices);",
        "Needs assistance from another person;",
        "Needs substantial assistance;",
        "Fully dependent. A higher score means better functional independence.",
        "Scope of use",
        "The FIM is rated by the rehabilitation team to track recovery outcomes after stroke or trauma; this tool only totals the sub-scores and cannot replace clinical assessment.",
    ]))


if __name__ == '__main__':
    main()