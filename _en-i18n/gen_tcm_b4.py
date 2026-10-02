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
    write('san-jiao-differentiation', build('san-jiao-differentiation', [
        "🌿 Three-Therb Burn Differentiation Locator",
        "Wu Jutong's three-jiao differentiation divides warm diseases into upper, middle and lower jiao to locate the disease position and judge progression (transmitting from top to bottom)",
        "Three-jiao differentiation follows progression from top downward: upper jiao (lung and heart) shows fever with aversion to cold, cough and clouded mind; middle jiao (spleen and stomach) shows high fever, abdominal fullness, constipation or loose stool; lower jiao (liver and kidney) shows low fever, writhing of the limbs, convulsions and bowel and bladder dysfunction. Judge the current position and stage of transmission in the order upper, middle, lower; sequential transmission is normal while reverse transmission is dangerous.",
        "Click to select the jiao position",
        "View the pattern and treatment",
        "After selecting the jiao position, view the detailed pattern and treatment",
        "💡 Transmission rule: warm disease begins in the upper jiao (lung and wei level) → middle jiao (spleen and stomach) → lower jiao (liver and kidney), from top to bottom and from mild to severe. \"Treat the upper jiao like a feather, the middle jiao like a balance, the lower jiao like a counterweight.\"",
        "📋 Zang-fu of the three jiao and their patterns and treatments",
        "Three jiao",
        "Associated zang-fu",
        "Main patterns",
        "Treatment characteristics",
        "Upper jiao",
        "Lung, pericardium",
        "Fever with cough (lung) / clouded mind with delirium (pericardium)",
        "Light, clear and dispersing (like a feather)",
        "Middle jiao",
        "Spleen, stomach",
        "High fever with constipation (Yangming) / fever not felt on the body (Taiyin)",
        "Clearing, draining and purging (like a balance)",
        "Lower jiao",
        "Liver, kidney",
        "Writhing of the limbs (liver) / low fever with malar flush (kidney)",
        "Nourishing yin and subduing yang (like a counterweight)",
        "📚 Deep dive: three-jiao differentiation localisation",
        "Warm disease staging",
        "Upper, middle and lower jiao",
        "Transmission localisation",
        "Upper jiao lung and wei level",
        "Selecting the upper jiao (lung / pericardium) → fever with aversion to cold, cough and floating rapid pulse, meaning the pathogen is in the lung and wei level at the early stage of a warm disease; acrid-cool exterior dispersal is indicated.",
        "Middle jiao spleen and stomach",
        "Selecting the middle jiao (stomach / spleen) → high fever with sweating and thirst, yellow dry coating, Yangming stomach heat, treated by clearing qi and draining heat (Bai Hu and Cheng Qi type formulas).",
        "What does three-jiao differentiation identify?",
        "The Ming and Qing warm disease school locates the depth of warm disease by upper (lung and pericardium), middle (stomach and spleen) and lower (liver and kidney).",
        "What about the lower jiao?",
        "The lower jiao covers liver and kidney; when heat consumes yin there, palms and soles feel hot and the tongue is crimson with little coating, treated by nourishing yin and subduing yang.",
        "About \"Three-Therb Burn Differentiation Locator\"",
        "Three-Therb Burn Differentiation Locator - warm disease three-jiao differentiation tool analysing the upper, middle and lower jiao position localisation by Wu Jutong. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('wei-qi-ying-xue', build('wei-qi-ying-xue', [
        "🧪 Wei-Qi-Ying-Xue Transmission Simulator",
        "Ye Tianshi's differentiation system for warm-heat disease, reflecting the layers of transmission from exterior to interior and from mild to severe (wei → qi → ying → xue)",
        "Wei, qi, ying and xue differentiate by transmission layer: the wei level (fever with slight aversion to cold, headache, floating rapid pulse) is the onset of an exterior syndrome; the qi level (high fever, no aversion to cold, sweating, flooding rapid pulse) is flourishing internal heat; the ying level (fever worse at night, restlessness and insomnia, crimson tongue) is heat scorching ying yin; the xue level (maculae and rash, bleeding, deep crimson tongue) is heat blazing and stirring blood. Judge the layer in the order wei, qi, ying, xue, with treatments of acrid-cool exterior release, clearing heat and draining fire, clearing ying and driving heat out, and cooling blood and dispersing stasis respectively.",
        "Select the current depth layer",
        "Simulate transmission",
        "Click a layer above to view its patterns, or click \"Simulate transmission\" to see the transmission path",
        "💡 Transmission rule: wei → qi → ying → xue is sequential transmission (shallow to deep); wei → ying or xue is reverse transmission (into the pericardium) and is critical. Ye Tianshi said: \"In the wei level, sweating suffices; at qi level only then may qi be cleared; entering ying one may still drive heat out of ying; entering xue one fears consuming and stirring blood, so cool the blood and disperse stasis at once.\"",
        "📋 The four layers of wei, qi, ying and xue differentiation",
        "Depth of location",
        "Wei level syndrome",
        "Shallowest (exterior)",
        "Fever with slight aversion to cold, headache, cough, thin white coating, floating rapid pulse",
        "Acrid-cool exterior release",
        "Qi level syndrome",
        "Shallower (interior)",
        "High fever without aversion to cold, much sweating with thirst, red tongue with yellow coating, rapid pulse",
        "Clear qi and drain heat",
        "Ying level syndrome",
        "Deeper",
        "Fever worse at night, restlessness and insomnia, faint maculae, crimson tongue, thready rapid pulse",
        "Clear ying and drive heat out",
        "Xue level syndrome",
        "Deepest",
        "High fever with bleeding, maculae fully revealed, clouded mind with delirium, deep crimson tongue",
        "Cool blood and disperse stasis",
        "📚 Deep dive: wei, qi, ying and xue transmission",
        "Four layers of warm disease",
        "Sequential and reverse transmission",
        "Path simulation",
        "Sequential path",
        "Selecting \"qi level\" → forward path \"wei → qi → ying → xue\" and reverse \"xue ← ying ← qi ← wei\"; used to teach transmission and the moment of interception.",
        "Reverse transmission into the pericardium",
        "If the wei level is not transmitted sequentially but falls straight into the pericardium (clouded mind with delirium), the tool flags \"reverse transmission\" and indicates emergency treatment with cooling and orifice-opening (An Gong Niu Huang type formulas).",
        "What do the four layers mean?",
        "Wei (exterior heat), qi (flourishing internal heat), ying (heat entering the ying level and disturbing the mind) and xue (stirring and consuming blood), from shallow to deep.",
        "How does it differ from the three jiao?",
        "Ye Tianshi's wei-qi-ying-xue focuses on the depth of warm disease while Wu Jutong's three jiao focuses on location; the two are often read together.",
        "About \"Wei-Qi-Ying-Xue Transmission Simulator\"",
        "Wei-Qi-Ying-Xue Transmission Simulator - warm-heat disease wei, qi, ying and xue differentiation tool analysing layer transmission in Ye Tianshi's warm disease system. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('zang-fu-differentiation', build('zang-fu-differentiation', [
        "🌿 Zang-Fu Differentiation Pattern Combiner",
        "Select a zang-fu organ to view common pattern types, click a pattern to see its pattern combination, treatment method and formula (based on the content of TCM Zang-Fu Differentiation)",
        "Select zang-fu organ",
        "Common pattern types",
        "After selecting the organ and pattern, view the detailed differentiation",
        "💡 Zang-fu differentiation is the core of differentiating internal injury and miscellaneous diseases. Clinically one must identify the disease location (which zang, which fu) and the disease nature (deficiency, excess, cold, heat), combining them into a complete pattern name such as \"heart qi deficiency\" or \"liver yang rising\".",
        "🌿 Physiological functions and pathological manifestations of the five zang",
        "Zang-fu",
        "Main function",
        "Orifice / manifestation",
        "Governs blood vessels, stores the shen",
        "Palpitations, insomnia, mental abnormalities",
        "Opens into the tongue, manifests in the face",
        "Governs free coursing, stores blood",
        "Flank pain, emotional abnormality, irregular menstruation",
        "Opens into the eyes, manifests in the nails",
        "Governs transportation and transformation, holds the blood",
        "Abdominal distension and poor appetite, loose stool and oedema",
        "Opens into the mouth, manifests in the lips",
        "Governs qi, controls respiration",
        "Cough and asthma, weakness of the defensive exterior",
        "Opens into the nose, manifests in the body hair",
        "Stores essence, governs water",
        "Weak lower back and knees, abnormal growth and development",
        "Opens into the ears, manifests in the hair",
        "📚 Deep dive: zang-fu differentiation combinations",
        "Zang-fu localisation",
        "Pattern combinations",
        "Formula and pattern correspondence",
        "Heart qi deficiency",
        "Selecting \"heart\" + \"qi deficiency\" → \"heart qi deficiency syndrome\": palpitations, shortness of breath and fatigue, treated by nourishing the heart and boosting qi (Zhi Gan Cao Tang and Gui Pi type formulas).",
        "Liver yang rising",
        "Selecting \"liver\" + \"hyperactive yang\" → dizziness, blurred vision and flushed face, treated by soothing the liver and subduing yang (Tian Ma Gou Teng Yin).",
        "What is zang-fu differentiation?",
        "It centres on dysfunction of the physiological functions of the five zang and six fu, combining localisation and characterisation of the pathogenesis into a pattern.",
        "Can it span organs?",
        "Yes, combinations such as heart and spleen deficiency are possible; the tool lists candidate patterns per organ for selection.",
        "About \"Zang-Fu Differentiation Pattern Combiner\"",
        "Zang-Fu Differentiation Pattern Combiner - TCM tool identifying patterns of the five zang (heart, liver, spleen, lung, kidney) with zang-fu pattern analysis. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('index', build('index', [
        "🩺 TCM Diagnosis Tools",
        "TCM Diagnosis",
        "TCM Diagnosis Tools",
        "Following the standard structure, this guides entry of chief complaint, present history and the four diagnostic methods (inspection, auscultation and olfaction, inquiry and palpation), automatically applying TCM medical record templates to generate structured record text for standardised writing and electronic archiving of TCM outpatient records.",
        "\"One asks about chills and fever, two about sweating, three about head and body, four about the bowels, five about diet, six about chest and abdomen, seven about hearing, eight about thirst - all must be differentiated, nine about past illness and ten about cause\" - structured TCM inquiry record",
        "A logic tree of TCM aetiology categories, expanding to view external pathogenic factors, internal injuries and other causative factors with their pathogenic characteristics (based on TCM Aetiology)",
        "TCM Inquiry (Ten Questions Verse) Auto-Generated Questionnaire",
        "The inquiry questionnaire generator (Ten Questions Verse) structures TCM inquiry questionnaires following the Ten Questions Verse, covering chills and fever, sweating, head and body, bowels and urination and more, assisting history collection in TCM.",
        "Syndrome Element Combination Deriver",
        "Zhu Wenfeng's \"syndrome element differentiation\" system: select disease-location elements and disease-nature elements to automatically derive the complete syndrome name (location plus nature)",
        "Identify your TCM constitution type through a nine-constitution questionnaire based on the ZYYXH/T 157-2009 standard Classification and Determination of TCM Body Constitution",
        "Ye Tianshi's differentiation system for warm-heat disease, reflecting the layers of transmission from exterior to interior and from mild to severe (wei → qi → ying → xue)",
        "Three-Therb Burn Differentiation Locator",
        "Wu Jutong's three-jiao differentiation divides warm diseases into upper, middle and lower jiao to locate the disease position and judge progression (transmitting from top to bottom)",
        "Select a zang-fu organ to view common pattern types, click a pattern to see its pattern combination, treatment method and formula (based on the content of TCM Zang-Fu Differentiation)",
        "Presents real TCM misdiagnosis cases where the user answers to identify the pattern from the four diagnostic findings; the system gives the correct answer and reasoning analysis, training TCM differentiation reasoning and sharpening differential diagnosis of easily confused patterns and clinical judgement.",
        "Enter a TCM pattern type or symptom (such as fever or fatigue) to search for matching classical formulas, listing composition, actions and indications with sources, assisting formula selection and formula study in TCM syndrome-based treatment.",
        "Judge the abundance or decline of the spirit from gaze, complexion, expression and posture, identifying full spirit, deficient spirit, lost spirit and false spirit (based on the spirit observation content of TCM Inspection)",
        "Disease Nature Discriminator",
        "Discriminate the nature of the six external pathogenic factors (wind, cold, summer heat, dampness, dryness, fire), ticking symptoms to analyse the nature automatically (based on the six pathogenic factor content of TCM Aetiology)",
        "Locate the meridian of the lesion by tracing the pathway of the pain or discomfort location along the twelve meridians, assisting meridian differentiation and point selection reference for massage.",
        "TCM Constitution Self-Test",
        "Identify the nine basic constitution types according to the ZYYXH/T157-2009 standard Classification and Determination of TCM Body Constitution",
        "Select the corresponding treatment principle and method from the differentiation result, covering treatment on the opposite and same aspects, treating the branch versus the root, supporting upright qi and dispelling pathogens, adjusting yin and yang, and adapting to the three causes",
        "Select the observed tongue body and coating features to automatically match the TCM tongue diagnosis pathology correspondence (based on the tongue diagnosis content of TCM Diagnostics)",
        "Select the pattern features of the four pairs of principles to automatically derive the result of eight-principle differentiation (exterior/interior · cold/heat · deficiency/excess · yin/yang)",
        "Record dynamic changes in tongue appearance, pulse and symptoms, with automatic analysis of the condition trend (data stored in the local browser)",
        "Look up the pulse features and disease correspondence of the twenty-eight TCM pulses (based on the pulse diagnosis content of Binhu Maixue and TCM Diagnostics)",
        "Auscultation and olfaction cover both listening to sound and smelling odours, identifying patterns from abnormal sounds and smells (based on the content of TCM Auscultation and Olfaction)",
        "About \"TCM Diagnosis Tools\"",
        "The TCM Diagnosis Tools collection contains 21 free online tools covering the common calculation, conversion and lookup needs of TCM diagnosis scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find practical tools here that are ready to use the moment you open them. All tools run entirely in the front end and upload no data to the server, protecting privacy and security.",
        "The TCM diagnosis tools collected on this page include (representative tools):",
        "These tools help you complete common TCM diagnosis tasks quickly without memorising complex formulas or manual conversions - just enter the values and get the result.",
        "Do the TCM diagnosis tools need downloading or registration?",
        "No. All TCM diagnosis tools on this page are pure front-end online tools. Open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the TCM diagnosis tool results accurate, and is the data secure?",
        "The tools are based on public mathematical formulas and general industry standards, computing locally in your browser for instant results. All computation happens on your own device and data is never uploaded to the server, so privacy and security are assured.",
    ]))


if __name__ == '__main__':
    main()