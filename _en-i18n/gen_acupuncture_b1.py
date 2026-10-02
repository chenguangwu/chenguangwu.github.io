#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'acupuncture')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'acupuncture')
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
    out = {'slug': slug, 'industry': 'acupuncture', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('acupoint-combination', build('acupoint-combination', [
        "💊 Acupoint Combination (Four Gates) Recommender",
        "Recommends classic acupoint combinations by disorder or combination method, such as the Four Gates and Back-Shu/Front-Mu pairing",
        "/ Acupoint Combination Recommender",
        "📖 View the usage guide for the Acupoint Combination (Four Gates) Recommender",
        "By disorder",
        "By combination method",
        "Disorder category",
        "📋 Copy the current plan",
        "⚠️ Acupoint combinations are reference ideas only; clinically the treatment must follow pattern differentiation and be modified to the presentation. Observe contraindicated points for pregnant women and those with special constitutions.",
        "📚 Deep dive: Acupoint Combination (Four Gates) Recommender",
        "For regulating qi stagnation and low spirits, use the 'opening the Four Gates' approach with Hegu and Taichong.",
        "For zang-fu disorders use the Back-Shu and Front-Mu pairing method, combining the back Shu points with the chest and abdominal Mu points.",
        "When the exterior and interior meridians are both affected, use the Yuan-Source and Luo-Connecting pairing (for example Hegu with Lieque) to link the two meridians.",
        "Four Gates combination",
        "For regulating liver qi stagnation, take bilateral Hegu (Yuan-Source point of the hand Yangming) and bilateral Taichong (Yuan-Source point of the foot Jueyin), four points in total on both sides, called 'opening the Four Gates', to soothe the liver, regulate qi and harmonize qi and blood; add Xingjian on the same meridian as Taichong to clear liver heat.",
        "Which four points are the Four Gates?",
        "Hegu and Taichong taken bilaterally, four points in all. Hegu governs qi and Taichong governs blood; used together they regulate qi and blood and relieve liver depression, and they are a commonly used point pair in practice.",
        "Can pregnant women use the Four Gates?",
        "Points such as Hegu and Sanyinjiao carry a risk of inducing uterine contractions and must not be needled during pregnancy. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Acupoint Combination (Four Gates) Recommender",
        "Acupoint Combination (Four Gates) Recommender - recommends classic acupuncture point combinations by disorder or function, such as the Four Gates, the Eight Confluent Points, Back-Shu/Front-Mu pairing and Yuan-Luo pairing. A medical professional tool based on authoritative medical standards, for reference only.",
        "e.g. headache, insomnia",
    ]))

    write('acupoint-injection', build('acupoint-injection', [
        "📏 Acupoint Injection (Solution Depth) Calculator",
        "Calculates the injection depth and dose according to the acupoint region, body build and solution properties, to standardize aqua-acupuncture practice",
        "📖 View the usage guide for the Acupoint Injection (Solution Depth) Calculator",
        "Back and lumbar region (Back-Shu points)",
        "Limbs (Zusanli and others)",
        "Solution type",
        "Vitamin B12 (0.5 mg/ml)",
        "Vitamin B1 (100 mg/2 ml)",
        "Angelica injection",
        "Compound angelica",
        "Procaine (0.5%-1%)",
        "Number of points injected per session",
        "📏 Calculate depth and dose",
        "📋 Acupoint injection reference standards",
        "⚠️ Acupoint injection is an invasive procedure that requires strict asepsis and proper qualification; it is contraindicated in those allergic to the solution, and depth must be controlled on the chest and back to avoid organ injury. This tool is for reference only.",
        "📚 Deep dive: Acupoint Injection (Solution Depth) Calculator",
        "Aqua-acupuncture for lumbar disc herniation, injecting the solution according to the depth of the Jiaji points.",
        "Acupoint injection of vitamin B12 to nourish the nerves, with the depth controlled by region to prevent injury.",
        "For facial points, inject a small dose into the superficial layer to avoid unevenness.",
        "Calculate the injection depth and dose",
        "For a patient of medium build, Zusanli is chosen (the muscle layer is thicker); standard insertion is about 30-40 mm with 2-4 mL of solution. For children or thin patients, reduce to 15-25 mm and 1-2 mL to avoid injuring the deep peroneal nerve by inserting too deeply.",
        "Which solutions are commonly used for acupoint injection?",
        "Angelica injection, B vitamins, Salvia and other Chinese patent medicine injections are commonly used; a negative skin test is required and the procedure must be performed by a physician at a medical institution.",
        "Why calculate the depth?",
        "The safe depth varies greatly by region (shallow on the chest and back, thick in the gluteal muscle), and inserting too deeply can injure organs or nerves. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Acupoint Injection (Solution Depth) Calculator",
        "Acupoint Injection (Solution Depth) Calculator - calculates the needling depth and solution dose for acupoint injection from the point region, body build and solution properties, to standardize aqua-acupuncture. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('acupoint-location', build('acupoint-location', [
        "📍 Acupoint Location (Bone-Length Measurement) Calculator",
        "Based on the proportional bone-length standards in the Lingshu and the national unified textbook, converts the patient's measured body-surface length for point location",
        "\"Based on the proportional bone-length standards in the Lingshu and the national unified textbook, converts the patient's measured body-surface length for point location\" performs a professional calculation on the input parameters and outputs the result.",
        "📖 View the usage guide for the Acupoint Location (Bone-Length Measurement) Calculator",
        "Standard proportional length",
        "(cun)",
        "Measured body-surface length of this segment (cm)",
        "Distance from the starting point to the target point (cun)",
        "Landmarks of the starting and ending points",
        "📐 Convert and locate",
        "Please select a region and enter the measured length",
        "Key points of the proportional bone-length method:",
        "Using the patient's own body-surface bony landmarks as the basis, a given region is divided into equal parts and each part is one cun. Regardless of height or build, measurement follows the individual's own proportions, ensuring individualized point location.",
        "📋 Table of commonly used proportional bone lengths",
        "⚠️ This tool converts according to textbook standards and is for acupuncture study and clinical point location reference only; it cannot replace point location by a professional physician based on pattern differentiation.",
        "📚 Deep dive: Acupoint Location (Bone-Length Measurement) Calculator",
        "Locate points by proportional measurement of the patient's own bone length, resolving differences in height and build.",
        "To locate Zusanli: 3 cun below Dubi, one finger-breadth lateral to the anterior crest of the tibia.",
        "To locate Neiguan: 2 cun above the wrist crease, between the two tendons.",
        "Bone-length proportional point location",
        "The patient's elbow crease to wrist crease measures 12 cun and the actual measurement is 24 cm, so 1 cun = 2 cm; Neiguan (2 cun above the wrist) is therefore 4 cm above the wrist crease, avoiding the deviation caused by using the practitioner's finger as the cun.",
        "What is the difference between the bone-length cun and the finger-length cun?",
        "The bone-length method uses equal divisions between bony landmarks and is more objective; the finger-length cun (such as the middle-finger cun) is affected by finger size and is best used as a supplement.",
        "Can bone-length location completely replace anatomical landmarks?",
        "No. It must be combined with body-surface landmarks and anatomical layers to locate points. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Acupoint Location (Bone-Length Measurement) Calculator",
        "Acupoint Location (Bone-Length Measurement) Calculator - based on the TCM proportional bone-length standard, converts the centimeters per cun from the patient's measured body-surface length to quickly complete point-location conversion. A medical professional tool based on authoritative medical standards, for reference only.",
        "e.g. 24",
        "e.g. 1.5",
    ]))

    write('bloodletting-therapy', build('bloodletting-therapy', [
        "🪡 Bloodletting Therapy (Blood Volume) Controller",
        "Controls the blood volume in collateral-pricking bloodletting according to the site, constitution and disease pattern, to guard against excessive loss",
        "/ Bloodletting Blood Volume Controller",
        "📖 View the usage guide for the Bloodletting Therapy (Blood Volume) Controller",
        "Bloodletting site",
        "Fingertip (Shixuan)",
        "Ear apex",
        "Neck and nape (Weizhong/Dazhui)",
        "Cubital fossa (Quze/Chize)",
        "Popliteal fossa (Weizhong)",
        "Back (Weiyang/Geshu)",
        "Superficial vein (distinct vein)",
        "Pricking method",
        "Spot pricking (quick prick)",
        "Scattered pricking (leopard-spot pricking)",
        "Pricking plus cupping",
        "Vein pricking",
        "Patient constitution",
        "Nature of the disease pattern",
        "Acute condition (high fever/coma)",
        "Blood stasis obstructing the collaterals",
        "Number of bloodletting points planned for this session",
        "🪡 Calculate blood volume",
        "📋 Bloodletting blood volume reference",
        "⚠️ Contraindicated in coagulation disorders, anemia, hypotension, pregnancy, severe heart disease and debilitated patients; the total volume for an adult in a single session should not exceed 20 mL. This tool is for reference and the procedure must be performed by a licensed physician.",
        "📚 Deep dive: Bloodletting Therapy (Blood Volume) Controller",
        "For acute sore swollen throat, spot-prick Shaoshang and Shangyang to release a few drops of blood.",
        "For heatstroke with high fever, spot-prick Shixuan to discharge heat.",
        "For blood-stasis headache, cluster-prick Taiyang to release blood.",
        "Calculate the safe blood volume",
        "For adults the total volume in a single spot-pricking session should be kept within 5-10 mL (about a few drops to 1-2 mL per point); for the debilitated, the elderly and those with anemia, reduce to 1-3 mL with fewer points, to prevent qi deficiency and dizziness.",
        "Which needles are commonly used?",
        "A three-edged needle or a disposable lancet for spot pricking; strict disinfection and one needle per person are required, and the procedure must be performed by a professional.",
        "Who is not suitable for bloodletting?",
        "Use with caution or avoid it in anemia, coagulation disorders, pregnancy and physical debility. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Bloodletting Therapy (Blood Volume) Controller",
        "Bloodletting Therapy (Blood Volume) Controller - controls the blood volume in collateral-pricking bloodletting according to site, constitution and disease pattern, prevents excessive bloodletting and provides safe threshold reference. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('cupping-mark-analysis', build('cupping-mark-analysis', [
        "📍 Cupping Mark (Pathology) Analyzer",
        "Analyzes constitution and pathological state from the color and shape of the cupping mark, providing pattern-differentiation reference",
        "📖 View the usage guide for the Cupping Mark (Pathology) Analyzer",
        "Cupping marks are differentiated by color and shape: pale red or no obvious mark means normal or a tendency to qi and blood deficiency; bright red mostly indicates a heat pattern or excess heat; purple-red mostly indicates blood stasis or qi stagnation with blood stasis; purple-black mostly indicates cold congealing with blood stasis or a long course; blisters and edema mostly indicate predominant dampness or too long a cupping time. Marks generally fade within 3 to 7 days, and not fading after 10 days suggests poor qi and blood circulation; a single cupping session should last 5 to 15 minutes.",
        "(1) Select the cupping mark appearance",
        "(2) Accompanying conditions (multiple choice)",
        "🔍 Analyze and differentiate",
        "📋 Cupping mark color differentiation table",
        "⚠️ The cupping mark is only a reference for constitution and local reaction, not a basis for diagnosis; marks generally fade in 3-7 days, and dark marks taking longer to fade is normal.",
        "📚 Deep dive: Cupping Mark (Pathology) Analyzer",
        "Blisters in the cupping mark suggest predominant damp-turbidity or too long a cupping time.",
        "Scattered bright red spots in the mark suggest wind-heat or blood heat.",
        "A pale center with a purple-red edge suggests a mixture of deficiency and excess.",
        "Interpreting the shape of the cupping mark",
        "After cupping the mark has a purple-red edge with a paler center and small blisters; combined with the patient's heavy body, fatigue and greasy coating, the tendency is 'spleen deficiency with damp predominance'. It is advised to shorten the cupping time to 5-8 minutes, reduce the negative pressure and lower the frequency.",
        "How are cupping blisters handled?",
        "Keep small blisters dry and prevent rupture; large blisters should be disinfected and aspirated by a physician; the cupping time should not be too long and the negative pressure not too great.",
        "Can cupping marks diagnose disease?",
        "They cannot replace diagnosis and serve only as a reference for constitution and treatment efficacy. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Cupping Mark (Pathology) Analyzer",
        "Cupping Mark (Pathology) Analyzer - analyzes constitution and pathological state from the color and shape of the cupping mark (bright red, purple-dark, blisters, itching), providing TCM pattern-differentiation reference. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()
