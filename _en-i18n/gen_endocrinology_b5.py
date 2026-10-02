#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'endocrinology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'endocrinology')
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
    out = {'slug': slug, 'industry': 'endocrinology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    write('insulin-adjustment', build('insulin-adjustment', [
        "\U0001F4D0 Insulin Dose (Basal + Bolus) Adjuster",
        "Based on a basal-bolus regimen, calculate insulin dose adjustment advice from blood glucose monitoring data",
        "Core formulas (by input): min(100, max(0, (basalDose \u00F7 (tdi \u00D7 0.8)) \u00D7 100)); max(0, basalDose + basalAdjust); bolusTotal \u00D7 0.30",
        "\U0001F4D6 See the \"Insulin Dose (Basal + Bolus) Adjuster User Guide\"",
        "Method for estimating total daily insulin",
        "By body weight",
        "Enter the total manually",
        "Total daily insulin TDI (U)",
        "Basal/bolus ratio",
        "50:50 (standard)",
        "40:60 (bolus weighted)",
        "60:40 (basal weighted)",
        "Target HbA1c (%)",
        "Mean fasting glucose (mmol/L)",
        "Target fasting glucose (mmol/L)",
        "Insulin glargine (long-acting)",
        "Insulin detemir (long-acting)",
        "Insulin degludec (ultra-long-acting)",
        "NPH (intermediate-acting)",
        "Bolus insulin",
        "Insulin aspart",
        "Insulin lispro",
        "Insulin glulisine",
        "Regular short-acting insulin",
        "Basal-bolus regimen",
        "Dose adjustment rules",
        "ISF/ICR calculation",
        "Basal-bolus allocation",
        "Action profile",
        "Onset",
        "Insulin degludec",
        "Ultra-long-acting, flat with no peak",
        "Insulin glargine U300",
        "Long-acting, flat",
        "About 36h",
        "Insulin glargine U100",
        "About 24h",
        "Insulin detemir",
        "Long-acting, with individual variation",
        "Intermediate-acting, with a clear peak",
        "Basal insulin mimics physiological basal secretion and suppresses hepatic glucose output; bolus insulin mimics meal-time secretion and controls post-meal glucose.",
        "Basal insulin adjustment rules (based on fasting glucose)",
        "Adjustment size",
        "Reduce the basal dose",
        "Keep unchanged",
        "Small increase",
        "Moderate increase",
        "+6 U or consult your doctor",
        "Bolus insulin adjustment (based on 2h post-meal glucose)",
        "2h post-meal glucose (mmol/L)",
        "Reduce the bolus dose by 10-20%",
        "Increase the bolus dose by 1-2U",
        "Increase the bolus dose by 2-4U",
        "Insulin sensitivity factor (ISF) and carbohydrate ratio (ICR)",
        "Insulin sensitivity factor (ISF)",
        "The 100 rule:",
        "ISF = 1500 (regular) / 1800 (rapid-acting) / 2000 (ultra-rapid) \u00F7 TDI",
        "Unit: mg/dL per U",
        "Convert to mmol/L: ISF(mmol/L/U) = ISF(mg/dL) \u00F7 18",
        "Carbohydrate ratio (ICR)",
        "The 500 rule:",
        "Unit: g/U (grams of carbohydrate covered by each unit of insulin)",
        "ICR experience reference values",
        "Clinical points on insulin therapy",
        "\U0001F4CB Starting dose estimate",
        "\u2022 T1DM: start at 0.4-0.5 U/kg/d",
        "\u2022 T2DM: start at 0.2-0.4 U/kg/d, or 10U/d titrated upwards",
        "\u2022 Basal:bolus = 50:50 for most patients; lean type 1 diabetes can use 40:60",
        "\u2696\uFE0F Principles of dose adjustment",
        "\u2022 Keep each adjustment within 10-20%",
        "\u2022 Observe 2-3 days after adjusting before reassessing",
        "\u2022 Adjust basal insulin first to control fasting glucose",
        "\u2022 For high post-meal glucose, adjust the bolus insulin of the matching meal",
        "\u2022 Insulin needs fall in renal impairment, so the dose must be reduced",
        "\u2022 Insulin needs rise during infection or stress",
        "\u2022 Consider reducing the bolus dose around exercise",
        "\u2022 Watch out for the difference between the dawn phenomenon and the Somogyi effect",
        "\u26A0\uFE0F Important statement:",
        "This tool is for education only; insulin dose changes must be decided by a specialist endocrinologist based on the individual patient. Never adjust your insulin dose on your own, as that risks severe hypoglycaemia or ketoacidosis.",
        "\U0001F4DA In-depth analysis: Insulin Dose (Basal + Bolus) Adjuster",
        "Estimating a correction dose with the correction factor when post-meal glucose is clearly high.",
        "Estimating the bolus insulin dose with the carbohydrate ratio for different carbohydrate intakes.",
        "Dose adjustment reference around exercise to reduce exercise-related hypoglycaemia risk.",
        "Correction dose calculation example",
        "Current glucose 14.0 mmol/L, target 7.0, using the 1800 rule with a daily total of 36 U gives ISF=(1800/36)=50 mmol/L/U: correction dose=(14-7)/50=0.14 U, that is about 1.4 U. Note: correction doses need a safety cap and should take any recent hypoglycaemia into account.",
        "How do I choose between the 1800, 1700 and 2200 rules?",
        "They suit approximate situations around a daily total of about 1800 U: 1700 for younger or insulin-sensitive people, 1800 as the routine choice, and 2200 for high insulin needs or clear resistance. All are empirical estimates.",
        "Can this tool replace the doctor's titration?",
        "No. It only helps you understand the dose composition and fine adjustments; in pregnancy, illness, changing kidney function or frequent hypoglycaemia the regimen should be adjusted by endocrinology.",
        "About \"Insulin Dose (Basal + Bolus) Adjuster\"",
        "Based on the basal-bolus multiple daily injection (MDI) regimen, this tool computes total daily insulin allocation and dose adjustment advice from body weight, HbA1c and glucose monitoring data.",
        "TDI by body weight or entered manually",
        "Automatic basal/bolus allocation",
        "ISF/ICR by the 1800/500 rules",
        "Adjustment advice based on fasting glucose",
        "Reference for planning insulin regimens",
        "Teaching MDI dose adjustment",
        "Endocrinology resident training",
        "Diabetes management education",
    ]))


if __name__ == '__main__':
    main()
