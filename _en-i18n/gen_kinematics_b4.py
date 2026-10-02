#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'kinematics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'kinematics')
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
    out = {'slug': slug, 'industry': 'kinematics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3

def main():
    # projectile-velocity-components (17)
    write('projectile-velocity-components', build('projectile-velocity-components', [
        "Horizontal and vertical components from initial speed and elevation",
        "Input initial speed v and elevation θ to find horizontal and vertical components.",
        "Projectile Velocity Components Calculator",
        "/ Projectile Velocity Components Calculator",
        '📖 View "Horizontal and Vertical Components from Initial Speed and Elevation Guide"',
        "Elevation θ (°)",
        '📚 In-depth: Projectile Velocity Components (v_x=v·cosθ, v_y=v·sinθ)',
        "Decompose initial speed into horizontal and vertical components.",
        "Foundation of ballistic analysis.",
        "Decompose the launch speed into horizontal and vertical components.",
        "v_x = 20×cos30 = 17.32 m/s, v_y = 20×sin30 = 10 m/s. Horizontal uniform motion, vertical under gravity.",
        "Initial speed 40 m/s, elevation 60°",
        "vₓ=v·cos60°=40×0.5=20.000 m/s; v_y=v·sin60°=40×0.866=34.641 m/s. Ignoring air resistance, the horizontal component stays constant throughout.",
        "Why compute components separately?",
        "Horizontal has no force (uniform), vertical has gravity (uniformly variable); separated, each is independent and kinematics formulas apply — the standard ballistic practice.",
        "Why does the horizontal component stay constant while the vertical changes?",
        "Ignoring air resistance, the horizontal direction has no force (acceleration 0), so vₓ is constant; the vertical direction is always under gravity, v_y decreases about 9.8 m/s each second, reaching 0 at the apex then increasing reversed. This tool gives the components at the instant of launch.",
    ]))

    # relative-velocity-1d (25)
    write('relative-velocity-1d', build('relative-velocity-1d', [
        "Relative velocity from two objects' velocities",
        "Input two objects' velocities v₁, v₂ to find relative velocity.",
        "1D Relative Velocity Calculator",
        "/ 1D Relative Velocity Calculator",
        '📖 View "Relative Velocity from Two Objects Velocities Guide"',
        "v_rel = v₁−v₂ (same direction).",
        '📚 In-depth: 1D Relative Velocity (v₁−v₂)',
        "Relative velocity of two objects on the same line.",
        "Overtaking/catching-up analysis.",
        "Find the relative velocity of two objects on the same straight line, judge catching-up and meeting.",
        "v₁=30, v₂=20 (same direction)",
        "v_r = 30−20 = 10 m/s. That is, the former approaches/recedes from the latter at 10 m/s.",
        "Front car 25 m/s, rear car 32 m/s",
        "v_rel=v₁−v₂=25−32=−7.000 m/s. If v₁ is defined as the front car, a negative value means the front car is approaching the rear car backward, i.e. the rear car is catching up.",
        "How to compute opposite directions?",
        "Take same direction as positive; opposite gives one positive one negative, v_r = v₁−v₂ still holds; a negative result means receding in opposite directions.",
        "How to interpret the sign?",
        "The sign depends on which object you take as reference. The tool computes v_rel=v₁−v₂: a positive result means object 1 recedes from object 2 along the positive direction. In practice, first set the positive direction, then substitute both velocities with their signs.",
        "How to use Relative Velocity from Two Objects Velocities",
        "What does Relative Velocity from Two Objects Velocities do?",
        "Input two objects' velocities v₁, v₂ on the same line, compute their relative velocity by v_rel = v₁ − v₂, commonly used for intuitive judgment in 1D kinematics scenarios like catching-up/meeting problems and reference-frame transformations.",
        "How to use Relative Velocity from Two Objects Velocities?",
        "What scenarios is Relative Velocity from Two Objects Velocities suitable for?",
        "1D relative velocity v_rel=v₁−v₂: the velocity of object 1 in the reference frame of object 2; the sign indicates direction (same/opposite).",
        "Same-direction motion subtracts relative velocities, opposite-direction adds; the result sign represents the relative motion direction. Commonly used for passing and chasing problems.",
    ]))

    # relativistic-velocity-add (21)
    write('relativistic-velocity-add', build('relativistic-velocity-add', [
        "Velocity composition in high-speed reference frames, never exceeds light speed.",
        "Relativistic Velocity Addition Calculator",
        "/ Relativistic Velocity Addition",
        "Relativistic velocity addition",
        '📖 View "Relativistic Velocity Addition Calculator Guide"',
        "u = (u′+v)/(1+u′v/c²). 0.6c+0.6c → 0.882c (subluminal).",
        "Object relative velocity u′ (c)",
        "Reference frame velocity v (c)",
        "Speed of light c (m/s)",
        "0.6c+0.6c → 0.882c (subluminal).",
        '📚 In-depth: Relativistic Velocity Addition',
        "Near light speed, velocities cannot be simply added.",
        "Subluminal motion composition.",
        "Compose two velocities in high-speed cases, ensuring the result does not exceed light speed.",
        "u = (0.6c+0.6c)/(1+0.6×0.6) = 1.2c/1.36 ≈ 0.882c. That is, two 0.6c added still less than c, not exceeding light speed.",
        "Two velocities each 0.5c, speed of light 3×10⁸ m/s",
        "u=(u′+v)/(1+u′v/c²)=(0.5+0.5)/(1+0.25)=0.800000 c, i.e. about 2.400×10⁸ m/s. Classical mechanics adding directly gives 1.0c, clearly violating relativity.",
        "Why not exceeding c?",
        "Classical addition gives 1.2c which is wrong; the relativistic denominator 1+u′v/c² corrects so the result is always < c, light speed cannot be surpassed.",
        "Why don't we feel this difference at everyday speeds?",
        "Because the correction term u′v/c² is extremely small. Taking two 350 km/h high-speed trains approaching each other as example, uv/c² is only about 10⁻¹² in magnitude, the difference between relativistic result and direct addition is far below any instrument's measurement error. Only when speed approaches light speed does the correction become significant.",
    ]))

    # rpm-to-radps (20)
    write('rpm-to-radps', build('rpm-to-radps', [
        "Angular velocity from revolutions per minute",
        "Input rotational speed n (rpm) to find angular velocity ω (rad/s).",
        "RPM to Angular Velocity Calculator",
        "/ RPM to Angular Velocity Calculator",
        '📖 View "Angular Velocity from Revolutions per Minute Guide"',
        '📚 In-depth: RPM to Angular Velocity (2πn/60)',
        "Convert rpm to rad/s for rotation calculations.",
        "Motor parameter conversion.",
        "Convert the commonly used engineering rotational speed",
        "to",
        "the",
        "required by physics calculation",
        "angular velocity",
        "ω = 2π×3000/60 ≈ 314.16 rad/s. That is, 3000 rpm is about 314 rad/s.",
        "Rotational speed 1500 rpm",
        "ω=2πn/60=2π×1500/60=157.080 rad/s. The motor nameplate 1500 rpm is about 25 turns per second.",
        "Why divide by 60?",
        "rpm is revolutions per minute; divide by 60 to get revolutions per second, then multiply by 2π to get rad/s.",
        "What is the conversion coefficient between rpm and rad/s?",
        "1 rpm=2π/60≈0.10472 rad/s, conversely 1 rad/s≈9.5493 rpm. For quick estimation remember \"multiply rad/s by 10 then subtract 5%\" to get roughly rpm; in this example 157.080×9.5493≈1500.",
    ]))

    # stopping-distance (21)
    write('stopping-distance', build('stopping-distance', [
        "Reaction distance plus deceleration braking distance.",
        "Braking Distance Calculator",
        "/ Braking Distance",
        "Braking distance",
        '📖 View "Braking Distance Calculator Guide"',
        "d = v₀t_r + v₀²/(2a). 100 km/h, reaction 1s, deceleration 7 → about 60 m.",
        "Reaction time t_r (s)",
        "100 km/h, reaction 1s, deceleration 7 → about 60 m.",
        '📚 In-depth: Braking Distance (v₀t_r + v₀²/2a)',
        "Total stopping distance including reaction distance.",
        "Safe following-distance evaluation.",
        "Add reaction distance and braking distance to evaluate total stopping distance.",
        "100km/h, reaction 1s, deceleration 7",
        "v₀=27.78 m/s, d = 27.78×1 + 27.78²/(2×7) = 27.78 + 55.1 ≈ 82.9 m. That is, about 83 m to stop.",
        "Vehicle speed 20 m/s, reaction time 1.5 s,",
        "braking deceleration",
        "Reaction distance=v₀·t_r=20×1.5=30.00 m; braking distance=v₀²/(2a)=400/10=40.00 m; total stopping distance=70.00 m. At 72 km/h you need about 70 m to stop.",
        "Is the reaction distance a large proportion?",
        "At 100km/h, reacting 1 s travels 27.8 m, about 1/3 of the total; fatigue/distraction significantly lengthens it, so keep distance.",
        "Why does braking distance become four times when speed doubles?",
        "Braking distance=v₀²/(2a), proportional to the square of speed. When speed goes from 20 to 40 m/s, the braking segment grows from 40.00 m to 160.00 m. This is also the fundamental reason high-speed driving must greatly increase following distance — danger does not grow linearly.",
    ]))

if __name__ == "__main__":
    main()
