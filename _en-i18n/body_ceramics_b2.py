def main():
    # ---------------- glaze-temp (26) ----------------
    write('glaze-temp', build('glaze-temp', [
        "🌡️ Glaze Temperature Reference",
        "Look up the temperature corresponding to pyrometric cones (Orton / Seger cones) and the glaze melting temperature classification, to choose a glaze firing temperature matching the body.",
        "Based on ceramic firing practice, this gives the recommended firing temperature ranges for low-fire (about 900-1050°C), medium-fire (about 1100-1200°C) and high-fire (about 1200-1300°C) glazes, and warns about the risks of over-firing running and under-firing dullness; the glaze formula and pyrometric cones govern. Pure front-end local calculation, data never leaves the browser.",
        "📋 Glaze Melting Temperature Classification",
        "📚 Deep dive: Glaze Temperature Reference",
        "Checking the maximum glaze firing temperature: look up the recommended upper limit by glaze type to avoid over-firing running and bubbles, or under-firing dullness and orange peel.",
        "Body-glaze matching: refer to the expansion coefficients and firing temperature ranges of the body and the glaze to reduce interface defects such as glaze flaking and crazing.",
        "Kiln temperature uniformity check: compare measured thermocouple temperatures with the nominal firing temperature to correct the color difference and deformation caused by top-bottom temperature differences.",
        "Transparent glaze firing temperature check worked example",
        "Entering a potassium feldspar transparent glaze, the tool gives a recommended firing range of 1220-1260°C (upper medium-fire) and warns that above 1280°C it tends to over-fire and run, while below 1180°C it may come out dull.",
        "How are low-fire, medium-fire and high-fire glazes distinguished?",
        "Usually by firing temperature: low-fire glazes about 900-1050°C (mostly lead-boron frit), medium-fire glazes about 1100-1200°C, and high-fire glazes about 1200-1300°C (feldspar porcelain glazes). The glaze formula and pyrometric cones govern.",
        "What does over-firing and under-firing look like?",
        "Over-firing: glaze running, pinholes, deformation and even sticking to the shelf; under-firing: dullness, orange peel and unresolved glaze bubbles. Both affect appearance and durability, and require refiring or lowering the temperature.",
        "How do pyrometric cones correspond to temperature?",
        "A pyrometric cone (such as an Orton cone) bends at a temperature corresponding to a specific heating curve, and is used to read the actual temperature inside the kiln, which reflects how the body and glaze actually experience the heat better than the controller reading.",
        "The Glaze Temperature Reference is an online tool for potters and studios, giving recommended firing ranges for low / medium / high-fire glazes and assisting body-glaze matching, processed entirely in the browser with data calculated locally to protect privacy.",
        "One-click conversion of ceramic parameters: shrinkage, ratio, temperature and wheel speed computed in real time",
        "Local calculation: data never leaves the browser, protecting recipe and process secrets",
        "Results can be copied and exported: convenient for records and refiring comparison",
        "Fits many clay bodies and glaze formulas: earthenware, stoneware and porcelain all work",
        "Glaze firing temperature check: avoid over-firing or under-firing",
        "Body-glaze matching: reduce flaking and crazing",
        "Kiln temperature uniformity check: correct top-bottom color differences",
        "Pyrometric cone reference: read the actual kiln temperature",
        "Enter a cone number or temperature to filter",
    ]))

    # ---------------- index (16) ----------------
    write('index', build('index', [
        "🏺 Ceramics Craft Tools",
        "Ceramics craft",
        "Ceramics Craft Tools",
        "The Clay Shrinkage Calculator derives the wet clay making dimensions from the target finished size and the total shrinkage, assisting ceramic forming and firing dimension control.",
        "Compute the weighing amount of each raw material from the glaze recipe percentages, and estimate the water needed to mix the glaze slip (dipping / pouring / spraying).",
        "Based on the body diameter and the stage (opening, pulling, closing), recommend a suitable potter's wheel speed to avoid centrifugal deformation, helping new potters grasp the speed range of each process.",
        "Look up the temperature corresponding to pyrometric cones (Orton / Seger cones) and the glaze melting temperature classification, to choose a glaze firing temperature matching the body.",
        "View the recommended firing temperature curve by body / glaze type, including the heating rate, soak temperature and soak time, and estimate the total firing duration.",
        "About \"Ceramics Craft Tools\"",
        "The Ceramics Craft Tools collection gathers 5 free online tools covering the common calculation, conversion and lookup needs of ceramics craft scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The ceramics craft tools listed on this page include (a few representative tools):",
        "These tools help you finish common ceramics craft tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the ceramics craft tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the ceramics craft tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
