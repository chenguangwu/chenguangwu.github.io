#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'civil')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'civil')
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
    out = {'slug': slug, 'industry': 'civil', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

DISCL_C = " A professional civil engineering tool based on authoritative structural codes, for reference only."


def main():
    write('active-earth-rankine', build('active-earth-rankine', [
        "\U0001F39A\uFE0F Rankine active earth pressure calculation (civil)",
        "Active earth pressure resultant and critical depth on a vertical wall back for cohesionless or cohesive backfill, using Rankine theory.",
        "Rankine active earth pressure calculation",
        "Unit weight of soil \u03B3 (kN/m\u00B3)",
        "Backfill height H (m)",
        "Critical depth for cohesive soil z\u2080 = 2c/(\u03B3\u221aKa)",
        "Active thrust Ea = \u00BD\u03B3H\u00B2Ka \u2212 2cH\u221AKa (when positive)",
        "This tool applies the Rankine theory for horizontal backfill with no surcharge",
        "\U0001F4DA In-depth analysis: Rankine active earth pressure calculation (civil)",
        "When designing a gravity or cantilever retaining wall, the active pressure intensity at the base pa = \u03B3zKa \u2212 2c\u221AKa governs the wall bending moment and the base reaction.",
        "Compare how the internal friction angle \u03C6 and the wall back inclination affect earth pressure, to optimise the section for both economy and safety.",
        "Check the saturated backfill or ground surcharge case: water pressure and surcharge raise earth pressure significantly and must be superposed.",
        "Active earth pressure on a retaining wall with homogeneous sand backfill",
        "With \u03B3 = 18 kN/m\u00B3, \u03C6 = 30\u00B0, c = 0 and wall height H = 5 m: Ka = tan\u00B2(45\u00B0 \u2212 \u03C6/2) = 0.333. At the base pa = \u03B3H\u00B7Ka = 18 \u00D7 5 \u00D7 0.333 \u2248 30 kPa, the resultant Ea = \u00BDpa\u00B7H = 75 kN/m acting at H/3 above the base.",
        "How do I choose between Rankine and Coulomb?",
        "They agree for a smooth vertical wall back with horizontal cohesionless backfill. With wall inclination, a rough back or surcharge, Coulomb is more general, while Rankine is convenient for quick hand estimates.",
        "Does cohesive soil with c > 0 produce negative pressure?",
        "Yes, a tension crack zone appears (pa < 0) and the soil behind the wall actually cracks. In practice the effective pressure is taken below the critical depth, or the resultant is measured from the critical depth down.",
        "How is the groundwater table handled?",
        "Below water use the submerged unit weight \u03B3\u2032 and add water pressure. As the table rises both earth pressure and uplift increase, so sliding and overturning stability must be rechecked.",
    ]))

    write('beam-udl', build('beam-udl', [
        "\u2696\uFE0F Simply supported beam under uniformly distributed load (civil)",
        "Maximum moment, shear, mid-span deflection and mid-span bending stress for a simply supported beam under a UDL.",
        "Simply supported beam UDL internal force calculation",
        "\u03C3 = M/W, where W = bh\u00B2/6 is the section modulus",
        "Maximum bending moment M",
        "= qL\u00B2/8 (at mid-span)",
        "Maximum shear V",
        "= qL/2 (at the supports)",
        "Mid-span deflection \u03B4 = 5qL\u2074/(384EI) (use N and m consistently)",
        "Bending stress \u03C3 = M/W, where W = bh\u00B2/6 is the section modulus",
        "\U0001F4DA In-depth analysis: simply supported beam under UDL (civil)",
        "For floor slabs and secondary beams, take the mid-span moment Mmax = wL\u00B2/8 and shear Vmax = wL/2 as the governing forces for reinforcement and connection design.",
        "Check deflection: the mid-span deflection f = 5wL\u2074/(384EI) governs floor comfort and clear headroom.",
        "Compare the sensitivity of the moment to span L and line load w, to optimise beam depth and material use.",
        "4 m simply supported secondary beam under UDL",
        "For span L = 4 m and line load w = 10 kN/m: Mmax = wL\u00B2/8 = 10 \u00D7 16/8 = 20 kN\u00B7m; Vmax = wL/2 = 20 kN. If EI = 2.4 \u00D7 10\u00B9\u00B9 N\u00B7mm\u00B2, the mid-span deflection f \u2248 5wL\u2074/(384EI) (assessed",
        "later).",
        "How much do UDL and point load results differ?",
        "For the same total load the mid-span moment from a central point load (PL/4) is about twice that of a UDL (wL\u00B2/8 = PL/8). Load form therefore directly affects reinforcement and the two must not be mixed.",
        "What if the deflection exceeds the limit?",
        "Increase the section depth h (deflection scales roughly as 1/h\u00B3), raise the stiffness EI, or shorten the span. You can also add a camber or switch to a continuous beam to reduce the mid-span moment.",
        "Can a continuous beam be estimated as simply supported?",
        "No. Support negative moments in a continuous beam are significantly larger than the mid-span moment of a simply supported beam, so a simply supported estimate understates support reinforcement. Use continuous-beam coefficients or a finite element check.",
    ]))

    write('calc-1', build('calc-1', [
        "\U0001F9EE Concrete mix design calculation (civil)",
        "Preliminary mix proportions from design strength, water-binder ratio, water content and sand ratio, following the JGJ 55 mix design standard.",
        "Cement content c = water content w \u00F7 water-binder ratio (W/C). Determine the total aggregate by the absolute volume method: total aggregate mass = concrete bulk density \u2212 cement \u2212 water; sand ratio \u03B2s = sand mass \u00F7 (sand + coarse aggregate) mass \u00D7 100% (usually 30% to 45%), so sand = total aggregate \u00D7 \u03B2s and coarse aggregate = total aggregate \u00D7 (1 \u2212 \u03B2s). Expressed relative to cement as 1, the materials give the mass ratio cement : sand : coarse aggregate : water.",
        "Design strength f",
        "Standard deviation \u03C3 (MPa)",
        "Water content per unit m",
        "Sand ratio \u03B2",
        "Cement density \u03C1",
        "Sand bulk density \u03C1",
        "Coarse aggregate bulk density \u03C1",
        "Air content \u03B1 (%)",
        "Calculate the mix",
        "Target strength: f",
        "Cement content: m",
        "Sand and coarse aggregate determined by the absolute volume method",
        "The result is a preliminary theoretical mix; actual construction must be adjusted by trial batching",
        "\U0001F4DA In-depth analysis: concrete mix design calculation (civil)",
        "For a cast-in-place C30 beam or slab, back-calculate water content and binder content from the trial strength and the water-binder ratio, then set the aggregate masses from the sand ratio.",
        "Adjusting slump: when the sand ratio or admixture is insufficient, recompute the aggregate proportion so the mix stays pumpable and densely compacted.",
        "Durability control for salt and frost: cap the maximum water-binder ratio and minimum binder content by exposure class; meeting strength is not enough, durability must also be satisfied.",
        "C30 absolute volume method example",
        "For a target slump of 35-50 mm, W/B = 0.50 and water content 185 kg/m\u00B3: binder = 185/0.50 = 370 kg. At a sand ratio of 0.35 the absolute volume method gives about 650 kg sand and 1205 kg coarse aggregate (tune for density and air), a mass ratio of 1 : 1.76 : 3.26.",
        "Does a lower water-binder ratio always mean higher strength?",
        "Generally inversely (Abrams' law), but too low a ratio makes the mix harsh and hard to compact and the strength can drop. Take the smallest ratio that satisfies durability while staying workable.",
        "Why is the trial strength higher than the design strength?",
        "To account for construction variability, trial strength = design strength + 1.645\u03C3 (where \u03C3 is",
        "the standard deviation), which guarantees a 95% pass rate. It is not simply the cement strength grade.",
        "Do crushed and rounded gravel differ in the mix?",
        "Crushed stone has a rough surface and needs more mortar to coat it, so the sand ratio and water content are slightly higher. Rounded gravel gives better workability but weaker interfacial bond, so adjust for the aggregate type.",
    ]))


if __name__ == '__main__':
    main()
