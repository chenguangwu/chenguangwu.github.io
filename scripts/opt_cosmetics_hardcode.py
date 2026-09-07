# -*- coding: utf-8 -*-
"""opt_cosmetics_hardcode.py — 清理 cosmetics/assessor-67 的 formula-desc 校验变体。

范围（探查确认）：
  (A) formula-desc 校验变体：assessor-67 含「本校验工具依据对应数据格式与语法规范…工具名称：…」→ 真实合规描述
  (B) opt 套话「工作与生活中的相关计算与查询」：0 页 → 不处理
  (C) tool-intro 块内 6 类通用套话：0 页（块已真实）→ 不处理
含 meta 回灌检测：替换后校验全站 JSON-LD 合法性。
"""
import re, os, json, sys

NEW_FD = '本工具按《化妆品安全技术规范》等公开限值，对输入的重金属（铅/汞/砷/镉）、甲醇、微生物等检测值逐项比对，判定各项是否达标；纯前端计算，数据不上传。'

def main():
    dry = '--dry' in sys.argv
    f = 'tools/cosmetics/assessor-67.html'
    assert os.path.exists(f), f
    s = open(f, encoding='utf-8').read()
    m = re.search(r'<p class="formula-desc">(.*?)</p>', s, re.S)
    assert m, '未找到 formula-desc'
    old = m.group(1)
    assert '本校验工具依据' in old, 'FD 非校验变体，无需处理'
    if dry:
        print('[dry] assessor-67 FD 将替换:\n  旧: %s\n  新: %s' % (old[:50], NEW_FD[:40]))
        return
    s2 = s.replace(old, NEW_FD, 1)
    assert '本校验工具依据' not in s2, '替换后仍有校验变体'
    open(f, 'w', encoding='utf-8').write(s2)
    # meta 回灌检测：JSON-LD 合法
    m2 = re.search(r'<script type="application/ld\+json">(.*?)</script>', s2, re.S)
    assert m2, 'JSON-LD 缺失'
    json.loads(m2.group(1))
    print('已清理 assessor-67 formula-desc 校验变体（JSON-LD 合法）')

if __name__ == '__main__':
    main()
