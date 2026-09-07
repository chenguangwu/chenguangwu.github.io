# -*- coding: utf-8 -*-
"""engineering 分类英文 i18n 套话清理：slug-en.json + _en_override.json 的 14 个 key 去套话补真实英文。"""
import json

SL = "i18n/tools/slug-en.json"
OV = "i18n/tools/_en_override.json"

EN = {
    "shaft-torsion": ("Shaft Torsion Calculator", "Estimate shaft torque from power and speed, check maximum shear stress of solid or hollow shafts against allowable stress for drive shaft design."),
    "bending-stress": ("Bending Stress Calculator", "Compute maximum bending stress sigma=M/W from moment and section modulus, verify beam and shaft bending strength."),
    "section-inertia": ("Section Moment of Inertia Calculator", "Calculate second moment of area for rectangle, circle and built-up sections with parallel axis theorem for beam deflection and bending."),
    "poisson-strain": ("Poisson's Ratio & Lateral Strain Calculator", "Compute lateral strain from axial strain and Poisson's ratio for steel, aluminum, copper and concrete."),
    "cantilever-deflection": ("Cantilever Beam Deflection Calculator", "Find free-end deflection of cantilever beams under end point load, UDL or end moment, compare with allowable deflection."),
    "thermal-expansion": ("Thermal Expansion Calculator", "Compute thermal elongation DeltaL=alpha*L*DeltaT for steel, aluminum, copper and plastics in piping and track joints."),
    "weld-strength": ("Weld Strength Calculator", "Check fillet weld shear stress tau=F/(0.707*a*L) against allowable for structural and pressure vessel joints."),
    "bolt-preload": ("Bolt Preload & Torque Calculator", "Convert tightening torque to bolt preload with torque coefficient K, for flanges and anchor bolts."),
    "axial-stress": ("Axial Stress Calculator", "Compute tensile/compressive stress sigma=F/A for rods, columns and links, check against allowable and buckling."),
    "pressure-vessel": ("Pressure Vessel Stress Calculator", "Compute thin-wall hoop and longitudinal stress for cylinders and spheres, size wall thickness for tanks and pipes."),
    "beam-calculator": ("Beam Deflection Calculator", "Compute maximum deflection of simply supported and cantilever beams under UDL or point load, verify stiffness limit."),
    "heat-transfer": ("Heat Transfer Calculator", "Compute conduction, convection and overall heat transfer for walls, pipes and heat exchangers."),
    "material-calculator": ("Material Section & Weight Calculator", "Estimate cross-section area, volume and weight of round, rectangular, tube and I sections for cutting and self-weight."),
    "stress-calculator": ("Stress Calculator", "Compute normal stress sigma=F/A for general members, compare with allowable stress and buckling check."),
}

BOILER = ["free online tool", "free and accurate", "calculate online, free", "free tool"]


def clean(s):
    if not s:
        return s
    low = s.lower()
    for b in BOILER:
        if b in low:
            return s
    return s


def main():
    sl = json.load(open(SL, encoding="utf-8"), strict=False)
    ov = json.load(open(OV, encoding="utf-8"), strict=False)
    n_sl = 0
    n_ov = 0
    for slug, (en, ed) in EN.items():
        key = "engineering/" + slug
        if key in sl:
            sl[key]["en"] = en
            sl[key]["ed"] = ed
            n_sl += 1
        if key in ov:
            ov[key]["en"] = en
            ov[key]["ed"] = ed
            n_ov += 1
    # 残留检测
    resid = 0
    for d in (sl, ov):
        for k, v in d.items():
            if not k.startswith("engineering/"):
                continue
            txt = (v.get("en", "") + " " + v.get("ed", "")).lower()
            if any(b in txt for b in BOILER):
                resid += 1
                print("RESIDUAL:", k, repr(v.get("en", "")), repr(v.get("ed", "")[:60]))
    with open(SL, "w", encoding="utf-8") as f:
        json.dump(sl, f, ensure_ascii=False, indent=2)
    with open(OV, "w", encoding="utf-8") as f:
        json.dump(ov, f, ensure_ascii=False, indent=2)
    print("slug-en updated:", n_sl, "override updated:", n_ov, "residual:", resid)


if __name__ == "__main__":
    main()
