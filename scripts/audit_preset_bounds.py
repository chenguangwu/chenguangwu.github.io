#!/usr/bin/env python3
"""预设值边界审计：只查 number/range 输入框的 min/max 越界。

为什么只查 min/max：
- step 不整除在小数/科学计数法预设中很常见，浏览器又不会阻止程序化赋值，属噪声；
- select 的 option 值可能含转义引号，静态解析容易误报。

用法：python3 scripts/audit_preset_bounds.py [--check]
退出码：--check 时有越界项返回 1，否则 0。
"""
import argparse
import glob
import re
import sys

PAIR = re.compile(r"([A-Za-z0-9_-]+|'[^']+')\s*:\s*('([^']*)'|\"([^\"]*)\"|[^,}]+)")


def parse_values(body):
    out = {}
    for m in PAIR.finditer(body):
        key = m.group(1).strip("'\"")
        value = m.group(3) if m.group(3) is not None else (
            m.group(4) if m.group(4) is not None else m.group(2)
        )
        out[key] = value.strip()
    return out


def attrs(tag):
    return {m.group(1).lower(): m.group(2) for m in re.finditer(r'([A-Za-z:-]+)="([^"]*)"', tag)}


def number_inputs(raw):
    found = {}
    for m in re.finditer(r'<input\b[^>]*>', raw, re.I):
        a = attrs(m.group(0))
        ident = a.get('id')
        if not ident:
            continue
        if (a.get('type') or 'text').lower() not in ('number', 'range'):
            continue
        found[ident] = a
    return found


def audit(root='tools'):
    issues = []
    for path in glob.glob(root + '/*/*.html'):
        raw = open(path, encoding='utf-8').read()
        if 'values:{' not in raw:
            continue
        inputs = number_inputs(raw)
        if not inputs:
            continue
        for block in re.finditer(r'values:\{(.*?)\}', raw):
            values = parse_values(block.group(1))
            for key, value in values.items():
                if key not in inputs or value == '':
                    continue
                try:
                    number = float(value)
                except ValueError:
                    continue
                a = inputs[key]
                for bound, compare in (('min', lambda x, b: x < b - 1e-12),
                                       ('max', lambda x, b: x > b + 1e-12)):
                    raw_bound = a.get(bound)
                    if raw_bound in (None, ''):
                        continue
                    try:
                        limit = float(raw_bound)
                    except ValueError:
                        continue
                    if compare(number, limit):
                        issues.append((path, key, value, bound, raw_bound))
    return issues


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    issues = audit()
    print('===== 预设值边界审计（仅 min/max）=====')
    print('越界项: %d' % len(issues))
    for path, key, value, bound, limit in issues[:80]:
        label = 'min' if bound == 'min' else 'max'
        print('%s  %s=%s  %s %s' % (path, key, value, label, limit))
    if args.check and issues:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
