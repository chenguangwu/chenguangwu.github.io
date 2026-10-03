#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'image')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'image')
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
    out = {'slug': slug, 'industry': 'image', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
#!/usr/bin/env python3
def main():
    write('image-watermark', build('image-watermark', [
"🏋️ Image Watermark Tool",
"Add a text or image watermark after uploading an image, with 9-grid positioning, custom coordinates, full-image tiling and rotation, live preview and export. Processing is entirely local and images are never uploaded.",
"Performs a professional calculation based on the entered parameters and outputs the result: add a text or image watermark after uploading an image, with 9-grid positioning, custom coordinates, full-image tiling and rotation, live preview and export. Processing is entirely local and images are never uploaded.",
"Image Watermark Adding Tool",
"Supports PNG / JPG / WEBP / GIF / BMP and other formats the browser can decode",
"Dimensions:",
"Type:",
"File size:",
"🎨 Watermark Settings",
"📝 Text watermark",
"🖼️ Image watermark",
"📝 Text content",
"Microsoft YaHei",
"SimSun",
"SimHei",
"KaiTi",
"FangSong",
"🖼️ Watermark image",
"Click to upload a watermark image (transparent PNG recommended)",
"📍 Position",
"Tiled watermark (covering the whole image)",
"9-grid positioning",
"Custom coordinates",
"Margin",
"X coordinate (px)",
"Y coordinate (px)",
"🔲 Tiling settings",
"Offset stagger",
"👁️ Live Preview",
"Download JPEG",
"Download WebP",
"🔒 All image processing is done locally in the browser and files are never uploaded to any server. JPEG is lossy compression, so export PNG when the watermark needs high fidelity.",
"📚 In-depth analysis: image watermark (text / image / opacity / stroke)",
"Discourage unauthorized reuse of original images by adding a semi-transparent text or logo watermark.",
"Sign event posters with a watermark whose position and style stay consistent.",
"Semi-transparent text watermark",
"Text \"ToolBox watermark\", font size 24, color #ffffff, opacity 0.3, stroke 1px, tiled diagonally at the bottom right, so the original image is barely obscured.",
"Image logo watermark",
"Upload a logo as the watermark image, scale it to 15% of the original width, set opacity 0.5 and place it in the bottom-left margin area.",
"How much opacity stays unobtrusive?",
"For text watermarks 0.2–0.35 deters reuse without harming the subject; for logo-type marks 0.4–0.6 is more eye-catching but should not cover key content.",
"What is the stroke for?",
"When white text is hard to read on a light image, a 1px dark stroke improves contrast so the watermark stays readable on any background.",
"About the Image Watermark Tool",
"The image watermark tool is a pure front-end online watermarking tool built on the Canvas API. No software to install: after uploading an image you can add a text or image watermark, with 9-grid quick positioning, custom coordinates, full-image tiling and rotation angle, live preview and one-click export to PNG/JPEG/WebP. Everything is processed locally in the browser and images are never uploaded to a server.",
"Drag and drop or click to upload an image",
"Text watermark: font / size / color / opacity / stroke",
"Image watermark: upload mark / scale / opacity",
"9-grid quick positioning",
"Custom X/Y coordinates for precise placement",
"Full-image tiling and rotation angle",
"Staggered offset for tiled marks",
"Live preview, what you see is what you get",
"Export PNG / JPEG / WebP",
"Add a copyright watermark to photographic work",
"Protect e-commerce product images from reuse",
"Mark ID photos and document images with their purpose",
"Add a personal mark to social media images",
"Stamp a logo onto design drafts",
"Tiled watermark across batches of images",
"This tool runs entirely in the front end and image files are never uploaded to a server",
"JPEG does not support transparency, so the background is white on export",
"Very large images may take a few seconds to process, please wait for the preview to refresh",
"Changing any parameter refreshes the preview in real time, what you see is what you get",
"Enter watermark text",
"Watermark preview",
"Top left",
"Top center",
"Top right",
"Middle left",
"Middle right",
"Bottom left",
"Bottom center",
"Bottom right",
    ]))

    write('image-resize', build('image-resize', [
"🖼️ Image Resize Tool",
"Resize images online, scaling by ratio or to explicit dimensions, with smooth and fast algorithms, output to PNG/JPEG. Pure front-end Canvas processing, images are never uploaded.",
"Performs a professional calculation based on the entered parameters and outputs the result: resize images online, scaling by ratio or to explicit dimensions, with smooth and fast algorithms, output to PNG/JPEG. Pure front-end Canvas processing, images are never uploaded.",
"Supports PNG / JPEG / WebP / GIF / BMP, images are processed locally only",
"Original Image Information",
"Scale by ratio",
"Set explicit dimensions",
"Target dimensions (pixels)",
"Scaling algorithm",
"Smooth (high quality bilinear)",
"Fast (nearest neighbour)",
"PNG (lossless, supports transparency)",
"JPEG (lossy, smaller file size)",
"WebP (modern format)",
"Output quality",
"A higher value means better image quality and a larger file",
"Resize Preview",
"Generating preview…",
"Original dimensions",
"Dimensions after resizing",
"⬇ Download resized image",
"📋 Copy as Data URL",
"Select image again",
"🔒 Privacy: all image processing is done locally in the browser via Canvas and is never uploaded to any server.",
"This tool runs entirely in the front end and image data never leaves your device",
"Enlarging an image adds no real detail, so blur or jaggies may appear",
"JPEG/WebP do not support transparent backgrounds, so output is filled with white",
"Very large images (such as above 10000px) may process slowly due to memory limits",
"📚 In-depth analysis: image resize (percentage / target size / quality)",
"Avatar uploads are capped at 500×500, so an oversized original must be scaled down.",
"Print needs a large image, so you want to enlarge to the target width and height while keeping it sharp.",
"50% proportional scaling",
"A 2000×1500 image scaled to 50% outputs 1000×750, JPEG quality 85, and the file size drops from 1.8MB to 260KB.",
"Target width 1920",
"Original 4000×3000 with a target width of 1920 gives a proportional height of 1920×3000/4000 = 1440, so the output is 1920×1440.",
"How is the height computed for proportional scaling?",
"new width / original width = ratio, so new height = original height × the same ratio. Halving the width halves the height.",
"Why does enlarging look blurry?",
"Enlarging interpolates to fill pixels and adds no real detail; choosing the smooth algorithm gives softer edges but cannot conjure clarity.",
"About the Image Resize Tool",
"The image resize tool is an online image dimension adjustment tool built on the browser Canvas API. It supports scaling by percentage and specifying exact target width and height, can lock the aspect ratio with one click to preserve proportions, offers smooth (high quality bilinear) and fast (nearest neighbour) resampling algorithms, and supports PNG, JPEG and WebP output with adjustable quality. Everything is processed locally and images are never uploaded, so it is safe and reliable.",
"Scale by ratio (10%~200% slider plus preset buttons)",
"Specify exact target width and height, with aspect ratio lock",
"Two resampling algorithms: smooth / fast",
"Multi-format output: PNG / JPEG / WebP",
"Adjustable JPEG/WebP quality (10%~100%)",
"Live preview of the resize result and size comparison",
"Scale web images down to optimize loading speed",
"Batch size adjustment for thumbnails and covers",
"Fit social media avatar and cover dimensions",
"ID photo and registration photo pixel dimensions",
"Enlarge or reduce wallpapers and banners",
"Compress images in email attachments",
"Lock/unlock the aspect ratio",
"Lock aspect ratio",
    ]))


if __name__ == '__main__':
    main()