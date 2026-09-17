#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 finance 行业混入的非金融工具：仅改页面 meta 的 industry 字段（分类页按
industry 分组、URL 按目录，故改 industry= 不改变 URL，零 301 风险）。

映射经功能核验（h1/description/cat）确定，目标行业均存在于 INDUSTRY_DEFS：
  driver-license-validator -> life   (驾驶证号格式校验，生活/证件类)
  mirror-text              -> text   (镜像文字，纯文本处理)
  word-wrap                -> text   (自动换行，文本排版)
  word-search              -> fun    (找词游戏)
  dns-record-info          -> network(DNS 记录速查，网络基础设施)
  password                 -> security(密码生成，安全类)
  password-generator-advanced -> security
  vcard-qr                 -> general (名片二维码，通用生成)

currency-converter（货币换算）本质即金融工具，不在此清单（已取证剔除）。

幂等：已是目标 industry 或文件不存在则跳过。dry-run 默认，--apply 落盘。
"""
import sys, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = {
    'driver-license-validator': 'life',
    'mirror-text': 'text',
    'word-wrap': 'text',
    'word-search': 'fun',
    'dns-record-info': 'network',
    'password': 'security',
    'password-generator-advanced': 'security',
    'vcard-qr': 'general',
}


def main():
    apply = '--apply' in sys.argv
    changed = 0
    for slug, target in MAP.items():
        p = os.path.join(ROOT, 'tools/finance', slug + '.html')
        if not os.path.exists(p):
            print(f'[SKIP] {slug}: 文件不存在')
            continue
        src = open(p, encoding='utf-8').read()
        # 仅在 meta content="..." 内替换 industry=finance -> industry=<target>
        pat = re.compile(r'(content="[^"]*?\bindustry=)finance\b')
        m = pat.search(src)
        if not m:
            print(f'[OK] {slug}: 无 industry=finance（已处理）')
            continue
        # 取当前 industry 值确认
        cur = re.search(r'industry=([a-z0-9_-]+)', m.group(0))
        if cur and cur.group(1) == target:
            print(f'[OK] {slug}: 已是 {target}')
            continue
        new = pat.sub(lambda x: x.group(1) + target, src, count=1)
        if not apply:
            print(f'[DRY] {slug}: finance -> {target}')
            changed += 1
            continue
        open(p, 'w', encoding='utf-8').write(new)
        print(f'[APPLY] {slug}: finance -> {target}')
        changed += 1
    print(f'\n待/已改 {changed} 个')
    if not apply:
        print('（dry-run，加 --apply 落盘）')


if __name__ == '__main__':
    main()
