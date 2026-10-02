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
    write('thin-lens-equation', build('thin-lens-equation', [
        "Thin lens imaging formula 1/f = 1/d_o + 1/d_i",
        "Find the image distance from the object distance and focal length.",
        "Thin Lens Imaging Formula Calculator",
        "/ Thin Lens Imaging",
        "Thin Lens Imaging",
        "📖 Read the \"Thin lens imaging formula 1/f = 1/d_o + 1/d_i\" guide",
        "Focal length f (m)",
        "f=0.1 and d_o=0.3 → d_i=0.15 m (real image).",
        "📚 Deep dive: the thin lens imaging formula",
        "Image distance calculations for cameras and projectors.",
        "Image position for magnifiers and eyeglasses.",
        "First element design in a lens group.",
        "Convex lens f=10cm, object distance 30cm",
        "1/di=1/f−1/do=1/0.1−1/0.3=10−3.33=6.67, di=15cm (real image).",
        "Object distance 8cm (less than f)",
        "1/di=10−12.5=−2.5, di=−0.4m, a virtual image, upright and magnified (the magnifier principle).",
        "Is the image distance negative for a virtual image?",
        "Yes; when do<f an upright magnified virtual image forms on the same side as the object.",
        "When does the thin lens approximation hold?",
        "It holds when the lens thickness is much smaller than the focal length and object and image distances; thick lenses need principal planes.",
    ]))

    write('combined-lens-focal', build('combined-lens-focal', [
        "Equivalent focal length of two lenses in contact.",
        "Combined Lens Focal Length Calculator",
        "/ Combined Lens Focal Length",
        "Combined Lens Focal Length",
        "📖 Read the \"Combined Lens Focal Length Calculator\" guide",
        "Focal length f₁ (m)",
        "Focal length f₂ (m)",
        "0.1 combined with 0.2 → 0.0667 m.",
        "📚 Deep dive: focal length of thin lenses in contact",
        "When two lenses are cemented or pressed together,",
        "design the total optical power of a compound lens group.",
        "Estimate the overall refractive power of a lens assembly.",
        "100mm and 200mm in contact",
        "1/F=1/f1+1/f2=1/0.1+1/0.2=10+5=15, F=1/15=0.0667m=66.7mm. Combined optical power = 15D.",
        "Two 50mm lenses of the same sign",
        "1/F=1/0.05+1/0.05=40, F=25mm. The more in contact two lenses of the same sign are, the shorter the combined focal length.",
        "What happens when a positive and a negative lens are joined?",
        "With opposite signs 1/F subtracts, so the optical power can cancel (as in achromatic doublets), and the combined focal length can even tend to infinity.",
        "Does this hold only for lenses in contact?",
        "This formula assumes the separation is about zero; with a gap use the separated lens formula 1/F=1/f1+1/f2−d/(f1f2).",
    ]))

    write('separated-lenses-focal', build('separated-lenses-focal', [
        "Combined focal length from two lens focal lengths and their separation",
        "Enter the two focal lengths f₁ and f₂ and the separation d to get the combined focal length.",
        "Separated Two-Lens Combination Focal Length Calculator",
        "/ Separated Two-Lens Combination Focal Length Calculator",
        "📖 Read the \"Combined focal length from two lens focal lengths and their separation\" guide",
        "Focal length f₁ (cm)",
        "Focal length f₂ (cm)",
        "Separation d (cm)",
        "As d→0 it reduces to lenses in contact.",
        "📚 Deep dive: combined focal length of separated lenses",
        "Telescope and microscope lens groups.",
        "Effect of lens separation on the combined focal point.",
        "Back-calculating zoom group designs.",
        "100mm and 100mm with 2cm spacing",
        "Separation increased to 5cm",
        "1/F=0.02−0.05/100=0.015, F=66.7mm; increasing the separation lengthens the combined focal length.",
        "What happens when d approaches f1+f2?",
        "Then 1/F→0 and the combined focal length→∞, so the system approaches afocal (telescope-like).",
        "How does it relate to the contact formula?",
        "With d=0 it reduces to 1/F=1/f1+1/f2.",
    ]))

    write('focal-length-mirror', build('focal-length-mirror', [
        "Focal length of a spherical mirror from its radius of curvature",
        "Enter the radius of curvature R of a spherical mirror to get the focal length.",
        "Spherical Mirror Focal Length Calculator",
        "/ Spherical Mirror Focal Length Calculator",
        "📖 Read the \"Focal length of a spherical mirror from its radius of curvature\" guide",
        "Radius of curvature R (cm)",
        "Take R and f positive for a concave mirror, negative for a convex mirror.",
        "📚 Deep dive: focal length of spherical mirrors",
        "Concave converging and convex diverging mirror designs.",
        "Calculations for telescope secondary mirrors and headlight reflectors.",
        "Judging the focal length of a make-up mirror or a rear-view mirror.",
        "Radius of curvature 20cm",
        "f=R/2=20/2=10cm. The focus of a concave mirror sits 10cm in front, the virtual focus of a convex mirror 10cm behind.",
        "R=80cm headlight bowl",
        "f=40cm; placing the source at the focus gives an approximately collimated output beam.",
        "What is the sign convention for a convex mirror?",
        "By convention a convex mirror has f<0 (virtual focus) and a concave mirror f>0 (real focus).",
        "Does it only hold in the paraxial regime?",
        "Spherical aberration makes large apertures deviate from f=R/2, and a parabolic mirror can eliminate on-axis aberration.",
    ]))

    write('mirror-equation', build('mirror-equation', [
        "Spherical mirror imaging formula 1/f = 1/d_o + 1/d_i",
        "Imaging formula for concave and convex mirrors (using the same sign convention as thin lenses).",
        "Spherical Mirror Imaging Formula Calculator",
        "/ Spherical Mirror Imaging",
        "📖 Read the \"Spherical mirror imaging formula 1/f = 1/d_o + 1/d_i\" guide",
        "Focal length f (positive for concave, negative for convex) (m)",
        "Concave mirror f>0, convex mirror f<0.",
        "📚 Deep dive: the spherical mirror imaging formula",
        "Image distance for concave and convex mirrors and whether it is real or virtual.",
        "Image position for rear-view mirrors and make-up mirrors.",
        "Spacing design for laser cavity mirrors.",
        "Concave mirror f=20cm, object distance 50cm",
        "1/di=1/f−1/do=1/0.2−1/0.5=5−2=3, di=0.333m=33.3cm (real image).",
        "Convex mirror f=−20cm, object distance 50cm",
        "1/di=−5−2=−7, di=−0.143m, a virtual image 14.3cm behind the mirror.",
        "Is the image distance negative for a convex mirror?",
        "Yes, it indicates a virtual image, reduced and upright, which suits wide-angle rear-view mirrors.",
        "How does it differ from the lens formula?",
        "The form is the same but the sign conventions differ: reflection uses f=R/2, while refraction uses the lensmaker's equation.",
    ]))

    write('optical-power-diopter', build('optical-power-diopter', [
        "Optical power (dioptres) of a lens from its focal length",
        "Enter the focal length f (metres) to get the optical power.",
        "Lens Optical Power (Dioptres) Calculator",
        "/ Lens Optical Power (Dioptres) Calculator",
        "📖 Read the \"Optical power (dioptres) of a lens from its focal length\" guide",
        "Focal length f (metres)",
        "P is positive for converging and negative for diverging.",
        "📚 Deep dive: optical power (dioptres)",
        "Converting prescription strengths for eyeglasses.",
        "Correspondence between lens focal length and refractive power.",
        "Designing powers for presbyopia and myopia lenses.",
        "Focal length 0.5m",
        "P=1/f=1/0.5=2D (200 degrees). Myopia lenses are negative dioptres, hyperopia lenses positive.",
        "Focal length −0.5m (myopia of 200 degrees)",
        "P=1/(−0.5)=−2D; an object at infinity images 0.5m in front of the retina.",
        "How do degrees and D convert?",
        "1D=100 degrees, so −2D is a lens for 200 degrees of myopia.",
        "What is the total power of two lenses worn together?",
        "For thin lenses in contact the powers add: P=P1+P2.",
    ]))


if __name__ == '__main__':
    main()