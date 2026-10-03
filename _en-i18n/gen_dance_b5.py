#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'dance')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'dance')
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
    out = {'slug': slug, 'industry': 'dance', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
# -*- coding: utf-8 -*-
def main():
    write('partner-distance', build('partner-distance', [
        '📏 Partner Spacing Calculator',
        'Compute optimal partner spacing and movement path radius from arm span and dance style',
        'Core formula (from input variables): min(100,(optimalDist÷maxReach)×100); max(5,optimalDist); optimalDist÷2',
        '📖 Read the "Partner Spacing Calculator User Guide"',
        'Leader arm span (cm)',
        'Follower arm span (cm)',
        'Dance style',
        'Rumba',
        'Swing dance',
        'Standard ballroom',
        'Movement type',
        'Closed hold',
        'Open hold',
        'Side position',
        'Pivot position',
        'Clearance (cm)',
        '📋 Spacing reference by dance style',
        'Closed spacing (cm)',
        'Open spacing (cm)',
        'Upper bodies close',
        'Closest',
        'Flexible and versatile',
        'Reserved and graceful',
        'Springy and lively',
        'Optimal spacing = average of the two arm spans × hold coefficient − clearance; path radius = spacing ÷ 2. Actual spacing should be adjusted to personal comfort.',
        '📚 Deep dive: partner spacing calculation',
        'Hold spacing: compute a comfortable distance from both arm spans and the dance style hold, avoiding being too close or too far.',
        'Path radius: derive the movement path radius from spacing during rotations and travel steps, for blocking planning.',
        'Height difference compensation: slightly adjust spacing when the height difference is large to keep the frame stable.',
        'Waltz spacing example',
        'Both arm spans 170 cm, waltz closed hold → optimal spacing about 45 cm, rotation path radius about 60 cm, high comfort index; if the height difference is 12 cm, increase spacing by about 5 cm.',
        'Does dance style affect spacing?',
        'Yes. Different dance styles have different hold distances and frames, so pick the matching style.',
        'How is height difference handled?',
        'You can reflect the height difference in the parameters, and the tool gives the compensated spacing suggestion.',
        'Are the results accurate?',
        'They are geometric estimates; in practice the live feel between the two dancers is the reference.',
        'About "Partner Spacing Calculator"',
        'The Partner Spacing Calculator computes optimal spacing, movement path radius and comfort index from both arm spans and the dance style hold.',
        'Multiple dance styles and hold types',
        'Spacing visualization',
        'Path radius calculation',
        'Comfort index assessment',
        'Partner dance spacing planning',
        'Dance teaching positioning',
        'Rotation path design',
        'Hold adjustment',
        'How to use the Partner Spacing Calculator',
        'Used for partner dance blocking, rotation path radius estimation and height difference compensation.',
        'What does the Partner Spacing Calculator do?',
        'The Partner Spacing Calculator finds the optimal partner spacing and movement path radius from arm span and dance style, assisting partner work and blocking.',
        'How do I use the Partner Spacing Calculator?',
        'What scenarios suit the Partner Spacing Calculator?',
    ]))

    write('rotation-stability', build('rotation-stability', [
        '🖼️ Spin Stability Calculator',
        'Assess dance spin turns, angular velocity and body stability, and predict dizziness risk',
        '📖 Read the "Spin Stability Calculator User Guide"',
        'Angular velocity ω = 2π × turns ÷ duration(seconds), rotation rate rpm = turns ÷ duration × 60; rotation radius r is about height × 0.25 (center of gravity to rotation axis), rim linear speed v = ω × r; angular momentum L = I × ω, where moment of inertia I ≈ m × r²; tightening the limbs reduces I and raises ω (angular momentum conservation), improving spin stability; stability margin is positively correlated with ω and r and negatively correlated with move difficulty.',
        'Number of turns',
        'Spin duration (seconds)',
        'Spin type',
        'Spot rotation (head stays, then whips)',
        'Traveling spin',
        'Chain spin (continuous)',
        'Ballet pirouette',
        'Beginner (0-1 year)',
        'Intermediate (1-3 years)',
        'Advanced (3-5 years)',
        'Professional (5+ years)',
        '📋 Spin stability reference',
        'Turns / 4 s',
        'Angular velocity (rad/s)',
        'Needs support',
        'Entry level',
        'Basically stable',
        'Fairly stable',
        'Highly stable',
        'Angular velocity ω = 2π × turns ÷ duration; the stability index combines angular velocity, training level and spin type. The spot technique lowers dizziness risk by about 30%.',
        '📚 Deep dive: spin stability calculation',
        'Single spin: from turns and duration compute',
        'angular velocity',
        'and judge spin intensity.',
        'Stability assessment: evaluate the stability margin together with training level and indicate whether the spin is controllable.',
        'Dizziness risk: consecutive turns accumulate angular velocity exposure, so suggest intervals and protection.',
        'Spin stability example',
        '3 turns in 2 seconds → angular velocity about 9.4 rad/s; an intermediate trainee is stable and in control, while beginners should start with single turns and limit consecutive turns.',
        'How is angular velocity computed?',
        'Angular velocity = turns × 2π ÷ spin duration.',
        'Do consecutive spins cause dizziness?',
        'Multiple consecutive turns accumulate dizziness risk, so take intervals and fix on a spotting point.',
        'Can the results guide training?',
        'They are safety notes only and do not replace professional dance or fitness coaching.',
        'About "Spin Stability Calculator"',
        'The Spin Stability Calculator computes angular velocity from turns and duration and assesses body stability and dizziness risk together with training level.',
        'Angular and linear velocity calculation',
        'Stability index visualization',
        'Dizziness risk assessment',
        'Supports multiple spin types',
        'Dance spin training planning',
        'Choreography spin design',
        'Spin technique assessment',
    ]))


if __name__ == '__main__':
    main()
