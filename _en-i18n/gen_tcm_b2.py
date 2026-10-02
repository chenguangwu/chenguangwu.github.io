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
    write('disease-tracking', build('disease-tracking', [
        "🩺 Condition Tracking Tool",
        "Record dynamic changes in tongue appearance, pulse and symptoms, with automatic analysis of the condition trend (data stored in the local browser)",
        "📝 Add follow-up record",
        "No symptoms (0)",
        "Mild (1)",
        "Moderate (2)",
        "Severe (3)",
        "+ Add symptom",
        "📅 Follow-up record timeline",
        "No records yet; add a follow-up record first",
        "This tool helps record condition trends and cannot replace medical diagnosis. Data is stored in the local browser and will be lost if you clear browser data.",
        "📚 Deep dive: dynamic condition tracking",
        "Symptom scoring",
        "Trend comparison",
        "Tongue and pulse changes",
        "Total score trend",
        "Record symptom scores 0-3; the first visit totals 8 and the follow-up 3, so scoreDiff=−5 indicates improvement. maxScore normalises the trend bar (green to red).",
        "Tongue and pulse comparison",
        "The tongue was pale and swollen at first visit and turns red at follow-up, so the tool flags \"tongue body change\"; a pulse shifting from weak to moderate and even is also recorded, supporting efficacy judgement.",
        "What is the scoring standard?",
        "Each symptom is 0 for none, 1 mild, 2 moderate, 3 severe; compare totals across records to see the trend.",
        "Where is it stored?",
        "In the browser locally (localStorage); records can be deleted and nothing goes online.",
        "About \"Condition Tracking Tool\"",
        "Condition Tracking Tool - TCM tongue, pulse and symptom change recording with trend analysis. Professional medical tool based on authoritative medical standards, for reference only.",
        "How to use Condition Tracking Tool",
        "What does Condition Tracking Tool do?",
        "How do I use Condition Tracking Tool?",
        "Which scenarios suit Condition Tracking Tool?",
        "Symptom name (e.g. headache)",
    ]))

    write('etiology-tree', build('etiology-tree', [
        "✨ Etiology Logic Tree Generator",
        "A logic tree of TCM aetiology categories, expanding to view external pathogenic factors, internal injuries and other causative factors with their pathogenic characteristics (based on TCM Aetiology)",
        "Aetiology falls into three categories: the six external pathogenic factors (wind, cold, summer heat, dampness, dryness, fire) plus epidemic qi; the seven internal emotions (joy, anger, worry, pensiveness, grief, fear, fright) with diet and overwork; and others (trauma, insect and animal bites, phlegm-fluid, blood stasis, stones). It expands in three layers of external, internal and other, with pathogenic characteristics hanging under each category, forming a logic tree from aetiology to syndrome that makes tracing straightforward.",
        "💡 TCM aetiology falls into three categories: external (six pathogenic factors and epidemic qi), internal (seven emotions, diet, overwork), and other causative factors (phlegm-fluid, blood stasis, stones, trauma and the like). Identifying the aetiology is the foundation of \"treating on the basis of the cause\".",
        "✨ Overview of the Three Causes Theory",
        "Chen Wuze's \"Three Causes\"",
        "External cause",
        "Six external pathogenic factors",
        "Wind, cold, summer heat, dampness, dryness, fire, epidemic qi",
        "They attack from outside onto the surface, mostly producing exterior syndromes",
        "Internal cause",
        "Seven emotions injuring the interior",
        "Joy, anger, worry, pensiveness, grief, fear, fright",
        "They strike the zang-fu directly and affect the qi mechanism",
        "Neither external nor internal",
        "Diet, overwork and trauma",
        "Improper diet, excessive work, trauma, insect and animal bites",
        "They damage the body form and affect the zang-fu",
        "📚 Deep dive: aetiology logic tree generation",
        "Three causes classification",
        "External pathogen / internal injury",
        "The six pathogenic factors are external causes",
        "Root node \"Aetiology\" → external cause \"Six pathogenic factors (wind, cold, summer heat, dampness, dryness, fire)\" → wind → aversion to wind with sweating; the whole tree exports for lesson preparation or science popularisation.",
        "Seven emotions injuring the interior",
        "The internal branch lists \"seven emotions (joy, anger, worry, pensiveness, grief, fear, fright)\" and \"diet and overwork\"; expanding shows the chain from emotional frustration to liver qi stagnation.",
        "What do the three causes refer to?",
        "External causes (the six pathogenic factors), internal causes (seven emotions, diet and overwork), and causes that are neither (falls, insect and animal bites); the tool layers them this way.",
        "Can it be exported?",
        "The logic tree renders as a text hierarchy that can be copied and saved.",
        "About \"Aetiology Logic Tree Generator\"",
        "Aetiology Logic Tree Generator - TCM aetiology analysis tool generating a classification logic tree of internal and external aetiology. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('syndrome-element', build('syndrome-element', [
        "🔢 Syndrome Element Combination Deriver",
        "Zhu Wenfeng's \"syndrome element differentiation\" system: select disease-location elements and disease-nature elements to automatically derive the complete syndrome name (location plus nature)",
        "📍 I. Select disease-location elements",
        "🏷️ II. Select disease-nature elements",
        "Derive syndrome name",
        "After selecting location and nature elements, click \"Derive syndrome name\"",
        "💡 A syndrome element is an element of a syndrome, split into disease-location elements (heart, liver, spleen, lung, kidney, stomach, gallbladder and the like) and disease-nature elements (qi deficiency, blood deficiency, yin deficiency, yang deficiency, cold, heat, phlegm, dampness, blood stasis and the like). Once combined they form the syndrome name, for example \"heart\" + \"qi deficiency\" = \"heart qi deficiency syndrome\".",
        "🔢 Common syndrome element combinations",
        "Disease-location elements",
        "Disease-nature elements",
        "Combined syndrome name",
        "Qi deficiency",
        "Heart qi deficiency syndrome",
        "Tonify heart qi",
        "Hyperactive yang",
        "Liver yang rising syndrome",
        "Soothe the liver and subdue yang",
        "Yang deficiency + dampness",
        "Spleen deficiency with dampness syndrome",
        "Strengthen the spleen and resolve dampness",
        "Yin deficiency",
        "Lung yin deficiency syndrome",
        "Nourish yin and moisten the lung",
        "Yang deficiency + water retention",
        "Kidney deficiency with water overflow syndrome",
        "Warm yang and promote urination",
        "Stomach",
        "Heat + food stagnation",
        "Stomach heat with food stagnation syndrome",
        "Clear stomach heat and purge fu organs",
        "📚 Deep dive: syndrome element combination and derivation",
        "Location + nature",
        "Syndrome name synthesis",
        "Treatment principle hints",
        "Heart + qi deficiency",
        "Checking location \"heart\" and nature \"qi deficiency\" → syndrome name \"heart qi deficiency syndrome\"; the treatment principle map gives \"nourish the heart\", suggesting nourishing heart qi; the same pattern applies to \"liver + hyperactive yang\" → liver yang rising syndrome.",
        "Multiple elements",
        "Selecting \"spleen + dampness + qi deficiency\" → \"spleen deficiency with dampness and qi deficiency syndrome\", with treatment principle of strengthening the spleen, resolving dampness and boosting qi, prompting attention to primary versus secondary.",
        "What are syndrome elements?",
        "The smallest differentiation units of location (zang-fu and channels) and nature (qi, blood, yin, yang, deficiency, excess, cold, heat, dampness, stasis); combined they form the syndrome name.",
        "How are the treatment principles derived?",
        "By mapping location (heart → nourish the heart, spleen → strengthen the spleen, kidney → tonify the kidney) and joining it with nature (qi deficiency → boost qi).",
        "About \"Syndrome Element Combination Deriver\"",
        "Syndrome Element Combination Deriver - TCM syndrome element differentiation tool deriving the complete syndrome name by combining disease-location and disease-nature elements. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('constitution-test', build('constitution-test', [
        "🌿 TCM Constitution Self-Test",
        "Identify the nine basic constitution types according to the ZYYXH/T157-2009 standard Classification and Determination of TCM Body Constitution",
        "Per the Classification and Determination of TCM Body Constitution standard: each constitution is scored across its items on a 5-level scale (1 to 5 points), with conversion score = (raw score − number of items) ÷ (number of items × 4) × 100. A conversion score of 60 or above with all other constitutions below 30 is judged as that constitution (the balanced constitution uses the same rule of 60 or above with all others below 30); 40 or above but below 60 is a tendency toward that constitution.",
        "📋 Scoring notes: each question has 5 options (1-5 points), 1 = never (not at all), 2 = rarely (a little), 3 = sometimes (sometimes), 4 = often (fairly), 5 = always (very much). Please answer based on your actual situation over the past year.",
        "Calculate constitution",
        "After completing all questions, click \"Calculate constitution\"",
        "⚠️ Constitution determination standard: a conversion score of 60 or above means \"yes\", 40-59 means \"tendency yes\", and below 40 means \"no\". Multiple constitution tendencies may coexist (mixed constitution). This tool is for health reference only and cannot replace physician diagnosis.",
        "📋 The nine constitutions at a glance",
        "Prone diseases",
        "Well-proportioned build, rosy complexion and abundant energy",
        "Rarely falls ill",
        "Shortness of breath, reluctance to speak, fatigue and spontaneous sweating",
        "Colds and visceral prolapse",
        "Aversion to cold, cold hands and feet",
        "Diarrhoea and oedema",
        "Hot palms and soles, dry mouth and throat",
        "Insomnia and constipation",
        "Obese build, soft abdomen",
        "Diabetes and hypertension",
        "Greasy face and yellow tongue coating",
        "Jaundice and acne",
        "Dull complexion and tendency to bruise",
        "Coronary disease and tumours",
        "Qi stagnation constitution",
        "Low mood and sensitivity",
        "Depression and insomnia",
        "Inherent constitution",
        "Allergic constitution, often asthma",
        "Allergic conditions",
        "📚 Deep dive: TCM constitution self-test",
        "Nine constitutions",
        "Conversion score determination",
        "Tendency hints",
        "A balanced constitution conversion score of 75",
        "All 5 questions answered 4 → rawAvg=4, transScore=(4−1)/4×100=75, which is 60 or above so judged \"yes\"; if all answered 3 → (3−1)/4×100=50, judged \"tendency yes\".",
        "Handling reverse items",
        "Reverse items (such as \"prone to fatigue\" scored in reverse as 6−raw) record raw=2 as 4 points, avoiding a mistaken judgement of qi deficiency.",
        "What is the conversion score formula?",
        "transScore=(average of items−1)/4×100; 60 or above means yes, 40-59 means tendency yes, below 40 means no.",
        "What are the nine constitutions?",
        "Balanced, qi deficiency, yang deficiency, yin deficiency, phlegm-dampness, damp-heat, blood stasis, qi stagnation and inherent; the report lists the primary and secondary types with any deviations.",
        "About \"TCM Constitution Self-Test\"",
        "TCM Constitution Self-Test - nine constitution identification tool with self-test scoring for balanced, qi deficiency, yang deficiency and other constitutions. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()