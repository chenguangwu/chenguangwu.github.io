#!/usr/bin/env python3
# gen_dentistry_head.py — shared head for dentistry batches b1..bN
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'dentistry')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'dentistry')
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
    out = {'slug': slug, 'industry': 'dentistry', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('alveolar-bone-loss', build('alveolar-bone-loss', [
        "Alveolar Bone Loss (Root-Length Ratio) Grader",
        "Estimates the percentage of alveolar bone loss from the remaining bone height and root length measured on X-rays to assess the severity of periodontal bone defects and prognosis.",
        "Alveolar Bone Loss (Root-Length Ratio) Grader",
        "/ Alveolar Bone Loss (Root-Length Ratio) Grader",
        'View "Alveolar Bone Loss (Root-Length Ratio) Grader User Guide"',
        "Remaining bone height (mm)",
        "Total root length (mm)",
        "Bone loss type",
        "Horizontal bone loss",
        "Vertical (angular) bone loss",
        "Furcation involvement",
        "Root-length ratio method",
        "CEJ-to-apex method",
        "Bone loss severity is a key indicator for periodontal diagnosis and prognosis. Severe bone loss has a poor prognosis and requires comprehensive assessment of retention value.",
        "Bone Loss Grading Criteria",
        "Bone loss ratio",
        "< 1/4 of root length (<25%)",
        "Early lesion, better prognosis",
        "1/4 - 1/2 of root length (25%-50%)",
        "Needs systematic treatment, moderate prognosis",
        "1/2 - 2/3 of root length (50%-66%)",
        "Poor prognosis, needs comprehensive assessment",
        "> 2/3 of root length (>66%)",
        "Very poor prognosis, often requires extraction",
        "Bone loss % = (root length - remaining bone height) / root length x 100%\nRemaining bone support % = remaining bone height / root length x 100%",
        "Reference: bone loss grading in Periodontology (Meng Huanxin). Clinically combined with crown-root ratio.",
        "In-Depth: Alveolar Bone Loss (Root-Length Ratio) Grader",
        "A clinical record shows the remaining bone height of a mandibular molar is about 40% of the root length; after entering this ratio, the tool classifies it as grade III bone loss and warns of significant loss of periodontal support and cautious prognosis.",
        "At follow-up, compare two periapical films and convert the difference in bone height into a progression rate to help judge whether periodontal treatment has controlled the destruction.",
        "Before implant placement, assess the available bone height in the edentulous area; when remaining bone height is insufficient, prompt for bone augmentation first. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Remaining Bone Height Ratio Calculation",
        "Input: root length L=13mm, remaining bone height on film H=5.2mm\nCalculation: bone loss ratio = (1 - H/L) x 100% = (1 - 5.2/13) x 100% approx 60%\nDetermination: > 1/2 of root length indicates grade III bone loss, suggesting significant loss of supporting tissue; implant placement needs bone augmentation assessment.",
        "How is bone loss graded?",
        "Commonly by root-length ratio: <1/3 is grade I, 1/3~1/2 is grade II, >1/2 is grade III, reaching the apex is grade IV (severe). Specific judgment follows clinical and imaging findings.",
        "Are bone loss and pocket depth the same?",
        "No. Bone loss reflects supporting-bone loss on X-ray, while pocket depth is the soft-tissue probing depth; both must be combined with clinical attachment loss (CAL) to assess periodontal severity.",
        "Can this ratio replace X-ray diagnosis?",
        "No. This tool is only a ratio estimate; diagnosis relies on periapical film or CBCT and periodontal probing; for loose teeth or gum bleeding, visit a periodontal specialist promptly.",
        "About the Alveolar Bone Loss (Root-Length Ratio) Grader",
        "Alveolar Bone Loss (Root-Length Ratio) Grader - Calculates the bone loss ratio from remaining bone height and root length to assess the severity of periodontal bone defects. A professional medical tool based on authoritative standards, for reference only.",
    ]))
    write('assessor-5', build('assessor-5', [
        "Zirconia (Translucency) Aesthetics Assessment",
        "Estimates the visible-light translucency of zirconia all-ceramic restorations and evaluates aesthetic fit by restoration site. Higher translucency is closer to natural tooth semitransparency, especially important in anterior aesthetic zones.",
        "Zirconia (Translucency) Aesthetics Assessment",
        "/ Zirconia (Translucency) Aesthetics Assessment",
        'View "Zirconia Translucency Aesthetics Assessment User Guide"',
        "Zirconia translucency = spectroscopic measurement",
        "Zirconia material type",
        "Super-translucent (ST, T0 ~46%)",
        "High-translucent (HT, T0 ~43%)",
        "Semi-translucent (STT, T0 ~35%)",
        "High-strength translucent (T0 ~25%)",
        "Conventional zirconia (T0 ~18%)",
        "Framework/base thickness (mm)",
        "External staining level",
        "No staining",
        "Mild staining",
        "Moderate staining",
        "Severe staining",
        "Restoration site",
        "Anterior aesthetic zone (incisors/canines)",
        "Assess aesthetics",
        "Translucency reference values come from literature on common zirconia materials; brands and sintering processes vary.",
        "Calculation uses Beer-Lambert attenuation approximation (k~0.6); results are estimates for material-selection reference only.",
        "For anterior aesthetic zones, choose high/super-translucent materials and control thickness; for posterior teeth, prioritize strength.",
        "In-Depth: Zirconia Translucency Aesthetics Assessment",
        "For anterior all-ceramic crown restoration, enter tooth position and translucency need; the tool recommends 4Y/5Y high-translucent zirconia to approach natural tooth semitransparency.",
        "For posterior high-occlusal-force areas, favor strength; recommend 3Y conventional-translucent zirconia and caution in aesthetic zones.",
        "After shade selection, if translucency differs noticeably from neighboring teeth, choose a higher-translucency generation or labial veneering adjustment. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Generation by tooth position",
        "Input: restoration site = maxillary central incisor, aesthetic need = high, shade = 2M2\nOutput: recommend 5Y high-translucent zirconia (translucency close to natural enamel); if needed, labial veneering for layering; for posterior areas, 3Y to balance flexural strength.",
        "What is the difference between 3Y/4Y/5Y zirconia?",
        "The number denotes yttria stabilizer content: 3Y has highest strength and lower translucency; 4Y is in between; 5Y has best translucency and slightly lower strength. Anterior aesthetic zones lean 4Y/5Y, posterior occlusal zones lean 3Y.",
        "Why is translucency especially important for anterior teeth?",
        "Natural anterior enamel is semi-transparent; insufficient translucency looks dead white and lacks depth; high-translucent zirconia or labial veneering is closer to the natural look.",
        "Can translucency and strength be combined?",
        "There is a trade-off; higher-translucency generations lose some strength, which the dentist can compensate via restoration design (thickness, bonding). This tool is for initial screening only.",
        "About the Zirconia Translucency Aesthetics Assessment",
        "The translucency of zirconia all-ceramic restorations directly affects aesthetic realism. This tool estimates final translucency from the material's base translucency, thickness and staining, and gives an aesthetic-fit rating and material advice by restoration site.",
        "Beer-Lambert model translucency estimate",
        "Distinguish anterior/premolar/molar aesthetic thresholds",
        "Material selection and thickness optimization advice",
        "Anterior all-ceramic crown/veneer material selection",
        "Zirconia framework thickness design",
        "Discolored-tooth masking vs translucency trade-off",
        "Shade-communication reference for dental technicians",
        "How to use the Zirconia Translucency Aesthetics Assessment",
        "Suitable for pre-shade-screening of material generations before anterior all-ceramic restoration, assessing restoration translucency against neighboring teeth, and zirconia-selection reference for different tooth positions (anterior aesthetic / posterior functional zones).",
        "What does the Zirconia Translucency Aesthetics Assessment do?",
        "How to use the Zirconia Translucency Aesthetics Assessment?",
        "Which scenarios suit the Zirconia Translucency Aesthetics Assessment?",
    ]))
    write('bite-contact', build('bite-contact', [
        "Occlusal Contact Balance-Point Analyzer",
        "Simulates T-Scan force-distribution data, calculates the Center of Force of occlusal force (COFP) and left-right/fore-aft balance to assist occlusal adjustment.",
        'View "Occlusal Contact Balance-Point Analyzer User Guide"',
        "Occlusal balance = contact-point analysis",
        "Occlusal force share by quadrant (%)",
        "Left anterior quadrant (%)",
        "Right anterior quadrant (%)",
        "Left posterior quadrant (%)",
        "Right posterior quadrant (%)",
        "Normalize",
        "This tool simulates the T-Scan center from quadrant force distribution; clinically combine with intercuspal position (ICP) and lateral/protrusive occlusion.",
        "Occlusal Balance Reference Criteria",
        "Left-right force difference",
        "Fore-aft force ratio (posterior/anterior)",
        "<1.5 or >5",
        "Force-center deviation",
        "Slight deviation",
        "Marked deviation",
        "Reference: T-Scan III occlusal analysis system clinical guideline. The normal occlusal force center should be near the midline and slightly toward the posterior.",
        "In-Depth: Occlusal Contact Balance-Point Analyzer",
        "After prosthesis insertion, if occlusion feels uncomfortable, import force-distribution data; the tool computes the force center shifted to the affected side, suggesting adjustment of premature contact.",
        "For TMD patients, assess left-right balance; a large left-right force difference suggests a unilateral-chewing habit.",
        "After implant restoration, monitor force distribution to avoid peri-implant overload. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Left-Right Balance Calculation",
        "Input: left occlusal force 80N, right occlusal force 40N\nCalculation: left/right ratio = 2.0, occlusal force center (COFP) shifts left\nNote: left-right force difference >30% is considered unbalanced; adjust occlusion or check unilateral chewing.",
        "What is COFP?",
        "Center of Force Platform, the occlusal force center, reflects the spatial position of the resultant force in the dental arch; deviation from midline or fore-aft abnormality suggests occlusal imbalance.",
        "What does left-right imbalance indicate?",
        "May suggest premature contact, prosthesis high spot, unilateral chewing or joint problems; combine clinical and T-Scan examinations for comprehensive judgment.",
        "Can it replace T-Scan equipment?",
        "No. This tool is for understanding force-distribution concepts and manual data review; formal occlusal analysis relies on T-Scan and clinician examination.",
        "About the Occlusal Contact Balance-Point Analyzer",
        "Occlusal Contact T-Scan Balance-Point Analyzer - Calculates the occlusal force center from left-right and fore-aft occlusal force distribution to assess occlusal balance. A professional medical tool based on authoritative standards, for reference only.",
    ]))
    write('bridge-span', build('bridge-span', [
        "Dental Bridge Span Mechanics Analyzer",
        "Based on Ante's law: the sum of abutment periodontal-membrane areas should be >= the replaced tooth's periodontal-membrane area, to assess fixed-bridge design feasibility.",
        'View "Dental Bridge Span Mechanics Analyzer User Guide"',
        "Missing teeth and abutment selection",
        "Number of missing teeth",
        "1 tooth",
        "2 teeth",
        "3 teeth",
        "Missing-tooth position (from left)",
        "Second missing-tooth position",
        "Abutment selection",
        "Mesial abutment position",
        "Distal abutment position",
        "Ante's law is a traditional design principle; modern fixed-bridge design also considers occlusal force, alveolar-bone condition, crown-root ratio and edentulous span.",
        "Permanent-Tooth Periodontal Membrane Area Reference (mm2)",
        "Ante's law: sum of abutment PDL areas / sum of missing-tooth PDL areas >= 1 (recommended >=1, >=0.8 at the margin)",
        "Maxilla",
        "Central incisor",
        "Smallest area",
        "Lateral incisor",
        "Smaller area",
        "Strongest among anterior teeth",
        "First premolar",
        "Second premolar",
        "First molar",
        "Largest area",
        "Second molar",
        "This tool uses maxillary/mandibular averages; data reference Jepsen (1963) PDL area table.",
        "In-Depth: Dental Bridge Span Mechanics Analyzer",
        "For Kennedy-class edentulous fixed prosthesis, enter abutment and replaced-tooth PDL areas; the tool checks compliance with Ante's law.",
        "For multi-unit bridges with large span and average abutments, suggest adding abutments or switching to removable/implant restoration.",
        "For a single anterior short-span defect with healthy abutments, verification passes with a load note. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Ante's Law Check",
        "Input: sum of abutment PDL areas SigmaP = 360mm2, replaced-tooth area R = 240mm2\nDetermination: SigmaP >= R -> satisfies Ante's law, fixed-bridge design feasible; if SigmaP < R, add abutments.",
        "What is Ante's law?",
        "Classic principle: the sum of abutment PDL areas should be no less than the replaced tooth's PDL area, to assess whether abutments can bear the extra load.",
        "How to understand PDL area?",
        "Approximates a tooth's support capacity; multi-rooted and large-rooted teeth have larger areas; modern design also combines alveolar-bone height and quality.",
        "What if the law is not satisfied?",
        "Add abutments, switch to removable partial denture or implant; final plan by the prosthodontist based on bone support and occlusion.",
        "About the Dental Bridge Span Mechanics Analyzer",
        "Bridge Span Edentulous-Interval Mechanics Analyzer - Analyzes the ratio of fixed-bridge abutment root area to missing-tooth root area based on Ante's law to assess abutment support. A professional medical tool based on authoritative standards, for reference only.",
    ]))
    write('bruxism-force', build('bruxism-force', [
        "Bruxism (Bite Force) Estimator",
        "Estimates the peak sleep bite force and cumulative load of bruxism patients from masseter EMG activity and bruxism-event parameters, to assess bruxism severity.",
        "Bruxism Bite Force Estimator",
        "/ Bruxism Bite Force Estimator",
        'View "Bruxism (Bite Force) Estimator User Guide"',
        "Bruxism event parameters",
        "Nighttime bruxism event count",
        "Average single-event duration (s)",
        "Masseter EMG peak (%MVC)",
        "Max voluntary bite force MVC (N)",
        "Sleep duration (hours)",
        "Bruxism type",
        "Grinding type",
        "Clenching type",
        "This tool estimates from an EMG-to-force model; actual bite force needs dedicated sensors (e.g. BiteStrip/portable EMG). Results are for assessment reference.",
        "Bruxism Assessment Reference",
        "Peak bite force approx MVC x (EMG%MVC / 100)\nCumulative occlusal load approx peak force x event count x single duration\nPer-event total force = cumulative load / sleep duration (converted to minutes)\n\nNormal max bite force: anterior 150-300N, posterior 500-800N",
        "Bruxism severity",
        "Nighttime event count",
        "EMG peak",
        "<5 events/night",
        "Occasional, no obvious wear",
        "5-15 events/night",
        "Tooth wear, morning muscle fatigue",
        ">15 events/night",
        "Severe wear, headache, TMD",
        "Reference: Lobbezoo bruxism diagnostic criteria; ICSD-R sleep-related bruxism grading.",
        "In-Depth: Bruxism (Bite Force) Estimator",
        "For morning masticatory-muscle soreness and tooth wear, enter EMG and event parameters; the tool estimates nighttime peak bite force and suggests a bruxism grade.",
        "Compare cumulative load before and after wearing an occlusal splint to monitor whether conservative treatment reduces load.",
        "Combine sleep-monitoring event frequency to quantify single-night cumulative bite force. (Results are for oral-health education and self-screening only, not a substitute for oral examination, periapical film/CBCT imaging, or diagnosis and treatment by dental, orthodontic or periodontal specialists; if you have toothache, gum bleeding, non-healing ulcers, abnormal oral mucosa or occlusal discomfort, please visit a regular hospital dental department promptly.)",
        "Peak Bite Force Estimation",
        "Input: masseter EMG peak EMG=450uV, bruxism events 40/night, single duration 8s\nEstimate: peak bite force approx k x EMG (empirical coefficient), cumulative load = peak x single duration x event count\nNote: significant overload suggests occlusal splint and follow-up assessment.",
        "What is normal sleep bite force?",
        "Awake maximum bite force often reaches hundreds of newtons; sleep bruxism can approach or exceed awake levels; this estimate is relative reference, not an absolute diagnosis.",
        "Can EMG be directly converted to bite force?",
        "There are empirical coefficients and individual differences; estimate only; bruxism diagnosis relies on history, wear signs and polysomnography.",
        "How to manage bruxism?",
        "Mild cases observe; obvious wear or soreness can use an occlusal splint and stress relief; for facial pain or severe wear, visit an oral-maxillofacial department.",
        "About the Bruxism Bite Force Estimator",
        "Bruxism Bite Force Estimator - Estimates the sleep bite force and wear of bruxism patients to assess bruxism severity. A professional medical tool based on authoritative standards, for reference only.",
    ]))

if __name__ == "__main__":
    main()
