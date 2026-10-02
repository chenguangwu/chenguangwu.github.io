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
    write('proprioception-error', build('proprioception-error', [
        "\U0001F4BE Proprioception (Joint Position Sense) Error Measurer",
        "Passively move a joint to the target angle, have the patient reproduce it actively, and compute the position sense error",
        "Passively move a joint to the target angle, have the patient reproduce it actively, and compute the position sense error from the entered parameters.",
        "Test mode",
        "Result analysis",
        "Reference standard",
        "Test settings",
        "Joint to test",
        "Side to test",
        "Target angle 1 (degrees)",
        "Reproduced angle 1 (degrees)",
        "Target angle 2 (degrees)",
        "Reproduced angle 2 (degrees)",
        "Target angle 3 (degrees)",
        "Reproduced angle 3 (degrees)",
        "Target angle 4 (degrees)",
        "Reproduced angle 4 (degrees)",
        "The error is computed automatically once the reproduced angles are entered",
        "Finish the test",
        "Complete the test in test mode first",
        "Proprioception error reference standard",
        "Error range",
        "Proprioception normal, joint position sense precise",
        "Proprioception basically normal",
        "Proprioception mildly reduced, needs attention",
        "Proprioception clearly reduced, training needed",
        "Proprioception severely impaired, function affected",
        "1. The patient closes the eyes or has vision blocked",
        "2. The examiner passively moves the patient's joint to the target angle and holds it for 3-5 seconds",
        "3. Return to the start position and ask the patient to reproduce that angle actively",
        "4. Record the target and reproduced angles and compute the absolute error",
        "5. Test each angle 3 times and take the average",
        "6. Test several angles (across different ROM ranges) for a comprehensive assessment",
        "Proprioception impairment is commonly seen in joint injury (ligament tears), neurological disease (stroke, spinal cord injury), degenerative joint disease (OA) and the postoperative state. Reduced proprioception affects balance and motor control and raises the risk of reinjury.",
        "Training methods",
        "Closed-chain exercise training (weight-bearing)",
        "Balance board / BOSU ball training",
        "Elastic band resistance training",
        "Mirror feedback training",
        "Joint angle reproduction training",
        "\U0001F4CC Test record",
        "\U0001F4DDA In-depth analysis: proprioception (joint position sense) error measurement",
        "Knee reconstruction",
        "Ankle instability",
        "Balance training",
        "Mean error 3.5 degrees",
        "Target 30 degrees / reproduced 33 degrees (3 degrees overshoot), mean 3.5 degrees over 4 trials with a maximum of 5 degrees: judged good,",
        "0.9 degrees, with the direction of error mostly overshoot.",
        "Abnormal 9 degrees",
        "Mean error 9 degrees, maximum 12 degrees: mildly abnormal, proprioception training (balance board / eyes-closed standing) is recommended to improve joint position sense.",
        "How are the grades defined?",
        "3 degrees or less excellent, 5 degrees or less good, 10 degrees or less mildly abnormal, above 10 degrees clearly abnormal; after hemiplegia or ligament surgery values are often above 5 degrees.",
        "How many trials are needed?",
        "Test at least 3 times for each target angle and take the mean absolute error, since a single measurement varies too much to base a conclusion on. Vision must be blocked and auditory cues removed (such as device noise); do 1-2 demonstrations first (not counted) and alternate the affected and healthy sides to cancel out the learning effect. An absolute error above 5 degrees is generally considered position sense impairment, but it is only reliable when compared with the healthy side at the same angle.",
        "About the Proprioception (Joint Position Sense) Error Measurer",
        "Proprioception (Joint Position Sense) Error Measurer." + DISCL_M,
    ]))
    write('prosthesis-alignment', build('prosthesis-alignment', [
        "\u2696\ufe0f Prosthesis Alignment (Load Line) Adjustment Calculator",
        "Computes the position of the prosthesis load line and alignment parameters to assist prosthetic fitting and adjustment",
        "Core formulas (from the input variables): weight x 9.8; thighLen x 0.05",
        "Prosthesis type",
        "Below-knee prosthesis",
        "Above-knee prosthesis",
        "Residual limb width (cm)",
        "Patient weight (kg)",
        "Hip joint center height (cm, from ischium)",
        "Knee joint axis height (cm, from ischium)",
        "Prosthetic foot model",
        "SACH foot (fixed ankle, soft heel)",
        "Multi-axial foot",
        "Energy-storing foot",
        "Hydraulic foot",
        "Heel height (cm)",
        "Enter parameters to compute the alignment data",
        "Compute alignment parameters",
        "\U0001F4D6 Alignment principle reference",
        "Load line",
        "The load line is the vertical gravity line from the socket at the top of the prosthesis down to the prosthetic foot; correct alignment makes it pass through the appropriate positions of the key prosthetic components.",
        "Below-knee prosthesis alignment",
        "Sagittal plane: the load line passes just in front of the tibial tuberosity and lands at the mid-foot of the prosthetic foot (about one third behind the heel)",
        "Frontal plane: the load line passes through the midline of the tibia and lands at the center of the prosthetic foot",
        "Initial socket flexion angle: 5-10 degrees",
        "Above-knee prosthesis alignment",
        "Sagittal plane: the load line passes in front of the ischial support, behind the knee joint axis, and lands at the mid-foot",
        "Frontal plane: the load line passes medial to the ischial tuberosity, through the knee joint center and the center of the prosthetic foot",
        "Initial socket adduction angle: 5-10 degrees",
        "Knee stability: make sure the knee does not buckle in stance",
        "Effect of heel height",
        "Heel height changes affect sagittal alignment. With a 2 cm heel increase the prosthetic foot must move forward about 1 cm or the socket tilt back 2-3 degrees. Different heels need matching SACH heel stiffness.",
        "\U0001F4CC Calculation record",
        "\U0001F4DDA In-depth analysis: prosthesis alignment (load line) adjustment",
        "Below-knee prosthesis",
        "Above-knee prosthesis",
        "Alignment recheck",
        "Bearing pressure 1.9 N/cm2",
        "Weight 70 kg gives a load of 686 N, residual limb length 15 cm x width 12 cm: pressure = 686/(2 x 12 x 15) = 1.91 N/cm2; when the heel is above 2 cm the prosthetic foot shifts back 10 mm.",
        "Thigh adduction angle",
        "An above-knee prosthesis starts at 7 degrees of adduction, knee height minus hip height gives the thigh length, and the knee setback = thigh length x 5%, keeping the load line slightly in front of the knee.",
        "Does heel height affect alignment?",
        "When the heel is not 2 cm the prosthetic foot shifts fore and aft (above 2 it moves back 10 mm, below 2 it moves forward 10 mm), keeping the load line stable and avoiding knee hyperextension or buckling.",
        "Where does poor alignment show up first?",
        "Three typical signs: (1) localized tenderness on the inner or outer wall of the socket (frontal alignment too medial / lateral); (2) the body involuntarily leans to one side when standing or the limb swings out (sagittal alignment too anterior / posterior); (3) step width clearly increases and energy expenditure rises (fear caused by unstable alignment). The adjustment order should be sagittal plane (front-back) first, then frontal plane (medial-lateral), changing only one parameter at a time and walking 20 steps before reassessing.",
        "About the Prosthesis Alignment (Load Line) Adjustment Calculator",
        "Prosthesis Alignment (Load Line) Adjustment Calculator." + DISCL_M,
        "How to use the Prosthesis Alignment (Load Line) Adjustment Calculator",
        "What does the Prosthesis Alignment (Load Line) Adjustment Calculator do?",
        "Enter the amputee's residual limb parameters and the prosthetic geometry, and the tool computes the load line (LOAD line) position and the alignment offset, flags inversion and eversion risk, and helps prosthetists assemble and dynamically adjust the prosthesis for better stability while walking.",
        "How do I use the Prosthesis Alignment (Load Line) Adjustment Calculator?",
        "Which scenarios suit the Prosthesis Alignment (Load Line) Adjustment Calculator?",
        "e.g. 15",
        "e.g. 8",
        "e.g. 70",
        "e.g. 12",
        "e.g. 45",
        "e.g. 2",
    ]))
    write('respiratory-training', build('respiratory-training', [
        "\U0001F39A\ufe0f Respiratory Training (Maximal Inspiratory Pressure) Target Calculator",
        "Computes target values for maximal inspiratory pressure (MIP), maximal expiratory pressure (MEP) and a respiratory muscle training plan",
        "Core formulas (from the input variables): Math.ceil((targetMIP - currentMIP) / weeklyImprove); (currentMIP / predictedMIP x 100); (weight / (height / 100)^2)",
        "Current measured MIP (cmH2O)",
        "Clinical situation",
        "Healthy adult",
        "Stroke",
        "Spinal cord injury",
        "Ventilator weaning",
        "Enter parameters to compute the target value",
        "\U0001F4D6 Respiratory muscle strength reference",
        "MIP (maximal inspiratory pressure)",
        "Reflects inspiratory muscle strength",
        "MEP (maximal expiratory pressure)",
        "Reflects expiratory muscle strength",
        "SNIP (sniff nasal inspiratory pressure)",
        "Non-invasive inspiratory muscle test",
        "FVC (forced vital capacity)",
        "Predicted value +/- 20%",
        "Lung volume assessment",
        "PEF (peak expiratory flow)",
        "Expiratory muscle strength",
        "MIP predicted formula (Black & Hyatt)",
        "Male: MIP = 142 - (1.03 x age) cmH2O",
        "Female: MIP = 81 - (0.46 x age) cmH2O",
        "MEP predicted formula",
        "Male: MEP = 184 - (0.81 x age) cmH2O",
        "Female: MEP = 114 - (0.41 x age) cmH2O",
        "\U0001F4CC Training record",
        "\U0001F4DDA In-depth analysis: respiratory training (maximal inspiratory pressure) target values",
        "Preoperative pulmonary rehabilitation",
        "Weaning training",
        "MIP 75 in a 65-year-old male",
        "Male predictedMIP = 142 - 1.03 x 65 = 75.05 cmH2O; with a COPD factor of 0.6 the target is about 45 and the training load about 45 x 0.6 = 27, improving about 2 per week so the target is reached in roughly 15 weeks.",
        "Female reference",
        "Female predictedMIP = 81 - 0.46 x age; a current value below 60% of predicted indicates inspiratory muscle weakness and calls for a flow-resistive incentive spirometer (target volume 2000 ml per set).",
        "What is the MIP predicted formula?",
        "Male 142 - 1.03 x age, female 81 - 0.46 x age (cmH2O); a measured/predicted ratio below 60% indicates marked inspiratory muscle weakness.",
        "How is the training load set?",
        "A common plan uses 30% of the measured MIP as the starting load (some schemes use 50-60% but tolerance is poor), with 3-5 sets per session of 10 breaths each, 1-2 minutes rest between sets, 5 days a week, and retesting and raising the load after 4-8 weeks. A load that is too low (below 20% MIP) gives almost no training effect; too high easily causes respiratory muscle fatigue and dizziness. If oxygen saturation drops or marked breathlessness appears during training, reduce the load.",
        "About the Respiratory Training (Maximal Inspiratory Pressure) Target Calculator",
        "Respiratory Training (Maximal Inspiratory Pressure) Target Calculator." + DISCL_M,
        "e.g. 65",
        "e.g. 170",
        "e.g. 45",
    ]))


if __name__ == '__main__':
    main()