#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""英文描述生成管线：i18n/tools/_en_desc.json（按 industry/slug 索引）。

背景
----
scripts/tool_desc_source.py::en_desc() 的英文来源只有三档：
  ① i18n en-US.intro（实测 3210 个工具的该字段是套话「X is a free online tool.」，
     剥套话后无实质内容 → 被判空）
  ② scripts/tool_desc_override.py 的 DESC_OVERRIDE（人工精翻，1511 条）
  ③ scripts/zh_en_dict.py 本地词典翻译（长中文句译不出）
三档全落空时，第 ④ 步「中文兜底」会直接把中文描述返回给英文态，
于是首页热门卡片、分类导航、搜索卡片在 ?lang=en-US 下显示中文。
i18n/tools/_en_override.json 与 slug-en.json 的 ed 字段实测 3009/3210 也是同一套
套话，不能作为来源（_build.py 的注释亦已说明禁用）。

本脚本负责生成并维护第四档权威来源：i18n/tools/_en_desc.json。
该文件被 en_desc() 在「人工精翻表」之后读取，命中即返回，不再回落中文。

用法
----
    python3 scripts/gen_en_desc.py --list                 # 输出待生成清单（TSV，供逐条翻译）
    python3 scripts/gen_en_desc.py --list --out /tmp/x.tsv
    python3 scripts/gen_en_desc.py --apply /tmp/batch1.tsv   # 合并一批译文
    python3 scripts/gen_en_desc.py --verify               # 覆盖率与质检报告

TSV 格式（--list 产出即为该格式，前 4 列为只读参考，追加第 5 列英文即可）：
    ind/slug <TAB> 英文名 <TAB> 中文名 <TAB> 中文描述 <TAB> 英文描述
--apply 只读取第 1 列与第 5 列；缺第 5 列或为空的行走跳过。
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

import tool_desc_source as TDS  # noqa: E402

TOOLS_JSON = os.path.join(ROOT, 'json', 'tools.json')
DESC_JSON = os.path.join(ROOT, 'i18n', 'tools', '_en_desc.json')

CJK = re.compile(r'[\u4e00-\u9fff]')
# 生成器套话（出现即判不合格，避免再次污染）
BOILER = re.compile(r'free online tool|client[- ]side|is a free\b|online, free and'
                    r'|free and instant|no data uploaded', re.I)
MIN_LEN, MAX_LEN = 8, 90


def key_of(t):
    """工具条目 -> _en_desc.json 键（industry/slug，与 _en_override.json 同规范）。"""
    return '%s/%s' % (t.get('industry', ''), TDS.slug_of(t))


def load_tools():
    with open(TOOLS_JSON, encoding='utf-8') as f:
        return [x for x in json.load(f) if isinstance(x, dict)]


def load_desc():
    if not os.path.isfile(DESC_JSON):
        return {}
    with open(DESC_JSON, encoding='utf-8') as f:
        d = json.load(f)
    return d if isinstance(d, dict) else {}


def save_desc(d):
    tmp = DESC_JSON + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump({k: d[k] for k in sorted(d)}, f, ensure_ascii=False, indent=1)
    os.replace(tmp, DESC_JSON)


def validate(slug, en):
    """返回 (ok, 原因)。"""
    s = ' '.join((en or '').split())
    if not s:
        return False, '空'
    if CJK.search(s):
        return False, '含中文'
    if BOILER.search(s):
        return False, '命中套话句式'
    if len(s) < MIN_LEN:
        return False, '过短（%d 字符）' % len(s)
    if len(s) > MAX_LEN:
        return False, '过长（%d 字符）' % len(s)
    if not re.search(r'[A-Za-z]{3}', s):
        return False, '无英文单词'
    return True, s


def has_existing_en(t):
    """现有来源（步骤 1 / 1.5 / 3）是否已能给出真英文描述。

    注意不能用 en_desc() 判定：其第 4 步兜底会返回英文名（非中文），
    若用「结果不含中文」当判据会把缺口全判成已满足。
    """
    name_en = (t.get('en') or '').strip()
    entry = TDS.i18n_entry(t) or {}
    en = entry.get('en-US') or {}
    if isinstance(en, dict) and TDS._clean_en(en.get('intro') or '', name_en):
        return True
    ov = TDS._DESC_OVERRIDE.get((t.get('name') or '').strip())
    if ov and isinstance(ov, (list, tuple)) and len(ov) >= 2 and isinstance(ov[1], str):
        if TDS._clean_en(ov[1], name_en):
            return True
    zh = TDS.zh_desc(t)
    if zh:
        tr = TDS._translate_text(zh)
        if tr and tr != zh and not TDS.has_cjk(tr) and TDS._clean_en(tr, name_en):
            return True
    return False


def _cell(s):
    """净化 TSV 单元格：制表符/换行会破坏行结构，统一压成单空格。"""
    return ' '.join((s or '').split())


def cmd_list(args):
    tools = load_tools()
    have = load_desc()
    rows = []
    for t in tools:
        k = key_of(t)
        if k in have:
            continue
        if has_existing_en(t):
            continue                      # 现有来源已给出真英文，无需生成
        rows.append((k,
                     _cell(t.get('en') or t.get('name') or ''),
                     _cell(t.get('name') or ''),
                     _cell(TDS.zh_desc(t, 80))))
    out = args.out
    lines = ['# ind/slug\tEN name\tZH name\tZH desc\tEN desc  <- 在行尾追加英文描述即可']
    for k, en, zhname, zh in rows:
        lines.append('%s\t%s\t%s\t%s\t' % (k, en, zhname, zh))
    text = '\n'.join(lines) + '\n'
    if out:
        with open(out, 'w', encoding='utf-8') as f:
            f.write(text)
        print('待生成 %d 条 → %s' % (len(rows), out))
    else:
        sys.stdout.write(text)
        print('\n# 合计待生成 %d 条' % len(rows), file=sys.stderr)


def cmd_apply(args):
    have = load_desc()
    known = {key_of(t) for t in load_tools()}
    ok = 0
    bad = []
    unknown = []
    for raw in open(args.apply, encoding='utf-8'):
        line = raw.rstrip('\n')
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        parts = line.split('\t')
        if len(parts) < 5:
            continue                        # 尚未填写
        slug = parts[0].strip()
        en = parts[4].strip()
        if not en:
            continue
        if slug not in known:
            unknown.append(slug)
            continue
        good, why = validate(slug, en)
        if not good:
            bad.append((slug, why, en[:50]))
            continue
        have[slug] = why
        ok += 1
    save_desc(have)
    print('已合并 %d 条 → %s（累计 %d 条）' % (ok, DESC_JSON, len(have)))
    if unknown:
        print('⚠️ 未知 slug %d 个：%s' % (len(unknown), unknown[:6]))
    if bad:
        print('⚠️ 未通过校验 %d 条：' % len(bad))
        for s, w, e in bad[:12]:
            print('    %-34s %s  %r' % (s, w, e))


def cmd_verify(args):
    tools = load_tools()
    have = load_desc()
    stat = {'generated': 0, 'other_en': 0, 'fallback_name': 0, 'empty': 0}
    still = []
    for t in tools:
        k = key_of(t)
        if k in have:
            stat['generated'] += 1
            continue
        # 判据必须用 has_existing_en（复刻步骤 1/1.5/3），不能用 en_desc()：
        # en_desc 的第 4 步兜底返回英文名，结果不含中文，会把缺口全判成已满足。
        if has_existing_en(t):
            stat['other_en'] += 1
            continue
        ed = TDS.en_desc(t, 60)
        if not ed:
            stat['empty'] += 1
            still.append((k, '(空)'))
        else:
            stat['fallback_name'] += 1
            still.append((k, ed[:40]))
    print('_en_desc.json 条目: %d' % len(have))
    print('全站 %d 个工具的英文描述来源：' % len(tools))
    print('   新生成表 _en_desc.json : %d' % stat['generated'])
    print('   其它既有英文来源       : %d' % stat['other_en'])
    print('   仅英文名兜底（缺口）   : %d' % stat['fallback_name'])
    print('   空描述                 : %d' % stat['empty'])
    if still:
        print('\n仍缺英文描述的条目（前 20）：')
        for k, v in still[:20]:
            print('   %-40s %s' % (k, v))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--out')
    ap.add_argument('--apply')
    ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()
    if args.list:
        cmd_list(args)
    elif args.apply:
        cmd_apply(args)
    elif args.verify:
        cmd_verify(args)
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
