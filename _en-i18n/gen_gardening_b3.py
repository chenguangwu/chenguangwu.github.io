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
    write('garden-layout', build('garden-layout', [
        "📐 Garden Layout Planner",
        "Plan plant arrangement by area, style and light conditions, and output a recommended list with cost estimate",
        "📖 Read the \"Courtyard Plant Layout and Budget Planning Usage Guide\"",
        "Garden area (m²)",
        "Light conditions",
        "☀️ Full sun (6h+ direct light daily)",
        "⛅ Partial shade (3-6h light daily)",
        "🌑 Full shade (<3h light daily)",
        "Garden style",
        "📐 Generate the plan",
        "Plant counts are estimated by style density, and prices are common nursery price references (excluding earthworks, hard landscaping and labour). Reserve a 10-15% margin when actually planting.",
        "📐 Density Reference by Style",
        "Density (plants/m²)",
        "Suitable area",
        "📚 In-Depth Analysis: Courtyard Plant Layout and Budget Planning",
        "Selection for English border / Japanese zen styles",
        "Match plant density to area and light",
        "Estimate procurement and hard landscaping cost",
        "Total plants = area × style density (English 4.5 plants/m², Japanese 2.0 plants/m²); plant cost = Σ(round(total×cultivar share)×unit price); hard landscaping = area × base cost (English 60 yuan/m²).",
        "English border, full sun, 20m²: total 20×4.5=90 plants; rose18×35+hydrangea14×40+larkspur9×25+iris14×18+lavender18×22+daisy18×8 = 2207 yuan; hard landscaping 20×60=1200 yuan; total about 3407 yuan.",
        "Does it work on a small balcony too?",
        "Enter a smaller area to try it out; arrange containers in a \"tall - medium - low\" three-tier layout, and density can be slightly higher than in-ground planting to add layering.",
        "How do I cut the budget?",
        "Raise the share of self-propagated seedings or cuttings, choose perennial perennials (lavender, iris) to cut annual purchases, and use gravel in place of part of the paving for hard landscaping.",
        "About \"Garden Layout Planner\"",
        "Garden Layout Planner. A gardening planting tool for computing planting parameters and quantities.",
    ]))

    write('garden-tools', build('garden-tools', [
        "📚 Gardening Tools Quick Reference",
        "Learn the uses, selection points, technique and maintenance of all kinds of gardening tools",
        "📖 Read the \"Gardening Tool Selection and Maintenance Usage Guide\"",
        "⛏️ Soil",
        "✂️ Pruning",
        "💧 Watering",
        "🦺 Protection",
        "🌱 Planting",
        "📏 Measuring",
        "Covers 24 common gardening tools. When choosing, prioritise ergonomic design, material durability and after-sales support.",
        "📚 In-Depth Analysis: Gardening Tool Selection and Maintenance",
        "Beginner basic equipment checklist",
        "Choose spade / shears / rake by use",
        "Tool cleaning and rust prevention",
        "Select by category: spade (transplanting / loosening soil), pruning shears (pruning branches <2cm diameter), rake (levelling / raking leaves), watering can / spray bottle (watering); when choosing look at material (stainless steel / carbon steel) and handle ergonomics.",
        "Beginner three-piece set: small trowel (25-40 yuan) + pruning shears (40-80 yuan, SK5 steel is best) + spray bottle (15-30 yuan) for around a hundred yuan to start; add hedge shears (100 yuan class) and gloves for perennial care; wipe carbon steel dry and oil it after use to prevent rust, and sharpen once a year.",
        "How do I choose pruning shears?",
        "Bypass type gives a clean cut and suits live branches; anvil type suits dead branches. Over 2cm diameter, switch to branch cutters or a saw.",
        "What if my tools rust?",
        "Remove rust with fine sandpaper or steel wool and then oil, and drop lubricant on moving joints; for long-term storage disassemble, dry and hang them away from blade impacts.",
        "About \"Gardening Tools Quick Reference\"",
        "Gardening Tools Quick Reference. A gardening planting tool for computing planting parameters and quantities.",
        "Tool name / use keyword...",
    ]))

    write('garden-calendar', build('garden-calendar', [
        "🌷 Gardening Calendar",
        "A 12-month gardening work guide showing sowing / transplanting / pruning / fertilising / pest control / harvest essentials by climate zone",
        "📖 Read the \"12-Month Gardening Work Calendar Usage Guide\"",
        "❄️ Northern (North China / Northeast / Northwest)",
        "🌤️ Southern (South China / East China / Central China)",
        "📄 Export this month as TXT",
        "📑 Export the full year as TXT",
        "📋 Copy this month's content",
        "The northern reference is North China (annual average temperature around 12℃, frost period November to March); the southern reference is Jiangsu/Zhejiang or South China (annual average temperature around 18℃, short or no frost period). Fine-tune by local climate in practice.",
        "📚 In-Depth Analysis: 12-Month Gardening Work Calendar",
        "Arrange monthly work by climate zone",
        "Sowing and harvest planning for the home vegetable plot",
        "Pest and disease prevention timing reminders",
        "Give month-by-month sowing, transplanting, pruning, fertilising, pest control and harvest essentials by climate zone (temperate, subtropical, etc.); sowing dates for the same crop differ by about a month between north and south.",
        "Temperate vegetable garden: sow tomato and pepper seedlings in March and transplant in April; harvest June-August and watch for aphids; sow autumn spinach in September and harvest root crops in October; clear and prune the garden December-February. Subtropical regions are about 30 days earlier, and drainage during the plum rain season needs attention.",
        "How does a beginner follow the calendar?",
        "Use the local last frost and first frost dates as anchors and work backwards from the crop's growing period to schedule raising seedlings; keeping a planting log works better than rigidly following the calendar.",
        "How do I use it on a city balcony?",
        "Also follow the months, but container raising is more flexible; sow indoors early then transition through \"false planting\" to avoid late spring cold snaps.",
        "About \"Gardening Calendar\"",
        "Gardening Calendar is an online tool for the gardening and planting field. A gardening planting tool for computing planting parameters and quantities.",
    ]))

    write('balcony-sunlight', build('balcony-sunlight', [
        "/ Balcony Plant Sunlight Assessor",
        "📖 Read the \"Balcony Sunlight Duration Estimation Usage Guide\"",
        "📋 Balcony Plant Sunlight Assessor",
        "Which flowers suit your balcony? Enter the orientation, floor and season to estimate daily direct sunlight hours and get recommended suitable plants with care tips.",
        "Balcony orientation",
        "📚 In-Depth Analysis: Balcony Sunlight Duration Estimation",
        "Assess the difference in direct light between south- and north-facing balconies",
        "Judge the impact of high-rise versus low-floor obstruction",
        "Plan suitable plants by season",
        "Estimate daily direct sunlight hours by orientation (south/east/west/north), floor (low floors are more obstructed, high floors more open) and season: a high south-facing balcony gets about 6-8h in summer and 4-5h in winter; a north-facing one gets diffuse light all day with no direct sun.",
        "South-facing 6th floor in summer: estimated about 7h direct light daily → suits sun-loving plants such as roses, jasmine and tomatoes; under the same conditions winter is about 4.5h, so switch to short-day flowers such as kalanchoe and succulents; a north-facing balcony can only grow shade-tolerant plants such as ferns and hostas.",
        "What about a west-facing balcony?",
        "A west-facing balcony gets strong light and high temperature in the afternoon in summer, so choose sun-tolerant varieties (portulaca, cactus) or add shade netting to avoid scorching tender leafy vegetables.",
        "How do I compensate for insufficient light?",
        "Add a plant grow light (full spectrum LED, 12-16h daily), or switch to shade-tolerant varieties and reduce the proportion of flowering plants.",
        "Direct light: south 4-8h / east 3-5h / west 2.5-6h / north 0.5-2h (by season)",
        "Floor correction: low floor -1h, high floor +0.5h",
        "Full sun ≥6h, half sun 4-6h, diffuse light 2-4h, shade tolerant <2h",
        "Watch for shading on west-facing balconies in summer; results are a reference for choosing plants",
    ]))

    write('recommender', build('recommender', [
        "🌷 Watering Frequency Recommendation (by Season / Weather / Soil)",
        "By season / weather / soil",
        "📖 Read the \"Watering Frequency and Reminder Recommendation Usage Guide\"",
        "Watering interval adjusts by season, weather and soil type: in the growing season (spring and autumn) generally 2 to 5 days, 1 to 2 days in summer, 7 to 15 days in winter; water-retention corrections for soil are × 0.8 for porous peat mix, × 1.0 for garden soil, × 0.6 for sandy soil; delay 1 to 2 days on overcast or rainy days and bring forward 1 day in hot dry weather; the criterion is water when dry on the surface, watering thoroughly once the top 2-3 cm is dry, using water running out of the pot base as the sign of thorough watering.",
        "📚 In-Depth Analysis: Watering Frequency and Reminder Recommendation",
        "Generate reminders by plant habit",
        "Dynamic adjustment by season and environment",
        "Produce a copyable care reminder",
        "Adjusted days = plant base frequency × season factor × environment factor; moisture lovers (pothos / rose) are watered often, drought tolerant types (snake plant / succulent) rarely; the summer factor is 0.6 (frequent) and winter 1.8 (restricted).",
        "Pothos, 20cm pot, summer balcony: base 5 days×0.6×1.0≈every 3 days, about 240ml each time, about 10 times a month, about 2.4L of water per month; the same pot in winter indoors gives 5×1.8×1.3≈every 12 days and about 234ml each time, a clear reduction in frequency.",
        "Can I follow the frequency recommendation as is?",
        "It is only a starting point; you still need to feel the soil (insert a chopstick and pull it out — water if it is not damp). Ventilation, light and soil vary a lot, so fine-tune by actual conditions.",
        "Why does summer need more frequent watering?",
        "High temperature makes evaporation fast and the soil dry out easily, but avoid cold water at midday; watering in the morning and evening plus leaf misting is safer.",
        "About \"Watering Frequency Recommendation (by Season / Weather / Soil)\"",
        "Watering Frequency Recommendation (by Season / Weather / Soil). A gardening planting tool for computing planting parameters and quantities.",
    ]))

    write('index', build('index', [
        "🌿 Gardening and Planting Tools",
        "Gardening and planting",
        "Gardening and Planting Tools",
        "Enter the plant species, current season and growing environment (light, pot diameter, etc.) to generate a personalised watering frequency and per-watering volume plan, avoiding over-drying or waterlogging, for scientific care.",
        "Pot capacity calculator. Enter the pot top diameter, bottom diameter and height and estimate the soil-holding volume with the frustum formula, for potting mix quantities and repot pot selection, supporting multiple units.",
        "Compute the overall C:N ratio of a mix of several compost raw materials; the ideal range is 25-35:1 (best 30:1)",
        "Balcony Plant Sunlight Assessor",
        "The Balcony Plant Sunlight Assessor is a free online gardening and planting tool. Which flowers suit your balcony? Enter the orientation, floor and season to estimate daily direct sunlight hours and get recommended suitable plants with care tips. It runs purely on the front end, uploads no data, needs no registration, and works as soon as you open the browser.",
        "Enter the garden area, style (such as natural / formal) and light conditions to plan the plant arrangement and output a recommended cultivar list with estimated procurement cost, assisting home courtyard design and budgeting.",
        "Enter the soil test pH and target plant to judge acid-alkali suitability and get adjustment advice and dosages, suitable for garden soil improvement.",
        "View planting times by month, season and vegetable category, including sowing, transplanting, harvest, growing period and optimal temperature tips, assisting home vegetable garden planning.",
        "Watering frequency recommendation tool. Give watering frequency advice by plant season, weather and soil type and generate a copyable care reminder for daily water management in home gardening.",
        "A 12-month gardening work guide showing sowing / transplanting / pruning / fertilising / pest control / harvest essentials by climate zone",
        "Filter common gardening tools (spades, shears, rakes, etc.) by category or use and view their uses, selection points, technique and maintenance, as reference when beginners equip themselves.",
        "Look up common plant diseases and pests by plant or symptom, view the affected part, typical symptoms and recommended control methods, helping home growers identify and handle plant disease promptly.",
        "Look up the care essentials for common ornamental plants, including light, watering, fertilising, temperature, humidity and propagation, for everyday gardening management.",
        "About \"Gardening and Planting Tools\"",
        "Gardening and Planting Tools collects 12 free online tools covering the common calculation, conversion and lookup needs of gardening and planting scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you can find practical small tools here that are ready to use the moment you open them. All tools run purely on the front end and data is not uploaded to the server, protecting privacy.",
        "The gardening and planting tools collected on this page include (some representative tools):",
        "These tools help you quickly complete common gardening and planting tasks without memorising complex formulas or doing manual conversions — just enter and the result appears.",
        "Do the Gardening and Planting Tools need a download or registration?",
        "No. All gardening and planting tools on this page are purely front-end online tools; open the page and use them directly, with no software to install, no account to register and no data uploaded.",
        "Are the Gardening and Planting Tools results accurate, and is the data secure?",
        "The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are available immediately. All computation runs locally on your device, the data is never uploaded to the server, and privacy is well protected.",
    ]))


if __name__ == '__main__':
    main()