#!/usr/bin/env python3
"""清理 cardiology 6 页的 opt-guide/JSON-LD 套话(工作与生活中的相关计算与查询)。

这些页除 content_deepdive 系统外，还在 <section class="opt-guide"> 的适用场景 <p>
以及 JSON-LD FAQPage 的「适合哪些场景」answer 中硬编码了通用套话。
用 content_deepdive 已真实化的 scenarios 前两条提炼真实适用场景，两处同步替换。
"""
import json, re, sys

DEEP = 'i18n/tools/content_deepdive.json'
ROOT = 'tools/cardiology'

TARGETS = ['antiarrhythmic-class', 'cpet-analysis', 'grace-score',
           'myocardial-bridge', 'rater-risk-3', 'statin-dose']

PLACEHOLDER = '工作与生活中的相关计算与查询。'


def build_scene(slug):
    d = json.load(open(DEEP, encoding='utf-8'))
    v = d['cardiology/' + slug]
    sc = v.get('scenarios', [])[:2]
    text = '；'.join(s.strip().rstrip('。') for s in sc) + '。'
    return text


def process(slug, dry=False):
    path = f'{ROOT}/{slug}.html'
    s = open(path, encoding='utf-8').read()
    scene = build_scene(slug)
    # opt-guide 适用场景 <p>
    s2 = s.replace(f'<p>{PLACEHOLDER}</p>', f'<p>{scene}</p>')
    # JSON-LD FAQ「适合哪些场景」answer text
    s2 = s2.replace(f'"text": "{PLACEHOLDER}"', f'"text": "{scene}"')
    # opt-faq 区块 <dd> 套话（HTML FAQ 列表，与 JSON-LD 不同系统）
    s2 = s2.replace(f'<dd>{PLACEHOLDER}</dd>', f'<dd>{scene}</dd>')
    n_opt = s.count(f'<p>{PLACEHOLDER}</p>')
    n_json = s.count(f'"text": "{PLACEHOLDER}"')
    n_dd = s.count(f'<dd>{PLACEHOLDER}</dd>')
    if dry:
        print(f'[dry] {slug}: opt-guide {n_opt} + JSON-LD {n_json} + opt-faq <dd> {n_dd} -> {scene[:40]}...')
        return
    if s2 != s:
        open(path, 'w', encoding='utf-8').write(s2)
        print(f'[ok] {slug}: 清理 opt-guide {n_opt} + JSON-LD {n_json} + opt-faq {n_dd} 处套话')
    else:
        print(f'[skip] {slug}: 未匹配占位（已真实或结构不同）')


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    for slug in TARGETS:
        process(slug, dry=dry)
