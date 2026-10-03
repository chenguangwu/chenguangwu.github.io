#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'decor')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'decor')
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
    out = {'slug': slug, 'industry': 'decor', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('scheduler', build('scheduler', [
        '⏱️ Construction Process Scheduling',
        'Automatically compute duration, total float and critical path by the Critical Path Method (CPM), and draw a Gantt chart.',
        'Construction (Process/Duration) Scheduling',
        '/ Construction Process Scheduling',
        '📖 View the User Guide for Construction Process Scheduling',
        'Start date',
        '+ Add process',
        'Load standard process template',
        'Export schedule table',
        'Process editing',
        'Process name',
        'Duration (days)',
        'Predecessor process',
        'Empty predecessor means start at project start; multiple processes can share the same predecessor to enable parallel work.',
        'Construction schedule Gantt chart',
        'Critical process',
        'Non-critical process',
        'In progress',
        'Using the Critical Path Method: earliest start ES = earliest finish of predecessor; latest start LS is back-calculated; total float = LS − ES, float 0 means critical process',
        'The critical path (all processes with zero float linked) determines total project duration; any critical-process delay postpones completion',
        'The standard template gives reference durations for common home decoration processes; adjust by workload and crew size in practice',
        '📚 Deep Dive: Construction Process Scheduling',
        'Whole-process home scheduling: enter demolition→plumbing→masonry→carpentry→painting→installation durations and dependencies to find the critical path and total duration.',
        'Parallel-process optimization: identify non-critical total float and flexibly insert idle waits like custom-furniture lead time without affecting total duration.',
        'Delay-impact assessment: when a process is delayed, check whether it lies on the critical path to judge the impact on the delivery date.',
        'Home serial duration',
        'Example: demolition 3d → plumbing 7d → masonry 10d → carpentry 8d → painting 6d (serial).',
        'What is the critical path?',
        'The longest process chain that decides total duration; any link delay postpones delivery; non-critical chains have float time.',
        'How to fill dependencies?',
        'Express order as predecessor → this process, e.g. plumbing must finish before masonry; parallel is shown by no dependency.',
        'Can the result be used as the contract duration?',
        'This tool estimates an ideal duration from input, excluding risks like weather/rework/material wait; allow a buffer and agree by contract in practice.',
        'About Construction Process Scheduling',
        'A project-scheduling tool for home decoration and small works, with built-in standard process templates, using the Critical Path Method to auto-compute duration, float and critical path, visualized as a Gantt chart.',
        'Critical Path Method auto-computation',
        'Total float and critical-path marking',
        'Gantt chart progress visualization',
        'Parallel processes supported',
        'Home process scheduling',
        'Small engineering project management',
        'Duration and critical-path analysis',
        'Construction progress tracking',
    ]))
    write('skirting-length', build('skirting-length', [
        '📏 Skirting & Cornice Length Calculator',
        'Compute skirting and cornice length, with door-opening deduction and construction waste',
        '📖 View the User Guide for Skirting & Cornice Length Calculator',
        'Skirting net length = room perimeter − total door width (window sills usually not deducted, except French windows); room perimeter = 2 × (room length + room width); purchase qty = net length × (1 + waste rate 5% to 8%); pieces = purchase qty ÷ single-piece length (common 2.4 m), rounded up; add 5 to 10 cm waste per corner and closure to avoid short-piece joins affecting appearance.',
        'Room dimensions',
        'Door count',
        'Single door width (m)',
        'Window count (bay/French window)',
        'Single window width (m)',
        'Material and waste',
        'Skirting waste rate (%)',
        'Cornice waste rate (%)',
        'Single skirting length (m)',
        'Single cornice length (m)',
        'Skirting total length (with waste)',
        'Cornice total length (with waste)',
        'Skirting',
        ': installed along the wall base, interrupted (not installed) at door openings; windows are usually not deducted (window sills with casing counted separately)',
        '• Skirting net length = room perimeter − total door width (windows not deducted)',
        'Cornice',
        ': installed around the top corners; still installed above door openings, so computed by full perimeter',
        '• At French/bay windows the cornice is computed by actual path; this tool estimates by full perimeter',
        '• Inside/outside corners and joints create waste; suggest a 5–10% waste rate',
        '• Solid-wood skirting suggests a higher waste rate for pattern alignment',
        '📚 Deep Dive: Skirting & Cornice Length Calculator',
        'Single-room skirting: enter four wall lengths and door width, subtract door from perimeter for net length, add 5% waste as needed.',
        'Multi-room roll-up: sum after per-room computation for unified purchase and fewer joints; watch corner-cut waste at outside corners.',
        'Irregular layout: measure bay/recess sections separately; approximate arcs by chord length or measure on site.',
        'Single-room skirting net length',
        'Example: room length 4 m, width 3 m, 1 door opening 0.9 m (sill not deducted).',
        'Why is the window sill not counted?',
        'Skirting runs along the floor; there is usually none at the window sill, so it is not deducted; only interruptions like door openings are deducted.',
        'How much waste to add?',
        'Straight room 3%–5%, many outside corners / irregular 5%–8%.',
        'How to handle inside/outside corners?',
        'Outside corners are best joined with a full piece cut at 45°; inside corners butt directly; corner cutting adds material, count it in the estimate.',
        'About Skirting & Cornice Length Calculator',
        'The Skirting & Cornice Length Calculator computes skirting and cornice usage by room dimensions, auto-deducting door openings and adding construction waste.',
        'Skirting and cornice computed separately',
        'Door and window openings auto-deducted',
        'Adjustable waste rate and single-piece length',
        'Decoration material purchase budget',
        'Wood-floor / tile matching skirting',
        'Top-corner cornice usage estimate',
        'Engineering material tally',
        'How to use the Skirting & Cornice Length Calculator',
        'Suitable for estimating skirting net length by each wall length and door width during decoration; sills not deducted, outside-corner cutting waste counted; results computed locally, not uploaded.',
        'What does the Skirting & Cornice Length Calculator do?',
        'Enter each wall length and door width; compute skirting net length by perimeter minus door openings (sills not deducted), easing material purchase and usage estimate.',
        'How to use the Skirting & Cornice Length Calculator?',
        'Which scenarios suit the Skirting & Cornice Length Calculator?',
    ]))
    write('wallpaper-quantity', build('wallpaper-quantity', [
        '📐 Wallpaper Quantity Calculator',
        'Compute required wallpaper rolls by wall size, wallpaper spec and pattern-match waste',
        '📖 View the User Guide for Wallpaper Quantity Calculator',
        'Wallpaper panels = total wall length ÷ panel width (common 0.53 m), rounded up; panels per roll = roll length ÷ (wall height + pattern-match waste, add 0.1–0.3 m per repeat for patterned) then floored; required rolls = panels ÷ panels per roll × (1 + waste rate 5% to 10%), rounded up; total wall length = room perimeter − total door/window width.',
        'Wall dimensions',
        'Total wall length (m)',
        'Wall height (m)',
        'Door/window deduction area (m²)',
        'Wallpaper spec',
        'Panel width (m)',
        'Roll length (m)',
        'Pattern repeat (m, 0 if no pattern)',
        'Construction waste rate (%)',
        'Wallpaper panels',
        '= total wall length ÷ panel width (rounded up)',
        'Usage per panel',
        '= wall height + pattern repeat (patterned needs one extra repeat per panel)',
        'Panels per roll',
        '= roll length ÷ usage per panel (floored)',
        'Required rolls',
        '= wallpaper panels ÷ panels per roll (rounded up, plus waste)',
        '• Door/window area is deducted; for complex shapes keep 1 extra roll',
        '• Buy one batch of the same color/pattern at once to avoid color difference',
        '📚 Deep Dive: Wallpaper Quantity Calculator',
        'Full-wall wallpapering: enter wall width/height and wallpaper width/length, get panels by wall height ÷ roll length rounded up × wall width ÷ panel width, then convert to rolls.',
        'Patterned wallpaper: a repeating pattern needs each panel aligned, add extra repeat waste, rolls go up.',
        'Multi-wall total: sum after per-wall computation, reserve 1–2 rolls of the same batch for replenishment to avoid color difference.',
        'Full-wall wallpaper rolls',
        'Example: wall width 3.6 m, height 2.7 m, wallpaper width 0.53 m, roll length 10 m, waste 5%.',
        'What is roll length?',
        'The usable length of a single roll (common 10 m/roll), deciding how many panels it can yield.',
        'How is pattern-match waste calculated?',
        'Wallpaper with a repeat wastes a segment per panel for alignment; add waste by repeat, usually one extra roll.',
        'Can you replenish the same color if short?',
        'Different batches easily show color difference; buy enough at once and keep 1–2 extra rolls; better extra than short.',
        'About Wallpaper Quantity Calculator',
        'The Wallpaper Quantity Calculator computes required rolls precisely by wall size, wallpaper width and roll length, combined with pattern repeat and construction waste.',
        'Pattern-repeat waste calculation supported',
        'Door/window area auto-deducted',
        'Adjustable construction waste rate',
        'Home decoration wallpaper purchase',
        'Engineering budget and material tally',
        'Patterned wallpaper waste estimate',
        'Usage estimate for rooms with many doors/windows',
        'How to use the Wallpaper Quantity Calculator',
        'Suitable for estimating required rolls and panels by wall size and wallpaper width/length before wallpapering, accounting for pattern waste and same-batch stock; results computed locally, not uploaded.',
        'What does the Wallpaper Quantity Calculator do?',
        'The Wallpaper Quantity Calculator computes required rolls and panels by wall size and wallpaper width, length and waste rate, assisting material prep and budget for wallpapering.',
        'How to use the Wallpaper Quantity Calculator?',
        'Which scenarios suit the Wallpaper Quantity Calculator?',
    ]))

if __name__ == '__main__':
    main()
