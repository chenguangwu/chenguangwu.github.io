#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'optics')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'optics')
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
    out = {'slug': slug, 'industry': 'optics', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('angular-magnification', build('angular-magnification', [
        "Angular magnification of a simple magnifier from near point and focal length",
        "Enter the near point N and the magnifier focal length f to get the angular magnification.",
        "Magnifier Angular Magnification Calculator",
        "/ Magnifier Angular Magnification Calculator",
        "📖 Read the \"Angular magnification of a simple magnifier from near point and focal length\" guide",
        "The near point is usually taken as 250 mm.",
        "📚 Deep dive: magnifier angular magnification",
        "Estimating visual magnification of handheld magnifiers and microscope eyepieces.",
        "Back out an equivalent magnification from known focal length and near point.",
        "Compare the magnifying power of vision aids with different focal lengths.",
        "Focal length 25mm magnifier",
        "With near point N=250mm and focal length f=25mm: M=N/f=250/25=10×. That is, a 1mm object subtends the same angle as a 10mm object viewed by the naked eye at the near point.",
        "Focal length 50mm vision aid",
        "f=50mm: M=250/50=5×. A longer focal length gives a lower magnification and a steadier field, which suits long reading sessions.",
        "How does it differ from lateral magnification?",
        "Angular magnification compares visual angles (M=N/f), while lateral magnification compares image height to object height (m=-di/do); they apply in different situations.",
        "What happens if f is too short?",
        "M increases, but aberrations and distortion grow and the working distance shortens; ordinary low-vision magnifiers fall between 2× and 10×.",
        "How to use Angular Magnification of a Simple Magnifier from Near Point and Focal Length",
        "What does Angular Magnification of a Simple Magnifier from Near Point and Focal Length do?",
        "Enter the near point N (about 25 cm) and the focal length f of a simple magnifier and compute the angular magnification with M = N / f. Used to estimate the optical magnifying power of magnifiers and loupes.",
        "How do I use Angular Magnification of a Simple Magnifier from Near Point and Focal Length?",
        "Which scenarios suit Angular Magnification of a Simple Magnifier from Near Point and Focal Length?",
        "Angular magnification M=θ′/θ: the ratio of the angle θ′ the image subtends at the eye to the angle θ the object subtends at the near point, describing how much bigger a magnifier or eyepiece makes an object appear.",
        "Approximation",
        "For a simple magnifier M≈25 cm / f (f is the focal length in cm). M>1 gives an upright enlarged image; the angular magnification of a telescope is ≈−f_obj/f_eye.",
    ]))

    write('magnification-optics', build('magnification-optics', [
        "Lateral magnification (a negative sign means inverted).",
        "Optical Magnification Calculator",
        "/ Optical Magnification",
        "Optical Magnification",
        "📖 Read the \"Optical Magnification Calculator\" guide",
        "Image distance d_i (m)",
        "|M|>1 enlarges, <1 shrinks.",
        "📚 Deep dive: lateral (linear) magnification",
        "Determining image size and whether it is upright or inverted.",
        "Estimating image height in projection and enlargement systems.",
        "Computing the scale ratio of a real image.",
        "Object distance 30cm, image distance 15cm",
        "m=−di/do=−15/30=−0.5. The image height is half the object height and inverted (negative sign).",
        "Object distance 20cm, image distance 60cm",
        "m=−60/20=−3, an enlarged inverted real image.",
        "What does the negative sign mean?",
        "A negative sign indicates an inverted image; a positive sign (a virtual image) indicates upright.",
        "Confused with angular magnification?",
        "Lateral magnification m compares image height to object height, while angular magnification M compares visual angles; the units and physical meanings differ.",
    ]))

    write('malus-law', build('malus-law', [
        "Transmitted intensity from the initial polarised intensity and the angle between polarisers",
        "Enter the incident intensity I₀ and the angle θ between polarisers (degrees) to get the transmitted intensity.",
        "Malus's Law Calculator",
        "/ Malus's Law Calculator",
        "📖 Read the \"Transmitted intensity from the initial polarised intensity and the angle between polarisers\" guide",
        "Incident intensity I₀",
        "At θ=90° the light is fully extinguished.",
        "📚 Deep dive: Malus's law",
        "Intensity attenuation when polarisers are stacked.",
        "Polarisation modulation calculations for LCD displays.",
        "Choosing the polarisation angle for sunglasses.",
        "Polarised 100, angle 60°",
        "I=I0·cos²θ=100×cos²60°=100×0.25=25. One quarter of the intensity is transmitted.",
        "Angle 45°",
        "I=100×0.5=50; at an angle of 90° I=0, complete extinction.",
        "Must the incident light be linearly polarised?",
        "Yes; natural light first passes through a polariser to become linearly polarised, and only then is Malus's law applied with the analyser.",
        "Is I0 before or after polarisation?",
        "I0 refers to the linearly polarised intensity arriving at the analyser (typically half the natural light intensity after polarisation).",
    ]))

    write('brewster-angle', build('brewster-angle', [
        "Incidence angle at which the reflected light is fully polarised.",
        "Brewster Angle Calculator",
        "/ Brewster Angle",
        "Brewster Angle",
        "📖 Read the \"Brewster Angle Calculator\" guide",
        "Refractive index n₁ (incident side)",
        "Refractive index n₂ (medium)",
        "Air to glass is about 56.3°.",
        "📚 Deep dive: the Brewster angle (polarising angle)",
        "Choosing incidence angles for camera polarisers and laser windows.",
        "Identifying the critical angle at which reflected light becomes fully linearly polarised.",
        "The angular basis for eliminating reflections from glass and water surfaces.",
        "Air to glass n=1.5",
        "θ_B=arctan(n2/n1)=arctan(1.5/1.0)=56.3°. At this angle the reflected light is pure s-polarised and the transmitted and reflected rays are perpendicular.",
        "Air to water n=1.33",
        "θ_B=arctan(1.33)=53.1°. At 53° incidence on water the glare is weakest and underwater shots are clearest.",
        "Why does one polarisation component disappear from the reflected light at the Brewster angle?",
        "The reflected ray is then at 90° to the refracted ray, the s-polarised component is fully reflected and the reflection coefficient of the p component is 0.",
        "Does the order of the media affect the result?",
        "Yes: tanθ_B=n2/n1 depends on the direction of propagation, and the forward and reverse Brewster angles are complementary.",
    ]))


if __name__ == '__main__':
    main()