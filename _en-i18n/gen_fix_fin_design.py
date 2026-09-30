#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""补录 finance(6 页) + design(2 页) 半译残留键。

形态/稳定性：MERGE 进既有 per-tool 字典（保留原有键），键一律取自探针 --keysrc
给出的 zh 权威源文（半译节点必须以中文源文为键，否则运行时匹配不上）。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')

ADD = {
    'finance': {
        'bond-yield-calculator': {
            '持有期(年)': 'Holding period (years)',
        },
        'depreciation-calculator': {
            '：年折旧额 = (原值 - 残值) / 使用年限':
                ': annual depreciation = (cost - salvage value) / useful life',
        },
        'investment-roi': {
            '= 初始投资 / 年现金流（静态）':
                '= initial investment / annual cash flow (static)',
        },
        'lease-payment-calculator': {
            '残值(元)': 'Residual value (CNY)',
            '手续费(元)': 'Fee (CNY)',
        },
        'tax-bracket': {
            '速算扣除数：用于一次性计算，避免分档累加':
                'Quick deduction: computes the tax in one step, avoiding tier-by-tier accumulation',
            '注：本工具仅作参考，具体以最新税法及当地税务规定为准':
                'Note: this tool is for reference only; always follow the latest tax law and local tax regulations',
        },
        'vat-calculator': {
            '含税价 → 不含税价': 'Tax-inclusive price → ex-tax price',
            '不含税价 → 含税价': 'Ex-tax price → tax-inclusive price',
            '增值税额 = 不含税价 × 税率': 'VAT amount = ex-tax price × tax rate',
            '含税价 = 不含税价 × (1 + 税率)': 'Tax-inclusive price = ex-tax price × (1 + tax rate)',
            '不含税价 = 含税价 ÷ (1 + 税率)': 'Ex-tax price = tax-inclusive price ÷ (1 + tax rate)',
        },
    },
    'design': {
        'px-to-rem': {
            '标题 / 间距': 'Title / spacing',
        },
        'rem-to-px': {
            '标题 / 间距': 'Title / spacing',
        },
    },
}


def validate(ind, slug, add):
    for k, v in add.items():
        if not isinstance(v, str) or v == '':
            print('!! %s/%s empty value for key %r' % (ind, slug, k[:40]))
            sys.exit(1)
        if CJK.search(v):
            print('!! %s/%s CJK in value: %r' % (ind, slug, v[:60]))
            sys.exit(1)
        if CNP.search(v):
            print('!! %s/%s CN punctuation in value: %r' % (ind, slug, v[:60]))
            sys.exit(1)


def main():
    total = 0
    for ind, tools in ADD.items():
        outdir = os.path.join(ROOT, 'i18n', 'tools', 'en', ind)
        for slug, add in tools.items():
            validate(ind, slug, add)
            path = os.path.join(outdir, slug + '.json')
            if not os.path.exists(path):
                print('!! missing dict %s' % path)
                sys.exit(1)
            d = json.load(open(path, encoding='utf-8'))
            m = d.setdefault('map', {})
            added = 0
            for k, v in add.items():
                if k in m:
                    print('   skip existing key %r' % k[:40])
                    continue
                m[k] = v
                added += 1
            json.dump(d, open(path, 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
            open(path, 'a', encoding='utf-8').write('\n')
            total += added
            print('MERGE %s/%s +%d (map now %d)' % (ind, slug, added, len(m)))
    print('gen_fix_fin_design done, added %d keys' % total)


if __name__ == '__main__':
    main()
