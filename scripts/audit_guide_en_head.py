#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""指南页英文头部回归锁。

检查三类问题：
1. 加载 js/guide-en-pack.js 的指南页，data-i18n-head 键必须全部存在于 GUIDE_EN_PACK；
2. 每页必须有 i18n/guides/<slug>.json 正文词典；
3. title 必须带 data-i18n-head，description 必须带 data-i18n-head + data-attr=content；
4. 指南页脚本必须走站内根相对路径，禁止写死线上域名（否则本地词典/脚本改动无法验证）；
5. js/i18n.js 必须消费 GUIDE_EN_PACK，否则 data-i18n 会在 init 时把正文重置回中文。

退出码：0 = 通过，1 = 有缺口。
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_pack():
    p = os.path.join(ROOT, 'js', 'guide-en-pack.js')
    raw = open(p, encoding='utf-8').read()
    raw = raw[raw.index('{'):raw.rstrip().rindex('}') + 1]
    return json.loads(raw)


def main():
    pack = load_pack()
    pages = []
    missing_keys = []
    missing_dict = []
    bad_title = []
    bad_desc = []
    bad_asset = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'guides', '*.html'))):
        s = open(f, encoding='utf-8').read()
        if 'guide-en-pack.js' not in s:
            continue
        rel = os.path.relpath(f, ROOT)
        slug = os.path.basename(f)[:-5]
        pages.append(rel)
        for k in re.findall(r'data-i18n-head="([^"]+)"', s):
            if k not in pack:
                missing_keys.append((rel, k))
        if not os.path.isfile(os.path.join(ROOT, 'i18n', 'guides', slug + '.json')):
            missing_dict.append(rel)
        if not re.search(r'<title[^>]+data-i18n-head="', s):
            bad_title.append(rel)
        if not re.search(r'<meta[^>]+name="description"[^>]+data-i18n-head="[^"]+"[^>]+data-attr="content"', s) and \
           not re.search(r'<meta[^>]+name="description"[^>]+data-attr="content"[^>]+data-i18n-head="', s):
            bad_desc.append(rel)
        if re.search(r'<script[^>]+src="https://chenguangwu\.github\.io/js/', s):
            bad_asset.append(rel)

    print('guide pages with EN pack: %d' % len(pages))
    print('missing pack keys: %d' % len(missing_keys))
    print('missing guide dictionary: %d' % len(missing_dict))
    print('title without data-i18n-head: %d' % len(bad_title))
    print('description without head key: %d' % len(bad_desc))
    print('pages hardcoding production JS URL: %d' % len(bad_asset))
    for label, arr in (('MISSING-KEY', missing_keys), ('MISSING-DICT', missing_dict),
                       ('BAD-TITLE', bad_title), ('BAD-DESC', bad_desc), ('BAD-ASSET', bad_asset)):
        for item in arr[:10]:
            print('  %s %s' % (label, item))
    i18n_js = open(os.path.join(ROOT, 'js', 'i18n.js'), encoding='utf-8').read()
    if 'GUIDE_EN_PACK' not in i18n_js:
        print('FAIL: js/i18n.js does not consume GUIDE_EN_PACK')
        return 1
    if missing_keys or missing_dict or bad_title or bad_desc or bad_asset:
        print('FAIL: guide EN head audit')
        return 1
    print('PASS: guide EN head audit')
    return 0


if __name__ == '__main__':
    sys.exit(main())
