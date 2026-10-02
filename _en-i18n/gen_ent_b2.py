#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'ent')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'ent')
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
    out = {'slug': slug, 'industry': 'ent', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

DISCL_M = " A professional medical tool based on authoritative medical standards, for reference only."


def main():
    write('caloric-test', build('caloric-test', [
        "\U0001F442 Vestibular Function (Caloric Test) Semicircular Canal Assessor",
        "Computes unilateral weakness (UW) and directional preponderance (DP) from the slow-phase velocity of nystagmus under bithermal irrigation of both ears (44 \u00b0C warm and 30 \u00b0C cold), to assess lateral semicircular canal function.",
        "Slow-phase nystagmus velocity for each condition (\u00b0/s)",
        "Right ear warm irrigation (RW 44 \u00b0C)",
        "Warm stimulation \u2192 left-beating nystagmus",
        "Left ear warm irrigation (LW 44 \u00b0C)",
        "Warm stimulation \u2192 right-beating nystagmus",
        "Right ear cold irrigation (RC 30 \u00b0C)",
        "Cold stimulation \u2192 right-beating nystagmus",
        "Left ear cold irrigation (LC 30 \u00b0C)",
        "Cold stimulation \u2192 left-beating nystagmus",
        "Formulas and interpretation criteria",
        "Unilateral weakness (UW)",
        "UW above 20-25% suggests reduced function of one canal (canal paresis); a positive value means the right side is weaker and a negative value the left.",
        "Directional preponderance (DP)",
        "DP above 25-30% suggests a directional bias; a positive value means the bias is to the left and a negative value to the right, commonly seen with incomplete central vestibular compensation.",
        "Clinical points:",
        "Caloric testing mainly assesses the lateral semicircular canal and the superior vestibular nerve. An abnormal UW points to peripheral vestibular disease (such as Meniere's disease or vestibular neuritis), while an abnormal DP mostly reflects vestibular tone imbalance and can appear in peripheral or central lesions. Confirm there is no tympanic membrane perforation before testing.",
        "\U0001F4DA In-depth Analysis: Vestibular Function (Caloric Test) Semicircular Canal Assessor",
        "Differentiating the cause of vertigo (peripheral versus central).",
        "Quantifying unilateral vestibular hypofunction.",
        "Follow-up of vestibular neuritis.",
        "Right-sided UW elevated",
        "Caloric testing shows a reduced response in the right ear with UW=42% (abnormal above 25%), indicating reduced right peripheral vestibular function, consistent with right vestibular neuritis.",
        "What is the COWS rule?",
        "The rule for nystagmus direction during water irrigation: warm water on the same side and cold water on the opposite side both drive nystagmus towards the irrigated side (Cold Opposite, Warm Same), which is used for interpretation.",
        "What is the difference between UW and DP?",
        "UW reflects a reduced response of one canal (the affected side); DP reflects a directional skew from asymmetry between the two sides and can indicate central involvement or unilateral dominance.",
        "About \"Vestibular Function (Caloric Test) Semicircular Canal Assessor\"",
        "Vestibular Function (Caloric Test) Semicircular Canal Assessor." + DISCL_M,
    ]))

    write('eustachian-tube', build('eustachian-tube', [
        "\U0001F442 Eustachian Tube (Valsalva) Patency Assessor",
        "Assesses eustachian tube patency and grades dysfunction by combining the Valsalva manoeuvre, tympanometry, acoustic reflexes and subjective symptoms.",
        "Eustachian tube function score = the sum of the probe item scores (out of 18) \u2212 the number of symptom items (\u22121 each, up to \u22125); 16 or above is grade 0 normal, 12\u201316 is grade I mild, 8\u201312 is grade II, and lower is grade III/IV dysfunction.",
        "1. Valsalva manoeuvre assessment",
        "Tympanic membrane movement (observed with an otoscope)",
        "Clearly bulging outward",
        "Slightly bulging outward",
        "Almost no movement",
        "No movement",
        "Subjective sensation",
        "Airflow or a \"pop\" sound in the ear",
        "Sensation of fullness in the ear",
        "Slight sensation",
        "No sensation at all",
        "2. Tympanogram type",
        "Type A (normal)",
        "Type C (negative pressure)",
        "Type B (flat)",
        "Type Ad (high compliance)",
        "Type As (low compliance)",
        "3. Acoustic reflex status",
        "Ipsilateral acoustic reflex (500 Hz / 1000 Hz)",
        "Elicitable (normal)",
        "Threshold elevated",
        "Absent",
        "4. Toynbee test (swallowing with the nose pinched)",
        "Visible tympanic membrane movement",
        "Change in subjective sensation",
        "No change",
        "5. Symptom assessment",
        "Main symptoms (multiple selections affect the weighting)",
        "Ear fullness",
        "Hearing loss",
        "Autophony",
        "Tinnitus",
        "Ear pain",
        "No symptoms",
        "Eustachian tube dysfunction grading",
        "Normal eustachian tube function, no treatment needed",
        "Medication plus tube inflation, consider surgery",
        "Tympanostomy tube insertion or balloon dilation recommended",
        "Extremely severe dysfunction",
        "Surgical intervention needed, evaluate the cause",
        "Assessment notes:",
        "This assessor scores eustachian tube function quantitatively from the Valsalva manoeuvre, tympanogram, acoustic reflexes, Toynbee test and clinical symptoms, out of a total of 18 points. A higher score means better tubal opening function. The Valsalva manoeuvre is the most common clinical screening method and tympanometry is an important objective assessment tool.",
        "\U0001F4DA In-depth Analysis: Eustachian Tube (Valsalva) Patency Assessor",
        "After a cold, with ear fullness and hearing loss, use the Valsalva manoeuvre to see whether the tube can open and whether the fullness eases.",
        "For ear pain during pressure changes when flying or diving, assess the tube's regulatory ability and guide pressure-equalising actions such as swallowing and chewing.",
        "For long-standing ear fullness with autophony, check for a patulous eustachian tube (lax palatopharyngeal muscles).",
        "Ear fullness relieved after Valsalva",
        "The patient hears a \"POP\" in the ear after blowing with the nose pinched and the fullness eases, showing the tube can open and function is essentially normal; if repeated inflation brings no relief and the eardrum is retracted, obstructive dysfunction is indicated.",
        "How is the Valsalva manoeuvre performed?",
        "Pinch the nostrils, close the mouth and exhale forcefully so air passes through the tube into the middle ear; normally the fullness eases or a click is heard. Use with caution in patients with hypertension or heart failure.",
        "How do you distinguish a patulous tube from an obstructed one?",
        "Obstruction means insufficient opening (ear fullness, hearing loss, retracted eardrum), while patulous means incomplete closure (autophony, airflow sounds in the ear, fullness while speaking). The two call for opposite management.",
        "About \"Eustachian Tube (Valsalva) Patency Assessor\"",
        "It quantitatively assesses and grades eustachian tube opening function from the Valsalva manoeuvre, tympanogram, acoustic reflexes, Toynbee test and clinical symptoms.",
        "Five-dimensional comprehensive assessment",
        "Combining objective tests with symptoms",
        "Five-level dysfunction grading",
        "Provides treatment recommendations for reference",
        "Otitis media with effusion assessment",
        "Diagnosing eustachian tube dysfunction",
        "Preoperative middle ear function assessment",
        "ENT outpatient screening",
    ]))

    write('facial-nerve-hb', build('facial-nerve-hb', [
        "\U0001F9E0 Facial Nerve (House-Brackmann) Function Assessor",
        "Based on the House-Brackmann grading system (grades I-VI), it assesses the degree of facial nerve impairment for diagnosing and following up facial palsy.",
        "The House-Brackmann facial nerve grading runs from I to VI: grade I normal, II mild, III moderate, IV moderately severe, V severe and VI total paralysis; it is judged comprehensively from the forehead wrinkles, eye closure and mouth corner symmetry.",
        "House-Brackmann grading criteria",
        "Clinical use:",
        "The House-Brackmann grade is the international standard for assessing facial nerve function and is widely used to evaluate and follow up Bell's palsy, Hunt syndrome and traumatic facial palsy. Palsy above grade III indicates a poorer prognosis and needs active treatment. It can be combined with electroneurography (ENoG) to assess the degree of facial nerve degeneration, and degeneration above 90% calls for considering facial nerve decompression.",
        "\U0001F4DA In-depth Analysis: Facial Nerve (House-Brackmann) Function Assessor",
        "Grading and follow-up of Bell's palsy (idiopathic facial palsy).",
        "Assessing facial nerve tumours or surgical injury.",
        "Prognosis of traumatic facial palsy.",
        "House-Brackmann grade III",
        "Slightly weak brow lift, incomplete eye closure (Bell's sign positive) and air leaking when blowing the cheeks, with symmetry at rest, is graded HB III (moderate); steroids plus eye protection are recommended, with review in 2 weeks.",
        "What does the HB grade mainly look at?",
        "Symmetry at rest, the range of voluntary movement (forehead wrinkles, eye closure, mouth corner), and whether synkinesis or spasm is present; grade I is normal and grade VI is total paralysis.",
        "How long does recovery take?",
        "About 70-80% of Bell's palsy cases recover completely and grades HB I-II carry a good prognosis; no recovery within 3 weeks of onset, or progressive worsening, needs imaging to exclude a tumour or fracture.",
        "About \"Facial Nerve (House-Brackmann) Function Assessor\"",
        "Facial Nerve (House-Brackmann) Function Assessor." + DISCL_M,
    ]))

    write('fistula-test', build('fistula-test', [
        "\U0001F50D Fistula Test (Inner Ear Window) Examiner",
        "Applies positive and negative pressure to the external auditory canal and watches for nystagmus and vertigo, to assess whether a labyrinthine fistula (inner ear window fistula) is present.",
        "\"Applies positive and negative pressure to the external auditory canal and watches for nystagmus and vertigo, to assess whether a labyrinthine fistula (inner ear window fistula) is present.\" It performs a professional calculation from the input parameters and outputs the result.",
        "Test method and parameters",
        "Test ear side",
        "Positive pressure (mmH\u2082O)",
        "Negative pressure (mmH\u2082O)",
        "Observed response to pressure",
        "Nystagmus on positive pressure",
        "Nystagmus towards the tested side (ipsilateral) \u2014 suggests a fistula may be present",
        "Nystagmus on negative pressure",
        "Nystagmus towards the opposite side \u2014 suggests a fistula may be present",
        "Vertigo or falling on pressure",
        "The patient feels marked vertigo, or the body tilts or sways",
        "Tullio phenomenon positive",
        "Loud sound provokes vertigo or nystagmus",
        "Hennebert sign positive",
        "Negative pressure in the canal provokes nystagmus and vertigo, even without a fistula",
        "No response to pressure",
        "Neither positive nor negative pressure provokes nystagmus or vertigo",
        "Fistula test interpretation criteria",
        "Pressure provokes nystagmus plus vertigo",
        "Strongly suggests a labyrinthine fistula",
        "Vertigo alone without nystagmus, or the Hennebert sign alone",
        "A fistula cannot be excluded; combine with other tests",
        "No nystagmus, no vertigo",
        "Does not support a fistula diagnosis (false negative rate about 10-15%)",
        "Common fistula sites",
        "Frequency",
        "Lateral semicircular canal",
        "Chronic otitis media, cholesteatoma",
        "Vestibular window (oval window)",
        "Trauma, surgery, syphilis",
        "Cochlear window (round window)",
        "Trauma, blast injury, idiopathic",
        "Cautions:",
        "A negative fistula test cannot fully exclude a fistula, with a false negative rate of 10-15%. Diagnosis requires combining the clinical picture, temporal bone CT and surgical exploration. Do not apply excessive pressure during testing, to avoid injury. The Tullio phenomenon and Hennebert sign also occur in non-fistula diseases such as Meniere's disease and syphilis, so they must be differentiated.",
        "\U0001F4DA In-depth Analysis: Fistula Test (Inner Ear Window) Examiner",
        "Sudden vertigo after trauma or surgery: use the fistula test to check for a perilymph fistula.",
        "Differentiating Meniere's disease, where the test is usually negative.",
        "Screening for congenital semicircular canal dehiscence syndrome.",
        "Hennebert sign positive",
        "Negative pressure in the canal provokes rotational nystagmus and vertigo; a positive result suggests a semicircular canal fistula or perilymph fistula, and VEMP plus high-resolution CT is recommended for confirmation.",
        "Does a positive fistula test always mean a specific disease?",
        "It indicates a defect of the inner ear window or canal wall, such as a perilymph fistula or congenital dehiscence, but sensitivity is limited and a negative result cannot exclude it, so combine with VEMP and CT.",
        "How is it distinguished from positional vertigo?",
        "The fistula test is provoked by pressure in the ear canal and lasts as long as the pressure, while BPPV is provoked by head position changes and is brief (under 1 minute); the mechanisms differ.",
        "About \"Fistula Test (Inner Ear Window) Examiner\"",
        "The fistula test applies positive and negative pressure to the external auditory canal and watches for nystagmus and vertigo, to assess whether a labyrinthine (inner ear window) fistula is present.",
        "Supports custom positive and negative pressure values",
        "Checkbox assessment of multiple signs",
        "Automatic reading of positive, suspicious or negative",
        "Includes a reference table of fistula sites",
        "Preoperative assessment for chronic otitis media",
        "Vestibular testing after ear trauma",
        "ENT teaching demonstration",
    ]))


if __name__ == '__main__':
    main()
