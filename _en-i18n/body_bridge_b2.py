def main():
    # ---------------- load-calc (21) ----------------
    write('load-calc', build('load-calc', [
        "⚖️ Bridge Load Calculator",
        "Dead load + lane live load + crowd load combination for a simply supported beam bridge, computing midspan moment and support shear",
        "📖 Read the \"Bridge Load Calculator User Guide\"",
        "📐 Calculation formulas (simply supported beam)",
        "📚 Deep dive: Load Calculation (Action Combination)",
        "Bridge design load combination: combine dead load (structural self weight, deck paving) and live load (vehicles, crowds) with the code factors to obtain the most unfavorable load intensity at the controlling section, used for reinforcement and foundation design.",
        "Construction-stage temporary load assessment: superimpose temporary loads such as form travelers, scaffolds and stockpiles onto the dead load, and check the scaffold and",
        "ground bearing capacity",
        "to prevent instability or settlement during construction.",
        "Load check before strengthening: when the in-service load standard of an old bridge has been raised, use this tool to recheck whether the original structure still satisfies the current combination requirements, deciding the scope of strengthening.",
        "Worked example (urban-A class approximation)",
        "Dead load 80 kN/m, live load 60 kN/m, dead load partial factor 1.2, live load 1.4: basic combination load intensity = 1.2×80 + 1.4×60 = 180 kN/m. Raising the live load to 100 shows how the combination value affects the internal forces of the section.",
        "How are the load factors for dead load and live load determined?",
        "Highway bridges per JTG D60 use 1.2 for dead load and 1.4 for live load in the ultimate limit state (urban-A / highway-I class); the frequent and quasi-permanent combination factors differ; buildings follow GB 50009. The code tables govern.",
        "How is multi-lane reduction considered?",
        "Under multi-lane loading, lane reduction is applied per the code (transverse distribution coefficient and lane-number reduction). This tool gives the single-girder line load intensity; an overall model must multiply by the distribution coefficient in a spatial analysis.",
        "Can the result be used directly for reinforcement design?",
        "The load intensity is only an input; reinforcement also needs internal forces, material strength and crack checks. This tool's result should serve as a check and a preceding step in the overall structural calculation.",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
        "Construction-stage temporary load assessment: superimpose temporary loads such as form travelers, scaffolds and stockpiles onto the dead load, and check the scaffold and ground bearing capacity to prevent instability or settlement during construction.",
    ]))

    # ---------------- material-qty (18) ----------------
    write('material-qty', build('material-qty', [
        "📐 Bridge Material Quantity Estimate",
        "Estimate main girder concrete, deck paving and reinforcement quantities (per span / whole bridge)",
        "📖 Read the \"Bridge Material Quantity Estimate User Guide\"",
        "📚 Deep dive: Material Quantity Calculation",
        "Concrete and reinforcement quantity estimate: quickly compute C30/C40 concrete volume and HRB400 reinforcement weight from the member volume and reinforcement ratio, for tender bills and material procurement plans.",
        "Formwork and scaffold quantities: estimate the contact formwork area from the member surface area, and combine it with the number of turns to get the required quantity, assisting construction planning and rental decisions.",
        "Waste and material preparation control: add the prescribed waste rate to the net quantity (concrete 1%~2%, reinforcement 2%~3%) to get the delivered amount to prepare, avoiding work stoppage for lack of material or waste.",
        "Worked example (single-span girder)",
        "Girder volume 12 m³, reinforcement ratio 1.5%, reinforcement density 7850 kg/m³: net concrete 12 m³ (adding 1% waste about 12.1 m³); net reinforcement = 12×1.5%×7850 ≈ 1413 kg, adding 2% waste about 1441 kg. Change the reinforcement ratio to see the reinforcement quantity change.",
        "What waste rate is normally used?",
        "Concrete construction waste is about 1%~2% (affected by transport and placing method), reinforcement about 2%~3% (including laps and fabrication); regional quotas differ slightly, so follow the local pricing rules.",
        "Are there upper and lower limits on the reinforcement ratio?",
        "Per GB 50010 the minimum longitudinal tensile reinforcement ratio for flexural members is about 0.2%~0.25%, while the maximum is governed by the limiting compression zone height (usually not exceeding 2.5%); otherwise the section must be enlarged.",
        "Can the result be used directly to place a purchase order?",
        "This tool gives the theoretical net quantity plus waste; actual purchasing must also account for cut lengths, joints and offcuts. The official bill should follow the reinforcement take-off from the construction drawings and the quota.",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
        "Concrete and reinforcement quantity estimate: quickly compute C30/C40 concrete volume and HRB400 reinforcement weight from the member volume and reinforcement ratio, for tender bills and material procurement plans.",
    ]))

    # ---------------- span-calc (17) ----------------
    write('span-calc', build('span-calc', [
        "🧮 Bridge Span Layout Calculator",
        "Compute the single-span length, pier and abutment count and continuous beam moment estimate from the total bridge length and number of spans",
        "📖 Read the \"Bridge Span Layout Calculator User Guide\"",
        "📚 Deep dive: Span Calculation (Bridge Layout)",
        "Bridge scheme comparison: in preliminary design, enter the total bridge length and number of spans to quickly obtain the single-span length, pier count and midspan / support moments, compare the force differences between simply supported and continuous girders, and assist span layout decisions.",
        "Existing bridge recheck: maintenance organizations back-calculate the single-span length from the measured total length and span count, and check whether the original design moments match the current loads, identifying overload and insufficient reinforcement risks.",
        "Teaching and technical briefing: use M=(g+q)L²/8 (simply supported), M=(g+q)L²/12 (continuous beam interior support), M=(g+q)L²/24 (midspan) for classroom demonstrations and construction briefings, showing intuitively how load intensity affects moments.",
        "Worked example (default parameters)",
        "Entering total length 300 m, 5 spans, continuous girder, dead load 150 kN/m, live load 60 kN/m: single-span length 60 m, 4 piers, total load intensity 210 kN/m, maximum interior support moment (g+q)L²/12 ≈ 75600 kN·m, midspan moment (g+q)L²/24 ≈ 37800 kN·m.",
        "Why do the moment formulas differ between simply supported and continuous girders?",
        "A continuous girder develops negative moments at the intermediate supports, so the interior support moment is largest ((g+q)L²/12) and the midspan smaller ((g+q)L²/24); a simply supported beam is largest only at midspan ((g+q)L²/8). The bridge type choice directly affects the reinforcement quantity and cost.",
        "Why is the number of piers the span count minus one?",
        "n spans laid out continuously have n-1 intermediate piers plus 2 abutments; this tool takes the pier count as n-1 and counts abutments separately, since piers and abutments both transfer loads but differ in construction.",
        "Can the result be used directly for construction drawings?",
        "This tool only gives a quick internal-force estimate; formal design must follow the JTG D60 load combinations and JTG 3362 reinforcement checks, and be signed off by a registered structural engineer.",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
    ]))


if __name__ == '__main__':
    main()
