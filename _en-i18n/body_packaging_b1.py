def main():
    # ---------------- calc-1 (18) ----------------
    write('calc-1', build('calc-1', [
        "📦 Carton Master Case Size Calculator",
        "Compute the master case size, volume and space utilization from the product inner dimensions, cushioning thickness and board caliper.",
        "Master case size = product inner size + 2 x (cushioning thickness + board caliper)",
        "Product inner length (mm)",
        "Product inner width (mm)",
        "Product inner height (mm)",
        "Cushioning thickness per side (mm)",
        "Master case size = product inner size + 2 x (cushioning thickness + board caliper). Results are rounded up to the next millimeter for practical material selection.",
        "📚 Deep dive: Carton Master Case Size Calculator",
        "Carton selection for e-commerce shipping: take the product length, width and height, add the foam cushioning thickness per side and the board caliper, and work backwards to the master case size you need, so you avoid cartons that do not fit or leave too much empty space that causes shaking in transit.",
        "Planning multi-unit packs: when one carton holds several products, first compute the footprint of a single product and then add the cushioning thickness, to verify the master case volume against the courier's volumetric weight and volume limits.",
        "Optimizing space utilization: adjust the cushioning and board caliper to trade protection against volume and freight cost, and use the utilization rate to quantify how much material is wasted.",
        "Worked example (product 400 x 300 x 200 mm, cushioning 15 mm per side, board 6 mm)",
        "Added amount per side = 2 x (cushioning + board) = 2 x (15 + 6) = 42 mm. Master case length = ceil(400 + 42) = 442 mm, width = ceil(300 + 42) = 342 mm, height = ceil(200 + 42) = 242 mm (the tool rounds each up to the next millimeter for practical die cutting). Inner net volume = 400 x 300 x 200 / 1e9 = 0.024 m3; master case volume = 442 x 342 x 242 / 1e9 = 0.0366 m3; space utilization = 0.024 / 0.0366 x 100% = 65.6%. The tool stacks master case = inner size + 2 x (cushioning + board), then computes the inner and outer volumes and the utilization rate.",
        "How do I choose the cushioning and board caliper?",
        "Cushioning is determined by the fragility of the contents and the drop height (see the cushioning material coefficient), while board caliper is determined by the carton strength grade (single/double/triple wall). Enter the actual values for both; the tool only does the geometry and does not choose materials for you.",
        "Utilization is only about 65% - is that waste?",
        "The master case must enclose the cushioning plus the board, so this loss is structurally unavoidable. The optimization path is to choose thinner compliant cushioning or a smarter product layout (for example standing the product up instead of laying it flat) to raise the inner net volume share, rather than blindly shrinking the carton and ending up with goods that do not fit or get crushed.",
    ]))

    # ---------------- calc-2 (20) ----------------
    write('calc-2', build('calc-2', [
        "📏 Cushioning Material Thickness Calculator",
        "Estimate the cushioning pad thickness needed for packaging from the drop height, the product fragility value (G factor) and the cushioning material coefficient.",
        "Cushioning layer thickness t = (H / G) x C, where H is the drop height, G is the product fragility value (the maximum acceleration it can take, in g) and C is the dynamic coefficient of the cushioning material. The lower the fragility value, the thicker the cushioning needed; use t to select the cushioning material and structure, and check the static compressive strength and cost.",
        "Product fragility value G",
        "Cushioning material coefficient C",
        "Product weight (kg, optional)",
        "Contact area (cm2, optional)",
        "Reference values for material coefficient C: EPE foam 2.0-2.8, EPS foam 3.0-4.0, bubble film / air cushion 4.0-5.0. Formula t = (H/G) x C.",
        "📚 Deep dive: Cushioning Material Thickness Calculator",
        "Protecting fragile goods: for phones, glass or ceramics, estimate the required pad thickness from the drop height and the product fragility value G. The smaller G is, the more delicate the product and the thicker the cushioning needed.",
        "Comparing materials: EPE foam cushions well but takes up space,",
        "stiffer and thinner materials such as bubble film need less thickness; use the material coefficient C to compare how thick each one must be for the same drop.",
        "Dynamic stress check: enter the product weight and the cushioning contact area to verify that the dynamic stress on the cushion face at impact stays within the material's limit, preventing puncture or crushing.",
        "Worked example (drop height 90 cm, fragility value G=40, EPE coefficient C=2.5, weight 3 kg, contact area 80 cm2)",
        "Cushioning thickness (cm) t = (H / G) x C = (90 / 40) x 2.5 = 5.625 cm = 56.25 mm. For a product weighing 3 kg with a cushioning contact area of 80 cm2, the drop dynamic stress = (weight x 9.80665 x G) / (area / 10000) / 1000 = (3 x 9.80665 x 40) / (80 / 10000) / 1000 = 147.10 kPa. The tool uses t = (H / G) x C (centimeters first, then x10 to millimeters) and can optionally compute the dynamic stress.",
        "What is the product fragility value G and how is it chosen?",
        "G is the maximum acceleration the product can withstand (in g), determined by its own impact resistance. It comes from the manufacturer datasheet or drop testing; fragile goods commonly use 30-60, and the more delicate the product the smaller G is and the thicker the cushioning must be. This tool only does the calculation, so you must fill in G from the product data.",
        "Where does the range of material coefficient C come from?",
        "C is determined by the cushioning efficiency of the material: EPE foam about 2.0-2.8, EPS foam about 3.0-4.0, bubble film / air cushion about 4.0-5.0. For the same drop, a larger C means weaker absorption per unit thickness and thus more thickness needed; it is an empirical coefficient rather than an absolute value.",
        "Used to compute the dynamic load",
    ]))


if __name__ == '__main__':
    main()
