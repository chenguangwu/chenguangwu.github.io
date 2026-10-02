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
    write('gag-reflex', build('gag-reflex', [
        "\U0001F4CB Gag Reflex (Sensitivity) Grader",
        "Grades the sensitivity of the gag reflex, helping to judge glossopharyngeal and vagus nerve function and its clinical significance.",
        "Gag reflex grading runs from 0 to 4: 0 absent, 1 diminished, 2 normal, 3 hyperactive, 4 extremely sensitive; 0 and 1 suggest glossopharyngeal or vagus nerve damage, while 3 and 4 suggest an upper motor neuron lesion (pseudobulbar palsy).",
        "Gag reflex sensitivity grading",
        "Grade 0",
        "Reflex absent",
        "Reflex diminished",
        "Reflex normal",
        "Reflex hyperactive",
        "Hyperactive with nausea and vomiting",
        "Gag reflex grading explained",
        "No response on stimulating the posterior pharyngeal wall",
        "Absent reflex, suggesting glossopharyngeal or vagus nerve damage (bulbar palsy, medullary lesions and similar)",
        "Weak response after stimulation",
        "A diminished reflex, which can be seen in advanced age, neurodegenerative disease or peripheral nerve injury",
        "A normal vomiting reflex after stimulation",
        "Normal gag reflex with intact glossopharyngeal and vagus nerve function",
        "Even slight stimulation provokes a strong reflex",
        "A hyperactive reflex, suggesting an upper motor neuron lesion (pseudobulbar palsy and similar)",
        "Hyperactive reflex with nausea and vomiting",
        "Extremely sensitive, interfering with oral examination and treatment; seen with psychological factors or neurosis",
        "Examination method",
        "Procedure",
        "Ask the patient to open the mouth and gently stimulate the posterior pharyngeal wall or the palatoglossal arch with a tongue depressor",
        "Observe the pharyngeal muscle contraction (soft palate elevation, constrictor contraction)",
        "Test each side separately and compare the two responses",
        "Record the reflex strength and whether nausea or vomiting accompanies it",
        "Explain the procedure to the patient beforehand to gain cooperation",
        "Use moderate stimulation and avoid overstimulating, which can provoke vomiting",
        "The gag reflex can be inconspicuous in some healthy people, so judge it together with other neurological signs",
        "An absent gag reflex is not necessarily pathological, since some people are born with a weak reflex",
        "Nerve supply:",
        "The afferent limb of the gag reflex is the glossopharyngeal nerve (CN IX) and the efferent limb is the vagus nerve (CN X), with the reflex centre in the medulla. Bilateral absence with tongue atrophy and fasciculation indicates bulbar palsy (true medullary palsy), while a hyperactive reflex with forced crying and laughing indicates pseudobulbar palsy.",
        "\U0001F4DA In-depth Analysis: Gag Reflex (Sensitivity) Grader",
        "Assessing the gag reflex and aspiration risk in patients with dysphagia.",
        "Screening for bulbar palsy after stroke.",
        "Airway assessment before general anaesthesia or intubation.",
        "Absent gag reflex",
        "Stimulating the posterior pharyngeal wall with a tongue depressor produces no retching; the absent gag reflex together with choking on water suggests bulbar palsy, so a swallowing study and aspiration assessment are needed.",
        "Is an absent gag reflex always abnormal?",
        "Some healthy people have a weak or absent reflex, especially the elderly, so consider swallowing function too; a sudden absence with choking warrants suspicion of nerve damage.",
        "Which cranial nerves are involved?",
        "The afferent limb is the glossopharyngeal nerve (IX) and the efferent limb the vagus nerve (X), with bilateral corticobulbar supply, so unilateral damage can weaken the reflex.",
        "About \"Gag Reflex (Sensitivity) Grader\"",
        "Gag Reflex (Sensitivity) Grader." + DISCL_M,
    ]))

    write('grbas-scale', build('grbas-scale', [
        "\U0001F4CB Voice (GRBAS) Auditory-Perceptual Assessor",
        "The GRBAS scale is an auditory-perceptual voice assessment standard set by the Japan Society of Logopedics and Phoniatrics, in which the rater scores five voice dimensions from 0 to 3.",
        "GRBAS voice total = overall grade G + roughness R + breathiness B + asthenia A + strain S (0 to 3 each), out of 15; 0 is normal, up to 3 mild, up to 7 moderate and above 7 severe abnormality.",
        "G - overall grade",
        "The overall degree of voice abnormality",
        "R - roughness",
        "The psychoacoustic impression of irregular voice fluctuation, such as a raspy or rough quality",
        "B - breathiness",
        "The psychoacoustic impression of air escape in the voice, such as a hissing or breathy quality",
        "A - asthenia",
        "The psychoacoustic impression of weakness or frailty in the voice",
        "S - strain",
        "The psychoacoustic impression of excessive effort or tension in the voice",
        "Assessment notes:",
        "GRBAS scoring must be done by an experienced voice rater through auditory perception. A standardised speech sample (a sustained /a/ vowel plus reading a short passage) is recommended. The total runs from 0 to 15, with the G score as the main reference, while the sub-items reveal the characteristic features of the voice disorder.",
        "\U0001F4DA In-depth Analysis: Voice (GRBAS) Auditory-Perceptual Assessor",
        "Grading the voice in vocal fold polyps or nodules.",
        "Follow-up during voice training.",
        "Differentiating spasmodic dysphonia.",
        "GRBAS rating",
        "G2 R2 B1 A0 S0 indicates moderate roughness with mild breathiness, consistent with a vocal fold mass or incomplete closure, so laryngoscopy is recommended.",
        "How does GRBAS relate to acoustic analysis?",
        "GRBAS is a subjective perceptual grade and acoustics (jitter, shimmer, HNR) give objective parameters; the two complement each other and improve reliability.",
        "Who performs the assessment?",
        "A trained speech therapist or ENT physician makes the judgement, and averaging several raters reduces bias.",
        "About \"Voice (GRBAS) Auditory-Perceptual Assessor\"",
        "\uFE0F Voice (GRBAS) Auditory-Perceptual Assessor." + DISCL_M,
    ]))

    write('hearing-loss-classification', build('hearing-loss-classification', [
        "\U0001F442 Hearing Loss (Pure Tone Audiometry) Classifier",
        "Computes the PTA from air and bone conduction thresholds on pure tone audiometry, and classifies the degree and type of hearing loss (conductive, sensorineural or mixed).",
        "Core formulas (by input variable): Math.round((ac[0] + ac[1] + ac[2] + ac[3]) \u00f7 4); Math.round((ac[0] + ac[1] + ac[2]) \u00f7 3); Math.round((bc[0] + bc[1] + bc[2]) \u00f7 3)",
        "Right ear",
        "Left ear",
        "Air conduction threshold (dB HL)",
        "Air conduction",
        "Bone conduction threshold (dB HL)",
        "Bone conduction",
        "WHO hearing loss grading criteria",
        "Normal hearing",
        "Difficulty hearing soft speech",
        "Difficulty with ordinary conversation",
        "Difficulty with loud conversation",
        "Almost no speech heard",
        "PTA is the mean of the air conduction thresholds at 500, 1000 and 2000 Hz. The air-bone gap (ABG) = PTA (air conduction) \u2212 PTA (bone conduction). An ABG above 10 dB indicates a conductive component, and a bone conduction threshold above 25 dB a sensorineural component.",
        "\U0001F4DA In-depth Analysis: Hearing Loss (Pure Tone Audiometry) Classifier",
        "Grading abnormal results in newborn and child hearing screening.",
        "Occupational assessment of noise-induced hearing loss.",
        "Indications for hearing aids or cochlear implants.",
        "Moderate sensorineural",
        "A four-frequency average threshold of 55 dB HL with both air and bone conduction raised (gap under 10 dB) is a moderate sensorineural hearing loss, and a hearing aid is recommended.",
        "Why is the average taken over these four frequencies?",
        "500-4000 Hz covers the main speech frequencies, and the average threshold best reflects speech understanding; this is the internationally used grading method.",
        "How are conductive and sensorineural losses distinguished?",
        "Poor air conduction with normal bone conduction is conductive (outer or middle ear); both poor with a gap under 10 dB is sensorineural (inner ear or retrocochlear); a gap above 10 dB is mixed.",
        "About \"Hearing Loss (Pure Tone Audiometry) Classifier\"",
        "Hearing Loss (Pure Tone Audiometry) Classifier." + DISCL_M,
    ]))

    write('index', build('index', [
        "\U0001F442 ENT Tools",
        "ENT",
        "ENT Tools",
        "Auditory temporal resolution test",
        "An experimental Web Audio hearing test. It includes two paradigms, gap detection and modulation detection, uses a 2-IFC adaptive staircase to estimate millisecond-level thresholds, and compares them against reference ranges for children, young adults and older adults. Please take it in a quiet environment wearing headphones\u2026",
        "Rhinitis symptom score",
        "The Total Nasal Symptom Score (TNSS) quantifies the severity of allergic or chronic rhinitis symptoms.",
        "Pure tone hearing screening and audiogram",
        "A pure front-end Web Audio tool: it generates pure tones at 125 / 250 / 500 / 1000 / 2000 / 4000 / 8000 Hz with AudioContext and applies an ascending method ear by ear\u2026",
        "Assesses eustachian tube patency and grades dysfunction by combining the Valsalva manoeuvre, tympanometry, acoustic reflexes and subjective symptoms.",
        "Computes unilateral and total nasal resistance from rhinomanometry data to assess nasal ventilation.",
        "Applies positive and negative pressure to the external auditory canal and watches for nystagmus and vertigo, to assess whether a labyrinthine fistula is present.",
        "Based on the Lund-Mackay scoring system, it grades CT severity in chronic rhinosinusitis, scoring each sinus's opacification from 0 to 2 and the ostiomeatal complex 0 or 2.",
        "Based on the House-Brackmann grading system (grades I-VI), it assesses the degree of facial nerve impairment for diagnosing and following up facial palsy.",
        "Enter the diameter and quadrant of a tympanic membrane perforation and the tool estimates the share of eardrum area it occupies plus the expected degree of hearing loss, for preliminary ENT reference only.",
        "Computes the PTA from air and bone conduction thresholds on pure tone audiometry and classifies the degree and type of hearing loss (conductive / sensorineural / mixed).",
        "Assesses vocal fold movement by laryngoscopy, judging mobility, the fixed position and glottic closure, to help diagnose vocal fold paralysis.",
        "Based on nasal endoscopy findings, it scores nasal polyps, oedema, discharge, scarring and crusting bilaterally in chronic rhinosinusitis, for a total of 0-20 points.",
        "Semi-quantitative grading of skin prick test (SPT) wheal diameters against the histamine positive control.",
        "Vestibular caloric test assessor. Enter the nystagmus parameters for both sides and compute canal weakness and directional preponderance with the UW/DP formulas; UW above 20-25% suggests canal paresis and DP above 25-30% a directional bias, used to diagnose vertigo and balance disorders.",
        "Records a patient's tinnitus pitch-match frequency and loudness-match value, classifies the acoustic characteristics of the tinnitus and supports clinical assessment, for ENT audiology and as a reference when planning tinnitus rehabilitation.",
        "Based on the three sub-tests of the Sniffin' Sticks olfactory test (threshold T, discrimination D, identification I), it computes the total TDI score and classifies olfactory function.",
        "The GRBAS scale is an auditory-perceptual voice assessment standard set by the Japan Society of Logopedics and Phoniatrics, in which the rater scores five voice dimensions from 0 to 3.",
        "Grades the sensitivity of the gag reflex, helping to judge glossopharyngeal and vagus nerve function and its clinical significance.",
        "Based on the Brodsky criteria, it grades the tonsils by the proportion of the oropharyngeal width they occupy and assesses surgical indications together with clinical symptoms.",
        "Computes the AHI and RDI from polysomnography (PSG) data to assess the severity of obstructive sleep apnoea (OSA).",
        "Enter voice acoustic analysis parameters to assess vocal fold vibration stability, supporting the objective diagnosis and follow-up of recurrent laryngeal nerve paralysis.",
        "Grades adenoid hypertrophy by the proportion of choanal obstruction seen on nasopharyngoscopy and assesses surgical indications together with clinical symptoms.",
        "Enter the tympanogram peak pressure (dPa) and compliance (mL) to classify it automatically (Jerger types A / As / Ad / B / C) and plot the tympanogram curve.",
        "About \"ENT Tools\"",
        "The ENT tools collection gathers 23 free online tools covering the common calculations, conversions and lookups needed in ENT scenarios. Whether you are a practitioner in the field, a student or a casual user, you will find handy tools here that work the moment you open them. All tools run purely in the browser and no data is uploaded to a server, so your privacy stays safe.",
        "The ENT tools listed on this page include (a selection of representative tools):",
        "These tools help you finish common ENT tasks quickly, with no need to memorize complex formulas or convert values by hand \u2014 just enter them and get results.",
        "Do the ENT tools need to be downloaded or registered?",
        "No. Every ENT tool on this page is a pure front-end online tool \u2014 open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the ENT tools' results accurate? Is my data safe?",
        "The tools compute locally in your browser using public formulas and common industry standards, so results appear instantly. All calculations run on your own device and no data is uploaded to a server, keeping your privacy secure.",
    ]))


if __name__ == '__main__':
    main()
