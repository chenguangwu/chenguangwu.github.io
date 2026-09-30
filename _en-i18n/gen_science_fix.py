# -*- coding: utf-8 -*-
"""science 收尾补丁：修正 star-magnitude 的源文键 + 补 text-extract-phones textarea 示例"""
import json, io, re, os

CJK = re.compile(r'[\u4e00-\u9fff]')


def load(p):
    return json.load(io.open(p, encoding='utf-8'))


def save(p, d):
    with io.open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write('\n')


def main():
    # 1) star-magnitude-compare：删错键（EN 残留形态），加源文键
    p1 = 'i18n/tools/en/science/star-magnitude-compare.json'
    d1 = load(p1)
    mp = d1['map']
    if 'Distance (光年)' in mp:
        del mp['Distance (光年)']
        print('removed wrong key Distance (光年)')
    mp['距离(光年)'] = 'Distance (light-years)'
    save(p1, d1)
    print('star-magnitude map size', len(mp))

    # 2) text-extract-phones：textarea 默认示例（三行）
    p2 = 'i18n/tools/en/science/text-extract-phones.json'
    d2 = load(p2)
    key = ('联系我们：13812345678 或 010-87654321。\n'
           '客服电话：400-800-1234，手机：186-0000-1111。\n'
           '国际号码：+86 139 0000 9999 或 +1 (650) 253-0000。')
    val = ('Contact us: 13812345678 or 010-87654321.\n'
           'Customer service: 400-800-1234, mobile: 186-0000-1111.\n'
           'International: +86 139 0000 9999 or +1 (650) 253-0000.')
    d2['map'][key] = val
    save(p2, d2)
    print('text-extract-phones map size', len(d2['map']))

    for p in (p1, p2):
        d = load(p)
        bad = [(k, v) for k, v in d['map'].items() if isinstance(v, str) and CJK.search(v)]
        print(os.path.basename(p), 'CJK values:', len(bad), bad[:3])


if __name__ == '__main__':
    main()
