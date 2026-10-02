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
    write('eight-principles', build('eight-principles', [
        "🌿 Eight-Principle Differentiation Logic Tool",
        "Select the pattern features of the four pairs of principles to automatically derive the result of eight-principle differentiation (exterior/interior · cold/heat · deficiency/excess · yin/yang)",
        "The eight principles cross-determine patterns with four pairs: exterior/interior locates the disease position, cold/heat determines the nature, deficiency/excess weighs pathogen against healthy qi, and yin/yang is the overarching principle (exterior, heat and excess are yang; interior, cold and deficiency are yin). After judging each pair item by item and combining them, such as an exterior-cold excess pattern or an interior-deficiency heat pattern, the remaining six principles yield the overall yin/yang attribute, which determines the treatment principle such as releasing the exterior, warming the interior, clearing heat or tonifying deficiency.",
        "I. Exterior / Interior (locating the depth of the disease)",
        "II. Cold / Heat (locating the nature of the disease)",
        "III. Deficiency / Excess (weighing pathogen against healthy qi)",
        "IV. Yin / Yang (overarching principle)",
        "Derive the pattern",
        "After selecting the features of each principle, click \"Derive the pattern\"",
        "💡 Yin and yang are the overarching principle of the eight principles: exterior, heat and excess are yang, while interior, cold and deficiency are yin. Clinically, exterior, interior, cold, heat, deficiency and excess often interleave, so the primary versus secondary and true versus false aspects must be distinguished.",
        "🌿 Eight-Principle Differentiation key points",
        "Principle",
        "Pattern",
        "Tongue and pulse",
        "Exterior / interior",
        "Exterior pattern",
        "Aversion to cold with fever, head and body pain, nasal congestion",
        "Thin white coating, floating pulse",
        "Interior pattern",
        "Fever without aversion to cold or chills without fever, zang-fu symptoms",
        "Thick coating, deep pulse",
        "Aversion to cold with preference for warmth, pale face, cold limbs",
        "Pale tongue with white coating, slow pulse",
        "Fever with preference for cool, flushed face, thirst",
        "Red tongue with yellow coating, rapid pulse",
        "Pale complexion, fatigue and weakness, shortness of breath",
        "Pale tender tongue, weak empty pulse",
        "Loud forceful voice, abdominal pain refusing pressure, constipation",
        "Thick coating, forceful pulse",
        "Yin / yang",
        "Yang pattern",
        "Signs of exterior, heat and excess (excitement, hyperactivity)",
        "Red tongue with yellow coating, rapid forceful pulse",
        "Yin pattern",
        "Signs of interior, cold and deficiency (inhibition, decline)",
        "Pale tongue with white coating, deep slow weak pulse",
        "📚 Deep dive: eight-principle differentiation logic",
        "Exterior, interior, cold and heat",
        "Deficiency, excess, yin and yang",
        "Treatment principle derivation",
        "Exterior cold pattern",
        "Selecting exterior + cold → \"exterior cold pattern: wind-cold invading the exterior, treated with acrid-warm exterior release, formulas such as Ma Huang Tang and Jing Fang Bai Du San\"; exterior heat uses Yin Qiao San or Sang Ju Yin.",
        "Interior excess heat",
        "Interior + heat + excess → \"interior excess heat pattern: clear heat, drain fire and purge fu organs, with Bai Hu Tang and Cheng Qi type formulas\"; half-exterior half-interior uses Xiao Chai Hu Tang to harmonise.",
        "Watch for true and false cold and heat",
        "Cold signs that actually belong to a yang pattern indicate true heat with false cold. Distinguish by preference for cold or heat, the pulse and abdominal warmth to avoid wrongly warming.",
        "What do the eight principles refer to?",
        "Yin and yang (overarching), exterior/interior, cold/heat and deficiency/excess; pairing them locates the disease position and nature.",
        "What if I choose wrong?",
        "The tool offers the corresponding formula hints, but these are for study only. Clinically a physician must combine all four diagnostic methods.",
        "About \"Eight-Principle Differentiation Logic Tool\"",
        "Eight-Principle Differentiation Logic Tool - TCM tool for exterior, interior, cold, heat, deficiency, excess, yin and yang differentiation, deriving the eight-principle analysis. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))

    write('disease-nature', build('disease-nature', [
        "🩺 Disease Nature Discriminator (Six Pathogenic Factors)",
        "Discriminate the nature of the six external pathogenic factors (wind, cold, summer heat, dampness, dryness, fire), ticking symptoms to analyse the nature automatically (based on the six pathogenic factor content of TCM Aetiology)",
        "Disease Nature Discriminator",
        "/ Disease Nature Discriminator",
        "Step one: select the suspected nature of the pathogen",
        "Step two: tick the patient's symptoms",
        "Analyse the nature",
        "After ticking symptoms, click \"Analyse the nature\"",
        "💡 The six pathogenic factors are the collective term for external pathogenic factors, with seasonal character and the ability to combine (such as wind-cold, wind-heat, damp-heat). Clinically the season of onset, environment and symptom features must be considered together.",
        "📋 Comparison of the pathogenic characteristics of the six factors",
        "Pathogen",
        "Site most easily affected",
        "Yang pathogen, light and dispersing",
        "Moves readily and changes often, chief of the hundred diseases, easily attacks yang positions",
        "Muscle surface, head and face, lung",
        "Yin pathogen, congealing and contracting",
        "Damages yang qi, congeals qi and blood, constricts the channels",
        "Muscle surface, joints, spleen and stomach",
        "Summer heat",
        "Yang pathogen, rising and dispersing, consuming fluids",
        "Only in summer, damages fluids and qi, easily carries dampness",
        "Head and face, heart, lung",
        "Dampness",
        "Yin pathogen, heavy, turbid and sticky",
        "Obstructs the qi mechanism, lingering and hard to cure, easily attacks yin positions",
        "Spleen and stomach, lower limbs",
        "Dryness",
        "Yang pathogen, drying and desiccating, damaging fluids",
        "Damages body fluids, causes dryness and roughness, common in autumn",
        "Lung, skin",
        "Fire (heat)",
        "Yang pathogen, flaring upward and consuming fluids",
        "Generates wind and stirs blood, causes swelling and sores, disturbs the shen",
        "Heart, liver and all zang-fu",
        "📚 Deep dive: disease nature discrimination (six pathogenic factors)",
        "Six pathogenic factor matching",
        "Degree of fit",
        "Combined pathogen hints",
        "Wind pathogen fit 67%",
        "4 of 6 wind symptoms ticked → confidence=4/6×100≈66.7%, \"high fit\"; if cold (c1/c6) is also indicated it gives wind-cold.",
        "Summer heat with dampness",
        "Summer heat symptoms with dampness signs d3/d5 → indicates \"summer heat-dampness\", treated by clearing summer heat and resolving dampness (Xiang Ru Yin type formulas).",
        "What are the six pathogenic factors?",
        "Wind, cold, summer heat, dampness, dryness and fire, each with its own main symptom combination.",
        "What is the fit threshold?",
        "A ticked proportion of 60% or more is high, 40-59% moderate and below 40% low; for reference only.",
        "About \"Disease Nature Discriminator\"",
        "Disease Nature Discriminator - TCM tool discriminating the nature of the six external pathogenic factors (wind, cold, summer heat, dampness, dryness, fire) with pattern analysis. Professional medical tool based on authoritative medical standards, for reference only.",
        "How to use Disease Nature Discriminator (Six Pathogenic Factors)",
        "What does Disease Nature Discriminator (Six Pathogenic Factors) do?",
        "How do I use Disease Nature Discriminator (Six Pathogenic Factors)?",
        "Which scenarios suit Disease Nature Discriminator (Six Pathogenic Factors)?",
    ]))


if __name__ == '__main__':
    main()