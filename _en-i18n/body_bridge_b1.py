def main():
    # ---------------- deflection-calc (27) ----------------
    write('deflection-calc', build('deflection-calc', [
        "🌉 Bridge Deflection Calculator",
        "Deflection calculation and allowable deflection check for simply supported beams under uniformly distributed / concentrated loads",
        "📖 Read the \"Bridge Deflection Calculator User Guide\"",
        "📐 Calculation formulas (simply supported beam)",
        "📚 Deep dive: Deflection Calculation (Flexural Members)",
        "Floor slabs and",
        "bridge deflection",
        "limits and stiffness checks: ",
        "In structural design, estimate the deflection of flexural members from the load, span and section stiffness, and check whether it satisfies the deflection limits of GB 50010 / JTG 3362 (such as L/250, L/400).",
        "Cracking and downward deflection diagnosis of existing structures: testing organizations back-calculate deflection from measured span and load, and compare against code limits to decide whether strengthening is needed (steel plate bonding, carbon fiber or a larger section).",
        "Camber design of precast members: producers preset the counter-camber from the estimated deflection to avoid the sagged appearance after lifting, especially for large-span prestressed beams and slabs.",
        "Worked example (simply supported beam)",
        "Uniformly distributed load q=20 kN/m, span L=6 m, flexural stiffness EI=2.0e8 kN·m²: midspan deflection 5qL⁴/(384EI) ≈ 10.1 mm, about L/594, below the common limit L/400 (15 mm), so stiffness is satisfied. Reducing EI lets you observe the deflection rise.",
        "What deflection limit is normally used?",
        "Concrete beams and slabs per GB 50010 usually take L/200~L/400 (depending on function), while bridges per JTG 3362 take L/400~L/600; members carrying dynamic loads such as crane beams are stricter. The design documents govern.",
        "Why must long-term deflection be considered?",
        "Concrete creep and shrinkage make deflection grow over time, and long-term deflection can reach 1.5~2 times the short-term value; prestressed members also require deducting the counter-camber, so the design should superimpose these.",
        "Can the result be issued directly as an inspection report?",
        "This tool gives a theoretical estimate. Formal inspection requires field-measured deflection, verification of the load history and attached instrument calibration certificates, so the results are only for preliminary judgement and scheme comparison.",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
        "Floor slab and bridge deflection limits and stiffness checks: in concrete structure design, estimate the deflection of flexural members from the load, span and section stiffness, and check whether it satisfies the deflection limits of GB 50010 / JTG 3362 (such as L/250, L/400).",
        "How to use the Bridge Deflection Calculator",
        "What does the bridge deflection calculator do?",
        "The bridge deflection calculator finds the deflection of a simply supported beam under a uniformly distributed or concentrated load and checks the allowable deflection; enter the elastic modulus, moment of inertia and span to ensure stiffness.",
        "How do you use the bridge deflection calculator?",
        "Which scenarios suit the bridge deflection calculator?",
    ]))

    # ---------------- foundation-calc (21) ----------------
    write('foundation-calc', build('foundation-calc', [
        "🧮 Pile Foundation Bearing Capacity Calculator",
        "Characteristic value of single-pile vertical bearing capacity and pile count estimate (friction pile)",
        "📖 Read the \"Pile Foundation Bearing Capacity Calculator User Guide\"",
        "📚 Deep dive: Foundation Calculation (Ground Bearing Capacity)",
        "Sizing of an isolated footing: enter the axial force from the superstructure and the",
        "ground bearing capacity",
        "characteristic value, estimate the required base area, then recheck by eccentricity whether the base pressure stays within 1.2 times the characteristic value.",
        "Comparison of soft ground improvement options: when the natural soil bearing capacity is insufficient, compare the engineering quantities of replacement fill, piles and composite ground, and combine them with cost to choose an economical treatment depth.",
        "Storey-addition check of existing buildings: for renovation projects, back-calculate the tolerable axial force from the existing base area to judge whether storeys can be added directly or the ground must be strengthened.",
        "Worked example (axial compression)",
        "Superstructure axial force 2000 kN, ground bearing capacity characteristic value 180 kPa, foundation embedment 1.5 m, soil unit weight 18 kN/m³: required base area A ≈ 2000/(180-1.5×18) ≈ 12.8 m² (about 3.6 m×3.6 m). Increasing the bearing capacity shows the area shrinking.",
        "Where does the ground bearing capacity characteristic value come from?",
        "It is given by the geotechnical investigation report through load testing or empirical formulas, and must account for depth and width corrections; what you enter here should be the corrected design value, and raw data must never be used directly.",
        "How is it checked under eccentric loading?",
        "Under eccentricity the base shows a trapezoidal / ",
        "pressure distribution, where the maximum pressure pmax should be ≤1.2fa and the average pressure ≤fa; the axial formula here is only a preliminary estimate, and eccentric cases must use the combined expression including the bending moment.",
        "Can the result be used directly for foundation construction drawings?",
        "Foundation design also involves settlement, seismic design and detailing reinforcement, and must be completed by a registered engineer per GB 50007 and the investigation report; this tool's results serve scheme comparison and preliminary sizing.",
        "Free to use, no registration or login required",
        "Supports Simplified / Traditional Chinese / English interface",
        "Sizing of an isolated footing: enter the axial force from the superstructure and the ground bearing capacity characteristic value, estimate the required base area, then recheck by eccentricity whether the base pressure stays within 1.2 times the characteristic value.",
    ]))

    # ---------------- index (20) ----------------
    write('index', build('index', [
        "🌉 Bridge Engineering Tools",
        "Bridge engineering",
        "Bridge Engineering Tools",
        "Span Calculation",
        "Bridge span layout calculator: given the total bridge length and the number of spans, it finds the single-span length, the number of piers and abutments, and estimates continuous beam moments, assisting bridge type scheme comparison.",
        "Per highway-I / II class lane loads, combines the bridge dead load, lane live load and crowd load to compute the midspan moment and support shear of a simply supported beam, checking the ultimate limit state combination.",
        "Deflection Calculator",
        "The bridge deflection calculator finds the deflection of a simply supported beam under a uniformly distributed or concentrated load and checks the allowable deflection; enter the elastic modulus, moment of inertia and span to ensure stiffness.",
        "Foundation Calculator",
        "Pile foundation bearing capacity calculator: uses empirical formulas for side resistance and end bearing to find the characteristic value of single-pile vertical bearing capacity and estimate the pile count, assisting bridge foundation design.",
        "Material Quantity Estimate",
        "The bridge material quantity estimator estimates main girder concrete, deck paving and reinforcement quantities per span or for the whole bridge, assisting budget estimates and material preparation.",
        "About \"Bridge Engineering Tools\"",
        "The Bridge Engineering Tools collection gathers 5 free online tools covering the common calculation, conversion and lookup needs of bridge engineering scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The bridge engineering tools listed on this page include (a few representative tools):",
        "These tools help you finish common bridge engineering tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the bridge engineering tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the bridge engineering tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
