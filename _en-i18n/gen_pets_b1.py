#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'pets')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'pets')
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
    out = {'slug': slug, 'industry': 'pets', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('feeding-amount', build('feeding-amount', [
        '🐾 Daily Pet Feeding Amount Calculator',
        'Calculate the daily feeding amount and feeding schedule from body weight, activity level and life stage',
        '/ Feeding Amount',
        '📖 View the Daily Pet Feeding Amount Calculator user guide',
        '📚 In-depth analysis: Daily Pet Feeding Amount Calculator',
        'Precise feeding for growing puppies and kittens: puppies under 4 months and kittens under 6 months are in a rapid growth phase with stage factors as high as 3.0 and 2.5; dosing by body weight and caloric density avoids underfeeding that stunts growth, or overfeeding that causes obesity.',
        'Extra amounts in pregnancy and lactation: the factor is 2.5 for pregnant or nursing bitches and 2.0 for queens, so energy needs are close to 1.5–2 times the adult level; the tool automatically scales the daily amount by the corresponding stage factor.',
        'Control for seniors and weight-loss groups: the factor drops to 1.3 for dogs over 7 years and 1.1 for senior cats; combined with the low-activity factor of 0.8 it precisely lowers total daily calories, which suits weight management.',
        'Worked example: adult dog, body weight 10 kg, 3.5 kcal/g, normal activity',
        'RER (resting energy) = 70 × 10^0.75 ≈ 70 × 5.623 = 393.6 → about 394 kcal;\nDER (daily energy) = RER × adult factor 1.6 × normal activity factor 1.0 = 393.6 × 1.6 = 629.8 kcal;\ndaily feeding amount = DER ÷ caloric density 3.5 = 629.8 ÷ 3.5 ≈ 180 g;\nan adult dog is fed twice a day → about 90 g per meal (puppies 4 meals, adolescents 3).',
        'How do I fill in the caloric density?',
        'It is the metabolisable energy (ME) per gram of pet food: typically about 3.0–4.0 kcal/g for dry food, 2.5–3.5 kcal/g for semi-moist food and 0.8–1.5 kcal/g for canned staple food. Look for the metabolisable energy / ME label on the bag; a wrong value directly inflates or shrinks the feeding amount.',
        'Why use RER × a factor instead of a fixed gram amount?',
        'RER = 70 × body weight^0.75 is the standard estimate of basal metabolism in dogs and cats (Kleiber’s law), corrected into DER by stage, activity and physiological-state factors. Breed, neuter status and season all make a difference, so the factor method is closer to real needs than a fixed gram amount — but it is still an estimate; for obese or ill dogs and cats follow your vet’s advice.',
        'About Feeding Amount',
    ]))

    write('grooming-guide', build('grooming-guide', [
        '🐱 Pet Grooming Style Guide',
        'A reference of common grooming styles for cats and dogs, with style notes and care advice',
        '/ Grooming Guide',
        '📖 View the Pet Grooming Style Guide user guide',
        '📚 In-depth analysis: Pet Grooming Style Guide',
        'Choose a style by breed: different dog breeds (poodle, bichon, schnauzer and so on) have signature cuts; the guide lists the available styles and suitable occasions by breed, so you do not blindly follow trends and ruin the coat.',
        'Adjust by season and function: a cool short coat in summer, a longer coat in winter for warmth; working dogs favour a clean, practical cut that picks up less dirt, while companion dogs can lean towards cute styles.',
        'Around surgery and during skin problems: elaborate styling is unsuitable when there is skin disease or injury; the guide advises prioritising medical care over grooming.',
        'Example: choosing a cool summer cut for a Golden Retriever',
        'Golden Retrievers are double-coated, so a cool trim is recommended in summer (2–3 cm left on the body, with the belly and paw pads thinned for heat dissipation), keeping the waterproof undercoat while lowering the risk of heatstroke. Switch breeds in the guide to see the key points, tools and cautions for that style. Note: the undercoat must never be shaved off, or thermoregulation is affected.',
        'How often should different breeds be groomed?',
        'Long-haired or curly-coated dogs (poodle, bichon, komondor) about every 4–6 weeks; short-haired dogs (French bulldog, pug) only need cleaning care every 6–8 weeks; cats usually groom themselves, with brushing care every 4–8 weeks for healthy cats. The exact interval varies with coat type, activity level and season.',
        'What should I watch out for when choosing a style?',
        '1. For double-coated dogs (Samoyed, Golden Retriever, Husky) never shave the undercoat off — only trim the outer coat for cooling. 2. Senior and very young dogs get stressed easily, so shorten each session. 3. With red or swollen skin, wounds or parasites, see a vet before grooming. 4. For white dogs, watch tear stains and the safety of coat-whitening products. This guide is popular-science reference only; have the work done by a professional groomer.',
        'About Grooming Guide',
    ]))

    write('kennel-space', build('kennel-space', [
        '🐾 Pet Boarding Space Calculator',
        'Calculate the area needed for boarding, plus kennel or cattery dimensions and activity space, from your pet’s size',
        '/ Kennel Space',
        '📖 View the Pet Boarding Space Calculator user guide',
        'Boarding area standards: kennel area = single-dog kennel area × number (not less than 4 m² per small dog); activity area = activity standard × (when the number is greater than 1, a sharing factor of 1 + (number − 1) × 0.7 applies); total area = kennel area + activity area; cats are counted separately by cattery and activity standards.',
        '📚 In-depth analysis: Pet Boarding Space Calculator',
        'Planning temporary boarding for several dogs at home: take the single-kennel area and activity area by dog size (small / medium / large / giant) and the tool works out the total footprint of N individual kennels plus the shared activity area, so you can free up rooms in advance.',
        'Zoning a cattery for several cats: a single cat needs far less area than a dog, but a litter area and vertical space are required; the tool gives the single-cage and activity areas by cat size.',
        'Enlarging the activity area for long stays (over 14 days): long-term confinement needs more exercise space, so the tool applies an extra 1.2 factor to the activity area, indicating that a larger exercise ground is needed.',
        'Worked example: 3 medium dogs, 20 days of boarding',
        'One medium dog: kennel area 6 m², activity area 15 m²;\ntotal kennel area = 6 × 3 = 18 m²;\nactivity area (shared by 3, with a diminishing factor) = 15 × (1 + (3−1)×0.5) = 15 × 2 = 30 m²;\nboarding 20 days > 14 days → activity area ×1.2 = 36 m²;\ntotal area required = 18 + 36 = 54.0 m² (single kennel about 2.5 × 2.4 × 2 m).',
        'What are the area standards based on?',
        'A single kennel of 4–12 m² and a cat cage of 1.5–2.5 m² are common reference values for households and small boarding facilities, increasing with body size; when several animals share the activity area a diminishing factor applies (each extra animal adds 0.5 times) so the figure does not grow without limit, keeping both exercise and space efficiency.',
        'Why does long-term boarding need a larger activity area?',
        'Dogs and cats kept in long-term confinement easily develop stereotypic behaviour and stress, and insufficient space accumulates health risks; stays over 14 days count as long-term, so the extra ×1.2 on the activity area signals that more walking or roaming space is needed. This tool is a planning reference; actual facilities must comply with local husbandry and animal welfare rules.',
        'About Kennel Space',
    ]))

    write('pet-age-convert', build('pet-age-convert', [
        '🔄 Pet Age Converter',
        'Convert cat and dog ages into human years, with a life-stage comparison',
        '/ Pet Age Converter',
        '📖 View the Pet Age Converter user guide',
        'Pet age conversion: a dog’s first year ≈ 15 human years, the second year ≈ 24 human years, and each dog year after that ≈ 4 to 5 human years (lower for small dogs, higher for large dogs); a cat’s first year ≈ 15 human years, the second year ≈ 24, and each cat year after that ≈ 4 human years; the puppy or kitten, adult and senior stages are labelled accordingly.',
        '📚 In-depth analysis: Pet Age Converter',
        'Estimating age for adoption or rescue: stray dogs and cats often have no known birthday, so converting the estimated age into human years helps judge whether they have entered old age (for example a 6-year-old large dog is equivalent to over 45 human years), and adjust feeding and check-ups accordingly.',
        'Timing senior-disease screening: the senior stage of dogs and cats (from 7 years in dogs, 8 in cats) corresponds to middle and old age in humans, so a check-up every six months is recommended; the converted result tells the owner intuitively that the pet is equivalent to a human of a certain age.',
        'Body-size differences: large and giant dogs age faster; at the same 5 years of age, a small dog ≈ 36 human years while a giant dog ≈ 45, so check-up and joint-care schedules differ.',
        'Worked example: a 5-year-old medium dog and a 5-year-old cat',
        'Medium dog (factor 1.0): year 1 = 15 years + year 2 = 9 years → 24, then +5 per year → 24 + (5−2)×5 = 39 years;\nsmall dog (factor 0.85, +4 per year) → 24 + 3×4 = 36 years;\ngiant dog (factor 1.3, +7 per year) → 24 + 3×7 = 45 years;\ncat (fixed +4 per year) → 24 + (5−2)×4 = 36 years.',
        'Why do large and small dogs use different conversion factors?',
        'Large dogs mature faster and live shorter lives, and senior diseases (joints, heart) appear earlier, so the bigger the body the more human years each year counts (small dog +4, medium +5, large +6, giant +7). This model is a general approximation and is not the same as precise physiological age.',
        'Can the age conversion be used directly for medication or vaccination?',
        'No. The conversion only helps you understand the degree of ageing and the care priorities; vaccination, deworming and drug doses must follow body weight, health status and your vet’s plan. This tool does not replace professional diagnosis and treatment.',
        'About Pet Age Converter',
    ]))

    write('vaccine-reminder', build('vaccine-reminder', [
        '⏰ Pet Vaccination and Deworming Reminder',
        'Manage your pet’s vaccination and deworming records with automatic due-date reminders (data stored locally)',
        '/ Vaccine Reminder',
        '📖 View the Pet Vaccination and Deworming Reminder user guide',
        '📚 In-depth analysis: Pet Vaccination and Deworming Reminder',
        'Primary vaccination for puppies and kittens: dogs start combination vaccines at 6–8 weeks, one shot every 21 days for 3 shots, with rabies added after 3 months; cats start the feline triple vaccine at 8 weeks along the same lines. The tool works out the due date of the next shot from the recorded dates.',
        'Annual boosters: the canine combination vaccine, rabies vaccine and feline triple vaccine are all boosted once a year (a 365-day cycle); the tool marks an item as due soon when it falls within the next 7 days.',
        'Deworming frequency management: internal deworming every 90 days, external deworming or heartworm prevention every 30 days; when several items run in parallel the tool groups them into three categories (overdue / due soon / normal) so nothing is missed.',
        'Worked example: two records for a 2-year-old dog (reference date 2026-09-10)',
        'Canine combination vaccine, last given 2025-09-01 (365-day cycle) → due 2026-09-01, which is −9 days from today → overdue;\ninternal deworming, last given 2026-08-01 (90-day cycle) → due 2026-10-30, which is +50 days from today → normal;\nsummary for this example: 1 overdue, 1 normal, 0 due soon. The tool keeps the records in the browser’s local storage, and each time you tap "done" the next due date for that item is refreshed.',
        'How is the primary vaccination programme scheduled?',
        'Dogs: first combination vaccine at 6–8 weeks, then one shot every 21–28 days up to 16 weeks of age (not fewer than 3 shots), with rabies at 3 months of age. Cats: first feline triple vaccine at 8 weeks, then one shot every 3–4 weeks for 2–3 shots. Follow the vaccine leaflet and local epidemic-prevention requirements in detail.',
        'Why is heartworm prevented monthly?',
        'Heartworm is transmitted by mosquito bites, and the larvae migrate in the body for about 6 months before becoming adults; monthly dosing blocks the larvae at every stage. Year-round prevention is recommended in southern regions or areas with active mosquito vectors. This tool is only a reminder — consult your vet before using any medication.',
        'About Vaccine Reminder',
        'Pet name',
    ]))


if __name__ == '__main__':
    main()
