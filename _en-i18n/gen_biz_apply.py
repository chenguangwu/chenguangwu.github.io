# -*- coding: utf-8 -*-
"""biz 行业 per-tool 字典写入器（共享）。

apply_tool(slug, name, en, mp, display=None, en_display=None, ind='biz')
- 自动补「工具名嵌入」5 条模板句：{name} / / {name} / 📖 查看「{name}使用指南」 /
  📚 深度解析：{name} / 关于「{display}」（display 默认 = name）。
- 写入前做零 CJK + 零中文标点校验；任一违规即打印并 exit(1)，不落盘。
- 值内不改动源节点首尾空白：运行时保留原节点空白，故拼接片段（含内链）的
  译文需自行携带首/尾空格（见坑「保留节点原有首尾空白」）。
"""
import json, io, os, re, sys

IND = 'biz'
CJK = re.compile(r'[\u4e00-\u9fff]')
PUNCT = re.compile(r'[，。、；：！？（）「」]')


def _gen_templates(name, en, display, en_display):
    d = display or name
    ed = en_display or en
    return {
        name: en,
        '/ ' + name: '/ ' + en,
        '📖 查看「' + name + '使用指南」': '📖 View the "' + en + ' Guide"',
        '📚 深度解析：' + name: '📚 In-Depth: ' + en,
        '关于「' + d + '」': 'About "' + ed + '"',
    }


def apply_tool(slug, name, en, mp, display=None, en_display=None, ind=IND, auto=True, dry=False):
    path = 'i18n/tools/en/%s/%s.json' % (ind, slug)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    full = dict(_gen_templates(name, en, display, en_display)) if auto else {}
    full.update(mp)
    cur = {}
    if os.path.exists(path):
        cur = json.load(io.open(path, encoding='utf-8')).get('map', {})
    bad = []
    for k, v in full.items():
        if not isinstance(v, str):
            bad.append((k, v, 'NOTSTR')); continue
        if CJK.search(v):
            bad.append((k, v, 'CJK'))
        if PUNCT.search(v):
            bad.append((k, v, 'PUNCT'))
    if bad:
        print('!! %s 违规 %d 条：' % (slug, len(bad)))
        for k, v, t in bad[:40]:
            print('   [%s] %r -> %r' % (t, k, v))
        if not dry:
            sys.exit(1)
        return 0
    if dry:
        print('OK(dry) %s: %d 键' % (slug, len(full)))
        return len(full)
    cur.update(full)
    out = {'slug': slug, 'industry': ind, 'name': name, 'map': cur}
    with io.open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE %s: +%d (total %d)' % (slug, len(full), len(cur)))
    return len(full)


def apply_common(mp):
    path = 'i18n/tools/en/_common.json'
    d = json.load(io.open(path, encoding='utf-8'))
    m = d.get('map', d)
    bad = [(k, v) for k, v in mp.items() if CJK.search(v) or PUNCT.search(v)]
    if bad:
        print('!! _common 违规：', bad[:10]); sys.exit(1)
    m.update(mp)
    with io.open(path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    print('WROTE _common: +%d' % len(mp))
