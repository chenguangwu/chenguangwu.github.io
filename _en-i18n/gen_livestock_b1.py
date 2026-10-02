#!/usr/bin/env python3
# gen_livestock_head.py — shared head for livestock batches b1..b6
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'livestock')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'livestock')
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
    out = {'slug': slug, 'industry': 'livestock', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('ammonia-ventilation', build('ammonia-ventilation', [
        "Ammonia concentration and ventilation demand calculator",
        "Assess the ammonia concentration level in a livestock house and calculate the minimum ventilation needed to reach a safe level.",
        "Core formula (by inputs): volume \u00d7 Math.log(c1 \u00f7 c2) \u00f7 (t \u00d7 eta); (gen \u00d7 1000) \u00f7 targetMgPerM3 \u00f7 eta; totalQ \u00f7 3600",
        'View "Ammonia concentration and ventilation demand calculator" guide',
        "Indoor ammonia concentration (ppm)",
        "Target safe concentration (ppm)",
        "Barn length (m)",
        "Barn width (m)",
        "Barn height (m)",
        "Ventilation efficiency factor",
        "0.7 (good)",
        "0.6 (average)",
        "0.5 (poor)",
        "Hourly ammonia generation (g/h, optional)",
        "Ammonia concentration reference standard",
        "Meets livestock house hygiene requirements",
        "Affects long-term production performance",
        "Irritates airways, lowers immunity",
        "Seriously harms health, ventilate immediately",
        "Ventilation is based on the dilution model: Q = V \u00d7 ln(C1/C2) / (t \u00d7 \u03b7). Real ventilation also depends on temperature, humidity and animal density; install ammonia sensors for live monitoring.",
        "Deep dive: Barn ammonia ventilation",
        "Derive required ventilation from the target ammonia concentration.",
        "Ammonia control design for closed poultry and pig houses.",
        "Evaluate whether existing ventilation meets the standard.",
        "Poultry house 40\u219215 ppm",
        "Volume 1800 m\u00b3 (50\u00d712\u00d73), \u03b7=0.6: Q=V\u00b7ln(c1/c2)/(t\u00b7\u03b7)=1800\u00d7ln(40/15)/0.6\u22482943 m\u00b3/s, about 98 air changes per minute.",
        "Stricter target",
        "Lower c2 from 15 to 10 ppm: Q rises to about 110 changes per minute.",
        "What is \u03b7?",
        "Dilution efficiency (0\u20131); mixing is uneven in practice, use 0.5\u20130.7.",
        "What are the ammonia limits?",
        "Poultry houses: \u226425 ppm recommended; human irritation warns at about 25\u201340 ppm.",
        'About "Ammonia concentration and ventilation demand calculator"',
        "Ammonia concentration and ventilation demand calculator. " + DISCL,
    ]))
    write('analysis-18', build('analysis-18', [
        "Layer hen analysis (lay rate / feed-egg ratio)",
        "Lay rate / feed-egg ratio",
        "From flock size, eggs laid and total egg weight over the period, plus feed consumed, compute hen-day lay rate, per-bird daily feed and feed-egg ratio, and convert to egg count by standard weight. Data is processed only locally in your browser and never uploaded.",
        'View "Layer hen analysis (lay rate / feed-egg ratio)" guide',
        "Lay rate = total eggs \u00f7 (hens \u00d7 days) \u00d7 100%",
        "Feed-egg ratio = total feed \u00f7 total egg weight",
        "From flock size and eggs, total egg weight and feed over the period, compute hen-day lay rate, per-bird daily feed and feed-egg ratio, and convert to egg count by standard weight. All data is processed only locally in your browser, not uploaded.",
        "Number of hens (birds)",
        "Number of days (days)",
        "Total eggs (count)",
        "Average egg weight (g/egg)",
        "Total feed (kg)",
        "Deep dive: Layer hen lay rate and feed-egg ratio",
        "Summarize weekly or monthly egg count, average weight and feed to compute hen-day lay rate.",
        "Use feed-egg ratio and per-bird daily feed to monitor feed efficiency and detect waste or underfeeding.",
        "Compare performance across houses, batches or age groups to guide ration tweaks and timely culling.",
        "Production accounting for 10,000 hens over a week",
        "10,000 hens, 63,000 eggs and 8,400 kg feed in 7 days, average egg 58 g. Hen-days = 10,000\u00d77 = 70,000, lay rate = 63,000\u00f770,000 = 90.00%; total egg weight = 63,000\u00d758\u00f71000 = 3,654 kg, feed-egg ratio = 8,400\u00f73,654 = 2.30, within the peak-range norm.",
        "Locating efficiency decline",
        "Lay rate stays 90% but feed-egg ratio rises from 2.15 to 2.40. First check the feed side (spillage, trough adjustment, rodents), then whether average egg weight dropped and shrank total weight; when lay rate is flat but the ratio rises, feed use is usually overstated.",
        "Cross-checking per-bird daily feed",
        "Per-bird daily feed 117.5 g/bird\u00b7day and daily egg weight 52.8 g give a ratio of about 2.23, matching the flock feed-egg ratio, so the entered weights are self-consistent; a clear mismatch usually means the average egg weight was a sample value rather than the whole-flock weigh.",
        "Why use hen-days for lay rate?",
        "Hen-day lay rate uses hens \u00d7 days as the denominator, reflecting both mortality and production drops, closer to reality than eggs\u00f7hens; the difference is especially clear across months.",
        "What is a reasonable feed-egg ratio?",
        "Commercial layers at peak are usually 2.0\u20132.4; above 2.5 check feed waste, egg-weight drop or flock health. The ratio rises naturally with age; judge against the same-age standard curve, not the absolute value.",
        "How should average egg weight be taken?",
        "Weigh 30\u201350 eggs daily or weigh the whole flock and average; a fixed value (e.g., 58 g) is fine short-term, but egg-weight changes amplify ratio swings, so measure weekly when comparing across weeks.",
        'About "Layer hen analysis (lay rate / feed-egg ratio)"',
        "Layer hen analysis (lay rate / feed-egg ratio). " + DISCL,
    ]))
    write('animal-welfare-score', build('animal-welfare-score', [
        "Animal Welfare Scorer",
        "Score farm-animal welfare across dimensions based on the Five Freedoms (simplified Welfare Quality)",
        'View "Animal Welfare Scorer" guide',
        "Food and nutrition",
        "Feed adequacy (no hunger)",
        "Water adequacy (no thirst)",
        "Environment and housing",
        "Comfortable resting area",
        "Temperature and thermal comfort",
        "Adequate space",
        "Health and medical care",
        "Free of disease and injury",
        "Timely medical treatment",
        "Behavior and psychology",
        "Freedom to express normal behavior",
        "Free of fear and stress",
        "Compute total score",
        "Total grade",
        "\u2022 85\u2013100 points:",
        "High animal welfare",
        "\u2022 70\u201384 points:",
        "Basically meets welfare requirements",
        "\u2022 55\u201369 points:",
        "Room for improvement",
        "\u2022 0\u201354 points:",
        "Needs immediate improvement",
        "The Five Freedoms: 1. from hunger and thirst; 2. from discomfort; 3. from pain/injury; 4. to express normal behavior; 5. from fear and stress. Scoring needs real observation plus quantitative indicators.",
        "Deep dive: Animal welfare scoring",
        "Weighted multi-dimensional welfare composite (100-point scale).",
        "Farm welfare audit and benchmarking.",
        "Locate and improve weak dimensions.",
        "5-dimension scores [9,8,7,8,9]",
        "Weights [0.25,0.2,0.2,0.2,0.15]: weighted = 8.7, composite = 87 (excellent).",
        "One dimension low",
        "One dimension drops from 7 to 4: composite falls to about 81, flagging that dimension as the weak point.",
        "What is the score range?",
        "Each dimension 0\u201310, composite scaled to 0\u2013100; \u226585 excellent, 70\u201385 good.",
        "How are weights set?",
        "Set dimension weights by a standard (e.g., Welfare Quality); adjustable.",
        'About "Animal Welfare Scorer"',
        "The Animal Welfare Scorer is a general-purpose online tool. " + DISCL,
    ]))
    write('breeding-timing', build('breeding-timing', [
        "Breeding animal optimal mating-time estimator",
        "From estrus onset time and animal type, estimate the optimal breeding/AI time window",
        'View "Breeding animal optimal mating-time estimator" guide',
        "Dairy/cattle",
        "Sow",
        "Sheep",
        "Goat",
        "Estrus onset time",
        "Artificial insemination",
        "Natural mating",
        "Breeding timing reference",
        "Estrus and breeding reference by animal",
        "Cattle",
        ": estrus lasts 12\u201318 h, ovulation 10\u201312 h after estrus ends. Best breeding: 8\u201316 h after estrus (or 'morning estrus breed in the afternoon, afternoon estrus breed next morning')",
        "Pig",
        ": estrus lasts 40\u201360 h, ovulation 36\u201342 h after onset. Best breeding: 20\u201330 h after onset, advise two breedings 12 h apart",
        ": estrus lasts 24\u201336 h, ovulation at estrus end. Best breeding: 18\u201324 h after onset",
        ": estrus lasts 24\u201348 h, ovulation 30\u201336 h after onset. Best breeding: 20\u201330 h after onset",
        ": estrus lasts 5\u20137 days, ovulation 24\u201348 h before estrus ends. Best breeding: every-other-day until ovulation",
        "Accurate estrus-onset detection is vital. Combine behavior (standing reflex, appetite drop), mucus changes and ultrasound. AI is usually 2\u20134 h later than natural mating.",
        "Deep dive: Breeding timing and due-date estimation",
        "Estimate the optimal breeding window from estrus onset.",
        "AI or natural-mating insemination-time advice.",
        "Back-calculate from gestation",
        "Expected calving/farrowing date",
        "Dairy cow AI",
        "Estrus onset 2026-01-01, optimal window +18\u2013+24 h (AI +2 h) \u2192 inseminated Jan 2; gestation 283 days \u2192 due 2026-10-11.",
        "Optimal breeding +12\u2013+36 h after onset, gestation 114 days to estimate due date.",
        "Why a window?",
        "Ovulation is mostly in a specific post-estrus window; AI must be near ovulation to raise conception.",
        "Gestation differences?",
        "Cattle ~283, pig ~114, sheep ~150 days; by species.",
        'About "Breeding animal optimal mating-time estimator"',
        "Breeding animal optimal mating-time estimator. " + DISCL,
    ]))
    write('calc-58', build('calc-58', [
        "Pedigree inbreeding coefficient calculator",
        "Enter a pedigree (one individual per line: individual, sire, dam; leave unknown parents blank); automatically compute each individual's inbreeding coefficient F and the additive genetic relationship matrix (A matrix).",
        'View "Pedigree inbreeding coefficient calculator" guide',
        "Pedigree data (each line: name, sire, dam)",
        "Example: S, A, D are founders; B=S\u00d7A, C=S\u00d7D; X=B\u00d7C (half-sib mating, expected F\u224812.5%). Parents must appear before their offspring.",
        "Load example",
        "Wright's formula: Fx = \u03a3 (1/2)^(n1+n2+1) \u00d7 (1+Fa); n1, n2 are the generations from sire and dam to the common ancestor, Fa is that ancestor's own inbreeding. Tabular method: Fi = \u00bd \u00d7 A(sire_i, dam_i).",
        "Additive genetic relationship matrix (A matrix)",
        "Names are case-sensitive and must be unique; separate fields on a line with a half-width comma",
        "Parents must appear before offspring, otherwise treated as unknown (founder)",
        "Inbreeding reference: F<6.25% acceptable, 6.25%\u201312.5% caution, >12.5% high inbreeding-depression risk",
        "Deep dive: Pedigree inbreeding coefficient",
        "From sire/dam, compute individual F via the tabular or path method.",
        "Breeding planning to avoid inbreeding depression.",
        "Output the relationship matrix and F rating.",
        "Sire mated to his daughter",
        "Sire is also the dam's father: offspring F=0.25 (25%), severe inbreeding.",
        "Half-sib mating",
        "Share one grandparent: F=0.125 (12.5%), moderate inbreeding.",
        "What does F mean?",
        "F is the probability of homozygosity; higher F means greater inbreeding-depression risk.",
        "What thresholds?",
        "Generally F<6.25% (half-uncle-niece level) is acceptable; \u226512.5% needs caution.",
        'About "Pedigree inbreeding coefficient calculator"',
        "For livestock pedigree analysis. Enter individuals and their parents; compute each individual's inbreeding coefficient by Henderson's tabular method (equivalent to Wright's path formula) and output the full additive relationship matrix (A matrix) for mating and kinship analysis.",
        "Wright inbreeding coefficient + A matrix",
        "Automatic topological sort and cycle detection",
        "Inbreeding-risk rating",
        "Sire mating inbreeding-risk assessment",
        "Conservation-herd kinship analysis",
        "Data prep for breeding-value estimation",
        "Teaching demonstration of pedigree calculation",
        "Pedigree data",
    ]))

if __name__ == "__main__":
    main()
