# -*- coding: utf-8 -*-
"""fluid 批2（10 工具）deep-dive 校正：
- manning-velocity：算例结果笔误 1.94 → 正确 1.53 m/s（与工具 JS 一致，node 复核 (1/0.013)*0.5^(2/3)*sqrt(0.001)=1.5324）
- laplace-sphere-pressure：原仅公式无数字算例，增补可复现算例（单界面 145.6 Pa / 肥皂泡 291.2 Pa）
其余 8 个已含真实公式+数字算例+2 FAQ，符合标准，不动。
`--apply` 写入；否则预览校验。
"""
import os, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

PATCH = {
    'fluid/manning-velocity': {
        'examples': [
            {'title': '公式', 'body': 'V = (1/n)·R^(2/3)·S^(1/2)。例：混凝土渠 n=0.013、水力半径 R=0.5、底坡 S=0.001，V=(1/0.013)×0.5^(2/3)×√0.001≈76.92×0.630×0.0316≈1.53 m/s（与工具实时计算一致）。'},
        ],
    },
    'fluid/laplace-sphere-pressure': {
        'examples': [
            {'title': '公式', 'body': 'Δp = 2γ/R（单界面球）；肥皂泡为双界面 Δp=4γ/R。'},
            {'title': '算例', 'body': 'Δp=2γ/R。例：水 γ=0.0728 N/m、曲率半径 R=1 mm，单界面 Δp=2×0.0728/0.001=145.6 Pa；若肥皂泡（双界面）Δp=4×0.0728/0.001=291.2 Pa，故小泡内压更高。'},
        ],
    },
}


def main():
    d = json.load(open(DD, encoding='utf-8'))
    for k, patch in PATCH.items():
        assert k in d, '缺失条目: %s' % k
        for fld, val in patch.items():
            d[k][fld] = val
        print('PATCH:', k, '| examples=%d' % len(d[k]['examples']))
    if '--apply' not in sys.argv:
        print('预览模式（加 --apply 写入）'); return 0
    json.dump(d, open(DD, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('已写入', DD)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
