#!/usr/bin/env python3
"""全站质量回归锁（2026-11-23，扫描 O3）。

只读静态检查，秒级完成，覆盖本轮批量修复的 3 类可机器判定缺陷：
  1. desc-en 退化：与 title-en 完全相同或短于 20 字（曾 3,570 页 / 2,581 页）；
  2. 通用占位 formula-desc「按输入参数进行专业计算并输出结果」（曾 197 页）；
  3. 临床评分页 applicationCategory 被误标 FinanceApplication（曾 17 页）。
另有 description <70 的计数作为趋势指标，不阻断（中文短描述仍有少量历史页）。

用法：python3 scripts/audit_site_quality.py --check
"""
import argparse
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDER = '按输入参数进行专业计算并输出结果'
MISCLASS_INDUSTRIES = {
    'cardiology', 'neurology', 'nephrology', 'urology',
    'psychiatry', 'hematology', 'rehabilitation',
}
META_RE = r'<meta name="{name}" content="([^"]*)"'
APP_RE = re.compile(r'"applicationCategory":"([^"]+)"')
DESC_RE = re.compile(META_RE.format(name='description'))
TITLE_EN_RE = re.compile(META_RE.format(name='title-en'))
DESC_EN_RE = re.compile(META_RE.format(name='desc-en'))
HAS_CJK = re.compile(r'[\u4e00-\u9fff]')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='有硬缺陷时返回 1')
    args = parser.parse_args()

    errors = []
    desc_short = []
    total = 0
    for path in sorted(glob.glob(os.path.join(ROOT, 'tools', '**', '*.html'), recursive=True)):
        if path.endswith('index.html'):
            continue
        rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
        try:
            src = open(path, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        total += 1
        if 'TOOLBOX-REDIRECT' in src:
            continue

        dm = DESC_EN_RE.search(src)
        tm = TITLE_EN_RE.search(src)
        if dm:
            desc_en = html.unescape(dm.group(1)).strip()
            title_en = html.unescape(tm.group(1)).strip() if tm else ''
            if desc_en and (desc_en == title_en or len(desc_en) < 20):
                errors.append(f'{rel}: desc-en 退化（{len(desc_en)} 字，标题是否相同={desc_en == title_en}）')

        if PLACEHOLDER in src:
            errors.append(f'{rel}: 通用占位 formula-desc 未替换')

        for m in APP_RE.finditer(src):
            if m.group(1) != 'FinanceApplication':
                continue
            industry = rel.split('/')[1]
            if industry in MISCLASS_INDUSTRIES:
                errors.append(f'{rel}: 临床页 applicationCategory 仍为 FinanceApplication')
                break

        zhm = DESC_RE.search(src)
        if zhm:
            d = html.unescape(zhm.group(1)).strip()
            if d and len(d) < 70:
                desc_short.append((len(d), rel))

    guide_short = 0
    guide_total = 0
    for path in sorted(glob.glob(os.path.join(ROOT, 'guides', '*.html'))):
        if path.endswith('index.html'):
            continue
        rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
        src = open(path, encoding='utf-8', errors='ignore').read()
        if 'TOOLBOX-REDIRECT' in src or 'name="robots" content="noindex' in src:
            continue
        guide_total += 1
        m = DESC_RE.search(src)
        if m and len(html.unescape(m.group(1)).strip()) < 70:
            guide_short += 1
            errors.append(f'{rel}: 指南 description <70 字')
    print(f'工具页: {total}  指南页: {guide_total}  硬缺陷: {len(errors)}  工具描述<70: {len(desc_short)}')

    if desc_short:
        print('description <70 最短 10 条：')
        for n, rel in sorted(desc_short)[:10]:
            print(f'  {n:>2} 字  {rel}')
    if errors:
        print('\n硬缺陷清单：')
        for e in errors[:40]:
            print('  ❌ ' + e)
        if len(errors) > 40:
            print(f'  … 其余 {len(errors) - 40} 条')
        if args.check:
            return 1
    else:
        print('✅ 站内质量回归锁通过：desc-en 无退化 / 无占位 formula-desc / 无临床分类错配')
    return 0


if __name__ == '__main__':
    sys.exit(main())
