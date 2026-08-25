#!/usr/bin/env python3
"""
_migrate_it_dict.py — 一次性迁移：把 it.json 中遗留的「扁平顶层语种字典」
（Batch 3 旧式 {"en-US": {"json-formatter.title": ...}}）转换为 tool-i18n.js
可消费的嵌套 schema：{"<slug>": {"zh-CN": {...}, "en-US": {...}, ...}}。

仅处理 i18n/tools/it.json（它是唯一带旧式扁平结构的文件）。其余 276 个
行业文件由 scripts/gen_i18n_dict.py 直接产出正确嵌套结构，无需迁移。
"""
import json

P = 'i18n/tools/it.json'
LANGS = ['en-US']


def flat_to_nested(flat):
    """flat: {"json-formatter.title": ..., "json-formatter.note.0": ...}
    -> nested: {"json-formatter": {"title": ..., "note": [...]}}"""
    nested = {}
    for k, v in flat.items():
        parts = k.split('.')
        slug, rest = parts[0], parts[1:]
        if not rest:
            continue
        if rest[0] == 'note' and len(rest) >= 2:
            try:
                idx = int(rest[1])
            except ValueError:
                idx = None
            if idx is not None:
                arr = nested.setdefault(slug, {}).setdefault('note', [])
                while len(arr) <= idx:
                    arr.append(None)
                arr[idx] = v
                continue
        if rest[0] == 'title' and len(rest) >= 2 and rest[1] == 'h1':
            nested.setdefault(slug, {})['h1'] = v
            continue
        nested.setdefault(slug, {})[rest[0]] = v
    return nested


def main():
    d = json.load(open(P, 'r', encoding='utf-8'))
    # 1) 抽取遗留扁平顶层语种字典
    legacy = {}
    for lg in LANGS:
        if lg in d and isinstance(d[lg], dict):
            legacy[lg] = d.pop(lg)
    nested_legacy = {lg: flat_to_nested(flat) for lg, flat in legacy.items()}

    # 2) 重建：保留每个 slug 的 zh-CN，注入嵌套语种
    out = {}
    for slug, entry in d.items():
        new_entry = {}
        if isinstance(entry, dict):
            if 'zh-CN' in entry:
                new_entry['zh-CN'] = entry['zh-CN']
            # 丢弃误生成在 slug 顶层的 'note' 噪声
        out[slug] = new_entry
    # 把遗留语种落到对应 slug（含仅存在于遗留中的 slug）
    for lg, nst in nested_legacy.items():
        for slug, fields in nst.items():
            out.setdefault(slug, {})
            out[slug].setdefault(lg, fields)

    json.dump(out, open(P, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    open(P, 'a').write('\n')
    print('migrated it.json. slugs=%d' % len(out))
    for lg in legacy:
        n = sum(1 for s, e in out.items() if lg in e)
        print('  %s slugs with %s: %d' % (lg, lg, n))


if __name__ == '__main__':
    main()
