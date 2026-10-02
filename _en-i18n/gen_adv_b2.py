#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'advertising')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'advertising')
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
    out = {'slug': slug, 'industry': 'advertising', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('copy-duration', build('copy-duration', [
        "⚡ Script Reading Duration",
        "Estimate reading duration from word count and speech rate, suited to voiceover, ads and presentations",
        "Core formula (in terms of input variables): zhCount+numCount+Math.round(enCount÷2); Math.round(enCount÷5)+zhCount+numCount; zhCount+numCount+Math.round(enCount÷5)",
        "📖 Read the Script Reading Duration user guide",
        "Enter the script content",
        "Welcome to our brand launch event. Today we are bringing you a completely new product experience. This product embodies three years of the team's hard work and is dedicated to creating a better experience for users. Let us begin this new journey together.",
        "Speech rate type",
        "Slow (news broadcast)",
        "Normal (standard reading)",
        "Fast (ad voiceover)",
        "Custom speech rate (characters per minute)",
        "Pause time (seconds per segment)",
        "⚡ Calculate duration",
        "Speech rate reference:",
        "Chinese is about 180 characters per minute when slow (news broadcast), about 240 (standard reading) when normal, and about 300 (ad voiceover) when fast. English is about 130-150 words per minute.",
        "📚 Deep Dive: Script Reading Duration",
        "Before an ad voiceover or a short video voice track, estimate the reading seconds of the script from the speech rate to hit the 15-second or 30-second cut precisely.",
        "For copy that is mostly Chinese with embedded English brand words, count the Chinese characters and the English words separately so the duration is not miscalculated.",
        "Leave pauses between segments (for example at punctuation) so the total duration is closer to the real recording.",
        "Estimate the duration of a 30-second voiceover script",
        "A 120-character Chinese script at 'Normal (standard reading)' of 250 characters per minute → reading time 120÷250×60 ≈ 28.8 seconds; adding three pauses of 1 second each, the total is about 31.8 seconds, which just fits a 30-35 second voiceover slot.",
        "How do I choose the speech rate tier?",
        "Slow (news broadcast) is about 180-200 characters per minute, normal (standard reading) about 240-260, and fast (ad voiceover) 300+. Real recording is affected by emotion and phrasing, so calibrate against a sample from the finished piece; what this tool gives is a theoretical estimate.",
        "How is duration computed for mixed Chinese and English?",
        "It is more accurate to count Chinese by characters per minute and English by words per minute separately (English words generally take longer than Chinese characters). For mixed copy, count them separately and add up, which fits real reading far better than a uniform character-count estimate.",
        "About Script Reading Duration",
        "Script Reading Duration is an online tool in the marketing and promotion field. Marketing analysis tools that help quantify and evaluate marketing effect and ROI.",
        "Paste or enter your script content here...",
    ]))
    write('reach-frequency', build('reach-frequency', [
        "🧮 Reach Calculator",
        "Calculate ad campaign reach, frequency and GRP metrics",
        "\"Calculate ad campaign reach, frequency and GRP metrics\" runs a professional calculation on the input parameters and outputs the result.",
        "📖 Read the Reach Calculator user guide",
        "Basic calculation",
        "Multi-flight campaign",
        "People reached (Reach)",
        "Total impressions (Impressions)",
        "Ad campaign cost (CNY)",
        "🧮 Calculate metrics",
        "Cumulative reach across multiple campaign flights (using a random probability model)",
        "Target audience",
        "Number of flights",
        "Per-flight single reach rate (%)",
        "Calculate cumulative reach",
        "Key metrics:",
        "Reach = people reached / target audience; average frequency = total impressions / people reached; GRP (gross rating points) = reach × frequency; CPM = cost / impressions × 1000; CPR = cost / people reached.",
        "📚 Deep Dive: Reach Calculator",
        "Given the target audience and the number of people reached, compute Reach% (the non-duplicated reach share) to judge how broad the coverage is.",
        "Divide total impressions by people reached to get the average frequency, to assess how many times the ad was seen.",
        "Combine it with the cost to get CPM and compare the value of several campaign plans horizontally.",
        "Campaign reach, frequency and CPM",
        "Target audience 1 million, reach 400 thousand, total impressions 2 million, cost 200 thousand. Reach = 40÷100 = 40%; average frequency = 2 million÷400 thousand = 5 times; CPM = 200000 ÷ (400 thousand÷1000) = 500 CNY per thousand.",
        "What is the difference between Reach and Impressions?",
        "Impressions is the total number of displays (including repeat exposures to the same person), while Reach is the share of people who saw it at least once. With the same 2 million impressions, if they concentrate on a few people, Reach is low and frequency is high; if spread out, the opposite. The two must be read together to judge coverage quality.",
        "What is the point of a frequency cap?",
        "A frequency cap prevents the same user from seeing the same ad too many times, which causes annoyance or wastes budget. Three to five times per cycle is common, balancing memorization against harassment, and the media strategy is authoritative.",
        "About Reach Calculator",
        "Reach Calculator is an online tool in the marketing and promotion field. Marketing analysis tools that help quantify and evaluate marketing effect and ROI.",
    ]))
    write('ad-size', build('ad-size', [
        "📣 Ad Size Conversion",
        "Pixel / millimeter / inch conversion with a quick reference of common ad sizes",
        "Core formula (in terms of input variables): Math.round(wMM÷25.4×dpi); Math.round(hMM÷25.4×dpi); min(220,w÷5)",
        "📖 Read the Ad Size Conversion user guide",
        "Quick selection of standard sizes",
        "Pixels px",
        "DPI resolution",
        "72 (screen)",
        "96 (web standard)",
        "150 (large format)",
        "300 (print)",
        "📣 Convert size",
        "📚 Deep Dive: Ad Size Conversion",
        "Design files are annotated in pixels (such as 1920×1080 px), and when delivering print or large-format materials you need to convert to centimeters or millimeters, with the physical size given for the target DPI.",
        "Given the print size and the DPI (such as 300 DPI for a business card), work back to the required pixels so the exported image is not blurry from insufficient resolution.",
        "When one creative has to run on both the web (96 DPI) and outdoor large format (150 DPI), quickly get two sets of pixel specs.",
        "Convert 1920×1080 px to centimeters at 96 DPI",
        "Width 1920 px, height 1080 px, DPI 96. Inches = pixels / DPI, and centimeters = inches × 2.54. Width = 1920/96×2.54 ≈ 50.8 cm, height = 1080/96×2.54 ≈ 28.6 cm. If you switch to 300 DPI for print, the same physical size needs 6000×3375 px.",
        "How do you convert between pixels and physical size?",
        "Core formula: pixels = physical inches × DPI, and physical inches = centimeters ÷ 2.54. So physical centimeters = pixels ÷ DPI × 2.54. The same pixel value maps to different physical sizes at different DPIs, so always settle the DPI before computing for print.",
        "Which DPI should I choose?",
        "Screen and web typically use 72-96 DPI, photo and large format about 100-150 DPI, and fine print (brochures, packaging) uses 300 DPI. The higher the DPI, the more pixels and the bigger the file. Follow the requirements of the material process; this tool only demonstrates size conversion.",
        "About Ad Size Conversion",
        "Ad Size Conversion is an online tool in the marketing and promotion field. Marketing analysis tools that help quantify and evaluate marketing effect and ROI.",
    ]))
    write('color-convert', build('color-convert', [
        "🎨 Color Conversion",
        "RGB/HEX/CMYK/HSL color space conversion with spot color references",
        "\"RGB/HEX/CMYK/HSL color space conversion with spot color references\" runs a professional calculation on the input parameters and outputs the result.",
        "📖 Read the Color Conversion user guide",
        "HEX value",
        "🎨 Copy color value",
        "Common spot color (Pantone) references",
        "Color space:",
        "RGB is for screen display and CMYK is for print. Converting RGB to CMYK loses gamut. HSL is based on hue / saturation / lightness, and Lab is a device-independent color space closest to human perception.",
        "📚 Deep Dive: Color Conversion",
        "Design files are annotated in RGB/HEX and must be converted to CMYK for print delivery, so the on-screen color does not drift too far from the finished product.",
        "Get the HEX value from an eyedropper and quickly obtain the RGB components for reuse in front-end code.",
        "Fine-tune hue and saturation with HSL to build same-hue gradients or a contrasting palette.",
        "Pure red RGB to HEX to CMYK",
        "RGB(255,0,0) → HEX #FF0000 → CMYK(0%,100%,100%,0%). Note that CMYK is a subtractive model: pure red in four-color printing comes from overprinting magenta and yellow, so dark red areas are prone to shifting color. Important brand colors are better printed as spot colors.",
        "Why can CMYK not reproduce some RGB colors?",
        "RGB is additive light with a wide gamut, while CMYK is subtractive ink with a narrow gamut, so bright blues, fluorescent greens and pure magentas turn dark and gray in print. Vivid on-screen colors often shift on paper, so key colors should use Pantone spot colors or a printed proof.",
        "Should a web page use HEX or RGB?",
        "Both are supported: HEX is more compact and historically compatible, while RGB/RGBA makes translucency and variable calculations easy. The numeric values of one color are equivalent, so pick whichever fits your team conventions; this tool handles the conversion.",
        "About Color Conversion",
        "Color Conversion is an online tool in the marketing and promotion field. Marketing analysis tools that help quantify and evaluate marketing effect and ROI.",
    ]))
    write('convert-26', build('convert-26', [
        "📣 Ad Size and Resolution Conversion (Pixel / Millimeter)",
        "Pixel / millimeter",
        "📖 Read the Ad Size and Resolution Conversion (Pixel / Millimeter) user guide",
        "Ad size",
        "Milli-ad size",
        "Kilo-ad size",
        "Resolution conversion",
        "Milli-resolution conversion",
        "Kilo-resolution conversion",
        "📚 Deep Dive: Ad Size and Resolution Conversion (Pixel / Millimeter)",
        "Convert the pixel dimensions of a design file into millimeters with a given coefficient, for annotating finished offline materials such as roll-up banners and posters.",
        "Given the physical size and the resolution coefficient, work back to the required pixels to guarantee a sharp output.",
        "Batch convert between px, mm, cm and in using the DPI relationship to unify specifications across many materials.",
        "Convert pixels to millimeters by coefficient",
        "Enter 1000 (px) with a conversion coefficient of 0.2646 (that is, 1px ≈ 0.2646mm at 96 DPI), converting from '",
        "Ad size' to 'Milli-ad size' → 1000×0.2646 ≈ 264.6 mm. With a 300 DPI coefficient of 0.0847 instead, the same 1000px is only 84.7mm, showing that at a higher DPI the same pixel count maps to a smaller physical size.",
        "How is the conversion coefficient determined?",
        "It is set by the target DPI: the inches corresponding to 1px = 1/DPI, and the millimeters = 25.4/DPI. At 96 DPI, 1px ≈ 0.2646mm; at 300 DPI, ≈ 0.0847mm. Picking the wrong DPI offsets the whole batch of material dimensions.",
        "What is the difference from the Ad Size Conversion tool?",
        "This tool focuses on batch and custom conversion with a coefficient (suited to templated material specs), while the other tool converts both ways from width, height and DPI and returns physical dimensions. Pick whichever matches the form of the data you have; the results agree.",
        "About Ad Size and Resolution Conversion (Pixel / Millimeter)",
        "Ad size and resolution conversion (pixel / millimeter). Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))
    write('convert-27', build('convert-27', [
        "🎨 Color (CMYK / RGB) Conversion and Spot Colors",
        "📖 Read the Color (CMYK / RGB) Conversion and Spot Colors user guide",
        "Milli-color conversion",
        "Kilo-color conversion",
        "Spot color",
        "Milli-spot color",
        "Kilo-spot color",
        "📚 Deep Dive: Color (CMYK / RGB) Conversion and Spot Colors",
        "Brand guidelines use RGB/HEX while the print shop needs CMYK, so convert both ways and check the color difference risk.",
        "Set the primary brand color as a spot color (Spot/Pantone) printed on its own plate outside the four process colors, which keeps color stable across large print runs.",
        "When one spot color is used in many places in the design file, unify its conversion and management so different print runs do not shift.",
        "Brand blue RGB to CMYK and spot color proofing",
        "Brand blue RGB(0,114,187) → CMYK approximately (100%,39%,0%,27%). Four-color overprinting on cheap paper tends to shift purple, so for large solid areas in a logo it is better to use a Pantone spot color (285 C is a close match) printed on its own plate for a more stable color.",
        "What is a spot color?",
        "A spot color is a separately mixed ink prepared in advance (such as a Pantone swatch) that does not rely on overprinting the four CMYK inks, so the color is precise and consistent, and it is often used for logos and corporate primary colors. The cost is one extra printing plate and higher expense, which is only worth it for large areas or key colors.",
        "Why does the color on screen never quite match the print?",
        "The screen is self-luminous RGB with a wide gamut, while print is CMYK ink with a narrow gamut, so the gap is natural. Narrowing it means designing in CMYK mode, using spot colors for key colors, and approving a proof before a large run. This tool only does numeric conversion; the proof or the printer's confirmation is final.",
        "About Color (CMYK / RGB) Conversion and Spot Colors",
        "Color (CMYK / RGB) conversion and spot colors. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
        "How to use Color (CMYK / RGB) Conversion and Spot Colors",
        "From",
        "to",
    ]))
    write('storyboard-timeline', build('storyboard-timeline', [
        "📜 Storyboard Timeline",
        "Plan the timeline of a video ad storyboard script with automatic duration totals",
        "\"Plan the timeline of a video ad storyboard script with automatic duration totals\" runs a professional calculation on the input parameters and outputs the result.",
        "📖 Read the Storyboard Timeline user guide",
        "Total video duration target (seconds)",
        "+ Add shot",
        "Load template",
        "Export script",
        "📚 Deep Dive: Storyboard Timeline",
        "Enter the duration in seconds of each scene of the video; the tool sums them automatically and compares against the total duration target, so an overrun shows up immediately.",
        "Label each scene with the shot size (wide / full / medium / close / extreme close) and a picture description to produce a deliverable storyboard sheet.",
        "Redistribute the duration of each shot under the total duration constraint, keeping the narrative pacing within bounds.",
        "Validate the durations of a five-scene plan",
        "Scene durations [8,12,10,15,5] seconds total 50 seconds, matching the 50-second target; the shot size sequence is full - medium - close - extreme close - full, so the pacing goes from wide to tight and then wraps up. If the total target changes to 45 seconds, compressing the 15-second shot to 10 seconds is enough.",
        "What if the total exceeds the target?",
        "Compress low-information or repetitive medium and close shots first, or merge adjacent scenes; cut secondary shots if necessary. Keep the opening and the conversion shot intact, since the middle demo shots are the most adjustable. The tool sums in real time, so you can adjust while watching.",
        "How do I use shot sizes (wide, full, medium, close, extreme close)?",
        "The wide and full shots establish the environment, the medium shot carries action, and the close or extreme close shot captures emotion and detail. The conventional structure 'wide - medium - close - extreme close - medium' balances information and emotion. Shot sizes are only shooting guidance; the director's storyboard is authoritative.",
        "About Storyboard Timeline",
        "Storyboard Timeline is an online tool in the marketing and promotion field. Marketing analysis tools that help quantify and evaluate marketing effect and ROI.",
    ]))
    write('generator-time', build('generator-time', [
        "📜 Video Storyboard Script Timeline Generator",
        "An online tool for generating a video storyboard script timeline",
        "📖 Read the Video Storyboard Script Timeline Generator user guide",
        "Single shot duration = total duration ÷ number of shots (when allocating by weight, single shot duration = total duration × that shot's weight ÷ sum of weights); the start time of each shot = Σ of the durations of the shots before it; transition durations follow the type (hard cut 0 seconds, dissolve 0.3 to 0.5 seconds, wipe 0.5 to 1 second); the check formula is total duration − Σ shot durations − Σ transition durations = 0, which confirms that the timeline allocation has no gaps.",
        "📚 Deep Dive: Video Storyboard Script Timeline Generator",
        "Take the total video duration target (such as 60 seconds) and divide it evenly by the number of shots to be generated, quickly building a timeline skeleton.",
        "Automatically arrange start and end timecodes for every storyboard, which helps with editing alignment and lip-sync for the voiceover.",
        "Fine-tune the duration of individual shots on an existing rhythm and regenerate the overall timeline while keeping the total duration unchanged.",
        "Split a 60-second video into 6 storyboard shots",
        "With a total video duration of 60 seconds and 6 generated shots, each segment is 10 seconds. Timeline: 00:00-00:10 opening, 00:10-00:20 pain point, 00:20-00:30 product, 00:30-00:40 demo, 00:40-00:50 testimonial, 00:50-01:00 conversion. Editing can simply align to this.",
        "How do I decide the number of storyboard shots?",
        "Usually the six-part structure of opening, pain point, solution, demo, trust and action, which can be compressed to 3-4 shots for a 15-second short video. Fewer shots mean higher information density per shot, more shots mean a calmer pace. This tool divides duration evenly; the actual structure is decided by the creative concept.",
        "What format is a timecode in?",
        "Usually hours:minutes:seconds (such as 00:00:10) or hours:minutes:seconds:frames. This tool outputs a second-level timeline, and editing software can convert it into a frame-accurate timecode for precise picture and audio alignment.",
        "About Video Storyboard Script Timeline Generator",
        "Video storyboard script timeline generation. Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected.",
    ]))


if __name__ == '__main__':
    main()
