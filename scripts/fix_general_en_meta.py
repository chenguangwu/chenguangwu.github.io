#!/usr/bin/env python3
"""general 分类：英文 meta(desc-en) 与 i18n 覆盖(ed) 套话真实化（首批 50 个）。

复用 fix_general_en_p.EN_MAP 的真实英文，保证三处英文(可见 <p> / desc-en meta / ed 覆盖)一致。

- desc-en meta：HTML <head> 里的 <meta name="desc-en" content="...">，截断到 <=155 字符做摘要级 meta description
- ed 字段：i18n/tools/_en_override.json 里 general/<slug> 的 "ed"，改为与 p 一致的真实英文（不截断）

用法：
    python3 scripts/fix_general_en_meta.py --dry-run
    python3 scripts/fix_general_en_meta.py --apply
安全约束：
  - desc-en 只替换同名 meta 的 content，正则保留标签；ed 只改 JSON 对应键的值。
  - 单文件若 desc-en 多处匹配则跳过报告。
后续批次往 EN_MAP(源脚本)追加 slug 后，本脚本自动覆盖新条目。
"""
import os
import re
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fix_general_en_p import EN_MAP  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OVERRIDE = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
META_PAT = re.compile(r'(<meta name="desc-en" content=")([^"]*)(">)')
META_MAX = 155


def trunc(s, n=META_MAX):
    s = s.strip()
    if len(s) <= n:
        return s
    cut = s[:n]
    sp = cut.rfind(' ')
    if sp > 40:
        cut = cut[:sp]
    return cut


def main():
    do_apply = '--apply' in sys.argv
    if not do_apply and '--dry-run' not in sys.argv:
        print('用法: python3 scripts/fix_general_en_meta.py --dry-run | --apply')
        return 1

    override = json.load(open(OVERRIDE, encoding='utf-8'))
    new_override = dict(override)

    changed_meta, changed_ed, skipped = 0, 0, []
    for slug, en in EN_MAP.items():
        path = os.path.join(ROOT, 'tools', 'general', slug + '.html')
        if not os.path.exists(path):
            skipped.append((slug, 'file-missing'))
            continue
        src = open(path, encoding='utf-8').read()
        hits = list(META_PAT.finditer(src))
        if not hits:
            skipped.append((slug, 'no-desc-en-meta'))
        elif len(hits) > 1:
            skipped.append((slug, 'multi-meta:%d' % len(hits)))
        else:
            new_meta = trunc(en)
            new_src = META_PAT.sub(lambda m: m.group(1) + new_meta + m.group(3), src, count=1)
            if new_src != src:
                if do_apply:
                    open(path, 'w', encoding='utf-8').write(new_src)
                changed_meta += 1

        # ed 字段
        key = 'general/' + slug
        if key in override:
            entry = dict(override[key])
            old_ed = entry.get('ed', '')
            if old_ed != en:
                entry['ed'] = en
                new_override[key] = entry
                changed_ed += 1
        else:
            skipped.append((slug, 'no-override-key'))

    if do_apply:
        json.dump(new_override, open(OVERRIDE, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)

    tag = 'APPLY' if do_apply else 'DRY-RUN'
    print('%s: desc-en meta 改 %d, ed 改 %d, 跳过 %d' % (tag, changed_meta, changed_ed, len(skipped)))
    for slug, reason in skipped[:30]:
        print('  skip  %-32s %s' % (slug, reason))
    return 0


if __name__ == '__main__':
    sys.exit(main())
