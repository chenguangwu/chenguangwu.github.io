# -*- coding: utf-8 -*-
"""fluid 批1（10 工具）deep-dive 补强：为缺数字算例的 chezy-velocity / cavitation-number 增补可复现算例。

其余 8 个条目已含真实公式 + 数字算例 + 2 FAQ，符合「3 场景 + 1 可复现算例 + 2 FAQ」标准，仅补 2 处缺口。
`--apply` 写入 i18n/tools/content_deepdive.json；否则仅预览校验。
"""
import os, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

PATCH = {
    'fluid/chezy-velocity': {
        'examples': [
            {'title': '公式', 'body': 'V = C·√(R·S)（R 为水力半径，S 为水力坡度/底坡，C 为谢才系数）。'},
            {'title': '算例', 'body': 'V = C·√(R·S)。例：混凝土渠道 C=50、水力半径 R=0.5 m、底坡 S=0.01，V=50×√(0.5×0.01)=50×0.07071≈3.54 m/s；若过水断面 A=2 m²，则流量 Q=V·A≈7.07 m³/s。'},
        ],
    },
    'fluid/cavitation-number': {
        'examples': [
            {'title': '公式', 'body': 'σ = (p − pv)/(½·ρ·v²)。pv 为液体饱和蒸汽压；σ 越小越易空化。'},
            {'title': '算例', 'body': 'σ = (p − pv)/(½·ρ·v²)。例：常温清水 pv=2339 Pa、p=101325 Pa、ρ=1000 kg/m³、v=10 m/s，σ=(101325−2339)/(0.5×1000×100)=98986/50000≈1.98；若叶型临界 σ≈0.3~1，则本例尚未空化，σ 越低越邻近汽蚀阈值。'},
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
