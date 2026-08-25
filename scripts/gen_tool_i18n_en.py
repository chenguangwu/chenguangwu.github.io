#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_tool_i18n_en.py — 工具页正文英文翻译生成器（v2 收尾）

数据源：
  - json/search-index.json  : 全量 5254 工具，每项已含高质量 en（工具名）/ ed（描述）
    （由 scripts/zh_en_dict.py 规则引擎在 _build.py 构建期注入）
  - i18n/tools/<ind>.json    : 已有的 per-industry 字典骨架（含 6 个首页工具的手工 en-US）

产出：
  - i18n/tools/<ind>-body.json : 扁平 { "<slug>": { "title": <en>, "intro": <en> } }
    供 js/tool-i18n.js 在工具页加载/切语时动态翻译 h2 标题与简介段落（纯前端、免改 5254 页 HTML）

规则：
  - title 优先用 search-index 的 en（高质量工具名）；缺失则 translate_name(name)
  - intro 优先用 search-index 的 ed；缺失则 translate_text(desc)
  - 若已有 i18n/tools/<ind>.json 的 en-US.title / en-US.intro（手工翻译），优先采用，避免覆盖
  - 幂等：重复运行结果稳定
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from zh_en_dict import translate_name, translate_text  # noqa: E402

SI_PATH = os.path.join(ROOT, 'json', 'search-index.json')
DICT_DIR = os.path.join(ROOT, 'i18n', 'tools')
OUT_SUFFIX = '-body.json'


def load_existing_en(industry):
    """读取已有字典中的 en-US 手工翻译，返回 {slug: {title, intro}}。"""
    p = os.path.join(DICT_DIR, industry + '.json')
    out = {}
    if not os.path.exists(p):
        return out
    try:
        data = json.load(open(p, encoding='utf-8'))
    except Exception:
        return out
    for slug, entry in data.items():
        if not isinstance(entry, dict):
            continue
        en = entry.get('en-US')
        if not isinstance(en, dict):
            continue
        item = {}
        if en.get('title'):
            item['title'] = en['title']
        if en.get('intro'):
            item['intro'] = en['intro']
        if item:
            out[slug] = item
    return out


def main():
    si = json.load(open(SI_PATH, encoding='utf-8'))
    # 按行业聚合
    by_ind = {}
    # slug -> 真实行业（用于把跨行业登记的手工翻译路由到正确行业）
    slug_ind = {}
    for t in si:
        ind = t.get('i') or (t.get('industry'))
        if not ind:
            continue
        url = t.get('u') or t.get('url') or ''
        slug = url.split('/')[-1].replace('.html', '')
        if not slug:
            continue
        if slug not in slug_ind:
            slug_ind[slug] = ind
        title_en = (t.get('en') or '').strip() or translate_name(t.get('name') or t.get('n') or '')
        intro_en = (t.get('ed') or '').strip() or translate_text(t.get('desc') or t.get('d') or '')
        by_ind.setdefault(ind, {})[slug] = {'title': title_en, 'intro': intro_en}

    stats = {'industries': 0, 'tools': 0, 'merged_hand': 0}
    for ind, bodies in by_ind.items():
        # 合并手工 en-US：按工具真实行业路由（修正跨行业登记被丢弃的问题）
        hand = load_existing_en(ind)
        for slug, item in hand.items():
            target = slug_ind.get(slug, ind)
            if target != ind:
                tb = by_ind.setdefault(target, {})
            else:
                tb = bodies
            if slug_ind.get(slug) != target:
                continue  # 游离手工条目（如纯首页工具），跳过避免孤儿键
            if 'title' in item and item['title']:
                tb.setdefault(slug, {})['title'] = item['title']
                stats['merged_hand'] += 1
            if 'intro' in item and item['intro']:
                tb.setdefault(slug, {})['intro'] = item['intro']
                stats['merged_hand'] += 1
        out_path = os.path.join(DICT_DIR, ind + OUT_SUFFIX)
        json.dump(bodies, open(out_path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=0, separators=(',', ':'))
        stats['industries'] += 1
        stats['tools'] += len(bodies)

    print('[gen_tool_i18n_en] industries=%d tools=%d merged_hand=%d' % (
        stats['industries'], stats['tools'], stats['merged_hand']))


if __name__ == '__main__':
    main()
