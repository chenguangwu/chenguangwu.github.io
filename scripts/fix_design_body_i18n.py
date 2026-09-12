#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""design 分类英文态数据源根治：同步三端 + 补缺失条目 + 报告孤儿键。

背景（与 general / finance 同坑，§6「英文态数据源三处」）：
  页面可见英文（p / desc-en meta / ed）只是表象；`?lang=en-US` 与 industry JSON 的 ed
  还取决于三个数据源，只改页面会导致英文态仍是占位串 / 工具代号：
    ① i18n/tools/design-body.json    -> build `_prerender_tool_body` 预渲染 h2 + 首个 <p>
    ② i18n/tools/design.json en-US   -> industry JSON 的 ed 最高优先级源（tool_desc_source.en_desc）
    ③ i18n/tools/_en_override.json   -> 运行时 en（h2/h1）与 ed

用法：
  python3 scripts/fix_design_body_i18n.py --dry-run
  python3 scripts/fix_design_body_i18n.py --apply
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'design')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'design-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'design.json')

# NAME = 英文名（h2 / h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
# 每条依据页面 zh-CN intro 的实际用途撰写，避免 "free online tool" 类套话。
NAME = {
    'analysis': 'Image Palette Analyzer',
    'audio-recorder': 'Audio Recorder & Processor',
    'avatar-generator': 'Avatar Generator',
    'aztec-code': 'Aztec Code Generator',
    'badge-generator': 'Badge Generator',
    'base64-to-image': 'Base64 to Image Converter',
    'blueprint-grid': 'Blueprint Grid Background Generator',
    'border-radius-generator': 'Border Radius Generator',
    'bpm-tapper': 'BPM Tapper',
    'breakpoint-queries': 'Responsive Breakpoint Query Generator',
    'button-generator': 'CSS Button Generator',
    'card-generator': 'CSS Card Generator',
    'checker': 'WCAG Contrast Check',
    'checkerboard-generator': 'Checkerboard Pattern Generator',
    'color-contrast-check': 'Color Contrast Checker',
    'color-palette-generator': 'Color Palette Generator',
    'color-palette': 'Color Scheme Generator',
    'color-picker': 'Color Picker & Converter',
    'color-shade-generator': 'Color Shade & Tint Generator',
    'color-temperature-converter': 'Color Temperature (Kelvin) Converter',
    'contrast-checker': 'Contrast Ratio Checker',
    'css-animation-generator': 'CSS Animation Generator',
    'css-border-radius': 'CSS Border Radius Generator',
    'css-box-shadow-generator': 'CSS Box Shadow Generator',
    'css-grid-generator': 'CSS Grid Layout Generator',
    'css-text-shadow': 'CSS Text Shadow Generator',
    'data-matrix': 'Data Matrix Code Generator',
    'depth-of-field-calculator': 'Depth of Field Calculator',
    'dot-pattern': 'Dot Pattern Generator',
    'exposure-triangle-calculator': 'Exposure Triangle Calculator',
    'favicon-from-emoji': 'Emoji Favicon Generator',
    'favicon-from-text': 'Text Favicon Generator',
    'favicon-generator': 'Favicon Generator',
    'flexbox-generator': 'Flexbox Layout Generator',
    'focal-length-equivalent': 'Focal Length Equivalent Calculator',
    'font-pairing': 'Font Pairing Suggester',
    'font-preview': 'Font Preview Tool',
    'generator-10': 'CSS Keyframe Animation Generator',
    'generator-11': 'CSS Background Pattern Generator',
    'generator-12': 'Particle Effect Generator',
    'generator-6': 'Box Shadow Generator (Visual)',
    'generator-7': 'CSS Border Style Generator',
    'generator-8': 'QR Code Generator',
    'generator-9': 'Barcode Generator (EAN-13)',
    'glassmorphism-generator': 'Glassmorphism CSS Generator',
    'gradient-from-color': 'Gradient from Color Generator',
    'gradient': 'CSS Gradient Generator',
    'grid-pattern': 'Grid Pattern Generator',
    'identicon-generator': 'Identicon Avatar Generator',
    'image-color-picker': 'Image Color Picker',
    'image-compress': 'Image Compressor',
    'image-cropper': 'Image Cropper',
    'image-dpi-converter': 'Image DPI/PPI Converter',
    'image-flipper': 'Image Flipper',
    'image-format-converter': 'Image Format Converter',
    'image-mosaic': 'Image Mosaic Tool',
    'image-resizer': 'Image Resizer',
    'image-rotator': 'Image Rotator',
    'image-rounded-corners': 'Rounded Corner Image Generator',
    'image-to-ascii': 'Image to ASCII Art Converter',
    'image-to-base64': 'Image to Base64 Converter',
    'image-watermark': 'Image Watermark Tool',
    'initials-avatar': 'Initials Avatar Generator',
    'iso-noise-reference': 'ISO Noise Reference',
    'isometric-grid': 'Isometric Grid Generator',
    'loading-dots': 'Loading Dots CSS Generator',
    'material-color': 'Material Design Color Palette',
    'mesh-gradient': 'Mesh Gradient Generator',
    'music-scale-reference': 'Music Scale & Key Reference',
    'neomorphism-generator': 'Neumorphism CSS Generator',
    'palette-extractor': 'Median-Cut Palette Extractor',
    'particle-effect-generator': 'Interactive Canvas Particle System',
    'pattern-generator': 'SVG Pattern Generator',
    'photo-aspect-ratio-calculator': 'Photo Aspect Ratio Calculator',
    'photo-print-size': 'Photo Print Size Calculator',
    'photo-storage-calculator': 'Photo Storage Calculator',
    'pixel-art-generator': 'Pixel Art Generator',
    'pixel-art': 'Pixel Art Editor',
    'png-to-svg': 'PNG to SVG Converter',
    'progress-bar-generator': 'Progress Bar Generator',
    'px-to-rem': 'Px to Rem Converter',
    'qr-code-styled': 'Styled QR Code Generator',
    'rem-to-px': 'Rem to Px Converter',
    'ripple-effect': 'Ripple Effect Generator',
    'shadow-generator-advanced': 'Advanced Shadow Generator',
    'shadow-generator': 'CSS Shadow Generator',
    'shutter-speed-calculator': 'Safe Shutter Speed Calculator',
    'signature-pad': 'Signature Pad',
    'skeleton-loader': 'Skeleton Loader Generator',
    'spacing-scale': 'Spacing Scale Generator',
    'spectrum-visualizer': 'Audio Spectrum Visualizer',
    'spinner-generator': 'CSS Spinner Generator',
    'stripe-pattern': 'Stripe Pattern Generator',
    'svg-minifier': 'SVG Minifier',
    'svg-to-png': 'SVG to PNG Converter',
    'svg-viewer': 'SVG Viewer',
    'tailwind-colors': 'Tailwind CSS Color Palette',
    'text-shadow-generator': 'Text Shadow Generator',
    'toast-generator': 'Toast Notification Generator',
    'typography-scale': 'Typography Scale Generator',
    'vh-vw': 'Viewport Unit (vw/vh) Converter',
    'waveform-visualizer': 'Audio Waveform Visualizer',
    'web-audio-metronome': 'Web Audio Metronome',
}

INTRO = {
    'analysis': 'Upload an image and analyse its pixels with Canvas to extract the dominant colour and a full palette with proportions, all locally.',
    'audio-recorder': 'Record audio in the browser, adjust volume and playback speed and visualise the waveform, with nothing uploaded.',
    'avatar-generator': 'Generate geometric, pixel or gradient avatars at random or from a seed, tweak colours and shapes and download PNG or SVG.',
    'aztec-code': 'Turn text or a URL into a simplified Aztec barcode for mobile scanning on tickets and logistics labels, generated locally.',
    'badge-generator': 'Design rounded or shield-shaped badges with custom text, colours and icons, preview live and export an image for events and awards.',
    'base64-to-image': 'Decode a Base64 string back into a viewable image, or encode an image to Base64 for embedding in HTML, CSS and documents.',
    'blueprint-grid': 'Create a blueprint-style grid background with adjustable density, cell size and colour for engineering sketches and slide backdrops.',
    'border-radius-generator': 'Drag to set the corner radius of an element and copy ready-to-use CSS border-radius, with independent control of all four corners.',
    'bpm-tapper': 'Tap along to a track or press the space bar to measure its tempo in beats per minute, useful for musicians and dancers.',
    'breakpoint-queries': 'Pick the device breakpoints you need and generate mobile-first (min-width) media query CSS without writing it by hand.',
    'button-generator': 'Style a button background, radius, shadow and hover state visually and copy the generated CSS, with several built-in presets.',
    'card-generator': 'Adjust card radius, shadow, padding and colours with sliders and copy the CSS, previewing the result live for landing pages and lists.',
    'checker': 'Enter foreground and background colours to compute the WCAG 2.1 contrast ratio and see whether text passes the AA and AAA levels.',
    'checkerboard-generator': 'Generate a checkerboard pattern with adjustable cells and colours for chess demos, backgrounds and game art, exportable as an image.',
    'color-contrast-check': 'Check whether text is readable by computing the WCAG 2.1 contrast ratio between a foreground and background colour and judging AA/AAA.',
    'color-palette-generator': 'Set a base colour and a harmony rule to build a matching palette, then export the swatches, gradients and CSS variables.',
    'color-palette': 'Drag a point on the colour wheel to set the base hue and get complementary, analogous and triadic schemes with live preview and values.',
    'color-picker': 'Pick or enter a colour and convert between HEX, RGB, HSL, HSV and CMYK, with preset swatches and one-click copy.',
    'color-shade-generator': 'Mix a base colour with white for lighter tints and with black for darker shades to build a coordinated ladder for buttons and backgrounds.',
    'color-temperature-converter': 'Convert between Kelvin colour temperature and RGB to understand white balance and light colour for photography and design.',
    'contrast-checker': 'Verify the WCAG contrast ratio between text and background in real time to keep copy readable for designers and developers.',
    'css-animation-generator': 'Choose an animation type, tune its parameters, preview the result live and copy the CSS keyframes for front-end motion work.',
    'css-border-radius': 'Tweak the radius visually and generate the matching CSS border-radius, supporting per-corner values and percentages.',
    'css-box-shadow-generator': 'Adjust offset, blur, spread and colour to produce CSS box-shadow code, with multiple layers for layered depth.',
    'css-grid-generator': 'Build a CSS Grid layout by setting columns, track sizing, gaps and breakpoints, then copy the generated CSS and HTML.',
    'css-text-shadow': 'Tune the offset, blur and colour of a text shadow and copy CSS text-shadow code for headings and taglines.',
    'data-matrix': 'Encode text or a part number into a simplified Data Matrix code for small-area marking on industrial parts and materials, offline.',
    'depth-of-field-calculator': 'From aperture, focal length and distance, compute near and far depth of field and hyperfocal distance to control sharpness and bokeh.',
    'dot-pattern': 'Create an even or offset dot texture with adjustable dot size, spacing and colour, exportable as a transparent or solid background image.',
    'exposure-triangle-calculator': 'Convert between aperture, shutter speed and ISO at constant exposure to find equivalent settings for a shot.',
    'favicon-from-emoji': 'Render a chosen emoji into a website favicon and export multi-size ICO or PNG icons, generated entirely in the browser.',
    'favicon-from-text': 'Type a letter or a short text to build a clean text-based favicon with adjustable colours and fonts for a quick brand mark.',
    'favicon-generator': 'Upload an image or type text or emoji to generate multi-size website icons with optional rounding and background, downloadable as .ico.',
    'flexbox-generator': 'Pick the key flex properties and immediately get the matching display:flex CSS with a live preview of one, two and three items.',
    'focal-length-equivalent': 'Convert focal length across sensor formats, compare angles of view and get lens suggestions for camera gear selection.',
    'font-pairing': 'Browse curated font combinations and copy the matching CSS to give a page or a poster a coherent typographic voice.',
    'font-preview': 'Preview how a line of text renders across system fonts side by side, and click a card to copy its font-family CSS.',
    'generator-10': 'Compose a CSS keyframe animation visually, adjust duration, easing and properties, preview it live and export the @keyframes code.',
    'generator-11': 'Tune parameters to build a tileable CSS background texture such as dots, grids or waves, with live preview and exported code.',
    'generator-12': 'Adjust particle count, speed, colour and gravity to preview an animated particle field, then export Canvas code or an image.',
    'generator-6': 'Drag controls to set the offset, blur, spread and colour of a box shadow and copy the CSS, including inset and multiple layers.',
    'generator-7': 'Configure border width, style, radius and colour with per-side control and copy the CSS for dividers and card outlines.',
    'generator-8': 'Turn a URL or text into a QR code with adjustable size, error-correction level and colours, downloadable for cards and posters.',
    'generator-9': 'Generate EAN-13 and other common barcodes from digits with an automatic check digit, downloadable for product labels and warehousing.',
    'glassmorphism-generator': 'Adjust blur, transparency and background to create a frosted-glass CSS effect for modern UI cards and panels.',
    'gradient-from-color': 'Derive same-hue or complementary gradients from a single colour, tune the angle and stops, preview live and copy the CSS.',
    'gradient': 'Configure the start and end colours, angle and stops of a linear or radial gradient and copy the resulting CSS gradient code.',
    'grid-pattern': 'Generate square or ruled grid backgrounds with adjustable spacing and line colour for engineering layouts, web textures and print.',
    'identicon-generator': 'Hash a name or string into a symmetric geometric identicon, a common default avatar for accounts without a picture.',
    'image-color-picker': 'Upload an image and click any pixel to read its HEX or RGB colour, with magnified sampling and a history of picks.',
    'image-compress': 'Compress PNG, JPG or WebP in the browser by quality and compare the size before and after, without uploading the original.',
    'image-cropper': 'Crop an image by dragging a free or fixed-ratio selection with live preview, ideal for avatars, ID photos and thumbnails.',
    'image-dpi-converter': 'Convert between pixel and physical dimensions and work out DPI/PPI for accurate print and screen output.',
    'image-flipper': 'Mirror an image horizontally or vertically to fix reversed shots or build symmetric compositions, processed locally.',
    'image-format-converter': 'Convert between PNG, JPEG, WebP and BMP with adjustable quality and size, handled entirely in the browser.',
    'image-mosaic': 'Pixelate an image with an adjustable block size over the whole picture or a selected area to blur sensitive content locally.',
    'image-resizer': 'Resize an image by pixels or percentage, optionally keeping the aspect ratio, and set the output quality before download.',
    'image-rotator': 'Rotate an image by any angle or in 90-degree steps to correct framing, then export the rotated result locally.',
    'image-rounded-corners': 'Round the corners of an uploaded image with live preview and export a PNG, handy for avatars and card thumbnails.',
    'image-to-ascii': 'Map image brightness to ASCII characters with adjustable width, contrast, brightness and character set, previewed and copied locally.',
    'image-to-base64': 'Encode an image into Base64 text for inlining in HTML or CSS, or decode it back, all without leaving the browser.',
    'image-watermark': 'Add a text or image watermark to photos with control over position, opacity, tiling and size, processed locally in batch.',
    'initials-avatar': 'Turn a name or initials into a coloured letter avatar with adjustable font, radius and palette, downloadable as PNG or SVG.',
    'iso-noise-reference': 'Compare noise levels across ISO settings for common cameras to choose a suitable sensitivity for a shoot.',
    'isometric-grid': 'Generate an isometric (2.5D) grid background with adjustable cell size and colours for game maps, illustrations and diagrams.',
    'loading-dots': 'Preview a three-dot bouncing loading animation, tune its speed and colour and copy the CSS for page placeholders.',
    'material-color': 'Browse the full Material Design palette of 19 colour families at 10 shades each and click a swatch to copy its HEX value.',
    'mesh-gradient': 'Build a multi-colour mesh gradient background by dragging colour stops, then export the gradient as an image or CSS.',
    'music-scale-reference': 'Look up the notes and accidentals of major and minor scales and modes to check key signatures and chord tones.',
    'neomorphism-generator': 'Tune distance, intensity, blur and base colour to generate soft, extruded neumorphic shadow and radius CSS for UI elements.',
    'palette-extractor': 'Upload an image and extract its dominant colours with the median-cut algorithm, then edit and export the palette as CSS or JSON.',
    'particle-effect-generator': 'A real-time Canvas particle system with multiple emitters, mouse interaction and presets, with every parameter adjustable live.',
    'pattern-generator': 'Build seamless SVG background textures such as dots, stripes, grids and waves, then export the CSS background code.',
    'photo-aspect-ratio-calculator': 'Enter pixels or a target size to compute a photo aspect ratio such as 16:9 or 4:3 and the matching length of the other side.',
    'photo-print-size': 'From pixel dimensions and print DPI, work out the best physical print size and compare it against standard paper formats.',
    'photo-storage-calculator': 'Estimate the memory card space needed from camera resolution, file format and number of shots to plan your cards.',
    'pixel-art-generator': 'Draw a pixel picture on a grid, change the grid size and palette, and export the result as character art or CSS code.',
    'pixel-art': 'A grid-based pixel editor with pen, eraser, fill and eyedropper tools plus undo/redo and PNG export at original or enlarged size.',
    'png-to-svg': 'Convert a raster PNG into vector SVG by tracing or embedding for lossless scaling, processed locally without uploading.',
    'progress-bar-generator': 'Adjust the length, thickness, radius, gradient and animation of a progress bar, preview it live and copy the HTML/CSS.',
    'px-to-rem': 'Convert pixel values to rem against a chosen root font size, the usual way to keep responsive and accessible layouts.',
    'qr-code-styled': 'Generate a standard QR code from the bundled qrcode.js library and customise its style, entirely in the browser.',
    'rem-to-px': 'Convert rem values from a spec or design file back to pixels using the current root font size for fixed-size contexts.',
    'ripple-effect': 'Create a Material Design ripple click effect, tune the colour, spread radius and duration and export the CSS/JS snippet.',
    'shadow-generator-advanced': 'Fine-tune multi-layer outer and inner shadows with blur and spread and copy advanced box-shadow or drop-shadow CSS.',
    'shadow-generator': 'Adjust the offset, blur, spread and colour of outer and inner shadows with presets and copy the CSS box-shadow code.',
    'shutter-speed-calculator': 'Estimate a safe handheld shutter speed from the focal length to avoid motion blur, useful when setting up a shot.',
    'signature-pad': 'Draw a smooth signature with mouse or touch using quadratic curves, undo strokes and export a transparent PNG.',
    'skeleton-loader': 'Configure list, card or media skeleton placeholders with adjustable radius, spacing and shimmer, and export the CSS.',
    'spacing-scale': 'Generate a consistent spacing ladder from a base unit such as 4/8/16 multiples and copy it as CSS variables for design systems.',
    'spectrum-visualizer': 'Plot live audio as a frequency-domain spectrum using the Web Audio API, with FFT analysis and peak inspection.',
    'spinner-generator': 'Choose from spin, ring and dot loading templates, tune the size, colour and speed and copy the CSS for page placeholders.',
    'stripe-pattern': 'Generate horizontal, vertical or diagonal stripe textures with adjustable width and two-tone colours for packaging and web backgrounds.',
    'svg-minifier': 'Paste SVG code to strip comments, whitespace and default attributes, shrinking the file, with a before/after comparison.',
    'svg-to-png': 'Rasterise a vector SVG into a PNG with a chosen size and background for contexts that cannot render SVG, processed locally.',
    'svg-viewer': 'Paste or upload SVG code to preview the graphic in the browser with zoom and copy the matching CSS for embedding.',
    'tailwind-colors': 'Browse the full Tailwind CSS palette of 22 colour families at 11 shades and click a swatch to copy it in various formats.',
    'text-shadow-generator': 'Adjust the offset, blur, colour and multiple layers of a text shadow, preview it live and copy the CSS for headings.',
    'toast-generator': 'Configure toast text, position, icon and animation and generate the matching HTML/CSS/JS snippet for quick integration.',
    'typography-scale': 'Build a font-size ladder from a ratio such as 1.25 and export a heading-to-body scale table and CSS for a consistent hierarchy.',
    'vh-vw': 'Convert between viewport units and pixels: vw and vh are 1% of the viewport width and height, handy for full-screen layouts.',
    'waveform-visualizer': 'Plot audio or signal data as a time-domain waveform, with file upload, live rendering and zoom for analysis and teaching.',
    'web-audio-metronome': 'A precise metronome built on the Web Audio API with selectable time signatures for instrument practice and rhythm training.',
}

# 缺 zh-CN 条目的工具（页面中文标题存在但 i18n 无条目）：slug -> (中文名, 中文简介)
ZH_FILL = {
    'breakpoint-queries': ('响应式断点生成器', '选择需要适配的设备断点，自动生成移动优先（min-width）的媒体查询 CSS 代码。'),
    'color-contrast-check': ('颜色对比度检查器', '输入前景色与背景色，按 WCAG 2.1 计算对比度比值，判定文字是否达到 AA / AAA 无障碍标准。'),
    'color-shade-generator': ('颜色明暗生成器', '在基色上按比例混入白色得到更亮的 tint、混入黑色得到更暗的 shade，指定档数生成协调的明暗色卡。'),
    'css-grid-generator': ('CSS 栅格布局生成器', '设置列数、列宽方式、间距与断点，快速生成 CSS Grid 布局并一键复制 CSS 与 HTML 代码。'),
    'flexbox-generator': ('Flexbox 布局生成器', '选择关键 flex 属性，立即得到对应的 display:flex CSS，并实时预览 1 / 2 / 3 个项目的排列效果。'),
    'pixel-art-generator': ('像素画生成器', '在网格上点击上色绘制像素画，可调整网格大小与调色板，完成后导出为字符画或 CSS 代码。'),
    'px-to-rem': ('px 转 rem 计算器', 'rem 相对根元素字体大小，做响应式与可访问性布局时常用来替代写死的 px。输入像素值与根字号即可得到 rem 值。'),
    'rem-to-px': ('rem 转 px 计算器', '把以 rem 为单位的标注或设计稿按当前根字号反算成 px，便于落地到固定尺寸场景。'),
    'vh-vw': ('视口单位转换（vh / vw ↔ px）', 'vw 为视口宽度的 1%，vh 为视口高度的 1%。选择模式并填入基准视口尺寸即可在视口单位与 px 之间换算。'),
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov = load(OV)
    body = load(BODY)
    gis = load(GIS)

    chg_en = chg_ed = chg_body = chg_gis = added_body = added_gis = added_zh = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'design/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'design'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'design')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + design-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + design.json 新增条目:', slug)
        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if slug in ZH_FILL:
            if not isinstance(g.get('zh-CN'), dict):
                zh_name, zh_intro = ZH_FILL[slug]
                g['zh-CN'] = {'h1': zh_name, 'title': zh_name, 'intro': zh_intro, 'desc': zh_name}
                added_zh += 1
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # 孤儿键：body 中存在但全站无对应页面（与 general 的 random-10 同类）
    orphans = []
    all_basenames = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'tools', '*', '*.html'))}
    for key in list(body.keys()):
        if key not in all_basenames:
            orphans.append(key)
    print('\n--- 汇总 ---')
    print('design 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('design-body 更新:', chg_body, ' 新增:', added_body)
    print('design.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis, ' 补 zh-CN:', added_zh)
    print('design-body 孤儿键:', orphans)

    if a.dry_run:
        for s in slugs[:3]:
            print('\n预览 %s:\n  name = %r\n  intro= %r' % (s, NAME[s], INTRO[s]))
        return 0

    json.dump(ov, open(OV, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump(body, open(BODY, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(gis, open(GIS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('\n已写入：_en_override.json(indent=1) / design-body.json(indent=2) / design.json(indent=2)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
