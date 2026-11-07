# -*- coding: utf-8 -*-
"""输出 F-N189 页面元信息 JSON，供 _verify_fn189_rollout.mjs 复用同一套解析。

背景：mjs 侧原先自研 parsePage（正则取全文第一个 `exportTable(...)`），第 46 批实测失效：
很多页面「导出 CSV」按钮的 onclick 里就写着 exportTable('#purityTable', ...)，
导致前缀被误判成 purity（真前缀 fertilizer_calculator），整页断言连锁 FAIL、
甚至 eval 出一个不存在的 `__purityResText()` 直接 FATAL。

用法（每次只解析一页，输出单行 JSON；不存在 / 无法解析输出 null）：
  python3 scripts/_fn189_meta.py --file=tools/it/aes-encryptor.html --slug=aes-encryptor
"""
import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _fn189_rollout as R  # noqa: E402


def meta_of(raw, slug):
    m = R.parse_meta(raw, slug)
    if not m:
        return None
    return dict(pre=m['pre'], csv=m['slug'], host=m['host'], resexpr=m['resexpr'],
                calc=m['calc'], start=m['a'], end=m['b'], seg=m['seg'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--file')
    ap.add_argument('--cat')
    ap.add_argument('--slug')
    a = ap.parse_args()
    path = a.file or 'tools/%s/%s.html' % (a.cat, a.slug)
    try:
        raw = io.open(path, encoding='utf-8').read()
    except IOError:
        print('null')
        return
    print(json.dumps(meta_of(raw, a.slug), ensure_ascii=False))


if __name__ == '__main__':
    main()
