#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'data')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'data')
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
    out = {'slug': slug, 'industry': 'data', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('calc-1', build('calc-1', [
        "📊 CSV to JSON",
        "Convert CSV data into a JSON array locally in the browser, with customizable delimiter and header handling.",
        "CSV to JSON splits row by row: if the first row is the header it supplies the field names, and every following row is split by the delimiter (an English comma by default, customizable) and paired column by column with the header to produce an array of \"field: value\" objects; a field containing the delimiter or a newline is wrapped in double quotes per RFC 4180, a double quote inside quotes is escaped as two double quotes, and the key-value pairs are emitted in row order.",
        "First row is the header",
        "When the first row is the header, field names come from that row; otherwise the default keys field_0, field_1 and so on are used.",
        "Quoted fields are supported, and quotes may contain delimiters and newlines.",
        "Empty cells become empty strings, and rows left unfilled are skipped.",
        "📚 Deep Dive: CSV to JSON",
        "API debugging: quickly turn a CSV export from the backend into a",
        "array that you can paste straight into a request body or a frontend mock, without hand-writing the fields.",
        "Table migration: a CSV exported from Excel or a database often needs to become JSON to fit NoSQL storage or a multidimensional structure, and the conversion preserves the original rows and columns.",
        "Field alignment: specify the header mapping and delimiter during conversion to avoid parse and field misalignment caused by Chinese commas and half-width quotes.",
        "Orders",
        "CSV to JSON",
        "Paste a CSV with the three columns \"order number, amount, status\", pick comma as the delimiter and use the first row as the header; the tool outputs [{\"order number\":\"A1001\",\"amount\":\"99.00\",\"status\":\"paid\"}], ready for API validation or frontend table rendering.",
        "Which delimiters are supported?",
        "Commas, tabs, semicolons and a custom single character are supported; delimiters inside quoted fields are not mis-split and the field content is preserved as is.",
        "Will Chinese or special characters get garbled?",
        "The conversion runs locally and preserves UTF-8 characters as is; after exporting, save as UTF-8 to avoid encoding problems when reopening the file.",
        "Can the result be used as API data directly?",
        "It only converts the format and does not validate business rules; amounts, dates and other types are still kept as strings, so validate types and ranges as needed before integrating.",
    ]))
    write('calc-2', build('calc-2', [
        "🧹 JSON Formatter",
        "Validate, format and minify JSON data, with every operation done locally.",
        "JSON formatting outputs recursively along the syntax tree: the parser first runs lexical analysis (recognizing strings, numbers, true/false/null and brackets), then indents by level (2 spaces or a tab per level); minifying removes all structural whitespace and keeps only separators; when validation fails it reports the error position, and escape sequences inside strings must be paired and must not span lines.",
        "Format: validates the JSON automatically and shows it with 2-space indentation.",
        "Minify: strips extra whitespace to produce single-line JSON.",
        "If the JSON is invalid, the error position and reason are highlighted.",
        "📚 Deep Dive: JSON Formatter",
        "API debugging: expand a response body that was minified into one line to quickly locate nested fields and missing keys, which helps troubleshoot integration problems.",
        "Config review: syntax-check local config files to catch stray commas, mismatched quotes and other parse failures ahead of time.",
        "Size comparison: minify redundant whitespace and compare the before/after size to assess the room for transmission optimization and field redundancy.",
        "Format a minified response body",
        "Paste {\"a\":1,\"b\":{\"c\":[1,2]}} and pick 2-space indentation; the tool outputs a readable structure with line breaks per level, and if there is a trailing comma it points out the exact line so you can fix it in place.",
        "Can it validate whether JSON is legal?",
        "Yes, it runs a syntax check before formatting and gives the line number and reason for invalid positions, but it only checks syntax, not the business meaning of fields.",
        "Will big files lag?",
        "Parsing runs locally and large volumes are limited by browser memory; split the file or paste only key fragments to avoid processing very long text at once.",
        "Does minifying lose information?",
        "Minifying only removes whitespace and newlines, and keys and values stay unchanged; if the original text contains illegal structures such as a trailing comma, it is rejected first with a notice.",
    ]))
    write('generator-14', build('generator-14', [
        "🔳 Barcode / QR Code Data Generator (existing)",
        "Existing",
        "Barcode Code128 maps every character to 11 modules, and the check digit is generated by alternately summing the start character and the data characters with weights 1 and 2 and taking the result modulo 103; QR codes encode data per the QR Code standard (numeric, alphanumeric and byte modes), with error correction (L 7%, M 15%, Q 25%, H 30%), mask selection and finder pattern layout, and capacity grows with versions 1 to 40.",
        "📚 Deep Dive: Barcode / QR Code Data Generator (existing)",
        "Material labels: turn an article number or SKU into a barcode so that scanning works for stock-in and inventory counting after printing and sticking it on.",
        "Information entry: generate a",
        "for a URL or work order number, so scanning on site jumps straight there and cuts down on manual typing.",
        "Event redemption: encode a coupon code as a QR code that the redemption terminal scans to read, avoiding transcription errors.",
        "Generate a QR code for a URL",
        "Enter https://example.com/act and pick the QR code; the tool produces an image that a camera can recognize, and scanning it opens the event page. The content is only encoded locally and never uploaded.",
        "Which encodings are supported?",
        "Common one-dimensional barcode and QR formats are supported; the page's selectable list is authoritative, and all encoding and rendering happen locally.",
        "Is there a length limit on the content?",
        "QR code capacity is limited, and overly long text lowers density and recognition rate; for very long content, shorten it with a short link first.",
        "Are the generated codes safe?",
        "Only the input text is encoded locally, with no storage and no upload; do not encode sensitive credentials directly into publicly posted codes.",
        "About Barcode / QR Code Data Generator (existing)",
        "Barcode / QR code data generator (existing). Data analysis tools that help you process and visualize data quickly.",
    ]))
    write('generator-35', build('generator-35', [
        "📈 Histogram (Bins / Frequency) Generator",
        "Bins / Frequency",
        "Histogram binning: the bin count k is the square root of the sample size n, or the Sturges formula k = 1 + log₂n rounded to an integer; the bin width h = (max − min) ÷ k; each bin frequency = the number of values falling in the left-closed right-open interval; frequency density = frequency ÷ (sample size × bin width), with rectangle area representing the frequency distribution of each bin.",
        "📚 Deep Dive: Histogram (Bins / Frequency) Generator",
        "Score bands: group exam scores to see how many students fall in each band, which helps assess difficulty.",
        "Duration distribution: group task durations to see which range most of them fall into, making schedule estimates easier.",
        "Quality sampling: group dimensional measurements to check whether they cluster around the target value.",
        "Bin survey durations",
        "Enter 50 response times in seconds and set the bin width to 30 seconds; the tool outputs a frequency bar chart such as \"0-30: 12 / 30-60: 23 / 60-90: 15\", showing that most fall in the 30-60 second band.",
        "How should the bin width be set?",
        "You can type the bin width and starting point manually; too small a width makes it volatile, too large hides the structure, so try a few",
        "different values.",
        "Which bin does a boundary value belong to?",
        "It is handled by the left-closed right-open or inclusive rule the page uses; follow the page's description for the conclusion and align the convention before comparing.",
        "What sample size is suitable?",
        "With a very small sample the distribution is only weakly informative, so read it together with other statistics as exploratory reference only.",
        "About Histogram (Bins / Frequency) Generator",
        "Histogram (bins and frequency) generator. Data analysis tools that help you process and visualize data quickly.",
    ]))
    write('generator-report', build('generator-report', [
        "✨ Report (Auto-generate / Send) Template",
        "Auto-generate / send",
        "A report is assembled by structure: header (title + generation date + dimension fields) + detail rows (filled in field order) + summary row (Σ or mean of the numeric columns) + footer (prepared by, reviewed by, page number); total = Σ detail values, share = detail value ÷ total × 100%, and the layout is aligned by field width for easy export and printing.",
        "📚 Deep Dive: Report (Auto-generate / Send) Template",
        "Weekly report template: generate a table skeleton from fixed fields so the team can fill it in and keep the format consistent.",
        "Stocktake sheet: preset header, footer and total rows, print it on site and fill it in by hand or re-enter the data.",
        "Export structure: copy the page's table structure into Excel and continue with formulas and styling.",
        "Generate an inventory stocktake template",
        "Set the header to \"item / spec / book count / actual count / difference\" with a total row in the footer; the tool outputs a printable template, and after entering the actual counts on site the difference column fills in automatically.",
        "Can it compute the summary directly?",
        "The template presets the summary row structure; if you need live calculation, export to spreadsheet software and add formulas, since this tool only generates structure and stores no data.",
        "Can the styling be changed?",
        "Columns and headers can be adjusted with the page's options; the page is authoritative, and you can keep laying things out in the target software after generation.",
        "The structure is only generated locally with no upload, and closing the page leaves nothing behind, so it suits quickly producing internal report skeletons.",
        "About Report (Auto-generate / Send) Template",
        "Report (auto-generate and send) template. Data analysis tools that help you process and visualize data quickly.",
    ]))
    write('random-1', build('random-1', [
        "🎨 Random Color (HEX/RGB)",
        "Random colors are drawn per channel: HEX is a hash sign plus RRGGBB, with each channel a random integer from 0 to 255 rendered as two hex digits; RGB is written as rgb(r, g, b) with each channel from 0 to 255; HSL is converted from hue 0 to 360, saturation 0 to 100% and lightness 0 to 100%; perceived lightness can be approximated as 0.299R + 0.587G + 0.114B.",
        "📚 Deep Dive: Random Color (HEX/RGB)",
        "Placeholder palettes: fill a prototype with random color blocks to check the layout before settling on a primary color.",
        "Inspiration exploration: keep drawing colors to find harmonious neighbors, which helps a first design draft.",
        "Code color picking: copy the selected HEX/RGB straight into",
        "and save yourself from",
        "switching back and forth.",
        "Get a set of neighboring colors",
        "Click Random repeatedly to get values like #6C5CE7 and #74B9FF, lock the HEX you like and copy it into your styles in one click; you can switch to the RGB format to fit different frameworks.",
        "Can colors be locked?",
        "You can lock the current value and keep randomizing, which helps build a multi-color scheme; the page buttons are authoritative.",
        "How do HEX and RGB convert?",
        "The page can switch the output format; the two notations of one color are equivalent, so copy and use.",
        "Is any history kept?",
        "Everything is generated locally and instantly with no upload, and closing the page clears it, so it suits temporary color picking.",
        "About Random Color (HEX/RGB)",
        "Random color (HEX/RGB). Data analysis tools that help you process and visualize data quickly.",
    ]))


if __name__ == '__main__':
    main()
