#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'nutrition')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'nutrition')
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
    out = {'slug': slug, 'industry': 'nutrition', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('generator-nutrition-label', build('generator-nutrition-label', [
        "🥗 Nutrition Label One-Click Generator",
        "Nutrition Label",
        "Nutrition labels are declared per 100 g or per serving: energy(kJ) = protein × 17 + fat × 37 + carbohydrate × 17 + dietary fiber × 8; NRV% = nutrient content ÷ NRV reference for that nutrient × 100% (the NRV references are 8400 kJ for energy, 60 g for protein, 60 g for fat, 300 g for carbohydrate and 2000 mg for sodium); the layout follows the format required by GB 28050.",
        "📚 Deep Dive: One-Click Nutrition Label Generation (NRV)",
        "Generate a compliant label from the energy, protein, fat, carbohydrate and sodium per 100 g",
        "Show each nutrient's share of the daily reference value against NRV",
        "Self-check prepackaged foods for compliance and verify the declared values",
        "Label and NRV%",
        "A food per 100 g: energy 450 kcal, protein 10g, fat 20g, carbohydrate 55g, sodium 300mg. NRV references (energy 2000 / protein 60 / fat 60 / carbohydrate 300 / sodium 2000): protein NRV% = 10/60 = 16.7%, fat = 20/60 = 33.3%, sodium = 300/2000 = 15%.",
        "High-Sodium Warning",
        "Sodium of 800mg per 100 g → NRV% = 40%; eating 250 g in one day would already reach 100%, so high-sodium foods need portion control.",
        "What are the NRV references based on?",
        "They follow GB 28050, the general standard for nutrition labels of prepackaged foods: energy 2000 kcal, protein 60g, fat 60g, carbohydrate 300g, sodium 2000mg and so on.",
        "How is energy calculated?",
        "Energy(kcal) ≈ protein×4 + carbohydrate×4 + fat×9 (dietary fiber is usually listed and deducted separately), and it must stay within the allowed deviation from the declared value.",
        "About Nutrition Label One-Click Generation",
        "Nutrition label one-click generation. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))
    write('nutrition-1', build('nutrition-1', [
        "🥗 Percentage Calculator (Nutrition)",
        "Calculate percentages, shares and growth rates of values",
        "Reference percentage for nutrients (intake)",
        "/ Reference Percentage for Nutrients (Intake)",
        "Part = total × percentage ÷ 100; share = actual intake ÷ reference value × 100% (for example an intake of 45 mg against an NRV of 60 mg gives a 75% share); change rate = (new value − original value) ÷ original value × 100%; this is used to compute how much of the daily NRV a nutrient intake covers, supporting diet records and nutrition assessment.",
        "📚 Deep Dive: Nutrient NRV Percentage Calculation",
        "Enter the actual intake and the reference value to compute the share of the daily NRV",
        "After keeping a diet diary, see whether an item meets or exceeds its target",
        "Switch between the two modes: a part as a percentage of the whole, or a whole back-solved into the part",
        "Share Calculation",
        "Actual protein intake 48g against an NRV reference of 60g → share = 48/60×100% = 80%; you are 12g short of the target. Change: from 40 to 48 → growth rate = (48−40)/40×100% = 20%.",
        "Back-solving the Part",
        "To reach 50% of the NRV (with a sodium reference of 2000mg) → sodium = 2000×50% = 1000mg; that is, keeping sodium under 1000mg in this meal holds the half-day allowance.",
        "Is an NRV% over 100% dangerous?",
        "A single meal over 100% is not necessarily a problem, look at the whole-day total; sodium and saturated fat chronically above the NRV are bad for cardiovascular health and deserve attention.",
        "Are the reference values the same for men and women?",
        "NRV uses one unified adult reference and does not distinguish sex or age; individual needs (such as pregnancy or older age) should be adjusted separately according to the dietary guidelines.",
    ]))
    write('recommender-2', build('recommender-2', [
        "🧓 Recommendations for Older Adults (Protein/Vitamins)",
        "Protein/Vitamins",
        "Recommended daily protein for older adults = body weight(kg) × 1.0 to 1.2 g (it can be raised to 1.2 to 1.5 g for sarcopenia or during recovery from illness), and high-quality protein should make up more than 50%; calcium 1000 mg, vitamin D 15 to 20 μg (800 to 1000 IU); energy = basal metabolism × 1.2 to 1.3, and spreading it over 4 to 5 meals together with resistance training helps prevent muscle loss.",
        "📚 Deep Dive: Protein and Vitamin Recommendations for Older Adults",
        "Estimate the daily protein and key vitamin needs of older adults from age and body weight",
        "Prevent sarcopenia with high-protein foods and vitamin D and calcium sources",
        "Check whether B12 and calcium meet the guideline targets",
        "Protein Needs in Older Age",
        "For a 60 kg older adult at 1.0-1.2 g/kg → 60-72 g/day; roughly = 1 egg (6g) + 250 ml milk (8g) + 100 g fish (20g) + 100 g tofu (8g) + staples, vegetables and fruit (about 20g) adds up to the target.",
        "Key Micronutrients",
        "Older adults are recommended 10-15 μg/day of vitamin D, 1000 mg of calcium and 2.4 μg of B12; insufficient sunlight and reduced absorption make deficiencies likely, so diet plus supplement assessment is needed.",
        "Why do older adults need more protein than young adults?",
        "To resist sarcopenia and maintain immunity, the recommendation for older adults is 1.0-1.2 and even 1.2-1.5 g/kg, above the 0.8 for adults; spreading intake evenly across meals also absorbs better.",
        "Is a vegetarian diet enough?",
        "Plant proteins need a diverse mix for complementarity, and B12, calcium and vitamin D are easy to miss, so strict vegetarians are advised to monitor regularly and supplement appropriately.",
        "About Recommendations for Older Adults (Protein/Vitamins)",
        "Recommendations for older adults (protein and vitamins). Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))
    write('recommender-3', build('recommender-3', [
        "🥗 Immunity (Vitamin C/Zinc) Recommendations",
        "Vitamin C/Zinc",
        "Recommended vitamin C intake for adults is 100 mg/day (tolerable upper intake level 2000 mg), and zinc 7.5 to 12.5 mg/day (upper limit 40 mg); vitamin C is rich in fresh jujubes, kiwifruit and green peppers (30 to 240 mg per 100 g), and zinc is rich in oysters, lean meat and nuts (2 to 15 mg per 100 g); during an infection you can supplement in moderate amounts under medical guidance, but large doses should not be taken long term.",
        "📚 Deep Dive: Immunity (Vitamin C/Zinc) Recommendations",
        "Estimate the daily recommended amounts of vitamin C and zinc by population and list food sources",
        "Compare the recommendation with the tolerable upper limit (UL) to avoid excess",
        "Self-check whether your intake is enough when you have a cold or low immunity",
        "Recommendation and Upper Limits",
        "For adults vitamin C RNI is 100mg/day with UL 2000mg; zinc is 12.5mg for men and 7.5mg for women with UL 40mg. One kiwifruit (about 70mg of vitamin C) plus one serving of oysters (16mg of zinc) easily hits the targets and can even exceed the zinc upper limit.",
        "Rich Food Sources",
        "Vitamin C: fresh jujubes, kiwifruit, citrus, green peppers; zinc: oysters, red meat, nuts, whole grains; a balanced diet usually needs no supplements.",
        "Does more vitamin C prevent colds?",
        "Regular doses do not prevent colds and only slightly shorten the course; staying above 2000mg/day long term risks diarrhea and kidney stones, so megadosing is unnecessary.",
        "What are the harms of excess zinc?",
        "Staying above the UL(40mg) long term interferes with copper and iron absorption and can suppress immunity; follow medical advice for zinc supplements, and food sources are safer.",
        "About Immunity (Vitamin C/Zinc) Recommendations",
        "Immunity (vitamin C and zinc) recommendations. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))
    write('recommender-4', build('recommender-4', [
        "🥗 Dietary Fiber Recommended Amount Check",
        "Recommended Amount",
        "The daily fiber recommendation is estimated from energy intake: 10 to 14 g per 1000 kcal is needed, which is about 25 to 30 g for adults (about 30 g for men and 25 g for women); adequacy rate = actual intake ÷ recommended amount × 100%; suggested sources are 50 to 150 g of whole grains, 300 to 500 g of vegetables, 200 to 350 g of fruit and moderate amounts of beans, plus enough water to let the fiber work.",
        "📚 Deep Dive: Meeting the Dietary Fiber Recommendation",
        "Estimate the daily fiber target (about 25-30g) by sex and energy intake",
        "Assess how close your current intake is and get a plan to close the gap",
        "Slot high-fiber foods into a balanced meal plan",
        "Adequacy Rate",
        "For an adult at 2000 kcal the fiber target ≈ 25-30g; with only 15 g currently the adequacy rate is 50-60%, so 10-15 g must be added, for example oats 30g at breakfast (+3g) + a mixed-grain rice dish at lunch + one serving of beans or vegetables at each of lunch and dinner.",
        "Source Pairing",
        "Soluble fiber (oats, beans, apple) steadies blood sugar, while insoluble fiber (whole wheat, vegetables) promotes bowel movement; combining the two is more complete.",
        "How is the fiber target set?",
        "For adults it is mostly 25-30 g/day (or 14 g per 1000 kcal); it decreases with age for children, and older adults should build up gradually to avoid bloating.",
        "Do you need water when adding fiber?",
        "Yes, fiber absorbs water and expands, and a shortage of water actually worsens constipation; raise daily water to 1.5-2 L alongside the fiber increase.",
        "About Meeting the Dietary Fiber Recommended Amount",
        "Meeting the dietary fiber recommended amount. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))


if __name__ == '__main__':
    main()
