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
    write('image-mosaic', build('image-mosaic', [
"🖼️ Image Mosaic Effect Tool",
"Pixelate and mosaic images using the Canvas API, over the whole image or a selected region, with live preview and pure front-end processing with no upload.",
"/ Image Mosaic",
"Click or drag an image here",
"Supports JPG / PNG / WebP / GIF and more; images are processed locally in your browser only",
"Whole-image mosaic",
"Region mosaic",
"Press and drag on the image to select the region to pixelate; you can drag repeatedly to adjust, and it takes effect when you release.",
"Clear selection",
"👁 Hold to see the original",
"⬇ Download JPG",
"This tool runs entirely in the front end and image data is never uploaded to any server",
"In region mosaic mode, drag on the image to select the area to pixelate; it takes effect in real time when you release",
"The larger the pixel block the stronger the mosaic and the smaller the block the more refined; 8~30px usually gives the best result",
"Downloading PNG is lossless, while JPEG gives a smaller file with compression; choose as needed",
"📚 In-depth analysis: image mosaic (local redaction)",
"Mask private areas such as phone numbers, ID numbers and faces in screenshots.",
"Create an artistic pixelation effect without exposing detail.",
"Pixelate a face with a 10px block",
"Select the face region with a 10px block size and fill each 10×10 pixel area with its average colour; from a distance the facial features are no longer recognisable.",
"Strong pixelation with a 20px block",
"For sensitive text blocks use a 20px block size, which blurs more heavily and even strokes are hard to reconstruct, suiting high-privacy scenarios.",
"Is a larger block safer?",
"Yes. A larger block covers more pixels per cell, so the original information is harder to reconstruct; 10px is already enough to cover a face, and 20px suits text.",
"Can a mosaic be reversed?",
"One-way pixel averaging is irreversible, so the original detail is lost after export; confirm the masked area is large enough before publishing.",
"About the Image Mosaic Effect Tool",
"The image mosaic effect tool is an online image processing tool that pixelates images to create a redaction effect. It supports whole-image mosaic and local region selection modes, lets you adjust the pixel block size with a slider and preview in real time, and can export PNG or JPEG after processing. All computation runs locally in your browser and images are never uploaded to a server, so privacy is protected.",
"Two modes: whole-image mosaic and region selection mosaic",
"Pixel block size adjustable from 2~50px with live preview",
"Supports drag upload and touch selection, mobile friendly",
"Exports PNG/JPEG at the original resolution with lossless quality",
"Mask private information such as ID numbers, licence plates and faces",
"Pixelate sensitive content in shared screenshots",
"Create creative pixelated style images",
"Hide text, watermarks or account information in images",
"Blur over a local region",
"Local image processing for privacy-sensitive scenarios",
"Mosaic mode",
    ]))

    write('index', build('index', [
"🖼️ Image Processing Tools",
"Image Processing",
"Image Processing Tools",
"Image Compression Tool",
"Compress images online, supporting JPEG / WebP / PNG formats, quality adjustment, size limits and batch processing, all processed locally in the browser with no upload to the server.",
"Image Converter",
"Convert images between JPEG/PNG/WebP and output multiple formats, for web optimisation, size compression and compatibility work, processed locally in the front end with no upload.",
"Add a text or image watermark after uploading an image, with 9-grid positioning, custom coordinates, full-image tiling and rotation, live preview and export. Processed locally, images never uploaded.",
"Online image cropping tool: upload an image and drag to select a region for free cropping, with ratio lock and rotation, local preview and download, ideal for avatars and illustrations, pure front-end.",
"Upload multiple images, choose a layout template and compose them into one collage, with adjustable spacing, margin, background colour and drag-to-reorder, downloadable with one click.",
"WeChat Official Account Cover Generator",
"Online WeChat Official Account cover image generator with size templates and text/image layout, exporting compliant covers and thumbnails with one click, ideal for content images, pure front-end.",
"Rounded corner image generator. Upload an image in the front end and generate a PNG with the specified corner radius (batch capable, right-click to save); images never leave the device, for quick rounded avatars and cards.",
"Online image scaling and resizing, supporting ratio-based or explicit dimensions, smooth and fast algorithms, and PNG/JPEG output. Pure front-end Canvas processing, images never uploaded.",
"ID Photo Cropper",
"Online ID photo cropper providing standard size templates such as one inch and two inch; uploads are cropped automatically with background replacement, exporting compliant ID photos for resumes and documents, pure front-end.",
"Online GIF extraction tool that parses GIF89a frame by frame locally in the browser, supporting single-frame PNG download and batch export, for animation breakdown and material extraction, pure front-end.",
"Image Filters",
"After uploading a local image, overlay grayscale, blur, contrast, saturation and other filter effects in real time via CSS Filter and Canvas, with parameter sliders and result preview, all processed locally in the browser, ideal for quick beautification or a consistent style.",
"Online image rotation tool: upload an image and rotate it by any angle or a multiple of 90° with correction, supporting flipping, local preview and download, ideal for photo layout and correction, pure front-end.",
"Online image mosaic tool that pixelates the whole image or a local region for redaction, with a slider to adjust pixel block size and live preview, then download to protect privacy, running purely front-end.",
"Nine-Grid Cutter",
"The nine-grid cutter is a free online image processing tool, a free online image processing tool, where entering the parameters gives results in real time; runs purely front-end, uploads no data and needs no registration, just open a browser. Runs front-end, uploads no data, no registration needed, open…",
"About the Image Processing Tools",
"The image processing tool collection brings together 14 free online tools covering the common calculation, conversion and lookup needs in image processing scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser, uploads no data to a server, and keeps your privacy secure.",
"The image processing tools collected on this page include (some representative tools):",
"These tools help you finish common image processing tasks quickly, with no need to memorize complex formulas or do manual conversions, just enter and get the result.",
"Do the Image Processing Tools need a download or registration?",
"No. All image processing tools on this page are pure front-end online tools: open the page and use them directly, with no software to install, no account to register, and no data uploaded.",
"Are the Image Processing Tools results accurate? Is my data safe?",
"The tools compute locally in your browser from public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device, data is never uploaded to a server, and your privacy is protected.",
    ]))

    write('image-converter', build('image-converter', [
"🖼️ Image Format Converter",
"Convert images to different formats (JPEG/PNG/WebP) and output several formats at once",
"Image Converter",
"/ Image Converter",
"Format conversion is chosen by codec characteristics: JPEG is lossy compression (quality 60% to 90% balances size and quality, no transparency support), PNG is lossless (supports alpha transparency, good for icons and screenshots), WebP offers both lossless and lossy with transparency support (25% to 35% smaller than JPEG at the same quality), and GIF is limited to 256 colours (good for simple animations); the compressed size is roughly pixel count × bytes per pixel × compression ratio; for web optimisation prefer WebP and keep JPEG as a fallback.",
"📁 Click or drag an image here",
"Conversion results (click to download)",
"Format notes",
"First choice for photos",
"Small (lossy)",
"Icons, screenshots",
"Large (lossless)",
"Modern format",
"Larger",
"Original bitmap",
"📚 In-depth analysis: image format conversion (PNG/JPEG/WebP)",
"A transparent background requires converting JPG to PNG or WebP.",
"To reduce size convert PNG to WebP, which is the first choice where compatibility allows.",
"A 1.2MB PNG logo converted to WebP drops to about 180KB, the alpha channel is preserved and the page loads faster.",
"A JPG with a white background stays white when converted to PNG (JPG has no transparency); for true transparency you must first cut out the subject in a cropping or background removal tool.",
"Does converting formats lose transparency?",
"JPG itself has no transparency, so transparent areas in the resulting PNG are white or the original background colour; the alpha channel is only preserved when the source already has one (PNG/WebP/GIF) and you convert within that family.",
"How good is WebP compatibility?",
"Modern browsers and WeChat both support it; some older systems and design software do not, so fall back to PNG when needed.",
"About the Image Converter",
"The image converter is an online tool in the field of image processing. An image processing tool computing purely in the front end, so images never leave the device.",
    ]))

    write('image-filter', build('image-filter', [
"🖼️ Image Filter Tool",
"Apply filter effects using CSS Filter and Canvas",
"Image Filters",
"/ Image Filters",
"📁 Click or drag an image here",
"Preset filters",
"Custom adjustments",
"Hue rotation",
"Grayscale",
"Sepia",
"Invert",
"⬇ Download filtered image",
"📚 In-depth analysis: image filter adjustments (brightness / contrast / saturation / hue / blur / grayscale)",
"A photo is too dark and you want to brighten it, or you want a vintage grayscale look.",
"Unify the tones of a batch of images so the set looks more coherent.",
"Brighten and boost saturation",
"Brightness 100→130, saturation 100→120 turns a washed-out original clearer, with all other parameters left at 100.",
"Vintage grayscale",
"Tick grayscale with brightness 100 and contrast 110 for a black-and-white film feel; then layer sepia 0→40 for a warm nostalgic tone.",
"Why is the baseline 100?",
"100 means the original value with no adjustment; above 100 enhances (brightness/contrast/saturation) and below 100 reduces it; hue 0 is the original hue.",
"Do blur and grayscale affect each other?",
"They are layered independently. Decide the blur level first and then grayscale, since the order changes the look slightly; you can compare in real time.",
"About the Image Filters",
"The image filters tool is an online tool in the field of image processing. An image processing tool computing purely in the front end, so images never leave the device.",
    ]))

    write('id-photo-crop', build('id-photo-crop', [
"🪪 ID Photo Cropper",
"Upload a photo and export it as PNG by specification, with background colour replacement and size preview.",
"/ ID Photo Cropper",
"Upload photo",
"Output specification",
"One inch (258×335)",
"Two inches (413×531)",
"Passport (354×472)",
"Small avatar (300×300)",
"Current parameters",
"📚 In-depth analysis: one-click ID photo cropping (one inch / two inches / passport sizes)",
"Resumes, visas and exam sign-ups need compliant ID photo sizes, and cropping by hand often misses the mark.",
"You want a different background colour (red/blue/white) without a retake, so replace the background colour with a tool.",
"One inch photo 258×335",
"Pick the one inch preset, which locks the canvas to 258×335px (25×35mm at 300DPI); export with a white background as id-photo.png, about 35KB.",
"Passport photo 354×472",
"Pick the passport preset at 354×472px (33×48mm at 300DPI) and export with a blue background; the file is about 48KB.",
"How do you convert dimensions at 300DPI?",
"Pixels = mm ÷ 25.4 × 300. A 25 mm width = 25÷25.4×300 ≈ 295px; the nominal 258 for one inch is the common value after actual cropping with margins.",
"Are the two-inch and passport sizes the same?",
"No. Two inches is 413×531 (35×49mm) while the passport is 354×472 (33×48mm); check the requirements before signing up and pick the matching preset.",
    ]))

    write('generator-15', build('generator-15', [
"🖼️ Rounded Corner Image (generate PNG with rounded corners)",
"Generate a PNG with rounded corners",
"📚 In-depth analysis: rounded corner image generation (PNG export with rounded corners)",
"Making card and avatar thumbnails needs a consistent rounded look, avoiding square corners that feel harsh.",
"E-commerce main images or app icons want softer corners for a friendlier visual feel.",
"Export an avatar with 50% corner radius",
"Upload a 400×400 square image, set the corner ratio to 50% (radius = 400×50% = 200px, a perfect circle), and export a transparent PNG of about 90KB.",
"Card corner radius 12px",
"A cover of 800×450 with a 12px corner radius (a small radius that does not crop the content) exports as an 800×450 PNG with transparent corners and everything else opaque.",
"How is the corner radius computed?",
"radius = short edge × ratio%. A ratio of 50% gives a perfect circle on a square; fixed values like 12px are small radii that do not cut into the subject.",
"Why export PNG instead of JPG?",
"The area outside the corner radius is transparent and JPG does not support transparency so it would fill white; transparency requires PNG or WebP.",
"About the Rounded Corner Image (generate PNG with rounded corners)",
"Rounded corner image (generate PNG with rounded corners). An image processing tool computing purely in the front end, so images never leave the device.",
"How to Use the Rounded Corner Image Tool",
"Number of images to generate",
"What does the rounded corner image tool do?",
"A rounded corner image generator. Upload an image in the front end and generate a PNG with the specified corner radius (batch capable, right-click to save); images never leave the device, for quick rounded avatars and cards.",
"How do I use the rounded corner image tool?",
"Which scenarios suit the rounded corner image tool?",
    ]))

    write('nine-grid-cutter', build('nine-grid-cutter', [
"🖼️ Nine-Grid Cutter",
"After uploading an image it is cut into 3×3 automatically, and each piece can be downloaded separately.",
"/ Nine-Grid Cutter",
"The nine-grid cutter divides a square image evenly into 3 × 3 for 9 blocks: single block size = original side ÷ 3 (rounded to integer); the crop origin of block (row, column) is x = (column − 1) × block width, y = (row − 1) × block height, with both dimensions equal to the block size; the original should be cropped or scaled to a square first (take the smaller of width and height) to avoid stretch distortion; it outputs 9 equal-sized images for nine-grid posting on social platforms.",
"Generate slices",
"Download all",
"📚 In-depth analysis: nine-grid cutting (3×3 moments grid)",
"A long image posted to moments gets compressed, so cut it into a nine-grid to reassemble the large image.",
"Make a nine-cell poster set with each cell saved separately.",
"Cut 900×900 into 3×3",
"A square image of 900×900 divided evenly into 3×3 gives each cell 300×300 and exports 9 PNGs numbered 1–9.",
"Cut 1200×1200 into nine cells",
"Each cell of a 1200×1200 image is 400×400, and the nine reassemble seamlessly into the original; a non-square image is cropped to a square by the shorter edge first.",
"How do you cut a non-square image?",
"The tool usually crops to a square by the shorter edge and then divides into 3×3, ensuring the nine cells are equal and reassemble without distortion.",
"What is the reassembly order?",
"Publish 1–9 in row-major order, left to right then top to bottom, and the moments nine-grid reproduces the original image.",
    ]))

    write('wechat-cover-maker', build('wechat-cover-maker', [
"✨ WeChat Official Account Cover Generator",
"Generate a 900×383 cover image purely front-end: title + subtitle + background gradient + download.",
"/ WeChat Official Account Cover Generator",
"Background colour 1",
"Background colour 2",
"📚 In-depth analysis: WeChat Official Account cover generation (main image / secondary article)",
"An article needs a compliant cover size, and making one by hand is time-consuming.",
"Unify the title style and brand colour to improve recognition.",
"Main image 900×383",
"Pick the main image spec 900×383 with the title \"Tool Name Example\" plus a subtitle, main colour #ff6b35, secondary colour #7c3aed and white text #ffffff, then export.",
"Secondary article 200×200",
"The secondary article is square at 200×200 with only a short title and the same main and secondary colours, so the brand tone reads even in a small image.",
"How different are the main and secondary image sizes?",
"The main image is 900×383 (about 2.35:1) and the secondary article is square at 200×200; the WeChat backend has different ratio requirements for each, so do not mix them up.",
"How do you pick text colour that stays legible?",
"White text #ffffff on a dark background is the safest; if the main colour is very light, switch the text to a darker colour and guarantee contrast so it stays clear at small sizes.",
    ]))


if __name__ == '__main__':
    main()