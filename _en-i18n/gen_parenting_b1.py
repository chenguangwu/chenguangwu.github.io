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
    # ---------------- diaper-usage (23) ----------------
    write('diaper-usage', build('diaper-usage', [
        "Diaper Usage performs a professional calculation from the input parameters and outputs the result.",
        "/ Diaper Usage Estimator",
        "📖 Read the \"diaper-usage User Guide\"",
        "📐 Diaper Usage Estimator",
        "The biggest risk when stockpiling diapers is buying the wrong size or too many. Look up the reference daily count by age in months, enter the unit price, and the tool automatically computes the monthly quantity and cost to help you plan purchases.",
        "Unit price per diaper (CNY)",
        "Estimation days",
        "📚 Deep dive: Diaper Usage Estimation",
        "New parents stocking up before the birth:",
        "Before the due date,",
        "estimate the total quantity and cost for the first 1-3 months based on the baby's age bracket, then buy in several small batches timed to promotions, to avoid the wrong size or stockpiling expired stock.",
        "Adjust the size by age bracket: babies gain weight fast and the NB/S window is short (mostly 0-4 months), so switch to M/L early using the weight reference table to prevent leaks or leg marks.",
        "Business trips and travel packing: stock up at travel days x daily usage plus 20%, and bring an extra pack of the next size in case the baby suddenly outgrows it.",
        "Age 6 months, unit price 2 CNY per diaper, usage over the next 30 days",
        "Enter age 6, unit price 2, days 30. Bracketing rule: 7-12 months is about 5.5 diapers per day, and the 6-month bracket takes 7 per day (the 4-6 month band). Total usage = ceil(7 x 30) = 210 diapers; cost = 210 x 2 = 420 CNY; recommended size M (6-11 kg, 4-10 months). That is about 210 diapers over 30 days at a cost of about 420 CNY.",
        "Why do the daily diaper counts differ so much by age?",
        "Newborns pass frequently (about 10-12 diapers per day); as the gut develops and a feeding routine forms, 1-3 months is about 8-10, 4-6 months about 6-8, 7-12 months about 5-6, and after age 1 about 4-5. This tool uses common bracketing experience values, but the actual change frequency of your baby is the final criterion.",
        "What happens if I pick the wrong size?",
        "Too small digs into the belly, leaves red marks and can leak; too large wraps loosely and leaks from the sides. Reference: NB up to 5 kg (0-1 month), S 3-8 kg (1-4 months), M 6-11 kg (4-10 months), L 9-14 kg (10-18 months), XL 12 kg+ (18 months+). When the weight crosses a band, follow the weight.",
        "Reference counts: newborn 10-12 per day, 1-3 months 8-10, 4-6 months 6-8, 7-12 months 5-6, after age 1 4-5",
        "Sizes: NB newborn, S 3-8 kg, M 6-11 kg, L 9-14 kg, XL 12 kg+, follow the baby's weight",
        "As age grows the amount per change rises while the frequency falls",
        "Results are for reference only; follow actual changes and your baby's comfort",
    ]))

    # ---------------- feeding-amount-baby (21) ----------------
    write('feeding-amount-baby', build('feeding-amount-baby', [
        "Feeding Amount Baby performs a professional calculation from the input parameters and outputs the result.",
        "/ Baby Feeding Amount Estimator",
        "📖 Read the \"feeding-amount-baby User Guide\"",
        "🔮 Baby Feeding Amount Estimator",
        "The most common question from new parents: how much per feeding? Based on age in months and weight, and combining \"daily milk volume = approx. weight x 150 ml/kg\" with the age reference values, it gives the per-feeding and daily volume ranges.",
        "Age in months",
        "Feedings per day",
        "📚 Deep dive: Daily Baby Milk Volume Estimation",
        "Preparing milk by age: for mixed and formula-fed families, estimate the daily total and per-feeding volume from the baby's age and weight, to plan formula purchases and the rhythm of bottle feeding.",
        "Cross-check with the growth curve: when the baby's weight gain deviates from expectations, use the milk volume estimate to infer whether intake is sufficient, then judge by diaper output (6 or more wet diapers per day signals sufficient intake).",
        "Transition to solid foods: from 6 months milk volume is gradually replaced by solids; use this tool to watch the total energy structure of \"milk plus solids\" and avoid a nutrition gap during weaning.",
        "Age 4 months, weight 6 kg, 6 feedings per day",
        "By the weight method: 6 kg x 150 ml/kg = 900 ml. The age reference table gives 900 ml at 4 months (refMap[4]=900). Daily recommendation = round((900+900)/2) = 900 ml; per feeding = round(900/6) = 150 ml. That is about 900 ml per day and about 150 ml per feeding.",
        "What if my baby cannot finish the recommended amount per feeding?",
        "The milk volume is only a reference averaged over weight and age, and individual differences are large. If the baby is alert, gains weight steadily and has 6 or more wet diapers per day, there is usually no need to force feeding; frequent spit-up or gas can be addressed by reducing the volume and checking feeding position and burping.",
        "Does milk volume drop after 6 months?",
        "The total usually stays around 800 ml, but its share declines as solids increase. Reference: 1-3 months 600-800 ml, 4-6 months 800-1000 ml, 7-12 months 800 ml plus solids, 180-240 ml per feeding, 4-5 times per day.",
        "Daily milk volume = approx. weight x 150 ml/kg, take the median of the age reference values",
        "In the newborn period feed every 2-3 hours; as age grows the amount per feeding rises and the number of feeds falls",
        "From 6 months solids are introduced and milk volume transitions gradually",
        "Results are for reference only; follow your pediatrician's guidance and the baby's actual needs",
    ]))

    # ---------------- feeding-schedule (14) ----------------
    write('feeding-schedule', build('feeding-schedule', [
        "👶 Baby Feeding Plan",
        "Generates a scientifically sound feeding plan from the age in months",
        "Generates a scientifically sound feeding plan from the age in months by professional calculation from the input parameters.",
        "📖 Read the \"Baby Feeding Plan User Guide\"",
        "📚 Deep dive: Baby Feeding Plan",
        "Regular bottle schedule: derive the daily total from the baby's age (FEEDING table) and weight, then generate a full-day feeding timetable automatically at a fixed interval from the start time you set.",
        "Breastfeeding rhythm: when you pick the \"Breast milk\" mode, each feeding is marked \"on demand\", offering only interval and total volume references, respecting the baby's hunger signals rather than forcing a fixed clock.",
        "Routine training: use the generated timetable to build a predictable feed-sleep rhythm that helps the baby tell day from night and reduce night feeding dependence.",
        "Age 4 months, weight 6 kg, start 08:00, formula",
        "FEEDING[4] = {perKg:120, feeds:7, interval:3}. Daily total = 120 x 6 = 720 ml; per feeding = 720/7 = 103 ml; starting at 08:00 every 3 hours: 08:00, 11:00, 14:00, 17:00, 20:00, 23:00, 02:00, seven feeds in total.",
        "Do I have to follow the timetable strictly?",
        "No. The timetable is a rhythm reference, and breastfed babies are better off on demand. As long as the daily total and weight gain are on target and output is normal, a 30-minute shift either way is fine. From 4 months you can gradually widen the intervals and reduce night feeds.",
        "How does the timetable change after solids are introduced?",
        "From 6 months the daily milk volume is still about 800 ml, but split into 5 feedings with 1-2 solid meals mixed in; after age 1 it transitions to 3 main meals plus 500 ml of milk. In the FEEDING table, perKg drops to 110 at 6 months and 100 at 12 months, and the number of feeds falls from 5 to 3.",
    ]))


if __name__ == '__main__':
    main()
