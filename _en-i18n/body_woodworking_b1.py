#!/usr/bin/env python3
from head_woodworking import build, write


def main():
    write('angle-cut', build('angle-cut', [
        '📐 Cut Angle Calculation',
        'Mitre and compound angle calculation, supporting mitre joints, taper cuts and bevel cuts',
        'Performs a professional calculation of "mitre and compound angle calculation, supporting mitre joints, taper cuts and bevel cuts" using the input parameters and outputs the result.',
        '/ Cut Angle',
        '📖 View the Cut Angle Calculation user guide',
        '📚 In-depth analysis: Cut Angle Calculation',
        'Corner joints for picture and photo frames: enter the total joint angle (for example 90°) and the number of equal segments to get each mitre angle and the saw table setting quickly, avoiding wasted stock from repeated trial cuts.',
        'Inside and outside corner finishing for crown moulding and skirting: when two runs meet at a non-90° angle (for example a 135° outside corner), use mitre mode to work out the cut angle for each piece.',
        'Compound mitring (ceiling crown moulding, stair handrails) and taper cutting (table legs, tapered handrails): use compound mitre mode and taper mode respectively to convert the entered mitre/bevel components into the actual saw angles.',
        'Example: mitring a picture frame at a 90° corner',
        'Total joint angle 90°, 2 equal segments: angle per segment = 90 ÷ 2 = 45.00°, mitre angle = (180 − 45) ÷ 2 = 67.50°, saw table setting = 90 − 67.50 = 22.50°. Compound mitre example: with a mitre angle of 45° and a bevel angle of 30°, the actual mitre angle ≈ 40.89°, the actual bevel angle ≈ 20.70° and the true cut angle ≈ 49.11°. Taper example: start width 40 mm, end width 30 mm, length 300 mm, single-sided taper angle ≈ 0.95°, total taper angle ≈ 1.91°, taper ratio 0.0333 (about 1:30).',
        'What is the difference between the mitre angle and the saw table setting?',
        'The mitre angle is the angle of each piece\'s end face relative to the joint centre line, which decides whether the corner closes tightly; the saw table setting is the rotation of the mitre saw table from perpendicular, equal to 90° minus the mitre angle. Both describe the same cut, only from different reference bases.',
        'Why is the entered angle not equal to the actual cut angle in a compound mitre?',
        'A compound mitre contains both a mitre and a bevel component; once the stock is tilted, the angles projected onto the horizontal and vertical planes become smaller. For example, with a mitre of 45° and a bevel of 30°, the actual mitre angle is about 40.89° and the actual bevel angle about 20.70°, and these two converted values must be used to set the saw.',
        'What does a taper ratio of 1:30 mean?',
        'Taper ratio = width difference ÷ length. 1:30 means the width narrows by 1 mm over every 30 mm of length. The single-sided taper angle = arctan(width difference / 2 ÷ length), and setting the saw table to the single-sided taper angle completes the taper cut.',
        'About Cut Angle',
    ]))

    write('board-feet', build('board-feet', [
        '🧮 Board Feet Calculation',
        'Convert between board feet, cubic metres and cubic feet, and work out timber volume quickly',
        '/ Board Feet',
        '📖 View the Board Feet Calculation user guide',
        'Unit price (USD per board foot)',
        '📚 In-depth analysis: Board Feet Calculation',
        'Timber purchasing and quoting: North American hardwood is conventionally priced in board feet (BF); enter thickness (in) × width (in) × length (ft) to get the volume of one board, and multiply by the quantity for the total volume.',
        'Volume ',
        ': when you need to convert between board feet, cubic metres and cubic feet, use conversion mode to get m³ / ft³ / cm³ / MBF in one step.',
        'Cost and inventory estimating: entering a unit price gives an estimate for a batch of timber, useful for price comparison, budgeting and stock accounting.',
        'Example: 10 pine boards of 1″ × 6″ × 8′',
        'Board feet per piece = 1 × 6 × 8 ÷ 12 = 4.00 BF; 10 pieces total 40.00 BF. Conversion: about 0.0944 m³, 3.33 ft³, 0.0400 MBF. At a unit price of $2/BF the estimated cost is $80.00. Note: sellers usually price by the "nominal size" rather than the actual planed size, and the kiln-drying grade and select grade also affect the unit price.',
        'How do board feet and cubic metres convert?',
        '1 board foot ≈ 0.0023597 cubic metres (about 2359.7 cm³). Multiply the total board feet by 0.0023597 to get the volume in cubic metres.',
        'Why is the board I actually buy smaller than the calculated size?',
        'The nominal size of timber (for example 1″ × 6″) is the rough size before planing, so the actual thickness and width are smaller; the board foot formula uses the nominal size, but stock and quotes may follow other conventions, so follow the seller\'s specification table when purchasing.',
        'What unit is MBF?',
        'MBF stands for thousand board feet, a common bulk unit in the hardwood trade. Total board feet ÷ 1000 gives MBF, which is convenient for quoting and statistics on large timber volumes.',
        'About Board Feet',
    ]))

    write('moisture-content', build('moisture-content', [
        '🪵 Wood Moisture Content',
        'Convert between moisture content and shrinkage, and judge how dry the wood is and where it can be used',
        'Core formulas (by input variable): shrink.tangential÷30×fromFsp; shrink.volumetric÷30×fromFsp; shrink.radial÷30×fromFsp',
        '/ Moisture Content',
        '📖 View the Wood Moisture Content user guide',
        '📚 In-depth analysis: Wood Moisture Content',
        'Assessing drying quality: weigh the wet sample and the oven-dry sample, compute the moisture content and judge whether it falls in the kiln-dried, air-dried, half-dried, wet or green range, to decide whether it can be used indoors.',
        'Selecting stock before machining: indoor furniture usually requires 8–12% moisture content; above that, drying must continue to prevent later cracking and distortion.',
        'Predicting drying shrinkage: the radial, tangential and volumetric shrinkage from the fibre saturation point (30%) to the current moisture content, to estimate dimensional change after panel gluing and mortising.',
        'Example: oak sample, wet weight 120 g / oven-dry weight 100 g',
        'Moisture content = (120 − 100) ÷ 100 × 100 = 20.0%, i.e. "wet" (further drying recommended). The gap from the fibre saturation point of 30% to 20% is 10 percentage points: radial shrinkage about 1.70%, tangential about 3.60% and volumetric about 5.20% (oak coefficients radial 5.1 / tangential 10.8 / volumetric 15.6, all computed as ÷ 30 × difference).',
        'What moisture content is suitable for furniture?',
        'Indoor woodwork generally requires 8–12% (the air-dried range). Below 8% is kiln-dried and suits precision woodworking; above 12% the stock must be dried further before indoor use, otherwise it cracks and warps easily.',
        'What is the fibre saturation point of 30%?',
        'The fibre saturation point (FSP) is the critical point at which the cell walls are saturated with water while the free water in the cell cavities has drained, about 30%. Only below this point does wood begin to shrink significantly; shrinkage is estimated as "(30% − current moisture content) ÷ 30 × species coefficient".',
        'Why do radial and tangential shrinkage differ?',
        'Tangential shrinkage is about 1.5–2 times the radial value, owing to differences in ray cells and grain direction. Wide boards therefore cup easily and glued panels open up at the joints, so allow extra stock and stress relief when cutting.',
        'About Moisture Content',
    ]))

    write('mortise-size', build('mortise-size', [
        '🪵 Tenon Size Calculation',
        'Computes tenon length, width and depth for common mortise-and-tenon joints, adapted to different board thicknesses and connection types',
        'Core formulas (by input variable): Math.round(t×actualRatio×hf); Math.round((w-tenonWidth)÷2); Math.round((t-tenonThick)÷2)',
        '/ Mortise Size',
        '📖 View the Tenon Size Calculation user guide',
        '📚 In-depth analysis: Tenon Size Calculation',
        'Furniture joint design: derive tenon thickness, width, depth and shoulder width from the board thickness, board width and joint type (through tenon / stub tenon / dovetail / exposed tenon / hidden tenon / lap joint), balancing strength and appearance.',
        'Compensating for different wood strengths: tenons in softwood loosen easily, so the thickness is scaled up by a hardness factor; hardwood can be tightened slightly.',
        'Layout for machining: cheek height, shoulder width and other detail dimensions are given, making it easy to set up tenoning machines and hand tools and to leave the shoulders.',
        'Example: through tenon, board thickness 25 mm / board width 100 mm / medium-hard wood',
        'Tenon thickness = 25 × 0.4 × 1.0 = 10 mm (40% of board thickness); tenon width = 100 × 0.7 = 70 mm (70% of board width); tenon depth = 25 × 3.0 = 75 mm (full through penetration); shoulder width on each side = (100 − 70) ÷ 2 = 15 mm; cheek height top and bottom = (25 − 10) ÷ 2 = 8 mm.',
        'What fraction of the board thickness is normally used for the tenon?',
        'Common practice is 1/3–1/2 of the board thickness (this tool uses coefficients of 0.33–0.6 for most joint types). Too thin a tenon breaks easily, too thick weakens the parent member; around 0.4 is a safe choice for a through tenon.',
        'How are the coefficients adjusted for softwood and hardwood?',
        'The tool compensates with a hardness factor: 1.1 for softwood (slightly thicker tenon to avoid loosening), 1.0 for medium-hard and 0.9 for hardwood. Hardwood is strong enough to tighten slightly, while softwood needs a thicker tenon or a wedge.',
        'What is special about the 14° angle of a dovetail?',
        'The dovetail angle is usually 8°–14°: a larger angle grips tighter and resists pull-out better, but machining and assembly become harder. This tool uses 14° for dovetails, balancing strength and ease of assembly.',
        'About Mortise Size',
    ]))

    write('wood-screws', build('wood-screws', [
        '🚀 Wood Screw Selection',
        'Recommends screw size, length and pilot hole diameter from board thickness and material',
        'Performs a professional calculation of "recommend screw size, length and pilot hole diameter from board thickness and material" using the input parameters and outputs the result.',
        '/ Wood Screws',
        '📖 View the Wood Screw Selection user guide',
        '🚀 Recommend',
        '📚 In-depth analysis: Wood Screw Selection',
        'Selection for woodworking assembly: enter the top board thickness, bottom board thickness and wood hardness to get the recommended screw size, length, thread outside diameter and pilot hole diameter, avoiding splitting or poor bite when driving.',
        'Adapting to different joint types: face-to-face joints, end joints and pocket-hole joints use different length rules (end and pocket joints need a longer bite).',
        'Countersinking and pilot holes: flat-head screws need a countersunk hole, hardwood needs a larger pilot hole to avoid breakage, and the tool gives both recommendations.',
        'Example: total board thickness 30 mm (15 top + 15 bottom) / medium-hard wood / face connection / flat head',
        'Ideal length = 15 + 15 × 0.67 ≈ 25.05 mm, rounded up to the 5 mm step gives 30 mm; a total thickness of 30 mm falls in the #10 size range, so "#10 × 30 mm flat head" is recommended. Thread outside diameter 4.8 mm, pilot hole diameter for medium-hard wood 3.5 mm, countersink diameter about 9.6 mm, penetration into the lower layer about 100%.',
        'How do I choose a screw length that holds firmly?',
        'As a rule the screw should pass through the top layer and bite into the lower layer by about 2/3 of its thickness. Face connections use top layer + bottom layer × 0.67, pocket connections use top layer + bottom layer × 0.7, then round up to the 5 mm size step.',
        'Why pre-drill, and how large should the hole be?',
        'Pre-drilling prevents the wood from splitting and reduces driving torque. Use a smaller hole in softwood and a larger one in hardwood (this tool interpolates by hardness: softwood uses the softwood pilot value, medium-hard the average of soft and hard, hardwood the hardwood pilot value).',
        'Why do flat-head screws need a countersunk hole?',
        'Flat-head (countersunk) screws must sink their head flush with the wood surface, and the countersink diameter is about twice the thread outside diameter; round heads and trumpet heads stay on the surface and need no countersinking.',
        'About Wood Screws',
    ]))


if __name__ == '__main__':
    main()
