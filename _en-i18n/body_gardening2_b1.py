#!/usr/bin/env python3
from head_gardening2 import build, write


def main():
    write('fertilizer-ppm', build('fertilizer-ppm', [
        '🧮 Liquid Fertilizer Dilution ppm Calculator',
        'Computes the required liquid fertilizer dose from the target ppm concentration and the water volume',
        '/ Liquid Fertilizer Dilution',
        '📖 View the guide to the liquid fertilizer dilution ppm calculator',
        'ppm means mg/L: required fertilizer (mg) = target concentration (ppm) × water volume (L); if the active ingredient ratio is P%, the amount to weigh = target concentration × water volume ÷ (P% ÷ 100); the diluted concentration = fertilizer amount (mg) × ingredient ratio ÷ water volume (L); hydroponics commonly uses 800 to 1500 ppm (growth stage) and 1500 to 2000 ppm (fruiting stage), and the EC value ≈ ppm ÷ 700 (mS/cm) can be used to cross-check whether the concentration is right.',
        '💡 ppm = mg/L (milligrams per liter). 1 ppm is one part per million. Calculation formula: dose (g) = target ppm × water volume (L) ÷ nutrient content (%) ÷ 10000.',
        '📚 In-depth: liquid fertilizer dilution ppm calculator',
        'Dose mode: given the target concentration (ppm), water volume (L) and fertilizer nutrient content (%), the fertilizer dose (g) = target ppm × water volume ÷ (nutrient content ÷ 100) ÷ 1000000 × 1000; the tool shows the result in g and ml as equal amounts (dilute liquid fertilizer is approximated to the density of water).',
        'Reverse concentration mode: given the actual fertilizer dose (g), water volume and nutrient content, the concentration in ppm = dose × (nutrient content ÷ 100) × 1000000 ÷ water volume ÷ 1000, used to check whether a prepared nutrient solution is over or under strength.',
        'Supporting conversions: dilution ratio = water volume (L) × 1000 ÷ dose (g) (how many parts water per part fertilizer), approximate drop count = dose (ml) ÷ 0.05 (estimated at 0.05 ml per drop), handy for dosing by drops when no measuring tool is at hand; all three are shown alongside the main result and can be screenshotted and kept as a mixing card.',
        'Worked example: target 200 ppm, 1 L of water, nutrient content 20%',
        'Dose: 200 × 1 ÷ 0.2 ÷ 1000000 × 1000 = 1 g (equal to 1 ml); dilution ratio = 1 × 1000 ÷ 1 = 1000x; approximate drops = 1 ÷ 0.05 = 20 drops. Changing water volume and concentration: 150 ppm / 10 L / 20% → 7.5 g, 1333x, 150 drops; 100 ppm / 20 L / 15% → 13.333 g, 1500x, 267 drops. Reverse check: dose 1 g / 1 L / 20% → 200 ppm; 7.5 g / 10 L / 20% → 150 ppm, consistent with the forward results.',
        'What exactly does ppm mean, and why does 1 L of water at 200 ppm need only 1 g of fertilizer?',
        'In water, ppm equals mg/L: 1 ppm means 1 mg of active nutrient per liter. For 1 L at 200 ppm you need 200 mg of active nutrient; if the fertilizer contains 20% of that element, you need 200 ÷ 0.2 = 1000 mg = 1 g of fertilizer. So a larger target concentration × water volume means a larger dose, while a higher nutrient content means a smaller dose — respectively proportional and inversely proportional.',
        'What number should go in the nutrient content field?',
        'Enter the content of the corresponding element or oxide printed on the fertilizer label (nitrogen N, or P₂O₅, K₂O',
        '), not the sum of the three nutrients. For example, with a balanced 20-20-20 fertilizer, enter 20 if calculating by nitrogen; if the formula is converted on a P₂O₅ basis, enter the corresponding P₂O₅ percentage. Entering it wrong makes the dose a fraction of or a multiple of what is actually needed, so check the label before mixing.',
        'About liquid fertilizer dilution',
    ]))

    write('lawn-height', build('lawn-height', [
        '📏 Lawn Mowing Height Guide',
        'Pick a grass species and season to see the recommended mowing height and frequency',
        '/ Lawn Mowing Height',
        '📖 View the guide to the lawn mowing height guide',
        'Stubble height is recommended by species and season: Kentucky bluegrass 5 to 8 cm (up to 8 cm in summer), bermudagrass 2 to 4 cm, zoysiagrass 2.5 to 5 cm, tall fescue 6 to 9 cm; follow the one-third rule (never remove more than one third of the grass height at once); mowing frequency = grass growth ÷ amount removed per cut, every 5 to 7 days in the peak season and every 2 to 4 weeks in dormancy; the mower blade height is the target stubble height.',
        '🌸 Spring',
        '☀️ Summer',
        '🍂 Autumn',
        '❄️ Winter',
        '📚 In-depth: lawn mowing height guide',
        'Recommended heights by species and season: 8 turfgrasses split into warm-season and cool-season types, each with a recommended stubble height and mowing interval per season. Warm-season — bermudagrass spring 2.5 / summer 3 / autumn 2.5 / winter 2 cm (max 5, interval 4-6 days in summer), zoysiagrass (Manila) 3 / 3.5 / 3 / 2.5 (max 5.5), seashore paspalum 2 / 2.5 / 2 / 1.5 (max 4), centipedegrass 3 / 3.5 / 3 / 2.5 (max 5.5).',
        'Cool-season and fine turf: Kentucky bluegrass and ryegrass 4 / 5 / 4 / 3 cm (max 7, interval 5-10 days), tall fescue 5 / 6 / 5 / 4 (max 8), bentgrass 1.5 / 2 / 1.5 / 1 (max 3, interval 3-5 days, for golf-green-grade fine turf). In winter every species is marked as stop mowing.',
        'The 1/3 rule and seasonal notes: never cut more than 1/3 of the leaf height at once; the page gives seasonal notes by grass type — warm-season grasses grow vigorously in summer and need frequent cutting, and stop being cut during winter dormancy; cool-season grasses are semi-dormant in summer and should be left slightly taller to reduce stress; height should be lowered a little during spring green-up to encourage tillering, and lowered before winter to prevent disease.',
        'Worked example: share of the recommended height within the maximum height (',
        'progress bar',
        'The page draws the progress bar as recommended height ÷ maximum height × 100%. Summer values: bermudagrass 3 ÷ 5 = 60.0%, zoysiagrass 3.5 ÷ 5.5 = 63.6%, Kentucky bluegrass and ryegrass 5 ÷ 7 = 71.4%, tall fescue 6 ÷ 8 = 75.0%, bentgrass 2 ÷ 3 = 66.7%, seashore paspalum 2.5 ÷ 4 = 62.5%. Spring comparison: bermudagrass 2.5 ÷ 5 = 50.0%, tall fescue 5 ÷ 8 = 62.5%. A lower share means the stubble is closer to that species’ lower limit and needs more frequent mowing; at or near 100% the species’ tolerance limit has been reached and it must be mowed immediately.',
        'Why follow the rule of cutting only 1/3 at a time?',
        'Removing more than 1/3 of the leaf height at once costs a large amount of photosynthetic area, forcing the plant to draw on root reserves to recover, suppressing root growth and inviting bare patches and weeds. The correct approach is little and often: mow at the intervals in the table (warm-season 4-7 days in summer, cool-season 5-10 days, bentgrass 3-5 days), removing only 1/3 each time. If the lawn has already grown too tall through delay, lower it to the target in 2-3 steps, 2-3 days apart.',
        'Why is winter marked as stop mowing?',
        'All species are marked as stop mowing in winter, when the lawn is dormant or barely growing; mowing then stimulates leggy growth, consumes stored reserves and raises the risk of freezing injury and disease. The last cut before winter can be slightly below the usual recommended height (for example 2 cm for bermudagrass, 3 cm for Kentucky bluegrass) to reduce snow mold and thatch buildup, helping overwintering and green-up next year.',
        'About lawn mowing height',
    ]))

    write('pest-control', build('pest-control', [
        '💊 Pest and Disease Spraying Interval Reference',
        'Interval and pre-harvest safety period reference for common pests and diseases — apply chemicals properly to avoid crop damage',
        '/ Spraying Interval',
        '📖 View the guide to the pest and disease spraying interval reference',
        'Intervals and pre-harvest safety periods by product type: protectant fungicides every 7 to 10 days, systemic ones every 10 to 14 days; the safety interval for insecticides is commonly 3 to 7 days (leafy vegetables) and 7 to 14 days (fruit vegetables); never use the same product more than 2 to 3 times in a row, to prevent resistance, and rotate products with different modes of action; the safety interval must have passed before harvest to keep residues compliant; mixing dilution ratio = product dose ÷ water volume, as stated on the label.',
        '📚 In-depth: pest and disease spraying interval reference',
        'Pest entries and key points: aphids (imidacloprid / acetamiprid, 7-10 day interval, max 3 times per season, 7 day safety period, spray evenly on both leaf surfaces and focus on the insects); spider mites (abamectin / spirodiclofen, 5-7 days, 3 times, 14 days, needs 2 or more consecutive treatments, alternate ovicides and miticides); whitefly (thiamethoxam / bifenthrin, 7-10 days, 3 times, 7 days, apply in the morning or evening and combine with yellow sticky traps); snails and slugs (metaldehyde, 7 days, 2 times, 7 days, spread around the base of the plants in the evening).',
        'Disease entries and key points: powdery mildew (triadimefon / difenoconazole, 7-10 days, 3 times, 14 days, treat at the first sign of disease, alternate systemic and protectant products); black spot (mancozeb / carbendazim, 7-10 days, 4 times, 14 days, focus on prevention and start spraying before the rainy season); gray mold (pyrimethanil / procymidone, 7 days, 3 times, 14 days, improve ventilation and reduce humidity, remove diseased leaves and flowers promptly); rust (triadimefon / tebuconazole, 10-14 days, 3 times, 14 days); anthracnose (prochloraz / difenoconazole, 7-10 days, 3 times, 14 days); root rot (hymexazol / thiophanate-methyl, 10 days, 2 times, 21 days).',
        'Resistance and safety management: entries with a long interval, many applications and a long',
        'safety period',
        'are flagged yellow or orange as warnings (scale insects: buprofezin / chlorpyrifos 10-14 days, 2 times, 21 days; ants and soil pests: phoxim / chlorpyrifos 14 days, 2 times, 21 days). Continuous use of products with the same mode of action easily selects resistant populations; once the seasonal application cap is reached, switch to a product with a different mode of action, and the pre-harvest safety period must be met before harvesting.',
        'How to use it: reading the 12 reference cards in three steps',
        'The page lists 12 pest and disease references; each card is arranged as recommended product → spraying interval → maximum applications per season → pre-harvest safety period, and colored by safety level: short safety interval (green, e.g. aphids 7 days), observe the interval (yellow, e.g. spider mites / powdery mildew 14 days), longer interval (orange, e.g. scale insects / root rot 21 days). In practice, first use the interval and count to build a spraying calendar, then work backwards from the pre-harvest period to fix the last spray date, and finally follow the tips at the bottom of the card (for example spider mites: needs 2 or more consecutive treatments, alternate ovicides and miticides; black spot: focus on prevention, start spraying before the rainy season).',
        'How should the pre-harvest safety period be applied, and what if the pest is not fully controlled?',
        'The pre-harvest safety period is the number of days that must pass between the last application and harvest (7 days for aphid products, 21 days for scale insect and root rot products, and so on). Even if the pest is not fully under control, you must wait out the interval before harvesting, and wash the produce thoroughly afterwards; if pest pressure remains close to harvest, switch to physical or biological control (yellow sticky traps, insect netting, predatory mites, manual removal) rather than shortening the safety interval.',
        'Why limit the maximum number of applications per season?',
        'Continuous use of products with the same mode of action selects resistant populations and leaves no effective product later, which is the point of the 2-4 times per season cap in the table. Once the cap is reached, rotate to a product with a different mode of action (for example alternating ovicides and miticides for spider mites), or switch to cultural measures such as garden cleanup, pruning diseased leaves, ventilation and humidity reduction; also spray strictly at the recommended interval, since shortening it does not improve efficacy — it only accelerates resistance and raises residue risk.',
        'About pest and disease spraying intervals',
    ]))

    write('pruning-time', build('pruning-time', [
        '⚖️ Plant Pruning Timing Reference',
        'Filter by pruning timing to see the best pruning period and key points for each plant',
        '/ Pruning Timing',
        '📖 View the guide to the plant pruning timing reference',
        'Pruning timing is classified by flowering habit: early-spring flowering plants (winter jasmine, forsythia, plum blossom) are pruned right after flowering, otherwise next year’s flower buds are cut off; summer and autumn flowering plants (rose, crape myrtle, hydrangea) are cut back hard at the end of dormancy (late winter to early spring) to push new growth; foliage and evergreen plants are shaped before spring bud break; pines and cypresses are pinched during the growing season; the principle is that pruning after flowering preserves flowers while dormant pruning builds form.',
        'Before flowering',
        'After flowering',
        'Dormant season',
        '📚 In-depth: plant pruning timing reference',
        'Timing by flowering habit: species that bloom on old wood (bigleaf hydrangea, azalea and so on) must be pruned after flowering and mostly before August, otherwise the next year’s buds formed after autumn are removed and there will be no flowers; species that bloom on new wood (panicle hydrangea, oakleaf hydrangea) flower on the current year’s new growth, so hard dormant pruning does not affect flowering.',
        'Hard dormant pruning: crape myrtle, pomegranate, grape, apple/pear, peach and others are cut back on one-year-old shoots after leaf fall until bud break in early spring, to push new growth and make shaping and thinning easier; with no leaves the branch structure is visible and wounds heal fast. The tool includes 6 species in this group.',
        'Light pruning after flowering and taboos: for roses, removing spent blooms after each flush encourages a second flowering, with a harder cut back to 3-5 buds in winter; for magnolia, only remove diseased and crossing branches after flowering and avoid heavy pruning (wounds heal slowly); osmanthus and jasmine are types that are not pruned before flowering — shape them in spring instead and remove interior branches.',
        'How to use it: 18 plants filtered into three pruning-timing groups',
        'The page covers 18 common flowering trees and shrubs in three timing groups: after flowering 10 species (rose, hydrangea blooming on old wood, magnolia, winter jasmine, plum blossom, camellia, azalea, crabapple, climbing rose, gardenia), dormant season 6 species (crape myrtle, hydrangea blooming on new wood, pomegranate, grape, apple/pear, peach), before flowering 2 species (osmanthus, jasmine). Click the tabs at the top (All / Before flowering / After flowering / Dormant) to filter by group; each card gives the specific pruning window and operating points for that plant (for example rose: lightly remove spent blooms after each flush, cut back hard to 3-5 buds in winter dormancy; bigleaf hydrangea: finish pruning before August, after which buds form and no pruning is allowed from autumn to the following spring).',
        'Why distinguish hydrangeas that bloom on old wood from those that bloom on new wood?',
        'Bigleaf hydrangea forms flower buds on old wood grown the previous year; pruning from autumn to the following spring cuts the buds off directly and there will be no flowers that year, so pruning must be finished after flowering and before August. Panicle and oakleaf hydrangea bloom on new growth, so hard pruning in early spring does not affect flowering that year and can even renew the shape. Confirming which type a cultivar belongs to before buying or caring for it is the first step in deciding the pruning time.',
        'What period exactly does dormant pruning refer to?',
        'It refers to the time after leaf fall until bud break in early spring (roughly January to March, earlier in the south). Sap flow is slow then, wounds heal easily, and with no leaves the direction of branches is easy to judge, which also helps remove diseased, pest-infested and crossing branches. Note that pruning in severe cold can freeze the cut ends, so finish before temperatures rise; evergreens and species that bleed heavily (such as grape) should especially avoid the bleeding period around bud break.',
        'About the pruning timing reference',
    ]))

    write('watering-frequency', build('watering-frequency', [
        '🌷 Watering Frequency Recommender',
        'Recommends watering frequency and volume from season, weather, potting mix and plant type',
        '/ Watering Frequency',
        '📖 View the guide to the watering frequency recommender',
        '📚 In-depth: watering frequency recommender',
        'Interval model: interval days = season base × weather factor × soil factor × plant factor × location factor, rounded and clamped to 1 to 30 days. Season base: spring 3, summer 2, autumn 4, winter 7; weather: sunny 0.8 / cloudy 1.2 / rainy 2.0 / hot 0.5 / dry 0.7; soil: sandy 0.7 / loam 1.0 / clay 1.4; plant: foliage 1.0 / flowering 0.9 / succulent 2.5 / cactus 4.0 / herbaceous 0.8; location: indoor 1.3 / balcony 1.0 / outdoor 0.8.',
        'Volume and frequency labels: water per session = pot diameter (cm)² × 0.8 (ml), monthly use = single volume × 30 ÷ interval days ÷ 1000 (L); labels by interval — 2 days or less needs frequent watering, 3-4 days normal watering, 5-7 days moderate watering, more than 7 days water sparingly.',
        'Seasonality and double-checking: summer heat and outdoor conditions shorten the interval markedly while winter lengthens it, and the tool gives seasonal notes (green-up in spring, high temperature in summer, vigorous growth in autumn, restricted watering in winter); results should be checked against how dry the surface soil is and the drainage from the pot bottom, rather than applied mechanically by the day.',
        'Worked example: spring / sunny / sandy / foliage / indoor / 15 cm pot',
        'Multiplying through: 3 × 0.8 × 0.7 × 1.0 × 1.3 = 2.184 → rounded to 2 days; water per session = 15² × 0.8 = 180 ml; monthly use = 180 × 30 ÷ 2 ÷ 1000 = 2.7 L; label needs frequent watering. Comparison of a few typical combinations: summer / hot / sandy / cactus / outdoor / 15 → 2 × 0.5 × 0.7 × 4.0 × 0.8 = 2.24 → 2 days; summer / hot / sandy / succulent / outdoor / 20 → 1.4 → 1 day, 320 ml per session, 9.6 L per month; winter / rainy / clay / cactus / indoor → 101.92 → capped at 30 days, 0.2 L per month, label water sparingly; autumn / cloudy / loam / flowering / balcony / 30 → 4.32 → 4 days, 720 ml per session, 5.4 L per month, label normal watering.',
        'Is multiplying five factors too crude — can I just water by the number of days given?',
        'The factor model is a starting baseline for beginners, meant to build a rhythm of how often to check, not to be followed mechanically. In practice judge by the top 2-3 cm of soil drying out, the pot feeling noticeably lighter, or a bamboo skewer coming out without a wet mark, and when you water, water thoroughly until it drains from the bottom holes. The value of this tool is giving directional adjustment with season and weather (shorter in summer, longer in winter, longer for clay, shorter for sandy soil).',
        'Why is the volume per session based on the square of the pot diameter, and is it reliable?',
        'The tool estimates it empirically as pot diameter (cm)² × 0.8 ml (a 15 cm pot → 180 ml), which approximates the pot as a short cylinder and ignores pot height, the water-holding capacity of the medium and plant size. In practice, water until it drains from the bottom holes; the per-session and monthly figures are better used for planning water use and reminders than as precise measurement.',
        'About watering frequency',
    ]))


if __name__ == '__main__':
    main()
