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
    write('formula-matching', build('formula-matching', [
        "🏋️ Syndrome-to-Formula Finder",
        "Look up the classical formula matching a syndrome type or symptom, including composition, actions and indications",
        "No matching formula found",
        "This tool collects common classical formulas for study reference; clinical formula selection and prescribing must be done by a licensed TCM practitioner after syndrome differentiation.",
        "📚 Deep dive: syndrome-to-formula assistance",
        "Search by formula name",
        "Syndrome matching",
        "Composition and actions",
        "Ma Huang Tang for exterior cold",
        "Searching \"chills without sweating\" → matches Ma Huang Tang (acrid-warm exterior-releasing with Ma Huang, Gui Zhi, Xing Ren and Gan Cao); filter by category for exterior-releasing formulas.",
        "Liu Wei for yin deficiency",
        "Searching \"lower back and knee soreness with night sweats\" → Liu Wei Di Huang Wan (nourishes kidney yin), with composition and indications in the detail view.",
        "Is the formula library large?",
        "It covers classical formulas and common contemporary formulas, filterable by syndrome type, action or composition keyword.",
        "Alternative formulas?",
        "Several formulas often share one syndrome; the tool offers candidates but does not choose for you - a physician must weigh the options.",
        "About \"Syndrome-to-Formula Finder\"",
        "Syndrome-to-Formula Finder - lookup tool mapping TCM formulas to syndrome types, helping select classical formulas. Professional medical tool based on authoritative medical standards, for reference only.",
        "Search formula names, syndrome types or symptoms (e.g. wind-cold, qi deficiency, Xiaoyao San)",
    ]))

    write('misdiagnosis-training', build('misdiagnosis-training', [
        "🩺 Misdiagnosis Case Clinical Reasoning Trainer",
        "Train TCM syndrome differentiation reasoning with real misdiagnosis cases to sharpen differential diagnosis skills",
        "Training complete! Accuracy",
        "💡 Training summary",
        "Retrain",
        "This tool is intended for TCM teaching and clinical reasoning training. All cases are for study reference only and cannot replace clinical diagnosis and treatment.",
        "📚 Deep dive: misdiagnosis reasoning training",
        "Case selection",
        "Analysis and review",
        "Accuracy 80%",
        "With 10 cases and 8 correct → percent=round(8/10×100)=80%, and finalScore shows \"8/10\"; review the analysisBox explanation for the wrong ones.",
        "Progress bar",
        "Draws progress as currentIdx/CASES.length×100, advancing question by question until the last question produces the final score.",
        "Where do the cases come from?",
        "Built-in commonly misdiagnosed scenarios (such as true heat with false cold), with immediate explanation of the differentiation point for right or wrong answers.",
        "Can I redo them?",
        "Refresh or reset returns to the first question, so you can drill the reasoning repeatedly.",
        "About \"Misdiagnosis Case Clinical Reasoning Trainer\"",
        "Misdiagnosis Case Clinical Reasoning Trainer - TCM clinical misdiagnosis case analysis and syndrome differentiation reasoning training tool. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('ten-questions', build('ten-questions', [
        "✨ Ten Questions in TCM Inquiry Questionnaire Generator",
        "\"One asks about chills and fever, two about sweating, three about head and body, four about the bowels, five about diet, six about chest and abdomen, seven about hearing, eight about thirst - all must be differentiated, nine about past illness and ten about cause\" - structured TCM inquiry record",
        "Generate inquiry record",
        "Download record",
        "Fill in the inquiry content then click \"Generate inquiry record\"",
        "💡 The full Ten Questions verse: \"Also consider medication and the constitution; for women one must always ask about menstruation, and timing, scanty flow and flooding all appear; add a few more lines for paediatrics, where smallpox and measles are fully covered by the examination.\"",
        "📚 Deep dive: Ten Questions in TCM Inquiry questionnaire",
        "Collect all ten questions",
        "Structured medical record",
        "Generation with pulse case attached",
        "All ten questions listed",
        "Generated per the Ten Questions verse: chills and fever, sweating, head and body, bowels and urination, diet, chest and abdomen, ears and eyes, thirst, past illness and cause, each with single-choice options or text; once filled, export an inquiry record such as \"Mr. X, male, ? years old\".",
        "Custom count",
        "The count box accepts 1-50; entering 10 generates 10 blank questionnaires for batch collection in a TCM outpatient clinic.",
        "What are the ten questions?",
        "One asks about chills and fever, two about sweating, three about head and body, four about the bowels, five about diet, six about chest and abdomen, seven about hearing, eight about thirst - all must be differentiated, nine about past illness and ten about cause.",
        "Can I enter the patient's name?",
        "Name, gender and age can be filled in; records are generated locally as text only and never uploaded.",
        "About \"Ten Questions in TCM Inquiry Questionnaire Generator\"",
        "Ten Questions in TCM Inquiry Questionnaire Generator - TCM inquiry tool that auto-generates questionnaires from the Ten Questions verse into a structured inquiry record. Professional medical tool based on authoritative medical standards, for reference only.",
        "Name",
        "years old",
    ]))

    write('generator-29', build('generator-29', [
        "✨ TCM Inquiry (Ten Questions Verse) Auto-Generated Questionnaire",
        "Ten Questions Verse",
        "TCM inquiry is structured by the Ten Questions Verse: one chills and fever, two sweating, three head and body, four bowels, five diet, six chest and abdomen, seven hearing, eight thirst, nine past illness, ten cause, plus medication and women's menstruation, leukorrhea, pregnancy and childbirth. Each question generates corresponding items and options (for instance chills and fever splits into aversion to cold with fever, alternating chills and fever, and fever without chills); filling them in yields a complete history outline.",
        "📚 Deep dive: auto-generated Ten Questions questionnaire",
        "Random scenarios",
        "Teaching drills",
        "Batch questionnaires",
        "Generate 5 copies",
        "With a count of 5, five Ten Questions scenarios are randomly drawn from CASES (such as \"aversion to cold with fever and no sweating\" or \"thirst with preference for cold drinks\"), for peer assessment among interns.",
        "Count limit",
        "Supports 1-50; entering 30 produces 30 candidates, and values above the range are clamped to 50.",
        "How does it differ from the Ten Questions verse tool?",
        "This tool leans towards randomly generated drill scenarios, whereas the Ten Questions verse tool leans towards a fixed inquiry structure template.",
        "Is it repeatable?",
        "Each run samples randomly, so the same input may give different results - which suits deliberate practice.",
        "About \"TCM Inquiry (Ten Questions Verse) Auto-Generated Questionnaire\"",
        "TCM Inquiry (Ten Questions Verse) Auto-Generated Questionnaire. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "How to use TCM Inquiry (Ten Questions Verse) Auto-Generated Questionnaire",
        "Generation count",
        "What does TCM Inquiry (Ten Questions Verse) Auto-Generated Questionnaire do?",
        "The inquiry questionnaire generator (Ten Questions Verse) structures TCM inquiry questionnaires following the Ten Questions Verse, covering chills and fever, sweating, head and body, bowels and urination and more, assisting history collection in TCM.",
        "How do I use TCM Inquiry (Ten Questions Verse) Auto-Generated Questionnaire?",
        "Which scenarios suit TCM Inquiry (Ten Questions Verse) Auto-Generated Questionnaire?",
    ]))


if __name__ == '__main__':
    main()