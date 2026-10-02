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
    write('self-test-constitution', build('self-test-constitution', [
        "📝 Constitution (Balanced / Qi Deficiency / Yang Deficiency etc.) Self-Test",
        "Identify your TCM constitution type through a nine-constitution questionnaire based on the ZYYXH/T 157-2009 standard Classification and Determination of TCM Body Constitution",
        "Balanced constitution: do you have abundant energy?",
        "Balanced constitution: do you easily tire? (reverse)",
        "Qi deficiency constitution: do you often have shortness of breath or rapid breathing?",
        "Qi deficiency constitution: do you often feel anxious or palpitations?",
        "Yang deficiency constitution: do your hands and feet feel cold?",
        "Yang deficiency constitution: do you feel cold in the epigastrium, back or lower back and knees?",
        "Yin deficiency constitution: do you feel heat in your palms and soles?",
        "Yin deficiency constitution: do you have dry lips?",
        "Phlegm-dampness constitution: do you have a greasy sensation in your face or nose?",
        "Phlegm-dampness constitution: is your tongue coating thick and greasy?",
        "Damp-heat constitution: do you easily get acne on your face?",
        "Damp-heat constitution: do you have bitter taste or an unpleasant taste in your mouth?",
        "Blood stasis constitution: do you have bruises on your skin or darker than usual lips?",
        "Blood stasis constitution: do you have dark circles?",
        "Qi stagnation constitution: do you feel downcast and low in mood?",
        "Qi stagnation constitution: do you easily feel nervous or anxious?",
        "Inherent constitution: do you easily develop allergies (medication/food/pollen)?",
        "Inherent constitution: does your skin easily develop urticaria?",
        "Determine constitution type",
        "Copy constitution report",
        "About \"Constitution (Balanced / Qi Deficiency / Yang Deficiency etc.) Self-Test\"",
        "Identify your TCM constitution type through a standardised nine-constitution questionnaire based on the ZYYXH/T 157-2009 standard Classification and Determination of TCM Body Constitution, with constitution conditioning advice.",
        "Determination of 9 TCM constitutions",
        "60-item standardised questionnaire",
        "Automatic conversion score calculation",
        "Constitution conditioning advice",
        "Comparative result analysis",
        "Personal constitution identification",
        "TCM health management",
        "Pre-disease screening",
        "Community health services",
        "📚 Deep dive: constitution self-test determination",
        "Nine-constitution questionnaire",
        "Primary constitution identification",
        "Deviation summary",
        "Primary constitution determination",
        "All 9 types are scored, and the one with the highest score among those judged \"yes\" becomes the primary constitution; for example qi deficiency 72 and yang deficiency 55 give a primary report of \"qi deficiency constitution\" with the rest listed as deviations.",
        "All negative means balanced",
        "When all 9 types are \"no\" it indicates \"tendency to balanced constitution / yes\", the colour turns green, and this is the healthy baseline state.",
        "How does it relate to the constitution self-test tool?",
        "It uses the same nine-constitution system, but this version focuses on the determination report (primary constitution plus a list of deviations), whereas the self-test tool focuses on question-by-question entry.",
        "Can it serve as a diagnosis?",
        "It is a self-assessment for education only; formal constitution identification requires a licensed TCM practitioner combining all four diagnostic methods.",
        "The constitution classification follows the ZYYXH/T 157-2009 standard Classification and Determination of TCM Body Constitution",
        "The nine constitutions: balanced, qi deficiency, yang deficiency, yin deficiency, phlegm-dampness, damp-heat, blood stasis, qi stagnation and inherent",
        "Determination standard: a conversion score of 60 or above is judged \"yes\", 40-59 is \"tendency yes\", and below 40 is \"no\"",
        "The balanced constitution is the normal constitution; the other 8 are deviation constitutions",
        "Constitutions can overlap, so constitution identification and conditioning are best done under the guidance of a TCM practitioner",
    ]))

    write('tongue-diagnosis', build('tongue-diagnosis', [
        "🩺 Tongue Appearance Classification and Pathology Matcher",
        "Select the observed tongue body and coating features to automatically match the TCM tongue diagnosis pathology correspondence (based on the tongue diagnosis content of TCM Diagnostics)",
        "I. Tongue body (inspecting the tongue body)",
        "Tongue posture (dynamic)",
        "II. Tongue coating",
        "Analyse tongue appearance",
        "After selecting tongue features above, click \"Analyse tongue appearance\"",
        "⚠️ Tongue diagnosis should be done in natural light, and observation should not take too long (to avoid the tongue colour changing from prolonged protrusion). This tool is for TCM study reference only and cannot replace professional physician diagnosis.",
        "📋 Tongue diagnosis quick reference table",
        "Primary disease / primary syndrome",
        "Pale red tongue",
        "Normal tongue colour, qi and blood harmonised",
        "Qi and blood deficiency, yang deficiency with water dampness",
        "Red or crimson tongue",
        "Heat syndrome (excess heat / internal heat from yin deficiency)",
        "Swollen tongue with teeth marks",
        "Spleen deficiency with internal retention of water dampness",
        "Thin and narrow tongue",
        "Insufficiency of qi, blood and yin fluids",
        "Yin fluid depletion, blood deficiency",
        "Exterior syndrome, cold syndrome, normal",
        "Interior syndrome, heat syndrome",
        "Severe interior cold or interior heat syndrome",
        "📚 Deep dive: tongue appearance classification pathology",
        "Tongue body and coating",
        "Tongue shape and posture",
        "Primary disease derivation",
        "Pale tongue with white coating",
        "color=lightred (pale) + coatColor=white → \"deficiency cold syndrome, qi and blood deficiency or yang deficiency\", treated by warming and tonifying qi and blood.",
        "Red or crimson tongue with thin coating",
        "color=red + coatNature=peeled → \"internal heat from yin deficiency\", treated by nourishing yin and clearing heat; a swollen tongue with a thick greasy coating indicates spleen deficiency with dampness.",
        "Bluish-purple tongue with bruising",
        "color=purple → \"blood stasis syndrome\", treated by activating blood and resolving stasis; a stiff or deviated tongue posture suggests liver wind or phlegm obstruction, so watch for stroke.",
        "What is being looked at?",
        "The tongue body (pale red / red / crimson / purple / pale white) reflects qi, blood, yin and yang, while the coating (thickness, yellow, white, peeled) reflects the depth of the pathogen.",
        "Can a single tongue appearance determine a disease?",
        "No. All four diagnostic methods must be combined; the tool offers common primary disease combination hints.",
        "About \"Tongue Appearance Classification and Pathology Matcher\"",
        "Tongue Appearance Classification and Pathology Matcher - TCM tongue diagnosis tool mapping tongue body and coating features for comparison, seeing health from the tongue. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('spirit-observation', build('spirit-observation', [
        "🩺 Spirit Observation Standard Tool",
        "Judge the abundance or decline of the spirit from gaze, complexion, expression and posture, identifying full spirit, deficient spirit, lost spirit and false spirit (based on the spirit observation content of TCM Inspection)",
        "Spirit observation judges four aspects: gaze, complexion, expression and posture. Full spirit (bright gaze, lustrous complexion, clear consciousness, relaxed posture) means abundant essence and qi; deficient spirit (dull gaze, pale complexion, fatigue) means insufficient essence and qi; lost spirit (dim gaze, dull complexion, clouded mind and confused speech) means depleted essence and failing spirit; false spirit (sudden brightening in chronic illness, flushed face as if made up) is a critical sign of yin-yang separation.",
        "Step one: tick the observed findings",
        "Gaze and spirit",
        "Complexion and expression",
        "Posture and reaction",
        "Judge the abundance or decline of the spirit",
        "After ticking the observed findings, click \"Judge the abundance or decline of the spirit\"",
        "💡 Spirit observation is the first of inspection methods. The \"spirit\" is the outward manifestation of the body's life activity and reflects the strength of upright qi. Full spirit is favourable, lost spirit is critical, and false spirit signals impending death (the last flare of vitality).",
        "📋 Comparison of the four types of spirit",
        "Full spirit",
        "Abundant essence and qi, vigorous vitality",
        "Upright qi unharmed, mild illness, good prognosis",
        "Deficient spirit (insufficient spirit)",
        "Mildly insufficient essence and qi",
        "Upright qi damaged, seen in deficiency syndromes or convalescence",
        "Lost spirit (absent spirit)",
        "Greatly depleted essence and qi, failing spirit",
        "Upright qi severely damaged, serious illness, poor prognosis",
        "Essence and qi about to be exhausted, false vitality",
        "The last flare of vitality, a guttering lamp relit, a sign of impending danger",
        "📚 Deep dive: spirit observation standard",
        "Full spirit / lost spirit",
        "Deficient spirit / false spirit",
        "Combined reading of eyes, face and body",
        "Identifying false spirit",
        "Ticking items such as \"suddenly bright eyes, incessant speech, desire to eat\" gives the highest false-spirit score → judged \"false spirit\" (last flare), a critical warning sign.",
        "Full spirit determination",
        "Eyes with spirit, moist complexion, quick reaction give the most full-spirit hits → \"full spirit\", upright qi unharmed with good prognosis.",
        "How is the spirit observed?",
        "Focus on gaze, complexion, form and reaction; four levels of full spirit, deficient spirit, lost spirit and false spirit.",
        "Is false spirit dangerous?",
        "False spirit is a sudden apparent \"improvement\" before death and is extremely critical clinically. Never mistake it for recovery.",
        "About \"Spirit Observation Standard Tool\"",
        "Spirit Observation Standard Tool - TCM spirit observation tool comparing full spirit, deficient spirit, lost spirit and false spirit, judging upright qi strength from the spirit. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('auscultation', build('auscultation', [
        "📚 Auscultation and Olfaction Abnormality Descriptor",
        "Auscultation and olfaction cover both listening to sound and smelling odours, identifying patterns from abnormal sounds and smells (based on the content of TCM Auscultation and Olfaction)",
        "Auscultation and olfaction identify the nature of illness from sound and smell: a loud, forceful voice usually indicates excess syndrome while a low, weak voice indicates deficiency; coarse rapid breathing indicates excess while low short breathing indicates deficiency; foul breath usually indicates stomach heat and sour putrid breath indicates food stagnation; a heavy turbid cough sound indicates wind-cold while a dry cough with little phlegm indicates dryness or yin deficiency. Abnormal features are classified by excess, deficiency, cold and heat, outputting pattern hints.",
        "Select an abnormal finding to see its diagnostic meaning",
        "💡 Auscultation and olfaction together mean both \"listening\" and \"smelling\". Listening covers voice, breathing, cough, vomiting, belching, hiccups and the like; smelling covers body odours and the odour of excretions.",
        "📋 Quick reference for common abnormal sounds and odours",
        "Abnormal finding",
        "Pattern indicated",
        "Voice",
        "Excess syndrome, heat syndrome",
        "Deficiency syndrome, cold syndrome",
        "Coarse forceful breathing",
        "Faint weak breathing",
        "Excess syndrome (wind-cold / phlegm-dampness)",
        "Dry cough without phlegm",
        "Dryness pathogen or yin deficiency",
        "Sour foul breath",
        "Food stagnation in the stomach and intestines",
        "Foul breath",
        "Stomach heat / dental caries",
        "📚 Deep dive: auscultation and olfaction abnormalities",
        "Voice and breathing",
        "Cough and borborygmus",
        "Smelling odours",
        "Low and faint voice",
        "Selecting the \"low faint voice\" sound type → indicates qi deficiency; coarse breathing with phlegm rattling indicates phlegm-heat obstructing the lung, and the tool lists the features and their meanings.",
        "Selecting \"heavy turbid cough sound\" → wind-cold or phlegm-dampness, usually with thin white sputum; compare with a hoarse cough (yin deficiency with fire).",
        "What is being listened for?",
        "Voice, breathing, cough, vomiting, borborygmus and body odours, to differentiate excess, deficiency, cold and heat.",
        "Can it be quantified?",
        "It relies mainly on feature description and does not replace objective auscultation.",
        "About \"Auscultation and Olfaction Abnormality Descriptor\"",
        "Auscultation and Olfaction Abnormality Descriptor - TCM auscultation tool identifying abnormalities by listening to sound and smelling odours, with pattern analysis. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()