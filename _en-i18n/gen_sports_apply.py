# -*- coding: utf-8 -*-
"""sports 行业 per-tool 字典写入器（共享）。
用法：from gen_sports_apply import apply_tool, apply_common
apply_tool(slug, zh_name, en_name, {zh: en, ...})
- 自动补 4 条「工具名嵌入」模板句（是做什么的/如何使用/适合哪些场景/关于「」）。
- 写入前做零 CJK + 零中文标点校验；任一违规即打印并 exit(1)，不落盘。
"""
import json, io, os, re, sys

IND = 'sports'
CJK = re.compile(r'[\u4e00-\u9fff]')
PUNCT = re.compile(r'[，。、；：！？（）「」]')


def _gen_templates(zh_name, en):
    return {
        zh_name + '是做什么的？': 'What does %s do?' % en,
        '如何使用' + zh_name + '？': 'How do I use %s?' % en,
        zh_name + '适合哪些场景？': 'What scenarios is %s best for?' % en,
        '关于「' + zh_name + '」': 'About "%s"' % en,
    }


def apply_tool(slug, name, en, mp, auto=True, dry=False):
    path = 'i18n/tools/en/%s/%s.json' % (IND, slug)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    full = dict(_gen_templates(name, en)) if auto else {}
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
    out = {'slug': slug, 'industry': IND, 'name': name, 'map': cur}
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
        f.write('\n')
    print('WROTE _common: +%d' % len(mp))
