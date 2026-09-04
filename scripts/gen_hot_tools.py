#!/usr/bin/env python3
"""Generate the editorial homepage hot-tools list from the current tools index.

This list intentionally complements traffic data: a small analytics sample can
overrepresent specialist, regulated, or one-off tools. Keep this ordered list
to broadly useful, self-contained browser tools and let the build resolve the
latest names, descriptions, icons, and i18n metadata from json/tools.json.
"""
import json
import os
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_PATH = os.path.join(ROOT, 'json', 'tools.json')
OUTPUT_PATH = os.path.join(ROOT, 'json', 'hot-tools.json')


# Ordered by expected general usefulness, not a claim about real-time traffic.
# Keep the list at 60: developer/data, visual/document, and everyday work all
# need representation on the homepage.
HOT_TOOL_URLS = (
    # Developer, data, and text (36)
    'tools/it/json-formatter.html',
    'tools/it/qrcode.html',
    'tools/it/password-generator.html',
    'tools/it/regex.html',
    'tools/life/timestamp.html',
    'tools/it/base64.html',
    'tools/it/url-encode.html',
    'tools/it/uuid-generator.html',
    'tools/it/jwt-debugger.html',
    'tools/it/hash-multi.html',
    'tools/it/json-diff.html',
    'tools/it/json-to-csv.html',
    'tools/it/csv-to-json.html',
    'tools/it/json-to-yaml.html',
    'tools/it/yaml-to-json.html',
    'tools/it/xml-formatter.html',
    'tools/it/xml-to-json.html',
    'tools/it/yaml-validator.html',
    'tools/it/sql-formatter.html',
    'tools/it/markdown-to-html.html',
    'tools/it/html-entity-encoder.html',
    'tools/it/css-minify.html',
    'tools/it/css-formatter.html',
    'tools/it/js-minify.html',
    'tools/it/slugify.html',
    'tools/it/case-converter.html',
    'tools/it/text-diff.html',
    'tools/it/unicode-lookup.html',
    'tools/it/csv-validator.html',
    'tools/it/mime-type-lookup.html',
    'tools/it/user-agent-parser.html',
    'tools/it/ip-calculator.html',
    'tools/it/cron.html',
    'tools/it/wifi-qr.html',
    'tools/it/lorem.html',
    'tools/it/base64-file.html',
    # Design, images, documents (11)
    'tools/design/color-picker.html',
    'tools/design/image-compress.html',
    'tools/design/image-format-converter.html',
    'tools/design/image-cropper.html',
    'tools/design/favicon-generator.html',
    'tools/design/shadow-generator.html',
    'tools/it/color-converter.html',
    'tools/biz/barcode-generator.html',
    'tools/office/pdf-merge.html',
    'tools/office/pdf-split.html',
    'tools/office/pdf-rotate.html',
    # Everyday, study, and work (13)
    'tools/life/unit-converter.html',
    'tools/life/percentage-calculator.html',
    'tools/life/age-calculator.html',
    'tools/life/date-diff.html',
    'tools/edu/timezone-converter.html',
    'tools/edu/gpa-calculator.html',
    'tools/marketing/utm-builder.html',
    'tools/finance/roi-calculator.html',
    'tools/finance/mortgage-calculator.html',
    'tools/finance/compound-interest.html',
    'tools/finance/invoice-generator.html',
    'tools/it/random-string.html',
    'tools/it/device-info.html',
)


def hot_card(tool):
    """Keep the public payload compact and stable for js/app.js."""
    name = tool.get('name', '')
    desc = tool.get('d') or tool.get('desc') or name
    return {
        'n': name,
        'en': tool.get('en') or name,
        'd': desc,
        'ed': tool.get('ed') or desc,
        'i': tool.get('industry', ''),
        'c': tool.get('cat', ''),
        'u': tool.get('url', ''),
        'ic': tool.get('icon', '🔧'),
        'b': tool.get('bg', '#f5f5f5'),
    }


def main():
    try:
        with open(TOOLS_PATH, encoding='utf-8') as source:
            tools = json.load(source)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit('Cannot read %s: %s' % (TOOLS_PATH, exc))

    by_url = {tool.get('url'): tool for tool in tools if isinstance(tool, dict)}
    missing = [url for url in HOT_TOOL_URLS if url not in by_url]
    duplicate_count = len(HOT_TOOL_URLS) - len(set(HOT_TOOL_URLS))
    if missing or duplicate_count or len(HOT_TOOL_URLS) != 60:
        if missing:
            print('Missing selected hot tools:', ', '.join(missing), file=sys.stderr)
        if duplicate_count:
            print('Duplicate selected hot tools: %d' % duplicate_count, file=sys.stderr)
        if len(HOT_TOOL_URLS) != 60:
            print('Expected 60 selected tools, got %d' % len(HOT_TOOL_URLS), file=sys.stderr)
        raise SystemExit(1)

    cards = [hot_card(by_url[url]) for url in HOT_TOOL_URLS]
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as output:
        json.dump(cards, output, ensure_ascii=False, indent=2)
        output.write('\n')
    print('Generated hot-tools.json (%d editorial cards)' % len(cards))


if __name__ == '__main__':
    main()
