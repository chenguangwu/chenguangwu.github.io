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
    write('treatment-principle', build('treatment-principle', [
        "🩺 Treatment Principle and Method Selection Advisor",
        "Select the corresponding treatment principle and method from the differentiation result, covering treatment on the opposite and same aspects, treating the branch versus the root, supporting upright qi and dispelling pathogens, adjusting yin and yang, and adapting to the three causes",
        "Treatment principle derivation",
        "Treatment on the opposite and same aspects",
        "Treating the branch versus the root",
        "Supporting upright qi and dispelling pathogens",
        "Adjusting yin and yang",
        "Adapting to the three causes",
        "Select the treatment principle by the nature of the pattern",
        "Nature of the disease",
        "Cold and deficiency combined",
        "Heat and excess combined",
        "True cold with false heat (yin excess repelling yang)",
        "True heat with false cold (yang excess repelling yin)",
        "True deficiency with false excess",
        "True excess with false deficiency",
        "Priority of branch versus root",
        "Disease as root, symptoms mild",
        "Branch symptoms urgent",
        "Branch and root equally important",
        "Strength of pathogen versus healthy qi",
        "Deficiency of upright qi dominant",
        "Strength of pathogen dominant",
        "Upright qi deficient with pathogen present",
        "Treatment on the opposite and same aspects",
        "Treatment on the opposite works against the nature of the pattern (the conventional method); treatment on the same follows the false appearance (for true and false patterns)",
        "Applicable patterns",
        "Treatment on the opposite",
        "(contrary treatment)",
        "Treat cold with heat",
        "Use warming hot medicines for cold patterns",
        "Excess cold, deficiency cold",
        "Treat heat with cold",
        "Use cooling cold medicines for heat patterns",
        "Excess heat, deficiency heat",
        "Tonify deficiency",
        "Use tonifying medicines for deficiency patterns",
        "Qi deficiency, blood deficiency, yin deficiency, yang deficiency",
        "Drain excess",
        "Use attacking medicines for excess patterns",
        "Qi stagnation, blood stasis, phlegm-fluid, food stagnation",
        "Treatment on the same aspect",
        "(following treatment)",
        "Use heat for heat",
        "Use warming hot medicines for false heat patterns",
        "Use cold for cold",
        "Use cooling cold medicines for false cold patterns",
        "Use blocking for blockage",
        "Use tonifying medicines for false excess patterns",
        "True deficiency with false excess (spleen deficiency abdominal distension)",
        "Use passage for passage",
        "Use draining medicines for false deficiency patterns",
        "True excess with false deficiency (heat binding with overflow)",
        "Treating the branch and the root",
        "Principle",
        "In urgency, treat the branch",
        "Branch disease urgent and severe, treat the branch first",
        "Branch symptoms threatening life or hindering root treatment",
        "Major bleeding: stop bleeding first; severe pain: relieve pain first",
        "When not urgent, treat the root",
        "Branch symptoms not urgent, treat the root as the main approach",
        "Chronic disease, mild branch symptoms",
        "Slow diarrhoea from spleen deficiency, strengthen the spleen to treat the root",
        "Treating branch and root together",
        "Treat branch and root together",
        "Both branch and root fairly urgent and severe",
        "Exterior invasion with qi deficiency, boost qi and release the exterior together",
        "Meaning of branch and root",
        "Angle of distinction",
        "Root",
        "Branch",
        "Pathogen-qi relationship",
        "Upright qi is the root",
        "Pathogenic qi is the branch",
        "Zang-fu is the root",
        "Channels are the branch",
        "The disease itself",
        "The primary disease is the root",
        "The secondary disease is the branch",
        "Symptoms and cause",
        "The cause is the root",
        "Symptoms are the branch",
        "Supporting upright qi and dispelling pathogens",
        "Treatment principle",
        "Specific method",
        "Supporting upright qi",
        "Support upright qi and strengthen resistance to disease",
        "Boost qi, nourish blood, nourish yin, warm yang",
        "Dispelling pathogens",
        "Remove pathogenic qi and eliminate the cause",
        "Induce sweating, clear heat, purge downward, resolve dampness",
        "Supporting upright qi while also dispelling pathogens",
        "Mainly support upright qi, also dispel pathogens",
        "Deficiency dominant, with pathogen retained",
        "Tonify middle and boost qi while relieving food stagnation",
        "Dispelling pathogens while also supporting upright qi",
        "Mainly dispel pathogens, also support upright qi",
        "Pathogen dominant, with upright qi deficiency",
        "Clear heat while nourishing yin",
        "Support upright qi first, then dispel pathogens",
        "Tonify first, then attack",
        "Severe deficiency, cannot tolerate attacking and draining",
        "Strengthen the spleen first, then purge downward",
        "Dispel pathogens first, then support upright qi",
        "Attack first, then tonify",
        "Pathogen dominant with qi deficiency; once the pathogen goes, upright qi recovers on its own",
        "Clear heat first, then nourish yin",
        "Reducing the excess",
        "Treat heat with cold (drain yang heat)",
        "Yang excess (excess heat pattern)",
        "Treat cold with heat (warm and disperse yin cold)",
        "Yin excess (excess cold pattern)",
        "Supplementing the deficiency",
        "Seek yin within yang (mainly nourish yin, assisted by tonifying yang)",
        "Yin deficiency (deficiency heat pattern)",
        "Seek yang within yin (mainly tonify yang, assisted by nourishing yin)",
        "Yang deficiency (deficiency cold pattern)",
        "Tonify yin and yang together",
        "Tonify yin and yang together",
        "Yin and yang deficiency",
        "Restore yang and rescue collapse",
        "Emergency restoration of yang",
        "Yang collapse pattern",
        "Rescue yin and prevent collapse",
        "Boost qi and rescue yin",
        "Yin collapse pattern",
        "Key points of treatment principles",
        "Adapting to the season",
        "Warm spring and hot summer",
        "Use warming hot medicines cautiously; acrid-cool mild formulas are appropriate",
        "Cool autumn and cold winter",
        "Use cooling cold medicines cautiously; acrid-warm formulas are appropriate",
        "Summer heat always carries dampness",
        "In summer, remember to clear summer heat and resolve dampness",
        "Adapting to the locality",
        "Warm and humid southeast",
        "Constitutions tend to be thin and weak, so medicines should be cooling",
        "Cold and dry northwest",
        "Constitutions tend to be robust, so medicines should be warming and drying",
        "Humid regions",
        "Dampness predominates; remember to resolve dampness",
        "Adapting to the person",
        "The elderly are often deficient and suit tonification; children have immature zang-fu so medicines should be gentle",
        "Women: note the medication contraindications during menstruation, pregnancy and postpartum",
        "Yang deficiency suits warmth; yin deficiency suits coolness; phlegm-dampness suits drying dampness",
        "This tool is for TCM study and reference only. Clinical prescribing must be done by a licensed TCM practitioner after syndrome differentiation. Never self-medicate.",
        "📚 Deep dive: treatment principle and method advice",
        "Dispelling pathogens and supporting upright qi",
        "With nature=cold the treatment principle map gives \"treatment on the opposite (treat cold with heat)\"; with urgency set to treat the branch in urgency, the branch-root map rescues the branch first.",
        "With nature=true cold with false heat it gives \"treatment on the same (use heat for heat)\", using warming hot medicines for the false heat; the nature-reinforce-defence map sets the balance between dispelling pathogens and supporting upright qi.",
        "What are treatment on the opposite and same?",
        "Treatment on the opposite works against the appearance (treat cold with heat), while treatment on the same follows the false appearance (use heat for heat); both are used for true and false cold and heat.",
        "How are branch and root determined?",
        "Treat the branch in urgency, treat the root when not urgent, and address both when both are urgent.",
        "About \"Treatment Principle and Method Selection Advisor\"",
        "Treatment Principle and Method Selection Advisor - TCM lookup tool for treatment on the opposite and same aspects, treating the branch versus the root, and supporting upright qi while dispelling pathogens. Professional medical tool based on authoritative medical standards, for reference only.",
    ]))


if __name__ == '__main__':
    main()