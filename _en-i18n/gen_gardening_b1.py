#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'gardening')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'gardening')
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
    out = {'slug': slug, 'industry': 'gardening', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('pot-capacity', build('pot-capacity', [
        "🧊 Pot Capacity Calculator",
        "Compute volume, required soil volume and weight from pot shape and size, and get drainage layer advice",
        "📖 Read the \"Pot Capacity and Soil Mix Calculator Usage Guide\"",
        "Frustum pot soil volume V = (π × h ÷ 3) × (R² + R × r + r²), where R is the top radius, r the bottom radius and h the pot height; when top and bottom have the same diameter it simplifies to V = π × r² × h; allowing for soil compaction and headspace, the actual soil fill is about 85% to 95% of the theoretical volume; 1 L = 1000 cm³, soil mix amount = volume (L) × 1.1 (including loss); the repot diameter should be 3 to 5 cm larger than the original pot.",
        "Pot shape",
        "Cylindrical pot",
        "Square pot",
        "Rectangular pot",
        "📐 Compute the amount",
        "• Cylindrical pot: V = π × r² × h (r is the inner radius, h the inner effective height)",
        "• Square pot: V = side² × height",
        "• Rectangular pot: V = length × width × height",
        "• Usable soil volume = total volume − drainage layer (about 2cm of clay pebbles) − top headspace (about 1cm)",
        "• Soil weight = usable volume × 1.2 g/cm³ (typical wet density of general purpose potting soil)",
        "• Clay pebble weight = drainage layer volume × 1.5 g/cm³",
        "📊 Standard Pot Size Table",
        "Size (inch)",
        "Diameter (cm)",
        "Height (cm)",
        "Approx. volume (L)",
        "Suitable plants",
        "3 inch",
        "Succulent seedlings / propagation",
        "4 inch",
        "Succulents / small herbs",
        "5 inch",
        "Herbaceous flowers / medium succulents",
        "6 inch",
        "Roses / pothos / spider plant",
        "7 inch",
        "Medium flowers / shrubs",
        "8 inch",
        "Large potted plants / fruit tree saplings",
        "10 inch",
        "Lemon / camellia / large plants",
        "12 inch",
        "Large woody plants / landscape trees",
        "14 inch",
        "Main feature tree of the courtyard",
        "💡 Tips:",
        "• 1 inch ≈ 3 cm (diameter); sizes are outer diameters, so actual volume is slightly smaller",
        "• For a newly potted plant reserve 1-2cm of top space so watering does not overflow",
        "• Adjust the clay pebble drainage layer thickness by pot depth: shallow pot 1cm, medium pot 2cm, deep pot 3cm",
        "• Soil density 1.2 g/cm³ is a reference value for general purpose potting soil; peat is about 0.3-0.5 and garden soil about 1.5",
        "📚 In-Depth Analysis: Pot Capacity and Soil Mix Calculator",
        "Estimate volume when choosing a repot pot size",
        "Mix potting soil and clay pebbles by volume",
        "Multiple shapes (round / square / rectangular) calculation",
        "For a frustum or cylinder, usable volume = base area × height minus the drainage layer (2cm of pebbles at the base) and the top headspace (1cm); potting soil weight = usable volume (cm³)×1.2 g/cm³÷1000, pebble weight = drainage volume×1.5÷1000; litres = volume÷1000.",
        "Cylindrical pot with inner diameter 20cm and inner height 18cm: base area π×10²=314.16cm², total volume 5654.9cm³; subtracting 628.3 for drainage and 314.2 for headspace gives usable 4712.4cm³ → about 5.65kg of potting soil, about 0.94kg of pebbles, volume 4.71L, corresponding to a 6-7 inch pot.",
        "Why lay pebbles at the bottom?",
        "The drainage layer prevents waterlogging and root rot, especially in pots without drainage holes or when overwatering; the top headspace prevents overflow when watering.",
        "How do I convert square and round pots?",
        "A square pot uses side²×height and a rectangular pot length×width×height, both likewise subtracting the drainage layer and top headspace; increase the drainage layer thickness for deep pots.",
        "About \"Pot Capacity Calculator\"",
        "Pot Capacity Calculator. A gardening planting tool for computing planting parameters and quantities.",
        "Pot capacity is estimated from the geometry: cylinder V=πr²h, frustum uses the top and bottom radii and height formula; the result is the volume that can be filled with soil.",
        "Estimate the soil volume and root space; deep pots suit deep-rooted plants while shallow pots suit shallow-rooted types such as succulents.",
        "Pot wall thickness and the drainage layer occupy real volume, so the result is for reference when buying and mixing soil.",
    ]))

    write('soil-ph', build('soil-ph', [
        "🧪 Soil pH Management",
        "Enter the soil test pH and the target plant to judge suitability and get adjustment advice and dosages",
        "📖 Read the \"Soil pH Suitability and Adjustment Usage Guide\"",
        "Soil test pH",
        "Target plant",
        "Hydrangea (blue flowers)",
        "Hosta",
        "Iris",
        "Succulent",
        "Cactus",
        "Radish",
        "Chinese cabbage",
        "Lettuce",
        "Chinese chives",
        "Scallion",
        "Blueberry",
        "Peach tree",
        "🧪 Analyse suitability",
        "📏 pH judgement standard:",
        "• Strongly acidic: pH < 5.0 ｜ acidic: 5.0-6.0 ｜ slightly acidic: 6.0-6.5 ｜ neutral: 6.5-7.0 ｜ slightly alkaline: 7.0-7.5 ｜ alkaline: >7.5",
        "• Most plants suit pH 5.5-7.0; a few acid-lovers (azalea, blueberry, gardenia) need 4.5-5.5",
        "• pH too low (<5.0): aluminium and manganese toxicity, phosphorus, calcium and magnesium deficiency",
        "• pH too high (>7.5): iron, manganese, phosphorus, boron and zinc get fixed, so the plant shows iron-deficiency chlorosis",
        "🌿 Suitable pH Table for Common Plants",
        "Suitable pH",
        "Preference",
        "⚗️ pH Adjustment Method Table",
        "Dosage (per m²)",
        "📚 In-Depth Analysis: Soil pH Suitability and Adjustment",
        "Judge plant suitability from soil test pH",
        "Dosage for acidifying or alkalinising",
        "Acidifying acid-loving plants (blueberry / azalea)",
        "Enter the soil pH and the target plant's suitable range [min,max]: inside the range it is \"fully suitable\"; below min it is too acidic and above max too alkaline, and the adjuster plus dosage follow from the difference (lowering 1 unit takes about 100-300 g/m² of lime powder, raising 1 unit about 100-200 g/m² of sulphur powder).",
        "Blueberry suits pH 4.5-5.5, measured 6.8 → 1.3 units too alkaline, so 100-200 g/m² of sulphur powder is recommended to lower pH (taking effect slowly over 2-3 months); tomato suits 6.0-7.0, measured 6.5 → fully suitable, no adjustment needed.",
        "What is the fastest way to acidify?",
        "Ferrous sulphate applied by root drench lowers pH by 0.3-0.5 and supplies iron (a good remedy for rose chlorosis), but is less durable than sulphur powder; for hydrangeas turned blue use aluminium sulphate.",
        "Is the pH test accurate?",
        "Test paper or a pen on a moist soil paste is enough, and a mixed sample from several points is more reliable; retest after 2-4 weeks following adjustment before top-dressing again.",
        "About \"Soil pH Management\"",
        "Soil pH Management. A gardening planting tool for computing planting parameters and quantities.",
    ]))

    write('watering-schedule', build('watering-schedule', [
        "✨ Watering Schedule Generator",
        "Generate a personalised watering schedule from plant, season and environment",
        "📖 Read the \"Personalised Watering Schedule Generator Usage Guide\"",
        "Areca palm",
        "Succulent (Crassulaceae)",
        "Golden barrel cactus",
        "Haworthia",
        "Kalanchoe",
        "🌸 Spring (Mar-May)",
        "☀️ Summer (Jun-Aug)",
        "🍂 Autumn (Sep-Nov)",
        "❄️ Winter (Dec-Feb)",
        "Environment",
        "🏠 Indoor",
        "🪟 Balcony",
        "🌳 Outdoor",
        "Pot diameter (cm, used to estimate water volume)",
        "📋 Copy schedule",
        "Calculation notes:",
        "• Base watering frequency is set by the plant's habit (drought tolerant / moisture loving)",
        "• Season factor: summer ×0.6 (more often), spring and autumn ×1.0, winter ×1.8 (less often)",
        "• Environment factor: indoor ×1.3 (slow evaporation), balcony ×1.0, outdoor ×0.8 (fast evaporation)",
        "• Water per watering ≈ pot diameter (cm) × factor × seasonal adjustment",
        "📊 Watering Reference Table for Common Plants",
        "Water preference",
        "Base frequency (days)",
        "Watering principle",
        "💾 Saved watering schedules",
        "📚 In-Depth Analysis: Personalised Watering Schedule Generator",
        "Produce a schedule from plant + season + environment",
        "Estimate water per watering and monthly usage",
        "Avoid over-drying and waterlogging",
        "Frequency (days)=max(1, round(base frequency×season factor×environment factor)); water per watering (ml)=round(pot diameter×base factor×season factor×environment factor×10); times per month=round(30/frequency), monthly water=per watering×times per month.",
        "Pothos, 20cm pot, summer balcony: frequency 5×0.6×1.0≈3 days, per watering 20×1.0×1.2×1.0×10=240ml, about 10 times per month, about 2400ml per month; in winter indoors the frequency is about 12 days and about 234ml per watering, a marked reduction.",
        "Can I follow the schedule as is?",
        "It is a starting reference and still needs fine-tuning according to soil moisture and weather; the chopstick method is the most reliable — insert and pull it out, and if no wet soil comes with it, water.",
        "How do you water succulents and cacti?",
        "For extremely drought-tolerant types the base frequency is 12-20 days with a low factor; water thoroughly only after drying out, and keep them dry in winter; waterlogging easily causes root rot.",
        "About \"Watering Schedule Generator\"",
        "Watering Schedule Generator. A gardening planting tool for computing planting parameters and quantities.",
    ]))


if __name__ == '__main__':
    main()