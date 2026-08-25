#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复全站 HTML 内的重复 id 与 id 冲突（维护迭代用）。

问题根因：
  1. 235 个工具页同时存在「模板专属介绍」(<div class="tool-intro" id="toolIntro">)
     与「历史注入的通用介绍」(<!-- SEO 介绍区块 --> ... <div class="tool-intro open" id="toolIntro"> ... <!-- /SEO 介绍区块 -->)，
     两处 id 冲突。删除通用块（保留更优质、且被 JS toggleIntro/getElementById 引用的专属块）。
     仅当页内 id="toolIntro" 出现 >1 次时才删，避免误删单介绍块页面。
  2. current-3.html：输入框与结果框共用 id="res" → 结果写到了输入框（显示失效）。
     结果框重命名为 resOut，更新 innerHTML 引用。
  3. elo-rating.html：<select> 与结果框共用 id="result" → 结果写到了 select（显示失效）。
     结果框重命名为 resultBox，更新 innerHTML 引用（select 的 .value 读取保持不变）。

注意：_build.py 不重新注入 SEO 介绍区块（grep 确认 0 处），故手动修复不会被下次构建覆盖。
纯本地文件改写，先备份逻辑由调用方负责。

用法：python3 _fix_dup_ids.py
"""

import os
import re

ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, 'tools')
SKIP_DIRS = {'.git', 'node_modules', '.workbuddy', 'scripts', '_regression_shots',
             '__pycache__', 'venv', 'vendor'}

OPEN_MARK = '<!-- SEO 介绍区块 -->'
CLOSE_MARK = '<!-- /SEO 介绍区块 -->'

# 单页定点修复：(文件路径相对 ROOT, [(旧串, 新串), ...])
TARGETED_FIXES = {
    'tools/automotive/current-3.html': [
        ('<div class="result-box" id="res"></div>',
         '<div class="result-box" id="resOut"></div>'),
        ("document.getElementById('res').innerHTML=",
         "document.getElementById('resOut').innerHTML="),
    ],
    'tools/chess/elo-rating.html': [
        ('<div class="result-box" id="result"></div>',
         '<div class="result-box" id="resultBox"></div>'),
        ("$('result').innerHTML=html",
         "$('resultBox').innerHTML=html"),
    ],
    'tools/fun/tic-tac-toe.html': [
        ('<input type="checkbox" id="playerFirst" checked>',
         '<input type="checkbox" id="playerFirstChk" checked>'),
        ("!document.getElementById('playerFirst').checked",
         "!document.getElementById('playerFirstChk').checked"),
    ],
}


def fix_tool_intro_dupe(content):
    """若页内 id=\"toolIntro\" 出现 >1 次，删除 SEO 介绍区块整块。返回 (新内容, 是否改动)。"""
    if content.count('id="toolIntro"') <= 1:
        return content, False
    if OPEN_MARK not in content or CLOSE_MARK not in content:
        return content, False
    oi = content.index(OPEN_MARK)
    ci = content.index(CLOSE_MARK)
    # 删除 [OPEN_MARK ... CLOSE_MARK]，含首尾换行
    end = ci + len(CLOSE_MARK)
    # 连同前面可能的换行一起去掉
    start = oi
    while start > 0 and content[start - 1] in '\r\n':
        start -= 1
    while end < len(content) and content[end] in '\r\n':
        end += 1
    new = content[:start] + content[end:]
    return new, True


def main():
    changed = 0
    # 1) 批量去重 toolIntro
    for dp, dn, fn in os.walk(TOOLS_DIR):
        parts = dp[len(ROOT):].split(os.sep)
        if any(p in SKIP_DIRS for p in parts):
            continue
        for f in fn:
            if not f.endswith('.html') or f == 'index.html':
                continue
            p = os.path.join(dp, f)
            try:
                c = open(p, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            new_c, did = fix_tool_intro_dupe(c)
            if did:
                open(p, 'w', encoding='utf-8').write(new_c)
                changed += 1
    print('toolIntro 去重页数: %d' % changed)

    # 2) 定点修复 id 冲突页
    for rel, repls in TARGETED_FIXES.items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print('跳过（文件不存在）: %s' % rel)
            continue
        c = open(p, encoding='utf-8', errors='ignore').read()
        before = c
        for old, new in repls:
            if old not in c:
                print('  警告: 未找到替换目标 -> %s :: %r' % (rel, old))
                continue
            c = c.replace(old, new, 1)
        if c != before:
            open(p, 'w', encoding='utf-8').write(c)
            changed += 1
            print('已修复 id 冲突: %s' % rel)
        else:
            print('无改动: %s' % rel)

    print('合计改动文件: %d' % changed)


if __name__ == '__main__':
    main()
