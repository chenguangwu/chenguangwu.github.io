#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'film')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'film')
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
    out = {'slug': slug, 'industry': 'film', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------- index (21) ----------
    slug = 'index'
    en = [
        '🎞️ Film & Video Tools',
        'Film & Video',
        'Film & Video Tools',
        'Editing Timecode Converter',
        'SMPTE timecode converter. Converts between HH:MM:SS:FF timecode, frames and seconds, supports different frame rates, and suits precise marking and footage locating in film editing.',
        'Editing Timecode (Hours/Minutes/Seconds/Frames) Converter',
        'Online video timecode converter supporting hours:minutes:seconds:frames (with different frame rates) and total-frame/second mutual conversion, for edit marking, subtitle alignment and project collaboration; runs purely in the browser.',
        'Film aspect-ratio converter, supporting landscape/portrait frame conversion, cropping and letterbox parameter calculation, for unifying output specs before multi-platform video publishing.',
        'Render Time Estimator',
        '3D render time estimator. Input frame count, per-frame render time, render node count and retry rate to quickly estimate project wall-clock duration, node load and delivery schedule.',
        'Color Grading LUT Reference',
        'Look up common LUT types, applicable color spaces and typical grading parameters; the tool helps editors pick a suitable look preset in a quick-reference table format.',
        'Input VFX shot count, complexity level, average shot length and team parameters to estimate project labor and budget, supporting quick schedule and cost checks before quoting.',
        'About "Film & Video Tools"',
        'The Film & Video Tools collection includes 6 free online tools covering common calculation, conversion and lookup needs in film and video scenarios. Whether you are a professional, student or general user, you can find ready-to-use mini tools here. All tools run purely in the browser; no data is uploaded to servers, protecting your privacy.',
        'The film & video tools featured on this page include (representative samples):',
        'These tools help you quickly complete common film & video tasks without memorizing complex formulas or manual conversions—just enter to get results.',
        'Do the film & video tools need download or registration?',
        'No. All film & video tools on this page are pure front-end online tools—open the page and use them directly, no software install, no account registration, and no data upload.',
        'Are the film & video tools’ results accurate? Is the data safe?',
        'The tools compute locally in your browser based on public mathematical formulas and general industry standards, with results available instantly. All calculations are done on your device; data is never uploaded to servers, ensuring privacy and security.',
    ]
    write(slug, build(slug, en))

    # ---------- render-time (27) ----------
    slug = 'render-time'
    en = [
        '🔮 3D Render Time Estimator',
        'Estimate total render duration from frame count, per-frame render time, parallel nodes and retry rate, with schedule suggestions by daily working hours.',
        'Render Time Estimator',
        '/ Render Time Estimator',
        'Total render hours = frames × (1 + retry rate) × per-frame time (minutes) / 60; actual time = total render hours / node count',
        'Render Parameters',
        'Per-Frame Render Time (minutes)',
        'Render Node Count',
        'Source Frame Rate (fps)',
        'Advanced Options',
        'Daily Working Hours',
        'Failure Retry Rate (%)',
        'Estimation Notes:',
        'Total render hours = frames × (1 + retry rate) × per-frame time (minutes) / 60; node parallelism spreads the above total duration by node count. The retry rate reflects the re-run cost caused by failed re-renders; a baseline value is given from historical projects first.',
        'Common Render Scenario References',
        '📚 In-Depth Analysis: Render Schedule and Node-Load Estimation',
        'Before project quoting, estimate wall-clock duration from frame count, per-frame render time and node count to judge whether delivery can be met.',
        'Convert schedule days by daily working hours to arrange render scheduling and delivery milestones.',
        'Evaluate the gain of adding nodes or raising per-frame efficiency: compare schedule differences under different configurations.',
        'Render schedule for 3000 frames',
        'Total frames 3000, per-frame 4 min, 5 nodes, frame rate 24 fps, 12 working hours/day, failure retry rate 10%: effective frames = 3000 × 1.10 = 3300 frames; total render time = 3300 × 4 = 13200 min = 220 hours; wall-clock time = 220 ÷ 5 = 44 hours; schedule = 220 ÷ 12 ≈ 18.3 days; finished length = 3000 ÷ 24 = 125 s (≈ 2.1 min). If nodes are increased to 10, wall-clock drops to 22 hours, but total machine-hours and cost stay the same—only faster delivery.',
        'What retry rate should I enter?',
        'Enter by the failed-frame ratio of historical projects, commonly 5–15%. Complex scenes (heavy hair/fur, volumetric light, displacement) fail easily, use a higher value; simple scenes use a lower value.',
        'Why does adding nodes halve wall-clock time but not the schedule days?',
        'Schedule is computed by total machine-hours ÷ daily working hours, independent of node count; wall-clock time is total machine-hours ÷ node count. Adding nodes shortens waiting time, not total workload.',
        'About "Render Time Estimator"',
        '3D render time estimator, computing total render time and completion date from frame count, per-frame render time and parallel nodes. A design/creative tool with visual operation and one-click CSS code generation.',
    ]
    write(slug, build(slug, en))

    # ---------- vfx-shot (43) ----------
    slug = 'vfx-shot'
    en = [
        '💰 VFX Shot Duration and Cost Estimator',
        'Estimate VFX production duration and budget from shot count, complexity level, average shot length and team size, supporting schedule discussion and quote review.',
        'Key formula (by input variables): totalSeconds ÷ 60; totalHours ÷ 8',
        '/ VFX Shot Calculator',
        'Estimate VFX production duration and budget from shot count, complexity level, average shot length and team size, supporting schedule discussion and quote review.',
        'Shot Parameters',
        'Total Shot Count',
        'Average Shot Length (seconds)',
        'Complexity Level',
        'Simple (cleanup / patch)',
        'Medium (composite / greenscreen)',
        'Complex (CG creature / environment)',
        'Hard (particles / fluid / destruction)',
        'Extreme (full CG / character animation)',
        'Cost Parameters',
        'Work Hours per Shot (hours)',
        'Team Size',
        'Daily Wage per Person (CNY)',
        'Complexity Coefficient:',
        'Simple ×1.0, Medium ×1.5, Complex ×2.8, Hard ×5.0, Extreme ×8.0. Higher complexity multiplies the work hours and cost per shot.',
        'VFX Complexity Reference',
        '📚 In-Depth Analysis: VFX Shot Duration and Cost Estimation',
        'Post-production film teams commonly use this estimate to build a "shot caliber + cost caliber" before quoting, to judge whether the schedule is controllable.',
        'Grouping by shot type (cleanup / greenscreen / CG / particles / destruction / character) then calculating quickly identifies high-risk shots and over-budget factors.',
        'In cross-team review, unifying the complexity coefficient and per-person daily-wage caliber avoids inconsistency between departments on the same project.',
        'Estimation Example',
        'Input 30 shots, 4 s per shot, complexity = Complex (2.8), 6 base work hours per shot, 8-person team, daily wage 1600 CNY: project labor = 504 h, project schedule ≈ 7.9 days, project budget ≈ 84,000 CNY.',
        'Cost-Reduction Optimization Example',
        'Do a tech preview early for high-complexity shots; after optimizing to medium process, the complexity coefficient can drop from 5.0 to 3.5, quickly simulating and comparing schedule and budget differences across plans.',
        'How should the complexity coefficient be annotated?',
        'It is recommended to define a standard table first, classify by historical shot deliverables (cleanup, composite, CG creature, character animation, etc.), then take the average correction value of samples from the last 3–5 months.',
        'Can this result be used directly as the final quote?',
        'It can serve as a technical preliminary estimate. Before formal quoting, overlay rework rate, approval rate, review turnaround and management buffer, then submit the commercial version.',
        'About "VFX Shot Duration and Cost Estimator"',
        'This tool estimates VFX project labor and budget from shot count, complexity, average length and team configuration, helping you quickly form a discussable schedule and cost caliber before quoting.',
        'Supports tiered complexity estimation and team-size scaling to quickly compare multiple schedule plans',
        'Outputs total labor, project schedule and person-day cost by shot count and average length',
        'Provides "cost per shot / cost per second" for internal checking and reimbursement review',
        'Runs purely in the browser; no business footage or parameters need to be uploaded',
        'Film project quoting and schedule-meeting assessment',
        'Quick caliber check before budget review',
        'Reuse a unified cost caliber when communicating across departments',
        'Schedule estimation under rework and delivery pressure',
    ]
    write(slug, build(slug, en))


if __name__ == '__main__':
    main()
