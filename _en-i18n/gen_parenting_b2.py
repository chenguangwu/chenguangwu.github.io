#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'parenting')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'parenting')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'parenting', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- formula-mixing (23) ----------------
    write('formula-mixing', build('formula-mixing', [
        "/ Formula Mixing Calculator",
        "📖 Read the \"formula-mixing User Guide\"",
        "🏋️ Formula Mixing Calculator",
        "Do not mix formula by feel: enter the target milk volume and the can's mixing ratio (water per scoop) and the tool computes the number of scoops and the water needed, avoiding over-concentrated or over-diluted formula.",
        "Mixing calculation: scoops needed = target milk volume / water per scoop; water needed = scoops x water per scoop; convert with the ratio printed on the can (for example 30 mL of water per scoop). A powder-to-water ratio that drifts off makes the formula too strong (high kidney load) or too weak (nutrient deficiency), so always add water first, then powder, and shake well.",
        "Target milk volume (ml)",
        "Mixing ratio (ml/scoop)",
        "Water first, then powder",
        "Yes (recommended)",
        "📚 Deep dive: Formula Mixing Ratios",
        "Everyday bottle mixing: given the target feed volume (such as 180 ml) and the ratio printed on the can (usually 30 ml/scoop), quickly work out how many level scoops of powder and how much water to add.",
        "Switching brands: scoop sizes differ by brand (commonly 30 ml/scoop, some 60 ml/scoop), so convert by the ratio to avoid over-concentration (kidney load) or over-dilution (nutrient deficiency).",
        "Travel and portability: work backwards from \"target volume / ratio\" to know how many scoops to bring, and carry pre-portioned warm water in a thermos to mix on site for hygiene.",
        "Target 180 ml, ratio 30 ml/scoop",
        "Scoops = round(180/30) = 6 scoops; water = 6 x 30 = 180 ml (add warm water first); total volume after mixing = 180 + round(6 x 4.3) = 180+26 = 206 ml (each scoop of powder is about 4.3 g, so the volume grows slightly once dissolved). That is 6 level scoops of powder plus 180 ml of warm water.",
        "Water first or powder first?",
        "Always add water to the mark first and then add level scoops of powder; this avoids exceeding the final volume and ending up too concentrated. Every scoop must be leveled off (not heaped), otherwise the concentration differs from what the can states.",
        "What water temperature is right?",
        "Most formulas recommend 40-50°C warm water (some brands 40°C), which dissolves well while preserving active nutrients; never use boiling water, as it destroys probiotics and protein structure. Feed right after mixing or refrigerate, and do not reheat leftover milk repeatedly.",
        "Most formulas are 30 ml/scoop, follow the label on the can",
        "Level scoops (scooped flat), water before powder, temperature per the can instructions (usually 40-70°C)",
        "The volume after mixing is slightly larger than the water, which is normal",
        "Results are for reference only; follow the mixing instructions on the formula can",
    ]))

    # ---------------- growth-chart (16) ----------------
    write('growth-chart', build('growth-chart', [
        "👶 Child Growth Chart",
        "Assesses growth and development of children aged 0-5 against WHO standards",
        "Core formula (by input variable): weight / (height/100)^2",
        "📖 Read the \"Child Growth Chart User Guide\"",
        "📚 Deep dive: Child Growth Chart",
        "Regular check-in entry: at each child health visit, enter the height and weight (plus head circumference",
        "after age 2) and compare against the WHO P3-P97 reference range for the same month of age to see which percentile the baby sits in.",
        "Track the longitudinal trend: a single value has limited meaning; consistently staying in the same percentile band (for example stable near P50) indicates health, while crossing down a band in a short period calls for checking feeding or illness.",
        "Individual interpretation: babies of tall parents often sit above P85 and those of shorter parents below P15, and both can be normal; the key is whether the \"genetic track\" is stable.",
        "Male, 12 months, height 75.7 cm, weight 9.6 kg",
        "WHO male reference height at 12 months is [68.6, 71.0, 75.7, 80.0, 82.5] cm and weight reference is [7.7, 8.6, 9.6, 10.8, 11.8] kg. Height 75.7 = the P50 median (medium); weight 9.6 = the P50 median (medium). A height of 80 cm would put the baby in the upper-middle P85 band. BMI is evaluated only after 24 months.",
        "Does a low percentile always mean there is a problem?",
        "Not necessarily. P3-P15 that stays stable and grows along its own track is often simply inherited shorter stature and needs no intervention; only below P3 or a clear drop over a short period warrants medical assessment of nutrition or endocrinology. Focus on growth velocity rather than a single absolute value.",
        "How do the WHO standards and China's",
        "compare?",
        "China's 2009 and 2015 growth standards are very close to WHO (both based on healthy breastfed populations). This tool uses the WHO 0-5 year standard: birth weight 2.5-4.0 kg is normal, monthly gain 1-1.5 kg in the first 3 months, 0.5-0.6 kg at 3-6 months, 0.25-0.3 kg at 6-12 months, and 2.5-3 kg for the whole year at 1-2 years.",
    ]))

    # ---------------- pumping-plan (21) ----------------
    write('pumping-plan', build('pumping-plan', [
        "/ Pumping Plan Calculator",
        "📖 Read the \"pumping-plan User Guide\"",
        "🧮 Pumping Plan Calculator",
        "Wondering how to pump after returning to work without the chaos? Enter the working hours and the baby's age in months, and the tool gives the number of daily pumping sessions, the interval and the per-session and total volume, following the \"pump once every 3-4 hours\" principle.",
        "Pump scheduling: following the \"pump once every 3 to 4 hours\" principle, sessions per day = working hours / pumping interval; target volume per session = approx. the baby's daily milk need / number of sessions; total = per-session volume x number of sessions, checked against the baby's age-based daily need (about 150 mL/kg per day).",
        "Working hours (h)",
        "Volume per session (ml, optional)",
        "📚 Deep dive: Pumping and Storage Plan",
        "Scheduling pumping for working mothers: enter working hours and the baby's age in months to estimate how many sessions are needed during work, how far apart they are, and the per-session and full-day stored volume, matched to the company's lactation room availability.",
        "Inventory management: plan the frozen stock by a single-day reserve, follow first-in-first-out and label with dates, so nothing expires and gets wasted.",
        "Increasing supply: when the baby's daily need rises (such as during a growth spurt), increase the volume per session or tighten the interval, and expand the frozen reserve accordingly.",
        "Work 9 hours, baby 4 months old",
        "Sessions = max(1, round(9/3.5)) = 3; interval = 9/3 = 3.0 hours; a 4-month-old baby needs 700 ml per day, so without a custom value each session = round(700/4) = 175 ml; single-day reserve = 175 x 3 = 525 ml. That is 3 pumping sessions at work, roughly every 3 hours, storing about 525 ml.",
        "How long should the pumping interval be?",
        "Every 3-4 hours is recommended, as close as possible to the baby's feeding rhythm in order to maintain milk supply; intervals that are too long cause engorgement and blocked ducts and suppress lactation. Estimate the volume per session as the baby's daily need / 4 (for example about 175 ml per session at 4 months).",
        "How long can pumped milk be stored?",
        "About 4 hours at room temperature 25°C, 24-48 hours refrigerated at 4°C, and about 3 months frozen at -18°C. Once thawed, drink within 24 hours and do not refreeze. Store it at the back of the fridge, label storage bags with dates, and use first in, first out.",
        "Pumping interval follows the 3-4 hour principle, sessions = working hours / interval",
        "The baby's daily milk need is estimated from age (600-750 ml), with large individual variation",
        "Refrigerate 24 h / freeze 3 months, label with dates and use first in, first out",
        "Results are for reference only; follow the baby's needs and your own lactation situation",
    ]))


if __name__ == '__main__':
    main()
