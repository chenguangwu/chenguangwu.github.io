#!/usr/bin/env python3
"""Check related-tool i18n mapping completeness between industry-*.json and slug-en.json."""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IND_DIR = os.path.join(ROOT, 'json')
SLUG_PATH = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')


def collect_tool_keys():
    """Collect normalized keys from industry-*.json: industry/slug."""
    tool_keys = set()
    bad_urls = []

    for name in sorted(os.listdir(IND_DIR)):
        if not (name.startswith('industry-') and name.endswith('.json')):
            continue
        path = os.path.join(IND_DIR, name)
        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            url = item.get('url')
            if not isinstance(url, str):
                continue
            if not url.startswith('tools/'):
                bad_urls.append(url)
                continue
            if not url.endswith('.html') or url.count('/') != 2:
                bad_urls.append(url)
                continue
            m = re.match(r'^tools/[^/]+/[^/]+\.html$', url)
            if not m:
                bad_urls.append(url)
                continue
            tool_keys.add(url[6:-5])

    return tool_keys, bad_urls


def main():
    parser = argparse.ArgumentParser(description='Check related-tools slug mapping')
    parser.add_argument('--report-json', help='Optional JSON report output path')
    args = parser.parse_args()

    tool_keys, bad_urls = collect_tool_keys()

    if not os.path.exists(SLUG_PATH):
        print('❌ missing', SLUG_PATH)
        return 1

    with open(SLUG_PATH, encoding='utf-8') as f:
        slug = json.load(f)

    slug_keys = set(slug.keys())
    missing = sorted(tool_keys - slug_keys)
    extra = sorted(slug_keys - tool_keys)

    print('总 tool url 数:', len(tool_keys))
    print('slug-en 条目数:', len(slug_keys))
    print('映射缺失:', len(missing))
    print('冗余 key:', len(extra))
    print('非标准 URL:', len(bad_urls))

    if bad_urls:
        print('⚠️  非标准路径样例:', ', '.join(bad_urls[:20]))

    if missing:
        print('❌ 首个缺失示例:', ', '.join(missing[:20]))
    if extra:
        print('⚠️ 首个冗余示例:', ', '.join(extra[:20]))

    if args.report_json:
        report = {
            'tools': len(tool_keys),
            'slug_keys': len(slug_keys),
            'missing': missing,
            'extra': extra,
            'bad_urls': bad_urls,
        }
        with open(args.report_json, 'w', encoding='utf-8') as w:
            json.dump(report, w, ensure_ascii=False, indent=2)

    if missing or bad_urls:
        return 1

    print('✅ 映射覆盖 100% 且路径规范')
    return 0


if __name__ == '__main__':
    sys.exit(main())
