#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'glass')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'glass')
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
    out = {'slug': slug, 'industry': 'glass', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))

#!/usr/bin/env python3


def main():
    write('annealing-curve', build('annealing-curve', [
        '🪟 Glass Annealing Curve Calculator',
        'Computes the annealing curve from glass thickness and type: soak temperature, soak time, critical-range slow cooling rate and fast cooling rate, and estimates the total annealing time.',
        'Core formula (by input variables): max(15,Math.round(4×t)); g.AP+5',
        '📖 View the guide to glass annealing curve calculation',
        'Soda-lime glass (window glass)',
        'Borosilicate glass (heat resistant)',
        'Lead glass (crystal)',
        'Potash-soda glass',
        'Cooling upper limit temperature (°C)',
        'Calculate annealing curve',
        '📋 Annealing Principles',
        'Annealing Point (AP):',
        'The temperature at which glass stress is relieved within a few minutes, at a viscosity of about 10¹² to 10¹³ Pa·s.',
        'Strain Point (SP):',
        'Below this temperature stress is no longer relieved; it is the lower limit for slow cooling.',
        'Three stages of annealing:',
        '① heat to the annealing point and soak (relieve stress); ② cool slowly through the critical AP→SP range (prevent stress from forming again); ③ below SP, cooling can be faster.',
        'Slow cooling rate:',
        'Inversely proportional to the square of the thickness, rate = K / t² (°C/min), where K varies by glass. Thick glass must be cooled extremely slowly.',
        'Reference points: soda-lime glass AP ≈ 545°C / SP ≈ 515°C; borosilicate AP ≈ 560°C / SP ≈ 510°C; lead glass AP ≈ 445°C / SP ≈ 415°C; potash-soda AP ≈ 525°C / SP ≈ 495°C.',
        '📚 In-depth: glass annealing curve calculation',
        'Annealing process: set the soak temperature, soak time and critical-range slow cooling rate by glass type and thickness',
        'Stress control: slow cooling from the annealing point (AP) to the strain point (SP) removes residual stress and prevents spontaneous cracking',
        'Scheduling: estimate the total annealing time from the fast cooling rate to plan furnace loads and cycle time',
        'Algorithm: soak temperature = annealing point AP + 5°C, soak time = max(15, round(4 × t)) minutes (t is thickness in mm); critical slow cooling rate Ks / t² °C/min (× 60 for °C/h), slow cooling duration = (AP − SP) / slow rate; fast cooling rate Kf / t² °C/min (capped at 60), fast cooling duration = (SP − final cooling temperature) / fast rate; total annealing time = soak + slow cooling + fast cooling. Requires thickness > 0 and a valid final cooling temperature.',
        'Example 1 (soda-lime glass t = 6 mm, cooling to 50°C): AP = 545, SP = 515, Ks = 4.2, Kf = 18 → soak 550°C / 24 min; slow cooling 4.2 / 36 = 0.1167°C/min = 7.0°C/h, slow duration (545 − 515) / 0.1167 = 257 min; fast cooling 18 / 36 = 0.50°C/min, fast (515 − 50) / 0.5 = 930 min; total 24 + 257 + 930 = 1211 min = 20 h 11 min. Example 2 (borosilicate glass t = 10 mm, cooling to 30°C): AP = 560, Ks = 3.5, Kf = 20 → soak 565°C / 40 min; slow cooling 3.5 / 100 = 0.035°C/min = 2.1°C/h, slow 50 / 0.035 = 1429 min; fast cooling 20 / 100 = 0.20°C/min, fast 480 / 0.2 = 2400 min; total 3869 min = 64 h 29 min.',
        'Why cool slowly through the critical range?',
        'AP → SP is the range where glass changes from a viscoelastic state to a rigid one and stress can still relax; slow cooling lets internal stress release along the temperature gradient, while fast cooling freezes in thermal stress that later causes spontaneous cracking. The slow cooling rate is inversely proportional to the square of the thickness — the thicker, the slower.',
        'How do parameters differ between glass types?',
        'Soda-lime, borosilicate, lead and potash-soda glasses differ in annealing point AP, strain point SP and the Ks / Kf coefficients (for example soda-lime AP = 545°C, borosilicate AP = 560°C, lead glass AP = 445°C), which set the soak temperature and slow cooling rate; at the same thickness, borosilicate cools more slowly and takes longer overall because Ks is smaller.',
        'About glass annealing curve calculation',
        'Glass annealing curve calculation is an online tool in the business and office field. Business and office tools improve efficiency, and data is processed locally to protect privacy.',
    ]))

    write('cutting-score', build('cutting-score', [
        '🧮 Glass Cutting Calculator',
        'Computes how many small pieces can be cut from a sheet, the number of cuts, the total cutting length and utilization, and recommends scoring pressure by thickness',
        'Core formula (by input variables): best.nx×pw+(best.nx-1)×k; best.ny×ph+(best.ny-1)×k; usedArea÷sheetArea×100',
        'Sheet width W (mm)',
        'Sheet height H (mm)',
        'Glass thickness (mm)',
        'Piece width w (mm)',
        'Piece height h (mm)',
        'Kerf / waste (mm)',
        'Calculate layout',
        '📋 Cutting Reference',
        'Layout count:',
        'Nx = floor((W + kerf) / (piece width + kerf)), and Ny likewise; both orientations are tried automatically and the better one is used.',
        'Number of cuts:',
        'Horizontal cuts = Nx (cut Nx strips along the height, or Ny segments), vertical likewise; total cuts ≈ (Nx + Ny − 2).',
        'Scoring pressure reference:',
        '2 mm about 4 to 5 kg, 3 mm about 5 to 6 kg, 5 mm about 6 to 8 kg, 8 mm about 8 to 10 kg, 10 mm about 10 to 12 kg. The thicker the glass, the larger the wheel angle.',
        'After scoring, apply even force along the score line to break it off; thick plates can use dedicated breaking pliers.',
        '📚 In-depth: glass sheet cutting layout and utilization',
        'Cutting optimization: given sheet and piece sizes, find the piece count and the most economical layout direction',
        'Cost estimation: estimate material and labor from utilization, number of cuts and total length',
        'Equipment settings: recommend scoring pressure (wheel load) by thickness',
        'Algorithm: single-direction layout nx = floor((sheet width + kerf) / (piece width + kerf)), ny = floor((sheet height + kerf) / (piece height + kerf)), pieces = nx × ny; compare the normal orientation with the one rotated 90° and take the larger. Utilization = (pieces × piece area) / (sheet area) × 100; cuts = nx + ny − 2; total cutting length = nx × sheet height + ny × sheet width; scoring pressure by thickness lookup (2 → 4.5, 5 → 7, 8 → 9, 12 → 12.5 kg and so on). Requires all sizes > 0 and kerf ≥ 0.',
        'Example 1 (sheet 1830 × 1220 × 5 mm, pieces 400 × 300, kerf 3 mm): normal nx = floor(1833/403) = 4, ny = floor(1223/303) = 4 → 16 pieces; rotated 90° nx = floor(1833/303) = 6, ny = floor(1223/403) = 3 → 18 pieces, so 18 rotated pieces are used; utilization 18 × 400 × 300 / (1830 × 1220) × 100 = 96.7%; cuts 6 + 3 − 2 = 7, total length 6 × 1220 + 3 × 1830 = 12810 mm = 12.81 m; pressure (T = 5) = 7.0 kg. Example 2 (sheet 2440 × 1830 × 8 mm, pieces 500 × 600, kerf 4 mm): both orientations give 12 pieces; utilization 12 × 500 × 600 / (2440 × 1830) × 100 = 80.6%; 5 cuts, total length 14.64 m; pressure (T = 8) = 9.0 kg.',
        'Why can rotating 90° give more pieces?',
        'When the aspect ratio of the piece does not match the sheet, switching orientation fits in more columns or rows; this tool computes both orientations and takes the better one, which can raise utilization by 5% to 15%. The kerf (saw cut or breakage loss) must also be counted in every gap, otherwise the piece count comes out too high.',
        'How should scoring pressure be chosen?',
        'Wheel load grows with thickness (2 mm ≈ 4.5 kg, 5 mm ≈ 7 kg, 8 mm ≈ 9 kg, 12 mm ≈ 12.5 kg); too little leaves a shallow score that is hard to break, too much causes edge chipping; thin glass needs tighter pressure control together with cutting oil and wheel speed.',
        'About glass cutting calculation',
        'Glass cutting calculation is an online tool in the business and office field. Business and office tools improve efficiency, and data is processed locally to protect privacy.',
    ]))

    write('snell-refraction', build('snell-refraction', [
        '🧮 Refractive Index Calculator',
        'Computes the refraction angle and the critical angle for total internal reflection from Snell’s law, with a refractive index table for common media',
        'Core formula (by input variables): Math.asin(sinT)×180÷π; n1×Math.sin(rad)÷n2; a1×π÷180',
        '🧮 Refractive Index Calculator',
        'Incident medium n₁',
        'Air (1.0003)',
        'Water (1.33)',
        'Crown glass (1.52)',
        'Flint glass (1.62)',
        'Acrylic (1.49)',
        'Diamond (2.42)',
        'n₁ value',
        'Refracting medium n₂',
        'n₂ value',
        '📋 Refractive Index of Common Media',
        'Snell’s law:',
        'n₁ · sinθ₁ = n₂ · sinθ₂, so θ₂ = arcsin(n₁ · sinθ₁ / n₂).',
        'Total internal reflection:',
        'When n₁ > n₂ and the angle of incidence exceeds the critical angle θc = arcsin(n₂/n₁), total internal reflection occurs and light does not enter n₂.',
        'Dispersion:',
        'The refractive index varies with wavelength (for crown glass, n for blue light is greater than for red light), which causes dispersion (measured by the Abbe number Vd).',
        'Apparent depth:',
        'Viewing an object in water from air, apparent depth = real depth × (n₂/n₁) = real depth / 1.33, so objects in water look shallower.',
        '📚 In-depth: refractive index and Snell’s law',
        'Optical design: find the refraction angle from the two refractive indices and the angle of incidence, and judge the direction of bending',
        'Total reflection: determine the critical angle and total reflection conditions when light passes from a denser into a rarer medium',
        'Material reference: look up the refractive index and critical angle of common media (water, glass, diamond and so on)',
        'Algorithm: Snell’s law n₁ · sinθ₁ = n₂ · sinθ₂, refraction angle θ₂ = arcsin(n₁ · sinθ₁ / n₂); if n₁ · sinθ₁ / n₂ > 1 then total internal reflection occurs (no real refraction angle); the',
        'critical angle for total internal reflection',
        'θc = arcsin(n₂/n₁) exists only when n₁ > n₂ (light going from dense to rare). Requires n₁, n₂ > 0 and 0 ≤ θ₁ ≤ 90°.',
        'Example 1 (air n₁ = 1.0003 → water n₂ = 1.33, θ₁ = 30°): sinθ₁ = 0.5, sinθ₂ = 1.0003 × 0.5 / 1.33 = 0.3761, θ₂ = arcsin(0.3761) = 22.09° (light goes from rare to dense and bends toward the normal); air to water is rare to dense, so there is no critical angle. Example 2 (water n₁ = 1.33 → air n₂ = 1.0003, θ₁ = 50°): n₁ · sinθ₁ / n₂ = 1.33 × sin50° / 1.0003 = 1.0185 > 1 → total internal reflection; the',
        'critical angle θc',
        '= arcsin(1.0003/1.33) = 48.77° (consistent with the table value for water of 48.6°, which uses n = 1.333).',
        'When does a critical angle appear?',
        'A critical angle exists only when light travels from an optically denser medium into a rarer one (n₁ > n₂, such as looking at air from under water); beyond θc the light is totally reflected and no refracted ray exists. Going from rare to dense (such as air into water) gives refraction at every angle and no total reflection.',
        'Why is diamond so brilliant?',
        'Diamond has n = 2.42, so its critical angle to air is only arcsin(1/2.42) = 24.4°; even a small angle of incidence causes total internal reflection, so light reflects many times inside before leaving through the top face, and with high dispersion this produces fire. Window glass at n ≈ 1.52 has a critical angle of about 41° and rarely reflects totally.',
        'About refractive index calculation',
        'Refractive index calculation is an online tool in the business and office field. Business and office tools improve efficiency, and data is processed locally to protect privacy.',
        'Is this tool free?',
        'Completely free, with no registration — use it directly in the browser.',
        'Will my data be uploaded?',
        'No. All processing happens locally in the browser and data is never sent to any server.',
        'Does it work on mobile?',
        'Yes. The page is responsive and works on both phones and computers.',
    ]))

    write('thermal-bend', build('thermal-bend', [
        '🏋️ Glass Thermal Bending Parameter Calculator',
        'Computes bending temperature, soak time and bend arc length from glass thickness, bend angle and radius, and assesses process difficulty',
        'Core formula (by input variables): Math.round((5+difficulty×2)×t÷5×5); g.base+difficulty×25; g.soft-10',
        'Thermal bending parameter calculation',
        '/ Thermal Bending Parameters',
        'Bend angle A (°)',
        'Soda-lime glass',
        'Borosilicate glass',
        'Calculate thermal bending parameters',
        '📋 Thermal Bending Basics',
        'Bending temperature:',
        'Soda-lime glass softens at about 696°C, and the thermal bending (slump/bend) range is 580 to 710°C. Small angles and large radii use slump (590 to 640°C); large angles and small radii need bend (650 to 710°C).',
        'Bend arc length:',
        'L = R × θ (θ in radians), used for stock cutting and mold design.',
        'Minimum radius:',
        'The bend radius is generally R ≥ 2 to 3t (thickness); too small a radius easily causes stress concentration and optical distortion, and needs a special mold.',
        'Soak time:',
        'Depends on thickness and temperature, roughly 5 to 15 min/mm depending on difficulty. Borosilicate glass has a higher softening point (~820°C) and is bent at 700 to 760°C.',
        '📚 In-depth: glass thermal bending process parameter calculation',
        'Thermal forming: set the heating temperature, soak time and arc length from thickness, bend angle and radius',
        'Difficulty assessment: judge natural sag / mold bending / forced bending from the R/t ratio and the angle',
        'Failure warning: too small a radius indicates',
        'stress concentration',
        ', which needs a professional mold and slow cooling',
        'Algorithm: bend arc length L = R × θ (θ = A × π/180, A in degrees); radius-to-thickness ratio R/t; difficulty score = angle > 90° (+1), > 135° (+1), R/t < 6 (+1), R/t < 3 (+1); temperature = base + difficulty × 25 (capped at softening point − 10°C), soak time = round((5 + difficulty × 2) × t / 5 × 5) min; recommended minimum radius = 2.5t. Requires 0 < A ≤ 180 and t, R > 0.',
        'Example 1 (soda-lime t = 5 mm, A = 90°, R = 60 mm): arc length 60 × 1.5708 = 94.2 mm; R/t = 12.0; difficulty 0 (no triggers) → temperature 600 + 0 = 600°C, soak 25 min, natural sag (slump). Example 2 (borosilicate t = 4 mm, A = 150°, R = 10 mm): arc length 10 × 2.618 = 26.2 mm; R/t = 2.5; difficulty A > 90 (+1) + A > 135 (+1) + R/t < 6 (+1) + R/t < 3 (+1) = 4 → temperature 720 + 100 = 820, capped (softening 820 − 10) = 810°C, soak 52 min, forced bending (high difficulty).',
        'Why is the R/t ratio critical?',
        'R/t reflects the bend curvature: the smaller the ratio, the greater the curvature and the higher the tensile stress on the outer surface; R/t below 3 is high difficulty and needs a mold plus slow cooling, while R/t below 6 is already noticeably harder. The recommended minimum radius of 2.5t is an empirical lower limit against cracking.',
        'Why does the temperature rise with difficulty?',
        'Large angles and small radii mean more glass flow and stress, so a higher temperature (base + difficulty × 25°C) is needed to form against the mold; but it is capped at softening point − 10°C to avoid edge sag or runaway deformation.',
        'About thermal bending parameter calculation',
        'Thermal bending parameter calculation is an online tool in the business and office field. Business and office tools improve efficiency, and data is processed locally to protect privacy.',
    ]))

    write('thickness-selection', build('thickness-selection', [
        '📏 Glass Thickness Selection',
        'Recommends the minimum glass thickness by glass area / span and use case, ensuring strength and safety',
        'Core formula (by input variables): max(w,h); w×h÷1e6',
        'Glass width (mm)',
        'Glass height (mm)',
        'Window / daylighting',
        'Glass door',
        'Glass shelf',
        'Desktop / countertop',
        'Partition / guardrail',
        'Recommended thickness',
        '📋 Thickness Selection Reference Table',
        'Safety note:',
        'Doors, tables and countertops, guardrails, shower partitions and other parts involving personal safety should use',
        'tempered glass',
        '(3 to 5 times stronger, breaking into small blunt particles).',
        'The larger the area, the longer the span and the higher the wind pressure or load, the greater the required thickness.',
        'This tool gives empirical recommendations for ordinary civil use; real projects must verify strength and deflection according to the Technical Specification for Application of Architectural Glass, JGJ 113.',
        '📚 In-depth: architectural glass thickness selection',
        'Door and window selection: recommended minimum safe thickness for ordinary and tempered glass by area',
        'Guardrails and partitions: large spans or safety scenarios require tempered or laminated thickness',
        'Ordering basis: look up the table by area and maximum span to avoid failures from glass that is too thin',
        'Algorithm: area = width × height / 10⁶ (m²), maximum span = max(width, height) (mm); the minimum recommended thickness is looked up by scenario — windows: ≤ 0.8 m² → 3 mm, ≤ 1.5 → 4, ≤ 2.5 → 5, ≤ 3.5 → 6, ≤ 5 → 8, > 5 → ≥ 10 mm; glass doors: span ≤ 900 → 6 mm tempered, ≤ 1800 → 8, ≤ 2400 → 10, > 2400 → 12 mm tempered; shelves, desktops and partitions each have their own brackets. Non-window scenarios default to tempered. Requires dimensions > 0.',
        'Example 1 (window 800 × 1200 mm): area 960000 / 1e6 = 0.96 m², span 1200 mm; 0.96 > 0.8 and ≤ 1.5 → 4 mm ordinary glass is usable. Example 2 (glass door 1500 × 2000 mm): area 3.00 m², span 2000 mm; span ≤ 2400 → 10 mm tempered glass recommended (safety scenarios must use tempered).',
        'Why are the thickness rules different for windows and doors?',
        'Windows are sized by area (wind pressure and deflection grow with area) and ordinary glass can be used for daylighting; glass doors and guardrails involve personal safety, so they are sized by span and must be tempered or laminated, starting at 6 mm.',
        'Can the selection be used directly?',
        'This table is for quick estimation and ordering reference; real projects must verify wind pressure, deflection and impact according to the Technical Specification for Application of Architectural Glass; large panels, high-rise buildings or crowded areas should use a higher grade and laminated safety glass.',
        'About glass thickness selection',
        'Glass thickness selection is an online tool in the business and office field. Business and office tools improve efficiency, and data is processed locally to protect privacy.',
    ]))


if __name__ == '__main__':
    main()
