def main():
    # ---------------- accessible-restroom (19) ----------------
    write('accessible-restroom', build('accessible-restroom', [
        "📚 Accessible Restroom",
        "Quick reference for accessible restroom facility dimensions, with layout diagrams, for design and acceptance",
        "📖 Read the \"Accessible Restroom User Guide\"",
        "A quick reference for the key dimensions of an accessible restroom (grab bar height, turning diameter, clear door width, toilet height, etc.) and design essentials, assisting accessible environment design and acceptance. Pure front-end local reference, no data uploaded.",
        "Floor layout",
        "Facility dimensions",
        "Acceptance checklist",
        "📚 Deep dive: Accessible Restroom",
        "Home aging-in-place renovation: renovate the bathroom for elderly people with limited mobility, and check with this tool that the toilet height is 0.45m, the L-shaped grab bars on both sides are 0.70m above the floor, and the turning diameter is ≥1.50m, so the renovation does not still fall short after completion.",
        "Public building design: public toilets provide an accessible stall, with a use area of ≥4.00m² (2m×2m or more), a clear door opening of ≥0.80m, a wash basin height of 0.80m with ≥0.60m clear space below, satisfying GB 55019-2021.",
        "Engineering acceptance: check the 14 built-in acceptance items one by one (no level difference inside and outside the door or a transition ramp ≤15mm, anti-slip floor class C, call button 0.40~0.50m above the floor, etc.), and export the checklist in one click for archiving.",
        "Example: measured check of a restroom",
        "A measured restroom plan of 1.8m×1.9m=3.42m² (<4.00m², not compliant), a door opening of 0.75m (<0.80m, not compliant), and a turning area of 1.2m square (diameter about 1.20m < 1.50m, not compliant). None of the three satisfies GB 55019-2021, so the use area must be expanded to at least 4.00m², the door opening widened, and wheelchair turning space guaranteed; otherwise the acceptance will not pass.",
        "What is the minimum area requirement for an accessible restroom?",
        "Under \"General Code for Accessibility of Buildings and Municipal Engineering\" GB 55019-2021, the use area of an accessible restroom should not be less than 4.00m² (2m×2m or more is recommended), and a wheelchair turning space of diameter ≥1.50m must be ensured; the clear door opening is ≥0.80m, with the door opening outward or sliding.",
        "What are the key points for grab bar installation?",
        "L-shaped or horizontal grab bars should be provided on both sides of the toilet, installed at a height of 0.70m above the floor with a length of ≥0.70m; grab bars should be firm and anti-slip, with a diameter of 30~40mm for easy gripping; the wash basin height is 0.80m, and lever or sensor faucets are preferred.",
        "About \"Accessible Restroom\"",
        "A quick reference for the key dimensions and design essentials of an accessible restroom, assisting accessible environment design and acceptance, with all data processed locally and never uploaded.",
    ]))

    # ---------------- braille-translator (23) ----------------
    write('braille-translator', build('braille-translator', [
        "♿ Braille Translator",
        "Transliterate pinyin, English letters and digits into braille cells, showing the dot pattern in sync, to assist braille learning",
        "📖 Read the \"Braille Translator User Guide\"",
        "Transliterate pinyin, English letters and digits into braille cells and show the dot pattern diagram in sync, assisting braille learning and teaching. Pure front-end local processing, no data uploaded.",
        "Left column, top to bottom:",
        "Dot",
        "Right column, top to bottom:",
        "Different dot combinations represent different letters, digits or symbols.",
        "📚 Deep dive: Braille Translator",
        "Braille learning: entering \"hello 2026\", the tool transliterates character by character — h→⠓, e→⠑, l→⠇(×2), o→⠕, separated by spaces, with a number sign ⠼ automatically added before numbers, followed by 2→⠉, 0→⠚, 2→⠉, 6→⠋, outputting the braille dot string.",
        "Teaching reference: check \"show dots\" to see the 6-dot pattern of each letter (left column 1/2/3, right column 4/5/6), a=[1], b=[1,2], c=[1,4]……z=[1,3,5,6], giving an intuitive grasp of the dot encoding.",
        "Preparing Chinese braille: Chinese must first be converted to pinyin (initial + final + tone); this tool supports pinyin letters and digits, and combined with the site's",
        "pinyin converter",
        "tool it can complete \"ni hao\"→braille.",
        "Example: transliterating \"12\" and \"ab\"",
        "Entering \"12\": the first character is a digit, so the number sign ⠼ is output first (dots 3,4,5,6), then 1→a's pattern ⠁ and 2→b's pattern ⠃ (consecutive digits do not repeat the number sign), 3 braille cells in total. Entering \"ab\": a→⠁, b→⠃, 2 cells in total. The whole phrase \"hello 2026\" has 5 letters and 4 digits, so with the number sign and the space it is 11 cells in total (hello=5, space=1, 2026 = number sign + 4 digits = 5).",
        "How are digits represented in braille?",
        "Braille digits borrow the patterns of a~j (1→a, 2→b……9→i, 0→j), and a number sign ⠼ must be added before the digits; consecutive digits add the number sign only once at the start. This tool already handles this rule automatically.",
        "Can Chinese be transliterated directly into braille?",
        "This tool uses Grade 1 braille for character-by-character transliteration and supports only pinyin letters, English and digits. Chinese must first be converted to pinyin (initial + final + tone); you can use the site's \"pinyin converter\" tool and paste the result in.",
        "About \"Braille Translator\"",
        "Braille cell transliteration and dot pattern diagram generation, assisting braille learning and teaching, with all data processed locally and never uploaded.",
        "e.g. ni hao / hello / 123",
    ]))

    # ---------------- index (14) ----------------
    write('index', build('index', [
        "♿ Accessibility Tools",
        "Accessibility tools",
        "Enter the height difference to compute the slope, horizontal length and ramp length of an accessible wheelchair ramp, and check compliance with the design code limits.",
        "Transliterate pinyin, English letters and digits into braille cells, showing the dot pattern diagram in sync, assisting braille learning and teaching.",
        "Accessible restroom facility dimension code quick reference tool, providing key dimensions such as wash basin, toilet and turning radius plus floor layout diagrams, assisting aging-in-place and accessible design as well as engineering acceptance.",
        "A quick reference of Chinese Sign Language basic vocabulary with diagrams, showing handshape, hand position and movement essentials by topic, facilitating communication for hearing-impaired people and comparison practice for sign language learners.",
        "About \"Accessibility Tools\"",
        "The Accessibility Tools collection gathers 5 free online tools covering the common calculation, conversion and lookup needs of accessibility scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The accessibility tools listed on this page include (a few representative tools):",
        "These tools help you finish common accessibility tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the accessibility tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the accessibility tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
