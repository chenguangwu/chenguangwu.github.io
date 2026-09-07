# -*- coding: utf-8 -*-
"""opt_fix_example_body.py — 修复 content_deepdive examples 字段名 bug。

_build.py 渲染 examples 读 e.get('body')，但早期真实化分类(construction/consulting/
content/convenience)误用 'code' 字段，导致这些页「示例」区渲染为空。
本脚本把 examples 项中 'code' 字段重命名为 'body'（仅当含 code 且无 body），幂等可恢复。
"""
import json, os

PATH = 'i18n/tools/content_deepdive.json'

def main():
    assert os.path.exists(PATH), PATH
    d = json.load(open(PATH, encoding='utf-8'))
    fixed = 0
    for k, v in d.items():
        for e in (v.get('examples') or []):
            if isinstance(e, dict) and 'code' in e and 'body' not in e:
                e['body'] = e.pop('code')
                fixed += 1
    json.dump(d, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('已修复 examples 字段(code→body): %d 处' % fixed)

if __name__ == '__main__':
    main()
