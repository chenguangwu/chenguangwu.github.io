#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复跨行业同名工具的 <title> 重复（SEO 自测发现的真实重复，非三方数据依赖）。

根因：_build.py 的 fix_tool_pages_seo() 写标题用
  _zh_title = _zh_title_of(industry, base) or t.get('name')
其中 _zh_title_of 读 i18n/tools/<ind>.json 的 <base>.zh-CN.title，
该字典优先于 tools.json 的 name —— 因此只改 name 不生效，必须改 zh-CN.title。

本脚本给 6 组（12 个）跨行业同名工具的 zh-CN.title 追加行业限定词，
使标题唯一、消除内部竞争。仅改 i18n 数据，不动 URL/内容/canonical。
幂等：已带限定词则跳过。

用法：
  python3 scripts/fix_title_dup_zh.py            # 干跑，打印将改项
  python3 scripts/fix_title_dup_zh.py --apply     # 写入
"""
import os
import re
import json
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_DIR = os.path.join(ROOT, 'i18n', 'tools')

# (industry, base) -> 限定词；base 为文件去 .html
PAIRS = {
    ('it', 'bayes-theorem'): 'IT',
    ('statistics', 'bayes-theorem'): '统计学',
    ('securities', 'sharpe-ratio'): '证券',
    ('investment', 'sharpe-ratio'): '投资',
    ('niche', 'pet-age'): '冷门',
    ('pet', 'pet-age-converter'): '宠物',
    ('science', 'factorial-calculator'): '科学',
    ('math', 'factorial-calc'): '数学',
    ('hr', 'overtime-pay-calc'): '人力资源',
    ('legal', 'overtime-pay'): '法律',
    ('economics', 'pv-annuity'): '经济学',
    ('insurance', 'annuity-present'): '保险',
}
# 基础标题（无限定词），用于从当前 zh-CN.title 还原并重组
BASE_TITLE = {
    'bayes-theorem': '贝叶斯定理计算器',
    'sharpe-ratio': '夏普比率计算器',
    'pet-age': '宠物年龄换算',
    'pet-age-converter': '宠物年龄换算',
    'factorial-calculator': '阶乘计算器',
    'factorial-calc': '阶乘计算器',
    'overtime-pay-calc': '加班费计算器',
    'overtime-pay': '加班费计算器',
    'pv-annuity': '年金现值计算器',
    'annuity-present': '年金现值计算器',
}


def strip_qualifier(title):
    """去掉已有的 （...） 限定词，回到基础标题。"""
    return re.sub(r'\s*[（(][^（）()]*[）)]\s*$', '', title).strip()


def main():
    apply = '--apply' in sys.argv
    changes = []
    for (ind, base), qual in PAIRS.items():
        fp = os.path.join(I18N_DIR, ind + '.json')
        if not os.path.isfile(fp):
            print(f'  跳过(无 i18n 文件): {fp}')
            continue
        d = json.load(open(fp, encoding='utf-8'))
        entry = d.get(base)
        if not isinstance(entry, dict):
            entry = {}
            d[base] = entry
        zh = entry.get('zh-CN', {})
        if not isinstance(zh, dict):
            zh = {}
            entry['zh-CN'] = zh
        cur = zh.get('title', '')
        base_title = BASE_TITLE.get(base, strip_qualifier(cur) if cur else '')
        new_title = '%s（%s）' % (base_title, qual)
        if cur == new_title:
            continue  # 已正确，幂等跳过
        zh['title'] = new_title
        changes.append((f'{ind}/{base}', cur or '(空)', new_title))
        if apply:
            with open(fp, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
                f.write('\n')
    if not apply:
        print('【干跑】以下 %d 个 zh-CN.title 将追加行业限定词：' % len(changes))
        for path, old, new in changes:
            print(f'  {path}: {old!r} -> {new!r}')
        print('（加 --apply 写入）')
    else:
        print('【已写入】%d 个 zh-CN.title 更新：' % len(changes))
        for path, old, new in changes:
            print(f'  {path}: {old!r} -> {new!r}')
    return len(changes)


if __name__ == '__main__':
    n = main()
    sys.exit(0)
