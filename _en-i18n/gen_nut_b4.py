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
    write('estimate-1', build('estimate-1', [
        "🔮 Dietary Fiber Intake Estimator",
        "Tick off the high-fiber foods you ate today to estimate your total dietary fiber and get suggestions.",
        "Total dietary fiber = Σ intake(g) × fiber content(g/100g) ÷ 100; the Chinese dietary guidelines recommend 25 to 30 g per day, and the adequacy rate = actual intake ÷ 25 × 100%; whole grains and mixed beans give about 5 to 10 g/100g, dark vegetables about 2 to 3 g/100g and soy products about 5 to 8 g/100g, and snack suggestions are derived from the adequacy rate.",
        "⚠️ This tool offers dietary self-management reference only and cannot replace a nutrition intervention plan. If you have a gastrointestinal disease or a chronic condition, follow your clinical advice.",
        "Dietary Fiber Reference",
        "Recommended daily intake for adults: 25 - 30 g.",
        "When raising fiber intake, drink more water at the same time to avoid gastrointestinal discomfort.",
        "Choose whole grains, beans, vegetables and fruit first.",
        "📚 Deep Dive: Dietary Fiber Intake Estimation",
        "Tick the foods you often eat to estimate fiber for the whole day and compare against the recommendation",
        "When intake falls short, add whole grains, beans, vegetables and fruit to make up the 25-30 g",
        "Compare fiber density across ingredients and pick high-fiber foods",
        "Adequacy Check",
        "Oats 30g (3g fiber) + sweet potato 150g (3.6g) + broccoli 100g (2.6g) + apple 200g (4.8g) + black beans 50g (4g) ≈ 18g; that is still 7-12g short of the recommended 25-30g, so one serving of mixed grains would close the gap.",
        "High-Fiber Choices",
        "Chia seeds, oats and beans are dense in fiber (up to 10-35g per 100g), while refined white rice and flour are extremely low (<1g/100g), so mixing coarse and fine grains raises your fiber intake.",
        "How much dietary fiber per day?",
        "The Chinese dietary guidelines recommend 25-30g per day; most people in China consume under 15g, so whole grains, beans, vegetables and fruit need to increase.",
        "Is more fiber always better?",
        "Excess (over 40g) causes bloating and interferes with mineral absorption; if you suddenly increase it, drink more water and raise it gradually.",
    ]))
    write('food-calorie-lookup', build('food-calorie-lookup', [
        "⚡ Common Food Calorie Lookup",
        "A local static lookup table with 200 g basic weight references for common Chinese foods.",
        "/ Common Food Calorie Lookup",
        "Total calories = Σ intake(g) × calories(kcal/100g) ÷ 100; the Chinese dietary reference for daily energy is roughly 1800 to 2100 kcal for adult women and 2250 to 2600 kcal for adult men (banded by physical activity level); the recommended macronutrient energy shares are 50% to 65% from carbohydrates, 20% to 30% from fat and 10% to 15% from protein.",
        "Per 100g (kcal)",
        "200g reference (kcal)",
        "📚 Deep Dive: Common Food Calorie Lookup (per 100g)",
        "Look up calories per 100g of common Chinese foods to plan your diet",
        "Use the 200g reference values to estimate the calories in one serving quickly",
        "Compare similar foods (such as rice versus steamed bun) and pick the lower-calorie one",
        "Per 100g Reference",
        "Rice 116, steamed bun 223, chicken breast 165, egg 144, avocado 160, banana 93, apple 54, broccoli 34 kcal/100g; 200 g of rice = 232 kcal.",
        "Like-for-Like Comparison",
        "At the same 100 g, steamed bun at 223 is nearly double rice at 116; during fat loss, replacing some of the steamed buns and noodles with rice or tubers controls calories better.",
        "Why per 100g and not per serving?",
        "100 g is the standard baseline and makes foods easy to compare; for an actual serving just use ratio = weight/100 to convert, so portion labels do not mislead you.",
        "Does cooking change calories?",
        "Yes, added oil or sugar raises them significantly; this table mostly lists raw weight or usual boiled preparations, so fried or braised dishes need cooking-oil calories added separately (oil 9 kcal/g).",
        "Enter a food name, e.g. chicken breast / rice / milk",
    ]))
    write('estimate-2', build('estimate-2', [
        "🔮 Salt Intake Estimator",
        "Select the high-sodium foods you ate today to estimate total sodium and salt intake and help control your salt.",
        "Salt intake = Σ intake(g) × sodium content(mg/100g) ÷ 100 ÷ 393.4; 1 g of salt contains about 393 mg of sodium, and the conversion is salt(g) ≈ sodium(mg) ÷ 400; the Chinese dietary guidelines recommend no more than 5 g of salt per day (about 2000 mg of sodium) and 3 to 5 g for people with high blood pressure; pickled products and processed meat can reach 800 to 2000 mg of sodium per 100 g.",
        "Other sodium intake (mg, optional)",
        "World Health Organization recommendation: adults should not exceed 5 g of salt per day (about 2000 mg of sodium), and people with high blood pressure should keep it as close to 3 g as possible.",
        "📚 Deep Dive: Salt (Sodium) Intake Estimation",
        "Tick the foods you often eat to estimate daily sodium and salt intake, then compare against the 5 g salt ceiling",
        "For high-sodium groups (high blood pressure), find hidden salt sources such as sauces and processed meat",
        "Convert sodium to salt: salt(g) ≈ sodium(mg)/0.393/1000",
        "Salt Conversion",
        "2300 mg of sodium for the whole day → salt ≈ 2300÷0.393÷1000 ≈ 5.85 g, over the 5 g ceiling; dropping one spoon of soy sauce (about 1000 mg of sodium) saves roughly 2.5 g of salt.",
        "Hidden Salt",
        "Luncheon meat 100 g sodium ≈ 1000 mg, pickled mustard tuber 100 g ≈ 4250 mg, dried noodles 100 g ≈ 900 mg; processed foods that do not taste salty can have off-the-charts sodium.",
        "How do salt and sodium convert?",
        "Table salt NaCl is about 39.3% sodium, so salt(g) = sodium(mg)/393; 5 g of salt ≈ 1965 mg of sodium, and the guidelines recommend less than 5 g of salt per day.",
        "Can low-sodium salt be used freely?",
        "Low-sodium salt replaces sodium with potassium, which is risky for people with impaired kidney function or those taking potassium-sparing drugs, so total salt intake still needs control.",
    ]))
    write('generator-glucose-load', build('generator-glucose-load', [
        "⚗️ GI (Glycemic Index) and Load",
        "Glycemic Index",
        "Glycemic load GL = GI × digestible carbohydrate(g) ÷ 100, where GI is the glycemic index (glucose 100 as the baseline); GL of 20 or more is a high load, 11 to 19 a medium load, and 10 or less a low load; total daily GL is recommended to stay under 80, and people managing blood sugar should pick foods with a low GI and a GL within 10.",
        "📚 Deep Dive: GI and Glycemic Load (GL) Calculation",
        "Compute GL from a food's GI and its carbohydrate intake to assess the post-meal blood sugar impact",
        "Compare a high-GI low-carbohydrate food such as watermelon with a low-GI high-carbohydrate one",
        "Choose foods by GL band when managing blood sugar or diabetes",
        "GL Calculation",
        "GL = GI × available carbohydrate(g) / 100. Plain white rice has GI 83 and a 50 g carbohydrate portion → GL = 83×50/100 = 41.5 (high load); an apple has GI 36 and 15 g carbohydrate → GL = 5.4 (low load).",
        "GL≤10 is a low load, 11-20 a medium load and >20 a high load; watermelon has GI 72 but about 11 g carbohydrate per portion → GL≈7.9, a low load instead, so quantity matters too.",
        "What is the difference between GI and GL?",
        "GI only looks at how fast blood sugar rises and ignores quantity, while GL multiplies in the actual carbohydrate and therefore reflects the real blood sugar burden, which makes it more practical for food choice.",
        "Does a low GI mean I can eat more?",
        "No. A low GI with a large amount of carbohydrate still gives a high GL; control GL and also keep total carbohydrate and portion size in check.",
        "About GI (Glycemic Index) and Load",
        "GI (Glycemic Index) and load. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))


if __name__ == '__main__':
    main()
