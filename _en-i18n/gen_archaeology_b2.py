#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'archaeology')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'archaeology')
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
    out = {'slug': slug, 'industry': 'archaeology', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ===== pottery-typology (22) =====
    write('pottery-typology', build('pottery-typology', [
        '📚 Pottery typology',
        'Comparison of pottery fabric, color, decoration and typical vessel forms by major Chinese archaeological culture periods',
        '📖 View "Pottery typology user guide"',
        'List pottery fabric, color, decoration and typical vessel forms by major Chinese archaeological culture periods (Yangshao, Longshan, Erlitou, Shang-Zhou, etc.) to aid field sherd identification and typological grouping. Compiled from public archaeological literature for study reference only.',
        'All stages',
        'Early Neolithic',
        'Middle Neolithic',
        'Late Neolithic',
        'Typology essentials: pottery fabric (fine-paste / sandy), color (red / grey / black / white), decoration (cord-marked / painted / rope-burnished / plain) and vessel-form combination are the core basis for periodization.',
        '📚 In-depth: pottery typology',
        'When identifying field sherds, compare by archaeological culture period the fabric (sandy / fine-paste), color (red / grey / black), decoration (cord-marked / basket-marked / painted) and typical vessel forms (li-tripod, jia, jar, ding), narrowing the cultural range.',
        'Distinguish the evolving features of Yangshao, Longshan, Erlitou and Shang-Zhou stages: e.g. Yangshao is mostly fine-paste red painted pottery, Longshan mostly grey-black eggshell cups, Erlitou sees the appearance of jue and he wine-ritual vessels.',
        'Record typical vessel assemblages rather than single pieces: the artifact group of one unit (pit layer) locates the culture period and relative age far better than a single piece.',
        'Cultural attribution of one cord-marked grey sherd',
        'The sherd is fine-paste grey pottery, decorated with vertical cord marks, identifiable as the foot of a pouch-legged li-tripod. The pouch-legged cord-marked li is typical of the late Longshan to early Erlitou of the Central Plains; combined with the excavated layer it can be preliminarily placed in the Longshan–Erlitou transition, then confirmed by C14 for absolute age.',
        'Can a single sherd determine the culture period?',
        'No. A single sherd only gives a possible range; it must be judged together with the layer, the coexisting vessel assemblage and dating data. Typology relies on standard typology — comparing against standard vessels from typical units.',
        'Are painted pottery and polychrome pottery the same?',
        'No. Painted pottery is typical of the Yangshao culture: mineral pigments painted in black/red on fine-paste red pottery and then fired. Painted-over pottery (e.g. some Eastern Zhou, Han) is painted after firing and easily flakes. Their color, craft and era differ, so record them separately.',
        'About "pottery typology"',
        'Pottery typology is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.',
        'Search culture / fabric / decoration / vessel form...',
    ]))

    # ===== site-grid (29) =====
    write('site-grid', build('site-grid', [
        '🧮 Site test-pit calculation',
        'Compute the number of test pits, excavation area and each pit coordinate by site extent and pit specification (southwest corner as origin, north as +X, east as +Y)',
        '📖 View "Site test-pit calculation user guide"',
        'Compute the number of test pits, excavation area and southwest-corner coordinate grid by site extent and pit specification (common 5×5m or 10×10m), generating a pit-numbering scheme. Calculation runs locally in the browser; data is not uploaded to the server.',
        'Site north-south length L (m)',
        'Site east-west width Wd (m)',
        'Pit side length S (m)',
        'Balk width G (m)',
        'Origin numbering start',
        'From T1',
        'From T0',
        'Numbering direction',
        'Row-first then column (west→east, south→north)',
        'Column-first then row (south→north, west→east)',
        'Copy coordinate table',
        'Test-pit coordinate table',
        'Note: each pit main excavation area is S×S, with a balk of width G reserved between adjacent pits; total footprint spreads by rows and columns, excavation area excludes balks. Balks are excavated after the main area as needed.',
        '📚 In-depth: site test-pit calculation',
        'When laying out pits, set the pit specification (common 5×5m or 10×10m) by site extent and excavation plan, compute the required pit count and total excavation area, and arrange pit numbering.',
        'Build a unified coordinate grid: take the site southwest corner as origin, north as +X, east as +Y, mark each pit southwest-corner coordinate (e.g. T0503 = X50 Y30) in the pit register.',
        'For rectangular sites use the ceil-plus-boundary method: rows=ceil(north-south length/spec), cols=ceil(east-west width/spec), then subtract corner pits fully outside the site.',
        '100m×60m site with 5m pits',
        'Cols=ceil(100/5)=20, rows=ceil(60/5)=12, total pits=20×12=240, excavation area=240×25=6000 m². The southwest first pit is marked T0000 (or T0101 by convention); column number increases eastward, row number increases northward.',
        'What does pit number T0503 mean?',
        'In the common convention the digits after T denote the X, Y coordinate grid of 10m/5m. E.g. under 5m pits T0503 means the southwest corner is at X=50m, Y=30m; the exact digit count and origin follow that site field "Excavation Plan".',
        'Why keep pit specification uniform?',
        'Uniform specification eases horizontal comparison of layers, artifact context units and area statistics, and later coordinate replay in GIS. Different specs make layers and artifact density incomparable.',
        'About "site test-pit calculation"',
        'Site test-pit calculation is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.',
    ]))

    # ===== stats-density (20) =====
    write('stats-density', build('stats-density', [
        '📊 Artifact density (pieces / m²) statistics',
        'pieces / m²',
        '📖 View "Artifact density (pieces / m²) statistics user guide"',
        'Artifact density = recovered count ÷ exposed area (pieces/m²); total density = Σcount ÷ Σarea',
        'Enter one test pit / sampling unit per line: recovered count, exposed area (m²). The tool aggregates and computes total density and per-unit density, for comparing layer deposit richness.',
        'Each pit data (per line: count, area m²)',
        'Compute density',
        '📚 In-depth: artifact density (pieces / m²) statistics',
        'Compare the deposit richness of different layers or pits: divide recovered count by excavation area to get artifact density (pieces/m²); a higher-density layer usually means more frequent activity or thicker deposit.',
        'Standardized sampling: when pit excavation areas differ, must convert to unit-area density before comparing, not compare counts directly.',
        'Locate ash pits, house floors and other activity surfaces via density anomaly zones: a local density spike often points to abandoned deposit or a specific functional area.',
        'Two-layer density comparison',
        'Pit T0503 layer ③ excavation area 25 m² recovered 150 sherds, density=150/25=6.0 pieces/m²; layer ④ area 25 m² recovered 40, density=1.6 pieces/m². Layer ③ density is about 3.75× that of ④, suggesting ③ had higher activity intensity or richer deposit.',
        'Does low artifact density mean an unimportant layer?',
        'Not necessarily. Density is affected by preservation, plough disturbance, excavation area and screening method (whether floated, sieve aperture). A low-density layer may be a living floor later destroyed, or small pieces lost due to no flotation; judge with deposit nature.',
        'Why do some reports use pieces / m³?',
        'For 3D deposits like post pits and ash pits, besides planar density (pieces/m²) they also use volumetric density (pieces/m³) to describe deposit content. The units differ; when citing, always note the denominator (area or volume), otherwise incomparable.',
        'About "artifact density (pieces / m²) statistics"',
        'Artifact density (pieces / m²) statistics. Free online tool, pure front-end processing, data not uploaded, privacy and security protected.',
        'Example: 150,25\n40,25\n80,30',
    ]))

    # ===== stratum-identify (22) =====
    write('stratum-identify', build('stratum-identify', [
        '🔍 Stratum identification',
        'Comparison of archaeological stratum ages and features, covering geological ages and major Chinese archaeological culture periods',
        '📖 View "Stratum identification user guide"',
        'Compare geological ages and major Chinese archaeological culture-period features to aid site stratigraphic division, superposition–cutting relation judgment and relative-age positioning. Compiled from public archaeological literature for study reference only.',
        'All ages',
        'Geological age',
        'Paleolithic',
        'Neolithic',
        'Tip: stratum deposits generally follow the "late on top, early at bottom" sequence principle; the superposition and cutting relations between features are key to judging relative age.',
        '📚 In-depth: stratum identification',
        'When dividing site strata, order by superposition–cutting relations: the upper layer is later than the lower, the cut unit is later than the one cutting it.',
        'Position by combining geological age and archaeological culture period: e.g. Holocene strata mostly correspond to Neolithic and later, Pleistocene deposits mostly Paleolithic; anchor the culture period with typical artifacts (stone industry, pottery).',
        'Record the sterile/ cultural-soil boundary: sterile soil is natural deposit untouched by human activity; its top surface is often an important reference for the earliest bottom of a site human activity.',
        'A set of superposition relations for dating',
        'In the test pit layer ② (plough soil) overlies layer ③ (Ming-Qing), layer ③ overlies layer ④ (Song-Yuan), below ④ is sterile soil. By the "lower earlier, upper later" principle: ④ earlier than ③ earlier than ②; ④ yielded Song-Yuan porcelain and ③ yielded Ming-Qing blue-and-white, mutually confirming, sequence consistent with culture period.',
        'What is the difference between stratigraphic and typological dating?',
        'Stratigraphy dates relative order by the upper-lower superposition and cutting relations; typology dates culture-period order by artifact morphological evolution. The two verify each other: if typology shows upper-layer artifacts earlier, it is mostly disturbance or later intrusive soil, recheck the layer.',
        'What is sterile soil? Why important?',
        'Sterile soil is natural deposit never turned by humans (e.g. alluvial, slope wash); its top marks the earliest bottom boundary of a site human activity. Finding sterile soil means the pit deposit is excavated to the bottom — an important basis for ending a pit.',
        'About "stratum identification"',
        'Stratum identification is an online tool in the scientific research field. A scientific research tool using standard scientific formulas for accurate calculation.',
        'Search stratum / culture / feature / remains...',
    ]))

    print('body_archaeology_b2 done')

if __name__ == '__main__':
    main()
