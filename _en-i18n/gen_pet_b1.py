#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pet')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pet')
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
    out = {'slug': slug, 'industry': 'pet', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('index', build('index', [
        "🐾 Pet Care Tools",
        "Pet Care Tools",
        "Pet Feeding Calculator",
        "Pet Feeding Calculator is a free online pet-care tool; the Pet Feeding Calculator is a free online pet-care tool: enter parameters to get real-time results; runs entirely in the browser, no data uploaded, no registration, just open the browser to use. Runs entirely in the browser, no data uploaded, no regi...",
        "The Pet Age Converter converts a cat's or dog's age to an equivalent human age using empirical coefficients, helping understand the pet's life stage; suitable for pet-keeping science popularization and health management.",
        "Diagnosis and treatment (exam / diagnosis / prescription) workflow",
        "Enter the pet's basic information and symptoms, and the system assists in generating exam suggestions, differential diagnosis and medication references. For study reference only; cannot replace a licensed veterinarian's diagnosis.",
        "Compliance (qualification / regulation / inspection) assurance",
        "Check each compliance item, and the system automatically evaluates qualification completeness, regulatory compliance and inspection pass rate, and gives a compliance grade and remediation advice.",
        "The pet-store cost, control and profit analysis tool accounts for operating cost and profit per general financial rules, suitable for store operation analysis, pricing and profitability estimation.",
        "Build health records for dogs and cats; the built-in vaccination and deworming cycles auto-compute the next due date and give color alerts, helping owners keep pets immunized and dewormed on time without missing a dose.",
        "Pet Training Plan",
        "Select the pet type (dog/cat), age stage and training goals (housebreaking, heel, recall, etc.); the tool generates daily training subjects, duration and reward schemes, arranging progressively harder exercises by stage to help owners build a regular pet-behavior training rhythm.",
        "Pet Medication Dosage",
        "Enter the pet's weight and the selected drug (e.g. dewormer, antibiotic); the tool computes the single dose and dosing frequency by dose per kg of body weight, suggests dosage ranges of common pet-specific drugs, and the result is for reference only; follow your vet's advice for actual medication.",
        "About Pet Care Tools",
        "The Pet Care Tools collection gathers 9 free online tools covering common calculation, conversion and lookup needs in pet-care scenarios. Whether you are a professional, student or ordinary user in the field, you can find ready-to-use handy tools here. All tools run entirely in the browser with no data uploaded to the server, protecting privacy and security.",
        "The pet-care tools collected on this page include (representative samples):",
        "These tools help you quickly complete common pet-care tasks without memorizing complex formulas or manual conversions; just enter to get results.",
        "Do Pet Care Tools need download or registration?",
        "No. All pet-care tools on this page are pure front-end online tools; open the web page and use them directly, with no software installation, no account registration and no data upload.",
        "Are the Pet Care Tools calculations accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and common industry standards, with results available instantly. All operations are performed locally on your device, data is never uploaded to a server, and privacy and security are guaranteed.",
    ]))

    write('pet-age-converter', build('pet-age-converter', [
        "🐾 Pet Age Converter",
        "Convert a dog's or cat's age to an equivalent human age (approximate reference only).",
        "/ Pet Age Converter",
        "📖 View the \"pet-age-converter User Guide\"",
        "Dog age to human age: the first 2 years count about 12 to 15 human years each (1 yr ≈ 15, 2 yr ≈ 24), then by body size add 4 to 7 human years per year (small 4, medium 5, large 6, extra-large 7); cat age: the first 2 years count as 15 and 9 respectively, then add 4 human years per year; a human-equivalent age above 7 is late adulthood and above 10 is senior, when joint, oral and metabolic assessments should be strengthened.",
        "Dog body size / cat age type",
        "📚 In-Depth Analysis: Pet Age Conversion",
        "Convert a dog's or cat's real age into an equivalent human age to intuitively understand its life stage and care priorities.",
        "Match diet, vaccination, exercise and check-up frequency to the converted stage (juvenile / adult / senior).",
        "Educate adopters on breed differences such as 'small dogs live longer and age later'.",
        "Example: cat vs dog comparison",
        "Cat 3 yr → 16+(3-2)×4 = 20 human yr (adult); small dog 5 yr → 16×ln5+31 ≈ 56.75 → 57 human yr (adult); large dog 3 yr → 22×ln3+15+2 ≈ 41 human yr (already near senior). The tool also labels stages by <1 juvenile / <7 adult / ≥7 senior.",
        "Are the cat and dog conversion formulas the same?",
        "No. Cat: <1 yr ×15, <2 yr 24+(a-1)×2, ≥2 yr 16+(a-2)×4. Dog: ≤2 yr small/medium takes 12, large takes age×10.5; >2 yr small/medium by 16×ln(age)+31, large plus +2 (capped at 100 yr). Large dogs age faster.",
        "Can the conversion result be used as a medical basis?",
        "Reference only. The formula gives an approximate equivalent human age to help understand the stage; actual lifespan and health management are still affected by genetics, nutrition and medical conditions; senior dogs and cats should have more frequent check-ups.",
    ]))

    write('pet-feeding-calc', build('pet-feeding-calc', [
        "🧮 Pet Feeding Calculator",
        "Estimate daily calorie needs and daily feed amount (g) from weight, age and activity level.",
        "/ Pet Feeding Calculator",
        "📖 View the \"pet-feeding-calc User Guide\"",
        "Resting energy requirement RER (kcal/day) = 70 × body weight (kg) to the 0.75 power; daily energy requirement DER = RER × factor (juvenile 2.5 to 3.0, neutered adult 1.6, intact adult 1.8, senior 1.2 to 1.4, weight-loss 0.8 to 1.0, weight-gain 1.2 to 1.8); daily feed (g) = DER ÷ energy per gram of feed (kcal/g); feed in 2 to 3 meals and adjust by 10% every 2 to 4 weeks by body-condition score.",
        "Activity level",
        "Low activity",
        "Moderate activity",
        "High activity",
        "Very active",
        "Food energy (kcal/100g)",
        "Maintenance",
        "Weight gain / muscle",
        "Weight loss",
        "📚 In-Depth Analysis: Pet Feeding Calculation",
        "Estimate daily calorie needs from the pet's weight, age and activity, then convert to specific feed grams to avoid over- or under-weight.",
        "When switching food, recompute the feed amount from the new food's kcal/100g to keep calories consistent and transition smoothly.",
        "During neutering / fat-loss, set the goal to 'weight loss' to auto-cut 10% of calories; during weight-gain raise by 10%.",
        "Example: 10 kg adult dog, maintenance",
        "Dog RMR = 130×weight^0.75 = 130×10^0.75 ≈ 731 kcal; age factor (adult=1) × activity (1) × RMR = 731 kcal/day. At 400 kcal/100g food, daily ration = 731÷400×100 ≈ 183 g, fed in 2–3 meals.",
        "Why do dogs and cats have different basal-metabolism coefficients?",
        "Dog RMR coefficient 130, cat 70 (both × body weight to the 0.75 power), reflecting species differences; cats have a higher metabolic rate. Juvenile (<1 yr) age factor 2, adult 1, senior (≥7) 0.9.",
        "What if the calculation differs from actual intake?",
        "The formula is a theoretical estimate; in practice fine-tune 5%–10% by weight change and appetite;",
        "Treat calories",
        "also count into the daily total; for overweight pets prefer low-fat food and increase activity.",
    ]))


if __name__ == '__main__':
    main()
