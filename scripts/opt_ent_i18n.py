#!/usr/bin/env python3
# 清理 ent 批英文 i18n 套话：_en_override 的 ed 后缀 "free online tool..." + 7 个占位 en 标题改真实名
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SL = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')

# 30 个 ent 工具的真实英文描述（ed）
EN_ED = {
    'ent/adenoid-grading': 'Grade adenoid hypertrophy by nasopharyngeal endoscopic occlusion: I (≤25%), II (26–50%), III (51–75%), IV (>75%), or by the adenoid/nasopharynx (A/N) ratio.',
    'ent/ahi-severity': 'Estimate obstructive sleep apnea severity from the Apnea–Hypopnea Index (AHI): normal <5, mild 5–15, moderate 15–30, severe >30 events/hour.',
    'ent/allergy-skin-test': 'Interpret skin prick test (SPT) wheal diameters against negative and positive controls to grade allergen sensitization.',
    'ent/analysis-13': 'Acoustic analysis of vocal function for recurrent laryngeal nerve paresis: maximum phonation time, jitter, shimmer, and harmonics-to-noise ratio.',
    'ent/assessor-6': 'Assess vocal fold mobility under laryngoscopy: normal, paresis, or paralysis, with compensatory patterns.',
    'ent/assessor-7': 'Perceptual GRBAS rating of dysphonia: Grade, Roughness, Breathiness, Asthenia, Strain.',
    'ent/calc-1': 'Total Nasal Symptom Score (TNSS) for allergic or perennial rhinitis: rhinorrhea, sneezing, nasal itch, and congestion, each scored 0–3.',
    'ent/caloric-test': 'Caloric (bithermal) test for semicircular canal function: warm/cold irrigation, nystagmus duration, and unilateral weakness / canal paresis.',
    'ent/checker-1': 'Fistula test for inner-ear window (oval/round) dehiscence: pressure-induced vertigo and nystagmus.',
    'ent/eustachian-tube': 'Assess Eustachian tube function via Valsalva, Toynbee, and Politzer maneuvers with a symptom-based patency score.',
    'ent/facial-nerve-hb': 'House–Brackmann facial nerve grading from I (normal) to VI (total paralysis) by motion and symmetry.',
    'ent/fistula-test': 'Fistula test for inner-ear window (oval/round) dehiscence: pressure-induced vertigo and nystagmus.',
    'ent/gag-reflex': 'Grade gag reflex sensitivity: absent, diminished, normal, or hyperactive.',
    'ent/grbas-scale': 'Perceptual GRBAS rating of dysphonia: Grade, Roughness, Breathiness, Asthenia, Strain.',
    'ent/hearing-loss-classification': 'Classify hearing loss by pure-tone audiometry: conductive, sensorineural, or mixed, and degree by the four-frequency PTA.',
    'ent/laryngeal-nerve': 'Acoustic analysis of vocal function for recurrent laryngeal nerve paresis: maximum phonation time, jitter, shimmer, and harmonics-to-noise ratio.',
    'ent/lund-kennedy-score': 'Lund–Kennedy endoscopic score: polyps, edema, discharge, scarring, and crusting, each 0–2 per side.',
    'ent/lund-mackay-score': 'Lund–Mackay CT score for chronic rhinosinusitis: 0–2 per sinus plus the ostiomeatal complex.',
    'ent/nasal-resistance': 'Measure nasal airway resistance by anterior rhinomanometry: inspiratory and expiratory flow–pressure curves.',
    'ent/pure-tone-audiometry': 'Web Audio pure-tone screening across 8 frequencies per ear with ascending thresholds and an auto-drawn, WHO-graded audiogram.',
    'ent/rater-10': 'Lund–Mackay CT score for chronic rhinosinusitis: 0–2 per sinus plus the ostiomeatal complex.',
    'ent/rater-9': 'Lund–Kennedy endoscopic score: polyps, edema, discharge, scarring, and crusting, each 0–2 per side.',
    'ent/tdi-score': "Sniffin' Sticks TDI olfaction score: Threshold, Discrimination, and Identification (≤15.5 anosmia, 16–30 hyposmia).",
    'ent/temporal-resolution-hearing': 'Web Audio temporal resolution test: gap detection (GDT) and amplitude-modulation detection (AMD) with a 2-IFC adaptive staircase against age norms.',
    'ent/tester-rater-1': "Sniffin' Sticks TDI olfaction score: Threshold, Discrimination, and Identification (≤15.5 anosmia, 16–30 hyposmia).",
    'ent/tinnitus-matching': 'Tinnitus matching of the phantom sound: pitch (frequency) and loudness (dB) relative to threshold.',
    'ent/tonsil-grading': 'Tonsil grading I–IV by protrusion beyond the anterior pillars toward the midline.',
    'ent/tympanic-perforation': 'Estimate tympanic membrane perforation area and the associated conductive hearing loss.',
    'ent/tympanometry': 'Tympanometry typing (A/B/C) by middle-ear pressure and compliance to classify effusion or Eustachian tube dysfunction.',
    'ent/vocal-cord-assessment': 'Assess vocal fold mobility under laryngoscopy: normal, paresis, or paralysis, with compensatory patterns.',
}

# 7 个占位 en 标题 -> 真实英文名
EN_TITLE = {
    'ent/analysis-13': 'Laryngeal Nerve Acoustic Analysis',
    'ent/assessor-6': 'Vocal Cord Assessment',
    'ent/assessor-7': 'GRBAS Dysphonia Rating',
    'ent/checker-1': 'Fistula Test',
    'ent/rater-9': 'Lund–Kennedy Endoscopic Score',
    'ent/rater-10': 'Lund–Mackay CT Score',
    'ent/tester-rater-1': 'TDI Olfaction Test',
}

TAIL = ' 100% client-side, no data uploaded.'

sl = json.load(open(SL, encoding='utf-8'))
ov = json.load(open(OV, encoding='utf-8'))

n_ed = 0
n_title = 0
for k in EN_ED:
    new_ed = EN_ED[k] + TAIL
    # slug-en
    if k in sl and isinstance(sl[k], dict):
        if sl[k].get('ed') != new_ed:
            sl[k]['ed'] = new_ed
            n_ed += 1
    # _en_override
    if k in ov and isinstance(ov[k], dict):
        if ov[k].get('ed') != new_ed:
            ov[k]['ed'] = new_ed
            n_ed += 1
    # 占位标题修正（slug-en + override 的 en）
    if k in EN_TITLE:
        if k in sl and isinstance(sl[k], dict) and sl[k].get('en') != EN_TITLE[k]:
            sl[k]['en'] = EN_TITLE[k]; n_title += 1
        if k in ov and isinstance(ov[k], dict) and ov[k].get('en') != EN_TITLE[k]:
            ov[k]['en'] = EN_TITLE[k]; n_title += 1

json.dump(sl, open(SL, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(ov, open(OV, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ed updated:', n_ed, '| en titles fixed:', n_title)
