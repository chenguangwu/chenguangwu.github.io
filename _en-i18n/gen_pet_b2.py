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
    write('pet-medicine', build('pet-medicine', [
        "💊 Pet Common Medication Dosage Calculator",
        "Calculate common drug dosages by pet body weight (for reference only; follow your vet's advice)",
        "Pet Medication Dosage",
        "/ Pet Medication Dosage",
        "📖 View the \"Pet Common Medication Dosage Calculator User Guide\"",
        "Pet body weight (kg)",
        "Drug category",
        "Dewormer",
        "Antiemetic / gastrointestinal",
        "Antipyretic / analgesic",
        "Antiallergic",
        "Specific drug",
        "Twice daily",
        "Three times daily",
        "Single use",
        "💊 Calculate dose",
        "📊 Dosage",
        "📖 Common drug reference",
        "⚠️ Medication contraindications",
        "🐕 Common dog medication dosage table",
        "Dosage range",
        "Bacterial infection",
        "Cephalexin",
        "Skin / respiratory infection",
        "Anaerobic / intestinal infection",
        "Omeprazole",
        "Excess stomach acid / ulcer",
        "Diphenhydramine",
        "2–3 times daily",
        "Allergy / motion sickness",
        "Fenbendazole",
        "Once daily × 3 days",
        "🐈 Common cat medication dosage table",
        "Broad-spectrum antibiotic",
        "Oral / intestinal infection",
        "Acid suppression",
        "1–2 times daily",
        "Respiratory infection",
        "Tapeworm",
        "❌ Absolutely forbidden drugs for cats and dogs:",
        "1. Acetaminophen (Tylenol):",
        "• Cats are extremely sensitive; a small amount can be fatal (even one tablet can kill)",
        "• Overdose in dogs also causes liver damage and hemolysis",
        "2. Ibuprofen (Brufen):",
        "• Forbidden for both cats and dogs; can cause gastric ulcer and kidney failure",
        "3. Other NSAIDs (naproxen, etc.):",
        "• Do not use unless prescribed by a veterinarian",
        "4. Ivermectin (forbidden for Collies):",
        "• Forbidden for MDR1-gene-defect breeds such as Collie, Shetland Sheepdog and Border Collie",
        "⚠️ Medication safety principles:",
        "1. When unsure, ask a vet first; do not search online and medicate by yourself",
        "2. Use extra caution for puppies/kittens, pregnant and senior pets",
        "3. Dose must be adjusted for impaired liver/kidney function",
        "4. Follow the course strictly; do not stop medication on your own",
        "5. Observe reactions after medication; seek care immediately if abnormal",
        "6. Record medication time and dose to avoid duplicate dosing",
        "💡 Medication tips:",
        "• Tablets: wrap in a treat / cheese / nutritional paste",
        "• Liquids: use a syringe to slowly push from the corner of the mouth",
        "• Capsules: place deep in the throat and massage the neck to help swallow",
        "• Give a little water after dosing to avoid the drug sticking to the esophagus",
        "⚠️ This tool is for reference only and cannot replace a veterinarian's diagnosis. If your pet is sick, seek timely care and do not medicate by yourself.",
        "📚 In-Depth Analysis: Pet Common Medication Dosage Calculator",
        "From the pet's body weight and the selected drug's safe dosage range (mg/kg), compute the single and daily doses to avoid overdose.",
        "Convert to daily total dose by dosing frequency (single / every 8, 12, 24 hours) and match the drug label.",
        "Convert the mg dose into the number of 50/100/250 mg tablets for easy home dosing (reference only; follow the vet's prescription).",
        "Example: dose of a drug for a 10 kg dog",
        "Suppose the drug's canine dose range is 5–10 mg/kg: single dose = 10 kg × (5–10) = 50–100 mg, average 75 mg; if every 12 hours (24÷12 = 2 times/day), daily total 100–200 mg; a 50 mg tablet is about 75÷50 = 1.50 tablets. The exact range follows the drug data sheet.",
        "How is the dose calculated?",
        "Single dose = body weight (kg) × drug dose range (mg/kg); average dose is the mean of the limits; daily total = average dose × doses per day (single = 1, every N hours = 24÷N). When some drugs are labeled 'not recommended' for a species, a contraindication is shown.",
        "Can you just feed it once calculated?",
        "No. This tool is only a dosage reference; actual medication must be by veterinary prescription; doses for liver/kidney disease, pregnant, young and senior pets often need reduction, and most human drugs are toxic to pets, so never apply them directly.",
        "About Pet Medication Dosage",
        "Pet medication dosage. A pet-care tool that helps compute pet diet and health metrics.",
    ]))

    write('convert-25', build('convert-25', [
        "🐾 Pet Age (cat/dog) to Human Conversion",
        "Cat / dog",
        "📖 View the \"Pet Age (cat/dog) to Human Conversion User Guide\"",
        "Milli pet age",
        "Kilo pet age",
        "Human conversion",
        "Milli human conversion",
        "Kilo human conversion",
        "📚 In-Depth Analysis: Pet Age (cat/dog) to Human Conversion",
        "Convert the pet's 'pet years' by a coefficient into an equivalent human age, to intuitively show your family 'how old in human years it is'.",
        "When making vaccine / diet / exercise plans, match care advice to the converted stage (juvenile / adult / senior).",
        "For science popularization or content creation, you need to convert",
        "to a unified human scale for comparison display.",
        "Example: coefficient method",
        "Formula: result = value × coefficient × (source factor ÷ target factor). Suppose a pet's 1 pet year corresponds to human coefficient f=7.5, target factor t=1, value v=3, then result = 3×1×7.5/1 = 22.5 human yr. In actual conversion, take the corresponding coefficient by selected species and age range.",
        "What do the coefficient and source/target factor each do?",
        "The coefficient is for overall scaling (e.g. species / age-stage conversion ratio); the source factor / target factor are for",
        ": result = value × coefficient × (source factor ÷ target factor). Convert both units to the same base then divide.",
        "How to read a result with many decimal places?",
        "The tool shows 6 decimal places; in practice keep only the",
        "significant figures",
        "; if the source/target factor is set reversed, the result differs by a conversion ratio, so confirm the factor direction when checking.",
        "About Pet Age (cat/dog) to Human Conversion",
        "Pet Age (cat/dog) to Human Conversion. A pet-care tool that helps compute pet diet and health metrics.",
    ]))


if __name__ == '__main__':
    main()
