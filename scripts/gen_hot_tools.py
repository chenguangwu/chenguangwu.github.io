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


# Ordered by the previously computed weighted ranking from four supplied AI
# lists (Sonnet 5 Extra, DeepSeek, Baidu, and Doubao). Missing/AI-service
# entries were removed or replaced with browser-only candidates before ranking.
HOT_TOOL_URLS = (
    'tools/it/json-formatter.html',
    'tools/it/base64-converter.html',
    'tools/it/regex.html',
    'tools/life/unit-converter.html',
    'tools/healthcare/bmi-calculator.html',
    'tools/it/url-encode.html',
    'tools/design/color-picker.html',
    'tools/it/cron.html',
    'tools/it/jwt-parser.html',
    'tools/finance/tax-calculator.html',
    'tools/it/uuid-generator.html',
    'tools/finance/compound-interest.html',
    'tools/it/qrcode.html',
    'tools/finance/mortgage-calculator.html',
    'tools/image/image-compress.html',
    'tools/it/md5.html',
    'tools/design/gradient.html',
    'tools/healthcare/bmr-calculator.html',
    'tools/it/sql-formatter.html',
    'tools/life/temperature-converter.html',
    'tools/design/favicon-generator.html',
    'tools/it/csv-to-json.html',
    'tools/it/aes-encryptor.html',
    'tools/it/yaml-formatter.html',
    'tools/finance/investment-roi.html',
    'tools/it/password-generator.html',
    'tools/life/percentage-calculator.html',
    'tools/it/timestamp-converter.html',
    'tools/it/js-formatter.html',
    'tools/it/markdown-editor.html',
    'tools/design/image-format-converter.html',
    'tools/it/json-to-csv.html',
    'tools/life/world-clock.html',
    'tools/life/date-diff.html',
    'tools/it/sha.html',
    'tools/image/image-converter.html',
    'tools/finance/currency-converter.html',
    'tools/finance/loan-amortization.html',
    'tools/life/countdown.html',
    'tools/it/css-minifier.html',
    'tools/healthcare/tdee-calculator.html',
    'tools/life/age-calculator.html',
    'tools/it/http-status.html',
    'tools/finance/word-counter.html',
    'tools/it/xml-formatter.html',
    'tools/finance/car-loan-calculator.html',
    'tools/health/pregnancy-due-date.html',
    'tools/life/length-converter.html',
    'tools/marketing/utm-builder.html',
    'tools/life/weight-converter.html',
    'tools/biz/simplified-traditional.html',
    'tools/it/text-diff.html',
    'tools/health/body-fat-calculator.html',
    'tools/image/image-watermark.html',
    'tools/edu/gpa-calculator.html',
    'tools/it/json-diff.html',
    'tools/image/image-crop.html',
    'tools/design/image-resizer.html',
    'tools/design/base64-to-image.html',
    'tools/it/code-runner.html',
    'tools/health/sleep-cycle-calculator.html',
    'tools/it/random.html',
    'tools/design/image-color-picker.html',
    'tools/finance/discount-calculator.html',
    'tools/life/daily-calorie-needs.html',
    'tools/life/workday-calculator.html',
    'tools/travel/world-timezone-converter.html',
    'tools/science/calculator.html',
    'tools/legal/court-fee.html',
    'tools/legal/labor-compensation-n1.html',
    'tools/marketing/marketing-keyword-density.html',
    'tools/it/markdown-table-generator.html',
    'tools/image/image-collage.html',
    'tools/office/pdf-merge.html',
    'tools/office/pdf-split.html',
    'tools/office/pdf-rotate.html',
    'tools/hotel/tip-calculator.html',
    'tools/office/excel-formula-reference.html',
    'tools/office/flowchart.html',
    'tools/travel/travel-budget-calculator.html',
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
    if missing or duplicate_count or len(HOT_TOOL_URLS) != 80:
        if missing:
            print('Missing selected hot tools:', ', '.join(missing), file=sys.stderr)
        if duplicate_count:
            print('Duplicate selected hot tools: %d' % duplicate_count, file=sys.stderr)
        if len(HOT_TOOL_URLS) != 80:
            print('Expected 80 selected tools, got %d' % len(HOT_TOOL_URLS), file=sys.stderr)
        raise SystemExit(1)

    cards = [hot_card(by_url[url]) for url in HOT_TOOL_URLS]
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as output:
        json.dump(cards, output, ensure_ascii=False, indent=2)
        output.write('\n')
    print('Generated hot-tools.json (%d editorial cards)' % len(cards))


if __name__ == '__main__':
    main()
