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
    write('pulse-diagnosis', build('pulse-diagnosis', [
        "⚖️ Pulse-to-Disease Reference Tool",
        "Look up the pulse features and disease correspondence of the twenty-eight TCM pulses (based on the pulse diagnosis content of Binhu Maixue and TCM Diagnostics)",
        "The twenty-eight pulses are identified by four elements - position, rate, form and force: floating indicates exterior, deep indicates interior, slow indicates cold (fewer than four beats per breath), rapid indicates heat (five or more beats per breath), deficient indicates deficiency, forceful indicates excess, slippery indicates phlegm, food stagnation, floating and rapid indicates heat, and choppy indicates qi stagnation and blood stasis. Disease is read from the four dimensions of pulse depth, rate, size and force.",
        "Search pulses",
        "Depth (position)",
        "Rate",
        "Force",
        "Form",
        "Click a pulse card above to view detail",
        "Copy details",
        "⚠️ Pulse diagnosis requires a quiet environment, lying flat or sitting upright, with the arm level with the heart. The \"cun-kou\" method is commonly used, dividing into cun, guan and chi positions, each taken at floating, middle and deep, giving nine subdivisions. This tool is for TCM study reference.",
        "📋 Key points for differentiating common pulses",
        "Pulse A",
        "Pulse B",
        "Floating and deep",
        "Floating pulse (felt with light pressure)",
        "Deep pulse (only felt with heavy pressure)",
        "Floating indicates exterior, deep indicates interior",
        "Slow and rapid",
        "Slow pulse (fewer than four beats per breath)",
        "Rapid pulse (five or more beats per breath)",
        "Slow indicates cold, rapid indicates heat",
        "Deficient pulse (weak)",
        "Forceful pulse (strong)",
        "Deficient indicates insufficiency, forceful indicates excess",
        "Slippery and choppy",
        "Slippery pulse (smooth and flowing)",
        "Choppy pulse (rough and hesitant)",
        "Slippery indicates phlegm, food, excess heat; choppy indicates blood deficiency and qi stagnation",
        "Flooding and thin",
        "Flooding pulse (large and forceful)",
        "Thin pulse (fine as a thread)",
        "Flooding indicates flourishing heat, thin indicates deficiency of both qi and blood",
        "📚 Deep dive: pulse-to-disease reference",
        "Floating, deep, slow and rapid",
        "Wiry, slippery, choppy, flooding",
        "Combining pulse and symptoms",
        "Floating rapid pulse",
        "Selecting \"floating\" (exterior) + \"rapid\" (heat) → floating rapid indicates a wind-heat exterior pattern with thin yellow coating and fever; acrid-cool exterior release is indicated.",
        "Selecting \"wiry\" → indicates liver and gallbladder disease, pain or phlegm-fluid; combined with slippery it becomes liver-gallbladder damp-heat, treated by soothing the liver and promoting bile flow.",
        "What are the basic pulses?",
        "Floating, deep, slow, rapid, slippery, choppy, wiry, flooding, thin, deficient and the like, distinguished across the four dimensions of position, rate, form and force.",
        "Can a single pulse confirm a diagnosis?",
        "No. It must be combined with tongue and symptoms; the tool only offers primary disease hints.",
        "About \"Pulse-to-Disease Reference Tool\"",
        "Pulse-to-Disease Reference Tool - TCM palpation tool for looking up the disease correspondence of the 28 pulses such as floating, deep, slow and rapid. Professional medical tool based on authoritative medical standards, for reference only.",
        "How to use Pulse-to-Disease Reference Tool",
        "Enter a pulse name, such as floating, deep, slow or rapid...",
        "What does Pulse-to-Disease Reference Tool do?",
        "How do I use Pulse-to-Disease Reference Tool?",
        "Which scenarios suit Pulse-to-Disease Reference Tool?",
        "Enter a pulse name, such as floating, deep, slow or rapid...",
    ]))

    write('meridian-differentiation', build('meridian-differentiation', [
        "🌿 Meridian Differentiation Pain Matcher",
        "Locate the meridian of a lesion by tracing the pathway of the pain or discomfort location (based on the pathways of the twelve meridians)",
        "Localise by the twelve meridian pathways: the pain location corresponds to the area traversed, frontal pain belongs to Yangming, lateral pain to Shaoyang, occipital pain to Taiyang and vertex pain to Jueyin. Each meridian has its own main symptoms and indicated points, so the affected meridian is located by crossing location with accompanying symptoms (bitter taste indicates gallbladder, dry throat indicates kidney), assisting point selection for massage and meridian differentiation.",
        "Search location",
        "Select the meridian corresponding to the discomfort",
        "Click a meridian above to view its pathway and indications",
        "💡 Meridian differentiation follows the principle \"where the meridian passes, what it treats\". Pain distributed along a meridian's pathway usually belongs to that meridian's lesion. Clinically the zang-fu connection can be combined and points selected along the meridian for treatment.",
        "📋 Flow order of the twelve meridians",
        "Lung meridian → Large intestine meridian → Stomach meridian → Spleen meridian → Heart meridian → Small intestine meridian → Bladder meridian → Kidney meridian → Pericardium meridian → Triple energiser meridian → Gallbladder meridian → Liver meridian → (back to Lung)",
        "Meridian",
        "Associated zang-fu",
        "Key points of surface distribution",
        "Hand Taiyin Lung Meridian",
        "Belongs to lung, connects to large intestine",
        "Chest → anterior border of medial upper limb → thumb",
        "Hand Yangming Large Intestine Meridian",
        "Belongs to large intestine, connects to lung",
        "Index finger → anterior border of lateral upper limb → shoulder → neck → face",
        "Foot Yangming Stomach Meridian",
        "Belongs to stomach, connects to spleen",
        "Face → neck → chest and abdomen → anterior border of lateral lower limb → second toe",
        "Foot Taiyin Spleen Meridian",
        "Belongs to spleen, connects to stomach",
        "Great toe → anterior border of medial lower limb → abdomen → chest",
        "Hand Shaoyin Heart Meridian",
        "Belongs to heart, connects to small intestine",
        "Axilla → posterior border of medial upper limb → little finger",
        "Hand Taiyang Small Intestine Meridian",
        "Belongs to small intestine, connects to heart",
        "Little finger → posterior border of lateral upper limb → shoulder blade → neck → face",
        "Foot Taiyang Bladder Meridian",
        "Belongs to bladder, connects to kidney",
        "Inner canthus → vertex → back of neck → back and waist → posterior lower limb → little toe",
        "Foot Shaoyin Kidney Meridian",
        "Belongs to kidney, connects to bladder",
        "Sole → posterior border of medial lower limb → abdomen → chest",
        "Hand Jueyin Pericardium Meridian",
        "Belongs to pericardium, connects to triple energiser",
        "Chest → middle line of medial upper limb → middle finger",
        "Hand Shaoyang Triple Energiser Meridian",
        "Belongs to triple energiser, connects to pericardium",
        "Ring finger → middle line of lateral upper limb → shoulder → neck → ear",
        "Foot Shaoyang Gallbladder Meridian",
        "Belongs to gallbladder, connects to liver",
        "Outer canthus → side of head → flank and waist → middle line of lateral lower limb → fourth toe",
        "Foot Jueyin Liver Meridian",
        "Belongs to liver, connects to gallbladder",
        "Great toe → middle line of medial lower limb → genital area → abdomen → flank",
        "📚 Deep dive: meridian differentiation pain",
        "Meridian pathways",
        "Pain localisation",
        "Treating by selecting the meridian",
        "Taiyang meridian with cold invasion",
        "Keywords \"headache extending to the nape and back with aversion to cold\" → matches the Taiyang meridian, indicating wind-cold invading Taiyang, treated with Gui Zhi Tang type formulas to release the exterior and harmonise the ying.",
        "Shaoyang meridian",
        "\"Lateral headache with bitter taste\" → Shaoyang meridian (side of head), treated by harmonising Shaoyang (Xiao Chai Hu Tang).",
        "What is meridian differentiation?",
        "Attribute pain and numbness to a meridian by its pathway, then select points or formulas accordingly.",
        "How does it relate to zang-fu differentiation?",
        "They are often combined: meridian disease is usually superficial pain along the pathway, while zang-fu disease usually involves internal functional disturbance.",
        "About \"Meridian Differentiation Pain Matcher\"",
        "Meridian Differentiation Pain Matcher - TCM meridian differentiation tool locating the affected meridian from the pain location along the pathway. Professional medical tool based on authoritative medical standards, for reference only.",
        "How to use Meridian Differentiation Pain Matcher",
        "What does Meridian Differentiation Pain Matcher do?",
        "Locate the meridian of the lesion by tracing the pain or discomfort location along the twelve meridians, based on their pathways, assisting meridian differentiation and massage point selection.",
        "How do I use Meridian Differentiation Pain Matcher?",
        "Which scenarios suit Meridian Differentiation Pain Matcher?",
        "e.g. headache, shoulder, lower back, knee, flank...",
    ]))


if __name__ == '__main__':
    main()