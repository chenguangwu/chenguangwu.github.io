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
    write('guasha-direction', build('guasha-direction', [
        "🪡 Gua Sha Direction (Meridian Course) Indicator",
        "Look up the gua sha direction and meridian course for each body region, to standardize the technique and avoid scraping against the meridian",
        "📖 View the usage guide for the Gua Sha Direction (Meridian Course) Indicator",
        "The gua sha direction follows the course of the meridian: the three hand yin meridians run from chest to hand (scrape toward the hand), the three hand yang meridians from hand to head, the three foot yang meridians from head to foot, and the three foot yin meridians from foot to abdomen and chest. On the back it is mostly from top to bottom and on the limbs mostly from proximal to distal. Scrape each region 20 to 30 times or until sha appears (red-purple spots on the skin); leave an interval of 1 to 2 weeks between sessions. The pressure should redden the skin slightly without breaking it, and scraping against the meridian or back and forth must be avoided.",
        "(1) Select the region",
        "Purpose of gua sha",
        "Health maintenance and unblocking",
        "Relaxing the sinews and relieving pain",
        "Releasing the exterior and expelling toxins",
        "📋 Copy the direction guidance",
        "📋 General principles of gua sha direction",
        "⚠️ Gua sha should follow the meridian course in a single direction; scraping back and forth is prohibited. It is contraindicated over broken or infected skin, with a coagulation disorder, and on the abdomen and lumbosacral region of pregnant women. This tool is for reference.",
        "📚 Deep dive: Gua Sha Direction (Meridian Course) Indicator",
        "On the back the Bladder meridian is scraped from top to bottom following the meridian.",
        "On the upper limb the three yin meridians run from chest to hand, scraping from proximal to distal.",
        "On the neck scrape in one direction from Fengfu toward Dazhui.",
        "Look up the scraping direction",
        "To scrape the foot Taiyang Bladder meridian (back and waist), scrape along both sides of the spine from top to bottom and from inside to outside in a single direction; going with the meridian reinforces and going against it reduces. Scrape each area 20-30 times until sha appears, and avoid random back-and-forth scraping that damages the skin.",
        "Why emphasize going with the meridian?",
        "Scraping along the course of the meridian reinforces and against it reduces; the wrong direction may defeat the intent of the treatment. This tool provides direction reference.",
        "Is more sha always better?",
        "No. Flushing of the skin or light sha is the limit; in yang deficiency or with a bleeding tendency, scrape lightly or not at all. Seek medical care for serious conditions.",
        "About the Gua Sha Direction (Meridian Course) Indicator",
        "Gua Sha Direction (Meridian Course) Indicator - look up the correct gua sha direction and meridian course for each body region, to standardize the technique and avoid scraping against the meridian. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('index', build('index', [
        "🪡 Acupuncture and Tuina Tools",
        "Acupuncture and Tuina",
        "Acupuncture and Tuina Tools",
        "Intradermal needle (embedding needle) retention time calculator: estimates the embedding duration from the point region, season and patient condition, to standardize long-acting intradermal needle stimulation protocols.",
        "Acupoint injection (aqua-acupuncture) parameter calculator: calculates the injection depth and dose from the point region, patient build and solution properties, to standardize aqua-acupuncture and guard against overdose risk.",
        "Based on the proportional bone-length standards in the Lingshu and the national unified textbook, converts the patient's measured body-surface length for point location",
        "Pediatric tuina dose converter: converts the number of tuina strokes, time and pressure according to the child's age, provides dosage guidance for commonly used points, and standardizes pediatric tuina practice.",
        "Needle retention time recommendation (by disorder)",
        "Suggests a retention time range according to disorder type and constitution, with contraindications and precautions, for acupuncture reference (reference only, not a medical prescription; follow medical advice).",
        "Acupoint combination (Four Gates) recommendation",
        "Based on the classic 'Four Gates' pairing of Hegu and Taichong, recommends point combinations and locations according to the regulation goal, for reference by acupuncture enthusiasts and therapists (reference only, not medical advice).",
        "Flash cupping versus retained cupping comparator: compares the skin color reaction after flash and retained cupping to judge the intensity of the operation and the constitutional tolerance, assisting the choice of cupping method and intensity control.",
        "Needle retention time (by disorder) recommender",
        "⏱️ Needle Retention Time (by Disorder) Recommender",
        "Moxibustion cone count recommender: recommends the number of moxa cones individually according to the skin reaction and the deficiency or excess of the pattern, with a safety upper limit to prevent burns and standardize the stimulation dose of moxibustion.",
        "Warm needling temperature simulator: simulates the temperature change of the burning moxa segment and estimates the heat received at the point and the safety parameters, helping control the stimulation intensity of warm needling and prevent burns.",
        "Cupping mark analyzer: infers constitutional deviation and pathological state from the color and shape of the cupping mark, providing TCM pattern-differentiation reference and assisting efficacy judgment after cupping.",
        "Deqi degree assessor: grades the intensity of deqi from the patient's subjective needle sensation (soreness, numbness, distension, heaviness) and the practitioner's sense under the needle, and advises on needle manipulation to improve acupuncture efficacy.",
        "Cupping negative pressure safety lookup: looks up the safe negative pressure range (mmHg) by cupping method (retained or flash) and treatment site, to prevent skin injury from excessively heavy cupping.",
        "Tuina medium selector: recommends oils, ointments and other tuina media according to the technique, disorder, season and skin type, providing lubrication and a synergistic medicinal effect while reducing skin injury.",
        "Tuina technique frequency standardizer: looks up the standard frequency range of common techniques (times per minute) and converts the technique rhythm according to the treatment goal, to standardize tuina intensity.",
        "Collateral-pricking bloodletting controller: controls the blood volume according to site, constitution and disorder and gives a safety upper limit, to guard against excessive bloodletting and assist the external treatment of TCM blood stasis patterns.",
        "Acupoint combination recommender: recommends point combinations by disorder or classic pairing methods (such as the Four Gates or Back-Shu/Front-Mu pairing) and explains the pairing principle, assisting the drafting of acupuncture plans.",
        "Select commonly used points to look up their standard needling depth, and adjust the insertion depth and angle individually according to the user's build, age and needling site, as a reference for standard acupuncture practice.",
        "Gua sha direction indicator: looks up the gua sha direction and meridian course for each region, reminds the user to scrape with the meridian and avoid going against it, and standardizes gua sha to prevent injury.",
        "Meridian pathway display: presents the courses of the fourteen meridians, the laws of propagated sensation along the meridians and the main acupoints, assisting acupuncture point selection and the study of meridian theory.",
        "Auricular acupressure lookup: looks up the corresponding auricular point location and operating points by body region or chief symptom, providing guidance for acupressure treatment and daily health care.",
        "Electroacupuncture parameter selector: recommends the electroacupuncture waveform, frequency and current intensity according to the treatment goal, to standardize electroacupuncture stimulation parameters and ensure safe and effective electrotherapy.",
        "About the Acupuncture and Tuina Tools",
        "The Acupuncture and Tuina tool collection includes 22 free online tools covering the common calculation, conversion and lookup needs in acupuncture and tuina scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find practical, ready-to-use tools here. All tools run purely in the front end, and data is not uploaded to a server, protecting your privacy and security.",
        "The acupuncture and tuina tools collected on this page include (some representative tools):",
        "These tools help you complete common acupuncture and tuina tasks quickly, with no need to memorize complex formulas or convert manually - just enter the values and get the result.",
        "Do the acupuncture and tuina tools require download or registration?",
        "No. All the acupuncture and tuina tools on this page are pure front-end online tools; just open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the calculation results of the acupuncture and tuina tools accurate? Is the data secure?",
        "The tools calculate locally in your browser based on public mathematical formulas and general industry standards, and the results are available instantly. All computation is done locally on your device, and data is not uploaded to a server, so your privacy and security are protected.",
    ]))

    write('intradermal-needle', build('intradermal-needle', [
        "🏋️ Intradermal Needle (Embedding) Retention Time Calculator",
        "Calculates the retention time of an embedded intradermal needle according to the point region, season and patient condition",
        "📖 View the usage guide for the Intradermal Needle (Embedding) Retention Time Calculator",
        "(1) Type of intradermal needle",
        "Embedding site",
        "Auricular point",
        "Trunk (chest and back)",
        "Pain relief",
        "Chronic disease regulation",
        "Withdrawal (smoking/alcohol)",
        "⏱️ Calculate retention time",
        "📋 Intradermal needle embedding reference standards",
        "⚠️ Keep the area dry during embedding to avoid infection; remove the needle immediately if the skin becomes red, swollen or allergic, or if infection occurs; use caution when embedding at joints or at sites prone to friction.",
        "📚 Deep dive: Intradermal Needle (Embedding) Retention Time Calculator",
        "Auricular point embedding for 3-7 days of continuous stimulation.",
        "For knee joint pain, shorten the embedding time in summer to prevent sweat and infection.",
        "For children, halve the embedding time and reinforce the fixation.",
        "Estimate the retention time",
        "For adults using an intradermal needle at an auricular point or on a limb, the routine retention is 3-7 days; in sweaty summer conditions shorten it to 2-3 days, while in winter it can be close to 7 days. Press the embedded site several times a day to reinforce deqi, and remove it if redness, swelling or pain appears.",
        "What should be watched during embedding?",
        "Keep the area clean and dry and protect it from water; do not rub or scratch. If redness, swelling, pain or exudate appears, remove the needle immediately and disinfect.",
        "Which sites are unsuitable for embedding?",
        "Use caution at joints with a large range of motion, at sites prone to friction and where the skin is broken. The results of this tool are reference only and cannot replace a physician's diagnosis and prescription; follow medical advice in practice.",
        "About the Intradermal Needle (Embedding) Retention Time Calculator",
        "Intradermal Needle (Embedding) Retention Time Calculator - calculates the retention time of an intradermal needle (press needle or granular type) according to the point region, season and patient condition, to standardize embedding practice. A medical professional tool based on authoritative medical standards, for reference only.",
    ]))

    write('meridian-pathway', build('meridian-pathway', [
        "🪡 Meridian Sensation (Propagated Sensation Along the Meridian) Pathway Display",
        "Displays the courses of the fourteen meridians, the laws of propagated sensation along the meridians and the main acupoints",
        "📖 View the usage guide for the Meridian Sensation (Propagated Sensation) Pathway Display",
        "(1) Select the meridian",
        "Type of propagated sensation",
        "Typical propagation (whole course)",
        "Partial propagation (short course)",
        "Cross-meridian propagation",
        "Individual sensitivity to propagation",
        "Insensitive type",
        "Relatively sensitive type",
        "Marked type",
        "📋 Copy the meridian information",
        "📋 Propagated sensation characteristics reference",
        "⚠️ Propagated sensation along the meridian is an objective meridian phenomenon, but the manifest rate varies greatly between individuals (about 15-20%); propagation is not the only indicator of efficacy. This tool is for study reference.",
        "📚 Deep dive: Meridian Sensation (Propagated Sensation) Pathway Display",
        "Study the course of the hand Taiyin Lung meridian running from chest to hand.",
        "Demonstrate the route of propagation along the meridian after deqi is obtained.",
        "Check the acupoints belonging to the meridian when locating points.",
        "View the meridian course",
        "The foot Yangming Stomach meridian starts beside the nose, descends through the face, neck, chest and abdomen to the lower limb and ends at the second toe; along the line are distributed such important points as Chengqi, Tianshu and Zusanli, and both point location and propagation demonstration follow this route.",
        "What is propagated sensation along the meridian?",
        "It is the phenomenon in which soreness, numbness and distension during needling or pressure travel along the meridian route; it is a perceptible expression of the movement of meridian qi and varies between individuals.",
        "Do the meridians have an anatomical entity?",
        "The meridians are the TCM functional generalization of the body's connecting system; modern research offers several hypotheses, and no single anatomical structure has been matched to them. This tool is for study reference.",
        "About the Meridian Sensation (Propagated Sensation) Pathway Display",
        "Meridian Sensation (Propagated Sensation) Pathway Display - displays the courses of the fourteen meridians, the laws of propagated sensation along the meridians and the main acupoints, to help understand the phenomenon of meridian sensation. A medical professional tool based on authoritative medical standards, for reference only.",
        "How to use the Meridian Sensation (Propagated Sensation) Pathway Display",
    ]))

    write('moxibustion-count', build('moxibustion-count', [
        "🧴 Moxibustion Cone Count (Skin Reaction) Individualized Recommender",
        "Recommends the number of moxa cones individually according to the skin reaction and the deficiency or excess of the pattern, to avoid burns",
        "/ Moxibustion Cone Count Individualized Recommender",
        "📖 View the usage guide for the Moxibustion Cone Count (Skin Reaction) Individualized Recommender",
        "(1) Type of moxibustion",
        "Moxibustion method",
        "Moxa cone moxibustion (direct)",
        "Indirect cone moxibustion (with ginger, garlic or salt)",
        "Warm needling",
        "Moxa stick moxibustion (gentle warming)",
        "Moxa cone size",
        "Small (wheat grain)",
        "Medium (soybean)",
        "Large (jujube pit)",
        "(2) Skin reaction grading (observed during moxibustion)",
        "Deficiency/cold pattern",
        "Excess pattern (use moxibustion with caution)",
        "Acute condition",
        "Patient tolerance",
        "🧴 Recommend the cone count",
        "📋 Moxa cone count and skin reaction reference",
        "⚠️ Suppurative (scarring) moxibustion requires a specialized procedure and the patient's consent; direct moxibustion should be used with caution on the face, over joints and large vessels, and on the abdomen of pregnant women. This tool is for reference.",
        "📚 Deep dive: Moxibustion Cone Count (Skin Reaction) Individualized Recommender",
        "For deficiency-cold stomach pain, moxa Zhongwan and Zusanli with a moderate cone count.",
        "For yang deficiency with cold intolerance, moxa Mingmen and Guanyuan; the cone count may be increased.",
        "For yin deficiency with effulgent fire and hot red skin, reduce the count or stop immediately.",
        "Recommend the number of moxa cones",
        "For an adult with deficiency-cold diarrhea, moxa Shenque (with ginger insulation) 3-5 cones per point, once daily; if the moxibustion site becomes clearly hot, red and burning, reduce to 1-2 cones or stop to prevent burns. For children and those with diminished sensation, halve the count and provide dedicated supervision.",
        "How long is one cone?",
        "Traditionally one cone is the burning out of a single moxa cone (for example wheat-grain size); modern practice mostly uses a suspended moxa stick with timing (10-15 minutes per point). The two can be converted, with comfortable warmth as the guide.",
        "What should be done if a burn occurs?",
        "Stop moxibustion immediately and cool the area; do not rupture the blisters; seek medical care in severe cases. The safety upper limit in this tool is reference only.",
        "About the Moxibustion Cone Count (Skin Reaction) Individualized Recommender",
        "Moxibustion Cone Count (Skin Reaction) Individualized Recommender - recommends the number of moxa cones individually according to the skin reaction (flushing, red areola, burning heat) and the deficiency or excess of the pattern, to avoid burns. A medical professional tool based on authoritative medical standards, for reference only.",
        "How to use the Moxibustion Cone Count (Skin Reaction) Individualized Recommender",
    ]))


if __name__ == '__main__':
    main()
