#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为缺失 phrases 数据的行业生成【可自动推导】的英文短语。

背景
----
js/tool-i18n.js 运行时按需加载 i18n/tools/<industry>-phrases.json，
内容是「页面中文短语 -> 英文」的扁平字典，用于英文模式下翻译正文。
全站仅 96/266 个行业生成过该数据（多为行业独有短语：参数标签、公式说明、
定制 FAQ 等，需真实翻译，脚本不臆造）。

本脚本只生成能 100% 确定、且英文来自站点权威数据的两类条目：
  1. "<中文工具名>"   -> "<英文工具名>"     正文 / 相关工具卡片里出现的工具名
  2. "/ <中文工具名>" -> "/ <英文工具名>"   面包屑（格式与既有 96 个文件一致）

英文来源（均非机翻，避免低质翻译污染站点）：
  - i18n/tools/_en_override.json 的 "<industry>/<slug>" -> {en, ed}
中文来源：
  - i18n/tools/<industry>.json 的 slug -> zh-CN.title / zh-CN.h1

不生成：行业专业短语（公式说明、参数标签、定制 FAQ 等）。
        这些需要真实翻译能力，宁缺毋滥 —— 缺失时页面保持中文，
        远好于给出错误/生硬的英文。

幂等：内容不变则不写盘（避免每次运行产生无意义变更）。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_DIR = os.path.join(ROOT, 'i18n', 'tools')
INDEX_FILE = os.path.join(I18N_DIR, 'phrases-index.json')


def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, OSError, ValueError):
        return None


def existing_industries():
    """已有 phrases 数据的行业（不覆盖既有成果）。"""
    out = set()
    if not os.path.isdir(I18N_DIR):
        return out
    for fn in os.listdir(I18N_DIR):
        if fn.endswith('-phrases.json'):
            out.add(fn[:-len('-phrases.json')])
    return out


def target_industries():
    """所有真正需要 phrases 的行业（URL 行业名，排除 -body 变体与索引）。"""
    out = []
    for fn in sorted(os.listdir(I18N_DIR)):
        if not fn.endswith('.json'):
            continue
        if fn.endswith('-phrases.json') or fn.endswith('-body.json'):
            continue
        if fn in ('phrases-index.json', '_en_override.json', 'slug-en.json'):
            continue
        out.append(fn[:-5])
    return out


def build_for(industry, en_override):
    """为单个行业生成可自动推导的短语字典。"""
    ind_data = load_json(os.path.join(I18N_DIR, industry + '.json'))
    if not isinstance(ind_data, dict):
        return None

    mapping = {}
    for slug, node in ind_data.items():
        if not isinstance(node, dict):
            continue
        zh_node = node.get('zh-CN') or {}
        zh_title = (zh_node.get('title') or zh_node.get('h1') or '').strip()
        if not zh_title:
            continue
        en_node = en_override.get('%s/%s' % (industry, slug))
        if not isinstance(en_node, dict):
            continue
        en_title = (en_node.get('en') or '').strip()
        if not en_title or en_title == zh_title:
            continue
        # 1) 工具名本体（正文 / 相关工具卡片文本）
        mapping.setdefault(zh_title, en_title)
        # 2) 面包屑形态（与既有文件格式一致）
        mapping.setdefault('/ ' + zh_title, '/ ' + en_title)
    return mapping


def main():
    en_override = load_json(os.path.join(I18N_DIR, '_en_override.json'))
    if not isinstance(en_override, dict):
        print('ERROR: 无法读取 _en_override.json', file=sys.stderr)
        return 1

    have = existing_industries()
    targets = [i for i in target_industries() if i not in have]

    written = 0
    total_entries = 0
    skipped_empty = []
    for ind in targets:
        mapping = build_for(ind, en_override)
        if not mapping:
            skipped_empty.append(ind)
            continue
        text = json.dumps(mapping, ensure_ascii=False, indent=1) + '\n'
        out = os.path.join(I18N_DIR, ind + '-phrases.json')
        try:
            with open(out, 'r', encoding='utf-8') as f:
                if f.read() == text:
                    total_entries += len(mapping)
                    continue      # 内容一致 → 不写盘（幂等）
        except (IOError, OSError):
            pass
        with open(out, 'w', encoding='utf-8') as f:
            f.write(text)
        written += 1
        total_entries += len(mapping)

    print('缺失行业数: %d' % len(targets))
    print('新生成文件: %d 个' % written)
    print('生成短语条目: %d 条' % total_entries)
    if skipped_empty:
        print('无可推导数据（跳过）: %d 个行业 -> %s'
              % (len(skipped_empty), ', '.join(skipped_empty[:8])))
    return 0


if __name__ == '__main__':
    sys.exit(main())
