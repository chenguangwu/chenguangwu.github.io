#!/usr/bin/env python3
"""B-OPT29: 修复存在多个 <h1> 的页面。

策略：保留 <h1 class="sr-only"> 作为页面唯一主标题，
把其余示例/预览内容里的 <h1> 降级为 <h2>。
"""
import os, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TARGET_FILES = [
    'ui/tool-editor.html',
    'tools/biz/text-extract-html-tags.html',
    'tools/biz/lorem-ipsum-advanced.html',
    'tools/biz/markdown.html',
    'tools/it/markdown-editor.html',
    'tools/it/html-formatter.html',
    'tools/it/markdown-to-html.html',
    'tools/it/code-highlighter.html',
    'tools/it/code-runner.html',
    'tools/it/html-tags.html',
]

MARKER = '###SR_ONLY_H1_PLACEHOLDER###'


def fix(path):
    try:
        raw = open(path, 'rb').read()
        text = raw.decode('utf-8')
    except Exception:
        return False
    before = text.count('<h1')
    # 保护 sr-only h1
    text = text.replace('<h1 class="sr-only">', MARKER)
    text = text.replace('</h1>', '</h2>')
    text = text.replace('<h1', '<h2')
    text = text.replace(MARKER, '<h1 class="sr-only">')
    after_h1 = text.count('<h1')
    after_h2 = text.count('<h2')
    if text != raw.decode('utf-8'):
        with open(path, 'wb') as f:
            f.write(text.encode('utf-8'))
        return True, before, after_h1, after_h2
    return False, before, after_h1, after_h2


def main():
    changed = 0
    for rel in TARGET_FILES:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f'[SKIP] 文件不存在: {rel}')
            continue
        modified, before, after_h1, after_h2 = fix(path)
        if modified:
            print(f'[FIXED] {rel}: h1 总数 {before} -> {after_h1}, h2 新增/变更后 {after_h2}')
            changed += 1
        else:
            print(f'[NOOP] {rel}: 无需修改')
    print(f'\n共修复文件数: {changed}')


if __name__ == '__main__':
    main()
