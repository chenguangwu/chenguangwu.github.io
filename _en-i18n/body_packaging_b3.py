def main():
    # ---------------- shousuomo-shousuolv-refeng-canshu (21) ----------------
    write('shousuomo-shousuolv-refeng-canshu', build('shousuomo-shousuolv-refeng-canshu', [
        "⚙️ Shrink Film (Shrink Rate / Heat Seal) Parameters",
        "Compute the heat shrink rate, post-shrink proportion and recommended cut film width from the sizes before and after heat shrinking.",
        "Heat shrink rate = (original size - shrunk size) / original size x 100%; recommended film width = original size x 1.06",
        "The shrink rate reflects the film's shrinking ability and directly affects wrap tightness and the heat seal position; the recommended film width leaves 6% shrink allowance for cutting stock and setting heat seal parameters.",
        "Original size (mm)",
        "Size after heat shrinking (mm)",
        "Tip: heat shrink rate = (original - shrunk) / original x 100%; the cut film width reserves shrink allowance of original size x 1.06.",
        "📚 Deep dive: Shrink Film (Shrink Rate / Heat Seal) Parameters",
        "Film grade selection: measure the actual heat shrink rate and compare it with the nominal ranges of PE, POF and PVC to judge whether the film suits the product shape and appearance requirements.",
        "Cut film width calculation: compute the cut film width with a 6% process allowance so the wrap does not end up loose or torn after shrinking.",
        "Tuning the heat shrink process: after changing the oven temperature or line speed, re-measure the shrink rate and use the post-shrink proportion to judge whether wrap tightness is stable.",
        "Worked example: original size 400 mm, 240 mm after heat shrinking",
        "Heat shrink rate = (400 - 240) / 400 x 100% = 40.00%; post-shrink proportion = 240 / 400 x 100% = 60.00%; recommended cut film width = 400 x 1.06 = 424.00 mm.",
        "What is the relation between shrink rate and post-shrink proportion?",
        "They are complementary: shrink rate + post-shrink proportion = 100%. A higher shrink rate means more shrink tension and a tighter wrap, but it also raises the risk of over-shrinking (deformation, tearing).",
        "Why reserve 6% allowance when cutting?",
        "6% is a common process allowance that absorbs uneven shrinking and the loss from seal overlap; for complex product shapes or films with a large shrink-rate deviation, raise it to 8%-10%.",
        "About \"Shrink Film (Shrink Rate / Heat Seal) Parameters\"",
        "Shrink Film (Shrink Rate / Heat Seal) Parameters. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Shrink rate",
        "Heat seal",
    ]))

    # ---------------- strength-11 (20) ----------------
    write('strength-11', build('strength-11', [
        "📐 Corrugated Board (Flute / Strength) Design",
        "Uses the McKee approximation to estimate the compression strength of a corrugated carton and its load capacity per unit caliper, with the box perimeter taken as 1000 mm.",
        "BCT = 5.87 x ECT x SQRT(thickness x box perimeter); this tool takes the box perimeter = 1000 mm",
        "The McKee formula converts edge crush strength ECT and board caliper into whole-box compression strength; the box perimeter is taken as 1000 mm, and the result is used for flute grade selection and stacking layer verification.",
        "Edge crush strength ECT (kN/m)",
        "Board caliper (mm)",
        "Tip: BCT = 5.87 x ECT x SQRT(thickness x box perimeter), with the box perimeter taken as 1000 mm; a larger ECT-to-thickness ratio means better rigidity.",
        "📚 Deep dive: Corrugated Board (Flute / Strength) Design",
        "Flute grade selection: substitute the ECT and board caliper of candidate flute grades into the McKee approximation to estimate whole-box compression strength BCT, and pick a grade strong enough without being stronger, to avoid wasted cost.",
        "Stacking verification: derive the allowable number of stacking layers from BCT and the safety factor, so lower cartons in the stack are not crushed.",
        "Down-gauging assessment: after reducing board caliper or switching to a lighter grammage liner, re-estimate BCT to quantify the strength loss.",
        "Worked example: ECT 7 kN/m, board caliper 3 mm",
        "BCT = 5.87 x 7 x SQRT(3 x 1000) = 2251 N = 2.251 kN (box perimeter taken as 1000 mm); ECT/thickness = 7 / 3 = 2.333 kN/m.mm; unit ECT load capacity coefficient = 5.87 x SQRT(3000) = 321.5 N/(kN/m).",
        "How is the box perimeter in the McKee formula chosen?",
        "The full form is BCT = 5.87 x ECT x SQRT(thickness x box perimeter). This tool fixes the box perimeter at 1000 mm (about a 250 mm cube standard box); for a different box size, correct it in proportion to the actual perimeter.",
        "How far off is the estimate from the measured compression strength?",
        "McKee is an empirical approximation with a typical deviation of about ±10%-20%, further affected by perforations, printing, humidity and stacking time; the final authority should be the whole-box compression test.",
        "About \"Corrugated Board (Flute / Strength) Design\"",
        "Corrugated Board (Flute / Strength) Design. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Flute grade",
    ]))

    # ---------------- strength-12 (21) ----------------
    write('strength-12', build('strength-12', [
        "⚙️ Carton Sealing (Tape / Hot Melt Adhesive) Strength",
        "Convert the peel force and tape width into peel strength per unit width of carton sealing tape (normalized to the 25 mm standard width).",
        "Peel strength = peel force x 25 / tape width (N/25mm); peel strength = peel force x 1000 / tape width (N/m)",
        "The peel strength of carton sealing tape is normalized to the 25 mm standard width for easy comparison across widths; results are also given in N/m, N/cm and the deviation from the common 10 N/25mm baseline.",
        "Peel force (N)",
        "Tape width (mm)",
        "Tip: peel strength = peel force x 25 / tape width (N/25mm); the common baseline is about 10 N/25mm, and anything below the baseline needs a sealing reliability review.",
        "📚 Deep dive: Carton Sealing (Tape / Hot Melt Adhesive) Strength",
        "Incoming inspection: convert the measured peel force of tapes of different widths to the 25 mm standard width, removing width differences so tape quality can be compared.",
        "Sealing method selection: bring tape peel strength and hot melt adhesive bond strength onto the same per-unit-width basis to judge which sealing method resists handling tears better.",
        "Low temperature check: adhesive peel strength drops markedly in cold conditions, so verify with measured values whether it is still above the common 10 N/25mm baseline.",
        "Worked example: peel force 30 N, tape width 48 mm",
        "Peel strength = 30 x 25 / 48 = 15.625 N/25mm; in N/m terms = 30 x 1000 / 48 = 625.0 N/m; peel force per centimeter = 30 x 10 / 48 = 6.25 N/cm; deviation from the 10 N/25mm baseline = (15.625 - 10) / 10 x 100% = 56.25%.",
        "Why normalize to a 25 mm width?",
        "Peel strength is proportional to width, so the peel force of a whole tape cannot be used to compare the quality of 45 mm and 60 mm tapes; only after converting to the 25 mm standard width can you compare across widths.",
        "Is higher peel strength always better?",
        "For sealing reliability higher is steadier, but too high causes difficulty opening cartons and adhesive residue; common carton sealing tapes fall between 8-20 N/25mm, so choose according to box weight and transport conditions.",
        "About \"Carton Sealing (Tape / Hot Melt Adhesive) Strength\"",
        "Carton Sealing (Tape / Hot Melt Adhesive) Strength. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "Tape",
        "Hot melt adhesive",
    ]))


if __name__ == '__main__':
    main()
